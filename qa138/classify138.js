// qa138/classify138.js — 用 index.html 真函數跑 dlg106ResolveCategory。
// 抽取範圍：DLG106_PUNCT／dlg106Normalize…dlg106ExprFor／DLG106_EMOTION_MAP／
// DLG106_CATEGORIES／DLG106_CAT_TO_EXPR／DLG106_OLD_EMOTION_TO_CAT／DLG106_EXPR_TO_CAT。
// 用法：node qa138/classify138.js qa138/occ_all_for_classify.json qa138/classify138.json
// 輸出：[{text, emotion, category, expr}]（expr 由 DLG106_CAT_TO_EXPR 派生）。
const fs = require("fs");
const html = fs.readFileSync("index.html", "utf-8");

function sliceBetween(startMarker, endMarker) {
  const a = html.indexOf(startMarker);
  if (a < 0) throw new Error("marker not found: " + startMarker);
  const b = endMarker ? html.indexOf(endMarker, a) : html.length;
  if (b < 0) throw new Error("end marker not found: " + endMarker);
  return html.slice(a, b);
}
function sliceLineContaining(marker) {
  const a = html.indexOf(marker);
  if (a < 0) throw new Error("marker not found: " + marker);
  const b = html.indexOf("\n", a);
  return html.slice(a, b < 0 ? html.length : b);
}

const parts = [];
// consts first (26243-26246)
parts.push(sliceLineContaining("const DLG106_CATEGORIES"));
parts.push(sliceLineContaining("const DLG106_CAT_TO_EXPR"));
parts.push(sliceLineContaining("const DLG106_OLD_EMOTION_TO_CAT"));
parts.push(sliceLineContaining("const DLG106_EXPR_TO_CAT"));
// emotion map (single huge line)
parts.push(sliceLineContaining("const DLG106_EMOTION_MAP"));
// punct + functions block (26507..end of dlg106ExprFor)
parts.push(sliceBetween("var DLG106_PUNCT", "/* 阿偉成長階段"));
// note: dlg106ExprFor is inside that span; the span ends at the awi comment after it.
const code = parts.join("\n");
const input = JSON.parse(fs.readFileSync(process.argv[2], "utf-8"));
const driver = `
;__classified = input.map((row) => {
  const cat = dlg106ResolveCategory({ emotion: row.emotion || null, text: row.text });
  return { text: row.text, emotion: row.emotion || null, category: cat,
           expr: DLG106_CAT_TO_EXPR[cat] || "base" };
});`;
let __classified;
eval(code + driver);
const out = __classified;
fs.writeFileSync(process.argv[3], JSON.stringify(out, null, 1), "utf-8");
const counts = {};
out.forEach((r) => { counts[r.category] = (counts[r.category] || 0) + 1; });
console.log("classified:", out.length, JSON.stringify(counts));
