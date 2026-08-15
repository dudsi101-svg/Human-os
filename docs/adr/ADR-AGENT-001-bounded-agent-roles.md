# ADR-AGENT-001: The Agent Network Applies Bounded Roles and Least Privilege

## Status
Accepted for implementation and further specification. Imported 2026-08-15
per founder review Q11, **verified against the original source docx bytes
2026-08-15** (`Human_OS_Rozszerzenie_Architektury_i_Integracja_v0_2_1.docx`,
founder-provided; filename carries a `v0_2_1` suffix not reflected in the
document's own "0.2" version header). Source: *Rozszerzenie Architektury i
Integracja v0.2*, §4. No content corrections were required.

## Decision
Human OS does not adopt a "single all-knowing agent" model. The Agent
Network consists of bounded agents with explicit roles, tools, and
responsibilities. The HOS Hub routes tasks, and HOS Core enforces policies
and execution contracts.

Named agents: **Executive/Integrator** (merges results, does not replace the
user in a decision), **Research** (searches for and evaluates sources per
Layer 3), **Health & Performance** (analyzes health data within the bounds
of risk and competence), **Finance & Business** (models costs, flows,
scenarios and risk), **Project Operator** (plans, monitors dependencies and
escalates blockers), **Legal & Compliance** (detects legal risks and
requires up-to-date sources), **Data Steward** (controls quality,
provenance, retention and access), **Automation** (executes permitted
operations in external systems), **Red Team/Critic** (looks for errors,
contradictions, gaps and overconfidence).

## Rationale
The bounded-role design is itself the safeguard against a single overpowered
agent — no agent's mandate is broader than its named domain.

## Consequences
The existing `hos_engine.agent_runtime` and `hos_engine.agent_policy`
implement generic, capability-bounded agent execution but do not yet encode
this specific nine-role roster or per-role tool/data-source scoping. Mapping
the generic runtime onto these named roles is future work.
