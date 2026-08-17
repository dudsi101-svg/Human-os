# Roadmap do Human OS Engine 1.0

- [x] 0.1 Formal Core
- [x] 0.2 Machine-Readable Specification
- [x] 0.3 Executable Policy Engine
- [x] 0.4 Persistent and Auditable Core
- [x] 0.5 Knowledge Graph and Provenance
- [x] 0.6 Agent Runtime and Capability Boundaries
- [x] 0.7 Simulation and Scenario Laboratory
- [x] 0.8 Human Model and Consent-Aware Personalization
- [x] 0.9 Protocol Interoperability and Security Review — zamknięte
      2026-08-17 wg kryterium DD-008: przegląd
      `docs/security-reviews/REVIEW_2026-08-17.md` (0 ustaleń
      krytycznych/wysokich), rejestr ryzyk AR-001…AR-005 podpisany przez
      foundera, zestaw regresji zabezpieczeń zielony
- [ ] 1.0 Stable Protocol, Engine and Reference Runtime

## Zrealizowane poza numeracją 0.x (sierpień 2026)

Fazy 3–4 fundamentu wykonawczego oraz pierwsze plastry warstw powstały
równolegle do powyższej osi i nie zamykają punktu 0.9:

- [x] pętla wykonawcza (identity, authority, consent, entity, constitution),
- [x] Decision Engine MVP z twardymi bramami, abstencją i eskalacją,
- [x] Sovereign Recovery Kernel: siedem trybów awaryjnych, dual-key,
      sześć kontraktów Hub,
- [x] konwersacyjny Living Self Model z klasami epistemicznymi
      i persystencją SQLite,
- [x] zerowy dług mypy w silniku,
- [x] kolejka odłożonych decyzji (`docs/DEFERRED_DECISIONS.md`),
- [x] autoryzacja per-wywołanie z kontekstem delegacji (domknięcie luki
      AR-003, `call_authorization.py`),
- [x] skale DI/IQ/AR podpięte do Decision Engine w trybie SHADOW
      (podpisane polityki v0.2.0, strukturalnie bez wpływu na wynik),
- [x] kanoniczny słownik zdarzeń Commons (0.4.0) z podpisanym mapowaniem
      ryzyka wyzwań publicznych na R0–R4 (ADR-COMMONS-003),
- [x] fundament prawny: deklaracja zamierzonego przeznaczenia, polityka
      prywatności, bramka wejściowa prototypu 16+, pakiet do przeglądu
      prawnego z aneksem analizy wewnętrznej.

Żaden z powyższych plastrów nie był podstawą zamknięcia punktu 0.9 —
zamknęło go wyłącznie spełnienie kryterium DD-008 (przegląd
`docs/security-reviews/REVIEW_2026-08-17.md`, podpisany rejestr ryzyk,
zielona regresja zabezpieczeń). Uczciwe zastrzeżenie: był to przegląd
**wewnętrzny według powtarzalnego protokołu**; niezależny przegląd
zewnętrzny pozostaje osobnym warunkiem 1.0 (poniżej) i nie jest
zamknięty.

## Warunki 1.0

- stabilna Konstytucja i Object Model,
- wersjonowany Human OS Protocol,
- migracje i kompatybilność,
- udokumentowany przegląd bezpieczeństwa według powtarzalnego protokołu
  wewnętrznego, z usunięciem problemów krytycznych i wysokich, zapisem
  ryzyk zaakceptowanych przez foundera i testem regresji zabezpieczeń
  (kryterium zmienione decyzją foundera 2026-08-17 — patrz DD-008),
- przegląd governance,
- pełna przenośność danych,
- mierzalna możliwość wyjścia,
- dokumentacja integracji,
- brak krytycznych naruszeń Proof Kernel.
