import unittest

from hos_engine.simulation import *


class SimulationTests(unittest.TestCase):
    def setUp(self):
        self.e=SimulationEngine()
        self.s=Scenario("S","Base",{
            "autonomy":.7,"creative_agency":.6,"relationships":.6,"responsibility":.7,
            "energy":.5,"attention":.5,"value_alignment":.7,
            "degrading_dependency":.2,"extraction":.1})
    def test_positive(self):
        r=self.e.simulate_once(self.s,Intervention("I","Good",{"energy":.1,"autonomy":.05}),
                               constitutional_invariants(),1)
        self.assertEqual(r.status,SimulationStatus.PASSED)
    def test_unsafe(self):
        r=self.e.simulate_once(self.s,Intervention("I2","Bad",{"autonomy":-.6,"extraction":.7}),
                               constitutional_invariants(),1)
        self.assertEqual(r.status,SimulationStatus.FAILED)
    def test_monte_carlo(self):
        x=self.e.monte_carlo(self.s,Intervention("I3","Uncertain",{"energy":.05},{"energy":.02}),
                             constitutional_invariants(),25,3)
        self.assertEqual(x.recommended_status,SimulationStatus.PASSED)
    def test_compare(self):
        safe=Intervention("SAFE","Safe",{"autonomy":.05})
        risky=Intervention("RISKY","Risky",{"autonomy":-.7})
        self.assertEqual(self.e.compare(self.s,[risky,safe],constitutional_invariants(),10)[0].intervention_id,"SAFE")
