// v20a110 OVR110：通告級別 vs 要求對齊・邏輯測試
// 合約（audit110.md；內容優先定級）：
//   A OVR110 對照表在位：TIER110 96 個 id、REQ110 246 個 id、ovr110Apply 函數；
//     normalizeGigRecord 喺 NAME93 呼叫之後呼叫 ovr110Apply（唔係池後加工）
//   B 覆蓋：改動表全部 id 都喺全池（去重 469 張）存在；觸及去重 273 張
//     （審計 §1 寫 281 係筆誤：96+246−重疊 69＝273，見 NOTES 殘留）
//   C 一致性（審計覆核標準，classify 移植自 audit110.py）：全池 469 張 A／B／C 全清零；
//     每級中位最高要求落帶（1990 初 20／中 70／高 130；1991 18／65／147.5；1992 18／66.5／172.5）
//   D 開局 day-0 全板可接 20（底線 ≥12；唔寫死上限——+6 全部係入門初工，見 audit §8.1）
//   E 第 2 週 rec_hk 板：零訓練 2／8、歌藝 1 堂後 3／8、再加台風 1 堂後 4／8
//   F 注入家族改動唔會被 board 重跑洗走（gigsForLocSeasonBoard 重跑兩次後覆核）
//   G 升 tier 27 張全部新 tier 正確、唔再喺臨記板（初級段）出現
//   H 冪等：觸及通告兩次 normalize 結果一致
//   I 錨點：和音家族四張新要求；《櫥窗》過場模特升中但「臨」印問題屬 press94 內容分類，
//     本測試只斷言 tier，不斷言見報分類（見 audit §5.3 更正）
// 反證：pristine main（v109）冇 TIER110／REQ110／ovr110Apply → A1–A4 FAIL，
//   且 C1 會報出 251 張脫節（A 155／B 96），D1 報 14 而唔係 20。
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) return null;
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){ if(html[j]==='{') depth++; else if(html[j]==='}'){ depth--; if(depth===0) break; } }
  return html.slice(i, j+1);
}
function extractConst(name){
  for(const kw of ['const ', 'var ']){
    const i = html.indexOf(kw+name+' =');
    if(i<0) continue;
    let depth=0, started=false;
    for(let k=i; k<html.length; k++){
      const ch = html[k];
      if(ch==='{'||ch==='['){ depth++; started = true; }
      else if(ch==='}'||ch===']'){ depth--; if(started && depth===0) return html.slice(i, k+1)+';'; }
      else if(ch===';' && !started) return html.slice(i, k+1);
    }
  }
  return null;
}
let fails = 0;
function ok(name, cond, extra){
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : ''));
  if(!cond) fails++;
}
const tfA = html.indexOf('/* ==== v20a55 TEXTFIX');
const tfB = html.indexOf('async function refreshCopyPacksFromDisk(){');
if(tfA<0 || tfB<=tfA){ console.log('FAIL TEXTFIX55 block not found'); process.exit(1); }
const TF_SRC = html.slice(tfA, tfB);
const CONSTS = ['STAT_LABEL','LEADSTAR59','POSTER59_STAR_IDS','POSTER85_IDS','ENTRY_GIGS_1988',
  'GIG_REQ_KEYS88','WINTER_ENTRY_GIGS_88','GIG_SEASON_SPAN88','GIG_SEASON_LEAD88',
  'SHOOT_DAYS','ROLE_SCALE_BAND','MID_GIGS_1988_35','SOFT_BRIDGE_GIGS_1988',
  'DUR90_OLD_BAND','DUR90_DAILY','NAT92_SPREAD','NAT92_PULL_MAX','NAT92_PULL_OPEN_MAX',
  'NAME93_FIX','CLEAN100_GIG_RELEASE','BRIDGE56_CROSSYEAR_RENAME','BRIDGE56_VARIANTS',
  'INTEL_HIDDEN_GIGS','FAVOR_DUE_GIGS','RIVAL_FACEOFF_GIGS','EXODUS_GIGS',
  'WF3_LIAO_GIG','WF3_LIAO_HARVEST_GIG','BR89_GIGS','GIGS36_1989_SPRING_F5',
  'GIGS36_1989_BRIDGE','GIGS36_1989_HIGH_F2','GIGS36_1989_MID_F3',
  'GIGS36_1990_AUTUMN_F6','GIGS36_1990_BRIDGE','GIGS36_1990_FINALE_F7',
  'GIGS36_1990_HIGH_F2','GIGS36_1990_MID_F3','GIGS36_BY_YEAR','GIGS36_ALL_IDS',
  'NAT92_GIGS','NAT92_ALL_IDS','WINTER_BRIDGE_GIGS_88','TIER110','REQ110'];
const FNS = ['years66ShiftYear','years66ShiftText','years66Walk','years66GigRemap','normalizeGigRecord',
  'bridge56NormalizeGig','leadStar59Apply','leadStar59Of','boardNotePlayerOk','looksLikeEraId','humanizeEraId',
  'clamp','resolveRoleScale','shootBandFor','effectiveShootDays','effectiveShootWeekdays',
  'effectiveShootDeadlineDays','gigPayExact','winterBridge88Gig','softBridgeGig','gig36',
  'dur90RoundPay','dur90CalibrateGig','name93ApplyGig','ovr110Apply',
  'reqGap','canAudition','fameFloor','gateTrainHint','isGigWrapped','gigActiveShoot','isGigInProduction',
  'isGigConsumed','seasonRank','calendarSeason','dateObj','boardPriorityRank','boardSortCompare',
  'gigsForLocSeasonBoard','clampEntryReqToTemplate','mergeEntryGigsIntoPool','entryGigPoolLive',
  'ensureEntryTierBoardFill','countApplyableEntryOnBoard','needsEntryBoardFill','weekNumNow',
  'mergeWinterBridge88','mergeMidGigs35','mergeYearGigs36','mergeSoftBridgeGigs',
  'mergeIntelGigs','mergeFavorGigs','mergeRivalGigs','mergeExodusGigs','mergeWf3Gigs','mergeBr89Gigs',
  'gigSeasonEarlyVisible88','gigSeasonHidden88','gigReleaseLine88','poster85File',
  'nat92Hash','nat92StaggerEligible','nat92DayIdxOf','nat92PostIntervals','nat92WindowStartDay',
  'nat92CalNeedDays','nat92BoardOffsetDays','gigBoardPosted92','nat92Gig','mergeNat92Gigs'];
const STUBS_SRC = `
  var START = { y:1990, m:1, d:1 };
  var S = null;
  var GIGS = [];
  var COURSE_DEFS = {};
  var softPreviewOn = function(){ return false; };
`;
const WORLD_SRC = TF_SRC + '\n' + CONSTS.map(c=>{
  const s = extractConst(c); return s ? s.replace('const '+c, 'var '+c) : 'var '+c+' = undefined;';
}).join('\n') + '\n' + FNS.map(f=>extractFn(f) || '').join('\n');
const W = new Function(STUBS_SRC + WORLD_SRC + `
; return { years66Walk, normalizeGigRecord, canAudition, gigsForLocSeasonBoard, calendarSeason,
  mergeEntryGigsIntoPool, mergeWinterBridge88, mergeNat92Gigs, mergeMidGigs35, mergeYearGigs36,
  mergeSoftBridgeGigs, mergeIntelGigs, mergeFavorGigs, mergeRivalGigs, mergeExodusGigs, mergeWf3Gigs, mergeBr89Gigs,
  TIER110: (typeof TIER110 !== 'undefined') ? TIER110 : null,
  REQ110: (typeof REQ110 !== 'undefined') ? REQ110 : null,
  ovr110Apply: (typeof ovr110Apply === 'function') ? ovr110Apply : null,
  setS:(s)=>{S=s;}, setGIGS:(g)=>{GIGS=g;}, getGIGS:()=>GIGS,
  ENTRY_GIGS_1988, WINTER_ENTRY_GIGS_88, WINTER_BRIDGE_GIGS_88, MID_GIGS_1988_35,
  SOFT_BRIDGE_GIGS_1988, INTEL_HIDDEN_GIGS, FAVOR_DUE_GIGS, RIVAL_FACEOFF_GIGS, EXODUS_GIGS,
  WF3_LIAO_GIG, WF3_LIAO_HARVEST_GIG, BR89_GIGS, NAT92_GIGS, GIGS36_BY_YEAR };`)();
function deepClone(o){ return JSON.parse(JSON.stringify(o)); }

/* A 對照表＋接線 */
ok('A1 TIER110 在位', !!W.TIER110);
ok('A2 REQ110 在位', !!W.REQ110);
ok('A3 ovr110Apply 在位', typeof W.ovr110Apply === 'function');
ok('A4 TIER110 96 個 id', W.TIER110 && Object.keys(W.TIER110).length === 96,
   W.TIER110 && ('n=' + Object.keys(W.TIER110).length));
ok('A5 REQ110 246 個 id', W.REQ110 && Object.keys(W.REQ110).length === 246,
   W.REQ110 && ('n=' + Object.keys(W.REQ110).length));
const normSrc = extractFn('normalizeGigRecord') || '';
const i93 = normSrc.indexOf('try{ name93ApplyGig(o); }catch(_n93){}');
const i110 = normSrc.indexOf('try{ ovr110Apply(o); }catch(_o110){}');
ok('A6 normalize 呼叫 ovr110Apply', i110 >= 0);
ok('A7 接線排 NAME93 之後', i93 >= 0 && i110 > i93);
ok('A8 TIER110 值只係 初／中／高',
   W.TIER110 && Object.values(W.TIER110).every(v=>['初','中','高'].includes(v)));
ok('A9 REQ110 值只含七屬性鍵',
   W.REQ110 && Object.values(W.REQ110).every(r=>r && typeof r === 'object' &&
     Object.keys(r).every(k=>['acting','stage','vocal','looks','charm','iq','stamina'].includes(k)) &&
     Object.values(r).every(v=>v === null || (typeof v === 'number' && v >= 0))));

/* 全池（audit110 口徑：5 年 pack＋全部注入家族＋GIGS36，去重） */
const pool = new Map();
function addPool(g){ if(g && g.id && !pool.has(g.id)) pool.set(g.id, g); }
for(const y of [1988, 1989, 1990, 1991, 1992]){
  const pack = deepClone(JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gigs_'+y+'.json'), 'utf8')));
  W.years66Walk(pack, null);
  for(const raw of (pack.gigs || [])) addPool(W.normalizeGigRecord(raw));
}
const inj = [
  ...(W.ENTRY_GIGS_1988 || []), ...(W.WINTER_ENTRY_GIGS_88 || []), ...(W.WINTER_BRIDGE_GIGS_88 || []),
  ...(W.MID_GIGS_1988_35 || []), ...(W.SOFT_BRIDGE_GIGS_1988 || []), ...(W.INTEL_HIDDEN_GIGS || []),
  ...(W.FAVOR_DUE_GIGS || []), ...(W.RIVAL_FACEOFF_GIGS || []), ...(W.EXODUS_GIGS || []),
  W.WF3_LIAO_GIG, W.WF3_LIAO_HARVEST_GIG, ...(W.BR89_GIGS || []), ...(W.NAT92_GIGS || []),
];
for(const g of inj){ if(g && g.id) addPool(W.normalizeGigRecord(deepClone(g))); }
for(const y of Object.keys(W.GIGS36_BY_YEAR || {})){
  for(const g of (W.GIGS36_BY_YEAR[y] || [])){ if(g && g.id) addPool(W.normalizeGigRecord(deepClone(g))); }
}
ok('B0 全池去重 469 張', pool.size === 469, 'n=' + pool.size);
const TIER_IDS = Object.keys(W.TIER110 || {});
const REQ_IDS = Object.keys(W.REQ110 || {});
const touched = new Set([...TIER_IDS, ...REQ_IDS]);
ok('B1 TIER110 全部 id 喺全池存在', TIER_IDS.every(id=>pool.has(id)),
   TIER_IDS.filter(id=>!pool.has(id)).join(','));
ok('B2 REQ110 全部 id 喺全池存在', REQ_IDS.every(id=>pool.has(id)),
   REQ_IDS.filter(id=>!pool.has(id)).join(','));
ok('B3 觸及去重 273 張（96＋246−重疊 69）', touched.size === 273, 'n=' + touched.size);
const G = id => pool.get(id);

/* C 一致性：審計覆核標準（classify 移植自 audit110.py，逐字對齊） */
const START = { acting:18, stage:14, vocal:14, looks:22, charm:16, iq:20, stamina:75 };
const SCALED = ['acting','stage','vocal','looks','charm','iq'];
function scaleOf(cur, stamina){
  if(stamina) return 1.0;
  if(cur < 28) return 1.0;
  if(cur < 55) return 0.36;
  if(cur < 110) return 0.25;
  if(cur < 190) return 0.19;
  return 0.14;
}
function nom(i){ return i < 5 ? 5.0 : (i < 10 ? 7.0 : 9.5); }
function lessonsNeeded(start, target, stamina, cap){
  cap = cap || 400;
  if(target <= start) return 0;
  let cur = start, bank = 0, n = 0;
  while(cur < target && n < cap){
    bank += nom(n) * scaleOf(cur, stamina);
    const w = Math.floor(bank); cur += w; bank -= w; n++;
  }
  return cur >= target ? n : null;
}
function maxReq6(g){
  const r = g.req || {};
  return Math.max(0, ...SCALED.map(k=>r[k] || 0));
}
function burdenOf(g){
  let tot = 0; const per = {};
  for(const [k, v] of Object.entries(g.req || {})){
    const n = lessonsNeeded(START[k] || 0, v, k === 'stamina');
    per[k] = n; tot += (n === null ? 999 : n);
  }
  return [tot, per];
}
const BAND = { '初':[0,40], '中':[41,110], '高':[111,200] };
const STAM_BAND = { '初':110, '中':200, '高':400 };
const BURDEN_CAP = { '初':15, '中':60, '高':150 };
const SECOND_CAP = { '初':8, '中':25, '高':60 };
function classify(g){
  const tier = g.tier || '初';
  const [lo, hi] = BAND[tier];
  const mr = maxReq6(g);
  const [b, per] = burdenOf(g);
  const reasons = [];
  let cls = null;
  if(mr > hi){ cls = 'A'; reasons.push('最高要求 ' + mr + ' 超' + tier + '上限 ' + hi); }
  if(b > BURDEN_CAP[tier]){ if(!cls) cls = 'A'; reasons.push('總負擔 ' + b + ' 堂超' + tier + '上限 ' + BURDEN_CAP[tier] + ' 堂'); }
  const st = (g.req || {}).stamina;
  if(st != null && st > STAM_BAND[tier]){ if(!cls) cls = 'A'; reasons.push('體能 ' + st + ' 超' + tier + '體能軸上限 ' + STAM_BAND[tier]); }
  if(!cls && (tier === '中' || tier === '高') && mr < lo && SCALED.some(k=>k in (g.req || {}))){
    cls = 'B'; reasons.push('最高要求 ' + mr + ' 低過' + tier + '下限 ' + lo);
  }
  if(!cls){
    const costs = Object.values(per).sort((a,b)=>b-a);
    if(costs.length >= 2 && costs[1] > SECOND_CAP[tier]){
      cls = 'C'; reasons.push('副項獨自要 ' + costs[1] + ' 堂超' + tier + '副項預算 ' + SECOND_CAP[tier] + ' 堂');
    }
  }
  return [cls, mr, b, reasons];
}
const bad = [];
for(const g of pool.values()){
  const [cls, mr, b, why] = classify(g);
  if(cls) bad.push(g.id + ':' + cls + ':' + why.join(';'));
}
ok('C1 全池 469 張 A／B／C 全清零', bad.length === 0, bad.slice(0, 10).join(' | '));
/* 每級中位最高要求（live 年池，sim110 setupYearPool 口徑） */
function med(a){
  a = [...a].sort((x,y)=>x-y); const n = a.length;
  if(!n) return null;
  return n % 2 ? a[n>>1] : (a[(n>>1)-1] + a[n>>1]) / 2;
}
const YEAR_FILE = { 1990:1988, 1991:1989, 1992:1990 };
const YEAR_START = { 1990:0, 1991:365, 1992:730 };
const MAXED = { acting:999, stage:999, vocal:999, looks:999, charm:999, iq:999, stamina:999, fame:999, popularity:999, stress:0, money:999999, dayIndex:0, flags:{}, shoots:[], booked:[], enrolled:{}, board:{}, known:{}, wrapHistory:[] };
const GIG_LOCS = ['rec_hk','tvb_longmen','film_lion','film_cotton','film_harbour','tvb_harbour','tvb_kowloon','ad_central','ad_adm','rec_wanchai','rec_star'];
function setupYearPool(year){
  const pack = deepClone(JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gigs_'+YEAR_FILE[year]+'.json'), 'utf8')));
  W.years66Walk(pack, null);
  W.setGIGS((pack.gigs || []).map(g => W.normalizeGigRecord(g)));
  const st = deepClone(MAXED); st.dayIndex = YEAR_START[year];
  W.setS(st);
  if(year === 1990){ W.mergeEntryGigsIntoPool(); W.mergeWinterBridge88(); }
  W.gigsForLocSeasonBoard(GIG_LOCS[0], W.calendarSeason());
  return W.getGIGS();
}
const EXPECT_MED = { 1990:{ '初':20, '中':70, '高':130 }, 1991:{ '初':18, '中':65, '高':147.5 }, 1992:{ '初':18, '中':66.5, '高':172.5 } };
for(const year of [1990, 1991, 1992]){
  const yp = setupYearPool(year);
  for(const t of ['初','中','高']){
    const ms = yp.filter(g=>g.tier === t && g.req && Object.keys(g.req).length).map(maxReq6);
    ok('C2 ' + year + ' 年' + t + '級中位最高要求 ' + EXPECT_MED[year][t] + '（落帶）',
       ms.length > 0 && med(ms) === EXPECT_MED[year][t],
       'n=' + ms.length + ' med=' + med(ms) + ' range=' + (ms.length ? Math.min(...ms) + '–' + Math.max(...ms) : '—'));
  }
}

/* D 開局 day-0 全板可接（v92 §D 口徑，sim110 checkDay0） */
const FRESH = { acting:18, stage:14, vocal:14, looks:22, stamina:75, iq:20, charm:16, fame:5, popularity:3, stress:12, money:12000, dayIndex:0, flags:{}, shoots:[], booked:[], enrolled:{}, board:{}, known:{} };
const LOCS = ['cafe_cha','rec_hk','tvb_longmen','film_lion','film_cotton','film_harbour','tvb_harbour','tvb_kowloon','ad_central','ad_adm','rec_wanchai','rec_star','agency_ho'];
setupYearPool(1990);
let day0Apply = 0; const perLocDay0 = {};
{
  const st = deepClone(FRESH); st.dayIndex = 0; W.setS(st);
  for(const loc of LOCS){
    const shown = W.gigsForLocSeasonBoard(loc, W.calendarSeason());
    const ap = shown.filter(g=>W.canAudition(g).ok).length;
    perLocDay0[loc] = ap; day0Apply += ap;
  }
}
ok('D1 開局 day-0 全板可接 20', day0Apply === 20, 'n=' + day0Apply);
ok('D2 開局 day-0 可接守住底線 ≥12', day0Apply >= 12, 'n=' + day0Apply);
ok('D3 rec_hk／rec_star 開局各有 2／4 可接（和音入門工開到）',
   perLocDay0.rec_hk === 2 && perLocDay0.rec_star === 4, JSON.stringify(perLocDay0));

/* E 第 2 週 rec_hk 板（sim110 checkWeek2 梯子） */
setupYearPool(1990);
const USER_WK2 = { acting:18, stage:18, vocal:14, looks:22, stamina:75, iq:20, charm:16,
  fame:5, popularity:3, stress:12, money:12000, flags:{}, shoots:[], booked:[], enrolled:{}, board:{}, known:{} };
function wk2Board(bump){
  const st = deepClone(USER_WK2); Object.assign(st, bump || {}); st.dayIndex = 7; W.setS(st);
  const shown = W.gigsForLocSeasonBoard('rec_hk', W.calendarSeason());
  const ap = shown.filter(g=>W.canAudition(g).ok).map(g=>g.id);
  return { shown: shown.length, applyable: ap.length, ids: ap };
}
const e0 = wk2Board({});
ok('E1 第 2 週 rec_hk 零訓練 2／8', e0.applyable === 2 && e0.shown === 8,
   e0.applyable + '/' + e0.shown + ' (' + e0.ids.join(',') + ')');
ok('E2 零訓練可接含夜更和音 gig_1988_rec_01', e0.ids.includes('gig_1988_rec_01'), e0.ids.join(','));
const e1 = wk2Board({ vocal:19 });
ok('E3 第 2 週 rec_hk 歌藝 1 堂後 3／8（新春大合唱開到）', e1.applyable === 3 && e1.shown === 8,
   e1.applyable + '/' + e1.shown + ' (' + e1.ids.join(',') + ')');
ok('E4 歌藝 1 堂後可接含新春大合唱 gig_1988_rec_hk_winter', e1.ids.includes('gig_1988_rec_hk_winter'), e1.ids.join(','));
const e3 = wk2Board({ vocal:24, charm:21, stage:23 });
ok('E5 第 2 週 rec_hk 歌藝 2 堂＋魅力 1 堂＋台風 1 堂後 4／8（三張和音全開）',
   e3.applyable === 4 && e3.shown === 8, e3.applyable + '/' + e3.shown + ' (' + e3.ids.join(',') + ')');
ok('E6 4／8 嗰陣含賀年大碟和唱 gig_1988_nat92_rechk_win_album', e3.ids.includes('gig_1988_nat92_rechk_win_album'), e3.ids.join(','));

/* F 注入家族改動唔會被 board 重跑洗走（通用版：唔依賴個別注入 gig 喺邊季先合併；
   快照成個 1990 池觸及通告嘅 tier＋req，重跑兩次全板後再對） */
setupYearPool(1990);
function snapTouched(){
  const out = {};
  for(const g of W.getGIGS()){
    if(g && g.id && touched.has(g.id)) out[g.id] = { tier: g.tier, req: JSON.stringify(g.req || {}) };
  }
  return out;
}
const beforeF = snapTouched();
for(let round = 0; round < 2; round++){
  const st = deepClone(FRESH); st.dayIndex = round * 7; W.setS(st);
  for(const loc of LOCS) W.gigsForLocSeasonBoard(loc, W.calendarSeason());
}
const afterF = snapTouched();
const washBad = Object.keys(beforeF).filter(id=>{
  const a = beforeF[id], b = afterF[id];
  return !b || b.tier !== a.tier || b.req !== a.req;
});
ok('F1 板重跑兩次後，池內觸及通告 tier＋req 全部不變（注入家族唔會被洗走）',
   washBad.length === 0, washBad.slice(0, 10).join(',') + '（池內觸及 ' + Object.keys(beforeF).length + ' 張）');
ok('F2 NAT92 和唱喺池內，重跑後仍係 初／{vocal:20,stage:20}',
   beforeF['gig_1988_nat92_rechk_win_album'] && afterF['gig_1988_nat92_rechk_win_album'] &&
   afterF['gig_1988_nat92_rechk_win_album'].tier === '初' &&
   afterF['gig_1988_nat92_rechk_win_album'].req === JSON.stringify({ vocal:20, stage:20 }),
   afterF['gig_1988_nat92_rechk_win_album'] && (afterF['gig_1988_nat92_rechk_win_album'].tier + '/' + afterF['gig_1988_nat92_rechk_win_album'].req));
/* 反證位：池後加工會被洗走——直接改 GIGS 入面一張注入 gig 嘅 req 做舊值 360，
   再上板，merge* 會由 raw const 重新 normalize，原位取代返 OVR110 值。
   （audit §9 實測：冇 normalize 層嗰陣，池後改動第一次上板即刻洗返 {vocal:360,...}；
   有 OVR110 喺 normalize 層，洗返嘅就係新值 {vocal:20,stage:20}。） */
{
  const gs = W.getGIGS();
  const nat = gs.find(g=>g.id === 'gig_1988_nat92_rechk_win_album');
  if(nat){
    nat.req = { vocal: 360, stage: 350, charm: 290 };
    const st = deepClone(FRESH); st.dayIndex = 0; W.setS(st);
    W.gigsForLocSeasonBoard('rec_hk', W.calendarSeason());
    const back = W.getGIGS().find(g=>g.id === 'gig_1988_nat92_rechk_win_album');
    ok('F3 池後加工對照：改 req 做舊值 360 再上板，會被洗返 OVR110 新值 {vocal:20,stage:20}',
       back && JSON.stringify(back.req) === JSON.stringify({ vocal:20, stage:20 }),
       back && JSON.stringify(back.req));
  } else {
    ok('F3 池後加工對照：NAT92 和唱喺池內', false, 'not in pool');
  }
}

/* G 升 tier 27 張：新 tier 正確、唔再喺臨記板出現 */
const RAISED = {
  'g36_89_win_adm_clearance':'中','gig_1988_ad_02':'中','gig_1988_ad_adm_autumn_low':'中',
  'gig_1988_mtv_02':'中','gig_1988_photo_01':'中','gig_1988_rec_02':'中',
  'gig_1988_rec_hk_autumn':'高','gig_1988_rec_hk_spring_mid':'高','gig_1988_rec_hk_winter_mid':'高',
  'gig_1988_rec_star_summer':'高','gig_1988_tv_kowloon_winter':'中',
  'gig_1988_tvb_harbour_summer_low':'中','gig_1988_tvb_harbour_winter_low':'中',
  'gig_1988_tvb_longmen_summer_low':'中','gig_1988_var_01':'中','gig_1988_var_03':'中',
  'gig_1989_mtv_01':'中','gig_1989_rec_08':'中','gig_1990_film_01':'中','gig_1990_mtv_01':'中',
  'gig_1990_rec_03':'中','gig_1990_tv_04':'中','gig_1991_ad_03':'中','gig_1991_mtv_01':'中',
  'gig_1991_var_06':'中','gig_1992_mtv_01':'中','gig_wf3_liao_stage':'中',
};
ok('G0 升 tier 清單 27 張', Object.keys(RAISED).length === 27);
const raisedBad = Object.entries(RAISED).filter(([id, t])=>!G(id) || G(id).tier !== t);
ok('G1 27 張升 tier 全部新 tier 正確', raisedBad.length === 0,
   raisedBad.map(([id])=>id + ':' + (G(id) && G(id).tier)).join(','));
/* 板面掃描：三年 live 池 × 全部地點 × day 0–13，升 tier 通告唔可以 tier 初上板 */
const raisedOnEntryBoard = [];
for(const year of [1990, 1991, 1992]){
  setupYearPool(year);
  for(let d = 0; d < 14; d++){
    const st = deepClone(FRESH); st.dayIndex = YEAR_START[year] + d; W.setS(st);
    for(const loc of LOCS){
      for(const g of W.gigsForLocSeasonBoard(loc, W.calendarSeason())){
        if(RAISED[g.id] && g.tier === '初') raisedOnEntryBoard.push(year + '/d' + d + '/' + loc + '/' + g.id);
      }
    }
  }
}
ok('G2 升 tier 27 張唔再以初級上板（三年掃描）', raisedOnEntryBoard.length === 0,
   raisedOnEntryBoard.slice(0, 10).join(' | '));

/* H 冪等 */
const idemBad = [];
for(const id of touched){
  const g1 = G(id);
  if(!g1) continue;
  const g2 = W.normalizeGigRecord(deepClone(g1));
  if(g1.tier !== g2.tier || JSON.stringify(g1.req) !== JSON.stringify(g2.req)) idemBad.push(id);
}
ok('H1 觸及通告兩次 normalize tier＋req 一致', idemBad.length === 0, idemBad.join(','));

/* I 錨點：和音家族＋升 tier 例證 */
ok('I1 夜更和音 gig_1988_rec_01 要求 {vocal:10}',
   G('gig_1988_rec_01') && JSON.stringify(G('gig_1988_rec_01').req) === JSON.stringify({ vocal:10 }),
   G('gig_1988_rec_01') && JSON.stringify(G('gig_1988_rec_01').req));
ok('I2 鬼馬夜更和音 gig_1988_rec_star_spring 中→初／{vocal:10}',
   G('gig_1988_rec_star_spring') && G('gig_1988_rec_star_spring').tier === '初' &&
   JSON.stringify(G('gig_1988_rec_star_spring').req) === JSON.stringify({ vocal:10 }),
   G('gig_1988_rec_star_spring') && (G('gig_1988_rec_star_spring').tier + '/' + JSON.stringify(G('gig_1988_rec_star_spring').req)));
ok('I3 新春大合唱 gig_1988_rec_hk_winter 要求 {vocal:15,stage:15}',
   G('gig_1988_rec_hk_winter') && JSON.stringify(G('gig_1988_rec_hk_winter').req) === JSON.stringify({ vocal:15, stage:15 }),
   G('gig_1988_rec_hk_winter') && JSON.stringify(G('gig_1988_rec_hk_winter').req));
ok('I4 賀年大碟和唱 gig_1988_nat92_rechk_win_album 中→初／{vocal:20,stage:20}',
   G('gig_1988_nat92_rechk_win_album') && G('gig_1988_nat92_rechk_win_album').tier === '初' &&
   JSON.stringify(G('gig_1988_nat92_rechk_win_album').req) === JSON.stringify({ vocal:20, stage:20 }),
   G('gig_1988_nat92_rechk_win_album') && (G('gig_1988_nat92_rechk_win_album').tier + '/' + JSON.stringify(G('gig_1988_nat92_rechk_win_album').req)));
ok('I5 唱片主唱 gig_1988_rec_hk_spring_mid 中→高',
   G('gig_1988_rec_hk_spring_mid') && G('gig_1988_rec_hk_spring_mid').tier === '高',
   G('gig_1988_rec_hk_spring_mid') && G('gig_1988_rec_hk_spring_mid').tier);
ok('I6 《櫥窗》過場模特 gig_1990_film_01 初→中（tier 升；「臨」印屬 press94 內容分類，唔喺呢度斷言）',
   G('gig_1990_film_01') && G('gig_1990_film_01').tier === '中',
   G('gig_1990_film_01') && G('gig_1990_film_01').tier);

console.log(fails ? ('FAILURES: ' + fails) : 'ALL PASS');
process.exit(fails ? 1 : 0);
