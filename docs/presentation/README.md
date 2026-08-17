# Prezentacje Human OS

W katalogu są dwie niezależne prezentacje, przeznaczone dla różnych odbiorców.
Obie są po polsku i obie generują się deterministycznie ze skryptów — plik
wynikowy edytuje się przez skrypt, nie ręcznie.

| Plik | Format | Slajdów | Dla kogo |
|---|---|---|---|
| `Human-OS-prezentacja-biznesowa.pdf` | PDF | 22 | osoby decyzyjne, partnerzy, zespoły rozważające wdrożenie |
| `Human-OS-prezentacja.pptx` | PowerPoint | 20 | prezentacja mówiona, spotkania, wykłady |

---

## 1. Prezentacja biznesowa (PDF)

`Human-OS-prezentacja-biznesowa.pdf` — dokument przeglądowy pisany prostym
językiem, bez żargonu i bez wewnętrznych identyfikatorów na slajdach. Ma być
czytelny bez prelegenta: numeracja stron, stopka z wersją, jedna myśl na stronę.

**Układ:** streszczenie w jednym akapicie · problem · pomysł (reguły wykonywalne) ·
co z tego ma człowiek · co z tego ma organizacja · jak to działa (widok z góry) ·
trzy kroki drogi żądania · wstrzymanie się · model wiedzy o użytkowniku · tryby
awaryjne · wyjście i przenośność · z czego składa się system · czego nie ma w tym
repozytorium · co działa dzisiaj · czego nie obiecujemy · licencje i zarządzanie ·
droga do 1.0 · dla kogo to jest · zamknięcie.

**Świadome decyzje redakcyjne — nie zmieniaj ich bez powodu:**

- **Brak liczb o świecie zewnętrznym.** Żadnych prognoz rynkowych, danych
  finansowych ani statystyk o użytkownikach — nie ma dla nich podstaw w
  repozytorium. Strony 2 i 3 mówią to wprost.
- **Brak obietnic zgodności prawnej.** Strona o korzyściach dla organizacji
  kończy się zastrzeżeniem, że to nie jest opinia prawna ani deklaracja
  zgodności z regulacją; Human OS dostarcza mechanizmy i dowody, nie certyfikaty.
- **Strona „Czego nie obiecujemy” jest obowiązkowa.** Wymienia brak logowania
  i uprawnień, brak szyfrowania w spoczynku, brak niezależnego audytu, brak
  kalibracji na danych, warstwy bez implementacji i dwa równoległe słowniki pojęć.
  Nie usuwaj jej przy skracaniu — jawność ograniczeń jest wymogiem konstytucyjnym
  (GEN-015).
- **Strona „Czego nie ma w tym repozytorium”** istnieje po to, żeby nikt nie ocenił
  całego przedsięwzięcia po zawartości jednego repozytorium — w żadną ze stron.

### Jak wygenerować PDF

```bash
npm install pptxgenjs                              # jednorazowo, poza repozytorium
node docs/presentation/build_business_deck.js      # -> .pptx (plik pośredni)
soffice --headless --convert-to pdf \
  --outdir docs/presentation \
  docs/presentation/Human-OS-prezentacja-biznesowa.pptx
```

Plik `.pptx` jest artefaktem pośrednim i nie jest wersjonowany — w repozytorium
trzymamy skrypt i gotowy PDF.

---

## 2. Prezentacja narracyjna (PowerPoint)

`Human-OS-prezentacja.pptx` — dwudziestoslajpowa opowieść z łukiem
dramaturgicznym, do prezentowania na żywo. Każdy slajd ma notatki prelegenta.

**Trzy akty:**

- **Akt I — Pytanie:** kto jest autorem twojego dnia · dwie miary sukcesu ·
  obietnica i granice.
- **Akt II — Reguły:** pięć warstw · genom konstytucyjny (15 genów) ·
  Proof Kernel (9 testów, 6 werdyktów).
- **Akt III — Podróż:** jedna intencja przechodzi przez cały system — sześć bram,
  odmowa i zgoda zakresowa, wstrzymanie się przy sprzecznych danych, korekta
  modelu siebie, hamulec awaryjny, suwerenny eksport.
- **Epilog:** czego jeszcze nie ma · gdzie jesteśmy · powrót do pytania z Aktu I.

„Marta” z Aktu III jest **przykładem ilustracyjnym, nie prawdziwym przypadkiem
użytkownika** — slajd otwierający akt mówi to wprost i to zdanie musi tam zostać.
Każdy mechanizm, przez który przechodzi jej intencja, istnieje w kodzie:
`ExecutionLoop` i `IntentOutcome.REFUSED_CONSENT` (`execution_loop.py`),
`APPROVED_WITH_LIMITS` jako status porażki PROOF-003 (`proof.rules.json`),
`AbstentionReason.CONTRADICTORY_EVIDENCE` (`decision_engine.py`),
`reject`/`correct` przez łańcuch „supersedes” (`self_model.py`),
tryby awaryjne i `export_sovereign_package()` (`recovery.py`).

```bash
node docs/presentation/build_presentation.js
```

---

## Wspólne źródła i zasady

Wszystkie liczby i sformułowania pochodzą z repozytorium, stan na 2026-08-17:
`README.md`, `constitution/README.md`, `genome.registry.json`, `proof.rules.json`,
`ECOSYSTEM.md`, `ROADMAP.md`, `GOVERNANCE.md`, `CONTRIBUTING.md`, `SECURITY.md`,
`LICENSE-DECISION.md`, `security/THREAT_MODEL.md`, `hos_engine/` oraz `docs/adr/`.
Liczby (36 modułów, 166 testów, 9 testów zasad, 67 zapisów decyzji) policzono
bezpośrednio z drzewa plików — przy edycji przelicz je, nie przepisuj.

Klasy ryzyka trybów awaryjnych podawaj za mapowaniem z `hos_engine/recovery.py`
(`SAFE_MODE`/`READ_ONLY` = R0, `FREEZE`/`DISCONNECT`/`EXPORT` = R1,
`ROLLBACK` = R2, `RECOVERY` = R3 — żaden tryb nie sięga R4). Drugiego klucza
wymagają wyłącznie `ROLLBACK` i `RECOVERY`.

Obie prezentacje opisują **silnik referencyjny i protokół** z tego repozytorium.
Szersza inicjatywa Human OS (Hub, Atlas, Lab/Forge, White Paper, governance,
warstwy normatywne) wykracza poza to repo — patrz `docs/FOUNDER_REVIEW_2026-08-15.md`.
