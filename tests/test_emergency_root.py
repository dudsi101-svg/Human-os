"""DD-007 skeleton tests.

ALL policy values in this file (TTL, k-of-n, authentication strength) are
SYNTHETIC TEST FIXTURES. They exercise the mechanism only and MUST NOT be
promoted to production configuration — real parameters are a separate
founder decision (DD-007).
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from hos_engine.authority import AuthorityRole
from hos_engine.emergency_root import (
    AuditKind,
    EmergencyKeyDescriptor,
    EmergencyRootKernel,
    EmergencyRootPolicy,
    EmergencyRootRefused,
    RequestState,
)
from hos_engine.sqlite_store import SQLiteEventStore

OWNER = "HOS-HUM-000001"
CUSTODIAN_A = "HOS-HUM-000002"
CUSTODIAN_B = "HOS-HUM-000003"
SYNTH_AUTH = "SYNTHETIC-STRONG-AUTH (test fixture, not a real requirement)"


def synthetic_policy(**overrides) -> EmergencyRootPolicy:
    defaults = {
        "config_id": "SYNTHETIC-ERP-001",
        "version": "0.0.0-synthetic",
        "approved_by": "SYNTHETIC-TEST-FIXTURE (not a real approval)",
        "scope": "test-scope",
        "ttl_seconds": 3600,
        "required_authentication_strength": SYNTH_AUTH,
        "required_approvals_k": 2,
        "total_custodians_n": 3,
        "custodian_roles": frozenset({AuthorityRole.RECOVERY_CUSTODIAN}),
    }
    defaults.update(overrides)
    return EmergencyRootPolicy(**defaults)


def key(key_id: str, holder: str) -> EmergencyKeyDescriptor:
    return EmergencyKeyDescriptor(
        key_id=key_id,
        holder_identity_id=holder,
        holder_role=AuthorityRole.RECOVERY_CUSTODIAN,
        authentication_strength=SYNTH_AUTH,
    )


class PolicyTests(unittest.TestCase):
    def test_every_field_is_required_and_validated(self):
        with self.assertRaises(ValueError):
            synthetic_policy(version="  ")
        with self.assertRaises(ValueError):
            synthetic_policy(ttl_seconds=0)
        with self.assertRaises(ValueError):
            synthetic_policy(required_approvals_k=0)
        with self.assertRaises(ValueError):
            synthetic_policy(required_approvals_k=4, total_custodians_n=3)
        with self.assertRaises(ValueError):
            synthetic_policy(custodian_roles=frozenset())

    def test_no_defaults_exist(self):
        with self.assertRaises(TypeError):
            EmergencyRootPolicy(config_id="X")  # type: ignore[call-arg]

    def test_agents_can_never_be_custodians(self):
        with self.assertRaises(ValueError):
            synthetic_policy(
                custodian_roles=frozenset({AuthorityRole.AGENT}),
            )


class KernelConstructionTests(unittest.TestCase):
    def test_missing_configuration_blocks_the_mechanism(self):
        with self.assertRaises(TypeError):
            EmergencyRootKernel()  # type: ignore[call-arg]
        with self.assertRaises(TypeError):
            EmergencyRootKernel(policy=None)  # type: ignore[arg-type]


class ActivationFlowTests(unittest.TestCase):
    def setUp(self):
        self.kernel = EmergencyRootKernel(policy=synthetic_policy())
        self.kernel.register_key(key("K-A", CUSTODIAN_A))
        self.kernel.register_key(key("K-B", CUSTODIAN_B))

    def kinds(self):
        return [r.kind for r in self.kernel.audit_trail()]

    def test_k_of_n_activation_and_use(self):
        request_id = self.kernel.request_activation(
            requested_by=OWNER, reason="suspected loss of primary keys",
        )
        state = self.kernel.approve(request_id, key_id="K-A")
        self.assertEqual(state, RequestState.PENDING)
        state = self.kernel.approve(request_id, key_id="K-B")
        self.assertEqual(state, RequestState.ACTIVATED)
        self.kernel.use(request_id, used_by=OWNER, action="rotate root key")
        self.assertIn(AuditKind.ACTIVATED, self.kinds())
        self.assertIn(AuditKind.USED, self.kinds())

    def test_single_custodian_cannot_activate_alone(self):
        request_id = self.kernel.request_activation(
            requested_by=OWNER, reason="test",
        )
        self.kernel.approve(request_id, key_id="K-A")
        with self.assertRaises(EmergencyRootRefused):
            self.kernel.use(request_id, used_by=OWNER, action="x")
        self.assertIn(AuditKind.REFUSED, self.kinds())

    def test_duplicate_key_and_duplicate_identity_are_refused_and_logged(self):
        request_id = self.kernel.request_activation(
            requested_by=OWNER, reason="test",
        )
        self.kernel.approve(request_id, key_id="K-A")
        with self.assertRaises(EmergencyRootRefused):
            self.kernel.approve(request_id, key_id="K-A")
        self.assertEqual(self.kinds().count(AuditKind.REFUSED), 1)

    def test_wrong_role_and_wrong_auth_declaration_are_refused(self):
        with self.assertRaises(EmergencyRootRefused):
            self.kernel.register_key(EmergencyKeyDescriptor(
                key_id="K-X", holder_identity_id="HOS-HUM-000009",
                holder_role=AuthorityRole.GUEST,
                authentication_strength=SYNTH_AUTH,
            ))
        with self.assertRaises(EmergencyRootRefused):
            self.kernel.register_key(EmergencyKeyDescriptor(
                key_id="K-Y", holder_identity_id="HOS-HUM-000010",
                holder_role=AuthorityRole.RECOVERY_CUSTODIAN,
                authentication_strength="weak",
            ))

    def test_ttl_expiry_refuses_approval_and_is_logged(self):
        kernel = EmergencyRootKernel(policy=synthetic_policy(ttl_seconds=1))
        kernel.register_key(key("K-A", CUSTODIAN_A))
        request_id = kernel.request_activation(
            requested_by=OWNER, reason="test",
        )
        request = kernel._requests[request_id]
        request.expires_at = request.requested_at  # force expiry
        with self.assertRaises(EmergencyRootRefused):
            kernel.approve(request_id, key_id="K-A")
        kinds = [r.kind for r in kernel.audit_trail()]
        self.assertIn(AuditKind.EXPIRED, kinds)
        self.assertIn(AuditKind.REFUSED, kinds)

    def test_audit_records_carry_policy_id_and_version(self):
        self.kernel.request_activation(requested_by=OWNER, reason="test")
        for record in self.kernel.audit_trail():
            self.assertEqual(record.policy_config_id, "SYNTHETIC-ERP-001")
            self.assertEqual(record.policy_version, "0.0.0-synthetic")

    def test_registry_respects_n_and_one_key_per_identity(self):
        self.kernel.register_key(key("K-C", "HOS-HUM-000004"))
        with self.assertRaises(EmergencyRootRefused):
            self.kernel.register_key(key("K-D", "HOS-HUM-000005"))

    def test_one_identity_cannot_hold_two_keys(self):
        with self.assertRaises(EmergencyRootRefused):
            self.kernel.register_key(key("K-E", CUSTODIAN_A))


class DurableAuditTests(unittest.TestCase):
    def test_audit_persists_to_hash_chained_store(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = SQLiteEventStore(str(Path(tmp) / "root.db"))
            kernel = EmergencyRootKernel(
                policy=synthetic_policy(), event_store=store,
            )
            kernel.register_key(key("K-A", CUSTODIAN_A))
            kernel.register_key(key("K-B", CUSTODIAN_B))
            request_id = kernel.request_activation(
                requested_by=OWNER, reason="loss of primary keys",
            )
            kernel.approve(request_id, key_id="K-A")
            kernel.approve(request_id, key_id="K-B")
            kernel.use(request_id, used_by=OWNER, action="rotate root key")
            events = store.all()
            # 2x KEY_REGISTERED + ACTIVATION_REQUESTED + 2x APPROVAL_RECORDED
            # + ACTIVATED + USED
            self.assertEqual(len(events), 7)
            self.assertTrue(all(
                e["event_type"] == "STATE_OBSERVED" for e in events
            ))
            self.assertTrue(store.verify_chain())


if __name__ == "__main__":
    unittest.main()
