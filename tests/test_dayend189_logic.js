// v20a189 日結板三粒掣・邏輯／真路徑測試
//   行真 dayEndContinueButtons＋真 countRemainingAutoDays＋真 runScheduleFromToday（抽出嚟跑）：
//   (a) v196：soft 日（排程日）唔出「返回地圖」，只留「開始今日行程」；「開始今日行程」繼續行 goRunSchedule。
//   (b) forced／map／ended 分支唔郁（map 嗰粒繼續經 goRunSchedule，等獎勵流程行先）。
//   (c) 加速係 role "link" 細連結，撳落去照行 confirmWeekAccel（thenGo 再行 goRunSchedule）；
//       本週冇剩餘自動日就唔出連結。
//   (d) runScheduleFromToday 分流核實（修前驗證）：soft 日直接開行程（resolvePlannedDay），
//       地圖日先至返地圖——所以 (a) 兩粒修好後真係分流，唔會再撞。
// 用法：node tests/test_dayend189_logic.js [path-to-index.html]
// 注意：todayPlanId 呢度 stub 做純查表（分支邏輯用）；真 todayPlanId 嘅 wrap:／死 shoot 改寫行為唔喺呢度測。
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

/* ---- stubs（只 stub 邊界；被測函數全部係真碼） ---- */
var S = { dayIndex: 1, weekPlan: [], shoots: [] };
var mapCalls = 0, schedCalls = 0, confirmCalls = [], resolveCalls = [];
function reset(){
  mapCalls = 0; schedCalls = 0; confirmCalls = []; resolveCalls = [];
  S = { dayIndex: 1, weekPlan: [], shoots: [] };
}
function todayPlanId(){ return (S.weekPlan || [])[weekdayIdx(S.dayIndex)] || null; }
function isMapDay(id){ return !!id && (id === 'scout_all' || id === 'scout_nt' || id === 'scout_kln' || id === 'scout_island'); }
function confirmWeekAccel(thenGo){ confirmCalls.push(thenGo); }
function goToMapForBrowse(){ mapCalls++; }
function resolvePlannedDay(id){ resolveCalls.push(id); }
function presentDueMorningPaper(){ return false; }
function aud91PresentDue(){ return false; }
/* v20a196 D2：共用晨鏈嘅其餘鏈環 stub（全部「冇嘢播」，鏈直接跌落去行程） */
var FREEPLAY_FW = {};
function ending78Gate(){ return false; }
function presentPendingPostShootReward(){ return false; }
function presentPendingAward(){ return false; }
function wf4PresentPending(){ return false; }
function story165TryForcedPlay(){ return false; }
function kickScheduleIfNeeded(){ return false; }
function hosp96TreatGate(){ return false; }
function conseq61IsSickToday(){ return false; }
function conseq61ResolveSickDay(){ return false; }
function storyOpenSnapshot(){ return { open: [] }; }
function modal(){ return false; }
function fmtDate(){ return ''; }
function weekBestReplayLine(){ return ''; }
var _weekAccel = false, _weekAccelBuf = [];
function goRunSchedule(){ schedCalls++; } // 標記函數：on === goRunSchedule 即係行程路徑

/* ---- 真碼入作用域 ---- */
eval(extractFn('weekdayIdx'));
eval(extractFn('planDayWouldWrap'));
eval(extractFn('isCriticalPlanDay'));
eval(extractFn('countRemainingAutoDays'));
eval(extractFn('nextDayIsMap')); /* v20a196 D7：dayEndContinueButtons 而家靠佢判定逛逛日 */
eval(extractFn('dayEndContinueButtons'));
eval(extractFn('morningChain196')); /* v20a196 D2：runScheduleFromToday 排程日行呢條共用晨鏈 */
eval(extractFn('runScheduleFromToday'));

function labels(btns){ return (btns || []).map(b => b.label); }
function findBtn(btns, sub){ return (btns || []).find(b => String(b.label || '').indexOf(sub) >= 0); }

/* ---- (a) v196 soft：排程日唔出「返回地圖」，只留「開始今日行程」＋加速連結 ---- */
(function(){
  reset();
  // 注意：dayEndContinueButtons 係 tickDay 之後先叫，S.dayIndex 已經係新一日（聽日）；
  // 呢度 dayIndex=1（週二）就係要分支嗰日：street（soft），Wed–Sat rest → 剩餘自動日 >0
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'street', 'rest', 'rest', 'rest', 'rest', 'scout_all'];
  const btns = dayEndContinueButtons(false, goRunSchedule);
  ok('a v196 soft has only schedule + accel-link (no 返回地圖)',
    JSON.stringify(labels(btns)) === JSON.stringify(['開始今日行程', '想跳過本週剩餘日子？加速 →']));
  ok('a soft has no 返回地圖 button', !findBtn(btns, '返回地圖'));
  const schedBtn = findBtn(btns, '開始今日行程');
  ok('a soft schedule button IS goRunSchedule', schedBtn && schedBtn.on === goRunSchedule);
  const link = findBtn(btns, '加速');
  ok('a accel is a link (role link, not a big button)', link && link.role === 'link');
  link.on();
  ok('a accel link calls confirmWeekAccel once', confirmCalls.length === 1 && typeof confirmCalls[0] === 'function');
  confirmCalls[0]();
  ok('a accel confirm continuation runs schedule', schedCalls === 1);
})();

/* ---- (b) forced／map／ended 唔郁 ---- */
(function(){
  reset();
  S.dayIndex = 1;
  S.shoots = [{ id: 'live1', doneDays: 0, totalDays: 3 }];
  S.weekPlan = ['rest', 'shoot:live1', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  const btns = dayEndContinueButtons(false, goRunSchedule);
  ok('b forced has only 開始今日行程', JSON.stringify(labels(btns)) === JSON.stringify(['開始今日行程']));
  ok('b forced schedule runs goRunSchedule', btns[0].on === goRunSchedule);
})();
(function(){
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  const btns = dayEndContinueButtons(false, goRunSchedule);
  ok('c map has only 返回地圖', JSON.stringify(labels(btns)) === JSON.stringify(['返回地圖']));
  ok('c map button still goes via goRunSchedule (v20a4 reward path)', btns[0].on === goRunSchedule);
})();
(function(){
  reset();
  const btns = dayEndContinueButtons(true, goRunSchedule);
  ok('d ended has only 回家結算', JSON.stringify(labels(btns)) === JSON.stringify(['回家結算']));
  ok('d ended goes home via goRunSchedule', btns[0].on === goRunSchedule);
})();

/* ---- (c) 冇剩餘自動日 → 唔出加速連結 ---- */
(function(){
  reset();
  S.dayIndex = 1;
  S.weekPlan = ['rest', 'street', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  const btns = dayEndContinueButtons(false, goRunSchedule);
  ok('e no remaining auto days -> no accel link, v196 soft only 開始今日行程',
    JSON.stringify(labels(btns)) === JSON.stringify(['開始今日行程']));
})();

/* ---- (d) runScheduleFromToday 分流核實 ---- */
(function(){
  reset();
  S.dayIndex = 1; // 今日 Tue street
  S.weekPlan = ['scout_all', 'street', 'rest', 'rest', 'rest', 'rest', 'scout_all'];
  runScheduleFromToday();
  ok('f soft day runs schedule directly (resolvePlannedDay)', JSON.stringify(resolveCalls) === JSON.stringify(['street']) && mapCalls === 0);
})();
(function(){
  reset();
  S.dayIndex = 1; // 今日 Tue map day
  S.weekPlan = ['scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  runScheduleFromToday();
  ok('g map day goes to map, no schedule', mapCalls === 1 && resolveCalls.length === 0);
})();
(function(){
  reset();
  S.dayIndex = 1; // 今日 Tue shoot day
  S.shoots = [{ id: 'live1', doneDays: 0, totalDays: 3 }];
  S.weekPlan = ['scout_all', 'shoot:live1', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  runScheduleFromToday();
  ok('h forced day runs schedule directly', JSON.stringify(resolveCalls) === JSON.stringify(['shoot:live1']) && mapCalls === 0);
})();

console.log(fails.length ? ('\nFAILURES: ' + fails.length + ' -> ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
