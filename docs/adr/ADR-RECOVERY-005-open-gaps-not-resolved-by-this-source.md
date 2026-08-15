# ADR-RECOVERY-005: What This Source Does Not Resolve — Recorded, Not Guessed

## Status
Informational — not a decision to implement anything, but a companion
record to ADR-RECOVERY-001..004. Imported 2026-08-15 from founder-provided
source `Human_OS_Sovereign_Recovery_Layer_i_Rejestr_Scalenia_v0_2_1.docx`.
See `docs/FOUNDER_REVIEW_2026-08-15.md`, "Czwarta tura" section, for
provenance, and `docs/RECOVERY_LAYER_DIGEST.md` for the full underlying
digest this is drawn from.

## Decision
Per this project's source-integrity protocol (preserve conflicts and gaps
rather than silently resolving them), the following items are explicitly
**open** after reading the Sovereign Recovery Layer source in full. None of
these should be filled in by inference in future work without a founder
decision — they should be resolved the same way Q1–Q13 were, in
`docs/FOUNDER_REVIEW_2026-08-15.md`:

1. **The `RECOVERY_CUSTODIAN` role is undefined by its own presumed
   source.** `hos_engine.authority.AuthorityRole` already contains
   `RECOVERY_CUSTODIAN` as one of eight roles — but this document, the one
   most likely to be its justification, never mentions a "Recovery
   Custodian" by name, never says who holds it, how it's granted, or what
   power it has relative to Emergency Root or dual-key sovereignty. The
   code contains a concept this source does not support.
2. **No mapping to the Constitution's seven governance roles** (Ch.13:
   Product Owner, Constitutional/Ethics Council, Security Team, Knowledge
   Team, Data Team, Moderators, User). The document speaks only generically
   of "User / system owner."
3. **No mapping to the Constitution's R0–R4 risk scale** (Ch.6). Emergency
   modes like ROLLBACK or RECOVERY-after-device-seizure intuitively feel
   like high-risk (R3/R4) actions, but the source never classifies them
   against this scale.
4. **No genome-registry (`GEN-0xx`) references.** `GEN-014`
   ("Odwracalność"/Reversibility) is thematically closest, but the source
   doesn't cite it or any other gene.
5. **Triggering mechanism is unresolved.** The document defines each mode
   by what it *does*, and defines RECOVERY by what *situations* it serves
   (failure, account loss, data corruption, device seizure, agent error) —
   but never states whether entering a mode is always a deliberate human
   action, or whether the system may enter one automatically upon detecting
   such a situation. This is foundational for "who/what may press the stop
   button" and is not decided.
6. **No concrete time values.** "Automatically expires" and "time-limited"
   appear repeatedly with no TTLs, key-validity windows, or dual-key
   confirmation windows given anywhere.
7. **`FROZEN` vs. `SUSPENDED` naming is internally inconsistent** — see
   ADR-RECOVERY-004's Consequences section.
8. **No reference to any `hos_engine` module by name.** The whole document
   is written at the architectural/normative level (HOS Core, HOS Hub,
   Human OS Lab as concepts); mapping "HOS Core" → `hos_core.py`, "HOS Hub"
   → `hub_entity_registry.py`/`hub/`, "Human OS Lab" → (no repo equivalent
   found; per `CLAUDE.md`, Lab/Forge may live outside this repo entirely)
   is interpretive, not stated by the source.
9. **The document's own "Rejestr Scalenia" (Merge Register, §11) is a log
   of its own adoption (four `HOS-CHG-2026-0721-00N` entries), not the
   general, living Human OS artifact/version registry its title implies.**
   §12 says that general registry still needs to be created separately —
   don't treat this document's §11 as that registry.

## Rationale
The project's own standing rule (repeated across this session's founder
reviews) is: never design or implement safety-critical architecture from
guesswork, and never silently resolve a gap that a human should decide.
Recovery/SAFE MODE is the highest-stakes surface in the whole project — it
is the mechanism a user relies on when something has already gone wrong.
Guessing any of the nine items above to make an ADR feel more complete
would defeat the purpose of finally having the real source.

## Consequences
No Recovery/SAFE MODE code should be written until at least items 1
(`RECOVERY_CUSTODIAN` justification), 3 (R0–R4 mapping), 5 (trigger
mechanism), and 7 (`FROZEN`/`SUSPENDED`) are resolved with the founder —
these four block a coherent implementation, not just a complete one. Items
2, 4, 6, 8, 9 are lower-stakes and could reasonably be resolved during
implementation itself rather than requiring a prior founder decision, but
should still be resolved explicitly and recorded, not assumed.
