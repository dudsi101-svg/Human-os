# Recovery contract (Sovereign Recovery Kernel, `hos_engine.recovery`)

Status: all six Hub contracts from the source's §9 implemented
(ADR-RECOVERY-001..004 under ADR-RECOVERY-006's resolutions). Style follows
`runtime-contract.md`.

## Mode table (ADR-RECOVERY-006)

| Mode | Constitutional risk | Auto-trigger | Dual key |
|---|---|---|---|
| SAFE_MODE | R0 | yes (owner notified) | no |
| READ_ONLY | R0 | yes (owner notified) | no |
| FREEZE | R1 | yes (owner notified) | no |
| DISCONNECT | R1 | yes (owner notified) | no |
| EXPORT | R1 | never | no |
| ROLLBACK | R2 | never | yes |
| RECOVERY | R3 | never | yes |

Dual key = approval by a different identity holding an active
`RECOVERY_CUSTODIAN` grant in scope.

## Inputs
- Activation requests: mode, initiator (id + `AuthorityRole`), scope,
  reason, expiry, verification method, trigger kind, optional custodian
  approval, owner-notification flag.
- Hub contract calls: freeze target, snapshot entity set, rollback
  (snapshot + entity), disconnect (entity + representation), export scope.

## Outputs
- `RecoveryActivation` (scope-isolated, time-bounded, reversible).
- 13-field `EmergencyEvent` for every attempt — refusals included; optional
  HMAC signature (reference mechanism, see `security/THREAT_MODEL.md`).
- `RecoverySnapshot` (non-destructive checkpoint),
  restored `HubEntity` (rollback: new version + attributed merge record,
  old version SUPERSEDED — never deleted),
  `DisconnectedRepresentation` (historical relation preserved),
  sovereign export package (open JSON incl. retired history and audit trail).
- Refusal is an exception (`RecoveryRefused`), logged before it leaves the
  kernel — ignoring a refused protection must not look like having it.

## Guarantees
- No API mutates recovery policy or the audit log (the operations do not exist).
- AGENT / SERVICE / SYSTEM_PROCESS can never activate, deactivate, or snapshot.
- Recovering one scope never unlocks another (`is_active` is per-scope).
- No AI model or external service in the code path — an AI outage cannot
  block manual recovery.

## Durable event types (DD-003, resolved 2026-08-17)
Durable recovery events map to the canonical vocabulary at the single
`_log` chokepoint:

| Outcome | Canonical `event_type` |
|---|---|
| activation, mode `FREEZE` | `ENTITY_FROZEN` |
| activation, any other mode | `RECOVERY_ACTIVATED` |
| deactivation | `RECOVERY_DEACTIVATED` |
| refusal (result `REFUSED: …`) | `RECOVERY_REFUSED` |
| usage records (snapshot / rollback / export) | `STATE_OBSERVED` |

Historical events written before DD-003 stay as `STATE_OBSERVED` and are
never rewritten; the full 13-field record remains in the payload in both
generations, so old and new events read uniformly.

## Emergency Root skeleton (DD-007, resolved 2026-08-17)
`hos_engine/emergency_root.py` implements the shape of the emergency-key
infrastructure without inventing its parameters:

- `EmergencyRootPolicy` — versioned configuration; every field (TTL,
  required authentication-strength declaration, k-of-n scheme, custodian
  roles, scope, id/version/approver) is explicit with **no defaults**;
  AGENT/SERVICE/SYSTEM_PROCESS can never be custodian roles.
- `EmergencyRootKernel` — cannot be constructed without a policy
  (missing configuration blocks the mechanism structurally); reference
  k-of-n approval flow over declared inputs; one key per custodian
  identity; TTL expiry; every request, approval, activation, refusal,
  use and expiry lands in an append-only audit trail (no mutator API)
  and optionally in a hash-chained event store as `STATE_OBSERVED`
  usage records.
- NOT included, per the founder resolution: key material, key storage,
  threshold cryptography, real authentication — those require a separate
  decision plus a deployment threat model. Test values are synthetic and
  must never become production configuration.

## Non-goals
- real key storage and threshold cryptography (see above — separate
  founder decision),
- deciding for the owner when to recover.
