from __future__ import annotations

import unittest

from hos_engine.consent import ConsentRegistry
from hos_engine.human_model import EvidenceType, RecordStatus
from hos_engine.self_model import (
    InteractionMode,
    MessageAuthor,
    SelfModelService,
    confidence_band,
)

SUBJECT = "HOS-HUM-000001"
OTHER = "HOS-HUM-000099"


def service() -> SelfModelService:
    return SelfModelService()


def start_chat(svc: SelfModelService, mode: InteractionMode = InteractionMode.NATURAL):
    it = svc.interactions.start(subject_id=SUBJECT, mode=mode)
    return it


class InteractionSeparationTests(unittest.TestCase):
    def test_messages_never_create_model_records_by_themselves(self):
        svc = service()
        it = start_chat(svc)
        svc.interactions.append(it.interaction_id, author=MessageAuthor.USER,
                                text="Cenię wolność i nie lubię, gdy ktoś organizuje mi życie.")
        svc.interactions.append(it.interaction_id, author=MessageAuthor.SYSTEM,
                                text="Rozumiem. Opowiedz więcej?")
        self.assertEqual(len(svc.interactions.messages(it.interaction_id)), 2)
        view = svc.living_view(SUBJECT)
        self.assertEqual(view["declared"], [])
        self.assertEqual(view["hypotheses"], [])

    def test_interaction_modes_are_recorded(self):
        svc = service()
        it = start_chat(svc, InteractionMode.EXPLORATORY)
        self.assertEqual(svc.interactions.get(it.interaction_id).mode,
                         InteractionMode.EXPLORATORY)


class DeclarationTests(unittest.TestCase):
    def test_explicit_declaration_with_provenance(self):
        svc = service()
        it = start_chat(svc)
        msg = svc.interactions.append(it.interaction_id, author=MessageAuthor.USER,
                                      text="Rodzina jest dla mnie bardzo ważna.")
        rec = svc.declare(subject_id=SUBJECT, domain="values", key="value_candidate",
                          value="rodzina", message_id=msg.message_id)
        self.assertEqual(rec.evidence_type, EvidenceType.USER_DECLARATION)
        self.assertIn(msg.message_id, rec.evidence_refs)
        why = svc.why(rec.record_id)
        self.assertEqual(why["sources"][0]["quote"], "Rodzina jest dla mnie bardzo ważna.")
        self.assertEqual(why["sources"][0]["interaction_id"], it.interaction_id)

    def test_declaration_is_not_a_fact(self):
        svc = service()
        it = start_chat(svc)
        msg = svc.interactions.append(it.interaction_id, author=MessageAuthor.USER,
                                      text="Cenię wolność.")
        rec = svc.declare(subject_id=SUBJECT, domain="values", key="value_candidate",
                          value="autonomia", message_id=msg.message_id)
        self.assertLess(rec.confidence, 1.0)
        self.assertEqual(svc.living_view(SUBJECT)["confirmed"], [])


class HypothesisLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.svc = service()
        self.it = start_chat(self.svc)
        self.m1 = self.svc.interactions.append(self.it.interaction_id,
                                               author=MessageAuthor.USER,
                                               text="Nie znoszę mikromanagementu.")
        self.m2 = self.svc.interactions.append(self.it.interaction_id,
                                               author=MessageAuthor.USER,
                                               text="Sam ustalam sobie rytm pracy.")
        self.hyp = self.svc.hypothesize(
            subject_id=SUBJECT, domain="values", key="dominant_value",
            value="autonomia", confidence=0.72,
            supported_by=[self.m1.message_id, self.m2.message_id],
            alternatives=["niezależność zawodowa tylko w pracy"])

    def test_unconfirmed_hypothesis_stays_a_hypothesis(self):
        view = self.svc.living_view(SUBJECT)
        self.assertEqual([r.record_id for r in view["hypotheses"]], [self.hyp.record_id])
        self.assertEqual(view["confirmed"], [])
        why = self.svc.why(self.hyp.record_id)
        self.assertEqual(why["confidence_band"], "MEDIUM")
        self.assertEqual(why["created_by"], "ProfileInterpreter v0.1")
        self.assertEqual(len(why["sources"]), 2)
        self.assertTrue(why["alternatives"])

    def test_hypothesis_requires_evidence(self):
        with self.assertRaises(ValueError):
            self.svc.hypothesize(subject_id=SUBJECT, domain="values", key="k",
                                 value="v", confidence=0.5, supported_by=[])

    def test_confirmation_versions_without_overwriting(self):
        m3 = self.svc.interactions.append(self.it.interaction_id,
                                          author=MessageAuthor.USER, text="Tak, zgadza się.")
        new = self.svc.confirm(self.hyp.record_id, subject_id=SUBJECT,
                               message_id=m3.message_id)
        self.assertEqual(new.evidence_type, EvidenceType.USER_DECLARATION)
        self.assertIsNotNone(new.last_confirmed_at)
        old = self.svc.model.get(self.hyp.record_id)
        self.assertEqual(old.status, RecordStatus.SUPERSEDED)
        self.assertEqual(old.evidence_type, EvidenceType.HYPOTHESIS)  # history intact
        view = self.svc.living_view(SUBJECT)
        self.assertEqual([r.record_id for r in view["confirmed"]], [new.record_id])
        self.assertEqual(view["hypotheses"], [])
        history = self.svc.history(new.record_id)
        self.assertEqual([r.record_id for r in history],
                         [new.record_id, self.hyp.record_id])

    def test_rejection_is_kept_not_deleted(self):
        rejected = self.svc.reject(self.hyp.record_id, subject_id=SUBJECT)
        self.assertEqual(rejected.status, RecordStatus.CONTESTED)
        view = self.svc.living_view(SUBJECT)
        self.assertEqual(view["hypotheses"], [])
        self.assertEqual([r.record_id for r in view["rejected"]], [self.hyp.record_id])

    def test_only_subject_may_confirm_or_reject(self):
        with self.assertRaises(PermissionError):
            self.svc.confirm(self.hyp.record_id, subject_id=OTHER, message_id="x")
        with self.assertRaises(PermissionError):
            self.svc.reject(self.hyp.record_id, subject_id=OTHER)


class CorrectionAndTemporalityTests(unittest.TestCase):
    def setUp(self):
        self.svc = service()
        self.it = start_chat(self.svc)
        self.msg = self.svc.interactions.append(self.it.interaction_id,
                                                author=MessageAuthor.USER,
                                                text="Trenuję bardzo intensywnie.")
        self.rec = self.svc.declare(subject_id=SUBJECT, domain="health",
                                    key="training_style", value="bardzo intensywne",
                                    message_id=self.msg.message_id)

    def test_user_correction_supersedes(self):
        m2 = self.svc.interactions.append(self.it.interaction_id,
                                          author=MessageAuthor.USER,
                                          text="Jednak raczej umiarkowanie.")
        new = self.svc.correct(self.rec.record_id, subject_id=SUBJECT,
                               value="umiarkowane", message_id=m2.message_id)
        self.assertEqual(new.value, "umiarkowane")
        self.assertEqual(self.svc.model.get(self.rec.record_id).status,
                         RecordStatus.SUPERSEDED)
        self.assertEqual(self.svc.model.get(self.rec.record_id).value,
                         "bardzo intensywne")  # history not rewritten

    def test_mark_outdated_closes_validity_and_keeps_history(self):
        closed = self.svc.mark_outdated(self.rec.record_id, subject_id=SUBJECT)
        self.assertIsNotNone(closed.valid_to)
        view = self.svc.living_view(SUBJECT)
        self.assertEqual(view["declared"], [])
        self.assertEqual([r.record_id for r in view["outdated"]], [closed.record_id])
        self.assertEqual(self.svc.model.get(self.rec.record_id).valid_to, None)


class ContradictionTests(unittest.TestCase):
    def test_contradictory_declarations_are_both_kept_and_tension_is_signal(self):
        svc = service()
        it = start_chat(svc)
        m1 = svc.interactions.append(it.interaction_id, author=MessageAuthor.USER,
                                     text="Wolność jest dla mnie bardzo ważna.")
        m2 = svc.interactions.append(it.interaction_id, author=MessageAuthor.USER,
                                     text="Potrzebuję dużej stabilności i bezpieczeństwa.")
        a = svc.declare(subject_id=SUBJECT, domain="values", key="value_candidate",
                        value="wolność", message_id=m1.message_id)
        b = svc.declare(subject_id=SUBJECT, domain="values", key="value_candidate",
                        value="bezpieczeństwo", message_id=m2.message_id)
        t = svc.record_tension(subject_id=SUBJECT, record_a=a.record_id,
                               record_b=b.record_id,
                               note="wolność vs bezpieczeństwo — różne decyzje w różnych sytuacjach")
        view = svc.living_view(SUBJECT)
        self.assertEqual(len(view["declared"]), 2)  # neither auto-removed
        self.assertEqual([x.tension_id for x in view["tensions"]], [t.tension_id])
        resolved = svc.resolve_tension(t.tension_id, subject_id=SUBJECT,
                                       resolution="wolność w pracy, bezpieczeństwo w finansach")
        self.assertEqual(svc.open_tensions(SUBJECT), [])
        self.assertEqual(resolved.resolution,
                         "wolność w pracy, bezpieczeństwo w finansach")

    def test_system_cannot_resolve_for_another_subject(self):
        svc = service()
        it = start_chat(svc)
        m = svc.interactions.append(it.interaction_id, author=MessageAuthor.USER, text="x")
        a = svc.declare(subject_id=SUBJECT, domain="values", key="k", value="a",
                        message_id=m.message_id)
        b = svc.declare(subject_id=SUBJECT, domain="values", key="k", value="b",
                        message_id=m.message_id)
        t = svc.record_tension(subject_id=SUBJECT, record_a=a.record_id,
                               record_b=b.record_id, note="n")
        with self.assertRaises(PermissionError):
            svc.resolve_tension(t.tension_id, subject_id=OTHER, resolution="r")


class ConsentTests(unittest.TestCase):
    def test_no_consent_means_conversation_only_no_model_write(self):
        consent = ConsentRegistry()
        svc = SelfModelService(consent=consent, grantee_id="HOS-AGT-PROFILER")
        it = svc.interactions.start(subject_id=SUBJECT)
        msg = svc.interactions.append(it.interaction_id, author=MessageAuthor.USER,
                                      text="Mam przewlekłą chorobę.")
        with self.assertRaises(PermissionError):
            svc.declare(subject_id=SUBJECT, domain="health", key="condition",
                        value="przewlekła choroba", message_id=msg.message_id,
                        sensitive=True)
        # the utterance itself still exists as interaction history
        self.assertEqual(len(svc.interactions.messages(it.interaction_id)), 1)
        self.assertEqual(svc.living_view(SUBJECT, include_sensitive=True)["declared"], [])

    def test_purpose_limited_consent_allows_write(self):
        consent = ConsentRegistry()
        consent.grant(subject_id=SUBJECT, grantee_id="HOS-AGT-PROFILER",
                      purposes={"self_model"}, domains={"health"}, actions={"write"},
                      allow_sensitive=True)
        svc = SelfModelService(consent=consent, grantee_id="HOS-AGT-PROFILER")
        it = svc.interactions.start(subject_id=SUBJECT)
        msg = svc.interactions.append(it.interaction_id, author=MessageAuthor.USER,
                                      text="Średnio 4 treningi tygodniowo od miesiąca.")
        rec = svc.observe(subject_id=SUBJECT, domain="health", key="training_frequency",
                          value="4/tydzień (4 tygodnie)", message_id=msg.message_id,
                          sensitive=True)
        self.assertEqual(rec.evidence_type, EvidenceType.OBSERVATION)

    def test_sensitive_records_hidden_from_default_view(self):
        consent = ConsentRegistry()
        consent.grant(subject_id=SUBJECT, grantee_id="HOS-AGT-PROFILER",
                      purposes={"self_model"}, domains={"*"}, actions={"write"},
                      allow_sensitive=True)
        svc = SelfModelService(consent=consent, grantee_id="HOS-AGT-PROFILER")
        it = svc.interactions.start(subject_id=SUBJECT)
        msg = svc.interactions.append(it.interaction_id, author=MessageAuthor.USER, text="…")
        svc.declare(subject_id=SUBJECT, domain="health", key="condition",
                    value="—", message_id=msg.message_id, sensitive=True)
        self.assertEqual(svc.living_view(SUBJECT)["declared"], [])
        self.assertEqual(len(svc.living_view(SUBJECT, include_sensitive=True)["declared"]), 1)


class DecisionFeedTests(unittest.TestCase):
    def test_feed_keeps_epistemic_split(self):
        svc = service()
        it = start_chat(svc)
        m = svc.interactions.append(it.interaction_id, author=MessageAuthor.USER,
                                    text="Zależy mi na energii do działania.")
        svc.declare(subject_id=SUBJECT, domain="goals", key="goal_candidate",
                    value="więcej energii", message_id=m.message_id)
        svc.hypothesize(subject_id=SUBJECT, domain="values", key="dominant_value",
                        value="autonomia", confidence=0.3,
                        supported_by=[m.message_id])
        feed = svc.decision_inputs(SUBJECT)
        self.assertEqual(len(feed["declared"]), 1)
        self.assertEqual(len(feed["hypotheses"]), 1)
        record, _conf, band = feed["hypotheses"][0]
        self.assertEqual(band, "LOW")
        self.assertNotIn(record, feed["declared"])


class DecisionContextAsymmetryTests(unittest.TestCase):
    """A weak AI hypothesis must never reach gate-grade inputs
    (ADR-DECISION-002/-005 asymmetry, enforced structurally at the bridge)."""

    def test_hypothesis_is_advisory_until_confirmed(self):
        svc = service()
        it = start_chat(svc)
        m = svc.interactions.append(it.interaction_id, author=MessageAuthor.USER,
                                    text="Chyba nie mogę trenować wieczorami.")
        hyp = svc.hypothesize(subject_id=SUBJECT, domain="constraints",
                              key="schedule_constraint", value="wieczory zajęte",
                              confidence=0.5, supported_by=[m.message_id])
        ctx = svc.decision_context(SUBJECT)
        self.assertEqual(ctx["constraints"], [])  # not gate-grade
        self.assertEqual([a["record"].record_id for a in ctx["advisory_hypotheses"]],
                         [hyp.record_id])
        m2 = svc.interactions.append(it.interaction_id, author=MessageAuthor.USER,
                                     text="Tak, wieczory odpadają.")
        confirmed = svc.confirm(hyp.record_id, subject_id=SUBJECT,
                                message_id=m2.message_id)
        ctx = svc.decision_context(SUBJECT)
        self.assertEqual([r.record_id for r in ctx["constraints"]],
                         [confirmed.record_id])  # now gate-grade
        self.assertEqual(ctx["advisory_hypotheses"], [])

    def test_declared_goal_is_gate_grade_immediately(self):
        svc = service()
        it = start_chat(svc)
        m = svc.interactions.append(it.interaction_id, author=MessageAuthor.USER,
                                    text="Chcę mieć energię po pracy.")
        rec = svc.declare(subject_id=SUBJECT, domain="goals", key="goal_candidate",
                          value="energia po pracy", message_id=m.message_id)
        ctx = svc.decision_context(SUBJECT)
        self.assertEqual([r.record_id for r in ctx["goals"]], [rec.record_id])


class DurableAuditTests(unittest.TestCase):
    def test_lifecycle_events_chain_in_sqlite(self):
        import tempfile
        from pathlib import Path

        from hos_engine.sqlite_store import SQLiteEventStore
        with tempfile.TemporaryDirectory() as tmp:
            store = SQLiteEventStore(str(Path(tmp) / "self_model.db"))
            svc = SelfModelService(event_store=store)
            it = svc.interactions.start(subject_id=SUBJECT)
            m1 = svc.interactions.append(it.interaction_id,
                                         author=MessageAuthor.USER, text="a")
            m2 = svc.interactions.append(it.interaction_id,
                                         author=MessageAuthor.USER, text="b")
            hyp = svc.hypothesize(subject_id=SUBJECT, domain="values", key="k",
                                  value="autonomia", confidence=0.7,
                                  supported_by=[m1.message_id, m2.message_id])
            svc.confirm(hyp.record_id, subject_id=SUBJECT, message_id=m2.message_id)
            svc.declare(subject_id=SUBJECT, domain="goals", key="g", value="x",
                        message_id=m1.message_id)
            self.assertTrue(store.verify_chain())
            kinds = [e["payload"]["self_model"] for e in store.all()]
            self.assertEqual(kinds, ["hypothesized", "confirmed_by_user", "declared"])


class DecisionEngineCompositionTests(unittest.TestCase):
    """End-to-end asymmetry: composing decision_context with the real
    DecisionEngine. A hypothesis alone must not change the outcome; the
    same information confirmed by the user must."""

    def _request_from_context(self, svc, subject_id):
        from hos_engine.decision_engine import (
            DecisionCandidate,
            DecisionRequest,
            Goal,
            RiskReactionClass,
        )
        ctx = svc.decision_context(subject_id)
        goal_rec = ctx["goals"][0]
        goal = Goal(owner_id=subject_id, outcome=str(goal_rec.value),
                    horizon="30d", success_criterion="declared by user")
        # The caller's mapping rule: only GATE-GRADE constraints may mark a
        # candidate infeasible. Advisory hypotheses are visible but inert.
        evenings_blocked = any(
            "wieczor" in str(r.value).lower() for r in ctx["constraints"])
        evening = DecisionCandidate(
            candidate_id="evening_training", description="Trening wieczorem",
            source="knowledge-map", risk_class=RiskReactionClass.NISKIE,
            evidence_level=5, burden=1, feasible=not evenings_blocked)
        morning = DecisionCandidate(
            candidate_id="morning_light", description="Poranne światło",
            source="knowledge-map", risk_class=RiskReactionClass.NISKIE,
            evidence_level=4, burden=1)
        return DecisionRequest(
            request_id="REQ-1", owner_id=subject_id,
            content="co poprawi energię?", domain="energy",
            goal=goal, candidates=(evening, morning))

    def test_hypothesis_does_not_change_outcome_until_confirmed(self):
        from hos_engine.decision_engine import DecisionEngine
        svc = service()
        it = start_chat(svc)
        m = svc.interactions.append(it.interaction_id, author=MessageAuthor.USER,
                                    text="Zależy mi na energii.")
        svc.declare(subject_id=SUBJECT, domain="goals", key="goal_candidate",
                    value="więcej energii", message_id=m.message_id)
        hyp = svc.hypothesize(subject_id=SUBJECT, domain="constraints",
                              key="schedule", value="wieczory zajęte",
                              confidence=0.6, supported_by=[m.message_id])
        engine = DecisionEngine()

        before = engine.decide(self._request_from_context(svc, SUBJECT))
        self.assertEqual(before.chosen.candidate_id, "evening_training")
        self.assertEqual(before.excluded, ())  # hypothesis was inert

        m2 = svc.interactions.append(it.interaction_id, author=MessageAuthor.USER,
                                     text="Tak, wieczory faktycznie odpadają.")
        svc.confirm(hyp.record_id, subject_id=SUBJECT, message_id=m2.message_id)

        after = engine.decide(self._request_from_context(svc, SUBJECT))
        self.assertEqual(after.chosen.candidate_id, "morning_light")
        self.assertIn("evening_training", after.excluded)  # gate, not ranking


class ConfidenceBandTests(unittest.TestCase):
    def test_bands_are_coarse_not_falsely_precise(self):
        self.assertEqual(confidence_band(0.1), "LOW")
        self.assertEqual(confidence_band(0.5), "MEDIUM")
        self.assertEqual(confidence_band(0.9), "HIGH")


if __name__ == "__main__":
    unittest.main()
