# ADR-EXP-004: AI's Role in the Experiment Engine Is Bounded by a Fixed List of Forbidden Autonomous Actions

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_6_Silnik_Eksperymentow_Monitorowania_i_Postepu_v0_1_2.docx`
("Warstwa 6"), §34 ("Ścieżka eksperymentu wysokiego ryzyka") and §37 ("Rola AI
w Silniku Eksperymentów"). See `docs/FOUNDER_REVIEW_2026-08-15.md`, "Trzecia
tura" section, for provenance. Newly formulated — the source has no ADR
numbering of its own.

## Decision
AI may not, without additional human control (§37.2, full list): autonomously
start an experiment or change consent; set dosing for medication or
high-risk substances or specialist-required therapy; hide unfavorable data
to sustain motivation; change success thresholds after seeing the result;
diagnose from an N-of-1 pattern; share data to the community layer without
active consent; optimize time-in-app as an experiment goal; or use symbolic
systems (Human Design, astrology — see ADR-EXP-005) for medical
qualification.

For the high-risk path specifically (§34, XP-7/high-risk processes): "Zakaz
automatycznego zwiększania ekspozycji przez AI" (ban on AI auto-increasing
exposure) is absolute. §34.2, verbatim: *"Determinacja użytkownika nie
obniża progu bezpieczeństwa"* (the user's determination does not lower the
safety threshold) — AI may inform, point out gaps, and facilitate a
conversation with a specialist, but *"nie tworzy szczegółowego protokołu
wykonawczego dla działania rażąco ryzykownego, nielegalnego albo
pozbawionego realnej możliwości monitorowania"* (it does not produce a
detailed executable protocol for an action that is grossly risky, illegal,
or impossible to monitor safely).

## Rationale
This is the Layer 6 instance of the Constitution's general AI-role-boundary
principle (`constitution/README.md` Ch.7) and matches the project's existing
"agent capability does not imply agent permission" stance already stated in
ADR-CORE-001's rationale ("an agent does not gain permissions merely because
it is capable of performing a task"). The high-risk-path rule is stricter
than a simple approval gate: even with an approving, determined user, the
system's own floor does not move.

## Consequences
No `hos_engine` module encodes this list of forbidden AI actions today.
`hos_engine.agent_runtime.AgentManifest` already has a general
capability/permission model but no Layer-6-specific forbidden-action set or
a hard-coded "never auto-escalate exposure" rule. Any future Layer 6 agent
integration should encode §37.2's list as an explicit denylist at the
capability-declaration level, not rely on prompt-level instruction alone —
consistent with how `ExecutionLoop`'s gates are enforced in code, not in
agent instructions.
