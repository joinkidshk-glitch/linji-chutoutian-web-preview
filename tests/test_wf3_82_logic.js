// v20a82 WF3 邏輯測試：報紙事件系統＋鏈 A/B/C/D 餘波＋好感階梯補渠道
// 用法：node tests/test_wf3_82_logic.js [path-to-index.html]
// 反證：喺 v20a81 index 行應該 FAIL（冇 NEWS82_EVENTS／WF3 模組）。
const fs = require('fs');
const path = process.argv[2] || require('path').join(__dirname, '..', 'index.html');
const html = fs.readFileSync(path, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) throw new Error('fn not found: '+name);
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){
    if(html[j]==='{') depth++;
    else if(html[j]==='}'){ depth--; if(depth===0) break; }
  }
  return html.slice(i, j+1);
}
function extractConst(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) throw new Error('const not found: '+name);
  let j = i;
  while(j<html.length && html[j]!=='{' && html[j]!=='[') j++;
  const openCh = html[j], closeCh = openCh==='{' ? '}' : ']';
  let depth=0, started=false;
  for(; j<html.length; j++){
    if(html[j]===openCh){ depth++; started=true; }
    else if(html[j]===closeCh){ depth--; if(started && depth===0) break; }
  }
  return html.slice(i, j+1)+';';
}

// ---------- stubs ----------
var saveQ = ()=>{};
var syncNotebookMirror = ()=>{};
var ensureMockJournal = ()=>{};
var toast = ()=>{};
var modal = ()=>{};
var syncDualTracks = ()=>{};
var _clips = [];
var ensureNewspaperClippings = ()=> _clips;
var _enqueued = [];
var enqueueNewspaperItem = (item)=>{ _enqueued.push(item); return item; };
var _intel = {};
var hasIntelFlag = (f)=> !!_intel[f];
var ensureFavorLedger = ()=> ({ settled:0, credits:0, exodus:[], counted:{} });
var favorLedgerNoteCredit = ()=>{};
var favorLedgerNoteSettled = ()=>{};
var _storyDone = {}, _storyFlags = {};
var StoryOC = {
  ensure(){},
  isDone(id){ return !!_storyDone[id]; },
  getFlag(f){ return !!_storyFlags[f]; },
  setFlag(f, v){ _storyFlags[f] = v; }
};
var S = null;
function freshS(day){
  return { dayIndex: day||0, fame:0, money:1000, industryCredit:10,
    mockRumors:[], mockCredits:[], mockDebts:[], wrapHistory:[], flags:{}, story:{ done:{}, flags:{} } };
}

// ---------- 1. 情報使用點（鏈 B gigLine 補返＋鏈 D 新使用點） ----------
eval(extractConst('INTEL_USE_POINTS').replace('const INTEL_USE_POINTS', 'globalThis.INTEL_USE_POINTS'));
const UP = globalThis.INTEL_USE_POINTS;
ok('鏈 B gigLine 非空（原為空字串）', typeof UP.rumor_liao_bingxing_money.gigLine==='string' && UP.rumor_liao_bingxing_money.gigLine.length>=20);
ok('鏈 B gigLine 講到水喉／金主', /水喉|金主/.test(UP.rumor_liao_bingxing_money.gigLine));
ok('鏈 D 葉敏芝使用點存在且非空', !!UP.rumor_yip_rumor_truth && UP.rumor_yip_rumor_truth.gigLine.length>=20);
ok('鏈 D 顧明輝使用點存在且非空', !!UP.rumor_ku_overwork_truth && UP.rumor_ku_overwork_truth.gigLine.length>=20);

// ---------- 2. 新拼合對＋情報旗 ----------
eval(extractConst('MERGE_PAIRS').replace('const MERGE_PAIRS', 'globalThis.MERGE_PAIRS'));
eval(extractConst('INTEL_FLAGS').replace('const INTEL_FLAGS', 'globalThis.INTEL_FLAGS'));
const PAIRS = globalThis.MERGE_PAIRS, FLAGS = globalThis.INTEL_FLAGS;
const pair = (a,b)=> PAIRS.find(p=> (p.a===a && p.b===b) || (p.a===b && p.b===a));
ok('yip 經典對（聽聞×聽聞）', (()=>{ const p = pair('rumor_yip_plasticsurgery_summer','rumor_yip_writeup_heard'); return !!p && p.merged==='rumor_yip_rumor_truth'; })());
ok('yip 跨系統對（報紙×聽聞）', (()=>{ const p = pair('paperfrag_yip_swimsuit','rumor_yip_plasticsurgery_summer'); return !!p && p.merged==='rumor_yip_rumor_truth'; })());
ok('ku 跨系統對（報紙×聽聞）', (()=>{ const p = pair('paperfrag_ku_wrap','rumor_ku_overwork_summer'); return !!p && p.merged==='rumor_ku_overwork_truth'; })());
ok('intel flags: yip', FLAGS.rumor_yip_rumor_truth==='intel_yip_truth');
ok('intel flags: ku', FLAGS.rumor_ku_overwork_truth==='intel_ku_overwork');

// ---------- 3. 報紙事件表：日期／級別／結構 ----------
eval(extractConst('NEWS82_EVENTS').replace('const NEWS82_EVENTS', 'globalThis.NEWS82_EVENTS'));
eval(extractFn('news82EventById'));
eval(extractFn('news82IsHead'));
eval(extractFn('news82DateLabel'));
const EV = globalThis.NEWS82_EVENTS;
ok('七則事件（6 則＋E6 第二年版）', EV.length===7);
ok('事件 id 唯一', new Set(EV.map(e=>e.id)).size===7);
const expectDays = { E6a:385, E5:532, E2:658, E1:744, E6b:750, E4:1015, E3:1092 };
ok('刊出日準確', EV.every(e=> expectDays[e.id]===e.day));
const dateOf = (d)=>{ const x = new Date(1990,0,1+d); return [x.getFullYear(), x.getMonth()+1, x.getDate()]; };
ok('E6a = 1991-01-21', JSON.stringify(dateOf(385))==='[1991,1,21]');
ok('E5 = 1991-06-17', JSON.stringify(dateOf(532))==='[1991,6,17]');
ok('E2 = 1991-10-21', JSON.stringify(dateOf(658))==='[1991,10,21]');
ok('E1 = 1992-01-15', JSON.stringify(dateOf(744))==='[1992,1,15]');
ok('E6b = 1992-01-21', JSON.stringify(dateOf(750))==='[1992,1,21]');
ok('E4 = 1992-10-12', JSON.stringify(dateOf(1015))==='[1992,10,12]');
ok('E3 = 1992-12-28', JSON.stringify(dateOf(1092))==='[1992,12,28]');
ok('頭版三則 = E1/E2/E3', ['E1','E2','E3'].every(id=>news82IsHead(id)) && ['E6a','E5','E6b','E4'].every(id=>!news82IsHead(id)));
ok('每則三段正文＋標題，冇餘波傳聞（G1 已刪 echo：有 echoDelay 欄、冇 echo 欄）', EV.every(e=> Array.isArray(e.paras) && e.paras.length===3 && e.headline && e.echoDelay===3 && !e.echo && !e.rumorEcho));
ok('每則有配圖鍵', EV.every(e=> !!e.imgKey));
ok('E4 沿用 E6 圖（版式重用）', news82EventById('E6b').imgKey==='E6' && news82EventById('E6a').imgKey==='E6');
ok('日期標籤格式', news82DateLabel(news82EventById('E1'))==='1992 年 1 月 15 日');

// ---------- 4. news82Tick：準時刊出／唔重複／餘波 ----------
eval(extractFn('ensureNews82'));
eval(extractFn('news82Tick'));
eval(extractFn('news82PublishedDay'));
_clips = []; _enqueued = [];
S = freshS(657);
news82Tick();
ok('E2 前一日唔刊', _enqueued.length===0 && !S.news82.pub.E2);
S.dayIndex = 658;
news82Tick();
ok('E2 準時刊出（day 658）', _enqueued.length===1 && _enqueued[0].worldId==='E2' && _enqueued[0].source==='world' && S.news82.pub.E2===658);
news82Tick();
ok('E2 唔重複刊', _enqueued.length===1);
S.dayIndex = 660;
news82Tick();
ok('餘波未到（刊後 2 日）', !S.mockRumors.some(r=>r.id==='echo_news_e2'));
S.dayIndex = 661;
news82Tick();
ok('餘波刊後 3 日唔入傳聞（G1 已刪 echo）', !S.mockRumors.some(r=>r.id==='echo_news_e2'));
news82Tick();
ok('餘波唔重複（冇 echo 可重複：重複 tick 亦唔入傳聞）', S.mockRumors.filter(r=>r.id==='echo_news_e2').length===0);

// ---------- 5. 舊檔規則：過期 7 日以上歸檔、7 日內照常刊 ----------
_clips = []; _enqueued = [];
S = freshS(800);
ensureNews82();
ok('舊檔 day800：E6a/E5/E2/E1/E6b 已歸檔', ['E6a','E5','E2','E1','E6b'].every(id=> S.news82.arc[id]===1));
ok('舊檔 day800：E4/E3 未歸檔（未來）', !S.news82.arc.E4 && !S.news82.arc.E3);
ok('舊報留底入剪報（帶圖＋段落＋標籤）', (()=>{ const c = _clips.find(x=>x.worldId==='E1'); return !!c && c.clipLabel==='舊報留底' && c.imgKey==='E1' && Array.isArray(c.paras) && c.paras.length===3; })());
news82Tick();
ok('已歸檔唔再彈刊', _enqueued.length===0);
_clips = []; _enqueued = [];
S = freshS(746);
ensureNews82();
ok('舊檔 day746：E1（2 日前）唔歸檔', !S.news82.arc.E1);
news82Tick();
ok('舊檔 day746：E1 照常入隊刊出', _enqueued.some(e=>e.worldId==='E1'));

// ---------- 6. N8 追加抉擇 ----------
eval(extractFn('wf3PrepareNode82'));
_intel = { intel_yip_truth: true };
const c11 = { id:'N8', choices:[{ id:'N8_a' }, { id:'N8_b' }] };
const prep = wf3PrepareNode82(c11);
ok('持有真相 → 追加 N8_d', !!prep && prep.choices.length===3 && prep.choices[2].id==='N8_d');
ok('N8_d 落旗 flag_yip_warned82', !!prep && prep.choices[2].effects.flags.indexOf('flag_yip_warned82')>=0);
ok('原節點冇被改（淺拷貝）', c11.choices.length===2);
_intel = {};
ok('冇真相 → 唔追加', wf3PrepareNode82(c11)===null);
_intel = { intel_yip_truth: true };
ok('其他節點唔受影響', wf3PrepareNode82({ id:'N11', choices:[] })===null);
ok('已追加過唔重複', wf3PrepareNode82(prep)===null);

// ---------- 7. mergeWf3Gigs：B3 中期——WF3_LIAO_GIG／WF3_LIAO_HARVEST_GIG 已係 null，
// mergeWf3Gigs 係 stub（回 0），有冇情報都唔注入、唔出舊 id、唔 crash（B5 觸發系統補返先恢復）。 ----------
var GIGS = [];
var normalizeGigRecord = (g)=> Object.assign({}, g);
eval(extractConst('WF3_LIAO_GIG').replace('const WF3_LIAO_GIG', 'globalThis.WF3_LIAO_GIG'));
eval(extractConst('WF3_LIAO_HARVEST_GIG').replace('const WF3_LIAO_HARVEST_GIG', 'globalThis.WF3_LIAO_HARVEST_GIG'));
eval(extractFn('mergeWf3Gigs'));
ok('B3 WF3_LIAO_GIG／WF3_LIAO_HARVEST_GIG 已係 null', globalThis.WF3_LIAO_GIG===null && globalThis.WF3_LIAO_HARVEST_GIG===null);
S = freshS(100);
_intel = {};
ok('B3 冇情報 → merge 回 0，隱藏通告唔出現', mergeWf3Gigs()===0 && !GIGS.some(g=>/^gig_wf3_/.test(g.id)));
_intel = { intel_liao_money: true };
ok('B3 有情報 → merge 照舊回 0，唔注入（池已清空，B5 補返）', mergeWf3Gigs()===0 && GIGS.length===0 && !GIGS.some(g=>/^gig_wf3_/.test(g.id)));
S.flags['done_gig_1990_film_101'] = 1;
mergeWf3Gigs();
ok('B3 完成旗亦唔會令舊通告上板', !GIGS.some(g=>/^gig_wf3_/.test(g.id)));

// ---------- 8. wf3SettleTick：B3 中期——鏈 A／鏈 B 結算塊已隨舊通告一併刪
// （E20），殺青任何工都唔再觸發嗰兩路結算；收割窗／收割完成路徑同樣休眠；
// 收割過期、鏈 D、方小龍路徑唔掂通告，照舊行。 ----------
eval(extractFn('ensureWf3'));
eval(extractFn('wf3GrantCredit'));
eval(extractFn('wf3GrantRumor'));
eval(extractFn('wf3SettleTick'));
// 鏈 A（已刪）：殺青任何工都唔再結算
_clips = []; _enqueued = [];
S = freshS(200);
S.wrapHistory = [{ gigId:'gig_1990_film_101', wrappedDay:199 }];
wf3SettleTick();
ok('B3 鏈 A 休眠：殺青唔再派天王團隊債權', !S.mockCredits.some(c=>c.id==='credit_wf3_lu_team'));
ok('B3 鏈 A 休眠：唔再有報紙角度入隊', !_enqueued.some(e=>e.eventKey==='wf3:lu_paper'));
ok('B3 鏈 A 休眠：唔再有傳聞伏筆', !S.mockRumors.some(r=>r.id==='rumor_wf3_lu_pa_favor'));
wf3SettleTick();
ok('B3 鏈 A 休眠：重複 tick 照舊乜都冇', S.mockCredits.filter(c=>c.id==='credit_wf3_lu_team').length===0);
// 鏈 B 穩陣（已刪）
_enqueued = [];
S = freshS(300);
S.wf3 = { liaoChoice:'steady' };
S.wrapHistory = [{ gigId:'gig_1990_film_101', wrappedDay:299 }];
const credBefore = S.industryCredit;
wf3SettleTick();
ok('B3 鏈 B 穩陣休眠：信用唔再 +2', S.industryCredit===credBefore);
ok('B3 鏈 B 穩陣休眠：唔再有報紙好評角度', !_enqueued.some(e=>e.eventKey==='wf3:liao_steady'));
// 鏈 B 搶鏡＋記仇＋收割（已刪）
_enqueued = [];
S = freshS(300);
S.wf3 = { liaoChoice:'steal' };
S.wrapHistory = [{ gigId:'gig_1990_film_101', wrappedDay:299 }];
const moneyBefore = S.money;
wf3SettleTick();
ok('B3 鏈 B 搶鏡休眠：唔再有額外片酬', S.money===moneyBefore);
ok('B3 鏈 B 搶鏡休眠：唔再記仇債', !S.mockDebts.some(x=>x.id==='debt_wf3_liao_grudge') && !S.wf3.grudgeDue);
ok('B3 鏈 B 搶鏡休眠：唔再有報紙內訌角度', !_enqueued.some(e=>e.eventKey==='wf3:liao_steal'));
S.dayIndex = 313;
wf3SettleTick();
ok('收割窗未到期唔開', !S.wf3.liaoHarvest);
S.dayIndex = 314;
wf3SettleTick();
ok('B3 記仇債到期 → 收割窗唔開（收割路徑已刪）', !S.wf3.liaoHarvest);
// 收割完成（已刪）：就算債＋窗齊晒，殺青任何工都唔清債／唔派喜劇組債權
S = freshS(316);
S.wf3 = { liaoChoice:'steal', liaoSettled:1, grudgeDue:314, liaoHarvest:{ gigDay:314, window:7 } };
S.mockDebts = [{ id:'debt_wf3_liao_grudge' }];
S.wrapHistory = [{ gigId:'gig_1990_film_101', wrappedDay:316 }];
wf3SettleTick();
ok('B3 收割休眠：殺青唔清記仇債、唔派喜劇組債權', S.mockDebts.some(d=>d.id==='debt_wf3_liao_grudge') && !S.mockCredits.some(c=>c.id==='credit_wf3_comedy_crew'));
ok('B3 收割休眠：唔再有情報渠道傳聞', !S.mockRumors.some(r=>r.id==='rumor_wf3_comedy_crew'));
// 收割過期
S = freshS(300);
S.wf3 = { liaoChoice:'steal', liaoSettled:1, grudgeDue:290, liaoHarvest:{ gigDay:290, window:7 } };
S.mockDebts = [{ id:'debt_wf3_liao_grudge' }];
const cred2 = S.industryCredit;
S.dayIndex = 298;
wf3SettleTick();
ok('收割過期：債銷＋信用 −2', !S.mockDebts.some(d=>d.id==='debt_wf3_liao_grudge') && S.industryCredit===cred2-2 && S.wf3.liaoHarvestExpired===1);
// 鏈 D：提點債權＋爆料回音
_enqueued = [];
S = freshS(400);
_storyFlags = { flag_yip_warned82: true };
wf3SettleTick();
ok('鏈 D：提點 → 經理人債權', S.mockCredits.some(c=>c.id==='credit_wf3_yip_manager'));
_storyFlags = { flag_miss_leak: true };
_storyDone = { N8: true };
_intel = { intel_yip_truth: true };
wf3SettleTick();
ok('鏈 D：爆料＋知真相 → 回音報紙', _enqueued.some(e=>e.eventKey==='wf3:yip_echo'));
// 方小龍情報卡
S = freshS(500);
_storyDone = { A_fong_push1: true };
_storyFlags = {};
_intel = {};
wf3SettleTick();
ok('方小龍中階卡（A_fong_push1）', S.mockRumors.some(r=>r.id==='rumor_wf3_fong_mid'));
_storyDone = { A_fong_crisis: true };
wf3SettleTick();
ok('方小龍高階卡（A_fong_crisis）', S.mockRumors.some(r=>r.id==='rumor_wf3_fong_high'));

// ---------- 9. WF3_TALK 可用性 ----------
eval(extractConst('WF3_TALK_NODES').replace('const WF3_TALK_NODES', 'globalThis.WF3_TALK_NODES'));
eval(extractConst('WF3_TALK_DEFS').replace('const WF3_TALK_DEFS', 'globalThis.WF3_TALK_DEFS'));
eval(extractFn('news82PublishedDay'));
eval(extractFn('wf3M27WindowOpen'));
eval(extractFn('wf3FongTalkAvail'));
eval(extractFn('wf3TalkDone'));
eval(extractFn('wf3TalkAvailable'));
eval(extractFn('wf3TalkActionsAt'));
S = freshS(100);
_intel = {};
ok('何生鏈 B 對白：冇情報唔出', wf3TalkActionsAt('agency_ho').length===0);
_intel = { intel_liao_money: true };
ok('何生鏈 B 對白：有情報先出', wf3TalkActionsAt('agency_ho').some(a=>a.id==='W3_ho_liao'));
S.news82 = { pub:{ E1: 740 }, arc:{}, echoDone:{} };
S.dayIndex = 750;
ok('M27 餘波對白：刊後 28 日內出（何生＋廖）', wf3TalkActionsAt('agency_ho').some(a=>a.id==='W3_ho_m27') && wf3TalkActionsAt('film_cotton').some(a=>a.id==='W3_liao_m27'));
S.dayIndex = 800;
ok('M27 餘波對白：過窗唔出', !wf3TalkActionsAt('agency_ho').some(a=>a.id==='W3_ho_m27'));
S = freshS(500);
S.wf3 = { luSettled: 1 };
ok('鏈 A 場務對白：結算後喺星河出', wf3TalkActionsAt('tvb_longmen').some(a=>a.id==='W3_lu_pa'));
_storyDone = { N12: true };
_storyFlags = { flag_stunt_double: true };
ok('方小龍傾談：跳咗版', wf3TalkActionsAt('film_harbour').some(a=>a.id==='W3_fong_jump') && !wf3TalkActionsAt('film_harbour').some(a=>a.id==='W3_fong_hold'));
_storyFlags = {};
ok('方小龍傾談：冇跳版', wf3TalkActionsAt('film_harbour').some(a=>a.id==='W3_fong_hold'));

// ---------- 10. 好感階梯補渠道 ----------
eval(extractConst('NPC_TIER_LINES').replace('const NPC_TIER_LINES', 'globalThis.NPC_TIER_LINES'));
const TL = globalThis.NPC_TIER_LINES;
['colleague','rival','director'].forEach(id=>{
  ok('階梯渠道 '+id+'：日常 4＋內幕 4', !!TL[id] && TL[id].daily.length===4 && TL[id].insider.length===4);
});
ok('方小龍唔用句池（線進度交付）', !TL.fong && !TL.fong_siulung);

console.log(fails.length ? ('\nFAILED: '+fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
