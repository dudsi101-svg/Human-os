# ADR-RECOVERY-006: Founder Resolutions for the Four Gaps That Blocked Recovery Implementation

## Status
Accepted. Resolves the four highest-severity items from `ADR-RECOVERY-005`'s
Consequences section (items 1, 3, 5, 7) via explicit founder decisions made
2026-08-15 in response to a deep audit of the project. See
`docs/FOUNDER_REVIEW_2026-08-15.md`, "Piąta tura", for the full record of
how each question was asked and answered. This ADR does not implement any
code — it records the decisions that unblock ADR-RECOVERY-001..004's
eventual implementation.

## Decision

### 1. `RECOVERY_CUSTODIAN` is mapped to the Constitution's Security Team role
The source document never defines who holds the independent recovery key in
dual-key sovereignty (`ADR-RECOVERY-003`). Founder decision: `authority.py`'s
`AuthorityRole.RECOVERY_CUSTODIAN` is formally mapped onto **Zespół
bezpieczeństwa** (Security Team), one of the Constitution's seven governance
roles (`constitution/README.md` Ch.13) — never the `OWNER` role, since the
second key exists specifically to guard against an irreversible action the
owner takes under coercion or by mistake. This is a stated, deliberate
mapping, not a discovery from source material — `authority.py` is annotated
accordingly.

### 2. Emergency modes are mapped to the Constitution's R0–R4 scale individually
Founder chose per-mode analysis over a single blanket level. Proposed
mapping, reasoned from each mode's actual reversibility and consequence
(Constitution Ch.6: R0 informational/no intervention, R1 low-risk and
easily reversible, R2 moderate, R3 significant caution warranted, R4
inadmissible without specialist support):

| Mode | R-level | Reasoning |
|---|---|---|
| SAFE MODE | R0 | Strictly reduces capability (no agents/automation); does not act on anything |
| READ-ONLY | R0 | Read-only by definition; no state change possible |
| FREEZE | R1 | Halts processes and checkpoints; explicitly non-destructive |
| DISCONNECT | R1 | Reversible; local trace and history explicitly preserved |
| EXPORT | R1 | No system-state change; risk is privacy-scoped, not action-scoped |
| ROLLBACK | R2 | Changes forward system state (via a new version); moderate consequence even though non-destructive |
| RECOVERY | R3 | Highest-consequence mode — account/device/identity recovery; closest analogue to needing the Emergency Root + dual-key safeguards |

No mode reaches R4 — none of the seven are "inadmissible"; all are
sanctioned, constitutionally-compliant mechanisms per `ADR-RECOVERY-002`.
This mapping is a proposal formalized by founder decision, not a value
derived from the source document, which does not classify its own modes
against R0–R4 at all.

### 3. Trigger mechanism is split per mode: some may auto-trigger, others never do
Founder decision: not a single rule. Protective, strictly non-destructive
modes may enter automatically on detecting a serious anomaly, with
immediate owner notification and an unconditional right to reverse the
entry. Higher-consequence modes always require explicit human initiation —
consistent with `ADR-RECOVERY-002`'s "no entity holds greater rights than
the owner" and the Constitution's AI-role boundaries.

| Mode | Trigger |
|---|---|
| SAFE MODE | May auto-trigger (protective; reduces attack surface) |
| READ-ONLY | May auto-trigger (protective; blocks writes only) |
| FREEZE | May auto-trigger (non-destructive checkpoint) |
| DISCONNECT | May auto-trigger for the specific compromised integration |
| ROLLBACK | Manual only — changes forward state |
| EXPORT | Manual only — touches sensitive/exportable data |
| RECOVERY | Manual only — the highest-consequence mode (see R3 above) |

Any automatic entry must still produce the full 13-field emergency event
log (`ADR-RECOVERY-004`) and remain instantly reversible by the owner —
automatic entry is a convenience for the protective modes, never a way
around the "explicit, bounded, auditable, time-limited, and reversible"
guarantee in `ADR-RECOVERY-002`.

### 4. `FROZEN` and `SUSPENDED` are the same state — no new entity status is added
Founder decision: Recovery's "Freeze Entity / Scope" contract
(`ADR-RECOVERY-004`) reuses the existing
`hub_entity_registry.HubEntityStatus.SUSPENDED` rather than introducing a
separate `FROZEN` status. `state_machine.py`'s `ALLOWED_TRANSITIONS` and
`hub_entity_registry.HubEntityStatus` are not modified by this decision —
this closes the naming ambiguity `ADR-RECOVERY-005` flagged (the source
document itself used "FROZEN" and "SUSPENDED/FROZEN" inconsistently)
without adding new code surface.

## Rationale
All four gaps were genuinely underdetermined by the source document — per
this project's source-integrity protocol, none were resolved by inference
during the digest or ADR-writing pass. Each was instead put to the founder
directly, in the same session as the deep audit that surfaced them, so the
project could move from "documented gap" to "actionable decision" without
guessing at safety-critical design.

## Consequences
`ADR-RECOVERY-005` remains the historical record of the gaps as originally
found — it is not edited or deleted, per this project's non-silent-
overwrite rule; this ADR supersedes items 1, 3, 5, and 7 of its
Consequences list specifically. `authority.py` is annotated with the
`RECOVERY_CUSTODIAN` mapping (item 1). No code changes are required for
items 3 or 4 (the R0–R4 mapping and the FROZEN/SUSPENDED decision are
design constraints for the eventual Recovery implementation, not present in
any code path today). Items 2, 4, 6, 8, 9 from `ADR-RECOVERY-005` remain
open and are not addressed here.

With these four resolved, the remaining blocker for beginning any
`ADR-RECOVERY-001..004` implementation work is engineering capacity, not an
unanswered design question.
