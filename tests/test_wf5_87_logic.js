/* v20a87 WF5 邏輯測試：觸達修復（巧遇節拍 store 錯配／getFlag alias）＋標籤衍生＋變體覆寫。
   反證行法：WF5_INDEX=~/workspace/linji-work86/index.html node tests/test_wf5_87_logic.js
   → F1/F2/F3/變體段應該 FAIL（v86 冇修復）；預設行 work87 index 應該全 PASS。 */
'use strict';
const fs = require('fs');
const path = require('path');
const INDEX = process.env.WF5_INDEX || path.join(__dirname, '..', 'index.html');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(INDEX, 'utf8');
let pass = 0, fail = 0;
function ok(name, cond) { if (cond) { pass++; } else { fail++; console.log('FAIL: ' + name); } }

function extractFn(sig) {
  const s = html.indexOf(sig);
  if (s < 0) return null;
  let i = html.indexOf('{', s), d = 0, inS = null, esc = false, k;
  for (k = i; k < html.length; k++) {
    const c = html[k];
    if (inS) { if (esc) esc = false; else if (c === '\\') esc = true; else if (c === inS) inS = null; continue; }
    if (c === '"' || c === "'" || c === '`') { inS = c; continue; }
    if (c === '{') d++; else if (c === '}') { d--; if (!d) break; }
  }
  return html.slice(s, k + 1);
}
function extractConst(name) {
  const s = html.indexOf('const ' + name);
  if (s < 0) return null;
  const eq = html.indexOf('=', s);
  let i = html.indexOf('{', eq), j = html.indexOf('[', eq);
  if (j >= 0 && (i < 0 || j < i)) i = j;
  const open = html[i], close = open === '{' ? '}' : ']';
  let d = 0, inS = null, esc = false, k;
  for (k = i; k < html.length; k++) {
    const c = html[k];
    if (inS) { if (esc) esc = false; else if (c === '\\') esc = true; else if (c === inS) inS = null; continue; }
    if (c === '"' || c === "'" || c === '`') { inS = c; continue; }
    if (c === open) d++; else if (c === close) { d--; if (!d) break; }
  }
  return html.slice(i, k + 1);
}
function loadPack(f) { return JSON.parse(fs.readFileSync(path.join(ROOT, 'content', f), 'utf8')); }

/* ================= F2：巧遇節拍 store 錯配（ching_after_*／chai_repay） ================= */
(function () {
  const helper = extractFn('function enc87StoryFlag');
  ok('F2 enc87StoryFlag 存在', !!helper);
  const chingSrc = (() => {
    const s = html.indexOf('ENC79_BEATS.ching_tinlok = [');
    if (s < 0) return null;
    let i = html.indexOf('[', s), d = 0, inS = null, esc = false, k;
    for (k = i; k < html.length; k++) {
      const c = html[k];
      if (inS) { if (esc) esc = false; else if (c === '\\') esc = true; else if (c === inS) inS = null; continue; }
      if (c === '"' || c === "'") { inS = c; continue; }
      if (c === '[') d++; else if (c === ']') { d--; if (!d) break; }
    }
    return html.slice(i, k + 1);
  })();
  ok('F2 ching beats 抽到', !!chingSrc);
  if (!helper || !chingSrc) return;
  const doneSet = new Set(['C16']);
  const sandbox = {
    S: { flags: {}, story: { flags: { flag_vocal_train: 1 }, done: { C16: true } } },
    enc83NodeDone: (id) => doneSet.has(id),
    enc79TierOf: (fav) => (fav >= 70 ? 4 : 0),
  };
  const beats = new Function('S', 'enc83NodeDone', 'enc79TierOf',
    helper + '\nreturn ' + chingSrc + ';')(sandbox.S, sandbox.enc83NodeDone, sandbox.enc79TierOf);
  const byId = {}; beats.forEach(b => byId[b.id] = b);
  const st = { fav: 30 };
  /* C16 揀苦練（flag 只入 story.flags——真實 play 嘅寫入 store）→ after_train 要開 */
  ok('F2 after_train：story.flags 有 flag_vocal_train → 開', byId.ching_after_train.when(st) === true);
  ok('F2 after_polish：冇 polish 旗 → 唔開', byId.ching_after_polish.when(st) === false);
  /* 旗喺 S.flags（舊存檔／其他寫入路）都要開（雙 store 兼容） */
  sandbox.S.story.flags = {}; sandbox.S.flags = { flag_vocal_polish: 1 };
  ok('F2 after_polish：S.flags 有旗 → 開', byId.ching_after_polish.when(st) === true);
  ok('F2 after_train：兩邊都冇旗 → 唔開', byId.ching_after_train.when(st) === false);
  /* C16 未完成 → 點都唔開 */
  doneSet.delete('C16'); sandbox.S.story.flags = { flag_vocal_train: 1 };
  ok('F2 after_train：C16 未 done → 唔開', byId.ching_after_train.when(st) === false);
})();

/* ================= F1：StoryOC.getFlag alias ================= */
(function () {
  const src = extractFn('function getFlag(');
  ok('F1 getFlag 抽到', !!src);
  if (!src) return;
  ok('F1 getFlag 含 alias 修復', src.indexOf('前綴 alias') >= 0);
  const st = { flags: { choi_honest: true }, routes: { route_tv: true } };
  const S = { flags: {} };
  const getFlag = new Function('ensure', 'S', 'return ' + src + ';')(() => st, S);
  ok('F1 裸名 choi_honest 接通 flag_choi_honest', getFlag('flag_choi_honest') === true);
  ok('F1 本名 choi_honest 照開', getFlag('choi_honest') === true);
  ok('F1 未有嘅旗唔好誤開', getFlag('flag_choi_spin') === false);
  ok('F1 route_tv 照舊', getFlag('route_tv') === true);
  st.flags = { flag_tang_open: 1 };
  ok('F1 反向：flag_ 旗接通裸名查詢', getFlag('tang_open') === true);
})();

/* ================= F3：標籤衍生 ================= */
(function () {
  const names = ['spSoftSeasonChar(raw)', 'spSoftLane(node)', 'spSoftSeasonLine(ch, node)', 'dualMeetChromePrefersSeed(node)', 'spPlayerMeta_softSeasonFrom(node, src)', 'spPlayerMeta(node, pack, label)', 'spPlayerMeta_softSeasonSelfCheck()'];
  const srcs = names.map(n => extractFn('function ' + n));
  ok('F3 標籤函數齊', srcs.every(Boolean));
  const shift = extractFn('function years66ShiftYear');
  ok('F3 years66ShiftYear 抽到', !!shift);
  if (!srcs.every(Boolean) || !shift) return;
  const env = new Function('START', 'BehaviorGate', 'spIsForcedStory',
    'const YEARS66_SHIFT = 2, YEARS66_OLD_MIN = 1988, YEARS66_OLD_MAX = 1992;\n' +
    shift + '\n' + srcs.join('\n') +
    '\nreturn { spPlayerMeta, spPlayerMeta_softSeasonFrom, spPlayerMeta_softSeasonSelfCheck };'
  )({ y: 1990 }, { featureFlag_softBehaviorGatePreview: () => false }, () => false);
  const LIVE = (node) => env.spPlayerMeta(node, null, null);
  const SOFT = (node) => env.spPlayerMeta_softSeasonFrom(node, {});
  /* LIVE：年份＋季節齊（修前：夏／冬節點得裸年份） */
  ok('F3 LIVE C9 = 1991冬', LIVE({ id: 'C9', eraTag: 'era_1989_winter_pressure', when: '1991冬' }) === '主線 · 1991冬');
  ok('F3 LIVE C13 = 1992冬', LIVE({ id: 'C13', eraTag: 'era_1990_winter_newyear', when: '1992冬' }) === '主線 · 1992冬');
  ok('F3 LIVE C7 = 1991夏', LIVE({ id: 'C7', eraTag: 'era_1989_summer_action', when: '1991夏' }) === '主線 · 1991夏');
  ok('F3 LIVE C14 = 1992夏', LIVE({ id: 'C14', eraTag: 'era_1990_summer_war', when: '1992夏' }) === '主線 · 1992夏');
  ok('F3 LIVE C8 = 1991秋', LIVE({ id: 'C8', eraTag: 'era_1989_autumn_commercial', when: '1991秋' }) === '主線 · 1991秋');
  ok('F3 LIVE C15 = 1992春', LIVE({ id: 'C15', eraTag: 'era_1990_spring_action', when: '1992春' }) === '主線 · 1992春');
  ok('F3 LIVE C6 全年冇季節', LIVE({ id: 'C6', eraTag: 'era_1988_canteen', when: '1990' }) === '主線 · 1990');
  ok('F3 LIVE C18 = 1990冬', LIVE({ id: 'C18', eraTag: 'era_1988_winter_agency', when: '1990冬' }) === '主線 · 1990冬');
  /* v20a98 CONTRA98 A-03：標籤格式（主線 · YYYY季）不變，但季節跟返開局曆法——
     START=1990-01-01・冬、開始按鈕寫「1990 年冬」、JAN67 已將 C1 when 改「1990冬」；
     原期望「春」係 v67 一月開局改版漏改嗰行硬編碼，屬硬矛盾，已修正為「冬」。 */
  ok('F3 LIVE C1 批准標籤不變', LIVE({ id: 'C1' }) === '主線 · 1990冬');
  /* F3d：forced session（進度頁「播呢幕」force 播）唔准再短路標籤——修前任何節點都變 1990春 */
  const envF = new Function('START', 'BehaviorGate', 'spIsForcedStory',
    'const YEARS66_SHIFT = 2, YEARS66_OLD_MIN = 1988, YEARS66_OLD_MAX = 1992;\n' +
    shift + '\n' + srcs.join('\n') +
    '\nreturn { spPlayerMeta };'
  )({ y: 1990 }, { featureFlag_softBehaviorGatePreview: () => false }, () => true);
  ok('F3d forced 播 C9 仍標 1991冬', envF.spPlayerMeta({ id: 'C9', eraTag: 'era_1989_winter_pressure', when: '1991冬' }, null, null) === '主線 · 1991冬');
  ok('F3d forced 播 C1 仍標 1990冬', envF.spPlayerMeta({ id: 'C1' }, null, null) === '主線 · 1990冬'); /* v20a98 CONTRA98 A-03 同上 */
  /* soft：年份跟節點 when（修前一律 1990） */
  ok('F3 soft C9 = 1991冬', SOFT({ id: 'C9', when: '1991冬', eraTag: 'era_1989_winter_pressure' }) === '主線 · 1991冬');
  ok('F3 soft C13 = 1992冬', SOFT({ id: 'C13', when: '1992冬', eraTag: 'era_1990_winter_newyear' }) === '主線 · 1992冬');
  ok('F3 soft C15 = 1992春', SOFT({ id: 'C15', when: '1992春', eraTag: 'era_1990_spring_action' }) === '主線 · 1992春');
  ok('F3 soft C19 = 1991春', SOFT({ id: 'C19', when: '1991春', eraTag: 'era_1989_spring_gamble' }) === '主線 · 1991春');
  ok('F3 soft C18 = 1990冬', SOFT({ id: 'C18', when: '1990冬', eraTag: 'era_1988_winter_agency' }) === '主線 · 1990冬');
  /* 內置 selfCheck：唔准有新失敗（dual* 四項係 1988 stub 世界嘅舊文字期望，修前修後同樣在列） */
  const chk = env.spPlayerMeta_softSeasonSelfCheck();
  const knownStale = ['dualSeedChrome', 'dualNoSeed', 'choiSpringCal', 'choiAutumnCal'];
  const newFails = (chk.fails || []).filter(f => !knownStale.some(k => f.indexOf(k) === 0));
  ok('F3 selfCheck 冇新失敗（實際 fails: ' + (chk.fails || []).join(',') + '）', newFails.length === 0);
})();

/* ================= 變體覆寫 ================= */
(function () {
  const ovSrc = extractConst('WF5_VARIANT_OVERRIDES87');
  const fnSrc = extractFn('function applyVariantWf5Overrides87');
  ok('變體 覆寫表存在', !!ovSrc);
  ok('變體 apply 函數存在', !!fnSrc);
  if (!ovSrc || !fnSrc) return;
  const applyVariantWf5Overrides87 = new Function('var WF5_VARIANT_OVERRIDES87 = ' + ovSrc + ';\n' + fnSrc + '\nreturn applyVariantWf5Overrides87;')();
  const OV_KEYS = Object.keys(eval('(' + ovSrc + ')'));
  const files = ['MOCK_STORY_DENG_LINE_MEET_SOFT_v1.1.json', 'MOCK_STORY_DENG_LINE_PUSH_SOFT_v1.json', 'MOCK_STORY_DUAL_MEET_THICKEN_SOFT_v1.json'];
  const orig = files.map(loadPack);
  const work = JSON.parse(JSON.stringify(orig));
  const applied = applyVariantWf5Overrides87(work[0], work[1], work[2]);
  ok('變體 套用節點數 = 7', applied === 7);
  const nodesOf = (packs) => packs.flatMap(p => [].concat(p.beats || [], p.nodes || [])).filter(n => n && n.id && Array.isArray(n.beats));
  const before = nodesOf(orig), after = nodesOf(work);
  const CANTO = ['嘅', '喺', '唔', '佢', '哋', '咗', '冇', '畀', '嚟', '㗎', '嗰', '呢', '先', '返', '埋', '攞', '睇', '講'];
  const density = (ns) => { let tot = 0, hit = 0; for (const n of ns) { const t = JSON.stringify(n.beats) + (n.synopsis || ''); tot += t.length; for (const c of CANTO) hit += t.split(c).length - 1; } return hit / Math.max(1, tot); };
  ok('變體 廣東話標記密度顯著上升（' + density(before).toFixed(4) + ' → ' + density(after).toFixed(4) + '）', density(after) > density(before) * 3);
  const byId = {}; after.forEach(n => byId[n.id] = n);
  const byId0 = {}; before.forEach(n => byId0[n.id] = n);
  /* 結構不變量：beat 數／行數／speaker／choice id+flags+stats／chrome／playerMeta／openConditions 逐一冇郁 */
  let structOk = true;
  for (const id of OV_KEYS) {
    const a = byId0[id], b = byId[id];
    if (!a || !b) { structOk = false; break; }
    if (a.beats.length !== b.beats.length) structOk = false;
    a.beats.forEach((bt, i) => { if (bt.speaker !== b.beats[i].speaker || bt.lines.length !== b.beats[i].lines.length) structOk = false; });
    if (JSON.stringify((a.choices || []).map(c => [c.id, (c.effects || {}).flags, (c.effects || {}).stats])) !==
        JSON.stringify((b.choices || []).map(c => [c.id, (c.effects || {}).flags, (c.effects || {}).stats]))) structOk = false;
    if (a.playerMeta !== b.playerMeta || a.chromeSeason !== b.chromeSeason) structOk = false;
    if (JSON.stringify(a.openConditions || null) !== JSON.stringify(b.openConditions || null)) structOk = false;
  }
  ok('變體 結構不變量全保', structOk);
  /* 鄧麗萍收尾同 WF2 定版咬合 */
  const end = byId.R_tang_ending, endTxt = JSON.stringify(end.beats);
  for (const k of ['紅筆圈住', '呢格，我睇好你', '改咗把尺', '百分之七', '五成九', '留返喺個紅圈入面'])
    ok('變體 ending 含關鍵句「' + k + '」', endTxt.indexOf(k) >= 0 || JSON.stringify(end).indexOf(k) >= 0);
  const labels = {}; (end.choices || []).forEach(c => labels[c.id] = c.label);
  ok('變體 ending HE label = WF2 定版', labels.C_tang_ending_he === '企返喺張表嗰邊：用一個數字，應承佢嗰格');
  ok('變體 ending BE label = WF2 定版', labels.C_tang_ending_be === '數字至上：收返嗰格，各行各路');
  ok('變體 ending 冇「跨越商業界線」舊味', JSON.stringify(end).indexOf('跨越商業界線') < 0);
  /* 禁詞＋年份數字（DengLine selfCheck 口徑） */
  const dengAll = JSON.stringify([byId.R_tang_meet, byId.R_tang_push1, byId.R_tang_push2, byId.R_tang_crisis, byId.R_tang_ending]);
  for (const b of ['關海媚', '陳淑芬', '施南生', 'Ho哥', 'nextHint']) ok('變體 鄧線冇禁詞「' + b + '」', dengAll.indexOf(b) < 0);
  ok('變體 鄧線 beats 冇 1989–1992 數字', !/19(89|90|91|92)/.test(JSON.stringify([byId.R_tang_push1.beats, byId.R_tang_push2.beats, byId.R_tang_crisis.beats, byId.R_tang_ending.beats])));
  /* 采兒 meet：週刊正字＋M33 口徑 */
  const choi = byId.R_choi_meet, choiVis = JSON.stringify({ t: choi.title, s: choi.setting, y: choi.synopsis, b: choi.beats });
  ok('變體 采兒 meet 用《星訊週刊》', choiVis.indexOf('《星訊週刊》') >= 0);
  ok('變體 采兒 meet 玩家可見文本冇簡體「周刊」', choiVis.indexOf('周刊') < 0);
  ok('變體 采兒 meet 有 M33 口徑（唔害人／獨家）', choiVis.indexOf('唔害人') >= 0 && choiVis.indexOf('獨家') >= 0);
})();

/* ================= C6 閘 + verify37 fixture ================= */
(function () {
  const gate = eval('(' + extractConst('STORY_GATE_3Y') + ')');
  ok('C6 閘 = route_tv + weekMin 15', gate.C6 && gate.C6.route === 'route_tv' && gate.C6.weekMin === 15);
  const main = loadPack('story_detail_c1_to_c17.json');
  const c1 = main.nodes.find(n => n.id === 'C1');
  ok('C1_a 寫 route_tv（C6 有生產者）', c1.choices.some(c => ((c.effects || {}).flags || []).indexOf('route_tv') >= 0));
  const v37 = fs.readFileSync(path.join(ROOT, 'tests', 'test_verify37_logic.js'), 'utf8');
  ok('verify37 fixture 已改 route_tv', v37.indexOf('routes: { route_tv: true }') >= 0 && v37.indexOf('routes: { tv: true }') < 0);
})();

console.log('test_wf5_87_logic: PASS ' + pass + ' / FAIL ' + fail + '（index: ' + INDEX + '）');
process.exit(fail ? 1 : 0);
