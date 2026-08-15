# Digest: HUMAN OS — WARSTWA 6 — SILNIK EKSPERYMENTÓW, MONITOROWANIA I POSTĘPU

**Status:** rozbiór strukturalny (nie parafraza) źródła dostarczonego przez
founder-a 2026-08-15 —
`Human_OS_Warstwa_6_Silnik_Eksperymentow_Monitorowania_i_Postepu_v0_1_2.docx`
(wersja dokumentu "0.1 – model bazowy"). Patrz
`docs/FOUNDER_REVIEW_2026-08-15.md`, sekcja "Trzecia tura", po kontekst i
listę ADR-EXP-001..005 sformułowanych na podstawie tego rozbioru. Oryginalny
plik DOCX pozostaje jedynym rozstrzygającym źródłem w razie wątpliwości
(`02_Source_Truth_Protocol`).

Źródło: ekstrakcja pandoc z DOCX (3585 linii tekstu jawnego). Cały plik
został przeczytany od początku do końca (linie 1–3585) w pięciu blokach.

Motto dokumentu (linie 10–12): *"Eksperyment nie służy udowadnianiu racji systemu. Służy
bezpiecznemu sprawdzeniu, co zmienia się u konkretnego człowieka, w konkretnych warunkach i za
jaką cenę."*

---

## 1. Metadane / nagłówek dokumentu (sekcja 0. Karta dokumentu)

Tabela z sekcji 0.1 (linie 30–58):

| Pole | Wartość |
|---|---|
| Wersja | 0.1 – model bazowy |
| Status | Projekt do iteracji, pilotażu, walidacji metodologicznej i audytu bezpieczeństwa |
| Zakres | Hipotezy, protokoły, punkt odniesienia, pomiary, ekspozycja, zgodność wykonania, bezpieczeństwo, analiza, postęp i uczenie |
| Dokument nadrzędny | Warstwa 1 – Konstytucja i Wartości |
| Model osoby | Warstwa 2 – Model Człowieka |
| Źródło wiedzy | Warstwa 3 – Mapa Wiedzy i Sygnatura Informacji |
| Kontekst osobisty | Warstwa 4 – Model Użytkownika i Cyfrowy Profil |
| Decyzja wejściowa | Warstwa 5 – Silnik Decyzji i Rekomendacji |
| Właściciel dokumentu | Zespół założycielski Human OS |
| Data | 2026-07-20 |

**Cel dokumentu** (0.1, linie 19–28): definiuje sposób, w jaki Human OS zamienia świadomie
wybraną rekomendację w wykonywalny, monitorowany i oceniany proces zmiany — hipoteza, mierniki,
punkt odniesienia, protokół, bezpieczeństwo, analiza wyniku, uczenie modelu użytkownika oraz
(po odrębnej zgodzie) zanonimizowany wkład do wiedzy zbiorowej. Zastrzeżenie: "Nie ma prawa
fabrykować pewności, wymuszać wykonania ani przedstawiać korelacji jako dowodu przyczynowego."

**Zakres obowiązywania** (0.2, linie 60–79):
- Obejmuje: eksperymenty N-of-1, wdrażanie nawyków, obserwacje bez interwencji, protokoły
  rozwojowe, testy refleksyjne, monitorowanie działań zaleconych przez specjalistę, ocenę
  utrzymania efektu.
- Obowiązuje: projektantów produktu, twórców modeli AI, metodologów, ekspertów domenowych,
  zespoły bezpieczeństwa, analityków danych, badaczy UX, audytorów.
- Nie obejmuje: samodzielnego diagnozowania chorób, projektowania nielegalnych/rażąco
  niebezpiecznych procedur, zastępowania lekarza, ukrytego eksperymentowania na użytkownikach.
- Rozróżnia: poprawę stanu, uczenie się o sobie, zmianę zachowania, zmianę biomarkera, efekt
  chwilowy, efekt utrzymany, brak rozstrzygnięcia.
- Podlega: prawom użytkownika, minimalizacji danych, progom dowodowym zależnym od ryzyka,
  obowiązkowi bezpiecznej eskalacji.

**Test nadrzędny** (0.5, linie 178–187) — zasada bramkująca uruchomienie eksperymentu:
> "Jeżeli system nie potrafi wyjaśnić: co dokładnie sprawdza, dlaczego ten protokół jest
> dopuszczalny, jaki jest punkt odniesienia, co zostanie zmierzone, jak rozpoznać szkodę, kiedy
> przerwać, które czynniki mogą zakłócić wynik i jaką decyzję umożliwi rezultat - eksperyment nie
> może zostać uruchomiony."

---

## 2. Nazwane decyzje architektoniczne w stylu ADR

**Brak.** Przeszukano cały dokument pod kątem wzorca `ADR-` — nie znaleziono ani jednego
wystąpienia. Dokument nie zawiera dedykowanej sekcji z listą ADR, w przeciwieństwie do niektórych
innych artefaktów projektu Human OS (np. `docs/adr/` w repozytorium kodu). Warstwa 6 jest
dokumentem specyfikacyjnym/projektowym (16 aksjomatów w sekcji 1, kryteria akceptacji w sekcji
47, deklaracja w Załączniku V), ale nie formalizuje decyzji w formacie ADR z numeracją. Jeśli
"Reconstruction Audit"/nowe ADR mają odnosić się do tego dokumentu, trzeba je utworzyć od zera —
nie ma tu istniejących ADR-ów do zmapowania.

Najbliższym odpowiednikiem "decyzji architektonicznych" są:
- 16 aksjomatów w sekcji 1 (linie 191–273) — zasady wiążące każdy protokół/pomiar/analizę,
- sekcja 39 "Referencyjna architektura techniczna" (moduły systemowe, linie 2513–2580),
- sekcja 47 "Kryteria akceptacji Warstwy 6" (lista twardych wymagań, linie 2960–3013).

---

## 3. Kluczowe encje / kontrakty danych

### 3.1 Ontologia obiektów eksperymentalnych (sekcja 4, linie 482–542)

Tabela "Obiekt / Obowiązkowe pola / Relacje":

| Obiekt | Obowiązkowe pola | Relacje |
|---|---|---|
| Experiment | ID, właściciel, cel, klasa, status, wersja, daty | łączy hipotezę, protokół, mierniki, zgody, wyniki |
| Hypothesis | treść, kierunek, horyzont, mechanizm, pewność, alternatywy | odnosi się do twierdzeń Warstwy 3 i celu Warstwy 5 |
| Protocol | interwencja, ekspozycja, harmonogram, warunki, wersja | steruje sesjami, przypomnieniami i zgodnością wykonania |
| EligibilityRule | kryterium wejścia, wykluczenie, źródło, twardość | wiąże profil użytkownika z bezpieczeństwem |
| Metric | nazwa, typ, jednostka, metoda, kierunek, próg | generuje obserwacje i wyniki |
| BaselineWindow | okres, liczba pomiarów, stabilność, jakość | porównywany z fazami eksperymentu |
| ExposureEvent | czas, ilość, jakość, potwierdzenie, odstępstwo | opisuje rzeczywiste wykonanie |
| Observation | czas, wartość, źródło, kontekst, jakość | zasila analizę wyniku |
| ContextEvent | typ, początek, koniec, wpływ, pewność | oznacza zakłócenia i zmiany warunków |
| SafetyEvent | objaw, nasilenie, czas, związek, reakcja | może uruchomić hold, stop lub eskalację |
| ProtocolDeviation | odstępstwo, przyczyna, zakres, wpływ | obniża lub modyfikuje interpretowalność |
| AnalysisPlan | porównania, progi, sposób braków, reguły interpretacji | ustanawiany przed analizą główną |
| Result | zmiana, pewność, znaczenie praktyczne, skutki uboczne | aktualizuje dowód osobisty i decyzję |
| PostExperimentDecision | kontynuacja, modyfikacja, powtórzenie, zakończenie | przekazywana Warstwie 5 i 4 |
| CommunityContribution | minimalny raport, anonimizacja, jakość, zgoda | opcjonalnie przekazywany Warstwie 3 |

**4.1 Identyfikowalność i wersje**: każdy obiekt ma stabilny identyfikator, czas utworzenia,
źródło, wersję i historię zmian. Wynik zawsze wskazuje dokładną wersję protokołu, planu analizy
i modelu AI użytego do interpretacji. Edycja danych źródłowych nie może po cichu zmienić
historycznej decyzji — tworzy nową wersję i nową analizę.

**4.2 Zakaz ukrytego scalania**: doświadczenie (samoopis), pomiar z urządzenia, wynik
laboratoryjny, przewidywanie modelu i interpretacja eksperta pozostają osobnymi obiektami —
system może pokazać zgodność/konflikt, ale nie może zlać ich w jedną liczbę bez zachowania
pochodzenia.

### 3.2 Kontrakty wejściowe/wyjściowe (sekcja 5)

**5.1 Minimalny pakiet wejściowy**: jawny cel użytkownika i decyzja, którą ma umożliwić wynik;
wybrana/zaakceptowana rekomendacja z Warstwy 5; profil ryzyka, przeciwwskazania, interakcje,
warunki dopuszczenia; minimalny kontekst do kwalifikacji i pomiaru; przewidywany horyzont efektu
i znane źródła niepewności; prawo do przerwania, zmiany zakresu danych i odmowy udziału w wiedzy
zbiorowej.

**5.3 Kontrakt wyjściowy** — każde zakończenie procesu musi zwrócić: status wykonania, jakość
danych, zmianę głównych i ochronnych mierników, działania niepożądane, poziom pewności,
ograniczenia, decyzję po eksperymencie, dane wymagające aktualizacji profilu, informację czy
wynik nadaje się do anonimowej agregacji.

### 3.3 Struktura hipotezy operacyjnej (7.1, linie 676–685)

Szablon: *"U osoby o [istotny kontekst], wykonanie [interwencja i ekspozycja] przez [czas]
prawdopodobnie spowoduje [kierunek i minimalna wielkość zmiany] w [miernik główny], bez
przekroczenia [mierniki ochronne / ryzyko], ponieważ [mechanizm lub wzorzec]. Wynik zostanie
użyty do decyzji [kontynuować / zmienić / odrzucić / zbadać dalej]."*

Hipotezy zerowa i alternatywne (7.3): H0 (brak zmiany ponad naturalną zmienność/próg), H1
(zmiana wynika głównie z interwencji), H2 (zmiana z oczekiwań/uwagi/sezonu/regresji do
średniej/innego zdarzenia), H3 (inny mechanizm niż zakładano), H4 (efekt dotyczy tylko części
domen, równoważony kosztem w innych), H5 (protokół niewykonalny, skuteczność nierozstrzygnięta).

### 3.4 Obowiązkowe elementy protokołu (11.1, linie 992–1029)

Cel, Interwencja, Ekspozycja, Fazy (baseline, aktywna, washout/obserwacja, podtrzymanie, review),
Mierniki (główny/ochronny/procesu/kontekst + harmonogram), Progi (sukces/pogorszenie/stop/wynik
nierozstrzygający), Zakłócenia, Bezpieczeństwo (czerwone flagi/reakcja/kontakt/eskalacja),
Obciążenie (czas/koszt/wysiłek/plan uproszczenia), Wersja (numer/data/autor/źródła/historia
zmian), Decyzja po wyniku.

### 3.5 Załączniki-formularze (karty pól, sekcja końcowa) — pełne listy pól

- **Załącznik A — Karta kontraktu eksperymentu**: ID i wersja, Właściciel celu, Cel użytkownika,
  Decyzja po wyniku, Klasa procesu XP, Profil ryzyka, Alternatywy, Zakres danych, Zgody, Data
  przeglądu/wygaśnięcia.
- **Załącznik B — Karta hipotezy operacyjnej**: Hipoteza główna, Hipoteza zerowa, Hipotezy
  alternatywne, Kontekst osoby, Interwencja i ekspozycja, Oczekiwany kierunek, Horyzont,
  Mechanizm/źródła, Próg praktyczny, Mierniki ochronne, Decyzja umożliwiona wynikiem.
- **Załącznik C — Karta protokołu**: Nazwa i wersja, Warunki wejścia, Faza baseline, Interwencja,
  Ekspozycja, Harmonogram, Miernik główny, Mierniki wtórne, Mierniki ochronne, Zdarzenia
  zakłócające, Kryteria HOLD, Kryteria STOP, Plan washout/follow-up, Obciążenie, Historia zmian.
- **Załącznik D — Karta miernika**: Nazwa, Rola (główny/wtórny/proces/ochronny/obciążenia/
  utrzymania), Definicja, Jednostka/skala, Źródło, Procedura, Okno pomiaru, Kierunek korzystny,
  Próg praktyczny, Próg bezpieczeństwa, Jakość MQ, Znane ograniczenia, Retencja i prywatność.
- **Załącznik F — Karta kwalifikacji i bezpieczeństwa**: Cel i wartość, Stan aktualny,
  Przeciwwskazania, Leki i interakcje, Inne interwencje, Zasoby i sprzęt, Zdolność
  monitorowania, Nadchodzące zakłócenia, Zgoda, Legalność, Nadzór specjalisty, Plan eskalacji
  (każde ze statusem i uwagami/źródłem).
- **Załącznik G — Minimalny dzienny check-in**: Czy wykonałeś dzisiejszy krok? (tak/częściowo/
  nie/nie dotyczy), Wartość miernika głównego, Wartość miernika ochronnego, Czy wydarzyło się
  coś, co mogło wpłynąć na wynik? (nie/kategoria/opis), Czy pojawił się niepokojący objaw?
  (nie / tak — uruchom ścieżkę bezpieczeństwa), Czy chcesz kontynuować jutro? (tak/zmodyfikować/
  wstrzymać/zakończyć).
- **Załącznik H — Raport zdarzenia bezpieczeństwa**: Czas i faza, Objaw/zdarzenie, Nasilenie SE,
  Początek i przebieg, Ostatnia ekspozycja, Inne możliwe czynniki, Wpływ na funkcjonowanie,
  Podjęte działanie, Status HOLD/STOP/ESCALATE, Kontakt ze specjalistą, Dalszy monitoring, Zgoda
  na anonimowy sygnał bezpieczeństwa.
- **Załącznik I — Log odstępstwa i zakłócenia**: kolumny Data, Typ, Opis, Wpływ na ekspozycję,
  Wpływ na wynik, Decyzja.
- **Załącznik J — Plan analizy**: Miernik główny, Fazy do porównania, Próg znaczenia, Próg
  bezpieczeństwa, Sposób podsumowania (średnia/mediana/trend/liczba dni/kategoria), Braki
  danych, Dni zakłócone, Analizy wtórne, Kryteria nierozstrzygnięcia, Skala przyczynowości,
  Autor i wersja.
- **Załącznik K — Karta wyniku**: Wykonanie PF, Jakość danych DQ, Jakość baseline BL, Zmiana
  główna, Zmiana ochronna, Znaczenie praktyczne, Koszt i obciążenie, Działania niepożądane,
  Pewność przyczynowa CA, Trwałość, Klasa wyniku, Następna decyzja (każde z Oceną i
  Uzasadnieniem).

---

## 4. Bramy ryzyka/bezpieczeństwa i reguły eskalacji

**Uwaga terminologiczna**: dokument NIE używa skali "R0–R4" (to pojęcie z Konstytucji/Warstwy 1
wg CLAUDE.md tego repozytorium — nie znaleziono w tym pliku). Warstwa 6 definiuje własny,
odrębny zestaw skal kodowanych literowo, wypisany zbiorczo w Załączniku M (linie 3335–3363):

| Obszar | Kody |
|---|---|
| Klasy procesu | XP-0 do XP-8 |
| Kompletność kontraktu | EC0 do EC5 |
| Jakość baseline | BL0 do BL5 |
| Jakość pomiaru | MQ0 do MQ5 |
| Wierność protokołu | PF0 do PF5 |
| Jakość danych | DQ0 do DQ5 |
| Bezpieczeństwo | SE0 do SE4 |
| Pewność przyczynowa | CA0 do CA5 |
| Dowód osobisty | PE0 do PE5 |
| Wynik | R+, R?+, R0, R?0, R-, R±, RL, RW |
| Stan cyklu | DRAFT, BASELINE, ACTIVE, HOLD, WASHOUT, MAINTENANCE, COMPLETED, STOPPED, INCONCLUSIVE |

### 4.1 Klasy procesów XP-0..XP-8 (2.2, linie 319–366) — najbliższy odpowiednik skali ryzyka

| Kod | Klasa | Cel |
|---|---|---|
| XP-0 | Obserwacja bez interwencji | Poznać naturalny wzorzec/baseline |
| XP-1 | Mikrointerwencja | Mała, odwracalna zmiana o niskim obciążeniu |
| XP-2 | Budowanie nawyku | Zwiększyć stabilność zachowania |
| XP-3 | Eksperyment porównawczy | Porównać dwa dopuszczalne warianty |
| XP-4 | Faza odstawienia lub powrotu | Sprawdzić utrzymanie, odwracalność, carry-over |
| XP-5 | Monitorowanie planu specjalisty | Wsparcie wykonania i bezpieczeństwa zaleconej terapii |
| XP-6 | Praktyka refleksyjna | Testowanie użyteczności narracji/rytuału |
| XP-7 | Eksperyment wysokiej kontroli | Wymaga nadzoru, badań lub formalnej akceptacji specjalisty |
| XP-8 | **Niedopuszczalny** | Odrzucić proces bez proporcjonalnego bezpieczeństwa lub legalności (przykład: nielegalna/skrajnie ryzykowna substancja) |

### 4.2 Klasy zdarzeń bezpieczeństwa SE0-SE4 (15.2, linie 1294–1319)

| Klasa | Opis | Domyślna reakcja |
|---|---|---|
| SE0 | Brak objawów / oczekiwany łagodny dyskomfort | Kontynuacja i obserwacja |
| SE1 | Łagodny, przejściowy objaw bez utraty funkcji | Dodatkowy monitoring; możliwa korekta |
| SE2 | Umiarkowany objaw, pogorszenie funkcji lub narastający trend | Hold, ocena i możliwa konsultacja |
| SE3 | Poważny objaw, ryzyko zdrowotne lub znacząca utrata funkcji | Natychmiastowe stop i eskalacja |
| SE4 | Stan nagły lub potencjalne zagrożenie życia | Instrukcja natychmiastowej pomocy; brak dalszego eksperymentowania |

### 4.3 Kryteria przerwania (15.3, linie 1321–1337)
Wystąpienie zdefiniowanej czerwonej flagi; przekroczenie progu miernika ochronnego lub
narastający wzorzec pogorszenia; nowa informacja o interakcji/przeciwwskazaniu/nielegalności;
wycofanie zgody lub zmiana celu; utrata zdolności do świadomego uczestnictwa; brak możliwości
bezpiecznego monitorowania; wykrycie błędu protokołu/urządzenia/danych o potencjalnym wpływie na
bezpieczeństwo.

### 4.4 Statusy Hold/Stop/Escalate (15.4, linie 1339–1360)

| Status | Znaczenie | Co dalej |
|---|---|---|
| HOLD | Czasowe wstrzymanie bez przesądzania o wyniku | Ocena zdarzenia, brak dalszej ekspozycji, decyzja o wznowieniu lub stop |
| STOP | Zakończenie interwencji | Monitoring ustępowania, dokumentacja, decyzja bezpieczeństwa |
| ESCALATE | Przekazanie do specjalisty lub służb | Pakiet informacji, jasny powód i priorytet |
| SYSTEM PAUSE | Wstrzymanie danego protokołu dla wszystkich | Audyt źródeł, wzorca szkód i wersji |

### 4.5 Ścieżka eksperymentu wysokiego ryzyka (sekcja 34, linie 2277–2311)
Warunki minimalne dla XP-7/wysokiego ryzyka: legalność interwencji i źródła; wyraźna wartość
celu nieosiągalna bezpieczniejszą drogą; odpowiednio silne źródła wiedzy do poziomu ryzyka;
kwalifikacja i nadzór właściwego specjalisty; plan badań/monitorowania/alarmów/opieki po
zdarzeniu; udokumentowana zgoda po przedstawieniu alternatyw; zdolność przerwania i bezpiecznego
odzyskania kontroli; **zakaz automatycznego zwiększania ekspozycji przez AI**. "Determinacja
użytkownika nie obniża progu bezpieczeństwa" (34.2) — AI może informować, wskazywać luki,
ułatwiać rozmowę ze specjalistą, ale "nie tworzy szczegółowego protokołu wykonawczego dla
działania rażąco ryzykownego, nielegalnego albo pozbawionego realnej możliwości monitorowania."

### 4.6 Pętle wsteczne procesu (3.2, linie 464–480)
- Nowe działanie niepożądane cofa proces z X8 (Prowadzenie i monitoring) do X2 (Kwalifikacja i
  bezpieczeństwo) i może natychmiast uruchomić wstrzymanie.
- Brak jakości baseline cofa proces z X9 (Analiza) do X4 (Punkt odniesienia) albo wymusza wynik
  nierozstrzygający.
- Zmiana celu użytkownika cofa proces do X1 (Kontrakt eksperymentu).
- Nieoczekiwany korzystny efekt tworzy hipotezę wtórną, ale nie wolno przepisać głównej hipotezy
  po wyniku bez oznaczenia analizy eksploracyjnej.
- Powtarzające się niewykonanie może cofnąć proces do projektu protokołu zamiast zwiększać
  presję na użytkownika.

### 4.7 Zasada nierównoważności rzędów (3.1)
"Nie wolno kompensować braku bezpieczeństwa wysoką wartością uczenia, braku punktu odniesienia
dużą liczbą późniejszych pomiarów ani braku zgody techniczną łatwością zbierania danych."

### 4.8 Rola AI — funkcje niedozwolone bez dodatkowej kontroli (37.2, linie 2445–2463)
Autonomiczne rozpoczynanie eksperymentu lub zmiana zgody; ustalanie dawkowania leków/substancji
wysokiego ryzyka/terapii wymagającej specjalisty; ukrywanie niekorzystnych danych dla
utrzymania motywacji; zmiana progów sukcesu po zobaczeniu wyniku; diagnozowanie na podstawie
wzorca N-of-1; przekazywanie danych społeczności bez aktywnej zgody; optymalizacja czasu w
aplikacji jako celu eksperymentu; wykorzystywanie systemów symbolicznych do medycznej
kwalifikacji.

### 4.9 Kryteria akceptacji Warstwy 6 (sekcja 47) — pełna lista bramkowa
Zawiera m.in.: "Proces wysokiego ryzyka nie może zostać uruchomiony bez wymaganych warunków i
człowieka"; "AI nie może autonomicznie omijać bram, zmieniać terapii ani przepisywać kryteriów
po wyniku"; "System potrafi wydać wynik nierozstrzygający bez nacisku na przedłużenie";
"Użytkownik może wstrzymać, zakończyć, poprawić dane, wycofać zgodę i eksportować historię."

Zamykająca "Kluczowa zasada Warstwy 6" (linie 3008–3013): *"Human OS nie eksperymentuje na
użytkowniku. Użytkownik - w granicach bezpieczeństwa i własnej zgody - prowadzi przejrzysty
proces uczenia się, a system pomaga mu zaprojektować, wykonać, zrozumieć i zakończyć ten
proces."*

---

## 5. Kluczowa terminologia (0.3 "Podstawowe terminy", linie 81–150)

| Termin | Definicja |
|---|---|
| Eksperyment osobisty | Ograniczony w czasie, jawny proces sprawdzania hipotezy poprzez interwencję lub obserwację u jednego użytkownika. |
| Hipoteza operacyjna | Precyzyjne, możliwe do zakwestionowania przewidywanie dotyczące kierunku, czasu i warunków zmiany. |
| Protokół | Zapis tego, co ma być wykonane, kiedy, jak długo, w jakiej kolejności, co będzie mierzone i kiedy należy przerwać. |
| Punkt odniesienia | Opis stanu przed interwencją, wraz z jego zmiennością, kontekstem i jakością pomiaru. |
| Ekspozycja | Rzeczywisty kontakt z interwencją: dawka, czas, częstotliwość, intensywność lub wykonana praktyka. |
| Wierność wykonania | Stopień zgodności rzeczywistego działania z uzgodnionym protokołem. |
| Miernik wyniku | Zmienna wybrana do oceny, czy zaszła istotna zmiana. |
| Miernik procesu | Zmienna opisująca wykonanie, warunki lub mechanizm pośredni, np. czas snu albo liczba sesji. |
| Zdarzenie zakłócające | Czynnik niezaplanowany, który mógł wpłynąć na wynik, np. infekcja, podróż, zmiana leku albo stres. |
| Próg istotnej zmiany | Ustalona wcześniej wielkość lub jakość zmiany, która ma znaczenie praktyczne dla użytkownika. |
| Efekt utrzymany | Zmiana obecna po zakończeniu interwencji lub po przejściu do fazy podtrzymania. |
| Wynik nierozstrzygający | Rezultat, którego nie można uczciwie sklasyfikować z powodu danych, wykonania, czasu lub zakłóceń. |
| Dowód osobisty | Uporządkowany zapis wyników dotyczących konkretnego użytkownika; nie jest automatycznie dowodem dla populacji. |
| Postęp | Kierunkowa poprawa zdolności, stanu, funkcjonowania lub spójności z wartościami, oceniana w odpowiednim horyzoncie. |
| Regres | Pogorszenie lub utrata wcześniej osiągniętej zdolności, które wymaga interpretacji, a nie moralnej oceny. |

Poza tym słowniczkiem, dokument definiuje dalsze pojęcia rozproszone w treści (nie w tabeli
terminów), m.in.:
- **Antywynik** (8.3) — wynik, którego użytkownik chce uniknąć (np. pogorszenie snu/lęku/relacji);
  ma własny próg i może zakończyć eksperyment nawet gdy miernik główny się poprawia.
- **Kontrfakt praktyczny** (26.3) — hipoteza o tym, co najprawdopodobniej wydarzyłoby się bez
  interwencji; "pozostaje hipotezą. Nie wolno go przedstawiać jako zaobserwowanego faktu."
  Wnioskuje się z baseline, wcześniejszych epizodów, faz kontrolnych i trendów.
- **Zapora epistemiczna** (32.4) — zasada, że dane z eksperymentów refleksyjnych/symbolicznych
  (np. Human Design, astrologia) są przechowywane w domenie interpretacyjnej i "nie podnoszą
  siły dowodów biologicznych, klinicznych ani przyczynowych w Mapie Wiedzy".
- **Eksperymenty infrastrukturalne** (29.3) — zmiany (stała pora snu, regularne posiłki,
  rehabilitacja, leki wg zalecenia), które po potwierdzeniu wartości "przechodzą do utrzymania i
  nie konkurują o uwagę jak aktywna hipoteza".

---

## 6. Relacje z innymi warstwami / komponentami Human OS

Podsumowanie interfejsów, sekcja 38 "Interfejsy z pozostałymi warstwami Human OS" (linie
2478–2504), tabela "Warstwa / Dane przyjmowane / Dane zwracane":

| Warstwa | Dane przyjmowane przez Warstwę 6 | Dane zwracane przez Warstwę 6 |
|---|---|---|
| 1. Konstytucja | prawa, zakazy, klasy ryzyka, zasady zgody | log zgodności, naruszenia, precedensy |
| 2. Model Człowieka | domeny, zależności, dynamika i kontekst | obserwowane zmiany i koszty między domenami |
| 3. Mapa Wiedzy | twierdzenia, protokoły bazowe, horyzont, ryzyko | ustrukturyzowane wyniki społeczności i sygnały szkód |
| 4. Model Użytkownika | cele, baseline, zasoby, preferencje, historia | dowód osobisty, nowe hipotezy, wykonanie, preferencje |
| 5. Silnik Decyzji | wybrany kandydat, uzasadnienie, warunki i alternatywy | wynik, decyzja po eksperymencie, potrzeba nowego wyboru |
| 7. Inteligencja zbiorowa | wzorce podobnych przypadków i jakość | zanonimizowany raport oraz niekorzystne zdarzenia |

Dodatkowe szczegóły relacyjne rozproszone w tekście:

- **Warstwa 1 (Konstytucja)**: "Dokument nadrzędny" (nagłówek 0.1). "Każdy protokół przepuszcza
  przez prawa i zakazy Warstwy 1" (0.4). Sekcja X0 "Brama konstytucyjna" pyta: "Czy cel, metoda
  i zbieranie danych są zgodne z prawami użytkownika?" (sekcja 3, rząd X0).
- **Warstwa 2 (Model Człowieka)**: "Model osoby". "Interpretuje wynik poprzez model domen i
  zależności Warstwy 2, aby nie uznać lokalnej poprawy za globalne dobro bez sprawdzenia kosztów
  ubocznych" (0.4). Wymieniona też jako zabezpieczenie przed trybem awarii "Efekt lokalny maskuje
  koszt globalny" (sekcja 43).
- **Warstwa 3 (Mapa Wiedzy i Sygnatura Informacji)**: "Źródło wiedzy". "Korzysta z Warstwy 3 do
  ustalenia oczekiwanego mechanizmu, typowego czasu efektu, znanych działań niepożądanych,
  interakcji i siły dowodów" (0.4). "Przekazuje Warstwie 3 wyłącznie odpowiednio zanonimizowane,
  ustrukturyzowane i oznaczone jakościowo wyniki społeczności" (0.4). Protokół bazowy "pochodzi z
  Mapy Wiedzy i zawiera zakres typowy" (11.3). Horyzont efektu "pochodzi z Mapy Wiedzy" (21.3).
- **Warstwa 4 (Model Użytkownika i Cyfrowy Profil)**: "Kontekst osobisty". "Korzysta z Warstwy 4
  do dopasowania obciążenia, mierników, częstotliwości kontaktu, sposobu komunikacji i osobistego
  punktu odniesienia" (0.4). "Przekazuje Warstwie 4 nowe obserwacje, wyniki, koszty, preferencje
  i zaktualizowane hipotezy osobiste" (0.4).
- **Warstwa 5 (Silnik Decyzji i Rekomendacji)**: "Decyzja wejściowa". "Przyjmuje z Warstwy 5 cel,
  wybraną rekomendację, alternatywy, założenia, profil ryzyka, warunki dopuszczenia i kryteria
  przerwania" (0.4). PostExperimentDecision jest "przekazywana Warstwie 5 i 4" (ontologia
  obiektów, sekcja 4).
- **Warstwa 7 ("Inteligencja zbiorowa")**: wspomniana wyłącznie w tabeli interfejsów sekcji 38 —
  przyjmuje "wzorce podobnych przypadków i jakość", otrzymuje "zanonimizowany raport oraz
  niekorzystne zdarzenia". Nie jest opisana nigdzie indziej w dokumencie z nazwy (nie ma odrębnej
  sekcji "Warstwa 7" poza tym wierszem tabeli) — traktować jako odniesienie do warstwy poza
  zakresem tego pliku.
- **Hub / Digital Twin / Knowledge Graph** — te nazwy własne (używane w repozytorium kodu:
  `hub/`, `knowledge_graph.py`) **nie pojawiają się** w tym dokumencie. Warstwa 6 odnosi się do
  "Mapy Wiedzy" (Warstwa 3) jako źródła wiedzy, a nie do "Knowledge Graph"/"Hub" nazwanych
  explicite — nie zakładać 1:1 mapowania na moduły kodu bez dodatkowej weryfikacji.
- **Human Design / astrologia / systemy interpretacyjne**: odrębna sekcja 32 (linie 2174–2225) —
  traktowane jako dopuszczalny *przedmiot* eksperymentu behawioralnego/refleksyjnego (np.
  hipoteza o wpływie 24h odroczenia decyzji), ale odgrodzone "zaporą epistemiczną" od wnioskowania
  medycznego/przyczynowego (32.4).

**38.1 Kontrakt błędu**: "Każdy moduł może zwrócić brak, konflikt, niską pewność albo
niedostępność. Warstwa 6 nie zastępuje tych stanów domysłami. Przechodzi do bezpieczniejszego
projektu, obserwacji, odroczenia, wyniku nierozstrzygającego albo eskalacji."

---

## 7. Explicit prohibitions ("nie ma prawa" / "nie wolno" / "zabrania się")

Dokument nie zawiera frazy "zabrania się" ani żadnej odmiany "nie ma prawa" poza jednym
wystąpieniem na początku dokumentu. Pełna lista dosłownych cytatów (wyszukano wzorce
case-insensitive w całym pliku):

1. (linia 27, sekcja 0.1) — *"Nie ma prawa fabrykować pewności, wymuszać wykonania ani
   przedstawiać korelacji jako dowodu przyczynowego."*
2. (linia 223, Aksjomat 6) — *"Nie wolno uznać interwencji za nieskuteczną, jeśli nie została
   rzeczywiście wykonana, ani uznać jej za skuteczną wyłącznie dlatego, że była wykonywana."*
3. (linia 458, 3.1 Zasada nierównoważności rzędów) — *"Nie wolno kompensować braku
   bezpieczeństwa wysoką wartością uczenia, braku punktu odniesienia dużą liczbą późniejszych
   pomiarów ani braku zgody techniczną łatwością zbierania danych."*
4. (linia 748, 7.4 Zakaz przepisywania hipotezy po wyniku) — *"Nie wolno przedstawiać go
   [nowego wyjaśnienia] jako wcześniej przewidzianego."*
5. (linia 1260, 14.3 Redukcja obciążenia) — *"Nie wolno automatycznie redukować elementów
   bezpieczeństwa."*
6. (linia 1896, 26.3 Kontrfakt praktyczny) — *"Nie wolno go [kontrfaktu] przedstawiać jako
   zaobserwowanego faktu."*
7. (linia 2194, 32.2 Niedopuszczalne wnioski) — *"Nie wolno uznać zgodności kilku obserwacji za
   dowód prawdziwości kosmologii lub mechanizmu biologicznego systemu."*
8. (linia 2197, 32.2) — *"Nie wolno używać mapy symbolicznej do diagnozy, dawkowania, oceny
   ryzyka medycznego ani przewidywania zdarzeń jako faktów."*
9. (linia 2200, 32.2) — *"Nie wolno przedstawiać niezgodności jako błędu użytkownika,
   niedojrzałości albo niewłaściwego życia swoim typem."*
10. (linia 2203, 32.2) — *"Nie wolno zamykać użytkownika w trwałej etykiecie ani ograniczać mu
    ścieżek rozwoju."*

Dodatkowe zdania z tytułami sekcji "Zakaz ..." (nie zawsze dosłownie zawierają słowo "wolno", ale
formułują wiążący zakaz):
- **4.2 Zakaz ukrytego scalania** (linie 552–557) — system "nie może zlać ich [obiektów
  danych] w jedną liczbę bez zachowania pochodzenia."
- **12.4 Zakaz moralizacji zgodności** (linie 1146–1151) — "System nie używa etykiet takich jak
  leniwy, niezdyscyplinowany czy niewspółpracujący."
- **2296, sekcja 34.1** — *"Zakaz automatycznego zwiększania ekspozycji przez AI."*
- **40.3 Zakazane wzorce wizualne** (linie 2622–2635) — lista zakazanych wzorców UI, m.in.
  "Czerwone alarmy dla neutralnych wahań i zielone pochwały dla ryzykownego przekraczania celu",
  "Jedna syntetyczna ocena zdrowia maskująca różne domeny i niepewność", "Gamifikacja
  zachęcająca do kontynuacji mimo szkody", "Ukrywanie kosztów i działań niepożądanych pod
  ekranem sukcesu".
- **3408, Załącznik O.2** — *"Zakaz samotnego testowania w sytuacji ryzyka utraty
  przytomności lub w środowisku, z którego trudno wyjść."*

Inne silne normatywne zdania warte odnotowania (bez dokładnie "nie wolno", ale równie wiążące):
- (2.3 Granice, linie 368–386) siedem stwierdzeń "Nie ... " opisujących granice Warstwy 6, np.
  "Nie tworzy diagnozy na podstawie eksperymentu osobistego", "Nie prowadzi ukrytych testów A/B
  dotyczących zdrowia, emocji lub zachowania użytkownika bez świadomej zgody", "Nie wykorzystuje
  zaangażowania jako zastępczego miernika dobrostanu", "Nie łączy danych do wiedzy zbiorowej bez
  odrębnej zgody i kontroli prywatności".
- (28.2 Niedozwolone adaptacje, linie 1996–2014) pięć zakazanych zmian protokołu w trakcie
  eksperymentu, m.in. "Usunięcie niekorzystnych dni albo działań niepożądanych dla poprawy
  obrazu", "Automatyczne dokładanie kolejnej interwencji, gdy pierwsza nie działa".
- (22.2 Nocebo) — *"System nie ukrywa zagrożeń..."*
- (Załącznik R.1, wysokiego ryzyka iniekcja) — *"Warstwa 6 nie generuje dawkowania, schematu
  iniekcji ani instrukcji wykonawczej."*
- (Deklaracja, Załącznik V) — *"Human OS traktuje każdą zmianę jako możliwość uczenia, nie jako
  test wartości człowieka."*

---

## 8. Struktura dokumentu (spis treści wg nagłówków)

```
HUMAN OS — WARSTWA 6 — SILNIK EKSPERYMENTÓW, MONITOROWANIA I POSTĘPU

0.   Karta dokumentu i sposób stosowania
  0.1  Cel dokumentu
  0.2  Zakres obowiązywania
  0.3  Podstawowe terminy
  0.4  Odpowiedzialność Warstwy 6
  0.5  Test nadrzędny
1.   Aksjomaty Silnika Eksperymentów (16 aksjomatów)
2.   Rola, granice i klasy procesów eksperymentalnych
  2.1  Główne role Warstwy 6
  2.2  Klasy procesów (XP-0..XP-8)
  2.3  Granice
3.   Wielorzędowa architektura procesu eksperymentalnego (X0..X11)
  3.1  Zasada nierównoważności rzędów
  3.2  Pętle wsteczne
4.   Ontologia obiektów eksperymentalnych
  4.1  Identyfikowalność i wersje
  4.2  Zakaz ukrytego scalania
5.   Kontrakty wejściowe i wyjściowe
  5.1  Minimalny pakiet wejściowy
  5.2  Klasy kompletności kontraktu EC0-EC5
  5.3  Kontrakt wyjściowy
6.   Kwalifikacja użytkownika, kontekstu i interwencji
  6.1  Wymiary kwalifikacji
  6.2  Kwalifikacja dynamiczna
  6.3  Brak danych a bezpieczeństwo
7.   Formułowanie hipotezy i modelu zmiany
  7.1  Struktura hipotezy operacyjnej
  7.2  Typy hipotez
  7.3  Hipotezy alternatywne i zerowe
  7.4  Zakaz przepisywania hipotezy po wyniku
8.   Wyniki, antywyniki i kryteria sukcesu
  8.1  Hierarchia mierników
  8.2  Kryteria sukcesu
  8.3  Antywyniki
9.   Projektowanie mierników
  9.1  Wymiary jakości miernika
  9.2  Typy źródeł pomiaru
  9.3  Skala jakości pomiaru MQ0-MQ5
  9.4  Minimalny zestaw pomiarowy
10.  Punkt odniesienia i naturalna zmienność
  10.1 Funkcje baseline
  10.2 Klasy jakości baseline BL0-BL5
  10.3 Długość baseline
  10.4 Stabilizacja przed eksperymentem
11.  Projektowanie protokołu
  11.1 Obowiązkowe elementy
  11.2 Zasada najmniejszej interwencji
  11.3 Protokoły bazowe i osobiste
  11.4 Zmiany protokołu
12.  Ekspozycja, wierność wykonania i zgodność
  12.1 Ekspozycja rzeczywista
  12.2 Skala wierności PF0-PF5
  12.3 Powody niewykonania
  12.4 Zakaz moralizacji zgodności
13.  Zdarzenia zakłócające, współinterwencje i kontekst
  13.1 Kategorie zakłóceń (CF-H..CF-U)
  13.2 Współinterwencje
  13.3 Regresja do średniej i spontaniczna poprawa
14.  Harmonogram, częstotliwość i budżet obciążenia
  14.1 Elementy harmonogramu
  14.2 Budżet obciążenia
  14.3 Redukcja obciążenia
15.  Monitorowanie bezpieczeństwa
  15.1 Warstwy bezpieczeństwa
  15.2 Klasy zdarzeń bezpieczeństwa SE0-SE4
  15.3 Kryteria przerwania
  15.4 Hold, stop i eskalacja
16.  Świadoma zgoda i kontrakt uczestnictwa
  16.1 Elementy zgody
  16.2 Zgoda warstwowa (C-EXP, C-SENSOR, C-SENSITIVE, C-SHARE, C-EXPERT, C-FOLLOW)
  16.3 Dynamiczna zgoda
17.  Cykl życia eksperymentu i statusy operacyjne
  17.1 Automatyczne wygaśnięcie
18.  Prowadzenie eksperymentu i codzienna interakcja
  18.1 Minimalistyczny check-in
  18.2 Tryby interakcji
  18.3 Przypomnienia
19.  Jakość danych, braki i korekty
  19.1 Wymiary jakości danych
  19.2 Klasy danych DQ0-DQ5
  19.3 Braki danych
20.  Projekty N-of-1 i schematy porównawcze
  20.1 Typy projektów
  20.2 Dobór projektu
  20.3 Losowanie i maskowanie
21.  Washout, efekt przeniesienia i opóźnienie
  21.1 Funkcje fazy washout
  21.2 Kiedy washout jest niewłaściwy
  21.3 Opóźnienie efektu
22.  Oczekiwania, placebo, nocebo i reaktywność pomiaru
  22.1 Oczekiwania jako zmienna
  22.2 Nocebo i komunikacja ryzyka
  22.3 Reaktywność pomiaru
23.  Plan analizy i ograniczenie dopasowywania wyniku
  23.1 Elementy planu
  23.2 Fałszywa precyzja
  23.3 Wielokrotne porównania
24.  Ocena zmiany i znaczenia praktycznego
  24.1 Wymiary efektu
  24.2 Próg minimalnie ważnej zmiany
  24.3 Zmiana statystyczna a życiowa
25.  Rozbieżność danych subiektywnych i obiektywnych
  25.1 Typowe konfiguracje
  25.2 Zasada nieredukowania doświadczenia
26.  Wnioskowanie przyczynowe w eksperymencie osobistym
  26.1 Minimalne pytania przyczynowe
  26.2 Skala pewności przyczynowej CA0-CA5
  26.3 Kontrfakt praktyczny
27.  Klasy wyniku i decyzja po eksperymencie (R+, R?+, R0, R?0, R-, R±, RL, RW)
  27.1 Decyzje po wyniku
28.  Eksperymenty adaptacyjne
  28.1 Dozwolone adaptacje
  28.2 Niedozwolone adaptacje
  28.3 Reguły zatrzymania adaptacji
29.  Portfel równoległych eksperymentów
  29.1 Limity aktywnych zmian
  29.2 Interakcje między eksperymentami
  29.3 Eksperymenty infrastrukturalne
30.  Model postępu i trajektorii
  30.1 Postęp wielowymiarowy
  30.2 Stany trajektorii
  30.3 Regres bez moralnej oceny
31.  Utrzymanie, wygaszanie i replikacja
  31.1 Przejście do utrzymania
  31.2 Wygaszanie monitorowania
  31.3 Replikacja
32.  Human Design, astrologia i systemy interpretacyjne w Warstwie 6
  32.1 Dopuszczalny przedmiot eksperymentu
  32.2 Niedopuszczalne wnioski
  32.3 Protokół hipotezy refleksyjnej
  32.4 Zapora epistemiczna
33.  Eksperymenty prowadzone lub nadzorowane przez specjalistę
  33.1 Role i odpowiedzialność
  33.2 Pakiet dla specjalisty
  33.3 Rozbieżność z zaleceniem specjalisty
34.  Ścieżka eksperymentu wysokiego ryzyka
  34.1 Warunki minimalne
  34.2 Determinacja użytkownika
  34.3 Redukcja szkód
35.  Wyniki społeczności i zbiorowe uczenie
  35.1 Minimalny raport społeczności
  35.2 Waga raportu
  35.3 Ochrona przed pętlą popularności
36.  Prywatność, własność danych i retencja
  36.1 Zasady
  36.2 Retencja zależna od funkcji
37.  Rola AI w Silniku Eksperymentów
  37.1 Funkcje dozwolone
  37.2 Funkcje niedozwolone bez dodatkowej kontroli
  37.3 Architektura z ograniczeniami
  37.4 Kalibracja i język
38.  Interfejsy z pozostałymi warstwami Human OS
  38.1 Kontrakt błędu
39.  Referencyjna architektura techniczna
  39.1 Moduły
  39.2 Deterministyczne reguły i modele probabilistyczne
  39.3 Tryb offline i degradacja
40.  Interfejs postępu i prezentacja wyniku
  40.1 Widok aktywnego eksperymentu
  40.2 Widok wyniku
  40.3 Zakazane wzorce wizualne
41.  Testowanie, walidacja i symulacje
  41.1 Poziomy testów
  41.2 Złote scenariusze
  41.3 Test zrozumienia
42.  Metryki jakości Warstwy 6
  42.1 Metryki podstawowe
  42.2 Antymetryki
43.  Tryby awarii i ryzyka systemowe
  43.1 Czerwone flagi organizacyjne
44.  Dostępność, sprawiedliwość i ochrona przed wykluczeniem
  44.1 Zasada równoważnej możliwości uczenia
  44.2 Źródła nierówności
  44.3 Audyt podgrup
45.  Integralność komercyjna
  45.1 Zasady
  45.2 Badania wewnętrzne produktu
46.  Audytowalność, role i zarządzanie
  46.1 Snapshot eksperymentu
  46.2 Role organizacyjne
  46.3 Zmiany wysokiego wpływu
47.  Kryteria akceptacji Warstwy 6  [+ "Kluczowa zasada Warstwy 6"]

Załączniki (A–V):
  A. Karta kontraktu eksperymentu
  B. Karta hipotezy operacyjnej
  C. Karta protokołu
  D. Karta miernika
  E. Checklista punktu odniesienia
  F. Karta kwalifikacji i bezpieczeństwa
  G. Minimalny dzienny check-in
  H. Raport zdarzenia bezpieczeństwa
  I. Log odstępstwa i zakłócenia
  J. Plan analizy
  K. Karta wyniku
  L. Drabina dowodu osobistego (PE0-PE5)
  M. Statusy i kody operacyjne (zbiorcza tabela wszystkich skal)
  N. Scenariusz: światło poranne i energia
  O. Scenariusz: ekspozycja na zimno
  P. Scenariusz: skóra i miejscowa interwencja
  Q. Scenariusz: praktyka Human Design
  R. Scenariusz: użytkownik chce eksperymentu iniekcyjnego wysokiego ryzyka
  S. Scenariusz: eksperyment przerwany
  T. Lista kontrolna audytu nowej funkcji
  U. Otwarte pytania do wersji 0.2
  V. Deklaracja Silnika Eksperymentów
```

---

## Dodatkowe obserwacje istotne dla audytu

- **Brak numeracji ADR** i brak jakiegokolwiek odniesienia do zewnętrznych ADR — jeśli
  Reconstruction Audit ma "zaimportować" decyzje z tego dokumentu do `docs/adr/` (wzorem
  `ADR-HUB-*`, `ADR-CORE-*` wspomnianych w CLAUDE.md repozytorium), trzeba je dopiero
  sformułować na podstawie aksjomatów (sekcja 1), architektury referencyjnej (sekcja 39) i
  kryteriów akceptacji (sekcja 47) — nie istnieją w źródle gotowe do wyciągnięcia.
  Nie jest to niniejszym audytem oceniane, po prostu odnotowuję fakt: sekcja "ADR" nie
  istnieje.
- Dokument jawnie zaznacza swój status jako **"Wersja 0.1 – model bazowy"**, "Projekt do
  iteracji, pilotażu, walidacji metodologicznej i audytu bezpieczeństwa" — czyli deklaratywnie
  niedojrzały/niewalidowany, spójnie z resztą projektu Human OS (BETA, brak niezależnego
  audytu bezpieczeństwa, zgodnie z README repo kodu).
  - Załącznik U ("Otwarte pytania do wersji 0.2") zawiera 12 nierozstrzygniętych pytań
    metodologicznych/etycznych (baseline, minimalnie ważna zmiana w domenach
    psychicznych/egzystencjalnych, wykrywanie szkodliwości monitoringu, anonimizacja rzadkich
    profili, niezależny nadzór nad eksperymentami produktu itd.) — potencjalne materiały do
    przyszłych ADR-ów lub do sekcji "Limitations/uncertainty" wymaganej przez
    `CONTRIBUTING.md`.
- Skale kodowe zdefiniowane w tym dokumencie (XP, EC, BL, MQ, PF, DQ, SE, CA, PE, R±) są
  **odrębne** od skali ryzyka R0–R4 z Konstytucji (wg CLAUDE.md tego repo) — nie mylić SE0-SE4
  (zdarzenia bezpieczeństwa Warstwy 6) z R0-R4 (ryzyko konstytucyjne Warstwy 1); to dwie różne
  taksonomie na dwóch różnych warstwach, tak jak wskazuje CLAUDE.md dla innych par
  "dwóch odrębnych osi" w tym projekcie (np. AuthorityRole vs IdentityType).
