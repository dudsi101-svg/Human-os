# Prezentacja Human OS

`Human-OS-prezentacja.pptx` — czternastoslajdowa prezentacja przeglądowa projektu
(język polski), przeznaczona do przedstawienia Human OS osobie, która nie zna
repozytorium.

## Zakres

1. Slajd tytułowy (wydanie 0.9.0, licencje, stos warstw)
2. Czym Human OS jest, a czym nigdy nie będzie
3. Odwrotne kryterium sukcesu (GEN-012)
4. Pięć warstw i kierunek zależności
5. Genom konstytucyjny — 15 genów
6. Proof Kernel — 9 testów, 6 werdyktów
7. Pętla wykonawcza — od intencji do poświadczenia
8. Sovereign Recovery Kernel — 7 trybów awaryjnych
9. Silnik decyzji (Warstwa 5) — bramy przed rankingiem
10. Żywy model siebie — klasy epistemiczne i proweniencja
11. Bezpieczeństwo i jawna deklaracja dojrzałości
12. Stan implementacji w liczbach
13. Roadmapa do 1.0
14. Slajd zamykający

Każdy slajd ma notatki prelegenta (`Widok prelegenta` w PowerPoint).

## Źródła treści

Wszystkie liczby i sformułowania pochodzą z repozytorium, stan na 2026-08-17:
`README.md`, `constitution/README.md`, `genome.registry.json`, `proof.rules.json`,
`ECOSYSTEM.md`, `ROADMAP.md`, `security/THREAT_MODEL.md`, `hos_engine/` oraz
`docs/adr/`. Liczby na slajdzie „Stan implementacji” policzono bezpośrednio
z drzewa plików (moduły, metody testowe, schematy, ADR-y).

Slajd 11 celowo powtarza ostrzeżenie z `README.md` i `security/THREAT_MODEL.md`:
wydanie **nie jest produkcyjne** (brak uwierzytelniania, autoryzacji, szyfrowania
w spoczynku, niezależnego przeglądu bezpieczeństwa i kalibracji empirycznej).
Nie usuwaj tego slajdu przy skracaniu prezentacji — jawność ograniczeń jest
wymogiem konstytucyjnym (GEN-015).

## Ponowne wygenerowanie

Plik `.pptx` jest generowany deterministycznie ze skryptu:

```bash
npm install pptxgenjs          # jednorazowo, poza repozytorium
node docs/presentation/build_presentation.js
```

Edytuj `build_presentation.js`, nie sam `.pptx` — dzięki temu zmiany treści są
widoczne w diffie. Po każdej zmianie liczb sprawdź, czy nadal zgadzają się
z repozytorium.

## Uwaga o zakresie

Prezentacja opisuje **silnik referencyjny i protokół** z tego repozytorium.
Szersza inicjatywa Human OS (Hub, Atlas, Lab/Forge, White Paper, governance,
warstwy normatywne) wykracza poza to repo — patrz `docs/FOUNDER_REVIEW_2026-08-15.md`.
