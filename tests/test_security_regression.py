"""Security regression set (SECURITY_REVIEW_PROTOCOL.md §6).

Each test is an ABUSE ATTEMPT that must be refused. A failure here is a
security regression, not an ordinary test failure. New CRITICAL/HIGH
findings that get fixed must leave a regression test in this file.

First run: security review REVIEW_2026-08-17. All attempts below are
refused on the reviewed commit — see docs/security-reviews/.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from hos_engine.agent_runtime import (
    AgentManifest,
    AgentRegistry,
    AgentRuntime,
    ApprovalMode,
    Capability,
    CapabilityRegistry,
    Delegation,
    InvocationRequest,
    RiskLevel,
)
from hos_engine.authority import AuthorityRole, RoleGrantRegistry
from hos_engine.protocol_security import HMACSigner, secure_envelope
from hos_engine.recovery import EmergencyMode, RecoveryRefused, SovereignRecoveryKernel
from hos_engine.replay_guard import ReplayGuard
from hos_engine.security_gateway import SecurityGateway
from hos_engine.security_identity import (
    IdentityRegistry,
    IdentityType,
    KeyDescriptor,
)
from hos_engine.sqlite_store import SQLiteEventStore
from hos_engine.trust import TrustLevel, TrustPolicy, TrustRegistry

OWNER = "HOS-HUM-000001"


# ---- 2.1 protocol signatures --------------------------------------------

class SignatureAbuseTests(unittest.TestCase):
    def setUp(self):
        self.signer = HMACSigner("HOS-KEY-1", b"correct-horse")
        self.env = secure_envelope(
            protocol="HOSP/0.2", message_type="hos.query", sender_id=OWNER,
            recipient_id="HOS-HUB-1", subject_id=OWNER, purpose="read",
            payload={"domain": "health"},
        )

    def test_tampered_payload_fails_verification(self):
        signed = self.signer.sign(self.env)
        signed.envelope["payload"]["domain"] = "finance"
        self.assertFalse(self.signer.verify(signed))

    def test_wrong_key_fails_verification(self):
        signed = self.signer.sign(self.env)
        self.assertFalse(HMACSigner("HOS-KEY-1", b"wrong-secret").verify(signed))

    def test_malformed_signature_returns_false_not_raise(self):
        signed = self.signer.sign(self.env)
        object.__setattr__(signed.signature, "value", "!!!not base64!!!")
        self.assertFalse(self.signer.verify(signed))


# ---- 2.3 / 2.4 gateway, replay, expiry, trust ---------------------------

class GatewayAbuseTests(unittest.TestCase):
    def setUp(self):
        self.ids = IdentityRegistry()
        self.ids.register_identity(identity_id=OWNER, identity_type=IdentityType.HUMAN,
                                   display_name="Owner", owner_id=OWNER)
        self.ids.attach_key(OWNER, KeyDescriptor(
            key_id="HOS-KEY-1", algorithm="HMAC-SHA256", public_material="x",
            created_at="2026-08-17T00:00:00+00:00"))
        self.signer = HMACSigner("HOS-KEY-1", b"s3cret")
        self.trust = TrustRegistry()
        self.trust.set_policy(TrustPolicy(
            policy_id="P1", identity_id=OWNER, trust_level=TrustLevel.TRUSTED,
            allowed_message_types={"hos.query"}, allowed_purposes={"read"},
            allowed_domains={"health"},
        ))
        self.guard = ReplayGuard()
        self.gw = SecurityGateway(self.ids, self.trust, self.guard,
                                  {"HOS-KEY-1": self.signer})

    def _signed(self, *, purpose="read", **over):
        env = secure_envelope(
            protocol="HOSP/0.2", message_type="hos.query", sender_id=OWNER,
            recipient_id="HOS-HUB-1", subject_id=OWNER, purpose=purpose,
            payload={"domain": "health"}, **over,
        )
        return self.signer.sign(env)

    def test_replayed_nonce_is_denied(self):
        signed = self._signed()
        self.assertTrue(self.gw.evaluate(signed).accepted)
        # same envelope again -> replay
        self.assertFalse(self.gw.evaluate(signed).accepted)

    def test_expired_envelope_is_denied(self):
        signed = self._signed(ttl_seconds=1)
        # evaluate far in the future
        decision = self.gw.evaluate(signed, now_epoch=9_999_999_999.0)
        self.assertFalse(decision.accepted)
        self.assertEqual(decision.reason, "Envelope expired")

    def test_unknown_sender_is_denied(self):
        env = secure_envelope(
            protocol="HOSP/0.2", message_type="hos.query", sender_id="HOS-HUM-999",
            recipient_id="HOS-HUB-1", subject_id=OWNER, purpose="read",
            payload={"domain": "health"},
        )
        self.assertFalse(self.gw.evaluate(self.signer.sign(env)).accepted)

    def test_purpose_outside_policy_is_denied(self):
        self.assertFalse(self.gw.evaluate(self._signed(purpose="write")).accepted)

    def test_domain_omission_does_not_widen_to_wildcard(self):
        # payload without domain -> "*", policy allows only "health"
        env = secure_envelope(
            protocol="HOSP/0.2", message_type="hos.query", sender_id=OWNER,
            recipient_id="HOS-HUB-1", subject_id=OWNER, purpose="read",
            payload={},
        )
        self.assertFalse(self.gw.evaluate(self.signer.sign(env)).accepted)


# ---- 2.6 recovery / emergency guarantees --------------------------------

class RecoveryAbuseTests(unittest.TestCase):
    def test_agent_cannot_activate_recovery(self):
        kernel = SovereignRecoveryKernel()
        with self.assertRaises(RecoveryRefused):
            kernel.activate(
                mode=EmergencyMode.SAFE_MODE, initiator_id="HOS-AGT-1",
                initiator_role=AuthorityRole.AGENT, scope="system",
                reason="malicious", expires_at="2999-01-01T00:00:00+00:00",
                verification_method="none",
            )

    def test_dual_key_rejects_same_identity_as_custodian(self):
        roles = RoleGrantRegistry()
        roles.grant(identity_id=OWNER, role=AuthorityRole.OWNER, scope="*",
                    issued_by=OWNER)
        roles.grant(identity_id=OWNER, role=AuthorityRole.RECOVERY_CUSTODIAN,
                    scope="*", issued_by=OWNER)
        kernel = SovereignRecoveryKernel(roles=roles)
        with self.assertRaises(RecoveryRefused):
            kernel.activate(
                mode=EmergencyMode.ROLLBACK, initiator_id=OWNER,
                initiator_role=AuthorityRole.OWNER, scope="*",
                reason="self-approved rollback", custodian_approval_by=OWNER,
                expires_at="2999-01-01T00:00:00+00:00",
                verification_method="recovery-key",
            )

    def test_recovery_kernel_exposes_no_policy_mutator(self):
        kernel = SovereignRecoveryKernel()
        public = [n for n in dir(kernel) if not n.startswith("_")]
        for forbidden in ("set_policy", "disable_audit", "clear_events",
                          "set_auto_trigger", "override"):
            self.assertNotIn(forbidden, public)


# ---- 2.8 agent / delegation boundaries ----------------------------------

class DelegationAbuseTests(unittest.TestCase):
    def setUp(self):
        self.caps = CapabilityRegistry()
        self.caps.register(Capability(
            capability_id="CAP-READ", action="read", resource_scope="health",
            risk_level=RiskLevel.LOW, approval_mode=ApprovalMode.AUTOMATIC,
        ))
        self.agents = AgentRegistry()
        self.runtime = AgentRuntime(self.caps, self.agents)
        self.runtime.register_tool("CAP-READ", lambda args: "ok")

    def test_delegating_unowned_capability_is_refused(self):
        # delegator does NOT hold CAP-READ
        self.agents.register(AgentManifest(
            agent_id="A", name="A", purpose="p", owner_id=OWNER,
            capabilities=set(), may_delegate=True, max_delegation_depth=1,
        ))
        self.agents.register(AgentManifest(
            agent_id="B", name="B", purpose="p", owner_id=OWNER,
            capabilities=set(),
        ))
        with self.assertRaises(PermissionError):
            self.agents.delegate(Delegation(
                delegation_id="D1", delegator_id="A", delegate_id="B",
                capability_ids={"CAP-READ"}, depth=1, reason="escalation",
            ))

    def test_invocation_without_capability_is_denied(self):
        self.agents.register(AgentManifest(
            agent_id="B", name="B", purpose="p", owner_id=OWNER,
            capabilities=set(),
        ))
        receipt = self.runtime.evaluate(InvocationRequest(
            request_id="R1", agent_id="B", capability_id="CAP-READ",
            action="read", resource="health/record", arguments={},
        ))
        self.assertEqual(receipt.status, "DENIED")

    def test_human_required_gate_cannot_be_bypassed(self):
        self.caps.register(Capability(
            capability_id="CAP-WRITE", action="write", resource_scope="health",
            risk_level=RiskLevel.HIGH, approval_mode=ApprovalMode.HUMAN_REQUIRED,
        ))
        self.runtime.register_tool("CAP-WRITE", lambda args: "written")
        self.agents.register(AgentManifest(
            agent_id="C", name="C", purpose="p", owner_id=OWNER,
            capabilities={"CAP-WRITE"},
        ))
        receipt = self.runtime.evaluate(InvocationRequest(
            request_id="R2", agent_id="C", capability_id="CAP-WRITE",
            action="write", resource="health/record", arguments={},
        ))
        self.assertEqual(receipt.status, "REQUIRES_HUMAN_APPROVAL")

    def test_resource_scope_prefix_is_not_bypassable_by_lookalike(self):
        self.agents.register(AgentManifest(
            agent_id="D", name="D", purpose="p", owner_id=OWNER,
            capabilities={"CAP-READ"},
        ))
        # "healthcare" must not match scope "health"
        receipt = self.runtime.evaluate(InvocationRequest(
            request_id="R3", agent_id="D", capability_id="CAP-READ",
            action="read", resource="healthcare/record", arguments={},
        ))
        self.assertEqual(receipt.status, "DENIED")


# ---- 2.7 event chain integrity ------------------------------------------

class ChainTamperTests(unittest.TestCase):
    def _store(self, tmp):
        store = SQLiteEventStore(str(Path(tmp) / "c.db"))
        for i in range(3):
            store.append({
                "id": f"HOS-EVT-{i:06d}", "event_type": "STATE_OBSERVED",
                "occurred_at": "2026-08-17T00:00:00+00:00", "actor_id": OWNER,
                "subject_ids": [], "payload": {"i": i},
                "correlation_id": f"HOS-EVT-{i:06d}", "immutable": True,
            })
        return store

    def test_modification_breaks_chain(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self._store(tmp)
            self.assertTrue(store.verify_chain())
            store.connection.execute(
                "UPDATE events SET payload='{\"i\": 99}' WHERE event_id='HOS-EVT-000001'"
            )
            store.connection.commit()
            self.assertFalse(store.verify_chain())

    def test_deletion_breaks_chain(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self._store(tmp)
            store.connection.execute("DELETE FROM events WHERE event_id='HOS-EVT-000001'")
            store.connection.commit()
            self.assertFalse(store.verify_chain())


if __name__ == "__main__":
    unittest.main()


class PerCallAuthorizationAbuseTests(unittest.TestCase):
    """Abuse attempts against the AR-003 closure (call_authorization.py):
    an attacker holding a legitimate capability grant tries to widen a
    single call beyond what its rule declares."""

    def setUp(self):
        from hos_engine.call_authorization import (
            CallAuthorizer,
            CallRule,
            UnruledPolicy,
        )
        self.auth = CallAuthorizer(
            [CallRule(
                "CAP-EXPORT",
                allowed_argument_keys=frozenset({"scope"}),
                allowed_argument_values={"scope": ("own-data",)},
                max_argument_chars=200,
                allow_via_delegation=False,
            )],
            unruled=UnruledPolicy.DENY,
        )

    def _try(self, arguments, chain=0):
        return self.auth.authorize(
            capability_id="CAP-EXPORT", arguments=arguments,
            delegation_chain_length=chain,
        )

    def test_widening_scope_value_is_refused(self):
        self.assertTrue(self._try({"scope": "own-data"}).allowed)
        self.assertFalse(self._try({"scope": "all-users"}).allowed)

    def test_smuggling_extra_argument_is_refused(self):
        self.assertFalse(
            self._try({"scope": "own-data", "target": "external"}).allowed,
        )

    def test_payload_oversize_is_refused(self):
        self.assertFalse(self._try({"scope": "x" * 500}).allowed)

    def test_laundering_through_delegation_is_refused(self):
        # The rule says direct holders only; arriving through any chain --
        # even a formally valid one -- must not widen the call.
        self.assertFalse(self._try({"scope": "own-data"}, chain=1).allowed)

    def test_unknown_capability_is_denied_under_deny_stance(self):
        verdict = self.auth.authorize(
            capability_id="CAP-NOT-CONFIGURED", arguments={},
            delegation_chain_length=0,
        )
        self.assertFalse(verdict.allowed)
