# ADR-ARCH-003: Applications Never Own Executive Constitutional Logic — the App↔Core Contract

## Status
Accepted direction (founder-approved execution of the 2026-08-17 full audit,
P1 item 5/6: "App ↔ Core Contract; UI przestaje implementować własne G0–G8").
Contract text: `docs/APP_CORE_CONTRACT.md` (v0.1, PROPOSED).

## Context
The user app (`apps/user-demo`, UX-ONLY prototype per DD-005) locally
re-implements rules the engine now truly owns: decision gates, self-model
epistemics, N-of-1 lifecycle, emergency modes, consents. The audit names
the risk: a "Human OS A" (Python Core) and "Human OS B" (JavaScript app)
drifting until one allows what the other blocks. The Constitution's
authority must have exactly one executable seat.

## Decision
1. The boundary is `UI → Request → Core → Decision/Policy → Receipt → UI`.
   Applications collect intent, display options/explanations, ask for
   consent, render state, and store receipts. Core interprets policy,
   decides (including refusing), runs workflows, records events, and
   controls provenance.
2. The prototype's local rules are a **mock of Core behavior**, never a
   second source of truth. Every app-side rule must map to a Core
   counterpart (or an explicit gap entry) in the contract's divergence
   table.
3. **No new app-only rules:** a feature needing a new gate/policy lands in
   `hos_engine` (or as a DD entry) first, UI second.
4. Request/Receipt shapes are transport-independent (in-process now, HTTP
   at the store/backend stage per DD-013) and defined in the contract doc.

## Consequences
- `docs/APP_CORE_CONTRACT.md` carries the normative field tables and the
  divergence table (N-of-1, G0–G8, self-model, emergency modes, consents,
  audit) with a closure plan; wiring the app's N-of-1 to
  `experiment_engine.py` is the audit's P1 item 6 and follows this ADR.
- The single-file app refactor waits until this boundary exists (audit
  §10: refactoring first would modularize the wrong boundary).
- The consent-vocabulary mismatch (app C0–C6 vs engine consent ids) needs
  its own deferred decision before unification.
