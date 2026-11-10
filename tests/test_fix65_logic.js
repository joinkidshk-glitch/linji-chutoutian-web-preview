/* v20a65 FIX65 修復包 — 邏輯測試（抽 index.html 真函數喺沙盒行）：
   (1) FIX65-1 用戶拍板規則：全日休息（排程 rest／doRest）delta = −S.stress → 休息後壓力 == 0
       （抽真表達式行）；入水維持原值（拍攝日 10–14）；部分休息保留。
   (2) FIX65-2 生活費首年緩坡：wk2/8/20/35 mid = 1100/1300/1500/1700；wk44+ full 2400；
       CALIB60 加幅保留（1989 wk50 = 2700、1990 wk100 = 3000）。
   (3) FIX65-2 寬限入帳解除：grace 中、本週入帳 ≥ 下週費、結算後存款 >0 → 解除（舊版 2 參數呼叫唔解除）；
       入帳唔夠 → 照倒數；存款夠全費 → 舊路徑解除（兩版都得）。
   (4) FIX65-3 跨媒介補分：多元 fixture（唱片桶＋電影擔正＋電視作品）→ borrow65 = 0.55×0.35×crossQ、
       repPower65 = 0.08×crossQ、base 高過冇補分；專攻 fixture（得電影）→ borrow/repPower 皆 0（曲線唔變）。
   (5) FIX65-4 提示認級數：代表作 = MTV 男主角（gig_1989_mtv_01 真身形狀）→ 唔出「缺擔正」句、出深度句；
       代表作係臨記 → 照出「缺擔正」；主軌最弱 → 指主軌（舊 parts 形狀 topQ 兜底唔崩）。
   反證：對 v20a64 index 行——壓力舊值／舊生活費帶／冇 weekEarnIn 解除／冇 borrow65 欄位／冇 awards65IsLeadWork → FAIL。
   用法：node tests/test_fix65_logic.js [path-to-index.html] */
const fs = require("fs");
const path = require("path");
const file = process.argv[2] || "index.html";
const src = fs.readFileSync(path.resolve(file), "utf8");
let pass = 0, fail = 0;
function ok(cond, msg){ if(cond){ pass++; } else { fail++; console.error("  ✗ FAIL:", msg); } }
function approx(a, b, eps){ return Math.abs(a - b) <= (eps || 0.001); }

function extractFn(name){
  const sig = "function " + name + "(";
  let i = src.indexOf(sig);
  if(i < 0) throw new Error("fn not found: " + name);
  let j = src.indexOf("{", i), depth = 0, k = j;
  for(; k < src.length; k++){
    if(src[k] === "{") depth++;
    else if(src[k] === "}"){ depth--; if(depth === 0) break; }
  }
  return src.slice(i, k + 1);
}
function extractConst(name){
  const sig = "const " + name + " =";
  let i = src.indexOf(sig);
  if(i < 0) throw new Error("const not found: " + name);
  let j = src.indexOf("=", i), depth = 0, k = j + 1, started = false;
  for(; k < src.length; k++){
    const ch = src[k];
    if(ch === "{" || ch === "[" || ch === "("){ depth++; started = true; }
    else if(ch === "}" || ch === "]" || ch === ")"){ depth--; }
    else if(ch === ";" && depth === 0) break;
  }
  return src.slice(i, k + 1);
}

/* ---------- 沙盒 stub ---------- */
var window = {};
var S = null;
var START = { y: 1988, m: 3, d: 7 };
let R_MODE = "min";
function R(a, b){ if(R_MODE === "min") return a; if(R_MODE === "max") return b; return Math.round((a + b) / 2); }
function clamp(v, a, b){ return Math.max(a, Math.min(b, v)); }
let SOFT = false;
function softPreviewOn(){ return SOFT; }
function calib60YearOfWeek(w){
  const dt = new Date(START.y, START.m - 1, START.d + (Number(w) - 1) * 7);
  return dt.getFullYear();
}
function livingCostEstimate(w){ return livingCostBand(w).mid; }
function endingDual410(st){ return { stageVolume: Number(st.fame) || 0, industryCredit: Number(st.industryCredit) || 0 }; }
function shootRemain(sh){ return (sh.totalDays || 0) - (sh.doneDays || 0); }

/* ---------- (1) FIX65-1 用戶拍板規則（2026-11-10）：全日休息＝壓力清零；入水大致原值 ---------- */
/* 行為斷言：抽出兩條全日休息路徑嘅真 delta 表達式，用遊戲 apply 語義（clamp 0..100）行——
   休息前 77/63 → 休息後必須 == 0。反證：v64 係 -(18+R(0,8)) / -(14+R(0,8))，永遠唔到零。 */
eval(extractFn("stressDeltaForAct"));
eval(extractFn("clamp"));
function restDeltaAfter(expr, before) {
  const S = { stress: before };
  const delta = eval(expr);
  return Math.max(0, Math.min(100, S.stress + delta));
}
const mPlan = (() => {
  const key = 'id==="rest"){ notes=apply({stress:';
  const i = src.indexOf(key);
  if (i < 0) return null;
  const j = src.indexOf('})', i + key.length);
  return [null, src.slice(i + key.length, j)];
})();
ok(!!mPlan, "排程休息 delta 表達式抽到");
if (mPlan) ok(restDeltaAfter(mPlan[1], 77) === 0, "排程全日休息：壓力 77 → 0（清零）");
const doIdx = src.indexOf("function doRest(");
const mDo = doIdx < 0 ? null : src.slice(doIdx, doIdx + 400).match(/apply\(\{stress:(.+?)\}\)/);
ok(!!mDo, "doRest delta 表達式抽到");
if (mDo) ok(restDeltaAfter(mDo[1], 63) === 0, "doRest 全日休息：壓力 63 → 0（清零）");
eval(extractFn("shootDailyDelta"));
{
  let mn = 1e9, mx = -1;
  for (let i = 0; i < 300; i++) { const d = shootDailyDelta({}, {}); mn = Math.min(mn, d.stress); mx = Math.max(mx, d.stress); }
  ok(mn >= 10 && mx <= 14, "拍攝日入水維持原值 10..14（實測 " + mn + ".." + mx + "）");
}
ok(stressDeltaForAct("rest") === -100, "預覽：rest = −100（清零標示）");
ok(stressDeltaForAct("train_acting") === 10 && stressDeltaForAct("shoot:gig_x") === 10, "預覽入水維持原值（train/shoot = 10）");
ok(src.includes("stress:-(4+R(0,4))"), "部分休息（提早返屋企）−(4+R(0,4)) 保留");
ok(src.includes("stress:-(6+R(0,4))"), "部分休息（家務）−(6+R(0,4)) 保留");

/* ---------- (2) FIX65-2 生活費緩坡 ---------- */
eval(extractFn("livingCostWeekNum"));
eval(extractFn("livingCostBand"));
S = { fame: 0 };
ok(livingCostBand(2).mid === 1100, "wk2 生活費 mid 1100（舊 1600）");
ok(livingCostBand(8).mid === 1300, "wk8 生活費 mid 1300（舊 soft 1900／LIVE 2400）");
ok(livingCostBand(20).mid === 1500, "wk20 生活費 mid 1500（舊 2400）");
ok(livingCostBand(35).mid === 1700, "wk35 生活費 mid 1700（舊 2400）");
ok(livingCostBand(44).mid === 2700, "wk44 已入 1989：full 帶 2400＋年份加幅 300 = 2700（後期規則冇郁）");
ok(livingCostBand(50).mid === 2700, "1989 wk50 = 2400+300（CALIB60 加幅保留）");
ok(livingCostBand(100).mid === 3000, "1990 wk100 = 2400+600（CALIB60 加幅保留）");
SOFT = true;
ok(livingCostBand(8).mid === 1300 && livingCostBand(35).mid === 1700, "soft 預覽同 LIVE 同一緩坡");
SOFT = false;

/* ---------- (3) FIX65-2 寬限入帳解除 ---------- */
eval(extractConst("CONSEQ61_REVIEWS").replace("const CONSEQ61_REVIEWS =", "var CONSEQ61_REVIEWS ="));
eval(extractConst("CONSEQ61_CFG").replace("const CONSEQ61_CFG =", "var CONSEQ61_CFG ="));
eval(extractFn("conseq61State"));
eval(extractFn("conseq61DualOf"));
eval(extractFn("conseq61SettleEval"));
function graceSave(money, weeksLeft){
  return { money: money, fame: 30, industryCredit: 20, shoots: [],
           conseq61: { reviews: {}, streak80: 0, streak90: 0, peak90: 0, cooldownUntil: 0,
                       grace: { weeksLeft: weeksLeft, startedWeek: 9 }, sick: null, pendingEnding: null } };
}
/* 入帳解除：存款 $300（< 全費 1500）、本週入帳 $2000 ≥ 1500、存款 >0 → 解除 */
let g = graceSave(300, 3);
let lines = conseq61SettleEval(g, 10, 2000);
ok(g.conseq61.grace === null && lines.join("").indexOf("寬限警報解除") >= 0,
   "寬限入帳解除：入帳 $2000 ≥ 下週費 $1500 ＋ 存款 $300 >0 → 解除（舊版冇呢條路）");
/* 反例：入帳唔夠 → 照倒數 */
g = graceSave(300, 3);
lines = conseq61SettleEval(g, 10, 1000);
ok(g.conseq61.grace && g.conseq61.grace.weeksLeft === 2, "入帳 $1000 < 1500 → 唔解除、倒數 3→2");
/* 反例：入帳夠但存款 = 0（冇返正數）→ 唔解除 */
g = graceSave(0, 3);
lines = conseq61SettleEval(g, 10, 2000);
ok(g.conseq61.grace && g.conseq61.grace.weeksLeft === 2, "入帳夠但結算後存款 $0 → 唔解除（防即入即出）");
/* 舊路徑：存款夠全費 → 解除 */
g = graceSave(2000, 3);
lines = conseq61SettleEval(g, 10, 0);
ok(g.conseq61.grace === null, "存款 $2000 ≥ 全費 → 舊路徑照解除");
/* 冇傳第三參數（舊呼叫形狀）→ 唔好崩、唔好誤解除 */
g = graceSave(300, 3);
lines = conseq61SettleEval(g, 10);
ok(g.conseq61.grace && g.conseq61.grace.weeksLeft === 2, "冇 weekEarnIn → 行舊邏輯倒數（唔崩）");

/* ---------- (4) FIX65-3 跨媒介補分 ---------- */
for(const c of ["AWARDS62_WIN_LINE", "AWARDS62_TASTE", "AWARDS62_ROLE_Q"])
  eval(extractConst(c).replace("const " + c + " =", "var " + c + " ="));
const GIGMAP = {
  g_film_lead: { id: "g_film_lead", roleScale: "film_lead_big", stars: 5, pay: [30000, 50000], type: "電影" },
  g_album1: { id: "g_album1", roleScale: "rec_album", stars: 4, pay: [8000, 12000], type: "唱片通告" },
  g_album2: { id: "g_album2", roleScale: "rec_album", stars: 3, pay: [6000, 9000], type: "唱片通告" },
  g_tv_sup: { id: "g_tv_sup", roleScale: "tv_support_main", stars: 3, pay: [5000, 8000], type: "電視劇" },
  g_extra: { id: "g_extra", roleScale: "film_extra_day", stars: 1, pay: [300, 500], type: "電影" }
};
function work59GigLookup(id){ return GIGMAP[id] || null; }
function work59WorkOf(h, g){ return (g && g.id) || (h && h.gigId) || ""; }
function ensureCastingTagsState(){ return []; }
function awardsDual(){ return { stageVolume: S.fame || 0, industryCredit: S.industryCredit || 0 }; }
eval(extractFn("awards62WorkQuality"));
eval(extractFn("awards62YearOf"));
eval(extractFn("awards62YearWorks"));
eval(extractFn("awards62ScoreParts"));
function wrap(gigId, year){ const g = GIGMAP[gigId]; return { gigId: gigId, type: g.type, year: year, pay: g.pay[1], wrappedDay: 100 }; }
const MUSIC_CER = { id: "award_golddisc_music", medium: "music", matchTypes: ["唱片通告"] };
const FILM_CER = { id: "award_harbour_film", medium: "film", matchTypes: ["電影"] };
const CAT_MU = { id: "cat_x", primaryTrack: "stageVolume", tagBonusAny: [] };
S = { fame: 60, industryCredit: 60, wrapHistory: [wrap("g_album1", 1989), wrap("g_album2", 1989), wrap("g_film_lead", 1989), wrap("g_tv_sup", 1989)] };
const pMu = awards62ScoreParts(CAT_MU, MUSIC_CER, 1989);
ok(approx(pMu.borrow65, 0.55 * 0.35 * 1.0, 0.0001), "借分 borrow65 = 0.55×0.35×crossQ(1.0)（實得 " + pMu.borrow65 + "）");
ok(approx(pMu.repPower65, 0.08, 0.0001), "跨桶星勢 repPower65 = 0.08×crossQ（桶外 2 部、crossQ ≥ 0.5）");
const pMuNoCross = (()=>{ const keep = S.wrapHistory; S.wrapHistory = [wrap("g_album1", 1989), wrap("g_album2", 1989)];
  const r = awards62ScoreParts(CAT_MU, MUSIC_CER, 1989); S.wrapHistory = keep; return r; })();
ok(pMu.base > pMuNoCross.base + 0.05, "多元 base（" + pMu.base.toFixed(3) + "）高過冇跨桶（" + pMuNoCross.base.toFixed(3) + "）至少 0.05");
/* 專攻：得電影作品 → 電影桶 crossQ = 0、借分/星勢皆 0 */
S = { fame: 60, industryCredit: 60, wrapHistory: [wrap("g_film_lead", 1989), wrap("g_extra", 1989)] };
const pFilm = awards62ScoreParts(CAT_MU, FILM_CER, 1989);
ok(pFilm.borrow65 === 0 && pFilm.repPower65 === 0, "專攻 fixture：borrow/repPower = 0（專攻曲線唔變）");
/* 本桶空 → 唔借（唔憑空造分） */
S = { fame: 60, industryCredit: 60, wrapHistory: [wrap("g_film_lead", 1989), wrap("g_tv_sup", 1989)] };
const pEmpty = awards62ScoreParts(CAT_MU, MUSIC_CER, 1989);
ok(pEmpty.borrow65 === 0 && pEmpty.worksScore === 0, "本桶冇作品 → borrow = 0");

/* ---------- (5) FIX65-4 提示認級數 ---------- */
eval(extractConst("AWARDS65_LEAD_SCALES").replace("const AWARDS65_LEAD_SCALES =", "var AWARDS65_LEAD_SCALES ="));
eval(extractFn("awards65IsLeadWork"));
eval(extractFn("awards62WeakHint"));
const mtvRep = { h: { gigId: "gig_1989_mtv_01" }, g: { id: "gig_1989_mtv_01", roleScale: "mtv", roleLabel: "" }, q: 0.48, title: "樂隊「夜渡」快歌 MTV 男主角" };
ok(awards65IsLeadWork(mtvRep) === true, "MTV 男主角（roleScale=mtv、靠作品名）判擔正");
ok(awards65IsLeadWork({ h: {}, g: { roleScale: "film_lead_big", roleLabel: "" }, q: 1, title: "大製作" }) === true, "film_lead_big 判擔正");
ok(awards65IsLeadWork({ h: {}, g: { roleScale: "mtv", roleLabel: "拍板／遞水助手" }, q: 0.48, title: "《錄音室》拍板助手" }) === false, "幕後拍板助手（同樣 mtv）唔判擔正");
const hintLead = awards62WeakHint({ primaryTrack: "stageVolume", normPrimary: 1, worksScore: 0.57, worksCount: 3, topQ: 0.48, rep: mtvRep }, CAT_MU);
ok(hintLead.indexOf("缺一部擔正") < 0 && hintLead.indexOf("深度") >= 0,
   "擔正代表作 → 唔出「缺擔正」、出深度句（實得：" + hintLead + "）");
const extraRep = { h: {}, g: { roleScale: "film_extra_day", roleLabel: "臨時群演" }, q: 0.22, title: "街景臨記" };
const hintExtra = awards62WeakHint({ primaryTrack: "stageVolume", normPrimary: 1, worksScore: 0.2, worksCount: 3, topQ: 0.22, rep: extraRep }, CAT_MU);
ok(hintExtra.indexOf("缺一部擔正") >= 0, "臨記代表作 → 照出「缺擔正」（唔好矯枉過正）");
const hintPrim = awards62WeakHint({ topQ: 0.9, normPrimary: 0.2, worksCount: 5, primaryTrack: "industryCredit" }, CAT_MU);
ok(hintPrim.indexOf("業內信用") >= 0, "舊 parts 形狀（冇 worksScore）主軌最弱 → 指主軌（topQ 兜底唔崩）");

console.log("FIX65 LOGIC: " + pass + " pass, " + fail + " fail");
process.exit(fail ? 1 : 0);
