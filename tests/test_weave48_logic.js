// WEAVE_PHASE4_8 邏輯測試（v20a31）：
// 行真路徑——STORY_SPINE_NODES_1990／STORY_SPINE_NODES_C6／ROMANCE_LAN_PA_OVERRIDES 覆寫
// （applyStorySpineOverrides48 套落真 pack nodes）→ StoryOC.listOpen({player:true}) 真 offer 路徑
// → StoryOC.applyChoice 真寫入 → story48SettleTick 真結算（C15／C13 債權登記）
// → COMMIT48 真可用性／真 applyChoice 落旗（commit 互斥／窗口／rel 門檻／crisis 前置）
// → paperSideItemForDay 真 picker（程天諾預熱年份閘）
// → newspaperStoryResolve 真函數證明 commit 新旗唔生報紙。
// 閘行 STORY_GATE_3Y／BehaviorGate.evalGate3Y 真函數（4-5 已落地，今步唔改閘）。
// pack 用 repo content 真副本（tests/fixtures/）：c1_to_c17＋romance_vera_hiu_choi＋romance_lan_xu。
// rel 經濟校準（S.story.rel）：鏈 meet1＋push1 2＋push2 2＋crisis 2＝7 max；COMMIT48_REL_MIN＝6。
// 用法：node tests/test_weave48_logic.js
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const pack = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'story_detail_c1_to_c17.json'), 'utf8'));
const romVHC = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'story_detail_romance_vera_hiu_choi.json'), 'utf8'));
const romLX = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'story_detail_romance_lan_xu.json'), 'utf8'));

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
var STORY_WIRE = { main: null, romance: { veraHiuChoi: null, lanXu: null, tang: null } };
var played48 = [];
var StoryPlay = { start(node, opts){ played48.push(node && node.id); return true; } };
var FREEPLAY_FW = { newspaperStub: null };
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
  extractFn('function choice47SeasonReached'),
  extractFn('function choice47StoryFlag'),
  extractFn('function choice47StoryDone'),
  extractFn('function commit48Rel'),
  extractFn('function commit48Available'),
  extractFn('function commit48ActionsAt'),
  extractFn('function commit48Play'),
  extractFn('function endingRomanceState48'),
  extractFn('function applyStorySpineOverrides46'),
  extractFn('function applyStorySpineOverrides48'),
  extractFn('function story46SettleTick'),
  extractFn('function story48SettleTick'),
  extractFn('function newspaperStoryLists'),
  extractFn('function newspaperStoryResolve'),
  extractFn('function paperSideItemForDay'),
  extractConst('STORY_GATE_3Y'),
  extractConst('STORY_SPINE_NODES_1989'),
  extractConst('STORY_SPINE_NODES_1990'),
  extractConst('STORY_SPINE_NODES_C6'),
  extractConst('ROMANCE_LAN_PA_OVERRIDES'),
  extractConst('STORY_LOC_SOFT'),
  extractConst('STORY_HINT_SOFT'),
  extractConst('STORY_TITLE_SOFT'),
  extractConst('STORY46_CREDIT_C7'),
  extractConst('STORY46_CREDIT_C9'),
  extractConst('STORY46_GIFT_ID'),
  extractConst('STORY48_CREDIT_C15'),
  extractConst('STORY48_CREDIT_C13'),
  extractConst('CHOICE47_SEASON_IDX'),
  extractConst('COMMIT48_NODES'),
  extractConst('COMMIT48_DEFS'),
  extractConst('COMMIT48_REL_MIN'),
  extractConst('STORY_FLAG_EVENT'),
  extractConst('STORY_PAPER_SKIP'),
  extractConst('PAPER_SIDE_ITEMS'),
  extractIIFE('const BehaviorGate = (function(){'),
  extractIIFE('const StoryOC = (()=>{'),
].join('\n')
 .replace('const STORY_GATE_3Y =', 'var STORY_GATE_3Y =')
 .replace('const STORY_SPINE_NODES_1989 =', 'var STORY_SPINE_NODES_1989 =')
 .replace('const STORY_SPINE_NODES_1990 =', 'var STORY_SPINE_NODES_1990 =')
 .replace('const STORY_SPINE_NODES_C6 =', 'var STORY_SPINE_NODES_C6 =')
 .replace('const ROMANCE_LAN_PA_OVERRIDES =', 'var ROMANCE_LAN_PA_OVERRIDES =')
 .replace('const STORY_LOC_SOFT =', 'var STORY_LOC_SOFT =')
 .replace('const STORY_HINT_SOFT =', 'var STORY_HINT_SOFT =')
 .replace('const STORY_TITLE_SOFT =', 'var STORY_TITLE_SOFT =')
 .replace('const STORY46_CREDIT_C7 =', 'var STORY46_CREDIT_C7 =')
 .replace('const STORY46_CREDIT_C9 =', 'var STORY46_CREDIT_C9 =')
 .replace('const STORY46_GIFT_ID =', 'var STORY46_GIFT_ID =')
 .replace('const STORY48_CREDIT_C15 =', 'var STORY48_CREDIT_C15 =')
 .replace('const STORY48_CREDIT_C13 =', 'var STORY48_CREDIT_C13 =')
 .replace('const CHOICE47_SEASON_IDX =', 'var CHOICE47_SEASON_IDX =')
 .replace('const COMMIT48_NODES =', 'var COMMIT48_NODES =')
 .replace('const COMMIT48_DEFS =', 'var COMMIT48_DEFS =')
 .replace('const COMMIT48_REL_MIN =', 'var COMMIT48_REL_MIN =')
 .replace('const STORY_FLAG_EVENT =', 'var STORY_FLAG_EVENT =')
 .replace('const STORY_PAPER_SKIP =', 'var STORY_PAPER_SKIP =')
 .replace('const PAPER_SIDE_ITEMS =', 'var PAPER_SIDE_ITEMS =')
 .replace('const BehaviorGate =', 'var BehaviorGate =')
 .replace('const StoryOC =', 'var StoryOC =');
eval(SRC);
var displayDateObj = function(){ return dateObj(); };

ok('harness: StoryOC/applyStorySpineOverrides48/commit48 載入',
   typeof StoryOC === 'object' && typeof applyStorySpineOverrides48 === 'function' && typeof commit48Available === 'function');
ok('harness: COMMIT48_REL_MIN = 6（鏈頂 7 校準）', COMMIT48_REL_MIN === 6);

function dayIndexOf(y, m, d){ return Math.round((Date.UTC(y, m-1, d) - Date.UTC(1990, 2, 7)) / 86400000); }
function baseSave(over){
  return Object.assign({
    dayIndex: dayIndexOf(1992, 4, 15), money: 900, fame: 20, acting: 8, popularity: 30,
    industryCredit: 0, industryCreditDelta: 0,
    flags: {}, routes: {}, mockCredits: [], mockDebts: [], mockRumors: [], inventory: {},
    castingTags: [], favorLedger: null,
    story: { flags: {}, rel: {}, done: {}, choices: {} },
  }, over || {});
}
function loadGame(save){
  S = save;
  STORY_WIRE.main = JSON.parse(JSON.stringify(pack));
  STORY_WIRE.romance.veraHiuChoi = JSON.parse(JSON.stringify(romVHC));
  STORY_WIRE.romance.lanXu = JSON.parse(JSON.stringify(romLX));
  const r46 = applyStorySpineOverrides46();
  if(!(r46 && r46.ok && r46.replaced === 5)) throw new Error('4-6 覆寫應替換 5 個，實際 ' + JSON.stringify(r46));
  const r48 = applyStorySpineOverrides48();
  if(!(r48 && r48.main === 6 && r48.lan === 5)) throw new Error('4-8 覆寫應 main=6/lan=5，實際 ' + JSON.stringify(r48));
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
function canon(o){
  if(Array.isArray(o)) return '[' + o.map(canon).join(',') + ']';
  if(o && typeof o === 'object') return '{' + Object.keys(o).sort().map(k => JSON.stringify(k) + ':' + canon(o[k])).join(',') + '}';
  return JSON.stringify(o);
}

/* ---- 覆寫完整性 ---- */
loadGame(baseSave());
{
  const t = { C15: ['高危替身', 'film_harbour', '麥震東'], C14: ['站隊', 'tvb_longmen', '齊鎮海'],
              C12: ['樂壇前哨', 'rec_star', '陸柏言'], C16: ['偶像實力之爭', 'rec_star', '程天諾'],
              C13: ['賀歲片', 'film_cotton', '廖炳星'] };
  let allOk = true;
  Object.keys(t).forEach(id => {
    const n = node(id);
    if(!n || n.title !== t[id][0] || n.locId !== t[id][1] || !JSON.stringify(n).includes(t[id][2]) || !n.playerOffer) allOk = false;
  });
  ok('覆寫完整性：1992 五節點標題／場地／紅星跟主幹', allOk);
  const stale = ['賀歲搶位', '緋聞公關真假', '尊重或包養', '聯姻逼退圈', '舊底片', '金九'];
  let clean = true;
  ['C12','C13','C14','C15','C16'].forEach(id => { if(stale.some(w => JSON.stringify(node(id)).includes(w))) clean = false; });
  ok('覆寫完整性：pack 自創線殘留字串清零（金九舊底片等）', clean);
  const c6 = node('C6');
  ok('C6 對齊 Qwen：標題「飯堂閒角」＋場地 tvb_longmen＋無約會旗／無 rel 加成',
     c6.title === '飯堂閒角' && c6.locId === 'tvb_longmen'
     && !JSON.stringify(c6).includes('date_')
     && (c6.choices || []).every(c => !Object.keys(((c.effects || {}).stats) || {}).some(k => k.startsWith('rel_')))
     && StoryOC.getFlag && c6.flags_written.includes('flag_canteen_grind'));
  const r2 = applyStorySpineOverrides48();
  ok('覆寫冪等：再套一次 main=6/lan=5、結果不變', r2.main === 6 && r2.lan === 5 && node('C15').title === '高危替身');
}

/* ---- 藍 PA 化：結構層同 pack 逐項一致、文字層零歌手向 ---- */
{
  const packLan = {};
  romLX.nodes.forEach(n => { packLan[n.id] = n; });
  /* v20a100 CLEAN100 B-03：pack 側 R_lan_push1 stats.music 正規化（見下面比較處註解） */
  const normStats100 = (id, pc) => {
    const st = Object.assign({}, ((pc || {}).effects || {}).stats || {});
    if(id === 'R_lan_push1' && ('music' in st)){ st.stage = st.music; delete st.music; }
    return st;
  };
  let structOk = true, proseOk = true;
  const singerWords = ['唱片店', '錄音室', '合唱', '狗仔', '緋聞', '聯姻', '豪門', '退圈', '登機證', '唱歌', '歌手', '情侶檔'];
  Object.keys(ROMANCE_LAN_PA_OVERRIDES).forEach(id => {
    const o = ROMANCE_LAN_PA_OVERRIDES[id], p = packLan[id];
    if(!p){ structOk = false; return; }
    if(o.phase !== p.phase || o.artId !== p.artId || o.romanceLine !== p.romanceLine || o.arcBeat !== p.arcBeat) structOk = false;
    if(canon(o.openConditions || []) !== canon(p.openConditions || [])) structOk = false;
    if(canon(o.openConditionsAny || null) !== canon(p.openConditionsAny || null)) structOk = false;
    if(canon((o.flags_written || []).slice().sort()) !== canon((p.flags_written || []).slice().sort())) structOk = false;
    if((o.choices || []).length !== (p.choices || []).length) structOk = false;
    (o.choices || []).forEach((c, i) => {
      const pc = (p.choices || [])[i];
      if(!pc || c.id !== pc.id) structOk = false;
      /* effects 嘅狀態部分（flags＋stats）必須同 pack 逐項一致；notes 係玩家可見文字，
         屬文字層——pack 原 notes 有歌手向字眼（合唱推進／狗仔護航／助抗聯姻），已改寫，另行驗零歌手向 */
      /* v20a100 CLEAN100 B-03 唯一例外：R_lan_push1 兩抉擇嘅 stats.music 係 PA 化漏網嘅
         歌手向殘留（嗰幕係對通告牌、冇唱歌；music 鍵連 applyChoice 映射都冇），已改 stage。
         比較前將 pack 嗰兩處 music 正規化做 stage；其餘全部仍須逐項一致。 */
      else if(canon((c.effects || {}).flags || []) !== canon((pc.effects || {}).flags || [])
           || canon((c.effects || {}).stats || {}) !== canon(normStats100(id, pc))) structOk = false;
      else if(singerWords.some(w => String((c.effects || {}).notes || '').includes(w))) proseOk = false;
    });
    const prose = JSON.stringify({ t: o.title, s: o.setting, y: o.synopsis, b: o.beats, l: (o.choices || []).map(c => c.label) });
    if(singerWords.some(w => prose.includes(w))) proseOk = false;
    if(!prose.includes('藍若曦')) proseOk = false;
  });
  ok('藍 PA：五節點結構層（phase/oc/choice id/effects/旗）同 pack 逐項一致', structOk);
  ok('藍 PA：文字層零歌手向字眼（唱片店/錄音室/合唱/狗仔/緋聞/聯姻/豪門…）', proseOk);
  const xu = STORY_WIRE.romance.lanXu.nodes.find(n => n.id === 'R_xu_meet');
  ok('藍 PA：R_xu_* 無被覆寫（徐寶珊維持富豪千金原線）', !!xu && xu.title === '春茗初遇');
  ok('半線狀態可讀：endingRomanceState48 五線齊（空存檔全 false/0）',
     (() => { const st = endingRomanceState48(); return ['hiu','choi','vera','lan','xu'].every(k => st[k] && st[k].met === false && st[k].rel === 0 && st[k].committed === false); })());
}

/* ---- N12＝C15 ---- */
function c15Save(over){
  return baseSave(Object.assign({
    dayIndex: dayIndexOf(1992, 4, 15), fame: 20,
    castingTags: [{ id: 'tag_action', label: '動作演員' }],
  }, over || {}));
}
loadGame(c15Save());
ok('C15：1992 春＋動作標籤 → offer 喺 film_harbour', !!openRow('C15') && openRow('C15').locId === 'film_harbour');
loadGame(c15Save({ castingTags: [] }));
ok('C15：冇動作標籤唔出現', !openIds().includes('C15'));
loadGame(c15Save({ dayIndex: dayIndexOf(1991, 4, 15) }));
ok('C15：1991 唔出現', !openIds().includes('C15'));
loadGame(c15Save({ dayIndex: dayIndexOf(1992, 7, 15) }));
ok('C15：1992 夏（非春）唔出現', !openIds().includes('C15'));
{
  const s = loadGame(c15Save());
  StoryOC.applyChoice(node('C15'), choice('C15', 'C15_a'));
  ok('C15_a：done＋flag_stunt_double＋聲量 20→23＋「搏命」標籤',
     StoryOC.isDone('C15') && !!StoryOC.getFlag('flag_stunt_double') && s.fame === 23 && s.castingTags.some(t => t.label === '搏命'));
  story48SettleTick();
  ok('C15_a：tick 登記債權 credit_c15_stunt＋ledger credits=1',
     s.mockCredits.some(c => c.id === 'credit_c15_stunt') && favorLedgerCounts().credits === 1);
  story48SettleTick();
  ok('C15_a：tick 重行唔雙計', s.mockCredits.filter(c => c.id === 'credit_c15_stunt').length === 1 && favorLedgerCounts().credits === 1);
}
{
  const s = loadGame(c15Save());
  StoryOC.applyChoice(node('C15'), choice('C15', 'C15_b'));
  story48SettleTick();
  ok('C15_b：flag_stunt_refuse＋「惜身」標籤＋tick 唔登記債權',
     !!StoryOC.getFlag('flag_stunt_refuse') && s.castingTags.some(t => t.label === '惜身') && !s.mockCredits.some(c => c.id === 'credit_c15_stunt'));
}

/* ---- N13＝C14 ---- */
function c14Save(over){
  return baseSave(Object.assign({
    dayIndex: dayIndexOf(1992, 7, 15), fame: 30, industryCreditDelta: 30,
    story: { flags: {}, rel: {}, done: { C5: true, C7: true, C9: true, C10: true }, choices: {} },
  }, over || {}));
}
loadGame(c14Save());
ok('C14：1992 夏＋C10 done＋信用 47（>42）→ offer', !!openRow('C14'));
loadGame(c14Save({ industryCreditDelta: 25 })); /* 信用 = 17+25 = 42 */
ok('C14：信用=42（嚴格 >42）唔出現', !openIds().includes('C14'));
loadGame(c14Save({ story: { flags: {}, rel: {}, done: { C5: true, C7: true, C9: true }, choices: {} } }));
ok('C14：C10 未做唔出現', !openIds().includes('C14'));
{
  const s = loadGame(c14Save());
  StoryOC.applyChoice(node('C14'), choice('C14', 'C14_a'));
  ok('C14_a：flag_side_tv＋信用 delta 30→32', !!StoryOC.getFlag('flag_side_tv') && s.industryCreditDelta === 32);
}
{
  const s = loadGame(c14Save());
  StoryOC.applyChoice(node('C14'), choice('C14', 'C14_b'));
  ok('C14_b：flag_side_film＋聲量 30→32', !!StoryOC.getFlag('flag_side_film') && s.fame === 32);
}

/* ---- N14＝C12 ---- */
function c12Save(over){
  return baseSave(Object.assign({
    dayIndex: dayIndexOf(1992, 10, 15), fame: 55,
    story: { flags: {}, rel: {}, done: { C10: true, C14: true }, choices: {} },
  }, over || {}));
}
loadGame(c12Save());
ok('C12：1992 秋＋C14 done＋聲量 55 → offer 喺 rec_star', !!openRow('C12') && openRow('C12').locId === 'rec_star');
loadGame(c12Save({ fame: 50 }));
ok('C12：聲量=50（嚴格 >50）唔出現', !openIds().includes('C12'));
loadGame(c12Save({ story: { flags: {}, rel: {}, done: { C10: true }, choices: {} } }));
ok('C12：C14 未做唔出現', !openIds().includes('C12'));
{
  const s = loadGame(c12Save());
  StoryOC.applyChoice(node('C12'), choice('C12', 'C12_a'));
  ok('C12_a：flag_fans_support＋聲量 55→57＋「親和力」標籤',
     !!StoryOC.getFlag('flag_fans_support') && s.fame === 57 && s.castingTags.some(t => t.label === '親和力'));
}
{
  const s = loadGame(c12Save());
  StoryOC.applyChoice(node('C12'), choice('C12', 'C12_b'));
  ok('C12_b：flag_fans_avoid＋「高冷」標籤', !!StoryOC.getFlag('flag_fans_avoid') && s.castingTags.some(t => t.label === '高冷'));
}

/* ---- N15＝C16 ---- */
function c16Save(over){
  return baseSave(Object.assign({
    dayIndex: dayIndexOf(1992, 11, 15), fame: 60, industryCreditDelta: 38,
    story: { flags: {}, rel: {}, done: { C10: true, C14: true, C12: true }, choices: {} },
  }, over || {}));
}
loadGame(c16Save()); /* 雙軌 = 60 + (32+38) = 130 */
ok('C16：1992 秋＋C12 done＋雙軌 130（>125）→ offer', !!openRow('C16'));
loadGame(c16Save({ industryCreditDelta: 33 })); /* 雙軌 = 60 + 65 = 125 */
ok('C16：雙軌=125（嚴格 >125）唔出現', !openIds().includes('C16'));
loadGame(c16Save({ story: { flags: {}, rel: {}, done: { C10: true, C14: true }, choices: {} } }));
ok('C16：C12 未做唔出現', !openIds().includes('C16'));
{
  const s = loadGame(c16Save());
  StoryOC.applyChoice(node('C16'), choice('C16', 'C16_a'));
  ok('C16_a：flag_vocal_polish＋「偶像派」標籤＋聲量 60→62',
     !!StoryOC.getFlag('flag_vocal_polish') && s.castingTags.some(t => t.label === '偶像派') && s.fame === 62);
}
{
  const s = loadGame(c16Save());
  StoryOC.applyChoice(node('C16'), choice('C16', 'C16_b'));
  ok('C16_b：flag_vocal_train＋「實力派」標籤＋信用 delta +2',
     !!StoryOC.getFlag('flag_vocal_train') && s.castingTags.some(t => t.label === '實力派') && s.industryCreditDelta === 40);
}

/* ---- N16＝C13 ---- */
loadGame(baseSave({ dayIndex: dayIndexOf(1992, 12, 15) }));
ok('C13：1992 冬 → offer 喺 film_cotton', !!openRow('C13') && openRow('C13').locId === 'film_cotton');
loadGame(baseSave({ dayIndex: dayIndexOf(1992, 10, 15) }));
ok('C13：1992 秋唔出現', !openIds().includes('C13'));
{
  const s = loadGame(baseSave({ dayIndex: dayIndexOf(1992, 12, 15) }));
  StoryOC.applyChoice(node('C13'), choice('C13', 'C13_a'));
  ok('C13_a：flag_newyear_improv＋「執生」標籤', !!StoryOC.getFlag('flag_newyear_improv') && s.castingTags.some(t => t.label === '執生'));
  story48SettleTick();
  ok('C13_a：tick 登記債權 credit_c13_newyear＋ledger credits=1',
     s.mockCredits.some(c => c.id === 'credit_c13_newyear') && favorLedgerCounts().credits === 1);
  story48SettleTick();
  ok('C13_a：tick 重行唔雙計', favorLedgerCounts().credits === 1);
}
{
  const s = loadGame(baseSave({ dayIndex: dayIndexOf(1992, 12, 15) }));
  StoryOC.applyChoice(node('C13'), choice('C13', 'C13_b'));
  story48SettleTick();
  ok('C13_b：flag_newyear_script＋tick 唔登記債權',
     !!StoryOC.getFlag('flag_newyear_script') && !s.mockCredits.some(c => c.id === 'credit_c13_newyear'));
}

/* ---- C6 真路徑＋回歸 ---- */
{
  const s = loadGame(baseSave({ dayIndex: 98, money: 900, story: { flags: { route_tv: true }, rel: {}, done: { C1: true, C2: true, C3: true, C4: true, C5: true }, choices: {} } }));
  ok('C6：route_tv＋W15 開（標題已對齊「飯堂閒角」）', !!openRow('C6') && node('C6').title === '飯堂閒角');
  StoryOC.applyChoice(node('C6'), choice('C6', 'C6_a'));
  ok('C6_a：flag_canteen_grind＋微量金錢 900→1400（wealth 1）', !!StoryOC.getFlag('flag_canteen_grind') && s.money === 1400);
}
{
  loadGame(baseSave({ dayIndex: 98, story: { flags: { route_tv: true }, rel: {}, done: { C1: true, C2: true, C3: true, C4: true, C5: true }, choices: {} } }));
  StoryOC.applyChoice(node('C6'), choice('C6', 'C6_b'));
  ok('C6_b：flag_canteen_quit', !!StoryOC.getFlag('flag_canteen_quit'));
}
loadGame(baseSave({ dayIndex: 1, fame: 5 }));
ok('回歸：C1 開局可開', openIds().includes('C1'));
loadGame(baseSave({ dayIndex: dayIndexOf(1991, 7, 15), story: { flags: {}, rel: {}, done: { C5: true }, choices: {} }, industryCreditDelta: 25 }));
ok('回歸：C7（4-6）照開', openIds().includes('C7'));

/* ---- 程天諾預熱：真 paperSideItemForDay 年份閘 ---- */
{
  const chengItems = PAPER_SIDE_ITEMS.filter(it => (it.h || '').includes('程天諾'));
  ok('預熱：程天諾花邊共 3 則、全數 fromYear=1992', chengItems.length === 3 && chengItems.every(it => it.fromYear === 1992));
  loadGame(baseSave({ dayIndex: dayIndexOf(1991, 6, 1) }));
  let hit89 = 0;
  for(let d = 0; d < 365; d++){ S.dayIndex = dayIndexOf(1991, 1, 1) + d; const it = paperSideItemForDay(S.dayIndex); if(it && (it.headline || '').includes('程天諾')) hit89++; }
  ok('預熱：1991 全年 picker 唔出程天諾', hit89 === 0);
  loadGame(baseSave({ dayIndex: dayIndexOf(1992, 6, 1) }));
  const seen90 = {};
  for(let d = 0; d < 365; d++){ S.dayIndex = dayIndexOf(1992, 1, 1) + d; const it = paperSideItemForDay(S.dayIndex); if(it && (it.headline || '').includes('程天諾')) seen90[it.headline] = true; }
  ok('預熱：1992 全年 picker 出齊 3 則程天諾', Object.keys(seen90).length === 3);
}

/* ---- 感情 commit 機制 ---- */
function cmtSave(over){
  return baseSave(Object.assign({
    dayIndex: dayIndexOf(1992, 10, 15),
    story: { flags: {}, rel: { rel_hiu: 7 }, done: { R_hiu_meet: true, R_hiu_crisis: true }, choices: {} },
  }, over || {}));
}
loadGame(cmtSave());
ok('commit：曉晴 rel 7＋crisis done＋1992 秋 → tvb_longmen 出 offer',
   commit48ActionsAt('tvb_longmen').some(a => a.id === 'CMT_hiu_commit'));
ok('commit：采兒未達標 → cafe_cha 唔出 offer', commit48ActionsAt('cafe_cha').length === 0);
loadGame(cmtSave({ dayIndex: dayIndexOf(1991, 10, 15) }));
ok('commit：1991（窗口外）rel 達標都唔出', !commit48Available('CMT_hiu_commit'));
loadGame(cmtSave({ dayIndex: dayIndexOf(1992, 7, 15) }));
ok('commit：1992 夏（未入秋）唔出', !commit48Available('CMT_hiu_commit'));
loadGame(cmtSave({ story: { flags: {}, rel: { rel_hiu: 5 }, done: { R_hiu_meet: true, R_hiu_crisis: true }, choices: {} } }));
ok('commit：rel 5（<6）唔出', !commit48Available('CMT_hiu_commit'));
loadGame(cmtSave({ story: { flags: {}, rel: { rel_hiu: 6 }, done: { R_hiu_meet: true, R_hiu_crisis: true }, choices: {} } }));
ok('commit：rel 6（＝門檻）出', commit48Available('CMT_hiu_commit'));
loadGame(cmtSave({ story: { flags: {}, rel: { rel_hiu: 7 }, done: { R_hiu_meet: true }, choices: {} } }));
ok('commit：crisis 未做唔出（唔提早收束）', !commit48Available('CMT_hiu_commit'));
loadGame(cmtSave({ story: { flags: { flag_choi_commit: true }, rel: { rel_hiu: 7 }, done: { R_hiu_meet: true, R_hiu_crisis: true }, choices: {} } }));
ok('commit：已 commit 采兒 → 曉晴唔再出（互斥）', !commit48Available('CMT_hiu_commit'));
{
  played48 = [];
  loadGame(cmtSave());
  ok('commit：commit48Play 行真 StoryPlay 入口', commit48Play('CMT_hiu_commit') === true && played48.includes('CMT_hiu_commit'));
  const s = S;
  StoryOC.applyChoice(COMMIT48_NODES.CMT_hiu_commit, COMMIT48_NODES.CMT_hiu_commit.choices[0]);
  ok('commit：確認 choice 落 flag_hiu_commit（真 applyChoice）', !!StoryOC.getFlag('flag_hiu_commit'));
  ok('commit：落旗後本線 offer 消失', !commit48Available('CMT_hiu_commit'));
  ok('commit：newspaperStoryResolve 對 commit 節點回 null（唔生報紙）',
     newspaperStoryResolve(COMMIT48_NODES.CMT_hiu_commit, COMMIT48_NODES.CMT_hiu_commit.choices[0]) === null);
  const st = endingRomanceState48();
  ok('commit：endingRomanceState48 讀到 hiu.committed＋rel 7', st.hiu.committed === true && st.hiu.rel === 7 && st.hiu.met === true);
  ok('commit：互斥——曉晴 commit 後采兒就算達標都唔出',
     !commit48Available('CMT_choi_commit'));
}
{
  loadGame(baseSave({
    dayIndex: dayIndexOf(1992, 12, 1),
    story: { flags: {}, rel: { rel_choi: 6 }, done: { R_choi_meet: true, R_choi_crisis: true }, choices: {} },
  }));
  ok('commit：采兒 rel 6＋crisis done＋1992 冬 → cafe_cha 出 offer',
     commit48ActionsAt('cafe_cha').some(a => a.id === 'CMT_choi_commit'));
  StoryOC.applyChoice(COMMIT48_NODES.CMT_choi_commit, COMMIT48_NODES.CMT_choi_commit.choices[1]);
  ok('commit：「再諗下」唔落旗', !StoryOC.getFlag('flag_choi_commit'));
  ok('commit：「再諗下」後 offer 仍然留返（唔查 done）', commit48Available('CMT_choi_commit'));
  StoryOC.applyChoice(COMMIT48_NODES.CMT_choi_commit, COMMIT48_NODES.CMT_choi_commit.choices[0]);
  ok('commit：之後確認照樣落 flag_choi_commit', !!StoryOC.getFlag('flag_choi_commit'));
  ok('commit：newspaperStoryResolve 對采兒 commit 回 null',
     newspaperStoryResolve(COMMIT48_NODES.CMT_choi_commit, COMMIT48_NODES.CMT_choi_commit.choices[0]) === null);
}

console.log('\nWEAVE_PHASE4_8 邏輯測試：' + pass + ' 過 / ' + fail + ' 失敗');
process.exit(fail ? 1 : 0);
