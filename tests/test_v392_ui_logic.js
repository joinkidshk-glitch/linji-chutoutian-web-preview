// v20a392 UI392 ②③・邏輯測試
//   行真碼：board392ExpDaily／board392Compare／confirmPlaceShoot；
//   modal 係 capture stub（唔經 DOM）。
//   反證：對 v391 index 行 → board392ExpDaily／confirmPlaceShoot 嘅新分支抽唔到／
//   confirmPlaceShoot 仍有三掣＋onDismiss → FAIL。
// 用法：node tests/test_v392_ui_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }
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

/* ---- stubs ---- */
var modalCalls = [];
var placedCalls = [];
var sortFallbackCalls = 0;
function reset(){ modalCalls = []; placedCalls = []; sortFallbackCalls = 0; }
function modal(htmlArg, btns, opts){ modalCalls.push({ html: htmlArg, btns: btns || [], opts: opts }); return true; }
function gigPayExact(g){ return (g && g._pay != null) ? g._pay : null; }
function chance(g){ return (g && g._ch != null) ? g._ch : 0; }
function effectiveShootDays(g){ return (g && g._days != null) ? g._days : 1; }
function boardSortCompare(a, b){ sortFallbackCalls++; return String(a.id||'').localeCompare(String(b.id||'')); }
function previewShootPlacement(shoot, fromWeekday){ return shoot._prev; }
function placeShootOnPlan(shoot, fromWeekday, overwrite){ placedCalls.push({ shoot, fromWeekday, overwrite: !!overwrite }); }
function labels(btns){ return (btns || []).map(b => b.label); }
function findBtn(btns, sub){ return (btns || []).find(b => String(b.label || '').indexOf(sub) >= 0); }
function press(call, substr){
  const b = findBtn(call.btns, substr);
  if(!b) throw new Error('button not found: ' + substr + ' in [' + labels(call.btns).join(',') + ']');
  b.on();
}

eval(extractFn('board392ExpDaily'));
eval(extractFn('board392Compare'));
eval(extractFn('weekdayName'));
eval(extractFn('confirmPlaceShoot'));

/* ---- (3) 預期日薪排序 ---- */
(function(){
  reset();
  const A = { id: 'gA', _pay: 1000, _ch: 0.9, _days: 2 };   // 450
  const B = { id: 'gB', _pay: 600, _ch: 0.5, _days: 1 };    // 300
  const C = { id: 'gC', _pay: 378, _ch: 0.86, _days: 3 };   // 108.36
  ok('3 expDaily A=450 B=300 C~108.36',
    board392ExpDaily(A) === 450 && board392ExpDaily(B) === 300
    && Math.abs(board392ExpDaily(C) - 108.36) < 0.01);
  ok('3 expDaily pay null → 0', board392ExpDaily({ id: 'gX', _pay: null, _ch: 0.9, _days: 2 }) === 0);
  ok('3 expDaily days 0 → 當 1 日', board392ExpDaily({ id: 'gY', _pay: 100, _ch: 1, _days: 0 }) === 100);
  const sorted = [C, A, B].sort((a, b) => board392Compare(a, b, 'exp'));
  ok('3 預設按預期日薪降（A＞B＞C）', sorted[0] === A && sorted[1] === B && sorted[2] === C);
  const byPay = [C, B].sort((a, b) => board392Compare(a, b, 'pay'));
  ok('3 切總片酬：B(600)＞C(378)', byPay[0] === B);
  const byChance = [C, A].sort((a, b) => board392Compare(a, b, 'chance'));
  ok('3 切成功率：A(90%)＞C(86%)', byChance[0] === A);
  // 預期日薪打和 → 跌返 boardSortCompare（tiebreak）
  const D = { id: 'gD', _pay: 200, _ch: 0.5, _days: 1 };    // 100
  const E = { id: 'gE', _pay: 100, _ch: 1, _days: 1 };      // 100
  sortFallbackCalls = 0;
  const tie = [E, D].sort((a, b) => board392Compare(a, b, 'exp'));
  ok('3 打和跌返 boardSortCompare（id 次序）', sortFallbackCalls > 0 && tie[0] === D && tie[1] === E);
})();

/* ---- (2) confirmPlaceShoot：無衝突即排；有衝突兩掣＋無 onDismiss ---- */
(function(){
  reset();
  let thenCalls = 0;
  const shoot = { id: 'sh1', _prev: { displaced: [], freeCount: 3 } };
  confirmPlaceShoot(shoot, 2, () => { thenCalls++; });
  ok('2 無衝突：唔彈 modal 即排（overwrite=false）＋行 thenFn',
    modalCalls.length === 0 && placedCalls.length === 1 && placedCalls[0].overwrite === false && thenCalls === 1);
})();
(function(){
  reset();
  let thenCalls = 0;
  const shoot = { id: 'sh2', _prev: { displaced: [{ wd: 3, name: '休息' }, { wd: 4, name: '咖啡店演出' }], freeCount: 1 } };
  confirmPlaceShoot(shoot, 2, () => { thenCalls++; });
  ok('2 有衝突：彈一個 modal', modalCalls.length === 1);
  const m = modalCalls[0];
  ok('2 modal 只有兩掣（無獨立「取消」）', m.btns.length === 2);
  ok('2 有空日：主掣係「只排空日」（role p）',
    m.btns[0].label === '只排空日' && m.btns[0].role === 'p');
  ok('2 次級掣係「取消原安排並拍攝」（role g，唔係金色）',
    m.btns[1].label === '取消原安排並拍攝' && m.btns[1].role === 'g');
  ok('2 警告講明損失（會取消週四休息同週五咖啡店演出，兩日改為拍攝）',
    m.html.indexOf('會取消') >= 0 && m.html.indexOf('週四（休息）') >= 0
    && m.html.indexOf('週五（咖啡店演出）') >= 0 && m.html.indexOf('兩日改為拍攝') >= 0);
  ok('2 冇「取消＝只排入空日」細字', m.html.indexOf('取消＝只排入空日') < 0);
  ok('2 無 onDismiss（撳遮罩只收起，唔排位唔行 thenFn）',
    m.opts == null || m.opts.onDismiss == null);
  press(m, '只排空日');
  ok('2 撳「只排空日」：排空日（overwrite=false）＋行 thenFn',
    placedCalls.length === 1 && placedCalls[0].overwrite === false && thenCalls === 1);
})();
(function(){
  reset();
  let thenCalls = 0;
  const shoot = { id: 'sh3', _prev: { displaced: [{ wd: 3, name: '休息' }, { wd: 4, name: '咖啡店演出' }], freeCount: 1 } };
  confirmPlaceShoot(shoot, 2, () => { thenCalls++; });
  press(modalCalls[0], '取消原安排並拍攝');
  ok('2 撳「取消原安排並拍攝」：覆寫（overwrite=true）＋行 thenFn',
    placedCalls.length === 1 && placedCalls[0].overwrite === true && thenCalls === 1);
})();
(function(){
  reset();
  let thenCalls = 0;
  const shoot = { id: 'sh4', _prev: { displaced: [{ wd: 5, name: '訓練' }], freeCount: 0 } };
  confirmPlaceShoot(shoot, 2, () => { thenCalls++; });
  const m = modalCalls[0];
  ok('2 冇空日：主掣係「留待下週」', m.btns[0].label === '留待下週' && m.btns[0].role === 'p');
  ok('2 冇空日：首行講明本週已經冇空日', m.html.indexOf('本週已經冇空日') >= 0);
  ok('2 單日衝突：寫「1日改為拍攝」', m.html.indexOf('1日改為拍攝') >= 0);
  press(m, '留待下週');
  ok('2 撳「留待下週」：唔排位（唔郁 weekPlan／daysLeft）、記 defer 旗、照行 thenFn',
    placedCalls.length === 0 && shoot._v392defer === true && thenCalls === 1);
})();

console.log(fails.length ? ('\nFAILURES: ' + fails.length + ' -> ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
