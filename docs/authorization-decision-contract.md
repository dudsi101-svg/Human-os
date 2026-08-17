# Authorization Decision Contract v0.1

Status: PROPOSED (P1 pełnowymiarowego audytu 2026-08-17, §12–13).
Szkielet wykonawczy: `hos_engine/authorization_decision.py`.

## Problem

Na pytanie „czy można wykonać tę operację?" odpowiada dziś **dziewięć
równoległych mechanizmów**, każdy fragmentarycznie: Identity,
AuthorityRole, RoleGrant, Capability, CallRule (`call_authorization.py`),
Consent, SecurityGateway, Approval, Proof Kernel. Funkcjonalnie poprawne —
architektonicznie brakuje **jednego miejsca kompozycji**, które złoży
fragmenty w jeden rozliczalny wynik.

## Kształt decyzji

Jedna `AuthorizationDecision` odpowiada w komplecie:

| Aspekt | Pytanie | Dzisiejszy mechanizm źródłowy |
|---|---|---|
| WHO | jaka tożsamość (rodzaj + konkret) | `security_identity` |
| BY WHAT AUTHORITY | rola / grant / delegacja | `authority.RoleGrantRegistry`, delegacja z `call_authorization` |
| ON WHAT | selektor zasobu | (brak — dług względem źródłowego Permission Grant) |
| WHAT ACTION | READ / WRITE / EXECUTE / DELEGATE | `agent_runtime` capabilities, `CallRule` |
| WHY | cel (purpose) | (brak — dług jw.) |
| UNDER WHAT CONSENT | id/wersja zgody | `consent.ConsentRegistry` |
| UNDER WHAT POLICY | wersja polityki | Proof Kernel / podpisane polityki |
| WITH WHAT CONSTRAINTS | ryzyko/czas/zakres | `CallRule` constraints, `TrustPolicy` |
| RESULT | allowed/denied + powody + kwit | wynik kompozycji |

## Reguły kompozycji (wiążące dla implementacji)

1. **Deny-first:** jeden niezaliczony aspekt = odmowa całości; aspekty nie
   kompensują się nawzajem (ten sam wzorzec co nierównoważność rzędów
   Warstwy 6 i twarde bramy G0–G8).
2. **Brak oceny ≠ zgoda:** aspekt wymagany a niedostarczony do kompozycji
   daje odmowę z powodem `NOT_EVALUATED:<aspekt>` — nigdy ciche pominięcie.
   Zestaw aspektów wymaganych jest jawną, obowiązkową konfiguracją bez
   wartości domyślnej (wzorzec DD-006/DD-007).
3. **Wynik jest kwitem:** decyzja niesie echo wszystkich aspektów (kto, z
   jakiego tytułu, na czym, po co, za jaką zgodą, pod jaką polityką) plus
   powody — nadaje się wprost na `Receipt` kontraktu App↔Core
   (`docs/APP_CORE_CONTRACT.md`).
4. **Kompozytor nie zastępuje mechanizmów:** istniejące rejestry/bramy
   pozostają źródłem prawdy swoich fragmentów; kompozytor je woła
   i składa, niczego nie reimplementując.
5. **Dług źródłowy pozostaje nazwany:** pola `resource_selector`,
   `purpose`, `approval_policy`, `audit_reference` z pełnego źródłowego
   Permission Grant nie mają dziś mechanizmów — szkielet przyjmuje je jako
   deklaracje wejścia i odnotowuje w kwicie, ale ich egzekucja to otwarta
   luka (patrz `artifact.registry.json` → authorization.open_gaps).

## Szkielet (co jest, czego nie ma)

`AuthorizationComposer` przyjmuje nazwane aspekty jako funkcje sprawdzające
oraz **obowiązkowy** zestaw `required_aspects`; zwraca niemutowalną
`AuthorizationDecision` (allowed/denied, powody, echo aspektów, id, czas).
Nie ma: własnych reguł, wartości domyślnych wymaganych aspektów, ścieżki
obejścia. Integracja z `ExecutionLoop`/`SecurityGateway` jako właściwym
wołającym — następny krok, osobna zmiana.
