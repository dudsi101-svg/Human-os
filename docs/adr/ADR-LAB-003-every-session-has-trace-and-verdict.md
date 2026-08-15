# ADR-LAB-003: Every Lab Session Carries a Trace and a Tester Verdict

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 per founder-provided
source `Human_OS_Lab_Specyfikacja_i_Interface_v0_1.docx`. See
`docs/FOUNDER_REVIEW_2026-08-15.md` for provenance.

## Decision
Every Lab test session produces both a full execution trace (TRACE & AUDIT
module, source §2: "Pełny ślad źródeł, decyzji, narzędzi, kosztów, błędów i
zgód") and an explicit tester verdict recorded on the experiment itself
(`tester_verdict`: `pass` / `partial` / `fail` / `blocked`, plus a
`confidence` score 0–100 and `evidence_refs`, source §5).

## Rationale
The tester is explicitly not a passive recipient but simultaneously plays
user, observer, reviewer, and co-designer (source §3). A verdict without a
traceable "why" would not satisfy the project's existing auditability
standard — the same standard that requires `SQLiteEventStore`'s hash chain
and `ExecutionResult.audit_events` in the already-implemented execution loop
to carry every intermediate artifact back to the caller.

## Consequences
A future Lab backend needs an experiment schema with at minimum:
`experiment_id`, `title`, `hypothesis`, `module_under_test`, `scenario`,
`input_data_class`, `risk_class`, `expected_result`, `success_metrics`,
`actual_result`, `tester_verdict`, `confidence`, `evidence_refs`, `decision`
(`repeat` / `change` / `reject` / `promote`), `version` (source §5, full
field table). None of this is implemented in `hos_engine` yet — it does not
map onto any existing schema in `schemas/`.
