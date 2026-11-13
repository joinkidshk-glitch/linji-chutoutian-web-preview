// v20a196 日流程自動連跑＋故事播放鎖死返地圖・邏輯／真路徑測試
//   行真碼：nextDayIsMap／dayEndContinueButtons／morningChain196／runScheduleFromToday／
//   afterDayModal／presentRestSleepDayEnd／presentStartScheduleConfirm45／
//   story165AfterCont*／wf4PresentPending（真）／wf4PresentFenFarewell（真）；
//   邊界（modal／鏈環／StoryPlay／save）全部 stub。
//   注意：真函數經 eval 入 module scope，所以全部 stub 都要係 module 層 var，
//   reset() 負責還原鏈環 stub（唔可以靠 IIFE 內 var）。
// 用法：node tests/test_dayflow196_logic.js [path-to-index.html]
// 反證：對 pristine（v191）index 行 → nextDayIsMap／morningChain196 抽唔到，直接 throw → FAIL。
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
function extractFnExpr(name){ return eval('(' + extractFn(name) + ')'); }

/* ---- module 層 stub（真函數喺 call time 先 resolve 呢啲名） ---- */
var S = { dayIndex: 1, weekPlan: [], shoots: [] };
var FREEPLAY_FW = {};
var modalCalls = [];
var schedCalls = 0, mapCalls = 0, homeCalls = 0, resolveCalls = [], chainOrder = [], capturedConts = [];
var storyPlayStarts = [];
var firedWf4 = null, fenAfterCont = null;
var presentedLinks = {};
function defaultChainStubs(){
  // 重要：鏈環 stub 只捕捉續鏈（capturedConts），唔可以同步叫 cont()——真鏈環係
  // 等玩家撳掣／dismiss 先叫續鏈；同步叫會喺 step() 未返之前重入 step()，無限遞歸。
  // 測試用 driveChain() 逐個續鏈驅動。
  // 另外每個 stub 係 one-shot：真鏈環呈現嗰陣會消耗自己嘅 pending 狀態（獎勵清 flag、
  // 報紙 commit、WF4 清 pending），第二輪 step() 先會跳過佢繼續行落去；stub 要模擬呢點，
  // 否則續鏈重入 step() 會喺同一環無限重播。
  presentedLinks = {};
  presentPendingPostShootReward = function(cont){ if(presentedLinks.reward) return false; presentedLinks.reward = true; FREEPLAY_FW._pendingPostShootReward = null; chainOrder.push('reward'); if(typeof cont === 'function') capturedConts.push(cont); return true; };
  presentPendingAward = function(cont){ if(presentedLinks.award) return false; presentedLinks.award = true; chainOrder.push('award'); if(typeof cont === 'function') capturedConts.push(cont); return true; };
  presentDueMorningPaper = function(cont){ if(presentedLinks.paper) return false; presentedLinks.paper = true; chainOrder.push('paper'); if(typeof cont === 'function') capturedConts.push(cont); return true; };
  aud91PresentDue = function(cont){ if(presentedLinks.aud) return false; presentedLinks.aud = true; chainOrder.push('aud'); if(typeof cont === 'function') capturedConts.push(cont); return true; };
  wf4PresentPending = function(cont, opts){ if(presentedLinks.wf4) return false; presentedLinks.wf4 = true; chainOrder.push('wf4'); if(typeof cont === 'function') capturedConts.push(cont); return true; };
  kickScheduleIfNeeded = function(){ chainOrder.push('kick'); return false; };
  story165TryForcedPlay = function(kind){ chainOrder.push('forced:' + kind); return false; };
  hosp96TreatGate = function(){ return false; };
  conseq61IsSickToday = function(){ return false; };
  conseq61ResolveSickDay = function(){ return false; };
  ending78Gate = function(){ return false; };
  ending78Locked = function(){ return false; };
  wf4Ensure = function(){ return { pending: null, pendingDay: 0, fenFarewellDone: false }; };
  wf4BaseOk = function(){ return true; };
  DAILY_EVENTS_WF4 = [{ id: 'ev1' }];
  wf4Fire = function(ev, doneCb){ firedWf4 = { ev: ev, doneCb: doneCb }; if(typeof doneCb === 'function') doneCb(); };
  wf4PresentFenFarewell = function(afterCont){ fenAfterCont = afterCont; return false; };
  todayIsForcedDay = function(){ return false; };
  StoryPlay = { start: function(node, opts){ storyPlayStarts.push({ node: node, opts: opts }); return false; } };
  wf4FenFarewellNode = function(){ return { id: 'WF4_fen_farewell' }; };
}
function driveChain(){
  // 逐個續鏈驅動條鏈，直到冇續鏈剩低（鏈行完／截停）或者撞到上限（防測試本身 hang）
  let guard = 0;
  while(capturedConts.length && guard++ < 50){
    const c = capturedConts.shift();
    c();
  }
  if(guard >= 50) throw new Error('driveChain guard tripped (chain did not terminate)');
}
function reset(){
  modalCalls = []; schedCalls = 0; mapCalls = 0; homeCalls = 0; resolveCalls = []; chainOrder = []; capturedConts = [];
  storyPlayStarts = []; firedWf4 = null; fenAfterCont = null;
  S = { dayIndex: 1, weekPlan: [], shoots: [] };
  FREEPLAY_FW = {};
  _weekAccel = false; _weekAccelBuf = [];
  defaultChainStubs();
}
function modal(htmlArg, btns, opts){ modalCalls.push({ html: htmlArg, btns: btns || [], opts: opts || {} }); return true; }
function fmtDate(){ return '1990年1月2日（二）'; }
function planLabel(id){ return ({ rest:'休息', street:'街頭表演' })[id] || String(id); }
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
function weekBestReplayLine(){ return ''; }
function goToMapForBrowse(){ mapCalls++; }
function enterHome(){ homeCalls++; }
function resolvePlannedDay(id){ resolveCalls.push(id); }
function runScheduleFromTodayStub(){ schedCalls++; }
var runScheduleFromToday = runScheduleFromTodayStub;
var _weekAccel = false, _weekAccelBuf = [];
var ending78Gate, ending78Locked, kickScheduleIfNeeded, story165TryForcedPlay;
var presentPendingPostShootReward, presentPendingAward, presentDueMorningPaper, aud91PresentDue;
var wf4PresentPending, hosp96TreatGate, conseq61IsSickToday, conseq61ResolveSickDay;
var wf4Ensure, wf4BaseOk, DAILY_EVENTS_WF4, wf4Fire, wf4PresentFenFarewell, todayIsForcedDay;
var StoryPlay, wf4FenFarewellNode;
var confirmWeekAccel = function(thenGo){ if(typeof thenGo === 'function') thenGo(); };
var document = {
  body: { classList: { add(){}, remove(){}, contains(){ return false; } } },
  getElementById(){ return { classList: { add(){}, remove(){}, contains(){ return false; } } }; }
};

/* ---- 真碼入作用域（eval 會覆寫同名 stub：runScheduleFromToday 變真碼，係預期） ---- */
eval(extractFn('weekdayIdx'));
eval(extractFn('isMapDay'));
eval(extractFn('todayPlanId'));
eval(extractFn('nextDayIsMap'));
eval(extractFn('story165AfterContTake'));
eval(extractFn('story165AfterContClear'));
eval(extractFn('story165AfterContSet'));
eval(extractFn('planDayWouldWrap'));
eval(extractFn('isCriticalPlanDay'));
eval(extractFn('countRemainingAutoDays'));
eval(extractFn('dayEndContinueButtons'));
eval(extractFn('morningChain196'));
eval(extractFn('runScheduleFromToday'));
eval(extractFn('afterDayModal'));
eval(extractFn('presentStartScheduleConfirm45'));
eval(extractFn('presentRestSleepDayEnd'));
var wf4PresentPendingReal = extractFnExpr('wf4PresentPending');
var wf4PresentFenFarewellReal = extractFnExpr('wf4PresentFenFarewell');

function labels(btns){ return (btns || []).map(b => b.label); }
function findBtn(btns, sub){ return (btns || []).find(b => String(b.label || '').indexOf(sub) >= 0); }
function press(call, substr){
  const b = findBtn(call.btns, substr);
  if(!b) throw new Error('button not found: ' + substr + ' in [' + labels(call.btns).join(',') + ']');
  b.on();
  return b;
}
function lastModal(){ return modalCalls[modalCalls.length - 1]; }

/* ---- (a) nextDayIsMap：D7 判定 ---- */
(function(){
  reset();
  S.dayIndex = 1; S.weekPlan = ['scout_all', null, 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  ok('a null plan is map', nextDayIsMap() === true);
  S.weekPlan[1] = 'scout_all';
  ok('a scout_all is map', nextDayIsMap() === true);
  S.weekPlan[1] = 'street';
  ok('a street is scheduled', nextDayIsMap() === false);
  S.weekPlan[1] = 'rest';
  ok('a rest is scheduled', nextDayIsMap() === false);
  S.shoots = [{ id: 'live1', doneDays: 0, totalDays: 3 }];
  S.weekPlan[1] = 'shoot:live1';
  ok('a shoot is scheduled', nextDayIsMap() === false);
  S.weekPlan[1] = 'wrap:live1';
  ok('a wrap: history marker is map (and rewritten to scout_all)', nextDayIsMap() === true && S.weekPlan[1] === 'scout_all');
  S.weekPlan[1] = 'audition:g1';
  ok('a audition: history marker is map', nextDayIsMap() === true);
})();

/* ---- (b) dayEndContinueButtons：soft 排程日唔出「返回地圖」 ---- */
(function(){
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'street', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  const btns = dayEndContinueButtons(false, runScheduleFromTodayStub);
  ok('b soft scheduled day: only 開始今日行程', JSON.stringify(labels(btns)) === JSON.stringify(['開始今日行程']));
  ok('b soft scheduled day: no 返回地圖 anywhere', !labels(btns).some(l => l.indexOf('返回地圖') >= 0));
  btns[0].on();
  ok('b soft schedule button runs schedule', schedCalls === 1 && mapCalls === 0);
})();
(function(){
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  const btns = dayEndContinueButtons(false, runScheduleFromTodayStub);
  ok('b map next day: only 返回地圖', JSON.stringify(labels(btns)) === JSON.stringify(['返回地圖']));
})();
(function(){
  reset();
  S.dayIndex = 1;
  S.shoots = [{ id: 'live1', doneDays: 0, totalDays: 3 }];
  S.weekPlan = ['rest', 'shoot:live1', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  const btns = dayEndContinueButtons(false, runScheduleFromTodayStub);
  ok('b forced next day: only 開始今日行程', JSON.stringify(labels(btns)) === JSON.stringify(['開始今日行程']));
})();
(function(){
  reset();
  const btns = dayEndContinueButtons(true, runScheduleFromTodayStub);
  ok('b ended: only 回家結算', JSON.stringify(labels(btns)) === JSON.stringify(['回家結算']));
})();

/* ---- (c) morningChain196：次序＋兩種 finalFn＋mapMode kick ---- */
(function(){
  reset();
  FREEPLAY_FW._pendingPostShootReward = { x: 1 }; // 令獎勵環都行
  let done = 0;
  morningChain196(()=>{ done++; }, { mapMode:false });
  ok('c schedule chain pauses at first presented link', done === 0 && JSON.stringify(chainOrder) === JSON.stringify(['reward']));
  driveChain();
  ok('c schedule chain order is reward>award>paper>aud>wf4>forced>done',
    JSON.stringify(chainOrder) === JSON.stringify(['reward', 'award', 'paper', 'aud', 'wf4', 'forced:schedule']));
  ok('c schedule chain reaches done once', done === 1);
  ok('c schedule chain does NOT kick', chainOrder.indexOf('kick') < 0);
})();
(function(){
  reset();
  FREEPLAY_FW._pendingPostShootReward = { x: 1 };
  let done = 0;
  morningChain196(()=>{ done++; }, { mapMode:true });
  driveChain();
  ok('c map chain order has kick before forced',
    JSON.stringify(chainOrder) === JSON.stringify(['reward', 'award', 'paper', 'aud', 'wf4', 'kick', 'forced:map']));
  ok('c map chain reaches done once', done === 1);
})();
(function(){
  // 鏈環呈現中途停低（等玩家撳掣），續鏈先繼續——模擬報紙 modal 等緊玩家
  reset();
  presentPendingAward = function(){ return false; }; // 呢朝冇請柬，鏈跌落去報紙
  let done = 0;
  morningChain196(()=>{ done++; }, { mapMode:false });
  ok('c chain pauses while paper is presented', done === 0 && JSON.stringify(chainOrder) === JSON.stringify(['paper']));
  driveChain();
  ok('c chain resumes after paper continuation', done === 1 && chainOrder[chainOrder.length - 1] === 'forced:schedule');
})();
(function(){
  // 病假截停條鏈（病假板自己續鏈）
  reset();
  conseq61IsSickToday = function(){ return true; };
  conseq61ResolveSickDay = function(){ chainOrder.push('sick'); return true; };
  let done = 0;
  morningChain196(()=>{ done++; }, { mapMode:false });
  driveChain();
  ok('c sick day stops chain before forced play', done === 0 && chainOrder.indexOf('forced:schedule') < 0 && chainOrder.indexOf('sick') >= 0);
})();

/* ---- (d) runScheduleFromToday：排程日行鏈→行程；逛逛日落地圖 ---- */
(function(){
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['scout_all', 'street', 'rest', 'rest', 'rest', 'rest', 'scout_all'];
  runScheduleFromToday();
  driveChain();
  ok('d soft day runs chain then schedule', JSON.stringify(resolveCalls) === JSON.stringify(['street']) && mapCalls === 0);
  ok('d soft day chain ran in schedule mode', chainOrder.indexOf('forced:schedule') >= 0);
})();
(function(){
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  runScheduleFromToday();
  ok('d map day goes to map, no schedule, no chain', mapCalls === 1 && resolveCalls.length === 0 && chainOrder.length === 0);
})();
(function(){
  reset();
  S.dayIndex = 1;
  S.shoots = [{ id: 'live1', doneDays: 0, totalDays: 3 }];
  S.weekPlan = ['scout_all', 'shoot:live1', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  runScheduleFromToday();
  driveChain();
  ok('d forced day runs chain then schedule', JSON.stringify(resolveCalls) === JSON.stringify(['shoot:live1']) && mapCalls === 0);
})();

/* ---- (e) D3 slot：set／take 一次性／預設 map／clear ---- */
(function(){
  reset();
  ok('e slot starts empty', story165AfterContTake() === null);
  story165AfterContSet('schedule');
  ok('e slot schedule taken once', story165AfterContTake() === 'schedule');
  ok('e slot consumed (second take null)', story165AfterContTake() === null);
  story165AfterContSet('bogus');
  ok('e unknown kind defaults to map', story165AfterContTake() === 'map');
  story165AfterContSet('schedule');
  story165AfterContClear();
  ok('e clear drops slot', story165AfterContTake() === null);
})();

/* ---- (f) afterDayModal dismiss：排程日＝繼續（真鏈→行程），逛逛日＝返地圖 ---- */
(function(){
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'street', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  afterDayModal('<p>ok</p>', '訓練', null, false, null, {});
  const m = lastModal();
  ok('f scheduled next day: no 返回地圖 button', !labels(m.btns).some(l => l.indexOf('返回地圖') >= 0));
  m.opts.onDismiss();
  driveChain();
  ok('f scheduled next day: dismiss runs schedule via real chain', JSON.stringify(resolveCalls) === JSON.stringify(['street']) && mapCalls === 0);
})();
(function(){
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  afterDayModal('<p>ok</p>', '訓練', null, false, null, {});
  const m = lastModal();
  ok('f map next day: 返回地圖 button present', labels(m.btns).some(l => l.indexOf('返回地圖') >= 0));
  m.opts.onDismiss();
  ok('f map next day: dismiss goes to map', mapCalls === 1 && resolveCalls.length === 0);
})();

/* ---- (g) 休息卡＋確認 modal：排程日冇返地圖路，逛逛日照舊 ---- */
(function(){
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'street', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  presentRestSleepDayEnd({ title: '休息', notes: [], ended: false, summary: null, confirmStartSchedule: true });
  const card = lastModal();
  ok('g scheduled next day: rest card has no 返回地圖', !labels(card.btns).some(l => l.indexOf('返回地圖') >= 0));
  card.opts.onDismiss();
  driveChain();
  ok('g scheduled next day: rest card dismiss runs schedule', JSON.stringify(resolveCalls) === JSON.stringify(['street']) && mapCalls === 0);
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'street', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  presentRestSleepDayEnd({ title: '休息', notes: [], ended: false, summary: null, confirmStartSchedule: true });
  press(lastModal(), '開始今日');
  ok('g scheduled next day: start opens confirm (not schedule yet)', modalCalls.length === 2 && resolveCalls.length === 0);
  const c = lastModal();
  ok('g scheduled next day: confirm has no 返回地圖', !labels(c.btns).some(l => l.indexOf('返回地圖') >= 0));
  press(c, '開始今日');
  driveChain();
  ok('g scheduled next day: confirm-start runs schedule', JSON.stringify(resolveCalls) === JSON.stringify(['street']) && mapCalls === 0);
})();
(function(){
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  presentRestSleepDayEnd({ title: '休息', notes: [], ended: false, summary: null, confirmStartSchedule: true });
  const card = lastModal();
  ok('g map next day: rest card has 返回地圖', labels(card.btns).some(l => l.indexOf('返回地圖') >= 0));
  card.opts.onDismiss();
  ok('g map next day: rest card dismiss goes to map', mapCalls === 1 && resolveCalls.length === 0);
})();
(function(){
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'street', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  let started = 0, mapped = 0;
  presentStartScheduleConfirm45(()=>{ started++; }, ()=>{ mapped++; });
  const c = lastModal();
  ok('g scheduled next day: confirm has no 返回地圖', !labels(c.btns).some(l => l.indexOf('返回地圖') >= 0));
  c.opts.onDismiss();
  ok('g scheduled next day: confirm dismiss starts schedule', started === 1 && mapped === 0);
})();
(function(){
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  let started = 0, mapped = 0;
  presentStartScheduleConfirm45(()=>{ started++; }, ()=>{ mapped++; });
  const c = lastModal();
  ok('g map next day: confirm has 返回地圖', labels(c.btns).some(l => l.indexOf('返回地圖') >= 0));
  press(c, '返回地圖');
  ok('g map next day: confirm cancel maps', mapped === 1 && started === 0);
  reset();
  started = 0; mapped = 0; // reset() 唔掂 IIFE 局部計數器，呢度手動重設
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  presentStartScheduleConfirm45(()=>{ started++; }, ()=>{ mapped++; });
  lastModal().opts.onDismiss();
  ok('g map next day: confirm dismiss maps', mapped === 1 && started === 0);
})();

/* ---- (h) wf4PresentPending（真）：forced 閘＋allowForced＋預設 cont＋Fen afterCont ---- */
(function(){
  reset();
  // 唔帶 allowForced：forced 日拒絕，唔 fire
  todayIsForcedDay = function(){ return true; };
  wf4Ensure = function(){ return { pending: 'ev1', pendingDay: 1 }; };
  wf4Fire = function(ev, doneCb){ firedWf4 = { ev: ev, doneCb: doneCb }; };
  const r1 = wf4PresentPendingReal();
  ok('h forced day without allowForced refuses', r1 === false && firedWf4 === null);
  // 鏈入面 allowForced：fire，doneCb＝傳入嘅鏈續鏈
  let contRan = 0;
  const r2 = wf4PresentPendingReal(()=>{ contRan++; }, { allowForced: true, afterCont: 'schedule' });
  ok('h chain allowForced fires on forced day', r2 === true && firedWf4 && firedWf4.ev.id === 'ev1');
  firedWf4.doneCb();
  ok('h wf4 doneCb runs chain continuation', contRan === 1 && mapCalls === 0);
  // 預設 cont＝返地圖（舊行為）
  reset();
  todayIsForcedDay = function(){ return false; };
  wf4Ensure = function(){ return { pending: 'ev1', pendingDay: 1 }; };
  wf4Fire = function(ev, doneCb){ firedWf4 = { ev: ev, doneCb: doneCb }; };
  const r3 = wf4PresentPendingReal();
  ok('h no-arg call still presents', r3 === true && firedWf4 !== null);
  firedWf4.doneCb();
  ok('h default continuation goes to map', mapCalls === 1);
  // Fen 優先：afterCont 傳過去
  reset();
  todayIsForcedDay = function(){ return false; };
  wf4Ensure = function(){ return { pending: 'ev1', pendingDay: 1 }; };
  wf4PresentFenFarewell = function(afterCont){ fenAfterCont = afterCont; return true; };
  const r4 = wf4PresentPendingReal(()=>{}, { allowForced: true, afterCont: 'schedule' });
  ok('h Fen farewell gets chain afterCont', r4 === true && fenAfterCont === 'schedule' && firedWf4 === null);
})();

/* ---- (i) wf4PresentFenFarewell（真）：播之前寫 slot，預設 map ---- */
(function(){
  reset();
  wf4Ensure = function(){ return { fenFarewellDone: false }; };
  StoryPlay = { start: function(node, opts){ storyPlayStarts.push({ node: node, opts: opts }); return true; } };
  S = { dayIndex: 5, weekPlan: [], shoots: [], wf4FenFarewell: { armed: true }, exodusFenFired: false };
  const r1 = wf4PresentFenFarewellReal('schedule');
  ok('i Fen farewell starts story and writes schedule slot',
    r1 === true && storyPlayStarts.length === 1 && story165AfterContTake() === 'schedule');
  reset();
  wf4Ensure = function(){ return { fenFarewellDone: false }; };
  StoryPlay = { start: function(node, opts){ storyPlayStarts.push({ node: node, opts: opts }); return true; } };
  S = { dayIndex: 5, weekPlan: [], shoots: [], wf4FenFarewell: { armed: true }, exodusFenFired: false };
  const r2 = wf4PresentFenFarewellReal();
  ok('i Fen farewell no-arg defaults slot to map', r2 === true && story165AfterContTake() === 'map');
  reset();
  wf4Ensure = function(){ return { fenFarewellDone: true }; };
  StoryPlay = { start: function(){ storyPlayStarts.push(1); return true; } };
  S = { dayIndex: 5, weekPlan: [], shoots: [], wf4FenFarewell: { armed: true }, exodusFenFired: false };
  const r3 = wf4PresentFenFarewellReal('schedule');
  ok('i Fen farewell done already: no story, no slot', r3 === false && storyPlayStarts.length === 0 && story165AfterContTake() === null);
})();

console.log(fails.length ? ('\nFAILURES: ' + fails.length + ' -> ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
