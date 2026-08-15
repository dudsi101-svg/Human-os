# ADR-RECOVERY-001: Seven Named Emergency Modes, Ranked Above Core/Hub/Agents in an Eight-Level Control Hierarchy

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Sovereign_Recovery_Layer_i_Rejestr_Scalenia_v0_2_1.docx` (version
0.2.1, dated 2026-07-21, status "przyjęte do rdzenia" — accepted into the
core). This is the single document `CLAUDE.md` previously identified as
blocking all Recovery/SAFE MODE work ("confirmed to exist, content
unavailable") — its bytes are now available. See
`docs/FOUNDER_REVIEW_2026-08-15.md`, "Czwarta tura" section, for provenance.

**Important framing, stated by the source itself (§13, its final section):**
this document is a *normative/architectural merge decision*, not a technical
specification. Its own header records the decision as "Scalone bez
konfliktów semantycznych; wymaga implementacji technicznej i testów"
(merged without semantic conflicts; requires technical implementation and
tests). It contains no ADR-numbered decisions, no field data types, no
threshold/TTL values, and does not name any `hos_engine` module. The
ADR-RECOVERY series is newly formulated from its content, and — per this
project's source-integrity protocol — records the source's own gaps
explicitly rather than filling them in by inference. See ADR-RECOVERY-005
for the consolidated gap list.

## Decision
The **Sovereign Recovery Kernel** is adopted as a protected HOS Core
component, explicitly "outside the normal agent cycle" — the ninth listed
element of HOS Core's component set (alongside Event Engine, Context
Manager, Memory Controller, Policy & Permission Engine, Workflow Engine,
Scheduler, AI Orchestrator Runtime, Observability & Audit; see
`ADR-CORE-001`).

Seven named emergency modes, quoted verbatim from the source:
- **SAFE MODE** — "Uruchomienie bez agentów, automatyzacji i zapisów
  zewnętrznych; dostęp do danych, konfiguracji, eksportu i odzyskiwania."
- **FREEZE** — "Natychmiastowe zatrzymanie procesów, kolejek i zmian; zapis
  punktu kontrolnego bez niszczenia danych."
- **READ-ONLY** — "Dozwolony odczyt i analiza; zakaz modyfikacji,
  publikacji, wysyłki, płatności i zmian w systemach zewnętrznych."
- **DISCONNECT** — "Odłączenie wybranych integracji bez utraty lokalnego
  śladu, metadanych i historii połączeń."
- **ROLLBACK** — "Powrót obiektu, modułu, konfiguracji lub systemu do
  wcześniejszego stanu przez utworzenie nowej wersji, bez kasowania
  historii."
- **EXPORT** — "Pełny eksport danych i grafu w otwartych formatach, bez
  blokady dostawcy."
- **RECOVERY** — "Odtworzenie działania po awarii, utracie konta,
  uszkodzeniu danych, przejęciu urządzenia lub błędzie agenta."

An eight-level control hierarchy (highest precedence first):
1. User / system owner
2. Human OS Constitution
3. **Sovereign Recovery Kernel**
4. HOS Core and its security policies
5. HOS Hub and registries
6. Agents and automations
7. External integrations
8. Interfaces and representations

The Sovereign Recovery Kernel outranks HOS Core, the Hub, agents, and
integrations — it yields only to the Constitution and to the user/owner
themselves.

## Rationale
Source §0's own compatibility table declares this addition compatible
("ZGODNE") with the Constitution, HOS Core v0.2, HOS Hub, and Human OS Lab,
framing it as a technical enforcement mechanism for rights the Constitution
already grants (autonomy, data control, reversibility, right of exit and
revocation) rather than a new grant of rights. Ranking it above ordinary
security policy — but below the Constitution and the user — matches the
Constitution's own stated precedence (`constitution/README.md` Ch.2's
values hierarchy already places human authorship above system continuity).

## Consequences
No code implements any of this. `hos_engine` has no Sovereign Recovery
Kernel module, no emergency-mode state machine, and no representation of
this eight-level hierarchy. The closest existing code artifact is
`authority.py`'s `AuthorityRole.RECOVERY_CUSTODIAN` — but per ADR-RECOVERY-005,
this source document never defines or justifies that role, so the two
should not be assumed to line up until that gap is resolved. Before writing
any Recovery/SAFE MODE code, resolve the open items in ADR-RECOVERY-005 —
this is exactly the kind of safety-critical, autonomy/consent-adjacent
design the project's escalation rules call out for explicit human
sign-off before implementation, not just documentation.

**Update 2026-08-15 (Phase 4, after ADR-RECOVERY-006's resolutions):** a
first slice now exists — `hos_engine.recovery.SovereignRecoveryKernel`
implements all seven `EmergencyMode`s with the per-mode R0–R4 mapping and
per-mode auto-vs-manual trigger policy from ADR-RECOVERY-006, scope-isolated
time-bounded activations, and the Freeze Entity/Scope Hub contract (18
tests, `tests/test_recovery.py`). The eight-level control hierarchy as a
whole, the remaining five Hub contracts, Emergency Root's key
infrastructure, and any UI remain unimplemented.
