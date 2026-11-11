/* v20a96 LOC96 地點整理 — 核心邏輯回歸測試
   抽 index.html 真函數喺受控沙盒行：
   (1) 禮物店正規化：shop_street_mk 由 rec_hk 搬去 gift_shop、改名；shopId 不變、冪等
   (2) 體檢：hosp96State 防禦初始化；生效期內 conseq61DailyTick 用有效壓力（−10）計連續日
       ——95 連兩日唔病、100 連兩日照病（唔係無敵）、過期後回復本體；冇體檢時行為同 v95 一致
   (3) 付費治療 gate：出選擇 modal；揀醫扣 $600＋今日變最後一日（resolve 行康復路徑）；
       揀唞唔扣錢照病；最後一日／已醫／週加速／冇病唔接管；唔夠錢出資訊版 modal
   (4) 探病：病程第一日按最高好感出探病旁白＋好感 +2；第二日唔再出；全 0 好感出芬姐版
   (5) 醫院 sheet：體檢購買扣錢＋寫 checkupUntil；生效中出「生效中」掣；唔夠錢擋；非醫院唔出掣
   用法：node tests/test_loc96_logic.js [path-to-index.html]（對 v20a95 index 行會 FAIL＝反證） */
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
    const ch = src[k];
    if(ch === "{") depth++;
    else if(ch === "}"){ depth--; if(depth === 0) break; }
  }
  return src.slice(i, k + 1);
}
function bindConst(name){
  const code = (()=>{ const sig = "const " + name + " ="; let i = src.indexOf(sig);
    if(i < 0) throw new Error("const not found: " + name);
    let j = src.indexOf("=", i), depth = 0, k = j + 1;
    for(; k < src.length; k++){ const ch = src[k];
      if(ch === "{" || ch === "[" || ch === "(") depth++;
      else if(ch === "}" || ch === "]" || ch === ")") depth--;
      else if(ch === ";" && depth === 0) break; }
    return src.slice(i, k + 1); })();
  const expr = code.replace(new RegExp("^(const|let|var)\\s+" + name + "\\s*=\\s*"), "").replace(/;\s*$/, "");
  return eval("(" + expr + ")");
}

/* ---------- 沙盒 stub ---------- */
var S = null;
var GIFT_SHOPS = { version: "0", shops: [] };
var _weekAccel = false;
var modalCalls = [];
var afterDayCalls = [];
var toastCalls = [];
function modal(html, btns, opts){ modalCalls.push({ html: String(html || ""), btns: btns || [], opts: opts || {} }); }
function afterDayModal(html, title, L, ended, summary, opts){ afterDayCalls.push({ html: String(html || ""), title: title, ended: !!ended }); }
function toast(t){ toastCalls.push(String(t || "")); }
function tickDay(){ return { ended: false, summary: null }; }
function saveQ(){}
function paintBar(){}
function fmtDate(){ return "1990年1月10日"; }
function formatResultNotes(notes){ return (notes || []).join("\n"); }
function weekdayIdx(d){ return ((Number(d) || 0) % 7 + 7) % 7; }
function isMapDay(){ return false; }
function apply(delta){
  for(const k of Object.keys(delta || {})){
    const v = Number(delta[k]) || 0;
    if(k === "stress") S.stress = Math.max(0, Math.min(100, (Number(S.stress) || 0) + v));
    else if(k === "money") S.money = (Number(S.money) || 0) + v;
    else if(typeof S[k] === "number") S[k] += v;
  }
  return [];
}
function bumpNpc(id, d){ S.npcs = S.npcs || {}; S.npcs[id] = Math.max(0, Math.min(100, (Number(S.npcs[id]) || 0) + d)); }

const LOC96_CFG = bindConst("LOC96_CFG");
const CONSEQ61_CFG = bindConst("CONSEQ61_CFG");
eval(extractFn("conseq61State"));
eval(extractFn("conseq61DailyTick"));
eval(extractFn("conseq61IsSickDay"));
eval(extractFn("conseq61IsSickToday"));
eval(extractFn("conseq61ResolveSickDay"));
eval(extractFn("hosp96State"));
eval(extractFn("loc96RemapGiftShop"));
eval(extractFn("hosp96CheckupActive"));
eval(extractFn("hosp96EffStress"));
eval(extractFn("hosp96TreatGate"));
eval(extractFn("hosp96VisitNote"));
eval(extractFn("loc96AddSheetActs"));

function baseSave(){
  return { dayIndex: 10, stress: 10, money: 5000, shoots: [], booked: [], npcs: {},
    weekPlan: ["rest","rest","rest","rest","rest","rest","rest"], industryCreditDelta: 0 };
}
function mkSick(s, from, to, extra){
  s.conseq61 = { reviews: {}, streak90: 0, streak80: 0, peak90: 0, cooldownUntil: 0, grace: null,
    sick: Object.assign({ from: from, to: to, days: to - from + 1, creditLost: 0, done: {}, peak: 95, streak: 2 }, extra || {}),
    pendingEnding: null };
  return s;
}

/* ---------- (1) 禮物店正規化 ---------- */
console.log("[1] 禮物店搬遷正規化");
GIFT_SHOPS = { shops: [
  { shopId: "shop_street_mk", locId: "rec_hk", name: "旺角街頭檔／樓上小賣", stock: [{ itemId: "gift_thermos", count: 2 }] },
  { shopId: "shop_other", locId: "cafe_cha", name: "其他" },
]};
loc96RemapGiftShop();
ok(GIFT_SHOPS.shops[0].locId === "gift_shop", "shop_street_mk locId 搬去 gift_shop");
ok(GIFT_SHOPS.shops[0].name === "廟街禮品檔", "店名改做廟街禮品檔");
ok(GIFT_SHOPS.shops[0].shopId === "shop_street_mk", "shopId 不變（舊檔 shopStock 相容）");
ok(GIFT_SHOPS.shops[1].locId === "cafe_cha", "其他 shop 冇被誤傷");
loc96RemapGiftShop();
ok(GIFT_SHOPS.shops[0].locId === "gift_shop", "正規化冪等");

/* ---------- (2) 體檢＋病倒判定 ---------- */
console.log("[2] 體檢有效壓力");
S = baseSave();
ok(hosp96State(S) && S.hosp96.checkupUntil === 0, "hosp96 防禦初始化");
ok(hosp96EffStress(S, 95) === 95, "冇體檢：有效壓力＝原壓力");
S.hosp96.checkupUntil = 10 + LOC96_CFG.checkupDays;
ok(hosp96CheckupActive(S) === true, "體檢生效中");
ok(hosp96EffStress(S, 95) === 85, "體檢生效：95 → 85");
ok(hosp96EffStress(S, 5) === 0, "體檢生效：唔減穿 0");
S.dayIndex = 10 + LOC96_CFG.checkupDays;
ok(hosp96CheckupActive(S) === false, "到 checkupUntil 當日即過期");
ok(hosp96EffStress(S, 95) === 95, "過期後回復原壓力");

function tickN(s, days){
  for(let i = 0; i < days; i++){ s.dayIndex++; conseq61DailyTick(); }
}
/* 冇體檢：95 連兩日 → 病（同 v95 本體一致） */
S = baseSave(); S.stress = 95;
tickN(S, 2);
ok(!!(S.conseq61 && S.conseq61.sick), "冇體檢：收市 95 連兩日照病倒（本體不變）");
/* 有體檢：95 → 有效 85，連三日都唔病（但警號 streak80 照計） */
S = baseSave(); S.stress = 95; S.hosp96 = { checkupUntil: 99 };
tickN(S, 3);
ok(!(S.conseq61 && S.conseq61.sick), "有體檢：收市 95（有效 85）連三日唔病倒");
ok(S.conseq61.streak80 >= 2, "有體檢：85 過警號線，streak80 照計（警號唔會被吞）");
/* 有體檢：100 → 有效 90，連兩日照病（唔係無敵） */
S = baseSave(); S.stress = 100; S.hosp96 = { checkupUntil: 99 };
tickN(S, 2);
ok(!!(S.conseq61 && S.conseq61.sick), "有體檢：收市 100（有效 90）連兩日照病倒");

/* ---------- (3) 付費治療 gate ---------- */
console.log("[3] 治療選擇 gate");
/* 冇病：唔接管 */
S = baseSave(); modalCalls = [];
ok(hosp96TreatGate("rest") === false && modalCalls.length === 0, "冇病：gate 唔接管");
/* 病程最後一日：唔接管 */
S = mkSick(baseSave(), 10, 10); modalCalls = [];
ok(hosp96TreatGate("rest") === false && modalCalls.length === 0, "最後一日：gate 唔接管（唞埋就好）");
/* 週加速：唔接管 */
S = mkSick(baseSave(), 10, 12); modalCalls = []; _weekAccel = true;
ok(hosp96TreatGate("rest") === false && modalCalls.length === 0, "週加速：gate 唔彈窗");
_weekAccel = false;
/* 已醫過：唔接管 */
S = mkSick(baseSave(), 10, 12, { hosp96Treated: true }); modalCalls = [];
ok(hosp96TreatGate("rest") === false && modalCalls.length === 0, "已醫過：gate 唔再接管");
/* 揀醫：扣 $600、今日變最後一日、行康復路徑 */
S = mkSick(baseSave(), 10, 12); S.stress = 88; modalCalls = []; afterDayCalls = [];
ok(hosp96TreatGate("rest") === true && modalCalls.length === 1, "病程中：gate 接管出選擇");
ok(modalCalls[0].btns.length === 2, "選擇有兩個掣（醫／唞）");
modalCalls[0].btns[0].on();
ok(S.money === 5000 - LOC96_CFG.treatFee, "揀醫：扣 $600");
ok(S.conseq61.sick === null, "揀醫：今日結算後病程完結（聽日好返）");
ok(S.conseq61.cooldownUntil > 10, "揀醫：照入病癒冷卻");
ok(afterDayCalls.length === 1 && afterDayCalls[0].title.indexOf("病倒休養") === 0, "揀醫：照出行程結算卡");
/* 揀唞：唔扣錢、今日照病假、病程未完 */
S = mkSick(baseSave(), 10, 12); modalCalls = []; afterDayCalls = [];
hosp96TreatGate("rest");
modalCalls[0].btns[1].on();
ok(S.money === 5000, "揀唞：冇扣錢");
ok(!!S.conseq61.sick && S.conseq61.sick.done[10] === true, "揀唞：今日照結算做病假");
ok(afterDayCalls.length === 1, "揀唞：照出結算卡");
/* dismiss（撳外面）：照結算，唔扣錢 */
S = mkSick(baseSave(), 10, 12); modalCalls = []; afterDayCalls = [];
hosp96TreatGate("rest");
modalCalls[0].opts.onDismiss();
ok(S.money === 5000 && !!S.conseq61.sick && S.conseq61.sick.done[10] === true, "dismiss：照病假結算、冇扣錢");
/* 唔夠錢：資訊版 modal（一個掣），撳完照結算 */
S = mkSick(baseSave(), 10, 12); S.money = 100; modalCalls = []; afterDayCalls = [];
ok(hosp96TreatGate("rest") === true && modalCalls.length === 1, "唔夠錢：gate 照接管出資訊版");
ok(modalCalls[0].btns.length === 1 && modalCalls[0].html.indexOf("唔夠畀") >= 0, "唔夠錢：文案講明醫唔起");
modalCalls[0].btns[0].on();
ok(S.money === 100 && S.conseq61.sick.done[10] === true, "唔夠錢：照病假結算、冇扣錢");

/* ---------- (4) 探病 ---------- */
console.log("[4] 探病場景");
S = mkSick(baseSave(), 10, 11); S.npcs = { colleague: 50, agent: 10, stylist: 0 };
afterDayCalls = [];
conseq61ResolveSickDay("rest");
ok(afterDayCalls.length === 1 && afterDayCalls[0].html.indexOf("林曉晴") >= 0 && afterDayCalls[0].html.indexOf("白粥") >= 0, "第一日：曉晴（最高好感）嚟探＋白粥場景");
ok(S.npcs.colleague === 52, "探病：曉晴好感 +2");
S.dayIndex = 11; afterDayCalls = [];
conseq61ResolveSickDay("rest");
ok(afterDayCalls.length === 1 && afterDayCalls[0].html.indexOf("白粥") < 0, "第二日：唔再重複探病");
/* 何生最高 */
S = mkSick(baseSave(), 10, 11); S.npcs = { colleague: 5, agent: 60, stylist: 20 };
afterDayCalls = [];
conseq61ResolveSickDay("rest");
ok(afterDayCalls[0].html.indexOf("何生上門探病") >= 0 && S.npcs.agent === 62, "何生最高：何生探病＋好感 +2");
/* 全 0：芬姐版 */
S = mkSick(baseSave(), 10, 11); S.npcs = {};
afterDayCalls = [];
conseq61ResolveSickDay("rest");
/* v20a100 CLEAN100 B-10：茶水檔嗰位已分名做「珍姐」（同副導演芬姐係兩個人，用戶拍板）→ 斷言跟住改 */
ok(afterDayCalls[0].html.indexOf("珍姐") >= 0 && afterDayCalls[0].html.indexOf("糖水") >= 0 && afterDayCalls[0].html.indexOf("芬姐") < 0, "冇人熟：珍姐送糖水（純文案）");
/* hosp96VisitNote 直接呼叫：dayNo≠1 唔出 */
S = mkSick(baseSave(), 10, 12);
ok(hosp96VisitNote(2) === null, "visitNote：第二日回 null");

/* ---------- (5) 醫院 sheet 體檢購買 ---------- */
console.log("[5] 醫院 sheet");
function sheetRun(locId){
  const adds = [];
  loc96AddSheetActs((title, hint, cost, on, cls)=>adds.push({ title, hint, cost, on, cls }), { id: locId });
  return adds;
}
S = baseSave(); S.money = 1000; toastCalls = [];
let adds = sheetRun("hospital");
ok(adds.length === 1 && adds[0].title === "身體檢查", "健康時：出身體檢查掣");
adds[0].on();
ok(S.money === 1000 - LOC96_CFG.checkupFee, "買體檢：扣 $500");
ok(S.hosp96.checkupUntil === 10 + LOC96_CFG.checkupDays, "買體檢：checkupUntil＝今日＋28");
adds = sheetRun("hospital");
ok(adds.length === 1 && adds[0].title.indexOf("生效中") >= 0, "生效中：出「生效中」掣、唔重複賣");
S = baseSave(); S.money = 100;
adds = sheetRun("hospital");
adds[0].on();
ok(S.money === 100 && !(S.hosp96 && S.hosp96.checkupUntil > 0), "唔夠錢：買唔到體檢、冇扣錢");
ok(sheetRun("cafe_cha").length === 0 && sheetRun("gift_shop").length === 0, "非醫院地點：唔出醫院掣");

console.log(`\nLOC96 logic: ${pass} pass, ${fail} fail`);
process.exit(fail ? 1 : 0);
