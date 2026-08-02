# ADR-0008: Signed Protocol and Identity

State-changing or data-revealing messages must be signed, time-bounded and
replay-resistant. Identities are separate from keys to support suspension,
revocation and rotation. Trust is checked before consent and execution.
