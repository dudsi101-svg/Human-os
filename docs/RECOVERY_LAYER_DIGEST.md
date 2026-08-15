# Digest: Human OS — Sovereign Recovery Layer i Rejestr Scalenia

**Status:** rozbiór strukturalny (nie parafraza) źródła dostarczonego przez founder-a
2026-08-15 — `Human_OS_Sovereign_Recovery_Layer_i_Rejestr_Scalenia_v0_2_1.docx` (uploadowany
w co najmniej trzech identycznych kopiach tego samego dnia). Patrz
`docs/FOUNDER_REVIEW_2026-08-15.md`, sekcja "Czwarta tura", po kontekst i listę
`ADR-RECOVERY-001..005` sformułowanych na podstawie tego rozbioru. Oryginalny plik DOCX
pozostaje jedynym rozstrzygającym źródłem w razie wątpliwości (`02_Source_Truth_Protocol`).

Źródło: ekstrakcja pandoc z DOCX (303/304 linie tekstu jawnego).

Uwaga metodologiczna: dokument jest krótki (14 ponumerowanych sekcji, 0–13) i ma charakter
**scaleniowy/decyzyjny** ("wynik porównania i decyzja o scaleniu"), a nie pełną specyfikację
techniczną. Wiele elementów jest zdefiniowanych na poziomie nazwy/zdania, bez pełnych kontraktów
danych (typów pól, wartości dopuszczalnych, JSON Schema, procedur krok-po-kroku). To jest
świadomie odnotowane w punktach 3 i 10 poniżej, a nie uzupełniane domysłem.

---

## 1. Metadane dokumentu / nagłówek

Z tabeli nagłówkowej (linie 1–28):

- **Tytuł:** HUMAN OS — SOVEREIGN RECOVERY LAYER (linie 1–2)
- **Podtytuł:** "Scalenie z architekturą v0.2, HOS Hub i Konstytucją" (linia 4)
- **Wersja:** 0.2.1 (linia 5)
- **Status:** "przyjęte do rdzenia" (linia 5) — czyli formalnie zaakceptowane jako część rdzenia
  Human OS, nie tylko projekt/draft
- **Data:** 21 lipca 2026 (linia 5)
- **Dokument nadrzędny:** "Konstytucja Human OS v0.1" (linia 8) — dokument jawnie podporządkowuje
  się Konstytucji
- **Dokumenty powiązane:** "Architektura Human OS v0.1; Rozszerzenie Architektury i Integracja
  v0.2; HOS Hub Entity-First v0.1" (linie 10–13)
- **Zakres:** "Suwerenne odzyskiwanie kontroli, tryby awaryjne, audyt, rollback, eksport i
  rejestr zmian" (linie 15–17)
- **Właściciel:** "Human OS — zespół założycielski" (linia 19)
- **Klasa zmiany:** "Istotna, bez zmiany misji; wzmacnia prawa użytkownika i odporność systemu"
  (linie 21–23)
- **Decyzja:** "Scalone bez konfliktów semantycznych; wymaga implementacji technicznej i testów"
  (linie 25–27) — czyli dokument sam stwierdza, że **jest jedynie decyzją normatywną/architektoniczną,
  a implementacja techniczna i testy dopiero mają nastąpić** (potwierdzone też w sekcji 12 i 13).

Sekcja 0 (linie 30–68) zawiera tabelę "wynik porównania": dokument deklaruje zgodność
("ZGODNE") z Konstytucją, HOS Core v0.2, HOS Hub, Human OS Lab, oraz stwierdza że rejestr wersji
był dotąd nieistniejący i zostaje "UZUPEŁNIONY" przez ten dokument (linie 64–67).

---

## 2. Nazwane mechanizmy / pojęcia

- **Sovereign Recovery Kernel** — nowy, chroniony komponent HOS Core, "poza zwykłym cyklem
  agentów" (linia 102–103). To jest formalna nazwa jądra realizującego prawa odzyskiwania
  kontroli. Umieszczony jako 9. (ostatni wymieniony) element zaktualizowanego składu HOS Core
  (linie 84–103).
- **SAFE MODE** — zdefiniowany operacyjnie jako: "Uruchomienie bez agentów, automatyzacji i
  zapisów zewnętrznych; dostęp do danych, konfiguracji, eksportu i odzyskiwania." (linie 125–126).
  To jest **jedyna definicja SAFE MODE w dokumencie** — jedno zdanie, brak dalszej rozbudowy
  (brak np. dokładnej listy zablokowanych operacji, brak sposobu wejścia/wyjścia z trybu, brak
  wskazania kto go uruchamia).
- **FREEZE** — "Natychmiastowe zatrzymanie procesów, kolejek i zmian; zapis punktu kontrolnego
  bez niszczenia danych." (linie 128–129).
- **READ-ONLY** — "Dozwolony odczyt i analiza; zakaz modyfikacji, publikacji, wysyłki, płatności
  i zmian w systemach zewnętrznych." (linie 131–132).
- **DISCONNECT** — "Odłączenie wybranych integracji bez utraty lokalnego śladu, metadanych i
  historii połączeń." (linie 134–135).
- **ROLLBACK** — "Powrót obiektu, modułu, konfiguracji lub systemu do wcześniejszego stanu przez
  utworzenie nowej wersji, bez kasowania historii." (linie 137–139) — istotne: rollback jest
  modelowany jako *nowa wersja*, nie jako destrukcyjne cofnięcie/nadpisanie.
- **EXPORT** — "Pełny eksport danych i grafu w otwartych formatach, bez blokady dostawcy." (linie
  141–142).
- **RECOVERY** — "Odtworzenie działania po awarii, utracie konta, uszkodzeniu danych, przejęciu
  urządzenia lub błędzie agenta." (linie 144–145).
- **Emergency Root** — specjalny mechanizm dostępu awaryjnego, opisany w sekcji 5 (linie 147–159)
  listą pięciu właściwości (patrz sekcja 4/8 poniżej). Nie jest to "konto" w sensie zwykłego
  konta administracyjnego — dokument explicite temu zaprzecza (linia 149).
- **Dwukluczowa suwerenność** (ang. dual-key sovereignty) — sekcja 6 (linie 161–167): działania
  krytyczne mogą wymagać klucza właściciela ORAZ niezależnego klucza odzyskiwania; klucz
  odzyskiwania może być offline lub podzielony progowo (np. schemat 2-z-3, secret sharing).
- **Minimalny zakres dostępu** — sekcja 7 (linie 169–173): zasada, że odzyskanie jednego obszaru
  (np. integracji Google Drive) nie odblokowuje innych obszarów (np. Gmaila, finansów, urządzeń,
  agentów biznesowych). To jest zasada izolacji zakresu (scope isolation), analogiczna do
  least-privilege, ale zastosowana do samego mechanizmu recovery.
- **Rejestr zdarzeń awaryjnych** — sekcja 8 (linie 175–218): kontrakt danych dla logowania każdego
  zdarzenia trybu awaryjnego (13 pól, patrz sekcja 4 digestu poniżej).
- **Kontrakty z HOS Hub** — sekcja 9 (linie 220–238): sześć nazwanych operacji/kontraktów, które
  Sovereign Recovery Kernel ma wywoływać na HOS Hub (patrz sekcja 4 digestu poniżej).
- **Rejestr scalenia i wersji** ("Merge Register") — sekcja 11 (linie 258–278): tabela czterech
  wpisów zmian (ID zmiany HOS-CHG-2026-0721-00{1..4}) dokumentujących samo to scalenie. To jest
  formalnie **to, co tytuł dokumentu nazywa "Rejestr Scalenia"** — ale w tej wersji dokumentu
  funkcjonuje on jako log samego aktu scalenia (4 wpisy dot. przyjęcia tego dokumentu), a NIE jako
  ogólny, żyjący rejestr wszystkich przyszłych scaleń/zmian w Human OS — sekcja 12 i 13 stwierdzają
  wprost, że taki "niezależny, trwały Rejestr Artefaktów i Wersji Human OS" dopiero ma powstać
  (linia 287).

**Nazwane role:** Dokument NIE definiuje nazwanej roli "Recovery Custodian" (opiekun/kustosz
odzyskiwania) — jedyne wymienione podmioty to: "Użytkownik / właściciel systemu" (hierarchia
kontroli, linia 107), generyczny "właściciel" (linia 78, linia 163), oraz podmioty którym prawa
są odmawiane: agent, administrator, dostawca infrastruktury, zewnętrzny system (linia 77),
agenci i automatyzacje (linia 151). Emergency Root jest opisany jako mechanizm/tryb dostępu, nie
jako rola przypisana konkretnej osobie/funkcji. **To jest istotna luka względem CLAUDE.md**, patrz
sekcja 10 poniżej — `authority.py` w repo już zawiera rolę `RECOVERY_CUSTODIAN` w enumie
`AuthorityRole`, a ten dokument źródłowy jej nie definiuje ani nie uzasadnia.

---

## 3. Decyzje architektoniczne w stylu ADR

**Brak.** Przeszukano cały plik pod kątem prefiksu "ADR-" — zero wystąpień. Dokument nie zawiera
żadnych numerowanych ADR-ów. Jedyna numeracja decyzyjna obecna w pliku to identyfikatory zmian w
formacie `HOS-CHG-2026-0721-0NN` w sekcji 11 (rejestr scalenia, linie 258–278) — to są wpisy
rejestru zmian/scalenia, nie ADR-y architektoniczne w formacie znanym z `docs/adr/` (nie mają
struktury Context/Decision/Consequences ani statusu Proposed/Accepted per-decyzja poza kolumną
"Decyzja" = "Przyjęto" dla wszystkich czterech).

---

## 4. Kluczowe encje / kontrakty danych (pola i znaczenie)

### 4.1 Rejestr zdarzeń awaryjnych (sekcja 8, linie 175–218)

Tabela ma dwie kolumny: "Pole" i "Wymóg". Dla WSZYSTKICH 13 pól wymóg jest identyczny:
"Obowiązkowe, wersjonowane i podpisane w śladzie audytowym" (mandatory, versioned, and signed in
the audit trail). Dokument **nie podaje** typów danych, formatów ani osobnych opisów semantyki
per pole — znaczenie poniżej jest odczytane wyłącznie z nazwy pola (nie jest to dosłowny cytat
z dokumentu, ponieważ dokument nie podaje definicji per-pole):

| Pole | Znaczenie (wywnioskowane z nazwy — dokument nie podaje osobnej definicji) |
|---|---|
| `event_id` | Unikalny identyfikator zdarzenia awaryjnego |
| `timestamp` | Znacznik czasu wystąpienia zdarzenia |
| `initiator` | Podmiot inicjujący tryb awaryjny |
| `recovery_mode` | Który z trybów (SAFE MODE / FREEZE / READ-ONLY / DISCONNECT / ROLLBACK / EXPORT / RECOVERY) został użyty |
| `reason` | Powód/uzasadnienie uruchomienia |
| `scope` | Zakres objęty działaniem (zgodnie z zasadą minimalnego zakresu, sekcja 7) |
| `systems_affected` | Systemy/integracje, których dotyczy zdarzenie |
| `actions_executed` | Lista wykonanych działań |
| `data_accessed` | Dane, do których uzyskano dostęp |
| `changes_created` | Zmiany/nowe wersje utworzone w wyniku działania |
| `expiration_time` | Czas wygaśnięcia dostępu/trybu |
| `verification_method` | Metoda weryfikacji/uwierzytelnienia inicjatora |
| `result` | Wynik/rezultat zdarzenia |

Wszystkie pola są opisane jako obowiązkowe (mandatory), wersjonowane (versioned) i podpisane
(signed) w ślad audytowy — czyli sam rejestr zdarzeń jest zaprojektowany jako niemodyfikowalny
log kryptograficznie podpisanych wpisów, spójny z ideą "nieusuwalnego śladu audytowego" z linii
157.

### 4.2 Kontrakty z HOS Hub (sekcja 9, linie 220–238)

Sześć nazwanych operacji (nie ma tu formalnych sygnatur pól wejścia/wyjścia — same nazwy i opisy
prozą):

| Kontrakt | Opis dosłowny z dokumentu |
|---|---|
| `Register Recovery Event` | "Rejestruje uruchomienie trybu, zakres, inicjatora i podstawę autoryzacji." |
| `Freeze Entity / Scope` | "Zmienia stan wskazanego bytu lub zakresu na SUSPENDED/FROZEN bez utraty historii." |
| `Create Recovery Snapshot` | "Tworzy kanoniczny punkt kontrolny z powiązaniami do wersji i reprezentacji." |
| `Rollback Entity / Workflow` | "Tworzy nową wersję opartą na wcześniejszym stanie i zapisuje łańcuch pochodzenia." |
| `Disconnect Representation` | "Odłącza lokalizację lub integrację, zachowując relację historyczną." |
| `Export Sovereign Package` | "Buduje przenośny pakiet danych, grafu, metadanych i rejestru zmian." |

Uwaga: `Freeze Entity / Scope` wprowadza stan `FROZEN`/`SUSPENDED` na bytach — sekcja 12 (linia
289) potwierdza, że status `FROZEN` jeszcze **nie istnieje** w schematach Entity/Event i ma
zostać dodany ("Dodać status FROZEN oraz zdarzenia recovery_* do schematów Entity/Event.").
To jest bezpośrednio istotne dla `hos_engine/state_machine.py::ALLOWED_TRANSITIONS`
(`draft, active, paused, completed, archived, revoked`) — `FROZEN`/`SUSPENDED` nie jest obecnie w
tej liście stanów (nie weryfikowałem tego pliku bezpośrednio w ramach tego zadania badawczego,
ale odnotowuję to jako punkt do sprawdzenia, bo CLAUDE.md opisuje dokładnie tę listę stanów).

### 4.3 Rejestr scalenia i wersji (sekcja 11, linie 258–278)

Kolumny tabeli: `ID zmiany`, `Data`, `Wersja`, `Typ`, `Zakres`, `Decyzja`, `Wpływ`. Cztery wiersze:

| ID zmiany | Data | Wersja | Typ | Zakres | Decyzja | Wpływ |
|---|---|---|---|---|---|---|
| HOS-CHG-2026-0721-001 | 2026-07-21 | 0.2.1 | Istotna | Dodanie Sovereign Recovery Kernel | Przyjęto | Wzmacnia autonomię i odporność |
| HOS-CHG-2026-0721-002 | 2026-07-21 | 0.2.1 | Operacyjna | Tryby SAFE/FREEZE/READ-ONLY/DISCONNECT/ROLLBACK/EXPORT/RECOVERY | Przyjęto | Nowe kontrakty wykonawcze |
| HOS-CHG-2026-0721-003 | 2026-07-21 | 0.2.1 | Architektoniczna | Połączenie Recovery z HOS Core, Hub, Event Ledger i Lab | Przyjęto | Bez zmiany numeracji Warstw 1–7 |
| HOS-CHG-2026-0721-004 | 2026-07-21 | 0.2.1 | Dokumentacyjna | Utworzenie kanonicznej sekcji rejestru zmian | Przyjęto | Usuwa lukę w zarządzaniu wersjami |

Uwaga: ten format ID (`HOS-CHG-YYYY-MMDD-NNN`) jest **inny** od obu ID-strategii opisanych w
CLAUDE.md (`HOS-<PREFIX>-######` licznikowe, oraz `uuid.uuid4().hex[:12].upper()`) — to jest
trzeci, jeszcze nieużywany w kodzie wzorzec ID, specyficzny dla wpisów rejestru zmian/scalenia.

---

## 5. Zasady bezpieczeństwa / eskalacji

**Hierarchia kontroli** (sekcja 3, linie 105–121) — ośmiopoziomowa, malejąca kolejność
pierwszeństwa:
1. Użytkownik / właściciel systemu
2. Konstytucja Human OS
3. Sovereign Recovery Kernel
4. HOS Core i polityki bezpieczeństwa
5. HOS Hub oraz rejestry
6. Agenci i automatyzacje
7. Integracje zewnętrzne
8. Interfejsy i reprezentacje

Kluczowe: **Sovereign Recovery Kernel stoi wyżej niż HOS Core, Hub, agenci i integracje** — czyli
w tej hierarchii Recovery ma pierwszeństwo egzekucyjne nad zwykłymi warstwami bezpieczeństwa i
politykami, ustępując tylko Konstytucji i samemu użytkownikowi/właścicielowi.

**Co wyzwala Recovery/tryby awaryjne:** Dokument nie podaje formalnej listy warunków-wyzwalaczy
(triggerów) w sensie automatycznych reguł ("jeśli X, to system wchodzi w SAFE MODE"). Zamiast
tego RECOVERY jest zdefiniowane przez listę *sytuacji*, po których ma służyć do odtworzenia
działania: "awaria, utrata konta, uszkodzenie danych, przejęcie urządzenia lub błąd agenta" (linia
144–145). Nie jest jasne, czy wejście w tryb jest zawsze inicjowane ręcznie przez
użytkownika/właściciela, czy może być też uruchamiane automatycznie przez system w reakcji na te
sytuacje — dokument tego nie rozstrzyga (patrz też sekcja 10 niżej).

**Kto może wyzwolić:** Explicite jedynie "initiator" jako pole rejestru zdarzeń (linia 186) i
"Użytkownik / właściciel systemu" najwyższy w hierarchii kontroli (linia 107). Sekcja 10 (test
obowiązkowy, linia 242) potwierdza zdolność użytkownika: "Użytkownik może zatrzymać wszystkie
aktywne agenty." Emergency Root (sekcja 5) wymaga "osobnego klucza odzyskiwania i silnego
uwierzytelnienia" (linia 153) — sugeruje mechanizm kryptograficzny, ale nie podaje dokładnej
procedury uwierzytelnienia.

**Co się dzieje:** Zależnie od trybu — patrz definicje w sekcji 2 digestu wyżej (SAFE MODE,
FREEZE, READ-ONLY, DISCONNECT, ROLLBACK, EXPORT, RECOVERY).

**Odwracalność / nieodwracalność — gwarancje explicite:**
- Rollback: "bez kasowania historii" (linia 139) i test: "Rollback odtwarza stan bez kasowania
  zdarzeń późniejszych." (linia 246) — silna gwarancja niedestrukcyjności rollbacku.
- Freeze: "zapis punktu kontrolnego bez niszczenia danych" (linia 129).
- Disconnect: "bez utraty lokalnego śladu, metadanych i historii połączeń" (linie 134–135) i test:
  "Odłączenie integracji nie usuwa historii ani pochodzenia danych." (linia 248).
- Sekcja 6 (dwukluczowa suwerenność) explicite mówi o ochronie "przed... nieodwracalnym działaniem
  wykonanym pod presją lub przez pomyłkę" (linie 165–167) — czyli drugi klucz jest pomyślany
  częściowo jako zabezpieczenie przed nieodwracalnością pod przymusem/błędem, nie tylko przed
  przejęciem konta.
- Sekcja 1 (zasada konstytucyjna): mechanizmy dostępu awaryjnego mają być "jawne, ograniczone,
  audytowalne, czasowe i odwracalne" (linie 72–74) — "odwracalne" jest tu explicite postawione
  jako cecha samego mechanizmu dostępu awaryjnego, nie tylko poszczególnych trybów.

**Rate-limiting / ochrona przed nadużyciem:**
- Emergency Root: "Dostęp jest ograniczony zakresem oraz czasem i automatycznie wygasa." (linia
  159) — czasowe wygaśnięcie, ale bez podania konkretnych wartości (np. TTL w minutach/godzinach).
- Minimalny zakres dostępu (sekcja 7): odzyskanie jednego obszaru nie odblokowuje innych — to jest
  mechanizm ograniczania "blast radius" pojedynczego zdarzenia recovery, a nie klasyczny
  rate-limiting (nie ma ograniczenia częstotliwości/liczby użyć w jednostce czasu).
- Dwukluczowa suwerenność (sekcja 6) — jest to głównie mechanizm anty-przejęcia/anty-przymusu, nie
  anty-spamowy.
- Nie znaleziono żadnego explicite określonego limitu liczby prób, cooldownu, ani polityki
  blokady po wielokrotnych nieudanych próbach uwierzytelnienia Emergency Root.

---

## 6. Terminologia (słownik)

Dokument nie ma osobnej, wydzielonej sekcji "Słownik"/"Definicje". Definicje pojęć są rozproszone
punktowo w treści sekcji 2 i 4–7. Zestawiam je poniżej term:definicja na podstawie literalnych
sformułowań z dokumentu:

- **Sovereign Recovery Kernel** : "komponent chroniony, poza zwykłym cyklem agentów" (linie
  102–103), 9. element składu HOS Core.
- **SAFE MODE** : "Uruchomienie bez agentów, automatyzacji i zapisów zewnętrznych; dostęp do
  danych, konfiguracji, eksportu i odzyskiwania." (linie 125–126)
- **FREEZE** : "Natychmiastowe zatrzymanie procesów, kolejek i zmian; zapis punktu kontrolnego
  bez niszczenia danych." (linie 128–129)
- **READ-ONLY** : "Dozwolony odczyt i analiza; zakaz modyfikacji, publikacji, wysyłki, płatności
  i zmian w systemach zewnętrznych." (linie 131–132)
- **DISCONNECT** : "Odłączenie wybranych integracji bez utraty lokalnego śladu, metadanych i
  historii połączeń." (linie 134–135)
- **ROLLBACK** : "Powrót obiektu, modułu, konfiguracji lub systemu do wcześniejszego stanu przez
  utworzenie nowej wersji, bez kasowania historii." (linie 137–139)
- **EXPORT** : "Pełny eksport danych i grafu w otwartych formatach, bez blokady dostawcy." (linie
  141–142)
- **RECOVERY** : "Odtworzenie działania po awarii, utracie konta, uszkodzeniu danych, przejęciu
  urządzenia lub błędzie agenta." (linie 144–145)
- **Emergency Root** : mechanizm o pięciu cechach (linie 149–159), patrz sekcja 8 digestu.
- **Dwukluczowa suwerenność** : nienazwany wprost jako pojedynczy termin poza tytułem sekcji 6, ale
  opisany jako wymóg klucza właściciela + niezależnego klucza odzyskiwania dla działań krytycznych
  (linie 163–167).
- **Minimalny zakres dostępu** : zasada, że "Uruchomienie procedury dla jednego obszaru nie
  odblokowuje pozostałych." (linia 171)

---

## 7. Powiązania / punkty integracji z innymi warstwami Human OS

Wszystkie poniższe to bezpośrednie cytaty z dokumentu:

- **Konstytucja Human OS** — dokument nadrzędny (linia 8). Sekcja 0 tabela: "Stan istniejący:
  Autonomia, kontrola danych, odwracalność, prawo do wyjścia i odwołania. Wpływ scalenia:
  Doprecyzowanie technicznych sposobów egzekwowania tych praw. Werdykt: ZGODNE" (linie 41–46). W
  hierarchii kontroli, Konstytucja stoi na pozycji 2, zaraz po użytkowniku/właścicielu, przed
  samym Sovereign Recovery Kernel (linie 107–111).
- **HOS Core v0.2** — sekcja 0: "Stan istniejący: Policy & Permission Engine, Workflow Engine,
  Audit, Event Engine. Wpływ scalenia: Dodanie Sovereign Recovery Kernel i nadrzędnych sygnałów
  awaryjnych. Werdykt: ZGODNE" (linie 47–51). Sekcja 2 podaje pełny, zaktualizowany skład HOS
  Core: "Event Engine, Context Manager, Memory Controller, Policy & Permission Engine, Workflow
  Engine, Scheduler, AI Orchestrator Runtime, Observability & Audit, Sovereign Recovery Kernel —
  komponent chroniony, poza zwykłym cyklem agentów" (linie 86–103).
- **HOS Hub** — sekcja 0: "Stan istniejący: Event Ledger, Policy Gateway, cykl życia bytów,
  wersjonowanie. Wpływ scalenia: Rejestracja zdarzeń awaryjnych, stanów zamrożenia i rollbacku.
  Werdykt: ZGODNE" (linie 53–57). Sekcja 9 definiuje sześć konkretnych kontraktów wywoływanych na
  Hub (patrz sekcja 4.2 digestu).
- **Human OS Lab** — sekcja 0: "Stan istniejący: Rollback, plan wycofania, środowisko izolowane.
  Wpływ scalenia: Dodanie testów awaryjnych i bramy promocji dla Recovery. Werdykt: ZGODNE" (linie
  59–62). Sekcja 10 podaje osiem konkretnych testów obowiązkowych "w Human OS Lab" (linie
  240–256).
- **Rejestr wersji** (ogólny, projektowy) — sekcja 0: "Stan istniejący: Zasady istnieją, brak
  osobnego kanonicznego pliku rejestru. Wpływ scalenia: Utworzenie sekcji rejestrowej w niniejszym
  dokumencie. Werdykt: UZUPEŁNIONE" (linie 64–67).
- **Warstwy 1–7** (numeracja warstw Human OS) — sekcja 0: "Nie tworzy konkurencyjnej warstwy
  domenowej i nie narusza numeracji Warstw 1–7. Zostaje włączona jako chroniony komponent HOS Core
  oraz mechanizm wykonawczy praw zapisanych w Konstytucji." (linie 32–36). Potwierdzone też w
  rejestrze scalenia: HOS-CHG-2026-0721-003, wpływ "Bez zmiany numeracji Warstw 1–7" (linie
  271–273).
- **hos_engine / kod** — dokument NIE wspomina żadnego konkretnego modułu Pythona (`hos_core.py`,
  `execution_loop.py`, `authority.py` itd.) po nazwie. Powiązanie z kodem repo jest więc
  interpretacyjne/pośrednie (np. "HOS Core" z dokumentu koresponduje koncepcyjnie z
  `hos_core.py` w repo, ale dokument tego nie stwierdza wprost) — to jest kolejny punkt
  niejednoznaczności, patrz sekcja 10.

---

## 8. Wszystkie explicite zakazy / reguły absolutne (cytaty dosłowne, z numerami linii)

To jest najbardziej safety-krytyczna część digestu. Poniżej WSZYSTKIE zdania o charakterze
zakazu, absolutnego wymogu, gwarancji lub niezmiennika, jakie znalazłem w dokumencie, w oryginalnym
brzmieniu polskim:

1. **(linie 72–75)** — "Human OS nie posiada ukrytych tylnych bramek. Posiada jawne, ograniczone,
   audytowalne, czasowe i odwracalne mechanizmy dostępu awaryjnego, których celem jest ochrona
   autonomii użytkownika, integralności danych i ciągłości działania systemu."
   *(Absolutne zaprzeczenie istnienia ukrytych backdoorów; pięć obowiązkowych cech każdego
   mechanizmu dostępu awaryjnego.)*

2. **(linie 77–78)** — "Żaden agent, administrator, dostawca infrastruktury ani zewnętrzny system
   nie może posiadać większych praw do Human OS niż jego właściciel."
   *(Absolutny zakaz — nikt i nic nie może mieć praw większych niż właściciel.)*

3. **(linie 79–80)** — "Mechanizm odzyskiwania nie może być zależny wyłącznie od pojedynczego
   modelu AI, pojedynczego dostawcy ani zwykłego interfejsu aplikacji."
   *(Zakaz architektonicznego single point of failure/single vendor lock-in dla mechanizmu
   recovery.)*

4. **(linie 131–132)** — "READ-ONLY — Dozwolony odczyt i analiza; zakaz modyfikacji, publikacji,
   wysyłki, płatności i zmian w systemach zewnętrznych."
   *(Explicite "zakaz" w definicji trybu READ-ONLY.)*

5. **(linia 149)** — "Nie jest kontem do codziennej administracji." *(dot. Emergency Root)*

6. **(linia 151)** — "Nie jest dostępny dla agentów ani automatyzacji." *(dot. Emergency Root —
   absolutne wykluczenie agentów/automatyzacji z dostępu do Emergency Root.)*

7. **(linia 153)** — "Wymaga osobnego klucza odzyskiwania i silnego uwierzytelnienia."

8. **(linia 155)** — "Uruchamia tylko zdefiniowane procedury awaryjne." *(ograniczenie zakresu
   działania Emergency Root wyłącznie do predefiniowanych procedur.)*

9. **(linia 157)** — "Każde użycie pozostawia nieusuwalny ślad audytowy." *("nieusuwalny" =
   niemodyfikowalna/trwała gwarancja audytu dla każdego użycia Emergency Root.)*

10. **(linia 159)** — "Dostęp jest ograniczony zakresem oraz czasem i automatycznie wygasa."

11. **(linia 171)** — "Uruchomienie procedury dla jednego obszaru nie odblokowuje pozostałych."

12. **(linie 242)** — "Użytkownik może zatrzymać wszystkie aktywne agenty." *(test obowiązkowy —
    gwarancja zdolności użytkownika do zatrzymania WSZYSTKICH agentów.)*

13. **(linia 244)** — "Tryb READ-ONLY blokuje rzeczywiste zapisy w systemach zewnętrznych."

14. **(linia 246)** — "Rollback odtwarza stan bez kasowania zdarzeń późniejszych."

15. **(linia 248)** — "Odłączenie integracji nie usuwa historii ani pochodzenia danych."

16. **(linia 250)** — "Awaria modelu AI nie blokuje ręcznego odzyskiwania." *(gwarancja, że
    recovery nie jest zależne od dostępności/sprawności modelu AI — krytyczne dla "stop the
    system" niezależnie od stanu AI.)*

17. **(linia 252)** — "Agent nie może zmienić polityki Recovery ani wyłączyć audytu." *(To jest
    prawdopodobnie NAJWAŻNIEJSZY pojedynczy zakaz w całym dokumencie z punktu widzenia
    bezpieczeństwa: absolutne, dwuczęściowe ograniczenie uprawnień agenta względem polityki
    Recovery i audytu.)*

18. **(linia 254)** — "Eksport pozostaje czytelny poza ekosystemem Human OS." *(gwarancja braku
    vendor/format lock-in dla wyeksportowanych danych — powiązane z prawem do wyjścia z
    Konstytucji.)*

19. **(linia 256)** — "Każde użycie Emergency Root jest wykrywalne i raportowane."

Uwaga: punkty 12–19 pochodzą z sekcji 10 "Testy obowiązkowe w Human OS Lab" — sformułowane są jako
kryteria testowe/asercje, a nie jako "MUSI"/"nie wolno" w typowej normatywnej frazeologii
Konstytucji, ale funkcjonalnie działają jako wiążące gwarancje/niezmienniki, które implementacja
ma spełniać, więc włączyłem je tutaj.

Nie znalazłem w dokumencie zwrotów "zabrania się" ani "zawsze musi" dosłownie — dokument
konsekwentnie używa "nie może", "nie jest", "zakaz", "nie" + czasownik, zamiast tych dokładnych
fraz.

---

## 9. Spis treści / struktura dokumentu

0. Wynik porównania i decyzja o scaleniu (linie 30–68)
1. Zasada konstytucyjna (linie 70–80)
2. Umiejscowienie w architekturze (linie 82–103)
3. Hierarchia kontroli (linie 105–121)
4. Tryby awaryjne (linie 123–145)
5. Emergency Root (linie 147–159)
6. Dwukluczowa suwerenność (linie 161–167)
7. Minimalny zakres dostępu (linie 169–173)
8. Rejestr zdarzeń awaryjnych (linie 175–218)
9. Kontrakty z HOS Hub (linie 220–238)
10. Testy obowiązkowe w Human OS Lab (linie 240–256)
11. Rejestr scalenia i wersji (linie 258–278)
12. Otwarte działania wdrożeniowe (linie 280–294)
13. Ograniczenie i status pewności (linie 296–303)

---

## 10. Niejednoznaczności, braki i potencjalne konflikty z CLAUDE.md / Konstytucją

Poniżej flagowane wprost, bez próby "cichego" rozstrzygnięcia:

1. **Brak roli "Recovery Custodian" w dokumencie źródłowym, mimo że istnieje w kodzie.** CLAUDE.md
   opisuje `authority.py::AuthorityRole` jako zawierające `RECOVERY_CUSTODIAN` jako jedną z ośmiu
   ról autorytetu. Ten dokument (recovery_a.txt) — który jest właśnie tym długo oczekiwanym
   źródłem dla Recovery/SAFE MODE — **nigdzie nie wspomina roli "Recovery Custodian"** ani nie
   definiuje kto ją pełni, jak jest powoływana, jakie ma uprawnienia względem Emergency Root czy
   dwukluczowej suwerenności. Kod repo zawiera więc pojęcie, którego uzasadnienia w tym źródle
   brakuje — to jest luka do wyjaśnienia, zanim `RECOVERY_CUSTODIAN` zostanie dalej rozwijany.

2. **Brak zgodności ról z Konstytucją, Rozdział 13.** Konstytucja (`constitution/README.md`,
   linie 227–230) wymienia siedem ról odpowiedzialności: Właściciel produktu, Rada
   konstytucyjna/etyczna, Zespół bezpieczeństwa, Zespół wiedzy, Zespół danych, Moderatorzy,
   Użytkownik. Żadna z tych ról nie jest wprost powiązana w recovery_a.txt z uprawnieniem do
   inicjowania Recovery/Emergency Root — dokument mówi ogólnie o "Użytkowniku / właścicielu
   systemu" (linia 107), co jest zgodne z rolą "Użytkownik"/"Właściciel produktu" z Konstytucji,
   ale nie precyzuje np. czy Zespół bezpieczeństwa może inicjować FREEZE w imieniu użytkownika w
   sytuacji awaryjnej, ani jaką rolę (jeśli jakąkolwiek) ma Rada konstytucyjna/etyczna względem
   Sovereign Recovery Kernel.

3. **Brak mapowania na skalę ryzyka R0–R4 z Konstytucji.** Konstytucja Rozdział 6 (linie 140–142)
   definiuje pięciopoziomową skalę ryzyka interwencji R0 (informacyjne) do R4 (niedopuszczalne bez
   wsparcia specjalisty). recovery_a.txt nigdzie nie klasyfikuje trybów awaryjnych (SAFE MODE,
   FREEZE, ROLLBACK itd.) względem tej skali, mimo że intuicyjnie np. ROLLBACK czy RECOVERY po
   "przejęciu urządzenia" wydają się kandydatami na wysokie R3/R4. To jest niedopatrzenie
   integracyjne — obie warstwy istnieją, ale się nie odwołują do siebie po nazwie mechanizmu.

4. **Brak mapowania na GEN-014 "Odwracalność" (genome.registry.json) ani żaden inny gen.**
   `genome.registry.json` zawiera 15 "genów konstytucyjnych" (GEN-001..015), z których GEN-014
   "Odwracalność" jest tematycznie najbliższy treści tego dokumentu (rollback, freeze, disconnect
   są zaprojektowane jako niedestrukcyjne). Dokument recovery_a.txt nie odwołuje się do numeracji
   genów w ogóle — zgodnie z CONTRIBUTING.md/PR template każda materialna zmiana ma deklarować
   powiązane geny; ten dokument (jako specyfikacja źródłowa, nie PR) nie musi formalnie tego robić,
   ale gdy zostanie przełożony na implementację, ta deklaracja będzie musiała powstać osobno.

5. **Niejasny mechanizm wyzwalania (triggering) trybów awaryjnych.** Jak odnotowano w sekcji 5
   digestu: dokument opisuje SAFE MODE/FREEZE/itd. przez to co *robią*, i przez to po jakich
   *sytuacjach* RECOVERY ma służyć (linie 144–145), ale nie mówi wprost, czy system może
   *automatycznie* wejść w te tryby (np. po wykryciu anomalii) bez inicjacji przez
   użytkownika/właściciela, czy wejście zawsze wymaga jawnej akcji człowieka. To jest fundamentalna
   niejasność dla implementacji "stop the system" — kto/co dokładnie ma prawo nacisnąć wyłącznik.

6. **Brak konkretnych wartości czasowych.** "Automatycznie wygasa" (linia 159) i "czasowe"
   mechanizmy (linia 73) nie mają podanych wartości TTL, okresów ważności klucza recovery, ani
   okna czasowego na potwierdzenie w schemacie dwukluczowym. Implementacja będzie musiała te
   wartości ustalić skądinąd — dokument tego nie rozstrzyga (i to samo w sobie jest zgodne z
   deklaracją sekcji 13, że to dopiero "punkt bazowy" do dalszej pracy).

7. **`FROZEN` / `SUSPENDED` jako nowy stan encji nie istnieje jeszcze w schematach.** Sekcja 12
   (linia 289) wprost mówi, że trzeba "Dodać status FROZEN oraz zdarzenia recovery_* do schematów
   Entity/Event" — czyli obecny `state_machine.py::ALLOWED_TRANSITIONS` (wg opisu w CLAUDE.md:
   `draft, active, paused, completed, archived, revoked`) **nie zawiera** stanu `FROZEN` ani
   `SUSPENDED`. `Freeze Entity / Scope` (sekcja 9, linia 225–226) explicite mówi o zmianie stanu na
   "SUSPENDED/FROZEN" — dokument używa obu tych słów niekonsekwentnie (raz "FROZEN" osobno w
   sekcji 12, raz "SUSPENDED/FROZEN" łącznie w sekcji 9) bez wyjaśnienia czy to synonimy, czy dwa
   różne stany. To jest wewnętrzna niejednoznaczność nazewnicza w samym dokumencie.

8. **Relacja do `hub_entity_registry.HubEntityStatus`.** CLAUDE.md opisuje istniejący
   `HubEntityStatus` w kodzie jako `PROPOSED, ACTIVE, SUSPENDED, SUPERSEDED, ARCHIVED` — czyli
   `SUSPENDED` **już istnieje** tam jako stan, ale `FROZEN` nie. recovery_a.txt (sekcja 9) mówi o
   "SUSPENDED/FROZEN" łącznie, co może sugerować, że autorzy dokumentu recovery zakładali, iż
   `SUSPENDED` z Hub Entity Registry i "FROZEN" z Recovery Layer to blisko powiązane/nakładające
   się pojęcia — ale to nie jest stwierdzone wprost, tylko interpretacja. Wymaga jawnego
   rozstrzygnięcia przy implementacji, nie zakładania.

9. **Rejestr scalenia (sekcja 11) jest wpisem samego siebie, nie ogólnym rejestrem.** Jak
   odnotowano w sekcji 2 digestu — tytuł dokumentu obiecuje "Rejestr Scalenia" jako coś ogólnego,
   ale w praktyce sekcja 11 zawiera tylko 4 wpisy dotyczące przyjęcia TEGO dokumentu. Sekcja 12
   (linia 287) mówi, że dopiero trzeba "Utworzyć niezależny, trwały Rejestr Artefaktów i Wersji
   Human OS" — czyli kanoniczny, żyjący rejestr nie istnieje jeszcze nigdzie, ten dokument jest
   jego zalążkiem/pierwszym wpisem, nie jego implementacją.

10. **Format ID `HOS-CHG-YYYY-MMDD-NNN` to trzeci wzorzec ID w projekcie**, nieopisany w CLAUDE.md
    (które zna tylko `HOS-<PREFIX>-######` licznikowy i `uuid.uuid4().hex[:12].upper()`) — warto
    to odnotować przy ewentualnym projektowaniu generatora ID dla rejestru zmian/scalenia.

11. **Brak jakiegokolwiek odniesienia do `hos_engine`, konkretnych plików Pythona, czy nazw modułów
    z repo.** Cały dokument jest napisany na poziomie architektoniczno-normatywnym (HOS Core, HOS
    Hub, Human OS Lab jako pojęcia), nie na poziomie implementacji. Mapowanie "HOS Core" z
    dokumentu → `hos_core.py` w repo, "HOS Hub" → `hub_entity_registry.py`/`hub/` w repo, "Human OS
    Lab" → (nie znaleziono odpowiednika w drzewie repo opisanym w CLAUDE.md — `Lab/Forge` jest
    wymieniony w CLAUDE.md jako część szerszej inicjatywy poza tym repo) jest interpretacyjne i
    NIE zostało zweryfikowane w kodzie w ramach tego zadania badawczego (zadanie było czysto
    tekstowe/badawcze na recovery_a.txt, bez dotykania repo). W szczególności nie jest jasne, czy
    "Human OS Lab" z tego dokumentu odpowiada czemukolwiek istniejącemu w tym repozytorium, czy
    jest częścią szerszej inicjatywy poza kodem (co CLAUDE.md explicite dopuszcza: "Lab/Forge"
    wymienione jako element inicjatywy poza repo).

12. **Zgodność z zasadą "malejącej niezbędności systemu" (GEN-012) i "prawa do wyjścia" —
    pozytywna, ale warta odnotowania.** EXPORT ("bez blokady dostawcy", linia 142) i test "Eksport
    pozostaje czytelny poza ekosystemem Human OS" (linia 254) wydają się dobrze wspierać
    GEN-012/GEN-002 (autorstwo życia, malejąca niezbędność) i konstytucyjne "prawo do wyjścia"
    (wspomniane w tabeli sekcji 0, linia 44) — to nie jest konflikt, ale odnotowuję jako pozytywne
    powiązanie, które warto zachować explicite przy przyszłej implementacji, żeby nie zgubić tego
    uzasadnienia.

13. **Status "przyjęte do rdzenia" a status całego repo "BETA".** Dokument deklaruje się jako
    "status: przyjęte do rdzenia" (linia 5), ale sam kodeks projektu (README/CLAUDE.md) stwierdza
    ogólny status repo jako BETA bez niezależnego przeglądu bezpieczeństwa. Sekcja 13 dokumentu
    (linie 296–303) sama zawiera zastrzeżenie: "Niniejszy dokument nie nadpisuje fizycznie
    wcześniejszych plików; stanowi formalne scalenie normatywne i architektoniczne oraz punkt
    bazowy do późniejszego ujednolicenia" — czyli mimo słowa "przyjęte", dokument sam siebie
    definiuje jako punkt wyjścia do dalszej pracy, nie jako gotową, wdrożoną specyfikację. Warto
    nie mylić statusu normatywnego "przyjęte do rdzenia" ze statusem "zaimplementowane i
    przetestowane" — sekcja 12 (Otwarte działania wdrożeniowe) i pole "Decyzja" w nagłówku
    ("wymaga implementacji technicznej i testów", linie 25–27) to potwierdzają.

---

## Podsumowanie (bardzo krótkie)

Dokument po raz pierwszy definiuje siedem nazwanych trybów awaryjnych (SAFE MODE, FREEZE,
READ-ONLY, DISCONNECT, ROLLBACK, EXPORT, RECOVERY), mechanizm Emergency Root, zasadę dwukluczowej
suwerenności i minimalnego zakresu dostępu, ośmiopoziomową hierarchię kontroli (z Sovereign
Recovery Kernel jako trzecim najwyższym ogniwem po użytkowniku i Konstytucji), kontrakt danych
rejestru zdarzeń awaryjnych (13 pól) oraz sześć kontraktów wykonawczych z HOS Hub. Krytyczne
gwarancje bezpieczeństwa to: brak ukrytych backdoorów, nikt nie ma praw większych niż właściciel,
recovery nie zależy od pojedynczego modelu AI/dostawcy, agent nie może zmieniać polityki Recovery
ani wyłączać audytu, oraz że rollback/freeze/disconnect są zaprojektowane jako niedestrukcyjne
(zachowują historię). Jednocześnie dokument jest wyraźnie na poziomie decyzji normatywnej/
architektonicznej, nie gotowej specyfikacji technicznej — nie zawiera ADR-ów, nie podaje typów
danych ani wartości progowych/czasowych, nie definiuje roli "Recovery Custodian" (mimo że istnieje
w kodzie repo), nie odwołuje się do skali ryzyka R0–R4 Konstytucji ani do numeracji genów, i sam
siebie opisuje jako "punkt bazowy do późniejszego ujednolicenia całego repozytorium" (linie
301–303), z listą sześciu wprost otwartych działań wdrożeniowych w sekcji 12.
