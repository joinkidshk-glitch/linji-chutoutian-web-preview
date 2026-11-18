// v20a310 Q23 程天諾 ching_e4 N15 旗變體測試（PLAN §9 Beat 3 逐字稿）：
//   (A) 數據：ching_e4 開場 8 句逐字、2 choices（label＋授旗唔郁）
//   (B) 苦練旗＋揀撐練 → 信任句「你嗰晚都係咁揀，我信你。」行先，再接原本「今晚唔停」
//   (C) 修音旗＋揀撐練 → 頂返句「你嗰晚都係靠部機交帶㗎，咁你而家係教我練，定教我執呀？」取代原本應承
//   (D) 無旗＋揀撐練 → 原回應；紅咗先算嗰邊任何旗都唔變
//   (E) 接駁：label／授旗／GRANT229／fav 唔郁；變體唔寫入 DLG 定義（重播無旗回復原樣）
//   (F) 舊檔：已有 N15 旗嘅舊 save 唔 crash，照播變體
//   (S) 靜態：開場 8 句、兩選擇 label、e4 註冊閘、after_train／after_polish 閘唔郁；gigs_new.json 仍係 306 張
// 用法：node tests/test_r310_ching_e4_n15.js [path-to-index.html]
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
const consts310 = ['ENC79_PLAYER_TIERS', 'ENC79_FAV_CAPS', 'ENC79_WEEK_SOFT_CAP', 'ENC79_STARS', 'ENC79_PILOT', 'ENC79_STAGEUP', 'ENC79_CAP_LINES', 'ENC79_WRAP_ECHO', 'ENC79_BEATS', 'ENC79_DIALOG', 'ENC79_FIRST_ALT98'].map(n => asVar(extractConst(n), n)).join('\n')
  + '\n' + asVar(extractDlg('ENC84_DLG_ching_tinlok'), 'ENC84_DLG_ching_tinlok')
  + '\nENC79_DIALOG["ching_tinlok"] = ENC84_DLG_ching_tinlok;';
const p2Start = html.indexOf('/* ---------- Phase 2 四星鏈節拍');
const p2End = html.indexOf('/* ===== ENC83 模組完 =====', p2Start);
if(p2Start < 0 || p2End < 0) throw new Error('Phase 2 beats region not found');
const p2Region = html.slice(p2Start, p2End);
const fns310 = ['enc79StarDef', 'enc79Hash', 'enc79Rand', 'enc79EnsureStars', 'enc79StarState', 'enc79TierOf', 'enc79PlayerTier', 'enc79FavCap', 'enc79AddFav', 'enc79WhisperActive', 'enc79GrantWhisper', 'enc79GrantCredit', 'enc79BoardHasStar', 'enc79BoardHasActionGig', 'enc79BeatOpen', 'enc79AnyBeatOpen', 'enc79PickBeat', 'enc79NormSeg', 'enc79BuildScript', 'enc79ChoiceFx', 'enc83NodeDone', 'enc83Flag', 'enc83HasCredit', 'enc83NewsOut', 'contra98EncFirstLocSwap', 'sideline280GrantCompletion', 'grant229Ensure', 'grant229GigById', 'grant229Record', 'grant229RecordFromEnc79'];
eval(consts310 + '\n' + asVar(extractConst('GRANT229_ENC79'), 'GRANT229_ENC79') + '\n' + p2Region + '\n' + extractAssign('ENC79_BEATS.ching_tinlok = [') + '\n' + fns310.map(extractFn).join('\n'));

/* ---- helpers ---- */
function hasText(b, sub){ return (b && b.steps || []).some(s => String(s.text || '').indexOf(sub) >= 0); }
function segSteps(b, seg){ return (b && b.steps || []).filter(s => s.seg === seg); }
function playSeg(b, seg){ segSteps(b, seg).forEach(s => { try{ if(typeof s.segFx === 'function') s.segFx(); }catch(_e){} }); }
function choiceStep(b, seg){ return (b && b.steps || []).find(s => s.choice && s.seg === seg); }
function build(flags, fav){
  resetS(950); _ys = { year: 1992, season: '冬' };
  setFav('ching_tinlok', fav || 20);
  const st = metStar('ching_tinlok');
  // 只留 ching_e4 未做——e4 係今次要播嗰幕；其餘 beat 標晒做完，免 pickBeat 行差
  for(const b of (ENC79_BEATS.ching_tinlok || [])) if(b.id !== 'ching_e4') st.beatsDone[b.id] = 1;
  Object.assign(S.flags, flags || {});
  return enc79BuildScript('ching_tinlok', false);
}

const OPENING_LINES = [
  '1992年，天星音樂舞蹈室，程天諾拿著一份報紙進來，走來走去，笑又不是，哭又不是。',
  '阿偉，你睇咗報紙未呀？『城中四子』呀，我個名……同陸柏言擺埋一齊呀，仲有嗰兩位前輩歌手。',
  '睇到喇，頭版咁大，你今次真係上咗位喇。',
  '我開心㗎，真係開心。但我一諗到要同柏言哥佢哋並列，我就驚……我夠唔夠班呀？我唱嗰瓣，仲未掂㗎。',
  '出面仲有人問，點解冇駱家聲份……我聽到都唔好意思，家聲哥唱功好過我咁多，點會輪到我先呀？',
  '你識咁諗，已經唔係嗰啲紅咗就飄嘅人喇。個名上咗報紙，功夫就要追得上個名，知唔知？',
  '知！我今晚加操，唱嗰課，練多一個鐘。人哋俾咗個位我，我唔可以丟人哋架。',
  '（呢個後生，紅到咁都仲識驚，佢跌唔落去㗎喇。）'
];
const TRAIN_TRUST = '你嗰晚都係咁揀，我信你。';
const POLISH_RETORT = '你嗰晚都係靠部機交帶㗎，咁你而家係教我練，定教我執呀？';
const ORIG_ACCEPT = '好！咁我今晚唔停，唱嗰課練多一個鐘，你唔准走！';
const ORIG_PLAYER = '天諾，個名上咗報紙，功夫就要追得上個名。你今晚加操嗰一個鐘，我陪你。你唱，我聽住。';
const ORIG_POLISH_PLAYER = '天諾，唔好諗咁多喇，呢行機會唔等人㗎，紅咗先算啦。紅咗，你想點練都仲有機會㗎。';
const ORIG_POLISH_REPLY = '……係嘅，紅咗先算。你講得啱，係我諗多咗。今晚唔講喇，我去沖個涼先。';

/* ---------- (A) 數據形狀＋開場 ---------- */
const D = ENC79_DIALOG.ching_tinlok;
ok('A ching_e4 存在（開場 8 句＋2 choices）',
  !!D && !!D.beats && !!D.beats.ching_e4 && Array.isArray(D.beats.ching_e4.lines) && D.beats.ching_e4.lines.length === 8 && Array.isArray(D.beats.ching_e4.choices) && D.beats.ching_e4.choices.length === 2,
  'lines=' + (D && D.beats && D.beats.ching_e4 && D.beats.ching_e4.lines && D.beats.ching_e4.lines.length));
ok('A 開場 8 句逐字唔郁（城中四子報紙 setup）',
  JSON.stringify(D.beats.ching_e4.lines.map(l => l[1])) === JSON.stringify(OPENING_LINES));
ok('A 兩個選擇 label 逐字唔郁',
  D.beats.ching_e4.choices[0].label === '撐佢練真功夫：個名上咗報紙，功夫就要追得上個名' &&
  D.beats.ching_e4.choices[1].label === '叫佢紅咗先算：執聲有咩所謂，紅咗先算');
ok('A 兩個選擇授旗唔郁（ching_back_train／ching_back_polish）',
  JSON.stringify(D.beats.ching_e4.choices[0].flags) === JSON.stringify(['ching_back_train']) &&
  JSON.stringify(D.beats.ching_e4.choices[1].flags) === JSON.stringify(['ching_back_polish']));

/* ---------- (B) 苦練旗變體 ---------- */
const train = build({ flag_vocal_train: 1 });
ok('B 苦練旗 → 播 e4（beat:ching_e4 8 句開場＋1 抉擇步）',
  train && segSteps(train, 'beat:ching_e4').filter(s => !s.choice).length === 8,
  'lineSegs=' + segSteps(train, 'beat:ching_e4').filter(s => !s.choice).length);
ok('B 苦練旗 → 開場 8 句照舊（無開場插入，報紙 setup 唔打斷）',
  train && JSON.stringify(segSteps(train, 'beat:ching_e4').filter(s => !s.choice).map(s => s.text)) === JSON.stringify(OPENING_LINES));
const trainChoice = choiceStep(train, 'beat:ching_e4');
ok('B 苦練旗＋撐練 → 3 句：玩家原句＋信任句＋原本「今晚唔停」',
  !!trainChoice && trainChoice.options[0].lines.length === 3 &&
  trainChoice.options[0].lines[0][1] === ORIG_PLAYER &&
  trainChoice.options[0].lines[1][0] === 'S' && trainChoice.options[0].lines[1][1] === TRAIN_TRUST &&
  trainChoice.options[0].lines[2][1] === ORIG_ACCEPT,
  'lines=' + JSON.stringify(trainChoice && trainChoice.options[0].lines.map(l => l[1])));
ok('B 苦練旗＋撐練 → 信任句行先（「今晚唔停」之前），唔係收尾附加',
  !!trainChoice && trainChoice.options[0].lines[1][1] === TRAIN_TRUST && trainChoice.options[0].lines[2][1] === ORIG_ACCEPT);
ok('B 苦練旗 → 紅咗先算嗰邊原樣（玩家原句＋原本應承，唔加變體）',
  !!trainChoice && trainChoice.options[1].lines.length === 2 &&
  trainChoice.options[1].lines[0][1] === ORIG_POLISH_PLAYER && trainChoice.options[1].lines[1][1] === ORIG_POLISH_REPLY);

/* ---------- (C) 修音旗變體 ---------- */
const polish = build({ flag_vocal_polish: 1 });
const polishChoice = choiceStep(polish, 'beat:ching_e4');
ok('C 修音旗＋撐練 → 2 句：玩家原句＋頂返句，取代原本應承',
  !!polishChoice && polishChoice.options[0].lines.length === 2 &&
  polishChoice.options[0].lines[0][1] === ORIG_PLAYER &&
  polishChoice.options[0].lines[1][0] === 'S' && polishChoice.options[0].lines[1][1] === POLISH_RETORT,
  'lines=' + JSON.stringify(polishChoice && polishChoice.options[0].lines.map(l => l[1])));
ok('C 修音旗＋撐練 → 原本「今晚唔停」唔再出現',
  !!polishChoice && !polishChoice.options[0].lines.some(l => l[1] === ORIG_ACCEPT));
ok('C 修音旗 → 紅咗先算嗰邊原樣（唔加變體）',
  !!polishChoice && polishChoice.options[1].lines.length === 2 &&
  polishChoice.options[1].lines[0][1] === ORIG_POLISH_PLAYER && polishChoice.options[1].lines[1][1] === ORIG_POLISH_REPLY);

/* ---------- (D) 無旗原樣 ---------- */
const plain = build({});
const plainChoice = choiceStep(plain, 'beat:ching_e4');
ok('D 無旗 → 撐練原回應 2 句（玩家原句＋原本「今晚唔停」），無信任句／頂返句',
  !!plainChoice && plainChoice.options[0].lines.length === 2 &&
  plainChoice.options[0].lines[0][1] === ORIG_PLAYER && plainChoice.options[0].lines[1][1] === ORIG_ACCEPT &&
  !hasText(plain, TRAIN_TRUST) && !hasText(plain, POLISH_RETORT));
ok('D 無旗 → 紅咗先算原回應 2 句',
  !!plainChoice && plainChoice.options[1].lines.length === 2 &&
  plainChoice.options[1].lines[0][1] === ORIG_POLISH_PLAYER && plainChoice.options[1].lines[1][1] === ORIG_POLISH_REPLY);

/* ---------- (E) 接駁：授旗／即派／fav／定義唔郁 ---------- */
ok('E 變體嗰陣授旗照舊（撐練 ching_back_train／紅咗先算 ching_back_polish）',
  !!trainChoice && JSON.stringify(trainChoice.options[0].flags) === JSON.stringify(['ching_back_train']) &&
  JSON.stringify(trainChoice.options[1].flags) === JSON.stringify(['ching_back_polish']) &&
  !!polishChoice && JSON.stringify(polishChoice.options[0].flags) === JSON.stringify(['ching_back_train']));
ok('E 撐練選擇 fav＋5（enc79ChoiceFx，同原版一樣）',
  enc79ChoiceFx('beat:ching_e4', '撐佢練真功夫：個名上咗報紙，功夫就要追得上個名').fav === 5);
ok('E 紅咗先算選擇 fav＋1（enc79ChoiceFx，同原版一樣）',
  enc79ChoiceFx('beat:ching_e4', '叫佢紅咗先算：執聲有咩所謂，紅咗先算').fav === 1);
resetS(950);
ok('E 撐練 label → GRANT229 照派 gig_1992_rec_107《霓虹舞影》MV 男主角',
  grant229RecordFromEnc79('beat:ching_e4', '撐佢練真功夫：個名上咗報紙，功夫就要追得上個名') === true && S.grant229Queue.some(q => q.gigId === 'gig_1992_rec_107'),
  'queue=' + JSON.stringify(S.grant229Queue.map(q => q.gigId)));
resetS(950);
ok('E 紅咗先算 label → GRANT229 照派 gig_1992_ad_105',
  grant229RecordFromEnc79('beat:ching_e4', '叫佢紅咗先算：執聲有咩所謂，紅咗先算') === true && S.grant229Queue.some(q => q.gigId === 'gig_1992_ad_105'),
  'queue=' + JSON.stringify(S.grant229Queue.map(q => q.gigId)));
ok('E 播完 e4 segFx → beatsDone.ching_e4 照標',
  (() => { const b = build({ flag_vocal_train: 1 }); playSeg(b, 'beat:ching_e4'); return !!(S.stars.ching_tinlok.beatsDone || {}).ching_e4; })());
ok('E 變體唔寫入 DLG 定義：苦練 build 之後，定義原樣（撐練仍係 2 句）；再 build 無旗回復原樣',
  (() => {
    build({ flag_vocal_train: 1 });
    const defOk = D.beats.ching_e4.choices[0].lines.length === 2 && D.beats.ching_e4.choices[0].lines[1][1] === ORIG_ACCEPT;
    const b2 = build({});
    const c2 = choiceStep(b2, 'beat:ching_e4');
    return defOk && !!c2 && c2.options[0].lines.length === 2 && c2.options[0].lines[1][1] === ORIG_ACCEPT;
  })());

/* ---------- (F) 舊檔 ---------- */
ok('F 舊檔（fav／met＋其餘 beat 已做＋N15 苦練旗）唔 crash，照播變體',
  (() => {
    resetS(950); _ys = { year: 1992, season: '冬' };
    S.stars = { ching_tinlok: { fav: 20, met: true, beatsDone: { ching_rival: 1, ching_after_train: 1, ching_after_polish: 1, ching_patron_cold: 1, ching_patron: 1 } } };
    S.flags.flag_vocal_train = 1;
    let b = null, err = null;
    try{ b = enc79BuildScript('ching_tinlok', false); }catch(e){ err = e; }
    const c = b && choiceStep(b, 'beat:ching_e4');
    return !err && !!b && !!c && c.options[0].lines.some(l => l[1] === TRAIN_TRUST) && c.options[0].lines.some(l => l[1] === ORIG_ACCEPT);
  })());
ok('F 舊檔修音旗（S.story.flags 讀法）照播頂返句',
  (() => {
    resetS(950); _ys = { year: 1992, season: '冬' };
    S.stars = { ching_tinlok: { fav: 20, met: true, beatsDone: { ching_rival: 1, ching_after_train: 1, ching_after_polish: 1, ching_patron_cold: 1, ching_patron: 1 } } };
    S.story.flags.flag_vocal_polish = 1;
    let b = null, err = null;
    try{ b = enc79BuildScript('ching_tinlok', false); }catch(e){ err = e; }
    const c = b && choiceStep(b, 'beat:ching_e4');
    return !err && !!b && !!c && c.options[0].lines.some(l => l[1] === POLISH_RETORT) && !c.options[0].lines.some(l => l[1] === ORIG_ACCEPT);
  })());

/* ---------- (S) 靜態：其餘唔郁 ---------- */
ok('S ching_e4 註冊閘唔郁（tier≥1＋enc83NewsOut("E4")）',
  (() => { const w = beatOf('ching_tinlok', 'ching_e4').when.toString(); return w.indexOf('enc83NewsOut("E4")') >= 0 && w.indexOf('flag_vocal') < 0; })());
ok('S ching_after_train／after_polish 閘唔郁（N15 做完＋對應旗）',
  (() => {
    const wt = beatOf('ching_tinlok', 'ching_after_train').when.toString();
    const wp = beatOf('ching_tinlok', 'ching_after_polish').when.toString();
    return wt.indexOf('flag_vocal_train') >= 0 && wp.indexOf('flag_vocal_polish') >= 0;
  })());
ok('S ching_e4 抉擇後對白只喺 buildScript 分流，唔係開場插入（開場無信任句／頂返句）',
  !OPENING_LINES.some(t => t === TRAIN_TRUST || t === POLISH_RETORT));
ok('S gigs_new.json 仍係 306 張', GIGS_ARR.length === 306, 'count=' + GIGS_ARR.length);

if(fails.length){ console.log('\nFAILURES: ' + fails.length); process.exit(1); }
console.log('\nALL PASS');
