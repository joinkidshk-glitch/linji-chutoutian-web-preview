// qa147/sim147.js — v147 D4 地面真相重算（Node）
// 用 index.html 入面真嘅 gig 定義（eval）＋真嘅 awards62* 函數（extract＋eval），
// 重建全弧三輪 arcN 嘅 wrapHistory（30 上限窗口＋h.year＝pack 年份規則），
// 逐場計 base，驗證 day 609 實況（6 部／代表作《西環貨倉》／落選），再校準贏線。
// 用法：node qa147/sim147.js  （在 ~/workspace/linji-work147 執行）
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const SRC = fs.readFileSync('index.html', 'utf8');
const OUT = [];
function log(...a) { const s = a.join(' '); OUT.push(s); console.log(s); }

// ---------- 1. 抽 source 段（brace matching） ----------
function extractFn(name) {
  const re = new RegExp('function ' + name + '\\s*\\(');
  const m = SRC.match(re);
  if (!m) throw new Error('fn not found: ' + name);
  let i = SRC.indexOf('{', m.index);
  let d = 0, j = i;
  for (; j < SRC.length; j++) { if (SRC[j] === '{') d++; else if (SRC[j] === '}') { d--; if (!d) break; } }
  return SRC.slice(m.index, j + 1);
}
function extractConst(name) {
  const re = new RegExp('(?:const|let|var)\\s+' + name + '\\s*=');
  const m = SRC.match(re);
  if (!m) throw new Error('const not found: ' + name);
  let i = SRC.indexOf('=', m.index) + 1;
  while (SRC[i] === ' ' || SRC[i] === '\n') i++;
  const open = SRC[i];
  if (open !== '{' && open !== '[') {
    // scalar const (e.g. = 0.82;)
    let j = SRC.indexOf(';', i);
    return SRC.slice(m.index, j + 1);
  }
  const close = open === '{' ? '}' : ']';
  let d = 0, j = i, inS = null, esc = false;
  for (; j < SRC.length; j++) {
    const c = SRC[j];
    if (inS) { if (esc) esc = false; else if (c === '\\') esc = true; else if (c === inS) inS = null; continue; }
    if (c === '"' || c === "'" || c === '`') { inS = c; continue; }
    if (c === open) d++; else if (c === close) { d--; if (!d) break; }
  }
  return SRC.slice(m.index, j + 1);
}

// ---------- 2. eval gig 定義 ----------
const gigCtx = vm.createContext({ console });
function evalInGig(code) { return vm.runInContext(code, gigCtx); }
evalInGig(extractFn('gig36'));
evalInGig(extractFn('softBridgeGig'));
evalInGig(extractFn('nat92Gig'));
evalInGig(extractFn('winterBridge88Gig'));
const INLINE_ARRAYS = [
  'ENTRY_GIGS_1988', 'WINTER_ENTRY_GIGS_88', 'MID_GIGS_1988_35',
  'GIGS36_1989_SPRING_F5', 'GIGS36_1989_BRIDGE', 'GIGS36_1989_HIGH_F2', 'GIGS36_1989_MID_F3',
  'GIGS36_1990_HIGH_F2', 'GIGS36_1990_MID_F3', 'GIGS36_1990_BRIDGE', 'GIGS36_1990_AUTUMN_F6', 'GIGS36_1990_FINALE_F7',
  'NAT92_GIGS', 'SOFT_BRIDGE_GIGS_1988', 'WINTER_BRIDGE_GIGS_88', 'BR89_GIGS',
  'EXODUS_GIGS', 'RIVAL_FACEOFF_GIGS', 'FAVOR_DUE_GIGS', 'INTEL_HIDDEN_GIGS',
];
const gigById = new Map();
function addGig(g) {
  if (!g || !g.id) return;
  if (!gigById.has(g.id)) gigById.set(g.id, g);
}
for (const name of INLINE_ARRAYS) {
  try {
    const arr = evalInGig(extractConst(name) + '\n;' + name + ';');
    if (Array.isArray(arr)) arr.forEach(addGig);
    else log('WARN array not array:', name);
  } catch (e) { log('WARN inline array eval fail:', name, String(e).slice(0, 120)); }
}
// content packs
const PACK_FILES = { 1990: 'gigs_1988.json', 1991: 'gigs_1989.json', 1992: 'gigs_1990.json', 1993: 'gigs_1991.json', 1994: 'gigs_1992.json' };
for (const [gy, file] of Object.entries(PACK_FILES)) {
  const d = JSON.parse(fs.readFileSync(path.join('content', file), 'utf8'));
  const gs = d.gigs || d;
  gs.forEach(g => { if (g && g.id && !gigById.has(g.id)) gigById.set(g.id, g); });
}
log('gig map size:', gigById.size);

// variants + rename
const VARIANTS = evalInGig(extractConst('BRIDGE56_VARIANTS') + '\n;BRIDGE56_VARIANTS;');
const RENAME = evalInGig(extractConst('BRIDGE56_CROSSYEAR_RENAME') + '\n;BRIDGE56_CROSSYEAR_RENAME;');
const titleToGig = new Map(); // log title -> {gig, workTitle?}
for (const g of gigById.values()) {
  if (g.title && !titleToGig.has(g.title)) titleToGig.set(g.title, { gig: g });
}
for (const [gid, pairs] of Object.entries(VARIANTS)) {
  const g = gigById.get(gid);
  if (!g) { log('WARN variant gig missing:', gid); continue; }
  for (const [wt, t] of pairs) {
    if (!titleToGig.has(t)) titleToGig.set(t, { gig: g, workTitle: wt });
  }
}
for (const [gid, obj] of Object.entries(RENAME)) {
  const g = gigById.get(gid);
  if (g && obj && obj.title && !titleToGig.has(obj.title)) titleToGig.set(obj.title, { gig: g, workTitle: obj.workTitle || '' });
}
log('title map size:', titleToGig.size);

// ---------- 3. 全弧 wraps ----------
const EPOCH = new Date(1990, 0, 1);
function calYear(day) { const d = new Date(EPOCH.getTime() + day * 86400000); return d.getFullYear(); }
function packYear(g) {
  const y = Number(g.year);
  if (isFinite(y) && y >= 1988 && y <= 1992) return y + 2;
  if (isFinite(y)) return y;
  const m = String(g.id || '').match(/(\d{4})/);
  if (m) { const n = Number(m[1]); return (n >= 1988 && n <= 1992) ? n + 2 : n; }
  return 0;
}
function pay0(g) {
  if (g.payExact != null) return Number(g.payExact) || 0;
  if (Array.isArray(g.pay)) return Number(g.pay[0]) || 0;
  return 0;
}
const wraps = [];
const unmatched = [];
for (const ln of fs.readFileSync('/home/hatch/workspace/fullarc3/arcN/gig_log.jsonl', 'utf8').split('\n')) {
  if (!ln.trim()) continue;
  const r = JSON.parse(ln);
  if (r.kind !== 'gig_shoot_end') continue;
  const hit = titleToGig.get(r.title);
  if (!hit) { unmatched.push([r.day, r.title]); continue; }
  const g = hit.gig;
  wraps.push({
    day: r.day, gigId: g.id, title: r.title, type: g.type,
    workTitle: hit.workTitle || g.workTitle || '', roleLabel: g.roleLabel || '',
    year: packYear(g), pay: pay0(g), wrappedDay: r.day,
  });
}
wraps.sort((a, b) => a.day - b.day);
log('wraps matched:', wraps.length, 'unmatched:', unmatched.length, JSON.stringify(unmatched));

// ---------- 4. 雙軌快照 ----------
const dualByDay = [];
for (const ln of fs.readFileSync('/home/hatch/workspace/fullarc3/arcN/days.jsonl', 'utf8').split('\n')) {
  if (!ln.trim()) continue;
  const r = JSON.parse(ln);
  dualByDay.push(r);
}
dualByDay.sort((a, b) => a.day - b.day);
function dualAt(day) {
  let best = dualByDay[0];
  for (const d of dualByDay) { if (d.dayIndex <= day) best = d; else break; }
  return best;
}

// ---------- 5. 真引擎函數 ----------
const eng = vm.createContext({});
eng.S = {};
eng.GIGS = [...gigById.values()];
eng.awardsDual = () => ({ stageVolume: eng.__dual.fame, industryCredit: eng.__dual.credit });
eng.work59GigLookup = (id) => gigById.get(id) || null;
eng.ensureCastingTagsState = () => [];
vm.runInContext(extractConst('AWARDS62_ROLE_Q'), eng);
vm.runInContext(extractConst('AWARDS62_WIN_LINE'), eng);
vm.runInContext(extractConst('AWARDS62_TASTE'), eng);
vm.runInContext(extractConst('AWARDS65_LEAD_SCALES'), eng);
vm.runInContext(extractConst('START'), eng);
for (const fn of ['awardsCalendarYear', 'awardsYearFromDay', 'countYearMediumWraps', 'awards62WorkQuality', 'awards62YearOf',
  'awards62YearWorks', 'awards62RepWork', 'awards62ScoreParts', 'awards65IsLeadWork', 'work59WorkOf']) {
  vm.runInContext(extractFn(fn), eng);
}
log('engine consts: WIN_LINE =', vm.runInContext('AWARDS62_WIN_LINE', eng), 'TASTE =', vm.runInContext('AWARDS62_TASTE', eng));

// ---------- 6. 典禮定義 ----------
const schema = JSON.parse(fs.readFileSync('content/SCHEMA_AWARDS_CEREMONY_v1.json', 'utf8'));
const CER = {};
for (const c of schema.ceremonies) CER[c.id] = c;
// 全弧逐場（報告 §2）：day, ceremonyId, 實際結果
const FIELDS = [
  { day: 59, id: 'award_harbour_ad', actual: 'gallery' },
  { day: 151, id: 'award_golddisc_music', actual: 'nominated' },
  { day: 245, id: 'award_harbour_film', actual: 'nominated' },
  { day: 364, id: 'award_singho_tv', actual: 'nominated' },
  { day: 365, id: 'award_singho_tv', actual: 'gallery' },
  { day: 427, id: 'award_harbour_ad', actual: 'nominated' },
  { day: 518, id: 'award_golddisc_music', actual: 'nominated' },
  { day: 609, id: 'award_harbour_film', actual: 'nominated' },
  { day: 742, id: 'award_singho_tv', actual: 'gallery' },
];
const CATS = [{ primaryTrack: 'industryCredit' }, { primaryTrack: 'stageVolume' }];
function pwin(base, L) { return Math.min(1, Math.max(0, (base + 0.05 - L) / 0.10)); }

log('\n=== A. 全弧真實檔案（30 窗口 wrapHistory，真引擎） ===');
log('day 典禮 年份 | 計數(wrappedDay) | score桶 works | rep | topQ | baseCredit baseStage baseMAX | P(win) L=0.82 / 0.78 / 0.76');
const resultsA = [];
for (const f of FIELDS) {
  const cer = CER[f.id];
  const year = calYear(f.day);
  const win30 = wraps.filter(w => w.day <= f.day).slice(-30);
  eng.S = { wrapHistory: win30, dayIndex: f.day };
  eng.__dual = dualAt(f.day);
  const count = vm.runInContext(`countYearMediumWraps(${JSON.stringify(cer.matchTypes)}, ${year})`, eng);
  const parts = CATS.map(cat => vm.runInContext(
    `awards62ScoreParts(${JSON.stringify(cat)}, ${JSON.stringify(cer)}, ${year})`, eng));
  const rep = vm.runInContext(`awards62RepWork(${JSON.stringify(cer)}, ${year})`, eng);
  const bMax = Math.max(parts[0].base, parts[1].base);
  const best = parts[0].base >= parts[1].base ? parts[0] : parts[1];
  resultsA.push({ ...f, year, count, bMax, rep, best });
  log(`${f.day} ${cer.displayName} ${year} | 計數=${count} | 桶=${best.worksCount} rep=《${rep}》 topQ=${best.topQ.toFixed(2)} crossQ=${best.crossQ65.toFixed(2)} | ` +
    `credit=${parts[0].base.toFixed(3)} stage=${parts[1].base.toFixed(3)} MAX=${bMax.toFixed(3)} | ` +
    `P82=${(pwin(bMax, 0.82) * 100).toFixed(0)}% P78=${(pwin(bMax, 0.78) * 100).toFixed(0)}% P76=${(pwin(bMax, 0.76) * 100).toFixed(0)}% | 實際=${f.actual}`);
}

// ---------- 7. what-if：窗口 60 ----------
log('\n=== B. what-if：窗口 30 → 60（同一批 wraps） ===');
for (const f of FIELDS.filter(x => x.actual === 'nominated')) {
  const cer = CER[f.id];
  const year = calYear(f.day);
  const win60 = wraps.filter(w => w.day <= f.day).slice(-60);
  eng.S = { wrapHistory: win60, dayIndex: f.day };
  eng.__dual = dualAt(f.day);
  const parts = CATS.map(cat => vm.runInContext(
    `awards62ScoreParts(${JSON.stringify(cat)}, ${JSON.stringify(cer)}, ${year})`, eng));
  const bMax = Math.max(parts[0].base, parts[1].base);
  const best = parts[0].base >= parts[1].base ? parts[0] : parts[1];
  const rep = vm.runInContext(`awards62RepWork(${JSON.stringify(cer)}, ${year})`, eng);
  log(`${f.day} ${cer.displayName} ${year} | 桶=${best.worksCount} rep=《${rep}》 topQ=${best.topQ.toFixed(2)} | MAX=${bMax.toFixed(3)} | P82=${(pwin(bMax, 0.82) * 100).toFixed(0)}% P78=${(pwin(bMax, 0.78) * 100).toFixed(0)}%`);
}

// ---------- 8. Synthetic 強勢檔案（直接砌 wrapHistory，無窗口問題） ----------
log('\n=== C. Synthetic 前瞻檔案（真引擎，桶向量直接砌） ===');
function synWrap(qs, type, year, crossQs, crossTypes) {
  // qs / crossQs：元素係 {rs, stars}、{pay} 或數字（roleScale 值反查；stars 預設 null）
  const RQ = vm.runInContext('AWARDS62_ROLE_Q', eng);
  const inv = {};
  for (const [k, v] of Object.entries(RQ)) inv[v.toFixed(2)] = k;
  function specToH(spec, id, t) {
    if (typeof spec === 'number') {
      const rs = inv[spec.toFixed(2)];
      if (!rs) throw new Error('no roleScale for q=' + spec);
      return { gigId: id, title: '《合成》', type: t, workTitle: '合成', roleLabel: '', year, pay: 0, wrappedDay: 700, roleScale: rs };
    }
    if (spec.pay != null) {
      return { gigId: id, title: '《合成》', type: t, workTitle: '合成', roleLabel: '', year, pay: spec.pay, wrappedDay: 700, roleScale: '' };
    }
    const h = { gigId: id, title: '《合成》', type: t, workTitle: '合成', roleLabel: '', year, pay: 0, wrappedDay: 700, roleScale: spec.rs };
    if (spec.stars != null) synGigs.set(id, { id, roleScale: spec.rs, stars: spec.stars });
    return h;
  }
  const hs = [];
  qs.forEach((q, i) => hs.push(specToH(q, 'syn_' + type + '_' + i, type)));
  (crossQs || []).forEach((q, i) => hs.push(specToH(q, 'syn_x_' + i, crossTypes[i % crossTypes.length])));
  return hs;
}
const synGigs = new Map();
eng.work59GigLookup = (id) => synGigs.get(id) || gigById.get(id) || null;
const SYN = [
  { name: 'Y1 正常 (wk26 fame43/credit52)', dual: { fame: 43, credit: 52 }, year: 1990, cer: 'award_harbour_film', qs: [0.55, 0.48], cross: [0.48], crossTypes: ['電視劇'] },
  { name: 'Y1 強 (wk39 fame64/credit71)', dual: { fame: 64, credit: 71 }, year: 1990, cer: 'award_harbour_film', qs: [0.78, 0.55, 0.48], cross: [0.55, 0.48], crossTypes: ['電視劇', '廣告'] },
  { name: 'Y2 中 (wk52 fame81/credit87)', dual: { fame: 81, credit: 87 }, year: 1991, cer: 'award_harbour_film', qs: [0.78, 0.55, 0.48, 0.40], cross: [0.55, 0.48], crossTypes: ['電視劇', '廣告'] },
  { name: 'Y2 thin 全弧風格 (fame149/credit162)', dual: { fame: 149, credit: 162 }, year: 1991, cer: 'award_harbour_film', qs: [0.55, 0.48, 0.40, { pay: 2000 }], cross: [0.55, 0.48], crossTypes: ['電視劇', '廣告'] },
  { name: 'Y2 擔正 (wk65 fame118/credit124)', dual: { fame: 118, credit: 124 }, year: 1991, cer: 'award_harbour_film', qs: [1.00, 0.78, 0.55], cross: [0.78, 0.55], crossTypes: ['電視劇', '廣告'] },
  { name: 'Y3 擔正 (wk104 fame176/credit200)', dual: { fame: 176, credit: 200 }, year: 1992, cer: 'award_harbour_film', qs: [1.00, 0.78, 0.55, 0.48], cross: [0.78, 0.55], crossTypes: ['電視劇', '廣告'] },
  { name: 'Y3 E1 弧深桶 (fame181/credit210)', dual: { fame: 181, credit: 210 }, year: 1992, cer: 'award_harbour_film', qs: [1.00, 0.78, 0.78, 0.55], cross: [0.78, 0.78, 0.55], crossTypes: ['電視劇', '電視劇', '廣告'] },
  { name: 'Y3 擔正但專攻 (fame176/credit200, 無跨媒介)', dual: { fame: 176, credit: 200 }, year: 1992, cer: 'award_harbour_film', qs: [1.00, 0.78, 0.55, 0.48], cross: [], crossTypes: [] },
];
for (const s of SYN) {
  const cer = CER[s.cer];
  eng.S = { wrapHistory: synWrap(s.qs, '電影', s.year, s.cross, s.crossTypes), dayIndex: 700 };
  eng.__dual = s.dual;
  const parts = CATS.map(cat => vm.runInContext(
    `awards62ScoreParts(${JSON.stringify(cat)}, ${JSON.stringify(cer)}, ${s.year})`, eng));
  const bMax = Math.max(parts[0].base, parts[1].base);
  log(`${s.name} | credit=${parts[0].base.toFixed(3)} stage=${parts[1].base.toFixed(3)} MAX=${bMax.toFixed(3)} | ` +
    `P82=${(pwin(bMax, 0.82) * 100).toFixed(0)}% P80=${(pwin(bMax, 0.80) * 100).toFixed(0)}% P78=${(pwin(bMax, 0.78) * 100).toFixed(0)}% P76=${(pwin(bMax, 0.76) * 100).toFixed(0)}% P75=${(pwin(bMax, 0.75) * 100).toFixed(0)}%`);
}

fs.writeFileSync('qa147/sim147_out2.txt', OUT.join('\n') + '\n');
log('\n已寫 qa147/sim147_out2.txt');
