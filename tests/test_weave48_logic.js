// WEAVE_PHASE4_8 邏輯測試（v20a31）：
// 行真路徑——JSON pack 主幹節點（v20a234：內嵌覆寫表已刪，N12–N16／N6 由 pack 直出，唯一來源）
// ＋ 藍 PA 線由 content/story_detail_romance_lan_xu.json 直出（v20a242：ROMANCE_LAN_PA_OVERRIDES 已刪，JSON 唯一來源）
// → StoryOC.listOpen({player:true}) 真 offer 路徑
// → StoryOC.applyChoice 真寫入 → story48SettleTick 真結算（N12／N16 債權登記）
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
const pack = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'content', 'story_detail_n1_to_n17.json'), 'utf8'));
const romVHC = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'story_detail_romance_vera_hiu_choi.json'), 'utf8'));
const romLX = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'content', 'story_detail_romance_lan_xu.json'), 'utf8'));

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
  extractFn('function story46SettleTick'),
  extractFn('function story48SettleTick'),
  extractFn('function newspaperStoryLists'),
  extractFn('function newspaperStoryResolve'),
  extractFn('function paperSideItemForDay'),
  extractConst('STORY_GATE_3Y'),
  extractConst('STORY_LOC_SOFT'),
  extractConst('STORY_HINT_SOFT'),
  extractConst('STORY_TITLE_SOFT'),
  extractConst('STORY46_CREDIT_N7'),
  extractConst('STORY46_CREDIT_N10'),
  extractConst('STORY46_GIFT_ID'),
  extractConst('STORY48_CREDIT_N12'),
  extractConst('STORY48_CREDIT_N16'),
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
 .replace('const STORY_LOC_SOFT =', 'var STORY_LOC_SOFT =')
 .replace('const STORY_HINT_SOFT =', 'var STORY_HINT_SOFT =')
 .replace('const STORY_TITLE_SOFT =', 'var STORY_TITLE_SOFT =')
 .replace('const STORY46_CREDIT_N7 =', 'var STORY46_CREDIT_N7 =')
 .replace('const STORY46_CREDIT_N10 =', 'var STORY46_CREDIT_N10 =')
 .replace('const STORY46_GIFT_ID =', 'var STORY46_GIFT_ID =')
 .replace('const STORY48_CREDIT_N12 =', 'var STORY48_CREDIT_N12 =')
 .replace('const STORY48_CREDIT_N16 =', 'var STORY48_CREDIT_N16 =')
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

ok('harness: StoryOC/commit48 載入',
   typeof StoryOC === 'object' && typeof commit48Available === 'function');
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

/* ---- 主幹完整性（v20a234：pack 直出，唔再經覆寫） ---- */
loadGame(baseSave());
{
  const t = { N12: ['墊', 'film_harbour', '麥震東'], N13: ['高爾夫球', 'tvb_longmen', '齊鎮海'],
              N14: ['樂壇前哨', 'rec_star', '陸柏言'], N15: ['錄音室', 'rec_star', '程天諾'],
              N16: ['飛紙仔', 'film_cotton', '廖炳星'] };
  let allOk = true;
  Object.keys(t).forEach(id => {
    const n = node(id);
    if(!n || n.title !== t[id][0] || n.locId !== t[id][1] || !JSON.stringify(n).includes(t[id][2]) || !n.playerOffer) allOk = false;
  });
  ok('主幹完整性：1992 五節點標題／場地／紅星跟主幹', allOk);
  const stale = ['賀歲搶位', '緋聞公關真假', '尊重或包養', '聯姻逼退圈', '舊底片', '金九'];
  let clean = true;
  ['N14','N16','N13','N12','N15'].forEach(id => { if(stale.some(w => JSON.stringify(node(id)).includes(w))) clean = false; });
  ok('主幹完整性：pack 自創線殘留字串清零（金九舊底片等）', clean);
  const c6 = node('N6');
  ok('N6 對齊 Qwen：標題「角落那張枱」（v250 新短詞標題）＋場地 tvb_longmen＋無約會旗／無 rel 加成',
     c6.title === '角落那張枱' && c6.locId === 'tvb_longmen'
     && !JSON.stringify(c6).includes('date_')
     && (c6.choices || []).every(c => !Object.keys(((c.effects || {}).stats) || {}).some(k => k.startsWith('rel_')))
     && StoryOC.getFlag && c6.flags_written.includes('flag_canteen_grind'));
}

/* ---- 藍 PA 線（v20a242：覆寫表已刪，R_lan_* 由 content JSON 直出，唯一來源） ---- */
{
  const lanNodes = {};
  STORY_WIRE.romance.lanXu.nodes.forEach(n => { if(n.id.startsWith('R_lan_')) lanNodes[n.id] = n; });
  const ids = ['R_lan_meet','R_lan_push1','R_lan_push2','R_lan_crisis','R_lan_ending'];
  const singerWords = ['唱片店', '錄音室', '合唱', '狗仔', '緋聞', '聯姻', '豪門', '退圈', '登機證', '唱歌', '歌手', '情侶檔'];
  let structOk = true, proseOk = true;
  const wantBeats = { R_lan_meet: 6, R_lan_push1: 5, R_lan_push2: 5, R_lan_crisis: 6, R_lan_ending: 9 }; /* v20a159 ROM159：crisis 重寫加一拍（阿爸親自到電視台），5→6 */
  const wantPhase = { R_lan_meet: 'P2', R_lan_push1: 'P2', R_lan_push2: 'P2', R_lan_crisis: 'P4', R_lan_ending: 'P5' };
  ids.forEach(id => {
    const n = lanNodes[id];
    if(!n){ structOk = false; return; }
    if((n.beats || []).length !== wantBeats[id]) structOk = false;
    if(n.playerOffer !== false) structOk = false;
    if(n.phase !== wantPhase[id]) structOk = false;
    if(!n.artId || n.romanceLine !== 'lan' || !n.arcBeat) structOk = false;
    if((n.choices || []).length !== 2) structOk = false;
    (n.choices || []).forEach(c => {
      const st = ((c.effects || {}).stats) || {};
      if('music' in st) structOk = false;
      if(singerWords.some(w => String((c.effects || {}).notes || '').includes(w))) proseOk = false;
    });
    const prose = JSON.stringify({ t: n.title, s: n.setting, y: n.synopsis, b: n.beats, l: (n.choices || []).map(c => c.label) });
    if(singerWords.some(w => prose.includes(w))) proseOk = false;
    if(!prose.includes('藍若曦') || (!prose.includes('場記') && !prose.includes('通告牌'))) proseOk = false;
  });
  ok('藍 PA：五節點 JSON 直出（beats 6/5/5/6/9、playerOffer false、結構層齊）', structOk);
  ok('藍 PA：文字層零歌手向字眼（唱片店/錄音室/合唱/狗仔/緋聞/聯姻/豪門…）＋PA 框架在位', proseOk);
  const p1 = lanNodes.R_lan_push1;
  const sang = (p1.choices || []).find(c => (c.effects && c.effects.flags || []).indexOf('flag_lan_sang_together') >= 0);
  ok('藍 PA：push1「一齊捱過」抉擇 stage:1（v20a100 修正已入 JSON，唔再靠覆寫表）',
     !!(sang && sang.effects.stats.stage === 1 && sang.effects.stats.rel_lan === 2));
  const end = lanNodes.R_lan_ending;
  ok('藍 PA：ending 抉擇 label／notes 係 JSON（RW-3）版',
     end.choices[0].label === '接住那個約定：那頓飯，我記住，不會失約'
     && end.choices[1].label === '收起那一步：笑著，當作一個約定');
  const xu = STORY_WIRE.romance.lanXu.nodes.find(n => n.id === 'R_xu_meet');
  ok('藍 PA：R_xu_* 無被覆寫（徐寶珊維持富豪千金原線）', !!xu && xu.title === '春茗初遇');
  ok('半線狀態可讀：endingRomanceState48 六線齊（v297 vera 已刪；空存檔全 false/0）',
     (() => { const st = endingRomanceState48(); return ['hiu','choi','lan','xu','yip','so'].every(k => st[k] && st[k].met === false && st[k].rel === 0 && st[k].committed === false); })());
}

/* ---- N12（v20a113：補鏈，需 N11 done） ---- */
function c15Save(over){
  return baseSave(Object.assign({
    dayIndex: dayIndexOf(1992, 4, 15), fame: 20,
    castingTags: [{ id: 'tag_action', label: '動作演員' }],
    story: { flags: {}, rel: {}, done: { N11: true }, choices: {} },
  }, over || {}));
}
loadGame(c15Save());
ok('N12：1992 春＋動作標籤 → offer 喺 film_harbour', !!openRow('N12') && openRow('N12').locId === 'film_harbour');
loadGame(c15Save({ story: { flags: {}, rel: {}, done: {}, choices: {} } }));
ok('N12：N11 未做唔出現', !openIds().includes('N12'));
loadGame(c15Save({ castingTags: [] }));
ok('N12：冇動作標籤唔出現', !openIds().includes('N12'));
loadGame(c15Save({ dayIndex: dayIndexOf(1991, 4, 15) }));
ok('N12：1991 唔出現', !openIds().includes('N12'));
loadGame(c15Save({ dayIndex: dayIndexOf(1992, 7, 15) }));
ok('N12：1992 夏（非春）唔出現', !openIds().includes('N12'));
{
  const s = loadGame(c15Save());
  StoryOC.applyChoice(node('N12'), choice('N12', 'N12_a'));
  ok('N12_a：done＋flag_stunt_double＋聲量 20→23＋「搏命」標籤',
     StoryOC.isDone('N12') && !!StoryOC.getFlag('flag_stunt_double') && s.fame === 23 && s.castingTags.some(t => t.label === '搏命'));
  story48SettleTick();
  ok('N12_a：tick 登記債權 credit_c15_stunt＋ledger credits=1',
     s.mockCredits.some(c => c.id === 'credit_c15_stunt') && favorLedgerCounts().credits === 1);
  story48SettleTick();
  ok('N12_a：tick 重行唔雙計', s.mockCredits.filter(c => c.id === 'credit_c15_stunt').length === 1 && favorLedgerCounts().credits === 1);
}
{
  const s = loadGame(c15Save());
  StoryOC.applyChoice(node('N12'), choice('N12', 'N12_b'));
  story48SettleTick();
  ok('N12_b：flag_stunt_refuse＋「惜身」標籤＋tick 唔登記債權',
     !!StoryOC.getFlag('flag_stunt_refuse') && s.castingTags.some(t => t.label === '惜身') && !s.mockCredits.some(c => c.id === 'credit_c15_stunt'));
}

/* ---- N13 ---- */
function c14Save(over){
  return baseSave(Object.assign({
    dayIndex: dayIndexOf(1992, 7, 15), fame: 30, industryCreditDelta: 30,
    story: { flags: {}, rel: {}, done: { N5: true, N7: true, N10: true, N11: true }, choices: {} },
  }, over || {}));
}
loadGame(c14Save());
ok('N13：1992 夏＋N11 done＋信用 47（>42）→ offer', !!openRow('N13'));
loadGame(c14Save({ industryCreditDelta: 25 })); /* 信用 = 17+25 = 42 */
ok('N13：信用=42（嚴格 >42）唔出現', !openIds().includes('N13'));
loadGame(c14Save({ story: { flags: {}, rel: {}, done: { N5: true, N7: true, N10: true }, choices: {} } }));
ok('N13：N11 未做唔出現', !openIds().includes('N13'));
{
  const s = loadGame(c14Save());
  StoryOC.applyChoice(node('N13'), choice('N13', 'N13_a'));
  ok('N13_a：flag_side_tv＋信用 delta 30→32', !!StoryOC.getFlag('flag_side_tv') && s.industryCreditDelta === 32);
}
{
  const s = loadGame(c14Save());
  StoryOC.applyChoice(node('N13'), choice('N13', 'N13_b'));
  ok('N13_b：flag_side_film＋聲量 30→32', !!StoryOC.getFlag('flag_side_film') && s.fame === 32);
}

/* ---- N14 ---- */
function c12Save(over){
  return baseSave(Object.assign({
    dayIndex: dayIndexOf(1992, 10, 15), fame: 55,
    story: { flags: {}, rel: {}, done: { N11: true, N13: true }, choices: {} },
  }, over || {}));
}
loadGame(c12Save());
ok('N14：1992 秋＋N13 done＋聲量 55 → offer 喺 rec_star', !!openRow('N14') && openRow('N14').locId === 'rec_star');
loadGame(c12Save({ fame: 50 }));
ok('N14：聲量=50（嚴格 >50）唔出現', !openIds().includes('N14'));
loadGame(c12Save({ story: { flags: {}, rel: {}, done: { N11: true }, choices: {} } }));
ok('N14：N13 未做唔出現', !openIds().includes('N14'));
{
  const s = loadGame(c12Save());
  StoryOC.applyChoice(node('N14'), choice('N14', 'N14_a'));
  ok('N14_a：flag_fans_support＋聲量 55→57＋「親和力」標籤',
     !!StoryOC.getFlag('flag_fans_support') && s.fame === 57 && s.castingTags.some(t => t.label === '親和力'));
}
{
  const s = loadGame(c12Save());
  StoryOC.applyChoice(node('N14'), choice('N14', 'N14_b'));
  ok('N14_b：flag_fans_avoid＋「高冷」標籤', !!StoryOC.getFlag('flag_fans_avoid') && s.castingTags.some(t => t.label === '高冷'));
}

/* ---- N15 ---- */
function c16Save(over){
  return baseSave(Object.assign({
    dayIndex: dayIndexOf(1992, 11, 15), fame: 60, industryCreditDelta: 38,
    story: { flags: {}, rel: {}, done: { N11: true, N13: true, N14: true }, choices: {} },
  }, over || {}));
}
loadGame(c16Save()); /* 雙軌 = 60 + (32+38) = 130 */
ok('N15：1992 秋＋N14 done＋雙軌 130（>125）→ offer', !!openRow('N15'));
loadGame(c16Save({ industryCreditDelta: 33 })); /* 雙軌 = 60 + 65 = 125 */
ok('N15：雙軌=125（嚴格 >125）唔出現', !openIds().includes('N15'));
loadGame(c16Save({ story: { flags: {}, rel: {}, done: { N11: true, N13: true }, choices: {} } }));
ok('N15：N14 未做唔出現', !openIds().includes('N15'));
{
  const s = loadGame(c16Save());
  StoryOC.applyChoice(node('N15'), choice('N15', 'N15_a'));
  ok('N15_a：flag_vocal_polish＋「偶像派」標籤＋聲量 60→62',
     !!StoryOC.getFlag('flag_vocal_polish') && s.castingTags.some(t => t.label === '偶像派') && s.fame === 62);
}
{
  const s = loadGame(c16Save());
  StoryOC.applyChoice(node('N15'), choice('N15', 'N15_b'));
  ok('N15_b：flag_vocal_train＋「實力派」標籤＋信用 delta +2',
     !!StoryOC.getFlag('flag_vocal_train') && s.castingTags.some(t => t.label === '實力派') && s.industryCreditDelta === 40);
}

/* ---- N16 ---- */
loadGame(baseSave({ dayIndex: dayIndexOf(1992, 12, 15) }));
ok('N16：1992 冬 → offer 喺 film_cotton', !!openRow('N16') && openRow('N16').locId === 'film_cotton');
loadGame(baseSave({ dayIndex: dayIndexOf(1992, 10, 15) }));
ok('N16：1992 秋唔出現', !openIds().includes('N16'));
{
  const s = loadGame(baseSave({ dayIndex: dayIndexOf(1992, 12, 15) }));
  StoryOC.applyChoice(node('N16'), choice('N16', 'N16_a'));
  ok('N16_a：flag_newyear_improv＋「執生」標籤', !!StoryOC.getFlag('flag_newyear_improv') && s.castingTags.some(t => t.label === '執生'));
  story48SettleTick();
  ok('N16_a：tick 登記債權 credit_c13_newyear＋ledger credits=1',
     s.mockCredits.some(c => c.id === 'credit_c13_newyear') && favorLedgerCounts().credits === 1);
  story48SettleTick();
  ok('N16_a：tick 重行唔雙計', favorLedgerCounts().credits === 1);
}
{
  const s = loadGame(baseSave({ dayIndex: dayIndexOf(1992, 12, 15) }));
  StoryOC.applyChoice(node('N16'), choice('N16', 'N16_b'));
  story48SettleTick();
  ok('N16_b：flag_newyear_script＋tick 唔登記債權',
     !!StoryOC.getFlag('flag_newyear_script') && !s.mockCredits.some(c => c.id === 'credit_c13_newyear'));
}

/* ---- N6 真路徑＋回歸 ---- */
{
  const s = loadGame(baseSave({ dayIndex: 98, money: 900, story: { flags: { route_tv: true }, rel: {}, done: { N1: true, N2: true, N3: true, N4: true, N5: true }, choices: {} } }));
  ok('N6：route_tv＋W15 開（標題已對齊「角落那張枱」，v250）', !!openRow('N6') && node('N6').title === '角落那張枱');
  StoryOC.applyChoice(node('N6'), choice('N6', 'N6_a'));
  ok('N6_a：flag_canteen_grind＋微量金錢 900→1400（wealth 1）', !!StoryOC.getFlag('flag_canteen_grind') && s.money === 1400);
}
{
  loadGame(baseSave({ dayIndex: 98, story: { flags: { route_tv: true }, rel: {}, done: { N1: true, N2: true, N3: true, N4: true, N5: true }, choices: {} } }));
  StoryOC.applyChoice(node('N6'), choice('N6', 'N6_b'));
  ok('N6_b：flag_canteen_quit', !!StoryOC.getFlag('flag_canteen_quit'));
}
loadGame(baseSave({ dayIndex: 1, fame: 5 }));
ok('回歸：N1 開局可開', openIds().includes('N1'));
loadGame(baseSave({ dayIndex: dayIndexOf(1991, 7, 15), story: { flags: {}, rel: {}, done: { N5: true }, choices: {} }, industryCreditDelta: 25 }));
ok('回歸：N7（4-6）照開', openIds().includes('N7'));

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
