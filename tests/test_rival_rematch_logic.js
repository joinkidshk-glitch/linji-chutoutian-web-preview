// 對手線強化票・邏輯測試：
// (1) 決戰通告三則齊全、無假限期、形狀同 R1 一致；
// (2) 再鬥循環：第 1 輪贏→冷卻 90 日→第 2 輪輸→冷卻→第 3 輪贏→終態；門檻 hard 46／endure 34／無態度 40；
// (3) R6a：逾期掉單（done_＋fail_shoot_）唔結算；
// (4) 舊檔遷移：won 舊檔轉 none＋nextOpenDay；第 3 輪終態唔郁；
// (5) R2 快訊：固定日槽、每則一次、N3 未做唔出；
// (6) R1 狀態行：open 講門檻＋雙軌、冷卻講下一場、終態講三場贏幾場；
// (7) R3 落選後續：電視劇／電影＋N3＋隨機細先出，每通告一次，決戰通告唔出；
// (8) mergeRivalGigs 只注入當輪嗰張。
// 反證：對 pristine main 行 → RIVAL_FACEOFF_GIGS 得一則／rivalryNewsTick／rivalryStatusLine 唔存在 → 乾淨 FAIL。
// 用法：node tests/test_rival_rematch_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
const ASSERT_NAMES = [
  '決戰通告三則：id／作品名各異','決戰通告無 applyDeadlineDays（假限期已刪）',
  '決戰通告 shootBand [1,1]、片酬 1200、req 空',
  '門檻：hard 46／endure 34／無態度 40',
  '第 1 輪：夠分開閘，round 1、gig r1、作品 霓虹夜影',
  '第 1 輪贏：結算後返 none、冷卻 90 日、wins 1、報紙 eventKey 無後綴',
  '冷卻期內唔重開；期滿開第 2 輪，gig r2、作品 火線街頭',
  '第 2 輪輸：返 none、再冷卻、wins 唔變、報紙 eventKey 有 _r2、傳聞 id 有 _r2',
  '第 3 輪贏：終態 won、wins 2、再行 tick 都唔變',
  'R6a：掉單（done_＋fail_shoot_）唔結算；清 fail 旗先結算',
  '舊檔遷移：won 舊檔轉 none＋nextOpenDay＝settled＋90、wins 補 1',
  '舊檔遷移：第 3 輪 won 終態唔郁',
  'R2 快訊：day150 出第 1 則、newsIdx 1；同日再行唔重複；day330 出第 2 則',
  'R2 快訊：N3 未做唔出；未到日子唔出',
  'R1 狀態行：open 講門檻同雙軌即時值',
  'R1 狀態行：冷卻講下一場日期；終態講三場贏幾場',
  'R3 落選：電視劇＋N3＋隨機細 → 有行＋閒話入帳',
  'R3 落選：同一通告第二次唔再出；決戰通告唔出；隨機大唔出',
  'mergeRivalGigs：open 只注入當輪嗰張；唔開就三張都清走'
];
function cleanFailMissing(what){
  console.log('抽唔到 ' + what + '（呢個版本冇對手線強化票）：以下斷言全部 FAIL');
  ASSERT_NAMES.forEach(n=>{ console.log('FAIL ' + n); fails.push(n); });
  console.log('\nFAILED: ' + fails.length);
  process.exit(1);
}
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
  if(i<0) cleanFailMissing('function ' + name);
  const b = html.indexOf('{', i);
  return html.slice(i, b) + extractBlock(b);
}
function extractConst(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) cleanFailMissing('const ' + name);
  const e = html.indexOf('=', i);
  let b = e+1;
  while(html[b]!=='{' && html[b]!=='[') b++;
  // eval 嘅 const 唔會漏出作用域，改 var 先 eval。
  return 'var ' + name + ' = ' + extractBlock(b) + ';';
}
eval(extractConst('RIVAL_CFG'));
eval(extractConst('RIVAL_FACEOFF_GIGS'));
eval(extractConst('RIVAL_NEWS_SLOTS'));
for(const f of ['ensureRivalry','rivalryStance','rivalryC3Done','rivalryScore','rivalryWinThreshold','rivalryGigForRound','rivalryRoundSuffix','rivalryTick','rivalryNewsTick','rivalryFaceoffPaper','rivalryResultRumor','mergeRivalGigs','rivalryStatusLine','rivalTookRoleLine'])
  eval(extractFn(f));

/* ---- 世界 stub ---- */
var S = null;
var GIGS = [];
var toasts = [];
var saved = 0;
var papers = [];
var seenKeys = new Set();
function freshS(){
  return {
    dayIndex:0, fame:5, popularity:3, industryCredit:10, industryCreditDelta:0,
    money:12000, stress:12,
    story:{ done:{}, flags:{} }, flags:{},
    mockRumors:[], newspaperQueue:[], newspaperClippings:[], wrapHistory:[],
    npcs:{ rival:6 }
  };
}
var toast = function(s){ toasts.push(String(s)); };
var saveQ = function(){ saved++; };
var bumpNpc = function(id, d){ S.npcs[id] = Math.max(0, Math.min(100, (S.npcs[id]||0)+d)); };
var readDualTracks = function(s){ return { stageVolume:(s.fame||0), industryCredit:(s.industryCredit||0) }; };
var syncDualTracks = function(s){ s.stageVolume = s.fame||0; s.industryCredit = s.industryCredit||0; return { stageVolume:s.fame||0, industryCredit:s.industryCredit||0 }; };
var ensureMockJournal = function(){ if(!Array.isArray(S.mockRumors)) S.mockRumors = []; };
var syncNotebookMirror = function(){};
var normalizeGigRecord = function(g){ return Object.assign({}, g); };
var newspaperNameTier = function(){ return 'named'; };
var newspaperPlayerRef = function(){ return '阿偉'; };
var fmtNewspaperDate = function(day){ return 'D'+(day|0); };
var enqueueNewspaperItem = function(raw){
  if(!raw || !raw.eventKey) return null;
  if(seenKeys.has(raw.eventKey)) return null;
  seenKeys.add(raw.eventKey);
  const it = Object.assign({}, raw);
  papers.push(it);
  S.newspaperQueue.push(it);
  return it;
};
var newspaperEventSeen = function(key){ return seenKeys.has(key); };
function c3done(){
  S.story.done.N3 = true;
  S.story.flags.rival_gao_hard = true;
}
function score3(){
  c3done();
  S.mockRumors.push({ id:'gao_steal_spotlight' });
  S.newspaperClippings.push({ topicKey:'rival:gao', eventKeys:['story:N3:hard'] });
}

/* ---- (1) 通告形狀 ---- */
ok('決戰通告三則：id／作品名各異',
  RIVAL_FACEOFF_GIGS.length===3 &&
  RIVAL_FACEOFF_GIGS[0].id==='gig_rival_gao_faceoff' && RIVAL_FACEOFF_GIGS[0].workTitle==='霓虹夜影' &&
  RIVAL_FACEOFF_GIGS[1].id==='gig_rival_gao_faceoff_r2' && RIVAL_FACEOFF_GIGS[1].workTitle==='火線街頭' &&
  RIVAL_FACEOFF_GIGS[2].id==='gig_rival_gao_faceoff_r3' && RIVAL_FACEOFF_GIGS[2].workTitle==='再見江湖');
ok('決戰通告無 applyDeadlineDays（假限期已刪）',
  RIVAL_FACEOFF_GIGS.every(g=> g.applyDeadlineDays==null));
ok('決戰通告 shootBand [1,1]、片酬 1200、req 空',
  RIVAL_FACEOFF_GIGS.every(g=> Array.isArray(g.shootBand) && g.shootBand[0]===1 && g.shootBand[1]===1 && g.payExact===1200 && g.req && Object.keys(g.req).length===0 && g.shootDeadlineDays===14));

/* ---- (2) 門檻 ---- */
ok('門檻：hard 46／endure 34／無態度 40',
  rivalryWinThreshold('hard')===46 && rivalryWinThreshold('endure')===34 && rivalryWinThreshold('')===40);

/* ---- (2) 再鬥循環 ---- */
S = freshS(); S.dayIndex = 100; score3();
rivalryTick();
let r = ensureRivalry();
ok('第 1 輪：夠分開閘，round 1、gig r1、作品 霓虹夜影',
  r.faceoffState==='open' && (r.round|0)===1 && r.gigId==='gig_rival_gao_faceoff' && r.workTitle==='霓虹夜影');
S.wrapHistory = [{ gigId:'gig_rival_gao_faceoff' }];
S.fame = 40; S.industryCredit = 10; // 雙軌 50 ≥ 46（hard）→ 贏
papers = []; seenKeys = new Set();
rivalryTick();
r = ensureRivalry();
ok('第 1 輪贏：結算後返 none、冷卻 90 日、wins 1、報紙 eventKey 無後綴',
  r.faceoffState==='none' && r.nextOpenDay===190 && (r.wins|0)===1 && r.lastResult==='won' &&
  papers.some(p=>p.eventKey==='story:N3:faceoff_win') &&
  S.mockRumors.some(x=>x && x.id==='rival_faceoff_result'));
S.dayIndex = 150; // 冷卻期內
rivalryTick();
ok('冷卻期內唔重開；期滿開第 2 輪，gig r2、作品 火線街頭',
  ensureRivalry().faceoffState==='none' &&
  (S.dayIndex = 190, rivalryTick(), (r = ensureRivalry()).faceoffState==='open' && (r.round|0)===2 && r.gigId==='gig_rival_gao_faceoff_r2' && r.workTitle==='火線街頭'));
S.wrapHistory = [{ gigId:'gig_rival_gao_faceoff_r2' }];
S.fame = 5; S.industryCredit = 10; // 雙軌 15 < 46 → 輸
papers = []; seenKeys = new Set();
rivalryTick();
r = ensureRivalry();
ok('第 2 輪輸：返 none、再冷卻、wins 唔變、報紙 eventKey 有 _r2、傳聞 id 有 _r2',
  r.faceoffState==='none' && r.nextOpenDay===280 && (r.wins|0)===1 && r.lastResult==='lost' &&
  papers.some(p=>p.eventKey==='story:N3:faceoff_lose_r2') &&
  S.mockRumors.some(x=>x && x.id==='rival_faceoff_result_r2'));
S.dayIndex = 280;
rivalryTick();
r = ensureRivalry();
ok('第 3 輪贏：終態 won、wins 2、再行 tick 都唔變',
  r.faceoffState==='open' && (r.round|0)===3 && r.gigId==='gig_rival_gao_faceoff_r3' && r.workTitle==='再見江湖' &&
  (S.wrapHistory = [{ gigId:'gig_rival_gao_faceoff_r3' }], S.fame = 40, S.industryCredit = 10,
   papers = [], seenKeys = new Set(), rivalryTick(),
   (r = ensureRivalry()).faceoffState==='won' && (r.wins|0)===2 &&
   papers.some(p=>p.eventKey==='story:N3:faceoff_win_r3') &&
   (rivalryTick(), ensureRivalry().faceoffState==='won')));

/* ---- (3) R6a 掉單 ---- */
S = freshS(); S.dayIndex = 200;
S.rivalry = { score:3, faceoffState:'open', openedDay:200, settledDay:null, stance:'hard', round:1, gigId:'gig_rival_gao_faceoff', nextOpenDay:null, lastResult:'', wins:0, newsIdx:0, workTitle:'霓虹夜影' };
S.flags['done_gig_rival_gao_faceoff'] = 1;
S.flags['fail_shoot_gig_rival_gao_faceoff'] = 1;
S.fame = 40; S.industryCredit = 10;
papers = []; seenKeys = new Set();
rivalryTick();
let stillOpen = ensureRivalry().faceoffState==='open' && papers.length===0;
delete S.flags['fail_shoot_gig_rival_gao_faceoff'];
rivalryTick();
ok('R6a：掉單（done_＋fail_shoot_）唔結算；清 fail 旗先結算',
  stillOpen && ensureRivalry().faceoffState==='none' && papers.some(p=>p.eventKey==='story:N3:faceoff_win'));

/* ---- (4) 舊檔遷移 ---- */
S = freshS();
S.rivalry = { score:4, faceoffState:'won', openedDay:50, settledDay:100, stance:'hard' };
r = ensureRivalry();
ok('舊檔遷移：won 舊檔轉 none＋nextOpenDay＝settled＋90、wins 補 1',
  r.faceoffState==='none' && r.nextOpenDay===190 && r.lastResult==='won' && (r.wins|0)===1 && (r.round|0)===1 && r.gigId==='gig_rival_gao_faceoff');
S = freshS();
S.rivalry = { score:4, faceoffState:'won', openedDay:50, settledDay:100, stance:'hard', round:3, gigId:'gig_rival_gao_faceoff_r3', nextOpenDay:null, lastResult:'won', wins:2, newsIdx:6, workTitle:'再見江湖' };
r = ensureRivalry();
ok('舊檔遷移：第 3 輪 won 終態唔郁', r.faceoffState==='won' && (r.round|0)===3);

/* ---- (5) R2 快訊 ---- */
S = freshS(); S.dayIndex = 100; c3done();
papers = []; seenKeys = new Set();
rivalryNewsTick();
let n1 = ensureRivalry().newsIdx===0 && papers.length===0;
S.dayIndex = 150;
rivalryNewsTick();
n1 = n1 && ensureRivalry().newsIdx===1 && papers.length===1 && papers[0].eventKey==='story:N3:rival_news_1';
rivalryNewsTick();
n1 = n1 && papers.length===1;
S.dayIndex = 330;
rivalryNewsTick();
ok('R2 快訊：day150 出第 1 則、newsIdx 1；同日再行唔重複；day330 出第 2 則',
  n1 && ensureRivalry().newsIdx===2 && papers.length===2 && papers[1].eventKey==='story:N3:rival_news_2');
S = freshS(); S.dayIndex = 500; // N3 未做
papers = []; seenKeys = new Set();
rivalryNewsTick();
ok('R2 快訊：N3 未做唔出；未到日子唔出',
  papers.length===0 && ensureRivalry().newsIdx===0 &&
  (S.dayIndex = 100, c3done(), rivalryNewsTick(), papers.length===0));

/* ---- (6) R1 狀態行 ---- */
S = freshS(); S.dayIndex = 100; score3();
rivalryTick(); // 開第 1 輪
S.fame = 30; S.industryCredit = 10; // 雙軌 40
let lineOpen = rivalryStatusLine();
let okOpen = lineOpen.indexOf('霓虹夜影')>=0 && lineOpen.indexOf('雙軌合共 46')>=0 && lineOpen.indexOf('而家你係 40')>=0;
S.wrapHistory = [{ gigId:'gig_rival_gao_faceoff' }];
S.fame = 40;
rivalryTick(); // 贏，入冷卻
let lineCool = rivalryStatusLine();
let okCool = lineCool.indexOf('上次爭位你贏咗')>=0 && lineCool.indexOf('下一場約咗 D190')>=0;
S.rivalry.faceoffState = 'won'; S.rivalry.round = 3; S.rivalry.wins = 2;
let lineEnd = rivalryStatusLine();
ok('R1 狀態行：open 講門檻同雙軌即時值', okOpen);
ok('R1 狀態行：冷卻講下一場日期；終態講三場贏幾場',
  okCool && lineEnd.indexOf('三場爭位鬥完，你贏咗 2 場')>=0);

/* ---- (7) R3 落選後續 ---- */
S = freshS(); c3done();
const _rnd = Math.random;
Math.random = ()=>0.1;
let gigTv = { id:'g_test_tv', type:'電視劇', title:'《測試劇》' };
let recTv = { gigId:'g_test_tv', title:'《測試劇》' };
let line1 = rivalTookRoleLine(gigTv, recTv);
let okR3 = line1.indexOf('高俊傑')>=0 && S.mockRumors.some(x=>x && x.id==='rival_took_g_test_tv');
let line2 = rivalTookRoleLine(gigTv, recTv);
okR3 = okR3 && line2==='';
let gigFace = { id:'gig_rival_gao_faceoff_r2', type:'電影', rivalFaceoffGig:true };
okR3 = okR3 && rivalTookRoleLine(gigFace, { gigId:'gig_rival_gao_faceoff_r2', title:'《火線街頭》' })==='';
Math.random = ()=>0.9;
let gigTv2 = { id:'g_test_tv2', type:'電視劇', title:'《測試劇二》' };
okR3 = okR3 && rivalTookRoleLine(gigTv2, { gigId:'g_test_tv2', title:'《測試劇二》' })==='';
Math.random = _rnd;
ok('R3 落選：電視劇＋N3＋隨機細 → 有行＋閒話入帳', line1.indexOf('高俊傑')>=0 && S.mockRumors.some(x=>x && x.id==='rival_took_g_test_tv'));
ok('R3 落選：同一通告第二次唔再出；決戰通告唔出；隨機大唔出', okR3);

/* ---- (8) mergeRivalGigs ---- */
S = freshS(); S.dayIndex = 100; score3();
rivalryTick(); // open round 1
GIGS = [{ id:'other_gig' }];
mergeRivalGigs();
let hasR1 = GIGS.some(g=>g.id==='gig_rival_gao_faceoff');
let hasOther = GIGS.some(g=>g.id==='other_gig');
let noR23 = !GIGS.some(g=>g.id==='gig_rival_gao_faceoff_r2' || g.id==='gig_rival_gao_faceoff_r3');
// 跳去第 2 輪
S.rivalry.faceoffState = 'none'; S.rivalry.nextOpenDay = 100; S.rivalry.round = 1; S.rivalry.lastResult = 'won';
S.dayIndex = 100;
rivalryTick();
mergeRivalGigs();
let hasR2 = GIGS.some(g=>g.id==='gig_rival_gao_faceoff_r2');
let noR1Now = !GIGS.some(g=>g.id==='gig_rival_gao_faceoff');
S.rivalry.faceoffState = 'none';
mergeRivalGigs();
let cleared = !GIGS.some(g=>g.id && g.id.indexOf('gig_rival_gao_faceoff')===0);
ok('mergeRivalGigs：open 只注入當輪嗰張；唔開就三張都清走',
  hasR1 && hasOther && noR23 && hasR2 && noR1Now && cleared);

console.log('\n' + (fails.length ? ('FAILED: ' + fails.length + ' — ' + fails.join('；')) : 'ALL PASS'));
process.exit(fails.length ? 1 : 0);
