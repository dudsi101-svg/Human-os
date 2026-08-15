# ADR-DECISION-005: The High-Risk Decision Path — User Determination Does Not Lower the Safety Threshold

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_5_Silnik_Decyzji_i_Rekomendacji_v0_1.docx`, §28
("Ścieżka decyzji wysokiego ryzyka"). See `docs/FOUNDER_REVIEW_2026-08-15.md`,
"Czwarta tura" section, for provenance. Newly formulated. This is the Layer
5 counterpart to `ADR-EXP-004`'s high-risk-path rule for Layer 6 — the
digest confirms the two documents use near-identical language here.

## Decision
Minimum conditions for a high-risk recommendation (§28.1): a clear, durable
goal; no safer alternative of similar value; a full risk/interaction
profile; an evidence level proportionate to the possible harm; a competent
specialist if required; a monitoring plan and stop criteria; unpressured
time to reflect; separate consent and a decision snapshot; and an explicit
**ban on financial incentive influencing the ranking**.

**User determination** (§28.2, verbatim): *"Determinacja może uzasadniać
bardziej szczegółowe omówienie ryzyka... Nie uzasadnia pomijania kontroli,
projektowania dawki poza kompetencjami ani normalizowania niebezpiecznej
praktyki."* — a determined user justifies a more detailed risk discussion,
never skipping controls, designing dosage beyond the system's competence,
or normalizing a dangerous practice.

**Harm-reduction procedure** (§28.3): permitted only when the user will
likely act regardless of the recommendation, and only if the information
given *"nie zwiększa w sposób nieproporcjonalny zdolności do spowodowania
ciężkiej szkody"* — does not disproportionately increase the capacity to
cause serious harm; scope of help remains subject to Layer 1 (Constitution)
and specialist safety policies.

The concrete instance the source gives (Załącznik L, high-risk GHK-Cu
injection scenario): *"Silnik wybiera RC6: nie tworzy samodzielnego schematu
iniekcji"* — the engine selects abstention/escalation and never generates
an injection protocol itself.

## Rationale
Both Layer 5 and Layer 6 independently arrive at the same rule — user
determination changes tone and depth of conversation, never the safety
floor itself. Having this rule appear twice, worded almost identically, in
two independently-authored layer specifications is strong evidence it is a
project-wide invariant rather than a per-layer opinion, and it should be
treated as such in any future implementation.

## Consequences
No code implements a high-risk decision path or a harm-reduction procedure
today. Any future Decision Engine module must treat "financial incentive
cannot influence ranking" and "determination never lowers the safety floor"
as hard, code-level constraints — not something a prompt or a UI warning
label can satisfy on its own, consistent with `ADR-DECISION-004`'s
architecture-with-constraints requirement.

**Update 2026-08-15 (Phase 3):** both constraints are now code-level in
`hos_engine.decision_engine`: `DecisionCandidate.sponsored` exists but is
deliberately absent from the ranking key, and
`DecisionRequest.user_determination` is read by nothing — each enforced by
a dedicated invariant test (`test_sponsorship_never_improves_ranking`,
`test_user_determination_never_changes_any_outcome`). The fuller high-risk
path (§28's minimum conditions, harm-reduction procedure) remains
unimplemented; the MVP simply never admits an R-KRYTYCZNE candidate and
routes R-PODWYZSZONE/R-WYSOKIE through a conditional recommendation.
