"""Tests for the Layer 6 Experiment Engine slice (ADR-EXP-001..005)."""

import unittest

from hos_engine.authority import AuthorityRole
from hos_engine.experiment_engine import (
    BaselineQuality,
    CycleState,
    EvidenceDomain,
    Experiment,
    ExperimentEngine,
    ExperimentProtocol,
    ExperimentResult,
    Hypothesis,
    MasterTest,
    Metric,
    MetricKind,
    Observation,
    ObservationSource,
    OutcomeCode,
    ProcessClass,
    SafetyEvent,
    SafetySeverity,
)


class _MemorySink:
    def __init__(self):
        self.events = []

    def append(self, event):
        self.events.append(event)


def _master_test():
    return MasterTest(
        what_it_tests="effect of an evening walk on sleep quality",
        why_protocol_admissible="low-burden, reversible micro-intervention",
        baseline_reference="7 days of sleep tracking before the change",
        what_is_measured="self-reported sleep quality 1-10 and sleep hours",
        how_harm_is_recognized="guard metric: evening anxiety above threshold",
        when_to_stop="guard threshold crossed or SE2+ safety event",
        confounding_factors="travel, illness, unusual work stress",
        decision_enabled="keep, drop, or adjust the walk habit",
    )


def _experiment(process_class=ProcessClass.XP1_MICRO_INTERVENTION, **overrides):
    metrics = overrides.pop(
        "metrics",
        [
            Metric(name="sleep quality", kind=MetricKind.OUTCOME, unit="1-10"),
            Metric(name="evening anxiety", kind=MetricKind.GUARD, stop_threshold=7.0),
        ],
    )
    defaults = {
        "hypothesis": Hypothesis(statement="walk improves sleep", direction="up", horizon_days=14),
        "protocol": ExperimentProtocol(
            description="20 min walk after dinner",
            duration_days=14,
            stop_rules=["guard metric above 7", "any SE2+ event"],
        ),
        "metrics": metrics,
        "process_class": process_class,
        "owner_id": "HOS-HUM-000001",
        "evidence_domain": EvidenceDomain.CAUSAL,
        "consent_confirmed": True,
        "baseline_quality": BaselineQuality.BL2,
    }
    defaults.update(overrides)
    return Experiment(**defaults)


class TestLaunchGate(unittest.TestCase):
    def setUp(self):
        self.sink = _MemorySink()
        self.engine = ExperimentEngine(event_store=self.sink)

    def test_happy_path_full_cycle(self):
        exp = _experiment()
        decision = self.engine.launch(exp, _master_test(), AuthorityRole.OWNER)
        self.assertTrue(decision.launched)
        self.assertEqual(exp.state, CycleState.BASELINE)
        self.assertTrue(self.engine.activate(exp).applied)
        result = self.engine.conclude(exp, OutcomeCode.R_PLUS, "clear improvement")
        self.assertIsInstance(result, ExperimentResult)
        self.assertEqual(exp.state, CycleState.COMPLETED)
        self.assertFalse(result.exploratory)
        kinds = [e["payload_kind"] for e in self.sink.events]
        self.assertIn("experiment_launched", kinds)
        self.assertIn("experiment_concluded", kinds)

    def test_xp8_rejected_outright(self):
        exp = _experiment(process_class=ProcessClass.XP8_INADMISSIBLE)
        decision = self.engine.launch(exp, _master_test(), AuthorityRole.OWNER)
        self.assertFalse(decision.launched)
        self.assertIn("XP-8", decision.reasons[0])
        self.assertEqual(exp.state, CycleState.DRAFT)

    def test_master_test_incomplete_refuses_and_names_missing(self):
        exp = _experiment()
        incomplete = MasterTest(
            what_it_tests="x",
            why_protocol_admissible="",
            baseline_reference="x",
            what_is_measured="x",
            how_harm_is_recognized="  ",
            when_to_stop="x",
            confounding_factors="x",
            decision_enabled="x",
        )
        decision = self.engine.launch(exp, incomplete, AuthorityRole.OWNER)
        self.assertFalse(decision.launched)
        joined = " ".join(decision.reasons)
        self.assertIn("why_protocol_admissible", joined)
        self.assertIn("how_harm_is_recognized", joined)

    def test_gates_are_non_fungible(self):
        # Missing consent is not offset by anything else being excellent.
        exp = _experiment(consent_confirmed=False, baseline_quality=BaselineQuality.BL5)
        decision = self.engine.launch(exp, _master_test(), AuthorityRole.OWNER)
        self.assertFalse(decision.launched)
        self.assertIn("consent not confirmed", decision.reasons)
        # Missing guard metric refuses independently.
        exp2 = _experiment(metrics=[Metric(name="sleep", kind=MetricKind.OUTCOME)])
        decision2 = self.engine.launch(exp2, _master_test(), AuthorityRole.OWNER)
        self.assertFalse(decision2.launched)
        self.assertIn("no guard (protective) metric defined", decision2.reasons)

    def test_agent_cannot_launch_and_refusal_is_logged(self):
        exp = _experiment()
        for role in (AuthorityRole.AGENT, AuthorityRole.SERVICE, AuthorityRole.SYSTEM_PROCESS):
            decision = self.engine.launch(exp, _master_test(), role)
            self.assertFalse(decision.launched)
        refusals = [e for e in self.sink.events if e["payload_kind"] == "experiment_launch_refused"]
        self.assertEqual(len(refusals), 3)

    def test_xp7_requires_specialist_conditions_no_override(self):
        exp = _experiment(process_class=ProcessClass.XP7_HIGH_CONTROL)
        decision = self.engine.launch(exp, _master_test(), AuthorityRole.OWNER)
        self.assertFalse(decision.launched)
        joined = " ".join(decision.reasons)
        self.assertIn("specialist approval", joined)
        self.assertIn("legality", joined)
        self.assertIn("monitoring plan", joined)
        exp.specialist_approved_by = "HOS-HUM-000099"
        exp.legality_confirmed = True
        exp.monitoring_plan = "weekly labs, daily check-in, emergency contact"
        self.assertTrue(self.engine.launch(exp, _master_test(), AuthorityRole.OWNER).launched)


class TestSafetyAndState(unittest.TestCase):
    def setUp(self):
        self.sink = _MemorySink()
        self.engine = ExperimentEngine(event_store=self.sink)
        self.exp = _experiment()
        self.engine.launch(self.exp, _master_test(), AuthorityRole.OWNER)
        self.engine.activate(self.exp)

    def test_baseline_bl0_blocks_activation(self):
        exp = _experiment(baseline_quality=BaselineQuality.BL0)
        self.engine.launch(exp, _master_test(), AuthorityRole.OWNER)
        result = self.engine.activate(exp)
        self.assertFalse(result.applied)
        self.assertEqual(exp.state, CycleState.BASELINE)

    def test_se2_holds_se3_stops_and_escalates(self):
        r2 = self.engine.report_safety_event(
            self.exp, SafetyEvent(severity=SafetySeverity.SE2, description="rising headaches", day=4)
        )
        self.assertTrue(r2.applied)
        self.assertEqual(self.exp.state, CycleState.HOLD)
        self.assertFalse(self.exp.escalated)
        self.engine.resume(self.exp, AuthorityRole.OWNER)
        r3 = self.engine.report_safety_event(
            self.exp, SafetyEvent(severity=SafetySeverity.SE3, description="chest pain", day=5)
        )
        self.assertTrue(r3.applied)
        self.assertEqual(self.exp.state, CycleState.STOPPED)
        self.assertTrue(self.exp.escalated)

    def test_se0_continues_without_transition(self):
        result = self.engine.report_safety_event(
            self.exp, SafetyEvent(severity=SafetySeverity.SE0, description="expected mild soreness", day=2)
        )
        self.assertTrue(result.applied)
        self.assertEqual(self.exp.state, CycleState.ACTIVE)

    def test_agent_cannot_resume_held_experiment(self):
        self.engine.report_safety_event(
            self.exp, SafetyEvent(severity=SafetySeverity.SE2, description="hold trigger", day=3)
        )
        result = self.engine.resume(self.exp, AuthorityRole.AGENT)
        self.assertFalse(result.applied)
        self.assertEqual(self.exp.state, CycleState.HOLD)

    def test_terminal_states_are_terminal(self):
        self.engine.report_safety_event(
            self.exp, SafetyEvent(severity=SafetySeverity.SE4, description="emergency", day=6)
        )
        self.assertEqual(self.exp.state, CycleState.STOPPED)
        self.assertFalse(self.engine.activate(self.exp).applied)


class TestProvenanceAndFirewall(unittest.TestCase):
    def setUp(self):
        self.engine = ExperimentEngine()
        self.exp = _experiment()
        self.engine.launch(self.exp, _master_test(), AuthorityRole.OWNER)
        self.engine.activate(self.exp)

    def test_observations_never_merge_across_sources(self):
        metric_id = self.exp.metrics[0].id
        self.engine.record_observation(
            self.exp, Observation(metric_id=metric_id, day=1, value=6.0, source=ObservationSource.SELF_REPORT)
        )
        self.engine.record_observation(
            self.exp, Observation(metric_id=metric_id, day=1, value=7.5, source=ObservationSource.DEVICE)
        )
        self.assertEqual(len(self.exp.observations), 2)
        agreement = self.engine.source_agreement(self.exp, metric_id, day=1)
        self.assertEqual(agreement, {"SELF_REPORT": 6.0, "DEVICE": 7.5})

    def test_post_hoc_hypothesis_amendment_is_exploratory_and_versioned(self):
        self.engine.record_observation(
            self.exp,
            Observation(
                metric_id=self.exp.metrics[0].id, day=1, value=6.0, source=ObservationSource.SELF_REPORT
            ),
        )
        original = self.exp.hypothesis
        amended = self.engine.amend_hypothesis(self.exp, "walk mainly reduces stress", "up")
        self.assertTrue(amended.exploratory)
        self.assertEqual(amended.supersedes, original.id)
        self.assertEqual(amended.version, original.version + 1)
        self.assertIn(original, self.exp.hypothesis_history)

    def test_threshold_change_after_launch_forces_exploratory_result(self):
        guard = self.exp.guard_metrics()[0]
        guard.stop_threshold = 9.0  # moved after seeing how things go
        result = self.engine.conclude(self.exp, OutcomeCode.R_PLUS, "improved")
        self.assertIsInstance(result, ExperimentResult)
        self.assertTrue(result.exploratory)

    def test_reflective_experiment_is_firewalled_from_causal_evidence(self):
        exp = _experiment(process_class=ProcessClass.XP6_REFLECTIVE_PRACTICE)
        self.assertTrue(
            ExperimentEngine().launch(exp, _master_test(), AuthorityRole.OWNER).launched
        )
        self.assertEqual(exp.evidence_domain, EvidenceDomain.INTERPRETIVE)
        engine = ExperimentEngine()
        engine.activate(exp)
        result = engine.conclude(exp, OutcomeCode.R_PLUS, "felt clarifying")
        self.assertIsInstance(result, ExperimentResult)
        self.assertFalse(result.causal_evidence_eligible)

    def test_inconclusive_is_first_class(self):
        result = self.engine.conclude(
            self.exp,
            OutcomeCode.R_LEARNING,
            "travel disrupted most of the active phase",
            inconclusive_reason="confounded by travel",
        )
        self.assertIsInstance(result, ExperimentResult)
        self.assertEqual(self.exp.state, CycleState.INCONCLUSIVE)
        self.assertEqual(result.inconclusive_reason, "confounded by travel")


if __name__ == "__main__":
    unittest.main()


class TestAdaptationAndPortfolio(unittest.TestCase):
    def setUp(self):
        from hos_engine.experiment_engine import ExperimentPortfolio

        self.engine = ExperimentEngine()
        self.portfolio_cls = ExperimentPortfolio
        self.exp = _experiment()
        self.engine.launch(self.exp, _master_test(), AuthorityRole.OWNER)
        self.engine.activate(self.exp)

    def test_adaptation_versions_protocol_and_keeps_history(self):
        old = self.exp.protocol
        result = self.engine.adapt_protocol(self.exp, "walk moved to before dinner", AuthorityRole.OWNER)
        self.assertTrue(result.applied)
        self.assertEqual(self.exp.protocol.version, old.version + 1)
        self.assertIn(old, self.exp.protocol_history)

    def test_stacking_intervention_mid_run_is_banned(self):
        result = self.engine.adapt_protocol(
            self.exp, "walk plus new supplement", AuthorityRole.OWNER, adds_new_intervention=True
        )
        self.assertFalse(result.applied)
        self.assertIn("§28.2", result.reasons[0])

    def test_agent_cannot_adapt_protocol(self):
        result = self.engine.adapt_protocol(self.exp, "tweak", AuthorityRole.AGENT)
        self.assertFalse(result.applied)

    def test_no_deletion_api_for_observations_or_safety_events(self):
        banned = [n for n in dir(ExperimentEngine) if "remove" in n or "delete" in n]
        self.assertEqual(banned, [])

    def test_portfolio_limit_is_explicit_and_enforced(self):
        with self.assertRaises(TypeError):
            self.portfolio_cls()  # no default limit exists on purpose (DD-017)
        with self.assertRaises(ValueError):
            self.portfolio_cls(0)
        portfolio = self.portfolio_cls(1)
        self.assertTrue(portfolio.admit(self.exp).admitted)
        second = _experiment()
        engine2 = ExperimentEngine()
        engine2.launch(second, _master_test(), AuthorityRole.OWNER)
        decision = portfolio.admit(second)
        self.assertFalse(decision.admitted)
        self.assertIn("portfolio limit", decision.reasons[0])

    def test_infrastructural_experiments_do_not_compete(self):
        portfolio = self.portfolio_cls(1)
        portfolio.admit(self.exp)
        infra = _experiment(infrastructural=True)
        engine2 = ExperimentEngine()
        engine2.launch(infra, _master_test(), AuthorityRole.OWNER)
        self.assertTrue(portfolio.admit(infra).admitted)
        self.assertEqual(portfolio.active_count(), 1)

    def test_interactions_are_declared_not_inferred(self):
        portfolio = self.portfolio_cls(2)
        second = _experiment()
        portfolio.admit(self.exp)
        portfolio.admit(second)
        portfolio.declare_interaction(self.exp, second, "both touch evening routine")
        self.assertEqual(len(portfolio.interactions), 1)
        self.assertEqual(portfolio.interactions[0]["note"], "both touch evening routine")
