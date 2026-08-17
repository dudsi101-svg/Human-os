# ADR-APP-004: Biometric/health data — local import only, C6 consent, explicit-act boundary

- Status: Accepted (founder direction, 2026-08-17: add biometric data reading
  and similar capabilities; implemented as the constitution-compatible slice)
- Layer: Applications (user app / `apps/user-demo`)
- Related: ADR-APP-002/003 (AI guide gates), ADR-COMMONS-001 (sovereignty
  asymmetry), DD-016 (native health-store access)

## Context

The founder wants biometric capabilities ("sczytywanie danych biometrycznych
i inne"). A browser PWA cannot read Apple Health / Google Health Connect
directly — that requires a native store app. What a PWA *can* do honestly:
read user-exported files locally, and use the platform authenticator
(WebAuthn) as an app lock. Body data is among the most sensitive data the
app will ever hold, so the boundaries matter more than the feature.

## Decision

1. **Import is local-only.** Health exports (Apple Health XML, generic CSV,
   Human OS JSON) are parsed entirely on the device; nothing leaves it. The
   parsed series (steps, sleep hours, heart rate, resting HR, HRV, weight,
   daily-aggregated, capped at 366 days) live in app state, are included in
   the user's export, and can be wiped with one audited action.
2. **A separate consent (C6) gates the feature.** Off by default; enabling
   or withdrawing is audited. Withdrawal blocks imports but never deletes
   existing series — deletion is the user's separate right.
3. **The model boundary is an explicit act.** Imported series never flow
   into the "O mnie" self-model automatically. The user may explicitly save
   a 7-day average as an observation (OBS, createdBy user, sourced to the
   import) — the same epistemic rules as everything else.
4. **The AI guide never sees biometrics.** `agentPayload()` does not include
   `S.biometrics`, under any engine or provider; a dedicated test enforces
   this. Extending the payload would be a new founder decision, not a patch.
5. **Biometric app lock is protection, not measurement.** WebAuthn platform
   authenticator (Face ID / fingerprint / device PIN) can lock the app's
   screen. Credential id lives device-side outside app state and export
   (like API keys). The UI states honestly that this is a screen lock, not
   encryption at rest. Enabling/disabling is audited; disabling requires a
   successful authentication.
6. **Live sensors and native health stores are out of scope here.** Web
   Bluetooth heart-rate reading (Android/desktop Chrome only) and native
   HealthKit / Health Connect integration (store packaging) are deferred —
   see DD-016.

## Consequences

- New "Pomiary ciała" card in the "O mnie" hub; C6 line in the consent
  registry; lock row in the rights screen.
- The N-of-1 experiment engine gains real, objective baselines the user can
  cite (explicitly) instead of impressions.
- Tests: `test_bio.js` covers the C6 gate, Apple XML parsing (per-day
  sum/avg/duration), CSV merge, explicit-act model boundary, AI-payload
  isolation, export inclusion, audited wipe, and the full lock lifecycle
  including failed authentication.
