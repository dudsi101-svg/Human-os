# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

Human OS is an experimental **constitutional protocol and reference engine** — not an operating
system in the traditional sense. It's a governance/ethics framework, implemented as a Python
library, whose stated goal is to increase human autonomy, creative agency, and meaningful
relations while *decreasing* dependence on the system itself over time ("Human OS does not decide
what a person's life should become. It helps the person remain the author of that life.").

Current release: **0.9.0 — "Protocol, Identity and Security"**, status **BETA**. Per README.md,
it explicitly lacks authentication, authorization, encryption at rest, independent security
review, and empirical calibration — **do not treat any part of this as production-hardened**,
especially the security modules (see Security section below).

The project layers are, in dependency order (no lower layer may silently redefine a
higher-layer principle — see `ECOSYSTEM.md`):

```
Constitution (constitution/) → HOSS/HOSP spec (spec/, protocol/) → Engine (hos_engine/) → SDK/Hub (sdk/, hub/) → Applications
```

- **Constitution** (`constitution/README.md`) — 10 base principles + 5 security-amendment
  principles (human primacy, revocable consent, inferences never masquerade as facts, no implied
  tool permission, data minimization, contestability, portability/exit, fail-closed security,
  etc.).
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
`.github/pull_request_template.md`, `.github/ISSUE_TEMPLATE/*.yml`) is written in **Polish**;
code, schemas, and ADRs are in English. Match the language of the doc you're editing.

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

**Known issue:** `pip install -e ".[dev]"` (both editable and non-editable `pip install .`)
currently fails on a clean environment with `error: Multiple top-level packages discovered in a
flat-layout` — `pyproject.toml` has no `[tool.setuptools.packages.find]`/`packages` config, so
setuptools can't disambiguate `hos_engine`, `hub`, `sdk`, `spec`, `schemas`, `protocol`,
`policies`, `security`, `bootstrap`, `constitution`, `data` as top-level directories. If a task
requires actually installing the package, either add explicit package discovery to
`pyproject.toml` (e.g. `packages = ["hos_engine"]` under `[tool.setuptools]`, since `hos_engine`
is the only real importable package) or install dependencies directly
(`pip install "jsonschema>=4.20,<5" "pytest>=8,<9" "ruff>=0.5,<1" "mypy>=1.10,<2"`) and run
`pytest`/`ruff`/`mypy` from the repo root without installing the project itself.

**Also note:** `ruff check .` and `mypy hos_engine` currently fail against the repository as-is
(hundreds of pre-existing ruff findings, dozens of pre-existing mypy findings) — `ruff` is pinned
only as `>=0.5,<1`, so a newly-installed ruff can enable stricter default rules than whatever
version was used historically. `pytest -q` (28 tests) passes cleanly. Don't assume `make verify`
starts from a clean baseline; when touching a file, check that your diff doesn't introduce *new*
lint/type errors rather than expecting the full-repo run to be green.

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

### ID and schema conventions

- All object IDs follow `HOS-<PREFIX>-######` (e.g. `HOS-HUM-000001`, `HOS-ACT-000002`), enforced
  by both `hos_engine/ids.py::IdGenerator` and `schemas/common.schema.json#/$defs/HOSId`
  (`^HOS-[A-Z]{2,8}-[0-9]{6,}$`).
- **Two ID-generation strategies coexist**: the counter-based `IdGenerator` (used by `engine.py`
  and older modules) and ad hoc `uuid.uuid4().hex[:12].upper()`-based generation used by newer
  modules (`agent_runtime.py`, `human_model.py`, `consent.py`, `security_identity.py`,
  `simulation.py`, `key_rotation.py`). Match whichever pattern the module you're editing already
  uses.
- `schemas/` holds 14 JSON Schema (Draft 2020-12) files. Every concrete entity schema (`action`,
  `human`, `intent`, `flow`, `knowledge`, `relation`, `system`) does
  `allOf: [{ $ref: entity.schema.json }, {...}]` against the shared base in
  `entity.schema.json`/`common.schema.json`. Validation against these schemas is done through
  `hos_engine/validation.py::SchemaRegistry` (`jsonschema.Draft202012Validator` +
  cross-schema `$ref` resolution).
- `schemas/common.schema.json`'s `Version` pattern is pinned to `^0\.2\.[0-9]+$`, which is stale
  relative to the actual project version (0.9.0) and component versions in `manifest.json` — be
  aware of this drift rather than "fixing" it silently in unrelated changes.
- `state_machine.py::ALLOWED_TRANSITIONS` governs the entity `status` field
  (`draft, active, paused, completed, archived, revoked`), matching `entity.schema.json`.

### Persistence

Two parallel persistence layers exist — pick based on what the module you're touching already
uses, don't mix:
- `event_store.py::EventStore` — simple JSONL append-only file (used by `engine.py` and the demo).
- `sqlite_store.py::SQLiteEventStore` — SQLite with a SHA-256 hash chain
  (`previous_hash`/`event_hash`, canonical JSON) and a `verify_chain()` integrity check.
- `graph_store.py::SQLiteGraphStore` — SQLite-backed knowledge graph storage.
- `replay.py::rebuild_entities` reconstructs entity state from the event log (distinct from
  `replay_guard.py`, see Security below — don't confuse the two "replay" modules).

### Security modules (`hos_engine/`)

`security_identity.py` (identity/key registry), `protocol_security.py` (`HMACSigner`,
`canonical_json`, `secure_envelope` — protocol tag `HOSP/0.2`), `replay_guard.py::ReplayGuard`
(nonce/expiry/message-id tracking, distinct from `replay.py`'s event-replay-for-state-rebuild),
`trust.py` (`TrustRegistry`/`TrustPolicy`/`TrustLevel`), `security_gateway.py::SecurityGateway`
(the check pipeline matching `protocol/security-profile.md`'s 10-step order: resolve identity →
verify active → validate key binding → verify signature → reject expired/replayed → trust policy
→ consent → capability checks → execute/deny → issue receipt), `key_rotation.py`.

`security/THREAT_MODEL.md` states explicitly that the current HMAC implementation is a **local
reference mechanism only** — production would need asymmetric signatures, protected key storage,
encrypted transport, trusted time, and rate limiting. Don't present it as production-grade in
docs or comments.

`sdk/python/human_os_sdk/` defines its own `ProtocolEnvelope` (protocol tag `HOSP/0.1`), which is
an older/different shape from `hos_engine.protocol_security.secure_envelope` (`HOSP/0.2`) — two
overlapping envelope representations exist; check which one a given call site expects.

### Module style split

Most of `hos_engine/` (`engine.py`, `models.py`, `policy.py`, `event_store.py`, `sqlite_store.py`,
`flow.py`, `state_machine.py`, `ids.py`, `validation.py`, `knowledge_graph.py`, `graph_store.py`)
is conventionally formatted (4-space indent, one statement per line). A distinct, later-added
group — `agent_runtime.py`, `human_model.py`, `consent.py`, `personalization.py`,
`security_identity.py`, `trust.py`, `security_gateway.py`, `key_rotation.py`, `simulation.py`,
`simulation_gate.py`, `protocol_security.py`, `replay_guard.py` — uses a dense, semicolon-joined,
single-line style (e.g. `class TrustLevel(str, Enum): UNTRUSTED = "UNTRUSTED"; ...`). This is a
consistent, intentional pattern in that group, not a formatting accident — match the style of
whichever file you're editing rather than reformatting it to match the other group.

`hos_engine/__init__.py` re-exports most submodules via `from .X import *`; none of those modules
define `__all__`, so new public names added to any of them become directly accessible as
`hos_engine.ClassName` and can collide across modules — check for name collisions when adding new
public classes/functions to these modules.

### Other components

- `hub/` is documentation-only (no code yet): describes a future Hub that routes HOSP messages,
  resolves identifiers, verifies consent, and issues receipts, without owning the human profile
  itself.
- `sdk/python/human_os_sdk/` directly imports from `hos_engine` — it is a thin convenience
  wrapper, not a decoupled client library.
- `docs/adr/` contains architecture decision records (ADR-0002 through ADR-0008), each in a short
  Decision / Constitutional rationale / Limitation format — check these before making
  architectural changes to understand prior rationale, and add a new ADR for any decision of
  similar weight.

## Contribution conventions

Per `CONTRIBUTING.md` and `.github/pull_request_template.md`, every material change is expected
to describe:
- which constitutional genes (`genome.registry.json`) it supports,
- which genes it places at risk, and the safeguards for that,
- limitations/uncertainty,
- impact on portability and exit (a user's ability to leave/export unaffected).

Constitution changes go through a separate governance process with a higher acceptance bar
(`GOVERNANCE.md`); security issues should be reported privately rather than as public issues
(`SECURITY.md`).
