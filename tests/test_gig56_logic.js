// v20a56 散工修復邏輯測試：明碼標籤／冷卻／變體輪換／拆同名複本／保底閥／舊檔相容。
// 行真路徑：真 mergeSoftBridgeGigs、真 renewSoftBridgeGigs（冷卻制）、真 normalizeGigRecord
// （連真 TEXTFIX55 清洗層＋真 bridge56NormalizeGig）、真 gigsForLocSeasonBoard、真 gigCardHtml。
// 反證：對 v20a55 index 行 → BRIDGE56_* 唔存在，抽取即 FAIL。
// 用法：node tests/test_gig56_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) throw new Error('fn not found: '+name);
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){
    if(html[j]==='{') depth++;
    else if(html[j]==='}'){ depth--; if(depth===0) break; }
  }
  return html.slice(i, j+1);
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
function dayIndexOf(y, m, d){ return Math.round((Date.UTC(y, m-1, d) - Date.UTC(1988, 2, 7)) / 86400000); }
function loadPack(y){
  return JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'gigs_'+y+'.json'), 'utf8'));
}
/* TEXTFIX55 清洗層（normalizeGigRecord 會呼叫） */
const tfA = html.indexOf('/* ==== v20a55 TEXTFIX');
const tfB = html.indexOf('async function refreshCopyPacksFromDisk(){');
if(tfA<0 || tfB<0 || tfB<=tfA){ console.log('FAIL TEXTFIX55 block not found'); process.exit(1); }
const TF_SRC = html.slice(tfA, tfB);

const CONSTS = ['SOFT_BRIDGE_GIGS_1988','BRIDGE56_VARIANTS','BRIDGE56_CROSSYEAR_RENAME','BRIDGE56_COOLDOWN_WEEKS'];
const FNS = ['softBridgeGig','mergeSoftBridgeGigs','renewSoftBridgeGigs','bridge56StarvationValve','bridge56NormalizeGig',
  'takeSoftBridgePay','weekNumNow','isGigWrapped','gigActiveShoot','isGigInProduction','isGigConsumed',
  'boardNotePlayerOk','looksLikeEraId','humanizeEraId','normalizeGigRecord',
  'seasonRank','boardPriorityRank','boardSortCompare','calendarSeason','dateObj','gigsForLocSeasonBoard','gigCardHtml',
  'stripEraIdsInText','eraTagDisplay'];
let WORLD_SRC;
try{
  WORLD_SRC = TF_SRC + '\n' + CONSTS.map(c=>extractConst(c).replace('const '+c, 'var '+c)).join('\n')
    + '\n' + FNS.map(f=>extractFn(f)).join('\n');
}catch(e){ console.log('FAIL extraction: '+e.message); process.exit(1); }
const STUBS_SRC = `
  var START = { y:1988, m:3, d:7 };
  var softPreviewOn = function(){ return true; };
  var mergeIntelGigs = function(){ return 0; };
  var mergeFavorGigs = function(){ return 0; };
  var mergeRivalGigs = function(){ return 0; };
  var mergeExodusGigs = function(){ return 0; };
  var mergeMidGigs35 = function(){ return 0; };
  var mergeYearGigs36 = function(){ return 0; };
  var canAudition = function(){ return { ok:true }; };
  var chance = function(){ return 0.8; };
  var reqHtml = function(){ return ''; };
  var gigPayExactText = function(){ return ''; };
  var gigScheduleVerb = function(){ return '拍攝'; };
  var effectiveShootDays = function(g){ return g.shootDaysHint || 1; };
  var effectiveShootWeekdays = function(){ return [1,2,3,4,5,6,7]; };
  var shootWeekdayLabel = function(){ return ''; };
  var gigApplyDeadlineText = function(){ return ''; };
  var effectiveShootDeadlineDays = function(){ return 14; };
  var gigTierKey = function(){ return 'extra'; };
  var seasonTipHtml = function(){ return ''; };
  var intelLineForGig = function(){ return ''; };
  var gigGapBoardLine37 = function(){ return ''; };
  var gigGapLine34 = function(){ return ''; };
`;
function baseState(dayIndex){
  return { dayIndex: dayIndex, acting:30, iq:20, stamina:120, looks:26, charm:22,
    stage:25, vocal:20, fame:10, popularity:5, stress:0, money:20000, industryCreditDelta:0,
    flags:{}, shoots:[], booked:[], board:{}, known:{}, npcs:{director:0,agent:0,colleague:0},
    enrolled:{}, mockDebts:[], mockRumors:[], castingTags:[] };
}
function setupSrc(dayIndex, doMerge){
  return 'eval(WORLD_SRC); eval(STUBS_SRC); var S = baseState('+dayIndex+'); var GIGS = [];'
    + (doMerge===false ? '' : ' mergeSoftBridgeGigs();');
}

/* ============ 段一：冷卻——完成後 2 週唔上板，期滿返板兼換變體 ============ */
(function(){
  eval(setupSrc(dayIndexOf(1988,7,4))); // 夏，week 18
  const id = 'gig_1988_soft_bridge_summer_ad';
  const wk0 = Math.floor(S.dayIndex/7)+1;
  let board = gigsForLocSeasonBoard('ad_central', '夏').filter(g=>g.id===id);
  ok('cool: 未完成前在板', board.length===1 && board[0].title==='《暑期街招》廣告路人');
  S.flags['done_'+id] = 1;
  renewSoftBridgeGigs();
  ok('cool: 首次結算唔刪旗（起冷卻）', !!S.flags['done_'+id]);
  ok('cool: bcool 設為 +2 週', Number(S.flags['bcool_'+id])===wk0+2);
  board = gigsForLocSeasonBoard('ad_central', '夏').filter(g=>g.id===id);
  ok('cool: 冷卻中唔上板', board.length===0);
  S.dayIndex += 7; renewSoftBridgeGigs();
  ok('cool: +1 週仍冷卻', !!S.flags['done_'+id]);
  board = gigsForLocSeasonBoard('ad_central', '夏').filter(g=>g.id===id);
  ok('cool: +1 週仍唔上板', board.length===0);
  S.dayIndex += 7; renewSoftBridgeGigs();
  ok('cool: +2 週刪旗返板', !S.flags['done_'+id] && !S.flags['bcool_'+id]);
  ok('cool: bvar 遞增到 1', Number(S.flags['bvar_'+id])===1);
  mergeSoftBridgeGigs();
  const g1 = GIGS.find(g=>g.id===id);
  ok('cool: 返板換變體一', g1.title==='《夏日涼茶招》廣告路人' && g1.workTitle==='夏日涼茶招');
  board = gigsForLocSeasonBoard('ad_central', '夏').filter(g=>g.id===id);
  ok('cool: 返板在板且係變體名', board.length===1 && board[0].title==='《夏日涼茶招》廣告路人');
  /* 第二輪：再完成 → 變體二；第三輪 → 繞回變體一 */
  S.flags['done_'+id] = 1; renewSoftBridgeGigs();
  S.dayIndex += 14; renewSoftBridgeGigs();
  mergeSoftBridgeGigs();
  const g2 = GIGS.find(g=>g.id===id);
  ok('cool: 第二輪換變體二', g2.title==='《暑期汽水招》廣告路人');
  S.flags['done_'+id] = 1; renewSoftBridgeGigs();
  S.dayIndex += 14; renewSoftBridgeGigs();
  mergeSoftBridgeGigs();
  const g3 = GIGS.find(g=>g.id===id);
  ok('cool: 第三輪繞回變體一', g3.title==='《夏日涼茶招》廣告路人');
})();

/* ============ 段二：甩期（fail）同行冷卻；經濟冇郁 ============ */
(function(){
  eval(setupSrc(dayIndexOf(1988,7,4)));
  const id = 'gig_1988_soft_bridge_summer_crew';
  S.flags['done_'+id] = 1; S.flags['fail_shoot_'+id] = 1;
  renewSoftBridgeGigs();
  ok('fail: 甩期都起冷卻唔即返', !!S.flags['done_'+id] && Number(S.flags['bcool_'+id])>0);
  S.dayIndex += 14; renewSoftBridgeGigs();
  ok('fail: 期滿 done+fail 一齊清', !S.flags['done_'+id] && !S.flags['fail_shoot_'+id]);
  S.flags.softBridgeFullWeek = 0;
  const full = takeSoftBridgePay(3600);
  const stip = takeSoftBridgePay(3600);
  ok('econ: 首單正薪冇改', full.pay===3600 && full.stipend===false);
  ok('econ: 補場 $800 冇改', stip.pay===800 && stip.stipend===true);
})();

/* ============ 段三：同季同名複本拆清（同週唔會兩地點同標題） ============ */
(function(){
  eval(setupSrc(dayIndexOf(1988,7,4)));
  ['夏','秋'].forEach(season=>{
    const gs = GIGS.filter(g=>g.softBridge && g.season===season);
    const titles = gs.map(g=>g.title), wts = gs.map(g=>g.workTitle);
    ok('dup: '+season+'季 6 張 bridge', gs.length===6);
    ok('dup: '+season+'季標題全互異', new Set(titles).size===titles.length);
    ok('dup: '+season+'季 workTitle 全互異', new Set(wts).size===wts.length);
  });
  const kln = GIGS.find(g=>g.id==='gig_1988_soft_bridge_summer_kln');
  const hbr = GIGS.find(g=>g.id==='gig_1988_soft_bridge_summer_crew');
  ok('dup: 跟組只剩海旁一張原名', hbr.title==='《暑期跟組》場務助手' && kln.title==='《暑期棚景組》場務助手');
})();

/* ============ 段四：明碼標籤（卡面） ============ */
(function(){
  eval(setupSrc(dayIndexOf(1988,7,4)));
  const g = GIGS.find(x=>x.id==='gig_1988_soft_bridge_summer_ad');
  const cardHtml = gigCardHtml(g, {});
  ok('label: bridge 卡有常駐散工標籤', cardHtml.indexOf('bridge-tag')>=0 && cardHtml.indexOf('常駐散工')>=0);
  ok('label: bridge 卡有每週有工開說明', cardHtml.indexOf('每週有工開')>=0);
  const plain = gigCardHtml({ id:'x1', title:'《某劇》配角', type:'電視劇', tier:'中', loc:'tvb_kowloon', req:{}, pay:[1000,2000], blurb:'', synopsis:'', roleHint:'' }, {});
  ok('label: 非 bridge 卡冇標籤', plain.indexOf('bridge-tag')<0 && plain.indexOf('常駐散工')<0);
})();

/* ============ 段五：跨年同名改名（1990 副本） ============ */
(function(){
  eval(setupSrc(dayIndexOf(1990,4,15), false));
  const p90 = loadPack(1990), p89 = loadPack(1989);
  const get = (pack,id)=> pack.gigs.find(g=>g.id===id);
  const cases = [
    ['gig_1990_film_13','《霧港夜航》過場：碼頭腳夫'],
    ['gig_1990_rec_06','春日合唱單曲《起錨》和音'],
    ['gig_1990_rec_07','夏日專輯《涼風》和音錄音'],
    ['gig_1990_rec_08','灣仔錄音室：夏日口白試音'],
    ['gig_1990_rec_10','灣仔錄音室：年終合唱收聲'],
    ['gig_1990_rec_11','賀歲歌合唱：灣仔錄音室']
  ];
  cases.forEach(([id, want])=>{
    const rec = normalizeGigRecord(JSON.parse(JSON.stringify(get(p90,id))));
    ok('xYear: '+id+' 改名', rec.title===want);
  });
  const orig = normalizeGigRecord(JSON.parse(JSON.stringify(get(p89,'gig_1989_film_11'))));
  ok('xYear: 1989 原作唔郁', orig.title==='《海港春潮》過場：碼頭腳夫');
  const t90 = new Set(p90.gigs.map(g=>normalizeGigRecord(JSON.parse(JSON.stringify(g))).title));
  const clash = p89.gigs.map(g=>normalizeGigRecord(JSON.parse(JSON.stringify(g))).title).filter(t=>t90.has(t));
  ok('xYear: 89/90 兩包再冇同標題', clash.length===0);
})();

/* ============ 段六：保底閥＋舊檔相容 ============ */
(function(){
  eval(setupSrc(dayIndexOf(1988,7,4)));
  const summer = GIGS.filter(g=>g.softBridge && g.season==='夏');
  summer.forEach(g=>{ S.flags['done_'+g.id]=1; });
  renewSoftBridgeGigs(); // 全部起冷卻
  ok('valve: 其餘 5 張仍在冷卻', summer.filter(g=>!!S.flags['done_'+g.id]).length===5);
  const freed = summer.filter(g=>!S.flags['done_'+g.id]);
  ok('valve: 保底放返恰好一張', freed.length===1);
  ok('valve: 放返嗰張 bvar+1', Number(S.flags['bvar_'+freed[0].id])===1);
  /* 舊檔：旗標全缺 → renew 唔出錯、唔亂起冷卻 */
  /* 舊檔：旗標全缺 → renew 唔出錯、唔亂起冷卻（另開作用域重行 setup） */
  (function(){
    eval(setupSrc(dayIndexOf(1988,7,4)));
    let threw = false;
    try{ renewSoftBridgeGigs(); }catch(e){ threw = true; }
    ok('compat: 舊檔冇新欄位唔出錯', !threw);
    ok('compat: 未完成過唔起冷卻', !Object.keys(S.flags).some(k=>k.indexOf('bcool_')===0));
  })();
  /* 拍攝中嘅卡唔俾 renew 掂 */
  (function(){
    eval(setupSrc(dayIndexOf(1988,7,4)));
    const gid = 'gig_1988_soft_bridge_summer_star';
    S.flags['done_'+gid] = 1;
    S.shoots.push({ id:'sh1', gigId:gid, title:'x', totalDays:1, doneDays:0 });
    renewSoftBridgeGigs();
    ok('compat: 拍攝中唔起冷卻', !S.flags['bcool_'+gid] && !!S.flags['done_'+gid]);
  })();
})();

if(fails.length){ console.log('FAILURES:', fails.join(' | ')); process.exit(1); }
console.log('ALL PASS');
