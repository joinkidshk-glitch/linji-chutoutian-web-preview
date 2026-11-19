// v20a195 TIER195・邏輯／真路徑測試（v20a229 B3 新庫版）
// B 方案（用戶 2026-11-13 20:58 由 A 改 B）：阿偉造型 tier 持久化做最高紀錄。
// 新庫場景移後一年：1990 年新庫得 0 部男主角（臨記／初級年，第一部男主角要到 1991），
// 所以 (a)／(c)／(d) 嘅 lead 場景由 1990→1991、跨年跌由 1991→1992。
// 覆蓋：(a) 即時 tier 跨年跌（重現根因：1991 lead → 1992 live tier 跌）＋
//           最高紀錄令 dlg106AweiStem() 唔跌（1992 照出 s2）
//       (b) enc195RecordTierMax 寫入：殺青 lead 後寫 2、唔會跌返、唔會覆寫更高值
//       (c) tier 3 跨年：3 部真男主角＋fame≥70 → 1992 照出 s3
//       (d) 舊檔 backfill（normalizeSaveObj）：冇 playerTierMax、有 1991 lead 旗 →
//           載入後寫 2；3 lead＋fame≥70 → 3；冪等（已有值唔郁）
//       (e) 假男主角陷阱（v252 新形）：label 男主角唔等於真男主角——新庫 7 個假 label 全部係 MTV
//           （roleScale mtv，lead／support 兩邊都唔計）。gig_1990_rec_108《月夜影》MV 男主角完成旗 →
//           tier 0（fame 5，乜都唔計）；舊樣本 film_107 而家係動作替身，唔再係假 label 案例。
//       (f) 年庫未載入嗰陣唔寫錯值（留空）＋dlg106AweiStem 懶回填（packs 到齊先補 2）
//       (g) 全池口徑：1990 年庫 normalize 後真男主角得 0 部、1991 年 8 部、1992 年 8 部（v337：＋film_207《虎嘯龍吟》男主角）
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
const CONSTS = ['GIG_REQ_KEYS88'];
const FNS = ['normalizeGigRecord', 'boardNotePlayerOk',
  'looksLikeEraId', 'humanizeEraId', 'leadStar59Of',
  'enc79PlayerTier', 'dlg106AweiStem',
  'enc195TierFromAllYears', 'enc195BackfillTierMax', 'enc195EnsureTierMax', 'enc195RecordTierMax',
  'normalizeSaveObj'];
const tryConst = c => { const s = extractConst(c); return s.replace('const ' + c, 'var ' + c); };
const tryFn = f => { try { return extractFn(f); } catch(e) { return ''; } };
const WORLD_SRC = TF_SRC + '\n' + CONSTS.map(tryConst).join('\n') + '\n' + FNS.map(tryFn).join('\n');
const STUBS_SRC = `
  var START = { y:1990, m:1, d:1 };
  var STRESS_MAX = 100;
  var S = null;
  var GIGS = [];
  var STORY_WIRE = { gigsByYear: { 1990: null, 1991: null, 1992: null } };
`;
const W = new Function(STUBS_SRC + WORLD_SRC + `
; return { normalizeGigRecord,
  enc79PlayerTier, dlg106AweiStem, enc195TierFromAllYears, enc195BackfillTierMax,
  enc195EnsureTierMax, enc195RecordTierMax, normalizeSaveObj,
  setS:(s)=>{S=s;}, getS:()=>S, setGIGS:(g)=>{GIGS=g;}, getGIGS:()=>GIGS,
  setWIRE:(w)=>{STORY_WIRE=w;}, getWIRE:()=>STORY_WIRE };`)();
function deepClone(o){ return JSON.parse(JSON.stringify(o)); }

// 真年庫（新庫：gigs_new.json 已經係顯示年 1990–1992，唔行 years66Walk；按 year 分年）。
const PACK_NEW = deepClone(JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gigs_new.json'), 'utf8')));
const PACKS = { 1990: { gigs: [] }, 1991: { gigs: [] }, 1992: { gigs: [] } };
PACK_NEW.gigs.forEach(g => { if(PACKS[g.year]) PACKS[g.year].gigs.push(g); });
function wirePacks(){
  W.setWIRE({ gigsByYear: { 1990: PACKS[1990], 1991: PACKS[1991], 1992: PACKS[1992] } });
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
const LEAD92 = leadIds(1992);
if(DEBUG) console.log('lead90:', LEAD90.length, LEAD90.join(','));
if(DEBUG) console.log('lead91:', LEAD91.length, LEAD91.join(','));
if(DEBUG) console.log('lead92:', LEAD92.length, LEAD92.join(','));

/* ---- (g) 全池口徑：新庫按年真男主角數 ---- */
ok('(g) 1990 年庫 normalize 後真男主角得 0 部（臨記／初級年，第一部男主角要到 1991）', LEAD90.length === 0, 'n=' + LEAD90.length);
ok('(g) 1991 年庫得 8 部真男主角', LEAD91.length === 8, 'n=' + LEAD91.length + ' ' + LEAD91.join(','));
ok('(g) 1992 年庫得 8 部真男主角', LEAD92.length === 8, 'n=' + LEAD92.length + ' ' + LEAD92.join(','));
ok('(g) gig_1990_rec_108 係假男主角（label 男主角、roleScale mtv）',
  (() => { const g = gigsOfYear(1990).find(x => x.id === 'gig_1990_rec_108');
    return g && /男主角/.test(String(g.roleLabel || '')) && !/lead/.test(String(g.roleScale || '')); })());
ok('(g) gig_1990_film_107 而家係動作替身，唔再係假男主角 label 案例',
  (() => { const g = gigsOfYear(1990).find(x => x.id === 'gig_1990_film_107');
    return g && g.roleLabel === '動作替身' && g.roleScale === 'film_support_small'; })());
ok('(g) gig_1991_film_102 係真男主角', LEAD91.indexOf('gig_1991_film_102') >= 0);

/* ---- (a) 即時 tier 跨年跌（根因重現）＋最高紀錄頂住 ---- */
let saveA = freshSave({ dayIndex: 400, fame: 30, flags: { done_gig_1991_film_102: 1 } });
setLive(saveA, 1991);
ok('(a) 1991 年即時 tier 係 2（做完一部真男主角）', W.enc79PlayerTier() === 2);
ok('(a) 1991 年 stem 係 awi_s2', W.dlg106AweiStem() === 'awi_s2');
setLive(saveA, 1992);
ok('(a) 1992 年即時 tier 跌返 1（根因：當年 GIGS 冇咗 1991 嗰部，fame 30 保住 tier 1）', W.enc79PlayerTier() === 1);
ok('(a) 1992 年 stem 照係 awi_s2（最高紀錄頂住，唔跌返）', W.dlg106AweiStem() === 'awi_s2');
ok('(a) 最高紀錄已寫入 playerTierMax=2', saveA.flags.playerTierMax === 2, 'v=' + saveA.flags.playerTierMax);
setLive(saveA, 1990);
ok('(a) 1990 年 stem 照係 awi_s2', W.dlg106AweiStem() === 'awi_s2');

/* ---- (b) enc195RecordTierMax：殺青寫入點呼叫嘅 helper ---- */
let saveB = freshSave({ fame: 30, flags: { done_gig_1991_film_102: 1 } });
setLive(saveB, 1991);
W.enc195RecordTierMax();
ok('(b) 殺青 lead 後 playerTierMax=2', saveB.flags.playerTierMax === 2, 'v=' + saveB.flags.playerTierMax);
setLive(saveB, 1992);
W.enc195RecordTierMax();
ok('(b) 跨年後再記一次，最高紀錄唔跌（仲係 2）', saveB.flags.playerTierMax === 2);
saveB.flags.playerTierMax = 3;
setLive(saveB, 1992);
W.enc195RecordTierMax();
ok('(b) 已有更高紀錄唔會俾較低即時 tier 覆寫（3 唔變 1）', saveB.flags.playerTierMax === 3);
let saveB0 = freshSave({ fame: 5, flags: {} });
setLive(saveB0, 1991);
W.enc195RecordTierMax();
ok('(b) 未做過主角嗰陣記 0（唔會無端升）', saveB0.flags.playerTierMax === 0, 'v=' + saveB0.flags.playerTierMax);

/* ---- (c) tier 3 跨年 ---- */
const threeLead = LEAD91.slice(0, 3);
let saveC = freshSave({ dayIndex: 400, fame: 70, flags: {} });
threeLead.forEach(id => { saveC.flags['done_' + id] = 1; });
setLive(saveC, 1991);
ok('(c) 1991 年 3 部 lead＋fame 70 → 即時 tier 3', W.enc79PlayerTier() === 3, 'leads=' + threeLead.join(','));
W.enc195RecordTierMax();
ok('(c) 殺青後 playerTierMax=3', saveC.flags.playerTierMax === 3);
setLive(saveC, 1992);
ok('(c) 1992 年即時 tier 跌返（當年庫 7 部 lead、全部未做）', W.enc79PlayerTier() < 3, 'live=' + W.enc79PlayerTier());
ok('(c) 1992 年 stem 照係 awi_s3', W.dlg106AweiStem() === 'awi_s3');

/* ---- (d) 舊檔 backfill：經 normalizeSaveObj 載入 ---- */
let oldD = freshSave({ dayIndex: 500, fame: 30, flags: { done_gig_1991_film_102: 1 } });
delete oldD.flags.playerTierMax;
const backD = W.normalizeSaveObj(oldD);
ok('(d) 舊檔（1991 lead、1992 年）載入後 playerTierMax=2', backD.flags.playerTierMax === 2, 'v=' + backD.flags.playerTierMax);
let oldD3 = freshSave({ dayIndex: 500, fame: 70, flags: {} });
threeLead.forEach(id => { oldD3.flags['done_' + id] = 1; });
const backD3 = W.normalizeSaveObj(oldD3);
ok('(d) 舊檔（3 lead＋fame 70）載入後 playerTierMax=3', backD3.flags.playerTierMax === 3, 'v=' + backD3.flags.playerTierMax);
let oldD2 = freshSave({ dayIndex: 500, fame: 70, flags: { playerTierMax: 2 } });
threeLead.forEach(id => { oldD2.flags['done_' + id] = 1; });
const backD2 = W.normalizeSaveObj(oldD2);
ok('(d) 已有最高紀錄唔會俾 backfill 覆寫（2 唔變 3——升 tier 行殺青寫入點）', backD2.flags.playerTierMax === 2, 'v=' + backD2.flags.playerTierMax);
let oldD0 = freshSave({ dayIndex: 500, fame: 5, flags: {} });
const backD0 = W.normalizeSaveObj(oldD0);
ok('(d) 未做過主角嘅舊檔回填 0', backD0.flags.playerTierMax === 0, 'v=' + backD0.flags.playerTierMax);

/* ---- (e) 假男主角陷阱：label 男主角、roleScale 係 support → 唔會計 lead、唔會上 s2 ---- */
// 註：gig_1990_rec_108 係 mtv，lead／support 兩邊都唔計（tier 0，s1 臨記樣，
// 同 tier 1 同一個 stem）；關鍵係唔會誤升做 tier 2／s2。
let saveE = freshSave({ dayIndex: 500, fame: 5, flags: { done_gig_1990_rec_108: 1 } });
const backE = W.normalizeSaveObj(saveE);
ok('(e) 淨做 gig_1990_rec_108（假男主角）→ backfill 0（乜都唔計，唔係 2）', backE.flags.playerTierMax === 0, 'v=' + backE.flags.playerTierMax);
setLive(saveE, 1990);
ok('(e) 假男主角即時 tier 都係 0（1990 年庫入面都唔計 lead）', W.enc79PlayerTier() === 0);
ok('(e) 假男主角 stem 係 awi（s1，唔會變 s2）', W.dlg106AweiStem() === 'awi');
let saveE2 = freshSave({ fame: 5, flags: { done_gig_1990_film_107: 1, done_gig_1990_film_101: 1, done_gig_1992_rec_103: 1 } });
const backE2 = W.normalizeSaveObj(saveE2);
ok('(e) 假男主角＋配角＋MTV 男主角 label 一齊都係 1（仲係配角級）', backE2.flags.playerTierMax === 1, 'v=' + backE2.flags.playerTierMax);

/* ---- (f) 年庫未齊唔寫錯值＋懶回填 ---- */
W.setWIRE({ gigsByYear: { 1990: null, 1991: null, 1992: null } });
ok('(f) 年庫未載入嗰陣 enc195TierFromAllYears 回 null（唔估）',
  W.enc195TierFromAllYears({ done_gig_1991_film_102: 1 }, 30) === null);
let saveF = freshSave({ dayIndex: 500, fame: 30, flags: { done_gig_1991_film_102: 1 } });
const backF = W.normalizeSaveObj(saveF);
ok('(f) 年庫未齊嗰陣 backfill 留空（唔寫 0）', backF.flags.playerTierMax === undefined, 'v=' + backF.flags.playerTierMax);
wirePacks(); //  packs 到齊（實機：boot 完成先讀檔／先播對話）
setLive(saveF, 1992);
ok('(f) packs 到齊後第一次讀 stem，懶回填補返 2、stem 係 awi_s2',
  W.dlg106AweiStem() === 'awi_s2' && saveF.flags.playerTierMax === 2,
  'stem=' + W.dlg106AweiStem() + ' v=' + saveF.flags.playerTierMax);

/* ---- (f 續) 最高紀錄讀取：live 0 都唔跌 ---- */
let saveF2 = freshSave({ fame: 5, flags: { playerTierMax: 2 } });
setLive(saveF2, 1992);
ok('(f) playerTierMax=2、即時 tier 0 → stem 照係 awi_s2', W.dlg106AweiStem() === 'awi_s2');
let saveF3 = freshSave({ fame: 5, flags: { playerTierMax: 3 } });
setLive(saveF3, 1992);
ok('(f) playerTierMax=3 → stem 係 awi_s3', W.dlg106AweiStem() === 'awi_s3');
let saveF0 = freshSave({ fame: 5, flags: {} });
setLive(saveF0, 1992);
ok('(f) 冇紀錄、冇 lead、fame 5 → stem 係 awi（s1）', W.dlg106AweiStem() === 'awi');

console.log(fails.length ? ('AWEI195 LOGIC: ' + fails.length + ' FAIL -> ' + fails.join(' | ')) : 'AWEI195 LOGIC: ALL PASS');
process.exit(fails.length ? 1 : 0);
