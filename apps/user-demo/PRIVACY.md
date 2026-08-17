# Polityka prywatności — aplikacja osobista Human OS (prototyp)

**Wersja:** 1.1 · 2026-08-17 · dotyczy prototypu publikowanego z tego
repozytorium na GitHub Pages. Ta sama treść jest widoczna w aplikacji
(Ustawienia → „O aplikacji" → Prywatność). Zmiany względem 1.0: sekcja
„Dane zdrowotne i biometria (zgoda C6)", blokada biometryczna, spójne
brzmienie bramki prototypu.

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

## Dane zdrowotne i biometria (zgoda C6)

Karta „Pomiary ciała" (O mnie) pozwala — **wyłącznie po włączeniu osobnej
zgody C6, domyślnie wyłączonej** — zaimportować plik z eksportu danych
zdrowotnych (Apple Zdrowie XML, CSV, JSON Human OS). Zasady:

- **Rodzaje danych:** kroki, sen, tętno, tętno spoczynkowe, HRV, waga —
  agregowane do wartości dziennych, maksymalnie 366 dni historii.
- **Przetwarzanie wyłącznie lokalne:** plik jest czytany w Twojej
  przeglądarce; nic nie jest nigdzie wysyłane; nie ma serwera.
- **AI nigdy nie widzi tych danych:** pakiet Przewodnika AI (zgoda C5)
  strukturalnie nie zawiera serii pomiarów — niezależnie od silnika
  i dostawcy.
- **Do modelu „O mnie" tylko jawnym aktem:** import niczego sam nie
  zapisuje w Twoim modelu; możesz świadomie zapisać średnią 7 dni jako
  obserwację — z oznaczonym źródłem.
- **Eksport i wymazanie:** serie wchodzą do pełnego eksportu; przycisk
  „Wymaż wszystkie pomiary" usuwa je nieodwracalnie (operacja audytowana).
- **Brak szyfrowania:** `localStorage` nie jest szyfrowany — patrz
  „Ograniczenia prototypu" niżej.
- **Blokada biometryczna** (Face ID / odcisk / PIN, WebAuthn) to **zamek
  na ekran chroniący podgląd — nie szyfrowanie danych**. Identyfikator
  poświadczenia zostaje na urządzeniu, poza stanem aplikacji i eksportem;
  żadne dane biometryczne (odcisk, obraz twarzy) nie są dostępne dla
  aplikacji — weryfikację wykonuje system operacyjny.

**Zalecenie na etap prototypu:** używaj plików testowych lub danych
przybliżonych. Bramka wejściowa prosi o niewprowadzanie prawdziwych danych
zdrowotnych, bo prototyp nie szyfruje pamięci lokalnej. Jeżeli mimo to
świadomie importujesz prawdziwy eksport, dzieje się to wyłącznie lokalnie,
na Twoim urządzeniu i na Twoją odpowiedzialność — a prawo eksportu
i wymazania działa zawsze.

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
- **Zgody C1–C6** są rozdzielne i odwoływalne w każdej chwili; odmowa
  niczego nie karze. Wycofanie C6 blokuje dalszy import; zapisane serie
  pozostają do Twojej dyspozycji (eksport/wymazanie).

## Ograniczenia prototypu

To prototyp badawczy: dane w `localStorage` nie są szyfrowane i mogą
zniknąć wraz z danymi przeglądarki. Bramka wejściowa aplikacji wymaga
potwierdzenia, że **nie wprowadzasz prawdziwych danych zdrowotnych ani
wrażliwych** — traktuj to poważnie. Funkcje przyjmujące dane wrażliwe
(rozmowa „O mnie", formularz, „Pomiary ciała" za zgodą C6) istnieją, by
przetestować mechanikę na danych przybliżonych lub testowych; świadome
użycie prawdziwych danych opisuje sekcja „Dane zdrowotne i biometria".

## Kontakt

Repozytorium projektu: https://github.com/dudsi101-svg/Human-os
(zgłoszenia dot. prywatności/bezpieczeństwa: patrz `SECURITY.md` — kanał
prywatny, nie publiczne issue).
