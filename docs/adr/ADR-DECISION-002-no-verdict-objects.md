# ADR-DECISION-002: No "Verdict Objects" — Judgments About a Person Must Decompose Into Observation, Context, and Hypothesis

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_5_Silnik_Decyzji_i_Rekomendacji_v0_1.docx`, §4.2
("Zakaz ukrytego scalania" / "Zakaz obiektu-wyroku"). See
`docs/FOUNDER_REVIEW_2026-08-15.md`, "Czwarta tura" section, for provenance.
Newly formulated — the source has no ADR numbering of its own.

## Decision
The system may never store a single field like *"użytkownik jest
niezdyscyplinowany"* (the user is undisciplined) or *"interwencja jest
dobra"* (the intervention is good) as a fact. Verbatim: such shortcuts
*"muszą zostać rozłożone na obserwacje, kontekst, hipotezę, pewność, datę
ważności i możliwe alternatywne wyjaśnienia"* — must decompose into
observations, context, hypothesis, confidence, an expiry date, and possible
alternative explanations.

Objects removed from an active decision process remain in the audit trail
(to the extent required by law and consent) but *"nie mogą potajemnie
wpływać na nowe decyzje"* — cannot secretly influence new decisions.

## Rationale
This is the same architectural pattern already documented for Layer 6
(`ADR-EXP-003`, "Zakaz ukrytego scalania") applied to the decision axis
instead of the measurement axis — the digest explicitly identifies it as
"ten sam wzorzec architektoniczny powtórzony na osi decyzyjnej." A decision
engine is especially exposed to this failure mode because verdict-shaped
labels are exactly what a ranking/scoring system tends to produce as
shorthand — this rule blocks that shorthand from ever becoming the system
of record.

## Consequences
No code implements this decomposition requirement today.
`hos_engine.human_model.HumanRecord` stores flat key/value records with a
single `confidence: float` — it does not enforce that a judgment-shaped
value be backed by a decomposed observation/hypothesis/context set. Any
future Decision Engine implementation should treat this as a hard schema
constraint, not a style guideline: a "verdict" field type should not exist.
