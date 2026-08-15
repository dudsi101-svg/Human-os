# Relation Vocabulary Crosswalk — v0.1

Status: **Draft, provisional**. Created 2026-08-15 during the source-integrity
correction pass following the founder's `CLAUDE_COPY_PASTE_CONTINUATION_DIRECTIVE_2026-08-15`.

## Provenance caveat — read before using this document

This crosswalk relates two vocabularies that are **not equally available** as
source material:

- **HUB_ENTITY_FIRST_RELATION_VOCAB_v0.1** — the 17 Polish-language relation
  verbs from `HOS Hub Model — Entity-First v0.1`, §4. This document was fully
  read; the vocabulary below is complete and confirmed.
- **FORMAL_ENTITY_RELATION_VOCAB_v0.1** — the English-language relation verbs
  attributed to `Human_OS_Formal_Entity_Relation_Model_v0_1.docx`. **This
  repository does not have that document's bytes** — it is a *confirmed File
  Library original whose raw bytes were not exported* (see
  `docs/FOUNDER_REVIEW_2026-08-15.md`, Q12 correction). Everything known about
  this vocabulary comes secondhand, from a list embedded in the founder's
  continuation directive: `IS_A, PART_OF, CONTAINS, OWNS, CONTROLS,
  RESPONSIBLE_FOR, ASSIGNED_TO, DEPENDS_ON, REQUIRES, BLOCKS, ENABLES,
  CONTRIBUTES_TO, DERIVED_FROM, REPRESENTS, REFERENCES, and additional
  relation semantics` (the directive's own wording signals this list is
  itself incomplete).

**Every classification below is therefore provisional** and should be
re-verified once `Human_OS_Formal_Entity_Relation_Model_v0_1.docx` is
actually uploaded and read in full. Do not treat this table as settled.

## Classification key

- **exact alias** — same relation, different language/spelling
- **semantic subset** — the Hub verb is narrower than its formal counterpart
- **semantic superset** — the Hub verb is broader than its formal counterpart
- **domain-specific** — a relation with no formal-model counterpart because it belongs to a domain (epistemic, temporal) the formal list doesn't cover
- **conflict** — plausible mappings to more than one formal verb, ambiguous without more context
- **no equivalent** — nothing in the (incomplete) formal list corresponds

## Crosswalk

| Hub verb (`HubRelationType`) | Meaning | Formal-model candidate | Classification | Note |
|---|---|---|---|---|
| `jest_typem` | is-a-type-of | `IS_A` | exact alias | |
| `należy_do` | belongs-to | `PART_OF` or `OWNS` | **conflict** | "Belongs to" covers both part-whole and ownership in Polish usage; the formal model splits these. Needs disambiguation before any migration. |
| `dotyczy` | concerns | `REFERENCES` | semantic superset | Hub's "concerns" is a loose topical association, broader than a formal reference/citation link. |
| `powstał_z` | originated-from | `DERIVED_FROM` | exact alias | |
| `reprezentuje` | represents | `REPRESENTS` | exact alias | |
| `wspiera` | supports | `CONTRIBUTES_TO` | semantic subset | Plausibly near-exact, but not confirmed without the source document. |
| `przeczy` | contradicts | — | domain-specific | Epistemic/knowledge-graph relation (contradicting claims, per Layer 3); no counterpart in the disclosed formal list. |
| `zależy_od` | depends-on | `DEPENDS_ON` | exact alias | |
| `powoduje` | causes | — | domain-specific | Causal relation; `ENABLES` is "makes possible," not strict causation -- not the same claim. |
| `poprzedza` | precedes | — | domain-specific | Temporal/sequence relation; no counterpart in the disclosed formal list. |
| `aktualizuje` | updates | — | no equivalent | Possibly related to a `VERSION` entity in the formal model, but no relation verb was disclosed for it. |
| `zastępuje` | replaces | — | no equivalent | Semantically close to `hos_engine.hub_entity_registry`'s own `HubEntityStatus.SUPERSEDED` / `MergeRecord`, but no formal `REPLACES` verb was disclosed. |
| `mierzy` | measures | — | domain-specific | A `METRIC` entity type is named in the formal entity list, but no `MEASURES` relation verb was disclosed. |
| `realizuje` | fulfills / realizes | `ENABLES` or `CONTRIBUTES_TO` | **conflict** | Ambiguous between "makes possible" and "contributes to" without the source document. |
| `został_zatwierdzony_przez` | was-approved-by | — | no equivalent | Governance/approval relation; `ASSIGNED_TO` is task assignment, not approval -- not the same claim. |
| `jest_przechowywany_w` | is-stored-in | `CONTAINS` (inverse) | semantic subset | Hub's verb is the inverse direction of a formal `CONTAINS` edge. |
| `jest_widokiem` | is-a-view-of | `REPRESENTS` | semantic subset | A "view" is a specific kind of representation, not identical to `REPRESENTS` in general. |

## What this crosswalk does NOT do

It does not choose a winning vocabulary. Per founder review Q8, both the
general graph-edge relation model and the interpersonal-relationship model
(`schemas/relation.schema.json`) are kept under different names — this
crosswalk adds a *third* consideration (Hub vs. Formal) to the same
"don't silently merge" principle. `hos_engine.hub_entity_registry.HubRelationType`
continues to implement HUB_ENTITY_FIRST_RELATION_VOCAB_v0.1 unchanged; no
code migration to the formal vocabulary has been made.

## Next step

Upload `Human_OS_Formal_Entity_Relation_Model_v0_1.docx` (confirmed to exist,
bytes not yet available) so this crosswalk can be completed against the full
source rather than a secondhand list, and the four `no equivalent` /
`conflict` rows above can be resolved with evidence instead of left open.
