// v20a109 DLG109 邏輯測試：per-character 身高比表 × DLG108 fitted 基礎高。
// 身高比數字理據見 index.html 內 DLG109 註解＋NOTES_V20A109_HEIGHT.md：
// 阿偉 1.00 基準；彭少祺 0.85（brief 矮胖＋AR 0.374 闊過阿偉 9%）；
// 顧明輝／程天諾 1.05（AR 全庫最瘦 0.232／0.267，圖中腿長身窄）；其餘 1.00。
// 闊高比數字來自真檔 PIL 實量（awi 0.343／pang 0.376／gu 0.232／ho 0.364／
// chung 0.337／fong 0.413／vera 0.382），同 test_dlg108_static.py 重測一致。
// 規則：渲染高＝fitted 基礎高（上限 60%）× 身高比；腳底 bottom:10% 唔郁；
// 單人步同樣 × 比；未知 id → 1.00。
// 反證：(a) 身高比改 1.00 → 彭少祺渲染高必須等於阿偉；(b) 收窄舞台令闊度綁死時，
//       pang 用 0.85 嘅 fitted 基礎高必須高過用 1.00；(c) 表缺一個 GAZE id →
//       覆蓋斷言必須 FAIL（用改爛咗嘅表驗證）；(d) 單人／無效輸入 → 回 60 基礎。
// 用法：node tests/test_dlg109_height_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS ' : 'FAIL ') + name); }
function info(msg){ console.log('INFO ' + msg); }

const a8 = html.indexOf('/* ===== v20a108 DLG108');
const b8 = html.indexOf('/* ===== DLG108 模組完 ===== */');
ok('搵到 DLG108 模組', a8 >= 0 && b8 > a8);
const a9 = html.indexOf('/* ===== v20a109 DLG109');
const b9 = html.indexOf('/* ===== DLG109 模組完 ===== */');
ok('搵到 DLG109 模組', a9 >= 0 && b9 > a9);
if (a8 < 0 || b8 <= a8 || a9 < 0 || b9 <= a9) { console.log('RESULT FAIL (no module)'); process.exit(1); }
global.window = {};
const M = eval(html.slice(a8, b8) + '\n' + html.slice(a9, b9) +
  '\n;({fitPct:dlg108FitPct, fitApply:dlg108FitApply, D109:window.DLG109})');
const fit = M.fitPct, apply = M.fitApply, D109 = M.D109;
ok('搵到 dlg108FitPct／dlg108FitApply／window.DLG109',
   typeof fit === 'function' && typeof apply === 'function' && D109 && typeof D109.scale === 'function');

// ---- 身高比表 ----
const GAZE_IDS = ["awi","awi_s2","awi_s3","chai_zanhoi","cheng_william","cheung_hakfan",
  "cheung_tsijun","ching_tinlok","chow_choiyi","chung_choning","extra_ad_fen",
  "fong_siulung","gao_wenhan","gu_mingfai","ho_sang","ko_chunkit","kwan_hoimei",
  "lan_ruoxi","lin_hiu","liu_bingxing","lok_gasing","lui_ging","luk_baakyin",
  "mak_zhendong","mok_siufai","ngai_wingnaam","pang_siuki","so_jiyan",
  "tang_laiping","tong_souwan","tsui_poushan","uncle_kim","vera","yip_manji"];
ok('身高比表有 34 個 key（DLG106_GAZE 全數）', Object.keys(D109.SCALE).length === 34);
ok('身高比表覆蓋全部 34 個 GAZE id', GAZE_IDS.every(id => typeof D109.SCALE[id] === 'number'));
ok('全部身高比喺 0.80–1.10 之間',
   Object.values(D109.SCALE).every(v => v >= 0.80 && v <= 1.10));
ok('阿偉基準 1.00（s1／s2／s3 同值）',
   D109.scale('awi') === 1 && D109.scale('awi_s2') === 1 && D109.scale('awi_s3') === 1);
ok('彭少祺 0.85（＜0.90，明顯矮過阿偉）', D109.scale('pang_siuki') === 0.85);
ok('顧明輝／程天諾 1.05（高檔）',
   D109.scale('gu_mingfai') === 1.05 && D109.scale('ching_tinlok') === 1.05);
ok('其餘角色一律 1.00（唔估身高）',
   GAZE_IDS.filter(id => ['awi','awi_s2','awi_s3','pang_siuki','gu_mingfai','ching_tinlok'].indexOf(id) < 0)
     .every(id => D109.scale(id) === 1));
ok('未知 id 回 1.00（舊圖後備唔郁）',
   D109.scale('nobody') === 1 && D109.scale('') === 1 && D109.scale(null) === 1);
ok('scaledPct：60% 基礎 → 彭少祺 51%／阿偉 60%／顧明輝 63%',
   D109.scaledPct(60, 'pang_siuki') === 51 && D109.scaledPct(60, 'awi') === 60 &&
   D109.scaledPct(60, 'gu_mingfai') === 63);
ok('scaledPct：收細後基礎 54.6% → 方小龍 54.6%（1.00 唔變）',
   D109.scaledPct(54.6, 'fong_siulung') === 54.6);
ok('scaledPct：無效基礎回 60', D109.scaledPct(0, 'pang_siuki') === 51 && D109.scaledPct(NaN, 'awi') === 60);

// ---- 實測闊高比（base 圖）----
const AR = { awi: 0.3429, pang: 0.3757, gu: 0.2319, ho: 0.3637, chung: 0.3370, fong: 0.4127, vera: 0.3821 };
const W = 390, H = 844; // 舞台 390×844
function gapAt(basePct, arL, scL, arR, scR, margin){
  const h = basePct / 100 * H, maxW = 0.48 * W;
  return W - margin - (Math.min(h * scL * arL, maxW) + Math.min(h * scR * arR, maxW));
}

// ---- fitted 基礎高 × 身高比（DLG108 6 參舊調用必須零變）----
let p = fit(AR.awi, AR.ho, W, H, 12, 0.48);
ok('舊調用（6 參，唔傳比）零變：阿偉×何生基礎高仍係 60%', p === 60);
p = fit(AR.fong, AR.vera, W, H, 12, 0.48);
ok('舊調用零變：最闊配對方小龍＋Vera 基礎高仍係 54–56%', p >= 54 && p <= 56);
p = fit(AR.awi, AR.pang, W, H, W * 0.04, 0.48, 1, 0.85);
ok('阿偉×彭少祺基礎高 60%（矮咗更鬆，唔使收）', p === 60);
ok('阿偉×彭少祺 60% 基礎淨空 ≥12（實數約 39.0px）',
   gapAt(60, AR.awi, 1, AR.pang, 0.85, W * 0.04) >= 12);
ok('阿偉×彭少祺渲染高：阿偉 60%／彭少祺 51%（頭頂差 76px）',
   D109.scaledPct(60, 'awi') - D109.scaledPct(60, 'pang_siuki') === 9);
p = fit(AR.awi, AR.gu, W, H, W * 0.04, 0.48, 1, 1.05);
ok('阿偉×顧明輝基礎高 60%（顧生瘦，唔使收）', p === 60);
ok('阿偉×顧明輝渲染高：顧明輝 63%（高過阿偉）', D109.scaledPct(60, 'gu_mingfai') === 63);
p = fit(AR.awi, AR.chung, W, H, W * 0.04, 0.48, 1, 1);
ok('阿偉×鍾楚凝基礎高 60%（兩人皆 1.00，v108 不變）', p === 60);

// ---- 反證：身高比真係影響計數（唔係擺設）----
ok('反證：彭少祺比由 0.85 改 1.00，渲染高必須等於阿偉（51→60）',
   D109.scaledPct(60, 'pang_siuki') !== 60 && (() => {
     const t = Object.assign({}, D109.SCALE, { pang_siuki: 1.00 });
     return Math.round(60 * t.pang_siuki * 10) / 10 === 60;
   })());
ok('反證：舞台收窄到 300px（max-width 帽放寬到 1.0，等闊度綁死），pang 用 0.85 嘅 fitted 基礎高必須高過用 1.00',
   fit(AR.awi, AR.pang, 300, H, 12, 1.0, 1, 0.85) > fit(AR.awi, AR.pang, 300, H, 12, 1.0, 1, 1.00));
ok('反證：表缺一個 GAZE id，覆蓋斷言必須 FAIL',
   !GAZE_IDS.every(id => typeof Object.assign({}, D109.SCALE, { vera: undefined })[id] === 'number'));

// ---- fitApply：逐張 inline height（mock DOM）----
function mockStage(isEnc, imgs){
  const vars = {};
  return { _vars: vars,
    classList: { contains: (c) => isEnc && c === 'e79-stage' },
    querySelectorAll: () => imgs,
    style: { setProperty: (k, v) => { vars[k] = v; } },
    clientWidth: 390, clientHeight: 844 };
}
function mockImg(id, nw, nh, viaSid){
  return { naturalWidth: nw, naturalHeight: nh, _sid106: viaSid ? id : null, style: {},
    getAttribute: (n) => (!viaSid && n === 'data-dlg-id') ? id : null };
}
let st = mockStage(true, [mockImg('awi', 480, 1400, true), mockImg('pang_siuki', 789, 2100, true)]);
ok('fitApply 巧遇 阿偉×彭少祺成功', apply(st) === true);
ok('fitApply 巧遇：舞台 var 仍係基礎高 60%', st._vars['--dlg108-char-h'] === '60%');
ok('fitApply 巧遇：阿偉 inline 高 60%／彭少祺 51%',
   st.querySelectorAll()[0].style.height === '60%' && st.querySelectorAll()[1].style.height === '51%');
st = mockStage(true, [mockImg('awi', 480, 1400, true), mockImg('gu_mingfai', 604, 2604, true)]);
ok('fitApply 巧遇 阿偉×顧明輝：顧明輝 inline 高 63%',
   apply(st) === true && st.querySelectorAll()[1].style.height === '63%');
st = mockStage(false, [mockImg('awi', 480, 1400), mockImg('ho_sang', 763, 2098)]);
ok('fitApply 主線 阿偉×何生：兩人皆 60%（v108 不變）',
   apply(st) === true && st.querySelectorAll()[0].style.height === '60%' &&
   st.querySelectorAll()[1].style.height === '60%');
st = mockStage(false, [mockImg('fong_siulung', 577, 1398), mockImg('vera', 543, 1421)]);
ok('fitApply 主線 最闊配對：基礎高收至 54–56%，兩人同高',
   apply(st) === true && parseFloat(st._vars['--dlg108-char-h']) >= 54 &&
   parseFloat(st._vars['--dlg108-char-h']) <= 56 &&
   st.querySelectorAll()[0].style.height === st.querySelectorAll()[1].style.height);
st = mockStage(false, [mockImg('pang_siuki', 789, 2100)]);
ok('fitApply 單人彭少祺：var 60%／inline 高 51%',
   apply(st) === true && st._vars['--dlg108-char-h'] === '60%' &&
   st.querySelectorAll()[0].style.height === '51%');
st = mockStage(false, [mockImg('mystery_npc', 500, 1400)]);
ok('fitApply 未知 id 單人：inline 高 60%（默認 1.00）',
   apply(st) === true && st.querySelectorAll()[0].style.height === '60%');
st = mockStage(false, [mockImg('awi', 0, 0)]);
ok('fitApply 未載入圖回 false（唔亂設高）', apply(st) === false);

info('渲染高一覽（基礎 60%）：awi=60 pang=51 gu=63 ho=60 chung=60 fong+vera~54.6');
console.log(fails.length ? ('RESULT FAIL (' + fails.length + ')') : 'RESULT PASS');
process.exit(fails.length ? 1 : 0);
