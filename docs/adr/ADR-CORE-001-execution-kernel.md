# ADR-CORE-001: HOS Core Is Established as the Executive Kernel Below the HOS Hub

## Status
Accepted for implementation and further specification. Imported 2026-08-15
per founder review Q6/Q11, **verified against the original source docx bytes
2026-08-15** (`Human_OS_Rozszerzenie_Architektury_i_Integracja_v0_2_1.docx`,
founder-provided). Source: *Rozszerzenie Architektury i Integracja v0.2*
(20 July 2026, internal version field; the filename carries a `v0_2_1` suffix
not reflected in the document's own header — noted, not resolved), §1–§2. The
original secondhand reconstruction matched the source text closely; no
content corrections were required.

## Decision
HOS Core is adopted as the system's technical kernel. It operates below the
Hub and the domain modules, occupying L1 in the stack (L0 Genesis/
Constitution → L1 HOS Core → L2 HOS Hub → L3 Entity Graph → L4 domain
modules → L5 Intelligence Fabric → L6 World Context → L7 Applications &
Interfaces). Its task is to safely and deterministically run processes in
accordance with the Constitution, policies, and the current context.

Eight named sub-modules: **Event Engine** (records and distributes events;
idempotency, ordering, retries, audit trail), **Context Manager** (builds an
explicit context package: user, goal, time, domain, constraints, consents,
sources), **Memory Controller** (session/working/long-term/semantic/sensitive
memory; retention and expiry), **Policy & Permission Engine** (consents,
access scope, risk class, data minimization, least privilege), **Workflow
Engine** (versioned processes, steps, gates, exceptions, compensations, human
approvals), **Scheduler** (time-based, recurring, conditional, priority
tasks), **AI Orchestrator Runtime** (model/agent selection, cost limits,
quality level, validation), **Observability & Audit** (quality, errors,
costs, latency, sources, decisions, human interventions).

Minimum execution contract every process must carry: `execution_id` and
`correlation_id`; an explicit goal and goal owner; a versioned context
package; required consents and permissions; a step plan and abort criteria;
a time, cost, and data budget; a result plus its uncertainty and evidence;
and a log of events, errors, and approvals.

## Rationale
Cross-cutting principle of responsibility: HOS Core does not define truth;
the HOS Hub does not take ownership of sources; the graph does not make
decisions; an agent does not gain permissions merely because it is capable
of performing a task; the interface must not accidentally define the
system's semantics.

## Consequences
`hos_engine.hos_core` implements a first slice of two of the eight
sub-modules: `ContextManager` (versioned context packages per subject) and
`EventEngine` (the minimum execution contract as `ExecutionContract`, with
lifecycle events logged per execution). Memory Controller, Policy &
Permission Engine, Workflow Engine, Scheduler, AI Orchestrator Runtime, and
Observability & Audit are not yet implemented as HOS Core components — note
that `hos_engine.event_store.EventStore` (JSONL/SQLite persistence) already
exists but serves a different purpose (durable storage of arbitrary domain
events) than this module's `EventEngine` (execution-lifecycle tracking); the
two are complementary, not duplicates.
