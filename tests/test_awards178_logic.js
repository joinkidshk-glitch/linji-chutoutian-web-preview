// v20a178 高俊傑上頒獎禮・邏輯測試（入池邏輯部分；sprite／卡片圖像部分等 character 到咗先補）：
// (1) 1990 年池冇佢：四媒介 × 多個 ceremony id 掃一轉，fellows 入面永遠冇 ko_chunkit／高俊傑。
// (2) 1991 年起有機會入池：1991／1992 同一個掃法，至少有一個組合有佢，亦至少有一個組合冇佢
//     （seeded 抽選，唔係逢場必出，唔係永遠唔出）。
// (3) 入池嗰陣結構齊：starId ko_chunkit、star 高俊傑（直接寫名——awards63StarName 查唔到佢，
//     POSTER59_STAR_IDS 刻意唔加佢，嗰個 map 係海報／主演邏輯）、title／gigId 非空、assigned true。
// (4) 上限唔郁：任何年份 fellows ≤ 3；第一輪真主演永遠唔會俾佢逼走（只可以取代第二輪兜底位，
//     或者喺未滿 3 嗰陣補位；三個都係第一輪真主演嗰陣佢唔入）。
// (5) 唱名：awards63FellowsHtml 有佢嗰陣印得出「高俊傑」。
// (6) 池／權重唔郁：佢唔入 AWARDS63_POOL，AWARDS63_TIER_WEIGHT 亦冇佢。
// 反證：對 pristine main 行 → v178 門檻／ko 條款唔存在 → 乾淨 FAIL（唔 crash，exit 1）。
// 用法：node tests/test_awards178_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) return null;
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){
    if(html[j]==='{') depth++;
    else if(html[j]==='}'){ depth--; if(depth===0) break; }
  }
  return html.slice(i, j+1);
}
function extractConst(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) return null;
  let depth = 0, started = false;
  for(let k=i; k<html.length; k++){
    const ch = html[k];
    if(ch==='{'||ch==='['){ depth++; started = true; }
    else if(ch==='}'||ch===']'){ depth--; if(started && depth===0) return html.slice(i, k+1)+';'; }
    else if(ch===';' && !started) return html.slice(i, k+1);
  }
  return null;
}

/* ---- 抽真函數；抽唔到就每項乾淨 FAIL，唔掟 stack ---- */
const needFns = ['awards63StarName','awards63AllGigs','awards63GigYear','awards63GigPay',
  'awards63KeySeed','awards63SeededRng','awards63WeightedPick','awards63Fellows','awards63FellowsHtml'];
const needConsts = ['POSTER59_STAR_IDS','POSTER59_IDS','AWARDS63_POOL','AWARDS63_TIER_WEIGHT','EMOJI_ICON112'];
let missing = false;
for(const c of needConsts){ const s = extractConst(c); if(s===null){ missing = true; } else { try{ eval(s.replace('const '+c+' =', 'var '+c+' =')); }catch(_e){ missing = true; } } }
for(const f of needFns){ const s = extractFn(f); if(s===null){ missing = true; } else { try{ eval(s); }catch(_e){ missing = true; } } }
try{ eval(extractFn('iconHtml112')); }catch(_e){ missing = true; }
if(missing){
  ok('v178 入池邏輯在位（awards63Fellows＋AWARDS63_POOL 等抽得到）', false);
  ok('1990 年池冇高俊傑', false);
  ok('1991 年起有機會入池（有出有唔出）', false);
  ok('入池嗰陣結構齊（starId／star／title／gigId／assigned）', false);
  ok('上限 3＋第一輪真主演唔會俾佢逼走', false);
  ok('唱名印得出「高俊傑」', false);
  ok('佢唔入 AWARDS63_POOL／AWARDS63_TIER_WEIGHT', false);
  console.log('\nFAILED: ' + fails.length);
  process.exit(1);
}

/* ---- 世界 stub ---- */
var TEST_STAR = {
  gig_1991_film_lead1: '陸柏言',
  gig_1991_film_lead2: '廖炳星',
  gig_1991_film_duo1: '陸柏言',
  gig_1991_film_duo2: '廖炳星',
  gig_1990_film_lead1: '陸柏言',
  gig_1992_tv_lead1: '齊鎮海'
};
function mkGigs(){
  const g = [];
  // 每媒介每年：2 張有主演（第一輪料）＋4 張冇主演（第二輪／高俊傑掛靠料）
  const media = [
    { medium:'film', type:'電影', cer:'award_harbour_film' },
    { medium:'tv', type:'電視劇', cer:'award_singho_tv' },
    { medium:'music', type:'唱片通告', cer:'award_golddisc_music' },
    { medium:'ad', type:'廣告', cer:'award_harbour_ad' }
  ];
  [1990, 1991, 1992].forEach(y=>{
    media.forEach((m, mi)=>{
      g.push({ id:'gig_'+y+'_'+m.medium+'_lead1', type:m.type, year:y, pay:[30000,40000], workTitle:y+'年'+m.medium+'主演作一' });
      g.push({ id:'gig_'+y+'_'+m.medium+'_lead2', type:m.type, year:y, pay:[20000,30000], workTitle:y+'年'+m.medium+'主演作二' });
      for(let k=1;k<=4;k++) g.push({ id:'gig_'+y+'_'+m.medium+'_nolead'+k, type:m.type, year:y, pay:[5000+k*1000,8000+k*1000], workTitle:y+'年'+m.medium+'無主演作'+k });
    });
  });
  // 1991 film 特別場（§4 minimal 場景用獨立 id，唔同 generic 嗰批撞 id）
  g.push({ id:'gig_1991_film_duo1', type:'電影', year:1991, pay:[90000,100000], workTitle:'1991電影真主演一' });
  g.push({ id:'gig_1991_film_duo2', type:'電影', year:1991, pay:[80000,90000], workTitle:'1991電影真主演二' });
  return g;
}
var GIGS = mkGigs();
var S = { wrapHistory: [] };
var leadStar59Of = function(g){ return (g && TEST_STAR[g.id]) || ''; };
var poster59Path = function(gid){ return ''; };
var work59WorkOf = function(h, g){ return (g && (g.workTitle || g.title)) || ''; };

const CERS = [
  { medium:'film', type:'電影', cer:'award_harbour_film' },
  { medium:'tv', type:'電視劇', cer:'award_singho_tv' },
  { medium:'music', type:'唱片通告', cer:'award_golddisc_music' },
  { medium:'ad', type:'廣告', cer:'award_harbour_ad' }
];
const CER_IDS = [];
for(let i=0;i<24;i++) CER_IDS.push('award_probe_'+i);
function fellowsFor(year, cerId, medium, type){
  return awards63Fellows({ id:cerId, medium:medium, matchTypes:[type] }, year);
}
const hasKo = (fl)=> (fl||[]).some(f=> f && (f.starId==='ko_chunkit' || f.star==='高俊傑'));

/* ---- (1) 1990 年池冇佢 ---- */
let ko1990 = 0, total1990 = 0, overCap = 0;
for(const c of CERS) for(const id of CER_IDS){
  const fl = fellowsFor(1990, id, c.medium, c.type);
  total1990++;
  if(hasKo(fl)) ko1990++;
  if(fl.length > 3) overCap++;
}
ok('1990 年池冇高俊傑（'+total1990+' 組合零出現）', ko1990 === 0);

/* ---- (2) 1991 年起有機會入池 ---- */
let ko91 = 0, total91 = 0;
for(const y of [1991, 1992]) for(const c of CERS) for(const id of CER_IDS){
  const fl = fellowsFor(y, id, c.medium, c.type);
  total91++;
  if(hasKo(fl)) ko91++;
  if(fl.length > 3) overCap++;
}
ok('1991 年起有機會入池（'+ko91+'/'+total91+' 組合有佢，唔係零亦唔係全部）', ko91 > 0 && ko91 < total91);

/* ---- (3) 入池嗰陣結構齊 ---- */
let koEntries = [];
for(const y of [1991, 1992]) for(const c of CERS) for(const id of CER_IDS){
  fellowsFor(y, id, c.medium, c.type).forEach(f=>{ if(f && f.starId==='ko_chunkit') koEntries.push(f); });
}
const structOk = koEntries.length > 0 && koEntries.every(f=>
  f.star === '高俊傑' && typeof f.title === 'string' && f.title.length > 0 &&
  typeof f.gigId === 'string' && f.gigId.length > 0 && f.assigned === true);
ok('入池嗰陣結構齊（starId／star／title／gigId／assigned，'+koEntries.length+' 個樣本）', structOk);

/* ---- (4) 上限 3＋第一輪真主演唔會俾佢逼走 ---- */
ok('上限 3（全年掃描零超標）', overCap === 0);
// Minimal 場景：2 張真主演（duo1／duo2）＋3 張冇主演 → 第一輪出 2 位，第二輪補 1 位湊夠 3。
// 高俊傑嗰步只能取代第二輪兜底位（繼承嗰個位嘅作品），唔可以逼走真主演。
let leadKept = true, leadChecked = 0;
const savedGigs = GIGS;
GIGS = [
  { id:'gig_1991_film_duo1', type:'電影', year:1991, pay:[90000,100000], workTitle:'1991電影真主演一' },
  { id:'gig_1991_film_duo2', type:'電影', year:1991, pay:[80000,90000], workTitle:'1991電影真主演二' },
  { id:'gig_1991_film_nl1', type:'電影', year:1991, pay:[10000,12000], workTitle:'1991電影無主演作一' },
  { id:'gig_1991_film_nl2', type:'電影', year:1991, pay:[9000,11000], workTitle:'1991電影無主演作二' },
  { id:'gig_1991_film_nl3', type:'電影', year:1991, pay:[8000,10000], workTitle:'1991電影無主演作三' }
];
for(const id of CER_IDS){
  const fl = fellowsFor(1991, id, 'film', '電影');
  if(hasKo(fl)){
    leadChecked++;
    const stars = fl.map(f=> f.star);
    if(!stars.includes('陸柏言') || !stars.includes('廖炳星')) leadKept = false;
  }
}
GIGS = savedGigs;
ok('第一輪真主演唔會俾佢逼走（'+leadChecked+' 場有佢在場核實）', leadChecked > 0 && leadKept);

/* ---- (5) 唱名：用真實入池樣本，冇樣本就 FAIL（唔用假 sample 頂住） ---- */
let htmlOut = '';
try{
  if(koEntries[0]) htmlOut = awards63FellowsHtml({ fellows63:[koEntries[0], { star:'陸柏言', title:'試作二' }], winner63:null, outcome:'gallery' });
}catch(_e){ htmlOut = ''; }
ok('唱名印得出「高俊傑」', koEntries.length > 0 && htmlOut.indexOf('高俊傑') >= 0);

/* ---- (6) 池／權重唔郁＋星名要直接寫 ---- */
ok('佢唔入 AWARDS63_POOL／AWARDS63_TIER_WEIGHT', JSON.stringify(AWARDS63_POOL).indexOf('ko_chunkit') < 0 && !('ko_chunkit' in AWARDS63_TIER_WEIGHT));
ok('awards63StarName 查唔到佢（所以 star 要直接寫「高俊傑」）', awards63StarName('ko_chunkit') === '');

console.log('');
console.log(fails.length ? ('FAILED: ' + fails.length) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
