// v20a212 頒獎禮逐格流程修復・邏輯測試：
// (B1) 同一晚同一人同一作品唔可以贏兩格——後面嘅格排除已贏組合（星＋作品 key），
//      揀嗰格第一位未贏過嘅提名人；全格都贏過／得一位提名人就 fallback 沿用 fellows[0]（唔死局）。
//      玩家格 won（得主係阿偉）唔入 used；玩家格 nominated 嘅 winner63 係正規賽果（結果卡／
//      報紙／log 都讀 pack.categories），唔喺呢度改，但預先登記，等其他格避開佢。
//      懸念句輪換（三句循環，第一格沿用「得獎者是……」），時長唔郁。
//      fellows 池本身唔郁（淨係改得主揀選）。
// 反證：對 pristine main 行 → awards208NightCats／awards208CatRank 唔存在 → 乾淨 FAIL。
// 用法：node tests/test_awards212_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
const ASSERT_NAMES = [
  'B1 film gallery：4 格得主組合全部唔同（星＋作品）',
  'B1 film gallery：首格得主＝fellows[0]（陸柏言《歲歲平安》）',
  'B1 film gallery：後格得主係嗰格未贏過嗰位（女配鍾楚凝／女主蘇芷茵／男主廖炳星）',
  'B1 music gallery：3 格得主組合全部唔同',
  'B1 退化 fallback：全格同一組合 → 唔 crash、沿用 fellows[0]',
  'B1 預先登記：玩家格 winner63 组合唔會俾前面嘅格贏走，玩家格得主照舊 winner63',
  'B1 玩家格 won：focus winner null（得主係阿偉），其他格照去重',
  'B1 懸念句輪換：4 格唔係同一句，第一格沿用「得獎者是……」',
  'B1 懸念輪換唔改時長：suspense 全部 1400ms、成晚總秒數照舊 50850',
  'B1 揭曉文案跟去重後得主（女主格唔再係陸柏言）',
  'B1 fellows 池本身唔郁：每格 fellows 順序不變（首位照舊）'
];
function cleanFailMissing(what){
  console.log('抽唔到 ' + what + '（呢個版本冇 v20a208／v20a212）：以下斷言全部 FAIL');
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
for(const f of ['awards208CatRank','awards208NightCats','awards208NomineeSlotIdx','awards62CeremonyBeats','awards63FocusCat'])
  eval(extractFn(f));

/* ---- 世界 stub（貼近真實數據：男池／女池分流，同一人同一作品會跨格重複） ---- */
var TABLE212 = {
  award_harbour_film: [
    { id:'cat_film_lead_m', label:'最佳男主角', role:'lead', gender:'m' },
    { id:'cat_film_lead_f', label:'最佳女主角', role:'lead', gender:'f' },
    { id:'cat_film_support_m', label:'最佳男配角', role:'support', gender:'m' },
    { id:'cat_film_support_f', label:'最佳女配角', role:'support', gender:'f' }
  ],
  award_golddisc_music: [
    { id:'cat_music_singer_m', label:'最佳男歌手', role:'singer', gender:'m' },
    { id:'cat_music_singer_f', label:'最佳女歌手', role:'singer', gender:'f' },
    { id:'cat_music_newcomer', label:'最佳新人獎', role:'newcomer', gender:'' }
  ],
  award_probe_same: [
    { id:'cat_same_a', label:'最佳男配角', role:'support', gender:'m' },
    { id:'cat_same_b', label:'最佳男主角', role:'lead', gender:'m' }
  ]
};
var MALE212 = [
  { starId:'luk_baakyin', star:'陸柏言', title:'歲歲平安', gigId:'g1', poster:'', assigned:false },
  { starId:'liu_bingxing', star:'廖炳星', title:'三年', gigId:'g2', poster:'', assigned:false },
  { starId:'mak_zhendong', star:'麥震東', title:'海傍詭影', gigId:'g3', poster:'', assigned:false }
];
var FEMALE212 = [
  { starId:'chung_choning', star:'鍾楚凝', title:'凶樓夜半怪談', gigId:'g4', poster:'', assigned:false },
  { starId:'so_jiyan', star:'蘇芷茵', title:'春日新潮時裝特輯', gigId:'g5', poster:'', assigned:false },
  { starId:'shum_yingsuet', star:'沈映雪', title:'夜雨心聲', gigId:'g6', poster:'', assigned:false }
];
var awardsMvpCategories = function(id){ return (TABLE212[id] || []).slice(); };
var awardsCeremonyById = function(id){
  var m = 'film';
  if(/music/.test(id)) m = 'music';
  return { id:id, medium:m, matchTypes:['電影'] };
};
var awards63Fellows = function(ceremony, year, gender, catId){
  if(/^cat_same/.test(catId || '')){
    const one = { starId:'luk_baakyin', star:'陸柏言', title:'歲歲平安', gigId:'g1', poster:'', assigned:false };
    return [Object.assign({}, one), Object.assign({}, one), Object.assign({}, one)];
  }
  if(gender === 'f') return FEMALE212.map(f=> Object.assign({}, f));
  if(gender === 'm') return MALE212.map(f=> Object.assign({}, f));
  return [Object.assign({}, MALE212[1]), Object.assign({}, { starId:'lan_ruoxi', star:'藍若曦', title:'三年', gigId:'g7', poster:'', assigned:false }), Object.assign({}, FEMALE212[2])];
};
var iconHtml112 = function(){ return ''; };
var poster59Path = function(gid){ return gid === 'gig_rep' ? 'data:poster:rep' : ''; };
var venue99ForCeremony = function(){ return ''; };

function packFilm212(outcome, focusId){
  const pool = (focusId === 'cat_film_lead_f' || focusId === 'cat_film_support_f') ? FEMALE212 : MALE212;
  return { ceremonyId:'award_harbour_film', year:1990, medium:'film', displayName:'維港影藝獎',
    bestOutcome: outcome, repWork62:'夜海鎗火', repGigId63:'gig_rep', venue99:'',
    categories:[{ id:focusId, label:'最佳男主角', outcome: outcome, repWorkTitle:'夜海鎗火',
      fellows63: pool.map(f=> Object.assign({}, f)), winner63: (outcome === 'nominated' ? Object.assign({}, pool[0]) : null) }] };
}
function beatsOfCat(beats, catId){ return beats.filter(b=> b.catId === catId); }
function winKey(n){ return (n.winner && n.winner.star || '') + '《' + (n.winner && n.winner.title || '') + '》'; }

/* ---- B1：film gallery（categories 空，無 focus，唔使預先登記） ---- */
const nightGal = awards208NightCats({ ceremonyId:'award_harbour_film', year:1990, medium:'film',
  displayName:'維港影藝獎', bestOutcome:'gallery', repWork62:'', repGigId63:'', venue99:'', categories:[] });
const keysGal = nightGal.map(winKey);
ok('B1 film gallery：4 格得主組合全部唔同（星＋作品）', new Set(keysGal).size === 4);
ok('B1 film gallery：首格得主＝fellows[0]（陸柏言《歲歲平安》）',
  winKey(nightGal[0]) === '陸柏言《歲歲平安》');
ok('B1 film gallery：後格得主係嗰格未贏過嗰位（女配鍾楚凝／女主蘇芷茵／男主廖炳星）',
  winKey(nightGal[1]) === '鍾楚凝《凶樓夜半怪談》' &&
  winKey(nightGal[2]) === '蘇芷茵《春日新潮時裝特輯》' &&
  winKey(nightGal[3]) === '廖炳星《三年》');
ok('B1 fellows 池本身唔郁：每格 fellows 順序不變（首位照舊）',
  nightGal[0].fellows[0].star === '陸柏言' && nightGal[0].fellows[1].star === '廖炳星' &&
  nightGal[1].fellows[0].star === '鍾楚凝' && nightGal[1].fellows[1].star === '蘇芷茵' &&
  nightGal.every(n=> n.fellows.length === 3));

/* ---- B1：music gallery ---- */
const nightMus = awards208NightCats({ ceremonyId:'award_golddisc_music', year:1991, medium:'music',
  displayName:'星河金碟夜', bestOutcome:'gallery', repWork62:'', repGigId63:'', venue99:'', categories:[] });
ok('B1 music gallery：3 格得主組合全部唔同',
  new Set(nightMus.map(winKey)).size === 3 && nightMus.every(n=> n.winner && n.winner.star));

/* ---- B1：退化 fallback（全格同一組合） ---- */
let sameOk = false;
try{
  const nightSame = awards208NightCats({ ceremonyId:'award_probe_same', year:1990, medium:'film',
    displayName:'探針獎', bestOutcome:'gallery', repWork62:'', repGigId63:'', venue99:'', categories:[] });
  const beatsSame = awards62CeremonyBeats({ ceremonyId:'award_probe_same', year:1990, medium:'film',
    displayName:'探針獎', bestOutcome:'gallery', repWork62:'', repGigId63:'', venue99:'', categories:[] });
  sameOk = nightSame.length === 2 && nightSame.every(n=> n.winner && winKey(n) === '陸柏言《歲歲平安》') &&
    beatsOfCat(beatsSame, 'cat_same_b').find(b=>b.id === 'reveal') &&
    /陸柏言憑《歲歲平安》得獎/.test(beatsOfCat(beatsSame, 'cat_same_b').find(b=>b.id === 'reveal').caption);
}catch(_e){ sameOk = false; }
ok('B1 退化 fallback：全格同一組合 → 唔 crash、沿用 fellows[0]', sameOk);

/* ---- B1：預先登記（focus nominated winner63＝男池首位，男配格早過玩家格） ---- */
const nightNom = awards208NightCats(packFilm212('nominated', 'cat_film_lead_m'));
ok('B1 預先登記：玩家格 winner63 组合唔會俾前面嘅格贏走，玩家格得主照舊 winner63',
  winKey(nightNom[0]) === '廖炳星《三年》' && /* 男配格避開預先登記嘅陸柏言《歲歲平安》 */
  winKey(nightNom[3]) === '陸柏言《歲歲平安》' && /* 玩家格（男主）得主照舊 winner63 */
  nightNom.slice(0, 3).every(n=> winKey(n) !== '陸柏言《歲歲平安》'));

/* ---- B1：玩家格 won ---- */
const nightWon = awards208NightCats(packFilm212('won', 'cat_film_lead_m'));
ok('B1 玩家格 won：focus winner null（得主係阿偉），其他格照去重',
  nightWon[3].winner === null && new Set(nightWon.slice(0, 3).map(winKey)).size === 3);

/* ---- B1：懸念句輪換＋時長唔郁 ---- */
const beatsNom = awards62CeremonyBeats(packFilm212('nominated', 'cat_film_lead_m'));
const susCaps = beatsNom.filter(b=>b.id === 'suspense').map(b=>b.caption);
ok('B1 懸念句輪換：4 格唔係同一句，第一格沿用「得獎者是……」',
  susCaps.length === 4 && new Set(susCaps).size === 3 && susCaps[0] === '得獎者是……' &&
  susCaps.join('|') === '得獎者是……|今晚呢個獎，屬於……|結果揭曉——得獎者是……|得獎者是……');
ok('B1 懸念輪換唔改時長：suspense 全部 1400ms、成晚總秒數照舊 50850',
  beatsNom.filter(b=>b.id === 'suspense').every(b=>b.ms === 1400) &&
  beatsNom.reduce((a, b)=> a + b.ms, 0) === 50850);

/* ---- B1：揭曉文案跟去重後得主 ---- */
const beatsGal = awards62CeremonyBeats({ ceremonyId:'award_harbour_film', year:1990, medium:'film',
  displayName:'維港影藝獎', bestOutcome:'gallery', repWork62:'', repGigId63:'', venue99:'', categories:[] });
ok('B1 揭曉文案跟去重後得主（女主格唔再係陸柏言）',
  /鍾楚凝憑《凶樓夜半怪談》得獎/.test(beatsOfCat(beatsGal, 'cat_film_support_f').find(b=>b.id === 'reveal').caption) &&
  /廖炳星憑《三年》得獎/.test(beatsOfCat(beatsGal, 'cat_film_lead_m').find(b=>b.id === 'reveal').caption));

console.log('');
console.log(fails.length ? ('FAILED: '+fails.length+' -> '+fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
