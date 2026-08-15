# ADR-AGENT-002: Every Agent Has a Versioned Card, an Autonomy Level, and a Validator

## Status
Accepted for implementation and further specification. Imported 2026-08-15
per founder review Q11, **verified against the original source docx bytes
2026-08-15** (`Human_OS_Rozszerzenie_Architektury_i_Integracja_v0_2_1.docx`,
founder-provided; filename carries a `v0_2_1` suffix not reflected in the
document's own "0.2" version header). Source: *Rozszerzenie Architektury i
Integracja v0.2*, §4.1–§4.2. No content corrections were required.

## Decision
Every agent must carry a "Karta agenta" (agent card): `agent_id` and
version; mission and domain; permitted and forbidden actions; tools and data
sources; memory scope; autonomy level A0–A5; risk class; escalation
criteria; a required validator; and quality, cost, and error metrics.

Autonomy levels: **A0** observation only; **A1** proposal without action;
**A2** preparation of an artifact for approval; **A3** low-risk execution
with the ability to reverse; **A4** conditional execution within an approved
workflow; **A5** autonomy bounded by domain, budget, time, and immediate
audit.

## Rationale
The graduated-autonomy structure caps what any agent can do without
escalation, independent of what it is technically capable of doing.

## Consequences
Not yet implemented. `hos_engine.agent_runtime.AgentManifest` carries
`may_delegate`/`max_delegation_depth` and a capability set, but no A0–A5
autonomy level field. Founder review Q7 notes this A0–A5 scale is distinct
from — and should not be confused with — the Constitution's separate R0–R4
risk scale or the Lab specification's R0–R4 risk-execution-mode scale (see
`Human OS Reconstruction Audit`, Conflict Map).
