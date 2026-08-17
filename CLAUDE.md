# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

Human OS is an experimental **constitutional protocol and reference engine** — not an operating
system in the traditional sense. It's a governance/ethics framework, implemented as a Python
library, whose stated goal is to increase human autonomy, creative agency, and meaningful
relations while *decreasing* dependence on the system itself over time ("Human OS does not decide
what a person's life should become. It helps the person remain the author of that life.").

**This repository is the reference engine and technical implementation of part of a wider Human OS
Initiative — not the whole of it.** The initiative also includes normative layers (a Constitution
far richer than what's summarized in code), human/knowledge/decision models, a Hub, an "Atlas,"
Guardian/Recovery concepts, Lab/Forge, narrative/public artifacts (a White Paper), governance, and
historical provenance living outside this repo. Don't describe or design as if this codebase were
the entire project — see `docs/FOUNDER_REVIEW_2026-08-15.md` and the `Human OS Reconstruction
Audit` referenced there for the fuller picture, and treat any single artifact (including this file)
as a view, not the whole truth.

Current release: **0.9.0 — "Protocol, Identity and Security"**, status **BETA**. Per README.md,
it explicitly lacks authentication, authorization, encryption at rest, independent security
review, and empirical calibration — **do not treat any part of this as production-hardened**,
especially the security modules (see Security section below).

The project layers are, in dependency order (no lower layer may silently redefine a
higher-layer principle — see `ECOSYSTEM.md`):

```
Constitution (constitution/) → HOSS/HOSP spec (spec/, protocol/) → Engine (hos_engine/) → SDK/Hub (sdk/, hub/) → Applications
```

- **Constitution** (`constitution/README.md`) — as of 2026-08-15, a full 21-chapter + 4-appendix
  expansion (values hierarchy, user rights, consent standard, R0–R4 risk scale, AI role
  boundaries, privacy rules, governance roles, amendment process, absolute-ban list, and more),
  not the earlier terse 15-principle summary. The document states its own provenance up top: it's
  a reconstruction from `Human OS Reconstruction Audit`'s reading of the source DOCX, not a
  verbatim transcription — treat exact wording of long lists as provisional until the source
  bytes are directly verified. A closing mapping table shows where each of the old 15 principles
  now lives.
- **Genome registry** (`genome.registry.json`) — 15 "constitutional genes" (GEN-001..015) that
  every material change must be checked against. `CONTRIBUTING.md` and the PR template require
  declaring which genes are supported/at-risk for a change.
- **HOSS** (Human OS Specification, `spec/`) — portable contracts for identity, human records,
  consent, provenance, agents, events, simulations.
- **HOSP** (Human OS Protocol, `protocol/`) — signed message envelopes for cross-component
  communication (`hos.query`, `hos.command`, `hos.event`, `hos.consent.check`,
  `hos.agent.invoke`, `hos.simulation.request`, `hos.receipt`).
- **Engine** (`hos_engine/`) — the executable Python reference implementation.

Much of the process/governance documentation (`GOVERNANCE.md`, `CONTRIBUTING.md`, `SECURITY.md`,
`.github/pull_request_template.md`, `.github/ISSUE_TEMPLATE/*.yml`, `docs/FOUNDER_REVIEW_*.md`) is
written in **Polish**; code, schemas, and most ADRs are in English. Match the language of the doc
you're editing.

## Commands

```bash
python -m venv .venv && source .venv/bin/activate
python -m pip install -e ".[dev]"   # or: make install

python -m pytest -q                 # or: make test
python -m pytest tests/test_engine.py            # single test file
python -m pytest tests/test_engine.py::TestEngine::test_name  # single test (unittest.TestCase style)

python -m ruff check .              # or: make lint
python -m mypy hos_engine           # or: make typecheck (only hos_engine/ is type-checked, not tests/ or sdk/)

python run_demo.py                  # or: make demo

make verify                         # lint + typecheck + test — run this before considering work done
```

CI (`.github/workflows/ci.yml`) runs on Python 3.11/3.12/3.13 and only does `ruff check .` +
`pytest -q` — it does **not** run mypy, even though `make verify` does. Tests are written with
stdlib `unittest.TestCase` (one file per subsystem, `tests/test_<module>.py`) but executed via
pytest.

`pip install -e ".[dev]"` and `ruff check .` were both previously broken (missing
`[tool.setuptools.packages.find]` config; hundreds of stale lint findings) — both are now fixed
and clean as of the "Fix pip install failure" and lint-cleanup commits. `mypy hos_engine` is
**clean (0 errors) as of 2026-08-16** (the historical ~64-error debt in the dense-style
security/agent modules was annotated away without reformatting them) — keep it at zero; adding
mypy as a CI gate is queued as DD-001 in `docs/DEFERRED_DECISIONS.md`.

## Architecture

### Core evaluation flow (`hos_engine/`)

The central object is `HumanOSEngine` (`engine.py`), typically constructed with an
`event_store_path` (see `run_demo.py`). Its main entry point, `evaluate_action(...)`, runs a
proposed action through the **Proof Kernel** (`policy.py`), which checks it against 9
constitutional tests defined in `proof.rules.json` (`PROOF-001`..`PROOF-009`) and returns one of
six `Decision` values: `APPROVED`, `APPROVED_WITH_LIMITS`, `REQUIRES_CONSENT`,
`REQUIRES_HUMAN_DECISION`, `REQUIRES_REDESIGN`, `CONSTITUTIONAL_VIOLATION`.

There is also a separate, simpler declarative rule set at `policies/constitutional.policies.json`
("Human OS Policy JSON v0.1", `POL-001..005`) that expresses similar logic as data. It is not
currently wired to an interpreter in `hos_engine` — treat it as a parallel/ahead-of-code spec
artifact, not the live implementation.

Every entity/event flows through `_emit` in `engine.py`, using the canonical event type strings
in `event.types.json` (mirrored in `schemas/event.schema.json`'s enum).

### Execution-foundation modules (added 2026-08-15, founder continuation directive Phase 3)

A second, newer generation of modules integrates identity, authority, consent, context, Hub
entities, the Constitution, and agents into one coherent, tested execution path — see
`docs/adr/ADR-CORE-001-execution-kernel.md` and `ADR-CORE-002-execution-loop-integration.md` for
the decision record.

- **`hos_core.py`** — `ContextManager`/`ContextPackage` (versioned, genuinely immutable context
  snapshots via `types.MappingProxyType`) and `EventEngine`/`ExecutionContract`/`ExecutionEvent`
  (the minimum execution contract: goal, owner, context, required permissions, budget, abort
  criteria, an in-memory lifecycle event log). This is a first slice of the much larger specified
  "HOS Core" (8 sub-modules; only Context Manager and Event Engine exist so far).
- **`hub_entity_registry.py`** — `EntityRegistry` (six MVP entity types — `PERSON, GOAL,
  KNOWLEDGE_CLAIM, DECISION, EXPERIMENT, RESOURCE` — explicitly marked `MVP_IMPLEMENTED_SUBSET`,
  not the canonical ontology) and `RelationRegistry` (17 typed relation verbs from the Hub
  Entity-First spec, e.g. `REALIZUJE`, `NALEZY_DO`; per-relation confidence and a
  `valid_from`/`valid_to` window). Duplicate entities are never auto-merged — `merge()` requires
  `reason`/`evidence`/`approved_by` and records a `MergeRecord`; the retired entity becomes
  `SUPERSEDED`, never deleted.
- **`authority.py`** — `AuthorityRole` (`OWNER, OPERATOR, TRUSTED_DELEGATE, RECOVERY_CUSTODIAN,
  AGENT, SERVICE, GUEST, SYSTEM_PROCESS`) and `RoleGrantRegistry`. This is deliberately a **second,
  separate axis** from `security_identity.IdentityType` (`HUMAN, AGENT, APPLICATION, SERVICE,
  HUB`) — identity *kind* and authority *role* are not the same thing (a `HUMAN` identity can hold
  an `OWNER` role); see the Q9 correction in `docs/FOUNDER_REVIEW_2026-08-15.md`. Do not merge
  these two enums or treat one as replacing the other without redoing that analysis.
- **`execution_loop.py`** — `ExecutionLoop.execute(HumanIntent) -> ExecutionResult` walks a human's
  declared intent through IDENTITY → AUTHORITY ROLE → CONSENT → CONTEXT → ENTITY RETRIEVAL →
  CONSTITUTIONAL CHECK (Proof Kernel) → AGENT EXECUTION (`agent_runtime.AgentRuntime`, its own
  human-approval gate included) → RECEIPT → EVENT (optionally to `SQLiteEventStore` for a
  verifiable hash chain) → STATE UPDATE → optional GRAPH relation (`fulfills_entity_id` →
  `REALIZUJE`) → AUDIT. **Refusal at any gate is a first-class `IntentOutcome.REFUSED_*` result,
  never an exception**, and stops the loop before anything downstream executes or persists — this
  matches the project-wide "hard gate before scoring" pattern already used by the Proof Kernel.
  This is a bounded slice: it does not yet touch `knowledge_graph.py` (a separate, unreconciled
  model — see `docs/RELATION_VOCABULARY_CROSSWALK.md`) and has no Recovery/SAFE MODE integration
  (blocked on a source document not yet available — see Q12 below).
- **`recovery.py`** (added later on 2026-08-15, audit-plan Phase 4) — the first slice of the
  Sovereign Recovery Kernel (`ADR-RECOVERY-001..004` under `ADR-RECOVERY-006`'s resolutions):
  seven `EmergencyMode`s each mapped to the Constitution's R0–R4, protective modes
  (SAFE_MODE/READ_ONLY/FREEZE/DISCONNECT) may auto-trigger only with owner notification and are
  unconditionally owner-reversible, consequential modes (ROLLBACK/EXPORT/RECOVERY) are manual-only,
  with dual-key custodian approval (a *different* identity holding `RECOVERY_CUSTODIAN`) for
  ROLLBACK/RECOVERY. Structural guarantees: no API exists to mutate policy or the audit log (agents
  can't disable what has no setter); AGENT/SERVICE/SYSTEM_PROCESS can never activate or deactivate,
  and the refusal itself is logged as a 13-field `EmergencyEvent`; zero AI/external dependencies.
  Refusal here is an **exception** (`RecoveryRefused`), deliberately unlike `ExecutionLoop`'s
  outcome-object style — ignoring a refused protection must not look like having it. Activations
  are scope-isolated and time-bounded; `freeze_entity()` reuses `HubEntityStatus.SUSPENDED`
  (FROZEN=SUSPENDED per founder decision). **All six Hub contracts from the source's §9 are now
  implemented**: Register Recovery Event (activate + log), Freeze Entity/Scope,
  `create_recovery_snapshot` (non-destructive checkpoint), `rollback_entity` (new version from
  snapshot + provenance via the registry's attributed merge — old version SUPERSEDED, never
  deleted), `disconnect_representation` (detach with the historical relation preserved as a
  record), `export_sovereign_package` (portable open-JSON package incl. retired history and the
  audit trail). Remaining: Emergency Root key infrastructure, `recovery_*` event types (durable
  events use `STATE_OBSERVED` meanwhile — DD-003 in `docs/DEFERRED_DECISIONS.md`).
- **`decision_engine.py`** (added later on 2026-08-15, audit-plan Phase 3) — the first MVP slice of
  Layer 5's Decision & Recommendation Engine (`ADR-DECISION-001..005`):
  `DecisionEngine.decide(DecisionRequest) -> DecisionOutcome` runs the nine hard gates G0–G8
  *before* any ranking (non-commutable: a gate-excluded candidate never re-enters), applies the
  evidence-asymmetry rule (declared evidence 0–5 vs. `RiskReactionClass`; `R-KRYTYCZNE` is never
  admissible), and returns abstention (eight named `AbstentionReason`s) and soft/conditional/hard
  escalation as first-class `DecisionOutcomeKind`s, never exceptions. Two ADR-DECISION-005
  invariants are enforced by code and dedicated tests: `user_determination` is read by nothing, and
  `sponsored` is absent from the ranking key. Like the Proof Kernel, it evaluates declared inputs
  only; the ten-axis §18 profile and live Knowledge Map integration are not implemented. Not yet
  wired into `ExecutionLoop` — the two compose at the caller's discretion. **DI/IQ/AR scales are
  wired in SHADOW mode only (2026-08-17):** `decision_scales.py` holds the skeleton types (DD-006)
  plus `load_policies_json()` for the founder-signed policies in
  `policies/scale.interpretation.policies.json`; `DecisionEngine(shadow_interpreters=...)`
  interprets `DecisionRequest.measurements` and attaches `DecisionOutcome.shadow_interpretations`
  only *after* the decision is fully computed — structurally unable to change gates, ranking, or
  outcome. Promotion to operational mode is a separate founder decision; no such code path exists.

- **`experiment_engine.py`** (added 2026-08-17, founder directive "działaj z tą warstwą") — the
  first executable slice of Layer 6's Experiment Engine (`ADR-EXP-001..005`,
  `docs/LAYER_6_EXPERIMENT_ENGINE_DIGEST.md`): Layer 6's own scales (`ProcessClass` XP-0..XP-8
  with XP-8 rejected outright, `SafetySeverity` SE0–SE4 with default reactions SE2→HOLD,
  SE3/SE4→STOP+escalate, `BaselineQuality` BL0–BL5 — all distinct from the Constitution's R0–R4),
  the eight-question "test nadrzędny" launch gate (`MasterTest`), non-fungible gates per
  ADR-EXP-002 (consent/guard-metric/stop-rules/baseline gate independently; no compensation
  parameter exists), `AGENT`/`SERVICE`/`SYSTEM_PROCESS` structurally refused at launch/resume
  (refusal logged), XP-7 requiring specialist approval+legality+monitoring with no
  user-determination override, observations never merged across `ObservationSource`s,
  post-result hypothesis amendments versioned and flagged exploratory, thresholds frozen at
  launch (moving them forces an exploratory result), XP-6 forced into the `INTERPRETIVE`
  evidence domain (`causal_evidence_eligible=False` — the epistemic firewall), and
  `INCONCLUSIVE` as a first-class outcome. Refusals are outcome objects (`LaunchDecision`/
  `TransitionResult`), never exceptions. Durable events use `STATE_OBSERVED` with
  `experiment_*` payload kinds (same interim pattern as DD-003). Not yet implemented: adaptive
  experiments, portfolio limits, trajectory model, community contribution, EC/MQ/PF/DQ/CA/PE
  scales. **Distinct from `simulation.py`** (ADR-0006's what-if scenario engine) — do not
  conflate the two. The app's client-side N-of-1 logic in `apps/user-demo` predates this module
  and is not yet backed by it.
- **`self_model.py`** (added 2026-08-16, founder implementation directive "Conversational About
  Me / Living Self Model", `ADR-SELFMODEL-001`) — the conversational-self-model slice, built **on
  top of `human_model.py`** (which already had the epistemic core: `EvidenceType`, confidence,
  provenance, `supersedes` versioning, `CONTESTED`) rather than as a parallel ontology.
  `InteractionLog` (`HOS-CNV-`/`HOS-MSG-`, three `InteractionMode`s) keeps conversations strictly
  separate from the model — appending a message never creates a record. `SelfModelService` adds
  the lifecycle: `declare`/`observe`/`hypothesize` (hypothesis requires evidence refs), user-only
  `confirm`/`reject`/`correct`/`mark_outdated` (always via the supersedes chain — history is never
  rewritten; reject = CONTESTED, never delete), `Tension` (contradictions are signal, only the
  subject resolves), `living_view` (epistemically split sections, sensitive hidden by default),
  `why()` (full provenance: quotes, creator, band, history), `decision_inputs()` (split feed —
  a hypothesis is never presented as a declaration), optional `ConsentRegistry` gate (no consent →
  utterance stays interaction-only). `confidence_band()` gives UI LOW/MEDIUM/HIGH — never raw
  numbers. NO NLP/extraction in the engine — candidate identification is an app/agent concern.
  `HumanRecord` gained optional `valid_from`/`valid_to`/`last_confirmed_at`/`evidence_refs` (same
  compatibility pattern as ADR-HUMAN-004). See the ADR for deliberately-unreconciled conflicts
  (HYPOTHESIS vs AI_INFERENCE convention; third status vocabulary; knowledge-graph overlap).

### ID and schema conventions

- All object IDs follow `HOS-<PREFIX>-######` (e.g. `HOS-HUM-000001`, `HOS-ACT-000002`), enforced
  by both `hos_engine/ids.py::IdGenerator` and `schemas/common.schema.json#/$defs/HOSId`
  (`^HOS-[A-Z]{2,8}-[0-9]{6,}$`).
- **Two ID-generation strategies coexist**: the counter-based `IdGenerator` (used by `engine.py`
  and older modules) and ad hoc `uuid.uuid4().hex[:12].upper()`-based generation used by newer
  modules (`agent_runtime.py`, `human_model.py`, `consent.py`, `security_identity.py`,
  `simulation.py`, `key_rotation.py`, and the newest execution-foundation modules —
  `hos_core.py`'s `HOS-CTX-`/`HOS-EXE-`/`HOS-COR-`/`HOS-CEV-`, `hub_entity_registry.py`'s
  `HOS-ENT-`/`HOS-REL-`/`HOS-MRG-`, `authority.py`'s `HOS-ROL-`, `execution_loop.py`'s
  `HOS-INT-`/`HOS-REQ-`/`HOS-EVT-`, `decision_engine.py`'s `HOS-DEC-`, `recovery.py`'s
  `HOS-RCV-`/`HOS-EMG-`). Match whichever pattern the module you're editing already uses.
- `schemas/` holds 14 JSON Schema (Draft 2020-12) files. Every concrete entity schema (`action`,
  `human`, `intent`, `flow`, `knowledge`, `relation`, `system`) does
  `allOf: [{ $ref: entity.schema.json }, {...}]` against the shared base in
  `entity.schema.json`/`common.schema.json`. Validation against these schemas is done through
  `hos_engine/validation.py::SchemaRegistry` (`jsonschema.Draft202012Validator` +
  cross-schema `$ref` resolution). None of the new execution-foundation modules have JSON Schemas
  yet — they're plain dataclasses.
- `schemas/common.schema.json`'s `Version` pattern is pinned to `^0\.2\.[0-9]+$`, which is stale
  relative to the actual project version (0.9.0) and component versions in `manifest.json` — be
  aware of this drift rather than "fixing" it silently in unrelated changes.
- `state_machine.py::ALLOWED_TRANSITIONS` governs the entity `status` field
  (`draft, active, paused, completed, archived, revoked`), matching `entity.schema.json`. This is
  a **different** lifecycle from `hub_entity_registry.HubEntityStatus`
  (`PROPOSED, ACTIVE, SUSPENDED, SUPERSEDED, ARCHIVED`) — the two are kept separate on purpose.

### Persistence

Two parallel persistence layers exist — pick based on what the module you're touching already
uses, don't mix:
- `event_store.py::EventStore` — simple JSONL append-only file (used by `engine.py`, the demo, and
  optionally `execution_loop.py`).
- `sqlite_store.py::SQLiteEventStore` — SQLite with a SHA-256 hash chain
  (`previous_hash`/`event_hash`, canonical JSON) and a `verify_chain()` integrity check.
  `execution_loop.ExecutionLoop` accepts either `EventStore` or `SQLiteEventStore` for its
  `event_store` parameter (both share the same `append(dict)` shape) — prefer `SQLiteEventStore`
  when a caller cares about provenance, not just a log.
- `graph_store.py::SQLiteGraphStore` — SQLite-backed knowledge graph storage (for
  `knowledge_graph.py`, not `hub_entity_registry.py`).
- `self_model_store.py::SQLiteSelfModelStore` — SQLite snapshot persistence for the Living Self
  Model (`HumanModel` records incl. the supersedes chain, `InteractionLog` conversations/messages,
  tensions); same snapshot-not-event-log semantics and `restore`-constructor pattern as
  `hub_store.py`. The lifecycle audit trail stays in the event stores.
- `hub_store.py::SQLiteHubStore` — SQLite snapshot persistence for the Hub's
  `EntityRegistry`/`RelationRegistry` (entities, relations, merge records, duplicate flags).
  Snapshot semantics, not an event log: `save_snapshot` atomically rewrites state and
  `load_registries` rebuilds via the registries' explicit `restore` constructors (ids/timestamps
  verbatim, no private-field pokes). Durable history stays in the event stores.
- `replay.py::rebuild_entities` reconstructs entity state from the event log (distinct from
  `replay_guard.py`, see Security below — don't confuse the two "replay" modules).
- `hos_core.EventEngine` is **not** durable persistence — it's an in-memory execution-lifecycle
  coordinator. Don't treat its log as a substitute for `EventStore`/`SQLiteEventStore`, and don't
  let a third, unrelated notion of "the event log" grow elsewhere; route new durable events through
  one of the two real stores.

### Security modules (`hos_engine/`)

`security_identity.py` (identity/key registry), `protocol_security.py` (`HMACSigner`,
`canonical_json`, `secure_envelope` — protocol tag `HOSP/0.2`), `replay_guard.py::ReplayGuard`
(nonce/expiry/message-id tracking, distinct from `replay.py`'s event-replay-for-state-rebuild),
`trust.py` (`TrustRegistry`/`TrustPolicy`/`TrustLevel`), `security_gateway.py::SecurityGateway`
(the check pipeline matching `protocol/security-profile.md`'s 10-step order: resolve identity →
verify active → validate key binding → verify signature → reject expired/replayed → trust policy
→ consent → capability checks → execute/deny → issue receipt), `key_rotation.py`, and now
`authority.py::RoleGrantRegistry` (a separate axis from identity, see above) and
`call_authorization.py::CallAuthorizer` (per-call authorization closing AR-003's gap, 2026-08-17:
declarative per-capability `CallRule`s — argument key/value/size constraints plus
delegation-context limits — consulted by `AgentRuntime.evaluate` before tool execution; the
stance toward unruled capabilities (`UnruledPolicy.ALLOW/DENY`) must be declared explicitly,
never defaulted; conventional style, unlike the dense group).

`security/THREAT_MODEL.md` states explicitly that the current HMAC implementation is a **local
reference mechanism only** — production would need asymmetric signatures, protected key storage,
encrypted transport, trusted time, and rate limiting. Don't present it as production-grade in
docs or comments.

`sdk/python/human_os_sdk/` defines its own `ProtocolEnvelope` (protocol tag `HOSP/0.1`), which is
an older/different shape from `hos_engine.protocol_security.secure_envelope` (`HOSP/0.2`) — two
overlapping envelope representations exist; check which one a given call site expects.

**Not implemented, design gaps now resolved:** SAFE MODE and the Sovereign Recovery Kernel (the
owner's inalienable "stop the system" rights) have zero code. The source document
(`Human_OS_Sovereign_Recovery_Layer_i_Rejestr_Scalenia_v0_2_1.docx`) was received 2026-08-15 and is
fully digested (`docs/RECOVERY_LAYER_DIGEST.md`, `ADR-RECOVERY-001..005`); the four highest-severity
gaps the source left unresolved (`RECOVERY_CUSTODIAN` role justification, mapping emergency modes
to R0–R4, auto-vs-manual triggering per mode, `FROZEN`/`SUSPENDED` naming) were put to the founder
directly the same day and resolved — see `ADR-RECOVERY-006`. Implementation may now proceed against
`ADR-RECOVERY-001..004` plus `ADR-RECOVERY-006`'s resolutions; it simply hasn't been built yet.
Lower-severity open items from `ADR-RECOVERY-005` (concrete TTL values, governance-role mapping
beyond `RECOVERY_CUSTODIAN`, genome-registry references, etc.) remain unresolved and non-blocking.

### Module style split

Most of `hos_engine/` (`engine.py`, `models.py`, `policy.py`, `event_store.py`, `sqlite_store.py`,
`flow.py`, `state_machine.py`, `ids.py`, `validation.py`, `knowledge_graph.py`, `graph_store.py`,
and the newer **`hos_core.py`, `hub_entity_registry.py`, `authority.py`, `execution_loop.py`,
`decision_engine.py`, `recovery.py`**) is conventionally formatted (4-space indent, one statement
per line). A distinct, separate group —
`agent_runtime.py`, `human_model.py`, `consent.py`, `personalization.py`, `security_identity.py`,
`trust.py`, `security_gateway.py`, `key_rotation.py`, `simulation.py`, `simulation_gate.py`,
`protocol_security.py`, `replay_guard.py` — uses a dense, semicolon-joined, single-line style
(e.g. `class TrustLevel(str, Enum): UNTRUSTED = "UNTRUSTED"; ...`). This is a consistent,
intentional pattern in that group, not a formatting accident — match the style of whichever file
you're editing rather than reformatting it to match the other group. New "core"/foundational
modules should default to the conventional style, matching the newest additions above.

`hos_engine/__init__.py` re-exports most submodules via `from .X import *`, plus an explicit,
alphabetically-sorted `__all__` covering the names that aren't reachable through a star-import
(fixed 2026-08; previously incomplete, which caused lint failures) — when adding a new
top-level-importable name via explicit `from .X import Name`, add it to `__all__` too, or `ruff`
will flag it as an unused import.

### Other components

- `hub/` is documentation-only (no code yet) for the **full** Hub spec: describes routing HOSP
  messages, resolving identifiers, verifying consent, discovering services, and issuing receipts,
  without owning the human profile itself. `hos_engine/hub_entity_registry.py` (above) is a first
  code slice of *part* of this (entity/relation registries only) — it is not the whole Hub.
- `sdk/python/human_os_sdk/` directly imports from `hos_engine` — it is a thin convenience
  wrapper, not a decoupled client library.
- `apps/user-demo/` — the single-file personal user app (HTML/JS, no build, no backend),
  committed per DD-005 as an exact copy of the artifact under active development.
  UX-ONLY PROTOTYPE: `localStorage` state, synthetic data, no auth, no promotion to Core/Hub.
  It re-implements engine *patterns* client-side (self-model epistemics, decision gates,
  recovery modes, Commons per ADR-COMMONS-001/002, freemium tiering per ADR-APP-001 —
  export/exit/model/emergency modes are never paywalled). Distinct from `app/` (the Flask
  Proof Kernel console). Its E2E tests (Playwright, `node test_*.js`) live in the artifact
  scratchpad, not in this repo.
- `docs/adr/` contains architecture decision records. Three populations exist:
  - `ADR-0002` through `ADR-0008` — original engine ADRs, each backing an implemented, tested
    component. Note `ADR-0006-simulation-laboratory.md` documents the code-level what-if scenario
    engine in `hos_engine/simulation.py` — a **different concept** from "Human OS Lab" below
    despite the shared word "lab"/"laboratorium"; do not conflate the two.
  - `ADR-HUB-001..006`, `ADR-CORE-001/002`, `ADR-GRAPH-002`, `ADR-AGENT-001/002`, `ADR-WORLD-001`,
    `ADR-USER-002`, `ADR-PRED-001`, `ADR-AUDIT-001`, `ADR-IMPL-001`, `ADR-ARCH-002` — imported
    2026-08-15 from DOCX specifications (see `docs/FOUNDER_REVIEW_2026-08-15.md` Q11), and later
    the same day **verified sentence-by-sentence against the original source docx bytes**
    (`Human_OS_Rozszerzenie_Architektury_i_Integracja_v0_2_1.docx`) once the founder supplied them
    — the secondhand reconstruction matched closely, no content corrections were needed. Most are
    "accepted direction, not yet implemented"; `ADR-CORE-001`/`ADR-CORE-002` back the
    execution-foundation modules above and are implemented.
  - `ADR-LAB-001..006` — imported 2026-08-15 from `Human_OS_Lab_Specyfikacja_i_Interface_v0_1.docx`,
    describing **Human OS Lab**: a tester-facing sandbox product (Lab Shell, Experiment Engine,
    Sandbox Data, Agent Arena, Trace & Audit, Feedback Loop, Promotion Gate) with a v0.1 clickable
    UX-only prototype (no backend, no auth, `localStorage`-only demo data). No code implements this
    yet. Distinct from `ADR-0006`'s simulation laboratory (see above).
  - `ADR-EXP-001..005` — formulated 2026-08-15 from `Human_OS_Warstwa_6_Silnik_Eksperymentow...docx`
    (Layer 6, the personal N-of-1 experiment engine — hypothesis, protocol, baseline, safety
    monitoring, analysis, and opt-in anonymized community contribution). Unlike the ADRs above,
    this source contains **no ADR numbering of its own** — these five were newly written from its
    axioms/reference-architecture/acceptance-criteria sections, not extracted verbatim; see
    `docs/LAYER_6_EXPERIMENT_ENGINE_DIGEST.md` for the full structural digest this drew from. Layer
    6 defines its own risk/safety scales (XP0–XP8, SE0–SE4, and others) — **do not confuse these
    with the Constitution's R0–R4** (different taxonomy, different layer). No code implements any
    of Layer 6 yet; `hub_entity_registry.HubEntityType.EXPERIMENT` is only a bare label.
  - `ADR-RECOVERY-001..006`, `ADR-DECISION-001..005`, `ADR-KNOWLEDGE-001..005`,
    `ADR-HUMAN-001..005`, `ADR-USERMODEL-001..006` — formulated 2026-08-15 from five more
    founder-provided source docs, none with their own ADR numbering: the **Sovereign Recovery
    Layer** (the long-blocked source for SAFE MODE — see below), **Layer 5** (Decision &
    Recommendation Engine, upstream of Layer 6), **Layer 3** (Knowledge Map & Information
    Signature), **Layer 2** (Human Model), and **Layer 4** (User Model & Digital Profile). Each has
    a full structural digest: `docs/RECOVERY_LAYER_DIGEST.md`,
    `docs/LAYER_5_DECISION_ENGINE_DIGEST.md`, `docs/LAYER_3_KNOWLEDGE_MAP_DIGEST.md`,
    `docs/LAYER_2_HUMAN_MODEL_DIGEST.md`, `docs/LAYER_4_USER_MODEL_DIGEST.md`. **Layer 4 was
    originally a different source document from the one behind `ADR-USER-002`**, flagged in
    `ADR-USERMODEL-005` as a sibling-not-duplicate specification — founder decision the same day
    (`ADR-USERMODEL-006`) merged the two: Layer 4's R0–R8/24-object structure is now canonical,
    `ADR-USER-002`'s nine components survive as a named view over it (mapping table in
    `ADR-USERMODEL-006`), and "Human Digital Twin" is retired as the model's primary name in favor
    of Layer 4's own "Model Użytkownika i Cyfrowy Profil Rozwojowy". Similarly, `ADR-RECOVERY-006`
    records founder resolutions for the four gaps `ADR-RECOVERY-005` originally left blocking (see
    "Not implemented" note below). Each layer defines its own coded risk/quality scale, all
    mutually distinct and distinct from the Constitution's R0–R4 — five independent taxonomies now
    exist across the digested layers; never
    assume a shared meaning across scales that merely share a letter.
  - `docs/FOUNDER_REVIEW_2026-08-15.md`'s "Czwarta tura" section (Sovereign Recovery) is the
    canonical place to check before writing any SAFE MODE / Recovery code: `ADR-RECOVERY-005`
    lists four specific unresolved gaps (the `RECOVERY_CUSTODIAN` role has no source justification,
    no mapping to R0–R4, no resolved auto-vs-manual trigger rule, inconsistent `FROZEN`/`SUSPENDED`
    naming) that should block implementation until resolved with the founder — the source itself
    describes itself as "wymaga implementacji technicznej i testów" (a normative decision, not a
    finished technical spec).
  Check these before making architectural changes, and add a new ADR for any decision of similar
  weight.
- `docs/FOUNDER_REVIEW_2026-08-15.md` is the live decision record for open questions raised by the
  `Human OS Reconstruction Audit` — check it before assuming a design question is still open. It
  now spans three rounds of corrections as the founder has supplied more original source files;
  read to the end, not just the initial Q1–Q13 answers.
- `docs/HOS_ENTITY_RELATION_EVENT_SCHEMA_v0.1.md` — the artifact `ADR-IMPL-001` names as the next
  mandatory step before further domain-module work: a consolidated index of every entity/relation/
  event/status/risk-scale vocabulary that exists across the codebase and digested layer specs, with
  IDs, validation, migration, error-contract, and minimal-API sections. It resolves nothing new —
  every parallel vocabulary it lists (Hub vs. Formal Entity Model, the five risk/quality scales,
  the three status vocabularies) stays deliberately unreconciled; read it before assuming any two
  of them are equivalent.
- `docs/RELATION_VOCABULARY_CROSSWALK.md` — a provisional, explicitly incomplete mapping between
  the Hub's relation vocabulary (`hub_entity_registry.HubRelationType`, fully sourced) and a
  separate "Formal Entity & Relation Model" vocabulary known only secondhand (source DOCX bytes
  not yet available). Don't assume a 1:1 mapping between the two without checking this document.
- `docs/white_paper/` — the first White Paper content committed to this repo (2026-08-15): a 1:1
  transcription of Chapter III ("Technologia, która pamięta, komu ma służyć"), now **complete** —
  main/overview text plus all four parts (A–D), each its own file, plus `rozdzial-III-pelny.md`
  concatenating all five for continuous reading (a convenience, not a separate edit — the per-part
  files remain the source of truth). See its `README.md` for provenance per file.
- `docs/LAYER_6_EXPERIMENT_ENGINE_DIGEST.md` — a full structural digest (Polish, matching the
  source language) of Layer 6's source docx: metadata, all coded scales, the 15-object experiment
  ontology, all appendix field lists, the full 47-section table of contents, and every literal
  prohibition. Read this before extending `ADR-EXP-*` or building anything experiment-related —
  it's more complete than the ADRs alone.
- `docs/runtime-contract.md` and `docs/simulation-contract.md` predate this session's audit work —
  short, standalone I/O contracts for `evaluate_action` (inputs/outputs/non-goals) and the
  simulation engine (`docs/adr/ADR-0006-simulation-laboratory.md`'s scenario/invariant/score-
  distribution shape) respectively. `docs/self-model-contract.md` and `docs/recovery-contract.md`
  (added 2026-08-16) do the same for `self_model.py` and `recovery.py` — including the per-mode
  risk/auto-trigger/dual-key table. `docs/call-authorization-contract.md` (added 2026-08-17) does
  the same for `call_authorization.py` and its `AgentRuntime` integration point. Check the
  relevant contract doc before changing any of these code paths' public shape.

## Licensing

Code is Apache-2.0 (`LICENSE`); documentation/specifications are CC BY 4.0 (`LICENSE-DOCS`). The
"Human OS" name/marks have a simple working trademark policy as of 2026-08-15 (name/marks identify
the official project and its governance, separate from the code/docs licenses per Apache-2.0's own
trademark clause; forks are fine but shouldn't present themselves as "Human OS") — it is explicitly
not a formal legal opinion, see `LICENSE-DECISION.md`.

## Contribution conventions

Per `CONTRIBUTING.md` and `.github/pull_request_template.md`, every material change is expected
to describe:
- which constitutional genes (`genome.registry.json`) it supports,
- which genes it places at risk, and the safeguards for that,
- limitations/uncertainty,
- impact on portability and exit (a user's ability to leave/export unaffected).

Constitution changes go through a separate governance process with a higher acceptance bar
(`GOVERNANCE.md`) — per `docs/FOUNDER_REVIEW_2026-08-15.md`, treat "would this change a
constitutional rule?" as a real escalation trigger requiring explicit human sign-off, not just a
code-review nicety. Security issues should be reported privately rather than as public issues
(`SECURITY.md`).
