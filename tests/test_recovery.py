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


if __name__ == "__main__":
    unittest.main()
