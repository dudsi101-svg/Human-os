# Deklaracja zamierzonego przeznaczenia — aplikacja osobista Human OS

**Wersja:** 1.0 · 2026-08-17 · przyjęta na polecenie foundera („Tak,
róbmy to") w następstwie wewnętrznej analizy prawnej (aneks w
`docs/LEGAL_REVIEW_PACKAGE.md`). Dokument wiąże treści aplikacji, język
marketingowy i reguły Przewodnika AI; jego zmiana wymaga decyzji foundera.

## 1. Zamierzone przeznaczenie

Aplikacja osobista Human OS jest narzędziem **dobrostanu i samorozwoju**
(wellness/lifestyle): wspiera samoobserwację codziennych nawyków,
wyznaczanie własnych celów, prowadzenie osobistych eksperymentów
nawykowych (N-of-1) o niskim ryzyku oraz refleksję nad własnymi
wartościami i decyzjami. Użytkownik pozostaje autorem swoich decyzji;
aplikacja dostarcza struktury, nie werdyktów.

## 2. Wykluczone przeznaczenia

Aplikacja **nie jest przeznaczona** do żadnego z celów medycznych
w rozumieniu art. 2 pkt 1 rozporządzenia (UE) 2017/745 (MDR), tj. do:

- diagnozowania chorób, urazów lub niepełnosprawności ani wspierania
  diagnozy,
- zapobiegania chorobom, ich monitorowania, przewidywania, prognozowania,
  leczenia lub łagodzenia,
- badania, zastępowania lub modyfikowania procesów fizjologicznych
  w celu medycznym,
- dostarczania informacji wykorzystywanych do podejmowania decyzji
  o przeznaczeniu terapeutycznym lub diagnostycznym.

W konsekwencji aplikacja: nie proponuje leków, suplementów, substancji
ani dawek; nie interpretuje objawów; nie formułuje zaleceń
terapeutycznych; przy sygnałach alarmowych kieruje wyłącznie do lekarza
lub pomocy doraźnej. Samoopisowe wpisy (sen, energia, nastrój) służą
samoobserwacji użytkownika, a mechanizmy przerwania eksperymentu
(HOLD/STOP) są jego własnym protokołem ostrożności — nie monitorowaniem
stanu zdrowia.

## 3. Zobowiązania wynikające z deklaracji

1. **Język produktu i marketingu:** żadnych twierdzeń o pomocy
   w chorobach lub dolegliwościach (także w opisach sklepowych,
   README i materiałach publicznych); dozwolone są sformułowania
   o samoobserwacji, nawykach i dobrostanie.
2. **Przewodnik AI:** reguły systemowe (`AGENT_SYSTEM` w aplikacji)
   muszą utrzymywać zakazy z §2 niezależnie od dostawcy modelu; stały
   dopisek przy interfejsie Przewodnika przypomina, że AI nie jest
   lekarzem.
3. **Nowe funkcje:** każda funkcja dotykająca zdrowia przechodzi test
   względem §2 **przed** implementacją; wątpliwość = pytanie do foundera
   i w razie potrzeby do prawnika.
4. **Przegląd:** deklarację weryfikuje się przy każdym wydaniu
   sklepowym oraz przy każdej zmianie funkcji zdrowotnych.
