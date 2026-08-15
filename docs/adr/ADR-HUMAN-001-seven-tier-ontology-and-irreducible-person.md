# ADR-HUMAN-001: The Human Model Is a Seven-Tier Ontology With an Irreducible Person at Tier Zero

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_2_Model_Czlowieka_v0_1.docx` ("Warstwa 2", version
"0.1 - model bazowy", dated 2026-07-19, status "Projekt do iteracji,
walidacji i zatwierdzenia"). This document was previously listed in
`docs/FOUNDER_REVIEW_2026-08-15.md` as "confirmed to exist, content
unavailable" — now available for the first time. See that file's "Czwarta
tura" section for provenance, and `docs/LAYER_2_HUMAN_MODEL_DIGEST.md` for
the full digest. The source has no ADR numbering of its own — this ADR is
newly formulated.

## Decision
The Human Model (Layer 2) organizes everything it represents about a person
into seven ordered tiers ("Rząd 0" through "Rząd 6"):

- **Rząd 0 — the person as an irreducible whole.** Verbatim: *"Model może
  opisywać funkcjonowanie, lecz nie może obliczać 'wartości człowieka',
  poziomu moralności ani ostatecznego potencjału."* Dignity, autonomy, and
  worth do not derive from data.
- **Rząd 1 — domains** (11 named life domains, see `ADR-HUMAN-002`).
- **Rząd 2 — systems and processes** (e.g. sleep regulation, attention,
  sense of safety, bonding, decision-making, meaning-making).
- **Rząd 3 — capacities, resources, constraints.**
- **Rząd 4 — states, patterns, behaviors** (state = a moment; pattern =
  recurrence; behavior = an action — no strong conclusion from an isolated
  event).
- **Rząd 5 — data and observations** (self-report, devices, documents,
  tests, in-app behavior, expert or community reflection; every record
  carries source, time, context, quality, consent, and interpretation
  limits).
- **Rząd 6 — hypotheses and decisions** (conclusions about the user are
  versioned hypotheses; recommendations form only after combining a
  hypothesis with a goal, risk tolerance, cost, and alternatives).

Document's own gating test (§0.5, verbatim): *"Czy opis pozostawia miejsce
na zmianę, kontekst, wyjątki i niewiedzę, czy też zamienia człowieka w
stałą etykietę? Jeśli zamienia go w etykietę, model wymaga korekty."*

## Rationale
Motto (verbatim): *"Model jest mapą człowieka, nie człowiekiem. Każdy
wniosek pozostaje hipotezą o określonym poziomie pewności."* Placing an
uncomputed, undata-derived tier (Rząd 0) *above* every measurable tier is
the structural guarantee that no amount of data accumulation can
mathematically produce a "human worth" score — the ban lives in the
ontology's shape, not just in a policy statement.

## Consequences
No `hos_engine` module implements this seven-tier structure.
`hos_engine.human_model.HumanModel`/`HumanRecord` is a flat, per-domain
store with no explicit tiering and no Rząd-0-equivalent concept guarding
against aggregate "worth" computation — this is an architectural gap, not
just a missing feature, since the ban's enforcement in the source document
depends on the tiering itself. Any future alignment work should treat
adding the tier structure as a precondition for any "aggregate score"
feature, not an optional refinement.
