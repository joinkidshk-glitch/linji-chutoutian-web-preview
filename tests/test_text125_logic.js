// v20a125 TEXT125 邏輯測試：StoryPlay 讀埋 `text` 單句 beats。
// 背景：CHOICE47／WF3／COMMIT48／WF4 全部節點用 `text` 形 beats，舊版 currentLine／
// advance 只讀 lines／line，呢啲 beats 逐句回 null → render 即跳去 choices，對白成段
// 唔顯示（v119 實駕：原裝 W3 一開即 mode=choices 行字空；原裝 G4 一開即出選項）。
// 修法 (b)：播放器 fallback lines＞line＞text，唔郁任何節點數據（唔改 content pack JSON，
// 節點本身就喺 index.html 入面亦唔郁）；applyFamilySafeToNode 嘅替換亦對齊到 text。
// 抽真身：currentLine／advance／applyFamilySafeToNode 全部由 index.html 原文抽出 eval，
// 唔用手抄副本；其餘 helper 做 stub（行為同真身一致嘅最小版）。
// 反證：同一檔對 pristine main 跑，text-beat 斷言必須 FAIL（見 handoff，唔喺呢檔入面跑）。
// 用法：node tests/test_text125_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS ' : 'FAIL ') + name); }
function info(msg){ console.log('INFO ' + msg); }

/* ---- 抽函數真身：由 `  function NAME(` 起，到之後第一行恰好係 `  }`（currentLine／advance
   喺 StoryPlay IIFE 入面，縮排 2 格）；applyFamilySafeToNode 係頂層，到第一行恰好係 `}`。 ---- */
function extractFn(startMarker, endLine){
  const lines = html.split('\n');
  let s = -1;
  for(let i = 0; i < lines.length; i++){
    if(lines[i].indexOf(startMarker) >= 0){ s = i; break; }
  }
  if(s < 0) return null;
  let e = -1;
  for(let i = s + 1; i < lines.length; i++){
    if(lines[i] === endLine){ e = i; break; }
  }
  if(e < 0) return null;
  return lines.slice(s, e + 1).join('\n');
}
function toFn(src, name){
  if(!src) return null;
  const body = src.replace(/^\s*function\s+\w+\s*\(/, 'function(');
  return eval('(' + body + ')');
}
const curSrc = extractFn('  function currentLine(){', '  }');
const advSrc = extractFn('  function advance(){', '  }');
const famSrc = extractFn('function applyFamilySafeToNode(node){', '}');
ok('搵到 currentLine／advance／applyFamilySafeToNode 真身', !!(curSrc && advSrc && famSrc));
if(!curSrc || !advSrc || !famSrc){
  console.log('RESULT FAIL');
  process.exit(1);
}
/* 反證前置：currentLine 真身必須有 text fallback，否則之後嘅 text 斷言無意義——
   pristine main 喺呢度已經乾淨 FAIL（唔係 crash）。 */
ok('currentLine 有 text fallback（pristine main 預期 FAIL）',
  curSrc.indexOf('b.text') >= 0 && curSrc.indexOf('[b.text]') >= 0);
ok('advance 有 text fallback（pristine main 預期 FAIL）',
  advSrc.indexOf('b.text') >= 0 && advSrc.indexOf('[b.text]') >= 0);
ok('applyFamilySafeToNode 處理 b.text（pristine main 預期 FAIL）',
  famSrc.indexOf('b.text') >= 0);
if(fails.length){
  console.log('RESULT FAIL (' + fails.length + ')');
  process.exit(1);
}
const currentLine = toFn(curSrc, 'currentLine');
const advance = toFn(advSrc, 'advance');
const applyFamilySafeToNode = toFn(famSrc, 'applyFamilySafeToNode');

/* ---- stubs：行為同真身一致嘅最小版 ---- */
let _sess = null;
function spIsSystemBeat(b){
  b = b || {};
  if(b.kind === 'system') return true;
  if(b.kind === 'dialogue') return false;
  if(b.type === 'narration') return true;
  const sp = String(b.speaker == null ? '' : b.speaker).trim();
  return !sp || sp === '系統' || sp === '旁白';
}
function spResolveSpeakerId(b){ return (b && b.speakerId) || null; }
function spDisplayName(b, id){ return (b && b.speaker) || ''; }
function spNormEmotion(e){ return e || 'neutral'; }
function spNormExpression(e){ return e || 'default'; }
function spExprFromEmotion(){ return null; }
function dlg106ResolveCategory(){ return 'neutral'; }
function render(){ /* advance 播完一格會 render；test 入面唔使真渲染 */ }
let __famOn = true;
function contentFilterOn(){ return __famOn; }

/* ---- (1) text 單句：旁白句 ---- */
_sess = { node: { id: 'G4_family_job', beats: [
  { speakerId: '', speaker: '', kind: 'system', text: '1990 年年尾，阿偉返屋企食飯。' },
  { speakerId: '', speaker: '阿媽', kind: 'npc', text: '阿偉，有件事同你商量。' },
  { speakerId: 'player', speaker: '阿偉', kind: 'player', text: '（一份穩陣工。一條未行完嘅路。）' }
]}, mode: 'beats', beatIdx: 0, lineIdx: 0 };
let cur = currentLine();
ok('text 旁白句顯示（system＋行字）', cur && cur.text === '1990 年年尾，阿偉返屋企食飯。' && cur.system === true && cur.speakerId === null);
ok('text 旁白句 lineCount＝1', cur && cur.lineCount === 1 && cur.beatCount === 3);
advance();
cur = currentLine();
ok('text 阿媽句顯示（講者＋行字）', cur && cur.text === '阿偉，有件事同你商量。' && cur.speaker === '阿媽' && cur.system === false);
advance();
cur = currentLine();
ok('text 阿偉句顯示（player kind）', cur && cur.text === '（一份穩陣工。一條未行完嘅路。）' && cur.kind === 'player');
advance();
ok('3 句 text beats 行完 → mode=choices', _sess.mode === 'choices');
ok('行完之後 currentLine 回 null', currentLine() === null);

/* ---- (2) 舊形不變：lines 多行／line 單句／空 beat ---- */
_sess = { node: { id: 'C1', beats: [
  { speakerId: 'agent', speaker: '何生', kind: 'npc', lines: ['第一句', '第二句'] },
  { speakerId: 'agent', speaker: '何生', kind: 'npc', line: '單句行' },
  { speakerId: 'agent', speaker: '何生', kind: 'npc' }
]}, mode: 'beats', beatIdx: 0, lineIdx: 0 };
ok('lines 多行第一句', currentLine() && currentLine().text === '第一句' && currentLine().lineCount === 2);
advance();
ok('lines 多行第二句（lineIdx 推進）', currentLine() && currentLine().text === '第二句' && _sess.lineIdx === 1);
advance();
ok('line 單句照舊顯示', currentLine() && currentLine().text === '單句行' && currentLine().lineCount === 1);
advance();
ok('空 beat（無 lines／line／text）→ null 唔 crash', currentLine() === null);
advance();
ok('空 beat 行完 → mode=choices', _sess.mode === 'choices');

/* ---- (3) 優先次序：lines＞line＞text（全庫零 beat 並存，次序只係保險） ---- */
_sess = { node: { id: 'X', beats: [
  { speakerId: 'agent', speaker: '何生', kind: 'npc', lines: ['L 行'], text: 'T 行' },
  { speakerId: 'agent', speaker: '何生', kind: 'npc', line: 'S 行', text: 'T 行' },
  { speakerId: 'agent', speaker: '何生', kind: 'npc', text: '' }
]}, mode: 'beats', beatIdx: 0, lineIdx: 0 };
ok('lines＋text 並存 → 行 lines', currentLine() && currentLine().text === 'L 行');
advance();
ok('line＋text 並存 → 行 line', currentLine() && currentLine().text === 'S 行');
advance();
ok('空字串 text 唔當一行 → null', currentLine() === null);

/* ---- (4) applyFamilySafeToNode：text 同 lines 同一套替換＋唔郁原節點 ---- */
__famOn = true;
const nodeIn = { id: 'T', beats: [
  { speakerId: 'agent', speaker: '何生', kind: 'npc', text: '收工去買醉，臨時演員蹲在路邊抽煙' },
  { speakerId: 'agent', speaker: '何生', kind: 'npc', lines: ['食煙嗰個，叫佢去歇息'] },
  { speakerId: 'agent', speaker: '何生', kind: 'npc', text: '乾淨句，乜都冇' }
]};
const nodeOut = applyFamilySafeToNode(nodeIn);
ok('text 句：買醉／抽煙照替換',
  nodeOut && nodeOut.beats[0].text === '收工去夜歸散心，臨時演員蹲在路邊喝紙包飲料、等開工');
ok('lines 句：食煙照替換（舊行為不變）',
  nodeOut && nodeOut.beats[1].lines[0] === '傾偈嗰個，叫佢去歇息');
ok('乾淨 text 句唔郁', nodeOut && nodeOut.beats[2].text === '乾淨句，乜都冇');
ok('原節點唔被改（深拷貝）',
  nodeIn.beats[0].text.indexOf('買醉') >= 0 && nodeIn.beats[1].lines[0].indexOf('食煙') >= 0);
__famOn = false;
ok('filter 關閉 → 原樣回傳同一物件', applyFamilySafeToNode(nodeIn) === nodeIn);

/* ---- (5) 反證（in-test 變異）：抽走 fallback 嘅舊版邏輯必須回 null ---- */
const oldLines = (b) => Array.isArray(b.lines) ? b.lines : (b.line ? [b.line] : []);
ok('反證：舊版解析 text beat 得空陣列（即 currentLine 回 null）',
  oldLines({ text: '阿媽句' }).length === 0);

console.log(fails.length ? 'RESULT FAIL (' + fails.length + ')' : 'RESULT PASS');
process.exit(fails.length ? 1 : 0);
