# Protokół wewnętrznego przeglądu bezpieczeństwa (v1.0)

Podstawa: rozstrzygnięcie DD-008 (2026-08-17) — przeglądy wykonywane
własnymi siłami, według powtarzalnego protokołu. Zamknięcie punktu 0.9
roadmapy wymaga: (1) udokumentowanego przeglądu według tego protokołu,
(2) usunięcia problemów krytycznych i wysokich, (3) zapisu ryzyk
zaakceptowanych przez foundera, (4) testu regresji zabezpieczeń.

**Zapisana granica (DD-008):** przegląd nie jest niezależny od autorów
kodu ani od agentów AI uczestniczących w rozwoju. Każdy raport z tego
protokołu musi powtarzać tę deklarację w nagłówku. Powrót do przeglądu
zewnętrznego pozostaje możliwy bez zmiany protokołu.

---

## 1. Zasady przeglądu

1. **Powtarzalność.** Przegląd wykonuje się od zera według tej listy —
   nie „od ostatniego razu". Każde uruchomienie ma własny raport
   z datą, wersją repo (commit SHA) i wykonawcą.
2. **Świadek pisemny.** Ustalenie bez zapisu nie istnieje. Każda
   pozycja checklisty kończy się jednym z: PASS / FINDING (z wagą) /
   N/A (z uzasadnieniem).
3. **Wagi ustaleń:** KRYTYCZNE (obejście zgody/własności/audytu,
   wykonanie bez uprawnień), WYSOKIE (osłabienie gwarancji bez pełnego
   obejścia), ŚREDNIE (defekt odporności), NISKIE (higiena). KRYTYCZNE
   i WYSOKIE blokują zamknięcie 0.9 do czasu naprawy.
4. **Ryzyko zaakceptowane** to decyzja foundera zapisana w rejestrze
   (sekcja 5) — nigdy domyślna kategoria dla niewygodnych ustaleń.
5. **Dwie perspektywy na pozycję:** „czy mechanizm działa" (test) oraz
   „czy da się go ominąć lub wyłączyć" (próba nadużycia). Pozycja bez
   próby nadużycia nie jest zakończona.

## 2. Zakres komponentów (z decyzji foundera, pkt 5)

Każdy komponent ma pytania kontrolne minimalne — wolno dodawać, nie
wolno pomijać.

### 2.1 Protokół HOSP i podpisy (`protocol_security`, `spec/`)
- Czy `canonical_json` jest deterministyczny (kolejność kluczy, unicode)?
- Czy podpis obejmuje całą kopertę (brak pól poza podpisem)?
- Czy zmiana dowolnego bajta payloadu unieważnia podpis (test tamper)?
- Czy dwie wersje kopert (SDK `HOSP/0.1` vs silnik `HOSP/0.2`) są
  rozróżniane i nie akceptują się nawzajem?
- Ograniczenie HMAC (mechanizm referencyjny) — potwierdzone w docs?

### 2.2 Identity / Authority / Consent (`security_identity`, `authority`, `consent`)
- Czy tożsamość zawieszona/unieważniona faktycznie traci skutki?
- Czy oś roli (OWNER, RECOVERY_CUSTODIAN…) jest sprawdzana niezależnie
  od osi tożsamości (HUMAN, AGENT…) — i nigdy nie zastępowana nią?
- Czy zgoda jest celowa (purpose-bound) i czy odwołanie działa wstecz
  na przyszłe operacje natychmiast?
- Czy brak zgody daje odmowę, nie degradację cichą?

### 2.3 Security Gateway (`security_gateway`)
- Czy 10-krokowa kolejność z `protocol/security-profile.md` jest
  zachowana w kodzie (resolve → verify → key binding → signature →
  expiry/replay → trust → consent → capability → execute → receipt)?
- Czy odmowa na wcześniejszym kroku uniemożliwia dojście do późniejszych?
- Czy każde przejście i odmowa wystawia pokwitowanie?

### 2.4 Replay Guard i wygasanie (`replay_guard`)
- Czy powtórzony nonce/message-id jest odrzucany także po restarcie
  procesu (granice pamięci guarda — udokumentowane)?
- Czy komunikat po `expires_at` jest odrzucany mimo ważnego podpisu?
- Czy zegar jest zależnością jawnie nazwaną (trusted time — ograniczenie)?

### 2.5 Execution Loop (`execution_loop`)
- Czy odmowa na każdej z bram (tożsamość, rola, zgoda, kontekst,
  Proof Kernel, aprobata człowieka) zatrzymuje wszystko dalej —
  test per brama?
- Czy `IntentOutcome.REFUSED_*` nigdy nie jest wyjątkiem połkniętym
  przez wywołującego?
- Czy zdarzenia trafiają na łańcuch hashy przy każdej ścieżce wyjścia?

### 2.6 Recovery Kernel i Emergency Root (`recovery`, `emergency_root`)
- Czy AGENT/SERVICE/SYSTEM_PROCESS ma zero ścieżek aktywacji/deaktywacji
  (w tym przez pośrednie API) i czy odmowa jest logowana?
- Czy tryby konsekwentne wymagają realnie odrębnej tożsamości kustosza?
- Czy nie istnieje żadne API mutujące politykę lub audyt (przegląd
  powierzchni modułu, nie tylko testy)?
- Czy kernel Emergency Root jest niekonstruowalny bez polityki i czy
  żadna wartość domyślna nie wkradła się do kodu (grep za literałami)?
- Czy rollback/eksport zachowują pełną historię (nic nie znika)?

### 2.7 Magazyny zdarzeń i integralność (`event_store`, `sqlite_store`, `replay`)
- Czy `verify_chain()` wykrywa modyfikację, wstawienie i usunięcie
  rekordu (trzy osobne testy manipulacji plikiem)?
- Czy odtworzenie stanu z historii daje stan równoważny (replay test)?
- Czy stara historia (sprzed zmian słownika zdarzeń) czyta się bez błędów?

### 2.8 Granice agentów i delegacji (`agent_runtime`)
- Czy grant capability ogranicza narzędzie, zakres i czas?
- Czy łańcuch delegacji zawęża uprawnienia (nigdy nie rozszerza) —
  test confused deputy?
- Czy brama aprobaty człowieka jest nieobchodzalna dla akcji, które jej
  wymagają?
- Znana luka per-call authorization (threat model) — status w rejestrze
  ryzyk, nie w domyśle.

### 2.9 Aktualność threat modelu (`security/THREAT_MODEL.md`)
- Czy każdy nowy moduł od ostatniego przeglądu ma odzwierciedlenie
  w zagrożeniach i mitygacjach?
- Czy sekcja "Not yet mitigated" zgadza się ze stanem kodu?

## 3. Metoda

Dla każdej pozycji: (a) przeczytaj kod ścieżki, (b) uruchom istniejące
testy pozycji, (c) wykonaj co najmniej jedną próbę nadużycia
(nowy test lub udokumentowana próba ręczna), (d) zapisz wynik.
Narzędzia minimum: `make verify`, przegląd diffów od poprzedniego
przeglądu, grep za nowymi powierzchniami API w modułach bezpieczeństwa.

## 4. Raport — szablon

```
# Przegląd bezpieczeństwa — <data>
Commit: <sha> · Wersja: <x.y.z> · Wykonawca: <kto + które agenty AI>
Deklaracja: przegląd wewnętrzny, nie niezależny od autorów (DD-008).

| Pozycja | Wynik | Waga | Notatka/odnośnik |
|---|---|---|---|
| 2.1 HOSP... | PASS/FINDING/N/A | — | ... |

Ustalenia: <lista z wagami i planem naprawy>
Ryzyka zaakceptowane: <odnośniki do rejestru, sekcja 5>
Regresja zabezpieczeń: <wynik, sekcja 6>
Werdykt: <czy warunki zamknięcia 0.9 spełnione>
```

Raporty składane w `docs/security-reviews/REVIEW_<data>.md`.

## 5. Rejestr ryzyk zaakceptowanych

`docs/security-reviews/ACCEPTED_RISKS.md` — pozycja ma: identyfikator
(AR-001…), opis, wagę pierwotną, uzasadnienie akceptacji, podpis
foundera z datą, warunki ponownego rozpatrzenia. Pozycje startowe do
założenia przy pierwszym przeglądzie: brak niezależności przeglądu
(DD-008), HMAC jako mechanizm referencyjny, brak per-call authorization,
brak produkcyjnego uwierzytelniania i szyfrowania w spoczynku.

## 6. Test regresji zabezpieczeń

Zbiór testów oznaczonych jako regresja zabezpieczeń = wszystkie testy
dotykające pozycji z sekcji 2 (dziś: test_protocol_security,
test_security_gateway, test_replay_guard, test_execution_loop,
test_recovery, test_emergency_root, test_persistence, test_agent_runtime
+ testy manipulacji łańcuchem z 2.7, do dopisania przy pierwszym
przeglądzie). Warunek: 100% zielone na commitcie raportu. Każde
naprawione ustalenie KRYTYCZNE/WYSOKIE musi zostawić test regresyjny.

## 7. Cykl

Pierwszy przegląd: przed zamknięciem 0.9. Kolejne: po każdej zmianie
materialnej w modułach z sekcji 2 albo co 30 dni aktywnego rozwoju —
co nastąpi pierwsze. Drugi etap (test penetracyjny pełnego wdrożenia)
następuje po połączeniu aplikacji, API, logowania i prawdziwych danych —
poza zakresem tego protokołu.
