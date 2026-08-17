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

## DD-001 · CI a mypy (RESOLVED 2026-08-17)
`make verify` uruchamia mypy, ale CI (`.github/workflows/ci.yml`) — nie.
**2026-08-16: dług zszedł do 0** (`mypy hos_engine` czysty, 33 pliki).
Pozostawała decyzja: czy dodać `mypy hos_engine` do CI jako bramkę?
**Rekomendacja:** tak — baza jest zielona, bramka utrwali stan zerowy.
**Rozstrzygnięcie (2026-08-17):** founder zaakceptował porządki tego etapu;
krok `python -m mypy hos_engine` dodany do `.github/workflows/ci.yml`
między ruff a pytest, zgodnie z rekomendacją.

## DD-002 · Promocja pozycji self-modelu do encji Hub (RESOLVED 2026-08-17)
Potwierdzone pozycje Living Self Model (wartości, cele) mogłyby stawać się
encjami Hub (`GOAL`, `KNOWLEDGE_CLAIM`) z relacjami. Wymaga decyzji
o semantyce: czy potwierdzenie = automatyczna promocja, czy osobny,
jawny akt użytkownika? (Konstytucja: minimalizacja i zgoda celowa
sugerują jawny akt.)
**Rekomendacja:** osobny jawny akt („dodaj do Hub") + relacja
`DOTYCZY`/`NALEZY_DO`; bez automatu.
**Tymczasowo:** brak promocji; feed `decision_inputs()` wystarcza.
**Rozstrzygnięcie foundera (2026-08-17):** potwierdzenie w Living Self
Model NIE oznacza automatycznej promocji do Hub. Promocja wymaga
osobnego, jawnego działania użytkownika („Dodaj do Hub"); operacja musi
być wersjonowana, audytowalna i odwracalna.

## DD-003 · `recovery_*` w kanonicznym słowniku zdarzeń (RESOLVED 2026-08-17)
ADR-RECOVERY przewiduje docelowe typy zdarzeń `recovery_*`;
dziś zdarzenia trwałe idą jako `STATE_OBSERVED`. Dodanie nowych typów
zmienia kanoniczny `event.types.json` + enum w `schemas/event.schema.json`
(zmiana materialna wg CONTRIBUTING).
**Rekomendacja:** dodać `recovery_activated`, `recovery_deactivated`,
`recovery_refused`, `entity_frozen` w jednej zmianie ze schematem i testami.
**Tymczasowo:** `STATE_OBSERVED` (zgodnie z ADR-RECOVERY-006 notą).
**Rozstrzygnięcie foundera (2026-08-17):** zatwierdzone zgodnie
z rekomendacją — cztery typy (`recovery_activated`, `recovery_deactivated`,
`recovery_refused`, `entity_frozen`) w jednej, osobnej zmianie ze schematem,
walidacją, mapowaniem, dokumentacją i testami. Historycznych zdarzeń nie
przepisujemy — stara historia jako `STATE_OBSERVED` pozostaje czytelna.
**Wdrożone 2026-08-17:** słownik 0.3.0 + enum schematu (nazwy w konwencji
UPPERCASE słownika), mapowanie w `_log` kernela, tabela mapowania
w `docs/recovery-contract.md`, addendum w ADR-RECOVERY-004, 7 nowych
testów (mapowanie, trwałość, zgodność słownik↔enum, czytelność historii).
Przy okazji wykryto rozjazd wzorca HOSId — zapisany jako DD-010.

## DD-004 · HYPOTHESIS vs AI_INFERENCE (RESOLVED 2026-08-17)
`EvidenceType` ma oba; ADR-SELFMODEL-001 przyjął konwencję
(HYPOTHESIS = interpretacje konwersacyjne czekające na potwierdzenie,
AI_INFERENCE = wnioski z danych). Czy docelowo scalić w jedną klasę
z polem `method`?
**Rekomendacja:** zostawić dwa (różne źródła epistemiczne), doprecyzować
w schemacie Layer 2 przy najbliższej rewizji.
**Tymczasowo:** konwencja z ADR-SELFMODEL-001 obowiązuje.
**Rozstrzygnięcie foundera (2026-08-17):** zachowujemy dwie osobne klasy
(HYPOTHESIS = interpretacja/możliwość oczekująca na potwierdzenie,
AI_INFERENCE = wniosek obliczony z danych). Nie scalać. Pole `method`
może później zostać dodane jako metadana sposobu powstania wniosku,
ale nie zastępuje różnicy epistemicznej.

## DD-005 · Relacja aplikacji demo do repo (RESOLVED 2026-08-17)
Aplikacja użytkownika (artefakt, single-file) implementuje wzorce silnika
po stronie klienta (self-model, bramy, recovery) jako demo produktowe.
Czy ma trafić do repo (np. `apps/user-demo/`) jako artefakt referencyjny
Human OS Lab (ADR-LAB), czy pozostać poza repo?
**Rekomendacja:** dodać do repo jako `apps/user-demo/` z README
o statusie „UX-only prototype" (spójnie z ADR-LAB-006 localStorage).
**Tymczasowo:** poza repo (punkt powrotu utrzymany).
**Rozstrzygnięcie foundera (2026-08-17):** włączyć do repo jako
`apps/user-demo/` — najpierw dokładna, niezmodyfikowana wersja obecnie
testowanego artefaktu jako punkt odniesienia. Oznaczenia obowiązkowe:
UX-ONLY PROTOTYPE, brak produkcyjnego backendu i uwierzytelniania, dane
syntetyczne domyślnie, localStorage ≠ trwały User Model, brak
automatycznej promocji do Core/Hub, żadnych prawdziwych danych
użytkownika w repo. README ma rozróżniać prototyp, konsolę Proof Kernel
w `app/` i silnik `hos_engine`.

## DD-007 · Parametry Emergency Root (RESOLVED 2026-08-17 — szkielet; parametry liczbowe nadal otwarte)
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
**Rozstrzygnięcie foundera (2026-08-17):** zatwierdzony szkielet:
deskryptor klucza awaryjnego, wersjonowana polityka (wymagany TTL,
deklaracja siły uwierzytelnienia, konfigurowalny schemat k-z-n, role
kustoszy, zakres, id i wersja konfiguracji), pełny audyt aktywacji,
odmowy, wykorzystania i wygaśnięcia. Bez wartości domyślnych (TTL,
uwierzytelnienie, schemat); brak konfiguracji blokuje mechanizm; wartości
testowe nie mogą trafić do konfiguracji produkcyjnej. Rzeczywisty magazyn
kluczy i kryptografia progowa — dopiero po osobnej decyzji i threat
modelu wdrożenia.

## DD-006 · Skale DI/IQ/AR i profil §18 (RESOLVED 2026-08-17 — szkielet; progi liczbowe nadal otwarte)
Layer 5 digest opisuje skale DI/IQ/AR i dziesięcioosiowy profil §18;
implementacja wymaga interpretacji progów, których źródło nie podaje
liczbowo. Wdrożyć z progami roboczymi (oznaczonymi PROVISIONAL), czy
czekać na doprecyzowanie założyciela?
**Rekomendacja:** wdrożyć szkielet typów bez progów liczbowych;
progi jako parametry konstruktora bez wartości domyślnych.
**Tymczasowo:** nie implementowane.
**Rozstrzygnięcie foundera (2026-08-17):** zatwierdzony szkielet typów
bez progów liczbowych i wartości domyślnych; progi wyłącznie przez jawną,
wersjonowaną konfigurację; brak konfiguracji => CONFIGURATION_REQUIRED,
abstencja albo bezpieczna odmowa — nigdy ciche przyjęcie progów; fixtures
testowe wyraźnie syntetyczne, nieprzedstawiane jako rekomendowane;
rozdzielenie struktury skali, wartości pomiaru i polityki interpretacji.
Konkretne progi liczbowe — osobna decyzja foundera po kalibracji
i walidacji.

## DD-008 · Model przeglądów bezpieczeństwa i kryterium zamknięcia 0.9 (RESOLVED 2026-08-17)
Decyzja z 2026-08-17 (pkt 5) zakładała przegląd etapu pierwszego przez
osobę lub zespół niezależny od autorów kodu i używanych agentów AI.
Tego samego dnia founder rozstrzygnął, że przeglądy będą wykonywane
własnymi siłami, i zatwierdził zmianę kryterium zamknięcia punktu 0.9.
**Rozstrzygnięcie foundera (2026-08-17):** kryterium zamknięcia 0.9
zmienione z „niezależny raport zewnętrzny" na: udokumentowany przegląd
bezpieczeństwa według powtarzalnego protokołu wewnętrznego (zakres
komponentów wg decyzji pkt 5), usunięcie problemów krytycznych
i wysokich, zapis ryzyk zaakceptowanych przez foundera oraz test
regresji zabezpieczeń. Świadomie zaakceptowana granica tej decyzji:
przegląd nie będzie niezależny od autorów kodu ani od agentów AI
uczestniczących w rozwoju — ta granica jest zapisana jako ryzyko
zaakceptowane, a powrót do przeglądu zewnętrznego pozostaje możliwy
w przyszłości bez zmiany protokołu.

## DD-009 · Zdarzenia `commons_*` w kanonicznym słowniku + fundament moderacji (OPEN)
Dyrektywa „Wspólnie" (ADR-COMMONS-001/002, digest
`docs/COMMONS_MODULE_DIGEST.md`) wymienia 16 zdarzeń współpracy
(challenge_created … moderation_case_resolved). Dodanie ich do
`event.types.json` + enum schematu to zmiana materialna; źródło samo wymaga
osobnego ADR, schematów i testów zgodności konstytucyjnej. Osobno:
ModerationCase nie ma precedensu w silniku (historia działań moderatora,
odwołania) i wymaga decyzji o minimalnym modelu ról moderacyjnych.
**Rekomendacja:** jedna zmiana wprowadzająca komplet 16 typów ze schematem
i mapowaniem na R0–R4 dla ryzyka wyzwań publicznych; ModerationCase jako
druga, osobna zmiana po decyzji o rolach.
**Tymczasowo:** demo aplikacji loguje te zdarzenia lokalnie w rejestrze
klienta; silnik nie emituje żadnych `commons_*`.

## DD-010 · Wzorzec HOSId w schemacie vs identyfikatory silnika (OPEN)
Wykryte 2026-08-17 podczas wdrażania DD-003, przez pierwszą próbę
walidacji trwałego zdarzenia Recovery pełnym `event.schema.json`:
kanoniczny wzorzec `HOSId` (`^HOS-[A-Z]{2,8}-[0-9]{6,}$`,
`schemas/common.schema.json`) dopuszcza wyłącznie cyfry w członie
numerycznym, podczas gdy silnik generuje identyfikatory szesnastkowe
(`uuid4().hex[:12].upper()` — np. `HOS-EMG-B47A501F7A30`) w co najmniej:
`recovery.py`, `execution_loop.py` (INT/PRF/REQ/EVT). Żaden runtime'owy
identyfikator nie przechodzi więc walidacji pełnej koperty. Dodatkowo
koperta z `sqlite_store` zawiera pola spoza schematu (`event_hash`,
`causation_id: None`).
**Opcje:** (a) rozszerzyć wzorzec `HOSId` o [0-9A-F] (zmiana materialna
kanonicznego schematu), (b) przestawić generatory silnika na cyfry
(zmiana formatu wszystkich nowych ID), (c) świadomie rozdzielić „ID
runtime" od „ID kanonicznych" (wymaga definicji mapowania).
**Rekomendacja:** (a) — wzorzec ma opisywać rzeczywistość silnika,
a rozszerzenie zbioru znaków nie unieważnia żadnego istniejącego ID.
**Tymczasowo:** testy DD-003 walidują zgodność `event_type` ze
słownikiem i enumem; pełna walidacja koperty czeka na tę decyzję.

