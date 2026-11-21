// v360 P0 函數級驗證（抽取 harness，跟 qa147/sim147.js 同一模式）
// ① aud91PresentDue 自癒 ② genre 標籤授予＋回填 ③ defaultWeekPlan 輪替
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

// ================= ① aud91PresentDue 自癒 =================
{
  const maskClasses = new Set();
  const ctx = vm.createContext({
    console,
    document: { getElementById: (id) => id === 'mask' ? { classList: { contains: (c) => maskClasses.has(c) } } : null },
    toast: () => {},
    ending78Locked: () => false,
    S: null,
  });
  const run = (code) => vm.runInContext(code, ctx);
  run(extractConst('_aud91Presenting'));
  run(extractFn('aud91Ensure'));
  run(extractFn('aud91DueList'));
  run(extractFn('aud91PresentDue'));
  // stub PresentOne: 正常＝剔單＋next；throwMode＝拋錯
  run(`
    let __throwMode = false; let __presented = [];
    function aud91PresentOne(rec, next){
      if(__throwMode){ __throwMode = false; throw new Error('boom360'); }
      S.pendingAud = aud91Ensure().filter(p=>p!==rec);
      __presented.push(rec.gigId);
      if(typeof next==='function') next();
    }
    function __mkRec(id, reveal){ return { gigId:id, revealDay:reveal, audDay:reveal-3, ok:false }; }
  `);
  // case A: strand（旗真＋mask 關）→ 自癒呈現
  run(`S = { dayIndex: 50, pendingAud: [__mkRec('g1', 45), __mkRec('g2', 46)] }; _aud91Presenting = true; __presented = [];`);
  maskClasses.clear();
  let ret = run(`aud91PresentDue(null)`);
  check('① strand 自癒呈現', ret === true && run(`__presented.length`) === 2 && run(`_aud91Presenting`) === false && run(`S.pendingAud.length`) === 0,
    `ret=${ret} presented=${run('__presented.length')}`);
  // case B: 旗真＋mask 開 → 回 false 唔搶
  run(`S.pendingAud = [__mkRec('g3', 47)]; _aud91Presenting = true; __presented = [];`);
  maskClasses.add('on');
  ret = run(`aud91PresentDue(null)`);
  check('① modal 開緊唔搶呈現', ret === false && run(`__presented.length`) === 0 && run(`S.pendingAud.length`) === 1);
  // case C: mask 閂後補呈現
  maskClasses.clear();
  ret = run(`aud91PresentDue(null)`);
  check('① modal 閂後補呈現', ret === true && run(`__presented.length`) === 1 && run(`_aud91Presenting`) === false);
  // case D: PresentOne 拋錯 → 壞單剔走、好單照呈現、旗清
  run(`S.pendingAud = [__mkRec('bad', 40), __mkRec('good', 41)]; __presented = []; __throwMode = true;`);
  ret = run(`aud91PresentDue(null)`);
  check('① 拋錯唔 strand', ret === true && run(`__presented[0]`) === 'good' && run(`S.pendingAud.length`) === 0 && run(`_aud91Presenting`) === false,
    `presented=${run('__presented.join(",")')}`);
  // case E: 正常路徑（旗假）照舊
  run(`S.pendingAud = [__mkRec('g4', 49)]; __presented = [];`);
  ret = run(`aud91PresentDue(null)`);
  check('① 正常路徑不變', ret === true && run(`__presented.length`) === 1);
  // case F: 未到期唔呈現
  run(`S.pendingAud = [__mkRec('g5', 99)]; __presented = [];`);
  ret = run(`aud91PresentDue(null)`);
  check('① 未到期唔呈現', ret === false && run(`S.pendingAud.length`) === 1);
  // case G: continueFn 只行一次
  run(`S.pendingAud = [__mkRec('g6', 48)]; __presented = []; let __cont = 0; aud91PresentDue(()=>{ __cont++; });`);
  check('① continueFn 只行一次', run(`__cont`) === 1, `cont=${run('__cont')}`);
}

// ================= ② genre 標籤授予＋回填 =================
{
  const gigs = JSON.parse(fs.readFileSync('content/gigs_new.json', 'utf8')).gigs;
  const reg = JSON.parse(fs.readFileSync('content/STUB_CASTING_TAGS_v1.json', 'utf8'));
  const byId = {};
  gigs.forEach(g => { byId[g.id] = g; });
  const ctx = vm.createContext({
    console,
    FREEPLAY_FW: { castingTagsReg: reg },
    work59GigLookup: (id) => byId[id] || null,
    syncDualTracks: () => {},
    calib60FameGain: (v) => v,
    ensureWeakSeals: () => {},
    S: null,
    GIGS: gigs,
  });
  const run = (code) => vm.runInContext(code, ctx);
  run(extractConst('GIG_GENRE_TAG360'));
  run(extractConst('GENRE_TAG_LABEL360'));
  run(extractFn('gigGenreTag360'));
  run(extractFn('castingTagGenreBackfill360'));
  run(extractFn('ensureCastingTagsState'));
  run(extractFn('castingTagRegistry'));
  run(extractFn('castingTagLabelToId'));
  run(extractFn('castingTagMeta'));
  run(extractFn('applyCastingTags'));
  run(extractFn('applyGigTagOnComplete'));

  const comedy = gigs.find(g => g.genre === '喜劇' && g.category === '作品');
  const action = gigs.find(g => g.genre === '動作');
  const wuxia = gigs.find(g => g.genre === '武俠');
  const wenyi = gigs.find(g => g.genre === '文藝');
  const stuntHorror = gigs.find(g => g.roleLabel === '動作替身' && g.genre === '靈異驚慄');

  run(`S = { castingTags: [], fame: 0, industryCreditDelta: 0 };`);
  let added = run(`applyGigTagOnComplete(${JSON.stringify(comedy.id)}).map(t=>t.id)`);
  check('② 喜劇授予 tag_comedy', JSON.stringify(added) === '["tag_comedy"]', JSON.stringify(added));
  added = run(`applyGigTagOnComplete(${JSON.stringify(action.id)}).map(t=>t.id)`);
  check('② 動作授予 tag_action', JSON.stringify(added) === '["tag_action"]', JSON.stringify(added));
  added = run(`applyGigTagOnComplete(${JSON.stringify(wenyi.id)}).map(t=>t.id)`);
  check('② 文藝唔授予', added.length === 0);
  added = run(`applyGigTagOnComplete(${JSON.stringify(comedy.id)}).length`);
  check('② 重複授予 dedupe', added === 0);
  const labels = run(`S.castingTags.map(t=>t.id+':'+t.label).join('|')`);
  check('② label 跟 registry', labels.includes('tag_comedy:喜劇細胞') && labels.includes('tag_action:動作好手'), labels);
  if (stuntHorror) {
    run(`S.castingTags = S.castingTags.filter(t=>t.id!=='tag_action');`);
    added = run(`applyGigTagOnComplete(${JSON.stringify(stuntHorror.id)}).map(t=>t.id)`);
    check('② 動作替身（靈異）授予 tag_action', JSON.stringify(added) === '["tag_action"]', JSON.stringify(added));
  }
  // 武俠
  run(`S.castingTags = [];`);
  added = run(`applyGigTagOnComplete(${JSON.stringify(wuxia.id)}).map(t=>t.id)`);
  check('② 武俠授予 tag_action', JSON.stringify(added) === '["tag_action"]', JSON.stringify(added));

  // 回填：舊檔（wrapHistory 喜劇＋done_ 動作，無標籤）
  run(`S = { castingTags: [], wrapHistory: [{gigId:${JSON.stringify(comedy.id)}}], flags: { ${JSON.stringify('done_' + action.id)}: 1 }, fame: 10, industryCreditDelta: 0 };`);
  run(`castingTagGenreBackfill360(S)`);
  let ids = run(`S.castingTags.map(t=>t.id).sort().join(',')`);
  check('② 舊檔回填兩標籤', ids === 'tag_action,tag_comedy', ids);
  const fameAfter = run(`S.fame`);
  check('② 回填唔改數值', fameAfter === 10 && run(`S.industryCreditDelta`) === 0, `fame=${fameAfter}`);
  run(`castingTagGenreBackfill360(S)`);
  check('② 回填冪等', run(`S.castingTags.length`) === 2);
  // 已有標籤唔重複（字串舊格式）
  run(`S = { castingTags: ['喜劇細胞'], wrapHistory: [{gigId:${JSON.stringify(comedy.id)}}], flags: {} };`);
  run(`castingTagGenreBackfill360(S)`);
  check('② 已有 label 唔重複', run(`S.castingTags.length`) === 1);
  // N9/N12 tagAny 命中（跟 liveTags 正規化＋indexOf 語義）
  run(`S = { castingTags: [], wrapHistory: [{gigId:${JSON.stringify(comedy.id)}}, {gigId:${JSON.stringify(action.id)}}], flags: {} }; castingTagGenreBackfill360(S);`);
  const gate = run(`(() => {
    const tags=[]; S.castingTags.forEach(t=>{ if(typeof t==='string') tags.push(t); else { if(t.id)tags.push(t.id); if(t.label)tags.push(t.label);} });
    const n9 = ["喜劇","comedy","動作","action","tag_comedy","喜劇細胞","tag_action","身手好"];
    const n12 = ["動作","action","tag_action","身手好"];
    return { n9: n9.some(t=>tags.indexOf(t)>=0), n12: n12.some(t=>tags.indexOf(t)>=0) };
  })()`);
  check('② N9 tagAny 命中', gate.n9 === true);
  check('② N12 tagAny 命中', gate.n12 === true);
}

// ================= ③ defaultWeekPlan 輪替 =================
{
  const ctx = vm.createContext({
    console,
    S: null,
    weekNumNow: () => Math.floor(((ctx.S && ctx.S.dayIndex) || 0) / 7) + 1,
    R: (a, b) => a + Math.floor(Math.random() * (b - a + 1)),
  });
  const run = (code) => vm.runInContext(code, ctx);
  run(extractConst('TRAIN75_SPEC'));
  run(extractConst('LEVELS75_STEP'));
  run(extractConst('LEVELS75_MAX'));
  run(extractConst('LEVELS75_NAMES'));
  run(extractFn('levels75Count'));
  run(extractFn('levels75Level'));
  run(extractFn('levels75GainRoll'));
  run(extractFn('defaultWeekPlan'));
  // stub applyCalib60：直接加落 S（驗輪替，唔驗增益數學——增益係既有已測 code）
  run(`function applyCalib60(g){ const out=[]; if(!g) return out; Object.keys(g).forEach(k=>{ if(k==='money'){ S.money=(Number(S.money)||0)+g[k]; } else if(k==='stress'){ S.stress=(Number(S.stress)||0)+g[k]; } else { S[k]=(Number(S[k])||0)+g[k]; } }); return out; }`);
  run(extractFn('train75ApplyLesson').replace('const applyGain60 = (typeof applyCalib60 === "function") ? applyCalib60 : apply;', 'const applyGain60 = applyCalib60;'));
  run(`function maybeUnlockMidCourses(notes){ const tc=S.trainCount||{}; const en=S.enrolled||{}; const total=Object.values(tc).reduce((a,b)=>a+b,0);
    if(total>=2 && !en.train_charm) en.train_charm=true; if(total>=2 && !en.train_stage) en.train_stage=true;
    if(total>=3 && !en.train_stamina) en.train_stamina=true; if(total>=4 && !en.train_iq) en.train_iq=true; }`);
  run(`function eventLine(){ return ''; }`);

  const base = { dayIndex: 30, money: 5000, stress: 0, acting: 18, stage: 14, vocal: 14, looks: 22, charm: 16, iq: 20, stamina: 75, enrolled: {}, trainCount: {}, mockDebts: [] };
  const set = (o) => { ctx.S = Object.assign({}, base, o); };

  set({ trainCount: { train_acting: 1 } });
  check('③ 演技 bootstrap 保留', run(`defaultWeekPlan()[1]`) === 'train_acting');
  set({ enrolled: { train_acting: true }, trainCount: { train_acting: 5 }, acting: 30 });
  check('③ 未報名歌藝最低→排歌藝', run(`defaultWeekPlan()[1]`) === 'train_vocal', run(`defaultWeekPlan()[1]`));
  set({ enrolled: { train_acting: true, train_vocal: true, train_stage: true }, trainCount: { train_acting: 5, train_vocal: 3 }, acting: 30, stage: 10, vocal: 20 });
  check('③ 已報名最低屬性（台風）', run(`defaultWeekPlan()[1]`) === 'train_stage', run(`defaultWeekPlan()[1]`));
  set({ enrolled: { train_acting: true, train_vocal: true, train_stage: true, train_looks: true, train_charm: true, train_iq: true, train_stamina: true },
        trainCount: { train_acting: 9, train_vocal: 9, train_stage: 9, train_looks: 9, train_charm: 9, train_iq: 0, train_stamina: 9 },
        acting: 60, stage: 60, vocal: 60, looks: 60, charm: 60, iq: 5 });
  check('③ 全報名最低屬性（智商）', run(`defaultWeekPlan()[1]`) === 'train_iq', run(`defaultWeekPlan()[1]`));
  set({ dayIndex: 0 });
  check('③ 第 1 週 base 不變', JSON.stringify(run(`defaultWeekPlan()`)) === JSON.stringify(["scout_all", "rest", "scout_all", "scout_all", "street", "cafe_gig", "rest"]));

  // 一年模擬：跟預設計劃（只報演技＋歌藝）
  set({ dayIndex: 7, enrolled: { train_acting: true, train_vocal: true } });
  const v0 = ctx.S.vocal;
  const picks = {};
  for (let w = 0; w < 52; w++) {
    const plan = run(`defaultWeekPlan()`);
    plan.forEach(id => {
      if (run(`!!TRAIN75_SPEC[${JSON.stringify(id)}]`)) { run(`train75ApplyLesson(${JSON.stringify(id)})`); picks[id] = (picks[id] || 0) + 1; }
    });
    ctx.S.dayIndex += 7; ctx.S.stress = 0;
  }
  check('③ 一年歌藝有成長', ctx.S.vocal > v0, `vocal ${v0}→${ctx.S.vocal} picks=${JSON.stringify(picks)}`);
  check('③ 一年演技有成長', ctx.S.acting > 18, `acting 18→${ctx.S.acting}`);
  // 一年模擬：全報名
  set({ dayIndex: 7, enrolled: { train_acting: true, train_vocal: true, train_stage: true, train_looks: true, train_charm: true, train_iq: true, train_stamina: true } });
  const start = { ...ctx.S };
  for (let w = 0; w < 52; w++) {
    const plan = run(`defaultWeekPlan()`);
    plan.forEach(id => { if (run(`!!TRAIN75_SPEC[${JSON.stringify(id)}]`)) run(`train75ApplyLesson(${JSON.stringify(id)})`); });
    ctx.S.dayIndex += 7; ctx.S.stress = 0;
  }
  const grew = ['acting', 'stage', 'vocal', 'looks', 'charm', 'iq'].filter(k => ctx.S[k] > start[k]);
  check('③ 全報名一年六科全成長', grew.length === 6, `grew=${grew.join(',')} vocal ${start.vocal}→${ctx.S.vocal}`);
}

console.log(`\nTOTAL ${pass}/${pass + fail} PASS`);
process.exit(fail ? 1 : 0);
