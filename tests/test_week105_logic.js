/* v20a105 WEEK105 週界狀態組 — 邏輯測試（抽 index.html 真函數喺沙盒行）：
   (1) S-12 週界落存檔＋防雙重扣錢：真 settleWeek 行一次 → 生活費只扣一次、
       weekBoundary105 旗寫入存檔（saveQ 快照）；模擬重載（JSON 還原＋normalize）
       → week105Pending 有效、金額不變；清旗（enterHome editable 語義）後旗失效；
       殘旗（日子已過週一）唔觸發。
   (2) S-13 計劃繼承剔已完成通告：scrubInherited105 將 wrap:/audition:/死 shoot:
       改返 scout_all，活 shoot:／一般日子保留；todayPlanId 見今日格係 wrap:
       即時改返自由日。
   (3) S-14 回顧記實際執行：recordExec105Day 合併同日多種（劇情＋試鏡）、
       提早休息獨立於全日休息；exec105MetaForDay 出實際名；nbRowMeta105 只對
       已過去日子生效；舊檔 normalize 補空欄唔炸、冇紀錄日子退返 null（用槽位）。
   反證：對 v20a104 index 行——冇 week105Pending／scrubInherited105／recordExec105Day
   等函數 → 抽取即 FAIL。
   用法：node tests/test_week105_logic.js [path-to-index.html] */
const fs = require("fs");
const path = require("path");
const file = process.argv[2] || "index.html";
const src = fs.readFileSync(path.resolve(file), "utf8");
let pass = 0, fail = 0;
function ok(cond, msg){ if(cond){ pass++; } else { fail++; console.error("  ✗ FAIL:", msg); } }

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
  let j = src.indexOf("=", i), depth = 0, k = j + 1;
  for(; k < src.length; k++){
    const ch = src[k];
    if(ch === "{" || ch === "[" || ch === "(") depth++;
    else if(ch === "}" || ch === "]" || ch === ")") depth--;
    else if(ch === ";" && depth === 0) break;
  }
  return src.slice(i, k + 1);
}

/* ---------- 沙盒 stub ---------- */
var window = {};
var S = null;
const STRESS_MAX = 100;
let STORE = null; /* saveQ 快照（模擬 localStorage） */
function saveQ(){ STORE = JSON.stringify(S); }
function clamp(v, a, b){ return Math.max(a, Math.min(b, v)); }
function R(a, b){ return a; }
function softPreviewOn(){ return false; }
function calib60YearOfWeek(w){ return 1990; }
function syncDualTracks(st){ return { stageVolume: Number(st && st.fame) || 0, industryCredit: 10 }; }
function refreshMoneyHud(){}
function eventLine(){ return ""; }
function statHardMax(){ return 999; }

eval(extractConst("STAT_LABEL").replace(/^const STAT_LABEL/, "var STAT_LABEL"));
eval(extractConst("EXEC105_KINDS").replace(/^const EXEC105_KINDS/, "var EXEC105_KINDS"));
eval(extractFn("weekdayIdx"));
eval(extractFn("weekNumNow"));
eval(extractFn("apply"));
eval(extractFn("stripSettleMoneyNoise"));
eval(extractFn("livingCostWeekNum"));
eval(extractFn("livingCostBand"));
eval(extractFn("livingCostRoll"));
eval(extractFn("settleWeek"));
eval(extractFn("week105Pending"));
eval(extractFn("scrubInherited105"));
eval(extractFn("recordExec105Day"));
eval(extractFn("exec105KindForSlot"));
eval(extractFn("exec105MetaForDay"));
eval(extractFn("nbShowingPrevWeek37"));
eval(extractFn("nbPlanMondayAbs105"));
eval(extractFn("nbRowMeta105"));
eval(extractFn("todayPlanId"));
eval(extractFn("normalizeSaveObj"));

/* ---------- (1) S-12：真 settleWeek 只扣一次＋旗落存檔＋重載唔重扣 ---------- */
S = {
  dayIndex: 7, /* 已翻到第 2 週週一，settleWeek 計 w=1 */
  money: 13898, weekEarn: 1882, stress: 10, stamina: 75, fame: 7, popularity: 3,
  flags: {}, weekGigsDone: 1, weekTrainDone: 0, shoots: [], booked: [],
  weekPlan: ["scout_all","rest","scout_all","scout_all","street","cafe_gig","rest"],
  giftMeta: { lastGiveDay:{}, weekGiftGain:{}, givenCount:{}, shopStock:{}, shopWeek: 0 },
};
const sum = settleWeek();
ok(S.money === 12798, "settleWeek 生活費 $1,100 只扣一次：13898 → 12798（實得 " + S.money + "）");
ok(sum && sum.weekNum === 1 && /1,100/.test(sum.html), "結算 summary 含生活費 $1,100");
ok(S.weekBoundary105 && S.weekBoundary105.week === 1, "WEEK105 旗已寫入 S（week=1）");
ok(S.weekBoundary105 && S.weekBoundary105.html === sum.html, "旗存低嘅 html 同結算 summary 一致");
ok(STORE && JSON.parse(STORE).weekBoundary105, "旗已隨 saveQ 落存檔快照");
/* 模擬重載：JSON 還原＋normalize（舊路徑 contFromSlot 嘅載入語義） */
const moneyBeforeReload = S.money;
S = normalizeSaveObj(JSON.parse(STORE));
const pend = week105Pending();
ok(!!pend && pend.week === 1, "重載後 week105Pending 有效 → 會強制返結算/編排步");
ok(S.money === moneyBeforeReload, "重載後金額不變（冇靜默再結算）："+ S.money);
/* 補呈現只讀 html：重複讀旗唔掂金額 */
week105Pending(); week105Pending();
ok(S.money === moneyBeforeReload, "重複讀旗唔扣錢（補呈現係唯讀）");
/* 入編排步清旗（enterHome editable 語義）→ 旗失效，之後重開唔再觸發 */
S.weekBoundary105 = null;
ok(week105Pending() === null, "清旗後 week105Pending 失效");
/* 殘旗：日子已行過週一（dayIndex 唔係 week*7）→ 唔觸發 */
S.weekBoundary105 = { week: 1, day: 7, html: "x" };
S.dayIndex = 9;
ok(week105Pending() === null, "殘旗（已過週一）唔誤觸發");
/* 舊檔：冇旗 → 唔觸發、唔炸 */
S = normalizeSaveObj({ dayIndex: 7, money: 5000 });
ok(week105Pending() === null, "舊檔冇旗 → 唔強制返結算步");
ok(S.execLog105 && typeof S.execLog105 === "object", "舊檔 normalize 補 execLog105 空欄");

/* ---------- (2) S-13：繼承剔已完成通告 ---------- */
S = { dayIndex: 9, shoots: [{ id: "sh_live" }], booked: [], flags: {},
      weekPlan: ["wrap:《賀歲特輯》拜年群演","audition:gig_x","shoot:sh_live","shoot:sh_dead","rest","scout_all","street"] };
const scrubbed = scrubInherited105(S.weekPlan);
ok(scrubbed[0] === "scout_all", "wrap: 已殺青標記被剔走 → scout_all");
ok(scrubbed[1] === "scout_all", "audition: 已耗標記被剔走 → scout_all");
ok(scrubbed[2] === "shoot:sh_live", "仍然存在嘅 shoot: 保留");
ok(scrubbed[3] === "scout_all", "已唔存在嘅 shoot: 被剔走 → scout_all");
ok(scrubbed[4] === "rest" && scrubbed[5] === "scout_all" && scrubbed[6] === "street", "一般日子原樣保留");
/* todayPlanId：今日格係 wrap: → 即時改返自由日兼回寫 */
S.weekPlan = ["scout_all","rest","wrap:《賀歲特輯》拜年群演","scout_all","street","cafe_gig","rest"];
ok(todayPlanId() === "scout_all", "今日格 wrap: → todayPlanId 回 scout_all（嗰日有正常入口）");
ok(S.weekPlan[2] === "scout_all", "今日格已回寫 scout_all");
S.weekPlan[2] = "shoot:sh_live";
ok(todayPlanId() === "shoot:sh_live", "今日格活 shoot: 照常回傳");

/* ---------- (3) S-14：回顧記實際執行 ---------- */
S = { dayIndex: 0, shoots: [], booked: [], flags: {}, execLog105: {} };
recordExec105Day("story", "C1");
recordExec105Day("audition", "《賀歲特輯》拜年群演");
const m0 = exec105MetaForDay(0);
ok(!!m0 && m0.name.indexOf("劇情") >= 0 && m0.name.indexOf("試鏡") >= 0,
   "同一日劇情＋試鏡合併顯示（實得：" + (m0 && m0.name) + "）");
ok(!!m0 && m0.name.indexOf("休息") < 0, "嗰日唔再顯示做休息（槽位頂替已除）");
S.dayIndex = 3;
recordExec105Day("browse");
recordExec105Day("early_rest");
const m3 = exec105MetaForDay(3);
ok(!!m3 && m3.name.indexOf("提早休息") >= 0 && m3.name.indexOf("到處逛逛") >= 0,
   "逛逛＋提早休息：兩樣都記低（實得：" + (m3 && m3.name) + "）");
ok(!!m3 && m3.name !== "休息睡覺", "提早休息唔等於全日休息睡覺");
/* nbRowMeta105：已過去日子用紀錄；今日／未來用排程（回 null）；冇紀錄回 null 退槽位 */
S.dayIndex = 10; S.weekPlanWeek37 = 1; /* 而家第 2 週、plan 係上週（週一絕對日 = 0） */
ok(nbPlanMondayAbs105() === 0, "上週 plan 週一絕對日 = 0");
const row0 = nbRowMeta105(0, false);
ok(!!row0 && row0.name.indexOf("試鏡") >= 0, "回顧第 1 週週一出實際紀錄（試鏡）而唔係槽位");
ok(nbRowMeta105(10, false) === null, "今日（未過去）唔用紀錄頂替排程");
ok(nbRowMeta105(1, false) === null, "冇紀錄嘅過去日子回 null（渲染退返槽位標籤，舊檔唔炸）");
ok(nbRowMeta105(0, true) === null, "編輯模式唔用紀錄（排緊新一週）");
/* 槽位兜底映射 */
ok(exec105KindForSlot("scout_all") === "browse" && exec105KindForSlot("rest") === "rest"
   && exec105KindForSlot("job:g1") === "audition" && exec105KindForSlot("wrap:X") === "wrap"
   && exec105KindForSlot("train_acting") === "train", "exec105KindForSlot 兜底映射正確");

console.log("week105_logic: pass=" + pass + " fail=" + fail);
process.exit(fail ? 1 : 0);
