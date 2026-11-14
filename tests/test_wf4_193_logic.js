// v20a193 WF4 once 硬規則邏輯測試：見過即封＋擴池＋頻率＋遷移＋抽乾優雅。
// 用法：node tests/test_wf4_193_logic.js [path-to-index.html]
// 反證：喺 pristine main（b3db32f）上行 → repeatDays 仲喺度、池得 36 單、
//   見過嘅事件 45 日後可再揀 → 多項乾淨 FAIL（唔 crash）。
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
/* ---- sandbox（同 test_wf4_86_logic.js 形狀） ---- */
let S;
let _ys = { year: 1990, season: '春' };
let _tier = 0;
function yearSeasonNow(){ return _ys; }
function enc79PlayerTier(){ return _tier; }
function ending78Locked(){ return false; }
function todayIsForcedDay(){ return false; }
function conseq61IsSickToday(){ return false; }
function saveQ(){}
function apply(fx){ const n=[]; for(const k of Object.keys(fx||{})){ const v=fx[k]; if(typeof v!=='number'||!v) continue; S[k]=Math.max(0,(S[k]||0)+v); n.push(k+v); } return n; }
function modal(h, buttons, opts){ if(buttons && buttons[0] && buttons[0].on) buttons[0].on(); }
function openLoc(id, opts){}
function goToMapForBrowse(){}
function enc79StoryPendingAt(){ return false; }
function wf4PresentFenFarewell(){ return false; } // wf4PresentPending 會 call（真機有定義，sandbox 要 stub）
const NEWS82_SRC = extractConst('NEWS82_EVENTS');
eval(NEWS82_SRC.replace('const NEWS82_EVENTS', 'global.NEWS82_EVENTS'));
const NEWS82_EVENTS = global.NEWS82_EVENTS;
const parts = [];
['DAILY_EVENTS_WF4','WF4_CFG'].forEach(n => parts.push(extractConst(n)));
['wf4Ensure','wf4Hash','wf4Rand','wf4NewsDay','wf4YearSeason','wf4Tier','wf4BaseOk','wf4CondOk','wf4PickEvent',
 'wf4ApplyFx','wf4Esc','wf4PlayEvent','wf4Fire','wf4DailyTick','wf4TryLocEvent','wf4PresentPending'].forEach(n => parts.push(extractFn(n)));
/* v203 helpers（pristine 冇）：抽唔到就用 stub 頂住，等斷言乾淨 FAIL，唔好成個測試 crash */
['wf4EffPDay','wf4EffPLoc'].forEach(n => {
  try { parts.push(extractFn(n)); }
  catch(e) { parts.push('function ' + n + '(){ return NaN; }'); }
});
eval(parts.join('\n') + '; global.__W = { DAILY_EVENTS_WF4, WF4_CFG, wf4Ensure, wf4BaseOk, wf4CondOk, wf4PickEvent, wf4Fire, wf4DailyTick, wf4TryLocEvent, wf4PresentPending, wf4EffPDay, wf4EffPLoc };');
const W = global.__W;
function freshS(day){
  return { dayIndex: day||0, money: 12000, stress: 50, stamina: 60, fame: 10, popularity: 10, acting: 10, charm: 10, stage: 10,
    mockRumors: [], mockDebts: [], mockCredits: [], story: { done:{}, flags:{} } };
}

/* (1) 頻率＋池 */
{
  ok('WF4_CFG pDay 0.03', W.WF4_CFG.pDay === 0.03);
  ok('WF4_CFG pLoc 0.03', W.WF4_CFG.pLoc === 0.03);
  ok('WF4_CFG gapDays 3', W.WF4_CFG.gapDays === 3);
  ok('WF4_CFG 冇 repeatDays（已刪）', !('repeatDays' in W.WF4_CFG));
  ok('WF4_CFG locTriesPerDay／pendingMaxAge 不變', W.WF4_CFG.locTriesPerDay === 3 && W.WF4_CFG.pendingMaxAge === 2);
  const evs = W.DAILY_EVENTS_WF4;
  ok('池 113 單（v20a203 Phase 2：72→113）', evs.length === 113);
  ok('day 池 48 單（v20a203：36→48）', evs.filter(e=>e.trig==='day').length === 48);
  ok('loc 池 65 單（v20a203：36→65）', evs.filter(e=>e.trig==='loc').length === 65);
  const byLoc = {};
  evs.filter(e=>e.trig==='loc').forEach(e=>{ (byLoc[e.loc]=byLoc[e.loc]||[]).push(e.id); });
  ok('每個地點 loc 池 ≥9（v20a203 Phase 2：每地點補到 9，cafe_cha 11 不變）',
    ['film_lion','film_cotton','film_harbour','tvb_longmen','tvb_harbour','tvb_kowloon'].every(l=>(byLoc[l]||[]).length===9)
    && (byLoc['cafe_cha']||[]).length === 11);
  ok('新事件 id 齊（v193：day05–16、st12–17、set11–25、cha05–07；v20a203：day17–28、set26–54）',
    ['wf4_ev_day05','wf4_ev_day16','wf4_ev_st12','wf4_ev_st17','wf4_ev_set11','wf4_ev_set25','wf4_ev_cha05','wf4_ev_cha07',
     'wf4_ev_day17','wf4_ev_day28','wf4_ev_set26','wf4_ev_set54']
      .every(id=>evs.some(e=>e.id===id)));
}

/* (2) once：逐單封印（全部 113 單，唔分 once 旗）——兩輪環境（1990 冬／tier 0／銀包見底／低壓
   ＋1992 夏／tier 2／高壓），等季節／年份／tier／銀包／壓力閘事件都有機會合資格，先驗封印 */
{
  const passes = [
    { ys: { year: 1990, season: '冬' }, tier: 0, money: 100, stress: 30 },
    { ys: { year: 1992, season: '夏' }, tier: 2, money: 12000, stress: 80 },
  ];
  let leaked = [];
  for(const pass of passes){
    S = freshS(200); _ys = pass.ys; _tier = pass.tier; S.money = pass.money; S.stress = pass.stress;
    const st = W.wf4Ensure();
    for(const ev of W.DAILY_EVENTS_WF4){
      st.seen[ev.id] = 1;
      S.dayIndex = 1200; // 快進到 1000 日後都唔應該再揀到
      for(let i = 0; i < 12; i++){
        st.seen.__n = i;
        const pDay = W.wf4PickEvent('day', null);
        const pLoc = ev.loc ? W.wf4PickEvent('loc', ev.loc) : null;
        if((pDay && pDay.id === ev.id) || (pLoc && pLoc.id === ev.id)) leaked.push(ev.id + '@' + pass.ys.year);
      }
      delete st.seen[ev.id];
    }
  }
  ok('113 單逐單見過即封（1000 日後都唔漏，兩輪環境）', leaked.length === 0);
}

/* (3) 抽乾嗰陣優雅：全池見晒 → pick 回 null，tick／入場唔 crash 唔出空卡 */
{
  S = freshS(500); _ys = { year:1992, season:'春' }; _tier = 2;
  const st = W.wf4Ensure();
  W.DAILY_EVENTS_WF4.forEach(e=>{ st.seen[e.id] = 1; });
  st.lastDay = -99;
  ok('全池見晒 day pick 回 null', W.wf4PickEvent('day', null) === null);
  ok('全池見晒 loc pick 回 null', W.wf4PickEvent('loc', 'tvb_longmen') === null);
  let threw = false;
  try{ W.wf4DailyTick(); W.wf4TryLocEvent('tvb_longmen'); W.wf4PresentPending(); }catch(e){ threw = true; }
  ok('抽乾後 tick／入場／present 唔 crash', !threw && !S.wf4.pending);
}

/* (4) pending 守 once：pending 嗰單已見過就清走唔彈 */
{
  S = freshS(100); _ys = { year:1990, season:'春' }; _tier = 1;
  const st = W.wf4Ensure();
  st.seen['wf4_ev_st04'] = 3; // 舊 save：呢單見過 3 次
  st.pending = 'wf4_ev_st04'; st.pendingDay = 100; st.lastDay = -99;
  const presented = W.wf4PresentPending();
  ok('pending 已見過 → 唔呈現＋清 pending', presented === false && st.pending === null);
  // 對照：pending 未見過照彈
  st.pending = 'wf4_ev_st01'; st.pendingDay = 100;
  ok('pending 未見過照常呈現', W.wf4PresentPending() === true);
}

/* (4b) Case C 根因：pending 指向已見過事件嗰陣，無論 base 條件點樣都要清走唔彈
   （守衛舊位排喺 baseOk 之後，報紙日／強制日／病日／gap 內會攔住清唔到） */
{
  const stale = () => {
    S = freshS(100); _ys = { year:1990, season:'春' }; _tier = 1;
    const st = W.wf4Ensure();
    st.seen['wf4_ev_set03'] = 21; // 舊 save：呢單見過 21 次
    st.pending = 'wf4_ev_set03'; st.pendingDay = 100; st.lastDay = -99;
    return st;
  };
  // (i) 報紙日：day 385 係 NEWS82 報紙日
  let st = stale(); S.dayIndex = 385; st.pendingDay = 385;
  ok('報紙日：stale pending 照清唔彈', W.wf4PresentPending() === false && st.pending === null && st.seen['wf4_ev_set03'] === 21);
  // (ii) 強制日
  st = stale(); todayIsForcedDay = () => true;
  ok('強制日：stale pending 照清唔彈', W.wf4PresentPending() === false && st.pending === null);
  todayIsForcedDay = () => false;
  // (iii) 病日
  st = stale(); conseq61IsSickToday = () => true;
  ok('病日：stale pending 照清唔彈', W.wf4PresentPending() === false && st.pending === null);
  conseq61IsSickToday = () => false;
  // (iv) gap 內（lastDay＝尋日，gap 1 < 3）
  st = stale(); st.lastDay = 99;
  ok('gap 內：stale pending 照清唔彈', W.wf4PresentPending() === false && st.pending === null);
  // (v) 對照：新鮮 pending（未見過）喺強制日唔彈之餘要保留，唔可以一併清走
  S = freshS(100); _ys = { year:1990, season:'春' }; _tier = 1;
  st = W.wf4Ensure();
  st.pending = 'wf4_ev_st01'; st.pendingDay = 100; st.lastDay = -99;
  todayIsForcedDay = () => true;
  ok('強制日：新鮮 pending 唔彈但保留', W.wf4PresentPending() === false && st.pending === 'wf4_ev_st01');
  todayIsForcedDay = () => false;
}

/* (4c) Case C 實駕：load 補跑 rest 日嗰陣 advanceDay tick 係第一個 WF4 觸發點——
   stale pending 要喺 tick 嗰陣清，唔等過期（pendingDay＝尋日，age 1 ≤ 2） */
{
  S = freshS(70); _ys = { year:1990, season:'春' }; _tier = 0;
  const st = W.wf4Ensure();
  st.seen['wf4_ev_set03'] = 21;
  st.pending = 'wf4_ev_set03'; st.pendingDay = 69; st.lastDay = 69; // gap 1：baseOk false，唔會順手擲新單
  W.wf4DailyTick();
  ok('DailyTick：stale pending 即清（唔等過期）', st.pending === null);
  // 對照：新鮮 pending 唔郁（tick 唔清未見過嘅 pending）
  st.pending = 'wf4_ev_st01'; st.pendingDay = 69;
  W.wf4DailyTick();
  ok('DailyTick：新鮮 pending 保留', st.pending === 'wf4_ev_st01');
}

/* (4d) Case C 實駕：入地點嗰陣 wf4TryLocEvent 係最後一個 WF4 觸發點——
   stale pending 唔可以一路閘住 loc 擲骰 */
{
  S = freshS(70); _ys = { year:1990, season:'春' }; _tier = 0;
  const st = W.wf4Ensure();
  st.seen['wf4_ev_set03'] = 21;
  st.pending = 'wf4_ev_set03'; st.pendingDay = 69; st.lastDay = 70; // lastDay＝今日：清完即回 false，唔擲新單
  ok('TryLocEvent：stale pending 即清', W.wf4TryLocEvent('cafe_cha') === false && st.pending === null);
  // 對照：新鮮 pending 照舊閘住入場擲骰（保留）
  st.pending = 'wf4_ev_st01'; st.pendingDay = 69;
  ok('TryLocEvent：新鮮 pending 照閘住＋保留', W.wf4TryLocEvent('cafe_cha') === false && st.pending === 'wf4_ev_st01');
}

/* (4e) v20a198 × v20a193 互動次序：wf4TryLocEvent 入面，清 stale pending 必須喺
   v198 嘅強制播 defer 守衛（story165CanPlay）之前——清 stale 係狀態清理，唔可以俾
   任何 early return 擋住。sandbox 冇 StoryOC，用 global stub 扮強制播 pending。
   前設：day 70、lastDay 67（gap 3，baseOk 過到）、報紙日唔係 70 號。 */
{
  const staleWithForced = () => {
    S = freshS(70); _ys = { year:1990, season:'春' }; _tier = 0;
    const st = W.wf4Ensure();
    st.seen['wf4_ev_set03'] = 21;
    st.pending = 'wf4_ev_set03'; st.pendingDay = 69; st.lastDay = 67; st.locDay = -99; st.locTries = 0;
    return st;
  };
  global.story165CanPlay = () => ({ id: 'C6F' }); // 強制播 pending（C6F 等播）
  let st = staleWithForced();
  ok('v198×v193：強制播 pending＋stale pending 同時存在，入場嗰次 stale pending 要清走',
    W.wf4TryLocEvent('cafe_cha') === false && st.pending === null);
  ok('v198×v193：嗰次 loc 事件照樣 defer（唔計 locTries）', st.locTries === 0);
  // 對照：新鮮 pending＋強制播 pending——pending 保留，loc 事件一樣 defer
  st = staleWithForced();
  st.pending = 'wf4_ev_st01'; delete st.seen['wf4_ev_set03'];
  ok('v198×v193 對照：新鮮 pending 保留＋defer（唔計 locTries）',
    W.wf4TryLocEvent('cafe_cha') === false && st.pending === 'wf4_ev_st01' && st.locTries === 0);
  // 對照：淨係強制播 pending（冇 WF4 pending）——v198 行為不變：defer，唔計 locTries
  st = staleWithForced();
  st.pending = null; delete st.seen['wf4_ev_set03'];
  ok('v198 行為不變：淨強制播 pending，入場 defer 唔計 locTries',
    W.wf4TryLocEvent('cafe_cha') === false && st.locTries === 0);
  // 對照：冇強制播 pending，stale pending 清完照入場擲骰（locTries 計 1，roll 過唔過唔理）
  global.story165CanPlay = () => null;
  st = staleWithForced();
  W.wf4TryLocEvent('cafe_cha');
  ok('v198×v193 對照：冇強制播，stale 清完照擲骰（locTries＝1）',
    st.pending === null && st.locTries === 1);
  delete global.story165CanPlay;
}

/* (5) 舊 save 遷移：舊 seen＋evDay 照封，冇 wf4 欄位唔 crash */
{
  S = freshS(300); _ys = { year:1991, season:'夏' }; _tier = 1;
  S.wf4 = { lastDay: 250, seen: { 'wf4_ev_set03': 21, 'wf4_ev_st04': 7, __n: 28 },
    pending: null, pendingDay: -99, flags: { boss_met: true },
    evDay: { 'wf4_ev_set03': 280, 'wf4_ev_st04': 290 }, // 舊冷卻紀錄，v193 唔再讀
    locDay: -99, locTries: 0, fenFarewellDone: false };
  const st = W.wf4Ensure();
  ok('舊 save seen 保留（set03 21 次照記）', st.seen['wf4_ev_set03'] === 21);
  let leakedOld = 0;
  for(let i = 0; i < 40; i++){ st.seen.__n = 1000 + i; const p = W.wf4PickEvent('loc', 'tvb_longmen'); if(p && p.id === 'wf4_ev_set03') leakedOld++; }
  ok('舊 save 見過嘅 set03 唔再出（電視線 21 次重複已封）', leakedOld === 0);
  S = freshS(50); delete S.wf4;
  let threw = false;
  try{ W.wf4Ensure(); W.wf4DailyTick(); W.wf4PresentPending(); }catch(e){ threw = true; }
  ok('冇 S.wf4 嘅舊 save 唔 crash', !threw && !!S.wf4);
}

/* (6) 三年模擬：用遊戲本身 WF4 code eval，四條路線 1095 日，重複率 0% */
{
  // 呢度用返同一套抽出嚟嘅 engine（wf4DailyTick／wf4TryLocEvent／wf4PresentPending）
  // 播種環境：壓力 50／銀包 $12000（穩陣玩家）、tier 隨日數升、報紙日為空
  // wf4Fire 會 call 真正嘅 wf4PlayEvent（modal stub 自動撳第一掣）；seen 差分即係當日出咗邊單。
  function runRoute(days, routeFn){
    S = freshS(0); _ys = { year: 1990, season: '春' }; _tier = 0;
    W.wf4Ensure();
    const fired = [];
    for(let d = 0; d < days; d++){
      S.dayIndex = d;
      const dt = new Date(1990, 0, 1 + d);
      _ys = { year: dt.getFullYear(), season: (dt.getMonth()+1>=3&&dt.getMonth()+1<=5)?'春':(dt.getMonth()+1>=6&&dt.getMonth()+1<=8)?'夏':(dt.getMonth()+1>=9&&dt.getMonth()+1<=11)?'秋':'冬' };
      _tier = d < 100 ? 0 : d < 400 ? 1 : 2;
      const snap = Object.assign({}, S.wf4.seen);
      // wf4PlayEvent 會開 modal（stub 自動撳第一掣）；fire 即記 seen，差分即係當日出咗邊單
      W.wf4DailyTick();
      for(const loc of routeFn(d)){ W.wf4TryLocEvent(loc); }
      W.wf4PresentPending();
      for(const id of Object.keys(S.wf4.seen)){
        if(id === '__n') continue;
        if((S.wf4.seen[id]||0) > (snap[id]||0)) fired.push({ day: d, id });
      }
    }
    return fired;
  }
  const routes = {
    A: d => [['film_lion','tvb_longmen','cafe_cha','film_cotton','film_harbour','tvb_harbour','tvb_kowloon'][d%7],
             ['film_lion','tvb_longmen','cafe_cha','film_cotton','film_harbour','tvb_harbour','tvb_kowloon'][(d+3)%7]],
    B: () => ['tvb_longmen','cafe_cha'],
    C: () => ['film_lion','film_cotton'],
    D: () => ['cafe_cha','cafe_cha'],
  };
  for(const [label, fn] of Object.entries(routes)){
    const fired = runRoute(1095, fn);
    const ids = fired.map(f=>f.id);
    const distinct = new Set(ids).size;
    ok(`三年模擬 ${label} 路線重複率 0%（${fired.length} 單，${distinct} 唔同）`,
      fired.length === distinct && fired.length > 0);
    // 每單最多見 1 次（once 鐵證）
    const maxSeen = Math.max(...Object.values(ids.reduce((a,id)=>{ a[id]=(a[id]||0)+1; return a; },{})));
    ok(`三年模擬 ${label} 路線每單最多見 1 次`, maxSeen === 1);
  }
}

/* (7) 新事件文案紀律：冇阿偉講者（NEW108 維持 8 單）、冇真人名／禁詞、fx 喺範圍內 */
{
  const NEW36 = W.DAILY_EVENTS_WF4.filter(e=>/^(wf4_ev_day0[5-9]|wf4_ev_day1[0-6]|wf4_ev_st1[2-7]|wf4_ev_set1[1-9]|wf4_ev_set2[0-5]|wf4_ev_cha0[5-7])$/.test(e.id));
  ok('v193 新事件數 36（不變）', NEW36.length === 36);
  const NEW41 = W.DAILY_EVENTS_WF4.filter(e=>/^(wf4_ev_day1[7-9]|wf4_ev_day2[0-8]|wf4_ev_set2[6-9]|wf4_ev_set3[0-9]|wf4_ev_set4[0-9]|wf4_ev_set5[0-4])$/.test(e.id));
  ok('v20a203 新事件數 41（day17–28＋set26–54）', NEW41.length === 41);
  const NEW77 = NEW36.concat(NEW41);
  ok('新事件冇阿偉做講者', NEW77.every(e=>!e.beats.some(b=>b.sp==='阿偉')));
  const txt = JSON.stringify(NEW77);
  ok('新事件文案冇真人名／禁詞', !/(周潤發|劉德華|張國榮|陳百強|梅艷芳|VCD|互聯網|狗仔隊|1989年)/.test(txt));
  let badFx = [];
  for(const e of NEW77){
    const fxs = [...(e.choices||[]).map(c=>c.fx||{}), e.fx||{}];
    for(const fx of fxs) for(const k of Object.keys(fx)){
      if(!['money','stress','stamina','fame','popularity','acting','charm','stage','looks','iq'].includes(k)) badFx.push(e.id+':key'+k);
    }
  }
  ok('新事件 fx 鍵全合規', badFx.length === 0);
  ok('新事件全部有香港質地（真地名／年代工種／片種關鍵詞）',
    NEW77.every(e=>/旺角|深水埗|油麻地|廟街|紅磡|清水灣|佐敦|港島|灣仔|維港|天星|啟德|片場|錄影廠|廣播|茶餐廳|冰室|大排檔|街市|卡拉OK|電車|渡輪|傳呼|Call機|屋邨|天台|電話亭|的士|涼茶|廠房|臨記|電視台|製片|影業|化妝|道具|開鏡/.test(e.setting + JSON.stringify(e.beats))));
}

console.log(fails.length ? ('FAILURES: ' + fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
