// v20a191 STORY191・邏輯／真路徑測試
// A 進度頁唔再將插入幕排做第 20 幕（C6F 跟 C6、番外錨季節）＋B 場景頂幕號同進度頁同一來源。
// 覆蓋：(a) C6F／C18／C19 新標籤（進度頁唔再見「第 20 幕」／「第 18 幕」／「第 19 幕」）
//       (b) 場景頂幕號同進度頁標籤同一來源（storyActLabel；進度頁行 label＝storyActLabel(id)，
//           StoryPlay head 呼叫點由靜態測試釘死）
//       (c) 遠幕合併＋逐項揭曉邏輯未爛（合併行位置／區間、鎖住插入幕唔觸發合併行）
//       (d) 舊存檔（已有 C6F done 旗）載入後進度頁顯示正確
//       (e) 前置句＋地圖下一幕提示同樣行共用幕號（C19 前置 C18、C6 路線後綴）
// 反證：喺 pristine main（v187）index 上行，storyActLabel 唔存在——
//       本檔唔 crash，逐組印 FAIL 後 exit 1。
// 用法：node tests/test_story191_logic.js（STORY191_DEBUG=1 印實際輸出）
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const storyPack = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'story_detail_c1_to_c17.json'), 'utf8'));
const gateStubPack = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'behavior_gate_c1_c5.json'), 'utf8'));
const DEBUG = !!process.env.STORY191_DEBUG;

let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }

if(html.indexOf('function storyActLabel(') < 0){
  ['(a) 插入幕新標籤', '(b) 同一來源', '(c) 遠幕合併＋逐項揭曉', '(d) 舊存檔 C6F done', '(e) 前置句＋地圖提示'].forEach(n=>{
    fails.push(n); console.log('FAIL ' + n + '（pristine：冇 storyActLabel）');
  });
  console.log('STORY191 LOGIC: ' + fails.length + ' FAIL');
  process.exit(1);
}

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
  return [
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
  ].join('\n')
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

(function(){
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
  eval(buildSrc());

  function loadGame(save){
    S = save; window.S = S;
    STORY_WIRE.main = JSON.parse(JSON.stringify(storyPack));
    /* v191：fixture 只含 C1–C17；補返真遊戲經 BR89／WF1 注入嘅 C6F／C18／C19 節點
       （id／phase／locId／title 跟真節點；playerOffer:true 對應實機狀態——
       調查報告實駕見到 C6F／C6 入 listOpen open 桶。閘由 STORY_GATE_3Y 評，
       唔靠節點 openConditions；進度頁標題由 STORY_TITLE_SOFT／calib60 出，唔靠呢度嘅 title）。 */
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

  /* ---- (a/b) 標籤函數本身 ---- */
  ok('(a) C1–C5／C7–C17 用順序號', storyActLabel('C1') === '第 1 幕' && storyActLabel('C5') === '第 5 幕'
    && storyActLabel('C7') === '第 7 幕' && storyActLabel('C17') === '第 17 幕');
  ok('(a) C6／C6F 係路線雙生、對稱後綴', storyActLabel('C6') === '第 6 幕・電視線' && storyActLabel('C6F') === '第 6 幕・電影線');
  ok('(a) C18／C19 係時間錨番外、唔佔順序號', storyActLabel('C18') === '番外・1990 冬' && storyActLabel('C19') === '番外・1991 春');
  ok('(a) 非主線 id 回空字串（場景頂唔出幕號）', storyActLabel('R_hiu_meet') === '' && storyActLabel('WF4_x') === ''
    && storyActLabel('C20') === '' && storyActLabel('') === '');
  ok('(b) 插入幕判定', storyActIsInsert('C6F') && storyActIsInsert('C18') && storyActIsInsert('C19')
    && !storyActIsInsert('C6') && !storyActIsInsert('C17'));

  /* ---- (a/c) 調查報告 Case A：film-route、第 15 週、C6F 已開放 ---- */
  loadGame(freshSave({
    dayIndex: 98, fame: 30, industryCreditDelta: 30,
    story: { done: { C1: true, C2: true, C3: true, C4: true, C5: true }, flags: {}, rel: {}, routes: { route_film: true }, phase: 'P2', gigCount: 12 },
  }));
  const rowsA = prog71Rows();
  ok('(b) prog71Rows 行次序跟播次序（C6、C6F、C18、C19、C7…）',
    rowsA.map(r=>r.id).join(',') === ['C1','C2','C3','C4','C5','C6','C6F','C18','C19','C7','C8','C9','C10','C11','C12','C13','C14','C15','C16','C17'].join(','));
  ok('(b) 每一行 label 都等於 storyActLabel(id)（同一來源）',
    rowsA.length === 20 && rowsA.every(r=>r.label === storyActLabel(r.id)));
  const paneA = pane71();
  if(DEBUG) console.log('paneA:', paneA);
  ok('(a) C6F 開放行係「第 6 幕・電影線：片場跟班」', paneA.indexOf('第 6 幕・電影線') >= 0 && paneA.indexOf('片場跟班') >= 0 && paneA.indexOf('已開放') >= 0);
  ok('(a) C6 行係「第 6 幕・電視線」（對稱，唔係齋「第 6 幕」）', paneA.indexOf('第 6 幕・電視線') >= 0);
  ok('(a) C6 行喺 C6F 行之前', paneA.indexOf('第 6 幕・電視線') < paneA.indexOf('第 6 幕・電影線'));
  noBadNumbers('(a) Case A 進度頁', paneA);
  ok('(c) 鎖住插入幕唔出獨立行（C18／C19 標題唔見）', paneA.indexOf('上岸路') < 0 && paneA.indexOf('賭枱邊') < 0);
  ok('(c) 遠幕合併行仲喺度、區間啱（第 8–17 幕）', paneA.indexOf('第 8–17 幕') >= 0 && paneA.indexOf('完成前面幕數後逐幕揭曉') >= 0);
  ok('(c) 合併行喺逐項行之後（唔會提早印喺 C7 上面）', paneA.indexOf('先完成第 5 幕〈采兒小訪題〉') >= 0
    && paneA.indexOf('先完成第 5 幕〈采兒小訪題〉') < paneA.indexOf('第 8–17 幕'));

  /* ---- (d) 舊存檔：C6F 已經 done（調查報告用戶狀態） ---- */
  loadGame(freshSave({
    dayIndex: 98, fame: 30, industryCreditDelta: 30,
    story: { done: { C1: true, C2: true, C3: true, C4: true, C5: true, C6F: true }, flags: {}, rel: {}, routes: { route_film: true }, phase: 'P2', gigCount: 12 },
  }));
  const paneD = pane71();
  if(DEBUG) console.log('paneD:', paneD);
  ok('(d) 舊存檔 C6F done 行係「第 6 幕・電影線 ✓ 已完成」', paneD.indexOf('第 6 幕・電影線') >= 0 && paneD.indexOf('✓ 已完成') >= 0);
  ok('(d) C6F done 行喺 C7 行之前', paneD.indexOf('第 6 幕・電影線') < paneD.indexOf('第 7 幕'));
  ok('(d) C6 未開放行喺 C6F done 行之前（雙生並排，對得返）', paneD.indexOf('第 6 幕・電視線') >= 0
    && paneD.indexOf('第 6 幕・電視線') < paneD.indexOf('第 6 幕・電影線'));
  noBadNumbers('(d) 舊存檔進度頁', paneD);

  /* ---- (a) C18 已開放（1990 冬、TV 線）——番外行喺 C6 同 C7 之間 ---- */
  loadGame(freshSave({
    dayIndex: 340, fame: 30, industryCreditDelta: 30,
    story: { done: { C1: true, C2: true, C3: true, C4: true, C5: true }, flags: {}, rel: {}, routes: { route_tv: true }, phase: 'P2', gigCount: 12 },
  }));
  const paneC18 = pane71();
  if(DEBUG) console.log('paneC18:', paneC18);
  ok('(a) C18 開放行係「番外・1990 冬：上岸路」', paneC18.indexOf('番外・1990 冬') >= 0 && paneC18.indexOf('上岸路') >= 0 && paneC18.indexOf('已開放') >= 0);
  ok('(a) C18 行喺 C6 行之後、C7 行之前', paneC18.indexOf('第 6 幕・電視線') < paneC18.indexOf('番外・1990 冬')
    && paneC18.indexOf('番外・1990 冬') < paneC18.indexOf('第 7 幕'));
  ok('(a) C19 鎖住唔出獨立行（賭枱邊唔見）', paneC18.indexOf('賭枱邊') < 0);
  noBadNumbers('(a) C18 開放進度頁', paneC18);

  /* ---- (e) 前置句：C19 前置 C18 用番外標籤 ---- */
  loadGame(freshSave({
    dayIndex: 500, fame: 40, industryCreditDelta: 40,
    story: { done: { C1: true, C2: true, C3: true, C4: true, C5: true, C18: true }, flags: {}, rel: {}, routes: { route_tv: true }, phase: 'P2', gigCount: 20 },
  }));
  const gateC19 = prog71GateItems('C19') || [];
  const gateC19Txt = gateC19.map(it=>it.text).join('｜');
  if(DEBUG) console.log('gateC19:', gateC19Txt);
  ok('(e) C19 前置句係「先完成番外・1990 冬〈上岸路〉」', gateC19Txt.indexOf('先完成番外・1990 冬〈上岸路〉') >= 0);
  ok('(e) C19 前置句冇「第 18 幕」', gateC19Txt.indexOf('第 18 幕') < 0);

  /* ---- (e) 地圖下一幕提示：同一 label 來源 ---- */
  loadGame(freshSave({
    dayIndex: 66,
    story: { done: { C1: true, C2: true, C3: true, C4: true, C5: true }, flags: {}, rel: {}, routes: { route_tv: true }, phase: 'P2', gigCount: 9 },
  }));
  const lineE = storyMainProgressLine();
  if(DEBUG) console.log('lineE:', lineE);
  ok('(e) 地圖提示指向「第 6 幕・電視線〈飯堂閒角〉」', lineE.indexOf('第 6 幕・電視線〈飯堂閒角〉') >= 0);
  ok('(e) 地圖提示冇舊寫法「第 6 幕〈飯堂閒角〉」', lineE.indexOf('第 6 幕〈飯堂閒角〉') < 0);

  /* ---- (c) 遠幕合併＋逐項揭曉：新遊戲 ---- */
  loadGame(freshSave());
  const paneFresh = pane71();
  if(DEBUG) console.log('paneFresh:', paneFresh);
  ok('(c) 新遊戲遠幕合併一行「第 4–17 幕」', paneFresh.indexOf('第 4–17 幕') >= 0 && paneFresh.indexOf('完成前面幕數後逐幕揭曉') >= 0);
  ok('(c) 新遊戲冇倒轉區間', paneFresh.indexOf('第 18–17 幕') < 0 && paneFresh.indexOf('第 20–17 幕') < 0);
  ok('(c) 新遊戲插入幕標題全唔見（防劇透維持）', paneFresh.indexOf('片場跟班') < 0 && paneFresh.indexOf('上岸路') < 0 && paneFresh.indexOf('賭枱邊') < 0);
  ok('(c) 新遊戲 C6 標題唔見（防劇透維持）', paneFresh.indexOf('飯堂閒角') < 0);
  noBadNumbers('(c) 新遊戲進度頁', paneFresh);
})();

console.log(fails.length ? ('STORY191 LOGIC: ' + fails.length + ' FAIL -> ' + fails.join(' | ')) : 'STORY191 LOGIC: ALL PASS');
process.exit(fails.length ? 1 : 0);
