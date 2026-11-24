// v397：第五輪 UI 檢視頭五項必修 — 邏輯測試（純函數＋夾實 stub）。
// 抽 index.html 入面 v397 段出嚟 eval，驗預期日薪計法／日結 ledger／地圖夾實。
// 用法：node tests/test_v397_logic.js
const fs = require('fs');
const path = require('path');
const rootDir = path.join(__dirname, '..');
const src = fs.readFileSync(path.join(rootDir, 'index.html'), 'utf8');

let pass = 0, fail = 0;
function ok(name, cond){
  if(cond){ pass++; console.log('  ok - ' + name); }
  else { fail++; console.log('  FAIL - ' + name); }
}
function extractFn(src, sig){
  const b = src.indexOf(sig);
  if(b < 0) throw new Error('not found: ' + sig);
  const e = src.indexOf('\n}\n', b);
  if(e < 0) throw new Error('no end for: ' + sig);
  return src.slice(b, e + 3);
}

// ---- (3) 詳情預期日薪計法：boardExpCalc397 ----
// stubs：gigPayExact／chance／effectiveShootDays 係 IIFE 內部函數，測試用替身。
const gigPayExact = g => g.pay;
const chance = g => g.chance;
const effectiveShootDays = g => g.days;
eval(extractFn(src, 'function boardExpCalc397(g){'));
{
  const c = boardExpCalc397({pay:378, chance:0.863, days:4});
  ok('calc 378×86.3%÷4：raw≈81.55、rounded 82', c && Math.abs(c.raw - 81.5535) < 1e-9 && c.rounded === 82);
  ok('calc 帶齊 pay／chance／days', c && c.pay === 378 && c.chance === 0.863 && c.days === 4);
  const c2 = boardExpCalc397({pay:378, chance:0.865, days:4});
  ok('calc 378×86.5%÷4 = 81.7425 → 82（audit 81.27 係用已取整 86% 計）',
     c2 && Math.abs(c2.raw - 81.7425) < 1e-9 && c2.rounded === 82);
  ok('calc pay null → null', boardExpCalc397({pay:null, chance:0.9, days:2}) === null);
  ok('calc chance 0 → null', boardExpCalc397({pay:378, chance:0, days:4}) === null);
  ok('calc days 0 → null（唔除零）', boardExpCalc397({pay:378, chance:0.9, days:0}) === null);
  ok('calc 單日：200×87%÷1 = 174', (()=>{ const x = boardExpCalc397({pay:200, chance:0.87, days:1}); return x && x.raw === 174 && x.rounded === 174; })());
}

// ---- (4) 27c 日結 ledger：dayResLedger397 ----
eval(extractFn(src, 'function dayResLedger397(html){'));
function statRow(nm, val, cls){
  return `<div class="result-line res-stat374"><span class="res-stat-n374">${nm}</span><span class="res-stat-v374 ${cls||'good'}">${val}</span></div>`;
}
{
  const html = `<div class="result-notes">${statRow('演技','+6')}${statRow('台風','+1')}${statRow('現金','−$20','bad')}${statRow('壓力','+12')}${statRow('演技','+1')}${statRow('壓力','−2','bad')}<div class="result-line res-note374">電視台排練結束，阿偉記住鏡頭位置。</div></div>`;
  const out = dayResLedger397(html);
  ok('ledger 同名合併：演技 +6＋+1 → +7；壓力 +12／−2 → +10',
     out.indexOf('演技 +7') >= 0 && out.indexOf('壓力 +10') >= 0);
  ok('ledger 一行齊：現金 −$20、台風 +1',
     out.indexOf('現金 −$20') >= 0 && out.indexOf('台風 +1') >= 0);
  ok('ledger 用 dayres-ledger397 class（一行手帳記錄）',
     out.indexOf('class="dayres-ledger397"') >= 0);
  ok('ledger 刪走個別 stat 框（res-stat374 歸零）',
     (out.match(/res-stat374/g) || []).length === 0);
  ok('ledger 敘事行唔郁（res-note374 保留）',
     out.indexOf('電視台排練結束') >= 0 && out.indexOf('res-note374') >= 0);
  const plain = `<div class="result-notes"><div class="result-line res-note374">純敘事，無數值。</div></div>`;
  ok('ledger 無 stat 行 → 原樣返', dayResLedger397(plain) === plain);
  ok('ledger 空字串 → 空字串', dayResLedger397('') === '');
  const weird = `<div class="result-notes">${statRow('演技','+6')}<div class="result-line res-stat374"><span class="res-stat-n374">聲望</span><span class="res-stat-v374 good">大升</span></div></div>`;
  const outW = dayResLedger397(weird);
  ok('ledger 唔識 parse 嘅行原樣留返（唔靜默刪走）',
     outW.indexOf('大升') >= 0 && outW.indexOf('演技 +6') >= 0);
}

// ---- (1) venue99 碰撞夾實：clampMapLabels397（fake document） ----
eval(extractFn(src, 'function clampMapLabels397(){'));
function makeStage(top, bottom){
  return { getBoundingClientRect: () => ({ top, bottom, left: 0, right: 390, width: 390, height: bottom - top }) };
}
function makeLabel(x, y, w, h){
  const baseTop = y;
  const el = { offsetParent: {}, style: { top: baseTop + 'px' }, _x: x, _y: y, _w: w, _h: h };
  el.getBoundingClientRect = () => {
    const dy = (parseFloat(el.style.top) || 0) - baseTop;
    return { left: el._x, top: el._y + dy, right: el._x + el._w, bottom: el._y + el._h + dy, width: el._w, height: el._h };
  };
  return el;
}
function withDoc(stage, labels, fn){
  const save = (typeof document !== 'undefined') ? global.document : undefined;
  global.document = {
    querySelector: () => stage,
    getElementById: () => null,
    querySelectorAll: () => labels,
  };
  try{ return fn(); } finally { if(save === undefined) delete global.document; else global.document = save; }
}
{
  // 紅棉 x240–304／y221–239 vs 金禧 x298–370／y221–234：水平重疊、垂直相交 → 移夠 8px 淨距。
  const stage = makeStage(0, 600);
  const a = makeLabel(240, 221, 64, 18);
  const b = makeLabel(298, 221, 72, 13);
  const moved = withDoc(stage, [a, b], () => clampMapLabels397());
  const ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
  const gap = (ra.bottom <= rb.top) ? (rb.top - ra.bottom) : (ra.top - rb.bottom);
  ok('clamp 相疊兩籤移夠 8px 淨距（moved>0）', moved > 0 && gap >= 8);
  ok('clamp 上面嗰張唔郁（只移下面嗰張）', ra.top === 221);
  // 底邊出舞台：籤底 610 > stageBottom 596 → 向上夾返入舞台留 4px。
  const stage2 = makeStage(0, 600);
  const c = makeLabel(100, 590, 60, 20);
  withDoc(stage2, [c, makeLabel(200, 100, 60, 18)], () => clampMapLabels397());
  ok('clamp 底邊出舞台夾返入嚟（底 ≤ 596）', c.getBoundingClientRect().bottom <= 596);
  // 冇碰撞＋唔出底：唔郁。
  const stage3 = makeStage(0, 600);
  const d = makeLabel(100, 100, 60, 18), e = makeLabel(200, 100, 60, 18);
  const moved3 = withDoc(stage3, [d, e], () => clampMapLabels397());
  ok('clamp 無碰撞唔郁（moved=0）', moved3 === 0 && d.style.top === '100px' && e.style.top === '100px');
  // 舞台冇尺寸：即刻返 0。
  const stage4 = makeStage(0, 0);
  ok('clamp 舞台冇尺寸返 0', withDoc(stage4, [d, e], () => clampMapLabels397()) === 0);
}

console.log(pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
