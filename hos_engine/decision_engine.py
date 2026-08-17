from __future__ import annotations

import uuid
from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from enum import Enum

from .decision_scales import (
    InterpretationOutcome,
    InterpretationOutcomeKind,
    ScaleInterpreter,
    ScaleKind,
    ScaleMeasurement,
)

"""First MVP slice of Layer 5, the Decision & Recommendation Engine.

Implements the load-bearing subset of ADR-DECISION-001..005: the nine hard
gates G0-G8 evaluated before any ranking, non-commutability (a ranking can
never resurrect a gate-excluded candidate), abstention and escalation as
first-class outcomes rather than errors, the rule that user determination
never lowers the safety floor, and the ban on financial incentive touching
the ranking.

Like the Proof Kernel, this engine evaluates *declared* inputs -- it cannot
verify whether declarations are honest. It is a bounded slice: intent
classes DI-1..8, input-quality IQ0-IQ5, readiness AR0-AR5, the ten-axis
decision profile of Layer 5 SS18, and integration with the Knowledge Map's
E0-E5 readiness scale are not implemented yet. Evidence strength is
declared as an integer 0-5 matching Layer 3's descriptive signature scale
(ADR-KNOWLEDGE-001) by convention only -- no live Knowledge Map lookup
happens here.
"""


class DecisionGate(str, Enum):
    """The nine hard gates from Layer 5 SS11.1 (ADR-DECISION-001)."""

    G0_LEGALITY_CONSTITUTION = "G0_LEGALITY_CONSTITUTION"
    G1_CONSENT = "G1_CONSENT"
    G2_GOAL_IDENTITY = "G2_GOAL_IDENTITY"
    G3_ACUTE_RISK = "G3_ACUTE_RISK"
    G4_CONTRAINDICATIONS = "G4_CONTRAINDICATIONS"
    G5_EVIDENCE_THRESHOLD = "G5_EVIDENCE_THRESHOLD"
    G6_SAFE_FEASIBILITY = "G6_SAFE_FEASIBILITY"
    G7_MONITORABILITY = "G7_MONITORABILITY"
    G8_THIRD_PARTY_IMPACT = "G8_THIRD_PARTY_IMPACT"


class RiskReactionClass(str, Enum):
    """Layer 5 SS12.2's word-coded risk-reaction classes. Deliberately not
    the Constitution's R0-R4 and not Layer 6's SE0-SE4 -- see
    ADR-DECISION-001's naming note before conflating any of them."""

    NISKIE = "R-NISKIE"
    UMIARKOWANE = "R-UMIARKOWANE"
    PODWYZSZONE = "R-PODWYZSZONE"
    WYSOKIE = "R-WYSOKIE"
    KRYTYCZNE = "R-KRYTYCZNE"


# The evidence-asymmetry principle (Layer 3 SS17.2 via ADR-KNOWLEDGE-001):
# the riskier the candidate, the stronger its declared evidence must be.
# Thresholds are normative design assumptions, not empirical truth.
MINIMUM_EVIDENCE_FOR_RISK: dict[RiskReactionClass, int] = {
    RiskReactionClass.NISKIE: 1,
    RiskReactionClass.UMIARKOWANE: 2,
    RiskReactionClass.PODWYZSZONE: 3,
    RiskReactionClass.WYSOKIE: 4,
    RiskReactionClass.KRYTYCZNE: 6,  # unreachable on the 0-5 scale: never admissible
}

_RISK_ORDER = [
    RiskReactionClass.NISKIE,
    RiskReactionClass.UMIARKOWANE,
    RiskReactionClass.PODWYZSZONE,
    RiskReactionClass.WYSOKIE,
    RiskReactionClass.KRYTYCZNE,
]


class RecommendationClass(str, Enum):
    """Layer 5 SS24.1's RC0-RC6 (subset relevant to this slice)."""

    RC0_NO_RECOMMENDATION = "RC0"
    RC3_SIMPLE_LOW_RISK_STEP = "RC3"
    RC5_CONDITIONAL = "RC5"
    RC6_ESCALATION_OR_SAFE_REFUSAL = "RC6"


class EscalationType(str, Enum):
    """Layer 5 SS27.3's graduated escalation."""

    SOFT = "SOFT"
    CONDITIONAL = "CONDITIONAL"
    HARD = "HARD"


class AbstentionReason(str, Enum):
    """The eight named abstention reasons from Layer 5 SS27.1
    (ADR-DECISION-003)."""

    NO_CLEAR_GOAL = "NO_CLEAR_GOAL"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    VALUE_CONFLICT = "VALUE_CONFLICT"
    CONTRADICTORY_EVIDENCE = "CONTRADICTORY_EVIDENCE"
    NOT_MONITORABLE = "NOT_MONITORABLE"
    EXCESSIVE_RISK = "EXCESSIVE_RISK"
    BEYOND_COMPETENCE = "BEYOND_COMPETENCE"
    SUSPECTED_CRISIS = "SUSPECTED_CRISIS"


class DecisionOutcomeKind(str, Enum):
    RECOMMENDATION = "RECOMMENDATION"
    ABSTENTION = "ABSTENTION"
    ESCALATION = "ESCALATION"


@dataclass(frozen=True)
class Goal:
    owner_id: str
    outcome: str
    horizon: str
    success_criterion: str


@dataclass(frozen=True)
class DecisionCandidate:
    """A possible action, declared by the caller. Per ADR-DECISION-002 no
    field here is a verdict about the person -- every field describes the
    candidate action itself."""

    candidate_id: str
    description: str
    source: str
    risk_class: RiskReactionClass
    evidence_level: int  # 0-5, Layer 3's descriptive signature scale
    lawful: bool = True
    contraindicated: bool = False
    monitorable: bool = True
    harms_third_parties: bool = False
    feasible: bool = True
    burden: int = 0  # relative effort/cost, lower is lighter
    sponsored: bool = False  # never touches ranking (ADR-DECISION-005)

    def __post_init__(self) -> None:
        # The evidence-asymmetry gate and the "R-KRYTYCZNE never admissible"
        # guarantee both rest on evidence_level living on Layer 3's 0-5
        # scale. Enforce it here so an out-of-range value (e.g. 6) cannot
        # clear a threshold it was never meant to reach.
        if not 0 <= self.evidence_level <= 5:
            raise ValueError(
                f"evidence_level must be on the 0-5 scale, got {self.evidence_level}"
            )


@dataclass(frozen=True)
class DecisionRequest:
    request_id: str
    owner_id: str
    content: str
    domain: str
    goal: Goal | None
    candidates: tuple[DecisionCandidate, ...]
    consent_granted: bool = True
    red_flags: tuple[str, ...] = ()
    user_determination: bool = False  # must never lower any gate (ADR-DECISION-005)
    # Declared DI/IQ/AR measurements. Shadow-phase only (policy file mode
    # "SHADOW"): they are interpreted and reported, never acted on.
    measurements: tuple[ScaleMeasurement, ...] = ()


@dataclass(frozen=True)
class GateResult:
    gate: DecisionGate
    candidate_id: str | None
    passed: bool
    reason: str


@dataclass(frozen=True)
class DecisionOutcome:
    outcome_id: str
    request_id: str
    kind: DecisionOutcomeKind
    recommendation_class: RecommendationClass
    chosen: DecisionCandidate | None = None
    alternatives: tuple[DecisionCandidate, ...] = ()
    abstention_reason: AbstentionReason | None = None
    escalation: EscalationType | None = None
    reason: str = ""
    gate_results: tuple[GateResult, ...] = ()
    excluded: tuple[str, ...] = field(default_factory=tuple)
    # Shadow-phase DI/IQ/AR readings. Purely observational: attached after
    # the decision is fully computed, so they cannot have influenced it.
    shadow_interpretations: tuple[InterpretationOutcome, ...] = ()


def _new_id(prefix: str) -> str:
    return f"HOS-{prefix}-{uuid.uuid4().hex[:12].upper()}"


class DecisionEngine:
    """Walks a DecisionRequest through request-level gates, then per-candidate
    gates, then a transparent ordinal ranking of what survives.

    Non-commutability (Layer 5 SS3.1): a candidate excluded by any hard gate
    is out for good -- nothing in the ranking stage can readmit it. The
    ranking key is (risk ascending, evidence descending, burden ascending);
    `sponsored` is deliberately absent from that key.

    Shadow-phase scales: `shadow_interpreters` optionally maps a ScaleKind
    to a ScaleInterpreter carrying a signed policy (see
    policies/scale.interpretation.policies.json, mode "SHADOW"). Declared
    measurements on the request are interpreted only *after* the decision
    is fully computed and attached to the outcome for the record -- by
    construction they cannot change gates, ranking or outcome kind.
    Promotion from shadow to operational mode is a separate founder
    decision (DD-006), not a code path that exists here.
    """

    def __init__(
        self,
        shadow_interpreters: Mapping[ScaleKind, ScaleInterpreter] | None = None,
    ) -> None:
        self._shadow_interpreters = dict(shadow_interpreters or {})

    def decide(self, request: DecisionRequest) -> DecisionOutcome:
        outcome = self._decide(request)
        if not request.measurements:
            return outcome
        return replace(
            outcome,
            shadow_interpretations=tuple(
                self._interpret_shadow(m) for m in request.measurements
            ),
        )

    def _interpret_shadow(self, measurement: ScaleMeasurement) -> InterpretationOutcome:
        interpreter = self._shadow_interpreters.get(measurement.scale)
        if interpreter is None:
            return InterpretationOutcome(
                kind=InterpretationOutcomeKind.CONFIGURATION_REQUIRED,
                measurement_id=measurement.measurement_id,
                reason=(
                    "no shadow interpreter configured for scale"
                    f" {measurement.scale.value}; readings are never guessed"
                ),
            )
        return interpreter.interpret(measurement)

    def _decide(self, request: DecisionRequest) -> DecisionOutcome:
        gate_results: list[GateResult] = []

        # Request-level gates -- checked before any candidate is looked at.
        if request.red_flags:
            gate_results.append(GateResult(
                DecisionGate.G3_ACUTE_RISK, None, False,
                f"Red flags declared: {', '.join(request.red_flags)}",
            ))
            return DecisionOutcome(
                outcome_id=_new_id("DEC"),
                request_id=request.request_id,
                kind=DecisionOutcomeKind.ESCALATION,
                recommendation_class=RecommendationClass.RC6_ESCALATION_OR_SAFE_REFUSAL,
                escalation=EscalationType.HARD,
                abstention_reason=AbstentionReason.SUSPECTED_CRISIS,
                reason="Acute risk declared; the engine stops and directs to help.",
                gate_results=tuple(gate_results),
            )

        if not request.consent_granted:
            gate_results.append(GateResult(
                DecisionGate.G1_CONSENT, None, False,
                "Consent not granted for this decision process.",
            ))
            return self._abstain(
                request, AbstentionReason.INSUFFICIENT_DATA,
                "No consent; the process stops before candidate evaluation.",
                gate_results,
            )

        if request.goal is None or request.goal.owner_id != request.owner_id:
            gate_results.append(GateResult(
                DecisionGate.G2_GOAL_IDENTITY, None, False,
                "Goal is missing or not owned by the requester.",
            ))
            return self._abstain(
                request, AbstentionReason.NO_CLEAR_GOAL,
                "No clear, owned goal; a recommendation cannot be published.",
                gate_results,
            )

        # Per-candidate hard gates.
        admissible: list[DecisionCandidate] = []
        excluded: list[str] = []
        for candidate in request.candidates:
            failure = self._first_gate_failure(candidate)
            if failure is None:
                admissible.append(candidate)
                continue
            gate_results.append(failure)
            excluded.append(candidate.candidate_id)

        if not admissible:
            reason = AbstentionReason.EXCESSIVE_RISK if excluded else AbstentionReason.INSUFFICIENT_DATA
            return self._abstain(
                request, reason,
                "No candidate survived the hard gates."
                if excluded else "No candidates were provided.",
                gate_results, excluded,
            )

        # Ranking -- only over survivors, sponsorship deliberately ignored.
        ranked = sorted(
            admissible,
            key=lambda c: (_RISK_ORDER.index(c.risk_class), -c.evidence_level, c.burden),
        )
        chosen = ranked[0]

        if chosen.risk_class in {RiskReactionClass.PODWYZSZONE, RiskReactionClass.WYSOKIE}:
            return DecisionOutcome(
                outcome_id=_new_id("DEC"),
                request_id=request.request_id,
                kind=DecisionOutcomeKind.RECOMMENDATION,
                recommendation_class=RecommendationClass.RC5_CONDITIONAL,
                chosen=chosen,
                alternatives=tuple(ranked[1:]),
                escalation=EscalationType.CONDITIONAL,
                reason="Best admissible candidate carries elevated risk; "
                       "conditional on consultation/monitoring per SS27.3.",
                gate_results=tuple(gate_results),
                excluded=tuple(excluded),
            )

        return DecisionOutcome(
            outcome_id=_new_id("DEC"),
            request_id=request.request_id,
            kind=DecisionOutcomeKind.RECOMMENDATION,
            recommendation_class=RecommendationClass.RC3_SIMPLE_LOW_RISK_STEP,
            chosen=chosen,
            alternatives=tuple(ranked[1:]),
            reason="Lowest-risk, best-evidenced admissible candidate.",
            gate_results=tuple(gate_results),
            excluded=tuple(excluded),
        )

    def _first_gate_failure(self, candidate: DecisionCandidate) -> GateResult | None:
        cid = candidate.candidate_id
        if not candidate.lawful:
            return GateResult(DecisionGate.G0_LEGALITY_CONSTITUTION, cid, False,
                              "Candidate declared unlawful or constitutionally barred.")
        if candidate.contraindicated:
            return GateResult(DecisionGate.G4_CONTRAINDICATIONS, cid, False,
                              "Declared contraindication excludes the candidate.")
        # ADR-DECISION-005: R-KRYTYCZNE is never admissible, unconditionally.
        # Stated as its own gate rather than left to depend on the
        # evidence-threshold arithmetic (defence in depth).
        if candidate.risk_class == RiskReactionClass.KRYTYCZNE:
            return GateResult(
                DecisionGate.G5_EVIDENCE_THRESHOLD, cid, False,
                "R-KRYTYCZNE candidates are never admissible (ADR-DECISION-005).",
            )
        required = MINIMUM_EVIDENCE_FOR_RISK[candidate.risk_class]
        if candidate.evidence_level < required:
            return GateResult(
                DecisionGate.G5_EVIDENCE_THRESHOLD, cid, False,
                f"Evidence {candidate.evidence_level} below the {required} required "
                f"for {candidate.risk_class.value} (evidence-asymmetry principle).",
            )
        if not candidate.feasible:
            return GateResult(DecisionGate.G6_SAFE_FEASIBILITY, cid, False,
                              "Candidate not safely executable with declared resources.")
        if not candidate.monitorable:
            return GateResult(DecisionGate.G7_MONITORABILITY, cid, False,
                              "Deterioration could not be detected; protocol barred.")
        if candidate.harms_third_parties:
            return GateResult(DecisionGate.G8_THIRD_PARTY_IMPACT, cid, False,
                              "Declared harm to third parties excludes the candidate.")
        return None

    def _abstain(
        self,
        request: DecisionRequest,
        reason: AbstentionReason,
        text: str,
        gate_results: list[GateResult],
        excluded: list[str] | None = None,
    ) -> DecisionOutcome:
        return DecisionOutcome(
            outcome_id=_new_id("DEC"),
            request_id=request.request_id,
            kind=DecisionOutcomeKind.ABSTENTION,
            recommendation_class=RecommendationClass.RC0_NO_RECOMMENDATION,
            abstention_reason=reason,
            reason=text,
            gate_results=tuple(gate_results),
            excluded=tuple(excluded or []),
        )
