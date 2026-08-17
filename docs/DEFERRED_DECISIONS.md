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
**Wdrożone 2026-08-17:** `hos_engine/emergency_root.py` —
`EmergencyKeyDescriptor` (bez materiału klucza), `EmergencyRootPolicy`
(wszystkie pola jawne, zero domyślnych; role AGENT/SERVICE/SYSTEM_PROCESS
nigdy nie mogą być kustoszami), `EmergencyRootKernel` (konstrukcja bez
polityki niemożliwa strukturalnie; referencyjny przepływ k-z-n na
deklarowanych wejściach; jeden klucz na tożsamość; wygasanie TTL;
append-only audyt wszystkich zdarzeń, opcjonalnie trwały na łańcuchu
hashy jako `STATE_OBSERVED`). 13 testów, wartości syntetyczne jawnie
oznaczone. Parametry produkcyjne (TTL, siła uwierzytelnienia, konkretne
k-z-n) — nadal osobna decyzja foundera.

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
**Wdrożone 2026-08-17:** `hos_engine/decision_scales.py` — struktura
(zamknięte listy kodów DI-1..8/IQ0..5/AR0..5 z Załącznika I), pomiar
(`ScaleMeasurement`: kod + podstawa + tożsamość, wg §18.2), polityka
interpretacji (`InterpretationPolicy`: jawna, wersjonowana, z aprobatą,
bez żadnej domyślnej instancji) i `ScaleInterpreter` zwracający
`CONFIGURATION_REQUIRED` jako wynik pierwszej klasy przy braku lub
niekompletności konfiguracji. 14 testów; fixtures jawnie syntetyczne.
Semantyka poszczególnych poziomów i progi — nadal otwarte (decyzja
foundera po kalibracji). Profil dziesięcioosiowy §18 nie wchodzi w zakres
tego szkieletu (zgoda obejmowała DI/IQ/AR).
**2026-08-17 (podpis kalibracji):** founder podpisał semantyki IQ0–IQ5
i AR0–AR5 oraz polityki `HOS-POL-IQ-001`/`HOS-POL-AR-001` v0.1.0
w trybie fazy cienia (`policies/scale.interpretation.policies.json`);
ścieżka uzupełnienia DI = odczyt sekcji 6.1 źródłowego DOCX (czeka na
źródło). Przejście polityk z fazy cienia na tryb operacyjny — osobna
decyzja po przeglądzie korpusu pomiarów.
**2026-08-17 (źródło dostarczone):** founder wgrał DOCX Warstwy 5 do
sesji; sekcje 5.2/6.1/8.2 odczytane z bajtów. Pełne semantyki źródłowe
wszystkich trzech skal w `DI_IQ_AR_CALIBRATION_PROPOSAL.md` v0.2 wraz
z tabelą rozbieżności v0.1→v0.2 (m.in. AR1: źródło surowsze niż
interpolacja). Polityki v0.2.0 (IQ/AR/DI, reguły dosłownie ze źródła)
czekają na podpis foundera; po podpisie v0.1.0 przechodzi do sekcji
superseded w konfiguracji.

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

## DD-009 · Zdarzenia `commons_*` w kanonicznym słowniku + fundament moderacji (CZĘŚCIOWO ROZSTRZYGNIĘTE 2026-08-17)
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
**Rozstrzygnięcie częściowe (2026-08-17):** founder zatwierdził wdrożenie
części 1 rekomendacji („Tak, należy wdrożyć te rozszerzenia" + wybór
„Commons: 16 zdarzeń") — komplet typów wchodzi do kanonicznego słownika
z ADR, schematem i mapowaniem ryzyka wyzwań publicznych na R0–R4.
Część 2 (ModerationCase i model ról moderacyjnych) pozostaje OTWARTA —
founder świadomie jej nie wybrał; propozycja modelu ról powstanie przed
jakimkolwiek kodem moderacji.
**Uzupełnienie (2026-08-17, później):** founder zatwierdził także granice
klas mapowania R0–R4 („Tak, róbmy to" — tabela przedstawiona wprost);
`policies/commons.challenge.risk.json` przechodzi ze statusu SZKIC na
ZATWIERDZONE, pozostając dokumentacyjne do czasu kodu Commons.

## DD-010 · Wzorzec HOSId w schemacie vs identyfikatory silnika (RESOLVED 2026-08-17)
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
**Rozstrzygnięcie foundera (2026-08-17):** opcja (a) — wzorzec `HOSId`
rozszerzony do `^HOS-[A-Z]{2,8}-[0-9A-F]{6,}$`. Żaden istniejący
identyfikator nie traci ważności (ID cyfrowe są podzbiorem).
**Wdrożone 2026-08-17:** `schemas/common.schema.json`, addendum
w `docs/HOS_ENTITY_RELATION_EVENT_SCHEMA_v0.1.md`, test pełnej walidacji
koperty zdarzenia Recovery włączony (pola warstwy magazynu — hash
łańcucha i `causation_id: None` — są zdejmowane przed walidacją
kanoniczną i opisane w teście; format change-log `HOS-CHG-...` z tekstu
ADR-RECOVERY-004 nadal nie ma implementacji ani pokrycia wzorcem).
Walidacja ujawniła też, że koperta Recovery wkładała wolnotekstowy
`scope` do `subject_ids` (typowanych jako HOSId) — poprawione: scope
pozostaje w payload, do `subject_ids` trafia wyłącznie ID encji
z zakresu `entity:...`.

## DD-011 · Cennik i pakowanie wydania sklepowego (OPEN)

**Aktualizacja 2026-08-17 (kierunek foundera, PROVISIONAL):** founder wskazał
„zamiast robić sekcji premium — miesiąc za darmo, choć trzeba się zastanowić".
Wdrożono prowizorycznie: każdy nowy użytkownik dostaje **30 dni pełnego
dostępu na start** (bez podawania czegokolwiek; zdarzenia `intro_started`/
`intro_expired` w rejestrze; wygaśnięcie niczego nie kasuje ani nie blokuje —
biegnące eksperymenty biegną dalej). Miesiąc powitalny zastępuje 7-dniowy
trial (jednorazowość zachowana). Ekran „Wersja i Premium" pozostaje jako
porównanie wersji i miejsce aktywacji — nie wita już nowego użytkownika.
Do ostatecznej decyzji foundera: czy 30 dni zostaje, czy wraca krótszy trial,
oraz jak to połączyć z rozliczeniami sklepu (trial subskrypcji po stronie
Google Play/App Store vs. własny okres powitalny).
Founder zatwierdził kierunek (2026-08-17): dystrybucja sklepowa aplikacji
osobistej w modelu freemium — wersja bezpłatna z ograniczeniami, Premium
z pełnym dostępem. Granice konstytucyjne (eksport/wyjście/model/tryby
awaryjne nigdy płatne; bez reklam; bez sprzedaży danych; bez pól
sponsorowanych) oraz podział funkcji w prototypie: `ADR-APP-001`.
Otwarte pozostają decyzje wyłącznie founderskie:
1) **cena subskrypcji** i waluty/rynki startowe;
2) **ostateczny podział free/premium** (prototyp: premium = 3 równoległe
   eksperymenty + prognoza zbiorcza, Plan/przypomnienia, moduł Wspólnie);
3) **długość okresu próbnego** (prototyp: 7 dni, jednorazowo, bez karty);
4) **kanał pakowania**: PWA→TWA (Google Play) i cienki wrapper (App Store)
   vs. Capacitor; konto dewelopera, podpisywanie, polityka aktualizacji;
5) **prawna wersja polityki prywatności i regulaminu** (teksty w aplikacji
   są dziś szczere, ale nie przeszły przeglądu prawnego).
**Rekomendacja:** utrzymać podział z ADR-APP-001; pakowanie przez PWA→TWA
(najmniej kodu, zachowuje architekturę local-first); przegląd prawny przed
publikacją. **Tymczasowo:** mechanizm referencyjny kodu aktywacyjnego
(format-only) + próbne 7 dni, wszystko audytowane w rejestrze aplikacji.


## DD-012 · Konta i logowanie w wydaniu sklepowym (OPEN)
Pytanie foundera (2026-08-17): „systemy logowania jakieś mamy?". Stan
faktyczny: aplikacja celowo **nie ma** logowania, kont ani serwera — cała
tożsamość jest lokalna (dane w pamięci urządzenia; wymiana „Wspólnie" przez
pakiety przekazywane samodzielnie; pseudonim zamiast tożsamości). Silnik ma
osobny rejestr tożsamości i kluczy (`security_identity`, HMAC, role), ale to
mechanizm referencyjny protokołu, nie system kont użytkowników aplikacji.
Logowanie stałoby się potrzebne dopiero dla: synchronizacji między
urządzeniami, publicznych wyzwań z moderacją (etapy 5–6 rolloutu Wspólnie,
DD-009) lub odzyskiwania danych po utracie urządzenia.
**Rekomendacja:** wydanie 1 bez kont (lokalnie + eksport jako backup —
najmniejsza powierzchnia ryzyka, spójna z Konstytucją); jeśli sync stanie się
potrzebny, najpierw szyfrowany end-to-end backup pliku eksportu (klucz u
użytkownika), a dopiero w dalszej kolejności konta z logowaniem platformy;
pełna tożsamość federacyjna wg HOSS dopiero z prawdziwym Hubem.
**Tymczasowo:** bez kont; README i ekran „O aplikacji" mówią to wprost.

## DD-013 · Przewodnik AI: backend, model i zakres danych wydania sklepowego (CZĘŚCIOWO ROZSTRZYGNIĘTE 2026-08-17)
Dyrektywa foundera (2026-08-17): agent LLM w aplikacji, objaśniający sytuacje
i generujący pomysły na poprawę domen na bazie danych użytkownika. Wdrożone
referencyjnie (ADR-APP-002): zgoda C5, zminimalizowany pakiet danych
(nigdy hipotezy/rejestr/Wspólnota/klucz), własny klucz API użytkownika
przechowywany poza stanem aplikacji, wyjścia wyłącznie jako hipotezy,
przyjęcie pomysłu = jawny akt przez bramę G4, pełny audyt (w tym odmowy
modelu). Otwarte decyzje foundera:
1. **Backend dla sklepu**: BYO-key nie nadaje się dla masowego użytkownika —
   potrzebny backend aplikacji (kustodia klucza, limity, nadużycia, koszty
   w cenie subskrypcji?) vs pozostawienie BYO-key jako opcji zaawansowanej.
2. **Model domyślny i polityka kosztów** (dziś: claude-opus-5, wybór
   sonnet/haiku w konfiguracji).
3. **Zakres danych**: czy Przewodnik może kiedykolwiek czytać historię
   rozmowy „O mnie" (dziś: nigdy) — wymagałoby to rozszerzenia C5.
4. **Przegląd prawny** kopii zgody C5 (dane zdrowotne wychodzą do API).
**Tymczasowo:** mechanizm referencyjny BYO-key, funkcja premium.
**Rozstrzygnięcie foundera (2026-08-17, architektura):** przyjęta
architektura **trzech wymiennych silników** („wymienny mózg" — ADR-APP-003):
(1) lokalny na urządzeniu — domyślny, gdy dostępny, nic nie wychodzi na
zewnątrz; (2) chmura na własnym kluczu użytkownika; (3) chmura w cenie
subskrypcji przez backend. Uzasadnienie foundera: modele będą się zmieniać
na przestrzeni czasu — warstwa silnika jest stabilnym kontraktem, modele
pod spodem wymienne. Wdrożone: selektor silnika, silnik lokalny na
wbudowanym AI przeglądarki (wykrywanie funkcji, degradacja), kopia zgody
zależna od silnika, silnik w audycie. Nadal otwarte: pkt 1 (kształt
backendu — teraz jako silnik nr 3), pkt 2 (model domyślny chmury i polityka
kosztów: analiza kosztów wskazuje Sonnet/Haiku dla subskrypcji), pkt 3-4
oraz pełny model lokalny (WebLLM, pobieranie na życzenie ~1,5–2,5 GB) jako
etap PWA.

## DD-014 · Powiadomienia push w tle (OPEN)
Dyrektywa foundera (2026-08-17): zewnętrzne powiadomienia + podsumowanie
ustaleń (wyzwania, rytuały, postanowienia) z odhaczaniem i godzinami.
Wdrożone: sekcja „Ustalenia dnia" w Planie (checklista wyzwań Wspólnie,
rytuałów i postanowień z odhaczaniem, cofaniem, godzinami per pozycja,
audytem) + powiadomienia systemowe (Notification API): opt-in, jedno
powiadomienie o ustawionej porze dla niezrobionych pozycji, bez duplikatów,
znikają po odhaczeniu; działają przy uruchomionej/zainstalowanej aplikacji
(PWA). Otwarte: **push przy całkiem zamkniętej aplikacji** wymaga Web Push
(backend z kluczami VAPID, subskrypcje push, retencja endpointów) — wiąże
się z DD-013 (backend Przewodnika) i DD-011 (wydanie sklepowe).
**Rekomendacja:** jeden wspólny backend etapu sklepowego obsługujący
rozliczenia, klucze Przewodnika i Web Push; do tego czasu powiadomienia
lokalne + poranna odprawa wystarczają dla wiernego użycia dziennego.
**Tymczasowo:** Notification API bez backendu; kopia w aplikacji mówi to
wprost.

## DD-015 · Status publicznego deployu prototypu (GitHub Pages) (RESOLVED 2026-08-17)
**Zgłoszone:** 2026-08-17 (audyt „Audyt Human OS II", priorytet 0).
**Kontekst:** `.github/workflows/pages.yml` publikuje `apps/user-demo/`
pod publicznym adresem GitHub Pages. Aplikacja przyjmuje samoopisowe dane
o zdrowiu/energii/śnie i — za zgodą C5, na kluczu własnym użytkownika —
wywołuje zewnętrzne API (OpenAI/Anthropic). AR-002/AR-004 podpisano przy
założeniu „brak danych produkcyjnych"; publiczny link to założenie
osłabia (realna osoba, realne dane, niezabezpieczony prototyp).
**Wdrożone niezależnie od decyzji (2026-08-17):** twarda bramka
onboardingu — bez potwierdzenia „to prototyp, żadnych prawdziwych danych
zdrowotnych" nie da się wejść; wpis AR-006 w rejestrze ryzyk
(PROPONOWANE, czeka na podpis).
**Do decyzji foundera (jedno z trzech):**
(a) utrzymać publiczny deploy z bramką — wtedy podpis AR-006 i przegląd
    prawny przed jakąkolwiek promocją linku;
(b) ograniczyć widoczność (wyłączyć workflow Pages lub przenieść na
    prywatny podgląd) do czasu przeglądu prawnego;
(c) utrzymać deploy wyłącznie jako demo z danymi syntetycznymi
    (tryb bez możliwości wpisywania własnych danych).
**Blokuje:** promocję linku poza krąg testerów; nie blokuje prac nad
silnikiem.
**Rozstrzygnięcie (2026-08-17):** founder wybrał wprost **wariant (a)** —
deploy pozostaje publiczny z twardą bramką onboardingu; AR-006 podpisane
(`docs/security-reviews/ACCEPTED_RISKS.md`); przegląd prawny odbywa się
**przed jakąkolwiek promocją linku** poza krąg testerów (szkic pakietu:
`docs/LEGAL_REVIEW_PACKAGE.md`). Zapis zgody: „Tak, należy wdrożyć te
rozszerzenia" + wybór „(a) Utrzymać z bramką" w sesji roboczej.
## DD-016 · Biometria na żywo: HealthKit/Health Connect i Web Bluetooth (OPEN)
Dodano (2026-08-17, dyrektywa foundera „bajery biometryczne", ADR-APP-004):
import plików zdrowotnych lokalnie (C6) + blokada biometryczna (WebAuthn).
Poza zasięgiem PWA pozostają: (a) ciągłe, automatyczne sczytywanie z Apple
Health / Google Health Connect — wymaga aplikacji natywnej (etap sklepowy);
(b) czujniki Web Bluetooth na żywo (pas tętna) — działa tylko w Chrome na
Androidzie/desktopie, brak w iOS Safari.
**Do decyzji foundera:** (1) czy pakujemy aplikację natywnie (Capacitor/TWA)
z modułem HealthKit/Health Connect i kiedy; (2) czy automatyczna
synchronizacja to wyróżnik Premium (sam dostęp do własnych danych pozostaje
bezpłatny — podłoga ADR-APP-001 §2; płatna mogłaby być automatyzacja);
(3) czy dokładać Web Bluetooth już teraz mimo braku wsparcia na iPhonie.
**Rekomendacja:** (1) tak, razem z decyzją DD-011 o kanale sklepowym;
(2) tak — automatyzacja jako Premium, import plików zawsze darmowy;
(3) nie teraz — wartość niska do czasu wersji natywnej.
**Tymczasowo:** import plików (XML/CSV/JSON) + jawny zapis średnich do
modelu pokrywa potrzebę twardych mierników eksperymentów.

## DD-017 · Warstwa 6: brakujące szczegóły §28/§29 (pełna lista zakazów adaptacji, limit portfela) (OPEN)
Drugi przyrost `hos_engine/experiment_engine.py` (2026-08-17) wdrożył
adaptacje protokołu i portfel równoległych eksperymentów, ale digest
(`docs/LAYER_6_EXPERIMENT_ENGINE_DIGEST.md`) nie niesie pełnej treści
źródła: z pięciu zakazanych adaptacji (§28.2) cytuje dosłownie dwie
(usuwanie niekorzystnych dni/zdarzeń dla poprawy obrazu; automatyczne
dokładanie kolejnej interwencji), a §29.1 nie podaje konkretnej liczby
limitu aktywnych zmian.
**Wdrożone tymczasowo (wzorzec DD-006/DD-007 — konfiguracja wymagana,
zero domyślnych):** dwa cytowane zakazy strukturalnie (brak API usuwania
obserwacji/zdarzeń; odmowa dokładania interwencji w trakcie); limit
portfela jako obowiązkowy jawny argument konstruktora bez wartości
domyślnej; adaptacje wersjonowane, historia zachowana.
**Do decyzji foundera / do źródła:** (1) pełna lista pięciu zakazów §28.2
i reguły zatrzymania adaptacji §28.3 — najlepiej przez ponowny odczyt
oryginalnego DOCX Warstwy 6; (2) kanoniczna wartość limitu §29.1 (aplikacja
używa dziś 3 równoległych eksperymentów + 5 celów — przyjąć te wartości?).
**Rekomendacja:** dosłać/odczytać źródło zamiast zgadywać; do tego czasu
konfiguracja jawna przy każdym użyciu.
