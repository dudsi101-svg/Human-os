# Changelog

Wersja techniczna (pyproject) i zapis dokumentacyjny są rozdzielone:
`0.10.0a1` (PEP 440) = `0.10.0-alpha.1` (dokumentacja). Numeracja wydań
jest niezależna od osi roadmapy 0.9 → 1.0 — wersja 1.0 pozostaje
zarezerwowana dla systemu stabilnego, przejrzanego i wdrażalnego
(decyzja foundera, 2026-08-17).

## Niewydane (po 0.10.0-alpha.1)

Zmiany zmergowane do `main` po tagu 0.10.0-alpha.1 (wszystkie 2026-08-17,
PR #48 i #50):

### Silnik
- **Autoryzacja per-wywołanie** (`call_authorization.py`): deklaratywne
  reguły per-capability (klucze/wartości/rozmiar argumentów, kontekst
  delegacji) egzekwowane w `AgentRuntime.evaluate`; postawa wobec
  capability bez reguły deklarowana jawnie (ALLOW/DENY, bez domyślnej).
  Domyka lukę AR-003.
- **Skale DI/IQ/AR w trybie SHADOW**: `DecisionRequest.measurements` →
  `DecisionOutcome.shadow_interpretations`; interpretacje pod podpisanymi
  politykami v0.2.0 liczone po pełnym obliczeniu decyzji (strukturalnie
  bez wpływu na wynik); `load_policies_json()`.
- **Słownik zdarzeń 0.4.0**: 14 kanonicznych typów Commons
  (ADR-COMMONS-003); zgody źródła mapują się na istniejące
  `CONSENT_GRANTED/REVOKED`; podpisane mapowanie ryzyka wyzwań
  publicznych na R0–R4 (`policies/commons.challenge.risk.json`).

### Aplikacja użytkownika
- Twarda bramka wejściowa prototypu (16+, „bez prawdziwych danych
  zdrowotnych", zdarzenie `PROTOTYP_ACK`).
- Pełna karta prywatności (trzy wyjątki uruchamiane przez użytkownika)
  + `PRIVACY.md`; stały dopisek „AI, nie lekarz" przy Przewodniku.

### Governance i bezpieczeństwo
- DD-015 rozstrzygnięte (wariant a), AR-006 podpisane, DD-009 cz. 1
  wdrożona i mapowanie podpisane; U-001 rozwiązane (threat model
  o mechanizmy suwerenności/odzyskiwania); `docs/INTENDED_PURPOSE.md`;
  `docs/LEGAL_REVIEW_PACKAGE.md` z aneksem analizy wewnętrznej.

## 0.10.0-alpha.1 — Execution Foundation and Sovereign Recovery (2026-08-17)

Status dojrzałości: **ALPHA / implementacja referencyjna** (obniżony
z „BETA" decyzją foundera — statusy komponentów w `manifest.json`
pozostają osobnym wymiarem).

### Silnik — nowe moduły

- **Fundament wykonawczy**: `hos_core` (niemutowalne snapshoty kontekstu,
  minimalny kontrakt wykonania), `authority` (role władzy jako osobna oś
  od tożsamości), `hub_entity_registry` (rejestry encji i relacji Hub,
  scalanie wyłącznie atrybuowane, nic nie jest kasowane),
  `execution_loop` (pełna pętla intencji z odmową jako pełnoprawnym
  wynikiem na każdej bramie).
- **Suwerenny Kernel Odzyskiwania** (`recovery`): siedem trybów
  awaryjnych zmapowanych na R0–R4, rozdział auto/manual, suwerenność
  dwukluczowa, wszystkie sześć kontraktów Hub (freeze, snapshot,
  rollback z provenance, disconnect, suwerenny eksport, rejestr
  zdarzeń); brak API do mutacji polityki i audytu.
- **Silnik Decyzji MVP** (`decision_engine`): dziewięć bram twardych
  G0–G8 przed rankingiem (niekomutowalne), asymetria dowodowa,
  abstencja i eskalacja jako wyniki pierwszej klasy.
- **Living Self Model** (`self_model`, `self_model_store`):
  konwersacyjny model siebie na epistemice `human_model`
  (deklaracja/obserwacja/hipoteza, potwierdzenia tylko od użytkownika,
  napięcia jako sygnał, pełna provenance, pasma pewności zamiast liczb),
  z persystencją SQLite; `hub_store` dla rejestrów Hub.
- **Szkielety skal DI/IQ/AR** (`decision_scales`, DD-006): struktura,
  pomiar i polityka interpretacji rozdzielone; zero progów i wartości
  domyślnych — brak konfiguracji daje `CONFIGURATION_REQUIRED`.
- **Szkielet Emergency Root** (`emergency_root`, DD-007): wersjonowana
  polityka k-z-n bez żadnych domyślnych wartości, deskryptory kluczy bez
  materiału kryptograficznego, pełny append-only audyt; brak konfiguracji
  blokuje mechanizm strukturalnie.

### Kanon i schematy

- Słownik zdarzeń 0.3.0: kanoniczne typy `RECOVERY_ACTIVATED`,
  `RECOVERY_DEACTIVATED`, `RECOVERY_REFUSED`, `ENTITY_FROZEN` (DD-003);
  historia `STATE_OBSERVED` pozostaje czytelna, nic nie jest
  przepisywane.
- Wzorzec `HOSId` rozszerzony o segment szesnastkowy (DD-010, opcja a);
  pełna walidacja koperty zdarzenia włączona i testowana; koperta
  Recovery poprawiona (`subject_ids` wyłącznie z realnymi ID encji).
- `SchemaRegistry` rozwiązuje referencje między schematami względem
  deklarowanego `$id` — walidacja krzyżowa działa offline.

### Konstytucja, dokumentacja, governance

- Konstytucja rozszerzona z 15 punktów do 21 rozdziałów + 4 załączników
  (wersja 0.2 rozszerzona), z mapowaniem starej wersji.
- Ponad 70 rekordów ADR z indeksem (`docs/adr/README.md`), w tym import
  i weryfikacja źródeł warstw 2–6, Recovery, Lab, Commons.
- Kolejka odłożonych decyzji (`docs/DEFERRED_DECISIONS.md`) —
  DD-001…DD-008 i DD-010 rozstrzygnięte przez foundera z zapisem daty
  i skutku; DD-009 i DD-011 otwarte.
- Kryterium zamknięcia punktu 0.9 zmienione (DD-008): udokumentowany
  przegląd wewnętrzny wg powtarzalnego protokołu + zapis ryzyk
  zaakceptowanych + test regresji zabezpieczeń.
- Kontrakty I/O: `docs/self-model-contract.md`, `docs/recovery-contract.md`
  (z tabelą mapowania zdarzeń i sekcją Emergency Root),
  `docs/runtime-contract.md`, `docs/simulation-contract.md`.
- Propozycja kalibracji skal DI/IQ/AR do podpisu foundera
  (`docs/DI_IQ_AR_CALIBRATION_PROPOSAL.md`).
- Threat model rozszerzony o zagrożenia agentowe/AI (goal hijack,
  zatruwanie pamięci i grafu wiedzy, luka autoryzacji per-wywołanie).
- Decyzja licencyjna przyjęta: kod Apache-2.0, dokumentacja CC BY 4.0,
  robocza polityka znaków „Human OS".
- Rozdział III White Paper w komplecie; digest modułu Wspólnie
  (Commons); konsola Proof Kernel (Flask, `app/`).

### Jakość

- Testy: 28 → 180 (wszystkie zielone, 3 wersje Pythona w CI).
- `mypy hos_engine`: zero błędów, wymuszane bramką CI (DD-001).
- `pip install -e ".[dev]"` i `ruff check .` naprawione i czyste.

## 0.9.0 — Protocol, Identity and Security (2026-08-15)

Wydanie bazowe tego changelogu: schematy obiektów, wykonywalny Proof
Kernel, maszyna stanów, persystencja zdarzeń (JSONL + SQLite z łańcuchem
SHA-256), odtwarzanie stanu, graf wiedzy z provenance, runtime agentów
ograniczony capability z bramami aprobaty człowieka, symulacje
z Monte Carlo, podpisane koperty HOSP, rejestr tożsamości i kluczy,
ochrona przed replay, polityki zaufania, bramka bezpieczeństwa, CI.
