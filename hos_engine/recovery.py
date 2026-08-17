from __future__ import annotations

import base64
import hashlib
import hmac as hmac_lib
import uuid
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import Enum

from .authority import AuthorityRole, RoleGrantRegistry
from .event_store import EventStore
from .hub_entity_registry import EntityRegistry, HubEntity, HubEntityStatus
from .protocol_security import canonical_json
from .sqlite_store import SQLiteEventStore

"""First slice of the Sovereign Recovery Kernel (SAFE MODE).

Implements ADR-RECOVERY-001..004 within the founder resolutions of
ADR-RECOVERY-006: seven named emergency modes with a per-mode mapping to
the Constitution's R0-R4 scale, a per-mode auto-vs-manual trigger split,
dual-key sovereignty for the consequential modes, minimal scope of access,
time-bounded activations, and a mandatory 13-field emergency event log in
which refusals are recorded too.

Structural guarantees (ADR-RECOVERY-002), enforced by design rather than
configuration:

- No API on this module mutates recovery policy or the audit log. The
  policy tables are module-level constants and the kernel exposes no
  setter, so "Agent nie moze zmienic polityki Recovery ani wylaczyc
  audytu" holds because the operations do not exist.
- The kernel calls no AI model and no external service -- an AI outage
  cannot block manual recovery.
- Agents, services, and system processes can never activate a mode; the
  refusal itself is logged.

Like the Proof Kernel and DecisionEngine, the kernel evaluates declared
inputs (who the initiator is, what was verified) -- pass a
RoleGrantRegistry to have OWNER/RECOVERY_CUSTODIAN claims checked against
real grants instead of trusted declarations. Event signing uses HMAC-SHA256
over the canonical JSON of the event, sharing security/THREAT_MODEL.md's
stated limitation: a local reference mechanism, not production-grade key
management.
"""


class EmergencyMode(str, Enum):
    """The seven modes from ADR-RECOVERY-001, source SS4."""

    SAFE_MODE = "SAFE_MODE"
    FREEZE = "FREEZE"
    READ_ONLY = "READ_ONLY"
    DISCONNECT = "DISCONNECT"
    ROLLBACK = "ROLLBACK"
    EXPORT = "EXPORT"
    RECOVERY = "RECOVERY"


# ADR-RECOVERY-006 SS2: each mode mapped individually to the Constitution's
# R0-R4; none reaches R4 (all seven are sanctioned mechanisms).
CONSTITUTIONAL_RISK_FOR_MODE: dict[EmergencyMode, str] = {
    EmergencyMode.SAFE_MODE: "R0",
    EmergencyMode.READ_ONLY: "R0",
    EmergencyMode.FREEZE: "R1",
    EmergencyMode.DISCONNECT: "R1",
    EmergencyMode.EXPORT: "R1",
    EmergencyMode.ROLLBACK: "R2",
    EmergencyMode.RECOVERY: "R3",
}

# ADR-RECOVERY-006 SS3: protective, non-destructive modes may auto-trigger
# (with owner notification and unconditional reversal); consequential modes
# require explicit human initiation, always.
AUTO_TRIGGER_ALLOWED: frozenset[EmergencyMode] = frozenset({
    EmergencyMode.SAFE_MODE,
    EmergencyMode.READ_ONLY,
    EmergencyMode.FREEZE,
    EmergencyMode.DISCONNECT,
})

# Dual-key sovereignty (ADR-RECOVERY-003): the two highest-consequence
# modes require an independent second key -- an approval from a
# RECOVERY_CUSTODIAN who is not the initiator.
DUAL_KEY_REQUIRED: frozenset[EmergencyMode] = frozenset({
    EmergencyMode.ROLLBACK,
    EmergencyMode.RECOVERY,
})

# Roles that can never activate any mode (ADR-RECOVERY-003: Emergency Root
# "nie jest dostepny dla agentow ani automatyzacji").
_EXCLUDED_ROLES: frozenset[AuthorityRole] = frozenset({
    AuthorityRole.AGENT,
    AuthorityRole.SERVICE,
    AuthorityRole.SYSTEM_PROCESS,
})


class TriggerKind(str, Enum):
    MANUAL_OWNER = "MANUAL_OWNER"
    AUTOMATIC_ANOMALY = "AUTOMATIC_ANOMALY"


@dataclass(frozen=True)
class EmergencyEvent:
    """The mandatory 13-field record from ADR-RECOVERY-004, plus a schema
    version and an optional HMAC signature. Refused attempts produce this
    record too -- the audit trail covers what was denied, not only what
    ran."""

    event_id: str
    timestamp: str
    initiator: str
    recovery_mode: str
    reason: str
    scope: str
    systems_affected: tuple[str, ...]
    actions_executed: tuple[str, ...]
    data_accessed: tuple[str, ...]
    changes_created: tuple[str, ...]
    expiration_time: str | None
    verification_method: str
    result: str
    version: str = "0.1"
    signature: str | None = None


@dataclass(frozen=True)
class RecoveryActivation:
    activation_id: str
    mode: EmergencyMode
    scope: str
    initiator: str
    trigger: TriggerKind
    constitutional_risk: str
    activated_at: str
    expires_at: str
    owner_notified: bool
    custodian_approval_by: str | None = None
    deactivated_at: str | None = None


@dataclass(frozen=True)
class RecoverySnapshot:
    """"Create Recovery Snapshot" contract (source SS9): a canonical
    checkpoint with links to versions and representations. This slice
    captures the declared entities' state verbatim; representation links
    beyond the Hub registry are future work."""

    snapshot_id: str
    scope: str
    created_at: str
    created_by: str
    entity_states: tuple[tuple[str, str, str], ...]  # (entity_id, working_name, status)


@dataclass(frozen=True)
class DisconnectedRepresentation:
    """"Disconnect Representation" contract (source SS9): the location or
    integration is detached while the historical relation is preserved --
    this record IS that preserved relation."""

    disconnect_id: str
    entity_id: str
    representation: str
    disconnected_at: str
    disconnected_by: str
    activation_id: str


class RecoveryRefused(Exception):
    """Raised for a refused activation/deactivation. Unlike ExecutionLoop's
    outcome-object style, refusal here is an exception on purpose: a caller
    that ignores a DecisionOutcome merely lacks a recommendation, but a
    caller that ignores a refused emergency-mode activation might proceed
    as if protection were active. The refusal is still logged as a
    first-class EmergencyEvent before the exception leaves the kernel."""


def _now() -> str:
    return datetime.now(UTC).isoformat()


class SovereignRecoveryKernel:
    """Activation, expiry, and audit of the seven emergency modes.

    Scope isolation (ADR-RECOVERY-003): an activation covers exactly the
    scope it names -- is_active(mode, scope) for any other scope stays
    False, so recovering one area never unlocks another.
    """

    def __init__(
        self,
        *,
        roles: RoleGrantRegistry | None = None,
        entities: EntityRegistry | None = None,
        event_store: EventStore | SQLiteEventStore | None = None,
        signing_secret: bytes | None = None,
    ) -> None:
        self._roles = roles
        self._entities = entities
        self._event_store = event_store
        self._signing_secret = signing_secret
        self._activations: dict[str, RecoveryActivation] = {}
        self._events: list[EmergencyEvent] = []
        self._snapshots: dict[str, RecoverySnapshot] = {}
        self._disconnects: list[DisconnectedRepresentation] = []

    # -- activation ------------------------------------------------------

    def activate(
        self,
        *,
        mode: EmergencyMode,
        initiator_id: str,
        initiator_role: AuthorityRole,
        scope: str,
        reason: str,
        expires_at: str,
        verification_method: str,
        trigger: TriggerKind = TriggerKind.MANUAL_OWNER,
        custodian_approval_by: str | None = None,
        owner_notified: bool = False,
    ) -> RecoveryActivation:
        refusal = self._refusal_reason(
            mode=mode,
            initiator_id=initiator_id,
            initiator_role=initiator_role,
            scope=scope,
            trigger=trigger,
            custodian_approval_by=custodian_approval_by,
            owner_notified=owner_notified,
        )
        if refusal is not None:
            self._log(
                initiator=initiator_id, mode=mode, reason=reason, scope=scope,
                expiration_time=expires_at, verification_method=verification_method,
                result=f"REFUSED: {refusal}",
            )
            raise RecoveryRefused(refusal)

        activation = RecoveryActivation(
            activation_id="HOS-RCV-" + uuid.uuid4().hex[:12].upper(),
            mode=mode,
            scope=scope,
            initiator=initiator_id,
            trigger=trigger,
            constitutional_risk=CONSTITUTIONAL_RISK_FOR_MODE[mode],
            activated_at=_now(),
            expires_at=expires_at,
            owner_notified=owner_notified or trigger == TriggerKind.MANUAL_OWNER,
            custodian_approval_by=custodian_approval_by,
        )
        self._activations[activation.activation_id] = activation
        self._log(
            initiator=initiator_id, mode=mode, reason=reason, scope=scope,
            actions_executed=(f"activate:{mode.value}",),
            changes_created=(activation.activation_id,),
            expiration_time=expires_at, verification_method=verification_method,
            result="ACTIVATED",
        )
        return activation

    def deactivate(
        self,
        activation_id: str,
        *,
        initiator_id: str,
        initiator_role: AuthorityRole,
        reason: str,
    ) -> RecoveryActivation:
        activation = self._activations[activation_id]
        if initiator_role in _EXCLUDED_ROLES:
            self._log(
                initiator=initiator_id, mode=activation.mode, reason=reason,
                scope=activation.scope, expiration_time=activation.expires_at,
                verification_method="role-declaration",
                result="REFUSED: agents and automations cannot deactivate recovery modes",
            )
            raise RecoveryRefused("Agents and automations cannot deactivate recovery modes.")
        if activation.deactivated_at is not None:
            raise ValueError(f"Activation {activation_id} is already deactivated")

        # An auto-triggered activation is unconditionally reversible by the
        # owner (ADR-RECOVERY-006 SS3); a manual one is reversible by its
        # initiator or the owner. Both paths land here -- the only barred
        # deactivators are the excluded roles above.
        updated = replace(activation, deactivated_at=_now())
        self._activations[activation_id] = updated
        self._log(
            initiator=initiator_id, mode=activation.mode, reason=reason,
            scope=activation.scope,
            actions_executed=(f"deactivate:{activation.mode.value}",),
            expiration_time=activation.expires_at,
            verification_method="role-declaration", result="DEACTIVATED",
        )
        return updated

    def is_active(self, mode: EmergencyMode, *, scope: str) -> bool:
        now = _now()
        return any(
            a.mode == mode and a.scope == scope
            and a.deactivated_at is None and a.expires_at > now
            for a in self._activations.values()
        )

    # -- Hub contracts (first slice: Freeze Entity / Scope) --------------

    def freeze_entity(
        self,
        entity_id: str,
        *,
        initiator_id: str,
        initiator_role: AuthorityRole,
        reason: str,
        expires_at: str,
        verification_method: str,
    ) -> HubEntity:
        """ADR-RECOVERY-004's "Freeze Entity / Scope" contract. Per the
        founder resolution (ADR-RECOVERY-006 SS4) the frozen state IS
        HubEntityStatus.SUSPENDED -- no separate FROZEN status exists.
        Non-destructive: the entity and its history stay retrievable."""
        if self._entities is None:
            raise ValueError("No EntityRegistry wired into this kernel")
        self.activate(
            mode=EmergencyMode.FREEZE,
            initiator_id=initiator_id,
            initiator_role=initiator_role,
            scope=f"entity:{entity_id}",
            reason=reason,
            expires_at=expires_at,
            verification_method=verification_method,
        )
        return self._entities.transition(entity_id, HubEntityStatus.SUSPENDED)

    def create_recovery_snapshot(
        self,
        *,
        initiator_id: str,
        initiator_role: AuthorityRole,
        scope: str,
        entity_ids: tuple[str, ...],
        reason: str,
        verification_method: str,
    ) -> RecoverySnapshot:
        """"Create Recovery Snapshot": non-destructive, so no dual key and no
        mode activation -- but the excluded roles still cannot call it, and
        the snapshot itself lands in the audit trail."""
        if self._entities is None:
            raise ValueError("No EntityRegistry wired into this kernel")
        if initiator_role in _EXCLUDED_ROLES:
            self._log(
                initiator=initiator_id, mode=EmergencyMode.RECOVERY, reason=reason,
                scope=scope, expiration_time=None,
                verification_method=verification_method,
                result="REFUSED: agents and automations cannot create recovery snapshots",
            )
            raise RecoveryRefused("Agents and automations cannot create recovery snapshots.")
        states = tuple(
            (e.entity_id, e.working_name, e.status.value)
            for e in (self._entities.get(eid) for eid in entity_ids)
        )
        snapshot = RecoverySnapshot(
            snapshot_id="HOS-SNP-" + uuid.uuid4().hex[:12].upper(),
            scope=scope, created_at=_now(), created_by=initiator_id,
            entity_states=states,
        )
        self._snapshots[snapshot.snapshot_id] = snapshot
        self._log(
            initiator=initiator_id, mode=EmergencyMode.RECOVERY, reason=reason,
            scope=scope, actions_executed=("create_recovery_snapshot",),
            data_accessed=entity_ids, changes_created=(snapshot.snapshot_id,),
            expiration_time=None, verification_method=verification_method,
            result="SNAPSHOT_CREATED",
        )
        return snapshot

    def get_snapshot(self, snapshot_id: str) -> RecoverySnapshot:
        return self._snapshots[snapshot_id]

    def rollback_entity(
        self,
        *,
        snapshot_id: str,
        entity_id: str,
        initiator_id: str,
        initiator_role: AuthorityRole,
        custodian_approval_by: str | None,
        reason: str,
        expires_at: str,
        verification_method: str,
    ) -> HubEntity:
        """"Rollback Entity / Workflow": creates a NEW version based on the
        snapshot state and records the provenance chain -- history is never
        rewritten. Consequential: goes through the full ROLLBACK activation,
        so dual-key sovereignty and the manual-only trigger rule apply."""
        if self._entities is None:
            raise ValueError("No EntityRegistry wired into this kernel")
        snapshot = self._snapshots[snapshot_id]
        captured = next(
            (s for s in snapshot.entity_states if s[0] == entity_id), None,
        )
        if captured is None:
            raise ValueError(f"Snapshot {snapshot_id} does not cover entity {entity_id}")
        activation = self.activate(
            mode=EmergencyMode.ROLLBACK,
            initiator_id=initiator_id,
            initiator_role=initiator_role,
            scope=f"entity:{entity_id}",
            reason=reason,
            expires_at=expires_at,
            verification_method=verification_method,
            custodian_approval_by=custodian_approval_by,
        )
        current = self._entities.get(entity_id)
        restored = self._entities.register(
            entity_type=current.entity_type,
            working_name=captured[1],
            responsibility_owner_id=current.responsibility_owner_id,
            provenance_source=f"rollback:{snapshot_id}:{entity_id}",
        )
        # The provenance chain: the old version is retired via the recorded,
        # attributed merge -- never deleted (ADR-HUB-005 semantics reused).
        self._entities.merge(
            keep_entity_id=restored.entity_id,
            retire_entity_id=entity_id,
            reason=f"rollback to snapshot {snapshot_id}: {reason}",
            evidence=snapshot_id,
            approved_by=custodian_approval_by or initiator_id,
        )
        self._log(
            initiator=initiator_id, mode=EmergencyMode.ROLLBACK, reason=reason,
            scope=f"entity:{entity_id}",
            actions_executed=("rollback_entity",),
            data_accessed=(snapshot_id,),
            changes_created=(restored.entity_id, activation.activation_id),
            expiration_time=expires_at, verification_method=verification_method,
            result="ROLLED_BACK",
        )
        return self._entities.get(restored.entity_id)

    def disconnect_representation(
        self,
        *,
        entity_id: str,
        representation: str,
        initiator_id: str,
        initiator_role: AuthorityRole,
        reason: str,
        expires_at: str,
        verification_method: str,
        trigger: TriggerKind = TriggerKind.MANUAL_OWNER,
        owner_notified: bool = False,
    ) -> DisconnectedRepresentation:
        """"Disconnect Representation": detaches a location/integration while
        keeping the historical relation (the returned record). Protective
        mode -- may auto-trigger with owner notification."""
        activation = self.activate(
            mode=EmergencyMode.DISCONNECT,
            initiator_id=initiator_id,
            initiator_role=initiator_role,
            scope=f"representation:{entity_id}:{representation}",
            reason=reason,
            expires_at=expires_at,
            verification_method=verification_method,
            trigger=trigger,
            owner_notified=owner_notified,
        )
        record = DisconnectedRepresentation(
            disconnect_id="HOS-DSC-" + uuid.uuid4().hex[:12].upper(),
            entity_id=entity_id, representation=representation,
            disconnected_at=_now(), disconnected_by=initiator_id,
            activation_id=activation.activation_id,
        )
        self._disconnects.append(record)
        return record

    def disconnected_representations(self, entity_id: str) -> tuple[DisconnectedRepresentation, ...]:
        return tuple(d for d in self._disconnects if d.entity_id == entity_id)

    def export_sovereign_package(
        self,
        *,
        initiator_id: str,
        initiator_role: AuthorityRole,
        scope: str,
        reason: str,
        expires_at: str,
        verification_method: str,
    ) -> dict[str, object]:
        """"Export Sovereign Package": a portable package of data, graph,
        metadata and the change register. Consequential (manual-only) but
        not dual-key -- EXPORT maps to R1 per ADR-RECOVERY-006."""
        activation = self.activate(
            mode=EmergencyMode.EXPORT,
            initiator_id=initiator_id,
            initiator_role=initiator_role,
            scope=scope,
            reason=reason,
            expires_at=expires_at,
            verification_method=verification_method,
        )
        entities: list[dict[str, str]] = []
        if self._entities is not None:
            entities = [
                {"entity_id": e.entity_id, "entity_type": e.entity_type.value,
                 "working_name": e.working_name, "status": e.status.value,
                 "created_at": e.created_at}
                for e in self._entities.all_entities()
            ]
        package: dict[str, object] = {
            "package_version": "0.1",
            "generated_at": _now(),
            "scope": scope,
            "activation_id": activation.activation_id,
            "entities": entities,
            "snapshots": [s.snapshot_id for s in self._snapshots.values()],
            "disconnected_representations": [
                d.disconnect_id for d in self._disconnects
            ],
            "emergency_events": [e.event_id for e in self._events],
            "format": "open-json",
        }
        self._log(
            initiator=initiator_id, mode=EmergencyMode.EXPORT, reason=reason,
            scope=scope, actions_executed=("export_sovereign_package",),
            data_accessed=("entities", "snapshots", "emergency_events"),
            changes_created=(activation.activation_id,),
            expiration_time=expires_at, verification_method=verification_method,
            result="EXPORTED",
        )
        return package

    # -- audit -----------------------------------------------------------

    def events(self) -> tuple[EmergencyEvent, ...]:
        """The append-only audit trail, refusals included. There is no
        deletion or mutation API for this log anywhere on the kernel."""
        return tuple(self._events)

    # -- internals -------------------------------------------------------

    def _refusal_reason(
        self,
        *,
        mode: EmergencyMode,
        initiator_id: str,
        initiator_role: AuthorityRole,
        scope: str,
        trigger: TriggerKind,
        custodian_approval_by: str | None,
        owner_notified: bool,
    ) -> str | None:
        if initiator_role in _EXCLUDED_ROLES:
            return "Agents and automations cannot activate recovery modes."
        if trigger == TriggerKind.AUTOMATIC_ANOMALY:
            if mode not in AUTO_TRIGGER_ALLOWED:
                return (
                    f"{mode.value} requires explicit human initiation; "
                    "automatic triggering is limited to protective modes."
                )
            if not owner_notified:
                return "Automatic activation requires immediate owner notification."
        if (
            self._roles is not None
            and trigger == TriggerKind.MANUAL_OWNER
            and not self._roles.has_role(initiator_id, AuthorityRole.OWNER, scope=scope)
        ):
            return "Initiator does not hold an active OWNER grant for this scope."
        if mode in DUAL_KEY_REQUIRED:
            if custodian_approval_by is None:
                return f"{mode.value} requires an independent recovery-custodian approval."
            if custodian_approval_by == initiator_id:
                return (
                    "Dual-key sovereignty requires the custodian to be a "
                    "different identity than the initiator."
                )
            if self._roles is not None and not self._roles.has_role(
                custodian_approval_by, AuthorityRole.RECOVERY_CUSTODIAN, scope=scope,
            ):
                return "Approver does not hold an active RECOVERY_CUSTODIAN grant for this scope."
        return None

    def _log(
        self,
        *,
        initiator: str,
        mode: EmergencyMode,
        reason: str,
        scope: str,
        expiration_time: str | None,
        verification_method: str,
        result: str,
        systems_affected: tuple[str, ...] = (),
        actions_executed: tuple[str, ...] = (),
        data_accessed: tuple[str, ...] = (),
        changes_created: tuple[str, ...] = (),
    ) -> EmergencyEvent:
        event_id = "HOS-EMG-" + uuid.uuid4().hex[:12].upper()
        timestamp = _now()
        fields = {
            "event_id": event_id,
            "timestamp": timestamp,
            "initiator": initiator,
            "recovery_mode": mode.value,
            "reason": reason,
            "scope": scope,
            "systems_affected": list(systems_affected),
            "actions_executed": list(actions_executed),
            "data_accessed": list(data_accessed),
            "changes_created": list(changes_created),
            "expiration_time": expiration_time,
            "verification_method": verification_method,
            "result": result,
            "version": "0.1",
        }
        signature = None
        if self._signing_secret is not None:
            digest = hmac_lib.new(
                self._signing_secret, canonical_json(fields), hashlib.sha256,
            ).digest()
            signature = base64.urlsafe_b64encode(digest).decode()
        event = EmergencyEvent(
            event_id=event_id,
            timestamp=timestamp,
            initiator=initiator,
            recovery_mode=mode.value,
            reason=reason,
            scope=scope,
            systems_affected=systems_affected,
            actions_executed=actions_executed,
            data_accessed=data_accessed,
            changes_created=changes_created,
            expiration_time=expiration_time,
            verification_method=verification_method,
            result=result,
            signature=signature,
        )
        self._events.append(event)
        if self._event_store is not None:
            # DD-003 (resolved 2026-08-17): recovery outcomes map to the
            # canonical vocabulary. Anything that is neither an activation,
            # a deactivation, nor a refusal (snapshot/rollback/export usage
            # records) stays STATE_OBSERVED, as does all pre-DD-003 history.
            # Envelope shape matches ExecutionLoop._record_domain_event's.
            if result.startswith("REFUSED"):
                canonical_type = "RECOVERY_REFUSED"
            elif result == "DEACTIVATED":
                canonical_type = "RECOVERY_DEACTIVATED"
            elif result == "ACTIVATED":
                canonical_type = (
                    "ENTITY_FROZEN"
                    if mode is EmergencyMode.FREEZE
                    else "RECOVERY_ACTIVATED"
                )
            else:
                canonical_type = "STATE_OBSERVED"
            self._event_store.append({
                "id": event_id,
                "event_type": canonical_type,
                "occurred_at": timestamp,
                "actor_id": initiator,
                # subject_ids is canonically a list of HOSIds; free-text
                # scopes ("system", "finances") live in the payload, and
                # only an entity-addressed scope contributes a real ID.
                "subject_ids": (
                    [scope.removeprefix("entity:")]
                    if scope.startswith("entity:")
                    else []
                ),
                "payload": {**fields, "signature": signature},
                "correlation_id": event_id,
                "immutable": True,
            })
        return event
