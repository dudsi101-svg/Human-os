# ADR-ARCH-002: New Execution-Platform Components Do Not Change the Existing Domain-Layer Numbering

## Status
Accepted for implementation and further specification. Imported 2026-08-15
per founder review Q11 (flagged during extraction, not originally named in
the founder's list of 14 — included because it directly resolves a
numbering question raised in the Reconstruction Audit's Conflict Map, §6),
**verified against the original source docx bytes 2026-08-15**
(`Human_OS_Rozszerzenie_Architektury_i_Integracja_v0_2_1.docx`,
founder-provided; filename carries a `v0_2_1` suffix not reflected in the
document's own "0.2" version header). Source: *Rozszerzenie Architektury i
Integracja v0.2*, §0. No content corrections were required.

## Decision
Layers 5, 6, and 7 (Decision Engine, Experiment Engine, Collective
Intelligence — from *Architektura v0.1*) keep their existing numbers and
responsibilities. The new execution-platform components — HOS Core, HOS Hub,
Entity Graph, Agent Network, World Model, Predictive & Proactive Layer — are
not assigned competing layer numbers. They form a separate execution stack
(L0–L7) that sits alongside and beneath the semantic layers, not on top of
them.

## Rationale
Avoids the numbering collision that would otherwise occur if the same
integers were reused for two different classification schemes — one semantic
(what the layer is about), one architectural (where the component sits in
the execution stack).

## Consequences
The Reconstruction Audit (§2, §6) documented three layer-numbering schemes
in the archive that had never been reconciled: *Architektura v0.1*'s seven
semantic layers, this extension's eight-layer execution stack, and the live
repository's four-stage `ECOSYSTEM.md` chain. This ADR resolves the
relationship between the first two directly: they compose rather than
compete. Reconciling both against `ECOSYSTEM.md`'s chain remains open.
