# Production Security Baseline

- asymmetric signatures,
- protected key storage,
- encrypted transport,
- clock-skew handling,
- key rotation and revocation,
- backup and recovery,
- security logging,
- rate limiting,
- vulnerability scanning,
- penetration tests,
- independent review for sensitive domains,
- per-call authorization bound to delegation-chain context, not only
  capability gating,
- memory and knowledge-graph poisoning detection,
- cryptographic content provenance for generated or transformed content,
- observed (not self-reported) measurement of degrading-dependency scores,
- agent supply-chain scanning (tool definitions, model and prompt sources),
- protected key material and threshold cryptography for Emergency Root
  (per its deployment threat model, before any real custodian keys exist),
- signed distribution of interpretation-policy files (scale policies must
  be verifiable at rest, not only via repository history),
- out-of-band verification of custodian identities before granting
  RECOVERY_CUSTODIAN roles.
