// v20a59 作品圖＋主演接入邏輯測試：LEADSTAR59 回填（137 部）、散工／入門零主演、
// 通告卡主演行、作品牆（舊存檔格式相容／有名製作過濾／海報＋CSS 卡）、殺青圖 helper。
// 海報交付形態：POSTER59_DATA data URI 內嵌（推送通道唔收 binary，外部圖檔入唔到 repo）。
// 行真路徑：真 normalizeGigRecord（連 TEXTFIX55＋BRIDGE56＋POSTER59 三層）、真 gigCardHtml、
// 真 worksWallEntries59／worksWallHtml59／wrapPoster59Html（STORY_WIRE.gigsByYear 用真 1988 包）。
// 反證：對 v20a58 index 行 → POSTER59 區塊唔存在，抽取即 FAIL。
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
// v20a85 harness 維護：poster59Path 擴充咗 POSTER85 分支，抽取清單加 POSTER85_IDS／poster85File；
// 本檔全部斷言（試點 10 張行為）冇改——POSTER85 覆蓋另見 test_poster85_logic.js。
const CONSTS = ['LEADSTAR59','POSTER59_STAR_IDS','POSTER59_IDS','POSTER59_DATA','POSTER85_IDS','BRIDGE56_VARIANTS','BRIDGE56_CROSSYEAR_RENAME'];
const FNS = ['poster59Path','poster85File','leadStar59Apply','leadStar59Of','leadStarLine59','esc59',
  'work59GigLookup','work59IsNamed','work59WorkOf','work59RoleOf','work59YearOf',
  'worksWallEntries59','workCard59Html','worksWallHtml59','wrapPoster59Html',
  'boardNotePlayerOk','looksLikeEraId','humanizeEraId','bridge56NormalizeGig','normalizeGigRecord',
  'stripEraIdsInText','eraTagDisplay','gigCardHtml'];
let WORLD_SRC;
try{
  WORLD_SRC = TF_SRC + '\n' + CONSTS.map(c=>extractConst(c).replace('const '+c, 'var '+c)).join('\n')
    + '\n' + FNS.map(f=>extractFn(f)).join('\n');
}catch(e){ console.log('FAIL extraction: '+e.message); process.exit(1); }
const PACK88 = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'gigs_1988.json'), 'utf8'));
const STUBS_SRC = `
  var PACK88 = ${JSON.stringify(PACK88)};
  var START = { y:1988, m:3, d:7 };
  var S = { dayIndex: 100, fame: 10, wrapHistory: [] };
  var GIGS = [];
  var STORY_WIRE = { gigsByYear: { "1988": PACK88 } };
  var awardsYearFromDay = function(di){ return 1988 + Math.floor((Number(di)||0) / 365); };
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
const ROSTER10 = ['陸柏言','廖炳星','齊鎮海','麥震東','鍾楚凝','蘇芷茵','彭少祺','葉敏芝','駱家聲','顧明輝'];

/* ============ 段一：對照表完整性（137 部全喺包入面；包非常規即入門 6 張） ============ */
(function(){
  eval(setup());
  const keys = Object.keys(LEADSTAR59);
  ok('table: 137 部齊', keys.length===137);
  const packIds = new Set(PACK88.gigs.map(g=>g.id));
  ok('table: 全部 id 真喺 1988 包', keys.every(k=>packIds.has(k)));
  const entryIds = new Set(PACK88.gigs.filter(g=>g.entryTier).map(g=>g.id));
  ok('table: 入門 6 張唔入表', keys.every(k=>!entryIds.has(k)) && entryIds.size===6);
  const nonEntry = PACK88.gigs.filter(g=>!g.entryTier).map(g=>g.id);
  ok('table: 包 137 部常規全覆蓋', nonEntry.every(id=>Object.prototype.hasOwnProperty.call(LEADSTAR59, id)));
})();

/* ============ 段二：normalize 回填（全 137 部＋散工／入門零主演＋冪等） ============ */
(function(){
  eval(setup());
  let bad = [];
  PACK88.gigs.forEach(raw=>{
    const g = normalizeGigRecord(JSON.parse(JSON.stringify(raw)));
    const inTable = Object.prototype.hasOwnProperty.call(LEADSTAR59, g.id);
    if(inTable){
      const want = LEADSTAR59[g.id];
      if(want === null){ if(g.leadStar !== null) bad.push(g.id+':null-star'); }
      else {
        if(g.leadStar !== want) bad.push(g.id+':value');
        else if(String(want).split('、').some(n=>ROSTER10.indexOf(n)<0)) bad.push(g.id+':roster');
      }
    } else {
      if(g.leadStar != null) bad.push(g.id+':should-be-empty');
    }
  });
  ok('fill: 137 部回填正確（名冊內／素人 null）', bad.length===0);
  if(bad.length) console.log('  bad:', bad.slice(0,8).join(', '));
  const spot = normalizeGigRecord(JSON.parse(JSON.stringify(PACK88.gigs.find(g=>g.id==='gig_1988_film_harbour_high'))));
  ok('fill: 夜海鎗火 leadStarId 接返名冊 id', spot.leadStar==='陸柏言' && spot.leadStarId==='luk_baakyin');
  const dual = normalizeGigRecord(JSON.parse(JSON.stringify(PACK88.gigs.find(g=>g.id==='gig_1988_var_04'))));
  ok('fill: 選拔夜雙主演', dual.leadStar==='彭少祺、葉敏芝');
  const bridge = normalizeGigRecord({ id:'gig_1988_soft_bridge_summer_ad', softBridge:true, title:'《暑期街招》廣告路人', type:'廣告', req:{} });
  ok('fill: 常駐散工冇 leadStar', bridge.leadStar == null);
  const once = normalizeGigRecord(JSON.parse(JSON.stringify(PACK88.gigs.find(g=>g.id==='gig_1988_tv_06'))));
  const twice = normalizeGigRecord(once);
  ok('fill: 冪等（normalize 兩次唔變）', twice.leadStar===once.leadStar && once.leadStar==='陸柏言');
})();

/* ============ 段三：海報 data URI（POSTER59_DATA 10 條；其餘冇圖） ============ */
(function(){
  eval(setup());
  const pilotIds = ['gig_1988_film_harbour_high','gig_1988_film_cotton_spring_high',
    'gig_1988_film_lion_summer_high','gig_1988_film_03','gig_1988_tv_03',
    'gig_1988_film_cotton_autumn_low','gig_1988_var_04','gig_1988_ad_central_spring_high',
    'gig_1988_rec_03','gig_1988_tv_06'];
  ok('poster: POSTER59_DATA 10 條齊', Object.keys(POSTER59_DATA).length===10);
  ok('poster: DATA 鍵同白名單 POSTER59_IDS 一致',
    pilotIds.every(id=>POSTER59_IDS[id] && POSTER59_DATA[id]) && Object.keys(POSTER59_DATA).every(id=>POSTER59_IDS[id]));
  ok('poster: 試點 10 張回 data URI',
    pilotIds.every(id=>poster59Path(id)===POSTER59_DATA[id] && poster59Path(id).indexOf('data:image/webp;base64,')===0));
  ok('poster: data URI 解碼係 WebP RIFF 頭', pilotIds.every(id=>{
    const buf = Buffer.from(POSTER59_DATA[id].split(',')[1], 'base64');
    return buf.length>5000 && buf.slice(0,4).toString('ascii')==='RIFF' && buf.slice(8,12).toString('ascii')==='WEBP';
  }));
  ok('poster: 未出圖嘅有名製作回空', poster59Path('gig_1988_film_02')==='');
  ok('poster: 散工／亂 id 回空', poster59Path('gig_1988_soft_bridge_summer_ad')==='' && poster59Path('nope')==='');
})();

/* ============ 段四：通告卡主演行（v20a90 POSTER90 改版） ============ */
/* POSTER90（用戶實玩拍板）：通告卡係完成前場合，唔再顯示主演行——本段由 v59 原版
   「有名製作卡有主演行」改為「有名製作卡都冇主演行」；leadStar 數據回填照舊
   （段二斷言冇改），主演名只喺完成後場合（作品牆段五／殺青）出現。 */
(function(){
  eval(setup());
  const g = normalizeGigRecord(JSON.parse(JSON.stringify(PACK88.gigs.find(x=>x.id==='gig_1988_film_harbour_high'))));
  const card = gigCardHtml(g, {});
  ok('card: 有名製作卡冇主演行 (POSTER90)', card.indexOf('lead-star')<0 && card.indexOf('主演：')<0);
  ok('card: 有名製作 leadStar 數據仍在 (POSTER90)', g.leadStar==='陸柏言');
  const e = normalizeGigRecord(JSON.parse(JSON.stringify(PACK88.gigs.find(x=>x.entryTier))));
  ok('card: 入門卡冇主演行（唔出空欄）', gigCardHtml(e, {}).indexOf('主演：')<0);
  const d = normalizeGigRecord(JSON.parse(JSON.stringify(PACK88.gigs.find(x=>x.id==='gig_1988_var_04'))));
  ok('card: 雙主演卡都唔預告主演 (POSTER90)', gigCardHtml(d, {}).indexOf('主演：')<0 && d.leadStar==='彭少祺、葉敏芝');
})();

/* ============ 段五：作品牆（舊存檔格式／過濾／欄位回查） ============ */
(function(){
  eval(setup());
  S.wrapHistory = [
    { gigId:'gig_1988_film_harbour_high', title:'《夜海鎗火》特約男主', type:'電影', totalDays:3, pay:48000, fame:5, popularity:5, wrappedDay:230, rating:'表現穩妥' },
    { gigId:'gig_1988_var_04', title:'《樂壇新星選拔夜》伴舞演員', type:'綜藝', totalDays:1, pay:4000, fame:2, popularity:3, wrappedDay:240, rating:'順利殺青' },
    { gigId:'gig_1988_ad_adm_autumn_low', title:'《秋裝街頭隨拍輯》街頭模特兒', type:'廣告', totalDays:1, pay:3350, fame:1, popularity:2, wrappedDay:250, rating:'順利殺青' },
    { gigId:'gig_1988_entry_ad_passerby', title:'《便利店短片》廣告路人 B', type:'廣告', totalDays:1, pay:950, fame:1, popularity:3, wrappedDay:10, rating:'順利殺青' },
    { gigId:'gig_1988_soft_bridge_summer_ad', title:'《暑期街招》廣告路人', type:'廣告', totalDays:1, pay:3700, fame:2, popularity:2, wrappedDay:120, rating:'順利殺青' },
    { gigId:'gig_1988_film_02', title:'《孤劍破陣》武師群戲', type:'電影', totalDays:2, pay:7000, fame:3, popularity:3, wrappedDay:150, rating:'表現穩妥', workTitle:'孤劍破陣', roleLabel:'武師群戲', year:1988 }
  ];
  const es = worksWallEntries59();
  ok('wall: 只入有名製作（6 條歷史 → 4 部）', es.length===4);
  const hb = es.find(x=>x.gigId==='gig_1988_film_harbour_high');
  ok('wall: 舊存檔回查 workTitle', !!hb && hb.work==='夜海鎗火');
  ok('wall: 舊存檔回查 roleLabel', !!hb && hb.role==='特約男主');
  ok('wall: 舊存檔回查年份＋主演＋海報', !!hb && hb.year===1988 && hb.leadStar==='陸柏言' && hb.poster===POSTER59_DATA['gig_1988_film_harbour_high']);
  const ss = es.find(x=>x.gigId==='gig_1988_ad_adm_autumn_low');
  ok('wall: 素人無星照入牆（冇主演冇海報）', !!ss && ss.leadStar==='' && ss.poster==='');
  const snap = es.find(x=>x.gigId==='gig_1988_film_02');
  ok('wall: 新存檔快照欄位優先', !!snap && snap.work==='孤劍破陣' && snap.role==='武師群戲' && snap.leadStar==='齊鎮海');
  const wallHtml = worksWallHtml59();
  ok('wall html: 有海報出 img（data URI）', wallHtml.indexOf(POSTER59_DATA['gig_1988_film_harbour_high'])>=0 && wallHtml.indexOf(POSTER59_DATA['gig_1988_var_04'])>=0);
  ok('wall html: 冇海報出 CSS 片名卡', wallHtml.indexOf('work-csscard59')>=0 && wallHtml.indexOf('秋裝街頭隨拍輯')>=0);
  ok('wall html: 顯示主演＋崗位', wallHtml.indexOf('主演：陸柏言')>=0 && wallHtml.indexOf('阿偉：特約男主')>=0);
  ok('wall html: 散工唔入牆', wallHtml.indexOf('暑期街招')<0 && wallHtml.indexOf('便利店短片')<0);
  S.wrapHistory = [];
  ok('wall html: 空牆有提示', worksWallHtml59().indexOf('仲未有作品入牆')>=0);
})();

/* ============ 段六：殺青圖 helper ============ */
(function(){
  eval(setup());
  const h = wrapPoster59Html('gig_1988_film_harbour_high');
  ok('wrap: 有海報出圖＋主演', h.indexOf('wrap-poster59')>=0 && h.indexOf(POSTER59_DATA['gig_1988_film_harbour_high'])>=0 && h.indexOf('主演：陸柏言')>=0);
  ok('wrap: 冇海報回空（唔阻流程）', wrapPoster59Html('gig_1988_film_02')==='' && wrapPoster59Html('gig_1988_soft_bridge_summer_ad')==='');
})();

if(fails.length){ console.log('FAILURES:', fails.join(' | ')); process.exit(1); }
console.log('ALL PASS');
