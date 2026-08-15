# ADR-AUDIT-001: Every Recommendation and Action Must Have a Complete Provenance and Execution Trail

## Status
Accepted for implementation and further specification. Imported 2026-08-15
per founder review Q11, **verified against the original source docx bytes
2026-08-15** (`Human_OS_Rozszerzenie_Architektury_i_Integracja_v0_2_1.docx`,
founder-provided; filename carries a `v0_2_1` suffix not reflected in the
document's own "0.2" version header). Source: *Rozszerzenie Architektury i
Integracja v0.2*, preamble, §2, §12. No content corrections were required.

## Decision
Human OS is moving from a documentation-based model to an operational model:
entities, relations, events, decisions and agents become elements of a
single auditable system.

The Observability & Audit sub-module of HOS Core (ADR-CORE-001) measures
quality, errors, costs, latency, sources used, decisions, and human
interventions. Every execution's minimum contract carries a result plus its
uncertainty and evidence, and a log of events, errors, and approvals — the
concrete mechanism that makes the audit trail happen.

## Rationale
Acceptance criteria for the whole architecture extension include: the
ability to reconstruct the entire path from the source to the recommendation
and the action; and that every agent, signal, forecast, and model has a
persistent identity and a version.

## Consequences
`hos_engine.hos_core.EventEngine` implements a first slice: an immutable
`ExecutionEvent` log per `ExecutionContract`, covering proposal and every
status transition. It does not yet implement cost/latency/source-usage
metrics or the Observability & Audit sub-module's aggregate reporting.
