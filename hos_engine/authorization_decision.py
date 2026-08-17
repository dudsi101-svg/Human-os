"""Unified authorization decision — composition skeleton (audit §12–13).

Nine mechanisms currently answer fragments of "may this operation run?"
(identity, authority role, role grant, capability, call rule, consent,
security gateway, approval, proof kernel). This module adds the single
composition point the audit calls for, without reimplementing any of
them: callers register named aspect checks (thin closures over the real
registries/gates) and an explicit, mandatory set of required aspects.

Binding rules (docs/authorization-decision-contract.md):
- deny-first: one failed aspect denies the whole decision; aspects never
  compensate each other;
- absence of evaluation is never consent: a required aspect with no
  registered check denies with ``NOT_EVALUATED:<aspect>``;
- ``required_aspects`` is an explicit constructor argument with no
  default (the DD-006/DD-007 configuration-required pattern);
- the decision is a receipt: it echoes WHO / BY WHAT AUTHORITY / ON WHAT /
  WHAT ACTION / WHY / UNDER WHAT CONSENT / UNDER WHAT POLICY plus every
  aspect result and reason.

Source-model debt stays named, not hidden: ``resource_selector``,
``purpose`` and policy versions are carried as declared inputs and echoed
in the receipt; mechanisms enforcing them do not exist yet (see
``artifact.registry.json`` -> authorization.open_gaps).
"""

from __future__ import annotations

import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum


def _now() -> str:
    return datetime.now(UTC).isoformat()


class AuthorizationAction(str, Enum):
    READ = "READ"
    WRITE = "WRITE"
    EXECUTE = "EXECUTE"
    DELEGATE = "DELEGATE"


@dataclass(frozen=True)
class AuthorizationRequest:
    """Declared inputs for one authorization question."""

    identity_id: str
    identity_kind: str
    authority_role: str
    resource_selector: str
    action: AuthorizationAction
    purpose: str
    consent_refs: tuple[str, ...] = ()
    policy_version: str = ""
    constraints: tuple[str, ...] = ()


@dataclass(frozen=True)
class AspectResult:
    aspect: str
    passed: bool
    reason: str


@dataclass(frozen=True)
class AuthorizationDecision:
    """The composed, receipt-grade answer."""

    allowed: bool
    request: AuthorizationRequest
    aspect_results: tuple[AspectResult, ...]
    reasons: tuple[str, ...]
    decision_id: str = field(
        default_factory=lambda: f"HOS-AUZ-{uuid.uuid4().hex[:12].upper()}"
    )
    decided_at: str = field(default_factory=_now)


AspectCheck = Callable[[AuthorizationRequest], AspectResult]


class AuthorizationComposer:
    """Composes registered aspect checks into one AuthorizationDecision.

    The composer owns no rules of its own. Each check is a thin closure
    over an existing mechanism (RoleGrantRegistry, CallAuthorizer,
    ConsentRegistry, SecurityGateway, Proof Kernel, ...). There is no
    default for ``required_aspects`` and no bypass path.
    """

    def __init__(self, required_aspects: set[str]) -> None:
        if not required_aspects:
            raise ValueError(
                "required_aspects must be an explicit, non-empty set - "
                "an empty requirement would make absence of evaluation look like consent"
            )
        self.required_aspects = frozenset(required_aspects)
        self._checks: dict[str, AspectCheck] = {}

    def register(self, aspect: str, check: AspectCheck) -> None:
        if aspect in self._checks:
            raise ValueError(f"aspect {aspect!r} already registered - replacing checks silently is not allowed")
        self._checks[aspect] = check

    def decide(self, request: AuthorizationRequest) -> AuthorizationDecision:
        results: list[AspectResult] = []
        reasons: list[str] = []

        # Absence of evaluation is never consent.
        for aspect in sorted(self.required_aspects):
            if aspect not in self._checks:
                results.append(
                    AspectResult(aspect, False, f"NOT_EVALUATED:{aspect} - no check registered")
                )
                reasons.append(f"NOT_EVALUATED:{aspect}")

        for aspect, check in self._checks.items():
            result = check(request)
            results.append(result)
            if not result.passed:
                reasons.append(f"{aspect}: {result.reason}")

        allowed = not reasons
        return AuthorizationDecision(
            allowed=allowed,
            request=request,
            aspect_results=tuple(results),
            reasons=tuple(reasons),
        )
