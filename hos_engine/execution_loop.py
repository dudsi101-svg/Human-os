from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from .agent_runtime import ActionReceipt, AgentRuntime, InvocationRequest
from .authority import AuthorityRole, RoleGrantRegistry
from .consent import ConsentRegistry
from .event_store import EventStore
from .hos_core import ContextManager, ContextPackage, EventEngine, ExecutionEvent, ExecutionStatus
from .hub_entity_registry import (
    EntityRegistry,
    HubEntityStatus,
    HubRelation,
    HubRelationType,
    RelationRegistry,
)
from .models import Decision, Proof
from .policy import ProofKernel
from .security_identity import IdentityRegistry, IdentityStatus
from .sqlite_store import SQLiteEventStore


class IntentOutcome(str, Enum):
    REFUSED_IDENTITY = "REFUSED_IDENTITY"
    REFUSED_AUTHORITY = "REFUSED_AUTHORITY"
    REFUSED_CONSENT = "REFUSED_CONSENT"
    REFUSED_ENTITY_NOT_FOUND = "REFUSED_ENTITY_NOT_FOUND"
    REFUSED_CONSTITUTIONAL = "REFUSED_CONSTITUTIONAL"
    REQUIRES_HUMAN_APPROVAL = "REQUIRES_HUMAN_APPROVAL"
    EXECUTED = "EXECUTED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class HumanIntent:
    """The starting point of the execution loop: a human's declared intent
    for an agent to act on a specific Hub entity. See founder continuation
    directive 2026-08-15, §20: HUMAN INTENT -> IDENTITY -> AUTHORITY ROLE ->
    PERMISSION/CONSENT -> CONTEXT -> ENTITY/KNOWLEDGE RETRIEVAL -> AGENT OR
    EXECUTION COMPONENT -> CONSTITUTIONAL/SAFETY CHECK -> HUMAN OR VALIDLY
    DELEGATED APPROVAL -> ACTION -> RECEIPT -> EVENT -> STATE UPDATE ->
    AUDIT/REVIEW.
    """

    subject_id: str
    agent_id: str
    capability_id: str
    action: str
    resource_entity_id: str
    arguments: dict[str, Any] = field(default_factory=dict)
    purpose: str = "unspecified"
    domain: str = "*"
    required_role: AuthorityRole = AuthorityRole.OWNER
    predicted_effects: dict[str, float] = field(default_factory=dict)
    reversibility: float = 0.0
    portability: float = 0.0
    exit_cost: float = 0.0
    limitations: tuple[str, ...] = ()
    human_approval_id: str | None = None
    fulfills_entity_id: str | None = None


@dataclass(frozen=True)
class ExecutionResult:
    """Everything produced while walking a HumanIntent through the loop --
    enough to reconstruct what happened and why. Refusal, at any gate, is a
    first-class outcome here, not an exception."""

    intent_id: str
    outcome: IntentOutcome
    reason: str
    context: ContextPackage | None = None
    proof: Proof | None = None
    receipt: ActionReceipt | None = None
    audit_events: tuple[ExecutionEvent, ...] = ()
    relation: HubRelation | None = None


class ExecutionLoop:
    """Wires the existing, independently-tested Human OS components into one
    coherent, auditable execution path.

    Built 2026-08-15 (founder continuation directive, Phase 3) to satisfy
    that directive's explicit warning: "Do not pretend this loop is
    complete until it is actually integrated and tested." Every gate can
    refuse; a refusal stops the loop before anything is executed or
    persisted, and is returned as an ExecutionResult rather than raised.

    This is a bounded slice, not the full Human OS execution model: it does
    not yet touch the Knowledge Graph (a separate, unreconciled model -- see
    docs/RELATION_VOCABULARY_CROSSWALK.md), and "human approval" here is
    limited to the human_approval_id identifier hos_engine.agent_runtime
    already accepts, not a full approval workflow.

    Event persistence and provenance (2026-08-15, second continuation slice):
    `event_store` accepts either the plain `EventStore` or
    `SQLiteEventStore`. Passing `SQLiteEventStore` gives every persisted
    domain event a SHA-256 hash chain (`verify_chain()`), which is the
    project's existing tamper-evidence mechanism -- prefer it over the plain
    `EventStore` whenever the caller cares about provenance, not just a log.

    Graph integration (2026-08-15, third continuation slice): passing
    `relations` (a `hos_engine.hub_entity_registry.RelationRegistry`) lets a
    `HumanIntent` optionally name a `fulfills_entity_id` -- another Hub
    entity (typically a GOAL) that the resource entity fulfills once the
    action succeeds. The target entity is resolved during ENTITY RETRIEVAL
    (so a bad reference refuses the whole intent before anything executes,
    same as the primary resource entity), and the `REALIZUJE` relation is
    only recorded after a successful STATE UPDATE. This still does not touch
    the Knowledge Graph (hos_engine.knowledge_graph) -- that remains a
    separate, unreconciled model, per docs/RELATION_VOCABULARY_CROSSWALK.md.
    """

    def __init__(
        self,
        *,
        identities: IdentityRegistry,
        roles: RoleGrantRegistry,
        consents: ConsentRegistry,
        contexts: ContextManager,
        entities: EntityRegistry,
        proof_kernel: ProofKernel,
        agent_runtime: AgentRuntime,
        events: EventEngine,
        event_store: EventStore | SQLiteEventStore | None = None,
        relations: RelationRegistry | None = None,
    ) -> None:
        self._identities = identities
        self._roles = roles
        self._consents = consents
        self._contexts = contexts
        self._entities = entities
        self._proof_kernel = proof_kernel
        self._agent_runtime = agent_runtime
        self._events = events
        self._event_store = event_store
        self._relations = relations

    def execute(self, intent: HumanIntent) -> ExecutionResult:
        intent_id = "HOS-INT-" + uuid.uuid4().hex[:12].upper()

        # IDENTITY
        try:
            identity = self._identities.get_identity(intent.subject_id)
        except KeyError:
            return self._refuse(intent_id, IntentOutcome.REFUSED_IDENTITY, f"Unknown identity: {intent.subject_id}")
        if identity.status != IdentityStatus.ACTIVE:
            return self._refuse(
                intent_id, IntentOutcome.REFUSED_IDENTITY,
                f"Identity is {identity.status.value}, not ACTIVE",
            )

        # AUTHORITY ROLE
        if not self._roles.has_role(intent.subject_id, intent.required_role, scope=intent.domain):
            return self._refuse(
                intent_id, IntentOutcome.REFUSED_AUTHORITY,
                f"Identity {intent.subject_id} does not hold role {intent.required_role.value} "
                f"in scope {intent.domain}",
            )

        # PERMISSION / CONSENT
        if not self._consents.authorize(
            subject_id=intent.subject_id,
            grantee_id=intent.agent_id,
            purpose=intent.purpose,
            domain=intent.domain,
            action=intent.action,
        ):
            return self._refuse(
                intent_id, IntentOutcome.REFUSED_CONSENT,
                "No active consent grant covers this purpose/domain/action",
            )

        # CONTEXT
        context = self._contexts.snapshot(intent.subject_id, {
            "intent_id": intent_id,
            "agent_id": intent.agent_id,
            "capability_id": intent.capability_id,
            "resource_entity_id": intent.resource_entity_id,
        })

        # ENTITY / KNOWLEDGE RETRIEVAL
        try:
            entity = self._entities.get(intent.resource_entity_id)
        except KeyError:
            return self._refuse(
                intent_id, IntentOutcome.REFUSED_ENTITY_NOT_FOUND,
                f"Unknown Hub entity: {intent.resource_entity_id}",
                context=context,
            )
        if intent.fulfills_entity_id is not None:
            try:
                self._entities.get(intent.fulfills_entity_id)
            except KeyError:
                return self._refuse(
                    intent_id, IntentOutcome.REFUSED_ENTITY_NOT_FOUND,
                    f"Unknown Hub entity (fulfills_entity_id): {intent.fulfills_entity_id}",
                    context=context,
                )

        # CONSTITUTIONAL / SAFETY CHECK
        proof_subject = {
            "id": entity.entity_id,
            "responsibility_owner_id": intent.subject_id,
            "consent": True,
            "reversibility": intent.reversibility,
            "portability": intent.portability,
            "exit_cost": intent.exit_cost,
            "predicted_effects": intent.predicted_effects,
            "limitations": list(intent.limitations),
        }
        proof = self._proof_kernel.evaluate(proof_subject, "HOS-PRF-" + uuid.uuid4().hex[:12].upper())
        if proof.final_status not in {Decision.APPROVED, Decision.APPROVED_WITH_LIMITS}:
            return self._refuse(
                intent_id, IntentOutcome.REFUSED_CONSTITUTIONAL,
                f"Proof Kernel returned {proof.final_status.value}",
                context=context, proof=proof,
            )

        # AGENT EXECUTION -- HOS Core tracks the execution's own lifecycle;
        # AgentRuntime.evaluate() carries its own HUMAN OR VALIDLY DELEGATED
        # APPROVAL gate (ApprovalMode.HUMAN_REQUIRED) and produces the ACTION
        # + RECEIPT.
        contract = self._events.open(
            goal=f"{intent.action} on {intent.resource_entity_id}",
            owner_id=intent.subject_id,
            context=context,
            required_permissions=(intent.action,),
        )
        self._events.transition(contract.execution_id, ExecutionStatus.IN_PROGRESS)

        request = InvocationRequest(
            request_id="HOS-REQ-" + uuid.uuid4().hex[:12].upper(),
            agent_id=intent.agent_id,
            capability_id=intent.capability_id,
            action=intent.action,
            resource=intent.resource_entity_id,
            arguments=dict(intent.arguments),
            human_approval_id=intent.human_approval_id,
        )
        receipt = self._agent_runtime.evaluate(request)

        if receipt.status == "REQUIRES_HUMAN_APPROVAL":
            self._events.transition(contract.execution_id, ExecutionStatus.BLOCKED, reason=receipt.reason)
            return ExecutionResult(
                intent_id, IntentOutcome.REQUIRES_HUMAN_APPROVAL, receipt.reason,
                context=context, proof=proof, receipt=receipt,
                audit_events=tuple(self._events.log(contract.execution_id)),
            )
        if receipt.status != "EXECUTED":
            self._events.transition(contract.execution_id, ExecutionStatus.FAILED, reason=receipt.reason)
            self._record_domain_event(intent_id, "EXECUTION_DENIED", intent, receipt)
            return ExecutionResult(
                intent_id, IntentOutcome.FAILED, receipt.reason,
                context=context, proof=proof, receipt=receipt,
                audit_events=tuple(self._events.log(contract.execution_id)),
            )

        # STATE UPDATE
        self._entities.transition(entity.entity_id, HubEntityStatus.ACTIVE)

        # GRAPH -- record that the resource fulfills the named goal/entity,
        # only now that the action has actually succeeded.
        relation: HubRelation | None = None
        if intent.fulfills_entity_id is not None and self._relations is not None:
            relation = self._relations.link(
                relation_type=HubRelationType.REALIZUJE,
                source_entity_id=entity.entity_id,
                target_entity_id=intent.fulfills_entity_id,
                asserted_by=intent.subject_id,
            )

        # EVENT
        self._events.transition(contract.execution_id, ExecutionStatus.COMPLETED)
        self._record_domain_event(intent_id, "EXECUTION_COMPLETED", intent, receipt)

        # AUDIT / REVIEW -- the caller gets every intermediate artifact back,
        # so the whole path can be reconstructed after the fact.
        return ExecutionResult(
            intent_id, IntentOutcome.EXECUTED, "Executed",
            context=context, proof=proof, receipt=receipt,
            audit_events=tuple(self._events.log(contract.execution_id)),
            relation=relation,
        )

    def _refuse(
        self,
        intent_id: str,
        outcome: IntentOutcome,
        reason: str,
        *,
        context: ContextPackage | None = None,
        proof: Proof | None = None,
    ) -> ExecutionResult:
        return ExecutionResult(intent_id, outcome, reason, context=context, proof=proof)

    def _record_domain_event(
        self, intent_id: str, event_type: str, intent: HumanIntent, receipt: ActionReceipt,
    ) -> None:
        if self._event_store is None:
            return
        self._event_store.append({
            "id": "HOS-EVT-" + uuid.uuid4().hex[:12].upper(),
            "event_type": event_type,
            "occurred_at": datetime.now(UTC).isoformat(),
            "actor_id": intent.subject_id,
            "subject_ids": [intent.resource_entity_id],
            "payload": {"intent_id": intent_id, "receipt_status": receipt.status},
            "correlation_id": intent_id,
            "immutable": True,
        })
