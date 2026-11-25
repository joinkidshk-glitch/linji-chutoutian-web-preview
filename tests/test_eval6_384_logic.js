// v20a384 第六輪評估 P2 收尾・邏輯測試
// 合約：
//   A 補位截止日：intel381DeadlineText 只喺 kept＋同 gigId 出「覆電後 7 日」日期，否則空。
//   B 自費短截止：tape383DeadlineShortText 出「M月D日截止」，同 A 同閘。
//   C 雙拍攝爭位：lockShootsIntoDraft 按 deadlineDay 升序填位，近限期先得位。
//   D 壓力 draft：v20a400 預設唔再因壓力靜靜換休息——「現壓力／預覽峰值取高」計法
//     保留喺 weekStressPeak400，改由手帳建議列出掣；高壓週預設照舊得一日休息。
// 反證：v383 index 冇 intel381DeadlineText／tape383DeadlineShortText → 抽取即 throw → FAIL。
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
function extractFn(name){
  const i = html.indexOf('function ' + name + '(');
  if (i < 0) throw new Error('fn not found: ' + name);
  let depth = 0, j = html.indexOf('{', i);
  for (; j < html.length; j++){ if (html[j] === '{') depth++; else if (html[j] === '}'){ depth--; if (depth === 0) break; } }
  return html.slice(i, j + 1);
}
let fails = 0;
function ok(name, cond, extra){
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : ''));
  if (!cond) fails++;
}

/* ---------- 沙盒 ---------- */
const START = { y: 1990, m: 1, d: 1 };
var S = { dayIndex: 100, money: 10000, flags: {}, shoots: [], intel381: null, tape383: null, stress: 0, enrolled: {}, trainCount: {}, mockDebts: [] };
var clamp = function(v,a,b){ return Math.max(a, Math.min(b, v)); };
var planMeta = function(id){ return { name: String(id||"") }; };
var weekdayName = function(i){ return "一二三四五六日"[i] || ""; };
var saveQ = function(){};
var toast = function(){};
var triggerGigLocName229 = function(id){ return String(id || ""); };
var weekNumNow = function(){ return Math.floor((S.dayIndex|0)/7)+1; };
var scrubStaleJobs = function(d){ return d; };
var shootRemain = function(sh){ return Math.max(0,(sh.totalDays||0)-(sh.doneDays||0)); };
var shootWeekdayOk = function(){ return true; };
var TRAIN75_SPEC = { train_acting:{main:"acting",sLo:10,sSpan:0}, train_vocal:{main:"vocal",sLo:10,sSpan:0}, train_stage:{main:"stage",sLo:10,sSpan:0}, train_looks:{main:"looks",sLo:7,sSpan:0}, train_charm:{main:"charm",sLo:6,sSpan:0}, train_iq:{main:"iq",sLo:5,sSpan:0}, train_stamina:{main:"stamina",sLo:10,sSpan:0} };
var levels75Level = function(){ return 1; };
S.acting=20; S.vocal=20; S.stage=20; S.looks=20; S.charm=20; S.iq=20; S.stamina=20;

eval(extractFn('intel381Slot'));
eval(extractFn('intel381KeptGig'));
eval(extractFn('intel381FmtDay'));
eval(extractFn('intel381DeadlineText'));
eval(extractFn('tape383Slot'));
eval(extractFn('tape383KeptGig'));
eval(extractFn('tape383DeadlineShortText'));
eval(extractFn('lockShootsIntoDraft'));
eval(extractFn('stressDeltaForAct'));
eval(extractFn('previewWeekStress'));
eval(extractFn('defaultWeekPlan'));

/* A：補位截止日 */
S.intel381 = { state:"kept", gigId:"g1", keptDay:100 };
ok('A1 kept 同 gig 出日期', intel381DeadlineText({id:"g1"}) === intel381FmtDay(107), intel381DeadlineText({id:"g1"}));
ok('A2 唔同 gig 空', intel381DeadlineText({id:"g2"}) === "");
S.intel381 = { state:"msg", gigId:"g1", keptDay:100 };
ok('A3 未覆電空', intel381DeadlineText({id:"g1"}) === "");

/* B：自費短截止 */
S.tape383 = { state:"kept", gigId:"g9", keptDay:100 };
const shortB = tape383DeadlineShortText({id:"g9"});
ok('B1 短格式', /^\d{1,2}月\d{1,2}日截止$/.test(shortB), shortB);
ok('B2 唔同 gig 空', tape383DeadlineShortText({id:"g1"}) === "");

/* C：雙拍攝爭位——近限期（剩 1 日、deadlineDay 細）先填，唔畀後入長拍攝搶晒 */
S.shoots = [
  { id:"long", totalDays:6, doneDays:0, deadlineDay:130 },
  { id:"tail", totalDays:1, doneDays:0, deadlineDay:102 },
];
const draftC = lockShootsIntoDraft(["scout_all","scout_all","scout_all","scout_all","scout_all","scout_all","scout_all"]);
ok('C1 尾日拍攝有位', draftC.includes("shoot:tail"), draftC.join(","));
ok('C2 長拍攝填其餘', draftC.filter(x=>x==="shoot:long").length === 6, draftC.join(","));

/* D：壓力 draft——v20a400：預設唔再因壓力靜靜換休息。現壓力 79（未跨 80），成週活動推峰值
   跨 80 → 舊制三日休息；v400 預設照舊得一日休息（plan[6]），壓力建議改由手帳建議列出
   （峰值計法保留喺 weekStressPeak400，見 test_v400_logic.js）。 */
S.stress = 79; S.dayIndex = 112; /* week 17 */
const planD = defaultWeekPlan();
ok('D1 v400 高壓預設唔靜靜加休息（得 plan[6] 一日）', planD.filter(x=>x==="rest").length === 1 && planD[1]==="scout_all", planD.join(","));
S.stress = 30;
S.shoots = []; /* v20a386：峰值預覽已計入已 lock 拍攝，C 段留低嘅 shoots 會推峰值——D2 驗嘅係低壓無拍攝負荷，清走先測 */
const planD2 = defaultWeekPlan();
ok('D2 低壓維持一至兩日休息', planD2.filter(x=>x==="rest").length <= 2, planD2.join(","));

console.log(fails ? ('TOTAL FAIL ' + fails) : 'TOTAL PASS');
process.exit(fails ? 1 : 0);
