# Mapowanie N-of-1: aplikacja ↔ ExperimentEngine (Warstwa 6)

Status: krok 1 punktu P1.6 pełnowymiarowego audytu (2026-08-17)
— „podłączyć aplikacyjny N-of-1 do `ExperimentEngine`". Zgodnie z
`ADR-ARCH-003` logika aplikacji jest **makietą** zachowań Core; ta tabela
jest słownikiem tłumaczenia makiety na prawdziwy silnik, warunkiem
każdego dalszego kroku integracji.

## Mapowanie pojęć

| Aplikacja (JS, makieta) | Silnik (`experiment_engine.py`) | Uwagi |
|---|---|---|
| eksperyment z katalogu / własny krok | `Experiment` + `ExperimentProtocol` | opis kroku → `protocol.description` |
| hipoteza wpisu katalogowego (`mech`) | `Hypothesis.statement` | horyzont z `activeLen` |
| faza `baseline` | `CycleState.BASELINE` | długość: `baselineLen` |
| faza `active` | `CycleState.ACTIVE` | wejście przez `activate()` — wymaga `BaselineQuality` ≥ BL1 |
| faza `HOLD` | `CycleState.HOLD` | w silniku HOLD wywołuje `SafetyEvent` SE2, nie ręczna flaga |
| `done` / `stopped` | `COMPLETED` / `STOPPED` | stany terminalne, w silniku nieodwracalne |
| brak odpowiednika | `WASHOUT`, `MAINTENANCE`, `INCONCLUSIVE` | luka aplikacji — silnik jest bogatszy |
| domena ochronna (`guard`) | `Metric(kind=GUARD, stop_threshold=…)` | app trzyma domenę; silnik wymaga progu — próg do zdefiniowania przy integracji |
| odprawa dnia (checkin, wartości domen) | `Observation(source=SELF_REPORT)` | pomiary ciała (C6) → `Observation(source=DEVICE)` — nigdy nie scalane |
| brama G4 (substancje) | bramka startu: `XP-8` odrzucany; wyższe klasy wymagają warunków XP-7 | regex aplikacji ≈ klasyfikacja do `ProcessClass` |
| dowody 1/5 wpisu | drabina `PersonalEvidence` PE0–PE5 (etykiety) | przypisanie klasy wymaga konfiguracji interpretacji (DD-006) |
| limit 3 równoległych eksperymentów | `ExperimentPortfolio(max_active_experiments=3)` | wartość 3 = dzisiejsza praktyka aplikacji; kanoniczna wartość §29.1 otwarta w DD-017 |
| prognoza/symulacja skutków | poza Warstwą 6 — `simulation.py` (ADR-0006) | nie mylić bytów |
| `S.log` wpisy eksperymentu | zdarzenia `STATE_OBSERVED` z `experiment_*` przez EventStore | docelowo Receipt z kontraktu App↔Core |
| pomysł Przewodnika AI „Dodaj jako własny krok" | `launch()` z `MasterTest` — AI nie może wołać (role AGENT odrzucane) | jawny akt użytkownika = wołający OWNER |

## Luki blokujące pełną integrację (nazwane, nie ukryte)

1. Aplikacja nie zbiera dziś odpowiedzi „testu nadrzędnego" (8 pytań) —
   UI musi je zadać przy starcie eksperymentu, inaczej silnik odmówi.
2. Progi mierników ochronnych: aplikacja ma domenę, silnik wymaga progu
   liczbowego zamrażanego przy starcie.
3. Transport: do czasu backendu (DD-013) silnik nie jest osiągalny z PWA —
   pierwszy krok wykonawczy to test zgodności (golden test), w którym te
   same scenariusze przechodzą przez makietę JS i silnik Python z tym
   samym wynikiem bram.

## Następny krok wykonawczy

Golden-test zgodności makieta↔silnik (scenariusze: start z/bez zgody,
G4/XP-8, HOLD po zdarzeniu, wynik nierozstrzygający) — wynik rozjazdu
trafia do tabeli rozjazdów `docs/APP_CORE_CONTRACT.md`.
