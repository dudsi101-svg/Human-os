import tempfile
import unittest
from pathlib import Path

from hos_engine.sqlite_store import SQLiteEventStore


class PersistenceTests(unittest.TestCase):
    def test_hash_chain_is_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            store = SQLiteEventStore(Path(directory) / "events.db")
            store.append({
                "id": "HOS-EVT-000001",
                "event_type": "ENTITY_CREATED",
                "occurred_at": "2026-07-20T12:00:00+00:00",
                "actor_id": "HOS-HUM-000001",
                "subject_ids": ["HOS-INT-000001"],
                "payload": {"snapshot": {"id": "HOS-INT-000001", "status": "draft"}},
                "correlation_id": "HOS-COR-000001",
                "immutable": True,
            })
            store.append({
                "id": "HOS-EVT-000002",
                "event_type": "ENTITY_UPDATED",
                "occurred_at": "2026-07-20T12:01:00+00:00",
                "actor_id": "HOS-HUM-000001",
                "subject_ids": ["HOS-INT-000001"],
                "payload": {"from": "draft", "to": "active"},
                "correlation_id": "HOS-COR-000002",
                "immutable": True,
            })
            self.assertTrue(store.verify_chain())
            self.assertEqual(len(store.all()), 2)
            store.close()


if __name__ == "__main__":
    unittest.main()
