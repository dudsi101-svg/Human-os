# Propozycja kalibracji skal DI / IQ / AR (v0.2 — po odczycie źródła)

> **Aktualizacja 2026-08-17 (v0.2):** founder dostarczył źródłowy DOCX
> Warstwy 5 (`Human_OS_Warstwa_5_Silnik_Decyzji_i_Rekomendacji_v0_1.docx`)
> do tej sesji. Sekcje 5.2, 6.1 i 8.2 zostały odczytane z oryginalnych
> bajtów — wszystkie trzy skale mają teraz **pełną semantykę źródłową**
> i status ŹRÓDŁO. Interpolacje z v0.1 (§7 niżej) są zastąpione.

**Status: PROPOZYCJA — czeka na podpis foundera.**
Nic z tego dokumentu nie jest aktywną konfiguracją. Silnik
(`hos_engine/decision_scales.py`, DD-006) zwraca `CONFIGURATION_REQUIRED`
dla każdej interpretacji, dopóki founder nie zatwierdzi polityki
interpretacji jawnie, z wersją i polem `approved_by`. Ten dokument jest
materiałem do tej decyzji — niczym więcej.

Proces zatwierdzony przez foundera 2026-08-17 („Zatwierdzam kalibrację")
obejmuje przygotowanie propozycji; wartości pozostają decyzją foundera
po kalibracji i walidacji (rozstrzygnięcie DD-006).

---

## 1. Rozwarstwienie epistemiczne tego dokumentu

Zgodnie z zasadą „inferencja nigdy nie udaje faktu", każda pozycja niżej
ma jeden z trzech statusów:

- **ŹRÓDŁO** — semantyka obecna w digescie Warstwy 5
  (`docs/LAYER_5_DECISION_ENGINE_DIGEST.md`), pochodząca z
  `Human_OS_Warstwa_5_...docx`.
- **PROPOZYCJA** — interpolacja lub projekt autorstwa tej propozycji;
  wymaga zatwierdzenia foundera, może być swobodnie odrzucona.
- **BRAK ŹRÓDŁA** — semantyki nie ma ani w digescie, ani w kodzie;
  wypełnienie jej wymaga powrotu do źródłowego DOCX lub decyzji foundera.
  Ta propozycja świadomie **nie zgaduje** takich pozycji.

## 2. Skala IQ — jakość wejścia (IQ0..IQ5)

Pełna semantyka źródłowa (DOCX §5.2, tabela „Poziom / Opis / Dozwolony
wynik", odczyt z bajtów 2026-08-17):

| Poziom | Opis (ŹRÓDŁO) | Dozwolony wynik (ŹRÓDŁO) |
|---|---|---|
| IQ0 | brak istotnych danych albo dane sprzeczne bez możliwości rozstrzygnięcia | wyłącznie pytania, bezpieczeństwo lub eskalacja |
| IQ1 | pojedyncza deklaracja bez kontekstu | ogólna edukacja i niskiego ryzyka sugestie |
| IQ2 | cel i podstawowy kontekst, ale brak bazy lub historii | krótki, odwracalny krok z dużym marginesem |
| IQ3 | spójny profil, kilka źródeł danych i znane ograniczenia | personalizowana rekomendacja średniej złożoności |
| IQ4 | dobry punkt odniesienia, historia odpowiedzi i wiarygodne pomiary | zaawansowana sekwencja i eksperyment N-of-1 |
| IQ5 | zweryfikowany kontekst, specjalista lub wysokiej jakości dane dla decyzji wysokiego wpływu | złożona decyzja z audytem i nadzorem |

**Polityka `HOS-POL-IQ-001` v0.2.0** (reguły = „Dozwolony wynik" ze
źródła; do podpisu, §7):

```
IQ0: "tylko-pytania-bezpieczenstwo-eskalacja"
IQ1: "ogolna-edukacja-i-sugestie-niskiego-ryzyka"
IQ2: "krotki-odwracalny-krok-z-marginesem"
IQ3: "personalizowana-rekomendacja-sredniej-zlozonosci"
IQ4: "zaawansowana-sekwencja-i-eksperyment-n-of-1"
IQ5: "zlozona-decyzja-z-audytem-i-nadzorem"
```

## 3. Skala AR — gotowość (AR0..AR5)

Pełna semantyka źródłowa (DOCX §8.2, tabela „Poziom / Stan / Odpowiedź
systemu"). Zasada ramowa §8.3 pozostaje wiążąca: **„Niewykonanie nie
jest etykietą"** — poziom gotowości opisuje warunki wykonania, nigdy
wartość osoby.

| Poziom | Stan (ŹRÓDŁO) | Odpowiedź systemu (ŹRÓDŁO) |
|---|---|---|
| AR0 | brak zgody lub brak zdolności do bezpiecznej decyzji | wstrzymanie i ewentualna pomoc bezpieczeństwa |
| AR1 | zainteresowanie bez gotowości do działania | edukacja i refleksja, bez protokołu |
| AR2 | gotowość do małego kroku | jedna prosta, odwracalna interwencja |
| AR3 | gotowość do regularnego eksperymentu | protokół, pomiar i przegląd |
| AR4 | wysoka dyscyplina i zdolność monitorowania | złożona sekwencja przy zachowaniu minimalizmu |
| AR5 | zaawansowany użytkownik z odpowiednim nadzorem | kontrolowane działania wysokiej złożoności |

**Polityka `HOS-POL-AR-001` v0.2.0** (do podpisu, §7):

```
AR0: "wstrzymanie-i-pomoc-bezpieczenstwa"
AR1: "edukacja-i-refleksja-bez-protokolu"
AR2: "jedna-prosta-odwracalna-interwencja"
AR3: "protokol-pomiar-i-przeglad"
AR4: "zlozona-sekwencja-przy-minimalizmie"
AR5: "kontrolowane-dzialania-wysokiej-zlozonosci"
```

## 4. Skala DI — klasa intencji (DI-1..DI-8)

**Ścieżka 1 wykonana 2026-08-17**: founder dostarczył źródłowy DOCX;
sekcja 6.1 odczytana z bajtów. Pełna tabela źródłowa („Kod / Intencja /
Odpowiedź domyślna"):

| Kod | Intencja (ŹRÓDŁO) | Odpowiedź domyślna (ŹRÓDŁO) |
|---|---|---|
| DI-1 | zrozumienie | wyjaśnienie pojęcia i niepewności |
| DI-2 | porównanie | warianty z profilami kompromisów |
| DI-3 | wybór następnego kroku | jedna rekomendacja plus alternatywa |
| DI-4 | projekt eksperymentu | hipoteza, protokół, pomiary, kryteria przerwania |
| DI-5 | kontynuacja lub przerwanie | analiza wyniku i aktualizacja decyzji |
| DI-6 | decyzja refleksyjna | pytania i hipotezy do samoweryfikacji |
| DI-7 | działanie regulowane lub wysokiego ryzyka | brama bezpieczeństwa i możliwa eskalacja |
| DI-8 | stan pilny | priorytet bezpieczeństwa i kontakt z właściwą pomocą |

Zasady ramowe źródła pozostają wiążące dla implementacji: intencje
mieszane należy rozdzielić i nazwać konflikt (§6.2 — „zgoda na edukację
nie jest traktowana jak zgoda na spersonalizowane działanie"), a reguła
niezależności (§6.3) mówi wprost: determinacja użytkownika „nie może
podnieść oceny dowodów, usunąć przeciwwskazań ani wymusić stworzenia
procedury, której głównym efektem byłoby zwiększenie ryzyka ciężkiej
szkody".

**Polityka `HOS-POL-DI-001` v0.2.0** (reguły = „Odpowiedź domyślna" ze
źródła; do podpisu, §7):

```
DI-1: "wyjasnienie-pojecia-i-niepewnosci"
DI-2: "warianty-z-profilami-kompromisow"
DI-3: "jedna-rekomendacja-plus-alternatywa"
DI-4: "hipoteza-protokol-pomiary-kryteria-przerwania"
DI-5: "analiza-wyniku-i-aktualizacja-decyzji"
DI-6: "pytania-i-hipotezy-do-samoweryfikacji"
DI-7: "brama-bezpieczenstwa-i-mozliwa-eskalacja"
DI-8: "priorytet-bezpieczenstwa-i-kontakt-z-pomoca"
```

## 5. Plan kalibracji i walidacji (PROPOZYCJA)

Silnik nie ma danych empirycznych — kalibracja startowa może być tylko
ekspercka. Proponowany proces trzyetapowy:

1. **Faza cienia (shadow):** po podpisie polityk 0.1.0 interpretacje są
   zapisywane w zdarzeniach, ale oznaczone `policy_version: 0.1.0`
   i nieużywane do blokowania — zbierany jest korpus pomiarów z polami
   `basis`.
2. **Przegląd:** po zebraniu korpusu (próg ilościowy do decyzji
   foundera) przegląd rozkładu kodów i przypadków spornych; korekta
   semantyk poziomów środkowych.
3. **Zatwierdzenie 1.0:** polityki interpretacji przechodzą na wersję
   operacyjną; od tej pory zmiany wyłącznie przez nową wersję polityki
   (stara nigdy nie jest nadpisywana — pełna historia wersji).

## 6. Co podpisuje founder

Zatwierdzenie tej propozycji oznacza dokładnie:

- [x] semantyki IQ1–IQ4 (tabela §2) — **podpisane 2026-08-17**,
- [x] semantyki AR0–AR5 (tabela §3) — **podpisane 2026-08-17**,
- [x] instancjonowanie `HOS-POL-IQ-001` i `HOS-POL-AR-001` w wersji
      0.1.0 z `approved_by` = founder, w trybie fazy cienia (§5.1) —
      **wykonane: `policies/scale.interpretation.policies.json`**,
- [x] ścieżka uzupełnienia DI: **opcja 1** (odczyt sekcji 6.1 źródłowego
      DOCX Warstwy 5) — czeka na dostarczenie źródła; do tego czasu DI
      pozostaje bez polityki.

**Podpis foundera: 2026-08-17** — zgoda wyrażona wprost w sesji roboczej
(„Masz moją zgodę, podpisuję się"). Polityki IQ/AR działają w fazie
cienia; przejście na tryb operacyjny wymaga osobnej decyzji po
przeglądzie korpusu (§5.2–5.3). Interpretacja DI pozostaje
`CONFIGURATION_REQUIRED` do czasu dostarczenia sekcji 6.1 źródła.

---

## 7. Korekta v0.1 → v0.2 i podpis polityk źródłowych

Polityki v0.1.0 (podpisane 2026-08-17 rano, przed dostępem do źródła)
były interpolacjami. Odczyt źródła pokazał rozbieżności — najistotniejsze:

| Kod | v0.1.0 (interpolacja, podpisana) | v0.2.0 (ŹRÓDŁO) | Różnica |
|---|---|---|---|
| IQ1 | edukacja **bez** rekomendacji | edukacja **i sugestie niskiego ryzyka** | źródło łagodniejsze |
| IQ3 | eksperymenty niskiego ryzyka | personalizowana rekomendacja **średniej** złożoności | źródło szersze |
| IQ4 | decyzje umiarkowane z monitoringiem | zaawansowana sekwencja i eksperyment N-of-1 | źródło szersze |
| AR0 | brak warunków (czas/zasoby) → zmniejsz zakres | **brak zgody lub zdolności** → wstrzymanie i pomoc bezpieczeństwa | źródło surowsze i o czym innym |
| AR1 | mikro-kroki odwracalne | edukacja i refleksja, **bez protokołu** | źródło surowsze |

Wniosek zgodny z etosem projektu: **źródło zastępuje interpolację**.
Wersja v0.1.0 pozostaje w historii konfiguracji jako podpisana, ale
zastąpiona — nigdy nie była użyta do blokowania (faza cienia).

### Do podpisu foundera (v0.2)

- [x] polityki `HOS-POL-IQ-001`, `HOS-POL-AR-001`, `HOS-POL-DI-001`
      w wersji **0.2.0**, z regułami dosłownie ze źródła (§2–§4),
      w trybie fazy cienia — zastępują v0.1.0,
- [x] semantyki poziomów wszystkich trzech skal = brzmienie źródłowe
      (status ŹRÓDŁO; nic do korekty redakcyjnej — to cytaty).

**Podpis foundera: 2026-08-17** — zgoda wyrażona wprost w sesji roboczej
(„Podpisuję"). Wykonane: `policies/scale.interpretation.policies.json`
zaktualizowane (v0.2.0 aktywne w SHADOW dla IQ/AR/DI; v0.1.0 w sekcji
`superseded` z pełnymi regułami i notą o rozbieżnościach). Kalibracja
startowa wszystkich trzech skal jest tym samym **zamknięta**; następny
krok to faza cienia → przegląd korpusu → decyzja o trybie operacyjnym
(§5).
