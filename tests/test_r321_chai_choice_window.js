// v20a356 resync：GRANT229 beat:chai_choice key 由「不出聲」改「婉拒畀意見」（齊 choice label 同步改），釘句同步更新。
// v20a321 齊鎮海 chai_choice（Beat 3 勸停）閘由 1992-only 放寬做 1991–1992：
//   草稿 Beat 3 閘（L993）：「T2＋1991 年」，掛鈎「N13〈站隊〉之前，1991 年」；
//   N13〈高爾夫球〉顯示 1992夏（source when "1990夏"，YEARS66＋2），live 1992 閘令次序倒轉；
//   1991 年上到 T3 嘅玩家 choice 閘死 → heart 照播，advise_stop／silent 兩個 heart 變體永久流失。
//   (S) 靜態：新閘字串逐字＋舊 1992-only 字串消失＋其餘齊線閘唔郁＋庫 326／trigger 38／BR89 19
//   (B) when() 直接判定：1991／1992 T2 開；1990 T2／1991 T1／1993 唔開
//   (C) 次序：1991 年 T3 玩家（fear 已做、choice 未做）→ picker 回 choice 唔係 heart；
//       choice 做完之後先輪到 heart（advise_stop 變體「你講中晒。」在位）；舊檔 1992 年未做 choice 照做到
//   (D) 共存：GRANT229 choice 兩行唔郁（停一停→tv_114、婉拒畀意見→tv_207）
// 用法：node tests/test_r321_chai_choice_window.js [path-to-index.html]
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
function extractObjLiteral(decl){
  const i = html.indexOf(decl);
  if(i < 0) throw new Error('decl not found: ' + decl);
  let depth = 0, j = html.indexOf('{', i);
  for(; j < html.length; j++){
    if(html[j] === '{') depth++;
    else if(html[j] === '}'){ depth--; if(depth === 0) break; }
  }
  return html.slice(html.indexOf('{', i), j + 1);
}
function extractDlg(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('missing ' + name);
  const j = html.indexOf('\nconst ', i + 10);
  return html.slice(i, j < 0 ? undefined : j);
}

/* ---- sandbox（跟 test_r318_chai_patron_truth.js） ---- */
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
const consts321 = ['ENC79_PLAYER_TIERS', 'ENC79_FAV_CAPS', 'ENC79_WEEK_SOFT_CAP', 'ENC79_STARS', 'ENC79_PILOT', 'ENC79_STAGEUP', 'ENC79_CAP_LINES', 'ENC79_WRAP_ECHO', 'ENC79_BEATS', 'ENC79_DIALOG', 'ENC79_FIRST_ALT98'].map(n => asVar(extractConst(n), n)).join('\n')
  + '\n' + asVar(extractDlg('ENC83_DLG_chai_zanhoi'), 'ENC83_DLG_chai_zanhoi')
  + '\nENC79_DIALOG["chai_zanhoi"] = ENC83_DLG_chai_zanhoi;';
const p2Start = html.indexOf('/* ---------- Phase 2 四星鏈節拍');
const p2End = html.indexOf('/* ===== ENC83 模組完 =====', p2Start);
if(p2Start < 0 || p2End < 0) throw new Error('Phase 2 beats region not found');
const p2Region = html.slice(p2Start, p2End);
const fns321 = ['enc79StarDef', 'enc79Hash', 'enc79Rand', 'enc79EnsureStars', 'enc79StarState', 'enc79TierOf', 'enc79PlayerTier', 'enc79FavCap', 'enc79AddFav', 'enc79WhisperActive', 'enc79GrantWhisper', 'enc79GrantCredit', 'enc79BoardHasStar', 'enc79BoardHasActionGig', 'enc79BeatOpen', 'enc79AnyBeatOpen', 'enc79PickBeat', 'enc79NormSeg', 'enc79BuildScript', 'enc79ChoiceFx', 'enc83NodeDone', 'enc83Flag', 'enc83HasCredit', 'enc83NewsOut', 'contra98EncFirstLocSwap', 'sideline280GrantCompletion', 'grant229Ensure', 'grant229GigById', 'grant229Record', 'grant229RecordFromEnc79'];
eval(consts321 + '\n' + asVar(extractConst('GRANT229_ENC79'), 'GRANT229_ENC79') + '\n' + p2Region + '\n' + fns321.map(extractFn).join('\n'));
var BR89_PATRON_OF_GIG = eval('(' + extractObjLiteral('const BR89_PATRON_OF_GIG = {') + ')');

/* ---- helpers ---- */
const CHOICE = beatOf('chai_zanhoi', 'chai_choice');
const FEAR = beatOf('chai_zanhoi', 'chai_fear');
const REPAY = beatOf('chai_zanhoi', 'chai_repay');
const PATRON = beatOf('chai_zanhoi', 'chai_patron');
const PATRON_COLD = beatOf('chai_zanhoi', 'chai_patron_cold');
const FINALE = beatOf('chai_zanhoi', 'chai_finale');
function hasSeg(script, seg){ return ((script && script.steps) || []).some(s => s.seg === seg); }
function hasHeartLine(script, text){ return ((script && script.steps) || []).some(s => s.seg === 'heart:chai_zanhoi' && s.text === text); }
function choiceOpen(year, season, fav){
  resetS(950); _ys = { year, season: season || '夏' };
  return CHOICE.when({ fav });
}
function setup1991T3(doneChoice, flags){
  resetS(950); _ys = { year: 1991, season: '夏' };
  setFav('chai_zanhoi', 45);
  const st = metStar('chai_zanhoi');
  st.beatsDone.chai_intel = 1;
  st.beatsDone.chai_fear = 1;
  if(doneChoice) st.beatsDone.chai_choice = 1;
  st.heartDone = false;
  Object.assign(S.flags, flags || {});
  return st;
}

/* ---------- (S) 靜態：新閘字串＋其餘齊線閘唔郁＋計數 ---------- */
ok('S choice 閘係 1991–1992＋T2（逐字）',
  html.indexOf('id:"chai_choice", when(st){ const ys=yearSeasonNow(); return ys.year>=1991 && ys.year<=1992 && enc79TierOf(st.fav)>=2; }') >= 0);
ok('S 舊 1992-only 閘字串已消失',
  html.indexOf('id:"chai_choice", when(st){ const ys=yearSeasonNow(); return ys.year===1992') < 0);
ok('S fear 閘唔郁（T1–T2＋1990–91 年窗＋N3）',
  !!FEAR && FEAR.when.toString().indexOf('ys.year>=1990 && ys.year<=1991') >= 0 &&
  FEAR.when.toString().indexOf('enc83NodeDone("N3")') >= 0);
ok('S repay 閘唔郁（T2＋＋!silent＋side 旗或 N13）',
  !!REPAY && REPAY.when.toString().indexOf('enc79TierOf(st.fav)>=2') >= 0 &&
  REPAY.when.toString().indexOf('chai_silent') >= 0 &&
  REPAY.when.toString().indexOf('enc83NodeDone("N13")') >= 0);
ok('S patron 閘唔郁（v318：T4＋truth_change＋三排除）',
  !!PATRON && PATRON.when.toString().indexOf('enc79TierOf(st.fav)>=4') >= 0 &&
  PATRON.when.toString().indexOf('chai_truth_change') >= 0 &&
  PATRON.when.toString().indexOf('chai_silent') >= 0 &&
  PATRON.when.toString().indexOf('chai_comfort') >= 0 &&
  PATRON.when.toString().indexOf('chai_loose_fear') >= 0);
ok('S patron_cold 閘唔郁（T4＋三壞旗任一）',
  !!PATRON_COLD && PATRON_COLD.when.toString().indexOf('enc79TierOf(st.fav)>=4') >= 0 &&
  PATRON_COLD.when.toString().indexOf('chai_silent') >= 0);
ok('S finale 閘唔郁（T4＋1992 冬＋patron 已播）',
  !!FINALE && FINALE.when.toString().indexOf('ys.year===1992') >= 0 &&
  FINALE.when.toString().indexOf('chai_patron') >= 0);
ok('S registry 次序唔郁（intel＜fear＜choice＜repay＜patron_cold＜patron＜finale）',
  JSON.stringify((ENC79_BEATS.chai_zanhoi || []).map(b => b.id)) === JSON.stringify(['chai_intel','chai_fear','chai_choice','chai_repay','chai_patron_cold','chai_patron','chai_finale']));
ok('S gigs 326 張／trigger 38（credit 27）／BR89 19 對',
  GIGS_ARR.length === 326 &&
  GIGS_ARR.filter(g => g.trigger && g.trigger.kind).length === 38 &&
  GIGS_ARR.filter(g => g.trigger && g.trigger.kind === 'credit').length === 27 &&
  Object.keys(BR89_PATRON_OF_GIG).length === 19,
  'gigs=' + GIGS_ARR.length + ' trig=' + GIGS_ARR.filter(g => g.trigger && g.trigger.kind).length + ' br89=' + Object.keys(BR89_PATRON_OF_GIG).length);

/* ---------- (B) when() 直接判定 ---------- */
ok('B 1991 年 T2（fav 25）→ choice 開', choiceOpen(1991, '夏', 25) === true);
ok('B 1992 年 T2（fav 25）→ choice 開', choiceOpen(1992, '夏', 25) === true);
ok('B 1990 年 T2 → choice 唔開', choiceOpen(1990, '夏', 25) === false);
ok('B 1991 年 T1（fav 10）→ choice 唔開', choiceOpen(1991, '夏', 10) === false);
ok('B 1993 年 T2 → choice 唔開', choiceOpen(1993, '夏', 25) === false);
ok('B 1991 年 T3（fav 45）→ choice 開（閘只係 T2＋）', choiceOpen(1991, '夏', 45) === true);
ok('B 1992 年 T4（fav 70）→ choice 開', choiceOpen(1992, '冬', 70) === true);

/* ---------- (C) 次序：registry 優先級＋heart 變體＋舊檔 ---------- */
ok('C 1991 年 T3 玩家（fear 已做、choice 未做）→ picker 回 choice 唔係 heart', (() => {
  setup1991T3(false);
  const picked = enc79PickBeat('chai_zanhoi');
  return picked && picked.id === 'chai_choice';
})());
ok('C 1991 年 T3 玩家 → buildScript 播 beat:chai_choice，唔播 heart', (() => {
  setup1991T3(false);
  const b = enc79BuildScript('chai_zanhoi', false);
  return hasSeg(b, 'beat:chai_choice') && !hasSeg(b, 'heart:chai_zanhoi');
})());
ok('C choice 做完之後先輪到 heart（advise_stop 變體「你講中晒。」在位）', (() => {
  setup1991T3(true, { chai_advise_stop: 1 });
  const b = enc79BuildScript('chai_zanhoi', false);
  return !hasSeg(b, 'beat:chai_choice') && hasSeg(b, 'heart:chai_zanhoi') && hasHeartLine(b, '你講中晒。');
})());
ok('C choice 做完之後 → heart 照播（無 advise_stop 嗰陣無變體句）', (() => {
  setup1991T3(true);
  const b = enc79BuildScript('chai_zanhoi', false);
  return hasSeg(b, 'heart:chai_zanhoi') && !hasHeartLine(b, '你講中晒。');
})());
ok('C 舊檔：1992 年未做 choice 嘅玩家照做到（picker 回 choice）', (() => {
  resetS(950); _ys = { year: 1992, season: '夏' };
  setFav('chai_zanhoi', 25);
  const st = metStar('chai_zanhoi');
  st.beatsDone.chai_intel = 1;
  st.beatsDone.chai_fear = 1;
  st.heartDone = false;
  const picked = enc79PickBeat('chai_zanhoi');
  return picked && picked.id === 'chai_choice';
})());
ok('C 舊檔：1991 年已做 choice 嘅玩家唔重播（beatsDone 擋住）', (() => {
  setup1991T3(true);
  return enc79PickBeat('chai_zanhoi') === null || enc79PickBeat('chai_zanhoi').id !== 'chai_choice';
})());

/* ---------- (D) 共存：GRANT229 choice 兩行唔郁 ---------- */
ok('D GRANT229 停一停→tv_114、婉拒畀意見→tv_207 唔郁',
  html.indexOf('seg:"beat:chai_choice", key:"停一停", gigId:"gig_1991_tv_114"') >= 0 &&
  html.indexOf('seg:"beat:chai_choice", key:"婉拒畀意見", gigId:"gig_1991_tv_207"') >= 0);

console.log(fails.length === 0 ? '\nALL PASS' : '\nFAILURES: ' + fails.join(' | '));
process.exit(fails.length === 0 ? 0 : 1);
