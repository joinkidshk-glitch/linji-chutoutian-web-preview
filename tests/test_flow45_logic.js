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
eval(extractFn('dayEndDismissNote202'));
eval(extractFn('storyResultDestLine202'));
eval(extractFn('dayEndContinueButtons'));
eval(extractFn('presentStartScheduleConfirm45'));
eval(extractFn('presentRestSleepDayEnd'));

function press(call, substr){
  const b = (call.btns || []).find(x => String(x.label || '').indexOf(substr) >= 0);
  if(!b) throw new Error('button not found: ' + substr + ' in ' + (call.btns || []).map(x => x.label).join(','));
  b.on();
  return b;
}
function lastModal(){ return modalCalls[modalCalls.length - 1]; }

/* ---- A：旗標開＋預設路徑＋今日休息 —— 卡撳開始 → 先確認，唔即刻行程 ---- */
(function(){
  reset(); PLAN_NOW = 'rest';
  presentRestSleepDayEnd({ title:'休息（週一）', notes:[], ended:false, summary:null, confirmStartSchedule:true });
  ok('A card shown once', modalCalls.length === 1);
  press(lastModal(), '開始今日');
  ok('A confirm modal appears before schedule', modalCalls.length === 2);
  ok('A schedule NOT started yet', schedCalls === 0 && mapCalls === 0);
  ok('A dayIndex untouched by confirm', S.dayIndex === 1);
  const c = lastModal();
  ok('A confirm copy has date', c.html.indexOf('1988年3月8日（二）') >= 0);
  ok('A confirm copy warns instant settle for rest', c.html.indexOf('即時結算埋今日') >= 0 && c.html.indexOf('休息') >= 0);
  press(c, '開始今日');
  ok('A confirm-start runs schedule exactly once', schedCalls === 1 && mapCalls === 0);
})();

/* ---- B（v196 改）：旗標開＋排程下一日（rest）—— 確認冇「返回地圖」，dismiss＝開始行程，唔推日 ---- */
(function(){
  reset(); PLAN_NOW = 'rest';
  presentRestSleepDayEnd({ title:'休息（週一）', notes:[], ended:false, summary:null, confirmStartSchedule:true });
  press(lastModal(), '開始今日');
  const c = lastModal();
  ok('B v196 scheduled next day: confirm has no 返回地圖', !c.btns.some(x => String(x.label || '').indexOf('返回地圖') >= 0));
  if(typeof c.opts.onDismiss === 'function') c.opts.onDismiss();
  ok('B2 v196 dismiss starts schedule, never maps', schedCalls === 1 && mapCalls === 0 && S.dayIndex === 1);
})();

/* ---- C：冇旗標（legacy playRestSleepFx 路徑）—— 開始即行程，冇確認 ---- */
(function(){
  reset(); PLAN_NOW = 'rest';
  presentRestSleepDayEnd({ title:'休息', notes:[], ended:false, summary:null });
  press(lastModal(), '開始今日');
  ok('C no-flag starts schedule immediately, no confirm modal', schedCalls === 1 && modalCalls.length === 1);
})();

/* ---- D：旗標開＋計劃休息卡（onSchedule 延續）—— 確認後行 onSchedule ---- */
(function(){
  reset(); PLAN_NOW = 'street';
  presentRestSleepDayEnd({ title:'休息', notes:[], ended:false, summary:null,
    confirmStartSchedule:true,
    onSchedule: ()=>{ onSchedCalls++; },
    onMap: ()=>{ mapCalls++; } });
  press(lastModal(), '開始今日');
  ok('D confirm appears for planned-rest card too', modalCalls.length === 2 && onSchedCalls === 0 && schedCalls === 0);
  press(lastModal(), '開始今日');
  ok('D confirm-start runs onSchedule continuation', onSchedCalls === 1 && schedCalls === 0);
})();

/* ---- E：ended（週結）＋旗標 —— 「回家結算」唔經確認 ---- */
(function(){
  reset(); PLAN_NOW = 'rest';
  presentRestSleepDayEnd({ title:'休息', notes:[], ended:true, summary:{}, confirmStartSchedule:true });
  press(lastModal(), '回家結算');
  ok('E ended goes home directly, no confirm modal', homeCalls === 1 && modalCalls.length === 1 && schedCalls === 0);
})();

/* ---- F／G：確認文案按計劃類型（直接行真 confirm 函數） ---- */
(function(){
  reset(); PLAN_NOW = 'street';
  let started = 0, mapped = 0;
  presentStartScheduleConfirm45(()=>{ started++; }, ()=>{ mapped++; });
  const c = lastModal();
  ok('F auto-plan copy names plan + instant settle', c.html.indexOf('街頭表演') >= 0 && c.html.indexOf('自動行程') >= 0 && c.html.indexOf('即時結算埋今日') >= 0);
  ok('F v196 scheduled next day: confirm has no 返回地圖', !c.btns.some(x => String(x.label || '').indexOf('返回地圖') >= 0));
  // 返地圖路徑改行逛逛日（scout_all）驗：確認照出兩粒掣，取消只返地圖
  reset(); PLAN_NOW = 'scout_all';
  presentStartScheduleConfirm45(()=>{ started++; }, ()=>{ mapped++; });
  const cm = lastModal();
  ok('F map next day: confirm still has 返回地圖', cm.btns.some(x => String(x.label || '').indexOf('返回地圖') >= 0));
  press(cm, '返回地圖');
  ok('F cancel callback only maps', mapped === 1 && started === 0 && S.dayIndex === 1);

  reset(); PLAN_NOW = 'shoot:demo1';
  presentStartScheduleConfirm45(()=>{ started++; }, ()=>{ mapped++; });
  const c2 = lastModal();
  ok('G forced-plan copy says proceeds directly, no instant-settle warning', c2.html.indexOf('直接進行') >= 0 && c2.html.indexOf('即時結算埋今日') < 0);
})();

console.log(fails.length ? ('\nFAILURES: '+fails.length+' -> '+fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
