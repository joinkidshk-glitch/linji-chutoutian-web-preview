// Weave Phase 4-4（v20a27）邏輯測試：鏈 G 第 2 拍——報紙首次點名 → 屋企回音
// 跟 v20a22 教訓：偵測行真 commitMorningPaper、渲染行真 renderDebtPane、屋企債行真 ensureFamilyHomeDebt 播種；
// 唔直接寫 echoNote／paperTier 扮觸發（狀態一律經真 commit 路徑產生）。
// 另含 4-3 覆檢跟進：屋企卡顯示排序（只改顯示、唔郁 S.mockDebts 數據次序）。
// 用法：node tests/test_weave44_logic.js [path-to-index.html]
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
const TIER_SRC = [
  extractConst('PAPER_NAME_TIER_NAMED'), extractConst('PAPER_NAME_TIER_TITLED'),
  extractFn('newspaperNameTier')
].join('\n')
 .replace(/const PAPER_NAME_TIER_NAMED/g, 'var PAPER_NAME_NAMED')
 .replace(/const PAPER_NAME_TIER_TITLED/g, 'var PAPER_NAME_TITLED')
 .replace(/PAPER_NAME_TIER_NAMED/g, 'PAPER_NAME_NAMED').replace(/PAPER_NAME_TIER_TITLED/g, 'PAPER_NAME_TITLED');

/* 共用 commit 環境（段一至段三）：真 commitMorningPaper＋真 tick；toast 記錄、saveQ／傳聞 stub */
function commitEnv(){
  var env = {};
  env.toastCalls = [];
  env.toast = (m, opts)=>{ env.toastCalls.push({ m:String(m), sub:(opts && opts.sub) ? String(opts.sub) : '' }); };
  env.document = { getElementById: ()=> null };
  env.saveQ = ()=>{};
  env.syncNotebookMirror = ()=>{};
  env.pushNewspaperRumor = ()=>{};
  env.S = null;
  return env;
}
function evalCommitStack(env){
  // 將 env 嘅 stub 綁入呢個 eval 作用域
  var toast = env.toast, document = env.document, saveQ = env.saveQ,
      syncNotebookMirror = env.syncNotebookMirror, pushNewspaperRumor = env.pushNewspaperRumor;
  var S = null;
  eval(TIER_SRC);
  eval(FAM_SRC);
  eval(extractFn('ensureNewspaperClippings'));
  eval(extractFn('commitMorningPaper'));
  return {
    setS(s){ S = s; env.S = s; },
    getS(){ return S; },
    commit(ed){ commitMorningPaper(ed); },
    tick(){ return familyPaperEchoTick(); }
  };
}
let paperSeq = 0;
function mkPaper(fameDelta){
  paperSeq++;
  return { id:'paper_t'+paperSeq, fameDelta: fameDelta||0, paperName:'娛樂快報',
           headline:'測試標題'+paperSeq, dek:'測試一行', dateLabel:'1988年3月8日' };
}
function baseSave(fame){
  return { dayIndex:10, fame:fame, newspaperClippings:[], mockDebts:[], mockRumors:[], mockCredits:[] };
}

/* ================================================================
   段一：首次觀察只初始化、永不觸發——anon／named／titled 三種舊檔形狀各一
   ================================================================ */
(function(){
  const env = commitEnv();
  const api = evalCommitStack(env);

  api.setS(baseSave(5));
  api.commit(mkPaper(0));
  ok('init anon: tier recorded, no echo, no toast',
     api.getS().familyHome.paperTier==='anon' && api.getS().familyHome.echoNote==='' && env.toastCalls.length===0);

  api.setS(baseSave(20));
  api.commit(mkPaper(0));
  ok('init named (old save already famous): NO retro trigger',
     api.getS().familyHome.paperTier==='named' && api.getS().familyHome.echoNote==='' && env.toastCalls.length===0);

  api.setS(baseSave(50));
  api.commit(mkPaper(0));
  ok('init titled (old save already titled): NO retro trigger',
     api.getS().familyHome.paperTier==='titled' && api.getS().familyHome.echoNote==='' && env.toastCalls.length===0);
})();

/* ================================================================
   段二：anon→named 嗰期觸發一次（包括靠嗰期 fameDelta 推過門檻），之後唔重複
   ================================================================ */
(function(){
  const env = commitEnv();
  const api = evalCommitStack(env);

  api.setS(baseSave(5));
  api.commit(mkPaper(0));                       // 初始化 anon
  api.commit(mkPaper(0));                       // anon→anon：唔觸發
  ok('anon->anon: still no echo', api.getS().familyHome.echoNote==='' && env.toastCalls.length===0);

  api.getS().fame = 14;                          // 門檻邊緣（named=15）
  api.commit(mkPaper(2));                        // 嗰期 +2 → 16，跨入 named
  const S = api.getS();
  ok('crossing paper: fame applied then echo fired', S.fame===16 && S.familyHome.echoNote.length>0);
  ok('echo note = clipping copy (較剪／電話簿)', S.familyHome.echoNote.indexOf('較剪')>=0 && S.familyHome.echoNote.indexOf('電話簿')>=0);
  ok('echo day recorded', S.familyHome.echoDay===10 && S.familyHome.paperTier==='named');
  ok('toast: exactly one, two-part (main + sub)', env.toastCalls.length===1 && env.toastCalls[0].m.length>0 && env.toastCalls[0].sub.length>0);
  ok('toast main = 茶餐廳留言', env.toastCalls[0].m.indexOf('茶餐廳伙記轉告')>=0 && env.toastCalls[0].m.indexOf('報紙見到你個名')>=0);
  ok('toast sub: 囑食飯＋剪報頁提示', env.toastCalls[0].sub.indexOf('記得食飯')>=0 && env.toastCalls[0].sub.indexOf('剪報頁')>=0);
  ok('crossing edition landed in clippings', (S.newspaperClippings||[]).length===3);

  api.commit(mkPaper(0));                        // 再出報紙：唔重複
  api.getS().fame = 45; api.commit(mkPaper(0));  // 之後再升 titled：都唔再觸發
  ok('no re-fire on later papers / later titled', env.toastCalls.length===1 && api.tick()===false);
})();

/* ================================================================
   段三：anon→titled 直跳觸發；named→titled 唔觸發（唔係首次跨級）
   ================================================================ */
(function(){
  const env = commitEnv();
  const api = evalCommitStack(env);

  api.setS(baseSave(5));
  api.commit(mkPaper(0));
  api.getS().fame = 45;
  api.commit(mkPaper(0));
  ok('anon->titled direct jump: fires', api.getS().familyHome.echoNote.length>0 && env.toastCalls.length===1);

  const env2 = commitEnv();
  const api2 = evalCommitStack(env2);
  api2.setS(baseSave(5));
  api2.commit(mkPaper(0));                       // init anon（paperTier 由真 commit 記低）
  api2.getS().fame = 20;
  api2.commit(mkPaper(0));                       // anon→named 先觸發（基準）
  ok('setup: anon->named fired once', env2.toastCalls.length===1);
  // 另一個存檔形狀：paperTier 已係 named（初始化嗰期已 named）→ 之後升 titled 唔觸發
  const env3 = commitEnv();
  const api3 = evalCommitStack(env3);
  api3.setS(baseSave(20));
  api3.commit(mkPaper(0));                       // init named
  api3.getS().fame = 45;
  api3.commit(mkPaper(0));                       // named→titled
  ok('named->titled: NOT a first crossing, no echo', api3.getS().familyHome.echoNote==='' && env3.toastCalls.length===0);
})();

/* ================================================================
   段四：真 renderDebtPane——觸發前無回音字條；觸發後屋企卡常駐回音字條（態度字條之後）
   ================================================================ */
(function(){
  var box = { innerHTML:'', onclick:null };
  var document = { getElementById: (id)=> id==='debt-list' ? box : null };
  var ensureMockJournal = ()=>{};
  var ensureWeakSeals = ()=>{};
  var softPreviewOn = ()=> true;
  var syncNotebookMirror = ()=>{};
  var calendarSeason = ()=>'春';
  var saveQ = ()=>{};
  var pushNewspaperRumor = ()=>{};
  var toastCalls = [];
  var toast = (m, opts)=>{ toastCalls.push({ m:String(m), sub:(opts && opts.sub) ? String(opts.sub) : '' }); };
  var S = null;
  eval(extractConst('START').replace('const START', 'globalThis.__START44'));
  var START = globalThis.__START44;
  eval(extractConst('FAVOR_DUE_CFG').replace('const FAVOR_DUE_CFG', 'globalThis.__FDC44'));
  var FAVOR_DUE_CFG = globalThis.__FDC44;
  eval(extractConst('MOCK_DEBT_TUTORIAL').replace('const MOCK_DEBT_TUTORIAL', 'globalThis.__MDT44'));
  var MOCK_DEBT_TUTORIAL = globalThis.__MDT44;
  eval(extractConst('SEASON_COLLECT').replace('const SEASON_COLLECT', 'globalThis.__SC44'));
  var SEASON_COLLECT = globalThis.__SC44;
  eval(extractConst('DEBT_FUZZY').replace('const DEBT_FUZZY', 'globalThis.__DF44'));
  var DEBT_FUZZY = globalThis.__DF44;
  eval(extractConst('MOCK_EMPTY').replace('const MOCK_EMPTY', 'globalThis.__ME44'));
  var MOCK_EMPTY = globalThis.__ME44;
  eval(TIER_SRC);
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
  eval(FAM_SRC);
  eval(extractFn('ensureNewspaperClippings'));
  eval(extractFn('commitMorningPaper'));
  eval(extractFn('renderDebtPane'));

  function famCard(htmlStr){
    const i = htmlStr.indexOf('data-debt-id="debt_family_home"');
    if(i<0) return '';
    const j = htmlStr.indexOf('</article>', i);
    return htmlStr.slice(i, j<0?htmlStr.length:j);
  }

  S = { dayIndex:5, fame:5, npcs:{},
    favorDueSettled:{ debt_ho_tutorial:{ result:'repaid_help', day:1 } },
    mockSeasonCleared:{}, mockDebts:[], mockCredits:[], newspaperClippings:[] };
  ensureFamilyHomeDebt(); // 真播種屋企債
  commitMorningPaper(mkPaper(0)); // 第一期：初始化 anon，唔觸發
  renderDebtPane();
  ok('before echo: family card has attitude note', famCard(box.innerHTML).indexOf('family-attitude')>=0);
  ok('before echo: NO echo note anywhere', box.innerHTML.indexOf('family-echo')<0 && box.innerHTML.indexOf('較剪')<0);

  S.fame = 20;
  commitMorningPaper(mkPaper(0)); // 跨級嗰期：真觸發
  ok('echo fired through real commit', S.familyHome.echoNote.length>0 && toastCalls.length===1);
  renderDebtPane();
  const card = famCard(box.innerHTML);
  ok('after echo: note inside family card (family-echo class)', card.indexOf('family-echo')>=0);
  ok('after echo: note copy = 阿媽剪報紙', card.indexOf('阿媽將嗰版寫住你名嘅報紙剪咗落嚟')>=0);
  ok('after echo: echo note AFTER attitude note in same card',
     card.indexOf('family-attitude')>=0 && card.indexOf('family-echo') > card.indexOf('family-attitude'));
  renderDebtPane();
  ok('after echo: note is resident (still there on re-render)', famCard(box.innerHTML).indexOf('family-echo')>=0);
})();

/* ================================================================
   段五（4-3 覆檢跟進）：顯示排序——新檔形狀（春季季節卡 2 張＋債 3 筆，屋企債數據排中間）
   屋企卡係輸出第一張；其餘債相對次序不變；S.mockDebts 數據次序冇俾改到
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
  eval(extractConst('START').replace('const START', 'globalThis.__START45'));
  var START = globalThis.__START45;
  eval(extractConst('FAVOR_DUE_CFG').replace('const FAVOR_DUE_CFG', 'globalThis.__FDC45'));
  var FAVOR_DUE_CFG = globalThis.__FDC45;
  eval(extractConst('MOCK_DEBT_TUTORIAL').replace('const MOCK_DEBT_TUTORIAL', 'globalThis.__MDT45'));
  var MOCK_DEBT_TUTORIAL = globalThis.__MDT45;
  eval(extractConst('SEASON_COLLECT').replace('const SEASON_COLLECT', 'globalThis.__SC45'));
  var SEASON_COLLECT = globalThis.__SC45;
  eval(extractConst('DEBT_FUZZY').replace('const DEBT_FUZZY', 'globalThis.__DF45'));
  var DEBT_FUZZY = globalThis.__DF45;
  eval(extractConst('MOCK_EMPTY').replace('const MOCK_EMPTY', 'globalThis.__ME45'));
  var MOCK_EMPTY = globalThis.__ME45;
  eval(TIER_SRC);
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
  eval(FAM_SRC);
  eval(extractFn('renderDebtPane'));

  const circle1 = { id:'debt_circle_a', creditor:'何生', title:'何生人情數', weight:'重', season:'', status:'未到期', amount:300 };
  const circle2 = { id:'debt_circle_b', creditor:'道具組老張', title:'老張人情數', weight:'中', season:'', status:'未到期' };
  S = { dayIndex:5, fame:5, npcs:{},
    favorDueSettled:{ debt_ho_tutorial:{ result:'repaid_help', day:1 } },
    mockSeasonCleared:{}, mockDebts:[circle1], mockCredits:[] };
  ensureFamilyHomeDebt();              // 真播種：數據次序 [circle_a, family]
  S.mockDebts.push(circle2);           // 數據次序 [circle_a, family, circle_b]
  const dataOrderBefore = S.mockDebts.map(d=>d.id).join(',');
  renderDebtPane();
  const out = box.innerHTML;

  ok('spring season cards present (live-check shape)', out.indexOf('何生春季數')>=0 && out.indexOf('老張開春器材數')>=0);
  const firstArticle = out.indexOf('<article');
  ok('family card is the FIRST card in output',
     firstArticle>=0 && out.slice(firstArticle, firstArticle+200).indexOf('data-debt-id="debt_family_home"')>=0);
  ok('family card before season cards', out.indexOf('data-debt-id="debt_family_home"') < out.indexOf('何生春季數'));
  ok('other debts keep relative order (a before b)',
     out.indexOf('data-debt-id="debt_circle_a"')>=0 &&
     out.indexOf('data-debt-id="debt_circle_a"') < out.indexOf('data-debt-id="debt_circle_b"'));
  ok('season cards keep relative order （何生 before 老張）',
     out.indexOf('何生春季數') < out.indexOf('老張開春器材數'));
  ok('S.mockDebts data order untouched by render', S.mockDebts.map(d=>d.id).join(',')===dataOrderBefore);
})();

console.log(fails.length ? ('\nFAILED: '+fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length?1:0);
