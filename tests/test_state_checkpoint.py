"""Tests for snapshot<->ledger checkpoints (audit §17)."""

import unittest

from hos_engine.state_checkpoint import (
    CheckpointVerdict,
    canonical_state_hash,
    create_checkpoint,
    verify_checkpoint,
)


def _state():
    return {"entities": [{"id": "HOS-ENT-1", "status": "ACTIVE"}], "version": 3}


class TestStateCheckpoint(unittest.TestCase):
    def test_consistent_when_nothing_changed(self):
        cp = create_checkpoint("hub", _state(), "abc123", 42, "0.3.0", "v3")
        verdict = verify_checkpoint(cp, _state(), "abc123", 42, "0.3.0")
        self.assertEqual(verdict.verdict, CheckpointVerdict.CONSISTENT)
        self.assertEqual(verdict.mismatches, ())

    def test_canonical_hash_is_key_order_independent(self):
        a = {"x": 1, "y": {"b": 2, "a": 3}}
        b = {"y": {"a": 3, "b": 2}, "x": 1}
        self.assertEqual(canonical_state_hash(a), canonical_state_hash(b))

    def test_snapshot_drift_requires_reconciliation(self):
        cp = create_checkpoint("hub", _state(), "abc123", 42, "0.3.0", "v3")
        drifted = _state()
        drifted["entities"][0]["status"] = "SUSPENDED"
        verdict = verify_checkpoint(cp, drifted, "abc123", 42)
        self.assertEqual(verdict.verdict, CheckpointVerdict.RECONCILIATION_REQUIRED)
        self.assertIn("snapshot hash differs", verdict.mismatches[0])

    def test_ledger_drift_requires_reconciliation_and_names_both(self):
        cp = create_checkpoint("selfmodel", _state(), "abc123", 42, "0.3.0", "v3")
        verdict = verify_checkpoint(cp, _state(), "def456", 45)
        self.assertEqual(verdict.verdict, CheckpointVerdict.RECONCILIATION_REQUIRED)
        joined = " ".join(verdict.mismatches)
        self.assertIn("ledger head differs", joined)
        self.assertIn("event sequence differs", joined)

    def test_schema_version_drift_detected_when_declared(self):
        cp = create_checkpoint("events", _state(), "abc123", 42, "0.3.0", "v3")
        verdict = verify_checkpoint(cp, _state(), "abc123", 42, schema_version="0.4.0")
        self.assertEqual(verdict.verdict, CheckpointVerdict.RECONCILIATION_REQUIRED)
        self.assertIn("schema version differs", verdict.mismatches[0])

    def test_no_silent_adoption_all_mismatches_listed(self):
        cp = create_checkpoint("graph", _state(), "abc123", 42, "0.3.0", "v3")
        verdict = verify_checkpoint(cp, {"other": True}, "zzz", 1, schema_version="9.9.9")
        self.assertEqual(len(verdict.mismatches), 4)

    def test_explicit_inputs_required(self):
        with self.assertRaises(ValueError):
            create_checkpoint("  ", _state(), "abc", 1, "0.3.0", "v1")
        with self.assertRaises(ValueError):
            create_checkpoint("hub", _state(), "abc", -1, "0.3.0", "v1")

    def test_checkpoint_id_and_immutability(self):
        cp = create_checkpoint("hub", _state(), "abc123", 42, "0.3.0", "v3")
        self.assertTrue(cp.checkpoint_id.startswith("HOS-CHK-"))
        with self.assertRaises(AttributeError):
            cp.snapshot_hash = "tampered"  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
