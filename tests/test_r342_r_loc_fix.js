// v342 R_LOC 邏輯測試：31 個 R_ 感情節點 locId 派位＋offer 觸發鏈＋crisis 頁首年份。
// 背景：R_ 節點 JSON 無 locId、STORY_LOC_SOFT 無 entry → storyNodeLocId 回 null
// → enterLoc／doTalk 永遠唔寫 offer → listOpen 入唔到 → StoryPlay.start 拒播。
// 修法：STORY_LOC_SOFT 派 locId＋JSON 移除 playerOffer:false（行返現成 offer 機制）
// ＋crisis/push2 when 1991→1990（YEARS66 walk 後顯示 1992，唔再 1993 超出終點）。
// 行真路徑：抽 StoryOC／storyNodeLocId／years66Walk／spPlayerMeta_softSeasonFrom 真函數
// → 播種存檔 → 複製 enterLoc offer loop 真寫 offer → listOpen 真入列
// → hasPlayerOffer＋evalNode（StoryPlay.start 兩個閘）真通過。
// StoryPlay.start 本體要 DOM render，沙盒唔行；drive-299 已實駕證明有 offer 即播到。
// 用法：node tests/test_r342_r_loc_fix.js
const fs = require('fs');
const path = require('path');
const rootDir = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(rootDir, 'index.html'), 'utf8');
const mainPack = JSON.parse(fs.readFileSync(path.join(rootDir, 'content', 'story_detail_n1_to_n17.json'), 'utf8'));
const packVH = JSON.parse(fs.readFileSync(path.join(rootDir, 'content', 'story_detail_romance_vera_hiu_choi.json'), 'utf8'));
const packLX = JSON.parse(fs.readFileSync(path.join(rootDir, 'content', 'story_detail_romance_lan_xu.json'), 'utf8'));
const packYS = JSON.parse(fs.readFileSync(path.join(rootDir, 'content', 'story_detail_romance_yip_so.json'), 'utf8'));

let pass = 0, fail = 0;
function ok(name, cond){
  if(cond){ pass++; console.log('  ok - ' + name); }
  else { fail++; console.log('  FAIL - ' + name); }
}

function extractFn(decl){
  const i = html.indexOf(decl);
  if(i<0) throw new Error('fn not found: '+decl);
  let j = html.indexOf('{', i), depth = 0, k = j;
  for(; k<html.length; k++){
    if(html[k]==='{') depth++;
    else if(html[k]==='}'){ depth--; if(depth===0){ k++; break; } }
  }
  return html.slice(i, k);
}
function extractConst(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) throw new Error('const not found: '+name);
  let depth = 0, started = false;
  for(let k=i; k<html.length; k++){
    const ch = html[k];
    if(ch==='{'||ch==='['){ depth++; started = true; }
    else if(ch==='}'||ch===']'){ depth--; if(started && depth===0) return html.slice(i, k+1)+';'; }
    else if(ch===';' && !started) return html.slice(i, k+1);
  }
  throw new Error('const end not found: '+name);
}
function extractIIFE(decl){
  const i = html.indexOf(decl);
  if(i<0) throw new Error('iife not found: '+decl);
  const end = html.indexOf('\n})();', i);
  if(end<0) throw new Error('iife end not found: '+decl);
  return html.slice(i, end) + '\n})();';
}

/* ---- 環境 stub ---- */
var window = {};
var location = { search: "" };
var localStorage = { getItem: ()=>null, setItem: ()=>{}, removeItem: ()=>{} };
var S = null;
var saveQ = function(){};
var toast = function(){};
var syncNotebookMirror = function(){};
var STORY_WIRE = { main: null, romance: { veraHiuChoi: null, lanXu: null, yipSo: null } };
var apply = function(delta){ Object.keys(delta||{}).forEach(k=>{ S[k] = (Number(S[k])||0) + delta[k]; }); return []; };
var applyCastingTags = function(labels){
  if(!Array.isArray(S.castingTags)) S.castingTags = [];
  const out = [];
  (labels||[]).forEach(lb=>{
    const s = String(lb||""); if(!s) return;
    if(!S.castingTags.some(t=>t && (t.id===s || t.label===s))) S.castingTags.push({ id:s, label:s });
    out.push({ id:s, label:s });
  });
  return out;
};

const SRC = [
  "var START = { y:1990, m:3, d:7 };",
  extractFn('function dateObj'),
  extractFn('function calendarSeason'),
  extractFn('function weekNumNow'),
  extractFn('function dualTrackNumbers'),
  extractFn('function readDualTracks'),
  extractFn('function syncDualTracks'),
  extractFn('function yearSeasonNow'),
  extractFn('function storyHintPack'),
  extractFn('function storyNodeLocId'),
  extractFn('function ensureFavorLedger'),
  extractFn('function favorLedgerNoteSettled'),
  extractFn('function favorLedgerNoteCredit'),
  extractFn('function favorLedgerCounts'),
  extractConst('STORY_GATE_3Y'),
  extractConst('STORY_LOC_SOFT'),
  extractConst('STORY_HINT_SOFT'),
  extractConst('STORY_TITLE_SOFT'),
  extractIIFE('const BehaviorGate = (function(){'),
  extractIIFE('const StoryOC = (()=>{'),
  // YEARS66 walk（頁首年份測試用）
  extractConst('YEARS66_SHIFT'),
  extractConst('YEARS66_OLD_MIN'),
  extractConst('YEARS66_TOKEN_RE'),
  extractFn('function years66ShiftYear'),
  extractFn('function years66ShiftText'),
  extractConst('YEARS66_SKIP_KEYS'),
  extractConst('YEARS66_YEAR_KEYS'),
  extractFn('function years66Walk'),
  // 頁首季節行（spPlayerMeta_softSeasonFrom 依賴）
  extractFn('function spSoftSeasonChar'),
  extractFn('function spSoftLane'),
  extractFn('function spSoftSeasonLine'),
  extractFn('function spPlayerMeta_softSeasonFrom'),
].join('\n')
 .replace('const STORY_GATE_3Y =', 'var STORY_GATE_3Y =')
 .replace('const STORY_LOC_SOFT =', 'var STORY_LOC_SOFT =')
 .replace('const STORY_HINT_SOFT =', 'var STORY_HINT_SOFT =')
 .replace('const STORY_TITLE_SOFT =', 'var STORY_TITLE_SOFT =')
 .replace('const BehaviorGate =', 'var BehaviorGate =')
 .replace('const StoryOC =', 'var StoryOC =')
 .replace('const YEARS66_SHIFT =', 'var YEARS66_SHIFT =')
 .replace('const YEARS66_OLD_MIN =', 'var YEARS66_OLD_MIN =')
 .replace('const YEARS66_TOKEN_RE =', 'var YEARS66_TOKEN_RE =')
 .replace('const YEARS66_SKIP_KEYS =', 'var YEARS66_SKIP_KEYS =')
 .replace('const YEARS66_YEAR_KEYS =', 'var YEARS66_YEAR_KEYS =');
eval(SRC);

ok('harness: StoryOC 載入', typeof StoryOC === 'object' && typeof StoryOC.listOpen === 'function' && typeof StoryOC.openMeetOffer === 'function');
ok('harness: storyNodeLocId／years66Walk 載入', typeof storyNodeLocId === 'function' && typeof years66Walk === 'function');

function dayIndexOf(y, m, d){ return Math.round((Date.UTC(y, m-1, d) - Date.UTC(1990, 2, 7)) / 86400000); }
function loadGame(over){
  S = Object.assign({
    dayIndex: dayIndexOf(1992, 6, 1), money: 900, fame: 30, acting: 30, popularity: 30,
    industryCredit: 0, industryCreditDelta: 0,
    flags: {}, routes: {}, mockCredits: [], mockDebts: [], mockRumors: [], inventory: {},
    castingTags: [], favorLedger: null,
    story: { flags: {}, rel: {}, done: {}, choices: {}, phase: "P5", offers: {} },
  }, over || {});
  STORY_WIRE.main = JSON.parse(JSON.stringify(mainPack));
  STORY_WIRE.romance.veraHiuChoi = JSON.parse(JSON.stringify(packVH));
  STORY_WIRE.romance.lanXu = JSON.parse(JSON.stringify(packLX));
  STORY_WIRE.romance.yipSo = JSON.parse(JSON.stringify(packYS));
  StoryOC.ensure();
  return S;
}

/* 複製 enterLoc offer loop（index.html enterLoc 內 StoryOC.iterNodes 段，逐字邏輯） */
function enterLocOffers(locId){
  StoryOC.ensure();
  StoryOC.iterNodes().forEach(({node, pack})=>{
    if(!node || !node.id) return;
    if(node.playerOffer === false) return;
    if(storyNodeLocId(node)!==locId) return;
    if(StoryOC.hasPlayerOffer(node, pack)) return;
    if(StoryOC.isStubNode(node)) return;
    if(StoryOC.isDone(node.id)) return;
    const ev = StoryOC.evalNode(node, { checkNodePhase:true });
    if(ev && ev.ok) StoryOC.openMeetOffer(node.id, "enterLoc:"+locId);
  });
}

/* ---- (0) 靜態：31 節點 locId＋playerOffer ---- */
const EXPECT_LOC = {
  R_lan_meet:"tvb_longmen", R_lan_push1:"tvb_longmen", R_lan_push2:"tvb_longmen",
  R_lan_crisis:"tvb_longmen", R_lan_ending:"tvb_longmen",
  R_xu_meet:"tvb_longmen", R_xu_push1:"ad_central", R_xu_push2:"ad_central",
  R_xu_crisis:"ad_central", R_xu_ending:"ad_central",
  R_tang_meet_stub:"ad_central",
  R_hiu_meet:"tvb_longmen", R_hiu_push1:"cafe_cha", R_hiu_push2:"tvb_longmen",
  R_hiu_crisis:"tvb_longmen", R_hiu_ending:"tvb_longmen",
  R_choi_meet:"tvb_longmen", R_choi_push1:"cafe_cha", R_choi_push2:"cafe_cha",
  R_choi_crisis:"ad_adm", R_choi_ending:"ad_adm",
  R_yip_meet:"tvb_longmen", R_yip_push1:"tvb_longmen", R_yip_push2:"tvb_longmen",
  R_yip_crisis:"tvb_longmen", R_yip_ending:"tvb_longmen",
  R_so_meet:"rec_wanchai", R_so_push1:"rec_wanchai", R_so_push2:"ad_central",
  R_so_crisis:"rec_wanchai", R_so_ending:"rec_wanchai",
};
loadGame();
{
  const all = StoryOC.iterNodes().filter(x=>/^R_/.test(x.node.id));
  ok('R_ 節點共 31 個', all.length === 31);
  let locOk = true, offerOk = true;
  all.forEach(({node})=>{
    if(storyNodeLocId(node) !== EXPECT_LOC[node.id]){ locOk = false; console.log('    loc mismatch: ' + node.id + ' got ' + storyNodeLocId(node) + ' want ' + EXPECT_LOC[node.id]); }
    if(node.playerOffer === false){ offerOk = false; console.log('    playerOffer still false: ' + node.id); }
  });
  ok('31 節點 storyNodeLocId 全部命中派位', locOk);
  ok('31 節點 playerOffer 無 false（offer 機制適用）', offerOk);
}

/* ---- (1) 逐線觸發鏈：enterLoc 寫 offer → listOpen 入列 → start 兩閘通過 ---- */
const LINES = [
  { key:"lan",  meet:"R_lan_meet" },
  { key:"xu",   meet:"R_xu_meet" },
  { key:"hiu",  meet:"R_hiu_meet" },
  { key:"choi", meet:"R_choi_meet" },
  { key:"yip",  meet:"R_yip_meet" },
  { key:"so",   meet:"R_so_meet" },
];
LINES.forEach(({key, meet})=>{
  loadGame();
  if(key === "yip") S.story.done.N8 = true; /* v380：R_yip_meet 補 N8 閘（設計掛 N8 選美後台），種子補 N8 done，意圖不變 */
  const node = StoryOC.findNodeRaw(meet);
  const loc = storyNodeLocId(node);
  ok(key + ' meet 有 locId（' + loc + '）', !!loc);
  ok(key + ' meet 入場前無 offer', !StoryOC.hasPlayerOffer(node, null));
  enterLocOffers(loc);
  ok(key + ' enterLoc 後 offer 已寫', StoryOC.hasPlayerOffer(node, null) === true);
  const oc = StoryOC.listOpen({ checkNodePhase:true, player:true, ignoreSheetLoc:true });
  ok(key + ' listOpen open 入列', (oc.open||[]).some(r=>r.id===meet));
  const ev = StoryOC.evalNode(node, { checkNodePhase:true });
  ok(key + ' evalNode ok（StoryPlay.start 閘）', ev.ok === true);
  ok(key + ' 非 stub／未 done（start 前置）', !StoryOC.isStubNode(node) && !StoryOC.isDone(meet));
});

/* ---- (2) push1 鏈：meet 旗開 push1（抽 lan＋choi 兩線） ---- */
{
  loadGame({ story: { flags: { flag_lan_met_warm: true }, rel: {}, done: { R_lan_meet: true }, choices: {}, phase: "P5", offers: {} } });
  const n = StoryOC.findNodeRaw("R_lan_push1");
  enterLocOffers(storyNodeLocId(n));
  const oc = StoryOC.listOpen({ checkNodePhase:true, player:true, ignoreSheetLoc:true });
  ok('lan push1：meet 旗在 → offer＋入列', StoryOC.hasPlayerOffer(n, null) && (oc.open||[]).some(r=>r.id==="R_lan_push1"));
}
{
  loadGame({ story: { flags: { flag_choi_spin: true }, rel: {}, done: {}, choices: {}, phase: "P5", offers: {} } });
  const n = StoryOC.findNodeRaw("R_choi_push1");
  enterLocOffers(storyNodeLocId(n));
  const oc = StoryOC.listOpen({ checkNodePhase:true, player:true, ignoreSheetLoc:true });
  ok('choi push1：N5 spin 旗在 → offer＋入列（cafe_cha）', storyNodeLocId(n) === "cafe_cha" && StoryOC.hasPlayerOffer(n, null) && (oc.open||[]).some(r=>r.id==="R_choi_push1"));
}

/* ---- (3) crisis 頁首年份：source 1990 → walk 後顯示 1992，唔出 1993 ---- */
{
  const crisisIds = ["R_lan_crisis", "R_xu_push2", "R_xu_crisis", "R_hiu_crisis", "R_choi_crisis"];
  crisisIds.forEach(id=>{
    const raw = StoryOC.findNodeRaw(id);
    ok(id + ' source when 1990 開頭', /^1990/.test(String(raw.when||"")));
    const walked = years66Walk(JSON.parse(JSON.stringify(raw)), null);
    const line = spPlayerMeta_softSeasonFrom(walked, {});
    ok(id + ' 頁首顯示 1992（' + line + '）', /1992/.test(line) && !/1993/.test(line));
  });
  const choi = years66Walk(JSON.parse(JSON.stringify(StoryOC.findNodeRaw("R_choi_crisis"))), null);
  ok('R_choi_crisis 頁首＝1992冬', spPlayerMeta_softSeasonFrom(choi, {}) === "主線 · 1992冬");
}

console.log('TOTAL ' + pass + ' PASS ' + fail + ' FAIL');
process.exit(fail ? 1 : 0);
