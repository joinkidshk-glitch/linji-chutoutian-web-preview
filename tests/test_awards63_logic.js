// v20a63 頒獎禮群星版・邏輯測試：
// (1) fellows 衍生：嗰年嗰媒介 pack 通告＋LEADSTAR59 主演，按片酬序、每星一部、唔用冇 sprite 嘅主演（彭兆基）。
// (2) 玩家自己殺青過嘅作品唔會變對手；年份唔串。
// (3) 冇主演數據（1991）→ 紅星池按媒介兜底：確定性、唔重複、唔出程天諾（1990 零出場紅線，池內根本冇佢）。
// (4) beats：入圍揭曉唱出得主星名＋作品；得獎＋有海報先有 glamour beat；冇海報得獎維持 9–10 秒（v64 enter 走路入場後基線）。
// (5) focus cat 揀啱（won 優先 won cat、nominated 揀 nominated cat）。
// 反證：對 v20a62 index 行 → AWARDS63 函數唔存在 → FAIL。
// 用法：node tests/test_awards63_logic.js [path-to-index.html]
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

/* ---- 世界 stub ---- */
var window = {};
for(const c of ['POSTER59_STAR_IDS','POSTER59_IDS','AWARDS63_POOL'])
  eval(extractConst(c).replace('const '+c+' =', 'var '+c+' ='));

var TEST_STAR = {
  gig_1988_film_harbour_high: '陸柏言',
  gig_1988_film_cotton_spring_high: '廖炳星',
  gig_1988_film_03: '麥震東',
  gig_1988_film_01: '廖炳星',
  gig_1988_ad_central_winter_low: '彭兆基',
  gig_1988_ad_02: '陸柏言',
  gig_1988_ad_05: '駱家聲',
  gig_1988_tv_06: '陸柏言',
  gig_1988_tv_03: '齊鎮海'
};
var GIGS = [
  { id:'gig_1988_film_harbour_high',        type:'電影',   pay:[40000,48000], workTitle:'夜海鎗火' },
  { id:'gig_1988_film_cotton_spring_high',  type:'電影',   pay:[35000,41900], workTitle:'詭校夜話' },
  { id:'gig_1988_film_03',                  type:'電影',   pay:[8000,10500],  workTitle:'神探闖天關' },
  { id:'gig_1988_film_01',                  type:'電影',   pay:[2000,3500],   workTitle:'陰陽夜更' },
  { id:'gig_1988_ad_central_winter_low',    type:'廣告',   pay:[1000,1800],   workTitle:'冬日飲品廣告' },
  { id:'gig_1988_ad_02',                    type:'廣告',   pay:[2500,3250],   workTitle:'龍鳳喜餅賀春照' },
  { id:'gig_1988_ad_05',                    type:'廣告',   pay:[3000,4000],   workTitle:'夏日汽水廣告' },
  { id:'gig_1988_tv_06',                    type:'電視劇', pay:[15000,20000], workTitle:'賀歲喜劇笑滿堂' },
  { id:'gig_1988_tv_03',                    type:'電視劇', pay:[6000,8000],   workTitle:'飛天劍影決雌雄' },
  { id:'gig_1989_film_a',                   type:'電影',   pay:[16000,20000], workTitle:'九龍夜行' },
  { id:'gig_1989_film_b',                   type:'電影',   pay:[9000,12000],  workTitle:'霓裳夜冷' },
  { id:'gig_1989_film_c',                   type:'電影',   pay:[7000,9000],   workTitle:'半島槍聲' }
];
var S = { wrapHistory: [] };
var leadStar59Of = function(g){ return (g && TEST_STAR[g.id]) || ''; };
var poster59Path = function(gid){ return (gid && POSTER59_IDS[gid]) ? ('data:poster:'+gid) : ''; };
var work59WorkOf = function(h, g){ return (g && (g.workTitle || g.title)) || ''; };

for(const f of ['awards63StarName','awards63AllGigs','awards63GigYear','awards63GigPay','awards63Fellows','awards63FocusCat','awards62CeremonyBeats'])
  eval(extractFn(f));

const CER_FILM = { id:'award_harbour_film', medium:'film', matchTypes:['電影'] };
const CER_TV   = { id:'award_singho_tv',    medium:'tv',   matchTypes:['電視劇','綜藝'] };
const CER_AD   = { id:'award_harbour_ad',   medium:'ad',   matchTypes:['廣告'] };

/* ---- (1) 真主演衍生 ---- */
S.wrapHistory = [];
let fl = awards63Fellows(CER_FILM, 1990);
ok('1990 電影 fellows 有 3 位', fl.length === 3);
ok('按片酬序：陸柏言《夜海鎗火》居首', fl[0] && fl[0].star === '陸柏言' && fl[0].title === '夜海鎗火' && fl[0].starId === 'luk_baakyin');
ok('廖炳星只出現一次（取最高 pay 嗰部《詭校夜話》）', fl.filter(f=>f.star==='廖炳星').length === 1 && fl.some(f=>f.title==='詭校夜話') && !fl.some(f=>f.title==='陰陽夜更'));
ok('第三位係麥震東《神探闖天關》', fl[2] && fl[2].star === '麥震東');
ok('真主演 fellows assigned=false', fl.every(f=>f.assigned === false));
ok('有海報嘅 fellow 帶 poster（夜海鎗火係試點十部）', fl[0].poster === 'data:poster:gig_1988_film_harbour_high');

let flAd = awards63Fellows(CER_AD, 1990);
ok('廣告 fellows 唔用冇 sprite 嘅彭兆基', !flAd.some(f=>f.gigId==='gig_1988_ad_central_winter_low') && flAd.length >= 2 && flAd.every(f=>f.starId));

let flTv = awards63Fellows(CER_TV, 1990);
ok('電視 fellows：陸柏言＋齊鎮海', flTv.length === 2 && flTv[0].star === '陸柏言' && flTv[1].star === '齊鎮海');

/* ---- (2) 自己作品唔做對手＋年份隔離 ---- */
S.wrapHistory = [{ gigId:'gig_1988_film_harbour_high' }];
fl = awards63Fellows(CER_FILM, 1990);
ok('玩家殺青過嘅《夜海鎗火》唔做對手', !fl.some(f=>f.title==='夜海鎗火') && fl[0] && fl[0].star === '廖炳星');
S.wrapHistory = [];
const fl89 = awards63Fellows(CER_FILM, 1991);
ok('1991 fellows 只用 1991 作品（gig_1989_* id 舊曆編碼，解析 +2）', fl89.length === 3 && fl89.every(f=>/^gig_1989_/.test(f.gigId)));

/* ---- (3) 池兜底 ---- */
ok('1991 fellows 全部 assigned=true（池兜底）', fl89.every(f=>f.assigned === true));
ok('兜底星全部喺電影池內且唔重複', fl89.every(f=>AWARDS63_POOL.film.indexOf(f.starId)>=0) && new Set(fl89.map(f=>f.starId)).size === fl89.length);
const fl89b = awards63Fellows(CER_FILM, 1991);
ok('兜底確定性（兩次呼叫結果一致）', JSON.stringify(fl89) === JSON.stringify(fl89b));
const poolNames = Object.values(AWARDS63_POOL).flat().map(id=>awards63StarName(id));
ok('紅星池冇程天諾（紅線）', poolNames.indexOf('程天諾') < 0 && poolNames.every(n=>n));
ok('任何 fellows 都唔會係程天諾', fl.concat(fl89, flTv, flAd).every(f=>f.star !== '程天諾'));

/* ---- (5) focus cat ---- */
const packMix = { bestOutcome:'nominated', categories:[
  { id:'a', outcome:'gallery' }, { id:'b', outcome:'nominated' }, { id:'c', outcome:'nominated' } ] };
ok('focus：nominated 揀第一個 nominated cat', awards63FocusCat(packMix).id === 'b');
const packWon = { bestOutcome:'won', categories:[ { id:'a', outcome:'nominated' }, { id:'b', outcome:'won' } ] };
ok('focus：won 揀 won cat', awards63FocusCat(packWon).id === 'b');

/* ---- (4) beats ---- */
const felLuk = { starId:'luk_baakyin', star:'陸柏言', title:'賀歲喜劇笑滿堂', gigId:'gig_1988_tv_06', poster:'', assigned:false };
const packNom = { displayName:'星河電視獎', bestOutcome:'nominated', repWork62:'飛天劍影決雌雄', repGigId63:'gig_1988_tv_03',
  categories:[{ label:'最佳男主角', outcome:'nominated', repWorkTitle:'飛天劍影決雌雄', fellows63:[felLuk], winner63:felLuk }] };
const beatsNom = awards62CeremonyBeats(packNom);
const revealNom = beatsNom.find(b=>b.id==='reveal');
ok('入圍揭曉 caption 唱出得主星名＋作品', !!revealNom && /陸柏言/.test(revealNom.caption) && /《賀歲喜劇笑滿堂》/.test(revealNom.caption));
ok('入圍揭曉 caption 提玩家代表作', !!revealNom && /《飛天劍影決雌雄》/.test(revealNom.caption));
const namesNom = beatsNom.find(b=>b.id==='names');
ok('唱名 lines 有齊玩家＋對手', !!namesNom && namesNom.lines.some(l=>/阿偉/.test(l)) && namesNom.lines.some(l=>/陸柏言/.test(l)));
ok('入圍冇 glamour beat（得獎先有）', !beatsNom.some(b=>b.id==='glamour'));

const packWonPoster = { displayName:'維港影藝獎', bestOutcome:'won', repWork62:'夜海鎗火', repGigId63:'gig_1988_film_harbour_high',
  categories:[{ label:'最佳電影', outcome:'won', repWorkTitle:'夜海鎗火', fellows63:[], winner63:null }] };
const beatsWP = awards62CeremonyBeats(packWonPoster);
ok('得獎＋有海報 → 有 glamour beat', beatsWP.some(b=>b.id==='glamour'));
ok('得獎＋海報全長 > 9 秒（glamour 一擊）', beatsWP.reduce((a,b)=>a+b.ms,0) > 9000);

const packWonNoPoster = { displayName:'維港影藝獎', bestOutcome:'won', repWork62:'陰陽夜更', repGigId63:'gig_1988_film_01',
  categories:[{ label:'最佳電影', outcome:'won', repWorkTitle:'陰陽夜更', fellows63:[], winner63:null }] };
const beatsWN = awards62CeremonyBeats(packWonNoPoster);
const totalWN = beatsWN.reduce((a,b)=>a+b.ms,0);
ok('得獎＋冇海報 → 冇 glamour、全長維持 9–10 秒', !beatsWN.some(b=>b.id==='glamour') && totalWN >= 9000 && totalWN <= 10000);

const beatsGal = awards62CeremonyBeats({ displayName:'海港廣告獎', bestOutcome:'gallery', categories:[] });
ok('旁聽：冇 names/suspense/reveal、有 pan 群星鏡頭且較短', !beatsGal.some(b=>b.id==='names'||b.id==='suspense'||b.id==='reveal') && beatsGal.some(b=>b.id==='pan') && beatsGal.reduce((a,b)=>a+b.ms,0) < totalWN);

console.log('');
console.log(fails.length ? ('FAILED: '+fails.length+' -> '+fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
