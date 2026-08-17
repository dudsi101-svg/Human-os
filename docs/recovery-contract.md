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

## Non-goals
- production key management (Emergency Root parameters are queued as DD-007),
- dedicated `recovery_*` event types (queued as DD-003; `STATE_OBSERVED` meanwhile),
- deciding for the owner when to recover.
