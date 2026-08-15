# ADR-USERMODEL-002: No Epistemic Shortcuts From Behavior to Label, and a Working "Right to Be Forgotten in the Model"

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_4_Model_Uzytkownika_i_Cyfrowy_Profil_v0_1.docx`, §2
("Zakaz skrótu epistemicznego") and §5.2 ("Prawa użytkownika wobec
profilu"). See `docs/FOUNDER_REVIEW_2026-08-15.md`, "Czwarta tura" section,
for provenance. Newly formulated — the source has no ADR numbering of its
own.

## Decision
Verbatim (§2, the "Zakaz skrótu epistemicznego" box): *"System NIE MOŻE
zapisać interpretacji jako danych źródłowych. Przykład: »użytkownik jest
mało zdyscyplinowany« nie jest obserwacją. Obserwacją może być: »w 3 z 10
zaplanowanych dni wykonano zadanie«. Interpretacja wymaga osobnej hipotezy i
kontekstu."* — this is the Layer 4 instance of the same "no verdict
objects" pattern already documented for Layer 5 (`ADR-DECISION-002`) and
Layer 6 (`ADR-EXP-003`).

Eight named user rights over their own profile (§5.2): inspection,
correction (*"możliwość poprawienia faktu, zakwestionowania interpretacji i
dodania własnego komentarza"*), opt-out, export, **deletion** (profile and
copies removed after the required technical period, with an explicit list
of legal exceptions), **the right to be forgotten in the model**
(*"wyłączenie nieaktualnych cech i hipotez z przyszłych decyzji"*), silence,
and a minimal-profile right.

A rejected hypothesis retains only a technical trace — verbatim (§24,
"Prawo do sprzeciwu wobec modelu" box): *"System może zachować techniczny
ślad, że hipoteza została odrzucona, ale nie może po cichu nadal używać jej
do personalizacji, segmentacji ani treningu, jeśli użytkownik wycofał
zgodę."*

## Rationale
"Right to be forgotten in the model" is stronger than ordinary data
deletion: it requires that a withdrawn or contested inference stop
*influencing future decisions*, not merely that its record be marked
deleted. This closes a real gap that a naive soft-delete implementation
would miss — a system could technically honor a deletion request while an
already-derived feature or trained weight continues to reflect the deleted
data's influence.

## Consequences
`hos_engine.human_model.HumanRecord.contest()` implements a single
`CONTESTED` status, not the described distinction between "marked
contested" and "actively excluded from future personalization" — this is a
concrete, checkable gap. Any future implementation of a right-to-be-
forgotten guarantee must verify that contested/withdrawn data is excluded
from whatever derived-feature or recommendation pipeline consumes
`HumanRecord`, not just flagged in storage.
