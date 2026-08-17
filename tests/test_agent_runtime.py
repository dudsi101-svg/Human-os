import unittest

from hos_engine.agent_policy import constitutional_capability
from hos_engine.agent_runtime import *


class AgentRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.cr=CapabilityRegistry()
        self.cr.register(constitutional_capability("READ","read","knowledge",RiskLevel.LOW,
            changes_external_state=False,affects_people=False,reversible=True,handles_sensitive_data=False))
        self.cr.register(constitutional_capability("WRITE","write","knowledge",RiskLevel.HIGH,
            changes_external_state=True,affects_people=True,reversible=True,handles_sensitive_data=False))
        self.ar=AgentRegistry()
        self.ar.register(AgentManifest("ROOT","Root","Coordinate","HUMAN",{"READ","WRITE"},True,1))
        self.ar.register(AgentManifest("READER","Reader","Read","HUMAN",{"READ"}))
        self.ar.register(AgentManifest("DELEGATE","Delegate","Delegated","HUMAN",set()))
        self.rt=AgentRuntime(self.cr,self.ar)
        self.rt.register_tool("READ",lambda a:{"value":a["key"]})
        self.rt.register_tool("WRITE",lambda a:{"saved":a["value"]})
    def test_read(self):
        r=self.rt.evaluate(InvocationRequest("1","READER","READ","read","knowledge/x",{"key":"x"}))
        self.assertEqual(r.status,"EXECUTED")
    def test_human_gate(self):
        r=self.rt.evaluate(InvocationRequest("2","ROOT","WRITE","write","knowledge/x",{"value":"x"}))
        self.assertEqual(r.status,"REQUIRES_HUMAN_APPROVAL")
    def test_scope(self):
        r=self.rt.evaluate(InvocationRequest("3","READER","READ","read","finance/x",{"key":"x"}))
        self.assertEqual(r.status,"DENIED")
    def test_delegation(self):
        self.ar.delegate(Delegation("D1","ROOT","DELEGATE",{"READ"},1,"research","HUMAN"))
        r=self.rt.evaluate(InvocationRequest("4","DELEGATE","READ","read","knowledge/x",{"key":"x"},
                                            delegation_chain=["D1"]))
        self.assertEqual(r.status,"EXECUTED")


class UnknownReferencesTests(unittest.TestCase):
    """Regression: the 2026-08-17 simulation found an intent naming an
    unknown capability crashed AgentRuntime.evaluate with KeyError instead
    of returning a DENIED receipt (breaking ExecutionLoop's no-exception
    contract)."""

    def setUp(self):
        self.caps = CapabilityRegistry()
        self.caps.register(Capability(
            capability_id="CAP-READ", action="read", resource_scope="*",
            risk_level=RiskLevel.LOW, approval_mode=ApprovalMode.AUTOMATIC))
        self.agents = AgentRegistry()
        self.agents.register(AgentManifest(
            agent_id="A", name="A", purpose="p", owner_id="O",
            capabilities={"CAP-READ"}))
        self.rt = AgentRuntime(self.caps, self.agents)
        self.rt.register_tool("CAP-READ", lambda a: "ok")

    def _req(self, **over):
        base = {"request_id": "R", "agent_id": "A", "capability_id": "CAP-READ",
                "action": "read", "resource": "x", "arguments": {}}
        base.update(over)
        return InvocationRequest(**base)

    def test_unknown_capability_is_denied_not_raised(self):
        receipt = self.rt.evaluate(self._req(capability_id="CAP-NONE"))
        self.assertEqual(receipt.status, "DENIED")
        self.assertEqual(receipt.reason, "Unknown capability")

    def test_unknown_agent_is_denied_not_raised(self):
        receipt = self.rt.evaluate(self._req(agent_id="A-NONE"))
        self.assertEqual(receipt.status, "DENIED")
        self.assertEqual(receipt.reason, "Unknown agent")
