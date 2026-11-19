// v20a328 A4 N-5 Beat 4 交心「加多一重閘」（駱＋齊兩腿；魏腿除外，見 B2）：
//   (A) 駱：lok_first_mock 玩家未做 lok_help → 暖版 heart 唔開；做埋 → 開；無旗唔受影響
//   (B) 齊：chai_first_bluff 玩家未做 chai_choice → 暖版 heart 唔開；做埋 → 開；無旗唔受影響
//   (C) 冷版 heart 閘唔郁：壞旗玩家照播冷版（唔係暖版）
//   (D) 提攜閘唔郁：lok_patron／chai_patron when 原封不動（mock／bluff 旗唔影響提攜）
//   (E) 靜態：暖版閘行入面有齊兩個新條件
// 用法：node tests/test_r328_heart_gate_a4.js [path-to-index.html]
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

/* ---- sandbox（跟 test_r308_lok_heart_cover.js；加 chai DLG） ---- */
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
const consts328 = ['ENC79_PLAYER_TIERS', 'ENC79_FAV_CAPS', 'ENC79_WEEK_SOFT_CAP', 'ENC79_STARS', 'ENC79_PILOT', 'ENC79_STAGEUP', 'ENC79_CAP_LINES', 'ENC79_WRAP_ECHO', 'ENC79_BEATS', 'ENC79_DIALOG', 'ENC79_FIRST_ALT98'].map(n => asVar(extractConst(n), n)).join('\n')
  + '\n' + ['ENC83_DLG_lok_gasing', 'ENC83_DLG_chai_zanhoi'].map(n => asVar(extractDlg(n), n)).join('\n')
  + '\nENC79_DIALOG["lok_gasing"] = ENC83_DLG_lok_gasing;\nENC79_DIALOG["chai_zanhoi"] = ENC83_DLG_chai_zanhoi;';
const p2Start = html.indexOf('/* ---------- Phase 2 四星鏈節拍');
const p2End = html.indexOf('/* ===== ENC83 模組完 =====', p2Start);
if(p2Start < 0 || p2End < 0) throw new Error('Phase 2 beats region not found');
const p2Region = html.slice(p2Start, p2End);
const fns328 = ['enc79StarDef', 'enc79Hash', 'enc79Rand', 'enc79EnsureStars', 'enc79StarState', 'enc79TierOf', 'enc79PlayerTier', 'enc79FavCap', 'enc79AddFav', 'enc79WhisperActive', 'enc79GrantWhisper', 'enc79GrantCredit', 'enc79BoardHasStar', 'enc79BoardHasActionGig', 'enc79BeatOpen', 'enc79AnyBeatOpen', 'enc79PickBeat', 'enc79NormSeg', 'enc79BuildScript', 'enc83NodeDone', 'enc83Flag', 'enc83HasCredit', 'enc83NewsOut', 'contra98EncFirstLocSwap', 'sideline280GrantCompletion', 'grant229Ensure', 'grant229GigById', 'grant229Record', 'grant229RecordFromEnc79'];
eval(consts328 + '\n' + asVar(extractConst('GRANT229_ENC79'), 'GRANT229_ENC79') + '\n' + p2Region + '\n' + fns328.map(extractFn).join('\n'));

/* ---- helpers ---- */
function heartSegs(b, sid){ return (b && b.steps || []).filter(s => s.seg === 'heart:' + sid); }
function coldSegs(b, sid){ return (b && b.steps || []).filter(s => s.seg === 'heartCold:' + sid); }
function build(sid, flags, dropBeat, year){
  resetS(950); _ys = { year: year || 1992, season: '冬' };
  setFav(sid, 45);
  const st = doneAllBeats(sid);
  st.heartDone = false;
  if(dropBeat) delete st.beatsDone[dropBeat];
  Object.assign(S.flags, flags || {});
  return enc79BuildScript(sid, false);
}

/* ---------- (A) 駱：lok_first_mock 嗰陣要先做埋 lok_help ---------- */
let a1 = build('lok_gasing', { lok_first_mock: 1 }, 'lok_help');
ok('A mock 未做 lok_help → 暖版 heart 唔開', heartSegs(a1, 'lok_gasing').length === 0, 'heartSegs=' + heartSegs(a1, 'lok_gasing').length);
let a2 = build('lok_gasing', { lok_first_mock: 1 });
ok('A mock 做埋 lok_help → 暖版 heart 開', heartSegs(a2, 'lok_gasing').length > 0, 'heartSegs=' + heartSegs(a2, 'lok_gasing').length);
let a3 = build('lok_gasing', {}, 'lok_help');
ok('A 無旗、未做 lok_help → 暖版 heart 照開（唔受影響）', heartSegs(a3, 'lok_gasing').length > 0, 'heartSegs=' + heartSegs(a3, 'lok_gasing').length);
ok('A mock 做埋嗰陣 heart 句數同無旗一致', heartSegs(a2, 'lok_gasing').length === heartSegs(a3, 'lok_gasing').length,
  'mock=' + heartSegs(a2, 'lok_gasing').length + ' plain=' + heartSegs(a3, 'lok_gasing').length);

/* ---------- (B) 齊：chai_first_bluff 嗰陣要先做埋 chai_choice ---------- */
// 註：chai_choice 嘅 when 係 1991–1992＋T2——year 1992 嗰陣，刪咗 beatsDone 會令嗰 beat 本身開返，
// build 會播 beat 而唔係 heart（唔係閘擋住）。所以「未做嗰步」嗰兩組用 year 1990，等 beat 因年份閂埋，
// 淨返暖版閘決定播唔播 heart；「做埋」嗰組用 year 1992（beat 已做，閘照過）。
let b1 = build('chai_zanhoi', { chai_first_bluff: 1 }, 'chai_choice', 1990);
ok('B bluff 未做 chai_choice → 暖版 heart 唔開', heartSegs(b1, 'chai_zanhoi').length === 0, 'heartSegs=' + heartSegs(b1, 'chai_zanhoi').length);
let b2 = build('chai_zanhoi', { chai_first_bluff: 1 });
ok('B bluff 做埋 chai_choice → 暖版 heart 開', heartSegs(b2, 'chai_zanhoi').length > 0, 'heartSegs=' + heartSegs(b2, 'chai_zanhoi').length);
let b3 = build('chai_zanhoi', {}, 'chai_choice', 1990);
ok('B 無旗、未做 chai_choice → 暖版 heart 照開（唔受影響）', heartSegs(b3, 'chai_zanhoi').length > 0, 'heartSegs=' + heartSegs(b3, 'chai_zanhoi').length);
ok('B bluff 做埋嗰陣 heart 句數同無旗一致', heartSegs(b2, 'chai_zanhoi').length === heartSegs(b3, 'chai_zanhoi').length,
  'bluff=' + heartSegs(b2, 'chai_zanhoi').length + ' plain=' + heartSegs(b3, 'chai_zanhoi').length);

/* ---------- (C) 冷版 heart 閘唔郁 ---------- */
let c1 = build('chai_zanhoi', { chai_loose_fear: 1 });
ok('C 壞旗 chai_loose_fear → 冷版 heart 照播', coldSegs(c1, 'chai_zanhoi').length > 0, 'coldSegs=' + coldSegs(c1, 'chai_zanhoi').length);
ok('C 壞旗 chai_loose_fear → 暖版 heart 唔播', heartSegs(c1, 'chai_zanhoi').length === 0);
let c2 = build('lok_gasing', { lok_loose_row: 1 });
ok('C 壞旗 lok_loose_row → 冷版 heart 照播', coldSegs(c2, 'lok_gasing').length > 0, 'coldSegs=' + coldSegs(c2, 'lok_gasing').length);
ok('C 壞旗 lok_loose_row → 暖版 heart 唔播', heartSegs(c2, 'lok_gasing').length === 0);

/* ---------- (D) 提攜閘唔郁 ---------- */
function patronWhen(sid, beatId, fav, flags){
  resetS(950); _ys = { year: 1992, season: '冬' };
  setFav(sid, fav);
  Object.assign(S.flags, flags || {});
  return beatOf(sid, beatId).when(enc79StarState(sid));
}
ok('D lok_patron：T4＋calm_truth → 開', patronWhen('lok_gasing', 'lok_patron', 70, { lok_calm_truth: 1 }) === true);
ok('D lok_patron：T4＋calm_truth＋mock 旗 → 照開（mock 唔影響提攜）', patronWhen('lok_gasing', 'lok_patron', 70, { lok_calm_truth: 1, lok_first_mock: 1 }) === true);
ok('D lok_patron：無 calm_truth → 唔開', patronWhen('lok_gasing', 'lok_patron', 70, {}) === false);
ok('D chai_patron：T4＋truth_change → 開', patronWhen('chai_zanhoi', 'chai_patron', 70, { chai_truth_change: 1 }) === true);
ok('D chai_patron：T4＋truth_change＋bluff 旗 → 照開（bluff 唔影響提攜）', patronWhen('chai_zanhoi', 'chai_patron', 70, { chai_truth_change: 1, chai_first_bluff: 1 }) === true);
ok('D chai_patron：無 truth_change → 唔開', patronWhen('chai_zanhoi', 'chai_patron', 70, {}) === false);

/* ---------- (E) 靜態：暖版閘行有齊兩個新條件 ---------- */
ok('E 暖版閘有 lok_first_mock＋lok_help 條件',
  html.indexOf('lok_first_mock && !(st.beatsDone||{}).lok_help') >= 0);
ok('E 暖版閘有 chai_first_bluff＋chai_choice 條件',
  html.indexOf('chai_first_bluff && !(st.beatsDone||{}).chai_choice') >= 0);

if(fails.length){ console.log('FAILURES: ' + fails.join(', ')); process.exit(1); }
console.log('ALL PASS');
