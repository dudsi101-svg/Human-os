from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from hos_engine.human_model import EvidenceType, RecordStatus
from hos_engine.self_model import MessageAuthor, SelfModelService, TensionStatus
from hos_engine.self_model_store import SQLiteSelfModelStore

SUBJECT = "HOS-HUM-000001"


def populated_service():
    svc = SelfModelService()
    it = svc.interactions.start(subject_id=SUBJECT)
    m1 = svc.interactions.append(it.interaction_id, author=MessageAuthor.USER,
                                 text="Cenię wolność i nie lubię mikromanagementu.")
    m2 = svc.interactions.append(it.interaction_id, author=MessageAuthor.USER,
                                 text="Potrzebuję też stabilności finansowej.")
    a = svc.declare(subject_id=SUBJECT, domain="values", key="value_candidate",
                    value="autonomia", message_id=m1.message_id)
    b = svc.declare(subject_id=SUBJECT, domain="values", key="value_candidate",
                    value="bezpieczeństwo", message_id=m2.message_id)
    hyp = svc.hypothesize(subject_id=SUBJECT, domain="values", key="dominant_value",
                          value="autonomia", confidence=0.72,
                          supported_by=[m1.message_id, m2.message_id])
    confirmed = svc.confirm(hyp.record_id, subject_id=SUBJECT, message_id=m2.message_id)
    sensitive = svc.declare(subject_id=SUBJECT, domain="health", key="condition",
                            value="migreny", message_id=m1.message_id, sensitive=True)
    tension = svc.record_tension(subject_id=SUBJECT, record_a=a.record_id,
                                 record_b=b.record_id, note="wolność vs bezpieczeństwo")
    return svc, {"a": a, "b": b, "hyp": hyp, "confirmed": confirmed,
                 "sensitive": sensitive, "tension": tension, "m1": m1}


class SelfModelStoreRoundTripTests(unittest.TestCase):
    def round_trip(self, svc):
        with tempfile.TemporaryDirectory() as tmp:
            store = SQLiteSelfModelStore(str(Path(tmp) / "self.db"))
            store.save_snapshot(svc)
            loaded = store.load_service()
            store.close()
        return loaded

    def test_supersedes_chain_and_view_survive_restart(self):
        svc, refs = populated_service()
        loaded = self.round_trip(svc)
        # the confirmed record supersedes the hypothesis; history intact
        history = loaded.history(refs["confirmed"].record_id)
        self.assertEqual([r.record_id for r in history],
                         [refs["confirmed"].record_id, refs["hyp"].record_id])
        self.assertEqual(history[1].status, RecordStatus.SUPERSEDED)
        self.assertEqual(history[1].evidence_type, EvidenceType.HYPOTHESIS)
        view = loaded.living_view(SUBJECT)
        self.assertEqual([r.record_id for r in view["confirmed"]],
                         [refs["confirmed"].record_id])
        self.assertEqual(view["hypotheses"], [])

    def test_why_quotes_survive_restart(self):
        svc, refs = populated_service()
        loaded = self.round_trip(svc)
        why = loaded.why(refs["confirmed"].record_id)
        quotes = [s["quote"] for s in why["sources"] if s["quote"]]
        self.assertIn("Cenię wolność i nie lubię mikromanagementu.", quotes)
        self.assertEqual(why["created_by"], "user")

    def test_tensions_and_sensitivity_survive_restart(self):
        svc, refs = populated_service()
        loaded = self.round_trip(svc)
        open_t = loaded.open_tensions(SUBJECT)
        self.assertEqual([t.tension_id for t in open_t],
                         [refs["tension"].tension_id])
        self.assertEqual(open_t[0].status, TensionStatus.OPEN)
        # sensitive record still hidden by default after reload
        self.assertNotIn(refs["sensitive"].record_id,
                         [r.record_id for r in loaded.living_view(SUBJECT)["declared"]])
        self.assertIn(refs["sensitive"].record_id,
                      [r.record_id for r in
                       loaded.living_view(SUBJECT, include_sensitive=True)["declared"]])

    def test_restored_service_keeps_enforcing_subject_only_rules(self):
        svc, refs = populated_service()
        loaded = self.round_trip(svc)
        with self.assertRaises(PermissionError):
            loaded.reject(refs["a"].record_id, subject_id="HOS-HUM-000099")
        # and the lifecycle continues working after restart
        m = loaded.interactions.append(
            loaded.interactions.all_interactions()[0].interaction_id,
            author=MessageAuthor.USER, text="Jednak to nieaktualne.")
        closed = loaded.mark_outdated(refs["b"].record_id, subject_id=SUBJECT)
        self.assertIsNotNone(closed.valid_to)
        self.assertIsNotNone(m.message_id)

    def test_resnapshot_replaces_not_duplicates(self):
        svc, _ = populated_service()
        with tempfile.TemporaryDirectory() as tmp:
            store = SQLiteSelfModelStore(str(Path(tmp) / "self.db"))
            store.save_snapshot(svc)
            first = store.counts()
            store.save_snapshot(svc)
            second = store.counts()
            store.close()
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
