
# ADR-0002: Executable Policy and State Engine

## Status
Accepted

## Decision
Implement a small reference runtime in Python with:

- append-only events,
- explicit state transitions,
- executable constitutional tests,
- deterministic aggregation of proof results,
- visible limitations.

## Rationale
The architecture must be testable before application, agent and interface layers
are allowed to depend on it.

## Consequences
The project now has executable behavior, but policy thresholds remain provisional
and require simulation, empirical research and human governance.
