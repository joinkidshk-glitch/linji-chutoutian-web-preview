// WF4 模擬器：直接 eval 遊戲 index.html 入面嘅真實 WF4 引擎 code（DAILY_EVENTS_WF4
// + WF4_CFG + wf4Ensure/wf4Hash/wf4Rand/wf4BaseOk/wf4CondOk/wf4PickEvent/wf4Fire/
// wf4DailyTick/wf4TryLocEvent/wf4PresentPending），其餘環境用 stub。
// 用途：量度隨機事件重複率。唔改遊戲 code。
const fs = require('fs');
const SRC = fs.readFileSync(process.env.WF4_SRC || '/home/hatch/workspace/linji-work193/index.html', 'utf8');
const lines = SRC.split('\n');
// 動態定位（唔寫死行號，main 落地會漂移）：由 DAILY_EVENTS_WF4 起，
// 到 wf4PresentPending 函數完結（之後第一個獨立 "}" 行）。
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
const fired = []; // {day, id, via}
globalThis.S = null;
function resetState() {
  S = { dayIndex: 0, money: 12000, stress: 50, wf4: null };
  globalThis.S = S;
  fired.length = 0;
}
// year/season from dayIndex (1990-01-01 起)
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
globalThis.todayIsForcedDay = () => false;
globalThis.conseq61IsSickToday = () => false;
globalThis.saveQ = () => {};
globalThis.openLoc = () => {};
globalThis.goToMapForBrowse = () => {};
globalThis.enc79StoryPendingAt = () => false;
// wf4Fire 會 call wf4PlayEvent：記低就算，唔播
globalThis.wf4PlayEvent = (ev, doneCb) => { fired.push({ day: S.dayIndex | 0, id: ev.id }); if (typeof doneCb === 'function') { try { doneCb(); } catch (e) {} } };
// wf4PresentPending 會 call wf4PresentFenFarewell：WF4_FRAG 嗰段之後先定義，呢度 stub false
globalThis.wf4PresentFenFarewell = () => false;
// NEWS82_EVENTS（報紙日）— 設空，唔擋事件
globalThis.NEWS82_EVENTS = [];

// eval 真實引擎 chunk（用 indirect eval 入 global scope，令 const/函數成 global）
// 注意：chunk 入面有真正嘅 wf4PlayEvent（L40726），eval 會蓋過上面嘅 stub，
// 所以 recorder stub 要喺 eval 之後再賦值一次。
(0, eval)(chunk + '\n;globalThis.__wf4 = { DAILY_EVENTS_WF4, WF4_CFG, wf4DailyTick, wf4TryLocEvent, wf4PresentPending, wf4Ensure, wf4PickEvent };');
globalThis.wf4PlayEvent = (ev, doneCb) => { fired.push({ day: S.dayIndex | 0, id: ev.id }); if (typeof doneCb === 'function') { try { doneCb(); } catch (e) {} } };
const WF = globalThis.__wf4;
if(process.env.WF4_PDAY) WF.WF4_CFG.pDay = parseFloat(process.env.WF4_PDAY);
if(process.env.WF4_PLOC) WF.WF4_CFG.pLoc = parseFloat(process.env.WF4_PLOC);
if(process.env.WF4_GAP) WF.WF4_CFG.gapDays = parseInt(process.env.WF4_GAP,10);

function runSim(days, locRoute, label) {
  resetState();
  const st0 = WF.wf4Ensure();
  for (let d = 0; d < days; d++) {
    S.dayIndex = d;
    // 每日 tick（朝早結算）
    WF.wf4DailyTick();
    // 入兩個地點（出行額度 2）
    for (const loc of locRoute(d)) {
      atLoc = loc;
      WF.wf4TryLocEvent(loc);
    }
    // 返地圖嗰陣 pending 事件彈出
    WF.wf4PresentPending();
  }
  // 統計
  const counts = {};
  const firstSeen = {}, lastSeen = {}, minGap = {};
  fired.forEach(f => {
    counts[f.id] = (counts[f.id] || 0) + 1;
    if (firstSeen[f.id] === undefined) firstSeen[f.id] = f.day;
    if (lastSeen[f.id] !== undefined) {
      const g = f.day - lastSeen[f.id];
      if (minGap[f.id] === undefined || g < minGap[f.id]) minGap[f.id] = g;
    }
    lastSeen[f.id] = f.day;
  });
  const total = fired.length;
  const distinct = Object.keys(counts).length;
  const repeats = total - distinct;
  const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]);
  const within60 = fired.filter((f, i) => {
    const prev = fired.slice(0, i).findLast(x => x.id === f.id);
    return prev && (f.day - prev.day) <= 60;
  }).length;
  const within90 = fired.filter((f, i) => {
    const prev = fired.slice(0, i).findLast(x => x.id === f.id);
    return prev && (f.day - prev.day) <= 90;
  }).length;
  console.log(`\n===== ${label} (${days} 日) =====`);
  console.log(`事件總數: ${total}（平均每 ${(days / total).toFixed(1)} 日一單）`);
  console.log(`唔同事件: ${distinct} / 36；重複次數: ${repeats}（${(100 * repeats / total).toFixed(0)}% 嘅事件係重複）`);
  console.log(`60 日內重複: ${within60} 次；90 日內重複: ${within90} 次`);
  console.log('頭 10 多見事件:');
  sorted.slice(0, 10).forEach(([id, c]) => {
    console.log(`  ${id}: ${c} 次（首次 day ${firstSeen[id]}，最短重複間隔 ${minGap[id] === undefined ? '-' : minGap[id] + ' 日'}）`);
  });
  console.log('從未出現: ' + WF.DAILY_EVENTS_WF4.map(e => e.id).filter(id => !counts[id]).join(', '));
  // 抽乾日：每組（day 池／各地點 loc 池）distinct 達到最終值嗰日（-1 = 未抽乾）
  const groups = { day: new Set(WF.DAILY_EVENTS_WF4.filter(e=>e.trig==='day').map(e=>e.id)) };
  WF.DAILY_EVENTS_WF4.filter(e=>e.trig==='loc').forEach(e=>{ (groups['loc:'+e.loc] = groups['loc:'+e.loc] || new Set()).add(e.id); });
  const finalByGroup = {}, exhByGroup = {};
  for(const g of Object.keys(groups)){
    const ids=[...groups[g]].filter(id=>counts[id]);
    finalByGroup[g]=ids.length;
    const seenG=new Set(); let d=-1;
    for(const f of fired){ if(groups[g].has(f.id)){ seenG.add(f.id); if(seenG.size===ids.length){ d=f.day; break; } } }
    exhByGroup[g]=d;
  }
  const dayIds = groups.day;
  const dayDistinct = finalByGroup.day;
  const dayTotal = fired.filter(f=>dayIds.has(f.id)).length;
  const locTotal = total - dayTotal;
  const exhDay = Math.max(...Object.values(exhByGroup));
  console.log(`抽乾日(全部 distinct 停長): ${exhDay}；day 池: ${dayDistinct} 單 distinct／${dayTotal} 次 day 抽獎 (day 池抽乾日 ${exhByGroup.day})；loc 抽獎 ${locTotal} 次`);
  console.log('各組抽乾日: ' + Object.entries(exhByGroup).map(([g,d])=>`${g}:${finalByGroup[g]}單@${d<0?'未抽乾':'day '+d}`).join(' '));
  const maxCnt = Math.max(...Object.values(counts));
  console.log(`重複率: ${(100*repeats/Math.max(total,1)).toFixed(1)}%（once 規則下應為 0%；最多見一單 ${maxCnt} 次）`);
  return { total, distinct, repeats, counts, fired: fired.slice(), exhDay, exhByGroup, dayDistinct, dayTotal };
}

const LOCS_A = ['film_lion', 'tvb_longmen', 'cafe_cha', 'film_cotton', 'film_harbour', 'tvb_harbour', 'tvb_kowloon'];
const routeA = d => [LOCS_A[d % 7], LOCS_A[(d + 3) % 7]];                       // 均衡跑圖
const routeB = d => ['tvb_longmen', 'cafe_cha'];                               // 電視線
const routeC = d => ['film_lion', 'film_cotton'];                              // 電影線
const routeD = d => ['cafe_cha', 'cafe_cha'];                                  // 成日去茶餐廳
runSim(365, routeA, 'A 均衡跑圖（7 地點輪住去）');
runSim(365, routeB, 'B 電視線（星河電視台＋金龍茶餐廳）');
runSim(365, routeC, 'C 電影線（獅子山＋紅棉）');
runSim(365, routeD, 'D 茶餐廳常客');
runSim(1095, routeA, 'A 均衡跑圖（全三年 1095 日）');
runSim(1095, routeB, 'B 電視線（全三年 1095 日）');
// 每個地點嘅 loc 池大細
console.log('\n===== 各地點 loc 池（未計條件過濾） =====');
const byLoc = {};
WF.DAILY_EVENTS_WF4.filter(e => e.trig === 'loc').forEach(e => {
  byLoc[e.loc] = byLoc[e.loc] || [];
  byLoc[e.loc].push(e.id + (e.once ? ' (once)' : ''));
});
Object.entries(byLoc).forEach(([loc, ids]) => console.log(`  ${loc}: ${ids.length} 個 — ${ids.join(', ')}`));
console.log(`day 池: ${WF.DAILY_EVENTS_WF4.filter(e => e.trig === 'day').length} 個`);
console.log('WF4_CFG:', JSON.stringify(WF.WF4_CFG));
