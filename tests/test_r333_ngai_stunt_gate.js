// v20a333 B2 魏腿：ngai_walk_past 玩家要先做埋任何一張「動作替身」通告先開暖版交心：
//   (A) walk_past＋無替身殺青 → 暖版 heart 唔開；做過 film_206 → 開；做過 film_201（淨體能）→ 開（唔係淨認 film_206）；
//       做過非替身通告（tv_205 群演）→ 唔開；無 walk_past 旗 → 照開（唔受影響）
//   (B) 冷版 heart 閘唔郁：hold_back 玩家照播冷版（唔係暖版）
//   (C) 提攜閘唔郁：ngai_patron 不受 walk_past 影響
//   (D) helper 單元：enc79HasDoneStuntDouble() 只認 roleLabel「動作替身」＋done_ 旗
//   (E) 靜態：暖版閘行有新條件；ngai_walk_past 授出 1 處＋讀者 1 處；gig_br89_stunt_ngai 全 repo 0 命中
// 用法：node tests/test_r333_ngai_stunt_gate.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
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

/* ---- sandbox（跟 test_r328_heart_gate_a4.js；加魏 DLG） ---- */
let S;
let _ys = { year: 1992, season: '冬' };
let _doneNodes = new Set();
function resetS(day){
  S = { dayIndex: day || 0, fame: 30, money: 2000, flags: {}, npcs: { agent: 0 }, mockRumors: [], mockDebts: [], mockCredits: [], board: {}, shoots: {}, mapTips: {}, story: { flags: {} }, starWeek: {}, starFavWeek: { week: -1, gain: 0 }, weekGigsDone: 0, starWhispers: {}, grant229Queue: [], pendingAud: [], news82: { pub: {}, arc: {} }, industryCreditDelta: 0 };
  _doneNodes = new Set();
  _ledger = null;
}
function setFav(sid, n){ enc79EnsureStars(); S.stars[sid].fav = n; }
function metStar(sid){ enc79EnsureStars(); S.stars[sid].met = true; S.stars[sid].stage = 3; return S.stars[sid]; }
function doneAllBeats(sid){ const st = metStar(sid); for(const b of (ENC79_BEATS[sid]||[])) st.beatsDone[b.id] = 1; return st; }
function beatOf(sid, id){ return (ENC79_BEATS[sid] || []).find(b => b.id === id); }
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
const consts333 = ['ENC79_PLAYER_TIERS', 'ENC79_FAV_CAPS', 'ENC79_WEEK_SOFT_CAP', 'ENC79_STARS', 'ENC79_PILOT', 'ENC79_STAGEUP', 'ENC79_CAP_LINES', 'ENC79_WRAP_ECHO', 'ENC79_BEATS', 'ENC79_DIALOG', 'ENC79_FIRST_ALT98'].map(n => asVar(extractConst(n), n)).join('\n')
  + '\n' + ['ENC83_DLG_ngai_wingnaam'].map(n => asVar(extractDlg(n), n)).join('\n')
  + '\nENC79_DIALOG["ngai_wingnaam"] = ENC83_DLG_ngai_wingnaam;';
const p2Start = html.indexOf('/* ---------- Phase 2 四星鏈節拍');
const p2End = html.indexOf('/* ===== ENC83 模組完 =====', p2Start);
if(p2Start < 0 || p2End < 0) throw new Error('Phase 2 beats region not found');
const p2Region = html.slice(p2Start, p2End);
const fns333 = ['enc79StarDef', 'enc79Hash', 'enc79Rand', 'enc79EnsureStars', 'enc79StarState', 'enc79TierOf', 'enc79PlayerTier', 'enc79FavCap', 'enc79AddFav', 'enc79WhisperActive', 'enc79GrantWhisper', 'enc79GrantCredit', 'enc79BoardHasStar', 'enc79BoardHasActionGig', 'enc79BeatOpen', 'enc79HasDoneStuntDouble', 'enc79AnyBeatOpen', 'enc79PickBeat', 'enc79NormSeg', 'enc79BuildScript', 'enc83NodeDone', 'enc83Flag', 'enc83HasCredit', 'enc83NewsOut', 'contra98EncFirstLocSwap', 'sideline280GrantCompletion', 'grant229Ensure', 'grant229GigById', 'grant229Record', 'grant229RecordFromEnc79'];
eval(consts333 + '\n' + asVar(extractConst('GRANT229_ENC79'), 'GRANT229_ENC79') + '\n' + p2Region + '\n' + fns333.map(extractFn).join('\n'));

/* 替身通告 stub（只取 helper 用嘅欄：id＋roleLabel） */
GIGS = [
  { id: 'gig_1990_film_103', roleLabel: '動作替身' },
  { id: 'gig_1991_film_114', roleLabel: '動作替身' },
  { id: 'gig_1991_film_206', roleLabel: '動作替身' },
  { id: 'gig_1992_film_201', roleLabel: '動作替身' },
  { id: 'gig_1991_tv_205', roleLabel: '群演' },
];

/* ---- helpers ---- */
function heartSegs(b, sid){ return (b && b.steps || []).filter(s => s.seg === 'heart:' + sid); }
function coldSegs(b, sid){ return (b && b.steps || []).filter(s => s.seg === 'heartCold:' + sid); }
function build(sid, flags){
  resetS(950); _ys = { year: 1992, season: '冬' };
  setFav(sid, 45);
  const st = doneAllBeats(sid);
  st.heartDone = false;
  Object.assign(S.flags, flags || {});
  return enc79BuildScript(sid, false);
}

/* ---------- (A) walk_past 嗰陣要先做埋替身工 ---------- */
let a1 = build('ngai_wingnaam', { ngai_walk_past: 1 });
ok('A walk_past＋無替身殺青 → 暖版 heart 唔開', heartSegs(a1, 'ngai_wingnaam').length === 0, 'heartSegs=' + heartSegs(a1, 'ngai_wingnaam').length);
let a2 = build('ngai_wingnaam', { ngai_walk_past: 1, done_gig_1991_film_206: 1 });
ok('A walk_past＋做過 film_206 → 暖版 heart 開', heartSegs(a2, 'ngai_wingnaam').length > 0, 'heartSegs=' + heartSegs(a2, 'ngai_wingnaam').length);
let a3 = build('ngai_wingnaam', { ngai_walk_past: 1, done_gig_1992_film_201: 1 });
ok('A walk_past＋做過 film_201（淨體能）→ 暖版 heart 開', heartSegs(a3, 'ngai_wingnaam').length > 0, 'heartSegs=' + heartSegs(a3, 'ngai_wingnaam').length);
let a4 = build('ngai_wingnaam', { ngai_walk_past: 1, done_gig_1991_tv_205: 1 });
ok('A walk_past＋只做過非替身通告（tv_205 群演）→ 暖版 heart 唔開', heartSegs(a4, 'ngai_wingnaam').length === 0, 'heartSegs=' + heartSegs(a4, 'ngai_wingnaam').length);
let a5 = build('ngai_wingnaam', {});
ok('A 無 walk_past 旗、無替身殺青 → 暖版 heart 照開（唔受影響）', heartSegs(a5, 'ngai_wingnaam').length > 0, 'heartSegs=' + heartSegs(a5, 'ngai_wingnaam').length);
ok('A walk_past 做埋嗰陣 heart 句數同無旗一致', heartSegs(a2, 'ngai_wingnaam').length === heartSegs(a5, 'ngai_wingnaam').length,
  'walkpast=' + heartSegs(a2, 'ngai_wingnaam').length + ' plain=' + heartSegs(a5, 'ngai_wingnaam').length);

/* ---------- (B) 冷版 heart 閘唔郁 ---------- */
let b1 = build('ngai_wingnaam', { ngai_rain_hold_back: 1 });
ok('B 壞旗 ngai_rain_hold_back → 冷版 heart 照播', coldSegs(b1, 'ngai_wingnaam').length > 0, 'coldSegs=' + coldSegs(b1, 'ngai_wingnaam').length);
ok('B 壞旗 ngai_rain_hold_back → 暖版 heart 唔播', heartSegs(b1, 'ngai_wingnaam').length === 0);
let b2 = build('ngai_wingnaam', { ngai_rain_hold_back: 1, ngai_walk_past: 1, done_gig_1991_film_206: 1 });
ok('B 壞旗＋walk_past＋做過替身 → 照播冷版（唔係暖版）', coldSegs(b2, 'ngai_wingnaam').length > 0 && heartSegs(b2, 'ngai_wingnaam').length === 0,
  'coldSegs=' + coldSegs(b2, 'ngai_wingnaam').length + ' heartSegs=' + heartSegs(b2, 'ngai_wingnaam').length);

/* ---------- (C) 提攜閘唔郁 ---------- */
function patronWhen(sid, beatId, fav, flags){
  resetS(950); _ys = { year: 1992, season: '冬' };
  setFav(sid, fav);
  Object.assign(S.flags, flags || {});
  return beatOf(sid, beatId).when(enc79StarState(sid));
}
ok('C ngai_patron：T4 → 開', patronWhen('ngai_wingnaam', 'ngai_patron', 70, {}) === true);
ok('C ngai_patron：T4＋walk_past → 照開（walk_past 唔影響提攜）', patronWhen('ngai_wingnaam', 'ngai_patron', 70, { ngai_walk_past: 1 }) === true);
ok('C ngai_patron：T4＋walk_past＋做過替身 → 照開', patronWhen('ngai_wingnaam', 'ngai_patron', 70, { ngai_walk_past: 1, done_gig_1991_film_206: 1 }) === true);
ok('C ngai_patron：T3 → 唔開', patronWhen('ngai_wingnaam', 'ngai_patron', 45, {}) === false);

/* ---------- (D) helper 單元 ---------- */
resetS(950);
ok('D helper：無 done_ 旗 → false', enc79HasDoneStuntDouble() === false);
S.flags.done_gig_1991_tv_205 = 1;
ok('D helper：只做過非替身通告 → false', enc79HasDoneStuntDouble() === false);
S.flags.done_gig_1991_film_114 = 1;
ok('D helper：做過 film_114（替身）→ true', enc79HasDoneStuntDouble() === true);

/* ---------- (E) 靜態 ---------- */
ok('E 暖版閘有 ngai_walk_past＋enc79HasDoneStuntDouble 條件',
  html.indexOf('ngai_walk_past && !enc79HasDoneStuntDouble()') >= 0);
ok('E ngai_walk_past 授出 1 處＋讀者 1 處',
  (html.match(/ngai_walk_past/g) || []).length === 2, 'hits=' + (html.match(/ngai_walk_past/g) || []).length);
ok('E gig_br89_stunt_ngai 全檔 0 命中', html.indexOf('gig_br89_stunt_ngai') < 0);
ok('E helper 定義在位', html.indexOf('function enc79HasDoneStuntDouble()') >= 0);

if(fails.length){ console.log('FAILURES: ' + fails.join(', ')); process.exit(1); }
console.log('ALL PASS');
