from __future__ import annotations

import unittest

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
from hos_engine.call_authorization import (
    CallAuthorizer,
    CallRule,
    UnruledPolicy,
)


class CallAuthorizerUnitTests(unittest.TestCase):
    def _authorize(self, authorizer, arguments=None, chain=0):
        return authorizer.authorize(
            capability_id="CAP",
            arguments=arguments or {},
            delegation_chain_length=chain,
        )

    def test_unruled_policy_must_be_declared_and_is_honoured(self):
        allow = CallAuthorizer([], unruled=UnruledPolicy.ALLOW)
        deny = CallAuthorizer([], unruled=UnruledPolicy.DENY)
        self.assertTrue(self._authorize(allow).allowed)
        self.assertFalse(self._authorize(deny).allowed)
        with self.assertRaises(TypeError):
            CallAuthorizer([])  # stance is never assumed

    def test_duplicate_rule_for_capability_is_refused(self):
        with self.assertRaises(ValueError):
            CallAuthorizer(
                [CallRule("CAP"), CallRule("CAP")],
                unruled=UnruledPolicy.DENY,
            )

    def test_argument_key_outside_allowed_set_is_denied(self):
        auth = CallAuthorizer(
            [CallRule("CAP", allowed_argument_keys=frozenset({"key"}))],
            unruled=UnruledPolicy.DENY,
        )
        self.assertTrue(self._authorize(auth, {"key": "x"}).allowed)
        verdict = self._authorize(auth, {"key": "x", "smuggled": "y"})
        self.assertFalse(verdict.allowed)
        self.assertIn("smuggled", verdict.reason)

    def test_missing_required_argument_is_denied(self):
        auth = CallAuthorizer(
            [CallRule("CAP", required_argument_keys=frozenset({"reason"}))],
            unruled=UnruledPolicy.DENY,
        )
        self.assertFalse(self._authorize(auth, {}).allowed)
        self.assertTrue(self._authorize(auth, {"reason": "why"}).allowed)

    def test_value_outside_closed_vocabulary_is_denied(self):
        auth = CallAuthorizer(
            [CallRule("CAP", allowed_argument_values={"mode": ("read", "list")})],
            unruled=UnruledPolicy.DENY,
        )
        self.assertTrue(self._authorize(auth, {"mode": "read"}).allowed)
        self.assertFalse(self._authorize(auth, {"mode": "delete"}).allowed)

    def test_oversized_arguments_are_denied(self):
        auth = CallAuthorizer(
            [CallRule("CAP", max_argument_chars=50)],
            unruled=UnruledPolicy.DENY,
        )
        self.assertTrue(self._authorize(auth, {"k": "small"}).allowed)
        self.assertFalse(self._authorize(auth, {"k": "x" * 200}).allowed)

    def test_delegation_context_is_part_of_the_decision(self):
        direct_only = CallAuthorizer(
            [CallRule("CAP", allow_via_delegation=False)],
            unruled=UnruledPolicy.DENY,
        )
        self.assertTrue(self._authorize(direct_only, chain=0).allowed)
        self.assertFalse(self._authorize(direct_only, chain=1).allowed)

        depth_bound = CallAuthorizer(
            [CallRule("CAP", max_delegation_depth=1)],
            unruled=UnruledPolicy.DENY,
        )
        self.assertTrue(self._authorize(depth_bound, chain=1).allowed)
        self.assertFalse(self._authorize(depth_bound, chain=2).allowed)


class RuntimeIntegrationTests(unittest.TestCase):
    """AR-003 closure: AgentRuntime consults the authorizer per call, and a
    denied verdict is a first-class DENIED receipt, never an exception."""

    def _runtime(self, authorizer=None):
        caps = CapabilityRegistry()
        caps.register(Capability(
            capability_id="CAP-READ", action="read", resource_scope="*",
            risk_level=RiskLevel.LOW, approval_mode=ApprovalMode.AUTOMATIC))
        agents = AgentRegistry()
        agents.register(AgentManifest(
            agent_id="OWNERAGENT", name="A", purpose="p", owner_id="O",
            capabilities={"CAP-READ"}, may_delegate=True,
            max_delegation_depth=1))
        agents.register(AgentManifest(
            agent_id="HELPER", name="H", purpose="p", owner_id="O",
            capabilities=set()))
        runtime = AgentRuntime(caps, agents, call_authorizer=authorizer)
        runtime.register_tool("CAP-READ", lambda a: "ok")
        return runtime, agents

    def _request(self, **over):
        base = {"request_id": "R", "agent_id": "OWNERAGENT",
                "capability_id": "CAP-READ", "action": "read",
                "resource": "x", "arguments": {"key": "x"}}
        base.update(over)
        return InvocationRequest(**base)

    def test_without_authorizer_behavior_is_unchanged(self):
        runtime, _ = self._runtime(authorizer=None)
        self.assertEqual(runtime.evaluate(self._request()).status, "EXECUTED")

    def test_denied_verdict_becomes_denied_receipt(self):
        auth = CallAuthorizer(
            [CallRule("CAP-READ", allowed_argument_keys=frozenset({"key"}))],
            unruled=UnruledPolicy.DENY,
        )
        runtime, _ = self._runtime(auth)
        receipt = runtime.evaluate(
            self._request(arguments={"key": "x", "extra": "y"}),
        )
        self.assertEqual(receipt.status, "DENIED")
        self.assertIn("Call refused", receipt.reason)
        self.assertIn("extra", receipt.reason)

    def test_allowed_call_still_executes(self):
        auth = CallAuthorizer(
            [CallRule("CAP-READ", allowed_argument_keys=frozenset({"key"}))],
            unruled=UnruledPolicy.DENY,
        )
        runtime, _ = self._runtime(auth)
        self.assertEqual(runtime.evaluate(self._request()).status, "EXECUTED")

    def test_delegated_call_is_refused_when_rule_requires_direct_holder(self):
        auth = CallAuthorizer(
            [CallRule("CAP-READ", allow_via_delegation=False)],
            unruled=UnruledPolicy.DENY,
        )
        runtime, agents = self._runtime(auth)
        agents.delegate(Delegation(
            "D1", "OWNERAGENT", "HELPER", {"CAP-READ"}, 1, "test", "HUMAN"))
        receipt = runtime.evaluate(self._request(
            agent_id="HELPER", delegation_chain=["D1"]))
        self.assertEqual(receipt.status, "DENIED")
        self.assertIn("direct holder", receipt.reason)

    def test_deny_stance_blocks_capabilities_without_rules(self):
        auth = CallAuthorizer([], unruled=UnruledPolicy.DENY)
        runtime, _ = self._runtime(auth)
        receipt = runtime.evaluate(self._request())
        self.assertEqual(receipt.status, "DENIED")
        self.assertIn("unruled", receipt.reason)


if __name__ == "__main__":
    unittest.main()
