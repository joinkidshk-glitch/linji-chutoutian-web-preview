// v20a80 WF1 邏輯測試：劇情豐富化 WF1——後段加厚＋真空帶補幕。
//   (1) 加厚完整性：C6–C17 每幕 beats ≥8 拍（C17 ≥9）、beats 字數過門檻、resultBeats 合計 ≥150（C17 除外，結局幕 choices 由 ending410 動態重建）；
//   (2) 後果拍：每幕每個 choice 都有 resultBeats（揀完有下文）；新第三 choice 旗入 flags_written、幅度唔勁過既有；
//   (3) 零回歸：既有 beats/choices/resultBeats 對 v79 fixture（tests/fixtures/spine_c6_c17_v79.json）子序列＋前綴保留；
//   (4) 補幕 C18/C19：結構（8–10 拍／2 抉擇連後果拍）、地點、when 用舊標籤（YEARS66 +2）、gate entry 規則
//       （yearMin＋seasonIn；1990冬 C18 開／1990秋唔開／1991春 C19 開／1990春唔開；冇 needDone 唔卡主線）；
//   (5) 注入：applyStoryWf1Nodes80 冪等（行兩次唔重複 push、唔覆蓋已有同 id 節點）；
//   (6) 紅線：14 節點全文冇真人名、冇關海媚名、冇直寫 1991–1994 年份。
// 反證：喺 v20a79 index 上行 → 冇 STORY_SPINE_NODES_WF1 → 抽取即 throw → FAIL。
// 用法：node tests/test_wf1_80_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }
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
const T89 = extractConst('STORY_SPINE_NODES_1989');
const T90 = extractConst('STORY_SPINE_NODES_1990');
const TC6 = extractConst('STORY_SPINE_NODES_C6');
const C17N = extractConst('STORY_SPINE_NODE_C17_410');
const WF1 = extractConst('STORY_SPINE_NODES_WF1');
const GATE = extractConst('STORY_GATE_3Y');
const CWIN = extractConst('CALIB60_NODE_WINDOWS');
const CTIT = extractConst('CALIB60_NODE_TITLES');
const NODES = Object.assign({}, T89, T90, TC6, { C17: C17N }, WF1);
const fixture = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'spine_c6_c17_v79.json'), 'utf8'));

function beatLines(n){ return (n.beats || []).flatMap(b => b.lines || []); }
function beatChars(n){ return beatLines(n).join('').length; }
function resultLines(n){ return (n.choices || []).flatMap(c => (c.resultBeats || []).flatMap(b => b.lines || [])); }
function resultChars(n){ return resultLines(n).join('').length; }
function isSubseq(sub, full){
  let k = 0;
  for(const x of full){ if(k < sub.length && x === sub[k]) k++; }
  return k === sub.length;
}

/* (1)(2) 加厚完整性 */
const FLOOR = { C6:350, C7:350, C11:350, C8:350, C9:350, C10:350, C15:350, C14:350, C12:350, C16:380, C13:350, C17:420 };
for(const id of Object.keys(FLOOR)){
  const n = NODES[id];
  ok(id + ' 節點在位', !!n);
  if(!n) continue;
  ok(id + ' beats ≥8 拍（實 ' + (n.beats || []).length + '）', (n.beats || []).length >= 8);
  ok(id + ' beats 字數 ≥' + FLOOR[id] + '（實 ' + beatChars(n) + '）', beatChars(n) >= FLOOR[id]);
  if(id !== 'C17'){
    ok(id + ' resultBeats 合計 ≥150（實 ' + resultChars(n) + '）', resultChars(n) >= 150);
    ok(id + ' 每個 choice 都有後果拍 resultBeats', (n.choices || []).every(c => (c.resultBeats || []).length >= 1));
  }
  /* C17 豁免：其 choices 播放時由 ending410EveNode 動態重建（帶 ending410Key），靜態 choices 本來就冇 resultBeats */
}
/* C17：choices 由 ending410 動態重建，靜態 choices 同 v79 逐字一致（fixture slim 口徑逐項比） */
{
  let c17ok = (C17N.choices || []).length === fixture.C17.choices.length;
  fixture.C17.choices.forEach((fc, i) => {
    const nc = (C17N.choices || [])[i] || {};
    if(nc.id !== fc.id || nc.label !== fc.label || JSON.stringify(nc.effects) !== JSON.stringify(fc.effects)) c17ok = false;
    const nRes = (nc.resultBeats || []).map(b => b.lines || []);
    if(JSON.stringify(nRes) !== JSON.stringify(fc.resultLines)) c17ok = false;
  });
  ok('C17 choices 同 v79 fixture 逐字一致', c17ok);
}

/* (3) 零回歸：對 fixture 子序列／前綴 */
for(const id of Object.keys(fixture)){
  const n = NODES[id], f = fixture[id];
  if(!n){ ok(id + ' fixture 回歸（節點在位）', false); continue; }
  ok(id + ' 既有 beats 子序列保留', isSubseq((f.beatLines || []).flat(), beatLines(n)));
  const fIds = f.choices.map(c => c.id), nIds = (n.choices || []).map(c => c.id);
  ok(id + ' 既有 choices id 子序列保留', isSubseq(fIds, nIds));
  let fxOk = true;
  for(const fc of f.choices){
    const nc = (n.choices || []).find(c => c.id === fc.id);
    if(!nc || nc.label !== fc.label || JSON.stringify(nc.effects) !== JSON.stringify(fc.effects)) fxOk = false;
    const fRes = fc.resultLines || [];
    const nRes = (((nc || {}).resultBeats) || []).map(b => b.lines || []);
    if(JSON.stringify(nRes.slice(0, fRes.length)) !== JSON.stringify(fRes)) fxOk = false;
  }
  ok(id + ' 既有 choices label/effects 不變＋resultBeats 前綴保留', fxOk);
  ok(id + ' flags_written ⊇ v79', (f.flags_written || []).every(x => (n.flags_written || []).includes(x)));
}

/* (2b) 新第三 choice：旗入帳、幅度唔勁過既有 */
const NEWC = { C7:'C7_c', C11:'C11_c', C9:'C9_c', C14:'C14_c', C12:'C12_c', C13:'C13_c' };
for(const [id, cid] of Object.entries(NEWC)){
  const n = NODES[id];
  const nc = (n.choices || []).find(c => c.id === cid);
  ok(id + ' 新 choice ' + cid + ' 在位', !!nc);
  if(!nc) continue;
  const flag = nc.effects && nc.effects.flags && nc.effects.flags[0];
  ok(cid + ' 新旗 ' + flag + ' 入 flags_written', !!flag && (n.flags_written || []).includes(flag));
  const oldMax = Math.max(...(n.choices || []).filter(c => c.id !== cid).flatMap(c => Object.values((c.effects && c.effects.stats) || {}).map(v => Math.abs(v))), 0);
  const newMax = Math.max(...Object.values((nc.effects && nc.effects.stats) || {}).map(v => Math.abs(v)), 0);
  ok(cid + ' 數值幅度唔勁過既有（' + newMax + ' ≤ ' + oldMax + '）', newMax <= oldMax);
  ok(cid + ' resultBeats ≥60 字', (nc.resultBeats || []).flatMap(b => b.lines || []).join('').length >= 60);
}

/* (4) 補幕結構＋閘 */
for(const id of ['C18', 'C19']){
  const n = NODES[id];
  ok(id + ' 節點在位', !!n);
  if(!n) continue;
  ok(id + ' beats 8–10 拍（實 ' + n.beats.length + '）', n.beats.length >= 8 && n.beats.length <= 10);
  ok(id + ' 2 抉擇＋每抉擇後果拍 ≥2', (n.choices || []).length === 2 && n.choices.every(c => (c.resultBeats || []).length >= 2));
  ok(id + ' CALIB60 時窗登記', !!CWIN[id]);
  ok(id + ' CALIB60 標題登記', typeof CTIT[id] === 'string' && CTIT[id].length > 0);
  const g = GATE[id];
  ok(id + ' gate entry 在位（yearMin＋seasonIn）', !!g && g.yearMin != null && Array.isArray(g.seasonIn));
  ok(id + ' gate 冇 needDone（唔卡主線）', !!g && !g.needDone);
}
ok('C18 地點＝何生事務所 agency_ho', NODES.C18.locId === 'agency_ho');
ok('C19 地點＝獅子山製片 film_lion', NODES.C19.locId === 'film_lion');
ok('C18 when 用舊標籤 1988冬（YEARS66 +2 → 1990冬）', NODES.C18.when === '1988冬');
ok('C19 when 用舊標籤 1989春（YEARS66 +2 → 1991春）', NODES.C19.when === '1989春');
/* gate 規則模擬（evalGate3Y 對 yearMin/seasonIn 兩項嘅文件化行為） */
function gatePass(id, year, season){
  const g = GATE[id];
  if(!g) return false;
  if(g.yearMin != null && !(year >= g.yearMin)) return false;
  if(Array.isArray(g.seasonIn) && g.seasonIn.length && !g.seasonIn.includes(season)) return false;
  if(g.yearEq != null && year !== g.yearEq) return false;
  return true;
}
ok('C18 1990冬 開', gatePass('C18', 1990, '冬'));
ok('C18 1990秋 唔開（未入冬）', !gatePass('C18', 1990, '秋'));
ok('C18 1991冬 仍開（yearMin 非 yearEq）', gatePass('C18', 1991, '冬'));
ok('C19 1991春 開', gatePass('C19', 1991, '春'));
ok('C19 1990春 唔開（未夠年份）', !gatePass('C19', 1990, '春'));
ok('C19 1991冬 唔開（過季）', !gatePass('C19', 1991, '冬'));

/* (5) 注入冪等 */
{
  const fnSrc = extractFn('applyStoryWf1Nodes80');
  const sandbox = { STORY_SPINE_NODES_WF1: WF1, STORY_WIRE: { main: { nodes: [{ id: 'C1' }] } } };
  const run = new Function('STORY_SPINE_NODES_WF1', 'STORY_WIRE', fnSrc + '\nreturn applyStoryWf1Nodes80();');
  const r1 = run(sandbox.STORY_SPINE_NODES_WF1, sandbox.STORY_WIRE);
  const ids1 = sandbox.STORY_WIRE.main.nodes.map(n => n.id);
  const r2 = run(sandbox.STORY_SPINE_NODES_WF1, sandbox.STORY_WIRE);
  const ids2 = sandbox.STORY_WIRE.main.nodes.map(n => n.id);
  ok('注入首次加入 C18/C19', r1.main === 2 && ids1.includes('C18') && ids1.includes('C19'));
  ok('注入冪等（行第二次零新增）', r2.main === 0 && JSON.stringify(ids1) === JSON.stringify(ids2));
}

/* (6) 紅線 */
{
  const all = Object.values(NODES).map(n => JSON.stringify(n)).join('\n');
  const realNames = ['周潤發', '劉德華', '張國榮', '梅艷芳', '陳百強', '鄧麗君', '成龍', '周星馳', '梁朝偉', '張曼玉', '王祖賢', '林青霞', '鍾楚紅', '李連杰', '洪金寶'];
  ok('14 節點全文冇真人名', realNames.every(x => !all.includes(x)));
  ok('全文冇關海媚名（只准稱號）', !all.includes('關海媚'));
  /* 年份紅線只管玩家面欄位；openConditionsNote 等 DEV 註解欄唔出玩家面，排除 */
  const playerTxt = ['C18', 'C19'].map(id => {
    const n = WF1[id];
    return JSON.stringify({ title: n.title, when: n.when, setting: n.setting, synopsis: n.synopsis, beats: n.beats, choices: n.choices });
  }).join('\n');
  ok('補幕玩家面欄位冇直寫 1991–1994（年份靠 +2）', !/199[1-4]/.test(playerTxt));
}

console.log(fails.length === 0 ? '\nALL PASS' : '\nFAILURES: ' + fails.join(' | '));
process.exit(fails.length === 0 ? 0 : 1);
