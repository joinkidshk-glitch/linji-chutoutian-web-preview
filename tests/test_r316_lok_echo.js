// v20a316 駱家聲支線回響通告：gig_1992_rec_112《追風少年》升格
//   rec_112 加 storyKeys ["lok_gasing"]＋credit trigger credit_enc83_lok_patron（駱家聲），
//   BR89 加第 16 對（同 rec_111《銅鑼灣》同一筆債權，陸 film_101＋film_114 雙 gig 前例）。
//   1992 春唱片中級板通告由 6 張變 5 張（rec_112 轉觸發通告，D-4／D-11 既定機制，唔係回歸）。
// 用法：node tests/test_r316_lok_echo.js [path-to-index.html]
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
const asVar = (code, name)=> code.replace('const ' + name + ' =', 'var ' + name + ' =');

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
var S = { mockCredits: [] };
let _ys316 = { year: 1992, season: '春' };
let _date316 = new Date(1992, 2, 15);
function journalText(s){ return String(s == null ? '' : s); }
function syncNotebookMirror(){}
function saveQ(){}
function refreshMoneyHud(){}
function toast(){}
function ensureMockJournal(){ if(!Array.isArray(S.mockRumors)) S.mockRumors = []; if(!Array.isArray(S.mockDebts)) S.mockDebts = []; }
function yearSeasonNow(){ return _ys316; }
function dateObj(){ return _date316; }
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
function resetS316(){
  S = { dayIndex: 0, fame: 0, money: 500, flags: {}, npcs: {}, mockCredits: [], mockDebts: [], mockRumors: [], favorDueSettled: {} };
}
const LOK_CREDIT = { id: 'credit_enc83_lok_patron', debtor: '駱家聲', title: '監製引薦', line: '駱家聲塞咗張唱片監製嘅卡片畀你。', status: '未收' };

// ---------- (0) 靜態結構 ----------
const rec112 = gigById['gig_1992_rec_112'];
const rec111 = gigById['gig_1992_rec_111'];
const rec102 = gigById['gig_1992_rec_102'];
ok('(0) gig_count_323', allGigs.length === 323 && new Set(allGigs.map(g=>g.id)).size === 323, 'n=' + allGigs.length);
ok('(0) trig_38_credit_27', allGigs.filter(g=>g.trigger && g.trigger.kind).length === 38 && allGigs.filter(g=>g.trigger && g.trigger.kind === 'credit').length === 27, 'credit 27（BR89 19＋通用 8）');
ok('(0) rec112_tag_trigger', !!rec112 && JSON.stringify(rec112.storyKeys) === '["lok_gasing"]' && rec112.trigger && rec112.trigger.kind === 'credit' && rec112.trigger.creditId === 'credit_enc83_lok_patron' && rec112.trigger.creditOwner === '駱家聲', 'storyKeys＋trigger 齊');
ok('(0) rec112_other_fields_unchanged', !!rec112 && rec112.title === '《追風少年》MV 男主角' && rec112.tier === '中級' && rec112.type === '唱片通告' && rec112.year === 1992 && rec112.season === '春' && rec112.days === 3 && JSON.stringify(rec112.pay) === '[330,396]' && rec112.singer === 'lok_gasing' && rec112.genre === '搖滾' && rec112.roleLabel === 'MV 男主角', 'title／tier／year／season／days／pay／singer 唔郁');
ok('(0) lok_patron_grants_match', html.indexOf('{ id:"credit_enc83_lok_patron", debtor:"駱家聲", title:"監製引薦"') >= 0, 'lok_patron 授出同一筆債權（id＋debtor＋title 一致）');
ok('(0) lok_patron_gate_unchanged', html.indexOf('{ id:"lok_patron", when(st){ return enc79TierOf(st.fav)>=4 && !!(S.flags||{}).lok_calm_truth && !(S.flags||{}).lok_join_rant && !(S.flags||{}).lok_loose_row && !(S.flags||{}).lok_cover_first; }') >= 0, 'v314 嚴格閘一行都唔郁');
ok('(0) rec111_unchanged', !!rec111 && JSON.stringify(rec111.storyKeys) === '["N14"]' && rec111.trigger && rec111.trigger.creditId === 'credit_enc83_lok_patron' && rec111.tier === '高級', 'rec_111 係 N14 tag＋lok trigger 共用，唔郁');
ok('(0) rec102_unchanged', !!rec102 && JSON.stringify(rec102.storyKeys) === '["lok_gasing"]' && !rec102.trigger, '初級搖滾 rec_102 唔郁');
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

// ---------- (1) 未持有債權：唔上板 ----------
resetS316();
ok('(1) no_credit_not_on', triggerGigOn(rec112) === false && br89GigOn({ id: 'gig_1992_rec_112' }) === false, 'D-4 觸發前隱藏');
resetS316();
S.mockCredits = [{ id: 'credit_enc83_luk_patron', debtor: '陸柏言', title: '天王引薦', line: 'x', status: '未收' }];
ok('(1) other_credit_not_on', triggerGigOn(rec112) === false, '持有陸引薦都唔開駱嗰張');

// ---------- (2) 持有債權：經通用 trigger 系統上板 ----------
resetS316();
S.mockCredits = [Object.assign({}, LOK_CREDIT)];
ok('(2) held_on_via_trigger', triggerGigOn(rec112) === true && br89GigOn({ id: 'gig_1992_rec_112' }) === true && triggerGigOn(rec111) === true, '持債權：兩張都開');
_date316 = new Date(1991, 10, 1);
ok('(2) window_not_yet', gigSeasonEarlyVisible88(rec112) === false, '1991-11-01 未入窗');
_date316 = new Date(1992, 2, 15);
ok('(2) window_open', gigSeasonEarlyVisible88(rec112) === true, '1992-03-15 可見（1992 春，span [3,5]＋提早 60 日）');

// ---------- (3) 雙 gig 同一筆債權：殺青邊張，另一張自動落板 ----------
resetS316();
S.mockCredits = [Object.assign({}, LOK_CREDIT)];
br89OnGigComplete('gig_1992_rec_111');
ok('(3) redeem_111_closes_112', S.mockCredits[0].redeemedBy === 'gig_1992_rec_111' && br89GigOn({ id: 'gig_1992_rec_112' }) === false && br89GigOn({ id: 'gig_1992_rec_111' }) === false && triggerGigOn(rec112) === false, '殺青《銅鑼灣》：新張自動落板');
resetS316();
S.mockCredits = [Object.assign({}, LOK_CREDIT)];
br89OnGigComplete('gig_1992_rec_112');
ok('(3) redeem_112_closes_111', S.mockCredits[0].redeemedBy === 'gig_1992_rec_112' && br89GigOn({ id: 'gig_1992_rec_111' }) === false && triggerGigOn(rec111) === false, '殺青《追風少年》：舊張自動落板');
resetS316();
S.mockCredits = [Object.assign({}, LOK_CREDIT)];
const lokLine = creditRedeemLine283({ id: 'credit_enc83_lok_patron' });
ok('(3) H_shows_both_titles', lokLine.indexOf('可以換：') >= 0 && lokLine.indexOf('銅鑼灣') >= 0 && lokLine.indexOf('追風少年') >= 0, '人情卡「可以換」出齊兩張名（BR89 反查自動）');

// ---------- (4) 舊檔唔 crash ----------
resetS316();
S.mockCredits = [];
let threw316 = false;
try{ triggerGigOn(rec112); br89GigOn({ id: 'gig_1992_rec_112' }); }catch(e){ threw316 = true; }
ok('(4) old_save_no_credit_no_throw', !threw316 && triggerGigOn(rec112) === false, '無債權舊檔唔掟錯');
resetS316();
delete S.mockCredits;
threw316 = false;
try{ triggerGigOn(rec112); br89GigOn({ id: 'gig_1992_rec_112' }); }catch(e){ threw316 = true; }
ok('(4) old_save_no_mockCredits_no_throw', !threw316 && triggerGigOn(rec112) === false, '無 mockCredits 舊檔唔掟錯');
resetS316();
S.mockCredits = [Object.assign({}, LOK_CREDIT, { status: '絕響' })];
ok('(4) expired_credit_not_on', triggerGigOn(rec112) === false, '絕響債權唔開');

console.log(fails.length === 0 ? 'ALL PASS' : 'FAILURES: ' + fails.join(', '));
process.exit(fails.length === 0 ? 0 : 1);
