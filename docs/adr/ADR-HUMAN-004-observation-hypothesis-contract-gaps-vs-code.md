# ADR-HUMAN-004: The Observation/Hypothesis Data Contract Is Richer Than the Current HumanRecord

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_2_Model_Czlowieka_v0_1.docx`, Appendix A ("Ontologia
skrócona") and §19 ("Pomiar, obserwacja i reprezentacja danych"). See
`docs/FOUNDER_REVIEW_2026-08-15.md`, "Czwarta tura" section, for provenance.
Newly formulated — the source has no ADR numbering of its own. This ADR
exists specifically to record a concrete, checkable gap the digest
identified between source and code.

## Decision
The source's minimal object tree (Appendix A) is:
```
PERSON
├── identity_and_roles
├── goals_values_meaning
├── domains[] (systems[], capacities[], resources[], constraints[], states_patterns[])
├── contexts[]
├── relationships[]
├── observations[]
├── hypotheses[]
├── trajectories[]
├── preferences_and_consent
└── model_versions[]
```
Minimum fields per object include: `Observation` (id, source, timestamp,
context, value, unit, quality, consent_scope), `Hypothesis` (statement,
evidence_refs, alternatives, confidence, scope, created_at, reviewed_at),
`Goal` (owner, domain, motive, metric, horizon, priority, tradeoffs,
status), and a **discrete, five-level, worded confidence scale** (§20.1:
"brak podstaw" / "możliwość" / "robocza hipoteza" / "wzorzec wspierany" /
"silnie wspierany") — not a continuous number.

Every data record requires mandatory metadata (§19.2): source and data
owner; time and timezone; context and active interventions; unit and scale;
quality, completeness, and possible error; status (raw/processed/inferred);
purpose of use and consent scope; retention period and deletability. Data
and inference must be kept strictly separate (§19.3's worked example: the
data is "slept 5h40m for four days, energy 3/10"; the inference is "sleep
deficit likely limits energy"; the recommendation is "test increasing
sleep" — each stored as its own layer).

## Rationale
This is the concrete field-level form of `ADR-DECISION-002`'s "no verdict
objects" rule and `ADR-HUMAN-001`'s ontology — recording exactly which
fields the source requires makes the gap against current code checkable
rather than abstract.

## Consequences
`hos_engine.human_model.HumanRecord`'s actual fields (`record_id,
subject_id, domain, key, value, evidence_type, confidence, source_id,
created_at, status, supersedes, sensitive, tags`) lack the source's
`source` (as distinct from `source_id`), `context`, `quality`, `unit`, and
`consent_scope` fields per-record. *(Update 2026-08-15, Phase 3: `context`,
`unit`, `quality`, and `consent_scope` added as optional fields on
`HumanRecord` and `HumanModel.add()`; the discrete-vs-continuous confidence
mapping and richer hypothesis statuses below remain open.)* The source's discrete five-level worded
confidence scale has no defined mapping to the code's continuous
`confidence: float` in [0,1] — neither this document nor `human_model.py`
defines that mapping. `RecordStatus` (ACTIVE/CONTESTED/SUPERSEDED/DELETED)
is coarser than the source's suggested hypothesis-status granularity
(active/rejected/supported/expired, per Appendix C). These are documented
gaps for a future alignment pass, not resolved by this ADR — do not assume
`HumanRecord` already satisfies this contract.
