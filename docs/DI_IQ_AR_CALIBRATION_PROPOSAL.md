# Propozycja kalibracji skal DI / IQ / AR (v0.1)

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

Skraje są zdefiniowane w źródle (digest, §5.2, linie 513–545 źródła):

| Poziom | Semantyka | Status |
|---|---|---|
| IQ0 | Brak istotnych danych lub dane sprzeczne → wyłącznie pytania, bezpieczeństwo lub eskalacja | **ŹRÓDŁO** |
| IQ1 | Pojedyncze, niezweryfikowane deklaracje; kontekst szczątkowy → proste pytania doprecyzowujące, edukacja, bez rekomendacji działania | PROPOZYCJA |
| IQ2 | Spójne deklaracje bez weryfikacji; podstawowy kontekst → rekomendacje niskiego ryzyka z zastrzeżeniem niepewności | PROPOZYCJA |
| IQ3 | Deklaracje + częściowe dane pomiarowe (samoopis w czasie); brak sprzeczności → proste decyzje i eksperymenty osobiste niskiego ryzyka | PROPOZYCJA |
| IQ4 | Dane wielokrotne, spójne, częściowo zweryfikowane → decyzje umiarkowanego ryzyka z monitorowaniem | PROPOZYCJA |
| IQ5 | Zweryfikowany kontekst, specjalista lub dane wysokiej jakości → złożona decyzja z audytem i nadzorem | **ŹRÓDŁO** |

**Szkic polityki interpretacji IQ** (do instancjonowania jako
`InterpretationPolicy` po podpisie):

```
policy_id: HOS-POL-IQ-001
version:   0.1.0-proposal          # po podpisie: 0.1.0, approved_by: <founder>
scale:     IQ
rules:
  IQ0: "tylko-pytania-lub-eskalacja"
  IQ1: "edukacja-bez-rekomendacji"        # PROPOZYCJA
  IQ2: "rekomendacje-niskiego-ryzyka"     # PROPOZYCJA
  IQ3: "eksperymenty-niskiego-ryzyka"     # PROPOZYCJA
  IQ4: "decyzje-umiarkowane-z-monitoringiem"  # PROPOZYCJA
  IQ5: "zlozona-decyzja-z-audytem"
```

## 3. Skala AR — gotowość (AR0..AR5)

Źródło definiuje tytuł sekcji (§8.2 „Gotowość AR0–AR5") i zasadę
ramową §8.3: **„Niewykonanie nie jest etykietą"** — poziom gotowości
opisuje warunki wykonania, nigdy wartość osoby (ŹRÓDŁO). Pełna semantyka
poziomów nie jest obecna w digescie.

| Poziom | Semantyka | Status |
|---|---|---|
| AR0 | Brak warunków wykonania (czas/zasoby/stan) → nie rekomendować działania; zaproponować zmniejszenie zakresu | PROPOZYCJA |
| AR1 | Warunki szczątkowe → wyłącznie mikro-kroki odwracalne | PROPOZYCJA |
| AR2 | Warunki częściowe, niestabilne → działania krótkiego horyzontu z łatwym przerwaniem | PROPOZYCJA |
| AR3 | Warunki wystarczające dla prostych protokołów → standardowe eksperymenty osobiste | PROPOZYCJA |
| AR4 | Warunki stabilne + doświadczenie wykonawcze → protokoły wieloetapowe | PROPOZYCJA |
| AR5 | Pełna gotowość (zasoby, kompetencje, wsparcie) → protokoły złożone, w tym wymagające nadzoru | PROPOZYCJA |

**Szkic polityki interpretacji AR** — analogiczny kształt jak IQ
(`HOS-POL-AR-001`, `0.1.0-proposal`); mapowanie kodów na nazwy klas
działań powyżej.

## 4. Skala DI — klasa intencji (DI-1..DI-8): BRAK ŹRÓDŁA

Digest potwierdza istnienie ośmiu klas (§6.1) oraz dwóch zasad ramowych:
intencje mieszane są dopuszczalne (§6.2), a system ma rozpoznawać
„presję na potwierdzenie" (§6.3) — ale **nie zawiera nazw ani definicji
poszczególnych klas DI-1..DI-8**.

Ta propozycja świadomie nie wymyśla ośmiu klas intencji. Wypełnienie
tej tabeli wymaga jednego z dwóch kroków (decyzja foundera):

1. dostarczenie/odczyt sekcji 6.1 źródłowego DOCX Warstwy 5 i digest
   uzupełniający (preferowane — zachowuje wierność źródłu), albo
2. autorska definicja ośmiu klas przez foundera jako nowa decyzja
   projektowa.

Do tego czasu pomiary na skali DI są możliwe (kody istnieją w
strukturze), ale żadna polityka interpretacji DI nie powinna być
zatwierdzana.

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
