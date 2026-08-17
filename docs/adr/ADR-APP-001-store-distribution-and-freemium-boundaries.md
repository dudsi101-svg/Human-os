# ADR-APP-001: Store distribution and the constitutional boundaries of a freemium model

- Status: Accepted (founder directive, 2026-08-17)
- Layer: Applications (user app / `apps/user-demo`)
- Source: founder instruction of 2026-08-17 — prepare the personal app for
  store distribution for other users, with a free tier ("z pewnymi
  ograniczeniami") and a premium tier ("z full dostępem").

## Context

The personal Human OS app (single-file prototype, `apps/user-demo/`) has so
far been a private artifact for one user. The founder has directed that it be
prepared for distribution through app stores (Google Play / App Store) to
other users, with a freemium model: a free tier with some limitations and a
paid premium tier with full access.

Monetization touches constitutional ground. The Constitution and genome
registry guarantee portability and exit (a user's ability to leave with
their data), autonomy, and freedom from manipulation. A naive freemium
split could paywall exactly those guarantees — which would make the paid
tier a constitutional violation, not a business model.

## Decision

### 1. Freemium is accepted as the distribution model

- A **free tier** exists and is a complete, sovereign product — not a
  crippled demo. It includes the full self-model ("O mnie", conversation,
  living self-model with consent gates), the recommendation engine and
  catalog, **one experiment at a time with full N-of-1 rigor**, the
  scenario simulator, the daily brief, the full event register, emergency
  modes, and unconditional export / import / erasure.
- A **premium tier** (subscription) may gate *power features*: up to three
  parallel experiments with the aggregate forecast, the Plan/reminders tab,
  and the "Wspólnie" (Commons) module. Future additions (e.g. sync) may
  also be premium.

### 2. The constitutional floor — never paywalled

The following can **never** be premium features, in any future revision:

- export of all data in open JSON, import (right of return), and
  irreversible erasure — exit from the system must not cost money;
- the user's model and its epistemics (viewing, correcting, confirming,
  rejecting, `why` provenance);
- emergency modes (SAFE MODE, READ-ONLY, wipe) — sovereignty is not a
  feature flag;
- the event register (audit of what the system did and refused to do).

Downgrading from premium to free (expiry, cancellation, deactivation)
**never deletes or locks data**: running experiments keep running, Commons
data stays readable and exportable; only *starting new* gated activity is
limited. The app states this guarantee verbatim in the "Wersja i Premium"
screen ("Gwarancja konstytucyjna").

### 3. Monetization bans

- **No ads.** The subscription is the only revenue source.
- **No sale, sharing, or secondary use of user data** (consistent with
  ADR-USERMODEL-003's ban on secondary use).
- **No sponsored placement** in recommendations (the Layer 5 invariant that
  `sponsored` is absent from the ranking key applies to the app's catalog
  as well).
- **No dark patterns around the paywall**: gated tabs stay visible and say
  honestly that they are premium; the paywall screen shows the full
  comparison table; the trial (7 days) requires no payment data and is
  single-use; expiry returns the user to the free tier silently logged as
  an event, never as data loss.

### 4. Billing and the reference mechanism

The prototype ships a **reference activation mechanism only**: an
activation-code input that validates format (`HOS-XXXX-XXXX`), plus a
single-use local trial. This is explicitly *not* a license system and is
labeled as such in the UI. A store release must use the platform's own
billing (Google Play Billing / App Store IAP) as the source of truth for
entitlements. All entitlement transitions (trial start, expiry, activation,
deactivation) are logged to the app's event register.

### 5. Distribution route (direction, not final)

The intended route is the web app packaged for stores (PWA→TWA for Google
Play; a thin wrapper for App Store), keeping the single-file, local-first
architecture. Store-required disclosures are already in-app under
"O aplikacji i prywatność": local-only data (no server, no accounts, no
telemetry), health disclaimer (not a medical device, not crisis
intervention), license notices, and user-controlled deletion. Final choice
of packaging, store accounts, and pricing is deferred — see DD-011.

## Genome check

- Supports: portability/exit (explicitly protected from monetization),
  autonomy (free tier is sovereign and complete), transparency (honest
  paywall, audited entitlement events).
- At risk: none identified as long as §2 and §3 hold; the deliberate
  boundary is that *convenience and scale* features are paid while
  *rights* are not.

## Consequences

- `apps/user-demo/` gains the tiering implementation; E2E tests cover the
  gates, the trial lifecycle, expiry without data loss, and the presence of
  the constitutional-guarantee and compliance screens.
- Pricing, trial length beyond the prototype's 7 days, the final
  free/premium split, and the concrete packaging pipeline are open founder
  decisions — queued as DD-011 in `docs/DEFERRED_DECISIONS.md`.
