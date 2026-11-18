// v20a286 LOAD286：讀檔後通告庫年份唔同步——讀入 1991／1992 年存檔後，GIGS 仍然係
// 1990 年庫（124 張，v291：111＋13），要翻一日先經 advanceDay 補返；期間開板見到舊年通告，當年
// 通告（包括決戰通告《霓虹夜影》）唔上板。
// 修法：contFromSlot 喺 syncDualTracks 之後、ensureEntryTierBoardFill 之前補
// syncGigsForCalendarYear(false)；maybeApplySoftSeed 喺 applySoftSeedState 之後補一次
// （種子改咗 S.dayIndex，presentSoftSeed 會直開地點／開板）。
// 斷言：A 組靜態——兩個 sync 呼叫喺正確位置＋順序＋guarded；B 組邏輯——抽出真
// syncGigsForCalendarYear＋dateObj＋normalizeGigRecord 跑：1991／1992 load 即刻
// 換成年庫、1990 load 係 no-op（唔重建、唔洗走入門通告）。
// 用法：node tests/test_r286_load_year_sync.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const gigsPath = path.join(__dirname, '..', 'content', 'gigs_new.json');
const gigData = JSON.parse(fs.readFileSync(gigsPath, 'utf8'));
const gigList = Array.isArray(gigData) ? gigData : gigData.gigs;
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
function extractBlock(start){
  let depth=0, j=start;
  for(; j<html.length; j++){
    if(html[j]==='{' || html[j]==='[') depth++;
    else if(html[j]==='}' || html[j]===']'){ depth--; if(depth===0) break; }
  }
  return html.slice(start, j+1);
}
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0){ console.log('FAIL 抽唔到 function '+name); process.exit(1); }
  const b = html.indexOf('{', i);
  return html.slice(i, b) + extractBlock(b);
}
function extractConst(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0){ console.log('FAIL 抽唔到 const '+name); process.exit(1); }
  const e = html.indexOf('=', i);
  let b = e+1;
  while(html[b]!=='{' && html[b]!=='[') b++;
  return 'var ' + name + ' = ' + extractBlock(b) + ';';
}

/* ---- A 組：靜態——load 路徑有 sync，順序啱 ---- */
const contSrc = extractFn('contFromSlot');
const seedSrc = extractFn('maybeApplySoftSeed');
const GUARD = 'try{ if(typeof syncGigsForCalendarYear==="function") syncGigsForCalendarYear(false); }catch(_e){}';
ok('A1 contFromSlot 有 guarded syncGigsForCalendarYear(false)',
  contSrc.indexOf(GUARD) >= 0);
ok('A2 contFromSlot：sync 喺 syncDualTracks(S) 之後',
  contSrc.indexOf('syncDualTracks(S)') >= 0 &&
  contSrc.indexOf('syncDualTracks(S)') < contSrc.indexOf('syncGigsForCalendarYear'));
ok('A3 contFromSlot：sync 喺 ensureEntryTierBoardFill() 之前（唔洗走入門通告）',
  contSrc.indexOf('syncGigsForCalendarYear') < contSrc.indexOf('ensureEntryTierBoardFill()'));
ok('A4 maybeApplySoftSeed：sync 喺 applySoftSeedState(seed) 之後',
  seedSrc.indexOf('applySoftSeedState(seed)') >= 0 &&
  seedSrc.indexOf('applySoftSeedState(seed)') < seedSrc.indexOf('syncGigsForCalendarYear'));
ok('A5 maybeApplySoftSeed：sync 喺 presentSoftSeed(res) 之前',
  seedSrc.indexOf('syncGigsForCalendarYear') >= 0 &&
  seedSrc.indexOf('syncGigsForCalendarYear') < seedSrc.indexOf('presentSoftSeed(res)'));

/* ---- B 組：邏輯——真 sync 函數 ---- */
eval(extractConst('START'));
eval(extractFn('dateObj'));
eval(extractFn('normalizeGigRecord'));
eval(extractFn('syncGigsForCalendarYear'));
global.window = {};
var S = null;
var GIGS = [];
var STORY_WIRE = null;
var mergeEntryCalls = 0, winterCalls = 0;
function mergeEntryGigsIntoPool(){ mergeEntryCalls++; return 0; }
function mergeWinterBridge88(){ winterCalls++; return 0; }
/* normalizeGigRecord 嘅無 guard helper——測試沙盒用最保守嘅 stub（唔改 eraTagLabel）： */
function boardNotePlayerOk(){ return false; }
function looksLikeEraId(){ return false; }
function humanizeEraId(s){ return s; }
function buildWire(yearActive){
  const byYear = {};
  gigList.forEach(g => { const yy = Number(g.year); (byYear[yy] = byYear[yy] || []).push(g); });
  const gigsByYear = {};
  [1990, 1991, 1992].forEach(yy => {
    if (byYear[yy].length) gigsByYear[yy] = { version: gigData.version || 'gigs_new v1', year: yy, gigs: byYear[yy] };
  });
  return { gigsByYear, gigsYearActive: yearActive, gigsFromFile: true, errors: [] };
}
const gigs1990 = gigList.filter(g => Number(g.year) === 1990);
const gigs1991 = gigList.filter(g => Number(g.year) === 1991);
const gigs1992 = gigList.filter(g => Number(g.year) === 1992);
ok('B1 庫 counts：1990:126／1991:100／1992:80，共 306',
  gigs1990.length === 126 && gigs1991.length === 100 && gigs1992.length === 80 && gigList.length === 306);
S = { dayIndex: 651 };
ok('B2 dateObj：dayIndex 651 → 1991 年；1000 → 1992 年；100 → 1990 年',
  dateObj().getFullYear() === 1991 &&
  (S = { dayIndex: 1000 }, dateObj().getFullYear() === 1992) &&
  (S = { dayIndex: 100 }, dateObj().getFullYear() === 1990));

/* 1991 load：GIGS 仲係 1990 庫 → sync(false) 即刻換成 1991 庫 */
S = { dayIndex: 651 };
GIGS = gigs1990.map(g => Object.assign({}, g));
STORY_WIRE = buildWire(1990);
mergeEntryCalls = 0; winterCalls = 0;
syncGigsForCalendarYear(false);
const has102 = GIGS.some(g => g && g.id === 'gig_1991_film_102');
const f102 = GIGS.find(g => g && g.id === 'gig_1991_film_102');
ok('B3 1991 load：sync 後 GIGS 100 張、yearActive 1991、含 film_102、冇 1990 年通告',
  GIGS.length === 100 && STORY_WIRE.gigsYearActive === 1991 && has102 &&
  !GIGS.some(g => g && Number(g.year) === 1990));
ok('B4 1991 load 後 film_102 內容啱：《霓虹夜影》男主角／秋／film_harbour／pay [4416,5184]／req 演技 130 體能 90',
  !!f102 && f102.title === '《霓虹夜影》男主角' && f102.season === '秋' &&
  f102.loc === 'film_harbour' && Array.isArray(f102.pay) && f102.pay[0] === 4416 && f102.pay[1] === 5184 &&
  f102.req && f102.req.acting === 130 && f102.req.stamina === 90);
ok('B5 1991 load：sync 唔 call mergeEntryGigsIntoPool（只限 1990 年）',
  mergeEntryCalls === 0 && winterCalls === 0);

/* 1992 load */
S = { dayIndex: 1000 };
GIGS = gigs1990.map(g => Object.assign({}, g));
STORY_WIRE = buildWire(1990);
syncGigsForCalendarYear(false);
ok('B6 1992 load：sync 後 GIGS 80 張、yearActive 1992、含 film_114《海角歸人》、全部 1992 年',
  GIGS.length === 80 && STORY_WIRE.gigsYearActive === 1992 &&
  GIGS.some(g => g && g.id === 'gig_1992_film_114') &&
  !GIGS.some(g => g && Number(g.year) !== 1992));

/* 1990 load：已經同步 → no-op，唔重建（入門通告唔會被洗走） */
S = { dayIndex: 100 };
const marker = { id: 'test_entry_marker', entryTier: true, boardPriority: 'high' };
GIGS = gigs1990.map(g => Object.assign({}, g));
GIGS.push(marker);
const beforeRef = GIGS;
STORY_WIRE = buildWire(1990);
mergeEntryCalls = 0;
syncGigsForCalendarYear(false);
ok('B7 1990 load：sync(false) 係 no-op——同一陣列、長度不變、入門 marker 仲喺度、唔 call mergeEntry',
  GIGS === beforeRef && GIGS.length === 127 && GIGS.indexOf(marker) >= 0 && mergeEntryCalls === 0);

/* 已經同步嘅 1991：early return */
S = { dayIndex: 651 };
GIGS = gigs1991.map(g => Object.assign({}, g));
const ref91 = GIGS;
STORY_WIRE = buildWire(1991);
syncGigsForCalendarYear(false);
ok('B8 已同步 1991：sync(false) early return，同一陣列',
  GIGS === ref91 && GIGS.length === 100 && STORY_WIRE.gigsYearActive === 1991);

console.log('\n' + (fails.length ? ('FAILED: ' + fails.length + ' — ' + fails.join('；')) : 'ALL PASS'));
process.exit(fails.length ? 1 : 0);
