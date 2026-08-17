# ADR-COMMONS-001: "Wspólnie" (Commons/Collaboration Module) — Principles, Structure, Rollout

## Status
Accepted direction — founder implementation directive delivered in-session
2026-08-17 (no source DOCX; full structural digest:
`docs/COMMONS_MODULE_DIGEST.md`). First UX slice exists in the user-demo
artifact (federated package exchange, opt-in C4); engine implementation not
started.

## Decision
1. **Opt-in module.** Solo use of Human OS remains fully legitimate; the
   module activates only by the user's explicit choice (consent C4).
2. **Governing principle:** "Mniej obserwowania innych. Więcej wspólnego
   działania." No scroll-based feed, no popularity mechanics, no
   time-in-app incentives; people gather around a goal, an experience,
   a problem, or a concrete action.
3. **Naming:** user-facing **Wspólnie**; architectural
   **Commons / Collaboration Module**.
4. **Six sections:** Wyzwania (challenges), Kręgi (small private support
   circles, 3–12 people), Doświadczenia (structured experience cards),
   Wzajemna pomoc (mutual aid), Projekty (longer collaboration),
   Wspólne wnioski (aggregated community knowledge).
5. **Sovereignty boundary:** no social-activity outcome ever changes the
   private user model automatically — only the explicit user act
   "Dodaj do mojego modelu" crosses that line (flow: sections → actions &
   results → explicit consent → user model / Hub).
6. **Hard bans (constitutional):** global people-ranking; any single
   "user worth" number; social scoring of persons; covert profiling by AI;
   AI-generated social pressure; rewarding in-app activity instead of
   real-world action. Contextual signals (e.g. "8 of 10 voluntary
   commitments met") are permitted.
7. **Encouragement mechanics** (non-addictive): collective challenge pulse,
   voluntary action partner, self-defined small commitments, support calls,
   group totals, milestones, continuity-without-punishment, "To mi pomogło"
   gratitude instead of likes, short AI summaries, out-of-app action focus.
8. **Rollout order (binding):** (1) private MVP — invite-only circles,
   simple challenge, join, check-in, comments, resignation; (2) experience
   cards with knowledge-type labels; (3) public challenges only after
   identity, permissions, and moderation exist; (4) collaboration AI;
   (5) anonymous aggregation under a separate consent; (6) projects and
   local actions.

## Consequences
The existing artifact demo's "public challenge catalog" is a *template
catalog*, not a public feed (no identity/moderation infrastructure yet) —
it must be labeled accordingly. Engine-side entities/events are specified
in ADR-COMMONS-002; canonical event-vocabulary changes are queued as DD-009
rather than applied silently.
