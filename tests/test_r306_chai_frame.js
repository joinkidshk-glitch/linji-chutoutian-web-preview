// v20a306 Q19 齊鎮海 FRAME cap／wrap 各寫兩個版本測試：
//   (A) 數據：FRAME 有 cap_try／wrap_safe（S 句、唔同舊句）；stageup 唔郁；註冊後 CAP／WRAP 預設仍係舊句
//   (B) cap 分流：try_new → cap_try；play_safe／未揀／舊檔 → 舊 cap；播完清 capHit
//   (C) wrap 分流：play_safe → wrap_safe；try_new／未揀／舊檔 → 舊 wrap；播完清 wrapEcho
//   (D) 暖／冷／finale 唔受影響：暖版 heart 照播（v20a318 之後獎勵／提攜讀法改 truth_change only，try_new 唔再係必要條件）；冷版 heartCold 照播；finale 尾句分流照舊（try_new 用 wrap 句、play_safe 用 cap 句）
//   (E) 舊檔：無 Beat 5 旗 → cap／wrap 都係舊句，唔 crash
//   (F) 靜態：其他星 cap／wrap 唔郁；chai_try_new／chai_play_safe 授出點唯一（Beat 5 抉擇）；gigs_new.json 仍係 323 張
// 用法：node tests/test_r306_chai_frame.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const GIGS_NEW = require('../content/gigs_new.json');
const GIGS_ARR = Array.isArray(GIGS_NEW) ? GIGS_NEW : (GIGS_NEW.gigs || []);
let fails = [];
function ok(name, cond, extra){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name + (extra ? ' ' + extra : '')); }
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
function extractAssign(prefix){
  const i = html.indexOf(prefix);
  if(i < 0) throw new Error('assign not found: ' + prefix);
  let depth = 0, started = false, j = i;
  for(; j < html.length; j++){
    const c = html[j];
    if(c === '['){ depth++; started = true; }
    else if(c === ']'){ depth--; if(started && depth === 0){ j++; break; } }
  }
  return html.slice(i, j);
}

/* ---- sandbox（跟 test_r305_warm_finale.js；加 ENC83_FRAME_chai_zanhoi，齊專用） ---- */
let S;
let _ys = { year: 1990, season: '春' };
let _doneNodes = new Set();
function resetS(day){
  S = { dayIndex: day || 0, fame: 30, money: 2000, flags: {}, npcs: { agent: 0 }, mockRumors: [], mockDebts: [], mockCredits: [], board: {}, shoots: [], mapTips: {}, story: { flags: {} }, starWeek: {}, starFavWeek: { week: -1, gain: 0 }, weekGigsDone: 0, starWhispers: {}, grant229Queue: [], pendingAud: [], news82: { pub: {}, arc: {} }, industryCreditDelta: 0 };
  _doneNodes = new Set();
  _ledger = null;
}
function setFav(sid, n){ enc79EnsureStars(); S.stars[sid].fav = n; }
function beatOf(sid, id){ return (ENC79_BEATS[sid] || []).find(b => b.id === id); }
function metStar(sid){ enc79EnsureStars(); S.stars[sid].met = true; S.stars[sid].stage = 3; return S.stars[sid]; }
function doneAllBeats(sid){ const st = metStar(sid); for(const b of (ENC79_BEATS[sid] || [])) st.beatsDone[b.id] = 1; return st; }
function doneExcept(sid, keep){
  const st = metStar(sid);
  for(const b of (ENC79_BEATS[sid] || [])) if(!keep.includes(b.id)) st.beatsDone[b.id] = 1;
  return st;
}
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
var GIGS = [];

const asVar = (code, name) => code.replace('const ' + name + ' =', 'var ' + name + ' =');
const consts306 = ['ENC79_PLAYER_TIERS', 'ENC79_FAV_CAPS', 'ENC79_WEEK_SOFT_CAP', 'ENC79_STARS', 'ENC79_PILOT', 'ENC79_STAGEUP', 'ENC79_CAP_LINES', 'ENC79_WRAP_ECHO', 'ENC79_BEATS', 'ENC79_DIALOG', 'ENC79_FIRST_ALT98', 'ENC83_FRAME_chai_zanhoi'].map(n => asVar(extractConst(n), n)).join('\n')
  + '\n' + ['ENC83_DLG_chai_zanhoi'].map(n => asVar(extractDlg(n), n)).join('\n')
  + '\nENC79_DIALOG["chai_zanhoi"] = ENC83_DLG_chai_zanhoi;\nENC79_STAGEUP.chai_zanhoi = ENC83_FRAME_chai_zanhoi.stageup;\nENC79_CAP_LINES.chai_zanhoi = ENC83_FRAME_chai_zanhoi.cap;\nENC79_WRAP_ECHO.chai_zanhoi = ENC83_FRAME_chai_zanhoi.wrap;';
const p2Start = html.indexOf('/* ---------- Phase 2 四星鏈節拍');
const p2End = html.indexOf('/* ===== ENC83 模組完 =====', p2Start);
if(p2Start < 0 || p2End < 0) throw new Error('Phase 2 beats region not found');
const p2Region = html.slice(p2Start, p2End);
const fns306 = ['enc79StarDef', 'enc79Hash', 'enc79Rand', 'enc79EnsureStars', 'enc79StarState', 'enc79TierOf', 'enc79PlayerTier', 'enc79FavCap', 'enc79AddFav', 'enc79WhisperActive', 'enc79GrantWhisper', 'enc79GrantCredit', 'enc79BoardHasStar', 'enc79BoardHasActionGig', 'enc79BeatOpen', 'enc79AnyBeatOpen', 'enc79PickBeat', 'enc79NormSeg', 'enc79BuildScript', 'enc83NodeDone', 'enc83Flag', 'enc83HasCredit', 'enc83NewsOut', 'contra98EncFirstLocSwap', 'sideline280GrantCompletion', 'grant229Ensure', 'grant229GigById', 'grant229Record', 'grant229RecordFromEnc79'];
eval(consts306 + '\n' + asVar(extractConst('GRANT229_ENC79'), 'GRANT229_ENC79') + '\n' + p2Region + '\n' + fns306.map(extractFn).join('\n'));

/* ---- helpers ---- */
function hasText(b, sub){ return (b && b.steps || []).some(s => String(s.text || '').indexOf(sub) >= 0); }
function segSteps(b, seg){ return (b && b.steps || []).filter(s => s.seg === seg); }
function playSeg(b, seg){ segSteps(b, seg).forEach(s => { try{ if(typeof s.segFx === 'function') s.segFx(); }catch(_e){} }); }

const CAP_OLD = '阿偉，今日傾到呢度先啦，我仲有場戲要默。你有呢份心，我領咗，不過有啲路，仲要慢慢行，唔好急。';
const WRAP_OLD = '殺青喇，阿偉。同你做呢套戲，我冇睇錯人。嚟緊嗰條路點行，你自己企穩，我會喺後面望住。';
const CAP_TRY = '阿偉，你肯試新嘢，呢份膽色我認。不過膽色唔係火候——等你試埋嗰個角色，企得穩先，我哋先再傾。';
const WRAP_SAFE = '殺青喇，阿偉。呢套戲你企得穩，冇浮冇躁，已經好難得。慢慢嚟唔係慢，係行得穩，之後嗰條路，你照咁行，我放心。';

/* 封住 beat／heart，只留 cap／wrap 兩句 */
function buildFrame(flags, mark){
  resetS(100); _ys = { year: 1990, season: '春' };
  setFav('chai_zanhoi', 45); // T3
  const st = doneAllBeats('chai_zanhoi');
  st.heartDone = true;
  if(mark === 'cap') st.capHit = true;
  if(mark === 'wrap') st.wrapEcho = true;
  Object.assign(S.flags, flags || {});
  return enc79BuildScript('chai_zanhoi', false);
}

/* ---------- (A) 數據形狀 ---------- */
(function(){
  const F = ENC83_FRAME_chai_zanhoi;
  ok('A FRAME 有 cap_try（S 句、非空）', !!F && Array.isArray(F.cap_try) && F.cap_try[0] === 'S' && typeof F.cap_try[1] === 'string' && F.cap_try[1].length > 0);
  ok('A FRAME 有 wrap_safe（S 句、非空）', !!F && Array.isArray(F.wrap_safe) && F.wrap_safe[0] === 'S' && typeof F.wrap_safe[1] === 'string' && F.wrap_safe[1].length > 0);
  ok('A cap_try 唔等於舊 cap 句', F.cap_try[1] !== CAP_OLD, 'cap_try=' + F.cap_try[1]);
  ok('A wrap_safe 唔等於舊 wrap 句', F.wrap_safe[1] !== WRAP_OLD, 'wrap_safe=' + F.wrap_safe[1]);
  ok('A cap_try 講試新嘢（膽色／試埋嗰個角色），同 play_safe 版唔同主題', /試新嘢|膽色/.test(F.cap_try[1]) && /試埋嗰個角色/.test(F.cap_try[1]));
  ok('A wrap_safe 講企得穩＋慢慢嚟（冇浮冇躁／行得穩），同 try_new 版唔同主題', /冇浮冇躁/.test(F.wrap_safe[1]) && /慢慢嚟唔係慢/.test(F.wrap_safe[1]));
  ok('A stageup 唔郁（3 句逐字）', Array.isArray(F.stageup) && F.stageup.length === 3 &&
    F.stageup[0][1] === '阿偉，唔知由幾時開始，我同你講嘢，唔再當你係企後面嗰個臨時演員喇。' &&
    F.stageup[1][1] === '人同人之間，過咗嗰條線，就唔同晒。你自己應該都覺得到。' &&
    F.stageup[2][1] === '齊鎮海說完，輕輕點了下頭，轉身回到監視器後面，背影和初見那天一樣挺直。');
  ok('A 註冊後 CAP／WRAP 預設仍係舊句（預設即舊句）', ENC79_CAP_LINES.chai_zanhoi && ENC79_CAP_LINES.chai_zanhoi[1] === CAP_OLD && ENC79_WRAP_ECHO.chai_zanhoi && ENC79_WRAP_ECHO.chai_zanhoi[1] === WRAP_OLD);
  ok('A cap_try／wrap_safe 係 S 對白（廣東話句，唔係旁白）', F.cap_try[0] === 'S' && F.wrap_safe[0] === 'S');
})();

/* ---------- (B) cap 分流 ---------- */
(function(){
  const bTry = buildFrame({ chai_try_new: 1 }, 'cap');
  const sTry = segSteps(bTry, 'cap:chai_zanhoi');
  ok('B try_new → cap 句係 cap_try（肯試新嘢）', sTry.length === 1 && sTry[0].text === CAP_TRY, 'got=' + (sTry[0] && sTry[0].text));
  const bSafe = buildFrame({ chai_play_safe: 1 }, 'cap');
  const sSafe = segSteps(bSafe, 'cap:chai_zanhoi');
  ok('B play_safe → cap 句係舊 cap 句（慢慢行唔好急）', sSafe.length === 1 && sSafe[0].text === CAP_OLD, 'got=' + (sSafe[0] && sSafe[0].text));
  const bNone = buildFrame({}, 'cap');
  const sNone = segSteps(bNone, 'cap:chai_zanhoi');
  ok('B 未揀 Beat 5 → cap 句係舊 cap 句（預設）', sNone.length === 1 && sNone[0].text === CAP_OLD, 'got=' + (sNone[0] && sNone[0].text));
  const bBoth = buildFrame({ chai_try_new: 1, chai_play_safe: 1 }, 'cap');
  const sBoth = segSteps(bBoth, 'cap:chai_zanhoi');
  ok('B 兩旗齊有（防禦）→ cap 句係 cap_try（try_new 優先）', sBoth.length === 1 && sBoth[0].text === CAP_TRY);
  const bNoHit = buildFrame({ chai_try_new: 1 }, null);
  ok('B capHit 唔係 true → 唔出 cap 句', segSteps(bNoHit, 'cap:chai_zanhoi').length === 0);
  ok('B cap 句播完 → 清 capHit（唔重播）', (() => { playSeg(bTry, 'cap:chai_zanhoi'); return S.stars.chai_zanhoi.capHit === false; })());
})();

/* ---------- (C) wrap 分流 ---------- */
(function(){
  const bSafe = buildFrame({ chai_play_safe: 1 }, 'wrap');
  const sSafe = segSteps(bSafe, 'wrapecho:chai_zanhoi');
  ok('C play_safe → wrap 句係 wrap_safe（企得穩嗰邊）', sSafe.length === 1 && sSafe[0].text === WRAP_SAFE, 'got=' + (sSafe[0] && sSafe[0].text));
  const bTry = buildFrame({ chai_try_new: 1 }, 'wrap');
  const sTry = segSteps(bTry, 'wrapecho:chai_zanhoi');
  ok('C try_new → wrap 句係舊 wrap 句（殺青喇…）', sTry.length === 1 && sTry[0].text === WRAP_OLD, 'got=' + (sTry[0] && sTry[0].text));
  const bNone = buildFrame({}, 'wrap');
  const sNone = segSteps(bNone, 'wrapecho:chai_zanhoi');
  ok('C 未揀 Beat 5 → wrap 句係舊 wrap 句（預設）', sNone.length === 1 && sNone[0].text === WRAP_OLD, 'got=' + (sNone[0] && sNone[0].text));
  const bBoth = buildFrame({ chai_try_new: 1, chai_play_safe: 1 }, 'wrap');
  const sBoth = segSteps(bBoth, 'wrapecho:chai_zanhoi');
  ok('C 兩旗齊有（防禦）→ wrap 句係 wrap_safe（play_safe 優先）', sBoth.length === 1 && sBoth[0].text === WRAP_SAFE);
  const bNoEcho = buildFrame({ chai_play_safe: 1 }, null);
  ok('C wrapEcho 唔係 true → 唔出 wrap 句', segSteps(bNoEcho, 'wrapecho:chai_zanhoi').length === 0);
  ok('C wrap 句播完 → 清 wrapEcho（唔重播）', (() => { playSeg(bSafe, 'wrapecho:chai_zanhoi'); return S.stars.chai_zanhoi.wrapEcho === false; })());
})();

/* ---------- (D) 暖／冷／finale 唔受影響 ---------- */
(function(){
  // 暖版 heart：truth_change → 播暖版 heart（v20a318：try_new 唔再係必要條件）
  resetS(200); _ys = { year: 1990, season: '春' };
  setFav('chai_zanhoi', 45);
  doneAllBeats('chai_zanhoi');
  S.flags.chai_truth_change = 1;
  const bWarm = enc79BuildScript('chai_zanhoi', false);
  ok('D 暖版齊晒（truth_change）→ 播暖版 heart', segSteps(bWarm, 'heart:chai_zanhoi').length > 0);
  // 冷版 heart：chai_loose_fear → 播 heartCold，唔播暖版 heart
  resetS(201); _ys = { year: 1990, season: '春' };
  setFav('chai_zanhoi', 45);
  doneAllBeats('chai_zanhoi');
  S.flags.chai_loose_fear = 1;
  const bCold = enc79BuildScript('chai_zanhoi', false);
  ok('D 有壞旗（chai_loose_fear）→ 播冷版 heartCold，唔播暖版 heart',
    segSteps(bCold, 'heartCold:chai_zanhoi').length > 0 && segSteps(bCold, 'heart:chai_zanhoi').length === 0);
  // finale 尾句分流照舊（v305 回歸）
  function buildWarmFinale(flags){
    resetS(950); _ys = { year: 1992, season: '冬' };
    setFav('chai_zanhoi', 70);
    const st = doneExcept('chai_zanhoi', ['chai_finale']);
    st.heartDone = true;
    Object.assign(S.flags, flags || {});
    return enc79BuildScript('chai_zanhoi', false);
  }
  const bTry = buildWarmFinale({ chai_try_new: 1 });
  const lastTry = segSteps(bTry, 'beat:chai_finale');
  ok('D finale try_new → 尾句照舊係 wrap 句（唔同 FRAME cap／wrap 打架）',
    lastTry.length === 6 && lastTry[5].text === WRAP_OLD, 'last=' + (lastTry[5] && lastTry[5].text));
  const bSafe = buildWarmFinale({ chai_play_safe: 1 });
  const lastSafe = segSteps(bSafe, 'beat:chai_finale');
  ok('D finale play_safe → 尾句照舊係 cap 句',
    lastSafe.length === 6 && lastSafe[5].text === CAP_OLD, 'last=' + (lastSafe[5] && lastSafe[5].text));
})();

/* ---------- (E) 舊檔 ---------- */
(function(){
  resetS(300); _ys = { year: 1992, season: '冬' };
  setFav('chai_zanhoi', 70);
  const st = doneAllBeats('chai_zanhoi');
  st.heartDone = true; st.capHit = true; st.wrapEcho = true;
  let b = null, err = null;
  try{ b = enc79BuildScript('chai_zanhoi', false); }catch(e){ err = e; }
  ok('E 舊檔（無 Beat 5 旗、fav 70、1992 冬）→ 唔 crash', !err && !!b, err && String(err));
  ok('E 舊檔 → cap 句係舊 cap 句', b && segSteps(b, 'cap:chai_zanhoi').length === 1 && segSteps(b, 'cap:chai_zanhoi')[0].text === CAP_OLD);
  ok('E 舊檔 → wrap 句係舊 wrap 句', b && segSteps(b, 'wrapecho:chai_zanhoi').length === 1 && segSteps(b, 'wrapecho:chai_zanhoi')[0].text === WRAP_OLD);
})();

/* ---------- (F) 靜態 ---------- */
ok('F 其他星 cap／wrap 唔郁（陸 cap 句在位）',
  ENC79_CAP_LINES.luk_baakyin && ENC79_CAP_LINES.luk_baakyin[1] === '等你擔正嗰日，我哋再慢慢傾。' &&
  ENC79_WRAP_ECHO.luk_baakyin && ENC79_WRAP_ECHO.luk_baakyin[1] === '上次嗰套戲，你嗰場做得唔錯。導演有提起你。');
ok('F chai_try_new 授出點唯一（Beat 5 抉擇 flags 1 處＋讀取 1 處：cap 分流；v20a318 之後 280 獎勵讀法唔再讀 try_new）',
  (html.match(/chai_try_new/g) || []).length === 2, 'count=' + (html.match(/chai_try_new/g) || []).length);
ok('F chai_play_safe 授出點唯一（Beat 5 抉擇 flags 1 處＋讀取 2 處：finale、wrap 分流）',
  (html.match(/chai_play_safe/g) || []).length === 3, 'count=' + (html.match(/chai_play_safe/g) || []).length);
ok('F v305 finale 機制唔郁（chai_finale 6 句＋play_safe 換尾句在位）',
  html.indexOf('id:"chai_finale"') >= 0 && html.indexOf('if(beat.id==="chai_finale" && (S.flags||{}).chai_play_safe') >= 0);
ok('F chai_finale 對白唔郁（6 句、尾句＝wrap 句）',
  (() => {
    const D = ENC79_DIALOG.chai_zanhoi;
    const fin = D && D.beats && D.beats.chai_finale;
    return !!fin && fin.lines.length === 6 && fin.lines[5][1] === WRAP_OLD;
  })());
ok('F 提攜冷版唔郁（chai_patron_cold 對白＋閘在位）',
  html.indexOf('id:"chai_patron_cold"') >= 0 && html.indexOf('chai_loose_fear') >= 0);
const gigsLib = GIGS_ARR;
ok('F gigs_new.json 仍係 323 張', gigsLib.length === 323, 'count=' + gigsLib.length);

if(fails.length){ console.log('FAILURES: ' + fails.join(', ')); process.exit(1); }
console.log('ALL PASS');
