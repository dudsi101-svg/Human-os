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
