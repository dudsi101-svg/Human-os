# Rejestr ryzyk zaakceptowanych

Każda pozycja wymaga podpisu foundera (kolumna „Podpis"). Pozycja bez
podpisu jest **zaproponowana, nie zaakceptowana** — i nie liczy się do
warunku zamknięcia 0.9. Format pozycji: identyfikator, opis, waga
pierwotna, uzasadnienie, warunki ponownego rozpatrzenia, podpis+data.

Status legendy: PROPONOWANE (czeka na foundera) · ZAAKCEPTOWANE (z datą
i podpisem).

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
- **Status:** PROPONOWANE · **Podpis:** ______________ · **Data:** ______

## AR-002 · HMAC jako mechanizm referencyjny
- **Waga pierwotna:** WYSOKIE (dla wdrożenia produkcyjnego).
- **Opis:** podpisy to HMAC-SHA256 z kluczem symetrycznym w pamięci; brak
  podpisów asymetrycznych, chronionego magazynu kluczy, zaufanego czasu
  i szyfrowanego transportu (`security/THREAT_MODEL.md`).
- **Uzasadnienie akceptacji:** wersja 0.x jest implementacją referencyjną,
  nie do danych produkcyjnych; ograniczenie jest jawnie udokumentowane.
- **Warunki ponownego rozpatrzenia:** przed jakimkolwiek wdrożeniem
  przetwarzającym realne dane; wymaga threat modelu wdrożenia.
- **Status:** PROPONOWANE · **Podpis:** ______________ · **Data:** ______

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
- **Status:** PROPONOWANE · **Podpis:** ______________ · **Data:** ______

## AR-004 · Brak produkcyjnego uwierzytelniania i szyfrowania w spoczynku
- **Waga pierwotna:** WYSOKIE (dla wdrożenia produkcyjnego).
- **Opis:** brak auth/authz na poziomie aplikacji i szyfrowania danych
  w spoczynku (README, sekcja „Not production-ready").
- **Uzasadnienie akceptacji:** zakres 0.x; brak przetwarzania danych
  produkcyjnych.
- **Warunki ponownego rozpatrzenia:** etap drugi przeglądu (test
  penetracyjny pełnego wdrożenia) po połączeniu aplikacji/API/logowania.
- **Status:** PROPONOWANE · **Podpis:** ______________ · **Data:** ______

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
- **Status:** PROPONOWANE · **Podpis:** ______________ · **Data:** ______
