// v395：殺青「最後一 take」小遊戲 prototype — 邏輯測試（純函數）。
// 抽 minigame395.js 入面 PURE 395 段出嚟 eval，驗判定窗／長音閾值／allowlist／
// 直接入口參數／輪換。用法：node tests/test_v395_logic.js
const fs = require('fs');
const path = require('path');
const rootDir = path.join(__dirname, '..');
const js = fs.readFileSync(path.join(rootDir, 'minigame395.js'), 'utf8');

let pass = 0, fail = 0;
function ok(name, cond){
  if(cond){ pass++; console.log('  ok - ' + name); }
  else { fail++; console.log('  FAIL - ' + name); }
}

const b = js.indexOf('/* ===== PURE 395 BEGIN');
const e = js.indexOf('/* ===== PURE 395 END');
if(b < 0 || e < 0 || e <= b) throw new Error('PURE 395 block not found');
const pure = js.slice(b, e);
eval(pure); /* 拎到 minigame395Judge／minigame395HoldDone／minigame395Eligible／minigame395ParamFromSearch／minigame395PickKind／MINIGAME395_ALLOWLIST */

// ---- (1) 判定窗：完美 ±80／良好 ±80–250／普通 ±250–500／失手 >500 ----
ok('judge 0 → perfect', minigame395Judge(0) === 'perfect');
ok('judge 80 → perfect', minigame395Judge(80) === 'perfect');
ok('judge -80 → perfect', minigame395Judge(-80) === 'perfect');
ok('judge 81 → good', minigame395Judge(81) === 'good');
ok('judge 250 → good', minigame395Judge(250) === 'good');
ok('judge -250 → good', minigame395Judge(-250) === 'good');
ok('judge 251 → ok', minigame395Judge(251) === 'ok');
ok('judge 500 → ok', minigame395Judge(500) === 'ok');
ok('judge 501 → miss', minigame395Judge(501) === 'miss');
ok('judge 1000 → miss', minigame395Judge(1000) === 'miss');
ok('judge -1000 → miss', minigame395Judge(-1000) === 'miss');

// ---- (2) 長音：按住 ≥80% 先算完成 ----
ok('hold 800/1000 → done', minigame395HoldDone(800, 1000) === true);
ok('hold 799/1000 → not done', minigame395HoldDone(799, 1000) === false);
ok('hold 0/1000 → not done', minigame395HoldDone(0, 1000) === false);
ok('hold 1600/1600 → done', minigame395HoldDone(1600, 1600) === true);
ok('hold 1280/1600 → done', minigame395HoldDone(1280, 1600) === true);
ok('hold 1279/1600 → not done', minigame395HoldDone(1279, 1600) === false);
ok('hold total 0 → not done', minigame395HoldDone(100, 0) === false);

// ---- (3) allowlist：只得 3 張，唔包主線／其他年份 ----
ok('allowlist 係 3 張', MINIGAME395_ALLOWLIST.length === 3);
ok('allowlist 有 204', MINIGAME395_ALLOWLIST.indexOf('gig_1990_film_204') >= 0);
ok('allowlist 有 205', MINIGAME395_ALLOWLIST.indexOf('gig_1990_film_205') >= 0);
ok('allowlist 有 206', MINIGAME395_ALLOWLIST.indexOf('gig_1990_film_206') >= 0);
ok('eligible 204', minigame395Eligible('gig_1990_film_204') === true);
ok('eligible 205', minigame395Eligible('gig_1990_film_205') === true);
ok('eligible 206', minigame395Eligible('gig_1990_film_206') === true);
ok('唔 eligible：其他 1990 電影 104', minigame395Eligible('gig_1990_film_104') === false);
ok('唔 eligible：1991 臨記 203', minigame395Eligible('gig_1991_film_203') === false);
ok('唔 eligible：主線 gig_1991_tv_203', minigame395Eligible('gig_1991_tv_203') === false);
ok('唔 eligible：空字串', minigame395Eligible('') === false);
ok('唔 eligible：null', minigame395Eligible(null) === false);

// ---- (4) 直接試玩入口參數 ----
ok('param ?minigame=cue → cue', minigame395ParamFromSearch('?minigame=cue') === 'cue');
ok('param ?minigame=rhythm → rhythm', minigame395ParamFromSearch('?minigame=rhythm') === 'rhythm');
ok('param 無 minigame → null', minigame395ParamFromSearch('?v=20a10&softBehaviorGate=1') === null);
ok('param bogus → null', minigame395ParamFromSearch('?minigame=bogus') === null);
ok('param 空 → null', minigame395ParamFromSearch('') === null);

// ---- (5) 殺青輪換：cue → rhythm → cue ----
ok('pickKind 第 1 單 → cue', minigame395PickKind('gig_1990_film_204') === 'cue');
ok('pickKind 第 2 單 → rhythm', minigame395PickKind('gig_1990_film_205') === 'rhythm');
ok('pickKind 第 3 單 → cue', minigame395PickKind('gig_1990_film_206') === 'cue');

console.log(`v395 logic: ${pass} passed, ${fail} failed`);
if(fail) process.exit(1);
