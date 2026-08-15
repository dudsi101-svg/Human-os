# ADR-HUB-004: The Hub Federates Data Instead of Forcing a Single Store

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 per founder
review Q11. Source: *HOS Hub Model — Entity-First v0.1*, §1.2–§1.3.

## Decision
The Hub knows where a data source is located, but it does not pretend to own
it. Source data may remain in Google Drive, a database, GitHub, the user's
device, or a partner system. The Hub stores only what is necessary for
identification, control, and linking.

## Rationale
A single source of truth does not mean a single store. It means an
unambiguous answer as to which record is canonical for a given aspect of an
Entity, and which other representations are copies, views, exports, or
derivative materials.

## Consequences
This shifts complexity onto the Hub's Location & Representation Registry
(ADR-HUB-002) to correctly track canonical-vs-derivative status across
federated stores. Not yet implemented — the current
`hos_engine.hub_entity_registry` module has no location/representation
tracking.
