# ADR-DECISION-003: Abstention Is a First-Class, Named Outcome — Not a Failure to Decide

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_5_Silnik_Decyzji_i_Rekomendacji_v0_1.docx`, §27
("Abstencja, odmowa i eskalacja"). See `docs/FOUNDER_REVIEW_2026-08-15.md`,
"Czwarta tura" section, for provenance. Newly formulated — the source has no
ADR numbering of its own.

## Decision
**Abstention** (`Abstention` object, §4.1's ontology table) is a deliberate,
valid system output — a conscious decision *not* to recommend an action —
distinct from an error or a missing result. Named reasons for abstention
(§27.1): no clear goal or decision owner; insufficient critical data; an
unresolved value conflict; contradictory evidence with no safe option; no
way to monitor the outcome; excessive risk or irreversibility; the problem
exceeds the system's competence; or suspicion of an urgent/crisis state.

Escalation is graduated into three named types (§27.3): **soft**
(education continues, consultation recommended), **conditional** (action
possible only after consultation or testing), and **hard** (the system
halts the protocol and directs to appropriate help).

## Rationale
This directly extends the project-wide "refusal is a first-class outcome,
never an exception" pattern (`ExecutionLoop`'s `IntentOutcome.REFUSED_*`,
the Proof Kernel's `Decision` enum) into the Decision Engine layer, with a
named object (`Abstention`) and named reasons rather than an implicit
absence of output. It also gives graduated escalation a vocabulary
(soft/conditional/hard) that the codebase does not currently have anywhere.

## Consequences
No code implements `Abstention` as a named object or a soft/conditional/hard
escalation gradient. `hos_engine.execution_loop.IntentOutcome` already has
`REFUSED_*` variants and `REQUIRES_HUMAN_DECISION` in
`hos_engine.policy.Decision`, but neither distinguishes "no clear goal" from
"contradictory evidence" from "suspected crisis" the way this document's
eight named abstention reasons do — a future Decision Engine module should
not assume the existing refusal vocabulary is granular enough without
extending it.

**Update 2026-08-15 (Phase 3):** implemented in
`hos_engine.decision_engine` — `AbstentionReason` carries all eight named
reasons, `EscalationType` carries the soft/conditional/hard gradient, and
`DecisionOutcomeKind.ABSTENTION`/`ESCALATION` are first-class returns of
`DecisionEngine.decide()`, never exceptions.
