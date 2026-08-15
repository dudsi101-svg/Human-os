# Human OS

Human OS is an open constitutional protocol and reference engine intended to
increase human autonomy, creative agency, responsibility, meaningful relations
and generative flows of value.

> Human OS does not decide what a person's life should become.
> It helps the person remain the author of that life.

## Current release

**Human OS Engine 0.9.0 — Protocol, Identity and Security**

Status: **BETA**

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

The final licensing model is intentionally not frozen yet. See
`LICENSE-DECISION.md`.
