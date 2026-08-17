"""Golden scenarios: engine side of the app-mock <-> engine conformance test.

Scenario ids (GS1..GS4) are shared with the app-side probe
(session scratchpad ``golden_nof1.js``) and the divergence table in
``docs/APP_CORE_CONTRACT.md``. This file asserts what the ENGINE does;
the app probe records what the MOCK does; divergences are documented,
never papered over (ADR-ARCH-003).
"""

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
    OutcomeCode,
    ProcessClass,
    SafetyEvent,
    SafetySeverity,
)


def _master():
    return MasterTest(
        what_it_tests="x", why_protocol_admissible="x", baseline_reference="x",
        what_is_measured="x", how_harm_is_recognized="x", when_to_stop="x",
        confounding_factors="x", decision_enabled="x",
    )


def _exp(process_class=ProcessClass.XP1_MICRO_INTERVENTION, consent=True):
    return Experiment(
        hypothesis=Hypothesis(statement="s", direction="up", horizon_days=7),
        protocol=ExperimentProtocol(description="d", duration_days=7, stop_rules=["stop"]),
        metrics=[
            Metric(name="outcome", kind=MetricKind.OUTCOME),
            Metric(name="guard", kind=MetricKind.GUARD, stop_threshold=7.0),
        ],
        process_class=process_class,
        owner_id="HOS-HUM-000001",
        evidence_domain=EvidenceDomain.CAUSAL,
        consent_confirmed=consent,
        baseline_quality=BaselineQuality.BL2,
    )


class TestGoldenScenariosEngineSide(unittest.TestCase):
    """GS1..GS4 as the engine answers them."""

    def setUp(self):
        self.engine = ExperimentEngine()

    def test_gs1_launch_without_consent_refused(self):
        # App mock divergence D-GS1: the mock's startExperiment() does not
        # gate on any consent - documented in APP_CORE_CONTRACT.md.
        decision = self.engine.launch(_exp(consent=False), _master(), AuthorityRole.OWNER)
        self.assertFalse(decision.launched)
        self.assertIn("consent not confirmed", decision.reasons)

    def test_gs2_inadmissible_process_refused_outright(self):
        # App mock: G4 regex blocks substance ideas at adoption - aligned
        # in effect (both stop before execution), different mechanism.
        decision = self.engine.launch(_exp(process_class=ProcessClass.XP8_INADMISSIBLE), _master(), AuthorityRole.OWNER)
        self.assertFalse(decision.launched)

    def test_gs3_se2_holds_the_experiment(self):
        exp = _exp()
        self.engine.launch(exp, _master(), AuthorityRole.OWNER)
        self.engine.activate(exp)
        self.engine.report_safety_event(exp, SafetyEvent(severity=SafetySeverity.SE2, description="x", day=1))
        self.assertEqual(exp.state, CycleState.HOLD)  # aligned with mock (SE2 -> HOLD)

    def test_gs4_inconclusive_is_first_class(self):
        # App mock divergence D-GS4: the mock has no INCONCLUSIVE phase at
        # all (done/stopped only) - documented in APP_CORE_CONTRACT.md.
        exp = _exp()
        self.engine.launch(exp, _master(), AuthorityRole.OWNER)
        self.engine.activate(exp)
        result = self.engine.conclude(
            exp, OutcomeCode.R_LEARNING, "confounded", inconclusive_reason="travel"
        )
        self.assertIsInstance(result, ExperimentResult)
        self.assertEqual(exp.state, CycleState.INCONCLUSIVE)


if __name__ == "__main__":
    unittest.main()
