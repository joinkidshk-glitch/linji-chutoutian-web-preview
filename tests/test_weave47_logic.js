// Weave Phase 4-7（v20a30）邏輯測試：1990 抉擇三連
// 跟 v20a22 教訓行真路徑：段一真 openLoc（offer 呈現＋撳掣行真 choice47Play→StoryPlay 入口）；
// 段二真 StoryOC.applyChoice 落旗（＋真 newspaperStoryResolve 證明新旗唔生報紙、真 choice47Available 把關）；
// 段三真 renderDebtPane（屋企行動卡呈現＋委派 onclick 真撳）；
// 段四真 mergeExodusGigs＋真 gigsForLocSeasonBoard＋真 canAudition＋真殺青狀態機（wrapHistory）。
// 用法：node tests/test_weave47_logic.js [path-to-index.html]
const fs = require('fs');
const path = process.argv[2] || require('path').join(__dirname, '..', 'index.html');
const html = fs.readFileSync(path, 'utf8');
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
function extractConstLine(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) throw new Error('const line not found: '+name);
  return html.slice(i, html.indexOf('\n', i))+';';
}
function extractIIFE(decl){
  const i = html.indexOf(decl);
  if(i<0) throw new Error('iife not found: '+decl);
  const end = html.indexOf('\n})();', i);
  if(end<0) throw new Error('iife end not found: '+decl);
  return html.slice(i, end) + '\n})();';
}
function dayIndexOf(y, m, d){ return Math.round((Date.UTC(y, m-1, d) - Date.UTC(1988, 2, 7)) / 86400000); }

/* ================================================================
   段一：真 openLoc——何生「走定留」offer 呈現（1990 夏起）＋撳掣真入 StoryPlay
   ================================================================ */
(function(){
  function fakeEl(){
    const el = {
      children: [], _html: '', textContent: '', style: {}, disabled: false,
      classList: { _s: new Set(),
        add(...c){ c.forEach(x=>this._s.add(x)); },
        remove(...c){ c.forEach(x=>this._s.delete(x)); },
        contains(c){ return this._s.has(c); }, toggle(){} },
      setAttribute(){},
      appendChild(c){ this.children.push(c); return c; },
      querySelector(){ return null; }, querySelectorAll(){ return []; }
    };
    Object.defineProperty(el, 'innerHTML', {
      get(){ return this._html; },
      set(v){ this._html = v; if(v==='') this.children = []; }
    });
    return el;
  }
  var els = {};
  var document = {
    getElementById(id){ if(!els[id]) els[id] = fakeEl(); return els[id]; },
    createElement(){ return fakeEl(); },
    querySelector(){ return null; }, querySelectorAll(){ return []; }
  };
  var requestAnimationFrame = ()=>{};
  var window = {};
  var toast = ()=>{};
  var isStoryPlayActive = ()=> false;
  var todayIsForcedDay = ()=> false;
  var preserveMapScroll = ()=>{}, restoreMapScroll = ()=>{}, paintBar = ()=>{}, drawMap = ()=>{};
  var applyLocSheetBg = ()=>{}, addStarSighting = ()=>{}, playPushDoor = ()=>{};
  var mapWrapEl = ()=> null;
  var scrollMapPinIntoView = ()=>{};
  var closeSheet = ()=>{};
  var ensureLocSheetInteractive = ()=> ({ ok:true });
  var softPreviewOn = ()=> true;
  var isGigConsumed = ()=> false;
  var boardSortCompare = ()=> 0;
  var canAudition = ()=> ({ ok:true });
  var chance = ()=> 0.8;
  var phase3CastCopy = ()=> ({ lockedLabel:'未能報名', readyLabel:'報名試鏡', lockedTag:'未開放', readyTag:'可接', readySub:'' });
  var gigLifecycleStatus = ()=> null;
  var gigGenreLabel = (g)=> g.type || '通告';
  var gigTypeCoarse = (g)=> g.type || '通告';
  var talkHintLabel = ()=>'傾談 hint';
  var talkCostLabel = ()=>'免費';
  var bumpNpc = (id, d)=>{ S.npcs[id] = Math.max(0, Math.min(100, (S.npcs[id]||0)+d)); return d; };
  var normalizeGigRecord = (g)=> g;
  var familySafeCafeAct = (d)=> d;
  var LOCS = [
    { id:'agency_ho', name:'何生事務所', emoji:'🏢', desc:'事務所', area:'中環', type:'agency' },
    { id:'cafe_cha', name:'金龍茶餐廳', emoji:'🍵', desc:'茶餐廳', area:'', type:'cafe' }
  ];
  var NPCS = {
    agent: { id:'agent', name:'何生', role:'經理人' },
    reporter: { id:'reporter', name:'周采兒', role:'娛樂記者' }
  };
  var GIGS = [];
  var playedNodes = [];
  var StoryPlay = { start(node, opts){ playedNodes.push({ node:node, opts:opts }); return true; } };
  var S = null;
  function freshS(dayIndex){
    return { dayIndex:dayIndex, visited:{}, flags:{}, board:{}, shoots:[], npcs:{ agent:40 },
      locNpc:{ agency_ho:'agent' }, mapTips:{}, mockDebts:[], mockRumors:[], favorDueSettled:{},
      story:{ done:{}, flags:{} } };
  }
  eval(extractConst('START').replace('const START', 'globalThis.__START47a'));
  var START = globalThis.__START47a;
  eval(extractFn('dateObj'));
  eval(extractFn('calendarSeason'));
  eval(extractFn('yearSeasonNow'));
  eval(extractConst('MOCK_ASK').replace('const MOCK_ASK', 'globalThis.__MOCK_ASK47'));
  var MOCK_ASK = globalThis.__MOCK_ASK47;
  eval(extractFn('mockAskDefs'));
  eval(extractConst('FAVOR_DUE_CFG').replace('const FAVOR_DUE_CFG', 'globalThis.__FDC47'));
  var FAVOR_DUE_CFG = globalThis.__FDC47;
  eval(extractConst('FAVOR_DUE_GIGS').replace('const FAVOR_DUE_GIGS', 'globalThis.__FDG47'));
  var FAVOR_DUE_GIGS = globalThis.__FDG47;
  eval(extractFn('favorDueDebt'));
  eval(extractFn('ensureFavorDueSettled'));
  eval(extractFn('mergeFavorGigs'));
  eval(extractConstLine('CHOICE47_SEASON_IDX').replace('const CHOICE47_SEASON_IDX', 'var CHOICE47_SEASON_IDX'));
  eval(extractConst('CHOICE47_NODES').replace('const CHOICE47_NODES', 'var CHOICE47_NODES'));
  eval(extractConst('CHOICE47_DEFS').replace('const CHOICE47_DEFS', 'var CHOICE47_DEFS'));
  eval(extractFn('choice47SeasonReached'));
  eval(extractFn('choice47StoryFlag'));
  eval(extractFn('choice47StoryDone'));
  eval(extractFn('choice47Answered'));
  eval(extractFn('choice47Available'));
  eval(extractFn('choice47ActionsAt'));
  eval(extractFn('choice47Play'));
  eval(extractConst('EXODUS_GIGS').replace('const EXODUS_GIGS', 'var EXODUS_GIGS'));
  eval(extractFn('mergeExodusGigs'));
  eval(extractFn('gigsForLocSeasonBoard'));
  eval(extractFn('locResidentNpcId'));
  eval(extractFn('locPanelNpcId'));
  eval(extractFn('addLocTalkGiftActs'));
  eval(extractFn('addLocBridgeActs'));
  eval(extractFn('addLocGigActs'));
  eval(extractFn('openLoc'));

  function actsBtns(){ return els['loc-acts'] ? els['loc-acts'].children : []; }
  function actsText(){ return actsBtns().map(b=>String(b.innerHTML||'')).join('\n'); }
  const TITLE = '何生有句說話想同你講';

  // 1990 春：未到夏，唔出現
  S = freshS(dayIndexOf(1990, 4, 15)); GIGS = []; els = {}; playedNodes = [];
  openLoc('agency_ho');
  ok('seg1 spring 1990: stay/leave offer NOT shown', actsText().indexOf(TITLE) < 0);

  // 1988：更加唔出現
  S = freshS(dayIndexOf(1988, 7, 15)); GIGS = []; els = {};
  openLoc('agency_ho');
  ok('seg1 1988: stay/leave offer NOT shown', actsText().indexOf(TITLE) < 0);

  // 1990 夏：出現；撳掣 → 真 choice47Play → StoryPlay.start 收到 F4 節點（force）
  S = freshS(dayIndexOf(1990, 7, 15)); GIGS = []; els = {}; playedNodes = [];
  openLoc('agency_ho');
  ok('seg1 summer 1990: stay/leave offer shown at agency', actsText().indexOf(TITLE) >= 0);
  const btn = actsBtns().find(b=>String(b.innerHTML||'').indexOf(TITLE) >= 0);
  ok('seg1 summer 1990: offer button found', !!btn);
  if(btn && btn.onclick) btn.onclick({});
  ok('seg1 click: StoryPlay.start got F4_stay_mind node', playedNodes.length === 1 && playedNodes[0].node.id === 'F4_stay_mind');
  ok('seg1 click: played with force (micro-node path)', !!(playedNodes[0] && playedNodes[0].opts && playedNodes[0].opts.force === true));
  ok('seg1 click: node asks 走定留', !!(playedNodes[0] && JSON.stringify(playedNodes[0].node).indexOf('有冇諗過走') >= 0));

  // 答完（旗已寫，段二證明由真 applyChoice 寫入）：再入事務所唔再問
  S = freshS(dayIndexOf(1990, 8, 1)); S.story.flags.flag_leave_mind = true; GIGS = []; els = {};
  openLoc('agency_ho');
  ok('seg1 answered (flag set): offer gone', actsText().indexOf(TITLE) < 0);

  // done 把關：done 已記但旗被清（異常檔）都唔再問
  S = freshS(dayIndexOf(1990, 8, 1)); S.story.done.F4_stay_mind = true; GIGS = []; els = {};
  openLoc('agency_ho');
  ok('seg1 answered (done set): offer gone', actsText().indexOf(TITLE) < 0);

  // catch-up：1991 年頭（已過 1990 冬）未答都仲問得
  S = freshS(dayIndexOf(1991, 1, 20)); GIGS = []; els = {};
  openLoc('agency_ho');
  ok('seg1 catch-up 1991 winter: offer still shown', actsText().indexOf(TITLE) >= 0);

  // 其他地點唔出呢條 offer
  S = freshS(dayIndexOf(1990, 7, 15)); S.locNpc = {}; GIGS = []; els = {};
  openLoc('cafe_cha');
  ok('seg1 other loc: offer NOT shown at cafe', actsText().indexOf(TITLE) < 0);
})();

/* ================================================================
   段二：真 StoryOC.applyChoice 落旗——五個抉擇逐個驗
   （旗正確、done 記錄、零數值變動、唔生報紙、可用性開關）
   ================================================================ */
(function(){
  var window = {};
  var location = { search: "" };
  var localStorage = { getItem: ()=>null, setItem: ()=>{}, removeItem: ()=>{} };
  var S = null;
  var saveQ = function(){};
  var toast = function(){};
  var syncNotebookMirror = function(){};
  var STORY_WIRE = { main: null };
  var FREEPLAY_FW = { newspaperStub: null };
  var apply = function(delta){ Object.keys(delta||{}).forEach(k=>{ S[k] = (Number(S[k])||0) + delta[k]; }); return []; };
  var applyCastingTags = function(){ return []; };
  const SRC = [
    "var START = { y:1988, m:3, d:7 };",
    extractFn('dateObj'),
    extractFn('calendarSeason'),
    extractFn('weekNumNow'),
    extractFn('dualTrackNumbers'),
    extractFn('readDualTracks'),
    extractFn('syncDualTracks'),
    extractFn('yearSeasonNow'),
    extractConstLine('CHOICE47_SEASON_IDX'),
    extractConst('CHOICE47_NODES'),
    extractConst('CHOICE47_DEFS'),
    extractFn('choice47SeasonReached'),
    extractFn('choice47StoryFlag'),
    extractFn('choice47StoryDone'),
    extractFn('choice47Answered'),
    extractFn('choice47Available'),
    extractConst('STORY_FLAG_EVENT'),
    extractConst('STORY_PAPER_SKIP'),
    extractFn('newspaperStoryLists'),
    extractFn('newspaperStoryResolve'),
    extractIIFE('const BehaviorGate = (function(){'),
    extractIIFE('const StoryOC = (()=>{'),
  ].join('\n')
   .replace('const CHOICE47_SEASON_IDX =', 'var CHOICE47_SEASON_IDX =')
   .replace('const CHOICE47_NODES =', 'var CHOICE47_NODES =')
   .replace('const CHOICE47_DEFS =', 'var CHOICE47_DEFS =')
   .replace('const STORY_FLAG_EVENT =', 'var STORY_FLAG_EVENT =')
   .replace('const STORY_PAPER_SKIP =', 'var STORY_PAPER_SKIP =')
   .replace('const BehaviorGate =', 'var BehaviorGate =')
   .replace('const StoryOC =', 'var StoryOC =');
  eval(SRC);

  ok('seg2 harness: StoryOC.applyChoice loaded', typeof StoryOC === 'object' && typeof StoryOC.applyChoice === 'function');

  function baseSave(dayIndex){
    return { dayIndex: dayIndex, money: 900, fame: 10, acting: 8, popularity: 30, stress: 12, stamina: 80,
      industryCredit: 0, industryCreditDelta: 0,
      flags: {}, routes: {}, mockCredits: [], mockDebts: [], mockRumors: [], inventory: {},
      castingTags: [], favorLedger: null, newspaperQueue: [],
      story: { flags: {}, rel: {}, done: {}, choices: {} } };
  }
  function node(id){ return CHOICE47_NODES[id]; }
  function choice(id, cid){ return (CHOICE47_NODES[id].choices || []).find(x => x.id === cid); }

  const CASES = [
    ['F4_stay_mind', 'F4_a', 'flag_stay_mind', ['flag_leave_mind', 'flag_undecided_mind']],
    ['F4_stay_mind', 'F4_b', 'flag_leave_mind', ['flag_stay_mind', 'flag_undecided_mind']],
    ['F4_stay_mind', 'F4_c', 'flag_undecided_mind', ['flag_stay_mind', 'flag_leave_mind']],
    ['G4_family_job', 'G4_a', 'flag_family_job_accept', ['flag_family_job_decline']],
    ['G4_family_job', 'G4_b', 'flag_family_job_decline', ['flag_family_job_accept']],
  ];
  CASES.forEach(([nid, cid, wantFlag, notFlags]) => {
    S = baseSave(dayIndexOf(1990, 12, 15));
    StoryOC.ensure();
    const before = { money: S.money, fame: S.fame, popularity: S.popularity, stress: S.stress, stamina: S.stamina };
    const res = StoryOC.applyChoice(node(nid), choice(nid, cid));
    ok('seg2 ' + cid + ': flag written ' + wantFlag, S.story.flags[wantFlag] === true && StoryOC.getFlag(wantFlag) === true);
    ok('seg2 ' + cid + ': other answer flags untouched', notFlags.every(f => !S.story.flags[f]));
    ok('seg2 ' + cid + ': node marked done', StoryOC.isDone(nid) === true && S.story.done[nid] === true);
    ok('seg2 ' + cid + ': zero stat change (餌, 唔改數值)',
       S.money === before.money && S.fame === before.fame && S.popularity === before.popularity &&
       S.stress === before.stress && S.stamina === before.stamina);
    ok('seg2 ' + cid + ': result notes = choice notes', (res.notes || []).join(' ').indexOf(choice(nid, cid).effects.notes) >= 0);
    ok('seg2 ' + cid + ': no newspaper event resolves for new flag', newspaperStoryResolve(node(nid), choice(nid, cid)) === null);
  });

  // 可用性開關（真 StoryOC 旗倉＋真日曆）
  S = baseSave(dayIndexOf(1990, 4, 15)); StoryOC.ensure();
  ok('seg2 gate: F4 closed in 1990 spring', choice47Available('F4_stay_mind') === false);
  ok('seg2 gate: G4 closed in 1990 spring', choice47Available('G4_family_job') === false);
  S = baseSave(dayIndexOf(1990, 7, 15)); StoryOC.ensure();
  ok('seg2 gate: F4 open in 1990 summer', choice47Available('F4_stay_mind') === true);
  ok('seg2 gate: G4 still closed in 1990 summer', choice47Available('G4_family_job') === false);
  S = baseSave(dayIndexOf(1990, 10, 15)); StoryOC.ensure();
  ok('seg2 gate: G4 still closed in 1990 autumn', choice47Available('G4_family_job') === false);
  S = baseSave(dayIndexOf(1990, 12, 15)); StoryOC.ensure();
  ok('seg2 gate: both open in 1990 winter', choice47Available('F4_stay_mind') === true && choice47Available('G4_family_job') === true);
  // 答完即關（經真 applyChoice）
  StoryOC.applyChoice(node('F4_stay_mind'), choice('F4_stay_mind', 'F4_a'));
  ok('seg2 gate: F4 closed after answering, G4 still open',
     choice47Available('F4_stay_mind') === false && choice47Available('G4_family_job') === true);
  // catch-up：1991 年存檔兩個都仲開到（未答的話）
  S = baseSave(dayIndexOf(1991, 2, 10)); StoryOC.ensure();
  ok('seg2 catch-up: both open in 1991 save', choice47Available('F4_stay_mind') === true && choice47Available('G4_family_job') === true);
  // 1989 全年唔開
  S = baseSave(dayIndexOf(1989, 12, 15)); StoryOC.ensure();
  ok('seg2 gate: both closed in 1989', choice47Available('F4_stay_mind') === false && choice47Available('G4_family_job') === false);
})();

/* ================================================================
   段三：真 renderDebtPane——屋企「穩陣工」行動卡（1990 冬起）＋委派 onclick 真撳
   ================================================================ */
(function(){
  var box = { innerHTML:'', onclick:null, contains:()=>true };
  var document = { getElementById: (id)=> id==='debt-list' ? box : null };
  var ensureMockJournal = ()=>{};
  var ensureWeakSeals = ()=>{};
  var softPreviewOn = ()=> true;
  var syncNotebookMirror = ()=>{};
  var saveQ = ()=>{};
  var pushNewspaperRumor = ()=>{};
  var toast = ()=>{};
  var playedNodes = [];
  var StoryPlay = { start(node, opts){ playedNodes.push({ node:node, opts:opts }); return true; } };
  var S = null;
  eval(extractConst('START').replace('const START', 'globalThis.__START47c'));
  var START = globalThis.__START47c;
  eval(extractConst('FAVOR_DUE_CFG').replace('const FAVOR_DUE_CFG', 'globalThis.__FDC47c'));
  var FAVOR_DUE_CFG = globalThis.__FDC47c;
  eval(extractConst('MOCK_DEBT_TUTORIAL').replace('const MOCK_DEBT_TUTORIAL', 'globalThis.__MDT47c'));
  var MOCK_DEBT_TUTORIAL = globalThis.__MDT47c;
  eval(extractConst('SEASON_COLLECT').replace('const SEASON_COLLECT', 'globalThis.__SC47c'));
  var SEASON_COLLECT = globalThis.__SC47c;
  eval(extractConst('DEBT_FUZZY').replace('const DEBT_FUZZY', 'globalThis.__DF47c'));
  var DEBT_FUZZY = globalThis.__DF47c;
  eval(extractConst('MOCK_EMPTY').replace('const MOCK_EMPTY', 'globalThis.__ME47c'));
  var MOCK_EMPTY = globalThis.__ME47c;
  const TIER_SRC = [
    extractConst('PAPER_NAME_TIER_NAMED'), extractConst('PAPER_NAME_TIER_TITLED'),
    extractFn('newspaperNameTier')
  ].join('\n')
   .replace(/const PAPER_NAME_TIER_NAMED/g, 'var PAPER_NAME_NAMED')
   .replace(/const PAPER_NAME_TIER_TITLED/g, 'var PAPER_NAME_TITLED')
   .replace(/PAPER_NAME_TIER_NAMED/g, 'PAPER_NAME_NAMED').replace(/PAPER_NAME_TIER_TITLED/g, 'PAPER_NAME_TITLED');
  const FAM_SRC = [
    extractConst('FAMILY_HOME_DEBT_ID'), extractConst('FAMILY_HOME_CYCLES'),
    extractConst('FAMILY_HOME_SEED_FLAVOR'), extractConst('FAMILY_HOME_PAID_FLAVOR'),
    extractFn('ensureFamilyHomeState'), extractFn('familyMonthKey'), extractFn('isFamilyHomeDebt'),
    extractFn('ensureFamilyHomeDebt'), extractFn('noteFamilyHomePaid'),
    extractFn('familyHomeSettleLines'), extractFn('familyAttitudeLine'),
    extractConst('FAMILY_ECHO_TOAST_MAIN'), extractConst('FAMILY_ECHO_TOAST_SUB'), extractConst('FAMILY_ECHO_NOTE'),
    extractFn('familyPaperEchoTick'), extractFn('familyEchoNoteText')
  ].join('\n')
   .replace(/const FAMILY_HOME_DEBT_ID/g, 'var FAMILY_HOME_DEBT_ID')
   .replace(/const FAMILY_HOME_CYCLES/g, 'var FAMILY_HOME_CYCLES')
   .replace(/const FAMILY_HOME_SEED_FLAVOR/g, 'var FAMILY_HOME_SEED_FLAVOR')
   .replace(/const FAMILY_HOME_PAID_FLAVOR/g, 'var FAMILY_HOME_PAID_FLAVOR')
   .replace(/const FAMILY_ECHO_TOAST_MAIN/g, 'var FAMILY_ECHO_TOAST_MAIN')
   .replace(/const FAMILY_ECHO_TOAST_SUB/g, 'var FAMILY_ECHO_TOAST_SUB')
   .replace(/const FAMILY_ECHO_NOTE/g, 'var FAMILY_ECHO_NOTE');
  eval(TIER_SRC);
  eval(FAM_SRC);
  eval(extractFn('dateObj'));
  eval(extractFn('calendarSeason'));
  eval(extractFn('yearSeasonNow'));
  eval(extractFn('journalText'));
  eval(extractFn('debtStatusLabel'));
  eval(extractFn('debtCreditorName'));
  eval(extractFn('ensureSeasonDebtClearedBag'));
  eval(extractFn('favorPressure'));
  eval(extractFn('favorDueDebt'));
  eval(extractFn('ensureFavorDueSettled'));
  eval(extractFn('ensureFavorDue'));
  eval(extractFn('favorDueHintText'));
  eval(extractConstLine('CHOICE47_SEASON_IDX').replace('const CHOICE47_SEASON_IDX', 'var CHOICE47_SEASON_IDX'));
  eval(extractConst('CHOICE47_NODES').replace('const CHOICE47_NODES', 'var CHOICE47_NODES'));
  eval(extractConst('CHOICE47_DEFS').replace('const CHOICE47_DEFS', 'var CHOICE47_DEFS'));
  eval(extractFn('choice47SeasonReached'));
  eval(extractFn('choice47StoryFlag'));
  eval(extractFn('choice47StoryDone'));
  eval(extractFn('choice47Answered'));
  eval(extractFn('choice47Available'));
  eval(extractFn('choice47Play'));
  eval(extractFn('choice47FamilyCardHtml'));
  eval(extractFn('renderDebtPane'));

  S = { dayIndex: dayIndexOf(1990, 10, 15), fame: 5, npcs:{},
    favorDueSettled:{ debt_ho_tutorial:{ result:'repaid_help', day:1 } },
    mockSeasonCleared:{}, mockDebts:[], mockCredits:[], mockRumors:[], newspaperClippings:[],
    story:{ done:{}, flags:{} } };
  ensureFamilyHomeDebt(); // 真播種屋企債

  // 1990 秋：未到冬，行動卡唔出
  renderDebtPane();
  ok('seg3 autumn 1990: family job card NOT shown', box.innerHTML.indexOf('data-choice47') < 0);
  ok('seg3 autumn 1990: family debt card present (context)', box.innerHTML.indexOf('data-debt-id="debt_family_home"') >= 0);

  // 1990 冬：行動卡出現，排喺屋企卡之後
  S.dayIndex = dayIndexOf(1990, 12, 15);
  renderDebtPane();
  const h = box.innerHTML;
  ok('seg3 winter 1990: family job card shown', h.indexOf('data-choice47="G4_family_job"') >= 0);
  ok('seg3 winter 1990: card copy has 穩陣工／表叔／文職', h.indexOf('表叔') >= 0 && h.indexOf('文職') >= 0);
  ok('seg3 winter 1990: card sits AFTER family debt card',
     h.indexOf('data-debt-id="debt_family_home"') >= 0 && h.indexOf('data-choice47-card') > h.indexOf('data-debt-id="debt_family_home"'));

  // 真撳掣（委派 onclick）：行真 choice47Play → StoryPlay 收到 G4 節點
  playedNodes = [];
  const fakeBtn = { getAttribute:(k)=> k==='data-choice47' ? 'G4_family_job' : null, closest:()=>null };
  box.onclick({ target:{ closest:(sel)=> sel==='[data-choice47]' ? fakeBtn : null },
    preventDefault(){}, stopPropagation(){} });
  ok('seg3 click: StoryPlay.start got G4_family_job node', playedNodes.length === 1 && playedNodes[0].node.id === 'G4_family_job');
  ok('seg3 click: node is the 屋企飯枱 scene', !!(playedNodes[0] && JSON.stringify(playedNodes[0].node).indexOf('阿媽') >= 0));

  // 答完（旗已寫）：卡消失
  S.story.flags.flag_family_job_decline = true;
  renderDebtPane();
  ok('seg3 answered: family job card gone', box.innerHTML.indexOf('data-choice47') < 0);

  // catch-up：1991 存檔未答，卡仍在
  S.story.flags = {}; S.story.done = {};
  S.dayIndex = dayIndexOf(1991, 1, 20);
  renderDebtPane();
  ok('seg3 catch-up 1991: family job card still shown', box.innerHTML.indexOf('data-choice47="G4_family_job"') >= 0);
})();

/* ================================================================
   段四：真 mergeExodusGigs＋真 board——移民潮空位通告（1990 秋起）
   ＋真 canAudition 接單閘＋真殺青狀態機（booked→wrapHistory→落板）
   ================================================================ */
(function(){
  var window = {};
  var saveQ = ()=>{};
  var toast = ()=>{};
  var COURSE_DEFS = {};
  var GIGS = [];
  var S = null;
  eval(extractConst('START').replace('const START', 'globalThis.__START47d'));
  var START = globalThis.__START47d;
  eval(extractFn('dateObj'));
  eval(extractFn('calendarSeason'));
  eval(extractFn('yearSeasonNow'));
  eval(extractConstLine('CHOICE47_SEASON_IDX').replace('const CHOICE47_SEASON_IDX', 'var CHOICE47_SEASON_IDX'));
  eval(extractFn('choice47SeasonReached'));
  eval(extractFn('boardNotePlayerOk'));
  eval(extractFn('looksLikeEraId'));
  eval(extractFn('humanizeEraId'));
  eval(extractFn('normalizeGigRecord'));
  eval(extractFn('boardPriorityRank'));
  eval(extractFn('boardSortCompare'));
  eval(extractFn('seasonRank'));
  eval(extractFn('gigActiveShoot'));
  eval(extractFn('isGigWrapped'));
  eval(extractFn('isGigInProduction'));
  eval(extractFn('isGigConsumed'));
  eval(extractFn('gigLifecycleStatus'));
  eval(extractFn('fameFloor'));
  eval(extractFn('reqGap'));
  eval(extractFn('gateTrainHint'));
  eval(extractFn('softCastingTagGate'));
  eval(extractFn('softIndustryCreditGate'));
  eval(extractFn('debtStatusLabel'));
  eval(extractFn('softOverdueFavorDebtLock'));
  eval(extractFn('canAudition'));
  eval(extractConst('EXODUS_GIGS').replace('const EXODUS_GIGS', 'var EXODUS_GIGS'));
  eval(extractFn('mergeExodusGigs'));
  eval(extractFn('gigsForLocSeasonBoard'));

  function freshS(dayIndex, fame){
    return { dayIndex: dayIndex, fame: fame == null ? 20 : fame, money: 900, popularity: 30, stress: 10, stamina: 80,
      flags: {}, npcs: {}, shoots: [], booked: [], wrapHistory: [], mockDebts: [], story: { done:{}, flags:{} } };
  }
  function boardIds(loc){ return gigsForLocSeasonBoard(loc).map(g => g.id); }

  // 1989 全年：唔注入
  S = freshS(dayIndexOf(1989, 12, 15)); GIGS = [];
  ok('seg4 1989: merge returns 0', mergeExodusGigs() === 0);
  ok('seg4 1989: boards have no exodus gigs',
     boardIds('tvb_longmen').indexOf('gig_exodus_tv_senior') < 0 && boardIds('film_harbour').indexOf('gig_exodus_film_hand') < 0);

  // 1990 春／夏：唔注入
  S = freshS(dayIndexOf(1990, 4, 15)); GIGS = [];
  ok('seg4 1990 spring: not injected', mergeExodusGigs() === 0 && GIGS.length === 0);
  S = freshS(dayIndexOf(1990, 7, 15)); GIGS = [];
  ok('seg4 1990 summer: not injected', mergeExodusGigs() === 0 && GIGS.length === 0);

  // 1990 秋：注入兩份，各自上返所屬地點板
  S = freshS(dayIndexOf(1990, 10, 15)); GIGS = [];
  const n = mergeExodusGigs();
  ok('seg4 1990 autumn: merge injects 2', n === 2 && GIGS.length === 2);
  ok('seg4 1990 autumn: tv gig on tvb_longmen board', boardIds('tvb_longmen').indexOf('gig_exodus_tv_senior') >= 0);
  ok('seg4 1990 autumn: film gig on film_harbour board', boardIds('film_harbour').indexOf('gig_exodus_film_hand') >= 0);
  ok('seg4 1990 autumn: gigs not cross-posted',
     boardIds('tvb_longmen').indexOf('gig_exodus_film_hand') < 0 && boardIds('film_harbour').indexOf('gig_exodus_tv_senior') < 0);
  ok('seg4 merge idempotent: second merge keeps 2', mergeExodusGigs() >= 0 && GIGS.filter(g => /^gig_exodus_/.test(g.id)).length === 2);

  // 數值校準：中級、定額喺 pay 範圍內、同隱藏通告 $3,100 同量級
  const tv = GIGS.find(g => g.id === 'gig_exodus_tv_senior');
  const film = GIGS.find(g => g.id === 'gig_exodus_film_hand');
  ok('seg4 calibration: both tier 中', tv.tier === '中' && film.tier === '中');
  ok('seg4 calibration: payExact within pay range',
     tv.payExact >= tv.pay[0] && tv.payExact <= tv.pay[1] && film.payExact >= film.pay[0] && film.payExact <= film.pay[1]);
  ok('seg4 calibration: payExact near intel gig $3,100 magnitude',
     tv.payExact >= 2800 && tv.payExact <= 3600 && film.payExact >= 2400 && film.payExact <= 3300);
  ok('seg4 calibration: boardNote marks 移民空位 (player-facing)',
     String(tv.eraTagLabel || '').indexOf('移民空位') >= 0 || String(tv.boardNote || '').indexOf('移民空位') >= 0);

  // 接單閘（真 canAudition）：聲望夠 → 可報；唔夠 → 中級 fameFloor 16 硬鎖
  ok('seg4 audition: fame 20 can audition tv gig', canAudition(tv).ok === true);
  S.fame = 5;
  ok('seg4 audition: fame 5 blocked by tier floor', canAudition(tv).ok === false);
  S.fame = 20;

  // 殺青狀態機（真函數）：open → booked → wrapped（落板）
  ok('seg4 lifecycle: starts open', gigLifecycleStatus(tv).key === 'open');
  S.booked = [{ gigId: 'gig_exodus_tv_senior' }];
  ok('seg4 lifecycle: booked after 接單', gigLifecycleStatus(tv).key === 'booked');
  S.booked = [];
  // 真殺青結算寫入嘅兩樣權威紀錄：S.flags["done_"+id]（isGigWrapped 讀佢）＋ wrapHistory 一筆
  S.flags['done_gig_exodus_tv_senior'] = 1;
  S.wrapHistory = [{ gigId: 'gig_exodus_tv_senior', title: tv.title }];
  ok('seg4 lifecycle: consumed after wrap', isGigConsumed(tv) === true && gigLifecycleStatus(tv).key === 'wrapped');
  ok('seg4 lifecycle: wrapped gig leaves the board', boardIds('tvb_longmen').indexOf('gig_exodus_tv_senior') < 0);
  ok('seg4 lifecycle: other exodus gig still on its board', boardIds('film_harbour').indexOf('gig_exodus_film_hand') >= 0);

  // 1990 冬（過秋）仍然注入（過季唔鎖死）
  S = freshS(dayIndexOf(1990, 12, 15)); GIGS = [];
  ok('seg4 1990 winter: still injected', mergeExodusGigs() === 2);
})();

console.log(fails.length ? ('\nFAILED: ' + fails.length + ' -> ' + fails.join(' | ')) : '\nALL PASS (weave47)');
process.exit(fails.length ? 1 : 0);
