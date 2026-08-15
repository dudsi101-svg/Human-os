# ADR-KNOWLEDGE-003: The Knowledge Graph Has a Closed Catalog of 13 Node Types and 9 Named Relations

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_3_Mapa_Wiedzy_i_Sygnatura_Informacji_v0_1.docx`, §21
("Graf wiedzy i sieć relacji"). See `docs/FOUNDER_REVIEW_2026-08-15.md`,
"Czwarta tura" section, for provenance. Newly formulated — the source has no
ADR numbering of its own.

## Decision
The Knowledge Map's graph has a closed catalog of node types (§21.1):
claim, source, intervention, protocol, outcome, mechanism, risk,
contraindication, population, metric, domain, user/cohort (kept separated
and protected), version, and editorial decision — plus nine named edge
relations (§21.2): **POPIERA** (supports), **OSŁABIA** (weakens),
**PRZECZY** (contradicts), **WARUNKUJE** (conditions), **WYJAŚNIA**
(explains), **RYZYKUJE** (risks), **WCHODZI_W_INTERAKCJE** (interacts
with), **JEST_WERSJA** (is a version of), **WYNIKA_Z** (follows from).
Critical conditions (population, dose, time, goal, contraindications) must
be modeled as comparable objects/fields, not free-text notes (§21.3).

## Rationale
A typed relation catalog is what lets the Decision Engine (Layer 5) and
Experiment Engine (Layer 6) reason over the graph programmatically rather
than re-parsing prose — the same justification already used in this
repository for `hub_entity_registry.HubRelationType`'s 17 typed verbs.

## Consequences
This is a concrete, checkable gap against the current implementation:
`hos_engine.knowledge_graph.GraphNode.node_type` and
`GraphEdge.relation_type` are plain, unconstrained `str` fields — any node
or edge type is programmatically permitted, with no enforcement of this
13-type/9-relation catalog. This contrasts with `hub_entity_registry.py`,
which *does* use a typed enum (`HubRelationType`) for its 17 relations. This
is not necessarily a defect — `knowledge_graph.py` may be an intentionally
general primitive awaiting specialization — but it is a documented gap the
project should track, analogous to how `CLAUDE.md` already marks
`hub_entity_registry.EntityRegistry` as an `MVP_IMPLEMENTED_SUBSET` against
the full Hub spec.

**Update 2026-08-15 (Phase 3):** the catalog now exists in code as
`KnowledgeNodeType` (13 values) and `KnowledgeRelationType` (9 values) in
`knowledge_graph.py`, with an opt-in
`KnowledgeGraph.validate_against_catalog()` that *reports* departures as
`CatalogViolation` records rather than raising — existing untyped graphs
keep working, per the project-wide surface-don't-silently-correct error
contract. Making the catalog mandatory (rejecting rather than reporting)
remains a future decision.
