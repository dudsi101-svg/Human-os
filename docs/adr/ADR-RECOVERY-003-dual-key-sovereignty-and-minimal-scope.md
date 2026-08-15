# ADR-RECOVERY-003: Dual-Key Sovereignty and Minimal Scope Contain Coercion and Blast Radius

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Sovereign_Recovery_Layer_i_Rejestr_Scalenia_v0_2_1.docx`, §5
("Emergency Root"), §6 ("Dwukluczowa suwerenność"), §7 ("Minimalny zakres
dostępu"). See `docs/FOUNDER_REVIEW_2026-08-15.md`, "Czwarta tura" section,
for provenance. Newly formulated — the source has no ADR numbering of its
own. No threshold-scheme parameters (e.g. which operations require the
second key, exact TTLs) are specified by the source; this ADR records only
what is stated, not what is implied.

## Decision
**Emergency Root** is explicitly not an ordinary administrative account
(source, verbatim: *"Nie jest kontem do codziennej administracji"*) and is
explicitly closed to agents and automations (*"Nie jest dostępny dla
agentów ani automatyzacji"*). It runs only predefined emergency procedures,
requires a separate recovery key and strong authentication, leaves an
undeletable audit trail on every use, and is scope- and time-bounded with
automatic expiry.

**Dual-key sovereignty:** critical actions may require both the owner's key
and an independent recovery key; the recovery key may be offline or
threshold-split (e.g. a 2-of-3 secret-sharing scheme). The source states
this exists specifically to protect *"przed... nieodwracalnym działaniem
wykonanym pod presją lub przez pomyłkę"* — against an irreversible action
taken under duress or by mistake, not only against account takeover.

**Minimal scope of access:** recovering one area (the source's example:
Google Drive integration) never unlocks others (Gmail, finances, devices,
business agents). Verbatim: *"Uruchomienie procedury dla jednego obszaru
nie odblokowuje pozostałych."*

## Rationale
These three mechanisms address three distinct threats with three distinct
shapes: Emergency Root closes the "an automated process could invoke
recovery" gap; dual-key sovereignty closes the "the owner themself, under
coercion or by mistake, could trigger something irreversible" gap; minimal
scope closes the "blast radius" gap (a single compromised or misused
recovery grant should not cascade). None of the three is a substitute for
the other two.

## Consequences
No code implements Emergency Root, threshold key-splitting, or scope
isolation for recovery today. `hos_engine.authority.RoleGrantRegistry`
already supports per-scope role grants (including wildcard `"*"`) and could
be a natural fit for minimal-scope enforcement, but this has not been
verified or designed — it is a candidate, not a decision. No TTL values,
key-splitting library, or authentication-strength requirement is specified
by the source; per ADR-RECOVERY-005, these are open implementation items,
not gaps to be silently filled by this ADR.

**Update 2026-08-15 (Phase 4):** `hos_engine.recovery` implements dual-key
sovereignty for `ROLLBACK`/`RECOVERY` (custodian approval required, the
custodian must be a different identity than the initiator, and — when a
`RoleGrantRegistry` is wired in — must hold an active `RECOVERY_CUSTODIAN`
grant in scope, exactly the candidate integration this ADR predicted).
Scope isolation is enforced: `is_active(mode, scope)` is per-scope, so
recovering one area never unlocks another. Every activation is
time-bounded (`expires_at` mandatory, auto-expiry on check). Threshold
key-*splitting* (e.g. 2-of-3 secret sharing) and real key infrastructure
remain unimplemented — the current custodian check is role-based, a
reference mechanism in the same sense as the project's HMAC signing.
