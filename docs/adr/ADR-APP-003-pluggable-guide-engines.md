# ADR-APP-003: The guide has swappable engines — local by default, cloud by choice

- Status: Accepted (founder decision, 2026-08-17: "architektura z wymiennym
  mózgiem to dobry pomysł, tym bardziej że na przestrzeni czasu modele się
  będą zmieniać — idźmy w te 3 silniki")
- Layer: Applications (user app / `apps/user-demo`)
- Extends: ADR-APP-002 (the in-app LLM guide and its constitutional gates)

## Context

ADR-APP-002 introduced the guide with a single engine (direct Anthropic API
on the user's own key). That leaves two structural problems: a store
customer should not have to buy tokens, and models change over time — the
app must not be welded to one provider or one generation. The founder chose
the pluggable-engine architecture over both alternatives considered
(subscription-includes-AI only; IAP question packs only).

## Decision

The guide ("Przewodnik") is an **engine-agnostic role**; the model behind
it is a swappable engine chosen by the user:

| Engine | Who pays | Data path | Status |
|---|---|---|---|
| `local` — on-device AI (browser/OS built-in Prompt API; later a full local model via WebLLM) | nobody | **nothing leaves the device** | implemented (feature-detected; default whenever available) |
| `key` — cloud model on the user's own API key; user picks the provider: **Claude (Anthropic)** or **GPT (OpenAI)** (founder decision, 2026-08-17) | the user, directly to the chosen provider | minimized C5 package | implemented (ADR-APP-002; OpenAI variant added as a provider adapter) |
| `backend` — cloud in the subscription price | the operator, priced into Premium | minimized C5 package via app backend | visible but disabled; blocked on DD-013 (backend, pricing, limits) |

Rules that hold across every engine, present and future:

1. **The constitutional gates of ADR-APP-002 are engine-independent** —
   C5 consent, payload minimization, hypothesis-only outputs, no write
   path to the model/plan, idea adoption through the G4 gate, full audit.
   The audit records which engine served each invocation.
2. **Local is the preferred default.** When a local engine is available it
   is auto-selected; the cloud is an option, not a requirement. This is
   the constitutional ordering (data sovereignty, offline autonomy,
   decreasing dependence), accepting lower answer quality as a stated
   trade-off in the UI.
3. **Engines are expected to change.** The engine layer is the stable
   contract (system rules, payload, output shape, refusal handling);
   models/providers behind it may be swapped without touching the gates.
   Local structured output cannot be guaranteed, so idea parsing is
   defensive (fence-stripping, brace extraction, empty-list fallback).
4. **No engine is ever paywalled into rights** — ADR-APP-001 §2 unchanged.
5. **Cloud providers are adapters inside the `key` engine, not new engines.**
   The `key` engine carries a provider selector (Anthropic Messages API /
   OpenAI Chat Completions API). Each provider has its own key and model
   storage (both device-local, outside app state and export), its own
   payment relationship (console.anthropic.com / platform.openai.com), and
   the audit names the provider on every invocation and switch. What
   cannot be plugged in is a consumer chat app (e.g. chat.openai.com) —
   only provider APIs, because the constitutional gates must wrap the call.

## Consequences

- Implemented now: engine selector in the guide's configuration (local /
  own key / subscription-disabled), Prompt API feature detection with
  graceful degradation, engine-aware consent copy ("silnik lokalny — nic
  nie wychodzi na zewnątrz"), engine name in every audit entry; within the
  `key` engine, a provider selector (Claude/GPT) with per-provider keys,
  models, refusal mapping (OpenAI `message.refusal` → the same honest
  refusal path), and strict JSON-schema structured output on both.
- Roadmap (PWA): full local model via WebLLM/WebGPU as an opt-in ~1.5–2.5 GB
  download, never part of the store package; store package stays ~2–4 MB.
- Open in DD-013: the backend engine (key custody, limits, Web Push reuse
  per DD-014), default cloud model and cost policy for the subscription.
