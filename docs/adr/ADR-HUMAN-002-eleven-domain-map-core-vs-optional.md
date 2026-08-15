# ADR-HUMAN-002: Eleven Life Domains, With a Protected Core and Consent-Gated Optional Domains

## Status
Accepted direction — not yet implemented. Imported 2026-08-15 from founder-provided
source `Human_OS_Warstwa_2_Model_Czlowieka_v0_1.docx`, §3 ("Mapa domen
człowieka"). See `docs/FOUNDER_REVIEW_2026-08-15.md`, "Czwarta tura"
section, for provenance. Newly formulated — the source has no ADR numbering
of its own.

## Decision
Eleven domains (§3, full table in `docs/LAYER_2_HUMAN_MODEL_DIGEST.md`
§3.2): biology & health, nervous system & psychophysiology, cognition,
emotion, identity & personality, motivation/values/agency, relationships &
social system, environment & lifestyle, consciousness/meaning/spirituality,
creativity/work/contribution, and **interpretive systems** (Human Design,
astrology, archetypes, typologies, traditions — for generating self-
reflective questions and hypotheses).

Every user has access to a **core** subset (safety, energy, emotion,
relationships, agency, meaning); specialist domains — including the
interpretive-systems domain — are **consciously activated** and *"nie
dominują profilu bez zgody"* (do not dominate the profile without consent).
Real-life phenomena usually span several domains at once (§3.1's "Zasada
domen przecinających się" — insomnia is the document's own example).

## Rationale
Gating the interpretive-systems domain behind active consent, rather than
excluding it or treating it as equal-weight-by-default, matches this
project's established stance on Human Design/astrology (Constitution Ch.10,
and the epistemic firewall pattern in `ADR-KNOWLEDGE-005`): the domain is
real and permitted, but never silently dominant.

## Consequences
No code implements this 11-domain structure or the core/optional
distinction. `human_model.py`'s flat `domain: str` field has no enumeration
matching these 11 domains and no consent-gating mechanism distinguishing
core from optional domains — a future implementation should not assume
`domain` is currently constrained to, or aligned with, this taxonomy.
