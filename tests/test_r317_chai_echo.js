// v20a356 resync：GRANT229 beat:chai_choice key 由「不出聲」改「婉拒畀意見」（齊 choice label 同步改），釘句同步更新。
// v20a317 齊鎮海支線回響通告：gig_1991_tv_114《亂世將軍傳》升格
//   tv_114 加 storyKeys ["chai_zanhoi"]＋credit trigger credit_enc83_chai_patron（齊鎮海），
//   BR89 加第 17 對（同 film_206《油麻地夜班》同一筆債權，陸 film_101＋film_114／駱 rec_111＋rec_112 雙 gig 前例）。
//   1991 秋電視高級開放板通告由 1 張變 0 張（tv_114 轉觸發通告，tv_210 本來已經 fame 閘；D-4／D-11 既定機制，唔係回歸）。
//   GRANT229「停一停」即派唔讀 trigger，持債與否照派（rec_111 N14 即派＋credit trigger 雙路徑前例）。
// 用法：node tests/test_r317_chai_echo.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const root = path.join(__dirname, '..');
let fails = [];
function ok(name, cond, extra){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name + (extra ? ' : ' + extra : '')); }
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

// ---------- 沙盒 ----------
const gigsPack = JSON.parse(fs.readFileSync(path.join(root, 'content/gigs_new.json'), 'utf8'));
const allGigs = gigsPack.gigs;
const gigById = {};
allGigs.forEach(g=>{ if(g && g.id) gigById[g.id] = g; });
const byYear = { 1990: [], 1991: [], 1992: [] };
allGigs.forEach(g=>{ if(g && byYear[Number(g.year)]) byYear[Number(g.year)].push(g); });
var GIGS = allGigs.map(g=>({ id: g.id, title: g.title, trigger: g.trigger }));
var STORY_WIRE = { gigsByYear: { 1990: { gigs: byYear[1990] }, 1991: { gigs: byYear[1991] }, 1992: { gigs: byYear[1992] } } };
var BR89_PATRON_OF_GIG = eval('(' + extractObjLiteral('const BR89_PATRON_OF_GIG = {') + ')');
var BR89_GIGS = [];
var CREDIT_REDEEM_GIG283 = eval('(' + extractObjLiteral('const CREDIT_REDEEM_GIG283 = {') + ')');
var CREDIT_REDEEM_TEXT283 = eval('(' + extractObjLiteral('const CREDIT_REDEEM_TEXT283 = {') + ')');
var GIG_SEASON_SPAN88 = eval('(' + extractObjLiteral('const GIG_SEASON_SPAN88 = {') + ')');
var GIG_SEASON_LEAD88 = Number((html.match(/const GIG_SEASON_LEAD88\s*=\s*(\d+)/) || [])[1] || 60);
var GRANT229_ENC79 = eval(extractConst('GRANT229_ENC79').replace(/^const GRANT229_ENC79\s*=\s*/, '').replace(/;\s*$/, ''));
var S = { mockCredits: [] };
let _ys317 = { year: 1991, season: '秋' };
let _date317 = new Date(1991, 8, 15);
function journalText(s){ return String(s == null ? '' : s); }
function syncNotebookMirror(){}
function saveQ(){}
function refreshMoneyHud(){}
function toast(){}
function ensureMockJournal(){ if(!Array.isArray(S.mockRumors)) S.mockRumors = []; if(!Array.isArray(S.mockDebts)) S.mockDebts = []; }
function yearSeasonNow(){ return _ys317; }
function dateObj(){ return _date317; }
function enc79Rand(){ return 0.1; }
function ensureFavorLedger(){ if(!S.favorLedger) S.favorLedger = { settled: 0, credits: 0, exodus: [], counted: {} }; return S.favorLedger; }
function favorLedgerNoteCredit(id){ const L = ensureFavorLedger(); if(L.counted[id]) return false; L.counted[id] = { kind: 'credit' }; L.credits++; return true; }
function ensureFavorDueSettled(){ if(!S.favorDueSettled) S.favorDueSettled = {}; return S.favorDueSettled; }
const BehaviorGate = { featureFlag_softBehaviorGatePreview: ()=>false };
eval(extractFn('gigRecordById283'));
eval(extractFn('gigTitleById283'));
eval(extractFn('genericCreditOnGigComplete283'));
eval(extractFn('creditRedeemLine283'));
eval(extractFn('favorCreditCountsAsHeld'));
eval(extractFn('br89GigOn'));
eval(extractFn('br89HasCredit'));
eval(extractFn('br89OnGigComplete'));
eval(extractFn('gigSeasonEarlyVisible88'));
eval(extractFn('triggerGigOn'));
eval(extractFn('grant229Ensure'));
eval(extractFn('grant229GigById'));
eval(extractFn('grant229Record'));
eval(extractFn('grant229RecordFromEnc79'));
function resetS317(){
  S = { dayIndex: 0, fame: 0, money: 500, flags: {}, npcs: {}, mockCredits: [], mockDebts: [], mockRumors: [], favorDueSettled: {}, grant229Queue: [], contracts229: [] };
}
const CHAI_CREDIT = { id: 'credit_enc83_chai_patron', debtor: '齊鎮海', title: '一哥引薦', line: '齊鎮海同監製打咗聲招呼：你去試鏡嗰日，提一哥個名，嗰道門會為你開。', status: '未收' };

// ---------- (0) 靜態結構 ----------
const tv114 = gigById['gig_1991_tv_114'];
const film206 = gigById['gig_1992_film_206'];
const tv210 = gigById['gig_1991_tv_210'];
ok('(0) gig_count_330', allGigs.length === 330 && new Set(allGigs.map(g=>g.id)).size === 330, 'n=' + allGigs.length);
ok('(0) trig_38_credit_27', allGigs.filter(g=>g.trigger && g.trigger.kind).length === 38 && allGigs.filter(g=>g.trigger && g.trigger.kind === 'credit').length === 27, 'credit 27（BR89 19＋通用 8）');
ok('(0) tv114_tag_trigger', !!tv114 && JSON.stringify(tv114.storyKeys) === '["chai_zanhoi"]' && tv114.trigger && tv114.trigger.kind === 'credit' && tv114.trigger.creditId === 'credit_enc83_chai_patron' && tv114.trigger.creditOwner === '齊鎮海', 'storyKeys＋trigger 齊');
ok('(0) tv114_other_fields_unchanged', !!tv114 && tv114.title === '《亂世將軍傳》男主角' && tv114.tier === '高級' && tv114.type === '電視劇' && tv114.year === 1991 && tv114.season === '秋' && tv114.days === 30 && JSON.stringify(tv114.pay) === '[8400,10080]' && tv114.genre === '歷史傳記' && tv114.roleLabel === '男主角' && tv114.cast && tv114.cast.leadM === null && tv114.cast.leadF === 'chung_choning' && tv114.cast.supportM === 'chai_zanhoi' && tv114.cast.supportF === 'kong_siying', 'title／tier／year／season／days／pay／genre／cast 唔郁');
ok('(0) chai_patron_grants_match', html.indexOf('{ id:"credit_enc83_chai_patron", debtor:"齊鎮海", title:"一哥引薦"') >= 0, 'chai_patron 授出同一筆債權（id＋debtor＋title 一致）');
ok('(0) chai_patron_gates_v318', html.indexOf('{ id:"chai_patron", when(st){ return enc79TierOf(st.fav)>=4 && !!(S.flags||{}).chai_truth_change && !(S.flags||{}).chai_silent && !(S.flags||{}).chai_comfort && !(S.flags||{}).chai_loose_fear; }') >= 0 && html.indexOf('{ id:"chai_patron_cold", when(st){ return enc79TierOf(st.fav)>=4 && ((S.flags||{}).chai_silent || (S.flags||{}).chai_comfort || (S.flags||{}).chai_loose_fear); }') >= 0, '暖版閘 v20a318：T4＋truth_change＋三排除；冷版閘一行都唔郁');
ok('(0) film206_unchanged', !!film206 && JSON.stringify(film206.storyKeys) === '["chai_zanhoi"]' && film206.trigger && film206.trigger.creditId === 'credit_enc83_chai_patron' && film206.tier === '中級', 'film_206 係 chai tag＋trigger，唔郁');
const EXPECT19 = {
  gig_1991_film_101:'credit_enc83_luk_patron', gig_1991_variety_203:'credit_enc84_pang_patron',
  gig_1992_rec_106:'credit_enc84_ching_patron', gig_1991_film_103:'credit_enc79_liu_priority',
  gig_1992_film_103:'credit_enc83_liu_patron', gig_1991_film_211:'credit_enc83_mak_patron',
  gig_1992_tv_105:'credit_enc83_yip_patron', gig_1992_rec_205:'credit_enc83_gu_patron',
  gig_1991_ad_102:'credit_enc84_so_patron', gig_1991_film_213:'credit_enc84_chung_patron',
  gig_1992_rec_111:'credit_enc83_lok_patron', gig_1991_film_212:'credit_enc83_ngai_patron',
  gig_1992_film_206:'credit_enc83_chai_patron', gig_1992_film_202:'credit_wf3_comedy_crew',
  gig_1992_film_114:'credit_enc83_luk_patron', gig_1992_rec_112:'credit_enc83_lok_patron',
  gig_1991_tv_114:'credit_enc83_chai_patron', gig_1992_variety_106:'credit_enc84_pang_patron',
  gig_1992_film_207:'credit_enc83_ngai_patron'
};
ok('(0) br89_map_19_pairs', Object.keys(BR89_PATRON_OF_GIG).length === 19 &&
  Object.keys(EXPECT19).every(k=>BR89_PATRON_OF_GIG[k] === EXPECT19[k]) &&
  Object.keys(BR89_PATRON_OF_GIG).every(k=>EXPECT19[k] === BR89_PATRON_OF_GIG[k]), 'n=' + Object.keys(BR89_PATRON_OF_GIG).length);
ok('(0) board_1991_autumn_tv_senior_0_open', allGigs.filter(g=>g.type === '電視劇' && g.tier === '高級' && g.year === 1991 && g.season === '秋' && !g.trigger).length === 0 && !!tv210 && tv210.trigger && tv210.trigger.kind === 'fame' && tv210.trigger.fameMin === 40, 'tv_114 轉 trigger 閘，tv_210 本來已經 fame 閘（D-4／D-11 既定機制）');

// ---------- (1) 未持有債權：唔上板 ----------
resetS317();
ok('(1) no_credit_not_on', triggerGigOn(tv114) === false && br89GigOn({ id: 'gig_1991_tv_114' }) === false, 'D-4 觸發前隱藏');
resetS317();
S.mockCredits = [{ id: 'credit_enc83_lok_patron', debtor: '駱家聲', title: '監製引薦', line: 'x', status: '未收' }];
ok('(1) other_credit_not_on', triggerGigOn(tv114) === false, '持有駱引薦都唔開齊嗰張');

// ---------- (2) 持有債權：經通用 trigger 系統上板 ----------
resetS317();
S.mockCredits = [Object.assign({}, CHAI_CREDIT)];
ok('(2) held_on_via_trigger', triggerGigOn(tv114) === true && br89GigOn({ id: 'gig_1991_tv_114' }) === true && triggerGigOn(film206) === true, '持債權：兩張都開');
_date317 = new Date(1991, 6, 1);
ok('(2) window_not_yet', gigSeasonEarlyVisible88(tv114) === false, '1991-07-01 未入窗');
_date317 = new Date(1991, 8, 15);
ok('(2) window_open', gigSeasonEarlyVisible88(tv114) === true, '1991-09-15 可見（1991 秋，span [9,11]＋提早 60 日）');

// ---------- (3) 雙 gig 同一筆債權：殺青邊張，另一張自動落板 ----------
resetS317();
S.mockCredits = [Object.assign({}, CHAI_CREDIT)];
br89OnGigComplete('gig_1992_film_206');
ok('(3) redeem_206_closes_114', S.mockCredits[0].redeemedBy === 'gig_1992_film_206' && br89GigOn({ id: 'gig_1991_tv_114' }) === false && br89GigOn({ id: 'gig_1992_film_206' }) === false && triggerGigOn(tv114) === false, '殺青《油麻地夜班》：新張自動落板');
resetS317();
S.mockCredits = [Object.assign({}, CHAI_CREDIT)];
br89OnGigComplete('gig_1991_tv_114');
ok('(3) redeem_114_closes_206', S.mockCredits[0].redeemedBy === 'gig_1991_tv_114' && br89GigOn({ id: 'gig_1992_film_206' }) === false && triggerGigOn(film206) === false, '殺青《亂世將軍傳》：舊張自動落板');
resetS317();
S.mockCredits = [Object.assign({}, CHAI_CREDIT)];
const chaiLine = creditRedeemLine283({ id: 'credit_enc83_chai_patron' });
ok('(3) H_shows_both_titles', chaiLine.indexOf('可以換：') >= 0 && chaiLine.indexOf('油麻地夜班') >= 0 && chaiLine.indexOf('亂世將軍傳') >= 0, '人情卡「可以換」出齊兩張名（BR89 反查自動）');

// ---------- (4) GRANT229「停一停」即派：唔使持債照派 ----------
resetS317();
ok('(4) grant229_stop_no_credit', grant229RecordFromEnc79('beat:chai_choice', '停一停') === true && S.grant229Queue.length === 1 && S.grant229Queue[0].gigId === 'gig_1991_tv_114', 'GRANT229 唔讀 trigger，唔持債照派 tv_114');
resetS317();
ok('(4) grant229_silent_other_gig', grant229RecordFromEnc79('beat:chai_choice', '婉拒畀意見') === true && S.grant229Queue.length === 1 && S.grant229Queue[0].gigId === 'gig_1991_tv_207', '「婉拒畀意見」嗰邊照派 tv_207');

// ---------- (5) 舊檔唔 crash ----------
resetS317();
S.mockCredits = [];
let threw317 = false;
try{ triggerGigOn(tv114); br89GigOn({ id: 'gig_1991_tv_114' }); }catch(e){ threw317 = true; }
ok('(5) old_save_no_credit_no_throw', !threw317 && triggerGigOn(tv114) === false, '無債權舊檔唔掟錯');
resetS317();
delete S.mockCredits;
threw317 = false;
try{ triggerGigOn(tv114); br89GigOn({ id: 'gig_1991_tv_114' }); }catch(e){ threw317 = true; }
ok('(5) old_save_no_mockCredits_no_throw', !threw317 && triggerGigOn(tv114) === false, '無 mockCredits 舊檔唔掟錯');
resetS317();
S.mockCredits = [Object.assign({}, CHAI_CREDIT, { status: '絕響' })];
ok('(5) expired_credit_not_on', triggerGigOn(tv114) === false, '絕響債權唔開');

console.log(fails.length === 0 ? 'ALL PASS' : 'FAILURES: ' + fails.join(', '));
process.exit(fails.length === 0 ? 0 : 1);
