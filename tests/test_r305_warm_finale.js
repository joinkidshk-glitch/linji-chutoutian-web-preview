// v20a305 Q18 五線 warm finale beats 測試：
//   (A) 數據：駱／魏／齊各有 *_finale（5／5／6 句、無 choices），對白＝草稿暖版收科逐字；旁白書面語
//   (B) 分流：暖版＋T4＋1992 冬＋提攜已播 → 播 finale；有壞旗／未到 1992 冬／tier 未夠／提攜未播 → 唔播
//   (C) 次序＋一次：提攜排 finale 之前（同場先播提攜）；播完落 enc79_*_finale 旗、唔重播
//   (D) 齊尾句分流：try_new 用 wrap 句、play_safe 用 cap 句（草稿好收尾變體二）
//   (E) 鍾：唔另開 finale beat；提攜排送別之前（遲到 T4 玩家先攞引薦、後送別；T2 玩家送別照播；冷版提攜冷版先播）
//   (F) 程：唔另開 finale beat；暖版收科＝after_train＋patron＋stageup 齊播，閘唔郁
//   (G) 舊檔：得 fav／met、提攜已播、1992 冬 → 唔 crash、照播 finale
//   (S) 靜態：patron／patron_cold 閘＋對白唔郁；陸／彭 finale 唔郁；gigs_new.json 仍係 322 張
// 用法：node tests/test_r305_warm_finale.js [path-to-index.html]
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

/* ---- sandbox（跟 test_r304_cold_heart.js；加 ENC84 對白＋鍾／程註冊） ---- */
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
const consts305 = ['ENC79_PLAYER_TIERS', 'ENC79_FAV_CAPS', 'ENC79_WEEK_SOFT_CAP', 'ENC79_STARS', 'ENC79_PILOT', 'ENC79_STAGEUP', 'ENC79_CAP_LINES', 'ENC79_WRAP_ECHO', 'ENC79_BEATS', 'ENC79_DIALOG', 'ENC79_FIRST_ALT98'].map(n => asVar(extractConst(n), n)).join('\n')
  + '\n' + ['ENC83_DLG_lok_gasing', 'ENC83_DLG_ngai_wingnaam', 'ENC83_DLG_chai_zanhoi', 'ENC84_DLG_chung_choning', 'ENC84_DLG_ching_tinlok'].map(n => asVar(extractDlg(n), n)).join('\n')
  + '\nENC79_DIALOG["lok_gasing"] = ENC83_DLG_lok_gasing;\nENC79_DIALOG["ngai_wingnaam"] = ENC83_DLG_ngai_wingnaam;\nENC79_DIALOG["chai_zanhoi"] = ENC83_DLG_chai_zanhoi;\nENC79_DIALOG["chung_choning"] = ENC84_DLG_chung_choning;\nENC79_DIALOG["ching_tinlok"] = ENC84_DLG_ching_tinlok;';
const p2Start = html.indexOf('/* ---------- Phase 2 四星鏈節拍');
const p2End = html.indexOf('/* ===== ENC83 模組完 =====', p2Start);
if(p2Start < 0 || p2End < 0) throw new Error('Phase 2 beats region not found');
const p2Region = html.slice(p2Start, p2End);
const p3Assigns = extractAssign('ENC79_BEATS.chung_choning = [') + '\n' + extractAssign('ENC79_BEATS.ching_tinlok = [');
const fns305 = ['enc79StarDef', 'enc79Hash', 'enc79Rand', 'enc79EnsureStars', 'enc79StarState', 'enc79TierOf', 'enc79PlayerTier', 'enc79FavCap', 'enc79AddFav', 'enc79WhisperActive', 'enc79GrantWhisper', 'enc79GrantCredit', 'enc79BoardHasStar', 'enc79BoardHasActionGig', 'enc79BeatOpen', 'enc79AnyBeatOpen', 'enc79PickBeat', 'enc79NormSeg', 'enc79BuildScript', 'enc83NodeDone', 'enc83Flag', 'enc83HasCredit', 'enc83NewsOut', 'contra98EncFirstLocSwap', 'sideline280GrantCompletion', 'grant229Ensure', 'grant229GigById', 'grant229Record', 'grant229RecordFromEnc79'];
eval(consts305 + '\n' + asVar(extractConst('GRANT229_ENC79'), 'GRANT229_ENC79') + '\n' + p2Region + '\n' + p3Assigns + '\n' + fns305.map(extractFn).join('\n'));

/* ---- helpers ---- */
function hasText(b, sub){ return (b && b.steps || []).some(s => String(s.text || '').indexOf(sub) >= 0); }
function segSteps(b, seg){ return (b && b.steps || []).filter(s => s.seg === seg); }
function playSeg(b, seg){ segSteps(b, seg).forEach(s => { try{ if(typeof s.segFx === 'function') s.segFx(); }catch(_e){} }); }
function linesOf(D, key){ return (D && D.beats && D.beats[key] && D.beats[key].lines) || []; }
const CASES = [
  { sid: 'lok_gasing', line: 'lok', bad: 'lok_loose_row', patron: 'lok_patron', cold: 'lok_patron_cold', n: 5,
    keys: ['歌係自己嘅，嗰種實淨，冇人攞得走', '我唱咗十幾年，輸俾排榜遊戲', '歌仲喺度，人就唔好俾人收埋'] },
  { sid: 'ngai_wingnaam', line: 'ngai', bad: 'ngai_rain_hold_back', patron: 'ngai_patron', cold: 'ngai_patron_cold', n: 5,
    keys: ['呢行唔記得邊個紅過，只記得邊個仲企得穩', '你而家企到呢個位，記得扶返啲肯捱嘅後生', '我個電話仲打得通'] },
  { sid: 'chai_zanhoi', line: 'chai', bad: 'chai_loose_fear', patron: 'chai_patron', cold: 'chai_patron_cold', n: 6,
    keys: ['唔再當你係企後面嗰個臨時演員喇', '人同人之間，過咗嗰條線，就唔同晒', '殺青喇，阿偉。同你做呢套戲，我冇睇錯人。嚟緊嗰條路點行，你自己企穩，我會喺後面望住。'] },
];
/* 暖版齊晒：T4＋1992 冬＋提攜已播＋無壞旗；前面 beats 全部做晒，淨低 finale */
function buildWarmFinale(c, ys, flags){
  resetS(950); _ys = ys || { year: 1992, season: '冬' };
  setFav(c.sid, 70);
  const st = doneExcept(c.sid, [c.line + '_finale']);
  st.heartDone = true; // 交心唔係今次測試對象，封住佢免得搶段
  Object.assign(S.flags, flags || {});
  return enc79BuildScript(c.sid, false);
}

/* ---------- (A) 數據形狀＋對白內容 ---------- */
CASES.forEach(c => {
  const D = ENC79_DIALOG[c.sid];
  const fin = D && D.beats && D.beats[c.line + '_finale'];
  ok('A ' + c.sid + ' 有 ' + c.line + '_finale（' + c.n + ' 句、無 choices）',
    !!fin && Array.isArray(fin.lines) && fin.lines.length === c.n && !fin.choices,
    'lines=' + (fin && fin.lines && fin.lines.length));
  ok('A ' + c.sid + ' finale 句句有講者（S／A／N）',
    !!fin && fin.lines.every(ln => Array.isArray(ln) && (ln[0] === 'S' || ln[0] === 'A' || ln[0] === 'N') && typeof ln[1] === 'string' && ln[1].length > 0));
  ok('A ' + c.sid + ' 旁白（N 句）係書面語，無廣東話口語字（㗎／咗／唔／嘅／喇／啲／嗰）',
    !!fin && fin.lines.filter(ln => ln[0] === 'N').every(ln => !/[㗎咗唔嘅喇啲嗰]/.test(ln[1])));
  c.keys.forEach(k => {
    ok('A ' + c.sid + ' finale 有草稿暖版關鍵句：' + k.slice(0, 12) + '…',
      fin.lines.some(ln => String(ln[1]).indexOf(k) >= 0));
  });
  const coldTexts = new Set(linesOf(D, c.cold).map(l => l[1]));
  const finTexts = new Set(fin.lines.map(l => l[1]));
  const overlap = [...finTexts].filter(t => coldTexts.has(t));
  ok('A ' + c.sid + ' finale 同提攜冷版零逐句重用（暖／冷唔係同一場）', overlap.length === 0, 'overlap=' + JSON.stringify(overlap));
  ok('A ' + c.sid + ' finale 排喺提攜之後（registry 次序）',
    (ENC79_BEATS[c.sid] || []).findIndex(b => b.id === c.patron) < (ENC79_BEATS[c.sid] || []).findIndex(b => b.id === c.line + '_finale'));
});

/* ---------- (B) 暖／冷／年份／tier／提攜先後分流 ---------- */
CASES.forEach(c => {
  const warm = buildWarmFinale(c);
  ok('B ' + c.sid + ' 暖版齊晒 → 播 finale（' + c.n + ' 句）',
    warm && segSteps(warm, 'beat:' + c.line + '_finale').length === c.n,
    'segs=' + segSteps(warm, 'beat:' + c.line + '_finale').length);
  ok('B ' + c.sid + ' 暖版齊晒 → finale 係今次揀中嗰個 beat（PickBeat）',
    (() => { resetS(951); _ys = { year: 1992, season: '冬' }; setFav(c.sid, 70); doneExcept(c.sid, [c.line + '_finale']); const p = enc79PickBeat(c.sid); return p && p.id === c.line + '_finale'; })());
  ok('B ' + c.sid + ' 有壞旗（' + c.bad + '）→ finale 唔開，提攜冷版照開',
    (() => { resetS(952); _ys = { year: 1992, season: '冬' }; setFav(c.sid, 70); doneExcept(c.sid, [c.cold, c.line + '_finale']); S.flags[c.bad] = 1;
      return enc79BeatOpen(c.sid, beatOf(c.sid, c.line + '_finale')) === false && enc79PickBeat(c.sid).id === c.cold; })());
  ok('B ' + c.sid + ' 未到 1992 冬（1992 秋）→ finale 唔開',
    (() => { resetS(953); _ys = { year: 1992, season: '秋' }; setFav(c.sid, 70); doneExcept(c.sid, [c.line + '_finale']); return enc79BeatOpen(c.sid, beatOf(c.sid, c.line + '_finale')) === false; })());
  ok('B ' + c.sid + ' 未到 1992 冬（1991 冬）→ finale 唔開',
    (() => { resetS(954); _ys = { year: 1991, season: '冬' }; setFav(c.sid, 70); doneExcept(c.sid, [c.line + '_finale']); return enc79BeatOpen(c.sid, beatOf(c.sid, c.line + '_finale')) === false; })());
  ok('B ' + c.sid + ' tier 未夠（T3，fav 45）→ finale 唔開',
    (() => { resetS(955); _ys = { year: 1992, season: '冬' }; setFav(c.sid, 45); doneExcept(c.sid, [c.line + '_finale']); return enc79BeatOpen(c.sid, beatOf(c.sid, c.line + '_finale')) === false; })());
  ok('B ' + c.sid + ' 提攜未播 → finale 唔開，先播提攜',
    (() => { resetS(956); _ys = { year: 1992, season: '冬' }; setFav(c.sid, 70); doneExcept(c.sid, [c.patron, c.line + '_finale']);
      if(c.sid==='lok_gasing') S.flags.lok_calm_truth=1; /* v20a314：駱提攜暖版嚴格閘要 lok_calm_truth 正面旗 */
      if(c.sid==='chai_zanhoi') S.flags.chai_truth_change=1; /* v20a318：齊提攜暖版閘要 chai_truth_change 正面旗 */
      return enc79BeatOpen(c.sid, beatOf(c.sid, c.line + '_finale')) === false && enc79PickBeat(c.sid).id === c.patron; })());
});

/* ---------- (C) 播完效果：落旗、唔重播、唔派收尾獎勵（提攜嗰陣已派） ---------- */
CASES.forEach(c => {
  const warm = buildWarmFinale(c);
  playSeg(warm, 'beat:' + c.line + '_finale');
  ok('C ' + c.sid + ' 播完 finale → 落 enc79_' + c.line + '_finale 旗',
    S.flags['enc79_' + c.line + '_finale'] === 1);
  ok('C ' + c.sid + ' 播完 finale → beatsDone 記低，唔重播',
    S.stars[c.sid].beatsDone[c.line + '_finale'] && (() => { const again = enc79BuildScript(c.sid, false); return again && !again.steps.some(s => s.seg === 'beat:' + c.line + '_finale'); })());
});

/* ---------- (D) 齊尾句分流 ---------- */
(function(){
  const c = CASES[2];
  const wrapLine = '殺青喇，阿偉。同你做呢套戲，我冇睇錯人。嚟緊嗰條路點行，你自己企穩，我會喺後面望住。';
  const capLine = '阿偉，今日傾到呢度先啦，我仲有場戲要默。你有呢份心，我領咗，不過有啲路，仲要慢慢行，唔好急。';
  const bTry = buildWarmFinale(c, { year: 1992, season: '冬' }, { chai_try_new: 1 });
  const lastTry = segSteps(bTry, 'beat:chai_finale');
  ok('D 齊 try_new → finale 尾句係 wrap 句（殺青喇…）',
    lastTry.length === 6 && lastTry[5].text === wrapLine, 'last=' + (lastTry[5] && lastTry[5].text));
  const bSafe = buildWarmFinale(c, { year: 1992, season: '冬' }, { chai_play_safe: 1 });
  const lastSafe = segSteps(bSafe, 'beat:chai_finale');
  ok('D 齊 play_safe → finale 尾句係 cap 句（今日傾到呢度先啦…）',
    lastSafe.length === 6 && lastSafe[5].text === capLine, 'last=' + (lastSafe[5] && lastSafe[5].text));
  ok('D 齊 play_safe 播完 finale → 照落 enc79_chai_finale 旗',
    (() => { playSeg(bSafe, 'beat:chai_finale'); return S.flags.enc79_chai_finale === 1; })());
})();

/* ---------- (E) 鍾：唔另開 finale；提攜排送別之前 ---------- */
ok('E 鍾無 finale beat（registry 無 chung_finale，對白表 beats 無 chung_finale）',
  !(ENC79_BEATS.chung_choning || []).some(b => b.id === 'chung_finale') &&
  !(ENC79_DIALOG.chung_choning && ENC79_DIALOG.chung_choning.beats && ENC79_DIALOG.chung_choning.beats.chung_finale));
ok('E 鍾 registry：提攜（冷／暖）排送別之前',
  (() => {
    const ids = (ENC79_BEATS.chung_choning || []).map(b => b.id);
    return ids.indexOf('chung_patron_cold') < ids.indexOf('chung_farewell') && ids.indexOf('chung_patron') < ids.indexOf('chung_farewell');
  })(), 'order=' + (ENC79_BEATS.chung_choning || []).map(b => b.id).join(','));
ok('E 鍾遲到 T4 暖版（1992 秋、乜都未播）→ 先播提攜、唔係送別',
  (() => { resetS(960); _ys = { year: 1992, season: '秋' }; setFav('chung_choning', 70); doneExcept('chung_choning', ['chung_patron', 'chung_farewell']);
    return enc79PickBeat('chung_choning').id === 'chung_patron'; })());
ok('E 鍾遲到 T4 暖版：提攜播完 → 下次先播送別（暖版收科齊播）',
  (() => { resetS(961); _ys = { year: 1992, season: '秋' }; setFav('chung_choning', 70); const st = doneExcept('chung_choning', ['chung_patron', 'chung_farewell']);
    const b1 = enc79BuildScript('chung_choning', false);
    playSeg(b1, 'beat:chung_patron');
    return S.stars.chung_choning.beatsDone.chung_patron && enc79PickBeat('chung_choning').id === 'chung_farewell'; })());
ok('E 鍾 T2 玩家（1992 秋）→ 送別照播（唔使 T4）',
  (() => { resetS(962); _ys = { year: 1992, season: '秋' }; setFav('chung_choning', 30); doneExcept('chung_choning', ['chung_farewell']);
    return enc79BeatOpen('chung_choning', beatOf('chung_choning', 'chung_farewell')) === true && enc79PickBeat('chung_choning').id === 'chung_farewell'; })());
ok('E 鍾冷版（T4＋loose_talk）→ 先播提攜冷版、後送別',
  (() => { resetS(963); _ys = { year: 1992, season: '秋' }; setFav('chung_choning', 70); doneExcept('chung_choning', ['chung_patron_cold', 'chung_farewell']); S.flags.chung_loose_talk = 1;
    const p1 = enc79PickBeat('chung_choning').id;
    S.stars.chung_choning.beatsDone.chung_patron_cold = 1;
    const p2 = enc79PickBeat('chung_choning').id;
    return p1 === 'chung_patron_cold' && p2 === 'chung_farewell'; })());
ok('E 鍾提攜播完 → 授 credit_enc84_chung_patron 債權（引薦照兌現）',
  (() => { resetS(964); _ys = { year: 1992, season: '秋' }; setFav('chung_choning', 70); doneExcept('chung_choning', ['chung_patron', 'chung_farewell']);
    const b = enc79BuildScript('chung_choning', false); playSeg(b, 'beat:chung_patron');
    return enc83HasCredit('credit_enc84_chung_patron') === true; })());

/* ---------- (F) 程：唔另開 finale；暖版收科三件套閘唔郁 ---------- */
ok('F 程無 finale beat（registry 無 ching_finale，對白表 beats 無 ching_finale）',
  !(ENC79_BEATS.ching_tinlok || []).some(b => b.id === 'ching_finale') &&
  !(ENC79_DIALOG.ching_tinlok && ENC79_DIALOG.ching_tinlok.beats && ENC79_DIALOG.ching_tinlok.beats.ching_finale));
ok('F 程暖版收科：after_train 閘（N15＋flag_vocal_train）照開',
  (() => { resetS(970); _ys = { year: 1992, season: '冬' }; setFav('ching_tinlok', 70); _doneNodes.add('N15'); S.flags.flag_vocal_train = 1; doneExcept('ching_tinlok', ['ching_after_train']);
    return enc79BeatOpen('ching_tinlok', beatOf('ching_tinlok', 'ching_after_train')) === true; })());
ok('F 程暖版收科：patron 閘（T4＋flag_vocal_train＋ching_back_train＋ching_stand_slow 三旗齊備，v20a311）照開',
  (() => { resetS(971); _ys = { year: 1992, season: '冬' }; setFav('ching_tinlok', 70); S.flags.flag_vocal_train = 1; S.flags.ching_back_train = 1; S.flags.ching_stand_slow = 1; doneExcept('ching_tinlok', ['ching_patron']);
    return enc79BeatOpen('ching_tinlok', beatOf('ching_tinlok', 'ching_patron')) === true; })());

/* ---------- (G) 舊檔 ---------- */
CASES.forEach(c => {
  resetS(980); _ys = { year: 1992, season: '冬' };
  S.stars = {};
  S.stars[c.sid] = { fav: 70, met: true }; // 舊檔：得 fav／met，無 beatsDone／poolSeen／heartDone／stage
  enc79EnsureStars();
  for(const b of (ENC79_BEATS[c.sid] || [])) if(b.id !== c.line + '_finale') S.stars[c.sid].beatsDone[b.id] = 1;
  S.stars[c.sid].heartDone = true;
  let b = null, err = null;
  try{ b = enc79BuildScript(c.sid, false); }catch(e){ err = e; }
  ok('G 舊檔 ' + c.sid + '（得 fav／met、提攜已播、1992 冬）→ 唔 crash、照播 finale',
    !err && b && segSteps(b, 'beat:' + c.line + '_finale').length === c.n, err ? String(err) : '');
});

/* ---------- (S) 靜態 guard ---------- */
ok('S 三線提攜閘唔郁（駱三旗／魏兩旗／齊 truth_change＋三旗排除式，v20a318）',
  html.indexOf('!(S.flags||{}).lok_join_rant && !(S.flags||{}).lok_loose_row && !(S.flags||{}).lok_cover_first') >= 0 &&
  html.indexOf('!(S.flags||{}).ngai_rain_hold_back && !(S.flags||{}).ngai_patron_honest') >= 0 &&
  html.indexOf('!(S.flags||{}).chai_silent && !(S.flags||{}).chai_comfort && !(S.flags||{}).chai_loose_fear') >= 0);
ok('S 三線提攜對白唔郁（駱監製老友／魏電話打得通／齊試鏡）',
  html.indexOf('我約咗一位唱片監製老友食飯，我同佢提起你') >= 0 &&
  html.indexOf('我魏詠男個名而家唔值錢，但呢個電話仲打得通。') >= 0 &&
  html.indexOf('我齊鎮海開口，佢會畀個試鏡你。') >= 0);
ok('S 三線提攜冷版對白唔郁（駱後巷／魏木箱／齊監視器）',
  html.indexOf('呢度冇人會趕我哋走。') >= 0 &&
  html.indexOf('木箱硬啲，唔好嫌。') >= 0 &&
  html.indexOf('我仲有場戲要默。') >= 0);
ok('S 鍾送別閘唔郁（T2＋1992 秋／冬）＋授 chungAdviceHeld229 唔郁',
  html.indexOf('id:"chung_farewell", when(st){ const ys=yearSeasonNow(); return enc79TierOf(st.fav)>=2 && ys.year===1992 && (ys.season==="秋" || ys.season==="冬"); }') >= 0 &&
  html.indexOf('S.flags.chungAdviceHeld229 = 1') >= 0);
ok('S 鍾提攜授 credit_enc84_chung_patron 唔郁',
  html.indexOf('id:"credit_enc84_chung_patron"') >= 0);
ok('S 程提攜閘（v20a311 嚴格版：T4＋flag_vocal_train＋ching_back_train＋ching_stand_slow）',
  html.indexOf('enc87StoryFlag("flag_vocal_train") && !!(S.flags||{}).ching_back_train && !!(S.flags||{}).ching_stand_slow') >= 0);
ok('S 陸／彭 finale 唔郁（luk_finale 閘＋旗、pang_finale 閘在位）',
  html.indexOf('id:"luk_finale"') >= 0 && html.indexOf('S.flags.enc79_luk_finale=1') >= 0 &&
  html.indexOf('id:"pang_finale"') >= 0 && html.indexOf('(st.beatsDone||{}).pang_n17 && (S.flags||{}).pang_cover_night && (S.flags||{}).pang_listened && (S.flags||{}).pang_noodle_night') >= 0);
ok('S 齊 FRAME cap／wrap 唔郁（Q19 範圍，今版唔掂）',
  html.indexOf('cap: ["S", "阿偉，今日傾到呢度先啦，我仲有場戲要默。你有呢份心，我領咗，不過有啲路，仲要慢慢行，唔好急。"]') >= 0 &&
  html.indexOf('wrap: ["S", "殺青喇，阿偉。同你做呢套戲，我冇睇錯人。嚟緊嗰條路點行，你自己企穩，我會喺後面望住。"]') >= 0);
const gigsLib = GIGS_ARR;
ok('S gigs_new.json 仍係 322 張', gigsLib.length === 322, 'count=' + gigsLib.length);
ok('S finale 唔叫 sideline280GrantCompletion（收尾獎勵提攜嗰陣已派，唔重派）',
  (() => {
    let good = true;
    ['lok_finale', 'ngai_finale', 'chai_finale'].forEach(id => {
      const i = html.indexOf('id:"' + id + '"');
      if(i < 0){ good = false; return; }
      const seg = html.slice(i, i + 500);
      if(seg.indexOf('sideline280GrantCompletion') >= 0) good = false;
    });
    return good;
  })());

if(fails.length){ console.log('FAILURES: ' + fails.join(', ')); process.exit(1); }
console.log('ALL PASS');
