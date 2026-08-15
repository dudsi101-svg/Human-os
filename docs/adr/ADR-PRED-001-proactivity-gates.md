# ADR-PRED-001: Proactivity Requires Consent, a Quality Threshold, and Control of Attention Cost

## Status
Accepted for implementation and further specification. Imported 2026-08-15
per founder review Q11, **verified against the original source docx bytes
2026-08-15** (`Human_OS_Rozszerzenie_Architektury_i_Integracja_v0_2_1.docx`,
founder-provided; filename carries a `v0_2_1` suffix not reflected in the
document's own "0.2" version header). Source: *Rozszerzenie Architektury i
Integracja v0.2*, §7–§7.1. No content corrections were required.

## Decision
Human OS may initiate signals without the user asking, but only within the
bounds of consent, significance, and attention cost. The system is meant to
detect deviations, risks, opportunities, and conflicts — not to produce a
constant stream of alarms.

Signal types: **Observation**, **Pattern**, **Risk Signal**, **Opportunity
Signal**, **Conflict Signal**, **Drift Signal**, **Forecast**.

Six proactivity gates every signal must pass: Has the user consented to this
type of signal? Does the signal have sufficient quality and currency? Does
the benefit justify the attention cost and the risk of error? Does the
message show its own uncertainty and the option to ignore it? Is the action
reversible? Is human or specialist approval required?

## Rationale
The six gates are themselves the stated limitation — no proactive signal may
bypass them, regardless of how confident the system is in its own detection.

## Consequences
Not implemented. No proactive-signal mechanism exists in `hos_engine` as of
2026-08-15. When built, it should sit downstream of the World Model
(ADR-WORLD-001) and the Digital Twin (ADR-USER-002), per the dependency order
implied by ADR-IMPL-001's roadmap.
