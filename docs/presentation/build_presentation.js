/**
 * Generator prezentacji "Human OS — opowieść o autorstwie własnego życia".
 *
 * Uruchomienie:  node docs/presentation/build_presentation.js
 * Wynik:         docs/presentation/Human-OS-prezentacja.pptx
 *
 * Struktura: trzy akty (Pytanie → Reguły → Podróż) plus epilog.
 * Bohaterka „Marta” jest przykładem ilustracyjnym, nie prawdziwym przypadkiem;
 * każdy mechanizm w jej historii istnieje w kodzie i jest opisany w ADR.
 *
 * Źródła treści: README.md, constitution/README.md, genome.registry.json,
 * proof.rules.json, ECOSYSTEM.md, ROADMAP.md, security/THREAT_MODEL.md,
 * hos_engine/{policy,execution_loop,decision_engine,self_model,recovery}.py.
 */

const pptxgen = require("pptxgenjs");
const path = require("path");

const OUT = path.join(__dirname, "Human-OS-prezentacja.pptx");

/* ---------------------------------------------------------------- paleta */

const INK = "0F1533"; // dominanta: głęboki atrament
const INK_SOFT = "1B2450";
const INK_LINE = "2B3563";
const PAPER = "FFFFFF";
const PAPER_ALT = "F2F4FA";
const CARD = "FFFFFF";
const GOLD = "D99A2B"; // akcent: pieczęć / suwerenność
const TEAL = "2F7D8E"; // wsparcie
const CRIMSON = "9E2B32"; // naruszenie / ostrzeżenie
const GREY = "5B6280";
const GREY_LT = "9AA0B8";
const DIM = "C9CEE0";

const H_FONT = "Cambria";
const B_FONT = "Calibri";
const M_FONT = "Courier New";

const W = 13.33;
const H = 7.5;
const M = 0.7; // margines

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Human OS Initiative";
pres.title = "Human OS — opowieść o autorstwie własnego życia";

/* -------------------------------------------------------------- pomocnicze */

// Motyw przewodni: identyfikator w monospace'owej „plakietce” (GEN-003, PROOF-004...)
function chip(slide, x, y, text, opts) {
  const o = opts || {};
  const w = o.w || 1.15;
  const h = o.h || 0.28;
  slide.addShape(pres.ShapeType.roundRect, {
    x, y, w, h,
    rectRadius: 0.06,
    fill: { color: o.fill || GOLD },
    line: { color: o.fill || GOLD, width: 0 },
  });
  slide.addText(text, {
    x, y, w, h,
    align: o.align || "center", valign: "middle", margin: 0,
    fontFace: M_FONT, fontSize: o.fontSize || 10, bold: true,
    color: o.color || INK,
  });
}

function darkBg(slide) {
  slide.background = { color: INK };
}

function lightBg(slide) {
  slide.background = { color: PAPER };
}

// Nagłówek slajdu (bez linii pod tytułem — oddziela go światło)
function title(slide, text, dark, sub) {
  slide.addText(text, {
    x: M, y: 0.5, w: W - 2 * M, h: 0.72,
    fontFace: H_FONT, fontSize: 34, bold: true, margin: 0,
    color: dark ? PAPER : INK, valign: "middle",
  });
  if (sub) {
    slide.addText(sub, {
      x: M, y: 1.24, w: W - 2 * M, h: 0.36,
      fontFace: B_FONT, fontSize: 14, margin: 0,
      color: dark ? GREY_LT : GREY, valign: "middle",
    });
  }
}

function card(slide, x, y, w, h, dark) {
  slide.addShape(pres.ShapeType.roundRect, {
    x, y, w, h,
    rectRadius: 0.04,
    fill: { color: dark ? INK_SOFT : CARD },
    line: { color: dark ? INK_LINE : "DFE3EE", width: 1 },
    shadow: dark ? undefined : { type: "outer", angle: 90, blur: 8, offset: 1, color: "9AA0B8", opacity: 0.18 },
  });
}

function bullet(slide, x, y, color, glyph) {
  slide.addShape(pres.ShapeType.ellipse, {
    x, y, w: 0.3, h: 0.3,
    fill: { color },
    line: { color, width: 0 },
  });
  slide.addText(glyph, {
    x, y, w: 0.3, h: 0.3,
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 12, bold: true, color: PAPER,
  });
}

function footer(slide, text) {
  slide.addText(text, {
    x: M, y: H - 0.62, w: W - 2 * M, h: 0.3,
    fontFace: B_FONT, fontSize: 10, italic: true, margin: 0,
    color: GREY_LT, valign: "middle",
  });
}

// Przerywnik aktu: cyfra rzymska w tle, tytuł aktu, jedno zdanie premisy.
function actBreak(numeral, name, premise, note) {
  const s = pres.addSlide();
  darkBg(s);
  s.addText(numeral, {
    x: 8.3, y: 1.1, w: 4.3, h: 4.6, margin: 0,
    align: "center", valign: "middle",
    fontFace: H_FONT, fontSize: 190, bold: true, color: INK_SOFT,
  });
  chip(s, M, 2.35, "AKT " + numeral, { w: 1.35, fill: GOLD });
  s.addText(name, {
    x: M, y: 2.85, w: 7.3, h: 0.95, margin: 0,
    fontFace: H_FONT, fontSize: 44, bold: true, color: PAPER, valign: "middle",
  });
  s.addText(premise, {
    x: M, y: 3.95, w: 7.2, h: 0.8, margin: 0,
    fontFace: B_FONT, fontSize: 16, color: GREY_LT, lineSpacing: 24, valign: "top",
  });
  if (note) {
    s.addText(note, {
      x: M, y: 4.95, w: 7.2, h: 0.4, margin: 0,
      fontFace: B_FONT, fontSize: 12, italic: true, color: GOLD, valign: "middle",
    });
  }
  return s;
}

/* ============================================================ 1. TYTUŁ === */
{
  const s = pres.addSlide();
  darkBg(s);

  const bands = ["Applications", "SDK / Hub", "Engine", "HOSS / HOSP", "Constitution"];
  bands.forEach((b, i) => {
    const y = 1.35 + i * 0.82;
    const inset = i * 0.16;
    s.addShape(pres.ShapeType.roundRect, {
      x: 8.55 + inset, y, w: 3.9 - 2 * inset, h: 0.62,
      rectRadius: 0.05,
      fill: { color: i === 4 ? GOLD : INK_SOFT },
      line: { color: i === 4 ? GOLD : INK_LINE, width: 1 },
    });
    s.addText(b, {
      x: 8.55 + inset, y, w: 3.9 - 2 * inset, h: 0.62,
      align: "center", valign: "middle", margin: 0,
      fontFace: B_FONT, fontSize: 13, bold: true,
      color: i === 4 ? INK : PAPER,
    });
  });

  s.addText("Human OS", {
    x: M, y: 1.95, w: 7.4, h: 1.1,
    fontFace: H_FONT, fontSize: 60, bold: true, margin: 0,
    color: PAPER, valign: "middle",
  });
  s.addText("Opowieść o autorstwie własnego życia", {
    x: M, y: 3.05, w: 7.4, h: 0.5,
    fontFace: B_FONT, fontSize: 21, margin: 0,
    color: GOLD, valign: "middle",
  });
  s.addText(
    "„Human OS nie decyduje, czym ma stać się życie człowieka.\nPomaga człowiekowi pozostać autorem tego życia.”",
    {
      x: M, y: 3.7, w: 7.2, h: 0.9,
      fontFace: B_FONT, fontSize: 14, italic: true, margin: 0,
      color: GREY_LT, lineSpacing: 22, valign: "top",
    }
  );

  chip(s, M, 4.85, "v0.9.0", { w: 1.0, fill: GOLD });
  chip(s, 1.8, 4.85, "BETA", { w: 0.9, fill: INK_SOFT, color: PAPER });
  chip(s, 2.85, 4.85, "Apache-2.0 / CC BY 4.0", { w: 2.5, fill: INK_SOFT, color: PAPER });

  s.addText("Konstytucyjny protokół i silnik referencyjny  ·  wydanie 0.9.0  ·  sierpień 2026", {
    x: M, y: 6.4, w: 7.6, h: 0.35,
    fontFace: B_FONT, fontSize: 11, margin: 0,
    color: GREY_LT, valign: "middle",
  });

  s.addNotes(
    "Trzy akty: Pytanie (dlaczego to w ogóle powstało), Reguły (czym są związane " +
    "obietnice), Podróż (jak wygląda jedna intencja od początku do końca). " +
    "Epilog mówi, czego jeszcze nie ma."
  );
}

/* ====================================================== 2. AKT I ========= */
{
  const s = actBreak(
    "I", "Pytanie",
    "Zanim powstała pierwsza linia kodu, było pytanie: kto właściwie pisze scenariusz " +
    "twojego dnia — ty czy systemy, z których korzystasz?"
  );
  s.addNotes("Ten akt nie mówi jeszcze o technologii. Mówi o stawce.");
}

/* ============================================ 3. HOOK: PYTANIE =========== */
{
  const s = pres.addSlide();
  lightBg(s);
  title(s, "Kto jest autorem twojego dnia?", false,
    "Zwykły poranek, w którym większość wyborów została podjęta zanim się obudziłeś");

  s.addText(
    "Nie chodzi o spisek. Chodzi o kierunek optymalizacji: systemy, które nas otaczają, " +
    "są strojone pod własną metrykę — a ta rzadko brzmi „niech ten człowiek będzie bardziej " +
    "samodzielny”.",
    {
      x: M, y: 1.95, w: 5.9, h: 1.6, margin: 0,
      fontFace: B_FONT, fontSize: 15, color: INK, lineSpacing: 26, valign: "top",
    }
  );
  s.addText(
    "Pytanie nie jest, czy technologia ma wpływ. Pytanie brzmi: czy ten wpływ jest " +
    "jawny, ograniczony i odwracalny — i czy ktoś go w ogóle egzekwuje.",
    {
      x: M, y: 3.75, w: 5.9, h: 1.5, margin: 0,
      fontFace: B_FONT, fontSize: 15, italic: true, color: GREY, lineSpacing: 26, valign: "top",
    }
  );

  const day = [
    ["Co czytasz", "wybiera ranking"],
    ["Co oglądasz", "wybiera rekomendacja"],
    ["Kiedy przerywasz", "wybiera powiadomienie"],
  ];
  day.forEach((d, i) => {
    const y = 1.95 + i * 1.55;
    card(s, 7.1, y, 5.53, 1.3, false);
    s.addText(d[0], {
      x: 7.45, y: y + 0.22, w: 4.9, h: 0.36, margin: 0,
      fontFace: B_FONT, fontSize: 17, bold: true, color: INK, valign: "middle",
    });
    s.addText(d[1], {
      x: 7.45, y: y + 0.62, w: 4.9, h: 0.4, margin: 0,
      fontFace: B_FONT, fontSize: 14, color: CRIMSON, valign: "middle",
    });
  });

  s.addNotes("Świadomie bez statystyk — deck nie opiera się na liczbach, których nie da się " +
    "zweryfikować w repozytorium.");
}

/* ============================================ 4. DWIE MIARY ============== */
{
  const s = pres.addSlide();
  lightBg(s);
  title(s, "Dwie miary sukcesu", false,
    "Ta sama technologia, dwa zupełnie różne kryteria wygranej");

  card(s, M, 1.9, 5.6, 4.4, false);
  s.addText("Typowa metryka", {
    x: M + 0.35, y: 2.15, w: 4.9, h: 0.4, margin: 0,
    fontFace: B_FONT, fontSize: 17, bold: true, color: CRIMSON, valign: "middle",
  });
  const theirs = ["czas spędzony w aplikacji", "retencja i częstotliwość powrotów",
    "„zaangażowanie” jako cel sam w sobie", "użytkownik, który nie potrafi odejść"];
  theirs.forEach((t, i) => {
    const y = 2.75 + i * 0.78;
    bullet(s, M + 0.35, y, CRIMSON, "✕");
    s.addText(t, {
      x: M + 0.85, y: y - 0.02, w: 4.4, h: 0.36, margin: 0,
      fontFace: B_FONT, fontSize: 13.5, color: INK, valign: "middle",
    });
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: 6.95, y: 1.9, w: 5.68, h: 4.4,
    rectRadius: 0.05,
    fill: { color: INK }, line: { color: INK, width: 0 },
  });
  s.addText("Metryka Human OS", {
    x: 7.3, y: 2.15, w: 5.0, h: 0.4, margin: 0,
    fontFace: B_FONT, fontSize: 17, bold: true, color: GOLD, valign: "middle",
  });
  const ours = ["spadek zależności od systemu", "wzrost autonomii i sprawczości",
    "jawność wpływu i ograniczeń", "wyjście, z którego da się skorzystać"];
  ours.forEach((t, i) => {
    const y = 2.75 + i * 0.78;
    bullet(s, 7.3, y, TEAL, "✓");
    s.addText(t, {
      x: 7.8, y: y - 0.02, w: 4.5, h: 0.36, margin: 0,
      fontFace: B_FONT, fontSize: 13.5, color: PAPER, valign: "middle",
    });
  });
  chip(s, 7.3, 5.85, "GEN-012", { w: 1.25, fill: GOLD });
  s.addText("malejąca niezbędność systemu", {
    x: 8.75, y: 5.85, w: 3.6, h: 0.28, margin: 0,
    fontFace: B_FONT, fontSize: 12, bold: true, color: GREY_LT, valign: "middle",
  });

  footer(s, "„Human OS wygrywa wtedy, gdy jest coraz mniej potrzebny” — to jedyny gen, który każe systemowi dążyć do własnego zaniku.");
  s.addNotes("To jest zwrot akcji całej opowieści: kryterium sukcesu jest odwrócone.");
}

/* ======================================== 5. OBIETNICA I GRANICE ========= */
{
  const s = pres.addSlide();
  lightBg(s);
  title(s, "Obietnica i granice", false,
    "Deklaracja jest tania — dlatego od razu towarzyszy jej lista rzeczy zakazanych");

  const jest = [
    ["Pomaga rozumieć", "Nie zastępuje rozumienia ani nie odbiera decyzji."],
    ["Ujawnia niepewność", "Zamiast ukrywać wątpliwość, pokazuje ją wprost."],
    ["Traktuje dane jak depozyt", "Powierzony zasób, nigdy towar do sprzedania."],
  ];
  const nie = [
    ["Wyrocznia", "Nie rozstrzyga, co jest słuszne w czyimś życiu."],
    ["Lekarz, terapeuta, doktryna", "Nie zastępuje profesjonalnej opieki ani systemu wartości."],
    ["Platforma uzależniająca", "Nie optymalizuje czasu w aplikacji i nie rankinguje ludzi."],
  ];

  s.addText("SZEŚĆ ZOBOWIĄZAŃ — OTO TRZY", {
    x: M, y: 1.78, w: 5.9, h: 0.3, margin: 0,
    fontFace: B_FONT, fontSize: 12, bold: true, color: TEAL, charSpacing: 2,
  });
  s.addText("SZEŚĆ ZAKAZÓW — OTO TRZY", {
    x: 6.95, y: 1.78, w: 5.7, h: 0.3, margin: 0,
    fontFace: B_FONT, fontSize: 12, bold: true, color: CRIMSON, charSpacing: 2,
  });

  jest.forEach((it, i) => {
    const y = 2.2 + i * 1.42;
    card(s, M, y, 5.6, 1.22, false);
    bullet(s, M + 0.28, y + 0.28, TEAL, "✓");
    s.addText(it[0], {
      x: M + 0.72, y: y + 0.2, w: 4.7, h: 0.36, margin: 0,
      fontFace: B_FONT, fontSize: 15, bold: true, color: INK, valign: "middle",
    });
    s.addText(it[1], {
      x: M + 0.72, y: y + 0.58, w: 4.6, h: 0.55, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: GREY, valign: "top",
    });
  });

  nie.forEach((it, i) => {
    const y = 2.2 + i * 1.42;
    card(s, 6.95, y, 5.68, 1.22, false);
    bullet(s, 7.23, y + 0.28, CRIMSON, "✕");
    s.addText(it[0], {
      x: 7.67, y: y + 0.2, w: 4.7, h: 0.36, margin: 0,
      fontFace: B_FONT, fontSize: 15, bold: true, color: INK, valign: "middle",
    });
    s.addText(it[1], {
      x: 7.67, y: y + 0.58, w: 4.7, h: 0.55, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: GREY, valign: "top",
    });
  });

  footer(s, "Źródło: constitution/README.md — „Obietnica systemu” i „Czym system nie jest”.");
  s.addNotes("Konstytucja wymienia po sześć pozycji w każdej kolumnie; slajd pokazuje po trzy.");
}

/* ===================================================== 6. AKT II ========= */
{
  const s = actBreak(
    "II", "Reguły",
    "Obietnica, której nikt nie egzekwuje, jest marketingiem. Dlatego zasady zostały " +
    "zapisane tak, żeby dało się je wykonać — i przetestować."
  );
  s.addNotes("Przejście od „chcemy dobrze” do „oto mechanizm, który tego pilnuje”.");
}

/* ==================================================== 7. ARCHITEKTURA ==== */
{
  const s = pres.addSlide();
  lightBg(s);
  title(s, "Pięć warstw, jeden kierunek zależności", false,
    "Żadna niższa warstwa nie może po cichu redefiniować zasady warstwy wyższej");

  const layers = [
    ["Constitution", "constitution/", "21 rozdziałów, 4 załączniki, 15 genów konstytucyjnych", GOLD, INK],
    ["HOSS / HOSP", "spec/, protocol/", "przenośne kontrakty i podpisane koperty komunikatów", TEAL, PAPER],
    ["Engine", "hos_engine/", "wykonywalna implementacja referencyjna w Pythonie", INK, PAPER],
    ["SDK / Hub", "sdk/, hub/", "routing, weryfikacja zgody, poświadczenia, odkrywanie usług", INK_SOFT, PAPER],
    ["Applications", "app/, apps/user-demo/", "cienkie klienty — bez własnej logiki polityk", GREY, PAPER],
  ];

  layers.forEach((l, i) => {
    const y = 1.85 + i * 0.98;
    s.addShape(pres.ShapeType.roundRect, {
      x: M, y, w: 7.6, h: 0.78,
      rectRadius: 0.05,
      fill: { color: l[3] }, line: { color: l[3], width: 0 },
    });
    s.addText(l[0], {
      x: M + 0.32, y: y + 0.06, w: 2.5, h: 0.36, margin: 0,
      fontFace: B_FONT, fontSize: 15, bold: true, color: l[4], valign: "middle",
    });
    s.addText(l[1], {
      x: M + 0.32, y: y + 0.42, w: 2.5, h: 0.3, margin: 0,
      fontFace: M_FONT, fontSize: 9.5, color: l[4], valign: "middle",
    });
    s.addText(l[2], {
      x: M + 2.95, y, w: 4.5, h: 0.78, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: l[4], valign: "middle",
    });
    if (i < 4) {
      s.addShape(pres.ShapeType.triangle, {
        x: M + 3.6, y: y + 0.8, w: 0.34, h: 0.16,
        fill: { color: DIM }, line: { color: DIM, width: 0 },
        rotate: 180,
      });
    }
  });

  card(s, 8.75, 1.85, 3.88, 2.35, false);
  s.addText("Zasada nadrzędności", {
    x: 9.05, y: 2.05, w: 3.3, h: 0.34, margin: 0,
    fontFace: B_FONT, fontSize: 15, bold: true, color: INK, valign: "middle",
  });
  s.addText(
    "Każde wydanie deklaruje zgodne wersje, wpływ migracji, wpływ na bezpieczeństwo " +
    "i znane ograniczenia. Reguł nie da się obejść „w dół” stosu.",
    {
      x: 9.05, y: 2.45, w: 3.3, h: 1.6, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: GREY, lineSpacing: 18, valign: "top",
    }
  );

  card(s, 8.75, 4.4, 3.88, 2.25, false);
  s.addText("Gdzie żyje polityka", {
    x: 9.05, y: 4.6, w: 3.3, h: 0.34, margin: 0,
    fontFace: B_FONT, fontSize: 15, bold: true, color: INK, valign: "middle",
  });
  s.addText(
    "Cała logika konstytucyjna należy do silnika. Aplikacja demonstracyjna i konsola " +
    "Proof Kernel są klientami — nie mają własnych reguł.",
    {
      x: 9.05, y: 5.0, w: 3.3, h: 1.45, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: GREY, lineSpacing: 18, valign: "top",
    }
  );

  s.addNotes("Źródło: ECOSYSTEM.md — kolejność zależności warstw.");
}

/* ========================================================= 8. GENOM ====== */
{
  const s = pres.addSlide();
  lightBg(s);
  title(s, "Genom konstytucyjny: 15 genów", false,
    "Każda materialna zmiana deklaruje, które geny wspiera i które stawia pod ryzykiem");

  const genes = [
    "Prymat człowieka", "Autorstwo życia", "Autonomia", "Świadomy wybór", "Odpowiedzialność",
    "Twórcza sprawczość", "Generatywny przepływ", "Symbioza", "Dobrowolność", "Prywatność",
    "Niezawłaszczanie wartości", "Malejąca niezbędność", "Różnorodność dróg", "Odwracalność",
    "Transparentność wpływu",
  ];

  const cols = 5, cw = 2.38, gap = 0.14;
  genes.forEach((g, i) => {
    const c = i % cols, r = Math.floor(i / cols);
    const x = M + c * (cw + gap);
    const y = 2.0 + r * 1.42;
    const hot = i === 11; // GEN-012 — bohater tej opowieści
    s.addShape(pres.ShapeType.roundRect, {
      x, y, w: cw, h: 1.22,
      rectRadius: 0.05,
      fill: { color: hot ? INK : PAPER_ALT },
      line: { color: hot ? INK : "DFE3EE", width: 1 },
    });
    s.addText("GEN-" + String(i + 1).padStart(3, "0"), {
      x: x + 0.22, y: y + 0.18, w: cw - 0.4, h: 0.28, margin: 0,
      fontFace: M_FONT, fontSize: 10.5, bold: true,
      color: hot ? GOLD : TEAL, valign: "middle",
    });
    s.addText(g, {
      x: x + 0.22, y: y + 0.5, w: cw - 0.4, h: 0.6, margin: 0,
      fontFace: B_FONT, fontSize: 13, bold: true,
      color: hot ? PAPER : INK, valign: "top",
    });
  });

  footer(s, "genome.registry.json v0.2.0 — geny deklaruje się w każdym pull requeście (CONTRIBUTING.md).");
  s.addNotes("Genom to nie ozdobnik: PR bez deklaracji genów nie przechodzi przeglądu.");
}

/* ==================================================== 9. PROOF KERNEL ==== */
{
  const s = pres.addSlide();
  lightBg(s);
  title(s, "Proof Kernel: 9 testów, 6 werdyktów", false,
    "evaluate_action() — każde działanie przechodzi test konstytucyjny przed wykonaniem");

  const tests = [
    ["PROOF-001", "Autorstwo"], ["PROOF-002", "Autonomia"], ["PROOF-003", "Generatywność"],
    ["PROOF-004", "Ekstrakcja"], ["PROOF-005", "Zgoda"], ["PROOF-006", "Odwracalność"],
    ["PROOF-007", "Zależność"], ["PROOF-008", "Przenośność i wyjście"], ["PROOF-009", "Transparentność"],
  ];

  card(s, M, 1.85, 6.55, 4.35, false);
  s.addText("Testy konstytucyjne", {
    x: M + 0.3, y: 2.02, w: 5.9, h: 0.34, margin: 0,
    fontFace: B_FONT, fontSize: 15, bold: true, color: INK, valign: "middle",
  });
  tests.forEach((t, i) => {
    const c = i % 2, r = Math.floor(i / 2);
    const x = M + 0.3 + c * 3.12;
    const y = 2.5 + r * 0.74;
    chip(s, x, y, t[0], { w: 1.15, fill: TEAL, color: PAPER });
    s.addText(t[1], {
      x: x + 1.25, y, w: 1.85, h: 0.28, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: INK, valign: "middle",
    });
  });

  const decisions = [
    ["APPROVED", TEAL], ["APPROVED_WITH_LIMITS", "4F9AA8"], ["REQUIRES_CONSENT", GOLD],
    ["REQUIRES_HUMAN_DECISION", "C07A22"], ["REQUIRES_REDESIGN", "8A5A9E"],
    ["CONSTITUTIONAL_VIOLATION", CRIMSON],
  ];

  card(s, 7.55, 1.85, 5.08, 4.35, false);
  s.addText("Możliwe werdykty", {
    x: 7.85, y: 2.02, w: 4.4, h: 0.34, margin: 0,
    fontFace: B_FONT, fontSize: 15, bold: true, color: INK, valign: "middle",
  });
  decisions.forEach((d, i) => {
    const y = 2.5 + i * 0.62;
    s.addShape(pres.ShapeType.roundRect, {
      x: 7.85, y, w: 4.48, h: 0.5,
      rectRadius: 0.05,
      fill: { color: d[1] }, line: { color: d[1], width: 0 },
    });
    s.addText(d[0], {
      x: 8.05, y, w: 4.2, h: 0.5, margin: 0,
      fontFace: M_FONT, fontSize: 11.5, bold: true, color: PAPER, valign: "middle",
    });
  });

  footer(s, "„Twarda brama przed punktacją” — odmowa nie jest błędem wykonania, tylko poprawnym wynikiem.");
  s.addNotes("proof.rules.json v0.2.0; implementacja w hos_engine/policy.py.");
}

/* ==================================================== 10. AKT III ======== */
{
  const s = actBreak(
    "III", "Podróż",
    "Prześledźmy jedną intencję od początku do końca — z bramami, odmową, wątpliwością, " +
    "hamulcem awaryjnym i wyjściem.",
    "Marta jest przykładem ilustracyjnym, nie prawdziwym przypadkiem użytkownika."
  );
  s.addNotes("Od tego miejsca mechanika przestaje być listą funkcji, a staje się fabułą.");
}

/* ==================================================== 11. INTENCJA ======= */
{
  const s = pres.addSlide();
  lightBg(s);
  title(s, "Intencja", false,
    "Wszystko zaczyna się od zdania wypowiedzianego przez człowieka — nie od decyzji systemu");

  card(s, M, 1.9, 6.6, 2.5, false);
  chip(s, M + 0.35, 2.15, "HOS-INT-…", { w: 1.55, fill: GOLD });
  s.addText(
    "„Poukładaj mi plan zmiany pracy na najbliższy kwartał — sięgnij po moje notatki z ostatniego roku.”",
    {
      x: M + 0.35, y: 2.6, w: 5.9, h: 1.5, margin: 0,
      fontFace: H_FONT, fontSize: 19, italic: true, color: INK, lineSpacing: 30, valign: "top",
    }
  );

  card(s, M, 4.6, 6.6, 1.75, false);
  s.addText("Dlaczego to trudna prośba", {
    x: M + 0.35, y: 4.78, w: 5.9, h: 0.32, margin: 0,
    fontFace: B_FONT, fontSize: 14, bold: true, color: CRIMSON, valign: "middle",
  });
  s.addText(
    "Dotyka danych wrażliwych, wymaga działania agenta w jej imieniu i dotyczy decyzji " +
    "życiowej, której nikt nie powinien podejmować za nią.",
    {
      x: M + 0.35, y: 5.15, w: 5.9, h: 1.0, margin: 0,
      fontFace: B_FONT, fontSize: 13, color: GREY, lineSpacing: 20, valign: "top",
    }
  );

  const asks = [
    ["Kto pyta?", "tożsamość i rola, w jakiej występuje"],
    ["Na co jest zgoda?", "cel, zakres i czas — nie „zgoda na wszystko”"],
    ["Czy wolno to zrobić?", "dziewięć testów konstytucyjnych"],
  ];
  s.addText("Zanim cokolwiek się wydarzy, system musi odpowiedzieć sobie na trzy pytania:", {
    x: 7.55, y: 1.9, w: 5.08, h: 0.6, margin: 0,
    fontFace: B_FONT, fontSize: 13, color: GREY, lineSpacing: 20, valign: "top",
  });
  asks.forEach((a, i) => {
    const y = 2.65 + i * 1.25;
    card(s, 7.55, y, 5.08, 1.05, false);
    s.addText(a[0], {
      x: 7.85, y: y + 0.16, w: 4.5, h: 0.34, margin: 0,
      fontFace: B_FONT, fontSize: 15, bold: true, color: TEAL, valign: "middle",
    });
    s.addText(a[1], {
      x: 7.85, y: y + 0.54, w: 4.5, h: 0.4, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: GREY, valign: "top",
    });
  });

  s.addNotes("HumanIntent to punkt wejścia ExecutionLoop (ADR-CORE-002).");
}

/* ==================================================== 12. SZEŚĆ BRAM ===== */
{
  const s = pres.addSlide();
  lightBg(s);
  title(s, "Sześć bram przed działaniem", false,
    "Każda brama zadaje jedno pytanie. Pierwsza odmowa kończy sprawę");

  const gates = [
    ["1 · TOŻSAMOŚĆ", "Czy prośba pochodzi od Marty, a nie od czegoś, co się nią podszywa?", "PRZECHODZI", TEAL],
    ["2 · ROLA", "W jakiej roli występuje? Jako właścicielka tych danych, nie jako agent.", "PRZECHODZI", TEAL],
    ["3 · ZGODA", "Czy jest zgoda na notatki z ostatniego roku — w tym konkretnym celu?", "BRAK ZGODY", GOLD],
    ["4 · KONTEKST", "Nie zostaje uruchomiona.", "—", DIM],
    ["5 · ENCJE", "Nie zostaje uruchomiona.", "—", DIM],
    ["6 · KONSTYTUCJA", "Nie zostaje uruchomiona.", "—", DIM],
  ];

  gates.forEach((g, i) => {
    const y = 1.9 + i * 0.75;
    const dead = g[3] === DIM;
    s.addShape(pres.ShapeType.roundRect, {
      x: M, y, w: 11.93, h: 0.62,
      rectRadius: 0.05,
      fill: { color: dead ? PAPER : PAPER_ALT },
      line: { color: "DFE3EE", width: 1 },
    });
    chip(s, M + 0.25, y + 0.17, g[0], {
      w: 2.25, fill: dead ? DIM : INK, color: dead ? GREY : PAPER, fontSize: 9.5,
    });
    s.addText(g[1], {
      x: M + 2.75, y, w: 7.0, h: 0.62, margin: 0,
      fontFace: B_FONT, fontSize: 12.5, italic: dead,
      color: dead ? GREY_LT : INK, valign: "middle",
    });
    chip(s, 10.9, y + 0.17, g[2], {
      w: 1.6, fill: dead ? PAPER : g[3], color: dead ? GREY_LT : PAPER, fontSize: 9.5,
    });
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: M, y: 6.4, w: 11.93, h: 0.55,
    rectRadius: 0.05,
    fill: { color: INK }, line: { color: INK, width: 0 },
  });
  chip(s, M + 0.3, 6.53, "REFUSED_CONSENT", { w: 2.1, fill: GOLD, fontSize: 9.5 });
  s.addText("Pętla zatrzymuje się, zanim cokolwiek zostanie wykonane lub zapisane.", {
    x: M + 2.65, y: 6.4, w: 9.0, h: 0.55, margin: 0,
    fontFace: B_FONT, fontSize: 13, bold: true, color: PAPER, valign: "middle",
  });

  s.addNotes("Kolejność bram: IDENTITY → AUTHORITY → CONSENT → CONTEXT → ENTITY → CONSTITUTION. " +
    "Bramy 4–6 nie są „pominięte” — one się po prostu nie wykonują.");
}

/* ============================================== 13. ODMOWA ============== */
{
  const s = pres.addSlide();
  lightBg(s);
  title(s, "Odmowa, która nie jest błędem", false,
    "Refusal jest wynikiem pierwszej klasy — nie wyjątkiem, nie ciszą, nie awarią");

  card(s, M, 1.9, 5.9, 4.4, false);
  s.addText("Co Marta widzi", {
    x: M + 0.35, y: 2.12, w: 5.2, h: 0.36, margin: 0,
    fontFace: B_FONT, fontSize: 16, bold: true, color: INK, valign: "middle",
  });
  const shown = [
    ["Czego zabrakło", "zgody na notatki z ostatniego roku"],
    ["W jakim celu", "wyłącznie ułożenie planu, nic poza tym"],
    ["Na jak długo", "zakres i czas deklarowane z góry"],
    ["Co się nie stało", "żadne dane nie zostały odczytane"],
  ];
  shown.forEach((it, i) => {
    const y = 2.65 + i * 0.88;
    bullet(s, M + 0.35, y, INK, String(i + 1));
    s.addText(it[0], {
      x: M + 0.85, y: y - 0.04, w: 4.7, h: 0.32, margin: 0,
      fontFace: B_FONT, fontSize: 13.5, bold: true, color: INK, valign: "middle",
    });
    s.addText(it[1], {
      x: M + 0.85, y: y + 0.28, w: 4.7, h: 0.32, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: GREY, valign: "middle",
    });
  });

  s.addText("DRUGIE PODEJŚCIE — ZGODA ZAKRESOWA", {
    x: 7.25, y: 1.9, w: 5.38, h: 0.3, margin: 0,
    fontFace: B_FONT, fontSize: 11, bold: true, color: TEAL, charSpacing: 1.5,
  });

  const after = [
    ["Bramy 1–6", "przechodzą — zgoda ma cel, zakres i czas", TEAL],
    ["Proof Kernel", "APPROVED_WITH_LIMITS (PROOF-003)", "4F9AA8"],
    ["Co to znaczy", "plan wraca jako szkic do redakcji, nie gotowa decyzja", GOLD],
  ];
  after.forEach((a, i) => {
    const y = 2.35 + i * 1.35;
    card(s, 7.25, y, 5.38, 1.15, false);
    s.addText(a[0], {
      x: 7.55, y: y + 0.14, w: 4.8, h: 0.32, margin: 0,
      fontFace: B_FONT, fontSize: 14, bold: true, color: a[2], valign: "middle",
    });
    s.addText(a[1], {
      x: 7.55, y: y + 0.5, w: 4.8, h: 0.5, margin: 0,
      fontFace: B_FONT, fontSize: 12.5, color: GREY, valign: "top",
    });
  });

  s.addText("A potem, już bez pytania:", {
    x: 7.25, y: 6.28, w: 5.38, h: 0.3, margin: 0,
    fontFace: B_FONT, fontSize: 11, italic: true, color: GREY, valign: "middle",
  });
  chip(s, 7.25, 6.6, "7 AGENT  ·  8 POŚWIADCZENIE  ·  9 ZDARZENIE  ·  10 AUDYT", {
    w: 5.38, fill: INK, color: PAPER, fontSize: 9,
  });

  s.addNotes("PROOF-003 (test generatywności) ma status porażki APPROVED_WITH_LIMITS — " +
    "działanie jest dozwolone, ale w ograniczonej formie.");
}

/* ============================================== 14. ABSTENCJA =========== */
{
  const s = pres.addSlide();
  lightBg(s);
  title(s, "Kiedy system nie wie", false,
    "Najtrudniejsza umiejętność doradcy: powiedzieć „wstrzymuję się” zamiast zgadywać");

  s.addText(
    "Notatki Marty przeczą sobie nawzajem: w marcu pisała, że chce stabilności, w listopadzie — " +
    "że dusi się w tej pracy. Zwykły ranking wybrałby po prostu wyżej punktowany wariant.",
    {
      x: M, y: 1.9, w: 6.05, h: 1.35, margin: 0,
      fontFace: B_FONT, fontSize: 14, color: INK, lineSpacing: 24, valign: "top",
    }
  );
  card(s, M, 3.35, 6.05, 2.62, false);
  chip(s, M + 0.35, 3.6, "CONTRADICTORY_EVIDENCE", { w: 3.1, fill: GOLD, fontSize: 9 });
  s.addText("Human OS nie rankinguje. Wstrzymuje się i mówi, dlaczego.", {
    x: M + 0.35, y: 4.05, w: 5.4, h: 0.7, margin: 0,
    fontFace: H_FONT, fontSize: 18, bold: true, color: INK, lineSpacing: 26, valign: "top",
  });
  s.addText(
    "Sprzeczność wraca do Marty jako pytanie, nie znika w uśrednionej rekomendacji. " +
    "Rozstrzygnięcie należy do niej.",
    {
      x: M + 0.35, y: 4.85, w: 5.4, h: 1.2, margin: 0,
      fontFace: B_FONT, fontSize: 13, color: GREY, lineSpacing: 20, valign: "top",
    }
  );

  s.addText("OSIEM NAZWANYCH POWODÓW WSTRZYMANIA SIĘ", {
    x: 7.25, y: 1.9, w: 5.38, h: 0.3, margin: 0,
    fontFace: B_FONT, fontSize: 11, bold: true, color: TEAL, charSpacing: 1.5,
  });
  const reasons = [
    "NO_CLEAR_GOAL", "INSUFFICIENT_DATA", "VALUE_CONFLICT", "CONTRADICTORY_EVIDENCE",
    "NOT_MONITORABLE", "EXCESSIVE_RISK", "BEYOND_COMPETENCE", "SUSPECTED_CRISIS",
  ];
  reasons.forEach((r, i) => {
    const y = 2.35 + i * 0.52;
    const hot = r === "CONTRADICTORY_EVIDENCE";
    s.addShape(pres.ShapeType.roundRect, {
      x: 7.25, y, w: 5.38, h: 0.42,
      rectRadius: 0.05,
      fill: { color: hot ? GOLD : PAPER_ALT },
      line: { color: hot ? GOLD : "DFE3EE", width: 1 },
    });
    s.addText(r, {
      x: 7.5, y, w: 5.0, h: 0.42, margin: 0,
      fontFace: M_FONT, fontSize: 11, bold: true,
      color: hot ? INK : GREY, valign: "middle",
    });
  });

  footer(s, "Abstencja i eskalacja są osobnymi rodzajami wyniku — nigdy wyjątkami (ADR-DECISION-003).");
  s.addNotes("Dziewięć twardych bram G0–G8 działa przed rankingiem; kandydat odrzucony przez bramę " +
    "nie wraca później nawet z wysokim wynikiem.");
}

/* ============================================== 15. KOREKTA ============= */
{
  const s = pres.addSlide();
  lightBg(s);
  title(s, "Kiedy system się myli", false,
    "Model siebie jest hipotezą o człowieku — i tylko ten człowiek może ją zatwierdzić");

  const kinds = [
    ["DEKLARACJA", "„Zmieniam branżę.” — powiedziała to wprost.", TEAL, PAPER],
    ["OBSERWACJA", "Wieczorami wraca do notatek o projektach.", "4F9AA8", PAPER],
    ["HIPOTEZA", "„Unikasz ryzyka.” — domysł systemu.", GOLD, INK],
  ];
  kinds.forEach((k, i) => {
    const x = M + i * 4.03;
    card(s, x, 1.9, 3.83, 1.72, false);
    chip(s, x + 0.28, 2.12, k[0], { w: 1.5, fill: k[2], color: k[3] });
    s.addText(k[1], {
      x: x + 0.28, y: 2.56, w: 3.3, h: 0.95, margin: 0,
      fontFace: B_FONT, fontSize: 12.5, color: GREY, lineSpacing: 18, valign: "top",
    });
  });

  s.addText("Marta czyta hipotezę i mówi: nieprawda.", {
    x: M, y: 3.85, w: 11.93, h: 0.42, margin: 0,
    fontFace: H_FONT, fontSize: 20, bold: true, color: INK, valign: "middle",
  });

  const steps = [
    ["Nie znika", "Hipoteza dostaje status CONTESTED — zapis zostaje, historia też."],
    ["Nie nadpisuje", "Korekta tworzy nową wersję przez łańcuch „supersedes”."],
    ["Tłumaczy się", "why() pokazuje cytat, autora, pasmo pewności i całą historię."],
    ["Nie awansuje sama", "Hipoteza nigdy nie jest podawana dalej jako deklaracja."],
  ];
  steps.forEach((st, i) => {
    const x = M + i * 3.03;
    card(s, x, 4.45, 2.85, 1.85, false);
    bullet(s, x + 0.25, 4.68, INK, String(i + 1));
    s.addText(st[0], {
      x: x + 0.25, y: 5.08, w: 2.35, h: 0.32, margin: 0,
      fontFace: B_FONT, fontSize: 14, bold: true, color: TEAL, valign: "middle",
    });
    s.addText(st[1], {
      x: x + 0.25, y: 5.42, w: 2.35, h: 0.8, margin: 0,
      fontFace: B_FONT, fontSize: 11.5, color: GREY, lineSpacing: 17, valign: "top",
    });
  });

  footer(s, "Sprzeczność między zapisami jest zachowywana jako sygnał — rozstrzyga ją tylko osoba, której dotyczy.");
  s.addNotes("Silnik nie zawiera NLP: rozpoznawanie kandydatów na zapisy to zadanie aplikacji.");
}

/* ============================================== 16. HAMULEC ============= */
{
  const s = pres.addSlide();
  darkBg(s);
  title(s, "Hamulec, którego nie da się zabrać", true,
    "Marta mówi „stop” — i to zdanie musi działać nawet wtedy, gdy reszta zawodzi");

  const prot = [["SAFE_MODE", "R0"], ["READ_ONLY", "R0"], ["FREEZE", "R1"], ["DISCONNECT", "R1"]];
  const cons = [["EXPORT", "R1"], ["ROLLBACK", "R2"], ["RECOVERY", "R3"]];

  s.addText("TRYBY OCHRONNE", {
    x: M, y: 1.95, w: 5.9, h: 0.3, margin: 0,
    fontFace: B_FONT, fontSize: 12, bold: true, color: TEAL, charSpacing: 2,
  });
  s.addText("automatyczne tylko za powiadomieniem · zawsze odwracalne", {
    x: M, y: 2.25, w: 5.9, h: 0.3, margin: 0,
    fontFace: B_FONT, fontSize: 11, color: GREY_LT,
  });
  prot.forEach((m, i) => {
    const y = 2.62 + i * 0.68;
    card(s, M, y, 5.6, 0.58, true);
    s.addText(m[0], {
      x: M + 0.28, y, w: 3.6, h: 0.58, margin: 0,
      fontFace: M_FONT, fontSize: 13, bold: true, color: PAPER, valign: "middle",
    });
    chip(s, M + 4.55, y + 0.15, m[1], { w: 0.75, fill: TEAL, color: PAPER });
  });

  s.addText("TRYBY KONSEKWENTNE", {
    x: 6.95, y: 1.95, w: 5.7, h: 0.3, margin: 0,
    fontFace: B_FONT, fontSize: 12, bold: true, color: GOLD, charSpacing: 2,
  });
  s.addText("wyłącznie ręcznie · ROLLBACK i RECOVERY na dwa klucze", {
    x: 6.95, y: 2.25, w: 5.7, h: 0.3, margin: 0,
    fontFace: B_FONT, fontSize: 11, color: GREY_LT,
  });
  cons.forEach((m, i) => {
    const y = 2.62 + i * 0.68;
    card(s, 6.95, y, 5.68, 0.58, true);
    s.addText(m[0], {
      x: 7.23, y, w: 3.6, h: 0.58, margin: 0,
      fontFace: M_FONT, fontSize: 13, bold: true, color: PAPER, valign: "middle",
    });
    chip(s, 11.6, y + 0.15, m[1], { w: 0.75, fill: GOLD });
  });

  const guards = [
    ["Nie ma czego wyłączyć", "Nie istnieje API zmieniające politykę ani dziennik audytu."],
    ["Agent nigdy nie aktywuje", "AGENT, SERVICE i SYSTEM_PROCESS dostają odmowę — a sama odmowa jest logowana."],
    ["Działa bez AI i bez sieci", "Warstwa ratunkowa nie ma zależności od modelu ani od świata zewnętrznego."],
  ];
  guards.forEach((g, i) => {
    const x = M + i * 4.03;
    const y = 5.6;
    s.addShape(pres.ShapeType.roundRect, {
      x, y, w: 3.83, h: 1.2,
      rectRadius: 0.05,
      fill: { color: INK_SOFT }, line: { color: INK_LINE, width: 1 },
    });
    s.addText(g[0], {
      x: x + 0.24, y: y + 0.14, w: 3.4, h: 0.32, margin: 0,
      fontFace: B_FONT, fontSize: 13, bold: true, color: GOLD, valign: "middle",
    });
    s.addText(g[1], {
      x: x + 0.24, y: y + 0.48, w: 3.4, h: 0.66, margin: 0,
      fontFace: B_FONT, fontSize: 11, color: GREY_LT, valign: "top",
    });
  });

  s.addNotes("R0–R3 to skala ryzyka Konstytucji; żaden z siedmiu trybów nie sięga R4, bo wszystkie " +
    "są mechanizmami sankcjonowanymi. Odmowa jest tu wyjątkiem (RecoveryRefused) — zignorowana " +
    "ochrona nie może wyglądać jak ochrona działająca.");
}

/* ============================================== 17. WYJŚCIE ============= */
{
  const s = pres.addSlide();
  lightBg(s);
  title(s, "Wyjście jest częścią umowy", false,
    "Ostatni rozdział tej historii: Marta odchodzi — i to nie jest porażka systemu");

  card(s, M, 1.9, 6.4, 4.4, false);
  s.addText("Co zabiera ze sobą", {
    x: M + 0.35, y: 2.12, w: 5.7, h: 0.36, margin: 0,
    fontFace: B_FONT, fontSize: 16, bold: true, color: INK, valign: "middle",
  });
  const pack = [
    "dane i graf powiązań w otwartym JSON",
    "metadane i rejestr zmian",
    "historię wersji wycofanych — nic nie zostaje po cichu skasowane",
    "ślad audytowy: kto, kiedy, na jakiej podstawie",
  ];
  pack.forEach((p, i) => {
    const y = 2.7 + i * 0.82;
    bullet(s, M + 0.35, y, TEAL, "✓");
    s.addText(p, {
      x: M + 0.85, y: y - 0.06, w: 5.2, h: 0.42, margin: 0,
      fontFace: B_FONT, fontSize: 13, color: INK, valign: "middle",
    });
  });
  chip(s, M + 0.35, 5.8, "EXPORT", { w: 1.15, fill: GOLD });
  s.addText("tryb ręczny, klasa ryzyka R1 —\nnigdy nie odbywa się bez jej decyzji", {
    x: M + 1.65, y: 5.72, w: 4.35, h: 0.55, margin: 0,
    fontFace: B_FONT, fontSize: 11.5, color: GREY, lineSpacing: 15, valign: "middle",
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: 7.55, y: 1.9, w: 5.08, h: 4.4,
    rectRadius: 0.05,
    fill: { color: INK }, line: { color: INK, width: 0 },
  });
  s.addText("Odejście jako dowód", {
    x: 7.9, y: 2.2, w: 4.4, h: 0.4, margin: 0,
    fontFace: B_FONT, fontSize: 17, bold: true, color: GOLD, valign: "middle",
  });
  s.addText(
    "Gdyby wyjście było trudne, cała reszta byłaby dekoracją. Kosztowne wyjście zamienia " +
    "obietnicę autonomii w pułapkę — i to niezależnie od tego, jak dobre są intencje twórców.",
    {
      x: 7.9, y: 2.75, w: 4.4, h: 1.7, margin: 0,
      fontFace: B_FONT, fontSize: 13, color: GREY_LT, lineSpacing: 21, valign: "top",
    }
  );
  s.addText(
    "Dlatego przenośność i wyjście mają własny test konstytucyjny (PROOF-008) i własny gen.",
    {
      x: 7.9, y: 4.5, w: 4.4, h: 1.0, margin: 0,
      fontFace: B_FONT, fontSize: 13, bold: true, color: PAPER, lineSpacing: 21, valign: "top",
    }
  );
  chip(s, 7.9, 5.75, "GEN-012", { w: 1.25, fill: GOLD });
  chip(s, 9.35, 5.75, "PROOF-008", { w: 1.45, fill: INK_SOFT, color: PAPER });

  s.addNotes("export_sovereign_package() w hos_engine/recovery.py — jeden z sześciu kontraktów Hub.");
}

/* ======================================== 18. CZEGO NIE MA ============== */
{
  const s = pres.addSlide();
  lightBg(s);
  title(s, "Czego jeszcze nie ma", false,
    "Historia, która chwali się tylko sukcesami, nie zasługuje na zaufanie");

  const have = [
    ["Podpisane koperty HOSP/0.2", "kanoniczny JSON, HMAC, znacznik protokołu"],
    ["Rejestr tożsamości i kluczy", "rotacja kluczy, powiązanie klucza z tożsamością"],
    ["ReplayGuard", "nonce, wygasanie, śledzenie identyfikatorów komunikatów"],
    ["Jawne polityki zaufania", "TrustLevel i TrustPolicy zamiast domyślnego zaufania"],
    ["Security Gateway", "dziesięciokrokowy potok kontroli przed wykonaniem"],
    ["Łańcuch skrótów SHA-256", "weryfikowalna integralność dziennika zdarzeń"],
  ];
  s.addText("CO JUŻ DZIAŁA", {
    x: M, y: 1.78, w: 7.6, h: 0.3, margin: 0,
    fontFace: B_FONT, fontSize: 11, bold: true, color: TEAL, charSpacing: 1.5,
  });
  have.forEach((h, i) => {
    const c = i % 2, r = Math.floor(i / 2);
    const x = M + c * 3.95;
    const y = 2.2 + r * 1.42;
    card(s, x, y, 3.75, 1.22, false);
    s.addText(h[0], {
      x: x + 0.25, y: y + 0.2, w: 3.3, h: 0.32, margin: 0,
      fontFace: B_FONT, fontSize: 13, bold: true, color: INK, valign: "middle",
    });
    s.addText(h[1], {
      x: x + 0.25, y: y + 0.56, w: 3.3, h: 0.55, margin: 0,
      fontFace: B_FONT, fontSize: 11, color: GREY, valign: "top",
    });
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: 8.75, y: 1.78, w: 3.88, h: 4.64,
    rectRadius: 0.05,
    fill: { color: CRIMSON }, line: { color: CRIMSON, width: 0 },
  });
  s.addText("Nie jest produkcyjne", {
    x: 9.05, y: 2.05, w: 3.3, h: 0.4, margin: 0,
    fontFace: H_FONT, fontSize: 19, bold: true, color: PAPER, valign: "middle",
  });
  s.addText(
    [
      { text: "Brak uwierzytelniania i autoryzacji", options: { bullet: true, breakLine: true } },
      { text: "Brak szyfrowania danych w spoczynku", options: { bullet: true, breakLine: true } },
      { text: "Brak niezależnego przeglądu bezpieczeństwa", options: { bullet: true, breakLine: true } },
      { text: "Brak kalibracji empirycznej", options: { bullet: true, breakLine: true } },
      { text: "HMAC to mechanizm referencyjny, lokalny — nie podpis asymetryczny", options: { bullet: true } },
    ],
    {
      x: 9.05, y: 2.6, w: 3.3, h: 3.0, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: PAPER,
      paraSpaceAfter: 8, valign: "top",
    }
  );
  s.addText("security/THREAT_MODEL.md", {
    x: 9.05, y: 5.9, w: 3.3, h: 0.3, margin: 0,
    fontFace: M_FONT, fontSize: 10, color: "F2C9CB", valign: "middle",
  });

  s.addNotes("Jawność ograniczeń nie jest tu skromnością, tylko wymogiem konstytucyjnym " +
    "(GEN-015, transparentność wpływu).");
}

/* ======================================== 19. GDZIE JESTEŚMY ============ */
{
  const s = pres.addSlide();
  darkBg(s);
  title(s, "Gdzie jesteśmy dzisiaj", true,
    "Osiem etapów zamkniętych, jeden otwarty — i jeden, który jest celem");

  const stats = [
    ["36", "modułów silnika", "hos_engine/"],
    ["166", "testów automatycznych", "Python 3.11 / 3.12 / 3.13"],
    ["67", "rekordów decyzji (ADR)", "docs/adr/"],
  ];
  stats.forEach((st, i) => {
    const x = M + i * 4.03;
    card(s, x, 1.9, 3.83, 1.65, true);
    s.addText(st[0], {
      x: x + 0.3, y: 2.02, w: 3.2, h: 0.75, margin: 0,
      fontFace: H_FONT, fontSize: 40, bold: true, color: GOLD, valign: "middle",
    });
    s.addText(st[1], {
      x: x + 0.3, y: 2.8, w: 3.25, h: 0.32, margin: 0,
      fontFace: B_FONT, fontSize: 13.5, bold: true, color: PAPER, valign: "middle",
    });
    s.addText(st[2], {
      x: x + 0.3, y: 3.12, w: 3.25, h: 0.3, margin: 0,
      fontFace: M_FONT, fontSize: 10, color: GREY_LT, valign: "middle",
    });
  });

  s.addText("0.1 – 0.8   formalny rdzeń · specyfikacja · silnik polityk · trwały audyt · graf wiedzy · " +
    "runtime agentów · symulacje · model człowieka", {
    x: M, y: 3.85, w: 11.93, h: 0.5, margin: 0,
    fontFace: B_FONT, fontSize: 12, color: GREY_LT, valign: "middle",
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: M, y: 4.45, w: 11.93, h: 1.1,
    rectRadius: 0.05,
    fill: { color: GOLD }, line: { color: GOLD, width: 0 },
  });
  s.addText("0.9", {
    x: M + 0.3, y: 4.45, w: 0.8, h: 1.1, margin: 0,
    fontFace: M_FONT, fontSize: 24, bold: true, color: INK, valign: "middle",
  });
  s.addText("Interoperacyjność protokołu i przegląd bezpieczeństwa — OTWARTE", {
    x: M + 1.15, y: 4.6, w: 10.4, h: 0.34, margin: 0,
    fontFace: B_FONT, fontSize: 15, bold: true, color: INK, valign: "middle",
  });
  s.addText("Warstwy wykonawcze i plastry warstw 2–6 powstały równolegle i nie zastępują tego punktu.", {
    x: M + 1.15, y: 4.96, w: 10.4, h: 0.36, margin: 0,
    fontFace: B_FONT, fontSize: 12, color: "5A4212", valign: "middle",
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: M, y: 5.7, w: 11.93, h: 1.1,
    rectRadius: 0.05,
    fill: { color: INK_SOFT }, line: { color: INK_LINE, width: 1 },
  });
  s.addText("1.0", {
    x: M + 0.3, y: 5.7, w: 0.8, h: 1.1, margin: 0,
    fontFace: M_FONT, fontSize: 24, bold: true, color: GOLD, valign: "middle",
  });
  s.addText("Stabilny protokół, silnik i runtime referencyjny", {
    x: M + 1.15, y: 5.85, w: 10.4, h: 0.34, margin: 0,
    fontFace: B_FONT, fontSize: 15, bold: true, color: PAPER, valign: "middle",
  });
  s.addText("Warunki: stabilna Konstytucja · wersjonowany protokół · migracje · udokumentowany przegląd " +
    "bezpieczeństwa · pełna przenośność danych · mierzalna możliwość wyjścia.", {
    x: M + 1.15, y: 6.21, w: 10.4, h: 0.36, margin: 0,
    fontFace: B_FONT, fontSize: 11.5, color: GREY_LT, valign: "middle",
  });

  s.addNotes("Zerowy dług mypy w silniku; CI uruchamia ruff i pytest na trzech wersjach Pythona. " +
    "Kryterium 0.9 zmienione decyzją foundera 2026-08-17 (DD-008).");
}

/* ==================================================== 20. ZAMKNIĘCIE ===== */
{
  const s = pres.addSlide();
  darkBg(s);

  s.addShape(pres.ShapeType.roundRect, {
    x: 8.9, y: 1.6, w: 3.73, h: 4.3,
    rectRadius: 0.05,
    fill: { color: INK_SOFT }, line: { color: INK_LINE, width: 1 },
  });
  s.addText("Co dalej", {
    x: 9.2, y: 1.85, w: 3.1, h: 0.38, margin: 0,
    fontFace: B_FONT, fontSize: 16, bold: true, color: GOLD, valign: "middle",
  });
  const next = [
    ["make verify", "lint, typy i testy przed każdą zmianą"],
    ["python run_demo.py", "ścieżka Proof Kernel od ręki"],
    ["CONTRIBUTING.md", "deklaracja genów w każdym PR"],
    ["GOVERNANCE.md", "zmiana Konstytucji to osobna ścieżka"],
  ];
  next.forEach((n, i) => {
    const y = 2.4 + i * 0.85;
    s.addText(n[0], {
      x: 9.2, y, w: 3.1, h: 0.3, margin: 0,
      fontFace: M_FONT, fontSize: 12, bold: true, color: PAPER, valign: "middle",
    });
    s.addText(n[1], {
      x: 9.2, y: y + 0.3, w: 3.1, h: 0.4, margin: 0,
      fontFace: B_FONT, fontSize: 11, color: GREY_LT, valign: "top",
    });
  });

  s.addText("Kto jest autorem twojego dnia?", {
    x: M, y: 2.05, w: 7.6, h: 0.6, margin: 0,
    fontFace: B_FONT, fontSize: 20, italic: true, color: GREY_LT, valign: "middle",
  });
  s.addText("Ty.\nSystem ma tylko pilnować,\nżeby tak zostało.", {
    x: M, y: 2.75, w: 7.7, h: 2.35, margin: 0,
    fontFace: H_FONT, fontSize: 32, bold: true, color: PAPER,
    lineSpacing: 44, valign: "top",
  });
  s.addText(
    "Każdy mechanizm z tej opowieści — bramy, odmowa, abstencja, korekta, hamulec, eksport — " +
    "służy jednemu kryterium: żeby po roku korzystania człowiek był bardziej samodzielny, " +
    "a nie bardziej związany.",
    {
      x: M, y: 5.25, w: 7.5, h: 1.05, margin: 0,
      fontFace: B_FONT, fontSize: 13.5, color: GREY_LT, lineSpacing: 21, valign: "top",
    }
  );
  chip(s, M, 6.5, "GEN-012", { w: 1.25, fill: GOLD });
  s.addText("github.com/dudsi101-svg/human-os", {
    x: M + 1.45, y: 6.5, w: 6.0, h: 0.28, margin: 0,
    fontFace: M_FONT, fontSize: 12, color: GREY_LT, valign: "middle",
  });

  s.addNotes("Klamra: wracamy do pytania ze slajdu 3. Odpowiedź jest jednozdaniowa i celowo " +
    "nie mówi o technologii.");
}

pres.writeFile({ fileName: OUT }).then(() => console.log("OK:", OUT));
