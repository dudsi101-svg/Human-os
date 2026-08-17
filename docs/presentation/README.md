# Prezentacja Human OS

`Human-OS-prezentacja.pptx` — dwudziestoslajdowa prezentacja narracyjna (język polski),
przeznaczona do przedstawienia Human OS osobie, która nie zna repozytorium.
To opowieść z łukiem dramaturgicznym, nie katalog funkcji: pytanie → stawka →
reguły → jedna intencja prześledzona od początku do końca → uczciwy epilog.

## Struktura

**Akt I — Pytanie** (slajdy 2–5)
Kto jest autorem twojego dnia · Dwie miary sukcesu (typowa metryka vs. GEN-012) ·
Obietnica i granice.

**Akt II — Reguły** (slajdy 6–9)
Pięć warstw i kierunek zależności · Genom konstytucyjny (15 genów) ·
Proof Kernel (9 testów, 6 werdyktów).

**Akt III — Podróż** (slajdy 10–17)
Jedna intencja przechodzi przez cały system: intencja → sześć bram → odmowa
i zgoda zakresowa → abstencja przy sprzecznych danych → korekta modelu siebie →
hamulec awaryjny → suwerenny eksport.

**Epilog** (slajdy 18–20)
Czego jeszcze nie ma · Gdzie jesteśmy dzisiaj (liczby + roadmapa) · Klamra:
powrót do pytania otwierającego.

Każdy slajd ma notatki prelegenta (`Widok prelegenta` w PowerPoint).

## O bohaterce

„Marta” z Aktu III jest **przykładem ilustracyjnym, nie prawdziwym przypadkiem
użytkownika** — slajd otwierający akt mówi to wprost i to zdanie musi tam zostać.
Każdy mechanizm, przez który przechodzi jej intencja, istnieje w kodzie:
`ExecutionLoop` i `IntentOutcome.REFUSED_CONSENT` (`execution_loop.py`),
`APPROVED_WITH_LIMITS` jako status porażki PROOF-003 (`proof.rules.json`),
`AbstentionReason.CONTRADICTORY_EVIDENCE` (`decision_engine.py`),
`reject`/`correct` przez łańcuch „supersedes” (`self_model.py`),
tryby awaryjne i `export_sovereign_package()` (`recovery.py`).

## Źródła treści

Wszystkie liczby i sformułowania pochodzą z repozytorium, stan na 2026-08-17:
`README.md`, `constitution/README.md`, `genome.registry.json`, `proof.rules.json`,
`ECOSYSTEM.md`, `ROADMAP.md`, `security/THREAT_MODEL.md`, `hos_engine/` oraz
`docs/adr/`. Liczby na slajdzie „Gdzie jesteśmy dzisiaj” policzono bezpośrednio
z drzewa plików (moduły, metody testowe, ADR-y).

Slajd „Hamulec, którego nie da się zabrać” podaje klasy ryzyka za mapowaniem
z `hos_engine/recovery.py` (`SAFE_MODE`/`READ_ONLY` = R0, `FREEZE`/`DISCONNECT`/
`EXPORT` = R1, `ROLLBACK` = R2, `RECOVERY` = R3 — żaden tryb nie sięga R4).
Przy edycji sprawdź to mapowanie w kodzie, a nie w pamięci.

Slajd „Czego jeszcze nie ma” celowo powtarza ostrzeżenie z `README.md`
i `security/THREAT_MODEL.md`: wydanie **nie jest produkcyjne** (brak
uwierzytelniania, autoryzacji, szyfrowania w spoczynku, niezależnego przeglądu
bezpieczeństwa i kalibracji empirycznej). Nie usuwaj tego slajdu przy skracaniu
prezentacji — jawność ograniczeń jest wymogiem konstytucyjnym (GEN-015), a w tej
opowieści pełni też rolę dramaturgiczną.

Prezentacja nie zawiera żadnych statystyk o świecie zewnętrznym — świadomie,
bo nie dałoby się ich zweryfikować w repozytorium.

## Ponowne wygenerowanie

Plik `.pptx` jest generowany deterministycznie ze skryptu:

```bash
npm install pptxgenjs          # jednorazowo, poza repozytorium
node docs/presentation/build_presentation.js
```

Edytuj `build_presentation.js`, nie sam `.pptx` — dzięki temu zmiany treści są
widoczne w diffie.

## Uwaga o zakresie

Prezentacja opisuje **silnik referencyjny i protokół** z tego repozytorium.
Szersza inicjatywa Human OS (Hub, Atlas, Lab/Forge, White Paper, governance,
warstwy normatywne) wykracza poza to repo — patrz `docs/FOUNDER_REVIEW_2026-08-15.md`.
