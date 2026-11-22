// v20a386 第七輪評估修正・邏輯測試
// 合約：
//   A 執行層休息覆寫（P2-6）：placeShootOnPlan pass2＋previewShootPlacement 先覆寫非休息格，休息格最後。
//   B 峰值預覽計入已 lock 拍攝（P2-7）：defaultWeekPlan 預覽用 lock 後計劃，拍攝 +10/日入峰值；
//     預覽唔留 daysLeft 副作用。
//   C BE 抉擇覆蓋 commit（P2-5）：endingRomance410 committed 喺 BE 旗已立時為 false。
//   D 補位失效來源（P2-3）：intel381Tick 失效時寫 expiredFrom（msg／kept）。
// 反證：v385 index 冇上述改動 → 相關斷言 FAIL。
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
function extractFn(name){
  const i = html.indexOf('function ' + name + '(');
  if (i < 0) throw new Error('fn not found: ' + name);
  let depth = 0, j = html.indexOf('{', i);
  for (; j < html.length; j++){ if (html[j] === '{') depth++; else if (html[j] === '}'){ depth--; if (depth === 0) break; } }
  return html.slice(i, j + 1);
}
let fails = 0;
function ok(name, cond, extra){
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : ''));
  if (!cond) fails++;
}

/* ---------- 沙盒 ---------- */
var S = { dayIndex: 0, stress: 0, weekPlan: null, shoots: [], flags: {}, story: { done: {}, rel: {} }, intel381: null, pendingAud: [] };
var clamp = (v, a, b) => Math.max(a, Math.min(b, v));
var weekdayName = (i) => ['一','二','三','四','五','六','日'][i] || '';
var planMeta = (id) => ({ name: String(id || '') });
var shootRemain = (sh) => Math.max(0, (sh.totalDays || 0) - (sh.doneDays || 0));
var shootWeekdayOk = () => true;
var stampWeekPlan37 = () => {};
var scrubStaleJobs = (d) => d;
var weekNumNow = () => 5;
var toast = () => {};
var saveQ = () => {};
eval([
  extractFn('isMapDay'),
  extractFn('isFreePlanSlot'),
  extractFn('previewShootPlacement'),
  extractFn('placeShootOnPlan'),
  extractFn('lockShootsIntoDraft'),
  extractFn('stressDeltaForAct'),
  extractFn('previewWeekStress'),
  extractFn('defaultWeekPlan'),
  extractFn('endingFlag410'),
  extractFn('endingRomance410'),
  extractFn('intel381Slot'),
  extractFn('intel381Tick'),
].join('\n'));

/* ---------- A 執行層休息覆寫 ---------- */
// 計劃：週一 scout（free）、週二 rest、週三 train（busy 非休息）、週四 scout、週五 rest、週六 cafe、週日 rest
// 新拍攝 need=3：free 位得週一/週四（2），要覆寫 1 格 → 應覆寫週三 train，唔好覆寫週二 rest。
S.weekPlan = ['scout_all', 'rest', 'train_acting', 'scout_all', 'rest', 'cafe_gig', 'rest'];
const shA = { id: 'shA', totalDays: 3, doneDays: 0, daysLeft: 3 };
const pvA = previewShootPlacement(shA, 0);
ok('A preview displaced 先非休息', pvA.displaced.length === 1 && pvA.displaced[0].id === 'train_acting', JSON.stringify(pvA.displaced));
const planA = placeShootOnPlan(shA, 0, true);
ok('A 週二休息保留', planA[1] === 'rest', JSON.stringify(planA));
ok('A 週三被覆寫', planA[2] === 'shoot:shA', JSON.stringify(planA));
// need=5：free 2＋非休息 busy 2（train/cafe）＝4，仲差 1 → 先至覆寫休息（週二）
S.weekPlan = ['scout_all', 'rest', 'train_acting', 'scout_all', 'rest', 'cafe_gig', 'rest'];
const shA2 = { id: 'shA2', totalDays: 5, doneDays: 0, daysLeft: 5 };
const planA2 = placeShootOnPlan(shA2, 0, true);
ok('A 唔夠位先覆寫休息', planA2[1] === 'shoot:shA2' && planA2[4] === 'rest' && planA2[6] === 'rest', JSON.stringify(planA2));

/* ---------- B 峰值預覽計入已 lock 拍攝 ---------- */
// 入口 stress 35、一個 5 日拍攝：未 lock 預覽峰值約 58（得一日休息）；lock 後 5 日拍攝 +10/日，
// 峰值 85 衝上 80 → 預設應畀三日休息（plan[1]、plan[3]、plan[6] 皆 rest）。
S.stress = 35;
S.enrolled = {}; S.trainCount = { train_acting: 5 }; S.mockDebts = [];
const shB = { id: 'shB', totalDays: 5, doneDays: 0, daysLeft: 99, deadlineDay: 999 };
S.shoots = [shB];
const planB = defaultWeekPlan();
const restsB = planB.filter(x => x === 'rest').length;
ok('B 重拍攝週預設三日休息', restsB >= 3, JSON.stringify(planB));
ok('B 預覽唔留 daysLeft 副作用', shB.daysLeft === 99, 'daysLeft=' + shB.daysLeft);
// 對照：冇拍攝時同 stress 只得一日休息
S.shoots = [];
const planB0 = defaultWeekPlan();
ok('B 無拍攝對照一日休息', planB0.filter(x => x === 'rest').length === 1, JSON.stringify(planB0));

/* ---------- C BE 抉擇覆蓋 commit ---------- */
const stC = { story: { done: { R_so_meet: 1, R_so_crisis: 1 }, rel: { rel_so: 6 } }, flags: { flag_so_commit: 1 } };
ok('C commit 未 BE → committed', endingRomance410(stC).so.committed === true);
stC.flags.flag_so_be = 1;
ok('C commit 後 BE → 唔當 committed', endingRomance410(stC).so.committed === false);
const stC2 = { story: { done: {}, rel: {} }, flags: { flag_hiu_be: 1 } };
ok('C 只有 BE 旗照舊唔 committed', endingRomance410(stC2).hiu.committed === false);

/* ---------- D 補位失效來源 ---------- */
S.dayIndex = 10; S.pendingAud = []; S.shoots = []; S.flags = {};
S.intel381 = { mk: 1, gigId: 'g1', state: 'msg', msgDay: 0, keptDay: 0 };
intel381Tick();
ok('D msg 失效寫 expiredFrom=msg', S.intel381.state === 'expired' && S.intel381.expiredFrom === 'msg', JSON.stringify(S.intel381));
S.intel381 = { mk: 1, gigId: 'g2', state: 'kept', msgDay: 0, keptDay: 0 };
intel381Tick();
ok('D kept 失效寫 expiredFrom=kept', S.intel381.state === 'expired' && S.intel381.expiredFrom === 'kept', JSON.stringify(S.intel381));

console.log(fails ? ('TOTAL FAIL ' + fails) : 'TOTAL PASS');
process.exit(fails ? 1 : 0);
