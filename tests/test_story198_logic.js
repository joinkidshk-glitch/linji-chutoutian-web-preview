// v20a198 STORY198・邏輯／真路徑測試
// B1：強制播優先於 WF4 地點事件（wf4TryLocEvent 有強制播 pending 嗰陣 defer，唔計 locTries；
//     boss01 本身唔郁，強制播完之後下一次入茶餐廳照出）
//     ——v20a193 互動（2026-11-13 第二次重驗）：v193 將 pLoc 0.20→0.03、cafe_cha 池 4→11 單，
//     B1 嘅根因對照／「之後照出」唔可以再寫死舊數（roll 0.1535、pick 落 boss01），已改寫做
//     頻率／池無關嘅寫法（池收窄＋day 127 確定性例子）；defer 主修斷言一隻字都冇郁。
// C1：死 code 已清（storyMapHintHtml／refreshMapHintStory 冇晒；storyMainProgressLine 保留）
// C2：鎖住插入幕出獨立鎖定行＋逐項解鎖條件；遠幕合併按段計（「第 4–6 幕」＋「第 7–17 幕」）
// C3：場景行唔再重複路線名（storySettingStripRoute198）
// 反證：喺 pristine（v191）index 上行——B1 守衛／C2 新行／C3 helper 唔存在，
//       對應組印 FAIL 後 exit 1，唔 crash。
// 用法：node tests/test_story198_logic.js（STORY198_DEBUG=1 印實際輸出）
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const storyPack = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'story_detail_c1_to_c17.json'), 'utf8'));
const gateStubPack = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'behavior_gate_c1_c5.json'), 'utf8'));
const DEBUG = !!process.env.STORY198_DEBUG;

let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }

function extractFn(decl){
  const i = html.indexOf(decl);
  if(i < 0) throw new Error('fn not found: ' + decl);
  let j = html.indexOf('{', i), depth = 0, k = j;
  for(; k < html.length; k++){
    if(html[k] === '{') depth++;
    else if(html[k] === '}'){ depth--; if(depth === 0){ k++; break; } }
  }
  return html.slice(i, k);
}
function extractConst(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('const not found: ' + name);
  let depth = 0, started = false;
  for(let k = i; k < html.length; k++){
    const ch = html[k];
    if(ch === '{' || ch === '['){ depth++; started = true; }
    else if(ch === '}' || ch === ']'){ depth--; if(started && depth === 0) return html.slice(i, k + 1) + ';'; }
    else if(ch === ';' && !started) return html.slice(i, k + 1);
  }
  throw new Error('const end not found: ' + name);
}
function extractIIFE(decl){
  const i = html.indexOf(decl);
  if(i < 0) throw new Error('iife not found: ' + decl);
  const end = html.indexOf('\n})();', i);
  if(end < 0) throw new Error('iife end not found: ' + decl);
  return html.slice(i, end) + '\n})();';
}

/* ---- C1：死 code 已清（純字串斷言，唔使 eval） ---- */
ok('(C1) storyMapHintHtml 宣告已拎走', html.indexOf('function storyMapHintHtml(){') < 0);
ok('(C1) refreshMapHintStory 宣告已拎走', html.indexOf('function refreshMapHintStory(){') < 0);
ok('(C1) window export 已拎走', html.indexOf('window.refreshMapHintStory') < 0);
ok('(C1) 呼叫點已拎走（唔留 refreshMapHintStory();）', html.indexOf('refreshMapHintStory();') < 0);
ok('(C1) storyMainProgressLine 保留（已測試嘅「下一幕」句式規格）', html.indexOf('function storyMainProgressLine(){') >= 0);
ok('(C1) storyMainProgressLine 仲行共用幕號', html.indexOf('storyActLabel(openMain.id)') >= 0 && html.indexOf('storyActLabel(id)') >= 0);

/* ---- B1：WF4 地點事件 vs 強制播（獨立 harness：StoryOC 用 stub，唔使成個 IIFE） ---- */
(function(){
  const need = ['function story165CanPlay(', 'function story165NextOpen(', 'function wf4TryLocEvent(',
    'function wf4Ensure(', 'function wf4BaseOk(', 'function wf4PickEvent(', 'function wf4Fire(',
    'function enc79StoryPendingAt(', 'function storyNodeLocId('];
  const missing = need.filter(d=>html.indexOf(d) < 0);
  if(missing.length){
    ['(B1) 強制播 pending 嗰陣 WF4 地點事件 defer', '(B1) boss01 之後照出', '(B1) A1 守衛仲有效',
     '(B1) 冇強制播嗰陣 seeded roll 照出 boss01'].forEach(n=>{ fails.push(n); console.log('FAIL ' + n + '（pristine：欠 ' + missing.join('、') + '）'); });
    return;
  }
  var __fired198 = [];
  function saveQ(){}
  function wf4PlayEvent(ev, doneCb){ __fired198.push(ev && ev.id); }
  var S = null;
  var StoryOC = {
    _open: [], _nodes: {},
    ensure(){},
    listOpen(){ return { open: this._open.slice(), locked: [], done: [], soft: [], phase: 'P1.5' }; },
    findNodeRaw(id){ return this._nodes[id] || null; },
    isDone(id){ return !!(S && S.story && S.story.done && S.story.done[id]); },
  };
  eval([
    extractConst('WF4_CFG').replace('const WF4_CFG =', 'var WF4_CFG ='),
    extractConst('DAILY_EVENTS_WF4').replace('const DAILY_EVENTS_WF4 =', 'var DAILY_EVENTS_WF4 ='),
    extractFn('function wf4Hash'),
    extractFn('function wf4Rand'),
    extractFn('function wf4NewsDay'),
    extractFn('function wf4YearSeason'),
    extractFn('function wf4Tier'),
    extractFn('function wf4Ensure'),
    extractFn('function wf4BaseOk'),
    extractFn('function wf4CondOk'),
    extractFn('function wf4PickEvent'),
    extractFn('function wf4Fire'),
    extractFn('function wf4TryLocEvent'),
    extractFn('function wf4EffPLoc'),
    extractFn('function story165NextOpen'),
    extractFn('function story165CanPlay'),
    extractFn('function storyNodeLocId'),
    extractFn('function enc79StoryPendingAt'),
  ].join('\n'));

  function freshS198(){
    return { dayIndex: 98, fame: 26, money: 14936, stress: 10, homeEditable: false, mapTips: {},
      wf4: undefined, story: { done: { C1: true, C2: true, C3: true, C4: true, C5: true }, flags: {}, rel: {}, routes: { route_film: true }, phase: 'P2', gigCount: 12 } };
  }
  function reset(openIds, nodes){
    S = freshS198();
    StoryOC._open = (openIds || []).map(id=>({ id: id }));
    StoryOC._nodes = nodes || {};
    __fired198.length = 0;
  }

  /* 根因對照（探針實測＋靜態計數）：v198 嗰陣 day 98 首次入茶餐廳，
     roll wf4loc:98:cafe_cha:1＝0.1535＜pLoc 0.20 通過，pool {cha03, cha04, boss01, st10}
     嘅 pick wf4pick:loc:cafe_cha:98:0＝0.6895 落 index 2＝boss01——必定打尖。
     v20a193 改咗兩樣嘢（用戶拍板，見 NOTES_V20A193 §3.1）：pLoc 0.20→0.03、
     cafe_cha 池 4→11 單——所以呢三個對照唔可以再寫死舊數，要改寫做頻率／池無關
     嘅寫法：(i) RNG 本身冇變（同一粒 seeded roll 值仲係 0.1535）；(ii) 將池收窄到
     得 boss01 嗰陣，pick／入場照樣出 boss01（證明 boss01 仲喺池、仲出到，唔係俾
     v193 清走咗）；(iii) 用 day 127（seeded roll 0.0256＜0.03）做「出到」嘅確定性
     例子。defer 本身（主修）嘅斷言一隻字都冇郁。 */
  reset([], {});
  var st0 = wf4Ensure();
  DAILY_EVENTS_WF4.filter(e=>e.loc==='cafe_cha' && e.id!=='wf4_ev_boss01').forEach(e=>{ st0.seen[e.id]=1; });
  ok('(B1) 根因：池收窄到得 boss01，pick 照落 boss01（boss01 仲喺池，唔係俾 v193 清走）',
    wf4PickEvent('loc', 'cafe_cha') && wf4PickEvent('loc', 'cafe_cha').id === 'wf4_ev_boss01');
  ok('(B1) 根因：seeded roll 值唔郁（0.1535，RNG 冇變）', Math.abs(wf4Rand('wf4loc:98:cafe_cha:1') - 0.1535) < 0.0001);
  ok('(B1) 根因：v193 pLoc 0.03 之下呢粒 roll 唔通過（頻率跌係 v193 拍板，唔係 defer 爛）',
    wf4Rand('wf4loc:98:cafe_cha:1') >= WF4_CFG.pLoc && WF4_CFG.pLoc === 0.03);
  reset([], {});
  S.dayIndex = 127; // seeded roll wf4loc:127:cafe_cha:1＝0.0256＜pLoc 0.03，確定性例子
  st0 = wf4Ensure();
  DAILY_EVENTS_WF4.filter(e=>e.loc==='cafe_cha' && e.id!=='wf4_ev_boss01').forEach(e=>{ st0.seen[e.id]=1; });
  ok('(B1) 對照：冇強制播嗰陣首次入茶餐廳照出 boss01', wf4TryLocEvent('cafe_cha') === true
    && __fired198.join(',') === 'wf4_ev_boss01' && S.wf4.seen.wf4_ev_boss01 === 1 && S.wf4.flags.boss_met === true);
  if(DEBUG) console.log('B1 control wf4:', JSON.stringify(S.wf4));

  /* 主修：C6F 強制播 pending（喺片場，唔喺茶餐廳——A1 守衛守唔住） */
  reset(['C6F'], { C6F: { id: 'C6F', locId: 'film_lion' } });
  const can = story165CanPlay();
  ok('(B1) 前設：C6F 強制播 pending', !!(can && can.id === 'C6F'));
  ok('(B1) 前設：A1 守衛喺茶餐廳唔着（C6F 喺片場）', enc79StoryPendingAt('cafe_cha') === false);
  ok('(B1) 前設：A1 守衛喺片場本身着（對照）', enc79StoryPendingAt('film_lion') === true);
  ok('(B1) 有強制播 pending 嗰陣 WF4 地點事件 defer（唔出 boss01）', wf4TryLocEvent('cafe_cha') === false
    && __fired198.length === 0 && (S.wf4.seen.wf4_ev_boss01 || 0) === 0);
  ok('(B1) defer 嗰次唔計 locTries（唔嘥當日事件額）', S.wf4.locTries === 0 && S.wf4.locDay === -99);
  if(DEBUG) console.log('B1 deferred wf4:', JSON.stringify(S.wf4));

  /* boss01 之後去向：強制播播完（open 清空）→ 下一次入茶餐廳照出。
     v193 之後 day 98 嗰粒 roll（0.1535）過唔到 pLoc 0.03，所以用返同一個
     確定性例子：day 127（roll 0.0256＜0.03）＋池收窄到得 boss01。 */
  StoryOC._open = [];
  ok('(B1) 前設：強制播播完之後 CanPlay 清空', story165CanPlay() === null);
  S.dayIndex = 127;
  DAILY_EVENTS_WF4.filter(e=>e.loc==='cafe_cha' && e.id!=='wf4_ev_boss01').forEach(e=>{ S.wf4.seen[e.id]=1; });
  ok('(B1) boss01 之後仲出：下一次入茶餐廳就出', wf4TryLocEvent('cafe_cha') === true
    && __fired198.join(',') === 'wf4_ev_boss01' && S.wf4.seen.wf4_ev_boss01 === 1 && S.wf4.locTries === 1);

  /* A1 守衛獨立有效：非主線事態喺同一地點 pending、但冇強制播嗰陣，WF4 照樣 defer */
  reset(['R_x'], { R_x: { id: 'R_x', locId: 'cafe_cha' } });
  ok('(B1) A1 對照：非主線事態喺茶餐廳 pending、冇強制播', story165CanPlay() === null && enc79StoryPendingAt('cafe_cha') === true);
  ok('(B1) A1 守衛仲有效（defer，唔計數）', wf4TryLocEvent('cafe_cha') === false && S.wf4.locTries === 0 && __fired198.length === 0);
})();

/* ---- C2＋C3：進度頁（v191 harness：真 StoryOC／BehaviorGate＋fixture＋插入節點） ---- */
(function(){
  if(html.indexOf('function storyActLabel(') < 0 || html.indexOf('function renderProgressPane71(') < 0){
    ['(C2) 鎖住插入幕出獨立行', '(C2) 遠幕按段合併', '(C3) 場景行唔重複路線名'].forEach(n=>{
      fails.push(n); console.log('FAIL ' + n + '（pristine：欠 storyActLabel／renderProgressPane71）');
    });
    return;
  }
  function makeEl(){
    const el = {
      children: [], style: {}, dataset: {}, hidden: false, disabled: false,
      textContent: '', innerHTML: '', value: '', title: '', className: '',
      classList: { add(){}, remove(){}, toggle(){}, contains(){ return false; } },
      setAttribute(){}, getAttribute(){ return null; }, removeAttribute(){},
      appendChild(c){ el.children.push(c); return c; },
      addEventListener(){}, removeEventListener(){},
      querySelector(){ return makeEl(); }, querySelectorAll(){ return []; },
      closest(){ return null; }, focus(){}, click(){}, remove(){},
    };
    return el;
  }
  function buildSrc(){
    const parts = [
      extractConst('START'),
      extractFn('function dateObj'),
      extractFn('function calendarSeason'),
      extractFn('function weekNumNow'),
      extractFn('function dualTrackNumbers'),
      extractFn('function readDualTracks'),
      extractFn('function syncDualTracks'),
      extractFn('function yearSeasonNow'),
      extractFn('function storyHintPack'),
      extractFn('function storyNodeLocId'),
      extractFn('function esc59'),
      extractFn('function calib60NodeTitle'),
      extractFn('function storyMainProgressLine'),
      extractFn('function storyActLabel'),
      extractFn('function storyActIsInsert'),
      extractFn('function prog71Esc'),
      extractFn('function prog71Title'),
      extractFn('function prog71LocName'),
      extractFn('function prog71GateItems'),
      extractFn('function prog71StubItems'),
      extractFn('function prog71Rows'),
      extractFn('function renderProgressPane71'),
      extractConst('STORY_GATE_3Y'),
      extractConst('STORY_LOC_SOFT'),
      extractConst('STORY_HINT_SOFT'),
      extractConst('STORY_TITLE_SOFT'),
      extractConst('CALIB60_NODE_WINDOWS'),
      extractConst('CALIB60_NODE_TITLES'),
      extractConst('LOCS'),
      extractIIFE('const BehaviorGate = (function(){'),
      extractIIFE('const StoryOC = (()=>{'),
    ];
    // C3 helper 喺 pristine 唔存在嗰陣用空 stub 頂住，等斷言乾淨 FAIL，唔喺 extractFn 拋錯 crash。
    if(html.indexOf('function storySettingStripRoute198(') >= 0){
      parts.push(extractFn('function storySettingStripRoute198'));
    } else {
      parts.push('function storySettingStripRoute198(s){ return String(s||""); }');
    }
    return parts.join('\n')
     .replace('const START =', 'var START =')
     .replace('const START =', 'var START =')
     .replace('const STORY_GATE_3Y =', 'var STORY_GATE_3Y =')
     .replace('const STORY_LOC_SOFT =', 'var STORY_LOC_SOFT =')
     .replace('const STORY_HINT_SOFT =', 'var STORY_HINT_SOFT =')
     .replace('const STORY_TITLE_SOFT =', 'var STORY_TITLE_SOFT =')
     .replace('const CALIB60_NODE_WINDOWS =', 'var CALIB60_NODE_WINDOWS =')
     .replace('const CALIB60_NODE_TITLES =', 'var CALIB60_NODE_TITLES =')
     .replace('const LOCS =', 'var LOCS =')
     .replace('const BehaviorGate =', 'var BehaviorGate =')
     .replace('const StoryOC =', 'var StoryOC =');
  }
  function freshSave(over){
    return Object.assign({
      dayIndex: 0, fame: 5, popularity: 3, acting: 18, stage: 14, vocal: 14, looks: 22, iq: 20, charm: 16,
      stress: 12, money: 12000, stamina: 75, industryCreditDelta: 0,
      flags: {}, npcs: {}, mockRumors: [], mockDebts: [], castingTags: [], inventory: {},
      calib60Missed: {},
      story: { done: {}, flags: {}, rel: {}, routes: {}, phase: 'P1', gigCount: 0 },
    }, over || {});
  }

  var window = {};
  var location = { search: '?softBehaviorGate=1' };
  var localStorage = { getItem: ()=>null, setItem: ()=>{}, removeItem: ()=>{} };
  var __els = {};
  var document = {
    getElementById(id){ return __els[id] || (__els[id] = makeEl()); },
    querySelector(){ return makeEl(); }, querySelectorAll(){ return []; },
    createElement(){ return makeEl(); }, body: makeEl(), addEventListener(){},
  };
  var STORY_WIRE = { main: null };
  var S = null;
  // C3 helper 喺 pristine 唔存在嗰陣用空 stub 頂住，等斷言乾淨 FAIL，唔喺 extractFn 拋錯 crash。
  var __src198 = buildSrc();
  eval(__src198);

  function loadGame(save){
    S = save; window.S = S;
    STORY_WIRE.main = JSON.parse(JSON.stringify(storyPack));
    STORY_WIRE.main.nodes.push(
      { id: 'C6F', title: '角落嗰張枱', phase: 'P1.5', locId: 'film_lion', playerOffer: true },
      { id: 'C18', title: '上岸路', phase: 'P2', locId: 'agency_ho', playerOffer: true },
      { id: 'C19', title: '賭枱邊', phase: 'P2', locId: 'film_lion', playerOffer: true }
    );
    BehaviorGate.loadStub_nodes_trigger(JSON.parse(JSON.stringify(gateStubPack)));
    StoryOC.ensure();
    return S;
  }
  function pane71(){
    renderProgressPane71();
    return (__els['progress-list'] && __els['progress-list'].innerHTML) || '';
  }
  function noBadNumbers(tag, pane){
    ok(tag + '：冇「第 20 幕」', pane.indexOf('第 20 幕') < 0);
    ok(tag + '：冇「第 18 幕」', pane.indexOf('第 18 幕') < 0);
    ok(tag + '：冇「第 19 幕」', pane.indexOf('第 19 幕') < 0);
  }

  /* ---- C3：場景行剝走路線名（helper 本身） ---- */
  ok('(C3) C6F 場景行剝走「電影線：」留返地點細節',
    storySettingStripRoute198('獅子山製片廠 · 1990 年 · 電影線：佈景板後面嗰個位') === '獅子山製片廠 · 1990 年 · 佈景板後面嗰個位');
  ok('(C3) C6 場景行剝走「電視線：」留返地點細節',
    storySettingStripRoute198('星河電視台飯堂 · 1990 年 · 電視線：角落嗰張枱') === '星河電視台飯堂 · 1990 年 · 角落嗰張枱');
  ok('(C3) 冇路線名嘅 setting 原樣唔郁', storySettingStripRoute198('何生事務所 · 1990 年 · 冬夜') === '何生事務所 · 1990 年 · 冬夜'
    && storySettingStripRoute198('') === '' && storySettingStripRoute198(null) === '');
  ok('(C3) 唔郁 setting 資料本身（節點原字仲有路線名）',
    html.indexOf('setting: "星河電視台飯堂 · 1988 年 · 電視線：角落嗰張枱"') >= 0
    && html.indexOf('setting: "獅子山製片廠 · 1988 年 · 電影線：佈景板後面嗰個位"') >= 0);

  /* ---- C2：film-route 第 15 週（C6F 已開放，C18／C19 鎖住） ---- */
  loadGame(freshSave({
    dayIndex: 98, fame: 30, industryCreditDelta: 30,
    story: { done: { C1: true, C2: true, C3: true, C4: true, C5: true }, flags: {}, rel: {}, routes: { route_film: true }, phase: 'P2', gigCount: 12 },
  }));
  const paneA = pane71();
  if(DEBUG) console.log('paneA198:', paneA);
  ok('(C2) C18 鎖住行見到（番外・1990 冬〈上岸路〉＋未開放）', paneA.indexOf('番外・1990 冬') >= 0 && paneA.indexOf('上岸路') >= 0 && paneA.indexOf('未開放') >= 0);
  ok('(C2) C18 鎖行講明解鎖條件（先完成 C5＋到第 48 週＋時窗）', paneA.indexOf('先完成第 5 幕〈采兒小訪題〉') >= 0 && paneA.indexOf('到第 48 週（而家第 15 週）') >= 0 && paneA.indexOf('時窗：1990 年冬') >= 0);
  ok('(C2) C19 鎖住行見到＋前置句在位（玩家面終於驗到）', paneA.indexOf('番外・1991 春') >= 0 && paneA.indexOf('賭枱邊') >= 0 && paneA.indexOf('先完成番外・1990 冬〈上岸路〉') >= 0);
  ok('(C2) C19 鎖行喺 C18 行之後、C7 行之前（次序跟播次序）', paneA.indexOf('番外・1990 冬') < paneA.indexOf('番外・1991 春') && paneA.indexOf('番外・1991 春') < paneA.indexOf('第 7 幕'));
  ok('(C2) 第 7 幕緊貼插入行之後搵得到', paneA.indexOf('第 7 幕') >= 0 && paneA.indexOf('番外・1991 春') < paneA.indexOf('第 7 幕'));
  ok('(C2) 合併行仲係「第 8–17 幕」（插入行之後先合併）', paneA.indexOf('第 8–17 幕') >= 0);
  noBadNumbers('(C2) Case A 進度頁', paneA);

  /* ---- C2：新遊戲——遠幕按段合併＋插入行常駐 ---- */
  loadGame(freshSave());
  const paneFresh = pane71();
  if(DEBUG) console.log('paneFresh198:', paneFresh);
  ok('(C2) 新遊戲遠幕按段合併：「第 4–6 幕」＋「第 7–17 幕」', paneFresh.indexOf('第 4–6 幕') >= 0 && paneFresh.indexOf('第 7–17 幕') >= 0);
  ok('(C2) 新遊戲唔再印舊合併行「第 4–17 幕」', paneFresh.indexOf('第 4–17 幕') < 0);
  ok('(C2) 新遊戲插入行之後緊貼「第 7–17 幕」合併行（C7 本身收咗入合併行，唔會走失）', paneFresh.indexOf('番外・1991 春') < paneFresh.indexOf('第 7–17 幕') && paneFresh.indexOf('第 4–6 幕') < paneFresh.indexOf('番外・1990 冬'));
  ok('(C2) 新遊戲一路數到 17（1、2、3、4–6、插入行、7、7–17）', paneFresh.indexOf('第 1 幕') >= 0 && paneFresh.indexOf('第 2 幕') >= 0 && paneFresh.indexOf('第 3 幕') >= 0);
  ok('(C2) 新遊戲 C6F 鎖行講啱條件（行電影線）', paneFresh.indexOf('行電影線') >= 0 && paneFresh.indexOf('行電視線') < 0);
  noBadNumbers('(C2) 新遊戲進度頁', paneFresh);

  /* ---- C2：得返一幕遠幕嗰陣印單幕，唔印「第 17–17 幕」 ---- */
  const done14 = {};
  for(let n = 1; n <= 14; n++) done14['C' + n] = true;
  loadGame(freshSave({
    dayIndex: 98, fame: 30, industryCreditDelta: 30,
    story: { done: done14, flags: {}, rel: {}, routes: { route_film: true }, phase: 'P2', gigCount: 12 },
  }));
  const paneSingle = pane71();
  if(DEBUG) console.log('paneSingle198:', paneSingle);
  ok('(C2) 得返一幕遠幕印「第 17 幕」唔印「第 17–17 幕」', paneSingle.indexOf('第 17–17 幕') < 0 && paneSingle.indexOf('第 17 幕') >= 0);
  noBadNumbers('(C2) 單一遠幕進度頁', paneSingle);

  /* ---- C2：主線行晒、得返插入幕未開嗰陣唔出合併行（v153 fallback 保留） ---- */
  const done17 = {};
  for(let n = 1; n <= 17; n++) done17['C' + n] = true;
  loadGame(freshSave({
    dayIndex: 900, fame: 80, industryCreditDelta: 60,
    story: { done: done17, flags: {}, rel: {}, routes: { route_tv: true }, phase: 'P5', gigCount: 60 },
  }));
  const paneDone = pane71();
  if(DEBUG) console.log('paneDone198:', paneDone);
  ok('(C2) 主線行晒唔出合併行（冇「–17 幕」倒轉區間）', paneDone.indexOf('–17 幕') < 0 && paneDone.indexOf('逐幕揭曉') < 0);
  noBadNumbers('(C2) 主線行晒進度頁', paneDone);
})();

console.log(fails.length ? ('STORY198 LOGIC: ' + fails.length + ' FAIL -> ' + fails.join(' | ')) : 'STORY198 LOGIC: ALL PASS');
process.exit(fails.length ? 1 : 0);
