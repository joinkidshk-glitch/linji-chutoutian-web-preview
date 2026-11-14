// v20a204 補女星入獎池＋提名人性別分流・邏輯測試：
// (1) 池：music 2 女／5、film 2 女／7；女星總數 4→7；新三位權重 ×3；舊 10 星權重／池位不變。
// (2) 名→id 反查：awards63StarName(新 id) 出返中文名（提名行／結果卡／報紙顯示用）。
// (3) 第一輪真主演按性別分流；第二輪池抽按性別過濾。
// (4) 女獎唔入高俊傑（男）；新人獎（gender ""）混合唔過濾。
// (5) 舊 signature（唔傳 gender）行為不變（同一 seed、同一抽籤結果）；每類別 (gender, catId) 可重現。
// (6) 過濾後池空／零候選 → fellows＝[]，唔 crash。
// 反證：對 pristine main (v20a193) 行 → AWARDS204_FEMALE_STARS／新池員唔存在 → 乾淨 FAIL。
// 用法：node tests/test_awards204_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
/* 反證要乾淨 FAIL 唔 crash：抽唔到 const／fn（pristine）嗰陣逐項印 FAIL 就 exit 1。 */
const ASSERT_NAMES = [
  '音樂池 5 人、2 女（藍若曦＋沈映雪）','電影池 7 人、2 女（魏詠男＋江詩盈）',
  '電視池 4 人 2 女、廣告池 5 人 3 女不變','女性 id 集齊 7 位','新三位權重 ×3','舊 10 星權重不變',
  '權重表齊晒池內 13 星','性別判定：7 女 → f，其餘 → m',
  '新星名反查啱（提名行／結果卡／報紙顯示用）','POSTER59_STAR_IDS 有齊 3 個新名→id',
  '女獎第一輪：只出女星（蘇芷茵＋鍾楚凝），唔出男星','男獎第一輪：只出男星（陸柏言＋廖炳星＋麥震東）',
  '女歌手第二輪：全女、只喺音樂女池出（藍若曦／沈映雪）','男歌手第二輪：全男、只喺音樂男池出',
  '女主角第二輪：全女、只喺電影女池出（魏詠男／江詩盈）','女獎掃描 96 組合零高俊傑',
  '新人獎（gender ""）混合：掃描見齊男女','舊 signature（唔傳 gender）＝傳 ""（同一結果）',
  '舊 signature 第二輪抽籤不變（1991 音樂同一結果）','舊 signature 兩次呼叫一致（seeded 可重現）',
  '同類別兩次呼叫一致（(gender, catId) 可重現）','男主角格同男配角格唔共用同一序列（seed 含 catId）',
  '男獎類別 fellows 全男＋上限 3','女獎遇着全男主演＋零無主演作品 → fellows=[]，唔 crash',
  '過濾後池抽乾：awards63WeightedPick 返 ""'
];
function cleanFailMissing(what){
  console.log('抽唔到 ' + what + '（呢個版本冇 v20a204）：以下斷言全部 FAIL');
  ASSERT_NAMES.forEach(n=>{ console.log('FAIL ' + n); fails.push(n); });
  console.log('\nFAILED: ' + fails.length);
  process.exit(1);
}
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) cleanFailMissing('function ' + name);
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){
    if(html[j]==='{') depth++;
    else if(html[j]==='}'){ depth--; if(depth===0) break; }
  }
  return html.slice(i, j+1);
}
function extractConst(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) cleanFailMissing('const ' + name);
  let depth = 0, started = false;
  for(let k=i; k<html.length; k++){
    const ch = html[k];
    if(ch==='{'||ch==='['){ depth++; started = true; }
    else if(ch==='}'||ch===']'){ depth--; if(started && depth===0) return html.slice(i, k+1)+';'; }
    else if(ch===';' && !started) return html.slice(i, k+1);
  }
  cleanFailMissing('const ' + name + ' 結尾');
}

/* ---- 世界 stub ---- */
var window = {};
for(const c of ['POSTER59_STAR_IDS','AWARDS63_POOL','AWARDS63_TIER_WEIGHT','AWARDS204_FEMALE_STARS'])
  eval(extractConst(c).replace('const '+c+' =', 'var '+c+' ='));
for(const f of ['awards204StarGender','awards63StarName','awards63AllGigs','awards63GigYear','awards63GigPay',
  'awards63KeySeed','awards63SeededRng','awards63WeightedPick','awards63Fellows'])
  eval(extractFn(f));

var TEST_STAR = {
  gig_1988_film_harbour_high: '陸柏言',
  gig_1988_film_cotton_spring_high: '廖炳星',
  gig_1988_film_cotton_winter_low: '蘇芷茵',
  gig_1988_film_cotton_spring_mid: '鍾楚凝',
  gig_1988_film_03: '麥震東',
  gig_1988_rec_star_spring: '廖炳星',
  gig_1988_rec_hk_autumn: '蘇芷茵'
};
var GIGS = [
  { id:'gig_1988_film_harbour_high',       type:'電影',   pay:[40000,48000], workTitle:'夜海鎗火' },
  { id:'gig_1988_film_cotton_spring_high', type:'電影',   pay:[35000,41900], workTitle:'詭校夜話' },
  { id:'gig_1988_film_cotton_winter_low',  type:'電影',   pay:[30000,36000], workTitle:'冬夜情書' },
  { id:'gig_1988_film_cotton_spring_mid',  type:'電影',   pay:[25000,30000], workTitle:'胭脂扣影' },
  { id:'gig_1988_film_03',                 type:'電影',   pay:[8000,10500],  workTitle:'神探闖天關' },
  { id:'gig_1988_rec_star_spring',         type:'唱片通告', pay:[20000,25000], workTitle:'星夜唱片' },
  { id:'gig_1988_rec_hk_autumn',           type:'唱片通告', pay:[15000,18000], workTitle:'秋意歌集' },
  { id:'gig_1989_film_a',                  type:'電影',   pay:[16000,20000], workTitle:'九龍夜行' },
  { id:'gig_1989_film_b',                  type:'電影',   pay:[9000,12000],  workTitle:'霓裳夜冷' },
  { id:'gig_1989_film_c',                  type:'電影',   pay:[7000,9000],   workTitle:'半島槍聲' },
  { id:'gig_1989_rec_a',                   type:'唱片通告', pay:[12000,15000], workTitle:'心曲集' },
  { id:'gig_1989_rec_b',                   type:'唱片通告', pay:[8000,10000],  workTitle:'夜歌集' },
  { id:'gig_1989_rec_c',                   type:'唱片通告', pay:[5000,7000],   workTitle:'晨歌集' }
];
var S = { wrapHistory: [] };
var leadStar59Of = function(g){ return (g && TEST_STAR[g.id]) || ''; };
var poster59Path = function(gid){ return ''; };
var work59WorkOf = function(h, g){ return (g && (g.workTitle || g.title)) || ''; };

const CER_FILM = { id:'award_harbour_film', medium:'film', matchTypes:['電影'] };
const CER_MUSIC = { id:'award_golddisc_music', medium:'music', matchTypes:['唱片通告'] };
const isF = (sid)=> !!AWARDS204_FEMALE_STARS[sid];
const FEMALE7 = ['so_jiyan','chung_choning','ngai_wingnaam','yip_manji','lan_ruoxi','shum_yingsuet','kong_siying'];

/* ---- (1) 池組成＋權重 ---- */
ok('音樂池 5 人、2 女（藍若曦＋沈映雪）', AWARDS63_POOL.music.length === 5 &&
  AWARDS63_POOL.music.filter(isF).sort().join(',') === 'lan_ruoxi,shum_yingsuet');
ok('電影池 7 人、2 女（魏詠男＋江詩盈）', AWARDS63_POOL.film.length === 7 &&
  AWARDS63_POOL.film.filter(isF).sort().join(',') === 'kong_siying,ngai_wingnaam');
ok('電視池 4 人 2 女、廣告池 5 人 3 女不變', AWARDS63_POOL.tv.length === 4 && AWARDS63_POOL.tv.filter(isF).length === 2 &&
  AWARDS63_POOL.ad.length === 5 && AWARDS63_POOL.ad.filter(isF).length === 3);
ok('女性 id 集齊 7 位', Object.keys(AWARDS204_FEMALE_STARS).sort().join(',') === FEMALE7.slice().sort().join(','));
ok('新三位權重 ×3', AWARDS63_TIER_WEIGHT.lan_ruoxi === 3 && AWARDS63_TIER_WEIGHT.shum_yingsuet === 3 && AWARDS63_TIER_WEIGHT.kong_siying === 3);
ok('舊 10 星權重不變', AWARDS63_TIER_WEIGHT.luk_baakyin === 3 && AWARDS63_TIER_WEIGHT.so_jiyan === 3 &&
  AWARDS63_TIER_WEIGHT.liu_bingxing === 3 && AWARDS63_TIER_WEIGHT.lok_gasing === 3 && AWARDS63_TIER_WEIGHT.yip_manji === 3 &&
  AWARDS63_TIER_WEIGHT.mak_zhendong === 2 && AWARDS63_TIER_WEIGHT.chai_zanhoi === 2 && AWARDS63_TIER_WEIGHT.chung_choning === 2 &&
  AWARDS63_TIER_WEIGHT.ngai_wingnaam === 1 && AWARDS63_TIER_WEIGHT.gu_mingfai === 1);
ok('權重表齊晒池內 13 星', Object.values(AWARDS63_POOL).flat().every(id=>AWARDS63_TIER_WEIGHT[id] != null));
ok('性別判定：7 女 → f，其餘 → m', FEMALE7.every(id=>awards204StarGender(id) === 'f') &&
  ['luk_baakyin','liu_bingxing','mak_zhendong','chai_zanhoi','lok_gasing','gu_mingfai','ko_chunkit'].every(id=>awards204StarGender(id) === 'm'));

/* ---- (2) 名牌反查 ---- */
ok('新星名反查啱（提名行／結果卡／報紙顯示用）', awards63StarName('lan_ruoxi') === '藍若曦' &&
  awards63StarName('shum_yingsuet') === '沈映雪' && awards63StarName('kong_siying') === '江詩盈');
ok('POSTER59_STAR_IDS 有齊 3 個新名→id', POSTER59_STAR_IDS['藍若曦'] === 'lan_ruoxi' &&
  POSTER59_STAR_IDS['沈映雪'] === 'shum_yingsuet' && POSTER59_STAR_IDS['江詩盈'] === 'kong_siying');

/* ---- (3) 第一輪分流（1990 電影：真主演按片酬序） ---- */
S.wrapHistory = [];
const flF = awards63Fellows(CER_FILM, 1990, 'f');
ok('女獎第一輪：只出女星（蘇芷茵＋鍾楚凝），唔出男星', flF.length === 2 &&
  flF.every(f=>isF(f.starId)) && flF[0].star === '蘇芷茵' && flF[1].star === '鍾楚凝');
const flM = awards63Fellows(CER_FILM, 1990, 'm');
ok('男獎第一輪：只出男星（陸柏言＋廖炳星＋麥震東）', flM.length === 3 &&
  flM.every(f=>!isF(f.starId)) && flM[0].star === '陸柏言' && flM[1].star === '廖炳星' && flM[2].star === '麥震東');

/* ---- (3b) 第二輪分流（1991：冇主演作品，池兜底） ---- */
const flMusF = awards63Fellows(CER_MUSIC, 1991, 'f');
ok('女歌手第二輪：全女、只喺音樂女池出（藍若曦／沈映雪）', flMusF.length === 2 &&
  flMusF.every(f=>isF(f.starId) && ['lan_ruoxi','shum_yingsuet'].indexOf(f.starId) >= 0) &&
  new Set(flMusF.map(f=>f.starId)).size === flMusF.length);
const flMusM = awards63Fellows(CER_MUSIC, 1991, 'm');
ok('男歌手第二輪：全男、只喺音樂男池出', flMusM.length === 3 &&
  flMusM.every(f=>!isF(f.starId) && ['lok_gasing','gu_mingfai','liu_bingxing'].indexOf(f.starId) >= 0));
const flFilmF = awards63Fellows(CER_FILM, 1991, 'f');
ok('女主角第二輪：全女、只喺電影女池出（魏詠男／江詩盈）', flFilmF.length === 2 &&
  flFilmF.every(f=>isF(f.starId) && ['ngai_wingnaam','kong_siying'].indexOf(f.starId) >= 0));

/* ---- (4) 女獎唔入高俊傑；新人獎混合 ---- */
let koInF = 0, koSweep = 0;
for(const y of [1991, 1992]) for(let i = 0; i < 24; i++){
  for(const cer of [CER_FILM, CER_MUSIC]){
    const fl = awards63Fellows({ id:'award_probe_'+i, medium:cer.medium, matchTypes:cer.matchTypes }, y, 'f');
    koSweep++;
    if(fl.some(f=>f.starId === 'ko_chunkit')) koInF++;
  }
}
ok('女獎掃描 '+koSweep+' 組合零高俊傑', koInF === 0);
let seenF = false, seenM = false;
for(let i = 0; i < 24; i++){
  const fl = awards63Fellows({ id:'award_probe_'+i, medium:'film', matchTypes:['電影'] }, 1991, '');
  fl.forEach(f=>{ if(isF(f.starId)) seenF = true; else seenM = true; });
}
ok('新人獎（gender ""）混合：掃描見齊男女', seenF && seenM);

/* ---- (5) 舊 signature 行為不變＋每類別可重現 ---- */
const oldFilm = awards63Fellows(CER_FILM, 1990);
const oldFilmEmpty = awards63Fellows(CER_FILM, 1990, '');
ok('舊 signature（唔傳 gender）＝傳 ""（同一結果）', JSON.stringify(oldFilm) === JSON.stringify(oldFilmEmpty));
const oldMus91 = awards63Fellows(CER_MUSIC, 1991);
ok('舊 signature 第二輪抽籤不變（1991 音樂同一結果）', JSON.stringify(oldMus91) === JSON.stringify(awards63Fellows(CER_MUSIC, 1991, '')));
ok('舊 signature 兩次呼叫一致（seeded 可重現）', JSON.stringify(awards63Fellows(CER_FILM, 1991)) === JSON.stringify(awards63Fellows(CER_FILM, 1991)));
const catA1 = awards63Fellows(CER_FILM, 1991, 'm', 'cat_film_lead_m');
const catA2 = awards63Fellows(CER_FILM, 1991, 'm', 'cat_film_lead_m');
const catB = awards63Fellows(CER_FILM, 1991, 'm', 'cat_film_support_m');
ok('同類別兩次呼叫一致（(gender, catId) 可重現）', JSON.stringify(catA1) === JSON.stringify(catA2));
ok('男主角格同男配角格唔共用同一序列（seed 含 catId）', JSON.stringify(catA1) !== JSON.stringify(catB) ||
  JSON.stringify(awards63Fellows(CER_MUSIC, 1991, 'm', 'cat_music_singer_m')) !== JSON.stringify(awards63Fellows(CER_MUSIC, 1991, 'm', 'cat_music_newcomer')));
ok('男獎類別 fellows 全男＋上限 3', catA1.length <= 3 && catA1.every(f=>!isF(f.starId)) &&
  catB.length <= 3 && catB.every(f=>!isF(f.starId)));

/* ---- (6) 過濾後零候選 → []，唔 crash ---- */
const savedGigs = GIGS;
GIGS = [
  { id:'gig_1988_film_harbour_high', type:'電影', pay:[40000,48000], workTitle:'夜海鎗火' },
  { id:'gig_1988_film_cotton_spring_high', type:'電影', pay:[35000,41900], workTitle:'詭校夜話' }
];
let emptyOk = false, emptyRes = null;
try{ emptyRes = awards63Fellows(CER_FILM, 1990, 'f'); emptyOk = Array.isArray(emptyRes) && emptyRes.length === 0; }catch(_e){ emptyOk = false; }
ok('女獎遇着全男主演＋零無主演作品 → fellows=[]，唔 crash', emptyOk);
GIGS = savedGigs;
ok('過濾後池抽乾：awards63WeightedPick 返 ""', awards63WeightedPick(['lan_ruoxi','shum_yingsuet'], { lan_ruoxi:true, shum_yingsuet:true }, awards63SeededRng(1)) === '');

console.log('');
console.log(fails.length ? ('FAILED: '+fails.length+' -> '+fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
