# ADR-IMPL-001: Stabilize the Schema of Entities and Events First, Then Agents, Then Interfaces

## Status
Accepted for implementation and further specification. Imported 2026-08-15
per founder review Q11, **verified against the original source docx bytes
2026-08-15** (`Human_OS_Rozszerzenie_Architektury_i_Integracja_v0_2_1.docx`,
founder-provided; filename carries a `v0_2_1` suffix not reflected in the
document's own "0.2" version header). Source: *Rozszerzenie Architektury i
Integracja v0.2*, §10–§11. No content corrections were required.

## Decision
An eight-stage implementation sequence, each stage gated by "consistency
audit, reproducibility test, and ADR approval":

1. **Semantic schema** — HOS Entity & Relation Schema v0.1; Event Schema;
   Access Policy Schema; identifiers and versioning.
2. **Minimal Core** — Event Ledger, Context Manager, Permission Engine, a
   simple Workflow Engine, and audit.
3. **MVP Hub + Graph** — entity/relation/location registry, duplicate
   resolution, and decision tracing.
4. **Digital Twin MVP** — goals, values, states, measurements, projects,
   snapshots, and consents.
5. **Agent Network MVP** — Research, Project Operator, Data Steward, and
   Critic agents at autonomy levels A1–A2.
6. **World Model MVP** — three pilot domains: finance, health/science, and
   the legal environment.
7. **Prediction and proactivity** — Drift, Risk, and Opportunity Signals
   with manual approval.
8. **Product interface** — HOS Hub dashboard, dependency graph, decision
   inbox, and consent center.

Next mandatory artifact: **HOS Entity, Relation & Event Schema v0.1** — a
dictionary of entity, relation, and event types; admissibility rules;
identifiers; statuses; confidentiality levels; JSON examples; validation
rules; migration procedures; error contracts; and a minimal API.

## Rationale
This is "the first artifact directly translatable into a database, a
backend, and tests" — sequencing schema before agents before interfaces
prevents the application screen from accidentally defining the system's
architecture (see ADR-HUB-006).

## Consequences
Acceptance criteria for the whole extension: no conflict with the existing
layer numbering and responsibilities (see ADR-ARCH-002); ability to
reconstruct the entire path from source to recommendation and action; every
agent, signal, forecast and model has a persistent identity and version; the
user can see, contest, and revoke the use of personal data; the World Model
does not hide its date, source, scope, or error; the system can operate
without automatically executing high-risk actions; the interface remains a
representation of the architecture, not its source.

On 2026-08-15, per founder review Q5/Q6, work began on stage 1 (partial —
`hos_engine.hos_core` and `hos_engine.hub_entity_registry` implement code
directly, ahead of a formally published HOS Entity, Relation & Event Schema
document). The formal schema artifact this ADR calls for has not yet been
written; the code should be treated as provisional until it exists.
