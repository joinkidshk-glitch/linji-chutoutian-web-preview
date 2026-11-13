// v20a188 頒獎獎項改名＋提名掛鈎・邏輯測試：
// (1) 新獎項表 15 個逐個斷言（id／label／winLine／loseLine／galleryLine 存在、廣東話、
//     唔含舊組別後綴／舊人氣獎／10 個舊生造名；role／gender 欄位齊）。
// (2) 角色判定 awards188WorkRole：主角／配角／歌手／臨記／替身陷阱（tv_lead_long＋替身雜務、
//     film_lead_big＋主要替身唔可以當主角）。
// (3) role-based 閘 awards188EligibleCats：臨記開局唔入圍男主角、做過主角先入圍男主角、
//     做過配角先入圍男配角、音樂獎要唱過歌先入圍、新人獎要係首年、女獎項永遠唔入玩家池。
// (4) 端到端 buildAwardResultPack（唔 forceTier）：臨記檔 tier 跌返 gallery、主角檔 tier nominee
//     且類別只係男主角、配角檔只係男配角、強檔到贏線 0.875 贏獎；forceTier nominee 嗰陣
//     eligible 空都唔留空 pack；請柬門檻行講明角色閘原因。
// 反證：對 pristine main index 行 → AWARDS188_CATEGORIES／awards188WorkRole 唔存在 → FAIL（唔 crash）。
// 用法：node tests/test_awards188_logic.js [path-to-index.html]
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

/* 反證守衛：v188 嘢唔存在嗰陣乾淨 FAIL（逐項列出），唔好等 extractConst／extractFn
   喺頂層 throw 崩潰。放喺任何 extraction 之前。 */
const NEED188_CONSTS = ['AWARDS188_CATEGORIES','AWARDS188_PLAYER_GENDER','AWARDS188_NP_WIN'];
const NEED188_FNS = ['awards188IsLead','awards188IsSupport','awards188WorkRole','awards188HadEarlierWork',
  'awards188CatEligible','awards188EligibleCats','awards188ApplyNpOverlay'];
let missing188 = [];
NEED188_CONSTS.forEach(c=>{ if(html.indexOf('const '+c+' =')<0) missing188.push(c); });
NEED188_FNS.forEach(f=>{ if(html.indexOf('function '+f+'(')<0) missing188.push(f); });
if(missing188.length){
  missing188.forEach(m=>{ fails.push('反證：'+m+' 唔存在'); console.log('FAIL 反證：'+m+' 唔存在（pristine main 預期，v188 未入）'); });
  console.log('\nFAILED: '+fails.length);
  process.exit(1);
}

/* ---- 世界 stub（沿用 test_awards62_logic.js 嗰套，再加四典禮＋新 role gig） ---- */
var window = {};
var S = null;
eval("var START = { y:1988, m:3, d:7 };");
for(const c of ['AWARDS62_WIN_LINE','AWARDS62_TASTE','AWARDS62_ROLE_Q','AWARDS62_MEDIUM_LABEL',
  'AWARDS188_CATEGORIES','AWARDS188_PLAYER_GENDER','AWARDS65_LEAD_SCALES',
  'END95_LEAD_SCALES','END95_STRONG_LEAD','PRESS94_NAMED_SCALES'])
  eval(extractConst(c).replace('const '+c+' =', 'var '+c+' ='));

var TEST_GIGS = {
  gig_film_lead:   { id:'gig_film_lead',   roleScale:'film_lead_big',     stars:5, pay:[30000,50000], type:'電影', workTitle:'大製作', roleLabel:'男主角' },
  gig_film_lead2:  { id:'gig_film_lead2',  roleScale:'film_second_lead',  stars:4, pay:[15000,22000], type:'電影', workTitle:'二番戲', roleLabel:'第二男主角' },
  gig_film_sup:    { id:'gig_film_sup',    roleScale:'film_support_main', stars:4, pay:[12000,18000], type:'電影', workTitle:'配角戲', roleLabel:'重要配角' },
  gig_film_sup2:   { id:'gig_film_sup2',   roleScale:'film_support',      stars:3, pay:[8000,12000],  type:'電影', workTitle:'綠葉戲', roleLabel:'男配角' },
  gig_film_extra:  { id:'gig_film_extra',  roleScale:'film_extra_short',  stars:1, pay:[300,500],     type:'電影', workTitle:'臨記工', roleLabel:'臨記' },
  gig_film_standin:{ id:'gig_film_standin', roleScale:'film_lead_big',    stars:4, pay:[15000,20000], type:'電影', workTitle:'替身戲', roleLabel:'主要替身' },
  gig_tv_lead:     { id:'gig_tv_lead',     roleScale:'tv_lead_long',      stars:4, pay:[20000,26000], type:'電視劇', workTitle:'長篇劇', roleLabel:'男主角' },
  gig_tv_sup:      { id:'gig_tv_sup',      roleScale:'tv_support_main',   stars:3, pay:[8000,10000],  type:'電視劇', workTitle:'電視配角戲', roleLabel:'配角' },
  gig_tv_cameo:    { id:'gig_tv_cameo',    roleScale:'tv_cameo_short',    stars:1, pay:[300,500],     type:'電視劇', workTitle:'客串工', roleLabel:'客串途人' },
  gig_tv_standin:  { id:'gig_tv_standin',  roleScale:'tv_lead_long',      stars:4, pay:[15000,20000], type:'電視劇', workTitle:'替身劇', roleLabel:'替身雜務' },
  gig_var:         { id:'gig_var',         roleScale:'variety_ep',        stars:2, pay:[2000,3000],  type:'綜藝', workTitle:'綜藝集', roleLabel:'遊戲嘉賓' },
  gig_ad_lead:     { id:'gig_ad_lead',     roleScale:'ad_lead',           stars:4, pay:[15000,20000], type:'廣告', workTitle:'大品牌廣告', roleLabel:'廣告男主角' },
  gig_ad_sup:      { id:'gig_ad_sup',      roleScale:'ad_support',        stars:3, pay:[8000,10000],  type:'廣告', workTitle:'配角廣告', roleLabel:'廣告配角' },
  gig_ad_extra:    { id:'gig_ad_extra',    roleScale:'ad_extra_day',      stars:1, pay:[300,500],     type:'廣告', workTitle:'路人廣告', roleLabel:'廣告路人' },
  gig_rec:         { id:'gig_rec',         roleScale:'rec_album',         stars:3, pay:[8000,12000],  type:'唱片通告', workTitle:'大碟', roleLabel:'主唱' },
  gig_rec2:        { id:'gig_rec2',        roleScale:'music_support',     stars:2, pay:[3000,5000],   type:'唱片通告', workTitle:'和音碟', roleLabel:'和音歌手' },
  gig_mtv_lead:    { id:'gig_mtv_lead',    roleScale:'mtv',               stars:3, pay:[8000,12000],  type:'唱片通告', workTitle:'冠軍歌MV', roleLabel:'男主角' }
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
var awardsCalendarYear = function(){ return (S && S._year) || 1990; };
var awardsYearFromDay = function(di){
  const dt = new Date(START.y, START.m-1, START.d + (di|0));
  return dt.getFullYear();
};
var ensurePostShootRewardLog = function(){ return []; };
var ensureCastingTagsState = function(){ return (S && S._tags) || []; };
var calendarSeason = function(){ return (S && S._season) || '春'; };
var weekNumNow = function(){ return 40; };
var TEST_CEREMONIES = [
  { id:'award_harbour_ad', medium:'ad', displayName:'維港街招・年度廣告賞', season:'春', matchTypes:['廣告'], metricEcho:'attention' },
  { id:'award_golddisc_music', medium:'music', displayName:'星河金碟夜', season:'夏', matchTypes:['唱片通告'], metricEcho:'sales' },
  { id:'award_harbour_film', medium:'film', displayName:'維港影藝獎', season:'秋', matchTypes:['電影'], metricEcho:'boxOffice' },
  { id:'award_singho_tv', medium:'tv', displayName:'星河台慶・年度頒獎夜', season:'冬', matchTypes:['電視劇','綜藝'], metricEcho:'ratings' }
];
var awardsCeremonies = function(){ return TEST_CEREMONIES; };
var awardsCeremonyById = function(id){ return TEST_CEREMONIES.find(c=>c.id===id) || null; };
var awardsGetFlag = function(y, id){ return (S && S.awardsFlags && S.awardsFlags[y+'/'+id]) || ''; };
var ensureAwardsLog = function(){ if(!Array.isArray(S.awardsLog)) S.awardsLog = []; return S.awardsLog; };
var FREEPLAY_FW = {
  awardsSchema: {
    tiers: [
      { id:'nominee', requires:{ yearMediumWrapsMin:2, yearMediumWrapsMinByMedium:{ ad:1, music:1, film:2, tv:2 }, anyOf:[{stageVolumeMin:10},{industryCreditMin:12}] } },
      { id:'gallery', requires:{ anyOf:[{yearMediumWrapsMin:1},{gigCountMin:2}] } }
    ],
    categories: {},
    dualTrackRewards: {
      won: { stageVolume:[3,5], industryCredit:[2,4] },
      nominated: { stageVolume:[1,2], industryCredit:[1,2] },
      gallery: { stageVolume:[0,1], industryCredit:[0,0] }
    }
  },
  awardsStub: {
    ceremonies: TEST_CEREMONIES.map(c=>({ id:c.id, displayName:c.displayName, inviteTitle:'請柬', inviteDek:'一封信。' })),
    categories: {},
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
  'awards62WeakHint','awards62WrapMin','awards62Standing','awards62GateLineHtml',
  'awards62ScoreParts','awardsScoreCategory','buildAwardResultPack',
  'press94ScaleOf','end95IsLead','awards65IsLeadWork',
  'awards188IsLead','awards188IsSupport','awards188WorkRole','awards188HadEarlierWork',
  'awards188CatEligible','awards188EligibleCats'];
eval(extractConst('EMOJI_ICON112').replace('const EMOJI_ICON112 =', 'var EMOJI_ICON112 ='));
eval(extractFn('iconHtml112'));
for(const f of FNS) eval(extractFn(f));

function baseSave(){
  return { dayIndex: 300, fame: 0, industryCreditDelta: 0, wrapHistory: [], awardsLog: [], awardsFlags: {},
    story: { gigCount: 0 }, _tags: [], _season: '秋', _year: 1990 };
}
function wrap(gigId, year){
  const g = TEST_GIGS[gigId] || {};
  return { gigId: gigId, title: '《'+(g.workTitle||gigId)+'》', type: g.type||'電影', workTitle: g.workTitle||'',
    roleLabel: g.roleLabel||'', year: year, pay: ((g.pay&&g.pay[0])||0), wrappedDay: (year-1988)*365 + 120 };
}
const FILM = TEST_CEREMONIES[2], TV = TEST_CEREMONIES[3], MUSIC = TEST_CEREMONIES[1], AD = TEST_CEREMONIES[0];
const OLD_LABELS = ['年度廣告新面孔','街外最記得住嘅一鏡','年度新人碟緣','最受歡迎出鏡嗓','影壇新面孔',
  '年度票房話題綠葉','最佳電視新人','最受歡迎螢幕面孔','綜藝閃光綠葉','最佳班底'];
const EXPECTED_LABELS = {
  award_harbour_ad: ['最佳廣告男主角','最佳廣告女主角','最佳廣告男配角','最佳廣告女配角'],
  award_golddisc_music: ['最佳男歌手','最佳女歌手','最佳新人獎'],
  award_harbour_film: ['最佳男主角','最佳女主角','最佳男配角','最佳女配角'],
  award_singho_tv: ['最佳男主角','最佳女主角','最佳男配角','最佳女配角']
};

/* ================= (1) 新獎項表 15 個 ================= */
let allCats = [];
Object.keys(AWARDS188_CATEGORIES).forEach(k=>{ (AWARDS188_CATEGORIES[k]||[]).forEach(c=>allCats.push(c)); });
ok('表：共 15 個獎項', allCats.length === 15);
Object.keys(EXPECTED_LABELS).forEach(k=>{
  const got = (AWARDS188_CATEGORIES[k]||[]).map(c=>c.label);
  ok('表：'+k+' labels 齊（'+EXPECTED_LABELS[k].length+' 個）',
    got.length === EXPECTED_LABELS[k].length && EXPECTED_LABELS[k].every(l=>got.indexOf(l) >= 0));
});
const ids188 = allCats.map(c=>c.id);
ok('表：id 全部唔同', new Set(ids188).size === 15);
let tableOk = true;
allCats.forEach(c=>{
  if(!c.id || !c.label || !c.winLine || !c.loseLine || !c.galleryLine) tableOk = false;
  if(!/[\u4e00-\u9fff]/.test(c.winLine) || !/[\u4e00-\u9fff]/.test(c.loseLine) || !/[\u4e00-\u9fff]/.test(c.galleryLine)) tableOk = false;
  if(['lead','support','singer','newcomer'].indexOf(c.role) < 0) tableOk = false;
  if(['m','f',''].indexOf(c.gender) < 0) tableOk = false;
  if(['stageVolume','industryCredit'].indexOf(c.primaryTrack) < 0) tableOk = false;
  [c.label, c.winLine, c.loseLine, c.galleryLine].forEach(t=>{
    if(/臨記組|最受歡迎/.test(t)) tableOk = false;
    OLD_LABELS.forEach(o=>{ if(t.indexOf(o) >= 0) tableOk = false; });
  });
});
ok('表：逐個有 id／label／winLine／loseLine／galleryLine，廣東話，唔含舊組別後綴／舊人氣獎／舊生造名', tableOk);
ok('表：女獎項齊（每典禮都有女主角／女配角／女歌手，淨係玩家池唔入）',
  ['cat_film_lead_f','cat_film_support_f','cat_tv_lead_f','cat_tv_support_f',
   'cat_ad_lead_f','cat_ad_support_f','cat_music_singer_f'].every(id=>ids188.indexOf(id) >= 0)
  && ids188.indexOf('cat_music_newcomer') >= 0);
ok('awardsMvpCategories 行覆寫表（film 4／music 3／tv 4／ad 4）',
  awardsMvpCategories('award_harbour_film').length === 4
  && awardsMvpCategories('award_golddisc_music').length === 3
  && awardsMvpCategories('award_singho_tv').length === 4
  && awardsMvpCategories('award_harbour_ad').length === 4);
ok('awardsStubCategory 行覆寫表（label／lines 由新表出）',
  awardsStubCategory('award_harbour_film','cat_film_lead_m').label === '最佳男主角'
  && /影藝獎台上念到你個名/.test(awardsStubCategory('award_harbour_film','cat_film_lead_m').winLine));

/* ================= (2) 角色判定 ================= */
function roleOf(gigId, year){
  return awards188WorkRole({ h: wrap(gigId, year || 1990), g: TEST_GIGS[gigId], q: 0, title: TEST_GIGS[gigId].workTitle });
}
ok('判定：電影男主角 → lead', roleOf('gig_film_lead') === 'lead');
ok('判定：電影二番 → lead', roleOf('gig_film_lead2') === 'lead');
ok('判定：電影重要配角 → support', roleOf('gig_film_sup') === 'support');
ok('判定：電影男配角 → support', roleOf('gig_film_sup2') === 'support');
ok('判定：電影臨記 → ""（唔係 lead 亦唔係 support）', roleOf('gig_film_extra') === '');
ok('判定：film_lead_big＋主要替身 → ""（替身唔係主角）', roleOf('gig_film_standin') === '');
ok('判定：電視男主角 → lead', roleOf('gig_tv_lead') === 'lead');
ok('判定：電視配角 → support', roleOf('gig_tv_sup') === 'support');
ok('判定：電視客串 → ""', roleOf('gig_tv_cameo') === '');
ok('判定：tv_lead_long＋替身雜務 → ""（替身陷阱）', roleOf('gig_tv_standin') === '');
ok('判定：綜藝嘉賓 → ""（綜藝唔係演員獎）', roleOf('gig_var') === '');
ok('判定：廣告男主角 → lead', roleOf('gig_ad_lead') === 'lead');
ok('判定：廣告配角 → support', roleOf('gig_ad_sup') === 'support');
ok('判定：廣告路人 → ""', roleOf('gig_ad_extra') === '');
ok('判定：大碟主唱 → singer', roleOf('gig_rec') === 'singer');
ok('判定：和音歌手 → singer（開過聲就計）', roleOf('gig_rec2') === 'singer');
ok('判定：MTV 男主角 → singer（唱片桶，唔係 lead）', roleOf('gig_mtv_lead') === 'singer');

/* ================= (3) role-based 閘 ================= */
function elig(cerId, year){
  const cer = awardsCeremonyById(cerId);
  return (awards188EligibleCats(cerId, cer, year) || []).map(c=>c.id);
}
S = baseSave(); S.fame = 45;
S.wrapHistory = [ wrap('gig_film_extra', 1990), wrap('gig_film_extra', 1990) ];
ok('閘：臨記開局（只做過臨記）→ 電影 eligible 空（唔入圍男主角）', elig('award_harbour_film', 1990).length === 0);
S.wrapHistory = [ wrap('gig_film_lead', 1990) ];
ok('閘：做過主角 → 入圍男主角（只得男主角，冇女主角／男配角）',
  JSON.stringify(elig('award_harbour_film', 1990)) === JSON.stringify(['cat_film_lead_m']));
S.wrapHistory = [ wrap('gig_film_sup', 1990) ];
ok('閘：做過配角 → 入圍男配角（只得男配角，冇男主角）',
  JSON.stringify(elig('award_harbour_film', 1990)) === JSON.stringify(['cat_film_support_m']));
S.wrapHistory = [ wrap('gig_film_lead', 1990), wrap('gig_film_sup', 1990) ];
ok('閘：主角＋配角 → 男主角＋男配角（女獎項永遠唔入）',
  JSON.stringify(elig('award_harbour_film', 1990)) === JSON.stringify(['cat_film_lead_m','cat_film_support_m']));
S.wrapHistory = [ wrap('gig_var', 1990), wrap('gig_var', 1990) ];
ok('閘：齋做綜藝 → 電視 eligible 空', elig('award_singho_tv', 1990).length === 0);
S.wrapHistory = [ wrap('gig_tv_lead', 1990) ];
ok('閘：電視男主角 → 只得 cat_tv_lead_m', JSON.stringify(elig('award_singho_tv', 1990)) === JSON.stringify(['cat_tv_lead_m']));
S.wrapHistory = [];
ok('閘：冇唱過歌 → 音樂 eligible 空', elig('award_golddisc_music', 1990).length === 0);
S.wrapHistory = [ wrap('gig_rec', 1990) ];
ok('閘：唱過歌（首年）→ 男歌手＋新人獎',
  JSON.stringify(elig('award_golddisc_music', 1990)) === JSON.stringify(['cat_music_singer_m','cat_music_newcomer']));
S.wrapHistory = [ wrap('gig_rec', 1990), wrap('gig_rec', 1991) ];
ok('閘：唱過歌但唔係首年 → 男歌手，冇新人獎',
  JSON.stringify(elig('award_golddisc_music', 1991)) === JSON.stringify(['cat_music_singer_m']));
S.wrapHistory = [ wrap('gig_ad_extra', 1990), wrap('gig_ad_extra', 1990) ];
ok('閘：廣告臨記 → eligible 空', elig('award_harbour_ad', 1990).length === 0);
S.wrapHistory = [ wrap('gig_ad_lead', 1990) ];
ok('閘：廣告男主角 → 只得 cat_ad_lead_m', JSON.stringify(elig('award_harbour_ad', 1990)) === JSON.stringify(['cat_ad_lead_m']));
S.wrapHistory = [ wrap('gig_ad_sup', 1990) ];
ok('閘：廣告配角 → 只得 cat_ad_support_m', JSON.stringify(elig('award_harbour_ad', 1990)) === JSON.stringify(['cat_ad_support_m']));

/* ================= (4) 端到端 build（唔 forceTier） ================= */
Math.random = function(){ return 0.5; }; /* taste 0，pickN 1 */
S = baseSave(); S.fame = 45; S.story.gigCount = 2;
S.wrapHistory = [ wrap('gig_film_extra', 1990), wrap('gig_film_extra', 1990) ];
let pack = buildAwardResultPack({ ceremonyId:'award_harbour_film', year:1990 });
ok('端到端：臨記檔作品數＋雙軌夠數，角色閘照跌返 gallery（唔入圍男主角）', pack.tier === 'gallery');
ok('端到端：臨記檔 gallery 類別來自全表（唔留空）', pack.categories.length >= 1);
const gateLow = awards62GateLineHtml(pack);
ok('端到端：請柬門檻行講明角色閘原因', /未做過主角／配角級作品/.test(gateLow));
S = baseSave(); S.fame = 25; S.story.gigCount = 2;
S.wrapHistory = [ wrap('gig_film_lead', 1990), wrap('gig_film_lead2', 1990) ];
pack = buildAwardResultPack({ ceremonyId:'award_harbour_film', year:1990 });
ok('端到端：主角檔 tier nominee', pack.tier === 'nominee');
ok('端到端：主角檔類別只係最佳男主角', pack.categories.length === 1 && pack.categories[0].id === 'cat_film_lead_m' && pack.categories[0].label === '最佳男主角');
ok('端到端：主角檔 outcome nominated（未到贏線）', pack.categories[0].outcome === 'nominated');
S = baseSave(); S.fame = 25; S.story.gigCount = 2;
S.wrapHistory = [ wrap('gig_film_sup', 1990), wrap('gig_film_sup2', 1990) ];
pack = buildAwardResultPack({ ceremonyId:'award_harbour_film', year:1990 });
ok('端到端：配角檔 tier nominee，類別只係最佳男配角',
  pack.tier === 'nominee' && pack.categories.length === 1 && pack.categories[0].id === 'cat_film_support_m');
S = baseSave(); S.fame = 25; S.story.gigCount = 1;
S.wrapHistory = [ wrap('gig_rec', 1990) ];
pack = buildAwardResultPack({ ceremonyId:'award_golddisc_music', year:1990 });
ok('端到端：唱過歌 → 音樂 tier nominee，類別係歌手／新人其一',
  pack.tier === 'nominee' && pack.categories.length === 1
  && ['cat_music_singer_m','cat_music_newcomer'].indexOf(pack.categories[0].id) >= 0);
S = baseSave(); S.fame = 45; S.story.gigCount = 5;
S.wrapHistory = [ wrap('gig_film_lead', 1990), wrap('gig_film_lead2', 1990),
  wrap('gig_tv_lead', 1990), wrap('gig_tv_lead', 1990) ];
pack = buildAwardResultPack({ ceremonyId:'award_harbour_film', year:1990 });
ok('端到端：強檔 base 0.90 過贏線 0.875 → won（WIN_LINE 唔郁）',
  AWARDS62_WIN_LINE === 0.875 && pack.categories[0].outcome === 'won');
ok('端到端：強檔贏嗰隻係最佳男主角', pack.categories[0].id === 'cat_film_lead_m');
S = baseSave(); S.fame = 45; S.story.gigCount = 2;
S.wrapHistory = [ wrap('gig_film_extra', 1990), wrap('gig_film_extra', 1990) ];
pack = buildAwardResultPack({ ceremonyId:'award_harbour_film', year:1990, forceTier:'nominee' });
ok('端到端：forceTier nominee＋eligible 空 → tier 照 forced，類別唔留空（debug fallback）',
  pack.tier === 'nominee' && pack.categories.length >= 1);
const adPack = buildAwardResultPack({ ceremonyId:'award_harbour_ad', year:1990, forceTier:'gallery' });
ok('端到端：廣告 gallery pack metricEcho attention', adPack.metricEcho === 'attention');
const muPack = buildAwardResultPack({ ceremonyId:'award_golddisc_music', year:1990, forceTier:'nominee' });
ok('端到端：音樂 nominee pack metricEcho sales', muPack.metricEcho === 'sales');

/* ---- (5) 報紙 win 模板覆寫：pack 8 款 headline／dek／clipLabel ---- */
eval(extractConst('AWARDS188_NP_WIN').replace('const AWARDS188_NP_WIN =', 'var AWARDS188_NP_WIN ='));
eval(extractFn('awards188ApplyNpOverlay'));
const NP_PACK_PATH = path.join(path.dirname(htmlPath), 'content', 'STUB_NEWSPAPER_MORNING_SOFT_v1.json');
const NP_PACK = JSON.parse(fs.readFileSync(NP_PACK_PATH, 'utf8'));
const NP_WIN_IDS = ['np_win_film_01','np_win_film_02','np_win_tv_01','np_win_tv_02',
  'np_win_music_01','np_win_music_02','np_win_ad_01','np_win_ad_02'];
const NP_BANNED = OLD_LABELS.concat(['街外最記得住的一鏡', '臨記組', '最受歡迎']);
const npWin = (NP_PACK.templates && NP_PACK.templates.award_win) || [];
ok('報紙：pack 有 8 款 award_win 模板', npWin.length === 8);
ok('報紙：AWARDS188_NP_WIN 蓋晒 8 款 id', NP_WIN_IDS.every(id => !!AWARDS188_NP_WIN[id]));
const npCopy = JSON.parse(JSON.stringify(NP_PACK));
/* 真實 load 次序：textfix55 → venue99 → v188——沙盒要照順序行兩個 overlay，
   否則 film_02／music_02／ad_02 嘅 dek（VENUE99 嗰邊改）會誤判為未覆寫。 */
for (const c of ['VENUE99_INVITE_DEK','VENUE99_PRESS_DEK','VENUE99_NEWS_LINE','VENUE99_NP_DEK'])
  eval(extractConst(c).replace('const '+c+' =', 'var '+c+' ='));
eval(extractFn('venue99ApplyOverlay'));
const FW188 = { awardsStub: {}, newspaperStub: npCopy };
venue99ApplyOverlay(FW188);
const npNomBefore188 = JSON.stringify((npCopy.templates && npCopy.templates.award_nominee) || []);
awards188ApplyNpOverlay(FW188);
const npWinAfter = (npCopy.templates && npCopy.templates.award_win) || [];
let npDirty = [];
npWinAfter.forEach(t => {
  ['headline','dek','clipLabel'].forEach(f => {
    const v = String((t && t[f]) || '');
    NP_BANNED.forEach(b => { if (v.indexOf(b) >= 0) npDirty.push(t.id + ':' + f + ':' + b); });
  });
});
ok('報紙：覆寫後 8 款 win 模板 headline／dek／clipLabel 零舊名', npDirty.length === 0);
if (npDirty.length) console.log('  dirty: ' + npDirty.join(' | '));
const npNom = (npCopy.templates && npCopy.templates.award_nominee) || [];
let nomDirty = [];
npNom.forEach(t => {
  ['headline','dek','clipLabel'].forEach(f => {
    const v = String((t && t[f]) || '');
    NP_BANNED.forEach(b => { if (v.indexOf(b) >= 0) nomDirty.push(t.id + ':' + f + ':' + b); });
  });
});
ok('報紙：4 款 nominee 模板本身已乾淨（唔使覆寫）', npNom.length === 4 && nomDirty.length === 0);
ok('報紙：v188 覆寫唔郁 nominee 模板（只改 award_win）',
  JSON.stringify(npNom) === npNomBefore188);

console.log(fails.length ? ('\nFAILED: '+fails.length) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
