// v20a108 DLG108 邏輯測試：per-pair 自動收細 dlg108FitPct。
// 闊高比數字來自 qa108d/remeasure108d.json（v106 現行 88 張實測，PIL 量度），
// 同 size-test README（awi 0.343／ho 0.364／chung 0.337／fong 0.413／vera 0.382）
// 逐項對得上（誤差 ≤0.001）。
// 規則：人物高上限 60% 舞台高；兩圖闊合計 ≤ stageW - margin - 12px；
// 每圖闊 ≤ 48% stageW（max-width 帽）；淨空 ＜12px 就降高到啱為止。
// 反證：(a) 最闊配對改闊 → fitted 高必須再降；(b) 淨空改 12→30 → fitted 高必須降；
//       (c) 單人／無效闊高比 → 必須回 60。
// 用法：node tests/test_dlg108_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS ' : 'FAIL ') + name); }
function info(msg){ console.log('INFO ' + msg); }

const a = html.indexOf('/* ===== v20a108 DLG108');
const b = html.indexOf('/* ===== DLG108 模組完 ===== */');
ok('搵到 DLG108 模組', a >= 0 && b > a);
if (a < 0 || b <= a) { console.log('RESULT FAIL (no DLG108 module)'); process.exit(1); }
const code = html.slice(a, b);
global.window = {};
const D = eval(code + '\n;({fitPct:dlg108FitPct, fitApply:dlg108FitApply})');
const fit = D.fitPct;
ok('搵到 dlg108FitPct', typeof fit === 'function');

// 實測闊高比（remeasure108d.json，base 圖）
const AR = { awi: 0.3429, ho: 0.3637, chung: 0.3370, fong: 0.4127, vera: 0.3821, yip: 0.3824 };
const W = 390, H = 844; // 舞台 390×844
function gapAt(pct, arL, arR, margin, maxWfrac){
  // 可見中間淨空（唔扣 12px 要求）：stageW - margin - 兩圖闊
  const h = pct / 100 * H, maxW = (maxWfrac || 0.48) * W;
  return W - margin - (Math.min(h * arL, maxW) + Math.min(h * arR, maxW));
}

// ---- 錨點配對：60% 唔使收，淨空 ≥12 ----
let p = fit(AR.awi, AR.ho, W, H, 12, 0.48);
ok('主線 阿偉×何生 60%（淨空 20.2px，size-test 17px 實測新批更鬆）', p === 60);
ok('主線 阿偉×何生 60% 淨空實數 ≥12', gapAt(60, AR.awi, AR.ho, 12) >= 12);
p = fit(AR.awi, AR.chung, W, H, W * 0.04, 0.48);
ok('巧遇 阿偉×鍾楚凝 60%（淨空 33.7px，size-test 30px）', p === 60);
ok('巧遇 阿偉×鍾楚凝 60% 淨空實數 ≥12', gapAt(60, AR.awi, AR.chung, W * 0.04) >= 12);

// ---- 最闊配對：60% 穿，收至約 54.6% ----
p = fit(AR.fong, AR.vera, W, H, 12, 0.48);
ok('最闊 方小龍＋Vera 收細到 54–56%（size-test 上限約 55%）', p >= 54 && p <= 56);
ok('最闊 方小龍＋Vera 收細後淨空 ≥12', gapAt(p, AR.fong, AR.vera, 12) >= 12);
ok('最闊 方小龍＋Vera 收細後淨空唔會過鬆（<20，唔係過度收）', gapAt(p, AR.fong, AR.vera, 12) < 20);
p = fit(AR.fong, AR.yip, W, H, 12, 0.48);
ok('最闊 方小龍＋葉敏芝（同合計 0.795）同樣收至 54–56%', p >= 54 && p <= 56);
p = fit(AR.fong, AR.vera, W, H, W * 0.04, 0.48);
ok('最闊配對巧遇邊距（2%＋2%）同樣收至 54–56%', p >= 54 && p <= 56);

// ---- 典型配對（中位數合計約 0.65）：60% 得 ----
ok('典型配對（0.325＋0.325）60% 唔使收', fit(0.325, 0.325, W, H, 12, 0.48) === 60);

// ---- 邊界／無效輸入 ----
ok('單人（其一闊高比 0）回 60', fit(AR.awi, 0, W, H, 12, 0.48) === 60);
ok('無效闊高比（NaN）回 60', fit(NaN, AR.ho, W, H, 12, 0.48) === 60);
ok('無效舞台尺寸回 60', fit(AR.awi, AR.ho, 0, H, 12, 0.48) === 60);
ok('fitted 高唔低過下限 30%', fit(0.9, 0.9, W, H, 12, 0.48) >= 30);
ok('max-width 帽有計入：有帽比冇帽 fitted 高（帽幫手食咗闊度）', (() => {
  const withCap = fit(AR.fong, AR.vera, W, H, 12, 0.48);
  const noCap = fit(AR.fong, AR.vera, W, H, 12, 1.0);
  return withCap > noCap && gapAt(withCap, AR.fong, AR.vera, 12) >= 12 - 0.01;
})());

// ---- 反證：改闊／改淨空要求，結果必須跟住變（證明係 live 計數） ----
ok('反證：配對闊高比加大（0.34＋0.34 → 0.37＋0.37，兩邊都唔撞 48% 帽），fitted 高必須降', fit(0.37, 0.37, W, H, 12, 0.48) < fit(0.34, 0.34, W, H, 12, 0.48));
ok('反證：淨空要求由 12 改大（margin ＋30），錨點配對都要收', fit(AR.awi, AR.ho, W, H, 12 + 30, 0.48) < 60);
ok('反證：舞台闊一倍，乜配對都唔使收', fit(AR.fong, AR.vera, W * 2, H, 12, 0.48) === 60);

info('fitted 高一覽：awi+ho=' + fit(AR.awi, AR.ho, W, H, 12, 0.48) + '%，awi+chung=' +
  fit(AR.awi, AR.chung, W, H, W * 0.04, 0.48) + '%，fong+vera=' + fit(AR.fong, AR.vera, W, H, 12, 0.48) + '%');
console.log(fails.length ? ('RESULT FAIL (' + fails.length + ')') : 'RESULT PASS');
process.exit(fails.length ? 1 : 0);
