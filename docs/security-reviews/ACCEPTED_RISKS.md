# Rejestr ryzyk zaakceptowanych

Każda pozycja wymaga podpisu foundera (kolumna „Podpis"). Pozycja bez
podpisu jest **zaproponowana, nie zaakceptowana** — i nie liczy się do
warunku zamknięcia 0.9. Format pozycji: identyfikator, opis, waga
pierwotna, uzasadnienie, warunki ponownego rozpatrzenia, podpis+data.

Status legendy: PROPONOWANE (czeka na foundera) · ZAAKCEPTOWANE (z datą
i podpisem).

**2026-08-17: founder zaakceptował wszystkie pięć pozycji (AR-001…AR-005)**
— zgoda wyrażona wprost w sesji roboczej; zapis poniżej przy każdej pozycji.

---

## AR-001 · Brak niezależności przeglądu bezpieczeństwa
- **Waga pierwotna:** WYSOKIE (metodologiczne).
- **Opis:** przeglądy wykonują autorzy kodu i agenty AI użyte do jego
  budowy (DD-008). Brak niezależnego spojrzenia zwiększa ryzyko
  przeoczenia klasy błędów, których wykonawca „nie widzi", bo sam je
  wprowadził.
- **Uzasadnienie akceptacji:** świadoma decyzja foundera (DD-008) o pracy
  własnymi siłami na tym etapie; koszt/dostępność przeglądu zewnętrznego.
- **Warunki ponownego rozpatrzenia:** przed wydaniem produkcyjnym; po
  podłączeniu prawdziwych danych; na żądanie foundera.
- **Status:** ZAAKCEPTOWANE · **Podpis:** founder (dudsi101-svg) — zgoda wyrażona wprost 2026-08-17 w sesji roboczej („Masz moją zgodę, podpisuję się") · **Data:** 2026-08-17

## AR-002 · HMAC jako mechanizm referencyjny
- **Waga pierwotna:** WYSOKIE (dla wdrożenia produkcyjnego).
- **Opis:** podpisy to HMAC-SHA256 z kluczem symetrycznym w pamięci; brak
  podpisów asymetrycznych, chronionego magazynu kluczy, zaufanego czasu
  i szyfrowanego transportu (`security/THREAT_MODEL.md`).
- **Uzasadnienie akceptacji:** wersja 0.x jest implementacją referencyjną,
  nie do danych produkcyjnych; ograniczenie jest jawnie udokumentowane.
- **Warunki ponownego rozpatrzenia:** przed jakimkolwiek wdrożeniem
  przetwarzającym realne dane; wymaga threat modelu wdrożenia.
- **Status:** ZAAKCEPTOWANE · **Podpis:** founder (dudsi101-svg) — zgoda wyrażona wprost 2026-08-17 w sesji roboczej („Masz moją zgodę, podpisuję się") · **Data:** 2026-08-17

## AR-003 · Brak autoryzacji per-wywołanie z kontekstem delegacji
- **Waga pierwotna:** ŚREDNIE.
- **Opis:** grant capability ogranicza narzędzie, akcję i zakres, ale nie
  autoryzuje konkretnego wywołania z konkretnymi argumentami w kontekście
  łańcucha delegacji (OWASP Agentic 2026; `security/THREAT_MODEL.md`).
- **Uzasadnienie akceptacji:** delegacja jest ograniczana do przecięcia
  uprawnień (nie da się delegować capability spoza manifestu), a bramy
  scope/approval domykają najgroźniejsze ścieżki; pełna autoryzacja
  per-call to zaplanowane rozszerzenie, nie luka blokująca.
- **Warunki ponownego rozpatrzenia:** przy dodaniu agentów o wyższym
  ryzyku lub argumentów wpływających na zakres skutku.
- **Status:** ZAAKCEPTOWANE · **Podpis:** founder (dudsi101-svg) — zgoda wyrażona wprost 2026-08-17 w sesji roboczej („Masz moją zgodę, podpisuję się") · **Data:** 2026-08-17
- **Aktualizacja 2026-08-17 (później tego samego dnia):** mechanizm
  wdrożony za zgodą foundera („Tak, należy wdrożyć te rozszerzenia") —
  `hos_engine/call_authorization.py` + brama w `AgentRuntime.evaluate`
  (reguły per-capability: argumenty, słowniki wartości, rozmiar ładunku,
  kontekst delegacji; postawa wobec capability bez reguły deklarowana
  jawnie, nigdy domyślna). Ryzyko zawęża się do pokrycia regułami
  konkretnych wdrożeń — samo istnienie mechanizmu nie konfiguruje reguł.

## AR-004 · Brak produkcyjnego uwierzytelniania i szyfrowania w spoczynku
- **Waga pierwotna:** WYSOKIE (dla wdrożenia produkcyjnego).
- **Opis:** brak auth/authz na poziomie aplikacji i szyfrowania danych
  w spoczynku (README, sekcja „Not production-ready").
- **Uzasadnienie akceptacji:** zakres 0.x; brak przetwarzania danych
  produkcyjnych.
- **Warunki ponownego rozpatrzenia:** etap drugi przeglądu (test
  penetracyjny pełnego wdrożenia) po połączeniu aplikacji/API/logowania.
- **Status:** ZAAKCEPTOWANE · **Podpis:** founder (dudsi101-svg) — zgoda wyrażona wprost 2026-08-17 w sesji roboczej („Masz moją zgodę, podpisuję się") · **Data:** 2026-08-17

## AR-005 · Replay Guard tylko w pamięci
- **Waga pierwotna:** ŚREDNIE.
- **Opis:** `ReplayGuard` trzyma zbiory `message_id`/`nonce` w pamięci
  procesu; restart zeruje okno wykrywania powtórzeń. Wygasanie kopert
  (`expires_at`) ogranicza okno nadużycia, ale nie eliminuje go w oknie
  ważności po restarcie.
- **Uzasadnienie akceptacji:** mechanizm referencyjny; realny system
  potrzebowałby trwałego magazynu nonce z TTL zgodnym z `expires_at`.
- **Warunki ponownego rozpatrzenia:** wdrożenie wieloprocesowe lub
  restartowalne przetwarzające realne komunikaty.
- **Status:** ZAAKCEPTOWANE · **Podpis:** founder (dudsi101-svg) — zgoda wyrażona wprost 2026-08-17 w sesji roboczej („Masz moją zgodę, podpisuję się") · **Data:** 2026-08-17

## AR-006 · Publiczny deploy prototypu aplikacji (GitHub Pages)
- **Waga pierwotna:** WYSOKIE.
- **Opis:** aplikacja użytkownika (`apps/user-demo/`) jest publicznie
  dostępna przez GitHub Pages, przyjmuje wpisy o zdrowiu/energii/śnie
  i (za zgodą C5, klucz własny użytkownika) wywołuje zewnętrzne API
  (OpenAI/Anthropic). AR-002 i AR-004 były akceptowane przy założeniu
  „brak danych produkcyjnych" — publiczny link osłabia to założenie:
  realna osoba może wpisać realne dane zdrowotne do niezabezpieczonego
  prototypu (audyt „Audyt Human OS II", 2026-08-17).
- **Mitygacje wdrożone:** twarda bramka wejściowa w onboardingu
  („PROTOTYP — nie wprowadzaj prawdziwych danych zdrowotnych", wymagane
  potwierdzenie, zdarzenie PROTOTYP_ACK w rejestrze aplikacji);
  zastrzeżenie zdrowotne w ustawieniach; dane wyłącznie w `localStorage`
  przeglądarki użytkownika — repozytorium i Pages nie przechowują żadnych
  danych osób.
- **Uzasadnienie akceptacji:** decyzja DD-015 wariant (a) — deploy
  pozostaje publiczny z twardą bramką onboardingu; dane wyłącznie
  w `localStorage` przeglądarki użytkownika; przegląd prawny nastąpi
  **przed jakąkolwiek promocją linku** poza krąg testerów (szkic pakietu
  do przeglądu: `docs/LEGAL_REVIEW_PACKAGE.md`).
- **Warunki ponownego rozpatrzenia:** przegląd prawny (RODO/wyrób
  medyczny/regulaminy dostawców API); dodanie jakiegokolwiek backendu lub
  kont; udostępnianie linku poza krąg testerów.
- **Status:** ZAAKCEPTOWANE · **Podpis:** founder (dudsi101-svg) — decyzja
  DD-015 wariant (a) wybrana wprost 2026-08-17 w sesji roboczej („Tak,
  należy wdrożyć te rozszerzenia" + wybór „(a) Utrzymać z bramką") ·
  **Data:** 2026-08-17
