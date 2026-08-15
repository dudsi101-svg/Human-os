# ADR-EXP-002: Safety, Baseline Quality, and Consent Are Not Fungible With Each Other

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_6_Silnik_Eksperymentow_Monitorowania_i_Postepu_v0_1_2.docx`
("Warstwa 6"), §1 (16 axioms) and §3.1. See `docs/FOUNDER_REVIEW_2026-08-15.md`,
"Trzecia tura" section, for provenance. This document has no ADR-numbered
decisions of its own — this ADR is newly formulated from its axioms, not
extracted verbatim.

## Decision
Layer 6's "zasada nierównoważności rzędów" (§3.1, verbatim): *"Nie wolno
kompensować braku bezpieczeństwa wysoką wartością uczenia, braku punktu
odniesienia dużą liczbą późniejszych pomiarów ani braku zgody techniczną
łatwością zbierania danych."* — missing safety cannot be offset by high
learning value; a missing baseline cannot be offset by more later
measurements; missing consent cannot be offset by how technically easy data
collection would be.

Additional binding rules from the 16 axioms (§1) that follow the same
non-substitution logic:
- An intervention may not be judged ineffective unless it was actually
  performed, nor effective merely because it was performed (Axiom 6).
- A hypothesis may not be silently rewritten after seeing the result; a new
  post-hoc explanation must never be presented as if it had been predicted
  in advance (§7.4).
- Safety elements may never be automatically reduced to lower participant
  burden (§14.3).
- Compliance failures are never described in moralizing terms — "lazy,"
  "undisciplined," "uncooperative" are explicitly banned labels (§12.4,
  "Zakaz moralizacji zgodności").

## Rationale
This is Layer 6's domain-specific instance of a principle already load-
bearing elsewhere in the project: `hub_entity_registry.EntityRegistry.merge()`
requires `reason`/`evidence`/`approved_by` rather than accepting convenience
as a substitute for provenance, and `ExecutionLoop`'s gates refuse rather
than degrade silently. Here the same shape of rule protects the experiment
subject specifically: no dimension of rigor (safety, baseline, consent) may
be quietly traded off against another, no matter how compelling the
trade looks from a single-metric view.

## Consequences
Any future experiment-record schema must keep safety status, baseline
quality (`BL0–BL5`), and consent scope as independently gating fields —
never derived from, or overridable by, each other or by a general
"progress" or "engagement" score. No code currently implements this; it is
a design constraint for whichever module eventually models Layer 6's
`Experiment`/`Protocol`/`BaselineWindow` objects (see ADR-EXP-003).
