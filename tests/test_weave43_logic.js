// Weave Phase 4-3（v20a26）邏輯測試：鏈 G 屋企線——屋企恆常債 debt_family_home＋家人態度字條
// 跟 v20a22 教訓：播種行真 ensureMockJournal、還款行真 applyMockAsk、跨月行真 advanceDay＋真 dateObj、
// 渲染行真 renderDebtPane、週結算行真 settleWeek；唔直接改 S 扮還清（段五嘅狀態安排只係 arrange 消費標記）。
// 用法：node tests/test_weave43_logic.js [path-to-index.html]
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
  const i = html.indexOf('const '+name+' =') >= 0 ? html.indexOf('const '+name+' =') : html.indexOf('const '+name+'=');
  if(i<0) throw new Error('const not found: '+name);
  let depth=0, j=i;
  while(j<html.length && html[j]!=='{' && html[j]!=='[' && html[j]!==';') j++;
  if(html[j]===';') return html.slice(i, j+1);
  const openCh = html[j], closeCh = openCh==='{' ? '}' : ']';
  let started=false;
  for(; j<html.length; j++){
    if(html[j]===openCh){ depth++; started=true; }
    else if(html[j]===closeCh){ depth--; if(started && depth===0) break; }
  }
  return html.slice(i, j+1)+';';
}
const FAM_SRC = [
  extractConst('FAMILY_HOME_DEBT_ID'), extractConst('FAMILY_HOME_CYCLES'),
  extractConst('FAMILY_HOME_SEED_FLAVOR'), extractConst('FAMILY_HOME_PAID_FLAVOR'),
  extractFn('ensureFamilyHomeState'), extractFn('familyMonthKey'), extractFn('isFamilyHomeDebt'),
  extractFn('ensureFamilyHomeDebt'), extractFn('noteFamilyHomePaid'),
  extractFn('familyHomeSettleLines'), extractFn('familyAttitudeLine')
].join('\n');
const LEDGER_SRC = ['ensureFavorLedger','favorLedgerNoteSettled','favorLedgerNoteCredit','favorLedgerCounts'].map(extractFn).join('\n');

/* ================================================================
   段一：播種——真 ensureMockJournal 入口：新檔第一筆債＝屋企債、舊檔補種、只一筆
   ================================================================ */
(function(){
  var S = null;
  eval(extractConst('START').replace('const START', 'globalThis.__START1'));
  var START = globalThis.__START1;
  eval(extractConst('MERGE_FRAGS').replace('const MERGE_FRAGS', 'globalThis.__MF1'));
  var MERGE_FRAGS = globalThis.__MF1;
  eval(extractConst('EXODUS_RUMOR_SEEDS').replace('const EXODUS_RUMOR_SEEDS', 'globalThis.__ERS1'));
  var EXODUS_RUMOR_SEEDS = globalThis.__ERS1;
  eval(extractConst('EXODUS_FEN_DEBT').replace('const EXODUS_FEN_DEBT', 'globalThis.__EFD1'));
  var EXODUS_FEN_DEBT = globalThis.__EFD1;
  eval(extractConst('EXODUS_FEN_CREDIT').replace('const EXODUS_FEN_CREDIT', 'globalThis.__EFC1'));
  var EXODUS_FEN_CREDIT = globalThis.__EFC1;
  eval(extractFn('dateObj'));
  eval(extractFn('calendarSeason'));
  eval(extractFn('yearSeasonNow'));
  eval(extractFn('healMayDebtCopy'));
  eval(extractFn('syncNotebookMirror'));
  eval(LEDGER_SRC);
  eval(extractFn('seedExodusFenPair'));
  eval(FAM_SRC.replace(/const FAMILY_HOME_DEBT_ID/g, 'var FAMILY_HOME_DEBT_ID').replace(/const FAMILY_HOME_CYCLES/g, 'var FAMILY_HOME_CYCLES').replace(/const FAMILY_HOME_SEED_FLAVOR/g, 'var FAMILY_HOME_SEED_FLAVOR').replace(/const FAMILY_HOME_PAID_FLAVOR/g, 'var FAMILY_HOME_PAID_FLAVOR'));
  eval(extractFn('ensureMockJournal'));

  // 新檔：mockJournalSeeded 未置，dayIndex 0（1988-03-07）
  S = { dayIndex:0 };
  ensureMockJournal();
  const fam = (S.mockDebts||[]).filter(d=>d.id==='debt_family_home');
  ok('new save: family debt seeded exactly once', fam.length===1);
  ok('new save: family debt is the FIRST and only debt at start', S.mockDebts.length===1 && S.mockDebts[0].id==='debt_family_home');
  ok('new save: family debt shape', fam.length===1 && fam[0].creditor==='屋企／阿媽' && fam[0].amount===600 && fam[0].status==='未到期' && fam[0].dueDay==null);
  ensureMockJournal();
  ok('new save: reseed guard — still one after re-ensure', (S.mockDebts||[]).filter(d=>d.id==='debt_family_home').length===1);

  // 舊檔：已有其他債、無屋企債 → 補種一筆，其他債唔受影響
  S = { dayIndex:100, mockJournalSeeded:true, mockRumors:[], mockDebts:[{ id:'debt_other', creditor:'阿標', title:'舊債', weight:'細', season:'', status:'未到期' }], mockCredits:[], favorDueSettled:{}, mockSeasonCleared:{} };
  ensureMockJournal();
  ok('old save: family debt seeded on first load', (S.mockDebts||[]).filter(d=>d.id==='debt_family_home').length===1);
  ok('old save: existing debt untouched', S.mockDebts.some(d=>d.id==='debt_other') && S.mockDebts.length===2);
  ensureMockJournal();
  ok('old save: still exactly one family debt', (S.mockDebts||[]).filter(d=>d.id==='debt_family_home').length===1);
})();

/* ================================================================
   段二：恆常機制——真 applyMockAsk 還款＋真 advanceDay 跨月補種／未還唔補／冪等
   ================================================================ */
(function(){
  var _storyPlayLocked = false;
  var isStoryPlayActive = ()=> false;
  var ensureMockJournal = ()=>{};
  var mockAskDefs = (id)=> id==='agency_ho' ? [{ id:'act_ho_repay', repay:true, title:'還人情 / 送禮', cost:'禮物／現金' }] : null;
  var mockAskAlreadyHeard = ()=> false;
  var softPreviewOn = ()=> true;
  var softSocialDailyCap = ()=> ({ ok:true });
  var softSocialDailyUse = ()=>{};
  var curDebt = null;
  var canRepayDebtById = (id)=> ({ ok:true, debt:curDebt, cashOk:true, giftId:null });
  var apply = (delta)=>{ if(delta && typeof delta.money==='number') S.money = (Number(S.money)||0) + delta.money; };
  var refreshMoneyHud = ()=>{};
  var refreshNpc = ()=>{};
  var R = (a)=> a;
  var bumpNpc = ()=> 0;
  var noteWeekHighlight = ()=>{};
  var syncNotebookMirror = ()=>{};
  var saveQ = ()=>{};
  var displayRumor = (r)=> r;
  var GiftShop = { invCount: ()=> 0 };
  var LOCS = [];
  var S = null;
  eval(extractConst('START').replace('const START', 'globalThis.__START2'));
  var START = globalThis.__START2;
  eval(extractConst('FAVOR_DUE_CFG').replace('const FAVOR_DUE_CFG', 'globalThis.__FDC2'));
  var FAVOR_DUE_CFG = globalThis.__FDC2;
  eval(extractConst('MOCK_TOAST').replace('const MOCK_TOAST', 'globalThis.__MT2'));
  var MOCK_TOAST = globalThis.__MT2;
  eval(extractConst('SEASON_COLLECT').replace('const SEASON_COLLECT', 'globalThis.__SC2'));
  var SEASON_COLLECT = globalThis.__SC2;
  eval(extractFn('dateObj'));
  eval(extractFn('weekdayIdx'));
  eval(extractFn('debtCreditorName'));
  eval(extractFn('ensureFavorDueSettled'));
  eval(extractFn('ensureSeasonDebtClearedBag'));
  eval(LEDGER_SRC);
  eval(FAM_SRC.replace(/const FAMILY_HOME_DEBT_ID/g, 'var FAMILY_HOME_DEBT_ID').replace(/const FAMILY_HOME_CYCLES/g, 'var FAMILY_HOME_CYCLES').replace(/const FAMILY_HOME_SEED_FLAVOR/g, 'var FAMILY_HOME_SEED_FLAVOR').replace(/const FAMILY_HOME_PAID_FLAVOR/g, 'var FAMILY_HOME_PAID_FLAVOR'));
  eval(extractFn('applyMockAsk'));
  eval(extractFn('advanceDay'));

  const famCount = ()=> (S.mockDebts||[]).filter(d=>d.id==='debt_family_home').length;
  const adv = (n)=>{ for(let i=0;i<n;i++) advanceDay(); };

  S = { dayIndex:0, money:5000, inventory:{}, npcs:{ agent:50 }, board:{}, flags:{}, mockDebts:[], mockRumors:[], mockCredits:[], favorDueSettled:{}, mockSeasonCleared:{} };
  ok('seed returns true first time', ensureFamilyHomeDebt()===true && famCount()===1);
  ok('seed: cycle0 = 今個月家用 $600', S.mockDebts[0].title==='今個月家用' && S.mockDebts[0].amount===600);

  adv(10); // dayIndex 10，仍係 1988 年 3 月；advanceDay 每日行 ensureFamilyHomeDebt
  ok('same month, debt present: no reseed', famCount()===1 && S.dayIndex===10);

  // 真還款（現金）：清債＋記月份＋唔入帳本
  curDebt = S.mockDebts.find(d=>d.id==='debt_family_home');
  const r = applyMockAsk('agency_ho', 'act_ho_repay', { debtId:'debt_family_home', mode:'cash' });
  ok('repay family debt ok', !!(r && r.ok && r.cleared) && famCount()===0);
  ok('repay: paidDay + monthKey recorded', S.familyHome.paidDay===10 && S.familyHome.monthKey==='1988-3');
  ok('repay: NOT in favorLedger (no ledger entry at all)', !S.favorLedger || !S.favorLedger.counted['debt_family_home']);
  ok('repay: ledger settled stays 0', !S.favorLedger || S.favorLedger.settled===0);

  adv(10); // dayIndex 20，仍係 3 月：還清當月唔補種
  ok('paid same month: no reseed for rest of month', famCount()===0 && S.dayIndex===20);

  adv(5); // dayIndex 25 = 1988-04-01：跨月補種
  ok('next month: reseeded exactly once', famCount()===1 && S.dayIndex===25);
  const d2 = S.mockDebts.find(d=>d.id==='debt_family_home');
  ok('next month: cycle rotated to 交租 $800', d2.title==='今期幫補交租' && d2.amount===800);
  ensureFamilyHomeDebt(); ensureFamilyHomeDebt();
  ok('reseed idempotent on repeated ensure', famCount()===1);

  adv(31); // dayIndex 56 = 1988-05-03：未還就唔好跨月再種
  ok('unpaid across another month: still the same single debt', famCount()===1 && S.mockDebts.find(d=>d.id==='debt_family_home').title==='今期幫補交租');
})();

/* ================================================================
   段三：排除清單——favorPressure／逾期鎖／favorLedger 讀口逐項斷言
   ================================================================ */
(function(){
  var calendarSeason = ()=>'春';
  var BehaviorGate = { featureFlag_softBehaviorGatePreview: ()=> true };
  var S = null;
  eval(extractConst('SEASON_COLLECT').replace('const SEASON_COLLECT', 'globalThis.__SC3'));
  var SEASON_COLLECT = globalThis.__SC3;
  eval(extractConst('PAPER_NAME_TIER_NAMED').replace('const PAPER_NAME_TIER_NAMED', 'globalThis.__PNT3'));
  var PAPER_NAME_TIER_NAMED = globalThis.__PNT3;
  eval(extractConst('PAPER_NAME_TIER_TITLED').replace('const PAPER_NAME_TIER_TITLED', 'globalThis.__PTT3'));
  var PAPER_NAME_TIER_TITLED = globalThis.__PTT3;
  eval(extractFn('debtStatusLabel'));
  eval(extractFn('favorPressure'));
  eval(extractFn('softOverdueFavorDebtLock'));
  eval(LEDGER_SRC);

  const famOverdue = { id:'debt_family_home', creditor:'屋企／阿媽', title:'今個月家用', amount:600, weight:'屋企嗰份', season:'', status:'已逾期', familyHome:true };
  const liveOverdue = { id:'debt_live', creditor:'阿標', title:'現行人情', weight:'細', season:'', status:'已逾期' };

  S = { dayIndex:5, mockDebts:[] };
  const base = favorPressure().n;
  S = { dayIndex:5, mockDebts:[famOverdue] };
  ok('pressure: family debt excluded even if status forced overdue', favorPressure().n===base);
  S = { dayIndex:5, mockDebts:[liveOverdue] };
  ok('pressure: normal overdue debt still counts (control)', favorPressure().n===base+1);
  S = { dayIndex:5, mockDebts:[famOverdue, liveOverdue] };
  ok('pressure: mixed = only live counts', favorPressure().n===base+1);

  S = { dayIndex:5, mockDebts:[famOverdue] };
  ok('lock: family debt never locks gigs', softOverdueFavorDebtLock({ id:'gig_x' }).ok===true);
  S = { dayIndex:5, mockDebts:[liveOverdue] };
  ok('lock: normal overdue debt still locks (control)', softOverdueFavorDebtLock({ id:'gig_x' }).ok===false);

  S = { dayIndex:5, favorLedger:{ settled:3, credits:1, exodus:[], counted:{}, __bf:1 },
        mockCredits:[], mockDebts:[ { id:'debt_family_home', status:'未到期' }, { id:'debt_live', status:'未到期' } ] };
  const c = favorLedgerCounts();
  ok('counts: openDebts excludes family debt', c.openDebts===1);
  ok('counts: settled/credits passthrough untouched', c.settled===3 && c.credits===1);
})();

/* ================================================================
   段四：家人態度字條——真 renderDebtPane × 三個 fame 值，真播種嘅屋企債卡
   ================================================================ */
(function(){
  var box = { innerHTML:'', onclick:null };
  var document = { getElementById: (id)=> id==='debt-list' ? box : null };
  var ensureMockJournal = ()=>{};
  var ensureWeakSeals = ()=>{};
  var softPreviewOn = ()=> true;
  var syncNotebookMirror = ()=>{};
  var calendarSeason = ()=>'春';
  var S = null;
  eval(extractConst('START').replace('const START', 'globalThis.__START4'));
  var START = globalThis.__START4;
  eval(extractConst('FAVOR_DUE_CFG').replace('const FAVOR_DUE_CFG', 'globalThis.__FDC4'));
  var FAVOR_DUE_CFG = globalThis.__FDC4;
  eval(extractConst('MOCK_DEBT_TUTORIAL').replace('const MOCK_DEBT_TUTORIAL', 'globalThis.__MDT4'));
  var MOCK_DEBT_TUTORIAL = globalThis.__MDT4;
  eval(extractConst('SEASON_COLLECT').replace('const SEASON_COLLECT', 'globalThis.__SC4'));
  var SEASON_COLLECT = globalThis.__SC4;
  eval(extractConst('DEBT_FUZZY').replace('const DEBT_FUZZY', 'globalThis.__DF4'));
  var DEBT_FUZZY = globalThis.__DF4;
  eval(extractConst('MOCK_EMPTY').replace('const MOCK_EMPTY', 'globalThis.__ME4'));
  var MOCK_EMPTY = globalThis.__ME4;
  eval(extractConst('PAPER_NAME_TIER_NAMED').replace('const PAPER_NAME_TIER_NAMED', 'globalThis.__PNT4'));
  var PAPER_NAME_TIER_NAMED = globalThis.__PNT4;
  eval(extractConst('PAPER_NAME_TIER_TITLED').replace('const PAPER_NAME_TIER_TITLED', 'globalThis.__PTT4'));
  var PAPER_NAME_TIER_TITLED = globalThis.__PTT4;
  eval(extractFn('dateObj'));
  eval(extractFn('journalText'));
  eval(extractFn('debtStatusLabel'));
  eval(extractFn('debtCreditorName'));
  eval(extractFn('ensureSeasonDebtClearedBag'));
  eval(extractFn('favorPressure'));
  eval(extractFn('favorDueDebt'));
  eval(extractFn('ensureFavorDueSettled'));
  eval(extractFn('ensureFavorDue'));
  eval(extractFn('favorDueHintText'));
  eval(extractFn('newspaperNameTier'));
  eval(FAM_SRC.replace(/const FAMILY_HOME_DEBT_ID/g, 'var FAMILY_HOME_DEBT_ID').replace(/const FAMILY_HOME_CYCLES/g, 'var FAMILY_HOME_CYCLES').replace(/const FAMILY_HOME_SEED_FLAVOR/g, 'var FAMILY_HOME_SEED_FLAVOR').replace(/const FAMILY_HOME_PAID_FLAVOR/g, 'var FAMILY_HOME_PAID_FLAVOR'));
  eval(extractFn('renderDebtPane'));

  function renderAt(fame){
    S = { dayIndex:5, fame:fame, npcs:{},
      favorDueSettled:{ debt_ho_tutorial:{ result:'repaid_help', day:1 } },
      mockSeasonCleared:{}, mockDebts:[], mockCredits:[] };
    ensureFamilyHomeDebt(); // 真播種，唔手砌債物件
    renderDebtPane();
    return box.innerHTML;
  }
  function famCard(htmlStr){
    const i = htmlStr.indexOf('data-debt-id="debt_family_home"');
    if(i<0) return '';
    const j = htmlStr.indexOf('</article>', i);
    return htmlStr.slice(i, j<0?htmlStr.length:j);
  }

  let h = renderAt(5);
  ok('tier anon: family card rendered with repay btn', famCard(h).indexOf('data-repay-id="debt_family_home"')>=0);
  ok('tier anon: attitude = 做臨記唔係辦法', famCard(h).indexOf('做臨記唔係辦法')>=0);
  ok('tier anon: note inside family card (family-attitude class)', famCard(h).indexOf('family-attitude')>=0);

  h = renderAt(20);
  ok('tier named: attitude = 半信半疑＋唔好俾人呃', famCard(h).indexOf('報紙有寫你個名')>=0 && famCard(h).indexOf('唔好俾人呃')>=0);
  ok('tier named: anon copy absent', famCard(h).indexOf('做臨記唔係辦法')<0);

  h = renderAt(50);
  ok('tier titled: attitude = 我個仔上報紙', famCard(h).indexOf('我個仔上報紙')>=0);
  ok('tier titled: anon/named copy absent', famCard(h).indexOf('做臨記唔係辦法')<0 && famCard(h).indexOf('唔好俾人呃')<0);

  ok('familyAttitudeLine direct: tiers switch', (function(){
    S = { dayIndex:5, fame:5 };
    const a = familyAttitudeLine();
    S.fame = 20; const b = familyAttitudeLine();
    S.fame = 50; const cLine = familyAttitudeLine();
    return a.indexOf('做臨記唔係辦法')>=0 && b.indexOf('報紙有寫你個名')>=0 && cLine.indexOf('上報紙')>=0 && a!==b && b!==cLine;
  })());
})();

/* ================================================================
   段五：週結算 flavor——真 settleWeek：播種週／還清週先出，其他週唔出，唔重複
   ================================================================ */
(function(){
  var softPreviewOn = ()=> true;
  var apply = (delta)=>{ if(delta){ ['money','fame','popularity','charm','stamina','stress'].forEach(k=>{ if(typeof delta[k]==='number') S[k]=(Number(S[k])||0)+delta[k]; }); } return ''; };
  var eventLine = ()=> '';
  var saveQ = ()=>{};
  var bumpNpc = ()=> 0;
  var S = null;
  eval(extractConst('START').replace('const START', 'globalThis.__START5'));
  var START = globalThis.__START5;
  eval(extractFn('dateObj'));
  eval(extractFn('calendarSeason'));
  eval(extractFn('weekNumNow'));
  eval(extractFn('livingCostWeekNum'));
  eval(extractFn('livingCostBand'));
  eval(extractFn('livingCostRoll'));
  eval(extractFn('livingCostEstimate'));
  eval(extractFn('stripSettleMoneyNoise'));
  eval(FAM_SRC.replace(/const FAMILY_HOME_DEBT_ID/g, 'var FAMILY_HOME_DEBT_ID').replace(/const FAMILY_HOME_CYCLES/g, 'var FAMILY_HOME_CYCLES').replace(/const FAMILY_HOME_SEED_FLAVOR/g, 'var FAMILY_HOME_SEED_FLAVOR').replace(/const FAMILY_HOME_PAID_FLAVOR/g, 'var FAMILY_HOME_PAID_FLAVOR'));
  eval(extractFn('settleWeek'));

  function baseS(day){ return { dayIndex:day, money:20000, weekEarn:0, weekGigsDone:1, weekTrainDone:0, stress:10, stamina:60, fame:5, popularity:3, flags:{}, npcs:{}, board:{}, mockDebts:[], mockRumors:[], mockCredits:[], giftMeta:{} }; }

  // 播種嗰週（day 0 種，day 7 結算）
  S = baseS(0);
  ensureFamilyHomeDebt();
  S.dayIndex = 7;
  let r = settleWeek();
  ok('settle seed week: seed flavor appears', r.html.indexOf('屋企人催數，從來唔出聲')>=0);
  S.dayIndex = 14;
  r = settleWeek();
  ok('settle next week: seed flavor does NOT repeat', r.html.indexOf('屋企人催數，從來唔出聲')<0);

  // 還清嗰週（種子 flavor 早已消費；day 20 還清記低，day 21 結算）
  S = baseS(0);
  S.familyHome = { cycle:1, monthKey:'1988-3', seedDay:0, paidDay:-1, seedFlavorDay:0, paidFlavorDay:-1 };
  S.dayIndex = 20;
  noteFamilyHomePaid();
  S.dayIndex = 21;
  r = settleWeek();
  ok('settle paid week: paid flavor appears', r.html.indexOf('煲多咗個湯')>=0);
  ok('settle paid week: seed flavor stays consumed', r.html.indexOf('屋企人催數，從來唔出聲')<0);
  S.dayIndex = 28;
  r = settleWeek();
  ok('settle after paid week: paid flavor does NOT repeat', r.html.indexOf('煲多咗個湯')<0);

  // 静週：無播種無還清
  S = baseS(0);
  S.familyHome = { cycle:1, monthKey:'1988-3', seedDay:-1, paidDay:-1, seedFlavorDay:-1, paidFlavorDay:-1 };
  S.dayIndex = 7;
  r = settleWeek();
  ok('settle quiet week: no family flavor at all', r.html.indexOf('屋企嗰邊')<0);
})();

console.log(fails.length ? ('\nFAILED: '+fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length?1:0);
