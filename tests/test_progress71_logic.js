// v20a71 PROGRESS71・邏輯／真路徑測試
// 段一（gate-on）：真 storyMainProgressLine 組句——多分支×多幕：
//   A1 新遊戲（gate-off 截圖情境嘅 gate-on 版）A2 用戶截圖本尊情境（C2 未開，通告 0／3）
//   A3 中段 C6（週數差額）A4 全通近尾 C17 已開放分支 A5 C3「先完成上一幕」分支
//   斷言：完整句（以「。」收尾）、冇「開咗去…播」拼裝、冇「即將」碎片頭、
//   冇「 · 」串燒、差額數字同地點名正確。
// 段二（gate-off）：fallback 路徑（progressToward 唔行嗰陣）組句同樣要完整——
//   用戶 12:44 截圖正正係呢條路徑出嘅。
// 段三（gate-on）：真 renderProgressPane71——新遊戲／中段／錯過登記三態：
//   逐項條件連即時進度、✓ 跟住存檔變、防劇透（遠幕冇標題冇條件）、
//   已完成／已開放／已錯過狀態分明、成頁冇 1988/1989、冇關海媚個名。
// 用法：node tests/test_progress71_logic.js（PROGRESS71_DEBUG=1 印實際輸出）
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const storyPack = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'story_detail_c1_to_c17.json'), 'utf8'));
const gateStubPack = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'behavior_gate_c1_c5.json'), 'utf8'));
const DEBUG = !!process.env.PROGRESS71_DEBUG;

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
function extractBlock(marker, endMarker){
  const a = html.indexOf(marker);
  const b = html.indexOf(endMarker);
  if(a < 0 || b < 0 || b <= a) throw new Error('block not found: ' + marker);
  return html.slice(a, b);
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
function sentenceChecks(tag, line){
  ok(tag + '：非空字串', typeof line === 'string' && line.length > 0);
  ok(tag + '：完整句以「。」收尾', /。$/.test(line));
  ok(tag + '：冇「開咗去…播」拼裝碎片', line.indexOf('開咗去') < 0);
  ok(tag + '：冇「即將」碎片頭', line.indexOf('即將') < 0);
  ok(tag + '：冇「 · 」碎片串燒', line.indexOf(' · ') < 0);
}

/* ================= 段一＋段三：gate-on ================= */
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
    BehaviorGate.loadStub_nodes_trigger(JSON.parse(JSON.stringify(gateStubPack)));
    StoryOC.ensure();
    return S;
  }
  function pane71(){
    renderProgressPane71();
    return (__els['progress-list'] && __els['progress-list'].innerHTML) || '';
  }

  /* ---- A1：新遊戲 ---- */
  loadGame(freshSave());
  const a1 = storyMainProgressLine();
  if(DEBUG) console.log('A1:', a1);
  sentenceChecks('A1 新遊戲進度行', a1);

  /* ---- A2：用戶截圖本尊情境（C1 已完成、C2 未開、通告 0） ---- */
  loadGame(freshSave({
    dayIndex: 8,
    story: { done: { C1: true }, flags: {}, rel: {}, routes: {}, phase: 'P1', gigCount: 0 },
  }));
  const a2 = storyMainProgressLine();
  if(DEBUG) console.log('A2:', a2);
  sentenceChecks('A2 C2 未開進度行', a2);
  ok('A2：句頭係「下一幕第 2 幕〈留人脈／趕通告〉未開——」', a2.indexOf('下一幕第 2 幕〈留人脈／趕通告〉未開——') === 0);
  ok('A2：通告差額正確（仲差 3 張・而家 0／3）', a2.indexOf('通告仲差 3 張（而家 0／3）') >= 0);
  ok('A2：週數差額正確（未到第 4 週）', a2.indexOf('未到第 4 週') >= 0);
  ok('A2：尾句講明去星河電視台觸發', /去星河電視台就會觸發。$/.test(a2));

  /* ---- A3：中段 C6（三年版閘節點） ----
     數據現實：progressToward 只覆蓋 stub C1–C5（byId trigger），C6+ 喺 hint 層
     本來就冇差額數據（判定／數據來源唔改係本包紀律）——hint 只出誠實完整句，
     唔虛報「條件夠晒」；C6 逐項差額（週數／路線）喺進度頁用 evalGate3Y 列（B2 驗）。 */
  loadGame(freshSave({
    dayIndex: 66,
    story: { done: { C1: true, C2: true, C3: true, C4: true, C5: true }, flags: {}, rel: {}, routes: { route_tv: true }, phase: 'P2', gigCount: 9 },
  }));
  const a3 = storyMainProgressLine();
  if(DEBUG) console.log('A3:', a3);
  sentenceChecks('A3 C6 未開進度行', a3);
  ok('A3：指向第 6 幕〈飯堂閒角〉', a3.indexOf('第 6 幕〈飯堂閒角〉') >= 0);
  ok('A3：冇差額數據嗰陣唔虛報「條件已經夠晒」', a3.indexOf('條件已經夠晒') < 0);
  ok('A3：尾句講明去星河電視台觸發', /去星河電視台就會觸發。$/.test(a3));

  /* ---- A4：已開放分支喺段一b（獨立 harness、單節點 pack 構造） ---- */

  /* ---- A4b：主線全完（C1–C16 done）→ 進度行收起（結局由結局閘處理，唔出假句） ---- */
  const doneAll = {};
  for(let n = 1; n <= 16; n++) doneAll['C' + n] = true;
  loadGame(freshSave({
    dayIndex: 730, fame: 80,
    story: { done: doneAll, flags: {}, rel: {}, routes: { route_tv: true }, phase: 'P5', gigCount: 60 },
  }));
  const a4b = storyMainProgressLine();
  if(DEBUG) console.log('A4b:', JSON.stringify(a4b));
  ok('A4b：主線全完嗰陣進度行係空字串', a4b === '');

  /* ---- A5：C3「先完成上一幕」分支 ---- */
  loadGame(freshSave({
    dayIndex: 30,
    story: { done: { C1: true }, flags: {}, rel: {}, routes: {}, phase: 'P1', gigCount: 0 },
  }));
  /* C2 條件齊（週數／通告數）但未播 → 下一幕目標轉 C3，remain 首項「先完成上一幕」 */
  S.flags.tvb_rules_gossip = true;
  S.mockRumors.push({ id: 'tvb_rules_gossip', source: '何生事務所', title: '電視城廠景生存守則', text: 'x', state: 'normal' });
  S.story.gigCount = 5;
  const a5 = storyMainProgressLine();
  if(DEBUG) console.log('A5:', a5);
  sentenceChecks('A5 進度行', a5);
  ok('A5：指向第 3 幕而且係完整子句「要先完成上一幕」', a5.indexOf('第 3 幕') >= 0 && a5.indexOf('要先完成上一幕') >= 0);

  /* ---- B1：進度頁・新遊戲 ---- */
  loadGame(freshSave());
  const b1 = pane71();
  if(DEBUG) console.log('B1 len:', b1.length);
  ok('B1：第 1 幕已開放＋標題＋觸發地點', b1.indexOf('第 1 幕') >= 0 && b1.indexOf('先學做動作戲') >= 0 && b1.indexOf('已開放') >= 0 && b1.indexOf('去何生事務所就會觸發') >= 0);
  ok('B1：第 2 幕逐項——前置旗未達', b1.indexOf('先完成第 1 幕〈先學做動作戲／先賺〉') >= 0);
  ok('B1：第 2 幕逐項——週數連即時進度（第 4 週・而家第 1 週）', b1.indexOf('到第 4 週（而家第 1 週）') >= 0);
  ok('B1：第 2 幕逐項——通告連即時進度（0／3）', b1.indexOf('接通告 0／3 張') >= 0);
  ok('B1：第 2 幕逐項——傳聞未達', b1.indexOf('聽到傳聞：') >= 0);
  ok('B1：第 3 幕（第二幕未開放）照列逐項', b1.indexOf('茶餐廳度橋') < 0 && b1.indexOf('先完成第 2 幕〈留人脈／趕通告〉') >= 0);
  ok('B1：防劇透——第 4 幕起冇標題', b1.indexOf('何生拒單') < 0 && b1.indexOf('采兒小訪題') < 0 && b1.indexOf('飯堂閒角') < 0);
  /* v20a105 S-45：遠幕 boilerplate 合併做一行「第 X–17 幕…逐幕揭曉」，唔再逐幕重複 */
  ok('B1：防劇透——遠幕合併一行', b1.indexOf('第 4–17 幕') >= 0 && b1.indexOf('完成前面幕數後逐幕揭曉') >= 0 && b1.indexOf('完成前面嘅幕之後，呢幕嘅標題同條件會逐項列出') < 0);
  ok('B1：成頁冇舊年份', b1.indexOf('1988') < 0 && b1.indexOf('1989') < 0);
  ok('B1：成頁冇關海媚個名', b1.indexOf('關海媚') < 0);

  /* ---- B2：進度頁・中段（C1–C5 已完成、第 6 幕部分達標） ----
     第 13 週：電視線已行（✓）、週數未到 15（○）——部分達標先驗到逐項跟住變。
     （若週數都達標，C6 會係真開放、唔再係 locked 逐項，嗰態由 B1 open 行覆蓋。） */
  loadGame(freshSave({
    dayIndex: 90, fame: 30, industryCreditDelta: 30,
    story: { done: { C1: true, C2: true, C3: true, C4: true, C5: true }, flags: {}, rel: {}, routes: { route_tv: true }, phase: 'P2', gigCount: 12 },
  }));
  const b2 = pane71();
  if(DEBUG) console.log('B2 credit:', syncDualTracks(S).industryCredit);
  ok('B2：已完成幕數正確（✓ 已完成 ×5）', (b2.match(/✓ 已完成/g) || []).length === 5);
  ok('B2：第 6 幕逐項——電視線已達標（✓）', /<li class="ok">✓ 行電視線<\/li>/.test(b2));
  ok('B2：第 6 幕逐項——週數未達連即時進度（第 15 週・而家第 13 週）', /<li class="no">○ 到第 15 週（而家第 13 週）<\/li>/.test(b2));
  ok('B2：第 7 幕逐項——前置 C5 已達標（✓）', /<li class="ok">✓ 先完成第 5 幕〈采兒小訪題〉<\/li>/.test(b2));
  ok('B2：第 7 幕逐項——信用已達標連即時進度', /<li class="ok">✓ 業內信用多於 20（而家 \d+）<\/li>/.test(b2));
  ok('B2：第 7 幕逐項——時窗未到（1991 年夏）', b2.indexOf('時窗：1991 年夏') >= 0);
  ok('B2：防劇透——第 8 幕起冇標題', b2.indexOf('茶餐廳度橋') < 0 && b2.indexOf('年尾追數') < 0);

  /* ---- B3：進度頁・錯過登記 ---- */
  const done14 = {};
  for(let n = 1; n <= 14; n++) done14['C' + n] = true;
  delete done14.C15;
  loadGame(freshSave({
    dayIndex: 800, fame: 60, industryCreditDelta: 40,
    calib60Missed: { C15: { title: '高危替身', whenLabel: '1992 年春', week: 118 } },
    story: { done: done14, flags: {}, rel: {}, routes: { route_tv: true }, phase: 'P3', gigCount: 40 },
  }));
  const b3 = pane71();
  ok('B3：第 15 幕顯示已錯過＋時窗標籤', b3.indexOf('高危替身') >= 0 && b3.indexOf('已錯過') >= 0 && b3.indexOf('1992 年春') >= 0);
  ok('B3：成頁冇舊年份', b3.indexOf('1988') < 0 && b3.indexOf('1989') < 0);
})();

/* ================= 段二：gate-off fallback ================= */
(function(){
  var window = {};
  var location = { search: '' };
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

  S = freshSave({
    story: { done: { C1: true }, flags: {}, rel: {}, routes: {}, phase: 'P1', gigCount: 0 },
  });
  window.S = S;
  STORY_WIRE.main = JSON.parse(JSON.stringify(storyPack));
  StoryOC.ensure();
  const line = storyMainProgressLine();
  if(DEBUG) console.log('GATEOFF:', line);
  sentenceChecks('段二 gate-off 進度行', line);
  ok('段二：指向第 2 幕〈留人脈／趕通告〉', line.indexOf('第 2 幕〈留人脈／趕通告〉') >= 0);
  ok('段二：冇數據嗰陣唔虛報「條件夠晒」', line.indexOf('條件已經夠晒') < 0);
})();

/* ================= 段一b：A4 已開放分支（單節點 pack） =================
   C 鏈係前置串連，正常存檔入面「有 open 又冇 locked C」幾乎唔會出現
   （下一幕永遠 locked 住；C17 係結局節點，listOpen 唔入任何桶）。
   用得一個主線節點嘅 pack 構造：C1 已開放、冇 locked → 行已開放分支。 */
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
  S = freshSave(); window.S = S;
  STORY_WIRE.main = { nodes: [JSON.parse(JSON.stringify(storyPack.nodes.find(n => n.id === 'C1')))] };
  BehaviorGate.loadStub_nodes_trigger(JSON.parse(JSON.stringify(gateStubPack)));
  StoryOC.ensure();
  const a4 = storyMainProgressLine();
  if(DEBUG) console.log('A4:', a4);
  sentenceChecks('A4 C1 已開放進度行', a4);
  ok('A4：已開放完整句（第 1 幕〈先學做動作戲／先賺〉已經開咗）', a4.indexOf('第 1 幕〈先學做動作戲／先賺〉已經開咗') >= 0);
  ok('A4：講明去何生事務所觸發', a4.indexOf('去何生事務所就會觸發。') >= 0);
})();

/* ================= 段四：PART3B 訓練選擇器 =================
   跟 test_ux68_logic 先例：成個 UX68 block 抽取（ux68ParseGainTable 內有含 } 嘅
   正則，逐函數 brace 抽取會截斷）；斷言 driver 同 block 同一 eval，共享 let 狀態。 */
(function(){
  var window = {};
  var __prefs = {};
  var loadPrefs = function(){ return __prefs; };
  var setPref = function(k, v){ __prefs[k] = v; };
  var document = { getElementById: () => null, querySelectorAll: () => [], createElement: () => ({}) };
  var S = null;
  const DRIVER = `
    ;(function(){
      function freshS(over){
        return Object.assign({
          dayIndex: 0, fame: 5, acting: 18, stage: 14, vocal: 14, looks: 22, iq: 20, charm: 16,
          stress: 12, money: 12000, stamina: 75, popularity: 3,
          enrolled: {}, trainCount: {}, homeEditable: true,
          story: { done: {}, flags: {}, rel: {}, routes: {}, phase: 'P1', gigCount: 0 },
        }, over || {});
      }
      /* P1：新遊戲（冇報名）——v20a73 改版（用戶 2026-11-10 15:16 拍板）：
         未報名只出一句純文字、未開放成課隱藏、成個 picker 零跳轉。
         （v71 舊斷言「未報名課有前往報名／未開放課出解鎖條件」已被用戶推翻，改版至此。） */
      S = freshS(); ux68GuideStat = '';
      const p1 = train71PickerHtml('fill');
      ok('P1：有按數值 chips＋主修分組', p1.indexOf('data-gstat="acting"') >= 0 && p1.indexOf('主修 · 主升演技') >= 0);
      /* v20a74 改版：主攻目標掣隨功能移除（用戶 2026-11-10 16:06 拍板）；
         舊斷言「目標入口喺頂」改為驗冇掣冇字樣；喺 v73 index 上行會 FAIL（反證）。 */
      ok('P1(v74)：預設開演技組＋冇主攻掣／冇「主攻」字樣', p1.indexOf('data-gtgt') < 0 && p1.indexOf('主攻') < 0);
      ok('P1：冇已報名課程嗰陣冇排入掣', p1.indexOf('data-t71pick') < 0);
      ok('P1(v73)：未報名課只出一句純文字（課名＋未報名——去…報名）',
         p1.indexOf('train73-note') >= 0 && /「.+」未報名——去 .+ 報名。/.test(p1));
      ok('P1(v73)：未報名課唔出卡身', p1.indexOf('t70-card') < 0);
      ok('P1(v73)：成個 picker 零跳轉（冇 data-gloc／冇「前往」字眼）',
         p1.indexOf('data-gloc') < 0 && p1.indexOf('前往') < 0);
      ok('P1(v73)：未開放課成課隱藏（課名唔出現）', p1.indexOf('進階演技') < 0);
      ok('P1(v73)：未開放條件文字唔出現', p1.indexOf('演技訓練累計 3 堂') < 0);
      ok('P1(v73)：零報名有純文字總說明（唔係死胡同）', p1.indexOf('你仲未報名任何課程') >= 0);

      /* P2：報咗演技入門 → 排入掣出現；未開放課仍然冇排入掣 */
      S = freshS({ enrolled: { train_acting: true }, trainCount: { train_acting: 2 } });
      const p2 = train71PickerHtml('fill');
      ok('P2：已報名課有排入掣（全日）', p2.indexOf('data-t71pick="train_acting"') >= 0 && p2.indexOf('全日排呢堂') >= 0);
      ok('P2：未開放課冇排入掣', p2.indexOf('data-t71pick="train_acting_mid"') < 0);
      ok('P2：已報名徽章＋已練次數', p2.indexOf('已開放') >= 0 && p2.indexOf('已練 2 次') >= 0);
      ok('P2(v73)：有已報名就唔出零報名總說明', p2.indexOf('你仲未報名任何課程') < 0);
      ok('P2(v73)：未開放課名仍然隱藏', p2.indexOf('進階演技') < 0);
      ok('P2(v73)：已報名卡冇加練跳轉（零 data-gloc／冇「加練」）',
         p2.indexOf('data-gloc') < 0 && p2.indexOf('加練') < 0);

      /* P3(v74)：主攻目標成個移除（用戶 2026-11-10 16:06 拍板）——picker 預設改用
         session 上次睇開嗰組（ux68GuideStat），唔再讀 prefs 目標。
         （v71 舊斷言「prefs 設目標 → 預設開嗰組＋目標掣顯示已設定」隨功能移除改版；
         喺 v73 index 上行會 FAIL，係反證。） */
      ux68GuideStat = 'vocal';
      S = freshS();
      const p3 = train71PickerHtml('day');
      ok('P3(v74)：重開 picker 記住 session 上次組（歌藝組）', p3.indexOf(COURSE_DEFS.train_vocal.name) >= 0 && p3.indexOf('主修 · 主升歌藝') >= 0);
      ok('P3(v74)：picker 冇主攻掣、冇「目標」chip 標記', p3.indexOf('data-gtgt') < 0 && p3.indexOf('guide68-tgtbtn') < 0 && p3.indexOf('class="gt"') < 0);

      /* P4：逐日唯讀（唔係編輯態）——已報名課都唔出排入掣 */
      ux68GuideStat = '';
      S = freshS({ enrolled: { train_acting: true }, homeEditable: false });
      const p4 = train71PickerHtml('day');
      ok('P4：唯讀嗰陣冇排入掣', p4.indexOf('data-t71pick') < 0);
      ok('P4：唯讀嗰陣有說明（編輯行程嗰陣排）', p4.indexOf('編輯行程嗰陣排呢堂') >= 0);

      /* P5(v73)：附帶組分流——魅力組主修（魅力訓練）未開放隱藏；附帶外貌課
         未報名嗰陣喺摺疊入面只出純文字句；報咗名就出細排入掣 */
      ux68GuideStat = 'charm';
      S = freshS();
      const p5 = train71PickerHtml('fill');
      ok('P5(v73)：附帶未報名課只出純文字句（摺疊保留）',
         p5.indexOf('data-tsub="1"') >= 0 && /「外貌／形象」未報名——去 .+ 報名。/.test(p5));
      ok('P5(v73)：主修未開放嗰陣唔出主修標題、課名隱藏',
         p5.indexOf('主修 · 主升魅力') < 0 && p5.indexOf(COURSE_DEFS.train_charm.name) < 0);
      S = freshS({ enrolled: { train_looks: true } });
      const p5b = train71PickerHtml('fill');
      ok('P5(v73)：附帶已報名課有細排入掣', p5b.indexOf('data-t71pick="train_looks"') >= 0);

      /* P6(v73)：成組課程全部未開放（台風組新遊戲）——唔成組消失：
         出通用一句，課名同條件都唔出；逐日版同樣零跳轉 */
      ux68GuideStat = 'stage';
      S = freshS();
      const p6 = train71PickerHtml('day');
      /* v20a75 改版：演技一級起有台風附帶 +1，台風組附帶課變咗 train_acting
         （未報名）——成組唔再剩返全未開放，改出 v73 未報名一句文字；主修課名
         同舊進階課名仍然隱藏。通用一句嘅全未開放情境改喺 levels75 測試覆蓋。 */
      ok('P6(v75)：台風組出附帶課未報名一句、主修／進階課名隱藏',
         p6.indexOf('「演技訓練」未報名') >= 0
         && p6.indexOf(COURSE_DEFS.train_stage.name) < 0
         && p6.indexOf('進階台風') < 0);
      ok('P6(v73)：逐日版零跳轉', p6.indexOf('data-gloc') < 0 && p6.indexOf('前往') < 0);
      ux68GuideStat = '';
    })();
  `;
  const SRC = [
    extractConst('EMOJI_ICON112'),
    extractFn('function iconHtml112'),
    extractFn('function favDots112'),
    extractConst('COURSE_DEFS'),
    extractConst('TRAIN_BY_TYPE'),
    extractConst('COURSE_ENROLL_EXTRA'),
    extractConst('STAT_LABEL'),
    extractConst('LOCS'),
    extractFn('function applyTrainLesson'),
    extractBlock('/* ===== v20a68 UX68', 'function looksLikeEraId(s){'),
    DRIVER,
  ].join('\n')
   .replace('const EMOJI_ICON112 =', 'var EMOJI_ICON112 =')
   .replace('const COURSE_DEFS =', 'var COURSE_DEFS =')
   .replace('const TRAIN_BY_TYPE =', 'var TRAIN_BY_TYPE =')
   .replace('const COURSE_ENROLL_EXTRA =', 'var COURSE_ENROLL_EXTRA =')
   .replace('const STAT_LABEL =', 'var STAT_LABEL =')
   .replace('const LOCS =', 'var LOCS =');
  eval(SRC);
})();

console.log(fails.length ? ('PROGRESS71 LOGIC: ' + fails.length + ' FAIL -> ' + fails.join(' | ')) : 'PROGRESS71 LOGIC: ALL PASS');
process.exit(fails.length ? 1 : 0);
