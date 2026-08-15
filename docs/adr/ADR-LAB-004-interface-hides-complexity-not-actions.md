# ADR-LAB-004: The Lab Interface May Hide Technical Complexity but Never System Actions

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 per founder-provided
source `Human_OS_Lab_Specyfikacja_i_Interface_v0_1.docx`. See
`docs/FOUNDER_REVIEW_2026-08-15.md` for provenance.

## Decision
The Lab Console interface is allowed to hide technical complexity from the
tester (source ADR-LAB-004: "Interfejs ukrywa złożoność techniczną, ale nie
ukrywa działań systemu") but must never hide what the system actually did.
Every step, source, uncertainty, and decision point must remain visible
(source §3, step 4: "Obserwuj kolejne kroki, źródła, niepewność i punkty
decyzyjne").

## Rationale
This is the Lab-specific instance of a constitutional rule that already
governs the whole project: the Constitution (`constitution/README.md`, Ch.4)
bans dark patterns and requires that inferences never masquerade as facts.
Simplifying an interface for usability is legitimate; simplifying it in a way
that conceals automation, data use, or risk is not — the same line already
drawn for the Proof Kernel's `limitations` field and the Proof Kernel Console
(`app/`)'s raw-JSON toggle.

## Consequences
Any future Lab Console implementation should follow the existing
`app/server.py` Proof Kernel Console precedent of always offering a way to
see the underlying decision/evidence, not just a friendly summary.
