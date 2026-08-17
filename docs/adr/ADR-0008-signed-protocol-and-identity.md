# ADR-0008: Signed Protocol and Identity

## Status
Accepted — implemented in engine release 0.9 (`protocol_security`,
`security_identity`, `trust`, `replay_guard`, `security_gateway`).

State-changing or data-revealing messages must be signed, time-bounded and
replay-resistant. Identities are separate from keys to support suspension,
revocation and rotation. Trust is checked before consent and execution.
