# Human OS — aplikacja osobista (demo)

## ⚠ UX-ONLY PROTOTYPE

Ten katalog zawiera **prototyp UX** aplikacji osobistej Human OS —
punkt odniesienia zaimportowany decyzją foundera (DD-005, 2026-08-17)
jako dokładna kopia aktualnie testowanego artefaktu. Obowiązują
wszystkie poniższe zastrzeżenia, bez wyjątków:

- **brak produkcyjnego backendu** — całość działa w przeglądarce,
- **brak produkcyjnego uwierzytelniania** — nie ma kont ani logowania,
- **dane syntetyczne domyślnie** — wszystko, co aplikacja pokazuje,
  pochodzi z lokalnych deklaracji użytkownika lub wartości przykładowych,
- **dane w `localStorage` NIE są trwałym Human OS User Model** — to
  lokalny stan prototypu, bez gwarancji migracji,
- **brak automatycznej promocji danych do Core lub Hub** — nic z tego
  prototypu nie zasila silnika ani rejestrów,
- **żadnych prawdziwych danych użytkownika w repozytorium** — plik
  został przeskanowany przed importem (brak adresów, telefonów,
  poświadczeń).

## Czym ten prototyp JEST, a czym NIE jest

| Artefakt | Rola | Czego dowodzi |
|---|---|---|
| `apps/user-demo/` (ten katalog) | Prototyp UX aplikacji osobistej: onboarding z Kontraktem, zgody warstwowe C0–C4, konwersacyjne „O mnie" (interakcja ≠ model), bramy, tryby awaryjne, eksport | Jak produkt ma **wyglądać i zachowywać się** wobec użytkownika |
| `app/` | Konsola Proof Kernel (Flask) — techniczny podgląd werdyktów konstytucyjnych silnika | Jak **silnik ocenia działania** — narzędzie deweloperskie, nie produkt |
| `hos_engine/` | Silnik referencyjny — jedyna wykonywalna implementacja Konstytucji (Proof Kernel, pętla wykonawcza, Recovery, Self Model…) | Jak zasady są **naprawdę egzekwowane** |

Prototyp **reimplementuje wzorce silnika po stronie klienta** (epistemika
self-modelu, bramy decyzyjne, SAFE MODE) na potrzeby testów UX. To nie
jest integracja z `hos_engine` — zbieżność jest wzorcowa, nie kodowa.
Promocja czegokolwiek stąd do Core/Hub wymaga jawnej bramy promocji
(ADR-LAB-005), nigdy kopiowania.

## Pochodzenie i dokładność kopii

- Źródło: artefakt claude.ai `Human OS`
  (`5556ee08-dd8a-43d8-86a8-920cd8d8de60`), wersja potwierdzona przez
  foundera 2026-08-17 jako aktualnie testowana.
- `index.html` to **treść autorska artefaktu bez modyfikacji**. Z
  opublikowanej strony odcięto wyłącznie elementy wstrzykiwane przez
  claude.ai przy publikacji, niebędące kodem autora: szkielet
  `<!doctype html><html><head>…</head><body>` z runtime'em ramki
  (`frame-runtime` / `__FRAME_PREAMBLE` — obsługa motywów, nawigacji
  i sandboxu podglądu) oraz domykające `</body></html>` tego szkieletu.
  Treść autorska zaczyna się od `<title>Human OS</title>` i jest
  zachowana co do bajta.
- Plik jest samowystarczalny: otwarcie `index.html` w przeglądarce
  uruchamia prototyp (stan w `localStorage` tej przeglądarki).

## Status w architekturze

Zgodnie z ADR-LAB-006 lokalny prototyp jest **etapem UX**, nie
backendem. Warstwa aplikacji nie może obejść żadnej bramy warstw
wyższych (ECOSYSTEM.md) — a ten prototyp nie ma nawet połączenia z
warstwami wyższymi. Decyzje o wydaniu sklepowym (cennik, podział
free/premium, pakowanie, przegląd prawny) są otwarte w DD-011.
