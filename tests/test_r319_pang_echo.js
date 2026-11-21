// v20a319 彭少祺支線回響通告：新開 gig_1992_variety_106《星光慈善夜》慈善晚會主持
//   SPEC §3.6B 彭行（SPEC.md:784）：司儀／綜藝主持通告｜中級。現有兩張都唔啱——
//   variety_104《歡樂大騷》崗位啱（主持）但初級；variety_203《台慶大騷》中級但崗位係台上助理
//   （草稿寫明係「助手位」，唔郁）。新 gig 1992 秋中級主持，數字照抄標板 variety_103《樂善之夜》
//   （req 台風 45＋魅力 30／pay [350,420]（v368 擔正片酬拉入 $350–600 帶）／fame [28,45]），storyKeys pang_siuki＋credit trigger
//   credit_enc84_pang_patron，BR89 加第 18 對（同 variety_203 同一筆債權，陸／駱／齊雙 gig 前例）。
//   季節窗實測（gigSeasonEarlyVisible88，秋 span [9,11]＋提早 60 日）：1992-07-01 未入、
//   1992-08-31 已入提早窗、1992-09-15 可見、1992-12-15 已過季尾（11-30）唔見——
//   brief 原寫「08-31 未入／12-15 照見」同 live 函數唔符，已按函數實測更正。
// 用法：node tests/test_r319_pang_echo.js [path-to-index.html]
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
let _ys319 = { year: 1992, season: '秋' };
let _date319 = new Date(1992, 8, 15);
function journalText(s){ return String(s == null ? '' : s); }
function syncNotebookMirror(){}
function saveQ(){}
function refreshMoneyHud(){}
function toast(){}
function ensureMockJournal(){ if(!Array.isArray(S.mockRumors)) S.mockRumors = []; if(!Array.isArray(S.mockDebts)) S.mockDebts = []; }
function yearSeasonNow(){ return _ys319; }
function dateObj(){ return _date319; }
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
function resetS319(){
  S = { dayIndex: 0, fame: 0, money: 500, flags: {}, npcs: {}, mockCredits: [], mockDebts: [], mockRumors: [], favorDueSettled: {}, grant229Queue: [], contracts229: [] };
}
const PANG_CREDIT = { id: 'credit_enc84_pang_patron', debtor: '彭少祺', title: '司儀引薦', line: '彭少祺喺大騷監製面前提咗你個名：嗰個後生仔唔係齋企喺度嗰啲臨記，畀個機會佢企上台試下。', status: '未收' };

// ---------- (0) 靜態結構 ----------
const v106 = gigById['gig_1992_variety_106'];
const v103 = gigById['gig_1991_variety_103'];
const v203 = gigById['gig_1991_variety_203'];
const v104 = gigById['gig_1991_variety_104'];
ok('(0) gig_count_330', allGigs.length === 330 && new Set(allGigs.map(g=>g.id)).size === 330, 'n=' + allGigs.length);
ok('(0) trig_38_credit_27', allGigs.filter(g=>g.trigger && g.trigger.kind).length === 38 && allGigs.filter(g=>g.trigger && g.trigger.kind === 'credit').length === 27, 'credit 27（BR89 19＋通用 8）');
ok('(0) v106_fields_match_template', !!v106 && v106.title === '《星光慈善夜》慈善晚會主持' && v106.type === '綜藝' && v106.tier === '中級' && v106.category === '作品' && v106.genre === '晚會' && v106.workTitle === '星光慈善夜' && v106.roleLabel === '慈善晚會主持' && v106.loc === 'tvb_kowloon' && v106.director === '晚會監製' && v106.year === 1992 && v106.season === '秋' && v106.days === 2 && v106.roleScale === 'variety_host_lead' && JSON.stringify(v106.req) === '{"stage":45,"charm":30}' && v106.hard === 0.5 && JSON.stringify(v106.pay) === '[350,420]' && JSON.stringify(v106.fame) === '[28,45]' && v106.host === null && JSON.stringify(v106.guests) === '["pang_siuki","so_jiyan","gu_mingfai"]' && JSON.stringify(v106.segments) === '["慈善拍賣","歌舞表演","捐款公佈"]', '數字照抄標板 variety_103');
ok('(0) v106_tag_trigger', !!v106 && JSON.stringify(v106.storyKeys) === '["pang_siuki"]' && v106.trigger && v106.trigger.kind === 'credit' && v106.trigger.creditId === 'credit_enc84_pang_patron' && v106.trigger.creditOwner === '彭少祺', 'storyKeys＋trigger 齊');
ok('(0) v106_matches_template_numbers', !!v103 && !!v106 && v106.tier === v103.tier && v106.category === v103.category && v106.genre === v103.genre && v106.days === v103.days && v106.roleScale === v103.roleScale && JSON.stringify(v106.req) === JSON.stringify(v103.req) && v106.hard === v103.hard && JSON.stringify(v106.pay) === JSON.stringify(v103.pay) && JSON.stringify(v106.fame) === JSON.stringify(v103.fame) && JSON.stringify(v106.guests) === JSON.stringify(v103.guests) && JSON.stringify(v106.segments) === JSON.stringify(v103.segments), '同 variety_103 逐項對照，數字一致');
ok('(0) pang_patron_grants_match', html.indexOf('{ id:"credit_enc84_pang_patron", debtor:"彭少祺", title:"司儀引薦"') >= 0, 'pang_patron 授出同一筆債權（id＋debtor＋title 一致）');
ok('(0) pang_patron_gate_t4_only', html.indexOf('{ id:"pang_patron", when(st){ return enc79TierOf(st.fav)>=4; }') >= 0, 'pang_patron 閘淨 T4，無年份窗、無冷版對照，唔郁');
ok('(0) v203_unchanged', !!v203 && v203.tier === '中級' && v203.roleLabel === '台上助理' && v203.category === '臨記通告' && JSON.stringify(v203.storyKeys) === '["pang_siuki"]' && v203.trigger && v203.trigger.creditId === 'credit_enc84_pang_patron', 'variety_203 係中級助理＋tag＋trigger，唔郁');
ok('(0) v104_unchanged', !!v104 && v104.tier === '初級' && v104.roleLabel === '綜合節目遊戲環節主持' && !v104.storyKeys && !v104.trigger, 'variety_104 係初級主持、無 tag 無 trigger，唔郁');
ok('(0) mc_gigs_7', allGigs.filter(g=>g.type === '綜藝' && (g.roleLabel || '').indexOf('主持') >= 0).length === 9, '司儀類 7→9（v372 +2 主持通告）');
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
ok('(0) board_1992_autumn_variety_3_rare_open', allGigs.filter(g=>g.type === '綜藝' && g.year === 1992 && g.season === '秋' && !g.trigger).length === 3 && allGigs.filter(g=>g.type === '綜藝' && g.year === 1992 && g.season === '秋' && !g.trigger).every(g=>g.tier === '稀有') && allGigs.filter(g=>g.type === '綜藝' && g.tier === '中級' && g.year === 1992 && g.season === '秋' && !g.trigger).length === 0, '1992 秋綜藝開放板維持 3 張稀有，中級開放 0→0（新 gig 係 trigger 閘，唔入開放板）');

// ---------- (1) 未持有債權：唔上板 ----------
resetS319();
ok('(1) no_credit_not_on', triggerGigOn(v106) === false && br89GigOn({ id: 'gig_1992_variety_106' }) === false, 'D-4 觸發前隱藏');
resetS319();
S.mockCredits = [{ id: 'credit_enc83_chai_patron', debtor: '齊鎮海', title: '一哥引薦', line: 'x', status: '未收' }];
ok('(1) other_credit_not_on', triggerGigOn(v106) === false, '持有齊引薦都唔開彭嗰張');

// ---------- (2) 持有債權：經通用 trigger 系統上板 ----------
resetS319();
S.mockCredits = [Object.assign({}, PANG_CREDIT)];
ok('(2) held_on_via_trigger', triggerGigOn(v106) === true && br89GigOn({ id: 'gig_1992_variety_106' }) === true && triggerGigOn(v203) === true, '持債權：兩張都開');
_date319 = new Date(1992, 6, 1);
ok('(2) window_not_yet', gigSeasonEarlyVisible88(v106) === false, '1992-07-01 未入窗（提早窗由 07-03 起）');
_date319 = new Date(1992, 7, 31);
ok('(2) window_early', gigSeasonEarlyVisible88(v106) === true, '1992-08-31 已入提早窗（秋 span [9,11]＋提早 60 日）');
_date319 = new Date(1992, 8, 15);
ok('(2) window_open', gigSeasonEarlyVisible88(v106) === true, '1992-09-15 可見');
_date319 = new Date(1992, 11, 15);
ok('(2) window_past', gigSeasonEarlyVisible88(v106) === false, '1992-12-15 已過季尾（11-30）唔見');

// ---------- (3) 雙 gig 同一筆債權：殺青邊張，另一張自動落板 ----------
resetS319();
S.mockCredits = [Object.assign({}, PANG_CREDIT)];
br89OnGigComplete('gig_1991_variety_203');
ok('(3) redeem_203_closes_106', S.mockCredits[0].redeemedBy === 'gig_1991_variety_203' && br89GigOn({ id: 'gig_1992_variety_106' }) === false && br89GigOn({ id: 'gig_1991_variety_203' }) === false && triggerGigOn(v106) === false, '殺青《台慶大騷》：新張自動落板');
resetS319();
S.mockCredits = [Object.assign({}, PANG_CREDIT)];
br89OnGigComplete('gig_1992_variety_106');
ok('(3) redeem_106_closes_203', S.mockCredits[0].redeemedBy === 'gig_1992_variety_106' && br89GigOn({ id: 'gig_1991_variety_203' }) === false && triggerGigOn(v203) === false, '殺青《星光慈善夜》：舊張自動落板');
resetS319();
S.mockCredits = [Object.assign({}, PANG_CREDIT)];
const pangLine = creditRedeemLine283({ id: 'credit_enc84_pang_patron' });
ok('(3) H_shows_both_titles', pangLine.indexOf('可以換：') >= 0 && pangLine.indexOf('台慶大騷') >= 0 && pangLine.indexOf('星光慈善夜') >= 0, '人情卡「可以換」出齊兩張名（BR89 反查自動）');

// ---------- (4) GRANT229 彭行唔郁 ----------
resetS319();
ok('(4) grant229_late_still_104', grant229RecordFromEnc79('beat:pang_intel', '遲咗') === true && S.grant229Queue.length === 1 && S.grant229Queue[0].gigId === 'gig_1991_variety_104', '「遲咗」照派 variety_104（唔使持債，唔郁）');
resetS319();
ok('(4) grant229_memory_still_103', grant229RecordFromEnc79('first:pang_siuki', '記性') === true && S.grant229Queue.length === 1 && S.grant229Queue[0].gigId === 'gig_1992_variety_103', '「記性」照派 variety_103');
resetS319();
ok('(4) grant229_n17_still_ad107', grant229RecordFromEnc79('beat:pang_n17', '雲吞麵') === true && S.grant229Queue.length === 1 && S.grant229Queue[0].gigId === 'gig_1991_ad_107', 'n17「雲吞麵」照派 ad_107（草稿 L1545 提案另開票，唔入 v319）');
resetS319();
ok('(4) grant229_no_106_row', GRANT229_ENC79.every(r=>r.gigId !== 'gig_1992_variety_106'), 'variety_106 唔係即派 gig，淨係 credit trigger 路徑');

// ---------- (5) 舊檔唔 crash ----------
resetS319();
S.mockCredits = [];
let threw319 = false;
try{ triggerGigOn(v106); br89GigOn({ id: 'gig_1992_variety_106' }); }catch(e){ threw319 = true; }
ok('(5) old_save_no_credit_no_throw', !threw319 && triggerGigOn(v106) === false, '無債權舊檔唔掟錯');
resetS319();
delete S.mockCredits;
threw319 = false;
try{ triggerGigOn(v106); br89GigOn({ id: 'gig_1992_variety_106' }); }catch(e){ threw319 = true; }
ok('(5) old_save_no_mockCredits_no_throw', !threw319 && triggerGigOn(v106) === false, '無 mockCredits 舊檔唔掟錯');
resetS319();
S.mockCredits = [Object.assign({}, PANG_CREDIT, { status: '絕響' })];
ok('(5) expired_credit_not_on', triggerGigOn(v106) === false, '絕響債權唔開');

console.log(fails.length === 0 ? 'ALL PASS' : 'FAILURES: ' + fails.join(', '));
process.exit(fails.length === 0 ? 0 : 1);
