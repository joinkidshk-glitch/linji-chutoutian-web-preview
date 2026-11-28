// v424 意圖更新：詳情分段重排，每週開工入檔期段（製作資料之前）。
// v20a252 詳情頁按類型分流＋作品牆陣容行邏輯測試（SPEC-v2 §6.2／§2.3，D-v2-6／D-v2-3）
// 合約：
//   A 詳情頁按類型分流：電影／電視四角（男主角／女主角／男配角／女配角），玩家格標「應徵中」
//     （由 roleLabel 推導，唔靠「邊格係 null」——null 亦可以係從缺）；廣告＝代言人＋產品＋適合性別；
//     唱片＝主唱歌手＋歌曲類型＋形式；綜藝＝主持＋嘉賓陣容＋環節名單；臨記通告唔顯示陣容；
//     補拍通告唔顯示陣容、只顯示原製作名。唔相關欄位永不渲染。
//   B 舊庫 gig 無新欄位嗰陣 graceful：唔顯示、唔爆錯（null／undefined／缺 category 全部回 ""）。
//   C 板卡維持 §6.1：唔出主演行、唔出成品海報、唔出分流欄位。
//   D 作品牆／履歷：主演行改陣容行（電影／電視「主演：leadM 名或阿偉、leadF 名」；廣告「代言：lead 名」；
//     唱片「主唱：singer 名」；綜藝「主持：host 名」）；無新欄位跌返舊制 leadStar59Of 行（舊檔相容）。
//   E 導演行只喺電影／電視作品出（§6.2）；臨記簡介用 blurb。
// 行真路徑：真 gigCastDetailRows252／work59CastLineOf／worksWallEntries59／workCard59Html／
//   gigCardHtml（STORY_WIRE.gigsByYear 用真新庫 v2）。
// 用法：node tests/test_cast252_logic.js [path-to-index.html]
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
const CONSTS = ['CAST252_STAR_NAMES','POSTER59_STAR_IDS'];
const FNS = ['starName252Of','gigPlayerCastSlot252','gigCastSlotValue252','gigCastDetailRows252',
  'work59CastLineOf','esc59','gigGenreLabel',
  'work59GigLookup','work59IsNamed','work59WorkOf','work59RoleOf','work59YearOf',
  'worksWallEntries59','workCard59Html','worksWallHtml59','leadStar59Of','poster59Path',
  'boardNotePlayerOk','looksLikeEraId','humanizeEraId','stripEraIdsInText','eraTagDisplay',
  'gigCardHtml'];
let WORLD_SRC;
try{
  WORLD_SRC = CONSTS.map(c=>extractConst(c).replace('const '+c, 'var '+c)).join('\n')
    + '\n' + FNS.map(f=>extractFn(f)).join('\n');
}catch(e){ console.log('FAIL extraction: '+e.message); process.exit(1); }
const PACK_NEW = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'content', 'gigs_new.json'), 'utf8'));
const BY_YEAR = {};
for(const y of [1990, 1991, 1992]){
  BY_YEAR[y] = { version: 'gigs_new v2', year: y, gigs: PACK_NEW.gigs.filter(g=>g.year === y) };
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

/* ============ 段一：星名對照（17 位，含兩個新星） ============ */
(function(){
  eval(setup());
  ok('name: 陸柏言／鍾楚凝', starName252Of('luk_baakyin')==='陸柏言' && starName252Of('chung_choning')==='鍾楚凝');
  ok('name: 新星胡美琳／韓秀婷', starName252Of('wu_meilam')==='胡美琳' && starName252Of('hon_sauting')==='韓秀婷');
  ok('name: 名冊外程天諾／彭少祺', starName252Of('ching_tinlok')==='程天諾' && starName252Of('pang_siuki')==='彭少祺');
  ok('name: 認唔到／空／null 回空', starName252Of('nobody')==='' && starName252Of('')==='' && starName252Of(null)==='' && starName252Of(undefined)==='');
})();

/* ============ 段二：玩家格由 roleLabel 推導（唔靠 null） ============ */
(function(){
  eval(setup());
  ok('slot: 電影男配角→supportM', gigPlayerCastSlot252(findGig('gig_1990_film_101'))==='supportM');
  ok('slot: 電影男主角→leadM', gigPlayerCastSlot252(findGig('gig_1991_film_102'))==='leadM');
  ok('slot: 武師唔佔四格', gigPlayerCastSlot252(findGig('gig_1990_film_105'))===null);
  ok('slot: 廣告電視廣告主角→leadM', gigPlayerCastSlot252(findGig('gig_1990_ad_104'))==='leadM');
  ok('slot: 廣告配角→supportM', gigPlayerCastSlot252(findGig('gig_1990_ad_102'))==='supportM');
  ok('slot: 廣告平面模特兒唔佔格', gigPlayerCastSlot252(findGig('gig_1990_ad_101'))===null);
  ok('slot: 臨記通告唔佔格（數據有齊四角都唔計）', gigPlayerCastSlot252(findGig('gig_1990_film_201'))===null);
  ok('slot: 補拍通告唔佔格', gigPlayerCastSlot252(findGig('gig_1990_film_301'))===null);
  ok('slot: 唱片／綜藝唔行四角', gigPlayerCastSlot252(findGig('gig_1990_rec_101'))===null && gigPlayerCastSlot252(findGig('gig_1990_variety_101'))===null);
  ok('slot: 缺 category／null 回 null', gigPlayerCastSlot252({ type:'電影', roleLabel:'男主角' })===null && gigPlayerCastSlot252(null)===null);
  ok('slot: roleLabel 缺失用 roleScale 兜底', gigPlayerCastSlot252({ category:'作品', type:'電影', roleScale:'film_lead_big' })==='leadM'
    && gigPlayerCastSlot252({ category:'作品', type:'電視劇', roleScale:'tv_cameo_short' })===null);
})();

/* ============ 段三：詳情頁——電影／電視四角 ============ */
(function(){
  eval(setup());
  const f101 = gigCastDetailRows252(findGig('gig_1990_film_101'));
  ok('detail film: 有已公布陣容＋四格齊', f101.indexOf('已公布陣容')>=0 && f101.indexOf('男主角')>=0 && f101.indexOf('女主角')>=0 && f101.indexOf('男配角')>=0 && f101.indexOf('女配角')>=0);
  ok('detail film: 男主角陸柏言／女主角鍾楚凝', f101.indexOf('陸柏言')>=0 && f101.indexOf('鍾楚凝')>=0);
  ok('detail film: 玩家男配角格標應徵中', f101.indexOf('應徵中')>=0 && f101.indexOf('男配角</span><span class="v">應徵中')>=0);
  ok('detail film: 女配角胡美琳（新星照顯示）', f101.indexOf('胡美琳')>=0);
  ok('detail film: 唔出代言／主唱／主持欄', f101.indexOf('代言人')<0 && f101.indexOf('主唱歌手')<0 && f101.indexOf('主持')<0);
  const f106 = gigCastDetailRows252(findGig('gig_1990_film_106'));
  ok('detail film: 從缺格標從缺（女主角／女配角），玩家格照標應徵中',
    f106.indexOf('女主角</span><span class="v">從缺')>=0 && f106.indexOf('女配角</span><span class="v">從缺')>=0
    && f106.indexOf('男配角</span><span class="v">應徵中')>=0 && f106.indexOf('麥震東')>=0);
  const f102 = gigCastDetailRows252(findGig('gig_1991_film_102'));
  ok('detail film: 男主角玩家格標應徵中（霓虹夜影爭位格）',
    f102.indexOf('男主角</span><span class="v">應徵中')>=0 && f102.indexOf('魏詠男')>=0);
  ok('detail film: 無 cast 嘅作品回空（舊庫 graceful）',
    gigCastDetailRows252({ category:'作品', type:'電影', roleLabel:'男配角' })==='');
  ok('detail film: 無 category 回空', gigCastDetailRows252({ type:'電影', roleLabel:'男主角' })==='')
  ok('detail film: null 回空', gigCastDetailRows252(null)==='' && gigCastDetailRows252(undefined)==='');
})();

/* ============ 段四：詳情頁——廣告 ============ */
(function(){
  eval(setup());
  const a101 = gigCastDetailRows252(findGig('gig_1990_ad_101'));
  ok('detail ad: 代言人沈映雪（F 產品女星做主角）', a101.indexOf('代言人</span><span class="v">沈映雪')>=0);
  ok('detail ad: 產品名＋類別＋品牌齊', a101.indexOf('護膚霜')>=0 && a101.indexOf('護膚品')>=0 && a101.indexOf('潤妍堂')>=0);
  ok('detail ad: 適合性別女', a101.indexOf('適合性別</span><span class="v">女')>=0);
  ok('detail ad: 平面模特兒唔佔格，唔出應徵中', a101.indexOf('應徵中')<0);
  ok('detail ad: 唔出四角／主唱／主持欄', a101.indexOf('男主角')<0 && a101.indexOf('女主角')<0 && a101.indexOf('主唱歌手')<0 && a101.indexOf('主持')<0);
  const a104 = gigCastDetailRows252(findGig('gig_1990_ad_104'));
  ok('detail ad: 玩家做電視廣告主角→代言人應徵中', a104.indexOf('代言人</span><span class="v">應徵中')>=0);
  const a102 = gigCastDetailRows252(findGig('gig_1990_ad_102'));
  ok('detail ad: 玩家做配角→代言人出 leadF 蘇芷茵', a102.indexOf('代言人</span><span class="v">蘇芷茵')>=0 && a102.indexOf('洗頭水')>=0 && a102.indexOf('清泉')>=0);
})();

/* ============ 段五：詳情頁——唱片 ============ */
(function(){
  eval(setup());
  const r101 = gigCastDetailRows252(findGig('gig_1990_rec_101'));
  ok('detail rec: 主唱歌手沈映雪（女）', r101.indexOf('主唱歌手</span><span class="v">沈映雪（女）')>=0);
  ok('detail rec: 歌曲類型抒情＋形式大碟', r101.indexOf('歌曲類型</span><span class="v">抒情')>=0 && r101.indexOf('形式</span><span class="v">大碟')>=0);
  ok('detail rec: 唔出四角／代言／主持欄', r101.indexOf('男主角')<0 && r101.indexOf('代言人')<0 && r101.indexOf('主持')<0);
  const r107 = gigCastDetailRows252(findGig('gig_1990_rec_107'));
  ok('detail rec: 玩家做大碟主唱→主唱歌手應徵中（v307 B1：singer 改 null，監製星唔再冒充主唱）',
    r107.indexOf('主唱歌手</span><span class="v">應徵中')>=0 && r107.indexOf('搖滾')>=0);
  ok('detail rec: 臨記唱片唔出任何欄', gigCastDetailRows252(findGig('gig_1990_rec_201'))==='');
})();

/* ============ 段六：詳情頁——綜藝 ============ */
(function(){
  eval(setup());
  const v101 = gigCastDetailRows252(findGig('gig_1990_variety_101'));
  ok('detail variety: 玩家做主持→主持應徵中', v101.indexOf('主持</span><span class="v">應徵中')>=0);
  ok('detail variety: 嘉賓陣容齊四位', v101.indexOf('彭少祺')>=0 && v101.indexOf('廖炳星')>=0 && v101.indexOf('藍若曦')>=0 && v101.indexOf('麥震東')>=0);
  ok('detail variety: 環節名單齊', v101.indexOf('搶答遊戲')>=0 && v101.indexOf('環節')>=0);
  const v102 = gigCastDetailRows252(findGig('gig_1990_variety_102'));
  ok('detail variety: 主持彭少祺＋嘉賓＋環節', v102.indexOf('主持</span><span class="v">彭少祺')>=0
    && v102.indexOf('駱家聲')>=0 && v102.indexOf('沈映雪')>=0 && v102.indexOf('初賽歌唱')>=0);
  ok('detail variety: 唔出四角／代言／主唱欄', v101.indexOf('男主角')<0 && v101.indexOf('代言人')<0 && v101.indexOf('主唱歌手')<0);
  ok('detail variety: 臨記綜藝唔出任何欄', gigCastDetailRows252(findGig('gig_1990_variety_201'))==='');
})();

/* ============ 段七：詳情頁——補拍／臨記 ============ */
(function(){
  eval(setup());
  const r301 = gigCastDetailRows252(findGig('gig_1990_film_301'));
  ok('detail reshoot: 只出原製作《西環月色》', r301.indexOf('原製作')>=0 && r301.indexOf('西環月色')>=0);
  ok('detail reshoot: 唔出陣容（數據有齊四角都唔顯示）',
    r301.indexOf('男主角')<0 && r301.indexOf('女主角')<0 && r301.indexOf('代言人')<0 && r301.indexOf('應徵中')<0);
  ok('detail extra: 臨記通告回空（唔顯示陣容）', gigCastDetailRows252(findGig('gig_1990_film_201'))==='');
})();

/* ============ 段八：作品牆陣容行 ============ */
(function(){
  eval(setup());
  ok('wall line film: 配角作品→主演：陸柏言、鍾楚凝（玩家配角格唔入主演行）',
    work59CastLineOf(findGig('gig_1990_film_101'), { roleLabel:'男配角' })==='主演：陸柏言、鍾楚凝');
  ok('wall line film: 男主角作品→主演：阿偉、魏詠男',
    work59CastLineOf(findGig('gig_1991_film_102'), { roleLabel:'男主角' })==='主演：阿偉、魏詠男');
  ok('wall line film: 從缺女主角唔出（血色江湖）',
    work59CastLineOf(findGig('gig_1990_film_106'), { roleLabel:'男配角' })==='主演：麥震東');
  ok('wall line ad: 代言：沈映雪／玩家代言→代言：阿偉',
    work59CastLineOf(findGig('gig_1990_ad_101'), {})==='代言：沈映雪'
    && work59CastLineOf(findGig('gig_1990_ad_104'), { roleLabel:'電視廣告主角' })==='代言：阿偉');
  ok('wall line rec: 主唱：沈映雪', work59CastLineOf(findGig('gig_1990_rec_101'), {})==='主唱：沈映雪');
  ok('wall line variety: 主持：阿偉／主持：彭少祺',
    work59CastLineOf(findGig('gig_1990_variety_101'), { roleLabel:'綜合節目遊戲環節主持' })==='主持：阿偉'
    && work59CastLineOf(findGig('gig_1990_variety_102'), { roleLabel:'歌唱比賽參賽者' })==='主持：彭少祺');
  ok('wall line: 無新欄位回空（舊庫 fallback 用 leadStar 行）',
    work59CastLineOf({ category:'作品', type:'電影', leadStarId:'luk_baakyin' }, {})==='' && work59CastLineOf(null, {})==='');
})();

/* ============ 段九：作品牆 entries＋卡片（陣容行＋舊檔 fallback） ============ */
(function(){
  eval(setup());
  S.wrapHistory = [
    { gigId:'gig_1990_film_101', title:'《梭哈》男配角', type:'電影', totalDays:4, pay:1200, fame:5, popularity:5, wrappedDay:230, rating:'表現穩妥' },
    { gigId:'gig_1990_film_201', title:'《富貴茶餐廳》趕檔場務助手', type:'電影', totalDays:1, pay:900, fame:1, popularity:2, wrappedDay:250, rating:'順利殺青' },
    { gigId:'gig_1990_film_301', title:'《西環月色》補拍群演', type:'電影', totalDays:1, pay:800, fame:1, popularity:1, wrappedDay:120, rating:'順利殺青' },
    { gigId:'gig_1992_rec_102', title:'《硬漢柔情》新人搖滾主唱', type:'唱片通告', totalDays:2, pay:3000, fame:4, popularity:4, wrappedDay:150, rating:'表現穩妥' },
    { gigId:'gig_1990_variety_101', title:'《今夜歡笑》綜合節目遊戲環節主持', type:'綜藝', totalDays:2, pay:2000, fame:4, popularity:4, wrappedDay:160, rating:'表現穩妥' }
  ];
  const es = worksWallEntries59();
  ok('wall: 只入作品（5 條歷史 → 3 部）', es.length===3);
  const hb = es.find(x=>x.gigId==='gig_1990_film_101');
  ok('wall: 電影陣容行', !!hb && hb.castLine==='主演：陸柏言、鍾楚凝');
  const ct = es.find(x=>x.gigId==='gig_1992_rec_102');
  ok('wall: 唱片陣容行（玩家主唱→主唱：阿偉）', !!ct && ct.castLine==='主唱：阿偉');
  const vt = es.find(x=>x.gigId==='gig_1990_variety_101');
  ok('wall: 綜藝陣容行（主持：阿偉）', !!vt && vt.castLine==='主持：阿偉');
  const wallHtml = worksWallHtml59();
  ok('wall html: 陣容行齊三種', wallHtml.indexOf('主演：陸柏言、鍾楚凝')>=0 && wallHtml.indexOf('主唱：阿偉')>=0 && wallHtml.indexOf('主持：阿偉')>=0);
  ok('wall html: 臨記通告／補拍唔入牆', wallHtml.indexOf('富貴茶餐廳')<0 && wallHtml.indexOf('西環月色')<0);
  /* 舊檔 fallback：舊庫 gig 有 leadStarId、無 cast——陣容行回空，卡片跌返舊制主演行 */
  GIGS = [{ id:'gig_1990_test_303', category:'作品', year:1990, type:'電影', title:'《舊庫戲》男配角', workTitle:'舊庫戲', roleLabel:'男配角', leadStarId:'luk_baakyin' }];
  STORY_WIRE = { gigsByYear:{} };
  S.wrapHistory = [{ gigId:'gig_1990_test_303', title:'《舊庫戲》男配角', type:'電影', totalDays:1, pay:1000, fame:1, popularity:1, wrappedDay:260, rating:'順利殺青' }];
  const es2 = worksWallEntries59();
  ok('wall fallback: 舊庫 gig castLine 回空、leadStar 照反查', es2.length===1 && es2[0].castLine==='' && es2[0].leadStar==='陸柏言');
  ok('wall fallback: 卡片出舊制主演行', worksWallHtml59().indexOf('主演：陸柏言')>=0);
})();

/* ============ 段十：板卡維持 §6.1＋詳情頁接線（靜態） ============ */
(function(){
  eval(setup());
  const g = JSON.parse(JSON.stringify(findGig('gig_1990_film_101')));
  const card = gigCardHtml(g, {});
  ok('card: 有名製作卡冇主演行／冇陣容／冇代言欄 (POSTER90＋§6.1)', card.indexOf('主演：')<0 && card.indexOf('已公布陣容')<0 && card.indexOf('代言人')<0 && card.indexOf('lead-star')<0);
  const e = JSON.parse(JSON.stringify(findGig('gig_1990_ad_101')));
  ok('card: 廣告卡一樣唔出分流欄', gigCardHtml(e, {}).indexOf('代言人')<0 && gigCardHtml(e, {}).indexOf('適合性別')<0);
  const di = html.indexOf('function castingNoticeDetailHtml');
  const dj = html.indexOf('\nfunction ', di + 100);
  const detail = html.slice(di, dj);
  ok('detail wiring: 模板有插 ${castRows252}', detail.indexOf('${castRows252}')>=0);
  ok('detail wiring: 順序 weeklyRow117（檔期段）→ producerLine → castRows252（製作段）（v424 分段次序）',
    detail.indexOf('${weeklyRow117}') < detail.indexOf('${producerLine}') && detail.indexOf('${producerLine}') < detail.indexOf('${castRows252}'));
  ok('detail wiring: 唔出舊主演行字面（POSTER90）', detail.indexOf('<span class="k">主演</span>')<0);
  ok('detail wiring: 導演行已收窄到電影／電視作品', detail.indexOf('directorType252')>=0 && detail.indexOf('g.category === "作品"')>=0);
  ok('detail wiring: 臨記簡介用 blurb', detail.indexOf('g.category === "臨記通告" && g.blurb')>=0);
})();

if(fails.length){ console.log('FAILURES:', fails.join(' | ')); process.exit(1); }
console.log('ALL PASS');
