// qa296/probe296.js — 用 runtime 真分類器試分類候選對白句。
// 用法：node qa296/probe296.js "句1" "句2" ...
const fs = require("fs");
const path = require("path");
const ROOT = path.join(__dirname, "..");
const html = fs.readFileSync(path.join(ROOT, "index.html"), "utf-8");
function sliceBetween(a, b) {
  const x = html.indexOf(a);
  if (x < 0) throw new Error("marker not found: " + a);
  const y = b ? html.indexOf(b, x) : html.length;
  return html.slice(x, y);
}
function sliceLineContaining(marker) {
  const a = html.indexOf(marker);
  if (a < 0) throw new Error("marker not found: " + marker);
  const b = html.indexOf("\n", a);
  return html.slice(a, b < 0 ? html.length : b);
}
const parts = [];
parts.push(sliceLineContaining("const DLG106_CATEGORIES"));
parts.push(sliceLineContaining("const DLG106_CAT_TO_EXPR"));
parts.push(sliceLineContaining("const DLG106_OLD_EMOTION_TO_CAT"));
parts.push(sliceLineContaining("const DLG106_EXPR_TO_CAT"));
parts.push(sliceLineContaining("const DLG106_EMOTION_MAP"));
parts.push(sliceBetween("var DLG106_PUNCT", "/* 阿偉成長階段"));
const code = parts.join("\n");
const lines = process.argv.slice(2);
const driver = `
;__out = input.map((t) => {
  const cat = dlg106ResolveCategory({ emotion: null, text: t });
  return { text: t, category: cat, expr: DLG106_CAT_TO_EXPR[cat] || "base" };
});
`;
const input = lines;
let __out;
eval(code + driver);
for (const r of __out) console.log(r.category + " -> " + r.expr + " | " + r.text);
