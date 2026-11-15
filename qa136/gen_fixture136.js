// 由現行 content/story_detail_n1_to_n17.json 重新生成 wf1_80 回歸 fixture（v136 版）。
// v20a234：內嵌覆寫表已刪，節點由 JSON pack 讀。
// 形狀同 v79 fixture 一致：{ id: { beatLines: [[...],...], choices: [{id,label,effects,resultLines}], flags_written: [...] } }
// 只喺意圖改動文案之後先跑；生成後即跑 test_wf1_80_logic.js 核實。
// 用法：node qa136/gen_fixture136.js
const fs = require('fs');
const path = require('path');
const pack = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'content', 'story_detail_n1_to_n17.json'), 'utf8'));
const NODES = {};
(pack.nodes || []).forEach(n => { if (n && n.id) NODES[n.id] = n; });
const IDS = ['N6','N7','N8','N9','N10','N11','N12','N13','N14','N15','N16','N17'];
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
