/* v20a87 WF5 觸達審計腳本（診斷用，非 pass/fail 套件）：
   全內容可達性盤點——旗標生產者/消費者全圖 + fixpoint 可達分析。
   行法：node tests/audit_wf5.js [indexPath]
   輸出：逐項清單（正常可達／低觸達／證實到唔到候選），候選要人手覆核先成立。 */
'use strict';
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const INDEX = process.argv[2] || path.join(ROOT, 'index.html');
const html = fs.readFileSync(INDEX, 'utf8');

function extractConst(name) {
  const start = html.indexOf('const ' + name);
  if (start < 0) return null;
  const eq = html.indexOf('=', start);
  let i = html.indexOf('{', eq), j = html.indexOf('[', eq), k;
  if (j >= 0 && (i < 0 || j < i)) i = j;
  const open = html[i]; const close = open === '{' ? '}' : ']';
  let depth = 0, inS = null, esc = false;
  for (k = i; k < html.length; k++) {
    const c = html[k];
    if (inS) { if (esc) esc = false; else if (c === '\\') esc = true; else if (c === inS) inS = null; continue; }
    if (c === '"' || c === "'" || c === '`') { inS = c; continue; }
    if (c === open) depth++;
    else if (c === close) { depth--; if (depth === 0) break; }
  }
  return html.slice(i, k + 1);
}
function evalConst(name) {
  const src = extractConst(name);
  if (!src) return null;
  try { return eval('(' + src + ')'); } catch (e) { return { __evalError: String(e && e.message || e) }; }
}
function loadPack(f) { try { return JSON.parse(fs.readFileSync(path.join(ROOT, 'content', f), 'utf8')); } catch (e) { return null; } }

/* ---------- 深層收集：object 入面所有 effects.flags / flags_written / effects 內字串 ---------- */
function deepCollect(node, out) {
  if (!node || typeof node !== 'object') return;
  if (Array.isArray(node)) { node.forEach(x => deepCollect(x, out)); return; }
  for (const k of Object.keys(node)) {
    const v = node[k];
    if (k === 'flags' && Array.isArray(v)) v.forEach(s => { if (typeof s === 'string') out.flags.add(s); });
    if (k === 'flags_written' && Array.isArray(v)) v.forEach(s => { if (typeof s === 'string') out.flags.add(s); });
    if (k === 'routes' && Array.isArray(v)) v.forEach(s => { if (typeof s === 'string') out.flags.add(s); });
    if (typeof v === 'string' && /^(flag_|route_|rival_|choi_|rel_)/.test(v)) out.strings.add(v);
    deepCollect(v, out);
  }
}
function nodeChoiceFlags(node) {
  const out = { flags: new Set(), strings: new Set() };
  (node.choices || []).forEach(c => deepCollect(c && c.effects || {}, out));
  if (Array.isArray(node.flags_written)) node.flags_written.forEach(s => out.flags.add(s));
  return out;
}

/* ---------- 節點宇宙 ---------- */
const universe = new Map(); // id -> {node, src, gate tokens}
function addNodes(nodes, src) {
  (nodes || []).forEach(n => { if (n && n.id && !universe.get(n.id)) universe.set(n.id, { node: n, src }); });
}
const packMain = loadPack('story_detail_c1_to_c17.json');
const packRomVHC = loadPack('story_detail_romance_vera_hiu_choi.json');
const packRomLX = loadPack('story_detail_romance_lan_xu.json');
const packRomT = loadPack('story_detail_romance_tang.json');
const packRival = loadPack('story_detail_rival_mentor.json');
addNodes(packMain && packMain.nodes, 'pack:c1_to_c17');
addNodes(packRomVHC && packRomVHC.nodes, 'pack:romance_vhc');
addNodes(packRomLX && packRomLX.nodes, 'pack:romance_lx');
addNodes(packRomT && packRomT.nodes, 'pack:romance_tang');
addNodes(packRival && packRival.nodes, 'pack:rival');
const spine89 = evalConst('STORY_SPINE_NODES_1989');
const spine90 = evalConst('STORY_SPINE_NODES_1990');
const spineC6 = evalConst('STORY_SPINE_NODES_C6');
const spineWF1 = evalConst('STORY_SPINE_NODES_WF1');
const c17Node = evalConst('STORY_SPINE_NODE_C17_410');
const commit48 = evalConst('COMMIT48_NODES');
const choice47 = evalConst('CHOICE47_NODES');
[spine89, spine90, spineC6, spineWF1].forEach((t, i) => {
  if (t && !t.__evalError) Object.values(t).forEach(n => addNodes([n], 'spine' + i));
});
if (c17Node && !c17Node.__evalError) addNodes([c17Node.node || c17Node], 'spine:c17');
if (commit48 && !commit48.__evalError) Object.values(commit48).forEach(n => addNodes([n], 'commit48'));
if (choice47 && !choice47.__evalError) Object.values(choice47).forEach(n => addNodes([n], 'choice47'));

/* ---------- 生產者：code 層 ---------- */
const codeProducers = new Set();
for (const m of html.matchAll(/flags\.([A-Za-z0-9_]+)\s*=(?!=)/g)) codeProducers.add(m[1]);
for (const m of html.matchAll(/flags\[["']([^"']+)["']\]\s*=(?!=)/g)) { if (!m[1].includes('+')) codeProducers.add(m[1]); }
for (const m of html.matchAll(/setFlag\(["']([^"']+)["']/g)) codeProducers.add(m[1]);
for (const m of html.matchAll(/StoryOC\.setFlag\(["']([^"']+)["']/g)) codeProducers.add(m[1]);
/* gig packs 嘅 effects 旗標（通告抉擇都可以寫旗） */
const gigIds = new Set();
for (const gf of ['gigs_1988.json', 'gigs_1989.json', 'gigs_1990.json', 'gigs_1991.json', 'gigs_1992.json',
  'gigs_1988_3.2.5-soft.json', 'gigs_1988_3.2.7-soft.json', 'gigs_1988_3.2.8-soft.json', 'gigs_1988_3.2.9-soft.json', 'gigs_1988_3.2.10-soft.json']) {
  const g = loadPack(gf); if (!g) continue;
  const out = { flags: new Set(), strings: new Set() };
  deepCollect(g, out);
  out.flags.forEach(f => codeProducers.add(f));
  const walkIds = (o) => { if (!o || typeof o !== 'object') return; if (Array.isArray(o)) return o.forEach(walkIds); if (typeof o.id === 'string' && /^gig_/.test(o.id)) gigIds.add(o.id); Object.values(o).forEach(walkIds); };
  walkIds(g);
}
/* index 內定義嘅 gig（情報通告等） */
for (const m of html.matchAll(/\bid\s*:\s*"(gig_[a-z0-9_]+)"/g)) gigIds.add(m[1]);
/* done_<gigId> 由殺青結算通用寫入（index line ~34316） */
const doneGigProducer = (tok) => tok.startsWith('done_') && gigIds.has(tok.slice(5));
/* alias 口徑跟被審計 index 本身：index 有 WF5 alias 修復先計 alias 接通（修前 FAIL／修後 PASS 對照） */
const ALIAS_ON = html.includes('前綴 alias');
const aliasOf = (t) => t.startsWith('flag_') ? t.slice(5) : ('flag_' + t);

/* ---------- token 分類 ---------- */
function classify(tok) {
  if (universe.has(tok)) return 'node';
  if (/^(week_min:|days_after_prev:|day_min:|fame_min:|credit_min:)/.test(tok)) return 'pacing';
  if (/_threshold$/.test(tok)) return 'threshold';
  if (/^season_/.test(tok)) return 'season';
  if (/^phase_/.test(tok)) return 'phase';
  return 'flag';
}
function nodeTokens(entry) {
  const n = entry.node;
  const and = [], any = [];
  const norm = (v) => Array.isArray(v) ? v.slice() : (typeof v === 'string' ? v.split(',').map(s => s.trim()).filter(Boolean) : []);
  norm(n.openConditions).forEach(t => and.push(t));
  norm(n.openConditionsAny).forEach(t => any.push(t));
  return { and, any };
}

/* ---------- fixpoint ---------- */
const produced = new Set(codeProducers);
const reachable = new Set();
let changed = true, rounds = 0;
while (changed && rounds < 60) {
  changed = false; rounds++;
  for (const [id, entry] of universe) {
    if (reachable.has(id)) continue;
    const { and, any } = nodeTokens(entry);
    const tokOk = (t) => {
      const c = classify(t);
      if (c === 'node') return reachable.has(t);
      if (c === 'flag') return produced.has(t) || (ALIAS_ON && produced.has(aliasOf(t))) || doneGigProducer(t);
      return true; /* pacing/threshold/season/phase：非旗標條件，另行人工核（rel 累積見下） */
    };
    if (and.every(tokOk) && (any.length === 0 || any.some(tokOk))) {
      reachable.add(id); changed = true;
      nodeChoiceFlags(entry.node).flags.forEach(f => produced.add(f));
    }
  }
}

/* ---------- rel 累積核查（感情線 threshold 保守估算） ---------- */
function lineRelReport(pack, npcKey) {
  if (!pack || !pack.nodes) return null;
  const order = { meet: 0, push1: 1, push2: 2, crisis: 3, ending: 4 };
  const rows = pack.nodes.filter(n => JSON.stringify(n.cast || []).includes(npcKey) || (n.romanceLine || '').includes(npcKey) || n.id.toLowerCase().includes(npcKey));
  return rows;
}

/* ---------- 輸出 ---------- */
const out = [];
out.push('# WF5 觸達審計輸出（index: ' + INDEX + '）');
out.push('節點宇宙：' + universe.size + ' 個；code/gig 生產者旗標：' + codeProducers.size + ' 個；gig 宇宙：' + gigIds.size + ' 個');
out.push('');
out.push('## 未達節點（fixpoint 到唔到——死內容候選，要人手覆核）');
let deadCount = 0;
for (const [id, entry] of universe) {
  if (reachable.has(id)) continue;
  deadCount++;
  const { and, any } = nodeTokens(entry);
  const miss = (t) => { const c = classify(t); return c === 'flag' && !produced.has(t) && !doneGigProducer(t) ? t + '(冇生產者)' : (c === 'node' && !reachable.has(t) ? t + '(前置未達)' : null); };
  out.push('- ' + id + ' [' + entry.src + '] AND缺: ' + (and.map(miss).filter(Boolean).join(', ') || '—') +
    ' | ANY全缺: ' + (any.length && any.every(t => miss(t)) ? any.join(', ') : '—'));
}
if (!deadCount) out.push('（冇）');
out.push('');
out.push('## 消費者旗標冇生產者（全域掃描）');
const consumerFlags = new Set();
for (const [, entry] of universe) {
  const { and, any } = nodeTokens(entry);
  and.concat(any).forEach(t => { if (classify(t) === 'flag') consumerFlags.add(t); });
}
const orphans = [...consumerFlags].filter(t => !produced.has(t) && !(ALIAS_ON && produced.has(aliasOf(t))) && !doneGigProducer(t)).sort();
out.push('getFlag alias 修復在場：' + ALIAS_ON);
out.push(orphans.length ? orphans.map(t => '- ' + t).join('\n') : '（冇）');
out.push('（註：ching_after_train／polish 嘅 store 錯配屬節拍層讀取問題，唔喺呢個旗標圖入面，見 Part 2 節拍清單原文對照。）');
console.log(out.join('\n'));

/* ================= Part 2：巧遇節拍 / 報紙 / 隱藏通告 / soft 變體層 ================= */
const out2 = [];
out2.push('');
out2.push('## 巧遇節拍清單（gate 依賴原文）');
/* 由 ENC79_BEATS 常量＋後續 assignment/push 抽節拍 */
const beatsFound = [];
{
  const region = html.slice(html.indexOf('const ENC79_BEATS'), html.indexOf('const STAR_SIGHTINGS'));
  const re = /\{\s*id:"([a-z0-9_]+)",\s*when\(st\)\{/g;
  let m;
  while ((m = re.exec(region))) {
    let i = re.lastIndex, depth = 1;
    while (i < region.length && depth > 0) { if (region[i] === '{') depth++; else if (region[i] === '}') depth--; i++; }
    beatsFound.push({ id: m[1], when: region.slice(re.lastIndex, i - 1).replace(/\s+/g, ' ').slice(0, 220) });
  }
}
/* DLG beats 段存在性 */
const dlgBeats = new Set();
for (const name of [...html.matchAll(/const (ENC(?:79|83|84)_DLG_[a-z_]+)\s*=/g)].map(x => x[1])) {
  const d = evalConst(name);
  if (d && d.beats) Object.keys(d.beats).forEach(k => dlgBeats.add(k));
}
for (const m of html.matchAll(/D\.beats\.([a-z0-9_]+)\s*=/g)) dlgBeats.add(m[1]); /* patron 段後加 */
const beatIds = new Set(beatsFound.map(b => b.id));
out2.push('節拍總數：' + beatsFound.length + '；DLG beats 段：' + dlgBeats.size);
out2.push('有 gate 冇對白段（播到會冇戲）：' + (beatsFound.filter(b => !dlgBeats.has(b.id)).map(b => b.id).join(', ') || '冇'));
out2.push('有對白段冇 gate（永遠唔會播）：' + ([...dlgBeats].filter(k => !beatIds.has(k)).join(', ') || '冇'));
beatsFound.forEach(b => out2.push('- ' + b.id + ' :: ' + b.when));
out2.push('');
out2.push('## 報紙 NEWS82');
const news82 = evalConst('NEWS82_EVENTS');
if (Array.isArray(news82)) {
  news82.forEach(e => out2.push('- ' + e.id + ' day ' + e.day + ' head版:' + !!e.headline + ' echo:' + (e.echo ? e.echo.id : '冇')));
} else out2.push('NEWS82_EVENTS 抽取失敗');
out2.push('');
out2.push('## 隱藏通告 / 情報交叉引用');
const intelGigs = evalConst('INTEL_HIDDEN_GIGS');
if (Array.isArray(intelGigs)) intelGigs.forEach(g => out2.push('- INTEL_HIDDEN_GIGS: ' + g.id + '（喺 gig 宇宙：' + gigIds.has(g.id) + '）'));
for (const m of html.matchAll(/id:"(gig_wf3_[a-z0-9_]+)"/g)) out2.push('- WF3 通告定義: ' + m[1]);
out2.push('');
out2.push('## soft 變體層（DengLine / DualMeet）內部旗標鏈');
for (const f of ['MOCK_STORY_DENG_LINE_MEET_SOFT_v1.1.json', 'MOCK_STORY_DENG_LINE_PUSH_SOFT_v1.json', 'MOCK_STORY_DUAL_MEET_THICKEN_SOFT_v1.json']) {
  const d = loadPack(f);
  if (!d) { out2.push('- ' + f + ' 載入失敗'); continue; }
  const nodes = d.nodes || d.beats || [];
  out2.push('- ' + f + '：' + (Array.isArray(nodes) ? nodes.length : Object.keys(nodes).length) + ' 段/節點');
}
console.log(out2.join('\n'));
