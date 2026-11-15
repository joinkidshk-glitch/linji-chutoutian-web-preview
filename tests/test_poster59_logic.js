// v20a59 作品圖＋主演接入邏輯測試（v20a229 B3 重寫：新庫版）
// 合約（B3 換庫）：
//   A 主演唔再經對照表回填——新庫 gig 自帶 leadStarId，leadStar59Of 經 POSTER59_STAR_IDS
//     反查中文名；名冊以外兩位（程天諾 ching_tinlok、彭少祺 pang_siuki）補喺函數入面
//   B normalize 唔再掂主演：leadStarId 原封唔郁，leadStar 唔回填；冪等
//   C 海報：POSTER59_DATA／POSTER85_IDS 已刪，poster59Path 一律回空字串（D-12 出圖之前，
//     各顯示位用 CSS 卡降級）
//   D 通告卡冇主演行 (POSTER90 照舊)：有名製作卡都唔預告主演；主演數據經 leadStarId 仍在
//   E 作品牆：只收 category 作品（臨記通告／補拍唔入牆）；年份係顯示年（唔再 +2）；
//     無星作品照入牆（冇主演冇海報）；冇海報出 CSS 片名卡；空牆有提示
//   F 殺青圖 helper：冇海報回空（唔阻流程）
// 行真路徑：真 normalizeGigRecord（連 TEXTFIX55＋BRIDGE56 兩層）、真 gigCardHtml、
// 真 worksWallEntries59／worksWallHtml59／wrapPoster59Html（STORY_WIRE.gigsByYear 用真新庫）。
// 反證：對 B2 index 行 → LEADSTAR59／POSTER59_DATA 抽取即 FAIL（舊表已刪）。
// 用法：node tests/test_poster59_logic.js [path-to-index.html]
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
const tfA = html.indexOf('/* ==== v20a55 TEXTFIX');
const tfB = html.indexOf('async function refreshCopyPacksFromDisk(){');
if(tfA<0 || tfB<0 || tfB<=tfA){ console.log('FAIL TEXTFIX55 block not found'); process.exit(1); }
const TF_SRC = html.slice(tfA, tfB);
const CONSTS = ['POSTER59_STAR_IDS'];
const FNS = ['poster59Path','leadStar59Of','leadStarLine59','esc59',
  'work59GigLookup','work59IsNamed','work59WorkOf','work59RoleOf','work59YearOf',
  'worksWallEntries59','workCard59Html','worksWallHtml59','wrapPoster59Html',
  'boardNotePlayerOk','looksLikeEraId','humanizeEraId','bridge56NormalizeGig','normalizeGigRecord',
  'stripEraIdsInText','eraTagDisplay','gigCardHtml'];
let WORLD_SRC;
try{
  WORLD_SRC = TF_SRC + '\n' + CONSTS.map(c=>extractConst(c).replace('const '+c, 'var '+c)).join('\n')
    + '\n' + FNS.map(f=>extractFn(f)).join('\n');
}catch(e){ console.log('FAIL extraction: '+e.message); process.exit(1); }
const PACK_NEW = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'content', 'gigs_new.json'), 'utf8'));
const BY_YEAR = {};
for(const y of [1990, 1991, 1992]){
  BY_YEAR[y] = { version: 'gigs_new v1', year: y, gigs: PACK_NEW.gigs.filter(g=>g.year === y) };
}
const STUBS_SRC = `
  var PACK_NEW = ${JSON.stringify(PACK_NEW)};
  var START = { y:1990, m:1, d:1 };
  var S = { dayIndex: 100, fame: 10, wrapHistory: [] };
  var GIGS = [];
  var STORY_WIRE = { gigsByYear: ${JSON.stringify(BY_YEAR)} };
  var awardsYearFromDay = function(di){ return 1990 + Math.floor((Number(di)||0) / 365); };
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
function setup(){ return 'eval(WORLD_SRC); eval(STUBS_SRC);'; }
const findGig = id=>PACK_NEW.gigs.find(g=>g.id===id);

/* ============ 段一：主演由 leadStarId 反查 ============ */
(function(){
  eval(setup());
  ok('star: 廖炳星（liu_bingxing）', leadStar59Of(findGig('gig_1990_film_101'))==='廖炳星');
  ok('star: 陸柏言（luk_baakyin）', leadStar59Of(findGig('gig_1990_film_108'))==='陸柏言');
  ok('star: 麥震東（mak_zhendong）', leadStar59Of(findGig('gig_1990_film_102'))==='麥震東');
  ok('star: 程天諾（ching_tinlok，名冊外補位）', leadStar59Of(findGig('gig_1992_rec_102'))==='程天諾');
  ok('star: 彭少祺（pang_siuki，名冊外補位）', leadStar59Of(findGig('gig_1990_ad_105'))==='彭少祺');
  ok('star: 無主演回空', leadStar59Of(findGig('gig_1990_film_113'))==='' && leadStar59Of(null)==='');
  ok('star: 已有 leadStar 字串優先', leadStar59Of({ leadStar:'陸柏言', leadStarId:'liu_bingxing' })==='陸柏言');
  ok('star: leadStarLine59 有名出主演行、無名出空', leadStarLine59(findGig('gig_1990_film_101')).indexOf('主演：廖炳星')>=0 && leadStarLine59(findGig('gig_1990_film_113'))==='');
})();

/* ============ 段二：normalize 唔再回填主演（leadStarId 原封唔郁＋冪等） ============ */
(function(){
  eval(setup());
  const g = normalizeGigRecord(JSON.parse(JSON.stringify(findGig('gig_1990_film_101'))));
  ok('fill: leadStarId 原封唔郁', g.leadStarId==='liu_bingxing');
  ok('fill: leadStar 唔回填（新庫唔帶呢欄）', g.leadStar == null);
  ok('fill: 反查照攞到中文名', leadStar59Of(g)==='廖炳星');
  const twice = normalizeGigRecord(JSON.parse(JSON.stringify(g)));
  ok('fill: 冪等（normalize 兩次唔變）', twice.leadStarId===g.leadStarId && leadStar59Of(twice)==='廖炳星');
  const nostar = normalizeGigRecord(JSON.parse(JSON.stringify(findGig('gig_1990_film_113'))));
  ok('fill: 無星 gig  normalize 後繼續無星', nostar.leadStarId == null && leadStar59Of(nostar)==='');
})();

/* ============ 段三：poster59Path 一律回空（D-12 之前） ============ */
(function(){
  eval(setup());
  ok('poster: 有名製作都回空', poster59Path('gig_1990_film_101')==='' && poster59Path('gig_1990_film_108')==='');
  ok('poster: 散工／亂 id 回空', poster59Path('gig_1990_film_113')==='' && poster59Path('nope')==='' && poster59Path('')==='' && poster59Path(null)==='');
})();

/* ============ 段四：通告卡主演行（POSTER90 照舊） ============ */
(function(){
  eval(setup());
  const g = normalizeGigRecord(JSON.parse(JSON.stringify(findGig('gig_1990_film_101'))));
  const card = gigCardHtml(g, {});
  ok('card: 有名製作卡冇主演行 (POSTER90)', card.indexOf('lead-star')<0 && card.indexOf('主演：')<0);
  ok('card: 有名製作 leadStarId 數據仍在 (POSTER90)', g.leadStarId==='liu_bingxing' && leadStar59Of(g)==='廖炳星');
  const e = normalizeGigRecord(JSON.parse(JSON.stringify(findGig('gig_1990_film_113'))));
  ok('card: 臨記通告卡冇主演行', gigCardHtml(e, {}).indexOf('主演：')<0);
})();

/* ============ 段五：作品牆（只收作品／年份顯示年／無星照入牆／CSS 卡） ============ */
(function(){
  eval(setup());
  S.wrapHistory = [
    { gigId:'gig_1990_film_101', title:'《大排檔笑話》男配角', type:'電影', totalDays:4, pay:1200, fame:5, popularity:5, wrappedDay:230, rating:'表現穩妥' },
    { gigId:'gig_1990_film_102', title:'《碼頭追風》男配角', type:'電影', totalDays:3, pay:1500, fame:3, popularity:3, wrappedDay:240, rating:'順利殺青' },
    { gigId:'gig_1990_film_113', title:'《片場門口》群演', type:'電影', totalDays:1, pay:900, fame:1, popularity:2, wrappedDay:250, rating:'順利殺青' },
    { gigId:'gig_1990_film_123', title:'《雨夜追逐戲》補拍群演', type:'電影', totalDays:1, pay:800, fame:1, popularity:1, wrappedDay:120, rating:'順利殺青' },
    { gigId:'gig_1992_rec_102', title:'《夜場匯演》匯演嘉賓歌手', type:'唱片通告', totalDays:2, pay:3000, fame:4, popularity:4, wrappedDay:150, rating:'表現穩妥' }
  ];
  const es = worksWallEntries59();
  ok('wall: 只入作品（5 條歷史 → 3 部：兩部臨記通告／補拍唔入）', es.length===3);
  const hb = es.find(x=>x.gigId==='gig_1990_film_101');
  ok('wall: 回查 workTitle', !!hb && hb.work==='大排檔笑話');
  ok('wall: 回查 roleLabel', !!hb && hb.role==='男配角');
  ok('wall: 年份係顯示年 1990（唔再 +2）', !!hb && hb.year===1990);
  ok('wall: 主演反查＋海報回空', !!hb && hb.leadStar==='廖炳星' && hb.poster==='');
  const ct = es.find(x=>x.gigId==='gig_1992_rec_102');
  ok('wall: 名冊外主演照顯示（程天諾）', !!ct && ct.leadStar==='程天諾' && ct.year===1992);
  ok('wall: 臨記通告／補拍唔入牆', !es.some(x=>x.gigId==='gig_1990_film_113' || x.gigId==='gig_1990_film_123'));
  /* 無星作品：新庫 141 張作品全部有星，用 synthetic gig 測無星路 */
  GIGS = [{ id:'gig_1990_test_301', category:'作品', year:1990, type:'電影', title:'《無星小品》臨時演員', workTitle:'無星小品', roleLabel:'臨時演員', leadStarId:null }];
  S.wrapHistory.push({ gigId:'gig_1990_test_301', title:'《無星小品》臨時演員', type:'電影', totalDays:1, pay:1000, fame:1, popularity:1, wrappedDay:260, rating:'順利殺青' });
  const es2 = worksWallEntries59();
  const ns = es2.find(x=>x.gigId==='gig_1990_test_301');
  ok('wall: 無星作品照入牆（冇主演冇海報）', !!ns && ns.leadStar==='' && ns.poster==='' && ns.work==='無星小品');
  const wallHtml = worksWallHtml59();
  ok('wall html: 全部 CSS 片名卡（冇 data URI 海報）', wallHtml.indexOf('work-csscard59')>=0 && wallHtml.indexOf('data:image')<0);
  ok('wall html: 顯示主演＋崗位', wallHtml.indexOf('主演：廖炳星')>=0 && wallHtml.indexOf('阿偉：男配角')>=0);
  ok('wall html: 臨記通告／補拍唔入牆', wallHtml.indexOf('片場門口')<0 && wallHtml.indexOf('雨夜追逐戲')<0);
  S.wrapHistory = [];
  ok('wall html: 空牆有提示', worksWallHtml59().indexOf('仲未有作品入牆')>=0);
  /* entryTier 旗照舊排除 */
  GIGS = [Object.assign({}, JSON.parse(JSON.stringify(findGig('gig_1990_film_101'))), { entryTier:true })];
  STORY_WIRE = { gigsByYear:{} };
  S.wrapHistory = [{ gigId:'gig_1990_film_101', title:'《大排檔笑話》男配角', type:'電影', totalDays:4, pay:1200, fame:5, popularity:5, wrappedDay:230, rating:'表現穩妥' }];
  ok('wall: entryTier 旗照舊排除', worksWallEntries59().length===0);
})();

/* ============ 段六：殺青圖 helper（冇海報回空） ============ */
(function(){
  eval(setup());
  ok('wrap: 有名製作都回空（D-12 之前，唔阻流程）', wrapPoster59Html('gig_1990_film_101')==='' && wrapPoster59Html('gig_1990_film_113')==='' && wrapPoster59Html('nope')==='');
})();

/* ============ 段七：work59YearOf 顯示年 ============ */
(function(){
  eval(setup());
  ok('year: 新 id 年份唔 +2（1992 唔變 1994）', work59YearOf({ gigId:'gig_1992_film_101' }, null)===1992);
  ok('year: 1990 唔變 1992', work59YearOf({ gigId:'gig_1990_film_101' }, null)===1990);
  ok('year: h.year 優先', work59YearOf({ gigId:'gig_1992_film_101', year:1991 }, null)===1991);
})();

if(fails.length){ console.log('FAILURES:', fails.join(' | ')); process.exit(1); }
console.log('ALL PASS');
