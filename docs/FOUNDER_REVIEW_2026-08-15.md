# Przegląd założycielski — 15 sierpnia 2026

Status: **Przyjęte**
Źródło: 13 pytań otwartych z sekcji 10 dokumentu *Human OS Reconstruction Audit*
(przygotowanego tego samego dnia na podstawie repozytorium, 77-plikowego
odzyskanego archiwum historycznego oraz tej rozmowy).

Ten dokument zapisuje rozstrzygnięcia founder-a dla każdego z 13 pytań, wraz
z pochodzeniem (numer pytania w audycie) i statusem wdrożenia. Zgodnie z
`Human_OS_Claude_Migration_Package/02_Source_Truth_Protocol`: żadna wcześniejsza
decyzja nie jest tu po cichu nadpisywana — tam, gdzie to rozstrzygnięcie zmienia
coś ustalonego wcześniej (np. kompresję Konstytucji do 15 zasad), stary stan
jest nazwany wprost jako zastąpiony, a nie usunięty z historii.

## Rozstrzygnięcia

### Q1 — Konstytucja: pełna maszyneria czy skrót
**Pytanie:** GitHub ma 15 zasad; źródłowy dokument v0.1 ma 21 rozdziałów i pełną
maszynerię (skale ryzyka R0–R4, antymetryki, rada konstytucyjna, rejestr
precedensów).
**Decyzja:** Pełna maszyneria z `Warstwa_1_Konstytucja_i_Wartości_v0.1` ma
docelowo trafić do wersji wiążącej. 15-punktowa wersja w `constitution/README.md`
przestaje być traktowana jako kompletna — jest punktem wyjścia do rozbudowy, nie
ostateczną formą.
**Status:** Przyjęte jako kierunek. Pełne wdrożenie (przepisanie
`constitution/README.md`) to osobne zadanie, nie wykonane w tej sesji.

### Q2 — Kanoniczny Rozdział I White Paper
**Decyzja:** Rozdziałem I jest długa wersja „Dlaczego Human OS?” (PDF, 12 sekcji).
Krótki esej „Moment, w którym się znaleźliśmy” (Draft/v2 docx) traci status
kandydata na rozdział — jego dalsza rola (np. jako prolog) nie została ustalona.
**Status:** Przyjęte jako rozstrzygnięcie kanonu. Brak zmian w plikach White
Paper w tej sesji.

### Q3 — Rozdział III White Paper: pełna wersja zamiast skrótu
**Decyzja:** Główny plik Rozdziału III ma zostać zastąpiony pełną wersją
czterech części (A–D), zgodnie z własną zasadą projektu, że limit rozmiaru
dzieli dokument, a nie go kompresuje.
**Status:** Przyjęte jako rozstrzygnięcie. Fizyczna podmiana pliku nie wykonana
w tej sesji.

### Q4 — Human Atlas
**Decyzja:** Human Atlas to odrębny, wciąż niezbudowany filar — nie jest
tożsamy z Knowledge Graph.
**Status:** Przyjęte. Nazwa pozostaje zarezerwowana; brak specyfikacji poza
jednym akapitem w Manifeście v0.1.

### Q5 — Priorytet: HOS Hub
**Decyzja:** Budowa Hub (Entity Registry, Relation Registry, Location &
Representation Registry, Orchestrator, Event Ledger, Policy & Permission
Gateway) to bliski priorytet.
**Status:** Rozpoczęte w tej sesji — patrz `docs/adr/` i `hos_engine/hub/`
(jeśli już dodane w tym samym PR).

### Q6 — Kolejność budowy: HOS Core przed Decision Engine i Collective Intelligence
**Decyzja:** Z trzech w pełni opisanych, niezaimplementowanych komponentów
(HOS Core, Silnik Decyzji — Warstwa 5, Inteligencja Zbiorowa — Warstwa 7),
**HOS Core idzie pierwszy** — jako fundament wykonawczy, na którym mają stanąć
pozostałe.
**Status:** Rozpoczęte w tej sesji.

### Q7 — SAFE MODE: ważne, ale nie pierwsze
**Decyzja:** SAFE MODE i Sovereign Recovery Kernel pozostają ważne, ale mają
poczekać na fundamenty wykonawcze (Hub, HOS Core) z Q5/Q6.
**Status:** Świadomie odłożone. Nie blokuje Q5/Q6.

### Q8 — „Relation”: dwa modele, dwie nazwy
**Decyzja:** Zachowujemy oba modele relacji pod różnymi nazwami — ogólną,
typowaną krawędź grafu ze specyfikacji Hub oraz istniejący w repo model relacji
międzyludzkiej (`trust`/`reciprocity`/`boundaries`). Docelowe nazwy do ustalenia
przy implementacji Hub (np. `relation` vs `interpersonal_relation`).
**Status:** Przyjęte jako kierunek nazewniczy. Konkretne nazwy pól — do ADR-HUB
(patrz `docs/adr/`).

### Q9 — Słownik ról tożsamości: wygrywa specyfikacja
**Decyzja:** Ośmiorolowy model z `Identity, Authority & Permissions v0.1`
(OWNER, OPERATOR, TRUSTED_DELEGATE, RECOVERY_CUSTODIAN, AGENT, SERVICE, GUEST,
SYSTEM_PROCESS) zastępuje docelowo pięciotypowy `IdentityType` z
`hos_engine/security_identity.py` (HUMAN, AGENT, APPLICATION, SERVICE, HUB).
**Status:** Przyjęte jako kierunek. Migracja istniejącego kodu (`security_identity.py`)
na nowy słownik ról to osobna, przyszła zmiana — nie wykonana w tej sesji, żeby
nie naruszać działającego, przetestowanego modułu bez wcześniejszego zaplanowania
migracji danych/testów.

### Q10 — Interfejs: konsole i gra turowa równolegle
**Decyzja:** Rodzina konsol/dashboardów (Lab Console, Proof Kernel Console) i
zaproponowana przez founder-a gra turowa (postać = życie użytkownika, tury =
ścieżki rozwoju) rozwijane są równolegle, dla różnych odbiorców — konsole dla
operatora/testera, gra dla użytkownika końcowego.
**Status:** Przyjęte jako kierunek. Brak nowej pracy nad interfejsem w tej sesji
poza tym zapisem.

### Q11 — Import 14 ADR-ów
**Decyzja:** ADR-HUB-001…006 oraz ADR-CORE-001, ADR-GRAPH-002, ADR-AGENT-001/002,
ADR-WORLD-001, ADR-USER-002, ADR-PRED-001, ADR-AUDIT-001, ADR-IMPL-001
importowane do `docs/adr/` teraz, niezależnie od stanu implementacji.
**Status:** Wykonane w tej sesji — patrz `docs/adr/`.

### Q12 — Aktywne poszukiwanie brakujących dokumentów
**Decyzja:** Layer 2 („Model Człowieka”), Layer 4 („Model Użytkownika i Cyfrowy
Profil”), Layer 6 („Silnik Eksperymentów”), Sovereign Recovery Layer i Living
Canon mają być aktywnie poszukiwane, zanim uznamy je za utracone.
**Status:** Otwarte — wymaga dostępu founder-a do źródeł spoza tej sesji
(historia ChatGPT, File Library, inne kopie zapasowe). Nie do wykonania przez
samo repozytorium/to archiwum.

### Q13 — Licencja rozstrzygnięta
**Decyzja:** Robocza rekomendacja z `LICENSE-DECISION.md` przyjęta wprost:
Apache-2.0 dla kodu, CC BY 4.0 dla dokumentacji, polityka znaków — wciąż otwarta.
**Status:** Wykonane w tej sesji — patrz `LICENSE`, `LICENSE-DOCS`,
`LICENSE-DECISION.md`.

## Co z tego wynika dla dalszej pracy

Priorytet budowy w kolejności przyjętej powyżej: **HOS Core → Hub → (SAFE MODE,
Decision Engine, Collective Intelligence — kolejność między nimi nierozstrzygnięta)**.
Q12 wymaga działania founder-a poza tym repozytorium. Q1–Q4, Q8–Q10 są
rozstrzygnięciami kanonu/kierunku, których fizyczne wdrożenie (przepisanie
Konstytucji, podmiana rozdziałów White Paper, migracja słownika ról) pozostaje
do zaplanowania jako osobne zadania.
