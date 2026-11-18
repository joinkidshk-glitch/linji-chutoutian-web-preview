// v20a285：RIVAL_CFG 錯配修正——決戰通告由 film_109（廖引薦《笑聲震天響》男配角）
// 改返 film_102（《霓虹夜影》男主角，rival trigger）。
// 斷言：CFG 指向 film_102；rivalryGigForRound 第 1／2／3 輪都回 film_102；
// GIGS 只有 film_109 嗰陣回 null（對手線唔會再開出《笑聲震天響》）；
// film_109 本身嘅廖引薦接駁唔郁；第 1 輪 rivalryTick 開局出 film_102。
// 用法：node tests/test_r285_rival_cfg.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const gigsPath = path.join(__dirname, '..', 'content', 'gigs_new.json');
const gigData = JSON.parse(fs.readFileSync(gigsPath, 'utf8'));
const gigList = Array.isArray(gigData) ? gigData : gigData.gigs;
const gigById = (id) => gigList.find(g => g && g.id === id);
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
function extractBlock(start){
  let depth=0, j=start;
  for(; j<html.length; j++){
    if(html[j]==='{' || html[j]==='[') depth++;
    else if(html[j]==='}' || html[j]===']'){ depth--; if(depth===0) break; }
  }
  return html.slice(start, j+1);
}
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0){ console.log('FAIL 抽唔到 function '+name); process.exit(1); }
  const b = html.indexOf('{', i);
  return html.slice(i, b) + extractBlock(b);
}
function extractConst(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0){ console.log('FAIL 抽唔到 const '+name); process.exit(1); }
  const e = html.indexOf('=', i);
  let b = e+1;
  while(html[b]!=='{' && html[b]!=='[') b++;
  return 'var ' + name + ' = ' + extractBlock(b) + ';';
}
eval(extractConst('RIVAL_CFG'));
eval(extractConst('RIVAL_FACEOFF_GIGS'));
for(const f of ['ensureRivalry','rivalryStance','rivalryScore','rivalryGigForRound','rivalryTick','isGigConsumed'])
  eval(extractFn(f));

/* ---- 靜態＋數據 ---- */
ok('R1 RIVAL_CFG.gigId 係 film_102', RIVAL_CFG.gigId === 'gig_1991_film_102');
const f102 = gigById('gig_1991_film_102');
ok('R2 film_102 係《霓虹夜影》男主角／高級／rival trigger rivalScoreMin 3',
  !!f102 && f102.title === '《霓虹夜影》男主角' && f102.tier === '高級' &&
  f102.trigger && f102.trigger.kind === 'rival' && f102.trigger.rivalScoreMin === 3);
const f109 = gigById('gig_1991_film_109');
ok('R3 film_109 唔郁：仍係《笑聲震天響》男配角／初級／廖引薦 credit_enc83_liu_patron',
  !!f109 && f109.title === '《笑聲震天響》男配角' && f109.tier === '初級' &&
  f109.trigger && f109.trigger.kind === 'credit' && f109.trigger.creditId === 'credit_enc83_liu_patron');
ok('R4 index.html 入面 RIVAL_CFG 嗰行唔再提 film_109',
  (function(){
    const i = html.indexOf('const RIVAL_CFG =');
    const line = html.slice(i, html.indexOf('\n', i));
    return line.indexOf('gig_1991_film_102') >= 0 && line.indexOf('gig_1991_film_109') < 0;
  })());
ok('R5 mergeRivalGigs 註解已改 film_102',
  html.indexOf('RIVAL_CFG.gigId＝gig_1991_film_102') >= 0);

/* ---- 邏輯：rivalryGigForRound ---- */
var S = null;
var GIGS = [];
var toasts = [];
var toast = function(s){ toasts.push(String(s)); };
var saveQ = function(){};
var bumpNpc = function(){};
var readDualTracks = function(s){ return { stageVolume:(s.fame||0), industryCredit:(s.industryCredit||0) }; };
var syncDualTracks = function(){};
var ensureMockJournal = function(){};
var syncNotebookMirror = function(){};
var newspaperEventSeen = function(){ return false; };
var enqueueNewspaperItem = function(){ return null; };
var isGigWrapped = function(){ return false; };
var isGigInProduction = function(){ return false; };
function freshS(){
  return {
    dayIndex:100, fame:5, popularity:3, industryCredit:10,
    money:12000, stress:0,
    story:{ done:{N1:true,N2:true,N3:true}, flags:{rival_gao_hard:true} },
    flags:{rival_gao_hard:true},
    newspaperQueue:[], newspaperClippings:[{topicKey:'rival:gao', eventKey:'story:N3'}],
    wrapHistory:[], pendingAud:[], npcs:{ rival:6 }
  };
}
S = freshS();
GIGS = [Object.assign({}, f102)];
ok('R6 rivalryGigForRound(1) 回 film_102（未消費）',
  (function(){ const g = rivalryGigForRound(1); return !!g && g.id === 'gig_1991_film_102'; })());
ok('R7 rivalryGigForRound(2) 回 film_102（第 2 輪重用同一張 id）',
  (function(){ const g = rivalryGigForRound(2); return !!g && g.id === 'gig_1991_film_102'; })());
ok('R8 rivalryGigForRound(3) 回 film_102（第 3 輪重用同一張 id）',
  (function(){ const g = rivalryGigForRound(3); return !!g && g.id === 'gig_1991_film_102'; })());
S.pendingAud = [{ gigId:'gig_1991_film_102' }];
ok('R9 film_102 已消費（等消息）→ rivalryGigForRound 回 null（閘住唔開局）',
  rivalryGigForRound(1) === null);
S.pendingAud = [];
GIGS = [Object.assign({}, f109)];
ok('R10 GIGS 只有 film_109 → rivalryGigForRound 回 null（對手線唔會再開出《笑聲震天響》）',
  rivalryGigForRound(1) === null && rivalryGigForRound(2) === null);

/* ---- ensureRivalry 預設＋第 1 輪開局 ---- */
S = freshS();
S.rivalry = null;
ensureRivalry();
ok('R11 ensureRivalry 預設 gigId 係 film_102', S.rivalry && S.rivalry.gigId === 'gig_1991_film_102');
S = freshS();
S.rivalry = { score:0, faceoffState:'none', openedDay:null, settledDay:null, stance:'',
  round:1, gigId:null, nextOpenDay:null, lastResult:'', wins:0, newsIdx:0, workTitle:'' };
GIGS = [Object.assign({}, f102)];
toasts.length = 0;
rivalryTick();
ok('R12 第 1 輪開局：score 3＋有 film_102 → open、gigId film_102、workTitle 霓虹夜影',
  S.rivalry.faceoffState === 'open' && S.rivalry.gigId === 'gig_1991_film_102' &&
  S.rivalry.workTitle === '霓虹夜影' && S.rivalry.round === 1);

console.log('\n' + (fails.length ? ('FAILED: ' + fails.length + ' — ' + fails.join('；')) : 'ALL PASS'));
process.exit(fails.length ? 1 : 0);
