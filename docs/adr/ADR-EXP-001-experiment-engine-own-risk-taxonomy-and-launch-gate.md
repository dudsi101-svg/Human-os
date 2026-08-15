# ADR-EXP-001: The Experiment Engine (Layer 6) Defines Its Own Risk Taxonomy and a Mandatory Pre-Launch Explainability Gate

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_6_Silnik_Eksperymentow_Monitorowania_i_Postepu_v0_1_2.docx`
("Warstwa 6", version "0.1 – model bazowy", dated 2026-07-20, status "Projekt
do iteracji, pilotażu, walidacji metodologicznej i audytu bezpieczeństwa" —
i.e. explicitly unvalidated). This document is one of the six sources
previously listed as "confirmed to exist, content unavailable" in Founder
Review Q12 — its bytes are now available. See
`docs/FOUNDER_REVIEW_2026-08-15.md`, "Trzecia tura" section, for provenance.
The document itself contains no ADR-numbered decisions — the ADR-EXP series
is newly formulated from its axioms (§1), reference architecture (§39), and
acceptance criteria (§47), not extracted verbatim from an existing ADR list.

**Naming note:** the source document's coded scales (XP0–XP8, SE0–SE4, EC0–EC5,
BL0–BL5, MQ0–MQ5, PF0–PF5, DQ0–DQ5, CA0–CA5, PE0–PE5) are a **separate
taxonomy from the Constitution's R0–R4 risk scale** (`constitution/README.md`
Ch.6). Do not conflate SE0–SE4 (Layer 6 safety-event severity) with R0–R4
(constitutional risk class) — they classify different things at different
layers, the same pattern already documented for `AuthorityRole` vs.
`IdentityType` in `CLAUDE.md`.

## Decision
Layer 6 (the Experiment Engine) governs how a chosen recommendation becomes
a safely executed, monitored, and evaluated personal experiment (N-of-1
style). It defines eleven independent coded scales rather than reusing the
Constitution's R0–R4:

- **XP-0..XP-8** — process class (observation only → micro-intervention →
  habit-building → comparative → withdrawal/return → specialist-monitored →
  reflective practice → high-control → **XP-8: inadmissible**, rejected
  outright without proportionate safety or legality).
- **SE0–SE4** — safety-event severity (none/expected mild → mild transient →
  moderate/functional decline → serious/health risk → emergency/life
  threat), each with a default reaction.
- **EC0–EC5, BL0–BL5, MQ0–MQ5, PF0–PF5, DQ0–DQ5, CA0–CA5, PE0–PE5** — contract
  completeness, baseline quality, measurement quality, protocol fidelity,
  data quality, causal confidence, and personal-evidence strength,
  respectively.
- **Outcome codes** R+, R?+, R0, R?0, R-, R±, RL, RW, and cycle states DRAFT,
  BASELINE, ACTIVE, HOLD, WASHOUT, MAINTENANCE, COMPLETED, STOPPED,
  INCONCLUSIVE.

No experiment may launch unless the system can answer its own "test
nadrzędny" (§0.5) — verbatim: *"co dokładnie sprawdza, dlaczego ten protokół
jest dopuszczalny, jaki jest punkt odniesienia, co zostanie zmierzone, jak
rozpoznać szkodę, kiedy przerwać, które czynniki mogą zakłócić wynik i jaką
decyzję umożliwi rezultat"* — if the system cannot answer all of these, the
experiment cannot be started, full stop.

## Rationale
Document motto (§0, verbatim): *"Eksperyment nie służy udowadnianiu racji
systemu. Służy bezpiecznemu sprawdzeniu, co zmienia się u konkretnego
człowieka, w konkretnych warunkach i za jaką cenę."* A domain as safety-
sensitive as personal experimentation (health, behavior, biomarkers) needs
graduated, purpose-built severity scales rather than overloading the
Constitution's general-purpose R0–R4 — a single scale could not distinguish
"micro-intervention" (XP-1) from "high-control, specialist-required" (XP-7)
with the granularity §34 (High-Risk Experiment Path) requires.

## Consequences
No `hos_engine` module currently implements any of these scales.
`hos_engine.hub_entity_registry.HubEntityType.EXPERIMENT` is only a bare
entity-type label with no dedicated fields — it does not yet model any of
Layer 6's ontology (see ADR-EXP-003). `hos_engine.simulation.py` and
`simulation_gate.py` implement a different, already-built concept (Monte
Carlo what-if scenario testing before executing an action, per
`ADR-0006-simulation-laboratory.md`) — that is not a personal N-of-1
experiment engine and should not be conflated with Layer 6. Before any of
this is implemented, the sequencing precedent set by `ADR-IMPL-001` (schema
before agents before interfaces) should apply here too.
