// v20a311 Q24 程天諾 ching_patron 暖版閘改嚴格版三旗齊備測試：
//   (A) 靜態：暖版閘要 T4＋flag_vocal_train＋ching_back_train＋ching_stand_slow，唔再提 back_polish／stand_fast；
//       冷版閘一行唔郁；grants（credit_enc84_ching_patron＋sideline280GrantCompletion("ching")）唔郁；
//       registry 次序 e4＜patron_cold＜patron（冷版排暖版前）；patron 對白 6 句／冷版 4 句唔郁
//   (B) when() 直接判定：三旗齊備→暖版；缺任何一旗→唔播暖版；
//       舊排除式會放行嘅組合（得 flag_vocal_train，無 back_train／stand_slow）→而家唔播（行為改變核心）；
//       T3（fav 69）三旗齊備→唔播；修音玩家→暖版唔播、冷版播
//   (C) 端到端 buildScript：三旗齊備→播 beat:ching_patron；缺 stand_slow→唔播；遲補 stand_slow→即播（漏做趕得切，唔死局）
//   (D) sideline280 一致：三旗齊備→收尾獎勵派（fame＋2／delta＋1／doneKey）；缺一旗→唔派
//   (E) 舊檔：舊排除式暖版玩家（得 flag_vocal_train）唔 crash、唔播暖版；三旗齊備舊檔照播暖版；S.story.flags 讀法照行
//   (S) 靜態：ching_e4 閘唔郁；gigs_new.json 仍係 323 張
// 用法：node tests/test_r311_ching_patron_strict.js [path-to-index.html]
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

/* ---- sandbox（跟 test_r310_ching_e4_n15.js） ---- */
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
const consts311 = ['ENC79_PLAYER_TIERS', 'ENC79_FAV_CAPS', 'ENC79_WEEK_SOFT_CAP', 'ENC79_STARS', 'ENC79_PILOT', 'ENC79_STAGEUP', 'ENC79_CAP_LINES', 'ENC79_WRAP_ECHO', 'ENC79_BEATS', 'ENC79_DIALOG', 'ENC79_FIRST_ALT98'].map(n => asVar(extractConst(n), n)).join('\n')
  + '\n' + asVar(extractDlg('ENC84_DLG_ching_tinlok'), 'ENC84_DLG_ching_tinlok')
  + '\nENC79_DIALOG["ching_tinlok"] = ENC84_DLG_ching_tinlok;';
const p2Start = html.indexOf('/* ---------- Phase 2 四星鏈節拍');
const p2End = html.indexOf('/* ===== ENC83 模組完 =====', p2Start);
if(p2Start < 0 || p2End < 0) throw new Error('Phase 2 beats region not found');
const p2Region = html.slice(p2Start, p2End);
const fns311 = ['enc79StarDef', 'enc79Hash', 'enc79Rand', 'enc79EnsureStars', 'enc79StarState', 'enc79TierOf', 'enc79PlayerTier', 'enc79FavCap', 'enc79AddFav', 'enc79WhisperActive', 'enc79GrantWhisper', 'enc79GrantCredit', 'enc79BoardHasStar', 'enc79BoardHasActionGig', 'enc79BeatOpen', 'enc79AnyBeatOpen', 'enc79PickBeat', 'enc79NormSeg', 'enc79BuildScript', 'enc79ChoiceFx', 'enc83NodeDone', 'enc83Flag', 'enc83HasCredit', 'enc83NewsOut', 'contra98EncFirstLocSwap', 'sideline280GrantCompletion', 'grant229Ensure', 'grant229GigById', 'grant229Record', 'grant229RecordFromEnc79'];
eval(consts311 + '\n' + asVar(extractConst('GRANT229_ENC79'), 'GRANT229_ENC79') + '\n' + p2Region + '\n' + extractAssign('ENC79_BEATS.ching_tinlok = [') + '\n' + fns311.map(extractFn).join('\n'));

/* ---- helpers ---- */
const WARM = beatOf('ching_tinlok', 'ching_patron');
const COLD = beatOf('ching_tinlok', 'ching_patron_cold');
function hasPatronSeg(script){ return ((script && script.steps) || []).some(s => s.seg === 'beat:ching_patron'); }
function buildPatron(flags, fav){
  resetS(950); _ys = { year: 1992, season: '冬' };
  setFav('ching_tinlok', fav === undefined ? 80 : fav);
  const st = metStar('ching_tinlok');
  for(const b of (ENC79_BEATS.ching_tinlok || [])) if(b.id !== 'ching_patron' && b.id !== 'ching_patron_cold') st.beatsDone[b.id] = 1;
  Object.assign(S.flags, flags || {});
  return enc79BuildScript('ching_tinlok', false);
}
const ALL3 = { flag_vocal_train: 1, ching_back_train: 1, ching_stand_slow: 1 };

/* ---------- (A) 靜態：閘字串＋grants＋次序＋對白 ---------- */
ok('A 暖版閘要三旗齊備（flag_vocal_train＋ching_back_train＋ching_stand_slow）',
  !!WARM && WARM.when.toString().indexOf('flag_vocal_train') >= 0 &&
  WARM.when.toString().indexOf('ching_back_train') >= 0 &&
  WARM.when.toString().indexOf('ching_stand_slow') >= 0);
ok('A 暖版閘唔再提排除式旗（ching_back_polish／ching_stand_fast）',
  !!WARM && WARM.when.toString().indexOf('ching_back_polish') < 0 &&
  WARM.when.toString().indexOf('ching_stand_fast') < 0);
ok('A 暖版閘仍要 T4（enc79TierOf(st.fav)>=4）',
  !!WARM && WARM.when.toString().indexOf('enc79TierOf(st.fav)>=4') >= 0);
ok('A 冷版閘一行唔郁（T4＋flag_vocal_polish／ching_back_polish／ching_stand_fast）',
  !!COLD && COLD.when.toString().indexOf('enc79TierOf(st.fav)>=4') >= 0 &&
  COLD.when.toString().indexOf('flag_vocal_polish') >= 0 &&
  COLD.when.toString().indexOf('ching_back_polish') >= 0 &&
  COLD.when.toString().indexOf('ching_stand_fast') >= 0);
ok('A grants 唔郁（credit_enc84_ching_patron＋sideline280GrantCompletion("ching")）',
  !!WARM && WARM.grants.toString().indexOf('credit_enc84_ching_patron') >= 0 &&
  WARM.grants.toString().indexOf('sideline280GrantCompletion("ching")') >= 0);
ok('A registry 次序唔郁（e4＜patron_cold＜patron，冷版排暖版前）',
  (() => {
    const ids = (ENC79_BEATS.ching_tinlok || []).map(b => b.id);
    return ids.indexOf('ching_e4') >= 0 && ids.indexOf('ching_e4') < ids.indexOf('ching_patron_cold') &&
      ids.indexOf('ching_patron_cold') < ids.indexOf('ching_patron');
  })());
const D = ENC79_DIALOG.ching_tinlok;
ok('A patron 對白 6 句唔郁（首句逐字）',
  !!D && !!D.beats && !!D.beats.ching_patron && D.beats.ching_patron.lines.length === 6 &&
  D.beats.ching_patron.lines[0][1] === '偉哥，等等，我有樣嘢要同你講，我嗰組跳唱騷嘅監製，嗰邊想搵多個人試下。');
ok('A patron_cold 對白 4 句唔郁',
  !!D && !!D.beats && !!D.beats.ching_patron_cold && D.beats.ching_patron_cold.lines.length === 4);

/* ---------- (B) when() 直接判定 ---------- */
ok('B 三旗齊備＋T4 → 暖版閘開',
  (() => { resetS(950); Object.assign(S.flags, ALL3); return WARM.when({ fav: 80 }) === true; })());
ok('B 缺 ching_back_train（漏做 Beat 3）→ 暖版閘閂',
  (() => { resetS(950); Object.assign(S.flags, { flag_vocal_train: 1, ching_stand_slow: 1 }); return WARM.when({ fav: 80 }) === false; })());
ok('B 缺 ching_stand_slow（漏做 Beat 4）→ 暖版閘閂',
  (() => { resetS(950); Object.assign(S.flags, { flag_vocal_train: 1, ching_back_train: 1 }); return WARM.when({ fav: 80 }) === false; })());
ok('B 缺 flag_vocal_train → 暖版閘閂',
  (() => { resetS(950); Object.assign(S.flags, { ching_back_train: 1, ching_stand_slow: 1 }); return WARM.when({ fav: 80 }) === false; })());
ok('B 舊排除式會放行嘅組合（得 flag_vocal_train）→ 而家唔播暖版',
  (() => { resetS(950); Object.assign(S.flags, { flag_vocal_train: 1 }); return WARM.when({ fav: 80 }) === false; })());
ok('B T3（fav 69）三旗齊備 → 暖版閘閂',
  (() => { resetS(950); Object.assign(S.flags, ALL3); return WARM.when({ fav: 69 }) === false; })());
ok('B 修音玩家（ching_back_polish，無 back_train／stand_slow）→ 暖版唔播、冷版播',
  (() => {
    resetS(950); Object.assign(S.flags, { flag_vocal_train: 1, ching_back_polish: 1 });
    return WARM.when({ fav: 80 }) === false && !!COLD.when({ fav: 80 });
  })());
ok('B flag_vocal_polish 玩家 → 冷版播、暖版唔播',
  (() => {
    resetS(950); Object.assign(S.flags, { flag_vocal_polish: 1 });
    return !!COLD.when({ fav: 80 }) && WARM.when({ fav: 80 }) === false;
  })());

/* ---------- (C) 端到端 buildScript ---------- */
ok('C 三旗齊備 → buildScript 播 beat:ching_patron',
  hasPatronSeg(buildPatron(ALL3, 80)));
ok('C 缺 ching_stand_slow → buildScript 唔播 beat:ching_patron',
  !hasPatronSeg(buildPatron({ flag_vocal_train: 1, ching_back_train: 1 }, 80)));
ok('C 缺 ching_back_train → buildScript 唔播 beat:ching_patron',
  !hasPatronSeg(buildPatron({ flag_vocal_train: 1, ching_stand_slow: 1 }, 80)));
ok('C 遲做趕得切：缺 stand_slow 唔播，遲補 stand_slow 即播（唔死局）',
  (() => {
    const b1 = buildPatron({ flag_vocal_train: 1, ching_back_train: 1 }, 80);
    if(hasPatronSeg(b1)) return false;
    S.flags.ching_stand_slow = 1;
    const st = S.stars.ching_tinlok;
    const b2 = enc79BuildScript('ching_tinlok', false);
    return hasPatronSeg(b2) && !st.beatsDone.ching_patron;
  })());
ok('C 三旗齊備但 T3（fav 69）→ buildScript 唔播 beat:ching_patron',
  !hasPatronSeg(buildPatron(ALL3, 69)));

/* ---------- (D) sideline280 一致 ---------- */
ok('D 三旗齊備 → sideline280 派收尾獎勵（fame＋2／delta＋1／doneKey）',
  (() => {
    resetS(950); Object.assign(S.flags, ALL3);
    const r = sideline280GrantCompletion('ching');
    return r === true && S.flags.sideline280_ching === 1 && S.fame === 32 && S.industryCreditDelta === 1;
  })(), 'fame=' + S.fame + ' delta=' + S.industryCreditDelta);
ok('D 缺 ching_back_train → sideline280 唔派（fame 唔郁、無 doneKey）',
  (() => {
    resetS(950); Object.assign(S.flags, { flag_vocal_train: 1, ching_stand_slow: 1 });
    const r = sideline280GrantCompletion('ching');
    return r === false && !S.flags.sideline280_ching && S.fame === 30 && S.industryCreditDelta === 0;
  })());
ok('D 缺 ching_stand_slow → sideline280 唔派',
  (() => {
    resetS(950); Object.assign(S.flags, { flag_vocal_train: 1, ching_back_train: 1 });
    const r = sideline280GrantCompletion('ching');
    return r === false && !S.flags.sideline280_ching && S.fame === 30;
  })());
ok('D 暖版閘同 sideline280 讀法一致：同一組旗，閘開＝獎勵派、閘閂＝獎勵唔派',
  (() => {
    const cases = [
      [ALL3, true],
      [{ flag_vocal_train: 1, ching_stand_slow: 1 }, false],
      [{ flag_vocal_train: 1, ching_back_train: 1 }, false],
      [{ flag_vocal_train: 1 }, false],
      [{ ching_back_train: 1, ching_stand_slow: 1 }, false],
    ];
    return cases.every(([flags, expect]) => {
      resetS(950); Object.assign(S.flags, flags);
      const gate = WARM.when({ fav: 80 });
      const r = sideline280GrantCompletion('ching');
      return gate === expect && r === expect;
    });
  })());

/* ---------- (E) 舊檔 ---------- */
ok('E 舊檔（得 flag_vocal_train，舊排除式暖版玩家）唔 crash、唔播暖版',
  (() => {
    resetS(950); _ys = { year: 1992, season: '冬' };
    S.stars = { ching_tinlok: { fav: 80, met: true, stage: 3, beatsDone: { ching_e4: 1, ching_rival: 1, ching_after_train: 1, ching_after_polish: 1, ching_patron_cold: 1 } } };
    S.flags.flag_vocal_train = 1;
    let b = null, err = null;
    try{ b = enc79BuildScript('ching_tinlok', false); }catch(e){ err = e; }
    return !err && !!b && !hasPatronSeg(b);
  })());
ok('E 舊檔三旗齊備照播暖版',
  (() => {
    resetS(950); _ys = { year: 1992, season: '冬' };
    S.stars = { ching_tinlok: { fav: 80, met: true, stage: 3, beatsDone: { ching_e4: 1, ching_rival: 1, ching_after_train: 1, ching_after_polish: 1, ching_patron_cold: 1 } } };
    Object.assign(S.flags, ALL3);
    let b = null, err = null;
    try{ b = enc79BuildScript('ching_tinlok', false); }catch(e){ err = e; }
    return !err && !!b && hasPatronSeg(b);
  })());
ok('E 舊檔 S.story.flags 讀法（flag_vocal_train 喺 story.flags）照播暖版',
  (() => {
    resetS(950); Object.assign(S.flags, { ching_back_train: 1, ching_stand_slow: 1 });
    S.story.flags.flag_vocal_train = 1;
    return WARM.when({ fav: 80 }) === true;
  })());

/* ---------- (S) 靜態其餘 ---------- */
ok('S ching_e4 註冊閘唔郁（tier≥1＋enc83NewsOut("E4")）',
  (() => { const w = beatOf('ching_tinlok', 'ching_e4').when.toString(); return w.indexOf('enc83NewsOut("E4")') >= 0 && w.indexOf('flag_vocal') < 0; })());
ok('S gigs_new.json 仍係 323 張', GIGS_ARR.length === 323, 'count=' + GIGS_ARR.length);

if(fails.length){ console.log('\nFAILURES: ' + fails.length); process.exit(1); }
console.log('\nALL PASS');
