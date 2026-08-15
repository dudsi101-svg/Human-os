
import unittest

from hos_engine import HumanOSEngine
from hos_engine.flow import generative_flow_score
from hos_engine.state_machine import transition


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = HumanOSEngine()

    def test_valid_state_transition(self):
        self.assertEqual(transition("draft", "active"), "active")

    def test_invalid_state_transition(self):
        with self.assertRaises(ValueError):
            transition("archived", "active")

    def test_approved_action(self):
        action = {
            "id": "HOS-ACT-000001",
            "responsibility_owner_id": "HOS-HUM-000001",
            "consent": True,
            "reversibility": 0.9,
            "portability": 0.8,
            "exit_cost": 0.1,
            "predicted_effects": {
                "autonomy": 0.2,
                "generativity": 0.8,
                "extraction": 0.0,
                "degrading_system_dependency": -0.2,
            },
            "limitations": ["Estimate only."]
        }
        result = self.engine.evaluate_action(action, "HOS-HUM-000001")
        self.assertEqual(result["final_status"], "APPROVED")

    def test_extractive_action_blocked(self):
        action = {
            "id": "HOS-ACT-000002",
            "responsibility_owner_id": "HOS-HUM-000001",
            "consent": True,
            "reversibility": 0.9,
            "portability": 0.8,
            "exit_cost": 0.1,
            "predicted_effects": {
                "autonomy": 0.0,
                "generativity": 0.3,
                "extraction": 0.9,
                "degrading_system_dependency": 0.0,
            },
            "limitations": ["Estimate only."]
        }
        result = self.engine.evaluate_action(action, "HOS-HUM-000001")
        self.assertEqual(result["final_status"], "CONSTITUTIONAL_VIOLATION")

    def test_flow_score(self):
        flow = {
            "gain": 0.8,
            "reciprocity": 0.8,
            "consent": 1.0,
            "durability": 0.7,
            "generativity": 0.9,
            "extraction": 0.05,
            "dependency_effect": -0.2,
            "externalities": {"positive": 0.4, "negative": 0.0},
        }
        self.assertGreater(generative_flow_score(flow), 0)


if __name__ == "__main__":
    unittest.main()
