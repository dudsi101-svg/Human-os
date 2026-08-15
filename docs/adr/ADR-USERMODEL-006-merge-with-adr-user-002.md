# ADR-USERMODEL-006: Merging ADR-USER-002 Into the Warstwa 4 User-Model Specification

## Status
Accepted. Founder decision, 2026-08-15, made in direct response to the gap
`ADR-USERMODEL-005` flagged (two independent source documents describing
overlapping-but-different user-model concepts). See
`docs/FOUNDER_REVIEW_2026-08-15.md`, "Piąta tura", for how the question was
put and answered: **merge**, not keep-separate. This ADR is the merge.
`ADR-USER-002` is retained (never deleted, per this project's non-silent-
overwrite convention) and its Status line is updated to point here.

## Decision
Going forward, **`Human_OS_Warstwa_4_Model_Uzytkownika_i_Cyfrowy_Profil_v0_1.docx`'s
R0–R8 architecture and 24-object ontology (`ADR-USERMODEL-001`) is the
canonical structure** for the User Model. `ADR-USER-002`'s nine named
components and five operating modes are retained as a **secondary, named
view** over that structure — useful vocabulary, not a competing schema.
"Cyfrowy bliźniak" / "Human Digital Twin" is retired as the model's name;
"Model Użytkownika i Cyfrowy Profil Rozwojowy" (Warstwa 4's own name) is
canonical. "Digital Twin" may still appear in prose as an informal synonym
inherited from `ADR-USER-002`, but no new documentation should introduce it
as if it were the primary name.

### Component mapping (resolves the two gaps `ADR-USERMODEL-005` left open)

| ADR-USER-002 component | Warstwa 4 equivalent |
|---|---|
| Identity & Roles | R0 (Tożsamość i kontrola) + `IdentityContext`, `Role` objects |
| Goals & Values | R1 (Kierunek) + `Goal`, `Value` objects |
| State Model | R6 (Stan operacyjny) + `State` object — dimensions differ (ADR-USER-002: sleep/energy/load/mood/readiness/context; Warstwa 4 §17.1: goal significance/energy/time/competence/confidence/support/risk/stability) and are **not reconciled by this ADR** — treat Warstwa 4's dimension set as authoritative going forward, ADR-USER-002's as the historical, narrower version |
| Behavior Model | `Pattern` object + R4 (Cechy pochodne) + the "Zakaz skrótu epistemicznego" guarantee (`ADR-USERMODEL-002`) |
| **Capability Model** *(previously unmapped)* | Resolved here: the "Kompetencja" dimension of §17.1's readiness assessment, combined with the `Resource` object (§8.2, "Zasoby wewnętrzne") — Warstwa 4 never names a single "Capability Model" object, so this is a cross-cutting view over two existing parts, not a new object |
| **Decision Style** *(previously unmapped)* | Resolved here: §18 ("Tolerancja ryzyka i styl podejmowania decyzji") plus the `Decision` and `RiskPreference` objects — Warstwa 4 covers this mainly through the risk-tolerance lens rather than a general decision-style profile; treat §18 as fulfilling this component until a richer treatment is warranted |
| Project & Financial Context | The "Finanse" context category, one of ten in §8.1 — not a dedicated object in Warstwa 4; no change needed, this ADR just records the mapping |
| Social Context | The "Relacje" context category (§8.1) plus §28 ("Dostęp specjalistów, opiekunów i osób wspierających") |
| Reflective/Symbolic Layer | §25 ("Human Design, astrologia i systemy interpretacyjne") — the one component the digest already found near-verbatim identical between the two sources |

### Operating-mode mapping (ADR-USER-002's five modes, absent from Warstwa 4)

Warstwa 4 has no equivalent list — founder decision adopts the five modes as
a cross-cutting *reading* of the R0–R8 rows rather than a separate
structure: **Descriptive** reads R3–R4 (source data, derived features);
**Explanatory** reads R5 (personal hypotheses with stated mechanism/basis);
**Predictive** reads R5→R6 forward (trajectory projection); **Prescriptive**
reads R7 (decision history feeding a recommendation); **Reflective** reads
R8 (the presentational profile) together with §25's symbolic layer.

## Rationale
The founder's choice to merge, rather than keep the two documents separate,
reflects that they describe the same real-world thing (a working model of
the user) built by the same broader project at different times — keeping
them as two live, unreconciled schemas would create exactly the integration
risk this project's deep audit (2026-08-15) flagged as a general pattern
across layers. Where the two sources genuinely differ (State Model's
dimension list) this ADR does not force a false reconciliation — it records
which version now governs and leaves the discrepancy visible rather than
inventing an artificial synthesis.

## Consequences
`ADR-USER-002`'s Status line now points here; its Decision/Rationale/
Consequences text is left intact as the historical record of what that
source said. No code changes result from this ADR by itself — it is a
specification-level merge. Any future implementation of the User Model
should build against `ADR-USERMODEL-001`'s R0–R8/24-object structure using
this table as the component-naming bridge, not against `ADR-USER-002`'s
nine components directly.
