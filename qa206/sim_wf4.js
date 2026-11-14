// WF4 模擬器 v20a206 C1：直接 eval 遊戲 index.html 入面嘅真實 WF4 引擎 code
// （DAILY_EVENTS_WF4 + WF4_CFG + wf4Ensure/wf4Hash/wf4Rand/wf4BaseOk/wf4CondOk/
// wf4PickEvent/wf4Fire/wf4DailyTick/wf4TryLocEvent/wf4PresentPending/wf4SeenAny），
// 其餘環境用 stub。唔改遊戲 code。
// 用法：node qa206/sim_wf4.js [path-to-index.html]
// （WF4_SRC 環境變數亦可指定；預設工作副本 ~/workspace/linji-work206/index.html）
//
// v203 sim 路線假設逐日 tick＋每日 2 地點；review C1 指出實玩「開始今日行程」一次
// 跳 3–4 日，質疑中間嗰幾日嘅 tick。Code 核實（見 NOTES_V20A206 §6）：唯一推進
// dayIndex 嘅生產路徑係 advanceDay()（+1，兼每次 call wf4DailyTick()）；直接賦值
// 嗰兩處係 console preview（previewJumpCalendarYear）同 soft-preview seed
// （applySoftSeedState，flag-gated），唔係 live 玩法——所以 live 玩法每日恰好一次 tick，
// 跳日唔會跳 tick。Sim 照實玩路線跑：每日 tick＋每日 2 地點（開局頭幾日係故事／
// 行程日，唔入場——R 路線）；另加對照變體 R-skip（假設 tick 只跑落點日，
// 落點日 0→3→7→9→…，等保底喺邊種 tick 模型下都企得住）＋兩個保底觸發情境
// （F：首 7 日強制日封 tick；E：day 4 pending 嗰日＋之後兩日都強制日，
// 晨鏈播唔出，捱到 day 7 過期清走，保底補派）。
// 兩種呈現次序都跑：same-day（v203 舊次序：tick→入場→即日呈現，等 A–D 數字可比）
// ＋morning（真實次序：晨鏈呈現→入場→收尾 tick 下一日，pending 翌朝先出）。
// 保底識別（唔靠估）：tick 之後 pending 係新設、當日日骰擲唔中（wf4Rand("wf4day:"+d)
// ≥ wf4EffPDay(d)）、設嗰陣 seen 空——三樣齊先記做保底派單。
const fs = require('fs');
const SRC = fs.readFileSync(process.env.WF4_SRC || '/home/hatch/workspace/linji-work206/index.html', 'utf8');
const lines = SRC.split('\n');
function findLine(pat) { for (let i = 0; i < lines.length; i++) if (lines[i].includes(pat)) return i; return -1; }
const start = findLine('const DAILY_EVENTS_WF4');
const ppStart = findLine('function wf4PresentPending');
let end = -1;
for (let j = ppStart; j < ppStart + 40; j++) { if (lines[j].trim() === '}') { end = j; break; } }
if (start < 0 || end < 0) throw new Error('WF4 block not found');
const chunk = lines.slice(start, end + 1).join('\n');

// ---- stubs ----
let S = null;
let atLoc = null;
let _forcedDays = null; // Set<day>：呢啲日子 todayIsForcedDay() 返 true（情境 F／E 用）
const fired = []; // {day, id}
globalThis.S = null;
function resetState() {
  S = { dayIndex: 0, money: 12000, stress: 50, wf4: null };
  globalThis.S = S;
  fired.length = 0;
}
function yearSeasonNow() {
  const d = new Date(1990, 0, 1 + (S.dayIndex | 0));
  const y = d.getFullYear(), m = d.getMonth() + 1;
  const season = (m >= 3 && m <= 5) ? '春' : (m >= 6 && m <= 8) ? '夏' : (m >= 9 && m <= 11) ? '秋' : '冬';
  return { year: y, season };
}
function enc79PlayerTier() {
  const d = S.dayIndex | 0;
  return d < 100 ? 0 : d < 400 ? 1 : 2;
}
globalThis.yearSeasonNow = yearSeasonNow;
globalThis.enc79PlayerTier = enc79PlayerTier;
globalThis.ending78Locked = () => false;
globalThis.todayIsForcedDay = () => !!(_forcedDays && _forcedDays.has(S.dayIndex | 0));
globalThis.conseq61IsSickToday = () => false;
globalThis.saveQ = () => {};
globalThis.openLoc = () => {};
globalThis.goToMapForBrowse = () => {};
globalThis.enc79StoryPendingAt = () => false;
globalThis.wf4PlayEvent = (ev, doneCb) => { fired.push({ day: S.dayIndex | 0, id: ev.id }); if (typeof doneCb === 'function') { try { doneCb(); } catch (e) {} } };
globalThis.wf4PresentFenFarewell = () => false;
globalThis.NEWS82_EVENTS = [];

(0, eval)(chunk + '\n;globalThis.__wf4 = { DAILY_EVENTS_WF4, WF4_CFG, wf4DailyTick, wf4TryLocEvent, wf4PresentPending, wf4Ensure, wf4PickEvent }; if(typeof wf4EffPDay!=="undefined") globalThis.__wf4.wf4EffPDay = wf4EffPDay; if(typeof wf4EffPLoc!=="undefined") globalThis.__wf4.wf4EffPLoc = wf4EffPLoc; if(typeof wf4SeenAny!=="undefined") globalThis.__wf4.wf4SeenAny = wf4SeenAny; if(typeof wf4Rand!=="undefined") globalThis.__wf4.wf4Rand = wf4Rand;');
globalThis.wf4PlayEvent = (ev, doneCb) => { fired.push({ day: S.dayIndex | 0, id: ev.id }); if (typeof doneCb === 'function') { try { doneCb(); } catch (e) {} } };
const WF = globalThis.__wf4;

const LOCS7 = ['film_lion', 'tvb_longmen', 'cafe_cha', 'film_cotton', 'film_harbour', 'tvb_harbour', 'tvb_kowloon'];
const routeA = d => [LOCS7[d % 7], LOCS7[(d + 3) % 7]];
const routeB = () => ['tvb_longmen', 'cafe_cha'];
const routeC = () => ['film_lion', 'film_cotton'];
const routeD = () => ['cafe_cha', 'cafe_cha'];
// R：實玩路線（review R2：每日輪入 7 地點其中 2 個＋過一日；開局頭 3 日係故事／行程日，唔入場）
const routeR = d => (d < 3 ? [] : [LOCS7[d % 7], LOCS7[(d + 3) % 7]]);
// S0：全程行程日，零入場（淨靠日骰）
const routeS0 = () => [];

function seenAny() {
  const st = S.wf4;
  if (!st || !st.seen) return false;
  return ((st.seen.__n || 0) > 0) || Object.keys(st.seen).some(k => k !== '__n' && (st.seen[k] || 0) > 0);
}

function runSim(days, locRoute, label, opts) {
  opts = opts || {};
  const order = opts.order || 'same-day';
  resetState();
  _forcedDays = opts.forcedDays || null;
  WF.wf4Ensure();
  const pitySets = []; // {day, id}：tick 新設 pending＋當日日骰擲唔中＋設嗰陣 seen 空
  const pityFired = [];
  function tickFor(day) {
    const beforePending = S.wf4.pending;
    const beforeSeen = seenAny();
    S.dayIndex = day;
    WF.wf4DailyTick();
    const st = S.wf4;
    if (st.pending && st.pending !== beforePending && st.pendingDay === day && !beforeSeen) {
      const rollPasses = WF.wf4Rand('wf4day:' + day) < WF.wf4EffPDay(day);
      if (!rollPasses && day >= (WF.WF4_CFG.pityDay || 7)) pitySets.push({ day, id: st.pending });
    }
  }
  function locsFor(day) {
    if (_forcedDays && _forcedDays.has(day)) return; // 強制日行行程，唔逛地點
    for (const loc of locRoute(day)) { atLoc = loc; WF.wf4TryLocEvent(loc); }
  }
  function presentFor(day) {
    const n0 = fired.length;
    S.dayIndex = day;
    WF.wf4PresentPending();
    for (let i = n0; i < fired.length; i++) {
      if (pitySets.some(p => p.id === fired[i].id)) pityFired.push({ day: fired[i].day, id: fired[i].id });
    }
  }
  if (order === 'morning') {
    for (let d = 0; d < days; d++) {
      presentFor(d);
      locsFor(d);
      tickFor(d + 1);
    }
  } else { // same-day（v203 舊次序）
    for (let d = 0; d < days; d++) {
      tickFor(d);
      locsFor(d);
      presentFor(d);
    }
  }
  _forcedDays = null;
  const in30 = fired.filter(f => f.day < 30);
  const first = fired.length ? fired[0].day : null;
  console.log(`${label} [${order}]：頭 30 日 ${in30.length} 單，首單 day ${first === null ? '-' : first}（${fired.slice(0, 8).map(f => 'day' + f.day + ':' + f.id).join('，') || '零事件'}）${pitySets.length ? '；保底派單：' + pitySets.map(p => 'day' + p.day + ':' + p.id).join('，') + '；保底播出：' + (pityFired.map(p => 'day' + p.day + ':' + p.id).join('，') || '未播出') : '；保底零觸發'}`);
  return { total30: in30.length, first, fired: fired.slice(), pitySets, pityFired };
}

// 保底揀邊單（day 7、seen 空、確定性 pick）：等實駕對返係咪保底派
{
  resetState();
  WF.wf4Ensure();
  S.dayIndex = 7;
  const pev = WF.wf4PickEvent('day', null);
  console.log(`保底 pick（day 7、seen 空）：${pev ? pev.id + '「' + pev.title + '」' : 'null（池空）'}`);
  console.log('WF4_CFG:', JSON.stringify(WF.WF4_CFG));
  console.log('day 池：' + WF.DAILY_EVENTS_WF4.filter(e => e.trig === 'day').length + ' 單；loc 池：' + WF.DAILY_EVENTS_WF4.filter(e => e.trig === 'loc').length + ' 單；總數：' + WF.DAILY_EVENTS_WF4.length + ' 單');
}

console.log('\n===== 頭 30 日：v203 四路線對照（same-day 次序，等數字可比） =====');
for (const [label, fn] of [['A 均衡', routeA], ['B 電視', routeB], ['C 電影', routeC], ['D 茶餐廳', routeD]]) {
  runSim(30, fn, label, { order: 'same-day' });
}
console.log('\n===== 頭 30 日：實玩路線 R（開局 3 日唔入場＋每日 2 地點） =====');
runSim(30, routeR, 'R 實玩', { order: 'same-day' });
runSim(30, routeR, 'R 實玩', { order: 'morning' });
runSim(30, routeS0, 'S0 零入場', { order: 'morning' });
console.log('\n===== 頭 30 日：對照變體 R-skip（假設 tick 只跑落點日 0→3→7→9→…，§14 假設） =====');
{
  const landings = [0, 3, 7, 9, 12, 16, 19, 23, 26, 29];
  resetState();
  WF.wf4Ensure();
  const pitySets = [];
  for (const d of landings) {
    S.dayIndex = d;
    const beforeSeen = seenAny();
    WF.wf4DailyTick();
    const st = S.wf4;
    if (st.pending && st.pendingDay === d && !beforeSeen && WF.wf4Rand('wf4day:' + d) >= WF.wf4EffPDay(d) && d >= (WF.WF4_CFG.pityDay || 7)) pitySets.push({ day: d, id: st.pending });
    for (const loc of [LOCS7[d % 7], LOCS7[(d + 3) % 7]]) { atLoc = loc; WF.wf4TryLocEvent(loc); }
    WF.wf4PresentPending();
  }
  const first = fired.length ? fired[0].day : null;
  console.log(`R-skip [same-day]：頭 30 日 ${fired.length} 單，首單 day ${first === null ? '-' : first}（${fired.map(f => 'day' + f.day + ':' + f.id).join('，') || '零事件'}）；保底派單：${pitySets.map(p => 'day' + p.day + ':' + p.id).join('，') || '零觸發'}`);
}
console.log('\n===== 保底觸發情境（morning 次序） =====');
// F：首 7 日強制日（tick 封死＋唔入場），day 7 起解封
runSim(30, d => (d < 7 ? [] : routeR(d)), 'F 首 7 日強制日封 tick', { order: 'morning', forcedDays: new Set([0, 1, 2, 3, 4, 5, 6]) });
// E：day 4 pending 設咗，但嗰日＋之後兩日都強制日（晨鏈呈現俾 baseOk 擋住，捱到 day 7 過期清走），保底補派
// （頭 7 日零入場，等 day 3 唔會有 loc 事件先設到 day 4 pending；唔係就會似舊版 E 咁俾 gap 擋住 tick）
runSim(30, d => (d < 7 ? [] : routeR(d)), 'E day 4 pending 播唔出→過期→保底補派', { order: 'morning', forcedDays: new Set([4, 5, 6]) });
console.log('\n===== 三年：A 均衡路線（保底有冇提早抽乾） =====');
{
  resetState();
  WF.wf4Ensure();
  for (let d = 0; d < 1095; d++) {
    S.dayIndex = d;
    WF.wf4DailyTick();
    for (const loc of routeA(d)) { atLoc = loc; WF.wf4TryLocEvent(loc); }
    WF.wf4PresentPending();
  }
  const distinct = new Set(fired.map(f => f.id)).size;
  console.log(`A 三年：${fired.length} 單，唔同 ${distinct}／113，首單 day ${fired[0].day}，尾單 day ${fired[fired.length - 1].day}`);
}
