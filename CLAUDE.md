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
and clean as of the "Fix pip install failure" and lint-cleanup commits. `mypy hos_engine` still has
pre-existing, uncorrected debt (~64 errors, mostly in the dense-style security/agent modules) —
don't assume `make verify` starts from a clean baseline on that front; when touching a file, check
that your diff doesn't introduce *new* mypy errors rather than expecting the full run to be green.

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
  `HOS-INT-`/`HOS-REQ-`/`HOS-EVT-`). Match whichever pattern the module you're editing already
  uses.
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
  `knowledge_graph.py`, not `hub_entity_registry.py` — the Hub's `EntityRegistry`/`RelationRegistry`
  are in-memory only so far, no persistence layer yet).
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
`authority.py::RoleGrantRegistry` (a separate axis from identity, see above).

`security/THREAT_MODEL.md` states explicitly that the current HMAC implementation is a **local
reference mechanism only** — production would need asymmetric signatures, protected key storage,
encrypted transport, trusted time, and rate limiting. Don't present it as production-grade in
docs or comments.

`sdk/python/human_os_sdk/` defines its own `ProtocolEnvelope` (protocol tag `HOSP/0.1`), which is
an older/different shape from `hos_engine.protocol_security.secure_envelope` (`HOSP/0.2`) — two
overlapping envelope representations exist; check which one a given call site expects.

**Not implemented, blocked on missing source:** SAFE MODE and the Sovereign Recovery Kernel (the
owner's inalienable "stop the system" rights) have zero code. The source document
(`Human_OS_Sovereign_Recovery_Layer_i_Rejestr_Scalenia_v0_2_1.docx`) is confirmed to exist but its
bytes are not yet available in this project — do not design or implement Recovery/SAFE MODE from
guesswork; wait for the source, per `docs/FOUNDER_REVIEW_2026-08-15.md` Q12.

### Module style split

Most of `hos_engine/` (`engine.py`, `models.py`, `policy.py`, `event_store.py`, `sqlite_store.py`,
`flow.py`, `state_machine.py`, `ids.py`, `validation.py`, `knowledge_graph.py`, `graph_store.py`,
and the newer **`hos_core.py`, `hub_entity_registry.py`, `authority.py`, `execution_loop.py`**) is
conventionally formatted (4-space indent, one statement per line). A distinct, separate group —
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
  Check these before making architectural changes, and add a new ADR for any decision of similar
  weight.
- `docs/FOUNDER_REVIEW_2026-08-15.md` is the live decision record for open questions raised by the
  `Human OS Reconstruction Audit` — check it before assuming a design question is still open. It
  now spans three rounds of corrections as the founder has supplied more original source files;
  read to the end, not just the initial Q1–Q13 answers.
- `docs/RELATION_VOCABULARY_CROSSWALK.md` — a provisional, explicitly incomplete mapping between
  the Hub's relation vocabulary (`hub_entity_registry.HubRelationType`, fully sourced) and a
  separate "Formal Entity & Relation Model" vocabulary known only secondhand (source DOCX bytes
  not yet available). Don't assume a 1:1 mapping between the two without checking this document.
- `docs/white_paper/` — the first White Paper content committed to this repo (2026-08-15): a 1:1
  transcription of two received PDFs covering Chapter III ("Technologia, która pamięta, komu ma
  służyć") — the main/overview text and Part C ("AI jako partner poznawczy"). Per
  `docs/FOUNDER_REVIEW_2026-08-15.md` Q3, the target is four parts (A–D); Parts A, B, D are not yet
  received — treat this directory as partial, not canon-complete, and check its `README.md` before
  assuming the chapter is whole.
- `docs/LAYER_6_EXPERIMENT_ENGINE_DIGEST.md` — a full structural digest (Polish, matching the
  source language) of Layer 6's source docx: metadata, all coded scales, the 15-object experiment
  ontology, all appendix field lists, the full 47-section table of contents, and every literal
  prohibition. Read this before extending `ADR-EXP-*` or building anything experiment-related —
  it's more complete than the ADRs alone.

## Licensing

Code is Apache-2.0 (`LICENSE`); documentation/specifications are CC BY 4.0 (`LICENSE-DOCS`). The
Human OS name/marks have no published trademark policy yet — this is explicitly unresolved, see
`LICENSE-DECISION.md`.

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
