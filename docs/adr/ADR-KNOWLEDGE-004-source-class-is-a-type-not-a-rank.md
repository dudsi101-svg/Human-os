# ADR-KNOWLEDGE-004: Source Classes Are Types Fit to a Question, Not One Best-to-Worst Ranking

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_3_Mapa_Wiedzy_i_Sygnatura_Informacji_v0_1.docx`, §6
("Taksonomia źródeł"). See `docs/FOUNDER_REVIEW_2026-08-15.md`, "Czwarta
tura" section, for provenance. Newly formulated — the source has no ADR
numbering of its own.

## Decision
Twelve source classes are defined (SCI, MEC, OBS, EXP, PRX, TRD, COM, N1,
SYM, HYP, REG, DOC — full definitions in `docs/LAYER_3_KNOWLEDGE_MAP_DIGEST.md`
§3.3). §6.1, verbatim: *"klasy nie tworzą jednej listy 'od najlepszej do
najgorszej' — problem pojawia się, gdy źródło odpowiada na pytanie, do
którego nie jest adekwatne."* — the classes do not form a single best-to-
worst list; the problem arises when a source answers a question it isn't
suited for, not from its class alone.

Every claim must be decomposed to a minimal atomic structure (§5.1, seven
fields: population/condition, intervention/factor, comparator, dose/form,
time horizon, outcome/metric, direction and magnitude with risk/
limitations) rather than left as a compound statement like "cold improves
health" or "meditation works" (§3.1's "Zakaz obiektów złożonych bez
rozbicia").

## Rationale
A fixed quality hierarchy of source types would systematically undervalue
appropriate-but-non-clinical evidence (e.g. `PRX` master-practitioner
knowledge for a procedural question no RCT has studied, or `N1` personal
evidence for a question only the individual user's own body can answer) —
this document instead makes fitness-for-question the organizing axis, with
the 0–5 signature scale (`ADR-KNOWLEDGE-001`) doing the actual strength
grading per-dimension, per-claim.

## Consequences
No code implements source-class typing, claim atomization, or this
fitness-for-question model today. When a real Knowledge Map / Layer 3
integration is built, source-class should be stored as a type tag on
`ProvenanceRecord` or its successor, not as an implicit ordinal ranking —
and claim ingestion should enforce the seven-field atomic structure rather
than accepting compound natural-language claims wholesale.
