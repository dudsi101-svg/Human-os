# Human OS

Human OS is an open constitutional protocol and reference engine intended to
increase human autonomy, creative agency, responsibility, meaningful relations
and generative flows of value.

> Human OS does not decide what a person's life should become.
> It helps the person remain the author of that life.

## Current release

**Human OS Engine 0.10.0-alpha.1 — Execution Foundation and Sovereign Recovery**

Status: **ALPHA — reference implementation**

Version and maturity are separate dimensions (founder decision,
2026-08-17): growing the engine justifies a new minor version, but it
does not imply production readiness, and release numbering is
independent of the roadmap's 0.9 → 1.0 axis. See `CHANGELOG.md` for the
full delta since 0.9.0.

The engine is a reference implementation of the Human OS protocol and
constitution. Individual components carry their own maturity statuses in
`manifest.json`; none of them implies the product as a whole is a
production-ready beta. Roadmap item 0.9 was closed on 2026-08-17 per the
DD-008 criterion (documented internal security review, founder-signed
risk register, green security regression); an independent external
security review remains a separate, open condition for 1.0 — see
`ROADMAP.md`.

### Implemented

- machine-readable object schemas,
- executable constitutional Proof Kernel,
- explicit state transitions,
- SQLite event persistence,
- SHA-256 hash chain for event integrity,
- state reconstruction from events,
- Generative Flow reference metric,
- automated tests,
- typed knowledge graph,
- provenance records,
- confidence-bearing relations,
- graph traversal and cycle/orphan detection,
- capability-bounded agent runtime,
- human approval gates,
- auditable delegation chains,
- action receipts,
- scenario simulation and counterfactual comparison,
- Monte Carlo uncertainty analysis,
- constitutional invariants and safety gates,
- signed canonical HOSP envelopes,
- identity and key registry,
- replay and expiry protection,
- explicit trust policies,
- security gateway and threat model,
- GitHub Actions CI,
- contribution and governance framework.

### Added in 0.10.0-alpha.1 (execution-foundation and layer slices, 2026-08)

- immutable context snapshots and a minimum execution contract (`hos_core`),
- Hub entity and relation registries with attributed, non-destructive merges,
- authority roles as a separate axis from identity (`authority`),
- an end-to-end execution loop with refusal as a first-class outcome,
- Layer 5 Decision Engine slice: nine hard gates before ranking,
  evidence asymmetry, abstention and escalation as first-class outcomes,
- Sovereign Recovery Kernel: seven emergency modes mapped to R0–R4,
  dual-key sovereignty, and all six Hub contracts (freeze, snapshot,
  rollback with provenance, disconnect, sovereign export, event register),
- conversational Living Self Model: interactions separated from the model,
  declaration / observation / hypothesis epistemics, user-only
  confirmation, tensions preserved as signal, full provenance (`why`),
- purpose-limited consent gating for model writes,
- durable audit trails for self-model and recovery on the hash chain,
- I/O contract docs: `docs/self-model-contract.md`, `docs/recovery-contract.md`,
- zero mypy debt across the engine, enforced as a CI gate,
- canonical recovery event types (`RECOVERY_ACTIVATED/DEACTIVATED/REFUSED`,
  `ENTITY_FROZEN`) with historical `STATE_OBSERVED` events kept readable,
- skeleton types for the Layer 5 scales DI/IQ/AR — structure, measurement
  and interpretation policy strictly separated; no thresholds exist until
  the founder approves a versioned configuration,
- Emergency Root skeleton: versioned k-of-n policy with no defaults,
  custodian key descriptors without key material, full append-only audit,
- the HOSId pattern extended to the engine's hex identifiers (DD-010),
- an ADR index covering every decision record (`docs/adr/README.md`).

See `docs/DEFERRED_DECISIONS.md` for decisions deliberately queued for the
founder rather than resolved silently.

### Not production-ready

The current release lacks authentication, authorization, encryption at rest,
independent security review, empirical calibration and production deployment.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest -q
python run_demo.py
```

## Graphical console

A small local web UI lets you edit an `action` entity and evaluate it against the
Proof Kernel interactively, instead of reading `run_demo.py`'s console output.

```bash
python -m pip install -e ".[app]"
FLASK_APP=app.server:create_app python -m flask run
```

Then open <http://127.0.0.1:5000>. It is a thin `Applications`-layer client of
`hos_engine` (see `ECOSYSTEM.md`) — it holds no policy logic of its own.

## Project structure

```text
human-os/
├── hos_engine/
├── app/
├── apps/
│   └── user-demo/
├── schemas/
├── policies/
├── tests/
├── examples/
├── docs/
│   └── adr/
├── .github/
├── CONTRIBUTING.md
├── GOVERNANCE.md
├── SECURITY.md
└── ROADMAP.md
```

## Core success criterion

Human OS succeeds as dependence decreases on systems that reduce autonomy,
attention, energy, creative agency, responsibility, relationship quality or
alignment with the user's own values.

## Contributing

See `CONTRIBUTING.md`. Every material change must describe:

- supported constitutional genes,
- genes placed at risk,
- safeguards,
- limitations and uncertainty,
- portability and exit impact.

## License

Code is licensed under Apache-2.0 (`LICENSE`); documentation and specifications
under CC BY 4.0 (`LICENSE-DOCS`). The Human OS name and marks are not yet
covered by a published trademark policy. See `LICENSE-DECISION.md`.
