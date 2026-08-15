# ADR-HUMAN-003: Anti-Labeling Rules and "Protected Changes" That Require Constitutional-Level Rejection

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_2_Model_Czlowieka_v0_1.docx`, §25.1 ("Zakazane
wnioski") and §26.3 ("Zmiany chronione"). See
`docs/FOUNDER_REVIEW_2026-08-15.md`, "Czwarta tura" section, for provenance.
Newly formulated — the source has no ADR numbering of its own.

## Decision
Six example sentences the system must never produce (§25.1, verbatim):
*"Jesteś swoim wynikiem, typem lub diagnozą."*, *"Twoja przyszłość jest
przesądzona."*, *"Brak postępu oznacza brak wartości lub zaangażowania."*,
*"System zna Cię lepiej niż Ty sam."*, *"Każde cierpienie jest lekcją, którą
sam wybrałeś."*, *"Jedna metoda wyjaśnia całego człowieka."*

**Protected changes** (§26.3, verbatim): changes that would enable
*"ocenę wartości człowieka, automatyczną diagnozę wysokiego ryzyka, niejawne
profilowanie osób trzecich lub deterministyczne wykorzystanie systemów
symbolicznych powinny wymagać odrzucenia jako sprzeczne z Warstwą 1, a nie
zwykłej decyzji produktowej."* — such changes require rejection as
conflicting with the Constitution, not an ordinary product decision. This
is the closest Layer 2 equivalent to Layer 6's explicit "brama
konstytucyjna" (constitutional gate).

Supporting rules: personality traits are represented as context-dependent
*distributions*, never deterministic predictions (§8.2, "Cechy jako
rozkłady, nie wyroki"); rejecting the model must never be auto-interpreted
as psychological resistance (§20.4); the model must never trap a person in
an old description just because it holds a lot of data about them (§21.4,
"Prawo do resetu modelu").

## Rationale
This is the project's `escalate when a constitutional rule would change`
rule (already standing in this session's conduct) instantiated *inside a
specification document itself* — the source pre-emptively marks certain
future changes as requiring the higher governance bar
(`GOVERNANCE.md`/Constitution amendment process) rather than an ordinary PR
review, before anyone has proposed making them.

## Consequences
No code enforces "protected change" status on any category of modification
to `human_model.py` today — there is no mechanism distinguishing an
ordinary schema change from one that would enable worth-scoring or
deterministic profiling. If `human_model.py` is ever extended toward
aggregate scoring, automatic high-risk diagnosis, or deterministic symbolic-
system output, that change should be treated as hitting this project's
existing constitutional-escalation trigger, not merged as routine code
review — consistent with how the Constitution rewrite (Q1) itself was
escalated to the founder in this session rather than done unilaterally.
