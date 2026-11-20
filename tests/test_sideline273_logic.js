// v20a356 resync：支線複檢 (a) 類修復改咗 ENC 釘句（齊 wrap／駱 patron_cold／彭 finale_cold＋n17／程 e4／魏 heartCold／駱 heart label／彭 intel label／齊 choice GRANT key），釘句同步更新，邏輯斷言唔郁。
// v20a273 支線實裝第三批邏輯測試：(a) 顧 heart fx 關鍵字修復、(b) 顧 Beat 2 天台抉擇實裝、
//   (c) 其餘六線 code 側核實（fx 關鍵字再發現 3 處同類 bug＋草稿旗 0 命中盤點）、
//   (d) PLAN §10 即派第一批 25 項核實（BR89 13 對／G-G2／免試鏡渠道／忠告卡／已刪／已核實項）、
//   (e) 陸 heart foreshadow 放寬。
// 反證：喺 pristine（v20a271）index 上行 → (a)(b)(c) fx／抉擇／讀返斷言乾淨 FAIL；(d) 靜態核實項本身已在位（v229／v254／v158）。
// 用法：node tests/test_sideline273_logic.js [path-to-index.html]
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

/* ---- sandbox（ENC79＋GRANT229 實函數＋BR89／favor158／忠告卡） ---- */
let S;
let _ys = { year: 1990, season: '春' };
let _doneNodes = new Set();
function resetS(day){
  S = { dayIndex: day||0, fame: 0, money: 2000, flags: {}, npcs: { agent: 0 }, mockRumors: [], mockDebts: [], mockCredits: [], board: {}, shoots: [], mapTips: {}, story: { flags: {} }, starWeek: {}, weekGigsDone: 0, starWhispers: {}, grant229Queue: [], pendingAud: [], news82: { pub: {}, arc: {} } };
  _doneNodes = new Set();
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
const consts273 = ['ENC79_TIER_NAMES','ENC79_PLAYER_TIERS','ENC79_FAV_CAPS','ENC79_STARS','ENC79_PILOT','ENC79_STAGEUP','ENC79_CAP_LINES','ENC79_WRAP_ECHO','ENC79_BEATS','ENC79_DIALOG','ENC79_FIRST_ALT98'].map(n=> asVar(extractConst(n), n)).join('\n')
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
const fns273 = ['enc79StarDef','enc79Hash','enc79Rand','enc79EnsureStars','enc79StarState','enc79TierOf','enc79PlayerTier','enc79FavCap','enc79AddFav','enc79WhisperActive','enc79GrantWhisper','enc79GrantCredit','enc79BoardHasStar','enc79BoardHasActionGig','enc79BeatOpen','enc79AnyBeatOpen','enc79PickBeat','enc79ChoiceFx','enc79RunChoiceFx','enc79NormSeg','enc79BuildScript','enc83NodeDone','enc83Flag','enc83HasCredit','enc83NewsOut','contra98EncFirstLocSwap','grant229Ensure','grant229GigById','grant229Record','grant229RecordDraft','br89HasCredit','br89GigOn','favor158CreditHeld','isMakWuzhiGig158','isPangCharityGig158','pangHalvedStageReq158','pangEffectiveGig158','pangChannelReady158','favor158ChannelForGig','chungAdviceCardHeld229','isWenyiAuditionGig229','chungAdviceTipForAudition229','chungAdviceSpend229'];
eval(consts273 + '\n' + asVar(extractConst('BR89_PATRON_OF_GIG'), 'BR89_PATRON_OF_GIG') + '\n' + asVar(extractConst('GRANT229_DRAFT'), 'GRANT229_DRAFT') + '\n' + asVar(extractConst('GRANT229_ENC79'), 'GRANT229_ENC79') + '\n' + asVar(extractConst('FAVOR158_MAK_CREDIT_ID'), 'FAVOR158_MAK_CREDIT_ID') + '\n' + asVar(extractConst('FAVOR158_PANG_CREDIT_ID'), 'FAVOR158_PANG_CREDIT_ID') + '\n' + asVar(extractConst('CHUNG_ADVICE_TEXT229'), 'CHUNG_ADVICE_TEXT229') + '\n' + t4Region + '\n' + enc84Region + '\n' + fns273.map(extractFn).join('\n'));

/* ---- (a) 顧 heart fx：跟 live label「陪他坐到天亮，不出聲」 ---- */
ok('(a) DLG label 在位：顧 heart 首選係「陪他坐到天亮，不出聲」', ENC83_DLG_gu_mingfai.heart.choices[0].label==='陪他坐到天亮，不出聲');
ok('(a) heart fx：陪到天亮 +3／勸戒賭 +1', enc79ChoiceFx('heart:gu_mingfai','陪他坐到天亮，不出聲').fav===3 && enc79ChoiceFx('heart:gu_mingfai','勸他戒賭，重新來過').fav===1);
ok('(a) 回歸 guard：舊廣東話 label「陪佢坐到天光」唔再命中（fx 跟 live label，唔跟舊詞）', enc79ChoiceFx('heart:gu_mingfai','陪佢坐到天光，唔出聲').fav===1);
ok('(a) 靜態：fx 行寫「天亮」，舊「天光」關鍵字已清', html.includes('has("天亮")?3:1') && !html.includes('if(segKey==="heart:gu_mingfai") return { fav: has("天光")'));

/* ---- (b) 顧 Beat 2 天台抉擇：gu_tease 兩選項＋寫旗＋即派分開＋後續讀取 ---- */
ok('(b) DLG：gu_tease 有兩選項（應承／問返），旗 gu_promise_clean／gu_ask_back', (()=>{ const ch = ENC83_DLG_gu_mingfai.beats.gu_tease.choices||[]; return ch.length===2 && ch[0].label==='應承他，自己一世都不碰賭' && JSON.stringify(ch[0].flags)==='["gu_promise_clean"]' && ch[1].label==='問回他：「那你自己呢？」' && JSON.stringify(ch[1].flags)==='["gu_ask_back"]'; })());
ok('(b) fx：應承 +2／fx gu_promise_clean；問返 +2／fx gu_ask_back', (()=>{ const a=enc79ChoiceFx('beat:gu_tease','應承他，自己一世都不碰賭'); const b=enc79ChoiceFx('beat:gu_tease','問回他：「那你自己呢？」'); return a.fav===2 && a.fx==='gu_promise_clean' && b.fav===2 && b.fx==='gu_ask_back'; })());
ok('(b) 即派：應承 → GRANT229_DRAFT rec_201（第二朝到期）', (()=>{ resetS(600); enc79RunChoiceFx('gu_promise_clean'); return S.grant229Queue.length===1 && S.grant229Queue[0].gigId==='gig_1991_rec_201' && S.grant229Queue[0].dueDay===601; })());
ok('(b) 即派：一生一次（重覆揀唔重派）', (()=>{ enc79RunChoiceFx('gu_promise_clean'); return S.grant229Queue.length===1; })());
ok('(b) 即派：問返 → rec_207，兩邊分開派', (()=>{ resetS(610); enc79RunChoiceFx('gu_ask_back'); return S.grant229Queue.length===1 && S.grant229Queue[0].gigId==='gig_1991_rec_207' && S.grant229Queue[0].dueDay===611; })());
ok('(b) 閘：gu_tease 1991＋T2＋N10 未完先開；PickBeat 排 loan 之前', (()=>{ resetS(620); _ys = { year:1991, season:'春' }; setFav('gu_mingfai', 25); metStar('gu_mingfai'); S.stars.gu_mingfai.beatsDone.gu_foreshadow = 1; return enc79BeatOpen('gu_mingfai', beatOf('gu_mingfai','gu_tease'))===true && enc79PickBeat('gu_mingfai').id==='gu_tease'; })());
ok('(b) 讀返 Beat 3：有 gu_promise_clean → gu_loan 開場插「你嗰日應承過我」', (()=>{ resetS(621); _ys = { year:1991, season:'夏' }; setFav('gu_mingfai', 25); metStar('gu_mingfai'); S.flags.gu_promise_clean = 1; const st = S.stars.gu_mingfai; st.beatsDone.gu_foreshadow = 1; st.beatsDone.gu_tease = 1; const built = enc79BuildScript('gu_mingfai', false); return !!built && built.steps.some(s=>String(s.text||'').indexOf('你嗰日應承過我，今日我先敢同你開口')>=0); })());
ok('(b) 讀返 Beat 3：無旗 → 唔插句', (()=>{ resetS(622); _ys = { year:1991, season:'夏' }; setFav('gu_mingfai', 25); metStar('gu_mingfai'); const st = S.stars.gu_mingfai; st.beatsDone.gu_foreshadow = 1; st.beatsDone.gu_tease = 1; const built = enc79BuildScript('gu_mingfai', false); return !!built && !built.steps.some(s=>String(s.text||'').indexOf('你嗰日應承過我')>=0); })());
ok('(b) 讀返 Beat 4：有 gu_ask_back → heart 插「你嗰日問我，我自己呢」', (()=>{ resetS(623); _ys = { year:1992, season:'秋' }; setFav('gu_mingfai', 45); metStar('gu_mingfai'); S.flags.gu_ask_back = 1; const st = S.stars.gu_mingfai; for(const b of (ENC79_BEATS.gu_mingfai||[])) st.beatsDone[b.id] = 1; const built = enc79BuildScript('gu_mingfai', false); return !!built && built.steps.some(s=>s.seg==='heart:gu_mingfai') && built.steps.some(s=>String(s.text||'').indexOf('你嗰日問我，我自己呢——我答你唔到，而家我答你：我輸咗')>=0); })());
ok('(b) 讀返 Beat 4：無旗 → heart 照開但唔插句', (()=>{ resetS(624); _ys = { year:1992, season:'秋' }; setFav('gu_mingfai', 45); metStar('gu_mingfai'); const st = S.stars.gu_mingfai; for(const b of (ENC79_BEATS.gu_mingfai||[])) st.beatsDone[b.id] = 1; const built = enc79BuildScript('gu_mingfai', false); return !!built && built.steps.some(s=>s.seg==='heart:gu_mingfai') && !built.steps.some(s=>String(s.text||'').indexOf('你嗰日問我，我自己呢')>=0); })());
ok('(b) 靜態：DRAFT 註釋已更新（唔再寫「遊戲未有呢個抉擇／現時無呼叫點」）', !html.includes('遊戲未有呢個抉擇') && !html.includes('現時無呼叫點') && html.includes('v20a273 1.14 已實裝'));
ok('(b) pushSeg：gu_tease 抉擇 options 帶旗（行 v269 機制 B+）', (()=>{ resetS(625); _ys = { year:1991, season:'春' }; setFav('gu_mingfai', 25); metStar('gu_mingfai'); S.stars.gu_mingfai.beatsDone.gu_foreshadow = 1; const built = enc79BuildScript('gu_mingfai', false); const ch = (built.steps||[]).find(s=>s.choice && s.seg==='beat:gu_tease'); return !!ch && JSON.stringify(ch.options[0].flags)==='["gu_promise_clean"]' && JSON.stringify(ch.options[1].flags)==='["gu_ask_back"]'; })());

/* ---- (c) 六線核實：fx 關鍵字再發現 3 處同類 bug（已修）＋草稿旗盤點 ---- */
ok('(c) fx 駱 first：講好話 +3／點頭 +1／笑佢 -2（live label）', enc79ChoiceFx('first:lok_gasing','出聲為他說句好話：這些歌是好聽的').fav===3 && enc79ChoiceFx('first:lok_gasing','點頭不出聲，等他走過').fav===1 && enc79ChoiceFx('first:lok_gasing','笑他脾氣這麼大，活該他倒霉').fav===-2);
ok('(c) fx 程 first：練到天亮 +3／遞一瓶水 +1／笑佢 -2（live label）', enc79ChoiceFx('first:ching_tinlok','說自己當年怎樣熬：被人笑的時候，我也是練到天亮').fav===3 && enc79ChoiceFx('first:ching_tinlok','靜靜遞一瓶水給他，不出聲').fav===1 && enc79ChoiceFx('first:ching_tinlok','笑他的唱功：你唱那兩句真的不行').fav===-2);
ok('(c) fx 蘇 first：護著 +3／讓開 +1／介紹 -2（live label）', enc79ChoiceFx('first:so_jiyan','護著她進升降機，一句也不多說').fav===3 && enc79ChoiceFx('first:so_jiyan','讓開站到一邊，不阻礙別人工作').fav===1 && enc79ChoiceFx('first:so_jiyan','趁機介紹自己，想攞個機會').fav===-2);
ok('(c) fx 六線 heart 全部對得上 live label（駱聽／魏認真／齊真話／彭聽／鍾出聲／程慢）', enc79ChoiceFx('heart:lok_gasing','靜靜聽他彈完寫好嗰半首').fav===3 && enc79ChoiceFx('heart:lok_gasing','讚他那首歌好聽').fav===1
  && enc79ChoiceFx('heart:ngai_wingnaam','認真記下，回去練習').fav===3 && enc79ChoiceFx('heart:ngai_wingnaam','笑著說怕自己學不來').fav===1
  && enc79ChoiceFx('heart:chai_zanhoi','說真話：戲路要變，不變才危險').fav===3 && enc79ChoiceFx('heart:chai_zanhoi','安慰他：一哥地位哪有這麼容易動搖').fav===1
  && enc79ChoiceFx('heart:pang_siuki','靜靜聽他說完').fav===3 && enc79ChoiceFx('heart:pang_siuki','笑著說他想多了').fav===1
  && enc79ChoiceFx('heart:chung_choning','靜靜聽，不出聲').fav===3 && enc79ChoiceFx('heart:chung_choning','問她會不會回來').fav===1
  && enc79ChoiceFx('heart:ching_tinlok','站在他那邊：慢的那條路才能走得遠').fav===3 && enc79ChoiceFx('heart:ching_tinlok','叫他不要想太多，紅了再說').fav===1);
ok('(c) fx 六線 first 其餘三線不變（魏汽水／齊答得出／彭記性／鍾受教）', enc79ChoiceFx('first:ngai_wingnaam','拿支汽水給他，陪他坐一陣').fav===5 && enc79ChoiceFx('first:chai_zanhoi','一口答得出：左三步，望返城門').fav===3 && enc79ChoiceFx('first:pang_siuki','佩服他的記性：彭生，你的記性真是無人能及').fav===3 && enc79ChoiceFx('first:chung_choning','站正一點，虛心受教：多謝鍾小姐指點').fav===3);
ok('(c) 六線 live 節拍在位（每線 beats＋heart＋ChoiceFx）', ['lok_gasing','ngai_wingnaam','chai_zanhoi','pang_siuki','chung_choning','ching_tinlok'].every(sid=> (ENC79_BEATS[sid]||[]).length>=4 && ENC79_DIALOG[sid] && ENC79_DIALOG[sid].heart && (ENC79_DIALOG[sid].heart.choices||[]).length===2)
  && (ENC79_BEATS.lok_gasing||[]).some(b=>b.id==='lok_help') && (ENC79_BEATS.ngai_wingnaam||[]).some(b=>b.id==='ngai_help') && (ENC79_BEATS.chai_zanhoi||[]).some(b=>b.id==='chai_choice') && (ENC79_BEATS.pang_siuki||[]).some(b=>b.id==='pang_help') && (ENC79_BEATS.chung_choning||[]).some(b=>b.id==='chung_farewell') && (ENC79_BEATS.ching_tinlok||[]).some(b=>b.id==='ching_after_train'));
ok('(c) 草稿旗盤點：六線 PLAN §4–§9 草稿旗 v278 已實裝（66 支全部在 html 出現；chai_silent 另有 flags 欄位）', (()=>{ const F = ['lok_first_stand','lok_first_quiet','lok_first_mock','lok_kept_row','lok_loose_row','lok_tried_harmony','lok_honest_not_ready','lok_stand_original','lok_cover_first','lok_heard_whole','lok_praised_song','lok_calm_truth','lok_join_rant','ngai_first_soda','ngai_first_tissue','ngai_first_walkaway','ngai_meal_treat','ngai_tea','ngai_walk_past','ngai_learn_serious','ngai_learn_later','ngai_rain_stand','ngai_rain_hold_back','ngai_heart_learn','ngai_heart_shy','ngai_patron_vouch','ngai_patron_honest','chai_first_right','chai_first_honest','chai_first_bluff','chai_kept_fear','chai_loose_fear','chai_advise_stop','chai_truth_change','chai_comfort','chai_try_new','chai_play_safe','pang_first_admire','pang_first_polite','pang_first_fake','pang_showed_up','pang_late','pang_cover_night','pang_absent_night','pang_listened','pang_brushed_off','pang_noodle_night','pang_early_night','chung_first_humble','chung_first_silent','chung_first_backtalk','chung_tried_director','chung_stayed_lane','chung_kept_quiet','chung_loose_talk','chung_listened','chung_asked_return','ching_first_grit','ching_first_water','ching_first_blunt','ching_stayed_late','ching_left_early','ching_back_train','ching_back_polish','ching_stand_slow','ching_stand_fast']; return F.every(f=>html.includes(f)) && html.includes('flags: ["chai_silent"]'); })());
ok('(c) 即派範圍：GRANT229_ENC79 六線行 v278 已實裝 57 行（總 17＋57＝74）', (()=>{ const SIX=['駱家聲支線','魏詠男支線','齊鎮海支線','彭少祺支線','鍾楚凝支線','程天諾支線']; return GRANT229_ENC79.length===74 && GRANT229_ENC79.filter(r=>r && SIX.indexOf(r.source)>=0).length===57; })());
ok('(c) 1.18 勘誤 code 側無嘢：gig_rec_02／gig_wf3_liao_stage repo 0 命中', !html.includes('gig_rec_02') && !html.includes('gig_wf3_liao_stage') && !gigById('gig_wf3_liao_stage'));

/* ---- (d) PLAN §10 第一批 25 項核實 ---- */
ok('(d) BR89 映射 19 張：每張新庫存在＋trigger.creditId 同映射一致', (()=>{ const ids = Object.keys(BR89_PATRON_OF_GIG); if(ids.length!==19) return false; return ids.every(id=>{ const g=gigById(id); return g && g.trigger && g.trigger.kind==='credit' && g.trigger.creditId===BR89_PATRON_OF_GIG[id]; }); })());
ok('(d) BR89 映射包齊 §10.1 八筆債權（廖 patron／顧／麥／駱／魏／齊／鍾／廖優先）', ['credit_enc83_liu_patron','credit_enc83_gu_patron','credit_enc83_mak_patron','credit_enc83_lok_patron','credit_enc83_ngai_patron','credit_enc83_chai_patron','credit_enc84_chung_patron','credit_enc79_liu_priority'].every(c=> Object.values(BR89_PATRON_OF_GIG).includes(c)));
ok('(d) G-G1：顧引薦＝gig_1992_rec_205《夜總會登台暖場》唱片中級 1992', (()=>{ const g=gigById('gig_1992_rec_205'); return !!g && g.title.indexOf('夜總會登台暖場')>=0 && g.type==='唱片通告' && g.tier==='中級' && g.year===1992 && g.trigger.creditId==='credit_enc83_gu_patron'; })());
ok('(d) G-G2：還錢結算（result＝1）無債權都開 rec_105；未還／無結果唔開', (()=>{ resetS(700); const g=gigById('gig_1992_rec_205'); if(br89GigOn(g)!==false) return false; S.flags.enc83_gu_loan_result = 1; if(br89GigOn(g)!==true) return false; S.flags.enc83_gu_loan_result = 2; if(br89GigOn(g)!==false) return false; return true; })());
ok('(d) G-G2：持債權本身都開（唔使等還錢）', (()=>{ resetS(701); S.mockCredits.push({ id:'credit_enc83_gu_patron', debtor:'顧明輝', title:'登台引薦', line:'x', status:'未收' }); return br89GigOn(gigById('gig_1992_rec_205'))===true; })());
ok('(d) G-G2：債權已兌現＋未還錢 → 落板（唔重開）', (()=>{ resetS(702); S.mockCredits.push({ id:'credit_enc83_gu_patron', debtor:'顧明輝', title:'登台引薦', line:'x', status:'未收', redeemedBy:'gig_1992_rec_205' }); return br89GigOn(gigById('gig_1992_rec_205'))===false; })());
ok('(d) G-L1：廖 patron＝gig_1992_film_103《吉星笑哈哈》，同優先 gig_1991_film_103 分開兩張', (()=>{ const a=gigById('gig_1992_film_103'), b=gigById('gig_1991_film_103'); return !!a && !!b && a.id!==b.id && a.trigger.creditId==='credit_enc83_liu_patron' && b.trigger.creditId==='credit_enc79_liu_priority'; })());
ok('(d) G-M2／G-LOK-1／G-NGAI-1／G-CHAI-1／G-C1：五張引薦通告 trigger 對位', (()=>{ const m = [['gig_1991_film_211','credit_enc83_mak_patron'],['gig_1992_rec_111','credit_enc83_lok_patron'],['gig_1991_film_212','credit_enc83_ngai_patron'],['gig_1992_film_206','credit_enc83_chai_patron'],['gig_1991_film_213','credit_enc84_chung_patron']]; return m.every(([id,c])=>{ const g=gigById(id); return g && g.trigger && g.trigger.creditId===c; }); })());
ok('(d) G-M1：持武指債權＋武打作品通告 → 免試鏡渠道開；錯類別／無債權／已兌現 → 唔開', (()=>{ resetS(710); const act = GIGS_ARR.find(g=>g && (g.genre==='動作'||g.genre==='武俠') && g.category==='作品'); const nonAct = GIGS_ARR.find(g=>g && g.genre==='喜劇' && g.category==='作品'); if(!act || !nonAct) return false; if(favor158ChannelForGig(act)!==null) return false; S.mockCredits.push({ id:'credit_enc79_mak_wuzhi', debtor:'紅棉武指', title:'武指照應人情', line:'x', status:'未收' }); if(!favor158ChannelForGig(act) || favor158ChannelForGig(act).creditId!=='credit_enc79_mak_wuzhi') return false; if(favor158ChannelForGig(nonAct)!==null) return false; S.mockCredits[0].redeemedBy = act.id; return favor158ChannelForGig(act)===null; })());
ok('(d) G-PANG-1：持慈善債權＋綜藝主持通告 → 免試鏡渠道開；錯類別 → 唔開', (()=>{ resetS(711); const mc = GIGS_ARR.find(g=>g && g.type==='綜藝' && String(g.roleLabel||'').indexOf('主持')>=0); const nonMc = GIGS_ARR.find(g=>g && g.type==='綜藝' && String(g.roleLabel||'').indexOf('主持')<0); if(!mc) return false; if(favor158ChannelForGig(mc)!==null) return false; S.mockCredits.push({ id:'credit_enc84_pang_charity', debtor:'彭少祺', title:'慈善騷頂班人情', line:'x', status:'未收' }); if(!favor158ChannelForGig(mc) || favor158ChannelForGig(mc).creditId!=='credit_enc84_pang_charity') return false; return !nonMc || favor158ChannelForGig(nonMc)===null; })());
ok('(d) G-C2：持忠告旗 → 下一次文藝片試鏡出提示；用一次即清；非文藝唔出', (()=>{ resetS(720); const wenyi = GIGS_ARR.find(g=>g && g.genre==='文藝' && g.type==='電影' && g.category==='作品'); const other = GIGS_ARR.find(g=>g && g.genre==='喜劇' && g.type==='電影' && g.category==='作品'); if(!wenyi || !other) return false; if(chungAdviceTipForAudition229(wenyi)!=='') return false; S.flags.chungAdviceHeld229 = 1; if(chungAdviceTipForAudition229(wenyi)!==CHUNG_ADVICE_TEXT229) return false; if(chungAdviceTipForAudition229(other)!=='') return false; chungAdviceSpend229(); return chungAdviceTipForAudition229(wenyi)===''; })());
ok('(d) G-NGAI-3：餐飯人情第二重兌現＝gig_1992_film_101《武館風波》trigger 對位', (()=>{ const g=gigById('gig_1992_film_101'); return !!g && g.trigger && g.trigger.creditId==='credit_enc83_ngai_meal'; })());
ok('(d) G-L2：trigger 通告 gig_1992_film_202《笑到最後》在位，債權 code 側已授出（v20a279 收割完成授債權＋BR89 map 第 14 對＋結局讀位，共 3 處）', (()=>{ const g=gigById('gig_1992_film_202'); return !!g && g.trigger && g.trigger.creditId==='credit_wf3_comedy_crew' && html.split('credit_wf3_comedy_crew').length-1===3; })());
ok('(d) G-NGAI-2：stub 債 debt_slot_ngai_01 code 側 0 命中（已刪）', !html.includes('debt_slot_ngai_01') && !gigById('debt_slot_ngai_01'));
ok('(d) G-CHAI-3：code 早已係「企邊嗰場風波」，舊詞 0 命中', html.includes('企邊嗰場風波') && !html.includes('站隊嗰場風波'));
ok('(d) G-LOK-2／G-NGAI-4／G-CHAI-2／G-PANG-2：草稿新寫抉擇唔在 live code（無「唱住先」抉擇 label）', !html.includes('label: "勸他唱住先，上咗台') && !html.includes('label: "勸他堅持企硬'));
ok('(d) M-1：GRANT229 晨鏈在位（PresentDue→DueList→DeliverOne）', html.includes('function grant229PresentDue') && html.includes('grant229DueList()') && html.includes('function grant229DeliverOne'));

/* ---- (e) 陸 foreshadow 放寬：遲遇都開，唔再鎖死 luk_kept_secret／heart ---- */
function openBeat(sid, id){ return enc79BeatOpen(sid, beatOf(sid, id)); }
ok('(e) 相容：1990 T0 照開（舊測試口徑不變）', (()=>{ resetS(800); _ys = { year:1990, season:'夏' }; setFav('luk_baakyin', 0); return openBeat('luk_baakyin','luk_foreshadow')===true && enc79PickBeat('luk_baakyin').id==='luk_foreshadow'; })());
ok('(e) 放寬：1991 T2 開（tier 升穿 1 先撞到都播）', (()=>{ resetS(801); _ys = { year:1991, season:'春' }; setFav('luk_baakyin', 30); metStar('luk_baakyin'); return openBeat('luk_baakyin','luk_foreshadow')===true && enc79PickBeat('luk_baakyin').id==='luk_foreshadow'; })());
ok('(e) 放寬：1992 T3 開（殺青回望推高好感嗰條路都唔鎖死）', (()=>{ resetS(802); _ys = { year:1992, season:'秋' }; setFav('luk_baakyin', 45); metStar('luk_baakyin'); return openBeat('luk_baakyin','luk_foreshadow')===true && enc79PickBeat('luk_baakyin').id==='luk_foreshadow'; })());
ok('(e) 放寬：1992 冬 T4 都排 finale 之前（遲遇只推遲收科一次）', (()=>{ resetS(803); _ys = { year:1992, season:'冬' }; setFav('luk_baakyin', 70); metStar('luk_baakyin'); return enc79PickBeat('luk_baakyin').id==='luk_foreshadow'; })());
ok('(e) 守口之後唔再開（luk_kept_secret）', (()=>{ resetS(804); _ys = { year:1991, season:'春' }; setFav('luk_baakyin', 30); S.flags.luk_kept_secret = 1; return openBeat('luk_baakyin','luk_foreshadow')===false; })());
ok('(e) 講兩句之後唔再開（luk_loose_talk）', (()=>{ resetS(805); _ys = { year:1991, season:'春' }; setFav('luk_baakyin', 30); S.flags.luk_loose_talk = 1; return openBeat('luk_baakyin','luk_foreshadow')===false; })());
ok('(e) 播過一次唔再開（beatsDone）', (()=>{ resetS(806); _ys = { year:1991, season:'春' }; setFav('luk_baakyin', 30); S.stars.luk_baakyin.beatsDone.luk_foreshadow = 100; return openBeat('luk_baakyin','luk_foreshadow')===false; })());
ok('(e) heart 閘不變：T3 無守口旗 → heart 唔開；有旗 → 開', (()=>{ resetS(807); _ys = { year:1991, season:'夏' }; setFav('luk_baakyin', 45); metStar('luk_baakyin'); const st = S.stars.luk_baakyin; for(const b of (ENC79_BEATS.luk_baakyin||[])) st.beatsDone[b.id] = 1; const a = enc79BuildScript('luk_baakyin', false); const noHeart = !!a && !a.steps.some(s=>s.seg==='heart:luk_baakyin'); S.flags.luk_kept_secret = 1; const b = enc79BuildScript('luk_baakyin', false); return noHeart && !!b && b.steps.some(s=>s.seg==='heart:luk_baakyin'); })());

console.log(fails.length ? ('\nFAILURES: ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
