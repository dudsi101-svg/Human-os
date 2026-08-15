# ADR-LAB-005: Promotion from Lab to Core Requires an Explicit, Reversible Gate

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 per founder-provided
source `Human_OS_Lab_Specyfikacja_i_Interface_v0_1.docx`. See
`docs/FOUNDER_REVIEW_2026-08-15.md` for provenance.

## Decision
Nothing built or tested in Human OS Lab reaches the core system (Core/Hub)
without passing an explicit PROMOTION GATE (source §2, §8). The gate requires
all of the following before migration:
- an unambiguous module contract and ownership of responsibility;
- critical tests passed and blocking bugs closed;
- sources, versions, data, and the execution trace are reproducible;
- negative scenarios and missing-data cases have been examined;
- the interface discloses uncertainty and does not hide automation;
- the product owner has approved both the migration and a withdrawal
  ("wycofanie"/rollback) plan;
- data migration, monitoring, and rollback capability are prepared.

## Rationale
This gate is the Lab-specific application of the same non-silent-crossing
principle already used by `hub_entity_registry.EntityRegistry.merge()`
(requires `reason`/`evidence`/`approved_by`, produces a `MergeRecord`,
never deletes the superseded entity) and by `ExecutionLoop`'s refusal gates
(refusal is a first-class, auditable outcome, never a silent skip).

## Consequences
Whenever a Lab-to-Core promotion mechanism is eventually built, it should be
modeled after the existing `MergeRecord`/`merge()` pattern in
`hub_entity_registry.py` rather than invented from scratch — both require the
same shape of evidence: what changed, why, on whose authority, and how to
undo it.
