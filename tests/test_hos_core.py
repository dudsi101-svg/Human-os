import unittest

from hos_engine.hos_core import ContextManager, EventEngine, ExecutionStatus


class ContextManagerTests(unittest.TestCase):
    def test_snapshot_versions_increment_per_subject(self):
        manager = ContextManager()
        first = manager.snapshot("HOS-HUM-000001", {"goal": "explore"})
        second = manager.snapshot("HOS-HUM-000001", {"goal": "decide"})

        self.assertEqual(first.version, 1)
        self.assertEqual(second.version, 2)
        self.assertEqual(manager.latest("HOS-HUM-000001"), second)
        self.assertEqual(manager.history("HOS-HUM-000001"), [first, second])

    def test_unknown_subject_has_no_latest(self):
        manager = ContextManager()
        self.assertIsNone(manager.latest("HOS-HUM-999999"))
        self.assertEqual(manager.history("HOS-HUM-999999"), [])

    def test_snapshots_are_independent_per_subject(self):
        manager = ContextManager()
        manager.snapshot("HOS-HUM-000001", {"a": 1})
        manager.snapshot("HOS-HUM-000002", {"b": 2})
        self.assertEqual(len(manager.history("HOS-HUM-000001")), 1)
        self.assertEqual(len(manager.history("HOS-HUM-000002")), 1)

    def test_snapshot_data_is_genuinely_immutable(self):
        manager = ContextManager()
        source = {"goal": "explore"}
        package = manager.snapshot("HOS-HUM-000001", source)

        source["goal"] = "mutated after snapshot"
        self.assertEqual(package.data["goal"], "explore")

        with self.assertRaises(TypeError):
            package.data["goal"] = "direct write"


class EventEngineTests(unittest.TestCase):
    def setUp(self):
        self.context_manager = ContextManager()
        self.engine = EventEngine()

    def test_open_creates_proposed_contract_with_proposal_event(self):
        context = self.context_manager.snapshot("HOS-HUM-000001", {})
        contract = self.engine.open(goal="Evaluate action", owner_id="HOS-HUM-000001", context=context)

        self.assertEqual(contract.status, ExecutionStatus.PROPOSED)
        self.assertTrue(contract.execution_id.startswith("HOS-EXE-"))
        self.assertTrue(contract.correlation_id.startswith("HOS-COR-"))

        log = self.engine.log(contract.execution_id)
        self.assertEqual(len(log), 1)
        self.assertEqual(log[0].event_type, "EXECUTION_PROPOSED")

    def test_transition_updates_status_and_appends_event(self):
        context = self.context_manager.snapshot("HOS-HUM-000001", {})
        contract = self.engine.open(goal="Evaluate action", owner_id="HOS-HUM-000001", context=context)

        updated = self.engine.transition(contract.execution_id, ExecutionStatus.IN_PROGRESS)
        self.assertEqual(updated.status, ExecutionStatus.IN_PROGRESS)

        completed = self.engine.transition(contract.execution_id, ExecutionStatus.COMPLETED, reason="done")
        self.assertEqual(completed.status, ExecutionStatus.COMPLETED)

        log = self.engine.log(contract.execution_id)
        self.assertEqual([e.event_type for e in log], [
            "EXECUTION_PROPOSED", "EXECUTION_IN_PROGRESS", "EXECUTION_COMPLETED",
        ])

    def test_transition_after_terminal_status_is_rejected(self):
        context = self.context_manager.snapshot("HOS-HUM-000001", {})
        contract = self.engine.open(goal="Evaluate action", owner_id="HOS-HUM-000001", context=context)
        self.engine.transition(contract.execution_id, ExecutionStatus.COMPLETED)

        with self.assertRaises(ValueError):
            self.engine.transition(contract.execution_id, ExecutionStatus.IN_PROGRESS)

    def test_open_carries_permissions_and_budget(self):
        context = self.context_manager.snapshot("HOS-HUM-000001", {})
        contract = self.engine.open(
            goal="Evaluate action",
            owner_id="HOS-HUM-000001",
            context=context,
            required_permissions=("READ", "EXECUTE"),
            budget={"time_seconds": 30},
            abort_criteria=("user_revokes_consent",),
        )
        self.assertEqual(contract.required_permissions, ("READ", "EXECUTE"))
        self.assertEqual(contract.budget, {"time_seconds": 30})
        self.assertEqual(contract.abort_criteria, ("user_revokes_consent",))


if __name__ == "__main__":
    unittest.main()
