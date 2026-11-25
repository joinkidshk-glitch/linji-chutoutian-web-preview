// v404 意圖更新：確認閘刪除（用戶拍板）——改驗「撳掣即執行＋掣名講明後果」，presentStartScheduleConfirm45 已刪唔再載入。
// v396 resync：afterDayRes／afterDayModal／休息卡靠 dayResDateLine396 等三 helper 出日結日期行，沙盒一併抽入；見 qa396/resync396.py。
// v392：dayEndDismissNote202 已刪＋(f)(g) dismiss 斷言改做 v392 契約（非週結 null／確認返休息卡／確認金掣「開始並結算當日」）。
// v20a45 流程確認（A 方案）邏輯／路徑測試：日結休息卡「開始今日行程」確認閘。
// 行真路徑：抽真 presentRestSleepDayEnd＋真 dayEndContinueButtons＋真 presentStartScheduleConfirm45，
// 以 stub modal／排程入口驗證——確認只出喺休息卡延續入口、開始先至行程、
// 返回地圖／關閉唔推日、冇旗標（legacy）唔加確認、ended 回家結算唔經確認、
// 確認文案按今日計劃（休息／自動／已排定）講明後果。
// 用法：node tests/test_flow45_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) throw new Error('fn not found: '+name);
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){
    if(html[j]==='{') depth++;
    else if(html[j]==='}'){ depth--; if(depth===0) break; }
  }
  return html.slice(i, j+1);
}

/* ---- stubs（只 stub 邊界：modal／排程入口／DOM；被測函數全部係真碼） ---- */
let S = { dayIndex: 1 };
let PLAN_NOW = 'rest';
let modalCalls = [];
let schedCalls = 0, mapCalls = 0, homeCalls = 0, onSchedCalls = 0;
function reset(){
  modalCalls = []; schedCalls = 0; mapCalls = 0; homeCalls = 0; onSchedCalls = 0;
  S = { dayIndex: 1 };
}
function modal(htmlArg, btns, opts){ modalCalls.push({ html: htmlArg, btns: btns || [], opts: opts || {} }); return true; }
function todayPlanId(){ return PLAN_NOW; }
function isMapDay(id){ return !!id && (id==='scout_all'||id==='scout_nt'||id==='scout_kln'||id==='scout_island'); }
function planLabel(id){ return ({ rest:'休息', street:'街頭表演', cafe_gig:'茶餐廳小唱' })[id] || String(id); }
function fmtDate(){ return '1988年3月8日（二）· 第1週'; }
function runScheduleFromToday(){ schedCalls++; }
function goToMapForBrowse(){ mapCalls++; }
function enterHome(){ homeCalls++; }
function syncDateChrome(){}
function paintBar(){}
function drawMap(){}
function saveQ(){}
function armRestSleepFxInModal(){}
function stopRestSleepFxInModal(){}
function restSleepFxHtml(){ return ''; }
function formatRestSleepDeltas(){ return ''; }
const document = {
  body: { classList: { add(){}, remove(){}, contains(){ return false; } } },
  getElementById(){ return { classList: { add(){}, remove(){}, contains(){ return false; } } }; }
};

/* ---- 真碼入作用域 ---- */
eval(extractFn('nextDayIsMap')); /* v20a196 D7：dayEndContinueButtons／休息卡／確認 modal 而家靠佢判定逛逛日 */
eval(extractFn('esc202')); /* v20a202：presentStartScheduleConfirm45／presentRestSleepDayEnd 而家靠呢啲 helper 出去向行＋dismiss 提示 */
eval(extractFn('nextDayLabel202'));
eval(extractFn('dayEndNextLine202'));
/* v392：dayEndDismissNote202 已刪（v392 ① 廢止 dismiss 提示機制），唔再載入。 */
eval(extractFn('storyResultDestLine202'));
eval(extractFn('dayEndContinueButtons'));
eval(extractFn('presentRestSleepDayEnd'));
/* v396：afterDayModal／afterDayRes／休息卡靠呢三個 helper 出日結日期行 */
eval(extractFn('settledDateObj396'));
eval(extractFn('fmtShortDate396'));
eval(extractFn('dayResDateLine396'));

function press(call, substr){
  const b = (call.btns || []).find(x => String(x.label || '').indexOf(substr) >= 0);
  if(!b) throw new Error('button not found: ' + substr + ' in ' + (call.btns || []).map(x => x.label).join(','));
  b.on();
  return b;
}
function lastModal(){ return modalCalls[modalCalls.length - 1]; }

/* ---- A（v404）：休息日 —— 撳「休息並過日」即執行，冇確認 modal ---- */
(function(){
  reset(); PLAN_NOW = 'rest';
  presentRestSleepDayEnd({ title:'休息（週一）', notes:[], ended:false, summary:null });
  ok('A card shown once', modalCalls.length === 1);
  ok('A rest-day button names consequence', lastModal().btns.some(x => String(x.label || '') === '休息並過日'));
  press(lastModal(), '休息並過日');
  ok('A press runs schedule immediately, no confirm modal', schedCalls === 1 && modalCalls.length === 1 && mapCalls === 0);
})();

/* ---- B（v404）：自動行程 —— 撳「執行今日行程」即執行 ---- */
(function(){
  reset(); PLAN_NOW = 'street';
  presentRestSleepDayEnd({ title:'休息', notes:[], ended:false, summary:null,
    onSchedule: ()=>{ onSchedCalls++; },
    onMap: ()=>{ mapCalls++; } });
  ok('B auto-plan button names consequence', lastModal().btns.some(x => String(x.label || '') === '執行今日行程'));
  press(lastModal(), '執行今日行程');
  ok('B press runs onSchedule continuation directly', onSchedCalls === 1 && schedCalls === 0 && modalCalls.length === 1);
})();

/* ---- C（v404）：拍攝日 —— 掣名「開始拍攝」，撳即執行 ---- */
(function(){
  reset(); PLAN_NOW = 'shoot:demo1';
  presentRestSleepDayEnd({ title:'休息', notes:[], ended:false, summary:null });
  ok('C shoot-day button names consequence', lastModal().btns.some(x => String(x.label || '') === '開始拍攝'));
  press(lastModal(), '開始拍攝');
  ok('C press runs schedule immediately', schedCalls === 1 && modalCalls.length === 1);
})();

/* ---- D（v404）：逛逛日 —— 「返回地圖」照舊，唔行程 ---- */
(function(){
  reset(); PLAN_NOW = 'scout_all';
  presentRestSleepDayEnd({ title:'休息', notes:[], ended:false, summary:null });
  press(lastModal(), '返回地圖');
  ok('D map day returns to map only', mapCalls === 1 && schedCalls === 0 && modalCalls.length === 1);
})();

/* ---- E：ended（週結）—— 「回家結算」直行 ---- */
(function(){
  reset(); PLAN_NOW = 'rest';
  presentRestSleepDayEnd({ title:'休息', notes:[], ended:true, summary:{} });
  press(lastModal(), '回家結算');
  ok('E ended goes home directly', homeCalls === 1 && modalCalls.length === 1 && schedCalls === 0);
})();

console.log(fails.length ? ('\nFAILURES: '+fails.length+' -> '+fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
