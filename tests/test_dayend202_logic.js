// v20a202 B1/B2/C1/C2・邏輯／真路徑測試
//   行真碼：nextDayLabel202／dayEndNextLine202／dayEndDismissNote202／
//   storyResultDestLine202／dayEndContinueButtons／afterDayModal／
//   presentStartScheduleConfirm45／presentRestSleepDayEnd；
//   modal 係 capture stub（唔經 DOM），C2 嘅 StoryPlay render 用靜態測試覆蓋
//   （render 喺 StoryPlay IIFE 入面，抽唔出嚟 eval）。
//   反證：對 pristine main（860e790）index 行 → nextDayLabel202 抽唔到，直接 throw → FAIL。
// 用法：node tests/test_dayend202_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }
function extractFn(name){
  const i = html.indexOf('function ' + name + '(');
  if(i < 0) throw new Error('fn not found: ' + name);
  let depth = 0, j = html.indexOf('{', i);
  for(; j < html.length; j++){
    if(html[j] === '{') depth++;
    else if(html[j] === '}'){ depth--; if(depth === 0) break; }
  }
  return html.slice(i, j + 1);
}

/* ---- module 層 stub ---- */
var S = { dayIndex: 1, weekPlan: [], shoots: [] };
var FREEPLAY_FW = {};
var modalCalls = [];
var schedCalls = 0, mapCalls = 0, homeCalls = 0, resolveCalls = [];
var capturedConts = [], chainOrder = [];
var presentedLinks = {};
function reset(){
  modalCalls = []; schedCalls = 0; mapCalls = 0; homeCalls = 0; resolveCalls = [];
  capturedConts = []; chainOrder = []; presentedLinks = {};
  S = { dayIndex: 1, weekPlan: [], shoots: [] };
  FREEPLAY_FW = {};
  _weekAccel = false; _weekAccelBuf = [];
}
function modal(htmlArg, btns, opts){ modalCalls.push({ html: htmlArg, btns: btns || [], opts: opts || {} }); return true; }
function fmtDate(){ return '1990年1月2日（二）'; }
function planLabel(id){
  return ({ rest:'休息睡覺', street:'街頭表演', train_acting:'演技課', sick61:'病假',
    'shoot:probe196w':'拍攝日：探測片', 'job:probe_gig':'探測通告' })[id] || String(id);
}
function syncDateChrome(){}
function paintBar(){}
function drawMap(){}
function saveQ(){}
function armRestSleepFxInModal(){}
function stopRestSleepFxInModal(){}
function restSleepFxHtml(){ return ''; }
function formatRestSleepDeltas(){ return ''; }
function livingCostDayEndHint(){ return ''; }
function actFx102Html(){ return ''; }
function armActFx102(){}
function takeShootDropNotes(){ return []; }
function storyOpenSnapshot(){ return { open: [], done: [], locked: [] }; }
function goToMapForBrowse(){ mapCalls++; }
function enterHome(){ homeCalls++; }
function runScheduleFromToday(){ schedCalls++; }
var _weekAccel = false, _weekAccelBuf = [];
var confirmWeekAccel = function(thenGo){ if(typeof thenGo === 'function') thenGo(); };
var document = {
  body: { classList: { add(){}, remove(){}, contains(){ return false; } } },
  getElementById(){ return { classList: { add(){}, remove(){}, contains(){ return false; } } }; }
};
function labels(btns){ return (btns || []).map(b => b.label); }
function findBtn(btns, sub){ return (btns || []).find(b => String(b.label || '').indexOf(sub) >= 0); }
function press(call, substr){
  const b = findBtn(call.btns, substr);
  if(!b) throw new Error('button not found: ' + substr + ' in [' + labels(call.btns).join(',') + ']');
  b.on();
  return b;
}
function lastModal(){ return modalCalls[modalCalls.length - 1]; }

/* ---- 真碼入作用域 ---- */
eval(extractFn('weekdayIdx'));
eval(extractFn('isMapDay'));
eval(extractFn('todayPlanId'));
eval(extractFn('nextDayIsMap'));
eval(extractFn('planDayWouldWrap'));
eval(extractFn('isCriticalPlanDay'));
eval(extractFn('countRemainingAutoDays'));
eval(extractFn('esc202'));
eval(extractFn('nextDayLabel202'));
eval(extractFn('dayEndNextLine202'));
eval(extractFn('dayEndDismissNote202'));
eval(extractFn('storyResultDestLine202'));
eval(extractFn('dayEndContinueButtons'));
eval(extractFn('afterDayModal'));
eval(extractFn('presentStartScheduleConfirm45'));
eval(extractFn('presentRestSleepDayEnd'));

/* ---- (a) nextDayLabel202：種類＋實名 ---- */
(function(){
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'street', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  let d = nextDayLabel202();
  ok('a street next day is schedule with real name', d.kind === 'schedule' && d.label === '街頭表演');
  S.weekPlan[1] = 'scout_all';
  d = nextDayLabel202();
  ok('a scout_all next day is map (到處逛逛)', d.kind === 'map' && d.label === '到處逛逛');
  S.weekPlan[1] = 'scout_nt';
  d = nextDayLabel202();
  ok('a scout_nt next day is map (唔用 raw id)', d.kind === 'map' && d.label === '到處逛逛');
  S.weekPlan[1] = 'rest';
  d = nextDayLabel202();
  ok('a rest next day is schedule labelled 休息', d.kind === 'schedule' && d.label === '休息');
  S.weekPlan[1] = 'sick61';
  d = nextDayLabel202();
  ok('a sick61 next day is schedule labelled 病假', d.kind === 'schedule' && d.label === '病假');
  S.weekPlan[1] = 'train_acting';
  d = nextDayLabel202();
  ok('a train next day is schedule with course name', d.kind === 'schedule' && d.label === '演技課');
  S.shoots = [{ id: 'probe196w', doneDays: 0, totalDays: 1 }];
  S.weekPlan[1] = 'shoot:probe196w';
  d = nextDayLabel202();
  ok('a shoot next day is schedule with shoot title', d.kind === 'schedule' && d.label === '拍攝日：探測片');
  S.weekPlan[1] = 'wrap:probe196w';
  d = nextDayLabel202();
  ok('a wrap: next day is map (歷史標記)', d.kind === 'map');
  S.weekPlan[1] = 'audition:probe_gig';
  d = nextDayLabel202();
  ok('a audition: next day is map (歷史標記)', d.kind === 'map');
  S.weekPlan[1] = null;
  d = nextDayLabel202();
  ok('a null next day is map', d.kind === 'map' && d.label === '到處逛逛');
})();

/* ---- (b) dayEndNextLine202 / dayEndDismissNote202：文案＋ended 邊界 ---- */
(function(){
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'street', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  ok('b schedule next line names the plan + 自動行程',
    dayEndNextLine202(false) === '<p class="dayend-next202">聽日：街頭表演（自動行程）</p>');
  let n = dayEndDismissNote202(false);
  ok('b schedule dismiss note says 繼續跑聽日行程', n.role === 'note' && n.label === '撳出面＝繼續跑聽日行程');
  S.weekPlan[1] = 'scout_all';
  ok('b map next line says 到處逛逛＋返地圖自由行',
    dayEndNextLine202(false) === '<p class="dayend-next202">聽日：到處逛逛（返地圖自由行）</p>');
  n = dayEndDismissNote202(false);
  ok('b map dismiss note says 返地圖', n.role === 'note' && n.label === '撳出面＝返地圖');
  ok('b ended: no next line', dayEndNextLine202(true) === '');
  n = dayEndDismissNote202(true);
  ok('b ended dismiss note says 回家結算', n.role === 'note' && n.label === '撳出面＝回家結算');
})();

/* ---- (c) storyResultDestLine202：slot peek（唔消費）＋今日 framing ---- */
(function(){
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'street', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  FREEPLAY_FW._story165AfterCont = 'schedule';
  ok('c slot schedule: dest line names today plan',
    storyResultDestLine202().indexOf('關閉之後：繼續跑今日行程「街頭表演」（自動行程）') >= 0);
  ok('c dest line is a peek (slot survives)', FREEPLAY_FW._story165AfterCont === 'schedule');
  FREEPLAY_FW._story165AfterCont = 'map';
  ok('c slot map: dest line says 返地圖',
    storyResultDestLine202().indexOf('關閉之後：返地圖（今日：到處逛逛）') >= 0);
  FREEPLAY_FW._story165AfterCont = null;
  ok('c no slot: dest line says 關閉返地圖',
    storyResultDestLine202().indexOf('關閉：返地圖') >= 0);
  S.weekPlan[1] = 'scout_all';
  FREEPLAY_FW._story165AfterCont = 'schedule';
  ok('c slot schedule but today is map: falls back to 返地圖',
    storyResultDestLine202().indexOf('關閉之後：返地圖（今日：到處逛逛）') >= 0);
})();

/* ---- (d) afterDayModal：去向行喺 <h3> 之後第一屏位＋note 喺掣列尾＋dismiss 行為唔變 ---- */
(function(){
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'street', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  afterDayModal('<p>RESULT-BODY</p>', '訓練', null, false, null, {});
  const m = lastModal();
  ok('d next line sits right after <h3> (before result body)',
    m.html.indexOf('dayend-next202') > 0 && m.html.indexOf('dayend-next202') < m.html.indexOf('RESULT-BODY'));
  ok('d next line text is the scheduled plan',
    m.html.indexOf('聽日：街頭表演（自動行程）') >= 0);
  const note = m.btns[m.btns.length - 1];
  ok('d dismiss note is last in button row (板底)',
    note && note.role === 'note' && note.label === '撳出面＝繼續跑聽日行程');
  ok('d note has no on() (唔可撳)', typeof note.on !== 'function');
  ok('d scheduled day still has no 返回地圖 button',
    !labels(m.btns).some(l => l.indexOf('返回地圖') >= 0));
  m.opts.onDismiss();
  ok('d dismiss still runs schedule (流程唔郁)', schedCalls === 1 && mapCalls === 0);
})();
(function(){
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  afterDayModal('<p>RESULT-BODY</p>', '訓練', null, false, null, {});
  const m = lastModal();
  ok('d map day: next line says 到處逛逛', m.html.indexOf('聽日：到處逛逛（返地圖自由行）') >= 0);
  ok('d map day: dismiss note says 返地圖',
    m.btns[m.btns.length - 1].label === '撳出面＝返地圖');
  m.opts.onDismiss();
  ok('d map day: dismiss still goes to map', mapCalls === 1 && schedCalls === 0);
})();
(function(){
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'street', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  afterDayModal('<p>RESULT-BODY</p>', '訓練', null, true, null, {});
  const m = lastModal();
  ok('d ended: no next line, dismiss note is 回家結算',
    m.html.indexOf('dayend-next202') < 0 && m.btns[m.btns.length - 1].label === '撳出面＝回家結算');
})();

/* ---- (e) 休息卡＋確認 modal：C1 取消返休息卡，dismiss 照跟 D1 ---- */
(function(){
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'street', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  presentRestSleepDayEnd({ title: '休息', notes: [], ended: false, summary: null, confirmStartSchedule: true });
  const card = lastModal();
  ok('e rest card has next line first (before body)',
    card.html.indexOf('dayend-next202') > 0 && card.html.indexOf('聽日：街頭表演（自動行程）') >= 0);
  ok('e rest card dismiss note is last',
    card.btns[card.btns.length - 1].label === '撳出面＝繼續跑聽日行程');
  press(card, '開始今日');
  ok('e start opens confirm (not schedule yet)', modalCalls.length === 2 && schedCalls === 0);
  const c = lastModal();
  ok('e confirm has 取消（返去休息卡） button',
    !!findBtn(c.btns, '取消（返去休息卡）'));
  ok('e confirm dismiss note says 撳出面＝開始今日行程',
    findBtn(c.btns, '撳出面＝開始今日行程') && findBtn(c.btns, '撳出面＝開始今日行程').role === 'note');
  press(c, '取消（返去休息卡）');
  ok('e cancel re-presents the rest card (same title, no schedule run)',
    modalCalls.length === 3 && lastModal().html.indexOf('<h3>休息</h3>') === 0 && schedCalls === 0 && mapCalls === 0);
  ok('e re-presented rest card still has next line + dismiss note',
    lastModal().html.indexOf('聽日：街頭表演（自動行程）') >= 0
    && lastModal().btns[lastModal().btns.length - 1].label === '撳出面＝繼續跑聽日行程');
  // 取消之後再入確認，dismiss 照跟 D1 繼續（唔係取消）
  press(lastModal(), '開始今日');
  lastModal().opts.onDismiss();
  ok('e confirm dismiss still starts schedule (D1 唔郁)', schedCalls === 1 && mapCalls === 0);
})();
(function(){
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  presentRestSleepDayEnd({ title: '休息', notes: [], ended: false, summary: null, confirmStartSchedule: true });
  const card = lastModal();
  ok('e map day rest card has 返回地圖 and no 開始今日 (v196: 逛逛日唔經確認 modal)',
    !!findBtn(card.btns, '返回地圖') && !findBtn(card.btns, '開始今日'));
  // 逛逛日確認 modal 本身（直接呼叫）：照有取消＋dismiss note 講返地圖
  let started = 0, mapped = 0, cancelled = 0;
  presentStartScheduleConfirm45(()=>{ started++; }, ()=>{ mapped++; }, ()=>{ cancelled++; });
  const c = lastModal();
  ok('e map day confirm has 返回地圖 + 取消',
    !!findBtn(c.btns, '返回地圖') && !!findBtn(c.btns, '取消（返去休息卡）'));
  ok('e map day confirm dismiss note says 撳出面＝返地圖',
    findBtn(c.btns, '撳出面＝返地圖') && findBtn(c.btns, '撳出面＝返地圖').role === 'note');
  press(c, '取消（返去休息卡）');
  ok('e map day confirm cancel calls onCancel only',
    cancelled === 1 && started === 0 && mapped === 0);
})();

/* ---- (f) presentStartScheduleConfirm45 直接呼叫：冇 onCancel 就唔出取消掣 ---- */
(function(){
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'street', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  let started = 0, cancelled = 0;
  presentStartScheduleConfirm45(()=>{ started++; }, ()=>{}, ()=>{ cancelled++; });
  const c = lastModal();
  ok('f confirm with onCancel has 取消 button', !!findBtn(c.btns, '取消（返去休息卡）'));
  press(c, '取消（返去休息卡）');
  ok('f cancel calls onCancel and nothing else', cancelled === 1 && started === 0);
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'street', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  presentStartScheduleConfirm45(()=>{ started++; }, ()=>{});
  ok('f confirm without onCancel has no 取消 button',
    !findBtn(lastModal().btns, '取消（返去休息卡）'));
})();

console.log(fails.length ? ('\nFAILURES: ' + fails.length + ' -> ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
