// v20a204 補女星入獎池＋提名人性別分流・邏輯測試（v20a252 D-v2-2／D-v2-3 cast 模型重寫）：
// (1) 女性 id 集 9 位（舊 7 位＋胡美琳／韓秀婷，F1 新星）；性別判定經 AWARDS204_FEMALE_STARS。
// (2) 名→id 反查：awards63StarName(新 id) 出返中文名（提名行／結果卡／報紙顯示用）。
// (3) 第一輪真陣容按 cast 格分流（leadM／leadF／supportM／supportF／singer／host）；
//     女獎只出女星、男獎只出男星；唱片讀 singer＋singerGender；新人獎混合；
//     最佳司儀讀 host（玩家主持嗰格 host 寫 null，唔產生對手）。
// (4) 高俊傑／程天諾永遠唔入（唔喺 POSTER59_STAR_IDS，冇 sprite）；唔夠 3 個唔兜底。
// (5) 舊 signature（唔傳 gender）行為不變（同一結果）；每類別 (gender, catId) 可重現
//     （確定性，唔靠 seed——seeded draw 已刪）。
// (6) 過濾後零候選 → fellows＝[]，唔 crash；無 cast／無 singer 嘅作品唔產生對手。
// 反證：對 pristine main (v20a193) 行 → AWARDS204_FEMALE_STARS／新池員唔存在 → 乾淨 FAIL。
// v20a229 B3：fixture id 由舊曆 gig_1988_／gig_1989_ 改做新庫格式 gig_1990_／gig_1991_＋year 欄（YearOf 唔再 +2，舊 id 會對唔上年份）；TEST_STAR／片酬／期望不變。
// 用法：node tests/test_awards204_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
/* 反證要乾淨 FAIL 唔 crash：抽唔到 const／fn（pristine）嗰陣逐項印 FAIL 就 exit 1。 */
const ASSERT_NAMES = [
  '女性 id 集齊 9 位','性別判定：9 女 → f，其餘 → m',
  '新星名反查啱（提名行／結果卡／報紙顯示用）','POSTER59_STAR_IDS 有齊 5 個新名→id',
  '女主角格：只出女星（蘇芷茵＋魏詠男＋藍若曦）','男主角格：只出男星（陸柏言＋麥震東＋顧明輝）',
  '配角格唔同主角格（support_m／support_f 各 3 位）',
  '女歌手格：全女（蘇芷茵＋沈映雪，唔夠 3 個回 2 個）','男歌手格：全男（駱家聲，得 1 個回 1 個）',
  '新人獎（gender ""）混合：男女齊','最佳司儀格讀 host（彭少祺＋顧明輝，唔計玩家主持／程天諾）',
  '女獎掃描零高俊傑／零程天諾','舊 signature（唔傳 gender）＝傳 ""（同一結果）',
  '舊 signature 兩次呼叫一致（確定性，唔靠 seed）',
  '同類別兩次呼叫一致（(gender, catId) 可重現）',
  '唔夠 3 個唔兜底：1991 電影 lead_m 零候選 → []',
  '男獎類別 fellows 全男＋上限 3','女獎遇着全男主演＋零無主演作品 → fellows=[]，唔 crash',
  '無 cast／無 singer 嘅作品唔產生對手',
  'fellows 唔用池抽／權重／seeded draw／高俊傑名額'
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

/* ---- 世界 stub（cast 模型：fixture 自帶 cast／singer／host） ---- */
var window = {};
for(const c of ['POSTER59_STAR_IDS','AWARDS188_CATEGORIES','AWARDS204_FEMALE_STARS'])
  eval(extractConst(c).replace('const '+c+' =', 'var '+c+' ='));
for(const f of ['awards204StarGender','awards63StarName','awards63AllGigs','awards63GigYear','awards63GigPay',
  'awards63CatSlot','awards63HasSprite','awards63Fellows','poster59Path'])
  eval(extractFn(f));

var NO_CAST = { leadM:null, leadF:null, supportM:null, supportF:null };
var GIGS = [
  { id:'gig_1990_film_301', type:'電影', year:1990, pay:[40000,48000], workTitle:'夜海鎗火',
    cast:{ leadM:'luk_baakyin', leadF:'so_jiyan', supportM:'liu_bingxing', supportF:'chung_choning' } },
  { id:'gig_1990_film_302', type:'電影', year:1990, pay:[35000,41900], workTitle:'詭校夜話',
    cast:{ leadM:'mak_zhendong', leadF:'ngai_wingnaam', supportM:'chai_zanhoi', supportF:'yip_manji' } },
  { id:'gig_1990_film_303', type:'電影', year:1990, pay:[30000,36000], workTitle:'冬夜情書',
    cast:{ leadM:'gu_mingfai', leadF:'lan_ruoxi', supportM:'lok_gasing', supportF:'shum_yingsuet' } },
  { id:'gig_1990_film_304', type:'電影', year:1990, pay:[25000,30000], workTitle:'胭脂扣影',
    cast:{ leadM:'chai_zanhoi', leadF:'kong_siying', supportM:'luk_baakyin', supportF:'hon_sauting' } },
  { id:'gig_1990_film_305', type:'電影', year:1990, pay:[8000,10500], workTitle:'神探闖天關',
    cast:{ leadM:null, leadF:null, supportM:null, supportF:null } },
  { id:'gig_1990_rec_301', type:'唱片通告', year:1990, pay:[20000,25000], workTitle:'星夜唱片',
    singer:'lok_gasing', singerGender:'m' },
  { id:'gig_1990_rec_302', type:'唱片通告', year:1990, pay:[15000,18000], workTitle:'秋意歌集',
    singer:'so_jiyan', singerGender:'f' },
  { id:'gig_1990_rec_303', type:'唱片通告', year:1990, pay:[12000,15000], workTitle:'心曲集',
    singer:'shum_yingsuet', singerGender:'f' },
  { id:'gig_1991_film_301', type:'電影', year:1991, pay:[16000,20000], workTitle:'九龍夜行', cast:NO_CAST },
  { id:'gig_1991_film_302', type:'電影', year:1991, pay:[9000,12000], workTitle:'霓裳夜冷', cast:NO_CAST },
  { id:'gig_1991_film_303', type:'電影', year:1991, pay:[7000,9000], workTitle:'半島槍聲', cast:NO_CAST },
  { id:'gig_1991_rec_301', type:'唱片通告', year:1991, pay:[12000,15000], workTitle:'心曲集',
    singer:'lan_ruoxi', singerGender:'f' },
  { id:'gig_1991_rec_302', type:'唱片通告', year:1991, pay:[8000,10000], workTitle:'夜歌集',
    singer:'gu_mingfai', singerGender:'m' },
  { id:'gig_1991_rec_303', type:'唱片通告', year:1991, pay:[5000,7000], workTitle:'晨歌集',
    singer:'hon_sauting', singerGender:'f' },
  { id:'gig_1990_variety_301', type:'綜藝', year:1990, pay:[9000,11000], workTitle:'星聲歌唱大賽',
    host:'pang_siuki', guests:['lok_gasing'] },
  { id:'gig_1990_variety_302', type:'綜藝', year:1990, pay:[8000,10000], workTitle:'清談今宵',
    host:'gu_mingfai', guests:['chung_choning'] },
  { id:'gig_1990_variety_303', type:'綜藝', year:1990, pay:[7000,9000], workTitle:'玩家主持之夜',
    host:null, roleLabel:'主持', guests:['so_jiyan'] },
  { id:'gig_1990_variety_304', type:'綜藝', year:1990, pay:[6000,8000], workTitle:'神秘嘉賓夜',
    host:'ching_tinlok', guests:['liu_bingxing'] }
];
var S = { wrapHistory: [] };
var work59WorkOf = function(h, g){ return (g && (g.workTitle || g.title)) || ''; };

const CER_FILM = { id:'award_harbour_film', medium:'film', matchTypes:['電影'] };
const CER_TV = { id:'award_singho_tv', medium:'tv', matchTypes:['電視劇','綜藝'] };
const CER_MUSIC = { id:'award_golddisc_music', medium:'music', matchTypes:['唱片通告'] };
const isF = (sid)=> !!AWARDS204_FEMALE_STARS[sid];
const FEMALE9 = ['so_jiyan','chung_choning','ngai_wingnaam','yip_manji','lan_ruoxi','shum_yingsuet','kong_siying','wu_meilam','hon_sauting'];

/* ---- (1) 女性集＋性別判定 ---- */
ok('女性 id 集齊 9 位', Object.keys(AWARDS204_FEMALE_STARS).sort().join(',') === FEMALE9.slice().sort().join(','));
ok('性別判定：9 女 → f，其餘 → m', FEMALE9.every(id=>awards204StarGender(id) === 'f') &&
  ['luk_baakyin','liu_bingxing','mak_zhendong','chai_zanhoi','lok_gasing','gu_mingfai','ko_chunkit','ching_tinlok','pang_siuki'].every(id=>awards204StarGender(id) === 'm'));

/* ---- (2) 名牌反查 ---- */
ok('新星名反查啱（提名行／結果卡／報紙顯示用）', awards63StarName('lan_ruoxi') === '藍若曦' &&
  awards63StarName('shum_yingsuet') === '沈映雪' && awards63StarName('kong_siying') === '江詩盈' &&
  awards63StarName('wu_meilam') === '胡美琳' && awards63StarName('hon_sauting') === '韓秀婷');
ok('POSTER59_STAR_IDS 有齊 5 個新名→id', POSTER59_STAR_IDS['藍若曦'] === 'lan_ruoxi' &&
  POSTER59_STAR_IDS['沈映雪'] === 'shum_yingsuet' && POSTER59_STAR_IDS['江詩盈'] === 'kong_siying' &&
  POSTER59_STAR_IDS['胡美琳'] === 'wu_meilam' && POSTER59_STAR_IDS['韓秀婷'] === 'hon_sauting');

/* ---- (3) 第一輪分流（1990 電影／唱片：真陣容按片酬序） ---- */
S.wrapHistory = [];
const flF = awards63Fellows(CER_FILM, 1990, 'f', 'cat_film_lead_f');
ok('女主角格：只出女星（蘇芷茵＋魏詠男＋藍若曦）', flF.length === 3 &&
  flF.every(f=>isF(f.starId)) && flF[0].star === '蘇芷茵' && flF[1].star === '魏詠男' && flF[2].star === '藍若曦');
const flM = awards63Fellows(CER_FILM, 1990, 'm', 'cat_film_lead_m');
ok('男主角格：只出男星（陸柏言＋麥震東＋顧明輝）', flM.length === 3 &&
  flM.every(f=>!isF(f.starId)) && flM[0].star === '陸柏言' && flM[1].star === '麥震東' && flM[2].star === '顧明輝');
const flSupM = awards63Fellows(CER_FILM, 1990, 'm', 'cat_film_support_m');
const flSupF = awards63Fellows(CER_FILM, 1990, 'f', 'cat_film_support_f');
ok('配角格唔同主角格（support_m：廖炳星＋齊鎮海＋駱家聲；support_f：鍾楚凝＋葉敏芝＋沈映雪）',
  flSupM.length === 3 && flSupM[0].star === '廖炳星' && flSupM[1].star === '齊鎮海' && flSupM[2].star === '駱家聲' &&
  flSupF.length === 3 && flSupF[0].star === '鍾楚凝' && flSupF[1].star === '葉敏芝' && flSupF[2].star === '沈映雪');
const flSingF = awards63Fellows(CER_MUSIC, 1990, 'f', 'cat_music_singer_f');
ok('女歌手格：全女（蘇芷茵＋沈映雪，唔夠 3 個回 2 個）', flSingF.length === 2 &&
  flSingF.every(f=>isF(f.starId)) && flSingF[0].star === '蘇芷茵' && flSingF[1].star === '沈映雪');
const flSingM = awards63Fellows(CER_MUSIC, 1990, 'm', 'cat_music_singer_m');
ok('男歌手格：全男（駱家聲，得 1 個回 1 個）', flSingM.length === 1 &&
  flSingM[0].star === '駱家聲' && !isF(flSingM[0].starId));
const flNew = awards63Fellows(CER_MUSIC, 1990, '', 'cat_music_newcomer');
ok('新人獎（gender ""）混合：男女齊', flNew.length === 3 &&
  flNew.some(f=>isF(f.starId)) && flNew.some(f=>!isF(f.starId)));
const flHost = awards63Fellows(CER_TV, 1990, '', 'cat_tv_host');
ok('最佳司儀格讀 host（彭少祺＋顧明輝，唔計玩家主持／程天諾）', flHost.length === 2 &&
  flHost[0].star === '彭少祺' && flHost[1].star === '顧明輝' &&
  flHost.every(f=>f.starId !== 'ching_tinlok'));

/* ---- (4) 高俊傑／程天諾永遠唔入 ---- */
let badInSweep = 0, sweepN = 0;
for(const y of [1990, 1991, 1992]) for(let i = 0; i < 24; i++){
  for(const cer of [CER_FILM, CER_MUSIC, CER_TV]){
    const fl = awards63Fellows({ id:'award_probe_'+i, medium:cer.medium, matchTypes:cer.matchTypes }, y);
    sweepN++;
    if(fl.some(f=>f.starId === 'ko_chunkit' || f.starId === 'ching_tinlok')) badInSweep++;
  }
}
ok('女獎／全掃描零高俊傑／零程天諾（'+sweepN+' 組合）', badInSweep === 0);

/* ---- (5) 舊 signature 行為不變＋每類別可重現（確定性） ---- */
const oldFilm = awards63Fellows(CER_FILM, 1990);
const oldFilmEmpty = awards63Fellows(CER_FILM, 1990, '');
ok('舊 signature（唔傳 gender）＝傳 ""（同一結果）', JSON.stringify(oldFilm) === JSON.stringify(oldFilmEmpty));
ok('舊 signature 兩次呼叫一致（確定性，唔靠 seed）', JSON.stringify(awards63Fellows(CER_FILM, 1990)) === JSON.stringify(awards63Fellows(CER_FILM, 1990)));
const catA1 = awards63Fellows(CER_FILM, 1990, 'm', 'cat_film_lead_m');
const catA2 = awards63Fellows(CER_FILM, 1990, 'm', 'cat_film_lead_m');
const catB = awards63Fellows(CER_FILM, 1990, 'm', 'cat_film_support_m');
ok('同類別兩次呼叫一致（(gender, catId) 可重現）', JSON.stringify(catA1) === JSON.stringify(catA2));
ok('男獎類別 fellows 全男＋上限 3', catA1.length <= 3 && catA1.every(f=>!isF(f.starId)) &&
  catB.length <= 3 && catB.every(f=>!isF(f.starId)));

/* ---- (6) 過濾後零候選 → []，唔 crash；無 cast 唔產生對手 ---- */
const fl91LeadM = awards63Fellows(CER_FILM, 1991, 'm', 'cat_film_lead_m');
ok('唔夠 3 個唔兜底：1991 電影 lead_m 零候選 → []', Array.isArray(fl91LeadM) && fl91LeadM.length === 0);
const savedGigs = GIGS;
GIGS = [
  { id:'gig_1990_film_301', type:'電影', year:1990, pay:[40000,48000], workTitle:'夜海鎗火',
    cast:{ leadM:'luk_baakyin', leadF:null, supportM:null, supportF:null } },
  { id:'gig_1990_film_302', type:'電影', year:1990, pay:[35000,41900], workTitle:'詭校夜話',
    cast:{ leadM:'liu_bingxing', leadF:null, supportM:null, supportF:null } }
];
let emptyOk = false, emptyRes = null;
try{ emptyRes = awards63Fellows(CER_FILM, 1990, 'f', 'cat_film_lead_f'); emptyOk = Array.isArray(emptyRes) && emptyRes.length === 0; }catch(_e){ emptyOk = false; }
ok('女獎遇着全男主演＋零無主演作品 → fellows=[]，唔 crash', emptyOk);
GIGS = savedGigs;
ok('無 cast／無 singer 嘅作品唔產生對手',
  awards63Fellows(CER_FILM, 1990).every(f=>f.gigId !== 'gig_1990_film_305') &&
  awards63Fellows(CER_FILM, 1991, 'm', 'cat_film_lead_m').length === 0);
const fellowsSrc = extractFn('awards63Fellows');
ok('fellows 唔用池抽／權重／seeded draw／高俊傑名額',
  fellowsSrc.indexOf('AWARDS63_POOL') < 0 && fellowsSrc.indexOf('AWARDS63_TIER_WEIGHT') < 0 &&
  fellowsSrc.indexOf('awards63WeightedPick') < 0 && fellowsSrc.indexOf('awards63SeededRng') < 0 &&
  fellowsSrc.indexOf('Math.random') < 0 && fellowsSrc.indexOf('ko_chunkit') < 0);

console.log('');
console.log(fails.length ? ('FAILED: '+fails.length+' -> '+fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
