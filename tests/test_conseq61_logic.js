/* v20a61 CONSEQ61 後果包 — 核心邏輯回歸測試
   抽 index.html 真函數喺受控沙盒行：
   (1) 年終評核地板推導鎖：hea 弧 dual 15/31 捉到、慢弧 70/183 有明顯餘裕；邊界週 43/95 同真日曆年份對齊
   (2) 評核流程：警告先行（dist 4–1 週）→ 邊界週先判收場；慢熱弧兩個評核點都過
   (3) 破產寬限：money≤0 起 4 週寬限、拍攝中暫停倒數、翻上水解除、用盡收場
   (4) 舊檔安全：normalizeSaveObj 靜靜標記已過評核，永不追溯
   (5) 呈現：conseq61PresentForcedEnding 寫 S.ending410（E7／variant／earlyEnd）、E7 唔入 resolveEnding410 判定表
   (6) 病倒：連續 2 日收市 ≥90 觸發、長度跟峰值、冷卻唔連鎖、警告 streak80
   (7) 告假日結算：限期順延、信用 −2/日封頂 6、病癒 −35 壓力、計劃格改寫 sick61、試鏡取消返板
   用法：node tests/test_conseq61_logic.js [path-to-index.html] */
const fs = require("fs");
const path = require("path");
const file = process.argv[2] || "index.html";
const src = fs.readFileSync(path.resolve(file), "utf8");
let pass = 0, fail = 0;
function ok(cond, msg){ if(cond){ pass++; } else { fail++; console.error("  ✗ FAIL:", msg); } }

function extractFn(name){
  const sig = "function " + name + "(";
  let i = src.indexOf(sig);
  if(i < 0){ i = src.indexOf("async function " + name + "("); if(i>=0) i += 6; }
  if(i < 0) throw new Error("fn not found: " + name);
  let j = src.indexOf("{", i), depth = 0, k = j;
  for(; k < src.length; k++){
    const ch = src[k];
    if(ch === "{") depth++;
    else if(ch === "}"){ depth--; if(depth === 0) break; }
  }
  return src.slice(i, k + 1);
}
function extractConst(name){
  const sig = "const " + name + " =";
  let i = src.indexOf(sig);
  if(i < 0){ const sig2 = "let " + name + " ="; i = src.indexOf(sig2); if(i>=0) return src.slice(i, src.indexOf(";", i) + 1); throw new Error("const not found: " + name); }
  let j = src.indexOf("=", i), depth = 0, k = j + 1, started = false;
  for(; k < src.length; k++){
    const ch = src[k];
    if(ch === "{" || ch === "[" || ch === "("){ depth++; started = true; }
    else if(ch === "}" || ch === "]" || ch === ")"){ depth--; }
    else if(ch === ";" && depth === 0) break;
  }
  return src.slice(i, k + 1);
}

/* ---------- 沙盒世界 stub（UI 層用假身，只驗狀態變化） ---------- */
var window = { addEventListener(){}, };
var localStorage = { _d:{}, getItem(k){ return this._d[k] ?? null; }, setItem(k,v){ this._d[k]=String(v); }, removeItem(k){ delete this._d[k]; } };
var S = null;
var planDraft = null;
var _weekAccel = false;
var modalCalls = [];
var afterDayCalls = [];
var tickDayCalls = 0;
function softPreviewOn(){ return false; }
function modal(html, btns){ modalCalls.push({ html: String(html||""), btns: btns||[] }); }
function afterDayModal(html, title, L, ended, summary, opts){ afterDayCalls.push({ html: String(html||""), title: title, ended: !!ended }); }
function tickDay(){ tickDayCalls++; return { ended: false, summary: null }; }
function saveQ(){}
function paintBar(){}
function fmtDate(){ return "1990年3月7日"; }
function formatResultNotes(notes){ return (notes||[]).join("\n"); }
function apply(delta){ /* 精簡版主引擎：只驗 stress/money 變化，夾返壓力 0..100 */
  const notes = [];
  for(const k of Object.keys(delta||{})){
    const v = Number(delta[k])||0;
    if(k === "stress") S.stress = Math.max(0, Math.min(100, (Number(S.stress)||0) + v));
    else if(k === "money") S.money = (Number(S.money)||0) + v;
    else if(typeof S[k] === "number") S[k] += v;
  }
  return notes;
}
Math.random = () => 0;

/* const 經 eval 唔會漏入 module scope，要自己再 bind（跟 test_calib60_logic.js 慣例） */
function bindConst(name){
  const code = extractConst(name);
  const expr = code.replace(new RegExp("^(const|let|var)\\s+" + name + "\\s*=\\s*"), "").replace(/;\s*$/, "");
  return eval("(" + expr + ")");
}
const START = bindConst("START");
const STAT_MAX = bindConst("STAT_MAX");
const STRESS_MAX = bindConst("STRESS_MAX");
eval(extractFn("clamp"));
eval(extractFn("dualTrackNumbers"));
eval(extractFn("syncDualTracks"));
eval(extractFn("readDualTracks"));
eval(extractFn("weekNumNow"));
eval(extractFn("weekdayIdx"));
eval(extractFn("calib60YearOfWeek"));
eval(extractFn("livingCostWeekNum"));
eval(extractFn("livingCostBand"));
eval(extractFn("livingCostRoll"));
eval(extractFn("livingCostEstimate"));
eval(extractFn("isMapDay"));
eval(extractFn("shootRemain"));
eval(extractFn("clearJobFromPlans"));
/* 結局系統（呈現測試用真函數） */
const ENDING410_T = bindConst("ENDING410_T");
const ENDING_NEG_TAGS410 = bindConst("ENDING_NEG_TAGS410");
const ENDING410_BACKSTAGE_KEYS = bindConst("ENDING410_BACKSTAGE_KEYS");
const ENDING410_CAREER_NAMES = bindConst("ENDING410_CAREER_NAMES");
const ENDING410_ADJ_RUMOR = bindConst("ENDING410_ADJ_RUMOR");
const ENDING410_NPC_NAMES = bindConst("ENDING410_NPC_NAMES");
eval(extractFn("endingFlag410"));
eval(extractFn("endingDual410"));
eval(extractFn("endingNegTagCount410"));
eval(extractFn("endingBackstageTagCount410"));
eval(extractFn("endingFavor410"));
eval(extractFn("endingRomance410"));
eval(extractFn("endingE2Eligible410"));
eval(extractFn("endingE3Eligible410"));
eval(extractFn("endingBackstageClose410"));
eval(extractFn("resolveEnding410"));
eval(extractFn("endingEsc410"));
eval(extractFn("endingCareerScene410"));
eval(extractFn("endingRomanceScene410"));
eval(extractFn("endingExodusScene410"));
eval(extractFn("endingInserts410"));
eval(extractFn("endingSummaryHtml410"));
eval(extractFn("showEndingSummary410"));
/* 存檔正規化（舊檔安全） */
eval(extractFn("normalizeSaveObj"));
/* CONSEQ61 本體 */
const CONSEQ61_REVIEWS = bindConst("CONSEQ61_REVIEWS");
const CONSEQ61_CFG = bindConst("CONSEQ61_CFG");
eval(extractFn("conseq61State"));
eval(extractFn("conseq61DualOf"));
eval(extractFn("conseq61LegacyMark"));
eval(extractFn("conseq61SettleEval"));
eval(extractFn("conseq61ExodusWord"));
eval(extractFn("conseq61PresentForcedEnding"));
eval(extractFn("conseq61DailyTick"));
eval(extractFn("conseq61IsSickDay"));
eval(extractFn("conseq61IsSickToday"));
eval(extractFn("conseq61ResolveSickDay"));

function baseSave(){
  return {
    dayIndex: 0, stress: 12, money: 12000, fame: 5, stage: 14, acting: 18, vocal: 5, looks: 10,
    industryCreditDelta: 0, negTags: {}, castingTags: [], favorLedger: undefined,
    mockCredits: [], mockDebts: [], shoots: [], booked: [],
    weekPlan: ["scout_all","rest","scout_all","scout_all","street","cafe_gig","rest"],
    story: { done: {}, flags: {}, rel: {} }, npcs: {}, ending410: null
  };
}
function heaSave(){ return baseSave(); } /* 開局凍結值：fame5/stage14/acting18 → dual 15 */
function heaDriftSave(){ const s = baseSave(); s.fame = 12; s.stage = 20; s.acting = 24; s.industryCreditDelta = 2; return s; } /* dual 31 */
function mkDual(target){
  const s = baseSave(); s.fame = 20; s.stage = 20; s.acting = 20; s.stress = 10;
  const base = dualTrackNumbers(s);
  s.industryCreditDelta = target - (base.stageVolume + base.industryCredit);
  return s;
}
const FMT = n => Math.round(n * 1000) / 1000;

/* ---------- (1) 地板推導鎖 ---------- */
console.log("[1] 地板推導＋邊界週年份");
ok(calib60YearOfWeek(43) === 1990 && calib60YearOfWeek(44) === 1991, "wk43 係 1990 最後週結、wk44 入 1991");
ok(calib60YearOfWeek(95) === 1991 && calib60YearOfWeek(96) === 1992, "wk95 係 1991 最後週結、wk96 入 1992");
ok(CONSEQ61_REVIEWS[1990].floor === 45 && CONSEQ61_REVIEWS[1991].floor === 100, "地板 45／100");
ok(CONSEQ61_REVIEWS[1990].boundaryWeek === 43 && CONSEQ61_REVIEWS[1991].boundaryWeek === 95, "邊界週 43／95");
ok(conseq61DualOf(heaSave()).dual === 15, "hea 弧 dual=15（實際 " + JSON.stringify(conseq61DualOf(heaSave())) + "）");
ok(conseq61DualOf(heaDriftSave()).dual === 31, "hea+輕微漂移 dual=31（實際 " + JSON.stringify(conseq61DualOf(heaDriftSave())) + "）");
ok(15 < 45 && 31 < 45, "兩條 hea 弧都低過 1990 地板 → 會被捉");
ok(70 >= 45 * 1.5, "慢弧 wk43 dual 70 ≥ 地板×1.5（餘裕 1.56×）");
ok(183 >= 100 * 1.8, "慢弧 wk95 dual 183 ≥ 地板×1.8（餘裕 1.83×）");
ok(CONSEQ61_REVIEWS[1990].warnLine === 65 && CONSEQ61_REVIEWS[1991].warnLine === 130, "警告線 65／130（慢弧 70／183 都高過警告線少少）");

/* ---------- (2) 評核流程：警告先行 ---------- */
console.log("[2] 評核：警告先行＋邊界判場");
{
  S = heaSave();
  const w40 = conseq61SettleEval(S, 40);
  ok(w40.some(t => t.includes("評核") && t.includes("何生")) && !S.conseq61.pendingEnding, "wk40（距評核 3 週）何生警告先行，唔收場");
  const w42 = conseq61SettleEval(S, 42);
  ok(w42.some(t => t.includes("下週就係") && t.includes("評核")) && !S.conseq61.pendingEnding, "wk42（距評核 1 週）急版警告，仍未收場");
  const w43 = conseq61SettleEval(S, 43);
  ok(w43.some(t => t.includes("評核結果")), "wk43 評核出結果行");
  ok(S.conseq61.pendingEnding && S.conseq61.pendingEnding.kind === "review" && S.conseq61.pendingEnding.year === 1990, "wk43 邊界週先判收場 review/1990");
  ok(S.conseq61.reviews[1990] && S.conseq61.reviews[1990].passed === false && S.conseq61.reviews[1990].dual === 15, "評核記錄 fail＋dual 快照");
  const w44 = conseq61SettleEval(S, 44);
  ok(!S.conseq61.reviews[1991], "判咗之後唔再重複判（wk44 冇新評核）");
}
{
  S = mkDual(70);
  const w43 = conseq61SettleEval(S, 43);
  ok(S.conseq61.reviews[1990].passed === true && !S.conseq61.pendingEnding, "慢弧 dual 70 過 1990 評核");
  ok(w43.some(t => t.includes("續你約")), "過關有何生續約行");
  S = mkDual(183);
  conseq61SettleEval(S, 95);
  ok(S.conseq61.reviews[1991].passed === true && !S.conseq61.pendingEnding, "慢弧 dual 183 過 1991 評核");
}
{
  S = mkDual(50); /* 地板 45 同警告線 65 之間：警告照出、但過關 */
  const w42 = conseq61SettleEval(S, 42);
  ok(w42.some(t => t.includes("年尾評核")), "貼線弧（dual 50）評核前照有警告");
  conseq61SettleEval(S, 43);
  ok(S.conseq61.reviews[1990].passed === true && !S.conseq61.pendingEnding, "貼線弧過關唔誤殺");
  S = mkDual(70); /* 警告線以上：評核前唔出警告 */
  const w42b = conseq61SettleEval(S, 42);
  ok(!w42b.some(t => t.includes("年尾評核")), "慢弧 dual 70 高過警告線 65 → 唔出無謂警告");
}
{
  S = heaSave(); S.ending410 = { career: "E1" };
  conseq61SettleEval(S, 43);
  ok(!S.conseq61.pendingEnding && !S.conseq61.reviews[1990], "已收科存檔：評核全跳過");
}

/* ---------- (3) 破產寬限 ---------- */
console.log("[3] 破產寬限：起／倒數／暫停／解除／用盡");
{
  S = baseSave(); S.money = 0;
  const l1 = conseq61SettleEval(S, 20);
  ok(S.conseq61.grace && S.conseq61.grace.weeksLeft === 4 && !S.conseq61.pendingEnding, "money≤0 起寬限 4 週，唔即收");
  ok(l1.some(t => t.includes("寬限") && t.includes("4 週")), "起寬限有明示行");
  conseq61SettleEval(S, 21); ok(S.conseq61.grace.weeksLeft === 3, "倒數 3");
  conseq61SettleEval(S, 22); ok(S.conseq61.grace.weeksLeft === 2, "倒數 2");
  const l4 = conseq61SettleEval(S, 23);
  ok(S.conseq61.grace.weeksLeft === 1 && l4.some(t => t.includes("寬限期仲有 1 週")), "倒數 1＋最後通牒行");
  conseq61SettleEval(S, 24);
  ok(S.conseq61.pendingEnding && S.conseq61.pendingEnding.kind === "bankrupt" && !S.conseq61.grace, "寬限用盡 → 收場 bankrupt");
}
{
  S = baseSave(); S.money = 0;
  conseq61SettleEval(S, 20);
  S.money = 5000; /* ≥ 下週生活費估算（1990 帶 $2400） */
  const l = conseq61SettleEval(S, 21);
  ok(!S.conseq61.grace && !S.conseq61.pendingEnding && l.some(t => t.includes("解除")), "寬限內翻上水 → 解除警報，唔收場");
  S = baseSave(); S.money = 0;
  conseq61SettleEval(S, 20);
  S.money = 100; /* 返少少唔夠生活費：未解除，照倒數 */
  conseq61SettleEval(S, 21);
  ok(S.conseq61.grace && S.conseq61.grace.weeksLeft === 3, "有錢返但未過生活費線 → 未解除，倒數照行");
}
{
  S = baseSave(); S.money = 0;
  conseq61SettleEval(S, 20);
  S.shoots = [{ id: "s1", gigId: "g", totalDays: 5, doneDays: 1 }];
  const l = conseq61SettleEval(S, 21);
  ok(S.conseq61.grace.weeksLeft === 4 && l.some(t => t.includes("暫停倒數")), "有未完拍攝 → 倒數暫停（唔好拍緊戲收人場）");
  S.shoots = [];
  conseq61SettleEval(S, 22);
  ok(S.conseq61.grace.weeksLeft === 3, "拍完之後倒數恢復");
}
{
  S = baseSave(); S.money = 1;
  conseq61SettleEval(S, 20);
  ok(!S.conseq61.grace, "money>0 唔起寬限（觸發線係真・水底 ≤0）");
}

/* ---------- (4) 舊檔安全 ---------- */
console.log("[4] 舊檔：唔追溯收場");
{
  const old = baseSave(); old.dayIndex = 800; /* 1992 年中 */
  const n = normalizeSaveObj(old);
  ok(n.conseq61.reviews[1990].legacy === true && n.conseq61.reviews[1991].legacy === true, "1992 舊檔：兩個評核點靜靜標記已過");
  S = n;
  conseq61SettleEval(S, 115);
  ok(!S.conseq61.pendingEnding, "標記後週結唔會追溯判收場");
  const young = baseSave(); young.dayIndex = 100; /* 1990 年中 */
  const n2 = normalizeSaveObj(young);
  ok(!n2.conseq61.reviews[1990], "1990 年中檔：評核未到，唔標記");
  const ended = baseSave(); ended.dayIndex = 100; ended.ending410 = { career: "E0" };
  const n3 = normalizeSaveObj(ended);
  ok(n3.conseq61.reviews[1990].legacy === true && n3.conseq61.reviews[1991].legacy === true, "已收科檔：兩個評核點都標記");
}

/* ---------- (5) 呈現：強制收場寫 ending410 ---------- */
console.log("[5] 呈現：E7 寫入＋總結頁＋判定表紀律");
{
  S = heaSave(); modalCalls = [];
  conseq61SettleEval(S, 43);
  ok(conseq61PresentForcedEnding() === true, "present 成功");
  ok(S.ending410 && S.ending410.career === "E7" && S.ending410.careerVariant === "review1990", "ending410 寫 E7／review1990");
  ok(S.ending410.title.indexOf("未紅先收・") === 0 && S.ending410.eveKey === "forced_review", "稱號＋eveKey");
  ok(S.ending410.earlyEnd && S.ending410.earlyEnd.floor === 45 && S.ending410.earlyEnd.year === 1990, "earlyEnd 快照（地板／年份）");
  ok(modalCalls.length === 1 && modalCalls[0].html.includes("事務所評核") && modalCalls[0].html.includes("記數簿"), "事業場景第一頁（評核文案）");
  ok(conseq61PresentForcedEnding() === false, "冪等：第二次 present 唔重出");
  const sum = endingSummaryHtml410();
  ok(sum.includes("1990 年尾評核・提早收科・手帳總結"), "總結頁標題跟收場原因");
  ok(!sum.includes(">三年收科・手帳總結<") && sum.includes("唔係你揀嘅"), "唔扮三年收科＋講明唔係自願");
}
{
  S = baseSave(); S.money = 0; modalCalls = [];
  for(let w = 20; w <= 24; w++) conseq61SettleEval(S, w);
  ok(conseq61PresentForcedEnding() === true, "破產 present 成功");
  ok(S.ending410.careerVariant === "bankrupt" && S.ending410.eveKey === "forced_bankrupt", "bankrupt variant／eveKey");
  ok(modalCalls[0].html.includes("寬限期") && modalCalls[0].html.includes("荷包"), "破產事業場景文案");
  ok(endingCareerScene410({ career: "E7", careerVariant: "review1991" }).includes("兩年"), "1991 評核場景分開寫");
}
{
  ok(resolveEnding410(heaSave()).career !== "E7", "resolveEnding410 判定表冇 E7（hea 弧照舊判其他格）");
  const rich = mkDual(400); rich.fame = 300; rich.stage = 300; rich.acting = 300;
  ok(resolveEnding410(rich).career !== "E7", "高數值弧 resolveEnding410 都唔會出 E7");
  ok(ENDING410_CAREER_NAMES.E7 === "未紅先收", "E7 名冊＝未紅先收");
}

/* ---------- (6) 病倒觸發／警告／冷卻 ---------- */
console.log("[6] 病倒：觸發／長度／警告層／冷卻");
function tickAt(day, stress){ S.dayIndex = day; S.stress = stress; conseq61DailyTick(); }
{
  S = baseSave();
  tickAt(10, 95);
  ok(S.conseq61.streak90 === 1 && !S.conseq61.sick, "≥90 第一日：儲 streak，唔即病");
  tickAt(11, 95);
  ok(!!S.conseq61.sick && S.conseq61.sick.from === 11 && S.conseq61.sick.days === 2, "連續 2 日 ≥90 → 病 2 日（峰值 95）");
  ok(conseq61IsSickDay(S, 11) && conseq61IsSickDay(S, 12) && !conseq61IsSickDay(S, 13), "病窗 from..to");
  tickAt(11, 100);
  ok(S.conseq61.sick.from === 11 && S.conseq61.sick.days === 2, "病緊再 tick 唔疊病唔改窗");
}
{
  S = baseSave();
  tickAt(10, 100); tickAt(11, 100);
  ok(S.conseq61.sick.days === 3, "峰值 ≥99 → 病 3 日");
  S = baseSave();
  conseq61State(S).streak90 = 5;
  tickAt(10, 100);
  ok(S.conseq61.sick.days === 4, "長 streak＋峰值 100 → 封頂 4 日");
}
{
  S = baseSave();
  tickAt(10, 85); tickAt(11, 85);
  ok(S.conseq61.streak80 === 2 && !S.conseq61.sick, "≥80 連續 2 日：警告 streak80=2，未病");
  tickAt(12, 50);
  ok(S.conseq61.streak80 === 0 && S.conseq61.streak90 === 0, "壓力回落 → streak 清零");
}
{
  S = baseSave();
  const c = conseq61State(S); c.cooldownUntil = 30;
  tickAt(20, 100); tickAt(21, 100);
  ok(!S.conseq61.sick && S.conseq61.streak90 === 0, "冷卻期內 ≥90 唔儲唔病");
  tickAt(31, 100); tickAt(32, 100);
  ok(!!S.conseq61.sick, "冷卻過後先可以再病");
}

/* ---------- (7) 告假日結算 ---------- */
console.log("[7] 病日結算：告假／作廢／病癒／冷卻");
function sickSave(from, to, day){
  const s = baseSave();
  s.dayIndex = day; s.stress = 95;
  const c = conseq61State(s);
  c.sick = { from: from, to: to, days: to - from + 1, creditLost: 0, done: {}, peak: 95, streak: 2 };
  return s;
}
{
  S = sickSave(20, 21, 20); afterDayCalls = []; tickDayCalls = 0;
  const wd = weekdayIdx(20); S.weekPlan[wd] = "shoot:sh1";
  S.shoots = [{ id: "sh1", gigId: "g1", title: "測試戲", totalDays: 3, doneDays: 1, deadlineDay: 25 }];
  ok(conseq61ResolveSickDay("shoot:sh1") === true, "拍攝病日接管");
  ok(S.shoots[0].deadlineDay === 26, "告假：限期順延 +1 日（唔觸發逾期取消）");
  ok(S.shoots[0].doneDays === 1, "告假：嗰日唔計進度");
  ok(S.industryCreditDelta === -2 && S.conseq61.sick.creditLost === 2, "告假：信用 −2");
  ok(S.weekPlan[wd] === "sick61", "今日格改寫病假");
  ok(S.conseq61.sick && tickDayCalls === 1 && afterDayCalls.length === 1, "未到最後一日：病續＋出日結卡＋耗日");
  ok(conseq61ResolveSickDay("shoot:sh1") === false, "同一日唔重複結算");
  S = sickSave(20, 21, 21); S.weekPlan[weekdayIdx(21)] = "rest";
  ok(conseq61ResolveSickDay("rest") === true, "最後一日接管");
  ok(S.conseq61.sick === null && S.stress === 60, "病癒：壓力 95−35=60");
  ok(S.conseq61.cooldownUntil === 21 + 14, "病癒設 14 日冷卻");
}
{
  /* 一次病 4 日、4 日都係拍攝日：信用扣 2+2+2+0 封頂 6 */
  S = sickSave(30, 33, 30);
  S.shoots = [{ id: "sh2", gigId: "g2", title: "長戲", totalDays: 9, doneDays: 0, deadlineDay: 60 }];
  for(let d = 30; d <= 33; d++){ S.dayIndex = d; S.weekPlan[weekdayIdx(d)] = "shoot:sh2"; conseq61ResolveSickDay("shoot:sh2"); }
  ok(S.industryCreditDelta === -6, "告假信用全程封頂 −6（實際 " + S.industryCreditDelta + "）");
  ok(S.shoots[0].deadlineDay === 64, "4 日告假限期順延 4 日");
  ok(S.conseq61.sick === null, "第 4 日病癒收尾");
}
{
  S = sickSave(40, 41, 40);
  S.weekPlan[weekdayIdx(40)] = "job:g9"; S.weekPlan[(weekdayIdx(40) + 2) % 7] = "job:g9";
  S.booked = [{ gigId: "g9", title: "試鏡戲" }];
  ok(conseq61ResolveSickDay("job:g9") === true, "試鏡病日接管");
  ok(S.booked.length === 0 && !S.weekPlan.includes("job:g9"), "試鏡取消、通告返板（計劃清走）");
  ok(S.weekPlan[weekdayIdx(40)] === "sick61", "試鏡日格改寫病假（唔畀 clear 蓋走）");
  ok(S.industryCreditDelta === 0, "試鏡告假零罰");
}
{
  S = baseSave(); S.dayIndex = 50;
  ok(conseq61ResolveSickDay("street") === false, "冇病嗰日唔接管");
  S = sickSave(60, 61, 59);
  ok(conseq61ResolveSickDay("street") === false, "病窗外唔接管");
}

console.log(`\nconseq61 logic: PASS ${pass} / FAIL ${fail}`);
process.exit(fail ? 1 : 0);
