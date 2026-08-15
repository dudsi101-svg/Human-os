# ADR-HUB-002: A Document Is a Representation of an Entity, Not Its Identity

## Status
Accepted direction — not yet fully implemented. Imported 2026-08-15 per founder
review Q11. Source: *HOS Hub Model — Entity-First v0.1*, §3.1, §5.3.

## Decision
An Entity's ID must be globally unique and immutable. Names, titles,
locations, and classifications may change without loss of continuity.
Recommended logical format: `HOS-ENT-<UUID>`, with an optional human-readable
alias.

## Rationale
The Location & Representation Registry indicates where the source data
exists and which representations are available: a DOCX document, a database
record, a spreadsheet, a graphic, a commit, an email message, an application
view, or an embedding. The Entity's identity is decoupled from any single
representation.

## Consequences
A document (or any other representation) can move, be replaced, or exist in
multiple forms without the underlying Entity losing continuity.
`hos_engine.hub_entity_registry.EntityRegistry` assigns the `HOS-ENT-`
identifier on registration; the Location & Representation Registry itself is
not yet implemented.
