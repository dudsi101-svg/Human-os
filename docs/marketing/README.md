# Materiały reklamowe aplikacji Human OS

Zestaw kampanijny dla aplikacji osobistej (`apps/user-demo/`): strategia, teksty
i gotowe grafiki. Wszystko po polsku, wszystko w palecie i typografii samej
aplikacji — reklama ma wyglądać jak produkt, a nie jak osobna marka.

> ## Stan przedpremierowy — przeczytaj przed publikacją
>
> Aplikacja jest **prototypem interfejsu**: działa w przeglądarce, bez konta,
> bez serwera, na danych syntetycznych. Nie ma wydania sklepowego, niezależnego
> audytu bezpieczeństwa ani szyfrowania danych na dysku.
>
> Materiały można dziś używać do prezentowania projektu. **Tekstów sklepowych
> nie wolno opublikować, dopóki aplikacja nie ma faktycznego wydania**, a żadnego
> materiału nie wolno zmienić w sposób łamiący listę z `KOMUNIKACJA.md` §8
> („Czego nie wolno obiecywać”).

## Co jest w katalogu

| Plik | Co to jest |
|---|---|
| `KOMUNIKACJA.md` | księga komunikacji: pozycjonowanie, segmenty, piramida komunikatu, ton głosu, hasła, dowody, obiekcje i **twarda lista zakazów** |
| `TEKSTY.md` | gotowe teksty: opis sklepowy z policzonymi limitami znaków, posty na LinkedIn / X / Instagram, e-mail zapowiadający, scenariusz spotu 30 s, one-liner prasowy |
| `landing.html` | jednoplikowa strona lądowania (samowystarczalna, zrzuty wbudowane jako dane) |
| `landing.template.html` | szablon strony bez zrzutów — tu się edytuje treść |
| `build_assets.js` | generator grafik (Playwright + Chromium) |
| `assets/*.png` | gotowe grafiki kampanijne |
| `assets/ekrany/*.png` | **prawdziwe** zrzuty z działającej aplikacji, źródło dla wszystkich materiałów |

## Grafiki

| Plik | Wymiar | Przeznaczenie |
|---|---|---|
| `kv-og-1200x630.png` | 1200×630 | podgląd linku (Open Graph), nagłówek artykułu |
| `post-01-nie-wiem-1080.png` | 1080×1080 | post: uczciwa abstencja |
| `post-02-wyjscie-1080.png` | 1080×1080 | post: gwarancja konstytucyjna (wersja ciemna) |
| `post-03-model-1080.png` | 1080×1080 | post: trzy klasy zapisów o użytkowniku |
| `story-1080x1920.png` | 1080×1920 | Stories / Reels — prywatność danych |
| `linkedin-1200x627.png` | 1200×627 | post firmowy z liczbami |
| `store-01-pulpit-1290x2796.png` | 1290×2796 | kadr sklepowy 1 — pulpit |
| `store-02-decyzje-1290x2796.png` | 1290×2796 | kadr sklepowy 2 — rekomendacje |
| `store-03-konstytucja-1290x2796.png` | 1290×2796 | kadr sklepowy 3 — prawa (wersja ciemna) |
| `baner-1600x400.png` | 1600×400 | nagłówek strony, newsletter |

Rozmiar 1290×2796 odpowiada kadrom 6,7″ w App Store; do Google Play te same pliki
działają bez zmian.

## Jak to odtworzyć

```bash
npm install playwright                     # jednorazowo, poza repozytorium
node docs/marketing/build_assets.js        # grafiki -> docs/marketing/assets/
```

Strona lądowania powstaje z szablonu przez wstawienie zrzutów jako danych
(base64), żeby plik był w pełni samowystarczalny — bez zewnętrznych zasobów.

Zrzuty w `assets/ekrany/` powstały przez uruchomienie `apps/user-demo/human_os_app.html`
w Chromium, przejście onboardingu i sfotografowanie kolejnych kart. Postać „Ala”
i wszystkie liczby są syntetyczne. **Nigdy nie zastępuj ich zrzutami z prawdziwymi
danymi osób.**

## Zasady, które trzymają ten zestaw razem

1. **Paleta i typografia pochodzą z aplikacji**, nie z osobnego brandbooka:
   pergamin `#F2EFE7`, atrament `#262A21`, szałwia `#5F7F55`, glina `#BC6448`,
   szeryfowe nagłówki, plakietki z interfejsu jako motyw przewodni.
2. **Zrzuty są prawdziwe.** Żadnych makiet i renderów interfejsu, którego nie ma.
3. **Jeden materiał niesie jeden filar** (widzi całość / nie udaje / nie zamyka).
   Nigdy trzy naraz.
4. **Reklama trzyma standard produktu**: bez presji, bez sztucznego niedoboru,
   bez obietnic zdrowotnych, z jawnie napisanym stanem prac.

Punkt 4 nie jest ozdobnikiem — produkt sprzedający autonomię metodami odbierającymi
autonomię traci swój jedyny argument.
