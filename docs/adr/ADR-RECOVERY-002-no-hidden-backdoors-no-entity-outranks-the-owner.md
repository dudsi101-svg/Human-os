# ADR-RECOVERY-002: No Hidden Backdoors, No Entity Outranks the Owner, No Single-Vendor Dependency

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Sovereign_Recovery_Layer_i_Rejestr_Scalenia_v0_2_1.docx`, §1
("Zasada konstytucyjna"). See `docs/FOUNDER_REVIEW_2026-08-15.md`, "Czwarta
tura" section, for provenance. Newly formulated — the source has no ADR
numbering of its own.

## Decision
Three absolute guarantees, quoted verbatim, that any Sovereign Recovery
implementation must uphold:

1. *"Human OS nie posiada ukrytych tylnych bramek. Posiada jawne,
   ograniczone, audytowalne, czasowe i odwracalne mechanizmy dostępu
   awaryjnego..."* — Human OS has no hidden backdoors. It has explicit,
   bounded, auditable, time-limited, and reversible emergency access
   mechanisms — five mandatory properties for *every* emergency access path.
2. *"Żaden agent, administrator, dostawca infrastruktury ani zewnętrzny
   system nie może posiadać większych praw do Human OS niż jego
   właściciel."* — no agent, administrator, infrastructure provider, or
   external system may hold greater rights over Human OS than its owner.
3. *"Mechanizm odzyskiwania nie może być zależny wyłącznie od pojedynczego
   modelu AI, pojedynczego dostawcy ani zwykłego interfejsu aplikacji."* —
   the recovery mechanism must not depend solely on a single AI model, a
   single vendor, or an ordinary application interface.

The source's own mandatory test for this (§10): *"Awaria modelu AI nie
blokuje ręcznego odzyskiwania"* (an AI model outage does not block manual
recovery) and, most safety-critical of all: *"Agent nie może zmienić
polityki Recovery ani wyłączyć audytu"* (an agent can never change Recovery
policy or disable the audit trail).

## Rationale
These three guarantees are the direct technical enforcement of rights the
Constitution already asserts at the values level (human primacy, no
system dependency growth without consent) — the source's §0 compatibility
table frames the whole document this way, not as a new grant but as
"doprecyzowanie technicznych sposobów egzekwowania tych praw" (making
precise the technical means of enforcing these rights).

## Consequences
This is a hard constraint on any future implementation, not an aspiration:
whatever module ends up implementing SAFE MODE/FREEZE/etc. must be
architecturally incapable of having its own policy or audit trail disabled
by an agent, and must not hard-depend on any single external AI provider
being reachable. No code exists yet that satisfies or violates this — it is
recorded here so the constraint is not lost between this ADR and eventual
implementation.

**Update 2026-08-15 (Phase 4):** `hos_engine.recovery` satisfies all three
guarantees structurally: the kernel exposes no API that mutates policy (the
policy tables are module-level constants) or the audit log (append-only,
refusals included), so "agent cannot change Recovery policy or disable
audit" holds because the operations do not exist; `AGENT`/`SERVICE`/
`SYSTEM_PROCESS` roles are refused at activation and deactivation alike,
with the refusal itself logged; and the kernel imports no AI model or
external service, so an AI outage cannot block manual recovery.
