# Polityka prywatności — aplikacja osobista Human OS (prototyp)

**Wersja:** 1.0 · 2026-08-17 · dotyczy prototypu publikowanego z tego
repozytorium na GitHub Pages. Ta sama treść jest widoczna w aplikacji
(Ustawienia → „O aplikacji" → Prywatność).

## Zasada podstawowa

Wszystkie dane, które wpisujesz, są przechowywane **wyłącznie lokalnie na
Twoim urządzeniu** (pamięć przeglądarki, `localStorage`). Aplikacja nie ma
serwera, kont, telemetrii ani analityki. Projekt Human OS **nie otrzymuje,
nie przechowuje i nie widzi żadnych Twoich danych** — nie występuje więc
jako administrator Twoich danych osobowych; przetwarzasz je samodzielnie,
na własnym urządzeniu, do własnych celów.

Lokalna pamięć przeglądarki służy wyłącznie działaniu aplikacji, o które
prosisz (zapis Twojego stanu) — jest to przechowywanie ściśle niezbędne do
świadczenia usługi w rozumieniu przepisów o prywatności łączności
elektronicznej; nie ma tu cookies śledzących ani identyfikatorów
reklamowych.

## Trzy wyjątki — zawsze uruchamiane przez Ciebie

1. **Przewodnik AI** (zgoda C5, silnik chmurowy): treść Twojego pytania
   i zminimalizowany pakiet danych (profil „O mnie", cel, wartości domen,
   potwierdzone pozycje modelu, aktywne eksperymenty — nigdy hipotezy,
   rejestr zdarzeń ani dane „Wspólnie") są wysyłane bezpośrednio z Twojej
   przeglądarki do wybranego przez Ciebie dostawcy (Anthropic lub OpenAI),
   **na Twoim własnym kluczu API i Twojej umowie z tym dostawcą**.
   Aplikacja nie pośredniczy w tych wywołaniach. Klucz pozostaje na Twoim
   urządzeniu — poza stanem aplikacji i poza eksportem. Silnik lokalny
   (wbudowane AI przeglądarki) nie wysyła niczego.
2. **Dyktowanie głosowe**: dźwięk może być przetwarzany przez mechanizm
   rozpoznawania mowy Twojej przeglądarki (w zależności od jej dostawcy —
   np. usługi Google przy Chrome). Aplikacja informuje o tym przy
   pierwszym użyciu dyktowania.
3. **„Wspólnie"** (zgoda C4): pakiety współpracy wymieniasz ręcznie i sam
   decydujesz, komu je przekazujesz. Nie ma serwera pośredniczącego.

## Hosting

Aplikację serwuje **GitHub Pages** jako statyczne pliki. Standardowe logi
serwera (np. adresy IP odwiedzających) powstają po stronie GitHub
i podlegają [polityce prywatności GitHub](https://docs.github.com/privacy);
projekt nie ma do nich dostępu.

## Twoje prawa i kontrola

- **Eksport całości danych** — w aplikacji: Konstytucja → „Eksport
  i import"; format otwarty (JSON).
- **Nieodwracalne usunięcie** — Konstytucja → „Pamięć i usunięcie";
  usunięcie danych przeglądarki lub odinstalowanie aplikacji także usuwa
  wszystko.
- **Zgody C1–C5** są rozdzielne i odwoływalne w każdej chwili; odmowa
  niczego nie karze.

## Ograniczenia prototypu

To prototyp badawczy: dane w `localStorage` nie są szyfrowane i mogą
zniknąć wraz z danymi przeglądarki. Bramka wejściowa aplikacji wymaga
potwierdzenia, że **nie wprowadzasz prawdziwych danych zdrowotnych ani
wrażliwych** — traktuj to poważnie.

## Kontakt

Repozytorium projektu: https://github.com/dudsi101-svg/Human-os
(zgłoszenia dot. prywatności/bezpieczeństwa: patrz `SECURITY.md` — kanał
prywatny, nie publiczne issue).
