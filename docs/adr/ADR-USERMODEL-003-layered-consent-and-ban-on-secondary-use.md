# ADR-USERMODEL-003: Six-Level Layered Consent, Five-Level Data Sensitivity, and an Absolute Ban on Secondary Commercial Use

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_4_Model_Uzytkownika_i_Cyfrowy_Profil_v0_1.docx`, §5.1
(consent), §27.1 (sensitivity), §27.3 ("Zakaz wtórnego wykorzystania"). See
`docs/FOUNDER_REVIEW_2026-08-15.md`, "Czwarta tura" section, for provenance.
Newly formulated — the source has no ADR numbering of its own.

## Decision
**Layered consent (C0–C5):** C0 account-essential (required to function),
C1 personalization (usage history, preferences, AI inferences — separately
revocable), C2 device data (per integration/category), C3 sensitive data
(health, psyche, biometrics, sexuality — explicit, purpose-bound, periodic
consent), C4 community contribution (separate consent per contribution
type), C5 research use (separate form, revocable).

**Data sensitivity (D0–D4):** D0 public/neutral through **D4 critical**
(disclosure could cause serious harm — requires minimization, local
processing, or no storage at all).

**Absolute ban on secondary use** (§27.3, verbatim): *"Dane zebrane dla
wsparcia użytkownika nie mogą zostać wykorzystane do reklamy, oceny
zdolności kredytowej, ubezpieczenia, zatrudnienia, dynamicznego ustalania
cen ani manipulowania podatnością bez odrębnej, dobrowolnej i rzeczywiście
odwoływalnej zgody. Niektóre zastosowania powinny pozostać bezwzględnie
zakazane niezależnie od zgody."* — critically, the final sentence states
some uses should remain **forbidden regardless of consent** — this is not
merely a consent-gate, it is a hard ban for at least some subset of uses,
though the document does not enumerate exactly which ones fall in that
absolute category versus the consent-gated category.

A companion rule blocks consent from becoming coercive: §5.1's "Zakaz zgody
pozornej" (ban on sham consent) requires that declining sensitive-data
consent never trigger a penalty, a manipulative interface, or a false "we
can't help you" message — the system must instead clearly show which
functions will be less precise and why.

## Rationale
Six granularity levels of consent and five of sensitivity are what let
"data minimization" (already a named principle in this project's
Constitution and `CONTRIBUTING.md` checklist) be enforced per-field rather
than as a single account-wide toggle — and the secondary-use ban directly
protects against the most common real-world failure mode of personal data
systems (repurposing wellness/health data for credit, insurance, or
employment decisions).

## Consequences
`hos_engine.personalization.ConsentAwarePersonalizer` currently gates
consent at `subject_id/grantee_id/purpose/domain/action` granularity with a
single boolean `sensitive` flag — a binary distinction where the source
specifies 6 consent levels and 5 sensitivity classes. This is a concrete,
checkable gap, not a contradiction — `personalization.py` may be an
intentionally coarser MVP primitive — but no code currently enforces the
secondary-use ban at all, absolute or consent-gated. Before any commercial
feature (ads, pricing, scoring) is built against user-model data, this ADR
should be treated as a hard blocker requiring explicit resolution of which
uses are absolutely forbidden versus merely consent-gated.
