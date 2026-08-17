"""Snapshot <-> event-ledger checkpoints (2026-08-17 full audit, §17).

The project keeps several durable states in parallel (SQLiteEventStore,
SQLiteHubStore, SQLiteSelfModelStore, GraphStore, recovery/execution/
experiment state, the app's localStorage). Nothing formally answered:
"this exact snapshot corresponds to the event ledger up to hash X" — so
after a restart the system could silently continue on a snapshot that lags
(or leads) its ledger.

``StateCheckpoint`` records that correspondence, and ``verify_checkpoint``
answers with an outcome object. On any mismatch the outcome is
``RECONCILIATION_REQUIRED`` — never a silent adoption of one side. Which
side wins is a human/owner decision performed elsewhere; this module only
detects and names the divergence (the same refusal-as-outcome convention
as the Proof Kernel and DecisionEngine).

Hashing note: ``snapshot_hash`` is computed here over canonical JSON of
whatever state dict the caller passes; ``ledger_head_hash`` should come
from the ledger itself (e.g. ``SQLiteEventStore``'s hash chain head).
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


def _now() -> str:
    return datetime.now(UTC).isoformat()


def canonical_state_hash(state: dict[str, Any]) -> str:
    """SHA-256 over canonical (sorted-keys, compact) JSON of a state dict."""
    canonical = json.dumps(state, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class CheckpointVerdict(str, Enum):
    CONSISTENT = "CONSISTENT"
    RECONCILIATION_REQUIRED = "RECONCILIATION_REQUIRED"


@dataclass(frozen=True)
class StateCheckpoint:
    """One recorded correspondence between a snapshot and its ledger."""

    subsystem: str
    snapshot_hash: str
    ledger_head_hash: str
    last_event_sequence: int
    schema_version: str
    state_version: str
    checkpoint_id: str = field(
        default_factory=lambda: f"HOS-CHK-{uuid.uuid4().hex[:12].upper()}"
    )
    created_at: str = field(default_factory=_now)


@dataclass(frozen=True)
class CheckpointVerification:
    verdict: CheckpointVerdict
    checkpoint_id: str
    mismatches: tuple[str, ...] = ()


def create_checkpoint(
    subsystem: str,
    state: dict[str, Any],
    ledger_head_hash: str,
    last_event_sequence: int,
    schema_version: str,
    state_version: str,
) -> StateCheckpoint:
    if not subsystem.strip():
        raise ValueError("subsystem must be named explicitly")
    if last_event_sequence < 0:
        raise ValueError("last_event_sequence must be >= 0")
    return StateCheckpoint(
        subsystem=subsystem,
        snapshot_hash=canonical_state_hash(state),
        ledger_head_hash=ledger_head_hash,
        last_event_sequence=last_event_sequence,
        schema_version=schema_version,
        state_version=state_version,
    )


def verify_checkpoint(
    checkpoint: StateCheckpoint,
    state: dict[str, Any],
    ledger_head_hash: str,
    last_event_sequence: int,
    schema_version: str | None = None,
) -> CheckpointVerification:
    """Compare current reality against a recorded checkpoint.

    Any divergence yields RECONCILIATION_REQUIRED with every mismatch
    named — never a silent adoption of either side.
    """
    mismatches: list[str] = []
    current_snapshot_hash = canonical_state_hash(state)
    if current_snapshot_hash != checkpoint.snapshot_hash:
        mismatches.append(
            f"snapshot hash differs (checkpoint {checkpoint.snapshot_hash[:12]}…, "
            f"current {current_snapshot_hash[:12]}…)"
        )
    if ledger_head_hash != checkpoint.ledger_head_hash:
        mismatches.append(
            f"ledger head differs (checkpoint {checkpoint.ledger_head_hash[:12]}…, "
            f"current {ledger_head_hash[:12]}…)"
        )
    if last_event_sequence != checkpoint.last_event_sequence:
        mismatches.append(
            f"event sequence differs (checkpoint {checkpoint.last_event_sequence}, "
            f"current {last_event_sequence})"
        )
    if schema_version is not None and schema_version != checkpoint.schema_version:
        mismatches.append(
            f"schema version differs (checkpoint {checkpoint.schema_version}, "
            f"current {schema_version})"
        )
    if mismatches:
        return CheckpointVerification(
            CheckpointVerdict.RECONCILIATION_REQUIRED,
            checkpoint.checkpoint_id,
            tuple(mismatches),
        )
    return CheckpointVerification(CheckpointVerdict.CONSISTENT, checkpoint.checkpoint_id)
