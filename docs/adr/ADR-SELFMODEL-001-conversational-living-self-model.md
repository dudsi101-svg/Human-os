# ADR-SELFMODEL-001: Conversational "About Me" — Living Self Model First Slice

## Status
Accepted and implemented (first vertical slice), 2026-08-16. Source: founder
implementation directive "Conversational About Me / Living Self Model"
(delivered in-session, 2026-08-16; no external source document). Related:
`ADR-HUMAN-001..005` (Layer 2 Human Model), `ADR-USERMODEL-001..006`
(Layer 4 User Model), `ADR-DECISION-001..005` (Decision Engine inputs).

## Context
The directive requires the "About Me" experience to be conversation-first
("CONVERSATION ON THE FRONT, STRUCTURED USER MODEL UNDERNEATH") while
strictly separating four epistemic classes: what the user said, what was
observed, what the AI inferred, and what the user confirmed. It explicitly
forbids building a parallel user ontology.

**Phase 1 audit finding:** `hos_engine.human_model` already carries the
epistemic core: `EvidenceType` (USER_DECLARATION, OBSERVATION,
VERIFIED_FACT, AI_INFERENCE, HYPOTHESIS), confidence in [0, 1], provenance
(`source_id`), a `supersedes` chain (versioning without overwriting),
subject-only `contest` (CONTESTED status), `sensitive`, `consent_scope`.
`hos_engine.consent.ConsentRegistry` already provides purpose-limited,
revocable, sensitivity-aware authorization. Therefore this slice **extends
HumanModel instead of creating a new ontology**.

## Decision
1. **`HumanRecord` extended** with optional `valid_from`, `valid_to`,
   `last_confirmed_at` (temporality: the model is a hypothesis in time) and
   `evidence_refs` (multi-source provenance). Optional-with-defaults, same
   compatibility pattern as ADR-HUMAN-004's metadata fields.
2. **New module `hos_engine/self_model.py`**:
   - `InteractionLog` (`HOS-CNV-`/`HOS-MSG-` ids, three
     `InteractionMode`s: NATURAL, DEEP_DISCOVERY, EXPLORATORY). THE CHAT IS
     NOT THE USER MODEL: appending messages never creates records; records
     reference messages, never the reverse.
   - `SelfModelService` — epistemic bookkeeping on top of `HumanModel`:
     `declare` / `observe` / `hypothesize` (hypothesis requires supporting
     evidence refs and records `created_by` + alternatives), user-only
     `confirm` / `reject` / `correct` / `mark_outdated` (all via the
     supersedes chain — history is never rewritten; rejection = CONTESTED,
     never deletion), `Tension` records (contradictions are signal; only
     the subject may resolve them), `living_view` (sections split by
     epistemic status, sensitive hidden by default), `why` ("where does
     Human OS know this from?" — quotes, interaction ids, creator,
     confidence band, status history), `decision_inputs` (epistemically
     split feed; a hypothesis is never presented as a declaration).
   - `confidence_band` — UI sees LOW/MEDIUM/HIGH, never falsely precise
     numbers. Confidence always means *interpretation* confidence; the fact
     that the user said something is carried by message provenance.
   - Optional consent gate: with a `ConsentRegistry` + grantee wired in,
     every write is purpose/domain/action/sensitivity-authorized; without
     consent the utterance stays interaction-only (conversation without
     profiling is possible by construction).
3. **Candidate extraction is out of scope for the engine.** No NLP, no
   `extract_profile()`: deciding that an utterance contains a candidate is
   an application/agent concern (the interview UX lives in the app layer).

## Documented conflicts (not silently resolved)
- `EvidenceType` has both `AI_INFERENCE` and `HYPOTHESIS`; the directive
  uses one class "AI HYPOTHESIS". Convention adopted here: `HYPOTHESIS` for
  conversational interpretations awaiting user confirmation; `AI_INFERENCE`
  reserved for data-derived inferences. Both are surfaced in the same
  "hypotheses" section of `living_view`. A future ADR may merge them; this
  one only records the convention.
- The record lifecycle here (ACTIVE/CONTESTED/SUPERSEDED via HumanModel) is
  intentionally **not** `HubEntityStatus` (PROPOSED/ACTIVE/SUSPENDED/…)
  and not `state_machine.ALLOWED_TRANSITIONS` — a third status vocabulary
  already listed in `docs/HOS_ENTITY_RELATION_EVENT_SCHEMA_v0.1.md` stays
  deliberately unreconciled.
- Overlap with `knowledge_graph.py` claims and Hub `KNOWLEDGE_CLAIM`
  entities remains unreconciled (same status as before this ADR; see
  `docs/RELATION_VOCABULARY_CROSSWALK.md`). Self-model records live in
  Layer 2's HumanModel; promoting them to Hub entities is future work.

## Consequences
- 18 tests in `tests/test_self_model.py` cover the directive's 12 required
  cases (declaration, unconfirmed hypothesis, confirmation, rejection,
  correction, contradiction, staleness, provenance, versioning,
  no-history-overwrite, consent/purpose, interaction-vs-model separation).
- The Decision Engine can consume `decision_inputs` at the caller's
  discretion (composition pattern consistent with the rest of the engine);
  no wiring inside `DecisionEngine` was changed.
- Temporary/MVP elements: `created_by`/alternatives ride in `tags`
  (`created_by:`/`alt:` prefixes) rather than dedicated fields;
  `missing_critical_information` in `decision_inputs` is an empty
  placeholder; interview adaptivity lives only in the demo app layer.
