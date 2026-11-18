// v20a308 Q20 駱家聲 heart cover 版變體測試：
//   (A) cover 版：關鍵句（index 10）換成懷疑版——同一主題反面講；唔再插入舊懷疑句；行數唔變（換句唔係加句）
//   (B) 非 cover 版：heart 12 句逐字唔變；同 harmony／honest 變體疊加嗰陣，關鍵句照換（按內容搵句，唔按 index）
//   (C) 其餘兩句唔郁：Beat 5 呼應句、提攜應用句；舊插入句全檔消失
//   (D) 守住：lok_cover beat／lok_cover_first 旗／暖版閘唔郁；播完效果同暖版一樣（heartDone＋好感＋2）；舊檔唔 crash
//   (E) 靜態：source D.heart.lines 唔俾變體污染（cover 跑完再跑非 cover，逐字還原）
// 用法：node tests/test_r308_lok_heart_cover.js [path-to-index.html]
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

/* ---- sandbox（跟 test_r304_cold_heart.js；只抽 Q20 需要嘅部分） ---- */
let S;
let _ys = { year: 1992, season: '冬' };
let _doneNodes = new Set();
function resetS(day){
  S = { dayIndex: day || 0, fame: 30, money: 2000, flags: {}, npcs: { agent: 0 }, mockRumors: [], mockDebts: [], mockCredits: [], board: {}, shoots: [], mapTips: {}, story: { flags: {} }, starWeek: {}, starFavWeek: { week: -1, gain: 0 }, weekGigsDone: 0, starWhispers: {}, grant229Queue: [], pendingAud: [], news82: { pub: {}, arc: {} }, industryCreditDelta: 0 };
  _doneNodes = new Set();
  _ledger = null;
}
function setFav(sid, n){ enc79EnsureStars(); S.stars[sid].fav = n; }
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
const consts308 = ['ENC79_PLAYER_TIERS', 'ENC79_FAV_CAPS', 'ENC79_WEEK_SOFT_CAP', 'ENC79_STARS', 'ENC79_PILOT', 'ENC79_STAGEUP', 'ENC79_CAP_LINES', 'ENC79_WRAP_ECHO', 'ENC79_BEATS', 'ENC79_DIALOG', 'ENC79_FIRST_ALT98'].map(n => asVar(extractConst(n), n)).join('\n')
  + '\n' + ['ENC83_DLG_lok_gasing'].map(n => asVar(extractDlg(n), n)).join('\n')
  + '\nENC79_DIALOG["lok_gasing"] = ENC83_DLG_lok_gasing;';
const p2Start = html.indexOf('/* ---------- Phase 2 四星鏈節拍');
const p2End = html.indexOf('/* ===== ENC83 模組完 =====', p2Start);
if(p2Start < 0 || p2End < 0) throw new Error('Phase 2 beats region not found');
const p2Region = html.slice(p2Start, p2End);
const fns308 = ['enc79StarDef', 'enc79Hash', 'enc79Rand', 'enc79EnsureStars', 'enc79StarState', 'enc79TierOf', 'enc79PlayerTier', 'enc79FavCap', 'enc79AddFav', 'enc79WhisperActive', 'enc79GrantWhisper', 'enc79GrantCredit', 'enc79BoardHasStar', 'enc79BoardHasActionGig', 'enc79BeatOpen', 'enc79AnyBeatOpen', 'enc79PickBeat', 'enc79NormSeg', 'enc79BuildScript', 'enc83NodeDone', 'enc83Flag', 'enc83HasCredit', 'enc83NewsOut', 'contra98EncFirstLocSwap', 'sideline280GrantCompletion', 'grant229Ensure', 'grant229GigById', 'grant229Record', 'grant229RecordFromEnc79'];
eval(consts308 + '\n' + asVar(extractConst('GRANT229_ENC79'), 'GRANT229_ENC79') + '\n' + p2Region + '\n' + fns308.map(extractFn).join('\n'));

/* ---- helpers ---- */
const OLD_KEY = '不過呢，阿偉，歌係自己嘅，嗰種實淨，冇人攞得走。你明唔明？';
const NEW_KEY = '不過呢，阿偉，歌係自己嘅——呢句我講咗咁多年，而家先發覺，我連自己仲唱唔唱得出，都唔敢肯定。你明唔明？';
const OLD_INSERT = '呢首，我唔知仲唱唔唱得出。';
const HARMONY_Q = '呢段你聽唔聽得出我想講咩？';
const HONEST_TAIL = '有啲歌，我而家唱畀你聽，你都未必接得住。';
function heartLines(b){ return (b && b.steps || []).filter(s => s.seg === 'heart:lok_gasing' && !s.choice).map(s => s.text); }
function heartChoices(b){ const c = (b && b.steps || []).find(s => s.seg === 'heart:lok_gasing' && s.choice); return c ? c.options : null; }
function playSeg(b, seg){ (b && b.steps || []).filter(s => s.seg === seg).forEach(s => { try{ if(typeof s.segFx === 'function') s.segFx(); }catch(_e){} }); }
function build(flags){
  resetS(950); _ys = { year: 1992, season: '冬' };
  setFav('lok_gasing', 45);
  const st = doneAllBeats('lok_gasing');
  st.heartDone = false;
  Object.assign(S.flags, flags || {});
  return enc79BuildScript('lok_gasing', false);
}

/* ---------- (A) cover 版：換句唔係加句 ---------- */
let cover = build({ lok_cover_first: 1 });
let cl = heartLines(cover);
ok('A cover 版：heart 仍係 12 句（換句唔係加句）', cl.length === 12, 'lines=' + cl.length);
ok('A cover 版：關鍵句（index 10）係懷疑版', cl[10] === NEW_KEY, 'got=' + JSON.stringify(cl[10]));
ok('A cover 版：舊關鍵句唔見咗', cl.indexOf(OLD_KEY) < 0);
ok('A cover 版：舊插入句唔見咗', cl.indexOf(OLD_INSERT) < 0);
ok('A cover 版：懷疑版只出現一次', cl.filter(t => t === NEW_KEY).length === 1);
ok('A cover 版：其餘 11 句逐字唔變',
  cl.filter((t, i) => i !== 10).every((t, j) => t === ENC79_DIALOG.lok_gasing.heart.lines[j < 10 ? j : j + 1][1]));
ok('A cover 版：抉擇照在位（靜靜聽／讚好聽）',
  (() => { const o = heartChoices(cover); return o && o.length === 2 && o[0].label === '靜靜聽他彈完整首' && o[1].label === '讚他那首歌好聽'; })());
ok('A cover 版：玩家回應句（我明……唔肯改嗰幾粒音）照在位', cl[11] === '我明。唔怪得你嗌交嗌到咁大聲，都唔肯改嗰幾粒音。');

/* ---------- (B) 非 cover 版＋疊加 ---------- */
let plain = build({});
let pl = heartLines(plain);
ok('B 非 cover 版：heart 12 句逐字等於 source', pl.length === 12 && pl.every((t, i) => t === ENC79_DIALOG.lok_gasing.heart.lines[i][1]));
ok('B 非 cover 版：關鍵句係舊版、無懷疑版、無舊插入句', pl[10] === OLD_KEY && pl.indexOf(NEW_KEY) < 0 && pl.indexOf(OLD_INSERT) < 0);
let ch = build({ lok_cover_first: 1, lok_tried_harmony: 1 });
let chl = heartLines(ch);
ok('B cover＋harmony：13 句（12＋問句）', chl.length === 13, 'lines=' + chl.length);
ok('B cover＋harmony：問句喺 index 5', chl[5] === HARMONY_Q);
ok('B cover＋harmony：關鍵句照換（推後咗一行都搵得到）', chl.indexOf(NEW_KEY) === 11 && chl.indexOf(OLD_KEY) < 0 && chl.indexOf(OLD_INSERT) < 0);
let chon = build({ lok_cover_first: 1, lok_honest_not_ready: 1 });
let chonl = heartLines(chon);
ok('B cover＋honest：13 句（12＋收尾附加句）', chonl.length === 13, 'lines=' + chonl.length);
ok('B cover＋honest：收尾附加句喺最尾、關鍵句照換', chonl[12] === HONEST_TAIL && chonl.indexOf(NEW_KEY) === 10 && chonl.indexOf(OLD_KEY) < 0);
let hon = build({ lok_tried_harmony: 1 });
let honl = heartLines(hon);
ok('B harmony 單獨：13 句、關鍵句推後到 index 11 照係舊版', honl.length === 13 && honl[11] === OLD_KEY && honl.indexOf(NEW_KEY) < 0);

/* ---------- (C) 其餘兩句唔郁 ---------- */
ok('C Beat 5 呼應句唔郁（榜係人排嘅，歌係自己嘅）', html.indexOf('……榜係人排嘅，歌係自己嘅。你呢句，我收落個心度。') >= 0);
ok('C 提攜應用句唔郁（企到台中間嗰陣……企自己嘅歌上去）', html.indexOf('係，我講過。不過我話你知，企到台中間嗰陣，唱緊唔係自己嘅歌，嗰種空，冇人同你講。你唔好學我咁，要企，就企自己嘅歌上去。') >= 0);
ok('C 舊插入句全檔消失', html.indexOf(OLD_INSERT) < 0);

/* ---------- (D) 守住：beat／旗／閘／播完效果／舊檔 ---------- */
ok('D lok_cover beat 唔郁（勸佢唱住先上台先）', html.indexOf('勸佢唱住先，上咗台先再慢慢推原創') >= 0);
ok('D lok_cover_first 旗唔郁', html.indexOf('flags: ["lok_cover_first"]') >= 0);
ok('D 暖版閘唔郁（cover_first 排除暖版）', html.indexOf('warm = !!(F.lok_calm_truth) && !(F.lok_join_rant) && !(F.lok_loose_row) && !(F.lok_cover_first);') >= 0);
ok('D lok_patron_cover 閘唔郁（T4＋cover_first）', html.indexOf('id:"lok_patron_cover", when(st){ return enc79TierOf(st.fav)>=4 && (S.flags||{}).lok_cover_first') >= 0);
ok('D cover 版播完：heartDone＝true、好感＋2（45→47，同暖版一樣）',
  (() => { const b = build({ lok_cover_first: 1 }); playSeg(b, 'heart:lok_gasing'); return S.stars.lok_gasing.heartDone === true && S.stars.lok_gasing.fav === 47; })(), 'fav=' + (S.stars && S.stars.lok_gasing && S.stars.lok_gasing.fav));
ok('D 舊檔（得 fav／met、有 cover 旗）→ 唔 crash、照播懷疑版',
  (() => {
    resetS(952); _ys = { year: 1992, season: '冬' };
    S.stars = {};
    S.stars.lok_gasing = { fav: 45, met: true };
    S.flags.lok_cover_first = 1;
    enc79EnsureStars();
    for(const b2 of (ENC79_BEATS.lok_gasing || [])) S.stars.lok_gasing.beatsDone[b2.id] = 1;
    let b3 = null, err = null;
    try{ b3 = enc79BuildScript('lok_gasing', false); }catch(e){ err = e; }
    return !err && b3 && heartLines(b3).indexOf(NEW_KEY) === 10;
  })());

/* ---------- (E) source 唔污染 ---------- */
ok('E source D.heart.lines[10] 照係舊關鍵句（變體只改副本）', ENC79_DIALOG.lok_gasing.heart.lines[10][1] === OLD_KEY);
ok('E cover 跑完再跑非 cover：逐字還原舊版',
  (() => { build({ lok_cover_first: 1 }); const b = build({}); const l = heartLines(b); return l.length === 12 && l[10] === OLD_KEY && l.indexOf(NEW_KEY) < 0; })());

if(fails.length){ console.log('FAILURES: ' + fails.join(', ')); process.exit(1); }
console.log('ALL PASS');
