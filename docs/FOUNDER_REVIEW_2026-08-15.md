# Przegląd założycielski — 15 sierpnia 2026

Status: **Przyjęte**
Źródło: 13 pytań otwartych z sekcji 10 dokumentu *Human OS Reconstruction Audit*
(przygotowanego tego samego dnia na podstawie repozytorium, 77-plikowego
odzyskanego archiwum historycznego oraz tej rozmowy).

Ten dokument zapisuje rozstrzygnięcia founder-a dla każdego z 13 pytań, wraz
z pochodzeniem (numer pytania w audycie) i statusem wdrożenia. Zgodnie z
`Human_OS_Claude_Migration_Package/02_Source_Truth_Protocol`: żadna wcześniejsza
decyzja nie jest tu po cichu nadpisywana — tam, gdzie to rozstrzygnięcie zmienia
coś ustalonego wcześniej (np. kompresję Konstytucji do 15 zasad), stary stan
jest nazwany wprost jako zastąpiony, a nie usunięty z historii.

## Rozstrzygnięcia

### Q1 — Konstytucja: pełna maszyneria czy skrót
**Pytanie:** GitHub ma 15 zasad; źródłowy dokument v0.1 ma 21 rozdziałów i pełną
maszynerię (skale ryzyka R0–R4, antymetryki, rada konstytucyjna, rejestr
precedensów).
**Decyzja:** Pełna maszyneria z `Warstwa_1_Konstytucja_i_Wartości_v0.1` ma
docelowo trafić do wersji wiążącej. 15-punktowa wersja w `constitution/README.md`
przestaje być traktowana jako kompletna — jest punktem wyjścia do rozbudowy, nie
ostateczną formą.
**Status:** **Wykonane.** Zapytany wprost przy przeglądzie Fazy 3 (dyrektywa
zawiera jawną regułę eskalacji: „a constitutional rule would change”),
founder potwierdził rozpisanie pełnej wersji. `constitution/README.md`
zastąpiony rozszerzoną, 21-rozdziałową + 4-załącznikową strukturą, z jawną
notą o pochodzeniu (rekonstrukcja z audytu, nie dosłowny przedruk DOCX — do
zweryfikowania gdy oryginalne bajty będą dostępne) i mapowaniem poprzednich
15 punktów na nowe rozdziały, żeby nic nie zniknęło po cichu.

### Q2 — Kanoniczny Rozdział I White Paper
**Decyzja:** Rozdziałem I jest długa wersja „Dlaczego Human OS?” (PDF, 12 sekcji).
Krótki esej „Moment, w którym się znaleźliśmy” (Draft/v2 docx) traci status
kandydata na rozdział — jego dalsza rola (np. jako prolog) nie została ustalona.
**Status:** Przyjęte jako rozstrzygnięcie kanonu. Brak zmian w plikach White
Paper w tej sesji.

### Q3 — Rozdział III White Paper: pełna wersja zamiast skrótu
**Decyzja:** Główny plik Rozdziału III ma zostać zastąpiony pełną wersją
czterech części (A–D), zgodnie z własną zasadą projektu, że limit rozmiaru
dzieli dokument, a nie go kompresuje.
**Status:** Przyjęte jako rozstrzygnięcie. Fizyczna podmiana pliku nie wykonana
w tej sesji.

### Q4 — Human Atlas
**Decyzja:** Human Atlas to odrębny, wciąż niezbudowany filar — nie jest
tożsamy z Knowledge Graph.
**Status:** Przyjęte. Nazwa pozostaje zarezerwowana; brak specyfikacji poza
jednym akapitem w Manifeście v0.1.

### Q5 — Priorytet: HOS Hub
**Decyzja:** Budowa Hub (Entity Registry, Relation Registry, Location &
Representation Registry, Orchestrator, Event Ledger, Policy & Permission
Gateway) to bliski priorytet.
**Status:** Rozpoczęte w tej sesji — patrz `docs/adr/` i
`hos_engine/hub_entity_registry.py` (ścieżka poprawiona 2026-08-15, druga
tura — poprzedni zapis `hos_engine/hub/` był nieprawidłowy, taki katalog
nigdy nie istniał).

### Q6 — Kolejność budowy: HOS Core przed Decision Engine i Collective Intelligence
**Decyzja:** Z trzech w pełni opisanych, niezaimplementowanych komponentów
(HOS Core, Silnik Decyzji — Warstwa 5, Inteligencja Zbiorowa — Warstwa 7),
**HOS Core idzie pierwszy** — jako fundament wykonawczy, na którym mają stanąć
pozostałe.
**Status:** Rozpoczęte w tej sesji.

### Q7 — SAFE MODE: ważne, ale nie pierwsze
**Decyzja:** SAFE MODE i Sovereign Recovery Kernel pozostają ważne, ale mają
poczekać na fundamenty wykonawcze (Hub, HOS Core) z Q5/Q6.
**Status:** Świadomie odłożone. Nie blokuje Q5/Q6.

### Q8 — „Relation”: dwa modele, dwie nazwy
**Decyzja:** Zachowujemy oba modele relacji pod różnymi nazwami — ogólną,
typowaną krawędź grafu ze specyfikacji Hub oraz istniejący w repo model relacji
międzyludzkiej (`trust`/`reciprocity`/`boundaries`). Docelowe nazwy do ustalenia
przy implementacji Hub (np. `relation` vs `interpersonal_relation`).
**Status:** Przyjęte jako kierunek nazewniczy. Konkretne nazwy pól — do ADR-HUB
(patrz `docs/adr/`).

### Q9 — Słownik ról tożsamości: wygrywa specyfikacja
**Decyzja:** Ośmiorolowy model z `Identity, Authority & Permissions v0.1`
(OWNER, OPERATOR, TRUSTED_DELEGATE, RECOVERY_CUSTODIAN, AGENT, SERVICE, GUEST,
SYSTEM_PROCESS) zastępuje docelowo pięciotypowy `IdentityType` z
`hos_engine/security_identity.py` (HUMAN, AGENT, APPLICATION, SERVICE, HUB).
**Status:** Przyjęte jako kierunek. Migracja istniejącego kodu (`security_identity.py`)
na nowy słownik ról to osobna, przyszła zmiana — nie wykonana w tej sesji, żeby
nie naruszać działającego, przetestowanego modułu bez wcześniejszego zaplanowania
migracji danych/testów.

### Q10 — Interfejs: konsole i gra turowa równolegle
**Decyzja:** Rodzina konsol/dashboardów (Lab Console, Proof Kernel Console) i
zaproponowana przez founder-a gra turowa (postać = życie użytkownika, tury =
ścieżki rozwoju) rozwijane są równolegle, dla różnych odbiorców — konsole dla
operatora/testera, gra dla użytkownika końcowego.
**Status:** Przyjęte jako kierunek. Brak nowej pracy nad interfejsem w tej sesji
poza tym zapisem.

### Q11 — Import 14 ADR-ów
**Decyzja:** ADR-HUB-001…006 oraz ADR-CORE-001, ADR-GRAPH-002, ADR-AGENT-001/002,
ADR-WORLD-001, ADR-USER-002, ADR-PRED-001, ADR-AUDIT-001, ADR-IMPL-001
importowane do `docs/adr/` teraz, niezależnie od stanu implementacji.
**Status:** Wykonane w tej sesji — patrz `docs/adr/`.

### Q12 — Aktywne poszukiwanie brakujących dokumentów
**Decyzja:** Layer 2 („Model Człowieka”), Layer 4 („Model Użytkownika i Cyfrowy
Profil”), Layer 6 („Silnik Eksperymentów”), Sovereign Recovery Layer i Living
Canon mają być aktywnie poszukiwane, zanim uznamy je za utracone.
**Status:** Otwarte — wymaga dostępu founder-a do źródeł spoza tej sesji
(historia ChatGPT, File Library, inne kopie zapasowe). Nie do wykonania przez
samo repozytorium/to archiwum.

### Q13 — Licencja rozstrzygnięta
**Decyzja:** Robocza rekomendacja z `LICENSE-DECISION.md` przyjęta wprost:
Apache-2.0 dla kodu, CC BY 4.0 dla dokumentacji, polityka znaków — wciąż otwarta.
**Status:** Wykonane w tej sesji — patrz `LICENSE`, `LICENSE-DOCS`,
`LICENSE-DECISION.md`.

## Co z tego wynika dla dalszej pracy

Priorytet budowy w kolejności przyjętej powyżej: **HOS Core i Hub rozwijane
iteracyjnie/równolegle jako fundamenty wykonawcze → (SAFE MODE, Decision
Engine, Collective Intelligence — kolejność między nimi nierozstrzygnięta)**
(sformułowanie poprawione w drugiej turze, patrz korekta niżej). Q1–Q4, Q8–Q10
są rozstrzygnięciami kanonu/kierunku, których fizyczne wdrożenie (przepisanie
Konstytucji, podmiana rozdziałów White Paper, migracja słownika ról) pozostaje
do zaplanowania jako osobne zadania.

## Korekty — druga tura (15 sierpnia 2026, przegląd korygujący)

Źródło: `CLAUDE_COPY_PASTE_CONTINUATION_DIRECTIVE_2026-08-15.txt` z paczki
`Human_OS_100pct_Accounted_Handoff_2026-08-15` — szczegółowy przegląd korygujący
PR #5, przygotowany przez founder-a. Poniższe korekty używają jawnego formatu:
poprzedni stan / nowy dowód / skorygowany stan / wpływ — zgodnie z zasadą
`02_Source_Truth_Protocol`, że historia nigdy nie jest po cichu nadpisywana.

### KOREKTA — Q4 (Human Atlas)

**Poprzedni stan:** „Nazwa pozostaje zarezerwowana; brak specyfikacji poza
jednym akapitem w Manifeście v0.1” — zbyt redukcyjne.

**Nowy dowód:** dyrektywa korygująca wskazuje, że materiał źródłowy rozróżnia
co najmniej cztery odrębne Atlasy: **Atlas Człowieka** (Human), **Atlas
Cywilizacji**, **Atlas Inteligencji**, **Atlas Ewolucji** — koncepcyjnie
rozwinięte, choć nie sformalizowane jako kompletny, samodzielny komponent.

**Skorygowany stan:** Human Atlas = REALNY, ODRĘBNY, KONCEPCYJNIE ROZWINIĘTY,
JESZCZE NIE SFORMALIZOWANY JAKO KOMPLETNY SAMODZIELNY KOMPONENT, JESZCZE
NIEZBUDOWANY. Atlas nie definiuje człowieka — dostarcza map, z których człowiek
może świadomie korzystać do rozumienia siebie i świata. Knowledge Graph może
być infrastrukturą używaną przez Atlas; to ich nie utożsamia.

**Wpływ:** przed implementacją Atlas wymaga osobnego artefaktu
granicznego/specyfikacji i odzyskania pełnego materiału źródłowego. Brak zmian
w kodzie w tej turze.

### KOREKTA — Q9 (słownik ról tożsamości)

**Poprzedni stan:** „Ośmiorolowy model... zastępuje docelowo pięciotypowy
`IdentityType`” — przedwczesne stwierdzenie, że jeden słownik zastępuje drugi.

**Nowy dowód:** dyrektywa korygująca wskazuje, że to prawdopodobnie dwie różne
osie, nie jedno spektrum:
- **OŚ A — rodzaj podmiotu** (IdentityKind): `HUMAN, AGENT, APPLICATION,
  SERVICE, HUB` z `hos_engine/security_identity.py` — odpowiada na pytanie
  „czym technicznie jest ten podmiot?”.
- **OŚ B — rola autorytetu** (AuthorityRole): `OWNER, OPERATOR,
  TRUSTED_DELEGATE, RECOVERY_CUSTODIAN, AGENT, SERVICE, GUEST,
  SYSTEM_PROCESS` z `Identity, Authority & Permissions v0.1` — odpowiada na
  pytanie „jaki ma zakres władzy?”.

Podmiot typu `HUMAN` może pełnić rolę `OWNER` lub `OPERATOR`; `SERVICE` może
być zarówno rodzajem podmiotu, jak i osobno otrzymać rolę autorytetu — te dwie
osie nie są tym samym wymiarem.

**Skorygowany stan:** ośmiorolowy model jest kanoniczny dla semantyki
autorytetu/uprawnień, ale to NIE dowodzi, że `IdentityType` ma zniknąć. Przed
jakąkolwiek zmianą `security_identity.py` potrzebna jest osobna analiza:
(1) relacja IdentityKind ↔ AuthorityRole, (2) kardynalność, (3) reguły
przypisania, (4) czy jeden podmiot może mieć wiele ról jednocześnie,
(5) zakres i ważność czasowa roli, (6) zachowanie migracji istniejących
danych, (7) kompatybilność wsteczna, (8) testy.

**Wpływ:** `hos_engine/security_identity.py` pozostaje niezmieniony w tej
turze — poprzednia decyzja Q9 w sformułowaniu „zastępuje” była przedwczesna;
poprawiona na „dwie osie do formalnego uzgodnienia, nie proste zastąpienie”.

### KOREKTA — Q12 (poszukiwanie brakujących dokumentów)

**Poprzedni stan:** Layer 2, Layer 4, Layer 6, Sovereign Recovery Layer i
Living Canon wymienione jako „do aktywnego poszukiwania”, status nieznany.

**Nowy dowód:** paczka `Human_OS_100pct_Accounted_Handoff_2026-08-15`
potwierdza, że następujące dokumenty **istnieją** w File Library founder-a
(potwierdzone metadanymi, data ostatniej modyfikacji), ale ich surowe bajty
nie zostały wyeksportowane do żadnej z dostarczonych paczek:

| Dokument | Status |
|---|---|
| `Human_OS_Warstwa_2_Model_Czlowieka_v0_1.docx` | POTWIERDZONY w File Library, treść niedostępna |
| `Human_OS_Warstwa_4_Model_Uzytkownika_i_Cyfrowy_Profil_v0_1.docx` | POTWIERDZONY, treść niedostępna |
| `Human_OS_Warstwa_6_Silnik_Eksperymentow_Monitorowania_i_Postepu_v0_1.docx` | POTWIERDZONY, treść niedostępna |
| `Human_OS_Sovereign_Recovery_Layer_i_Rejestr_Scalenia_v0_2_1.docx` | POTWIERDZONY, treść niedostępna |
| `Human_OS_Formal_Entity_Relation_Model_v0_1.docx` | POTWIERDZONY, treść znana tylko pośrednio (cytaty w dyrektywie korygującej) — patrz `docs/RELATION_VOCABULARY_CROSSWALK.md` |
| `Human_OS_prezentacja_znajomi_v0_1.pptx` | POTWIERDZONY, treść niedostępna |

Dla przypomnienia, te dokumenty były już fizycznie dostępne (bajty obecne) i
wykorzystane wcześniej w audycie: `Warstwa_1`, `Warstwa_3`, `Warstwa_5`,
`Warstwa_7`, `Architektura v0.1`, `Rozszerzenie Architektury v0.2`,
`HOS Hub Model Entity-First`, `Identity, Authority & Permissions`,
`Lab Specyfikacja i Interface`, `Manifest v0.1`.

**Skorygowany stan:** powyższe sześć dokumentów to **FOUND** (potwierdzone
jako istniejące) — osobna kategoria od „wymaga poszukiwania od zera”. Nie są
zagubione; są zidentyfikowane i czekają na wgranie oryginalnych plików
binarnych do weryfikacji SHA-256.

Wciąż nierozwiązane jako w pełni formalne, samodzielne artefakty (patrz nowa
sekcja „Rejestr niezweryfikowanych artefaktów formalnych” niżej): specyfikacja
Living Canon, samodzielna specyfikacja Guardian, samodzielna specyfikacja
Forge, formalna specyfikacja Human Atlas, artefakt Natural Compatibility Layer
(NCL), pełne archiwum rozmów źródłowych, ostateczna polityka znaków
towarowych.

**Wpływ:** Q12 nie jest już „wymaga aktywnego poszukiwania od zera” — jest
„sześć dokumentów zidentyfikowanych i potwierdzonych, czeka na wgranie
oryginalnych plików binarnych”.

### KOREKTA — kolejność budowy Core/Hub (Q5/Q6)

**Poprzedni stan:** sformułowanie „Priorytet budowy: HOS Core → Hub” mogło
sugerować sekwencję „najpierw dokończ cały Core, potem zacznij Hub”.

**Nowy dowód:** decyzje founder-a ustalają, że Hub jest bliskim priorytetem, a
HOS Core musi poprzedzać Silnik Decyzji i Inteligencję Zbiorową — nie
ustalają, że Core musi być ukończony w całości przed rozpoczęciem Hub.

**Skorygowany stan:** HOS Core + Hub to natychmiastowe fundamenty wykonawcze,
rozwijane **iteracyjnie i równolegle** przez jawne kontrakty — nie
sekwencyjnie. Praca równoległa nad minimalnym wycinkiem Core i minimalnym
wycinkiem Hub (tak jak faktycznie wykonano w PR #5) jest zgodna z decyzją.
HOS Core musi jedynie poprzedzać wyższopoziomową rozbudowę Decision Engine i
Collective Intelligence — nie poprzedzać Hub.

**Wpływ:** brak zmian w kodzie; korekta dotyczy wyłącznie sformułowania w tym
dokumencie (patrz zaktualizowane podsumowanie na początku tej sekcji).

### Nowa pozycja — Natural Compatibility Layer (NCL): otwarty wątek historyczny

Historyczna dyskusja poruszała ideę zgodności Human OS ze zdrowymi, trwałymi,
regeneratywnymi wzorcami obserwowanymi w naturze — **nie** jako mechaniczne
naśladowanie natury, lecz jako test zgodności z zasadami: relacyjność,
przepływ, homeostaza, różnorodność, ewolucja, regeneracja, współzależność.
Robocza nazwa: **Natural Compatibility Layer (NCL)**. Towarzyszące pytanie
badawcze: czy Human OS mógłby być nie tylko produktem/platformą, ale też
językiem opisu rzeczywistości przez byty/relacje/wpływy/pola.

**Status: PROPONOWANE / HISTORYCZNE / WYMAGA PRZEGLĄDU FOUNDER-A.** Nie
implementować teraz. Nie odrzucać po cichu — ma pozostać w rejestrze otwartych
koncepcji (docelowo: Living Canon, gdy powstanie jako artefakt).

### Nowa pozycja — rejestr niezweryfikowanych artefaktów formalnych

- **Specyfikacja Living Canon** — nie znaleziona jako samodzielny dokument.
- **Samodzielna specyfikacja Guardian** — nie znaleziona. Guardian istnieje
  dziś jako rola governance w `GOVERNANCE.md` („Constitutional Guardian”,
  proces ludzki) i jako jednolinijkowy, porzucony placeholder `MOD-006` w
  manifeście Engine v0.2 (`docs/adr/ADR-HUB-001...` itd. go nie dotyczą) —
  żadne z nich nie jest pełną specyfikacją systemu bezpieczeństwa.
- **Samodzielna specyfikacja Forge** — nie znaleziona nigdzie w żadnym z
  dwóch odzyskanych archiwów.
- **Formalna, samodzielna specyfikacja Human Atlas** — nie znaleziona, patrz
  korekta Q4 wyżej.
- **Natural Compatibility Layer / NCL** — patrz wyżej, status
  proponowane/historyczne.
- **Pełne archiwum rozmów źródłowych** — nie znalezione; dostępny jest tylko
  `05_Selected_Historical_Conversations` — kuratorski digest, nie pełny
  eksport.
- **Ostateczna polityka znaków towarowych** — wciąż jawnie otwarta, patrz
  `LICENSE-DECISION.md`.

## Faza 3 — pierwsza zintegrowana pętla wykonania (15 sierpnia 2026)

Zgodnie z dyrektywą kontynuacyjną, sekcja 20: kolejny kamień milowy to nie
"więcej klas", tylko spójna, audytowalna ścieżka wykonania. Zbudowano:

- `hos_engine/authority.py` — `AuthorityRole`/`RoleGrantRegistry`, jako
  osobna, nowa oś (AXIS B) obok istniejącego `IdentityType` w
  `security_identity.py` (AXIS A) — zgodnie z korektą Q9 wyżej, bez
  dotykania tego drugiego modułu.
- `hos_engine/execution_loop.py` — `ExecutionLoop`, spinający realnie ze
  sobą: `IdentityRegistry` → `RoleGrantRegistry` → `ConsentRegistry` →
  `ContextManager` → `EntityRegistry` → `ProofKernel` → `AgentRuntime` →
  `EventEngine`/`EventStore`, z odmową jako pełnoprawnym wynikiem na każdej
  bramce (patrz `docs/adr/ADR-CORE-002-execution-loop-integration.md`).

To ograniczony, celowo wąski wycinek (nie dotyka jeszcze Knowledge Graph,
`RelationRegistry` Hub-a, ani łańcucha integralności `SQLiteEventStore`) —
ale pierwszy raz te elementy są przetestowane razem, a nie osobno. 16 nowych
testów (7 dla `authority.py`, 9 dla `execution_loop.py`), 62/62 w całym
repo, lint czysty, demo bez zmian.
