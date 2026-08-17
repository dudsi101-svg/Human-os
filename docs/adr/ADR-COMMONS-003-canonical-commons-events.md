# ADR-COMMONS-003: Canonical `commons_*` Event Types (DD-009 part 1)

## Status
Accepted and implemented 2026-08-17 — founder approval recorded in
`docs/DEFERRED_DECISIONS.md` DD-009 („Tak, należy wdrożyć te rozszerzenia"
+ explicit selection of „Commons: 16 zdarzeń"). Part 2 of DD-009
(ModerationCase and the moderation-roles model) remains open and is **not**
implemented by this ADR.

## Context
`docs/COMMONS_MODULE_DIGEST.md` §8 lists sixteen collaboration events for
the "Wspólnie" module (challenge_created … moderation_case_resolved). The
digest itself notes that adding them to the canonical dictionary requires a
separate ADR, schemas, and constitutional-compatibility tests. DD-009's
recorded recommendation — one change introducing the complete set with
schema support and an R0–R4 mapping for public-challenge risk — was
approved by the founder on 2026-08-17.

## Decision

1. **Fourteen new canonical event types** enter `event.types.json`
   (0.3.0 → 0.4.0) and the `event.schema.json` enum, in the dictionary's
   UPPER_SNAKE convention:
   `CHALLENGE_CREATED`, `CHALLENGE_PUBLISHED`, `CHALLENGE_JOINED`,
   `CHALLENGE_LEFT`, `COMMITMENT_CREATED`, `COMMITMENT_RENEGOTIATED`,
   `CHECKIN_RECORDED`, `EXPERIENCE_SHARED`, `EXPERIENCE_RETRACTED`,
   `SUPPORT_REQUESTED`, `SUPPORT_ACCEPTED`, `OUTCOME_RECORDED`,
   `MODERATION_CASE_OPENED`, `MODERATION_CASE_RESOLVED`.

2. **The two commons consent events reuse the existing canonical types.**
   The source's `consent_granted`/`consent_revoked` are semantically the
   same act as the dictionary's existing `CONSENT_GRANTED`/
   `CONSENT_REVOKED` (a consent came into force / was withdrawn); the
   Commons context lives in the event payload, not in a parallel type.
   No `COMMONS_CONSENT_*` duplicates are created — this repository already
   carries enough deliberately-parallel vocabularies, and consent is not
   one of them. All sixteen source events are therefore covered:
   fourteen new types plus two existing ones.

3. **Risk mapping for public challenges** is recorded as a data artifact,
   `policies/commons.challenge.risk.json`, mapping challenge categories to
   the Constitution's R0–R4 with per-class publication rules, transcribing
   the digest's §7 constraints (sensitive-domain public challenges require
   risk classification; extreme actions are never published without
   additional control). Like `policies/constitutional.policies.json`, it
   is a spec-ahead-of-code artifact: nothing interprets it yet.
   **Update 2026-08-17 (later the same day):** the founder confirmed the
   class boundaries — the full table was presented verbatim in-session and
   approved („Tak, róbmy to") — so the mapping is signed, while remaining
   documentation-only until Commons engine code exists.

4. **No engine module emits any commons event yet.** The user-demo app
   keeps logging its client-side equivalents locally. Emission starts only
   with the Commons engine slice, which (per ADR-COMMONS-001's binding
   rollout order) begins with private circles — and public challenges
   arrive only after identity, permissions, and moderation exist
   (DD-009 part 2).

## Consequences
- The dictionary and schema stay in lockstep (existing sync test extended
  by `tests/test_commons_events.py`).
- The change is purely additive: no existing event stream is invalidated,
  and history needs no rewriting.
- `MODERATION_CASE_OPENED`/`MODERATION_CASE_RESOLVED` exist as vocabulary
  only; recording an actual moderation case requires the part-2 model of
  moderation roles, which is a separate founder decision.
- The R4 class's required "additional control" is moderation, which does
  not exist yet — so R4 (and the control half of R3) publication is
  structurally unavailable until DD-009 part 2 lands. This is a fact the
  mapping file states, not a policy this ADR invents.
