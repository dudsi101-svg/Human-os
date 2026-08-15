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
            # Dedicated recovery_* event types are not yet in event.types.json
            # (ADR-RECOVERY-004's open item); STATE_OBSERVED is the closest
            # canonical type until they are added. Envelope shape matches
            # ExecutionLoop._record_domain_event's.
            self._event_store.append({
                "id": event_id,
                "event_type": "STATE_OBSERVED",
                "occurred_at": timestamp,
                "actor_id": initiator,
                "subject_ids": [scope],
                "payload": {**fields, "signature": signature},
                "correlation_id": event_id,
                "immutable": True,
            })
        return event
