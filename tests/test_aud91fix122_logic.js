// v20a122 AUD91FIX 邏輯測試：H1 晨報 _paperShowing 旗卡死、H2 拍攝排程 modal 遮罩點走。
//   H1 (a) 旗卡死＋冇報紙到期 → presentDueMorningPaper 唔再靜默 return true：清旗＋return false，
//         等 goToMapForBrowse／runScheduleFromToday 條鏈繼續行 aud91。
//   H1 (b) 旗卡死＋有報紙到期 → 照常出晨報 modal（return true），dismiss 後清旗＋cont 照行。
//   H1 (c) 正常路徑不變：旗 false＋有報紙 → 出 modal；旗 false＋冇報紙 → return false。
//   H1 (d) closeModal() 保底清旗：任何關 modal 嘅路都清 _paperShowing。
//   H2 (a) confirmPlaceShoot 要佔用日子嗰陣，modal 呼叫唔帶 onDismiss（v392：
//         撳遮罩只收起 modal，唔排位、唔行 thenFn）。
//   H2 (b) 安全掣分流：有空日「只排空日」go(false)；冇空日「留待下週」defer
//         （唔排位、記 _v392defer 旗、thenFn 照行）；覆寫掣「取消原安排並拍攝」go(true)。
//   H2 (c) 唔使佔用日子嗰陣照舊即刻 go(false)，唔彈 modal。
// 反證：pristine main（v121）跑呢檔要 FAIL——舊 early-return 會 return true、
//   confirmPlaceShoot 冇 onDismiss（modal stub 收到 opts.onDismiss === undefined）。
// 用法：node tests/test_aud91fix122_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = 0;
function ok(name, cond, extra){
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : ''));
  if(!cond) fails++;
}
function extractFn(name){
  const i = html.indexOf('function ' + name + '(');
  if(i < 0) throw new Error('fn not found: ' + name);
  let depth = 0, j = html.indexOf('{', i);
  for(; j < html.length; j++){
    if(html[j] === '{') depth++;
    else if(html[j] === '}'){ depth--; if(depth === 0) break; }
  }
  return html.slice(i, j + 1);
}

/* ---------- 沙盒 ---------- */
var S = { dayIndex: 0 };
var FREEPLAY_FW = { _paperShowing: false };
var _tut = null;
var __modals = [];
var __commitCount = 0;
var __holdToday = false;
var __editionDue = null;
function flushPendingStoryPapers(){}
function newspaperHoldForToday(){ return __holdToday; }
function pullDueNewspaperEdition(){ return __editionDue; }
function commitMorningPaper(){ __commitCount++; }
function renderMorningPaperHtml(){ return '<h3>晨報</h3>'; }
var modal = function(body, btns, opts){
  __modals.push({ body: String(body || ''), btns: btns || [], opts: opts || {} });
};
function makeEl(){
  return { innerHTML:'', textContent:'', style:{},
    classList:{ add(){}, remove(){}, toggle(){}, contains(){ return false; } },
    setAttribute(){}, appendChild(){}, querySelector(){ return makeEl(); }, querySelectorAll(){ return []; } };
}
var __els = {};
var document = {
  getElementById(id){ return __els[id] || (__els[id] = makeEl()); },
  querySelector(){ return makeEl(); }, querySelectorAll(){ return []; },
  createElement(){ return makeEl(); }, body: makeEl(), addEventListener(){},
};
function setStoryPlayLock(){}
function setTutMask(){}
function setUnderlyingInert(){}
function stopActFx102(){}
function clearTutSpotlight(){}
function restoreMapScroll(){}
function ensureLocSheetInteractive(){}
function weekdayName(wd){ return ['日','一','二','三','四','五','六'][wd]; }
/* confirmPlaceShoot 嘅兩個下游用 stub（行為本身已有 test_aud91 覆蓋，呢度只驗 onDismiss 接線） */
var __placed = [];
var __previewDisplaced = [];
var __previewFreeCount = 0;
function previewShootPlacement(){ return { displaced: __previewDisplaced, freeCount: __previewFreeCount }; }
function placeShootOnPlan(shoot, wd, overwrite){ __placed.push({ shoot: shoot, wd: wd, overwrite: !!overwrite }); }

eval(extractFn('presentDueMorningPaper'));
eval(extractFn('closeModal'));
eval(extractFn('confirmPlaceShoot'));
ok('harness: 函數全載入', typeof presentDueMorningPaper === 'function' && typeof closeModal === 'function' && typeof confirmPlaceShoot === 'function');

/* ---------- H1 (a) 旗卡死＋冇報紙到期 ---------- */
(function(){
  S = { dayIndex: 1 };
  FREEPLAY_FW._paperShowing = true; /* 模擬卡死 */
  __holdToday = false; __editionDue = null; __modals = [];
  let cont = false;
  const ret = presentDueMorningPaper(()=>{ cont = true; });
  ok('H1a 旗卡死＋冇報紙到期：唔再靜默 return true', ret === false);
  ok('H1a 旗卡死＋冇報紙到期：旗已清', FREEPLAY_FW._paperShowing === false);
  ok('H1a 旗卡死＋冇報紙到期：冇彈 modal', __modals.length === 0);
  ok('H1a 旗卡死＋冇報紙到期：cont 未行（等上游鏈行 aud91）', cont === false);
})();

/* ---------- H1 (a2) 旗卡死＋今日 hold 紙 ---------- */
(function(){
  FREEPLAY_FW._paperShowing = true;
  __holdToday = true; __editionDue = { headline: 'x' }; __modals = [];
  const ret = presentDueMorningPaper(()=>{});
  ok('H1a2 旗卡死＋hold：清旗＋return false', ret === false && FREEPLAY_FW._paperShowing === false && __modals.length === 0);
  __holdToday = false;
})();

/* ---------- H1 (b) 旗卡死＋有報紙到期 ---------- */
(function(){
  FREEPLAY_FW._paperShowing = true;
  __editionDue = { headline: '晨報' }; __modals = []; __commitCount = 0;
  let cont = false;
  const ret = presentDueMorningPaper(()=>{ cont = true; });
  ok('H1b 旗卡死＋有報紙：照常出晨報 modal（return true）', ret === true && __modals.length === 1);
  ok('H1b 晨報 modal 有 onDismiss（掣／遮罩都清旗）', __modals[0] && typeof __modals[0].opts.onDismiss === 'function');
  if(__modals[0] && typeof __modals[0].opts.onDismiss === 'function') __modals[0].opts.onDismiss(); /* 模擬 dismiss */
  else ok('H1b dismiss 後旗清＋cont 照行＋commit 行過', false, '冇 modal onDismiss 可行');
  if(__modals[0] && typeof __modals[0].opts.onDismiss === 'function')
    ok('H1b dismiss 後旗清＋cont 照行＋commit 行過', FREEPLAY_FW._paperShowing === false && cont === true && __commitCount === 1);
})();

/* ---------- H1 (c) 正常路徑不變 ---------- */
(function(){
  FREEPLAY_FW._paperShowing = false;
  __editionDue = { headline: '晨報' }; __modals = [];
  let cont = false;
  ok('H1c 正常＋有報紙：出 modal return true', presentDueMorningPaper(()=>{ cont = true; }) === true && __modals.length === 1);
  if(__modals[0] && typeof __modals[0].opts.onDismiss === 'function') __modals[0].opts.onDismiss();
  ok('H1c 正常 dismiss 後 cont 照行', cont === true);
  FREEPLAY_FW._paperShowing = false;
  __editionDue = null; __modals = [];
  ok('H1c 正常＋冇報紙：return false 唔彈 modal', presentDueMorningPaper(()=>{}) === false && __modals.length === 0);
})();

/* ---------- H1 (d) closeModal 保底清旗 ---------- */
(function(){
  FREEPLAY_FW._paperShowing = true;
  let threw = false;
  try{ closeModal(); }catch(_e){ threw = true; }
  ok('H1d closeModal() 清 _paperShowing', !threw && FREEPLAY_FW._paperShowing === false);
})();

/* ---------- H2 (v392) ---------- */
(function(){
  const shoot = { id: 'sh_test' };
  /* (a) 有空日＋要佔用日子 → 彈 modal、唔帶 onDismiss；安全掣係「只排空日」 */
  __previewDisplaced = [{ wd: 1, name: '街頭表演' }];
  __previewFreeCount = 2;
  __placed = []; __modals = [];
  let thenCalled = false;
  confirmPlaceShoot(shoot, 1, ()=>{ thenCalled = true; });
  ok('H2a 要佔用日子：彈拍攝排程 modal', __modals.length === 1 && __modals[0].body.indexOf('拍攝排程') >= 0);
  ok('H2a 排程 modal 唔帶 onDismiss（v392：遮罩只收起 modal）', __modals[0] && typeof __modals[0].opts.onDismiss === 'undefined');
  ok('H2a 有空日：安全掣係「只排空日」（金色主掣）', __modals[0] && __modals[0].btns.some(b => b.label === '只排空日' && b.role === 'p'));
  ok('H2a 「取消」掣已刪、「確定佔用」已改名「取消原安排並拍攝」',
    __modals[0] && !__modals[0].btns.some(b => b.label === '取消' || b.label === '確定佔用')
    && __modals[0].btns.some(b => b.label === '取消原安排並拍攝'));
  /* (b) 遮罩點走＝乜都唔做：冇 onDismiss 可行，唔排位、thenFn 唔行 */
  ok('H2b 遮罩點走：唔排位、thenFn 唔行（冇 onDismiss）', __placed.length === 0 && thenCalled === false);
  /* 「只排空日」掣：go(false)＋thenFn */
  const freeBtn = __modals[0].btns.find(b => b.label === '只排空日');
  __placed = []; thenCalled = false;
  freeBtn.on();
  ok('H2b 對照：「只排空日」掣 go(false)＋thenFn', __placed.length === 1 && __placed[0].overwrite === false && thenCalled === true);
  /* (c) 冇空日 → 安全掣變「留待下週」：defer，唔排位、記旗、thenFn 照行 */
  __previewDisplaced = [{ wd: 1, name: '街頭表演' }];
  __previewFreeCount = 0;
  __placed = []; __modals = []; thenCalled = false;
  const shoot2 = { id: 'sh_test2' };
  confirmPlaceShoot(shoot2, 1, ()=>{ thenCalled = true; });
  ok('H2c 冇空日：安全掣係「留待下週」', __modals[0] && __modals[0].btns.some(b => b.label === '留待下週' && b.role === 'p'));
  const deferBtn = __modals[0].btns.find(b => b.label === '留待下週');
  deferBtn.on();
  ok('H2c 「留待下週」：唔排位、記 _v392defer 旗、thenFn 照行', __placed.length === 0 && shoot2._v392defer === true && thenCalled === true);
  /* 覆寫掣對照：go(true)＋thenFn */
  const owBtn = __modals[0].btns.find(b => b.label === '取消原安排並拍攝');
  __placed = []; thenCalled = false;
  owBtn.on();
  ok('H2c 對照：「取消原安排並拍攝」掣 go(true)＋thenFn', __placed.length === 1 && __placed[0].overwrite === true && thenCalled === true);
  /* (d) 唔使佔用日子 → 即刻 go(false)，唔彈 modal */
  __previewDisplaced = [];
  __placed = []; __modals = []; thenCalled = false;
  confirmPlaceShoot(shoot, 1, ()=>{ thenCalled = true; });
  ok('H2d 唔使佔用：唔彈 modal、即刻 go(false)＋thenFn', __modals.length === 0 && __placed.length === 1 && __placed[0].overwrite === false && thenCalled === true);
})();

console.log('\nAUD91FIX122 LOGIC: ' + (fails ? fails + ' FAIL' : 'ALL PASS'));
process.exit(fails ? 1 : 0);
