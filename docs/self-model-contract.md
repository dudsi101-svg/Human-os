# Self-model contract (Living Self Model, `hos_engine.self_model`)

Status: first vertical slice (ADR-SELFMODEL-001). Style follows
`runtime-contract.md`: this is the public I/O shape, not an API reference.

## Inputs
- Interactions: conversations appended to `InteractionLog`
  (`HOS-CNV-`/`HOS-MSG-`; three modes: NATURAL, DEEP_DISCOVERY, EXPLORATORY).
- Candidate structured information, already identified by the application
  or an agent (the engine does no NLP): a declaration, an observation, or
  a hypothesis with supporting evidence refs.
- User lifecycle decisions: confirm, reject, correct, mark outdated,
  resolve tension — subject-only.

## Outputs
- `HumanRecord`s with epistemic class (`EvidenceType`), interpretation
  confidence, provenance (`evidence_refs` → messages), temporality
  (`valid_from`/`valid_to`/`last_confirmed_at`), versioned via the
  `supersedes` chain.
- `Tension` records — contradictions preserved as signal.
- `living_view(subject_id)` — sections split by epistemic status;
  sensitive hidden unless explicitly requested.
- `why(record_id)` — full provenance: quotes, creator, confidence band,
  status history.
- `decision_inputs` / `decision_context` — epistemically split feeds;
  `decision_context` marks gate-grade (declared/confirmed/observed) vs
  advisory-only (hypotheses).
- Optional durable audit: every lifecycle transition appended to an event
  store (`STATE_OBSERVED` until DD-003 lands dedicated types).
- Snapshot persistence: `SQLiteSelfModelStore.save_snapshot` /
  `load_service` — current state (records incl. supersedes chain,
  conversations, tensions) survives a process restart verbatim; the audit
  trail stays in the event stores.

## Guarantees
- The chat is not the user model: appending a message never creates a record.
- History is never rewritten: every change is a superseding record;
  rejection is CONTESTED, never deletion.
- Only the subject confirms, rejects, corrects, outdates, or resolves.
- A hypothesis without user confirmation never gains declaration authority
  (evidence asymmetry, enforced structurally in `decision_context`).
- No consent → no model write; the utterance stays interaction-only.
- Confidence reaches the UI only as LOW/MEDIUM/HIGH bands.

## Non-goals
- extracting information from raw text (application/agent concern),
- resolving contradictions automatically,
- profile completeness, personality scoring, or any "quality of person" metric,
- treating AI inference as user truth.
