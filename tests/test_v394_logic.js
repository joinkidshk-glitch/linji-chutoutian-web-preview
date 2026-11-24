// v20a394：E0 浮沉未定加入 1992 floor 豁免（ending361FloorExempt）。
// 背景：E0 係「以上皆不合」預設格，低名望＋低投入（fame≤40 且活動 ≤2 宗）
// 嘅 dual 上限約 124，結構上到唔到 1992 floor 140；唔豁免就永遠被 E7 蓋過，
// 19 格得 18 格可達。豁免只影響最後嗰個計算，唔影響中途破產／年尾評核唔合格
// 嘅提早收場，亦唔郁其他結局條件。
// 用法：node tests/test_v394_logic.js
const fs = require('fs');
const path = require('path');
const rootDir = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(rootDir, 'index.html'), 'utf8');

let pass = 0, fail = 0;
function ok(name, cond){
  if(cond){ pass++; console.log('  ok - ' + name); }
  else { fail++; console.log('  FAIL - ' + name); }
}

function extractFn(decl){
  const i = html.indexOf(decl);
  if(i<0) throw new Error('fn not found: '+decl);
  let j = html.indexOf('{', i), depth = 0, k = j;
  for(; k<html.length; k++){
    if(html[k]==='{') depth++;
    else if(html[k]==='}'){ depth--; if(depth===0){ k++; break; } }
  }
  return html.slice(i, k);
}
function extractConst(decl){
  const i = html.indexOf(decl);
  if(i<0) throw new Error('const not found: '+decl);
  let j = html.indexOf('{', i), depth = 0, k = j;
  for(; k<html.length; k++){
    if(html[k]==='{') depth++;
    else if(html[k]==='}'){ depth--; if(depth===0){ k++; break; } }
  }
  return html.slice(i, k) + ';';
}
function safeExtractFn(decl, stub){
  try{ return extractFn(decl); }catch(_e){ return stub; }
}

/* ---- 共用 stub（同 test_r345_fullarc_fix.js F2 段一致） ---- */
var S = null;
var _modalCalls = [];
var modal = function(h, btns, opts){ _modalCalls.push(String(h||'')); };
var saveQ = function(){};
var document = { getElementById: function(){ return { classList: { contains: function(){ return false; } } }; } };
var ending78Locked = function(){ return false; };
var _realSetTimeout = setTimeout;
global.setTimeout = function(fn){ fn(); return 0; };
var calib60YearOfWeek = function(w){ return w<=52?1990:(w<=104?1991:1992); };
var livingCostEstimate = function(){ return 2400; };
var shootRemain = function(){ return 0; };
var weekNumNow = function(){ return 154; };

var _stubRes = null;
var resolveEnding410 = function(){ return JSON.parse(JSON.stringify(_stubRes)); };
var endingFavor410 = function(){ return {}; };
var endingInserts410 = function(){ return []; };
var endingCareerScene410 = function(rec){ return 'SCENE:' + rec.career + '/' + (rec.careerVariant||''); };
var endingRomanceScene410 = function(){ return ''; };
var endingExodusScene410 = function(){ return ''; };
var endingEsc410 = function(x){ return String(x==null?'':x); };
var showEndingSummary410 = function(){};

eval(safeExtractFn('function ending361FloorExempt(career)', 'function ending361FloorExempt(career){ return career==="E6"; }'));
eval(extractFn('function ending410ResolvePresent410(node, choice, result, key, opts)'));
eval(extractConst('const CONSEQ61_REVIEWS = {').replace('const CONSEQ61_REVIEWS', 'var CONSEQ61_REVIEWS'));
ok('harness: ending361FloorExempt 載入', typeof ending361FloorExempt === 'function');
ok('harness: ending410ResolvePresent410 載入', typeof ending410ResolvePresent410 === 'function');
ok('harness: CONSEQ61_REVIEWS 1992 floor 140 不變', CONSEQ61_REVIEWS[1992].floor === 140);

/* ---- 豁免名單 ---- */
ok('v394: E0 豁免', ending361FloorExempt('E0') === true);
ok('v394: E6 豁免不變', ending361FloorExempt('E6') === true);
ok('v394: E4 豁免不變', ending361FloorExempt('E4') === true);
ok('v394: E3 豁免不變', ending361FloorExempt('E3') === true);
ok('v394: E5 豁免不變', ending361FloorExempt('E5') === true);
ok('v394: E2 唔豁免', ending361FloorExempt('E2') === false);
ok('v394: E1 唔豁免', ending361FloorExempt('E1') === false);
ok('v394: SS 唔豁免', ending361FloorExempt('SS') === false);
ok('v394: FK 唔豁免', ending361FloorExempt('FK') === false);

/* ---- ending410ResolvePresent410 真跑 ---- */
function mkState(fame, credit, dayIndex){
  return { fame: fame, industryCredit: credit, money: 5000, stress: 30, stamina: 100,
    dayIndex: dayIndex, weekEarn: 0, weekGigsDone: 1, weekTrainDone: 0,
    flags: {}, shoots: [], conseq61: null, ending410: null };
}
function mkRes(career, dual, exodus){
  return { career: career, careerVariant: '', gaps95: ['gap-line'],
    romance: { line: null, kind: 'solo', rel: 0 }, exodus: exodus || 'stay',
    title: '原判定・留下來的人',
    snapshot: { fame: Math.floor(dual/2), credit: dual - Math.floor(dual/2), dual: dual,
      settled: 0, creditsHeld: 0, exodusNames: [] } };
}

/* v393 實證個案：閒置路線 fame 36／credit 40／dual 76，舊行為改判 E7 */
S = mkState(36, 40, 1070); S.ending410 = null;
_stubRes = mkRes('E0', 76);
_modalCalls = [];
ending410ResolvePresent410(null, null, null, 'natural', { exodus: 'stay' });
ok('v394: E0 dual 76（v393 閒置個案）留 E0，唔改判 E7', S.ending410.career === 'E0');
ok('v394: E0 dual 76 唔寫 earlyEnd', !S.ending410.earlyEnd);
ok('v394: E0 dual 76 gaps95 保留（唔係 E7 清走）', Array.isArray(S.ending410.gaps95) && S.ending410.gaps95.length === 1);
ok('v394: E0 dual 76 場景行 E0', _modalCalls.some(h=>h.includes('SCENE:E0/')));

S = mkState(50, 50, 1070); S.ending410 = null;
_stubRes = mkRes('E0', 139);
ending410ResolvePresent410(null, null, null, 'natural', { exodus: 'stay' });
ok('v394: E0 dual 139（差 1）留 E0', S.ending410.career === 'E0');

S = mkState(80, 75, 1070); S.ending410 = null;
_stubRes = mkRes('E0', 140);
ending410ResolvePresent410(null, null, null, 'natural', { exodus: 'stay' });
ok('v394: E0 dual 140 照舊 E0', S.ending410.career === 'E0');

/* E7 兜底未受影響：非豁免格低 dual 照舊改判 */
S = mkState(50, 50, 1070); S.ending410 = null;
_stubRes = mkRes('E2', 100);
_modalCalls = [];
ending410ResolvePresent410(null, null, null, 'natural', { exodus: 'stay' });
ok('v394: E2 dual 100 <140 照舊改判 E7', S.ending410.career === 'E7');
ok('v394: E2 dual 100 variant review1992', S.ending410.careerVariant === 'review1992');
ok('v394: E2 dual 100 寫 earlyEnd review 1992 floor 140', !!(S.ending410.earlyEnd && S.ending410.earlyEnd.kind==='review' && S.ending410.earlyEnd.year===1992 && S.ending410.earlyEnd.floor===140));

S = mkState(100, 100, 1070); S.ending410 = null;
_stubRes = mkRes('E2', 200);
ending410ResolvePresent410(null, null, null, 'natural', { exodus: 'stay' });
ok('v394: E2 dual 200 ≥140 照舊 E2', S.ending410.career === 'E2');
ok('v394: E2 dual 200 唔寫 earlyEnd', !S.ending410.earlyEnd);

/* 舊豁免格回歸 */
S = mkState(27, 56, 1070); S.ending410 = null;
_stubRes = mkRes('E4', 83);
_stubRes.careerVariant = 'sunk';
ending410ResolvePresent410(null, null, null, 'natural', { exodus: 'stay' });
ok('v394: E4 dual 83 豁免不變', S.ending410.career === 'E4');

console.log(pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
