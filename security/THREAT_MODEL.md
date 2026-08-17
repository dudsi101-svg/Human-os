# Human OS Threat Model v0.9

Protected assets: identity, consent, human records, capabilities, messages,
receipts, signing keys and provenance.

Primary threats: impersonation, payload modification, replay, stale permission,
over-broad trust, privilege escalation, key compromise, silent aggregation,
compromised Hub and confused-deputy delegation.

Current mitigations: signed canonical envelopes, identity-key binding, expiry,
nonce replay protection, explicit trust, consent, capabilities and audit receipts.

The HMAC implementation is a local reference mechanism. Production requires
asymmetric signatures, protected key storage, encrypted transport, trusted time,
rate limiting, dependency scanning and independent security review.

## Agentic and AI-specific threats

Protected assets: agent goals, memory, knowledge graph edges, human profile
records, delegation chains and generated content.

Primary threats: goal hijack via crafted input, tool misuse beyond stated
intent, memory and knowledge-graph poisoning, rogue or runaway agents,
cascading multi-step failures, confused-deputy escalation across delegation
chains, unverifiable synthetic content presented as human-authored, and
degrading dependency masked as neutral personalization.

Current mitigations: capability grants, human approval gates, delegation
auditing, action receipts, simulation gates, extraction and dependency
policy limits (POL-002, POL-004).

Per-call authorization (closed 2026-08-17): `call_authorization.py`
supplies declarative per-capability rules — closed argument-key sets,
required keys, closed value vocabularies, payload size bounds, and
delegation-context limits (direct-holder-only, maximum chain length) —
evaluated by `AgentRuntime` on every invocation before the tool executes.
The authorizer's stance toward unruled capabilities must be declared
explicitly (ALLOW or DENY); a denied verdict is a first-class DENIED
receipt. Rules judge the call as declared; they cannot verify the
declaration's honesty.

Not yet mitigated: memory/knowledge-graph poisoning detection,
cryptographic provenance for generated or transformed content, and
independent measurement of degrading-dependency scores (currently
self-reported, not observed).

## Sovereignty and recovery mechanisms

Protected assets: emergency modes and their activation records, recovery
snapshots and rollback provenance, the canonical recovery event types
(`RECOVERY_ACTIVATED`, `RECOVERY_DEACTIVATED`, `RECOVERY_REFUSED`,
`ENTITY_FROZEN`), Emergency Root policies and key descriptors
(`emergency_root.py`), custodian role grants, and scale interpretation
policies (`decision_scales.py`).

Primary threats: an agent or service activating or deactivating a
protective mode; custodian collusion or coercion below the declared k-of-n
threshold; a forged or tampered interpretation policy changing how DI/IQ/AR
measurements are read; a missing policy silently defaulting to permissive
behavior; suppression or rewriting of refusal records; confusion between
durable recovery events and generic `STATE_OBSERVED` usage records.

Current mitigations: AGENT/SERVICE/SYSTEM_PROCESS can never activate or
deactivate recovery, and the refusal itself is logged; consequential modes
require a distinct `RECOVERY_CUSTODIAN` identity (dual key); Emergency Root
is unconstructible without a complete versioned policy (no defaults) and
keeps an append-only audit; missing scale configuration is a structural
`CONFIGURATION_REQUIRED` outcome, never a fallback; canonical recovery
events flow through the hash-chained event store; interpretation policies
are versioned, founder-approved and superseded-never-overwritten.

Not yet mitigated: real key storage and threshold cryptography for
Emergency Root (deliberately deferred pending a deployment threat model,
DD-007), cryptographic signing of interpretation-policy files at rest
(currently plain JSON in the repository, integrity rests on git history and
review), and out-of-band custodian identity verification.
