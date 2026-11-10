// WEAVE_PHASE4_6 邏輯測試（v20a29）：
// 行真路徑——STORY_SPINE_NODES_1989 覆寫（applyStorySpineOverrides46 套落真 pack nodes）
// → StoryOC.listOpen({player:true}) 真 offer 路徑 → StoryOC.applyChoice 真寫入
// → story46SettleTick 真結算（債權登記＋C11 見面禮互動）。
// 閘行 STORY_GATE_3Y／BehaviorGate.evalGate3Y 真函數（4-5 已落地，今步唔改閘，只補 registry tag 候選）。
// pack 用 repo content/story_detail_c1_to_c17.json 嘅真副本（tests/fixtures/）；
// loader 將成個 JSON 做 STORY_WIRE.main，測試照砌。
// stub：window/location/localStorage/saveQ/toast/syncNotebookMirror；apply（引擎 stats 落地，
// 語義照 applyChoice 內置 fallback：直接累加 S 欄位）；applyCastingTags（照引擎 fallback 形狀：
// 未註冊 label 以 {id:label,label} 入 S.castingTags）。
// 用法：node tests/test_weave46_logic.js
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const pack = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'story_detail_c1_to_c17.json'), 'utf8'));

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

/* ---- 環境 stub（module scope；eval 喺同一 scope 行） ---- */
var window = {};
var location = { search: "" };
var localStorage = { getItem: ()=>null, setItem: ()=>{}, removeItem: ()=>{} };
var S = null;
var saveQ = function(){};
var toast = function(){};
var syncNotebookMirror = function(){};
var STORY_WIRE = { main: null };
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
  extractConst('STORY_SPINE_NODES_1989'),
  extractConst('STORY_LOC_SOFT'),
  extractConst('STORY_HINT_SOFT'),
  extractConst('STORY_TITLE_SOFT'),
  extractConst('STORY46_CREDIT_C7'),
  extractConst('STORY46_CREDIT_C9'),
  extractConst('STORY46_GIFT_ID'),
  extractFn('function applyStorySpineOverrides46'),
  extractFn('function story46SettleTick'),
  extractIIFE('const BehaviorGate = (function(){'),
  extractIIFE('const StoryOC = (()=>{'),
].join('\n')
 .replace('const STORY_GATE_3Y =', 'var STORY_GATE_3Y =')
 .replace('const STORY_SPINE_NODES_1989 =', 'var STORY_SPINE_NODES_1989 =')
 .replace('const STORY_LOC_SOFT =', 'var STORY_LOC_SOFT =')
 .replace('const STORY_HINT_SOFT =', 'var STORY_HINT_SOFT =')
 .replace('const STORY_TITLE_SOFT =', 'var STORY_TITLE_SOFT =')
 .replace('const STORY46_CREDIT_C7 =', 'var STORY46_CREDIT_C7 =')
 .replace('const STORY46_CREDIT_C9 =', 'var STORY46_CREDIT_C9 =')
 .replace('const STORY46_GIFT_ID =', 'var STORY46_GIFT_ID =')
 .replace('const BehaviorGate =', 'var BehaviorGate =')
 .replace('const StoryOC =', 'var StoryOC =');
eval(SRC);

ok('harness: StoryOC.listOpen/applyChoice 載入', typeof StoryOC === 'object' && typeof StoryOC.listOpen === 'function' && typeof StoryOC.applyChoice === 'function');
ok('harness: story46SettleTick 載入', typeof story46SettleTick === 'function');

function dayIndexOf(y, m, d){ return Math.round((Date.UTC(y, m-1, d) - Date.UTC(1990, 2, 7)) / 86400000); }
function baseSave(over){
  return Object.assign({
    dayIndex: dayIndexOf(1991, 7, 15), money: 900, fame: 10, acting: 8, popularity: 30,
    industryCredit: 0, industryCreditDelta: 0,
    flags: {}, routes: {}, mockCredits: [], mockDebts: [], mockRumors: [], inventory: {},
    castingTags: [], favorLedger: null,
    story: { flags: {}, rel: {}, done: {}, choices: {} },
  }, over || {});
}
function loadGame(save){
  S = save;
  STORY_WIRE.main = JSON.parse(JSON.stringify(pack));
  const r = applyStorySpineOverrides46();
  if(!(r && r.ok && r.replaced === 5)) throw new Error('覆寫應替換 5 個節點，實際 ' + JSON.stringify(r));
  StoryOC.ensure();
  return S;
}
function openIds(){ return StoryOC.listOpen({ player: true }).open.map(r => r.id); }
function openRow(id){ return StoryOC.listOpen({ player: true }).open.find(r => r.id === id); }
function node(id){ return StoryOC.findNodeRaw(id); }
function choice(nodeId, choiceId){
  const c = (node(nodeId).choices || []).find(x => x.id === choiceId);
  if(!c) throw new Error(nodeId + ' 應有 choice ' + choiceId);
  return c;
}

/* ---- 覆寫完整性 ---- */
loadGame(baseSave());
{
  const t = { C7: ['暴雨救場', 'film_harbour', '魏詠男'], C11: ['選美後台', 'tvb_longmen', '葉敏芝'],
              C8: ['茶餐廳度橋', 'cafe_cha', '廖炳星'], C9: ['年尾追數', 'tvb_harbour', '顧明輝'],
              C10: ['戲路定型', 'tvb_longmen', '彭兆基'] };
  let allOk = true;
  Object.keys(t).forEach(id => {
    const n = node(id);
    if(!n || n.title !== t[id][0] || n.locId !== t[id][1] || !JSON.stringify(n).includes(t[id][2]) || !n.playerOffer) allOk = false;
    if(n && JSON.stringify(n).includes('藍若曦')) allOk = false;
  });
  ok('覆寫完整性：五節點標題／場地／紅星跟主幹，內容無舊歌手線人物', allOk);
  const r2 = applyStorySpineOverrides46();
  ok('覆寫冪等：再套一次 replaced=5、結果不變', r2.ok && r2.replaced === 5 && node('C7').title === '暴雨救場');
}

/* ---- N7＝C7 ---- */
loadGame(baseSave({ story: { flags: {}, rel: {}, done: { C5: true }, choices: {} }, industryCreditDelta: 25 }));
ok('C7：1991 夏＋C5 done＋信用>20 → offer 喺 film_harbour', !!openRow('C7') && openRow('C7').locId === 'film_harbour');
loadGame(baseSave({ dayIndex: dayIndexOf(1990, 7, 15), story: { flags: {}, rel: {}, done: { C5: true }, choices: {} }, industryCreditDelta: 25 }));
ok('C7：1990 唔出現', !openIds().includes('C7'));
loadGame(baseSave({ story: { flags: {}, rel: {}, done: {}, choices: {} }, industryCreditDelta: 25 }));
ok('C7：C5 未做唔出現', !openIds().includes('C7'));
loadGame(baseSave({ story: { flags: {}, rel: {}, done: { C5: true }, choices: {} }, industryCreditDelta: 13 })); /* base 7＋13＝信用 20 */
ok('C7：信用=20（嚴格 >20）唔出現', !openIds().includes('C7'));
loadGame(baseSave({ dayIndex: dayIndexOf(1991, 10, 15), story: { flags: {}, rel: {}, done: { C5: true }, choices: {} }, industryCreditDelta: 25 }));
ok('C7：秋天唔出現', !openIds().includes('C7'));

{
  const s = loadGame(baseSave({ story: { flags: {}, rel: {}, done: { C5: true }, choices: {} }, industryCreditDelta: 25 }));
  StoryOC.applyChoice(node('C7'), choice('C7', 'C7_a'));
  ok('C7_a：done＋flag_rain_rescue＋信用 delta 25→27', StoryOC.isDone('C7') && !!StoryOC.getFlag('flag_rain_rescue') && s.industryCreditDelta === 27);
  ok('C7_a：沉澱「識做」標籤', s.castingTags.some(t => t.label === '識做'));
  story46SettleTick();
  ok('C7_a：tick 登記債權 credit_c7_rain＋ledger credits=1', s.mockCredits.some(c => c.id === 'credit_c7_rain') && favorLedgerCounts().credits === 1);
  story46SettleTick();
  ok('C7_a：tick 重行唔雙計', s.mockCredits.filter(c => c.id === 'credit_c7_rain').length === 1 && favorLedgerCounts().credits === 1);
}
{
  const s = loadGame(baseSave({ story: { flags: {}, rel: {}, done: { C5: true }, choices: {} }, industryCreditDelta: 25 }));
  StoryOC.applyChoice(node('C7'), choice('C7', 'C7_b'));
  story46SettleTick();
  ok('C7_b：flag_rain_shelter，tick 唔登記債權', !!StoryOC.getFlag('flag_rain_shelter') && !s.mockCredits.some(c => c.id === 'credit_c7_rain'));
}

/* ---- N8＝C11 ---- */
loadGame(baseSave({ dayIndex: dayIndexOf(1991, 9, 10) }));
ok('C11：1991 秋開，場地 tvb_longmen', !!openRow('C11') && openRow('C11').locId === 'tvb_longmen');
loadGame(baseSave({ dayIndex: dayIndexOf(1991, 7, 20) }));
ok('C11：1991 夏（夏末）亦開', openIds().includes('C11'));
loadGame(baseSave({ dayIndex: dayIndexOf(1991, 12, 10) }));
ok('C11：冬唔出現', !openIds().includes('C11'));
loadGame(baseSave({ dayIndex: dayIndexOf(1990, 9, 10) }));
ok('C11：1990 唔出現', !openIds().includes('C11'));
{
  const s = loadGame(baseSave({ dayIndex: dayIndexOf(1991, 9, 10), inventory: { gift_perfume_sample: 1 } }));
  StoryOC.applyChoice(node('C11'), choice('C11', 'C11_a'));
  ok('C11_a：done＋flag_miss_cover＋「守口如瓶」標籤', StoryOC.isDone('C11') && !!StoryOC.getFlag('flag_miss_cover') && s.castingTags.some(t => t.label === '守口如瓶'));
  story46SettleTick();
  ok('C11_a＋有禮：tick 扣禮＋記 flag_miss_gift_prepared', !(s.inventory.gift_perfume_sample > 0) && !!StoryOC.getFlag('flag_miss_gift_prepared'));
}
{
  loadGame(baseSave({ dayIndex: dayIndexOf(1991, 9, 10), inventory: {} }));
  StoryOC.applyChoice(node('C11'), choice('C11', 'C11_a'));
  story46SettleTick();
  ok('C11_a＋冇禮：tick 記 flag_miss_gift_missed', !!StoryOC.getFlag('flag_miss_gift_missed') && !StoryOC.getFlag('flag_miss_gift_prepared'));
}
{
  const s = loadGame(baseSave({ dayIndex: dayIndexOf(1991, 9, 10), money: 900 }));
  StoryOC.applyChoice(node('C11'), choice('C11', 'C11_b'));
  story46SettleTick();
  ok('C11_b：flag_miss_leak＋「八卦」標籤＋wealth→money 900→1400＋唔觸發見面禮互動',
     !!StoryOC.getFlag('flag_miss_leak') && s.castingTags.some(t => t.label === '八卦') && s.money === 1400 && !StoryOC.getFlag('flag_miss_gift_missed'));
}

/* ---- N9＝C8 ---- */
function c8Save(over){
  return baseSave(Object.assign({
    dayIndex: dayIndexOf(1991, 10, 15), fame: 30,
    story: { flags: {}, rel: {}, done: { C5: true, C7: true }, choices: {} },
    castingTags: [{ id: 'tag_comedy', label: '喜劇細胞' }],
  }, over || {}));
}
loadGame(c8Save());
ok('C8：秋＋C7 done＋聲量>28＋喜劇標籤 → offer 喺 cafe_cha', !!openRow('C8') && openRow('C8').locId === 'cafe_cha');
loadGame(c8Save({ castingTags: [{ id: 'tag_action', label: '動作演員' }] }));
ok('C8：動作標籤（registry id/label）亦開', openIds().includes('C8'));
loadGame(c8Save({ castingTags: [] }));
ok('C8：冇標籤唔出現', !openIds().includes('C8'));
loadGame(c8Save({ fame: 28 }));
ok('C8：聲量=28（嚴格 >28）唔出現', !openIds().includes('C8'));
loadGame(c8Save({ story: { flags: {}, rel: {}, done: { C5: true }, choices: {} } }));
ok('C8：C7 未做唔出現', !openIds().includes('C8'));
loadGame(c8Save({ dayIndex: dayIndexOf(1991, 7, 15) }));
ok('C8：夏天唔出現', !openIds().includes('C8'));
{
  const s = loadGame(c8Save());
  StoryOC.applyChoice(node('C8'), choice('C8', 'C8_a'));
  ok('C8_a：done＋flag_bing_bridge＋聲量 30→33', StoryOC.isDone('C8') && !!StoryOC.getFlag('flag_bing_bridge') && s.fame === 33);
}
{
  const s = loadGame(c8Save());
  StoryOC.applyChoice(node('C8'), choice('C8', 'C8_b'));
  ok('C8_b：flag_bing_background＋信用 delta +2', !!StoryOC.getFlag('flag_bing_background') && s.industryCreditDelta === 2);
}

/* ---- N10＝C9 ---- */
loadGame(baseSave({ dayIndex: dayIndexOf(1991, 12, 15) }));
ok('C9：1991 冬開，場地 tvb_harbour', !!openRow('C9') && openRow('C9').locId === 'tvb_harbour');
loadGame(baseSave({ dayIndex: dayIndexOf(1991, 10, 15) }));
ok('C9：秋唔出現', !openIds().includes('C9'));
{
  const s = loadGame(baseSave({ dayIndex: dayIndexOf(1991, 12, 15) }));
  StoryOC.applyChoice(node('C9'), choice('C9', 'C9_a'));
  story46SettleTick();
  ok('C9_a：flag_chase_for_ho＋何生好感=2＋tick 唔登記債權',
     !!StoryOC.getFlag('flag_chase_for_ho') && StoryOC.getRel('ho') === 2 && !s.mockCredits.some(c => c.id === 'credit_c9_crew'));
}
{
  const s = loadGame(baseSave({ dayIndex: dayIndexOf(1991, 12, 15) }));
  StoryOC.applyChoice(node('C9'), choice('C9', 'C9_b'));
  story46SettleTick();
  ok('C9_b：flag_standup_crew＋tick 登記 credit_c9_crew＋ledger credits=1',
     !!StoryOC.getFlag('flag_standup_crew') && s.mockCredits.some(c => c.id === 'credit_c9_crew') && favorLedgerCounts().credits === 1);
  story46SettleTick();
  ok('C9_b：tick 重行唔雙計', favorLedgerCounts().credits === 1);
}

/* ---- N11＝C10 ---- */
function c10Save(over){
  return baseSave(Object.assign({
    dayIndex: dayIndexOf(1991, 12, 20), fame: 40, industryCreditDelta: 35,
    story: { flags: {}, rel: {}, done: { C5: true, C7: true, C9: true }, choices: {} },
  }, over || {}));
}
loadGame(c10Save());
ok('C10：冬＋C9 done＋雙軌>70 → offer（場地 tvb_longmen）', !!openRow('C10') && openRow('C10').locId === 'tvb_longmen');
loadGame(c10Save({ fame: 20, industryCreditDelta: 20 }));
ok('C10：雙軌=52（門檻 >70）唔出現', !openIds().includes('C10'));
loadGame(c10Save({ story: { flags: {}, rel: {}, done: { C5: true, C7: true }, choices: {} } }));
ok('C10：C9 未做唔出現', !openIds().includes('C10'));
loadGame(c10Save());
StoryOC.applyChoice(node('C10'), choice('C10', 'C10_a'));
ok('C10_a：flag_role_gangster', StoryOC.isDone('C10') && !!StoryOC.getFlag('flag_role_gangster'));
loadGame(c10Save());
StoryOC.applyChoice(node('C10'), choice('C10', 'C10_b'));
ok('C10_b：flag_role_cop', !!StoryOC.getFlag('flag_role_cop'));

/* ---- 回歸：C1／C6 ---- */
loadGame(baseSave({ dayIndex: 1, fame: 5 }));
ok('回歸：C1 開局可開', openIds().includes('C1'));
loadGame(baseSave({ dayIndex: 98, fame: 12, story: { flags: { route_tv: true }, rel: {}, done: { C1: true, C2: true, C3: true, C4: true, C5: true }, choices: {} } }));
ok('回歸：C6 route_tv＋W15 開', openIds().includes('C6'));
loadGame(baseSave({ dayIndex: 98, fame: 12, story: { flags: {}, rel: {}, done: { C1: true, C2: true, C3: true, C4: true, C5: true }, choices: {} } }));
ok('回歸：C6 缺 route 唔開', !openIds().includes('C6'));

console.log('\nWEAVE_PHASE4_6 邏輯測試：' + pass + ' 過 / ' + fail + ' 失敗');
process.exit(fail ? 1 : 0);
