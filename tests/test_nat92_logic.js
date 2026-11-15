// v20a92 NAT92 邏輯測試：通告板分布自然化（v20a229 B3 新庫版）——
//  (A) 決定性：偏移/落板拉前按 id 雜湊，兩個獨立 world 計出嚟逐張一致；重載（重行管線）不變。
//  (B) 豁免：entryTier/softBridge 唔錯峰；年初已開窗 interval 偏移恆 0（開局板面唔俾抽乾）。
//  (C) 夾位：逐張逐 interval 驗 off+pull+工期所需日曆日 ≤ interval 長度（接咗拍得完）。
//  (D) 開局守衛：day-0 FRESH 可接 ≥12（v88/v90 口徑，基線 12）；第一週逐日逐地點 ≥1 可接——
//      新庫例外：九龍電視台（tvb_kowloon）第一週 0 可接（見 D2 註）；
//      紅棉影業／灣仔唱片 day-0 有可接（新庫供應，唔再靠 NAT92 入門補位）。
//  (E) 分布守衛：52 週普查（MAXED 組成）1990「恰好 2」占比 <40%；
//      三年全板 0 嘅地點-週＝94（新庫地點-季節洞，見 E2 註——舊版 0 係 351 張＋18 張
//      注入先做到，新庫 240 張有季節性空洞，呢個數係分佈釘，唔係回歸目標）。
//      v20a229 B5：MAXED 而家真係 maxed——47 張 trigger 條件齊開（E0 守衛，v232 補寫《星夜迷離》第 241 張），
//      E2 釘先至繼續量度庫分佈而唔係觸發狀態；沙盒抽埋 triggerGigOn＋依賴，
//      唔係 board filter 嘅 typeof 守衛會將全部 trigger 通告當未觸發隱藏。
//  (F) 注入池已刪：NAT92_GIGS 18 張拎走，mergeNat92Gigs 回 0；錯峰資格改由
//      新庫 gig 本身判定（229 張合資格、12 張入門唔錯峰）；舊 nat92 旗全庫 0 命中。
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
const CONSTS = ['STAT_LABEL','POSTER59_STAR_IDS',
  'GIG_REQ_KEYS88','GIG_SEASON_SPAN88','GIG_SEASON_LEAD88',
  'SHOOT_DAYS','ROLE_SCALE_BAND',
  'DUR90_OLD_BAND','DUR90_DAILY','NAT92_SPREAD','NAT92_PULL_MAX','NAT92_PULL_OPEN_MAX',
  'BR89_PATRON_OF_GIG','GIG_TRIGGER_AWARD_MAP229','RIVAL_CFG'];
const FNS = ['normalizeGigRecord',
  'bridge56NormalizeGig','leadStar59Of','boardNotePlayerOk','looksLikeEraId','humanizeEraId',
  'clamp','resolveRoleScale','shootBandFor','effectiveShootDays','effectiveShootWeekdays',
  'effectiveShootDeadlineDays','gigPayExact','gigTierCanon229',
  'dur90RoundPay','dur90CalibrateGig',
  'reqGap','canAudition','fameFloor','gateTrainHint','isGigWrapped','gigActiveShoot','isGigInProduction',
  'isGigConsumed','seasonRank','calendarSeason','dateObj','boardPriorityRank','boardSortCompare',
  'gigsForLocSeasonBoard','clampEntryReqToTemplate','mergeEntryGigsIntoPool','entryGigPool229','entryGigPoolLive',
  'ensureEntryTierBoardFill','countApplyableEntryOnBoard','needsEntryBoardFill','weekNumNow',
  'mergeWinterBridge88','gigSeasonEarlyVisible88','gigSeasonHidden88','gigReleaseLine88',
  'nat92Hash','nat92StaggerEligible','nat92DayIdxOf','nat92PostIntervals','nat92WindowStartDay',
  'nat92CalNeedDays','nat92BoardOffsetDays','gigBoardPosted92','nat92Gig','mergeNat92Gigs',
  'br89HasCredit','br89GigOn','awardTriggerOn229','rivalTriggerOpenable229','triggerGigOn',
  'rivalryScore','ensureRivalry'];
let WORLD_SRC;
try{
  WORLD_SRC = TF_SRC + '\n' + CONSTS.map(c=>extractConst(c).replace('const '+c, 'var '+c)).join('\n')
    + '\n' + FNS.map(f=>extractFn(f)).join('\n');
}catch(e){ console.log('FAIL extraction（v91 反證應在此觸發）: '+e.message); process.exit(1); }
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
  var mergeBr89Gigs = function(){ return 0; };
  var mergeYearGigs36 = function(){ return 0; };
`;
function buildWorld(){
  return new Function(STUBS_SRC + WORLD_SRC + `
  ; return { normalizeGigRecord, canAudition, gigsForLocSeasonBoard, calendarSeason, triggerGigOn,
    mergeEntryGigsIntoPool, mergeWinterBridge88, mergeNat92Gigs, gigBoardPosted92,
    nat92StaggerEligible, nat92PostIntervals, nat92BoardOffsetDays, nat92CalNeedDays,
    effectiveShootDays, gigPayExact, resolveRoleScale,
    setS:(s)=>{S=s;}, setGIGS:(g)=>{GIGS=g;}, getGIGS:()=>GIGS,
    DUR90_DAILY, ROLE_SCALE_BAND };`)();
}
const W = buildWorld();
function deepClone(o){ return JSON.parse(JSON.stringify(o)); }
const PACK_NEW = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gigs_new.json'), 'utf8'));
function loadPackPipeline(y){
  return (PACK_NEW.gigs || []).filter(g => g.year === y).map(g => W.normalizeGigRecord(deepClone(g)));
}
const FRESH = { acting:18, stage:14, vocal:14, looks:22, stamina:75, iq:20, charm:16, fame:5, popularity:3, stress:12, money:12000, dayIndex:0, flags:{}, shoots:[], booked:[], enrolled:{}, board:{}, known:{} };
const MAXED = { acting:999, stage:999, vocal:999, looks:999, charm:999, iq:999, stamina:999, fame:999, popularity:999, stress:0, money:999999, dayIndex:0, flags:{}, shoots:[], booked:[], enrolled:{}, board:{}, known:{}, wrapHistory:[] };
/* B5：MAXED 要真係 maxed——47 張 trigger 條件齊開，E2 普查先至量度庫分佈而唔係觸發狀態。
   credit／rel 由新庫 trigger 逐張抽（唔人手抄 id）；獎項級紀錄 4 典禮 × 3 年全部 won；
   主線全 done；對手線 4 分（傳聞＋N3＋報紙）。 */
{
  const _trig = (PACK_NEW.gigs || []).filter(g => g.trigger && g.trigger.kind);
  MAXED.mockCredits = [...new Set(_trig.filter(t => t.trigger.kind === 'credit').map(t => t.trigger.creditId))]
    .map(id => ({ id, debtor: 'x', title: 'x', line: 'x', status: '未收' }));
  MAXED.mockRumors = [{ id: 'gao_steal_spotlight', title: '高俊傑搶鏡' }];
  MAXED.newspaperClippings = [{ topicKey: 'rival:gao', eventKey: 'story:N3' }];
  MAXED.story = { done: {}, flags: { rival_gao_hard: true } };
  for (let n = 1; n <= 19; n++) MAXED.story.done['N' + n] = true;
  MAXED.story.done.N6F = true;
  MAXED.npcs = {};
  [...new Set(_trig.filter(t => t.trigger.kind === 'rel').map(t => t.trigger.npcId))].forEach(id => { MAXED.npcs[id] = 100; });
  const _cats = ['cat_film_lead_m','cat_film_lead_f','cat_film_support_m','cat_tv_lead_m','cat_tv_lead_f','cat_tv_support_m','cat_music_newcomer','cat_ad_lead_m','cat_ad_lead_f','cat_ad_support_m'];
  MAXED.awardsResults = {};
  for (const y of [1990, 1991, 1992]) for (const c of ['award_harbour_ad','award_golddisc_music','award_harbour_film','award_singho_tv']) {
    const cats = {}; _cats.forEach(k => { cats[k] = 'won'; });
    MAXED.awardsResults[y + '/' + c] = { year: y, won: true, nominated: true, cats };
  }
}
const LOCS = ['cafe_cha','rec_hk','tvb_longmen','film_lion','film_cotton','film_harbour','tvb_harbour','tvb_kowloon','ad_central','ad_adm','rec_wanchai','rec_star','agency_ho'];
const GIG_LOCS = LOCS.filter(l=>l!=='cafe_cha' && l!=='agency_ho');
const YEAR_START = { 1990:0, 1991:365, 1992:730 };
function setupYearPool(year){
  W.setGIGS(loadPackPipeline(year));
  const st = deepClone(MAXED); st.dayIndex = YEAR_START[year];
  W.setS(st);
  if(year===1990){ W.mergeEntryGigsIntoPool(); W.mergeWinterBridge88(); }
  W.gigsForLocSeasonBoard(GIG_LOCS[0], W.calendarSeason());
  return W.getGIGS();
}

/* ---------- (F) 注入池已刪＋錯峰資格 ---------- */
ok('F1 mergeNat92Gigs 回 0（注入池已刪，錯峰機制留返）', W.mergeNat92Gigs() === 0);
ok('F1b NAT92_GIGS 池已清空（const NAT92_GIGS = [];，機制佔位留返）', html.indexOf('const NAT92_GIGS = [];') >= 0);
const CANON = { acting:1, stage:1, vocal:1, looks:1, charm:1, iq:1, stamina:1 };
const poolByYear = {};
for(const y of [1990, 1991, 1992]) poolByYear[y] = setupYearPool(y);
let stagN = 0, entryN = 0, nat92FlagN = 0, reqBad = [];
for(const y of [1990, 1991, 1992]) for(const g of poolByYear[y]){
  if(g.nat92) nat92FlagN++;
  if(g.entryTier) entryN++;
  if(W.nat92StaggerEligible(g)) stagN++;
  if(Object.keys(g.req||{}).some(k=>!CANON[k])) reqBad.push(g.id);
}
ok('F2 錯峰合資格 229 張（241－12 入門）', stagN === 229, 'stagN=' + stagN);
ok('F2b 入門 12 張唔錯峰', entryN === 12);
ok('F3 舊 nat92 旗全庫 0 命中', nat92FlagN === 0);
ok('F3b 新庫 req 只含七真屬性鍵', reqBad.length === 0, reqBad.slice(0,3).join(','));

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
  let openBad = 0, stagN2 = 0;
  for(const y of [1990, 1991, 1992]){
    for(const g of poolByYear[y]){
      if(!W.nat92StaggerEligible(g)) continue;
      stagN2++;
      const yStart = Math.round((new Date(g.year, 0, 1) - new Date(1990, 0, 1)) / 86400000);
      for(const iv of W.nat92PostIntervals(g)) if(iv.from <= yStart && iv.off !== 0) openBad++;
    }
  }
  ok('B2 年初已開窗 interval 偏移恆 0（違規 '+openBad+'／錯峰 gig '+stagN2+' 張）', openBad === 0 && stagN2 > 200);
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
  ok('N1 逐張逐 interval：偏移+拉前+工期日曆日 ≤ interval 長度（違規 '+(bad.slice(0,3).join(',')||'無')+'）', bad.length === 0);
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
  ok('D2 第一週逐日有通告地點 ≥1 可接，例外只得九龍電視台（實數：'+(badLoc.join(',')||'無')+'）',
    badLoc.length === 1 && badLoc[0] === 'tvb_kowloon');
  // D2 註：tvb_kowloon 1990 冬窗得兩張（tv_104 acting 30、tv_111 acting 68），開局演技 18 接唔到；
  // 入口池 12 張冇一張喺呢個地點過冬——新庫分佈缺口，留待通告庫覆蓋校準票處理，B3 唔補新通告。
  ok('D3 紅棉影業 day-0 有可接（新庫供應）', perLocDay[0]['film_cotton'] >= 1);
  ok('D4 灣仔唱片 day-0 有可接（新庫供應）', perLocDay[0]['rec_wanchai'] >= 1);
}

/* ---------- (E) 分布守衛 ---------- */
{
  /* E0 普查前提：MAXED 開齊 47 張 trigger（唔齊就 E2 釘量度緊觸發狀態，唔係庫分佈）。 */
  const _allTrig = (PACK_NEW.gigs || []).filter(g => g.trigger && g.trigger.kind);
  const _unopened = _allTrig.filter(g => { const st = deepClone(MAXED); W.setS(st); return !W.triggerGigOn(g); }).map(g => g.id);
  ok('E0 MAXED 開齊 47 張 trigger（普查前提；B5）', _allTrig.length === 47 && _unopened.length === 0, '未開：' + _unopened.join(','));
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
  // E2 註：新庫地點-季節洞——1990：film_harbour 春／夏 0 張、ad_adm 夏 0、rec_wanchai 夏 0、
  // tvb_harbour 秋 0、rec_star 秋 0；1991：rec_wanchai 冬／夏 0、film_lion 夏 0、tvb_harbour 春 0；
  // 1992：ad_adm 冬／夏 0、ad_central 春 0、film_cotton 秋 0、film_lion 春 0、rec_hk 冬 0、
  // rec_wanchai 春 0、tvb_harbour 春 0。呢啲洞令錯峰保底都填唔到（嗰季嗰地點根本冇通告）。
  ok('E2 三年全板 0 地點-週＝94（1990:38／1991:18／1992:38，新庫分佈釘）',
    c90.zero === 38 && c91.zero === 18 && c92.zero === 38, '實數 ' + c90.zero + '/' + c91.zero + '/' + c92.zero);
  ok('E3 1991/1992「恰好 2」占比 <40%（實數 '+c91.pct.toFixed(1)+'%／'+c92.pct.toFixed(1)+'%）', c91.pct < 40 && c92.pct < 40);
}

console.log(fails.length ? ('FAILURES: '+fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
