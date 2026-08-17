from __future__ import annotations

import json
import uuid
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from types import MappingProxyType

"""Skeleton types for Layer 5's coded scales DI, IQ and AR (DD-006).

Implements the founder resolution of DD-006 (2026-08-17): structure only.
Three things are deliberately kept apart and must never be merged:

1. **Scale structure** (`ScaleDefinition`) — the closed code lists from the
   source's Załącznik I (DI-1..DI-8, IQ0..IQ5, AR0..AR5). Structure is the
   only thing the source defines exactly, so it is the only thing encoded
   here.
2. **Measurement value** (`ScaleMeasurement`) — a declared code with its
   provenance (who declared it, on what basis). Per the source's §18.2 ban
   on false precision, a measurement is a code plus a stated basis — never
   a bare number.
3. **Interpretation policy** (`InterpretationPolicy`) — what a code means
   for downstream decisions. The source does not provide numeric
   thresholds, so none exist here: every rule arrives through an explicit,
   versioned, attributed configuration object. A missing or incomplete
   configuration yields `CONFIGURATION_REQUIRED` as a first-class outcome
   — never an exception, never a silently assumed threshold.

Numeric thresholds and per-level semantics remain a separate founder
decision requiring calibration and validation (DD-006). Test fixtures for
this module are synthetic and are marked as such — they are not
recommended values.
"""


class ScaleKind(str, Enum):
    """The three Layer 5 scales approved for skeleton implementation."""

    DECISION_INTENT = "DI"
    INPUT_QUALITY = "IQ"
    ACTION_READINESS = "AR"


@dataclass(frozen=True)
class ScaleLevel:
    """One code on a scale. Ordinal gives source ordering, not a score."""

    code: str
    ordinal: int


@dataclass(frozen=True)
class ScaleDefinition:
    """The closed, source-defined structure of one scale."""

    kind: ScaleKind
    source: str
    levels: tuple[ScaleLevel, ...]

    def codes(self) -> tuple[str, ...]:
        return tuple(level.code for level in self.levels)


def _levels(prefix: str, first: int, last: int, *, dash: bool) -> tuple[ScaleLevel, ...]:
    joiner = "-" if dash else ""
    return tuple(
        ScaleLevel(code=f"{prefix}{joiner}{value}", ordinal=value)
        for value in range(first, last + 1)
    )


# Załącznik I of the Layer 5 source ("Statusy i kody operacyjne"), via
# docs/LAYER_5_DECISION_ENGINE_DIGEST.md. Codes only — the source digest
# carries per-level semantics for the endpoints alone, so none are
# invented here.
SCALE_DEFINITIONS: Mapping[ScaleKind, ScaleDefinition] = MappingProxyType({
    ScaleKind.DECISION_INTENT: ScaleDefinition(
        kind=ScaleKind.DECISION_INTENT,
        source="Layer 5 Załącznik I: Intencja DI-1..DI-8",
        levels=_levels("DI", 1, 8, dash=True),
    ),
    ScaleKind.INPUT_QUALITY: ScaleDefinition(
        kind=ScaleKind.INPUT_QUALITY,
        source="Layer 5 Załącznik I: Jakość wejścia IQ0..IQ5",
        levels=_levels("IQ", 0, 5, dash=False),
    ),
    ScaleKind.ACTION_READINESS: ScaleDefinition(
        kind=ScaleKind.ACTION_READINESS,
        source="Layer 5 Załącznik I: Gotowość AR0..AR5",
        levels=_levels("AR", 0, 5, dash=False),
    ),
})


def _now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(frozen=True)
class ScaleMeasurement:
    """A declared code on one scale, with provenance.

    §18.2 ("Zakaz fałszywej precyzji"): a measurement names its basis and
    stays a code — it never pretends to numeric precision.
    """

    scale: ScaleKind
    code: str
    declared_by: str
    basis: str
    measurement_id: str = field(
        default_factory=lambda: "HOS-MSR-" + uuid.uuid4().hex[:12].upper(),
    )
    declared_at: str = field(default_factory=_now)

    def __post_init__(self) -> None:
        valid = SCALE_DEFINITIONS[self.scale].codes()
        if self.code not in valid:
            raise ValueError(
                f"{self.code!r} is not a code of scale {self.scale.value}"
                f" (valid: {', '.join(valid)})"
            )
        if not self.basis.strip():
            raise ValueError("a measurement requires a stated basis (§18.2)")
        if not self.declared_by.strip():
            raise ValueError("a measurement requires a declaring identity")


@dataclass(frozen=True)
class InterpretationPolicy:
    """An explicit, versioned mapping from codes to named outcomes.

    There is no default policy anywhere in the engine. Every instance must
    be constructed deliberately, carries its own version and approver, and
    covers only the codes it names — anything it does not name yields
    CONFIGURATION_REQUIRED downstream, never a guess.
    """

    policy_id: str
    version: str
    approved_by: str
    scale: ScaleKind
    rules: Mapping[str, str]

    def __post_init__(self) -> None:
        if not self.version.strip():
            raise ValueError("an interpretation policy must be versioned")
        if not self.approved_by.strip():
            raise ValueError("an interpretation policy must name its approver")
        valid = SCALE_DEFINITIONS[self.scale].codes()
        unknown = [code for code in self.rules if code not in valid]
        if unknown:
            raise ValueError(
                f"policy rules name codes outside scale {self.scale.value}:"
                f" {', '.join(sorted(unknown))}"
            )
        object.__setattr__(self, "rules", MappingProxyType(dict(self.rules)))


class InterpretationOutcomeKind(str, Enum):
    INTERPRETED = "INTERPRETED"
    CONFIGURATION_REQUIRED = "CONFIGURATION_REQUIRED"


@dataclass(frozen=True)
class InterpretationOutcome:
    """First-class result of interpreting a measurement — never an exception."""

    kind: InterpretationOutcomeKind
    measurement_id: str
    reason: str
    result: str | None = None
    policy_id: str | None = None
    policy_version: str | None = None


def load_policies_json(path: str) -> Mapping[ScaleKind, InterpretationPolicy]:
    """Build the active per-scale policies from a signed policy file.

    Reads only the ``policies`` section (the ``superseded`` history is kept
    for provenance, never loaded for use). Every entry must carry its own
    version; the approver comes from the file's top-level ``approved_by``
    field — an unattributed file refuses to load, matching the no-defaults
    rule of DD-006.
    """
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    approved_by = str(data.get("approved_by", "")).strip()
    if not approved_by:
        raise ValueError(f"policy file {path} names no approver (approved_by)")
    loaded: dict[ScaleKind, InterpretationPolicy] = {}
    for entry in data.get("policies", []):
        policy = InterpretationPolicy(
            policy_id=entry["policy_id"],
            version=entry["version"],
            approved_by=approved_by,
            scale=ScaleKind(entry["scale"]),
            rules=entry["rules"],
        )
        if policy.scale in loaded:
            raise ValueError(
                f"policy file {path} declares two active policies for scale"
                f" {policy.scale.value}"
            )
        loaded[policy.scale] = policy
    return MappingProxyType(loaded)


class ScaleInterpreter:
    """Applies an explicit policy to measurements of one scale.

    Constructed without a policy it still works — every interpretation
    then returns CONFIGURATION_REQUIRED, which is the safe refusal the
    founder resolution requires. It never falls back to built-in
    thresholds, because none exist.
    """

    def __init__(self, policy: InterpretationPolicy | None = None) -> None:
        self._policy = policy

    def interpret(self, measurement: ScaleMeasurement) -> InterpretationOutcome:
        if self._policy is None:
            return InterpretationOutcome(
                kind=InterpretationOutcomeKind.CONFIGURATION_REQUIRED,
                measurement_id=measurement.measurement_id,
                reason=(
                    "no interpretation policy configured for scale"
                    f" {measurement.scale.value}; thresholds are a founder"
                    " decision (DD-006) and are never assumed"
                ),
            )
        if self._policy.scale is not measurement.scale:
            return InterpretationOutcome(
                kind=InterpretationOutcomeKind.CONFIGURATION_REQUIRED,
                measurement_id=measurement.measurement_id,
                reason=(
                    f"configured policy {self._policy.policy_id} covers scale"
                    f" {self._policy.scale.value}, not {measurement.scale.value}"
                ),
            )
        rule = self._policy.rules.get(measurement.code)
        if rule is None:
            return InterpretationOutcome(
                kind=InterpretationOutcomeKind.CONFIGURATION_REQUIRED,
                measurement_id=measurement.measurement_id,
                reason=(
                    f"policy {self._policy.policy_id} v{self._policy.version}"
                    f" has no rule for {measurement.code}; missing rules are"
                    " never guessed"
                ),
                policy_id=self._policy.policy_id,
                policy_version=self._policy.version,
            )
        return InterpretationOutcome(
            kind=InterpretationOutcomeKind.INTERPRETED,
            measurement_id=measurement.measurement_id,
            reason=f"rule from policy {self._policy.policy_id} v{self._policy.version}",
            result=rule,
            policy_id=self._policy.policy_id,
            policy_version=self._policy.version,
        )
