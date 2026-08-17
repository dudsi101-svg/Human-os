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

Known gap: capability grants authorize which tools an agent may call, not
whether a specific call, with its actual arguments, in its actual delegation
context, should be allowed. Per-call authorization is not yet implemented
and remains the most significant open item in this section.

Not yet mitigated: memory/knowledge-graph poisoning detection, per-call
authorization bound to delegation-chain context, cryptographic provenance
for generated or transformed content, and independent measurement of
degrading-dependency scores (currently self-reported, not observed).
