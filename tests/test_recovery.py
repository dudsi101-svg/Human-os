from __future__ import annotations

import tempfile
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path

from hos_engine.authority import AuthorityRole, RoleGrantRegistry
from hos_engine.hub_entity_registry import EntityRegistry, HubEntityStatus, HubEntityType
from hos_engine.recovery import (
    AUTO_TRIGGER_ALLOWED,
    CONSTITUTIONAL_RISK_FOR_MODE,
    EmergencyMode,
    RecoveryRefused,
    SovereignRecoveryKernel,
    TriggerKind,
)
from hos_engine.sqlite_store import SQLiteEventStore

OWNER = "HOS-HUM-000001"
CUSTODIAN = "HOS-HUM-000002"


def far_future() -> str:
    return (datetime.now(UTC) + timedelta(hours=1)).isoformat()


def activate(kernel: SovereignRecoveryKernel, **overrides):
    defaults = {
        "mode": EmergencyMode.SAFE_MODE,
        "initiator_id": OWNER,
        "initiator_role": AuthorityRole.OWNER,
        "scope": "system",
        "reason": "suspected device compromise",
        "expires_at": far_future(),
        "verification_method": "recovery-key+strong-auth",
    }
    defaults.update(overrides)
    return kernel.activate(**defaults)


class ActivationTests(unittest.TestCase):
    def setUp(self):
        self.kernel = SovereignRecoveryKernel()

    def test_owner_activates_safe_mode_and_it_is_scoped(self):
        activation = activate(self.kernel)
        self.assertTrue(self.kernel.is_active(EmergencyMode.SAFE_MODE, scope="system"))
        self.assertFalse(self.kernel.is_active(EmergencyMode.SAFE_MODE, scope="gmail"))
        self.assertEqual(activation.constitutional_risk, "R0")

    def test_every_mode_has_a_constitutional_risk_mapping(self):
        for mode in EmergencyMode:
            self.assertIn(CONSTITUTIONAL_RISK_FOR_MODE[mode], {"R0", "R1", "R2", "R3"})

    def test_expired_activation_is_not_active(self):
        past = (datetime.now(UTC) - timedelta(seconds=1)).isoformat()
        activate(self.kernel, expires_at=past)
        self.assertFalse(self.kernel.is_active(EmergencyMode.SAFE_MODE, scope="system"))

    def test_agent_activation_is_refused_and_logged(self):
        with self.assertRaises(RecoveryRefused):
            activate(self.kernel, initiator_role=AuthorityRole.AGENT, initiator_id="HOS-AGT-1")
        self.assertFalse(self.kernel.is_active(EmergencyMode.SAFE_MODE, scope="system"))
        events = self.kernel.events()
        self.assertEqual(len(events), 1)
        self.assertTrue(events[0].result.startswith("REFUSED"))

    def test_service_and_system_process_are_excluded_too(self):
        for role in (AuthorityRole.SERVICE, AuthorityRole.SYSTEM_PROCESS):
            with self.assertRaises(RecoveryRefused):
                activate(self.kernel, initiator_role=role)


class TriggerPolicyTests(unittest.TestCase):
    def setUp(self):
        self.kernel = SovereignRecoveryKernel()

    def test_protective_modes_may_auto_trigger_with_notification(self):
        for mode in AUTO_TRIGGER_ALLOWED:
            activation = activate(
                self.kernel, mode=mode, scope=f"scope-{mode.value}",
                trigger=TriggerKind.AUTOMATIC_ANOMALY, owner_notified=True,
                initiator_role=AuthorityRole.OPERATOR,
            )
            self.assertTrue(activation.owner_notified)

    def test_auto_trigger_without_notification_is_refused(self):
        with self.assertRaises(RecoveryRefused):
            activate(
                self.kernel, trigger=TriggerKind.AUTOMATIC_ANOMALY,
                owner_notified=False, initiator_role=AuthorityRole.OPERATOR,
            )

    def test_consequential_modes_never_auto_trigger(self):
        for mode in (EmergencyMode.ROLLBACK, EmergencyMode.EXPORT, EmergencyMode.RECOVERY):
            with self.assertRaises(RecoveryRefused):
                activate(
                    self.kernel, mode=mode, trigger=TriggerKind.AUTOMATIC_ANOMALY,
                    owner_notified=True, custodian_approval_by=CUSTODIAN,
                    initiator_role=AuthorityRole.OPERATOR,
                )

    def test_auto_triggered_activation_is_reversible_by_owner(self):
        activation = activate(
            self.kernel, trigger=TriggerKind.AUTOMATIC_ANOMALY, owner_notified=True,
            initiator_role=AuthorityRole.OPERATOR, initiator_id="HOS-SYS-MON",
        )
        self.kernel.deactivate(
            activation.activation_id, initiator_id=OWNER,
            initiator_role=AuthorityRole.OWNER, reason="false alarm",
        )
        self.assertFalse(self.kernel.is_active(EmergencyMode.SAFE_MODE, scope="system"))

    def test_agent_cannot_deactivate(self):
        activation = activate(self.kernel)
        with self.assertRaises(RecoveryRefused):
            self.kernel.deactivate(
                activation.activation_id, initiator_id="HOS-AGT-1",
                initiator_role=AuthorityRole.AGENT, reason="agent tries to lift protection",
            )
        self.assertTrue(self.kernel.is_active(EmergencyMode.SAFE_MODE, scope="system"))


class DualKeyTests(unittest.TestCase):
    def setUp(self):
        self.roles = RoleGrantRegistry()
        self.roles.grant(identity_id=OWNER, role=AuthorityRole.OWNER, scope="system", issued_by=OWNER)
        self.roles.grant(
            identity_id=CUSTODIAN, role=AuthorityRole.RECOVERY_CUSTODIAN,
            scope="system", issued_by=OWNER,
        )
        self.kernel = SovereignRecoveryKernel(roles=self.roles)

    def test_rollback_requires_custodian_approval(self):
        with self.assertRaises(RecoveryRefused):
            activate(self.kernel, mode=EmergencyMode.ROLLBACK)

    def test_custodian_must_differ_from_initiator(self):
        with self.assertRaises(RecoveryRefused):
            activate(self.kernel, mode=EmergencyMode.ROLLBACK, custodian_approval_by=OWNER)

    def test_custodian_without_grant_is_refused(self):
        with self.assertRaises(RecoveryRefused):
            activate(self.kernel, mode=EmergencyMode.RECOVERY, custodian_approval_by="HOS-HUM-000099")

    def test_dual_key_activation_succeeds_with_real_grants(self):
        activation = activate(
            self.kernel, mode=EmergencyMode.RECOVERY, custodian_approval_by=CUSTODIAN,
        )
        self.assertEqual(activation.constitutional_risk, "R3")
        self.assertEqual(activation.custodian_approval_by, CUSTODIAN)

    def test_initiator_without_owner_grant_is_refused(self):
        with self.assertRaises(RecoveryRefused):
            activate(self.kernel, initiator_id="HOS-HUM-000077")


class AuditTests(unittest.TestCase):
    def test_thirteen_field_event_and_refusals_are_logged(self):
        kernel = SovereignRecoveryKernel(signing_secret=b"local-reference-secret")
        activate(kernel)
        with self.assertRaises(RecoveryRefused):
            activate(kernel, initiator_role=AuthorityRole.AGENT)
        events = kernel.events()
        self.assertEqual(len(events), 2)
        activated, refused = events
        self.assertEqual(activated.result, "ACTIVATED")
        self.assertTrue(refused.result.startswith("REFUSED"))
        for event in events:
            self.assertTrue(event.event_id.startswith("HOS-EMG-"))
            self.assertIsNotNone(event.signature)
            self.assertEqual(event.recovery_mode, EmergencyMode.SAFE_MODE.value)

    def test_durable_log_chains_in_sqlite(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = SQLiteEventStore(str(Path(tmp) / "recovery.db"))
            kernel = SovereignRecoveryKernel(event_store=store)
            activate(kernel)
            activate(kernel, mode=EmergencyMode.READ_ONLY, scope="finances")
            self.assertTrue(store.verify_chain())


class SnapshotRollbackContractTests(unittest.TestCase):
    def setUp(self):
        self.entities = EntityRegistry()
        self.entity = self.entities.register(
            entity_type=HubEntityType.RESOURCE, working_name="Notatnik projektu",
            responsibility_owner_id=OWNER, provenance_source="test",
        )
        self.roles = RoleGrantRegistry()
        self.roles.grant(identity_id=OWNER, role=AuthorityRole.OWNER,
                         scope="*", issued_by=OWNER)
        self.roles.grant(identity_id=CUSTODIAN, role=AuthorityRole.RECOVERY_CUSTODIAN,
                         scope="*", issued_by=OWNER)
        self.kernel = SovereignRecoveryKernel(roles=None, entities=self.entities)

    def snapshot(self):
        return self.kernel.create_recovery_snapshot(
            initiator_id=OWNER, initiator_role=AuthorityRole.OWNER,
            scope="projekt", entity_ids=(self.entity.entity_id,),
            reason="checkpoint before risky change", verification_method="recovery-key",
        )

    def test_snapshot_captures_state_and_is_audited(self):
        snap = self.snapshot()
        self.assertTrue(snap.snapshot_id.startswith("HOS-SNP-"))
        self.assertEqual(snap.entity_states[0][1], "Notatnik projektu")
        self.assertIn("SNAPSHOT_CREATED", [e.result for e in self.kernel.events()])

    def test_agent_cannot_create_snapshot(self):
        with self.assertRaises(RecoveryRefused):
            self.kernel.create_recovery_snapshot(
                initiator_id="HOS-AGT-1", initiator_role=AuthorityRole.AGENT,
                scope="projekt", entity_ids=(self.entity.entity_id,),
                reason="agent tries", verification_method="none",
            )
        self.assertTrue(self.kernel.events()[-1].result.startswith("REFUSED"))

    def test_rollback_creates_new_version_and_keeps_history(self):
        snap = self.snapshot()
        self.entities.transition(self.entity.entity_id, HubEntityStatus.ACTIVE)
        restored = self.kernel.rollback_entity(
            snapshot_id=snap.snapshot_id, entity_id=self.entity.entity_id,
            initiator_id=OWNER, initiator_role=AuthorityRole.OWNER,
            custodian_approval_by=CUSTODIAN, reason="undo risky change",
            expires_at=far_future(), verification_method="recovery-key+strong-auth",
        )
        self.assertNotEqual(restored.entity_id, self.entity.entity_id)
        self.assertEqual(restored.working_name, "Notatnik projektu")
        old = self.entities.get(self.entity.entity_id)
        self.assertEqual(old.status, HubEntityStatus.SUPERSEDED)  # never deleted
        merge = self.entities.merge_record_for(self.entity.entity_id)
        self.assertIsNotNone(merge)
        self.assertEqual(merge.evidence, snap.snapshot_id)  # provenance chain

    def test_rollback_requires_dual_key(self):
        snap = self.snapshot()
        with self.assertRaises(RecoveryRefused):
            self.kernel.rollback_entity(
                snapshot_id=snap.snapshot_id, entity_id=self.entity.entity_id,
                initiator_id=OWNER, initiator_role=AuthorityRole.OWNER,
                custodian_approval_by=None, reason="no custodian",
                expires_at=far_future(), verification_method="recovery-key",
            )
        self.assertEqual(self.entities.get(self.entity.entity_id).status,
                         HubEntityStatus.PROPOSED)  # nothing changed


class DisconnectExportContractTests(unittest.TestCase):
    def setUp(self):
        self.entities = EntityRegistry()
        self.entity = self.entities.register(
            entity_type=HubEntityType.RESOURCE, working_name="Dysk w chmurze",
            responsibility_owner_id=OWNER, provenance_source="test",
        )
        self.kernel = SovereignRecoveryKernel(entities=self.entities)

    def test_disconnect_preserves_historical_relation(self):
        rec = self.kernel.disconnect_representation(
            entity_id=self.entity.entity_id, representation="gdrive-sync",
            initiator_id=OWNER, initiator_role=AuthorityRole.OWNER,
            reason="suspected token leak", expires_at=far_future(),
            verification_method="recovery-key",
        )
        kept = self.kernel.disconnected_representations(self.entity.entity_id)
        self.assertEqual([r.disconnect_id for r in kept], [rec.disconnect_id])
        self.assertTrue(self.kernel.is_active(
            EmergencyMode.DISCONNECT,
            scope=f"representation:{self.entity.entity_id}:gdrive-sync"))

    def test_export_builds_portable_package_including_history(self):
        self.kernel.create_recovery_snapshot(
            initiator_id=OWNER, initiator_role=AuthorityRole.OWNER,
            scope="system", entity_ids=(self.entity.entity_id,),
            reason="pre-export checkpoint", verification_method="recovery-key",
        )
        pkg = self.kernel.export_sovereign_package(
            initiator_id=OWNER, initiator_role=AuthorityRole.OWNER,
            scope="system", reason="right to exit", expires_at=far_future(),
            verification_method="recovery-key",
        )
        self.assertEqual(pkg["format"], "open-json")
        self.assertEqual(len(pkg["entities"]), 1)
        self.assertEqual(len(pkg["snapshots"]), 1)
        self.assertTrue(pkg["emergency_events"])  # audit rides along

    def test_export_never_auto_triggers(self):
        with self.assertRaises(RecoveryRefused):
            self.kernel.activate(
                mode=EmergencyMode.EXPORT, initiator_id="HOS-SYS-MON",
                initiator_role=AuthorityRole.OPERATOR, scope="system",
                reason="auto export attempt", expires_at=far_future(),
                verification_method="none", trigger=TriggerKind.AUTOMATIC_ANOMALY,
                owner_notified=True,
            )


class FreezeContractTests(unittest.TestCase):
    def test_freeze_suspends_entity_without_destroying_it(self):
        entities = EntityRegistry()
        entity = entities.register(
            entity_type=HubEntityType.RESOURCE, working_name="Cloud drive",
            responsibility_owner_id=OWNER, provenance_source="test",
        )
        kernel = SovereignRecoveryKernel(entities=entities)
        frozen = kernel.freeze_entity(
            entity.entity_id, initiator_id=OWNER, initiator_role=AuthorityRole.OWNER,
            reason="account takeover suspected", expires_at=far_future(),
            verification_method="recovery-key",
        )
        self.assertEqual(frozen.status, HubEntityStatus.SUSPENDED)
        self.assertEqual(entities.get(entity.entity_id).working_name, "Cloud drive")
        self.assertTrue(kernel.is_active(EmergencyMode.FREEZE, scope=f"entity:{entity.entity_id}"))


class CanonicalEventTypeTests(unittest.TestCase):
    """DD-003: recovery outcomes map to the canonical event vocabulary."""

    def kernel_with_store(self, tmp):
        store = SQLiteEventStore(str(Path(tmp) / "recovery.db"))
        return store, SovereignRecoveryKernel(event_store=store)

    def types_in(self, store):
        return [e["event_type"] for e in store.all()]

    def test_activation_maps_to_recovery_activated(self):
        with tempfile.TemporaryDirectory() as tmp:
            store, kernel = self.kernel_with_store(tmp)
            activate(kernel)
            self.assertEqual(self.types_in(store), ["RECOVERY_ACTIVATED"])

    def test_deactivation_maps_to_recovery_deactivated(self):
        with tempfile.TemporaryDirectory() as tmp:
            store, kernel = self.kernel_with_store(tmp)
            activation = activate(kernel)
            kernel.deactivate(
                activation.activation_id, initiator_id=OWNER,
                initiator_role=AuthorityRole.OWNER, reason="threat cleared",
            )
            self.assertEqual(
                self.types_in(store),
                ["RECOVERY_ACTIVATED", "RECOVERY_DEACTIVATED"],
            )

    def test_refusal_maps_to_recovery_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            store, kernel = self.kernel_with_store(tmp)
            with self.assertRaises(RecoveryRefused):
                activate(kernel, initiator_role=AuthorityRole.AGENT,
                         initiator_id="HOS-AGT-000001")
            self.assertEqual(self.types_in(store), ["RECOVERY_REFUSED"])

    def test_freeze_maps_to_entity_frozen(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = SQLiteEventStore(str(Path(tmp) / "recovery.db"))
            entities = EntityRegistry()
            entity = entities.register(
                entity_type=HubEntityType.RESOURCE, working_name="Notatnik",
                responsibility_owner_id=OWNER, provenance_source="test",
            )
            kernel = SovereignRecoveryKernel(event_store=store, entities=entities)
            kernel.freeze_entity(
                entity.entity_id, initiator_id=OWNER,
                initiator_role=AuthorityRole.OWNER, reason="containment",
                expires_at=far_future(), verification_method="recovery-key",
            )
            self.assertEqual(self.types_in(store), ["ENTITY_FROZEN"])

    def test_usage_records_stay_state_observed(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = SQLiteEventStore(str(Path(tmp) / "recovery.db"))
            entities = EntityRegistry()
            entity = entities.register(
                entity_type=HubEntityType.RESOURCE, working_name="Notatnik",
                responsibility_owner_id=OWNER, provenance_source="test",
            )
            kernel = SovereignRecoveryKernel(event_store=store, entities=entities)
            kernel.create_recovery_snapshot(
                initiator_id=OWNER, initiator_role=AuthorityRole.OWNER,
                scope="projekt", entity_ids=(entity.entity_id,),
                reason="checkpoint", verification_method="recovery-key",
            )
            types = self.types_in(store)
            # RECOVERY mode activation precedes the snapshot usage record
            # only if snapshotting activates a mode; the usage record itself
            # must remain STATE_OBSERVED.
            self.assertIn("STATE_OBSERVED", types)
            self.assertNotIn("RECOVERY_REFUSED", types)

    def test_full_envelope_validates_against_event_schema(self):
        """DD-010 resolved: the HOSId pattern now covers hex IDs, so the
        whole canonical envelope validates. Storage-layer fields (the hash
        chain) and the storage layer's explicit None for an absent
        causation_id are stripped first - they belong to sqlite_store's
        persistence format, not to the canonical event."""
        from hos_engine.validation import SchemaRegistry
        with tempfile.TemporaryDirectory() as tmp:
            store, kernel = self.kernel_with_store(tmp)
            activation = activate(kernel)
            kernel.deactivate(
                activation.activation_id, initiator_id=OWNER,
                initiator_role=AuthorityRole.OWNER, reason="threat cleared",
            )
            registry = SchemaRegistry(Path(__file__).parent.parent / "schemas")
            for event in store.all():
                canonical = {
                    key: value for key, value in event.items()
                    if key not in ("event_hash", "previous_hash")
                    and value is not None
                }
                registry.validate("event.schema.json", canonical)

    def test_new_types_are_canonical_in_dictionary_and_schema(self):
        import json
        root = Path(__file__).parent.parent
        dictionary = json.loads((root / "event.types.json").read_text())["event_types"]
        schema = json.loads((root / "schemas" / "event.schema.json").read_text())
        enum = schema["properties"]["event_type"]["enum"]
        self.assertEqual(set(dictionary), set(enum))
        with tempfile.TemporaryDirectory() as tmp:
            store, kernel = self.kernel_with_store(tmp)
            activation = activate(kernel)
            kernel.deactivate(
                activation.activation_id, initiator_id=OWNER,
                initiator_role=AuthorityRole.OWNER, reason="threat cleared",
            )
            for event in store.all():
                self.assertIn(event["event_type"], dictionary)
                self.assertIn(event["event_type"], enum)

    def test_historical_state_observed_events_remain_readable(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = SQLiteEventStore(str(Path(tmp) / "recovery.db"))
            # a pre-DD-003 durable recovery event, exactly as recovery.py
            # wrote it before the canonical types existed
            store.append({
                "id": "HOS-EMG-LEGACY000001",
                "event_type": "STATE_OBSERVED",
                "occurred_at": "2026-08-15T10:00:00+00:00",
                "actor_id": OWNER,
                "subject_ids": ["system"],
                "payload": {"recovery_mode": "SAFE_MODE", "result": "ACTIVATED"},
                "correlation_id": "HOS-EMG-LEGACY000001",
                "immutable": True,
            })
            kernel = SovereignRecoveryKernel(event_store=store)
            activate(kernel)
            types = self.types_in(store)
            self.assertEqual(types, ["STATE_OBSERVED", "RECOVERY_ACTIVATED"])
            self.assertTrue(store.verify_chain())


if __name__ == "__main__":
    unittest.main()
