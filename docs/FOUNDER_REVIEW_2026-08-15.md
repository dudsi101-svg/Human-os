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
**Status:** **Wykonane** (15 sierpnia 2026, później tego samego dnia — patrz
kolejna korekta niżej i sekcja "Szósta tura"). Wersja główna oraz Części
A–D dostarczone i przetranskrybowane w całości do `docs/white_paper/`.

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

**Update, ta sama sesja (SQLite provenance + graf):** dodatkowe testy dla
`SQLiteEventStore` (łańcuch skrótów) i `RelationRegistry` (`REALIZUJE`)
podniosły łączną liczbę testów execution-loop do 14 (patrz
`ADR-CORE-002-execution-loop-integration.md`, sekcja Consequences,
zaktualizowana o oba wątki), a `CLAUDE.md` zostało przepisane, by opisywać
`hos_core`, `hub_entity_registry`, `authority`, `execution_loop`,
rozszerzoną Konstytucję i granicę EventEngine/EventStore. 67/67 testów,
lint czysty, demo bez zmian.

## Trzecia tura — nowe pliki źródłowe (15 sierpnia 2026, po południu)

Founder dostarczył pięć nowych oryginalnych plików (trzy `.docx`, dwa `.pdf`),
odzyskane niezależnie od dwóch wcześniejszych paczek archiwalnych. Zgodnie z
`02_Source_Truth_Protocol`, każdy plik jest tu odnotowany z jawnym statusem
przyjęcia, zamiast milcząco wchłonięty.

### Otrzymane pliki

| Plik | Dotyczy | Status po tej turze |
|---|---|---|
| `Human_OS_Lab_Specyfikacja_i_Interface_v0_1.docx` | Human OS Lab (środowisko testowe, osobne od symulacji w kodzie) | **NOWY** — brak wcześniejszej reprezentacji w repo. Dodano `docs/adr/ADR-LAB-001`…`006`. |
| `Human_OS_Rozszerzenie_Architektury_i_Integracja_v0_2_1.docx` | Źródło już wcześniej użyte pośrednio (audyt) do ADR-CORE-001, ADR-CORE-002 (częściowo), ADR-GRAPH-002, ADR-AGENT-001/002, ADR-WORLD-001, ADR-USER-002, ADR-PRED-001, ADR-AUDIT-001, ADR-IMPL-001, ADR-ARCH-002 | **ZWERYFIKOWANY** — treść tych 10 ADR-ów porównana zdanie po zdaniu z oryginalnymi bajtami. Rekonstrukcja pośrednia okazała się wierna źródłu; nie wymagała korekt merytorycznych. Każdy z tych ADR-ów ma teraz jawną notę "verified against the original source docx bytes 2026-08-15". Jedyna rozbieżność: nazwa pliku niesie sufiks `v0_2_1`, którego nagłówek dokumentu ("Wersja: 0.2") nie odzwierciedla — odnotowane, nierozstrzygnięte. |
| `Human_OS_Warstwa_6_Silnik_Eksperymentow_Monitorowania_i_Postepu_v0_1_2.docx` | Q12 — jeden z sześciu dokumentów wcześniej oznaczonych jako "POTWIERDZONY w File Library, treść niedostępna" | **TREŚĆ OTRZYMANA** (3585 linii po konwersji). Pełny rozbiór i wnioski architektoniczne — patrz kolejna aktualizacja tego dokumentu po zakończeniu analizy. |
| `Human_OS_White_Paper_Rozdzial_III_v1.0.pdf` | Q3 — kanoniczna wersja Rozdziału III | **CZĘŚCIOWO OTRZYMANE** — wersja główna (przeglądowa, sekcje 3.1–3.7). Dodano do `docs/white_paper/`. |
| `Human_OS_White_Paper_Rozdzial_III_Czesc_C_v1.0.pdf` | Q3 — Część C z czteroczęściowej wersji A–D | **CZĘŚCIOWO OTRZYMANE** — Część C (sekcje 3C.1–3C.7). Części A, B, D wciąż brakuje. Dodano do `docs/white_paper/`. |

### KOREKTA — Q3 (Rozdział III White Paper)

**Poprzedni stan:** "Fizyczna podmiana pliku nie wykonana w tej sesji" —
całkowity brak reprezentacji w repo.

**Nowy dowód:** dwa z czterech planowanych plików (wersja główna + Część C)
dostarczone jako PDF.

**Skorygowany stan:** `docs/white_paper/` zawiera teraz transkrypcję 1:1
wersji głównej i Części C. Części A, B, D pozostają nieotrzymane — status
rozdziału to **CZĘŚCIOWY**, nie kompletny. Nie zgadywano treści brakujących
części.

**Wpływ:** żaden — to czysto addytywna zmiana dokumentacyjna, brak wpływu na
kod ani testy.

### Aktualizacja Q12 (Warstwa 6)

Wiersz dla `Human_OS_Warstwa_6_Silnik_Eksperymentow_Monitorowania_i_Postepu_v0_1.docx`
w tabeli "Rejestr niezweryfikowanych artefaktów formalnych" (druga tura,
wyżej) zmienia status z "POTWIERDZONY w File Library, treść niedostępna" na
**"TREŚĆ OTRZYMANA I PRZEANALIZOWANA"**.

Dokument (3585 linii po konwersji z DOCX, wersja "0.1 – model bazowy",
jawnie oznaczony jako "Projekt do iteracji, pilotażu, walidacji
metodologicznej i audytu bezpieczeństwa") nie zawiera własnej numeracji ADR
— w przeciwieństwie do `Rozszerzenie Architektury i Integracja v0.2.1`, nie
było tu nic do wiernego wyodrębnienia, tylko materiał do sformułowania
nowych decyzji. Na tej podstawie dodano pięć nowych ADR-ów w tej turze:

- `ADR-EXP-001` — własna taksonomia ryzyka Warstwy 6 (XP0–XP8, SE0–SE4,
  EC/BL/MQ/PF/DQ/CA/PE, kody wyniku) i obowiązkowa "test nadrzędny" brama
  przed startem eksperymentu — jawnie **odrębna** od skali R0–R4 Konstytucji.
- `ADR-EXP-002` — zasada nierównoważności rzędów: bezpieczeństwo, jakość
  punktu odniesienia i zgoda nie są wzajemnie zastępowalne.
- `ADR-EXP-003` — obiekty eksperymentalne (15 typów) są niezależnie
  wersjonowane i nigdy nie scalane po cichu — ten sam wzorzec provenance co
  `EntityRegistry.merge()`.
- `ADR-EXP-004` — granice roli AI w Silniku Eksperymentów: lista zakazanych
  działań autonomicznych (§37.2) oraz bezwzględny zakaz automatycznego
  zwiększania ekspozycji na ścieżce wysokiego ryzyka (§34), niezależny od
  determinacji użytkownika.
- `ADR-EXP-005` — eksperymenty refleksyjne/symboliczne (Human Design,
  astrologia) za "zaporą epistemiczną": dopuszczalny przedmiot eksperymentu
  behawioralnego, ale nigdy podstawa wniosku medycznego/przyczynowego w
  Mapie Wiedzy.

Pełny, ustrukturyzowany rozbiór dokumentu (metadane, wszystkie skale,
15-obiektowa ontologia, 12 pól Załączników A–K, pełny spis treści 47 sekcji
+ Załączniki A–V, wszystkie dosłowne zakazy) zapisany trwale w
`docs/LAYER_6_EXPERIMENT_ENGINE_DIGEST.md` — ten wpis streszcza tylko
decyzje przełożone na ADR-y. Załącznik U źródła zawiera 12 nierozstrzygniętych
pytań metodologicznych/etycznych do wersji 0.2 — potencjalny materiał na
przyszłe ADR-y, nieuwzględniony w tej turze.

**Ważne rozróżnienie potwierdzone podczas analizy:** nazwy "Hub", "Digital
Twin", "Knowledge Graph" (używane w kodzie repozytorium) **nie występują** w
tym dokumencie — odnosi się on do "Mapy Wiedzy" (Warstwa 3). Nie zakładać
mapowania 1:1 na moduły kodu bez dalszej weryfikacji.

Wciąż w kategorii "POTWIERDZONY, treść niedostępna": Warstwa 2, Warstwa 4,
Sovereign Recovery Layer, prezentacja `znajomi`. `Formal_Entity_Relation_Model`
pozostaje w kategorii "treść znana tylko pośrednio".

## Czwarta tura — Sovereign Recovery, Warstwy 2/3/4/5 (15 sierpnia 2026, wieczór)

Founder dostarczył jedenaście kolejnych plików w dwóch turach uploadu: pierwsza
zawierała `Sovereign_Recovery_Layer_v0_2_1` (dwie identyczne kopie),
`Warstwa_5_Silnik_Decyzji`, `Warstwa_6` (duplikat już przetworzonego),
`Warstwa_3_Mapa_Wiedzy`, `Warstwa_2_Model_Czlowieka`; druga zawierała pięć
kolejnych plików, z czego cztery okazały się **bajt-w-bajt identycznymi
duplikatami** plików z pierwszej tury (zweryfikowane `diff`), a jeden —
`Warstwa_4_Model_Uzytkownika_i_Cyfrowy_Profil` — był genuinie nowy. Łącznie
**pięć unikalnych nowych dokumentów źródłowych** zostało w pełni przeanalizowanych
(każdy przeczytany od początku do końca przez dedykowanego agenta badawczego,
zweryfikowany dodatkowymi wyszukiwaniami `grep` po całym pliku) i przełożonych
na 25 nowych ADR-ów. Wszystkie pięć pełnych rozbiorów zapisano trwale w `docs/`:

| Dokument | Digest | Nowe ADR-y | Status w Q12 po tej turze |
|---|---|---|---|
| Sovereign Recovery Layer v0.2.1 | `docs/RECOVERY_LAYER_DIGEST.md` | `ADR-RECOVERY-001..005` | **TREŚĆ OTRZYMANA I PRZEANALIZOWANA** — było jedynym dokumentem blokującym SAFE MODE |
| Warstwa 5 — Silnik Decyzji i Rekomendacji | `docs/LAYER_5_DECISION_ENGINE_DIGEST.md` | `ADR-DECISION-001..005` | nowy — nie był w rejestrze Q12 |
| Warstwa 3 — Mapa Wiedzy i Sygnatura Informacji | `docs/LAYER_3_KNOWLEDGE_MAP_DIGEST.md` | `ADR-KNOWLEDGE-001..005` | nowy — nie był w rejestrze Q12 |
| Warstwa 2 — Model Człowieka | `docs/LAYER_2_HUMAN_MODEL_DIGEST.md` | `ADR-HUMAN-001..005` | **TREŚĆ OTRZYMANA I PRZEANALIZOWANA** |
| Warstwa 4 — Model Użytkownika i Cyfrowy Profil | `docs/LAYER_4_USER_MODEL_DIGEST.md` | `ADR-USERMODEL-001..005` | **TREŚĆ OTRZYMANA I PRZEANALIZOWANA** |

Po tej turze, z sześciu dokumentów wymienionych w drugiej turze jako
"POTWIERDZONY, treść niedostępna", pozostają nieotrzymane tylko:
`Sovereign_Recovery` (teraz otrzymany, usunięty z listy), `Warstwa_2` (teraz
otrzymany), `Warstwa_4` (teraz otrzymany) — **wszystkie trzy zamknięte**.
`Human_OS_prezentacja_znajomi_v0_1.pptx` — founder zdecydował, że ten plik
**nie jest potrzebny**; zdjęty z listy poszukiwań, nie jako utracony, tylko
jako świadomie odrzucony (decyzja z 15 sierpnia 2026, ta sama sesja). Wciąż
nieotrzymane: pełne archiwum rozmów źródłowych. `Formal_Entity_Relation_Model`
pozostaje "treść znana tylko pośrednio".

### Najważniejsze ustalenie — Sovereign Recovery / SAFE MODE (odblokowane, ale niekompletne)

Dokument źródłowy dla SAFE MODE **wreszcie istnieje w projekcie**, ale sam
siebie definiuje jako decyzję normatywną/architektoniczną, nie gotową
specyfikację techniczną (własny nagłówek: "Scalone bez konfliktów
semantycznych; wymaga implementacji technicznej i testów"). Zdefiniowano
siedem trybów awaryjnych (SAFE MODE, FREEZE, READ-ONLY, DISCONNECT, ROLLBACK,
EXPORT, RECOVERY), ośmiopoziomową hierarchię kontroli (Sovereign Recovery
Kernel jako 3. najwyższe ogniwo po użytkowniku i Konstytucji), Emergency Root,
dwukluczową suwerenność i 13-polowy kontrakt rejestru zdarzeń awaryjnych —
pełne szczegóły w `ADR-RECOVERY-001..004`.

**Zgodnie z własnym protokołem tej sesji (nie zgadywać architektury
bezpieczeństwa), `ADR-RECOVERY-005` jawnie wypisuje dziewięć nierozstrzygniętych
luk zamiast je wypełniać domysłem** — najważniejsze cztery, blokujące spójną
implementację: (1) rola `RECOVERY_CUSTODIAN`, która już istnieje w
`authority.py`, nie jest nigdzie w tym dokumencie zdefiniowana ani uzasadniona;
(2) brak mapowania trybów awaryjnych na skalę R0–R4 Konstytucji; (3) nie
rozstrzygnięto, czy tryby awaryjne mogą włączać się automatycznie, czy zawsze
wymagają jawnej akcji człowieka; (4) niejednoznaczność nazewnicza `FROZEN` vs
`SUSPENDED` między sekcjami samego dokumentu. **Rekomendacja: żaden kod
SAFE MODE/Recovery nie powinien powstać, dopóki te cztery punkty nie zostaną
rozstrzygnięte z founder-em** — to nie jest decyzja podjęta jednostronnie w tej
turze, tylko wniosek z analizy zgodny z regułą eskalacji tej sesji.

### Drugie ważne ustalenie — Warstwa 4 to NIE źródło ADR-USER-002

Podczas analizy Warstwy 4 potwierdzono (pełne porównanie w
`docs/LAYER_4_USER_MODEL_DIGEST.md` §9 i `ADR-USERMODEL-005`), że **to nie jest
ten sam dokument**, który był źródłem istniejącego `ADR-USER-002` ("Human
Digital Twin"). `ADR-USER-002` cytuje `Rozszerzenie_Architektury_i_Integracja_v0_2_1.docx`
jako źródło — inny plik. Warstwa 4 nigdzie nie używa terminu "Cyfrowy
bliźniak"/"Digital Twin"; ma inną dekompozycję architektoniczną (R0–R8 +
24-obiektowa płaska ontologia, zamiast dziewięciu nazwanych komponentów i
pięciu trybów działania z ADR-USER-002). Oba dokumenty dzielą fundamentalną
filozofię ("model to mapa, nie definicja") i prawa
weryfikacji/kontestacji/korekty/usunięcia, ale **nie powinny być po cichu
utożsamiane ani scalane** — zgodnie z `02_Source_Truth_Protocol`, to zostaje
tu odnotowane jako otwarte pytanie governance, nie rozstrzygnięte
jednostronnie. `ADR-USERMODEL-001..004` opisują wyłącznie treść Warstwy 4;
`ADR-USER-002` pozostaje niezmieniony.

### Pozostałe ustalenia warte odnotowania

- **Pięć niezależnych, nienakładających się taksonomii ryzyka/jakości** istnieje
  teraz w projekcie: Konstytucja R0–R4, Warstwa 6 (XP/SE/EC/BL/MQ/PF/DQ/CA/PE),
  Warstwa 5 (DI/IQ/AR/RV/RC/G/R-poziom), Warstwa 3 (sygnatura 0–5/E0–E5/K1–K4/
  klasy źródeł), Warstwa 4 (R0–R8/H0–H5/P0–P5/C0–C5/D0–D4). Żadna nie pokrywa
  się znaczeniowo z pozostałymi mimo współdzielonych liter — to zamierzony
  wzorzec "różne osie na różnych warstwach" (patrz `CLAUDE.md`,
  `AuthorityRole` vs `IdentityType`), ale warty jawnego, zbiorczego
  odnotowania, żeby żadna przyszła sesja nie założyła fałszywej ekwiwalencji.
- **"Zapora epistemiczna" wobec systemów symbolicznych (Human Design,
  astrologia) występuje niezależnie w Warstwach 2, 3, 5, 6 i 4** — z niemal
  identycznym sformułowaniem za każdym razem. To silny dowód na rzeczywisty,
  ogólnoprojektowy niezmiennik, nie przypadkową zbieżność (patrz
  `ADR-KNOWLEDGE-005`, gdzie odnotowano to pierwszy raz zbiorczo).
- **Rozbieżność liczby pól "sygnatury wiedzy"** między `constitution/README.md`
  (7 pól) a Warstwą 3 (11 wymiarów w pełnej tabeli, ale inny 7-elementowy
  podzbiór w jej własnym kryterium akceptacji 29.3) — konkretny, sprawdzalny
  punkt do rozstrzygnięcia przez founder-a, nieopisany dalej w tej turze
  (patrz `ADR-KNOWLEDGE-001`).
- Wszystkie pięć nowych dokumentów źródłowych jawnie deklaruje status "Wersja
  0.1/0.2.1 – model bazowy/przyjęte do rdzenia", "Projekt do iteracji,
  walidacji i audytu" — deklaratywnie niedojrzałe, spójne z BETA repozytorium
  kodu. Każdy ma własny załącznik "Otwarte pytania do wersji 0.2"
  (10–14 pytań) — potencjalny materiał na przyszłe ADR-y, nieuwzględniony w
  tej turze.

**Wpływ na kod:** żaden. Ta tura jest wyłącznie dokumentacyjna — 25 nowych
plików ADR + 5 plików digest + rozszerzenie tego dokumentu. Zgodnie z zasadą
tej sesji ("Reconstruction Audit" najpierw, implementacja dopiero po
rozstrzygnięciu otwartych pytań), żaden z nowo udokumentowanych komponentów
(Sovereign Recovery Kernel, Silnik Decyzji, rozszerzona Mapa Wiedzy, Model
Człowieka, Model Użytkownika R0–R8) nie został zaimplementowany w
`hos_engine` w tej turze.

## Piąta tura — decyzje po głębokim audycie (15 sierpnia 2026)

Po scaleniu PR #2 (zamknięty jako zastąpiony), PR #4 i PR #5 do `main`,
wykonano głęboki audyt stanu projektu (60 ADR-ów, 9 z nich zaimplementowanych,
2281 linii kodu, zero pracy z tego dnia dotąd scalonej — patrz opublikowany
artefakt audytu). Audyt wskazał pięć pytań wymagających decyzji founder-a.
Zamiast zostawiać je dalej otwarte, zadano je wprost — odpowiedzi poniżej,
w formacie zgodnym z resztą tego dokumentu.

### Decyzja — Sovereign Recovery / SAFE MODE (cztery luki z ADR-RECOVERY-005)

1. **Rola `RECOVERY_CUSTODIAN`** → zdefiniowana teraz na bazie ról
   governance z Konstytucji, nie czekamy na dodatkowe źródło. Zmapowana na
   **Zespół bezpieczeństwa** (Konstytucja, rozdz. 13) — nigdy na `OWNER`,
   bo drugi klucz w schemacie dwukluczowym istnieje właśnie po to, by
   chronić przed nieodwracalnym działaniem samego właściciela pod presją
   lub przez pomyłkę. Zapisane w `hos_engine/authority.py` (komentarz przy
   `RECOVERY_CUSTODIAN`) i `ADR-RECOVERY-006`.
2. **Mapowanie trybów awaryjnych na R0–R4** → każdy tryb osobno, nie jedna
   wspólna wartość. Zaproponowane i przyjęte mapowanie: SAFE MODE/READ-ONLY
   = R0, FREEZE/DISCONNECT/EXPORT = R1, ROLLBACK = R2, RECOVERY = R3. Żaden
   tryb nie sięga R4 — wszystkie są usankcjonowanymi mechanizmami, nie
   niedopuszczalnymi działaniami. Pełne uzasadnienie w `ADR-RECOVERY-006`.
3. **Automatyczne czy ręczne wyzwalanie** → zależnie od trybu. SAFE MODE,
   READ-ONLY, FREEZE i DISCONNECT mogą włączać się automatycznie po
   wykryciu poważnej anomalii (z natychmiastowym powiadomieniem właściciela
   i bezwarunkowym prawem cofnięcia); ROLLBACK, EXPORT i RECOVERY zawsze
   wymagają jawnej akcji człowieka.
4. **`FROZEN` vs `SUSPENDED`** → to ten sam stan. Kontrakt „Freeze Entity /
   Scope” z Recovery używa istniejącego `HubEntityStatus.SUSPENDED` —
   żaden nowy stan encji nie jest dodawany do `state_machine.py` ani
   `hub_entity_registry.py`.

Wszystkie cztery decyzje zapisane szczegółowo w `ADR-RECOVERY-006` — nie
implementują same w sobie kodu SAFE MODE, ale usuwają blokery, które
wcześniej uniemożliwiały rozpoczęcie tej implementacji. Pozostałe punkty z
`ADR-RECOVERY-005` (2, 4, 6, 8, 9) pozostają otwarte, nieporuszone w tej
turze.

### Decyzja — Warstwa 4 i ADR-USER-002

**Scalone.** Warstwa 4 (R0–R8, 24-obiektowa ontologia) staje się kanoniczną
strukturą; dziewięć nazwanych komponentów z ADR-USER-002 i pięć trybów
działania zostają zachowane jako nazwane widoki nad tą strukturą, nie
osobny schemat. Rozstrzygnięto oba wcześniej niezmapowane komponenty
(Capability Model, Decision Style) i zaproponowano mapowanie pięciu trybów
na wiersze R0–R8. „Cyfrowy bliźniak”/„Human Digital Twin” przestaje być
nazwą główną modelu — kanoniczna nazwa to „Model Użytkownika i Cyfrowy
Profil Rozwojowy”. Pełny zapis: `ADR-USERMODEL-006`; `ADR-USER-002` pozostaje
nienaruszony jako zapis historyczny, ze zaktualizowanym statusem wskazującym
na scalenie.

### Decyzja — Sygnatura wiedzy (7 pól czy 11 wymiarów)

**Oba obowiązują, w różnych rolach.** 7 pól z Konstytucji to twarda,
wszędzie obowiązująca podłoga; 11 wymiarów z Warstwy 3 to pełna, zalecana
forma stosowana tam, gdzie to możliwe. `constitution/README.md` rozdz. 5
zaktualizowany, żeby to stwierdzić wprost. `ADR-KNOWLEDGE-001` zaktualizowany
o notę rozstrzygającą. Wewnętrzna niespójność w samej Warstwie 3 (jej
kryterium akceptacji 29.3 wymienia jeszcze inny, trzeci 7-elementowy
podzbiór) pozostaje nierozwiązana — to osobna usterka redakcyjna źródła, nie
objęta tą decyzją.

### Decyzja — polityka znaków towarowych

**Ustalona teraz, robocza.** Nazwa i znaki „Human OS” identyfikują
oficjalny projekt; licencje Apache-2.0/CC BY 4.0 nie obejmują nazwy/marki
(zgodnie z klauzulą 6 Apache-2.0). Forki dozwolone, ale nie mogą przedstawiać
się jako „Human OS” bez zgody founder-a; opisowe odniesienia („zgodny z
Human OS”) pozostają dozwolone. Jawnie oznaczona jako polityka robocza, nie
formalna opinia prawna — pełna analiza prawna nazwy/marki wciąż otwarta.
Pełny zapis: `LICENSE-DECISION.md`.

### Decyzja — priorytet brakujących części White Paper

**Niski priorytet.** Części A i B Rozdziału III pozostają oczekiwane, ale
bez pośpiechu — nie blokują żadnej pracy nad kodem, ADR-ami ani Konstytucją.
Brak zmian w `docs/white_paper/`.

**Wpływ na kod:** `hos_engine/authority.py` — jeden komentarz dokumentujący
mapowanie `RECOVERY_CUSTODIAN`. Żadna inna zmiana kodu. Reszta tej tury to
wyłącznie ADR-y, Konstytucja i `LICENSE-DECISION.md`.

## Szósta tura — Rozdział III White Paper kompletny (15 sierpnia 2026)

Tego samego dnia, wkrótce po "Piątej turze" (gdzie priorytet uzupełnienia
Części A i B ustalono jako niski), founder dostarczył wszystkie trzy
brakujące pliki naraz: Część A, Część B i Część D (Część C przesłana
ponownie — potwierdzona jako bajt-identyczna z już posiadaną wersją, patrz
`diff`).

### KOREKTA — Q3 (Rozdział III White Paper), druga korekta

**Poprzedni stan (druga tura):** "CZĘŚCIOWY — wersja główna i Część C
dostarczone; Części A, B, D nieotrzymane."

**Nowy dowód:** Części A, B, D dostarczone jako PDF 15 sierpnia 2026, po
południu (ta sama sesja, po zamknięciu Piątej tury).

**Skorygowany stan:** Rozdział III jest **KOMPLETNY**. `docs/white_paper/`
zawiera teraz wszystkie pięć segmentów (wersja główna + A + B + C + D) jako
osobne pliki 1:1 transkrypcji, plus jeden plik złączony
(`rozdzial-III-pelny.md`) dla wygody lektury ciągłej — założyciel wybrał tę
opcję wprost (osobne pliki jako źródło prawdy + dodatkowy plik złączony,
zamiast tylko jednego lub tylko drugiego).

**Wpływ:** żaden na kod — zmiana wyłącznie w `docs/white_paper/` i tym
dokumencie. Zgodnie z decyzją założyciela z tej samej tury pytań, zmiana
scalona bezpośrednio do `main` bez osobnej rundy przeglądu (transkrypcja
1:1, bez interpretacji).

## Siódma tura — Faza 3: pierwsze moduły domenowe (15 sierpnia 2026)

Founder zatwierdził samodzielne przejście przez Fazę 3 planu z audytu
("Tak śmiało samodzielnie możesz przejść przez fazę 3"). Zrealizowano trzy
ograniczone, w pełni przetestowane wycinki — wszystkie zgodnie z wcześniej
przyjętymi ADR-ami, bez nowych decyzji projektowych:

1. **Silnik Decyzji — pierwszy MVP** (`hos_engine/decision_engine.py`,
   21 testów): dziewięć bram twardych G0–G8 przed jakimkolwiek rankingiem,
   klasy reakcji R-NISKIE..R-KRYTYCZNE, zasada asymetrii dowodowej
   (deklarowany poziom dowodów 0–5 vs. klasa ryzyka; R-KRYTYCZNE nigdy
   niedopuszczalne), abstencja z ośmioma nazwanymi powodami i eskalacja
   miękka/warunkowa/twarda jako pełnoprawne wyniki, nieprzemienne
   wykluczenia (ranking nie wskrzesza kandydata odrzuconego przez bramę).
   Dwa niezmienniki z ADR-DECISION-005 wymuszone kodem i testem:
   determinacja użytkownika nie zmienia żadnego wyniku, sponsorowanie nie
   wpływa na ranking. Jak Proof Kernel — silnik ocenia deklarowane wejścia.
2. **Typowany słownik Mapy Wiedzy** (`knowledge_graph.py`):
   `KnowledgeNodeType` (13 typów) i `KnowledgeRelationType` (9 relacji) z
   ADR-KNOWLEDGE-003, plus opcjonalne
   `KnowledgeGraph.validate_against_catalog()` — raportuje odstępstwa jako
   `CatalogViolation`, nigdy nie rzuca wyjątku ani nie poprawia po cichu;
   istniejące nietypowane grafy działają bez zmian.
3. **Brakujące pola `HumanRecord`** (`human_model.py`): opcjonalne
   `context`, `unit`, `quality`, `consent_scope` z ADR-HUMAN-004 (metadane
   obowiązkowe Warstwy 2, §19.2), wstecznie kompatybilne.

Świadomie NIE zrobione w tej fazie (pozostają otwarte): klasy intencji
DI-1..8, skale IQ/AR, dziesięcioosiowy profil decyzyjny §18, żywa
integracja Silnika Decyzji z Mapą Wiedzy, obowiązkowość katalogu grafu
(dziś tylko raportowanie), mapowanie dyskretnej skali pewności 0–4 Warstwy
2 na ciągłe `confidence: float`, SAFE MODE (odblokowany decyzyjnie w
Piątej turze, nadal czeka na implementację).

Zaktualizowane ADR-y (noty "Update" w Consequences, bez zmiany historii):
ADR-DECISION-001/003/005, ADR-KNOWLEDGE-003, ADR-HUMAN-004.

**Weryfikacja:** 89/89 testów (67 + 22 nowe), ruff czysty, mypy bez nowych
błędów w dotykanych modułach, demo bez zmian.

## Ósma tura — Faza 4: pierwszy wycinek Sovereign Recovery Kernel (15 sierpnia 2026)

Kontynuacja samodzielnej realizacji planu ("Kontynuuj"). SAFE MODE — po
odblokowaniu decyzyjnym w Piątej turze — dostał pierwszy działający wycinek:
`hos_engine/recovery.py` (`SovereignRecoveryKernel`, 18 testów, wszystkie
rozstrzygnięcia z `ADR-RECOVERY-006` przełożone na kod):

- **Siedem trybów awaryjnych** z mapowaniem per tryb na R0–R4 i podziałem
  wyzwalania: SAFE_MODE/READ_ONLY/FREEZE/DISCONNECT mogą wejść automatycznie
  (wyłącznie z natychmiastowym powiadomieniem właściciela; cofnięcie przez
  właściciela bezwarunkowe), ROLLBACK/EXPORT/RECOVERY tylko ręcznie.
- **Wykluczenie agentów strukturalnie**: role AGENT/SERVICE/SYSTEM_PROCESS
  nie mogą ani aktywować, ani dezaktywować żadnego trybu — a sama odmowa
  jest logowana. Kernel nie ma żadnego API zmieniającego politykę ani
  wyłączającego audyt (tabele polityk to stałe modułowe, log tylko-dopisujący)
  — gwarancja "Agent nie może zmienić polityki Recovery ani wyłączyć audytu"
  zachodzi, bo te operacje nie istnieją. Zero zależności od AI — awaria
  modelu nie blokuje ręcznego odzyskiwania.
- **Dwukluczowa suwerenność** dla ROLLBACK/RECOVERY: wymagane zatwierdzenie
  kustosza, kustosz musi być inną tożsamością niż inicjator, a przy wpiętym
  `RoleGrantRegistry` — posiadać aktywny grant `RECOVERY_CUSTODIAN` w danym
  zakresie (realizacja mapowania roli z Piątej tury).
- **Minimalny zakres i ograniczenie czasowe**: aktywacja obejmuje dokładnie
  nazwany zakres (odzyskanie jednego obszaru nie odblokowuje innych),
  `expires_at` obowiązkowe, automatyczne wygasanie.
- **13-polowy rejestr zdarzeń awaryjnych** (ADR-RECOVERY-004) z wersją
  schematu i opcjonalnym podpisem HMAC-SHA256; odmowy też są zdarzeniami.
  Opcjonalny zapis trwały do `EventStore`/`SQLiteEventStore` (łańcuch
  skrótów zweryfikowany testem).
- **Kontrakt "Freeze Entity / Scope"**: `freeze_entity()` przełącza byt na
  `HubEntityStatus.SUSPENDED` (rozstrzygnięcie FROZEN=SUSPENDED z Piątej
  tury), niedestrukcyjnie.

Świadomie NIE zrobione: pozostałe cztery kontrakty Hub (Snapshot, Rollback,
Disconnect, Export Sovereign Package), infrastruktura kluczy Emergency Root
(progowe dzielenie sekretu), typy zdarzeń `recovery_*` w `event.types.json`
(trwałe zdarzenia używają `STATE_OBSERVED` z pełnym rekordem w payload),
ośmiopoziomowa hierarchia kontroli jako całość, konkretne wartości TTL.
Podpis HMAC dzieli zastrzeżenie z `security/THREAT_MODEL.md`: mechanizm
referencyjny, nie produkcyjny.

Zaktualizowane ADR-y: noty "Update" w ADR-RECOVERY-001..004.

**Weryfikacja:** 107/107 testów (89 + 18 nowych z tej fazy), ruff czysty,
zero błędów mypy w `recovery.py` (66 znanych, wcześniejszych bez zmian),
demo bez zmian.
