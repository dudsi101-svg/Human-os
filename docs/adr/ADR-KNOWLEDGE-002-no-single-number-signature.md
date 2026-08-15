# ADR-KNOWLEDGE-002: A Knowledge Signature Is a Vector, Never Collapsed to One Number

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_3_Mapa_Wiedzy_i_Sygnatura_Informacji_v0_1.docx`, §7.2
("Zakaz jednego wyniku bez wektora"). See `docs/FOUNDER_REVIEW_2026-08-15.md`,
"Czwarta tura" section, for provenance. Newly formulated — the source has no
ADR numbering of its own.

## Decision
Verbatim: *"System może tworzyć uproszczony status dla interfejsu, ale pełna
sygnatura pozostaje wektorem. […] Suma punktów nie może ukryć słabego
wymiaru krytycznego."* — the system may present a simplified status in the
UI, but the full signature must remain a vector internally; a summed score
must never hide a critically weak dimension.

## Rationale
This is the epistemic-layer instance of the same anti-flattening principle
already established for Layer 5's decision profile (§18.2's "Zakaz fałszywej
precyzji") and Layer 6's measurement objects (`ADR-EXP-003`'s ban on hidden
merging). A single confidence number is exactly the failure mode a
knowledge system is most tempted to produce for UI simplicity — this rule
draws the line at *internal representation*, not display: simplification at
the interface is fine, information loss in storage is not.

## Consequences
This directly conflicts, in spirit, with the current implementation:
`hos_engine.knowledge_graph.ProvenanceRecord` has a single scalar
`confidence: float` field, not an 11-dimension vector. The digest flags this
as an observation, not a resolved conflict — `ProvenanceRecord` may be an
intentionally narrower primitive than the full "Sygnatura wiedzy," but this
should be confirmed against original design intent before assuming
compatibility, not assumed. Any future work that makes `knowledge_graph.py`
compliant with this ADR must add vector-shaped signature storage rather than
extending the single `confidence` scalar.
