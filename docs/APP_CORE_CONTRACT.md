# Human OS Application Contract v0.1

Status: PROPOSED (P1 pełnowymiarowego audytu z 2026-08-17, §6) · decyzja
architektoniczna: `docs/adr/ADR-ARCH-003-app-core-contract.md`.
Język polski — dokument graniczny dla twórców aplikacji.

## Problem, który ten kontrakt rozwiązuje

Aplikacja użytkownika (`apps/user-demo`) implementuje dziś lokalnie własne
kopie reguł, które silnik `hos_engine` posiada już naprawdę: bramy G0–G8,
self-model, N-of-1, tryby awaryjne, zgody. Audyt nazywa to wprost: zaczynają
istnieć **Human OS A (Python Core)** i **Human OS B (JavaScript w
aplikacji)** — a po kilku miesiącach Core będzie blokował to, na co
aplikacja pozwala, albo odwrotnie. Aplikacja nie może posiadać własnej
Konstytucji wykonawczej.

## Zasada graniczna

```
UI → Request → HOS Core → Decision/Policy → Receipt → UI
```

nigdy:

```
UI → lokalna kopia reguł → decyzja UI
```

### Aplikacja (UI) wyłącznie:

1. zbiera intencję użytkownika (tekst, wybory, formularze),
2. pokazuje opcje i wyjaśnienia zwrócone przez Core,
3. pyta o zgodę i przekazuje ją jako jawne pole żądania,
4. renderuje stan i historię (w tym odmowy),
5. wysyła jawne, kompletne żądanie do Core,
6. przechowuje i pokazuje otrzymane **Receipty**.

### Core wyłącznie:

1. interpretuje politykę (Proof Kernel, DecisionEngine, ExperimentEngine,
   RecoveryKernel, CallAuthorizer, ConsentRegistry),
2. decyduje — w tym odmawia (odmowa jest wynikiem, nie błędem),
3. uruchamia przepływ (ExecutionLoop) i pilnuje bram,
4. rejestruje zdarzenie w trwałym magazynie (EventStore/SQLite),
5. kontroluje provenance (wersje polityk, źródła, supersedes),
6. zwraca **Receipt**.

## Kształt żądania (Request)

Minimalny kontrakt (niezależny od transportu — lokalny import w Pythonie,
HTTP w przyszłym backendzie, mostek WASM w PWA):

| Pole | Znaczenie |
|---|---|
| `request_id` | unikalny identyfikator żądania (idempotencja) |
| `intent` | co człowiek chce osiągnąć, jego słowami |
| `subject_id` | czyja sprawa (tożsamość) |
| `actor` | kto wysyła (tożsamość + rola z `authority.py`) |
| `consent_refs` | zgody, na które powołuje się żądanie |
| `payload` | dane specyficzne dla operacji |
| `client` | nazwa+wersja aplikacji, wersja kontraktu |

## Kształt odpowiedzi (Receipt)

| Pole | Znaczenie |
|---|---|
| `receipt_id` | identyfikator kwitu |
| `request_id` | powiązanie z żądaniem |
| `decision` | wynik (np. `Decision` Proof Kernela / outcome silnika) |
| `reasons` | powody — w tym pełne powody odmowy |
| `policy_versions` | wersje polityk/reguł, które orzekały |
| `events` | identyfikatory zdarzeń zapisanych w rejestrze |
| `at` | czas orzeczenia |

## Reguły przejściowe (stan dzisiejszy → docelowy)

1. **Prototyp `apps/user-demo` pozostaje UX-ONLY** (DD-005) — jego lokalne
   reguły są *makietą zachowań Core*, nie drugim źródłem prawdy. Każda
   nowa reguła w aplikacji musi mieć odpowiednik (lub jawny brak) w Core
   i wpis w tabeli rozjazdów poniżej.
2. **Zakaz nowych reguł tylko-aplikacyjnych:** jeżeli funkcja wymaga nowej
   bramy/polityki, najpierw powstaje w `hos_engine` (albo jako wpis DD),
   potem w UI.
3. **Docelowy transport:** etap sklepowy z backendem (DD-013) wystawia
   Core przez HTTP i aplikacja przechodzi z lokalnych makiet na Request→
   Receipt bez zmiany UX.

## Tabela znanych rozjazdów (do zamknięcia)

| Obszar | Aplikacja (makieta) | Core (prawda) | Plan |
|---|---|---|---|
| N-of-1 | własna logika faz/HOLD/prognozy | `experiment_engine.py` | mapowanie pojęć + stopniowe przejście (P1 audytu, pkt 6) |
| Bramy decyzji | G0–G8 w JS | `decision_engine.py` G0–G8 | UI ma pokazywać wynik Core; makieta do wygaszenia |
| Self-model | epistemika w JS | `self_model.py` | jak wyżej |
| Tryby awaryjne | SAFE MODE/READ-ONLY w JS | `recovery.py` | jak wyżej |
| Zgody | C0–C6 w JS | `consent.py` (inne id) | ujednolicenie słownika zgód — wymaga decyzji (DD) |
| Audyt | `S.log` w localStorage | EventStore/SQLite z hash chain | Receipty + rejestr Core |

## Kryterium końcowe (test pionowy audytu)

Intencja → Self Model → Knowledge → Decision → Consent/Authority →
Experiment → Result → Learning → Provenance → UI, z odpowiedzią w każdym
kroku na: „dlaczego?", „na podstawie czego?", „kto na to pozwolił?",
„jak to cofnąć?", „co stanie się po restarcie?".
