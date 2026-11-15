// v20a219 harness：模擬真實載入 pipeline，斷言 when 顯示值。
// 抽取全部係 index.html 入面嘅真函數／真表（唔係手抄邏輯）：
//   ROMANCE_LAN_PA_OVERRIDES + applyRomanceLanOverrides48（PA，v20a234 改名；主線覆寫已刪）
//   normaliseTangStub152 → contra98FixNodeWhen（CONTRA98_WHEN_FIX＋CLEAN100_WHEN_FIX）
//   → years66Walk（years66ShiftText／ShiftYear／SKIP_KEYS／TOKEN_RE）
// 顯示值查兩層：(a) 節點 when（walk 後）；(b) 實播頁首 spPlayerMeta（LIVE 預設路徑，
//   eraTag 優先：L28002 soft = eraTag||when，年份顯示前 +2、季節由 spSoftSeasonChar 抽）。
// 用法：node qa219/harness_v219.js   （cwd 必須係工作副本根目錄）
// 舊表對照由 `git show 5580f8d:index.html`（v218 main 基底）抽出，同一 pipeline、同一 pack 跑兩次比對。
'use strict';
const fs = require('fs');
const { execSync } = require('child_process');
const vm = require('vm');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const htmlNew = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
const htmlOld = execSync('git show 5580f8d:index.html', { cwd: ROOT, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 }); // v218 main 基底（唔用 HEAD：commit 之後 HEAD 已經係修復版，對照會失效）

let fails = [];
function ok(name, cond, extra) {
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (cond ? '' : '  << ' + (extra || '')));
  if (!cond) fails.push(name);
}

// --- 掃描器：跳過字串／模板／註解，先搵配對括號 -----------------------------
function extractBlock(src, startIdx, openCh, closeCh) {
  let i = src.indexOf(openCh, startIdx);
  if (i < 0) throw new Error('open not found at ' + startIdx);
  let depth = 0;
  for (let j = i; j < src.length; j++) {
    const c = src[j];
    if (c === "'" || c === '"' || c === '`') {
      const q = c; j++;
      for (; j < src.length; j++) {
        if (src[j] === '\\') { j++; continue; }
        if (src[j] === q) break;
        if (q === '`' && src[j] === '$' && src[j + 1] === '{') {
          // 模板 ${...}：遞迴跳過表達式，之後繼續掃模板字串直至反引號
          const sub = extractBlock(src, j + 1, '{', '}');
          j = sub.end; continue;
        }
      }
      continue;
    }
    if (c === '/' && src[j + 1] === '/') { while (j < src.length && src[j] !== '\n') j++; continue; }
    if (c === '/' && src[j + 1] === '*') { j = src.indexOf('*/', j + 2) + 1; continue; }
    if (c === openCh) depth++;
    else if (c === closeCh) { depth--; if (depth === 0) return { code: src.slice(i, j + 1), end: j }; }
  }
  throw new Error('unbalanced ' + openCh + closeCh);
}
function extractFn(src, sig) {
  const i = src.indexOf(sig);
  if (i < 0) throw new Error('not found: ' + sig);
  const b = extractBlock(src, i, '{', '}');
  return src.slice(i, b.end + 1);
}
function extractConstObj(src, name) {
  const i = src.indexOf('const ' + name + ' =');
  if (i < 0) throw new Error('const not found: ' + name);
  const b = extractBlock(src, i, '{', '}');
  return src.slice(i, b.end + 1) + ';';
}
function extractConstStmt(src, name) {
  const i = src.indexOf('const ' + name + ' =');
  if (i < 0) throw new Error('const not found: ' + name);
  const semi = src.indexOf(';', i);
  return src.slice(i, semi + 1);
}

// --- 抽取（新版） ------------------------------------------------------------
// 共用部分（兩版相同，git diff 證實零改動）：YEARS66、contra98 函數本體、
// normaliseTangStub152、applyRomanceLanOverrides48 函數本體、spPlayerMeta 簇。
const codeCommon = [
  extractConstStmt(htmlNew, 'YEARS66_SHIFT'),
  extractConstStmt(htmlNew, 'YEARS66_OLD_MIN'),
  extractConstStmt(htmlNew, 'YEARS66_TOKEN_RE'),
  extractConstObj(htmlNew, 'YEARS66_SKIP_KEYS'),
  extractConstObj(htmlNew, 'YEARS66_YEAR_KEYS'),
  extractFn(htmlNew, 'function years66ShiftYear('),
  extractFn(htmlNew, 'function years66ShiftText('),
  extractFn(htmlNew, 'function years66Walk('),
  extractConstObj(htmlNew, 'CLEAN100_WHEN_FIX'),
  extractFn(htmlNew, 'function contra98FixNodeWhen('),
  extractFn(htmlNew, 'function normaliseTangStub152('),
  extractFn(htmlNew, 'function applyRomanceLanOverrides48('),
  // spPlayerMeta 簇：spSoftSeasonChar 起至 spPlayerMeta 尾（含 dualMeetChromePrefersSeed）
  extractFn(htmlNew, 'function spSoftSeasonChar('),
  extractFn(htmlNew, 'function spSoftLane('),
  extractFn(htmlNew, 'function spSoftSeasonLine('),
  extractFn(htmlNew, 'function spPlayerMeta_softSeasonFrom('),
  extractFn(htmlNew, 'function dualMeetChromePrefersSeed('),
  extractFn(htmlNew, 'function spPlayerMeta_softSeason('),
  extractFn(htmlNew, 'function spPlayerMeta('),
].join('\n');
// 兩版唔同嘅表：PA 覆寫＋CONTRA98（舊版由 HEAD 抽出；組裝時先代入，避免 const 重賦值）
function assembleCode(paSrc, contraSrc) {
  return [codeCommon, paSrc, contraSrc].join('\n');
}
const codeNew = assembleCode(
  extractConstObj(htmlNew, 'ROMANCE_LAN_PA_OVERRIDES'),
  extractConstObj(htmlNew, 'CONTRA98_WHEN_FIX'));
const codeOld = assembleCode(
  extractConstObj(htmlOld, 'ROMANCE_LAN_PA_OVERRIDES'),
  extractConstObj(htmlOld, 'CONTRA98_WHEN_FIX'));

function makeCtx() {
  const ctx = {
    console,
    BehaviorGate: { featureFlag_softBehaviorGatePreview: () => false }, // LIVE 預設
    START: { y: 1990, m: 1, d: 1 },
    S: { dayIndex: 0 },
    calendarSeason: () => '冬',
    STORY_WIRE: { main: { nodes: [] }, romance: {} },
  };
  vm.createContext(ctx);
  return ctx;
}

function loadPacks() {
  const read = (f) => JSON.parse(fs.readFileSync(path.join(ROOT, 'content', f), 'utf8'));
  return {
    main: read('story_detail_n1_to_n17.json'),
    rom1: read('story_detail_romance_vera_hiu_choi.json'),
    rom2: read('story_detail_romance_lan_xu.json'),
    rival: read('story_detail_rival_mentor.json'),
  };
}

// 真實次序（refreshCopyPacksFromDisk）：
//   STORY_WIRE 賦值 → applyRomanceLanOverrides48（PA）→ normaliseTangStub152
//   → textfix（唔影響 when）→ contra98FixNodeWhen → years66Walk
function runPipeline(htmlCode) {
  const ctx = makeCtx();
  vm.runInContext(htmlCode, ctx);
  const packs = loadPacks();
  ctx.STORY_WIRE.main = packs.main;
  ctx.STORY_WIRE.romance = { veraHiuChoi: packs.rom1, lanXu: packs.rom2 };
  ctx.STORY_WIRE.rival = packs.rival;
  vm.runInContext('applyRomanceLanOverrides48();', ctx);
  vm.runInContext('normaliseTangStub152(' + 'STORY_WIRE.romance.lanXu' + ');', ctx);
  vm.runInContext('contra98FixNodeWhen([STORY_WIRE.main, STORY_WIRE.romance.veraHiuChoi, STORY_WIRE.romance.lanXu, STORY_WIRE.rival]);', ctx);
  vm.runInContext('[STORY_WIRE.main, STORY_WIRE.romance.veraHiuChoi, STORY_WIRE.romance.lanXu, STORY_WIRE.rival].forEach(p=>years66Walk(p, null));', ctx);
  // 收集 when／eraTag／LIVE 頁首
  const out = {};
  for (const p of [packs.main, packs.rom1, packs.rom2, packs.rival]) {
    for (const n of (p.nodes || [])) {
      if (!n || !n.id) continue;
      ctx.__n = n;
      const header = vm.runInContext('spPlayerMeta(__n, null, null)', ctx);
      out[n.id] = { when: n.when, eraTag: n.eraTag, header };
    }
  }
  return out;
}

const EXPECT_WHEN = {
  R_hiu_crisis: '1991秋',
  R_choi_crisis: '1991冬',
  R_lan_ending: '1992秋',
  R_xu_ending: '1992秋',
  R_hiu_ending: '1992秋',
  R_choi_ending: '1992秋',
  R_tang_meet_stub: '1991秋',
};
const TARGETS = Object.keys(EXPECT_WHEN);

console.log('=== A. 新表 pipeline：when 顯示值 ===');
const resNew = runPipeline(codeNew);
for (const id of TARGETS) {
  ok(id + ' when=' + EXPECT_WHEN[id], resNew[id] && resNew[id].when === EXPECT_WHEN[id],
    'got when=' + JSON.stringify(resNew[id] && resNew[id].when));
}

console.log('=== B. 新表 pipeline：LIVE 頁首 spPlayerMeta（eraTag 優先路徑） ===');
for (const id of TARGETS) {
  const wantHeader = '主線 · ' + EXPECT_WHEN[id];
  const got = resNew[id] && resNew[id].header;
  // (1) eraTag 已跟 when 一對改（統籌覆核：spPlayerMeta eraTag 優先，唔改會令頁首留 1992冬）：同其他節點一樣斷言頁首。
  ok(id + ' header=' + wantHeader, got === wantHeader, 'got ' + JSON.stringify(got));
}

console.log('=== C. 舊表（main 5580f8d）對照：改前值，證明修復有實效 ===');
const resOld = runPipeline(codeOld);
const EXPECT_OLD_WHEN = {
  R_hiu_crisis: '1992秋', R_choi_crisis: '1992冬',
  R_lan_ending: '1992冬', R_xu_ending: '1992冬',
  R_hiu_ending: '1992冬', R_choi_ending: '1992冬',
  R_tang_meet_stub: '1993',
};
for (const id of TARGETS) {
  ok(id + ' 舊 when=' + EXPECT_OLD_WHEN[id], resOld[id] && resOld[id].when === EXPECT_OLD_WHEN[id],
    'got ' + JSON.stringify(resOld[id] && resOld[id].when));
}
ok('stub 舊 header=1993秋（1993 bug 實證）', resOld.R_tang_meet_stub.header === '主線 · 1993秋',
  'got ' + JSON.stringify(resOld.R_tang_meet_stub.header));

console.log('=== D. 其餘節點顯示值不變（新表 vs 舊表，全四 pack 逐個比對） ===');
let diffCount = 0;
const allIds = new Set([...Object.keys(resNew), ...Object.keys(resOld)]);
for (const id of allIds) {
  if (TARGETS.includes(id)) continue;
  const a = resNew[id], b = resOld[id];
  if (!a || !b) { console.log('NOTE ' + id + ' 只喺一邊出現'); continue; }
  if (a.when !== b.when || a.eraTag !== b.eraTag || a.header !== b.header) {
    diffCount++;
    console.log('FAIL diff ' + id + ' old=' + JSON.stringify(b) + ' new=' + JSON.stringify(a));
  }
}
ok('非目標節點 0 差異（共比對 ' + (allIds.size - TARGETS.length) + ' 個）', diffCount === 0, diffCount + ' 處差異');

console.log('=== E. CONTRA98 其餘表項原封不動 ===');
const oldTable = vm.runInContext(extractConstObj(htmlOld, 'CONTRA98_WHEN_FIX') + ' CONTRA98_WHEN_FIX;', makeCtx());
const newTable = vm.runInContext(extractConstObj(htmlNew, 'CONTRA98_WHEN_FIX') + ' CONTRA98_WHEN_FIX;', makeCtx());
const changedKeys = Object.keys(newTable).filter(k => (k in oldTable) && JSON.stringify(newTable[k]) !== JSON.stringify(oldTable[k]));
const addedKeys = Object.keys(newTable).filter(k => !(k in oldTable));
console.log('改動表項：' + JSON.stringify(changedKeys) + '；新增表項：' + JSON.stringify(addedKeys));
ok('只改 5 項＋新增 stub 1 項',
  changedKeys.length === 5 && addedKeys.length === 1 && addedKeys[0] === 'R_tang_meet_stub' &&
  ['R_xu_ending', 'R_hiu_ending', 'R_choi_ending', 'R_hiu_crisis', 'R_choi_crisis'].every(k => changedKeys.includes(k)),
  'changed=' + JSON.stringify(changedKeys) + ' added=' + JSON.stringify(addedKeys));

console.log(fails.length === 0 ? '\nALL PASS' : '\nFAILURES: ' + fails.join(' | '));
process.exit(fails.length === 0 ? 0 : 1);
