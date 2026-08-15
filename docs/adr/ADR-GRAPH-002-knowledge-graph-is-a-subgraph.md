# ADR-GRAPH-002: The Knowledge Graph Is a Subgraph of the Shared Entity Graph

## Status
Accepted for implementation and further specification. Imported 2026-08-15
per founder review Q11, **verified against the original source docx bytes
2026-08-15** (`Human_OS_Rozszerzenie_Architektury_i_Integracja_v0_2_1.docx`,
founder-provided; filename carries a `v0_2_1` suffix not reflected in the
document's own "0.2" version header). Source: *Rozszerzenie Architektury i
Integracja v0.2*, §3. No content corrections were required.

## Decision
Human OS adopts a single shared Entity Graph. The Knowledge Graph is not a
separate, competing database, but a specialized subgraph describing claims,
sources, evidence, disputes, scopes of validity, and information signatures.

Subgraph classes: **Identity Graph** (people, organizations, accounts, roles
and permissions), **Personal Graph** (goals, values, states, measurements,
preferences, user history), **Knowledge Graph** (claims, sources, evidence,
conflicts, uncertainty), **Decision Graph** (problems, variants, criteria,
recommendations, decisions, effects), **Experiment Graph** (protocols,
interventions, measurements, results, replications), **Project & Resource
Graph** (projects, tasks, resources, costs, documents, suppliers), **World
Graph** (external events, indicators, regulations, trends, dependencies).

Mandatory relation properties across the graph: `relation_id`,
`relation_type` + `schema_version`, `source_entity_id`/`target_entity_id`,
`valid_from`/`valid_to`, `asserted_by`, `evidence_refs`, `confidence`,
`scope`, `access_policy`, `created_at`/`superseded_at`, `provenance_chain`,
and `status` (proposed, active, disputed, superseded, archived).

## Rationale
Layer 3 ("Mapa Wiedzy") becomes the epistemic subgraph of the Entity Graph
and the source validator for the World Model — one graph, specialized views,
instead of parallel stores that can drift apart.

## Consequences
The existing `hos_engine.knowledge_graph` module predates this decision and
implements a standalone graph with a smaller relation model. Aligning it
with the shared Entity Graph (and with
`hos_engine.hub_entity_registry.RelationRegistry`) is future work; the two
models coexist until that alignment is planned explicitly.
