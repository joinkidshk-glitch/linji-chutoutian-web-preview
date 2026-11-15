// v20a210 C2N210 邏輯測試：舊存檔章節進度 C id→N id 遷移。
//   (1) 真 c2n210MigrateSave——舊存檔播種（done 裸鍵 C5／C8／C11／C6F、lastMainDoneId C5、
//       calib60Missed C9、flags done_C10／story_C10／done_C11）經遷移後全部對照做 N 鍵，舊 C 鍵全清；
//   (2) 換位對（C8→N9／C11→N8）唔會互撞；新舊鍵並存嗰陣 OR 合併；
//   (3) 非章節鍵唔郁（C20、done_tv_01 通告旗、R_ 前綴）；冪等（跑兩次同一結果）；空物件／null 唔拋錯；
//   (4) 靜態：normalizeSaveObj 入面呼叫次序 levels75MigrateSave → c2n210MigrateSave →
//       storyGate113Scrub → calib60MissedScan（遷移必須喺嗰兩個讀 N id 嘅函數之前）。
// 反證：喺 v20a227 index 上行會 FAIL（冇 c2n210MigrateSave、normalizeSaveObj 冇呼叫）。
// 用法：node tests/test_story210_migrate_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }
function extractFn(name){
  const i = html.indexOf('function ' + name + '(');
  if(i < 0) throw new Error('fn not found: ' + name);
  let depth = 0, j = html.indexOf('{', i);
  for(; j < html.length; j++){
    if(html[j] === '{') depth++;
    else if(html[j] === '}'){ depth--; if(depth === 0) break; }
  }
  return html.slice(i, j + 1);
}
eval(extractFn('c2n210MigrateSave'));
const normSrc = extractFn('normalizeSaveObj');

/* ================= (1) 舊存檔播種 → 遷移後對照 ================= */
const oldSave = {
  story: {
    done: { C1: true, C5: true, C8: true, C11: true, C6F: true },
    lastMainDoneId: 'C5'
  },
  calib60Missed: { C9: 2 },
  flags: { done_C10: true, story_C10: 'x', done_C11: true, done_C6F: true, done_tv_01: true }
};
c2n210MigrateSave(oldSave);
ok('done：C1→N1、C5→N5、C8→N9、C11→N8、C6F→N6F 全部在位',
  oldSave.story.done.N1 === true && oldSave.story.done.N5 === true &&
  oldSave.story.done.N9 === true && oldSave.story.done.N8 === true &&
  oldSave.story.done.N6F === true);
ok('done：舊 C 鍵全清（C1／C5／C8／C11／C6F 全部唔見）',
  !('C1' in oldSave.story.done) && !('C5' in oldSave.story.done) &&
  !('C8' in oldSave.story.done) && !('C11' in oldSave.story.done) &&
  !('C6F' in oldSave.story.done));
ok('lastMainDoneId：C5→N5', oldSave.story.lastMainDoneId === 'N5');
ok('calib60Missed：C9→N10（值保留）',
  oldSave.calib60Missed.N10 === 2 && !('C9' in oldSave.calib60Missed));
ok('flags：done_C10→done_N11、story_C10→story_N11、done_C11→done_N8、done_C6F→done_N6F',
  oldSave.flags.done_N11 === true && oldSave.flags.story_N11 === 'x' &&
  oldSave.flags.done_N8 === true && oldSave.flags.done_N6F === true &&
  !('done_C10' in oldSave.flags) && !('story_C10' in oldSave.flags) &&
  !('done_C11' in oldSave.flags) && !('done_C6F' in oldSave.flags));

/* ================= (2) 換位對唔互撞；OR 合併 ================= */
const swapSave = { story: { done: { C8: true, C11: true }, lastMainDoneId: 'C11' } };
c2n210MigrateSave(swapSave);
ok('換位對：C8＋C11 同時在場 → N9＋N8 各自 true，唔會撞值',
  swapSave.story.done.N9 === true && swapSave.story.done.N8 === true &&
  Object.keys(swapSave.story.done).length === 2 && swapSave.story.lastMainDoneId === 'N8');
const mergeSave = { story: { done: { C8: true, N9: true, C5: false }, lastMainDoneId: 'C8' } };
c2n210MigrateSave(mergeSave);
ok('OR 合併：C8＋已存在嘅 N9 → N9 保持 true、C8 清走；C5 false 照搬做 N5 false',
  mergeSave.story.done.N9 === true && !('C8' in mergeSave.story.done) &&
  mergeSave.story.done.N5 === false && !('C5' in mergeSave.story.done));

/* ================= (3) 非章節鍵唔郁；冪等；空物件唔拋錯 ================= */
const keepSave = {
  story: { done: { C20: true, C1x: true, R_foo: true, N5: true }, lastMainDoneId: 'N5' },
  flags: { done_tv_01: true, done_C20: true }
};
c2n210MigrateSave(keepSave);
ok('非章節鍵唔郁：C20／C1x／R_／done_C20／done_tv_01 全部原樣保留',
  keepSave.story.done.C20 === true && keepSave.story.done.C1x === true &&
  keepSave.story.done.R_foo === true && keepSave.story.done.N5 === true &&
  keepSave.flags.done_tv_01 === true && keepSave.flags.done_C20 === true);
const once = { story: { done: { C5: true, C12: true, C16: true }, lastMainDoneId: 'C16' } };
c2n210MigrateSave(once);
const afterOnce = JSON.stringify(once);
c2n210MigrateSave(once);
ok('冪等：跑第二次結果完全一樣（C12→N14／C16→N15）',
  JSON.stringify(once) === afterOnce && once.story.done.N14 === true &&
  once.story.done.N15 === true && once.story.lastMainDoneId === 'N15');
let threw = false;
try{ c2n210MigrateSave({}); c2n210MigrateSave(null); c2n210MigrateSave({ story: {} }); }catch(e){ threw = true; }
ok('空物件／null／story 空殼唔拋錯', !threw);

/* ================= (4) 靜態：normalizeSaveObj 呼叫次序 ================= */
/* 註：要用呼叫式（帶 (o)）搵——註解入面都提到 calib60MissedScan，裸名 indexOf 會搵到註解先。 */
const iLevels = normSrc.indexOf('levels75MigrateSave(o)');
const iC2n = normSrc.indexOf('c2n210MigrateSave(o)');
const iGate = normSrc.indexOf('storyGate113Scrub(o)');
const iCalib = normSrc.indexOf('calib60MissedScan(o)');
ok('normalizeSaveObj 有呼叫 c2n210MigrateSave', iC2n > 0);
ok('呼叫次序：levels75 → c2n210 → storyGate113Scrub → calib60MissedScan',
  iLevels > 0 && iC2n > iLevels && iGate > iC2n && iCalib > iC2n);

if(fails.length){ console.log('FAILURES: ' + fails.join(', ')); process.exit(1); }
console.log('ALL PASS');
