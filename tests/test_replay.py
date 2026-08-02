import unittest

from hos_engine.replay import rebuild_entities


class ReplayTests(unittest.TestCase):
    def test_rebuild_state(self):
        events = [
            {
                "event_type": "ENTITY_CREATED",
                "subject_ids": ["HOS-INT-000001"],
                "payload": {"snapshot": {"id": "HOS-INT-000001", "status": "draft"}},
            },
            {
                "event_type": "ENTITY_UPDATED",
                "subject_ids": ["HOS-INT-000001"],
                "payload": {"from": "draft", "to": "active"},
            },
        ]
        entities = rebuild_entities(events)
        self.assertEqual(entities["HOS-INT-000001"]["status"], "active")


if __name__ == "__main__":
    unittest.main()
