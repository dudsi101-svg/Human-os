# ADR-KNOWLEDGE-005: The Epistemic Firewall Around Symbolic/Traditional Knowledge Is Consistent Across Layers 3, 5, and 6

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_3_Mapa_Wiedzy_i_Sygnatura_Informacji_v0_1.docx`, §11.4
("Zapora epistemiczna"). See `docs/FOUNDER_REVIEW_2026-08-15.md`, "Czwarta
tura" section, for provenance. Newly formulated — the source has no ADR
numbering of its own. This ADR exists specifically to record that the same
rule appears, independently worded but functionally identical, in three
separately-authored layer documents.

## Decision
Content from the SYM (symbolic/interpretive systems) and TRD (tradition)
source classes *"mogą wpływać na pytania/refleksję/niskoryzykowne
eksperymenty, ale nie mogą bez niezależnego wsparcia przechodzić bezpośrednio
do medycznych twierdzeń przyczynowych ani protokołów wysokiego ryzyka"* —
may inform questions, reflection, and low-risk experiments, but may not,
without independent support, feed directly into medical causal claims or
high-risk protocols.

This is functionally identical to:
- Layer 6's "zapora epistemiczna" (`ADR-EXP-005`, §32.4): reflective/
  symbolic experiment data stays in an interpretive domain and does not
  raise biological/clinical/causal confidence in the Knowledge Map.
- Layer 5's "Nienaruszalna granica" (§30.4): a symbolic system's output may
  influence questions and voluntary reflective experiments but *"Nie może
  obniżyć bramy bezpieczeństwa, podnieść siły dowodów medycznych ani
  automatycznie zmienić profilu ryzyka"* — cannot lower the safety gate,
  raise medical evidence strength, or automatically change the risk
  profile.

## Rationale
Three independently-written layer documents converge on the same firewall,
worded differently but semantically identical each time. Per this digest
series' recurring observation, this is strong evidence of a genuine,
load-bearing project-wide invariant — not a coincidence of drafting — and it
should be implemented once, centrally, rather than three times per-layer.

## Consequences
No `hos_engine` module implements any evidence-pool separation today (see
`ADR-EXP-005`'s Consequences section, which flags the same gap from Layer
6's side). This ADR adds confirmation from Layer 3 and Layer 5 that the
firewall is not layer-specific — a future Knowledge Graph implementation
should build the SYM/TRD-vs-clinical separation once, at the schema level,
and have Layers 5 and 6 both consume it rather than re-implementing their
own local version of the same rule.
