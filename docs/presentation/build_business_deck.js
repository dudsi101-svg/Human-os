/**
 * Generator prezentacji biznesowej "Human OS — zasady, które da się wykonać".
 *
 * Uruchomienie:  node docs/presentation/build_business_deck.js
 * Wynik:         docs/presentation/Human-OS-prezentacja-biznesowa.pptx
 *                (PDF powstaje z niego konwersją — patrz README.md)
 *
 * Rejestr: język prosty, bez żargonu i bez kodów wewnętrznych na slajdach.
 * Dokument świadomie nie zawiera prognoz rynkowych ani danych finansowych —
 * nie ma dla nich podstaw w repozytorium.
 *
 * Źródła treści: README.md, constitution/README.md, ECOSYSTEM.md, ROADMAP.md,
 * GOVERNANCE.md, CONTRIBUTING.md, SECURITY.md, LICENSE-DECISION.md,
 * security/THREAT_MODEL.md, genome.registry.json, proof.rules.json,
 * hos_engine/*.py, docs/adr/*, docs/white_paper/*.
 */

const pptxgen = require("pptxgenjs");
const path = require("path");

const OUT = path.join(__dirname, "Human-OS-prezentacja-biznesowa.pptx");

/* ---------------------------------------------------------------- paleta */

const INK = "0F1533";
const INK_SOFT = "1B2450";
const INK_LINE = "2B3563";
const PAPER = "FFFFFF";
const PAPER_ALT = "F2F4FA";
const GOLD = "D99A2B";
const TEAL = "2F7D8E";
const TEAL_LT = "4F9AA8";
const CRIMSON = "9E2B32";
const GREY = "5B6280";
const GREY_LT = "9AA0B8";
const DIM = "C9CEE0";

const H_FONT = "Cambria";
const B_FONT = "Calibri";
const M_FONT = "Courier New";

const W = 13.33;
const H = 7.5;
const M = 0.7;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Human OS Initiative";
pres.title = "Human OS — zasady, które da się wykonać";

let page = 0; // numeracja stron w PDF

/* ------------------------------------------------------------- pomocnicze */

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
    fontFace: o.mono === false ? B_FONT : M_FONT,
    fontSize: o.fontSize || 10, bold: true,
    color: o.color || INK,
  });
}

function card(slide, x, y, w, h, dark) {
  slide.addShape(pres.ShapeType.roundRect, {
    x, y, w, h,
    rectRadius: 0.04,
    fill: { color: dark ? INK_SOFT : PAPER },
    line: { color: dark ? INK_LINE : "DFE3EE", width: 1 },
    shadow: dark ? undefined : { type: "outer", angle: 90, blur: 8, offset: 1, color: "9AA0B8", opacity: 0.18 },
  });
}

function bullet(slide, x, y, color, glyph) {
  slide.addShape(pres.ShapeType.ellipse, {
    x, y, w: 0.3, h: 0.3,
    fill: { color }, line: { color, width: 0 },
  });
  slide.addText(glyph, {
    x, y, w: 0.3, h: 0.3,
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 12, bold: true, color: PAPER,
  });
}

// Stopka strony — w PDF-ie czyta się to jak dokument, nie jak slajdy.
function pageFoot(slide, dark) {
  page += 1;
  const c = dark ? INK_LINE : DIM;
  slide.addText("Human OS · protokół i silnik referencyjny · wersja 0.9.0 BETA", {
    x: M, y: H - 0.48, w: 8.0, h: 0.28, margin: 0,
    fontFace: B_FONT, fontSize: 9, color: c, valign: "middle",
  });
  slide.addText(String(page), {
    x: W - M - 1.0, y: H - 0.48, w: 1.0, h: 0.28, margin: 0,
    align: "right", margin: 0,
    fontFace: M_FONT, fontSize: 9, color: c, valign: "middle",
  });
}

function slide(dark) {
  const s = pres.addSlide();
  s.background = { color: dark ? INK : PAPER };
  return s;
}

function title(s, text, dark, sub) {
  s.addText(text, {
    x: M, y: 0.5, w: W - 2 * M, h: 0.72,
    fontFace: H_FONT, fontSize: 34, bold: true, margin: 0,
    color: dark ? PAPER : INK, valign: "middle",
  });
  if (sub) {
    s.addText(sub, {
      x: M, y: 1.24, w: W - 2 * M, h: 0.36,
      fontFace: B_FONT, fontSize: 14, margin: 0,
      color: dark ? GREY_LT : GREY, valign: "middle",
    });
  }
}

function note(s, text, dark) {
  s.addText(text, {
    x: M, y: H - 1.02, w: W - 2 * M, h: 0.42, margin: 0,
    fontFace: B_FONT, fontSize: 10.5, italic: true,
    color: dark ? GREY_LT : GREY_LT, valign: "middle",
  });
}

/* ================================================== 1. OKŁADKA ========== */
{
  const s = slide(true);

  s.addText("Human OS", {
    x: M, y: 2.15, w: 8.2, h: 1.15, margin: 0,
    fontFace: H_FONT, fontSize: 58, bold: true, color: PAPER, valign: "middle",
  });
  s.addText("Zasady, których nie da się ominąć — bo są wykonywane, nie deklarowane", {
    x: M, y: 3.35, w: 8.0, h: 0.85, margin: 0,
    fontFace: B_FONT, fontSize: 20, color: GOLD, lineSpacing: 30, valign: "top",
  });
  s.addText(
    "Dokument przeglądowy dla osób decyzyjnych, partnerów i zespołów, które rozważają " +
    "oparcie własnego produktu na Human OS. Bez żargonu, za to konkretnie: co to jest, " +
    "co już działa, czego jeszcze nie ma i na jakich zasadach można z tego korzystać.",
    {
      x: M, y: 4.4, w: 7.9, h: 1.4, margin: 0,
      fontFace: B_FONT, fontSize: 14, color: GREY_LT, lineSpacing: 24, valign: "top",
    }
  );

  chip(s, M, 5.95, "wersja 0.9.0", { w: 1.6, fill: GOLD, mono: false, fontSize: 10.5 });
  chip(s, 2.45, 5.95, "status: BETA", { w: 1.6, fill: INK_SOFT, color: PAPER, mono: false, fontSize: 10.5 });
  chip(s, 4.2, 5.95, "sierpień 2026", { w: 1.7, fill: INK_SOFT, color: PAPER, mono: false, fontSize: 10.5 });

  // znak graficzny: warstwy systemu
  const bands = ["Aplikacje", "Integracje i Hub", "Silnik", "Specyfikacja", "Konstytucja"];
  bands.forEach((b, i) => {
    const y = 1.5 + i * 0.86;
    const inset = i * 0.17;
    s.addShape(pres.ShapeType.roundRect, {
      x: 9.35 + inset, y, w: 3.28 - 2 * inset, h: 0.66,
      rectRadius: 0.05,
      fill: { color: i === 4 ? GOLD : INK_SOFT },
      line: { color: i === 4 ? GOLD : INK_LINE, width: 1 },
    });
    s.addText(b, {
      x: 9.35 + inset, y, w: 3.28 - 2 * inset, h: 0.66,
      align: "center", valign: "middle", margin: 0,
      fontFace: B_FONT, fontSize: 12.5, bold: true,
      color: i === 4 ? INK : PAPER,
    });
  });
  s.addText("każda warstwa niżej musi mieścić się w regułach warstwy wyżej", {
    x: 9.0, y: 5.95, w: 3.95, h: 0.6, margin: 0,
    align: "center",
    fontFace: B_FONT, fontSize: 10.5, italic: true, color: GREY_LT, valign: "top",
  });

  pageFoot(s, true);
}

/* ================================================== 2. STRESZCZENIE ===== */
{
  const s = slide(false);
  title(s, "Human OS w jednym akapicie", false,
    "Jeśli miałbyś przeczytać tylko jedną stronę, to tę");

  card(s, M, 1.85, 7.55, 2.25, false);
  s.addText(
    "Human OS to spisany zestaw zasad, jak oprogramowanie może traktować człowieka — " +
    "oraz działający silnik, który sprawdza każde zaplanowane działanie wobec tych zasad, " +
    "zanim ono nastąpi. Zasady nie są dodatkiem do produktu; są bramką, przez którą " +
    "produkt musi przejść.",
    {
      x: M + 0.4, y: 2.15, w: 6.85, h: 1.8, margin: 0,
      fontFace: H_FONT, fontSize: 15.5, color: INK, lineSpacing: 26, valign: "top",
    }
  );

  const facts = [
    ["To nie system operacyjny", "Mimo nazwy — warstwa reguł do wbudowania w istniejący produkt."],
    ["To nie gotowy produkt", "Wersja beta. Nie nadaje się dziś do wdrożenia produkcyjnego."],
    ["Cel jest nietypowy", "Ma być coraz mniej potrzebny, im samodzielniejszy użytkownik."],
  ];
  facts.forEach((f, i) => {
    const y = 4.4 + i * 0.7;
    bullet(s, M, y, TEAL, String(i + 1));
    s.addText(f[0], {
      x: M + 0.45, y, w: 2.9, h: 0.3, margin: 0,
      fontFace: B_FONT, fontSize: 13, bold: true, color: INK, valign: "middle",
    });
    s.addText(f[1], {
      x: M + 3.45, y, w: 4.2, h: 0.44, margin: 0,
      fontFace: B_FONT, fontSize: 11.5, color: GREY, lineSpacing: 16, valign: "top",
    });
  });

  card(s, 8.6, 1.85, 4.03, 4.6, false);
  s.addText("Trzy zdania, które warto zapamiętać", {
    x: 8.9, y: 2.1, w: 3.45, h: 0.7, margin: 0,
    fontFace: B_FONT, fontSize: 15, bold: true, color: INK, valign: "top",
  });
  const quotes = [
    "Reguła zapisana w dokumencie jest deklaracją. Reguła zapisana w silniku jest warunkiem.",
    "Odmowa systemu to poprawna odpowiedź, a nie awaria.",
    "Możliwość odejścia z całym dorobkiem jest częścią umowy, nie uprzejmością.",
  ];
  quotes.forEach((q, i) => {
    const y = 2.95 + i * 1.15;
    s.addText(q, {
      x: 8.9, y, w: 3.45, h: 1.0, margin: 0,
      fontFace: B_FONT, fontSize: 12.5, italic: true, color: GREY, lineSpacing: 19, valign: "top",
    });
  });

  note(s, "Dokument nie zawiera prognoz rynkowych ani danych finansowych — nie ma dla nich podstaw w repozytorium.", false);
  pageFoot(s, false);
}

/* ================================================== 3. PROBLEM ========== */
{
  const s = slide(false);
  title(s, "Problem, który wszyscy znamy", false,
    "Nie chodzi o złe intencje twórców oprogramowania, tylko o to, co jest mierzone");

  const rows = [
    ["Decyzje przesuwają się do systemu",
     "Coraz więcej drobnych wyborów — co przeczytasz, co zobaczysz, kiedy przerwiesz pracę — " +
     "podejmuje algorytm. Każdy z osobna jest nieszkodliwy. Razem układają się w czyjś scenariusz dnia."],
    ["Zasady etyczne żyją osobno od kodu",
     "Deklaracje o odpowiedzialnej technologii zwykle są dokumentem PDF, a nie warunkiem, " +
     "który musi spełnić konkretne żądanie w konkretnym momencie. Nikt ich nie egzekwuje w czasie działania."],
    ["Wyjście bywa teoretyczne",
     "Eksport danych często oznacza worek plików bez kontekstu, bez historii i bez powodów, " +
     "dla których system podjął takie, a nie inne decyzje. Formalnie można odejść. Praktycznie — trudno."],
  ];
  rows.forEach((r, i) => {
    const y = 1.9 + i * 1.55;
    card(s, M, y, 11.93, 1.35, false);
    bullet(s, M + 0.35, y + 0.2, CRIMSON, "!");
    s.addText(r[0], {
      x: M + 0.85, y: y + 0.16, w: 3.5, h: 0.4, margin: 0,
      fontFace: B_FONT, fontSize: 15, bold: true, color: INK, valign: "middle",
    });
    s.addText(r[1], {
      x: M + 4.5, y: y + 0.18, w: 7.05, h: 1.0, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: GREY, lineSpacing: 18, valign: "top",
    });
  });

  note(s, "To opis jakościowy. Świadomie nie podajemy tu statystyk — nie mamy własnych badań, na które moglibyśmy się powołać.", false);
  pageFoot(s, false);
}

/* ================================================== 4. POMYSŁ =========== */
{
  const s = slide(true);
  title(s, "Pomysł: reguły, które da się wykonać", true,
    "Ta sama zmiana, którą przeszły kiedyś testy jednostkowe i kontrola wersji");

  s.addText(
    "Weź zasady, które zwykle zostają na poziomie deklaracji — autonomia człowieka, świadoma " +
    "zgoda, odwracalność, prawo wyjścia — i zapisz je w formie, którą maszyna potrafi sprawdzić " +
    "przed wykonaniem działania.",
    {
      x: M, y: 1.95, w: 6.3, h: 1.6, margin: 0,
      fontFace: B_FONT, fontSize: 15, color: PAPER, lineSpacing: 26, valign: "top",
    }
  );
  s.addText(
    "Od tego momentu „system nie powinien tego robić” przestaje być opinią, a staje się " +
    "warunkiem, którego niespełnienie zatrzymuje działanie — i zostawia po sobie ślad.",
    {
      x: M, y: 3.65, w: 6.3, h: 1.4, margin: 0,
      fontFace: B_FONT, fontSize: 15, italic: true, color: GOLD, lineSpacing: 26, valign: "top",
    }
  );

  const before = ["zasady w dokumencie", "zgodność sprawdzana po fakcie", "„zaufaj nam”"];
  const after = ["zasady w silniku", "warunek przed wykonaniem", "sprawdź sam — kod jest otwarty"];

  s.addText("ZWYKLE", {
    x: 7.4, y: 1.95, w: 2.4, h: 0.3, margin: 0,
    fontFace: B_FONT, fontSize: 11, bold: true, color: GREY_LT, charSpacing: 2,
  });
  s.addText("TUTAJ", {
    x: 10.3, y: 1.95, w: 2.4, h: 0.3, margin: 0,
    fontFace: B_FONT, fontSize: 11, bold: true, color: GOLD, charSpacing: 2,
  });
  before.forEach((b, i) => {
    const y = 2.45 + i * 1.25;
    card(s, 7.4, y, 2.55, 1.05, true);
    s.addText(b, {
      x: 7.6, y, w: 2.15, h: 1.05, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: GREY_LT, valign: "middle",
    });
    s.addShape(pres.ShapeType.triangle, {
      x: 10.02, y: y + 0.44, w: 0.2, h: 0.18,
      fill: { color: GOLD }, line: { color: GOLD, width: 0 }, rotate: 90,
    });
    s.addShape(pres.ShapeType.roundRect, {
      x: 10.3, y, w: 2.33, h: 1.05,
      rectRadius: 0.05,
      fill: { color: GOLD }, line: { color: GOLD, width: 0 },
    });
    s.addText(after[i], {
      x: 10.5, y, w: 1.95, h: 1.05, margin: 0,
      fontFace: B_FONT, fontSize: 12, bold: true, color: INK, valign: "middle",
    });
  });

  note(s, "Nazwa własna tego mechanizmu w projekcie to Proof Kernel — dalej opisujemy go po ludzku, bez kodów.", true);
  pageFoot(s, true);
}

/* ================================================== 5. DLA CZŁOWIEKA ==== */
{
  const s = slide(false);
  title(s, "Co z tego ma człowiek", false,
    "Cztery rzeczy, które użytkownik odczuwa w praktyce, a nie tylko czyta w regulaminie");

  const items = [
    ["Wie, skąd system coś o nim wie",
     "Przy każdym zapisie widać, czy to jego własne słowa, obserwacja systemu, czy tylko domysł — " +
     "razem z cytatem i historią zmian."],
    ["Nie jest oceniany rankingiem",
     "System nie porządkuje ludzi i nie sprzedaje pozycji w rekomendacjach. Gdy dane są sprzeczne, " +
     "mówi „wstrzymuję się” zamiast zgadywać."],
    ["Może zatrzymać wszystko",
     "Zestaw trybów awaryjnych — od zamrożenia po odcięcie — działa bez modelu AI i bez sieci, " +
     "a żaden automat nie może ich wyłączyć."],
    ["Może odejść z całym dorobkiem",
     "Eksport obejmuje dane, powiązania, historię wersji i ślad decyzji — w otwartym formacie, " +
     "nie w worku plików."],
  ];
  items.forEach((it, i) => {
    const c = i % 2, r = Math.floor(i / 2);
    const x = M + c * 6.13;
    const y = 1.9 + r * 2.35;
    card(s, x, y, 5.8, 2.05, false);
    bullet(s, x + 0.35, y + 0.28, TEAL, "✓");
    s.addText(it[0], {
      x: x + 0.85, y: y + 0.24, w: 4.6, h: 0.4, margin: 0,
      fontFace: B_FONT, fontSize: 15.5, bold: true, color: INK, valign: "middle",
    });
    s.addText(it[1], {
      x: x + 0.85, y: y + 0.72, w: 4.6, h: 1.15, margin: 0,
      fontFace: B_FONT, fontSize: 12.5, color: GREY, lineSpacing: 19, valign: "top",
    });
  });

  pageFoot(s, false);
}

/* ================================================== 6. DLA FIRMY ======== */
{
  const s = slide(false);
  title(s, "Co z tego ma organizacja", false,
    "Co zyskuje zespół, który buduje produkt na tej warstwie");

  const items = [
    ["Polityka jako dane, nie jako slajd",
     "Reguły są zapisane w plikach, które czyta silnik. Zmiana reguły jest zmianą w repozytorium — " +
     "z historią, autorem i przeglądem."],
    ["Ślad, który da się pokazać",
     "Każde wykonane działanie zostawia poświadczenie i wpis w dzienniku spiętym łańcuchem skrótów. " +
     "Manipulacja przy historii jest wykrywalna."],
    ["Gotowe testy zgodności",
     "Dziewięć testów konstytucyjnych i zestaw testów automatycznych są częścią repozytorium — " +
     "nie trzeba wymyślać własnego rozumienia zgodności."],
    ["Mniejsze ryzyko sporu o dane",
     "Zgoda ma cel, zakres i czas; wyjście jest zaprojektowane od początku. To ułatwia wykazanie, " +
     "jak system zachował się w konkretnej sprawie."],
  ];
  items.forEach((it, i) => {
    const c = i % 2, r = Math.floor(i / 2);
    const x = M + c * 6.13;
    const y = 1.9 + r * 2.15;
    card(s, x, y, 5.8, 1.9, false);
    bullet(s, x + 0.35, y + 0.26, INK, String(i + 1));
    s.addText(it[0], {
      x: x + 0.85, y: y + 0.22, w: 4.6, h: 0.4, margin: 0,
      fontFace: B_FONT, fontSize: 15.5, bold: true, color: INK, valign: "middle",
    });
    s.addText(it[1], {
      x: x + 0.85, y: y + 0.68, w: 4.6, h: 1.05, margin: 0,
      fontFace: B_FONT, fontSize: 12.5, color: GREY, lineSpacing: 19, valign: "top",
    });
  });

  note(s, "To nie jest opinia prawna ani deklaracja zgodności z konkretną regulacją. Human OS dostarcza mechanizmy i dowody, nie certyfikaty.", false);
  pageFoot(s, false);
}

/* ================================================== 7. WIDOK Z GÓRY ===== */
{
  const s = slide(false);
  title(s, "Jak to działa — widok z góry", false,
    "Droga jednego żądania: od prośby człowieka do zapisanego śladu");

  const steps = [
    ["Prośba", "Człowiek mówi, czego chce. To jedyny punkt wejścia — system nie zaczyna sam z siebie.", TEAL],
    ["Bramy", "Kto pyta, w jakiej roli, na co ma zgodę i jakich danych dotyczy sprawa.", TEAL],
    ["Test zasad", "Dziewięć pytań kontrolnych. Wynik to jedna z sześciu możliwych odpowiedzi.", GOLD],
    ["Wykonanie", "Dopiero teraz — i tylko w granicach, które wyznaczył test.", TEAL_LT],
    ["Ślad", "Poświadczenie, wpis w dzienniku, zapis w audycie. Bez wyjątków.", INK],
  ];
  steps.forEach((st, i) => {
    const x = M + i * 2.44;
    const w = 2.2;
    s.addShape(pres.ShapeType.roundRect, {
      x, y: 2.0, w, h: 2.5,
      rectRadius: 0.05,
      fill: { color: PAPER_ALT }, line: { color: "DFE3EE", width: 1 },
    });
    s.addShape(pres.ShapeType.ellipse, {
      x: x + 0.22, y: 2.22, w: 0.42, h: 0.42,
      fill: { color: st[2] }, line: { color: st[2], width: 0 },
    });
    s.addText(String(i + 1), {
      x: x + 0.22, y: 2.22, w: 0.42, h: 0.42, margin: 0,
      align: "center", valign: "middle",
      fontFace: B_FONT, fontSize: 13, bold: true, color: PAPER,
    });
    s.addText(st[0], {
      x: x + 0.22, y: 2.76, w: w - 0.44, h: 0.36, margin: 0,
      fontFace: B_FONT, fontSize: 15, bold: true, color: INK, valign: "middle",
    });
    s.addText(st[1], {
      x: x + 0.22, y: 3.16, w: w - 0.44, h: 1.2, margin: 0,
      fontFace: B_FONT, fontSize: 11.5, color: GREY, lineSpacing: 17, valign: "top",
    });
    if (i < 4) {
      s.addShape(pres.ShapeType.triangle, {
        x: x + w + 0.05, y: 3.16, w: 0.16, h: 0.2,
        fill: { color: DIM }, line: { color: DIM, width: 0 }, rotate: 90,
      });
    }
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: M, y: 4.85, w: 11.93, h: 1.35,
    rectRadius: 0.05,
    fill: { color: INK }, line: { color: INK, width: 0 },
  });
  s.addText("Odmowa na dowolnym etapie jest normalnym wynikiem, nie błędem.", {
    x: M + 0.4, y: 5.05, w: 11.1, h: 0.36, margin: 0,
    fontFace: B_FONT, fontSize: 16, bold: true, color: PAPER, valign: "middle",
  });
  s.addText(
    "Gdy któraś brama nie przepuści żądania, kolejne etapy w ogóle się nie uruchamiają — nic nie " +
    "zostaje wykonane ani zapisane, a człowiek dostaje informację, czego zabrakło i dlaczego.",
    {
      x: M + 0.4, y: 5.45, w: 11.1, h: 0.65, margin: 0,
      fontFace: B_FONT, fontSize: 12.5, color: GREY_LT, lineSpacing: 19, valign: "top",
    }
  );

  pageFoot(s, false);
}

/* ================================================== 8. KROK 1 =========== */
{
  const s = slide(false);
  title(s, "Krok 1: kto pyta i na co ma zgodę", false,
    "Pięć pytań, na które trzeba odpowiedzieć, zanim cokolwiek się wydarzy");

  const gates = [
    ["Tożsamość", "Czy żądanie pochodzi od tej osoby, za którą się podaje?"],
    ["Rola", "W jakiej roli występuje: właściciela danych, opiekuna, usługi, automatu? Rola to nie to samo co tożsamość."],
    ["Zgoda", "Czy zgoda obejmuje właśnie te dane, w tym celu i w tym czasie? Zgoda ogólna nie wystarcza."],
    ["Kontekst", "Jaki jest cel, budżet działania i warunki przerwania? Kontekst jest zamrażany, żeby dało się go później odtworzyć."],
    ["Dane sprawy", "Których konkretnych obiektów dotyczy żądanie i czy w ogóle istnieją?"],
  ];
  gates.forEach((g, i) => {
    const y = 1.9 + i * 0.95;
    card(s, M, y, 11.93, 0.82, false);
    s.addShape(pres.ShapeType.ellipse, {
      x: M + 0.3, y: y + 0.21, w: 0.4, h: 0.4,
      fill: { color: INK }, line: { color: INK, width: 0 },
    });
    s.addText(String(i + 1), {
      x: M + 0.3, y: y + 0.21, w: 0.4, h: 0.4, margin: 0,
      align: "center", valign: "middle",
      fontFace: B_FONT, fontSize: 12.5, bold: true, color: PAPER,
    });
    s.addText(g[0], {
      x: M + 0.9, y, w: 2.0, h: 0.82, margin: 0,
      fontFace: B_FONT, fontSize: 15, bold: true, color: INK, valign: "middle",
    });
    s.addText(g[1], {
      x: M + 3.0, y, w: 8.5, h: 0.82, margin: 0,
      fontFace: B_FONT, fontSize: 12.5, color: GREY, valign: "middle",
    });
  });

  note(s, "Kolejność ma znaczenie: pytanie o zgodę pada zanim system sięgnie po jakiekolwiek dane, a nie po fakcie.", false);
  pageFoot(s, false);
}

/* ================================================== 9. KROK 2 =========== */
{
  const s = slide(false);
  title(s, "Krok 2: dziewięć pytań kontrolnych", false,
    "Tak brzmią testy zasad, gdy przetłumaczyć je na zwykły język");

  const tests = [
    "Czy człowiek pozostaje autorem tej decyzji?",
    "Czy działanie nie zawęża jego samodzielności?",
    "Czy tworzy coś, czy tylko konsumuje uwagę?",
    "Czy nie wyciąga z niego wartości bez zwrotu?",
    "Czy jest na to świadoma, konkretna zgoda?",
    "Czy da się to cofnąć?",
    "Czy nie uzależnia od rozwiązań, które szkodzą?",
    "Czy dane zostają przenośne i da się odejść?",
    "Czy ograniczenia są powiedziane wprost?",
  ];
  tests.forEach((t, i) => {
    const c = i % 3, r = Math.floor(i / 3);
    const x = M + c * 4.03;
    const y = 1.95 + r * 1.45;
    card(s, x, y, 3.83, 1.25, false);
    s.addText(String(i + 1), {
      x: x + 0.25, y: y + 0.16, w: 0.5, h: 0.35, margin: 0,
      fontFace: M_FONT, fontSize: 12, bold: true, color: TEAL, valign: "middle",
    });
    s.addText(t, {
      x: x + 0.25, y: y + 0.52, w: 3.35, h: 0.62, margin: 0,
      fontFace: B_FONT, fontSize: 12.5, bold: true, color: INK, lineSpacing: 18, valign: "top",
    });
  });

  note(s, "Każde pytanie ma w kodzie własny numer i własny skutek odmowy — powyżej podane są ich znaczenia, nie identyfikatory.", false);
  pageFoot(s, false);
}

/* ================================================== 10. KROK 3 ========== */
{
  const s = slide(false);
  title(s, "Krok 3: sześć możliwych odpowiedzi", false,
    "System nie ma trybu „jakoś to zrobię” — każde żądanie kończy się jednym z sześciu wyników");

  const verdicts = [
    ["Zgoda", "Można wykonać bez zastrzeżeń.", TEAL],
    ["Zgoda z ograniczeniem", "Można, ale w węższej formie — na przykład jako szkic do redakcji, nie gotowa decyzja.", TEAL_LT],
    ["Potrzebna zgoda", "Brakuje świadomej zgody na ten konkretny zakres i cel.", GOLD],
    ["Decyzja należy do człowieka", "Sprawa przekracza to, co system może rozstrzygnąć za kogoś.", "C07A22"],
    ["Do przeprojektowania", "Sposób wykonania łamie zasadę — trzeba zmienić projekt działania, nie prosić o zgodę.", "8A5A9E"],
    ["Naruszenie zasad", "Działania tego rodzaju nie wykonuje się w ogóle.", CRIMSON],
  ];
  verdicts.forEach((v, i) => {
    const c = i % 2, r = Math.floor(i / 2);
    const x = M + c * 6.13;
    const y = 1.95 + r * 1.55;
    card(s, x, y, 5.8, 1.35, false);
    s.addShape(pres.ShapeType.roundRect, {
      x: x + 0.3, y: y + 0.28, w: 0.14, h: 0.8,
      rectRadius: 0.07,
      fill: { color: v[2] }, line: { color: v[2], width: 0 },
    });
    s.addText(v[0], {
      x: x + 0.65, y: y + 0.24, w: 4.9, h: 0.36, margin: 0,
      fontFace: B_FONT, fontSize: 15.5, bold: true, color: v[2], valign: "middle",
    });
    s.addText(v[1], {
      x: x + 0.65, y: y + 0.64, w: 4.9, h: 0.6, margin: 0,
      fontFace: B_FONT, fontSize: 12.5, color: GREY, lineSpacing: 18, valign: "top",
    });
  });

  pageFoot(s, false);
}

/* ================================================== 11. NIE WIEM ======== */
{
  const s = slide(true);
  title(s, "Kiedy system mówi: nie wiem", true,
    "Wstrzymanie się jest osobnym, przewidzianym wynikiem — nie awarią i nie ciszą");

  s.addText(
    "Doradca, który zawsze ma odpowiedź, jest podejrzany. Gdy dane są sprzeczne, celu nie da się " +
    "ustalić, ryzyko jest zbyt duże albo sprawa wykracza poza kompetencje systemu, Human OS nie " +
    "wybiera wariantu z najwyższą punktacją. Nazywa powód i oddaje decyzję człowiekowi.",
    {
      x: M, y: 1.95, w: 6.2, h: 2.0, margin: 0,
      fontFace: B_FONT, fontSize: 15, color: PAPER, lineSpacing: 26, valign: "top",
    }
  );
  s.addText(
    "Powodów wstrzymania się jest osiem i każdy ma nazwę. To nie jest ozdobnik: nazwany powód " +
    "można pokazać użytkownikowi, przetestować i zakwestionować.",
    {
      x: M, y: 4.0, w: 6.2, h: 1.4, margin: 0,
      fontFace: B_FONT, fontSize: 14, italic: true, color: GOLD, lineSpacing: 24, valign: "top",
    }
  );

  const reasons = [
    "brak jasnego celu", "za mało danych", "konflikt wartości", "sprzeczne przesłanki",
    "nie da się tego monitorować", "zbyt duże ryzyko", "poza kompetencją systemu", "podejrzenie kryzysu",
  ];
  reasons.forEach((r, i) => {
    const c = i % 2, row = Math.floor(i / 2);
    const x = 7.25 + c * 2.75;
    const y = 1.95 + row * 1.1;
    card(s, x, y, 2.6, 0.92, true);
    s.addText(r, {
      x: x + 0.22, y, w: 2.2, h: 0.92, margin: 0,
      fontFace: B_FONT, fontSize: 12.5, bold: true, color: PAPER, valign: "middle",
    });
  });

  note(s, "Osobno od wstrzymania się istnieje eskalacja: sprawa wraca do człowieka lub do opiekuna, zamiast zostać rozstrzygnięta automatycznie.", true);
  pageFoot(s, true);
}

/* ================================================== 12. MODEL SIEBIE ==== */
{
  const s = slide(false);
  title(s, "Co system o tobie wie", false,
    "Trzy rodzaje zapisów, które nigdy się ze sobą nie mieszają");

  const kinds = [
    ["Powiedziałeś to sam", "Twoje własne słowa. Tylko ty możesz je zmienić.", TEAL],
    ["System to zauważył", "Wzorzec w danych, które mu powierzyłeś — podany z zaznaczeniem, że to obserwacja.", TEAL_LT],
    ["System się domyśla", "Hipoteza. Musi mieć wskazane przesłanki i nigdy nie jest podawana dalej jak fakt.", GOLD],
  ];
  kinds.forEach((k, i) => {
    const x = M + i * 4.03;
    card(s, x, 1.9, 3.83, 1.85, false);
    s.addShape(pres.ShapeType.roundRect, {
      x: x + 0.28, y: 2.12, w: 1.9, h: 0.3,
      rectRadius: 0.06,
      fill: { color: k[2] }, line: { color: k[2], width: 0 },
    });
    s.addText(String(i + 1), {
      x: x + 0.28, y: 2.12, w: 1.9, h: 0.3, margin: 0,
      align: "center", valign: "middle",
      fontFace: B_FONT, fontSize: 11, bold: true, color: i === 2 ? INK : PAPER,
    });
    s.addText(k[0], {
      x: x + 0.28, y: 2.55, w: 3.3, h: 0.36, margin: 0,
      fontFace: B_FONT, fontSize: 15, bold: true, color: INK, valign: "middle",
    });
    s.addText(k[1], {
      x: x + 0.28, y: 2.95, w: 3.3, h: 0.75, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: GREY, lineSpacing: 18, valign: "top",
    });
  });

  const rules = [
    ["Poprawka nie kasuje historii", "Zmiana tworzy nową wersję, a poprzednia zostaje widoczna wraz z powodem zmiany."],
    ["Odrzucenie to nie usunięcie", "Zakwestionowany zapis dostaje status spornego — nie znika, ale i nie jest już używany jak fakt."],
    ["Zawsze można spytać „skąd to wiesz”", "System pokazuje źródło, autora, poziom pewności i całą historię danego zapisu."],
    ["Sprzeczność zostaje sprzecznością", "Napięcie między zapisami jest zachowane jako sygnał; rozstrzyga je wyłącznie osoba, której dotyczy."],
  ];
  rules.forEach((r, i) => {
    const c = i % 2, row = Math.floor(i / 2);
    const x = M + c * 6.13;
    const y = 4.05 + row * 1.25;
    bullet(s, x, y + 0.05, INK, "✓");
    s.addText(r[0], {
      x: x + 0.45, y, w: 5.4, h: 0.34, margin: 0,
      fontFace: B_FONT, fontSize: 14, bold: true, color: INK, valign: "middle",
    });
    s.addText(r[1], {
      x: x + 0.45, y: y + 0.36, w: 5.35, h: 0.7, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: GREY, lineSpacing: 18, valign: "top",
    });
  });

  note(s, "Silnik nie rozpoznaje treści rozmowy samodzielnie — wskazanie, co jest kandydatem na zapis, należy do aplikacji i do człowieka.", false);
  pageFoot(s, false);
}

/* ================================================== 13. HAMULEC ========= */
{
  const s = slide(true);
  title(s, "Hamulec bezpieczeństwa", true,
    "Siedem trybów awaryjnych, z których człowiek może skorzystać w każdej chwili");

  const modes = [
    ["Tryb bezpieczny", "ogranicza działanie do niezbędnego minimum", "ochronny"],
    ["Tylko odczyt", "system przestaje cokolwiek zmieniać", "ochronny"],
    ["Zamrożenie", "wskazany obszar zostaje wstrzymany", "ochronny"],
    ["Odcięcie", "zerwanie połączenia z zewnętrzną reprezentacją", "ochronny"],
    ["Eksport", "wydanie pełnej, przenośnej paczki danych", "ręczny"],
    ["Cofnięcie", "powrót do wcześniejszego stanu z zachowaniem historii", "ręczny · dwa klucze"],
    ["Odbudowa", "odtworzenie środowiska po poważnej awarii", "ręczny · dwa klucze"],
  ];
  modes.forEach((m, i) => {
    const c = i % 2, r = Math.floor(i / 2);
    const x = M + c * 6.13;
    const y = 1.95 + r * 0.86;
    if (i === 6) return; // ostatni pod spodem, na całą szerokość
    card(s, x, y, 5.8, 0.74, true);
    s.addText(m[0], {
      x: x + 0.28, y, w: 2.3, h: 0.74, margin: 0,
      fontFace: B_FONT, fontSize: 13.5, bold: true, color: PAPER, valign: "middle",
    });
    s.addText(m[1], {
      x: x + 2.65, y, w: 2.05, h: 0.74, margin: 0,
      fontFace: B_FONT, fontSize: 11, color: GREY_LT, valign: "middle",
    });
    chip(s, x + 4.75, y + 0.22, m[2] === "ochronny" ? "auto" : "ręczny", {
      w: 0.8, fill: m[2] === "ochronny" ? TEAL : GOLD,
      color: m[2] === "ochronny" ? PAPER : INK, mono: false, fontSize: 9.5,
    });
  });
  card(s, M, 1.95 + 3 * 0.86, 11.93, 0.74, true);
  s.addText("Odbudowa", {
    x: M + 0.28, y: 1.95 + 3 * 0.86, w: 2.3, h: 0.74, margin: 0,
    fontFace: B_FONT, fontSize: 13.5, bold: true, color: PAPER, valign: "middle",
  });
  s.addText("odtworzenie środowiska po poważnej awarii — najpoważniejszy z trybów", {
    x: M + 2.65, y: 1.95 + 3 * 0.86, w: 7.5, h: 0.74, margin: 0,
    fontFace: B_FONT, fontSize: 11, color: GREY_LT, valign: "middle",
  });
  chip(s, M + 10.4, 1.95 + 3 * 0.86 + 0.22, "dwa klucze", {
    w: 1.25, fill: GOLD, mono: false, fontSize: 9.5,
  });

  const guards = [
    ["Automat nie może tego użyć", "Agenci i usługi dostają odmowę, a sama próba zostaje zapisana."],
    ["Nie ma czego wyłączyć", "Nie istnieje funkcja zmieniająca politykę ani czyszcząca dziennik audytu."],
    ["Działa bez AI i bez sieci", "Warstwa awaryjna nie zależy od modelu ani od usług zewnętrznych."],
  ];
  guards.forEach((g, i) => {
    const x = M + i * 4.03;
    const y = 5.35;
    card(s, x, y, 3.83, 1.15, true);
    s.addText(g[0], {
      x: x + 0.24, y: y + 0.14, w: 3.4, h: 0.32, margin: 0,
      fontFace: B_FONT, fontSize: 13, bold: true, color: GOLD, valign: "middle",
    });
    s.addText(g[1], {
      x: x + 0.24, y: y + 0.48, w: 3.4, h: 0.6, margin: 0,
      fontFace: B_FONT, fontSize: 11, color: GREY_LT, lineSpacing: 16, valign: "top",
    });
  });

  note(s, "Tryby ochronne mogą włączyć się samoczynnie, ale zawsze z powiadomieniem właściciela i zawsze są przez niego odwracalne.", true);
  pageFoot(s, true);
}

/* ================================================== 14. WYJŚCIE ========= */
{
  const s = slide(false);
  title(s, "Wyjście bez utraty dorobku", false,
    "Jeśli odejście jest kosztowne, cała reszta obietnic traci znaczenie");

  card(s, M, 1.9, 6.5, 4.35, false);
  s.addText("Co zawiera paczka wyjściowa", {
    x: M + 0.35, y: 2.12, w: 5.8, h: 0.4, margin: 0,
    fontFace: B_FONT, fontSize: 16, bold: true, color: INK, valign: "middle",
  });
  const pack = [
    ["Dane i powiązania", "w otwartym formacie, czytelnym bez tego systemu"],
    ["Metadane i rejestr zmian", "co, kiedy i przez kogo było zmieniane"],
    ["Historia wersji wycofanych", "nic nie znika po cichu — stare wersje zostają oznaczone"],
    ["Ślad audytowy", "na jakiej podstawie system podejmował decyzje"],
  ];
  pack.forEach((p, i) => {
    const y = 2.7 + i * 0.85;
    bullet(s, M + 0.35, y, TEAL, "✓");
    s.addText(p[0], {
      x: M + 0.85, y: y - 0.04, w: 5.3, h: 0.32, margin: 0,
      fontFace: B_FONT, fontSize: 13.5, bold: true, color: INK, valign: "middle",
    });
    s.addText(p[1], {
      x: M + 0.85, y: y + 0.28, w: 5.3, h: 0.32, margin: 0,
      fontFace: B_FONT, fontSize: 11.5, color: GREY, valign: "middle",
    });
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: 7.55, y: 1.9, w: 5.08, h: 4.35,
    rectRadius: 0.05,
    fill: { color: INK }, line: { color: INK, width: 0 },
  });
  s.addText("Dlaczego to jest w centrum, a nie w opcjach", {
    x: 7.9, y: 2.15, w: 4.4, h: 0.8, margin: 0,
    fontFace: B_FONT, fontSize: 16, bold: true, color: GOLD, lineSpacing: 24, valign: "top",
  });
  s.addText(
    "Kosztowne wyjście zamienia obietnicę samodzielności w pułapkę — niezależnie od tego, jak dobre " +
    "są intencje twórców. Dlatego przenośność i możliwość odejścia mają w Human OS własny test " +
    "kontrolny i własną zasadę w konstytucji, a każda zmiana w projekcie musi odpowiedzieć, " +
    "czy ich nie pogarsza.",
    {
      x: 7.9, y: 3.05, w: 4.4, h: 2.9, margin: 0,
      fontFace: B_FONT, fontSize: 13, color: GREY_LT, lineSpacing: 21, valign: "top",
    }
  );

  pageFoot(s, false);
}

/* ================================================== 15. SKŁADNIKI ======= */
{
  const s = slide(false);
  title(s, "Z czego to się składa", false,
    "Pięć warstw i jasny podział: co jest dokumentem, a co działającym kodem");

  const layers = [
    ["Konstytucja", "Zasady, prawa użytkownika, skala ryzyka, zakazy. Dokument nadrzędny.", "dokument", GOLD, INK],
    ["Specyfikacja i protokół", "Przenośne kontrakty i podpisane komunikaty między częściami systemu.", "dokument + kod", TEAL, PAPER],
    ["Silnik", "Bramy, testy zasad, tryby awaryjne, dzienniki i eksport.", "kod", INK, PAPER],
    ["Integracje i Hub", "Kierowanie komunikatów, sprawdzanie zgody, poświadczenia.", "kod + projekt", INK_SOFT, PAPER],
    ["Aplikacje", "Konsola reguł i prototyp aplikacji osobistej. Bez własnych reguł.", "prototypy", GREY, PAPER],
  ];
  layers.forEach((l, i) => {
    const y = 1.85 + i * 0.86;
    s.addShape(pres.ShapeType.roundRect, {
      x: M, y, w: 9.5, h: 0.72,
      rectRadius: 0.05,
      fill: { color: l[3] }, line: { color: l[3], width: 0 },
    });
    s.addText(l[0], {
      x: M + 0.3, y, w: 2.7, h: 0.72, margin: 0,
      fontFace: B_FONT, fontSize: 14.5, bold: true, color: l[4], valign: "middle",
    });
    s.addText(l[1], {
      x: M + 3.1, y, w: 6.2, h: 0.72, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: l[4], valign: "middle",
    });
    chip(s, 10.45, y + 0.22, l[2], { w: 2.18, fill: PAPER_ALT, color: GREY, mono: false, fontSize: 10 });
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: M, y: 6.25, w: 11.93, h: 0.6,
    rectRadius: 0.05,
    fill: { color: PAPER_ALT }, line: { color: "DFE3EE", width: 1 },
  });
  s.addText("Zasada porządkująca: żadna warstwa niżej nie może po cichu zmienić reguły ustalonej wyżej.", {
    x: M + 0.35, y: 6.25, w: 11.2, h: 0.6, margin: 0,
    fontFace: B_FONT, fontSize: 13, bold: true, color: INK, valign: "middle",
  });

  pageFoot(s, false);
}

/* ================================================== 16. SZERSZY PROGRAM = */
{
  const s = slide(false);
  title(s, "Czego nie ma w tym repozytorium", false,
    "Kod, o którym mowa, jest częścią większego przedsięwzięcia — nie jego całością");

  const parts = [
    ["Warstwy modelu człowieka i wiedzy", "Model człowieka, mapa wiedzy, profil rozwojowy i silnik decyzji mają pełne opisy projektowe; w kodzie istnieją na razie wybrane fragmenty."],
    ["Silnik eksperymentów osobistych", "Warstwa prowadzenia własnych, małych eksperymentów życiowych — opisana i rozpisana na decyzje, bez implementacji."],
    ["Hub i szersza wymiana danych", "Kierowanie komunikatów między niezależnymi uczestnikami sieci jest dziś dokumentacją, nie działającą usługą."],
    ["Laboratorium i środowisko testowe", "Piaskownica dla testerów z własnym interfejsem: zaprojektowana, prototyp interfejsu istnieje poza tym repozytorium."],
    ["Warstwa narracyjna i White Paper", "Rozdział o technologii, która pamięta, komu ma służyć — w repozytorium jest jego pełna transkrypcja."],
    ["Zarządzanie i historia decyzji", "Kilkadziesiąt zapisów decyzji projektowych, przeglądy założyciela i kolejka spraw odłożonych świadomie."],
  ];
  parts.forEach((p, i) => {
    const c = i % 2, r = Math.floor(i / 2);
    const x = M + c * 6.13;
    const y = 1.9 + r * 1.55;
    card(s, x, y, 5.8, 1.35, false);
    s.addText(p[0], {
      x: x + 0.3, y: y + 0.18, w: 5.2, h: 0.36, margin: 0,
      fontFace: B_FONT, fontSize: 14, bold: true, color: INK, valign: "middle",
    });
    s.addText(p[1], {
      x: x + 0.3, y: y + 0.56, w: 5.2, h: 0.7, margin: 0,
      fontFace: B_FONT, fontSize: 11.5, color: GREY, lineSpacing: 17, valign: "top",
    });
  });

  note(s, "Mówimy o tym wprost, żeby nikt nie ocenił całego przedsięwzięcia wyłącznie po zawartości jednego repozytorium — w żadną ze stron.", false);
  pageFoot(s, false);
}

/* ================================================== 17. CO DZIAŁA ======= */
{
  const s = slide(true);
  title(s, "Co działa dzisiaj", true,
    "Stan faktyczny, policzony z repozytorium — bez zaokrągleń w górę");

  const stats = [
    ["36", "modułów silnika"],
    ["166", "testów automatycznych"],
    ["9", "testów zasad"],
    ["67", "zapisanych decyzji projektowych"],
  ];
  stats.forEach((st, i) => {
    const x = M + i * 3.03;
    card(s, x, 1.9, 2.85, 1.5, true);
    s.addText(st[0], {
      x: x + 0.25, y: 2.0, w: 2.35, h: 0.7, margin: 0,
      fontFace: H_FONT, fontSize: 36, bold: true, color: GOLD, valign: "middle",
    });
    s.addText(st[1], {
      x: x + 0.25, y: 2.72, w: 2.4, h: 0.55, margin: 0,
      fontFace: B_FONT, fontSize: 12.5, bold: true, color: PAPER, lineSpacing: 16, valign: "top",
    });
  });

  const done = [
    "pełna droga żądania: tożsamość, rola, zgoda, kontekst, dane, test zasad, wykonanie, ślad",
    "dziennik zdarzeń spięty łańcuchem skrótów, z możliwością sprawdzenia integralności",
    "siedem trybów awaryjnych wraz z eksportem, cofnięciem i odbudową",
    "model tego, co system wie o człowieku, wraz z historią zmian i poziomem pewności",
    "silnik decyzji z twardymi warunkami wstępnymi, wstrzymaniem się i eskalacją",
    "podpisywane komunikaty, rejestr tożsamości i kluczy, ochrona przed powtórzeniem żądania",
  ];
  s.addText("W KODZIE, PRZETESTOWANE", {
    x: M, y: 3.65, w: 11.93, h: 0.3, margin: 0,
    fontFace: B_FONT, fontSize: 11, bold: true, color: TEAL, charSpacing: 2,
  });
  done.forEach((d, i) => {
    const c = i % 2, r = Math.floor(i / 2);
    const x = M + c * 6.13;
    const y = 4.05 + r * 0.78;
    bullet(s, x, y, TEAL, "✓");
    s.addText(d, {
      x: x + 0.45, y: y - 0.06, w: 5.4, h: 0.6, margin: 0,
      fontFace: B_FONT, fontSize: 11.5, color: PAPER, lineSpacing: 16, valign: "top",
    });
  });

  note(s, "Testy uruchamiane są automatycznie na trzech wersjach Pythona przy każdej zmianie w repozytorium.", true);
  pageFoot(s, true);
}

/* ================================================== 18. CZEGO BRAK ====== */
{
  const s = slide(false);
  title(s, "Czego nie obiecujemy", false,
    "Lista, którą zwykle znajduje się dopiero podczas wdrożenia — tutaj jest od razu");

  const gaps = [
    ["Brak logowania i uprawnień", "Nie ma mechanizmu uwierzytelniania użytkowników ani kontroli dostępu na poziomie wdrożeniowym."],
    ["Brak szyfrowania danych na dysku", "Dane w spoczynku nie są szyfrowane przez sam silnik."],
    ["Brak niezależnego audytu", "Przegląd zewnętrzny jeszcze się nie odbył. Obecne podpisy to mechanizm referencyjny, lokalny."],
    ["Brak kalibracji na danych", "Skale ryzyka i progi nie zostały sprawdzone na rzeczywistym użyciu."],
    ["Część opisanych warstw bez kodu", "Kilka warstw ma dopracowany projekt, ale nie ma jeszcze implementacji."],
    ["Dwa równoległe słowniki pojęć", "Niektóre nazwy obiektów i relacji istnieją w dwóch wersjach; ujednolicenie jest świadomie odłożone."],
  ];
  gaps.forEach((g, i) => {
    const y = 1.88 + i * 0.74;
    card(s, M, y, 11.93, 0.62, false);
    s.addShape(pres.ShapeType.roundRect, {
      x: M + 0.3, y: y + 0.14, w: 0.14, h: 0.34,
      rectRadius: 0.07,
      fill: { color: CRIMSON }, line: { color: CRIMSON, width: 0 },
    });
    s.addText(g[0], {
      x: M + 0.65, y, w: 4.0, h: 0.62, margin: 0,
      fontFace: B_FONT, fontSize: 13.5, bold: true, color: INK, valign: "middle",
    });
    s.addText(g[1], {
      x: M + 4.8, y, w: 6.7, h: 0.62, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: GREY, valign: "middle",
    });
  });

  note(s, "Wniosek jest prosty: to wersja do badań, prototypów i integracji testowych — nie do produkcji z prawdziwymi danymi osób.", false);
  pageFoot(s, false);
}

/* ================================================== 19. ZASADY ========== */
{
  const s = slide(false);
  title(s, "Licencje, znaki, zarządzanie", false,
    "Na jakich warunkach można z tego korzystać i jak wygląda wprowadzanie zmian");

  const blocks = [
    ["Kod", "Apache 2.0", "Wolno używać komercyjnie, modyfikować i rozprowadzać, z zachowaniem informacji o autorstwie.", TEAL],
    ["Dokumentacja", "CC BY 4.0", "Wolno cytować i przetwarzać z podaniem źródła — dotyczy konstytucji i specyfikacji.", TEAL_LT],
    ["Nazwa i znaki", "polityka robocza", "Rozgałęzienia projektu są w porządku, ale nie powinny przedstawiać się jako oficjalny Human OS.", GOLD],
  ];
  blocks.forEach((b, i) => {
    const x = M + i * 4.03;
    card(s, x, 1.9, 3.83, 2.15, false);
    s.addText(b[0], {
      x: x + 0.3, y: 2.12, w: 3.2, h: 0.36, margin: 0,
      fontFace: B_FONT, fontSize: 15, bold: true, color: INK, valign: "middle",
    });
    chip(s, x + 0.3, 2.55, b[1], { w: 2.2, fill: b[3], color: i === 2 ? INK : PAPER, mono: false, fontSize: 10.5 });
    s.addText(b[2], {
      x: x + 0.3, y: 3.0, w: 3.25, h: 0.95, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: GREY, lineSpacing: 18, valign: "top",
    });
  });

  const rules = [
    ["Zmiana zasad to osobna ścieżka", "Poprawka w konstytucji nie przechodzi zwykłym trybem — wymaga wyższego progu akceptacji i zgody człowieka odpowiedzialnego za projekt."],
    ["Każda zmiana deklaruje wpływ", "Zgłoszenie musi napisać, które zasady wspiera, które stawia pod ryzykiem, jakie ma ograniczenia i czy nie pogarsza możliwości wyjścia."],
    ["Błędy zgłasza się prywatnie", "Osobny kanał bezpieczeństwa, opisany w repozytorium — nie przez publiczne zgłoszenie."],
  ];
  rules.forEach((r, i) => {
    const y = 4.2 + i * 0.75;
    card(s, M, y, 11.93, 0.64, false);
    s.addText(r[0], {
      x: M + 0.35, y, w: 4.1, h: 0.64, margin: 0,
      fontFace: B_FONT, fontSize: 13, bold: true, color: TEAL, valign: "middle",
    });
    s.addText(r[1], {
      x: M + 4.6, y, w: 6.9, h: 0.64, margin: 0,
      fontFace: B_FONT, fontSize: 11.5, color: GREY, valign: "middle",
    });
  });

  note(s, "Polityka znaku towarowego jest deklaracją roboczą projektu, a nie opinią prawną.", false);
  pageFoot(s, false);
}

/* ================================================== 20. ROADMAPA ======== */
{
  const s = slide(true);
  title(s, "Droga do wersji 1.0", true,
    "Osiem etapów zamkniętych, jeden otwarty i wyraźnie opisany cel");

  s.addText(
    "Zamknięte: formalny rdzeń · specyfikacja czytelna dla maszyn · silnik reguł · trwały, " +
    "audytowalny zapis · graf wiedzy i pochodzenie danych · granice działania agentów · " +
    "symulacje scenariuszy · model człowieka i zgoda",
    {
      x: M, y: 1.95, w: 11.93, h: 0.9, margin: 0,
      fontFace: B_FONT, fontSize: 12.5, color: GREY_LT, lineSpacing: 20, valign: "top",
    }
  );

  s.addShape(pres.ShapeType.roundRect, {
    x: M, y: 3.05, w: 11.93, h: 1.25,
    rectRadius: 0.05,
    fill: { color: GOLD }, line: { color: GOLD, width: 0 },
  });
  s.addText("Etap otwarty", {
    x: M + 0.35, y: 3.2, w: 3.0, h: 0.34, margin: 0,
    fontFace: B_FONT, fontSize: 12, bold: true, color: "5A4212", valign: "middle",
  });
  s.addText("Zgodność protokołu między niezależnymi wdrożeniami oraz przegląd bezpieczeństwa", {
    x: M + 0.35, y: 3.56, w: 11.2, h: 0.36, margin: 0,
    fontFace: B_FONT, fontSize: 15.5, bold: true, color: INK, valign: "middle",
  });
  s.addText("Prace nad kolejnymi warstwami toczą się równolegle i nie zastępują tego etapu.", {
    x: M + 0.35, y: 3.92, w: 11.2, h: 0.32, margin: 0,
    fontFace: B_FONT, fontSize: 11.5, color: "5A4212", valign: "middle",
  });

  const conds = [
    "stabilna konstytucja i model obiektów",
    "protokół z jasnym wersjonowaniem",
    "opisane ścieżki migracji",
    "udokumentowany przegląd bezpieczeństwa",
    "pełna przenośność danych",
    "mierzalna, sprawdzalna możliwość wyjścia",
  ];
  s.addText("WARUNKI OGŁOSZENIA WERSJI 1.0", {
    x: M, y: 4.55, w: 11.93, h: 0.3, margin: 0,
    fontFace: B_FONT, fontSize: 11, bold: true, color: GOLD, charSpacing: 2,
  });
  conds.forEach((c, i) => {
    const col = i % 3, r = Math.floor(i / 3);
    const x = M + col * 4.03;
    const y = 4.95 + r * 0.72;
    card(s, x, y, 3.83, 0.6, true);
    s.addText(c, {
      x: x + 0.25, y, w: 3.4, h: 0.6, margin: 0,
      fontFace: B_FONT, fontSize: 11.5, color: PAPER, valign: "middle",
    });
  });

  pageFoot(s, true);
}

/* ================================================== 21. DLA KOGO ======== */
{
  const s = slide(false);
  title(s, "Dla kogo to jest", false,
    "Trzy sytuacje, w których warto sięgnąć po Human OS już teraz");

  const who = [
    ["Zespół produktowy",
     "Buduje asystenta lub narzędzie pracujące na danych osobistych i potrzebuje sprawdzalnej " +
     "granicy tego, co wolno zrobić bez pytania.",
     "Zacznij od uruchomienia konsoli reguł na własnym przykładzie działania."],
    ["Organizacja i dział ryzyka",
     "Musi pokazać, jak system zachował się w konkretnej sprawie i na jakiej podstawie — " +
     "nie ogólnie, lecz co do zdarzenia.",
     "Przejrzyj mechanizm śladu, zgody zakresowej i eksportu."],
    ["Badacz lub instytucja",
     "Pracuje nad odpowiedzialną technologią i szuka opisu, który da się przetestować, " +
     "a nie tylko zacytować.",
     "Konstytucja, zapisy decyzji i testy zasad są otwarte i cytowalne."],
  ];
  who.forEach((w, i) => {
    const x = M + i * 4.03;
    card(s, x, 1.9, 3.83, 4.3, false);
    s.addShape(pres.ShapeType.ellipse, {
      x: x + 0.3, y: 2.15, w: 0.44, h: 0.44,
      fill: { color: [TEAL, INK, GOLD][i] }, line: { color: [TEAL, INK, GOLD][i], width: 0 },
    });
    s.addText(String(i + 1), {
      x: x + 0.3, y: 2.15, w: 0.44, h: 0.44, margin: 0,
      align: "center", valign: "middle",
      fontFace: B_FONT, fontSize: 13, bold: true, color: i === 2 ? INK : PAPER,
    });
    s.addText(w[0], {
      x: x + 0.3, y: 2.72, w: 3.25, h: 0.4, margin: 0,
      fontFace: B_FONT, fontSize: 16, bold: true, color: INK, valign: "middle",
    });
    s.addText(w[1], {
      x: x + 0.3, y: 3.2, w: 3.25, h: 1.5, margin: 0,
      fontFace: B_FONT, fontSize: 12.5, color: GREY, lineSpacing: 19, valign: "top",
    });
    s.addText("Pierwszy krok", {
      x: x + 0.3, y: 4.75, w: 3.25, h: 0.3, margin: 0,
      fontFace: B_FONT, fontSize: 11, bold: true, color: TEAL, valign: "middle",
    });
    s.addText(w[2], {
      x: x + 0.3, y: 5.08, w: 3.25, h: 0.95, margin: 0,
      fontFace: B_FONT, fontSize: 12, color: INK, lineSpacing: 18, valign: "top",
    });
  });

  pageFoot(s, false);
}

/* ================================================== 22. ZAMKNIĘCIE ====== */
{
  const s = slide(true);

  s.addText("Jedno kryterium, do którego wszystko wraca", {
    x: M, y: 1.95, w: 7.8, h: 0.5, margin: 0,
    fontFace: B_FONT, fontSize: 16, color: GREY_LT, valign: "middle",
  });
  s.addText("System, który ma stawać się\ncoraz mniej potrzebny.", {
    x: M, y: 2.6, w: 7.9, h: 1.9, margin: 0,
    fontFace: H_FONT, fontSize: 36, bold: true, color: PAPER, lineSpacing: 50, valign: "top",
  });
  s.addText(
    "Miarą powodzenia nie jest to, ile czasu ktoś spędza w produkcie, tylko ile samodzielności " +
    "z niego wynosi. Wszystkie opisane wcześniej mechanizmy — bramy, testy zasad, wstrzymanie się, " +
    "poprawki, hamulec awaryjny, eksport — służą temu jednemu kryterium.",
    {
      x: M, y: 4.55, w: 7.7, h: 1.4, margin: 0,
      fontFace: B_FONT, fontSize: 13.5, color: GREY_LT, lineSpacing: 22, valign: "top",
    }
  );
  s.addText("github.com/dudsi101-svg/human-os", {
    x: M, y: 6.05, w: 7.7, h: 0.32, margin: 0,
    fontFace: M_FONT, fontSize: 12, color: GOLD, valign: "middle",
  });

  card(s, 9.0, 1.9, 3.63, 4.35, true);
  s.addText("Gdzie zajrzeć najpierw", {
    x: 9.3, y: 2.15, w: 3.05, h: 0.4, margin: 0,
    fontFace: B_FONT, fontSize: 15, bold: true, color: GOLD, valign: "middle",
  });
  const links = [
    ["Konstytucja", "zasady i prawa użytkownika"],
    ["Przegląd bezpieczeństwa", "co jest, a czego brakuje"],
    ["Zasady współpracy", "jak zgłaszać zmiany"],
    ["Zapisy decyzji", "dlaczego zbudowano to tak"],
  ];
  links.forEach((l, i) => {
    const y = 2.75 + i * 0.85;
    s.addText(l[0], {
      x: 9.3, y, w: 3.05, h: 0.3, margin: 0,
      fontFace: B_FONT, fontSize: 13, bold: true, color: PAPER, valign: "middle",
    });
    s.addText(l[1], {
      x: 9.3, y: y + 0.3, w: 3.05, h: 0.34, margin: 0,
      fontFace: B_FONT, fontSize: 11, color: GREY_LT, valign: "middle",
    });
  });

  pageFoot(s, true);
}

pres.writeFile({ fileName: OUT }).then(() => console.log("OK:", OUT));
