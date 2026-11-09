// 引導包（v20a34）邏輯／路徑測試：P0-1 差額卡／P0-3 死路修正／P0-4 過一日掣／
// P0-5 系統出場交代／P1-1(a) 壓力後果／P1-1(b) 雙軌解釋。
// 跟 v20a22 教訓行真路徑：真 gigBoardTeaserHtml＋真 canAudition 鏈、真 BehaviorGate
// progressToward／softLockPlayerLine（真 stub 注入）、真 paintBar→真 confirmEarlyRestFromMenu
// →真 endBrowseDayGoHome（tickDay 係全遊戲共用結算引擎、本包唔郁佢，只以計數 stub
// 驗「行咗一次、日＋1」呢個接駁契約）、真 renderDebtPane／renderRumorPane、
// 真 chance() 驗壓力折減比率、真 showStressPreviewModal。
// 用法：node tests/test_guidance34_logic.js [path-to-index.html]
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
   段一 (a)：P0-1——真 gigBoardTeaserHtml＋真 canAudition＋真差額計法
   未達卡含正確差額字串；齊條件卡冇差額行；同詳情頁 gigLockReasonLine 同源。
   ================================================================ */
(function(){
  var S = { fame:3, acting:8, iq:10, stage:0, stamina:80, stress:0, money:1000,
    flags:{}, shoots:[], booked:[], npcs:{ director:0, agent:0, colleague:0 },
    enrolled:{}, mockDebts:[] };
  var phase3SoftOn = ()=> false;
  var gigPayExactText = ()=> "$900";
  var gigScheduleVerb = ()=> "拍攝";
  var effectiveShootDays = ()=> 3;
  var seasonTipHtml = ()=> "";
  var stripEraIdsInText = (s)=> String(s||"");
  var eraTagDisplay = ()=> "";
  var looksLikeEraId = ()=> false;
  eval(extractConstLine('STAT_LABEL').replace('const STAT_LABEL', 'var STAT_LABEL'));
  eval(extractConst('COURSE_DEFS').replace('const COURSE_DEFS', 'var COURSE_DEFS'));
  const FNS_A = ['clamp','fameFloor','reqGap','isGigWrapped','gigActiveShoot','isGigInProduction',
   'isGigConsumed','gateTrainHint','canAudition','chance','gigTierKey','gigWorkTitle',
   'gigTypeCoarse','gigLifecycleStatus','gigRecruitStatus','gigBoardCardState',
   'phase3CastCopy','reqHtml','gigLockReasonLine',
   'gigGapBits34','gigGapTotal34','gigGapLine34','gigBoardTeaserHtml','gigCardHtml'];
  for(let i=0;i<FNS_A.length;i++) eval(extractFn(FNS_A[i]));

  const gigLocked = { id:'g34_locked', title:'《試鏡甲》主角', workTitle:'試鏡甲',
    type:'電視劇', tier:'中', loc:'tvb_longmen', req:{ acting:20, iq:15 }, pay:[900,1200] };
  const gigReady = { id:'g34_ready', title:'《街景臨記》路人', workTitle:'街景臨記',
    type:'電視劇', tier:'初', loc:'tvb_longmen', req:{ acting:5 }, pay:[550,650] };

  ok('a0 canAudition real: locked gig fails', canAudition(gigLocked).ok === false);
  ok('a0 canAudition real: ready gig passes', canAudition(gigReady).ok === true);
  /* 差額：聲望 floor（中=16，現 3）差 13；演技 20-8=12；智商 15-10=5 */
  ok('a1 gap line exact', gigGapLine34(gigLocked) === '欠：聲望 13／演技 12／智商 5');
  ok('a2 gap total', gigGapTotal34(gigLocked) === 30);
  ok('a3 gap line empty when ready', gigGapLine34(gigReady) === '');
  /* 同詳情頁同一套現值/需要值：gigLockReasonLine 真函數列嘅數要同差額對得返 */
  const lr = gigLockReasonLine(gigLocked);
  ok('a4 detail lock reason same source numbers',
     lr.indexOf('聲望現 3／需要 16') >= 0 && lr.indexOf('演技現 8／需要 20') >= 0 && lr.indexOf('智商現 10／需要 15') >= 0);

  const tLock = gigBoardTeaserHtml(gigLocked);
  ok('a5 teaser locked shows gap line', tLock.indexOf('<div class="gt-gap">欠：聲望 13／演技 12／智商 5</div>') >= 0);
  ok('a6 teaser locked no closest by default', tLock.indexOf('最接近') < 0);
  const tClose = gigBoardTeaserHtml(gigLocked, { closest:true });
  ok('a7 teaser closest marker when flagged', tClose.indexOf('最接近') >= 0);
  const tReady = gigBoardTeaserHtml(gigReady);
  ok('a8 teaser ready has NO gap row', tReady.indexOf('gt-gap') < 0 && tReady.indexOf('欠：') < 0);
  ok('a9 teaser ready badge intact', tReady.indexOf('可接通告') >= 0);

  const cLock = gigCardHtml(gigLocked, {});
  ok('a10 gigCardHtml locked shows gap', cLock.indexOf('欠：聲望 13／演技 12／智商 5') >= 0);
  const cReady = gigCardHtml(gigReady, {});
  ok('a11 gigCardHtml ready has no gap text', cReady.indexOf('欠：') < 0 && cReady.indexOf('可接通告') >= 0);
})();

/* ================================================================
   段二 (b)：P0-3——真 BehaviorGate（真 LOCS／真 MOCK_ASK）＋真 stub 注入 C2 閘
   底欄 remain：傳聞步要講明去茶餐廳／事務所打聽（唔指向電視台）；地點步係「播」。
   鎖定說明：連行動名（打聽電視城規矩／請教何生入廠守則）。
   ================================================================ */
(function(){
  var window = {};
  var location = { search: "" };
  var localStorage = { getItem: ()=>null, setItem: ()=>{}, removeItem: ()=>{} };
  var S = null;
  var atLoc = null;
  var saveQ = function(){};
  var STORY_WIRE = { main:{ nodes: [] }, romance:{ veraHiuChoi:{ nodes: [] }, lanXu:{ nodes: [] }, tang:{ nodes: [] } }, rival:{ nodes: [] } };
  const SRC = [
    extractConst('START'),
    extractConst('LOCS'),
    extractConst('MOCK_ASK'),
    extractFn('dateObj'),
    extractFn('calendarSeason'),
    extractFn('weekNumNow'),
    extractFn('dualTrackNumbers'),
    extractFn('readDualTracks'),
    extractFn('syncDualTracks'),
    extractFn('yearSeasonNow'),
    extractIIFE('const BehaviorGate = (function(){'),
  ].join('\n')
   .replace('const START =', 'var START =')
   .replace('const LOCS =', 'var LOCS =')
   .replace('const MOCK_ASK =', 'var MOCK_ASK =')
   .replace('const BehaviorGate =', 'var BehaviorGate =');
  eval(SRC);
  ok('b0 harness: BehaviorGate loaded', typeof BehaviorGate === 'object' && typeof BehaviorGate.progressToward === 'function');

  const load = BehaviorGate.loadStub_nodes_trigger({
    stubRev: 'v1.3.0-full-literal-or', liveWeekGateStillActive: true, tipForbidden: true,
    engineSlice: { flags: { liveWeekGateStillActive: true, tipForbidden: true, rivalGaoMixC5: false, change89to92: false },
      iosSoftHooks: [1,2,3,4,5,6,7] },
    nodes: [ { beatId:'C2', id:'C2', title:'留人脈／趕通告',
      trigger: { needDone:['C1'], weekMin:4, gigCountMin:3,
        rumorAny:['tvb_rules_gossip'], locIdAny:['tvb_longmen','cafe_cha'] } } ]
  });
  ok('b1 stub ingested', !!load.ok);

  S = { dayIndex: 8, fame: 0, stage: 0, acting: 0, stress: 0, industryCreditDelta: 0,
    castingTags: [], mockDebts: [], mockRumors: [], wrapHistory: [], flags: {}, npcs: {},
    story: { done:{}, flags:{}, rel:{}, routes:{}, phase:'P1' } };

  const pt = BehaviorGate.progressToward({ beatId:'C2' });
  ok('b2 progressToward returns remain', !!pt && Array.isArray(pt.remain));
  const rumorItem = (pt.remain||[]).find(x=>x.indexOf('未聽聞')===0) || '';
  const locItem = (pt.remain||[]).find(x=>x.indexOf('到')===0) || '';
  ok('b3 bottom bar rumor step names hear locations (cafe+agency, short form)',
     rumorItem === '未聽聞「電視城廠景生存守則」（去金龍茶餐廳或何生事務所打聽）');
  ok('b4 rumor step does NOT point at TV station', rumorItem.indexOf('星河電視台') < 0);
  ok('b5 bottom bar loc step marked as play location', locItem === '到星河電視台或金龍茶餐廳播');

  const lock = BehaviorGate.lockedCopy_noEngineeringTerms({ beatId:'C2' });
  ok('b6 lock line names exact ask actions',
     lock.indexOf('未聽聞「電視城廠景生存守則」（去金龍茶餐廳「打聽電視城規矩」或去何生事務所「請教何生入廠守則」）') >= 0);
})();

/* ================================================================
   段三 (c)：P0-4——真 paintBar 逛逛日出「過一日」掣；真撳→真 confirmEarlyRestFromMenu
   →真 endBrowseDayGoHome（tickDay 以計數 stub 驗接駁：行一次、日＋1、plan 寫 rest）。
   有安排活動嘅日子（street）唔出呢個掣、出返「開始今日行程」。
   ================================================================ */
(function(){
  function fakeEl(){
    const el = { children: [], _html: '', textContent: '', style: {}, disabled: false, onclick: null,
      classList: { _s: new Set(),
        add(...c){ c.forEach(x=>this._s.add(x)); },
        remove(...c){ c.forEach(x=>this._s.delete(x)); },
        contains(c){ return this._s.has(c); }, toggle(){} },
      setAttribute(){}, getAttribute(){ return null; },
      appendChild(c){ this.children.push(c); return c; },
      querySelector(){ return null; }, querySelectorAll(){ return []; } };
    Object.defineProperty(el, 'innerHTML', {
      get(){ return this._html; }, set(v){ this._html = v; if(v==='') this.children = []; } });
    return el;
  }
  var els = {};
  var document = { getElementById(id){ if(!els[id]) els[id] = fakeEl(); return els[id]; },
    createElement(){ return fakeEl(); }, querySelector(){ return null; }, querySelectorAll(){ return []; } };
  var window = {};
  var atLoc = null;
  var saveQ = ()=>{};
  var toast = ()=>{};
  var closeSheet = ()=>{}, closeModal = ()=>{};
  var planLabel = (id)=> ({ scout_all:'到處逛逛', street:'街頭表演', rest:'休息' })[id] || String(id||'');
  var fmtDate = ()=> '1988年3月7日（一）· 第1週';
  var fmtDateShort = ()=> '1988/3/7';
  var R = (a,b)=> a;
  var modalCalls = [];
  var modal = (body, btns)=>{ modalCalls.push({ body, btns }); };
  var restPresented = 0;
  var presentRestSleepDayEnd = ()=>{ restPresented++; };
  var afterDayModal = ()=>{};
  var formatRestSleepDeltas = ()=> '';
  var tickCalls = 0;
  var tickDay = ()=>{ tickCalls++; S.dayIndex++; return { ended:false, summary:null }; };
  var S = { dayIndex: 0, stamina: 50, stress: 10, fame: 0, popularity: 0, money: 12000,
    weekPlan: ['scout_all','rest','scout_all','scout_all','street','cafe_gig','rest'],
    flags: {}, npcs: {}, homeEditable: false, enrolled: {}, trainCount: {} };
  eval(extractConst('START').replace('const START', 'var START'));
  eval(extractConstLine('STAT_LABEL').replace('const STAT_LABEL', 'var STAT_LABEL'));
  eval(extractConstLine('STAT_MAX').replace('const STAT_MAX', 'var STAT_MAX'));
  eval(extractConstLine('STRESS_MAX').replace('const STRESS_MAX', 'var STRESS_MAX'));
  const FNS_C = ['clamp','statHardMax','dateObj','calendarSeason','weekdayIdx','weekdayName',
   'todayPlanId','isMapDay','todayIsForcedDay','todayHasSoftSchedule','paintBar',
   'writeTodayPlan','apply','kickScheduleIfNeeded','confirmEarlyRestFromMenu','endBrowseDayGoHome'];
  for(let i=0;i<FNS_C.length;i++) eval(extractFn(FNS_C[i]));

  /* 逛逛日（週一 scout_all） */
  paintBar();
  const hintHtml = els['map-hint'].innerHTML;
  ok('c1 scout day: end-day button rendered in map hint', hintHtml.indexOf('id="map-end-day"') >= 0 && hintHtml.indexOf('逛完・過一日') >= 0);
  ok('c2 scout day: no start-today button', hintHtml.indexOf('id="map-start-today"') < 0);
  const edBtn = els['map-end-day'];
  ok('c3 scout day: button wired by paintBar', typeof edBtn.onclick === 'function');
  const dayBefore = S.dayIndex;
  edBtn.onclick({ preventDefault(){}, stopPropagation(){} });
  ok('c4 click opens the REAL early-rest confirm modal',
     modalCalls.length === 1 && modalCalls[0].body.indexOf('確認提早休息') >= 0);
  const confirmBtn = (modalCalls[0].btns||[]).find(b=>b.label.indexOf('確定休息') >= 0);
  ok('c5 confirm button present', !!confirmBtn);
  confirmBtn.on();
  ok('c6 day advanced exactly once via endBrowseDayGoHome→tickDay', tickCalls === 1 && S.dayIndex === dayBefore + 1);
  ok('c7 today plan written as rest (existing semantics)', S.weekPlan[weekdayIdx(dayBefore)] === 'rest');
  ok('c8 rest day-end presented once, no double settle', restPresented === 1);

  /* 有安排活動嘅日子（週五 street，dayIndex 4） */
  modalCalls = []; tickCalls = 0; restPresented = 0;
  S.dayIndex = 4; S.weekPlan = ['scout_all','rest','scout_all','scout_all','street','cafe_gig','rest'];
  paintBar();
  const hint2 = els['map-hint'].innerHTML;
  ok('c9 scheduled day: NO end-day button', hint2.indexOf('id="map-end-day"') < 0);
  ok('c10 scheduled day: start-today button instead', hint2.indexOf('id="map-start-today"') >= 0);
  ok('c11 scheduled day: nothing settled', tickCalls === 0 && restPresented === 0);
})();

/* ================================================================
   段四 (d)：P0-5——真 renderDebtPane（開局四筆債各有來歷行＋頁面總說明）
   ＋真 renderRumorPane（來源標示跟真 source／預設＋頁面總說明）
   ================================================================ */
(function(){
  var box = { innerHTML:'', onclick:null, contains:()=>true, querySelectorAll:()=>[] };
  var document = { getElementById: (id)=> id==='debt-list' ? box : (id==='rumor-list' ? box : null) };
  var ensureMockJournal = ()=>{};
  var ensureWeakSeals = ()=>{};
  var softPreviewOn = ()=> true;
  var syncNotebookMirror = ()=>{};
  var saveQ = ()=>{};
  var toast = ()=>{};
  var S = null;
  eval(extractConst('START').replace('const START', 'globalThis.__START34d'));
  var START = globalThis.__START34d;
  eval(extractConst('FAVOR_DUE_CFG').replace('const FAVOR_DUE_CFG', 'globalThis.__FDC34d'));
  var FAVOR_DUE_CFG = globalThis.__FDC34d;
  eval(extractConst('MOCK_DEBT_TUTORIAL').replace('const MOCK_DEBT_TUTORIAL', 'globalThis.__MDT34d'));
  var MOCK_DEBT_TUTORIAL = globalThis.__MDT34d;
  eval(extractConst('SEASON_COLLECT').replace('const SEASON_COLLECT', 'globalThis.__SC34d'));
  var SEASON_COLLECT = globalThis.__SC34d;
  eval(extractConst('DEBT_FUZZY').replace('const DEBT_FUZZY', 'globalThis.__DF34d'));
  var DEBT_FUZZY = globalThis.__DF34d;
  eval(extractConst('MOCK_EMPTY').replace('const MOCK_EMPTY', 'globalThis.__ME34d'));
  var MOCK_EMPTY = globalThis.__ME34d;
  eval(extractConst('DEBT_ORIGIN_LINES34').replace('const DEBT_ORIGIN_LINES34', 'globalThis.__DOL34d'));
  var DEBT_ORIGIN_LINES34 = globalThis.__DOL34d;
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
  eval(extractFn('choice47FamilyCardHtml'));
  eval(extractFn('renderDebtPane'));

  eval(extractFn('isHoCreditorDebt'));
  eval(extractFn('rumorTutorialDone'));
  eval(extractFn('markRumorTutorialDone'));
  /* 開局第 3 日（1988-03-09，春）：跟真玩家路徑——ensureMockJournal 尾播屋企債
     （呢度直接行真 ensureFamilyHomeDebt）、拼合教學完成 markRumorTutorialDone 入教學債 */
  S = { dayIndex: 2, fame: 0, npcs:{}, favorDueSettled:{}, mockSeasonCleared:{},
    mockDebts:[], mockCredits:[], mockRumors:[], newspaperClippings:[],
    story:{ done:{}, flags:{} }, flags:{} };
  ensureFamilyHomeDebt();
  markRumorTutorialDone('done');
  renderDebtPane();
  const h = box.innerHTML;
  ok('d1 debt pane intro line present', h.indexOf('呢頁記住邊個欠你、你欠邊個') >= 0);
  ok('d2 family debt card present', h.indexOf('data-debt-id="debt_family_home"') >= 0);
  ok('d3 tutorial debt seeded by real tutorial-done path', h.indexOf('data-debt-id="debt_ho_tutorial"') >= 0);
  ok('d4 origin: family home', h.indexOf('來歷：你出嚟做臨記嗰陣應承屋企嘅') >= 0);
  ok('d5 origin: Ho spring season card', h.indexOf('來歷：入行嗰陣何生幫你打點墊支嗰筆') >= 0);
  ok('d6 origin: props Zhang spring season card', h.indexOf('來歷：早前你借過道具組嘅器材嚟用') >= 0);
  ok('d7 origin: tutorial debt', h.indexOf('來歷：何生手把手教你入行規矩嗰份人情') >= 0);
  ok('d8 exactly four origin lines on opening pane', (h.split('來歷：').length - 1) === 4);

  /* ---- 傳聞頁 ---- */
  var applyPhase2Steps56TabLabel = ()=>{};
  var phase2Steps56CoachHtml = ()=> '';
  var phase2Steps56Copy = ()=> null;
  var heardPickIds = ()=> [];
  var tutorialPhase2FxOn = ()=> false;
  var displayRumor = (r)=> r; /* 家庭友善過濾係 PR#109 範疇（test_p03_filter 覆蓋）；呢度只驗來源顯示 */
  eval(extractConst('RUMOR_STATE_ZH').replace('const RUMOR_STATE_ZH', 'globalThis.__RSZ34d'));
  var RUMOR_STATE_ZH = globalThis.__RSZ34d;
  eval(extractConstLine('WEAK_WHISPER').replace('const WEAK_WHISPER', 'var WEAK_WHISPER'));
  eval(extractFn('rumorStateLabel'));
  eval(extractFn('renderRumorPane'));
  S.mockRumors = [
    { id:'tvb_rules_gossip', source:'金龍茶餐廳', title:'電視城廠景生存守則', text:'聽聞入廠拍劇最忌遲到。', state:'normal', season:'' },
    { id:'paperfrag_lu_concert', paperFrag:true, title:'陸柏言開演唱會', text:'報紙花邊寫道：陸柏言開演唱會。', state:'normal', season:'' },
    { id:'rumor_sourceless', title:'唔知邊度聽返嚟', text:'一則冇來源欄嘅舊碎片。', state:'normal', season:'' }
  ];
  renderRumorPane();
  const rh = box.innerHTML;
  ok('d9 rumor pane intro line present', rh.indexOf('呢頁係你聽返嚟嘅傳聞碎片') >= 0);
  ok('d10 rumor card shows real source', rh.indexOf('來源：金龍茶餐廳') >= 0);
  ok('d11 paper fragment without source shows 報紙花邊', rh.indexOf('來源：報紙花邊') >= 0);
  ok('d12 sourceless card shows neutral default', rh.indexOf('來源：街坊傳聞') >= 0);
  ok('d13 no empty/undefined source rendered', rh.indexOf('來源：</p>') < 0 && rh.indexOf('undefined') < 0);
})();

/* ================================================================
   段五 (e)：P1-1(a)——壓力後果數字行真計法：
   stressImpact34 分支值＋真 chance() 折減比率＋真 showStressPreviewModal 整合。
   （打工收入分支 pay×0.5／×0.2 由 static 測試釘住 resolvePlannedDay 真碼。）
   ================================================================ */
(function(){
  eval(extractFn('stressImpact34'));
  eval(extractFn('stressImpactLine34'));
  const near = (a,b)=> Math.abs(a-b) < 1e-9;
  ok('e1 impact below 70: no discount', near(stressImpact34(0).income,1) && near(stressImpact34(69).audition,1));
  ok('e2 impact at 70: income 0.5 / audition 0.78',
     near(stressImpact34(70).income,0.5) && near(stressImpact34(70).audition,0.78) && near(stressImpact34(89).income,0.5));
  ok('e3 impact at 90: income 0.2 / audition 0.78*0.7',
     near(stressImpact34(90).income,0.2) && near(stressImpact34(95).audition,0.78*0.7) && near(stressImpact34(100).income,0.2));
  [75, 95].forEach(s=>{
    const im = stressImpact34(s);
    const line = stressImpactLine34(s);
    ok('e4 line numbers derived from impact fn @'+s,
       line.indexOf(Math.round(im.income*100)+'%') >= 0 && line.indexOf(Math.round(im.audition*100)+'%') >= 0);
  });

  /* 真 chance()：同一狀態淨改壓力，成功率比率要等於真碼乘數 */
  var S = { acting:30, stage:0, vocal:0, looks:0, iq:0, charm:0, stamina:100, stress:0,
    fame:0, popularity:0, npcs:{ director:0, agent:0, colleague:0 }, flags:{} };
  eval(extractFn('clamp'));
  eval(extractFn('chance'));
  const gig = { id:'g34_chance', req:{ acting:30 }, tier:'初', hard:0.4 };
  const p0 = chance(gig);
  S.stress = 75; const p75 = chance(gig);
  S.stress = 95; const p95 = chance(gig);
  ok('e5 real chance: stress 75 ratio = 0.78', Math.abs(p75/p0 - 0.78) < 0.001);
  ok('e6 real chance: stress 95 ratio = 0.78*0.7', Math.abs(p95/p0 - 0.78*0.7) < 0.001);
  ok('e7 helper matches real chance ratios',
     Math.abs(stressImpact34(75).audition - p75/p0) < 0.001 && Math.abs(stressImpact34(95).audition - p95/p0) < 0.001);

  /* 真預覽 modal：高峰 95 → 後果行有 20%／55%；高峰 75 → 50%／78% */
  var modalBodies = [];
  var modal = (body)=>{ modalBodies.push(body); };
  var planDraft = [];
  var livingCostEstimate = ()=> 1600;
  var livingCostRangeLabel = ()=> '';
  var isLowRiskWeek = ()=> false;
  var moneyRecoveryHint = ()=> '';
  S = { money: 12000 };
  eval(extractFn('showStressPreviewModal'));
  showStressPreviewModal({ start:30, end:95, peak:95, rows:[{ wd:'一', name:'街頭表演', delta:5, sign:'+5', after:95 }] }, ()=>{});
  ok('e8 preview @peak95 shows consequence line with real numbers',
     modalBodies.length === 1 && modalBodies[0].indexOf('後果講明') >= 0
     && modalBodies[0].indexOf('約 20%') >= 0 && modalBodies[0].indexOf('約 55%') >= 0);
  modalBodies = [];
  showStressPreviewModal({ start:30, end:75, peak:75, rows:[{ wd:'一', name:'街頭表演', delta:5, sign:'+5', after:75 }] }, ()=>{});
  ok('e9 preview @peak75 shows 50%/78%',
     modalBodies.length === 1 && modalBodies[0].indexOf('約 50%') >= 0 && modalBodies[0].indexOf('約 78%') >= 0);
})();

/* ================================================================
   段六 (f)：P1-1(b)——真 dualTrackExplainHtml34。
   v20a37 改約：舊約「有正 delta 先出」經實機證實喺真路徑永不觸發
   （C1／C2 揀嘅 effects.stats 全空、delta 永遠 0）；新約係第一次事態
   結算展示雙軌面板（result 帶 dual 物件）就出、只出一次；冇 result／
   冇 dual 物件唔出亦唔燒旗。真路徑覆核喺 test_verify37_logic.js 段一。
   ================================================================ */
(function(){
  var saveCalls = 0;
  var saveQ = ()=>{ saveCalls++; };
  var S = { flags:{} };
  eval(extractFn('dualTrackExplainHtml34'));
  const rN = dualTrackExplainHtml34(null);
  ok('f1 null result: no explainer, flag untouched', rN === '' && !S.flags.guidanceDualExplained34);
  const rE = dualTrackExplainHtml34({});
  ok('f2 result without dual object: no explainer, flag untouched', rE === '' && !S.flags.guidanceDualExplained34);
  const r0 = dualTrackExplainHtml34({ dual:{ dStage:0, dCredit:0 } });
  ok('f3 first real settle (zero delta, C1/C2 shape): explainer shown with grounded scale',
     r0.indexOf('聲望＝觀眾識唔識你') >= 0 && r0.indexOf('15') >= 0 && r0.indexOf('40') >= 0
     && r0.indexOf('信用＝行內人信唔信你') >= 0);
  ok('f4 flag set after showing', S.flags.guidanceDualExplained34 === true);
  const r2 = dualTrackExplainHtml34({ dual:{ dStage:1, dCredit:1 } });
  ok('f5 second settlement: explainer NOT repeated', r2 === '');
  var S2 = { flags:{} };
  S = S2;
  const r3 = dualTrackExplainHtml34({ dual:{ dStage:2, dCredit:0 } });
  ok('f6 positive gain also triggers (fresh save)', r3.indexOf('何生提你') >= 0 && S2.flags.guidanceDualExplained34 === true);
})();

console.log(fails.length ? ('\nGUIDANCE34 LOGIC: '+fails.length+' FAIL') : '\nGUIDANCE34 LOGIC: ALL PASS');
process.exit(fails.length ? 1 : 0);
