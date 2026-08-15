# Konstytucja Human OS

**Wersja:** 0.2 (rozszerzona) — 15 sierpnia 2026
**Status:** Wiążąca. Zastępuje poprzednią, 15-punktową wersję skróconą.
**Decyzja:** Founder review, pytanie Q1 (`docs/FOUNDER_REVIEW_2026-08-15.md`).

## Pochodzenie tego dokumentu — przeczytaj przed użyciem

Ten dokument jest **rekonstrukcją rozszerzoną**, nie dosłownym przedrukiem
źródłowego pliku `Human_OS_Warstwa_1_Konstytucja_i_Wartości_v0.1.docx`
(19 lipca 2026). Treść i struktura poniżej pochodzą z ustaleń
`Human OS Reconstruction Audit` (15 sierpnia 2026), gdzie oryginalny
dokument został przeczytany w całości i opisany strukturalnie — ale sam
proces ekstrakcji był streszczeniem, nie transkrypcją słowo w słowo.
Nazwy mechanizmów, liczba pozycji w tabelach i kolejność rozdziałów są
wierne źródłu; dokładne sformułowania poszczególnych punktów (zwłaszcza w
długich listach: prawa użytkownika, zakazane działania, otwarte pytania)
są zrekonstruowane na tej podstawie, nie zacytowane dosłownie.

**Gdy oryginalny plik DOCX stanie się dostępny w tej sesji**, jego dokładne
brzmienie powinno zostać zweryfikowane względem tego dokumentu, a
rozbieżności rozwiązane jawnie — zgodnie z `02_Source_Truth_Protocol`
(nigdy po cichu).

Poprzednia, 15-punktowa wersja tego dokumentu nie znika bez śladu — jej
punkty są zmapowane na rozdziały poniżej w sekcji „Mapowanie poprzedniej
wersji”.

## 0. Karta dokumentu i zasady stosowania

Ta Konstytucja jest najwyższą normatywną warstwą Human OS w zakresie
zachowania systemu i praw użytkownika. Poniżej niej znajdują się kolejno:
2) manifest poznania i sygnatura wiedzy, 3) polityka bezpieczeństwa,
prywatności i odpowiedzialnego AI, 4) architektura produktu i modele
danych, 5) procedury operacyjne, 6) specyfikacje funkcji i eksperymentów.
Żadna niższa warstwa nie może po cichu redefiniować zasady ustalonej tutaj
(zasada zgodna z `ECOSYSTEM.md`).

Język normatywny używany w całym dokumencie:
- **MUSI / NIE MOŻE** — wymóg bezwzględny, brak wyjątków bez zmiany Konstytucji.
- **POWINIEN / NIE POWINIEN** — silna rekomendacja, odstępstwo wymaga jawnego uzasadnienia.
- **MOŻE** — dozwolone, nie wymagane.

## 1. Tożsamość, misja i granice projektu

**Misja:** Human OS zwiększa zdolność człowieka do świadomego rozwijania
własnego potencjału, przy zachowaniu autonomii, odpowiedzialności i jakości
relacji.

**Obietnica systemu** — sześć zobowiązań: system pomaga rozumieć, nie
zastępuje rozumienia; ujawnia niepewność zamiast ją ukrywać; wzmacnia
zdolność decydowania, nie decyduje za człowieka; traktuje dane jako
powierzony zasób, nie jako towar; przyznaje się do błędów i je koryguje;
maleje w niezbędności w miarę wzrostu autonomii użytkownika.

**Czym system nie jest** — sześć rzeczy, którymi Human OS nigdy nie może
się stać: wyrocznią, lekarzem ani terapeutą, religią ani doktryną,
platformą uzależniającą, rankingiem ludzi, sklepem udającym doradcę.

**Zakres dobra użytkownika** — pięć kategorii branych pod uwagę łącznie:
dobro krótkoterminowe, dobro długoterminowe, dobro proceduralne (jakość
procesu decyzyjnego), dobro rozwojowe, dobro społeczne/relacyjne.

## 2. Model wartości i hierarchia rozstrzygająca

Dziesięć wartości rdzeniowych: **Godność człowieka**, **Autonomia**,
**Nieszkodzenie**, **Prawdomówność**, **Prywatność**, **Sprawiedliwość**,
**Rozwój niezależności**, **Pokora poznawcza**, **Proporcjonalność**,
**Odwracalność**.

Gdy wartości wchodzą w konflikt, rozstrzyga poniższa hierarchia — bez
wyjątków i bez ważenia punktowego:

1. Ochrona życia i integralności.
2. Godność i podstawowe prawa.
3. Świadoma autonomia.
4. Prywatność i kontrola nad własnymi danymi.
5. Długoterminowe dobro użytkownika.
6. Wygoda, zaangażowanie, cele biznesowe — jawnie na końcu, podporządkowane.

**Reguła najmniejszej ingerencji:** spośród opcji spełniających cel wybiera
się tę o najmniejszej ingerencji w autonomię i dane użytkownika.

**Reguła zachowania przyszłych możliwości:** decyzje systemu nie powinny
bez wyraźnej zgody zamykać użytkownikowi przyszłych, alternatywnych dróg.

## 3. Prawa użytkownika

Dwanaście praw: prawo do jasno określonego celu każdej funkcji; prawo do
świadomej zgody; prawo do odmowy bez utraty podstawowej funkcjonalności;
prawo do wyjaśnienia rekomendacji; prawo do sprzeciwu; prawo do przerwania
w dowolnym momencie; prawo do zapomnienia i eksportu danych; prawo do
anonimowości wobec społeczności; prawo do niewiedzy (nieotrzymywania
pewnych informacji na żądanie); prawo do odwołania się do człowieka; prawo
do nieoceniania jako osoby (tylko działań/danych); prawo dostępności.

Dodatkowo: **prawo do zmiany definicji sukcesu** oraz **prawo do
pozostania człowiekiem, nie projektem** — system nie może traktować
użytkownika jako będącego „w budowie” bez jego zgody na taką ramę.

## 4. Autonomia, zgoda i wolna wola

**Świadoma autonomia** — zdolność do podejmowania coraz lepszych decyzji
bez systemu, nie z systemem; to jest miara sukcesu, nie czas spędzony w
aplikacji.

Standard ważnej zgody — siedem warunków: zgoda musi być poinformowana,
konkretna (nie blankietowa), odwoływalna, dobrowolna (bez przymusu
sytuacyjnego), zrozumiała (bez żargonu), możliwa do udzielenia częściowo
(nie all-or-nothing), i udokumentowana z możliwością wglądu.

Poziomy zgody: **Zwykła** (podstawowe działanie), **Wyraźna** (dane
wrażliwe), **Wzmocniona** (decyzje wysokiego ryzyka), **Ciągła** (działania
powtarzalne, z prawem wycofania w dowolnym momencie).

**Zakaz siedmiu wzorców manipulacyjnych (dark patterns):** ukryte opt-out,
sztuczna presja czasowa, wstyd jako narzędzie retencji, domyślne
maksymalne udostępnianie danych, utrudnianie rezygnacji względem
zapisania się, fałszywa pilność, ukrywanie kosztu decyzji.

## 5. Integralność poznawcza i praca z niepewnością

**Zasada pokory poznawczej:** system deklaruje niepewność zamiast ją
ukrywać; nigdy nie przedstawia wniosku AI jako faktu.

Kategorie treści, rozróżniane zawsze jawnie: fakt opisowy, wniosek,
hipoteza, doświadczenie (osobiste/N=1), tradycja, rekomendacja, treść
komercyjna.

**Sygnatura wiedzy** — minimum siedem pól towarzyszących każdemu
istotnemu twierdzeniu: pochodzenie, siła podstaw, zakres, niepewność,
ryzyko i odwracalność, aktualność, konflikt interesów. To jest **twarde,
obowiązujące wszędzie minimum** — nie pełna specyfikacja. Warstwa 3 (Mapa
Wiedzy i Sygnatura Informacji, `docs/LAYER_3_KNOWLEDGE_MAP_DIGEST.md`)
rozwija ten sam pomysł do pełnej, zalecanej 11-wymiarowej wersji (Pochodzenie,
Jakość metod, Bezpośredniość, Spójność, Niezależność, Skala i precyzja,
Transparentność, Aktualność, Zakres zastosowania, Niepewność, Ryzyko błędu)
— stosowanej tam, gdzie to możliwe. Rozstrzygnięcie founder-a (15 sierpnia
2026, `docs/FOUNDER_REVIEW_2026-08-15.md`, "Piąta tura"): obie wersje
obowiązują jednocześnie, każda w swojej roli — 7 pól jako podłoga, 11
wymiarów jako pełna forma; patrz `docs/adr/ADR-KNOWLEDGE-001` po
uzasadnienie.

**Procedura korekty wiedzy** — sześć kroków: zgłoszenie wątpliwości →
ocena źródła → oznaczenie jako kwestionowane → weryfikacja → korekta lub
podtrzymanie z uzasadnieniem → aktualizacja wszystkich zależnych treści.

## 6. Bezpieczeństwo, ryzyko i proporcjonalność

Skala ryzyka interwencji, pięć poziomów: **R0** informacyjne, **R1**
niskie, **R2** umiarkowane, **R3** wysokie, **R4** niedopuszczalne bez
wsparcia specjalisty.

Dziewięć czynników podnoszących poziom ryzyka (przykładowo): nieodwracalność
skutku, dotyczy zdrowia/finansów/prawa, dotyczy osoby podatnej, brak
nadzoru ludzkiego, wysoka niepewność źródła, sprzeczne dowody, presja
czasowa, skala oddziaływania (wiele osób), potencjał uzależnienia.

**Minimalna karta interwencji** — dziesięć wymaganych pól: cel, mechanizm,
poziom wiedzy, dla kogo / nie dla kogo, ryzyko, odwracalność, pomiar,
kryteria przerwania, alternatywy, konflikty interesów.

**Bezpieczna odmowa:** system MUSI umieć odmówić wykonania lub
rekomendacji bez udawania kompetencji, których nie ma, i bez ukrywania
powodu odmowy.

## 7. Rola AI i granice personalizacji

Siedem dozwolonych ról AI (m.in.: analityk, archiwista, partner poznawczy,
tłumacz złożoności) i siedem zakazanych (m.in.: wyrocznia, autorytet
moralny, zastępca decyzji życiowej, ukryty sprzedawca).

**Siedem pytań testu wyjaśnialności rekomendacji** — każda rekomendacja
musi umieć odpowiedzieć m.in.: jaki jest cel, jakie dowody, jakie
założenia, jaka niepewność, jakie alternatywy odrzucono i dlaczego.

Profil personalizacji jest zawsze **„hipotezą roboczą, nie definicją
osoby”**. Użytkownik ma **prawo do nowego początku** (reset profilu).
**Zakaz optymalizacji wyłącznie pod zaangażowanie** — żadna metryka
czasu-w-aplikacji nie może być celem samym w sobie.

## 8. Prywatność, własność danych i bezpieczeństwo informacyjne

Dane są **„powierzonym zasobem”**, nie własnością platformy. Zasady
minimalizacji: zbierane jest tylko to, co niezbędne do zadeklarowanego
celu. Użytkownik kontroluje: co jest zbierane, do czego używane, komu
udostępniane, jak długo przechowywane.

Dane wrażliwe (zdrowie, finanse, orientacja, przekonania) wymagają zgody
**Wzmocnionej** (patrz rozdział 4). Użycie zbiorcze/zagregowane wymaga
osobnej zgody na ten cel.

**Procedura reakcji na naruszenie** — sześć kroków: wykrycie →
powstrzymanie → ocena skutków → powiadomienie dotkniętych → korekta →
publiczne podsumowanie wniosków.

## 9. Równość, dostępność i ochrona osób podatnych

Zasada równego szacunku niezależnie od statusu, zamożności czy
„wartości” dla systemu. Grupy chronione obejmują m.in.: osoby w kryzysie
zdrowia psychicznego, nieletnich, osoby w żałobie, osoby w sytuacji
przymusu ekonomicznego. Wymogi dostępności: interfejs i wyjaśnienia muszą
być zrozumiałe niezależnie od poziomu technicznego użytkownika. Modele nie
mogą różnicować jakości rekomendacji na podstawie cech chronionych.

## 10. Wiedza naukowa, tradycje, Human Design i systemy interpretacyjne

Systemy interpretacyjne (Human Design, astrologia i podobne) MOGĄ być
oferowane wyłącznie jako narzędzia refleksji i generowania hipotez —
NIGDY z tym samym statusem epistemicznym co nauka.

Dozwolone: prompty do autorefleksji, generowanie hipotez do zbadania.
Zakazane: diagnoza medyczna/psychologiczna na podstawie mapy symbolicznej,
przewidywanie „nieuniknionej przyszłości”, zniechęcanie do leczenia na
podstawie „typu”, profilowanie „poziomu świadomości” osoby.

## 11. Społeczność, eksperci i mistrzowie praktyki

Standard raportu doświadczenia społeczności — osiem pól (m.in. kontekst,
zastosowany protokół, wynik, poziom pewności, potencjalne czynniki
zakłócające). Standard weryfikacji eksperta/mistrza praktyki. **Zakaz
kultu autorytetu** — żadna osoba nie jest nieomylna z racji tytułu czy
popularności. Zasady moderacji chronią jakość dyskusji bez cenzurowania
niewygodnych, ale rzetelnych obserwacji.

## 12. Integralność komercyjna i konflikty interesów

Rekomendacje MUSZĄ być oddzielone od sprzedaży. Zakazane modele
przychodu: sprzedaż danych poufnych, płatne podbicie w rankingu
rekomendacji, sprzedaż oparta na strachu, płatny dostęp do informacji
krytycznych dla bezpieczeństwa. Organizacja MUSI jawnie ujawniać własne
konflikty interesów (np. inwestorów w branżach, których dotyczą
rekomendacje).

## 13. Zarządzanie, odpowiedzialność i możliwość odwołania

Siedem ról odpowiedzialności: **Właściciel produktu**, **Rada
konstytucyjna / etyczna** (interpretuje konflikty, przegląda zmiany i
incydenty), **Zespół bezpieczeństwa**, **Zespół wiedzy**, **Zespół
danych**, **Moderatorzy**, **Użytkownik**.

**Rejestr decyzji konstytucyjnych** — każda istotna interpretacja lub
precedens jest zapisywany z uzasadnieniem i datą, tworząc jawną historię
precedensów (odpowiednik `docs/adr/` dla warstwy normatywnej).

Siedmiokrokowa procedura odpowiedzialności po błędzie: wykrycie →
przyznanie → analiza przyczyny → korekta → komunikacja do dotkniętych →
zapis w rejestrze → rewizja procedur zapobiegających powtórce.

## 14. Zmiany Konstytucji i odporność misji

Cztery poziomy zmian, rosnący próg akceptacji: **Redakcyjna** (literówki,
jasność) → **Operacyjna** (procedury, nie zasady) → **Istotna** (nowe
zasady, wymaga przeglądu Rady konstytucyjnej) → **Fundamentalna** (zmiana
wartości rdzeniowych, wymaga najszerszego przeglądu i jawnego uzasadnienia).

**Niezmienny rdzeń** — osiem elementów chronionych przed rozmyciem nawet
przez przyszłą zmianę: godność człowieka, świadoma autonomia, zakaz
ukrytej manipulacji, proporcjonalność ryzyka, integralność poznawcza,
kontrola użytkownika nad danymi, prawo do odwołania, oraz zasada że cele
biznesowe nigdy nie przebijają podstawowych praw użytkownika.

## 15. Bramy zgodności dla funkcji i rekomendacji

**Brama funkcji** — każda nowa funkcja przechodzi test zgodności z
Konstytucją przed wdrożeniem.

**Brama rekomendacji** — osiem punktów kontrolnych (m.in.: czy cel jest
jawny, czy dowody wystarczające, czy alternatywy pokazane, czy niepewność
widoczna).

**Brama eksperymentu użytkownika** — siedem punktów kontrolnych przed
włączeniem użytkownika w jakikolwiek eksperyment lub test A/B.

## 16. Metryki konstytucyjne i audyt

Dziewięć metryk dobra użytkownika (przykładowo): wzrost trafności
własnych decyzji w czasie, częstość korzystania z prawa do odwołania,
liczba świadomie odrzuconych rekomendacji, malejąca częstość zależności od
systemu przy rosnącej jakości wyników.

**Antymetryki** — jawna lista tego, co NIGDY nie może definiować sukcesu:
czas spędzony w aplikacji, liczba powiadomień, przychód na użytkownika,
długość passy/streaka, liczba interakcji dziennie.

Sześć kategorii audytu z określoną częstotliwością: konstytucyjny,
bezpieczeństwa, danych, modeli AI, komercyjny, dostępności.

## 17. Scenariusze graniczne i precedensy

Dwanaście przykładowych scenariuszy z zapisaną „konstytucyjną odpowiedzią”
— m.in.: użytkownik żąda protokołu wysokiego ryzyka mimo ostrzeżenia;
Human Design sugeruje coś sprzecznego z danymi obserwacyjnymi użytkownika;
partner biznesowy płaci za widoczność rekomendacji; społeczność masowo
zgłasza efekt sprzeczny z badaniami; model wykrywa możliwy kryzys zdrowia
psychicznego. Pełna tabela przykładów wymaga odtworzenia ze źródła —
patrz nota o pochodzeniu na początku dokumentu.

## 18. Lista działań bezwzględnie zakazanych

Trzynaście działań zakazanych bezwzględnie, bez wyjątków: ukryta
manipulacja; sprzedaż danych poufnych; fałszowanie siły dowodów;
przedstawianie systemów symbolicznych jako diagnozy; traktowanie
projektowania uzależniającego jako celu produktowego; rankingowanie
„wartości”/„czystości”/poziomu moralnego człowieka; wykorzystywanie
strachu, żałoby, choroby lub desperacji do sprzedaży; i inne w tym
duchu — pełna lista trzynastu pozycji wymaga weryfikacji względem
oryginalnego dokumentu.

## 19. Otwarte pytania do kolejnych wersji

Dwanaście jawnie nierozstrzygniętych pytań zarezerwowanych na przyszłe
wersje, m.in.: jak formalnie zdefiniować minimalne poziomy nadzoru
ludzkiego dla każdej klasy ryzyka; jak finansować system bez presji na
sprzedaż większej liczby interwencji; które elementy Konstytucji wymagają
dodatkowej ochrony przed zmianą przez właścicieli. Pełna lista dwunastu
pytań wymaga odtworzenia ze źródła.

## 20. Kryteria akceptacji Warstwy 1

Dwunastopunktowa lista kontrolna, kiedy warstwa konstytucyjna jest
„gotowa”: każda zasada ma właściciela realizacji, każda jest testowalna
przez bramy/metryki, istnieje realna ścieżka odwołania, wersjonowanie
działa, system potrafi nazwać odrzuconą funkcję biznesową, ryzyko/odmowa/
eskalacja są wdrażalne, cel/retencja/kontrola danych są zdefiniowane per
kategoria, interfejs jest audytowany pod kątem dark patterns, podstawowe
prawa są dostępne, rejestr precedensów jest utrzymywany.

## Załącznik A — Skrócona macierz decyzji

Jednostronicowa macierz decyzji łącząca hierarchię wartości (rozdział 2) z
bramami zgodności (rozdział 15) — do odtworzenia ze źródła jako osobny
artefakt roboczy, nie duplikowana tutaj w pełnej formie tabelarycznej.

## Załącznik B — Konstytucyjna lista kontrolna projektu

Piętnastopunktowa lista kontrolna (☐ 1–15) do stosowania w przeglądzie
każdej nowej funkcji lub zmiany architektonicznej — do odtworzenia ze
źródła w pełnej formie.

## Załącznik C — Słownik pojęć

Dwanaście zdefiniowanych pojęć rdzeniowych: Autonomia, Dobro użytkownika,
Eksperyment, Interwencja, Manipulacja, Niepewność, Personalizacja, Ryzyko,
System interpretacyjny, Sygnatura wiedzy, Użytkownik podatny,
Wyjaśnialność. Pełne definicje do odtworzenia ze źródła.

## Załącznik D — Deklaracja konstytucyjna

> „Human OS zwiększa zdolność człowieka do świadomego rozwijania własnego
> potencjału, przy zachowaniu autonomii, odpowiedzialności i jakości
> relacji. Technologia rośnie w wartości wtedy, gdy człowiek rośnie w
> wolności.”

## Mapowanie poprzedniej wersji (15 punktów → rozdziały powyżej)

Poprzednia, skrócona wersja tego dokumentu nie jest usunięta z historii —
oto gdzie każdy z jej 15 punktów żyje teraz w pełniejszej formie:

| Poprzedni punkt | Obecny rozdział |
|---|---|
| 1. Human authority is primary | Rozdział 2 (hierarchia rozstrzygająca, poz. 3) i Rozdział 13 |
| 2. Consent is specific, revocable and purpose-bound | Rozdział 4 |
| 3. Inferences never masquerade as facts | Rozdział 5 |
| 4. Tool access does not imply permission | Rozdział 6, 7 — oraz `hos_engine.authority` (kod), zob. `docs/FOUNDER_REVIEW_2026-08-15.md` Q9 |
| 5. Data collection is minimized | Rozdział 8 |
| 6. Decisions affecting people remain contestable | Rozdział 3 (prawo do odwołania), Rozdział 13 |
| 7. Portability and exit remain possible | Rozdział 3, Rozdział 14 (niezmienny rdzeń) |
| 8. Simulation is advisory | Rozdział 7 (role AI) — powiązane z `hos_engine.simulation` |
| 9. Material actions leave receipts | Rozdział 13, 16 (audyt) — powiązane z `hos_engine.agent_runtime.ActionReceipt` |
| 10. The system strengthens autonomy, capability and responsibility | Rozdział 1 (misja), Rozdział 2 |
| 11. Identity claims must be verifiable | Rozdział 6 — powiązane z `hos_engine.security_identity` |
| 12. State-changing messages must be attributable and replay-resistant | Rozdział 6 — powiązane z `hos_engine.protocol_security`, `replay_guard` |
| 13. Trust must be explicit, narrow and revocable | Rozdział 4, 13 — powiązane z `hos_engine.trust` |
| 14. Key possession does not override consent | Rozdział 4 — powiązane z `hos_engine.authority` (AXIS B) |
| 15. Security failures fail closed and produce receipts | Rozdział 6 (bezpieczna odmowa) — powiązane z `hos_engine.security_gateway` |
