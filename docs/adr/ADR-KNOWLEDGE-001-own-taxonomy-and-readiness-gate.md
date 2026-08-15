# ADR-KNOWLEDGE-001: The Knowledge Map Defines Its Own Signature, Readiness, and Source-Class Taxonomies

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_3_Mapa_Wiedzy_i_Sygnatura_Informacji_v0_1.docx`
("Warstwa 3", version "0.1 - model bazowy", dated 2026-07-20, status
"Projekt do iteracji, audytu i zatwierdzenia"). See
`docs/FOUNDER_REVIEW_2026-08-15.md`, "Czwarta tura" section, for provenance,
and `docs/LAYER_3_KNOWLEDGE_MAP_DIGEST.md` for the full digest. The source
has no ADR numbering of its own — this ADR is newly formulated.

**Naming note:** this is a *fourth* independent coded-scale taxonomy across
the layers digested so far (Constitution's R0–R4; Layer 6's XP/SE/EC/BL/MQ/
PF/DQ/CA/PE; Layer 5's DI/IQ/AR/RV/RC/G/R-level). None of Layer 3's letters
overlap in meaning with any of the others.

## Decision
Layer 3 (the Knowledge Map & Information Signature) defines:
- A **0–5 descriptive signature scale** (0 = no data, 5 = very strong,
  multiply-confirmed) applied across 11 signature dimensions (Pochodzenie,
  Jakość metod, Bezpośredniość, Spójność, Niezależność, Skala i precyzja,
  Transparentność, Aktualność, Zakres zastosowania, Niepewność, Ryzyko
  błędu).
- A **decision-readiness scale E0–E5** (E0 recognition-only through E5
  safety-requirement) — the closest equivalent to a "risk gate" for whether
  a knowledge object may be used in a recommendation at all.
- A **review-level scale K1–K4** (informational through high-risk),
  determining what reviewer composition a knowledge object needs before
  publication.
- A **12-code source-class taxonomy**: SCI (human research), MEC
  (mechanism/preclinical), OBS (observational), EXP (expert knowledge), PRX
  (master-practitioner knowledge), TRD (tradition), COM (community-
  structured data), N1 (personal N-of-1 evidence), SYM (symbolic/
  interpretive systems), HYP (theoretical hypothesis), REG (regulatory
  data), DOC (technical documentation) — explicitly *not* a single
  best-to-worst ranking (§6.1, "Zakaz spłaszczania źródeł" — a source class
  fails only when used to answer a question it isn't suited for).

No knowledge object may be used in a recommendation unless the system can
answer its own "test nadrzędny" (§0.5, verbatim): *"'co dokładnie jest
twierdzone?', 'skąd to pochodzi?', 'dla kogo i kiedy ma zastosowanie?', 'jak
bardzo jesteśmy tego pewni?' oraz 'co może pójść źle?'"* — the same
structural gate pattern as Layer 5 (`ADR-DECISION-001`) and Layer 6
(`ADR-EXP-001`), applied here to knowledge readiness instead of decision
publication or experiment launch.

## Rationale
Document motto (verbatim): *"Human OS nie przechowuje jednej wersji prawdy.
Przechowuje twierdzenia, ich pochodzenie, kontekst, poziom pewności i
historię zmian."* Treating source class as a *type* rather than a *rank*
is the epistemic equivalent of Layer 5's "hard gate before ranking"
principle — a source cannot be excluded from consideration just for being
low on a single quality axis if it's the right type of evidence for the
question being asked.

## Consequences
No `hos_engine` module implements any of these four taxonomies.
`hos_engine.knowledge_graph.py` exists but its node/edge types are untyped
strings, not the closed 13-type/9-relation catalog this document specifies
(see `ADR-KNOWLEDGE-003`). Note also a discrepancy the digest flags but does
not resolve: `constitution/README.md` Ch.5 describes a "knowledge signature"
of a minimum 7 fields, while this document's §7 defines 11 dimensions (and
its own §29.3 acceptance criterion cites yet another 7-item subset that
doesn't exactly match either list) — this is a concrete, checkable item for
founder resolution, not something this ADR resolves by picking one.

**Resolved 2026-08-15** (founder decision, `docs/FOUNDER_REVIEW_2026-08-15.md`,
"Piąta tura"): both versions stand, in different roles. The Constitution's 7
fields are the hard, everywhere-mandatory floor; this document's 11
dimensions are the full, recommended form used wherever practical. Neither
is "wrong" and neither is dropped — `constitution/README.md` Ch.5 has been
updated to state this explicitly. §29.3's own third, non-matching 7-item
subset remains an internal editorial inconsistency in the source document,
not addressed by this resolution.
