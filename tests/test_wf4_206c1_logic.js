// v20a206 C1：迎新期保底機制（pity timer）邏輯測試。
// 用法：node tests/test_wf4_206c1_logic.js [path-to-index.html]
// 反證：喺 pristine main（v203 落地 165597e）上行 → 冇 pityDay／wf4SeenAny／
//   wf4DailyTick 冇保底檢查 → 多項乾淨 FAIL（唔 crash）。
// 關鍵種子事實（wf4Rand 確定性）：day-roll 頭 15 日只得 day 4（0.0605＜0.108）
//   同 day 10（0.0752＜0.090）擲中；day 7（0.3891）／8（0.3748）／9（0.1510）
//   全部擲唔中——所以 day 7／8／9 出 pending 一定係保底，唔係正常擲骰。
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
function extractConst(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('const not found: ' + name);
  let depth = 0, started = false, j = i;
  for(; j < html.length; j++){
    const c = html[j];
    if(c === '{' || c === '['){ depth++; started = true; }
    else if(c === '}' || c === ']'){ depth--; if(started && depth === 0){ j++; break; } }
    else if(c === ';' && !started){ j++; break; }
  }
  return html.slice(i, j);
}
/* ---- sandbox（同 test_wf4_203_logic.js 形狀；ending／forced／sick 用旗控制，等 base 守衛可測） ---- */
let S;
let _ys = { year: 1990, season: '冬' };
let _tier = 0;
let _ending = false, _forced = false, _sick = false;
let atLoc = null;
function yearSeasonNow(){ return _ys; }
function enc79PlayerTier(){ return _tier; }
function ending78Locked(){ return _ending; }
function todayIsForcedDay(){ return _forced; }
function conseq61IsSickToday(){ return _sick; }
function saveQ(){}
function apply(fx){ const n=[]; for(const k of Object.keys(fx||{})){ const v=fx[k]; if(typeof v!=='number'||!v) continue; n.push(k+v); } return n; }
function modal(h, buttons, opts){ if(buttons && buttons[0] && buttons[0].on) buttons[0].on(); }
function openLoc(id, opts){}
function goToMapForBrowse(){}
function enc79StoryPendingAt(){ return false; }
function wf4PresentFenFarewell(){ return false; }
global.document = { getElementById: () => ({ classList: { add(){}, remove(){} } }), querySelector: () => null };
const NEWS82_SRC = extractConst('NEWS82_EVENTS');
eval(NEWS82_SRC.replace('const NEWS82_EVENTS', 'global.NEWS82_EVENTS'));
const NEWS82_EVENTS = global.NEWS82_EVENTS;
const parts = [];
['DAILY_EVENTS_WF4','WF4_CFG'].forEach(n => parts.push(extractConst(n)));
['wf4Ensure','wf4Hash','wf4Rand','wf4NewsDay','wf4YearSeason','wf4Tier','wf4BaseOk','wf4CondOk','wf4PickEvent',
 'wf4ApplyFx','wf4Esc','wf4PlayEvent','wf4Fire','wf4DailyTick','wf4PresentPending',
 'wf4EffPDay','wf4EffPLoc'].forEach(n => parts.push(extractFn(n)));
/* v206 C1 新增函數（pristine 冇）：抽唔到就用 stub 頂住，等斷言乾淨 FAIL，唔好成個測試 crash */
try { parts.push(extractFn('wf4SeenAny')); }
catch(e) { parts.push('function wf4SeenAny(){ return false; }'); }
eval(parts.join('\n') + '; global.__W = { DAILY_EVENTS_WF4, WF4_CFG, wf4Ensure, wf4BaseOk, wf4CondOk, wf4PickEvent, wf4Fire, wf4DailyTick, wf4PresentPending, wf4EffPDay, wf4EffPLoc, wf4SeenAny };');
const W = global.__W;
function freshS(day){
  return { dayIndex: day||0, money: 12000, stress: 50, stamina: 60, fame: 10, popularity: 10, acting: 10, charm: 10, stage: 10,
    mockRumors: [], mockDebts: [], mockCredits: [], story: { done:{}, flags:{} } };
}
function setDay(d){
  S.dayIndex = d;
  const dt = new Date(1990, 0, 1 + d);
  const m = dt.getMonth() + 1;
  _ys = { year: dt.getFullYear(), season: (m>=3&&m<=5)?'春':(m>=6&&m<=8)?'夏':(m>=9&&m<=11)?'秋':'冬' };
  _tier = d < 100 ? 0 : d < 400 ? 1 : 2;
}
function freshAt(day){ S = freshS(day); setDay(day); _ending = false; _forced = false; _sick = false; W.wf4Ensure(); return S.wf4; }

/* (1) Config：pityDay 係 CFG 數字，唔寫死；頻率全部唔郁 */
{
  ok('WF4_CFG pityDay 7', W.WF4_CFG.pityDay === 7);
  ok('WF4_CFG 基線／迎新頻率唔郁（pDay 0.03／pLoc 0.03／pDayWelcome 0.12／pLocWelcome 0.08／welcomeDays 30）',
    W.WF4_CFG.pDay === 0.03 && W.WF4_CFG.pLoc === 0.03 && W.WF4_CFG.pDayWelcome === 0.12
    && W.WF4_CFG.pLocWelcome === 0.08 && W.WF4_CFG.welcomeDays === 30);
  ok('迎新曲線唔郁（wf4EffPDay(0)=0.12／(30)=0.03，wf4EffPLoc(0)=0.08／(30)=0.03）',
    Math.abs(W.wf4EffPDay(0) - 0.12) < 1e-9 && W.wf4EffPDay(30) === 0.03
    && Math.abs(W.wf4EffPLoc(0) - 0.08) < 1e-9 && W.wf4EffPLoc(30) === 0.03);
  ok('事件池仲係 113 單（保底唔加／減事件）', W.DAILY_EVENTS_WF4.length === 113);
}

/* (2) wf4SeenAny：兩邊都計（__n＋逐個 event id），舊 save 唔誤判 */
{
  let st = freshAt(0);
  ok('wf4SeenAny：fresh（seen 空）返 false', W.wf4SeenAny() === false);
  st.seen['wf4_ev_day01'] = 1; st.seen.__n = 1;
  ok('wf4SeenAny：__n＝1 返 true', W.wf4SeenAny() === true);
  st = freshAt(0);
  st.seen['wf4_ev_day01'] = 1; st.seen.__n = 0; // 舊 save：有 seen 但 __n 係 0
  ok('wf4SeenAny：舊 save 有 seen[id]＝1 但 __n＝0，照樣返 true（唔誤觸保底）', W.wf4SeenAny() === true);
  st = freshAt(0);
  st.seen['wf4_ev_day01'] = 1; delete st.seen.__n; // 舊 save：__n 根本 undefined
  ok('wf4SeenAny：舊 save __n undefined 但有 seen[id]，照樣返 true', W.wf4SeenAny() === true);
  st = freshAt(0);
  st.seen.__n = 0;
  ok('wf4SeenAny：__n＝0 且冇任何 event id，返 false', W.wf4SeenAny() === false);
}

/* (3) 保底喺首個 ≥ day 7 嘅 tick 觸發（day 7 正常擲骰擲唔中，出 pending 一定係保底） */
{
  const st = freshAt(7);
  W.wf4DailyTick();
  const pev = st.pending && W.DAILY_EVENTS_WF4.find(e=>e.id===st.pending);
  ok('保底：day 7 fresh 局 tick 後有 pending', !!st.pending);
  ok('保底：pendingDay＝7', st.pendingDay === 7);
  ok('保底：pending 嗰單係未見過嘅 day 事件（trig day，seen 係 0）',
    !!pev && pev.trig === 'day' && (st.seen[pev.id]||0) === 0);
  ok('保底：pending 未播——唔直接 fire（seen 仲係空，__n 仲係 0）',
    (st.seen.__n||0) === 0 && Object.keys(st.seen).filter(k=>k!=='__n').length === 0);
}

/* (4) day 7 之前唔觸發（逐日驗 day 0／1／2／3／5／6；day 4 正常擲骰擲中，唔係保底） */
{
  let anyPending = false;
  for(const d of [0, 1, 2, 3, 5, 6]){
    const st = freshAt(d);
    W.wf4DailyTick();
    if(st.pending) anyPending = true;
  }
  ok('保底：day 0／1／2／3／5／6 fresh 局 tick 後全部零 pending（保底未到日子）', !anyPending);
  const st4 = freshAt(4);
  W.wf4DailyTick();
  ok('對照：day 4 正常擲骰擲中（roll 0.0605＜0.108），pending 係正常機制，唔係保底',
    !!st4.pending && st4.pendingDay === 4);
}

/* (5) 見過事件就唔觸發（新 save __n＋舊 save 得 seen[id] 兩種） */
{
  let st = freshAt(7);
  st.seen['wf4_ev_day01'] = 1; st.seen.__n = 1;
  W.wf4DailyTick();
  ok('保底：見過 1 單（__n＝1），day 7 tick 唔設 pending', !st.pending);
  st = freshAt(7);
  st.seen['wf4_ev_day01'] = 1; st.seen.__n = 0; // 舊 save
  W.wf4DailyTick();
  ok('保底：舊 save 有 seen[id] 但 __n＝0，day 7 tick 唔誤觸', !st.pending);
  st = freshAt(8);
  st.seen['wf4_ev_day01'] = 1; st.seen.__n = 1;
  W.wf4DailyTick();
  ok('保底：見過事件，day 8（正常擲骰都擲唔中）照樣零 pending', !st.pending);
}

/* (6) 保底只觸發一次：day 7 保底 pending 經正常晨鏈播完，之後擲唔中嘅日子唔再有保底 pending */
{
  const st = freshAt(7);
  W.wf4DailyTick();
  const pityId = st.pending;
  ok('保底一次：day 7 保底 pending 已設', !!pityId);
  ok('保底一次：晨鏈 wf4PresentPending 播出保底嗰單（返 true）', W.wf4PresentPending() === true);
  ok('保底一次：播完 pending 清走，seen 記低保底嗰單（__n＝1）',
    !st.pending && (st.seen[pityId]||0) === 1 && (st.seen.__n||0) === 1);
  let pityAgain = false;
  for(const d of [8, 9, 11, 12]){ // 全部係正常擲骰擲唔中嘅日子（day 10 擲中，係正常機制，唔計）
    setDay(d);
    W.wf4DailyTick();
    if(st.pending) pityAgain = true;
    st.pending = null; // 清走先驗下一日（正常流程 pending 會經晨鏈播／過期，呢度淨係驗唔再有保底）
  }
  ok('保底一次：播完之後 day 8／9／11／12 全部零 pending（唔會觸發第二次）', !pityAgain);
}

/* (7) 有 pending 嗰陣唔觸發（唔覆蓋現有 pending） */
{
  const st = freshAt(7);
  st.pending = 'wf4_ev_day02'; st.pendingDay = 7;
  W.wf4DailyTick();
  ok('保底：已有 pending，day 7 tick 唔覆蓋（pending 仲係原先嗰單）',
    st.pending === 'wf4_ev_day02' && st.pendingDay === 7);
}

/* (8) base 唔 ok 嗰陣唔觸發（結局鎖／強制日／病日） */
{
  let st = freshAt(7);
  _ending = true;
  W.wf4DailyTick();
  ok('保底：已結局（ending78Locked），day 7 tick 唔設 pending', !st.pending);
  st = freshAt(7);
  _forced = true;
  W.wf4DailyTick();
  ok('保底：強制日（todayIsForcedDay），day 7 tick 唔設 pending', !st.pending);
  st = freshAt(7);
  _sick = true;
  W.wf4DailyTick();
  ok('保底：病日（conseq61IsSickToday），day 7 tick 唔設 pending', !st.pending);
  st = freshAt(7);
  _forced = true;
  W.wf4DailyTick(); // 強制日擋住，唔設 pending
  _forced = false;
  setDay(8);
  W.wf4DailyTick(); // 下一日唔再係強制日，保底喺 day 8 補觸發（唔會因為 day 7 錯過就永遠唔出）
  ok('保底：day 7 撞強制日，day 8 一解封即刻補觸發（pendingDay＝8）',
    !!st.pending && st.pendingDay === 8);
}

/* (9) pityDay 係 CFG 數字，唔係寫死 7：改做 9，day 7／8 唔觸發，day 9 觸發 */
{
  const old = W.WF4_CFG.pityDay;
  W.WF4_CFG.pityDay = 9;
  let st = freshAt(7);
  W.wf4DailyTick();
  const no7 = !st.pending;
  st = freshAt(8);
  W.wf4DailyTick();
  const no8 = !st.pending;
  st = freshAt(9);
  W.wf4DailyTick();
  const yes9 = !!st.pending && st.pendingDay === 9; // day 9 正常擲骰擲唔中（0.1510≥0.093），出 pending 一定係保底
  W.WF4_CFG.pityDay = old;
  ok('保底：pityDay 改做 9，day 7／8 唔觸發、day 9 先觸發（數字跟 CFG 行）', no7 && no8 && yes9);
  ok('保底：CFG 還原返 7', W.WF4_CFG.pityDay === 7);
}

/* (10) 保底揀嘅單合資格：day 7 池（1990 年冬、tier 0）入面 cond 啱＋未見過 */
{
  const st = freshAt(7);
  W.wf4DailyTick();
  const pev = W.DAILY_EVENTS_WF4.find(e=>e.id===st.pending);
  ok('保底：揀出嚟嗰單 cond 合資格（wf4CondOk 返 true）', !!pev && W.wf4CondOk(pev) === true);
}

console.log(fails.length ? ('FAILURES: ' + fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
