"""Layer 6 Experiment Engine — first executable slice.

Implements the core, safety-bearing subset of the Layer 6 specification
(``docs/LAYER_6_EXPERIMENT_ENGINE_DIGEST.md``) under ADR-EXP-001..005:

- Layer 6's own coded scales (``ProcessClass`` XP-0..XP-8, ``SafetySeverity``
  SE0..SE4, ``BaselineQuality`` BL0..BL5) — deliberately distinct from the
  Constitution's R0-R4 (ADR-EXP-001; never conflate the taxonomies).
- The mandatory pre-launch explainability gate ("test nadrzędny", source
  §0.5): an experiment cannot launch unless all eight questions are
  answered (ADR-EXP-001).
- The non-fungibility rule (source §3.1, ADR-EXP-002): safety, baseline
  quality, and consent gate independently; none can compensate another.
  There is deliberately no parameter anywhere that trades one for another.
- Versioned objects that are never silently merged (ADR-EXP-003):
  observations from different source kinds stay separate objects; editing
  a hypothesis or thresholds after results creates a new version marked
  exploratory instead of rewriting history (source §7.4).
- AI role boundaries (ADR-EXP-004): launch, resume, and exposure changes
  refuse ``AGENT``/``SERVICE``/``SYSTEM_PROCESS`` actors structurally —
  there is no API an agent could call to auto-start an experiment or
  auto-increase exposure, and the refusal itself is logged.
- The epistemic firewall (ADR-EXP-005): reflective/symbolic experiments
  (XP-6) are forced into the ``INTERPRETIVE`` evidence domain and their
  results are structurally ineligible as causal/clinical evidence.

Refusals follow the Proof-Kernel/DecisionEngine convention: a refusal is a
first-class ``LaunchDecision``/``TransitionResult`` outcome, never an
exception — a hard gate runs before anything downstream mutates state.

Durable events go to an optional ``EventStore``/``SQLiteEventStore`` via the
``STATE_OBSERVED`` canonical type with an ``experiment_*`` payload kind —
same interim pattern DD-003 used for recovery before ``RECOVERY_*`` types
existed; dedicated ``EXPERIMENT_*`` event types are future vocabulary work.

This is a bounded slice. Second increment adds: the EC/MQ/PF/DQ/CA/PE
quality scales as ordinal labels (class assignment from raw data would
need an explicit, versioned interpretation config — the DD-006 pattern —
and is not implemented), protocol adaptation with the §28.2 bans the
digest quotes verbatim (full five-item list awaits source bytes, DD-017),
and ``ExperimentPortfolio`` (§29) whose active-changes limit is a
mandatory explicit argument because the digest does not carry the
concrete number (DD-017). Still not implemented: adaptive-experiment
stop rules (§28.3), trajectory model (§30), community contribution (§38).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from typing import Protocol as TypingProtocol

from .authority import AuthorityRole


def _new_id(prefix: str) -> str:
    return f"HOS-{prefix}-{uuid.uuid4().hex[:12].upper()}"


def _now() -> str:
    return datetime.now(UTC).isoformat()


class ProcessClass(str, Enum):
    """XP-0..XP-8 process classes (source §2.2). XP-8 is inadmissible."""

    XP0_OBSERVATION = "XP-0"
    XP1_MICRO_INTERVENTION = "XP-1"
    XP2_HABIT_BUILDING = "XP-2"
    XP3_COMPARATIVE = "XP-3"
    XP4_WITHDRAWAL_RETURN = "XP-4"
    XP5_SPECIALIST_MONITORED = "XP-5"
    XP6_REFLECTIVE_PRACTICE = "XP-6"
    XP7_HIGH_CONTROL = "XP-7"
    XP8_INADMISSIBLE = "XP-8"


class SafetySeverity(str, Enum):
    """SE0..SE4 safety-event severity with default reactions (source §15.2)."""

    SE0 = "SE0"  # no symptoms / expected mild discomfort -> continue, observe
    SE1 = "SE1"  # mild transient symptom -> extra monitoring, possible tweak
    SE2 = "SE2"  # moderate / functional decline / rising trend -> HOLD
    SE3 = "SE3"  # serious / health risk -> immediate STOP and escalation
    SE4 = "SE4"  # emergency / life threat -> immediate-help instruction, stop


class BaselineQuality(str, Enum):
    """BL0..BL5 baseline quality classes (source §10.2)."""

    BL0 = "BL0"
    BL1 = "BL1"
    BL2 = "BL2"
    BL3 = "BL3"
    BL4 = "BL4"
    BL5 = "BL5"


class CycleState(str, Enum):
    DRAFT = "DRAFT"
    BASELINE = "BASELINE"
    ACTIVE = "ACTIVE"
    HOLD = "HOLD"
    WASHOUT = "WASHOUT"
    MAINTENANCE = "MAINTENANCE"
    COMPLETED = "COMPLETED"
    STOPPED = "STOPPED"
    INCONCLUSIVE = "INCONCLUSIVE"


ALLOWED_TRANSITIONS: dict[CycleState, set[CycleState]] = {
    CycleState.DRAFT: {CycleState.BASELINE, CycleState.STOPPED},
    CycleState.BASELINE: {CycleState.ACTIVE, CycleState.STOPPED, CycleState.INCONCLUSIVE},
    CycleState.ACTIVE: {
        CycleState.HOLD,
        CycleState.WASHOUT,
        CycleState.MAINTENANCE,
        CycleState.COMPLETED,
        CycleState.STOPPED,
        CycleState.INCONCLUSIVE,
    },
    CycleState.HOLD: {CycleState.ACTIVE, CycleState.STOPPED, CycleState.INCONCLUSIVE},
    CycleState.WASHOUT: {CycleState.COMPLETED, CycleState.INCONCLUSIVE, CycleState.STOPPED},
    CycleState.MAINTENANCE: {CycleState.COMPLETED, CycleState.STOPPED},
    CycleState.COMPLETED: set(),
    CycleState.STOPPED: set(),
    CycleState.INCONCLUSIVE: set(),
}


class OutcomeCode(str, Enum):
    """Result classes (source §27). Semantics live in the source table;
    the engine treats INCONCLUSIVE-compatible codes as first-class results,
    never as failures to be pressured into more data (source §47)."""

    R_PLUS = "R+"
    R_UNCERTAIN_PLUS = "R?+"
    R_ZERO = "R0"
    R_UNCERTAIN_ZERO = "R?0"
    R_MINUS = "R-"
    R_MIXED = "R±"
    R_LEARNING = "RL"
    R_WITHDRAWN = "RW"


class EvidenceDomain(str, Enum):
    """ADR-EXP-005: causal/clinical evidence vs. the interpretive domain
    behind the epistemic firewall. Interpretive results never raise causal,
    biological, or clinical evidence strength."""

    CAUSAL = "CAUSAL"
    INTERPRETIVE = "INTERPRETIVE"


class ObservationSource(str, Enum):
    """§4.2 ban on hidden merging: these stay separate objects forever."""

    SELF_REPORT = "SELF_REPORT"
    DEVICE = "DEVICE"
    LAB = "LAB"
    MODEL_PREDICTION = "MODEL_PREDICTION"
    EXPERT = "EXPERT"


class MetricKind(str, Enum):
    OUTCOME = "OUTCOME"
    PROCESS = "PROCESS"
    GUARD = "GUARD"  # protective metric with its own stop threshold ("antywynik")


class ContractCompleteness(str, Enum):
    """EC0..EC5 (source §5.2). Ordinal class labels only — assigning a class
    from raw data requires an explicit, versioned interpretation config (the
    DD-006 pattern); this module never infers a class silently."""

    EC0 = "EC0"
    EC1 = "EC1"
    EC2 = "EC2"
    EC3 = "EC3"
    EC4 = "EC4"
    EC5 = "EC5"


class MeasurementQuality(str, Enum):
    """MQ0..MQ5 (source §9.3). Labels only — see ContractCompleteness note."""

    MQ0 = "MQ0"
    MQ1 = "MQ1"
    MQ2 = "MQ2"
    MQ3 = "MQ3"
    MQ4 = "MQ4"
    MQ5 = "MQ5"


class ProtocolFidelity(str, Enum):
    """PF0..PF5 (source §12.2). Labels only. Compliance failures are never
    described in moralizing terms (source §12.4 "Zakaz moralizacji
    zgodności") — these are classes of fidelity, not judgments of character."""

    PF0 = "PF0"
    PF1 = "PF1"
    PF2 = "PF2"
    PF3 = "PF3"
    PF4 = "PF4"
    PF5 = "PF5"


class DataQuality(str, Enum):
    """DQ0..DQ5 (source §19.2). Labels only — see ContractCompleteness note."""

    DQ0 = "DQ0"
    DQ1 = "DQ1"
    DQ2 = "DQ2"
    DQ3 = "DQ3"
    DQ4 = "DQ4"
    DQ5 = "DQ5"


class CausalConfidence(str, Enum):
    """CA0..CA5 (source §26.2). Labels only. Interpretive-domain results can
    never raise this scale (ADR-EXP-005)."""

    CA0 = "CA0"
    CA1 = "CA1"
    CA2 = "CA2"
    CA3 = "CA3"
    CA4 = "CA4"
    CA5 = "CA5"


class PersonalEvidence(str, Enum):
    """PE0..PE5, the personal-evidence ladder (source appendix L). Personal
    evidence is never automatically population evidence (source §0.3)."""

    PE0 = "PE0"
    PE1 = "PE1"
    PE2 = "PE2"
    PE3 = "PE3"
    PE4 = "PE4"
    PE5 = "PE5"


_FORBIDDEN_ACTOR_ROLES = {
    AuthorityRole.AGENT,
    AuthorityRole.SERVICE,
    AuthorityRole.SYSTEM_PROCESS,
}


@dataclass(frozen=True)
class MasterTest:
    """The eight answers of the "test nadrzędny" (source §0.5).

    Every field must be a non-empty explanation; the launch gate refuses
    otherwise. Field order mirrors the verbatim sentence."""

    what_it_tests: str
    why_protocol_admissible: str
    baseline_reference: str
    what_is_measured: str
    how_harm_is_recognized: str
    when_to_stop: str
    confounding_factors: str
    decision_enabled: str

    def missing(self) -> list[str]:
        return [name for name, value in vars(self).items() if not str(value).strip()]


@dataclass
class Hypothesis:
    statement: str
    direction: str
    horizon_days: int
    id: str = field(default_factory=lambda: _new_id("HYP"))
    version: int = 1
    created_at: str = field(default_factory=_now)
    supersedes: str | None = None
    exploratory: bool = False  # set on post-result amendments (source §7.4)


@dataclass
class Metric:
    name: str
    kind: MetricKind
    unit: str = ""
    stop_threshold: float | None = None  # meaningful for GUARD metrics
    id: str = field(default_factory=lambda: _new_id("MET"))


@dataclass
class ExperimentProtocol:
    description: str
    duration_days: int
    stop_rules: list[str]
    id: str = field(default_factory=lambda: _new_id("PRO"))
    version: int = 1


@dataclass
class Observation:
    metric_id: str
    day: int
    value: float
    source: ObservationSource
    id: str = field(default_factory=lambda: _new_id("OBS"))
    recorded_at: str = field(default_factory=_now)


@dataclass
class SafetyEvent:
    severity: SafetySeverity
    description: str
    day: int
    id: str = field(default_factory=lambda: _new_id("SEV"))
    recorded_at: str = field(default_factory=_now)
    reaction: str = ""


@dataclass
class ExperimentResult:
    outcome: OutcomeCode
    summary: str
    exploratory: bool = False
    inconclusive_reason: str | None = None
    causal_evidence_eligible: bool = True
    id: str = field(default_factory=lambda: _new_id("RES"))
    created_at: str = field(default_factory=_now)


@dataclass
class Experiment:
    hypothesis: Hypothesis
    protocol: ExperimentProtocol
    metrics: list[Metric]
    process_class: ProcessClass
    owner_id: str
    evidence_domain: EvidenceDomain
    baseline_quality: BaselineQuality = BaselineQuality.BL0
    state: CycleState = CycleState.DRAFT
    consent_confirmed: bool = False
    specialist_approved_by: str | None = None  # required for XP-7
    legality_confirmed: bool = False  # required for XP-7
    monitoring_plan: str | None = None  # required for XP-7
    infrastructural: bool = False  # §29.3: confirmed-value routines in maintenance
    id: str = field(default_factory=lambda: _new_id("XPR"))
    created_at: str = field(default_factory=_now)
    observations: list[Observation] = field(default_factory=list)
    safety_events: list[SafetyEvent] = field(default_factory=list)
    hypothesis_history: list[Hypothesis] = field(default_factory=list)
    protocol_history: list[ExperimentProtocol] = field(default_factory=list)
    launch_thresholds: dict[str, float | None] = field(default_factory=dict)
    result: ExperimentResult | None = None
    escalated: bool = False

    def guard_metrics(self) -> list[Metric]:
        return [m for m in self.metrics if m.kind is MetricKind.GUARD]


@dataclass(frozen=True)
class LaunchDecision:
    launched: bool
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True)
class TransitionResult:
    applied: bool
    state: CycleState
    reasons: tuple[str, ...] = ()


class _EventSink(TypingProtocol):  # pragma: no cover - structural typing only
    def append(self, event: dict[str, Any]) -> Any: ...


class ExperimentEngine:
    """Gate-first coordinator for personal N-of-1 experiments.

    Mirrors the project-wide "hard gate before scoring" pattern: every
    refusal is an outcome object and stops the operation before any state
    mutates or persists.
    """

    def __init__(self, event_store: _EventSink | None = None) -> None:
        self._event_store = event_store

    # -- event plumbing ----------------------------------------------------

    def _emit(self, kind: str, experiment: Experiment, detail: dict[str, Any]) -> None:
        if self._event_store is None:
            return
        self._event_store.append(
            {
                "event_type": "STATE_OBSERVED",
                "payload_kind": kind,
                "experiment_id": experiment.id,
                "owner_id": experiment.owner_id,
                "state": experiment.state.value,
                "at": _now(),
                **detail,
            }
        )

    # -- launch gate (ADR-EXP-001/002/004) ---------------------------------

    def launch(
        self,
        experiment: Experiment,
        master_test: MasterTest,
        actor_role: AuthorityRole,
    ) -> LaunchDecision:
        reasons: list[str] = []

        # ADR-EXP-004: agents can never start an experiment; the refusal is logged.
        if actor_role in _FORBIDDEN_ACTOR_ROLES:
            decision = LaunchDecision(False, (f"actor role {actor_role.value} may not launch experiments",))
            self._emit("experiment_launch_refused", experiment, {"reasons": list(decision.reasons)})
            return decision

        # ADR-EXP-001: XP-8 is rejected outright, before anything else is weighed.
        if experiment.process_class is ProcessClass.XP8_INADMISSIBLE:
            decision = LaunchDecision(False, ("process class XP-8 is inadmissible",))
            self._emit("experiment_launch_refused", experiment, {"reasons": list(decision.reasons)})
            return decision

        # ADR-EXP-001: the eight-question explainability gate.
        missing = master_test.missing()
        if missing:
            reasons.append("master test incomplete: " + ", ".join(missing))

        # ADR-EXP-002: independent, non-fungible gates. Nothing offsets these.
        if not experiment.consent_confirmed:
            reasons.append("consent not confirmed")
        if not experiment.guard_metrics():
            reasons.append("no guard (protective) metric defined")
        if not experiment.protocol.stop_rules:
            reasons.append("protocol has no stop rules")

        # ADR-EXP-004 §34: high-control experiments need specialist conditions;
        # there is intentionally no override for user determination.
        if experiment.process_class is ProcessClass.XP7_HIGH_CONTROL:
            if not experiment.specialist_approved_by:
                reasons.append("XP-7 requires specialist approval")
            if not experiment.legality_confirmed:
                reasons.append("XP-7 requires confirmed legality")
            if not experiment.monitoring_plan:
                reasons.append("XP-7 requires a monitoring plan")

        if experiment.state is not CycleState.DRAFT:
            reasons.append(f"cannot launch from state {experiment.state.value}")

        if reasons:
            decision = LaunchDecision(False, tuple(reasons))
            self._emit("experiment_launch_refused", experiment, {"reasons": reasons})
            return decision

        # ADR-EXP-005: reflective/symbolic practice lives behind the firewall.
        if experiment.process_class is ProcessClass.XP6_REFLECTIVE_PRACTICE:
            experiment.evidence_domain = EvidenceDomain.INTERPRETIVE

        experiment.launch_thresholds = {m.id: m.stop_threshold for m in experiment.metrics}
        experiment.state = CycleState.BASELINE
        self._emit("experiment_launched", experiment, {"process_class": experiment.process_class.value})
        return LaunchDecision(True)

    # -- state machine -----------------------------------------------------

    def _transition(self, experiment: Experiment, target: CycleState, why: str) -> TransitionResult:
        if target not in ALLOWED_TRANSITIONS[experiment.state]:
            return TransitionResult(
                False, experiment.state, (f"transition {experiment.state.value} -> {target.value} not allowed",)
            )
        experiment.state = target
        self._emit("experiment_state_changed", experiment, {"why": why})
        return TransitionResult(True, target)

    def activate(self, experiment: Experiment) -> TransitionResult:
        # ADR-EXP-002: baseline quality gates independently; more later
        # measurements never substitute for a missing reference point.
        if experiment.state is CycleState.BASELINE and experiment.baseline_quality is BaselineQuality.BL0:
            return TransitionResult(False, experiment.state, ("baseline quality BL0 - reference point missing",))
        return self._transition(experiment, CycleState.ACTIVE, "activation")

    def resume(self, experiment: Experiment, actor_role: AuthorityRole) -> TransitionResult:
        if actor_role in _FORBIDDEN_ACTOR_ROLES:
            result = TransitionResult(
                False, experiment.state, (f"actor role {actor_role.value} may not resume a held experiment",)
            )
            self._emit("experiment_resume_refused", experiment, {"reasons": list(result.reasons)})
            return result
        return self._transition(experiment, CycleState.ACTIVE, "resumed after hold")

    # -- observations (ADR-EXP-003) ----------------------------------------

    def record_observation(self, experiment: Experiment, observation: Observation) -> None:
        """Observations are appended, never merged across sources (§4.2)."""
        experiment.observations.append(observation)
        self._emit(
            "experiment_observation",
            experiment,
            {"metric_id": observation.metric_id, "source": observation.source.value},
        )

    def source_agreement(self, experiment: Experiment, metric_id: str, day: int) -> dict[str, float]:
        """Show agreement/conflict between sources without collapsing them."""
        return {
            o.source.value: o.value
            for o in experiment.observations
            if o.metric_id == metric_id and o.day == day
        }

    # -- safety (source §15) ----------------------------------------------

    def report_safety_event(self, experiment: Experiment, event: SafetyEvent) -> TransitionResult:
        """Apply the default reaction for the severity class. Protective
        transitions here are automatic (like Recovery's protective modes) —
        weakening them to reduce burden is banned (source §14.3)."""
        experiment.safety_events.append(event)
        if event.severity is SafetySeverity.SE2:
            event.reaction = "hold for assessment"
            result = self._transition(experiment, CycleState.HOLD, f"SE2: {event.description}")
        elif event.severity is SafetySeverity.SE3:
            event.reaction = "immediate stop and escalation"
            experiment.escalated = True
            result = self._transition(experiment, CycleState.STOPPED, f"SE3: {event.description}")
        elif event.severity is SafetySeverity.SE4:
            event.reaction = "immediate-help instruction; no further experimentation"
            experiment.escalated = True
            result = self._transition(experiment, CycleState.STOPPED, f"SE4: {event.description}")
        else:
            event.reaction = "continue with observation" if event.severity is SafetySeverity.SE0 else "extra monitoring"
            result = TransitionResult(True, experiment.state)
        self._emit(
            "experiment_safety_event",
            experiment,
            {"severity": event.severity.value, "reaction": event.reaction},
        )
        return result

    # -- hypothesis integrity (source §7.4) --------------------------------

    def amend_hypothesis(self, experiment: Experiment, new_statement: str, new_direction: str) -> Hypothesis:
        """Amending after results exist creates a superseding version marked
        exploratory — a post-hoc explanation is never presented as predicted."""
        old = experiment.hypothesis
        experiment.hypothesis_history.append(old)
        amended = Hypothesis(
            statement=new_statement,
            direction=new_direction,
            horizon_days=old.horizon_days,
            version=old.version + 1,
            supersedes=old.id,
            exploratory=experiment.result is not None or bool(experiment.observations),
        )
        experiment.hypothesis = amended
        self._emit(
            "experiment_hypothesis_amended",
            experiment,
            {"supersedes": old.id, "exploratory": amended.exploratory},
        )
        return amended

    def thresholds_changed_after_launch(self, experiment: Experiment) -> bool:
        return any(
            experiment.launch_thresholds.get(m.id) != m.stop_threshold for m in experiment.metrics
        )

    # -- protocol adaptation (source §28) ----------------------------------

    def adapt_protocol(
        self,
        experiment: Experiment,
        new_description: str,
        actor_role: AuthorityRole,
        adds_new_intervention: bool = False,
    ) -> TransitionResult:
        """Versioned protocol adaptation with the source's structural bans.

        Only the bans the digest quotes verbatim from §28.2 are enforced
        here; the full five-item list awaits the source bytes (DD-017):
        - removing unfavorable days or adverse events to improve the picture
          is impossible by construction — no deletion API exists for
          ``observations`` or ``safety_events``;
        - stacking another intervention while the current one runs is
          refused ("Automatyczne dokładanie kolejnej interwencji, gdy
          pierwsza nie działa");
        - agents cannot adapt protocols at all (ADR-EXP-004).
        """
        if actor_role in _FORBIDDEN_ACTOR_ROLES:
            result = TransitionResult(
                False, experiment.state, (f"actor role {actor_role.value} may not adapt a protocol",)
            )
            self._emit("experiment_adaptation_refused", experiment, {"reasons": list(result.reasons)})
            return result
        if adds_new_intervention and experiment.state in (CycleState.ACTIVE, CycleState.HOLD):
            result = TransitionResult(
                False,
                experiment.state,
                ("banned adaptation (§28.2): adding another intervention while one is running",),
            )
            self._emit("experiment_adaptation_refused", experiment, {"reasons": list(result.reasons)})
            return result
        if experiment.state in (CycleState.COMPLETED, CycleState.STOPPED, CycleState.INCONCLUSIVE):
            return TransitionResult(
                False, experiment.state, ("cannot adapt a concluded experiment",)
            )
        old = experiment.protocol
        experiment.protocol_history.append(old)
        experiment.protocol = ExperimentProtocol(
            description=new_description,
            duration_days=old.duration_days,
            stop_rules=list(old.stop_rules),
            version=old.version + 1,
        )
        self._emit(
            "experiment_protocol_adapted",
            experiment,
            {"supersedes": old.id, "version": experiment.protocol.version},
        )
        return TransitionResult(True, experiment.state)

    # -- conclusion --------------------------------------------------------

    def conclude(
        self,
        experiment: Experiment,
        outcome: OutcomeCode,
        summary: str,
        inconclusive_reason: str | None = None,
    ) -> ExperimentResult | TransitionResult:
        """Produce the result. An inconclusive outcome is a first-class,
        honest result (source §47) — the engine applies no pressure to
        extend. Thresholds moved after launch force the exploratory flag
        (ADR-EXP-004: no rewriting success criteria after seeing results)."""
        target = (
            CycleState.INCONCLUSIVE
            if inconclusive_reason is not None
            else CycleState.COMPLETED
        )
        transition = self._transition(experiment, target, f"concluded {outcome.value}")
        if not transition.applied:
            return transition
        experiment.result = ExperimentResult(
            outcome=outcome,
            summary=summary,
            exploratory=self.thresholds_changed_after_launch(experiment),
            inconclusive_reason=inconclusive_reason,
            causal_evidence_eligible=experiment.evidence_domain is EvidenceDomain.CAUSAL,
        )
        self._emit(
            "experiment_concluded",
            experiment,
            {
                "outcome": outcome.value,
                "exploratory": experiment.result.exploratory,
                "causal_evidence_eligible": experiment.result.causal_evidence_eligible,
            },
        )
        return experiment.result


_PORTFOLIO_ACTIVE_STATES = {CycleState.BASELINE, CycleState.ACTIVE, CycleState.HOLD}


@dataclass(frozen=True)
class PortfolioDecision:
    admitted: bool
    reasons: tuple[str, ...] = ()


class ExperimentPortfolio:
    """Parallel-experiment portfolio (source §29).

    The source caps the number of simultaneously active changes but the
    digest does not carry the concrete number, so the limit is an explicit,
    mandatory constructor argument with no default (the DD-006/DD-007
    configuration-required pattern; see DD-017). Infrastructural
    experiments (§29.3 — confirmed-value routines such as a fixed sleep
    time or prescribed rehabilitation) move to maintenance and do not
    compete with active hypotheses for attention, so they never count
    against the limit. Interactions between experiments are recorded as
    declared context, never silently inferred.
    """

    def __init__(self, max_active_experiments: int) -> None:
        if max_active_experiments < 1:
            raise ValueError("max_active_experiments must be a positive, explicit limit")
        self.max_active_experiments = max_active_experiments
        self._experiments: dict[str, Experiment] = {}
        self.interactions: list[dict[str, str]] = []

    def active_count(self) -> int:
        return sum(
            1
            for e in self._experiments.values()
            if e.state in _PORTFOLIO_ACTIVE_STATES and not e.infrastructural
        )

    def admit(self, experiment: Experiment) -> PortfolioDecision:
        if experiment.id in self._experiments:
            return PortfolioDecision(False, ("experiment already in portfolio",))
        if not experiment.infrastructural and self.active_count() >= self.max_active_experiments:
            reason = (
                f"portfolio limit reached ({self.max_active_experiments} active changes); "
                "attention spread over more stops being attention (§29.1)"
            )
            return PortfolioDecision(False, (reason,))
        self._experiments[experiment.id] = experiment
        return PortfolioDecision(True)

    def declare_interaction(self, experiment_a: Experiment, experiment_b: Experiment, note: str) -> None:
        """§29.2: possible interactions are declared context for analysis,
        recorded verbatim — the portfolio never merges or reweighs results."""
        self.interactions.append(
            {"a": experiment_a.id, "b": experiment_b.id, "note": note, "at": _now()}
        )

    def experiments(self) -> list[Experiment]:
        return list(self._experiments.values())
