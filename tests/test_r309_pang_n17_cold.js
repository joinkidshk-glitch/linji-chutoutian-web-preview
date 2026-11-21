// v20a356 resync：支線複檢 (a) 類修復改咗 ENC 釘句（齊 wrap／駱 patron_cold／彭 finale_cold＋n17／程 e4／魏 heartCold／駱 heart label／彭 intel label／齊 choice GRANT key），釘句同步更新，邏輯斷言唔郁。
// v20a309 Q22 彭少祺 n17 brushed_off 冷版場面測試：
//   (A) 數據：pang_n17_cold 存在（7 句＋2 choices），對白講距離、認返 heart 嗰晚裂痕、唔抄暖版句；旁白書面語
//   (B) 分流：有 pang_brushed_off → 播冷版、唔播暖版；無旗 → 播暖版、唔播冷版；兩個選擇照出、授旗照落
//   (C) 接駁：播完冷版 → beatsDone.pang_n17 照標；再遇 → pang_finale_cold 照開、暖版 finale 唔開、sideline280 唔派（缺 pang_listened）
//   (D) 對位：冷版選擇 label 照含「雲吞麵」／「返屋企瞓」→ GRANT229 照派同一張通告、fav 照計（3／1）
//   (E) 舊檔：已有 brushed_off、beat 做晒頭兩幕嘅舊 save，唔 crash，照播冷版
//   (S) 靜態：暖版 n17 逐字唔郁；pang_finale_cold 閘／對白唔郁；gigs_new.json 仍係 330 張
// 用法：node tests/test_r309_pang_n17_cold.js [path-to-index.html]
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
  // 抽一段頂層賦值陳述式（例如 ENC79_BEATS.pang_siuki = [...]），用括號深度對位收尾
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

/* ---- sandbox（跟 test_r304_cold_heart.js） ---- */
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
const consts309 = ['ENC79_PLAYER_TIERS', 'ENC79_FAV_CAPS', 'ENC79_WEEK_SOFT_CAP', 'ENC79_STARS', 'ENC79_PILOT', 'ENC79_STAGEUP', 'ENC79_CAP_LINES', 'ENC79_WRAP_ECHO', 'ENC79_BEATS', 'ENC79_DIALOG', 'ENC79_FIRST_ALT98'].map(n => asVar(extractConst(n), n)).join('\n')
  + '\n' + asVar(extractDlg('ENC84_DLG_pang_siuki'), 'ENC84_DLG_pang_siuki')
  + '\nENC79_DIALOG["pang_siuki"] = ENC84_DLG_pang_siuki;';
const p2Start = html.indexOf('/* ---------- Phase 2 四星鏈節拍');
const p2End = html.indexOf('/* ===== ENC83 模組完 =====', p2Start);
if(p2Start < 0 || p2End < 0) throw new Error('Phase 2 beats region not found');
const p2Region = html.slice(p2Start, p2End);
const fns309 = ['enc79StarDef', 'enc79Hash', 'enc79Rand', 'enc79EnsureStars', 'enc79StarState', 'enc79TierOf', 'enc79PlayerTier', 'enc79FavCap', 'enc79AddFav', 'enc79WhisperActive', 'enc79GrantWhisper', 'enc79GrantCredit', 'enc79BoardHasStar', 'enc79BoardHasActionGig', 'enc79BeatOpen', 'enc79AnyBeatOpen', 'enc79PickBeat', 'enc79NormSeg', 'enc79BuildScript', 'enc79ChoiceFx', 'enc83NodeDone', 'enc83Flag', 'enc83HasCredit', 'enc83NewsOut', 'contra98EncFirstLocSwap', 'sideline280GrantCompletion', 'grant229Ensure', 'grant229GigById', 'grant229Record', 'grant229RecordFromEnc79'];
eval(consts309 + '\n' + asVar(extractConst('GRANT229_ENC79'), 'GRANT229_ENC79') + '\n' + p2Region + '\n' + extractAssign('ENC79_BEATS.pang_siuki = [') + '\n' + fns309.map(extractFn).join('\n'));

/* ---- helpers ---- */
function hasText(b, sub){ return (b && b.steps || []).some(s => String(s.text || '').indexOf(sub) >= 0); }
function segSteps(b, seg){ return (b && b.steps || []).filter(s => s.seg === seg); }
function playSeg(b, seg){ segSteps(b, seg).forEach(s => { try{ if(typeof s.segFx === 'function') s.segFx(); }catch(_e){} }); }
function choiceStep(b, seg){ return (b && b.steps || []).find(s => s.choice && s.seg === seg); }
function build(flags, fav){
  resetS(950); _ys = { year: 1992, season: '冬' };
  setFav('pang_siuki', fav || 45);
  const st = metStar('pang_siuki');
  // 頭兩幕已做；pang_n17、pang_finale_cold、pang_finale 留返唔標——n17 係今次要播嗰幕，
  // finale_cold 係播完 n17 之後要驗嗰幕，finale 係要驗閘唔開嗰幕（標咗做完會令 BeatOpen
  // 為錯嘅原因回 false）。註冊次序保證 pickBeat 先揀到 pang_n17。
  for(const b of (ENC79_BEATS.pang_siuki || [])) if(b.id !== 'pang_n17' && b.id !== 'pang_finale_cold' && b.id !== 'pang_finale') st.beatsDone[b.id] = 1;
  Object.assign(S.flags, flags || {});
  return enc79BuildScript('pang_siuki', false);
}

const WARM_LINES = [
  '阿偉！你嚟到啦，我喺後台咁多人入面，第一眼就見到你。',
  '一九九二年年底頒獎禮後台，人頭湧湧，彭少祺穿著司儀禮服，手持咪牌，第一個走過來跟阿偉打招呼。',
  '記唔記得嗰陣喺大騷後台？你企喺後台門口嗰堆臨記入面，我叫你個名，你嚇到彈起。',
  '點會唔記得呀彭生，嗰日我返到屋企仲諗，點解你會記得我呢啲細角色。',
  '而家唔同晒啦，今晚你企到嚟呢度，係嘉賓席嗰邊入場㗎啦，我喺台上讀到你個名嗰陣，都替你驕傲。',
  '冇你嗰陣時時提點，我都唔知自己行唔行到嚟呢一步。',
  '係你自己捱出嚟㗎，我只係嗌過你幾次名啫。嚟，陣間完騷，老地方食雲吞麵，慶祝下。'
];

/* ---------- (A) 數據形狀＋對白內容 ---------- */
const D = ENC79_DIALOG.pang_siuki;
ok('A pang_n17_cold 存在（7 句＋2 choices）',
  !!D && !!D.beats && !!D.beats.pang_n17_cold && Array.isArray(D.beats.pang_n17_cold.lines) && D.beats.pang_n17_cold.lines.length === 7 && Array.isArray(D.beats.pang_n17_cold.choices) && D.beats.pang_n17_cold.choices.length === 2,
  'lines=' + (D && D.beats && D.beats.pang_n17_cold && D.beats.pang_n17_cold.lines && D.beats.pang_n17_cold.lines.length));
ok('A cold 句句有講者（S／A／N）',
  !!D && D.beats.pang_n17_cold.lines.every(ln => Array.isArray(ln) && (ln[0] === 'S' || ln[0] === 'A' || ln[0] === 'N') && typeof ln[1] === 'string' && ln[1].length > 0));
ok('A cold 旁白（N 句）係書面語，無廣東話口語字（㗎／咗／唔／嘅／喇／啲／嗰）',
  !!D && D.beats.pang_n17_cold.lines.filter(ln => ln[0] === 'N').every(ln => !/[㗎咗唔嘅喇啲嗰]/.test(ln[1])));
const coldSteps = { steps: D.beats.pang_n17_cold.lines.map(l => ({ text: l[1] })) };
ok('A cold 講距離：佢同每個人打招呼、唯獨唔再望向阿偉、連頭都冇回',
  hasText(coldSteps, '跟每一個人打招呼') && hasText(coldSteps, '唯獨沒有再望向自己') && hasText(coldSteps, '連頭也沒有回'));
ok('A cold 認返 heart 嗰晚裂痕：笑住話佢諗多咗、臉色僵了一下',
  hasText(coldSteps, '笑著說對方想多了') && hasText(coldSteps, '臉色僵了一下')); /* v20a358 (b) 潤飾：人稱講明 */
ok('A cold 唔用暖版關鍵句（第一眼就見到你／第一個走過來／嘉賓席／老地方食雲吞麵，慶祝下）',
  !hasText(coldSteps, '第一眼就見到你') && !hasText(coldSteps, '第一個走過來') && !hasText(coldSteps, '嘉賓席') && !hasText(coldSteps, '慶祝下'));
const coldTexts = new Set(D.beats.pang_n17_cold.lines.map(l => l[1]));
const warmTexts = new Set(D.beats.pang_n17.lines.map(l => l[1]));
const overlap = [...coldTexts].filter(t => warmTexts.has(t));
ok('A cold 主線 7 句同暖版零逐句重用（唔可以直接用暖版對白）', overlap.length === 0, 'overlap=' + JSON.stringify(overlap));

/* ---------- (B) 暖／冷分流＋兩個選擇 ---------- */
const cold = build({ pang_brushed_off: 1 });
ok('B 有 brushed_off → 播冷版（beat:pang_n17 7 句對白＋1 抉擇步，含冷版關鍵句）',
  cold && segSteps(cold, 'beat:pang_n17').filter(s => !s.choice).length === 7 && hasText(cold, '唯獨沒有再望向自己') && hasText(cold, '臉色僵了一下'),
  'lineSegs=' + segSteps(cold, 'beat:pang_n17').filter(s => !s.choice).length);
ok('B 有 brushed_off → 唔播暖版句（第一眼就見到你／第一個走過來）',
  cold && !hasText(cold, '第一眼就見到你') && !hasText(cold, '第一個走過來'));
const coldChoice = choiceStep(cold, 'beat:pang_n17');
ok('B 冷版兩個選擇照出（雲吞麵／返屋企瞓），授旗同暖版一樣',
  !!coldChoice && Array.isArray(coldChoice.options) && coldChoice.options.length === 2 &&
  coldChoice.options[0].label.indexOf('雲吞麵') >= 0 && JSON.stringify(coldChoice.options[0].flags) === JSON.stringify(['pang_noodle_night']) &&
  coldChoice.options[1].label.indexOf('返屋企瞓') >= 0 && JSON.stringify(coldChoice.options[1].flags) === JSON.stringify(['pang_early_night']),
  'labels=' + (coldChoice && coldChoice.options && coldChoice.options.map(o => o.label).join('｜')));
const warm = build({});
ok('B 無旗 → 播暖版（beat:pang_n17 7 句對白＋1 抉擇步，含第一眼就見到你）、唔播冷版句',
  warm && segSteps(warm, 'beat:pang_n17').filter(s => !s.choice).length === 7 && hasText(warm, '第一眼就見到你') && !hasText(warm, '唯獨沒有再望向自己') && !hasText(warm, '臉色僵了一下'),
  'lineSegs=' + segSteps(warm, 'beat:pang_n17').filter(s => !s.choice).length);
const warmChoice = choiceStep(warm, 'beat:pang_n17');
ok('B 暖版兩個選擇照舊（label＋授旗唔郁）',
  !!warmChoice && warmChoice.options[0].label === '去廟街吃一碗雲吞麵，陪他坐下' && JSON.stringify(warmChoice.options[0].flags) === JSON.stringify(['pang_noodle_night']) &&
  warmChoice.options[1].label === '趕住返屋企瞓，聽日仲有工開' && JSON.stringify(warmChoice.options[1].flags) === JSON.stringify(['pang_early_night']));

/* ---------- (C) 播完接駁 ---------- */
ok('C 播完冷版 segFx → beatsDone.pang_n17 照標（收尾閘讀呢個）',
  (() => { const b = build({ pang_brushed_off: 1 }); playSeg(b, 'beat:pang_n17'); return !!(S.stars.pang_siuki.beatsDone || {}).pang_n17; })());
ok('C 冷版 n17 之後再遇 → pang_finale_cold 照開（pickBeat）',
  (() => { const b = build({ pang_brushed_off: 1 }); playSeg(b, 'beat:pang_n17'); const b2 = enc79BuildScript('pang_siuki', false); return !!b2 && hasText(b2, '阿偉一早到了，叫了一碗雲吞麵，坐著等') && b2.steps.some(s => s.seg === 'beat:pang_finale_cold'); })());
ok('C 冷版玩家唔會誤入暖版收尾（缺 pang_listened，pang_finale 閘唔開）',
  (() => { const b = build({ pang_brushed_off: 1 }); playSeg(b, 'beat:pang_n17'); S.flags.pang_noodle_night = 1; return enc79BeatOpen('pang_siuki', beatOf('pang_siuki', 'pang_finale')) === false; })());
ok('C 冷版 n17 唔派暖線收尾獎勵（sideline280：缺 pang_listened，聲望唔郁）',
  (() => { const b = build({ pang_brushed_off: 1 }); const before = S.fame; playSeg(b, 'beat:pang_n17'); return S.fame === before && !S.flags.sideline280_pang; })());

/* ---------- (D) GRANT229＋fav 對位 ---------- */
resetS(950);
ok('D 冷版雲吞麵 label → GRANT229 照派 gig_1991_ad_107（同暖版一樣）',
  grant229RecordFromEnc79('beat:pang_n17', '自己去廟街食碗雲吞麵，坐低等佢') === true && S.grant229Queue.some(q => q.gigId === 'gig_1991_ad_107'),
  'queue=' + JSON.stringify(S.grant229Queue.map(q => q.gigId)));
resetS(950);
ok('D 冷版返屋企瞓 label → GRANT229 照派 gig_1992_tv_301（同暖版一樣）',
  grant229RecordFromEnc79('beat:pang_n17', '趕住返屋企瞓，聽日仲有工開') === true && S.grant229Queue.some(q => q.gigId === 'gig_1992_tv_301'),
  'queue=' + JSON.stringify(S.grant229Queue.map(q => q.gigId)));
ok('D 冷版雲吞麵選擇 fav＋3（enc79ChoiceFx 同暖版一樣）',
  enc79ChoiceFx('beat:pang_n17', '自己去廟街食碗雲吞麵，坐低等佢').fav === 3);
ok('D 冷版返屋企瞓選擇 fav＋1（enc79ChoiceFx 同暖版一樣）',
  enc79ChoiceFx('beat:pang_n17', '趕住返屋企瞓，聽日仲有工開').fav === 1);

/* ---------- (E) 舊檔 ---------- */
ok('E 舊檔（fav／met＋頭兩幕已做＋brushed_off）唔 crash，照播冷版',
  (() => {
    resetS(950); _ys = { year: 1992, season: '冬' };
    S.stars = { pang_siuki: { fav: 45, met: true, beatsDone: { pang_intel: 1, pang_help: 1 } } };
    S.flags.pang_brushed_off = 1;
    let b = null, err = null;
    try{ b = enc79BuildScript('pang_siuki', false); }catch(e){ err = e; }
    return !err && !!b && hasText(b, '唯獨沒有再望向自己');
  })());

/* ---------- (S) 靜態：暖版／收尾唔郁 ---------- */
ok('S 暖版 pang_n17 7 句逐字唔郁',
  JSON.stringify(D.beats.pang_n17.lines.map(l => l[1])) === JSON.stringify(WARM_LINES));
ok('S 暖版 pang_n17 兩個選擇逐字唔郁',
  D.beats.pang_n17.choices[0].label === '去廟街吃一碗雲吞麵，陪他坐下' && D.beats.pang_n17.choices[1].label === '趕住返屋企瞓，聽日仲有工開' &&
  D.beats.pang_n17.choices[0].lines[1][1] === '辛苦咩啫，今晚食碗麵，唔使講笑話，坐低慢慢講。');
ok('S pang_n17 註冊閘唔郁（tier≥3＋1992 冬，無旗條件）',
  (() => { const w = beatOf('pang_siuki', 'pang_n17').when.toString(); return w.indexOf('1992') >= 0 && w.indexOf('冬') >= 0 && w.indexOf('brushed_off') < 0; })());
ok('S pang_finale_cold 閘唔郁（n17 做完＋absent／brushed_off／early_night 三旗）',
  (() => { const w = beatOf('pang_siuki', 'pang_finale_cold').when.toString(); return w.indexOf('pang_n17') >= 0 && w.indexOf('pang_absent_night') >= 0 && w.indexOf('pang_brushed_off') >= 0 && w.indexOf('pang_early_night') >= 0; })());
ok('S pang_finale_cold 對白唔郁（阿偉先到開場在位）',
  hasText({ steps: D.beats.pang_finale_cold.lines.map(l => ({ text: l[1] })) }, '阿偉一早到了，叫了一碗雲吞麵，坐著等'));
ok('S gigs_new.json 仍係 330 張', GIGS_ARR.length === 330, 'count=' + GIGS_ARR.length);

if(fails.length){ console.log('\nFAILURES: ' + fails.length); process.exit(1); }
console.log('\nALL PASS');
