// v20a356 resync：支線複檢 (a) 類修復改咗 ENC 釘句（齊 wrap／駱 patron_cold／彭 finale_cold＋n17／程 e4／魏 heartCold／駱 heart label／彭 intel label／齊 choice GRANT key），釘句同步更新，邏輯斷言唔郁。
// v20a318 齊鎮海 patron 閘同收尾獎勵按草稿對齊測試：
//   (A) 靜態：暖版閘要 T4＋truth_change＋三排除（silent／comfort／loose_fear）；冷版閘一行唔郁；
//       grants（credit_enc83_chai_patron＋sideline280GrantCompletion("chai")）唔郁；280 齊線讀法 truth_change only；
//       registry 次序 patron_cold＜patron＜finale
//   (B) when() 直接判定：提攜閘矩陣（truth_change 有／無 × 三壞旗）——穩陣玩家攞到提攜；
//       silent＋truth_change 仍係冷（草稿 L1182）；無 truth_change 唔播暖版，無論有無 try_new
//   (C) 獎勵讀法矩陣：truth_change only——play_safe 有獎；try_new 單獨／comfort／silent／loose_fear／無旗無獎
//   (D) 次序＋補派：無 heart 嘅 T4 玩家攞唔到提攜，播完 heart 揀真話之後即刻攞到；
//       三個補派點（heart／repay／patron）邊個後到邊個派獎、唔重派
//   (E) 舊檔：已有 beatsDone.chai_patron 但無 truth_change → finale 照播；已有 sideline280_chai → 唔重派
//   (S) 靜態：heart／fear／choice／repay 閘、GRANT229 即派、wrap_safe／cap_try／finale 尾句變體、gigs 306 張
// 用法：node tests/test_r318_chai_patron_truth.js [path-to-index.html]
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

/* ---- sandbox（跟 test_r311_ching_patron_strict.js） ---- */
let S;
let _ys = { year: 1992, season: '冬' };
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
const consts318 = ['ENC79_PLAYER_TIERS', 'ENC79_FAV_CAPS', 'ENC79_WEEK_SOFT_CAP', 'ENC79_STARS', 'ENC79_PILOT', 'ENC79_STAGEUP', 'ENC79_CAP_LINES', 'ENC79_WRAP_ECHO', 'ENC79_BEATS', 'ENC79_DIALOG', 'ENC79_FIRST_ALT98'].map(n => asVar(extractConst(n), n)).join('\n')
  + '\n' + asVar(extractDlg('ENC83_DLG_chai_zanhoi'), 'ENC83_DLG_chai_zanhoi')
  + '\nENC79_DIALOG["chai_zanhoi"] = ENC83_DLG_chai_zanhoi;';
const p2Start = html.indexOf('/* ---------- Phase 2 四星鏈節拍');
const p2End = html.indexOf('/* ===== ENC83 模組完 =====', p2Start);
if(p2Start < 0 || p2End < 0) throw new Error('Phase 2 beats region not found');
const p2Region = html.slice(p2Start, p2End);
const fns318 = ['enc79StarDef', 'enc79Hash', 'enc79Rand', 'enc79EnsureStars', 'enc79StarState', 'enc79TierOf', 'enc79PlayerTier', 'enc79FavCap', 'enc79AddFav', 'enc79WhisperActive', 'enc79GrantWhisper', 'enc79GrantCredit', 'enc79BoardHasStar', 'enc79BoardHasActionGig', 'enc79BeatOpen', 'enc79AnyBeatOpen', 'enc79PickBeat', 'enc79NormSeg', 'enc79BuildScript', 'enc79ChoiceFx', 'enc83NodeDone', 'enc83Flag', 'enc83HasCredit', 'enc83NewsOut', 'contra98EncFirstLocSwap', 'sideline280GrantCompletion', 'grant229Ensure', 'grant229GigById', 'grant229Record', 'grant229RecordFromEnc79'];
eval(consts318 + '\n' + asVar(extractConst('GRANT229_ENC79'), 'GRANT229_ENC79') + '\n' + p2Region + '\n' + fns318.map(extractFn).join('\n'));

/* ---- helpers ---- */
const WARM = beatOf('chai_zanhoi', 'chai_patron');
const COLD = beatOf('chai_zanhoi', 'chai_patron_cold');
const REPAY = beatOf('chai_zanhoi', 'chai_repay');
const FINALE = beatOf('chai_zanhoi', 'chai_finale');
function hasSeg(script, seg){ return ((script && script.steps) || []).some(s => s.seg === seg); }
function buildPatron(flags, fav){
  resetS(950); _ys = { year: 1992, season: '冬' };
  setFav('chai_zanhoi', fav === undefined ? 70 : fav);
  const st = metStar('chai_zanhoi');
  for(const b of (ENC79_BEATS.chai_zanhoi || [])) if(b.id !== 'chai_patron' && b.id !== 'chai_patron_cold') st.beatsDone[b.id] = 1;
  Object.assign(S.flags, flags || {});
  return enc79BuildScript('chai_zanhoi', false);
}
function buildHeart(flags){
  resetS(950); _ys = { year: 1991, season: '夏' };
  setFav('chai_zanhoi', 45);
  const st = doneAllBeats('chai_zanhoi');
  st.heartDone = false;
  Object.assign(S.flags, flags || {});
  return enc79BuildScript('chai_zanhoi', false);
}
function playHeartCallback(script){
  const hs = ((script && script.steps) || []).filter(s => s.seg === 'heart:chai_zanhoi');
  if(!hs.length) return false;
  const last = hs[hs.length - 1];
  if(typeof last.segFx !== 'function') return false;
  last.segFx();
  return true;
}

/* ---------- (A) 靜態：閘字串＋grants＋280 讀法＋次序 ---------- */
ok('A 暖版閘要 truth_change（草稿 L1110 引薦閘）', !!WARM && WARM.when.toString().indexOf('chai_truth_change') >= 0);
ok('A 暖版閘仍要 T4（enc79TierOf(st.fav)>=4）', !!WARM && WARM.when.toString().indexOf('enc79TierOf(st.fav)>=4') >= 0);
ok('A 暖版閘保留三排除（silent／comfort／loose_fear）', !!WARM &&
  WARM.when.toString().indexOf('chai_silent') >= 0 &&
  WARM.when.toString().indexOf('chai_comfort') >= 0 &&
  WARM.when.toString().indexOf('chai_loose_fear') >= 0);
ok('A 暖版閘唔讀 try_new（唔係兩旗齊備，草稿反對）', !!WARM && WARM.when.toString().indexOf('chai_try_new') < 0);
ok('A 冷版閘一行唔郁（T4＋silent／comfort／loose_fear 任一）', !!COLD &&
  COLD.when.toString().indexOf('enc79TierOf(st.fav)>=4') >= 0 &&
  COLD.when.toString().indexOf('chai_silent') >= 0 &&
  COLD.when.toString().indexOf('chai_comfort') >= 0 &&
  COLD.when.toString().indexOf('chai_loose_fear') >= 0 &&
  COLD.when.toString().indexOf('chai_truth_change') < 0);
ok('A grants 唔郁（credit_enc83_chai_patron＋sideline280GrantCompletion("chai")）', !!WARM &&
  WARM.grants.toString().indexOf('credit_enc83_chai_patron') >= 0 &&
  WARM.grants.toString().indexOf('sideline280GrantCompletion("chai")') >= 0);
ok('A 280 齊線讀法 truth_change only（唔再讀 try_new）',
  html.indexOf('lineKey==="chai") warm = !!(F.chai_truth_change);') >= 0 &&
  html.indexOf('lineKey==="chai") warm = !!(F.chai_truth_change) && !!(F.chai_try_new)') < 0);
ok('A registry 次序唔郁（patron_cold＜patron＜finale，冷版排暖版前）',
  (() => {
    const ids = (ENC79_BEATS.chai_zanhoi || []).map(b => b.id);
    return ids.indexOf('chai_patron_cold') < ids.indexOf('chai_patron') &&
      ids.indexOf('chai_patron') < ids.indexOf('chai_finale');
  })());
const D = ENC79_DIALOG.chai_zanhoi;
ok('A patron 對白唔郁（7 句，首句逐字）', !!D && !!D.beats && !!D.beats.chai_patron &&
  D.beats.chai_patron.lines.length === 7 &&
  D.beats.chai_patron.lines[0][1] === '阿偉，你最近嗰幾場戲，我有睇返，進步唔係扮出嚟嗰種，係企得穩咗。');
ok('A patron_cold 對白唔郁', !!D && !!D.beats && !!D.beats.chai_patron_cold &&
  D.beats.chai_patron_cold.lines.length >= 1);

/* ---------- (B) when() 直接判定：提攜閘矩陣 ---------- */
ok('B truth_change＋T4 → 暖版閘開', (() => { resetS(950); S.flags.chai_truth_change = 1; return WARM.when({ fav: 70 }) === true; })());
ok('B truth_change＋try_new → 暖版閘開（試新角嗰邊）', (() => { resetS(950); S.flags.chai_truth_change = 1; S.flags.chai_try_new = 1; return WARM.when({ fav: 70 }) === true; })());
ok('B truth_change＋play_safe → 暖版閘開（穩陣玩家攞到提攜，唔會失去債權＋film_206＋finale）', (() => { resetS(950); S.flags.chai_truth_change = 1; S.flags.chai_play_safe = 1; return WARM.when({ fav: 70 }) === true; })());
ok('B 無 truth_change（得 try_new）→ 暖版閘閂（舊制會放行）', (() => { resetS(950); S.flags.chai_try_new = 1; return WARM.when({ fav: 70 }) === false; })());
ok('B 無 truth_change（乜旗都無）→ 暖版閘閂', (() => { resetS(950); return WARM.when({ fav: 70 }) === false; })());
ok('B truth_change＋silent → 暖版閘閂、冷版閘開（草稿 L1182：silent 係冷）', (() => { resetS(950); S.flags.chai_truth_change = 1; S.flags.chai_silent = 1; return WARM.when({ fav: 70 }) === false && !!COLD.when({ fav: 70 }); })());
ok('B truth_change＋comfort → 暖版閘閂、冷版閘開', (() => { resetS(950); S.flags.chai_truth_change = 1; S.flags.chai_comfort = 1; return WARM.when({ fav: 70 }) === false && !!COLD.when({ fav: 70 }); })());
ok('B truth_change＋loose_fear → 暖版閘閂、冷版閘開', (() => { resetS(950); S.flags.chai_truth_change = 1; S.flags.chai_loose_fear = 1; return WARM.when({ fav: 70 }) === false && !!COLD.when({ fav: 70 }); })());
ok('B T3（fav 69）truth_change 齊 → 暖版閘閂', (() => { resetS(950); S.flags.chai_truth_change = 1; return WARM.when({ fav: 69 }) === false; })());

/* ---------- (C) 獎勵讀法矩陣 ---------- */
function grantResult(flags){
  resetS(950);
  Object.assign(S.flags, flags || {});
  const r = sideline280GrantCompletion('chai');
  return { r, fame: S.fame, delta: S.industryCreditDelta, done: S.flags.sideline280_chai };
}
ok('C truth_change only → 派收尾獎勵（fame＋2／delta＋1／doneKey）', (() => { const g = grantResult({ chai_truth_change: 1 }); return g.r === true && g.fame === 32 && g.delta === 1 && g.done === 1; })());
ok('C truth_change＋play_safe → 派（穩陣玩家賺返收尾獎勵）', (() => { const g = grantResult({ chai_truth_change: 1, chai_play_safe: 1 }); return g.r === true && g.fame === 32 && g.delta === 1; })());
ok('C truth_change＋try_new → 派', (() => { const g = grantResult({ chai_truth_change: 1, chai_try_new: 1 }); return g.r === true && g.fame === 32; })());
ok('C try_new 單獨 → 唔派', (() => { const g = grantResult({ chai_try_new: 1 }); return g.r === false && g.fame === 30 && !g.done; })());
ok('C play_safe 單獨 → 唔派', (() => { const g = grantResult({ chai_play_safe: 1 }); return g.r === false && g.fame === 30; })());
ok('C comfort 單獨 → 唔派', (() => { const g = grantResult({ chai_comfort: 1 }); return g.r === false && g.fame === 30; })());
ok('C silent 單獨 → 唔派', (() => { const g = grantResult({ chai_silent: 1 }); return g.r === false && g.fame === 30; })());
ok('C loose_fear 單獨 → 唔派', (() => { const g = grantResult({ chai_loose_fear: 1 }); return g.r === false && g.fame === 30; })());
ok('C 無 heart（乜旗都無）→ 唔派', (() => { const g = grantResult({}); return g.r === false && g.fame === 30; })());

/* ---------- (D) 次序＋補派 ---------- */
ok('D 無 heart 嘅 T4 玩家 → buildScript 唔播 beat:chai_patron', !hasSeg(buildPatron({}, 70), 'beat:chai_patron'));
ok('D 播完 heart 揀真話之後 → buildScript 即刻播 beat:chai_patron', hasSeg(buildPatron({ chai_truth_change: 1 }, 70), 'beat:chai_patron'));
ok('D 遲補 truth_change 即播（漏做趕得切，唔死局）', (() => {
  const b1 = buildPatron({}, 70);
  if(hasSeg(b1, 'beat:chai_patron')) return false;
  S.flags.chai_truth_change = 1;
  const b2 = enc79BuildScript('chai_zanhoi', false);
  return hasSeg(b2, 'beat:chai_patron') && !S.stars.chai_zanhoi.beatsDone.chai_patron;
})());
ok('D 補派點 heart：講真話後撳 heart 回調 → 派獎；無真話 → 唔派', (() => {
  const b1 = buildHeart({ chai_truth_change: 1 });
  if(!playHeartCallback(b1)) return false;
  const paid = S.fame === 32 && S.industryCreditDelta === 1 && S.flags.sideline280_chai === 1;
  const b2 = buildHeart({});
  if(!playHeartCallback(b2)) return false;
  return paid && S.fame === 30 && !S.flags.sideline280_chai;
})());
ok('D 補派點：patron 先派 → repay 唔重派', (() => {
  resetS(950); setFav('chai_zanhoi', 70); metStar('chai_zanhoi');
  S.flags.chai_truth_change = 1;
  WARM.grants();
  const afterPatron = S.fame === 32 && S.industryCreditDelta === 1;
  REPAY.grants();
  return afterPatron && S.fame === 32 && S.industryCreditDelta === 1;
})());
ok('D 補派點：repay 先派 → patron 唔重派', (() => {
  resetS(950); setFav('chai_zanhoi', 70); metStar('chai_zanhoi');
  S.flags.chai_truth_change = 1;
  REPAY.grants();
  const afterRepay = S.fame === 32 && S.industryCreditDelta === 1;
  WARM.grants();
  return afterRepay && S.fame === 32 && S.industryCreditDelta === 1 && enc83HasCredit('credit_enc83_chai_patron') === true;
})());

/* ---------- (E) 舊檔 ---------- */
ok('E 舊檔：已有 beatsDone.chai_patron 但無 truth_change → finale 照播（finale 閘唔讀 truth_change）', (() => {
  resetS(950); _ys = { year: 1992, season: '冬' };
  setFav('chai_zanhoi', 70);
  const st = metStar('chai_zanhoi');
  for(const b of (ENC79_BEATS.chai_zanhoi || [])) if(b.id !== 'chai_finale') st.beatsDone[b.id] = 1;
  st.heartDone = true;
  const b = enc79BuildScript('chai_zanhoi', false);
  return hasSeg(b, 'beat:chai_finale') && ((b.steps || []).filter(s => s.seg === 'beat:chai_finale').length === 6);
})());
ok('E 舊檔：已有 sideline280_chai → 唔重派', (() => {
  resetS(950);
  S.flags.chai_truth_change = 1; S.flags.sideline280_chai = 1;
  const r = sideline280GrantCompletion('chai');
  return r === false && S.fame === 30 && S.industryCreditDelta === 0;
})());
ok('E 舊檔（無 Beat 5 旗、fav 70、1992 冬）→ 唔 crash', (() => {
  resetS(950); _ys = { year: 1992, season: '冬' };
  setFav('chai_zanhoi', 70);
  const st = metStar('chai_zanhoi');
  for(const b of (ENC79_BEATS.chai_zanhoi || [])) st.beatsDone[b.id] = 1;
  st.heartDone = true;
  let b = null, err = null;
  try{ b = enc79BuildScript('chai_zanhoi', false); }catch(e){ err = e; }
  return !err && !!b;
})());

/* ---------- (S) 靜態 guard ---------- */
ok('S heart 閘唔郁（T3＋loose_fear 排除，無年份窗、唔要 kept_fear）',
  html.indexOf('!(starId==="chai_zanhoi" && (S.flags||{}).chai_loose_fear)') >= 0);
ok('S fear 閘唔郁（T1–T2＋1990–91 年窗＋N3）',
  html.indexOf('id:"chai_fear", when(st){ const ys=yearSeasonNow(); return enc79TierOf(st.fav)>=1 && enc79TierOf(st.fav)<=2 && ys.year>=1990 && ys.year<=1991 && enc83NodeDone("N3")') >= 0);
ok('S choice 閘已放寬（1991–1992＋T2，v321：草稿 L993「T2＋1991 年」、choice 在 N13 之前）',
  html.indexOf('id:"chai_choice", when(st){ const ys=yearSeasonNow(); return ys.year>=1991 && ys.year<=1992 && enc79TierOf(st.fav)>=2; }') >= 0);
ok('S repay 閘唔郁（T2＋＋!silent＋side 旗或 N13）',
  html.indexOf('id:"chai_repay", when(st){ return enc79TierOf(st.fav)>=2 && !(S.flags||{}).chai_silent') >= 0);
ok('S finale 閘唔郁（T4＋1992 冬＋patron 已播＋同一組排除條件）',
  !!FINALE && FINALE.when.toString().indexOf('1992') >= 0 &&
  FINALE.when.toString().indexOf('chai_patron') >= 0 &&
  FINALE.when.toString().indexOf('chai_silent') >= 0);
ok('S GRANT229 即派唔郁（fear 守口→tv_111、choice 勸停→tv_114、choice 婉拒畀意見→tv_207、repay 唔同→tv_111、repay 穩陣→tv_112）',
  html.indexOf('seg:"beat:chai_fear", key:"守口", gigId:"gig_1991_tv_111"') >= 0 &&
  html.indexOf('seg:"beat:chai_choice", key:"停一停", gigId:"gig_1991_tv_114"') >= 0 &&
  html.indexOf('seg:"beat:chai_choice", key:"婉拒畀意見", gigId:"gig_1991_tv_207"') >= 0 &&
  html.indexOf('seg:"beat:chai_repay", key:"唔同", gigId:"gig_1992_tv_111"') >= 0 &&
  html.indexOf('seg:"beat:chai_repay", key:"穩陣", gigId:"gig_1992_tv_112"') >= 0);
ok('S wrap_safe／cap_try／finale 尾句變體唔郁',
  html.indexOf('cap_try: ["S", "阿偉，你肯試新嘢，呢份膽色我認。') >= 0 &&
  html.indexOf('wrap_safe: ["S", "行到今日，你企嘅位唔同晒喇。呢套戲你企得穩，冇浮冇躁，已經好難得。') >= 0 &&
  html.indexOf('if(beat.id==="chai_finale" && (S.flags||{}).chai_play_safe') >= 0);
ok('S gigs_new.json 仍係 323 張', GIGS_ARR.length === 323, 'count=' + GIGS_ARR.length);
ok('S 回響通告 trigger 唔郁（tv_114＋film_206 全部係 credit_enc83_chai_patron）',
  (() => {
    const byId = id => GIGS_ARR.find(g => g.id === id || g.gigId === id);
    const t = byId('gig_1991_tv_114'), f = byId('gig_1992_film_206');
    return !!t && !!f && t.trigger && t.trigger.creditId === 'credit_enc83_chai_patron' &&
      f.trigger && f.trigger.creditId === 'credit_enc83_chai_patron';
  })());

if(fails.length){ console.log('FAILURES: ' + fails.join(' | ')); process.exit(1); }
console.log('ALL PASS r318');
