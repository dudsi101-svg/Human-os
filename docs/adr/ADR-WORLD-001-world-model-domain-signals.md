# ADR-WORLD-001: The World Model Consists of Domain Models With Currency and Uncertainty

## Status
Accepted for implementation and further specification. Imported 2026-08-15
per founder review Q11, **verified against the original source docx bytes
2026-08-15** (`Human_OS_Rozszerzenie_Architektury_i_Integracja_v0_2_1.docx`,
founder-provided; filename carries a `v0_2_1` suffix not reflected in the
document's own "0.2" version header). Source: *Rozszerzenie Architektury i
Integracja v0.2*, §5. No content corrections were required.

## Decision
The World Model is adopted as a versioned model of external factors
affecting the user, projects, and decisions. It is explicitly not a "model
of the entire world." It is a set of domain models with explicit sources,
currency, scope, and error.

Domains: economy and finance; law and regulations; geopolitics and
security; weather, climate and environment; science and medicine;
technology and AI; markets, prices and supply chains; local infrastructure
and social environment.

World signal contract fields: `world_signal_id`, `domain`,
`observation_time`, `validity_window`, `source_refs`, `confidence`,
`impact_scope`, `causal_status` (correlation, hypothesis, mechanism, or
confirmed impact), `change_type` (new, increase, decrease, reversal,
expiration), `recommended_refresh`.

## Rationale
Per-signal metadata (confidence, validity window, causal status) is the
mechanism that prevents the World Model from overstating its certainty about
any one domain.

## Consequences
Not implemented. No `hos_engine` module exists for the World Model as of
2026-08-15 (see `Human OS Reconstruction Audit`, §2 and §7 — Loss Report).
The implementation roadmap in ADR-IMPL-001 places a three-domain pilot
(finance, health/science, legal environment) after the Digital Twin and
Agent Network MVPs.
