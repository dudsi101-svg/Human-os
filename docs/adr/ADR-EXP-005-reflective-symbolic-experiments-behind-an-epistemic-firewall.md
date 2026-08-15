# ADR-EXP-005: Reflective/Symbolic Experiments Sit Behind an Epistemic Firewall From Causal and Medical Claims

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_6_Silnik_Eksperymentow_Monitorowania_i_Postepu_v0_1_2.docx`
("Warstwa 6"), §32 ("Human Design, astrologia i systemy interpretacyjne w
Warstwie 6"). See `docs/FOUNDER_REVIEW_2026-08-15.md`, "Trzecia tura"
section, for provenance. Newly formulated — the source has no ADR numbering
of its own.

## Decision
Human Design, astrology, and other symbolic/interpretive systems are a
permitted *object* of a behavioral/reflective experiment (§32.1) — e.g. a
hypothesis about the effect of a 24-hour decision-delay practice suggested
by such a system. They are explicitly not a permitted *basis* for medical or
causal inference (§32.2, verbatim, four bans): the system must not treat
agreement across a few observations as proof that the underlying cosmology
or biological mechanism is true; must not use a symbolic map for diagnosis,
dosing, medical risk assessment, or predicting events as facts; must not
frame non-conformance with the map as user error, immaturity, or "living
wrong for your type"; and must not lock a user into a permanent label or
constrain their development paths.

The "zapora epistemiczna" (epistemic firewall, §32.4): data from
reflective/symbolic experiments is stored in an interpretive domain and
*does not raise the biological, clinical, or causal evidence strength in
the Knowledge Map (Layer 3)* — it stays on its own side of the wall
regardless of how consistent the pattern looks.

## Rationale
This directly extends `constitution/README.md` Ch.10 (Human Design/astrology
guardrails) into Layer 6's specific mechanics: it is not enough to *state*
that these systems are non-diagnostic — the data pipeline itself must be
structurally incapable of feeding symbolic-system agreement into a causal or
medical confidence score. A firewall implemented only as a policy statement,
without a structural separation between the two evidence pools, would not
satisfy this.

## Consequences
No `hos_engine` module implements any evidence-pool separation today; the
existing `hos_engine.knowledge_graph` has no notion of a firewalled
interpretive-evidence subgraph distinct from clinical/causal claims. When a
real Knowledge Graph / Layer 3 integration is eventually built, this ADR is
a constraint on that design: reflective/symbolic-origin claims must be
tagged and isolated at the schema level, not merely by convention, from
`CA0–CA5` causal-confidence-bearing claims (see ADR-EXP-001).
