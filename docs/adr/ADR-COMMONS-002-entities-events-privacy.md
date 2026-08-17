# ADR-COMMONS-002: Commons Entities, Events, Privacy and Safety Contract

## Status
Accepted direction — same founder directive as ADR-COMMONS-001
(2026-08-17, digest in `docs/COMMONS_MODULE_DIGEST.md`). Not implemented in
`hos_engine`; the user-demo artifact carries a UX-only approximation.

## Decision
1. **Entities (target model):** CollaborationSpace, Challenge,
   ChallengeMembership, Circle, Commitment, CheckIn, ExperienceCard,
   SupportRequest, Contribution, Outcome, ConsentGrant, ModerationCase.
   ConsentGrant reuses `hos_engine.consent` semantics (purpose-limited,
   revocable, time-boxed) — no parallel consent ontology.
2. **Events (target vocabulary):** challenge_created, challenge_published,
   challenge_joined, challenge_left, commitment_created,
   commitment_renegotiated, checkin_recorded, experience_shared,
   experience_retracted, support_requested, support_accepted,
   outcome_recorded, consent_granted, consent_revoked,
   moderation_case_opened, moderation_case_resolved. Adding them to the
   canonical `event.types.json` + schema enum is a material change —
   **queued as DD-009**, per the source's own requirement of a separate
   ADR, schemas, and constitutional-compatibility tests.
3. **Challenge card contract:** goal/expected result, duration, required
   engagement, participant count, rules, privacy level, data visible to
   others, organizer and role, **risk level**, how to quit, and why
   Human OS recommends it. Public health/financial/psychological challenges
   require risk classification; extreme protocols (e.g. extreme fasting,
   dangerous training competition) are not publishable without additional
   control.
4. **Join-consent screen (normative copy):** joining shares only pseudonym,
   today's-step completion, and voluntary posts; health data, the "O mnie"
   profile, and private notes stay invisible. Circle leaders get no
   automatic access to members' private profiles.
5. **Experience Card:** structured fields (what was tried, situation,
   duration, what happened, what helped, what did not, side effects,
   knowledge type: personal experience / hypothesis / sourced knowledge,
   who it may not suit). Retraction is first-class
   (`experience_retracted`); aggregated AI conclusions must be labeled as
   collective observation, never causal proof.
6. **Privacy/safety floor (from day one):** four visibility levels
   (public/limited/private/anonymous), per-field consent with expiry,
   leave/retract/export rights, block/mute/report, moderator action
   history, and appeal against moderation decisions.

## Consequences
Engine work should reuse: `ConsentRegistry` (grants), Hub registries
(spaces/challenges as entities + relations), `EventStore`/`SQLiteEventStore`
(durable events; `STATE_OBSERVED` until DD-009 lands), and the R0–R4 scale
for challenge risk (mapping to be proposed in the DD-009 change, not
invented ad hoc). ModerationCase has no engine precedent — new design,
with the moderator audit trail on the hash chain.
