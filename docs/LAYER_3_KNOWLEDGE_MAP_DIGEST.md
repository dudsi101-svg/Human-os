# Digest: HUMAN OS — WARSTWA 3 — MAPA WIEDZY I SYGNATURA INFORMACJI

**Status:** rozbiór strukturalny (nie parafraza) źródła dostarczonego przez founder-a
2026-08-15 — `Human_OS_Warstwa_3_Mapa_Wiedzy_i_Sygnatura_Informacji_v0_1.docx`. Patrz
`docs/FOUNDER_REVIEW_2026-08-15.md`, sekcja "Czwarta tura", po kontekst i listę
`ADR-KNOWLEDGE-001..005` sformułowanych na podstawie tego rozbioru. Oryginalny plik DOCX
pozostaje jedynym rozstrzygającym źródłem w razie wątpliwości (`02_Source_Truth_Protocol`).

Źródło: `warstwa3.txt` — ekstrakcja pandoc z DOCX pt. "HUMAN OS — WARSTWA 3 — MAPA WIEDZY I SYGNATURA
INFORMACJI. Pełna dokumentacja epistemiczna, informacyjna i operacyjna". Plik liczy 2249 linii i
został przeczytany od początku do końca (linie 1–2249) w ośmiu blokach, z dodatkowymi
przeszukaniami regex całego pliku dla wzorców "ADR-", "nie wolno", "zabrania", "nie ma prawa",
"Hub", "Digital Twin", "Knowledge Graph".

Motto dokumentu (linie 28–29): *"Human OS nie przechowuje jednej wersji prawdy. Przechowuje
twierdzenia, ich pochodzenie, kontekst, poziom pewności i historię zmian."*

Ten digest naśladuje układ ośmiu nagłówków z
`docs/LAYER_6_EXPERIMENT_ENGINE_DIGEST.md` (dla spójności formatu), ale treść dotyczy wyłącznie
tego, nowego dokumentu Warstwy 3 — nie kopiuje treści digestu Warstwy 6.

---

## 1. Metadane / nagłówek dokumentu (sekcja 0. Karta dokumentu)

Tabela nagłówkowa (linie 9–26):

| Pole | Wartość |
|---|---|
| Wersja | 0.1 - model bazowy |
| Status | Projekt do iteracji, audytu i zatwierdzenia |
| Zakres | Wiedza, źródła, twierdzenia, sygnatury, niepewność, ryzyko i aktualizacja |
| Dokument nadrzędny | Warstwa 1 - Konstytucja i Wartości |
| Model odniesienia | Warstwa 2 - Model Człowieka |
| Właściciel dokumentu | Zespół założycielski Human OS |
| Data | 2026-07-20 |

Ta sama data (2026-07-20) i ten sam "Właściciel dokumentu" (Zespół założycielski Human OS)
występują w karcie dokumentu Warstwy 6 — spójne z resztą serii warstw.

**Cel dokumentu** (0.1, linie 36–52): definiuje sposób, w jaki Human OS przyjmuje, rozkłada,
opisuje, ocenia, łączy, aktualizuje i prezentuje wiedzę. Kluczowe zdanie: "Warstwa 3 nie jest
biblioteką treści. Jest systemem kontroli pochodzenia i znaczenia informacji. Jej zadaniem jest
zapobieganie zlewaniu faktów, hipotez, tradycji, doświadczeń, opinii ekspertów i obserwacji
użytkowników w jedną nieczytelną kategorię."

**Zasada nadrzędna Warstwy 3** (ramka, linie 45–52): *"Każde twierdzenie MUSI mieć widoczne
pochodzenie, zakres zastosowania, poziom niepewności i relację z ryzykiem. System NIE MOŻE
tworzyć pozoru pewności przez ukrywanie braków danych, sprzeczności ani konfliktów interesów."*

**Zakres obowiązywania** (0.2, linie 55–71):
- Obejmuje: bazę wiedzy, graf wiedzy, rekomendacje AI, protokoły, eksperymenty, raporty
  społeczności, ścieżki symboliczne i edukację.
- Obowiązuje: badaczy, redaktorów wiedzy, ekspertów domenowych, architektów danych, twórców
  modeli AI, moderatorów i partnerów.
- Nie rozstrzyga: metafizycznej prawdziwości światopoglądów ani wartości osoby na podstawie tego,
  w jakie systemy wierzy.
- Nie zastępuje: procesu diagnostycznego, profesjonalnej oceny przypadku ani indywidualnej
  odpowiedzialności za decyzję.
- Podlega: Konstytucji Human OS, zasadzie minimalizacji ryzyka oraz prawu użytkownika do
  zrozumiałego wyjaśnienia.

**Co Warstwa 3 dostarcza innym warstwom** (0.4, linie 117–129) — patrz też sekcja 6 poniżej.

**Test nadrzędny** (0.5, linie 131–136): *"Jeżeli użytkownik, audytor lub ekspert nie może
odpowiedzieć na pytania: 'co dokładnie jest twierdzone?', 'skąd to pochodzi?', 'dla kogo i kiedy
ma zastosowanie?', 'jak bardzo jesteśmy tego pewni?' oraz 'co może pójść źle?', obiekt wiedzy nie
jest gotowy do użycia w rekomendacji."* — analogiczna forma bramkująca jak "Test nadrzędny" w
Warstwie 6, ale tu bramkuje gotowość obiektu wiedzy, a nie start eksperymentu.

---

## 2. Nazwane decyzje architektoniczne w stylu ADR

**Brak.** Przeszukano cały plik (case-sensitive i wzorcowo) pod kątem `ADR-` — zero wystąpień.
Dokument, tak jak Warstwa 6, nie zawiera dedykowanej sekcji ani numeracji ADR. Nie ma też
odniesień do `docs/adr/` repozytorium kodu ani do zewnętrznych identyfikatorów decyzyjnych.

Najbliższe odpowiedniki "decyzji architektonicznych":
- 10 aksjomatów w sekcji 1 "Aksjomaty Mapy Wiedzy" (linie 138–192),
- architektura wielorzędowa wiedzy, Rząd 0–7, sekcja 2 (linie 194–251),
- proces przyjmowania i publikacji wiedzy, 10 etapów, sekcja 20.1 (linie 1313–1333),
- kryteria akceptacji Warstwy 3, sekcja 29 (linie 1837–1892).

Jeśli Reconstruction Audit ma sformułować ADR-y dla tego dokumentu, trzeba je utworzyć od zera na
bazie powyższych sekcji — nie istnieją gotowe do wyciągnięcia.

---

## 3. Kluczowe encje / kontrakty danych

### 3.1 Ontologia obiektów wiedzy (sekcja 3, linie 281–345)

Tabela "Obiekt / Definicja operacyjna":

| Obiekt | Definicja operacyjna |
|---|---|
| Pytanie | Problem, cel lub niepewność, którą system ma uporządkować. |
| Twierdzenie | Jedno zdanie o świecie, możliwe do poparcia lub ograniczenia. |
| Obserwacja | Zapis zdarzenia lub pomiaru bez przypisania przyczyny. |
| Mechanizm | Proponowany ciąg przyczynowy wyjaśniający efekt. |
| Model | Uproszczona reprezentacja relacji między obiektami. |
| Praktyka | Powtarzalne działanie mające cel zdrowotny, rozwojowy, relacyjny lub kontemplacyjny. |
| Interwencja | Celowa zmiana przeznaczona do wywołania określonego efektu. |
| Protokół | Wykonalny opis interwencji: kto, co, jak, kiedy, jak długo i kiedy przerwać. |
| Wynik | Zaobserwowana zmiana wraz z metodą pomiaru i horyzontem czasu. |
| Ryzyko | Możliwa szkoda, jej prawdopodobieństwo, nasilenie i odwracalność. |
| Interakcja | Zmiana skutku lub ryzyka przez inny czynnik, lek, praktykę, stan lub kontekst. |
| Przeciwwskazanie | Warunek, przy którym działanie jest niewłaściwe lub wymaga eskalacji. |
| Źródło | Nośnik wiedzy z identyfikowalnym autorem, datą, metodą i pochodzeniem. |
| Dowód | Element wspierający albo osłabiający twierdzenie. |
| Sprzeczność | Relacja wymagająca wyjaśnienia różnic metod, populacji, miar lub interpretacji. |
| Luka wiedzy | Istotne pytanie, dla którego brak wystarczających danych. |
| Rekomendacja | Wniosek decyzyjny oparty na twierdzeniach, ryzyku, celach i modelu użytkownika. |

**3.1 Zakaz obiektów złożonych bez rozbicia** (linie 347–352): zdania typu "zimno poprawia
zdrowie" lub "medytacja działa" muszą zostać rozbite na osobne twierdzenia o populacji, formie
działania, dawce, horyzoncie czasu, mierniku, wielkości efektu i ryzyku.

**3.2 Identyfikowalność** (linie 354–358): każdy obiekt otrzymuje trwały identyfikator, wersję,
datę utworzenia, właściciela merytorycznego, status, powiązane źródła i rejestr zmian. "Treść
może ewoluować, lecz historia nie może być nadpisywana bez śladu."

### 3.2 Minimalna struktura twierdzenia (5.1, linie 431–447)

Szablon (7 pól): DLA [POPULACJI / WARUNKU] — INTERWENCJA LUB CZYNNIK [X] — W POROWNANIU Z
[Y / BRAKIEM ZMIANY] — W DAWCE / FORMIE [D] — W HORYZONCIE [T] — ZMIENIA [MIERNIK / WYNIK] — O
[KIERUNEK I WIELKOSC] — PRZY [RYZYKU / OGRANICZENIACH].

**Reguły atomizacji** (5.2, linie 449–463), sześć reguł: (1) jedno twierdzenie = jeden główny
wynik; (2) skuteczność i bezpieczeństwo to osobne twierdzenia; (3) mechanizm nie zastępuje dowodu
skuteczności; (4) doświadczenie znaczenia ≠ automatycznie zmiana biologiczna; (5) opis oddzielony
od zalecenia normatywnego; (6) wniosek o grupie nie przenosi się wprost na jednostkę bez oceny
dopasowania.

### 3.3 Taksonomia źródeł (sekcja 6, linie 472–534) — kody klas źródeł

| Kod | Klasa źródła | Główna funkcja |
|---|---|---|
| SCI | Badania na ludziach | Ocena skuteczności, bezpieczeństwa, związku i wielkości efektu. |
| MEC | Mechanizmy i badania przedkliniczne | Wyjaśnienie możliwych dróg działania; generowanie hipotez. |
| OBS | Dane obserwacyjne i populacyjne | Wzorce, związki, częstość, sygnały bezpieczeństwa. |
| EXP | Wiedza ekspertów | Synteza złożonych przypadków, interpretacja, ograniczenia, warunki praktyczne. |
| PRX | Wiedza mistrzów praktyki | Proceduralna wiedza z długiego, udokumentowanego doświadczenia. |
| TRD | Tradycja i przekaz historyczny | Długotrwała praktyka, znaczenie kulturowe, repertuar hipotez i rytuałów. |
| COM | Ustrukturyzowane dane społeczności | Sygnały efektów, tolerancji, adherencji i różnic osobniczych. |
| N1 | Dowody osobiste użytkownika | Indywidualna odpowiedź w kontrolowanym lub naturalnym eksperymencie. |
| SYM | Systemy symboliczne i interpretacyjne | Autorefleksja, język pytań, narracja, generowanie hipotez o sobie. |
| HYP | Hipoteza teoretyczna | Pomysł wymagający testowania; brak prawa do przedstawiania jako ustalony fakt. |
| REG | Dane regulacyjne i nadzorcze | Ostrzeżenia, ograniczenia, wycofania, raporty bezpieczeństwa. |
| DOC | Dokumentacja techniczna | Specyfikacje urządzeń, skład, procedury i parametry wykonania. |

**6.1 Zakaz spłaszczania źródeł** (linie 536–542): klasy nie tworzą jednej listy "od najlepszej
do najgorszej" — problem pojawia się, gdy źródło odpowiada na pytanie, do którego nie jest
adekwatne.

### 3.4 Sygnatura wiedzy (sekcja 7, linie 551–656) — 11 wymiarów

Tabela "Wymiar / Pytanie kontrolne": Pochodzenie, Jakość metod, Bezpośredniość, Spójność,
Niezależność, Skala i precyzja, Transparentność, Aktualność, Zakres zastosowania, Niepewność,
Ryzyko błędu (11 wierszy, linie 555–595 — pełne pytania kontrolne w treści dokumentu).

Patrz sekcja 4 poniżej dla skal liczbowych (0–5) i statusu gotowości (E0–E5).

### 3.5 Graf wiedzy — węzły i krawędzie (sekcja 21, linie 1369–1446)

**21.1 Typy węzłów** (linie 1374–1400): twierdzenie, źródło, interwencja, protokół, wynik,
mechanizm, ryzyko, przeciwwskazanie, populacja, miernik, domena, użytkownik lub kohorta (w formie
odseparowanej i chronionej), wersja i decyzja redakcyjna.

**21.2 Typy krawędzi** (linie 1402–1433):

| Relacja | Znaczenie |
|---|---|
| POPIERA | Źródło lub wynik zwiększa wiarygodność twierdzenia. |
| OSŁABIA | Źródło lub wynik zmniejsza wiarygodność twierdzenia. |
| PRZECZY | Twierdzenia są sprzeczne w porównywalnym kontekście. |
| WARUNKUJE | Prawdziwość lub użyteczność zależy od kontekstu. |
| WYJAŚNIA | Mechanizm proponuje drogę prowadzącą do wyniku. |
| RYZYKUJE | Interwencja wiąże się z potencjalną szkodą. |
| WCHODZI_W_INTERAKCJE | Efekt lub ryzyko zmienia się przy innym obiekcie. |
| JEST_WERSJA | Obiekt zastępuje lub rozwija wcześniejszą wersję. |
| WYNIKA_Z | Rekomendacja jest pochodną zestawu twierdzeń, preferencji i ryzyk. |

**21.3 Kontekst jako węzeł**: krytyczne warunki (populacja, dawka, czas, cel, przeciwwskazania)
muszą być obiektami/polami porównywalnymi przez Silnik Decyzji, nie tekstową notatką.

**21.4 Oddzielenie danych użytkownika**: dane osobowe i surowe obserwacje pozostają w chronionej
warstwie profilu; do wiedzy zbiorowej trafiają wyłącznie zanonimizowane/zagregowane obiekty,
zgodnie ze zgodą i minimalizacją.

### 3.6 Statusy cyklu życia wiedzy (22.1, linie 1452–1481)

Kandydat → W przeglądzie → Aktywny → Kwestionowany → Ograniczony → Zawieszony → Wycofany →
Historyczny (8 statusów, z opisami).

### 3.7 Załączniki-formularze (karty pól) — pełne listy pól

- **Załącznik A — Karta sygnatury wiedzy** (linie 1894–1936): ID / wersja, Twierdzenie, Typ
  pytania, Klasy źródeł, Sygnatura, Zakres, Niepewność, Ryzyko, Gotowość (E0–E5 z uzasadnieniem),
  Sprzeczności, Pochodzenie, Warunek aktualizacji.
- **Załącznik B — Karta twierdzenia** (linie 1938–1980): ID, TWIERDZENIE, POPULACJA/WARUNKI,
  INTERWENCJA/CZYNNIK, POROWNANIE, DAWKA/FORMA/CZAS, WYNIK I MIERNIK, KIERUNEK I WIELKOSC EFEKTU,
  ZRODLA POPIERAJACE, ZRODLA OSLABIAJACE, ALTERNATYWNE WYJASNIENIA, OGRANICZENIA,
  RYZYKA/INTERAKCJE, STATUS/GOTOWOSC, DATA PRZEGLADU. Zawiera "Test atomowości" (ramka, linie
  1975–1980).
- **Załącznik C — Lista kontrolna audytu źródła** (linie 1983–2010): 12 pytań checkbox, m.in.
  źródło pierwotne, tożsamość twórcy, metoda vs pytanie, populacja/interwencja/kontrola/czas/
  mierniki, wielkość efektu i niepewność, wszystkie wyniki (w tym szkody/przerwania), konflikty
  interesów, korekty/wycofania, niezależność źródeł, siła języka vs metoda, zakres zastosowania,
  co mogłoby zmienić ocenę.
- **Załącznik D — Karta raportu społeczności** (linie 2012–2047): sekcje Kontekst, Protokół,
  Wykonanie, Współzmienne, Pomiar, Efekt (subiektywny i obiektywny osobno), Szkody, Interpretacja,
  Zgoda.
- **Załącznik E — Karta eksperymentu N-of-1** (linie 2049–2082): Pytanie, Hipoteza, Okres bazowy,
  Interwencja, Miernik główny, Mierniki wtórne, Współzmienne, Kryteria przerwania, Analiza,
  Decyzja.
- **Załącznik F — Macierz ryzyka i gotowości** (linie 2084–2116) — patrz sekcja 4 poniżej.
- **Załącznik G — Przykłady sygnatur** (linie 2118–2190): pięć w pełni rozpisanych przykładów
  (G.1 poranne światło, G.2 GHK-Cu miejscowo, G.3 GHK-Cu iniekcyjnie, G.4 Human Design, G.5 zimna
  ekspozycja) — każdy z polami Twierdzenie / Źródła / Gotowość / Ryzyko lub Kontekst/Niepewność/
  Ograniczenie.
- **Załącznik H — Otwarte pytania do wersji 0.2** (linie 2192–2227): 12 pytań (m.in. forma
  prezentacji sygnatury — radar/etykiety/karta, które wymiary są niekompensowalne, kalibracja
  E0–E5, wykrywanie klonów źródeł, retencja danych surowych, walidacja dopasowania bez
  dyskryminującego profilowania).
- **Załącznik I — Deklaracja Mapy Wiedzy** (linie 2229–2243) — patrz cytat w sekcji 1 powyżej.

---

## 4. Bramy ryzyka/bezpieczeństwa i reguły eskalacji

**Uwaga terminologiczna kluczowa**: dokument NIE używa skali "R0–R4" (skala ryzyka z
Konstytucji/Warstwy 1 wg CLAUDE.md tego repozytorium i potwierdzona w `constitution/README.md`
rozdz. 6, linie 140–142: R0 informacyjne … R4 niedopuszczalne bez wsparcia specjalisty) — brak tej
frazy w całym pliku warstwa3.txt. Warstwa 3 definiuje **własny, odrębny zestaw skal**:

| Skala | Zakres | Co mierzy |
|---|---|---|
| Skala opisowa sygnatury (7.1) | 0 (brak danych) do 5 (bardzo silny) | siła wsparcia dla danego wymiaru sygnatury |
| Gotowość decyzyjna (7.3) | E0 (rozpoznanie) do E5 (wymóg bezpieczeństwa) | dozwolone zastosowanie obiektu wiedzy |
| Poziom przeglądu wg wpływu (26.2) | K1 (informacyjny) do K4 (wysokiego ryzyka) | wymagany skład zespołu przeglądającego |
| Kody klas źródeł (sekcja 6) | SCI, MEC, OBS, EXP, PRX, TRD, COM, N1, SYM, HYP, REG, DOC | typ pochodzenia dowodu (nie ranking) |

To jest **trzecia, odrębna taksonomia** obok skali R0–R4 Konstytucji i skal XP/EC/BL/MQ/PF/DQ/SE/
CA/PE/R±/statusy cyklu Warstwy 6 (opisanych w `docs/LAYER_6_EXPERIMENT_ENGINE_DIGEST.md`). Żadna z
liter/kodów Warstwy 3 (E, K, SCI/MEC/…) nie pokrywa się nazewniczo z kodami Warstwy 6 ani z R0–R4.
Wzorem obu poprzednich dokumentów, nie należy ich mylić — to trzy różne osie na trzech różnych
warstwach.

**Rozbieżność wobec Konstytucji do odnotowania**: `constitution/README.md` rozdz. 5 (linia
130–132) definiuje "Sygnaturę wiedzy" jako "minimum siedem pól towarzyszących każdemu istotnemu
twierdzeniu: pochodzenie, siła podstaw, zakres, niepewność, ryzyko i odwracalność, aktualność,
konflikt interesów" — 7 pól. Warstwa 3 (sekcja 7, linie 551–595) definiuje sygnaturę jako **11
wymiarów**: Pochodzenie, Jakość metod, Bezpośredniość, Spójność, Niezależność, Skala i precyzja,
Transparentność, Aktualność, Zakres zastosowania, Niepewność, Ryzyko błędu. Część nazw się
pokrywa (Pochodzenie, Aktualność, Niepewność), ale liczba wymiarów i część etykiet różnią się
("konflikt interesów" jest w Konstytucji częścią samej sygnatury, w Warstwie 3 jest odrębną
sekcją 25 "Konflikty interesów i integralność informacyjna", nie polem sygnatury z sekcji 7). Nie
rozstrzygam tej rozbieżności — flaguję ją do dalszej weryfikacji przez audyt.

### 4.1 Skala opisowa sygnatury 0–5 (7.1, linie 597–623)

| Poziom | Znaczenie |
|---|---|
| 0 - brak danych | Wymiar nie został oceniony lub brak informacji. |
| 1 - bardzo słaby | Poważne ograniczenia; użyteczne głównie do generowania hipotez. |
| 2 - słaby | Istnieje sygnał, lecz wynik jest podatny na błąd lub ma wąski zakres. |
| 3 - umiarkowany | Wystarczające do ostrożnej interpretacji lub niskoryzykownego działania. |
| 4 - silny | Dobre, spójne i bezpośrednie wsparcie przy znanych ograniczeniach. |
| 5 - bardzo silny | Wielokrotnie potwierdzone, bezpośrednie i odporne na typowe źródła błędu. |

**7.2 Zakaz jednego wyniku bez wektora** (linie 625–631): "System może tworzyć uproszczony status
dla interfejsu, ale pełna sygnatura pozostaje wektorem. […] Suma punktów nie może ukryć słabego
wymiaru krytycznego." — bezpośrednio odpowiada zakazowi z Konstytucji nt. nieukrywania braków
(patrz sekcja 1 powyżej) i jest w tensji z jednowymiarowym `confidence: float` polem
`ProvenanceRecord` w `hos_engine/knowledge_graph.py` (patrz sekcja 6 poniżej — flaga do audytu, nie
rozstrzygana tutaj).

### 4.2 Gotowość decyzyjna E0–E5 (7.3, linie 633–656) — najbliższy odpowiednik "bramy ryzyka"

| Status | Dozwolone zastosowanie |
|---|---|
| E0 - rozpoznanie | Treść może być przechowywana jako sygnał lub pytanie. |
| E1 - hipoteza | Może generować dalsze badanie i refleksję. |
| E2 - eksploracja | Może wspierać niskoryzykowny, odwracalny eksperyment z pomiarem. |
| E3 - ostrożna rekomendacja | Może zostać zaproponowana po sprawdzeniu kontekstu i przeciwwskazań. |
| E4 - rekomendacja standardowa | Może stanowić domyślną opcję w odpowiednim kontekście. |
| E5 - wymóg bezpieczeństwa | Informacja jest na tyle istotna, że pominięcie jej byłoby ryzykowne. |

### 4.3 Zasada asymetrii dowodowej (17.2, linie 1183–1202)

| Ryzyko / odwracalność | Minimalna gotowość wiedzy |
|---|---|
| Niskie i łatwo odwracalne | Możliwa eksploracja przy statusie E2, jeśli użytkownik rozumie niepewność. |
| Umiarkowane lub kosztowne | Wymagana wyższa bezpośredniość, kontrola interakcji i plan monitorowania. |
| Wysokie lub trudno odwracalne | Wymagane silne źródła, zgodność ekspertów i profesjonalny nadzór. |
| Krytyczne lub potencjalnie trwałe | System nie tworzy samodzielnego protokołu; eskaluje lub odmawia aktywnego ułatwiania. |

### 4.4 Macierz ryzyka i gotowości — Załącznik F (linie 2084–2116)

| Ryzyko | Odwracalność | Minimalny status | Domyślny tryb |
|---|---|---|---|
| Niskie | Wysoka | E2 | Samodzielny eksperyment z prostym pomiarem. |
| Niskie | Niska | E3 | Ostrożna rekomendacja i pełna informacja. |
| Umiarkowane | Wysoka | E3 | Sprawdzenie interakcji i kryteria przerwania. |
| Umiarkowane | Niska | E4 | Przegląd eksperta i monitoring. |
| Wysokie | Dowolna | E4/E5 | Profesjonalny nadzór; brak autonomicznego protokołu AI. |
| Krytyczne | Dowolna | Poza samodzielnym trybem | Eskalacja, odmowa lub pilne działanie bezpieczeństwa. |

### 4.5 Poziom przeglądu zależny od wpływu K1–K4 (26.2, linie 1690–1709)

| Poziom | Przykład | Wymóg |
|---|---|---|
| K1 - informacyjny | Niskoryzykowna ciekawostka lub definicja. | Automatyczny audyt + redaktor. |
| K2 - refleksyjny | Praktyka autorefleksji lub stylu życia. | Redaktor + przegląd domenowy. |
| K3 - decyzyjny | Rekomendacja wpływająca na zdrowie lub istotne zasoby. | Metodolog + ekspert + bezpieczeństwo. |
| K4 - wysokiego ryzyka | Interwencja medyczna, nieodwracalna lub eksperymentalna. | Wielospecjalistyczny przegląd i ograniczony tryb użycia. |

### 4.6 Bramy publikacyjne (20.2, linie 1335–1360)

Sześć bram: Tożsamość, Atomizacja, Kontekst, Bezpieczeństwo, Pochodzenie, Przegląd — każda ze
"skutkiem negatywnym" (np. brak spełnienia bramy Bezpieczeństwo → "Brak użycia w rekomendacji").

### 4.7 Ryzyka systemowe / tryby awarii (sekcja 28, linie 1768–1836)

Tabela 12 trybów awarii z zabezpieczeniami: epistemiczne spłaszczenie, nadmierna pewność AI, kult
autorytetu, popularność jako prawda, cherry-picking, fałszywa równowaga, wiedza bez kontekstu,
pętla samopotwierdzająca, ukryta komercjalizacja, przestarzała wiedza, przeprofilowanie duchowe,
nadmierne mierzenie. Plus **28.1 Czerwone flagi organizacyjne** (7 flag, linie 1821–1835).

### 4.8 Kryteria akceptacji Warstwy 3 (sekcja 29, linie 1837–1892) — pełna lista bramkowa

15 punktów (m.in. formalna ontologia; trwały identyfikator/wersja/właściciel/źródło dla każdego
aktywnego twierdzenia; sygnatura z min. 7 wymiarami wymienionymi explicite w kryterium 3 —
**uwaga**: to kryterium akceptacyjne samo wymienia inny podzbiór niż pełna tabela sekcji 7, patrz
niżej; rozróżnienie 8 klas źródeł; zapora epistemiczna dla Human Design i systemów
interpretacyjnych; procedura pełnego cyklu życia wiedzy; sprzeczności/luki przechowywane a nie
usuwane; wyższy próg dowodowy dla wysokiego ryzyka; ślad wyjaśnienia dla każdej rekomendacji;
dane społeczności z mianownikiem; dane użytkownika nieautomatycznie kopiowane do wiedzy zbiorowej;
role/uprawnienia/odwołanie/audyt konfliktów; widok minimalistyczny + rozwijalny; co najmniej
jedna ścieżka MVP end-to-end).

**Uwaga wewnętrzna niespójność do odnotowania**: kryterium 3 sekcji 29 (linia 1846–1847) wymienia
sygnaturę jako "co najmniej: pochodzenie, jakość, bezpośredniość, spójność, zakres, niepewność i
ryzyko" — **7 elementów**, nie 11 z pełnej tabeli sekcji 7 (Jakość metod, Skala i precyzja,
Transparentność, Aktualność, Zakres zastosowania są w tabeli sekcji 7, ale "jakość"/"zakres" w
kryterium 29.3 to skrócone/zlane etykiety). To może być zamierzone streszczenie albo rozbieżność
redakcyjna wewnątrz samego dokumentu — audyt może chcieć to sprawdzić względem oryginalnego DOCX.

Zamykająca ramka "Kryterium końcowe" (linie 1884–1891): *"Warstwa 3 jest wdrożona dopiero wtedy,
gdy system potrafi uczciwie powiedzieć nie tylko 'co wiemy', lecz także 'skąd to wiemy', 'dla
kogo', 'jak bardzo', 'czego nie wiemy' i 'co zmieniłoby nasz wniosek'."*

---

## 5. Kluczowa terminologia (0.3 "Podstawowe terminy", linie 73–115)

| Termin | Znaczenie |
|---|---|
| Twierdzenie | Jednoznaczna, możliwie mała jednostka treści, którą można poprzeć, ograniczyć, zakwestionować lub wycofać. |
| Źródło | Obiekt, z którego pochodzi obserwacja, argument, dane lub interpretacja. |
| Dowód | Informacja zwiększająca albo zmniejszająca wiarygodność określonego twierdzenia. |
| Sygnatura wiedzy | Wielowymiarowy opis pochodzenia, jakości, spójności, zakresu, niepewności i ryzyka. |
| Kontekst | Warunki, populacja, cel, dawka, czas i środowisko, w których twierdzenie ma zastosowanie. |
| Protokół | Operacyjny opis działania, który może być wykonany i monitorowany. |
| Sprzeczność | Relacja między twierdzeniami lub wynikami, których nie można jednocześnie przyjąć bez dodatkowych warunków. |
| Stan wiedzy | Status cyklu życia: kandydat, w przeglądzie, aktywny, kwestionowany, ograniczony, wycofany lub historyczny. |
| Pochodzenie | Pełny ślad od źródła pierwotnego do aktualnej treści, tłumaczenia, streszczenia i rekomendacji. |

Dodatkowe pojęcia zdefiniowane rozproszone w treści (poza tabelą 0.3), istotne dla "Sygnatury
Informacji":

- **Trzy poziomy pewności** (2.2, linie 261–279) — Pewność twierdzenia (na ile źródła wspierają
  samo twierdzenie), Pewność zastosowania (na ile twierdzenie pasuje do warunków/celu), Pewność
  rekomendacji osobistej (na ile zasadne jest zaproponowanie tego użytkownikowi) — trzy oddzielnie
  przechowywane wymiary, nie jedna liczba.
- **Odległość translacyjna** (9.2, linie 743–748): "model -> tkanka -> organizm -> zachowanie ->
  wynik ważny dla osoby. Im więcej kroków, tym niższa bezpośredniość" — miara przenoszalności
  dowodów przedklinicznych.
- **Pułapka mechanistycznego zachwytu** (9.3, ramka, linie 750–759): przekonujący mechanizm
  biologiczny nie może samodzielnie uzasadniać wysokoryzykownej interwencji ani obietnicy efektu
  klinicznego.
- **Zapora epistemiczna** (11.4, ramka, linie 862–872): treści SYM i TRD (systemy symboliczne i
  tradycja) mogą wpływać na pytania/refleksję/niskoryzykowne eksperymenty, ale "nie mogą bez
  niezależnego wsparcia przechodzić bezpośrednio do medycznych twierdzeń przyczynowych ani
  protokołów wysokiego ryzyka" — ten sam termin pojawia się też w dokumencie Warstwy 6 (32.4), z
  niemal identyczną funkcją — spójne między dwoma warstwami.
- **Waga raportu** (12.3, tabela linie 905–932): siedem wymiarów (Kompletność, Izolacja zmiennej,
  Pomiar, Adherencja, Trwałość, Bezpieczeństwo, Podobieństwo) różnicujących "niższą" i "wyższą"
  wagę raportu społeczności.
- **Typy relacji przyczynowych** (15.1, tabela linie 1032–1056): Współwystępowanie, Predykcja,
  Przyczynowość, Mediator, Moderator, Sprzężenie zwrotne, Wspólna przyczyna.
- **Rodzaje niepewności** (16.1, tabela linie 1078–1113): 10 typów — Losowa, Pomiarowa,
  Metodologiczna, Modelowa, Translacyjna, Czasowa, Bezpieczeństwa, Normatywna, Semantyczna,
  Nieznane nieznane.
- **Komunikacja niepewności** (16.2, tabela linie 1115–1139): sześciostopniowa skala słowna —
  Dobrze ustalone, Prawdopodobne, Możliwe, Niejednoznaczne, Nie wiemy, Nie można obecnie ustalić.
- **Język przyczynowy** (15.3, linie 1066–1072): słowa "powoduje", "odwraca", "leczy",
  "zapobiega" dozwolone tylko gdy bezpośredniość/metoda to wspierają; inaczej system używa
  "wiąże się", "może wspierać", "zaobserwowano", "istnieje hipoteza", "u tej osoby
  współwystąpiło".

---

## 6. Relacje z innymi warstwami / komponentami Human OS

**0.4 "Co Warstwa 3 dostarcza innym warstwom"** (linie 117–129):
- Warstwie 4 - Model Użytkownika: "zweryfikowane pojęcia, zakresy normatywne i kontekst
  interpretacji danych."
- Warstwie 5 - Silnik Decyzji: "twierdzenia, ograniczenia, warianty, interakcje, ryzyko i
  gotowość decyzyjną."
- Warstwie 6 - Silnik Eksperymentów: "hipotezy, mierniki, oczekiwane efekty, czas obserwacji i
  kryteria przerwania."
- Warstwie 7 - Inteligencja Zbiorowa: "strukturę raportów i reguły włączania doświadczeń
  użytkowników do wiedzy zbiorowej."

**Sekcja 27 "Interfejsy z pozostałymi warstwami"** (linie 1718–1751), tabela pełna:

| Warstwa | Kontrakt |
|---|---|
| Warstwa 1 - Konstytucja | "Wyznacza wartości, prawa użytkownika, granice ryzyka i zakaz manipulacji. Warstwa 3 nie może ich obchodzić przez dobór źródeł." |
| Warstwa 2 - Model Człowieka | "Dostarcza domeny, konteksty i pojęcia. Warstwa 3 dostarcza definicje i zakres interpretacji." |
| Warstwa 4 - Model Użytkownika | "Przekazuje dane kontekstowe i osobiste wyniki. Otrzymuje twierdzenia z poziomem zastosowania." |
| Warstwa 5 - Silnik Decyzji | "Otrzymuje kandydatów, ryzyka, alternatywy i gotowość. Zwraca informacje o decyzjach i lukach." |
| Warstwa 6 - Silnik Eksperymentów | "Otrzymuje hipotezy i mierniki. Zwraca wyniki oraz jakość wykonania." |
| Warstwa 7 - Inteligencja Zbiorowa | "Otrzymuje schemat raportu. Zwraca zanonimizowane sygnały efektów, szkód i heterogeniczności." |

**27.1 Minimalny pakiet dla Silnika Decyzji** (linie 1752–1766): identyfikator/wersja
twierdzenia, status i gotowość decyzyjna, pełna sygnatura i słabe wymiary krytyczne, zakres
zastosowania i przeciwwskazania, korzyści/ryzyka/interakcje/koszt/obciążenie, alternatywy, data
przeglądu i warunki ponownej oceny.

**Uwaga na spójność z Warstwą 6 (już opisaną w `docs/LAYER_6_EXPERIMENT_ENGINE_DIGEST.md`)**:
tabela interfejsów Warstwy 6 sekcja 38 (jej digest, linia 340) opisuje kontrakt z "3. Mapa
Wiedzy" niemal symetrycznie do tego, co Warstwa 3 mówi o Warstwie 6 tutaj — obie strony zgadzają
się co do kierunku wymiany (hipotezy/mierniki/ryzyko w jedną stronę, wyniki/jakość wykonania w
drugą). Nie znaleziono sprzeczności między dwoma dokumentami w tym punkcie.

**Hub / Digital Twin / Knowledge Graph** — nazwy własne modułów kodu (`hub/`,
`hos_engine/knowledge_graph.py`) **nie pojawiają się dosłownie** w tym dokumencie (przeszukano
case-insensitive: zero wystąpień "Hub", "Digital Twin", "Cyfrowy Bliźniak", "Knowledge Graph").
Dokument mówi wyłącznie o "Mapie Wiedzy" (nazwa własna Warstwy 3) i "grafie wiedzy" (pospolita
nazwa struktury w sekcji 21) — nie o kodowej nazwie `KnowledgeGraph`. To ten sam wzorzec, który
`docs/LAYER_6_EXPERIMENT_ENGINE_DIGEST.md` odnotował dla Warstwy 6: nazwy modułów kodu nie
występują w źródłowych dokumentach warstw; nie zakładać 1:1 mapowania bez dodatkowej weryfikacji.

**Cross-check z kodem (`hos_engine/knowledge_graph.py`)** — obserwacje, nie rozstrzygnięcia:
- Sekcja 21.1 dokumentu wymienia 13 typów węzłów (twierdzenie, źródło, interwencja, protokół,
  wynik, mechanizm, ryzyko, przeciwwskazanie, populacja, miernik, domena, użytkownik/kohorta,
  wersja/decyzja redakcyjna) jako zamknięty katalog. W kodzie `GraphNode.node_type` to zwykły
  `str` bez enumeracji ograniczającej wartości — węzły dowolnego typu są dopuszczalne
  programistycznie; brak wymuszenia katalogu z sekcji 21.1.
- Sekcja 21.2 dokumentu definiuje 9 nazwanych relacji grafowych (POPIERA, OSŁABIA, PRZECZY,
  WARUNKUJE, WYJAŚNIA, RYZYKUJE, WCHODZI_W_INTERAKCJE, JEST_WERSJA, WYNIKA_Z). W kodzie
  `GraphEdge.relation_type` jest również zwykłym `str` — brak enumeracji odpowiadającej tym 9
  wartościom (kontrastuje to z `hub_entity_registry.HubRelationType`, który wg CLAUDE.md *jest*
  typowanym enumem 17 relacji Hub-a). Innymi słowy: `knowledge_graph.py` obecnie nie koduje
  wprost słownika relacji z Warstwy 3 sekcja 21.2 — to luka do potencjalnego zamknięcia, nie błąd,
  bo moduł jest ogólnym grafem, ale audyt może chcieć to odnotować.
- `ProvenanceRecord` w kodzie ma pojedyncze pole `confidence: float` (0.0–1.0) na rekord
  pochodzenia. Dokument w 7.2 wprost zakazuje redukowania sygnatury do jednej liczby ("Zakaz
  jednego wyniku bez wektora" — "Suma punktów nie może ukryć słabego wymiaru krytycznego").
  `ProvenanceRecord.confidence` jest skalarem, a pełna sygnatura wiedzy z sekcji 7 dokumentu ma
  11 wymiarów. To nie musi być sprzeczność — `ProvenanceRecord` może być zamierzenie węższym
  prymitywem niż pełna "Sygnatura wiedzy" — ale warto to sprawdzić względem intencji projektowej,
  nie zakładać automatycznie zgodności.
- Kod ma pola `reversible: bool` na `GraphEdge` i mechanizmy `has_directed_cycle`/
  `confidence_of_path` (mnożenie confidence wzdłuż ścieżki) — dokument nie opisuje algorytmu
  propagacji pewności wzdłuż ścieżek grafowych w żadnym miejscu przeczytanego tekstu; to
  implementacyjny wybór bez bezpośredniego odpowiednika normatywnego w Warstwie 3 (nie jest to
  sprzeczne z dokumentem, po prostu nienormowane przez niego).

**Cross-check z `constitution/README.md` rozdz. 5** — opisany w sekcji 4 powyżej (rozbieżność
liczby pól sygnatury: 7 w Konstytucji vs 11 w Warstwie 3).

---

## 7. Explicit prohibitions ("nie ma prawa" / "nie wolno" / "zabrania się")

**Żadna z trzech dokładnych fraz nie występuje w dokumencie** — przeszukano cały plik
case-insensitive dla "nie ma prawa", "nie wolno" i "zabrania" (wraz z odmianami "zabraniać" itp.)
— zero wystąpień. To odróżnia Warstwę 3 od Warstwy 6, która miała jedno wystąpienie "Nie ma
prawa" na początku dokumentu (0.1) — w Warstwie 3 nawet to jedno wystąpienie jest nieobecne.

Zamiast tego dokument formułuje wiążące zakazy poprzez (a) nagłówki sekcji zaczynające się od
"Zakaz ..." i (b) zdania z "nie może" / "nie mogą" / "nie mogą być". Pełna lista znalezionych
przykładów, z numerami linii:

**Nagłówki "Zakaz ..." (sekcje normatywne, nie tylko zdania)**:
1. (linia 347) **3.1 Zakaz obiektów złożonych bez rozbicia**
2. (linia 536) **6.1 Zakaz spłaszczania źródeł**
3. (linia 625) **7.2 Zakaz jednego wyniku bez wektora**
4. (linia 1348, komórka tabeli "Kontekst") **Zakaz uogólnienia** (skutek negatywny bramy
   publikacyjnej "Kontekst" w tabeli 20.2)
5. (linia 1503) **22.3 Zakaz cichego nadpisywania**
6. (linia 1546) **23.3 Zakaz konfabulacji epistemicznej**
7. (linia 1585) **24.2 Zakaz fałszywej precyzji**

**Zdania z "nie może" / "nie mogą" formułujące wiążący zakaz** (cytaty dosłowne, z numerami
linii):
1. (linia 145) *"Mapa porządkuje wiedzę, ale nie jest rzeczywistością i nie może rościć sobie
   prawa do kompletności."* (aksjomat 1.1)
2. (linia 358) *"Treść może ewoluować, lecz historia nie może być nadpisywana bez śladu."* (3.2)
3. (linia 455) *"Mechanizm nie może zastępować dowodu skuteczności."* (5.2, reguła 3)
4. (linia 457–458) *"Doświadczenie znaczenia nie może być automatycznie tłumaczone jako zmiana
   biologiczna."* (5.2, reguła 4)
5. (linia 462–463) *"Wniosek o grupie nie może być bezpośrednio przypisany jednostce bez oceny
   dopasowania."* (5.2, reguła 6)
6. (linia 630) *"Suma punktów nie może ukryć słabego wymiaru krytycznego."* (7.2)
7. (linia 882) *"[Liczba pozytywnych opinii] nie może zastąpić mianownika: ilu użytkowników
   rozpoczęło, ukończyło, przerwało, nie odpowiedziało lub doświadczyło szkody."* (12.1)
8. (linia 936–937) *"Rzadkie, ale poważne działania niepożądane nie mogą być zagłuszone przez
   dużą liczbę pozytywnych raportów."* (12.4)
9. (linia 1437) *"Kontekst nie może być jedynie tekstową notatką."* (21.3)
10. (linia 1630–1631) *"Sponsor nie może decydować o sygnaturze ani usuwać danych
    niekorzystnych."* (25.2, zasada 2)
11. (linia 1727–1728) *"Warstwa 3 nie może ich [praw/zakazów Warstwy 1] obchodzić przez dobór
    źródeł."* (sekcja 27, kontrakt z Warstwą 1)
12. (linia 1835) *"[…] odpowiedź AI nie może być odtworzona z istniejących obiektów"* — jako
    czerwona flaga organizacyjna (28.1), czyli sytuacja, która **nie powinna** wystąpić (odwrotnie
    sformułowany zakaz: brak odtwarzalności jest symptomem błędu).
13. (linia 2175–2176) *"system nie może mówić użytkownikowi, że typ [Human Design] determinuje
    jego naturę ani używać mapy do diagnozy."* (Załącznik G.4, przykład ograniczenia)

**Inne silne zdania normatywne warte odnotowania** (nie zawierają "nie może"/"nie wolno" wprost,
ale są wiążącymi ograniczeniami):
- Ramka "Zasada nadrzędna Warstwy 3" (linie 47–51): *"System NIE MOŻE tworzyć pozoru pewności
  przez ukrywanie braków danych, sprzeczności ani konfliktów interesów."* (jedyne wystąpienie
  wersalikami "NIE MOŻE" w dokumencie, w ramce na początku).
- Ramka "Reguła" 9.3 (linie 753–758): *"Przekonujący mechanizm może zwiększać sens testowania.
  Nie może samodzielnie uzasadniać wysokoryzykownej interwencji ani obietnicy klinicznego
  efektu."*
- Ramka "Zapora" 11.4 (linie 865–870): *"Treści SYM i TRD […] Nie mogą bez niezależnego wsparcia
  przechodzić bezpośrednio do medycznych twierdzeń przyczynowych ani protokołów wysokiego
  ryzyka."*
- 11.2 "Niedozwolone" (linie 835–838, lista myślników): diagnozowanie chorób, prognozowanie
  nieuniknionych zdarzeń, zamykanie osoby w typie, uzasadnianie wysokiego ryzyka lub
  dyskryminacji — dla systemów symbolicznych.
- Ramka "Zasada" 23.3, "Zakaz konfabulacji epistemicznej" (linie 1551–1554): *"Jeżeli źródło,
  data, autor, wynik lub relacja nie są dostępne, AI ma powiedzieć, że ich nie zna. Nie może
  uzupełniać braków prawdopodobnie brzmiącą treścią ani nadawać własnemu przypuszczeniu statusu
  źródła."*
- 18.2, procedura rozstrzygania sprzeczności, punkt 7 (linie 1253–1254): *"Nie tworzyć sztucznego
  kompromisu, gdy jedna strona ma wyraźnie słabsze podstawy."*
- 25.3 "Pluralizm bez symetrii" (linie 1645–1648): system nie nadaje szkołom myślenia równej wagi
  "wyłącznie dla wrażenia neutralności".

---

## 8. Struktura dokumentu (spis treści wg nagłówków)

```
HUMAN OS — WARSTWA 3 — MAPA WIEDZY I SYGNATURA INFORMACJI

0.   Karta dokumentu i sposób stosowania
  0.1  Cel dokumentu
  0.2  Zakres obowiązywania
  0.3  Podstawowe terminy
  0.4  Co Warstwa 3 dostarcza innym warstwom
  0.5  Test nadrzędny
1.   Aksjomaty Mapy Wiedzy (10 aksjomatów, 1.1–1.10)
2.   Architektura wielorzędowa wiedzy (Rząd 0–7)
  2.1  Rozdzielenie prawdziwości od użyteczności
  2.2  Trzy poziomy pewności
3.   Ontologia obiektów wiedzy
  3.1  Zakaz obiektów złożonych bez rozbicia
  3.2  Identyfikowalność
4.   Domeny, taksonomie i tagowanie
  4.1  Taksonomia domen
  4.2  Tagi przekrojowe
  4.3  Wiele klasyfikacji jednocześnie
5.   Rozkład twierdzeń i poziom szczegółowości
  5.1  Minimalna struktura twierdzenia
  5.2  Reguły atomizacji
  5.3  Twierdzenia normatywne
6.   Taksonomia źródeł
  6.1  Zakaz spłaszczania źródeł
  6.2  Źródła mieszane
7.   Sygnatura wiedzy
  7.1  Skala opisowa
  7.2  Zakaz jednego wyniku bez wektora
  7.3  Gotowość decyzyjna
8.   Dowody naukowe dotyczące ludzi
  8.1  Elementy oceny
  8.2  Typ pytania a odpowiedni projekt
  8.3  Istotność statystyczna nie jest wystarczająca
  8.4  Badania negatywne i neutralne
9.   Mechanizmy i dowody przedkliniczne
  9.1  Role mechanizmu
  9.2  Granice przenoszenia
  9.3  Pułapka mechanistycznego zachwytu
10.  Wiedza ekspertów i mistrzów praktyki
  10.1 Rozdzielenie dwóch ról
  10.2 Kryteria wiarygodności osoby
  10.3 Fama, dostęp do elit i sukces życiowy
  10.4 Twierdzenia proceduralne
11.  Tradycje, praktyki kontemplacyjne i systemy symboliczne
  11.1 Status tradycji
  11.2 Systemy symboliczne: Human Design, astrologia i typologie
  11.3 Rozdzielenie doświadczenia od interpretacji
  11.4 Zapora epistemiczna
12.  Dane społeczności i zbiorowa obserwacja
  12.1 Raport nie jest głosem
  12.2 Minimalny raport społeczności
  12.3 Waga raportu
  12.4 Sygnały bezpieczeństwa
13.  Dowody osobiste i eksperymenty N-of-1
  13.1 Status dowodu osobistego
  13.2 Elementy dobrego N-of-1
  13.3 Uczenie modelu użytkownika
  13.4 Efekt oczekiwania i znaczenie
14.  Zakres zastosowania i dopasowanie kontekstu
  14.1 Wymiary kontekstu
  14.2 Dopasowanie populacyjne
  14.3 Wartości i preferencje
15.  Przyczynowość, korelacja i alternatywne wyjaśnienia
  15.1 Typy relacji
  15.2 Obowiązek alternatyw
  15.3 Język przyczynowy
16.  Niepewność i luki wiedzy
  16.1 Rodzaje niepewności
  16.2 Komunikacja niepewności
  16.3 Wyjście ze stanu niepewności
17.  Ryzyko, odwracalność, koszt i obciążenie
  17.1 Wymiary ryzyka
  17.2 Zasada asymetrii dowodowej
  17.3 Koszt i obciążenie
  17.4 Procedura minimalizacji szkód
18.  Sprzeczności, rozbieżności i konsensus
  18.1 Typy sprzeczności
  18.2 Procedura rozstrzygania
  18.3 Konsensus
19.  Ocena jakości i audyt źródeł
  19.1 Minimalny audyt źródła
  19.2 Źródła wtórne i łańcuch cytowania
  19.3 Automatyczny audyt nie wystarcza
  19.4 Audyt języka
20.  Proces przyjmowania i publikacji wiedzy
  20.1 Etapy (10-etapowy przepływ: POZYSKANIE SYGNAŁU … MONITOROWANIE NOWYCH DANYCH I SYGNAŁÓW SZKODY)
  20.2 Bramy publikacyjne
  20.3 Priorytety pozyskiwania
21.  Graf wiedzy i sieć relacji
  21.1 Typy węzłów
  21.2 Typy krawędzi
  21.3 Kontekst jako węzeł
  21.4 Oddzielenie danych użytkownika
22.  Wersjonowanie, aktualizacja i wycofywanie
  22.1 Statusy cyklu życia
  22.2 Wyzwalacze aktualizacji
  22.3 Zakaz cichego nadpisywania
  22.4 Propagacja zmiany
23.  Rola AI i wymagania wyjaśnialności
  23.1 Dozwolone funkcje AI
  23.2 Obowiązkowy ślad odpowiedzi
  23.3 Zakaz konfabulacji epistemicznej
  23.4 Oddzielenie modelu językowego od rejestru wiedzy
24.  Prezentacja wiedzy użytkownikowi
  24.1 Widok warstwowy
  24.2 Zakaz fałszywej precyzji
  24.3 Język niepewności i ryzyka
  24.4 Prawo do prostoty
25.  Konflikty interesów i integralność informacyjna
  25.1 Rodzaje konfliktów
  25.2 Zasady
  25.3 Pluralizm bez symetrii
26.  Zarządzanie wiedzą i odpowiedzialność
  26.1 Role
  26.2 Poziom przeglądu zależny od wpływu
  26.3 Odwołanie i korekta
27.  Interfejsy z pozostałymi warstwami
  27.1 Minimalny pakiet dla Silnika Decyzji
28.  Ryzyka systemowe i tryby awarii
  28.1 Czerwone flagi organizacyjne
29.  Kryteria akceptacji Warstwy 3

Załączniki (A–I):
  A. Karta sygnatury wiedzy
  B. Karta twierdzenia
  C. Lista kontrolna audytu źródła
  D. Karta raportu społeczności
  E. Karta eksperymentu N-of-1
  F. Macierz ryzyka i gotowości
  G. Przykłady sygnatur (5 scenariuszy: G.1 poranne światło, G.2 GHK-Cu miejscowo, G.3 GHK-Cu
     iniekcyjnie, G.4 Human Design, G.5 zimna ekspozycja)
  H. Otwarte pytania do wersji 0.2
  I. Deklaracja Mapy Wiedzy
```

Struktura jest wyraźnie płytsza niż Warstwy 6 (29 sekcji głównych + 9 załączników A–I, wobec 47
sekcji + 22 załączniki A–V w Warstwie 6) — spójne z tym, że Warstwa 3 jest dokumentem o
zasadach epistemicznych/sygnaturze wiedzy, a nie pełnym cyklem operacyjnym eksperymentu.

---

## Dodatkowe obserwacje istotne dla audytu

- **Brak numeracji ADR i brak jakiegokolwiek "nie wolno"/"nie ma prawa"/"zabrania się"** — oba te
  fakty są warte odnotowania razem: Warstwa 3 jest redakcyjnie "łagodniejsza" w formie zakazu niż
  Warstwa 6 (która miała choć jedno dosłowne "Nie ma prawa"), mimo że materialnie formułuje
  równie wiążące normy przez nagłówki "Zakaz ..." i zdania "nie może/nie mogą". Audyt
  Reconstruction Audit powinien traktować to jako różnicę stylu redakcyjnego, nie różnicę wagi
  normatywnej.
- **Trzy odrębne, nienakładające się taksonomie skal** widoczne teraz w trzech przeanalizowanych
  dokumentach: R0–R4 (Konstytucja/Warstwa 1, ryzyko interwencji), XP/EC/BL/MQ/PF/DQ/SE/CA/PE/R±
  (Warstwa 6, klasy procesu eksperymentalnego i jego jakość/bezpieczeństwo), oraz teraz
  E0–E5/K1–K4/skala opisowa 0–5/kody klas źródeł SCI-DOC (Warstwa 3, gotowość i jakość wiedzy).
  Żadne z liter nie kolidują między warstwami, ale też żadne nie mapują się 1:1 — to zamierzony
  wzorzec "różne osie na różnych warstwach", spójny z uwagą CLAUDE.md o AuthorityRole vs
  IdentityType w warstwie kodu.
- **Rozbieżność liczby pól "sygnatury wiedzy"** między `constitution/README.md` (7 pól) a
  Warstwą 3 (11 wymiarów w sekcji 7, ale 7 wymienionych explicite w kryterium akceptacyjnym 29.3)
  — patrz szczegóły w sekcji 4 powyżej. To najbardziej konkretny, sprawdzalny punkt do
  rozstrzygnięcia przez founder-a/audyt: czy 11-wymiarowa tabela sekcji 7 jest kanoniczna, a
  7-polowe podsumowania (Konstytucja, kryterium 29.3) są uproszczeniami, czy odwrotnie.
- **Kod `hos_engine/knowledge_graph.py` jest generycznym, nietypowanym grafem** (węzły/krawędzie
  jako wolne stringi `node_type`/`relation_type`, pojedynczy skalarny `confidence` na rekord
  pochodzenia) wobec dość szczegółowo wyspecyfikowanej w dokumencie ontologii 13 typów węzłów, 9
  nazwanych relacji i 11-wymiarowej sygnatury z jawnym zakazem redukcji do jednej liczby. Nie jest
  to jednoznacznie "błąd" (moduł może być zamierzenie ogólnym prymitywem pod przyszłą
  specjalizację), ale jest to zauważalna luka między specyfikacją a obecną implementacją, wartą
  wpisania do listy rozbieżności audytu — analogicznie do tego, jak CLAUDE.md już odnotowuje
  `hub_entity_registry.EntityRegistry` jako "MVP_IMPLEMENTED_SUBSET" wobec pełnej specyfikacji
  Hub-a.
- Dokument deklaruje ten sam status dojrzałości co Warstwa 6: **"Wersja 0.1 – model bazowy"**,
  "Projekt do iteracji, audytu i zatwierdzenia" — deklaratywnie niedojrzały, spójnie z BETA
  repozytorium kodu. Załącznik H zawiera 12 nierozstrzygniętych pytań do wersji 0.2 (m.in. forma
  prezentacji sygnatury, kalibracja E0–E5 na danych rzeczywistych, wykrywanie klonów źródeł,
  retencja danych surowych) — potencjalny materiał do przyszłych ADR-ów lub sekcji
  "Limitations/uncertainty" wymaganej przez `CONTRIBUTING.md`.
