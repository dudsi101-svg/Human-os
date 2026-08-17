# ADR-RECOVERY-004: Every Emergency-Mode Use Is Logged in a Mandatory, Versioned, Signed 13-Field Record

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Sovereign_Recovery_Layer_i_Rejestr_Scalenia_v0_2_1.docx`, §8
("Rejestr zdarzeń awaryjnych"), §9 ("Kontrakty z HOS Hub"). See
`docs/FOUNDER_REVIEW_2026-08-15.md`, "Czwarta tura" section, for provenance.
Newly formulated — the source has no ADR numbering of its own, and gives no
field data types or JSON shapes, only field names and a blanket requirement.

## Decision
Every emergency-mode event must be logged with all thirteen fields below,
each mandatory, versioned, and cryptographically signed into the audit
trail (the source states this requirement identically for all thirteen
fields, rather than per-field):

`event_id`, `timestamp`, `initiator`, `recovery_mode`, `reason`, `scope`,
`systems_affected`, `actions_executed`, `data_accessed`, `changes_created`,
`expiration_time`, `verification_method`, `result`.

The Sovereign Recovery Kernel calls six named contracts on the HOS Hub
(quoted verbatim):
- **Register Recovery Event** — "Rejestruje uruchomienie trybu, zakres,
  inicjatora i podstawę autoryzacji."
- **Freeze Entity / Scope** — "Zmienia stan wskazanego bytu lub zakresu na
  SUSPENDED/FROZEN bez utraty historii."
- **Create Recovery Snapshot** — "Tworzy kanoniczny punkt kontrolny z
  powiązaniami do wersji i reprezentacji."
- **Rollback Entity / Workflow** — "Tworzy nową wersję opartą na
  wcześniejszym stanie i zapisuje łańcuch pochodzenia."
- **Disconnect Representation** — "Odłącza lokalizację lub integrację,
  zachowując relację historyczną."
- **Export Sovereign Package** — "Buduje przenośny pakiet danych, grafu,
  metadanych i rejestru zmian."

## Rationale
A "stop the system" mechanism is only as trustworthy as its own audit
trail — the source's guarantee that agents can never disable this log
(ADR-RECOVERY-002) only matters if the log itself is complete and
structurally mandatory, which is why all thirteen fields carry the same
non-negotiable requirement rather than a mix of required/optional.

## Consequences
**Update 2026-08-15 (Phase 4):** partially implemented in
`hos_engine.recovery` — every activation, deactivation, *and refusal*
produces the full 13-field `EmergencyEvent` (plus a schema version and an
optional HMAC-SHA256 signature over the canonical JSON, sharing
`security/THREAT_MODEL.md`'s local-reference-only caveat), kept in an
append-only in-kernel log with optional durable append to
`EventStore`/`SQLiteEventStore` (hash-chained, `verify_chain()`-covered by
test). Of the six Hub contracts, only **Freeze Entity / Scope** exists
(`freeze_entity()`, transitioning to `SUSPENDED` per ADR-RECOVERY-006 §4,
non-destructively); Register Recovery Event is implicit in the log; the
other four (Snapshot, Rollback, Disconnect, Export Sovereign Package)
remain unimplemented. Dedicated `recovery_*` event types are still not
added to `event.types.json` — durable events use `STATE_OBSERVED` with the
full 13-field record in the payload until that vocabulary decision is made.

**Addendum 2026-08-17 (DD-003 resolved):** the vocabulary decision was
made — `RECOVERY_ACTIVATED`, `RECOVERY_DEACTIVATED`, `RECOVERY_REFUSED`
and `ENTITY_FROZEN` are now canonical types in `event.types.json` (0.3.0)
and the event schema enum, mapped at the kernel's `_log` chokepoint.
Names follow the dictionary's UPPERCASE convention. Historical
`STATE_OBSERVED` events are not rewritten and remain readable; usage
records (snapshot/rollback/export) intentionally stay `STATE_OBSERVED`.
See `docs/recovery-contract.md` for the mapping table.

Originally none of this was implemented. Two open, source-flagged items
matter for any future implementation:
1. The source itself (§12) states `FROZEN` must be added to the
   Entity/Event schemas — `hos_engine.state_machine.ALLOWED_TRANSITIONS`
   (`draft, active, paused, completed, archived, revoked`) has no `FROZEN`
   or `SUSPENDED` state today, and `hub_entity_registry.HubEntityStatus`
   has `SUSPENDED` but not `FROZEN`. The source uses "FROZEN" alone in one
   place (§12) and "SUSPENDED/FROZEN" jointly in another (§9) without
   clarifying whether these are the same state — do not assume they are;
   resolve explicitly at implementation time.
2. The `HOS-CHG-YYYY-MMDD-NNN` change-ID format used in this source's own
   §11 merge register is a **third ID pattern**, distinct from both ID
   strategies `CLAUDE.md` already documents (`HOS-<PREFIX>-######` counter-
   based, and `uuid.uuid4().hex[:12].upper()`) — worth noting if a change-
   log generator is ever built.
