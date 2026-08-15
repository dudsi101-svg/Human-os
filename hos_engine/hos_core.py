from __future__ import annotations

import uuid
from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from enum import Enum
from types import MappingProxyType
from typing import Any


class ExecutionStatus(str, Enum):
    PROPOSED = "PROPOSED"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ABORTED = "ABORTED"


@dataclass(frozen=True)
class ContextPackage:
    """A single versioned context snapshot.

    `data` is a true read-only view (types.MappingProxyType), not just a
    plain dict behind a frozen dataclass -- mutating the dict passed into
    ContextManager.snapshot() after the call, or writing to `.data[...]`
    directly, cannot alter a package already handed out. This was corrected
    on 2026-08-15 (source-integrity correction pass) after review found the
    original implementation claimed immutability while actually storing a
    mutable dict.
    """

    context_id: str
    subject_id: str
    version: int
    data: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class ContextManager:
    """Builds and versions the context package an execution runs against.

    First slice of HOS Core (ADR-CORE-001, Rozszerzenie Architektury v0.2 §2).
    Each snapshot is immutable and additive; nothing is overwritten in place.
    """

    def __init__(self) -> None:
        self._history: dict[str, list[ContextPackage]] = {}

    def snapshot(self, subject_id: str, data: Mapping[str, Any]) -> ContextPackage:
        history = self._history.setdefault(subject_id, [])
        package = ContextPackage(
            context_id="HOS-CTX-" + uuid.uuid4().hex[:12].upper(),
            subject_id=subject_id,
            version=len(history) + 1,
            data=MappingProxyType(dict(data)),
        )
        history.append(package)
        return package

    def latest(self, subject_id: str) -> ContextPackage | None:
        history = self._history.get(subject_id)
        return history[-1] if history else None

    def history(self, subject_id: str) -> list[ContextPackage]:
        return list(self._history.get(subject_id, []))


@dataclass(frozen=True)
class ExecutionContract:
    """The minimum execution contract from ADR-CORE-001.

    `required_permissions` is a flat tuple of permission strings. This is a
    TEMPORARY MVP REFERENCE MECHANISM ONLY, not the canonical permission
    model -- the Identity, Authority & Permissions specification defines a
    much richer Permission Grant (subject, role, resource selector, action,
    purpose, scope, constraints, issuer, validity, approval policy,
    revocation, audit reference, policy version). Do not spread this
    placeholder shape into new modules; replace it here once the formal
    Permission Grant is implemented.
    """

    execution_id: str
    correlation_id: str
    goal: str
    owner_id: str
    context: ContextPackage
    required_permissions: tuple[str, ...] = ()
    budget: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    abort_criteria: tuple[str, ...] = ()
    status: ExecutionStatus = ExecutionStatus.PROPOSED


@dataclass(frozen=True)
class ExecutionEvent:
    event_id: str
    execution_id: str
    event_type: str
    occurred_at: str
    payload: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))


_TERMINAL_STATUSES = frozenset(
    {ExecutionStatus.COMPLETED, ExecutionStatus.FAILED, ExecutionStatus.ABORTED}
)


class EventEngine:
    """Opens execution contracts and logs their lifecycle as an immutable event trail.

    First slice of HOS Core (ADR-CORE-001, Rozszerzenie Architektury v0.2 §2).

    Event-truth boundary (corrected 2026-08-15, source-integrity correction
    pass): Human OS now has three event-shaped things and they must not be
    treated as interchangeable or allowed to drift into separate truths:

    - `EventEngine` (this class) is an execution-lifecycle PRODUCER/COORDINATOR.
      It tracks one ExecutionContract from proposal through a terminal status
      and is deliberately in-memory and process-local -- it is not durable
      storage and does not survive a restart.
    - `hos_engine.event_store.EventStore` / `SQLiteEventStore` is the
      CANONICAL PERSISTENCE interface for durable domain events (including,
      eventually, execution-lifecycle events emitted here). SQLiteEventStore
      additionally provides hash-chain integrity verification.

    Any future integration should have EventEngine call into an EventStore
    (or a shared event-ledger port) to persist lifecycle events, rather than
    each new module growing its own independent notion of "the" event log.
    """

    def __init__(self) -> None:
        self._contracts: dict[str, ExecutionContract] = {}
        self._log: dict[str, list[ExecutionEvent]] = {}

    def open(
        self,
        *,
        goal: str,
        owner_id: str,
        context: ContextPackage,
        required_permissions: tuple[str, ...] = (),
        budget: Mapping[str, Any] | None = None,
        abort_criteria: tuple[str, ...] = (),
    ) -> ExecutionContract:
        contract = ExecutionContract(
            execution_id="HOS-EXE-" + uuid.uuid4().hex[:12].upper(),
            correlation_id="HOS-COR-" + uuid.uuid4().hex[:12].upper(),
            goal=goal,
            owner_id=owner_id,
            context=context,
            required_permissions=tuple(required_permissions),
            budget=MappingProxyType(dict(budget or {})),
            abort_criteria=tuple(abort_criteria),
        )
        self._contracts[contract.execution_id] = contract
        self._emit(contract.execution_id, "EXECUTION_PROPOSED", {"goal": goal, "owner_id": owner_id})
        return contract

    def transition(self, execution_id: str, status: ExecutionStatus, *, reason: str = "") -> ExecutionContract:
        current = self._contracts[execution_id]
        if current.status in _TERMINAL_STATUSES:
            raise ValueError(f"Execution {execution_id} already reached a terminal status: {current.status.value}")
        updated = replace(current, status=status)
        self._contracts[execution_id] = updated
        self._emit(execution_id, f"EXECUTION_{status.value}", {"reason": reason})
        return updated

    def get(self, execution_id: str) -> ExecutionContract:
        return self._contracts[execution_id]

    def log(self, execution_id: str) -> list[ExecutionEvent]:
        return list(self._log.get(execution_id, []))

    def _emit(self, execution_id: str, event_type: str, payload: Mapping[str, Any]) -> None:
        event = ExecutionEvent(
            event_id="HOS-CEV-" + uuid.uuid4().hex[:12].upper(),
            execution_id=execution_id,
            event_type=event_type,
            occurred_at=datetime.now(UTC).isoformat(),
            payload=MappingProxyType(dict(payload)),
        )
        self._log.setdefault(execution_id, []).append(event)
