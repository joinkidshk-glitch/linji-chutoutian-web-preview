// v20a280 支線收尾獎勵邏輯測試（WORKORDER §12／PLAN §12：九條線統一框架）：
//   (1) helper 單元：九線暖版各派聲望 ＋2／信用 delta ＋1（淨 ＋2）、只派一次、冷版／缺一唔派；
//   (2) patron grants() 整合：暖版授債權＋派獎勵、冷版閘唔開、魏行 ngai_vouch fx、彭／齊債權照授但獎勵唔派；
//   (3) 補派點：patron 早開 → 收尾 beat／heart 後補派；收尾先啱 → patron 唔重複派；
//   (4) 專屬引薦通告接駁：九線 10 張全部新庫在位＋BR89 映射＋trigger 對位（0 張新開）；舊 id 唔喺度；
//   (5) 3.10 結局門檻未郁：E1／E2／E4／E5 數字＋E2 邊界 live 行為；
//   (6) 九線全暖合計 ＋18／＋18（delta ＋9＋派生 ＋9；v20a281 收窄，原派生信用 ＋27）；
//   (7) 靜態 guard：helper 一次、call sites 18 處、草稿旗唔入 code、唔改 SAVE key／softRev／?v=、通告庫仍 288 張。
// 反證：喺 pristine（v20a279）index 上行 → (1)(2)(3) helper／grants 鉤乾淨 FAIL；(4) 映射在位但獎勵無；(5)(6)(7) 部分 PASS（門檻本來就啱）。
// 用法：node tests/test_sideline280_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const GIGS_NEW = require('../content/gigs_new.json');
const GIGS_ARR = Array.isArray(GIGS_NEW) ? GIGS_NEW : (GIGS_NEW.gigs||[]);
const gigById = (id)=> GIGS_ARR.find(g=>g && g.id===id) || null;
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

/* ---- sandbox（同 test_sideline278_logic.js；resetS 加雙軌欄位） ---- */
let S;
let _ys = { year: 1990, season: '春' };
let _doneNodes = new Set();
function resetS(day){
  S = { dayIndex: day||0, fame: 0, money: 2000, stage: 0, acting: 0, vocal: 0, looks: 0, charm: 0, iq: 0, stress: 0, industryCreditDelta: 0, industryCredit: 0, stageVolume: 0, calib60Bank: {}, flags: {}, npcs: { agent: 0 }, mockRumors: [], mockDebts: [], mockCredits: [], board: {}, shoots: [], mapTips: {}, story: { flags: {} }, starWeek: {}, weekGigsDone: 0, starWhispers: {}, grant229Queue: [], pendingAud: [], news82: { pub: {}, arc: {} } };
  _doneNodes = new Set();
  _ledger = null;
}
function setFav(sid, n){ enc79EnsureStars(); S.stars[sid].fav = n; }
function beatOf(sid, id){ return (ENC79_BEATS[sid] || []).find(b => b.id === id); }
function metStar(sid){ enc79EnsureStars(); S.stars[sid].met = true; return S.stars[sid]; }
function doneAllBeats(sid){ const st = metStar(sid); for(const b of (ENC79_BEATS[sid]||[])) st.beatsDone[b.id] = 1; return st; }
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
const consts278 = ['ENC79_TIER_NAMES','ENC79_PLAYER_TIERS','ENC79_FAV_CAPS','ENC79_STARS','ENC79_PILOT','ENC79_STAGEUP','ENC79_CAP_LINES','ENC79_WRAP_ECHO','ENC79_BEATS','ENC79_DIALOG','ENC79_FIRST_ALT98'].map(n=> asVar(extractConst(n), n)).join('\n')
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
const fns278 = ['enc79StarDef','enc79Hash','enc79Rand','enc79EnsureStars','enc79StarState','enc79TierOf','enc79PlayerTier','enc79FavCap','enc79AddFav','enc79WhisperActive','enc79GrantWhisper','enc79GrantCredit','enc79BoardHasStar','enc79BoardHasActionGig','enc79BeatOpen','enc79AnyBeatOpen','enc79PickBeat','enc79ChoiceFx','enc79RunChoiceFx','enc79NormSeg','enc79BuildScript','enc83NodeDone','enc83Flag','enc83HasCredit','enc83NewsOut','contra98EncFirstLocSwap','grant229Ensure','grant229GigById','grant229Record','grant229RecordFromEnc79','grant229RecordDraft','br89HasCredit','br89GigOn','favor158CreditHeld','isMakWuzhiGig158','isPangCharityGig158','pangHalvedStageReq158','pangEffectiveGig158','pangChannelReady158','favor158ChannelForGig','chungAdviceCardHeld229','isWenyiAuditionGig229','chungAdviceTipForAudition229','chungAdviceSpend229'];
eval(consts278 + '\n' + asVar(extractConst('BR89_PATRON_OF_GIG'), 'BR89_PATRON_OF_GIG') + '\n' + asVar(extractConst('GRANT229_DRAFT'), 'GRANT229_DRAFT') + '\n' + asVar(extractConst('GRANT229_ENC79'), 'GRANT229_ENC79') + '\n' + asVar(extractConst('FAVOR158_MAK_CREDIT_ID'), 'FAVOR158_MAK_CREDIT_ID') + '\n' + asVar(extractConst('FAVOR158_PANG_CREDIT_ID'), 'FAVOR158_PANG_CREDIT_ID') + '\n' + asVar(extractConst('CHUNG_ADVICE_TEXT229'), 'CHUNG_ADVICE_TEXT229') + '\n' + asVar(extractConst('ENDING410_T'), 'ENDING410_T') + '\n' + asVar(extractConst('ENDING95_T'), 'ENDING95_T') + '\n' + t4Region + '\n' + enc84Region + '\n' + fns278.map(extractFn).join('\n') + '\n' + ['dualTrackNumbers','readDualTracks','syncDualTracks','endingDual410','endingE2Eligible410','sideline280GrantCompletion'].map(extractFn).join('\n'));

/* ---- helper：每線暖旗 ---- */
function warmFlags280(line){
  if(line==='liu') S.flags.enc79_liu_clash_stand = 1;
  else if(line==='gu'){ /* 顧無正面暖旗：暖版＝patron 閘本身（無拒借、無提賭） */ }
  else if(line==='mak'){ /* 麥無正面暖旗：暖版＝patron 閘本身（無老實講會驚） */ }
  else if(line==='lok') S.flags.lok_calm_truth = 1;
  else if(line==='ngai'){ /* 魏暖版＝vouch fx 本身 */ }
  else if(line==='chai'){ S.flags.chai_truth_change = 1; S.flags.chai_try_new = 1; }
  else if(line==='pang'){ S.flags.pang_cover_night = 1; S.flags.pang_listened = 1; S.flags.pang_noodle_night = 1; }
  else if(line==='chung'){ S.flags.chung_kept_quiet = 1; S.flags.chung_listened = 1; }
  else if(line==='ching'){ S.story.flags.flag_vocal_train = 1; S.flags.ching_back_train = 1; S.flags.ching_stand_slow = 1; }
}
const PATRON280 = {
  liu: ['liu_bingxing','liu_patron','credit_enc83_liu_patron'],
  gu: ['gu_mingfai','gu_patron','credit_enc83_gu_patron'],
  mak: ['mak_zhendong','mak_patron','credit_enc83_mak_patron'],
  lok: ['lok_gasing','lok_patron','credit_enc83_lok_patron'],
  chai: ['chai_zanhoi','chai_patron','credit_enc83_chai_patron'],
  pang: ['pang_siuki','pang_patron','credit_enc84_pang_patron'],
  chung: ['chung_choning','chung_patron','credit_enc84_chung_patron'],
  ching: ['ching_tinlok','ching_patron','credit_enc84_ching_patron'],
};

/* ---- (1) helper 單元 ---- */
ok('(1) 暖版九線：helper 各派聲望 ＋2／信用 delta ＋1（淨 ＋2）＋已派標記', (()=> {
  let good = true;
  for(const line of ['liu','gu','mak','lok','ngai','chai','pang','chung','ching']){
    resetS(1000); warmFlags280(line);
    const r = sideline280GrantCompletion(line);
    if(!(r===true && S.fame===2 && S.industryCreditDelta===1 && S.flags['sideline280_'+line]===1)) good = false;
  }
  return good;
})());
ok('(1) 只派一次：同一線再呼叫唔再加', (()=> {
  resetS(1001); warmFlags280('lok');
  sideline280GrantCompletion('lok');
  const r2 = sideline280GrantCompletion('lok');
  return r2===false && S.fame===2 && S.industryCreditDelta===1;
})());
ok('(1) 冷版唔派：廖企導演邊／推辭、顧拒借／提賭、麥老實講會驚', (()=> {
  let good = true;
  resetS(1002); S.flags.enc79_liu_clash_script = 1; if(sideline280GrantCompletion('liu')!==false || S.fame!==0) good = false;
  resetS(1003); S.flags.enc79_liu_declined = 1; if(sideline280GrantCompletion('liu')!==false || S.fame!==0) good = false;
  resetS(1004); S.flags.enc83_gu_loan_refused = 1; if(sideline280GrantCompletion('gu')!==false || S.fame!==0) good = false;
  resetS(1005); S.flags.gu_n10_warned = 1; if(sideline280GrantCompletion('gu')!==false || S.fame!==0) good = false;
  resetS(1006); S.flags.enc79_mak_honest = 1; if(sideline280GrantCompletion('mak')!==false || S.fame!==0) good = false;
  return good;
})());
ok('(1) 冷版唔派：駱陪鬧／講出去／翻唱、魏企埋一邊／唔講大話', (()=> {
  let good = true;
  resetS(1007); S.flags.lok_calm_truth = 1; S.flags.lok_join_rant = 1; if(sideline280GrantCompletion('lok')!==false || S.fame!==0) good = false;
  resetS(1008); S.flags.lok_calm_truth = 1; S.flags.lok_loose_row = 1; if(sideline280GrantCompletion('lok')!==false || S.fame!==0) good = false;
  resetS(1009); S.flags.lok_calm_truth = 1; S.flags.lok_cover_first = 1; if(sideline280GrantCompletion('lok')!==false || S.fame!==0) good = false;
  resetS(1010); S.flags.ngai_rain_hold_back = 1; if(sideline280GrantCompletion('ngai')!==false || S.fame!==0) good = false;
  return good;
})());
ok('(1) 缺一唔派：齊缺 Beat 5／缺 Beat 4、彭缺麵／缺聽／缺頂、鍾缺守口／缺靜聽、程缺 N15／缺撐練／缺慢路', (()=> {
  let good = true;
  const cases = [
    ['chai', ()=>{ S.flags.chai_truth_change = 1; }],
    ['chai', ()=>{ S.flags.chai_try_new = 1; }],
    ['pang', ()=>{ S.flags.pang_cover_night = 1; S.flags.pang_listened = 1; }],
    ['pang', ()=>{ S.flags.pang_cover_night = 1; S.flags.pang_noodle_night = 1; }],
    ['pang', ()=>{ S.flags.pang_listened = 1; S.flags.pang_noodle_night = 1; }],
    ['chung', ()=>{ S.flags.chung_kept_quiet = 1; }],
    ['chung', ()=>{ S.flags.chung_listened = 1; }],
    ['ching', ()=>{ S.flags.ching_back_train = 1; S.flags.ching_stand_slow = 1; }],
    ['ching', ()=>{ S.story.flags.flag_vocal_train = 1; S.flags.ching_stand_slow = 1; }],
    ['ching', ()=>{ S.story.flags.flag_vocal_train = 1; S.flags.ching_back_train = 1; }],
  ];
  for(const [line, setup] of cases){
    resetS(1011); setup();
    if(sideline280GrantCompletion(line)!==false || S.fame!==0) good = false;
  }
  return good;
})());
ok('(1) 錯過成段唔派：齊唔出聲（repay 唔開）、彭嚟唔到（交心唔開）→ 暖旗本身落唔到，helper 唔派', (()=> {
  resetS(1012); S.flags.chai_silent = 1;
  const a = sideline280GrantCompletion('chai')===false && S.fame===0;
  resetS(1013); S.flags.pang_absent_night = 1;
  const b = sideline280GrantCompletion('pang')===false && S.fame===0;
  return a && b;
})());
ok('(1) 派生值：＋2 聲望＋＋1 delta → readDualTracks 信用 ＋2（v20a281 收窄；fame×0.5 派生 ＋1）', (()=> {
  resetS(1014); warmFlags280('lok');
  const before = readDualTracks(S).industryCredit;
  sideline280GrantCompletion('lok');
  const after = readDualTracks(S).industryCredit;
  return before===0 && after===2 && S.fame===2 && S.industryCreditDelta===1;
})());
ok('(1) 未知線 key 唔派唔寫入', (()=>{ resetS(1015); return sideline280GrantCompletion('nope')===false && S.fame===0; })());

/* ---- (2) patron grants() 整合 ---- */
ok('(2) 暖版 patron grants()：八線授債權＋派 ＋2／＋2', (()=> {
  let bad = [];
  for(const line of Object.keys(PATRON280)){
    const [sid, pid, cid] = PATRON280[line];
    resetS(1020); setFav(sid, 70); metStar(sid); warmFlags280(line);
    beatOf(sid, pid).grants();
    if(!(enc83HasCredit(cid)===true && S.fame===2 && S.industryCreditDelta===1 && S.flags['sideline280_'+line]===1)) bad.push(line);
  }
  if(bad.length) console.log('  (2) bad: ' + bad.join(','));
  return bad.length===0;
})());
ok('(2) 暖版 patron 閘：冷旗在位 → 六線暖版 patron 唔開（credit＋獎勵都唔派）', (()=> {
  const cases = [
    ['liu_bingxing','liu_patron','enc79_liu_clash_script'],
    ['gu_mingfai','gu_patron','enc83_gu_loan_refused'],
    ['mak_zhendong','mak_patron','enc79_mak_honest'],
    ['lok_gasing','lok_patron','lok_join_rant'],
    ['chai_zanhoi','chai_patron','chai_comfort'],
    ['chung_choning','chung_patron','chung_asked_return'],
  ];
  return cases.every(([sid, pid, flag])=>{ resetS(1021); setFav(sid,70); metStar(sid); S.flags[flag]=1; return enc79BeatOpen(sid, beatOf(sid,pid))===false; });
})());
ok('(2) 魏 ngai_vouch fx：照實講授債權＋派 ＋2／＋2；再跑唔重複', (()=> {
  resetS(1022); enc79RunChoiceFx('ngai_vouch');
  const a = enc83HasCredit('credit_enc83_ngai_patron')===true && S.fame===2 && S.industryCreditDelta===1 && S.flags.sideline280_ngai===1;
  enc79RunChoiceFx('ngai_vouch');
  const b = S.fame===2 && S.industryCreditDelta===1 && S.mockCredits.length===1;
  return a && b;
})());
ok('(2) 魏 ngai_patron 仍然無 grants()（債權改行 fx 通道，v278 不變）', beatOf('ngai_wingnaam','ngai_patron') && typeof beatOf('ngai_wingnaam','ngai_patron').grants==='undefined');
ok('(2) 彭 patron 閘本身只睇 tier（舊制）：冷版 grants() 照授債權，但獎勵唔派', (()=> {
  resetS(1023); setFav('pang_siuki',70); metStar('pang_siuki');
  S.flags.pang_early_night = 1; /* Beat 5 趕住返屋企瞓（冷版） */
  beatOf('pang_siuki','pang_patron').grants();
  return enc83HasCredit('credit_enc84_pang_patron')===true && S.fame===0 && S.industryCreditDelta===0 && !S.flags.sideline280_pang;
})());
ok('(2) 齊 patron 閘唔讀 try_new（舊制）：穩陣版 grants() 照授債權，但獎勵唔派', (()=> {
  resetS(1024); setFav('chai_zanhoi',70); metStar('chai_zanhoi');
  S.flags.chai_truth_change = 1; S.flags.chai_play_safe = 1; /* Beat 4 講真話、Beat 5 要穩陣 */
  beatOf('chai_zanhoi','chai_patron').grants();
  return enc83HasCredit('credit_enc83_chai_patron')===true && S.fame===0 && S.industryCreditDelta===0 && !S.flags.sideline280_chai;
})());

/* ---- (3) 補派點：patron 早開 → 收尾 beat／heart 後補派；收尾先啱 → patron 唔重複 ---- */
ok('(3) 廖：patron 早開（未嗌交）唔派；Beat 5 企佢嗰邊後 clash grants() 補派', (()=> {
  resetS(1030); setFav('liu_bingxing',70); metStar('liu_bingxing');
  beatOf('liu_bingxing','liu_patron').grants();
  const early = S.fame===0 && !S.flags.sideline280_liu;
  S.flags.enc79_liu_clash_stand = 1;
  beatOf('liu_bingxing','liu_clash').grants();
  return early && S.fame===2 && S.industryCreditDelta===1 && S.flags.sideline280_liu===1;
})());
ok('(3) 廖：Beat 5 先企佢嗰邊 → clash 派；patron 之後唔重複派', (()=> {
  resetS(1031); setFav('liu_bingxing',70); metStar('liu_bingxing');
  S.flags.enc79_liu_clash_stand = 1;
  beatOf('liu_bingxing','liu_clash').grants();
  beatOf('liu_bingxing','liu_patron').grants();
  return S.fame===2 && S.industryCreditDelta===1;
})());
ok('(3) 駱：patron 早開（E4 未出）唔派；e4grudge 勸佢後補派；講出去嗰陣補派都唔派', (()=> {
  resetS(1032); setFav('lok_gasing',70); metStar('lok_gasing');
  beatOf('lok_gasing','lok_patron').grants();
  const early = S.fame===0 && !S.flags.sideline280_lok;
  S.flags.lok_calm_truth = 1;
  beatOf('lok_gasing','lok_e4grudge').grants();
  const paid = S.fame===2 && S.industryCreditDelta===1;
  resetS(1033); S.flags.lok_calm_truth = 1; S.flags.lok_loose_row = 1;
  beatOf('lok_gasing','lok_e4grudge').grants();
  return early && paid && S.fame===0 && !S.flags.sideline280_lok;
})());
ok('(3) 齊：patron 早開（未試新角）唔派；repay 試新角後補派', (()=> {
  resetS(1034); setFav('chai_zanhoi',70); metStar('chai_zanhoi');
  S.flags.chai_truth_change = 1;
  beatOf('chai_zanhoi','chai_patron').grants();
  const early = S.fame===0 && !S.flags.sideline280_chai;
  S.flags.chai_try_new = 1;
  beatOf('chai_zanhoi','chai_repay').grants();
  return early && S.fame===2 && S.industryCreditDelta===1;
})());
ok('(3) 彭：patron 早開（未食麵）唔派；n17 食麵後補派', (()=> {
  resetS(1035); setFav('pang_siuki',70); metStar('pang_siuki');
  S.flags.pang_cover_night = 1; S.flags.pang_listened = 1;
  beatOf('pang_siuki','pang_patron').grants();
  const early = S.fame===0 && !S.flags.sideline280_pang;
  S.flags.pang_noodle_night = 1;
  beatOf('pang_siuki','pang_n17').grants();
  return early && S.fame===2 && S.industryCreditDelta===1;
})());
ok('(3) 程：patron 早開（未企慢路）唔派；e4 撐練嗰陣未齊唔派，heart 企慢路後 helper 補派', (()=> {
  resetS(1036); setFav('ching_tinlok',70); metStar('ching_tinlok');
  S.story.flags.flag_vocal_train = 1; S.flags.ching_back_train = 1;
  beatOf('ching_tinlok','ching_patron').grants();
  const early = S.fame===0 && !S.flags.sideline280_ching;
  beatOf('ching_tinlok','ching_e4').grants();
  const mid = S.fame===0 && !S.flags.sideline280_ching;
  S.flags.ching_stand_slow = 1;
  const paid = sideline280GrantCompletion('ching')===true && S.fame===2 && S.industryCreditDelta===1;
  return early && mid && paid;
})());
ok('(3) heart 補派點在位：enc79BuildScript heart 回調有 chai／pang／chung／ching 四線守衛呼叫', (()=> {
  const src = extractFn('enc79BuildScript');
  return src.indexOf('sideline280GrantCompletion("chai")')>=0 && src.indexOf('sideline280GrantCompletion("pang")')>=0 && src.indexOf('sideline280GrantCompletion("chung")')>=0 && src.indexOf('sideline280GrantCompletion("ching")')>=0;
})());
ok('(3) heart segFx 真行：ching heart 完成（企慢路已落）→ helper 補派', (()=> {
  resetS(1037); _ys={year:1992,season:'冬'}; setFav('ching_tinlok',45);
  const st = doneAllBeats('ching_tinlok'); st.heartDone = false;
  S.story.flags.flag_vocal_train = 1; S.flags.ching_back_train = 1; S.flags.ching_stand_slow = 1;
  const built = enc79BuildScript('ching_tinlok', false);
  const heartStep = (built && built.steps || []).find(s=>s.seg==='heart:ching_tinlok' && typeof s.segFx==='function'); /* 抉擇段嘅 segFx 掛喺 choice step（最後一步），唔係第一句 */
  if(!heartStep || typeof heartStep.segFx!=='function') return false;
  heartStep.segFx();
  return S.fame===2 && S.industryCreditDelta===1 && S.flags.sideline280_ching===1;
})());
ok('(3) 收尾 beats grants 在位：liu_clash／lok_e4grudge／chai_repay／pang_n17／ching_e4 全部有 grants()', ['liu_bingxing|liu_clash','lok_gasing|lok_e4grudge','chai_zanhoi|chai_repay','pang_siuki|pang_n17','ching_tinlok|ching_e4'].every(pair=>{ const [sid, bid] = pair.split('|'); const b = beatOf(sid, bid); return b && typeof b.grants==='function'; }));

/* ---- (4) 專屬引薦通告接駁（九線 10 張，0 張新開） ---- */
const GIG280 = [
  ['liu-priority','gig_1991_film_103','credit_enc79_liu_priority'],
  ['liu-G-L1','gig_1992_film_103','credit_enc83_liu_patron'],
  ['gu-G-G1','gig_1992_rec_205','credit_enc83_gu_patron'],
  ['mak-G-M2','gig_1991_film_211','credit_enc83_mak_patron'],
  ['lok-G-LOK-1','gig_1992_rec_111','credit_enc83_lok_patron'],
  ['ngai-G-NGAI-1','gig_1991_film_212','credit_enc83_ngai_patron'],
  ['chai-G-CHAI-1','gig_1992_film_206','credit_enc83_chai_patron'],
  ['pang','gig_1991_variety_203','credit_enc84_pang_patron'],
  ['chung-G-C1','gig_1991_film_213','credit_enc84_chung_patron'],
  ['ching','gig_1992_rec_106','credit_enc84_ching_patron'],
];
ok('(4) 九線 10 張專屬通告全部新庫在位＋trigger 憑債權＋BR89 映射對位', GIG280.every(([tag, gid, cid])=>{ const g = gigById(gid); return !!g && g.trigger && g.trigger.kind==='credit' && g.trigger.creditId===cid && BR89_PATRON_OF_GIG[gid]===cid; }));
ok('(4) 顧 G-G1 就係 v274 gig_1992_rec_205《夜總會登台暖場》，唔係重開', (()=>{ const g = gigById('gig_1992_rec_205'); return !!g && String(g.title||'').indexOf('夜總會登台暖場')>=0 && g.trigger.creditId==='credit_enc83_gu_patron'; })());
ok('(4) 廖收割通告唔係外傳：gig_1991_film_214 係 wf3harvest 補拍，唔係優先試鏡', (()=>{ const g = gigById('gig_1991_film_214'); const p = gigById('gig_1991_film_103'); return !!g && g.trigger.kind==='wf3harvest' && String(g.title||'').indexOf('夜景補拍')>=0 && !!p && String(p.title||'').indexOf('外傳')>=0 && p.trigger.creditId==='credit_enc79_liu_priority'; })());
ok('(4) 舊庫三 id 唔喺新庫＋唔喺 BR89 映射（gig_br89_liu_priority／gig_br89_patron_pang／gig_br89_patron_ching）', ['gig_br89_liu_priority','gig_br89_patron_pang','gig_br89_patron_ching'].every(id=> !gigById(id) && !(id in BR89_PATRON_OF_GIG)));
ok('(4) 專屬通告標題唔含年份數字（新庫規格）', GIG280.every(([, gid])=>{ const t = String((gigById(gid)||{}).title||''); return !/19\d\d|20\d\d/.test(t); }));
ok('(4) 通告庫總數 306 張（v280 0 張新開＋v284 1 張 film_114＋v291 13 張冬季 gig＋v307 4 張真唱片 gig）', GIGS_ARR.length===306);

/* ---- (5) 3.10 結局門檻未郁 ---- */
ok('(5) E1 數字：ENDING95_T 聲望 70／信用 65／雙軌 350／負標籤 ≤1', ENDING95_T.e1Fame===70 && ENDING95_T.e1Credit===65 && ENDING95_T.e1Dual===350 && ENDING95_T.e1NegMax===1);
ok('(5) E1 質性閘：獎 ≥1＋擔正媒介 ≥2＋主線脊骨（live 判定式未郁）', html.indexOf('awards95.hasWin && leadMedia95.length >= 2 && spine95.done')>=0 && html.indexOf('fame>=T95.e1Fame && credit>=T95.e1Credit && sum>=T95.e1Dual && neg<=T95.e1NegMax && e1Qual95')>=0);
ok('(5) E2 數字：信用 ≥42＋聲望 ≥35', ENDING410_T.e2Credit===42 && ENDING410_T.e2Fame===35);
ok('(5) E2 邊界 live 行為：信用 42／聲望 35 入閘，差 1 唔入', (()=> {
  resetS(1050); S.fame = 35; S.industryCreditDelta = 24; /* base round(35×0.5)=18，信用 42 */
  const a = endingE2Eligible410(S)===true;
  resetS(1051); S.fame = 35; S.industryCreditDelta = 23; /* 信用 41 */
  const b = endingE2Eligible410(S)===false;
  resetS(1052); S.fame = 34; S.industryCreditDelta = 24; /* 聲望 34，信用 41 */
  const c = endingE2Eligible410(S)===false;
  return a && b && c;
})());
ok('(5) E4 救回門檻 ≥2 筆未用債權，唔放寬', ENDING410_T.e4RescueCredits===2 && html.indexOf('favor.creditsHeld>=T.e4RescueCredits')>=0);
ok('(5) E5：已清債＋持有 ≥6＋何生 rel ≥60', ENDING410_T.e5FavorTotal===6 && ENDING410_T.e5AgentRel===60 && html.indexOf('(favor.settled + favor.creditsHeld)>=T.e5FavorTotal && agentRel>=T.e5AgentRel')>=0);

/* ---- (6) 九線全暖合計 ---- */
ok('(6) 九線全暖：聲望 ＋18／信用 delta ＋9／派生信用 ＋18（v20a281 收窄）', (()=> {
  resetS(1060);
  let good = true;
  for(const line of ['liu','gu','mak','lok','ngai','chai','pang','chung','ching']){
    warmFlags280(line);
    if(sideline280GrantCompletion(line)!==true) good = false;
  }
  const derived = readDualTracks(S).industryCredit;
  return good && S.fame===18 && S.industryCreditDelta===9 && derived===18;
})());

/* ---- (6b) v20a281：每線信用淨 ＋2 機制 ---- */
ok('(6b) 每線信用淨 ＋2：＋2 聲望經 baseCredit 派生 ＋1 ＋ delta ＋1 ＝ ＋2', (()=> {
  resetS(1061); warmFlags280('ching');
  const before = readDualTracks(S).industryCredit;
  if(sideline280GrantCompletion('ching')!==true) return false;
  const after = readDualTracks(S).industryCredit;
  return before===0 && after===2 && S.fame===2 && S.industryCreditDelta===1 && after-before===2;
})());

/* ---- (7) 靜態 guard ---- */
ok('(7) helper 只定義一次', (html.match(/function sideline280GrantCompletion\(lineKey\)/g)||[]).length===1);
ok('(7) call sites 18 處：patron 8＋ngai fx 1＋收尾 beats 5＋heart 4', (html.match(/sideline280GrantCompletion\("[a-z]+"\)/g)||[]).length===18);
ok('(7) 草稿旗 liu_stand_92／gu_patron_take／mak_follow_big 只喺 v280 註解提一次，唔入判定 code', ['liu_stand_92','gu_patron_take','mak_follow_big'].every(f=> (html.match(new RegExp(f,'g'))||[]).length===1 && html.indexOf('F.'+f)<0 && html.indexOf('flags: ["'+f+'"]')<0));
ok('(7) 唔改 SAVE key／softRev／?v=（v280 只改內容）', html.indexOf('starVolunteer_map_v19w')>=0 && html.indexOf('"s107"')>=0 && html.indexOf('v20a10')>=0);

console.log(fails.length ? ('FAILURES: ' + fails.length + '\n' + fails.join('\n')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
