# ADR-DECISION-004: AI's Role in the Decision Engine — Organizes and Translates, Is Not the Source of Truth or the Final Arbiter of Risk

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_5_Silnik_Decyzji_i_Rekomendacji_v0_1.docx`, §40
("Rola AI w Silniku Decyzji"). See `docs/FOUNDER_REVIEW_2026-08-15.md`,
"Czwarta tura" section, for provenance. Newly formulated — the source has no
ADR numbering of its own. Structurally near-identical to Layer 6's AI-role
section (`ADR-EXP-004`) — the digest explicitly flags this as a shared
design template across layers, not coincidence.

## Decision
Section header (verbatim): *"Model językowy może organizować i tłumaczyć,
ale nie jest samodzielnym źródłem prawdy ani ostatecznym arbitrem ryzyka."*

**Permitted** (§40.1): recognizing intent and clarifying goals; generating
candidates from the *approved* Knowledge Map; summarizing evidence and
trade-offs; detecting gaps, contradictions, and potential interactions;
personalizing language and presentation; producing reflective questions and
alternative scenarios; preparing an explanation from explicit rules and
data.

**Forbidden without additional control** (§40.2): independently inventing
new contraindications or doses as facts; silently modifying risk weights;
diagnosing from speech style; using unapproved sources in a high-impact
decision; publishing a recommendation after detecting a rule conflict;
faking confidence to keep a conversation flowing.

**Architecture constraint** (§40.3, verbatim): *"Krytyczne bramy,
identyfikatory źródeł, klasy ryzyka i wymogi zgody nie mogą istnieć
wyłącznie w tekście promptu."* — critical gates, source identifiers, risk
classes, and consent requirements must not live only in prompt text.

**Calibration** (§40.4, verbatim): *"Pewność językowa modelu nie może być
używana jako pewność decyzji."* — the model's linguistic confidence must
never be used as decision confidence; confidence must derive from explicit
data, knowledge quality, fit, and validation results instead.

## Rationale
This mirrors `ADR-EXP-004`'s treatment of AI boundaries in the Experiment
Engine, and reflects the same project-wide stance already in
`ADR-CORE-001`'s rationale ("an agent does not gain permissions merely
because it is capable of performing a task"). The explicit ban on encoding
safety logic only in prompt text is the same principle that already governs
this codebase's actual security architecture (`security_gateway.py`'s
code-level check pipeline, not LLM-level instructions).

## Consequences
No code implements this list of permitted/forbidden AI functions for a
Decision Engine today. When one is built, §40.2's denylist should be
enforced at the capability-declaration or gate level (the same pattern
`ADR-EXP-004` recommends for Layer 6), and §42.2's companion rule —
*"Twarde zakazy, zgoda i krytyczne interakcje powinny być reprezentowane w
deterministycznych lub formalnie walidowanych regułach"* — should guide
where hard gates live in the architecture: never solely inside a
probabilistic model's output.
