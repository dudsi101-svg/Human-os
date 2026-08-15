# ADR-HUB-003: A Relation Is a First-Class Record With Its Own Provenance and History

## Status
Accepted direction — not yet fully implemented. Imported 2026-08-15 per founder
review Q11. Source: *HOS Hub Model — Entity-First v0.1*, §4.1–§4.3, §5.2.

## Decision
A relation ("Relacja") is not a mere tag. It is its own record with a type,
direction, source, confidence level, temporal scope, author, and history.
This lets the system distinguish an established fact from a supposition, a
similarity, a succession, or a dependency.

Minimum relation types: is-a-type-of (`jest_typem`), belongs-to
(`należy_do`), concerns (`dotyczy`), originated-from (`powstał_z`),
represents (`reprezentuje`), supports (`wspiera`), contradicts (`przeczy`),
depends-on (`zależy_od`), causes (`powoduje`), precedes (`poprzedza`),
updates (`aktualizuje`), replaces (`zastępuje`), measures (`mierzy`),
fulfills (`realizuje`), was-approved-by (`został_zatwierdzony_przez`),
is-stored-in (`jest_przechowywany_w`), and is-a-view-of (`jest_widokiem`).

A relation can be valid from a start to an end date and can lose currency
without being deleted — enabling reconstruction of the graph's state on a
given day and tracing the evolution of a decision, rather than treating old
determinations as current.

## Rationale
The Relation Registry indexes relations and their evidence, enabling review
of the graph, and detection of orphaned Entities, conflicts, and unconfirmed
relations.

## Consequences
Relations carry the same rigor (provenance, confidence, temporality) as
Entities themselves. Per founder review Q8, this generic graph-edge model is
kept distinct from the repository's existing `schemas/relation.schema.json`
(an interpersonal-relationship model with `trust`/`reciprocity`/`boundaries`)
under different names, rather than merging the two.

`hos_engine.hub_entity_registry.RelationRegistry` implements a first slice:
sixteen named relation types, per-relation confidence and a `valid_from`/
`valid_to` window, and orphan detection. Full temporal-reconstruction queries
and conflict detection are not yet implemented.
