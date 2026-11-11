// v20a88 FIX88 邏輯測試：通告荒修復包——
//  (A) 幻影門檻根治：五個年份 pack 行真載入管線（years66Walk → normalizeGigRecord）後，
//      每張 gig 嘅 req 只准含七個真屬性鍵；滿屬狀態下 reqGap 零缺項。
//      另加 reqGap 防禦：未經 normalize 嘅快照 gig 帶 __y66w 都唔可以鎖死玩家。
//  (B) 冬季供應：day 0 冬季新玩家普查（真 gigsForLocSeasonBoard＋canAudition）——
//      可接 ≥3、冬季入門 6 張全可接、春季入門經提早窗一併可接；橋接工門檻釘喺
//      「頭月可達曲線」內、唔係白送（fresh 唔會全接）、去到 day-14 進度至少 3 張接到。
//  (C) 提早窗：賀歲（冬）通告上映前約兩個月已上板、上映季過後唔再出現；
//      春／夏通告同樣行提早窗；上映行 gigReleaseLine88 口徑正確。
//  (D) 復活完整性：POSTER85 五十九張喺管線後主演回填冇斷（leadStar59Of 全數有值）。
// 反證：對 v87 index 行 → FIX88 符號（GIG_REQ_KEYS88／WINTER_*_88／gigSeasonHidden88）
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
const CONSTS = ['STAT_LABEL','LEADSTAR59','POSTER59_STAR_IDS','POSTER85_IDS','ENTRY_GIGS_1988',
  'GIG_REQ_KEYS88','WINTER_ENTRY_GIGS_88','GIG_SEASON_SPAN88','GIG_SEASON_LEAD88'];
const FNS = ['years66ShiftYear','years66ShiftText','years66Walk','years66GigRemap','normalizeGigRecord',
  'bridge56NormalizeGig','leadStar59Apply','leadStar59Of','boardNotePlayerOk','looksLikeEraId','humanizeEraId',
  'reqGap','canAudition','fameFloor','gateTrainHint','isGigWrapped','gigActiveShoot','isGigInProduction',
  'isGigConsumed','seasonRank','calendarSeason','dateObj','boardPriorityRank','boardSortCompare',
  'gigsForLocSeasonBoard','clampEntryReqToTemplate','mergeEntryGigsIntoPool','entryGigPoolLive',
  'ensureEntryTierBoardFill','countApplyableEntryOnBoard','needsEntryBoardFill','weekNumNow',
  'winterBridge88Gig','mergeWinterBridge88','gigSeasonEarlyVisible88','gigSeasonHidden88','gigReleaseLine88','poster85File'];
let WORLD_SRC;
try{
  WORLD_SRC = TF_SRC + '\n' + CONSTS.map(c=>extractConst(c).replace('const '+c, 'var '+c)).join('\n')
    + '\n' + FNS.map(f=>extractFn(f)).join('\n')
    + '\n' + extractConst('WINTER_BRIDGE_GIGS_88').replace('const WINTER_BRIDGE_GIGS_88', 'var WINTER_BRIDGE_GIGS_88');
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
; return { years66Walk, normalizeGigRecord, reqGap, canAudition, mergeEntryGigsIntoPool, mergeWinterBridge88,
  gigsForLocSeasonBoard, entryGigPoolLive, gigSeasonHidden88, gigSeasonEarlyVisible88, seasonRank, calendarSeason,
  leadStar59Of, gigReleaseLine88, setS:(s)=>{S=s;}, setGIGS:(g)=>{GIGS=g;}, getGIGS:()=>GIGS,
  POSTER85_IDS, WINTER_ENTRY_GIGS_88, WINTER_BRIDGE_GIGS_88, GIG_REQ_KEYS88 };`)();
const CANON = { acting:1, stage:1, vocal:1, looks:1, charm:1, iq:1, stamina:1 };
function deepClone(o){ return JSON.parse(JSON.stringify(o)); }
function loadPackPipeline(y){
  const pack = deepClone(JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gigs_'+y+'.json'), 'utf8')));
  W.years66Walk(pack, null);
  return (pack.gigs || []).map(g => W.normalizeGigRecord(g));
}
const MAXED = { acting:999, stage:999, vocal:999, looks:999, charm:999, iq:999, stamina:999, fame:999, dayIndex:0, flags:{}, shoots:[], booked:[], enrolled:{} };
const FRESH = { acting:18, stage:14, vocal:14, looks:22, stamina:75, iq:20, charm:16, fame:5, popularity:3, stress:12, money:12000, dayIndex:0, flags:{}, shoots:[], booked:[], enrolled:{}, board:{}, known:{} };
/* 頭月可達曲線（診斷實測＋訓練增益）：day-14 約 acting 32／stage 22／vocal 19／looks 33／charm 26／iq 21 */
const DAY14 = { acting:32, stage:22, vocal:19, looks:33, stamina:75, iq:21, charm:26, fame:8, popularity:6, stress:20, money:9000, dayIndex:14, flags:{}, shoots:[], booked:[], enrolled:{}, board:{}, known:{} };

/* ---------- (A) 幻影門檻根治 ---------- */
let totalGigs = 0, badKeyGigs = 0, unpassable = 0;
for(const y of [1988, 1989, 1990, 1991, 1992]){
  const gigs = loadPackPipeline(y);
  W.setS(deepClone(MAXED));
  for(const g of gigs){
    totalGigs++;
    if(Object.keys(g.req||{}).some(k=>!CANON[k])) badKeyGigs++;
    if(W.reqGap(g).missing !== 0) unpassable++;
  }
}
ok('A1 五包 351 張全行管線（實數 '+totalGigs+'）', totalGigs === 351);
ok('A2 管線後 req 非屬性鍵殘留 = 0（實數 '+badKeyGigs+'）', badKeyGigs === 0);
ok('A3 滿屬狀態下 reqGap 缺項 = 0 張（實數 '+unpassable+'）', unpassable === 0);
W.setS(deepClone(FRESH));
const snapshotGig = { id:'snap_test', req:{ acting:18, __y66w:1, __debug:'x' } };
ok('A4 reqGap 防禦：未經 normalize 嘅快照帶工程鍵都唔鎖（missing=0）', W.reqGap(snapshotGig).missing === 0 && W.reqGap(snapshotGig).keys === 1);
ok('A5 GIG_REQ_KEYS88 只有七真屬性鍵', Object.keys(W.GIG_REQ_KEYS88).length === 7 && Object.keys(W.GIG_REQ_KEYS88).every(k=>CANON[k]));

/* ---------- (B) 冬季供應 ---------- */
const pool1990 = loadPackPipeline(1988);
W.setGIGS(pool1990.slice());
W.setS(deepClone(FRESH));
W.mergeEntryGigsIntoPool();
W.mergeWinterBridge88();
const pool = W.getGIGS();
ok('B1 冬季入門 6 張入池', W.WINTER_ENTRY_GIGS_88.length === 6 && W.WINTER_ENTRY_GIGS_88.every(w=>pool.some(g=>g.id===w.id)));
ok('B2 冬季橋接 6 張入池', W.WINTER_BRIDGE_GIGS_88.length === 6 && W.WINTER_BRIDGE_GIGS_88.every(w=>pool.some(g=>g.id===w.id)));
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
const winterEntryIds = W.WINTER_ENTRY_GIGS_88.map(g=>g.id);
ok('B5 冬季入門 6 張 day0 全可接', winterEntryIds.every(id=>c0.apply.includes(id)));
ok('B6 春季入門經提早窗 day0 亦可接（≥4/6）', W.WINTER_ENTRY_GIGS_88.length===6 && ['gig_1988_entry_ad_passerby','gig_1988_entry_crew_assist','gig_1988_entry_street_extra','gig_1988_entry_ferry_crowd','gig_1988_entry_print_hand','gig_1988_entry_rec_clap'].filter(id=>c0.apply.includes(id)).length >= 4);
/* 橋接校準：req 全部落喺頭月曲線上限內；fresh 唔會全接；day-14 至少 3 張接到 */
const CURVE_MAX = { acting:32, stage:24, vocal:22, looks:30, charm:24, iq:24, stamina:75 };
ok('B7 橋接 req 全部 ≤ 頭月可達曲線', W.WINTER_BRIDGE_GIGS_88.every(g=>Object.entries(g.req||{}).every(([k,v])=>CANON[k] && v <= CURVE_MAX[k])));
const bridgeAtFresh = W.WINTER_BRIDGE_GIGS_88.filter(g=>{ W.setS(deepClone(FRESH)); const p = pool.find(x=>x.id===g.id); return p && W.canAudition(p).ok; }).length;
ok('B8 橋接唔係白送：fresh 接到 ≤2/6（實數 '+bridgeAtFresh+'）', bridgeAtFresh <= 2);
const bridgeAt14 = W.WINTER_BRIDGE_GIGS_88.filter(g=>{ W.setS(deepClone(DAY14)); const p = pool.find(x=>x.id===g.id); return p && W.canAudition(p).ok; }).length;
ok('B9 橋接 day-14 進度接到 ≥3/6（實數 '+bridgeAt14+'）', bridgeAt14 >= 3);

/* ---------- (C) 提早窗 ---------- */
function atDay(di){ const s = deepClone(FRESH); s.dayIndex = di; W.setS(s); }
const springEntry = pool.find(g=>g.id==='gig_1988_entry_ad_passerby');
atDay(0);
ok('C1 春通告 day0（冬）已入提早窗上板（seasonRank>0 但 hidden=false）', W.seasonRank(springEntry, '冬') > 0 && W.gigSeasonHidden88(springEntry, '冬') === false);
atDay(165); /* 1990-06-15 夏 */
ok('C2 春通告上映季過後（6 月中）唔再出現', W.gigSeasonHidden88(springEntry, '夏') === true);
const summerGig = pool1990.find(g=>g.season==='夏');
atDay(73); /* 1990-03-15 春 */
ok('C3 夏通告 3 月中未入提早窗（hidden）', !!summerGig && W.gigSeasonHidden88(summerGig, '春') === true);
atDay(104); /* 1990-04-14 春，距 6 月 1 日 48 日 */
ok('C4 夏通告 4 月中已入提早窗上板', !!summerGig && W.gigSeasonHidden88(summerGig, '春') === false);
const cnyBridge = pool.find(g=>g.id==='gig_1988_winter88_bridge_cny_support');
atDay(257); /* 1990-09-14 秋，距 12 月 1 日 78 日 */
ok('C5 賀歲通告 9 月中未上板（早過提早窗）', W.gigSeasonHidden88(cnyBridge, '秋') === true);
atDay(287); /* 1990-10-14 秋，距 12 月 1 日 48 日 */
ok('C6 賀歲通告 10 月中已上板（上映前約兩個月）', W.gigSeasonHidden88(cnyBridge, '秋') === false);
atDay(73);
ok('C7 賀歲通告唔會喺上映後先出現（3 月已落板）', W.gigSeasonHidden88(cnyBridge, '春') === true);
ok('C8 上映行：賀歲橋接用 releaseLabel', W.gigReleaseLine88(cnyBridge).includes('賀歲檔'));
const springFilm = pool1990.find(g=>g.season==='春' && g.type==='電影');
ok('C9 上映行：春季電影衍生「預計上映：1990 年春季」', !!springFilm && W.gigReleaseLine88(springFilm) === '預計上映：'+springFilm.year+' 年春季');

/* ---------- (D) 復活完整性 ---------- */
let lsOk = 0; const p85 = Object.keys(W.POSTER85_IDS||{});
for(const id of p85){ const g = pool.find(x=>x.id===id); if(g && W.leadStar59Of(g)) lsOk++; }
ok('D1 POSTER85 主演回填完整（'+lsOk+'/'+p85.length+'）', p85.length === 59 && lsOk === 59);
const entryLive = (()=>{ atDay(0); return W.entryGigPoolLive(); })();
ok('D2 入門池 day0 冬季非空（實數 '+entryLive.length+'）', entryLive.length >= 6);

console.log(fails.length ? ('FAILURES: '+fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
