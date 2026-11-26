// v396：第四輪 UI 檢視頭五項必修 — 邏輯測試（純函數）。
// 抽 index.html 入面 v396 段出嚟 eval，驗預期日薪計法／日結日期標示。
// 用法：node tests/test_v396_logic.js
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
  // 函數由 sig 開始，到第一個行首 } 為止（呢啲函數無巢狀行首 }）
  const e = src.indexOf('\n}\n', b);
  if(e < 0) throw new Error('no end for: ' + sig);
  return src.slice(b, e + 3);
}

// ---- (2) 預期日薪：board392ExpDaily = chance × pay ÷ days ----
// stubs：gigPayExact／chance／effectiveShootDays 係 IIFE 內部函數，測試用替身。
const gigPayExact = g => g.pay;
const chance = g => g.chance;
const effectiveShootDays = g => g.days;
eval(extractFn(src, 'function board392ExpDaily(g){'));
ok('exp 378×0.86÷4 = 81.27', Math.abs(board392ExpDaily({pay:378, chance:0.86, days:4}) - 81.27) < 1e-9);
ok('exp 284×0.86÷3 = 81.41…', Math.abs(board392ExpDaily({pay:284, chance:0.86, days:3}) - 81.41333333333333) < 1e-9);
ok('exp 259×0.87÷3 = 75.11', Math.abs(board392ExpDaily({pay:259, chance:0.87, days:3}) - 75.11) < 1e-9);
ok('exp 1 日 87% → pay×0.87', Math.abs(board392ExpDaily({pay:200, chance:0.87, days:1}) - 174) < 1e-9);
ok('exp pay 0 → 0', board392ExpDaily({pay:0, chance:0.9, days:2}) === 0);
ok('exp pay null → 0', board392ExpDaily({pay:null, chance:0.9, days:2}) === 0);
ok('exp days 0 → 當 1 日計（唔除零）', Math.abs(board392ExpDaily({pay:100, chance:0.5, days:0}) - 50) < 1e-9);
ok('exp chance 0 → 0', board392ExpDaily({pay:378, chance:0, days:4}) === 0);
ok('exp 四捨五入：378×0.87÷4 = 82.215 → 82（實駕 $82，顯示 86% 係 chance() 另一口徑）', Math.round(board392ExpDaily({pay:378, chance:0.87, days:4})) === 82);
ok('exp 一屋人實駕數 $57（低數值 66%）', Math.round(board392ExpDaily({pay:259, chance:0.66, days:3})) === 57);

// ---- (3) 日結日期標示：dayResDateLine396 ----
// stub displayDateObj：卡出嗰陣 dayIndex 已經係下一日（1990-01-19 星期五）。
// 用 let，等跨月測試可以換 stub。
let displayDateObj = () => new Date(1990, 0, 19);
eval(extractFn(src, 'function settledDateObj396(){'));
eval(extractFn(src, 'function fmtShortDate396(d){'));
eval(extractFn(src, 'function dayResDateLine396(firstLabel, doneFull){'));
ok('fmtShortDate 1990-01-19（五）', fmtShortDate396(new Date(1990, 0, 19)) === '1月19日（五）');
ok('fmtShortDate 1990-01-18（四）', fmtShortDate396(new Date(1990, 0, 18)) === '1月18日（四）');
ok('fmtShortDate 1990-01-21（日）', fmtShortDate396(new Date(1990, 0, 21)) === '1月21日（日）');
ok('fmtShortDate 跨月 1990-02-01（四）', fmtShortDate396(new Date(1990, 1, 1)) === '2月1日（四）');
ok('fmtShortDate null → 空字串', fmtShortDate396(null) === '');
ok('settledDateObj = displayDateObj 減一日（1月18日）',
   settledDateObj396() && settledDateObj396().getDate() === 18 && settledDateObj396().getMonth() === 0);
ok('settledDateObj 跨月：display 1990-02-01 → 結算 1月31日', (() => {
  const save = displayDateObj;
  displayDateObj = () => new Date(1990, 1, 1);
  const s = settledDateObj396();
  displayDateObj = save;
  return s && s.getMonth() === 0 && s.getDate() === 31;
})());
ok('settledDateObj 跨年：display 1991-01-01 → 結算 1990-12-31', (() => {
  const save = displayDateObj;
  displayDateObj = () => new Date(1991, 0, 1);
  const s = settledDateObj396();
  displayDateObj = save;
  return s && s.getFullYear() === 1990 && s.getMonth() === 11 && s.getDate() === 31;
})());
ok('dayResDateLine 結算（有傳入 dayDone）',
   dayResDateLine396('結算', '1990年1月18日（四）· 第3週') === '結算：1月18日（四） · 今日：1月19日（五）');
ok('dayResDateLine 完成日（有傳入 dayDone）',
   dayResDateLine396('完成日', '1990年1月18日（四）· 第3週') === '完成日：1月18日（四） · 今日：1月19日（五）');
ok('dayResDateLine 無傳入 dayDone → 重計結算日',
   dayResDateLine396('結算', null) === '結算：1月18日（四） · 今日：1月19日（五）');
ok('dayResDateLine 週結 D1：結算日抽到 1月21日（日）（下一日由 displayDateObj stub 定）',
   dayResDateLine396('結算', '1990年1月21日（日）· 第4週').indexOf('結算：1月21日（日）') === 0);
ok('dayResDateLine 結算日一定係「M月D日（週X）」格式',
   /^結算：\d+月\d+日（[日一二三四五六]） · 今日：\d+月\d+日（[日一二三四五六]）$/.test(dayResDateLine396('結算', '1990年1月18日（四）· 第3週')));

console.log(pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
