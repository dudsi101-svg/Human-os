# ADR-CORE-002: A Single Execution Loop Integrates Identity, Authority, Consent, Context, Entity, Constitution, Agent, and Audit

## Status
Accepted, implemented. 2026-08-15, Phase 3 of the founder continuation
directive (`docs/FOUNDER_REVIEW_2026-08-15.md`).

## Decision
`hos_engine.execution_loop.ExecutionLoop` wires the following
independently-built, independently-tested components into one coherent,
auditable path, matching the loop specified in the founder continuation
directive §20:

```
HUMAN INTENT
  -> IDENTITY            (security_identity.IdentityRegistry)
  -> AUTHORITY ROLE       (authority.RoleGrantRegistry)
  -> PERMISSION / CONSENT (consent.ConsentRegistry)
  -> CONTEXT              (hos_core.ContextManager)
  -> ENTITY RETRIEVAL     (hub_entity_registry.EntityRegistry)
  -> CONSTITUTIONAL CHECK (policy.ProofKernel)
  -> AGENT EXECUTION      (agent_runtime.AgentRuntime, its own
                            human-approval gate included)
  -> RECEIPT              (agent_runtime.ActionReceipt)
  -> EVENT                (hos_core.EventEngine + event_store.EventStore)
  -> STATE UPDATE         (hub_entity_registry.EntityRegistry.transition)
  -> AUDIT / REVIEW       (ExecutionResult carries every intermediate
                            artifact back to the caller)
```

Every gate can refuse. A refusal is a first-class `ExecutionResult`
(`IntentOutcome.REFUSED_*`), not an exception, and stops the loop before
anything downstream is executed or persisted -- consistent with the
project-wide "hard gate before scoring, refusal is a valid output" pattern
already used by the Proof Kernel, the Constitution's risk gates, and the
Hub's merge-approval requirement.

## Rationale
The founder continuation directive was explicit that "the next major
milestone is NOT 'more classes' or 'more UI.' It is a coherent, auditable
execution path," and that the loop must not be considered complete "until
it is actually integrated and tested." Building `AuthorityRole` (see
`hos_engine/authority.py`) and this loop was the first point at which
identity, authority, consent, context, entities, the Constitution, and
agent execution were exercised together rather than as isolated modules.

`authority.py` deliberately does not modify `security_identity.py`: per the
Q9 correction, IdentityKind (what a subject technically is) and
AuthorityRole (what authority it holds) are kept as two separate,
independently-revocable axes, joined only by `identity_id`.

## Consequences
This is a bounded slice, not the full Human OS execution model:

- It does not yet touch `hos_engine.knowledge_graph` -- that remains a
  separate, unreconciled model (see
  `docs/RELATION_VOCABULARY_CROSSWALK.md`). Entity retrieval against the
  Hub's `EntityRegistry` is a direct lookup, not a graph traversal.
- "Human or validly delegated approval" is limited to the
  `human_approval_id` identifier `agent_runtime.InvocationRequest` already
  accepted; there is no approval-workflow UI or notification behind it yet.
- `ExecutionLoop` does not yet call `hos_engine.policy.ProofKernel` with a
  richer subject shape than the existing `action.schema.json`-style fields;
  Decision/Recommendation Engine (Layer 5, ADR still unbuilt) is not
  involved.

**Update, same day (event persistence):** `event_store` now accepts either
`EventStore` or `SQLiteEventStore` -- passing the latter gives every
persisted domain event a verifiable SHA-256 hash chain, closing the "event
persistence" and "provenance" items from the founder continuation
directive's progressive-integration list. `EventEngine`'s in-memory
execution-lifecycle log is unaffected; the two remain separate as
originally documented in `hos_core.py`.

**Update, same day (graph):** `ExecutionLoop` now optionally accepts a
`relations: RelationRegistry`. A `HumanIntent` may name a
`fulfills_entity_id` (typically a GOAL entity); it is resolved during
ENTITY RETRIEVAL -- an unknown reference refuses the whole intent before
anything executes -- and a `REALIZUJE` relation from the resource entity to
it is recorded only after a successful STATE UPDATE. This closes the
"graph" item from the same list. It still does not touch
`hos_engine.knowledge_graph`, which remains a separate, unreconciled model.

Covered by 14 integration tests (`tests/test_execution_loop.py`) plus 7
tests for `authority.py` (`tests/test_authority.py`): the full happy path
with a complete audit trail, refusal at every named gate (unknown identity,
suspended identity, missing authority role, missing consent, unknown
entity, unknown `fulfills_entity_id`, constitutional violation, a
capability that requires human approval, and an agent-level denial that
still produces a durable domain event); against `SQLiteEventStore`
specifically, that executed intents chain correctly and `verify_chain()`
passes while refused intents never reach the chain; and against
`RelationRegistry`, that a successful execution with `fulfills_entity_id`
set records exactly one `REALIZUJE` relation while an execution without it
records none.
