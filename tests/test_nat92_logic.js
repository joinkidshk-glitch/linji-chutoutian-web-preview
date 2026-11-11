// v20a92 NAT92 邏輯測試：通告板分布自然化——
//  (A) 決定性：偏移/落板拉前按 id 雜湊，兩個獨立 world 計出嚟逐張一致；重載（重行管線）不變。
//  (B) 豁免：entryTier/softBridge 唔錯峰；年初已開窗 interval 偏移恆 0（開局板面唔俾抽乾）。
//  (C) 夾位：逐張逐 interval 驗 off+pull+工期所需日曆日 ≤ interval 長度（接咗拍得完）。
//  (D) 開局守衛：day-0 FRESH 可接 ≥12（v88/v90 口徑，基線 12）；第一週逐日逐地點 ≥1 可接
//      （含 v91 基線缺供應嘅紅棉影業／灣仔唱片——由 NAT92 入門補位）。
//  (E) 分布守衛：52 週普查（MAXED 組成）1990「恰好 2」占比 <40%（基線 62.2%）；
//      三年全板 0 嘅地點-週 = 0（保底生效）。
//  (F) 加厚：NAT92_GIGS 18 張；逐年入池數啱（1990:14／1991:2／1992:2）；中/高新工
//      工期入 ROLE_SCALE_BAND、日薪入 DUR90_DAILY 帶；req 只含七真屬性鍵。
// 反證：對 v91 index 行 → NAT92 符號唔存在，抽取即 FAIL。
// 用法：node tests/test_nat92_logic.js [path-to-index.html]
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
  'GIG_REQ_KEYS88','WINTER_ENTRY_GIGS_88','GIG_SEASON_SPAN88','GIG_SEASON_LEAD88',
  'SHOOT_DAYS','ROLE_SCALE_BAND','MID_GIGS_1988_35','SOFT_BRIDGE_GIGS_1988',
  'DUR90_OLD_BAND','DUR90_DAILY','NAT92_SPREAD','NAT92_PULL_MAX','NAT92_PULL_OPEN_MAX'];
const FNS = ['years66ShiftYear','years66ShiftText','years66Walk','years66GigRemap','normalizeGigRecord',
  'bridge56NormalizeGig','leadStar59Apply','leadStar59Of','boardNotePlayerOk','looksLikeEraId','humanizeEraId',
  'clamp','resolveRoleScale','shootBandFor','effectiveShootDays','effectiveShootWeekdays',
  'effectiveShootDeadlineDays','gigPayExact','winterBridge88Gig','softBridgeGig','gig36',
  'dur90RoundPay','dur90CalibrateGig',
  'reqGap','canAudition','fameFloor','gateTrainHint','isGigWrapped','gigActiveShoot','isGigInProduction',
  'isGigConsumed','seasonRank','calendarSeason','dateObj','boardPriorityRank','boardSortCompare',
  'gigsForLocSeasonBoard','clampEntryReqToTemplate','mergeEntryGigsIntoPool','entryGigPoolLive',
  'ensureEntryTierBoardFill','countApplyableEntryOnBoard','needsEntryBoardFill','weekNumNow',
  'mergeWinterBridge88','mergeMidGigs35','mergeYearGigs36','mergeSoftBridgeGigs',
  'gigSeasonEarlyVisible88','gigSeasonHidden88','gigReleaseLine88','poster85File',
  'nat92Hash','nat92StaggerEligible','nat92DayIdxOf','nat92PostIntervals','nat92WindowStartDay',
  'nat92CalNeedDays','nat92BoardOffsetDays','gigBoardPosted92','nat92Gig','mergeNat92Gigs'];
let WORLD_SRC;
try{
  WORLD_SRC = TF_SRC + '\n' + CONSTS.map(c=>extractConst(c).replace('const '+c, 'var '+c)).join('\n')
    + '\n' + FNS.map(f=>extractFn(f)).join('\n')
    + '\n' + extractConst('WINTER_BRIDGE_GIGS_88').replace('const WINTER_BRIDGE_GIGS_88', 'var WINTER_BRIDGE_GIGS_88')
    + '\n' + ['GIGS36_1989_SPRING_F5','GIGS36_1989_BRIDGE','GIGS36_1989_HIGH_F2','GIGS36_1989_MID_F3',
      'GIGS36_1990_AUTUMN_F6','GIGS36_1990_BRIDGE','GIGS36_1990_FINALE_F7','GIGS36_1990_HIGH_F2','GIGS36_1990_MID_F3',
      'GIGS36_BY_YEAR','GIGS36_ALL_IDS'].map(c=>extractConst(c).replace('const '+c, 'var '+c)).join('\n')
    + '\n' + extractConst('NAT92_GIGS').replace('const NAT92_GIGS', 'var NAT92_GIGS')
    + '\n' + extractConst('NAT92_ALL_IDS').replace('const NAT92_ALL_IDS', 'var NAT92_ALL_IDS');
}catch(e){ console.log('FAIL extraction（v91 反證應在此觸發）: '+e.message); process.exit(1); }
const STUBS_SRC = `
  var START = { y:1990, m:1, d:1 };
  var S = null;
  var GIGS = [];
  var COURSE_DEFS = {};
  var softPreviewOn = function(){ return false; };
`;
function buildWorld(){
  return new Function(STUBS_SRC + WORLD_SRC + `
  ; return { years66Walk, normalizeGigRecord, canAudition, gigsForLocSeasonBoard, calendarSeason,
    mergeEntryGigsIntoPool, mergeWinterBridge88, mergeNat92Gigs, gigBoardPosted92,
    nat92StaggerEligible, nat92PostIntervals, nat92BoardOffsetDays, nat92CalNeedDays,
    effectiveShootDays, gigPayExact, resolveRoleScale,
    setS:(s)=>{S=s;}, setGIGS:(g)=>{GIGS=g;}, getGIGS:()=>GIGS,
    NAT92_GIGS, DUR90_DAILY, ROLE_SCALE_BAND };`)();
}
const W = buildWorld();
function deepClone(o){ return JSON.parse(JSON.stringify(o)); }
function loadPackPipeline(y){
  const pack = deepClone(JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gigs_'+y+'.json'), 'utf8')));
  W.years66Walk(pack, null);
  return (pack.gigs || []).map(g => W.normalizeGigRecord(g));
}
const FRESH = { acting:18, stage:14, vocal:14, looks:22, stamina:75, iq:20, charm:16, fame:5, popularity:3, stress:12, money:12000, dayIndex:0, flags:{}, shoots:[], booked:[], enrolled:{}, board:{}, known:{} };
const MAXED = { acting:999, stage:999, vocal:999, looks:999, charm:999, iq:999, stamina:999, fame:999, popularity:999, stress:0, money:999999, dayIndex:0, flags:{}, shoots:[], booked:[], enrolled:{}, board:{}, known:{}, wrapHistory:[] };
const LOCS = ['cafe_cha','rec_hk','tvb_longmen','film_lion','film_cotton','film_harbour','tvb_harbour','tvb_kowloon','ad_central','ad_adm','rec_wanchai','rec_star','agency_ho'];
const GIG_LOCS = LOCS.filter(l=>l!=='cafe_cha' && l!=='agency_ho');
const YEAR_FILE = { 1990:1988, 1991:1989, 1992:1990 };
const YEAR_START = { 1990:0, 1991:365, 1992:730 };
function setupYearPool(year){
  W.setGIGS(loadPackPipeline(YEAR_FILE[year]));
  const st = deepClone(MAXED); st.dayIndex = YEAR_START[year];
  W.setS(st);
  if(year===1990){ W.mergeEntryGigsIntoPool(); W.mergeWinterBridge88(); }
  W.gigsForLocSeasonBoard(GIG_LOCS[0], W.calendarSeason());
  return W.getGIGS();
}

/* ---------- (F) 加厚表 ---------- */
ok('F1 NAT92_GIGS 共 18 張', W.NAT92_GIGS.length === 18);
const CANON = { acting:1, stage:1, vocal:1, looks:1, charm:1, iq:1, stamina:1 };
let fBad = [];
for(const raw of W.NAT92_GIGS){
  const g = W.normalizeGigRecord(deepClone(raw));
  if(Object.keys(g.req||{}).some(k=>!CANON[k])) fBad.push(g.id+':req鍵');
  if(g.entryTier) continue;
  const band = W.ROLE_SCALE_BAND[W.resolveRoleScale(g) || g.roleScale];
  const days = W.effectiveShootDays(g);
  if(!band || days < band[0] || days > band[1]) fBad.push(g.id+':工期出帶');
  const pay = W.gigPayExact(g);
  const isAd = ['ad_av','ad_print','photobook'].includes(g.roleScale);
  const db = (W.DUR90_DAILY[g.tier||'初'] || W.DUR90_DAILY['初'])[isAd?1:0];
  const daily = pay / Math.max(1, days);
  if(daily < db[0] || daily > db[1]) fBad.push(g.id+':日薪出帶('+Math.round(daily)+')');
}
ok('F2 中/高新工工期入帶＋日薪入帶＋req 純屬性（違規：'+(fBad.join(',')||'無')+'）', fBad.length === 0);
const poolByYear = {};
for(const y of [1990, 1991, 1992]){
  poolByYear[y] = setupYearPool(y);
  const n = poolByYear[y].filter(g=>g.nat92).length;
  ok('F3 '+y+' 年 NAT92 入池 '+(y===1990?14:2)+' 張（實數 '+n+'）', n === (y===1990 ? 14 : 2));
}

/* ---------- (A) 決定性 ---------- */
{
  const W2 = buildWorld();
  const sig = w => poolByYear[1990].map(g => g.id + ':' + (w.nat92BoardOffsetDays ? w.nat92BoardOffsetDays(g) : 0) + ':' +
    (w.nat92PostIntervals ? JSON.stringify(w.nat92PostIntervals(g).map(iv=>[iv.post, iv.last])) : '')).join('|');
  W2.setGIGS(poolByYear[1990].slice()); W2.setS(deepClone(MAXED));
  ok('A1 兩個獨立 world 偏移/上板日逐張一致', sig(W) === sig(W2));
  const g0 = poolByYear[1990].find(g=>W.nat92StaggerEligible(g));
  const v1 = JSON.stringify(W.nat92PostIntervals(g0));
  const v2 = JSON.stringify(W.nat92PostIntervals(deepClone(g0)));
  ok('A2 同一 gig 深拷貝重計 intervals 不變', v1 === v2);
}

/* ---------- (B) 豁免 ---------- */
{
  const pool = poolByYear[1990];
  const badExempt = pool.filter(g => (g.entryTier || g.softBridge) && W.nat92StaggerEligible(g));
  ok('B1 entryTier/softBridge 全部唔錯峰（違規 '+badExempt.length+'）', badExempt.length === 0);
  let openBad = 0, stagN = 0;
  for(const y of [1990, 1991, 1992]){
    for(const g of poolByYear[y]){
      if(!W.nat92StaggerEligible(g)) continue;
      stagN++;
      const yStart = Math.round((new Date(g.year, 0, 1) - new Date(1990, 0, 1)) / 86400000);
      for(const iv of W.nat92PostIntervals(g)) if(iv.from <= yStart && iv.off !== 0) openBad++;
    }
  }
  ok('B2 年初已開窗 interval 偏移恆 0（違規 '+openBad+'／錯峰 gig '+stagN+' 張）', openBad === 0 && stagN > 200);
}

/* ---------- (C) 夾位 ---------- */
{
  let bad = [];
  for(const y of [1990, 1991, 1992]){
    for(const g of poolByYear[y]){
      if(!W.nat92StaggerEligible(g)) continue;
      const cal = W.nat92CalNeedDays(g);
      for(const iv of W.nat92PostIntervals(g)){
        if(iv.off + iv.pull + cal > (iv.to - iv.from + 1)) bad.push(g.id);
      }
    }
  }
  ok('C1 逐張逐 interval：偏移+拉前+工期日曆日 ≤ interval 長度（違規 '+(bad.slice(0,3).join(',')||'無')+'）', bad.length === 0);
}

/* ---------- (D) 開局守衛 ---------- */
{
  setupYearPool(1990);
  let day0Apply = 0; const perLocDay = [];
  for(let d = 0; d < 7; d++){
    const st = deepClone(FRESH); st.dayIndex = d; W.setS(st);
    const row = {};
    for(const loc of LOCS){
      const shown = W.gigsForLocSeasonBoard(loc, W.calendarSeason());
      const ap = shown.filter(g=>W.canAudition(g).ok).length;
      row[loc] = ap;
      if(d === 0) day0Apply += ap;
    }
    perLocDay.push(row);
  }
  ok('D1 day-0 全板可接 ≥12（實數 '+day0Apply+'）', day0Apply >= 12);
  const badLoc = GIG_LOCS.filter(loc => perLocDay.some(row => row[loc] < 1));
  ok('D2 第一週逐日每個有通告地點 ≥1 可接（違規地點：'+(badLoc.join(',')||'無')+'）', badLoc.length === 0);
  ok('D3 紅棉影業 day-0 有可接（NAT92 入門補位）', perLocDay[0]['film_cotton'] >= 1);
  ok('D4 灣仔唱片 day-0 有可接（NAT92 入門補位）', perLocDay[0]['rec_wanchai'] >= 1);
}

/* ---------- (E) 分布守衛 ---------- */
{
  function censusYear(year){
    setupYearPool(year);
    let tot = 0, ex2 = 0, zero = 0;
    for(let w = 0; w < 52; w++){
      const st = deepClone(MAXED); st.dayIndex = YEAR_START[year] + w * 7; W.setS(st);
      for(const loc of GIG_LOCS){
        const shown = W.gigsForLocSeasonBoard(loc, W.calendarSeason());
        if(!shown.length){ zero++; continue; }
        const tiers = { '中':0, '高':0 };
        shown.forEach(g=>{ if(tiers[g.tier] != null) tiers[g.tier]++; });
        for(const t of ['中','高']){ tot++; if(tiers[t] === 2) ex2++; }
      }
    }
    return { tot, ex2, pct: 100 * ex2 / tot, zero };
  }
  const c90 = censusYear(1990);
  ok('E1 1990「恰好 2」占比 <40%（實數 '+c90.pct.toFixed(1)+'%）', c90.pct < 40);
  const c91 = censusYear(1991), c92 = censusYear(1992);
  ok('E2 三年全板 0 地點-週 = 0（實數 '+(c90.zero + c91.zero + c92.zero)+'）', (c90.zero + c91.zero + c92.zero) === 0);
  ok('E3 1991/1992「恰好 2」占比 <40%（實數 '+c91.pct.toFixed(1)+'%／'+c92.pct.toFixed(1)+'%）', c91.pct < 40 && c92.pct < 40);
}

console.log(fails.length ? ('FAILURES: '+fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
