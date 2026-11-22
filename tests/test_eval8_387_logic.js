// v20a387 第八輪評估 P2 收尾・邏輯測試
// 合約：
//   A 壓力峰值預覽校準（W3 P2-1）：stressDeltaForAct 拍攝日 = 12（實際 8+R(2,6) 平均）；
//     低入口（10）＋5 日連拍預覽峰值 ≥70（舊 +10 只有 60），觸發兩日休息門檻。
//   B wrapHistory 封頂 240（W4 P2-11）：寫入點 cap 同 careerStats95 全史口徑對齊。
//   C 觸控目標 44px（W2 P2-2/3/7）：子 tab 闊、people-go、np214-switch、awd62-skip、
//     gig-locked108 summary、btn-load-mini 全部 ≥44px。
//   D 頒獎舞台窄屏放大（W2 P2-6）：@media 480px frame scale(1.06)＋stage overflow-x:hidden。
//   E 落敗差額提示（W4 P2-12）：awards379GapBand 三段＋awards62WeakHint 非空，
//     nominated 格 weakHint62 接線存在（電影／電視男主角同口徑）。
// 反證：v386 index 冇上述改動 → 相關斷言 FAIL。
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
var S = { dayIndex: 0, stress: 10, weekPlan: null, shoots: [], flags: {}, story: { done: {}, rel: {} } };
var clamp = (v, a, b) => Math.max(a, Math.min(b, v));
var weekdayName = (i) => ['一','二','三','四','五','六','日'][i] || '';
var planMeta = (id) => ({ name: String(id || '') });
var AWARDS62_WIN_LINE = 0.875;
eval([
  extractFn('stressDeltaForAct'),
  extractFn('previewWeekStress'),
  extractFn('awards379GapBand'),
  extractFn('awards62WeakHint'),
].join('\n'));

/* ---------- A 壓力峰值預覽校準 ---------- */
ok('A1 拍攝日預覽 = 12', stressDeltaForAct('shoot:x') === 12, String(stressDeltaForAct('shoot:x')));
S.stress = 10;
const pvA = previewWeekStress(['shoot:a','shoot:a','shoot:a','shoot:a','shoot:a','cafe_gig','rest']);
ok('A2 低入口 5 日連拍峰值 ≥70', pvA.peak >= 70, 'peak=' + pvA.peak);

/* ---------- B wrapHistory 封頂 ---------- */
ok('B1 cap 240 寫入點', html.includes('S.wrapHistory.length>240) S.wrapHistory.length=240'));
ok('B2 舊 cap 90 已刪', !html.includes('S.wrapHistory.length>90) S.wrapHistory.length=90'));

/* ---------- C 觸控目標 ---------- */
ok('C1 people-go 44px', /\.people-go, \.debt-empty \.debt-repay-btn\{\s*\n\s*margin-top:6px; min-height:44px/.test(html));
ok('C2 np214-switch 44px', html.includes('min-height:44px; display:inline-flex; align-items:center; justify-content:center; /* v20a387（第八輪評估 W2 P2-7）：觸控高 39→44px'));
ok('C3 awd62-skip 44px', html.includes('min-height:44px;display:inline-flex;align-items:center;justify-content:center} /* v20a387'));
ok('C4 gig-locked108 summary 44px', html.includes('.gig-locked108 summary{ display:flex; align-items:center; min-height:44px;'));
ok('C5 btn-load-mini 44px', html.includes('#btn-load-mini{ font-size:.75rem; padding:5px 14px; min-height:44px;'));
ok('C6 子 tab 闊 44px', html.includes('#home-subtabs .home-tab{ min-height:44px !important; min-width:44px !important;'));

/* ---------- D 頒獎舞台 ---------- */
ok('D1 窄屏 frame scale', html.includes('@media (max-width:480px){ .awd62-frame{transform:scale(1.06);transform-origin:top center} }'));
ok('D2 stage overflow-x hidden', html.includes('.awd62-stage{overflow-x:hidden;'));

/* ---------- E 落敗差額提示 ---------- */
ok('E1 GapBand 近', awards379GapBand(0.84) === '今次只差一線。', awards379GapBand(0.84));
ok('E2 GapBand 中', awards379GapBand(0.75) === '今次差一截。', awards379GapBand(0.75));
ok('E3 GapBand 遠', awards379GapBand(0.60) === '今次距離得獎還有一段路。', awards379GapBand(0.60));
const hintE = awards62WeakHint({ primaryTrack: 'fame', normPrimary: 0.9, worksScore: 0.5, worksCount: 3, repIsLead65: true }, {});
ok('E4 WeakHint 非空', typeof hintE === 'string' && hintE.indexOf('差啲咩') === 0, hintE);
ok('E5 nominated 接線', html.includes('weakHint62: (scored.outcome==="nominated" && scored.parts) ? (awards62WeakHint(scored.parts, cat) + awards379GapBand(scored.score)) : ""'));

console.log(fails === 0 ? 'ALL PASS' : ('FAILS: ' + fails));
process.exit(fails === 0 ? 0 : 1);
