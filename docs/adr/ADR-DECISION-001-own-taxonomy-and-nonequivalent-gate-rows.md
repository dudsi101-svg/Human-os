# ADR-DECISION-001: The Decision Engine Defines Its Own Taxonomy and a Ten-Row Non-Commutable Process Architecture

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_5_Silnik_Decyzji_i_Rekomendacji_v0_1.docx` ("Warstwa 5",
version "0.1 - model bazowy", dated 2026-07-20, status "Projekt do iteracji,
testów, walidacji i audytu"). See `docs/FOUNDER_REVIEW_2026-08-15.md`,
"Czwarta tura" section, for provenance, and
`docs/LAYER_5_DECISION_ENGINE_DIGEST.md` for the full underlying digest. The
source has no ADR numbering of its own — this ADR is newly formulated.

**Naming note:** this document independently uses the letter "R" four
different ways within itself — process rows R0–R9 (§3), risk-reaction
classes R-NISKIE..R-KRYTYCZNE (§12.2), reversibility scale RV0–RV4 (§16.1),
and recommendation classes RC0–RC6 (§24.1) — **none of which is the
Constitution's R0–R4 risk scale**, and none of which line up with Layer 6's
XP/SE/EC/BL/MQ/PF/DQ/CA/PE scales either. Three independent, non-overlapping
taxonomies now exist across three digested layers (Constitution, Layer 5,
Layer 6) — do not conflate any of them.

## Decision
Layer 5 (the Decision & Recommendation Engine) turns a goal/context/
knowledge input into a recommended decision, immediately upstream of Layer 6
(which turns an accepted recommendation into an executed experiment). It
defines a ten-row process architecture, R0 through R9 (constitutional gate →
intent/goal → state/context → problem map → candidate generation → hard
gates → decision profile → prioritization → explanation/consent →
execution/feedback), plus independent coded scales: **DI-1..DI-8** (intent
classes), **IQ0–IQ5** (input quality), **AR0–AR5** (readiness), **RV0–RV4**
(reversibility), **RC0–RC6** (recommendation classes), **G0–G8** (named hard
gates), and **R-NISKIE..R-KRYTYCZNE** (risk-reaction classes).

No recommendation may be published unless the system can answer its own
"test nadrzędny" (§0.5) — verbatim: *"'jaki cel realizuje ten wybór?',
'dlaczego ten wariant jest dopuszczalny?', 'co może pójść źle?', 'jakie są
alternatywy?', 'jakiej informacji brakuje?', 'jak użytkownik może odmówić?'
oraz 'kiedy należy przerwać lub ponownie ocenić decyzję?'"* — an exact
structural mirror of Layer 6's own pre-launch gate (`ADR-EXP-001`), applied
here to publishing a recommendation instead of starting an experiment.

**Non-commutability (§3.1):** *"Rzędy nie są punktami jednego rankingu.
Wynik wyższego etapu nie może unieważnić twardego ograniczenia z
wcześniejszej bramy."* — a candidate with high projected benefit remains
excluded if it violates the Constitution, consent, law, or critical safety,
regardless of how the later ranking stage would score it.

## Rationale
Document motto (verbatim): *"Dobra decyzja nie jest wyrokiem algorytmu. Jest
przejrzystym, możliwym do zakwestionowania wyborem dokonanym wspólnie z
użytkownikiem."* The row architecture and non-commutability rule are the
same "hard gate before scoring" pattern already used throughout this
project (the Proof Kernel, `ExecutionLoop`'s refusal gates, Layer 6's
XP-class gating) — applied here specifically to prevent a high-ranking
recommendation from ever overriding an earlier constitutional or safety
exclusion.

## Consequences
No `hos_engine` module implements any of this. The existing
`hos_engine.policy.ProofKernel` is a different, already-built mechanism
(9 constitutional tests, PROOF-001..009) that operates at a more general
level than this document's ten-row decision pipeline — the two should not
be assumed equivalent without a design pass. Before implementing, note this
document's own explicit gap: no mapping is given between its four
independent "R"-prefixed scales and either the Constitution's R0–R4 or
Layer 6's coded scales — integration between Layer 5 and Layer 6 is
described only in natural-language field names (§41's interface table), not
shared numeric codes.

**Update 2026-08-15 (Phase 3):** a first MVP slice now exists —
`hos_engine.decision_engine.DecisionEngine` implements the nine hard gates
G0–G8, the R-NISKIE..R-KRYTYCZNE reaction classes, the evidence-asymmetry
threshold (declared evidence 0–5 vs. risk class), non-commutable
gate-before-ranking ordering, and an RC0/RC3/RC5/RC6 outcome subset, with
21 tests (`tests/test_decision_engine.py`). Intent classes DI-1..8,
IQ0–IQ5, AR0–AR5, the ten-axis §18 profile, and live Knowledge Map
integration remain unimplemented; like the Proof Kernel, the engine
evaluates declared inputs only.
