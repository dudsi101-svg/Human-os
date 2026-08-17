from __future__ import annotations

import unittest
from dataclasses import replace

from hos_engine.decision_engine import (
    AbstentionReason,
    DecisionCandidate,
    DecisionEngine,
    DecisionGate,
    DecisionOutcomeKind,
    DecisionRequest,
    EscalationType,
    Goal,
    RecommendationClass,
    RiskReactionClass,
)


def goal(owner: str = "HOS-HUM-000001") -> Goal:
    return Goal(
        owner_id=owner,
        outcome="Sleep 7h30 on average",
        horizon="30 days",
        success_criterion="Mean sleep >= 7h30 over the last 14 days",
    )


def candidate(**overrides) -> DecisionCandidate:
    defaults = {
        "candidate_id": "CAND-1",
        "description": "Fixed lights-out time",
        "source": "knowledge-map",
        "risk_class": RiskReactionClass.NISKIE,
        "evidence_level": 3,
    }
    defaults.update(overrides)
    return DecisionCandidate(**defaults)


def request(**overrides) -> DecisionRequest:
    defaults = {
        "request_id": "REQ-1",
        "owner_id": "HOS-HUM-000001",
        "content": "How do I improve my sleep?",
        "domain": "sleep",
        "goal": goal(),
        "candidates": (candidate(),),
    }
    defaults.update(overrides)
    return DecisionRequest(**defaults)


class DecisionEngineHappyPathTests(unittest.TestCase):
    def setUp(self):
        self.engine = DecisionEngine()

    def test_low_risk_candidate_is_recommended(self):
        outcome = self.engine.decide(request())
        self.assertEqual(outcome.kind, DecisionOutcomeKind.RECOMMENDATION)
        self.assertEqual(outcome.recommendation_class, RecommendationClass.RC3_SIMPLE_LOW_RISK_STEP)
        self.assertEqual(outcome.chosen.candidate_id, "CAND-1")

    def test_ranking_prefers_lower_risk_then_stronger_evidence(self):
        risky = candidate(candidate_id="RISKY", risk_class=RiskReactionClass.UMIARKOWANE, evidence_level=5)
        weak = candidate(candidate_id="WEAK", evidence_level=2)
        strong = candidate(candidate_id="STRONG", evidence_level=5)
        outcome = self.engine.decide(request(candidates=(risky, weak, strong)))
        self.assertEqual(outcome.chosen.candidate_id, "STRONG")
        self.assertEqual([c.candidate_id for c in outcome.alternatives], ["WEAK", "RISKY"])

    def test_elevated_risk_yields_conditional_recommendation(self):
        elevated = candidate(risk_class=RiskReactionClass.PODWYZSZONE, evidence_level=4)
        outcome = self.engine.decide(request(candidates=(elevated,)))
        self.assertEqual(outcome.recommendation_class, RecommendationClass.RC5_CONDITIONAL)
        self.assertEqual(outcome.escalation, EscalationType.CONDITIONAL)


class DecisionEngineGateTests(unittest.TestCase):
    def setUp(self):
        self.engine = DecisionEngine()

    def test_red_flags_hard_escalate_before_candidates_are_touched(self):
        outcome = self.engine.decide(request(red_flags=("chest pain",)))
        self.assertEqual(outcome.kind, DecisionOutcomeKind.ESCALATION)
        self.assertEqual(outcome.escalation, EscalationType.HARD)
        self.assertEqual(outcome.abstention_reason, AbstentionReason.SUSPECTED_CRISIS)
        self.assertEqual(outcome.gate_results[0].gate, DecisionGate.G3_ACUTE_RISK)

    def test_missing_consent_abstains(self):
        outcome = self.engine.decide(request(consent_granted=False))
        self.assertEqual(outcome.kind, DecisionOutcomeKind.ABSTENTION)
        self.assertEqual(outcome.gate_results[0].gate, DecisionGate.G1_CONSENT)

    def test_missing_goal_abstains_with_no_clear_goal(self):
        outcome = self.engine.decide(request(goal=None))
        self.assertEqual(outcome.abstention_reason, AbstentionReason.NO_CLEAR_GOAL)

    def test_goal_owned_by_someone_else_abstains(self):
        outcome = self.engine.decide(request(goal=goal(owner="HOS-HUM-000999")))
        self.assertEqual(outcome.abstention_reason, AbstentionReason.NO_CLEAR_GOAL)

    def test_unlawful_candidate_is_excluded_at_g0(self):
        outcome = self.engine.decide(request(candidates=(candidate(lawful=False),)))
        self.assertEqual(outcome.kind, DecisionOutcomeKind.ABSTENTION)
        self.assertIn("CAND-1", outcome.excluded)
        self.assertEqual(outcome.gate_results[0].gate, DecisionGate.G0_LEGALITY_CONSTITUTION)

    def test_contraindication_excludes_at_g4(self):
        outcome = self.engine.decide(request(candidates=(candidate(contraindicated=True),)))
        self.assertEqual(outcome.gate_results[0].gate, DecisionGate.G4_CONTRAINDICATIONS)

    def test_evidence_asymmetry_blocks_underevidenced_risky_candidate(self):
        underevidenced = candidate(risk_class=RiskReactionClass.WYSOKIE, evidence_level=3)
        outcome = self.engine.decide(request(candidates=(underevidenced,)))
        self.assertEqual(outcome.kind, DecisionOutcomeKind.ABSTENTION)
        self.assertEqual(outcome.gate_results[0].gate, DecisionGate.G5_EVIDENCE_THRESHOLD)

    def test_critical_risk_is_never_admissible_even_at_max_evidence(self):
        critical = candidate(risk_class=RiskReactionClass.KRYTYCZNE, evidence_level=5)
        outcome = self.engine.decide(request(candidates=(critical,)))
        self.assertEqual(outcome.kind, DecisionOutcomeKind.ABSTENTION)
        self.assertEqual(outcome.abstention_reason, AbstentionReason.EXCESSIVE_RISK)

    def test_unmonitorable_candidate_is_excluded_at_g7(self):
        outcome = self.engine.decide(request(candidates=(candidate(monitorable=False),)))
        self.assertEqual(outcome.gate_results[0].gate, DecisionGate.G7_MONITORABILITY)

    def test_third_party_harm_excludes_at_g8(self):
        outcome = self.engine.decide(request(candidates=(candidate(harms_third_parties=True),)))
        self.assertEqual(outcome.gate_results[0].gate, DecisionGate.G8_THIRD_PARTY_IMPACT)

    def test_no_candidates_abstains_with_insufficient_data(self):
        outcome = self.engine.decide(request(candidates=()))
        self.assertEqual(outcome.abstention_reason, AbstentionReason.INSUFFICIENT_DATA)


class DecisionEngineInvariantTests(unittest.TestCase):
    """The two hardest constitutional rules from ADR-DECISION-005."""

    def setUp(self):
        self.engine = DecisionEngine()

    def test_user_determination_never_changes_any_outcome(self):
        critical = candidate(risk_class=RiskReactionClass.KRYTYCZNE, evidence_level=5)
        base = request(candidates=(critical,))
        determined = replace(base, user_determination=True)
        self.assertEqual(self.engine.decide(base).kind, self.engine.decide(determined).kind)
        self.assertEqual(
            self.engine.decide(base).abstention_reason,
            self.engine.decide(determined).abstention_reason,
        )

    def test_sponsorship_never_improves_ranking(self):
        organic = candidate(candidate_id="ORGANIC", evidence_level=4)
        sponsored = candidate(candidate_id="SPONSORED", evidence_level=4, sponsored=True)
        outcome = self.engine.decide(request(candidates=(organic, sponsored)))
        # Equal on every ranking axis: the stable sort must keep declaration
        # order, so sponsorship alone can never move a candidate up.
        self.assertEqual(outcome.chosen.candidate_id, "ORGANIC")

    def test_excluded_candidate_never_reenters_ranking(self):
        barred = candidate(candidate_id="BARRED", lawful=False, evidence_level=5)
        modest = candidate(candidate_id="MODEST", evidence_level=1)
        outcome = self.engine.decide(request(candidates=(barred, modest)))
        self.assertEqual(outcome.chosen.candidate_id, "MODEST")
        self.assertIn("BARRED", outcome.excluded)
        self.assertNotIn("BARRED", [c.candidate_id for c in outcome.alternatives])


if __name__ == "__main__":
    unittest.main()


class EvidenceScaleAndCriticalTests(unittest.TestCase):
    """Regression: 10k-iteration user simulation (2026-08-17) found that an
    out-of-range evidence_level (>=6) let an R-KRYTYCZNE candidate clear the
    'never admissible' threshold and be recommended."""

    def _cand(self, **over):
        base = {
            "candidate_id": "C", "description": "d", "source": "s",
            "risk_class": RiskReactionClass.NISKIE, "evidence_level": 1,
        }
        base.update(over)
        return DecisionCandidate(**base)

    def test_evidence_level_must_be_on_0_5_scale(self):
        for bad in (-1, 6, 99):
            with self.assertRaises(ValueError):
                self._cand(evidence_level=bad)

    def test_krytyczne_is_never_recommended_even_with_max_evidence(self):
        cand = self._cand(risk_class=RiskReactionClass.KRYTYCZNE, evidence_level=5)
        req = DecisionRequest(
            request_id="R", owner_id="O", content="c", domain="d",
            goal=Goal(owner_id="O", outcome="o", horizon="h", success_criterion="s"),
            candidates=(cand,), consent_granted=True,
        )
        out = DecisionEngine().decide(req)
        self.assertNotEqual(out.kind, DecisionOutcomeKind.RECOMMENDATION)
        self.assertIsNone(out.chosen)
        self.assertIn("C", out.excluded)


class ShadowScaleTests(unittest.TestCase):
    """DD-006 shadow phase: DI/IQ/AR measurements on a request are
    interpreted under the signed policies and attached to the outcome,
    and can never change the decision itself."""

    POLICY_FILE = "policies/scale.interpretation.policies.json"

    def setUp(self):
        from hos_engine.decision_scales import (
            ScaleInterpreter,
            load_policies_json,
        )
        self.interpreters = {
            kind: ScaleInterpreter(policy)
            for kind, policy in load_policies_json(self.POLICY_FILE).items()
        }

    def _measurements(self):
        from hos_engine.decision_scales import ScaleKind, ScaleMeasurement
        basis = "syntetyczna deklaracja testowa -- nie wartosc zalecana"
        return (
            ScaleMeasurement(scale=ScaleKind.INPUT_QUALITY, code="IQ0",
                             declared_by="HOS-HUM-000001", basis=basis),
            ScaleMeasurement(scale=ScaleKind.ACTION_READINESS, code="AR0",
                             declared_by="HOS-HUM-000001", basis=basis),
            ScaleMeasurement(scale=ScaleKind.DECISION_INTENT, code="DI-8",
                             declared_by="HOS-HUM-000001", basis=basis),
        )

    def test_shadow_readings_are_attached_under_signed_policy(self):
        from hos_engine.decision_scales import InterpretationOutcomeKind
        engine = DecisionEngine(shadow_interpreters=self.interpreters)
        outcome = engine.decide(request(measurements=self._measurements()))
        self.assertEqual(len(outcome.shadow_interpretations), 3)
        for reading in outcome.shadow_interpretations:
            self.assertEqual(reading.kind, InterpretationOutcomeKind.INTERPRETED)
            self.assertEqual(reading.policy_version, "0.2.0")

    def test_worst_case_measurements_never_change_the_decision(self):
        # IQ0/AR0/DI-8 are the most alarming codes on each scale; in the
        # shadow phase they still must not move the outcome at all.
        plain = DecisionEngine().decide(request())
        shadowed = DecisionEngine(shadow_interpreters=self.interpreters).decide(
            request(measurements=self._measurements()),
        )
        for field_name in (
            "kind", "recommendation_class", "abstention_reason",
            "escalation", "excluded", "gate_results", "reason",
        ):
            self.assertEqual(
                getattr(plain, field_name), getattr(shadowed, field_name),
            )
        self.assertEqual(plain.chosen.candidate_id, shadowed.chosen.candidate_id)

    def test_missing_interpreter_yields_configuration_required(self):
        from hos_engine.decision_scales import InterpretationOutcomeKind
        engine = DecisionEngine()  # no shadow interpreters configured
        outcome = engine.decide(request(measurements=self._measurements()))
        self.assertEqual(len(outcome.shadow_interpretations), 3)
        for reading in outcome.shadow_interpretations:
            self.assertEqual(
                reading.kind, InterpretationOutcomeKind.CONFIGURATION_REQUIRED,
            )

    def test_no_measurements_means_no_shadow_section(self):
        outcome = DecisionEngine(shadow_interpreters=self.interpreters).decide(request())
        self.assertEqual(outcome.shadow_interpretations, ())
