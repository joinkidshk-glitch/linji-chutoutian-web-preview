// v20a86 WF4 邏輯測試：日常事件池＋碎片庫＋芬姐／霞姐小弧＋對手線做深覆寫
// 用法：node tests/test_wf4_86_logic.js [path-to-index.html]
// 反證：喺 v20a85 index 上行 → 冇 DAILY_EVENTS_WF4／WF4 模組 → 抽取即 throw → FAIL。
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
/* ---- sandbox ---- */
let S;
let _ys = { year: 1990, season: '春' };
let _tier = 0, _locked = false, _forced = false, _sick = false;
let _playedNodes = [], _openedLocs = [], _mapReturns = 0;
function yearSeasonNow(){ return _ys; }
function enc79PlayerTier(){ return _tier; }
function ending78Locked(){ return _locked; }
function todayIsForcedDay(){ return _forced; }
function conseq61IsSickToday(){ return _sick; }
function saveQ(){}
function apply(fx){
  const notes = [];
  for(const k of Object.keys(fx||{})){
    const v = fx[k]; if(typeof v !== 'number' || !v) continue;
    if(k === 'money'){ S.money = Math.max(0, (S.money||0) + v); }
    else { S[k] = Math.max(0, (S[k]||0) + v); }
    notes.push(k + v);
  }
  return notes;
}
function modal(h, buttons, opts){ if(buttons && buttons[0] && buttons[0].on) buttons[0].on(); }
function openLoc(id, opts){ _openedLocs.push([id, opts]); }
function goToMapForBrowse(){ _mapReturns++; }
const StoryPlay = { start(node, opts){ _playedNodes.push(node); return true; } };
const StoryOC = { isDone(){ return false; }, getFlag(){ return false; } };

const NEWS82_SRC = extractConst('NEWS82_EVENTS');
eval(NEWS82_SRC.replace('const NEWS82_EVENTS', 'global.NEWS82_EVENTS'));
const NEWS82_EVENTS = global.NEWS82_EVENTS;

const parts = [];
['DAILY_EVENTS_WF4','WF4_CFG','WF4_FX_LABEL','WF4_FRAG_SEEDS','WF4_FEN_INTRO_NODE','RIVAL_WF4_OVERRIDES','WF4_RIVAL_APPLIED86']
  .forEach(n => parts.push(extractConst(n)));
['wf4Ensure','wf4Hash','wf4Rand','wf4NewsDay','wf4YearSeason','wf4Tier','wf4BaseOk','wf4CondOk','wf4PickEvent',
 'wf4ApplyFx','wf4Esc','wf4PlayEvent','wf4Fire','wf4DailyTick','wf4TryLocEvent','wf4PresentPending','wf4SeedFrags',
 'wf4FenIntroDone','wf4FenActionsAt','wf4FenPlay','wf4FenFarewellArm','wf4FenFarewellNode','wf4PresentFenFarewell',
 'applyRivalWf4Overrides86'].forEach(n => parts.push(extractFn(n)));
eval(parts.join('\n') + '; global.__W = { DAILY_EVENTS_WF4, WF4_CFG, WF4_FRAG_SEEDS, RIVAL_WF4_OVERRIDES, wf4Ensure, wf4BaseOk, wf4CondOk, wf4PickEvent, wf4Fire, wf4DailyTick, wf4TryLocEvent, wf4PresentPending, wf4SeedFrags, wf4FenActionsAt, wf4FenFarewellArm, wf4FenFarewellNode, wf4PresentFenFarewell, applyRivalWf4Overrides86 };');
const W = global.__W;

function freshS(day){
  return { dayIndex: day||0, money: 1000, stress: 30, stamina: 60, fame: 10, popularity: 10, acting: 10, charm: 10, stage: 10,
    mockRumors: [], mockDebts: [], mockCredits: [], story: { done:{}, flags:{} }, exodusFenSeeded: false, exodusFenFired: false };
}

/* (1) 事件表完整性 */
{
  const evs = W.DAILY_EVENTS_WF4;
  ok('事件總數 36', evs.length === 36);
  ok('id 唯一', new Set(evs.map(e=>e.id)).size === evs.length);
  ok('day/loc 各 18', evs.filter(e=>e.trig==='day').length === 18 && evs.filter(e=>e.trig==='loc').length === 18);
  let schemaBad = [];
  for(const e of evs){
    if(!e.title || !e.setting || !Array.isArray(e.beats) || e.beats.length < 1 || e.beats.length > 3) schemaBad.push(e.id+':beats');
    if(e.trig === 'loc' && !e.loc) schemaBad.push(e.id+':noloc');
    if(e.trig === 'day' && e.loc) schemaBad.push(e.id+':dayloc');
    const fxs = [...(e.choices||[]).map(c=>c.fx||{}), e.fx || {}];
    for(const fx of fxs) for(const k of Object.keys(fx)){
      const v = fx[k];
      if(!['money','stress','stamina','fame','popularity','acting','charm','stage','looks','iq'].includes(k)) schemaBad.push(e.id+':key'+k);
      if(k==='money' && (v < -80 || v > 120)) schemaBad.push(e.id+':money');
      if(k==='stress' && (v < -8 || v > 8)) schemaBad.push(e.id+':stress');
      if(k==='stamina' && (v < -6 || v > 6)) schemaBad.push(e.id+':stamina');
      if(['fame','popularity','acting','charm','stage'].includes(k) && (v < -2 || v > 2)) schemaBad.push(e.id+':attr');
    }
    if(!(e.choices && e.choices.length) && !(typeof e.tail === 'string' && e.tail)) schemaBad.push(e.id+':noend');
  }
  ok('schema＋fx 範圍全合規', schemaBad.length === 0);
  const allText = JSON.stringify(evs);
  ok('事件文案冇真人名／禁詞', !/(周潤發|劉德華|張國榮|陳百強|梅艷芳|VCD|互聯網|狗仔隊|1989年)/.test(allText));
  ok('事件含 Call 機＋大哥大題材', allText.includes('Call機') && allText.includes('大哥大'));
}

/* (2) 觸發閘 */
{
  S = freshS(100); _ys = { year:1990, season:'春' }; _tier = 0; _locked = _forced = _sick = false;
  ok('乾淨日子 baseOk', W.wf4BaseOk() === true);
  S.dayIndex = 385; ok('報紙頭版日（385）唔出事件', W.wf4BaseOk() === false);
  S.dayIndex = 1015; ok('報紙頭版日（1015）唔出事件', W.wf4BaseOk() === false);
  S.dayIndex = 100; _forced = true; ok('強制日（拍攝日）唔出事件', W.wf4BaseOk() === false); _forced = false;
  _sick = true; ok('病日唔出事件', W.wf4BaseOk() === false); _sick = false;
  _locked = true; ok('已結局唔出事件', W.wf4BaseOk() === false); _locked = false;
  S.wf4.lastDay = 99; ok('同上次觸發隔唔夠 2 日唔出', W.wf4BaseOk() === false);
  S.wf4.lastDay = 98; ok('隔夠 2 日回復', W.wf4BaseOk() === true);
}

/* (3) 每日種子擲＋呈現＋後果入帳 */
{
  S = freshS(0); _ys = { year:1990, season:'春' }; _tier = 1;
  let pendingDay = -1;
  for(let d = 0; d < 120 && pendingDay < 0; d++){
    S.dayIndex = d; W.wf4Ensure(); S.wf4.lastDay = -99;
    W.wf4DailyTick();
    if(S.wf4.pending) pendingDay = d;
  }
  ok('120 日內種子擲必中至少一次（pDay 唔餓死）', pendingDay >= 0);
  const ev = W.DAILY_EVENTS_WF4.find(e => e.id === S.wf4.pending);
  ok('pending 係 day 事件', !!ev && ev.trig === 'day');
  const stressBefore = S.stress, moneyBefore = S.money;
  const presented = W.wf4PresentPending();
  ok('pending 經 present 呈現', presented === true && S.wf4.pending === null);
  ok('呈現後 lastDay＝當日＋seen 記數', S.wf4.lastDay === pendingDay && (S.wf4.seen[ev.id]||0) >= 1);
  ok('播完返地圖（callback）', _mapReturns >= 1);
  // fx 入帳：modal stub 自動揀第一個選擇／純質地直接入帳，至少唔 crash 且數值冇出界
  ok('fx 入帳後數值冇出界', S.stress >= 0 && S.money >= 0 && Math.abs(S.stress - stressBefore) <= 8 && Math.abs(S.money - moneyBefore) <= 120);
  // 報紙日 tick 唔種 pending
  let newsPending = 0;
  for(const nd of [385, 532, 658, 744, 750, 1015, 1092]){
    S = freshS(nd); W.wf4Ensure(); S.wf4.lastDay = -99; W.wf4DailyTick(); if(S.wf4.pending) newsPending++;
  }
  ok('七個報紙日 tick 零 pending', newsPending === 0);
}

/* (4) 冷卻／once／cond 把關 */
{
  S = freshS(200); _ys = { year:1991, season:'夏' }; _tier = 2;
  const st = W.wf4Ensure();
  st.evDay['wf4_ev_st04'] = 190; // 10 日前出過
  let pickedCool = 0;
  for(let i = 0; i < 40; i++){ st.seen.__n = i; const p = W.wf4PickEvent('day', null); if(p && p.id === 'wf4_ev_st04') pickedCool++; }
  ok('45 日冷卻內唔重複揀同一事件', pickedCool === 0);
  st.evDay['wf4_ev_st04'] = 100; // 100 日前
  let pickedAfter = 0;
  for(let i = 0; i < 60; i++){ st.seen.__n = 100 + i; const p = W.wf4PickEvent('day', null); if(p && p.id === 'wf4_ev_st04') pickedAfter++; }
  ok('過冷卻後可再出', pickedAfter >= 1);
  const boss01 = W.DAILY_EVENTS_WF4.find(e => e.id === 'wf4_ev_boss01');
  const boss02 = W.DAILY_EVENTS_WF4.find(e => e.id === 'wf4_ev_boss02');
  const boss03 = W.DAILY_EVENTS_WF4.find(e => e.id === 'wf4_ev_boss03');
  ok('boss02 未識霞姐前 cond 唔過', W.wf4CondOk(boss02) === false);
  st.flags.boss_met = true;
  ok('boss02 識咗霞姐＋1991 後 cond 過', W.wf4CondOk(boss02) === true);
  _tier = 1; ok('boss03 tier 唔夠 cond 唔過', W.wf4CondOk(boss03) === false);
  _tier = 2; ok('boss03 tier 夠 cond 過', W.wf4CondOk(boss03) === true);
  st.seen['wf4_ev_boss01'] = 1;
  let bossPicked = 0;
  for(let i = 0; i < 60; i++){ st.seen.__n = 200 + i; const p = W.wf4PickEvent('loc', 'cafe_cha'); if(p && p.id === 'wf4_ev_boss01') bossPicked++; }
  ok('once 事件出過唔再揀', bossPicked === 0);
  // boss01 fire 設 boss_met 旗
  S = freshS(300); _ys = { year:1990, season:'秋' }; _tier = 0;
  W.wf4Fire(boss01, ()=>{});
  ok('boss01 播完設 boss_met 旗', S.wf4.flags.boss_met === true);
  // day03 moneyMax
  const day03 = W.DAILY_EVENTS_WF4.find(e => e.id === 'wf4_ev_day03');
  S.money = 1000; ok('day03 有錢唔出', W.wf4CondOk(day03) === false);
  S.money = 200; ok('day03 銀包見底先出', W.wf4CondOk(day03) === true);
  // home01 stressMin
  const home01 = W.DAILY_EVENTS_WF4.find(e => e.id === 'wf4_ev_home01');
  S.stress = 30; ok('home01 壓力低唔出', W.wf4CondOk(home01) === false);
  S.stress = 60; ok('home01 高壓先出', W.wf4CondOk(home01) === true);
}

/* (5) 碎片庫補完 */
{
  S = freshS(0); _ys = { year:1990, season:'冬' };
  W.wf4SeedFrags();
  const y90 = S.mockRumors.filter(r => r.id.startsWith('rumor_wf4_'));
  ok('1990 冬種入合資格碎片（≥3，含冬季限定）', y90.length >= 3 && y90.some(r => r.id === 'rumor_wf4_airport_winter'));
  const n0 = S.mockRumors.length;
  W.wf4SeedFrags();
  ok('補種冪等（第二次零新增）', S.mockRumors.length === n0);
  _ys = { year:1991, season:'春' }; W.wf4SeedFrags();
  _ys = { year:1992, season:'春' }; W.wf4SeedFrags();
  const all = S.mockRumors.filter(r => r.id.startsWith('rumor_wf4_'));
  ok('跨年累積碎片 ≥17', all.length >= 17);
  const txt = JSON.stringify(all);
  ok('碎片含 Call 機／傳呼 ≥4 條', (txt.match(/Call機|傳呼/g) || []).length >= 4);
  ok('碎片含大哥大 ≥3 條', (txt.match(/大哥大/g) || []).length >= 3);
}

/* (6) 芬姐小弧 */
{
  S = freshS(400); _ys = { year:1991, season:'夏' };
  ok('未播種前冇芬姐動作', W.wf4FenActionsAt('tvb_harbour').length === 0);
  S.exodusFenSeeded = true;
  ok('播種後清水灣出芬姐相識場', W.wf4FenActionsAt('tvb_harbour').length === 1);
  ok('其他地點唔出芬姐場', W.wf4FenActionsAt('cafe_cha').length === 0);
  S.exodusFenFired = true;
  ok('芬姐走咗之後相識場消失', W.wf4FenActionsAt('tvb_harbour').length === 0);
  S.exodusFenFired = false;
  W.wf4FenFarewellArm(true, true);
  ok('arm 送別戲帶帳本變體', !!S.wf4FenFarewell && S.wf4FenFarewell.wroteOff === true && S.wf4FenFarewell.exodused === true);
  const nodeBoth = W.wf4FenFarewellNode(S.wf4FenFarewell);
  const txtBoth = JSON.stringify(nodeBoth);
  ok('送別戲雙變體行齊（勾銷＋絕響）', txtBoth.includes('一筆勾銷') && txtBoth.includes('還唔到'));
  const nodeNone = W.wf4FenFarewellNode({ wroteOff:false, exodused:false });
  ok('送別戲中性變體（舊更紙）', JSON.stringify(nodeNone).includes('舊更紙'));
  ok('送別戲場景係啟德', nodeBoth.setting.includes('啟德'));
  _playedNodes = [];
  const presented = W.wf4PresentFenFarewell();
  ok('送別戲經 StoryPlay 呈現＋標完成', presented === true && _playedNodes.some(n => n.id === 'WF4_fen_farewell') && S.wf4.fenFarewellDone === true);
  ok('送別戲唔重播', W.wf4PresentFenFarewell() === false);
  // 舊檔 catch-up：fired 已 true、冇 arm → 中性變體補播
  S = freshS(500); S.exodusFenFired = true; _playedNodes = [];
  ok('舊檔 catch-up 補播送別戲', W.wf4PresentFenFarewell() === true && _playedNodes.some(n => n.id === 'WF4_fen_farewell'));
}

/* (7) 對手線覆寫 */
{
  const packPath = path.join(path.dirname(htmlPath), 'content', 'story_detail_rival_mentor.json');
  const pack = JSON.parse(fs.readFileSync(packPath, 'utf8'));
  const before = JSON.parse(JSON.stringify(pack));
  global.STORY_WIRE = { rival: pack };
  const applied = applyRivalWf4Overrides86();
  ok('覆寫命中 20 節點', applied === 20);
  const byId = {}; pack.nodes.forEach(n => byId[n.id] = n);
  const bById = {}; before.nodes.forEach(n => bById[n.id] = n);
  const four = Object.keys(W.RIVAL_WF4_OVERRIDES);
  ok('四線齊（ko/tsijun/fong/ho 各 5）', ['A_ko_','A_tsijun_','A_fong_','A_ho_'].every(p => four.filter(id => id.startsWith(p)).length === 5));
  let beatsOk = true, choiceOk = true;
  for(const id of four){
    const n = byId[id], b = bById[id];
    if(!n || !Array.isArray(n.beats) || n.beats.length < 5) beatsOk = false;
    if(JSON.stringify(n.choices) !== JSON.stringify(b.choices)) choiceOk = false;
    if(JSON.stringify(n.flags_written) !== JSON.stringify(b.flags_written)) choiceOk = false;
  }
  ok('20 節點 beats 增至 ≥5 拍', beatsOk);
  ok('choices／flags_written 逐字冇郁', choiceOk);
  const lei = byId['A_lei_meet'];
  ok('其餘線冇俾覆寫掂到', !!lei && JSON.stringify(lei.beats) === JSON.stringify(bById['A_lei_meet'].beats));
  ok('覆寫冪等（第二次 0）', applyRivalWf4Overrides86() === 0);
  const koTxt = JSON.stringify(byId['A_ko_meet'].beats);
  ok('改寫係廣東話口語（唔再書面語）', koTxt.includes('喇') && !koTxt.includes('那個位置我早已排好'));
}

/* (8) 舊檔兼容：冇 wf4 欄位唔 crash */
{
  S = freshS(50); delete S.wf4;
  let threw = false;
  try{ W.wf4Ensure(); W.wf4DailyTick(); W.wf4SeedFrags(); W.wf4PresentPending(); }catch(e){ threw = true; }
  ok('舊檔（冇 S.wf4）全套 entry 唔 crash', !threw && !!S.wf4);
}

console.log(fails.length ? ('FAILURES: ' + fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
