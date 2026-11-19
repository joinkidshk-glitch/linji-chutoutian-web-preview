// v20a314 Q24前例（程線 v311）駱家聲 lok_patron 暖版閘改嚴格版測試：
//   (A) 靜態：暖版閘要 T4＋lok_calm_truth＋唔係 join_rant／loose_row／cover_first；
//       冷版閘（patron_cold／patron_cover）一行唔郁；grants（credit_enc83_lok_patron＋sideline280GrantCompletion("lok")）唔郁；
//       registry 次序 e4grudge＜patron_cold＜patron_cover＜patron＜finale；patron 對白 6 句／冷版 4 句／翻唱 4 句唔郁
//   (B) when() 直接判定：lok_calm_truth 齊備→暖版；無旗→暖／冷／翻唱都唔開；
//       舊排除式會放行嘅組合（無旗）→而家唔播（行為改變核心）；
//       T3（fav 69）有 calm_truth→唔播；calm_truth＋任一壞旗→暖版唔播、對應冷版播
//   (C) 端到端 buildScript：calm_truth 齊備→播 beat:lok_patron；無旗→唔播；遲補 calm_truth→即播（漏做趕得切，唔死局）
//   (D) sideline280 一致：calm_truth 齊備→收尾獎勵派（fame＋2／delta＋1／doneKey）；無旗／有壞旗→唔派；
//       閘開＝獎勵派、閘閂＝獎勵唔派（同一組旗對照）
//   (E) 舊檔：無旗舊檔（舊排除式暖版玩家）唔 crash、唔播暖版；calm_truth 舊檔照播暖版
//   (S) 靜態：lok_e4grudge 閘唔郁；gigs_new.json 仍係 323 張
// 用法：node tests/test_r314_lok_patron_strict.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const GIGS_NEW = require('../content/gigs_new.json');
const GIGS_ARR = Array.isArray(GIGS_NEW) ? GIGS_NEW : (GIGS_NEW.gigs || []);
let fails = [];
function ok(name, cond, extra){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name + (extra ? ' :: ' + extra : '')); }
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
    else if(c === ';' && !started) { j++; break; }
  }
  return html.slice(i, j);
}
function extractDlg(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('missing ' + name);
  const j = html.indexOf('\nconst ', i + 10);
  return html.slice(i, j < 0 ? undefined : j);
}
function extractAssign(startMarker){
  const i = html.indexOf(startMarker);
  if(i < 0) throw new Error('assign not found: ' + startMarker);
  let depth = 0, started = false, j = i;
  for(; j < html.length; j++){
    const c = html[j];
    if(c === '{' || c === '['){ depth++; started = true; }
    else if(c === '}' || c === ']'){ depth--; if(started && depth === 0){ j++; break; } }
  }
  return html.slice(i, j);
}

/* ---- sandbox（跟 test_r311_ching_patron_strict.js） ---- */
let S;
let _ys = { year: 1992, season: '冬' };
let _doneNodes = new Set();
function resetS(day){
  S = { dayIndex: day || 0, fame: 30, money: 2000, flags: {}, npcs: { agent: 0 }, mockRumors: [], mockDebts: [], mockCredits: [], board: {}, shoots: [], mapTips: {}, story: { flags: {} }, starWeek: {}, starFavWeek: { week: -1, gain: 0 }, weekGigsDone: 0, starWhispers: {}, grant229Queue: [], pendingAud: [], news82: { pub: { E4: 1 }, arc: {} }, industryCreditDelta: 0 };
  _doneNodes = new Set();
  _ledger = null;
}
function setFav(sid, n){ enc79EnsureStars(); S.stars[sid].fav = n; }
function beatOf(sid, id){ return (ENC79_BEATS[sid] || []).find(b => b.id === id); }
function metStar(sid){ enc79EnsureStars(); S.stars[sid].met = true; S.stars[sid].stage = 3; return S.stars[sid]; }
function weekNumNow(){ return 3; }
function yearSeasonNow(){ return _ys; }
function enc87StoryFlag(f){ return !!((S.flags && S.flags[f]) || (S.story && S.story.flags && S.story.flags[f])); }
function syncNotebookMirror(){}
function syncDualTracks(){}
function saveQ(){}
function toast(){}
function enc79LocName(id){ return id; }
let _ledger = null;
function ensureFavorLedger(){ if(!_ledger) _ledger = { settled: 0, credits: 0, exodus: [], counted: {} }; return _ledger; }
function favorLedgerNoteCredit(id){ const L = ensureFavorLedger(); if(L.counted[id]) return false; L.counted[id] = { kind: 'credit' }; L.credits++; return true; }
const StoryOC = {
  isDone: (id) => _doneNodes.has(id),
  listOpen: () => ({ open: [] }),
  findNodeRaw: (id) => ({ id }),
};
function storyNodeLocId(n){ return n && n.__loc; }
var GIGS = GIGS_ARR;

const asVar = (code, name) => code.replace('const ' + name + ' =', 'var ' + name + ' =');
const consts314 = ['ENC79_PLAYER_TIERS', 'ENC79_FAV_CAPS', 'ENC79_WEEK_SOFT_CAP', 'ENC79_STARS', 'ENC79_PILOT', 'ENC79_STAGEUP', 'ENC79_CAP_LINES', 'ENC79_WRAP_ECHO', 'ENC79_BEATS', 'ENC79_DIALOG', 'ENC79_FIRST_ALT98'].map(n => asVar(extractConst(n), n)).join('\n')
  + '\n' + asVar(extractDlg('ENC83_DLG_lok_gasing'), 'ENC83_DLG_lok_gasing')
  + '\nENC79_DIALOG["lok_gasing"] = ENC83_DLG_lok_gasing;';
const p2Start = html.indexOf('/* ---------- Phase 2 四星鏈節拍');
const p2End = html.indexOf('/* ===== ENC83 模組完 =====', p2Start);
if(p2Start < 0 || p2End < 0) throw new Error('Phase 2 beats region not found');
const p2Region = html.slice(p2Start, p2End);
const fns314 = ['enc79StarDef', 'enc79Hash', 'enc79Rand', 'enc79EnsureStars', 'enc79StarState', 'enc79TierOf', 'enc79PlayerTier', 'enc79FavCap', 'enc79AddFav', 'enc79WhisperActive', 'enc79GrantWhisper', 'enc79GrantCredit', 'enc79BoardHasStar', 'enc79BoardHasActionGig', 'enc79BeatOpen', 'enc79AnyBeatOpen', 'enc79PickBeat', 'enc79NormSeg', 'enc79BuildScript', 'enc79ChoiceFx', 'enc83NodeDone', 'enc83Flag', 'enc83HasCredit', 'enc83NewsOut', 'contra98EncFirstLocSwap', 'sideline280GrantCompletion', 'grant229Ensure', 'grant229GigById', 'grant229Record', 'grant229RecordFromEnc79'];
eval(consts314 + '\n' + asVar(extractConst('GRANT229_ENC79'), 'GRANT229_ENC79') + '\n' + p2Region + '\n' + extractAssign('ENC79_BEATS.lok_gasing = [') + '\n' + fns314.map(extractFn).join('\n'));

/* ---- helpers ---- */
const WARM = beatOf('lok_gasing', 'lok_patron');
const COLD = beatOf('lok_gasing', 'lok_patron_cold');
const COVER = beatOf('lok_gasing', 'lok_patron_cover');
function hasPatronSeg(script){ return ((script && script.steps) || []).some(s => s.seg === 'beat:lok_patron'); }
function buildPatron(flags, fav){
  resetS(950); _ys = { year: 1992, season: '冬' };
  setFav('lok_gasing', fav === undefined ? 80 : fav);
  const st = metStar('lok_gasing');
  for(const b of (ENC79_BEATS.lok_gasing || [])) if(b.id !== 'lok_patron' && b.id !== 'lok_patron_cold' && b.id !== 'lok_patron_cover') st.beatsDone[b.id] = 1;
  Object.assign(S.flags, flags || {});
  return enc79BuildScript('lok_gasing', false);
}
const CALM = { lok_calm_truth: 1 };

/* ---------- (A) 靜態：閘字串＋grants＋次序＋對白 ---------- */
ok('A 暖版閘要 lok_calm_truth 正面旗',
  !!WARM && WARM.when.toString().indexOf('lok_calm_truth') >= 0);
ok('A 暖版閘仍排除 join_rant／loose_row／cover_first',
  !!WARM && WARM.when.toString().indexOf('lok_join_rant') >= 0 &&
  WARM.when.toString().indexOf('lok_loose_row') >= 0 &&
  WARM.when.toString().indexOf('lok_cover_first') >= 0);
ok('A 暖版閘仍要 T4（enc79TierOf(st.fav)>=4）',
  !!WARM && WARM.when.toString().indexOf('enc79TierOf(st.fav)>=4') >= 0);
ok('A 冷版閘一行唔郁（T4＋loose_row／join_rant）',
  !!COLD && COLD.when.toString().indexOf('enc79TierOf(st.fav)>=4') >= 0 &&
  COLD.when.toString().indexOf('lok_loose_row') >= 0 &&
  COLD.when.toString().indexOf('lok_join_rant') >= 0 &&
  COLD.when.toString().indexOf('lok_calm_truth') < 0);
ok('A 翻唱閘一行唔郁（T4＋cover_first＋唔係 loose_row／join_rant）',
  !!COVER && COVER.when.toString().indexOf('enc79TierOf(st.fav)>=4') >= 0 &&
  COVER.when.toString().indexOf('lok_cover_first') >= 0 &&
  COVER.when.toString().indexOf('lok_loose_row') >= 0 &&
  COVER.when.toString().indexOf('lok_join_rant') >= 0 &&
  COVER.when.toString().indexOf('lok_calm_truth') < 0);
ok('A grants 唔郁（credit_enc83_lok_patron＋sideline280GrantCompletion("lok")）',
  !!WARM && WARM.grants.toString().indexOf('credit_enc83_lok_patron') >= 0 &&
  WARM.grants.toString().indexOf('sideline280GrantCompletion("lok")') >= 0);
ok('A registry 次序唔郁（e4grudge＜patron_cold＜patron_cover＜patron＜finale，冷版／翻唱排暖版前）',
  (() => {
    const ids = (ENC79_BEATS.lok_gasing || []).map(b => b.id);
    return ids.indexOf('lok_e4grudge') >= 0 && ids.indexOf('lok_e4grudge') < ids.indexOf('lok_patron_cold') &&
      ids.indexOf('lok_patron_cold') < ids.indexOf('lok_patron_cover') &&
      ids.indexOf('lok_patron_cover') < ids.indexOf('lok_patron') &&
      ids.indexOf('lok_patron') < ids.indexOf('lok_finale');
  })());
const D = ENC79_DIALOG.lok_gasing;
ok('A patron 對白 6 句唔郁（首句逐字）',
  !!D && !!D.beats && !!D.beats.lok_patron && D.beats.lok_patron.lines.length === 6 &&
  D.beats.lok_patron.lines[0][1] === '偉翔，你過嚟，我有件事同你講，唔好周圍揚。');
ok('A patron_cold 對白 4 句唔郁',
  !!D && !!D.beats && !!D.beats.lok_patron_cold && D.beats.lok_patron_cold.lines.length === 4);
ok('A patron_cover 對白 4 句唔郁',
  !!D && !!D.beats && !!D.beats.lok_patron_cover && D.beats.lok_patron_cover.lines.length === 4);

/* ---------- (B) when() 直接判定 ---------- */
ok('B lok_calm_truth 齊備＋T4 → 暖版閘開',
  (() => { resetS(950); Object.assign(S.flags, CALM); return WARM.when({ fav: 80 }) === true; })());
ok('B 無旗（漏做 Beat 5）→ 暖／冷／翻唱都唔開',
  (() => { resetS(950); return !WARM.when({ fav: 80 }) && !COLD.when({ fav: 80 }) && !COVER.when({ fav: 80 }); })());
ok('B 舊排除式會放行嘅組合（無旗、T4）→ 而家唔播暖版（行為改變核心）',
  (() => { resetS(950); return WARM.when({ fav: 80 }) === false; })());
ok('B T3（fav 69）有 calm_truth → 暖版閘閂',
  (() => { resetS(950); Object.assign(S.flags, CALM); return WARM.when({ fav: 69 }) === false; })());
ok('B calm_truth＋lok_join_rant → 暖版唔播、冷版播',
  (() => {
    resetS(950); Object.assign(S.flags, { lok_calm_truth: 1, lok_join_rant: 1 });
    return WARM.when({ fav: 80 }) === false && !!COLD.when({ fav: 80 });
  })());
ok('B calm_truth＋lok_loose_row → 暖版唔播、冷版播',
  (() => {
    resetS(950); Object.assign(S.flags, { lok_calm_truth: 1, lok_loose_row: 1 });
    return WARM.when({ fav: 80 }) === false && !!COLD.when({ fav: 80 });
  })());
ok('B calm_truth＋lok_cover_first → 暖版唔播、翻唱播',
  (() => {
    resetS(950); Object.assign(S.flags, { lok_calm_truth: 1, lok_cover_first: 1 });
    return !WARM.when({ fav: 80 }) && !!COVER.when({ fav: 80 }) && !COLD.when({ fav: 80 });
  })());
ok('B lok_join_rant 玩家（無 calm_truth）→ 冷版播、暖版唔播',
  (() => {
    resetS(950); Object.assign(S.flags, { lok_join_rant: 1 });
    return !!COLD.when({ fav: 80 }) && WARM.when({ fav: 80 }) === false;
  })());
ok('B lok_cover_first 玩家（無 calm_truth）→ 翻唱播、暖版唔播',
  (() => {
    resetS(950); Object.assign(S.flags, { lok_cover_first: 1 });
    return !!COVER.when({ fav: 80 }) && WARM.when({ fav: 80 }) === false;
  })());

/* ---------- (C) 端到端 buildScript ---------- */
ok('C calm_truth 齊備 → buildScript 播 beat:lok_patron',
  hasPatronSeg(buildPatron(CALM, 80)));
ok('C 無旗 → buildScript 唔播 beat:lok_patron',
  !hasPatronSeg(buildPatron({}, 80)));
ok('C 漏做趕得切：無旗唔播，遲補 calm_truth 即播（唔死局）',
  (() => {
    const b1 = buildPatron({}, 80);
    if(hasPatronSeg(b1)) return false;
    S.flags.lok_calm_truth = 1;
    const st = S.stars.lok_gasing;
    const b2 = enc79BuildScript('lok_gasing', false);
    return hasPatronSeg(b2) && !st.beatsDone.lok_patron;
  })());
ok('C calm_truth 齊備但 T3（fav 69）→ buildScript 唔播 beat:lok_patron',
  !hasPatronSeg(buildPatron(CALM, 69)));
ok('C calm_truth＋lok_join_rant → buildScript 唔播暖版（行冷版）',
  !hasPatronSeg(buildPatron({ lok_calm_truth: 1, lok_join_rant: 1 }, 80)));

/* ---------- (D) sideline280 一致 ---------- */
ok('D calm_truth 齊備 → sideline280 派收尾獎勵（fame＋2／delta＋1／doneKey）',
  (() => {
    resetS(950); Object.assign(S.flags, CALM);
    const r = sideline280GrantCompletion('lok');
    return r === true && S.flags.sideline280_lok === 1 && S.fame === 32 && S.industryCreditDelta === 1;
  })(), 'fame=' + S.fame + ' delta=' + S.industryCreditDelta);
ok('D 無旗 → sideline280 唔派（fame 唔郁、無 doneKey）',
  (() => {
    resetS(950);
    const r = sideline280GrantCompletion('lok');
    return r === false && !S.flags.sideline280_lok && S.fame === 30 && S.industryCreditDelta === 0;
  })());
ok('D calm_truth＋lok_join_rant → sideline280 唔派',
  (() => {
    resetS(950); Object.assign(S.flags, { lok_calm_truth: 1, lok_join_rant: 1 });
    const r = sideline280GrantCompletion('lok');
    return r === false && !S.flags.sideline280_lok && S.fame === 30;
  })());
ok('D 暖版閘同 sideline280 讀法一致：同一組旗，閘開＝獎勵派、閘閂＝獎勵唔派',
  (() => {
    const cases = [
      [CALM, true],
      [{}, false],
      [{ lok_calm_truth: 1, lok_join_rant: 1 }, false],
      [{ lok_calm_truth: 1, lok_loose_row: 1 }, false],
      [{ lok_calm_truth: 1, lok_cover_first: 1 }, false],
      [{ lok_join_rant: 1 }, false],
      [{ lok_cover_first: 1 }, false],
    ];
    return cases.every(([flags, expect]) => {
      resetS(950); Object.assign(S.flags, flags);
      const gate = WARM.when({ fav: 80 });
      const r = sideline280GrantCompletion('lok');
      return gate === expect && r === expect;
    });
  })());

/* ---------- (E) 舊檔 ---------- */
ok('E 舊檔（無旗，舊排除式暖版玩家）唔 crash、唔播暖版',
  (() => {
    resetS(950); _ys = { year: 1992, season: '冬' };
    S.stars = { lok_gasing: { fav: 80, met: true, stage: 3, beatsDone: { lok_foreshadow: 1, lok_intel: 1, lok_help: 1, lok_cover: 1, lok_recover: 1, lok_e4grudge: 1, lok_patron_cold: 1, lok_patron_cover: 1 } } };
    let b = null, err = null;
    try{ b = enc79BuildScript('lok_gasing', false); }catch(e){ err = e; }
    return !err && !!b && !hasPatronSeg(b);
  })());
ok('E 舊檔 calm_truth 齊備照播暖版',
  (() => {
    resetS(950); _ys = { year: 1992, season: '冬' };
    S.stars = { lok_gasing: { fav: 80, met: true, stage: 3, beatsDone: { lok_foreshadow: 1, lok_intel: 1, lok_help: 1, lok_cover: 1, lok_recover: 1, lok_e4grudge: 1, lok_patron_cold: 1, lok_patron_cover: 1 } } };
    Object.assign(S.flags, CALM);
    let b = null, err = null;
    try{ b = enc79BuildScript('lok_gasing', false); }catch(e){ err = e; }
    return !err && !!b && hasPatronSeg(b);
  })());

/* ---------- (S) 靜態其餘 ---------- */
ok('S lok_e4grudge 註冊閘唔郁（tier≥1＋enc83NewsOut("E4")）',
  (() => { const w = beatOf('lok_gasing', 'lok_e4grudge').when.toString(); return w.indexOf('enc83NewsOut("E4")') >= 0 && w.indexOf('lok_calm_truth') < 0; })());
ok('S lok_finale 閘唔郁（要 beatsDone.lok_patron）',
  (() => { const w = beatOf('lok_gasing', 'lok_finale').when.toString(); return w.indexOf('beatsDone') >= 0 && w.indexOf('lok_patron') >= 0; })());
ok('S gigs_new.json 仍係 323 張', GIGS_ARR.length === 323, 'count=' + GIGS_ARR.length);

if(fails.length){ console.log('\nFAILURES: ' + fails.length); process.exit(1); }
console.log('\nALL PASS');
