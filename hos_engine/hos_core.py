from __future__ import annotations

import uuid
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from enum import Enum
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
    context_id: str
    subject_id: str
    version: int
    data: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class ContextManager:
    """Builds and versions the context package an execution runs against.

    First slice of HOS Core (ADR-CORE-001, Rozszerzenie Architektury v0.2 §2).
    Each snapshot is immutable and additive; nothing is overwritten in place.
    """

    def __init__(self) -> None:
        self._history: dict[str, list[ContextPackage]] = {}

    def snapshot(self, subject_id: str, data: dict[str, Any]) -> ContextPackage:
        history = self._history.setdefault(subject_id, [])
        package = ContextPackage(
            context_id="HOS-CTX-" + uuid.uuid4().hex[:12].upper(),
            subject_id=subject_id,
            version=len(history) + 1,
            data=dict(data),
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
    execution_id: str
    correlation_id: str
    goal: str
    owner_id: str
    context: ContextPackage
    required_permissions: tuple[str, ...] = ()
    budget: dict[str, Any] = field(default_factory=dict)
    abort_criteria: tuple[str, ...] = ()
    status: ExecutionStatus = ExecutionStatus.PROPOSED


@dataclass(frozen=True)
class ExecutionEvent:
    event_id: str
    execution_id: str
    event_type: str
    occurred_at: str
    payload: dict[str, Any] = field(default_factory=dict)


_TERMINAL_STATUSES = frozenset(
    {ExecutionStatus.COMPLETED, ExecutionStatus.FAILED, ExecutionStatus.ABORTED}
)


class EventEngine:
    """Opens execution contracts and logs their lifecycle as an immutable event trail.

    First slice of HOS Core (ADR-CORE-001, Rozszerzenie Architektury v0.2 §2).
    This is deliberately narrower than hos_engine.event_store.EventStore: that
    module persists arbitrary domain events, while this one tracks the
    lifecycle of a single unit of work (an ExecutionContract) from proposal
    through a terminal status, matching the "minimal execution contract"
    fields in the HOS Core specification (execution_id, correlation_id, goal,
    owner, context, required permissions, budget, abort criteria, event log).
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
        budget: dict[str, Any] | None = None,
        abort_criteria: tuple[str, ...] = (),
    ) -> ExecutionContract:
        contract = ExecutionContract(
            execution_id="HOS-EXE-" + uuid.uuid4().hex[:12].upper(),
            correlation_id="HOS-COR-" + uuid.uuid4().hex[:12].upper(),
            goal=goal,
            owner_id=owner_id,
            context=context,
            required_permissions=tuple(required_permissions),
            budget=dict(budget or {}),
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

    def _emit(self, execution_id: str, event_type: str, payload: dict[str, Any]) -> None:
        event = ExecutionEvent(
            event_id="HOS-CEV-" + uuid.uuid4().hex[:12].upper(),
            execution_id=execution_id,
            event_type=event_type,
            occurred_at=datetime.now(UTC).isoformat(),
            payload=payload,
        )
        self._log.setdefault(execution_id, []).append(event)
