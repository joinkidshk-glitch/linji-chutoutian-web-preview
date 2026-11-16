// v20a88 FIX88 邏輯測試：通告荒修復包（v20a229 B3 新庫版）——
//  (A) 幻影門檻根治：新庫 251 張行真載入管線（normalizeGigRecord）後，
//      每張 gig 嘅 req 只准含七個真屬性鍵；滿屬狀態下 reqGap 零缺項。
//      另加 reqGap 防禦：未經 normalize 嘅快照 gig 帶 __y66w 都唔可以鎖死玩家。
//  (B) 冬季供應：day 0 冬季新玩家普查（真 gigsForLocSeasonBoard＋canAudition）——
//      可接 33 張、入門 12 張入面 day0 可接 8 張（冬 6＋春提早窗 2）；冬季入門 6 張
//      day0 全可接、春季入門 2 張經提早窗 day0 亦可接；入口池 req 全部 ≤ 開局數值；
//      橋接池已清空（WINTER_BRIDGE_GIGS_88＝[]，merge 唔加嘢）。
//  (C) 提早窗：賀歲（冬）通告上映前約兩個月已上板、上映季過後唔再出現；
//      春／夏通告同樣行提早窗；上映行 gigReleaseLine88 口徑正確。
//  (D) 主演反查完整性：新庫 142 張作品（除 129 主演未定外）全部有 leadStarId，leadStar59Of 全部反查到
//      中文名（含名冊外補位彭少祺／程天諾）；入門池 day0 冬季非空。
// 反證：對 v87 index 行 → FIX88 符號（GIG_REQ_KEYS88／gigSeasonHidden88）
//      唔存在，抽取即 FAIL。
// 用法：node tests/test_fix88_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) throw new Error('fn not found: '+name);
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){ if(html[j]==='{') depth++; else if(html[j]==='}'){ depth--; if(depth===0) break; } }
  return html.slice(i, j+1);
}
function extractConst(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) throw new Error('const not found: '+name);
  let depth=0, started=false;
  for(let k=i; k<html.length; k++){
    const ch = html[k];
    if(ch==='{'||ch==='['){ depth++; started = true; }
    else if(ch==='}'||ch===']'){ depth--; if(started && depth===0) return html.slice(i, k+1)+';'; }
    else if(ch===';' && !started) return html.slice(i, k+1);
  }
  throw new Error('const end not found: '+name);
}
const tfA = html.indexOf('/* ==== v20a55 TEXTFIX');
const tfB = html.indexOf('async function refreshCopyPacksFromDisk(){');
if(tfA<0 || tfB<=tfA){ console.log('FAIL TEXTFIX55 block not found'); process.exit(1); }
const TF_SRC = html.slice(tfA, tfB);
const CONSTS = ['STAT_LABEL','POSTER59_STAR_IDS',
  'GIG_REQ_KEYS88','GIG_SEASON_SPAN88','GIG_SEASON_LEAD88'];
const FNS = ['normalizeGigRecord',
  'bridge56NormalizeGig','leadStar59Of','boardNotePlayerOk','looksLikeEraId','humanizeEraId',
  'reqGap','canAudition','fameFloor','gateTrainHint','isGigWrapped','gigActiveShoot','isGigInProduction',
  'isGigConsumed','seasonRank','calendarSeason','dateObj','boardPriorityRank','boardSortCompare',
  'gigsForLocSeasonBoard','clampEntryReqToTemplate','mergeEntryGigsIntoPool','entryGigPool229','entryGigPoolLive',
  'ensureEntryTierBoardFill','countApplyableEntryOnBoard','needsEntryBoardFill','weekNumNow',
  'mergeWinterBridge88','gigSeasonEarlyVisible88','gigSeasonHidden88','gigReleaseLine88'];
let WORLD_SRC;
try{
  WORLD_SRC = TF_SRC + '\n' + CONSTS.map(c=>extractConst(c).replace('const '+c, 'var '+c)).join('\n')
    + '\n' + FNS.map(f=>extractFn(f)).join('\n');
}catch(e){ console.log('FAIL extraction（v87 反證應在此觸發）: '+e.message); process.exit(1); }
const STUBS_SRC = `
  var START = { y:1990, m:1, d:1 };
  var S = null;
  var GIGS = [];
  var COURSE_DEFS = {};
  var softPreviewOn = function(){ return false; };
  var mergeSoftBridgeGigs = function(){ return 0; };
  var mergeIntelGigs = function(){ return 0; };
  var mergeFavorGigs = function(){ return 0; };
  var mergeRivalGigs = function(){ return 0; };
  var mergeExodusGigs = function(){ return 0; };
  var mergeMidGigs35 = function(){ return 0; };
  var mergeWf3Gigs = function(){ return 0; };
`;
const W = new Function(STUBS_SRC + WORLD_SRC + `
; return { normalizeGigRecord, reqGap, canAudition, mergeEntryGigsIntoPool, mergeWinterBridge88,
  gigsForLocSeasonBoard, entryGigPoolLive, entryGigPool229, gigSeasonHidden88, gigSeasonEarlyVisible88, seasonRank, calendarSeason,
  leadStar59Of, gigReleaseLine88, setS:(s)=>{S=s;}, setGIGS:(g)=>{GIGS=g;}, getGIGS:()=>GIGS,
  GIG_REQ_KEYS88 };`)();
const CANON = { acting:1, stage:1, vocal:1, looks:1, charm:1, iq:1, stamina:1 };
const OPENING = { acting:18, stage:14, vocal:14, looks:22, charm:16, iq:20, stamina:75 };
function deepClone(o){ return JSON.parse(JSON.stringify(o)); }
const PACK_NEW = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gigs_new.json'), 'utf8'));
function loadPackPipeline(y){
  return (PACK_NEW.gigs || []).filter(g => g.year === y).map(g => W.normalizeGigRecord(deepClone(g)));
}
const MAXED = { acting:999, stage:999, vocal:999, looks:999, charm:999, iq:999, stamina:999, fame:999, dayIndex:0, flags:{}, shoots:[], booked:[], enrolled:{} };
const FRESH = { acting:18, stage:14, vocal:14, looks:22, stamina:75, iq:20, charm:16, fame:5, popularity:3, stress:12, money:12000, dayIndex:0, flags:{}, shoots:[], booked:[], enrolled:{}, board:{}, known:{} };
/* 頭月可達曲線（診斷實測＋訓練增益）：day-14 約 acting 32／stage 22／vocal 19／looks 33／charm 26／iq 21 */
const DAY14 = { acting:32, stage:22, vocal:19, looks:33, stamina:75, iq:21, charm:26, fame:8, popularity:6, stress:20, money:9000, dayIndex:14, flags:{}, shoots:[], booked:[], enrolled:{}, board:{}, known:{} };

/* ---------- (A) 幻影門檻根治 ---------- */
let totalGigs = 0, badKeyGigs = 0, unpassable = 0;
for(const y of [1990, 1991, 1992]){
  const gigs = loadPackPipeline(y);
  W.setS(deepClone(MAXED));
  for(const g of gigs){
    totalGigs++;
    if(Object.keys(g.req||{}).some(k=>!CANON[k])) badKeyGigs++;
    if(W.reqGap(g).missing !== 0) unpassable++;
  }
}
ok('A1 新庫 251 張全行管線（實數 '+totalGigs+'）', totalGigs === 251);
ok('A2 管線後 req 非屬性鍵殘留 = 0（實數 '+badKeyGigs+'）', badKeyGigs === 0);
ok('A3 滿屬狀態下 reqGap 缺項 = 0 張（實數 '+unpassable+'）', unpassable === 0);
W.setS(deepClone(FRESH));
const snapshotGig = { id:'snap_test', req:{ acting:18, __y66w:1, __debug:'x' } };
ok('A4 reqGap 防禦：未經 normalize 嘅快照帶工程鍵都唔鎖（missing=0）', W.reqGap(snapshotGig).missing === 0 && W.reqGap(snapshotGig).keys === 1);
ok('A5 GIG_REQ_KEYS88 只有七真屬性鍵', Object.keys(W.GIG_REQ_KEYS88).length === 7 && Object.keys(W.GIG_REQ_KEYS88).every(k=>CANON[k]));

/* ---------- (B) 冬季供應 ---------- */
const pool1990 = loadPackPipeline(1990);
W.setGIGS(pool1990.slice());
W.setS(deepClone(FRESH));
W.mergeEntryGigsIntoPool();
const poolSizeAfterEntry = W.getGIGS().length;
W.mergeWinterBridge88();
const pool = W.getGIGS();
const entryTier = pool.filter(g => g.entryTier);
ok('B1 入口池 12 張入池（新庫篩出，entryTier）', entryTier.length === 12 && entryTier.every(g=>pool.some(x=>x.id===g.id)));
ok('B2 橋接池已清空（mergeWinterBridge88 唔加嘢，池維持 '+poolSizeAfterEntry+' 張）', W.getGIGS().length === poolSizeAfterEntry && poolSizeAfterEntry === 104);
const LOCS = ['cafe_cha','rec_hk','tvb_longmen','film_lion','film_cotton','film_harbour','tvb_harbour','tvb_kowloon','ad_central','ad_adm','rec_wanchai','rec_star','agency_ho'];
function census(state){
  W.setS(deepClone(state));
  let cards = 0, apply = [], entryApply = 0;
  for(const loc of LOCS){
    const shown = W.gigsForLocSeasonBoard(loc, '冬');
    cards += shown.length;
    for(const g of shown){ if(W.canAudition(g).ok){ apply.push(g.id); if(g.entryTier) entryApply++; } }
  }
  return { cards, apply, entryApply };
}
const c0 = census(FRESH);
ok('B3 day0 冬季板面可接 ≥3（實數 '+c0.apply.length+'）', c0.apply.length >= 3);
ok('B4 day0 入門可接 ≥3（實數 '+c0.entryApply+'）', c0.entryApply >= 3);
const winterEntryIds = ['gig_1990_film_113','gig_1990_film_118','gig_1990_film_123','gig_1990_tv_113','gig_1990_rec_116','gig_1990_ad_110'];
ok('B5 冬季入門 6 張 day0 全可接', winterEntryIds.every(id=>c0.apply.includes(id)));
ok('B6 春季入門經提早窗 day0 亦可接（2/2：gig_1990_film_119／gig_1990_rec_117）',
  ['gig_1990_film_119','gig_1990_rec_117'].every(id=>c0.apply.includes(id)));
/* 入口池校準：req 全部落喺開局數值內；day0 入門可接 8/12（冬 6＋春提早窗 2，夏／秋 4 張未到窗）；day-14 唔跌 */
ok('B7 入口池 req 全部 ≤ 開局數值（12/12）',
  W.entryGigPool229().length === 12 && W.entryGigPool229().every(g=>Object.entries(g.req||{}).every(([k,v])=>CANON[k] && v <= OPENING[k])));
ok('B8 day0 入門可接 8/12（實數 '+c0.entryApply+'）', c0.entryApply === 8);
const c14 = census(DAY14);
ok('B9 day-14 入門可接仍 8/12、板面可接唔少過 day0（實數 '+c14.entryApply+'／'+c14.apply.length+'）',
  c14.entryApply === 8 && c14.apply.length >= c0.apply.length);

/* ---------- (C) 提早窗 ---------- */
function atDay(di){ const s = deepClone(FRESH); s.dayIndex = di; W.setS(s); }
const springEntry = pool.find(g=>g.id==='gig_1990_film_119');
atDay(0);
ok('N1 春通告 day0（冬）已入提早窗上板（seasonRank>0 但 hidden=false）', W.seasonRank(springEntry, '冬') > 0 && W.gigSeasonHidden88(springEntry, '冬') === false);
atDay(165); /* 1990-06-15 夏 */
ok('N2 春通告上映季過後（6 月中）唔再出現', W.gigSeasonHidden88(springEntry, '夏') === true);
const summerGig = pool1990.find(g=>g.season==='夏');
atDay(73); /* 1990-03-15 春 */
ok('N3 夏通告 3 月中未入提早窗（hidden）', !!summerGig && W.gigSeasonHidden88(summerGig, '春') === true);
atDay(104); /* 1990-04-14 春，距 6 月 1 日 48 日 */
ok('N4 夏通告 4 月中已入提早窗上板', !!summerGig && W.gigSeasonHidden88(summerGig, '春') === false);
const cnyBridge = pool.find(g=>g.id==='gig_1990_film_101');
atDay(257); /* 1990-09-14 秋，距 12 月 1 日 78 日 */
ok('N5 賀歲通告 9 月中未上板（早過提早窗）', W.gigSeasonHidden88(cnyBridge, '秋') === true);
atDay(287); /* 1990-10-14 秋，距 12 月 1 日 48 日 */
ok('N6 賀歲通告 10 月中已上板（上映前約兩個月）', W.gigSeasonHidden88(cnyBridge, '秋') === false);
atDay(73);
ok('N7 賀歲通告唔會喺上映後先出現（3 月已落板）', W.gigSeasonHidden88(cnyBridge, '春') === true);
ok('N9 上映行：賀歲冬片衍生「預計上映：1990 年冬季」', W.gigReleaseLine88(cnyBridge) === '預計上映：1990 年冬季');
const springFilm = pool1990.find(g=>g.season==='春' && g.type==='電影');
ok('N10 上映行：春季電影衍生「預計上映：1990 年春季」', !!springFilm && W.gigReleaseLine88(springFilm) === '預計上映：'+springFilm.year+' 年春季');

/* ---------- (D) 主演反查完整性 ---------- */
const allPool = [1990, 1991, 1992].flatMap(y => loadPackPipeline(y));
const works = allPool.filter(g => g.category === '作品');
ok('D1 新庫 142 張作品除《冬日單元劇》主演未定外全部有 leadStarId，leadStar59Of 全部反查到中文名（v250：gig_1990_tv_129 leadStarId null 已知，等選角拍板）',
  works.length === 142 && works.filter(g=>g.id !== 'gig_1990_tv_129').every(g=>g.leadStarId) && works.filter(g=>g.leadStarId).every(g=>W.leadStar59Of(g)));
ok('D1b 名冊外補位：彭少祺／程天諾照反查到',
  W.leadStar59Of(allPool.find(g=>g.id==='gig_1990_ad_105')) === '彭少祺' &&
  W.leadStar59Of(allPool.find(g=>g.id==='gig_1992_rec_102')) === '程天諾');
const entryLive = (()=>{ atDay(0); return W.entryGigPoolLive(); })();
ok('D2 入門池 day0 冬季非空（實數 '+entryLive.length+'）', entryLive.length >= 6);

console.log(fails.length ? ('FAILURES: '+fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
