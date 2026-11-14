// v20a208 頒獎禮逐格宣佈・邏輯測試：
// (1) 格次序：film／tv／ad 男配角→女配角→女主角→男主角；music 新人獎→女歌手→男歌手。
// (2) beat 結構：open／out／pan／enter 成晚各一次；每格 catTitle＋逐位 nominee beats＋懸念＋揭曉；
//     舊 names 快閃 beat 消失；玩家格額外 walkup／glamour（won）／comfort（nominated）。
// (3) 每格秒數／成晚總秒數喺任務範圍（3 格約 38–45 秒、4 格約 45–55 秒）。
// (4) 非玩家格得主＝fellows[0]；玩家格揭曉文案（won／nominated）不變。
// (5) 逐位宣佈欄位：nomineeIdx／nomineeTotal／slotIdx 映射啱（玩家格阿偉喺 slot 1）。
// (6) 邊界：某格 fellows 空 → 通用提名 beat＋揭曉 fallback，唔 crash；全表空／冇 ceremonyId → 跌返舊單格。
// (7) 跳過語義：全晚一個 beats list、一個 out（finish 一次即成晚完）。
// 反證：對 pristine main 行 → awards208NightCats／awards208CatRank 唔存在 → 乾淨 FAIL。
// 用法：node tests/test_awards208_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
const ASSERT_NAMES = [
  'film 次序：男配角→女配角→女主角→男主角','tv 次序同 film 一樣','ad 次序同 film 一樣',
  'music 次序：新人獎→女歌手→男歌手','未知 role 排最後（rank 9）',
  'night film 4 格，全部有 3 位 fellows','玩家格 isFocus 啱（lead_m），其餘格唔係',
  '非玩家格 outcome gallery、得主＝fellows[0]','玩家格 nominated 得主＝winner63（陸柏言）',
  'open／out 成晚各一次','每格 1 個 catTitle，次序同 night 一致',
  '每格 nominee beats 數：玩家格 4、其他格 3','多格模式冇舊 names beat',
  '提名 beat caption 逐位「星：《作品》」，第一位係阿偉','nominee 欄位：idx／total／slotIdx 映射啱（阿偉 slot 1）',
  '非玩家格 slotIdx＝nomineeIdx','enter 1 次，喺玩家格 catTitle 之前',
  'focus 係第一格嗰陣 enter 緊接 open','玩家格 nominated：comfort 2600，冇 walkup／glamour',
  '玩家格 won：walkup 2200＋glamour 1800，冇 comfort','gallery：pan 1 次、冇 enter／walkup／glamour／comfort',
  'declined：pan 電視轉播版、成晚多格','每格秒數：非玩家格 10700ms、玩家格 nominated 15300ms',
  '成晚總秒數：film nominated 約 51 秒（45–55）','成晚總秒數：music nominated 約 40 秒（38–45）',
  '成晚總秒數：film won（有海報）約 52 秒（45–55）','揭曉 caption：非玩家格得主＝fellows[0]',
  '揭曉 caption：玩家格 nominated 有得主＋差少少','揭曉 caption：玩家格 won 有得獎＋代表作',
  'fellows 空嗰格：通用提名 beat＋揭曉 fallback，唔 crash','全表空 → 跌返舊單格（有 names beat）',
  '冇 ceremonyId → 跌返舊單格（有 names beat）','跳過語義：一個 beats list、一個 out 喺最後',
  'nominee beat 每位 2000ms','catTitle 1200／suspense 1400／reveal 2100'
];
function cleanFailMissing(what){
  console.log('抽唔到 ' + what + '（呢個版本冇 v20a208）：以下斷言全部 FAIL');
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

/* ---- 世界 stub ---- */
var TABLE208 = {
  award_harbour_film: [
    { id:'cat_film_lead_m', label:'最佳男主角', role:'lead', gender:'m' },
    { id:'cat_film_lead_f', label:'最佳女主角', role:'lead', gender:'f' },
    { id:'cat_film_support_m', label:'最佳男配角', role:'support', gender:'m' },
    { id:'cat_film_support_f', label:'最佳女配角', role:'support', gender:'f' }
  ],
  award_singho_tv: [
    { id:'cat_tv_lead_m', label:'最佳男主角', role:'lead', gender:'m' },
    { id:'cat_tv_lead_f', label:'最佳女主角', role:'lead', gender:'f' },
    { id:'cat_tv_support_m', label:'最佳男配角', role:'support', gender:'m' },
    { id:'cat_tv_support_f', label:'最佳女配角', role:'support', gender:'f' }
  ],
  award_harbour_ad: [
    { id:'cat_ad_lead_m', label:'最佳廣告男主角', role:'lead', gender:'m' },
    { id:'cat_ad_lead_f', label:'最佳廣告女主角', role:'lead', gender:'f' },
    { id:'cat_ad_support_m', label:'最佳廣告男配角', role:'support', gender:'m' },
    { id:'cat_ad_support_f', label:'最佳廣告女配角', role:'support', gender:'f' }
  ],
  award_golddisc_music: [
    { id:'cat_music_singer_m', label:'最佳男歌手', role:'singer', gender:'m' },
    { id:'cat_music_singer_f', label:'最佳女歌手', role:'singer', gender:'f' },
    { id:'cat_music_newcomer', label:'最佳新人獎', role:'newcomer', gender:'' }
  ],
  award_probe_empty: [
    { id:'cat_empty', label:'最佳男配角', role:'support', gender:'m' },
    { id:'cat_probe_lead', label:'最佳男主角', role:'lead', gender:'m' }
  ]
};
var awardsMvpCategories = function(id){ return (TABLE208[id] || []).slice(); };
var awardsCeremonyById = function(id){
  var m = 'film';
  if(/tv/.test(id)) m = 'tv'; else if(/music/.test(id)) m = 'music'; else if(/ad/.test(id)) m = 'ad';
  return { id:id, medium:m, matchTypes:['電影'] };
};
var awards63Fellows = function(ceremony, year, gender, catId){
  if(catId === 'cat_empty') return [];
  var out = [];
  for(var i = 0; i < 3; i++)
    out.push({ starId:'fx_'+catId+'_'+i, star:'星'+(i+1)+'號', title:'戲'+(i+1)+'號', gigId:'g_'+catId+'_'+i, poster:'', assigned:true });
  return out;
};
var iconHtml112 = function(){ return ''; };
var poster59Path = function(gid){ return gid === 'gig_rep' ? 'data:poster:rep' : ''; };
var venue99ForCeremony = function(){ return ''; };

const FEL_NOM = [
  { starId:'luk_baakyin', star:'陸柏言', title:'賀歲喜劇笑滿堂', gigId:'g1', poster:'', assigned:false },
  { starId:'liu_bingxing', star:'廖炳星', title:'詭校夜話', gigId:'g2', poster:'', assigned:false },
  { starId:'mak_zhendong', star:'麥震東', title:'神探闖天關', gigId:'g3', poster:'', assigned:false }
];
function packFilm(outcome, focusId){
  return { ceremonyId:'award_harbour_film', year:1990, medium:'film', displayName:'維港影藝獎',
    bestOutcome: outcome, repWork62:'夜海鎗火', repGigId63:'gig_rep', venue99:'',
    categories:[{ id:focusId, label:'最佳男主角', outcome: outcome, repWorkTitle:'夜海鎗火',
      fellows63: FEL_NOM.slice(), winner63: (outcome === 'nominated' ? FEL_NOM[0] : null) }] };
}
function beatsOfCat(beats, catId){ return beats.filter(b=> b.catId === catId); }
function totalOf(beats, ids){ return beats.filter(b=> ids.indexOf(b.id) >= 0).reduce((a, b)=> a + b.ms, 0); }

/* ---- (1) 格次序 ---- */
const nightFilm = awards208NightCats(packFilm('nominated', 'cat_film_lead_m'));
ok('film 次序：男配角→女配角→女主角→男主角',
  nightFilm.map(n=>n.id).join(',') === 'cat_film_support_m,cat_film_support_f,cat_film_lead_f,cat_film_lead_m');
const nightTv = awards208NightCats({ ceremonyId:'award_singho_tv', year:1990, medium:'tv', bestOutcome:'gallery', categories:[] });
ok('tv 次序同 film 一樣',
  nightTv.map(n=>n.id).join(',') === 'cat_tv_support_m,cat_tv_support_f,cat_tv_lead_f,cat_tv_lead_m');
const nightAd = awards208NightCats({ ceremonyId:'award_harbour_ad', year:1990, medium:'ad', bestOutcome:'gallery', categories:[] });
ok('ad 次序同 film 一樣',
  nightAd.map(n=>n.id).join(',') === 'cat_ad_support_m,cat_ad_support_f,cat_ad_lead_f,cat_ad_lead_m');
const nightMusic = awards208NightCats({ ceremonyId:'award_golddisc_music', year:1990, medium:'music', bestOutcome:'gallery', categories:[] });
ok('music 次序：新人獎→女歌手→男歌手',
  nightMusic.map(n=>n.id).join(',') === 'cat_music_newcomer,cat_music_singer_f,cat_music_singer_m');
ok('未知 role 排最後（rank 9）', awards208CatRank({ role:'x', gender:'m' }) === 9 &&
  awards208CatRank({}) === 9 && awards208CatRank(null) === 9);

/* ---- nightCats 內容 ---- */
ok('night film 4 格，全部有 3 位 fellows', nightFilm.length === 4 && nightFilm.every(n=> n.fellows.length === 3));
ok('玩家格 isFocus 啱（lead_m），其餘格唔係',
  nightFilm.filter(n=>n.isFocus).length === 1 && nightFilm[3].isFocus && !nightFilm[0].isFocus);
ok('非玩家格 outcome gallery、得主＝fellows[0]',
  nightFilm.slice(0, 3).every(n=> n.outcome === 'gallery' && n.winner && n.winner.star === '星1號'));
ok('玩家格 nominated 得主＝winner63（陸柏言）', nightFilm[3].winner && nightFilm[3].winner.star === '陸柏言');

/* ---- (2) beat 結構：nominated film ---- */
const beatsNom = awards62CeremonyBeats(packFilm('nominated', 'cat_film_lead_m'));
ok('open／out 成晚各一次',
  beatsNom.filter(b=>b.id === 'open').length === 1 && beatsNom.filter(b=>b.id === 'out').length === 1);
const titlesNom = beatsNom.filter(b=>b.id === 'catTitle');
ok('每格 1 個 catTitle，次序同 night 一致',
  titlesNom.length === 4 && titlesNom.map(b=>b.catId).join(',') === 'cat_film_support_m,cat_film_support_f,cat_film_lead_f,cat_film_lead_m');
ok('每格 nominee beats 數：玩家格 4、其他格 3',
  beatsOfCat(beatsNom, 'cat_film_lead_m').filter(b=>b.id === 'nominee').length === 4 &&
  ['cat_film_support_m','cat_film_support_f','cat_film_lead_f'].every(id=> beatsOfCat(beatsNom, id).filter(b=>b.id === 'nominee').length === 3));
ok('多格模式冇舊 names beat', !beatsNom.some(b=>b.id === 'names'));
const nomLead = beatsOfCat(beatsNom, 'cat_film_lead_m').filter(b=>b.id === 'nominee');
ok('提名 beat caption 逐位「星：《作品》」，第一位係阿偉',
  nomLead[0].caption === '阿偉：《夜海鎗火》' && nomLead[1].caption === '陸柏言：《賀歲喜劇笑滿堂》' &&
  nomLead[2].caption === '廖炳星：《詭校夜話》' && nomLead[3].caption === '麥震東：《神探闖天關》');
ok('nominee 欄位：idx／total／slotIdx 映射啱（阿偉 slot 1）',
  nomLead.map(b=>b.nomineeIdx).join(',') === '0,1,2,3' && nomLead.every(b=>b.nomineeTotal === 4) &&
  nomLead.map(b=>b.slotIdx).join(',') === '1,0,2,3');
const nomSup = beatsOfCat(beatsNom, 'cat_film_support_m').filter(b=>b.id === 'nominee');
ok('非玩家格 slotIdx＝nomineeIdx', nomSup.map(b=>b.slotIdx).join(',') === '0,1,2');
const enterNom = beatsNom.filter(b=>b.id === 'enter');
const titleLeadIdx = beatsNom.indexOf(titlesNom[3]);
ok('enter 1 次，喺玩家格 catTitle 之前',
  enterNom.length === 1 && beatsNom.indexOf(enterNom[0]) === titleLeadIdx - 1);
const beatsSup = awards62CeremonyBeats(packFilm('nominated', 'cat_film_support_m'));
ok('focus 係第一格嗰陣 enter 緊接 open',
  beatsSup.filter(b=>b.id === 'enter').length === 1 && beatsSup.indexOf(beatsSup.find(b=>b.id === 'enter')) === 1);
const comfortNom = beatsNom.find(b=>b.id === 'comfort');
ok('玩家格 nominated：comfort 2600，冇 walkup／glamour',
  !!comfortNom && comfortNom.ms === 2600 && !beatsNom.some(b=>b.id === 'walkup') && !beatsNom.some(b=>b.id === 'glamour') &&
  beatsNom.indexOf(comfortNom) === beatsNom.indexOf(beatsNom.filter(b=>b.id === 'reveal').pop()) + 1);
const beatsWon = awards62CeremonyBeats(packFilm('won', 'cat_film_lead_m'));
const walkWon = beatsWon.find(b=>b.id === 'walkup');
const glamWon = beatsWon.find(b=>b.id === 'glamour');
ok('玩家格 won：walkup 2200＋glamour 1800，冇 comfort',
  !!walkWon && walkWon.ms === 2200 && !!glamWon && glamWon.ms === 1800 && !beatsWon.some(b=>b.id === 'comfort') &&
  beatsWon.indexOf(walkWon) === beatsWon.indexOf(beatsWon.filter(b=>b.id === 'reveal').pop()) + 1 &&
  beatsWon.indexOf(glamWon) === beatsWon.indexOf(walkWon) + 1);

/* ---- gallery／declined ---- */
const beatsGal = awards62CeremonyBeats({ ceremonyId:'award_harbour_film', year:1990, medium:'film',
  displayName:'維港影藝獎', bestOutcome:'gallery', repWork62:'', repGigId63:'', venue99:'', categories:[] });
ok('gallery：pan 1 次、冇 enter／walkup／glamour／comfort',
  beatsGal.filter(b=>b.id === 'pan').length === 1 && !beatsGal.some(b=>['enter','walkup','glamour','comfort'].indexOf(b.id) >= 0) &&
  beatsGal.filter(b=>b.id === 'catTitle').length === 4);
ok('declined：pan 電視轉播版、成晚多格',
  (()=>{ const d = awards62CeremonyBeats({ ceremonyId:'award_harbour_film', year:1990, medium:'film',
    displayName:'維港影藝獎', bestOutcome:'gallery', declined165:true, repWork62:'', repGigId63:'', venue99:'', categories:[] });
    return /電視轉播/.test(d.find(b=>b.id === 'pan').caption) && d.filter(b=>b.id === 'catTitle').length === 4; })());

/* ---- (3) 秒數 ---- */
const perCat = (beats, catId)=> beatsOfCat(beats, catId).filter(b=> b.id !== 'enter').reduce((a, b)=> a + b.ms, 0); /* enter 成晚一次，喺玩家格之前，唔計入嗰格本身 */
ok('每格秒數：非玩家格 10700ms、玩家格 nominated 15300ms',
  perCat(beatsNom, 'cat_film_support_m') === 10700 && perCat(beatsNom, 'cat_film_lead_m') === 15300);
const totalNom = beatsNom.reduce((a, b)=> a + b.ms, 0);
ok('成晚總秒數：film nominated 約 51 秒（45–55）', totalNom === 50850);
const beatsMus = awards62CeremonyBeats({ ceremonyId:'award_golddisc_music', year:1990, medium:'music',
  displayName:'星河金碟夜', bestOutcome:'nominated', repWork62:'夜歌', repGigId63:'', venue99:'',
  categories:[{ id:'cat_music_singer_m', label:'最佳男歌手', outcome:'nominated', repWorkTitle:'夜歌',
    fellows63: FEL_NOM.slice(), winner63: FEL_NOM[0] }] });
const totalMus = beatsMus.reduce((a, b)=> a + b.ms, 0);
ok('成晚總秒數：music nominated 約 40 秒（38–45）', totalMus === 40150);
const totalWon = beatsWon.reduce((a, b)=> a + b.ms, 0);
ok('成晚總秒數：film won（有海報）約 52 秒（45–55）', totalWon === 52250);

/* ---- (4) 揭曉文案 ---- */
const revSup = beatsOfCat(beatsNom, 'cat_film_support_m').find(b=>b.id === 'reveal');
ok('揭曉 caption：非玩家格得主＝fellows[0]', /星1號憑《戲1號》得獎/.test(revSup.caption));
const revLeadNom = beatsOfCat(beatsNom, 'cat_film_lead_m').find(b=>b.id === 'reveal');
ok('揭曉 caption：玩家格 nominated 有得主＋差少少',
  /陸柏言憑《賀歲喜劇笑滿堂》得獎/.test(revLeadNom.caption) && /差少少，下年再嚟/.test(revLeadNom.caption));
const revLeadWon = beatsOfCat(beatsWon, 'cat_film_lead_m').find(b=>b.id === 'reveal');
ok('揭曉 caption：玩家格 won 有得獎＋代表作', /得獎/.test(revLeadWon.caption) && /《夜海鎗火》/.test(revLeadWon.caption));

/* ---- (6) 邊界 ---- */
let emptyOk = false;
try{
  const bEmpty = awards62CeremonyBeats({ ceremonyId:'award_probe_empty', year:1990, medium:'film',
    displayName:'探針獎', bestOutcome:'gallery', repWork62:'', repGigId63:'', venue99:'', categories:[] });
  const nomEmpty = beatsOfCat(bEmpty, 'cat_empty').filter(b=>b.id === 'nominee');
  const revEmpty = beatsOfCat(bEmpty, 'cat_empty').find(b=>b.id === 'reveal');
  emptyOk = nomEmpty.length === 1 && /入圍名單逐個唱出/.test(nomEmpty[0].caption) &&
    /今晚嘅得獎者誕生/.test(revEmpty.caption) &&
    beatsOfCat(bEmpty, 'cat_probe_lead').filter(b=>b.id === 'nominee').length === 3;
}catch(_e){ emptyOk = false; }
ok('fellows 空嗰格：通用提名 beat＋揭曉 fallback，唔 crash', emptyOk);
const savedMvp = awardsMvpCategories;
awardsMvpCategories = function(){ return []; };
let fbOk = false;
try{
  const bFb = awards62CeremonyBeats(packFilm('nominated', 'cat_film_lead_m'));
  const tFb = bFb.reduce((a, b)=> a + b.ms, 0);
  fbOk = !!bFb.find(b=>b.id === 'names') && tFb >= 9000 && tFb <= 12000;
}catch(_e){ fbOk = false; }
awardsMvpCategories = savedMvp;
ok('全表空 → 跌返舊單格（有 names beat）', fbOk);
let noCerOk = false;
try{
  const bNc = awards62CeremonyBeats({ displayName:'星河電視獎', bestOutcome:'nominated', repWork62:'長篇劇',
    categories:[{ label:'最佳男主角', outcome:'nominated', repWorkTitle:'長篇劇', fellows63: FEL_NOM.slice(), winner63: FEL_NOM[0] }] });
  noCerOk = !!bNc.find(b=>b.id === 'names');
}catch(_e){ noCerOk = false; }
ok('冇 ceremonyId → 跌返舊單格（有 names beat）', noCerOk);

/* ---- (7) 跳過語義＋固定 beat 時長 ---- */
ok('跳過語義：一個 beats list、一個 out 喺最後',
  Array.isArray(beatsNom) && beatsNom.filter(b=>b.id === 'out').length === 1 &&
  beatsNom[beatsNom.length - 1].id === 'out');
ok('nominee beat 每位 2000ms', beatsNom.filter(b=>b.id === 'nominee').every(b=>b.ms === 2000));
ok('catTitle 1200／suspense 1400／reveal 2100',
  beatsNom.filter(b=>b.id === 'catTitle').every(b=>b.ms === 1200) &&
  beatsNom.filter(b=>b.id === 'suspense').every(b=>b.ms === 1400) &&
  beatsNom.filter(b=>b.id === 'reveal').every(b=>b.ms === 2100));

console.log('');
console.log(fails.length ? ('FAILED: '+fails.length+' -> '+fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
