// v20a356 resync：支線複檢 (a) 類修復改咗 ENC 釘句（齊 wrap／駱 patron_cold／彭 finale_cold＋n17／程 e4／魏 heartCold／駱 heart label／彭 intel label／齊 choice GRANT key），釘句同步更新，邏輯斷言唔郁。
// v20a312 Q25 彭少祺 pang_help 遲到行冷版，全套三閘測試：
//   (A) 靜態：三閘齊加 pang_late；pang_n17 閘唔郁（遲到玩家去得到 n17）；
//       pang_intel 選擇／授旗／即派唔郁；對白唔郁
//   (B) when() 直接判定：pang_help——準時開、遲到閂、N11 未做閂、T0 閂；
//       pang_finale_cold——遲到開、無旗閂、T2 閂、n17 未做閂；舊三旗照開
//   (C) 端到端 buildScript：遲到→頂一晚唔開、唔播暖版交心、去得到 n17、冷收尾照去得到；
//       準時→三閘行為唔變；遲到＋暖收尾三旗齊→冷收尾贏（註冊次序冷行先）
//   (D) 對位：pang_intel 兩選擇 GRANT229 照派（準時→variety_201／遲到→variety_104）、fav 照計
//   (E) 舊檔：已有 pang_late 嘅舊 save 唔 crash，閘行為同新檔一致
//   (S) 靜態：pang_patron 閘唔郁；gigs_new.json 仍係 326 張
// 用法：node tests/test_r312_pang_late_cold.js [path-to-index.html]
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

/* ---- sandbox（跟 test_r309_pang_n17_cold.js） ---- */
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
const consts312 = ['ENC79_PLAYER_TIERS', 'ENC79_FAV_CAPS', 'ENC79_WEEK_SOFT_CAP', 'ENC79_STARS', 'ENC79_PILOT', 'ENC79_STAGEUP', 'ENC79_CAP_LINES', 'ENC79_WRAP_ECHO', 'ENC79_BEATS', 'ENC79_DIALOG', 'ENC79_FIRST_ALT98'].map(n => asVar(extractConst(n), n)).join('\n')
  + '\n' + asVar(extractDlg('ENC84_DLG_pang_siuki'), 'ENC84_DLG_pang_siuki')
  + '\nENC79_DIALOG["pang_siuki"] = ENC84_DLG_pang_siuki;';
const p2Start = html.indexOf('/* ---------- Phase 2 四星鏈節拍');
const p2End = html.indexOf('/* ===== ENC83 模組完 =====', p2Start);
if(p2Start < 0 || p2End < 0) throw new Error('Phase 2 beats region not found');
const p2Region = html.slice(p2Start, p2End);
const fns312 = ['enc79StarDef', 'enc79Hash', 'enc79Rand', 'enc79EnsureStars', 'enc79StarState', 'enc79TierOf', 'enc79PlayerTier', 'enc79FavCap', 'enc79AddFav', 'enc79WhisperActive', 'enc79GrantWhisper', 'enc79GrantCredit', 'enc79BoardHasStar', 'enc79BoardHasActionGig', 'enc79BeatOpen', 'enc79AnyBeatOpen', 'enc79PickBeat', 'enc79NormSeg', 'enc79BuildScript', 'enc79ChoiceFx', 'enc83NodeDone', 'enc83Flag', 'enc83HasCredit', 'enc83NewsOut', 'contra98EncFirstLocSwap', 'sideline280GrantCompletion', 'grant229Ensure', 'grant229GigById', 'grant229Record', 'grant229RecordFromEnc79'];
eval(consts312 + '\n' + asVar(extractConst('GRANT229_ENC79'), 'GRANT229_ENC79') + '\n' + p2Region + '\n' + extractAssign('ENC79_BEATS.pang_siuki = [') + '\n' + fns312.map(extractFn).join('\n'));

/* ---- helpers ---- */
function hasSeg(b, seg){ return ((b && b.steps) || []).some(s => s.seg === seg); }
function buildPang(opts){
  const o = opts || {};
  resetS(o.day || 950); _ys = o.ys || { year: 1992, season: '冬' };
  setFav('pang_siuki', o.fav === undefined ? 45 : o.fav);
  const st = metStar('pang_siuki');
  (o.done || []).forEach(id => { st.beatsDone[id] = 1; });
  if(o.n11) _doneNodes.add('N11');
  Object.assign(S.flags, o.flags || {});
  return enc79BuildScript('pang_siuki', false);
}
const HELP = beatOf('pang_siuki', 'pang_help');
const N17 = beatOf('pang_siuki', 'pang_n17');
const FCOLD = beatOf('pang_siuki', 'pang_finale_cold');
const FWARM = beatOf('pang_siuki', 'pang_finale');
const PATRON = beatOf('pang_siuki', 'pang_patron');
const D = ENC79_DIALOG.pang_siuki;

/* ---------- (A) 靜態：三閘齊加 pang_late，其餘唔郁 ---------- */
ok('A pang_help 閘加 !pang_late（仍要 T1＋N11）',
  !!HELP && HELP.when.toString().indexOf('pang_late') >= 0 &&
  HELP.when.toString().indexOf('enc79TierOf(st.fav)>=1') >= 0 &&
  HELP.when.toString().indexOf('enc83NodeDone("N11")') >= 0);
ok('A 暖版 heart 閘加 pang_late（彭嗰邊同 absent_night 並列）',
  html.indexOf('starId==="pang_siuki" && (S.flags||{}).pang_late') >= 0 &&
  html.indexOf('starId==="pang_siuki" && (S.flags||{}).pang_absent_night') >= 0);
ok('A pang_finale_cold 閘加 pang_late 做第四旗（舊三旗＋n17＋1992 冬齊晒）',
  !!FCOLD && FCOLD.when.toString().indexOf('pang_late') >= 0 &&
  FCOLD.when.toString().indexOf('pang_absent_night') >= 0 &&
  FCOLD.when.toString().indexOf('pang_brushed_off') >= 0 &&
  FCOLD.when.toString().indexOf('pang_early_night') >= 0 &&
  FCOLD.when.toString().indexOf('pang_n17') >= 0 &&
  FCOLD.when.toString().indexOf('1992') >= 0);
ok('A pang_n17 閘唔郁（淨 T3＋1992 冬，無 pang_late）',
  !!N17 && N17.when.toString().indexOf('pang_late') < 0 &&
  N17.when.toString().indexOf('enc79TierOf(st.fav)>=3') >= 0 &&
  N17.when.toString().indexOf('1992') >= 0);
ok('A pang_intel 兩選擇唔郁（準時授 pang_showed_up／遲到授 pang_late）',
  !!D && !!D.beats && !!D.beats.pang_intel &&
  D.beats.pang_intel.choices[0].label === '一早去後台留名，準時到' &&
  JSON.stringify(D.beats.pang_intel.choices[0].flags) === JSON.stringify(['pang_showed_up']) &&
  D.beats.pang_intel.choices[1].label === '遲咗去，覺得唔差在' &&
  JSON.stringify(D.beats.pang_intel.choices[1].flags) === JSON.stringify(['pang_late']));
ok('A pang_help 對白唔郁（首句逐字）',
  !!D && !!D.beats && !!D.beats.pang_help &&
  D.beats.pang_help.lines[0][1] === '阿偉，今晚要你幫下手啦，慈善騷綵排，後台臨時唔見咗個助手，成個流程冇人睇住。');
ok('A pang heart 對白唔郁（D.heart 在位）',
  !!D && !!D.heart && Array.isArray(D.heart.lines) && D.heart.lines.length > 0);
ok('A pang_finale_cold 對白唔郁（凍咗嗰碗麵開場在位）',
  !!D && !!D.beats && !!D.beats.pang_finale_cold &&
  D.beats.pang_finale_cold.lines.some(l => String(l[1]).indexOf('阿偉一早到了，叫了一碗雲吞麵，坐著等') >= 0));

/* ---------- (B) when() 直接判定 ---------- */
ok('B pang_help：N11 做咗＋T1（fav 10）＋準時 → 開',
  (() => { resetS(950); _doneNodes.add('N11'); return HELP.when({ fav: 10 }) === true; })());
ok('B pang_help：同一條件＋pang_late → 閂（行為改變核心）',
  (() => { resetS(950); _doneNodes.add('N11'); S.flags.pang_late = 1; return HELP.when({ fav: 10 }) === false; })());
ok('B pang_help：N11 未做 → 閂（舊閘照行）',
  (() => { resetS(950); return HELP.when({ fav: 10 }) === false; })());
ok('B pang_help：T0（fav 9）→ 閂',
  (() => { resetS(950); _doneNodes.add('N11'); return HELP.when({ fav: 9 }) === false; })());
ok('B pang_help：遲到但 fav 高（T3）照閂',
  (() => { resetS(950); _doneNodes.add('N11'); S.flags.pang_late = 1; return HELP.when({ fav: 45 }) === false; })());
ok('B pang_finale_cold：T3＋1992 冬＋n17 做完＋pang_late → 開（when() 回 truthy，唔係 boolean true）',
  (() => { resetS(950); _ys = { year: 1992, season: '冬' }; S.flags.pang_late = 1; return !!FCOLD.when({ fav: 45, beatsDone: { pang_n17: 1 } }); })());
ok('B pang_finale_cold：同一條件無任何旗 → 閂',
  (() => { resetS(950); _ys = { year: 1992, season: '冬' }; return !FCOLD.when({ fav: 45, beatsDone: { pang_n17: 1 } }); })());
ok('B pang_finale_cold：舊三旗照開（brushed_off）',
  (() => { resetS(950); _ys = { year: 1992, season: '冬' }; S.flags.pang_brushed_off = 1; return !!FCOLD.when({ fav: 45, beatsDone: { pang_n17: 1 } }); })());
ok('B pang_finale_cold：T2（fav 25）＋遲到 → 閂',
  (() => { resetS(950); _ys = { year: 1992, season: '冬' }; S.flags.pang_late = 1; return !FCOLD.when({ fav: 25, beatsDone: { pang_n17: 1 } }); })());
ok('B pang_finale_cold：n17 未做＋遲到 → 閂',
  (() => { resetS(950); _ys = { year: 1992, season: '冬' }; S.flags.pang_late = 1; return !FCOLD.when({ fav: 45, beatsDone: {} }); })());
ok('B pang_n17：遲到玩家 T3＋1992 冬 → 閘開（去得到 n17，唔死局）',
  (() => { resetS(950); _ys = { year: 1992, season: '冬' }; setFav('pang_siuki', 45); metStar('pang_siuki'); S.flags.pang_late = 1; return enc79BeatOpen('pang_siuki', N17) === true; })());

/* ---------- (C) 端到端 buildScript ---------- */
ok('C 準時玩家（T1＋N11＋intel 做咗）→ 播 beat:pang_help',
  hasSeg(buildPang({ fav: 10, n11: true, done: ['pang_intel'], ys: { year: 1991, season: '秋' } }), 'beat:pang_help'));
ok('C 遲到玩家同一條件 → 唔播 beat:pang_help（行 pool，唔 crash）',
  (() => { const b = buildPang({ fav: 10, n11: true, done: ['pang_intel'], flags: { pang_late: 1 }, ys: { year: 1991, season: '秋' } }); return !!b && !hasSeg(b, 'beat:pang_help'); })());
ok('C 準時玩家（T3＋intel／help 做咗，1992 春，n17 未開）→ 播 heart:pang_siuki',
  hasSeg(buildPang({ fav: 45, done: ['pang_intel', 'pang_help'], ys: { year: 1992, season: '春' } }), 'heart:pang_siuki'));
ok('C 遲到玩家同一條件 → 唔播 heart:pang_siuki（行 pool，唔 crash）',
  (() => { const b = buildPang({ fav: 45, done: ['pang_intel', 'pang_help'], flags: { pang_late: 1 }, ys: { year: 1992, season: '春' } }); return !!b && !hasSeg(b, 'heart:pang_siuki'); })());
ok('C 遲到玩家 n17 做完 → 再遇播 beat:pang_finale_cold',
  hasSeg(buildPang({ fav: 45, done: ['pang_intel', 'pang_help', 'pang_n17'], flags: { pang_late: 1 }, ys: { year: 1992, season: '冬' } }), 'beat:pang_finale_cold'));
ok('C 準時玩家 n17 做完、無任何旗 → 唔播 beat:pang_finale_cold',
  (() => { const b = buildPang({ fav: 45, done: ['pang_intel', 'pang_help', 'pang_n17'], ys: { year: 1992, season: '冬' } }); return !!b && !hasSeg(b, 'beat:pang_finale_cold'); })());
ok('C 遲到玩家＋暖收尾三旗齊（cover／listened／noodle）→ 冷收尾贏，唔入暖收尾',
  (() => {
    const b = buildPang({ fav: 45, done: ['pang_intel', 'pang_help', 'pang_n17'], flags: { pang_late: 1, pang_cover_night: 1, pang_listened: 1, pang_noodle_night: 1 }, ys: { year: 1992, season: '冬' } });
    return !!b && hasSeg(b, 'beat:pang_finale_cold') && !hasSeg(b, 'beat:pang_finale');
  })());
ok('C 準時玩家＋暖收尾三旗齊 → 播暖收尾（舊行為唔變）',
  (() => {
    const b = buildPang({ fav: 45, done: ['pang_intel', 'pang_help', 'pang_n17'], flags: { pang_cover_night: 1, pang_listened: 1, pang_noodle_night: 1 }, ys: { year: 1992, season: '冬' } });
    return !!b && hasSeg(b, 'beat:pang_finale') && !hasSeg(b, 'beat:pang_finale_cold');
  })());

/* ---------- (D) GRANT229＋fav 對位唔郁 ---------- */
resetS(950);
ok('D pang_intel 準時 label → GRANT229 照派 gig_1991_variety_201',
  grant229RecordFromEnc79('beat:pang_intel', '一早去後台留名，準時到') === true && S.grant229Queue.some(q => q.gigId === 'gig_1991_variety_201'),
  'queue=' + JSON.stringify(S.grant229Queue.map(q => q.gigId)));
resetS(950);
ok('D pang_intel 遲到 label → GRANT229 照派 gig_1991_variety_104',
  grant229RecordFromEnc79('beat:pang_intel', '遲咗去，覺得唔差在') === true && S.grant229Queue.some(q => q.gigId === 'gig_1991_variety_104'),
  'queue=' + JSON.stringify(S.grant229Queue.map(q => q.gigId)));
ok('D pang_intel 準時選擇 fav＋3（enc79ChoiceFx 同舊一樣）',
  enc79ChoiceFx('beat:pang_intel', '一早去後台留名，準時到').fav === 3);
ok('D pang_intel 遲到選擇 fav＋0（enc79ChoiceFx 同舊一樣：遲到無好感）',
  enc79ChoiceFx('beat:pang_intel', '遲咗去，覺得唔差在').fav === 0);

/* ---------- (E) 舊檔 ---------- */
ok('E 舊檔（fav／met＋頭兩幕已做＋pang_late）唔 crash：頂一晚唔開、暖版交心唔播',
  (() => {
    resetS(950); _ys = { year: 1992, season: '春' };
    S.stars = { pang_siuki: { fav: 45, met: true, stage: 3, beatsDone: { pang_intel: 1, pang_help: 1 } } };
    S.flags.pang_late = 1;
    _doneNodes.add('N11');
    let b = null, err = null;
    try{ b = enc79BuildScript('pang_siuki', false); }catch(e){ err = e; }
    return !err && !!b && !hasSeg(b, 'beat:pang_help') && !hasSeg(b, 'heart:pang_siuki');
  })());
ok('E 舊檔遲到玩家 n17 做完 → 冷收尾照開',
  (() => {
    resetS(950); _ys = { year: 1992, season: '冬' };
    S.stars = { pang_siuki: { fav: 45, met: true, stage: 3, beatsDone: { pang_intel: 1, pang_help: 1, pang_n17: 1 } } };
    S.flags.pang_late = 1;
    let b = null, err = null;
    try{ b = enc79BuildScript('pang_siuki', false); }catch(e){ err = e; }
    return !err && !!b && hasSeg(b, 'beat:pang_finale_cold');
  })());

/* ---------- (S) 靜態其餘 ---------- */
ok('S pang_patron 閘唔郁（淨 T4，無 pang_late）',
  !!PATRON && PATRON.when.toString().indexOf('enc79TierOf(st.fav)>=4') >= 0 && PATRON.when.toString().indexOf('pang_late') < 0);
ok('S pang_finale 暖收尾閘唔郁（cover＋listened＋noodle 三旗）',
  !!FWARM && FWARM.when.toString().indexOf('pang_cover_night') >= 0 && FWARM.when.toString().indexOf('pang_listened') >= 0 && FWARM.when.toString().indexOf('pang_noodle_night') >= 0);
ok('S 註冊次序唔郁（finale_cold 排 finale 之前，冷贏暖）',
  (() => { const ids = (ENC79_BEATS.pang_siuki || []).map(b => b.id); return ids.indexOf('pang_finale_cold') >= 0 && ids.indexOf('pang_finale_cold') < ids.indexOf('pang_finale'); })());
ok('S gigs_new.json 仍係 326 張', GIGS_ARR.length === 326, 'count=' + GIGS_ARR.length);

if(fails.length){ console.log('\nFAILURES: ' + fails.length); process.exit(1); }
console.log('\nALL PASS');
