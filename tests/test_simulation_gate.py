import unittest

from hos_engine.agent_runtime import InvocationRequest
from hos_engine.simulation import *
from hos_engine.simulation_gate import SimulationGate


class GateTests(unittest.TestCase):
    def test_block(self):
        s=Scenario("S","Base",{"autonomy":.6,"creative_agency":.6,"relationships":.6,
          "responsibility":.6,"energy":.6,"attention":.6,"value_alignment":.6,
          "degrading_dependency":.2,"extraction":.1})
        i=Intervention("I","Unsafe",{"autonomy":-.5,"extraction":.7})
        q=InvocationRequest("Q","A","C","write","knowledge/x",{})
        d=SimulationGate(SimulationEngine()).evaluate(q,s,i,constitutional_invariants(),10)
        self.assertEqual(d.status,"BLOCKED")
