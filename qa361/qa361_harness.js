// v361 P1 函數級驗證（抽取 harness，跟 qa147/sim147.js／qa360 同一模式）
// A：頒獎天花板逐媒介逐年（真引擎 awards62ScoreParts）
// B：結局矩陣（真函數 resolveEnding410＋F2 floor 覆寫）
// C：合約信用來源（contractCredit361OnWrap，v361 新增；舊 code 無此函數時跳過）
// D：負標籤預警（applyCastingTags＋toast stub；v361 後驗證）
// 用法：node qa361/qa361_harness.js（喺 repo root 執行）
const fs = require('fs');
const vm = require('vm');

const SRC = fs.readFileSync('index.html', 'utf8');
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS', name, detail || ''); }
  else { fail++; console.log('FAIL', name, detail || ''); }
}
function extractFn(name) {
  const re = new RegExp('function ' + name + '\\s*\\(');
  const m = SRC.match(re);
  if (!m) throw new Error('fn not found: ' + name);
  let i = SRC.indexOf('{', m.index);
  let d = 0, j = i, inS = null, esc = false;
  for (; j < SRC.length; j++) {
    const c = SRC[j];
    if (inS) { if (esc) esc = false; else if (c === '\\') esc = true; else if (c === inS) inS = null; continue; }
    if (c === '"' || c === "'" || c === '`') { inS = c; continue; }
    if (c === '{') d++; else if (c === '}') { d--; if (!d) break; }
  }
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
function hasFn(name) { return new RegExp('function ' + name + '\\s*\\(').test(SRC); }

// ================= A：頒獎天花板 =================
{
  const pack = JSON.parse(fs.readFileSync('content/gigs_new.json', 'utf8'));
  const gigs = pack.gigs;
  const gigById = new Map(gigs.map(g => [g.id, g]));
  const eng = vm.createContext({});
  eng.S = {};
  eng.GIGS = gigs;
  eng.__dual = { fame: 100, credit: 100 };
  eng.awardsDual = () => ({ stageVolume: eng.__dual.fame, industryCredit: eng.__dual.credit });
  eng.work59GigLookup = (id) => gigById.get(id) || null;
  eng.ensureCastingTagsState = () => [];
  const run = (code) => vm.runInContext(code, eng);
  run(extractConst('AWARDS62_ROLE_Q'));
  run(extractConst('AWARDS62_WIN_LINE'));
  run(extractConst('AWARDS62_TASTE'));
  run(extractConst('AWARDS65_LEAD_SCALES'));
  run(extractConst('START'));
  for (const fn of ['awardsCalendarYear', 'awardsYearFromDay', 'countYearMediumWraps', 'awards62WorkQuality',
    'awards62YearOf', 'awards62YearWorks', 'awards62RepWork', 'awards62ScoreParts', 'awards65IsLeadWork', 'work59WorkOf']) {
    run(extractFn(fn));
  }
  const WIN = run('AWARDS62_WIN_LINE');
  const qOf = (g) => run(`awards62WorkQuality({gigId:${JSON.stringify(g.id)}, roleScale:${JSON.stringify(g.roleScale)}, pay:${(Array.isArray(g.pay) ? g.pay[1] : 0) || 0}})`);
  const pwin = (base) => Math.min(1, Math.max(0, (base + 0.05 - WIN) / 0.10));
  const MIDDAY = { 1990: 180, 1991: 545, 1992: 910 };
  const wrapOf = (g, year) => ({
    gigId: g.id, title: g.title, type: g.type, workTitle: g.workTitle || '', roleLabel: g.roleLabel || '',
    year: g.year, pay: Array.isArray(g.pay) ? g.pay[1] : 0, wrappedDay: MIDDAY[year], roleScale: g.roleScale, totalDays: g.days || 2,
  });
  const MEDIUMS = [
    { name: '電影', types: ['電影'], crossType: '電視劇' },
    { name: '電視劇', types: ['電視劇'], crossType: '電影' },
    { name: '廣告', types: ['廣告'], crossType: '電影' },
    { name: '綜藝(司儀)', types: ['綜藝'], crossType: '電影' },
    { name: '唱片', types: ['唱片通告'], crossType: '電影' },
  ];
  console.log('\n=== A. 頒獎天花板（真引擎；WIN_LINE=' + WIN + '）===');
  console.log('媒介 年 | full-kit base(P) | pure base(P) | strong base(P) | 桶內最佳 q 組合');
  for (const med of MEDIUMS) {
    for (const year of [1990, 1991, 1992]) {
      const pool = gigs.filter(g => g.year === year && med.types.includes(g.type))
        .map(g => ({ g, q: qOf(g) })).sort((a, b) => b.q - a.q);
      const crossPool = gigs.filter(g => g.year === year && g.type === med.crossType)
        .map(g => ({ g, q: qOf(g) })).sort((a, b) => b.q - a.q);
      const cer = { matchTypes: med.types };
      const catS = { primaryTrack: 'stageVolume' };
      const catC = { primaryTrack: 'industryCredit' };
      const score = (wraps, fame, credit) => {
        eng.S = { wrapHistory: wraps, dayIndex: MIDDAY[year] };
        eng.__dual = { fame, credit };
        const p1 = run(`awards62ScoreParts(${JSON.stringify(catS)}, ${JSON.stringify(cer)}, ${year})`);
        const p2 = run(`awards62ScoreParts(${JSON.stringify(catC)}, ${JSON.stringify(cer)}, ${year})`);
        return Math.max(p1.base, p2.base);
      };
      const best4 = pool.slice(0, 4).map(x => wrapOf(x.g, year));
      const cross2 = crossPool.slice(0, 2).map(x => wrapOf(x.g, year));
      const crossMid = crossPool.filter(x => x.q >= 0.5 && x.q < 1).slice(0, 2).map(x => wrapOf(x.g, year));
      const full = score([...best4, ...cross2], 100, 100);
      const pure = score(best4, 100, 100);
      const strong = score([...pool.slice(0, 3).map(x => wrapOf(x.g, year)), ...crossMid], 45, 60);
      console.log(`${med.name} ${year} | ${full.toFixed(4)}(${(pwin(full) * 100).toFixed(0)}%) | ${pure.toFixed(4)}(${(pwin(pure) * 100).toFixed(0)}%) | ${strong.toFixed(4)}(${(pwin(strong) * 100).toFixed(0)}%) | q=[${pool.slice(0, 4).map(x => x.q.toFixed(2)).join(',')}] crossQ=${crossPool.length ? crossPool[0].q.toFixed(2) : '-'}`);
    }
  }
}

// ================= B：結局矩陣 =================
{
  const eng = vm.createContext({});
  eng.GIGS = [];
  const run = (code) => vm.runInContext(code, eng);
  for (const c of ['ENDING410_T', 'ENDING95_T', 'ENDING_NEG_TAGS410', 'ENDING410_BACKSTAGE_KEYS',
    'ENDING410_EXODUS_NAME_FALLBACK', 'ENDING410_CAREER_NAMES', 'END95_TYPE_MEDIUM', 'END95_LEAD_SCALES',
    'END95_STRONG_LEAD', 'END95_GENRE_TYPE_NAMES', 'END95_COMEDY_G', 'END95_ACTION_G', 'END95_COMEDY_KW',
    'END95_ACTION_KW', 'END229_LEAD_MEDIUM', 'SPINE95_REQUIRED', 'CONSEQ61_REVIEWS']) {
    run(extractConst(c));
  }
  for (const fn of ['dualTrackNumbers', 'readDualTracks', 'endingDual410', 'endingFlag410', 'endingNegTagCount410',
    'endingBackstageTagCount410', 'favorCreditCountsAsHeld', 'endingFavor410', 'endingRomance410', 'endingE3Eligible410',
    'press94ScaleOf', 'end95IsLead', 'end95GenreOf', 'end95ClassifyWrap', 'end95EmptyStats', 'end95StatsAddOne',
    'end95DeriveStats', 'careerStats95Of', 'end229IsLead', 'end229ClassifyLead', 'end229EmptyLeadStats',
    'end229DeriveLeadStats', 'leadStats229Of', 'end95Awards', 'end95EverHeldCredit', 'end95StoryDone',
    'end95ChainsDone', 'end95SpineDone', 'end95PangProgress', 'end95E3Variant', 'end95BuildGaps', 'resolveEnding410']) {
    run(extractFn(fn));
  }
  const FLOOR92 = run('CONSEQ61_REVIEWS[1992].floor');
  const hasExemptHelper = hasFn('ending361FloorExempt');
  if (hasExemptHelper) run(extractFn('ending361FloorExempt'));
  // F2 覆寫複刻：dual<floor → E7（E6 除外；v361 後經 ending361FloorExempt 豁免明確路線）
  const applyF2 = (res) => {
    const dual = res.snapshot.dual;
    let exempt = res.career === 'E6';
    if (hasExemptHelper) exempt = run(`ending361FloorExempt(${JSON.stringify(res.career)})`);
    if (!exempt && dual < FLOOR92) return 'E7';
    return res.career;
  };
  const SPINE = ['N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'N9', 'N10', 'N11', 'N12', 'N13', 'N14', 'N15', 'N16', 'N17'];
  function mkS(o) {
    const done = {};
    (o.spine ? SPINE : (o.done || [])).forEach(id => done[id] = true);
    const held = [];
    for (let i = 0; i < (o.held || 0); i++) held.push({ id: 'credit_test_' + i, status: '有效' });
    return {
      fame: o.fame || 0, stage: o.stage || 0, acting: o.acting || 0, stress: o.stress || 0,
      industryCreditDelta: o.delta || 0,
      castingTags: (o.tags || []).map(t => ({ id: t, label: t })),
      npcs: { agent: o.agentRel || 0, director: o.directorRel || 0 },
      story: { done, rel: {}, flags: o.sflags || {} },
      flags: o.flags || {},
      favorLedger: { settled: o.settled || 0, credits: (o.settled || 0) + (o.held || 0), exodus: [] },
      mockCredits: held, mockDebts: [],
      awardsLog: o.win ? [{ medium: o.winMedium || 'film', categories: [{ outcome: 'won' }] }] : (o.musicNom ? [{ medium: 'music', categories: [{ outcome: 'nominated' }] }] : []),
      careerStats95: o.stats || { total: 0, byMedium: { film: 0, tv: 0, music: 0, variety: 0, ad: 0 }, leadByMedium: { film: 0, tv: 0, music: 0, variety: 0, ad: 0 }, tvLongLeads: 0, genreIdentified: 0, genreComedy: 0, genreAction: 0, backstageWorks: 0 },
      leadStats229: { byMedium: Object.assign({ film: 0, tv: 0, music: 0, variety: 0, ad: 0 }, o.leads || {}) },
      stars: o.pangFav ? { pang_siuki: { fav: o.pangFav } } : {},
      trainCount: { train_stamina: o.staminaLessons || 0 },
      wrapHistory: [],
    };
  }
  const stats = (byMedium, extra) => Object.assign({ total: Object.values(byMedium).reduce((a, b) => a + b, 0), byMedium: Object.assign({ film: 0, tv: 0, music: 0, variety: 0, ad: 0 }, byMedium), leadByMedium: { film: 0, tv: 0, music: 0, variety: 0, ad: 0 }, tvLongLeads: 0, genreIdentified: 0, genreComedy: 0, genreAction: 0, backstageWorks: 0 }, extra || {});
  const CASES = [
    // [name, seed, opts, expectAfterF2]
    ['e1_full', { fame: 190, stage: 130, acting: 130, win: 1, spine: 1, leads: { film: 2, tv: 1 } }, {}, 'E1'],
    ['e1_neg2_cliff', { fame: 190, stage: 130, acting: 130, win: 1, spine: 1, leads: { film: 2, tv: 1 }, tags: ['八卦', '高冷'] }, {}, 'E2'],
    ['ss_nowin', { fame: 170, stage: 130, acting: 130, spine: 1, leads: { film: 2, tv: 1 } }, {}, 'SS'],
    ['fk', { fame: 120, stage: 100, acting: 100, stats: stats({ film: 12, tv: 4, ad: 4 }), leads: { film: 2 } }, {}, 'FK'],
    ['tk', { fame: 120, stage: 100, acting: 100, stats: stats({ tv: 12, film: 4, ad: 4 }), leads: { tv: 1 } }, {}, 'TK'],
    ['sk', { fame: 120, stage: 100, acting: 100, stats: stats({ music: 12, film: 4, ad: 4 }), musicNom: 1 }, {}, 'SK'],
    ['gh', { fame: 100, stage: 90, acting: 90, stats: stats({ variety: 12, film: 4, ad: 4 }), pangFav: 50 }, {}, 'GH'],
    ['ck', { fame: 100, stage: 90, acting: 90, stats: stats({ film: 10 }, { genreIdentified: 10, genreComedy: 6 }) }, {}, 'CK'],
    ['ak', { fame: 100, stage: 90, acting: 90, stats: stats({ film: 10 }, { genreIdentified: 10, genreAction: 6 }), staminaLessons: 5 }, {}, 'AK'],
    ['id', { fame: 110, stage: 20, acting: 20, stress: 100, delta: -14 }, {}, 'ID'],
    ['cr', { fame: 45, stage: 130, acting: 130, delta: 12 }, {}, 'CR'],
    ['e2_mid', { fame: 80, stage: 80, acting: 80 }, {}, 'E2'],
    ['e3_natural', { fame: 50, stage: 110, acting: 110, delta: 20, directorRel: 70 }, {}, 'E3'],
    ['e3_lowfame', { fame: 30, stage: 130, acting: 130, delta: 36, directorRel: 70 }, {}, 'E3'],
    ['e3_boss', { fame: 40, stage: 120, acting: 120, delta: 30, directorRel: 70, settled: 3, held: 3 }, {}, 'E3'],
    ['e3_tv_variant', { fame: 40, stage: 120, acting: 120, delta: 30, directorRel: 70, stats: stats({ tv: 8, film: 2 }) }, {}, 'E3'],
    ['e3_tags', { fame: 35, stage: 120, acting: 120, delta: 30, tags: ['場記', '副導'] }, {}, 'E3'],
    ['e5_natural', { fame: 55, stage: 90, acting: 90, delta: 18, settled: 4, held: 4, agentRel: 70 }, {}, 'E5'],
    ['e4_natural', { fame: 54, stage: 14, acting: 18, stress: 100 }, {}, 'E4'],
    ['e4_rescued', { fame: 54, stage: 14, acting: 18, stress: 100, held: 2 }, {}, 'E4'],
    ['e0_natural', { fame: 30, stage: 130, acting: 130, delta: 36, directorRel: 10, agentRel: 10 }, {}, 'E0'],
    ['e7_low', { fame: 40, stage: 40, acting: 40 }, {}, 'E7'],
    ['e6_quit', { fame: 80, stage: 80, acting: 80 }, { quit: 'job' }, 'E6'],
    ['floor_below', { fame: 70, stage: 60, acting: 60 }, {}, 'E7'],
    ['floor_above', { fame: 75, stage: 65, acting: 65 }, {}, 'E2'],
  ];
  console.log('\n=== B. 結局矩陣（1992 floor=' + FLOOR92 + '，exemptHelper=' + hasExemptHelper + '）===');
  for (const [name, seed, opts, expect] of CASES) {
    const S = mkS(seed);
    const res = run(`resolveEnding410(${JSON.stringify(S)}, ${JSON.stringify(opts)})`);
    const final = applyF2(res);
    const ok = final === expect;
    check('B:' + name, ok, `career=${res.career}${res.careerVariant ? '/' + res.careerVariant : ''} final=${final} expect=${expect} dual=${res.snapshot.dual} fame=${res.snapshot.fame} credit=${res.snapshot.credit} neg=${res.snapshot.negTags} gaps=${JSON.stringify(res.gaps95)}`);
  }
}

// ================= C：合約信用來源（v361 新增） =================
if (hasFn('contractCredit361OnWrap')) {
  const eng = vm.createContext({});
  const run = (code) => vm.runInContext(code, eng);
  run(extractConst('CONTRACT_CREDIT361_CFG'));
  run(extractFn('contractCredit361QuarterOf'));
  run(extractFn('contractCredit361OnWrap'));
  console.log('\n=== C. 合約信用來源 ===');
  // 模擬三年：每季 6 張通告（2 張高級），驗季上限 +4、生涯 +36
  const S = { industryCreditDelta: 0, contractCredit361: null };
  let totalGain = 0;
  for (let q = 0; q < 12; q++) {
    for (let i = 0; i < 6; i++) {
      const gig = { tier: i < 2 ? '高級' : '初級' };
      const day = q * 91 + i * 10;
      totalGain += run(`contractCredit361OnWrap(${JSON.stringify(S)}, ${JSON.stringify(gig)}, ${day})`);
      // 同步 S 狀態（函數寫入 Sref 物件，JSON 傳入係副本，要讀返）
      const st = run(`contractCredit361OnWrap.__lastState || null`);
      void st;
    }
    break; // 佔位，下方用直接引用重跑
  }
  // 直接引用版（函數改 Sref，唔經 JSON）
  const S2 = { industryCreditDelta: 0 };
  eng.__S2 = S2;
  let g2 = 0;
  for (let q = 0; q < 12; q++) {
    let qGain = 0;
    for (let i = 0; i < 6; i++) {
      eng.__gig = { tier: i < 2 ? '高級' : '初級' };
      const got = run(`contractCredit361OnWrap(__S2, __gig, ${q * 91 + i * 10})`);
      qGain += got; g2 += got;
    }
    if (q < 3) check('C:quarter' + q + '_cap4', qGain === 4, 'qGain=' + qGain);
  }
  check('C:lifetime_cap36', g2 === 36, 'total=' + g2);
  check('C:delta_written', S2.industryCreditDelta === 36, 'delta=' + S2.industryCreditDelta);
  // 高級額外 +1：單季第一張高級應 +2
  const S3 = { industryCreditDelta: 0 };
  eng.__S3 = S3; eng.__gig = { tier: '稀有' };
  const first = run('contractCredit361OnWrap(__S3, __gig, 0)');
  check('C:high_tier_bonus', first === 2, 'first=' + first);
  eng.__gig = { tier: '初級' };
  const second = run('contractCredit361OnWrap(__S3, __gig, 5)');
  check('C:normal_plus1', second === 1, 'second=' + second);
} else {
  console.log('\n=== C. 合約信用來源：函數未存在（改版前基線，跳過）===');
}

// ================= D：負標籤預警（v361） =================
if (hasFn('negTagWarn361')) {
  const eng = vm.createContext({});
  const toasts = [];
  eng.toast = (t) => toasts.push(String(t));
  eng.S = { castingTags: [], fame: 0, industryCreditDelta: 0 };
  eng.ensureWeakSeals = () => {};
  eng.calib60FameGain = (x) => x;
  eng.syncDualTracks = () => {};
  eng.FREEPLAY_FW = { castingTagsReg: null };
  const run = (code) => vm.runInContext(code, eng);
  run(extractConst('ENDING_NEG_TAGS410'));
  run(extractFn('endingFlag410'));
  run(extractFn('endingNegTagCount410'));
  run(extractFn('ensureCastingTagsState'));
  run(extractFn('castingTagRegistry'));
  run(extractFn('castingTagLabelToId'));
  run(extractFn('castingTagMeta'));
  run(extractFn('negTagWarn361'));
  run(extractFn('applyCastingTags'));
  console.log('\n=== D. 負標籤預警 ===');
  run(`applyCastingTags(['八卦'], {from:'story:N8', applyDual:false})`);
  check('D:first_neg_warn', toasts.length === 1, JSON.stringify(toasts));
  run(`applyCastingTags(['喜劇細胞'], {from:'gig:x', applyDual:false})`);
  check('D:non_neg_no_warn', toasts.length === 1, JSON.stringify(toasts));
  run(`applyCastingTags(['高冷'], {from:'story:N14', applyDual:false})`);
  check('D:second_neg_warn', toasts.length === 2, JSON.stringify(toasts));
  run(`applyCastingTags(['八卦'], {from:'story:N8', applyDual:false})`);
  check('D:dupe_no_warn', toasts.length === 2, JSON.stringify(toasts));
} else {
  console.log('\n=== D. 負標籤預警：函數未存在（改版前基線，跳過）===');
}

console.log(`\nTOTAL PASS ${pass} FAIL ${fail}`);
process.exit(fail ? 1 : 0);
