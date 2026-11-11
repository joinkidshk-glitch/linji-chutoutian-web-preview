// v20a109 BUST109 邏輯測試：頁頭阿偉像跟成長級數（bust109HeroSrc）。
// 資料一律由 index.html 抽真身 eval：DLG106 模組切片（同 test_dlg107_logic.js
// 手法，含 dlg106AweiStem＋bust109HeroSrc）＋ PORTRAITS／BUST109_EXTRA
// 兩個 map 嘅真值；tier 經 global.__tier109 stub（enc79PlayerTier 替身）控制。
// 覆蓋：(1) tier 0／1 → s1（PORTRAITS.hero_awi）；tier 2 → BUST109_EXTRA.awi_s2；
//         tier 3／99 → awi_s3；(2) 缺圖後備：EXTRA 缺失／PORTRAITS 缺失／
//         兩邊都冇／enc79PlayerTier 拋錯，全部唔 crash 且有確定回值；
//         (3) 回值一定係解得到嘅 WebP data URI（RIFF/WEBP 檔頭）；
//         (4) 反證：tier 2↔3 切換回值必須跟住變；s1 回值唔等於 s2／s3 回值；
//         dlg106AweiStem 本身 tier→stem 映射不變（回歸）。
// 注意：檔案存在＋尺寸＋hash 由 test_bust109_static.py 守門；
// 瀏覽器真載入由 qa109b 實駕驗證。
// 用法：node tests/test_bust109_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS ' : 'FAIL ') + name); }

function extractMap(name){
  const a = html.indexOf('const ' + name + ' = {');
  ok('搵到 ' + name, a >= 0);
  if (a < 0) return null;
  const b = html.indexOf('};', a) + 2;
  // 值係 base64（唔含 '};'），第一個 '};' 就係 block 尾。
  const code = html.slice(a, b);
  return new Function(code + '; return ' + name + ';')();
}
global.PORTRAITS = extractMap('PORTRAITS');
global.BUST109_EXTRA = extractMap('BUST109_EXTRA');
if (!global.PORTRAITS || !global.BUST109_EXTRA) {
  console.log('FAILURES: ' + fails.length);
  for (const f of fails) console.log(' - ' + f);
  process.exit(1);
}
ok('PORTRAITS 7 鍵', Object.keys(global.PORTRAITS).length === 7);
ok('BUST109_EXTRA 14 鍵', Object.keys(global.BUST109_EXTRA).length === 14);

const a = html.indexOf('/* ===== v20a106 DLG106');
const b = html.indexOf('/* ===== DLG106 模組完 ===== */');
ok('搵到 DLG106 模組', a >= 0 && b > a);
ok('模組內有 bust109HeroSrc', html.slice(a, b).indexOf('function bust109HeroSrc()') >= 0);
global.window = {};
global.__tier109 = 0;
global.enc79PlayerTier = () => global.__tier109;
eval(html.slice(a, b) + '\n;({DLG106_GAZE,DLG106_EMOTION_MAP,DLG106_CAT_TO_EXPR})');
// function 宣告經 eval 已入 scope：dlg106AweiStem／bust109HeroSrc

const isWebpDataUri = (u) => {
  if (typeof u !== 'string' || !u.startsWith('data:image/webp;base64,')) return false;
  const raw = Buffer.from(u.slice(u.indexOf(',') + 1), 'base64');
  return raw.length > 12 && raw.slice(0, 4).toString('ascii') === 'RIFF'
      && raw.slice(8, 12).toString('ascii') === 'WEBP';
};

/* ---- (1) tier → 頁頭像 ---- */
global.__tier109 = 0;
ok('tier 0 → s1 hero_awi', bust109HeroSrc() === global.PORTRAITS.hero_awi);
global.__tier109 = 1;
ok('tier 1 → s1 hero_awi（配角仍係 s1）', bust109HeroSrc() === global.PORTRAITS.hero_awi);
global.__tier109 = 2;
ok('tier 2 → awi_s2', bust109HeroSrc() === global.BUST109_EXTRA.awi_s2);
global.__tier109 = 3;
ok('tier 3 → awi_s3', bust109HeroSrc() === global.BUST109_EXTRA.awi_s3);
global.__tier109 = 99;
ok('tier 99 → awi_s3（>=3 一律 s3）', bust109HeroSrc() === global.BUST109_EXTRA.awi_s3);

/* ---- (4) 反證：切換跟住變＋三階段互不相同 ---- */
global.__tier109 = 2; const s2 = bust109HeroSrc();
global.__tier109 = 3; const s3 = bust109HeroSrc();
global.__tier109 = 0; const s1 = bust109HeroSrc();
ok('反證：tier 2↔3 回值唔同', s2 !== s3);
ok('反證：s1／s2／s3 三個回值互不相同', s1 !== s2 && s1 !== s3 && s2 !== s3);
ok('dlg106AweiStem 回歸：tier 0→awi', (()=>{ global.__tier109=0; return dlg106AweiStem()==='awi'; })());
ok('dlg106AweiStem 回歸：tier 2→awi_s2', (()=>{ global.__tier109=2; return dlg106AweiStem()==='awi_s2'; })());
ok('dlg106AweiStem 回歸：tier 3→awi_s3', (()=>{ global.__tier109=3; return dlg106AweiStem()==='awi_s3'; })());

/* ---- (3) 回值係真 WebP ---- */
for (const t of [0, 1, 2, 3]) {
  global.__tier109 = t;
  ok(`tier ${t} 回值係 WebP data URI`, isWebpDataUri(bust109HeroSrc()));
}
for (const [k, v] of Object.entries(global.BUST109_EXTRA)) {
  ok(`BUST109_EXTRA.${k} 係 WebP data URI`, isWebpDataUri(v));
}
for (const [k, v] of Object.entries(global.PORTRAITS)) {
  ok(`PORTRAITS.${k} 係 WebP data URI`, isWebpDataUri(v));
}

/* ---- (2) 缺圖／拋錯後備（唔 crash、有確定回值） ---- */
const savedExtra = global.BUST109_EXTRA;
const savedPortraits = global.PORTRAITS;
global.__tier109 = 2;
global.BUST109_EXTRA = undefined;
ok('EXTRA 缺失＋tier 2 → 退 s1，唔 crash', bust109HeroSrc() === savedPortraits.hero_awi);
global.BUST109_EXTRA = {};
ok('EXTRA 空物件＋tier 2 → 退 s1，唔 crash', bust109HeroSrc() === savedPortraits.hero_awi);
global.BUST109_EXTRA = savedExtra;
global.PORTRAITS = {};
ok('PORTRAITS 空物件＋tier 2 → 仍出 awi_s2', bust109HeroSrc() === savedExtra.awi_s2);
global.PORTRAITS = undefined;
global.BUST109_EXTRA = {};
ok('兩邊都冇 → 回 ""，唔 crash', bust109HeroSrc() === '');
global.PORTRAITS = savedPortraits;
global.BUST109_EXTRA = savedExtra;
global.enc79PlayerTier = () => { throw new Error('tier boom'); };
ok('enc79PlayerTier 拋錯 → 退 s1，唔 crash', bust109HeroSrc() === savedPortraits.hero_awi);
global.enc79PlayerTier = () => global.__tier109;
global.__tier109 = 2;
ok('修復後 tier 2 → awi_s2（後備測試冇污染狀態）', bust109HeroSrc() === savedExtra.awi_s2);

console.log('FAILURES: ' + fails.length);
for (const f of fails) console.log(' - ' + f);
process.exit(fails.length ? 1 : 0);
