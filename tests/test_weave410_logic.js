// WEAVE_PHASE4_10 邏輯測試（v20a33）：結局系統。
// 行真路徑——STORY_SPINE_NODE_C17_410 覆寫（applyStorySpineOverrides410 套落真 pack nodes）
// → StoryOC.listOpen 真閘（STORY_GATE_3Y C17：C13 done＋1990 冬）→ ending410EveNode 動態重建
// （choices＝endingEveOptions410 相鄰規則）→ StoryOC.applyChoice 真寫入
// → ending410AfterEveChoice 真組裝（resolveEnding410 判定＋S.ending410 落檔＋modal 逐頁呈現）。
// resolveEnding410 判定矩陣用合成狀態逐個命中；純函數深等驗證；
// endingFavor410／endingRomance410 同生產讀取口（favorLedgerCounts／endingRomanceState48）交叉對照。
// 用法：node tests/test_weave410_logic.js
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
var StoryPlay = { start(){ return true; } };
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
var modalPages410 = [];
var modal = function(htmlStr, buttons){ modalPages410.push({ html: htmlStr, buttons: buttons || [] }); };

const SRC = [
  "var START = { y:1988, m:3, d:7 };",
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
  extractFn('function favorLedgerCounts'),
  extractFn('function choice47StoryFlag'),
  extractFn('function choice47StoryDone'),
  extractFn('function commit48Rel'),
  extractFn('function endingRomanceState48'),
  extractFn('function newspaperNameTier'),
  extractFn('function trajTagCounts49'),
  extractFn('function trajectoryOf49'),
  extractFn('function newspaperTrajRef49'),
  extractFn('function newspaperStoryLists'),
  extractFn('function newspaperStoryResolve'),
  extractFn('function endingFlag410'),
  extractFn('function endingDual410'),
  extractFn('function endingNegTagCount410'),
  extractFn('function endingBackstageTagCount410'),
  extractFn('function endingFavor410'),
  extractFn('function endingRomance410'),
  extractFn('function endingE2Eligible410'),
  extractFn('function endingE3Eligible410'),
  extractFn('function endingBackstageClose410'),
  extractFn('function resolveEnding410'),
  extractFn('function endingEveOptions410'),
  extractFn('function applyStorySpineOverrides410'),
  extractFn('function ending410EveNode'),
  extractFn('function endingEsc410'),
  extractFn('function endingCareerScene410'),
  extractFn('function endingRomanceScene410'),
  extractFn('function endingExodusScene410'),
  extractFn('function endingInserts410'),
  extractFn('function endingSummaryHtml410'),
  extractFn('function showEndingSummary410'),
  extractFn('function ending410AfterEveChoice'),
  extractConst('STORY_GATE_3Y'),
  extractConst('STORY_LOC_SOFT'),
  extractConst('STORY_HINT_SOFT'),
  extractConst('STORY_TITLE_SOFT'),
  extractConst('STORY_FLAG_EVENT'),
  extractConst('STORY_PAPER_SKIP'),
  extractConst('TRAJ49_TAG_SETS'),
  "var TRAJ49_IDOL_GAP=15, TRAJ49_IDOL_FAME=30, TRAJ49_CREDIT_GAP=10, TRAJ49_TAG_LEAD=2, TRAJ49_SUPER_FAME=55, TRAJ49_SUPER_CREDIT=50, TRAJ49_CRAFT_FAME=40, TRAJ49_CRAFT_CREDIT=35, TRAJ49_CRAFT_GAP=15, TRAJ49_DIRECTOR_REL=60;",
  extractConst('TRAJ_PAPER_REF49'),
  extractConst('ENDING410_CAREER_NAMES'),
  extractConst('ENDING410_T'),
  extractConst('ENDING_NEG_TAGS410'),
  extractConst('ENDING410_BACKSTAGE_KEYS'),
  extractConst('ENDING410_EXODUS_NAME_FALLBACK'),
  extractConst('ENDING410_NPC_NAMES'),
  extractConst('ENDING410_CHOICE_IDS'),
  extractConst('STORY_SPINE_NODE_C17_410'),
  extractConst('ENDING410_ADJ_RUMOR'),
  extractIIFE('const BehaviorGate = (function(){'),
  extractIIFE('const StoryOC = (()=>{'),
].join('\n')
 .replace('const STORY_GATE_3Y =', 'var STORY_GATE_3Y =')
 .replace('const STORY_LOC_SOFT =', 'var STORY_LOC_SOFT =')
 .replace('const STORY_HINT_SOFT =', 'var STORY_HINT_SOFT =')
 .replace('const STORY_TITLE_SOFT =', 'var STORY_TITLE_SOFT =')
 .replace('const STORY_FLAG_EVENT =', 'var STORY_FLAG_EVENT =')
 .replace('const STORY_PAPER_SKIP =', 'var STORY_PAPER_SKIP =')
 .replace('const TRAJ49_TAG_SETS =', 'var TRAJ49_TAG_SETS =')
 .replace('const TRAJ_PAPER_REF49 =', 'var TRAJ_PAPER_REF49 =')
 .replace('const ENDING410_CAREER_NAMES =', 'var ENDING410_CAREER_NAMES =')
 .replace('const ENDING410_T =', 'var ENDING410_T =')
 .replace('const ENDING_NEG_TAGS410 =', 'var ENDING_NEG_TAGS410 =')
 .replace('const ENDING410_BACKSTAGE_KEYS =', 'var ENDING410_BACKSTAGE_KEYS =')
 .replace('const ENDING410_EXODUS_NAME_FALLBACK =', 'var ENDING410_EXODUS_NAME_FALLBACK =')
 .replace('const ENDING410_NPC_NAMES =', 'var ENDING410_NPC_NAMES =')
 .replace('const ENDING410_CHOICE_IDS =', 'var ENDING410_CHOICE_IDS =')
 .replace('const STORY_SPINE_NODE_C17_410 =', 'var STORY_SPINE_NODE_C17_410 =')
 .replace('const ENDING410_ADJ_RUMOR =', 'var ENDING410_ADJ_RUMOR =')
 .replace('const BehaviorGate =', 'var BehaviorGate =')
 .replace('const StoryOC =', 'var StoryOC =');
eval(SRC);
var displayDateObj = function(){ return dateObj(); };

ok('harness: 結局系統函數載入', typeof resolveEnding410 === 'function' && typeof endingEveOptions410 === 'function' && typeof applyStorySpineOverrides410 === 'function');

function dayIndexOf(y, m, d){ return Math.round((Date.UTC(y, m-1, d) - Date.UTC(1988, 2, 7)) / 86400000); }
function baseSave(over){
  return Object.assign({
    dayIndex: dayIndexOf(1990, 12, 15), money: 900, fame: 20, stage: 0, acting: 8, popularity: 30,
    stress: 0, industryCredit: 0, industryCreditDelta: 0,
    flags: {}, routes: {}, mockCredits: [], mockDebts: [], mockRumors: [], inventory: {},
    castingTags: [], npcs: { agent: 0, director: 0, colleague: 0, reporter: 0, stylist: 0, rival: 0 },
    favorLedger: { settled: 0, credits: 0, exodus: [], counted: {} },
    story: { flags: {}, rel: {}, done: {}, choices: {} },
  }, over || {});
}
function loadGame(save){
  S = save;
  STORY_WIRE.main = JSON.parse(JSON.stringify(pack));
  STORY_WIRE.romance.veraHiuChoi = JSON.parse(JSON.stringify(romVHC));
  STORY_WIRE.romance.lanXu = JSON.parse(JSON.stringify(romLX));
  const r = applyStorySpineOverrides410();
  if(!(r && r.ok && r.main === 1)) throw new Error('4-10 覆寫應替換 1 個（C17），實際 ' + JSON.stringify(r));
  StoryOC.ensure();
  return S;
}
function openIds(){ return StoryOC.listOpen({ player: true }).open.map(r => r.id); }
function node(id){ return StoryOC.findNodeRaw(id); }
function canon(o){
  if(Array.isArray(o)) return '[' + o.map(canon).join(',') + ']';
  if(o && typeof o === 'object') return '{' + Object.keys(o).sort().map(k => JSON.stringify(k) + ':' + canon(o[k])).join(',') + '}';
  return JSON.stringify(o);
}
function R(over){ S = baseSave(over); return resolveEnding410(S); }

/* ================= (a) 判定矩陣 ================= */
{
  const r = R({ fame: 70, stage: 45, acting: 40, industryCreditDelta: 4 });
  ok('E1：聲量70/台風45/演技40/delta4 → 信用61、雙軌131 → E1', r.career === 'E1' && r.snapshot.credit === 61 && r.snapshot.dual === 131);
}
{
  const r = R({ fame: 70, stage: 45, acting: 40, industryCreditDelta: 4, castingTags: [{ id: '八卦', label: '八卦' }, { id: '高冷', label: '高冷' }] });
  ok('E1 被負標籤 2 擋下（八卦＋高冷）→ 落 E2', r.career === 'E2' && r.snapshot.negTags === 2);
}
{
  const r = R({ fame: 60, stage: 0, acting: 0, story: { flags: { flag_miss_leak: true }, rel: {}, done: {}, choices: {} } });
  ok('負標籤兜底：只有 flag_miss_leak（無標籤）都計 1', r.snapshot.negTags === 1);
}
{
  const held2 = [{ id: 'c1', debtor: '甲', title: '人情一', status: '未收' }, { id: 'c2', debtor: '乙', title: '人情二', status: '未收' }];
  const r = R({ fame: 55, stage: 0, acting: 0, mockCredits: held2 });
  ok('E4 沉唔死版：聲量55/信用28＋債權持有 2 → E4 rescued', r.career === 'E4' && r.careerVariant === 'rescued' && r.snapshot.credit === 28);
  const r2 = R({ fame: 55, stage: 0, acting: 0, mockCredits: held2.slice(0, 1) });
  ok('E4 真沉版：債權持有 1（<2，門檻唔放寬）→ E4 sunk', r2.career === 'E4' && r2.careerVariant === 'sunk');
}
{
  const r = R({ fame: 40, stage: 50, acting: 35 });
  ok('E2：信用42＋聲量40 → E2', r.career === 'E2' && r.snapshot.credit === 42);
}
{
  const r = R({ fame: 30, stage: 60, acting: 50, npcs: { agent: 0, director: 65, colleague: 0, reporter: 0, stylist: 0, rival: 0 } });
  ok('E3（導演線）：信用43＋聲量30（唔夠 E2）＋導演 rel 65 → E3', r.career === 'E3');
  const r2 = R({ fame: 30, stage: 60, acting: 50, castingTags: [{ id: '編劇', label: '編劇' }, { id: '剪接', label: '剪接' }] });
  ok('E3（標籤線）：幕後標籤 2 → E3', r2.career === 'E3' && r2.snapshot.backstageTags === 2);
}
{
  const r = R({ fame: 20, stage: 30, acting: 30,
    favorLedger: { settled: 4, credits: 5, exodus: [], counted: {} },
    mockCredits: [{ id: 'c1', debtor: '甲', title: '人情一', status: '未收' }, { id: 'c2', debtor: '乙', title: '人情二', status: '未收' }],
    npcs: { agent: 70, director: 0, colleague: 0, reporter: 0, stylist: 0, rival: 0 } });
  ok('E5：已清4＋持有2＝6＋何生 rel 70 → E5', r.career === 'E5');
  const r2 = R({ fame: 20, stage: 30, acting: 30,
    favorLedger: { settled: 4, credits: 5, exodus: [], counted: {} },
    mockCredits: [{ id: 'c1', debtor: '甲', title: '人情一', status: '未收' }, { id: 'c2', debtor: '乙', title: '人情二', status: '未收' }],
    npcs: { agent: 50, director: 0, colleague: 0, reporter: 0, stylist: 0, rival: 0 } });
  ok('E5 差何生 rel（50<60）→ E0', r2.career === 'E0');
}
{
  const r = R({ fame: 10 });
  ok('E0 預設：低數值 → E0', r.career === 'E0');
}
{
  /* E6：旗本身唔觸發；只有 opts 主動入口先入 */
  const st = { fame: 70, stage: 45, acting: 40, industryCreditDelta: 4,
    story: { flags: { flag_family_job_accept: true }, rel: {}, done: {}, choices: {} } };
  const rNo = R(st);
  ok('E6 唔會自己觸發：有 flag_family_job_accept 都照計 E1', rNo.career === 'E1');
  S = baseSave(st);
  ok('E6 安穩版：opts.quit=job → E6／安穩', resolveEnding410(S, { quit: 'job' }).career === 'E6' && resolveEnding410(S, { quit: 'job' }).careerVariant === '安穩');
  ok('E6 遠走版：opts.quit=leave → E6／遠走／exodus=leave', (()=>{ const q = resolveEnding410(S, { quit: 'leave' }); return q.career === 'E6' && q.careerVariant === '遠走' && q.exodus === 'leave'; })());
  const rE4 = R({ fame: 55, stage: 0, acting: 0 });
  S = baseSave({ fame: 55, stage: 0, acting: 0 });
  ok('E6 心灰版：原判定 E4＋quit=job → 心灰', resolveEnding410(S, { quit: 'job' }).careerVariant === '心灰' && rE4.career === 'E4');
}
{
  /* 純函數深等：判定前後狀態逐字不變 */
  S = baseSave({ fame: 70, stage: 45, acting: 40, industryCreditDelta: 4,
    mockCredits: [{ id: 'credit_fen_rescue', debtor: '副導演芬姐', title: '芬姐人情', status: '絕響' }],
    favorLedger: { settled: 3, credits: 4, exodus: ['credit_fen_rescue'], counted: { x: { kind: 'settled' } } },
    story: { flags: { flag_stay_mind: true }, rel: { rel_hiu: 5 }, done: { R_hiu_meet: true }, choices: {} } });
  const before = canon(S);
  resolveEnding410(S); resolveEnding410(S, { quit: 'job' }); endingEveOptions410(S);
  ok('純函數：resolveEnding410＋endingEveOptions410 唔改狀態（deep equal）', canon(S) === before);
}
{
  /* 讀取口交叉對照：唯讀鏡像 vs 生產 favorLedgerCounts／endingRomanceState48 */
  loadGame(baseSave({
    mockCredits: [{ id: 'credit_fen_rescue', debtor: '副導演芬姐', title: '芬姐人情', status: '絕響' }, { id: 'c9', debtor: '場務', title: '出頭人情', status: '未收' }],
    favorLedger: { settled: 3, credits: 4, exodus: ['credit_fen_rescue'], counted: {} },
    story: { flags: { flag_hiu_commit: true }, rel: { rel_hiu: 7, rel_vera: 5 }, done: { R_hiu_meet: true, R_hiu_crisis: true, R_vera_meet: true }, choices: {} }
  }));
  const mine = endingFavor410(S), prod = favorLedgerCounts();
  ok('favor 鏡像對照：settled/creditsHeld/exodus 一致', mine.settled === prod.settled && mine.creditsHeld === prod.creditsHeld && mine.exodusNames.join() === '副導演芬姐');
  const mr = endingRomance410(S), pr = endingRomanceState48();
  ok('romance 鏡像對照：hiu commit／vera rel 一致', mr.hiu.committed === pr.hiu.committed && mr.vera.rel === pr.vera.rel && mr.hiu.crisisDone === pr.hiu.crisisDone);
  const rr = resolveEnding410(S);
  ok('感情軸：hiu commit → romance commit/hiu', rr.romance.kind === 'commit' && rr.romance.line === 'hiu');
}
{
  /* 半線 pack commit 旗唔入 commit（專檔定性）：vera 有 flag_vera_commit＋rel 5 → 只做差一步 */
  const r = R({ story: { flags: { flag_vera_commit: true }, rel: { rel_vera: 5 }, done: { R_vera_meet: true, R_vera_crisis: true }, choices: {} } });
  ok('半線定性：flag_vera_commit 唔當 commit → almost/vera', r.romance.kind === 'almost' && r.romance.line === 'vera');
  const r2 = R({ story: { flags: {}, rel: { rel_vera: 3 }, done: { R_vera_meet: true }, choices: {} } });
  ok('差一步門檻：rel 3 <4 → solo', r2.romance.kind === 'solo');
}

/* ================= (b) 觸發閘＋覆寫 ================= */
{
  loadGame(baseSave({ dayIndex: dayIndexOf(1989, 12, 15), story: { flags: {}, rel: {}, done: { C13: true }, choices: {} } }));
  ok('閘：1989 冬（yearEq 唔中）→ C17 唔開', !openIds().includes('C17'));
  loadGame(baseSave({ story: { flags: {}, rel: {}, done: {}, choices: {} } }));
  ok('閘：1990 冬但 C13 未 done → C17 唔開', !openIds().includes('C17'));
  loadGame(baseSave({ story: { flags: {}, rel: {}, done: { C13: true }, choices: {} } }));
  ok('閘：1990 冬＋C13 done → C17 開', openIds().includes('C17'));
  const n = node('C17');
  ok('覆寫：C17 係「三年收科」＋locId tvb_longmen＋有 playerOffer', n.title === '三年收科' && n.locId === 'tvb_longmen' && !!n.playerOffer);
  ok('覆寫：舊十檔清零（冇 endingId choices／冇 E01 字串／冇 ending_e 旗）',
     (n.choices || []).every(c => !c.endingId) && !JSON.stringify(n).includes('E01') && !JSON.stringify(n).includes('ending_e'));
  const r2 = applyStorySpineOverrides410();
  ok('覆寫冪等：再套一次 main=1、標題不變', r2.main === 1 && node('C17').title === '三年收科');
}

/* ================= (c) 相鄰規則 ================= */
function eveKeys(over){
  S = baseSave(over);
  return endingEveOptions410(S).map(o => o.key);
}
{
  const keys = eveKeys({ fame: 55, stage: 0, acting: 0, npcs: { agent: 0, director: 40, colleague: 0, reporter: 0, stylist: 0, rival: 0 } });
  ok('相鄰：E4＋債權0＋導演 rel 40（差少少）→ 出 to_backstage', keys.includes('to_backstage'));
  const keys2 = eveKeys({ fame: 55, stage: 0, acting: 0, npcs: { agent: 0, director: 39, colleague: 0, reporter: 0, stylist: 0, rival: 0 } });
  ok('相鄰：E4＋導演 rel 39＋零幕後標籤 → 唔出 to_backstage', !keys2.includes('to_backstage'));
  const keys3 = eveKeys({ fame: 55, stage: 0, acting: 0,
    mockCredits: [{ id: 'a', debtor: '甲', title: '一', status: '未收' }, { id: 'b', debtor: '乙', title: '二', status: '未收' }],
    npcs: { agent: 0, director: 60, colleague: 0, reporter: 0, stylist: 0, rival: 0 } });
  ok('相鄰：E4 已有債權 2（沉唔死版）→ 唔出 to_backstage', !keys3.includes('to_backstage'));
  const keys4 = eveKeys({ fame: 40, stage: 50, acting: 35, npcs: { agent: 0, director: 60, colleague: 0, reporter: 0, stylist: 0, rival: 0 } });
  ok('相鄰：E2 同時合 E3 資格 → 出 to_backstage（前夕分流）', keys4.includes('to_backstage'));
  const keys5 = eveKeys({ fame: 30, stage: 60, acting: 50, npcs: { agent: 0, director: 65, colleague: 0, reporter: 0, stylist: 0, rival: 0 } });
  ok('相鄰：E3 但聲量 30 唔合 E2 → 唔出 to_support', !keys5.includes('to_support'));
  const keys6 = eveKeys({ fame: 10, story: { flags: { flag_leave_mind: true }, rel: {}, done: {}, choices: {} } });
  ok('相鄰：leave_mind＋E0 → 出 leave_follow＋quit_leave', keys6.includes('leave_follow') && keys6.includes('quit_leave'));
  const keys7 = eveKeys({ fame: 70, stage: 45, acting: 40, industryCreditDelta: 4, story: { flags: { flag_leave_mind: true }, rel: {}, done: {}, choices: {} } });
  ok('相鄰：leave_mind＋E1 → 唔出 leave_follow（只限 E0／E2）', !keys7.includes('leave_follow'));
  ok('相鄰：任何狀態都有 natural＋quit_job', keys7.includes('natural') && keys7.includes('quit_job'));
  ok('相鄰：冇 leave_mind → 唔出 quit_leave', !eveKeys({ fame: 10 }).includes('quit_leave'));
}

/* ================= (d) 全流程真呈現 ================= */
{
  modalPages410 = [];
  loadGame(baseSave({
    fame: 40, stage: 50, acting: 35,
    npcs: { agent: 30, director: 10, colleague: 0, reporter: 0, stylist: 0, rival: 0 },
    mockCredits: [{ id: 'credit_fen_rescue', debtor: '副導演芬姐', title: '芬姐人情', status: '絕響' }, { id: 'credit_c9_crew', debtor: '劇組場務', title: '年尾出頭人情', status: '未收' }],
    favorLedger: { settled: 3, credits: 4, exodus: ['credit_fen_rescue'], counted: {} },
    story: { flags: { flag_hiu_commit: true, flag_stay_mind: true }, rel: { rel_hiu: 7 }, done: { C13: true, R_hiu_meet: true, R_hiu_crisis: true }, choices: {} }
  }));
  const base = node('C17');
  const eve = ending410EveNode(base);
  ok('前夕節點：choices 由狀態生成（natural/quit_job 在列）', eve.choices.some(c => c.ending410Key === 'natural') && eve.choices.some(c => c.ending410Key === 'quit_job'));
  ok('前夕節點：eve choices 唔生報紙（newspaperStoryResolve 全 null）', eve.choices.every(c => newspaperStoryResolve(eve, c) === null));
  const natural = eve.choices.find(c => c.ending410Key === 'natural');
  const result = StoryOC.applyChoice(eve, natural);
  ok('真 applyChoice：C17 落 done＋旗寫入', StoryOC.isDone('C17') && StoryOC.getFlag('flag_ending410_natural'));
  const handled = ending410AfterEveChoice(eve, natural, result);
  ok('組裝接管：ending410AfterEveChoice 回 true', handled === true);
  ok('落檔：S.ending410 career=E2／romance commit hiu／exodus stay／稱號含甘草王',
     S.ending410 && S.ending410.career === 'E2' && S.ending410.romanceKind === 'commit' && S.ending410.romanceLine === 'hiu'
     && S.ending410.exodus === 'stay' && S.ending410.title.indexOf('甘草王') === 0);
  ok('呈現第一頁：事業場景（金牌甘草）', modalPages410.length >= 1 && modalPages410[0].html.includes('金牌甘草'));
  modalPages410[0].buttons[0].on();
  ok('呈現第二頁：感情段（曉晴 commit）＋去留段＋個人化插入（芬姐絕響）',
     modalPages410.length >= 2 && modalPages410[1].html.includes('林曉晴') && modalPages410[1].html.includes('芬姐'));
  modalPages410[1].buttons[0].on();
  const sum = modalPages410[modalPages410.length - 1].html;
  ok('總結頁五元素齊：稱號卡／雙軌／人情總帳／走咗名單（芬姐）／感情＋去留行',
     sum.includes('甘草王・留下來的人') && sum.includes('幕前聲量') && sum.includes('人情總帳') && sum.includes('邊啲人走咗') && sum.includes('副導演芬姐') && sum.includes('感情') && sum.includes('去留'));
  ok('總結頁：差啲嗰條路傳聞句在場', sum.includes('聽講'));
  const pagesBefore = modalPages410.length;
  const again = ending410AfterEveChoice(eve, natural, result);
  ok('冪等：重入只重開總結頁、唔重複成個流程', again === true && modalPages410.length === pagesBefore + 1 && S.ending410.career === 'E2');
  ok('收科後唔再開 C17（done）', !openIds().includes('C17'));
}
{
  /* E4 前夕：危機 beats 插入＋to_backstage 揀完呈現 E3 變體 */
  modalPages410 = [];
  loadGame(baseSave({
    fame: 55, stage: 0, acting: 0,
    npcs: { agent: 0, director: 45, colleague: 0, reporter: 0, stylist: 0, rival: 0 },
    story: { flags: {}, rel: {}, done: { C13: true }, choices: {} }
  }));
  const eve = ending410EveNode(node('C17'));
  ok('E4 前夕：beats 插入形象危機拍', JSON.stringify(eve.beats).includes('頭版'));
  const pick = eve.choices.find(c => c.ending410Key === 'to_backstage');
  ok('E4 前夕：to_backstage 選項在列', !!pick);
  const result = StoryOC.applyChoice(eve, pick);
  ending410AfterEveChoice(eve, pick, result);
  ok('E4 行一格：落檔 career=E3／variant 記由 E4 轉幕後', S.ending410.career === 'E3' && S.ending410.careerVariant.includes('泡沫'));
  ok('E4 行一格：呈現係幕後場景（控制台）', modalPages410[0].html.includes('控制台'));
}
{
  /* leave_follow：事業不變、去留轉 leave */
  modalPages410 = [];
  loadGame(baseSave({
    fame: 10,
    story: { flags: { flag_leave_mind: true }, rel: {}, done: { C13: true }, choices: {} }
  }));
  const eve = ending410EveNode(node('C17'));
  const pick = eve.choices.find(c => c.ending410Key === 'leave_follow');
  const result = StoryOC.applyChoice(eve, pick);
  ending410AfterEveChoice(eve, pick, result);
  modalPages410[0].buttons[0].on();
  ok('leave_follow：career 照 E0、exodus=leave、呈現有啟德', S.ending410.career === 'E0' && S.ending410.exodus === 'leave' && JSON.stringify(modalPages410.map(p => p.html)).includes('啟德'));
}

/* ================= (f) 舊存檔相容 ================= */
{
  /* 舊檔 A：舊 pack C13 已 done、C17 未播（offer 狀態）→ 行到新流程 */
  loadGame(baseSave({
    story: { flags: { gossip_vague: true }, rel: { rel_choi: 2 }, done: { C13: true }, choices: { C13: 'C13_c' } }
  }));
  ok('舊檔 A：C17 以新節點開到、唔 crash', openIds().includes('C17') && node('C17').title === '三年收科');
  /* 舊檔 B：舊十檔已揀（C17 done＋ending_e01＋career_lock）→ 唔重播、判定／總結唔 crash */
  loadGame(baseSave({
    story: { flags: { ending_e01: true, career_lock: true }, rel: {}, done: { C13: true, C17: true }, choices: { C17: 'C17_e01' } }
  }));
  ok('舊檔 B：C17 已 done 唔再開', !openIds().includes('C17'));
  let noCrash = true;
  try{ resolveEnding410(S); endingSummaryHtml410(); }catch(_e){ noCrash = false; }
  ok('舊檔 B：resolve／總結頁唔 crash（未有 S.ending410 照出未收科版）', noCrash && endingSummaryHtml410().includes('未收科'));
}

console.log('\nweave410 logic: ' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
