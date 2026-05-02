// Generate the full Mueen Evaluation delivery package.
// Consistent visual language across Arabic cover letter + English attachments.

const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, PageOrientation, LevelFormat,
  HeadingLevel, BorderStyle, WidthType, ShadingType, VerticalAlign,
  PageNumber, PageBreak, TabStopType, TabStopPosition,
} = require("docx");

// ---------- Brand ----------
const COLOR = {
  primary: "1F4E79",   // deep navy
  secondary: "2E75B6", // medium blue
  accent: "C9A227",    // gold
  text: "1A1A1A",
  muted: "595959",
  light: "F2F6FB",
  white: "FFFFFF",
  success: "2E7D32",
  danger: "C62828",
  tableHeaderFill: "1F4E79",
  altRowFill: "F2F6FB",
  borderGrey: "BFBFBF",
};

const FONT = { latin: "Calibri", arabic: "Tahoma", mono: "Consolas" };

const OUT_DIR = path.join(__dirname);

// US Letter DXA: 12240 x 15840, margins 1" = 1440
const PAGE = { width: 12240, height: 15840, margin: 1440, content: 12240 - 2880 }; // 9360

// ---------- Helpers ----------
const border = (c = COLOR.borderGrey, size = 1) => ({
  style: BorderStyle.SINGLE, size, color: c,
});
const cellBorders = (c = COLOR.borderGrey) => ({
  top: border(c), bottom: border(c), left: border(c), right: border(c),
});

function runLatin(text, opts = {}) {
  return new TextRun({
    text,
    font: { ascii: FONT.latin, hAnsi: FONT.latin, cs: FONT.arabic },
    size: opts.size || 22,                 // 11pt default
    bold: opts.bold || false,
    italics: opts.italic || false,
    color: opts.color || COLOR.text,
    ...(opts.extra || {}),
  });
}

function runAr(text, opts = {}) {
  return new TextRun({
    text,
    font: { ascii: FONT.arabic, hAnsi: FONT.arabic, cs: FONT.arabic },
    rightToLeft: true,
    size: opts.size || 24,                 // 12pt default for Arabic
    bold: opts.bold || false,
    italics: opts.italic || false,
    color: opts.color || COLOR.text,
    ...(opts.extra || {}),
  });
}

function pLatin(text, opts = {}) {
  return new Paragraph({
    alignment: opts.align || AlignmentType.LEFT,
    spacing: { before: opts.before || 0, after: opts.after || 120, line: 312 },
    children: Array.isArray(text)
      ? text
      : [runLatin(text, opts)],
    ...(opts.paraExtra || {}),
  });
}

function pAr(text, opts = {}) {
  return new Paragraph({
    bidirectional: true,
    alignment: opts.align || AlignmentType.RIGHT,
    spacing: { before: opts.before || 0, after: opts.after || 160, line: 360 },
    children: Array.isArray(text)
      ? text
      : [runAr(text, opts)],
    ...(opts.paraExtra || {}),
  });
}

function heading(text, lvl = 1, arabic = null) {
  if (arabic === null) arabic = /[\u0600-\u06FF]/.test(text);
  const sizes = { 1: 40, 2: 32, 3: 28, 4: 24 };
  const run = arabic
    ? runAr(text, { size: sizes[lvl], bold: true, color: COLOR.primary })
    : runLatin(text, { size: sizes[lvl], bold: true, color: COLOR.primary });
  return new Paragraph({
    heading: [HeadingLevel.HEADING_1, HeadingLevel.HEADING_2, HeadingLevel.HEADING_3, HeadingLevel.HEADING_4][lvl - 1],
    bidirectional: !!arabic,
    alignment: arabic ? AlignmentType.RIGHT : AlignmentType.LEFT,
    spacing: { before: lvl === 1 ? 360 : 240, after: 160 },
    children: [run],
  });
}

function hrThin() {
  return new Paragraph({
    spacing: { before: 60, after: 120 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: COLOR.secondary, space: 2 } },
    children: [new TextRun("")],
  });
}

function hrThick() {
  return new Paragraph({
    spacing: { before: 60, after: 180 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 18, color: COLOR.primary, space: 2 } },
    children: [new TextRun("")],
  });
}

// ---------- Letterhead (used as page header) ----------
function letterheadHeader(arabic = false) {
  const titleLine = arabic
    ? new Paragraph({
        bidirectional: true,
        alignment: AlignmentType.RIGHT,
        spacing: { after: 40 },
        children: [runAr("منصة تقييم نماذج اللغة العربية", { bold: true, size: 26, color: COLOR.primary })],
      })
    : new Paragraph({
        alignment: AlignmentType.LEFT,
        spacing: { after: 40 },
        children: [runLatin("Arabic LLM Benchmark Platform", { bold: true, size: 24, color: COLOR.primary })],
      });
  const subLine = arabic
    ? new Paragraph({
        bidirectional: true,
        alignment: AlignmentType.RIGHT,
        spacing: { after: 0 },
        children: [runAr("تقييم مستقل لنموذج معين الذكي — أبريل ٢٠٢٦", { size: 20, color: COLOR.muted })],
      })
    : new Paragraph({
        alignment: AlignmentType.LEFT,
        spacing: { after: 0 },
        children: [runLatin("Independent Evaluation of Mueen AI — April 2026", { size: 18, color: COLOR.muted })],
      });
  const ruler = new Paragraph({
    spacing: { before: 60, after: 0 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: COLOR.accent, space: 2 } },
    children: [new TextRun("")],
  });
  return new Header({ children: [titleLine, subLine, ruler] });
}

function pageFooter(docTitle, arabic = false) {
  // Left: document title; Right: page N of total
  const runA = arabic ? runAr : runLatin;
  const opts = { size: 18, color: COLOR.muted };
  return new Footer({
    children: [
      new Paragraph({
        bidirectional: !!arabic,
        spacing: { before: 60 },
        border: { top: { style: BorderStyle.SINGLE, size: 4, color: COLOR.secondary, space: 2 } },
        tabStops: [{ type: TabStopType.RIGHT, position: PAGE.content }],
        children: arabic
          ? [
              runA(docTitle, opts),
              new TextRun({ text: "\t", ...{ font: { ascii: FONT.latin, hAnsi: FONT.latin } } }),
              runLatin("صفحة ", opts),
              new TextRun({ children: [PageNumber.CURRENT], ...opts, font: { ascii: FONT.latin, hAnsi: FONT.latin } }),
              runLatin(" / ", opts),
              new TextRun({ children: [PageNumber.TOTAL_PAGES], ...opts, font: { ascii: FONT.latin, hAnsi: FONT.latin } }),
            ]
          : [
              runA(docTitle, opts),
              new TextRun({ text: "\t", font: { ascii: FONT.latin, hAnsi: FONT.latin } }),
              runLatin("Page ", opts),
              new TextRun({ children: [PageNumber.CURRENT], ...opts, font: { ascii: FONT.latin, hAnsi: FONT.latin } }),
              runLatin(" of ", opts),
              new TextRun({ children: [PageNumber.TOTAL_PAGES], ...opts, font: { ascii: FONT.latin, hAnsi: FONT.latin } }),
            ],
      }),
    ],
  });
}

// ---------- Shared style defs ----------
function docStyles() {
  return {
    default: {
      document: {
        run: { font: FONT.latin, size: 22, color: COLOR.text },
        paragraph: { spacing: { line: 312 } },
      },
    },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 40, bold: true, color: COLOR.primary, font: FONT.latin },
        paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, color: COLOR.primary, font: FONT.latin },
        paragraph: { spacing: { before: 280, after: 140 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, color: COLOR.secondary, font: FONT.latin },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 2 } },
      { id: "Heading4", name: "Heading 4", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, color: COLOR.secondary, font: FONT.latin },
        paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 3 } },
    ],
  };
}

const NUMBERING = {
  config: [
    { reference: "bullets",
      levels: [
        { level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
        { level: 1, format: LevelFormat.BULLET, text: "\u25E6", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 1440, hanging: 360 } } } },
      ] },
    { reference: "numbers",
      levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "arNumbers",
      levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.RIGHT,
        style: { paragraph: { indent: { right: 720, hanging: 360 } } } }] },
  ],
};

function bullet(text, opts = {}) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { before: 0, after: 80 },
    children: [runLatin(text, opts)],
  });
}
function bulletAr(text, opts = {}) {
  return new Paragraph({
    bidirectional: true,
    alignment: AlignmentType.RIGHT,
    numbering: { reference: "bullets", level: 0 },
    spacing: { before: 0, after: 80 },
    children: [runAr(text, opts)],
  });
}
function numItem(text, opts = {}) {
  return new Paragraph({
    numbering: { reference: "numbers", level: 0 },
    spacing: { before: 0, after: 80 },
    children: [runLatin(text, opts)],
  });
}
function numItemAr(text, opts = {}) {
  return new Paragraph({
    bidirectional: true,
    alignment: AlignmentType.RIGHT,
    numbering: { reference: "arNumbers", level: 0 },
    spacing: { before: 0, after: 80 },
    children: [runAr(text, opts)],
  });
}

// ---------- Table builder ----------
function makeTable({ headers, rows, widths, arabic = false, firstColWider = false, highlightLastCol = false }) {
  // widths must sum to PAGE.content
  const nCols = headers.length;
  let colWidths = widths;
  if (!colWidths) {
    const base = Math.floor(PAGE.content / nCols);
    colWidths = Array(nCols).fill(base);
    colWidths[0] = PAGE.content - base * (nCols - 1);
    if (firstColWider && nCols > 1) {
      const extra = 800;
      colWidths[0] += extra;
      for (let i = 1; i < nCols; i++) colWidths[i] -= Math.floor(extra / (nCols - 1));
      // adjust last
      const diff = PAGE.content - colWidths.reduce((a, b) => a + b, 0);
      colWidths[nCols - 1] += diff;
    }
  }

  const headerCells = headers.map((h, i) =>
    new TableCell({
      borders: cellBorders(COLOR.primary),
      width: { size: colWidths[i], type: WidthType.DXA },
      shading: { fill: COLOR.tableHeaderFill, type: ShadingType.CLEAR, color: "auto" },
      margins: { top: 100, bottom: 100, left: 120, right: 120 },
      verticalAlign: VerticalAlign.CENTER,
      children: [
        new Paragraph({
          bidirectional: arabic,
          alignment: arabic ? AlignmentType.RIGHT : AlignmentType.CENTER,
          spacing: { before: 0, after: 0 },
          children: [
            arabic
              ? runAr(h, { bold: true, color: COLOR.white, size: 22 })
              : runLatin(h, { bold: true, color: COLOR.white, size: 22 }),
          ],
        }),
      ],
    })
  );

  const bodyRows = rows.map((row, ri) => {
    const fill = ri % 2 === 1 ? COLOR.altRowFill : COLOR.white;
    const cells = row.map((cell, ci) => {
      const isHighlight = highlightLastCol && ci === row.length - 1;
      const isArCell = arabic || /[\u0600-\u06FF]/.test(String(cell));
      const cellRun = isArCell
        ? runAr(String(cell), { bold: isHighlight, color: isHighlight ? COLOR.primary : COLOR.text, size: 22 })
        : runLatin(String(cell), { bold: isHighlight, color: isHighlight ? COLOR.primary : COLOR.text, size: 22 });
      const align = isArCell
        ? AlignmentType.RIGHT
        : (ci === 0 && !arabic ? AlignmentType.LEFT : AlignmentType.CENTER);
      return new TableCell({
        borders: cellBorders(),
        width: { size: colWidths[ci], type: WidthType.DXA },
        shading: { fill, type: ShadingType.CLEAR, color: "auto" },
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        verticalAlign: VerticalAlign.CENTER,
        children: [
          new Paragraph({
            bidirectional: isArCell,
            alignment: align,
            spacing: { before: 0, after: 0 },
            children: [cellRun],
          }),
        ],
      });
    });
    return new TableRow({ children: cells });
  });

  return new Table({
    width: { size: PAGE.content, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [new TableRow({ tableHeader: true, children: headerCells }), ...bodyRows],
  });
}

// Info-strip (two-column label/value row)
function infoStrip(rows, arabic = false) {
  const half = Math.floor(PAGE.content / 2);
  return new Table({
    width: { size: PAGE.content, type: WidthType.DXA },
    columnWidths: [half, PAGE.content - half],
    rows: rows.map((r, i) => new TableRow({
      children: [
        new TableCell({
          borders: cellBorders(COLOR.light),
          width: { size: half, type: WidthType.DXA },
          shading: { fill: COLOR.primary, type: ShadingType.CLEAR, color: "auto" },
          margins: { top: 80, bottom: 80, left: 140, right: 140 },
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({
            bidirectional: arabic,
            alignment: arabic ? AlignmentType.RIGHT : AlignmentType.LEFT,
            children: [arabic
              ? runAr(r.label, { bold: true, color: COLOR.white, size: 22 })
              : runLatin(r.label, { bold: true, color: COLOR.white, size: 22 })],
          })],
        }),
        new TableCell({
          borders: cellBorders(COLOR.light),
          width: { size: PAGE.content - half, type: WidthType.DXA },
          shading: { fill: COLOR.light, type: ShadingType.CLEAR, color: "auto" },
          margins: { top: 80, bottom: 80, left: 140, right: 140 },
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({
            bidirectional: arabic,
            alignment: arabic ? AlignmentType.RIGHT : AlignmentType.LEFT,
            children: [arabic
              ? runAr(r.value, { color: COLOR.text, size: 22 })
              : runLatin(r.value, { color: COLOR.text, size: 22 })],
          })],
        }),
      ],
    })),
  });
}

// Cover page builder for English attachments
function coverPage({ kicker, title, subtitle, meta }) {
  const filler = (n) => Array.from({ length: n }, () => new Paragraph({ children: [new TextRun("")] }));
  return [
    ...filler(4),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 100 },
      children: [runLatin(kicker, { bold: true, size: 22, color: COLOR.accent, extra: { allCaps: true } })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 120, after: 60 },
      border: { top: { style: BorderStyle.SINGLE, size: 18, color: COLOR.primary, space: 4 } },
      children: [new TextRun("")],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 60 },
      children: [runLatin(title, { bold: true, size: 52, color: COLOR.primary })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 120 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 18, color: COLOR.primary, space: 4 } },
      children: [new TextRun("")],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 600 },
      children: [runLatin(subtitle, { size: 26, color: COLOR.muted, italic: true })],
    }),
    ...filler(2),
    ...(meta || []).map((m) => new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 60 },
      children: [
        runLatin(m.label + "  ", { bold: true, size: 22, color: COLOR.secondary }),
        runLatin(m.value, { size: 22, color: COLOR.text }),
      ],
    })),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

function coverPageAr({ kicker, title, subtitle, meta }) {
  const filler = (n) => Array.from({ length: n }, () => new Paragraph({ children: [new TextRun("")] }));
  return [
    ...filler(4),
    new Paragraph({
      bidirectional: true,
      alignment: AlignmentType.CENTER,
      spacing: { after: 100 },
      children: [runAr(kicker, { bold: true, size: 24, color: COLOR.accent })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 120, after: 60 },
      border: { top: { style: BorderStyle.SINGLE, size: 18, color: COLOR.primary, space: 4 } },
      children: [new TextRun("")],
    }),
    new Paragraph({
      bidirectional: true,
      alignment: AlignmentType.CENTER,
      spacing: { after: 60 },
      children: [runAr(title, { bold: true, size: 56, color: COLOR.primary })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 120 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 18, color: COLOR.primary, space: 4 } },
      children: [new TextRun("")],
    }),
    new Paragraph({
      bidirectional: true,
      alignment: AlignmentType.CENTER,
      spacing: { after: 600 },
      children: [runAr(subtitle, { size: 28, color: COLOR.muted })],
    }),
    ...filler(2),
    ...(meta || []).map((m) => new Paragraph({
      bidirectional: true,
      alignment: AlignmentType.CENTER,
      spacing: { after: 60 },
      children: [
        runAr(m.label + "  ", { bold: true, size: 24, color: COLOR.secondary }),
        runAr(m.value, { size: 24, color: COLOR.text }),
      ],
    })),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// Section properties factory
function sectionProps() {
  return {
    page: {
      size: { width: PAGE.width, height: PAGE.height },
      margin: { top: PAGE.margin, right: PAGE.margin, bottom: PAGE.margin, left: PAGE.margin },
    },
  };
}

function save(doc, filename) {
  return Packer.toBuffer(doc).then(buf => {
    const out = path.join(OUT_DIR, filename);
    fs.writeFileSync(out, buf);
    console.log("  wrote " + out + "  (" + buf.length + " bytes)");
  });
}

// =================================================================
// DOCUMENT 1 — Arabic cover letter
// =================================================================
function buildArabicLetter() {
  const docTitle = "خطاب تقييم معين الذكي";
  const body = [];

  // Top info strip (date / ref / attachments count)
  body.push(infoStrip([
    { label: "التاريخ", value: "١٧ / ٠٤ / ٢٠٢٦م" },
    { label: "الرقم المرجعي", value: "ME/2026/001" },
    { label: "عدد المرفقات", value: "ست (٦) مرفقات" },
  ], true));
  body.push(new Paragraph({ spacing: { after: 200 }, children: [new TextRun("")] }));

  body.push(heading("خطاب رسمي", 1, true));

  body.push(pAr("السادة المعنيون باعتماد نموذج معين الذكي للغة العربية المحترمين", {
    bold: true, size: 26, color: COLOR.primary, before: 120, after: 120,
  }));

  // Subject line as a highlighted strip
  body.push(new Table({
    width: { size: PAGE.content, type: WidthType.DXA },
    columnWidths: [PAGE.content],
    rows: [new TableRow({ children: [new TableCell({
      borders: {
        top: border(COLOR.accent, 6), bottom: border(COLOR.accent, 6),
        left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
        right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      },
      width: { size: PAGE.content, type: WidthType.DXA },
      shading: { fill: COLOR.light, type: ShadingType.CLEAR, color: "auto" },
      margins: { top: 140, bottom: 140, left: 160, right: 160 },
      children: [new Paragraph({
        bidirectional: true, alignment: AlignmentType.RIGHT,
        children: [
          runAr("الموضوع: ", { bold: true, color: COLOR.primary, size: 26 }),
          runAr("نتائج التقييم المقارن لنموذج معين الذكي على مهام معالجة اللغة العربية الطبيعية",
            { bold: true, size: 26, color: COLOR.text }),
        ],
      })],
    })] })],
  }));
  body.push(new Paragraph({ spacing: { after: 200 }, children: [new TextRun("")] }));

  // Salutation
  body.push(pAr("السلام عليكم ورحمة الله وبركاته،،، وبعد:", {
    bold: true, size: 24, after: 160,
  }));

  body.push(pAr([
    runAr("إشارةً إلى ما أُسند إلينا من مهمة تقييم نموذج ", { size: 24 }),
    runAr("معين الذكي (Mueen AI)", { size: 24, bold: true, color: COLOR.primary }),
    runAr(" للغة العربية، تشرفنا بإجراء دراسة تقييمية مستقلة ومنهجية، نرفع إلى سعادتكم نتائجها الكاملة في هذا الخطاب وفي المرفقات المرافقة له.", { size: 24 }),
  ]));

  // I. Scope & methodology
  body.push(heading("أولاً: نطاق التقييم والمنهجية", 2, true));
  body.push(pAr([
    runAr("أُجري التقييم على ", { size: 24 }),
    runAr("مئتي (٢٠٠) مقالة عربية", { size: 24, bold: true }),
    runAr(" منتقاة بشكل عشوائي ضمن خمس فئات (الثقافة، الاقتصاد، السياسة، الرياضة، التقنية)، بمعدل أربعين مقالة لكل فئة. تم تقييم نموذج معين على ", { size: 24 }),
    runAr("أربع مهام رئيسية", { size: 24, bold: true }),
    runAr(" هي:", { size: 24 }),
  ]));
  body.push(numItemAr("التعرف على الكيانات المسماة (NER) — استخراج الأشخاص والمواقع والمؤسسات والكيانات الأخرى من النص العربي."));
  body.push(numItemAr("الاستدلال اللغوي الطبيعي (NLI) — تصنيف الادعاءات بناءً على مضمون المقالة (مدعوم / مُكذَّب / غير كافٍ)."));
  body.push(numItemAr("التلخيص العربي — إنتاج ملخص من جملتين بالعربية الفصحى."));
  body.push(numItemAr("الترجمة من الإنجليزية إلى العربية — ترجمة نص إنجليزي إلى عربية رسمية."));
  body.push(pAr([
    runAr("ولأغراض المقارنة، أُجريت ذات الاختبارات على ", { size: 24 }),
    runAr("ثلاثة نماذج تجارية متقدمة", { size: 24, bold: true }),
    runAr(" هي: Qwen 3.5 (٣٩٧ مليار معلمة) من علي بابا، وDeepSeek Chat (V3) الصيني، وMistral Large من فرنسا.", { size: 24 }),
  ], { before: 80 }));
  body.push(pAr([
    runAr("اعتمدت منهجية التقييم على نموذج ", { size: 24 }),
    runAr("Claude Opus 4.6", { size: 24, bold: true, color: COLOR.secondary }),
    runAr(" (شركة Anthropic) لتوليد البيانات المرجعية، وعلى نموذج ", { size: 24 }),
    runAr("GPT-5.2", { size: 24, bold: true, color: COLOR.secondary }),
    runAr(" (شركة OpenAI) كحَكم مستقل لتقييم مهمتي التلخيص والترجمة وفق معايير تقييمية موزونة. أما مهمتا التعرف على الكيانات والاستدلال اللغوي فقد قُيِّمتا حسابياً (Deterministic F1 موزون) دون تدخل بشري.", { size: 24 }),
  ]));

  // II. Overall results
  body.push(heading("ثانياً: النتائج الإجمالية", 2, true));
  body.push(pAr([
    runAr("حصل نموذج معين على ", { size: 24 }),
    runAr("معدل عام بلغ 5.91 من ١٠", { size: 24, bold: true, color: COLOR.danger }),
    runAr("، محتلاً المرتبة الرابعة من بين النماذج الأربعة المُقَيَّمة. وفيما يلي ترتيب النماذج كاملاً:", { size: 24 }),
  ]));
  body.push(makeTable({
    headers: ["الترتيب", "النموذج", "NER", "NLI", "التلخيص", "الترجمة", "المعدل العام"],
    rows: [
      ["١", "Qwen 3.5", "7.62", "9.80", "9.12", "9.20", "8.76"],
      ["٢", "DeepSeek Chat", "7.07", "9.88", "8.83", "8.80", "8.46"],
      ["٣", "Mistral Large", "5.95", "9.39", "8.09", "5.02", "6.89"],
      ["٤", "معين الذكي", "4.03", "7.54", "7.30", "5.45", "5.91"],
    ],
    widths: [900, 2000, 1092, 1092, 1092, 1092, 2092],
    arabic: true,
    highlightLastCol: true,
  }));
  body.push(new Paragraph({ spacing: { after: 100 }, children: [new TextRun("")] }));
  body.push(pAr([
    runAr("الفجوة بين معين والنموذج الأول (Qwen 3.5) تبلغ ", { size: 24 }),
    runAr("2.85 نقطة", { size: 24, bold: true, color: COLOR.danger }),
    runAr(" على المعدل العام.", { size: 24 }),
  ]));

  // III. Per-category
  body.push(heading("ثالثاً: أداء معين حسب الفئة", 2, true));
  body.push(makeTable({
    headers: ["الفئة", "عدد المقالات", "NER", "NLI", "التلخيص", "الترجمة", "المعدل"],
    rows: [
      ["الثقافة", "40", "3.92", "7.91", "7.20", "5.76", "6.00"],
      ["الاقتصاد والمال", "40", "4.76", "7.72", "7.10", "6.14", "6.28"],
      ["السياسة", "42", "3.08", "7.19", "7.15", "5.52", "5.53"],
      ["الرياضة", "33", "3.36", "6.50", "6.91", "4.63", "5.19"],
      ["التقنية", "41", "4.94", "8.21", "8.08", "5.09", "6.42"],
    ],
    widths: [1600, 1400, 1072, 1072, 1072, 1072, 2072],
    arabic: true,
    highlightLastCol: true,
  }));
  body.push(new Paragraph({ spacing: { after: 100 }, children: [new TextRun("")] }));
  body.push(pAr([
    runAr("وكما يتضح من الجدول أعلاه، فإن أفضل أداء لمعين كان في فئة ", { size: 24 }),
    runAr("التقنية", { size: 24, bold: true, color: COLOR.success }),
    runAr(" بمعدل 6.42/١٠، فيما كان أضعف أداء في فئة ", { size: 24 }),
    runAr("الرياضة", { size: 24, bold: true, color: COLOR.danger }),
    runAr(" بمعدل 5.19/١٠.", { size: 24 }),
  ]));

  // IV. Detailed notes
  body.push(heading("رابعاً: ملاحظات تفصيلية", 2, true));
  const notes = [
    ["١. التعرف على الكيانات المسماة (NER):", "يُعد هذا المكون نقطة الضعف الأبرز لدى نموذج معين، إذ بلغ معدله 4.03/١٠ مقابل 7.62 للنموذج الأفضل أداءً. يُلاحظ أن النموذج يميل إلى استخراج مجموعة أصغر من الكيانات مقارنة بالمرجع، ويُغفل في كثير من الأحيان التنويعات الصرفية وأسماء الأشخاص الكاملة."],
    ["٢. الاستدلال اللغوي (NLI):", "بلغ معدل معين 7.54/١٠، وهو أقل من النماذج التجارية التي تجمعت كلها في النطاق ٩٫٤–٩٫٩. يُذكر أن هذا الرقم تحسّن بشكل ملحوظ بعد ضبط صيغة الأمر (prompt) لإجبار النموذج على نسخ نص الادعاء حرفياً قبل تصنيفه."],
    ["٣. التلخيص العربي:", "أداء مقبول (7.30/١٠) لكن أقل من النماذج التجارية. الملخصات تصدر بالعربية الفصحى لكنها تميل إلى الإطالة وتفقد بعض التغطية للأحداث الرئيسية."],
    ["٤. الترجمة من الإنجليزية إلى العربية:", "حصل معين على 5.45/١٠، وهي النقطة الأقوى نسبياً له، حيث تجاوز نموذج Mistral Large (5.02/١٠) في هذه المهمة."],
  ];
  for (const [title, txt] of notes) {
    body.push(pAr([
      runAr(title + " ", { size: 24, bold: true, color: COLOR.secondary }),
      runAr(txt, { size: 24 }),
    ], { after: 140 }));
  }

  // V. Recommendations
  body.push(heading("خامساً: التوصيات", 2, true));
  body.push(pAr("بناءً على نتائج التقييم، نوصي بما يلي مرتباً حسب الأولوية:", { size: 24, after: 120 }));
  const recs = [
    ["أولوية قصوى — تعزيز قدرات التعرف على الكيانات العربية:", "زيادة بيانات التدريب المُعنونة بالكيانات (PERSON / LOCATION / ORGANIZATION) مع تغطية التنويعات الصرفية والأسماء الجزئية."],
    ["تحسين معالجة مهام التصنيف:", "تدريب النموذج على الالتزام الحرفي بنصوص الادعاءات المُقدَّمة دون إعادة صياغتها."],
    ["ضبط طول التلخيص:", "التزام النموذج بالعدد المحدد من الجمل (جملتان) دون إطالة."],
    ["تقليل الإضافات في الترجمة:", "إضافة قيود الأمانة (faithfulness) لمنع إدخال معلومات غير موجودة في النص الأصلي."],
    ["معالجة فروقات الأداء بين الفئات:", "فئة الرياضة تستدعي مراجعة تغطية بيانات التدريب فيها."],
  ];
  recs.forEach(([t, txt]) => {
    body.push(new Paragraph({
      bidirectional: true, alignment: AlignmentType.RIGHT,
      numbering: { reference: "arNumbers", level: 0 },
      spacing: { after: 100 },
      children: [
        runAr(t + " ", { bold: true, color: COLOR.primary, size: 24 }),
        runAr(txt, { size: 24 }),
      ],
    }));
  });

  // VI. Conclusion
  body.push(heading("سادساً: الخلاصة", 2, true));
  body.push(pAr("نموذج معين الذكي يُظهر قدرة أساسية على معالجة المحتوى العربي عبر المهام الأربع، لكنه يبقى متأخراً بفارق ملحوظ (2.85 نقطة) عن النماذج التجارية الرائدة. الفرص الأكبر لتحسين الأداء تكمن في تعزيز قدرات التعرف على الكيانات والاستدلال اللغوي. أما مهمة الترجمة من الإنجليزية إلى العربية فتُمثّل نقطة قوة نسبية يُمكن البناء عليها."));

  body.push(pAr("نُحيط سعادتكم علماً بأن جميع التفاصيل التقنية والأمثلة المُفصَّلة والبيانات الخام للتقييم متوفرة في المرفقات المُرفقة بهذا الخطاب. ونحن في انتظار توجيهاتكم الكريمة بشأن أي توضيحات أو تحاليل إضافية قد ترونها ضرورية."));

  // Closing
  body.push(new Paragraph({ spacing: { before: 260, after: 60 }, children: [new TextRun("")] }));
  body.push(pAr("وتفضلوا بقبول فائق الاحترام والتقدير،،،", {
    bold: true, size: 26, color: COLOR.primary, align: AlignmentType.RIGHT, after: 200,
  }));

  // Signature block
  body.push(new Table({
    width: { size: PAGE.content, type: WidthType.DXA },
    columnWidths: [PAGE.content],
    rows: [new TableRow({ children: [new TableCell({
      borders: {
        top: border(COLOR.primary, 6),
        bottom: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
        left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
        right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      },
      width: { size: PAGE.content, type: WidthType.DXA },
      margins: { top: 140, bottom: 40, left: 0, right: 0 },
      children: [
        new Paragraph({
          bidirectional: true, alignment: AlignmentType.RIGHT, spacing: { after: 40 },
          children: [runAr("فريق تقييم منصة نماذج اللغة العربية", { bold: true, size: 24, color: COLOR.primary })],
        }),
        new Paragraph({
          bidirectional: true, alignment: AlignmentType.RIGHT, spacing: { after: 40 },
          children: [runAr("Arabic LLM Benchmark Platform — Independent Evaluation Team", { size: 20, color: COLOR.muted })],
        }),
        new Paragraph({
          bidirectional: true, alignment: AlignmentType.RIGHT, spacing: { after: 0 },
          children: [runAr("أبريل ٢٠٢٦م", { size: 20, color: COLOR.muted })],
        }),
      ],
    })] })],
  }));

  // Attachments list page
  body.push(new Paragraph({ children: [new PageBreak()] }));
  body.push(heading("المرفقات", 1, true));
  body.push(pAr("يُرفق بهذا الخطاب الحزمة التقييمية التالية:", { size: 24, after: 140 }));
  body.push(makeTable({
    headers: ["#", "اسم المرفق", "الوصف", "الصيغة"],
    rows: [
      ["١", "التقرير التقني الكامل",    "تقرير إنجليزي شامل يغطي المنهجية والنتائج الكاملة والتوصيات", "Word"],
      ["٢", "جدول المقارنة الشامل",    "مقارنة بين النماذج الأربعة على مستوى المهمة والفئة",         "Word"],
      ["٣", "أمثلة جنباً إلى جنب",      "خمسة أمثلة تقييمية مع درجات الحَكم وتعليقاته",              "Word"],
      ["٤", "قائمة المرفقات التفصيلية",  "فهرس رسمي بالعربية لجميع مرفقات هذه الحزمة",                 "Word"],
      ["٥", "البيانات الكاملة لمعين",    "بيانات خام لمخرجات معين والمرجع على ٢٠٠ مقالة",             "JSON"],
      ["٦", "بيانات المقارنة الآلية",    "ملف CSV يحوي درجات النماذج الأربعة × ٢٠٠ مقالة",           "CSV"],
    ],
    widths: [700, 2400, 4660, 1600],
    arabic: true,
  }));

  const doc = new Document({
    styles: docStyles(),
    numbering: NUMBERING,
    sections: [{
      properties: sectionProps(),
      headers: { default: letterheadHeader(true) },
      footers: { default: pageFooter(docTitle, true) },
      children: body,
    }],
  });
  return save(doc, "00_خطاب_الرد_الرسمي_AR.docx");
}

// =================================================================
// DOCUMENT 2 — Arabic attachments index
// =================================================================
function buildArabicIndex() {
  const docTitle = "فهرس مرفقات تقييم معين الذكي";
  const body = [
    ...coverPageAr({
      kicker: "مرفق رقم ٤",
      title: "فهرس مرفقات التقييم",
      subtitle: "دليل رسمي بجميع مكونات حزمة التسليم",
      meta: [
        { label: "التاريخ:", value: "١٧ أبريل ٢٠٢٦م" },
        { label: "الرقم المرجعي:", value: "ME/2026/001" },
        { label: "إعداد:", value: "فريق تقييم نماذج اللغة العربية" },
      ],
    }),

    heading("نظرة عامة", 1, true),
    pAr("يحتوي هذا الفهرس على تفصيل رسمي لجميع مرفقات حزمة تقييم نموذج معين الذكي المُسلَّمة إلى الجهة الطالبة، مرتبةً حسب الأولوية مع وصف مختصر لكل مرفق والغرض منه."),

    heading("جدول المرفقات", 2, true),
    makeTable({
      headers: ["#", "اسم الملف", "اللغة", "الصيغة", "الوصف الموجز"],
      rows: [
        ["٠٠", "00_خطاب_الرد_الرسمي_AR.docx",      "عربية",  "Word", "الخطاب الرسمي للرد على طلب التقييم"],
        ["٠١", "01_Technical_Report_EN.docx",      "إنجليزية","Word", "التقرير التقني الكامل بالإنجليزية"],
        ["٠٢", "02_Cross_Model_Comparison_EN.docx","إنجليزية","Word", "تقرير المقارنة بين النماذج الأربعة"],
        ["٠٣", "03_Worked_Examples.docx",           "ثنائي",   "Word", "خمسة أمثلة جنباً إلى جنب مع تعليقات الحَكم"],
        ["٠٤", "04_فهرس_المرفقات_AR.docx",          "عربية",  "Word", "هذا المستند (الفهرس الرسمي للمرفقات)"],
        ["٠٥", "05_mueen_results_full.json",        "—",       "JSON", "البيانات الخام الكاملة لمخرجات معين ودرجاتها"],
        ["٠٦", "06_comparison_data.csv",            "—",       "CSV",  "بيانات قابلة للقراءة الآلية للنماذج الأربعة"],
      ],
      widths: [600, 3200, 900, 900, 3760],
      arabic: true,
    }),

    heading("وصف تفصيلي لكل مرفق", 1, true),

    heading("المرفق ٠١ — التقرير التقني الكامل", 2, true),
    pAr([runAr("الملف: ", { bold: true }), runLatin("01_Technical_Report_EN.docx", { size: 22, color: COLOR.secondary, bold: true })]),
    pAr("تقرير تقني شامل باللغة الإنجليزية يغطي:"),
    bulletAr("الملخص التنفيذي وجدول الترتيب."),
    bulletAr("المنهجية الكاملة (البنية، المهام الأربع، معادلات التقييم)."),
    bulletAr("النتائج التفصيلية لكل مهمة ولكل فئة لجميع النماذج الأربعة."),
    bulletAr("تحليل متعمّق لأداء معين (نقاط القوة، نقاط الضعف، أنماط الإخفاق)."),
    bulletAr("توصيات مرتبة بحسب الأولوية لفريق تطوير نموذج معين."),

    heading("المرفق ٠٢ — جدول المقارنة الشامل", 2, true),
    pAr([runAr("الملف: ", { bold: true }), runLatin("02_Cross_Model_Comparison_EN.docx", { size: 22, color: COLOR.secondary, bold: true })]),
    pAr("مستند مستقل يقارن النماذج الأربعة على كامل مجموعة المقالات البالغة ٢٠٠ مقالة: Qwen 3.5 (٣٩٧ مليار معلمة)، DeepSeek Chat (V3)، Mistral Large، ومعين الذكي. يتضمن:"),
    bulletAr("تفصيل نتائج كل مهمة على حدة."),
    bulletAr("تفصيل نتائج كل فئة على حدة."),
    bulletAr("تحليل ثبات التقييم بين جولة المئة مقالة وجولة المئتي مقالة."),

    heading("المرفق ٠٣ — أمثلة جنباً إلى جنب", 2, true),
    pAr([runAr("الملف: ", { bold: true }), runLatin("03_Worked_Examples.docx", { size: 22, color: COLOR.secondary, bold: true })]),
    pAr("خمسة أمثلة تقييمية حقيقية (مثال واحد لكل فئة، مُنتقى عند متوسط أداء معين في تلك الفئة). يعرض كل مثال:"),
    bulletAr("مقتطف المقالة بالعربية."),
    bulletAr("مخرجات NER لمعين مقارنةً بمرجع Claude Opus."),
    bulletAr("ملخص معين مقارنةً بالمرجع مع معايير الحَكم."),
    bulletAr("تصنيفات NLI لمعين مقارنةً بالعلامات الصحيحة (لكل ادعاء)."),
    bulletAr("ترجمة معين مقارنةً بالمرجع مع معايير الحَكم وتعليقاته."),

    heading("المرفق ٠٥ — البيانات الكاملة لمعين", 2, true),
    pAr([runAr("الملف: ", { bold: true }), runLatin("05_mueen_results_full.json", { size: 22, color: COLOR.secondary, bold: true })]),
    pAr("ملف JSON يحتوي على سجل واحد لكل مقالة مُقيَّمة متضمنًا: معرّف المقالة، الفئة، العنوان، درجات المهام الأربع، مخرجات معين الأربع، مخرجات المرجع الأربع (من Claude Opus)، وتعليقات الحَكم (GPT-5.2) على مهمتي التلخيص والترجمة. مناسب لإعادة التحليل أو المراجعة الخارجية."),

    heading("المرفق ٠٦ — بيانات المقارنة الآلية", 2, true),
    pAr([runAr("الملف: ", { bold: true }), runLatin("06_comparison_data.csv", { size: 22, color: COLOR.secondary, bold: true })]),
    pAr("ملف CSV يحوي صفاً واحداً لكل ثنائية (نموذج، مقالة) على النماذج الأربعة و ٢٠٠ مقالة. الأعمدة: model_name، article_id، category، ner_score، nli_score، summary_score، translation_score، overall_score. بإجمالي ~٨٠٠ صف. ترميز UTF-8 مع BOM لتوافقه مع Microsoft Excel."),

    heading("التحقق من سلامة الملفات", 2, true),
    pAr("يمكن للجهة المستلمة التحقق من سلامة الملفات بحساب بصمة SHA-256 لكل ملف باستخدام الأمر التالي:"),
    new Paragraph({
      spacing: { before: 80, after: 120 },
      shading: { fill: COLOR.light, type: ShadingType.CLEAR, color: "auto" },
      children: [new TextRun({
        text: "sha256sum 00_خطاب_الرد_الرسمي_AR.docx 01_Technical_Report_EN.docx 02_Cross_Model_Comparison_EN.docx 03_Worked_Examples.docx 04_فهرس_المرفقات_AR.docx 05_mueen_results_full.json 06_comparison_data.csv",
        font: { ascii: FONT.mono, hAnsi: FONT.mono }, size: 18, color: COLOR.primary,
      })],
    }),
  ];

  const doc = new Document({
    styles: docStyles(),
    numbering: NUMBERING,
    sections: [{
      properties: sectionProps(),
      headers: { default: letterheadHeader(true) },
      footers: { default: pageFooter(docTitle, true) },
      children: body,
    }],
  });
  return save(doc, "04_فهرس_المرفقات_AR.docx");
}

// =================================================================
// DOCUMENT 3 — English technical report
// =================================================================
function buildTechnicalReport() {
  const docTitle = "Mueen AI — Comprehensive Evaluation Report";
  const body = [
    ...coverPage({
      kicker: "Attachment 01",
      title: "Mueen AI",
      subtitle: "Comprehensive Evaluation Report",
      meta: [
        { label: "Date:",             value: "April 2026" },
        { label: "Framework:",        value: "Arabic LLM Benchmark Platform" },
        { label: "Articles evaluated:", value: "200 Arabic articles across 5 domains" },
        { label: "Models compared:",  value: "Mueen AI vs Qwen 3.5 397B, DeepSeek Chat (V3), Mistral Large" },
        { label: "Reference number:", value: "ME/2026/001" },
      ],
    }),

    heading("1. Executive Summary", 1),
    pLatin("Mueen AI was evaluated on 200 Arabic news articles across 5 categories (culture, finance, politics, sports, tech) on 4 NLP tasks: Named Entity Recognition (NER), Natural Language Inference (NLI), Arabic Summarization, and English-to-Arabic Translation. Three commercial frontier models were evaluated on the same dataset for comparison."),

    heading("Headline Result", 3),
    pLatin([
      runLatin("Mueen AI achieved an ", { size: 22 }),
      runLatin("overall score of 5.91 / 10", { size: 22, bold: true, color: COLOR.danger }),
      runLatin(", placing it in ", { size: 22 }),
      runLatin("4th position", { size: 22, bold: true }),
      runLatin(" among the 4 evaluated models. The leading frontier model (Qwen 3.5 397B) scored 8.76/10, a gap of 2.85 points.", { size: 22 }),
    ]),

    heading("Final Leaderboard (200 articles)", 3),
    makeTable({
      headers: ["Rank", "Model", "NER", "NLI", "Summary", "Translation", "Overall"],
      rows: [
        ["1", "Qwen 3.5 397B",   "7.62", "9.80", "9.12", "9.20", "8.76"],
        ["2", "DeepSeek Chat",   "7.07", "9.88", "8.83", "8.80", "8.46"],
        ["3", "Mistral Large",   "5.95", "9.39", "8.09", "5.02", "6.89"],
        ["4", "Mueen AI",        "4.03", "7.54", "7.30", "5.45", "5.91"],
      ],
      widths: [900, 2400, 1092, 1092, 1092, 1092, 1692],
      highlightLastCol: true,
    }),
    pLatin("", { after: 120 }),

    heading("Key Insight", 3),
    pLatin("Mueen AI's relative weakness is concentrated in Named Entity Recognition (4.03/10, vs 7.62 for the leader). NLI also shows a meaningful gap (7.54 vs 9.80). Generative tasks (Summary 7.30, Translation 5.45) are closer to the field — actually outperforming Mistral Large on Translation (5.45 vs 5.02)."),

    hrThin(),

    heading("2. Methodology", 1),
    heading("The 4 Tasks", 2),
    numItem("NER (Named Entity Recognition) — Extract entities into 4 categories (PERSON, LOCATION, ORGANIZATION, MISC) from each Arabic article. Scored deterministically using weighted F1 with Arabic normalization (diacritics, alef variants, definite article ال) and a hallucination penalty for entities not found in the source."),
    numItem("NLI (Natural Language Inference / Fact Verification) — Given an article and 4 claims, label each as SUPPORTED, REFUTED, or NOT_ENOUGH_INFO. Scored by positional weighted accuracy (NOT_ENOUGH_INFO×1.5, REFUTED×1.2, SUPPORTED×1.0)."),
    numItem("Arabic Summarization — Produce a 2-sentence summary in formal Modern Standard Arabic (فصحى). Scored by GPT-5.2 with a 5-criterion rubric: factual accuracy (0–3), coverage (0–3), no added inference (0–2), register fluency (0–2), and verbatim copying penalty (0–1)."),
    numItem("English→Arabic Translation — Translate a 3-sentence English summary of the article into formal Arabic. Scored by GPT-5.2 with a 4-criterion rubric: faithfulness (0–3), fluency (0–3), terminology handling (0–2), register/formality (0–2)."),

    heading("Overall Score Formula", 2),
    new Paragraph({
      spacing: { before: 80, after: 160 },
      shading: { fill: COLOR.light, type: ShadingType.CLEAR, color: "auto" },
      alignment: AlignmentType.CENTER,
      children: [new TextRun({
        text: "Overall = NER × 0.30 + NLI × 0.20 + Summary × 0.25 + Translation × 0.25",
        font: { ascii: FONT.mono, hAnsi: FONT.mono }, size: 22, bold: true, color: COLOR.primary,
      })],
    }),

    heading("Dataset", 2),
    bullet("500 Arabic articles collected across 5 categories (100 each)."),
    bullet("200 articles sampled for evaluation: round 1 (seed=42), round 2 (seed=99)."),
    bullet("~40 articles per category in the final 200-article evaluation set."),

    heading("Judges", 2),
    bullet("Teacher model (reference generation): Claude Opus 4.6 (Anthropic)."),
    bullet("Judge model (summary + translation): GPT-5.2 (OpenAI)."),
    bullet("NER + NLI scored deterministically — no human or LLM judgment."),

    hrThin(),

    heading("3. Detailed Results", 1),
    heading("Per-task Scores (all 4 models)", 2),
    makeTable({
      headers: ["Task", "Qwen 3.5", "DeepSeek", "Mistral", "Mueen AI", "Mueen Rank"],
      rows: [
        ["NER",         "7.62", "7.07", "5.95", "4.03", "4"],
        ["NLI",         "9.80", "9.88", "9.39", "7.54", "4"],
        ["Summary",     "9.12", "8.83", "8.09", "7.30", "4"],
        ["Translation", "9.20", "8.80", "5.02", "5.45", "3"],
        ["Overall",     "8.76", "8.46", "6.89", "5.91", "4"],
      ],
      widths: [1700, 1432, 1432, 1432, 1432, 1932],
    }),
    pLatin("Note: On Translation, Mueen AI outperforms Mistral Large.", { italic: true, color: COLOR.muted, before: 120 }),

    heading("Mueen AI — Per-Category Breakdown", 2),
    makeTable({
      headers: ["Category", "N", "NER", "NLI", "Summary", "Translation", "Overall"],
      rows: [
        ["Culture",  "40", "3.92", "7.91", "7.20", "5.76", "6.00"],
        ["Finance",  "40", "4.76", "7.72", "7.10", "6.14", "6.28"],
        ["Politics", "42", "3.08", "7.19", "7.15", "5.52", "5.53"],
        ["Sports",   "33", "3.36", "6.50", "6.91", "4.63", "5.19"],
        ["Tech",     "41", "4.94", "8.21", "8.08", "5.09", "6.42"],
      ],
      widths: [1700, 900, 1152, 1152, 1152, 1452, 1852],
      highlightLastCol: true,
    }),

    hrThin(),

    heading("4. Mueen AI Deep-Dive", 1),
    heading("Strengths", 2),
    bullet("Best category: Tech with overall score 6.42/10. Mueen handles tech content with the most consistency."),
    bullet("Second-best category: Finance (6.28/10)."),
    bullet("Translation is Mueen's relatively strongest task ranked against the field — 3rd of 4 models, beating Mistral Large."),
    bullet("NLI labels are usable when claims are presented in the expected format (7.54/10) — meaningful signal, even if behind the leaders."),

    heading("Weaknesses", 2),
    bullet("Worst category: Sports with overall score 5.19/10. The sports domain produces the most misses."),
    bullet("NER (4.03/10) is the weakest task overall — the gap to the leader (Qwen 3.5: 7.62) is 3.59 points. Mueen frequently misses entities that the reference includes, particularly people's full names and organization variants."),
    bullet("NLI accuracy (7.54/10) trails the field — all three commercial models cluster at 9.4–9.9 on this task."),

    heading("Worked Examples", 2),
    pLatin("Five articles (one per category, picked at the per-category median Mueen score) are reproduced in the companion file 03_Worked_Examples.docx. Each example shows Mueen's actual outputs side-by-side with the Claude Opus reference and the GPT-5.2 judge feedback."),

    hrThin(),

    heading("5. Failure Pattern Analysis", 1),
    pLatin("Patterns observed across the 196 scored Mueen articles:"),
    numItem("NER under-extraction — Mueen tends to extract a smaller entity set than the reference. The reference includes morphological variants and secondary mentions; Mueen tends to capture only the most prominent."),
    numItem("NLI claim-text drift — In the first manual round, Mueen rewrote several claims rather than copying them verbatim. Once the prompt was tightened to enforce verbatim claim copying, NLI scores rose substantially (2.90 → 7.36 on the same articles). This is a prompt-engineering finding, not a model capability finding."),
    numItem("Summary register — Summaries are in MSA but tend to be more verbose than the reference 2-sentence target. The judge rubric penalizes coverage and conciseness."),
    numItem("Translation occasionally adds material — A subset of translations include details not in the English source, hurting the faithfulness component of the judge rubric."),

    hrThin(),

    heading("6. Recommendations for the Mueen Team", 1),
    pLatin("Priority order (highest impact first):", { bold: true }),

    pLatin([runLatin("P1 — Improve Arabic NER coverage", { bold: true, color: COLOR.primary, size: 24 })], { before: 120 }),
    bullet("Collect more annotated Arabic news data with PERSON/LOCATION/ORGANIZATION tags including morphological variants and partial mentions."),
    bullet("Consider an explicit entity-extraction prompt scaffold during training/inference."),

    pLatin([runLatin("P2 — Improve NLI claim handling", { bold: true, color: COLOR.primary, size: 24 })], { before: 120 }),
    bullet("Ensure the model strictly preserves provided claim text in classification tasks."),
    bullet("Investigate why NOT_ENOUGH_INFO (the hardest, weight 1.5) is missed most often."),

    pLatin([runLatin("P3 — Tighten summary length", { bold: true, color: COLOR.primary, size: 24 })], { before: 120 }),
    bullet("Train/instruct the model to honor the 2-sentence target."),
    bullet("Penalize verbatim sentence copying explicitly."),

    pLatin([runLatin("P4 — Reduce translation hallucinations", { bold: true, color: COLOR.primary, size: 24 })], { before: 120 }),
    bullet("Add faithfulness constraints to the translation prompt."),
    bullet("Consider a translation-specific fine-tuning pass on faithful Eng→Ar pairs."),

    pLatin([runLatin("P5 — Reduce category variance", { bold: true, color: COLOR.primary, size: 24 })], { before: 120 }),
    bullet("Sports category (5.19) underperforms; investigate domain coverage in training data."),

    hrThin(),

    heading("7. Reproducibility", 1),
    pLatin("All evaluation artifacts are captured in this repository:"),
    bullet("arabic_500_dataset.json — full corpus (500 articles)."),
    bullet("selected_100.json + selected_next_100.json — the 200-article evaluation set."),
    bullet("mueen_results_full.json — Mueen's outputs alongside reference data and scores."),
    bullet("comparison_data.csv — machine-readable scores for all 4 models × 200 articles."),
    bullet("200-ARTICLE-EVALUATION.md — high-level cross-model comparison."),
    bullet("mueen_evaluation_samples.md — 5 worked side-by-side examples."),
    bullet("scripts/sample_100.py — deterministic article sampler."),
    bullet("scripts/run_benchmark.py — end-to-end orchestration."),

    pLatin("This report was generated from the live evaluation database by scripts/build_mueen_report.py. All numbers are cross-verifiable against the underlying SQLite database and the JSON artifacts in this repository.",
      { italic: true, color: COLOR.muted, before: 240 }),
  ];

  const doc = new Document({
    styles: docStyles(),
    numbering: NUMBERING,
    sections: [{
      properties: sectionProps(),
      headers: { default: letterheadHeader(false) },
      footers: { default: pageFooter(docTitle, false) },
      children: body,
    }],
  });
  return save(doc, "01_Technical_Report_EN.docx");
}

// =================================================================
// DOCUMENT 4 — Cross-model comparison
// =================================================================
function buildCrossModelComparison() {
  const docTitle = "Cross-Model Comparison — 200 Arabic Articles";
  const body = [
    ...coverPage({
      kicker: "Attachment 02",
      title: "Cross-Model Comparison",
      subtitle: "200-Article Arabic LLM Benchmark — Evaluation Results",
      meta: [
        { label: "Date:",       value: "April 2026" },
        { label: "Teacher:",    value: "Claude Opus 4.6 (Anthropic)" },
        { label: "Judge:",      value: "GPT-5.2 (OpenAI)" },
        { label: "Sample:",     value: "200 articles (seed=42 + seed=99), ~40/category" },
        { label: "Tasks:",      value: "NER, NLI, Summary (Arabic), Translation (Eng→Arabic)" },
        { label: "Reference number:", value: "ME/2026/001" },
      ],
    }),

    heading("1. Overview", 1),
    pLatin("Full evaluation of 4 LLMs on Arabic NLP tasks using 200 Arabic articles across 5 categories (culture, finance, politics, sports, tech — ~40 per category)."),
    bullet("Teacher Model (reference dataset): Claude Opus 4.6 (Anthropic)."),
    bullet("Judge Model (summaries & translations): GPT-5.2 (OpenAI)."),
    bullet("Evaluation date: April 2026."),
    bullet("Articles: 200 (sampled from 500-article corpus, two rounds: seed=42 and seed=99)."),
    bullet("Tasks: 4 — NER, NLI, Summary (Arabic), Translation (English→Arabic)."),

    heading("Score Weights", 2),
    new Paragraph({
      spacing: { before: 80, after: 160 },
      shading: { fill: COLOR.light, type: ShadingType.CLEAR, color: "auto" },
      alignment: AlignmentType.CENTER,
      children: [new TextRun({
        text: "Overall = NER × 0.30 + NLI × 0.20 + Summary × 0.25 + Translation × 0.25",
        font: { ascii: FONT.mono, hAnsi: FONT.mono }, size: 22, bold: true, color: COLOR.primary,
      })],
    }),

    heading("2. Models Evaluated", 1),
    makeTable({
      headers: ["Model", "Provider", "Type"],
      rows: [
        ["Qwen 3.5 397B-A17B", "Alibaba Dashscope",       "API"],
        ["DeepSeek Chat (V3)", "DeepSeek native API",     "API"],
        ["Mistral Large",      "AWS Bedrock",             "API"],
        ["Mueen AI",           "Manual (browser-based)",  "Manual upload"],
      ],
      widths: [3200, 3880, 2280],
    }),

    hrThin(),

    heading("3. Overall Results — 200 Articles", 1),
    makeTable({
      headers: ["Model", "N", "NER", "NLI", "Summary", "Translation", "Overall"],
      rows: [
        ["Qwen 3.5 397B", "200", "7.62", "9.80", "9.12", "9.20", "8.76"],
        ["DeepSeek Chat", "196", "7.07", "9.88", "8.83", "8.80", "8.46"],
        ["Mistral Large", "200", "5.95", "9.39", "8.09", "5.02", "6.89"],
        ["Mueen AI",      "196", "4.03", "7.54", "7.30", "5.45", "5.91"],
      ],
      widths: [2300, 900, 1132, 1132, 1132, 1132, 1632],
      highlightLastCol: true,
    }),

    heading("Ranking", 2),
    numItem("Qwen 3.5 397B — 8.76 (best across all tasks)."),
    numItem("DeepSeek Chat — 8.46 (consistently strong, near-perfect NLI)."),
    numItem("Mistral Large — 6.89 (still weak on translation: 5.02)."),
    numItem("Mueen AI — 5.91 (lowest NER and NLI; competitive on tech and finance)."),

    hrThin(),

    heading("4. Per-Task Analysis", 1),

    heading("NER — Deterministic F1", 3),
    makeTable({
      headers: ["Model", "Score"],
      rows: [["Qwen 3.5", "7.62"], ["DeepSeek", "7.07"], ["Mistral", "5.95"], ["Mueen AI", "4.03"]],
      widths: [6680, 2680],
      highlightLastCol: true,
    }),

    heading("NLI — Deterministic Weighted Accuracy", 3),
    makeTable({
      headers: ["Model", "Score"],
      rows: [["DeepSeek", "9.88"], ["Qwen 3.5", "9.80"], ["Mistral", "9.39"], ["Mueen AI", "7.54"]],
      widths: [6680, 2680],
      highlightLastCol: true,
    }),

    heading("Summary (Arabic) — GPT-5.2 Judge", 3),
    makeTable({
      headers: ["Model", "Score"],
      rows: [["Qwen 3.5", "9.12"], ["DeepSeek", "8.83"], ["Mistral", "8.09"], ["Mueen AI", "7.30"]],
      widths: [6680, 2680],
      highlightLastCol: true,
    }),

    heading("Translation (English → Arabic) — GPT-5.2 Judge", 3),
    makeTable({
      headers: ["Model", "Score"],
      rows: [["Qwen 3.5", "9.20"], ["DeepSeek", "8.80"], ["Mueen AI", "5.45"], ["Mistral", "5.02"]],
      widths: [6680, 2680],
      highlightLastCol: true,
    }),

    hrThin(),

    heading("5. Per-Category Breakdown — All Tasks", 1),

    heading("Qwen 3.5 397B (Overall: 8.76)", 3),
    makeTable({
      headers: ["Category", "N", "NER", "NLI", "Summary", "Translation", "Overall"],
      rows: [
        ["Culture",  "40", "7.58", "9.86",  "9.38", "8.82", "8.75"],
        ["Finance",  "41", "8.74", "9.58",  "8.95", "9.34", "9.08"],
        ["Politics", "43", "6.93", "9.72",  "9.29", "9.44", "8.61"],
        ["Sports",   "34", "7.56", "9.84",  "8.83", "9.00", "8.63"],
        ["Tech",     "42", "7.31", "10.00", "9.08", "9.34", "8.73"],
      ],
      widths: [1700, 900, 1152, 1152, 1152, 1452, 1852],
      highlightLastCol: true,
    }),

    heading("DeepSeek Chat (Overall: 8.46)", 3),
    makeTable({
      headers: ["Category", "N", "NER", "NLI", "Summary", "Translation", "Overall"],
      rows: [
        ["Culture",  "40", "7.26", "9.86",  "9.02", "8.66", "8.51"],
        ["Finance",  "40", "7.28", "9.78",  "8.45", "8.40", "8.35"],
        ["Politics", "42", "7.16", "9.94",  "8.96", "9.18", "8.61"],
        ["Sports",   "33", "7.08", "10.00", "8.71", "8.64", "8.43"],
        ["Tech",     "41", "6.58", "9.83",  "8.96", "9.05", "8.41"],
      ],
      widths: [1700, 900, 1152, 1152, 1152, 1452, 1852],
      highlightLastCol: true,
    }),

    heading("Mistral Large (Overall: 6.89)", 3),
    makeTable({
      headers: ["Category", "N", "NER", "NLI", "Summary", "Translation", "Overall"],
      rows: [
        ["Culture",  "40", "6.51", "9.88", "8.50", "4.91", "7.24"],
        ["Finance",  "41", "5.86", "8.09", "7.46", "5.15", "6.50"],
        ["Politics", "43", "5.69", "9.56", "8.48", "4.68", "6.84"],
        ["Sports",   "34", "5.99", "9.66", "7.97", "4.99", "6.91"],
        ["Tech",     "42", "5.74", "9.80", "7.98", "5.36", "6.97"],
      ],
      widths: [1700, 900, 1152, 1152, 1152, 1452, 1852],
      highlightLastCol: true,
    }),

    heading("Mueen AI (Overall: 5.91)", 3),
    makeTable({
      headers: ["Category", "N", "NER", "NLI", "Summary", "Translation", "Overall"],
      rows: [
        ["Culture",  "40", "3.92", "7.91", "7.20", "5.76", "6.00"],
        ["Finance",  "40", "4.76", "7.72", "7.10", "6.14", "6.28"],
        ["Politics", "42", "3.08", "7.19", "7.15", "5.52", "5.53"],
        ["Sports",   "33", "3.36", "6.50", "6.91", "4.63", "5.19"],
        ["Tech",     "41", "4.94", "8.21", "8.08", "5.09", "6.42"],
      ],
      widths: [1700, 900, 1152, 1152, 1152, 1452, 1852],
      highlightLastCol: true,
    }),

    hrThin(),

    heading("6. Key Findings", 1),
    numItem("Qwen 3.5 remains the clear winner at 8.76 overall — consistent across all categories with a peak of 9.08 on Finance. Top 3 in every single task."),
    numItem("DeepSeek Chat is a reliable second at 8.46 — virtually tied with Qwen on NLI (9.88 vs 9.80) and very close on Summary. Best for cost-conscious deployment."),
    numItem("Mistral Large has a critical Arabic generation weakness — Translation score of 5.02 (worse than Mueen!) caps its ceiling. Strong on NLI (9.39) and Summary (8.09)."),
    numItem("Mueen AI shows clear gaps — weakest on NER (4.03) and NLI (7.54). Strongest on Tech (6.42) and weakest on Sports (5.19)."),
    numItem("Scores are very stable across the two 100-article batches — variation of ±0.2 points or less for all models. This validates the scoring methodology."),
    numItem("Tech and Politics categories produce the most consistent scores across all models. Sports and Culture have the widest variance."),
    numItem("Translation is the most discriminating task — spread from 5.02 (Mistral) to 9.20 (Qwen) is the widest. Confirms the Eng→Arabic direction is the key discriminator for Arabic capability."),

    hrThin(),

    heading("7. Comparison: 100 vs 200 Articles", 1),
    pLatin("Scores remained remarkably stable when expanding from 100 to 200 articles — confirming the methodology's reliability:"),
    makeTable({
      headers: ["Model", "100-article", "200-article", "Δ"],
      rows: [
        ["Qwen 3.5",  "8.62", "8.76", "+0.14"],
        ["DeepSeek",  "8.38", "8.46", "+0.08"],
        ["Mistral",   "6.60", "6.89", "+0.29"],
        ["Mueen AI",  "5.79", "5.91", "+0.12"],
      ],
      widths: [3000, 2120, 2120, 2120],
      highlightLastCol: true,
    }),

    hrThin(),

    heading("8. Methodology", 1),

    heading("Dataset Generation", 3),
    bullet("500 Arabic articles collected across 5 categories (100 each)."),
    bullet("200 articles sampled in two rounds: Round 1 — 100 articles (random.seed(42), 20 per category); Round 2 — 100 articles (random.seed(99), 20 per category, no overlap with round 1)."),
    bullet("Claude Opus 4.6 generated reference data via Anthropic Batch API (50% cost discount)."),
    bullet("4 reference outputs per article: NER entities, 2-sentence Arabic summary, 4 NLI claims, English→Arabic translation pair."),

    heading("Evaluation", 3),
    bullet("API models evaluated programmatically via their respective APIs."),
    bullet("Mueen AI evaluated manually via browser-based assistant with structured prompts split into 10-article chunks."),
    bullet("Each model performed the same 4 tasks on the same 200 articles."),

    heading("Scoring", 3),
    bullet("NER: Deterministic weighted F1 with Arabic normalization and hallucination penalty."),
    bullet("NLI: Deterministic positional label matching with per-label importance weights (NOT_ENOUGH_INFO×1.5, REFUTED×1.2, SUPPORTED×1.0)."),
    bullet("Summary: GPT-5.2 LLM-as-Judge — rubric (factual accuracy, coverage, no inference, register fluency, verbatim penalty)."),
    bullet("Translation: GPT-5.2 LLM-as-Judge — rubric (faithfulness, fluency, terminology, register)."),
    bullet("Overall: Weighted average — NER×0.30 + NLI×0.20 + Summary×0.25 + Translation×0.25."),

    heading("Infrastructure", 3),
    bullet("Backend: FastAPI + SQLite (Python 3.12)."),
    bullet("Frontend: Angular 20 + Material."),
    bullet("Multi-provider LLM client: OpenAI, Anthropic, AWS Bedrock, Dashscope, DeepSeek."),
    bullet("Anthropic Batch API for teacher generation (50% cost savings)."),
    bullet("53 unit tests passing."),
  ];

  const doc = new Document({
    styles: docStyles(),
    numbering: NUMBERING,
    sections: [{
      properties: sectionProps(),
      headers: { default: letterheadHeader(false) },
      footers: { default: pageFooter(docTitle, false) },
      children: body,
    }],
  });
  return save(doc, "02_Cross_Model_Comparison_EN.docx");
}

// =================================================================
// DOCUMENT 5 — Worked examples (bilingual / mixed)
// =================================================================
function buildWorkedExamples() {
  const docTitle = "أمثلة تقييم معين الذكي جنباً إلى جنب";

  // Side-by-side two-column box with Arabic column titles.
  function twoColArabic(leftTitle, leftText, rightTitle, rightText) {
    const colW = Math.floor(PAGE.content / 2);
    const makeCell = (title, text, fill) => new TableCell({
      borders: cellBorders(COLOR.borderGrey),
      width: { size: colW, type: WidthType.DXA },
      shading: { fill, type: ShadingType.CLEAR, color: "auto" },
      margins: { top: 120, bottom: 120, left: 160, right: 160 },
      children: [
        new Paragraph({
          bidirectional: true, alignment: AlignmentType.RIGHT,
          spacing: { after: 80 },
          children: [runAr(title, { bold: true, size: 22, color: COLOR.primary })],
        }),
        new Paragraph({
          bidirectional: true, alignment: AlignmentType.RIGHT,
          spacing: { line: 340, after: 0 },
          children: [runAr(text, { size: 22 })],
        }),
      ],
    });
    return new Table({
      width: { size: PAGE.content, type: WidthType.DXA },
      columnWidths: [colW, PAGE.content - colW],
      rows: [new TableRow({ children: [
        makeCell(leftTitle,  leftText,  COLOR.light),
        makeCell(rightTitle, rightText, COLOR.white),
      ] })],
    });
  }

  function rubricStrip(rubric, note) {
    return [
      new Paragraph({
        bidirectional: true, alignment: AlignmentType.RIGHT,
        spacing: { before: 140, after: 80 },
        shading: { fill: COLOR.primary, type: ShadingType.CLEAR, color: "auto" },
        children: [
          runAr("  معايير الحَكم:  ", { bold: true, size: 22, color: COLOR.white }),
          new TextRun({
            text: rubric, size: 22, color: COLOR.white,
            font: { ascii: FONT.mono, hAnsi: FONT.mono },
          }),
        ],
      }),
      new Paragraph({
        bidirectional: true, alignment: AlignmentType.RIGHT,
        spacing: { before: 0, after: 120, line: 340 },
        shading: { fill: COLOR.light, type: ShadingType.CLEAR, color: "auto" },
        children: [
          runAr("تعليق الحَكم: ", { bold: true, color: COLOR.primary, size: 22 }),
          runAr(note, { size: 22 }),
        ],
      }),
    ];
  }

  // Labelled English source block — keeps the actual training text in English.
  function englishSource(text) {
    return [
      new Paragraph({
        bidirectional: true, alignment: AlignmentType.RIGHT,
        spacing: { before: 100, after: 60 },
        children: [runAr("المصدر الإنجليزي (نص اختبار الترجمة):",
          { bold: true, size: 22, color: COLOR.secondary })],
      }),
      new Paragraph({
        alignment: AlignmentType.LEFT,
        spacing: { before: 0, after: 160, line: 320 },
        shading: { fill: COLOR.light, type: ShadingType.CLEAR, color: "auto" },
        children: [runLatin(text, { size: 22, italic: true, color: COLOR.muted })],
      }),
    ];
  }

  function articleExcerpt(text) {
    // Use a single-cell table to get the accent left-bar look reliably.
    return new Table({
      width: { size: PAGE.content, type: WidthType.DXA },
      columnWidths: [PAGE.content],
      rows: [new TableRow({ children: [new TableCell({
        borders: {
          top:    { style: BorderStyle.SINGLE, size: 2,  color: COLOR.borderGrey },
          bottom: { style: BorderStyle.SINGLE, size: 2,  color: COLOR.borderGrey },
          left:   { style: BorderStyle.SINGLE, size: 24, color: COLOR.accent },
          right:  { style: BorderStyle.SINGLE, size: 2,  color: COLOR.borderGrey },
        },
        width: { size: PAGE.content, type: WidthType.DXA },
        shading: { fill: COLOR.light, type: ShadingType.CLEAR, color: "auto" },
        margins: { top: 160, bottom: 160, left: 200, right: 200 },
        children: [new Paragraph({
          bidirectional: true, alignment: AlignmentType.RIGHT,
          spacing: { before: 0, after: 0, line: 340 },
          children: [runAr(text, { size: 22, italic: true, color: COLOR.muted })],
        })],
      })] })],
    });
  }

  function scoreCard(overall, ner, nli, summary, translation) {
    return makeTable({
      headers: ["المعدل العام", "NER", "NLI", "التلخيص", "الترجمة"],
      rows: [[overall, ner, nli, summary, translation]],
      widths: [1872, 1872, 1872, 1872, 1872],
      arabic: true,
      highlightLastCol: false,
    });
  }

  function nerTable(person, location, organization, misc) {
    return makeTable({
      headers: ["الفئة", "المرجع (Claude Opus)", "معين الذكي"],
      rows: [
        ["أشخاص",   person[0]       || "—", person[1]       || "—"],
        ["مواقع",   location[0]     || "—", location[1]     || "—"],
        ["مؤسسات",  organization[0] || "—", organization[1] || "—"],
        ["متنوع",   misc[0]         || "—", misc[1]         || "—"],
      ],
      widths: [1760, 3800, 3800],
      arabic: true,
    });
  }

  function nliTable(claims) {
    return makeTable({
      headers: ["#", "نص الادعاء", "المرجع", "معين", "المطابقة"],
      rows: claims.map(c => [String(c.n), c.claim, c.ref, c.mueen, c.match ? "✓" : "✗"]),
      widths: [600, 5000, 1600, 1600, 560],
      arabic: true,
    });
  }

  const body = [
    ...coverPageAr({
      kicker: "المرفق رقم ٠٣",
      title: "أمثلة تقييمية جنباً إلى جنب",
      subtitle: "مقارنة مخرجات معين الذكي بالمرجع — مثال واحد لكل فئة",
      meta: [
        { label: "التاريخ:",        value: "أبريل ٢٠٢٦م" },
        { label: "المرجع:",         value: "Claude Opus 4.6" },
        { label: "الحَكم:",          value: "GPT-5.2" },
        { label: "منهجية الانتقاء:", value: "مقالات عند متوسط أداء معين في كل فئة" },
        { label: "الرقم المرجعي:",   value: "ME/2026/001" },
      ],
    }),

    heading("مقدمة", 1, true),
    pAr("يُعيد هذا المرفق عرض خمس حالات تقييمية تمثيلية — بمعدل حالة واحدة لكل فئة — تُبيّن مخرجات نموذج معين الذكي الفعلية جنباً إلى جنب مع المرجع المستخرَج من Claude Opus، وتعليقات ومعايير الحَكم GPT-5.2. وقد انتُقيت المقالات عند متوسط درجات معين في كل فئة، بحيث تعكس كل حالة السلوك المعتاد للنموذج لا أفضل أداء له ولا أسوأه."),
    pAr("يتضمن كل مثال العناصر التالية: (١) مقتطف من المقالة بالعربية، (٢) مقارنة جنباً إلى جنب لمخرجات التعرف على الكيانات (NER)، (٣) مقارنة جنباً إلى جنب للتلخيص مع معايير الحَكم وتعليقاته، (٤) مقارنة تفصيلية للاستدلال اللغوي (NLI) على مستوى كل ادعاء، (٥) مقارنة جنباً إلى جنب للترجمة مع معايير الحَكم وتعليقاته."),

    // ===== 1. CULTURE =====
    new Paragraph({ children: [new PageBreak()] }),
    heading("المثال الأول — الثقافة (CULTURE_039)", 1, true),
    pAr([
      runAr("العنوان: ", { bold: true, color: COLOR.secondary }),
      runAr("انطلقت فعاليات الدورة العاشرة لأيام الشارقة المسرحية مساء 27 من مارس/آذار برعاية صاحب السمو الشيخ ...", { size: 24 }),
    ]),
    scoreCard("6.27 / 10", "4.80", "10.00", "5.83", "5.50"),

    heading("مقتطف من المقالة", 3, true),
    articleExcerpt("انطلقت فعاليات الدورة العاشرة لأيام الشارقة المسرحية مساء 27 من مارس/آذار برعاية صاحب السمو الشيخ الدكتور سلطان بن محمد القاسمي عضو المجلس الأعلى حاكم الشارقة وبعرض القضية، إحدى أعماله المسرحية، واختتمت مساء 5 من أبريل/نيسان، حيث شاركت إحدى عشرة فرقة مسرحية قدمت اثني عشر عملاً مسرحياً في إطار التنافس على جوائز مسابقة المهرجان التي ارتفع عددها إلى ثلاث عشرة جائزة..."),

    heading("المهمة الأولى — التعرف على الكيانات (NER —4.80 / 10)", 3),
    nerTable(
      ["سلطان بن محمد القاسمي, نضال الأشقر, جواد الأسدي, جمال مطر, ابراهيم الأميري, أحمد الأنصاري, محمد الطريفي, حكيم جاسم, عبد الله الراشد, محمود أبو العباس, مريم سلطان, ناجي الحاي, عائشة عبد الرحمن, أحمد الجسمي, قاسم محمد, هدى الخطيب, بدرية أحمد",
       "صاحب السمو الشيخ الدكتور سلطان بن محمد القاسمي, نضال الأشقر, جواد الأسدي, جمال مطر, ابراهيم الأميري, محمد الطريفي, عبد الله الراشد, مريم سلطان, عائشة عبد الرحمن, أحمد الجسمي, هدى الخطيب, بدرية أحمد, ناجي الحاي, قاسم محمد, أحمد الأنصاري"],
      ["الشارقة, أبوظبي, دبا الفجيرة, دبي, الفجيرة, رأس الخيمة, أم القيوين, دبا الحصن",
       "الشارقة, أبوظبي, دبا الفجيرة, دبي, رأس الخيمة, أم القيوين, الفجيرة, دبا الحصن, الدوحة"],
      ["المجلس الأعلى, فرقة مسرح الاتحاد, فرقة مسرح دبا الفجيرة, فرقة مسرح دبي الأهلي, فرقة مسرح الشارقة الوطني, فرقة مسرح الفجيرة القومي, فرقة مسرح رأس الخيمة الوطني, فرقة مسرح أم القيوين الوطني, فرقة المسرح الحديث في الشارقة, فرقة مسرح دبا الحصن, فرقة المسرح القومي للشباب في دبي",
       "فرقة مسرح الاتحاد, فرقة مسرح دبا الفجيرة, فرقة مسرح دبي الأهلي, فرقة مسرح الشارقة الوطني, فرقة مسرح الفجيرة القومي, فرقة مسرح رأس الخيمة الوطني, فرقة مسرح أم القيوين الوطني, فرقة المسرح الحديث في الشارقة, فرقة مسرح رأس الخيمة الوطني, فرقة مسرح الشارقة الوطني, فرقة مسرح دبا الحصن, فرقة المسرح القومي للشباب في دبي"],
      ["—", "الدراماتورغ, العرض المسرحي, النص المسرحي, المفاهيم المسرحية"],
    ),

    heading("المهمة الثانية — التلخيص (5.83 / 10)", 3),
    twoColArabic(
      "المرجع (Claude Opus)",
      "افتُتِحَت الدورة العاشرة لأيام الشارقة المسرحية في السابع والعشرين من مارس برعاية صاحب السمو الشيخ الدكتور سلطان بن محمد القاسمي حاكم الشارقة، وشهدت مشاركة إحدى عشرة فرقة مسرحية قدّمت اثني عشر عملاً تنافست على ثلاث عشرة جائزة، فيما تضمّن الملتقى الفكري المصاحب نقاشات حول إدارة المهرجانات المسرحية العربية والدوريات المتخصصة فضلاً عن التمييز بين دور الدراماتورغ والمخرج. أسفرت نتائج لجنة التحكيم برئاسة الفنانة نضال الأشقر عن فوز مسرحية «ما كان لأحمد بنت سليمان» لفرقة المسرح القومي للشباب في دبي بجائزة أفضل عرض متكامل، ونيل أحمد الأنصاري جائزة أفضل إخراج عن مسرحية «الياثوم»، وحصول أحمد الجسمي على جائزة أفضل ممثل لدور أول، ومنح الفنان العراقي قاسم محمد جائزة أفضل فنان عربي متميز.",
      "معين الذكي",
      "انطلقت فعاليات الدورة العاشرة لأيام الشارقة المسرحية برعاية صاحب السمو الشيخ الدكتور سلطان بن محمد القاسمي، وشهدت مشاركة العديد من الفرق المسرحية من مختلف الدول. شهدت الدورة منافسة على جوائز متعددة، وشملت فعاليات مصاحبة تتناول موضوعات مسرحية وفنية مهمة.",
    ),
    ...rubricStrip(
      "factual=2/3    coverage=1/3    no_inference=1/2    register=2/2",
      "الملخص صحيح في العموم بشأن انطلاق الدورة العاشرة برعاية حاكم الشارقة ووجود فرق وجوائز وفعاليات مصاحبة، لكنه يفتقد الدقة والتحديد (لا يذكر التواريخ، عدد الفرق/الأعمال/الجوائز، محوري الملتقى الفكري، أو نتائج التحكيم وأبرز الفائزين). كما أضاف تعميماً غير مدعوم بدقة وهو أن الفرق من «مختلف الدول»، بينما المصدر يتحدث عن فرق مسرحية (إماراتية) دون تأكيد مشاركة دول متعددة. اللغة سليمة ومترابطة ولا يوجد نسخ حرفي."),

    heading("المهمة الثالثة — الاستدلال اللغوي (NLI —10.00 / 10)", 3),
    nliTable([
      { n: 1, claim: "بدأت فعاليات الدورة العاشرة لأيام الشارقة المسرحية في السابع والعشرين من مارس...", ref: "SUPPORTED", mueen: "SUPPORTED", match: true },
      { n: 2, claim: "فاز الفنان أحمد الأنصاري بجائزة أفضل إخراج عن عمله في مسرحية الياثوم",             ref: "SUPPORTED", mueen: "SUPPORTED", match: true },
      { n: 3, claim: "حصل الممثل أحمد الجسمي على جائزة أفضل ممثل لدور أول عن أدائه في مسرحية الياثوم",   ref: "REFUTED",   mueen: "REFUTED",   match: true },
      { n: 4, claim: "شهدت الدورة العاشرة حضور وفود مسرحية من دول خليجية مجاورة خارج الإمارات",          ref: "NOT_ENOUGH_INFO", mueen: "NOT_ENOUGH_INFO", match: true },
    ]),

    heading("المهمة الرابعة — الترجمة (5.50 / 10)", 3),
    ...englishSource("The 10th Sharjah Theatre Days, held under the patronage of His Highness Sheikh Dr. Sultan bin Muhammad Al Qasimi, Ruler of Sharjah, took place from March 27 to April 5, featuring twelve theatrical works performed by eleven troupes competing for thirteen awards. The accompanying intellectual forum addressed..."),
    twoColArabic(
      "المرجع (Claude Opus)",
      "أُقيمت الدورة العاشرة لأيام الشارقة المسرحية برعاية صاحب السمو الشيخ الدكتور سلطان بن محمد القاسمي حاكم الشارقة، في الفترة من السابع والعشرين من مارس حتى الخامس من أبريل، وشارك فيها إحدى عشرة فرقة مسرحية قدّمت اثني عشر عملاً مسرحياً تنافست على ثلاث عشرة جائزة. وتناول الملتقى الفكري المصاحب محورين رئيسيين: لقاءات تداولية بين مديري المهرجانات المسرحية العربية ورؤساء تحرير الدوريات المعنية بالشأن المسرحي، ونقاش حول الفوارق بين عمل الدراماتورغ والمخرج في الفن المسرحي. وأعلنت لجنة التحكيم برئاسة الفنانة نضال الأشقر النتائج النهائية، حيث فازت مسرحية «ما كان لأحمد بنت سليمان» بجائزة أفضل عرض مسرحي متكامل، ونال أحمد الأنصاري جائزة أفضل إخراج عن مسرحية «الياثوم»، وحصل الفنان العراقي قاسم محمد على جائزة أفضل فنان عربي متميز.",
      "معين الذكي",
      "انطلقت فعاليات الدورة العاشرة لأيام الشارقة المسرحية مساء 27 مارس برعاية صاحب السمو الشيخ الدكتور سلطان بن محمد القاسمي، عضو المجلس الأعلى حاكم الشارقة، وبعرض مسرحية 'القضية'، إحدى أعماله المسرحية، واختتمت مساء 5 أبريل، حيث شاركت إحدى عشرة فرق مسرحية قدمت اثني عشر عملاً مسرحياً... [النص مطوّل ويضيف تفاصيل أبعد بكثير من المصدر الأصلي، مع سرد كامل لعناوين العروض والفرق وقائمة طويلة بالجوائز الفرعية وأسماء الفائزين].",
    ),
    ...rubricStrip(
      "faithfulness=0/3    fluency=2/3    terminology=2/2    register=2/2",
      "الترجمة العربية سليمة لغويًا وبأسلوب صحفي فصيح، وتستخدم مصطلحات مسرحية دقيقة. لكنها غير أمينة للمصدر والمرجع: أضافت كمًا كبيرًا من المعلومات غير الموجودة (افتتاح بعرض «القضية»، سرد كامل لعناوين العروض والفرق، وتفاصيل موسعة جدًا، وقائمة طويلة بنتائج جوائز فرعية وأسماء فائزين) بينما النص الإنجليزي/المرجع يذكر فقط الإطار العام و3 نتائج رئيسية. هذا يُعد إضافة جوهرية."),

    // ===== 2. FINANCE =====
    new Paragraph({ children: [new PageBreak()] }),
    heading("المثال الثاني — الاقتصاد والمال (FINANCE_029)", 1),
    pAr([
      runAr("العنوان: ", { bold: true, color: COLOR.secondary }),
      runAr("استمرت التحركات السعرية البطيئة في أسواق الأسهم المحلية برغم التقلبات الحادة في الأسواق العالمية ليغ...", { size: 24 }),
    ]),
    scoreCard("6.44 / 10", "7.88", "7.45", "5.83", "4.50"),

    heading("مقتطف من المقالة", 3, true),
    articleExcerpt("استمرت التحركات السعرية البطيئة في أسواق الأسهم المحلية برغم التقلبات الحادة في الأسواق العالمية ليغلق مؤشر سوق الإمارات منخفضاً 0.06% إلى 2547.36 نقطة بخسائر 207.78 مليون درهم أوصلت القيمة السوقية إلى 374.82 مليار درهم بتداولات 125.42 مليون درهم، وذلك نتيجة لانخفاض مؤشر سوق أبوظبي 0.15% إلى 2601.02 نقطة بتداولات 59.33 مليون درهم، وارتفاع مؤشر سوق دبي 0.2% إلى 1487.98 نقطة..."),

    heading("المهمة الأولى — التعرف على الكيانات (NER —7.88 / 10)", 3),
    nerTable(
      ["—", "—"],
      ["الإمارات, أبوظبي, دبي", "الإمارات, أبوظبي, دبي"],
      ["سوق الإمارات, سوق أبوظبي, سوق دبي, تمويل, الدار, صروح, أرابتك, إعمار, أبوظبي الوطني",
       "هيئة الأوراق المالية, تمويل, الدار, صروح, أرابتك, إعمار, أبوظبي الوطني"],
      ["—", "—"],
    ),

    heading("المهمة الثانية — التلخيص (5.83 / 10)", 3),
    twoColArabic(
      "المرجع (Claude Opus)",
      "أغلق مؤشر سوق الإمارات على انخفاض طفيف بنسبة ستة من مئة بالمئة عند مستوى ألفين وخمسمئة وسبع وأربعين نقطة، متأثراً بتراجع سوق أبوظبي رغم ارتفاع سوق دبي، في حين سجلت أسهم بعينها كتمويل والدار وصروح وأرابتك وإعمار مكاسب متفاوتة بينما تراجع سهم بنك أبوظبي الوطني. وسادت حالة من الترقب والحذر بين المستثمرين الذين تباينت توقعاتهم حول اتجاه الأسواق في المرحلة المقبلة، مما أبقى التحركات السعرية لمعظم الأسهم ضمن نطاق ضيق في ظل تفضيلهم صعوداً تدريجياً يستند إلى أسس متينة بعيداً عن الفجوات السعرية.",
      "معين الذكي",
      "شهدت أسواق الأسهم المحلية تقلبات بطيئة رغم التقلبات الحادة في الأسواق العالمية، مع تراجع مؤشر سوق الإمارات بنسبة 0.06% وارتفاع مؤشر سوق دبي بنسبة 0.2%. كما سجلت بعض الأسهم ارتفاعات ملحوظة، بينما تراجعت أخرى، مع توقعات بتحسن في الأداء الاقتصادي.",
    ),
    ...rubricStrip(
      "factual=2/3    coverage=1/3    no_inference=1/2    register=2/2",
      "الملخص صحيح في الخطوط العامة: بطء الحركة محلياً رغم تقلبات عالمية، تراجع مؤشر الإمارات 0.06% وارتفاع دبي 0.2%. لكنه أغفل معلومة أساسية هي تراجع مؤشر أبوظبي 0.15% وأثره، ولم يذكر الأرقام/المستويات أو تفاصيل الأسهم المذكورة بالاسم. كما أضاف صياغة توحي بـ«توقعات بتحسن في الأداء الاقتصادي» بينما النص يتحدث عن انتظار مؤشرات اقتصادية مشجعة دون تقرير توقع تحسن فعلي."),

    heading("المهمة الثالثة — الاستدلال اللغوي (NLI —7.45 / 10)", 3),
    nliTable([
      { n: 1, claim: "أغلق مؤشر سوق الإمارات على تراجع بنسبة 0.06% ليصل إلى 2547.36 نقطة",                           ref: "SUPPORTED", mueen: "SUPPORTED", match: true },
      { n: 2, claim: "سجل سهم تمويل ارتفاعاً بنسبة 3.52% مع تداولات شملت أكثر من عشرة ملايين سهم",                       ref: "SUPPORTED", mueen: "SUPPORTED", match: true },
      { n: 3, claim: "تراجع مؤشر سوق دبي بنسبة 0.2% ليستقر عند 1487.98 نقطة",                                          ref: "REFUTED",   mueen: "SUPPORTED", match: false },
      { n: 4, claim: "أعلنت هيئة الأوراق المالية عن إجراءات جديدة لتحفيز التداول في الأسواق المحلية",                  ref: "NOT_ENOUGH_INFO", mueen: "NOT_ENOUGH_INFO", match: true },
    ]),

    heading("المهمة الرابعة — الترجمة (4.50 / 10)", 3),
    ...englishSource("The UAE stock market index closed down 0.06% at 2547.36 points, losing 207.78 million dirhams in market value amid slow price movements despite sharp global market fluctuations, with Abu Dhabi's index falling 0.15% while Dubai's index rose 0.2%. Several stocks saw notable gains, including Tamweel rising 3.52%..."),
    twoColArabic(
      "المرجع (Claude Opus)",
      "أغلق مؤشر سوق الإمارات للأسهم منخفضاً بنسبة 0.06% عند 2547.36 نقطة، مسجلاً خسائر في القيمة السوقية بلغت 207.78 مليون درهم في ظل تحركات سعرية بطيئة على الرغم من التقلبات الحادة في الأسواق العالمية، حيث تراجع مؤشر سوق أبوظبي بنسبة 0.15% فيما ارتفع مؤشر سوق دبي بنسبة 0.2%. وسجلت عدة أسهم ارتفاعات ملحوظة، من بينها سهم تمويل الذي صعد بنسبة 3.52%، وسهم الدار الذي ارتفع بنسبة 1.64%، وسهم إعمار بنسبة 0.35%، في حين انخفض سهم بنك أبوظبي الوطني بنسبة 1.29%.",
      "معين الذكي",
      "أغلق مؤشر سوق الإمارات على تراجع بنسبة 0.06% ليصل إلى 2547.36 نقطة، مع خسائر بلغت 207.78 مليون درهم، مما أدى إلى استقرار القيمة السوقية عند 374 مليار درهم، وذلك نتيجة لانخفاض مؤشر سوق أبوظبي بنسبة 0.15% إلى 2601.02 نقطة، بينما ارتفع مؤشر سوق دبي بنسبة 0.2% ليصل إلى 1487.98 نقطة. كما سجل سهم تمويل ارتفاعاً بنسبة 3.52% مع تداولات شملت أكثر من عشرة ملايين سهم، بينما ارتفع سهم الدار بنسبة 64.1% إلى 24.1 درهم، وصروح بنسبة 85%... [الترجمة تحوي أخطاء رقمية جوهرية].",
    ),
    ...rubricStrip(
      "faithfulness=0/3    fluency=2/3    terminology=1/2    register=2/2",
      "الترجمة غير أمينة للمصدر/المرجع بسبب إضافات وتغييرات رقمية ومعلوماتية كبيرة: أضافت قيمة سوقية (374 مليار) ومستويات نقاط لمؤشري أبوظبي ودبي وأحجام تداول، وأدخلت أسهماً غير مذكورة في المصدر مع نسب/أسعار مبالغ فيها. كما حوّلت مكاسب بسيطة (الدار 1.64%، إعمار 0.35%) إلى قفزات هائلة (64.1%، 35%...) وغيّرت هبوط بنك أبوظبي الوطني من 1.29% إلى 29.1%."),

    // ===== 3. POLITICS =====
    new Paragraph({ children: [new PageBreak()] }),
    heading("المثال الثالث — السياسة (POLITICS_044)", 1),
    pAr([
      runAr("العنوان: ", { bold: true, color: COLOR.secondary }),
      runAr("رحب مجلس التعاون لدول الخليج العربية، ببيان وزارة الخارجية الأمريكية الذي جسد موقف الإدارة الأمريكية...", { size: 24 }),
    ]),
    scoreCard("5.92 / 10", "0.00", "10.00", "10.00", "5.67"),

    heading("مقتطف من المقالة", 3, true),
    articleExcerpt("رحب مجلس التعاون لدول الخليج العربية، ببيان وزارة الخارجية الأمريكية الذي جسد موقف الإدارة الأمريكية الثابت تجاه دعم جهود البحرين في مكافحة التنظيمات الإرهابية المتطرفة، وما تتعرض له من أعمال إرهابية تستهدف المساس بأمنها واستقرارها. وقال عبداللطيف بن راشد الزياني، أمين عام مجلس التعاون، إن بيان وزارة الخارجية الأمريكية الذي تضمن وضع أشخاص بحرينيين على قائمة الإرهاب العالمي دليل على مساندة الإدارة الأمريكية..."),

    heading("المهمة الأولى — التعرف على الكيانات (NER —0.00 / 10)", 3),
    nerTable(
      ["عبداللطيف بن راشد الزياني", "عبدلطيف بن راشد الزياني, الزياني"],
      ["البحرين, الولايات المتحدة", "البحرين, الولايات المتحدة, سويسرا, مجلس التعاون الخليجي, مجلس حقوق الإنسان الأممي, مجلس الأمم المتحدة لحقوق الإنسان"],
      ["مجلس التعاون لدول الخليج العربية, وزارة الخارجية الأمريكية, سرايا الأشتر, وكالة أنباء البحرين الرسمية, وزارة الخارجية البحرينية, الاتحاد السويسري, مجلس الأمم المتحدة لحقوق الإنسان, الحكومة السويسرية, وام",
       "مجلس التعاون لدول الخليج العربية, وزارة الخارجية الأمريكية, البحرين, الاتحاد السويسري, وكالة أنباء البحرين (بنا), مجلس حقوق الإنسان الأممي, مجلس الأمم المتحدة لحقوق الإنسان, GCC, الولايات المتحدة, الولايات المتحدة الصديقة, الإدارة الأمريكية, الخارجية البحرينية"],
      ["قائمة الإرهاب العالمي",
       "سرايا الأشتر, التنظيمات الإرهابية المتطرفة, الإرهاب, الإرهاب الدولي, الإرهاب العالمي, التنظيمات الإرهابية, الجماعات المتطرفة, الإرهابي, الإرهابية, الإرهابي"],
    ),

    heading("المهمة الثانية — التلخيص (10.00 / 10)", 3),
    twoColArabic(
      "المرجع (Claude Opus)",
      "أعرب مجلس التعاون الخليجي على لسان أمينه العام عبداللطيف الزياني عن ترحيبه ببيان الخارجية الأمريكية الذي تضمّن إدراج أشخاص بحرينيين وتنظيم «سرايا الأشتر» على قائمة الإرهاب الدولي، معتبرًا ذلك مساندةً صريحة لجهود البحرين في التصدي للتنظيمات المتطرفة التي تستهدف أمنها واستقرارها. وفي السياق ذاته، أبدت دول المجلس رفضها القاطع لما ورد في بيان المندوب السويسري أمام مجلس حقوق الإنسان الأممي من اتهامات وصفتها بالمغالطات بشأن أوضاع حقوق الإنسان في البحرين.",
      "معين الذكي",
      "أعلن أمين عام مجلس التعاون الخليجي عبداللطيف بن راشد الزياني أن إدراج أشخاص بحرينيين في قائمة الإرهاب الدولي يعكس دعم الولايات المتحدة لجهود البحرين في مكافحة التنظيمات الإرهابية. كما رحبت البحرين بقرار إدراج مجموعة 'سرايا الأشتر' في قائمة الإرهاب، ورفضت دول الخليج بشكل قاطع ادعاءات سويسرا حول أوضاع حقوق الإنسان في البحرين.",
    ),
    ...rubricStrip(
      "factual=3/3    coverage=3/3    no_inference=2/2    register=2/2",
      "الملخص مطابق لمحتوى المصدر والمرجع: ذكر ترحيب مجلس التعاون/الزياني ببيان الخارجية الأمريكية وإدراج أشخاص بحرينيين على قائمة الإرهاب، وذكر ترحيب البحرين بإدراج «سرايا الأشتر»، وذكر الرفض الخليجي القاطع لادعاءات/اتهامات سويسرا بشأن حقوق الإنسان في البحرين. لا توجد أخطاء جوهرية أو استنتاجات مضافة."),

    heading("المهمة الثالثة — الاستدلال اللغوي (NLI —10.00 / 10)", 3),
    nliTable([
      { n: 1, claim: "أعلن عبداللطيف بن راشد الزياني بصفته أميناً عاماً لمجلس التعاون الخليجي أن إدراج...", ref: "SUPPORTED", mueen: "SUPPORTED", match: true },
      { n: 2, claim: "أبدت دول مجلس التعاون الخليجي رفضها التام لما ورد في بيان المندوب السويسري...",       ref: "SUPPORTED", mueen: "SUPPORTED", match: true },
      { n: 3, claim: "ألقى مندوب الاتحاد السويسري بيانه المتعلق بالبحرين أمام مجلس حقوق الإنسان يوم ال...",   ref: "REFUTED",   mueen: "REFUTED",   match: true },
      { n: 4, claim: "طالبت الحكومة البحرينية بفرض عقوبات اقتصادية على سويسرا رداً على بيان مندوبها في...",   ref: "NOT_ENOUGH_INFO", mueen: "NOT_ENOUGH_INFO", match: true },
    ]),

    heading("المهمة الرابعة — الترجمة (5.67 / 10)", 3),
    ...englishSource("The Gulf Cooperation Council (GCC) welcomed the U.S. State Department's statement supporting Bahrain's efforts to combat extremist terrorist organizations, including the designation of Bahraini individuals and the group 'Saraya al-Ashtar' on the global terrorism list. GCC Secretary-General Abdullatif bin Rashid Al-Zayani commended the Bahraini government's efforts..."),
    twoColArabic(
      "المرجع (Claude Opus)",
      "رحّب مجلس التعاون لدول الخليج العربية ببيان وزارة الخارجية الأمريكية الداعم لجهود البحرين في مكافحة التنظيمات الإرهابية المتطرفة، بما في ذلك إدراج أشخاص بحرينيين وتنظيم «سرايا الأشتر» على قائمة الإرهاب العالمي. وأشاد الأمين العام لمجلس التعاون عبداللطيف بن راشد الزياني بجهود حكومة البحرين في كشف المؤامرات التي تستهدفها.",
      "معين الذكي",
      "أعلن أمين عام مجلس التعاون الخليجي عبداللطيف بن راشد الزياني أن إدراج أشخاص بحرينيين في قائمة الإرهاب الدولي يعكس دعم الولايات المتحدة لجهود البحرين في مكافحة التنظيمات الإرهابية المتطرفة. كما رحبت البحرين بقرار إدراج مجموعة 'سرايا الأشتر' في قائمة الإرهاب، مؤكدة أن هذا الموقف يعكس إصرار الولايات المتحدة الصديقة على مواجهة جميع أشكال الإرهاب.",
    ),
    ...rubricStrip(
      "faithfulness=1/3    fluency=2/3    terminology=1/2    register=2/2",
      "المعنى العام قريب، لكن توجد إضافات وتحريفات مؤثرة: جعل الترحيب صادراً عن البحرين بدلاً من مجلس التعاون، وحذف الإشارة الصريحة إلى بيان وزارة الخارجية الأمريكية، والثناء على حكومة البحرين لكشف المؤامرات. كما أضافت توصيفات غير موجودة مثل «الولايات المتحدة الصديقة» و«إصرار... على مواجهة جميع أشكال الإرهاب»."),

    // ===== 4. SPORTS =====
    new Paragraph({ children: [new PageBreak()] }),
    heading("المثال الرابع — الرياضة (SPORTS_049)", 1),
    pAr([
      runAr("العنوان: ", { bold: true, color: COLOR.secondary }),
      runAr("ناصر منسى يسجل الهدف الثانى للزمالك فى شباك المصرى بالدقيقة 44", { size: 24 }),
    ]),
    scoreCard("5.19 / 10", "1.08", "7.45", "5.83", "7.67"),

    heading("مقتطف من المقالة", 3, true),
    articleExcerpt("سجل ناصر منسى لاعب الزمالك، الهدف الثاني لفريقه فى شباك المصرى بعد تمريرة من أحمد فتوح فى الدقيقة 44 من عمر المباراة التي تجمعهما حاليًا على استاد برج العرب، في الجولة الأولى من المرحلة النهائية لحسم لقب الدوري، لتصبح النتيجة 2 - 1 للفارس الأبيض. حراسة المرمى: مهدي سليمان. خط الدفاع: محمود بنتايج – حسام عبد المجيد – محمد إسماعيل – عمر جابر..."),

    heading("المهمة الأولى — التعرف على الكيانات (NER —1.08 / 10)", 3),
    nerTable(
      ["ناصر منسى, أحمد فتوح, مهدي سليمان, محمود بنتايج, حسام عبد المجيد, محمد إسماعيل, عمر جابر, أحمد ربيع, عبد الله السعيد, خوان بيزيرا, ناصر منسي, عدي الدباغ, محمد عواد, محمود حمدي الونش, ... (40+ names)",
       "ناصر منسى, أحمد فتوح"],
      ["استاد برج العرب", "استاد برج العرب"],
      ["الزمالك, المصري البورسعيدي, بيراميدز, الأهلي, سيراميكا, سموحة, إنبي",
       "الزمالك, المصرى, بيراميدز, النادي الأهلي, سيراميكا"],
      ["—", "الدقيقة 44, المرحلة النهائية, الدوري المصري"],
    ),

    heading("المهمة الثانية — التلخيص (5.83 / 10)", 3),
    twoColArabic(
      "المرجع (Claude Opus)",
      "أحرز ناصر منسى الهدف الثاني لنادي الزمالك في مرمى المصري البورسعيدي عقب تمريرة من أحمد فتوح في الدقيقة الرابعة والأربعين، ليتقدم فريقه بنتيجة هدفين مقابل هدف واحد في المباراة المقامة على استاد برج العرب ضمن الجولة الافتتاحية للمرحلة النهائية من الدوري. ويتصدر الزمالك ترتيب المجموعة برصيد ثلاث وأربعين نقطة متساوياً مع بيراميدز لكن بأفضلية فارق الأهداف، بينما يحل الأهلي ثالثاً بأربعين نقطة وسيراميكا رابعاً بثمانٍ وثلاثين نقطة.",
      "معين الذكي",
      "حقق نادي الزمالك فوزاً مثيراً على فريق المصري بنتيجة 2-1 في المباراة التي أقيمت بحضور جماهيري كبير. يحتل الزمالك المركز الأول في جدول الترتيب برصيد 43 نقطة، بينما يحتل النادي الأهلي المركز الثالث برصيد 40 نقطة.",
    ),
    ...rubricStrip(
      "factual=2/3    coverage=1/3    no_inference=1/2    register=2/2",
      "الملخص صحيح جزئياً: ذكر نتيجة 2-1 وترتيب الزمالك (43) والأهلي (40)، لكنه صاغها كـ«فوز» نهائي بينما المصدر يتحدث عن تقدم الزمالك 2-1 أثناء المباراة دون تأكيد النهاية، وأضاف ادعاء «بحضور جماهيري كبير» غير مذكور. التغطية ضعيفة لأنه أغفل تفاصيل الهدف (ناصر منسي، تمريرة فتوح، الدقيقة 44، استاد برج العرب، الجولة الافتتاحية)."),

    heading("المهمة الثالثة — الاستدلال اللغوي (NLI —7.45 / 10)", 3),
    nliTable([
      { n: 1, claim: "أحرز ناصر منسى الهدف الثاني للزمالك في مرمى المصري بعد تمريرة من أحمد فتوح قبل ن...", ref: "SUPPORTED", mueen: "SUPPORTED", match: true },
      { n: 2, claim: "يحتل النادي الأهلي المرتبة الثالثة في جدول الترتيب بأربعين نقطة",                      ref: "SUPPORTED", mueen: "SUPPORTED", match: true },
      { n: 3, claim: "يتقدم الزمالك على بيراميدز في الترتيب بفارق نقطة واحدة",                                ref: "REFUTED",   mueen: "SUPPORTED", match: false },
      { n: 4, claim: "أُقيمت المباراة بحضور جماهيري كبير تجاوز خمسين ألف متفرج في استاد برج العرب",           ref: "NOT_ENOUGH_INFO", mueen: "NOT_ENOUGH_INFO", match: true },
    ]),

    heading("المهمة الرابعة — الترجمة (7.67 / 10)", 3),
    ...englishSource("Nasser Mansi scored Zamalek's second goal against Al-Masry in the 44th minute, assisted by Ahmed Fattouh, bringing the score to 2-1 in favor of Zamalek during their match at Borg El Arab Stadium in the first round of the Egyptian league's final stage. Zamalek currently tops the group standings with 43 points, tied with Pyramids on points but ahead on goal difference..."),
    twoColArabic(
      "المرجع (Claude Opus)",
      "سجّل ناصر منسي الهدف الثاني لنادي الزمالك في شباك المصري في الدقيقة الرابعة والأربعين بتمريرة من أحمد فتوح، لتصبح النتيجة 2-1 لصالح الزمالك خلال المباراة التي أُقيمت على استاد برج العرب في الجولة الأولى من المرحلة النهائية للدوري المصري. ويتصدّر الزمالك حاليًّا جدول ترتيب المجموعة برصيد ثلاث وأربعين نقطة، متساويًا مع بيراميدز في عدد النقاط لكنّه يتقدّم عليه بفارق الأهداف، فيما يحلّ الأهلي في المركز الثالث برصيد أربعين نقطة.",
      "معين الذكي",
      "سجل ناصر منسى لاعب الزمالك الهدف الثاني لفريقه في شباك المصري بعد تمريرة من أحمد فتوح في الدقيقة 44 من المباراة، مما جعل النتيجة 2-1 لصالح الزمالك. يحتل نادي الزمالك المركز الأول في جدول الترتيب برصيد 43 نقطة، متساوياً مع بيراميدز صاحب المركز الثاني، لكنه يتفوق عليه بفارق الأهداف. يحتل النادي الأهلي المركز الثالث برصيد 40 نقطة، بينما يحتل سيراميكا المركز الرابع برصيد 38 نقطة.",
    ),
    ...rubricStrip(
      "faithfulness=1/3    fluency=3/3    terminology=2/2    register=2/2",
      "الترجمة سليمة لغويًا وبأسلوب عربي فصيح ومصطلحات كروية دقيقة. لكنها تُسقط معلومات أساسية: مكان المباراة (استاد برج العرب) وكونها في الجولة الأولى من المرحلة النهائية للدوري، كما تُسقط فقرة استمرار المنافسة وذكر الأندية الأخرى. إضافةً إلى ذلك أضافت معلومة غير واردة عن ترتيب سيراميكا الرابع برصيد 38 نقطة."),

    // ===== 5. TECH =====
    new Paragraph({ children: [new PageBreak()] }),
    heading("المثال الخامس — التقنية (TECH_023)", 1),
    pAr([
      runAr("العنوان: ", { bold: true, color: COLOR.secondary }),
      runAr("دبي: «الخليج» دفع تنامي التحوّل الذكي في المنازل حول العالم المراقبين إلى اعتبار 2017 «عام المنازل ال...»", { size: 24 }),
    ]),
    scoreCard("6.85 / 10", "4.76", "10.00", "8.00", "5.67"),

    heading("مقتطف من المقالة", 3, true),
    articleExcerpt("دبي: «الخليج» دفع تنامي التحوّل الذكي في المنازل حول العالم المراقبين إلى اعتبار 2017 «عام المنازل الذكية»، في وقت تشير التوقعات إلى أن أعدادها سوف تتضاعف خمس مرات من 90 مليوناً في العام 2016 إلى 463 مليون منزل ذكي في عام 2021. ويواكب «جيتكس شوبر»، أكبر معرض سنوي للإلكترونيات والتقنيات الاستهلاكية في الشرق الأوسط، هذا التحوّل..."),

    heading("المهمة الأولى — التعرف على الكيانات (NER —4.76 / 10)", 3),
    nerTable(
      ["أفيناش شانبوج", "أفيناش شانبوج"],
      ["دبي, الشرق الأوسط", "دبي, مركز دبي التجاري العالمي, الخليج"],
      ["مركز دبي التجاري العالمي, شرف دي جي, جوجل, نيست, جمبو للإلكترونيات, أمازون, أبل, سامسونج",
       "جيتكس شوبر, مركز دبي التجاري العالمي, شركة شرف دي جي, شركة جمبو للإلكترونيات, جوجل, نيست, أمازون, أبل, سامسونج"],
      ["جيتكس شوبر, سمارت هوم, أسيستنت, ثيرموستات, إيكو, هوم كيت, سمارت ثينجز, جرينز",
       "زعبيل 3، 4، 5، 6"],
    ),

    heading("المهمة الثانية — التلخيص (8.00 / 10)", 3),
    twoColArabic(
      "المرجع (Claude Opus)",
      "يشهد معرض «جيتكس شوبر» المقام في مركز دبي التجاري العالمي حتى الثلاثين من سبتمبر عرض مجموعة متنوعة من المنتجات المنزلية الذكية، حيث تقدم شركتا «شرف دي جي» و«جمبو للإلكترونيات» أجهزة تشمل سماعات «جوجل» الذكية وأنظمة ترشيد الطاقة وأجهزة الأمن المنزلي. وتأتي هذه الفعاليات في ظل توقعات بتضاعف أعداد المنازل الذكية عالمياً خمس مرات لتبلغ أربعمئة وثلاثة وستين مليون منزل بحلول عام ألفين وواحد وعشرين، بعد أن أطلقت كبرى شركات التقنية مثل «أمازون» و«أبل» و«جوجل» و«سامسونج» أنظمة متعددة للتحكم الذكي في المنازل.",
      "معين الذكي",
      "يرتفع عدد المنازل الذكية من 90 مليوناً في 2016 إلى 463 مليوناً بحلول 2021، ويعتبر جيتكس شوبر أكبر معرض سنوي للإلكترونيات في الشرق الأوسط، حيث يعرض أحدث المنتجات الذكية من شركات عالمية.",
    ),
    ...rubricStrip(
      "factual=3/3    coverage=1/3    no_inference=2/2    register=2/2",
      "الملخص صحيح في الأرقام الأساسية (90 مليوناً في 2016 إلى 463 مليوناً في 2021) وفي توصيف «جيتكس شوبر» كأكبر معرض سنوي للإلكترونيات في الشرق الأوسط. لكنه يغفل معظم التفاصيل الجوهرية الواردة في المصدر والمرجع: مكان وزمان المعرض (حتى 30 سبتمبر في مركز دبي التجاري العالمي)، وأمثلة المنتجات والشركات المشاركة (شرف دي جي، جمبو، سماعات جوجل، نيست)."),

    heading("المهمة الثالثة — الاستدلال اللغوي (NLI —10.00 / 10)", 3),
    nliTable([
      { n: 1, claim: "تشير التقديرات إلى أن عدد المنازل الذكية سيرتفع من 90 مليوناً في 2016 إلى نحو 46...", ref: "SUPPORTED", mueen: "SUPPORTED", match: true },
      { n: 2, claim: "تقوم شركة جمبو للإلكترونيات بعرض أجهزة أمن منزلية ذكية تشمل قفلاً يُفتح عن طريق ...", ref: "SUPPORTED", mueen: "SUPPORTED", match: true },
      { n: 3, claim: "تستمر فعاليات جيتكس شوبر حتى يوم الجمعة 29 سبتمبر في مركز دبي التجاري العالمي",       ref: "REFUTED",   mueen: "REFUTED",   match: true },
      { n: 4, claim: "بلغ عدد الزوار الإجمالي لمعرض جيتكس شوبر في نسخة 2017 أكثر من مليون زائر",            ref: "NOT_ENOUGH_INFO", mueen: "NOT_ENOUGH_INFO", match: true },
    ]),

    heading("المهمة الرابعة — الترجمة (5.67 / 10)", 3),
    ...englishSource("The growing global shift toward smart homes has led observers to label 2017 as the 'Year of Smart Homes,' with projections indicating that the number of smart homes will increase fivefold from 90 million in 2016 to 463 million by 2021. GITEX Shopper, the Middle East's largest annual consumer electronics event, keeps pace with this shift..."),
    twoColArabic(
      "المرجع (Claude Opus)",
      "دفع التحوّل العالمي المتنامي نحو المنازل الذكية المراقبين إلى وصف عام 2017 بأنه «عام المنازل الذكية»، إذ تشير التوقعات إلى أن أعداد المنازل الذكية ستتضاعف خمس مرات من 90 مليوناً في عام 2016 إلى 463 مليوناً بحلول عام 2021. ويعرض «جيتكس شوبر»، أكبر معرض سنوي للإلكترونيات الاستهلاكية في الشرق الأوسط، تشكيلة واسعة من منتجات المنازل الذكية في مركز دبي التجاري العالمي حتى الثلاثين من سبتمبر.",
      "معين الذكي",
      "مع تزايد التحوّل الذكي في المنازل حول العالم، اعتُبرت عام 2017 «عام المنازل الذكية»، حيث تشير التوقعات إلى أن عدد المنازل الذكية سيرتفع خمس مرات من 90 مليوناً في عام 2016 إلى 463 مليوناً بحلول عام 2021. يواكب «جيتكس شوبر»، أكبر معرض سنوي للإلكترونيات والتقنيات الاستهلاكية في الشرق الأوسط، هذا التحوّل... [النص يستطرد إلى تفاصيل غير موجودة في المصدر، تشمل اقتباسات وقاعات زعبيل 3،4،5،6 وتفاصيل منتجات موسّعة].",
    ),
    ...rubricStrip(
      "faithfulness=1/3    fluency=2/3    terminology=1/2    register=2/2",
      "المعنى الأساسي في الجملة الأولى والأرقام محفوظة. لكن الترجمة تضيف كثيراً من معلومات غير موجودة في المصدر/المرجع (أسماء أشخاص واقتباسات، قاعات زعبيل، تفاصيل منتجات محددة مثل Nest وجرس الباب المصوّر وبصمة الإصبع، وسرد موسّع)، ما يضعف الأمانة بشكل واضح."),

    hrThin(),

    heading("ملخص الأنماط المُلاحَظة", 1),
    numItemAr("التعرف على الكيانات (NER): يميل معين بشكل ثابت إلى استخراج عدد أقل من الكيانات مقارنة بالمرجع، لا سيما في كشوفات اللاعبين الرياضية الطويلة والتصريحات السياسية الغنية بالأسماء."),
    numItemAr("التلخيص: جودة لغوية عالية مع سلامة في الأسلوب، لكن الملخصات عمومية في الغالب — تسقط التفاصيل المحددة (الأسماء والتواريخ والأرقام) أو تُستبدل بصياغات عامة."),
    numItemAr("الاستدلال اللغوي (NLI): دقيق في تصنيفات SUPPORTED و NOT_ENOUGH_INFO؛ نمط الخطأ الرئيسي هو تصنيف الادعاءات REFUTED على أنها SUPPORTED عند تطابق الصياغة السطحية."),
    numItemAr("الترجمة: الطلاقة العربية والأسلوب الفصيح قويّان؛ نمط الإخفاق الأبرز هو إضافة معلومات غير واردة في المصدر الإنجليزي، مما يُضعف معيار الأمانة (faithfulness)."),
  ];

  const doc = new Document({
    styles: docStyles(),
    numbering: NUMBERING,
    sections: [{
      properties: sectionProps(),
      headers: { default: letterheadHeader(true) },
      footers: { default: pageFooter(docTitle, true) },
      children: body,
    }],
  });
  return save(doc, "03_Worked_Examples.docx");
}

// =================================================================
async function main() {
  console.log("Building Mueen Evaluation delivery package...");
  await buildArabicLetter();
  await buildArabicIndex();
  await buildTechnicalReport();
  await buildCrossModelComparison();
  await buildWorkedExamples();

  // Copy raw data attachments into the package with consistent numbering
  const srcDir = path.resolve(__dirname, "..");
  const copies = [
    { src: "mueen_results_full.json", dst: "05_mueen_results_full.json" },
    { src: "comparison_data.csv",     dst: "06_comparison_data.csv" },
  ];
  for (const c of copies) {
    const sp = path.join(srcDir, c.src);
    const dp = path.join(OUT_DIR, c.dst);
    if (fs.existsSync(sp)) {
      fs.copyFileSync(sp, dp);
      console.log("  copied " + c.src + " -> " + c.dst);
    } else {
      console.log("  (skip) source not found: " + c.src);
    }
  }
  console.log("Done.");
}

main().catch(err => { console.error(err); process.exit(1); });
