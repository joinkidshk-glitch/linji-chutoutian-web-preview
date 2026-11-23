// v20a337 魏詠男引薦第二張：新開 gig_1992_film_207《虎嘯龍吟》江湖拳手阿虎
//   G-NGAI-3 實駕 BUG-2：credit_enc83_ngai_patron（打女引薦）只掛 gig_1991_film_212
//   《鐵橋風雲》（1991 夏），patron beat 無年份閘，1992 年播出即授一筆永遠兌唔到嘅債權；
//   1991 年底播、未喺年內接 film_212 亦同樣死。跟陸柏言 film_101→film_114 接力前例：
//   新 gig 1992 春 film_harbour，數字逐項照抄 film_212（高級男主角／24 日／pay
//   [4416,5184]／req 演技 130＋體能 90／fame [35,55]／hard 0.58／同 cast），storyKeys
//   ngai_wingnaam＋credit trigger credit_enc83_ngai_patron，BR89 加第 19 對（同一筆債權，
//   殺青邊張都標 redeemedBy，另一張自動落板）。
//   季節窗實測（gigSeasonEarlyVisible88，春 span [3,5]＋提早 60 日）：1991-12-15 未入、
//   1992-01-15 已入提早窗、1992-03-15 可見、1992-06-15 已過季尾（05-31）唔見。
// 用法：node tests/test_r337_ngai_patron_1992.js [path-to-index.html]
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
let _ys337 = { year: 1992, season: '春' };
let _date337 = new Date(1992, 2, 15);
function journalText(s){ return String(s == null ? '' : s); }
function syncNotebookMirror(){}
function saveQ(){}
function refreshMoneyHud(){}
function toast(){}
function ensureMockJournal(){ if(!Array.isArray(S.mockRumors)) S.mockRumors = []; if(!Array.isArray(S.mockDebts)) S.mockDebts = []; }
function yearSeasonNow(){ return _ys337; }
function dateObj(){ return _date337; }
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
function resetS337(){
  S = { dayIndex: 0, fame: 0, money: 500, flags: {}, npcs: {}, mockCredits: [], mockDebts: [], mockRumors: [], favorDueSettled: {}, grant229Queue: [], contracts229: [] };
}
const NGAI_CREDIT = { id: 'credit_enc83_ngai_patron', debtor: '魏詠男', title: '打女引薦', line: '魏詠男畀咗個電話你：嗰位導演仲肯開武打戲，你打過去，提我個名，佢會見你一面。', status: '未收' };

// ---------- (0) 靜態結構 ----------
const f207 = gigById['gig_1992_film_207'];
const f212 = gigById['gig_1991_film_212'];
ok('(0) gig_count_330', allGigs.length === 330 && new Set(allGigs.map(g=>g.id)).size === 330, 'n=' + allGigs.length);
ok('(0) trig_38_credit_27', allGigs.filter(g=>g.trigger && g.trigger.kind).length === 38 && allGigs.filter(g=>g.trigger && g.trigger.kind === 'credit').length === 27, 'credit 27（BR89 19＋通用 8）');
ok('(0) f207_fields_match_template', !!f207 && f207.title === '《虎嘯龍吟》江湖拳手阿虎' && f207.type === '電影' && f207.tier === '高級' && f207.category === '作品' && f207.genre === '動作' && f207.workTitle === '虎嘯龍吟' && f207.roleLabel === '男主角' && f207.loc === 'film_harbour' && f207.director === '導演' && f207.year === 1992 && f207.season === '春' && f207.days === 24 && f207.roleScale === 'film_lead_big' && JSON.stringify(f207.req) === '{"acting":130,"stamina":90}' && f207.hard === 0.58 && JSON.stringify(f207.pay) === '[6182,7258]' && JSON.stringify(f207.fame) === '[35,55]' && JSON.stringify(f207.cast) === '{"leadM":null,"leadF":"ngai_wingnaam","supportM":"mak_zhendong","supportF":"wu_meilam"}' && (f207.discoverNote || '').indexOf('魏詠男引薦') >= 0 && !!f207.posterBrief, '數字照抄標板 film_212');
ok('(0) f207_tag_trigger', !!f207 && JSON.stringify(f207.storyKeys) === '["ngai_wingnaam"]' && f207.trigger && f207.trigger.kind === 'credit' && f207.trigger.creditId === 'credit_enc83_ngai_patron' && f207.trigger.creditOwner === '魏詠男', 'storyKeys＋trigger 齊');
ok('(0) f207_matches_f212_numbers', !!f212 && !!f207 && f207.tier === f212.tier && f207.category === f212.category && f207.genre === f212.genre && f207.type === f212.type && f207.loc === f212.loc && f207.days === f212.days && f207.roleScale === f212.roleScale && JSON.stringify(f207.req) === JSON.stringify(f212.req) && f207.hard === f212.hard && JSON.stringify(f207.pay) === JSON.stringify(f212.pay) && JSON.stringify(f207.fame) === JSON.stringify(f212.fame) && JSON.stringify(f207.cast) === JSON.stringify(f212.cast), '同 film_212 逐項對照，數字一致（陸 film_101→film_114 接力前例）');
ok('(0) ngai_patron_grants_match', html.indexOf('{ id:"credit_enc83_ngai_patron", debtor:"魏詠男", title:"打女引薦"') >= 0, 'ngai_patron 授出同一筆債權（id＋debtor＋title 一致）');
ok('(0) f212_unchanged', !!f212 && f212.tier === '高級' && f212.roleLabel === '男主角' && f212.year === 1991 && f212.season === '夏' && f212.category === '作品' && JSON.stringify(f212.storyKeys) === '["ngai_wingnaam"]' && f212.trigger && f212.trigger.creditId === 'credit_enc83_ngai_patron', 'film_212 係高級男主角＋tag＋trigger，唔郁');
ok('(0) year_pools_split', byYear[1991].some(g=>g.id === 'gig_1991_film_212') && !byYear[1991].some(g=>g.id === 'gig_1992_film_207') && byYear[1992].some(g=>g.id === 'gig_1992_film_207') && !byYear[1992].some(g=>g.id === 'gig_1991_film_212'), '1991 池得 film_212、1992 池得 film_207，唔互相污染');
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
resetS337();
ok('(1) no_credit_not_on', triggerGigOn(f207) === false && br89GigOn({ id: 'gig_1992_film_207' }) === false, 'D-4 觸發前隱藏');
resetS337();
S.mockCredits = [{ id: 'credit_enc83_luk_patron', debtor: '陸柏言', title: '一哥引薦', line: 'x', status: '未收' }];
ok('(1) other_credit_not_on', triggerGigOn(f207) === false, '持有陸引薦都唔開魏嗰張');

// ---------- (2) 持有債權：經通用 trigger 系統上板 ----------
resetS337();
S.mockCredits = [Object.assign({}, NGAI_CREDIT)];
ok('(2) held_on_via_trigger', triggerGigOn(f207) === true && br89GigOn({ id: 'gig_1992_film_207' }) === true && triggerGigOn(f212) === true, '持債權：兩張都開');
_date337 = new Date(1991, 11, 15);
ok('(2) window_not_yet', gigSeasonEarlyVisible88(f207) === false, '1991-12-15 未入窗（提早窗由 12-31 起）');
_date337 = new Date(1992, 0, 15);
ok('(2) window_early', gigSeasonEarlyVisible88(f207) === true, '1992-01-15 已入提早窗（春 span [3,5]＋提早 60 日）');
_date337 = new Date(1992, 2, 15);
ok('(2) window_open', gigSeasonEarlyVisible88(f207) === true, '1992-03-15 可見');
_date337 = new Date(1992, 5, 15);
ok('(2) window_past', gigSeasonEarlyVisible88(f207) === false, '1992-06-15 已過季尾（05-31）唔見');
_date337 = new Date(1991, 6, 15);
ok('(2) f212_window_1991_summer', gigSeasonEarlyVisible88(f212) === true && gigSeasonEarlyVisible88(f207) === false, '1991-07-15：film_212 可見、film_207 未入窗（唔互相污染）');

// ---------- (3) 雙 gig 同一筆債權：殺青邊張，另一張自動落板 ----------
resetS337();
S.mockCredits = [Object.assign({}, NGAI_CREDIT)];
br89OnGigComplete('gig_1991_film_212');
ok('(3) redeem_212_closes_207', S.mockCredits[0].redeemedBy === 'gig_1991_film_212' && br89GigOn({ id: 'gig_1992_film_207' }) === false && br89GigOn({ id: 'gig_1991_film_212' }) === false && triggerGigOn(f207) === false, '殺青《鐵橋風雲》：新張自動落板');
resetS337();
S.mockCredits = [Object.assign({}, NGAI_CREDIT)];
br89OnGigComplete('gig_1992_film_207');
ok('(3) redeem_207_closes_212', S.mockCredits[0].redeemedBy === 'gig_1992_film_207' && S.mockCredits[0].line.indexOf('已兌現') >= 0 && S.mockCredits[0].line.indexOf('虎嘯龍吟') >= 0 && br89GigOn({ id: 'gig_1991_film_212' }) === false && triggerGigOn(f212) === false, '殺青《虎嘯龍吟》：舊張自動落板＋債權 line 更新');
resetS337();
S.mockCredits = [Object.assign({}, NGAI_CREDIT)];
genericCreditOnGigComplete283('gig_1992_film_207');
ok('(3) generic283_skips_br89', !S.mockCredits[0].redeemedBy, 'BR89 gig 行 br89OnGigComplete，generic283 跳過唔重複標');
resetS337();
S.mockCredits = [Object.assign({}, NGAI_CREDIT)];
const ngaiLine = creditRedeemLine283({ id: 'credit_enc83_ngai_patron' });
ok('(3) H_shows_both_titles', ngaiLine.indexOf('可以換：') >= 0 && ngaiLine.indexOf('鐵橋風雲') >= 0 && ngaiLine.indexOf('虎嘯龍吟') >= 0, '人情卡「可以換」出齊兩張名（BR89 反查自動）');

// ---------- (4) GRANT229 魏行唔郁 ----------
resetS337();
ok('(4) grant229_lie_still_film114', grant229RecordFromEnc79('beat:ngai_patron', '講大話') === true && S.grant229Queue.length === 1 && S.grant229Queue[0].gigId === 'gig_1991_film_114', 'patron「講大話」照派 film_114《刀光劍影錄》動作替身（唔郁）');
resetS337();
ok('(4) grant229_no_207_row', GRANT229_ENC79.every(r=>r.gigId !== 'gig_1992_film_207'), 'film_207 唔係即派 gig，淨係 credit trigger 路徑');

// ---------- (5) 舊檔唔 crash ----------
resetS337();
S.mockCredits = [];
let threw337 = false;
try{ triggerGigOn(f207); br89GigOn({ id: 'gig_1992_film_207' }); }catch(e){ threw337 = true; }
ok('(5) old_save_no_credit_no_throw', !threw337 && triggerGigOn(f207) === false, '無債權舊檔唔掟錯');
resetS337();
delete S.mockCredits;
threw337 = false;
try{ triggerGigOn(f207); br89GigOn({ id: 'gig_1992_film_207' }); }catch(e){ threw337 = true; }
ok('(5) old_save_no_mockCredits_no_throw', !threw337 && triggerGigOn(f207) === false, '無 mockCredits 舊檔唔掟錯');
resetS337();
S.mockCredits = [Object.assign({}, NGAI_CREDIT, { status: '絕響' })];
ok('(5) expired_credit_not_on', triggerGigOn(f207) === false, '絕響債權唔開');

console.log(fails.length === 0 ? 'ALL PASS' : 'FAILURES: ' + fails.join(', '));
process.exit(fails.length === 0 ? 0 : 1);
