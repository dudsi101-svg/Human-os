# ADR-APP-002: An in-app LLM guide ("Przewodnik AI") behind constitutional gates

- Status: Accepted (founder directive, 2026-08-17)
- Layer: Applications (user app / `apps/user-demo`)
- Source: founder instruction of 2026-08-17 — add an LLM agent to the app
  that can explain situations and generate many more improvement ideas
  based on the user's information.

## Context

Until now the app contained no AI: recommendations came from a curated
catalog, and the "conversation" was rule-based by design
(ADR-SELFMODEL-001 forbids NLP extraction in the engine). The founder has
asked for a real LLM agent inside the app. The engine already defines how
agents must behave (capability-bounded runtime, human-approval gates,
ADR-USERMODEL-004: AI may not silently infer or write the model), so the
question is how an LLM enters the *app* without violating those layers.

## Decision

### 1. Role: explain and propose — never decide, never write

The guide ("Przewodnik AI", default model `claude-opus-5`, user-selectable)
has exactly two functions: explaining the user's current situation from
their data, and generating improvement ideas for a chosen domain. Its
output is always labeled as AI hypothesis — "hipoteza AI — nie fakt, nie
diagnoza". Structural guarantees, not promises:

- **No write path.** The agent's output lands in a display container only.
  There is no code path from an agent response to the self-model, the
  experiment list, the plan, or any consent. (Mirrors ADR-USERMODEL-004
  and the Commons boundary in ADR-COMMONS-001.)
- **Ideas are adopted only by an explicit user act**, and that act flows
  through the *existing* custom-step pipeline: the G4 substance gate
  (regex refusal, audited), evidence pinned to 1/5, risk `R-NISKIE`, full
  N-of-1 rigor. An AI idea is epistemically identical to a step the user
  typed themselves.
- **System prompt carries the constitutional rules** (no diagnosis, no
  substances/doses, hypotheses only, uncertainty marked, autonomy
  respected, red-flag symptoms → professional help, no fabrication beyond
  provided data).

### 2. Consent C5 and data minimization

A new, separate consent **C5** gates the agent (default off; toggle in the
agent card and in Konstytucja). The consent copy states exactly what
leaves the device and when: on each user-initiated question, a minimized
package — profile, goal, domain scores, *confirmed* model items, active
experiment summaries. **Never sent:** model hypotheses (HYP), the event
register, Commons/community data, the API key. The exact outgoing package
is inspectable in-app ("Co wysyłam?"). Every invocation, response,
refusal, error, and adoption is logged to the register.

### 3. BYO key as reference mechanism; backend is a founder decision

The prototype calls the Anthropic API directly from the client with the
user's own API key, stored in `localStorage` **outside the app state** —
it can never enter exports or packages. Raw `fetch` is used deliberately:
the app is a single-file, no-build artifact where an SDK cannot be
vendored. Provider refusals (`stop_reason: "refusal"`) are surfaced
honestly and audited. In the artifact preview, external calls are blocked
by CSP; the feature degrades to an explanatory message and works in the
PWA and store builds. A store release should replace BYO-key with an app
backend (key custody, rate limiting, abuse handling) — queued as DD-013.

### 4. Tier

The agent is a premium feature (per ADR-APP-001 §1: power features), so it
is included in the 30-day welcome access. The constitutional floor of
ADR-APP-001 §2 is untouched.

## Genome check

- Supports: autonomy (AI proposes, the user disposes — structurally),
  transparency (payload preview, full audit incl. refusals), minimization
  (C5 scope is closed and inspectable), consent purpose-limitation
  (separate consent, revocable, default off).
- At risk: sending sensitive profile data to an external API — mitigated
  by C5's explicit copy, per-question minimized payload, user-owned key,
  and the ban on hypothesis/registry/community egress. The residual risk
  (provider-side handling) is inherent to any LLM feature and is stated to
  the user rather than hidden.

## Consequences

- `apps/user-demo/` gains the agent card in the Decisions view; E2E tests
  (mocked API) cover the C5 gate, payload minimization, header/model
  shape, G4 blocking of substance ideas, explicit adoption, refusal
  honesty, key isolation from state, and premium gating.
- Open founder decisions → DD-013: backend proxy vs BYO-key for the store
  release, default model and cost policy, whether the agent may ever read
  conversation history (today: never), C5 legal review.
