# ADR-LAB-002: Human OS Lab Defaults to Synthetic Data

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 per founder-provided
source `Human_OS_Lab_Specyfikacja_i_Interface_v0_1.docx`. See
`docs/FOUNDER_REVIEW_2026-08-15.md` for provenance.

## Decision
Human OS Lab defaults to synthetic data ("Domyślnie wykorzystywane są dane
syntetyczne"). The Lab's data model explicitly separates three classes for any
experiment: `synthetic`, `anonymized`, and `personal-lab` (source §5, field
`input_data_class`). Personal data may only enter the Lab as an explicit,
higher-risk choice, not the default path.

## Rationale
Source §2 assigns this separation to a dedicated module, SANDBOX DATA
("Dane syntetyczne, kopie zanonimizowane i izolowane zestawy testowe"),
independent from production data stores. Source §7 ties data class to a risk
class (R0–R4): R0–R1 use no personal data at all; R2 permits personal data
inside the Lab but restricted to analysis/simulation only; R3 requires
per-action approval; R4 (health, finance, legal, safety, or hard-to-reverse
actions) is never auto-executed by the Lab.

## Consequences
Any future Lab implementation must make `input_data_class` and `risk_class`
mandatory, first-class fields on every experiment record, not optional
metadata — matching how `hos_engine`'s existing modules (e.g. the Proof
Kernel's PROOF-008 portability/exit test, `hub_entity_registry`'s Hub entity
statuses) already treat risk and provenance as structural, not decorative.
