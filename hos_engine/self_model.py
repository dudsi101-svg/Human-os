"""Conversational self model — the first vertical slice of the Living Self Model.

Principle (implementation directive, 2026-08-16): CONVERSATION ON THE FRONT,
STRUCTURED USER MODEL UNDERNEATH. A conversation with an AI is an *input
interface* and an evidence source — it is never the canonical user model.

This module deliberately builds ON TOP of ``hos_engine.human_model`` rather
than beside it: ``HumanRecord`` already carries the epistemic core the
directive requires (``EvidenceType`` with USER_DECLARATION / OBSERVATION /
AI_INFERENCE / HYPOTHESIS, confidence in [0, 1], provenance via ``source_id``,
a ``supersedes`` chain that versions without overwriting, subject-only
``contest``, ``sensitive`` and ``consent_scope``). What this module adds:

- ``InteractionLog`` — conversations stored as first-class Interactions,
  strictly separated from the user model (storing a message never creates a
  model record by itself);
- a hypothesis lifecycle: propose -> confirm (user) / reject (user) /
  mark outdated, always via the supersedes chain, never by mutation;
- ``Tension`` — contradictions kept as valuable signal, never auto-resolved;
- ``living_view`` / ``why`` / ``decision_inputs`` — the Living Self Model
  presentation, per-record provenance ("why does Human OS think this?"),
  and the epistemically-split feed for the Decision Engine.

Confidence semantics: the *fact that the user said something* is carried by
provenance (the message reference), not by the confidence number; the
``confidence`` field always means confidence in the *interpretation*.

What is deliberately NOT here: no NLP, no extract_profile() magic — deciding
that an utterance contains a candidate declaration/observation/hypothesis is
an application/agent concern. The engine only guarantees the epistemic
bookkeeping once a candidate is submitted.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from .consent import ConsentRegistry
from .human_model import EvidenceType, HumanModel, HumanRecord, RecordStatus


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _new_id(prefix: str) -> str:
    return f"HOS-{prefix}-" + uuid.uuid4().hex[:12].upper()


class InteractionMode(str, Enum):
    """The three exploration depths of the About-Me conversation."""

    NATURAL = "NATURAL"
    DEEP_DISCOVERY = "DEEP_DISCOVERY"
    EXPLORATORY = "EXPLORATORY"


class MessageAuthor(str, Enum):
    USER = "USER"
    SYSTEM = "SYSTEM"


@dataclass(frozen=True)
class InteractionMessage:
    message_id: str
    interaction_id: str
    author: MessageAuthor
    text: str
    at: str


@dataclass(frozen=True)
class Interaction:
    interaction_id: str
    subject_id: str
    mode: InteractionMode
    started_at: str
    purpose: str


class InteractionLog:
    """Conversations as raw, append-only Interactions.

    THE CHAT IS NOT THE USER MODEL: nothing recorded here changes the
    HumanModel. Records reference messages (provenance), never the reverse.
    """

    def __init__(self) -> None:
        self._interactions: dict[str, Interaction] = {}
        self._messages: dict[str, list[InteractionMessage]] = {}

    def start(self, *, subject_id: str, mode: InteractionMode = InteractionMode.NATURAL,
              purpose: str = "self_model") -> Interaction:
        it = Interaction(_new_id("CNV"), subject_id, mode, _now(), purpose)
        self._interactions[it.interaction_id] = it
        self._messages[it.interaction_id] = []
        return it

    def append(self, interaction_id: str, *, author: MessageAuthor, text: str) -> InteractionMessage:
        if interaction_id not in self._interactions:
            raise KeyError("unknown interaction")
        msg = InteractionMessage(_new_id("MSG"), interaction_id, author, text, _now())
        self._messages[interaction_id].append(msg)
        return msg

    def get(self, interaction_id: str) -> Interaction:
        return self._interactions[interaction_id]

    def messages(self, interaction_id: str) -> list[InteractionMessage]:
        return list(self._messages[interaction_id])

    def all_interactions(self) -> list[Interaction]:
        return list(self._interactions.values())

    def all_messages(self) -> list[InteractionMessage]:
        return [m for msgs in self._messages.values() for m in msgs]

    @classmethod
    def restore(cls, interactions: list[Interaction],
                messages: list[InteractionMessage]) -> InteractionLog:
        log = cls()
        for it in interactions:
            log._interactions[it.interaction_id] = it
            log._messages[it.interaction_id] = []
        for m in sorted(messages, key=lambda x: x.at):
            log._messages[m.interaction_id].append(m)
        return log

    def find_message(self, message_id: str) -> InteractionMessage | None:
        for msgs in self._messages.values():
            for m in msgs:
                if m.message_id == message_id:
                    return m
        return None


class TensionStatus(str, Enum):
    OPEN = "OPEN"
    EXPLORED = "EXPLORED"
    RESOLVED_BY_USER = "RESOLVED_BY_USER"


@dataclass(frozen=True)
class Tension:
    """A contradiction kept as signal. Never auto-resolved by the system."""

    tension_id: str
    subject_id: str
    record_a: str
    record_b: str
    note: str
    status: TensionStatus
    created_at: str
    resolution: str | None = None


def confidence_band(confidence: float) -> str:
    """UI-facing band — never show false numeric precision to the user."""
    if confidence < 0.4:
        return "LOW"
    if confidence < 0.75:
        return "MEDIUM"
    return "HIGH"


@dataclass
class SelfModelService:
    """Epistemic bookkeeping for the Living Self Model on top of HumanModel.

    Optional consent integration: when a ``consent`` registry and a
    ``grantee_id`` (the profiling agent identity) are supplied, every write
    is authorized against purpose/domain/action/sensitivity first —
    conversations without profiling consent simply never reach the model.
    """

    model: HumanModel = field(default_factory=HumanModel)
    interactions: InteractionLog = field(default_factory=InteractionLog)
    consent: ConsentRegistry | None = None
    grantee_id: str | None = None
    created_by: str = "ProfileInterpreter v0.1"
    event_store: Any = None  # EventStore | SQLiteEventStore (same append(dict) shape)
    _tensions: dict[str, Tension] = field(default_factory=dict)

    def _emit(self, event_type: str, subject_id: str, payload: dict[str, Any],
              correlation_id: str) -> None:
        """Durable audit trail (optional). Uses STATE_OBSERVED like the other
        execution-foundation modules until dedicated event types land
        (docs/DEFERRED_DECISIONS.md DD-003)."""
        if self.event_store is None:
            return
        self.event_store.append({
            "id": _new_id("EVT"),
            "event_type": "STATE_OBSERVED",
            "occurred_at": _now(),
            "actor_id": subject_id,
            "subject_ids": [subject_id],
            "payload": {"self_model": event_type, **payload},
            "correlation_id": correlation_id,
            "immutable": True,
        })

    # ---------------- consent gate ----------------

    def _authorize_write(self, *, subject_id: str, domain: str, sensitive: bool,
                         purpose: str) -> None:
        if self.consent is None or self.grantee_id is None:
            return
        ok = self.consent.authorize(subject_id=subject_id, grantee_id=self.grantee_id,
                                    purpose=purpose, domain=domain, action="write",
                                    sensitive=sensitive)
        if not ok:
            raise PermissionError(
                f"no active consent for purpose={purpose!r} domain={domain!r} "
                f"(sensitive={sensitive}) — utterance stays in the interaction only")

    # ---------------- intake: the three epistemic entry points ----------------

    def declare(self, *, subject_id: str, domain: str, key: str, value: Any,
                message_id: str, sensitive: bool = False, consent_scope: str | None = None,
                purpose: str = "self_model", supersedes: str | None = None) -> HumanRecord:
        """Something the user explicitly said. Interpretation confidence is
        high but not absolute (the mapping utterance->structure can be wrong)."""
        self._authorize_write(subject_id=subject_id, domain=domain,
                              sensitive=sensitive, purpose=purpose)
        rec = self.model.add(
            subject_id=subject_id, domain=domain, key=key, value=value,
            evidence_type=EvidenceType.USER_DECLARATION, confidence=0.9,
            source_id=message_id, sensitive=sensitive, consent_scope=consent_scope,
            supersedes=supersedes, valid_from=_now(), evidence_refs=(message_id,))
        self._emit("declared", subject_id, {"record_id": rec.record_id,
                   "domain": domain, "key": key}, rec.record_id)
        return rec

    def observe(self, *, subject_id: str, domain: str, key: str, value: Any,
                message_id: str, sensitive: bool = False,
                purpose: str = "self_model") -> HumanRecord:
        """A concrete record without interpretation attached."""
        self._authorize_write(subject_id=subject_id, domain=domain,
                              sensitive=sensitive, purpose=purpose)
        rec = self.model.add(
            subject_id=subject_id, domain=domain, key=key, value=value,
            evidence_type=EvidenceType.OBSERVATION, confidence=0.9,
            source_id=message_id, sensitive=sensitive,
            valid_from=_now(), evidence_refs=(message_id,))
        self._emit("observed", subject_id, {"record_id": rec.record_id,
                   "domain": domain, "key": key}, rec.record_id)
        return rec

    def hypothesize(self, *, subject_id: str, domain: str, key: str, value: Any,
                    confidence: float, supported_by: list[str],
                    alternatives: list[str] | None = None,
                    sensitive: bool = False, purpose: str = "self_model") -> HumanRecord:
        """An interpretation generated by the system. Requires supporting
        evidence refs; stays a hypothesis until the user confirms it."""
        if not supported_by:
            raise ValueError("a hypothesis requires supporting evidence refs")
        self._authorize_write(subject_id=subject_id, domain=domain,
                              sensitive=sensitive, purpose=purpose)
        tags = {f"alt:{a}" for a in (alternatives or [])}
        tags.add(f"created_by:{self.created_by}")
        rec = self.model.add(
            subject_id=subject_id, domain=domain, key=key, value=value,
            evidence_type=EvidenceType.HYPOTHESIS, confidence=confidence,
            source_id=supported_by[0], sensitive=sensitive, tags=tags,
            valid_from=_now(), evidence_refs=tuple(supported_by))
        self._emit("hypothesized", subject_id, {"record_id": rec.record_id,
                   "domain": domain, "key": key, "confidence": confidence},
                   rec.record_id)
        return rec

    # ---------------- lifecycle: user-controlled transitions ----------------

    def confirm(self, record_id: str, *, subject_id: str, message_id: str) -> HumanRecord:
        """User confirms a hypothesis: a NEW record (USER_DECLARATION) supersedes
        it; the hypothesis and its status history stay in the store."""
        old = self.model.get(record_id)
        if old.subject_id != subject_id:
            raise PermissionError("only the subject may confirm")
        rec = self.model.add(
            subject_id=subject_id, domain=old.domain, key=old.key, value=old.value,
            evidence_type=EvidenceType.USER_DECLARATION, confidence=0.95,
            source_id=message_id, sensitive=old.sensitive,
            consent_scope=old.consent_scope, supersedes=record_id,
            valid_from=old.valid_from or _now(), last_confirmed_at=_now(),
            evidence_refs=(*old.evidence_refs, message_id))
        self._emit("confirmed_by_user", subject_id,
                   {"record_id": rec.record_id, "supersedes": record_id},
                   record_id)
        return rec

    def reject(self, record_id: str, *, subject_id: str) -> HumanRecord:
        """User rejects a hypothesis: it becomes CONTESTED, never deleted."""
        self.model.contest(record_id, subject_id=subject_id)
        self._emit("rejected_by_user", subject_id, {"record_id": record_id},
                   record_id)
        return self.model.get(record_id)

    def correct(self, record_id: str, *, subject_id: str, value: Any,
                message_id: str) -> HumanRecord:
        """User correction: a new declaration supersedes the old record."""
        old = self.model.get(record_id)
        if old.subject_id != subject_id:
            raise PermissionError("only the subject may correct")
        rec = self.model.add(
            subject_id=subject_id, domain=old.domain, key=old.key, value=value,
            evidence_type=EvidenceType.USER_DECLARATION, confidence=0.9,
            source_id=message_id, sensitive=old.sensitive,
            consent_scope=old.consent_scope, supersedes=record_id,
            valid_from=_now(), last_confirmed_at=_now(),
            evidence_refs=(message_id,))
        self._emit("corrected_by_user", subject_id,
                   {"record_id": rec.record_id, "supersedes": record_id},
                   record_id)
        return rec

    def mark_outdated(self, record_id: str, *, subject_id: str) -> HumanRecord:
        """The information no longer describes the person: the record is
        superseded by a copy with ``valid_to`` closed — history intact."""
        old = self.model.get(record_id)
        if old.subject_id != subject_id:
            raise PermissionError("only the subject may mark outdated")
        rec = self.model.add(
            subject_id=subject_id, domain=old.domain, key=old.key, value=old.value,
            evidence_type=old.evidence_type, confidence=old.confidence,
            source_id=old.source_id, sensitive=old.sensitive,
            consent_scope=old.consent_scope, supersedes=record_id,
            valid_from=old.valid_from, valid_to=_now(),
            evidence_refs=old.evidence_refs)
        self._emit("marked_outdated", subject_id,
                   {"record_id": rec.record_id, "supersedes": record_id},
                   record_id)
        return rec

    # ---------------- tensions ----------------

    def record_tension(self, *, subject_id: str, record_a: str, record_b: str,
                       note: str) -> Tension:
        for rid in (record_a, record_b):
            if self.model.get(rid).subject_id != subject_id:
                raise ValueError("tension records must belong to the subject")
        t = Tension(_new_id("TNS"), subject_id, record_a, record_b, note,
                    TensionStatus.OPEN, _now())
        self._tensions[t.tension_id] = t
        self._emit("tension_recorded", subject_id,
                   {"tension_id": t.tension_id, "record_a": record_a,
                    "record_b": record_b}, t.tension_id)
        return t

    def resolve_tension(self, tension_id: str, *, subject_id: str,
                        resolution: str) -> Tension:
        """Only the user resolves a tension; the system never does."""
        old = self._tensions[tension_id]
        if old.subject_id != subject_id:
            raise PermissionError("only the subject may resolve a tension")
        new = Tension(old.tension_id, old.subject_id, old.record_a, old.record_b,
                      old.note, TensionStatus.RESOLVED_BY_USER, old.created_at,
                      resolution=resolution)
        self._tensions[tension_id] = new
        self._emit("tension_resolved_by_user", subject_id,
                   {"tension_id": tension_id, "resolution": resolution},
                   tension_id)
        return new

    def all_tensions(self) -> list[Tension]:
        return list(self._tensions.values())

    def restore_tension(self, tension: Tension) -> None:
        """Persistence-layer hook: reinsert a tension verbatim, without
        emitting a new audit event (the original recording already did)."""
        self._tensions[tension.tension_id] = tension

    def open_tensions(self, subject_id: str) -> list[Tension]:
        return [t for t in self._tensions.values()
                if t.subject_id == subject_id and t.status == TensionStatus.OPEN]

    # ---------------- presentation: Living Self Model ----------------

    def living_view(self, subject_id: str, *, include_sensitive: bool = False,
                    now_iso: str | None = None) -> dict[str, Any]:
        """The versioned map of the person, split by epistemic status —
        never a raw database table."""
        now = now_iso or _now()
        rows = [r for r in self.model.active_records(subject_id)
                if include_sensitive or not r.sensitive]
        current = [r for r in rows if r.valid_to is None or r.valid_to > now]
        outdated = [r for r in self.model.records_of(subject_id, RecordStatus.ACTIVE)
                    if r.valid_to is not None and r.valid_to <= now
                    and (include_sensitive or not r.sensitive)]

        def of(et: EvidenceType) -> list[HumanRecord]:
            return [r for r in current if r.evidence_type == et]

        contested = [r for r in self.model.records_of(subject_id, RecordStatus.CONTESTED)
                     if include_sensitive or not r.sensitive]
        confirmed = [r for r in of(EvidenceType.USER_DECLARATION)
                     if r.last_confirmed_at is not None]
        declared = [r for r in of(EvidenceType.USER_DECLARATION)
                    if r.last_confirmed_at is None]
        return {
            "confirmed": confirmed,
            "declared": declared,
            "observations": of(EvidenceType.OBSERVATION),
            "hypotheses": of(EvidenceType.HYPOTHESIS) + of(EvidenceType.AI_INFERENCE),
            "rejected": contested,
            "outdated": outdated,
            "tensions": self.open_tensions(subject_id),
        }

    def why(self, record_id: str) -> dict[str, Any]:
        """Answer: WHERE DOES HUMAN OS KNOW THIS FROM?"""
        r = self.model.get(record_id)
        sources = []
        for ref in r.evidence_refs or (r.source_id,):
            msg = self.interactions.find_message(ref)
            sources.append({
                "ref": ref,
                "kind": "interaction_message" if msg else "record_or_external",
                "quote": msg.text if msg else None,
                "interaction_id": msg.interaction_id if msg else None,
            })
        chain, cursor = [], r
        while cursor.supersedes is not None:
            cursor = self.model.get(cursor.supersedes)
            chain.append({"record_id": cursor.record_id, "status": cursor.status.value,
                          "evidence_type": cursor.evidence_type.value,
                          "created_at": cursor.created_at})
        return {
            "record_id": r.record_id,
            "statement": {"domain": r.domain, "key": r.key, "value": r.value},
            "evidence_type": r.evidence_type.value,
            "confidence": r.confidence,
            "confidence_band": confidence_band(r.confidence),
            "created_by": next((t.removeprefix("created_by:") for t in r.tags
                                if t.startswith("created_by:")), "user"),
            "alternatives": [t.removeprefix("alt:") for t in r.tags if t.startswith("alt:")],
            "last_confirmed_at": r.last_confirmed_at,
            "sources": sources,
            "history": chain,
        }

    def history(self, record_id: str) -> list[HumanRecord]:
        """Full supersedes chain, newest first. Nothing is ever dropped."""
        out, cursor = [], self.model.get(record_id)
        out.append(cursor)
        while cursor.supersedes is not None:
            cursor = self.model.get(cursor.supersedes)
            out.append(cursor)
        return out

    # ---------------- Decision Engine feed ----------------

    def decision_inputs(self, subject_id: str) -> dict[str, Any]:
        """Epistemically split feed for the Decision Engine. A weak hypothesis
        must never be treated like a confirmed declaration — the split is the
        contract; composing this with DecisionEngine stays at the caller's
        discretion (same pattern as the rest of the engine)."""
        view = self.living_view(subject_id, include_sensitive=True)
        return {
            "confirmed": view["confirmed"],
            "declared": view["declared"],
            "observations": view["observations"],
            "hypotheses": [(r, r.confidence, confidence_band(r.confidence))
                           for r in view["hypotheses"]],
            "tensions": view["tensions"],
            "missing_critical_information": [],
        }

    def decision_context(self, subject_id: str) -> dict[str, Any]:
        """Gate-grade context for composing a ``DecisionRequest``.

        The evidence-asymmetry rule (ADR-DECISION-002/-005) starts here,
        structurally: only what the user said, confirmed, or what was
        concretely observed is *gate-grade* (may shape goals/constraints a
        caller feeds into the Decision Engine's hard gates). Hypotheses are
        returned in a separate, advisory-only list and MUST NOT be mapped
        onto gate inputs — a weak AI hypothesis never carries the authority
        of a confirmed declaration.
        """
        view = self.living_view(subject_id, include_sensitive=True)
        gate_grade = view["confirmed"] + view["declared"] + view["observations"]
        return {
            "goals": [r for r in gate_grade if r.domain == "goals"],
            "constraints": [r for r in gate_grade if r.domain == "constraints"],
            "values": [r for r in gate_grade if r.domain == "values"],
            "advisory_hypotheses": [
                {"record": r, "confidence_band": confidence_band(r.confidence)}
                for r in view["hypotheses"]],
            "open_tensions": view["tensions"],
        }
