# ADR-USERMODEL-001: The User Model Is a Nine-Row R0–R8 Architecture With Its Own Four Coded Scales

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_4_Model_Uzytkownika_i_Cyfrowy_Profil_v0_1.docx` ("Warstwa
4", version "0.1 – model bazowy", dated 2026-07-20, status "Projekt do
iteracji, testów użytkowników i audytu"). See
`docs/FOUNDER_REVIEW_2026-08-15.md`, "Czwarta tura" section, for provenance,
and `docs/LAYER_4_USER_MODEL_DIGEST.md` for the full digest. The source has
no ADR numbering of its own — this ADR is newly formulated. **See
`ADR-USERMODEL-005` first** — this document is not the source behind the
already-existing `ADR-USER-002` ("Human Digital Twin"); treat the two as
related sibling specifications, not duplicates.

**Naming note:** this document's "R0–R8" labels a nine-row *model
architecture*, unrelated in meaning to the Constitution's R0–R4 *risk
scale* — confirmed by the source never mentioning the Constitution's scale.
This is now the **fifth** independent letter/number scheme found across the
layers digested so far (Constitution R0–R4; Layer 6 XP/SE/EC/BL/MQ/PF/DQ/CA/
PE; Layer 5 DI/IQ/AR/RV/RC/G/R-level; Layer 3's signature/E/K/source-codes;
now Layer 4's R0–R8/H/P/C/D) — none overlapping in meaning despite
overlapping letters.

## Decision
Twelve axioms (§1) govern every profile, personalization algorithm, and
inference about a person — most notably: the model is a hypothesis in time
(#2), the user retains the right to interpret their own experience (#3),
absence of data does not mean absence of the phenomenon (#7), contradiction
is information and must be stored with context rather than averaged away
(#8), the profile must be able to forget (#9), and the system never
predicts a person's worth (#12).

A nine-row architecture, R0–R8: **R0** identity & control, **R1** direction
(values/goals), **R2** context, **R3** source data, **R4** derived
features, **R5** personal hypotheses, **R6** operational state, **R7**
decision history, **R8** presentational profile ("Cyfrowy profil
rozwojowy" — explicitly only this one presentational *layer*, not a synonym
for the whole model).

Four independent coded scales: **H0–H5** (personal-hypothesis readiness for
use in personalization — explicitly *not* a probability of truth, per the
source's own caveat), **P0–P5** (personal/N-of-1 evidence strength, anecdote
through stable personal rule), **C0–C5** (layered consent, from account-
essential through research use), **D0–D4** (data sensitivity class, from
public/neutral through critical-if-disclosed).

The system's own gating test (§0.5, verbatim): *"Jeżeli nie można jasno
odpowiedzieć: »po co przechowujemy tę informację?«, »skąd pochodzi?«, »jak
długo jest aktualna?«, »kto ją widzi?«, »jak wpływa na decyzje?« i »jak
użytkownik może ją poprawić lub usunąć?«, informacja nie może zostać
aktywnie użyta w Modelu Użytkownika."*

## Rationale
Opening line (verbatim): *"Model jest mapą osoby w określonym czasie i
kontekście. Nigdy nie jest jej ostateczną definicją."* The nine-row
structure gives every field in the profile an explicit place between raw
data (R3) and presentation (R8), preventing a shortcut from observation
straight to a labeled conclusion — the same purpose Layer 2's seven-tier
ontology (`ADR-HUMAN-001`) serves for the underlying person model.

## Consequences
No `hos_engine` module implements the R0–R8 architecture or any of the four
scales. `hos_engine.human_model.HumanModel`/`HumanRecord` is a flat,
per-domain store implementing only a narrow slice — see
`ADR-USERMODEL-004`'s Consequences for the itemized gap against
`personalization.py`'s single boolean `sensitive` flag versus this
document's 6-level C0–C5 and 5-level D0–D4 scales.
