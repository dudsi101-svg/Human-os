# ADR-EXP-003: Experiment Objects Are Independently Versioned and Never Silently Merged

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_6_Silnik_Eksperymentow_Monitorowania_i_Postepu_v0_1_2.docx`
("Warstwa 6"), §4 ("Ontologia obiektów eksperymentalnych"). See
`docs/FOUNDER_REVIEW_2026-08-15.md`, "Trzecia tura" section, for provenance.
Newly formulated from the source's ontology section, which has no ADR
numbering of its own.

## Decision
Layer 6 defines fifteen distinct experimental object types — `Experiment`,
`Hypothesis`, `Protocol`, `EligibilityRule`, `Metric`, `BaselineWindow`,
`ExposureEvent`, `Observation`, `ContextEvent`, `SafetyEvent`,
`ProtocolDeviation`, `AnalysisPlan`, `Result`, `PostExperimentDecision`,
`CommunityContribution` (§4, full field table in
`docs/FOUNDER_REVIEW_2026-08-15.md`'s linked digest). Every object carries a
stable identifier, creation time, source, version, and change history
(§4.1). Editing source data can never silently change a historical decision
— it must create a new version and a new analysis instead.

**Zakaz ukrytego scalania (§4.2, ban on hidden merging):** self-report,
device measurement, lab result, model prediction, and expert interpretation
remain separate objects. The system may display agreement or conflict
between them, but must never collapse them into a single number without
preserving provenance.

## Rationale
This mirrors, at finer grain, the same provenance discipline
`hub_entity_registry.EntityRegistry.merge()` already enforces for Hub
entities (explicit `reason`/`evidence`/`approved_by`, a `MergeRecord`, the
superseded entity marked `SUPERSEDED` rather than deleted) — Layer 6 applies
it to measurement data specifically, where the temptation to silently
average away disagreement between a wearable reading and a self-report is
strongest.

## Consequences
`hos_engine.hub_entity_registry.HubEntityType.EXPERIMENT` currently exists
only as a bare label in the six-type MVP subset (see ADR-HUB-006) — it has
no dedicated fields and does not implement this fifteen-object ontology or
its versioning/no-silent-merge rules. Building a real Layer 6 experiment
model is future work; when it happens, it should reuse the
`MergeRecord`-style provenance pattern already proven in
`hub_entity_registry.py` rather than inventing a new one.
