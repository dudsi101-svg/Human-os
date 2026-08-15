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
