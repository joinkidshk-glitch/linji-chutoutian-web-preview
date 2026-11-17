// v20a259 農場洞修補 R1＋R2＋R3＋R4：人情計數新口徑
// R1：茶餐廳幫手債權（credit_enc79_cafe_help_*）唔計 creditsHeld；
// R2：已兌現債權（有 redeemedBy）唔計 creditsHeld；
// R3：settled 只計真係還清（勾銷／作廢／過期唔做唔計）；
// R4：人情頁／結局頁分組顯示「故事債權／茶餐廳幫手／已兌現」。
// 用法：node tests/test_favor259_counts.js [path-to-index.html]
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
var ENDING410_EXODUS_NAME_FALLBACK = {};
const LEDGER_SRC = ['favorCreditCountsAsHeld','ensureFavorLedger','favorLedgerNoteSettled','favorLedgerNoteCredit','favorLedgerCounts','endingFavor410'].map(extractFn).join('\n');

/* ================================================================
   R1：茶餐廳幫手債權唔計 creditsHeld（兩條讀取口一致）
   ================================================================ */
(function(){
  var S = null;
  eval(LEDGER_SRC);
  S = { dayIndex: 100, mockDebts: [],
    mockCredits: [
      { id:'credit_story_a', debtor:'甲', title:'故事債權一', status:'未收' },
      { id:'credit_story_b', debtor:'乙', title:'故事債權二', status:'未收' },
      { id:'credit_enc79_cafe_help_10', debtor:'霞姐', title:'茶餐廳幫手', status:'未收' },
      { id:'credit_enc79_cafe_help_11', debtor:'霞姐', title:'茶餐廳幫手', status:'未收' },
      { id:'credit_enc79_cafe_help_12', debtor:'霞姐', title:'茶餐廳幫手', status:'未收' }
    ],
    favorLedger: { settled:0, credits:5, exodus:[], counted:{}, __bf:1 } };
  ok('R1 favorLedgerCounts：3 筆茶餐廳債權唔計，creditsHeld＝2', favorLedgerCounts().creditsHeld===2);
  ok('R1 endingFavor410：creditsHeld＝2（鏡像一致）', endingFavor410(S).creditsHeld===2);
  ok('R1 creditsTotal 照計（曾獲總數唔郁）', favorLedgerCounts().credits===5);
})();

/* ================================================================
   R2：已兌現債權唔計 creditsHeld（兩條讀取口一致）
   ================================================================ */
(function(){
  var S = null;
  eval(LEDGER_SRC);
  S = { dayIndex: 100, mockDebts: [],
    mockCredits: [
      { id:'credit_story_a', debtor:'甲', title:'故事債權一', status:'未收' },
      { id:'credit_story_b', debtor:'乙', title:'故事債權二', status:'未收' },
      { id:'credit_br89_luk', debtor:'陸柏言', title:'引薦債權', status:'未收', redeemedBy:'gig_1991_film_101' },
      { id:'credit_c13_newyear', debtor:'副導', title:'賀歲片債權', status:'未收', redeemedBy:'ending_c13_newyear' }
    ],
    favorLedger: { settled:0, credits:4, exodus:[], counted:{}, __bf:1 } };
  ok('R2 favorLedgerCounts：2 筆已兌現唔計，creditsHeld＝2', favorLedgerCounts().creditsHeld===2);
  ok('R2 endingFavor410：creditsHeld＝2（鏡像一致）', endingFavor410(S).creditsHeld===2);
  ok('R2 heldList 唔含已兌現', endingFavor410(S).heldList.every(c=>!c.redeemedBy));
})();

/* ================================================================
   R1＋R2 混合：故事 1＋茶餐廳 2＋已兌現 1＋絕響 1 → creditsHeld＝1
   ================================================================ */
(function(){
  var S = null;
  eval(LEDGER_SRC);
  S = { dayIndex: 100, mockDebts: [],
    mockCredits: [
      { id:'credit_story_a', debtor:'甲', title:'故事債權一', status:'未收' },
      { id:'credit_enc79_cafe_help_10', debtor:'霞姐', title:'茶餐廳幫手', status:'未收' },
      { id:'credit_enc79_cafe_help_11', debtor:'霞姐', title:'茶餐廳幫手', status:'未收' },
      { id:'credit_br89_luk', debtor:'陸柏言', title:'引薦債權', status:'未收', redeemedBy:'gig_1991_film_101' },
      { id:'credit_fen_rescue', debtor:'副導演芬姐', title:'芬姐人情', status:'絕響' }
    ],
    favorLedger: { settled:0, credits:5, exodus:['credit_fen_rescue'], counted:{}, __bf:1 } };
  ok('R1＋R2 混合：creditsHeld＝1（只計故事未兌現）', favorLedgerCounts().creditsHeld===1 && endingFavor410(S).creditsHeld===1);
  ok('R1＋R2 混合：heldList 只有故事債權一', endingFavor410(S).heldList.length===1 && endingFavor410(S).heldList[0].id==='credit_story_a');
})();

/* ================================================================
   R3：settled 只計真係還清——勾銷／作廢／過期唔做一律唔計
   ================================================================ */
(function(){
  var S = null;
  eval(LEDGER_SRC);
  S = { dayIndex: 100, mockDebts: [], mockCredits: [],
    favorDueSettled:{}, mockSeasonCleared:{},
    favorLedger: { settled:0, credits:0, exodus:[], counted:{}, __bf:1 } };
  ok('R3 exodus_writeoff 拒絕：唔計、唔登記', favorLedgerNoteSettled('debt_fen_standin', 'exodus_writeoff')===false && S.favorLedger.settled===0 && !S.favorLedger.counted['debt_fen_standin']);
  ok('R3 wf3_harvest_expired 拒絕：唔計、唔登記', favorLedgerNoteSettled('debt_wf3_liao_grudge', 'wf3_harvest_expired')===false && S.favorLedger.settled===0 && !S.favorLedger.counted['debt_wf3_liao_grudge']);
  ok('R3 void_expired 拒絕：唔計、唔登記', favorLedgerNoteSettled('debt_ho_tutorial', 'void_expired')===false && S.favorLedger.settled===0 && !S.favorLedger.counted['debt_ho_tutorial']);
  ok('R3 拒絕後真還清照計（唔會鎖死）', favorLedgerNoteSettled('debt_fen_standin', 'repay_cash')===true && S.favorLedger.settled===1);
  ok('R3 repay_cash 計', favorLedgerNoteSettled('debt_a', 'repay_cash')===true && S.favorLedger.settled===2);
  ok('R3 repay_gift 計', favorLedgerNoteSettled('debt_b', 'repay_gift')===true && S.favorLedger.settled===3);
  ok('R3 repay_season 計', favorLedgerNoteSettled('card_x', 'repay_season')===true && S.favorLedger.settled===4);
  ok('R3 repaid_help 計', favorLedgerNoteSettled('debt_ho_tutorial', 'repaid_help')===true && S.favorLedger.settled===5);
  ok('R3 wf3_harvest 計', favorLedgerNoteSettled('debt_wf3_liao_grudge', 'wf3_harvest')===true && S.favorLedger.settled===6);
  ok('R3 closed_other（現金／禮物還教學債）計', favorLedgerNoteSettled('debt_ho_tutorial2', 'closed_other')===true && S.favorLedger.settled===7);
  ok('R3 同一筆唔雙計', favorLedgerNoteSettled('debt_a', 'repay_cash')===false && S.favorLedger.settled===7);
})();

/* ================================================================
   R4：人情頁分三組顯示（真 renderDebtPane；跟 weave42 段六同一沙盒）
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
  eval(extractConst('FAVOR_DUE_CFG').replace('const FAVOR_DUE_CFG', 'globalThis.__FDC259'));
  var FAVOR_DUE_CFG = globalThis.__FDC259;
  eval(extractConst('MOCK_DEBT_TUTORIAL').replace('const MOCK_DEBT_TUTORIAL', 'globalThis.__MDT259'));
  var MOCK_DEBT_TUTORIAL = globalThis.__MDT259;
  eval(extractConst('SEASON_COLLECT').replace('const SEASON_COLLECT', 'globalThis.__SC259'));
  var SEASON_COLLECT = globalThis.__SC259;
  eval(extractConst('DEBT_FUZZY').replace('const DEBT_FUZZY', 'globalThis.__DF259'));
  var DEBT_FUZZY = globalThis.__DF259;
  eval(extractConst('MOCK_EMPTY').replace('const MOCK_EMPTY', 'globalThis.__ME259'));
  var MOCK_EMPTY = globalThis.__ME259;
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
    mockDebts:[],
    mockCredits:[
      { id:'credit_story_a', debtor:'甲', title:'故事債權', line:'記住先。', status:'未收' },
      { id:'credit_enc79_cafe_help_10', debtor:'霞姐', title:'茶餐廳幫手', line:'幫手執漏。', status:'未收' },
      { id:'credit_br89_luk', debtor:'陸柏言', title:'引薦債權', line:'引薦。', status:'未收', redeemedBy:'gig_1991_film_101' },
      { id:'credit_fen_rescue', debtor:'副導演芬姐', title:'芬姐欠你嗰次救場', line:'清水灣外景嗰日亂到七彩。', status:'絕響' }
    ] };
  renderDebtPane();
  const h = box.innerHTML;
  const iStory = h.indexOf('故事債權'), iCafe = h.indexOf('茶餐廳幫手'), iRed = h.indexOf('已兌現');
  ok('R4 三組標題齊', iStory>=0 && iCafe>=0 && iRed>=0);
  ok('R4 組次序：故事 → 茶餐廳 → 已兌現', iStory < iCafe && iCafe < iRed);
  ok('R4 已兌現卡狀態寫「已兌現」', h.indexOf('>已兌現<')>=0);
  ok('R4 絕響卡仍灰階＋人已不在香港', h.indexOf('credit-row debt-exodus')>=0 && h.indexOf('人已不在香港')>=0);
  ok('R4 故事債權卡仍寫「未收」', h.indexOf('>未收<')>=0);
})();

/* ================================================================
   R4：結局頁分佈行（靜態核實——endingSummaryHtml410 含分佈行）
   ================================================================ */
(function(){
  ok('R4 結局頁：人情債權分佈行在位', html.indexOf('人情債權分佈：故事債權')>=0);
  ok('R4 結局頁：分佈行三組齊', html.indexOf('茶餐廳幫手')>=0 && html.indexOf('已兌現')>=0);
  ok('R4 守衛：exodus_writeoff／wf3_harvest_expired 拒絕集在位', html.indexOf('"exodus_writeoff"')>=0 && html.indexOf('"wf3_harvest_expired"')>=0);
})();

if(fails.length){ console.log('FAILURES: '+fails.join(' | ')); process.exit(1); }
console.log('ALL PASS');
