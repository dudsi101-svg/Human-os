# ADR-HUB-006: Semantics and Contracts Precede Interface Design

## Status
Accepted direction — not yet fully implemented. Imported 2026-08-15 per
founder review Q11. Source: *HOS Hub Model — Entity-First v0.1*, §10.1–§10.3.

## Decision
First stabilize the semantics, then the technical schema, and only later the
interface. Otherwise the application screen begins to accidentally define
the system's architecture.

Open items still to be established: a formal catalog of Entity types, rules
for permissible relations, an identifier format, an event model,
confidentiality levels, and the boundaries between semantic memory and
personal data.

## Rationale
The next artifact after this ADR should be the HOS Entity & Relation Schema
v0.1 — a dictionary of types, fields, constraints, relations, statuses, JSON
examples, and validation rules — the first document directly translatable
into a database and an API.

## Consequences
Per founder review Q6, `hos_engine.hos_core` (HOS Core) and
`hos_engine.hub_entity_registry` (Hub Entity/Relation Registry MVP, six entity
types per ADR-IMPL-001) were built as a first slice on 2026-08-15, following
this sequencing: semantics and code contracts first, no new interface work
was started alongside them.
