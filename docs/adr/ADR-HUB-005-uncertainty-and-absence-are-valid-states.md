# ADR-HUB-005: Uncertainty, Conflict, and Absence Are Valid States of the System

## Status
Accepted direction — not yet fully implemented. Imported 2026-08-15 per
founder review Q11. Source: *HOS Hub Model — Entity-First v0.1*, §3.3, §6.3,
§7.1, §7.3.

## Decision
An Entity may be complete, partial, contradictory, suspect, withdrawn, or
archived. The Hub does not resolve uncertainty by guessing. It records
absence, conflict, and the need for escalation.

The Hub does not automatically merge Entities of high significance. It forms
a hypothesis of correspondence, evaluates the evidence, and requires
confirmation when an erroneous merge could affect health, finances, identity,
rights, or the history of a decision.

Operational contracts: **Register Entity** — input is an Entity candidate,
type, source, and scope of consent; output is an ID, or an indication of a
possible duplicate; fail-safe behavior is to pause and request resolution.
**Resolve Entity** — input is a name, context, and intent; output is a
single Entity, a list of candidates, or explicit non-resolvability. The Hub
must not hide ambiguity.

## Rationale
The system deliberately trades automation speed for safety — high-stakes
merges and ambiguous resolutions require human confirmation rather than
being resolved silently.

## Consequences
`hos_engine.hub_entity_registry.EntityRegistry` implements
`flag_possible_duplicate()` and a manual `merge()` operation (the retired
entity becomes `SUPERSEDED`, never silently deleted). It does not yet
implement risk-weighted confirmation requirements (health/finance/identity)
or the `Resolve Entity` contract's candidate-list / non-resolvability output.
