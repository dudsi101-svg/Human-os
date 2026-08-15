# ADR-LAB-006: The Local Lab Prototype Is a UX Stage, Not a Backend

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 per founder-provided
source `Human_OS_Lab_Specyfikacja_i_Interface_v0_1.docx`. See
`docs/FOUNDER_REVIEW_2026-08-15.md` for provenance.

## Decision
The v0.1 Human OS Lab Console prototype (described in source §10, "Status
prototypu v0.1") is a clickable, local, responsive web app with demo data
held only in browser `localStorage` — no server, no authentication, no real
agent orchestration. Source, verbatim: "Prototyp jest demonstracją UX i
modelu operacyjnego; nie zawiera jeszcze backendu, uwierzytelniania ani
prawdziwej orkiestracji agentów." A real backend is explicitly deferred until
the Entity/Relation/Event schemas stabilize (source ADR-LAB-006 itself:
"Prototyp lokalny jest etapem UX; backend zostanie dołączony po stabilizacji
schematów Entity/Relation/Event").

## Rationale
This sequencing matches the project's own accepted build order elsewhere:
ADR-IMPL-001 ("Najpierw stabilizujemy schemat bytów i zdarzeń, potem agentów,
dopiero później interfejsy") and the founder's Q5/Q6 decision that schema
work precedes UI work. The Lab prototype is explicitly UX-first by design,
not a violation of that order — its own document defers backend work until
schemas are ready, consistent with the rest of the project.

## Consequences
No claim should be made in project documentation that a working Lab backend
exists. The prototype (if/when its files are made available) is a design
artifact, not a functioning `hos_engine` component — nothing in this
repository currently implements it, and this repository's own
Entity/Relation/Event schemas (`hos_engine.hub_entity_registry`,
`schemas/event.schema.json`) are themselves still an MVP subset per
ADR-HUB-006, so the stated precondition for a Lab backend is not yet met.
