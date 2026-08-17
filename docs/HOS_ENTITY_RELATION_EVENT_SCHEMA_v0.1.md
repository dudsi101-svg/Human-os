# HOS Entity, Relation & Event Schema v0.1

## Status

Draft v0.1, first version. This is the artifact `ADR-IMPL-001` names as
"the next mandatory artifact" — the schema-level document that Stage 1 of
its eight-stage build sequence calls for, which every later stage depends
on. It was not written before `hos_core.py` and `hub_entity_registry.py`
landed; `ADR-IMPL-001`'s own Consequences section already flags this
inversion ("the code should be treated as provisional until it exists").
**This document exists to close that gap — it consolidates decisions
already made across ADRs and schema files into one place; it does not make
new design decisions.** Where the underlying sources disagree or are
incomplete, that is stated explicitly rather than resolved here.

Scope, per `ADR-IMPL-001`: "słownik typów bytów, relacji i zdarzeń; reguły
dopuszczalności; identyfikatory; statusy; poziomy poufności; przykłady
JSON; zasady walidacji; procedury migracji; kontrakty błędu oraz minimalne
API."

## 1. Identifiers

Three ID patterns coexist in this project — this document does not merge
them, only names them so a future reader recognizes each on sight:

| Pattern | Example | Used by |
|---|---|---|
| Counter-based | `HOS-HUM-000001` | `hos_engine.ids.IdGenerator`, `engine.py` and older modules |
| UUID-based | `HOS-CTX-a1b2c3d4e5f6` | `uuid.uuid4().hex[:12].upper()`, most modules added since `agent_runtime.py` (see `CLAUDE.md` for the full list) |
| Change-log ID | `HOS-CHG-2026-0721-001` | Sovereign Recovery's own merge register (`ADR-RECOVERY-004`), not used anywhere else yet |

All three match `schemas/common.schema.json#/$defs/HOSId`'s pattern
(`^HOS-[A-Z]{2,8}-[0-9]{6,}$`) **except** the UUID-based pattern, whose hex
segment does not satisfy `[0-9]{6,}` as a pure numeric run — this is a
pre-existing, undocumented-until-now mismatch between the schema regex and
actual runtime IDs; flagged here, not fixed, since fixing it means picking
one pattern as canonical (a real design decision, not a documentation
task).

**Resolved 2026-08-17 (DD-010, founder option a):** the canonical pattern
is now `^HOS-[A-Z]{2,8}-[0-9A-F]{6,}$` — extended to cover the uppercase
hex segment the engine actually generates. No existing ID becomes
invalid (digit-only IDs are a subset). Note the change-log format
(`HOS-CHG-2026-0721-001`) still does not match either pattern generation —
it exists only in ADR-RECOVERY-004's text and no code emits it; if it is
ever implemented, its dashes need their own decision.

## 2. Entity types

### 2.1 Base entity types (`schemas/entity.schema.json`)

The original ten: `human`, `relation`, `flow`, `intent`, `action`,
`project`, `knowledge`, `community`, `system`, `event`. Every concrete
schema does `allOf: [{ $ref: entity.schema.json }, {...}]` against this
base plus `common.schema.json`.

### 2.2 Hub MVP entity types (`hub_entity_registry.HubEntityType`)

Six types, explicitly marked `MVP_IMPLEMENTED_SUBSET` in code: `PERSON`,
`GOAL`, `KNOWLEDGE_CLAIM`, `DECISION`, `EXPERIMENT`, `RESOURCE`. This is
**not** the base ten above and **not** the Formal Entity & Relation Model's
larger set below — a third, partially-overlapping vocabulary.

### 2.3 Formal Entity & Relation Model's type set (known only secondhand)

Per `hub_entity_registry.py`'s own docstring, the Formal Entity & Relation
Model (source bytes not yet available — see Founder Review Q12) describes a
much broader set: `IDENTITY, PROFILE, PROJECT, OUTCOME, TASK, WORKFLOW,
ASSET, LOCATION, DOCUMENT, KNOWLEDGE_ITEM, SOURCE, RISK, METRIC, EVENT,
POLICY, PERMISSION_GRANT, CONSENT, RELATION, REPRESENTATION, VERSION,
AGENT, AUTOMATION, INTERACTION, COMMITMENT, CAPABILITY`, and more. **Do not
map Hub's six types onto this list by convenience** (e.g. `PERSON` →
`IDENTITY`) — that mapping needs its own source-grounded analysis once the
actual document is available, per the existing code comment.

### 2.4 Knowledge Map node types (Layer 3, `ADR-KNOWLEDGE-003`)

A closed catalog of 13: claim, source, intervention, protocol, outcome,
mechanism, risk, contraindication, population, metric, domain, user/cohort,
version/editorial-decision. `hos_engine.knowledge_graph.GraphNode.node_type`
is currently an unconstrained `str` — this catalog is not enforced in code.

### 2.5 Domain-layer object ontologies are not part of this dictionary

Layers 2, 4, 5, and 6 each define their own rich object ontologies (Layer
2's `Observation`/`Hypothesis`/`Pattern`/etc., Layer 4's 24-object
ontology, Layer 5's 13 decision objects, Layer 6's 15 experiment objects —
see their respective digests in `docs/`). These are **domain-specific
record shapes**, not entries in the core Entity type dictionary — they
would, if implemented, most naturally live as `knowledge`/`intent`/`action`
entities carrying domain-specific payloads, or as their own schema
extensions. This document does not decide that mapping; it only notes that
these ontologies are a distinct concern from entity *typing*.

## 3. Relation types

### 3.1 Hub relation vocabulary (`hub_entity_registry.HubRelationType`)

17 verbs from the Hub Entity-First spec §4 (e.g. `JEST_TYPEM`,
`NALEZY_DO`, `REALIZUJE`) — the `HUB_ENTITY_FIRST_RELATION_VOCAB_v0.1`.

### 3.2 Formal relation vocabulary (known only secondhand)

Different English verb names (`IS_A`, `PART_OF`, `CONTAINS`, `OWNS`,
`CONTROLS`, `DEPENDS_ON`, ...) with richer first-class metadata
(directionality, status, provenance, `created_by`, validity, constraints,
`schema_version`). See `docs/RELATION_VOCABULARY_CROSSWALK.md` for the
provisional, explicitly incomplete mapping between the two — do not assume
1:1 correspondence beyond what that document states.

### 3.3 Knowledge Map relations (Layer 3, `ADR-KNOWLEDGE-003`)

9 named edges: `POPIERA`, `OSŁABIA`, `PRZECZY`, `WARUNKUJE`, `WYJAŚNIA`,
`RYZYKUJE`, `WCHODZI_W_INTERAKCJE`, `JEST_WERSJA`, `WYNIKA_Z`. Not enforced
in `knowledge_graph.py` today (`GraphEdge.relation_type` is `str`).

### 3.4 Interpersonal relation model (`schemas/relation.schema.json`)

A pre-existing, deliberately separate model (`trust`/`reciprocity`/
`boundaries` fields) for relations *between people* — kept apart from
`RelationRegistry`'s graph-edge relations per founder review Q8. Not part
of this dictionary's node-graph vocabulary.

## 4. Event types

### 4.1 Canonical domain events (`event.types.json`, mirrored in `schemas/event.schema.json`)

15 types: `ENTITY_CREATED`, `ENTITY_UPDATED`, `ENTITY_ARCHIVED`,
`CONSENT_GRANTED`, `CONSENT_REVOKED`, `INTENT_DECLARED`, `ACTION_PROPOSED`,
`ACTION_APPROVED`, `ACTION_BLOCKED`, `ACTION_EXECUTED`, `FLOW_RECORDED`,
`STATE_OBSERVED`, `PROOF_COMPLETED`, `LIMITATION_DISCLOSED`,
`VERSION_RELEASED`. These are what `EventStore`/`SQLiteEventStore` persist
via `engine.py`'s `_emit`.

### 4.2 Execution-lifecycle events (`hos_core.EventEngine`)

A separate, in-memory-only log per `ExecutionContract` — not the same
vocabulary or the same durability guarantee as 4.1 (see `CLAUDE.md`'s
Persistence section for the boundary). Not enumerated as a closed type set
in code today.

### 4.3 Proposed recovery events (`ADR-RECOVERY-004`, not yet implemented)

Sovereign Recovery's source calls for `recovery_*` events to be added to
the Entity/Event schemas, alongside a `FROZEN` status — resolved by founder
decision (`ADR-RECOVERY-006`) to reuse the existing `SUSPENDED` status
rather than add `FROZEN`; the `recovery_*` event types themselves are not
yet named or added to `event.types.json`.

## 5. Status / lifecycle vocabularies

Three are deliberately kept separate, per existing project convention —
this document does not unify them:

| Vocabulary | Values | Owner |
|---|---|---|
| `entity.schema.json` status | `draft, active, paused, completed, archived, revoked` | `state_machine.ALLOWED_TRANSITIONS` |
| `HubEntityStatus` | `PROPOSED, ACTIVE, SUSPENDED, SUPERSEDED, ARCHIVED` | `hub_entity_registry.py` |
| `RecordStatus` | `ACTIVE, CONTESTED, SUPERSEDED, DELETED` | `human_model.py` |

Per `ADR-RECOVERY-006`, Recovery's "Freeze Entity / Scope" contract reuses
`HubEntityStatus.SUSPENDED` — no fourth vocabulary is introduced for it.

## 6. Confidentiality / risk / quality scales

Five independent, non-overlapping coded taxonomies now exist across the
digested layers (full detail in each layer's ADR series and digest — this
table is a pointer, not a redefinition):

| Scale | Owner | Measures |
|---|---|---|
| R0–R4 | Constitution Ch.6 | Intervention risk |
| XP0–XP8, SE0–SE4, EC/BL/MQ/PF/DQ/CA/PE | Layer 6 (`ADR-EXP-001`) | Experiment process class and quality/safety |
| DI/IQ/AR/RV/RC/G, R-NISKIE..R-KRYTYCZNE | Layer 5 (`ADR-DECISION-001`) | Decision intent, readiness, reversibility, risk |
| Signature 0–5, E0–E5, K1–K4, SCI/MEC/.../DOC | Layer 3 (`ADR-KNOWLEDGE-001`) | Knowledge signature strength and source class |
| R0–R8, H0–H5, P0–P5, C0–C5, D0–D4 | Layer 4 (`ADR-USERMODEL-001`) | User-model architecture row, hypothesis/evidence strength, consent, sensitivity |

No entry in this table should be assumed equivalent to any other, even
where letters coincide (e.g. none of the four non-Constitution "R" scales
are the Constitution's R0–R4). `hos_engine` implements none of these scales
in code today.

## 7. JSON examples

Concrete examples already exist and are not duplicated here: `examples/
action.approved.example.json`, `examples/action.blocked.example.json`
(consumed by `run_demo.py` and the Proof Kernel Console). No JSON examples
exist yet for Hub entities, knowledge-graph nodes/edges, or any of the
domain-layer object ontologies (§2.5) — this is an open item for whoever
first implements one of them.

## 8. Validation rules

`hos_engine.validation.SchemaRegistry` (`jsonschema.Draft202012Validator` +
cross-schema `$ref` resolution) validates against the 14 files in
`schemas/`. It has no awareness of `hub_entity_registry`'s Python-level
enums (§2.2, §3.1) or any of the layer-specific ontologies (§2.5) — those
are validated only by their dataclass/Enum type constraints in Python, not
by JSON Schema, since none of them have `.schema.json` counterparts yet.

## 9. Migration procedures

`hos_engine.replay.rebuild_entities` reconstructs entity state from the
`EventStore`/`SQLiteEventStore` log — this is the only migration mechanism
that exists today, and it operates on §4.1's event vocabulary only. No
migration procedure exists for Hub entities/relations (`EntityRegistry`/
`RelationRegistry` are in-memory only, per `CLAUDE.md`) or for any
domain-layer ontology.

## 10. Error contracts

A single pattern recurs across every digested layer's own "Kontrakt błędu"
section (Layer 3 §27.1, Layer 5 §41.1, Layer 6 §38.1, all quoted in their
respective digests): **a module facing missing data, a conflict, low
confidence, or a disallowed state must return that state explicitly — never
silently substitute a default or force a confident-looking answer.** This
project's closest existing code expression of the same idea is
`ExecutionLoop`'s `IntentOutcome.REFUSED_*` family and the Proof Kernel's
`Decision` enum: refusal/uncertainty is a first-class return value, never
an exception swallowed into a fallback. Any future schema-level error
contract should follow this same shape rather than inventing a new one.

## 11. Minimal API surface (as it exists today)

Not a proposal — an inventory of what already exists, so a future
implementer knows what's available versus what to build:

| Operation | Module |
|---|---|
| `register`, `get`, `transition`, `flag_possible_duplicate`, `merge`, `by_type` | `hub_entity_registry.EntityRegistry` |
| `link`, `get`, `outgoing`, `incoming`, `orphans` | `hub_entity_registry.RelationRegistry` |
| `append` (JSONL) | `event_store.EventStore` |
| `append` (hash-chained), `verify_chain` | `sqlite_store.SQLiteEventStore` |
| `open`, `transition`, `get`, `log` | `hos_core.EventEngine` |
| `snapshot`, `latest`, `history` | `hos_core.ContextManager` |
| `evaluate_action` | `engine.HumanOSEngine` (drives the Proof Kernel) |
| `execute` | `execution_loop.ExecutionLoop` (the full gated pipeline) |

## What this document is not

Not a `.schema.json` file itself — `schemas/` remains the machine-validated
source for the base ten entity types. Not a decision to reconcile any of
the parallel vocabularies in §2–§6 — every "not yet reconciled" note above
is deliberate and should stay that way until the founder or a dedicated ADR
resolves it. Not an implementation plan — see the audit's Faza 2/3
recommendations (`docs/FOUNDER_REVIEW_2026-08-15.md`) for what to build
next.
