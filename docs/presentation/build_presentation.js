/**
 * Generator prezentacji "Human OS — konstytucyjny protokół i silnik referencyjny".
 *
 * Uruchomienie:  node docs/presentation/build_presentation.js
 * Wynik:         docs/presentation/Human-OS-prezentacja.pptx
 *
 * Źródła treści: README.md, constitution/README.md, genome.registry.json,
 * proof.rules.json, ECOSYSTEM.md, ROADMAP.md, hos_engine/*.py, docs/adr/*.
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

const H_FONT = "Cambria";
const B_FONT = "Calibri";
const M_FONT = "Courier New";

const W = 13.33;
const H = 7.5;
const M = 0.7; // margines

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Human OS Initiative";
pres.title = "Human OS — konstytucyjny protokół i silnik referencyjny";

/* -------------------------------------------------------------- pomocnicze */

// Motyw przewodni: identyfikator w monospace'owej „plakietce” (GEN-003, PROOF-004...)
function chip(slide, x, y, text, opts) {
  const o = opts || {};
  const w = o.w || 1.15;
  slide.addShape(pres.ShapeType.roundRect, {
    x, y, w, h: o.h || 0.28,
    rectRadius: 0.06,
    fill: { color: o.fill || GOLD },
    line: { color: o.fill || GOLD, width: 0 },
  });
  slide.addText(text, {
    x, y, w, h: o.h || 0.28,
    align: "center", valign: "middle", margin: 0,
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

/* ============================================================ 1. TYTUŁ === */
{
  const s = pres.addSlide();
  darkBg(s);

  // motyw warstw po prawej: pięć pasm architektury
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
  s.addText("Konstytucyjny protokół i silnik referencyjny", {
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

  s.addText("Protocol, Identity and Security  ·  wydanie 0.9.0  ·  sierpień 2026", {
    x: M, y: 6.4, w: 7.4, h: 0.35,
    fontFace: B_FONT, fontSize: 11, margin: 0,
    color: GREY_LT, valign: "middle",
  });

  s.addNotes(
    "Human OS to nie system operacyjny w potocznym sensie. To protokół konstytucyjny " +
    "wraz z referencyjną implementacją w Pythonie. Repozytorium jest silnikiem " +
    "referencyjnym — częścią szerszej inicjatywy, nie jej całością."
  );
}

/* ================================================ 2. CZYM JEST / NIE JEST = */
{
  const s = pres.addSlide();
  lightBg(s);
  title(s, "Czym jest — i czym nigdy nie będzie", false,
    "Obietnica systemu i jego jawne granice (Konstytucja, rozdz. 1)");

  const jest = [
    ["Protokół konstytucyjny", "Zestaw wiążących zasad, które system musi spełnić, zanim cokolwiek wykona."],
    ["Silnik referencyjny", "Wykonywalna implementacja tych zasad — testowalna, audytowalna, otwarta."],
    ["Warstwa suwerenności danych", "Pełny eksport, historia zmian, prawo wyjścia bez utraty dorobku."],
  ];
  const nie = [
    ["Wyrocznia", "Nie rozstrzyga, co jest słuszne w czyimś życiu."],
    ["Lekarz, terapeuta, doktryna", "Nie zastępuje profesjonalnej opieki ani systemu wartości."],
    ["Platforma uzależniająca", "Nie optymalizuje czasu w aplikacji i nie rankinguje ludzi."],
  ];

  s.addText("JEST", {
    x: M, y: 1.78, w: 5.9, h: 0.3, margin: 0,
    fontFace: B_FONT, fontSize: 13, bold: true, color: TEAL, charSpacing: 2,
  });
  s.addText("NIE JEST", {
    x: 6.95, y: 1.78, w: 5.7, h: 0.3, margin: 0,
    fontFace: B_FONT, fontSize: 13, bold: true, color: CRIMSON, charSpacing: 2,
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
  s.addNotes("Sześć zobowiązań i sześć jawnych zakazów tożsamościowych z Konstytucji 0.2.");
}

/* ================================================= 3. KRYTERIUM SUKCESU == */
{
  const s = pres.addSlide();
  darkBg(s);
  title(s, "Odwrotne kryterium sukcesu", true,
    "Nie wzrost zaangażowania, lecz spadek własnej niezbędności");

  chip(s, M, 2.05, "GEN-012", { w: 1.25, fill: GOLD });
  s.addText("Malejąca niezbędność systemu", {
    x: M + 1.45, y: 2.02, w: 6.2, h: 0.34, margin: 0,
    fontFace: B_FONT, fontSize: 13, bold: true, color: GREY_LT, valign: "middle",
  });

  s.addText("Human OS wygrywa wtedy,\ngdy jest coraz mniej potrzebny.", {
    x: M, y: 2.55, w: 7.7, h: 1.7, margin: 0,
    fontFace: H_FONT, fontSize: 30, bold: true, color: PAPER,
    lineSpacing: 40, valign: "top",
  });
  s.addText(
    "Sukces mierzy się spadkiem zależności od rozwiązań, które obniżają autonomię, " +
    "uwagę, energię, sprawczość twórczą, odpowiedzialność, jakość relacji lub " +
    "zgodność z własnymi wartościami użytkownika.",
    {
      x: M, y: 4.45, w: 7.5, h: 1.3, margin: 0,
      fontFace: B_FONT, fontSize: 14, color: GREY_LT, lineSpacing: 22, valign: "top",
    }
  );

  const stats = [
    ["↑", "Autonomia", "sprawczość i autorstwo decyzji"],
    ["↓", "Zależność", "od systemu i od mechanik uwagi"],
    ["→", "Wyjście", "pełny eksport, zawsze dostępny"],
  ];
  stats.forEach((st, i) => {
    const y = 1.95 + i * 1.55;
    card(s, 8.75, y, 3.88, 1.32, true);
    s.addText(st[0], {
      x: 8.98, y: y + 0.18, w: 0.6, h: 0.95, margin: 0,
      fontFace: "Arial", fontSize: 30, bold: true, color: GOLD,
      align: "center", valign: "middle",
    });
    s.addText(st[1], {
      x: 9.65, y: y + 0.24, w: 2.8, h: 0.34, margin: 0,
      fontFace: B_FONT, fontSize: 15, bold: true, color: PAPER, valign: "middle",
    });
    s.addText(st[2], {
      x: 9.65, y: y + 0.6, w: 2.85, h: 0.55, margin: 0,
      fontFace: B_FONT, fontSize: 11, color: GREY_LT, valign: "top",
    });
  });

  s.addNotes("Kryterium z README: „Human OS succeeds as dependence decreases…”.");
}

/* ==================================================== 4. ARCHITEKTURA ==== */
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
      fill: { color: l[3] },
      line: { color: l[3], width: 0 },
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
        fill: { color: "C9CEE0" }, line: { color: "C9CEE0", width: 0 },
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

/* ========================================================= 5. GENOM ====== */
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
    const hot = i === 11; // GEN-012 — wyróżniony
    s.addShape(pres.ShapeType.roundRect, {
      x, y, w: cw, h: 1.22,
      rectRadius: 0.05,
      fill: { color: hot ? INK : PAPER_ALT },
      line: { color: hot ? INK : "DFE3EE", width: 1 },
    });
    const id = "GEN-" + String(i + 1).padStart(3, "0");
    s.addText(id, {
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
  s.addNotes("GEN-012 wyróżniony, bo to jedyny gen, który każe systemowi dążyć do własnego zaniku.");
}

/* ==================================================== 6. PROOF KERNEL ==== */
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
    ["APPROVED", TEAL],
    ["APPROVED_WITH_LIMITS", "4F9AA8"],
    ["REQUIRES_CONSENT", GOLD],
    ["REQUIRES_HUMAN_DECISION", "C07A22"],
    ["REQUIRES_REDESIGN", "8A5A9E"],
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

/* =================================================== 7. PĘTLA WYKONAWCZA = */
{
  const s = pres.addSlide();
  lightBg(s);
  title(s, "Od intencji do poświadczenia", false,
    "ExecutionLoop.execute(HumanIntent) → ExecutionResult (ADR-CORE-002)");

  const steps = [
    "TOŻSAMOŚĆ", "ROLA", "ZGODA", "KONTEKST", "ENCJE",
    "KONSTYTUCJA", "AGENT", "POŚWIADCZENIE", "ZDARZENIE", "AUDYT",
  ];
  const cw = 2.28, gap = 0.22;
  steps.forEach((st, i) => {
    const c = i % 5, r = Math.floor(i / 5);
    const x = M + c * (cw + gap);
    const y = 1.95 + r * 1.35;
    const gate = i < 6;
    s.addShape(pres.ShapeType.roundRect, {
      x, y, w: cw, h: 1.05,
      rectRadius: 0.05,
      fill: { color: gate ? PAPER_ALT : CARD },
      line: { color: gate ? "C9CEE0" : "DFE3EE", width: 1 },
    });
    s.addShape(pres.ShapeType.ellipse, {
      x: x + 0.2, y: y + 0.2, w: 0.36, h: 0.36,
      fill: { color: gate ? INK : TEAL }, line: { color: gate ? INK : TEAL, width: 0 },
    });
    s.addText(String(i + 1), {
      x: x + 0.2, y: y + 0.2, w: 0.36, h: 0.36, margin: 0,
      align: "center", valign: "middle",
      fontFace: B_FONT, fontSize: 12, bold: true, color: PAPER,
    });
    s.addText(st, {
      x: x + 0.18, y: y + 0.62, w: cw - 0.36, h: 0.34, margin: 0,
      fontFace: B_FONT, fontSize: 12, bold: true, color: INK, valign: "middle",
    });
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: M, y: 4.8, w: W - 2 * M, h: 1.5,
    rectRadius: 0.05,
    fill: { color: INK }, line: { color: INK, width: 0 },
  });
  chip(s, M + 0.35, 5.05, "REFUSED_*", { w: 1.5, fill: GOLD });
  s.addText("Odmowa jest wynikiem pierwszej klasy — nigdy wyjątkiem.", {
    x: M + 2.05, y: 5.02, w: 9.2, h: 0.34, margin: 0,
    fontFace: B_FONT, fontSize: 15, bold: true, color: PAPER, valign: "middle",
  });
  s.addText(
    "Odrzucenie na dowolnej z sześciu pierwszych bram zatrzymuje pętlę, zanim cokolwiek " +
    "zostanie wykonane lub zapisane. Kroki 7–10 nie są opcjonalne: każde wykonanie zostawia " +
    "poświadczenie, zdarzenie na łańcuchu skrótów i ślad audytowy.",
    {
      x: M + 0.35, y: 5.45, w: 11.5, h: 0.75, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: GREY_LT, lineSpacing: 18, valign: "top",
    }
  );

  s.addNotes("Bramy 1–6 to twarde gate'y; runtime agentów ma dodatkową bramę zatwierdzenia przez człowieka.");
}

/* ====================================================== 8. RECOVERY ====== */
{
  const s = pres.addSlide();
  darkBg(s);
  title(s, "Sovereign Recovery Kernel", true,
    "Niezbywalne prawo właściciela do zatrzymania systemu — siedem trybów awaryjnych");

  const prot = [["SAFE_MODE", "R1"], ["READ_ONLY", "R1"], ["FREEZE", "R2"], ["DISCONNECT", "R2"]];
  const cons = [["ROLLBACK", "R3"], ["EXPORT", "R2"], ["RECOVERY", "R4"]];

  s.addText("TRYBY OCHRONNE", {
    x: M, y: 1.95, w: 5.9, h: 0.3, margin: 0,
    fontFace: B_FONT, fontSize: 12, bold: true, color: TEAL, charSpacing: 2,
  });
  s.addText("automatyczne tylko za powiadomieniem właściciela · zawsze odwracalne", {
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
  s.addText("wyłącznie ręcznie · ROLLBACK i RECOVERY wymagają drugiego klucza", {
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
    ["Brak API do zmiany polityki", "Agent nie wyłączy tego, co nie ma settera."],
    ["Agent nigdy nie aktywuje", "AGENT, SERVICE i SYSTEM_PROCESS dostają odmowę — a sama odmowa jest logowana."],
    ["Zero zależności od AI", "Warstwa ratunkowa działa bez modelu i bez sieci."],
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

  s.addNotes("R1–R4 to skala ryzyka Konstytucji. Odmowa jest tu wyjątkiem (RecoveryRefused) — " +
    "zignorowana ochrona nie może wyglądać jak ochrona działająca.");
}

/* ================================================ 9. DECISION ENGINE ===== */
{
  const s = pres.addSlide();
  lightBg(s);
  title(s, "Silnik decyzji: bramy przed rankingiem", false,
    "Warstwa 5 — dziewięć twardych bram G0–G8 działa, zanim cokolwiek zostanie uszeregowane");

  card(s, M, 1.9, 6.05, 2.35, false);
  s.addText("Nieprzemienność", {
    x: M + 0.3, y: 2.08, w: 5.4, h: 0.34, margin: 0,
    fontFace: B_FONT, fontSize: 15, bold: true, color: INK, valign: "middle",
  });
  s.addText(
    "Kandydat odrzucony przez bramę nie wraca do gry później, nawet z wysokim wynikiem. " +
    "Kolejność bram i rankingu nie jest wymienna.",
    {
      x: M + 0.3, y: 2.48, w: 5.4, h: 0.85, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: GREY, lineSpacing: 18, valign: "top",
    }
  );
  ["G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8"].forEach((g, i) => {
    chip(s, M + 0.3 + i * 0.63, 3.5, g, { w: 0.55, fill: INK, color: PAPER, fontSize: 10 });
  });

  card(s, M, 4.45, 6.05, 2.2, false);
  s.addText("Asymetria dowodowa", {
    x: M + 0.3, y: 4.63, w: 5.4, h: 0.34, margin: 0,
    fontFace: B_FONT, fontSize: 15, bold: true, color: INK, valign: "middle",
  });
  s.addText(
    "Im wyższa klasa ryzyka, tym wyższy próg wymaganego dowodu (skala 0–5). " +
    "Klasa R-KRYTYCZNE nie jest dopuszczalna w żadnym wariancie.",
    {
      x: M + 0.3, y: 5.03, w: 5.4, h: 0.9, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: GREY, lineSpacing: 18, valign: "top",
    }
  );
  chip(s, M + 0.3, 6.05, "R-KRYTYCZNE", { w: 1.75, fill: CRIMSON, color: PAPER });
  s.addText("nigdy dopuszczalne", {
    x: M + 2.2, y: 6.05, w: 3.4, h: 0.28, margin: 0,
    fontFace: B_FONT, fontSize: 12, italic: true, color: CRIMSON, valign: "middle",
  });

  const rights = [
    ["Abstencja jest wynikiem", "Osiem nazwanych powodów wstrzymania się od rekomendacji — nie awaria, tylko odpowiedź."],
    ["Eskalacja trójstopniowa", "Miękka, warunkowa i twarda — decyzja wraca do człowieka, gdy przekracza kompetencje systemu."],
    ["Dwie niezmienności w kodzie", "Pole „user_determination” nie jest czytane przez nic. Pole „sponsored” nie istnieje w kluczu rankingu."],
  ];
  rights.forEach((r, i) => {
    const y = 1.9 + i * 1.63;
    card(s, 7.15, y, 5.48, 1.42, false);
    s.addText(r[0], {
      x: 7.45, y: y + 0.16, w: 4.9, h: 0.34, margin: 0,
      fontFace: B_FONT, fontSize: 15, bold: true, color: TEAL, valign: "middle",
    });
    s.addText(r[1], {
      x: 7.45, y: y + 0.54, w: 4.9, h: 0.75, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: GREY, lineSpacing: 18, valign: "top",
    });
  });

  s.addNotes("ADR-DECISION-001..005; implementacja hos_engine/decision_engine.py. " +
    "Sponsorowanie i etykiety użytkownika są strukturalnie odcięte od rankingu.");
}

/* ================================================ 10. SELF MODEL ========= */
{
  const s = pres.addSlide();
  lightBg(s);
  title(s, "Żywy model siebie", false,
    "Rozmowa nigdy nie staje się faktem automatycznie (ADR-SELFMODEL-001)");

  const kinds = [
    ["DEKLARACJA", "Użytkownik powiedział to wprost o sobie.", TEAL, PAPER],
    ["OBSERWACJA", "System zauważył wzorzec w danych, które mu powierzono.", "4F9AA8", PAPER],
    ["HIPOTEZA", "Domysł — wymaga wskazania dowodu i nigdy nie jest podawany jak fakt.", GOLD, INK],
  ];
  kinds.forEach((k, i) => {
    const x = M + i * 4.03;
    card(s, x, 1.95, 3.83, 1.62, false);
    chip(s, x + 0.28, 2.18, k[0], { w: 1.5, fill: k[2], color: k[3] });
    s.addText(k[1], {
      x: x + 0.28, y: 2.62, w: 3.3, h: 1.0, margin: 0,
      fontFace: B_FONT, fontSize: 12.5, color: GREY, lineSpacing: 18, valign: "top",
    });
  });

  const rules = [
    ["Tylko użytkownik potwierdza", "Potwierdzenie, odrzucenie i korekta są wyłącznie w jego rękach."],
    ["Historia nigdy nie znika", "Zmiana tworzy nową wersję przez łańcuch „supersedes”; odrzucenie oznacza CONTESTED, nie usunięcie."],
    ["Sprzeczność to sygnał", "Napięcie między zapisami jest zachowywane; rozstrzyga je tylko osoba, której dotyczy."],
    ["Pełna proweniencja: why()", "Dla każdego zapisu: cytat, autor, pasmo pewności i cała historia zmian."],
  ];
  rules.forEach((r, i) => {
    const c = i % 2, row = Math.floor(i / 2);
    const x = M + c * 6.13;
    const y = 4.1 + row * 1.32;
    bullet(s, x, y + 0.05, INK, String(i + 1));
    s.addText(r[0], {
      x: x + 0.45, y, w: 5.4, h: 0.34, margin: 0,
      fontFace: B_FONT, fontSize: 14, bold: true, color: INK, valign: "middle",
    });
    s.addText(r[1], {
      x: x + 0.45, y: y + 0.36, w: 5.35, h: 0.75, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: GREY, lineSpacing: 18, valign: "top",
    });
  });

  footer(s, "Silnik nie zawiera NLP — rozpoznawanie kandydatów na zapisy to zadanie aplikacji, nie jądra.");
  s.addNotes("Pasma pewności pokazywane są jako LOW/MEDIUM/HIGH, nigdy jako surowa liczba.");
}

/* ============================================== 11. BEZPIECZEŃSTWO ======= */
{
  const s = pres.addSlide();
  lightBg(s);
  title(s, "Bezpieczeństwo i dojrzałość", false,
    "Co już działa — i czego świadomie jeszcze nie ma");

  const have = [
    ["Podpisane koperty HOSP/0.2", "kanoniczny JSON, HMAC, znacznik protokołu"],
    ["Rejestr tożsamości i kluczy", "rotacja kluczy, powiązanie klucza z tożsamością"],
    ["ReplayGuard", "nonce, wygasanie, śledzenie identyfikatorów komunikatów"],
    ["Jawne polityki zaufania", "TrustLevel i TrustPolicy zamiast domyślnego zaufania"],
    ["Security Gateway", "dziesięciokrokowy potok kontroli przed wykonaniem"],
    ["Łańcuch skrótów SHA-256", "weryfikowalna integralność dziennika zdarzeń"],
  ];
  have.forEach((h, i) => {
    const c = i % 2, r = Math.floor(i / 2);
    const x = M + c * 3.95;
    const y = 1.95 + r * 1.5;
    card(s, x, y, 3.75, 1.28, false);
    s.addText(h[0], {
      x: x + 0.25, y: y + 0.24, w: 3.3, h: 0.32, margin: 0,
      fontFace: B_FONT, fontSize: 13, bold: true, color: INK, valign: "middle",
    });
    s.addText(h[1], {
      x: x + 0.25, y: y + 0.6, w: 3.3, h: 0.55, margin: 0,
      fontFace: B_FONT, fontSize: 11, color: GREY, valign: "top",
    });
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: 8.75, y: 1.95, w: 3.88, h: 4.4,
    rectRadius: 0.05,
    fill: { color: CRIMSON }, line: { color: CRIMSON, width: 0 },
  });
  s.addText("Nie jest produkcyjne", {
    x: 9.05, y: 2.18, w: 3.3, h: 0.4, margin: 0,
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
      x: 9.05, y: 2.7, w: 3.3, h: 2.9, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: PAPER,
      paraSpaceAfter: 8, valign: "top",
    }
  );
  s.addText("security/THREAT_MODEL.md", {
    x: 9.05, y: 5.78, w: 3.3, h: 0.3, margin: 0,
    fontFace: M_FONT, fontSize: 10, color: "F2C9CB", valign: "middle",
  });

  s.addNotes("Uczciwość co do dojrzałości jest sama w sobie wymogiem konstytucyjnym " +
    "(GEN-015, transparentność wpływu i ograniczeń).");
}

/* ================================================= 12. STAN W LICZBACH == */
{
  const s = pres.addSlide();
  darkBg(s);
  title(s, "Stan implementacji", true, "Silnik referencyjny, stan na sierpień 2026");

  const stats = [
    ["36", "modułów silnika", "hos_engine/"],
    ["166", "testów automatycznych", "Python 3.11 / 3.12 / 3.13"],
    ["9", "testów konstytucyjnych", "Proof Kernel"],
    ["15", "genów konstytucyjnych", "genome.registry.json"],
    ["14", "schematów JSON", "Draft 2020-12"],
    ["67", "rekordów decyzji (ADR)", "docs/adr/"],
  ];
  stats.forEach((st, i) => {
    const c = i % 3, r = Math.floor(i / 3);
    const x = M + c * 4.03;
    const y = 2.05 + r * 2.15;
    card(s, x, y, 3.83, 1.85, true);
    s.addText(st[0], {
      x: x + 0.3, y: y + 0.18, w: 3.2, h: 0.85, margin: 0,
      fontFace: H_FONT, fontSize: 48, bold: true, color: GOLD, valign: "middle",
    });
    s.addText(st[1], {
      x: x + 0.3, y: y + 1.05, w: 3.25, h: 0.34, margin: 0,
      fontFace: B_FONT, fontSize: 14, bold: true, color: PAPER, valign: "middle",
    });
    s.addText(st[2], {
      x: x + 0.3, y: y + 1.38, w: 3.25, h: 0.3, margin: 0,
      fontFace: M_FONT, fontSize: 10, color: GREY_LT, valign: "middle",
    });
  });

  footer(s, "Zerowy dług mypy w silniku. CI: ruff + pytest na trzech wersjach Pythona.");
  s.addNotes("Liczby policzone z repozytorium: moduły, metody testowe, schematy, ADR-y.");
}

/* ==================================================== 13. ROADMAPA ======= */
{
  const s = pres.addSlide();
  lightBg(s);
  title(s, "Droga do 1.0", false, "Osiem etapów zamkniętych, jeden otwarty, jeden przed nami");

  const done = [
    ["0.1", "Formalny rdzeń"], ["0.2", "Specyfikacja maszynowa"], ["0.3", "Silnik polityk"],
    ["0.4", "Trwały i audytowalny rdzeń"], ["0.5", "Graf wiedzy i proweniencja"],
    ["0.6", "Runtime agentów i granice"], ["0.7", "Symulacje i scenariusze"],
    ["0.8", "Model człowieka i zgoda"],
  ];

  done.forEach((d, i) => {
    const c = i % 4, r = Math.floor(i / 4);
    const x = M + c * 3.03;
    const y = 1.95 + r * 0.95;
    s.addShape(pres.ShapeType.roundRect, {
      x, y, w: 2.85, h: 0.78,
      rectRadius: 0.05,
      fill: { color: PAPER_ALT }, line: { color: "DFE3EE", width: 1 },
    });
    s.addText(d[0], {
      x: x + 0.2, y, w: 0.55, h: 0.78, margin: 0,
      fontFace: M_FONT, fontSize: 13, bold: true, color: TEAL, valign: "middle",
    });
    s.addText(d[1], {
      x: x + 0.8, y, w: 1.95, h: 0.78, margin: 0,
      fontFace: B_FONT, fontSize: 11.5, color: INK, valign: "middle",
    });
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: M, y: 4.0, w: 11.93, h: 1.15,
    rectRadius: 0.05,
    fill: { color: GOLD }, line: { color: GOLD, width: 0 },
  });
  s.addText("0.9", {
    x: M + 0.3, y: 4.0, w: 0.8, h: 1.15, margin: 0,
    fontFace: M_FONT, fontSize: 24, bold: true, color: INK, valign: "middle",
  });
  s.addText("Interoperacyjność protokołu i przegląd bezpieczeństwa — OTWARTE", {
    x: M + 1.15, y: 4.16, w: 10.4, h: 0.36, margin: 0,
    fontFace: B_FONT, fontSize: 15, bold: true, color: INK, valign: "middle",
  });
  s.addText(
    "Warstwy wykonawcze i plastry warstw 2–6 powstały równolegle do tej osi i nie zastępują punktu 0.9.",
    {
      x: M + 1.15, y: 4.54, w: 10.4, h: 0.4, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: "5A4212", valign: "middle",
    }
  );

  s.addShape(pres.ShapeType.roundRect, {
    x: M, y: 5.35, w: 11.93, h: 1.15,
    rectRadius: 0.05,
    fill: { color: INK }, line: { color: INK, width: 0 },
  });
  s.addText("1.0", {
    x: M + 0.3, y: 5.35, w: 0.8, h: 1.15, margin: 0,
    fontFace: M_FONT, fontSize: 24, bold: true, color: GOLD, valign: "middle",
  });
  s.addText("Stabilny protokół, silnik i runtime referencyjny", {
    x: M + 1.15, y: 5.5, w: 10.4, h: 0.36, margin: 0,
    fontFace: B_FONT, fontSize: 15, bold: true, color: PAPER, valign: "middle",
  });
  s.addText(
    "Warunki: stabilna Konstytucja i model obiektów · wersjonowany protokół · migracje · udokumentowany " +
    "przegląd bezpieczeństwa · pełna przenośność danych · mierzalna możliwość wyjścia.",
    {
      x: M + 1.15, y: 5.88, w: 10.4, h: 0.45, margin: 0,
      fontFace: B_FONT, fontSize: 11.5, color: GREY_LT, valign: "middle",
    }
  );

  s.addNotes("ROADMAP.md; kryterium 0.9 zmienione decyzją foundera 2026-08-17 (DD-008).");
}

/* ==================================================== 14. ZAMKNIĘCIE ===== */
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

  s.addText("System, który chce być\ncoraz mniej potrzebny.", {
    x: M, y: 2.3, w: 7.6, h: 1.7, margin: 0,
    fontFace: H_FONT, fontSize: 40, bold: true, color: PAPER,
    lineSpacing: 50, valign: "middle",
  });
  s.addText(
    "Human OS mierzy się nie tym, jak długo ktoś w nim zostaje, lecz tym, ile autonomii " +
    "z niego wynosi. Każdy mechanizm w tym repozytorium — bramy, poświadczenia, tryby " +
    "awaryjne, eksport — służy temu jednemu kryterium.",
    {
      x: M, y: 4.15, w: 7.4, h: 1.2, margin: 0,
      fontFace: B_FONT, fontSize: 14, color: GREY_LT, lineSpacing: 22, valign: "top",
    }
  );
  chip(s, M, 5.6, "GEN-012", { w: 1.25, fill: GOLD });
  s.addText("github.com/dudsi101-svg/human-os", {
    x: M + 1.45, y: 5.6, w: 6.0, h: 0.28, margin: 0,
    fontFace: M_FONT, fontSize: 12, color: GREY_LT, valign: "middle",
  });

  s.addNotes("Slajd zamykający: wracamy do kryterium sukcesu ze slajdu 3.");
}

pres.writeFile({ fileName: OUT }).then(() => console.log("OK:", OUT));
