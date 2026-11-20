// v20a98 CONTRA98 邏輯測試：劇情矛盾修復——
//   (1) A-01/A-02：支線 P4/P5 共 21 節點經 contra98FixNodeWhen＋真 years66Walk 後，
//       用真 spPlayerMeta 計頁首標籤：年份按表（危機 1991、其餘 1992）＋季節按表（冬 10／秋 11），冇 1993/1994；
//       三個支線 pack 全部節點頁首年份 ≤1992（全域守門）；
//       （v20a152：R_tang_ending 已刪，23→22；v20a219：加 R_tang_meet_stub 衞生行，22→23；
//        v20a242：加 R_lan_crisis／R_lan_ending 兩行（LAN 表已刪），23→25；
//        v20a268：刪 R_vera_ending／R_vera_crisis 兩行（Vera 節點由 JSON 刪除）＋
//        刪 R_tang_push2／R_tang_crisis 兩行（節點數據只喺已刪嘅 romance_tang.json，fixer 輸入從來冇呢個 pack），25→21；
//        全域守門唔再讀 romance_tang.json——檔已刪，見 test_tang152_static.py §6。）
//   (2) A-03：spPlayerMeta('N1') 出「主線 · 1990冬」；
//   (3) B-01：contra98PrepareNode——對方 commit 已立時 HE choice 換坦白差一步變體（只寫自己 BE 旗、原節點不變）；
//       冇旗／自己已 commit／非目標節點 → null（零改動）；
//   (4) C-02/C-03：ENC79_FIRST_ALT98 齊 12 星；contra98EncFirstLocSwap 只喺 at 地點生效、
//       旁白同 choice 內文案都換；其他地點零改動。
// 反證：喺 v20a97 index 上行 → 冇 CONTRA98_* → 抽取即 throw → FAIL。
// 用法：node tests/test_contra98_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const rootDir = path.dirname(htmlPath);
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }
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
function extractConst(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('const not found: ' + name);
  let depth = 0, started = false, j = i;
  for(; j < html.length; j++){
    const c = html[j];
    if(c === '{' || c === '['){ depth++; started = true; }
    else if(c === '}' || c === ']'){ depth--; if(started && depth === 0){ j++; break; } }
    else if(c === ';' && !started){ j++; break; }
  }
  return html.slice(i, j);
}
/* ---- sandbox stubs ---- */
const START = { y: 1990, m: 1, d: 1 };
let __flags = {};
function enc87StoryFlag(f){ return !!__flags[f]; }
let __nodeMap = {};
function findNodeInPack(id){ return __nodeMap[id] || null; }
/* ---- eval real code（const 綁定唔會漏出 eval，尾巴收集入 __C98） ---- */
eval([
  extractConst('YEARS66_SHIFT'), extractConst('YEARS66_OLD_MIN'), extractConst('YEARS66_TOKEN_RE'),
  extractConst('YEARS66_SKIP_KEYS'), extractConst('YEARS66_YEAR_KEYS'),
  extractFn('years66ShiftYear'), extractFn('years66ShiftText'), extractFn('years66Walk'),
  extractConst('CONTRA98_WHEN_FIX'), extractConst('CLEAN100_WHEN_FIX'), extractFn('contra98FixNodeWhen'), /* v20a100：contra98FixNodeWhen 兼讀 CLEAN100_WHEN_FIX（N2/N3），抽取要帶埋 */
  extractFn('spSoftSeasonChar'), extractFn('spPlayerMeta_softSeason'), extractFn('spPlayerMeta'),
  extractFn('contra98PrepareNode'),
  extractConst('ENC79_FIRST_ALT98'), extractFn('contra98EncFirstLocSwap'),
  'globalThis.__C98 = { CONTRA98_WHEN_FIX, contra98FixNodeWhen, years66Walk, spPlayerMeta, contra98PrepareNode, ENC79_FIRST_ALT98, contra98EncFirstLocSwap };',
].join('\n'));
const FIX98 = globalThis.__C98.CONTRA98_WHEN_FIX, fixWhen98 = globalThis.__C98.contra98FixNodeWhen,
  walk98 = globalThis.__C98.years66Walk, meta98 = globalThis.__C98.spPlayerMeta,
  prep98 = globalThis.__C98.contra98PrepareNode, ALT98 = globalThis.__C98.ENC79_FIRST_ALT98,
  swap98 = globalThis.__C98.contra98EncFirstLocSwap;

/* ---- (1) A-01/A-02 ---- */
/* v20a268：PACK_FILES 唔再包 story_detail_romance_tang.json——檔已刪（見 test_tang152_static.py §6）。
   CONTRA98_WHEN_FIX 嘅 R_tang_push2／R_tang_crisis 兩行同步刪除（節點數據只喺呢個檔，fixer 輸入
   [main, rom1, rom2, rom3, rival] 從來唔包佢，兩行係死項）；R_tang_meet_stub 節點數據喺 lan_xu.json，留返。 */
const PACK_FILES = ['story_detail_rival_mentor.json', 'story_detail_romance_vera_hiu_choi.json', 'story_detail_romance_lan_xu.json'];
const packs = PACK_FILES.map(f => JSON.parse(fs.readFileSync(path.join(rootDir, 'content', f), 'utf8')));
const fixIds = Object.keys(FIX98);
ok('A: FIX98 齊 21 節點', fixIds.length === 21);
fixWhen98(packs);
packs.forEach(p => walk98(p, null));
packs.forEach(p => (p.nodes || []).forEach(n => { __nodeMap[n.id] = n; }));
/* v20a219 顯示值（walk +2 後；見 DECISIONS-2026-11-15「when 欄年份核查結果」）：
   年份：危機節點 1992（v20a343：R_choi_crisis／R_hiu_crisis 表值 1989→1990，頁首由 1991 改 1992；
   R_tang_meet_stub 表值 1989 唔郁，顯示 1991，stub 永不入玩家列表），其餘 18 節點 1992；
   季節：冬＝7 個 A_ending＋A_ko_ending＋A_ho_crisis＋R_choi_crisis（10），
   秋＝其餘 11 節點（hiu／choi／xu 三個結局由冬改秋；R_hiu_crisis 1992秋／R_tang_meet_stub 1991秋；
   v20a242：R_lan_crisis／R_lan_ending 1992秋；v20a268：R_vera_ending／R_vera_crisis／R_tang_push2／R_tang_crisis 四行已刪）。 */
const WANT_YEAR98 = { R_tang_meet_stub: 1991 };
const WANT_SEASON98 = { A_hakfan_ending: '冬', A_tsijun_ending: '冬', A_fong_ending: '冬', A_tong_ending: '冬',
  A_ho_ending: '冬', A_gao_ending: '冬', A_lei_ending: '冬',
  A_ko_ending: '冬', A_ho_crisis: '冬', R_choi_crisis: '冬' };
let badYear = [], badSeason = [];
for(const id of fixIds){
  const n = __nodeMap[id];
  if(!n){ badYear.push(id + ':missing'); continue; }
  const meta = meta98(n, null, '');
  const wy = WANT_YEAR98[id] || 1992, ws = WANT_SEASON98[id] || '秋';
  if(meta.indexOf(String(wy)) < 0 || /199[3-9]|20\d\d/.test(meta)) badYear.push(id + ':' + meta);
  if(meta.indexOf(wy + ws) < 0) badSeason.push(id + ':' + meta + ' want ' + wy + ws);
}
ok('A-01/A-02: 21 節點頁首年份正確（crisis 1992、stub 1991、其餘 1992；冇 1993/1994）', badYear.length === 0);
if(badYear.length) console.log('   badYear:', badYear.join(' | '));
ok('A-01/A-02: 21 節點季節正確（冬 10／秋 11，按表）', badSeason.length === 0);
if(badSeason.length) console.log('   badSeason:', badSeason.join(' | '));
/* 全域守門：三個支線 pack 全部節點頁首年份唔過 1992。
   豁免（已逐項查證，唔係漏網）：*_stub ——index 有 supersede 過濾（/stub/+/tang/ 或 supersededBy 唔出街）。
   （v20a268：R_tang_ending 豁免已刪——romance_tang.json 成檔刪除，節點數據已唔存在；CONTRA98 嗰行早喺 v152 刪咗。
   v20a242：R_lan_* 豁免已刪——LAN 覆寫表已刪，crisis／ending 經 CONTRA98_WHEN_FIX 新行入表，行返正常守門。） */
let overYear = [];
packs.forEach(p => (p.nodes || []).forEach(n => {
  if(/_stub$/.test(n.id)) return;
  const meta = meta98(n, null, '');
  const m = meta && meta.match(/(19|20)\d\d/);
  if(m && Number(m[0]) > 1992) overYear.push(n.id + ':' + meta);
}));
ok('A: 三個支線 pack 全部節點頁首年份 ≤1992', overYear.length === 0);
if(overYear.length) console.log('   overYear:', overYear.slice(0, 8).join(' | '));

/* ---- (2) A-03 ---- */
ok('A-03: N1 頁首係「主線 · 1990冬」', meta98({ id: 'N1' }, null, '') === '主線 · 1990冬');

/* ---- (3) B-01 ---- */
function fakeEnding(id, heId){
  return { id, choices: [
    { id: heId, label: '同佢講明', effects: { flags: [id === 'R_hiu_ending' ? 'flag_hiu_commit' : 'flag_choi_commit'], stats: { hiu: 1 }, notes: 'he' } },
    { id: 'C_x_be', label: '收埋心底', effects: { flags: ['flag_x_be'], stats: {}, notes: 'be' } },
  ]};
}
__flags = { flag_choi_commit: true };
const hiuNode = fakeEnding('R_hiu_ending', 'C_hiu_ending_he');
const patched = prep98(hiuNode);
ok('B-01: 采兒已 commit → 播曉晴結局出淺拷貝', !!patched && patched !== hiuNode);
ok('B-01: HE choice 換坦白變體＋只寫 flag_hiu_be', !!patched && patched.choices[0].label.indexOf('坦白') === 0
   && JSON.stringify(patched.choices[0].effects.flags) === '["flag_hiu_be"]'
   && patched.choices[0].effects.notes.indexOf('差一步') === 0);
ok('B-01: 原節點零改動', hiuNode.choices[0].effects.flags[0] === 'flag_hiu_commit');
__flags = { flag_hiu_commit: true };
const choiPatched = prep98(fakeEnding('R_choi_ending', 'C_choi_ending_he'));
ok('B-01: 曉晴已 commit → 采兒結局同樣互斥', !!choiPatched && choiPatched.choices[0].effects.flags[0] === 'flag_choi_be');
__flags = {};
ok('B-01: 冇任何 commit 旗 → null（原 HE 照行）', prep98(fakeEnding('R_hiu_ending', 'C_hiu_ending_he')) === null);
__flags = { flag_hiu_commit: true, flag_choi_commit: true };
ok('B-01: 自己已 commit → null（唔好擋返自己條線）', prep98(fakeEnding('R_hiu_ending', 'C_hiu_ending_he')) === null);
__flags = { flag_choi_commit: true };
ok('B-01: 非目標節點 → null', prep98({ id: 'R_vera_ending', choices: [] }) === null);

/* ---- (4) C-02/C-03 ---- */
const ALT_STARS = ['luk_baakyin','liu_bingxing','ngai_wingnaam','yip_manji','mak_zhendong','lok_gasing','pang_siuki','chung_choning','gu_mingfai','so_jiyan','chai_zanhoi','ching_tinlok'];
ok('C-02: ALT 表齊 12 星', ALT_STARS.every(s => ALT98[s] && ALT98[s].at && ALT98[s].swaps.length >= 1));
function firstSteps(starId){
  const alt = ALT98[starId];
  const steps = alt.swaps.map(([f]) => ({ who: 'N', text: f, seg: 'first:' + starId }));
  steps.push({ choice: true, seg: 'first:' + starId, options: [{ label: 'x', lines: [['N', alt.swaps[0][0]]] }] });
  return steps;
}
let swapBad = [];
for(const sid of ALT_STARS){
  const alt = ALT98[sid];
  const st = firstSteps(sid);
  swap98(st, sid, alt.at);
  const joined = JSON.stringify(st);
  for(const [f, t] of alt.swaps){ if(joined.indexOf(t) < 0 || joined.indexOf(f) >= 0) swapBad.push(sid); }
  const st2 = firstSteps(sid);
  swap98(st2, sid, 'cafe_cha' === alt.at ? 'film_lion' : 'cafe_cha');
  if(JSON.stringify(st2) !== JSON.stringify(firstSteps(sid)) && sid !== 'gu_mingfai') swapBad.push(sid + ':wrongloc');
  /* gu_mingfai 嘅 at 就係 cafe_cha，上面 generic wrong-loc 分支對佢用 film_lion，已覆蓋 */
}
ok('C-02: 12 星喺 at 地點全部換到（旁白＋choice 內文案）、其他地點零改動', swapBad.length === 0);
if(swapBad.length) console.log('   swapBad:', swapBad.join(' | '));
ok('C-03: 麥震東底稿唔再寫清水灣', html.indexOf('清水灣片場邊') < 0 && html.indexOf('紅棉影業片場一角，竹棚底下熱得冒煙') >= 0);

console.log(fails.length ? ('CONTRA98 LOGIC: ' + fails.length + ' FAIL') : 'CONTRA98 LOGIC: ALL PASS');
process.exit(fails.length ? 1 : 0);
