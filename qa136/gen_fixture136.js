// 由現行 index.html 重新生成 wf1_80 回歸 fixture（v136 版）。
// 形狀同 v79 fixture 一致：{ id: { beatLines: [[...],...], choices: [{id,label,effects,resultLines}], flags_written: [...] } }
// 只喺意圖改動文案之後先跑；生成後即跑 test_wf1_80_logic.js 核實。
// 用法：node qa136/gen_fixture136.js
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
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
const T89 = extractConst('STORY_SPINE_NODES_1989');
const T90 = extractConst('STORY_SPINE_NODES_1990');
const TC6 = extractConst('STORY_SPINE_NODES_C6');
const C17N = extractConst('STORY_SPINE_NODE_C17_410');
const WF1 = extractConst('STORY_SPINE_NODES_WF1');
const NODES = Object.assign({}, T89, T90, TC6, { C17: C17N }, WF1);
const IDS = ['C6','C7','C11','C8','C9','C10','C15','C14','C12','C16','C13','C17'];
const out = {};
for(const id of IDS){
  const n = NODES[id];
  if(!n) throw new Error('node missing: ' + id);
  out[id] = {
    beatLines: (n.beats || []).map(b => b.lines || []),
    choices: (n.choices || []).map(c => ({
      id: c.id, label: c.label, effects: c.effects || {},
      resultLines: (c.resultBeats || []).map(b => b.lines || []),
    })),
    flags_written: n.flags_written || [],
  };
}
const target = path.join(__dirname, '..', 'tests', 'fixtures', 'spine_c6_c17_v136.json');
fs.writeFileSync(target, JSON.stringify(out, null, 2) + '\n', 'utf8');
console.log('wrote', target);
