// WEAVE_PHASE4_6 邏輯測試（v20a29）：
// 行真路徑——JSON pack 主幹節點（v20a234：內嵌覆寫表已刪，N7–N11 由 pack 直出，唯一來源）
// → StoryOC.listOpen({player:true}) 真 offer 路徑 → StoryOC.applyChoice 真寫入
// → story46SettleTick 真結算（債權登記＋N8 見面禮互動）。
// 閘行 STORY_GATE_3Y／BehaviorGate.evalGate3Y 真函數（4-5 已落地，今步唔改閘，只補 registry tag 候選）。
// pack 用 repo content/story_detail_n1_to_n17.json 嘅 live 副本；
// loader 將成個 JSON 做 STORY_WIRE.main，測試照砌。
// stub：window/location/localStorage/saveQ/toast/syncNotebookMirror；apply（引擎 stats 落地，
// 語義照 applyChoice 內置 fallback：直接累加 S 欄位）；applyCastingTags（照引擎 fallback 形狀：
// 未註冊 label 以 {id:label,label} 入 S.castingTags）。
// 用法：node tests/test_weave46_logic.js
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const pack = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'content', 'story_detail_n1_to_n17.json'), 'utf8'));

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
  extractConst('STORY_LOC_SOFT'),
  extractConst('STORY_HINT_SOFT'),
  extractConst('STORY_TITLE_SOFT'),
  extractConst('STORY46_CREDIT_N7'),
  extractConst('STORY46_CREDIT_N10'),
  extractConst('STORY46_GIFT_ID'),
  extractFn('function story46SettleTick'),
  extractIIFE('const BehaviorGate = (function(){'),
  extractIIFE('const StoryOC = (()=>{'),
].join('\n')
 .replace('const STORY_GATE_3Y =', 'var STORY_GATE_3Y =')
 .replace('const STORY_LOC_SOFT =', 'var STORY_LOC_SOFT =')
 .replace('const STORY_HINT_SOFT =', 'var STORY_HINT_SOFT =')
 .replace('const STORY_TITLE_SOFT =', 'var STORY_TITLE_SOFT =')
 .replace('const STORY46_CREDIT_N7 =', 'var STORY46_CREDIT_N7 =')
 .replace('const STORY46_CREDIT_N10 =', 'var STORY46_CREDIT_N10 =')
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

/* ---- 主幹節點完整性（v20a234：pack 直出，唔再經覆寫） ---- */
loadGame(baseSave());
{
  const t = { N7: ['暴雨', 'film_harbour', '魏詠男'], N8: ['化妝間', 'tvb_longmen', '葉敏芝'],
              N9: ['卡座', 'cafe_cha', '廖炳星'], N10: ['酒廊', 'tvb_harbour', '顧明輝'],
              N11: ['黑西裝與舊風褸', 'tvb_longmen', '彭少祺'] };
  let allOk = true;
  Object.keys(t).forEach(id => {
    const n = node(id);
    if(!n || n.title !== t[id][0] || n.locId !== t[id][1] || !JSON.stringify(n).includes(t[id][2]) || !n.playerOffer) allOk = false;
    if(n && JSON.stringify(n).includes('藍若曦')) allOk = false;
  });
  ok('主幹完整性：五節點標題／場地／紅星跟主幹，內容無舊歌手線人物', allOk);
}

/* ---- N7 ---- */
loadGame(baseSave({ story: { flags: {}, rel: {}, done: { N5: true }, choices: {} }, industryCreditDelta: 25 }));
ok('N7：1991 夏＋N5 done＋信用>20 → offer 喺 film_harbour', !!openRow('N7') && openRow('N7').locId === 'film_harbour');
loadGame(baseSave({ dayIndex: dayIndexOf(1990, 7, 15), story: { flags: {}, rel: {}, done: { N5: true }, choices: {} }, industryCreditDelta: 25 }));
ok('N7：1990 唔出現', !openIds().includes('N7'));
loadGame(baseSave({ story: { flags: {}, rel: {}, done: {}, choices: {} }, industryCreditDelta: 25 }));
ok('N7：N5 未做唔出現', !openIds().includes('N7'));
loadGame(baseSave({ story: { flags: {}, rel: {}, done: { N5: true }, choices: {} }, industryCreditDelta: 13 })); /* base 7＋13＝信用 20 */
ok('N7：信用=20（嚴格 >20）唔出現', !openIds().includes('N7'));
loadGame(baseSave({ dayIndex: dayIndexOf(1991, 10, 15), story: { flags: {}, rel: {}, done: { N5: true }, choices: {} }, industryCreditDelta: 25 }));
ok('N7：秋天唔出現', !openIds().includes('N7'));

{
  const s = loadGame(baseSave({ story: { flags: {}, rel: {}, done: { N5: true }, choices: {} }, industryCreditDelta: 25 }));
  StoryOC.applyChoice(node('N7'), choice('N7', 'N7_a'));
  ok('N7_a：done＋flag_rain_rescue＋信用 delta 25→27', StoryOC.isDone('N7') && !!StoryOC.getFlag('flag_rain_rescue') && s.industryCreditDelta === 27);
  ok('N7_a：沉澱「識做」標籤', s.castingTags.some(t => t.label === '識做'));
  story46SettleTick();
  ok('N7_a：tick 登記債權 credit_c7_rain＋ledger credits=1', s.mockCredits.some(c => c.id === 'credit_c7_rain') && favorLedgerCounts().credits === 1);
  story46SettleTick();
  ok('N7_a：tick 重行唔雙計', s.mockCredits.filter(c => c.id === 'credit_c7_rain').length === 1 && favorLedgerCounts().credits === 1);
}
{
  const s = loadGame(baseSave({ story: { flags: {}, rel: {}, done: { N5: true }, choices: {} }, industryCreditDelta: 25 }));
  StoryOC.applyChoice(node('N7'), choice('N7', 'N7_b'));
  story46SettleTick();
  ok('N7_b：flag_rain_shelter，tick 唔登記債權', !!StoryOC.getFlag('flag_rain_shelter') && !s.mockCredits.some(c => c.id === 'credit_c7_rain'));
}

/* ---- N8（v20a113：補鏈，需 N7 done） ---- */
loadGame(baseSave({ dayIndex: dayIndexOf(1991, 9, 10), story: { flags: {}, rel: {}, done: { N7: true }, choices: {} } }));
ok('N8：1991 秋開，場地 tvb_longmen', !!openRow('N8') && openRow('N8').locId === 'tvb_longmen');
loadGame(baseSave({ dayIndex: dayIndexOf(1991, 7, 20), story: { flags: {}, rel: {}, done: { N7: true }, choices: {} } }));
ok('N8：1991 夏（夏末）亦開', openIds().includes('N8'));
loadGame(baseSave({ dayIndex: dayIndexOf(1991, 9, 10) }));
ok('N8：N7 未做唔出現', !openIds().includes('N8'));
loadGame(baseSave({ dayIndex: dayIndexOf(1991, 12, 10) }));
ok('N8：冬唔出現', !openIds().includes('N8'));
loadGame(baseSave({ dayIndex: dayIndexOf(1990, 9, 10) }));
ok('N8：1990 唔出現', !openIds().includes('N8'));
{
  const s = loadGame(baseSave({ dayIndex: dayIndexOf(1991, 9, 10), story: { flags: {}, rel: {}, done: { N7: true }, choices: {} }, inventory: { gift_perfume_sample: 1 } }));
  StoryOC.applyChoice(node('N8'), choice('N8', 'N8_a'));
  ok('N8_a：done＋flag_miss_cover＋「守口如瓶」標籤', StoryOC.isDone('N8') && !!StoryOC.getFlag('flag_miss_cover') && s.castingTags.some(t => t.label === '守口如瓶'));
  story46SettleTick();
  ok('N8_a＋有禮：tick 扣禮＋記 flag_miss_gift_prepared', !(s.inventory.gift_perfume_sample > 0) && !!StoryOC.getFlag('flag_miss_gift_prepared'));
}
{
  loadGame(baseSave({ dayIndex: dayIndexOf(1991, 9, 10), inventory: {} }));
  StoryOC.applyChoice(node('N8'), choice('N8', 'N8_a'));
  story46SettleTick();
  ok('N8_a＋冇禮：tick 記 flag_miss_gift_missed', !!StoryOC.getFlag('flag_miss_gift_missed') && !StoryOC.getFlag('flag_miss_gift_prepared'));
}
{
  const s = loadGame(baseSave({ dayIndex: dayIndexOf(1991, 9, 10), money: 900 }));
  StoryOC.applyChoice(node('N8'), choice('N8', 'N8_b'));
  story46SettleTick();
  ok('N8_b：flag_miss_leak＋「八卦」標籤＋wealth→money 900→1400＋唔觸發見面禮互動',
     !!StoryOC.getFlag('flag_miss_leak') && s.castingTags.some(t => t.label === '八卦') && s.money === 1400 && !StoryOC.getFlag('flag_miss_gift_missed'));
}

/* ---- N9 ---- */
function c8Save(over){
  return baseSave(Object.assign({
    dayIndex: dayIndexOf(1991, 10, 15), fame: 30,
    story: { flags: {}, rel: {}, done: { N5: true, N7: true }, choices: {} },
    castingTags: [{ id: 'tag_comedy', label: '喜劇細胞' }],
  }, over || {}));
}
loadGame(c8Save());
ok('N9：秋＋N7 done＋聲量>28＋喜劇標籤 → offer 喺 cafe_cha', !!openRow('N9') && openRow('N9').locId === 'cafe_cha');
loadGame(c8Save({ castingTags: [{ id: 'tag_action', label: '動作演員' }] }));
ok('N9：動作標籤（registry id/label）亦開', openIds().includes('N9'));
loadGame(c8Save({ castingTags: [] }));
ok('N9：冇標籤唔出現', !openIds().includes('N9'));
loadGame(c8Save({ fame: 28 }));
ok('N9：聲量=28（嚴格 >28）唔出現', !openIds().includes('N9'));
loadGame(c8Save({ story: { flags: {}, rel: {}, done: { N5: true }, choices: {} } }));
ok('N9：N7 未做唔出現', !openIds().includes('N9'));
loadGame(c8Save({ dayIndex: dayIndexOf(1991, 7, 15) }));
ok('N9：夏天唔出現', !openIds().includes('N9'));
{
  const s = loadGame(c8Save());
  StoryOC.applyChoice(node('N9'), choice('N9', 'N9_a'));
  ok('N9_a：done＋flag_bing_bridge＋聲量 30→33', StoryOC.isDone('N9') && !!StoryOC.getFlag('flag_bing_bridge') && s.fame === 33);
}
{
  const s = loadGame(c8Save());
  StoryOC.applyChoice(node('N9'), choice('N9', 'N9_b'));
  ok('N9_b：flag_bing_background＋信用 delta +2', !!StoryOC.getFlag('flag_bing_background') && s.industryCreditDelta === 2);
}

/* ---- N10 ---- */
loadGame(baseSave({ dayIndex: dayIndexOf(1991, 12, 15) }));
ok('N10：1991 冬開，場地 tvb_harbour', !!openRow('N10') && openRow('N10').locId === 'tvb_harbour');
loadGame(baseSave({ dayIndex: dayIndexOf(1991, 10, 15) }));
ok('N10：秋唔出現', !openIds().includes('N10'));
{
  const s = loadGame(baseSave({ dayIndex: dayIndexOf(1991, 12, 15) }));
  StoryOC.applyChoice(node('N10'), choice('N10', 'N10_a'));
  story46SettleTick();
  ok('N10_a：flag_chase_for_ho＋何生好感=2＋tick 唔登記債權',
     !!StoryOC.getFlag('flag_chase_for_ho') && StoryOC.getRel('ho') === 2 && !s.mockCredits.some(c => c.id === 'credit_c9_crew'));
}
{
  const s = loadGame(baseSave({ dayIndex: dayIndexOf(1991, 12, 15) }));
  StoryOC.applyChoice(node('N10'), choice('N10', 'N10_b'));
  story46SettleTick();
  ok('N10_b：flag_standup_crew＋tick 登記 credit_c9_crew＋ledger credits=1',
     !!StoryOC.getFlag('flag_standup_crew') && s.mockCredits.some(c => c.id === 'credit_c9_crew') && favorLedgerCounts().credits === 1);
  story46SettleTick();
  ok('N10_b：tick 重行唔雙計', favorLedgerCounts().credits === 1);
}

/* ---- N11 ---- */
function c10Save(over){
  return baseSave(Object.assign({
    dayIndex: dayIndexOf(1991, 12, 20), fame: 40, industryCreditDelta: 35,
    story: { flags: {}, rel: {}, done: { N5: true, N7: true, N10: true }, choices: {} },
  }, over || {}));
}
loadGame(c10Save());
ok('N11：冬＋N10 done＋雙軌>70 → offer（場地 tvb_longmen）', !!openRow('N11') && openRow('N11').locId === 'tvb_longmen');
loadGame(c10Save({ fame: 20, industryCreditDelta: 20 }));
ok('N11：雙軌=52（門檻 >70）唔出現', !openIds().includes('N11'));
loadGame(c10Save({ story: { flags: {}, rel: {}, done: { N5: true, N7: true }, choices: {} } }));
ok('N11：N10 未做唔出現', !openIds().includes('N11'));
loadGame(c10Save());
StoryOC.applyChoice(node('N11'), choice('N11', 'N11_a'));
ok('N11_a：flag_role_gangster', StoryOC.isDone('N11') && !!StoryOC.getFlag('flag_role_gangster'));
loadGame(c10Save());
StoryOC.applyChoice(node('N11'), choice('N11', 'N11_b'));
ok('N11_b：flag_role_cop', !!StoryOC.getFlag('flag_role_cop'));

/* ---- 回歸：N1／N6 ---- */
loadGame(baseSave({ dayIndex: 1, fame: 5 }));
ok('回歸：N1 開局可開', openIds().includes('N1'));
loadGame(baseSave({ dayIndex: 98, fame: 12, story: { flags: { route_tv: true }, rel: {}, done: { N1: true, N2: true, N3: true, N4: true, N5: true }, choices: {} } }));
ok('回歸：N6 route_tv＋W15 開', openIds().includes('N6'));
loadGame(baseSave({ dayIndex: 98, fame: 12, story: { flags: {}, rel: {}, done: { N1: true, N2: true, N3: true, N4: true, N5: true }, choices: {} } }));
ok('回歸：N6 缺 route 唔開', !openIds().includes('N6'));

console.log('\nWEAVE_PHASE4_6 邏輯測試：' + pass + ' 過 / ' + fail + ' 失敗');
process.exit(fail ? 1 : 0);
