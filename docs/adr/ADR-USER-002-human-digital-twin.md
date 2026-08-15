# ADR-USER-002: The User Model Evolves Into a Human Digital Twin, But Does Not Become a Definition of the Person

## Status
Accepted for implementation and further specification. Imported 2026-08-15
per founder review Q11, **verified against the original source docx bytes
2026-08-15** (`Human_OS_Rozszerzenie_Architektury_i_Integracja_v0_2_1.docx`,
founder-provided; filename carries a `v0_2_1` suffix not reflected in the
document's own "0.2" version header). Source: *Rozszerzenie Architektury i
Integracja v0.2*, §6. No content corrections were required.

**Merged 2026-08-15** into the Warstwa 4 user-model specification per
explicit founder decision — see `ADR-USERMODEL-006` for the merge and the
component-mapping table. This document's Decision/Rationale/Consequences
below are left intact as the historical record of this source; new work
should build against `ADR-USERMODEL-001`'s R0–R8 structure via
`ADR-USERMODEL-006`'s mapping, not against this ADR's nine components
directly.

## Decision
The Digital Twin ("Cyfrowy bliźniak") is an operational, temporal
representation of the user. It is not the user's definition, diagnosis, or a
scoring of their worth. Every conclusion it produces must be verifiable,
contestable, correctable, and deletable.

Components: **Identity & Roles**, **Goals & Values**, **State Model** (sleep,
energy, load, mood, readiness, context), **Behavior Model** (habits and
patterns, explicitly without deterministic labels), **Capability Model**,
**Decision Style**, **Project & Financial Context**, **Social Context** (only
to the extent of consent), and a **Reflective/Symbolic Layer** (astrology,
Human Design, archetypes and traditions as an explicitly optional reflective
layer).

Operating modes: **Descriptive**, **Explanatory**, **Predictive**,
**Prescriptive**, **Reflective**.

## Rationale
"Model jest mapą człowieka, nie człowiekiem" — a model is a map of the
person, never the person. The verify/contest/correct/delete rights are what
keep the Twin from hardening into a fixed profile.

## Consequences
`hos_engine.human_model.HumanModel` is the closest existing implementation —
a flat, per-domain `HumanRecord` store with evidence type and a contestable
`RecordStatus`. It does not implement the nine named component models, the
five operating modes, or the optional Reflective/Symbolic Layer. The name
"Human Digital Twin" does not appear in code as of this ADR's import.
