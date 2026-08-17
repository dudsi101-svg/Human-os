# Kolejka odłożonych decyzji (Deferred Decisions Queue)

Tryb pracy (dyrektywa założyciela, 2026-08-16): praca ciągła w tle bez
przerywania; momenty wymagające decyzji człowieka są **odkładane tutaj**
zamiast blokować pracę. Każdy wpis ma: kontekst, opcje, rekomendację
i co zrobiono tymczasowo. Rozstrzygnięcia będą nanoszone w trakcie —
po decyzji wpis przenosimy do `docs/FOUNDER_REVIEW_2026-08-15.md`
(lub nowego rundy) z datą i skutkiem.

Status: OPEN = czeka na decyzję · PROVISIONAL = przyjęto tymczasowe
rozwiązanie opisane niżej · RESOLVED = rozstrzygnięte (z datą).

---

## DD-001 · CI a mypy (OPEN — warunek wstępny spełniony)
`make verify` uruchamia mypy, ale CI (`.github/workflows/ci.yml`) — nie.
**2026-08-16: dług zszedł do 0** (`mypy hos_engine` czysty, 33 pliki).
Pozostaje decyzja: czy dodać `mypy hos_engine` do CI jako bramkę?
**Rekomendacja:** tak — baza jest zielona, bramka utrwali stan zerowy.
**Tymczasowo:** CI bez zmian; `make verify` łapie regresje lokalnie.

## DD-002 · Promocja pozycji self-modelu do encji Hub (OPEN)
Potwierdzone pozycje Living Self Model (wartości, cele) mogłyby stawać się
encjami Hub (`GOAL`, `KNOWLEDGE_CLAIM`) z relacjami. Wymaga decyzji
o semantyce: czy potwierdzenie = automatyczna promocja, czy osobny,
jawny akt użytkownika? (Konstytucja: minimalizacja i zgoda celowa
sugerują jawny akt.)
**Rekomendacja:** osobny jawny akt („dodaj do Hub") + relacja
`DOTYCZY`/`NALEZY_DO`; bez automatu.
**Tymczasowo:** brak promocji; feed `decision_inputs()` wystarcza.

## DD-003 · `recovery_*` w kanonicznym słowniku zdarzeń (OPEN)
ADR-RECOVERY przewiduje docelowe typy zdarzeń `recovery_*`;
dziś zdarzenia trwałe idą jako `STATE_OBSERVED`. Dodanie nowych typów
zmienia kanoniczny `event.types.json` + enum w `schemas/event.schema.json`
(zmiana materialna wg CONTRIBUTING).
**Rekomendacja:** dodać `recovery_activated`, `recovery_deactivated`,
`recovery_refused`, `entity_frozen` w jednej zmianie ze schematem i testami.
**Tymczasowo:** `STATE_OBSERVED` (zgodnie z ADR-RECOVERY-006 notą).

## DD-004 · HYPOTHESIS vs AI_INFERENCE (OPEN)
`EvidenceType` ma oba; ADR-SELFMODEL-001 przyjął konwencję
(HYPOTHESIS = interpretacje konwersacyjne czekające na potwierdzenie,
AI_INFERENCE = wnioski z danych). Czy docelowo scalić w jedną klasę
z polem `method`?
**Rekomendacja:** zostawić dwa (różne źródła epistemiczne), doprecyzować
w schemacie Layer 2 przy najbliższej rewizji.
**Tymczasowo:** konwencja z ADR-SELFMODEL-001 obowiązuje.

## DD-005 · Relacja aplikacji demo do repo (OPEN)
Aplikacja użytkownika (artefakt, single-file) implementuje wzorce silnika
po stronie klienta (self-model, bramy, recovery) jako demo produktowe.
Czy ma trafić do repo (np. `apps/user-demo/`) jako artefakt referencyjny
Human OS Lab (ADR-LAB), czy pozostać poza repo?
**Rekomendacja:** dodać do repo jako `apps/user-demo/` z README
o statusie „UX-only prototype" (spójnie z ADR-LAB-006 localStorage).
**Tymczasowo:** poza repo (punkt powrotu utrzymany).

## DD-007 · Parametry Emergency Root (OPEN)
Sześć kontraktów Hub jest zaimplementowanych; pozostaje infrastruktura
klucza awaryjnego. Źródło (ADR-RECOVERY-003) wprost nie podaje: wartości
TTL, wymaganej siły uwierzytelnienia, biblioteki/schematu podziału
progowego (np. 2-z-3). ADR-RECOVERY-005 klasyfikuje to jako otwarte
pozycje wdrożeniowe — implementacja bez decyzji wypełniałaby luki po cichu.
**Rekomendacja:** szkielet typów (deskryptor klucza, deklaracja silnego
uwierzytelnienia) z parametrami jako argumenty konstruktora bez wartości
domyślnych; konkretne TTL/schemat — decyzja założyciela.
**Tymczasowo:** kontrola dwukluczowa oparta o role (RECOVERY_CUSTODIAN),
jawnie oznaczona jako mechanizm referencyjny.

## DD-006 · Skale DI/IQ/AR i profil §18 (OPEN)
Layer 5 digest opisuje skale DI/IQ/AR i dziesięcioosiowy profil §18;
implementacja wymaga interpretacji progów, których źródło nie podaje
liczbowo. Wdrożyć z progami roboczymi (oznaczonymi PROVISIONAL), czy
czekać na doprecyzowanie założyciela?
**Rekomendacja:** wdrożyć szkielet typów bez progów liczbowych;
progi jako parametry konstruktora bez wartości domyślnych.
**Tymczasowo:** nie implementowane.
