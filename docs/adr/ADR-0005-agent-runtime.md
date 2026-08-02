# ADR-0005: Capability-bounded agent runtime

## Status
Accepted

## Decision
Agents receive explicit capabilities. Tool availability, intelligence or purpose
never imply permission. Every invocation is checked against identity, action,
resource scope, risk, approval mode and delegation chain. Every result produces
an auditable receipt.

## Constitutional rationale
An agent is an instrument of human intent, not an autonomous authority.

## Limitations
No model hosting, authentication, remote transport or production secrets
management is included in v0.6.
