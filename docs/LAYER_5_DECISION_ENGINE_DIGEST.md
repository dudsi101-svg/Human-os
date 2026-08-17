# Digest: HUMAN OS — WARSTWA 5 — SILNIK DECYZJI I REKOMENDACJI

**Status:** rozbiór strukturalny (nie parafraza) źródła dostarczonego przez founder-a
2026-08-15 — `Human_OS_Warstwa_5_Silnik_Decyzji_i_Rekomendacji_v0_1.docx`. Patrz
`docs/FOUNDER_REVIEW_2026-08-15.md`, sekcja "Czwarta tura", po kontekst i listę
`ADR-DECISION-001..005` sformułowanych na podstawie tego rozbioru. Oryginalny plik DOCX
pozostaje jedynym rozstrzygającym źródłem w razie wątpliwości (`02_Source_Truth_Protocol`).

> **Weryfikacja względem bajtów źródła (2026-08-17):** founder dostarczył
> oryginalny DOCX do sesji roboczej. Sekcje 5.2 (IQ0–IQ5), 6.1 (klasy
> intencji DI-1..DI-8) i 8.2 (AR0–AR5) odczytano bezpośrednio ze źródła —
> pełne tabele semantyk przeniesiono do
> `docs/DI_IQ_AR_CALIBRATION_PROPOSAL.md` (v0.2). Digest w tych punktach
> był poprawny, lecz niekompletny (streszczał skraje). Pozostałe sekcje
> digestu nie były w tym przebiegu weryfikowane linia po linii.

Źródło: ekstrakcja pandoc z DOCX,
plik `warstwa5.txt` (3048 linii tekstu jawnego). Cały plik został przeczytany od
początku do końca (linie 1–3047) w sześciu blokach, dodatkowo zweryfikowany
wyszukiwaniami `grep` po wzorcach `ADR-`, `nie ma prawa|nie wolno|zabrania się|zakaz`,
`Hub|Digital Twin|Knowledge Graph` i `R0-R4` na całym pliku.

Motto dokumentu (linie 36–37): *"Dobra decyzja nie jest wyrokiem algorytmu. Jest
przejrzystym, możliwym do zakwestionowania wyborem dokonanym wspólnie z
użytkownikiem."*

Warstwa 5 sytuuje się bezpośrednio przed już przetworzoną Warstwą 6 (Silnik
Eksperymentów): Warstwa 5 zamienia cel/kontekst/wiedzę w rekomendowaną decyzję;
Warstwa 6 zamienia zaakceptowaną rekomendację w wykonywany, monitorowany
eksperyment. Ten digest celowo nie kopiuje treści digestu Warstwy 6
(`docs/LAYER_6_EXPERIMENT_ENGINE_DIGEST.md`), a jedynie powiela jego strukturę
8 sekcji dla spójności formatu.

---

## 1. Metadane / nagłówek dokumentu (sekcja 0. Karta dokumentu)

Tabela nagłówkowa (linie 10–34):

| Pole | Wartość |
|---|---|
| Wersja | 0.1 - model bazowy |
| Status | Projekt do iteracji, testów, walidacji i audytu |
| Zakres | Cele, warianty, bramy bezpieczeństwa, priorytety, rekomendacje, wyjaśnienia i eskalacja |
| Dokument nadrzędny | Warstwa 1 - Konstytucja i Wartości |
| Model osoby | Warstwa 2 - Model Człowieka |
| Źródło wiedzy | Warstwa 3 - Mapa Wiedzy i Sygnatura Informacji |
| Kontekst osobisty | Warstwa 4 - Model Użytkownika i Cyfrowy Profil |
| Właściciel dokumentu | Zespół założycielski Human OS |
| Data | 2026-07-20 |

Uwaga: w przeciwieństwie do Warstwy 6 (której karta dokumentu dodatkowo wskazuje
"Decyzja wejściowa: Warstwa 5"), karta Warstwy 5 **nie wymienia Warstwy 6** jako
wiersza tabeli nagłówkowej — relacja z Warstwą 6 jest opisana dopiero w sekcji 0.4
(patrz sekcja 6 niżej) i w sekcji 41 (interfejsy).

**Cel dokumentu** (0.1, linie 44–52): Warstwa 5 "odpowiada za rozpoznanie problemu
decyzyjnego, wygenerowanie możliwych dróg, odrzucenie wariantów niedopuszczalnych,
ocenę pozostałych możliwości, przedstawienie alternatyw oraz zapisanie
uzasadnienia". Zastrzeżenie: "Nie ma ona prawa samodzielnie definiować dobra
użytkownika ani ukrywać niepewności."

**Zasada nadrzędna Warstwy 5** (ramka, linie 54–61): *"Żadna rekomendacja nie
może powstać wyłącznie dlatego, że algorytm potrafi ją wygenerować. Musi istnieć
jawny cel, wystarczający kontekst, dopuszczalny profil ryzyka, sensowna możliwość
pomiaru oraz realna możliwość odmowy lub zmiany decyzji przez użytkownika."*

**Zakres obowiązywania** (0.2, linie 64–82):
- Obejmuje: interpretację celu, budowanie wariantów, bramy bezpieczeństwa,
  priorytetyzację, wyjaśnienie, decyzję o wstrzymaniu oraz eskalację do człowieka.
- Obowiązuje: twórców modeli AI, projektantów produktu, ekspertów domenowych,
  architektów danych, zespoły bezpieczeństwa, partnerów i audytorów.
- Nie obejmuje: pełnej bazy wiedzy, tworzenia profilu użytkownika, wykonania
  eksperymentu ani agregacji rezultatów społeczności — odpowiadają za nie inne
  warstwy.
- Nie zastępuje: diagnozy medycznej, porady prawnej lub finansowej,
  odpowiedzialności specjalisty ani osobistego osądu użytkownika.
- Podlega: Konstytucji Human OS, prawom użytkownika, zasadzie minimalnej
  ingerencji i progom dowodowym zależnym od ryzyka.

**Test nadrzędny** (0.5, linie 163–169) — brama publikacji rekomendacji:
> "Jeżeli system nie potrafi odpowiedzieć: 'jaki cel realizuje ten wybór?',
> 'dlaczego ten wariant jest dopuszczalny?', 'co może pójść źle?', 'jakie są
> alternatywy?', 'jakiej informacji brakuje?', 'jak użytkownik może odmówić?'
> oraz 'kiedy należy przerwać lub ponownie ocenić decyzję?' - rekomendacja nie
> może zostać opublikowana."

Ten test jest strukturalnym odpowiednikiem "testu nadrzędnego" z Warstwy 6 (0.5)
— identyczny wzorzec bramkujący ("jeżeli system nie potrafi wyjaśnić X, Y nie
może zostać uruchomione/opublikowane"), zastosowany tu do publikacji rekomendacji
zamiast do uruchomienia eksperymentu.

---

## 2. Nazwane decyzje architektoniczne w stylu ADR

**Brak.** Przeszukano cały dokument (`grep -i "ADR-"` na wszystkich 3048 liniach)
— nie znaleziono ani jednego wystąpienia wzorca `ADR-`. Tak jak w Warstwie 6,
dokument nie zawiera dedykowanej sekcji z listą ADR i nie formalizuje decyzji w
formacie ADR z numeracją, mimo że jest dokumentem specyfikacyjnym o podobnej
skali (14 aksjomatów w sekcji 1, kryteria akceptacji w sekcji 47, deklaracja w
Załączniku Q). Jeśli "Reconstruction Audit"/nowe ADR mają odnosić się do tego
dokumentu, trzeba je sformułować od zera.

Najbliższe odpowiedniki "decyzji architektonicznych":
- 14 aksjomatów w sekcji 1 (linie 175–244) — zasady wiążące każdy wybór, ranking,
  rekomendację i odmowę;
- sekcja 42 "Referencyjna architektura techniczna" (14 modułów systemowych,
  linie 2219–2280);
- sekcja 47 "Kryteria akceptacji Warstwy 5" (13-punktowa lista bramkowa,
  linie 2506–2548).

---

## 3. Kluczowe encje / kontrakty danych

### 3.1 Ontologia obiektów decyzyjnych (sekcja 4, linie 402–457)

Tabela "Obiekt / Pola minimalne / Relacje":

| Obiekt | Pola minimalne | Relacje |
|---|---|---|
| DecisionRequest | właściciel, treść, domena, czas, pilność, źródło | Goal, ContextSnapshot |
| Goal | wynik, znaczenie, horyzont, kryterium sukcesu, priorytet | Value, Constraint, Metric |
| ContextSnapshot | stan, data, dane, jakość, zdarzenia, zasoby | UserModel, Observation |
| Constraint | typ, twardość, źródło, okres ważności | Candidate, Risk, Consent |
| Candidate | opis, mechanizm, dawka/zakres, wymagania, źródło | KnowledgeSignature, DecisionProfile |
| Exclusion | powód, próg, dowód, możliwość odwołania | Candidate, Gate |
| DecisionProfile | korzyść, ryzyko, dopasowanie, koszt, odwracalność, wykonalność | Candidate, Goal |
| Recommendation | wariant główny, alternatywy, uzasadnienie, pewność | DecisionSnapshot |
| Abstention | powód, brakujące dane, warunki wznowienia | DecisionRequest |
| Escalation | adresat, pilność, potrzebne informacje, granice | Professional, SafetyEvent |
| DecisionSnapshot | wersje danych, modeli, reguł i treści | AuditLog |
| UserChoice | akceptacja, modyfikacja, odmowa, komentarz | Recommendation, UserModel |
| ReviewTrigger | czas, zdarzenie, próg, działanie po przekroczeniu | Experiment, Recommendation |

**4.1 Identyfikowalność** (linie 459–464): każdy obiekt ma stabilny identyfikator,
wersję, datę utworzenia, właściciela odpowiedzialności i źródło. Obiekty usunięte
z aktywnego procesu pozostają w audycie w zakresie wymaganym prawem i zgodą, lecz
"nie mogą potajemnie wpływać na nowe decyzje".

**4.2 Zakaz ukrytego scalania / "Zakaz obiektu-wyroku"** (ramka, linie 466–476):
system nie może przechowywać pojedynczego pola typu „użytkownik jest
niezdyscyplinowany” albo „interwencja jest dobra” — takie skróty muszą zostać
rozłożone na obserwacje, kontekst, hipotezę, pewność, datę ważności i możliwe
alternatywne wyjaśnienia. (Bezpośredni odpowiednik "Zakazu ukrytego scalania"
z Warstwy 6, 4.2 — ten sam wzorzec architektoniczny powtórzony na osi decyzyjnej.)

### 3.2 Kontrakt wejściowy (sekcja 5)

**5.1 Pakiet minimalny** — tabela Kategoria/Wymagane minimum/Skutek braku
(linie 483–511): Cel, Kontekst, Bezpieczeństwo, Preferencje, Wiedza, Zgoda —
każda kategoria ma zdefiniowany skutek braku (np. brak "Wiedzy" → "kandydat nie
może być rekomendowany"; brak "Zgody" → "ograniczenie lub przerwanie procesu").

**5.2 Klasy jakości wejścia IQ0–IQ5** (linie 513–545) — od IQ0 (brak istotnych
danych/dane sprzeczne → wyłącznie pytania, bezpieczeństwo lub eskalacja) do IQ5
(zweryfikowany kontekst, specjalista lub dane wysokiej jakości → złożona decyzja
z audytem i nadzorem).

### 3.3 Katalog bram twardych G0–G8 (sekcja 11.1, linie 839–879)

| Brama | Pytanie | Możliwy wynik |
|---|---|---|
| G0 - legalność i konstytucja | Czy zadanie narusza prawo, autonomię lub zakazy Human OS? | odmowa lub ograniczenie |
| G1 - zgoda | Czy użytkownik zgodził się na typ danych i działania? | doprecyzowanie lub zatrzymanie |
| G2 - tożsamość celu | Czy cel należy do użytkownika i jest zrozumiały? | pytanie lub odrzucenie celu narzuconego |
| G3 - ostre ryzyko | Czy występują czerwone flagi lub stan nagły? | eskalacja bezpieczeństwa |
| G4 - przeciwwskazania | Czy kandydat koliduje z lekami, chorobą, ciążą lub ograniczeniem? | wykluczenie albo nadzór |
| G5 - próg dowodowy | Czy poziom dowodów jest wystarczający dla skali ryzyka? | ograniczenie do edukacji lub eksperymentu |
| G6 - wykonalność bezpieczna | Czy użytkownik ma zasoby i kompetencje do prawidłowego wykonania? | uproszczenie lub specjalista |
| G7 - monitorowanie | Czy można wykryć pogorszenie i przerwać działanie? | zakaz protokołu lub dodatkowe warunki |
| G8 - wpływ na innych | Czy decyzja narusza prawa lub bezpieczeństwo osób trzecich? | modyfikacja albo odmowa |

### 3.4 Wektor profilu decyzyjnego, oś B-E-F-S-R-V-C-L-T-A (18.1, linie 1198–1232)

Korzyść (B), Dowody (E), Dopasowanie (F), Bezpieczeństwo (S), Odwracalność (R),
Wykonalność (V), Koszt (C), Uczenie (L), Czas (T), Zgodność z wartościami (A) —
każda oś ma zakres i znaczenie; "18.2 Zakaz fałszywej precyzji" zabrania
przedstawiania wyniku jako "niepodważalnego wyniku typu 87,4%".

### 3.5 Załączniki-formularze (karty pól) — pełne listy pól

- **Załącznik A — Karta żądania decyzyjnego**: ID i data, Właściciel decyzji,
  Treść żądania, Klasa intencji (DI-1..DI-8), Domena, Cel i znaczenie, Horyzont,
  Pilność, Kontekst krytyczny, Zakres zgody, Braki, Status.
- **Załącznik B — Karta kandydata**: Nazwa i opis, Typ, Cel, Źródło,
  Mechanizm/logika, Wymagania, Ryzyko, Odwracalność (RV0-RV4), Koszt, Mierniki,
  Warunki przerwania, Status bram (G0-G8).
- **Załącznik C — Karta profilu decyzyjnego**: tabela osi B/E/F/S/R/V/C/L/T/A z
  kolumnami Ocena/Podstawa/Niepewność; reguła użycia: "Karta nie jest
  kalkulatorem prawdy... Ocena musi wskazywać podstawę i niepewność."
- **Załącznik D — Snapshot decyzji**: Żądanie i cel, Kontekst, Wiedza, Kandydaci,
  Bramy, Profile, Wynik, Wyjaśnienie, Wybór użytkownika, Ewaluacja, Wersje
  techniczne.
- **Załącznik E — Lista kontrolna bram**: 10 pozycji checklisty (cel, zgoda,
  stan pilny, przeciwwskazania, próg dowodowy, zasoby/kompetencje, wykrywalność
  pogorszenia, wpływ na innych, konflikty interesów, alternatywa/odmowa).
- **Załącznik F — Szablon wyjaśnienia dla użytkownika**: Twój cel, Co uznajemy
  za główne ograniczenie, Następny krok, Dlaczego, Najważniejsze ryzyko,
  Alternatywa, Jak ocenić, Kiedy przerwać, Kiedy wrócić do decyzji, Twoja
  kontrola.
- **Załącznik G — Checklista decyzji wysokiego ryzyka**: 10 pytań (bezpieczniejszy
  wariant, najgorszy skutek, wystarczalność dowodów, specjalista, legalność,
  monitorowalność, czerwone flagi, czas na namysł, presja finansowa/społeczna,
  snapshot i zgoda).
- **Załącznik H — Karta eskalacji do specjalisty**: Powód eskalacji, Pilność,
  Cel użytkownika, Najważniejszy kontekst, Aktualne działania i leki, Wykryte
  ryzyka/interakcje, Pytania do specjalisty, Źródła i sygnatury wiedzy, Czego
  system nie wie, Zakres zgody na udostępnienie, Wynik konsultacji, Zmiana
  decyzji.
- **Załącznik I — Statusy i kody operacyjne** (zbiorcza tabela wszystkich skal
  dokumentu): Intencja DI-1..DI-8, Jakość wejścia IQ0..IQ5, Gotowość AR0..AR5,
  Odwracalność RV0..RV4, Rekomendacja RC0..RC6, Brama G0..G8, Ryzyko
  R-NISKIE..R-KRYTYCZNE, Cykl życia DRAFT..COMPLETED.
- **Załączniki J–N — scenariusze**: J (energia i sen), K (skóra i włosy), L
  (iniekcyjne GHK-Cu — wysokiego ryzyka), M (Human Design i decyzja zawodowa),
  N (konflikt celów i niska realizacja) — każdy z podsekcjami
  Żądanie/Decyzja/Uzasadnienie.
- **Załącznik O — Lista kontrolna audytu nowej funkcji** (12 pozycji).
- **Załącznik P — Otwarte pytania do wersji 0.2** (12 pytań).
- **Załącznik Q — Deklaracja Silnika Decyzji** (patrz sekcja 7 niżej, cytat
  pełny).

---

## 4. Bramy ryzyka/bezpieczeństwa i reguły eskalacji

**Uwaga terminologiczna**: dokument NIE używa skali "R0–R4" (pojęcie z
Konstytucji/Warstwy 1 wg CLAUDE.md tego repozytorium) — potwierdzone `grep`
na całym pliku, zero wystąpień "R0-R4"/"R0–R4". Warstwa 5, podobnie jak Warstwa 6,
definiuje **własny, odrębny zestaw skal i kodów**, zbiorczo wypisanych w
Załączniku I (linie 2796–2820):

| Obszar | Kody |
|---|---|
| Klasa intencji | DI-1 do DI-8 |
| Jakość wejścia | IQ0 do IQ5 |
| Gotowość | AR0 do AR5 |
| Odwracalność | RV0 do RV4 |
| Rekomendacja | RC0 do RC6 |
| Brama | G0 do G8 |
| Ryzyko | R-NISKIE, R-UMIARKOWANE, R-PODWYŻSZONE, R-WYSOKIE, R-KRYTYCZNE |
| Cykl życia | DRAFT, ACTIVE, ACCEPTED, MODIFIED, PAUSED, EXPIRED, WITHDRAWN, COMPLETED, REJECTED |

Uwaga dla audytu: skala ryzyka Warstwy 5 (`R-NISKIE`...`R-KRYTYCZNE`, słownie
kodowana) jest **inną taksonomią** niż zarówno konstytucyjne R0–R4, jak i
liczbowo kodowana `SE0-SE4` (zdarzenia bezpieczeństwa) z Warstwy 6 — trzecia,
odrębna skala na tej samej "osi ryzyka" pojęciowej w projekcie.

### 4.1 Wielorzędowa architektura procesu decyzyjnego R0–R9 (sekcja 3, linie 321–378)

**Uwaga o nazewnictwie**: dokument używa oznaczeń rzędów procesu "R0"–"R9" w tej
samej sekcji, w której later stosuje kompletnie inną skalę ryzyka
"R-NISKIE..R-KRYTYCZNE" (sekcja 12.2) — to są **dwa różne użycia litery "R"
w obrębie jednego dokumentu**, nie należy ich mylić z konstytucyjną skalą R0–R4
ani ze sobą nawzajem:

| Rząd | Nazwa | Pytanie kontrolne | Wynik |
|---|---|---|---|
| R0 | Brama konstytucyjna | Czy zadanie i sposób działania są zgodne z prawami użytkownika? | dopuszczenie, ograniczenie lub odmowa |
| R1 | Intencja i cel | Co użytkownik rzeczywiście próbuje zmienić lub zrozumieć? | cel, właściciel, horyzont, kryteria |
| R2 | Stan i kontekst | W jakich warunkach decyzja będzie wykonywana? | snapshot kontekstu i jakości danych |
| R3 | Mapa problemu | Co może ograniczać cel i które zależności są istotne? | hipotezy wąskiego gardła |
| R4 | Generowanie kandydatów | Jakie działania, obserwacje i alternatywy są możliwe? | zbiór kandydatów z pochodzeniem |
| R5 | Bramy twarde | Które warianty są niedopuszczalne lub wymagają eskalacji? | lista odrzuceń i warunków |
| R6 | Profil decyzyjny | Jak wyglądają korzyści, ryzyka, koszty i dopasowanie? | wektor ocen bez fałszywej precyzji |
| R7 | Priorytetyzacja | Który wariant jest najlepszym następnym krokiem? | rekomendacja, alternatywy, abstencja |
| R8 | Wyjaśnienie i zgoda | Czy użytkownik rozumie wybór i może go zmienić? | świadoma decyzja użytkownika |
| R9 | Wykonanie i sprzężenie | Jak mierzymy, przerywamy i aktualizujemy model? | kontrakt z Warstwą 6 i plan powrotu |

**3.1 Zasada nierównoważności rzędów** (linie 380–385): "Rzędy nie są punktami
jednego rankingu. Wynik wyższego etapu nie może unieważnić twardego ograniczenia
z wcześniejszej bramy." Kandydat o dużym potencjale korzyści pozostaje wykluczony,
jeśli narusza konstytucję, zgodę, prawo albo krytyczne bezpieczeństwo.

**3.2 Pętle wsteczne** (linie 387–399): brak jasnego celu cofa proces z R4 do R1;
niewystarczający kontekst cofa proces do pytań/obserwacji/pomiaru; wykryte
przeciwwskazanie może wymusić nową pulę kandydatów; odmowa użytkownika aktualizuje
preferencje, ale "nie jest automatycznie traktowana jako opór lub błąd"; wynik
eksperymentu wraca do profilu i może zmienić wagi kolejnych decyzji.

### 4.2 Model ryzyka i klasy reakcji R-NISKIE..R-KRYTYCZNE (sekcja 12, linie 895–959)

Wymiary ryzyka (12.1): Prawdopodobieństwo, Ciężkość, Odwracalność, Wykrywalność,
Czas do szkody, Ekspozycja, Interakcje, Wrażliwość osoby, Wpływ na osoby trzecie.

Klasy reakcji (12.2):

| Klasa | Charakter | Domyślna reakcja |
|---|---|---|
| R-NISKIE | łatwo odwracalne, dobrze znane, możliwe do samokontroli | normalna rekomendacja |
| R-UMIARKOWANE | wymaga monitorowania lub precyzyjnego wykonania | jawne ostrzeżenia i plan przerwania |
| R-PODWYŻSZONE | ograniczone dowody, możliwe istotne skutki | warunkowa rekomendacja lub specjalista |
| R-WYSOKIE | możliwa ciężka szkoda, trwałość lub trudne monitorowanie | eskalacja; brak samodzielnego protokołu |
| R-KRYTYCZNE | bezpośrednie niebezpieczeństwo, działanie niedopuszczalne lub stan nagły | odmowa i wskazanie pilnej pomocy |

**12.3 Ryzyko kumulacyjne**: "Niskie ryzyko pojedynczych działań nie oznacza
niskiego ryzyka ich połączenia."

### 4.3 Ścieżka decyzji wysokiego ryzyka (sekcja 28, linie 1680–1719)

**28.1 Warunki minimalne**: jasny i trwały cel; brak bezpieczniejszej alternatywy
o podobnej wartości; pełny profil ryzyka i interakcji; odpowiedni poziom dowodów
względem możliwej szkody; kompetentny specjalista jeśli wymagany; plan
monitorowania i kryteria przerwania; czas na namysł wolny od presji; oddzielna
zgoda i snapshot decyzji; **zakaz finansowego bodźca wpływającego na ranking**.

**28.2 Determinacja użytkownika**: "Determinacja może uzasadniać bardziej
szczegółowe omówienie ryzyka... Nie uzasadnia pomijania kontroli, projektowania
dawki poza kompetencjami ani normalizowania niebezpiecznej praktyki." (Ten sam
wzorzec co Warstwy 6 "34.2 Determinacja użytkownika" / "Determinacja użytkownika
nie obniża progu bezpieczeństwa".)

**28.3 Procedura redukcji szkód**: dopuszczalna, gdy użytkownik prawdopodobnie
podejmie działanie niezależnie od rekomendacji, o ile informacja "nie zwiększa
w sposób nieproporcjonalny zdolności do spowodowania ciężkiej szkody"; "Zakres
pomocy podlega Warstwie 1 i specjalistycznym politykom bezpieczeństwa."

### 4.4 Eskalacja miękka/warunkowa/twarda (27.3, linie 1662–1678)

| Typ | Znaczenie | Przykład |
|---|---|---|
| Miękka | system może kontynuować edukację, ale zaleca konsultację | złożony problem bez ostrego ryzyka |
| Warunkowa | działanie możliwe dopiero po konsultacji lub badaniu | interwencja z możliwą interakcją |
| Twarda | system przerywa protokół i kieruje do właściwej pomocy | czerwone flagi lub stan nagły |

### 4.5 Abstencja jako pełnoprawny wynik (sekcja 27, linie 1633–1660)

Powody abstencji (27.1): brak jasnego celu/właściciela decyzji; niewystarczające
dane krytyczne; nierozstrzygnięty konflikt wartości; sprzeczne dowody bez
bezpiecznego wariantu; brak możliwości monitorowania; zbyt duże ryzyko lub
nieodwracalność; problem przekraczający kompetencje systemu; podejrzenie stanu
pilnego albo kryzysu.

### 4.6 Skala odwracalności RV0-RV4 (16.1, linie 1124–1147)

Od RV0 (natychmiast odwracalne, np. zmiana kolejności zadania) do RV4
(nieodwracalne albo potencjalnie trwałe, np. decyzje chirurgiczne, prawne lub
życiowe wysokiego wpływu).

### 4.7 Klasy rekomendacji RC0–RC6 (24.1, linie 1479–1509)

Od RC0 (brak rekomendacji) przez RC3 (prosty krok niskiego ryzyka), RC4
(eksperyment osobisty), RC5 (rekomendacja warunkowa) do RC6 (eskalacja lub
bezpieczna odmowa).

---

## 5. Kluczowa terminologia (0.3 "Podstawowe terminy", linie 84–142)

| Termin | Definicja |
|---|---|
| Żądanie decyzyjne | Jawna lub rozpoznana potrzeba wyboru, rozwiązania problemu albo ustalenia następnego kroku. |
| Cel operacyjny | Konkretny rezultat, kierunek lub zdolność, dla których można określić horyzont i kryteria sukcesu. |
| Kandydat | Możliwa interwencja, obserwacja, pytanie, konsultacja, zmiana kolejności albo świadome niedziałanie. |
| Brama twarda | Warunek, którego niespełnienie wyklucza wariant niezależnie od jego potencjalnych korzyści. |
| Preferencja miękka | Czynnik wpływający na kolejność wariantów, ale nie powodujący automatycznego wykluczenia. |
| Profil decyzyjny | Wielowymiarowa ocena kandydata: korzyść, ryzyko, dopasowanie, koszt, odwracalność, wykonalność i wartość uczenia. |
| Rekomendacja | Wyjaśniona propozycja działania przedstawiona użytkownikowi jako wybór, nie rozkaz. |
| Alternatywa | Inny dopuszczalny wariant o odmiennym kompromisie korzyści, ryzyka, kosztu lub wysiłku. |
| Abstencja | Świadoma decyzja systemu, by nie rekomendować działania z powodu braku podstaw, konfliktu albo nadmiernego ryzyka. |
| Eskalacja | Przekazanie decyzji do specjalisty, opiekuna, zespołu bezpieczeństwa lub użytkownika z dodatkowymi warunkami. |
| Snapshot decyzji | Niezmienny zapis danych, założeń, wersji modeli i uzasadnienia obowiązujących w chwili rekomendacji. |
| Następny najlepszy krok | Najmniejsza sensowna czynność zwiększająca szansę realizacji celu lub redukująca istotną niepewność. |

Poza tym słowniczkiem, dokument definiuje dalsze pojęcia rozproszone w treści
(nie w tabeli terminów), m.in.:
- **Wąskie gardło** (sekcja 9) — dziewięć typów: informacyjne, biologiczne,
  behawioralne, środowiskowe, poznawcze, emocjonalne, wartości, zasobowe,
  systemowe (tabela, linie 736–773).
- **Antycel** (7.3, linie 665–675) — pięć przykładów, np. "Nie pogorszyć zdolności
  do bezpiecznej pracy", "Nie utracić możliwości wycofania się bez trwałych
  konsekwencji".
- **Kandydat pozorny** (10.3, linie 821–833) — pięć wzorców fałszywie atrakcyjnych
  kandydatów (modny bez związku z celem, powtórzenie tego co już nie zadziałało,
  niemożliwy do oceny z powodu wielu równoległych zmian, koszt większy niż
  korzyść, wsparty wyłącznie marketingiem/konfliktem interesów).
- **Kontrfakt praktyczny** (33.2, linie 1898–1903) — "System nie zna z pewnością
  tego, co wydarzyłoby się bez działania" — pojęciowy odpowiednik "Kontrfaktu
  praktycznego" z Warstwy 6 (26.3), zastosowany tu do wnioskowania przyczynowego
  na poziomie decyzji.
- **Zapora epistemiczna** (30.4, linie 1794–1804, ramka "Nienaruszalna granica")
  — bezpośredni odpowiednik terminu z Warstwy 6 (32.4): "Wynik systemu
  symbolicznego może wpływać na pytania, język i dobrowolny eksperyment
  refleksyjny. Nie może obniżyć bramy bezpieczeństwa, podnieść siły dowodów
  medycznych ani automatycznie zmienić profilu ryzyka."
- **Budżet zmiany** (15.1, linie 1101–1106) — ile aktywnych zmian użytkownik może
  utrzymać bez przeciążenia; zależy od stanu, doświadczenia, obowiązków i
  wcześniejszej regularności.
- **Progressive disclosure** (25.3, linie 1574–1579) — interfejs minimalistyczny
  na pierwszym poziomie, przejrzysty po rozwinięciu; "Uproszczenie nie może
  polegać na usuwaniu ryzyka, niepewności lub alternatyw".

---

## 6. Relacje z innymi warstwami / komponentami Human OS

Podsumowanie interfejsów, sekcja 41 "Interfejsy z pozostałymi warstwami Human OS"
(linie 2179–2210), tabela "Warstwa / Dane wejściowe do Warstwy 5 / Dane
wyjściowe z Warstwy 5":

| Warstwa | Dane wejściowe do Warstwy 5 | Dane wyjściowe z Warstwy 5 |
|---|---|---|
| 1 - Konstytucja | prawa, zakazy, hierarchia wartości, reguły ryzyka | log zgodności i przypadki wymagające precedensu |
| 2 - Model Człowieka | domeny, procesy, zależności i granice interpretacji | hipotezy o wąskim gardle i wpływie między domenami |
| 3 - Mapa Wiedzy | kandydaci, dowody, ryzyko, interakcje, aktualność | zapotrzebowanie na nowe twierdzenia i sprzeczności |
| 4 - Model Użytkownika | cel, kontekst, historia, preferencje, zgody, gotowość | snapshot decyzji, nowe hipotezy i przyczyny odmowy |
| 6 - Silnik Eksperymentów | wyniki, wykonanie, działania niepożądane | hipoteza, protokół, mierniki i warunki przerwania |
| 7 - Inteligencja Zbiorowa | ustrukturyzowane wzorce odpowiedzi i bezpieczeństwa | anonimizowane wyniki decyzji w dozwolonym zakresie |

Dodatkowe szczegóły relacyjne rozproszone w tekście (sekcja 0.4 "Odpowiedzialność
Warstwy 5", linie 144–162):
- **Warstwa 1 (Konstytucja)**: "Dokument nadrzędny" (nagłówek 0.1). "Każdy wynik
  przepuszcza przez prawa i zakazy Warstwy 1" (0.4).
- **Warstwa 2 (Model Człowieka)**: "Model osoby" (nagłówek). "Interpretując
  osobę, korzysta z domen i relacji z Warstwy 2, ale nie redukuje jej do
  pojedynczej cechy" (0.4).
- **Warstwa 3 (Mapa Wiedzy i Sygnatura Informacji)**: "Źródło wiedzy" (nagłówek).
  "Przyjmuje twierdzenia, poziomy dowodów, ryzyko, interakcje i status
  aktualności z Warstwy 3" (0.4). Kandydaci mają "pochodzenie w Mapie Wiedzy
  albo status hipotezy roboczej" (kryteria akceptacji 47).
- **Warstwa 4 (Model Użytkownika i Cyfrowy Profil)**: "Kontekst osobisty"
  (nagłówek). "Przyjmuje cele, ograniczenia, stan, historię i preferencje z
  Warstwy 4" (0.4). "Przekazuje Warstwie 4 decyzję użytkownika, przyjęte
  założenia oraz informacje wymagające aktualizacji profilu" (0.4).
- **Warstwa 6 (Silnik Eksperymentów)**: nie wymieniona w karcie dokumentu (0.1),
  ale explicite w 0.4: "Przekazuje Warstwie 6 rekomendację, hipotezę, protokół,
  kryteria przerwania i plan pomiaru." W sekcji 32.1 "Pętla aktualizacji" (krok 3,
  linia 1853): "Przekaż plan do Silnika Eksperymentów." Rząd R9 architektury
  wielorzędowej (3, linia 374–377) produkuje "kontrakt z Warstwą 6 i plan
  powrotu". Spójne z tabelą interfejsów Warstwy 6 (sekcja 38 tamtego dokumentu),
  gdzie Warstwa 5 figuruje jako "Decyzja wejściowa".
- **Warstwa 7 ("Inteligencja zbiorowa")**: wspomniana wyłącznie w tabeli
  interfejsów sekcji 41 (jak w Warstwie 6) — przyjmuje "ustrukturyzowane wzorce
  odpowiedzi i bezpieczeństwa", zwraca "anonimizowane wyniki decyzji w dozwolonym
  zakresie". Nie jest opisana nigdzie indziej w dokumencie z nazwy własnej — jak
  w Warstwie 6, traktować jako odniesienie do warstwy poza zakresem tego pliku.
- **Hub / Digital Twin / Knowledge Graph** — te nazwy własne (używane w
  repozytorium kodu: `hub/`, `knowledge_graph.py`) **nie pojawiają się** w tym
  dokumencie (potwierdzone `grep` na całym pliku — zero wystąpień). Tak samo jak
  w Warstwie 6, dokument odnosi się do "Mapy Wiedzy" (Warstwa 3) jako źródła
  wiedzy, a nie do "Knowledge Graph"/"Hub" nazwanych explicite — nie zakładać
  1:1 mapowania na moduły kodu bez dodatkowej weryfikacji.
- **Human Design / astrologia / systemy interpretacyjne**: odrębna sekcja 30
  (linie 1755–1804) — dopuszczalny *przedmiot* refleksji/generowania pytań, ale
  odgrodzony "zaporą epistemiczną" (30.4) od diagnoz, przeciwwskazań biologicznych
  i przewidywania zdarzeń jako faktów (30.2). Dokładny paralelny wzorzec do
  Warstwy 6, sekcja 32.

**41.1 Kontrakt błędu** (linie 2212–2217): "Każda warstwa musi potrafić zwrócić
stan 'brak danych', 'sprzeczność', 'nieaktualne' lub 'niedozwolone', zamiast
wymuszać wartość domyślną. Silnik Decyzji nie może przekształcać błędu interfejsu
w pewną rekomendację." (Ten sam wzorzec co Warstwy 6 "38.1 Kontrakt błędu".)

---

## 7. Explicit prohibitions ("nie ma prawa" / "nie wolno" / "zabrania się")

Dokument **nie zawiera** frazy "zabrania się" (0 wystąpień, `grep -i` na całym
pliku). Pełna lista dosłownych cytatów z "nie ma prawa" / "nie wolno" (wyszukano
wzorce case-insensitive w całym pliku):

1. (linia 51, sekcja 0.1, Cel dokumentu) — *"Nie ma ona [Warstwa 5] prawa
   samodzielnie definiować dobra użytkownika ani ukrywać niepewności."*
2. (linia 182, Aksjomat 2 "Bezpieczeństwo nie jest punktem w rankingu") —
   *"Twardego przeciwwskazania nie wolno skompensować wysoką atrakcyjnością,
   popularnością ani przewidywaną korzyścią."*
3. (linia 837, nagłówek sekcji 11 "Bramy twarde, wykluczenia i warunki
   dopuszczenia") — *"Filtry, których nie wolno zastąpić rankingiem korzyści."*
4. (linia 1244, 18.3 "Model ograniczeń przed użytecznością") — *"Funkcja
   użyteczności nie ma prawa przywrócić kandydata wykluczonego przez
   bezpieczeństwo lub brak zgody."*
5. (linia 1874, 32.3 "Efekt uboczny jako priorytet") — *"Sygnały pogorszenia i
   zdarzenia niepożądane mają osobny strumień, którego nie wolno ukrywać w
   średniej poprawie."*

Dodatkowe zdania z tytułami sekcji "Zakaz ..." (nie zawsze dosłownie zawierają
słowo "wolno"/"prawo", ale formułują wiążący zakaz):
- **4.2 "Zakaz ukrytego scalania" / ramka "Zakaz obiektu-wyroku"** (linie
  466–476) — "System nie może przechowywać pojedynczego pola typu 'użytkownik
  jest niezdyscyplinowany' albo 'interwencja jest dobra'."
- **18.2 "Zakaz fałszywej precyzji"** (linie 1234–1239) — liczby dopuszczalne
  tylko z opisem źródła i zakresem niepewności, "nie sugerują większej
  dokładności niż dane".
- **28.1** (linia 1704) — *"zakaz finansowego bodźca wpływającego na ranking"*
  jako jeden z warunków minimalnych ścieżki wysokiego ryzyka.
- **25.2 "Zakazane wzorce interfejsu"** (linie 1558–1572) — siedem zakazanych
  wzorców UI, m.in. "domyślna zgoda na działania wysokiego wpływu", "ukrywanie
  opcji odmowy lub anulowania", "wstydzące komunikaty o utraconej serii",
  "używanie autorytetu AI zamiast uzasadnienia".
- **40.2 "Funkcje niedozwolone bez dodatkowej kontroli"** (rola AI, linie
  2153–2165) — sześć pozycji, patrz sekcja "Rola AI" niżej.
- **23.2 "Co nie może się personalizować w dół"** (linie 1450–1460) — pięć
  pozycji: minimalne standardy świadomej zgody; twarde przeciwwskazania i
  ochrona osób trzecich; obowiązek ujawnienia niepewności i konfliktów
  interesów; "zakaz manipulacji i uzależniającego projektowania"; wymóg
  specjalisty przy określonych klasach ryzyka.
- **30.2 "Niedopuszczalne zastosowania"** (Human Design/astrologia, linie
  1772–1785) — sześć pozycji, m.in. "diagnoza zdrowotna lub psychologiczna",
  "wykluczenie leczenia, badania lub bezpiecznej praktyki", "ustalanie
  przeciwwskazań biologicznych".
- **30.4 "Zapora epistemiczna" / ramka "Nienaruszalna granica"** (linie
  1794–1804) — "Nie może obniżyć bramy bezpieczeństwa, podnieść siły dowodów
  medycznych ani automatycznie zmienić profilu ryzyka."
- **31.2 "Niedopuszczalny wpływ"** (wiedza zbiorowa, linie 1823–1833) — pięć
  pozycji, m.in. "popularność jako substytut dowodu", "automatyczne
  przenoszenie wyniku grupy na konkretną osobę".
- **37.3 "Metryki antycelowe"** (linie 2053–2064) — pięć antymetryk niedozwolonych
  jako cel systemu, m.in. "liczba sprzedanych produktów", "częstotliwość
  powiadomień".
- **44.2 "Antymetryki"** (linie 2376–2388) — sześć pozycji, m.in. "maksymalizacja
  liczby zaakceptowanych rekomendacji", "utrzymywanie serii za wszelką cenę".
- Załącznik L (scenariusz GHK-Cu, iniekcja wysokiego ryzyka, linie 2899–2900) —
  *"Silnik wybiera RC6: nie tworzy samodzielnego schematu iniekcji"* — analogiczny
  do zdania z Warstwy 6 ("Warstwa 6 nie generuje dawkowania, schematu iniekcji
  ani instrukcji wykonawczej").

Inne silne normatywne zdania warte odnotowania (bez dokładnie "nie wolno", ale
równie wiążące, w formacie wypunktowanych "granic"):
- **2.3 "Problemy poza autonomicznym zakresem systemu"** (linie 306–319) — pięć
  wypunktowań, np. "Rozstrzyganie stanów nagłych, diagnozowanie chorób lub
  modyfikowanie leczenia bez uprawnionego specjalisty", "Podejmowanie
  nieodwracalnych decyzji za użytkownika", "Wydawanie poleceń dotyczących osób
  trzecich bez ich zgody i danych".
- **6.3 "Presja na potwierdzenie" / ramka "Reguła niezależności"** (linie
  609–618) — *"Determinacja użytkownika może zmienić sposób rozmowy i potrzebny
  poziom wsparcia, ale nie może podnieść oceny dowodów, usunąć przeciwwskazań ani
  wymusić stworzenia procedury, której głównym efektem byłoby zwiększenie ryzyka
  ciężkiej szkody."*
- **17.2 "Eksperyment nie jest wymówką" / ramka "Granica eksperymentalności"**
  (linie 1177–1184) — *"Etykieta 'eksperyment' nie obniża standardu
  bezpieczeństwa."*
- **35.2 "Rekomendacje relacyjne"** (linie 1979–1992) — "nie mogą diagnozować
  partnera lub pracownika bez jego udziału", "nie mogą używać prywatnych danych
  jednej osoby do ukrytej manipulacji drugą".
- **37.1 "Zasady" (integralność komercyjna)** (linie 2032–2045) — "płatność
  dostawcy nie może podnosić profilu decyzyjnego", "model biznesowy nie może
  nagradzać większej liczby interwencji kosztem minimalizmu".
- (Deklaracja, Załącznik Q, linia ~3037–3047) — *"Human OS nie podejmuje życia
  za użytkownika."*

---

## 8. Struktura dokumentu (spis treści wg nagłówków)

```
HUMAN OS — WARSTWA 5 — SILNIK DECYZJI I REKOMENDACJI

0.   Karta dokumentu i sposób stosowania
  0.1  Cel dokumentu
  0.2  Zakres obowiązywania
  0.3  Podstawowe terminy
  0.4  Odpowiedzialność Warstwy 5
  0.5  Test nadrzędny
1.   Aksjomaty Silnika Decyzji (14 aksjomatów)
2.   Rola, granice i klasy problemów decyzyjnych
  2.1  Główne role
  2.2  Klasy problemów
  2.3  Problemy poza autonomicznym zakresem systemu
3.   Wielorzędowa architektura procesu decyzyjnego (R0..R9)
  3.1  Zasada nierównoważności rzędów
  3.2  Pętle wsteczne
4.   Ontologia obiektów decyzyjnych
  4.1  Identyfikowalność
  4.2  Zakaz ukrytego scalania
5.   Kontrakty wejściowe i jakość danych
  5.1  Pakiet minimalny
  5.2  Klasy jakości wejścia IQ0-IQ5
  5.3  Braki i sprzeczności
6.   Rozpoznanie żądania decyzyjnego
  6.1  Klasy intencji (DI-1..DI-8)
  6.2  Intencje mieszane
  6.3  Presja na potwierdzenie
7.   Model celu i kryteriów sukcesu
  7.1  Składniki celu
  7.2  Cele instrumentalne i wartości końcowe
  7.3  Antycele
8.   Ocena stanu, kontekstu i gotowości
  8.1  Snapshot kontekstu
  8.2  Gotowość AR0-AR5
  8.3  Niewykonanie nie jest etykietą
9.   Mapa problemu i wykrywanie wąskiego gardła
  9.1  Typy wąskich gardeł
  9.2  Wskaźnik dźwigni
  9.3  Hipotezy konkurencyjne
10.  Generowanie kandydatów
  10.1 Źródła kandydatów
  10.2 Wymóg różnorodności
  10.3 Kandydaci pozorni
11.  Bramy twarde, wykluczenia i warunki dopuszczenia
  11.1 Katalog bram (G0-G8)
  11.2 Twarde i warunkowe wykluczenie
  11.3 Prawo do odwołania
12.  Model ryzyka i możliwej szkody
  12.1 Wymiary ryzyka
  12.2 Klasy reakcji na ryzyko (R-NISKIE..R-KRYTYCZNE)
  12.3 Ryzyko kumulacyjne
13.  Niepewność i wartość informacji
  13.1 Typy niepewności
  13.2 Wartość informacji
  13.3 Próg działania
14.  Oczekiwana korzyść i dopasowanie osobiste
  14.1 Wymiary korzyści
  14.2 Dopasowanie
  14.3 Populacja a jednostka
15.  Koszt, obciążenie i koszt alternatywny
  15.1 Budżet zmiany
  15.2 Koszty ukryte
16.  Odwracalność, wykrywalność i zdolność powrotu
  16.1 Skala odwracalności RV0-RV4
  16.2 Zdolność odzyskania kontroli
17.  Wartość uczenia i eksperymentalność
  17.1 Wartość uczenia
  17.2 Eksperyment nie jest wymówką
  17.3 Negatywny wynik
18.  Profil decyzyjny i model oceny kandydatów
  18.1 Wektor decyzji (osie B-E-F-S-R-V-C-L-T-A)
  18.2 Zakaz fałszywej precyzji
  18.3 Model ograniczeń przed użytecznością
  18.4 Wagi użytkownika
19.  Priorytetyzacja i minimalna skuteczna zmiana
  19.1 Reguła następnego najlepszego kroku
  19.2 Kiedy rekomendować więcej niż jedną zmianę
  19.3 Minimalizm adaptacyjny
20.  Kolejność, zależności i portfel interwencji
  20.1 Typy zależności
  20.2 Limity aktywnych interwencji
  20.3 Długie ścieżki
21.  Konflikty celów, wartości i kompromisy
  21.1 Typy konfliktów
  21.2 Procedura rozstrzygnięcia
  21.3 Konflikt nierozstrzygnięty
22.  Czas, pilność i moment decyzji
  22.1 Horyzonty
  22.2 Pilność pozorna
  22.3 Okno gotowości
23.  Personalizacja i adaptacja logiki wyboru
  23.1 Co może się personalizować
  23.2 Co nie może się personalizować w dół
  23.3 Eksploracja kontra eksploatacja
  23.4 Prawo do nowego początku
24.  Klasy rekomendacji i tryby działania systemu
  24.1 Klasy RC0-RC6
  24.2 Tryby użytkowe
25.  Architektura wyboru i interfejs użytkownika
  25.1 Widok podstawowy
  25.2 Zakazane wzorce interfejsu
  25.3 Progressive disclosure
26.  Protokół wyjaśnienia rekomendacji
  26.1 Obowiązkowe elementy
  26.2 Poziomy szczegółowości (L1-L4)
  26.3 Wyjaśnienie negatywne
27.  Abstencja, odmowa i eskalacja
  27.1 Powody abstencji
  27.2 Język odmowy
  27.3 Eskalacja miękka i twarda
28.  Ścieżka decyzji wysokiego ryzyka
  28.1 Warunki minimalne
  28.2 Determinacja użytkownika
  28.3 Procedura redukcji szkód
29.  Rola specjalistów i decyzje wspomagane
  29.1 Funkcje specjalisty
  29.2 Pakiet dla specjalisty
  29.3 Rozbieżność opinii
30.  Human Design, astrologia i systemy interpretacyjne
  30.1 Dopuszczalne zastosowania
  30.2 Niedopuszczalne zastosowania
  30.3 Logika hipotezy refleksyjnej
  30.4 Zapora epistemiczna
31.  Wiedza zbiorowa i wyniki innych użytkowników
  31.1 Dopuszczalny wpływ
  31.2 Niedopuszczalny wpływ
  31.3 Podobieństwo użytkowników
32.  Sprzężenie zwrotne i uczenie z rezultatu
  32.1 Pętla aktualizacji
  32.2 Wierność wykonania
  32.3 Efekt uboczny jako priorytet
33.  Przyczynowość, korelacja i kontrfakty
  33.1 Minimalne pytania przyczynowe
  33.2 Kontrfakt praktyczny
  33.3 Aktualizacja bez nadmiernego uczenia
34.  Starzenie się decyzji, drift i wycofanie
  34.1 Przyczyny wygaśnięcia
  34.2 Statusy życia rekomendacji
  34.3 Rollback
35.  Decyzje współdzielone i wpływ na innych
  35.1 Właściciele i interesariusze
  35.2 Rekomendacje relacyjne
36.  Równość, uprzedzenia i sprawiedliwość
  36.1 Źródła uprzedzeń
  36.2 Zasada równoważnej ochrony
  36.3 Audyt podgrup
37.  Integralność komercyjna i konflikty interesów
  37.1 Zasady
  37.2 Konflikt eksperta
  37.3 Metryki antycelowe
38.  Prywatność i minimalizacja w procesie decyzji
  38.1 Zasada potrzeby
  38.2 Tryb prywatny
  38.3 Dane wrażliwe i wnioskowane
39.  Audytowalność, log decyzji i prawo do rekonstrukcji
  39.1 Zawartość snapshotu
  39.2 Log dla użytkownika i log techniczny
  39.3 Prawo do korekty
40.  Rola AI w Silniku Decyzji
  40.1 Funkcje dozwolone
  40.2 Funkcje niedozwolone bez dodatkowej kontroli
  40.3 Architektura z ograniczeniami
  40.4 Kalibracja
41.  Interfejsy z pozostałymi warstwami Human OS
  41.1 Kontrakt błędu
42.  Referencyjna architektura techniczna
  42.1 Moduły
  42.2 Deterministyczne reguły i modele probabilistyczne
  42.3 Tryb degradacji
43.  Testowanie, walidacja i symulacje
  43.1 Poziomy testów
  43.2 Złote scenariusze
  43.3 Test zrozumienia
44.  Metryki jakości Silnika Decyzji
  44.1 Metryki podstawowe
  44.2 Antymetryki
45.  Tryby awarii i ryzyka systemowe
  45.1 Czerwone flagi organizacyjne
46.  Zarządzanie, role i odpowiedzialność
  46.1 Role
  46.2 Zmiany wysokiego wpływu
  46.3 Precedensy
47.  Kryteria akceptacji Warstwy 5

Załączniki (A–Q):
  A. Karta żądania decyzyjnego
  B. Karta kandydata
  C. Karta profilu decyzyjnego
  D. Snapshot decyzji
  E. Lista kontrolna bram
  F. Szablon wyjaśnienia dla użytkownika
  G. Checklista decyzji wysokiego ryzyka
  H. Karta eskalacji do specjalisty
  I. Statusy i kody operacyjne (zbiorcza tabela wszystkich skal)
  J. Scenariusz: energia i sen
  K. Scenariusz: skóra i włosy
  L. Scenariusz: iniekcyjne GHK-Cu
  M. Scenariusz: Human Design i decyzja zawodowa
  N. Scenariusz: konflikt celów i niska realizacja
  O. Lista kontrolna audytu nowej funkcji
  P. Otwarte pytania do wersji 0.2
  Q. Deklaracja Silnika Decyzji
```

Struktura jest krótsza niż Warstwa 6 (47 sekcji + 17 załączników A–Q, wobec
47 sekcji + 22 załączników A–V w Warstwie 6), ale zbudowana wg tego samego
szkieletu: karta dokumentu → aksjomaty → architektura wielorzędowa → ontologia
obiektów → kontrakty danych → logika domenowa szczegółowa → rola AI → interfejsy
z innymi warstwami → architektura techniczna → testowanie → metryki → tryby
awarii → zarządzanie → kryteria akceptacji → załączniki-formularze i scenariusze.

---

## Rola AI w Silniku Decyzji (sekcja 40, linie 2132–2177)

Motyw wiodący (nagłówek, linia 2134): "Model językowy może organizować i
tłumaczyć, ale nie jest samodzielnym źródłem prawdy ani ostatecznym arbitrem
ryzyka."

**40.1 Funkcje dozwolone** (linie 2137–2151):
- rozpoznawanie intencji i doprecyzowanie celu;
- generowanie kandydatów z zatwierdzonej Mapy Wiedzy;
- streszczanie dowodów i kompromisów;
- wykrywanie braków, sprzeczności i potencjalnych interakcji;
- personalizacja języka i formy prezentacji;
- tworzenie pytań refleksyjnych i scenariuszy alternatywnych;
- przygotowanie wyjaśnienia na podstawie jawnych reguł i danych.

**40.2 Funkcje niedozwolone bez dodatkowej kontroli** (linie 2153–2165):
- samodzielne tworzenie nowych przeciwwskazań lub dawek jako faktów;
- ukryte modyfikowanie wagi ryzyka;
- diagnozowanie na podstawie stylu wypowiedzi;
- używanie niezatwierdzonych źródeł w decyzji wysokiego wpływu;
- publikowanie rekomendacji po wykryciu konfliktu reguł;
- udawanie pewności w celu utrzymania płynności rozmowy.

**40.3 Architektura z ograniczeniami** (linie 2167–2171): "Model generatywny
powinien działać wewnątrz systemu reguł, narzędzi i walidatorów. Krytyczne bramy,
identyfikatory źródeł, klasy ryzyka i wymogi zgody nie mogą istnieć wyłącznie
w tekście promptu." — bezpośredni odpowiednik architektonicznej zasady Warstwy 6
(37.3), że logika bezpieczeństwa musi być kodowana poza samym LLM-em.

**40.4 Kalibracja** (linie 2173–2177): "Pewność językowa modelu nie może być
używana jako pewność decyzji. Ocena pewności pochodzi z jawnych danych, jakości
wiedzy, dopasowania i wyników walidacji."

Ten sam temat wzmocniony gdzie indziej w dokumencie:
- **18.3 "Model ograniczeń przed użytecznością"** — "Funkcja użyteczności nie ma
  prawa przywrócić kandydata wykluczonego przez bezpieczeństwo lub brak zgody."
- **42.2 "Deterministyczne reguły i modele probabilistyczne"** (linie 2268–2273)
  — "Twarde zakazy, zgoda i krytyczne interakcje powinny być reprezentowane w
  deterministycznych lub formalnie walidowanych regułach. Modele probabilistyczne
  mogą wspierać ranking, dopasowanie i rozpoznanie intencji, lecz ich wynik
  podlega bramom."
- **42.3 "Tryb degradacji"** (linie 2275–2280) — przy awarii modelu, integracji
  lub bazy wiedzy: "system powinien bezpiecznie ograniczyć funkcję: przejść do
  edukacji ogólnej, pokazać brak danych, zachować dostęp do historii i nie
  generować improwizowanej rekomendacji wysokiego wpływu."
- Załącznik L, scenariusz iniekcyjne GHK-Cu (linie 2899–2900): "Silnik wybiera
  RC6: nie tworzy samodzielnego schematu iniekcji" — konkretny przypadek
  ilustrujący granicę AI dla decyzji wysokiego ryzyka.

Porównanie z Warstwą 6: struktura sekcji "Rola AI" (dozwolone / niedozwolone /
architektura z ograniczeniami) jest niemal identyczna między dokumentami — ten
sam wzorzec projektowy zastosowany na dwóch różnych etapach procesu (decyzja
vs. wykonanie eksperymentu).

---

## Dodatkowe obserwacje istotne dla audytu

- **Brak numeracji ADR** i brak jakiegokolwiek odniesienia do zewnętrznych ADR —
  identycznie jak w Warstwie 6. Jeśli Reconstruction Audit ma "zaimportować"
  decyzje z tego dokumentu do `docs/adr/`, trzeba je dopiero sformułować na
  podstawie aksjomatów (sekcja 1), architektury referencyjnej (sekcja 42) i
  kryteriów akceptacji (sekcja 47) — nie istnieją w źródle gotowe do
  wyciągnięcia.
- Dokument jawnie zaznacza swój status jako **"Wersja 0.1 - model bazowy"**,
  "Projekt do iteracji, testów, walidacji i audytu" — deklaratywnie
  niedojrzały/niewalidowany, spójnie z resztą projektu Human OS (BETA, brak
  niezależnego audytu bezpieczeństwa, zgodnie z README repo kodu) i z Warstwą 6.
  - Załącznik P ("Otwarte pytania do wersji 0.2") zawiera 12 nierozstrzygniętych
    pytań (kalibracja pewności, wspólne vs. specjalistyczne bramy, budżet zmiany
    bez etykietowania, eksploracja bez destabilizacji rutyn, decyzje wymagające
    obowiązkowej drugiej oceny człowieka, redukcja szkód dla zdeterminowanych
    użytkowników, konflikty modeli/ekspertów, wpływ na autonomię/zależność,
    wynagradzanie ekspertów, reprezentacja wartości bez wspólnej skali, ciągłość
    decyzji przy migracji modeli AI) — potencjalne materiały do przyszłych ADR-ów
    lub sekcji "Limitations/uncertainty" wymaganej przez `CONTRIBUTING.md`.
- **Podwójne, niezależne użycie litery "R" w dokumencie**: (a) "R0"–"R9" jako
  numery rzędów architektury wielorzędowej (sekcja 3), (b) "R-NISKIE" do
  "R-KRYTYCZNE" jako klasy reakcji na ryzyko (sekcja 12.2), (c) "RV0-RV4" jako
  skala odwracalności (sekcja 16.1), (d) "RC0-RC6" jako klasy rekomendacji
  (sekcja 24.1). Żadna z tych czterech skal nie jest tożsama z konstytucyjną
  R0–R4 z CLAUDE.md tego repozytorium — potencjalne źródło pomyłki przy pracach
  nad Reconstruction Audit, warte jawnego odnotowania.
- Skale kodowe zdefiniowane w tym dokumencie (DI, IQ, AR, RV, RC, G, R-[poziom],
  cykl życia rekomendacji) są **odrębne** zarówno od skali ryzyka R0–R4 z
  Konstytucji, jak i od skal Warstwy 6 (XP, EC, BL, MQ, PF, DQ, SE, CA, PE) — trzy
  różne, nieskoordynowane w źródle taksonomie na trzech różnych warstwach, zgodnie
  ze wzorcem "dwóch odrębnych osi" z CLAUDE.md (np. AuthorityRole vs
  IdentityType). Warstwa 5 i Warstwa 6 nie definiują wspólnego słownika kodów —
  integracja między nimi (sekcja 41 / sekcja 38 w Warstwie 6) opisana jest w
  języku naturalnym (nazwy pól przekazywanych obiektów), nie przez wspólne kody
  liczbowe.
- Dokument silnie powiela architektoniczne wzorce Warstwy 6 (bramy przed
  rankingiem/scoringiem, zakaz obiektu-wyroku/ukrytego scalania, zapora
  epistemiczna wobec systemów symbolicznych, sekcja "Rola AI" o identycznej
  strukturze trójdzielnej, "Tryby awarii i ryzyka systemowe" jako tabela
  Tryb/Objaw/Zabezpieczenie, metryki + antymetryki, kryteria akceptacji jako
  checklista) — sugeruje wspólny szablon projektowy dla wszystkich warstw
  Human OS, a nie przypadkową zbieżność.
