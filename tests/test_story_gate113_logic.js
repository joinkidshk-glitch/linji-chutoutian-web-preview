// v20a113 主線順序閘守門測試：C18／C19 跳步修復。
//   (1) 鏈守門：全部主線幕 C1–C19（C6／C6F 路線分支可選幕除外）嘅閘必須包含已判斷設計嘅 needDone 鏈；
//       C1–C5 鏈嚟自 content stub（SANDBOX_BEHAVIOR_GATE_C1_C5_SOFT_STUB_v1.json），C6–C19 鏈嚟自 STORY_GATE_3Y；
//       C9／C13 預期係無 needDone——刻意恢復節點（防錯過窗口成條關鍵路徑軟鎖），唔係漏網，見 index 註解；
//   (2) 鏈無環＋前置存在；(3) C18 weekMin 48／C19 weekMin 61（同 pacing 章戳一致）；
//   (4) 載入遷移 storyGate113Scrub：舉報個案（第 2 週 C1 done＋C18 done）清 C18；合法完成唔誤清；
//       週數 forensic（week < weekMin）清；冪等；退化輸入唔炸。
// 反證：將閘表 copy 入面 C18／C11 嘅 needDone 刪走（模擬舊漏鏈），鏈檢查必須報違規；
//       殘廢版 scrub（乜都唔清）對舉報個案必須交白卷——證明斷言對漏鏈／失效遷移敏感。
// 用法：node tests/test_story_gate113_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }
function extractConst(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('const not found: ' + name);
  let depth = 0, started = false, j = i;
  for(; j < html.length; j++){
    const c = html[j];
    if(c === '{' || c === '['){ depth++; started = true; }
    else if(c === '}' || c === ']'){ depth--; if(started && depth === 0){ j++; break; } }
  }
  return eval('(' + html.slice(html.indexOf('=', i) + 1, j) + ')');
}
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
const GATE = extractConst('STORY_GATE_3Y');
const scrubSrc = extractFn('storyGate113Scrub');
const scrub = new Function(scrubSrc + '\nreturn storyGate113Scrub;')();
const stub = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'content', 'SANDBOX_BEHAVIOR_GATE_C1_C5_SOFT_STUB_v1.json'), 'utf8'));
const stubChain = {};
for(const n of stub.nodes) stubChain[n.beatId] = (n.trigger && n.trigger.needDone) || [];

/* 已判斷設計嘅預期鏈（v20a113；C9／C13 無 needDone 係刻意，見 index 註解＋NOTES） */
const EXPECT = {
  C1: [], C2: ['C1'], C3: ['C2'], C4: ['C3'], C5: ['C4'],
  C7: ['C5'], C8: ['C7'], C9: [], C10: ['C9'], C11: ['C7'], C12: ['C14'],
  C13: [], C14: ['C10'], C15: ['C10'], C16: ['C12'], C17: ['C13'],
  C18: ['C5'], C19: ['C18'],
};
const EXEMPT = ['C6', 'C6F']; /* 路線分支可選幕，唔當順序主幹鏈 */
function actualNeedDone(id){
  if(stubChain[id] !== undefined) return stubChain[id];
  const g = GATE[id];
  return g ? (g.needDone || []) : null;
}
function chainViolations(gate, stubMap){
  const out = [];
  const get = (id) => stubMap[id] !== undefined ? stubMap[id] : (gate[id] ? (gate[id].needDone || []) : null);
  for(const id of Object.keys(EXPECT)){
    const got = get(id);
    if(got === null){ out.push(id + ':missing'); continue; }
    if(JSON.stringify(got) !== JSON.stringify(EXPECT[id])) out.push(id + ':want ' + JSON.stringify(EXPECT[id]) + ' got ' + JSON.stringify(got));
  }
  return out;
}

/* (1) 鏈守門 */
const v = chainViolations(GATE, stubChain);
ok('全部主線幕鏈符合已判斷設計（C1–C19，C6／C6F 除外）', v.length === 0);
if(v.length) console.log('  violations: ' + v.join(' | '));
for(const id of EXEMPT){
  const g = GATE[id];
  ok(id + ' 豁免：路線分支幕（有 route＋weekMin，唔入順序鏈）', !!g && !!g.route && g.weekMin != null);
}
ok('C9 無 needDone 係刻意（恢復節點，見 index 註解）', JSON.stringify(actualNeedDone('C9')) === '[]');
ok('C13 無 needDone 係刻意（恢復節點，見 index 註解）', JSON.stringify(actualNeedDone('C13')) === '[]');

/* (2) 鏈無環＋前置存在 */
{
  const all = Object.keys(EXPECT).concat(EXEMPT);
  const missing = [];
  const cyclic = [];
  const visiting = new Set(), visited = new Set();
  function dfs(id){
    if(visited.has(id)) return;
    if(visiting.has(id)){ cyclic.push(id); return; }
    visiting.add(id);
    for(const d of (actualNeedDone(id) || [])){
      if(!all.includes(d)) missing.push(id + '→' + d);
      else dfs(d);
    }
    visiting.delete(id);
    visited.add(id);
  }
  for(const id of all) dfs(id);
  ok('全部前置都係已知主線幕', missing.length === 0);
  ok('needDone 鏈無環', cyclic.length === 0);
}

/* (3) 深冬／春窗週數 */
ok('C18 weekMin＝48（1990-12-01 第 48 週，同 pacing 章戳一致）', GATE.C18 && GATE.C18.weekMin === 48);
ok('C19 weekMin＝61（1991-03-01 春首日 第 61 週，同 pacing 章戳一致）', GATE.C19 && GATE.C19.weekMin === 61);

/* (4) 載入遷移 */
function mkSave(dayIndex, doneIds){
  const done = {};
  for(const id of doneIds) done[id] = true;
  return { dayIndex: dayIndex, story: { done: done } };
}
{
  const s = mkSave(7, ['C1', 'C18']); /* 舉報個案：第 2 週，C1 done＋C18 done */
  const cleared = scrub(s, GATE);
  ok('舉報個案：載入清走 C18（前置 C5 未做）', cleared.join() === 'C18' && !s.story.done.C18);
  ok('舉報個案：C1 唔受影響', !!s.story.done.C1);
}
{
  const s = mkSave(430, ['C1', 'C2', 'C3', 'C4', 'C5', 'C19']); /* 第 62 週，C19 done 但 C18 未做 */
  const cleared = scrub(s, GATE);
  ok('C19 無 C18 前置：載入清走 C19', cleared.join() === 'C19' && !s.story.done.C19);
}
{
  const s = mkSave(340, ['C1', 'C2', 'C3', 'C4', 'C5', 'C18']); /* 第 49 週，合法 12 月 C18 */
  ok('合法 C18（第 49 週＋C5 已做）：唔誤清', scrub(s, GATE).length === 0 && !!s.story.done.C18);
}
{
  const s = mkSave(430, ['C1', 'C2', 'C3', 'C4', 'C5', 'C18', 'C19']); /* 第 62 週，合法 C19 */
  ok('合法 C19（第 62 週＋C18 已做）：唔誤清', scrub(s, GATE).length === 0 && !!s.story.done.C19);
}
{
  const s = mkSave(140, ['C1', 'C2', 'C3', 'C4', 'C5', 'C18']); /* 第 21 週：C5 齊但週數 <48→1 月非法播出 */
  ok('週數 forensic：第 21 週 C18 done 必清（播出一定早過第 48 週）', scrub(s, GATE).join() === 'C18');
}
{
  const s = mkSave(400, ['C11']); /* C11 無 C7 前置 */
  ok('C11 無 C7 前置：載入清走 C11', scrub(s, GATE).join() === 'C11');
  const s2 = mkSave(400, ['C15']); /* C15 無 C10 前置 */
  ok('C15 無 C10 前置：載入清走 C15', scrub(s2, GATE).join() === 'C15');
}
{
  const s = mkSave(7, ['C1', 'C18']);
  scrub(s, GATE);
  ok('遷移冪等（行第二次零新增清除）', scrub(s, GATE).length === 0);
  const clean = mkSave(7, ['C1']);
  ok('乾淨舊檔：遷移零動作', scrub(clean, GATE).length === 0);
  ok('退化輸入唔炸（null／空物件／冇 story.done）', JSON.stringify(scrub(null, GATE)) === '[]' && JSON.stringify(scrub({}, GATE)) === '[]' && JSON.stringify(scrub({ story: {} }, GATE)) === '[]');
}

/* 反證 */
{
  const brokenGate = JSON.parse(JSON.stringify(GATE));
  delete brokenGate.C18.needDone; brokenGate.C18.weekMin = undefined;
  const mv = chainViolations(brokenGate, stubChain);
  ok('反證：C18 漏鏈嘅閘表必報違規', mv.some(x => x.indexOf('C18') === 0));
  const brokenGate2 = JSON.parse(JSON.stringify(GATE));
  delete brokenGate2.C11.needDone;
  ok('反證：C11 漏鏈嘅閘表必報違規', chainViolations(brokenGate2, stubChain).some(x => x.indexOf('C11') === 0));
  const brokenScrub = function(){ return []; };
  const s = mkSave(7, ['C1', 'C18']);
  ok('反證：殘廢版 scrub（乜都唔清）捉唔到舉報個案', brokenScrub(s).length === 0 && !!s.story.done.C18);
}

console.log(fails.length === 0 ? '\nALL PASS' : '\nFAILURES: ' + fails.join(' | '));
process.exit(fails.length === 0 ? 0 : 1);
