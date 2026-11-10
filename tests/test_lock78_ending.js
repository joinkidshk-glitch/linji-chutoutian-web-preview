// v20a78 LOCK78 邏輯＋接線測試：結局鎖定。
// 背景（全弧驗證第三輪實證）：E1／E7 出完結局總結之後遊戲返回可玩狀態——
// 日子繼續行、數值繼續變（正常弧 +10 日 fame 181→190；高壓弧 +42 日再病倒）。
// 本包修法：S.ending410 存在＝已結局；advanceDay 硬閘＋各主循環入口 ending78Gate；
// 手帳唯讀；總結頁出口只剩回顧／新局／讀檔；已結局存檔載入即鎖（contFromSlot）。
// (1) ending78Locked 判定：冇 ending410 → false；有 → true；S 唔存在 → false。
// (2) advanceDay 行為：未結局照翻日；已結局 return false 且 dayIndex 唔郁。
// (3) ending78Gate 行為：已結局 → true＋出總結；未結局 → false＋唔出。
// (4) 接線（靜態）：goToMapForBrowse／resolvePlannedDay／endBrowseDayGoHome／
//     commitPlanAndGo／openLoc 有 ending78Gate；enterHome 強制 editable=false；
//     contFromSlot 有已結局分支；StoryPlay.start 有鎖閘；tickDay 有硬閘。
// (5) 總結頁出口：showEndingSummary410 已結局時出「回顧手帳／開新一局／讀檔」；
//     舊文案「遊戲唔鎖檔」「照樣可以繼續跑通告過日子」全檔清零。
// (6) 紀律：SAVE key／softRev／?v= 不變；resolveEnding410 判定函數仍在（冇改判定）。
// 反證：對 v20a77 index 行 → ending78Locked／ending78Gate 唔存在 → FAIL。
// 用法：node tests/test_lock78_ending.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) throw new Error('fn not found: '+name);
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){
    if(html[j]==='{') depth++;
    else if(html[j]==='}'){ depth--; if(depth===0) break; }
  }
  return html.slice(i, j+1);
}
function fnSeg(name){ try{ return extractFn(name); }catch(_e){ return ''; } }

/* ---- 世界 stub ---- */
var window = {};
var S = null;
var _weekAccel = false, _weekAccelBuf = [];
var summaryShown = 0;
function showEndingSummary410(){ summaryShown++; }
function refreshNpc(){}
function syncGigsForCalendarYear(){}
function ensureEntryTierBoardFill(){}
function pinSoftBridgeOnBoard(){}
function gigsForLocSeasonBoard(){ return []; }
function favorDueTick(){}
function rivalryTick(){}
function exodusFenTick(){}
function story46SettleTick(){}
function story48SettleTick(){}
function ensureFamilyHomeDebt(){}
function conseq61DailyTick(){}
var LOCS = [];

let booted = true;
try{
  eval(extractFn('weekdayIdx'));
  eval(extractFn('ending78Locked'));
  eval(extractFn('ending78Gate'));
  eval(extractFn('advanceDay'));
}catch(e){
  booted = false;
  ok('LOCK78 函數存在（ending78Locked／ending78Gate／advanceDay 可抽出）', false);
  console.log('  extract error: '+e.message);
}

if(booted){
  /* (1) ending78Locked 判定 */
  S = { dayIndex: 10 };
  ok('未結局（冇 ending410）→ 未鎖', ending78Locked() === false);
  S = { dayIndex: 746, ending410: { career: 'E1' } };
  ok('已結局 E1 → 鎖', ending78Locked() === true);
  S = { dayIndex: 98, ending410: { career: 'E7' } };
  ok('已結局 E7 → 鎖', ending78Locked() === true);
  ok('傳入 state 判定（E6）', ending78Locked({ ending410: { career: 'E6' } }) === true);
  ok('傳入空 state → 未鎖', ending78Locked({}) === false);
  S = null;
  ok('S 唔存在 → 未鎖（唔 crash）', ending78Locked() === false);

  /* (2) advanceDay 行為 */
  S = { dayIndex: 100, board: {}, flags: {} };
  const r1 = advanceDay();
  ok('未結局：advanceDay 照翻日 100→101', S.dayIndex === 101 && r1 === false);
  S.ending410 = { career: 'E7', day: 101 };
  const before = S.dayIndex;
  const r2 = advanceDay();
  ok('已結局：advanceDay return false', r2 === false);
  ok('已結局：dayIndex 唔郁（日子唔再行）', S.dayIndex === before);
  advanceDay(); advanceDay();
  ok('已結局：重複呼叫都唔翻日', S.dayIndex === before);

  /* (3) ending78Gate 行為 */
  summaryShown = 0;
  ok('已結局：gate 擋（return true）', ending78Gate() === true);
  ok('已結局：gate 有出結局總結', summaryShown === 1);
  S = { dayIndex: 5 };
  ok('未結局：gate 放行（return false）', ending78Gate() === false);
  ok('未結局：gate 唔出總結', summaryShown === 1);
}

/* (4) 接線（靜態） */
const advSrc = fnSeg('advanceDay');
ok('advanceDay：LOCK78 硬閘喺 dayIndex += 1 之前',
  advSrc.indexOf('ending78Locked') >= 0 && advSrc.indexOf('ending78Locked') < advSrc.indexOf('S.dayIndex += 1'));
ok('tickDay：有 LOCK78 硬閘', fnSeg('tickDay').includes('ending78Locked'));
ok('goToMapForBrowse：有 ending78Gate', fnSeg('goToMapForBrowse').includes('ending78Gate()'));
ok('resolvePlannedDay：有 ending78Gate', fnSeg('resolvePlannedDay').includes('ending78Gate()'));
ok('endBrowseDayGoHome：有 ending78Gate', fnSeg('endBrowseDayGoHome').includes('ending78Gate()'));
ok('commitPlanAndGo：有 ending78Gate', fnSeg('commitPlanAndGo').includes('ending78Gate()'));
ok('openLoc：有 ending78Gate', fnSeg('openLoc').includes('ending78Gate()'));
ok('book70ExitHome（手帳恆常出口）：有 ending78Gate', fnSeg('book70ExitHome').includes('ending78Gate()'));
ok('leaveHomeFromNotebook：有 ending78Gate', fnSeg('leaveHomeFromNotebook').includes('ending78Gate()'));
const ehSrc = fnSeg('enterHome');
ok('enterHome：已結局強制 editable=false', ehSrc.includes('ending78Locked') && ehSrc.includes('editable = false'));
const cfSrc = fnSeg('contFromSlot');
ok('contFromSlot：已結局存檔載入分支（ending78Locked＋showEndingSummary410）',
  cfSrc.includes('ending78Locked') && cfSrc.includes('showEndingSummary410'));
const spStart = (()=>{ const i = html.indexOf('function start(idOrNode, opts)'); return i<0 ? '' : html.slice(i, i+4000); })();
ok('StoryPlay.start：有 LOCK78 閘', spStart.includes('ending78Locked'));

/* (5) 總結頁出口＋舊文案清零 */
const showSrc = fnSeg('showEndingSummary410');
ok('showEndingSummary410：已結局出口有「回顧手帳」', showSrc.includes('回顧手帳'));
ok('showEndingSummary410：已結局出口有「開新一局」', showSrc.includes('開新一局'));
ok('showEndingSummary410：已結局出口有「讀檔」', showSrc.includes('讀檔'));
ok('全檔冇「遊戲唔鎖檔」舊文案', !html.includes('遊戲唔鎖檔'));
ok('全檔冇「照樣可以繼續跑通告過日子」舊文案', !html.includes('照樣可以繼續跑通告過日子'));

/* (6) 紀律 */
ok('SAVE key 不變', html.includes('starVolunteer_map_v19w'));
ok('softRev 不變', html.includes('s107'));
ok('?v= 不變', html.includes('v20a10'));
ok('resolveEnding410 判定函數仍在（冇改判定）', fnSeg('resolveEnding410').length > 100);

console.log(fails.length ? ('\nFAILED: '+fails.length) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
