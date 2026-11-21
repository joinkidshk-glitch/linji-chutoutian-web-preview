// v20a356 resync：支線複檢 (a) 類修復改咗 ENC 釘句（齊 wrap／駱 patron_cold／彭 finale_cold＋n17／程 e4／魏 heartCold／駱 heart label／彭 intel label／齊 choice GRANT key），釘句同步更新，邏輯斷言唔郁。
// v20a304 Q17 駱／魏／齊冷版 heart 交心測試：
//   (A) 數據：三線各有 heartCold（7 句、無 choices），對白承接各自裂痕、唔抄暖版句；旁白書面語
//   (B) 分流：有壞旗 → 播 heartCold、唔播暖版 heart／pool；無壞旗 → 播暖版 heart、唔播 heartCold
//   (C) 獨立：冷版 heart 同提攜冷版係兩個獨立 beat；播完冷版 heart 之後 T4 提攜冷版照去得到（唔死局）
//   (D) 播完：heartDone 照標（唔重播）；好感＋1（唔係暖版＋2）；唔派暖版收尾獎勵（sideline280／聲望唔郁）
//   (E) GRANT229：冷版無 choices、seg "heartCold:…" 無對應行，唔派即派通告
//   (F) 舊檔：已有壞旗、未播 heart、star state 只有 fav／met，唔 crash，照播冷版
//   (S) 靜態：暖版 heart 閘／暖版對白／patron_cold 對白／鍾冷版唔郁；gigs_new.json 仍係 330 張
// 用法：node tests/test_r304_cold_heart.js [path-to-index.html]
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

/* ---- sandbox（跟 test_sideline278_logic.js；只抽 Q17 需要嘅部分） ---- */
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
var GIGS = [];

const asVar = (code, name) => code.replace('const ' + name + ' =', 'var ' + name + ' =');
const consts304 = ['ENC79_PLAYER_TIERS', 'ENC79_FAV_CAPS', 'ENC79_WEEK_SOFT_CAP', 'ENC79_STARS', 'ENC79_PILOT', 'ENC79_STAGEUP', 'ENC79_CAP_LINES', 'ENC79_WRAP_ECHO', 'ENC79_BEATS', 'ENC79_DIALOG', 'ENC79_FIRST_ALT98'].map(n => asVar(extractConst(n), n)).join('\n')
  + '\n' + ['ENC83_DLG_lok_gasing', 'ENC83_DLG_ngai_wingnaam', 'ENC83_DLG_chai_zanhoi'].map(n => asVar(extractDlg(n), n)).join('\n')
  + '\nENC79_DIALOG["lok_gasing"] = ENC83_DLG_lok_gasing;\nENC79_DIALOG["ngai_wingnaam"] = ENC83_DLG_ngai_wingnaam;\nENC79_DIALOG["chai_zanhoi"] = ENC83_DLG_chai_zanhoi;';
const p2Start = html.indexOf('/* ---------- Phase 2 四星鏈節拍');
const p2End = html.indexOf('/* ===== ENC83 模組完 =====', p2Start);
if(p2Start < 0 || p2End < 0) throw new Error('Phase 2 beats region not found');
const p2Region = html.slice(p2Start, p2End);
const fns304 = ['enc79StarDef', 'enc79Hash', 'enc79Rand', 'enc79EnsureStars', 'enc79StarState', 'enc79TierOf', 'enc79PlayerTier', 'enc79FavCap', 'enc79AddFav', 'enc79WhisperActive', 'enc79GrantWhisper', 'enc79GrantCredit', 'enc79BoardHasStar', 'enc79BoardHasActionGig', 'enc79BeatOpen', 'enc79AnyBeatOpen', 'enc79PickBeat', 'enc79NormSeg', 'enc79BuildScript', 'enc83NodeDone', 'enc83Flag', 'enc83HasCredit', 'enc83NewsOut', 'contra98EncFirstLocSwap', 'sideline280GrantCompletion', 'grant229Ensure', 'grant229GigById', 'grant229Record', 'grant229RecordFromEnc79'];
eval(consts304 + '\n' + asVar(extractConst('GRANT229_ENC79'), 'GRANT229_ENC79') + '\n' + p2Region + '\n' + fns304.map(extractFn).join('\n'));

/* ---- helpers ---- */
function hasText(b, sub){ return (b && b.steps || []).some(s => String(s.text || '').indexOf(sub) >= 0); }
function segSteps(b, seg){ return (b && b.steps || []).filter(s => s.seg === seg); }
function playSeg(b, seg){ segSteps(b, seg).forEach(s => { try{ if(typeof s.segFx === 'function') s.segFx(); }catch(_e){} }); }
const CASES = [
  { sid: 'lok_gasing', bad: 'lok_loose_row', coldFlag: 'lok_heart_cold', line: 'lok' },
  { sid: 'ngai_wingnaam', bad: 'ngai_rain_hold_back', coldFlag: 'ngai_heart_cold', line: 'ngai' },
  { sid: 'chai_zanhoi', bad: 'chai_loose_fear', coldFlag: 'chai_heart_cold', line: 'chai' },
];
function build(sid, fav, ys, flags){
  resetS(950); _ys = ys || { year: 1992, season: '冬' };
  setFav(sid, fav || 45);
  const st = doneAllBeats(sid);
  st.heartDone = false;
  Object.assign(S.flags, flags || {});
  return enc79BuildScript(sid, false);
}

/* ---------- (A) 數據形狀＋對白內容 ---------- */
CASES.forEach(({ sid, coldFlag }) => {
  const D = ENC79_DIALOG[sid];
  ok('A ' + sid + ' 有 heartCold（7 句、無 choices）',
    !!D && !!D.heartCold && Array.isArray(D.heartCold.lines) && D.heartCold.lines.length === 7 && !D.heartCold.choices,
    'lines=' + (D && D.heartCold && D.heartCold.lines && D.heartCold.lines.length));
  ok('A ' + sid + ' cold 句句有講者（S／A／N）',
    !!D && D.heartCold.lines.every(ln => Array.isArray(ln) && (ln[0] === 'S' || ln[0] === 'A' || ln[0] === 'N') && typeof ln[1] === 'string' && ln[1].length > 0));
  ok('A ' + sid + ' 旁白（N 句）係書面語，無廣東話口語字（㗎／咗／唔／嘅／喇／啲／嗰）',
    !!D && D.heartCold.lines.filter(ln => ln[0] === 'N').every(ln => !/[㗎咗唔嘅喇啲嗰]/.test(ln[1])));
});
ok('A 駱 cold 講裂痕：彈畀自己聽、唔彈埋落去',
  hasText({ steps: ENC79_DIALOG.lok_gasing.heartCold.lines.map(l => ({ text: l[1] })) }, '彈畀自己聽') &&
  hasText({ steps: ENC79_DIALOG.lok_gasing.heartCold.lines.map(l => ({ text: l[1] })) }, '唔彈畀人聽'));
ok('A 魏 cold 講裂痕：企喺應該企嘅位、嗰晚未做到',
  hasText({ steps: ENC79_DIALOG.ngai_wingnaam.heartCold.lines.map(l => ({ text: l[1] })) }, '企喺應該企嘅位') &&
  hasText({ steps: ENC79_DIALOG.ngai_wingnaam.heartCold.lines.map(l => ({ text: l[1] })) }, '你嗰晚未做到'));
ok('A 齊 cold 講裂痕：驚嗰啲唔會同人講、唔講「冇同第二個人講過」',
  hasText({ steps: ENC79_DIALOG.chai_zanhoi.heartCold.lines.map(l => ({ text: l[1] })) }, '驚嗰啲，我唔會同人講') &&
  !hasText({ steps: ENC79_DIALOG.chai_zanhoi.heartCold.lines.map(l => ({ text: l[1] })) }, '冇同第二個人講過'));
CASES.forEach(({ sid }) => {
  const D = ENC79_DIALOG[sid];
  const coldTexts = new Set(D.heartCold.lines.map(l => l[1]));
  const warmTexts = new Set(D.heart.lines.map(l => l[1]));
  const overlap = [...coldTexts].filter(t => warmTexts.has(t));
  ok('A ' + sid + ' cold 同 warm 零逐句重用（唔可以直接用暖版對白）', overlap.length === 0, 'overlap=' + JSON.stringify(overlap));
});
ok('A 駱 cold 唔用暖版關鍵句（由頭聽到尾／彈畀你聽下）',
  !hasText({ steps: ENC79_DIALOG.lok_gasing.heartCold.lines.map(l => ({ text: l[1] })) }, '肯由頭聽到尾') &&
  !hasText({ steps: ENC79_DIALOG.lok_gasing.heartCold.lines.map(l => ({ text: l[1] })) }, '想彈畀你聽下'));
ok('A 魏 cold 唔用暖版關鍵句（你嗰下似返我後生／留三分力／眼要先到）',
  !hasText({ steps: ENC79_DIALOG.ngai_wingnaam.heartCold.lines.map(l => ({ text: l[1] })) }, '你嗰下，似返我後生') &&
  !hasText({ steps: ENC79_DIALOG.ngai_wingnaam.heartCold.lines.map(l => ({ text: l[1] })) }, '留三分力') &&
  !hasText({ steps: ENC79_DIALOG.ngai_wingnaam.heartCold.lines.map(l => ({ text: l[1] })) }, '眼要先到'));
ok('A 齊 cold 唔用暖版關鍵句（你覺得我應該點行／一哥呢兩個字）',
  !hasText({ steps: ENC79_DIALOG.chai_zanhoi.heartCold.lines.map(l => ({ text: l[1] })) }, '你覺得我應該點行') &&
  !hasText({ steps: ENC79_DIALOG.chai_zanhoi.heartCold.lines.map(l => ({ text: l[1] })) }, '一哥呢兩個字'));

/* ---------- (B) 暖／冷對照 ---------- */
CASES.forEach(({ sid, bad }) => {
  const cold = build(sid, 45, { year: 1992, season: '冬' }, { [bad]: 1 });
  ok('B ' + sid + ' 有壞旗 → 播 heartCold（7 句）、唔播暖版 heart、唔行 pool',
    cold && segSteps(cold, 'heartCold:' + sid).length === 7 &&
    !cold.steps.some(s => s.seg === 'heart:' + sid) &&
    !cold.steps.some(s => s.seg === 'pool:' + sid),
    'coldSegs=' + segSteps(cold, 'heartCold:' + sid).length);
  ok('B ' + sid + ' 有壞旗 → cold 無抉擇步（唔係抉擇交心）',
    cold && !cold.steps.some(s => s.choice && s.seg === 'heartCold:' + sid));
  const warm = build(sid, 45, { year: 1992, season: '冬' }, {});
  ok('B ' + sid + ' 無壞旗 → 播暖版 heart、唔播 heartCold',
    warm && warm.steps.some(s => s.seg === 'heart:' + sid) &&
    !warm.steps.some(s => s.seg === 'heartCold:' + sid));
});

/* ---------- (C) 冷版 heart 同提攜冷版獨立＋唔死局 ---------- */
CASES.forEach(({ sid, bad }) => {
  const cold = build(sid, 45, { year: 1992, season: '冬' }, { [bad]: 1 });
  const patronId = sid === 'lok_gasing' ? 'lok_patron_cold' : sid === 'ngai_wingnaam' ? 'ngai_patron_cold' : 'chai_patron_cold';
  ok('C ' + sid + ' cold heart 嗰次唔會順便播埋提攜冷版（兩個獨立 beat）',
    cold && !cold.steps.some(s => s.seg === 'beat:' + patronId));
  ok('C ' + sid + ' T4＋壞旗 → patron_cold beat 照開（enc79PickBeat）',
    (() => { resetS(951); setFav(sid, 70); const st = metStar(sid); for(const b of (ENC79_BEATS[sid] || [])) if(b.id !== patronId) st.beatsDone[b.id] = 1; S.flags[bad] = 1; return enc79BeatOpen(sid, beatOf(sid, patronId)) === true && enc79PickBeat(sid).id === patronId; })());
});
CASES.forEach(({ sid, bad }) => {
  // 播完冷版 heart（heartDone＋fav 46，仍 T3）→ 升到 T4 再撞，提攜冷版照播
  const cold = build(sid, 45, { year: 1992, season: '冬' }, { [bad]: 1 });
  playSeg(cold, 'heartCold:' + sid);
  const patronId = sid === 'lok_gasing' ? 'lok_patron_cold' : sid === 'ngai_wingnaam' ? 'ngai_patron_cold' : 'chai_patron_cold';
  const favAfter = S.stars[sid].fav;
  setFav(sid, 70);
  const st = S.stars[sid];
  for(const b of (ENC79_BEATS[sid] || [])) if(b.id !== patronId) st.beatsDone[b.id] = 1;
  delete st.beatsDone[patronId];
  const b2 = enc79BuildScript(sid, false);
  ok('C ' + sid + ' 播完冷版 heart 之後升 T4 → 提攜冷版照播（唔死局）',
    b2 && b2.steps.some(s => s.seg === 'beat:' + patronId), 'favAfterCold=' + favAfter);
});

/* ---------- (D) 播完效果 ---------- */
CASES.forEach(({ sid, bad, coldFlag, line }) => {
  const cold = build(sid, 45, { year: 1992, season: '冬' }, { [bad]: 1 });
  const fameBefore = S.fame;
  playSeg(cold, 'heartCold:' + sid);
  ok('D ' + sid + ' 冷版播完：heartDone＝true、好感＋1（45→46）、記 ' + coldFlag,
    S.stars[sid].heartDone === true && S.stars[sid].fav === 46 && S.flags[coldFlag] === 1,
    'fav=' + S.stars[sid].fav);
  ok('D ' + sid + ' 冷版播完：唔派暖版收尾獎勵（sideline280_' + line + ' 未落、聲望唔郁）',
    !S.flags['sideline280_' + line] && S.fame === fameBefore && S.industryCreditDelta === 0,
    'fame=' + S.fame);
  ok('D ' + sid + ' 冷版播完：唔入 grant229Queue',
    Array.isArray(S.grant229Queue) && S.grant229Queue.length === 0);
  const again = enc79BuildScript(sid, false);
  ok('D ' + sid + ' 再撞一次 → 唔重播冷版 heart（行 pool）',
    again && !again.steps.some(s => s.seg === 'heartCold:' + sid) && again.steps.some(s => s.seg === 'pool:' + sid));
});
CASES.forEach(({ sid }) => {
  const warm = build(sid, 45, { year: 1992, season: '冬' }, {});
  playSeg(warm, 'heart:' + sid);
  ok('D ' + sid + ' 暖版對照：播完 heartDone＝true、好感＋2（45→47）',
    S.stars[sid].heartDone === true && S.stars[sid].fav === 47, 'fav=' + S.stars[sid].fav);
});

/* ---------- (E) GRANT229 ---------- */
CASES.forEach(({ sid }) => {
  const before = S ? (S.grant229Queue || []).length : 0;
  const r = grant229RecordFromEnc79('heartCold:' + sid, '任何 label 都唔應該命中');
  ok('E grant229RecordFromEnc79("heartCold:' + sid + '") → false、唔入 queue',
    r === false && (S.grant229Queue || []).length === before);
});
ok('E GRANT229_ENC79 無任何 heartCold 行（暖版 heart: 行照在位）',
  Array.isArray(GRANT229_ENC79) &&
  !GRANT229_ENC79.some(r => String(r.seg || '').indexOf('heartCold:') === 0) &&
  ['heart:lok_gasing', 'heart:ngai_wingnaam', 'heart:chai_zanhoi'].every(seg => GRANT229_ENC79.some(r => r.seg === seg)));

/* ---------- (F) 舊檔 ---------- */
CASES.forEach(({ sid, bad }) => {
  resetS(952); _ys = { year: 1992, season: '冬' };
  S.stars = {};
  S.stars[sid] = { fav: 45, met: true }; // 舊檔：得 fav／met，無 beatsDone／poolSeen／heartDone／stage
  S.flags[bad] = 1;
  enc79EnsureStars();
  for(const b of (ENC79_BEATS[sid] || [])) S.stars[sid].beatsDone[b.id] = 1; // 行到 T3 嗰陣前面 beats 已經做晒（heart 先輪到）
  let b = null, err = null;
  try{ b = enc79BuildScript(sid, false); }catch(e){ err = e; }
  ok('F 舊檔 ' + sid + '（得 fav／met、有壞旗）→ 唔 crash、照播冷版 heart',
    !err && b && segSteps(b, 'heartCold:' + sid).length === 7, err ? String(err) : '');
});

/* ---------- (S) 靜態 guard ---------- */
ok('S 冷版分支排暖版之前',
  html.indexOf('D.heartCold && ((starId==="lok_gasing"') >= 0 &&
  html.indexOf('D.heartCold && ((starId==="lok_gasing"') < html.indexOf('} else if(tier>=3 && !st.heartDone && D.heart && !(starId==="chung_choning"'));
ok('S 暖版 heart 閘唔郁（三支壞旗照排除）',
  html.indexOf('!(starId==="lok_gasing" && (S.flags||{}).lok_loose_row)') >= 0 &&
  html.indexOf('!(starId==="ngai_wingnaam" && (S.flags||{}).ngai_rain_hold_back)') >= 0 &&
  html.indexOf('!(starId==="chai_zanhoi" && (S.flags||{}).chai_loose_fear)') >= 0);
ok('S 暖版 heart 對白唔郁（駱新歌／魏留三分力／齊冇同第二個人講過）',
  html.indexOf('我有首新歌，寫咗一半，想彈畀你聽下。') >= 0 &&
  html.indexOf('留三分力喺手，收得返，先唔會傷到自己人。') >= 0 &&
  html.indexOf('今日呢啲說話，我冇同第二個人講過。') >= 0);
ok('S 提攜冷版對白唔郁（駱錄音室／魏木箱／齊監視器）',
  html.indexOf('錄音室收咗工，冇人會趕我哋走。') >= 0 &&
  html.indexOf('木箱硬啲，唔好嫌。') >= 0 &&
  html.indexOf('我仲有場戲要默。') >= 0);
ok('S 鍾 cold 靜態在位（金鐘細房 4 句）',
  html.indexOf('金鐘創意的一間小房間，活動結束，人已散得七七八八。鍾楚凝坐在窗邊，看見阿偉進來，沒有叫他坐下。') >= 0 &&
  html.indexOf('阿偉，今日唔傾喇。我啲安排搞到七七八八，講多一句，都係多餘。') >= 0);
const gigsLib = GIGS_ARR;
ok('S gigs_new.json 仍係 330 張', gigsLib.length === 330, 'count=' + gigsLib.length);
ok('S 冷版 heart 唔叫 sideline280GrantCompletion（冷版回調無呢個 call）',
  (() => {
    const i = html.indexOf('pushSeg(D.heartCold, "heartCold:"+starId');
    if(i < 0) return false;
    const seg = html.slice(i, i + 400);
    return seg.indexOf('sideline280GrantCompletion') < 0;
  })());

if(fails.length){ console.log('FAILURES: ' + fails.join(', ')); process.exit(1); }
console.log('ALL PASS');
