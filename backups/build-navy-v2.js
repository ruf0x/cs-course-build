// Builds PowerPoint decks (and PDF copies) from the Markdown files in topics/.
//
//   node build.js                      -> builds every topics/*.md into decks/ and decks/pdf/
//   node build.js topics/01-big-o.md   -> builds just that one
//   node build.js --no-pdf             -> skip the PDF export
//
// Write the content in Markdown (see README.md for the syntax). The design lives here,
// in THEME and the layout functions, so changing a color or font restyles every deck.

const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require("./lib/apply_theme.js");

// ───────────────────────────── Design ─────────────────────────────
const AUTHOR = "Ismail Cherrak"; // shown on every deck unless a topic sets `author:`
const FONT = "JetBrains Mono";
const THEME = {
  name: "CS Courses",
  headFontFace: FONT,
  bodyFontFace: FONT,
  colors: {
    dk1: "0B1626", // navy: title / section pages, code, key ideas
    lt1: "FFFFFF",
    dk2: "34465F", // secondary text on light
    lt2: "EEF5FD", // light blue tint: table rows, chips
    accent1: "7CC4FA", // light blue (on navy)
    accent2: "2474D1", // strong blue (on white)
    accent3: "BFE0FB", // pale blue: lines, borders
    accent4: "FFC46B", // amber: strings in code
    accent5: "1C5FAF", // inline `code` on white
    accent6: "5FD3B3", // mint: numbers in code
    hlink: "2474D1",
    folHlink: "1C5FAF",
  },
};
const T = THEME.colors;
const PAGE = "F7FAFE"; // content page background
const MUTED = "7F93B0"; // footer / captions / comments
const DIM = "22385A"; // subtle decoration on navy
const SOFT = "A9BCD6"; // secondary text on navy
const W = 13.333, H = 7.5, M = 0.75; // canvas (LAYOUT_WIDE) and side margin
const TOP = 1.95, BOTTOM = 6.65; // content area on content slides
const CH = 0.6; // JetBrains Mono: character width ≈ 0.6 em

// ───────────────────────────── Markdown parsing ─────────────────────────────
function parseTopic(src) {
  const lines = src.replace(/\r/g, "").split("\n");
  const meta = {};
  let i = 0;
  if (lines[0] && lines[0].trim() === "---") {
    for (i = 1; i < lines.length && lines[i].trim() !== "---"; i++) {
      const m = lines[i].match(/^(\w+)\s*:\s*(.*)$/);
      if (m) meta[m[1].toLowerCase()] = m[2].trim();
    }
    i++;
  }
  const items = [];
  let cur = null, inCode = null, inComment = false;
  const newSlide = (title) => ({ kind: "slide", title, list: [], code: null, table: null, callout: [], images: [], notes: [] });

  for (; i < lines.length; i++) {
    const raw = lines[i];
    const line = raw.trimEnd();
    if (inCode) {
      if (/^\s*```/.test(line)) { cur.code = inCode; inCode = null; } else inCode.lines.push(raw);
      continue;
    }
    if (inComment) { if (line.includes("-->")) inComment = false; continue; }
    if (/^\s*<!--/.test(line)) { if (!line.includes("-->")) inComment = true; continue; }
    if (!line.trim()) continue;

    let m;
    if ((m = line.match(/^#\s+(.*)/))) { cur = { kind: "section", title: m[1].trim(), desc: [] }; items.push(cur); continue; }
    if ((m = line.match(/^##\s+(.*)/))) { cur = newSlide(m[1].trim()); items.push(cur); continue; }
    if (!cur) continue;
    if (cur.kind === "section") { cur.desc.push(line.trim()); continue; }

    if ((m = line.match(/^\s*```(\w*)/))) { inCode = { lang: m[1] || "", lines: [] }; continue; }
    if ((m = line.match(/^\s*notes?\s*:\s*(.*)/i))) { cur.notes.push(m[1]); continue; }
    if ((m = line.match(/^\s*!\[(.*?)\]\((.*?)\)/))) { cur.images.push({ caption: m[1], src: m[2] }); continue; }
    if ((m = line.match(/^\s*>\s?(.*)/))) { cur.callout.push(m[1]); continue; }
    if (/^\s*\|/.test(line)) {
      if (/^\s*\|[\s:|-]+\|\s*$/.test(line)) continue;
      const cells = line.trim().replace(/^\||\|$/g, "").split("|").map((c) => c.trim());
      (cur.table = cur.table || []).push(cells);
      continue;
    }
    if ((m = raw.match(/^(\s*)[-*+]\s+(.*)/))) { cur.list.push({ text: m[2], level: Math.min(2, Math.floor(m[1].replace(/\t/g, "  ").length / 2)), type: "bullet" }); continue; }
    if ((m = raw.match(/^(\s*)\d+[.)]\s+(.*)/))) { cur.list.push({ text: m[2], level: Math.min(2, Math.floor(m[1].length / 2)), type: "number" }); continue; }
    cur.list.push({ text: line.trim(), level: 0, type: "para" });
  }
  if (inCode && cur) cur.code = inCode;
  return { meta, items };
}

// Inline **bold** and `code` -> pptxgenjs text runs.
function runs(text, base = {}, codeColor) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|`[^`]+`)/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push({ text: text.slice(last, m.index), options: { ...base } });
    const t = m[0];
    if (t.startsWith("**")) out.push({ text: t.slice(2, -2), options: { ...base, bold: true } });
    else out.push({ text: t.slice(1, -1), options: { ...base, bold: true, color: codeColor || base.color } });
    last = m.index + t.length;
  }
  if (last < text.length) out.push({ text: text.slice(last), options: { ...base } });
  if (!out.length) out.push({ text: "", options: { ...base } });
  return out;
}
const plain = (t) => t.replace(/\*\*|`/g, "");
const pad2 = (n) => String(n).padStart(2, "0");
// Rough line count for monospaced text of `size` pt in a box `w` inches wide.
const linesFor = (text, size, w) => Math.max(1, Math.ceil(plain(text).length / Math.max(1, Math.floor(w / (size * CH / 72)))));

// ───────────────────────────── Decorations ─────────────────────────────
function dots(pres, s, x, y, cols, rows, gap, color, d = 0.05) {
  for (let r = 0; r < rows; r++)
    for (let c = 0; c < cols; c++)
      s.addShape(pres.shapes.OVAL, { x: x + c * gap, y: y + r * gap, w: d, h: d, fill: { color }, line: { type: "none" }, objectName: "Dot" });
}
function corner(pres, s, x, y, dx, dy, color, len = 0.45, width = 1.5) {
  // An L-shaped bracket; dx/dy = +1 or -1 pick the direction of the arms.
  s.addShape(pres.shapes.LINE, { x: dx > 0 ? x : x - len, y, w: len, h: 0, line: { color, width }, objectName: "Corner" });
  s.addShape(pres.shapes.LINE, { x, y: dy > 0 ? y : y - len, w: 0, h: len, line: { color, width }, objectName: "Corner" });
}
function ring(pres, s, x, y, d, color, width = 1) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { type: "none" }, line: { color, width }, objectName: "Ring" });
}
function chip(pres, s, text, x, y, w, h, size = 14) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.06, fill: { color: T.dk1 }, line: { type: "none" }, objectName: "Chip" });
  s.addText(text, { x, y, w, h, fontSize: size, bold: true, color: pres.SchemeColor.accent1, align: "center", valign: "middle", margin: 0, isTextBox: true });
}

// ───────────────────────────── Deck builder ─────────────────────────────
function buildDeck(file) {
  const { meta, items } = parseTopic(fs.readFileSync(file, "utf8"));
  const deckTitle = meta.title || path.basename(file, ".md");
  const author = meta.author || AUTHOR;
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.title = deckTitle;
  pres.author = author;
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  const C = pres.SchemeColor;
  const xmlSafe = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
  const footer = xmlSafe(`${author.toLowerCase()}  ·  ${deckTitle.toLowerCase()}`);
  const footerObj = (color) => ({ text: { text: footer, options: { x: M, y: 6.95, w: 9, h: 0.3, fontSize: 9, color, margin: 0, valign: "middle", isTextBox: true, objectName: "Footer" } } });
  const slideNumber = (color) => ({ x: W - M - 1.4, y: 6.95, w: 0.8, h: 0.3, fontSize: 9, color, align: "right", valign: "middle", margin: 0 });

  pres.defineSlideMaster({
    title: "Title",
    background: { color: T.dk1 },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: M, y: 2.6, w: 8.0, h: 2.0, fontSize: 46, bold: true, color: C.background1, valign: "bottom", align: "left", margin: 0 }, text: "" } },
      { placeholder: { options: { name: "subtitle", type: "body", x: M, y: 4.8, w: 8.0, h: 0.9, fontSize: 18, color: SOFT, valign: "top", align: "left", margin: 0 }, text: "" } },
    ],
  });
  pres.defineSlideMaster({
    title: "Section",
    background: { color: T.dk1 },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: M, y: 3.55, w: 9.0, h: 1.2, fontSize: 38, bold: true, color: C.background1, valign: "top", align: "left", margin: 0 }, text: "" } },
      footerObj(MUTED),
    ],
    slideNumber: slideNumber(MUTED),
  });
  pres.defineSlideMaster({
    title: "Content",
    background: { color: PAGE },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: M, y: 0.82, w: W - 2 * M, h: 0.8, fontSize: 28, bold: true, color: C.text1, valign: "middle", align: "left", margin: 0 }, text: "" } },
      footerObj(MUTED),
    ],
    slideNumber: slideNumber(MUTED),
  });

  const sections = items.filter((x) => x.kind === "section");
  let sectionName = "Introduction";
  pres.addSection({ title: sectionName });

  // Title slide
  {
    const s = pres.addSlide({ masterName: "Title", sectionTitle: sectionName });
    ring(pres, s, 8.6, -1.6, 6.4, T.accent1, 1);
    ring(pres, s, 10.1, 2.9, 4.4, DIM, 1.25);
    ring(pres, s, 11.35, 4.15, 1.9, T.accent1, 1);
    dots(pres, s, 8.95, 5.05, 7, 5, 0.26, DIM, 0.06);
    corner(pres, s, 0.45, 0.45, 1, 1, T.accent1);
    corner(pres, s, W - 0.45, H - 0.45, -1, -1, T.accent1);
    s.addText([{ text: ">_ ", options: { color: C.accent1, bold: true } }, { text: author.toLowerCase(), options: { color: C.background1 } }], { x: M, y: 0.8, w: 7, h: 0.35, fontSize: 13, margin: 0, valign: "middle", isTextBox: true, objectName: "Author" });
    if (meta.course) s.addText(`// ${meta.course.toLowerCase()}`, { x: M, y: 2.2, w: 8, h: 0.35, fontSize: 14, bold: true, color: C.accent1, margin: 0, isTextBox: true, objectName: "Course" });
    s.addText(deckTitle, { placeholder: "title" });
    if (meta.subtitle) s.addText(meta.subtitle, { placeholder: "subtitle", bullet: false });
    s.addText(["course notes", meta.date].filter(Boolean).join("  ·  "), { x: M, y: 6.55, w: 6, h: 0.3, fontSize: 11, color: MUTED, margin: 0, isTextBox: true, objectName: "Date" });
  }

  // Contents (auto, from the # sections)
  if (sections.length >= 2) {
    const s = contentSlide(pres, { sectionName }, "Contents", `// ${deckTitle}`);
    const n = sections.length;
    const cols = n > 4 ? 2 : 1;
    const per = Math.ceil(n / cols);
    const colW = (W - 2 * M - (cols - 1) * 0.4) / cols;
    const rowH = Math.min(1.0, (BOTTOM - TOP) / per);
    sections.forEach((sec, k) => {
      const cx = M + Math.floor(k / per) * (colW + 0.4), y = TOP + (k % per) * rowH;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: cx, y, w: colW, h: rowH - 0.18, rectRadius: 0.08, fill: { color: T.lt1 }, line: { color: T.accent3, width: 1 }, objectName: `Contents card ${k + 1}` });
      chip(pres, s, pad2(k + 1), cx + 0.2, y + (rowH - 0.18 - 0.5) / 2, 0.62, 0.5, 15);
      s.addText(sec.title, { x: cx + 1.05, y, w: colW - 1.3, h: rowH - 0.18, fontSize: 18, color: C.text1, valign: "middle", margin: 0, isTextBox: true, objectName: `Contents item ${k + 1}` });
    });
  }

  let secNo = 0;
  for (const it of items) {
    if (it.kind === "section") {
      secNo++;
      sectionName = it.title;
      pres.addSection({ title: sectionName });
      const s = pres.addSlide({ masterName: "Section", sectionTitle: sectionName });
      dots(pres, s, 8.75, 1.2, 14, 14, 0.28, DIM, 0.06);
      ring(pres, s, 9.6, 1.9, 3.2, T.accent1, 1);
      corner(pres, s, 0.45, 0.45, 1, 1, T.accent1);
      corner(pres, s, W - 0.45, H - 0.45, -1, -1, T.accent1);
      s.addText(`// section ${secNo} of ${sections.length}`, { x: M, y: 0.8, w: 6, h: 0.35, fontSize: 13, color: C.accent1, margin: 0, valign: "middle", isTextBox: true });
      s.addText(pad2(secNo), { x: M, y: 1.55, w: 4, h: 1.9, fontSize: 110, bold: true, color: C.accent1, margin: 0, valign: "bottom", isTextBox: true, objectName: "Section number" });
      s.addText(it.title, { placeholder: "title" });
      if (it.desc.length) s.addText(it.desc.join(" "), { x: M, y: 4.85, w: 7.6, h: 1.4, fontSize: 15, color: SOFT, valign: "top", margin: 0, isTextBox: true, objectName: "Section summary" });
      continue;
    }
    renderSlide(pres, it, { sectionName, secNo, file });
  }
  return { pres, deckTitle };
}

// ───────────────────────────── Slide renderers ─────────────────────────────
function contentSlide(pres, ctx, title, eyebrowText) {
  const s = pres.addSlide({ masterName: "Content", sectionTitle: ctx.sectionName });
  s.addText(title, { placeholder: "title" });
  const eb = eyebrowText || (ctx.secNo ? `// ${pad2(ctx.secNo)} · ${ctx.sectionName}` : `// ${ctx.sectionName}`);
  s.addText(eb.toLowerCase(), { x: M, y: 0.48, w: 9, h: 0.3, fontSize: 11, bold: true, color: pres.SchemeColor.accent2, margin: 0, isTextBox: true, objectName: "Eyebrow" });
  dots(pres, s, W - M - 1.3, 0.42, 6, 3, 0.26, T.accent3, 0.06);
  corner(pres, s, W - 0.4, H - 0.4, -1, -1, T.accent3, 0.3, 1.25);
  return s;
}

function renderSlide(pres, sl, ctx) {
  const C = pres.SchemeColor;
  if (sl.title.startsWith("?")) {
    const q = sl.title.replace(/^\?\s*/, "");
    const s1 = contentSlide(pres, ctx, "Check yourself", `// quiz · ${ctx.sectionName}`);
    const cy = TOP + 0.15, chh = 3.3;
    s1.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M, y: cy, w: W - 2 * M, h: chh, rectRadius: 0.1, fill: { color: T.dk1 }, line: { type: "none" }, objectName: "Question card" });
    dots(pres, s1, W - M - 2.0, cy + chh - 1.0, 7, 3, 0.26, DIM, 0.06);
    s1.addShape(pres.shapes.OVAL, { x: M + 0.5, y: cy + 0.5, w: 1.1, h: 1.1, fill: { color: T.accent1 }, line: { type: "none" }, objectName: "Question mark circle" });
    s1.addText("?", { x: M + 0.5, y: cy + 0.5, w: 1.1, h: 1.1, fontSize: 44, bold: true, color: C.text1, align: "center", valign: "middle", margin: 0, isTextBox: true });
    s1.addText(runs(q, { fontSize: 22, color: C.background1 }, C.accent1), { x: M + 2.0, y: cy + 0.45, w: W - 2 * M - 2.6, h: chh - 0.9, valign: "top", margin: 0, isTextBox: true, objectName: "Question" });
    s1.addText("→ answer on the next slide", { x: M, y: cy + chh + 0.3, w: 8, h: 0.4, fontSize: 13, color: C.accent2, margin: 0, isTextBox: true });
    if (sl.notes.length) s1.addNotes(sl.notes.join("\n"));
    const s2 = contentSlide(pres, ctx, "Answer", `// quiz · ${ctx.sectionName}`);
    body(pres, s2, { ...sl, notes: [] }, ctx);
    return;
  }
  const s = contentSlide(pres, ctx, sl.title);
  body(pres, s, sl, ctx);
  if (sl.notes.length) s.addNotes(sl.notes.join("\n"));
}

function body(pres, s, sl, ctx) {
  const hasMain = sl.code || sl.table || sl.images.length;
  const hasList = sl.list.length > 0;
  const hasCallout = sl.callout.length > 0;
  const fullW = W - 2 * M, areaH = BOTTOM - TOP;
  const callout = sl.callout.join(" ");

  const isTerms = !hasMain && hasList && sl.list.length >= 2 && sl.list.length <= 6 && sl.list.every((x) => x.level === 0 && /^\*\*[^*]+\*\*\s*[:—–-]\s*/.test(x.text));
  const isSteps = !hasMain && hasList && sl.list.length >= 2 && sl.list.length <= 5 && sl.list.every((x) => x.type === "number" && x.level === 0);
  if (isTerms || isSteps) {
    let h0 = areaH;
    if (hasCallout) { keyIdea(pres, s, callout, M, BOTTOM - 0.95, fullW, 0.95, true); h0 -= 1.25; }
    return isTerms ? termCards(pres, s, sl.list, M, TOP, fullW, h0) : steps(pres, s, sl.list, M, TOP, fullW, Math.min(h0, 3.2));
  }

  if (hasMain) {
    const side = hasList || hasCallout;
    const mainW = side ? 7.2 : fullW;
    const mainX = side ? W - M - mainW : M;
    if (side) {
      const sideW = fullW - mainW - 0.45;
      let listH = areaH;
      if (hasCallout) {
        const ch = Math.min(areaH, keyIdeaHeight(callout, sideW));
        keyIdea(pres, s, callout, M, hasList ? BOTTOM - ch : TOP, sideW, ch, false);
        listH -= ch + 0.3;
      }
      if (hasList) bulletList(pres, s, sl.list, M, TOP, sideW, listH, -2);
    }
    const parts = [sl.code && "code", sl.table && "table", sl.images.length && "image"].filter(Boolean);
    const partH = (areaH - 0.3 * (parts.length - 1)) / parts.length;
    parts.forEach((p, k) => {
      const y = TOP + k * (partH + 0.3);
      if (p === "code") codeBlock(pres, s, sl.code, mainX, y, mainW, partH);
      if (p === "table") table(pres, s, sl.table, mainX, y, mainW, partH);
      if (p === "image") image(pres, s, sl.images[0], mainX, y, mainW, partH, ctx.file, !side);
    });
    return;
  }

  if (hasList && hasCallout) {
    const cw = 4.5;
    bulletList(pres, s, sl.list, M, TOP, fullW - cw - 0.45, areaH, 0);
    keyIdea(pres, s, callout, W - M - cw, TOP, cw, Math.min(areaH, keyIdeaHeight(callout, cw)), false);
    return;
  }
  if (hasCallout) return statement(pres, s, callout, M, TOP, fullW, areaH);
  if (hasList) {
    const simple = sl.list.length <= 5 && sl.list.every((x) => x.level === 0 && x.type === "bullet" && plain(x.text).length <= 110);
    return simple ? numberedRows(pres, s, sl.list, M, TOP, fullW, areaH) : bulletList(pres, s, sl.list, M, TOP, fullW, areaH, 0);
  }
}

function listFontSize(list, w, h, delta) {
  // Largest size (18 → 14) at which the list fits the box.
  for (let size = 18 + delta; size > 14; size--) {
    const height = list.reduce((a, x) => a + linesFor(x.text, x.level ? size - 2 : size, w - 0.45) * size * 1.25 / 72 + (x.level ? 4 : 10) / 72, 0);
    if (height <= h) return size;
  }
  return 14;
}

function bulletList(pres, s, list, x, y, w, h, delta) {
  const C = pres.SchemeColor;
  const fs0 = listFontSize(list, w, h, delta);
  const paras = [];
  list.forEach((it, k) => {
    const base = { fontSize: it.level ? fs0 - 2 : fs0, color: it.level ? C.text2 : C.text1 };
    const r = runs(it.text, base, C.accent5);
    Object.assign(r[0].options, {
      bullet: it.type === "para" ? false : it.type === "number" ? { type: "number", indent: 24 } : { characterCode: it.level ? "2013" : "25B8", indent: 22 },
      indentLevel: it.level,
      paraSpaceAfter: it.level ? 4 : 10,
    });
    if (k < list.length - 1) r[r.length - 1].options.breakLine = true;
    paras.push(...r);
  });
  s.addText(paras, { x, y, w, h, valign: "top", margin: [4, 4, 4, 0], isTextBox: true, objectName: "Bullets" });
}

function numberedRows(pres, s, list, x, y, w, h) {
  const C = pres.SchemeColor;
  const rowH = Math.min(1.0, h / list.length);
  list.forEach((it, k) => {
    const ry = y + k * rowH;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: ry, w, h: rowH - 0.16, rectRadius: 0.08, fill: { color: T.lt1 }, line: { color: T.accent3, width: 1 }, objectName: `Row ${k + 1}` });
    chip(pres, s, pad2(k + 1), x + 0.22, ry + (rowH - 0.16 - 0.48) / 2, 0.62, 0.48, 14);
    s.addText(runs(it.text, { fontSize: 16, color: C.text1 }, C.accent5), { x: x + 1.1, y: ry, w: w - 1.35, h: rowH - 0.16, valign: "middle", margin: 0, isTextBox: true, objectName: `Row ${k + 1} text` });
  });
}

function termCards(pres, s, list, x, y, w, h) {
  const C = pres.SchemeColor;
  const n = list.length;
  const cols = n <= 3 ? n : n === 4 ? 2 : 3;
  const rows = Math.ceil(n / cols);
  const gap = 0.3;
  const cw = (w - gap * (cols - 1)) / cols, ch = Math.min(2.6, (h - gap * (rows - 1)) / rows);
  list.forEach((it, k) => {
    const m = it.text.match(/^\*\*([^*]+)\*\*\s*[:—–-]\s*(.*)$/);
    const cx = x + (k % cols) * (cw + gap), cy = y + Math.floor(k / cols) * (ch + gap);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: cx, y: cy, w: cw, h: ch, rectRadius: 0.08, fill: { color: T.lt1 }, line: { color: T.accent3, width: 1 }, objectName: `Card ${k + 1}` });
    corner(pres, s, cx + 0.22, cy + 0.22, 1, 1, T.accent2, 0.22, 1.5);
    s.addText(pad2(k + 1), { x: cx + cw - 0.9, y: cy + 0.25, w: 0.65, h: 0.3, fontSize: 10, color: MUTED, align: "right", margin: 0, isTextBox: true });
    s.addText(m[1], { x: cx + 0.45, y: cy + 0.32, w: cw - 1.4, h: 0.5, fontSize: 17, bold: true, color: C.accent2, valign: "middle", margin: 0, isTextBox: true, objectName: `Card ${k + 1} term` });
    s.addText(runs(m[2], { fontSize: 14, color: C.text2 }, C.accent5), { x: cx + 0.45, y: cy + 0.95, w: cw - 0.8, h: ch - 1.15, valign: "top", margin: 0, isTextBox: true, objectName: `Card ${k + 1} definition` });
  });
}

function steps(pres, s, list, x, y, w, h) {
  const C = pres.SchemeColor;
  const n = list.length, gap = 0.45;
  const cw = (w - gap * (n - 1)) / n;
  const size = n >= 5 ? 13 : 15;
  const maxLines = Math.max(...list.map((it) => linesFor(it.text, size, cw - 0.6)));
  h = Math.min(h, 1.05 + maxLines * size * 1.3 / 72 + 0.45);
  list.forEach((it, k) => {
    const cx = x + k * (cw + gap);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: cx, y, w: cw, h, rectRadius: 0.08, fill: { color: T.lt1 }, line: { color: T.accent3, width: 1 }, objectName: `Step ${k + 1}` });
    chip(pres, s, pad2(k + 1), cx + 0.3, y + 0.3, 0.7, 0.5, 15);
    s.addText(runs(it.text, { fontSize: size, color: C.text1 }, C.accent5), { x: cx + 0.3, y: y + 1.05, w: cw - 0.6, h: h - 1.3, valign: "top", margin: 0, isTextBox: true, objectName: `Step ${k + 1} text` });
    if (k < n - 1) s.addText("→", { x: cx + cw, y: y + 0.3, w: gap, h: 0.5, fontSize: 18, bold: true, color: C.accent2, align: "center", valign: "middle", margin: 0, isTextBox: true });
  });
}

function keyIdeaSize(text) { return plain(text).length > 140 ? 14 : 16; }
function keyIdeaHeight(text, w) {
  const size = keyIdeaSize(text);
  return Math.max(1.6, 0.75 + (linesFor(text, size, w - 0.7) + 1) * size * 1.25 / 72 + 0.3);
}
function keyIdea(pres, s, text, x, y, w, h, wide) {
  const C = pres.SchemeColor;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: T.dk1 }, line: { type: "none" }, objectName: "Key idea panel" });
  if (wide) {
    s.addText("> key idea", { x: x + 0.35, y, w: 1.9, h, fontSize: 12, bold: true, color: C.accent1, valign: "middle", margin: 0, isTextBox: true });
    s.addText(runs(text, { fontSize: 15, color: C.background1 }, C.accent1), { x: x + 2.3, y, w: w - 2.6, h, valign: "middle", margin: 0, isTextBox: true, objectName: "Key idea" });
  } else {
    s.addText("> key idea", { x: x + 0.35, y: y + 0.3, w: w - 0.7, h: 0.3, fontSize: 12, bold: true, color: C.accent1, margin: 0, isTextBox: true });
    s.addText(runs(text, { fontSize: keyIdeaSize(text), color: C.background1 }, C.accent1), { x: x + 0.35, y: y + 0.75, w: w - 0.7, h: h - 1.0, valign: "top", margin: 0, isTextBox: true, objectName: "Key idea" });
  }
}

function statement(pres, s, text, x, y, w, h) {
  const C = pres.SchemeColor;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.1, fill: { color: T.dk1 }, line: { type: "none" }, objectName: "Statement panel" });
  ring(pres, s, x + w - 2.7, y + h - 2.3, 1.8, DIM, 1.25);
  dots(pres, s, x + w - 2.3, y + 0.5, 7, 4, 0.26, DIM, 0.06);
  corner(pres, s, x + 0.4, y + 0.4, 1, 1, T.accent1, 0.35);
  s.addText("> key idea", { x: x + 0.7, y: y + 0.55, w: 4, h: 0.35, fontSize: 13, bold: true, color: C.accent1, margin: 0, isTextBox: true });
  const size = plain(text).length > 160 ? 20 : 24;
  s.addText(runs(text, { fontSize: size, color: C.background1 }, C.accent1), { x: x + 0.7, y: y + 1.1, w: w - 4.2, h: h - 1.6, valign: "middle", margin: 0, isTextBox: true, objectName: "Statement" });
}

// ── Code with light syntax highlighting ──
const KEYWORDS = new Set("def return if elif else for while in not and or is class import from as with try except finally raise pass break continue lambda yield None True False function const let var new this null undefined true false public private protected static void int long float double char bool boolean string String struct typedef include using namespace switch case default do".split(" "));
function highlight(line, size, C) {
  const base = { fontSize: size, color: "E6EEF8" };
  const out = [];
  const re = /(#.*$|\/\/.*$|--.*$)|("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|\b(\d+(?:\.\d+)?)\b|\b([A-Za-z_]\w*)\b/g;
  let last = 0, m;
  const push = (text, opts) => text && out.push({ text, options: { ...base, ...opts } });
  while ((m = re.exec(line))) {
    push(line.slice(last, m.index), {});
    if (m[1]) push(m[1], { color: MUTED, italic: true });
    else if (m[2]) push(m[2], { color: T.accent4 });
    else if (m[3]) push(m[3], { color: T.accent6 });
    else if (KEYWORDS.has(m[4])) push(m[4], { color: T.accent1, bold: true });
    else if (line[re.lastIndex] === "(") push(m[4], { color: "9FD8FF" });
    else push(m[4], {});
    last = re.lastIndex;
  }
  push(line.slice(last), {});
  if (!out.length) out.push({ text: "\u00A0", options: { ...base } });
  out[0].text = out[0].text.replace(/^ +/, (sp) => "\u00A0".repeat(sp.length));
  return out;
}

function codeBlock(pres, s, code, x, y, w, h) {
  const C = pres.SchemeColor;
  let lines = code.lines.map((l) => l.replace(/\t/g, "    ").trimEnd());
  while (lines.length && !lines[lines.length - 1]) lines.pop();
  const ind = Math.min(...lines.filter((l) => l.trim()).map((l) => l.match(/^ */)[0].length));
  lines = lines.map((l) => l.slice(isFinite(ind) ? ind : 0));
  const longest = Math.max(...lines.map((l) => l.length), 1);
  const innerW = w - 0.7, innerH = h - 0.95;
  let size = 16;
  while (size > 10 && (longest * size * CH / 72 > innerW || lines.length * size * 1.25 / 72 > innerH)) size--;
  h = Math.min(h, 0.7 + lines.length * size * 1.25 / 72 + 0.45);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: T.dk1 }, line: { type: "none" }, objectName: "Code panel" });
  ["FF6B6B", "FFC46B", "5FD3B3"].forEach((c, k) => s.addShape(pres.shapes.OVAL, { x: x + 0.3 + k * 0.24, y: y + 0.24, w: 0.13, h: 0.13, fill: { color: c }, line: { type: "none" }, objectName: "Window dot" }));
  s.addText((code.lang || "code").toLowerCase(), { x: x + w - 2.3, y: y + 0.14, w: 2.0, h: 0.32, fontSize: 10, color: C.accent1, align: "right", margin: 0, isTextBox: true });
  s.addShape(pres.shapes.LINE, { x, y: y + 0.55, w, h: 0, line: { color: DIM, width: 1 }, objectName: "Code header rule" });
  const textRuns = [];
  lines.forEach((l, k) => {
    const r = highlight(l, size, C);
    if (k < lines.length - 1) r[r.length - 1].options.breakLine = true;
    textRuns.push(...r);
  });
  s.addText(textRuns, { x: x + 0.35, y: y + 0.72, w: innerW, h: h - 0.9, valign: "top", margin: 0, isTextBox: true, objectName: "Code" });
}

function table(pres, s, rows, x, y, w, h) {
  const C = pres.SchemeColor;
  const nCols = Math.max(...rows.map((r) => r.length));
  const size = rows.length > 8 ? 12 : 14;
  const data = rows.map((r, ri) =>
    Array.from({ length: nCols }, (_, ci) => {
      const head = ri === 0;
      return {
        text: runs(r[ci] || "", { fontSize: head ? 12 : size, color: head ? C.accent1 : ci === 0 ? C.accent2 : C.text1, bold: head || ci === 0 }, C.accent5),
        options: { valign: "middle", margin: [5, 10, 5, 12], fill: { color: head ? T.dk1 : ri % 2 ? T.lt1 : T.lt2 } },
      };
    })
  );
  const rowH = Math.min(0.56, h / rows.length);
  s.addTable(data, { x, y, w, colW: Array(nCols).fill(w / nCols), rowH, border: { type: "solid", pt: 0.75, color: T.accent3 }, objectName: "Table" });
}

function imageSize(p) {
  // Reads pixel size from PNG / JPEG headers, so pictures keep their proportions.
  const b = fs.readFileSync(p);
  if (b.readUInt32BE(0) === 0x89504e47) return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
  let i = 2;
  while (i < b.length) {
    if (b[i] !== 0xff) { i++; continue; }
    const mk = b[i + 1], len = b.readUInt16BE(i + 2);
    if (mk >= 0xc0 && mk <= 0xcf && mk !== 0xc4 && mk !== 0xc8 && mk !== 0xcc) return { w: b.readUInt16BE(i + 7), h: b.readUInt16BE(i + 5) };
    i += 2 + len;
  }
  return null;
}

function image(pres, s, img, x, y, w, h, file, center) {
  const C = pres.SchemeColor;
  const p = path.resolve(path.dirname(file), img.src);
  if (!fs.existsSync(p)) {
    console.warn(`  ! image not found: ${img.src}`);
    s.addText(`image missing: ${img.src}`, { x, y, w, h, fontSize: 13, color: MUTED, align: "center", valign: "middle", fill: { color: T.lt2 }, isTextBox: true });
    return;
  }
  const pad = 0.25, capH = img.caption ? 0.45 : 0;
  const boxW = w - 2 * pad, boxH = h - 2 * pad - capH;
  let iw = boxW, ih = boxH;
  const dim = imageSize(p);
  if (dim) { const r = dim.w / dim.h; if (boxW / boxH > r) iw = boxH * r; else ih = boxW / r; }
  const fw = iw + 2 * pad, fh = ih + 2 * pad + capH;
  const fx = center ? x + (w - fw) / 2 : x + (w - fw) / 2, fy = y + (h - fh) / 2;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: fx, y: fy, w: fw, h: fh, rectRadius: 0.08, fill: { color: T.lt1 }, line: { color: T.accent3, width: 1 }, objectName: "Figure frame" });
  corner(pres, s, fx - 0.12, fy - 0.12, 1, 1, T.accent2, 0.3, 1.5);
  corner(pres, s, fx + fw + 0.12, fy + fh + 0.12, -1, -1, T.accent2, 0.3, 1.5);
  s.addImage({ path: p, x: fx + pad, y: fy + pad, w: iw, h: ih, altText: img.caption || path.basename(p), objectName: "Figure" });
  if (img.caption) s.addText(`fig. ${img.caption}`, { x: fx + pad, y: fy + pad + ih + 0.08, w: iw, h: 0.32, fontSize: 10, italic: true, color: MUTED, margin: 0, isTextBox: true, objectName: "Caption" });
}

// pptxgenjs writes a <a:pPr> before every run of a multi-run paragraph; only the first is valid
// (later ones drop the bullet). Keep the first pPr in each paragraph, remove the rest.
async function fixParagraphProps(file) {
  const JSZip = require(require.resolve("jszip", { paths: [require.resolve("pptxgenjs")] }));
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  const pPr = /<a:pPr\b[^>]*?(?:\/>|>[\s\S]*?<\/a:pPr>)/g;
  for (const name of Object.keys(zip.files).filter((n) => /^ppt\/slides\/slide\d+\.xml$/.test(n))) {
    const xml = await zip.file(name).async("string");
    const fixed = xml.replace(/<a:p>([\s\S]*?)<\/a:p>/g, (all, inner) => {
      let seen = false;
      return "<a:p>" + inner.replace(pPr, (m) => (seen ? "" : ((seen = true), m))) + "</a:p>";
    });
    if (fixed !== xml) zip.file(name, fixed);
  }
  fs.writeFileSync(file, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

// ───────────────────────────── PDF export (LibreOffice) ─────────────────────────────
function findSoffice() {
  return [
    process.env.SOFFICE,
    "C:\\Program Files\\LibreOffice\\program\\soffice.exe",
    "C:\\Program Files (x86)\\LibreOffice\\program\\soffice.exe",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    "/usr/bin/soffice",
  ].filter(Boolean).find((p) => fs.existsSync(p));
}
function toPdf(pptxPath, outDir) {
  const soffice = findSoffice();
  if (!soffice) return false;
  const { execFileSync } = require("child_process");
  fs.mkdirSync(outDir, { recursive: true });
  execFileSync(soffice, ["--headless", "--norestore", "--convert-to", "pdf", "--outdir", outDir, pptxPath], { stdio: "ignore", timeout: 180000 });
  return true;
}

// ───────────────────────────── Main ─────────────────────────────
(async () => {
  const root = __dirname;
  const args = process.argv.slice(2).filter((a) => !a.startsWith("--"));
  const files = args.length ? args.map((a) => path.resolve(a)) : fs.readdirSync(path.join(root, "topics")).filter((f) => f.endsWith(".md") && !f.startsWith("_")).sort().map((f) => path.join(root, "topics", f));
  fs.mkdirSync(path.join(root, "decks"), { recursive: true });
  for (const f of files) {
    const out = path.join(root, "decks", path.basename(f, ".md") + ".pptx");
    try {
      const { pres } = buildDeck(f);
      await pres.writeFile({ fileName: out });
      await applyTheme(out, THEME);
      await fixParagraphProps(out);
      console.log(`✓ ${path.relative(root, out)}`);
    } catch (e) {
      if (e.code === "EBUSY") console.error(`✗ ${path.basename(out)} is open in PowerPoint — close it and rebuild.`);
      else { console.error(`✗ ${path.basename(f)}: ${e.message}`); process.exitCode = 1; }
      continue;
    }
    if (process.argv.includes("--no-pdf")) continue;
    try {
      if (toPdf(out, path.join(root, "decks", "pdf"))) console.log(`✓ ${path.join("decks", "pdf", path.basename(out, ".pptx") + ".pdf")}`);
      else if (!toPdf.warned) { toPdf.warned = true; console.warn("  (LibreOffice not found — skipping PDF export)"); }
    } catch (e) { console.warn(`  ! PDF export failed: ${e.message}`); }
  }
})();
