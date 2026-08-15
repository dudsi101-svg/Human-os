# ADR-USERMODEL-004: AI May Not Silently Infer, Label, or Override an Explicit User Correction

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_4_Model_Uzytkownika_i_Cyfrowy_Profil_v0_1.docx`, §33
("Rola AI w budowie Modelu Użytkownika"). See
`docs/FOUNDER_REVIEW_2026-08-15.md`, "Czwarta tura" section, for provenance.
Newly formulated — the source has no ADR numbering of its own.

## Decision
Forbidden AI functions (§33.2, "Zakazane funkcje", full list): hidden
inference; personality labeling; manipulation; **overriding the user**
(verbatim: *"traktowanie wniosku AI jako ważniejszego od jawnej korekty
osoby"* — treating an AI conclusion as more authoritative than the person's
own explicit correction); false/performed diagnostics; **unilateral consent
expansion** (verbatim: *"rozszerzanie zakresu danych przez domniemanie"* —
expanding data scope by inference/assumption); and **invisible learning**
(verbatim: *"wykorzystanie danych profilu do trenowania modeli bez
wyraźnej podstawy i informacji"* — using profile data to train models
without an explicit basis and disclosure).

Companion "dark pattern" ban (§17.2/§1209 box, "Zakaz ciemnych wzorców"):
streaks, progress-loss alarms, social shame, artificial urgency, and
addictive rewards may never be used to force behavior — engagement is a
means, never a product goal.

## Rationale
"Overriding the user" is the sharpest, most consequential item on this
list: it directly forbids the single most common AI-personalization failure
mode — treating a system's own inference as more reliable than the person
it is supposedly modeling. Combined with the unilateral-consent-expansion
and invisible-learning bans, this closes the three main routes by which a
personalization system typically drifts from "supporting the user" to
"overriding the user without them noticing."

## Consequences
No code enforces any of these three bans today. If model training or
inference pipelines are ever built against `HumanRecord` data, this ADR
requires: (1) an explicit precedence rule where a user's `contest()` call
always outranks a system-derived hypothesis, never the reverse; (2) that
consent scope expansion always requires an explicit new grant, never
inferred from behavior; (3) that any use of profile data for model training
carries its own disclosed, explicit consent basis, separate from
personalization consent. None of these three guarantees currently exist in
`hos_engine.personalization.py` or `human_model.py`.
