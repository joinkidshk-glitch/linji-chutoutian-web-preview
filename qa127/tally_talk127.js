// v20a127 T1-redo：傾談分流點票（Node，直接執行遊戲真代碼）。
// 抽 index.html 入面嘅 NPC_TIER_LINES／NPC_AFF_TIERS／AFF_DIALOGUE_GATES／
// npcTierPool／affUnlockedKeys／pickNpcLine（括號配對抽取，唔改原文），
// NPC_LINES 用遊戲實際載入嘅 content/npc_lines_core.json（disk 版）。
// S 用 stub（aff＝100，stress＝0）。每 NPC 2000 次抽樣，點算 5 句目標句。
const fs = require('fs');
const path = require('path');
const ROOT = process.argv[2] || path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');

function extract(src, startMarker) {
  const i = src.indexOf(startMarker);
  if (i < 0) throw new Error('marker not found: ' + startMarker);
  let j = src.indexOf('{', i);
  let bracket = null;
  if (src[i + startMarker.length - 1] === '[' || src.slice(i, i + 60).includes('= [')) {
    j = src.indexOf('[', i); bracket = ['[', ']'];
  } else {
    bracket = ['{', '}'];
  }
  let depth = 0, k = j;
  for (; k < src.length; k++) {
    const c = src[k];
    if (c === bracket[0]) depth++;
    else if (c === bracket[1]) { depth--; if (depth === 0) { k++; break; } }
  }
  return src.slice(i, k);
}
function extractFn(src, name) {
  const marker = 'function ' + name + '(';
  const i = src.indexOf(marker);
  if (i < 0) throw new Error('fn not found: ' + name);
  let j = src.indexOf('{', i);
  let depth = 0, k = j;
  for (; k < src.length; k++) {
    const c = src[k];
    if (c === '{') depth++;
    else if (c === '}') { depth--; if (depth === 0) { k++; break; } }
  }
  return src.slice(i, k);
}

const code = [
  extract(html, 'const NPC_TIER_LINES = '),
  extract(html, 'const NPC_AFF_TIERS = '),
  extract(html, 'const AFF_DIALOGUE_GATES = '),
  extractFn(html, 'npcTierPool'),
  extractFn(html, 'affUnlockedKeys'),
  extractFn(html, 'pickNpcLine'),
].join('\n;\n');
const NPC_LINES = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'npc_lines_core.json'), 'utf8'));
// 驗證：5 句目標句喺邊個 tier 池
const NPC_TIER_LINES = eval(code + '\n; NPC_TIER_LINES');
for (const [pool, arr] of [['colleague.daily', NPC_TIER_LINES.colleague.daily],
    ['colleague.insider', NPC_TIER_LINES.colleague.insider],
    ['rival.insider', NPC_TIER_LINES.rival.insider],
    ['director.daily', NPC_TIER_LINES.director.daily],
    ['reporter.daily', NPC_TIER_LINES.reporter.daily],
    ['reporter.insider', NPC_TIER_LINES.reporter.insider]]) {
  console.log('pool', pool, 'n=', arr.length);
}

const TARGETS = {
  'chow_angry#1': '我前幾日喺清水灣嗰組做嘢，氣氛幾好，副導又唔會亂鬧人，新人去嗰邊撞下，學到嘢又唔使捱得咁辛苦。',
  'chow_angry#2': '你嚟試鏡，唔好背到滾瓜爛熟就算，留返少少即場反應畀我睇，我想知你聽到新指示，識唔識得即刻變。',
  'chow_sad#1': '陸柏言嗰場戲，佢明明背熟晒對白，但一埋位就停咗兩停，導演冇鬧，仲叫大家抖下先，可能佢真係好攰。',
  'chow_sad#2': '呢份工我睇過，唔啱我做，漏畀你算啦：嗰組缺個肯捱夜嘅後生，你肯頂，入去就有位，唔好講我益你。',
  'chow_sad#3': '嗰個組而家四圍搵人，唔係冇人，係之前嗰個走咗佬，你有本事補到位，導演點都會記得你呢份人情。',
};

// 在 sandbox 執行真 pickNpcLine
const vm = require('vm');
const sandbox = {
  console, Math,
  S: { npcs: {}, stress: 0, flags: {} },
  NPC_LINES,
  NPC_LINES_CORE: NPC_LINES,
  hoIntroLine49: () => null,
};
vm.createContext(sandbox);
vm.runInContext(code + '\n; this.__pick = pickNpcLine;', sandbox);
const pickFn = sandbox.__pick;

for (const id of ['colleague', 'rival', 'director', 'reporter', 'agent']) {
  sandbox.S.npcs = { [id]: 100 };
  sandbox.S.stress = 0;
  const hits = {};
  for (const k of Object.keys(TARGETS)) hits[k] = 0;
  const distinct = new Set();
  let total = 0;
  for (let i = 0; i < 2000; i++) {
    const t = pickFn(id, {}) || '';
    if (!t) continue;
    total++;
    distinct.add(t);
    for (const [k, line] of Object.entries(TARGETS)) if (t === line) hits[k]++;
  }
  console.log(`T1 ${id}: 抽 ${total} 次／${distinct.size} 句唔同｜目標句命中 ${JSON.stringify(hits)}`);
}
console.log('DONE');
