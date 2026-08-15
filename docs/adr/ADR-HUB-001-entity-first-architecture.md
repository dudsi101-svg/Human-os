# ADR-HUB-001: Human OS Adopts an Entity-First Architecture

## Status
Accepted direction — not yet fully implemented. Imported 2026-08-15 per founder
review Q11 (`docs/FOUNDER_REVIEW_2026-08-15.md`). Source: *HOS Hub Model —
Entity-First v0.1* (20 July 2026), §0.

## Decision
Human OS adopts an Entity-First architecture ("architektura Entity-First").
The fundamental unit of the system is the Entity ("Byt"), not a file, folder,
document, table, or application screen. A document remains a possible
representation of an Entity, but it is not its identity.

The base stack: GENESIS → KERNEL → HUB → KNOWLEDGE GRAPH / MEMORY → MODULES →
APPLICATIONS. Genesis defines identity and rights. Kernel enforces the
lowest-level rules. Hub identifies, links, and orchestrates. The graph and
memory maintain meaning and history.

## Rationale
The HOS Hub acts like a central nervous system. It does not store all data in
one place and does not force its migration. It maintains the identity of
objects, records their locations, recognizes relations, routes queries,
watches over versions, and triggers the appropriate processes.

## Consequences
The organism metaphor helps in understanding the system's function, but it
cannot replace precise technical contracts. Every function of the Hub must
have explicit inputs, outputs, error rules, permissions, and an execution
history.

A first slice — `hos_engine.hub_entity_registry.EntityRegistry` — implements
identity assignment for the six MVP entity types (see ADR-HUB-006). It does
not yet implement the Location & Representation Registry, the Orchestrator,
the Event Ledger, or the Policy & Permission Gateway.
