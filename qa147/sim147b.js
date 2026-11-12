// qa147/sim147b.js — v147 D4 重做校準：槓桿組合掃描（Node）
// 在 sim147.js（上一手，已核實）之上參數化三個槓桿，唔改 sim147.js／sim147_out2.txt：
//   WIN  wrapHistory 窗口（30／60／90／999＝無限）
//   DIV  worksScore 除數（1.6／1.5／1.4／1.3／1.2）
//   YEAR 計分年份口徑（pack＝現行 h.year／cal＝wrappedDay 日曆年）
// 對每個組合：A 節 9 場真實全弧檔案逐場計 base；C 節 synthetic 前瞻檔；
// 再掃贏線 L 格，計期望贏場數 E[wins]（6 場入圍）＋ P(top 0.882 檔)＋P(Y1 強)＋P(Y2 中)。
// 用法：node qa147/sim147b.js （在 ~/workspace/linji-work147 執行）
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const SRC = fs.readFileSync('index.html', 'utf8');
const OUT = [];
function log(...a) { const s = a.join(' '); OUT.push(s); console.log(s); }

// ---------- 1. 抽 source 段（同 sim147.js） ----------
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

// ---------- 2. eval gig 定義（同 sim147.js） ----------
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
function addGig(g) { if (!g || !g.id) return; if (!gigById.has(g.id)) gigById.set(g.id, g); }
for (const name of INLINE_ARRAYS) {
  try {
    const arr = evalInGig(extractConst(name) + '\n;' + name + ';');
    if (Array.isArray(arr)) arr.forEach(addGig);
    else log('WARN array not array:', name);
  } catch (e) { log('WARN inline array eval fail:', name, String(e).slice(0, 120)); }
}
const PACK_FILES = { 1990: 'gigs_1988.json', 1991: 'gigs_1989.json', 1992: 'gigs_1990.json', 1993: 'gigs_1991.json', 1994: 'gigs_1992.json' };
for (const [gy, file] of Object.entries(PACK_FILES)) {
  const d = JSON.parse(fs.readFileSync(path.join('content', file), 'utf8'));
  const gs = d.gigs || d;
  gs.forEach(g => { if (g && g.id && !gigById.has(g.id)) gigById.set(g.id, g); });
}
const VARIANTS = evalInGig(extractConst('BRIDGE56_VARIANTS') + '\n;BRIDGE56_VARIANTS;');
const RENAME = evalInGig(extractConst('BRIDGE56_CROSSYEAR_RENAME') + '\n;BRIDGE56_CROSSYEAR_RENAME;');
const titleToGig = new Map();
for (const g of gigById.values()) { if (g.title && !titleToGig.has(g.title)) titleToGig.set(g.title, { gig: g }); }
for (const [gid, pairs] of Object.entries(VARIANTS)) {
  const g = gigById.get(gid);
  if (!g) continue;
  for (const [wt, t] of pairs) { if (!titleToGig.has(t)) titleToGig.set(t, { gig: g, workTitle: wt }); }
}
for (const [gid, obj] of Object.entries(RENAME)) {
  const g = gigById.get(gid);
  if (g && obj && obj.title && !titleToGig.has(obj.title)) titleToGig.set(obj.title, { gig: g, workTitle: obj.workTitle || '' });
}

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
  wraps.push({ day: r.day, gigId: g.id, title: r.title, type: g.type, workTitle: hit.workTitle || g.workTitle || '', roleLabel: g.roleLabel || '', year: packYear(g), pay: pay0(g), wrappedDay: r.day });
}
wraps.sort((a, b) => a.day - b.day);
log('wraps matched:', wraps.length, 'unmatched:', unmatched.length);

// ---------- 3b. pack 年 vs 日曆年分歧量度 ----------
const byCalYear = {};
wraps.forEach(w => { const cy = calYear(w.day); byCalYear[cy] = (byCalYear[cy] || 0) + 1; });
log('wraps per calendar year:', JSON.stringify(byCalYear), 'total:', wraps.length);
const divergent = wraps.filter(w => w.year !== calYear(w.day));
log('packYear != calYear wraps:', divergent.length);
divergent.forEach(w => log('  DIVERGE day=' + w.day + ' calYear=' + calYear(w.day) + ' packYear=' + w.year + ' type=' + w.type + ' 《' + w.title + '》 gigId=' + w.gigId));
// 滑動 365 日最大 wraps 數（窗口要覆蓋一年份量嘅參考）
let maxWin = 0;
for (let i = 0; i < wraps.length; i++) { let n = 0; for (let j = i; j < wraps.length && wraps[j].day - wraps[i].day < 365; j++) n++; if (n > maxWin) maxWin = n; }
log('max wraps in any 365-day window:', maxWin);

// ---------- 4. 雙軌快照 ----------
const dualByDay = [];
for (const ln of fs.readFileSync('/home/hatch/workspace/fullarc3/arcN/days.jsonl', 'utf8').split('\n')) {
  if (!ln.trim()) continue;
  dualByDay.push(JSON.parse(ln));
}
dualByDay.sort((a, b) => a.day - b.day);
function dualAt(day) {
  let best = dualByDay[0];
  for (const d of dualByDay) { if (d.dayIndex <= day) best = d; else break; }
  return best;
}

// ---------- 5. 引擎：參數化 DIV／YEAR ----------
const YEAROF_CAL =
  'function awards62YearOf(h){\n' +
  '  try{ if(h && h.wrappedDay != null){ const y = awardsYearFromDay(h.wrappedDay); if(y) return y; } }catch(_e){}\n' +
  '  if(h && h.year) return Number(h.year) || 0;\n' +
  '  const m = String((h && h.gigId) || "").match(/(\\d{4})/);\n' +
  '  if(m){ const y66 = Number(m[1]); return (y66>=1988 && y66<=1992) ? y66+2 : y66; }\n' +
  '  return 0;\n' +
  '}';
function makeEngine(div, yearMode) {
  const eng = vm.createContext({});
  eng.S = {};
  eng.GIGS = [...gigById.values()];
  eng.awardsDual = () => ({ stageVolume: eng.__dual.fame, industryCredit: eng.__dual.credit });
  eng.work59GigLookup = (id) => gigById.get(id) || null;
  eng.ensureCastingTagsState = () => [];
  vm.runInContext(extractConst('AWARDS62_ROLE_Q'), eng);
  vm.runInContext(extractConst('AWARDS62_TASTE'), eng);
  vm.runInContext(extractConst('AWARDS65_LEAD_SCALES'), eng);
  vm.runInContext(extractConst('START'), eng);
  let scoreSrc = extractFn('awards62ScoreParts');
  if (Math.abs(div - 1.6) > 1e-9) {
    if (!scoreSrc.includes('wsum / 1.6')) throw new Error('divisor literal not found in awards62ScoreParts');
    scoreSrc = scoreSrc.replace('wsum / 1.6', 'wsum / ' + div);
  }
  for (const fn of ['awardsCalendarYear', 'awardsYearFromDay', 'countYearMediumWraps', 'awards62WorkQuality', 'awards62YearWorks', 'awards62RepWork', 'awards65IsLeadWork', 'work59WorkOf']) {
    vm.runInContext(extractFn(fn), eng);
  }
  if (yearMode === 'cal') vm.runInContext(YEAROF_CAL, eng);
  else vm.runInContext(extractFn('awards62YearOf'), eng);
  vm.runInContext(scoreSrc, eng);
  return eng;
}

const schema = JSON.parse(fs.readFileSync('content/SCHEMA_AWARDS_CEREMONY_v1.json', 'utf8'));
const CER = {};
for (const c of schema.ceremonies) CER[c.id] = c;
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

function sectionA(eng, win) {
  const out = [];
  for (const f of FIELDS) {
    const cer = CER[f.id];
    const year = calYear(f.day);
    const winHist = wraps.filter(w => w.day <= f.day).slice(-win);
    eng.S = { wrapHistory: winHist, dayIndex: f.day };
    eng.__dual = dualAt(f.day);
    const count = vm.runInContext(`countYearMediumWraps(${JSON.stringify(cer.matchTypes)}, ${year})`, eng);
    const parts = CATS.map(cat => vm.runInContext(
      `awards62ScoreParts(${JSON.stringify(cat)}, ${JSON.stringify(cer)}, ${year})`, eng));
    const rep = vm.runInContext(`awards62RepWork(${JSON.stringify(cer)}, ${year})`, eng);
    const bMax = Math.max(parts[0].base, parts[1].base);
    const best = parts[0].base >= parts[1].base ? parts[0] : parts[1];
    // 桶內作品明細（解釋用）
    const works = vm.runInContext(`awards62YearWorks(${JSON.stringify(cer)}, ${year})`, eng);
    out.push({ ...f, year, count, bMax, rep, best, works: works.map(w => ({ t: w.title, q: +w.q.toFixed(2), py: (w.h && w.h.year) || 0, cy: calYear(w.h.wrappedDay), day: w.h.wrappedDay })) });
  }
  return out;
}

// ---------- 6. Synthetic（wrappedDay 同目標年年中對齊，cal 口徑先啱） ----------
function synWrapFactory(eng) {
  const synGigs = new Map();
  eng.work59GigLookup = (id) => synGigs.get(id) || gigById.get(id) || null;
  const RQ = vm.runInContext('AWARDS62_ROLE_Q', eng);
  const inv = {};
  for (const [k, v] of Object.entries(RQ)) inv[v.toFixed(2)] = k;
  const MIDDAY = { 1990: 182, 1991: 547, 1992: 912 };
  function specToH(spec, id, t, year) {
    if (typeof spec === 'number') {
      const rs = inv[spec.toFixed(2)];
      if (!rs) throw new Error('no roleScale for q=' + spec);
      return { gigId: id, title: '《合成》', type: t, workTitle: '合成', roleLabel: '', year, pay: 0, wrappedDay: MIDDAY[year], roleScale: rs };
    }
    if (spec.pay != null) {
      return { gigId: id, title: '《合成》', type: t, workTitle: '合成', roleLabel: '', year, pay: spec.pay, wrappedDay: MIDDAY[year], roleScale: '' };
    }
    const h = { gigId: id, title: '《合成》', type: t, workTitle: '合成', roleLabel: '', year, pay: 0, wrappedDay: MIDDAY[year], roleScale: spec.rs };
    if (spec.stars != null) synGigs.set(id, { id, roleScale: spec.rs, stars: spec.stars });
    return h;
  }
  function synWrap(qs, type, year, crossQs, crossTypes) {
    const hs = [];
    qs.forEach((q, i) => hs.push(specToH(q, 'syn_' + type + '_' + i, type, year)));
    (crossQs || []).forEach((q, i) => hs.push(specToH(q, 'syn_x_' + i, crossTypes[i % crossTypes.length], year)));
    return hs;
  }
  return synWrap;
}
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
function sectionC(eng) {
  const synWrap = synWrapFactory(eng);
  const out = {};
  for (const s of SYN) {
    const cer = CER[s.cer];
    eng.S = { wrapHistory: synWrap(s.qs, '電影', s.year, s.cross, s.crossTypes), dayIndex: 700 };
    eng.__dual = s.dual;
    const parts = CATS.map(cat => vm.runInContext(
      `awards62ScoreParts(${JSON.stringify(cat)}, ${JSON.stringify(cer)}, ${s.year})`, eng));
    out[s.name] = Math.max(parts[0].base, parts[1].base);
  }
  return out;
}

// ---------- 7. 掃描 ----------
const LINES = [0.82, 0.84, 0.85, 0.86, 0.87, 0.875, 0.88, 0.885, 0.89, 0.90];
const WINS = [30, 60, 90, 999];
const DIVS = [1.6, 1.5, 1.4, 1.3, 1.2];
const YEARS = ['pack', 'cal'];
const NOM = ['Y1 強 (wk39 fame64/credit71)', 'Y2 中 (wk52 fame81/credit87)', 'Y2 thin 全弧風格 (fame149/credit162)', 'Y2 擔正 (wk65 fame118/credit124)', 'Y3 擔正 (wk104 fame176/credit200)', 'Y3 擔正但專攻 (fame176/credit200, 無跨媒介)'];
const TOPKEY = 'Y2 擔正 (wk65 fame118/credit124)';
const Y1KEY = 'Y1 強 (wk39 fame64/credit71)';
const Y2MIDKEY = 'Y2 中 (wk52 fame81/credit87)';

log('\n=== 掃描總表：每組合 × 每條線：E[wins]（9 場中 6 入圍）| P(top 0.882 級) | P(Y1 強) | P(Y2 中) ===');
log('PASS 條件：0.5 ≤ E ≤ 1.5 且 P(top) ≤ 0.60 且 P(Y1強) ≤ 0.30');
const passCombos = [];
for (const yearMode of YEARS) {
  for (const div of DIVS) {
    for (const win of WINS) {
      const eng = makeEngine(div, yearMode);
      const A = sectionA(eng, win);
      const C = sectionC(eng);
      const nomBases = A.filter(f => f.actual === 'nominated').map(f => f.bMax);
      const baseStr = nomBases.map(b => b.toFixed(3)).join(',');
      log(`\n--- YEAR=${yearMode} DIV=${div} WIN=${win} | 入圍 6 場 base=[${baseStr}] | SYN top=${C[TOPKEY].toFixed(3)} Y1強=${C[Y1KEY].toFixed(3)} Y2中=${C[Y2MIDKEY].toFixed(3)}`);
      for (const L of LINES) {
        const E = nomBases.reduce((s, b) => s + pwin(b, L), 0);
        const pTop = pwin(C[TOPKEY], L), pY1 = pwin(C[Y1KEY], L), pY2m = pwin(C[Y2MIDKEY], L);
        const ok = E >= 0.5 && E <= 1.5 && pTop <= 0.60 && pY1 <= 0.30;
        if (ok) passCombos.push({ yearMode, div, win, L, E: +E.toFixed(2), pTop: +pTop.toFixed(2), pY1: +pY1.toFixed(2), pY2m: +pY2m.toFixed(2) });
        log(`  L=${L.toFixed(3)} E=${E.toFixed(2)} P(top)=${(pTop * 100).toFixed(0)}% P(Y1強)=${(pY1 * 100).toFixed(0)}% P(Y2中)=${(pY2m * 100).toFixed(0)}% ${ok ? '★ PASS' : ''}`);
      }
    }
  }
}
log('\n=== 通過驗收嘅組合（全部） ===');
if (!passCombos.length) log('(none)');
passCombos.forEach(c => log(JSON.stringify(c)));

// ---------- 8. 候選組合桶明細（解釋邊個樽頸郁咗） ----------
log('\n=== 桶明細：WIN=30 vs 60（DIV=1.6，pack vs cal）— 只列入圍 6 場 ===');
for (const yearMode of ['pack', 'cal']) {
  for (const win of [30, 60]) {
    const eng = makeEngine(1.6, yearMode);
    const A = sectionA(eng, win);
    log(`\n--- YEAR=${yearMode} WIN=${win}`);
    for (const f of A.filter(x => x.actual === 'nominated')) {
      const ws = f.works.map(w => `《${w.t}》q${w.q.toFixed(2)}(pack${w.py}/cal${w.cy}/d${w.day})`).join('；');
      log(`day ${f.day} ${f.year} 計數=${f.count} 桶=${f.works.length} base=${f.bMax.toFixed(3)} rep=《${f.rep}》 topQ=${f.best.topQ.toFixed(2)} crossQ=${f.best.crossQ65.toFixed(2)} worksScore=${f.best.worksScore.toFixed(3)} | ${ws}`);
    }
  }
}
// DIV 對照：DIV=1.4／1.2 下同一批 base（WIN=60，cal）
log('\n=== DIV 對照（WIN=60，YEAR=cal）：入圍 base＋SYN base ===');
for (const div of [1.6, 1.5, 1.4, 1.3, 1.2]) {
  const eng = makeEngine(div, 'cal');
  const A = sectionA(eng, 60);
  const C = sectionC(eng);
  const nomBases = A.filter(f => f.actual === 'nominated').map(f => f.bMax.toFixed(3)).join(',');
  log(`DIV=${div} 入圍 base=[${nomBases}] | SYN: ` + NOM.map(k => k.slice(0, 6) + '=' + C[k].toFixed(3)).join(' '));
}

try { fs.writeFileSync('qa147/sim147b_out.txt', OUT.join('\n') + '\n'); log('\n已寫 qa147/sim147b_out.txt'); }
catch (e) { log('\n寫檔失敗（環境攔截？）: ' + String(e).slice(0, 120) + ' —— stdout 已有全部數字'); }
