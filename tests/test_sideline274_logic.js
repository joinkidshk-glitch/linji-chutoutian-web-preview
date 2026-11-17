// v20a274 取代票測試：6 張支線人情引薦通告取代（開 5 張新＋駱接駁 rec_111＋拆 6 張舊 trigger）
//   A 庫對位：287 張／trigger 33／credit 23；每筆債權只兌現一張；新 gig 欄位齊；rec_111 接駁；舊 6 張無 trigger＋無引薦字句
//   B 開閘：新 gig 無債權唔開／持債權開＋標「引薦」；舊 gig 持債權都唔經 BR89 開
//   C R-4：還錢路開新顧 gig（rec_205）唔開舊 rec_105
//   D BR89 映射 13 張逐對啱（新對位）
// 用法：node tests/test_sideline274_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond, extra){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name+(extra?' :: '+extra:'')); }
function deepClone(o){ return JSON.parse(JSON.stringify(o)); }
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) return null;
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){ if(html[j]==='{') depth++; else if(html[j]==='}'){ depth--; if(depth===0) break; } }
  return html.slice(i, j+1);
}
function extractConstVar(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) return null;
  let depth=0, started=false;
  for(let k=i; k<html.length; k++){
    const ch = html[k];
    if(ch==='{'||ch==='['){ depth++; started = true; }
    else if(ch==='}'||ch===']'){ depth--; if(started && depth===0) return html.slice(i, k+1).replace('const '+name, 'var '+name)+';'; }
    else if(ch===';' && !started) return html.slice(i, k+1).replace('const '+name, 'var '+name);
  }
  return null;
}

const pack = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gigs_new.json'), 'utf8'));
const gigs = pack.gigs || [];
const gigById = id => gigs.find(g=>g.id===id);

/* ---------- eval 沙盒：trigger＋BR89 模組（同 test_gig229_trigger.js 口徑） ---------- */
eval(extractConstVar('BR89_PATRON_OF_GIG'));
eval(extractConstVar('GIG_TRIGGER_AWARD_MAP229'));
eval(extractConstVar('RIVAL_CFG'));
eval(extractConstVar('RIVAL_FACEOFF_GIGS'));
for(const f of ['br89HasCredit','br89GigOn','awardTriggerOn229','rivalTriggerOpenable229',
  'triggerGigOn','triggerGigLabel229','triggerGigLocName229','mergeTriggerGigs',
  'ensureAwardsResults','recordAwardResult','rivalryScore','ensureRivalry',
  'rivalryGigForRound','enc79TierOf','gigsForLocSeasonBoard']){
  const src = extractFn(f);
  if(!src){ ok('抽取 function '+f, false); }
  else eval(src);
}
var S = null;
var GIGS = [];
var window = {};
var LOCS = [
  { id:'film_lion', name:'獅子山製片' }, { id:'film_cotton', name:'紅棉影業' },
  { id:'film_harbour', name:'維港電影' }, { id:'tvb_longmen', name:'星河電視台' },
  { id:'tvb_kowloon', name:'九龍電視台' }, { id:'tvb_harbour', name:'海港廣播' },
  { id:'rec_star', name:'天星音樂' }, { id:'rec_hk', name:'香江唱片' },
  { id:'rec_wanchai', name:'灣仔唱片' }, { id:'ad_central', name:'中環廣告' },
  { id:'ad_adm', name:'金鐘創意' }
];
var toasts = [];
var toast = function(m){ toasts.push(String(m)); };
var calendarSeason = function(){ return '秋'; };
var gigSeasonHidden88 = function(){ return false; };
var gigBoardPosted92 = function(){ return false; };
var isGigConsumed = function(){ return false; };
var boardSortCompare = function(){ return 0; };
var normalizeGigRecord = function(g){ return g; };
var mergeSoftBridgeGigs = function(){};
var mergeFavorGigs = function(){};
var mergeWf3Gigs = function(){};
var mergeBr89Gigs = function(){};
var mergeRivalGigs = function(){};
var mergeExodusGigs = function(){};
var mergeMidGigs35 = function(){};
var mergeWinterBridge88 = function(){};
var mergeYearGigs36 = function(){};
var mergeNat92Gigs = function(){};
function freshS(){
  return {
    dayIndex: 600, fame: 0, popularity: 0, industryCredit: 0, money: 12000, stress: 0,
    story: { done: {}, flags: {}, rel: {} },
    flags: {}, npcs: {}, stars: {}, mockCredits: [], mockDebts: [], mockRumors: [],
    newspaperClippings: [], wrapHistory: [], pendingAud: [],
    awardsLog: [], awardsFlags: {}, awardsResults: {},
    rivalry: { score: 0, faceoffState: 'none', openedDay: null, settledDay: null, stance: '',
      round: 1, gigId: null, nextOpenDay: null, lastResult: '', wins: 0, newsIdx: 0, workTitle: '' }
  };
}
function giveCredit(id, debtor){ S.mockCredits.push({ id, debtor, title:'引薦', line:'x', status:'未收' }); }

/* 新 6 對（債權 → 兌現 gig）＋舊 6 張 */
const NEW6 = [
  ['credit_enc83_mak_patron', 'gig_1991_film_211'],
  ['credit_enc83_lok_patron', 'gig_1992_rec_111'],
  ['credit_enc83_ngai_patron', 'gig_1991_film_212'],
  ['credit_enc83_chai_patron', 'gig_1992_film_206'],
  ['credit_enc84_chung_patron', 'gig_1991_film_213'],
  ['credit_enc83_gu_patron', 'gig_1992_rec_205'],
];
const OLD6 = ['gig_1991_film_110', 'gig_1992_rec_102', 'gig_1991_film_111',
  'gig_1992_tv_104', 'gig_1991_tv_108', 'gig_1992_rec_105'];

/* ---------- A：庫對位 ---------- */
ok('A1 庫 289 張', gigs.length===289, 'n='+gigs.length);
const trig = gigs.filter(g=>g.trigger && g.trigger.kind);
ok('A1 trigger 34 張（credit 23）', trig.length===34 && trig.filter(g=>g.trigger.kind==='credit').length===23,
  'trig='+trig.length+' credit='+trig.filter(g=>g.trigger.kind==='credit').length);
ok('A2 每筆債權只兌現一張（新 6 對）', NEW6.every(([c, id])=>{
  const hits = gigs.filter(g=>g.trigger && g.trigger.kind==='credit' && g.trigger.creditId===c);
  return hits.length===1 && hits[0].id===id;
}), NEW6.map(([c, id])=>c+'→'+id).join(', '));
ok('A3 新 5 張欄位齊（媒介／級／作品／年季／trigger／引薦字句／posterBrief／pay 帶）', (()=> {
  const want = {
    'gig_1991_film_211': ['電影', '中級', 1991, '春'],
    'gig_1991_film_212': ['電影', '高級', 1991, '夏'],
    'gig_1992_film_206': ['電影', '中級', 1992, '秋'],
    'gig_1991_film_213': ['電影', '中級', 1991, '秋'],
    'gig_1992_rec_205': ['唱片通告', '中級', 1992, '春'],
  };
  return Object.keys(want).every(id=>{
    const g = gigById(id); if(!g) return false;
    const [type, tier, year, season] = want[id];
    return g.type===type && g.tier===tier && g.category==='作品' && g.year===year && g.season===season
      && g.trigger && g.trigger.kind==='credit' && (g.discoverNote||'').indexOf('引薦')>=0
      && (g.blurb||'').indexOf('引薦')>=0 && !!g.posterBrief
      && g.pay && g.pay[1] <= g.pay[0]*1.25;
  });
})());
ok('A4 rec_111 接駁：trigger 駱債權＋singer 仍係陸柏言＋引薦字句', (()=> {
  const g = gigById('gig_1992_rec_111');
  return !!g && g.trigger && g.trigger.kind==='credit' && g.trigger.creditId==='credit_enc83_lok_patron'
    && g.trigger.creditOwner==='駱家聲' && g.singer==='luk_baakyin'
    && (g.discoverNote||'').indexOf('駱家聲引薦')>=0 && (g.blurb||'').indexOf('駱家聲引薦')>=0;
})());
ok('A5 舊 6 張全部無 trigger', OLD6.every(id=>{ const g=gigById(id); return !!g && !g.trigger; }), OLD6.join(','));
ok('A6 舊 6 張 blurb／synopsis 無「引薦」字句', OLD6.every(id=>{
  const g=gigById(id); return (g.blurb||'').indexOf('引薦')<0 && (g.synopsis||'').indexOf('引薦')<0;
}));

/* ---------- B：開閘 ---------- */
S = freshS();
ok('B1 新 6 張無債權 → 唔開（trigger＋BR89 兩路）', NEW6.every(([, id])=>{
  const g = gigById(id); return triggerGigOn(g)===false && br89GigOn(g)===false;
}));
for(const [c, id] of NEW6){
  S = freshS();
  giveCredit(c, 'x');
  const g = gigById(id);
  ok('B2 持債權 → 開＋標「引薦」：'+id, triggerGigOn(g)===true && br89GigOn(g)===true && triggerGigLabel229(g)==='引薦');
}
S = freshS();
NEW6.forEach(([c])=>giveCredit(c, 'x'));
ok('B3 舊 6 張持債權 → BR89 唔開（唔再係引薦通告）', OLD6.every(id=>br89GigOn(gigById(id))===false));
ok('B4 舊 6 張無 trigger → 普通板通告（triggerGigOn 照常開，唔經 credit 閘）',
  OLD6.every(id=>triggerGigOn(gigById(id))===true));

/* ---------- C：R-4 還錢路 ---------- */
S = freshS();
const gGu = gigById('gig_1992_rec_205'), gOldGu = gigById('gig_1992_rec_105');
ok('C1 R-4 兩條路都冇 → 新顧 gig 唔開', triggerGigOn(gGu)===false && br89GigOn(gGu)===false);
S.flags.enc83_gu_loan_result = 1;
ok('C1 R-4 還錢結算完成（result＝1）→ 新顧 gig 開（唔使持債）', triggerGigOn(gGu)===true && br89GigOn(gGu)===true);
ok('C1 R-4 還錢路唔開舊 rec_105', br89GigOn(gOldGu)===false);
S.flags.enc83_gu_loan_result = 2;
ok('C1 R-4 還錢失敗（result＝2）→ 新顧 gig 唔開', triggerGigOn(gGu)===false && br89GigOn(gGu)===false);
S = freshS();
giveCredit('credit_enc83_gu_patron', '顧明輝');
ok('C2 R-4 持債權 → 新顧 gig 開', br89GigOn(gGu)===true);
S.mockCredits[0].redeemedBy = 'gig_1992_rec_205';
ok('C2 R-4 債權已兌現 → 新顧 gig 落板', br89GigOn(gGu)===false);

/* ---------- D：BR89 映射 ---------- */
const EXPECT13 = {
  gig_1991_film_101:'credit_enc83_luk_patron', gig_1991_variety_203:'credit_enc84_pang_patron',
  gig_1992_rec_106:'credit_enc84_ching_patron', gig_1991_film_103:'credit_enc79_liu_priority',
  gig_1992_film_103:'credit_enc83_liu_patron', gig_1991_film_211:'credit_enc83_mak_patron',
  gig_1992_tv_105:'credit_enc83_yip_patron', gig_1992_rec_205:'credit_enc83_gu_patron',
  gig_1991_ad_102:'credit_enc84_so_patron', gig_1991_film_213:'credit_enc84_chung_patron',
  gig_1992_rec_111:'credit_enc83_lok_patron', gig_1991_film_212:'credit_enc83_ngai_patron',
  gig_1992_film_206:'credit_enc83_chai_patron',
  gig_1992_film_202:'credit_wf3_comedy_crew',
  gig_1992_film_114:'credit_enc83_luk_patron'
};
ok('D1 BR89 映射 15 張逐對啱（v274 新對位＋v279 收割鏈＋v284 film_114）',
  Object.keys(BR89_PATRON_OF_GIG).length===15 &&
  Object.keys(EXPECT13).every(k=>BR89_PATRON_OF_GIG[k]===EXPECT13[k]));
ok('D2 BR89 15 張全部喺庫＋trigger.creditId 對位',
  Object.keys(BR89_PATRON_OF_GIG).every(id=>{ const g=gigById(id);
    return !!g && g.trigger && g.trigger.kind==='credit' && g.trigger.creditId===BR89_PATRON_OF_GIG[id]; }));
ok('D3 舊 6 張 id 唔再喺 BR89 映射入面', OLD6.every(id=>!(id in BR89_PATRON_OF_GIG)));

console.log('');
console.log(fails.length ? ('FAILED: '+fails.length+' -> '+fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
