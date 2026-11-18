// v20a305 resync：(4) 節拍表順序——三線加 finale（排提攜之後）、鍾提攜排送別之前。
// v20a278 六線草稿抉擇全面實裝邏輯測試（PLAN §4–§9：駱／魏／齊／彭／鍾／程）：
//   (1) ChoiceFx 12 新分支（fav＋ngai_vouch fx）；(2) RunChoiceFx ngai_vouch 授債權＋ngai_patron grants() 已拆；
//   (3) GRANT229_ENC79 57 行（gig 在位＋key 唯一命中 live label＋即派正確）；
//   (4) registry 閘門（3 新 beats／6 冷版 patron／2 彭收尾／暖版排除式閘／延遲開／repay 放寬）；
//   (5) BuildScript 變體＋heart 分流＋ngai_repay 冷版；(6) 靜態 guard（67 旗＋新 beats DLG＋registry）。
// 反證：喺 pristine（v20a277）index 上行 → (1)(2)(3)(4)(5) 新抉擇／新 beats／新閘斷言乾淨 FAIL；(6) 旗盤點 FAIL。
// 用法：node tests/test_sideline278_logic.js [path-to-index.html]
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

/* ---- sandbox（同 test_sideline273_logic.js；加 grant229RecordFromEnc79） ---- */
let S;
let _ys = { year: 1990, season: '春' };
let _doneNodes = new Set();
function resetS(day){
  S = { dayIndex: day||0, fame: 0, money: 2000, flags: {}, npcs: { agent: 0 }, mockRumors: [], mockDebts: [], mockCredits: [], board: {}, shoots: [], mapTips: {}, story: { flags: {} }, starWeek: {}, weekGigsDone: 0, starWhispers: {}, grant229Queue: [], pendingAud: [], news82: { pub: {}, arc: {} } };
  _doneNodes = new Set();
  _ledger = null; /* v20a278：resetS 連 favor ledger 一齊清——否則同一 credit id 喺唔同 test 再授會俾 counted 擋走（S 已全新，ledger 唔清就唔同步） */
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
eval(consts278 + '\n' + asVar(extractConst('BR89_PATRON_OF_GIG'), 'BR89_PATRON_OF_GIG') + '\n' + asVar(extractConst('GRANT229_DRAFT'), 'GRANT229_DRAFT') + '\n' + asVar(extractConst('GRANT229_ENC79'), 'GRANT229_ENC79') + '\n' + asVar(extractConst('FAVOR158_MAK_CREDIT_ID'), 'FAVOR158_MAK_CREDIT_ID') + '\n' + asVar(extractConst('FAVOR158_PANG_CREDIT_ID'), 'FAVOR158_PANG_CREDIT_ID') + '\n' + asVar(extractConst('CHUNG_ADVICE_TEXT229'), 'CHUNG_ADVICE_TEXT229') + '\n' + t4Region + '\n' + enc84Region + '\n' + fns278.map(extractFn).join('\n'));

/* ---- helper：攞 live label ---- */
function labelsOf(seg){
  const kind = seg.split(':')[0], rest = seg.split(':').slice(1).join(':');
  if(kind==='first' || kind==='heart'){
    const D = ENC79_DIALOG[rest];
    if(!D) return [];
    const s = kind==='first' ? D.first : D.heart;
    return ((s&&s.choices)||[]).map(c=>c.label);
  }
  if(kind==='beat'){
    const starId = rest.indexOf('lok_')===0 ? 'lok_gasing' : rest.indexOf('ngai_')===0 ? 'ngai_wingnaam' : rest.indexOf('chai_')===0 ? 'chai_zanhoi' : rest.indexOf('pang_')===0 ? 'pang_siuki' : rest.indexOf('chung_')===0 ? 'chung_choning' : rest.indexOf('ching_')===0 ? 'ching_tinlok' : null;
    if(!starId) return [];
    const D = ENC79_DIALOG[starId];
    const b = D && D.beats && D.beats[rest];
    return ((b&&b.choices)||[]).map(c=>c.label);
  }
  return [];
}
function beatLabels(star, bid){ const D = ENC79_DIALOG[star]; const b = D && D.beats && D.beats[bid]; return ((b&&b.choices)||[]).map(c=>c.label); }
function stepsText(built){ return (built && built.steps || []).map(s=>String(s.text||'')); }
function hasText(built, sub){ return stepsText(built).some(t=>t.indexOf(sub)>=0); }

/* ---- (1) ChoiceFx 12 新分支（用 live label 逐個對） ---- */
ok('(1) lok_foreshadow：守口 +3／講兩句 -2', enc79ChoiceFx('beat:lok_foreshadow','守口，話冇咩事').fav===3 && enc79ChoiceFx('beat:lok_foreshadow','同人講兩句，話佢為原創歌同高層嗌交').fav===-2);
ok('(1) lok_cover：企硬 +5／唱住先 +3', enc79ChoiceFx('beat:lok_cover','勸佢企硬，唔好唱翻唱').fav===5 && enc79ChoiceFx('beat:lok_cover','勸佢唱住先，上咗台先再慢慢推原創').fav===3);
ok('(1) ngai_rain：衝入雨幕 +5／企埋一邊 0', enc79ChoiceFx('beat:ngai_rain','衝入雨幕，用佢教嘅企位頂住燈架').fav===5 && enc79ChoiceFx('beat:ngai_rain','企埋一邊，等武指嚟').fav===0);
ok('(1) chai_fear：守口 +3／講兩句 -2', enc79ChoiceFx('beat:chai_fear','守口，話佢好穩陣，唔好亂講').fav===3 && enc79ChoiceFx('beat:chai_fear','講兩句，話一哥都驚後生追上嚟').fav===-2);
ok('(1) pang_intel：一早去 +3／遲咗 0', enc79ChoiceFx('beat:pang_intel','一早去後台留名，準時到').fav===3 && enc79ChoiceFx('beat:pang_intel','遲咗去／唔去，覺得唔差在').fav===0);
ok('(1) chung_intel：跟指點 +3／跑熟路 +1', enc79ChoiceFx('beat:chung_intel','跟佢指點去試：帶住個腦去，唔背定一套演法').fav===3 && enc79ChoiceFx('beat:chung_intel','繼續跑熟路通告：邊度有工就去邊度').fav===1);
ok('(1) chung_f_clue：守口 +3／講兩句 -2', enc79ChoiceFx('beat:chung_f_clue','守口，話冇咩事').fav===3 && enc79ChoiceFx('beat:chung_f_clue','同人講兩句：佢加拿大手續辦緊').fav===-2);
ok('(1) ching_rival：留低 +3／走先 +1', enc79ChoiceFx('beat:ching_rival','留低陪佢練：幫佢聽住，走音即刻嗌停').fav===3 && enc79ChoiceFx('beat:ching_rival','走先返去瞓：聽朝仲有通告要開工').fav===1);
ok('(1) ching_e4：撐練 +5／紅先算 +1', enc79ChoiceFx('beat:ching_e4','撐佢練真功夫：個名上咗報紙，功夫就要追得上個名').fav===5 && enc79ChoiceFx('beat:ching_e4','叫佢紅咗先算：執聲有咩所謂，紅咗先算').fav===1);
ok('(1) ngai_patron：照實講 +3＋fx ngai_vouch／唔講大話 +1 無 fx', (()=>{ const a=enc79ChoiceFx('beat:ngai_patron','照實講：佢得，佢企得穩'); const b=enc79ChoiceFx('beat:ngai_patron','唔好為我講大話，照實講就得，唔得我自己再練'); return a.fav===3 && a.fx==='ngai_vouch' && b.fav===1 && !b.fx; })());
ok('(1) ngai_patron key 互斥：兩選項都含「照實講」，A 靠「企得穩」分流', enc79ChoiceFx('beat:ngai_patron','照實講：佢得，佢企得穩').fx==='ngai_vouch' && !enc79ChoiceFx('beat:ngai_patron','唔好為我講大話，照實講就得，唔得我自己再練').fx);
ok('(1) chai_repay：唔同 +3／穩陣 +1', enc79ChoiceFx('beat:chai_repay','試個同以前唔同嘅角色').fav===3 && enc79ChoiceFx('beat:chai_repay','要個穩陣嘅，慢慢嚟').fav===1);
ok('(1) pang_n17：雲吞麵 +3／返屋企瞓 +1', enc79ChoiceFx('beat:pang_n17','去廟街食碗雲吞麵，陪佢坐低').fav===3 && enc79ChoiceFx('beat:pang_n17','趕住返屋企瞓，聽日仲有工開').fav===1);
ok('(1) 舊分支唔郁：lok_help 試 +5／ngai_help 大排檔 +5 fx ngai_meal／pang_help 頂一晚 +5 fx pang_helped', enc79ChoiceFx('beat:lok_help','試試，一Take過給你看').fav===5 && enc79ChoiceFx('beat:ngai_help','請他去大排檔，吃頓好的').fav===5 && enc79ChoiceFx('beat:ngai_help','請他去大排檔，吃頓好的').fx==='ngai_meal' && enc79ChoiceFx('beat:pang_help','頂一晚：整晚跟足全程，幫他看流程').fav===5 && enc79ChoiceFx('beat:pang_help','頂一晚：整晚跟足全程，幫他看流程').fx==='pang_helped');

/* ---- (2) RunChoiceFx ngai_vouch＋ngai_patron grants() 已拆 ---- */
ok('(2) ngai_vouch 授 credit_enc83_ngai_patron（打女引薦）', (()=>{ resetS(700); enc79RunChoiceFx('ngai_vouch'); return enc83HasCredit('credit_enc83_ngai_patron')===true; })());
ok('(2) ngai_vouch 冪等（一生一次）', (()=>{ const n = S.mockCredits.length; enc79RunChoiceFx('ngai_vouch'); return S.mockCredits.length===n; })());
ok('(2) registry：ngai_patron 無 grants()（債權改行 fx 通道）', beatOf('ngai_wingnaam','ngai_patron') && typeof beatOf('ngai_wingnaam','ngai_patron').grants==='undefined');
ok('(2) registry：其餘五線 patron grants() 照舊在位', ['lok_gasing','chai_zanhoi','pang_siuki','chung_choning','ching_tinlok'].every(sid=>{ const b = beatOf(sid, sid==='lok_gasing'?'lok_patron':sid==='chai_zanhoi'?'chai_patron':sid==='pang_siuki'?'pang_patron':sid==='chung_choning'?'chung_patron':'ching_patron'); return b && typeof b.grants==='function'; }));

/* ---- (3) GRANT229_ENC79 57 行：gig 在位＋key 唯一命中＋即派正確 ---- */
const SIX = ['駱家聲支線','魏詠男支線','齊鎮海支線','彭少祺支線','鍾楚凝支線','程天諾支線'];
const rows278 = GRANT229_ENC79.filter(r=>r && SIX.indexOf(r.source)>=0);
ok('(3) v278 行數＝57', rows278.length===57);
ok('(3) 全部 gig 在位（新庫 0 缺口）', rows278.every(r=>!!gigById(r.gigId)));
ok('(3) 全部 key 非空（無兜底行，「無即派」唔會錯派）', rows278.every(r=>String(r.key||'').length>0));
ok('(3) 每行 key 唯一命中同 seg 唯一一個 live 選項', rows278.every(r=>{
  const ls = labelsOf(r.seg);
  const hits = ls.filter(l=>l.indexOf(r.key)>=0);
  return hits.length===1;
}));
ok('(3) 即派逐行：揀中嗰個選項 → 派對應 gig（第二朝到期，一生一次）', (()=> {
  let bad = [];
  for(const r of rows278){
    resetS(800);
    const ls = labelsOf(r.seg);
    const lab = ls.find(l=>l.indexOf(r.key)>=0);
    if(!lab){ bad.push(r.seg+':'+r.key+':no-label'); continue; }
    const okRec = grant229RecordFromEnc79(r.seg, lab);
    const q = S.grant229Queue[0];
    if(!okRec || !q || q.gigId!==r.gigId || q.dueDay!==801) bad.push(r.seg+':'+r.key+'->'+(q&&q.gigId));
    grant229RecordFromEnc79(r.seg, lab);
    if(S.grant229Queue.length!==1) bad.push(r.seg+':'+r.key+':dup');
  }
  if(bad.length) console.log('  (3) bad rows: ' + bad.join(' | '));
  return bad.length===0;
})());
ok('(3) 無即派選項唔派：lok_foreshadow B／chai_fear B／ngai_patron A／lok_e4grudge A 全部無行', (()=> {
  resetS(810);
  const noRows = [
    ['beat:lok_foreshadow','同人講兩句，話佢為原創歌同高層嗌交'],
    ['beat:chai_fear','講兩句，話一哥都驚後生追上嚟'],
    ['beat:ngai_patron','照實講：佢得，佢企得穩'],
    ['beat:lok_e4grudge','勸他：榜是人排的，歌是自己的'],
  ];
  return noRows.every(([seg, lab])=> grant229RecordFromEnc79(seg, lab)===false && S.grant229Queue.length===0);
})());
ok('(3) 共用 gig 6 對在位（草稿重用同一舊 id，刻意保留）', ['gig_1991_rec_109','gig_1992_rec_107','gig_1992_rec_105','gig_1991_rec_202','gig_1991_film_205','gig_1990_film_210'].every(id=> rows278.filter(r=>r.gigId===id).length===2 && !!gigById(id)));

/* ---- (4) registry 閘門 ---- */
ok('(4) 新 beats 順序：駱 cover 排 help 之後、patron 冷版排暖版前、finale 排提攜之後', JSON.stringify((ENC79_BEATS.lok_gasing||[]).map(b=>b.id))===JSON.stringify(['lok_foreshadow','lok_intel','lok_help','lok_cover','lok_recover','lok_e4grudge','lok_patron_cold','lok_patron_cover','lok_patron','lok_finale']));
ok('(4) 新 beats 順序：魏 rain 排 repay 之後、patron 冷版排暖版前、finale 排提攜之後', JSON.stringify((ENC79_BEATS.ngai_wingnaam||[]).map(b=>b.id))===JSON.stringify(['ngai_intel','ngai_help','ngai_repay','ngai_rain','ngai_patron_cold','ngai_patron','ngai_finale']));
ok('(4) 新 beats 順序：齊 fear 排 intel 之後、patron 冷版排暖版前、finale 排提攜之後', JSON.stringify((ENC79_BEATS.chai_zanhoi||[]).map(b=>b.id))===JSON.stringify(['chai_intel','chai_fear','chai_choice','chai_repay','chai_patron_cold','chai_patron','chai_finale']));
ok('(4) 新 beats 順序：彭收尾排 n17 之後、patron 之前（冷版先）', JSON.stringify((ENC79_BEATS.pang_siuki||[]).map(b=>b.id))===JSON.stringify(['pang_intel','pang_help','pang_n17','pang_finale_cold','pang_finale','pang_patron']));
ok('(4) 新 beats 順序：鍾提攜排送別之前、程冷版 patron 排暖版前', JSON.stringify((ENC79_BEATS.chung_choning||[]).map(b=>b.id))===JSON.stringify(['chung_review','chung_intel','chung_f_clue','chung_patron_cold','chung_patron','chung_farewell']) && JSON.stringify((ENC79_BEATS.ching_tinlok||[]).map(b=>b.id))===JSON.stringify(['ching_e4','ching_rival','ching_after_train','ching_after_polish','ching_patron_cold','ching_patron']));
ok('(4) lok_cover 閘：T2–T3＋1991 冬＋lok_kept_row 先開', (()=>{ resetS(900); _ys={year:1991,season:'冬'}; setFav('lok_gasing',25); metStar('lok_gasing'); S.flags.lok_kept_row=1; const st=S.stars.lok_gasing; st.beatsDone.lok_foreshadow=1; st.beatsDone.lok_intel=1; st.beatsDone.lok_help=1; return enc79BeatOpen('lok_gasing', beatOf('lok_gasing','lok_cover'))===true; })());
ok('(4) lok_cover 閘：無 kept_row 唔開；T4 唔開', (()=>{ resetS(901); _ys={year:1991,season:'冬'}; setFav('lok_gasing',25); metStar('lok_gasing'); S.flags.lok_kept_row=0; const a = enc79BeatOpen('lok_gasing', beatOf('lok_gasing','lok_cover'))===false; setFav('lok_gasing',70); S.flags.lok_kept_row=1; const b = enc79BeatOpen('lok_gasing', beatOf('lok_gasing','lok_cover'))===false; return a && b; })());
ok('(4) ngai_rain 閘：T2＋N7 已做＋1991 夏–秋先開', (()=>{ resetS(902); _ys={year:1991,season:'夏'}; setFav('ngai_wingnaam',25); metStar('ngai_wingnaam'); _doneNodes.add('N7'); const st=S.stars.ngai_wingnaam; st.beatsDone.ngai_intel=1; st.beatsDone.ngai_help=1; st.beatsDone.ngai_repay=1; return enc79BeatOpen('ngai_wingnaam', beatOf('ngai_wingnaam','ngai_rain'))===true; })());
ok('(4) ngai_rain 閘：N7 未做唔開；1992 唔開', (()=>{ resetS(903); _ys={year:1991,season:'夏'}; setFav('ngai_wingnaam',25); metStar('ngai_wingnaam'); const a = enc79BeatOpen('ngai_wingnaam', beatOf('ngai_wingnaam','ngai_rain'))===false; _doneNodes.add('N7'); _ys={year:1992,season:'夏'}; const b = enc79BeatOpen('ngai_wingnaam', beatOf('ngai_wingnaam','ngai_rain'))===false; return a && b; })());
ok('(4) chai_fear 閘：T1–T2＋1990–1991＋N3 已做先開', (()=>{ resetS(904); _ys={year:1990,season:'秋'}; setFav('chai_zanhoi',10); metStar('chai_zanhoi'); _doneNodes.add('N3'); const st=S.stars.chai_zanhoi; st.beatsDone.chai_intel=1; return enc79BeatOpen('chai_zanhoi', beatOf('chai_zanhoi','chai_fear'))===true; })());
ok('(4) 延遲開：初遇 mock／walkaway／bluff／fake → 見多一次先開 Beat 2', (()=> {
  resetS(905); _ys={year:1990,season:'夏'};
  setFav('lok_gasing',10); const s1=metStar('lok_gasing'); s1.seen=1; S.flags.lok_first_mock=1;
  const a = enc79BeatOpen('lok_gasing', beatOf('lok_gasing','lok_foreshadow'))===false;
  s1.seen=2; const a2 = enc79BeatOpen('lok_gasing', beatOf('lok_gasing','lok_foreshadow'))===true;
  resetS(906); _ys={year:1991,season:'春'}; setFav('ngai_wingnaam',25); const s2=metStar('ngai_wingnaam'); s2.seen=1; S.flags.ngai_first_walkaway=1;
  const b = enc79BeatOpen('ngai_wingnaam', beatOf('ngai_wingnaam','ngai_help'))===false;
  s2.seen=2; const b2 = enc79BeatOpen('ngai_wingnaam', beatOf('ngai_wingnaam','ngai_help'))===true;
  resetS(907); _ys={year:1990,season:'秋'}; setFav('chai_zanhoi',10); const s3=metStar('chai_zanhoi'); s3.seen=1; S.flags.chai_first_bluff=1; _doneNodes.add('N3');
  const c = enc79BeatOpen('chai_zanhoi', beatOf('chai_zanhoi','chai_fear'))===false;
  s3.seen=2; const c2 = enc79BeatOpen('chai_zanhoi', beatOf('chai_zanhoi','chai_fear'))===true;
  resetS(908); _ys={year:1991,season:'春'}; setFav('pang_siuki',25); const s4=metStar('pang_siuki'); s4.seen=1; S.flags.pang_first_fake=1;
  const d = enc79BeatOpen('pang_siuki', beatOf('pang_siuki','pang_intel'))===false;
  s4.seen=2; const d2 = enc79BeatOpen('pang_siuki', beatOf('pang_siuki','pang_intel'))===true;
  return a && a2 && b && b2 && c && c2 && d && d2;
})());
ok('(4) 延遲開：無 mock 旗 → 見一次就開（唔係永久鎖）', (()=>{ resetS(909); _ys={year:1990,season:'夏'}; setFav('lok_gasing',10); const s=metStar('lok_gasing'); s.seen=1; return enc79BeatOpen('lok_gasing', beatOf('lok_gasing','lok_foreshadow'))===true; })());
ok('(4) ngai_repay 閘放寬：餐飯債權 OR ngai_tea 都開', (()=>{ resetS(910); setFav('ngai_wingnaam',25); metStar('ngai_wingnaam'); const st=S.stars.ngai_wingnaam; st.beatsDone.ngai_intel=1; st.beatsDone.ngai_help=1; const a = enc79BeatOpen('ngai_wingnaam', beatOf('ngai_wingnaam','ngai_repay'))===false; S.flags.ngai_tea=1; const b = enc79BeatOpen('ngai_wingnaam', beatOf('ngai_wingnaam','ngai_repay'))===true; return a && b; })());
ok('(4) ngai_repay 閘放寬：餐飯債權照開', (()=>{ resetS(911); setFav('ngai_wingnaam',25); metStar('ngai_wingnaam'); const st=S.stars.ngai_wingnaam; st.beatsDone.ngai_intel=1; st.beatsDone.ngai_help=1; enc79GrantCredit({ id:'credit_enc83_ngai_meal', debtor:'魏詠男', title:'一餐飯嘅人情', line:'x', status:'未收' }); return enc79BeatOpen('ngai_wingnaam', beatOf('ngai_wingnaam','ngai_repay'))===true; })());
ok('(4) chai_repay 閘：chai_silent 嗰陣唔開（回報唔開，冷後果由 patron 冷版承接）', (()=>{ resetS(912); setFav('chai_zanhoi',25); metStar('chai_zanhoi'); _doneNodes.add('N13'); const st=S.stars.chai_zanhoi; st.beatsDone.chai_intel=1; st.beatsDone.chai_fear=1; st.beatsDone.chai_choice=1; const a = enc79BeatOpen('chai_zanhoi', beatOf('chai_zanhoi','chai_repay'))===true; S.flags.chai_silent=1; const b = enc79BeatOpen('chai_zanhoi', beatOf('chai_zanhoi','chai_repay'))===false; return a && b; })());
ok('(4) 暖版 patron 排除式閘：駱 loose_row／join_rant／cover_first 任一 → 暖版唔開，冷版開', (()=> {
  const cases = [['lok_loose_row','lok_patron_cold'],['lok_join_rant','lok_patron_cold'],['lok_cover_first','lok_patron_cover']];
  return cases.every(([flag, coldId])=>{ resetS(913); setFav('lok_gasing',70); const st=metStar('lok_gasing'); ['lok_foreshadow','lok_intel','lok_help','lok_cover','lok_recover','lok_e4grudge'].forEach(id=>st.beatsDone[id]=1); S.flags[flag]=1; return enc79BeatOpen('lok_gasing', beatOf('lok_gasing','lok_patron'))===false && enc79BeatOpen('lok_gasing', beatOf('lok_gasing',coldId))===true && enc79PickBeat('lok_gasing').id===coldId; });
})());
ok('(4) 暖版 patron 排除式閘：魏 hold_back／honest → 暖版唔開，冷版開', (()=> {
  return ['ngai_rain_hold_back','ngai_patron_honest'].every(flag=>{ resetS(914); setFav('ngai_wingnaam',70); const st=metStar('ngai_wingnaam'); ['ngai_intel','ngai_help','ngai_repay','ngai_rain'].forEach(id=>st.beatsDone[id]=1); S.flags[flag]=1; return enc79BeatOpen('ngai_wingnaam', beatOf('ngai_wingnaam','ngai_patron'))===false && enc79BeatOpen('ngai_wingnaam', beatOf('ngai_wingnaam','ngai_patron_cold'))===true && enc79PickBeat('ngai_wingnaam').id==='ngai_patron_cold'; });
})());
ok('(4) 暖版 patron 排除式閘：齊 silent／comfort／loose_fear 任一 → 暖版唔開，冷版開', (()=> {
  return ['chai_silent','chai_comfort','chai_loose_fear'].every(flag=>{ resetS(915); setFav('chai_zanhoi',70); metStar('chai_zanhoi'); S.flags[flag]=1; return enc79BeatOpen('chai_zanhoi', beatOf('chai_zanhoi','chai_patron'))===false && enc79BeatOpen('chai_zanhoi', beatOf('chai_zanhoi','chai_patron_cold'))===true; });
})());
ok('(4) 暖版 patron 排除式閘：鍾 loose_talk／asked_return → 暖版唔開，冷版開', (()=> {
  return ['chung_loose_talk','chung_asked_return'].every(flag=>{ resetS(916); setFav('chung_choning',70); metStar('chung_choning'); S.flags[flag]=1; return enc79BeatOpen('chung_choning', beatOf('chung_choning','chung_patron'))===false && enc79BeatOpen('chung_choning', beatOf('chung_choning','chung_patron_cold'))===true; });
})());
ok('(4) 暖版 patron 排除式閘：程 polish／back_polish／stand_fast → 暖版唔開，冷版開', (()=> {
  const cases = [['flag_vocal_polish','story'],['ching_back_polish','flags'],['ching_stand_fast','flags']];
  return cases.every(([flag, store])=>{ resetS(917); setFav('ching_tinlok',70); metStar('ching_tinlok'); if(store==='story') S.story.flags[flag]=1; else S.flags[flag]=1; return enc79BeatOpen('ching_tinlok', beatOf('ching_tinlok','ching_patron'))===false && enc79BeatOpen('ching_tinlok', beatOf('ching_tinlok','ching_patron_cold'))===true; });
})());
ok('(4) 暖版 patron：程要 N15 苦練旗先開（無 train 旗 → 暖／冷都唔開）', (()=>{ resetS(918); setFav('ching_tinlok',70); metStar('ching_tinlok'); return enc79BeatOpen('ching_tinlok', beatOf('ching_tinlok','ching_patron'))===false && enc79BeatOpen('ching_tinlok', beatOf('ching_tinlok','ching_patron_cold'))===false; })());
ok('(4) 暖版 patron：程有 train 旗＋無壞旗 → 暖版開', (()=>{ resetS(919); setFav('ching_tinlok',70); const st=metStar('ching_tinlok'); ['ching_e4','ching_rival','ching_after_train','ching_after_polish'].forEach(id=>st.beatsDone[id]=1); S.story.flags.flag_vocal_train=1; return enc79BeatOpen('ching_tinlok', beatOf('ching_tinlok','ching_patron'))===true && enc79PickBeat('ching_tinlok').id==='ching_patron'; })());
ok('(4) 暖版 patron：無壞旗 → 六線暖版照開', (()=> {
  return [['lok_gasing','lok_patron'],['ngai_wingnaam','ngai_patron'],['chai_zanhoi','chai_patron'],['chung_choning','chung_patron']].every(([sid, pid])=>{ resetS(920); setFav(sid,70); metStar(sid); return enc79BeatOpen(sid, beatOf(sid,pid))===true; });
})());
ok('(4) 彭收尾：好收尾要 cover＋listened＋noodle＋n17 已播', (()=>{ resetS(921); _ys={year:1992,season:'冬'}; setFav('pang_siuki',45); const st=metStar('pang_siuki'); st.beatsDone.pang_intel=1; st.beatsDone.pang_help=1; st.beatsDone.pang_n17=1; S.flags.pang_cover_night=1; S.flags.pang_listened=1; S.flags.pang_noodle_night=1; return enc79BeatOpen('pang_siuki', beatOf('pang_siuki','pang_finale'))===true && enc79PickBeat('pang_siuki').id==='pang_finale'; })());
ok('(4) 彭收尾：absent／brushed_off／early_night 任一 → 冷收尾開，好收尾唔開', (()=> {
  return ['pang_absent_night','pang_brushed_off','pang_early_night'].every(flag=>{ resetS(922); _ys={year:1992,season:'冬'}; setFav('pang_siuki',45); const st=metStar('pang_siuki'); st.beatsDone.pang_intel=1; st.beatsDone.pang_help=1; st.beatsDone.pang_n17=1; S.flags[flag]=1; return enc79BeatOpen('pang_siuki', beatOf('pang_siuki','pang_finale_cold'))===true && enc79BeatOpen('pang_siuki', beatOf('pang_siuki','pang_finale'))===false; });
})());
ok('(4) 彭收尾：n17 未播 → 兩收尾都唔開', (()=>{ resetS(923); _ys={year:1992,season:'冬'}; setFav('pang_siuki',45); metStar('pang_siuki'); S.flags.pang_cover_night=1; S.flags.pang_listened=1; S.flags.pang_noodle_night=1; return enc79BeatOpen('pang_siuki', beatOf('pang_siuki','pang_finale'))===false && enc79BeatOpen('pang_siuki', beatOf('pang_siuki','pang_finale_cold'))===false; })());

/* ---- (5) BuildScript 變體＋heart 分流＋ngai_repay 冷版 ---- */
function heartBuild(sid, fav, ys, flags){
  resetS(950); _ys = ys || {year:1992,season:'冬'};
  setFav(sid, fav||45);
  const st = doneAllBeats(sid);
  st.heartDone = false;
  Object.assign(S.flags, flags||{});
  return enc79BuildScript(sid, false);
}
ok('(5) heart 排除：駱 loose_row → 暖版 heart 唔播（行 pool）', (()=>{ const b = heartBuild('lok_gasing',45,{year:1992,season:'冬'},{lok_loose_row:1}); return b && !b.steps.some(s=>s.seg==='heart:lok_gasing'); })());
ok('(5) heart 排除：魏 hold_back → 暖版 heart 唔播', (()=>{ const b = heartBuild('ngai_wingnaam',45,{year:1992,season:'冬'},{ngai_rain_hold_back:1}); return b && !b.steps.some(s=>s.seg==='heart:ngai_wingnaam'); })());
ok('(5) heart 排除：齊 loose_fear → 暖版 heart 唔播', (()=>{ const b = heartBuild('chai_zanhoi',45,{year:1992,season:'冬'},{chai_loose_fear:1}); return b && !b.steps.some(s=>s.seg==='heart:chai_zanhoi'); })());
ok('(5) heart 排除：彭 absent_night → 暖版 heart 唔播', (()=>{ const b = heartBuild('pang_siuki',45,{year:1992,season:'冬'},{pang_absent_night:1}); return b && !b.steps.some(s=>s.seg==='heart:pang_siuki'); })());
ok('(5) heart 排除：無壞旗 → 暖版 heart 照播', (()=>{ const b = heartBuild('lok_gasing',45,{year:1992,season:'冬'},{}); return b && b.steps.some(s=>s.seg==='heart:lok_gasing'); })());
ok('(5) 鍾冷版 heart：loose_talk → 播 heartCold（金鐘細房 4 句），唔播暖版 heart', (()=>{ const b = heartBuild('chung_choning',45,{year:1992,season:'冬'},{chung_loose_talk:1}); return b && hasText(b,'金鐘創意一間細房') && hasText(b,'阿偉，今日唔傾喇') && !hasText(b,'阿偉，坐啦，唔使成日企'); })());
ok('(5) 鍾暖版 heart：無 loose_talk → 播暖版 heart（金鐘小房間）', (()=>{ const b = heartBuild('chung_choning',45,{year:1992,season:'冬'},{}); return b && hasText(b,'金鐘創意一間小房間') && !hasText(b,'阿偉，今日唔傾喇'); })());
ok('(5) 齊 silent heart：尾句問句換走＋choices 剝走（Beat 4 抉擇唔開）', (()=>{ const b = heartBuild('chai_zanhoi',45,{year:1992,season:'冬'},{chai_silent:1}); const heartSteps = (b&&b.steps||[]).filter(s=>s.seg==='heart:chai_zanhoi'); return b && heartSteps.length>0 && !heartSteps.some(s=>String(s.text||'').indexOf('你覺得我應該點行')>=0) && hasText(b,'你唔使答我，我自己諗') && !b.steps.some(s=>s.choice && s.seg==='heart:chai_zanhoi'); })());
ok('(5) 齊 advise_stop heart：首句前插「你講中晒。」', (()=>{ const b = heartBuild('chai_zanhoi',45,{year:1992,season:'冬'},{chai_advise_stop:1}); const hs = (b&&b.steps||[]).filter(s=>s.seg==='heart:chai_zanhoi'); return b && hs.length>0 && hs[0].text==='你講中晒。'; })());
ok('(5) 程 back_polish heart：首句換做「今晚唔講喇。」', (()=>{ const b = heartBuild('ching_tinlok',45,{year:1992,season:'冬'},{ching_back_polish:1}); const hs = (b&&b.steps||[]).filter(s=>s.seg==='heart:ching_tinlok'); return b && hs.length>0 && hs[0].text==='今晚唔講喇。'; })());
ok('(5) 程 stayed_late heart：第 2 位插認領句「佢記得你嗰晚留低過」', (()=>{ const b = heartBuild('ching_tinlok',45,{year:1992,season:'冬'},{ching_stayed_late:1}); return b && hasText(b,'佢記得你嗰晚留低過，肯同你講真話'); })());
ok('(5) 程 back_polish 優先於 stayed_late（冷開場壓過認領句）', (()=>{ const b = heartBuild('ching_tinlok',45,{year:1992,season:'冬'},{ching_back_polish:1,ching_stayed_late:1}); const hs = (b&&b.steps||[]).filter(s=>s.seg==='heart:ching_tinlok'); return b && hs.length>0 && hs[0].text==='今晚唔講喇。' && !hasText(b,'佢記得你嗰晚留低過'); })());
ok('(5) 駱 heart tried：問句「呢段你聽唔聽得出我想講咩」插喺「你聽清楚，呢一段」之後', (()=>{ const b = heartBuild('lok_gasing',45,{year:1992,season:'冬'},{lok_tried_harmony:1}); const hs = (b&&b.steps||[]).filter(s=>s.seg==='heart:lok_gasing').map(s=>s.text); const i = hs.indexOf('呢段你聽唔聽得出我想講咩？'); return b && i>0 && hs[i-1].indexOf('你聽清楚，呢一段')===0; })());
ok('(5) 駱 heart cover_first：關鍵句換成懷疑版（v20a308 Q20：唔再插入停低句，換句唔係加句）', (()=>{ const b = heartBuild('lok_gasing',45,{year:1992,season:'冬'},{lok_cover_first:1}); const hs = (b&&b.steps||[]).filter(s=>s.seg==='heart:lok_gasing' && !s.choice).map(s=>s.text); return b && hs.length===12 && hs[10]==='不過呢，阿偉，歌係自己嘅——呢句我講咗咁多年，而家先發覺，我連自己仲唱唔唱得出，都唔敢肯定。你明唔明？' && hs.indexOf('不過呢，阿偉，歌係自己嘅，嗰種實淨，冇人攞得走。你明唔明？')<0 && hs.indexOf('呢首，我唔知仲唱唔唱得出。')<0; })());
ok('(5) 駱 heart honest：收尾附加「有啲歌，我而家唱畀你聽，你都未必接得住」', (()=>{ const b = heartBuild('lok_gasing',45,{year:1992,season:'冬'},{lok_honest_not_ready:1}); const hs = (b&&b.steps||[]).filter(s=>s.seg==='heart:lok_gasing').map(s=>s.text).filter(t=>t!=null); return b && hs[hs.length-1]==='有啲歌，我而家唱畀你聽，你都未必接得住。'; })());
ok('(5) 駱 heart 三變體可疊加（tried＋cover_first＋honest 齊在位）', (()=>{ const b = heartBuild('lok_gasing',45,{year:1992,season:'冬'},{lok_tried_harmony:1,lok_cover_first:1,lok_honest_not_ready:1}); return b && hasText(b,'呢段你聽唔聽得出我想講咩') && hasText(b,'我連自己仲唱唔唱得出，都唔敢肯定') && !hasText(b,'呢首，我唔知仲唱唔唱得出') && hasText(b,'有啲歌，我而家唱畀你聽，你都未必接得住'); })());
ok('(5) 駱 foreshadow stand：認領 N 行插喺開場（走廊肯出聲嗰個）', (()=>{ resetS(951); _ys={year:1990,season:'夏'}; setFav('lok_gasing',10); metStar('lok_gasing'); S.flags.lok_first_stand=1; const b = enc79BuildScript('lok_gasing', false); return b && hasText(b,'佢認得你——走廊嗰陣，肯出聲為佢講句好話嗰個'); })());
ok('(5) 駱 patron heard_whole／praised_song：監製飯局句插喺「約咗監製老友食飯」之後', (()=> {
  const run = (flag, line)=>{ resetS(952); setFav('lok_gasing',70); const st=metStar('lok_gasing'); st.beatsDone.lok_foreshadow=1; st.beatsDone.lok_intel=1; st.beatsDone.lok_help=1; st.beatsDone.lok_cover=1; st.beatsDone.lok_recover=1; st.beatsDone.lok_e4grudge=1; S.flags[flag]=1; const b = enc79BuildScript('lok_gasing', false); const ps = (b&&b.steps||[]).filter(s=>s.seg==='beat:lok_patron').map(s=>s.text); const i = ps.indexOf(line); return b && i>0 && ps[i-1].indexOf('我約咗一位唱片監製老友食飯')===0; };
  return run('lok_heard_whole','呢個後生仔，肯由頭聽到尾。') && run('lok_praised_song','呢個後生仔，識聽。');
})());
ok('(5) 魏 help soda：開場插「你嚟得啱。」', (()=>{ resetS(953); _ys={year:1991,season:'春'}; setFav('ngai_wingnaam',25); metStar('ngai_wingnaam'); S.stars.ngai_wingnaam.beatsDone.ngai_intel=1; S.flags.ngai_first_soda=1; const b = enc79BuildScript('ngai_wingnaam', false); const hs = (b&&b.steps||[]).filter(s=>s.seg==='beat:ngai_help').map(s=>s.text); return b && hs[1]==='你嚟得啱。'; })());
ok('(5) 魏 rain serious／later：企位變體插喺「想起嗰句」之後', (()=> {
  const run = (flag, sub)=>{ resetS(954); _ys={year:1991,season:'夏'}; setFav('ngai_wingnaam',25); metStar('ngai_wingnaam'); _doneNodes.add('N7'); const st=S.stars.ngai_wingnaam; st.beatsDone.ngai_intel=1; st.beatsDone.ngai_help=1; st.beatsDone.ngai_repay=1; S.flags[flag]=1; const b = enc79BuildScript('ngai_wingnaam', false); return b && hasText(b, sub); };
  return run('ngai_learn_serious','佢企得穩，落地屈膝卸力') && run('ngai_learn_later','佢企位唔穩，武指要嗌多句');
})());
ok('(5) 魏 patron learn：插「你係肯跌嗰個。」；shy：收尾附加「肯跌，先學得嚟。」', (()=> {
  const run = (flag)=>{ resetS(955); setFav('ngai_wingnaam',70); metStar('ngai_wingnaam'); const st=S.stars.ngai_wingnaam; st.beatsDone.ngai_intel=1; st.beatsDone.ngai_help=1; st.beatsDone.ngai_repay=1; st.beatsDone.ngai_rain=1; S.flags[flag]=1; const b = enc79BuildScript('ngai_wingnaam', false); return b; };
  const b1 = run('ngai_heart_learn'); const ps1 = (b1&&b1.steps||[]).filter(s=>s.seg==='beat:ngai_patron').map(s=>s.text);
  const b2 = run('ngai_heart_shy'); const ps2 = (b2&&b2.steps||[]).filter(s=>s.seg==='beat:ngai_patron').map(s=>s.text).filter(t=>t!=null);
  return ps1[1]==='你係肯跌嗰個。' && ps2[ps2.length-1]==='肯跌，先學得嚟。';
})());
ok('(5) 齊 intel right：插「上次嗰場戲之後，我有留意你，你開工幾定性。」', (()=>{ resetS(956); _ys={year:1990,season:'秋'}; setFav('chai_zanhoi',25); metStar('chai_zanhoi'); S.flags.chai_first_right=1; const b = enc79BuildScript('chai_zanhoi', false); const is = (b&&b.steps||[]).filter(s=>s.seg==='beat:chai_intel').map(s=>s.text); return b && is[1]==='上次嗰場戲之後，我有留意你，你開工幾定性。'; })());
ok('(5) 彭 intel admire：認領 N 行插喺開場', (()=>{ resetS(957); _ys={year:1991,season:'春'}; setFav('pang_siuki',25); metStar('pang_siuki'); S.flags.pang_first_admire=1; const b = enc79BuildScript('pang_siuki', false); return b && hasText(b,'佢認得你——嗰個讚佢記性嘅後生仔'); })());
ok('(5) 鍾 intel 三變體：humble／silent／backtalk 各插認領 N 行', (()=> {
  const run = (flag, sub)=>{ resetS(958); _ys={year:1991,season:'秋'}; setFav('chung_choning',25); metStar('chung_choning'); const st=S.stars.chung_choning; st.beatsDone.chung_review=1; S.flags[flag]=1; const b = enc79BuildScript('chung_choning', false); return b && hasText(b, sub); };
  return run('chung_first_humble','佢認得你——嗰個肯聽嘅後生仔') && run('chung_first_silent','佢記得你企姿定咗少少') && run('chung_first_backtalk','佢記住你係嗰個頂嘴嘅臨記');
})());
ok('(5) 鍾 patron tried：插「佢去試過嗰邊。」', (()=>{ resetS(959); setFav('chung_choning',70); metStar('chung_choning'); const st=S.stars.chung_choning; st.beatsDone.chung_review=1; st.beatsDone.chung_intel=1; st.beatsDone.chung_f_clue=1; st.beatsDone.chung_farewell=1; S.flags.chung_tried_director=1; const b = enc79BuildScript('chung_choning', false); const ps = (b&&b.steps||[]).filter(s=>s.seg==='beat:chung_patron').map(s=>s.text); return b && ps[1]==='佢去試過嗰邊。'; })());
ok('(5) 程 rival 三變體：grit／water／blunt 各插認領 N 行', (()=> {
  const run = (flag, sub)=>{ resetS(960); _ys={year:1992,season:'秋'}; setFav('ching_tinlok',10); metStar('ching_tinlok'); S.flags[flag]=1; const b = enc79BuildScript('ching_tinlok', false); return b && hasText(b, sub); };
  return run('ching_first_grit','佢記得你——嗰個練到天光嘅臨記') && run('ching_first_water','佢記得你——嗰個唔出聲嘅人') && run('ching_first_blunt','佢記得你夠膽講真話');
})());
ok('(5) 魏 repay 冷版：ngai_tea（無餐飯債權）→ 第 2 句換做順手教', (()=>{ resetS(961); setFav('ngai_wingnaam',25); metStar('ngai_wingnaam'); const st=S.stars.ngai_wingnaam; st.beatsDone.ngai_intel=1; st.beatsDone.ngai_help=1; S.flags.ngai_tea=1; const b = enc79BuildScript('ngai_wingnaam', false); return b && hasText(b,'今日得閒，順手教你兵器套路') && !hasText(b,'上次你幫過我，我魏詠男唔欠人嘅'); })());
ok('(5) 魏 repay 暖版：有餐飯債權 → 第 2 句照舊「還人情」', (()=>{ resetS(962); setFav('ngai_wingnaam',25); metStar('ngai_wingnaam'); const st=S.stars.ngai_wingnaam; st.beatsDone.ngai_intel=1; st.beatsDone.ngai_help=1; enc79GrantCredit({ id:'credit_enc83_ngai_meal', debtor:'魏詠男', title:'一餐飯嘅人情', line:'x', status:'未收' }); const b = enc79BuildScript('ngai_wingnaam', false); return b && hasText(b,'上次你幫過我，我魏詠男唔欠人嘅') && !hasText(b,'今日得閒，順手教'); })());
ok('(5) 冷版 patron beats 播得出：lok_patron_cold／ngai_patron_cold／chai_patron_cold／chung_patron_cold／ching_patron_cold／lok_patron_cover', (()=> {
  const cases = [
    ['lok_gasing','lok_patron_cold',{lok_loose_row:1},70],
    ['ngai_wingnaam','ngai_patron_cold',{ngai_rain_hold_back:1},70],
    ['chai_zanhoi','chai_patron_cold',{chai_silent:1},70],
    ['chung_choning','chung_patron_cold',{chung_loose_talk:1},70],
    ['ching_tinlok','ching_patron_cold',{ching_stand_fast:1},70],
    ['lok_gasing','lok_patron_cover',{lok_cover_first:1},70],
  ];
  return cases.every(([sid, bid, flags, fav])=>{ resetS(963); setFav(sid, fav); const st=metStar(sid); for(const b of (ENC79_BEATS[sid]||[])) if(b.id!==bid) st.beatsDone[b.id]=1; Object.assign(S.flags, flags); const built = enc79BuildScript(sid, false); return built && built.steps.some(s=>s.seg==='beat:'+bid); });
})());
ok('(5) 彭收尾 beats 播得出：pang_finale／pang_finale_cold', (()=> {
  const run = (flags, bid)=>{ resetS(964); _ys={year:1992,season:'冬'}; setFav('pang_siuki',45); const st=metStar('pang_siuki'); st.beatsDone.pang_intel=1; st.beatsDone.pang_help=1; st.beatsDone.pang_n17=1; Object.assign(S.flags, flags); const b = enc79BuildScript('pang_siuki', false); return b && b.steps.some(s=>s.seg==='beat:'+bid); };
  return run({pang_cover_night:1,pang_listened:1,pang_noodle_night:1},'pang_finale') && run({pang_absent_night:1},'pang_finale_cold');
})());

/* ---- (6) 靜態 guard ---- */
const FLAGS278 = ['lok_first_stand','lok_first_quiet','lok_first_mock','lok_kept_row','lok_loose_row','lok_tried_harmony','lok_honest_not_ready','lok_stand_original','lok_cover_first','lok_heard_whole','lok_praised_song','lok_calm_truth','lok_join_rant','ngai_first_soda','ngai_first_tissue','ngai_first_walkaway','ngai_meal_treat','ngai_tea','ngai_walk_past','ngai_learn_serious','ngai_learn_later','ngai_rain_stand','ngai_rain_hold_back','ngai_heart_learn','ngai_heart_shy','ngai_patron_vouch','ngai_patron_honest','chai_first_right','chai_first_honest','chai_first_bluff','chai_kept_fear','chai_loose_fear','chai_advise_stop','chai_silent','chai_truth_change','chai_comfort','chai_try_new','chai_play_safe','pang_first_admire','pang_first_polite','pang_first_fake','pang_showed_up','pang_late','pang_cover_night','pang_absent_night','pang_listened','pang_brushed_off','pang_noodle_night','pang_early_night','chung_first_humble','chung_first_silent','chung_first_backtalk','chung_tried_director','chung_stayed_lane','chung_kept_quiet','chung_loose_talk','chung_listened','chung_asked_return','ching_first_grit','ching_first_water','ching_first_blunt','ching_stayed_late','ching_left_early','ching_back_train','ching_back_polish','ching_stand_slow','ching_stand_fast'];
ok('(6) 67 支草稿旗全部落 DLG flags 欄位（各 1 次）', FLAGS278.length===67 && FLAGS278.every(f=> (html.match(new RegExp('flags: \\["'+f.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'"\]', 'g'))||[]).length===1));
ok('(6) 新 beats DLG 在位：lok_cover／ngai_rain／chai_fear／6 冷版 patron／2 彭收尾／heartCold', ['lok_cover','ngai_rain','chai_fear','lok_patron_cold','lok_patron_cover','ngai_patron_cold','chai_patron_cold','chung_patron_cold','ching_patron_cold','pang_finale','pang_finale_cold'].every(bid=>{ const D = ENC79_DIALOG[bid.indexOf('lok_')===0?'lok_gasing':bid.indexOf('ngai_')===0?'ngai_wingnaam':bid.indexOf('chai_')===0?'chai_zanhoi':bid.indexOf('pang_')===0?'pang_siuki':bid.indexOf('chung_')===0?'chung_choning':'ching_tinlok']; return D && D.beats && D.beats[bid] && (D.beats[bid].lines||[]).length>=1; }) && !!ENC79_DIALOG.chung_choning.heartCold && ENC79_DIALOG.chung_choning.heartCold.lines.length===4);
ok('(6) 新 labels 一律廣東話（新抉擇 label 無書面語「說／這些／那個」字眼）', (()=>{ const newLabels = [...beatLabels('lok_gasing','lok_foreshadow'),...beatLabels('lok_gasing','lok_cover'),...beatLabels('ngai_wingnaam','ngai_rain'),...beatLabels('chai_zanhoi','chai_fear'),...beatLabels('pang_siuki','pang_intel'),...beatLabels('chung_choning','chung_intel'),...beatLabels('chung_choning','chung_f_clue'),...beatLabels('ching_tinlok','ching_rival'),...beatLabels('ching_tinlok','ching_e4'),...beatLabels('ngai_wingnaam','ngai_patron'),...beatLabels('chai_zanhoi','chai_repay'),...beatLabels('pang_siuki','pang_n17')]; return newLabels.length===24 && newLabels.every(l=>l.indexOf('說')<0 && l.indexOf('這些')<0 && l.indexOf('那個')<0); })());
ok('(6) 唔改 SAVE key／softRev／?v=（v278 只改內容）', html.indexOf('starVolunteer_map_v19w')>=0 && html.indexOf('"s107"')>=0 && html.indexOf('v20a10')>=0);

console.log(fails.length ? ('FAILURES: ' + fails.length + '\n' + fails.join('\n')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
