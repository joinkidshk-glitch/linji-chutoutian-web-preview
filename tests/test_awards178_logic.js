// v20a178 高俊傑上頒獎禮・邏輯測試（v20a252 D-v2-2：特別名額已刪——重寫做退役測試）：
// (1) 特別名額已刪：全年掃描，fellows 入面永遠冇 ko_chunkit／高俊傑（唔係有出有唔出，
//     係零出現）；awards63Fellows 入面無 ko 條款、無 1991 年閘。
// (2) 程天諾同樣唔入（唔喺 POSTER59_STAR_IDS，冇 sprite）。
// (3) 入池嗰陣結構齊：starId／star／title／gigId 非空、assigned 一律 false。
// (4) 上限唔郁：任何年份 fellows ≤ 3；第一輪真主演齊晒（2 張真主演＋零兜底 →
//     回 2 個，唔會補位，唔會俾人逼走）。
// (5) 唱名：awards63FellowsHtml 有真主演嗰陣印得出佢哋個名。
// (6) 池／權重已刪：AWARDS63_POOL／AWARDS63_TIER_WEIGHT 唔喺 index.html。
// 反證：對 pristine main 行 → v178 門檻／ko 條款唔存在 → 乾淨 FAIL（唔 crash，exit 1）。
// v20a229 B3：POSTER59_IDS 已刪（海報舊表），needConsts 唔再抽佢；fixture 係合成 id＋stub，不變。
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
  'awards63CatSlot','awards63HasSprite','awards63Fellows','awards63FellowsHtml'];
const needConsts = ['POSTER59_STAR_IDS','AWARDS188_CATEGORIES','AWARDS204_FEMALE_STARS','EMOJI_ICON112'];
let missing = false;
for(const c of needConsts){ const s = extractConst(c); if(s===null){ missing = true; } else { try{ eval(s.replace('const '+c+' =', 'var '+c+' =')); }catch(_e){ missing = true; } } }
for(const f of needFns){ const s = extractFn(f); if(s===null){ missing = true; } else { try{ eval(s); }catch(_e){ missing = true; } } }
try{ eval(extractFn('iconHtml112')); }catch(_e){ missing = true; }
if(missing){
  ok('v178 退役：在位嘅係 cast 模型 fellows（awards63Fellows＋AWARDS188_CATEGORIES 等抽得到）', false);
  ok('全年掃描零高俊傑', false);
  ok('全年掃描零程天諾', false);
  ok('入池嗰陣結構齊（starId／star／title／gigId／assigned=false）', false);
  ok('上限 3＋第一輪真主演齊晒（唔補位）', false);
  ok('唱名印得出真主演名', false);
  ok('AWARDS63_POOL／AWARDS63_TIER_WEIGHT 已刪', false);
  console.log('\nFAILED: ' + fails.length);
  process.exit(1);
}

/* ---- 世界 stub（cast 模型：fixture 自帶 cast／singer／host） ---- */
function mkGigs(){
  const g = [];
  // 每媒介每年：2 張有陣容（第一輪料）＋4 張無陣容（唔產生對手，唔兜底）
  const media = [
    { medium:'film', type:'電影', cer:'award_harbour_film' },
    { medium:'tv', type:'電視劇', cer:'award_singho_tv' },
    { medium:'music', type:'唱片通告', cer:'award_golddisc_music' },
    { medium:'ad', type:'廣告', cer:'award_harbour_ad' }
  ];
  [1990, 1991, 1992].forEach(y=>{
    media.forEach((m, mi)=>{
      if(m.medium === 'music'){
        g.push({ id:'gig_'+y+'_'+m.medium+'_lead1', type:m.type, year:y, pay:[30000,40000], workTitle:y+'年'+m.medium+'主演作一', singer:'luk_baakyin', singerGender:'m' });
        g.push({ id:'gig_'+y+'_'+m.medium+'_lead2', type:m.type, year:y, pay:[20000,30000], workTitle:y+'年'+m.medium+'主演作二', singer:'so_jiyan', singerGender:'f' });
      }else{
        g.push({ id:'gig_'+y+'_'+m.medium+'_lead1', type:m.type, year:y, pay:[30000,40000], workTitle:y+'年'+m.medium+'主演作一',
          cast:{ leadM:'luk_baakyin', leadF:'so_jiyan', supportM:null, supportF:null } });
        g.push({ id:'gig_'+y+'_'+m.medium+'_lead2', type:m.type, year:y, pay:[20000,30000], workTitle:y+'年'+m.medium+'主演作二',
          cast:{ leadM:'liu_bingxing', leadF:'chung_choning', supportM:null, supportF:null } });
      }
      for(let k=1;k<=4;k++) g.push({ id:'gig_'+y+'_'+m.medium+'_nolead'+k, type:m.type, year:y, pay:[5000+k*1000,8000+k*1000], workTitle:y+'年'+m.medium+'無主演作'+k,
        cast:{ leadM:null, leadF:null, supportM:null, supportF:null } });
    });
  });
  return g;
}
var GIGS = mkGigs();
var S = { wrapHistory: [] };
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
const hasTinlok = (fl)=> (fl||[]).some(f=> f && (f.starId==='ching_tinlok' || f.star==='程天諾'));

/* ---- (1) 全年掃描零高俊傑（特別名額已刪） ---- */
let koCount = 0, totalSweep = 0, overCap = 0, structBad = 0, allFellows = [];
for(const y of [1990, 1991, 1992]) for(const c of CERS) for(const id of CER_IDS){
  const fl = fellowsFor(y, id, c.medium, c.type);
  totalSweep++;
  if(hasKo(fl)) koCount++;
  if(fl.length > 3) overCap++;
  fl.forEach(f=>{
    allFellows.push(f);
    if(!(f.starId && f.star && f.title && f.gigId && f.assigned === false)) structBad++;
  });
}
ok('全年掃描零高俊傑（'+totalSweep+' 組合，特別名額已刪）', koCount === 0);

/* ---- (2) 程天諾同樣唔入 ---- */
let tinlokCount = 0;
for(const y of [1990, 1991, 1992]) for(const c of CERS) for(const id of CER_IDS){
  if(hasTinlok(fellowsFor(y, id, c.medium, c.type))) tinlokCount++;
}
ok('全年掃描零程天諾（唔喺 POSTER59_STAR_IDS，冇 sprite）', tinlokCount === 0);

/* ---- (3) 入池嗰陣結構齊 ---- */
ok('入池嗰陣結構齊（starId／star／title／gigId 非空、assigned 一律 false，'+allFellows.length+' 個樣本）',
  allFellows.length > 0 && structBad === 0);

/* ---- (4) 上限 3＋第一輪真主演齊晒（唔補位） ---- */
ok('上限 3（全年掃描零超標）', overCap === 0);
// Minimal 場景：2 張真主演（duo1／duo2，leadM）＋3 張無陣容 → 回 2 位真主演，唔補位。
let duoOk = false;
const savedGigs = GIGS;
GIGS = [
  { id:'gig_1991_film_duo1', type:'電影', year:1991, pay:[90000,100000], workTitle:'1991電影真主演一',
    cast:{ leadM:'luk_baakyin', leadF:null, supportM:null, supportF:null } },
  { id:'gig_1991_film_duo2', type:'電影', year:1991, pay:[80000,90000], workTitle:'1991電影真主演二',
    cast:{ leadM:'liu_bingxing', leadF:null, supportM:null, supportF:null } },
  { id:'gig_1991_film_nl1', type:'電影', year:1991, pay:[10000,12000], workTitle:'1991電影無主演作一',
    cast:{ leadM:null, leadF:null, supportM:null, supportF:null } },
  { id:'gig_1991_film_nl2', type:'電影', year:1991, pay:[9000,11000], workTitle:'1991電影無主演作二',
    cast:{ leadM:null, leadF:null, supportM:null, supportF:null } },
  { id:'gig_1991_film_nl3', type:'電影', year:1991, pay:[8000,10000], workTitle:'1991電影無主演作三',
    cast:{ leadM:null, leadF:null, supportM:null, supportF:null } }
];
const flDuo = fellowsFor(1991, 'award_probe_0', 'film', '電影');
duoOk = flDuo.length === 2 && flDuo[0].star === '陸柏言' && flDuo[1].star === '廖炳星' &&
  flDuo.every(f=>f.assigned === false);
GIGS = savedGigs;
ok('第一輪真主演齊晒（2 張真主演＋零兜底 → 回 2 個，唔補位）', duoOk);
// fellows 函數入面無 ko 條款、無年份閘
const fellowsSrc = extractFn('awards63Fellows') || '';
ok('fellows 入面無 ko 條款、無 1991 年閘（D-v2-2）',
  fellowsSrc.indexOf('ko_chunkit') < 0 && fellowsSrc.indexOf('高俊傑') < 0 && fellowsSrc.indexOf('1991') < 0);

/* ---- (5) 唱名：用真實入池樣本，冇樣本就 FAIL（唔用假 sample 頂住） ---- */
let htmlOut = '';
try{
  if(allFellows[0]) htmlOut = awards63FellowsHtml({ fellows63:[allFellows[0], { star:'陸柏言', title:'試作二' }], winner63:null, outcome:'gallery' });
}catch(_e){ htmlOut = ''; }
ok('唱名印得出真主演名', allFellows.length > 0 && htmlOut.indexOf(allFellows[0].star) >= 0);

/* ---- (6) 池／權重已刪＋星名查唔到佢 ---- */
ok('AWARDS63_POOL／AWARDS63_TIER_WEIGHT 已刪（D-v2-2，唔留 dormant）',
  html.indexOf('const AWARDS63_POOL') < 0 && html.indexOf('const AWARDS63_TIER_WEIGHT') < 0 &&
  html.indexOf('function awards63WeightedPick(') < 0);
ok('awards63StarName 查唔到佢（唔喺 POSTER59_STAR_IDS）', awards63StarName('ko_chunkit') === '');

console.log('');
console.log(fails.length ? ('FAILED: ' + fails.length) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
