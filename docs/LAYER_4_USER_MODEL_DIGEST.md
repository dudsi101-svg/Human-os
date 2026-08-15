# Digest: HUMAN OS — WARSTWA 4 — MODEL UŻYTKOWNIKA I CYFROWY PROFIL ROZWOJOWY

**Status:** rozbiór strukturalny (nie parafraza) źródła dostarczonego przez founder-a 2026-08-15 —
`Human_OS_Warstwa_4_Model_Uzytkownika_i_Cyfrowy_Profil_v0_1.docx`. Patrz
`docs/FOUNDER_REVIEW_2026-08-15.md`, sekcja "Czwarta tura", po kontekst i listę
`ADR-USERMODEL-001..005` sformułowanych na podstawie tego rozbioru — w tym ważne zastrzeżenie
(`ADR-USERMODEL-005`), że ten dokument to NIE to samo źródło co `ADR-USER-002`. Oryginalny plik
DOCX pozostaje jedynym rozstrzygającym źródłem w razie wątpliwości (`02_Source_Truth_Protocol`).
Dokument był wcześniej odnotowany w Founder Review jako "potwierdzony, treść niedostępna" — jest
to jego pierwszy odczyt. Cały plik został przeczytany od początku do
końca (linie 1–2771) w pięciu blokach, plus przeszukanie pełnotekstowe (`grep`) dla wzorców
`ADR-`, zakazów, oraz terminów `Hub`, `Graf Wiedzy`/`Knowledge Graph`, `bliźniak`/`Digital Twin`,
`R0-R4`. Oryginalny plik DOCX pozostaje jedynym rozstrzygającym źródłem w razie wątpliwości.

Motto/zdanie otwierające dokument (linie 32–33): *"Model jest mapą osoby w określonym czasie i
kontekście. Nigdy nie jest jej ostateczną definicją."*

---

## 1. Metadane / nagłówek dokumentu (sekcja 0. Karta dokumentu i sposób stosowania)

Tabela nagłówkowa (linie 10–30):

| Pole | Wartość |
|---|---|
| Wersja | 0.1 – model bazowy |
| Status | Projekt do iteracji, testów użytkowników i audytu |
| Zakres | Tożsamość, cele, wartości, kontekst, historia, dane, hipotezy i personalizacja |
| Dokument nadrzędny | Warstwa 1 – Konstytucja i Wartości |
| Model odniesienia | Warstwa 2 – Model Człowieka |
| Źródło wiedzy | Warstwa 3 – Mapa Wiedzy i Sygnatura Informacji |
| Właściciel dokumentu | Zespół założycielski Human OS |
| Data | 2026-07-20 |

Podtytuł dokumentu (linia 7–8): *"Pełna dokumentacja koncepcyjna, danych, personalizacji i
kontroli użytkownika."*

**0.1 Cel dokumentu** (linie 42–48): definiuje sposób, w jaki Human OS tworzy, aktualizuje,
wykorzystuje i usuwa cyfrowy model konkretnej osoby. Model Użytkownika łączy deklaracje, cele,
wartości, kontekst, historię, pomiary, zachowania, wyniki eksperymentów i hipotezy systemu.
Zastrzeżenie wprost: *"Nie jest kartoteką ani portretem psychologicznym. Jest kontrolowanym przez
użytkownika, wersjonowanym modelem roboczym, którego jedynym uzasadnieniem jest poprawa jakości
decyzji i uczenia się siebie."*

**Zasada nadrzędna Warstwy 4** (ramka, linie 50–57): *"System może modelować tylko to, co jest
potrzebne do jasno określonego celu, w sposób zrozumiały, odwracalny i możliwy do
zakwestionowania przez użytkownika. Profil nie może stać się etykietą, wyrokiem ani ukrytym
narzędziem wpływu."*

**0.2 Zakres obowiązywania** (linie 60–76):
- Obejmuje: onboarding, profil, pamięć systemu, cele, pomiary, dzienniki, integracje, wnioski AI,
  N-of-1 i personalizację.
- Obowiązuje: projektantów produktu, twórców AI, architektów danych, analityków, ekspertów,
  moderatorów i partnerów integracyjnych.
- Nie obejmuje: pełnej ontologii człowieka, oceny źródeł wiedzy ani finalnego algorytmu decyzji —
  są to odpowiedzialności innych warstw.
- Nie zastępuje: diagnozy, relacji terapeutycznej, badania klinicznego, osobistej
  odpowiedzialności ani ludzkiego osądu.
- Podlega: autonomii, minimalizacji danych, proporcjonalności ryzyka, prawu do wyjaśnienia oraz
  prawu do usunięcia profilu.

**0.4 Odpowiedzialność Warstwy 4** (linie 132–147) — kontrakty jednokierunkowe:
- Dostarcza Warstwie 5: aktualny kontekst osoby, cele, ograniczenia, tolerancję ryzyka, historię
  odpowiedzi i poziom gotowości.
- Dostarcza Warstwie 6: bazę, mierniki, historię interwencji i osobiste kryteria przerwania
  eksperymentu.
- Dostarcza Warstwie 7: zanonimizowane i dozwolone rekordy wyników, bez ujawniania tożsamości i
  narracji poza zakresem zgody.
- Odbiera z Warstwy 3: pojęcia, zakresy, interakcje, status wiedzy i strukturę sygnatur potrzebną
  do interpretacji danych.
- Podlega Warstwie 1: w każdym przypadku konfliktu między użytecznością profilu a prawami
  użytkownika.

**0.5 Test nadrzędny** (linie 149–155) — zasada bramkująca użycie danych: *"Jeżeli nie można
jasno odpowiedzieć: »po co przechowujemy tę informację?«, »skąd pochodzi?«, »jak długo jest
aktualna?«, »kto ją widzi?«, »jak wpływa na decyzje?« i »jak użytkownik może ją poprawić lub
usunąć?«, informacja nie może zostać aktywnie użyta w Modelu Użytkownika."*

---

## 2. Nazwane decyzje architektoniczne w stylu ADR

**Brak.** Przeszukano cały dokument (`grep -n "ADR-"`) — zero wystąpień. Dokument nie zawiera
dedykowanej sekcji z listą ADR, podobnie jak Warstwa 6 (`LAYER_6_EXPERIMENT_ENGINE_DIGEST.md`,
sekcja 2). Warstwa 4 jest dokumentem specyfikacyjnym/projektowym (12 aksjomatów w sekcji 1,
kryteria akceptacji w sekcji 37, deklaracja w Załączniku M), ale nie formalizuje decyzji w
formacie ADR z numeracją. Jeśli "Reconstruction Audit"/nowe ADR-y (np. rozszerzenie
`ADR-USER-002` albo nowy `ADR-USER-00x`) mają odnosić się do tego dokumentu, trzeba je utworzyć od
zera — nie ma tu istniejących ADR-ów do zmapowania.

Najbliższe odpowiedniki "decyzji architektonicznych":
- 12 aksjomatów w sekcji 1 (linie 157–216),
- architektura wielorzędowa R0–R8 w sekcji 2 (linie 218–265),
- sekcja 30 "Graf Modelu Użytkownika i schemat danych" (relacje węzłów, linie 1849–1919),
- sekcja 37 "Kryteria akceptacji Warstwy 4" (lista twardych wymagań, linie 2244–2309).

---

## 3. Kluczowe encje / kontrakty danych

### 3.1 Aksjomaty Modelu Użytkownika (sekcja 1, linie 157–216)

12 aksjomatów obowiązujących każdy profil, algorytm personalizacji i wniosek o osobie (skrócone):

| # | Aksjomat | Treść |
|---|---|---|
| 1 | Osoba jest większa niż jej dane | rozbudowany profil to fragmentaryczna reprezentacja, nie definicja |
| 2 | Model jest hipotezą w czasie | każdy wniosek ma datę, kontekst, pochodzenie i poziom pewności |
| 3 | Użytkownik zachowuje prawo do znaczenia | system nie może odebrać prawa do interpretowania własnego doświadczenia |
| 4 | Dane nie są neutralne | sposób pomiaru, pytania, urządzenie i kontekst wpływają na wynik |
| 5 | Personalizacja wymaga celu | nie modeluje się cech tylko dlatego, że technicznie można je przewidywać |
| 6 | Najpierw baza własna, potem norma populacyjna | zmiana wobec własnego punktu odniesienia bywa ważniejsza niż porównanie do przeciętnej |
| 7 | Brak danych nie oznacza braku zjawiska | system oznacza luki zamiast wypełniać je pozorną pewnością |
| 8 | Sprzeczność jest informacją | rozbieżne deklaracje/pomiary/zachowania przechowywane z kontekstem, nie uśredniane |
| 9 | Profil musi umieć zapominać | nieaktualne etykiety i wnioski nie mogą bez końca wpływać na przyszłe rekomendacje |
| 10 | Użytkownik może odmówić personalizacji | podstawowe funkcje działają także przy ograniczonym profilu |
| 11 | Ryzyko profilowania rośnie z wrażliwością danych | im bardziej intymna informacja, tym silniejsze wymagania zgody, bezpieczeństwa i uzasadnienia |
| 12 | System nie przewiduje wartości człowieka | brak rankingu moralnego, potencjału życiowego, "jakości osoby" |

### 3.2 Architektura wielorzędowa R0–R8 (sekcja 2, linie 218–265)

| Rząd | Zawartość | Funkcja |
|---|---|---|
| R0 – Tożsamość i kontrola | konto, zgody, uprawnienia, preferencje prywatności | określa właściciela i granice użycia |
| R1 – Kierunek | wartości, role, cele, priorytety, definicje sukcesu | wyjaśnia po co system działa |
| R2 – Kontekst | środowisko, zasoby, ograniczenia, etap życia, rytm dnia | określa warunki realnego działania |
| R3 – Dane źródłowe | deklaracje, pomiary, dziennik, urządzenia, dokumenty | rejestruje obserwacje bez ukrytej interpretacji |
| R4 – Cechy pochodne | trendy, zmienność, regularność, anomalie, korelacje | porządkuje sygnały w czasie |
| R5 – Hipotezy osobiste | wzorce, czynniki wspierające i ograniczające, gotowość | buduje ostrożne rozumienie osoby |
| R6 – Stan operacyjny | aktualne obciążenie, ryzyko, dostępność, priorytet | przekazuje kontekst Silnikowi Decyzji |
| R7 – Historia decyzji | rekomendacje, wybory, wykonanie, wyniki, refleksje | umożliwia uczenie się z poprzednich działań |
| R8 – Profil prezentacyjny | zrozumiała mapa postępu, wzorców i otwartych pytań | wspiera samoświadomość bez etykietowania |

**Uwaga terminologiczna dot. skali "R":** ta skala **R0–R8** NIE jest tożsama ze skalą R0–R4
Konstytucji (skala ryzyka wg CLAUDE.md tego repozytorium) — to zupełnie inna oś: "R" tu oznacza
"rząd/warstwę architektury modelu", nie poziom ryzyka. Nazewnictwo koliduje literowo z R0-R4, ale
nie ma z nim żadnego związku semantycznego — dokument nie wspomina R0-R4 Konstytucji ani razu
(potwierdzone grep-em).

**Zakaz skrótu epistemicznego** (ramka, linie 267–275): *"System NIE MOŻE zapisać interpretacji
jako danych źródłowych. Przykład: »użytkownik jest mało zdyscyplinowany« nie jest obserwacją.
Obserwacją może być: »w 3 z 10 zaplanowanych dni wykonano zadanie«. Interpretacja wymaga osobnej
hipotezy i kontekstu."*

Główna pętla aktualizacji (2.1, linie 277–299): CEL I WARTOŚCI → KONTEKST + BAZA WŁASNA + AKTUALNY
STAN → OBSERWACJA/POMIAR/DECYZJA → CECHA POCHODNA + HIPOTEZA Z POZIOMEM PEWNOŚCI →
REKOMENDACJA/EKSPERYMENT/REFLEKSJA → WYNIK + KOREKTA MODELU + WYGASZENIE NIEAKTUALNYCH WNIOSKÓW.

### 3.3 Ontologia obiektów profilu (sekcja 3, linie 301–397) — 24 obiekty

| Obiekt | Znaczenie |
|---|---|
| User | techniczny właściciel profilu; nie jest synonimem całej osoby |
| IdentityContext | jawnie podane informacje identyfikacyjne i preferowane formy zwracania się |
| Consent | zakres, cel, data, wersja i możliwość wycofania zgody |
| Value | wartość użytkownika wraz z opisem znaczenia i przykładem zachowania |
| Role | rola życiowa, np. rodzic, przedsiębiorca, sportowiec, opiekun |
| Goal | cel, kierunek, kryterium sukcesu, horyzont, priorytet i status |
| Constraint | ograniczenie zdrowotne, czasowe, finansowe, środowiskowe lub społeczne |
| Resource | zasób wspierający realizację celu |
| Preference | preferowany sposób, tempo, język, format lub intensywność działania |
| RiskPreference | deklarowana i obserwowana tolerancja ryzyka dla określonej domeny |
| Observation | jednostkowa obserwacja z czasem, źródłem i kontekstem |
| Measurement | wartość zmierzona wraz z jednostką, metodą i jakością |
| JournalEntry | narracja użytkownika przechowywana oddzielnie od wniosków systemu |
| DerivedFeature | obliczona cecha posiadająca wersję algorytmu |
| Hypothesis | wniosek o osobie z podstawą, pewnością i alternatywami |
| State | czasowo ograniczony stan operacyjny |
| Pattern | powtarzalna relacja występująca w określonych warunkach |
| InterventionExposure | rzeczywiste narażenie na działanie, nie tylko deklaracja planu |
| Outcome | wynik obiektywny, subiektywny lub behawioralny |
| Decision | wybór użytkownika wraz z przedstawionymi opcjami i uzasadnieniem |
| ModelSnapshot | zamrożony obraz profilu użyty do konkretnej decyzji |
| Correction | zmiana zgłoszona przez użytkownika albo audytora |
| AuditEvent | ślad dostępu, zmiany, eksportu lub usunięcia danych |

Relacje (3.1, linie 381–397): Cel wspierany przez wartości/role/zasoby/mniejsze cele, ograniczany
przez konflikty/koszt/kontekst. Obserwacja opisuje stan/zachowanie/wynik/ekspozycję/zdarzenie —
"nigdy sama nie staje się automatycznie cechą osoby". Hipoteza opiera się na obserwacjach,
pomiarach, historii decyzji i wiedzy z Warstwy 3. Rekomendacja korzysta z ModelSnapshot, aby móc
odtworzyć, dlaczego została wygenerowana.

### 3.4 Inne kluczowe struktury pól (skrót)

- **Warstwy tożsamości** (4.1, tabela): Techniczna / Relacyjna / Kontekstowa / Wrażliwa /
  Symboliczna — każda z osobnym zakresem dostępu.
- **Hierarchia celów** (6.1, tabela): Sens/kierunek → Domena → Rezultat → Proces → Eksperyment →
  Działanie dzienne.
- **Minimalna karta celu** (6.2): Nazwa, Znaczenie, Horyzont, Kryteria sukcesu, Koszt akceptowalny,
  Konflikty, Stopień własności, Status.
- **Wartości operacyjne** (7.1, tabela pól): Nazwa, Znaczenie, Przejaw, Granica, Konflikt,
  Aktualność.
- **Kategorie kontekstu** (8.1, 10 kategorii): Czas, Środowisko, Finanse, Praca, Relacje, Zdrowie,
  Dostęp, Kultura, Etap życia, Kryzys/zmiana.
- **Warstwy osi czasu** (9.1, tabela): Zdarzenia życiowe, Historia zdrowotna, Interwencje, Cele,
  Pomiary, Decyzje, Hipotezy, Okresy ciszy — każda z własną polityką retencji.
- **Rodzaje bazy własnej** (10.1, 7 typów): Deklaratywna, Pomiarowa, Kontekstowa, Funkcjonalna,
  Subiektywna, Sezonowa, Celowa.
- **Minimalny ślad pochodzenia** (11.1): Kto lub co / Kiedy / Jak / Po co / Jakość / Wersja.
- **Ocena jakości rekordu** (12.2, skala 0-4 dla 7 wymiarów): Kompletność, Wiarygodność źródła,
  Powtarzalność, Kontekst, Aktualność, Zgodność, Użyteczność.
- **Struktura hipotezy osobistej** (14.1): Treść, Podstawa, Kontekst, Pewność, Alternatywy,
  Kontrdowody, Test, Data wygaśnięcia, Status użytkownika.
- **Pakiet kontekstowy decyzji dla Warstwy 5** (23.1): Aktywny cel, Wartości i konflikty, Aktualny
  stan, Kontekst, Historia odpowiedzi, Tolerancja ryzyka, Preferencje interakcji, Luki danych,
  Zakazy i przeciwwskazania, Stan zgody.
- **Minimalny rekord hipotezy — przykład logiczny** (30.3, linie 1897–1919): pełny przykładowy
  obiekt `hypothesis_id: H-2026-00421` z polami `claim`, `context`, `evidence_for`,
  `evidence_against`, `alternatives`, `confidence: H3`, `user_status`, `last_confirmed`,
  `review_due`, `allowed_use`.
- **Graf** (30.1, linie 1853–1873) — 11 relacji węzeł→relacja→węzeł w notacji strzałkowej, np.
  `USER ──owns──> CONSENT / PRIVACY SETTINGS`, `HYPOTHESIS ──applies_in──> CONTEXT
  ──expires_at──> REVIEW`, `CORRECTION ──changes──> DATA / HYPOTHESIS ──logged_as──> AUDIT EVENT`.
- **Załączniki A–M** (formularze/karty pól, pełna treść w sekcji 8 poniżej — Karta profilu, Karta
  celu, Karta wartości i roli, Karta obserwacji i pomiaru, Karta hipotezy osobistej, Karta decyzji
  i snapshotu, Macierz retencji, Onboarding adaptacyjny (10 kroków), Przykład ścieżki aktualizacji,
  Słownik statusów i kodów, Lista kontrolna audytu funkcji, Otwarte pytania do wersji 0.2,
  Deklaracja Modelu Użytkownika).

---

## 4. Bramy ryzyka/bezpieczeństwa i reguły eskalacji

**Uwaga terminologiczna**: dokument NIE używa skali "R0–R4" Konstytucji/Warstwy 1 — potwierdzone
grep-em, zero wystąpień. Zamiast tego Warstwa 4 definiuje pięć **własnych, odrębnych** skal
kodowanych literowo (żadna nie pokrywa się z R0-R4 ani z kodami Warstwy 6 — XP/SE/EC/BL/MQ/PF/DQ/CA/PE):

| Skala | Zakres | Znaczenie | Sekcja |
|---|---|---|---|
| H0–H5 | 6 poziomów | gotowość hipotezy osobistej do użycia w personalizacji | 14.1, Zał. J |
| P0–P5 | 6 poziomów | siła dowodu osobistego / N-of-1 | 21.1, Zał. J |
| C0–C5 | 6 poziomów | zakres zgody warstwowej na przetwarzanie i użycie | 5.1, Zał. J |
| D0–D4 | 5 poziomów | klasa wrażliwości danych | 27.1, Zał. D, Zał. J |
| (0-4) | skala liczbowa | 7-wymiarowa ocena jakości rekordu (Kompletność, Wiarygodność...) | 12.2 |

### 4.1 H0–H5 — Poziomy pewności hipotezy osobistej (14.1, linie 1029–1052)

| Poziom | Opis | Dozwolone użycie |
|---|---|---|
| H0 – brak | brak podstaw lub czysta spekulacja | pytanie eksploracyjne, nie rekomendacja |
| H1 – sygnał | pojedyncza obserwacja lub słaba wskazówka | delikatna sugestia obserwacji |
| H2 – hipoteza | kilka zgodnych danych, nadal liczne alternatywy | prosty, niskoryzykowny test |
| H3 – wzorzec roboczy | powtarzalny efekt w podobnym kontekście | personalizacja niskiego i średniego ryzyka |
| H4 – wzorzec potwierdzony | wiele źródeł, powtórzenia, stabilność | silniejsza personalizacja z wyjaśnieniem |
| H5 – ograniczona reguła osobista | wielokrotne testy, znane granice obowiązywania | domyślna reguła, nadal możliwa do wyłączenia |

Zastrzeżenie (ramka, linie 1054–1061): *"Pewność nie jest prawdopodobieństwem prawdy — wartość
H0-H5 opisuje gotowość do użycia hipotezy w personalizacji, nie matematyczne prawdopodobieństwo,
że zdanie jest absolutnie prawdziwe."*

### 4.2 P0–P5 — Stopnie dowodu osobistego / N-of-1 (21.1, linie 1368–1388)

P0 anegdota → P1 obserwacja powtarzalna → P2 test planowany (baza+protokół+mierniki) → P3
replikacja → P4 test naprzemienny (A/B lub wycofanie i powrót) → P5 stabilna reguła osobista
(wiele testów i znane granice) → domyślna personalizacja.

### 4.3 C0–C5 — Zgoda warstwowa (5.1, linie 453–475)

| Poziom | Zakres | Wymaganie |
|---|---|---|
| C0 – podstawowy | konto, ustawienia, ręcznie zapisane cele | niezbędne do działania |
| C1 – personalizacja | historia użycia, preferencje, wnioski AI | osobna, możliwa do wyłączenia |
| C2 – dane urządzeń | sen, aktywność, tętno, lokalne trendy | zgoda per integracja i kategoria |
| C3 – dane wrażliwe | zdrowie, psychika, biometria, seksualność | wyraźna zgoda celowa i okresowa |
| C4 – wkład społeczności | anonimowe wyniki eksperymentów | oddzielna zgoda na każdy typ wkładu |
| C5 – badania | użycie w zatwierdzonym projekcie badawczym | osobny formularz i możliwość wycofania |

### 4.4 D0–D4 — Klasy wrażliwości danych (27.1, linie 1691–1712)

| Klasa | Przykład | Kontrola |
|---|---|---|
| D0 – publiczne/neutralne | język aplikacji, motyw wyświetlania | standardowe zabezpieczenia |
| D1 – osobiste | cele, preferencje, harmonogram | szyfrowanie i kontrola dostępu |
| D2 – wrażliwe | zdrowie, relacje, finanse, lokalizacja | odrębne zgody i ograniczona retencja |
| D3 – wysoce wrażliwe | biometria, trauma, seksualność, dane genetyczne | sejf danych, ścisły dostęp, audyt |
| D4 – krytyczne | dane mogące spowodować poważną szkodę przy ujawnieniu | minimalizacja, lokalne przetwarzanie lub brak przechowywania |

### 4.5 Kategorie sygnałów bezpieczeństwa i eskalacja (sekcja 26, linie 1637–1686)

6 kategorii sygnałów: Techniczny, Funkcjonalny, Działanie niepożądane, Psychiczny kryzys, Konflikt
danych, Naruszenie prywatności — każda z ograniczeniem systemu (np. dla "Psychiczny kryzys":
*"priorytet bezpieczeństwa i pomoc kryzysowa"*). Minimalne zasady (26.2): Nie diagnozuj, Nie
bagatelizuj, Nie panikuj, Pokaż następny krok, Zachowaj ślad, Chroń prywatność (*"nie powiadamiaj
osoby trzeciej bez podstawy prawnej lub uprzedniej zgody, poza ściśle określonymi wyjątkami"*).

### 4.6 Statusy obiektów (Zał. J, linie 2638–2673)

ACTIVE / PENDING / CONTESTED / SUSPENDED / EXPIRED / WITHDRAWN / ARCHIVED / DELETED — 8 statusów
opisujące cykl życia dowolnego obiektu profilu (hipotezy, danych, rekomendacji).

### 4.7 Tryby awarii systemowej (sekcja 34, linie 2066–2116)

13 "trybów awarii" z mechanizmem szkody i kontrolą, m.in.: Nadmierne profilowanie, Fałszywa
precyzja, Etykietowanie, Samospełniająca przepowiednia, Uzależnienie od pomiaru, Optymalizacja
wskaźnika kosztem życia, Halucynacja AI, Przejęcie komercyjne, Bias populacyjny, Ukryta presja.
*"Wysoka skuteczność rekomendacji nie kompensuje naruszenia autonomii, prywatności lub
bezpieczeństwa"* (34.1, linie 2121–2123).

---

## 5. Kluczowe definicje terminologiczne (0.3 Podstawowe terminy, linie 78–130)

| Termin | Znaczenie |
|---|---|
| Model Użytkownika | Wersjonowany zbiór danych, relacji, hipotez i stanów dotyczących konkretnej osoby. |
| Dane źródłowe | Informacje wprowadzone przez użytkownika, urządzenie, integrację, specjalistę lub system. |
| Cecha pochodna | Wartość obliczona z danych źródłowych, np. trend, regularność, odchylenie od własnej bazy. |
| Hipoteza osobista | Wniosek o użytkowniku wymagający określenia pewności, podstawy i możliwości korekty. |
| Stan | Krótkotrwała konfiguracja, np. zmęczenie, gotowość, nastrój lub obciążenie. |
| Wzorzec | Powtarzalna relacja obserwowana w czasie i w określonym kontekście. |
| Cecha względnie trwała | Właściwość bardziej stabilna niż stan, ale nadal podatna na zmianę i kontekst. |
| Cel | Pożądany kierunek lub rezultat z właścicielem, horyzontem i kryterium sukcesu. |
| Wartość | Zasada, którą użytkownik uznaje za ważną przy wyborze kierunku działania. |
| Dowód osobisty | Ustrukturyzowany wynik dotyczący konkretnego użytkownika, niekoniecznie uogólnialny na innych. |
| Wygaszenie | Zmniejszenie wagi informacji wraz z czasem, zmianą kontekstu albo brakiem potwierdzeń. |
| Cyfrowy profil rozwojowy | Warstwa prezentacyjna Modelu Użytkownika używana przez osobę do autorefleksji i planowania. |

Dodatkowy słownik statusów i kodów w Załączniku J (zob. sekcja 4.6 wyżej): H0-H5, P0-P5, C0-C5,
D0-D4, ACTIVE, PENDING, CONTESTED, SUSPENDED, EXPIRED, WITHDRAWN, ARCHIVED, DELETED.

**Uwaga**: termin "Cyfrowy profil rozwojowy" (definiowany tu jako *warstwa prezentacyjna*, R8 w
architekturze wielorzędowej) jest bliski, ale **nie identyczny** z "Cyfrowy bliźniak"/"Digital
Twin" z `ADR-USER-002` — patrz sekcja 9 poniżej.

---

## 6. Relacje/punkty integracji z innymi warstwami/komponentami

Dokument odwołuje się wyłącznie do innych **Warstw Human OS** ponazywanych numerycznie — **nie
znaleziono ani jednego wystąpienia** słów "Hub", "Graf Wiedzy"/"Knowledge Graph" ani
"bliźniak"/"Digital Twin" w całym pliku (potwierdzone grep-em, zero trafień dla wszystkich
czterech wzorców). To istotna rozbieżność względem nazewnictwa repozytorium kodu
(`hos_engine/knowledge_graph.py`, `hub/`) i względem `ADR-USER-002`.

### 6.1 Nagłówek — relacje nadrzędne (linie 20–24)
- Dokument nadrzędny: **Warstwa 1 – Konstytucja i Wartości**.
- Model odniesienia: **Warstwa 2 – Model Człowieka**.
- Źródło wiedzy: **Warstwa 3 – Mapa Wiedzy i Sygnatura Informacji**.

### 6.2 Sekcja 0.4 — kontrakty jednokierunkowe (linie 132–147, cytowane dosłownie w sekcji 1
   powyżej): Warstwa 4 dostarcza Warstwie 5 (Silnik Decyzji, nazwa wywnioskowana z kontekstu, nie
   ma numerowanego nagłówka "Warstwa 5" wprost tutaj poza tabelą 32), Warstwie 6 (Silnik
   Eksperymentów) i Warstwie 7 (Inteligencja Zbiorowa); odbiera z Warstwy 3; podlega Warstwie 1.

### 6.3 Sekcja 32 — "Interfejsy z pozostałymi warstwami" (linie 1961–1993), tabela pełna:

| Warstwa | Model Użytkownika odbiera | Model Użytkownika dostarcza |
|---|---|---|
| 1 – Konstytucja | prawa, zakazy, hierarchię wartości systemu | dowody zgodności i naruszeń |
| 2 – Model Człowieka | domeny, procesy, pojęcia i granice modelowania | konkretną instancję i dane osobiste |
| 3 – Mapa Wiedzy | twierdzenia, sygnatury, zakresy, ryzyko | wyniki osobiste i pytania wymagające wiedzy |
| 5 – Silnik Decyzji | żądanie kontekstu i rezultat rekomendacji | snapshot, cele, ograniczenia, historię odpowiedzi |
| 6 – Silnik Eksperymentów | protokół, mierniki, kryteria przerwania | bazę, ekspozycję, wynik i refleksję |
| 7 – Inteligencja Zbiorowa | wzorce populacyjne z ograniczeniami | wyłącznie dozwolone, zanonimizowane raporty |
| Interfejs użytkownika | korekty, cele, deklaracje i wybory | profil, wyjaśnienia, postęp i kontrolę |

To jest jedyne miejsce, gdzie dokument nazywa "Warstwę 5" (jako "Silnik Decyzji"), "Warstwę 6"
(jako "Silnik Eksperymentów") i "Warstwę 7" (jako "Inteligencja Zbiorowa") — spójne z nagłówkiem
Warstwy 6 (`docs/LAYER_6_EXPERIMENT_ENGINE_DIGEST.md`, wiersz "Decyzja wejściowa | Warstwa 5 –
Silnik Decyzji i Rekomendacji" oraz "Kontekst osobisty | Warstwa 4 – Model Użytkownika i Cyfrowy
Profil" — nazewnictwo wzajemnie spójne między obydwoma dokumentami).

**Kontrakt jakości** (32.1, linie 1995–2009): każde wejście musi mieć źródło/czas/zgodę/jakość/
znaczenie; każde wyjście musi wskazywać zakres/aktualność/pewność/ograniczenia; każda decyzja musi
odwoływać się do snapshotu, nie do zmiennego profilu "na żywo"; każdy wynik społeczności musi być
odłączony od danych identyfikacyjnych i narracji prywatnej.

---

## 7. Explicit prohibitions (dosłowne cytaty z numerami linii)

Wybór najistotniejszych zakazów/ograniczeń, ze szczególnym naciskiem na kwestionowalność, prawo do
usunięcia, zakres zgody i determinizm profilu (jak wymagane przez zadanie):

- **Linia 55–56** (ramka "Zasada nadrzędna Warstwy 4"): *"Profil nie może stać się etykietą,
  wyrokiem ani ukrytym narzędziem wpływu."*
- **Linie 153–155** (0.5, Test nadrzędny): *"...informacja nie może zostać aktywnie użyta w
  Modelu Użytkownika"* — jeśli nie można odpowiedzieć na sześć pytań kontrolnych (po co, skąd,
  jak długo, kto widzi, jak wpływa, jak poprawić/usunąć).
- **Linie 172–174** (Aksjomat 3): *"System może wskazać rozbieżność, ale nie może odebrać osobie
  prawa do interpretowania własnego doświadczenia."*
- **Linie 268–273** (ramka "Zakaz skrótu epistemicznego"): *"System NIE MOŻE zapisać
  interpretacji jako danych źródłowych. Przykład: »użytkownik jest mało zdyscyplinowany« nie jest
  obserwacją."*
- **Linie 436–437** (4.2, "Zakaz mieszania"): *"dane dwóch osób nie mogą zostać automatycznie
  połączone na podstawie jednego urządzenia."*
- **Linie 445–446**: *"Tryb gościa: nie może zasilać długoterminowego profilu bez świadomego
  przypisania."*
- **Linie 503–508** (ramka "Zakaz zgody pozornej"): *"Brak akceptacji danych wrażliwych nie może
  skutkować karą, manipulacyjnym interfejsem ani fałszywym komunikatem, że system »nie może
  pomóc«. Powinien jasno pokazać, które funkcje będą mniej precyzyjne i dlaczego."*
- **Linie 566–568** (6.3): *"Nie powinien jednak arbitralnie uznawać celu za nieautentyczny.
  Ostateczna kwalifikacja należy do użytkownika."*
- **Linie 945–950** (ramka "Zakaz presji pomiarowej"): *"Model nie może wymuszać coraz większej
  liczby pomiarów tylko po to, aby zwiększyć kompletność danych. Jeżeli monitorowanie obniża
  dobrostan, wzmacnia kompulsję lub odciąga od życia, system powinien ograniczyć częstotliwość i
  przejść na pomiary minimalne."*
- **Linie 1157–1159** (16.1): *"Wniosek z zachowania nie może automatycznie nadpisać deklaracji.
  [...] Nie może optymalizować zaangażowania kosztem celu użytkownika."*
- **Linie 1200–1201** (17.2): *"Nie może obniżać wartości osoby: system nie tworzy punktów
  posłuszeństwa ani etykiety »dobry użytkownik«."*
- **Linie 1209–1214** (ramka "Zakaz ciemnych wzorców"): *"Streaki, alarmy utraty postępu, społeczny
  wstyd, sztuczne poczucie pilności i nagrody uzależniające nie mogą być używane do wymuszania
  zachowań. Zaangażowanie jest środkiem, nie celem produktu."*
- **Linie 1256–1259** (18.2, Granice autonomii): *"Deklarowana determinacja nie zmienia
  niebezpiecznej interwencji w akceptowalną rekomendację. [...] nie obniża progów konstytucyjnych
  ani zasad odmowy Warstwy 1."*
- **Linie 1567–1570** (ramka "Prawo do sprzeciwu wobec modelu"): *"System może zachować techniczny
  ślad, że hipoteza została odrzucona, ale nie może po cichu nadal używać jej do personalizacji,
  segmentacji ani treningu, jeśli użytkownik wycofał zgodę."*
- **Linie 1627–1634** (ramka "Zapora interpretacyjna"): *"Wynik Human Design, astrologii,
  enneagramu lub innego systemu symbolicznego nie może samodzielnie zwiększać pewności hipotezy
  biologicznej, psychologicznej ani medycznej. Może jedynie zainicjować pytanie lub dobrowolny
  eksperyment niskiego ryzyka."*
- **Linie 1684–1685** (26.2): *"Chroń prywatność: nie powiadamiaj osoby trzeciej bez podstawy
  prawnej lub uprzedniej zgody, poza ściśle określonymi wyjątkami."*
- **Linie 1739–1745** (27.3, "Zakaz wtórnego wykorzystania"): *"Dane zebrane dla wsparcia
  użytkownika nie mogą zostać wykorzystane do reklamy, oceny zdolności kredytowej, ubezpieczenia,
  zatrudnienia, dynamicznego ustalania cen ani manipulowania podatnością bez odrębnej,
  dobrowolnej i rzeczywiście odwoływalnej zgody. Niektóre zastosowania powinny pozostać
  bezwzględnie zakazane niezależnie od zgody."*
- **Linie 1831–1847** (29.2, "Zakazane wnioski") — pełna lista: Wartość człowieka (ranking
  moralny/"jakość"/przydatność społeczna), Nieodwracalny potencjał, Diagnoza ukryta, Ocena
  zatrudnialności/kredytu/ubezpieczenia na podstawie danych rozwojowych/zdrowotnych,
  Manipulowalność (profil podatności do sprzedaży/retencji), Przynależność wrażliwa (wnioskowanie
  przekonań/orientacji/zdrowia bez zgody i konieczności).
- **Linie 2036–2057** (33.2, "Zakazane funkcje" AI) — pełna lista: Ukryte wnioskowanie,
  Etykietowanie osobowości, Manipulacja, Nadpisanie użytkownika (*"traktowanie wniosku AI jako
  ważniejszego od jawnej korekty osoby"*), Diagnostyka pozorna, Samodzielna zmiana zgody
  (*"rozszerzanie zakresu danych przez domniemanie"*), Niewidzialne uczenie (*"wykorzystanie danych
  profilu do trenowania modeli bez wyraźnej podstawy i informacji"*).

**Prawa użytkownika wobec profilu** (5.2, linie 477–500) — bezpośrednio odpowiadające na pytanie
zadania o kwestionowalność/usuwanie/zgodę: Prawo wglądu, Prawo korekty (*"możliwość poprawienia
faktu, zakwestionowania interpretacji i dodania własnego komentarza"*), Prawo wyłączenia, Prawo
eksportu, **Prawo usunięcia** (*"usunięcie profilu i kopii po wymaganym okresie technicznym, z
jawnym opisem wyjątków prawnych"*), **Prawo do zapomnienia w modelu** (*"wyłączenie nieaktualnych
cech i hipotez z przyszłych decyzji"*), Prawo do ciszy, Prawo do profilu minimalnego.

**Determinizm profilu** — dodatkowo wart odnotowania jest cały zestaw mechanizmów
antydeterministycznych rozsianych po dokumencie: sekcja 13 (stany/cechy/wzorce/kontekst/narracja
z regułą "nie uogólniać"), sekcja 15 (sprzeczności przechowywane, nie uśredniane), sekcja 22
(wygaszanie wag i "epoki profilu"), sekcja 29 ("Bias, sprawiedliwość i ochrona przed
determinizmem").

---

## 8. Spis treści / struktura sekcji (numery i tytuły)

0. Karta dokumentu i sposób stosowania (0.1–0.5)
1. Aksjomaty Modelu Użytkownika
2. Architektura wielorzędowa Modelu Użytkownika (2.1 Główna pętla aktualizacji)
3. Ontologia obiektów profilu (3.1 Relacje między obiektami)
4. Tożsamość, konto i granice profilu (4.1 Minimalna tożsamość techniczna, 4.2 Profile
   wieloosobowe i współdzielone urządzenia)
5. Zgoda, własność i kontrola użytkownika (5.1 Zgoda warstwowa, 5.2 Prawa użytkownika wobec
   profilu)
6. Cele, kierunek i definicja sukcesu (6.1 Hierarchia celów, 6.2 Minimalna karta celu, 6.3
   Wykrywanie celów pozornych)
7. Wartości, role i tożsamość narracyjna (7.1 Wartości operacyjne, 7.2 Role życiowe, 7.3 Narracja
   o sobie)
8. Kontekst życia, zasoby i ograniczenia (8.1 Kategorie kontekstu, 8.2 Zasoby, 8.3 Reguła
   wykonalności)
9. Historia i oś czasu użytkownika (9.1 Warstwy osi czasu, 9.2 Pamięć kontekstowa, 9.3 Zdarzenia
   przełomowe)
10. Baza własna i stan początkowy (10.1 Rodzaje bazy, 10.2 Okres kalibracji, 10.3 Zmiana bazy)
11. Źródła danych i pochodzenie informacji (11.1 Minimalny ślad pochodzenia)
12. Pomiary, obserwacje i jakość danych (12.1 Typy pomiarów, 12.2 Ocena jakości rekordu, 12.3
    Braki danych)
13. Stany, cechy, wzorce i kontekst (13.1 Kryteria wzorca)
14. Hipotezy osobiste i poziomy pewności (14.1 Struktura hipotezy)
15. Sprzeczności, niejednoznaczność i korekta (15.1 Rodzaje sprzeczności, 15.2 Procedura
    rozstrzygania)
16. Preferencje, styl interakcji i dostępność (16.1 Uczenie preferencji)
17. Gotowość, zaangażowanie i zdolność do działania (17.1 Wymiary gotowości, 17.2 Niewykonanie
    jako dane)
18. Tolerancja ryzyka i styl podejmowania decyzji (18.1 Ryzyko jest domenowe, 18.2 Granice
    autonomii)
19. Interwencje, ekspozycje i rzeczywiste wykonanie (19.1 Cykl interwencji, 19.2
    Wielointerwencyjność)
20. Wyniki, postęp i znaczenie zmiany (20.1 Minimalna istotna zmiana osobista, 20.2 Brak postępu)
21. Dowody osobiste i eksperymenty N-of-1 (21.1 Stopnie dowodu osobistego, 21.2 Ochrona przed
    efektem potwierdzenia)
22. Model czasu, wygaszanie i epoki profilu (22.1 Daty każdego obiektu, 22.2 Wygaszanie wag, 22.3
    Epoki profilu)
23. Personalizacja i kontrakt z Silnikiem Decyzji (23.1 Pakiet kontekstowy decyzji, 23.2 Czego
    Model nie rozstrzyga)
24. Wyjaśnialność, podgląd i korekta modelu (24.1 Widok "Dlaczego system tak uważa", 24.2 Tryby
    korekty)
25. Human Design, astrologia i systemy interpretacyjne (25.1 Status w Modelu Użytkownika, 25.2
    Sygnatura osobista systemu symbolicznego)
26. Stan bezpieczeństwa i eskalacja (26.1 Kategorie sygnałów, 26.2 Minimalne zasady)
27. Prywatność, bezpieczeństwo i minimalizacja danych (27.1 Klasy wrażliwości, 27.2 Zasady
    techniczne i organizacyjne, 27.3 Zakaz wtórnego wykorzystania)
28. Dostęp specjalistów, opiekunów i osób wspierających (28.1 Udostępnianie selektywne)
29. Bias, sprawiedliwość i ochrona przed determinizmem (29.1 Źródła uprzedzeń, 29.2 Zakazane
    wnioski)
30. Graf Modelu Użytkownika i schemat danych (30.1 Węzły główne, 30.2 Wymagane cechy techniczne,
    30.3 Minimalny rekord hipotezy — przykład logiczny)
31. Wersjonowanie, migracje i ślad audytowy (31.1 Co podlega wersjonowaniu, 31.2 Snapshot decyzji,
    31.3 Audyt użytkownika)
32. Interfejsy z pozostałymi warstwami (32.1 Kontrakt jakości)
33. Rola AI w budowie Modelu Użytkownika (33.1 Dozwolone funkcje, 33.2 Zakazane funkcje, 33.3
    Human-in-the-loop)
34. Ryzyka systemowe i tryby awarii (34.1 Rejestr ryzyk)
35. Zarządzanie, role i odpowiedzialność (35.1 Zmiany wysokiego wpływu)
36. Metryki jakości Modelu Użytkownika (36.1 Metryki antycelowe)
37. Kryteria akceptacji Warstwy 4

Załączniki:
- A. Karta profilu użytkownika
- B. Karta celu
- C. Karta wartości i roli
- D. Karta obserwacji i pomiaru
- E. Karta hipotezy osobistej
- F. Karta decyzji i snapshotu
- G. Macierz retencji i wygaszania
- H. Onboarding adaptacyjny (10 kroków)
- I. Przykład ścieżki aktualizacji (10-krokowy przykład narracyjny: poprawa energii rano)
- J. Słownik statusów i kodów
- K. Lista kontrolna audytu funkcji (checklist, 14 pytań)
- L. Otwarte pytania do wersji 0.2 (12 tematów)
- M. Deklaracja Modelu Użytkownika

Dokument kończy się (linie 2768–2771) zdaniem: *"Warstwa 4 staje się operacyjnym mostem między
uniwersalnym Modelem Człowieka a konkretną, zmieniającą się osobą. Jej dojrzałość mierzy się nie
liczbą danych ani trafnością etykiet, lecz zdolnością do wspierania rozwoju bez redukowania
człowieka do profilu."*

---

## 9. Porównanie z ADR-USER-002 ("Human Digital Twin") — czy to to samo źródło?

**Wniosek: to NIE jest to samo źródło, i dokument nie potwierdza koncepcji "Cyfrowy bliźniak"
dosłownie — jest to odrębny, komplementarny dokument o pokrywającym się, ale innym zakresie.**

`ADR-USER-002` jawnie deklaruje swoje źródło jako
`Human_OS_Rozszerzenie_Architektury_i_Integracja_v0_2_1.docx` (*"Rozszerzenie Architektury i
Integracja v0.2"*, §6) — **inny plik niż `warstwa4.txt`** (który pochodzi z
`Human_OS_Warstwa_4_...` wg konwencji nazw sióstr-dokumentów widocznej w digestcie Warstwy 6).
Nie ma potrzeby zgadywać: dokument Warstwy 4 sam siebie zatytułowuje "MODEL UŻYTKOWNIKA I CYFROWY
PROFIL ROZWOJOWY" (linie 1–7), nie "Cyfrowy bliźniak"/"Digital Twin".

Konkretne rozbieżności terminologiczne i strukturalne:

1. **Termin "Cyfrowy bliźniak"/"Digital Twin" nie występuje w ogóle** w `warstwa4.txt` (grep:
   zero trafień dla "bliźniak" i "twin"). Warstwa 4 używa własnego terminu **"Cyfrowy profil
   rozwojowy"** — zdefiniowanego w słowniku (0.3, linia 127) jako *"Warstwa prezentacyjna Modelu
   Użytkownika używana przez osobę do autorefleksji i planowania"* — czyli węziej, jako jedna
   warstwa prezentacji (R8 w architekturze R0-R8), a nie synonim całego modelu.

2. **Inna dekompozycja komponentów.** ADR-USER-002 wymienia dziewięć nazwanych "components":
   Identity & Roles, Goals & Values, State Model, Behavior Model, Capability Model, Decision
   Style, Project & Financial Context, Social Context, Reflective/Symbolic Layer. Warstwa 4 nie
   ma listy o tej samej nazwie ani strukturze — zamiast tego ma (a) architekturę wielorzędową
   R0–R8 (sekcja 2) i (b) płaską ontologię 24 obiektów (sekcja 3: User, Value, Role, Goal,
   Constraint, Resource, Preference, RiskPreference, Observation, Measurement, JournalEntry,
   DerivedFeature, Hypothesis, State, Pattern, InterventionExposure, Outcome, Decision,
   ModelSnapshot, Correction, AuditEvent, IdentityContext, Consent). Częściowe pokrycie
   koncepcyjne istnieje, ale nazewnictwo i granulacja są inne:
   - Identity & Roles ≈ R0 Tożsamość i kontrola + obiekty `IdentityContext`/`Role` (sekcja 4, 7.2).
   - Goals & Values ≈ R1 Kierunek + obiekty `Goal`/`Value` (sekcje 6, 7.1).
   - State Model ≈ R6 Stan operacyjny + obiekt `State` + sekcja 17 "Gotowość" — ale wymiary są
     inne: ADR wymienia sleep/energy/load/mood/readiness/context; Warstwa 4 (17.1) wymienia
     Znaczenie celu/Energia/Czas/Kompetencja/Pewność siebie/Wsparcie/Ryzyko/Stabilność — nakładają
     się częściowo (energia, gotowość), ale nie identycznie.
   - Behavior Model ("explicitly without deterministic labels") ≈ obiekt `Pattern` + cała sekcja 13
     ("Stany, cechy, wzorce i kontekst") + "Zakaz skrótu epistemicznego" — silne pokrycie
     koncepcyjne, ale bez nazwy "Behavior Model".
   - Capability Model — **brak bezpośredniego odpowiednika** w Warstwie 4 jako nazwana jednostka;
     najbliżej: "Kompetencja" jako wymiar gotowości (17.1) i "Zasoby wewnętrzne" (8.2).
   - Decision Style — **brak nazwanego komponentu**; najbliżej: sekcja 18 "Tolerancja ryzyka i
     styl podejmowania decyzji" + obiekt `Decision`, ale skupiona głównie na ryzyku, nie na
     ogólnym stylu decyzyjnym.
   - Project & Financial Context — Warstwa 4 ma "Finanse" jako jedną z 10 kategorii kontekstu
     (8.1), ale brak wydzielonego "Project Context".
   - Social Context ("only to the extent of consent") ≈ kategoria "Relacje" (8.1) + źródło "Osoba
     bliska" (11) + sekcja 28 (dostęp osób wspierających) — pokrycie częściowe, brak nazwanego
     komponentu "Social Context".
   - **Reflective/Symbolic Layer — silne, niemal dosłowne pokrycie**: sekcja 25 "Human Design,
     astrologia i systemy interpretacyjne" z identyczną ideą "zapory interpretacyjnej"
     (opcjonalna, dobrowolna, oddzielona od faktów biologicznych/decyzji wysokiego ryzyka) — to
     jedyny komponent ADR-USER-002, który ma jasny, dosłowny odpowiednik w tym dokumencie.

3. **Pięć trybów działania (Descriptive/Explanatory/Predictive/Prescriptive/Reflective) z
   ADR-USER-002 nie występuje w Warstwie 4** — nie znaleziono takiej listy ani jej polskiego
   odpowiednika w żadnej sekcji. Warstwa 4 nie modeluje "trybów" modelu w ten sposób; ma za to
   9-etapową "pętlę aktualizacji" (2.1) i 24-elementową ontologię obiektów — inna oś podziału.

4. **Zgodne fundamenty filozoficzne** — obie deklaracje brzmią niemal identycznie: ADR-USER-002
   cytuje *"Model jest mapą człowieka, nie człowiekiem"*; Warstwa 4 otwiera się zdaniem *"Model
   jest mapą osoby w określonym czasie i kontekście. Nigdy nie jest jej ostateczną definicją"*
   (linie 32–33) i kończy deklaracją Załącznika M o niemal tej samej treści (linie 2755–2765).
   Prawa verify/contest/correct/delete z ADR-USER-002 mają pełne, rozbudowane pokrycie w Warstwie
   4 — sekcja 5.2 (Prawa użytkownika) i sekcja 24 (Wyjaśnialność, podgląd i korekta modelu, z
   6 trybami korekty: Popraw fakt / Dodaj kontekst / Zakwestionuj / Odrzuć / Zawieś / Przetestuj /
   Usuń).

**Wniosek dla audytu**: Warstwa 4 i "Rozszerzenie Architektury i Integracja v0.2" (źródło
ADR-USER-002) wyglądają na dwa **niezależne, siostrzane dokumenty o tym samym ogólnym temacie**
(model użytkownika/profil rozwojowy), napisane prawdopodobnie w różnym czasie lub przez różnych
autorów w ramach tego samego projektu, dzielące fundamentalną filozofię ("mapa, nie definicja";
prawo do kontestacji/korekty/usunięcia) i częściowo pokrywający się zestaw pojęć (zwłaszcza
warstwa symboliczna/refleksyjna), ale **z różną terminologią najwyższego poziomu** ("Model
Użytkownika i Cyfrowy profil rozwojowy" vs. "Cyfrowy bliźniak"/"Human Digital Twin") i różną
dekompozycją architektoniczną (R0-R8 + 24-obiektowa ontologia vs. 9 nazwanych komponentów + 5
trybów działania). `ADR-USER-002` **nie powinien być cicho przemianowany** na "potwierdzony przez
Warstwę 4" — to dwa różne, wzajemnie niesprzeczne, ale nie tożsame opisy pokrewnej koncepcji.
Ewentualna rekonstrukcja powinna albo (a) traktować je jako dwa odrębne ADR-y/źródła z jawnym
odesłaniem między sobą, albo (b) jeśli zamierzone jest scalenie, wymagać jawnej decyzji
governance (per `docs/FOUNDER_REVIEW_2026-08-15.md` / `GOVERNANCE.md`), a nie milczącego
domniemania tożsamości.

### 9.1 Zgodność / rozbieżność z istniejącym kodem

- **`hos_engine/human_model.py`** (`HumanModel`, `HumanRecord`, `EvidenceType`,
  `RecordStatus`) — implementuje jedynie bardzo wąski wycinek Warstwy 4: płaski, per-domenowy
  magazyn rekordów z `evidence_type` (`USER_DECLARATION/OBSERVATION/VERIFIED_FACT/AI_INFERENCE/
  HYPOTHESIS` — częściowo odpowiada "Źródłom danych" z sekcji 11, ale bez pełnego śladu
  pochodzenia: brak pól czasu obowiązywania, metody, wersji algorytmu) i `RecordStatus`
  (`ACTIVE/CONTESTED/SUPERSEDED/DELETED` — 4 z 8 statusów Załącznika J; brakuje
  `PENDING/SUSPENDED/EXPIRED/WITHDRAWN/ARCHIVED`). Metoda `contest()` odpowiada dokumentowej
  "Zakwestionuj" (24.2), ale sam kod nie implementuje: architektury R0-R8, żadnej z pięciu skal
  (H0-H5, P0-P5, C0-C5, D0-D4, 0-4 jakości), 24-obiektowej ontologii, grafu relacji (sekcja 30),
  wersjonowania/`ModelSnapshot` (sekcja 31), epok profilu (22.3), ani warstwy
  symbolicznej/refleksyjnej (sekcja 25).
- **`hos_engine/personalization.py`** (`ConsentAwarePersonalizer`) — implementuje bramkę zgody na
  poziomie `subject_id/grantee_id/purpose/domain/action` plus boolowską flagę `sensitive`,
  co jest bardzo zredukowaną wersją zgody warstwowej C0-C5 (sekcja 5.1) i klas wrażliwości D0-D4
  (sekcja 27.1) — kod ma jeden poziom binarny tam, gdzie dokument specyfikuje 6+5 poziomów
  granularności. `build_context()` konstruuje coś zbliżone do "Pakietu kontekstowego decyzji"
  (23.1), ale bez pól: aktywny cel, tolerancja ryzyka, luki danych, zakazy/przeciwwskazania.
- Nie znaleziono w repozytorium kodu żadnej implementacji: architektury R0-R8, skal H0-H5/P0-P5,
  klas D0-D4/C0-C5 (poza jednobitowym `sensitive`), grafu Modelu Użytkownika (sekcja 30), ani
  "zapory interpretacyjnej" dla systemów symbolicznych (sekcja 25) — to potwierdza status Warstwy
  4 jako w większości niezaimplementowanej specyfikacji docelowej, podobnie jak większość
  zaimportowanych 2026-08-15 ADR-ów wymienionych w CLAUDE.md tego repozytorium.
