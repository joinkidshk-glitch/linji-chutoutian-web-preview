// v20a136 結局閘搬去 1992 年 12 月 — 閘邏輯守門測試。
//   抽 index.html 真函數（evalGate3Y＋readCtx＋done＋gate3YEntry＋seasonKeyOf＋gatePath＋nodeId）
//   喺 vm 沙盒行，awardsGetFlag 用假旗標表（done／skipped／invited／pending／空字串／throw／undefined）。
//   (1) C17 喺 1992-01（week 105）唔開；(2) 1992-11（week 152）唔開；(3) 1992-11-30（week 153，秋）唔開；
//   (4) 1992-12-01（week 153）＋台慶未解決唔開（invited／pending／空字串）；
//   (5) week 153＋台慶已解決（done／skipped）開；(6) dayIndex 1096 之後無條件開（連 C13 未做都開，
//       季節唔啱都開）；(7) defensive：awardsGetFlag 唔存在／throw 嗰陣唔 crash、當未解決；
//   (8) C13 閘不變（1992 冬 1–2 月照開）；(9) scrub：已收科舊檔唔清 C17，未收科＋week<153 先清。
// 反證：閘表 copy 拎走 weekMin／awardResolved／backstopDay 嗰陣，對應斷言必須反轉
//       （證明斷言對新欄位敏感，唔係永遠 PASS）；舊閘（得 yearEq＋seasonIn）喺 1992-01 會開。
// 用法：node tests/test_story_gate136_logic.js [path-to-index.html]
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
function makeCtx(gate){
  const flags = {};
  const sb = {
    console: console,
    STORY_GATE_3Y: gate,
    SEASON_KEY: { "春":"spring", "夏":"summer", "秋":"autumn", "冬":"winter", spring:"spring", summer:"summer", autumn:"autumn", winter:"winter" },
    featureFlag_softBehaviorGatePreview: function(){ return false; },
    awardsGetFlag: function(year, id){ return flags[year + "/" + id] || ""; },
    __flags: flags,
  };
  sb.__setFlag = function(year, id, st){ flags[year + "/" + id] = st; };
  vm.createContext(sb);
  const src = ["nodeId", "gate3YEntry", "seasonKeyOf", "gatePath", "readCtx", "done", "evalGate3Y", "storyGate113Scrub"]
    .map(extractFn).join("\n");
  vm.runInContext(src, sb);
  return sb;
}
const GATE = eval("(" + extractConst("STORY_GATE_3Y") + ")");
const sb = makeCtx(GATE);
function evalC17(ctx){
  return vm.runInContext("evalGate3Y(\"C17\", { ctx: " + JSON.stringify(ctx) + " })", sb);
}
function baseCtx(over){
  return Object.assign({
    week: 153, dayIndex: 1065, year: 1992, season: "冬",
    done: { C13: true }, lastMainDoneDay: null, fame: 0, credit: 0, tags: [], flags: {},
  }, over || {});
}

/* (0) 閘表靜態形狀 */
ok("C17 weekMin＝153（1992-12-01 第 153 週）", GATE.C17 && GATE.C17.weekMin === 153);
ok("C17 awardResolved＝{ ceremonyId: award_singho_tv, year: 1992 }",
  GATE.C17 && GATE.C17.awardResolved && GATE.C17.awardResolved.ceremonyId === "award_singho_tv" && GATE.C17.awardResolved.year === 1992);
ok("C17 backstopDay＝1096（1993-01-01）", GATE.C17 && GATE.C17.backstopDay === 1096);
ok("C17 保留 needDone C13＋yearEq 1992＋seasonIn 冬", GATE.C17 && JSON.stringify(GATE.C17.needDone) === '["C13"]'
  && GATE.C17.yearEq === 1992 && JSON.stringify(GATE.C17.seasonIn) === '["冬"]');

/* (1) 1992-01 唔開（舊閘會開嘅位） */
{
  const r = evalC17(baseCtx({ week: 105, dayIndex: 730, year: 1992, season: "冬" }));
  ok("1992-01（week 105）C17 唔開", r && r.ok === false);
  ok("1992-01 原因有 weekMin:153", r && r.reasons.indexOf("weekMin:153") >= 0);
}
/* (2) 1992-11 唔開 */
{
  const r = evalC17(baseCtx({ week: 152, dayIndex: 1057, year: 1992, season: "秋" }));
  ok("1992-11（week 152）C17 唔開", r && r.ok === false);
}
/* (3) 1992-11-30：week 153 但係秋，唔開 */
{
  const r = evalC17(baseCtx({ week: 153, dayIndex: 1064, year: 1992, season: "秋" }));
  ok("1992-11-30（week 153，秋）C17 唔開", r && r.ok === false);
  ok("1992-11-30 原因有 seasonIn", r && r.reasons.some(t=>String(t).indexOf("seasonIn:") === 0));
}
/* (4) 1992-12-01＋台慶未解決唔開 */
{
  const cases = [
    ["旗標空字串", ""],
    ["旗標 invited", "invited"],
    ["旗標 pending", "pending"],
  ];
  cases.forEach(pair=>{
    sb.__setFlag(1992, "award_singho_tv", pair[1]);
    const r = evalC17(baseCtx({ week: 153, dayIndex: 1065, year: 1992, season: "冬" }));
    ok("1992-12-01＋台慶" + pair[0] + " C17 唔開", r && r.ok === false);
    ok("1992-12-01＋台慶" + pair[0] + " 原因有 awardResolved", r && r.reasons.indexOf("awardResolved:1992/award_singho_tv") >= 0);
  });
  /* 1992 年 1 月嗰場台慶係屆別 1991——佢嘅 flag 唔可以誤觸 1992 條件 */
  sb.__setFlag(1991, "award_singho_tv", "done");
  sb.__setFlag(1992, "award_singho_tv", "");
  const r = evalC17(baseCtx({ week: 153, dayIndex: 1065, year: 1992, season: "冬" }));
  ok("屆別 1991 done 唔會誤觸 1992 條件", r && r.ok === false);
}
/* (5) week 153＋台慶已解決開 */
["done", "skipped"].forEach(st=>{
  sb.__setFlag(1992, "award_singho_tv", st);
  const r = evalC17(baseCtx({ week: 153, dayIndex: 1065, year: 1992, season: "冬" }));
  ok("1992-12-01＋台慶 " + st + " C17 開", r && r.ok === true);
});
/* (6) backstop：dayIndex 1096 之後無條件開 */
{
  sb.__setFlag(1992, "award_singho_tv", "");
  const r1 = evalC17(baseCtx({ week: 157, dayIndex: 1096, year: 1993, season: "冬", done: {} }));
  ok("dayIndex 1096＋C13 未做 C17 照開（backstop）", r1 && r1.ok === true);
  ok("backstop 回傳 token backstopDay:1096", r1 && r1.and && r1.and.length === 1 && r1.and[0].token === "backstopDay:1096");
  const r2 = evalC17(baseCtx({ week: 157, dayIndex: 1100, year: 1993, season: "夏", done: {} }));
  ok("dayIndex 1100＋季節唔啱 C17 照開（backstop 繞過全部條件）", r2 && r2.ok === true);
  const r3 = evalC17(baseCtx({ week: 156, dayIndex: 1095, year: 1992, season: "冬", done: {} }));
  ok("dayIndex 1095（未到 backstop）＋C13 未做 C17 唔開", r3 && r3.ok === false);
}
/* (7) defensive：awardsGetFlag 唔存在／throw 唔 crash、當未解決 */
{
  const sb2 = makeCtx(GATE);
  sb2.awardsGetFlag = undefined;
  const r1 = vm.runInContext("evalGate3Y(\"C17\", { ctx: " + JSON.stringify(baseCtx()) + " })", sb2);
  ok("awardsGetFlag 未定義：唔 crash、當未解決（唔開）", r1 && r1.ok === false);
  const sb3 = makeCtx(GATE);
  sb3.awardsGetFlag = function(){ throw new Error("flags boom"); };
  const r2 = vm.runInContext("evalGate3Y(\"C17\", { ctx: " + JSON.stringify(baseCtx()) + " })", sb3);
  ok("awardsGetFlag throw：唔 crash、當未解決（唔開）", r2 && r2.ok === false);
}
/* (8) C13 閘不變 */
{
  const r = vm.runInContext("evalGate3Y(\"C13\", { ctx: " + JSON.stringify({ week: 105, dayIndex: 730, year: 1992, season: "冬", done: {}, lastMainDoneDay: null }) + " })", sb);
  ok("C13 喺 1992-01（冬）照開（閘不變）", r && r.ok === true);
}
/* (9) scrub：已收科舊檔唔清 C17 */
{
  function mkSave(dayIndex, doneIds, ending410){
    const done = {};
    doneIds.forEach(id=>{ done[id] = true; });
    const o = { dayIndex: dayIndex, story: { done: done } };
    if(ending410) o.ending410 = { career: "E0" };
    return o;
  }
  const s1 = mkSave(742, ["C13", "C17"], true);
  const c1 = vm.runInContext("storyGate113Scrub(" + JSON.stringify(s1).replace(/"/g, "'") + ")", sb);
  ok("已收科舊檔（C17 喺 week 107 做完）：scrub 唔清 C17", Array.isArray(c1) && c1.indexOf("C17") < 0);
  const s2 = mkSave(742, ["C13", "C17"], false);
  const c2 = vm.runInContext("storyGate113Scrub(" + JSON.stringify(s2).replace(/"/g, "'") + ")", sb);
  ok("未收科＋week<153 嘅 C17 紀錄：scrub 清走", Array.isArray(c2) && c2.indexOf("C17") >= 0);
  const s3 = mkSave(1120, ["C13", "C17"], false);
  const c3 = vm.runInContext("storyGate113Scrub(" + JSON.stringify(s3).replace(/"/g, "'") + ")", sb);
  ok("week≥153 嘅 C17 紀錄：scrub 唔郁", Array.isArray(c3) && c3.indexOf("C17") < 0);
}

/* 反證：殘廢閘（拎走新欄位）對應斷言必須反轉 */
{
  const gMut = JSON.parse(JSON.stringify(GATE));
  delete gMut.C17.weekMin; delete gMut.C17.awardResolved; delete gMut.C17.backstopDay;
  const sbM = makeCtx(gMut);
  const rJan = vm.runInContext("evalGate3Y(\"C17\", { ctx: " + JSON.stringify(baseCtx({ week: 105, dayIndex: 730, year: 1992, season: "冬" })) + " })", sbM);
  ok("反證：冇 weekMin／awardResolved 嗰陣 1992-01 會開（證明新欄位先係守衛）", rJan && rJan.ok === true);
  const gMut2 = JSON.parse(JSON.stringify(GATE));
  delete gMut2.C17.backstopDay;
  const sbM2 = makeCtx(gMut2);
  const rBs = vm.runInContext("evalGate3Y(\"C17\", { ctx: " + JSON.stringify(baseCtx({ week: 157, dayIndex: 1096, year: 1993, season: "冬", done: {} })) + " })", sbM2);
  ok("反證：冇 backstopDay 嗰陣 dayIndex 1096＋C13 未做唔開", rBs && rBs.ok === false);
}

if(fails.length){ console.error("FAILURES: " + fails.join(" | ")); process.exit(1); }
console.log("ALL PASS (gate136 logic)");
