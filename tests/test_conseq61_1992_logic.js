// v20a136 CONSEQ61 1992 年終評核 — 邏輯測試。
//   抽 index.html 真函數（CONSEQ61_REVIEWS＋calib60YearOfWeek＋conseq61State＋conseq61DualOf＋
//   conseq61LegacyMark＋conseq61SettleEval）喺 vm 沙盒行。
//   (1) 1992 條目數字：floor 155／warnLine 195／boundaryWeek 156，calib60YearOfWeek(156)＝1992；
//   (2) 警告：152–155 週、dual < 195 先出聲，dual ≥ 195 唔出聲；
//   (3) 邊界週 156：dual 154 收場（pendingEnding review／1992）、dual 155 過關；
//   (4) 舊檔：1993 年存檔靜默標記 1992 已過；1992 年 12 月存檔唔標記；已收科存檔標記；
//   (5) 1990／1991 條目數字不變。
// 反證：拎走 1992 條目嗰陣，week 156 dual 100 唔會收場（證明 1992 條目先係觸發源）。
// 用法：node tests/test_conseq61_1992_logic.js [path-to-index.html]
const fs = require("fs");
const path = require("path");
const vm = require("vm");
const htmlPath = process.argv[2] || path.join(__dirname, "..", "index.html");
const html = fs.readFileSync(htmlPath, "utf8");
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? "PASS" : "FAIL") + " " + name); }
function extractConst(name){
  const i = html.indexOf("const " + name + " =");
  if(i < 0) throw new Error("const not found: " + name);
  let depth = 0, started = false, j = i;
  for(; j < html.length; j++){
    const c = html[j];
    if(c === "{" || c === "["){ depth++; started = true; }
    else if(c === "}" || c === "]"){ depth--; if(started && depth === 0){ j++; break; } }
  }
  return html.slice(html.indexOf("=", i) + 1, j);
}
function extractFn(name){
  const i = html.indexOf("function " + name + "(");
  if(i < 0) throw new Error("fn not found: " + name);
  let depth = 0, j = html.indexOf("{", i);
  for(; j < html.length; j++){
    if(html[j] === "{") depth++;
    else if(html[j] === "}"){ depth--; if(depth === 0) break; }
  }
  return html.slice(i, j + 1);
}
function makeCtx(reviewsSrc){
  const sb = { console: console };
  vm.createContext(sb);
  const src = "const START = " + extractConst("START") + ";\n"
    + "const CONSEQ61_REVIEWS = " + reviewsSrc + ";\n"
    + "const CONSEQ61_CFG = " + extractConst("CONSEQ61_CFG") + ";\n"
    + ["calib60YearOfWeek", "conseq61State", "conseq61DualOf", "conseq61LegacyMark", "conseq61SettleEval"]
      .map(extractFn).join("\n");
  vm.runInContext(src, sb);
  return sb;
}
const REVIEWS_SRC = extractConst("CONSEQ61_REVIEWS");
const sb = makeCtx(REVIEWS_SRC);
function run(sb, code){ return vm.runInContext(code, sb); }
function mkState(dual, dayIndex){
  return { fame: dual, industryCredit: 0, money: 5000, dayIndex: dayIndex || 0, conseq61: {}, shoots: [] };
}

/* (1) 條目數字＋曆法對位 */
{
  const r = run(sb, "CONSEQ61_REVIEWS[1992]");
  ok("1992 條目：floor 155／warnLine 195／boundaryWeek 156",
    r && r.floor === 155 && r.warnLine === 195 && r.boundaryWeek === 156);
  ok("calib60YearOfWeek(156)＝1992", run(sb, "calib60YearOfWeek(156)") === 1992);
  ok("calib60YearOfWeek(152)＝1992（警告週同屬 1992）", run(sb, "calib60YearOfWeek(152)") === 1992);
  const r90 = run(sb, "CONSEQ61_REVIEWS[1990]");
  const r91 = run(sb, "CONSEQ61_REVIEWS[1991]");
  ok("1990／1991 條目數字不變（45／65／52；100／130／104）",
    r90 && r90.floor === 45 && r90.warnLine === 65 && r90.boundaryWeek === 52
    && r91 && r91.floor === 100 && r91.warnLine === 130 && r91.boundaryWeek === 104);
}

/* (2) 警告：152–155 週、dual < warnLine 先出聲 */
{
  const st = mkState(150, 1050);
  const lines = run(sb, "(function(){ const st = " + JSON.stringify(st) + "; const L = conseq61SettleEval(st, 152); return { lines: L, reviews: st.conseq61.reviews }; })()");
  ok("week 152＋dual 150：有 1992 評核警告", lines.lines.some(l=>String(l).indexOf("1992") >= 0));
  ok("week 152 警告唔判收場", !lines.reviews[1992]);
  const st2 = mkState(200, 1050);
  const lines2 = run(sb, "(function(){ const st = " + JSON.stringify(st2) + "; return conseq61SettleEval(st, 152); })()");
  ok("week 152＋dual 200（≥warnLine 195）：唔出聲", !lines2.some(l=>String(l).indexOf("1992") >= 0));
  const st3 = mkState(140, 1080);
  const lines3 = run(sb, "(function(){ const st = " + JSON.stringify(st3) + "; return conseq61SettleEval(st, 155); })()");
  ok("week 155（邊界前 1 週）＋dual 140：強警告提到 1992 年尾評核", lines3.some(l=>String(l).indexOf("1992 年尾評核") >= 0));
  ok("week 155 強警告原文：下週就係 1992 年尾評核＋dual＋floor 155", lines3.some(l=>{ const s = String(l); return s.indexOf("下週就係 1992 年尾評核") >= 0 && s.indexOf("140") >= 0 && s.indexOf("155") >= 0; }));
  const st4 = mkState(150, 900);
  const lines4 = run(sb, "(function(){ const st = " + JSON.stringify(st4) + "; return conseq61SettleEval(st, 150); })()");
  ok("week 150（邊界前 6 週）：唔出 1992 警告", !lines4.some(l=>String(l).indexOf("1992") >= 0));
}

/* (3) 邊界週 156 即判 */
{
  const low = run(sb, "(function(){ const st = " + JSON.stringify(mkState(154, 1091)) + "; const L = conseq61SettleEval(st, 156); return { lines: L, rev: st.conseq61.reviews[1992], pend: st.conseq61.pendingEnding }; })()");
  ok("week 156＋dual 154（<floor 155）：判收場", low.rev && low.rev.passed === false);
  ok("week 156＋dual 154：pendingEnding kind review／year 1992",
    low.pend && low.pend.kind === "review" && low.pend.year === 1992 && low.pend.floor === 155);
  ok("week 156＋dual 154：結算行文有「1992 年尾評核結果出咗」",
    low.lines.some(l=>String(l).indexOf("1992 年尾評核結果出咗") >= 0));
  const edge = run(sb, "(function(){ const st = " + JSON.stringify(mkState(155, 1091)) + "; const L = conseq61SettleEval(st, 156); return { rev: st.conseq61.reviews[1992], pend: st.conseq61.pendingEnding }; })()");
  ok("week 156＋dual 155（＝floor）：過關，唔收場", edge.rev && edge.rev.passed === true && !edge.pend);
  const hi = run(sb, "(function(){ const st = " + JSON.stringify(mkState(210, 1091)) + "; conseq61SettleEval(st, 156); return st.conseq61.reviews[1992]; })()");
  ok("week 156＋dual 210：過關紀錄 dual 210", hi && hi.passed === true && hi.dual === 210);
}

/* (4) 舊檔安全：conseq61LegacyMark */
{
  const m1993 = run(sb, "(function(){ const st = { dayIndex: 1096, conseq61: {} }; conseq61LegacyMark(st); return st.conseq61.reviews; })()");
  ok("1993 年舊檔：1992 評核靜默標記已過（legacy）", m1993 && m1993[1992] && m1993[1992].passed === true && m1993[1992].legacy === true);
  const m1992 = run(sb, "(function(){ const st = { dayIndex: 1065, conseq61: {} }; conseq61LegacyMark(st); return st.conseq61.reviews; })()");
  ok("1992-12-01 舊檔：1992 評核唔標記（仲未過）", m1992 && !m1992[1992]);
  const mEnd = run(sb, "(function(){ const st = { dayIndex: 500, ending410: { career: 'E0' }, conseq61: {} }; conseq61LegacyMark(st); return st.conseq61.reviews; })()");
  ok("已收科舊檔：1992 評核靜默標記", mEnd && mEnd[1992] && mEnd[1992].legacy === true);
}

/* 反證：冇 1992 條目嗰陣 week 156 唔收場 */
{
  const revObj = JSON.parse(JSON.stringify(eval("(" + REVIEWS_SRC + ")")));
  delete revObj[1992];
  const sbM = makeCtx(JSON.stringify(revObj));
  const r = run(sbM, "(function(){ const st = " + JSON.stringify(mkState(100, 1091)) + "; conseq61SettleEval(st, 156); return st.conseq61.pendingEnding; })()");
  ok("反證：冇 1992 條目嗰陣 week 156＋dual 100 唔收場", !r);
}

if(fails.length){ console.error("FAILURES: " + fails.join(" | ")); process.exit(1); }
console.log("ALL PASS (conseq61 1992 logic)");
