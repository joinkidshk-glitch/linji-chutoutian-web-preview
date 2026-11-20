// v345 F1＋F2 測試（full arc 實駕發現）。
// F1：年終評核警告喺連續遊玩下不可見——警告行經 pushFlavor 入 settle flavor 後
// 只存 S.weekBoundary105.html，v20a71 移除 home 結算卡後唯一渲染位係重開補呈現。
// 修法：settleWeek 另存 warnHtml（cq61 行＋class="bad" 行），enterHome 入編排步
// 嗰刻經 presentSettleWarn345 排隊彈提醒 modal（所有週結路徑都經 enterHome）。
// F2：1992 E7 正常玩法不可達——N17 閘 weekMin 153 搶先 week156 評核。
// 修法：ending410ResolvePresent410 結局判定嗰刻補 floor 檢查，dual<155 改判
// E7（review1992）；E6 主動退圈唔覆蓋；1990／1991 評核路徑唔郁。
// 用法：node tests/test_r345_fullarc_fix.js
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

/* ---- 共用 stub ---- */
var S = null;
var _modalCalls = [];
var modal = function(h, btns, opts){ _modalCalls.push(String(h||'')); };
var saveQ = function(){};
var document = { getElementById: function(){ return { classList: { contains: function(){ return false; } } }; } };
var ending78Locked = function(){ return false; };
var _realSetTimeout = setTimeout;
global.setTimeout = function(fn){ fn(); return 0; }; /* 同步跑，方便斷言 */
var calib60YearOfWeek = function(w){ return w<=52?1990:(w<=104?1991:1992); };
var livingCostEstimate = function(){ return 2400; };
var shootRemain = function(){ return 0; };
var weekNumNow = function(){ return 154; };

function safeExtractFn(decl, stub){
  try{ return extractFn(decl); }catch(_e){ return stub; }
}

eval([
  extractConst('const CONSEQ61_REVIEWS = {').replace('const CONSEQ61_REVIEWS', 'var CONSEQ61_REVIEWS'),
  extractConst('const CONSEQ61_CFG = {').replace('const CONSEQ61_CFG', 'var CONSEQ61_CFG'),
  extractFn('function conseq61State(st)'),
  extractFn('function endingDual410(st)'),
  extractFn('function conseq61DualOf(st)'),
  extractFn('function conseq61SettleEval(st, weekJustEnded, weekEarnIn)'),
  extractFn('function stripSettleMoneyNoise(html)'),
  safeExtractFn('function presentSettleWarn345(summary)', 'function presentSettleWarn345(summary){}'),
].join('\n'));

ok('harness: conseq61SettleEval 載入', typeof conseq61SettleEval === 'function');
ok('harness: presentSettleWarn345 載入', typeof presentSettleWarn345 === 'function');
ok('harness: CONSEQ61_REVIEWS 1992 floor 155', CONSEQ61_REVIEWS[1992].floor === 155);

/* ---- F1a：conseq61SettleEval 警告行生成（1991 評核前 2 週） ---- */
function mkState(fame, credit, dayIndex){
  return { fame: fame, industryCredit: credit, money: 5000, stress: 30, stamina: 100,
    dayIndex: dayIndex, weekEarn: 0, weekGigsDone: 1, weekTrainDone: 0,
    flags: {}, shoots: [], conseq61: null, ending410: null };
}
S = mkState(40, 40, 710); /* dual 80 < warnLine 130 */
let lines = conseq61SettleEval(S, 102, 0);
ok('F1a: dist=2 警告行生成', lines.some(l=>l.includes('1991 年尾事務所要做評核')));
ok('F1a: 警告行講明仲有 2 週', lines.some(l=>l.includes('仲有 2 週')));

S = mkState(40, 40, 717);
lines = conseq61SettleEval(S, 103, 0);
ok('F1a: dist=1 強警告行生成', lines.some(l=>l.includes('下週就係 1991 年尾評核')));

S = mkState(120, 80, 710); /* dual 200 ≥ warnLine */
lines = conseq61SettleEval(S, 102, 0);
ok('F1a: dual 夠高唔出評核警告', !lines.some(l=>l.includes('評核')));

/* ---- F2 回歸：1991 評核路徑唔郁 ---- */
S = mkState(40, 40, 728);
lines = conseq61SettleEval(S, 104, 0);
ok('F2回歸: 1991 評核唔過寫 pendingEnding', !!(S.conseq61 && S.conseq61.pendingEnding && S.conseq61.pendingEnding.kind==='review' && S.conseq61.pendingEnding.year===1991));
ok('F2回歸: 1991 評核唔過出結果行', lines.some(l=>l.includes('1991 年尾評核結果出咗')));

S = mkState(80, 60, 728); /* dual 140 ≥ floor 100 */
lines = conseq61SettleEval(S, 104, 0);
ok('F2回歸: 1991 評核過咗唔寫 pendingEnding', !(S.conseq61 && S.conseq61.pendingEnding));
ok('F2回歸: 1991 評核過咗出續約行', lines.some(l=>l.includes('過咗事務所條線')));

/* ---- F1b：settleWeek 真跑出 warnHtml ---- */
var livingCostRoll = function(){ return 1100; };
var apply = function(d){ if(d && typeof d.money==='number') S.money = Math.max(0,(S.money||0)+d.money); return ''; };
var eventLine = function(){ return ''; };
var b10Line = function(){ return ''; };
var bumpNpc = function(){};
var renewSoftBridgeGigs = function(){};

eval(extractFn('function settleWeek()'));
ok('harness: settleWeek 載入', typeof settleWeek === 'function');

S = mkState(40, 40, 710); /* w = floor((710-1)/7)+1 = 102 */
let summary = settleWeek();
ok('F1b: summary 有 warnHtml 欄', typeof summary.warnHtml === 'string');
ok('F1b: warnHtml 含評核警告', (summary.warnHtml||'').includes('1991 年尾事務所要做評核'));
ok('F1b: summary.html 照舊含警告（back-compat）', summary.html.includes('1991 年尾事務所要做評核'));
ok('F1b: weekBoundary105.html 照舊含警告（重開補呈現唔受影響）', String(S.weekBoundary105.html).includes('1991 年尾事務所要做評核'));

S = mkState(120, 80, 710); /* dual 200，錢夠、壓力低 → 無警告行 */
S.weekEarn = 2000; /* bal ≥0，唔觸發入不敷支警告 */
summary = settleWeek();
ok('F1b: 無警告週 warnHtml 空', (summary.warnHtml||'') === '');

/* ---- F1c：presentSettleWarn345 真跑彈 modal ---- */
_modalCalls = [];
S = mkState(40, 40, 710);
presentSettleWarn345({ warnHtml: '<div class="settle-flavor"><div class="settle-flavor-line">WARN-LINE</div></div>', weekNum: 102 });
ok('F1c: 有 warnHtml 彈提醒 modal', _modalCalls.length === 1 && (_modalCalls[0]||'').includes('WARN-LINE'));
ok('F1c: modal 標題有週數', (_modalCalls[0]||'').includes('週結算提醒 · 第 102 週'));

_modalCalls = [];
presentSettleWarn345({ warnHtml: '', weekNum: 102 });
ok('F1c: warnHtml 空唔彈', _modalCalls.length === 0);

_modalCalls = [];
presentSettleWarn345(null);
ok('F1c: summary null 唔彈', _modalCalls.length === 0);

_modalCalls = [];
S.conseq61 = { pendingEnding: { kind:'review', year:1991 } };
presentSettleWarn345({ warnHtml: '<div>WARN</div>', weekNum: 104 });
ok('F1c: 已判強制收場唔重複彈（結局呈現會交代）', _modalCalls.length === 0);
S.conseq61 = null;

/* ---- F2：ending410ResolvePresent410 floor 覆寫 ---- */
var _stubRes = null;
var resolveEnding410 = function(){ return JSON.parse(JSON.stringify(_stubRes)); };
var endingFavor410 = function(){ return {}; };
var endingInserts410 = function(){ return []; };
var endingCareerScene410 = function(rec){ return 'SCENE:' + rec.career + '/' + (rec.careerVariant||''); };
var endingRomanceScene410 = function(){ return ''; };
var endingExodusScene410 = function(){ return ''; };
var endingEsc410 = function(x){ return String(x==null?'':x); };
var showEndingSummary410 = function(){};

eval(extractFn('function ending410ResolvePresent410(node, choice, result, key, opts)'));
ok('harness: ending410ResolvePresent410 載入', typeof ending410ResolvePresent410 === 'function');

function mkRes(career, dual, exodus){
  return { career: career, careerVariant: '', gaps95: ['gap-line'],
    romance: { line: null, kind: 'solo', rel: 0 }, exodus: exodus || 'stay',
    title: '原判定・留下來的人',
    snapshot: { fame: Math.floor(dual/2), credit: dual - Math.floor(dual/2), dual: dual,
      settled: 0, creditsHeld: 0, exodusNames: [] } };
}

S = mkState(50, 50, 1070); S.ending410 = null;
_stubRes = mkRes('E2', 100);
_modalCalls = [];
ending410ResolvePresent410(null, null, null, 'natural', { exodus: 'stay' });
ok('F2: dual 100 <155 改判 E7', S.ending410.career === 'E7');
ok('F2: variant review1992', S.ending410.careerVariant === 'review1992');
ok('F2: title 未紅先收', String(S.ending410.title).startsWith('未紅先收'));
ok('F2: earlyEnd review 1992 floor 155', !!(S.ending410.earlyEnd && S.ending410.earlyEnd.kind==='review' && S.ending410.earlyEnd.year===1992 && S.ending410.earlyEnd.floor===155));
ok('F2: gaps95 清走（同強制 E7 一致）', Array.isArray(S.ending410.gaps95) && S.ending410.gaps95.length === 0);
ok('F2: 場景行 E7/review1992', _modalCalls.some(h=>h.includes('SCENE:E7/review1992')));

S = mkState(100, 100, 1070); S.ending410 = null;
_stubRes = mkRes('E2', 200);
ending410ResolvePresent410(null, null, null, 'natural', { exodus: 'stay' });
ok('F2: dual 200 ≥155 照舊 E2', S.ending410.career === 'E2');
ok('F2: dual 200 唔寫 earlyEnd', !S.ending410.earlyEnd);

S = mkState(50, 50, 1070); S.ending410 = null;
_stubRes = mkRes('E0', 154);
ending410ResolvePresent410(null, null, null, 'natural', { exodus: 'stay' });
ok('F2: dual 154（差 1）改判 E7', S.ending410.career === 'E7');

S = mkState(80, 75, 1070); S.ending410 = null;
_stubRes = mkRes('E0', 155);
ending410ResolvePresent410(null, null, null, 'natural', { exodus: 'stay' });
ok('F2: dual 155（啱啱到線）唔改判', S.ending410.career === 'E0');

S = mkState(50, 50, 1070); S.ending410 = null;
_stubRes = mkRes('E6', 100);
_stubRes.careerVariant = '安穩';
ending410ResolvePresent410(null, null, null, 'quit_job', { quit: 'job' });
ok('F2: E6 主動退圈唔覆蓋', S.ending410.career === 'E6');

/* ---- F2：E7 review1992 場景文字 ---- */
var endingFlag410 = function(){ return false; };
eval(extractFn('function endingCareerScene410(rec)'));
S = mkState(50, 50, 1070);
const scene92 = endingCareerScene410({ career: 'E7', careerVariant: 'review1992' });
ok('F2: review1992 場景出第三年年尾', scene92.includes('第三年年尾'));
ok('F2: review1992 場景唔出第一年年尾', !scene92.includes('第一年年尾'));
const scene91 = endingCareerScene410({ career: 'E7', careerVariant: 'review1991' });
ok('F2回歸: review1991 場景照舊第二年年尾', scene91.includes('第二年年尾'));

/* ---- 靜態：enterHome 接駁 ---- */
ok('F1靜態: enterHome 呼叫 presentSettleWarn345', html.includes('presentSettleWarn345(summary)'));
ok('F1靜態: settleWeek 回傳 warnHtml', html.includes('warnHtml: warnHtml345'));

global.setTimeout = _realSetTimeout;
console.log(`\nTOTAL PASS ${pass} FAIL ${fail}`);
process.exit(fail ? 1 : 0);
