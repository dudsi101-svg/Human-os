# ADR-HUMAN-005: Three Operating Modes and a Hard Clinical Boundary — No Autonomous Diagnosis

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_2_Model_Czlowieka_v0_1.docx`, §22 ("Granice
zdrowia, rozwoju i pomocy specjalistycznej") and §4.4 ("Granice
interpretacji"). See `docs/FOUNDER_REVIEW_2026-08-15.md`, "Czwarta tura"
section, for provenance. Newly formulated — the source has no ADR numbering
of its own.

**Naming note:** unlike Layer 6's lettered safety-event scale (SE0–SE4),
Layer 2 defines its safety response **qualitatively**, as three named modes
rather than a coded scale — the digest confirms this is a deliberate
difference in kind (Layer 2 is an epistemic/ontological model of the
person; Layer 6 is an experiment-execution engine), not an oversight.

## Decision
Three operating modes (§22.1): **Rozwój i dobrostan** (development &
wellbeing — no signs of urgent risk; experiments, education, reflection),
**Wsparcie przy ograniczeniu** (support under limitation — symptoms,
chronic difficulty, or uncertainty; caution, monitoring, consultation), and
**Bezpieczeństwo i eskalacja** (safety & escalation — direct or serious
risk; optimization halts, urgent help is indicated).

**Clinical boundary** (§4.4, verbatim): *"Human OS może porządkować
informacje, wspierać pytania do specjalisty i monitorować uzgodnione
działania. Nie stawia samodzielnie diagnozy ani nie odradza leczenia na
podstawie systemu symbolicznego, doświadczeń społeczności lub pojedynczego
wskaźnika."* — the system organizes information and supports
specialist-facing questions; it never independently diagnoses or advises
against treatment based on a symbolic system, community experience, or a
single indicator.

**Non-pathologizing principle** (§22.3, verbatim): *"Nie każda różnica,
intensywna emocja, kryzys sensu lub nietypowe doświadczenie jest
zaburzeniem."* The model must weigh suffering, functioning, duration,
context, and risk together — avoiding both minimizing and over-medicalizing.

## Rationale
This is Layer 2's version of the "hard gate before scoring" pattern used
everywhere else in the project, applied to a domain where the two failure
modes (dismissing real distress vs. pathologizing normal variation) are
both actively harmful — the non-pathologizing principle exists specifically
to prevent the safety-mode machinery from over-triggering on ordinary human
variation.

## Consequences
No code implements these three modes, the escalation-signal list (§22.2),
or the non-pathologizing balancing rule. If `human_model.py` or a future
module ever adds risk-mode switching, it should model this as three named,
qualitative modes (not force-fit onto Layer 6's numeric SE0–SE4, which
measures something different — experiment-safety-event severity, not
general life-risk state) and should explicitly implement the non-
pathologizing check as a counterweight, not just the escalation trigger
list alone.
