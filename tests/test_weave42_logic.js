// Weave Phase 4-2（v20a25）邏輯測試：人情帳本 favorLedger＋鏈 F 第 2 拍（芬姐離港／人情絕響）
// 跟 v20a22 教訓：結清計數全部行真入口（applyMockAsk／favorDueTick／exodusFenTick／renderDebtPane），
// 唔直接改 S 扮結清；日期行真 dateObj／calendarSeason／yearSeasonNow。
// 用法：node tests/test_weave42_logic.js [path-to-index.html]
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
  let depth=0, j=i;
  while(j<html.length && html[j]!=='{' && html[j]!=='[') j++;
  const openCh = html[j], closeCh = openCh==='{' ? '}' : ']';
  let started=false;
  for(; j<html.length; j++){
    if(html[j]===openCh){ depth++; started=true; }
    else if(html[j]===closeCh){ depth--; if(started && depth===0) break; }
  }
  return html.slice(i, j+1)+';';
}
const LEDGER_SRC = ['ensureFavorLedger','favorLedgerNoteSettled','favorLedgerNoteCredit','favorLedgerCounts'].map(extractFn).join('\n');

/* ================================================================
   段一：帳本基本＋舊檔回填（favorDueSettled／mockSeasonCleared 推斷；作廢唔計）
   ================================================================ */
(function(){
  var S = {
    dayIndex: 40,
    favorDueSettled: {
      debt_ho_tutorial: { result:'repaid_help', day:30 },
      debt_old_a: { result:'closed_other', day:20 },
      debt_old_b: { result:'void_expired', day:25 }
    },
    mockSeasonCleared: { card_ho_spring:true, card_zhang_spring:true, card_may_summer:false },
    mockDebts: [], mockCredits: []
  };
  eval(LEDGER_SRC);
  const L = ensureFavorLedger();
  ok('backfill: settled = repaid_help+closed_other+2 season = 4', L.settled===4);
  ok('backfill: void_expired not counted', !L.counted['debt_old_b']);
  ok('backfill: credits starts 0', L.credits===0);
  ensureFavorLedger();
  ok('backfill: idempotent on re-ensure', ensureFavorLedger().settled===4);
  ok('note settled new id +1', favorLedgerNoteSettled('debt_new', 'repay_cash')===true && L.settled===5);
  ok('note settled same id no double', favorLedgerNoteSettled('debt_new', 'repay_cash')===false && L.settled===5);
  ok('note credit +1', favorLedgerNoteCredit('credit_new', 'seed')===true && L.credits===1);
  ok('note credit same id no double', favorLedgerNoteCredit('credit_new', 'seed')===false && L.credits===1);
  const c = favorLedgerCounts();
  ok('counts shape', c.settled===5 && c.credits===1 && c.creditsHeld===0 && c.openDebts===0 && Array.isArray(c.exodus));
})();

/* ================================================================
   段二：真 applyMockAsk 還款路徑——一般債／季節卡／教學債各 +1，來源正確
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
  var canRepayDebtById = (id)=> ({ ok:true, debt:curDebt, cashOk:true, giftId:'gift_tea' });
  var apply = (delta)=>{ if(delta && typeof delta.money==='number') S.money = (Number(S.money)||0) + delta.money; };
  var refreshMoneyHud = ()=>{};
  var R = (a)=> a;
  var bumpNpc = ()=> 0;
  var noteWeekHighlight = ()=>{};
  var syncNotebookMirror = ()=>{};
  var saveQ = ()=>{};
  var displayRumor = (r)=> r;
  var GiftShop = { invCount: (gid)=> (S.inventory && S.inventory[gid]) || 0 };
  var curDebt = null;
  var S = null;
  eval(extractConst('FAVOR_DUE_CFG').replace('const FAVOR_DUE_CFG', 'globalThis.__FDC2'));
  var FAVOR_DUE_CFG = globalThis.__FDC2;
  eval(extractConst('MOCK_TOAST').replace('const MOCK_TOAST', 'globalThis.__MT2'));
  var MOCK_TOAST = globalThis.__MT2;
  eval(extractConst('SEASON_COLLECT').replace('const SEASON_COLLECT', 'globalThis.__SC2'));
  var SEASON_COLLECT = globalThis.__SC2;
  eval(extractFn('debtCreditorName'));
  eval(extractFn('ensureFavorDueSettled'));
  eval(extractFn('ensureSeasonDebtClearedBag'));
  eval(LEDGER_SRC);
  eval(extractFn('applyMockAsk'));

  function baseS(){ return { money:1000, dayIndex:6, inventory:{}, npcs:{ agent:50 }, mockDebts:[], mockRumors:[], mockCredits:[], favorDueSettled:{}, mockSeasonCleared:{} }; }

  // A：一般債現金還
  S = baseS();
  curDebt = { id:'debt_generic_x', creditor:'阿標', title:'一般人情', weight:'細', season:'', status:'未到期' };
  S.mockDebts = [curDebt];
  let r = applyMockAsk('agency_ho', 'act_ho_repay', { debtId:'debt_generic_x', mode:'cash' });
  ok('A repay ok', !!(r && r.ok && r.cleared));
  ok('A ledger settled 1 source repay_cash', S.favorLedger.settled===1 && S.favorLedger.counted['debt_generic_x'].source==='repay_cash');

  // B：一般債禮物還
  S = baseS(); S.inventory = { gift_tea:1 };
  curDebt = { id:'debt_generic_y', creditor:'阿標', title:'一般人情二', weight:'細', season:'', status:'未到期' };
  S.mockDebts = [curDebt];
  r = applyMockAsk('agency_ho', 'act_ho_repay', { debtId:'debt_generic_y', mode:'gift', giftId:'gift_tea' });
  ok('B gift repay ok', !!(r && r.ok && r.cleared));
  ok('B ledger settled 1 source repay_gift', S.favorLedger.settled===1 && S.favorLedger.counted['debt_generic_y'].source==='repay_gift');

  // C：季節卡還清（實際語義＝玩家欠債主 → settled，來源 repay_season）
  S = baseS();
  curDebt = { id:'card_ho_spring', creditor:'何生', title:'何生春季數', weight:'季節催收', season:'', status:'就嚟到期', _seasonCard:true };
  r = applyMockAsk('agency_ho', 'act_ho_repay', { debtId:'card_ho_spring', mode:'cash' });
  ok('C season repay ok', !!(r && r.ok && r.cleared));
  ok('C season cleared bag set', S.mockSeasonCleared['card_ho_spring']===true);
  ok('C ledger settled 1 source repay_season, credits 0', S.favorLedger.settled===1 && S.favorLedger.credits===0 && S.favorLedger.counted['card_ho_spring'].source==='repay_season');

  // D：教學債現金還（closed_other；同 favorDueSettled 雙寫但帳本只計一次）
  S = baseS();
  curDebt = { id:'debt_ho_tutorial', creditor:'何生', title:'教學人情（記低未還）', weight:'舉手之勞', season:'', status:'未到期', kind:'help_gig', favorState:'pending', dueDay:13 };
  S.mockDebts = [curDebt];
  r = applyMockAsk('agency_ho', 'act_ho_repay', { debtId:'debt_ho_tutorial', mode:'cash' });
  ok('D tutorial repay ok', !!(r && r.ok && r.cleared));
  ok('D favorDueSettled closed_other (existing behaviour)', S.favorDueSettled.debt_ho_tutorial.result==='closed_other');
  ok('D ledger settled 1 source closed_other', S.favorLedger.settled===1 && S.favorLedger.counted['debt_ho_tutorial'].source==='closed_other');
})();

/* ================================================================
   段三：真 favorDueTick——幫忙結清計 settled／作廢唔計／closed_other 兜底計
   ================================================================ */
(function(){
  var toastCalls = [];
  var toast = (m, opts)=>{ toastCalls.push({ m:String(m), opts:opts||null }); };
  var bumpNpc = ()=> 0;
  var saveQ = ()=>{};
  var syncNotebookMirror = ()=>{};
  var ensureMockJournal = ()=>{};
  var normalizeGigRecord = (g)=> g;
  var window = {};
  var GIGS = [];
  var S = null;
  eval(extractConst('FAVOR_DUE_CFG').replace('const FAVOR_DUE_CFG', 'globalThis.__FDC3'));
  var FAVOR_DUE_CFG = globalThis.__FDC3;
  eval(extractConst('FAVOR_DUE_GIGS').replace('const FAVOR_DUE_GIGS', 'globalThis.__FDG3'));
  var FAVOR_DUE_GIGS = globalThis.__FDG3;
  eval(extractFn('favorDueDebt'));
  eval(extractFn('ensureFavorDueSettled'));
  eval(extractFn('ensureFavorDue'));
  eval(LEDGER_SRC);
  eval(extractFn('favorDueTick'));

  const base = { id:'debt_ho_tutorial', creditor:'何生', title:'教學人情（記低未還）', weight:'舉手之勞', season:'', status:'未到期', kind:'help_gig', favorState:'pending', dueDay:9 };

  // repaid_help：called＋幫忙通告已殺青
  S = { dayIndex:11, mockDebts:[Object.assign({}, base, { favorState:'called', favorGigDay:9 })], wrapHistory:[{ gigId:'gig_favor_ho_errand' }], flags:{}, npcs:{ agent:50 }, favorDueSettled:{}, mockCredits:[] };
  favorDueTick();
  ok('repaid_help: debt removed', S.mockDebts.length===0);
  ok('repaid_help: ledger settled 1', !!(S.favorLedger && S.favorLedger.settled===1 && S.favorLedger.counted['debt_ho_tutorial'].source==='repaid_help'));

  // void_expired：called 過窗口無做 → 作廢，唔計 settled
  S = { dayIndex:20, mockDebts:[Object.assign({}, base, { favorState:'called', favorGigDay:9 })], wrapHistory:[], flags:{}, npcs:{ agent:50 }, favorDueSettled:{}, mockCredits:[] };
  favorDueTick();
  ok('void: settled record is void_expired', S.favorDueSettled.debt_ho_tutorial.result==='void_expired');
  ok('void: ledger settled stays 0', !S.favorLedger || S.favorLedger.settled===0);

  // closed_other 兜底：債已唔見（玩家用其他方法還咗）＋armed → tick 記帳，只計一次
  S = { dayIndex:8, mockDebts:[], wrapHistory:[], flags:{}, npcs:{ agent:50 }, favorDueSettled:{}, favorDueArmed:true, mockCredits:[] };
  favorDueTick();
  ok('closed_other fallback: record written', S.favorDueSettled.debt_ho_tutorial.result==='closed_other');
  ok('closed_other fallback: ledger settled 1', S.favorLedger.settled===1);
  favorDueTick();
  ok('closed_other fallback: second tick no double count', S.favorLedger.settled===1);
})();

/* ================================================================
   段四：芬姐播種——1988 唔種／1989 春種一對／冪等／已結清唔重種
   （行真 ensureMockJournal 入口＋真日曆）
   ================================================================ */
(function(){
  var S = null;
  eval(extractConst('START').replace('const START', 'globalThis.__START4'));
  var START = globalThis.__START4;
  eval(extractConst('MERGE_FRAGS').replace('const MERGE_FRAGS', 'globalThis.__MF4'));
  var MERGE_FRAGS = globalThis.__MF4;
  eval(extractConst('EXODUS_RUMOR_SEEDS').replace('const EXODUS_RUMOR_SEEDS', 'globalThis.__ERS4'));
  var EXODUS_RUMOR_SEEDS = globalThis.__ERS4;
  eval(extractConst('EXODUS_FEN_DEBT').replace('const EXODUS_FEN_DEBT', 'globalThis.__EFD4'));
  var EXODUS_FEN_DEBT = globalThis.__EFD4;
  eval(extractConst('EXODUS_FEN_CREDIT').replace('const EXODUS_FEN_CREDIT', 'globalThis.__EFC4'));
  var EXODUS_FEN_CREDIT = globalThis.__EFC4;
  eval(extractFn('dateObj'));
  eval(extractFn('calendarSeason'));
  eval(extractFn('yearSeasonNow'));
  eval(extractFn('healMayDebtCopy'));
  eval(extractFn('syncNotebookMirror'));
  eval(LEDGER_SRC);
  eval(extractFn('seedExodusFenPair'));
  eval(extractFn('ensureMockJournal'));

  function saveAt(day){ return { dayIndex:day, mockJournalSeeded:true, mockRumors:[], mockDebts:[], mockCredits:[], favorDueSettled:{}, mockSeasonCleared:{} }; }

  S = saveAt(10); // 1988 春
  ensureMockJournal();
  ok('1988: no fen debt seeded', !S.mockDebts.some(d=>d.id==='debt_fen_standin'));
  ok('1988: no fen credit seeded', !(S.mockCredits||[]).some(c=>c.id==='credit_fen_rescue'));
  ok('1988: ledger credits 0', favorLedgerCounts().credits===0);

  S = saveAt(370); // 1989 春（1989-03-12）
  ensureMockJournal();
  ok('1989 spring: fen debt seeded', S.mockDebts.some(d=>d.id==='debt_fen_standin'));
  ok('1989 spring: fen credit seeded', S.mockCredits.some(c=>c.id==='credit_fen_rescue' && c.status==='未收'));
  ok('1989 spring: ledger credits 1', favorLedgerCounts().credits===1);
  ensureMockJournal();
  ok('seed idempotent: still one pair', S.mockDebts.filter(d=>d.id==='debt_fen_standin').length===1 && S.mockCredits.filter(c=>c.id==='credit_fen_rescue').length===1 && favorLedgerCounts().credits===1);

  // 已結清過（counted 有紀錄）→ 唔重種筆債（旗遺失都要守）
  S = saveAt(370);
  favorLedgerNoteSettled('debt_fen_standin', 'repay_cash');
  seedExodusFenPair();
  ok('settled fen debt never reseeds', !S.mockDebts.some(d=>d.id==='debt_fen_standin'));
})();

/* ================================================================
   段五：離港事件——兩分支齊／只觸發一次／無對分支仍有 toast＋情報／1990 catch-up
   ================================================================ */
(function(){
  var toastCalls = [];
  var toast = (m, opts)=>{ toastCalls.push({ m:String(m), opts:opts||null }); };
  var saveQ = ()=>{};
  var syncNotebookMirror = ()=>{};
  var S = null;
  eval(extractConst('START').replace('const START', 'globalThis.__START5'));
  var START = globalThis.__START5;
  eval(extractConst('EXODUS_FEN_DEBT').replace('const EXODUS_FEN_DEBT', 'globalThis.__EFD5'));
  var EXODUS_FEN_DEBT = globalThis.__EFD5;
  eval(extractConst('EXODUS_FEN_CREDIT').replace('const EXODUS_FEN_CREDIT', 'globalThis.__EFC5'));
  var EXODUS_FEN_CREDIT = globalThis.__EFC5;
  eval(extractConst('EXODUS_FEN_INTEL').replace('const EXODUS_FEN_INTEL', 'globalThis.__EFI5'));
  var EXODUS_FEN_INTEL = globalThis.__EFI5;
  eval(extractFn('dateObj'));
  eval(extractFn('calendarSeason'));
  eval(extractFn('yearSeasonNow'));
  eval(LEDGER_SRC);
  eval(extractFn('seedExodusFenPair'));
  eval(extractFn('exodusFenTick'));

  function saveAt(day){ return { dayIndex:day, mockRumors:[], mockDebts:[], mockCredits:[], favorDueSettled:{}, mockSeasonCleared:{} }; }

  // 全對在場：春播種 → 夏觸發
  S = saveAt(370); toastCalls = [];
  seedExodusFenPair();
  S.dayIndex = 545; // 1991 夏（1991-06-30；v20a67 1 月 epoch 重對位）
  exodusFenTick();
  ok('exodus: debt written off (removed)', !S.mockDebts.some(d=>d.id==='debt_fen_standin'));
  ok('exodus: write-off counts settled with source', S.favorLedger.settled===1 && S.favorLedger.counted['debt_fen_standin'].source==='exodus_writeoff');
  const cred = S.mockCredits.find(c=>c.id==='credit_fen_rescue');
  ok('exodus: credit becomes 絕響', !!cred && cred.status==='絕響');
  ok('exodus: ledger.exodus lists credit', S.favorLedger.exodus.indexOf('credit_fen_rescue')>=0);
  ok('exodus: intel frag added', S.mockRumors.some(r=>r.id==='rumor_fen_exodus_tip'));
  ok('exodus: toast fired once with write-off main', toastCalls.length===1 && toastCalls[0].m.indexOf('一筆勾銷')>=0);
  exodusFenTick();
  ok('exodus: fires only once', toastCalls.length===1 && S.favorLedger.settled===1);

  // 觸發前已還清筆債（帳本已有結清紀錄、債行已移除）→ 只剩絕響分支，唔雙計
  S = saveAt(370); toastCalls = [];
  seedExodusFenPair();
  S.mockDebts = S.mockDebts.filter(d=>d.id!=='debt_fen_standin');
  favorLedgerNoteSettled('debt_fen_standin', 'repay_cash');
  S.dayIndex = 545;
  exodusFenTick();
  ok('exodus after repay: settled stays 1 (no double)', S.favorLedger.settled===1);
  ok('exodus after repay: credit still 絕響', S.mockCredits.find(c=>c.id==='credit_fen_rescue').status==='絕響');
  ok('exodus after repay: toast mentions 絕響', toastCalls.length===1 && toastCalls[0].m.indexOf('絕響')>=0);

  // 兩邊都無（種過但兩項都唔在場）→ 仍有 toast＋情報，唔靜默
  S = saveAt(545); toastCalls = []; // 1991 夏（觸發窗內）
  S.exodusFenSeeded = true; // 種子旗已置，兩項均已處理完／唔在場
  exodusFenTick();
  ok('exodus neither: toast still fires', toastCalls.length===1);
  ok('exodus neither: intel frag still added', S.mockRumors.some(r=>r.id==='rumor_fen_exodus_tip'));
  ok('exodus neither: no phantom counts', favorLedgerCounts().settled===0);

  // 1989 春未到夏：唔觸發
  S = saveAt(370); toastCalls = [];
  seedExodusFenPair();
  exodusFenTick();
  ok('spring: event not fired yet', toastCalls.length===0 && !S.exodusFenFired);

  // catch-up：存檔已喺 1990（更新前跨咗年）→ 補種＋即時觸發
  S = saveAt(760); toastCalls = []; // 1992-01-30（已過觸發窗，catch-up）
  exodusFenTick();
  ok('catch-up 1990: fired with write-off', !!S.exodusFenFired && S.favorLedger.settled===1 && toastCalls.length===1);
})();

/* ================================================================
   段六：渲染路徑——真 renderDebtPane 絕響灰階／債權段／favorPressure＋還款入口排除絕響
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
  eval(extractConst('FAVOR_DUE_CFG').replace('const FAVOR_DUE_CFG', 'globalThis.__FDC6'));
  var FAVOR_DUE_CFG = globalThis.__FDC6;
  eval(extractConst('MOCK_DEBT_TUTORIAL').replace('const MOCK_DEBT_TUTORIAL', 'globalThis.__MDT6'));
  var MOCK_DEBT_TUTORIAL = globalThis.__MDT6;
  eval(extractConst('SEASON_COLLECT').replace('const SEASON_COLLECT', 'globalThis.__SC6'));
  var SEASON_COLLECT = globalThis.__SC6;
  eval(extractConst('DEBT_FUZZY').replace('const DEBT_FUZZY', 'globalThis.__DF6'));
  var DEBT_FUZZY = globalThis.__DF6;
  eval(extractConst('MOCK_EMPTY').replace('const MOCK_EMPTY', 'globalThis.__ME6'));
  var MOCK_EMPTY = globalThis.__ME6;
  eval(extractFn('journalText'));
  eval(extractFn('debtStatusLabel'));
  eval(extractFn('debtCreditorName'));
  eval(extractFn('ensureSeasonDebtClearedBag'));
  eval(extractFn('favorPressure'));
  eval(extractFn('allDebtsForRepay'));
  eval(extractFn('favorDueDebt'));
  eval(extractFn('ensureFavorDueSettled'));
  eval(extractFn('ensureFavorDue'));
  eval(extractFn('favorDueHintText'));
  eval(extractFn('renderDebtPane'));

  S = { dayIndex:5, npcs:{},
    favorDueSettled:{ debt_ho_tutorial:{ result:'repaid_help', day:1 } },
    mockSeasonCleared:{},
    mockDebts:[
      { id:'debt_ghost', creditor:'某舊識', title:'舊人情', weight:'細', season:'', status:'絕響' },
      { id:'debt_live', creditor:'阿標', title:'現行人情', weight:'細', season:'', status:'已逾期' }
    ],
    mockCredits:[
      { id:'credit_fen_rescue', debtor:'副導演芬姐', title:'芬姐欠你嗰次救場', line:'清水灣外景嗰日亂到七彩。', status:'絕響' },
      { id:'credit_live', debtor:'副導阿標', title:'阿標欠你嗰次', line:'記住先。', status:'未收' }
    ] };
  renderDebtPane();
  const h = box.innerHTML;
  ok('render: exodus grey class on 絕響 credit', h.indexOf('credit-row debt-exodus')>=0);
  ok('render: 人已不在香港 copy present', h.indexOf('人已不在香港')>=0);
  ok('render: credit section labels debtor', h.indexOf('欠你人情：副導演芬姐')>=0);
  ok('render: live credit not greyed alone', (h.match(/debt-exodus/g)||[]).length===2); // 絕響 credit + 絕響 debt 各一
  ok('render: no repay button for 絕響 debt', h.indexOf('data-repay-id="debt_ghost"')<0);
  ok('render: repay button kept for live debt', h.indexOf('data-repay-id="debt_live"')>=0);
  ok('pressure: 絕響 excluded, only live overdue counts', favorPressure().n===1);
  const repayIds = allDebtsForRepay().map(d=>d.id);
  ok('repay list: 絕響 excluded', repayIds.indexOf('debt_ghost')<0 && repayIds.indexOf('debt_live')>=0);
})();

/* ================================================================
   段七：favorLedgerCounts——結局判定讀取口
   ================================================================ */
(function(){
  var S = { dayIndex: 100,
    favorLedger: { settled:5, credits:2, exodus:['credit_fen_rescue'], counted:{} , __bf:1 },
    mockCredits:[ { id:'c1', status:'未收' }, { id:'credit_fen_rescue', status:'絕響' } ],
    mockDebts:[ { id:'d1', status:'未到期' }, { id:'d2', status:'絕響' } ] };
  eval(LEDGER_SRC);
  const c = favorLedgerCounts();
  ok('counts: settled/credits passthrough', c.settled===5 && c.credits===2);
  ok('counts: creditsHeld excludes 絕響', c.creditsHeld===1);
  ok('counts: openDebts excludes 絕響', c.openDebts===1);
  ok('counts: exodus list passthrough', c.exodus.length===1 && c.exodus[0]==='credit_fen_rescue');
})();

console.log(fails.length ? ('\nFAILED: '+fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length?1:0);
