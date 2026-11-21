// v20a322 駱家聲 lok_stand_original 加軟條件讀者——lok_patron 引薦句變體：
//   lok_stand_original 授出（lok_cover 抉擇 A「勸佢企硬」）之後全檔 0 讀者；v314 殘留已結案——
//   絕對唔加落任何閘（cover 窗口得 1991 年冬一季，加閘會鎖死遲遇／T1／T4 玩家＋舊存檔，
//   兼同收尾獎勵判定再脫鈎）。呢票只加一句引薦變體，跟 v278 寫法一式一樣：
//   (S) 靜態：回call 句在位＋閘／獎勵判定／heard-praised 變體逐字唔郁＋計數
//   (B) 行為：有旗 → patron 多 1 句回call（第 3 句之後）；無旗 → 6 句原樣；
//       stand＋heard／praised 共存 → 兩句變體、回call 行先；冷版／翻唱版唔插呢句
// 用法：node tests/test_r322_lok_stand_variant.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const GIGS_NEW = require('../content/gigs_new.json');
const GIGS_ARR = Array.isArray(GIGS_NEW) ? GIGS_NEW : (GIGS_NEW.gigs || []);
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }
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

/* ---- sandbox（跟 test_sideline278_logic.js） ---- */
let S;
let _ys = { year: 1992, season: '冬' };
let _doneNodes = new Set();
function resetS(day){
  S = { dayIndex: day||0, fame: 0, money: 2000, flags: {}, npcs: { agent: 0 }, mockRumors: [], mockDebts: [], mockCredits: [], board: {}, shoots: [], mapTips: {}, story: { flags: {} }, starWeek: {}, weekGigsDone: 0, starWhispers: {}, grant229Queue: [], pendingAud: [], news82: { pub: {}, arc: {} } };
  _doneNodes = new Set();
  _ledger = null;
}
function setFav(sid, n){ enc79EnsureStars(); S.stars[sid].fav = n; }
function beatOf(sid, id){ return (ENC79_BEATS[sid] || []).find(b => b.id === id); }
function metStar(sid){ enc79EnsureStars(); S.stars[sid].met = true; return S.stars[sid]; }
function weekNumNow(){ return 3; }
function yearSeasonNow(){ return _ys; }
function enc87StoryFlag(f){ return !!((S.flags && S.flags[f]) || (S.story && S.story.flags && S.story.flags[f])); }
function ensureMockJournal(){ if(!Array.isArray(S.mockRumors)) S.mockRumors=[]; if(!Array.isArray(S.mockDebts)) S.mockDebts=[]; }
function syncNotebookMirror(){}
function saveQ(){}
function refreshMoneyHud(){}
function noteWeekHighlight(){}
function rumorStateLabel(state){ return '剛聽聞'; }
function R(a,b){ return a; }
function bumpNpc(id, d){ const b = S.npcs[id]||0; S.npcs[id] = Math.min(100, b+d); return S.npcs[id]-b; }
function toast(){}
function enc79LocName(id){ return id; }
function canAudition(gig){ return { ok: true }; }
let _ledger = null;
function ensureFavorLedger(){ if(!_ledger) _ledger = { settled:0, credits:0, exodus:[], counted:{} }; return _ledger; }
function favorLedgerNoteCredit(id){ const L = ensureFavorLedger(); if(L.counted[id]) return false; L.counted[id]={kind:'credit'}; L.credits++; return true; }
function softSocialDailyCap(){ return { ok:true, used:0, max:99, left:99 }; }
function softSocialDailyUse(){}
function softPreviewOn(){ return false; }
function ending78Gate(){ return false; }
function npcNextTierHint(){ return null; }
const BehaviorGate = { featureFlag_softBehaviorGatePreview: ()=>false };
const StoryOC = {
  isDone: (id)=> _doneNodes.has(id),
  listOpen: ()=>({ open: [] }),
  findNodeRaw: (id)=>({ id }),
};
function storyNodeLocId(n){ return n && n.__loc; }
function enc79PlayEncounter(){}
var GIGS = GIGS_ARR;

const asVar = (code, name)=> code.replace('const ' + name + ' =', 'var ' + name + ' =');
const consts322 = ['ENC79_TIER_NAMES','ENC79_PLAYER_TIERS','ENC79_FAV_CAPS','ENC79_STARS','ENC79_PILOT','ENC79_STAGEUP','ENC79_CAP_LINES','ENC79_WRAP_ECHO','ENC79_BEATS','ENC79_DIALOG','ENC79_FIRST_ALT98'].map(n=> asVar(extractConst(n), n)).join('\n')
  + '\n' + ['ENC79_DLG_luk_baakyin','ENC79_DLG_liu_bingxing','ENC79_DLG_mak_zhendong'].map(n=> asVar(extractDlg(n), n)).join('\n')
  + '\n' + ['ENC83_DLG_gu_mingfai','ENC83_DLG_lok_gasing','ENC83_DLG_ngai_wingnaam','ENC83_DLG_chai_zanhoi'].map(n=> asVar(extractDlg(n), n)).join('\n')
  + '\n' + ['ENC84_DLG_pang_siuki','ENC84_DLG_so_jiyan','ENC84_DLG_chung_choning','ENC84_DLG_ching_tinlok'].map(n=> asVar(extractDlg(n), n)).join('\n')
  + '\nENC79_DIALOG["luk_baakyin"] = ENC79_DLG_luk_baakyin;\nENC79_DIALOG["liu_bingxing"] = ENC79_DLG_liu_bingxing;\nENC79_DIALOG["mak_zhendong"] = ENC79_DLG_mak_zhendong;\nENC79_DIALOG["gu_mingfai"] = ENC83_DLG_gu_mingfai;\nENC79_DIALOG["lok_gasing"] = ENC83_DLG_lok_gasing;\nENC79_DIALOG["ngai_wingnaam"] = ENC83_DLG_ngai_wingnaam;\nENC79_DIALOG["chai_zanhoi"] = ENC83_DLG_chai_zanhoi;\nENC79_DIALOG["pang_siuki"] = ENC84_DLG_pang_siuki;\nENC79_DIALOG["so_jiyan"] = ENC84_DLG_so_jiyan;\nENC79_DIALOG["chung_choning"] = ENC84_DLG_chung_choning;\nENC79_DIALOG["ching_tinlok"] = ENC84_DLG_ching_tinlok;';
const t4Start = html.indexOf('/* ---------- T4 提攜');
const t4End = html.indexOf('/* ===== v20a84 ENC84', t4Start);
if(t4Start < 0 || t4End < 0) throw new Error('T4 region not found');
const t4Region = html.slice(t4Start, t4End);
const enc84Start = html.indexOf('/* ---------- Phase 3 四星鏈節拍');
const enc84End = html.indexOf('/* ===== ENC84 模組完 =====', enc84Start);
if(enc84Start < 0 || enc84End < 0) throw new Error('ENC84 beats region not found');
const enc84Region = html.slice(enc84Start, enc84End);
const fns322 = ['enc79StarDef','enc79Hash','enc79Rand','enc79EnsureStars','enc79StarState','enc79TierOf','enc79PlayerTier','enc79FavCap','enc79AddFav','enc79WhisperActive','enc79GrantWhisper','enc79GrantCredit','enc79BoardHasStar','enc79BoardHasActionGig','enc79BeatOpen','enc79AnyBeatOpen','enc79PickBeat','enc79ChoiceFx','enc79RunChoiceFx','enc79NormSeg','enc79BuildScript','enc83NodeDone','enc83Flag','enc83HasCredit','enc83NewsOut','contra98EncFirstLocSwap','grant229Ensure','grant229GigById','grant229Record','grant229RecordFromEnc79','grant229RecordDraft','br89HasCredit','br89GigOn','favor158CreditHeld','isMakWuzhiGig158','isPangCharityGig158','pangHalvedStageReq158','pangEffectiveGig158','pangChannelReady158','favor158ChannelForGig','chungAdviceCardHeld229','isWenyiAuditionGig229','chungAdviceTipForAudition229','chungAdviceSpend229'];
eval(consts322 + '\n' + asVar(extractConst('BR89_PATRON_OF_GIG'), 'BR89_PATRON_OF_GIG') + '\n' + asVar(extractConst('GRANT229_DRAFT'), 'GRANT229_DRAFT') + '\n' + asVar(extractConst('GRANT229_ENC79'), 'GRANT229_ENC79') + '\n' + asVar(extractConst('FAVOR158_MAK_CREDIT_ID'), 'FAVOR158_MAK_CREDIT_ID') + '\n' + asVar(extractConst('FAVOR158_PANG_CREDIT_ID'), 'FAVOR158_PANG_CREDIT_ID') + '\n' + asVar(extractConst('CHUNG_ADVICE_TEXT229'), 'CHUNG_ADVICE_TEXT229') + '\n' + t4Region + '\n' + enc84Region + '\n' + fns322.map(extractFn).join('\n'));

/* ---- helpers ---- */
const RECALL = '你嗰陣勸我企硬，我記得。';
const HEARD = '呢個後生仔，肯由頭聽到尾。';
const PRAISED = '呢個後生仔，識聽。';
const PATRON = beatOf('lok_gasing', 'lok_patron');
function patronSteps(flags){
  resetS(952); _ys = { year: 1992, season: '冬' };
  setFav('lok_gasing', 70);
  const st = metStar('lok_gasing');
  ['lok_foreshadow','lok_intel','lok_help','lok_cover','lok_recover','lok_e4grudge'].forEach(id=>st.beatsDone[id]=1);
  S.flags.lok_calm_truth = 1;
  Object.assign(S.flags, flags || {});
  const b = enc79BuildScript('lok_gasing', false);
  return (b && b.steps || []).filter(s=>s.seg==='beat:lok_patron').map(s=>s.text);
}
function allSteps(flags, doneExcept){
  resetS(953); _ys = { year: 1992, season: '冬' };
  setFav('lok_gasing', 70);
  const st = metStar('lok_gasing');
  for(const b of (ENC79_BEATS.lok_gasing || [])) if(b.id !== doneExcept) st.beatsDone[b.id] = 1;
  Object.assign(S.flags, flags || {});
  const built = enc79BuildScript('lok_gasing', false);
  return (built && built.steps || []).map(s=>({ seg: s.seg, text: String(s.text || '') }));
}

/* ---------- (S) 靜態：回call 句在位＋閘／獎勵／heard-praised 唔郁＋計數 ---------- */
ok('S v322 回call 句字串在位', html.indexOf('["S","你嗰陣勸我企硬，我記得。"]') >= 0);
ok('S stand_original 讀者係 v322 插入段（逐字）',
  html.indexOf('if((S.flags||{}).lok_stand_original) v322.push(["S","你嗰陣勸我企硬，我記得。"]);') >= 0);
ok('S lok_patron 閘逐字唔郁（v314：T4＋calm_truth＋三排除）',
  !!PATRON && PATRON.when.toString().indexOf('enc79TierOf(st.fav)>=4') >= 0 &&
  PATRON.when.toString().indexOf('lok_calm_truth') >= 0 &&
  PATRON.when.toString().indexOf('lok_join_rant') >= 0 &&
  PATRON.when.toString().indexOf('lok_loose_row') >= 0 &&
  PATRON.when.toString().indexOf('lok_cover_first') >= 0);
ok('S 收尾獎勵判定唔郁（sideline280：calm_truth＋三排除）',
  html.indexOf('else if(lineKey==="lok") warm = !!(F.lok_calm_truth) && !(F.lok_join_rant) && !(F.lok_loose_row) && !(F.lok_cover_first);') >= 0);
ok('S heard／praised 變體句唔郁（v278）',
  html.indexOf('["S","呢個後生仔，肯由頭聽到尾。"]') >= 0 &&
  html.indexOf('["S","呢個後生仔，識聽。"]') >= 0);
ok('S 計數零改動：庫 326／trigger 38（credit 27）／BR89 19',
  GIGS_ARR.length === 326 &&
  GIGS_ARR.filter(g=>g && g.trigger).length === 38 &&
  GIGS_ARR.filter(g=>g && g.trigger && g.trigger.kind === 'credit').length === 27 &&
  Object.keys(BR89_PATRON_OF_GIG).length === 19);

/* ---------- (B) 行為：變體插入位置＋共存次序＋冷版／翻唱版唔插 ---------- */
ok('B stand 有旗 → patron 7 句，回call 插喺第 3 句之後', (()=> {
  const ps = patronSteps({ lok_stand_original: 1 });
  return ps.length === 7 && ps[3] === RECALL &&
    ps[2].indexOf('我約咗一位唱片監製老友食飯') === 0 &&
    ps[4].indexOf('你……你幫我引薦呀？') === 0;
})());
ok('B 無旗 → patron 6 句原樣', (()=> {
  const ps = patronSteps({});
  return ps.length === 6 && ps[3].indexOf('你……你幫我引薦呀？') === 0 &&
    ps.indexOf(RECALL) < 0;
})());
ok('B stand＋heard → 8 句，回call 行先、heard 行後', (()=> {
  const ps = patronSteps({ lok_stand_original: 1, lok_heard_whole: 1 });
  return ps.length === 8 && ps[3] === RECALL && ps[4] === HEARD;
})());
ok('B stand＋praised → 8 句，回call 行先、praised 行後', (()=> {
  const ps = patronSteps({ lok_stand_original: 1, lok_praised_song: 1 });
  return ps.length === 8 && ps[3] === RECALL && ps[4] === PRAISED;
})());
ok('B heard 只有 → 7 句，heard 插喺第 3 句之後（v278 唔郁）', (()=> {
  const ps = patronSteps({ lok_heard_whole: 1 });
  return ps.length === 7 && ps[3] === HEARD && ps.indexOf(RECALL) < 0;
})());
ok('B praised 只有 → 7 句，praised 插喺第 3 句之後（v278 唔郁）', (()=> {
  const ps = patronSteps({ lok_praised_song: 1 });
  return ps.length === 7 && ps[3] === PRAISED && ps.indexOf(RECALL) < 0;
})());
ok('B 冷版 patron_cold（loose_row）→ 真係播冷版，全 steps 無回call 句', (()=> {
  const steps = allSteps({ lok_loose_row: 1 }, 'lok_patron_cold');
  return steps.some(s=>s.seg === 'beat:lok_patron_cold') &&
    steps.every(s=>s.text !== RECALL);
})());
ok('B 翻唱版 patron_cover（cover_first）→ 真係播翻唱版，全 steps 無回call 句', (()=> {
  const steps = allSteps({ lok_cover_first: 1 }, 'lok_patron_cover');
  return steps.some(s=>s.seg === 'beat:lok_patron_cover') &&
    steps.every(s=>s.text !== RECALL);
})());
ok('B 閘行為唔郁：calm_truth＋無壞旗 → patron 開；join_rant → patron 唔開', (()=> {
  resetS(954); setFav('lok_gasing', 70); metStar('lok_gasing');
  S.flags.lok_calm_truth = 1;
  const openWarm = enc79BeatOpen('lok_gasing', PATRON) === true;
  S.flags.lok_join_rant = 1;
  const closedRant = enc79BeatOpen('lok_gasing', PATRON) === false;
  return openWarm && closedRant;
})());

console.log(fails.length ? ('FAILURES: ' + fails.length + '\n' + fails.join('\n')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
