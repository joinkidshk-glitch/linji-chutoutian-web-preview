// v398：第六輪 UI 檢視頭五項必修 — 邏輯測試（純函數＋夾實 stub＋相片裁剪＋重複句）。
// 抽 index.html 入面 v398 段出嚟 eval，驗可見帶夾實／cropBanner／TUT_MAP 唔重複。
// 用法：node tests/test_v398_logic.js
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

// ---- (2) 可見帶夾實：clampMapLabels397（fake document；沿用 v397 harness） ----
eval(extractFn(src, 'function clampMapLabels397(){'));
function makeStage(top, bottom){
  return { getBoundingClientRect: () => ({ top, bottom, left: 0, right: 390, width: 390, height: bottom - top }) };
}
function makeRectEl(top, bottom){
  return { offsetParent: {}, getBoundingClientRect: () => ({ top, bottom, left: 0, right: 390, width: 390, height: bottom - top }) };
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
function withDoc(stage, labels, fn, extra){
  const save = (typeof document !== 'undefined') ? global.document : undefined;
  const polar = (extra && extra.polar) || null;
  const hint = (extra && extra.hint) || null;
  global.document = {
    querySelector: () => stage,
    getElementById: (id) => (id === 'map-polaroid' ? polar : (id === 'map-hint' ? hint : null)),
    querySelectorAll: () => labels,
  };
  try{ return fn(); } finally { if(save === undefined) delete global.document; else global.document = save; }
}
{
  // 冇 polaroid／hint（fake doc 舊制）：跌返舞台界，v397 行為唔變。
  const stage = makeStage(0, 600);
  const c = makeLabel(100, 590, 60, 20);
  withDoc(stage, [c, makeLabel(200, 100, 60, 18)], () => clampMapLabels397());
  ok('clamp 冇 polaroid：底邊出舞台夾返入嚟（底 ≤ 596）', c.getBoundingClientRect().bottom <= 596);
  // 頂邊出舞台頂：向下夾返入嚟（頂 ≥ 2）。
  const d = makeLabel(100, -10, 60, 18);
  withDoc(stage, [d, makeLabel(200, 100, 60, 18)], () => clampMapLabels397());
  ok('clamp 頂邊出界向下夾返入嚟（頂 ≥ 2）', d.getBoundingClientRect().top >= 2);
  // 有 polaroid（100–500）＋日卡（頂 520）：可見帶 102–496。
  const stage2 = makeStage(0, 600);
  const polar = makeRectEl(100, 500), hint = makeRectEl(520, 640);
  const e = makeLabel(100, 590, 60, 20); // 底 610，遠出可見帶
  withDoc(stage2, [e, makeLabel(200, 200, 60, 18)], () => clampMapLabels397(), { polar, hint });
  ok('clamp 可見帶：底邊出 polaroid／日卡夾返入嚟（底 ≤ 496）', e.getBoundingClientRect().bottom <= 496);
  const f = makeLabel(100, 50, 60, 18); // 頂 50，高過可見帶頂 102
  withDoc(stage2, [f, makeLabel(200, 200, 60, 18)], () => clampMapLabels397(), { polar, hint });
  ok('clamp 可見帶：頂邊出 polaroid 頂向下夾返入嚟（頂 ≥ 102）', f.getBoundingClientRect().top >= 102);
  const g = makeLabel(100, 300, 60, 18); // 帶內，唔郁
  withDoc(stage2, [g, makeLabel(200, 200, 60, 18)], () => clampMapLabels397(), { polar, hint });
  ok('clamp 可見帶：帶內標籤唔郁', g.getBoundingClientRect().top === 300 && g.style.top === '300px');
}

// ---- (3) 35c 相片橫額：np214AwardPhoto214 cropBanner ----
const awards63FocusCat = () => null;
const awardWinner149 = () => null;
const NEWS82_IMGS = {};
const NP214_AWARD_PHOTOS_214 = {
  np214_award_awi: 'assets/story/newspaper/photo_awi_ceremony.webp',
  np214_award_lok: 'assets/story/newspaper/photo_lok_ceremony.webp',
};
eval(extractFn(src, 'function np214AwardPhoto214('));
{
  const ad = np214AwardPhoto214({ displayName: '維港街招・年度廣告賞', bestOutcome: 'nominated', repWork62: '新春團圓' });
  ok('35c 廣告賞：cropBanner=true（相頂金碟夜橫額要裁走）', !!ad && ad.cropBanner === true);
  ok('35c 廣告賞：圖說照舊講廣告賞（唔改文案）',
     !!ad && ad.caption.indexOf('維港街招・年度廣告賞') >= 0 && ad.caption.indexOf('新春團圓') >= 0);
  const music = np214AwardPhoto214({ displayName: '星河金碟夜', bestOutcome: 'nominated', repWork62: '冬暖' });
  ok('35c 金碟夜：cropBanner=false（橫額本身對口，唔裁）', !!music && music.cropBanner === false);
  const adAfter = np214AwardPhoto214({ displayName: '維港街招・年度廣告賞', bestOutcome: 'nominated', repWork62: '新春團圓' }, { aftermath: true });
  ok('35c 廣告賞散場版：一樣裁橫額', !!adAfter && adAfter.cropBanner === true);
}

// ---- (1) TUT_MAP 重複句：rom183ApplyLineOverrides ----
const ROM183_PACK_GREET = {};
const NPC_LINES = {};
let TUTORIAL = { steps: [
  { id: 'TUT_MAP', body: ['第一句', '第二句'], bodyAlt: ['甲', '乙'] },
  { id: 'TUT_NPC', body: ['a', 'b'], bodyAlt: ['c', 'd'] },
] };
eval(extractFn(src, 'function rom183ApplyLineOverrides(){'));
{
  rom183ApplyLineOverrides();
  const mapStep = TUTORIAL.steps[0];
  const countIn = (arr) => (arr.join('').match(/去他們常出沒的地方/g) || []).length;
  ok('TUT_MAP：巧遇句只出一次（body 內 1 次，bodyAlt 0 次）',
     countIn(mapStep.body) === 1 && countIn(mapStep.bodyAlt) === 0);
  ok('TUT_MAP：原有兩行唔郁，巧遇句黐喺尾（body 長 3）',
     mapStep.body.length === 3 && mapStep.body[0] === '第一句' && mapStep.body[1] === '第二句');
  const npcStep = TUTORIAL.steps[1];
  ok('TUT_NPC：照舊經 body／bodyAlt loop（兩邊各 1 次，唔受 TUT_MAP 修正影響）',
     countIn(npcStep.body) === 1 && countIn(npcStep.bodyAlt) === 1);
  // 冪等：再行一次唔會再加。
  rom183ApplyLineOverrides();
  ok('重複行一次：TUT_MAP 巧遇句仍然只係 1 次', countIn(TUTORIAL.steps[0].body) === 1);
}

console.log(pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
