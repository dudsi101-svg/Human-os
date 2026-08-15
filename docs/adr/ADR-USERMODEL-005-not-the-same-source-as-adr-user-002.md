# ADR-USERMODEL-005: This Document Is Not the Source Behind ADR-USER-002 — Two Sibling Specifications, Not One

## Status
Informational — flags a source-provenance question for founder resolution,
does not itself decide anything. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_4_Model_Uzytkownika_i_Cyfrowy_Profil_v0_1.docx`. See
`docs/FOUNDER_REVIEW_2026-08-15.md`, "Czwarta tura" section, and
`docs/LAYER_4_USER_MODEL_DIGEST.md` §9 for the full comparison this ADR
summarizes.

## Decision
`ADR-USER-002` ("The User Model Evolves Into a Human Digital Twin...") cites
its source as `Human_OS_Rozszerzenie_Architektury_i_Integracja_v0_2_1.docx`
§6 — a **different file** from this one. This document (`Warstwa 4`) never
uses the term "Cyfrowy bliźniak"/"Digital Twin" anywhere (confirmed by
full-text search) — it names itself "Model Użytkownika i Cyfrowy Profil
Rozwojowy" and defines "Cyfrowy profil rozwojowy" narrowly as one
presentational layer (R8) of its own nine-row architecture, not a synonym
for the whole model.

Concrete structural differences from `ADR-USER-002`'s nine named components
(Identity & Roles, Goals & Values, State Model, Behavior Model, Capability
Model, Decision Style, Project & Financial Context, Social Context,
Reflective/Symbolic Layer) and five operating modes (Descriptive,
Explanatory, Predictive, Prescriptive, Reflective):
- This document has no matching "nine components" list or "five modes"
  list at all — it organizes instead around the R0–R8 architecture plus a
  flat 24-object ontology (`ADR-USERMODEL-001`).
- Partial conceptual overlap exists for most components (e.g. State Model ≈
  R6 + `State` object, though the named dimensions differ: ADR-USER-002 has
  sleep/energy/load/mood/readiness/context, this document's §17.1 has goal
  significance/energy/time/competence/confidence/support/risk/stability).
  "Capability Model" and "Decision Style" have **no clear named
  counterpart** in this document at all.
- The **Reflective/Symbolic Layer is the one component with a strong,
  near-verbatim match** — this document's §25 "epistemic firewall"
  language is functionally identical to ADR-USER-002's description and to
  the same firewall pattern already confirmed across Layers 3, 5, and 6
  (`ADR-KNOWLEDGE-005`).
- Shared philosophy: both open with near-identical "model is a map, not the
  person" statements, and both grant full verify/contest/correct/delete
  rights — but shared philosophy is not shared authorship, and should not
  be used to infer the two documents are the same specification.

## Rationale
Per this project's `02_Source_Truth_Protocol` (no single artifact is
supreme, conflicts are preserved not silently resolved): finding two
documents about the same general topic with overlapping but non-identical
structure is exactly the situation that protocol exists for. Silently
treating this document as "confirmation" of `ADR-USER-002`, or silently
treating `ADR-USER-002` as superseded by this one, would both be
inappropriate — they are more likely two independently-authored,
mutually-compatible-but-not-identical specifications from the same broader
project.

## Consequences
No ADR content should be merged or rewritten based on this discovery
without an explicit founder decision — this matches the project's standing
escalation rule ("a major source would be deprecated/replaced"). Until that
decision is made: `ADR-USER-002` continues to describe its own source
faithfully; `ADR-USERMODEL-001..004` describe this document faithfully;
neither should be treated as the authoritative or superseding version of
"the User Model" without the founder choosing (a) keep both as distinct,
cross-referenced specifications, or (b) explicitly reconcile them into one,
with a recorded governance decision per `GOVERNANCE.md`.
