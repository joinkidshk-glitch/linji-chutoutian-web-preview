// v20a241 resync：index.html 淨 −859 行（刪 WF4 覆寫表全數＋WF2 hiu/choi/xu 15 條）。
//   WF2 表頭註解 ＋4／WF2 15 條 −650／WF4 塊（註解＋表＋WeakSet＋apply 函數）−213；
//   WF4 呼叫點 1 行換 1 行刪除註解，淨 0。總淨變 4−650−213＝−859。
// 用法：node qa241/resync241.js — 對照 4dd00ca（v241b）舊版 index.html，
// 將 77 個釘行按段映射（WF2 表前 ＋0／中段 −646／WF4 塊之後 −859），逐行核實內容逐字相同（純漂移）。
const fs = require('fs'), { execSync } = require('child_process');
const oldText = execSync('git show 4dd00ca:index.html', { cwd: __dirname + '/..', encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
const newText = fs.readFileSync(__dirname + '/../index.html', 'utf8');
const oldLines = oldText.split('\n'), newLines = newText.split('\n');
function find(lines, pred, from = 0) { for (let i = from; i < lines.length; i++) if (pred(lines[i])) return i; return -1; }
const wf2ConstOld = find(oldLines, l => l.startsWith('const ROMANCE_WF2_OVERRIDES'));
const wf2ConstNew = find(newLines, l => l.startsWith('const ROMANCE_WF2_OVERRIDES'));
function tableEnd(lines, start) { for (let i = start; i < lines.length; i++) if (lines[i] === '};') return i; return -1; }
const wf2EndOld = tableEnd(oldLines, wf2ConstOld), wf2EndNew = tableEnd(newLines, wf2ConstNew);
const WF2DEL = (wf2EndOld - wf2ConstOld) - (wf2EndNew - wf2ConstNew);
const wf4ConstOld = find(oldLines, l => l.startsWith('const RIVAL_WF4_OVERRIDES'));
let wf4BlockStart = wf4ConstOld;
for (let i = wf4ConstOld - 1; i >= wf4ConstOld - 8; i--) { if (oldLines[i].startsWith('/*')) { wf4BlockStart = i; break; } }
const wf4FnStart = find(oldLines, l => l.startsWith('function applyRivalWf4Overrides86()'));
let depth = 0, wf4FnEnd = -1;
for (let i = wf4FnStart; i < oldLines.length; i++) {
  for (const c of oldLines[i]) { if (c === '{') depth++; else if (c === '}') depth--; }
  if (i > wf4FnStart && depth === 0) { wf4FnEnd = i; break; }
}
const wf4NoteNewIdx = find(newLines, l => l.includes('RIVAL_WF4_OVERRIDES 已刪——'));
let wf4NoteEnd = wf4NoteNewIdx;
for (let i = wf4NoteNewIdx; i < newLines.length; i++) { wf4NoteEnd = i; if (newLines[i].includes('*/')) break; }
const WF4DEL = (wf4FnEnd - wf4BlockStart + 1) - (wf4NoteEnd - wf4NoteNewIdx + 1);
console.log('old lines:', oldLines.length, 'new lines:', newLines.length, 'delta:', newLines.length - oldLines.length);
console.log('WF2DEL:', WF2DEL, '| WF4DEL:', WF4DEL, '| predicted total:', 4 - WF2DEL - WF4DEL);
function shift(oldIdx) {
  let s = 0;
  if (oldIdx >= wf2ConstOld) s += 4;
  if (oldIdx > wf2EndOld) s -= WF2DEL;
  if (oldIdx > wf4FnEnd) s -= WF4DEL;
  return s;
}
// 77 錨點（0-indexed，見各測試檔；kwan151／rom176／travel114 用 1-indexed line(n)，數值同 shift 算法一致）
const pins = [9844, 10185, 10188, 10189, 10190, 10233, 10452, 11453, 11486, 15172, 15181, 15182, 15224,
  10003, 15571, 15694, 15643, 39288, 39661, 40799, 40899, 6360, 11977, 12114, 17290, 40868, 28878,
  16224, 19450, 21610, 22816, 23251, 23254, 23285, 28309, 43978, 44190, 44338, 44359,
  8869, 14994, 14995, 15007, 15008, 15019, 15020, 15123, 25179, 27956, 27989, 39088, 39207, 39280,
  39503, 39547, 39553, 39620, 39622, 39625, 39652, 40762, 40809, 41142, 41164, 41316, 41321, 42222,
  43711, 43855, 43856, 43900, 43901, 43926, 44809];
let bad = 0;
for (const p of pins) {
  const n = p + shift(p);
  const ok = oldLines[p] === newLines[n];
  if (!ok) { bad++; console.log(`MISMATCH pin ${p} -> ${n} :: old: ${JSON.stringify((oldLines[p] || '').slice(0, 80))} || new: ${JSON.stringify((newLines[n] || '').slice(0, 80))}`); }
}
console.log(bad === 0 ? `ALL ${pins.length} PINS PURE DRIFT` : `${bad} MISMATCHES`);
process.exit(bad === 0 ? 0 : 1);
