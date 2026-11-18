// P7-board-r2 focused（B5）：輸咗第 1 輪 → 冷卻期滿，
// rivalryTick 輪次次序修正——先閘通告存在，後先＋1 開局（B3 係先＋1 後閘住，冷卻期滿會燒輪次）；
// GIGS 無新庫通告 gig_1991_film_102 嗰陣，冷卻期滿唔燒輪次（round 留 1、faceoffState 留 none、唔 toast）；
// GIGS 有呢張通告嗰陣開第 2 輪（round→2、state open、gigId 係新 id、toast 有出）。
// 板面過濾（觸發前隱藏／觸發後上板）見 tests/test_gig229_trigger.js T4。
// 用法：node tests/test_rival_board_r2.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
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
eval(extractConst('RIVAL_NEWS_SLOTS'));
for(const f of ['ensureRivalry','rivalryStance','rivalryC3Done','rivalryScore','rivalryWinThreshold',
  'rivalryGigForRound','rivalryRoundSuffix','rivalryTick','rivalryNewsTick','rivalryFaceoffPaper',
  'mergeRivalGigs','rivalryStatusLine','rivalTookRoleLine',
  'normalizeGigRecord','seasonRank','gigSeasonHidden88','gigSeasonEarlyVisible88',
  'gigBoardPosted92','nat92StaggerEligible','nat92PostIntervals','isGigConsumed',
  'boardSortCompare','boardPriorityRank','boardNotePlayerOk','looksLikeEraId','humanizeEraId',
  'gigsForLocSeasonBoard'])
  eval(extractFn(f));

/* ---- 世界 stub ---- */
var S = null;
var GIGS = [];
var toasts = [];
var papers = [];
var seenKeys = new Set();
function freshS(){
  return {
    dayIndex:244, fame:5, popularity:3, industryCredit:10,
    money:12000, stress:0,
    story:{ done:{N1:true,N2:true,N3:true,N4:true,N5:true,N6:true,N7:true,N9:true}, flags:{rival_gao_hard:true} },
    flags:{rival_gao_hard:true},
    newspaperQueue:[], newspaperClippings:[{topicKey:"rival:gao", eventKey:"story:N3"}],
    wrapHistory:[], pendingAud:[],
    npcs:{ rival:6 }
  };
}
var toast = function(s){ toasts.push(String(s)); };
var saveQ = function(){};
var bumpNpc = function(id, d){ S.npcs[id] = Math.max(0, Math.min(100, (S.npcs[id]||0)+d)); };
var readDualTracks = function(s){ return { stageVolume:(s.fame||0), industryCredit:(s.industryCredit||0) }; };
var syncDualTracks = function(s){ return { stageVolume:s.fame||0, industryCredit:s.industryCredit||0 }; };
var ensureMockJournal = function(){ if(!Array.isArray(S.mockRumors)) S.mockRumors = []; };
var syncNotebookMirror = function(){};
var newspaperEventSeen = function(key){ return seenKeys.has(key); };
var enqueueNewspaperItem = function(raw){
  if(!raw || !raw.eventKey) return null;
  if(seenKeys.has(raw.eventKey)) return null;
  seenKeys.add(raw.eventKey);
  const it = Object.assign({}, raw);
  papers.push(it); S.newspaperQueue.push(it);
  return it;
};
var fmtNewspaperDate = function(day){ return 'D'+(day|0); };
var calendarSeason = function(){ return '秋'; };
var isGigWrapped = function(){ return false; };
var isGigInProduction = function(){ return false; };
var mergeSoftBridgeGigs = function(){};
var mergeIntelGigs = function(){};
var mergeFavorGigs = function(){};
var mergeWf3Gigs = function(){};
var mergeBr89Gigs = function(){};
var mergeExodusGigs = function(){};
var mergeMidGigs35 = function(){};
var mergeWinterBridge88 = function(){};
var mergeYearGigs36 = function(){};
var mergeNat92Gigs = function(){};

/* ---- 播種：輸咗第 1 輪（run10 P6 實測狀態），day 243，冷卻期滿 244 ---- */
S = freshS();
S.dayIndex = 243;
S.rivalry = {score:4, faceoffState:"none", openedDay:150, settledDay:154, stance:"hard",
  round:1, gigId:"gig_rival_stale_r1", nextOpenDay:244, lastResult:"lost", wins:0,
  newsIdx:1, workTitle:"霓虹夜影", settledDual:18};
GIGS = [{ id:'other_gig', loc:'film_lion', season:'不限', tier:'初', type:'電影' }];
rivalryTick(); // day 243：未到期，唔開
ok('冷卻期內（day 243）唔開第 2 輪', S.rivalry.faceoffState === 'none' && S.rivalry.round === 1);
S.dayIndex = 244;
rivalryTick(); // 期滿：GIGS 無新庫通告 → 唔燒輪次（B5 次序修正：先閘後＋1）
ok('B2 B5 期滿無通告：round 唔＋1（留 1）、faceoffState 留 none、gigId／作品名唔郁、唔 toast',
  S.rivalry.faceoffState === 'none' && S.rivalry.round === 1 &&
  S.rivalry.gigId === 'gig_rival_stale_r1' && S.rivalry.workTitle === '霓虹夜影' &&
  toasts.length === 0);
ok('B3 rivalryGigForRound(2) 回 null（GIGS 無新庫通告）', rivalryGigForRound(2) === null);
ok('B4 mergeRivalGigs 係 no-op（唔加通告；新庫決戰通告經 trigger 系統上板）',
  (function(){ const n = GIGS.length; mergeRivalGigs(); return GIGS.length === n && !GIGS.some(g=>/^gig_rival_/.test(g.id)); })());

// (B5) B5 供新庫通告 → 開第 2 輪
S = freshS();
S.dayIndex = 244;
S.rivalry = {score:4, faceoffState:"none", openedDay:150, settledDay:154, stance:"hard",
  round:1, gigId:"gig_rival_stale_r1", nextOpenDay:244, lastResult:"lost", wins:0,
  newsIdx:1, workTitle:"霓虹夜影", settledDual:18};
GIGS = [{ id:'gig_1991_film_102', loc:'film_cotton', season:'秋', tier:'高級', type:'電影', title:'《霓虹夜影》男主角', workTitle:'霓虹夜影' }];
toasts.length = 0;
rivalryTick(); // 期滿＋有通告 → 開第 2 輪
ok('B5 供新庫通告 → 開第 2 輪（round→2、state open、gigId 係新 id、toast 有出）',
  S.rivalry.round===2 && S.rivalry.faceoffState==='open' && S.rivalry.gigId==='gig_1991_film_102' &&
  S.rivalry.workTitle==='霓虹夜影' && toasts.length===1 && toasts[0].indexOf('霓虹夜影')>=0);
ok('B6 開局唔改 nextOpenDay（冷卻只喺結算嗰陣先設：settledDay＋90）', S.rivalry.nextOpenDay===244);

// 還原 B3 播種板面檢查用嘅世界
S = freshS();
S.dayIndex = 244;
S.rivalry = {score:4, faceoffState:"none", openedDay:150, settledDay:154, stance:"hard",
  round:1, gigId:"gig_rival_stale_r1", nextOpenDay:244, lastResult:"lost", wins:0,
  newsIdx:1, workTitle:"霓虹夜影", settledDual:18};
GIGS = [{ id:'other_gig', loc:'film_lion', season:'不限', tier:'初', type:'電影' }];

var filmBoard = gigsForLocSeasonBoard('film_lion', '秋');
var filmIds = filmBoard.map(g=>g.id);
console.log('film_lion 板：', JSON.stringify(filmIds));
ok("B7 film 板冇《火線街頭》(r2)", !filmIds.some(id=>/^gig_rival_/.test(id)));
ok("B8 film 板冇《霓虹夜影》(r1)", !filmIds.some(id=>/^gig_rival_/.test(id)));
var tvBoard = gigsForLocSeasonBoard('tvb_longmen', '秋');
var tvIds = tvBoard.map(g=>g.id);
console.log('tvb_longmen 板：', JSON.stringify(tvIds));
ok("B9 星河電視台板唔再有《霓虹夜影》(r1)", !tvIds.some(id=>/^gig_rival_/.test(id)));

console.log('\n' + (fails.length ? ('FAILED: ' + fails.length + ' — ' + fails.join('；')) : 'ALL PASS'));
process.exit(fails.length ? 1 : 0);
