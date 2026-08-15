# Digest: HUMAN OS — WARSTWA 2 — MODEL CZŁOWIEKA

**Status:** rozbiór strukturalny (nie parafraza) źródła dostarczonego przez founder-a
2026-08-15 — `Human_OS_Warstwa_2_Model_Czlowieka_v0_1.docx` (ekstrakcja pandoc z DOCX,
1865 linii tekstu jawnego). Patrz `docs/FOUNDER_REVIEW_2026-08-15.md`, sekcja "Czwarta
tura", po kontekst i listę `ADR-HUMAN-001..005` sformułowanych na podstawie tego rozbioru.
Oryginalny plik DOCX pozostaje jedynym rozstrzygającym źródłem w razie wątpliwości
(`02_Source_Truth_Protocol`). Dokument był wcześniej odnotowany w Founder Review jako
"confirmed to exist, content unavailable" — obecnie dostępny po raz pierwszy. Cały plik został przeczytany od początku do
końca (linie 1–1865) w czterech blokach, plus dodatkowe wyszukiwania wzorców (`ADR-`, "nie
wolno"/"nie może"/"zakaz", "R0-R4", "Hub"/"Digital Twin"/"Knowledge Graph") na całym pliku dla
kompletności.

Motto dokumentu (linie 25–26): *"Model jest mapą człowieka, nie człowiekiem. Każdy wniosek
pozostaje hipotezą o określonym poziomie pewności."*

---

## 1. Metadane / nagłówek dokumentu

Tabela nagłówkowa (linie 9–23):

| Pole | Wartość |
|---|---|
| Wersja | 0.1 – model bazowy |
| Status | Projekt do iteracji, walidacji i zatwierdzenia |
| Zakres | Wielowymiarowy model człowieka, jego dynamiki, kontekstu i rozwoju |
| Dokument nadrzędny | Warstwa 1 – Konstytucja i Wartości |
| Właściciel dokumentu | Zespół założycielski Human OS |
| Data | 2026-07-19 |

Uwaga: w przeciwieństwie do Warstwy 6 (która ma osobne wiersze "Model osoby", "Źródło wiedzy"
itd. wskazujące na wszystkie warstwy nadrzędne), Warstwa 2 wskazuje **tylko jeden** dokument
nadrzędny — Warstwę 1 (Konstytucję). Nie ma tu odniesienia do innych warstw w samej karcie
dokumentu — te pojawiają się dopiero w sekcji 24 "Interfejsy".

**Cel dokumentu** (0.1, linie 32–40): definiuje wspólną reprezentację człowieka używaną przez
Human OS — jakie obszary życia system rozpoznaje, jak rozdziela dane od interpretacji, jak
opisuje zmiany w czasie oraz jak łączy biologię, psychikę, relacje, środowisko, znaczenie i
systemy autorefleksji. Zastrzeżenie: "Dokument nie opisuje konkretnej osoby. Opisuje język,
którym system może mówić o osobie bez redukowania jej do pojedynczej etykiety."

**Zasada nadrzędna modelu** (ramka, linie 42–49): *"Model człowieka MUSI zwiększać zrozumienie,
sprawczość i bezpieczeństwo użytkownika. NIE MOŻE stawać się mechanizmem szufladkowania,
deterministycznego przewidywania ani oceniania wartości człowieka."*

**Zakres obowiązywania** (0.2, linie 52–66):
- Obejmuje: onboarding, profil użytkownika, dialog AI, rekomendacje, pomiary, ścieżki rozwoju,
  eksperymenty, społeczność, raporty i integracje.
- Obowiązuje: projektantów produktu, architektów danych, twórców modeli AI, ekspertów
  domenowych, badaczy i moderatorów.
- Nie zastępuje: diagnozy medycznej, psychologicznej, psychiatrycznej, oceny prawnej ani pełnego
  obrazu osoby uzyskanego w relacji międzyludzkiej.
- Podlega: Konstytucji i Wartościom, zasadom prywatności, bezpieczeństwa oraz sygnaturze wiedzy.

**Test nadrzędny** (0.5, linie 117–125) — pytanie kontrolne bramkujące każdy opis człowieka:
> "Czy opis pozostawia miejsce na zmianę, kontekst, wyjątki i niewiedzę, czy też zamienia
> człowieka w stałą etykietę? Jeśli zamienia go w etykietę, model wymaga korekty."

Hierarchia reprezentacji (0.4, linie 101–116): OSOBA → DOMENY ŻYCIA → SYSTEMY I PROCESY →
ZDOLNOŚCI/ZASOBY/OGRANICZENIA → STANY/WZORCE/ZACHOWANIA → WSKAŹNIKI/OBSERWACJE/DANE → HIPOTEZY I
DECYZJE.

---

## 2. Nazwane decyzje architektoniczne w stylu ADR

**Brak.** Przeszukano cały dokument pod kątem wzorca `ADR-` (case-sensitive) — zero wystąpień.
Tak jak Warstwa 6, Warstwa 2 nie zawiera dedykowanej sekcji ani numeracji ADR. Jest to dokument
specyfikacyjny/ontologiczny (7 aksjomatów w sekcji 1, "wielorzędowa architektura" Rząd 0–6 w
sekcji 2, kryteria akceptacji w sekcji 27, deklaracja w Załączniku G), ale nie formalizuje
decyzji w formacie ADR. Jeśli Reconstruction Audit ma zaimportować decyzje z tego dokumentu do
`docs/adr/`, trzeba je dopiero sformułować — nie ma tu gotowych ADR-ów do wyciągnięcia.

Najbliższe odpowiedniki "decyzji architektonicznych":
- 7 aksjomatów Modelu Człowieka w sekcji 1 (linie 128–194),
- "Architektura wielorzędowa modelu" (Rząd 0–6, sekcja 2, linie 196–273) — kluczowa decyzja
  strukturalna: od osoby-jako-całości, przez domeny, systemy/procesy, zdolności/zasoby/
  ograniczenia, stany/wzorce/zachowania, dane/obserwacje, aż po hipotezy/decyzje,
- "Kryteria akceptacji Warstwy 2" (sekcja 27, linie 1547–1587) — 15-punktowa lista bramkowa,
- Załącznik A "Ontologia skrócona" (linie 1589–1650) — minimalne drzewo pojęć do implementacji.

---

## 3. Kluczowe encje / kontrakty danych

### 3.1 Architektura wielorzędowa (sekcja 2, linie 196–273) — szkielet ontologii

| Rząd | Poziom | Definicja |
|---|---|---|
| Rząd 0 | Osoba jako nieredukowalna całość | Godność, autonomia i wartość nie wynikają z danych; model NIE MOŻE obliczać "wartości człowieka", poziomu moralności ani ostatecznego potencjału |
| Rząd 1 | Domeny | Porządkują złożoność, nie są oddzielnymi częściami człowieka; mają granice robocze i jawne połączenia |
| Rząd 2 | Systemy i procesy | Działające mechanizmy, np. regulacja snu, uwaga, poczucie bezpieczeństwa, budowa więzi, podejmowanie decyzji, budowa znaczenia |
| Rząd 3 | Zdolności, zasoby, ograniczenia | Zdolność = co osoba może zrobić przy sprzyjających warunkach; zasób zwiększa możliwość działania; ograniczenie zmniejsza ją czasowo lub trwale |
| Rząd 4 | Stany, wzorce, zachowania | Stan = chwila; wzorzec = powtarzalność; zachowanie = działanie; nie budować mocnych wniosków z izolowanych wydarzeń |
| Rząd 5 | Dane i obserwacje | Z samoopisu, urządzeń, dokumentów, testów, zachowania w systemie, refleksji eksperta lub społeczności; każdy rekord ma źródło, czas, kontekst, jakość, zgodę, ograniczenia interpretacji |
| Rząd 6 | Hipotezy i decyzje | Wnioski o użytkowniku są wersjonowanymi hipotezami; rekomendacje powstają po połączeniu hipotezy z celem, tolerancją ryzyka, kosztami, alternatywami |

### 3.2 Mapa 11 domen człowieka (sekcja 3, linie 275–326) — pełna tabela

| # | Domena | Zakres | Funkcja |
|---|---|---|---|
| 1 | Biologia i zdrowie | Ciało, energia, regeneracja, metabolizm, odporność, starzenie | Funkcjonowanie fizyczne i bezpieczeństwo zdrowotne |
| 2 | Układ nerwowy i psychofizjologia | Pobudzenie, stres, rytmy, odczucia z ciała, regulacja | Zdolność przechodzenia między działaniem a regeneracją |
| 3 | Poznanie | Uwaga, pamięć, uczenie się, rozumowanie, decyzje | Orientacja w świecie i skuteczne rozwiązywanie problemów |
| 4 | Emocje | Rozpoznawanie, tolerowanie, wyrażanie i regulacja emocji | Informacja o potrzebach, znaczeniu i bezpieczeństwie |
| 5 | Tożsamość i osobowość | Obraz siebie, role, cechy, narracja autobiograficzna | Ciągłość i elastyczność sposobu bycia |
| 6 | Motywacja, wartości i sprawczość | Potrzeby, cele, wybory, samoskuteczność, dyscyplina | Nadawanie kierunku i przejście od intencji do działania |
| 7 | Relacje i system społeczny | Więź, komunikacja, granice, role, wsparcie i konflikt | Współregulacja, przynależność i współdziałanie |
| 8 | Środowisko i styl życia | Dom, praca, technologia, ekonomia, natura, rytm dnia | Warunki wzmacniające lub osłabiające możliwości osoby |
| 9 | Świadomość, sens i duchowość | Obecność, refleksja, światopogląd, śmiertelność, praktyka | Budowanie znaczenia i relacji z doświadczeniem |
| 10 | Twórczość, praca i wkład | Ekspresja, mistrzostwo, tworzenie, przywództwo, służba | Przekształcanie potencjału w wartość dla siebie i świata |
| 11 | Systemy interpretacyjne | Human Design, astrologia, archetypy, typologie, tradycje | Generowanie pytań i hipotez autorefleksyjnych |

**3.2 Domeny rdzeniowe vs opcjonalne**: każdy użytkownik ma dostęp do rdzenia (bezpieczeństwo,
energia, emocje, relacje, sprawczość, sens); domeny specjalistyczne (w tym systemy symboliczne,
domena 11) aktywowane świadomie i nie dominują profilu bez zgody.

### 3.3 Terminy podstawowe modelu — Rząd/kategoria (0.3, linie 68–99)

Domena, System, Zdolność, Stan, Cecha, Wzorzec, Kontekst, Trajektoria, Hipoteza użytkownika —
pełne definicje w sekcji 5 poniżej (glosariusz).

### 3.4 Poszczególne domeny — jednostki modelu (przykłady, sekcje 4–18)

- **4.2 Jednostki modelu biologicznego**: Funkcja, Regulacja, Rezerwa, Obciążenie, Objaw,
  Marker, Zdarzenie kliniczne (każda z opisem i przykładem, linie 362–389).
- **5.1 Procesy psychofizjologiczne**: Pobudzenie, Regulacja, Interocepcja, Współregulacja,
  Tolerancja obciążenia, Rytmiczność, Ucieleśnienie (linie 414–429).
- **5.2 Mapa stanów regulacyjnych** (linie 431–454): Regulacja użyteczna, Nadmierne pobudzenie,
  Obniżone pobudzenie, Przeciążenie mieszane, Regeneracja — każdy z sygnałami i "potrzebą
  systemową".
- **6.1 Funkcje poznawcze**: Uwaga, Pamięć robocza, Uczenie się, Rozumowanie, Metapoznanie,
  Decyzje, Elastyczność (linie 466–493).
- **7.1 Elementy modelu emocji**: Sygnał, Interpretacja, Impuls, Potrzeba, Regulacja, Ekspresja,
  Skutek (linie 512–528).
- **7.2 Zdolności emocjonalne**: Rozpoznawanie, Różnicowanie, Tolerowanie, Regulowanie,
  Komunikowanie, Integracja (linie 530–553).
- **8.1 Składniki tożsamości**: poczucie "kim jestem"/"kim się staję", role życiowe,
  historia autobiograficzna, wartości i zobowiązania, obraz ciała i możliwości, stosunek do
  sukcesu/porażki/zmiany, aspiracje/ideały/obawy (linie 566–580).
- **9.1 Hierarchia kierunku**: SENS/WARTOŚCI → PRIORYTETY ŻYCIOWE → CELE I KRYTERIA SUKCESU →
  PROJEKTY I EKSPERYMENTY → NASTĘPNY KROK/NAWYK/DECYZJA (linie 622–640).
- **10.1 Jednostki relacyjne**: Relacja, Więź, Rola, Granica, Wymiana, Konflikt, Sieć (linie
  682–707).
- **11.1 Mapa środowiska**: Fizyczne, Czasowe, Cyfrowe, Ekonomiczne, Organizacyjne, Kulturowe,
  Prawne i społeczne (linie 736–763).
- **17.2 Rodzaje zasobów**: Biologiczne, Psychologiczne, Relacyjne, Materialne, Czasowe,
  Informacyjne, Znaczeniowe (linie 1042–1066).
- **18.1 Typy relacji między domenami**: Wzmacniająca, Hamująca, Dwukierunkowa, Warunkowa,
  Opóźniona, Progowa, Kompensacyjna, Konfliktowa (linie 1086–1116) — z przykładami (np. "sen
  wspiera regulację emocji", "alkohol pogarsza jakość snu").

### 3.5 Kontrakty pomiarowe (sekcja 19, linie 1132–1197)

**19.1 Źródła danych** (tabela z mocnymi stronami i ograniczeniami): Samoopis, Urządzenie,
Badanie/dokument, Zachowanie w aplikacji, Obserwacja eksperta, Raport społeczności, System
symboliczny.

**19.2 Metadane obowiązkowe** dla każdego rekordu danych: źródło i właściciel danych; czas oraz
strefa czasowa; kontekst i aktywne interwencje; jednostka oraz skala; jakość, kompletność i
możliwy błąd; status (surowe/przetworzone/wywnioskowane); cel użycia i zakres zgody; okres
retencji i możliwość usunięcia.

**19.3 Rozdzielenie danych od wniosku** — przykład wzorcowy (ramka, linie 1183–1191): "Dane:
'użytkownik spał średnio 5 h 40 min przez cztery dni i ocenił energię na 3/10'. Wniosek:
'niedobór snu prawdopodobnie ogranicza energię'. Rekomendacja: 'najpierw przetestuj możliwość
zwiększenia snu'. Każda warstwa powinna być przechowywana osobno."

### 3.6 Ontologia obiektów danych — Załącznik A "Ontologia skrócona" (linie 1589–1650)

Drzewo minimalnych pojęć do implementacji:

```
PERSON
├── identity_and_roles
├── goals_values_meaning
├── domains[]
│   ├── systems[]
│   ├── capacities[]
│   ├── resources[]
│   ├── constraints[]
│   └── states_patterns[]
├── contexts[]
├── relationships[]
├── observations[]
├── hypotheses[]
├── trajectories[]
├── preferences_and_consent
└── model_versions[]
```

Pola minimalne poszczególnych obiektów (tabela, linie 1626–1650):

| Obiekt | Pola minimalne |
|---|---|
| Observation | id, source, timestamp, context, value, unit, quality, consent_scope |
| Hypothesis | statement, evidence_refs, alternatives, confidence, scope, created_at, reviewed_at |
| Pattern | trigger, sequence, context, frequency, exceptions, impact |
| Goal | owner, domain, motive, metric, horizon, priority, tradeoffs, status |
| Context | place, role, people, time, load, environment, relevant_events |
| Trajectory | variable, period, direction, variability, turning_points |
| Interpretive map | system, source, claim_type, reflection_questions, user_response |

**Krytyczne dla porównania z kodem (`hos_engine/human_model.py`):** dokument nazywa "Observation"
jako podstawowy rekord danych (`id, source, timestamp, context, value, unit, quality,
consent_scope`) — pola `source`, `context`, `quality`, `consent_scope`, `unit` nie mają
odpowiedników w polach `HumanRecord` z kodu (`record_id, subject_id, domain, key, value,
evidence_type, confidence, source_id, created_at, status, supersedes, sensitive, tags`). Kod
dodatkowo ma `status: RecordStatus` (ACTIVE/CONTESTED/SUPERSEDED/DELETED) i `supersedes`
(łańcuch wersji), których dokument osobno nie nazywa polami obiektu, choć koncepcyjnie żąda tej
funkcji w sekcji 23.2 "Wersjonowanie" (data utworzenia, wersja, podstawa, zmiana poziomu
pewności, historia korekt) i w sekcji 20.4 "Prawo użytkownika do korekty" (oznaczenie hipotezy
jako trafnej/częściowo trafnej/nietrafnej/niechcianej — zbliżone do `contest()` w kodzie, ale
kod ma tylko jeden stan CONTESTED, a dokument sugeruje więcej granulacji). Dokument też wymaga
`consent_scope`/zakresu zgody per-obserwacja — pole to nie istnieje w `HumanRecord`. To są
rozbieżności do odnotowania, nie do rozstrzygnięcia w tym zadaniu.

**Poziomy pewności** (sekcja 20.1, linie 1203–1223) — skala 0–4 słowna ("brak podstaw" /
"możliwość" / "robocza hipoteza" / "wzorzec wspierany" / "silnie wspierany") z przypisanym
językiem komunikacji — różni się od pola `confidence: float` (0–1 ciągłe) w kodzie. Nie jest to
sprzeczne wprost, ale dokument opisuje dyskretną, 5-poziomową skalę słowną, a kod używa ciągłej
liczby zmiennoprzecinkowej — mapowanie między nimi nie jest zdefiniowane w żadnym z dwóch
źródeł.

### 3.7 Załącznik B — Karta domeny (szablon, linie 1652–1693)

Pola: Nazwa i identyfikator, Cel, Zakres, Połączenia, Jednostki, Źródła danych, Ograniczenia,
Ryzyka, Sygnały eskalacji, Metryki sukcesu, Właściciel, Wersja i przegląd.

### 3.8 Załącznik C — Karta hipotezy o użytkowniku (linie 1695–1728)

Pola: Treść hipotezy, Zakres, Źródła, Pewność, Alternatywy, Kontrprzykłady, Test, Ryzyko testu,
Kryterium wyniku, Status (Aktywna/odrzucona/wsparta/wygasła).

---

## 4. Bramy ryzyka/bezpieczeństwa i reguły eskalacji

**Uwaga terminologiczna**: dokument NIE używa skali "R0–R4" (skala Konstytucji/Warstwy 1 wg
CLAUDE.md tego repozytorium — przeszukano cały plik, brak wystąpień "R0", "R1"…"R4" w tym
kontekście). Warstwa 2 **nie definiuje własnej litero-kodowanej skali ryzyka** w stylu Warstwy 6
(XP/SE/EC/BL/MQ/PF/DQ/CA/PE) — nie ma tu analogicznego zbiorczego załącznika kodów operacyjnych.
Zamiast tego Warstwa 2 opisuje bramy jako **tryby działania** (nazwane słownie, nie kodowo).

### 4.1 Trzy tryby działania (22.1, linie 1313–1332)

| Tryb | Zakres | Odpowiedź systemu |
|---|---|---|
| Rozwój i dobrostan | Brak oznak pilnego ryzyka | Eksperymenty, edukacja, refleksja |
| Wsparcie przy ograniczeniu | Objawy, przewlekłe trudności lub niepewność | Ostrożność, monitoring, konsultacja |
| Bezpieczeństwo i eskalacja | Bezpośrednie lub poważne ryzyko | Przerwanie optymalizacji, pilne wskazanie pomocy |

### 4.2 Przykładowe sygnały eskalacyjne (22.2, linie 1334–1351)

- Nagły lub nasilający się objaw fizyczny o potencjalnie poważnym znaczeniu.
- Utrata kontaktu z rzeczywistością, mania albo znaczna dezorganizacja.
- Ryzyko samouszkodzenia, przemocy lub wykorzystania.
- Istotne działania niepożądane po interwencji.
- Przemoc domowa, przymus lub zagrożenie bezpieczeństwa.
- Długotrwałe pogorszenie funkcjonowania mimo prostych działań.
- Zamiar zastąpienia koniecznego leczenia praktyką symboliczną lub eksperymentalną.

### 4.3 Zasada niepatologizowania (22.3, linie 1353–1358)

"Nie każda różnica, intensywna emocja, kryzys sensu lub nietypowe doświadczenie jest
zaburzeniem. System powinien uwzględniać cierpienie, funkcjonowanie, czas, kontekst i ryzyko,
unikając zarówno bagatelizowania, jak i nadmiernej medykalizacji."

### 4.4 Bezpieczeństwo emocjonalne (7.3, linie 555–560)

"W sytuacji silnego cierpienia, kryzysu, przemocy, psychozy, manii lub ryzyka samouszkodzenia
system powinien przełączyć się z optymalizacji na bezpieczeństwo, uprościć komunikację i
kierować do odpowiedniej pomocy. Model rozwoju nie może przykrywać potrzeb klinicznych."

### 4.5 Granica kliniczna (4.4, ramka, linie 401–407)

"Human OS może porządkować informacje, wspierać pytania do specjalisty i monitorować uzgodnione
działania. Nie stawia samodzielnie diagnozy ani nie odradza leczenia na podstawie systemu
symbolicznego, doświadczeń społeczności lub pojedynczego wskaźnika."

### 4.6 Ryzyka modelu i tryby awarii — sekcja 25 (linie 1431–1473)

Tabela pełna: Redukcjonizm, Determinizm, Efekt potwierdzenia, Nadmierna personalizacja, Pomiar
zamiast życia, Autorytet AI, Kult mistrza, Spiritual bypassing, Dyskryminacja, Zbieranie
nadmiaru — każdy z "Mechanizmem szkody" i "Zabezpieczeniem" (patrz sekcja 7 tej digest dla
szczegółów zabezpieczeń niedeterminizmu).

### 4.7 Zmiany chronione ontologii (26.3, linie 1539–1545)

"Zmiany umożliwiające ocenę wartości człowieka, automatyczną diagnozę wysokiego ryzyka, niejawne
profilowanie osób trzecich lub deterministyczne wykorzystanie systemów symbolicznych powinny
wymagać odrzucenia jako sprzeczne z Warstwą 1, a nie zwykłej decyzji produktowej." — to jest
najbliższy odpowiednik "bramy konstytucyjnej" widocznej explicite w Warstwie 6 (sekcja X0 "Brama
konstytucyjna").

**Podsumowanie różnicy względem Warstwy 6**: Warstwa 6 ma rozbudowaną, wielowarstwową
architekturę bram (SE0-SE4, HOLD/STOP/ESCALATE/SYSTEM PAUSE, XP-0..XP-8 klasy procesu) z
osobnym załącznikiem zbiorczym kodów (Załącznik M). Warstwa 2 nie ma takiej infrastruktury
kodowej — jej "bramy" są jakościowe/opisowe (trzy tryby, sygnały eskalacyjne, granica kliniczna,
zasada niepatologizowania), skoncentrowane bardziej na **epistemicznym** ryzyku (redukcjonizm,
determinizm, etykietowanie) niż na **proceduralnym** ryzyku eksperymentu. To spójne z tym, że
Warstwa 2 jest modelem/ontologią osoby, a Warstwa 6 jest silnikiem wykonawczym eksperymentów.

---

## 5. Kluczowa terminologia (0.3 "Język modelu", linie 68–99)

| Termin | Definicja |
|---|---|
| Domena | Szeroki obszar funkcjonowania, np. biologia, emocje, relacje. |
| System | Zespół powiązanych procesów w domenie, np. regulacja stresu. |
| Zdolność | Relatywnie trwała możliwość działania, np. samoregulacja. |
| Stan | Aktualna, zmienna konfiguracja, np. pobudzenie lub zmęczenie. |
| Cecha | Względnie stabilna tendencja, która nie determinuje zachowania. |
| Wzorzec | Powtarzalna sekwencja stanów i działań w określonym kontekście. |
| Kontekst | Warunki, w których ujawnia się stan, zachowanie lub wynik. |
| Trajektoria | Kierunek zmian w czasie, a nie pojedynczy pomiar. |
| Hipoteza użytkownika | Wniosek systemu wymagający dalszej obserwacji lub potwierdzenia. |

Dodatkowe pojęcia zdefiniowane rozproszone w treści (poza tabelą 0.3):

- **Rząd** (sekcja 2) — poziom w architekturze wielorzędowej (Rząd 0 = osoba, ..., Rząd 6 =
  hipotezy i decyzje); zob. sekcja 3.1 tej digest.
- **Epizod** (sekcja 16, tabela) — trwałość "ograniczona w czasie", np. "tydzień silnego
  stresu"; wymóg: "szukać zdarzeń i początku".
- **Reguła trzech kontekstów** (16.1) — "Przed uznaniem zachowania za względnie stały wzorzec
  system powinien, gdy to możliwe, zebrać obserwacje z co najmniej trzech różnych sytuacji lub
  wyraźnie oznaczyć ograniczony zakres wniosku."
- **Reguła kontrprzykładu** (16.2) — "Każda mocniejsza hipoteza o osobie powinna zawierać
  pytanie: 'Kiedy jest inaczej?'."
- **Potrzeba** (17.1) — "warunek dobrostanu, bezpieczeństwa albo realizacji wartości"; odróżniona
  od jednej konkretnej strategii jej zaspokojenia.
- **Rezerwa i próg przeciążenia** (17.4) — model powinien szacować nie tylko aktualne wykonanie,
  ale rezerwę zdolności.
- **Sygnatura obowiązkowa** (14.1, ramka) — status epistemiczny systemów symbolicznych: "Systemy
  symboliczne są prezentowane jako mapy interpretacyjne i generatory pytań. Nie są używane jako
  podstawa diagnozy medycznej, prawnej, finansowej ani jako dowód niezmiennej natury
  użytkownika."
- **Zasada domen przecinających się** (3.1) — zjawiska realnego życia zwykle należą do kilku
  domen naraz (przykład: bezsenność).
- **Zasada pluralizmu rozwojowego** (1.7, ramka) — "Human OS nie definiuje jednego modelu
  doskonałego życia."
- **Zasada funkcji ponad pojedynczym markerem** (4.3) — wynik laboratoryjny/masa ciała/wiek
  biologiczny to elementy mapy, nie ostateczny cel.
- **Cechy jako rozkłady, nie wyroki** (8.2) — cechy osobowości reprezentowane jako tendencje
  zależne od kontekstu i czasu, nie jako deterministyczne przewidywania.
- **Zasada efektów wtórnych** (18.3) — każda istotna rekomendacja powinna oceniać skutki w co
  najmniej trzech domenach (bezpośredniej, powiązanej, długoterminowej).
- **Zasada niepatologizowania** (22.3) — patrz sekcja 4.3 powyżej.
- **Minimalna skuteczna personalizacja** (21.3) — system zaczyna od najprostszego modelu
  wystarczającego do dobrej decyzji.
- **Prawo do resetu modelu** (21.4) — użytkownik może zarchiwizować hipotezy, rozpocząć nowy
  etap lub ograniczyć wpływ historii.

---

## 6. Relacje z innymi warstwami / komponentami Human OS

Sekcja 24 "Interfejsy z pozostałymi warstwami Human OS" (linie 1390–1429), tabela "Warstwa / Co
otrzymuje z Modelu Człowieka / Co przekazuje do Modelu Człowieka" (uwaga: w tej tabeli wiersze są
podpisane tylko numerem, np. "1. Konstytucja", "3. Mapa wiedzy" — bez pełnego słowa "Warstwa X"
przed nazwą, w przeciwieństwie do karty dokumentu, gdzie "Warstwa 1" pojawia się w pełnej formie
tylko raz):

| Warstwa | Co otrzymuje z Modelu Człowieka | Co przekazuje do Modelu Człowieka |
|---|---|---|
| 1. Konstytucja | granice opisu, zakaz determinizmu, prawa użytkownika | wartości i reguły nadrzędne |
| 3. Mapa wiedzy | domeny, kontekst i potrzeby personalizacji | źródła, mechanizmy, niepewność |
| 4. Model użytkownika | strukturę profilu i relacji | konkretne dane, cele i historię osoby |
| 5. Silnik decyzji | cele, zasoby, ograniczenia i konflikty | rekomendacje oraz uzasadnienie |
| 6. Silnik eksperymentów | zmienne, mierniki i kryteria | wyniki i nowe obserwacje |
| 7. Inteligencja zbiorowa | anonimowe cechy kontekstu i wyników | wzorce populacyjne i sygnały bezpieczeństwa |

**Uwaga o numeracji warstw**: ta tabela **nie wymienia "2. Model Człowieka"** samego siebie
(oczywiste, bo to dokument tej warstwy) ani nie ma osobnego wiersza dla siebie w formacie
identycznym jak Warstwa 6 miała ("2. Model Człowieka" jako wiersz w tabeli interfejsów Warstwy
6). Numeracja warstw jest tu spójna z tym, co Warstwa 6 przypisała: Warstwa 1 = Konstytucja,
Warstwa 3 = Mapa Wiedzy, Warstwa 4 = Model Użytkownika (i Cyfrowy Profil — ale to dokładne
sformułowanie "Cyfrowy Profil" nie pojawia się w tym pliku, tylko w nagłówku Warstwy 6), Warstwa
5 = Silnik Decyzji, Warstwa 6 = Silnik Eksperymentów, Warstwa 7 = Inteligencja zbiorowa (podobnie
jak w Warstwie 6, brak odrębnej sekcji opisującej Warstwę 7 z nazwy — tylko wiersz w tabeli
interfejsów).

**24.1 Kontrakt minimalny** (linie 1419–1429): każdy wniosek posiada źródło i poziom pewności;
każda obserwacja posiada czas i kontekst; każdy cel posiada właściciela — użytkownika, nie
system; każda rekomendacja wskazuje, jakie elementy modelu ją uruchomiły; każda warstwa
respektuje prawo do korekty, odmowy i usunięcia.

**Hub / Digital Twin / Knowledge Graph** — te nazwy własne używane w repozytorium kodu (`hub/`,
`knowledge_graph.py`) **nie pojawiają się** w tym dokumencie (przeszukano cały plik). Tak samo
jak w Warstwie 6, dokument mówi o "Mapie Wiedzy" (Warstwa 3), a nie o "Knowledge Graph"/"Hub"
explicite. Nie zakładać 1:1 mapowania na moduły kodu bez dodatkowej weryfikacji.

**Human Design / astrologia / systemy interpretacyjne** — traktowane jako **jedna z 11 domen
modelu** (domena 11 "Systemy interpretacyjne", linie 323–325) oraz osobna sekcja 14 "Systemy
interpretacyjne i symboliczne" (linie 870–939), a nie jako oddzielny moduł eksperymentalny jak w
Warstwie 6 (sekcja 32). Warstwa 2 traktuje je fundamentalniej — jako część samej ontologii osoby
("generowanie pytań i hipotez autorefleksyjnych"), podczas gdy Warstwa 6 traktuje je jako
przedmiot eksperymentu behawioralnego. Oba dokumenty zgadzają się co do "zapory epistemicznej":
Warstwa 2 ma "Sygnaturę obowiązkową" (14.1) niemal identyczną w duchu do "Zapory epistemicznej"
(32.4) Warstwy 6.

---

## 7. Explicit prohibitions ("nie ma prawa" / "nie wolno" / "zabrania się")

Dokument **nie zawiera** ani jednego wystąpienia fraz "nie ma prawa", "nie wolno" ani "zabrania
się" (przeszukano cały plik, case-insensitive — zero trafień dla tych trzech fraz). Jest to
istotna różnica względem Warstwy 6, która miała 10 dosłownych wystąpień "nie wolno" plus jedno
"nie ma prawa". Warstwa 2 formułuje swoje zakazy niemal wyłącznie przez **"nie może"/"NIE
MOŻE"/"nie jest"/tytuły sekcji "Zakaz ..."** zamiast przez "nie wolno". Pełna lista znalezionych
cytatów normatywnych (wyszukano wzorce case-insensitive w całym pliku):

1. (linia 46, ramka "Zasada nadrzędna modelu", 0.1) — *"Model człowieka MUSI zwiększać
   zrozumienie, sprawczość i bezpieczeństwo użytkownika. NIE MOŻE stawać się mechanizmem
   szufladkowania, deterministycznego przewidywania ani oceniania wartości człowieka."*
2. (linia 175, Aksjomat 1.5 Kontekstowość) — *"Model MUSI przechowywać kontekst obserwacji i NIE
   MOŻE automatycznie uogólniać zachowania z jednej sytuacji na całą osobowość."*
3. (linia 182, Aksjomat 1.6 Subiektywność) — *"[Doświadczenie pierwszoosobowe] Nie zastępuje ono
   pomiarów zewnętrznych, ale nie może być przez nie automatycznie unieważniane."*
4. (linia 203, 2.1 Rząd 0 – osoba jako nieredukowalna całość) — *"Model może opisywać
   funkcjonowanie, lecz nie może obliczać 'wartości człowieka', poziomu moralności ani
   ostatecznego potencjału."*
5. (linia 456–459, tytuł sekcji 5.3 "Zakaz moralizowania stanu") — *"Stan układu nerwowego nie
   jest wadą charakteru. System nie może interpretować zmęczenia jako lenistwa, pobudzenia jako
   braku dojrzałości ani trudności regulacyjnych jako niższej wartości użytkownika."*
6. (linia 560, 7.3 Bezpieczeństwo emocjonalne) — *"Model rozwoju nie może przykrywać potrzeb
   klinicznych."*
7. (linia 860, 13.2 Oddzielenie produktywności od wartości osoby) — *"Wynik pracy może być
   oceniany, lecz wartość człowieka nie może zależeć od produktywności."*
8. (linia 1249, 20.4 Prawo użytkownika do korekty) — *"Odrzucenie modelu przez użytkownika nie
   może być automatycznie interpretowane jako opór psychologiczny."*
9. (linia 1310, 21.4 Prawo do resetu modelu) — *"Model nie może więzić osoby w dawnym opisie
   tylko dlatego, że posiada dużo danych."*
10. (linia 403–406, ramka "Granica kliniczna", 4.4) — *"Human OS może porządkować informacje,
    wspierać pytania do specjalisty i monitorować uzgodnione działania. Nie stawia samodzielnie
    diagnozy ani nie odradza leczenia na podstawie systemu symbolicznego, doświadczeń
    społeczności lub pojedynczego wskaźnika."*

Sekcje tytułowane "Zakaz ..." (formułują wiążący zakaz w tytule, bez dosłownego "nie wolno"):
- **5.3 Zakaz moralizowania stanu** (cytat nr 5 powyżej).

Listy zakazanych elementów bez frazy "nie wolno"/"nie może", ale normatywne z tytułu/kontekstu:
- **14.3 Niedopuszczalne zastosowania [systemów symbolicznych]** (linie 901–914) — sześć
  punktów: stwierdzanie, że użytkownik "musi" działać zgodnie z typem; przewidywanie choroby,
  śmierci, zdrady lub wyniku inwestycji; odradzanie leczenia albo profesjonalnej pomocy;
  tworzenie hierarchii typów, poziomu duszy lub wartości człowieka; profilowanie osób trzecich
  bez zgody; uzależnianie dostępu do ścieżki rozwoju od zaakceptowania światopoglądu.
- **25.1 Zakazane wnioski** (linie 1475–1487) — sześć przykładowych zdań, których system nie
  powinien formułować: *"Jesteś swoim wynikiem, typem lub diagnozą."*, *"Twoja przyszłość jest
  przesądzona."*, *"Brak postępu oznacza brak wartości lub zaangażowania."*, *"System zna Cię
  lepiej niż Ty sam."*, *"Każde cierpienie jest lekcją, którą sam wybrałeś."*, *"Jedna metoda
  wyjaśnia całego człowieka."*
- **26.3 Zmiany chronione** (linie 1539–1545) — zmiany "umożliwiające ocenę wartości człowieka,
  automatyczną diagnozę wysokiego ryzyka, niejawne profilowanie osób trzecich lub
  deterministyczne wykorzystanie systemów symbolicznych powinny wymagać odrzucenia jako
  sprzeczne z Warstwą 1."
- **10.3 Ochrona osób trzecich** (linie 725–730) — "Model użytkownika [...] nie może tworzyć
  pełnych profili psychologicznych osób trzecich bez ich zgody."

**Uwaga dla audytu (zgodnie ze wskazówką zadania o determinizmie/etykietowaniu):** ta warstwa,
mimo że dotyka wrażliwego modelowania psychologiczno-biologicznego, formułuje swoje
zabezpieczenia przeciw redukcjonizmowi/determinizmowi/etykietowaniu **słabszym językiem
modalnym** niż Warstwa 6 (przewaga "nie może"/"MUSI"/"NIE MOŻE" nad "nie wolno"). Rdzeń tych
zabezpieczeń skupia się wokół Rzędu 0 (osoba jako nieredukowalna całość, sekcja 2.1), zakazu
etykietowania (sekcja 25.1 "Zakazane wnioski"), zakazu moralizacji (5.3, 12.4-analog niewystępujący
tu dosłownie — patrz niżej), oraz sekcji 8.2 "Cechy jako rozkłady, nie wyroki". Nie znaleziono w
tym dokumencie odpowiednika sformułowania "12.4 Zakaz moralizacji zgodności" z Warstwy 6 — Warstwa
2 ma analogiczną zasadę pod inną numeracją i tytułem (5.3 "Zakaz moralizowania stanu"), co
sugeruje możliwe zamierzone powielenie tej samej zasady na dwóch warstwach pod różnymi nazwami —
warto to zaznaczyć jako potencjalny punkt do ADR/harmonizacji terminologii, bez rozstrzygania tu.

---

## 8. Struktura dokumentu (spis treści wg nagłówków)

```
HUMAN OS — WARSTWA 2 — MODEL CZŁOWIEKA
Pełna dokumentacja ontologiczna, funkcjonalna i operacyjna

0.   Karta dokumentu i sposób stosowania
  0.1  Cel dokumentu
  0.2  Zakres obowiązywania
  0.3  Język modelu
  0.4  Hierarchia reprezentacji
  0.5  Test nadrzędny
1.   Aksjomaty Modelu Człowieka
  1.1  Człowiek jest systemem otwartym
  1.2  Człowiek nie jest sumą danych
  1.3  Wielopoziomowość
  1.4  Dynamika i plastyczność
  1.5  Kontekstowość
  1.6  Subiektywność jako prawidłowe źródło danych
  1.7  Brak jednego ideału człowieka
2.   Architektura wielorzędowa modelu
  2.1  Rząd 0 – osoba jako nieredukowalna całość
  2.2  Rząd 1 – domeny
  2.3  Rząd 2 – systemy i procesy
  2.4  Rząd 3 – zdolności, zasoby i ograniczenia
  2.5  Rząd 4 – stany, wzorce i zachowania
  2.6  Rząd 5 – dane i obserwacje
  2.7  Rząd 6 – hipotezy i decyzje
3.   Mapa domen człowieka
  3.1  Zasada domen przecinających się
  3.2  Domeny rdzeniowe i ścieżki opcjonalne
4.   Domena biologii i zdrowia
  4.1  Zakres
  4.2  Jednostki modelu biologicznego
  4.3  Zasada funkcji ponad pojedynczym markerem
  4.4  Granice interpretacji
5.   Układ nerwowy i psychofizjologia
  5.1  Główne procesy
  5.2  Mapa stanów regulacyjnych
  5.3  Zakaz moralizowania stanu
6.   Domena poznawcza
  6.1  Funkcje poznawcze
  6.2  Obciążenie poznawcze
  6.3  Style poznawcze
7.   Domena emocjonalna
  7.1  Elementy modelu emocji
  7.2  Zdolności emocjonalne
  7.3  Bezpieczeństwo emocjonalne
8.   Tożsamość, osobowość i narracja
  8.1  Składniki tożsamości
  8.2  Cechy jako rozkłady, nie wyroki
  8.3  Narracje wspierające i ograniczające
  8.4  Prawo do wielu tożsamości
9.   Motywacja, wartości, cele i sprawczość
  9.1  Hierarchia kierunku
  9.2  Rodzaje motywacji
  9.3  Sprawczość
  9.4  Konflikty celów
10.  Relacje i system społeczny
  10.1 Jednostki relacyjne
  10.2 Jakość relacji
  10.3 Ochrona osób trzecich
11.  Środowisko, styl życia i warunki strukturalne
  11.1 Mapa środowiska
  11.2 Zasada projektowania warunków
  11.3 Ograniczenia strukturalne
12.  Świadomość, sens, duchowość i egzystencja
  12.1 Zakres
  12.2 Rozdzielenie doświadczenia od interpretacji
  12.3 Wskaźniki rozwoju świadomości
  12.4 Ryzyka
13.  Twórczość, praca, mistrzostwo i wkład
  13.1 Wymiary
  13.2 Oddzielenie produktywności od wartości osoby
  13.3 Cykl twórczy
14.  Systemy interpretacyjne i symboliczne
  14.1 Status epistemiczny
  14.2 Dopuszczalne zastosowania
  14.3 Niedopuszczalne zastosowania
  14.4 Procedura refleksyjna
  14.5 Human Design jako ścieżka
15.  Czas, rozwój i trajektorie
  15.1 Skale czasu
  15.2 Stan, trend i punkt zwrotny
  15.3 Etapy życia
  15.4 Regresja i kryzys
16.  Stany, cechy, wzorce i kontekst
  16.1 Reguła trzech kontekstów
  16.2 Reguła kontrprzykładu
17.  Potrzeby, zasoby, zdolności i ograniczenia
  17.1 Potrzeby
  17.2 Zasoby
  17.3 Zdolność a wykonanie
  17.4 Rezerwa i próg przeciążenia
18.  Sieć połączeń i pętle sprzężenia zwrotnego
  18.1 Typy relacji
  18.2 Pętle wzmacniające
  18.3 Zasada efektów wtórnych
19.  Pomiar, obserwacja i reprezentacja danych
  19.1 Źródła danych
  19.2 Metadane obowiązkowe
  19.3 Rozdzielenie danych od wniosku
  19.4 Minimalizacja pomiaru
20.  Wnioskowanie, pewność i sprzeczności
  20.1 Poziomy pewności hipotezy użytkownika
  20.2 Sprzeczne dane
  20.3 Brakujące dane
  20.4 Prawo użytkownika do korekty
21.  Personalizacja i ścieżki rozwoju
  21.1 Elementy personalizacji
  21.2 Tryby użytkownika
  21.3 Minimalna skuteczna personalizacja
  21.4 Prawo do resetu modelu
22.  Granice zdrowia, rozwoju i pomocy specjalistycznej
  22.1 Trzy tryby działania
  22.2 Przykładowe sygnały eskalacyjne
  22.3 Zasada niepatologizowania
23.  Aktualizacja modelu i uczenie się użytkownika
  23.1 Cykl aktualizacji
  23.2 Wersjonowanie
  23.3 Wygaszanie danych
  23.4 Uczenie się z braku efektu
24.  Interfejsy z pozostałymi warstwami Human OS
  24.1 Kontrakt minimalny
25.  Ryzyka modelu, uprzedzenia i tryby awarii
  25.1 Zakazane wnioski
26.  Zarządzanie modelem i odpowiedzialność
  26.1 Role
  26.2 Zmiana ontologii
  26.3 Zmiany chronione
27.  Kryteria akceptacji Warstwy 2

Załączniki (A–G):
  A. Ontologia skrócona
  B. Karta domeny
  C. Karta hipotezy o użytkowniku
  D. Pytania onboardingowe
  E. Lista kontrolna zgodności modelu
  F. Otwarte pytania do wersji 0.2
  G. Deklaracja Modelu Człowieka
```

---

## Dodatkowe obserwacje istotne dla audytu

- **Brak numeracji ADR** i brak jakiegokolwiek odniesienia do zewnętrznych ADR — tak samo jak
  Warstwa 6. Jeśli Reconstruction Audit ma zaimportować decyzje z tego dokumentu do
  `docs/adr/` (wzorem `ADR-HUB-*`, `ADR-CORE-*`), trzeba je dopiero sformułować na podstawie
  aksjomatów (sekcja 1), architektury wielorzędowej (sekcja 2) i kryteriów akceptacji (sekcja
  27) — nie istnieją gotowe w źródle.
- Dokument jawnie deklaruje status **"Wersja 0.1 – model bazowy"**, "Projekt do iteracji,
  walidacji i zatwierdzenia" — deklaratywnie niedojrzały/niewalidowany, spójnie z resztą
  projektu (BETA, brak niezależnego audytu bezpieczeństwa wg README repo kodu).
  - Załącznik F ("Otwarte pytania do wersji 0.2") zawiera 14 nierozstrzygniętych pytań
    metodologicznych/etycznych (minimalny zestaw domen, wygaszanie danych, mierzenie rozwoju
    świadomości bez hierarchii duchowej, testowanie uprzedzeń wobec wieku/płci/kultury/statusu
    ekonomicznego/neuroróżnorodności, przenoszalność modelu między systemami itd.) —
    potencjalne materiały do przyszłych ADR-ów lub sekcji "Limitations/uncertainty" wymaganej
    przez `CONTRIBUTING.md`.
- **Brak skali kodowej ryzyka** w stylu Warstwy 6 (XP/SE/EC/BL/MQ/PF/DQ/CA/PE) — Warstwa 2 nie
  wprowadza własnych liter/kodów operacyjnych. Jej bramy bezpieczeństwa są opisowe (trzy tryby
  działania: Rozwój i dobrostan / Wsparcie przy ograniczeniu / Bezpieczeństwo i eskalacja).
  Skala R0–R4 z Konstytucji (wg CLAUDE.md tego repo) także nie występuje w tym pliku.
- **Rozbieżność potencjalna z kodem `hos_engine/human_model.py`**: dokument wymaga per-rekord
  pól `source` (nie tylko `source_id`), `context`, `quality`/`unit` i `consent_scope`, których
  brak w obecnym `HumanRecord`; dokument opisuje pewność jako 5-poziomową skalę słowną (0–4),
  podczas gdy kod używa ciągłego `confidence: float` w [0,1]; dokument sugeruje bogatszy zestaw
  statusów hipotezy (Aktywna/odrzucona/wsparta/wygasła — Załącznik C) niż kodowy
  `RecordStatus` (ACTIVE/CONTESTED/SUPERSEDED/DELETED). Są to obserwacje do odnotowania, nie
  rozstrzygnięcia — flagowane zgodnie z poleceniem zadania.
- Warstwa 2 explicite nazywa siebie "Modelem osoby" tylko w karcie nagłówkowej Warstwy 6 (nie w
  swojej własnej karcie, gdzie widnieje tylko jako dokument podrzędny Warstwie 1) — w swoim
  własnym tekście nazywa się po prostu "Model Człowieka" lub "Modelem".
