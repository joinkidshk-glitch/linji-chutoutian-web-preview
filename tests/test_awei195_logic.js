// v20a195 TIER195・邏輯／真路徑測試
// B 方案（用戶 2026-11-13 20:58 由 A 改 B）：阿偉造型 tier 持久化做最高紀錄。
// 覆蓋：(a) 即時 tier 跨年跌（重現根因：1990 lead → 1991 live tier 跌）＋
//           最高紀錄令 dlg106AweiStem() 唔跌（1991 照出 s2）
//       (b) enc195RecordTierMax 寫入：殺青 lead 後寫 2、唔會跌返、唔會覆寫更高值
//       (c) tier 3 跨年：3 部真男主角＋fame≥70 → 1991 照出 s3
//       (d) 舊檔 backfill（normalizeSaveObj）：冇 playerTierMax、有 1990 lead 旗 →
//           載入後寫 2；3 lead＋fame≥70 → 3；冪等（已有值唔郁）
//       (e) 假男主角陷阱：gig_1988_tv_06（NAME93 降級做配角）完成旗 → tier 唔升（0，fame 5）
//       (f) 年庫未載入嗰陣唔寫錯值（留空）＋dlg106AweiStem 懶回填（packs 到齊先補 2）
//       (g) 全池口徑：1990 年庫 normalize 後真男主角得 15 部（唔係 pack 話嘅 20 部）
// 反證：喺 pristine main（f2a6b0c）index 上行，enc195BackfillTierMax 唔存在——
//       本檔唔 crash，逐組印 FAIL 後 exit 1。
// 用法：node tests/test_awei195_logic.js（AWEI195_DEBUG=1 印實際輸出）
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
const DEBUG = !!process.env.AWEI195_DEBUG;

let fails = [];
function ok(name, cond, extra){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name + (extra ? ' :: ' + extra : '')); }

const GROUPS = ['(a) 跨年唔跌', '(b) 殺青寫入', '(c) tier 3 跨年', '(d) 舊檔 backfill', '(e) 假男主角', '(f) 年庫未齊＋懶回填', '(g) 全池口徑'];
if(html.indexOf('function enc195BackfillTierMax(') < 0){
  GROUPS.forEach(n=>{ fails.push(n); console.log('FAIL ' + n + '（pristine：冇 enc195BackfillTierMax）'); });
  console.log('AWEI195 LOGIC: ' + fails.length + ' FAIL');
  process.exit(1);
}

function extractFn(name){
  const i = html.indexOf('function '+name+'(');
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
  let depth = 0, started = false;
  for(let k = i; k < html.length; k++){
    const ch = html[k];
    if(ch === '{' || ch === '['){ depth++; started = true; }
    else if(ch === '}' || ch === ']'){ depth--; if(started && depth === 0) return html.slice(i, k + 1) + ';'; }
    else if(ch === ';' && !started) return html.slice(i, k + 1);
  }
  throw new Error('const end not found: ' + name);
}
// TEXTFIX 切片（同 test_name93_logic.js 口徑：normalizeGigRecord 依賴 textfix55／years66）。
const tfA = html.indexOf('/* ==== v20a55 TEXTFIX');
const tfB = html.indexOf('async function refreshCopyPacksFromDisk(){');
if(tfA < 0 || tfB <= tfA){ console.log('FAIL TEXTFIX55 block not found'); process.exit(1); }
const TF_SRC = html.slice(tfA, tfB);
const CONSTS = ['NAME93_FIX', 'GIG_REQ_KEYS88', 'CLEAN100_GIG_RELEASE', 'LEADSTAR59'];
const FNS = ['normalizeGigRecord', 'name93ApplyGig', 'ovr110Apply', 'boardNotePlayerOk',
  'looksLikeEraId', 'humanizeEraId', 'dur90CalibrateGig', 'leadStar59Apply', 'leadStar59Of',
  'enc79PlayerTier', 'dlg106AweiStem',
  'enc195TierFromAllYears', 'enc195BackfillTierMax', 'enc195EnsureTierMax', 'enc195RecordTierMax',
  'normalizeSaveObj'];
const tryConst = c => { const s = extractConst(c); return s.replace('const ' + c, 'var ' + c); };
// TIER110／REQ110 係 var 單行長行（>600 字），唔行 extractConst 口徑，直接成行抽。
function extractVarLine(name){
  const i = html.indexOf('var ' + name + ' =');
  if(i < 0) throw new Error('var not found: ' + name);
  const e = html.indexOf('\n', i);
  return html.slice(i, e < 0 ? html.length : e);
}
const VARCONSTS = ['TIER110', 'REQ110'];
const tryFn = f => { try { return extractFn(f); } catch(e) { return ''; } };
const WORLD_SRC = TF_SRC + '\n' + CONSTS.map(tryConst).join('\n') + '\n' + VARCONSTS.map(extractVarLine).join('\n') + '\n' + FNS.map(tryFn).join('\n');
const STUBS_SRC = `
  var START = { y:1990, m:1, d:1 };
  var STRESS_MAX = 100;
  var S = null;
  var GIGS = [];
  var STORY_WIRE = { gigsByYear: { 1990: null, 1991: null, 1992: null, 1993: null, 1994: null } };
`;
const W = new Function(STUBS_SRC + WORLD_SRC + `
; return { normalizeGigRecord, years66Walk: (typeof years66Walk === 'function') ? years66Walk : null,
  enc79PlayerTier, dlg106AweiStem, enc195TierFromAllYears, enc195BackfillTierMax,
  enc195EnsureTierMax, enc195RecordTierMax, normalizeSaveObj,
  setS:(s)=>{S=s;}, getS:()=>S, setGIGS:(g)=>{GIGS=g;}, getGIGS:()=>GIGS,
  setWIRE:(w)=>{STORY_WIRE=w;}, getWIRE:()=>STORY_WIRE };`)();
function deepClone(o){ return JSON.parse(JSON.stringify(o)); }

// 真年庫（同 boot 口徑：pack 先 years66Walk，再 normalize；遊戲 1990 年＝gigs_1988.json）。
function loadPack(fileYear){
  const pack = deepClone(JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gigs_' + fileYear + '.json'), 'utf8')));
  if(W.years66Walk) W.years66Walk(pack, null);
  return pack;
}
const PACKS = { 1990: loadPack(1988), 1991: loadPack(1989), 1992: loadPack(1990), 1993: loadPack(1991), 1994: loadPack(1992) };
function wirePacks(){
  W.setWIRE({ gigsByYear: { 1990: PACKS[1990], 1991: PACKS[1991], 1992: PACKS[1992], 1993: PACKS[1993], 1994: PACKS[1994] } });
}
function gigsOfYear(y){ return (PACKS[y].gigs || []).map(g => W.normalizeGigRecord(deepClone(g))); }
function leadIds(y){ return gigsOfYear(y).filter(g => /lead/.test(String(g.roleScale || ''))).map(g => g.id); }
function freshSave(over){
  return Object.assign({
    dayIndex: 0, fame: 5, popularity: 3, money: 12000, stress: 12,
    flags: {}, inventory: {}, giftMeta: {}, wrapHistory: [], castingTags: [],
    postShootRewards: [], awardsLog: [], awardsFlags: {}, newspaperQueue: [],
    newspaperClippings: [], execLog105: {},
  }, over || {});
}
function setLive(save, year){
  W.setS(save);
  W.setGIGS(gigsOfYear(year));
  return save;
}

wirePacks();
const LEAD90 = leadIds(1990);
const LEAD91 = leadIds(1991);
if(DEBUG) console.log('lead90:', LEAD90.length, LEAD90.join(','));
if(DEBUG) console.log('lead91:', LEAD91.length, LEAD91.join(','));

/* ---- (g) 全池口徑：NAME93 降級後真男主角數 ---- */
ok('(g) 1990 年庫 normalize 後真男主角得 15 部（唔係 pack 話嘅 20 部）', LEAD90.length === 15, 'n=' + LEAD90.length);
ok('(g) gig_1988_tv_06／07／08 降級做配角／綜藝、唔係 lead',
  ['gig_1988_tv_06', 'gig_1988_tv_07', 'gig_1988_tv_08'].every(id => {
    const g = gigsOfYear(1990).find(x => x.id === id);
    return g && !/lead/.test(String(g.roleScale || ''));
  }));
ok('(g) gig_1988_film_05 係真男主角', LEAD90.indexOf('gig_1988_film_05') >= 0);
ok('(g) 1991 年庫得 2 部真男主角', LEAD91.length === 2, 'n=' + LEAD91.length);

/* ---- (a) 即時 tier 跨年跌（根因重現）＋最高紀錄頂住 ---- */
let saveA = freshSave({ dayIndex: 300, fame: 30, flags: { done_gig_1988_film_05: 1 } });
setLive(saveA, 1990);
ok('(a) 1990 年即時 tier 係 2（做完一部真男主角）', W.enc79PlayerTier() === 2);
ok('(a) 1990 年 stem 係 awi_s2', W.dlg106AweiStem() === 'awi_s2');
setLive(saveA, 1991);
ok('(a) 1991 年即時 tier 跌返 1（根因：當年 GIGS 冇咗 1990 嗰部）', W.enc79PlayerTier() === 1);
ok('(a) 1991 年 stem 照係 awi_s2（最高紀錄頂住，唔跌返）', W.dlg106AweiStem() === 'awi_s2');
ok('(a) 最高紀錄已寫入 playerTierMax=2', saveA.flags.playerTierMax === 2, 'v=' + saveA.flags.playerTierMax);
setLive(saveA, 1992);
ok('(a) 1992 年 stem 照係 awi_s2', W.dlg106AweiStem() === 'awi_s2');

/* ---- (b) enc195RecordTierMax：殺青寫入點呼叫嘅 helper ---- */
let saveB = freshSave({ fame: 30, flags: { done_gig_1988_film_05: 1 } });
setLive(saveB, 1990);
W.enc195RecordTierMax();
ok('(b) 殺青 lead 後 playerTierMax=2', saveB.flags.playerTierMax === 2, 'v=' + saveB.flags.playerTierMax);
setLive(saveB, 1991);
W.enc195RecordTierMax();
ok('(b) 跨年後再記一次，最高紀錄唔跌（仲係 2）', saveB.flags.playerTierMax === 2);
saveB.flags.playerTierMax = 3;
setLive(saveB, 1991);
W.enc195RecordTierMax();
ok('(b) 已有更高紀錄唔會俾較低即時 tier 覆寫（3 唔變 1）', saveB.flags.playerTierMax === 3);
let saveB0 = freshSave({ fame: 5, flags: {} });
setLive(saveB0, 1990);
W.enc195RecordTierMax();
ok('(b) 未做過主角嗰陣記 0（唔會無端升）', saveB0.flags.playerTierMax === 0, 'v=' + saveB0.flags.playerTierMax);

/* ---- (c) tier 3 跨年 ---- */
const threeLead = LEAD90.slice(0, 3);
let saveC = freshSave({ dayIndex: 300, fame: 70, flags: {} });
threeLead.forEach(id => { saveC.flags['done_' + id] = 1; });
setLive(saveC, 1990);
ok('(c) 1990 年 3 部 lead＋fame 70 → 即時 tier 3', W.enc79PlayerTier() === 3, 'leads=' + threeLead.join(','));
W.enc195RecordTierMax();
ok('(c) 殺青後 playerTierMax=3', saveC.flags.playerTierMax === 3);
setLive(saveC, 1991);
ok('(c) 1991 年即時 tier 跌返（當年庫得 2 部 lead、全部未做）', W.enc79PlayerTier() < 3, 'live=' + W.enc79PlayerTier());
ok('(c) 1991 年 stem 照係 awi_s3', W.dlg106AweiStem() === 'awi_s3');

/* ---- (d) 舊檔 backfill：經 normalizeSaveObj 載入 ---- */
let oldD = freshSave({ dayIndex: 400, fame: 30, flags: { done_gig_1988_film_05: 1 } });
delete oldD.flags.playerTierMax;
const backD = W.normalizeSaveObj(oldD);
ok('(d) 舊檔（1990 lead、1991 年）載入後 playerTierMax=2', backD.flags.playerTierMax === 2, 'v=' + backD.flags.playerTierMax);
let oldD3 = freshSave({ dayIndex: 400, fame: 70, flags: {} });
threeLead.forEach(id => { oldD3.flags['done_' + id] = 1; });
const backD3 = W.normalizeSaveObj(oldD3);
ok('(d) 舊檔（3 lead＋fame 70）載入後 playerTierMax=3', backD3.flags.playerTierMax === 3, 'v=' + backD3.flags.playerTierMax);
let oldD2 = freshSave({ dayIndex: 400, fame: 70, flags: { playerTierMax: 2 } });
threeLead.forEach(id => { oldD2.flags['done_' + id] = 1; });
const backD2 = W.normalizeSaveObj(oldD2);
ok('(d) 已有最高紀錄唔會俾 backfill 覆寫（2 唔變 3——升 tier 行殺青寫入點）', backD2.flags.playerTierMax === 2, 'v=' + backD2.flags.playerTierMax);
let oldD0 = freshSave({ dayIndex: 400, fame: 5, flags: {} });
const backD0 = W.normalizeSaveObj(oldD0);
ok('(d) 未做過主角嘅舊檔回填 0', backD0.flags.playerTierMax === 0, 'v=' + backD0.flags.playerTierMax);

/* ---- (e) 假男主角陷阱：降級做配角 → 唔會計 lead、唔會上 s2 ---- */
// 註：tv_06／07 降級做 tv_support_main，support 計 tier 1（s1 臨記樣，
// 同 tier 0 同一個 stem）；關鍵係唔會誤升做 tier 2／s2。
let saveE = freshSave({ dayIndex: 400, fame: 5, flags: { done_gig_1988_tv_06: 1 } });
const backE = W.normalizeSaveObj(saveE);
ok('(e) 淨做 gig_1988_tv_06（假男主角）→ backfill 1（配角級，唔係 2）', backE.flags.playerTierMax === 1, 'v=' + backE.flags.playerTierMax);
setLive(saveE, 1990);
ok('(e) 假男主角即時 tier 都係 1（1990 年庫入面都唔計 lead）', W.enc79PlayerTier() === 1);
ok('(e) 假男主角 stem 係 awi（s1，唔會變 s2）', W.dlg106AweiStem() === 'awi');
let saveE2 = freshSave({ fame: 5, flags: { done_gig_1988_tv_06: 1, done_gig_1988_tv_07: 1, done_gig_1988_tv_08: 1 } });
const backE2 = W.normalizeSaveObj(saveE2);
ok('(e) 三張假男主角一齊都係 1（仲係配角級）', backE2.flags.playerTierMax === 1, 'v=' + backE2.flags.playerTierMax);

/* ---- (f) 年庫未齊唔寫錯值＋懶回填 ---- */
W.setWIRE({ gigsByYear: { 1990: null, 1991: null, 1992: null, 1993: null, 1994: null } });
ok('(f) 年庫未載入嗰陣 enc195TierFromAllYears 回 null（唔估）',
  W.enc195TierFromAllYears({ done_gig_1988_film_05: 1 }, 30) === null);
let saveF = freshSave({ dayIndex: 400, fame: 30, flags: { done_gig_1988_film_05: 1 } });
const backF = W.normalizeSaveObj(saveF);
ok('(f) 年庫未齊嗰陣 backfill 留空（唔寫 0）', backF.flags.playerTierMax === undefined, 'v=' + backF.flags.playerTierMax);
wirePacks(); //  packs 到齊（實機：boot 完成先讀檔／先播對話）
setLive(saveF, 1991);
ok('(f) packs 到齊後第一次讀 stem，懶回填補返 2、stem 係 awi_s2',
  W.dlg106AweiStem() === 'awi_s2' && saveF.flags.playerTierMax === 2,
  'stem=' + W.dlg106AweiStem() + ' v=' + saveF.flags.playerTierMax);

/* ---- (f 續) 最高紀錄讀取：live 0 都唔跌 ---- */
let saveF2 = freshSave({ fame: 5, flags: { playerTierMax: 2 } });
setLive(saveF2, 1991);
ok('(f) playerTierMax=2、即時 tier 0 → stem 照係 awi_s2', W.dlg106AweiStem() === 'awi_s2');
let saveF3 = freshSave({ fame: 5, flags: { playerTierMax: 3 } });
setLive(saveF3, 1991);
ok('(f) playerTierMax=3 → stem 係 awi_s3', W.dlg106AweiStem() === 'awi_s3');
let saveF0 = freshSave({ fame: 5, flags: {} });
setLive(saveF0, 1991);
ok('(f) 冇紀錄、冇 lead、fame 5 → stem 係 awi（s1）', W.dlg106AweiStem() === 'awi');

console.log(fails.length ? ('AWEI195 LOGIC: ' + fails.length + ' FAIL -> ' + fails.join(' | ')) : 'AWEI195 LOGIC: ALL PASS');
process.exit(fails.length ? 1 : 0);
