# Human OS — aplikacja osobista (user demo)

**Status: UX-ONLY PROTOTYPE / prototyp referencyjny.** Ten katalog zawiera
dokładną kopię jednoplikowej aplikacji użytkownika rozwijanej jako artefakt
(dyrektywa DD-005, rozstrzygnięta 2026-08-17: najpierw niezmodyfikowana wersja
obecnie testowanego artefaktu jako punkt odniesienia).

## Oznaczenia obowiązkowe (DD-005)

- **UX-ONLY PROTOTYPE** — to prototyp interfejsu i wzorców produktowych,
  nie wydanie produkcyjne.
- **Brak produkcyjnego backendu i uwierzytelniania.** Aplikacja nie ma
  serwera, kont ani telemetrii.
- **Dane syntetyczne domyślnie.** Żadne prawdziwe dane użytkownika nie
  znajdują się w tym repozytorium i nie mogą do niego trafić.
- **`localStorage` ≠ trwały User Model.** Stan aplikacji żyje wyłącznie
  w pamięci przeglądarki użytkownika; nie jest to implementacja Warstwy 4.
- **Brak automatycznej promocji do Core/Hub.** Wszystko, co aplikacja
  nazywa „modelem", jest lokalnym demem wzorców silnika — nic nie zapisuje
  się do `hos_engine` ani do encji Hub.

## Czym różni się od pozostałych aplikacji w repo

| Warstwa | Co to jest |
|---|---|
| `hos_engine/` | silnik referencyjny (Python) — Proof Kernel, rejestry, pętla wykonawcza |
| `app/` | konsola Proof Kernel (Flask) — cienki klient silnika do oceny encji `action` |
| `apps/user-demo/` | **ten katalog** — jednoplikowy prototyp produktowej aplikacji osobistej (HTML/JS, bez zależności) |

## Uruchomienie

Otwórz `human_os_app.html` w przeglądarce. Bez budowania, bez zależności.

## PWA (przygotowanie do wydania sklepowego, ADR-APP-001 §5)

Katalog jest kompletną aplikacją PWA: `manifest.webmanifest` (standalone,
ikony zwykłe i maskable, po polsku), `sw.js` (offline-first: powłoka
z cache, ciche odświeżenie w tle, wyłącznie własny origin — zero żądań na
zewnątrz) oraz ikony w `icons/`. Rejestracja service workera w
`human_os_app.html` jest osłonięta — aktywuje się tylko przy serwowaniu
przez http/https, więc ten sam plik działa bez zmian jako artefakt
i po otwarciu z dysku.

Test lokalny:

```bash
cd apps/user-demo && python3 -m http.server 8080
# http://localhost:8080/ → instalacja „Dodaj do ekranu głównego”, działa offline
```

Ścieżka sklepowa (kierunek wg ADR-APP-001, finalizacja w DD-011):
hosting statyczny → TWA (Google Play) / cienki wrapper (App Store).
Przy każdej zmianie plików powłoki podbij `CACHE` w `sw.js`.

## Co implementuje (po stronie klienta, jako demo wzorców)

- pulpit równowagi 5 domen i „odprawę dnia",
- żywy model „O mnie" (deklaracja/obserwacja/hipoteza, zgody, napięcia,
  pełna proweniencja `why`, jawne potwierdzanie — wzorce ADR-SELFMODEL-001),
- silnik rekomendacji ze spektrum, uczciwą abstencją i bramami G0–G8
  (wzorce ADR-DECISION-*),
- eksperymenty N-of-1 (do 3 równoległych, baza→próba, HOLD, prognoza zbiorcza),
- moduł „Wspólnie" (ADR-COMMONS-001/002): ekran zgody, kręgi, Karty
  Doświadczeń, wymiana federacyjna pakietami JSON — bez serwera,
- tryby awaryjne (SAFE MODE, READ-ONLY, wymazanie) i pełny rejestr zdarzeń,
- eksport/import całości stanu (prawo wyjścia i powrotu),
- **wersje bezpłatna/Premium** (przygotowanie do dystrybucji sklepowej,
  ADR-APP-001): mechanizm referencyjny — kod aktywacyjny sprawdza wyłącznie
  format, wydanie sklepowe rozliczałoby zakupy przez platformę sklepu.

Granica konstytucyjna wersji płatnej: eksport, import, wymazanie, model
użytkownika i tryby awaryjne **nigdy** nie są funkcją premium (ADR-APP-001).
