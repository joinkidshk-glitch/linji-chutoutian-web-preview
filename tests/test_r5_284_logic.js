// v20a284 R5 人情兌現票餘項（B＋C＋D＋E＋F＋G）：
//   B 芬姐 tv_201 改 1991 春＋中級（pay 跟中級 peer 帶）；C film_112 拆死 trigger 變普通板通告
//     ＋CREDIT_REDEEM_GIG283 清走 lu_team 行；D tv_106 改 1992 春（初級不變）；
//   E 霞姐情報貨幣：每筆執漏人情＝茶餐廳多打聽一次（用完消耗，情報用現成風聲池）；
//   F 新 1992 年陸引薦 gig_1992_film_114《海角歸人》＋BR89 第 15 對；
//   G 還錢授登台引薦債權（冪等，OR 閘留返做舊存檔遷移路）。
// 用法：node tests/test_r5_284_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const root = path.join(__dirname, '..');
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
var MOCK_ASK = eval('(' + extractObjLiteral('const MOCK_ASK = {') + ')');
var GIG_SEASON_SPAN88 = eval('(' + extractObjLiteral('const GIG_SEASON_SPAN88 = {') + ')');
var GIG_SEASON_LEAD88 = Number((html.match(/const GIG_SEASON_LEAD88\s*=\s*(\d+)/) || [])[1] || 60);
eval(asVar(extractConst('ENC79_STARS'), 'ENC79_STARS'));
eval(asVar(extractConst('ENC79_TEA_POOL'), 'ENC79_TEA_POOL'));
var S = { mockCredits: [] };
var mirrorCalls = 0;
var _toasts284 = [];
let _ys284 = { year: 1991, season: '春' };
let _date284 = new Date(1991, 2, 15);
let _rand284 = 0.1;
function journalText(s){ return String(s == null ? '' : s); }
function syncNotebookMirror(){ mirrorCalls++; }
function saveQ(){}
function refreshMoneyHud(){}
function toast(t, o){ _toasts284.push(String(t) + ' ' + ((o && o.sub) ? String(o.sub) : '')); }
function ensureMockJournal(){ if(!Array.isArray(S.mockRumors)) S.mockRumors = []; if(!Array.isArray(S.mockDebts)) S.mockDebts = []; }
function yearSeasonNow(){ return _ys284; }
function dateObj(){ return _date284; }
function enc79Rand(){ return _rand284; }
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
eval(extractFn('enc79StarDef'));
eval(extractFn('enc79LocName'));
eval(extractFn('enc79EnsureStars'));
eval(extractFn('enc79WhisperActive'));
eval(extractFn('enc79GrantWhisper'));
eval(extractFn('enc79GrantCredit'));
eval(extractFn('enc79PayTea'));
eval(extractFn('enc79HelpAvailable'));
eval(extractFn('enc79CafeHelpHeld284'));
eval(extractFn('enc79ConsumeCafeHelp284'));
eval(extractFn('enc79TeaListen'));
eval(extractFn('enc79HelpClear'));
eval(extractFn('softSocialDailyState'));
eval(extractFn('softSocialDailyCap'));
eval(extractFn('softSocialDailyUse'));
eval(extractFn('mockAskDefs'));
eval(extractFn('enc83GuLoanTick'));
function resetS284(day){
  S = { dayIndex: day || 0, fame: 0, money: 500, flags: {}, npcs: { agent: 0 }, mockCredits: [], mockDebts: [], mockRumors: [], starWhispers: {}, favorDueSettled: {} };
  mirrorCalls = 0; _toasts284 = [];
}

// ---------- (0) 靜態結構 ----------
ok('(0) gig_count_306', allGigs.length === 306 && new Set(allGigs.map(g=>g.id)).size === 306, 'n=' + allGigs.length);
ok('(0) kind_credit_still_23', allGigs.filter(g=>g.trigger && g.trigger.kind === 'credit').length === 23, 'BR89 15＋通用 8');
ok('(0) br89_map_15_pairs', Object.keys(BR89_PATRON_OF_GIG).length === 15, 'n=' + Object.keys(BR89_PATRON_OF_GIG).length);
ok('(0) redeem_gig_map_8_entries', Object.keys(CREDIT_REDEEM_GIG283).length === 8, 'CREDIT_REDEEM_GIG283 8 個對照（lu_team 已清）');
ok('(0) lu_team_not_in_redeem_map', !('credit_wf3_lu_team' in CREDIT_REDEEM_GIG283), '舊存檔卡唔再出死行');
const tv201 = gigById['gig_1992_tv_201'];
ok('(0) B_tv201_fields', tv201 && tv201.year === 1991 && tv201.season === '春' && tv201.tier === '中級' && JSON.stringify(tv201.pay) === '[270,330]' && tv201.trigger && tv201.trigger.creditId === 'credit_fen_rescue' && tv201.days === 3, 'year/tier/pay/trigger');
ok('(0) B_tv201_pay_peer', tv201.pay[0] / tv201.days === 90 && tv201.pay[1] / tv201.days === 110, '中級電視 3 日 peer-exact（90–110／日，SPEC 7.1 中級帶 90–160／日）');
const tv106 = gigById['gig_1991_tv_106'];
ok('(0) D_tv106_fields', tv106 && tv106.year === 1992 && tv106.season === '春' && tv106.tier === '初級' && JSON.stringify(tv106.pay) === '[245,295]' && tv106.trigger && tv106.trigger.creditId === 'credit_enc79_yip_manager', '改年改季，級別／片酬／trigger 不變');
const f112 = gigById['gig_1991_film_112'];
ok('(0) C_f112_no_trigger', f112 && !f112.trigger && !f112.discoverNote && f112.blurb.indexOf('引薦') < 0 && f112.tier === '初級' && JSON.stringify(f112.pay) === '[1100,1320]', '普通板通告：無 trigger／無 discoverNote／blurb 無引薦句');
ok('(0) C_f112_source_clean', html.indexOf('credit_wf3_lu_team:"gig_1991_film_112"') < 0 && html.indexOf('"creditId": "credit_wf3_lu_team"') < 0, '對照＋trigger 兩處已清（結局讀取 L12913 保留，永不觸發）');
const f114 = gigById['gig_1992_film_114'];
ok('(0) F_f114_fields', f114 && f114.year === 1992 && f114.season === '春' && f114.tier === '中級' && f114.type === '電影' && f114.days === 12 && JSON.stringify(f114.pay) === '[1210,1430]' && JSON.stringify(f114.fame) === '[28,45]' && f114.req && f114.req.acting === 75 && f114.posterBrief && f114.trigger && f114.trigger.creditId === 'credit_enc83_luk_patron', '中級 12 日 peer-exact（同 film_101 形狀）');
ok('(0) F_f114_cast', f114.cast && f114.cast.leadM === 'luk_baakyin' && f114.cast.leadF === 'chung_choning' && f114.cast.supportM === null && f114.cast.supportF === 'kong_siying', '四格：陸主演＋鍾女主＋玩家格＋江配角');
ok('(0) F_f114_title_no_year_digits', !/[0-9]/.test(f114.workTitle) && !/[0-9]/.test(f114.title) && allGigs.filter(g=>g.workTitle === '海角歸人').length === 1, '標題唔含年份數字（YEARS66 唔會 +2）');
ok('(0) F_f114_in_br89', BR89_PATRON_OF_GIG['gig_1992_film_114'] === 'credit_enc83_luk_patron' && BR89_PATRON_OF_GIG['gig_1991_film_101'] === 'credit_enc83_luk_patron', '同一筆債權兩張兌現通告');

// ---------- (1) B：芬姐窗口喺絕響之前開到 ----------
// 春 span [3,5]＋提早 60 日：1991 春 gig 可見 1990-12-31–1991-05-31；絕響最早 1991-06-01（1991 夏）。
_date284 = new Date(1991, 2, 15);
ok('(1) B_window_mid_spring', gigSeasonEarlyVisible88(tv201) === true, '1991-03-15 可見');
_date284 = new Date(1991, 4, 31);
ok('(1) B_window_last_day', gigSeasonEarlyVisible88(tv201) === true, '1991-05-31 仲可見');
_date284 = new Date(1991, 5, 1);
ok('(1) B_window_closed_before_exodus', gigSeasonEarlyVisible88(tv201) === false, '1991-06-01 落板——絕響同一日先嚟，窗口全程喺絕響之前');
ok('(1) B_season_span_spring', JSON.stringify(GIG_SEASON_SPAN88['春']) === '[3,5]' && GIG_SEASON_LEAD88 === 60, 'span/lead 常量');

// ---------- (2) C：死 trigger 拆走之後嘅行為 ----------
// 舊存檔持有 credit_wf3_lu_team 嘅卡：唔再出「可以換」行（唔留死行）。
ok('(2) C_old_save_card_no_dead_line', creditRedeemLine283({ id: 'credit_wf3_lu_team', debtor: '陸柏言', title: '天王團隊', line: '舊卡。', status: '未收' }) === '', 'lu_team 卡返空字串');
resetS284(100);
S.mockCredits = [{ id: 'credit_wf3_lu_team', debtor: '陸柏言', title: '天王團隊', line: '舊卡。' }];
let threw284 = false;
try{ genericCreditOnGigComplete283('gig_1991_film_112'); }catch(e){ threw284 = true; }
ok('(2) C_kill_no_mark_no_throw', !threw284 && S.mockCredits[0].redeemedBy === undefined, 'film_112 殺青唔再標 redeemedBy，唔掟錯');
// 通用 8 張其餘照標（抽查一張：芬姐 tv_201）。
resetS284(100);
S.mockCredits = [{ id: 'credit_fen_rescue', debtor: '芬姐', title: 't', line: '原句。' }];
genericCreditOnGigComplete283('gig_1992_tv_201');
ok('(2) C_generic_others_still_mark', S.mockCredits[0].redeemedBy === 'gig_1992_tv_201' && S.mockCredits[0].line.indexOf('芬姐茶檔') >= 0, '通用分支其餘 8 張照標');

// ---------- (3) D：葉守口窗口喺授出之後開到 ----------
// 1992 春 gig 可見 1991-12-31–1992-05-31；授出多數 1991 秋後，窗口開嗰陣債權已在手。
_date284 = new Date(1991, 11, 15);
ok('(3) D_window_not_yet', gigSeasonEarlyVisible88(tv106) === false, '1991-12-15 未入窗');
_date284 = new Date(1992, 0, 15);
ok('(3) D_window_open', gigSeasonEarlyVisible88(tv106) === true, '1992-01-15 可見——授出（1991 秋–冬）之後');
_date284 = new Date(1992, 2, 15);
ok('(3) D_window_mid_spring', gigSeasonEarlyVisible88(tv106) === true, '1992-03-15 可見');

// ---------- (4) E：霞姐情報貨幣 ----------
// 單元：持有／消耗。
resetS284(200);
S.mockCredits = [
  { id: 'credit_enc79_cafe_help_190', debtor: '霞姐', title: '執漏幫手人情', line: '幫手。', status: '未收' },
  { id: 'credit_enc79_cafe_help_195', debtor: '霞姐', title: '執漏幫手人情', line: '幫手。', status: '未收' },
  { id: 'credit_enc79_cafe_help_180', debtor: '霞姐', title: '執漏幫手人情', line: '已用。', status: '未收', redeemedBy: 'cafe_help_intel' },
  { id: 'credit_enc79_cafe_help_170', debtor: '霞姐', title: '執漏幫手人情', line: '絕響。', status: '絕響' },
];
ok('(4) E_held_counts_unredeemed_only', enc79CafeHelpHeld284().length === 2, '未兌現＋未絕響先計');
ok('(4) E_old_save_compat', enc79CafeHelpHeld284().some(c=>c.id === 'credit_enc79_cafe_help_190'), '舊存檔（舊 dayIndex）照計');
const c284 = enc79CafeHelpHeld284()[0];
ok('(4) E_consume_marks', enc79ConsumeCafeHelp284(c284) === true && c284.redeemedBy === 'cafe_help_intel' && c284.line.indexOf('已兌現：霞姐情報') >= 0 && enc79CafeHelpHeld284().length === 1, '消耗標 redeemedBy＋加已兌現句');
ok('(4) E_consume_idempotent', enc79ConsumeCafeHelp284(c284) === false && (c284.line.match(/已兌現：霞姐情報/g) || []).length === 1, '重複消耗唔重複加句');
ok('(4) E_consume_null_safe', enc79ConsumeCafeHelp284(null) === false && enc79ConsumeCafeHelp284(undefined) === false, 'null 唔掟錯');
// 端到端：每日 2 次用晒 → 每筆多打聽一次，用完消耗。
const _mr284 = Math.random;
Math.random = ()=>0.10; /* 風聲路徑；霞姐強制風聲揀 targets[0] */
resetS284(300);
S.money = 500;
S.mockCredits = [
  { id: 'credit_enc79_cafe_help_290', debtor: '霞姐', title: '執漏幫手人情', line: '幫手。', status: '未收' },
  { id: 'credit_enc79_cafe_help_295', debtor: '霞姐', title: '執漏幫手人情', line: '幫手。', status: '未收' },
];
const teaA = enc79TeaListen({ id: 'act_cha_hall_tea', moneyCost: 15, source: '金龍茶餐廳' });
const teaB = enc79TeaListen({ id: 'act_cha_hall_tea', moneyCost: 15, source: '金龍茶餐廳' });
ok('(4) E_normal_two_listens', teaA && teaA.ok && teaB && teaB.ok && S.money === 470 && Object.keys(S.starWhispers).length === 2, '每日頭 2 次正常打聽，唔用霞姐人情');
ok('(4) E_normal_listens_keep_credit', enc79CafeHelpHeld284().length === 2, '頭 2 次唔消耗');
const teaC = enc79TeaListen({ id: 'act_cha_hall_tea', moneyCost: 15, source: '金龍茶餐廳' });
ok('(4) E_third_uses_credit', teaC && teaC.ok && teaC.intelText.indexOf('3 日內有效') >= 0 && S.money === 455 && Object.keys(S.starWhispers).length === 3, '第 3 次用霞姐人情：保底星風聲（現成風聲池）');
ok('(4) E_third_consumes_one', enc79CafeHelpHeld284().length === 1 && S.mockCredits.filter(c=>c.redeemedBy === 'cafe_help_intel').length === 1 && teaC.toast.indexOf('尚餘 1 筆') >= 0, '用一次消耗一筆，toast 講明尚餘');
const teaD = enc79TeaListen({ id: 'act_cha_hall_tea', moneyCost: 15, source: '金龍茶餐廳' });
ok('(4) E_fourth_uses_last_credit', teaD && teaD.ok && S.money === 440 && Object.keys(S.starWhispers).length === 4 && enc79CafeHelpHeld284().length === 0 && teaD.toast.indexOf('尚餘 0 筆') >= 0, '第 4 次用埋最後一筆');
const teaE = enc79TeaListen({ id: 'act_cha_hall_tea', moneyCost: 15, source: '金龍茶餐廳' });
ok('(4) E_fifth_blocked_no_credit', teaE && teaE.ok === false && /已用晒/.test(teaE.toast) && S.money === 440, '冇人情就擋返（每日上限），唔收錢');
Math.random = _mr284;
// 無人情：用晒 2 次就擋。
resetS284(310);
S.money = 500;
enc79TeaListen({ id: 'act_cha_hall_tea', moneyCost: 15, source: '金龍茶餐廳' });
enc79TeaListen({ id: 'act_cha_hall_tea', moneyCost: 15, source: '金龍茶餐廳' });
const teaBlocked = enc79TeaListen({ id: 'act_cha_hall_tea', moneyCost: 15, source: '金龍茶餐廳' });
ok('(4) E_no_credit_blocked', teaBlocked && teaBlocked.ok === false && S.money === 470, '無霞姐人情：第 3 次照擋');
// 風聲開晒：唔消耗，唔收錢。
resetS284(320);
S.money = 500;
S.mockCredits = [{ id: 'credit_enc79_cafe_help_315', debtor: '霞姐', title: '執漏幫手人情', line: '幫手。', status: '未收' }];
S.starWhispers = {};
for(const s of ENC79_STARS) S.starWhispers[s.id] = { until: 9999, src: 'tea' };
enc79TeaListen({ id: 'act_cha_hall_tea', moneyCost: 15, source: '金龍茶餐廳' });
enc79TeaListen({ id: 'act_cha_hall_tea', moneyCost: 15, source: '金龍茶餐廳' });
const teaQuiet = enc79TeaListen({ id: 'act_cha_hall_tea', moneyCost: 15, source: '金龍茶餐廳' });
ok('(4) E_no_targets_no_consume', teaQuiet && teaQuiet.ok === false && /留返第日用/.test(teaQuiet.toast) && S.money === 470 && enc79CafeHelpHeld284().length === 1, '行內靜靜哋：人情留返，唔收茶錢');
// 打聽掣提示：持人情嗰陣講明可多打聽幾多次。
resetS284(330);
S.mockCredits = [
  { id: 'credit_enc79_cafe_help_325', debtor: '霞姐', title: '執漏幫手人情', line: '幫手。', status: '未收' },
  { id: 'credit_enc79_cafe_help_328', debtor: '霞姐', title: '執漏幫手人情', line: '幫手。', status: '未收' },
];
const defsWith = mockAskDefs('cafe_cha');
const teaDefWith = (defsWith || []).find(d=>d && d.id === 'act_cha_hall_tea');
ok('(4) E_hint_shows_count', !!teaDefWith && String(teaDefWith.hint || '').indexOf('霞姐人情 ×2') >= 0 && String(teaDefWith.hint || '').indexOf('每次消耗一筆') >= 0, '飲茶掣 hint 講明 ×2＋每次消耗一筆');
resetS284(331);
const defsWithout = mockAskDefs('cafe_cha');
const teaDefWithout = (defsWithout || []).find(d=>d && d.id === 'act_cha_hall_tea');
ok('(4) E_hint_hidden_without_credit', !!teaDefWithout && String(teaDefWithout.hint || '').indexOf('霞姐人情') < 0, '無人情嗰陣唔出提示');
// 幫手授出照舊（E 唔郁授出路；R1 結局計數照舊剔除）。
resetS284(340);
S.flags.enc79HelpDay = -1;
const help284 = enc79HelpClear({ id: 'act_cha_help_clear' });
ok('(4) E_help_grant_unchanged', help284 && help284.ok && S.mockCredits.some(c=>c.id === 'credit_enc79_cafe_help_340') && favorCreditCountsAsHeld(S.mockCredits.find(c=>c.id === 'credit_enc79_cafe_help_340')) === false, '執漏照授債權，結局計數照剔除');

// ---------- (5) F：陸引薦第二張 ----------
// 兩張兌現通告共用同一筆債權：殺青邊張，另一張自動落板。
resetS284(400);
S.mockCredits = [{ id: 'credit_enc83_luk_patron', debtor: '陸柏言', title: '天王引薦', line: 'x', status: '未收' }];
ok('(5) F_both_on_when_held', br89GigOn({ id: 'gig_1991_film_101' }) === true && br89GigOn({ id: 'gig_1992_film_114' }) === true, '持債權：兩張都開');
br89OnGigComplete('gig_1991_film_101');
ok('(5) F_redeem_first_closes_second', S.mockCredits[0].redeemedBy === 'gig_1991_film_101' && br89GigOn({ id: 'gig_1992_film_114' }) === false && br89GigOn({ id: 'gig_1991_film_101' }) === false, '殺青《江河歲月》：新張自動落板');
resetS284(401);
S.mockCredits = [{ id: 'credit_enc83_luk_patron', debtor: '陸柏言', title: '天王引薦', line: 'x', status: '未收' }];
br89OnGigComplete('gig_1992_film_114');
ok('(5) F_redeem_second_closes_first', S.mockCredits[0].redeemedBy === 'gig_1992_film_114' && br89GigOn({ id: 'gig_1991_film_101' }) === false, '殺青《海角歸人》：舊張自動落板');
const lukLine = creditRedeemLine283({ id: 'credit_enc83_luk_patron' });
ok('(5) F_H_shows_both_titles', lukLine.indexOf('可以換：') >= 0 && lukLine.indexOf('江河歲月') >= 0 && lukLine.indexOf('海角歸人') >= 0, '人情卡「可以換」出齊兩張名（BR89 反查自動）');
// 新張窗口：1992 春，可見 1991-12-31–1992-05-31。
_date284 = new Date(1991, 10, 1);
ok('(5) F_window_not_yet', gigSeasonEarlyVisible88(f114) === false, '1991-11-01 未入窗');
_date284 = new Date(1992, 2, 15);
ok('(5) F_window_open', gigSeasonEarlyVisible88(f114) === true, '1992-03-15 可見——1992 先上到 70 分嘅玩家趕得切');

// ---------- (6) G：還錢授登台引薦債權 ----------
function loanS284(day, amt){
  resetS284(day);
  S.money = 1600;
  S.mockCredits = [{ id: 'credit_enc83_gu_loan', debtor: '顧明輝', title: '借錢', line: '借。', status: '未收' }];
  S.flags.enc83_gu_loan_due = 428;
  S.flags.enc83_gu_loan_amt = amt;
  S.flags.enc83_gu_loan_lvl = 1;
  S.flags.enc83_gu_loan_day = 400;
  S.dayIndex = 428;
}
_rand284 = 0.1; /* lvl 1 還款門檻 0.3 → 還款路 */
loanS284(400, 400);
enc83GuLoanTick();
ok('(6) G_repay_grants_patron_credit', S.flags.enc83_gu_loan_result === 1 && S.money === 2000 && S.mockCredits.some(c=>c.id === 'credit_enc83_gu_patron' && c.debtor === '顧明輝' && c.title === '登台引薦') && !S.mockCredits.some(c=>c.id === 'credit_enc83_gu_loan'), '還錢：授卡＋還錢＋借錢債權移出');
ok('(6) G_repay_toast_mentions_card', _toasts284.join(' ').indexOf('登台引薦') >= 0, '還錢 toast 副句講明寫咗登台引薦卡片');
enc83GuLoanTick();
ok('(6) G_repay_idempotent', S.mockCredits.filter(c=>c.id === 'credit_enc83_gu_patron').length === 1 && S.money === 2000, '重複 tick 唔重複授、唔重複還錢');
_rand284 = 0.1;
loanS284(400, 400);
S.mockCredits.push({ id: 'credit_enc83_gu_patron', debtor: '顧明輝', title: '登台引薦', line: '舊卡。', status: '未收' });
enc83GuLoanTick();
ok('(6) G_preheld_no_duplicate', S.mockCredits.filter(c=>c.id === 'credit_enc83_gu_patron').length === 1 && (S.mockCredits.find(c=>c.id === 'credit_enc83_gu_patron').line || '') === '舊卡。', '已持卡：還錢唔重複授，舊卡原句不變');
_rand284 = 0.9; /* → 壞帳路 */
loanS284(400, 400);
enc83GuLoanTick();
ok('(6) G_void_no_credit', S.flags.enc83_gu_loan_result === 2 && S.money === 1600 && !S.mockCredits.some(c=>c.id === 'credit_enc83_gu_patron'), '壞帳：唔授卡');
ok('(6) G_or_gate_kept', html.indexOf('v20a229 B5 R-4') >= 0 && html.indexOf('if(raw.id==="gig_1992_rec_205")') >= 0, 'OR 閘留返：v284 之前已還錢嘅舊存檔靠佢開通告（tick 唔會重跑）');

// ---------- (7) 收尾 ----------
// 舊存檔兼容：film_112 變普通板通告，triggerGigOn 唔再需要佢；tv_201／tv_106 id 不變，H 對照照用 id。
ok('(7) ids_unchanged', !!gigById['gig_1992_tv_201'] && !!gigById['gig_1991_tv_106'] && !!gigById['gig_1991_film_112'], '三張舊 gig id 不變（H 對照／舊存檔唔斷）');
ok('(7) no_dead_lu_team_trigger', !allGigs.some(g=>g.trigger && g.trigger.creditId === 'credit_wf3_lu_team'), '全庫再無 lu_team trigger');

console.log(fails.length === 0 ? 'ALL PASS' : 'FAILURES: ' + fails.join(', '));
process.exit(fails.length === 0 ? 0 : 1);
