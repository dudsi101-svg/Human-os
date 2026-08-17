/**
 * Generator materiałów reklamowych aplikacji Human OS.
 *
 * Uruchomienie:  node docs/marketing/build_assets.js
 * Wynik:         docs/marketing/assets/*.png
 *
 * Zasady, których ten plik pilnuje:
 *  - paleta i typografia są przepisane z samej aplikacji (apps/user-demo/human_os_app.html),
 *    żeby reklama wyglądała jak produkt, a nie jak osobna marka,
 *  - zrzuty ekranu w assets/ekrany/ są prawdziwe (zrobione z działającej aplikacji),
 *    nie są to makiety ani rendery,
 *  - żadne hasło nie obiecuje funkcji, której aplikacja nie ma — patrz KOMUNIKACJA.md,
 *    sekcja „Czego nie wolno obiecywać”.
 *
 * Wymaga: playwright + Chromium.
 */

const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const DIR = __dirname;
const OUT = path.join(DIR, "assets");
const EXE = process.env.CHROMIUM_PATH || "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";

/* ------------------------------------------- paleta przepisana z aplikacji */

const C = {
  bg: "#F2EFE7",
  surface: "#FBFAF4",
  surface2: "#EDE9DD",
  line: "#DCD6C4",
  ink: "#262A21",
  ink2: "#555B4B",
  ink3: "#878D7B",
  accent: "#7C9370",
  accentTint: "#E2E8D9",
  verdigris: "#5F7F55",
  clay: "#BC6448",
  clayTint: "#F2DFD6",
  warn: "#A98544",
  warnTint: "#EFE6CE",
  darkBg: "#161812",
  darkSurface: "#1E211A",
  darkLine: "#39402F",
  darkInk: "#E8E6DA",
  darkInk2: "#B3B8A6",
  darkAccent: "#A3B896",
};

// serif: w aplikacji Iowan Old Style / Palatino; w kontenerze najbliższy jest Charter
const SERIF = `"Iowan Old Style", "Palatino Linotype", Palatino, "Bitstream Charter", Georgia, serif`;
const SANS = `"DejaVu Sans", -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`;
const MONO = `"DejaVu Sans Mono", ui-monospace, Consolas, monospace`;

const base = (dark) => `
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{width:100%;height:100%}
  body{
    background:${dark ? C.darkBg : C.bg};
    color:${dark ? C.darkInk : C.ink};
    font-family:${SANS};
    -webkit-font-smoothing:antialiased;
    display:flex;flex-direction:column;
    overflow:hidden;
  }
  .serif{font-family:${SERIF}}
  .pill{
    display:inline-block;border-radius:999px;
    font-family:${SANS};font-weight:700;letter-spacing:.09em;text-transform:uppercase;
  }
  .card{
    background:${dark ? C.darkSurface : C.surface};
    border:1px solid ${dark ? C.darkLine : C.line};
    border-radius:22px;
  }
  .mark{font-family:${SERIF};letter-spacing:-.01em}
  .muted{color:${dark ? C.darkInk2 : C.ink2}}
  .faint{color:${dark ? "#828876" : C.ink3}}
`;

// delikatne „pyłki” — motyw z tła aplikacji
function dust(n, dark) {
  const seed = [
    [12, 18, 6], [78, 9, 4], [46, 27, 3], [88, 41, 5], [22, 62, 4],
    [67, 74, 6], [35, 88, 3], [92, 82, 4], [8, 47, 5], [57, 52, 3],
  ];
  return seed.slice(0, n).map(([x, y, r], i) => {
    const col = i % 3 === 0 ? C.clay : i % 3 === 1 ? C.accent : C.warn;
    return `<div style="position:absolute;left:${x}%;top:${y}%;width:${r * 2}px;height:${r * 2}px;
      border-radius:999px;background:${col};opacity:${dark ? 0.24 : 0.18};filter:blur(.5px)"></div>`;
  }).join("");
}

function pill(text, { fg = C.verdigris, bg = C.accentTint, size = 20, pad = "14px 26px" } = {}) {
  return `<span class="pill" style="color:${fg};background:${bg};font-size:${size}px;padding:${pad}">${text}</span>`;
}

function logo(size, dark) {
  return `<span class="mark" style="font-size:${size}px;font-weight:600;color:${dark ? C.darkInk : C.ink}">Human OS</span>`;
}

function page(w, h, dark, body, extraCss = "") {
  return `<!doctype html><html lang="pl"><head><meta charset="utf-8">
  <style>${base(dark)}
  .stage{position:relative;width:${w}px;height:${h}px;overflow:hidden}
  ${extraCss}</style></head>
  <body><div class="stage">${body}</div></body></html>`;
}

/* ============================================================== materiały */

const assets = [];

/* --- 1. Key visual / Open Graph 1200x630 -------------------------------- */
assets.push({
  name: "kv-og-1200x630",
  w: 1200, h: 630,
  html: page(1200, 630, false, `
    ${dust(8, false)}
    <div style="position:absolute;inset:0;display:flex;align-items:center;padding:64px 72px;gap:56px">
      <div style="flex:1;min-width:0">
        ${logo(30, false)}
        <div class="serif" style="font-size:64px;line-height:1.08;margin-top:26px;letter-spacing:-.015em">
          Aplikacja, która chce być<br>coraz mniej potrzebna.
        </div>
        <div class="muted" style="font-size:23px;line-height:1.5;margin-top:26px;max-width:600px">
          Rozwój osobisty bez oddawania sterów. Twoje dane zostają u Ciebie,
          a system mówi „nie wiem”, kiedy nie wie.
        </div>
        <div style="margin-top:34px;display:flex;gap:14px">
          ${pill("Bez konta", { size: 17, pad: "12px 22px" })}
          ${pill("Bez serwera", { fg: C.clay, bg: C.clayTint, size: 17, pad: "12px 22px" })}
          ${pill("Eksport zawsze bezpłatny", { fg: C.warn, bg: C.warnTint, size: 17, pad: "12px 22px" })}
        </div>
      </div>
      <div style="width:300px;flex:none;position:relative">
        <div style="border-radius:38px;overflow:hidden;border:10px solid ${C.ink};
             box-shadow:0 30px 70px rgba(38,42,33,.28)">
          <img src="ekrany/pulpit.png" style="display:block;width:100%">
        </div>
      </div>
    </div>
  `),
});

/* --- 2. Post kwadratowy: abstencja -------------------------------------- */
assets.push({
  name: "post-01-nie-wiem-1080",
  w: 1080, h: 1080,
  html: page(1080, 1080, false, `
    ${dust(7, false)}
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;padding:84px 80px">
      ${logo(28, false)}
      <div style="margin-top:auto">
        ${pill("Uczciwa abstencja", { size: 21 })}
        <div class="serif" style="font-size:132px;line-height:1;margin-top:34px;letter-spacing:-.02em">
          „Nie wiem.”
        </div>
        <div class="muted" style="font-size:31px;line-height:1.45;margin-top:32px;max-width:820px">
          Trzy słowa, których nie usłyszysz od aplikacji rozwojowej.
          Ta je mówi — i od razu nazywa powód: sprzeczne przesłanki,
          za mało danych, poza jej kompetencją.
        </div>
      </div>
      <div style="margin-top:auto;display:flex;align-items:center;gap:16px">
        <div style="width:44px;height:2px;background:${C.line}"></div>
        <div class="faint" style="font-size:21px">Rekomendacja bez pewności siebie na kredyt.</div>
      </div>
    </div>
  `),
});

/* --- 3. Post kwadratowy: wyjście ---------------------------------------- */
assets.push({
  name: "post-02-wyjscie-1080",
  w: 1080, h: 1080,
  html: page(1080, 1080, true, `
    ${dust(7, true)}
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;padding:84px 80px">
      ${logo(28, true)}
      <div style="margin-top:auto">
        ${pill("Gwarancja konstytucyjna", { fg: C.darkBg, bg: C.darkAccent, size: 21 })}
        <div class="serif" style="font-size:96px;line-height:1.06;margin-top:34px;letter-spacing:-.02em;color:${C.darkInk}">
          Wyjście jest<br>bezpłatne. Zawsze.
        </div>
        <div style="font-size:31px;line-height:1.45;margin-top:32px;max-width:840px;color:${C.darkInk2}">
          Eksport, import, Twój model i tryby awaryjne nigdy nie będą funkcją premium.
          Nie dlatego, że jesteśmy mili — dlatego, że tak stanowi konstytucja aplikacji.
        </div>
      </div>
      <div style="margin-top:auto;display:flex;gap:14px;flex-wrap:wrap">
        ${pill("Eksport", { fg: C.darkAccent, bg: "#22301E", size: 18, pad: "13px 22px" })}
        ${pill("Import", { fg: C.darkAccent, bg: "#22301E", size: 18, pad: "13px 22px" })}
        ${pill("Model", { fg: C.darkAccent, bg: "#22301E", size: 18, pad: "13px 22px" })}
        ${pill("Usunięcie", { fg: C.darkAccent, bg: "#22301E", size: 18, pad: "13px 22px" })}
        ${pill("Tryby awaryjne", { fg: C.darkAccent, bg: "#22301E", size: 18, pad: "13px 22px" })}
      </div>
    </div>
  `),
});

/* --- 4. Post kwadratowy: model siebie ----------------------------------- */
assets.push({
  name: "post-03-model-1080",
  w: 1080, h: 1080,
  html: page(1080, 1080, false, `
    ${dust(6, false)}
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;padding:84px 80px">
      ${logo(28, false)}
      <div class="serif" style="font-size:74px;line-height:1.1;margin-top:44px;letter-spacing:-.02em">
        To, co powiedziałeś,<br>nie miesza się z tym,<br>co system podejrzewa.
      </div>
      <div style="margin-top:auto;display:flex;flex-direction:column;gap:20px">
        ${[
          ["Deklaracja", "Twoje własne słowa. Tylko Ty je zmieniasz.", C.verdigris, C.accentTint],
          ["Obserwacja", "Wzorzec w danych, które sam powierzyłeś.", C.accent, C.accentTint],
          ["Hipoteza", "Domysł. Musi pokazać przesłanki i nigdy nie udaje faktu.", C.warn, C.warnTint],
        ].map(([t, d, fg, bg]) => `
          <div class="card" style="padding:30px 34px;display:flex;align-items:center;gap:28px">
            <span class="pill" style="color:${fg};background:${bg};font-size:19px;padding:12px 22px;flex:none;width:210px;text-align:center">${t}</span>
            <span class="muted" style="font-size:26px;line-height:1.35">${d}</span>
          </div>`).join("")}
      </div>
      <div class="faint" style="font-size:21px;margin-top:38px">
        Przy każdym zapisie możesz spytać: skąd to wiesz?
      </div>
    </div>
  `),
});

/* --- 5. Story pionowe 1080x1920 ----------------------------------------- */
assets.push({
  name: "story-1080x1920",
  w: 1080, h: 1920,
  html: page(1080, 1920, true, `
    ${dust(9, true)}
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;padding:120px 84px 110px">
      ${logo(30, true)}
      <div class="serif" style="font-size:88px;line-height:1.08;margin-top:60px;letter-spacing:-.02em;color:${C.darkInk}">
        Twoje dane<br>zostają<br>u Ciebie.
      </div>
      <div style="font-size:32px;line-height:1.5;margin-top:40px;color:${C.darkInk2};max-width:800px">
        Bez konta. Bez serwera. Bez telemetrii. Aplikacja działa w Twojej
        przeglądarce, a całość stanu możesz w każdej chwili wyeksportować
        albo skasować.
      </div>
      <div style="margin-top:56px;display:flex;justify-content:center">
        <div style="width:470px;height:700px;border-radius:44px;overflow:hidden;border:12px solid #0D0F0A;
             box-shadow:0 40px 90px rgba(0,0,0,.5)">
          <img src="ekrany/konstytucja.png"
               style="display:block;width:100%;height:100%;object-fit:cover;object-position:top">
        </div>
      </div>
      <div style="margin-top:auto;display:flex;align-items:center;gap:18px">
        ${pill("Prawo wyjścia", { fg: C.darkBg, bg: C.darkAccent, size: 22, pad: "15px 28px" })}
        <span style="font-size:24px;color:${C.darkInk2}">otwarty JSON, jedno kliknięcie</span>
      </div>
    </div>
  `),
});

/* --- 6. LinkedIn 1200x627 ----------------------------------------------- */
assets.push({
  name: "linkedin-1200x627",
  w: 1200, h: 627,
  html: page(1200, 627, false, `
    ${dust(6, false)}
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;padding:62px 70px">
      <div style="display:flex;align-items:center;gap:18px">
        ${logo(26, false)}
        <span class="faint" style="font-size:19px">· aplikacja osobista</span>
      </div>
      <div class="serif" style="font-size:52px;line-height:1.12;margin-top:30px;letter-spacing:-.015em;max-width:1000px">
        Zbudowaliśmy aplikację rozwojową,<br>która potrafi powiedzieć „nie wiem”.
      </div>
      <div class="muted" style="font-size:22px;line-height:1.5;margin-top:24px;max-width:930px">
        Zasady nie są w regulaminie, tylko w silniku: zgoda ma cel i termin, hipoteza nigdy
        nie udaje faktu, a eksport całości danych jest zawsze bezpłatny.
      </div>
      <div style="margin-top:auto;display:flex;gap:52px">
        ${[
          ["5", "domen życia w równowadze"],
          ["8", "nazwanych powodów wstrzymania się"],
          ["0", "kont, serwerów i telemetrii"],
        ].map(([n, t]) => `
          <div style="display:flex;align-items:baseline;gap:14px">
            <span class="serif" style="font-size:52px;color:${C.verdigris};font-weight:600">${n}</span>
            <span class="muted" style="font-size:20px;max-width:230px;line-height:1.3">${t}</span>
          </div>`).join("")}
      </div>
    </div>
  `),
});

/* --- 7-9. Kadry do sklepu 1290x2796 ------------------------------------- */
const storeShots = [
  ["store-01-pulpit", "Pulpit, który nie krzyczy",
   "Pięć domen życia w równowadze. Bez rankingów, bez serii do utrzymania, bez presji.",
   "ekrany/pulpit.png", false],
  ["store-02-decyzje", "Rada, która zna swoje granice",
   "Rekomendacja z widocznym spektrum wariantów — albo uczciwe „wstrzymuję się” i powód.",
   "ekrany/decyzje.png", false],
  ["store-03-konstytucja", "Twoje prawa w menu,\nnie w regulaminie",
   "Eksport, import, korekta modelu i usunięcie wszystkiego — dwa kliknięcia stąd.",
   "ekrany/konstytucja.png", true],
];

storeShots.forEach(([name, head, sub, img, dark]) => {
  assets.push({
    name: `${name}-1290x2796`,
    w: 1290, h: 2796,
    html: page(1290, 2796, dark, `
      ${dust(8, dark)}
      <div style="position:absolute;inset:0;display:flex;flex-direction:column;padding:150px 96px 0;align-items:center">
        <div class="serif" style="font-size:96px;line-height:1.1;text-align:center;letter-spacing:-.02em;
             color:${dark ? C.darkInk : C.ink};white-space:pre-line">${head}</div>
        <div style="font-size:38px;line-height:1.45;text-align:center;margin-top:36px;max-width:1000px;
             color:${dark ? C.darkInk2 : C.ink2}">${sub}</div>
        <div style="margin-top:86px;width:1000px;border-radius:64px;overflow:hidden;
             border:14px solid ${dark ? "#0D0F0A" : C.ink};
             box-shadow:0 50px 120px rgba(38,42,33,${dark ? ".6" : ".3"})">
          <img src="${img}" style="display:block;width:100%">
        </div>
      </div>
    `),
  });
});

/* --- 10. Baner poziomy 1600x400 (nagłówek strony / newsletter) ---------- */
assets.push({
  name: "baner-1600x400",
  w: 1600, h: 400,
  html: page(1600, 400, false, `
    ${dust(5, false)}
    <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:space-between;padding:0 84px">
      <div>
        ${logo(26, false)}
        <div class="serif" style="font-size:54px;line-height:1.1;margin-top:18px;letter-spacing:-.015em">
          Rozwój bez oddawania sterów.
        </div>
        <div class="muted" style="font-size:22px;margin-top:16px">
          Aplikacja osobista, która pilnuje, żeby to nadal było Twoje życie.
        </div>
      </div>
      <div style="display:flex;flex-direction:column;gap:14px;align-items:flex-end">
        ${pill("Nie ocenia", { size: 18, pad: "13px 24px" })}
        ${pill("Nie rankinguje", { fg: C.clay, bg: C.clayTint, size: 18, pad: "13px 24px" })}
        ${pill("Nie zatrzymuje", { fg: C.warn, bg: C.warnTint, size: 18, pad: "13px 24px" })}
      </div>
    </div>
  `),
});

/* ================================================================ render */

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ executablePath: EXE });
  for (const a of assets) {
    const tmp = path.join(OUT, `_tmp-${a.name}.html`);
    fs.writeFileSync(tmp, a.html);
    const p = await browser.newPage({ viewport: { width: a.w, height: a.h }, deviceScaleFactor: 1 });
    await p.goto("file://" + tmp);
    await p.waitForTimeout(250);
    await p.screenshot({ path: path.join(OUT, a.name + ".png") });
    await p.close();
    fs.unlinkSync(tmp);
    console.log("✓", a.name + ".png", `${a.w}×${a.h}`);
  }
  await browser.close();
})();
