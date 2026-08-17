# Pakiet do przeglądu prawnego — aplikacja użytkownika Human OS

**Status:** SZKIC przygotowany 2026-08-17 na polecenie foundera (decyzja
DD-015 wariant (a): przegląd prawny odbywa się **przed jakąkolwiek
promocją linku** do publicznego deployu poza krąg testerów; ryzyko
AR-006 w `docs/security-reviews/ACCEPTED_RISKS.md`).

**Czym ten dokument jest:** inwentarzem stanu faktycznego sporządzonym
przez wykonawców technicznych jako materiał wejściowy dla prawnika.
**Czym nie jest:** poradą prawną ani oceną zgodności — tę może wydać
wyłącznie prawnik.

---

## 1. Przedmiot przeglądu

Aplikacja `apps/user-demo/human_os_app.html` („Human OS — tryb
użytkownika"), publikowana automatycznie na **GitHub Pages** z tego
repozytorium (`.github/workflows/pages.yml`). Charakterystyka:

- pojedynczy plik HTML/JS (PWA z service workerem), **bez backendu,
  bez kont, bez logowania**;
- wszystkie dane użytkownika wyłącznie w `localStorage` przeglądarki
  użytkownika — repozytorium i serwer Pages nie przechowują żadnych
  danych osób;
- status: **prototyp badawczy** (UX-ONLY, DD-005), oznaczony w aplikacji
  twardą bramką wejściową („PROTOTYP — nie wprowadzaj prawdziwych danych
  zdrowotnych ani wrażliwych", wymagane potwierdzenie, zdarzenie
  `PROTOTYP_ACK` w lokalnym rejestrze) oraz zastrzeżeniem zdrowotnym
  w ustawieniach;
- licencje: kod Apache-2.0, dokumentacja CC BY 4.0; polityka znaku
  „Human OS" w `LICENSE-DECISION.md` (jawnie nie-formalna opinia).

## 2. Inwentarz danych, które użytkownik może wpisać

Wszystkie poniższe kategorie żyją wyłącznie lokalnie w przeglądarce,
chyba że zaznaczono inaczej:

| Kategoria | Przykład | Wrażliwość |
|---|---|---|
| Pseudonim/imię zwracania się | „Aleks" | niska |
| Samooceny domen życia (suwaki 10–90) | zdrowie, relacje, sprawczość | średnia |
| Cele i horyzonty | „stabilna energia, 30 dni" | średnia |
| Codzienne check-iny | sen, energia, wykonanie kroku | **zdrowotna (samoopis)** |
| Rozmowy „O mnie" (tekst i głos) | swobodne wypowiedzi o sobie | **potencjalnie wysoka** |
| Rekordy modelu siebie | deklaracje/hipotezy/napięcia | **potencjalnie wysoka** |
| Eksperymenty N-of-1 | hipoteza zdrowotna + protokół | **zdrowotna (samoopis)** |
| Wkład „Wspólnie" (C4) | pseudonim + wykonanie kroku, pakiety wymieniane ręcznie | średnia |
| Klucz API dostawcy AI (C5) | klucz OpenAI/Anthropic użytkownika | wysoka (sekret) |
| Dyktowanie głosowe | dźwięk przetwarzany przez mechanizm przeglądarki | zależna od treści |

## 3. Przepływy danych poza urządzenie użytkownika

1. **Przewodnik AI (zgoda C5, opt-in):** treść rozmowy wysyłana do
   `api.openai.com` lub `api.anthropic.com` **na kluczu własnym
   użytkownika**, wprowadzonym przez niego świadomie; projekt nie
   pośredniczy, nie przechowuje i nie widzi tych wywołań (brak backendu).
2. **Rozpoznawanie mowy:** Web Speech API — w zależności od przeglądarki
   dźwięk może być przetwarzany przez dostawcę przeglądarki; aplikacja
   informuje o tym przy pierwszym użyciu (zdarzenie w rejestrze).
3. **Hosting:** GitHub Pages serwuje statyczne pliki; standardowe logi
   serwera (adresy IP) są po stronie GitHub, poza kontrolą projektu.
4. **Nic więcej:** brak analityki, brak cookies stron trzecich, brak
   trackerów, brak własnego serwera.

## 4. Istniejące zabezpieczenia i oznaczenia

- twarda bramka wejściowa (potwierdzenie „bez prawdziwych danych
  zdrowotnych") — nie do pominięcia;
- warstwowy model zgód C0–C5, każda osobno odwoływalna, odmowa nie karze;
- eksport całości danych i prawo wyjścia (niepaywallowane, ADR-APP-001);
- zastrzeżenie zdrowotne i informacja o wersji/prototypie w ustawieniach;
- zasada „żadnych prawdziwych danych użytkownika w repozytorium" (DD-005).

## 5. Pytania do prawnika

1. **RODO — role:** czy przy architekturze bez backendu projekt w ogóle
   występuje jako administrator lub podmiot przetwarzający? Jak ocenić
   wywołania API na kluczu własnym użytkownika (rola dostawców API,
   rola projektu jako dostawcy oprogramowania)?
2. **RODO — dane szczególne:** samoopisowe dane o zdrowiu/śnie/energii
   w `localStorage` — czy potrzebna jest polityka prywatności mimo braku
   przetwarzania po stronie projektu, i w jakim kształcie?
3. **Wyrób medyczny (MDR) / software as medical device:** czy funkcje
   (check-iny zdrowotne, eksperymenty N-of-1, rekomendacje z bramkami)
   mieszczą się w kategorii wellness, czy któraś przekracza granicę
   wyrobu medycznego? Czy obecne zastrzeżenia wystarczą?
4. **Małoletni:** brak weryfikacji wieku — czy dla prototypu z bramką
   ostrzegawczą to akceptowalne; co przy wydaniu sklepowym?
5. **Regulaminy dostawców API:** czy schemat BYO-key (użytkownik używa
   własnego klucza OpenAI/Anthropic w aplikacji strony trzeciej) jest
   zgodny z warunkami tych usług, w tym dla treści zdrowotnych?
6. **ePrivacy / cookies:** czy `localStorage` w tym użyciu wymaga zgody
   lub informacji cookie-podobnej?
7. **Konsument / przyszły freemium:** model ADR-APP-001 (eksport, wyjście,
   model, tryby awaryjne nigdy niepaywallowane) — wymagania przy
   przyszłym wydaniu sklepowym (Google Play/App Store), w tym prawo
   odstąpienia i komunikacja „prototyp → produkt".
8. **Odpowiedzialność:** adekwatność wyłączeń odpowiedzialności dla
   oprogramowania badawczego udostępnionego publicznie (Apache-2.0 §7–8
   a komunikaty w aplikacji po polsku).
9. **Znak „Human OS":** czy roboczą politykę znaku (`LICENSE-DECISION.md`)
   należy sformalizować przed promocją publiczną.

## 6. Materiały źródłowe dla prawnika

- `apps/user-demo/README.md` (oznaczenia prototypu), sama aplikacja;
- `docs/security-reviews/ACCEPTED_RISKS.md` (AR-001…AR-006, podpisy);
- `docs/DEFERRED_DECISIONS.md` (DD-005, DD-012, DD-013, DD-015);
- `security/THREAT_MODEL.md`, `SECURITY.md`;
- `LICENSE`, `LICENSE-DOCS`, `LICENSE-DECISION.md`;
- ADR-APP-001 (freemium i granice paywalla), ADR-COMMONS-001/002
  (moduł „Wspólnie"), ADR-APP-002/003 (Przewodnik AI).

## 7. Ograniczenia tego pakietu

Inwentarz sporządzono na stan repozytorium z 2026-08-17; aplikacja jest
aktywnie rozwijana (kilkadziesiąt commitów dziennie), więc przegląd
prawny powinien wskazać, które zmiany wymagają ponownej konsultacji.
Autorzy pakietu nie są prawnikami; pominięcia są niezamierzone, ale
możliwe — pakiet ma zaczynać rozmowę z prawnikiem, nie ją zastępować.

---

# Aneks A — wewnętrzna analiza prawna (AI, 2026-08-17)

**Charakter:** analiza wewnętrzna sporządzona przez AI na polecenie
foundera, w konwencji przeglądów wewnętrznych projektu (jak AR-001 dla
bezpieczeństwa: brak niezależności jest jawnie zadeklarowany). **Nie jest
poradą prawną i nie zastępuje kancelarii** — przy wydaniu sklepowym lub
przed szeroką promocją pytania 1–9 powinny trafić do prawnika wraz z tym
aneksem jako materiałem wejściowym.

Skrót odpowiedzi (pełna treść w zapisie sesji roboczej 2026-08-17):

1. **Role RODO:** przy architekturze bez backendu projekt najpewniej nie
   jest administratorem danych użytkowników (przetwarzanie lokalne, użytek
   osobisty — art. 2 ust. 2 lit. c RODO; dostarczanie oprogramowania to
   nie przetwarzanie). Szare strefy: logi GitHub Pages (wskazać GitHub
   w informacji o prywatności) i wywołania API na kluczu własnym
   (umowa użytkownik–dostawca, projekt nie jest stroną).
2. **Polityka prywatności:** formalnie niewymagana, praktycznie konieczna
   — wdrożona (`apps/user-demo/PRIVACY.md` + karta w aplikacji).
3. **MDR:** obecne funkcje po stronie wellness (MDCG 2019-11); granicy
   pilnują: deklaracja przeznaczenia (`docs/INTENDED_PURPOSE.md`), zakazy
   w regułach Przewodnika, dyscyplina języka marketingowego. Najwyższe
   ryzyko regulacyjne z całej listy — mitygacje wdrożone.
4. **Małoletni:** art. 8 RODO wprost nie obciąża (brak roli
   administratora); dopisek „16+" dodany do bramki; klasyfikacja wiekowa
   wróci przy sklepach.
5. **BYO-key:** wzorzec co do zasady dopuszczalny (użytkownik korzysta
   z własnego API); pilnować polityk użycia dostawców dla treści
   zdrowotnych (ujawnienie AI — wdrożone dopiskiem) i ponawiać przegląd
   przy każdym wydaniu (najbardziej zmienny punkt).
6. **ePrivacy/localStorage:** wyjątek „ściśle niezbędne do usługi
   zażądanej przez użytkownika" — baner zbędny; odnotowane w polityce.
7. **Konsument/freemium:** obowiązki aktywują się przy sklepie
   (dyrektywa 2019/770, odstąpienie, Omnibus); zasadę niepaywallowanej
   suwerenności z ADR-APP-001 wpisać wtedy do regulaminu.
8. **Odpowiedzialność:** Apache-2.0 §7–8 nie wyłączy odpowiedzialności
   konsumenckiej; przy darmowym prototypie ekspozycja niska dzięki
   bramce i polskim zastrzeżeniom przed użyciem; regulamin konieczny
   dopiero przy płatnościach/backendzie.
9. **Znak:** przed promocją marki badanie czystości, potem ewentualna
   rejestracja słowna (UPRP/EUIPO, kl. 9 i 42; bez klasy medycznej —
   spójnie z pkt 3); opisowość może wymusić znak słowno-graficzny.

**Wdrożone mitygacje (2026-08-17):** deklaracja zamierzonego
przeznaczenia; polityka prywatności (plik + karta w aplikacji z trzema
wyjątkami); dopisek wiekowy 16+ w bramce wejściowej; stały dopisek
„AI, nie lekarz" w interfejsie Przewodnika.
