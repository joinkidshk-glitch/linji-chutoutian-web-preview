// v20a62 頒獎優化包・邏輯測試：
// (1) 作品質量加權：一部擔正大製作明顯抵兩三部閒角工；quality 表（roleScale／片酬段／stars 微調）。
// (2) 實力判定：刪 18% 贏獎骰——遠離贏線時口味 ±0.05 翻唔到盤；邊界 ±0.05 內先由口味話事。
// (3) 冇第一年隱形壓分：同參數下 1988 同 1990 年 base 分完全一樣。
// (4) 代表作＝嗰年嗰媒介最高質嗰部；請柬門檻行；結果弱瓣「差啲咩」。
// (5) standing 差額（入圍差幾部／贏線差幾多）；季前提示觸發／靜默（含冬→春跨年跳過）。
// (6) beats 純資料：得獎全長 9–10 秒（v64 起 enter 改真走路入場 1750ms，基線由 8–9 秒更新）、旁聽較短、唱名行掛代表作。
// (7) 獎項頁 render：新記錄（displayName＋repTitle）同舊記錄（乜都冇）都顯示到，唔崩。
// (8) buildAwardResultPack 端到端：categories 掛 repWorkTitle／weakHint62、pack 有 standing62。
// 反證：對 v20a61 index 行 → AWARDS62 函數唔存在 → FAIL。
// 用法：node tests/test_awards62_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
function approx(a, b, eps){ return Math.abs(a-b) <= (eps||0.001); }
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
var S = null;
eval("var START = { y:1988, m:3, d:7 };");
for(const c of ['AWARDS62_WIN_LINE','AWARDS62_TASTE','AWARDS62_ROLE_Q','AWARDS62_MEDIUM_LABEL'])
  eval(extractConst(c).replace('const '+c+' =', 'var '+c+' ='));

var TEST_GIGS = {
  gig_lead:   { id:'gig_lead',   roleScale:'film_lead_big',     stars:5, pay:[30000,50000], type:'電影', workTitle:'大製作', roleLabel:'男主角' },
  gig_lead2:  { id:'gig_lead2',  roleScale:'film_support_main', stars:4, pay:[12000,18000], type:'電影', workTitle:'配角戲', roleLabel:'第二男主角' },
  gig_extra:  { id:'gig_extra',  roleScale:'film_extra_day',    stars:1, pay:[300,500],     type:'電影', workTitle:'臨記工', roleLabel:'臨記' },
  gig_tvlead: { id:'gig_tvlead', roleScale:'tv_lead_long',      stars:4, pay:[20000,26000], type:'電視劇', workTitle:'長篇劇', roleLabel:'男主角' },
  gig_tv2:    { id:'gig_tv2',    roleScale:'tv_support_main',   stars:3, pay:[8000,10000],  type:'電視劇', workTitle:'電視配角戲', roleLabel:'配角' }
};
var work59GigLookup = function(id){ return TEST_GIGS[id] || null; };
var work59WorkOf = function(h, g){
  if(h && h.workTitle) return String(h.workTitle);
  if(g && g.workTitle) return String(g.workTitle);
  const t = String((h && h.title) || (g && g.title) || '');
  const m = t.match(/《(.+?)》/);
  return m ? m[1] : t;
};
var esc59 = function(s){ return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); };
var awardsDual = function(){ return { stageVolume: Number(S&&S.fame)||0, industryCredit: 10 + (Number(S&&S.industryCreditDelta)||0) }; };
var awardsCalendarYear = function(){ return (S && S._year) || 1989; };
var awardsYearFromDay = function(di){
  const dt = new Date(START.y, START.m-1, START.d + (di|0));
  return dt.getFullYear();
};
var ensurePostShootRewardLog = function(){ return []; };
var ensureCastingTagsState = function(){ return (S && S._tags) || []; };
var calendarSeason = function(){ return (S && S._season) || '春'; };
var weekNumNow = function(){ return 20; };
var TEST_CEREMONIES = [
  { id:'award_singho_tv', medium:'tv', displayName:'星河電視獎', season:'冬', matchTypes:['電視劇','綜藝'], metricEcho:'ratings' },
  { id:'award_harbour_ad', medium:'ad', displayName:'海港廣告獎', season:'春', matchTypes:['廣告'], metricEcho:'attention' }
];
var awardsCeremonies = function(){ return TEST_CEREMONIES; };
var awardsCeremonyById = function(id){ return TEST_CEREMONIES.find(c=>c.id===id) || null; };
var awardsGetFlag = function(y, id){ return (S && S.awardsFlags && S.awardsFlags[y+'/'+id]) || ''; };
var ensureAwardsLog = function(){ if(!Array.isArray(S.awardsLog)) S.awardsLog = []; return S.awardsLog; };
var FREEPLAY_FW = {
  awardsSchema: {
    tiers: [
      { id:'nominee', requires:{ yearMediumWrapsMin:2, anyOf:[{stageVolumeMin:10},{industryCreditMin:12}] } },
      { id:'gallery', requires:{ anyOf:[{yearMediumWrapsMin:1},{gigCountMin:2}] } }
    ],
    categories: {
      award_singho_tv: [
        { id:'tv_lead', primaryTrack:'stageVolume' },
        { id:'tv_pop', primaryTrack:'industryCredit' }
      ],
      award_harbour_ad: [ { id:'ad_best', primaryTrack:'stageVolume' } ]
    },
    dualTrackRewards: {
      won: { stageVolume:[3,5], industryCredit:[2,4] },
      nominated: { stageVolume:[1,2], industryCredit:[1,2] },
      gallery: { stageVolume:[0,1], industryCredit:[0,0] }
    }
  },
  awardsStub: {
    ceremonies: [
      { id:'award_singho_tv', displayName:'星河電視獎', inviteTitle:'電視獎請柬', inviteDek:'一封燙金信。' },
      { id:'award_harbour_ad', displayName:'海港廣告獎', inviteTitle:'廣告獎請柬', inviteDek:'一封燙金信。' }
    ],
    categories: {
      award_singho_tv: [
        { id:'tv_lead', label:'最佳男主角', winLine:'台上念到你個名。', loseLine:'入圍未得獎。', galleryLine:'觀禮一晚。' },
        { id:'tv_pop', label:'最受歡迎男藝員', winLine:'觀眾票選有你。', loseLine:'入圍未得獎。', galleryLine:'觀禮一晚。' }
      ],
      award_harbour_ad: [
        { id:'ad_best', label:'最佳廣告演繹', winLine:'台上念到你個名。', loseLine:'入圍未得獎。', galleryLine:'觀禮一晚。' }
      ]
    },
    tiers: [ { id:'nominee', label:'入圍／提名' }, { id:'gallery', label:'旁聽席' } ],
    fallbacks: {},
    pressTemplates: [], newsTemplates: []
  }
};
var awardsStubCeremony = function(id){ return FREEPLAY_FW.awardsStub.ceremonies.find(c=>c.id===id) || null; };
var document = { _els: {}, getElementById: function(id){ if(!this._els[id]) this._els[id] = { innerHTML:'' }; return this._els[id]; } };

const FNS = ['awardsCopyLine','awardsSchemaTiers','awardsGigCount','countYearMediumWraps','awardsEvalTier','awardsMetricEchoLabel',
  'awardsMvpCategories','awardsStubCategory','awardsPickPressNews','awardsDualRewardForOutcome',
  'awards62WorkQuality','awards62YearOf','awards62YearWorks','awards62RepWork','awards62ScoreParts',
  'awards62WeakHint','awards62WrapMin','awards62Standing','awards62GateLineHtml','renderAwardsPane62',
  'awards62SeasonHints','awards62CeremonyBeats','awardsScoreCategory','buildAwardResultPack'];
/* v128 A5：獎項渲染經 iconHtml112（🏆→trophy 圖）——抽真身入 stub，唔係 mock。 */
eval(extractConst('EMOJI_ICON112').replace('const EMOJI_ICON112 =', 'var EMOJI_ICON112 ='));
eval(extractFn('iconHtml112'));
for(const f of FNS) eval(extractFn(f));

function baseSave(){
  return { dayIndex: 300, fame: 0, industryCreditDelta: 0, wrapHistory: [], awardsLog: [], awardsFlags: {},
    story: { gigCount: 0 }, _tags: [], _season: '秋', _year: 1989 };
}
function wrap(gigId, year, pay){
  const g = TEST_GIGS[gigId] || {};
  return { gigId: gigId, title: '《'+(g.workTitle||gigId)+'》', type: g.type||'電影', workTitle: g.workTitle||'',
    roleLabel: g.roleLabel||'', year: year, pay: pay!=null?pay:((g.pay&&g.pay[0])||0), wrappedDay: (year-1988)*365 + 120 };
}
const FILM_CER = { id:'award_harbour_film', medium:'film', displayName:'海港電影獎', season:'秋', matchTypes:['電影'] };
const CAT_SV = { id:'film_actor', primaryTrack:'stageVolume' };

/* ================= (1) 質量加權 ================= */
ok('quality: 擔正大製作 stars5 → 1.0', awards62WorkQuality({ gigId:'gig_lead' }) === 1);
ok('quality: 臨記 stars1 → 0.18', approx(awards62WorkQuality({ gigId:'gig_extra' }), 0.18));
ok('quality: 冇 gig 用片酬段 25000 → 0.80', awards62WorkQuality({ gigId:'nope', pay:25000 }) === 0.8);
ok('quality: 冇 gig 片酬 500 → 0.25', awards62WorkQuality({ gigId:'nope', pay:500 }) === 0.25);

S = baseSave(); S.fame = 20;
S.wrapHistory = [ wrap('gig_lead', 1989) ];
const pLead = awards62ScoreParts(CAT_SV, FILM_CER, 1989);
S.wrapHistory = [ wrap('gig_extra', 1989), wrap('gig_extra', 1989), wrap('gig_extra', 1989), wrap('gig_extra', 1989) ];
const pExtras = awards62ScoreParts(CAT_SV, FILM_CER, 1989);
ok('worksScore: 一部擔正 0.625', approx(pLead.worksScore, 0.625));
ok('一部擔正抵三部閒角有多（base 差 ≥0.15）', (pLead.base - pExtras.base) >= 0.15);

/* ================= (2) 實力判定，冇運氣骰 ================= */
Math.random = function(){ return 0.5; }; /* taste = 0 */
S = baseSave(); S.fame = 40; S._tags = ['動作演員'];
S.wrapHistory = [ wrap('gig_lead', 1989), wrap('gig_lead2', 1989) ];
const catTag = { id:'film_actor', primaryTrack:'stageVolume', tagBonusAny:['動作演員'] };
const pMid = awards62ScoreParts(catTag, FILM_CER, 1989);
ok('中間帶 base ≈ 0.8306', approx(pMid.base, 0.8306, 0.002));
let r = awardsScoreCategory(catTag, FILM_CER, 1989, 'nominee');
ok('taste 0 → won（過贏線）', r.outcome === 'won');
Math.random = function(){ return 0; }; /* taste = -0.05 */
r = awardsScoreCategory(catTag, FILM_CER, 1989, 'nominee');
ok('taste -0.05 → 擦邊跌返 nominated', r.outcome === 'nominated');
Math.random = function(){ return 1; }; /* taste = +0.05：最勁口味都翻唔到遠離贏線嘅盤 */
S = baseSave(); S.fame = 45;
S.wrapHistory = [ wrap('gig_lead', 1989) ];
r = awardsScoreCategory(CAT_SV, FILM_CER, 1989, 'nominee');
ok('base 0.6625 + 口味盡 0.05 都未到贏線 → nominated（冇 18% 骰翻盤）', r.outcome === 'nominated');
r = awardsScoreCategory(CAT_SV, FILM_CER, 1989, 'gallery');
ok('gallery tier 恆 gallery', r.outcome === 'gallery');

/* ================= (3) 冇第一年壓分 ================= */
function partsForYear(y){
  S = baseSave(); S.fame = 30;
  S.wrapHistory = [ wrap('gig_lead', y), wrap('gig_lead2', y) ];
  return awards62ScoreParts(CAT_SV, FILM_CER, y).base;
}
ok('1988 同 1990 同參數 base 一樣（冇 ×0.72）', approx(partsForYear(1988), partsForYear(1990)));

/* ================= (4) 代表作／弱瓣／門檻行 ================= */
S = baseSave(); S.fame = 20;
S.wrapHistory = [ wrap('gig_extra', 1989), wrap('gig_lead', 1989), wrap('gig_lead2', 1989) ];
ok('代表作揀最高質嗰部', awards62RepWork(FILM_CER, 1989) === '大製作');
S.wrapHistory = [];
ok('冇作品 → 代表作空字串（唔作故仔）', awards62RepWork(FILM_CER, 1989) === '');
const hint = awards62WeakHint({ topQ: 0.2, normPrimary: 0.9, worksCount: 5, primaryTrack: 'stageVolume' }, CAT_SV);
ok('弱瓣：代表作最弱 → 指路接主角級', /擔正/.test(hint) && /差啲咩/.test(hint));
const hint2 = awards62WeakHint({ topQ: 0.9, normPrimary: 0.2, worksCount: 5, primaryTrack: 'industryCredit' }, CAT_SV);
ok('弱瓣：主軌最弱 → 指路谷信用', /業內信用/.test(hint2));

/* ================= (5) standing + 季前提示 ================= */
const TV = TEST_CEREMONIES[0];
S = baseSave(); S.fame = 30; S.story.gigCount = 3;
S.wrapHistory = [ wrap('gig_tvlead', 1989) ];
let sd = awards62Standing(TV, 1989);
ok('standing: 差 1 部入圍', sd.gapWorks === 1 && sd.wrapMin === 2);
S._season = '秋'; /* 電視獎喺冬：d=1 下季 */
let h = awards62SeasonHints(S, 30);
ok('季前提示：下季差一部電視作品 → 出聲', !!h && /下季就係/.test(h) && /仲差 1 部電視作品/.test(h));
S.wrapHistory = [ wrap('gig_tvlead', 1989), wrap('gig_tv2', 1989) ];
h = awards62SeasonHints(S, 30);
ok('已入圍但離贏線遠 → 靜默（唔嘈）', h === null);
S.fame = 45; S.industryCreditDelta = 50; /* credit 60：tv_pop normPrimary 1 */
S.wrapHistory = [ wrap('gig_tvlead', 1989), wrap('gig_tv2', 1989) ];
sd = awards62Standing(TV, 1989);
ok('勁玩家 standing 到贏線帶', sd.tier === 'nominee' && sd.gapWin <= 0.15);
h = awards62SeasonHints(S, 30);
ok('季前提示：接近贏線 → 出聲指路', !!h && /接近贏嗰格|大熱/.test(h));
S = baseSave(); S._season = '冬'; S._year = 1989; S.fame = 30;
S.awardsFlags = { '1989/award_singho_tv': 'done' }; /* 今季電視獎已完，淨返春季廣告獎有缺口 */
S.wrapHistory = [ wrap('gig_tvlead', 1989) ]; /* 廣告作品 0 部：冇跨年擋就會出提示 */
h = awards62SeasonHints(S, 40);
ok('冬→春跨年唔出季前版（計數年份防錯位）', h === null);

/* ================= (6) beats ================= */
const wonPack = { displayName:'星河電視獎', bestOutcome:'won', repWork62:'長篇劇',
  categories:[{ label:'最佳男主角', outcome:'won', repWorkTitle:'長篇劇' }] };
const beatsWon = awards62CeremonyBeats(wonPack);
const totalWon = beatsWon.reduce((a,b)=>a+b.ms, 0);
ok('得獎 beats 全長 9–10 秒', totalWon >= 9000 && totalWon <= 10000);
ok('beats 有齊 open/enter/names/suspense/reveal/out', ['open','enter','names','suspense','reveal','out'].every(id=>beatsWon.some(b=>b.id===id)));
const namesBeat = beatsWon.find(b=>b.id==='names');
ok('唱名行掛代表作', !!namesBeat && namesBeat.lines.some(l=>/《長篇劇》/.test(l)));
const beatsGal = awards62CeremonyBeats({ displayName:'海港廣告獎', bestOutcome:'gallery', categories:[] });
const totalGal = beatsGal.reduce((a,b)=>a+b.ms, 0);
ok('旁聽 beats 較短且冇唱名/懸念', totalGal < totalWon && !beatsGal.some(b=>b.id==='names'||b.id==='suspense'));

/* ================= (7) 獎項頁 render ================= */
S = baseSave();
S.awardsLog = [
  { id:'aw_1989_tv', ceremonyId:'award_singho_tv', medium:'tv', year:1989, season:'冬', tier:'nominee',
    displayName:'星河電視獎', categories:[{ id:'tv_lead', outcome:'won', repTitle:'長篇劇' }], skipped:false },
  { id:'aw_1988_film', ceremonyId:'award_harbour_film', medium:'film', year:1988, season:'秋', tier:'gallery',
    categories:[{ id:'x', outcome:'gallery' }], skipped:false }
];
renderAwardsPane62();
const paneHtml = document._els['awards-list'].innerHTML;
ok('獎項頁：新記錄出得獎＋代表作', /得獎/.test(paneHtml) && /《長篇劇》/.test(paneHtml));
ok('獎項頁：舊記錄（冇新欄位）照顯示唔崩', /電影頒獎禮/.test(paneHtml) && /觀禮/.test(paneHtml));
S.awardsLog = [];
renderAwardsPane62();
ok('獎項頁：空記錄有引導文案', /未有頒獎紀錄/.test(document._els['awards-list'].innerHTML));

/* ================= (8) buildAwardResultPack 端到端 ================= */
Math.random = function(){ return 0.5; };
S = baseSave(); S.fame = 45; S.industryCreditDelta = 50;
S.wrapHistory = [ wrap('gig_tvlead', 1989), wrap('gig_tv2', 1989) ];
const pack = buildAwardResultPack({ ceremonyId:'award_singho_tv', year:1989 });
ok('pack：類別掛代表作', pack.categories.every(c=>c.repWorkTitle === '長篇劇'));
ok('pack：有 standing62 快照', !!pack.standing62 && pack.standing62.tier === 'nominee');
ok('pack：repWork62 齊', pack.repWork62 === '長篇劇');
const gateHtml = awards62GateLineHtml(pack);
ok('請柬門檻行：已達標＋代表作', /入圍門檻已達標/.test(gateHtml) && /《長篇劇》/.test(gateHtml));
S = baseSave(); S.fame = 0;
S.wrapHistory = [];
const packLow = buildAwardResultPack({ ceremonyId:'award_singho_tv', year:1989 });
const gateLow = awards62GateLineHtml(packLow);
ok('請柬門檻行：新人出差額', /仲差 2 部電視作品/.test(gateLow));

console.log(fails.length ? ('\nFAILED: '+fails.length) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
