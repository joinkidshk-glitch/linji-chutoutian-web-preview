// v20a81 WF2 邏輯測試：感情線廣東話化＋半線差一步收尾。
//   (1) 覆寫表在位：v268 瘦身後剩 5 節點（藍 5；Vera 5 已刪——R_vera_* 節點由 JSON 刪除，覆寫表同步清走）；
//       hiu／choi／xu 15 節點已刪入 JSON（覆寫值同 JSON 逐條核實一致）；
//       合併視圖 SRC（表 5＋JSON 15）20 節點齊；
//   (2) 語體（新語言規則，用戶 2026-11-15 11:20 拍板：除咗對白之外全部書面語）：
//       對白句（speaker 唔係旁白／系統）保留廣東話標記（門檻按 P3 後對白句實測量定：
//       hiu／choi 15、xu／lan 5、半線 ending 10；實測對白句廣東話標記最低 6
//       R_xu_crisis、最高 49 R_choi_crisis），對白句書面語骨幹標記零出現；
//       旁白句（speaker 旁白／系統＋synopsis）書面語骨幹標記 ＞0（即旁白確實轉咗書面語）。
//       旁白用嘅書面語標記表 WRITTEN_NAR 比骨幹表多四個（她／如果／說／立刻），
//       因為短旁白未必撞到九個骨幹詞——例如 R_choi_crisis 旁白＋synopsis 全是書面語，
//       用骨幹表計係 0，用擴充表計係 8。
//   (3) 采兒 M33：追訪記者質地關鍵字在位（追訪／獨家／查證／通稿＋唔害人飯碗底線）；
//   (4) 半線收尾：四條 ending beats ≥450 字、各有專屬關鍵字、兩兩 bigram Jaccard <0.35（防範本換名）；
//       ending synopsis／choice label／notes 冇「確定關係／伴侶／承諾／一齊走下去」；
//   (5) merge 行為：以 v80 fixture 起假 pack（lan 節點用 content JSON 真身，v20a242）→ applyRomanceWf2Overrides81，
//       斷言 beats/synopsis 已換、choices id/flags/stats 同 fixture 逐項一致（半線 ending 只准 label/notes 變）、
//       flags_written/openConditions 不變、stub 冇被掂（v20a152：stub 改由 rom2 提供續斷言）、冪等（行兩次 applied 10→0，v241）；
//   (6) commit 回歸：COMMIT48_DEFS 同 v80 fixture 逐字一致、COMMIT48_REL_MIN=6、節點在位；
//   (7) 紅線：覆寫表全文冇真人名、冇關海媚名、beats/synopsis 冇直寫年份。
// 反證：喺 v20a80 index 上行 → 冇 ROMANCE_WF2_OVERRIDES → 抽取即 throw → FAIL。
// v20a100 CLEAN100 B-03：fixture romance_wf2_v80.json 嘅 lanPa.R_lan_push1 兩抉擇 stats
// 已跟覆寫表同步（music→stage，PA 化殘留修正）；fixture 其餘部分維持 v80 原貌。
// 用法：node tests/test_wf2_81_logic.js [path-to-index.html]
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
const T = extractConst('ROMANCE_WF2_OVERRIDES');
/* v20a241：hiu／choi／xu 15 條已由覆寫表刪入 JSON——合併視圖 SRC：表入面有就用表，冇就用 JSON pack（兩邊逐條核實一致）。 */
const _lanxu = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'content', 'story_detail_romance_lan_xu.json'), 'utf8'));
const _vhc = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'content', 'story_detail_romance_vera_hiu_choi.json'), 'utf8'));
const JBYID = {};
[..._lanxu.nodes, ..._vhc.nodes].forEach(n => { if(n && n.id) JBYID[n.id] = n; });
const DEFS = extractConst('COMMIT48_DEFS');
const CNODES = extractConst('COMMIT48_NODES');
const REL_MIN = Number((html.match(/const COMMIT48_REL_MIN = (\d+)/) || [])[1]);
const fixture = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'romance_wf2_v80.json'), 'utf8'));

const LINES = {
  hiu:  ['R_hiu_meet','R_hiu_push1','R_hiu_push2','R_hiu_crisis','R_hiu_ending'],
  choi: ['R_choi_meet','R_choi_push1','R_choi_push2','R_choi_crisis','R_choi_ending'],
  xu:   ['R_xu_meet','R_xu_push1','R_xu_push2','R_xu_crisis','R_xu_ending'],
  lan:  ['R_lan_meet','R_lan_push1','R_lan_push2','R_lan_crisis','R_lan_ending'],
  /* v20a152：tang 行已刪——R_tang_* 感情線覆寫唔再喺表入面（排片線行 DengLine mock，唔行 WF2） */
  /* v20a268：vera 行已刪——R_vera_* 節點由 JSON 刪除，覆寫表同步清走 */
};
const ALL = Object.values(LINES).flat();
const SRC = {};
for(const id of ALL){
  if(T[id]) SRC[id] = T[id];
  else {
    const jn = JBYID[id];
    SRC[id] = { synopsis: jn.synopsis, beats: jn.beats,
      choiceText: Object.fromEntries((jn.choices || []).map(c => [c.id, { label: c.label, notes: c.effects ? c.effects.notes : undefined }])) };
  }
}
const HALF_END = ['R_xu_ending','R_lan_ending']; /* v20a268：R_vera_ending 已刪 */
function beatText(n){ return (n.beats || []).flatMap(b => b.lines || []).join(''); }
/* 新語言規則：對白 vs 旁白分開計——對白句 speaker 唔係旁白／系統；旁白句係旁白／系統 beat＋synopsis */
function dlgText(n){ return (n.beats || []).filter(b => b.speaker !== '旁白' && b.speaker !== '系統').flatMap(b => b.lines || []).join(''); }
function narText(n){ return (n.beats || []).filter(b => b.speaker === '旁白' || b.speaker === '系統').flatMap(b => b.lines || []).join('') + (n.synopsis || ''); }
function beatChars(n){ return beatText(n).length; }
const MARKERS = '嘅喺啲咗冇唔佢哋畀嚟嗰咁嘢喇嘛囉喎㗎呢';
function markerCount(s){ return [...s].filter(ch => MARKERS.includes(ch)).length; }
const WRITTEN = ['的','了','沒有','什麼','為什麼','他們','我們','不是','著'];
function writtenCount(s){ return WRITTEN.reduce((a, w) => a + s.split(w).length - 1, 0); }
/* 旁白用嘅擴充表：短旁白未必撞到九個骨幹詞，加四個書面語標記（她／如果／說／立刻）；
   只計旁白，唔影響對白句「書面語骨幹標記 = 0」嗰個骨幹表斷言 */
const WRITTEN_NAR = WRITTEN.concat(['她','如果','說','立刻']);
function writtenNarCount(s){ return WRITTEN_NAR.reduce((a, w) => a + s.split(w).length - 1, 0); }

/* (1) 表在位＋合併視圖 */
ok('覆寫表剩 5 節點（lan；v268：vera 5 條已刪；v241：hiu/choi/xu 15 條已刪入 JSON）',
  Object.keys(T).length === 5 && [...LINES.lan].every(id => !!T[id]));
ok('合併視圖 20 節點齊（表 5＋JSON 15）', ALL.every(id => !!SRC[id]));
ok('覆寫表冇鄧麗萍感情線（v20a152）', !T.R_tang_meet && !T.R_tang_ending);
ok('每節點有 beats＋synopsis', ALL.every(id => Array.isArray(SRC[id].beats) && SRC[id].beats.length >= 4 && typeof SRC[id].synopsis === 'string' && SRC[id].synopsis.length >= 10));

/* (2) 語體——新語言規則：對白留廣東話、旁白轉書面語（分開計，唔再成段一齊計） */
for(const id of ALL){
  const dlg = dlgText(SRC[id]), nar = narText(SRC[id]);
  const floor = HALF_END.includes(id) ? 10 : (LINES.hiu.includes(id) || LINES.choi.includes(id) ? 15 : 5);
  ok(id + ' 對白廣東話標記 ≥' + floor + '（實 ' + markerCount(dlg) + '）', markerCount(dlg) >= floor);
  ok(id + ' 對白書面語骨幹標記 = 0', writtenCount(dlg) === 0);
  ok(id + ' 旁白書面語骨幹標記 > 0（實 ' + writtenNarCount(nar) + '）', writtenNarCount(nar) > 0);
}
for(const id of [...LINES.hiu, ...LINES.choi]) ok(id + ' beats ≥300 字（實 ' + beatChars(SRC[id]) + '）', beatChars(SRC[id]) >= 300);
for(const id of [...LINES.xu].filter(x => !x.endsWith('ending'))) ok(id + ' beats ≥200 字（實 ' + beatChars(SRC[id]) + '）', beatChars(SRC[id]) >= 200);

/* (3) 采兒 M33 */
{
  const all = LINES.choi.map(id => beatText(SRC[id])).join('');
  ok('采兒線有追訪質地（追＋查證＋獨家＋通稿）', all.includes('追') && all.includes('查證') && all.includes('獨家') && all.includes('通稿'));
  ok('采兒線底線：唔害人飯碗', beatText(SRC.R_choi_push1).includes('飯碗') || beatText(SRC.R_choi_push1).includes('唔害人'));
  ok('采兒刊名只用《星訊週刊》（v57 術語）', all.includes('星訊週刊'));
}

/* (4) 半線收尾 */
const ENDKW = { R_xu_ending: ['錶'], R_lan_ending: ['通告牌', '食飯'] }; /* v20a268：R_vera_ending（領口）已刪 */
function bigrams(s){ const set = new Set(); const t = s.replace(/\s/g, ''); for(let i = 0; i < t.length - 1; i++) set.add(t.slice(i, i + 2)); return set; }
function jaccard(a, b){ let inter = 0; for(const x of a) if(b.has(x)) inter++; return inter / (a.size + b.size - inter); }
for(const id of HALF_END){
  ok(id + ' beats ≥450 字（實 ' + beatChars(SRC[id]) + '）', beatChars(SRC[id]) >= 450);
  ok(id + ' 專屬關鍵字在位', ENDKW[id].every(k => beatText(SRC[id]).includes(k)));
}
for(let i = 0; i < HALF_END.length; i++) for(let j = i + 1; j < HALF_END.length; j++){
  const sim = jaccard(bigrams(beatText(SRC[HALF_END[i]])), bigrams(beatText(SRC[HALF_END[j]])));
  ok('收尾互異 ' + HALF_END[i] + ' vs ' + HALF_END[j] + '（Jaccard ' + sim.toFixed(3) + ' < 0.35）', sim < 0.35);
}
for(const id of HALF_END){
  const ban = ['確定關係', '伴侶', '承諾', '一齊走下去'];
  const ct = SRC[id].choiceText || {};
  const texts = [SRC[id].synopsis, ...Object.values(ct).flatMap(t => [t.label, t.notes])];
  ok(id + ' synopsis/label/notes 冇承諾字眼', ban.every(b => texts.every(t => !String(t || '').includes(b))));
  ok(id + ' choiceText 兩條齊', ['he', 'be'].every(k => Object.keys(ct).some(cid => cid.endsWith('_' + k))));
}
/* 藍：JSON 原句保留（加厚唔改原句；v20a242：PA 表已刪，原句來源改做 content JSON） */
{
  const jsonLines = _lanxu.nodes.filter(n => n.id.startsWith('R_lan_')).flatMap(n => (n.beats || []).flatMap(b => b.lines || []));
  const lanText = LINES.lan.map(id => beatText(T[id])).join('\n');
  ok('藍 JSON 版原 lines 全數保留（' + jsonLines.length + ' 句）', jsonLines.every(l => lanText.includes(l)));
}
/* v20a152：「鄧：數字不變」段已刪——R_tang_* 唔再喺 WF2 表入面（排片數字留喺 DengLine mock／WF5 業務覆寫，見 test_tang152_static.py）。 */

/* (5) merge 行為 */
{
  const clone = o => JSON.parse(JSON.stringify(o));
  const mkNode = (id, fx) => ({ id, title: 'T', synopsis: '原版 synopsis', beats: [{ speaker: '旁白', lines: ['原版對白。'] }], choices: clone(fx.choices), flags_written: clone(fx.flags_written), openConditions: clone(fx.openConditions) });
  const rom1 = { nodes: Object.keys(fixture.packNodes).filter(id => /_(hiu|choi)_/.test(id)).map(id => mkNode(id, fixture.packNodes[id])) }; /* v20a268：vera 已刪，唔再由 fixture 拎 vera 節點 */
  const rom2 = { nodes: [
    ...Object.keys(fixture.packNodes).filter(id => id.startsWith('R_xu_')).map(id => mkNode(id, fixture.packNodes[id])),
    ...LINES.lan.map(id => clone(_lanxu.nodes.find(n => n.id === id))), /* v20a242：LAN 表已刪，lan 節點用 content JSON 真身（唔再靠 PA 表轉換） */
    /* v20a152：R_tang_meet_stub 唔再經 romTang 入嚟，改由 rom2 提供，續斷言 stub 唔被掂 */
    ...Object.keys(fixture.packNodes).filter(id => id === 'R_tang_meet_stub').map(id => mkNode(id, fixture.packNodes[id])),
  ]};
  /* v20a152：WIRE.romance 冇 tang 槽（romance_tang pack 已停載） */
  const WIRE = { romance: { veraHiuChoi: rom1, lanXu: rom2 }, main: { nodes: [] } };
  /* v20a242：LAN 覆寫表已刪，lan 節點已係 content JSON 真身，唔再經 applyRomanceLanOverrides48 轉換 */
  const run81 = new Function('ROMANCE_WF2_OVERRIDES', 'STORY_WIRE', 'WF2_APPLIED81',
    'const WF2A = WF2_APPLIED81;\n' + extractFn('applyRomanceWf2Overrides81').replace('WF2_APPLIED81', 'WF2A') + '\nreturn applyRomanceWf2Overrides81();');
  const appliedSet = new WeakSet();
  const n1 = run81(T, WIRE, appliedSet);
  ok('apply 命中 5 節點（lan；v268：vera 已刪；v241：hiu/choi/xu 已刪入 JSON，實 ' + n1 + '）', n1 === 5);
  const byId = {};
  [...rom1.nodes, ...rom2.nodes].forEach(n => byId[n.id] = n);
  let beatsOk = true, synOk = true, mechOk = true, fwOk = true;
  for(const id of Object.keys(T)){
    const node = byId[id], ov = T[id];
    const normBeats = bs => JSON.stringify((bs || []).map(b => [b.speaker, b.lines]));
    if(normBeats(node.beats) !== normBeats(ov.beats)) beatsOk = false;
    if(node.synopsis !== ov.synopsis) synOk = false;
    const fx = id.startsWith('R_lan_') ? fixture.lanPa[id] : fixture.packNodes[id];
    if(!fx || node.choices.length !== fx.choices.length) { mechOk = false; continue; }
    node.choices.forEach((c, i) => {
      const f = fx.choices[i];
      if(c.id !== f.id) mechOk = false;
      const fFx = clone(f.effects || {}), cFx = clone(c.effects || {});
      const ct = (ov.choiceText || {})[c.id];
      if(ct){ if(c.label !== ct.label) mechOk = false; if(cFx.notes !== ct.notes) mechOk = false; }
      else if(c.label !== f.label) mechOk = false;
      delete fFx.notes; delete cFx.notes;
      if(JSON.stringify(cFx) !== JSON.stringify(fFx)) mechOk = false;
      if(ct && f.effects && f.effects.notes !== undefined && c.effects.notes === f.effects.notes) mechOk = false;
    });
    if(JSON.stringify(node.flags_written) !== JSON.stringify(fx.flags_written)) fwOk = false;
    if(JSON.stringify(node.openConditions) !== JSON.stringify(fx.openConditions)) fwOk = false;
  }
  ok('merge 後 beats 同覆寫表一致', beatsOk);
  ok('merge 後 synopsis 同覆寫表一致', synOk);
  ok('choices 機制零改動（id/flags/stats 不變；半線 ending 只變 label/notes）', mechOk);
  ok('flags_written／openConditions 不變', fwOk);
  ok('hiu/choi/xu 15 節點唔再俾 apply 掂（留 fixture 原版）',
    ALL.filter(id => !T[id]).every(id => byId[id] && byId[id].synopsis === '原版 synopsis'));
  ok('R_tang_meet_stub 冇被掂', byId.R_tang_meet_stub && byId.R_tang_meet_stub.synopsis === '原版 synopsis');
  const lanBeatsRef = byId.R_lan_meet.beats;
  const n2 = run81(T, WIRE, appliedSet);
  ok('冪等：第二次 applied = 0 且 beats 參照不變', n2 === 0 && byId.R_lan_meet.beats === lanBeatsRef);
}

/* (6) commit 回歸 */
ok('COMMIT48_REL_MIN = 6', REL_MIN === 6);
ok('COMMIT48_DEFS 同 v80 逐字一致', JSON.stringify(DEFS) === JSON.stringify(fixture.commit48.defs));
ok('COMMIT48 節點在位', JSON.stringify(Object.keys(CNODES).sort()) === JSON.stringify(fixture.commit48.nodeIds.slice().sort()));
ok('互斥旗在 DEFS（hiu/choi commit 旗並存待判定層互斥）', JSON.stringify(DEFS).includes('flag_hiu_commit') && JSON.stringify(DEFS).includes('flag_choi_commit'));

/* (7) 紅線（合併視圖：表 10＋JSON 15） */
{
  const all = JSON.stringify(SRC);
  const realNames = ['周潤發','劉德華','張國榮','梅艷芳','陳百強','鄧麗君','成龍','周星馳','梁朝偉','張曼玉','王祖賢','林青霞','鍾楚紅','李連杰','洪金寶'];
  ok('覆寫表冇真人名', realNames.every(x => !all.includes(x)));
  ok('覆寫表冇關海媚名', !all.includes('關海媚'));
  const playerTxt = ALL.map(id => JSON.stringify({ s: SRC[id].synopsis, b: SRC[id].beats })).join('');
  ok('beats/synopsis 冇直寫年份數字', !/199\d|198\d/.test(playerTxt));
}

console.log(fails.length === 0 ? '\nALL PASS' : '\nFAILURES: ' + fails.join(' | '));
process.exit(fails.length === 0 ? 0 : 1);
