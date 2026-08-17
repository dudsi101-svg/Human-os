from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum

from .authority import AuthorityRole
from .event_store import EventStore
from .sqlite_store import SQLiteEventStore

"""Skeleton of the Emergency Root key infrastructure (DD-007).

Implements the founder resolution of DD-007 (2026-08-17). This is the
missing piece named by ADR-RECOVERY-003: the dual-key sovereignty story
needs real key infrastructure — but the source provides no TTL values,
no authentication-strength requirement and no threshold scheme, so this
module encodes the *shape* of that infrastructure and refuses to invent
its numbers:

- `EmergencyRootPolicy` is the versioned configuration. Every parameter
  is keyword-only with **no default**: TTL, required authentication
  strength, the k-of-n threshold scheme, custodian roles, scope, and the
  configuration's own id/version/approver all must be stated explicitly.
  There is no built-in "2-of-3" anywhere.
- `EmergencyRootKernel` cannot exist without a policy — the constructor
  requires one, so "missing configuration blocks the mechanism" is a
  structural guarantee, not a runtime check.
- Every activation request, custodian approval, refusal, use and expiry
  is recorded in an append-only audit trail the kernel exposes no API to
  mutate, and optionally in a durable event store (as `STATE_OBSERVED`
  usage records, matching DD-003's convention for non-activation
  records).
- Refusal is an exception (`EmergencyRootRefused`), matching
  `recovery.py`'s convention: ignoring a refused protection must not
  look like having it.

Deliberately NOT here (per the founder resolution): real key material,
key storage, threshold cryptography, and authentication verification.
The descriptor's `authentication_strength` and approvals are *declared
inputs*, checked against the policy's declaration — a reference
mechanism sharing security/THREAT_MODEL.md's stated limitation. Building
the real thing requires a separate founder decision plus a deployment
threat model. Test values are synthetic fixtures and must never be
promoted to production configuration.
"""


class EmergencyRootRefused(Exception):
    """A refused Emergency Root operation. The refusal itself is logged."""


_EXCLUDED_ROLES = frozenset({
    AuthorityRole.AGENT,
    AuthorityRole.SERVICE,
    AuthorityRole.SYSTEM_PROCESS,
})


def _now() -> datetime:
    return datetime.now(UTC)


@dataclass(frozen=True)
class EmergencyKeyDescriptor:
    """Describes an emergency key without holding any key material."""

    key_id: str
    holder_identity_id: str
    holder_role: AuthorityRole
    authentication_strength: str
    registered_at: str = field(default_factory=lambda: _now().isoformat())

    def __post_init__(self) -> None:
        if not self.key_id.strip():
            raise ValueError("a key descriptor requires a key_id")
        if not self.holder_identity_id.strip():
            raise ValueError("a key descriptor requires a holder identity")
        if not self.authentication_strength.strip():
            raise ValueError(
                "a key descriptor requires a declared authentication strength"
            )


@dataclass(frozen=True)
class EmergencyRootPolicy:
    """The versioned Emergency Root configuration. No parameter has a
    default — every value is an explicit founder decision."""

    config_id: str
    version: str
    approved_by: str
    scope: str
    ttl_seconds: int
    required_authentication_strength: str
    required_approvals_k: int
    total_custodians_n: int
    custodian_roles: frozenset[AuthorityRole]

    def __post_init__(self) -> None:
        for name in ("config_id", "version", "approved_by", "scope",
                     "required_authentication_strength"):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"policy field {name} must be explicitly set")
        if self.ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be a positive, explicit value")
        if self.required_approvals_k < 1:
            raise ValueError("required_approvals_k must be at least 1")
        if self.total_custodians_n < self.required_approvals_k:
            raise ValueError(
                "total_custodians_n must be >= required_approvals_k"
                " (a k-of-n scheme needs n >= k)"
            )
        if not self.custodian_roles:
            raise ValueError("custodian_roles must name at least one role")
        forbidden = self.custodian_roles & _EXCLUDED_ROLES
        if forbidden:
            raise ValueError(
                "agents, services and system processes can never be"
                f" custodians: {sorted(role.value for role in forbidden)}"
            )


class AuditKind(str, Enum):
    KEY_REGISTERED = "KEY_REGISTERED"
    ACTIVATION_REQUESTED = "ACTIVATION_REQUESTED"
    APPROVAL_RECORDED = "APPROVAL_RECORDED"
    ACTIVATED = "ACTIVATED"
    REFUSED = "REFUSED"
    USED = "USED"
    EXPIRED = "EXPIRED"


@dataclass(frozen=True)
class EmergencyRootAuditRecord:
    record_id: str
    kind: AuditKind
    occurred_at: str
    actor_id: str
    request_id: str | None
    key_id: str | None
    policy_config_id: str
    policy_version: str
    detail: str


class RequestState(str, Enum):
    PENDING = "PENDING"
    ACTIVATED = "ACTIVATED"
    USED = "USED"
    EXPIRED = "EXPIRED"


@dataclass
class _ActivationRequest:
    request_id: str
    requested_by: str
    reason: str
    requested_at: datetime
    expires_at: datetime
    state: RequestState
    approvals: dict[str, str]  # key_id -> holder_identity_id


class EmergencyRootKernel:
    """Reference k-of-n approval flow over declared inputs.

    Construction without a policy is impossible by design — that is the
    "missing configuration blocks the mechanism" guarantee. The kernel
    exposes no API to alter its policy or its audit trail.
    """

    def __init__(
        self,
        *,
        policy: EmergencyRootPolicy,
        event_store: EventStore | SQLiteEventStore | None = None,
    ) -> None:
        if not isinstance(policy, EmergencyRootPolicy):
            raise TypeError(
                "EmergencyRootKernel requires an explicit EmergencyRootPolicy"
            )
        self._policy = policy
        self._event_store = event_store
        self._keys: dict[str, EmergencyKeyDescriptor] = {}
        self._requests: dict[str, _ActivationRequest] = {}
        self._audit: list[EmergencyRootAuditRecord] = []

    @property
    def policy(self) -> EmergencyRootPolicy:
        return self._policy

    def audit_trail(self) -> tuple[EmergencyRootAuditRecord, ...]:
        return tuple(self._audit)

    # -- key registration ------------------------------------------------

    def register_key(self, descriptor: EmergencyKeyDescriptor) -> None:
        if descriptor.holder_role not in self._policy.custodian_roles:
            self._refuse(
                actor_id=descriptor.holder_identity_id,
                key_id=descriptor.key_id,
                detail=(
                    f"role {descriptor.holder_role.value} is not among the"
                    " policy's custodian roles"
                ),
            )
        if descriptor.authentication_strength != (
            self._policy.required_authentication_strength
        ):
            self._refuse(
                actor_id=descriptor.holder_identity_id,
                key_id=descriptor.key_id,
                detail=(
                    "declared authentication strength"
                    f" {descriptor.authentication_strength!r} does not match"
                    " the policy's required declaration"
                ),
            )
        if len(self._keys) >= self._policy.total_custodians_n:
            self._refuse(
                actor_id=descriptor.holder_identity_id,
                key_id=descriptor.key_id,
                detail=(
                    f"policy admits {self._policy.total_custodians_n}"
                    " custodian keys; registry is full"
                ),
            )
        if any(
            existing.holder_identity_id == descriptor.holder_identity_id
            for existing in self._keys.values()
        ):
            self._refuse(
                actor_id=descriptor.holder_identity_id,
                key_id=descriptor.key_id,
                detail="each custodian identity may hold exactly one key",
            )
        self._keys[descriptor.key_id] = descriptor
        self._record(
            kind=AuditKind.KEY_REGISTERED,
            actor_id=descriptor.holder_identity_id,
            request_id=None,
            key_id=descriptor.key_id,
            detail=f"key registered for role {descriptor.holder_role.value}",
        )

    # -- activation flow -------------------------------------------------

    def request_activation(self, *, requested_by: str, reason: str) -> str:
        if not reason.strip():
            self._refuse(
                actor_id=requested_by, key_id=None,
                detail="an activation request requires a stated reason",
            )
        now = _now()
        request = _ActivationRequest(
            request_id="HOS-ERQ-" + uuid.uuid4().hex[:12].upper(),
            requested_by=requested_by,
            reason=reason,
            requested_at=now,
            expires_at=now.replace(microsecond=0).fromtimestamp(
                now.timestamp() + self._policy.ttl_seconds, tz=UTC,
            ),
            state=RequestState.PENDING,
            approvals={},
        )
        self._requests[request.request_id] = request
        self._record(
            kind=AuditKind.ACTIVATION_REQUESTED,
            actor_id=requested_by,
            request_id=request.request_id,
            key_id=None,
            detail=reason,
        )
        return request.request_id

    def approve(self, request_id: str, *, key_id: str) -> RequestState:
        request = self._requests[request_id]
        self._expire_if_due(request)
        if request.state is RequestState.EXPIRED:
            self._refuse(
                actor_id=key_id, request_id=request_id, key_id=key_id,
                detail="request expired before approval (TTL elapsed)",
            )
        if request.state is not RequestState.PENDING:
            self._refuse(
                actor_id=key_id, request_id=request_id, key_id=key_id,
                detail=f"request is {request.state.value}, not PENDING",
            )
        descriptor = self._keys.get(key_id)
        if descriptor is None:
            self._refuse(
                actor_id=key_id, request_id=request_id, key_id=key_id,
                detail="unknown key",
            )
        assert descriptor is not None
        if key_id in request.approvals:
            self._refuse(
                actor_id=descriptor.holder_identity_id,
                request_id=request_id, key_id=key_id,
                detail="duplicate approval from the same key",
            )
        if descriptor.holder_identity_id in request.approvals.values():
            self._refuse(
                actor_id=descriptor.holder_identity_id,
                request_id=request_id, key_id=key_id,
                detail="duplicate approval from the same custodian identity",
            )
        request.approvals[key_id] = descriptor.holder_identity_id
        self._record(
            kind=AuditKind.APPROVAL_RECORDED,
            actor_id=descriptor.holder_identity_id,
            request_id=request_id,
            key_id=key_id,
            detail=(
                f"{len(request.approvals)}"
                f"/{self._policy.required_approvals_k} approvals"
            ),
        )
        if len(request.approvals) >= self._policy.required_approvals_k:
            request.state = RequestState.ACTIVATED
            self._record(
                kind=AuditKind.ACTIVATED,
                actor_id=descriptor.holder_identity_id,
                request_id=request_id,
                key_id=key_id,
                detail=(
                    f"k-of-n satisfied ({self._policy.required_approvals_k}"
                    f"-of-{self._policy.total_custodians_n})"
                ),
            )
        return request.state

    def use(self, request_id: str, *, used_by: str, action: str) -> None:
        request = self._requests[request_id]
        self._expire_if_due(request)
        if request.state is not RequestState.ACTIVATED:
            self._refuse(
                actor_id=used_by, request_id=request_id, key_id=None,
                detail=(
                    f"request is {request.state.value}; only an ACTIVATED,"
                    " unexpired request may be used"
                ),
            )
        request.state = RequestState.USED
        self._record(
            kind=AuditKind.USED,
            actor_id=used_by,
            request_id=request_id,
            key_id=None,
            detail=action,
        )

    # -- internals -------------------------------------------------------

    def _expire_if_due(self, request: _ActivationRequest) -> None:
        if (
            request.state in (RequestState.PENDING, RequestState.ACTIVATED)
            and _now() >= request.expires_at
        ):
            request.state = RequestState.EXPIRED
            self._record(
                kind=AuditKind.EXPIRED,
                actor_id=request.requested_by,
                request_id=request.request_id,
                key_id=None,
                detail=f"TTL of {self._policy.ttl_seconds}s elapsed",
            )

    def _refuse(
        self,
        *,
        actor_id: str,
        detail: str,
        request_id: str | None = None,
        key_id: str | None = None,
    ) -> None:
        self._record(
            kind=AuditKind.REFUSED,
            actor_id=actor_id,
            request_id=request_id,
            key_id=key_id,
            detail=detail,
        )
        raise EmergencyRootRefused(detail)

    def _record(
        self,
        *,
        kind: AuditKind,
        actor_id: str,
        request_id: str | None,
        key_id: str | None,
        detail: str,
    ) -> None:
        record = EmergencyRootAuditRecord(
            record_id="HOS-ERA-" + uuid.uuid4().hex[:12].upper(),
            kind=kind,
            occurred_at=_now().isoformat(),
            actor_id=actor_id,
            request_id=request_id,
            key_id=key_id,
            policy_config_id=self._policy.config_id,
            policy_version=self._policy.version,
            detail=detail,
        )
        self._audit.append(record)
        if self._event_store is not None:
            # Emergency Root records are usage/infrastructure records, not
            # mode activations — per DD-003's mapping they stay
            # STATE_OBSERVED with the full record in the payload.
            self._event_store.append({
                "id": record.record_id,
                "event_type": "STATE_OBSERVED",
                "occurred_at": record.occurred_at,
                "actor_id": actor_id,
                "subject_ids": [],
                "payload": {
                    "kind": record.kind.value,
                    "request_id": request_id,
                    "key_id": key_id,
                    "policy_config_id": record.policy_config_id,
                    "policy_version": record.policy_version,
                    "detail": detail,
                },
                "correlation_id": request_id or record.record_id,
                "immutable": True,
            })
