// v20a89 BR89：dead-flag lint（真分支審計流程防再犯）
// 規則：每隻由「抉擇」寫入嘅 story 旗（flag_*），必須有 ≥1 個 gameplay 讀取位，
// 或者喺 tests/br89_flag_whitelist.json 度有註明理由（純風味／孖旗／元數據）。
// 寫入來源：content pack 嘅 choice effects.flags + index 內嵌數據表嘅 flags:[...]。
// 讀取來源：index 入面讀旗函數呼叫（getFlag/hasFlag/endingFlag410/enc87StoryFlag/
//   storyFlag/getStoryFlag/hasStoryFlag/flagOn）參數、gate/條件物件入面嘅字串、
//   pack 入面寫入陣列以外嘅出現（節點 gate 等）。
// 反證：對 v88 基線行，應該捉到審計點名嗰批（WF1/WF3/WF4/八線 ending 等死旗）。
// 用法：node tests/test_br89_deadflag_lint.js [indexPath] [contentDir]
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const indexPath = process.argv[2] || path.join(ROOT, 'index.html');
const contentDir = process.argv[3] || path.join(ROOT, 'content');
const wlPath = path.join(__dirname, 'br89_flag_whitelist.json');
const whitelist = fs.existsSync(wlPath) ? JSON.parse(fs.readFileSync(wlPath, 'utf8')) : {};
const html = fs.readFileSync(indexPath, 'utf8');

const FLAG_RE = /flag_[a-z0-9_]+/g;
function uniq(a){ return Array.from(new Set(a)); }

/* ---------- 1. 收集寫入 ---------- */
const writes = new Set();
// (a) pack JSON：行 choice effects.flags（用正則掃 "flags": [ ... ] 塊，跨 pack 通用）
let packText = '';
if (fs.existsSync(contentDir)) {
  for (const f of fs.readdirSync(contentDir)) {
    if (!f.endsWith('.json')) continue;
    try { packText += '\n' + fs.readFileSync(path.join(contentDir, f), 'utf8'); } catch (_e) {}
  }
}
function collectFlagArrays(text, into) {
  const re = /"?flags"?\s*:\s*\[([^\]]*)\]/g;
  let m;
  while ((m = re.exec(text))) {
    const inner = m[1];
    let q;
    const qre = /["'](flag_[a-z0-9_]+)["']/g;
    while ((q = qre.exec(inner))) into.add(q[1]);
  }
}
collectFlagArrays(packText, writes);
collectFlagArrays(html, writes);
// (b) index 內 setFlag("flag_x") 直接寫入
{
  const re = /setFlag\(\s*["'](flag_[a-z0-9_]+)["']/g;
  let m; while ((m = re.exec(html))) writes.add(m[1]);
}

/* ---------- 2. 收集讀取 ---------- */
const reads = new Set();
// (a) 讀旗函數呼叫參數
{
  const re = /(?:getFlag|hasFlag|endingFlag410|enc87StoryFlag|storyFlag|getStoryFlag|hasStoryFlag|flagOn|hasIntelFlag)\s*\([^)]*?["'](flag_[a-z0-9_]+)["']/g;
  let m; while ((m = re.exec(html))) reads.add(m[1]);
}
// (b) index 入面：將所有「寫入陣列」同「flags_written 元數據」遮起嚟之後，剩低嘅出現當讀取
function maskWrites(text) {
  let t = text.replace(/"?flags"?\s*:\s*\[[^\]]*\]/g, ' ');
  t = t.replace(/"?flags_written"?\s*:\s*\[[^\]]*\]/g, ' ');
  t = t.replace(/setFlag\(\s*["']flag_[a-z0-9_]+["']/g, ' ');
  return t;
}
{
  const masked = maskWrites(html);
  let m; const re = new RegExp(FLAG_RE.source, 'g');
  while ((m = re.exec(masked))) reads.add(m[0]);
}
// (c) pack 入面寫入陣列以外嘅出現（節點 gate／條件引用）
{
  const masked = maskWrites(packText);
  let m; const re = new RegExp(FLAG_RE.source, 'g');
  while ((m = re.exec(masked))) reads.add(m[0]);
}

/* ---------- 3. 判定 ---------- */
const dead = [];
for (const f of Array.from(writes).sort()) {
  if (!reads.has(f) && !whitelist[f]) dead.push(f);
}
const wlUsed = Object.keys(whitelist).filter(f => writes.has(f) && !reads.has(f));
console.log('抉擇寫入旗總數: ' + writes.size);
console.log('有讀取位: ' + Array.from(writes).filter(f => reads.has(f)).length);
console.log('白名單豁免: ' + wlUsed.length + (wlUsed.length ? '（' + wlUsed.join(', ') + '）' : ''));
if (dead.length) {
  console.log('FAIL 死旗（寫入但零讀取、又唔喺白名單）: ' + dead.length);
  dead.forEach(f => console.log('  DEAD ' + f));
  process.exit(1);
}
console.log('PASS dead-flag lint：冇未註明嘅死旗');
