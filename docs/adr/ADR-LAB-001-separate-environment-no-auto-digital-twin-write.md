# ADR-LAB-001: Human OS Lab Is a Separate Environment That Never Auto-Writes to the Human Digital Twin

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 per founder-provided
source `Human_OS_Lab_Specyfikacja_i_Interface_v0_1.docx` (20 July 2026, status
"prototyp operacyjny"). See `docs/FOUNDER_REVIEW_2026-08-15.md` for provenance.

**Naming note:** "Human OS Lab" (this document, a tester-facing sandbox product
with its own UI) is a distinct concept from the code-level "simulation
laboratory" already implemented in `hos_engine/simulation.py` and documented in
`ADR-0006-simulation-laboratory.md` (a what-if scenario engine used inside
`evaluate_action`). The two share the word "lab"/"laboratorium" in casual
conversation but are not the same system — do not merge them without a
separate reconciliation pass, matching the project's existing pattern for
other same-name-different-model concepts (see `docs/RELATION_VOCABULARY_CROSSWALK.md`).

## Decision
Human OS Lab is a dedicated, walled-off research-and-development environment
("wydzielone środowisko badawczo-rozwojowe"). Its purpose is not to imitate a
finished product but to accelerate the system's learning while preserving
auditability, reversibility, and user control. No result produced inside the
Lab automatically becomes truth, a permanent user profile, or a production
rule. Moving an element from the Lab into the core system requires a separate
decision, acceptance criteria, and a migration record (ADR-LAB-005).

## Rationale
Source, §1.1 ("Zasada nadrzędna"): "Żaden wynik z Labu nie staje się
automatycznie prawdą, trwałym profilem użytkownika ani regułą produkcyjną."
This mirrors the project-wide pattern already used elsewhere in the codebase
(e.g. the Hub's `EntityRegistry.merge()` requiring explicit `reason`/
`evidence`/`approved_by`, or `ExecutionLoop`'s refusal-is-first-class gates):
nothing crosses a trust boundary silently.

## Consequences
No code exists yet for Human OS Lab. When it is built, its data layer must be
architecturally incapable of writing to the Human Digital Twin / Hub entity
store by default — a promotion path (ADR-LAB-005) is the only sanctioned
route, and it must be explicit and auditable.
