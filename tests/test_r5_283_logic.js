// v20a283 R5 人情兌現票（A＋H）：A 通用 credit-trigger 通告殺青標 redeemedBy；
//   H 人情頁債權卡加「可以換：」一行。
// 用法：node tests/test_r5_283_logic.js [path-to-index.html]
// 核心結論：
//   A——殺青鉤加通用分支 genericCreditOnGigComplete283，讀 gig.trigger.creditId 標記，
//     模式照抄 br89OnGigComplete；BR89 14 張留返 br89 標，唔補入 BR89 map；
//     film_202 雖有 trigger.creditId 但喺 BR89 map 入面，通用分支跳過，唔重複標。
//   H——creditRedeemLine283：BR89 14 張由 BR89_PATRON_OF_GIG 反查＋通用 9 張由
//     CREDIT_REDEEM_GIG283 對照＋v158 兩條渠道寫類別名；只喺未兌現嗰陣出。
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

// ---------- 沙盒：先設 var，再 eval 真 code（沿用 v282 模式） ----------
const gigsPack = JSON.parse(fs.readFileSync(path.join(root, 'content/gigs_new.json'), 'utf8'));
const allGigs = gigsPack.gigs;
const gigById = {};
allGigs.forEach(g=>{ if(g && g.id) gigById[g.id] = g; });
const byYear = { 1990: [], 1991: [], 1992: [] };
allGigs.forEach(g=>{ if(g && byYear[Number(g.year)]) byYear[Number(g.year)].push(g); });
var GIGS = allGigs.map(g=>({ id: g.id, title: g.title, trigger: g.trigger }));
var STORY_WIRE = { gigsByYear: { 1990: { gigs: byYear[1990] }, 1991: { gigs: byYear[1991] }, 1992: { gigs: byYear[1992] } } };
var BR89_PATRON_OF_GIG = eval('(' + extractObjLiteral('const BR89_PATRON_OF_GIG = {') + ')');
var CREDIT_REDEEM_GIG283 = eval('(' + extractObjLiteral('const CREDIT_REDEEM_GIG283 = {') + ')');
var CREDIT_REDEEM_TEXT283 = eval('(' + extractObjLiteral('const CREDIT_REDEEM_TEXT283 = {') + ')');
var S = { mockCredits: [] };
var mirrorCalls = 0;
function journalText(s){ return String(s == null ? '' : s); }
function syncNotebookMirror(){ mirrorCalls++; }
eval(extractFn('gigRecordById283'));
eval(extractFn('gigTitleById283'));
eval(extractFn('genericCreditOnGigComplete283'));
eval(extractFn('creditRedeemLine283'));
eval(extractFn('favorCreditCountsAsHeld'));

// ---------- (0) 靜態結構 ----------
const br89CallIdx = html.indexOf('br89OnGigComplete(sh.gigId)');
const genCallIdx = html.indexOf('genericCreditOnGigComplete283(sh.gigId)');
ok('(0) hook_br89_call_in_place', br89CallIdx > 0, '殺青鉤仍有 br89 呼叫');
ok('(0) hook_generic_call_after_br89', genCallIdx > br89CallIdx && (genCallIdx - br89CallIdx) < 500, '通用分支呼叫喺 br89 之後（相鄰兩行）');
ok('(0) br89_map_still_14_pairs', Object.keys(BR89_PATRON_OF_GIG).length === 14, 'BR89 map 維持 14 對，無補入通用 9 張');
const nineGigs = ['gig_1991_tv_204','gig_1991_film_108','gig_1992_film_203','gig_1991_film_112','gig_1992_tv_106','gig_1991_tv_106','gig_1992_tv_201','gig_1992_film_101','gig_1991_film_109'];
ok('(0) nine_not_in_br89_map', nineGigs.every(g=>!(g in BR89_PATRON_OF_GIG)), '通用 9 張無一喺 BR89 map 入面');
ok('(0) redeem_gig_map_9_entries', Object.keys(CREDIT_REDEEM_GIG283).length === 9, 'CREDIT_REDEEM_GIG283 9 個對照');
ok('(0) redeem_text_map_2_entries', Object.keys(CREDIT_REDEEM_TEXT283).length === 2, 'CREDIT_REDEEM_TEXT283 2 條渠道');
ok('(0) credit_card_calls_redeem_line', html.includes('creditRedeemLine283(c)'), 'creditCardHtml 呼叫 creditRedeemLine283(c)');
ok('(0) credit_trigger_gigs_still_23', allGigs.filter(g=>g.trigger && g.trigger.kind === 'credit').length === 23, '通告庫 kind:credit 仍係 23 張（14 BR89＋9 通用），無刪通告');

// ---------- (1) A：通用 9 張逐張殺青標記 ----------
const nine = [
  ['gig_1991_tv_204', 'credit_c7_rain', '通宵追捕'],
  ['gig_1991_film_108', 'credit_c9_crew', '月夜酒廊'],
  ['gig_1992_film_203', 'credit_c15_stunt', '江湖復仇'],
  ['gig_1991_film_112', 'credit_wf3_lu_team', '夜半無人聲'],
  ['gig_1992_tv_106', 'credit_wf3_yip_manager', '冬日情書'],
  ['gig_1991_tv_106', 'credit_enc79_yip_manager', '鬼馬經理人'],
  ['gig_1992_tv_201', 'credit_fen_rescue', '芬姐茶檔'],
  ['gig_1992_film_101', 'credit_enc83_ngai_meal', '武館風波'],
  ['gig_1991_film_109', 'credit_enc83_liu_patron', '笑聲震天響'],
];
nine.forEach(([gid, cid, titlePart])=>{
  S = { mockCredits: [{ id: cid, debtor: 'test', title: 'test', line: '原句。' }] };
  mirrorCalls = 0;
  ok('(1) A_mark_' + gid + '_redeemedBy', (genericCreditOnGigComplete283(gid), S.mockCredits[0].redeemedBy === gid), cid + ' → redeemedBy=' + gid);
  ok('(1) A_mark_' + gid + '_line', S.mockCredits[0].line.includes('已兌現') && S.mockCredits[0].line.includes(titlePart), 'line 寫「已兌現：' + titlePart + '…"');
  ok('(1) A_mark_' + gid + '_held_false', favorCreditCountsAsHeld(S.mockCredits[0]) === false, '標記後 favorCreditCountsAsHeld 返 false，creditsHeld 唔再計');
  ok('(1) A_mark_' + gid + '_mirror', mirrorCalls === 1, 'syncNotebookMirror 行一次');
});
// 冪等：再標一次，唔重複加「已兌現」句
S = { mockCredits: [{ id: 'credit_c7_rain', debtor: 'test', title: 'test', line: '原句。' }] };
genericCreditOnGigComplete283('gig_1991_tv_204');
genericCreditOnGigComplete283('gig_1991_tv_204');
ok('(1) A_idempotent', (S.mockCredits[0].line.match(/已兌現/g) || []).length === 1, '重複殺青唔重複加句');
// BR89 嗰張唔經通用分支：film_202（BR89 第 14 對）＋film_101（BR89）
S = { mockCredits: [
  { id: 'credit_wf3_comedy_crew', debtor: '廖炳星', title: 't', line: '原句。' },
  { id: 'credit_enc83_luk_patron', debtor: '陸柏言', title: 't', line: '原句。' },
] };
genericCreditOnGigComplete283('gig_1992_film_202');
genericCreditOnGigComplete283('gig_1991_film_101');
ok('(1) A_br89_film202_skipped', S.mockCredits[0].redeemedBy === undefined, 'film_202 留返 br89 標，通用分支唔郁佢');
ok('(1) A_br89_film101_skipped', S.mockCredits[1].redeemedBy === undefined, 'film_101 留返 br89 標，通用分支唔郁佢');
// 無 trigger／唔識嘅 gig／空 S：唔掟錯，唔標記
S = { mockCredits: [{ id: 'credit_c7_rain', debtor: 'test', title: 'test', line: '原句。' }] };
let threw = false;
try{
  genericCreditOnGigComplete283('gig_1990_film_206'); // 普通板通告，無 trigger
  genericCreditOnGigComplete283('gig_no_such_id');
  genericCreditOnGigComplete283(null);
  genericCreditOnGigComplete283(undefined);
}catch(e){ threw = true; }
ok('(1) A_no_trigger_no_throw', !threw && S.mockCredits[0].redeemedBy === undefined, '普通通告／未知 id／null 唔掟錯亦唔標記');
// 跨年兜底：GIGS 只得 1992 年，1991 年通告照標（經 gigsByYear 反查）
GIGS = byYear[1992].map(g=>({ id: g.id, title: g.title, trigger: g.trigger }));
S = { mockCredits: [{ id: 'credit_c7_rain', debtor: 'test', title: 'test', line: '原句。' }] };
genericCreditOnGigComplete283('gig_1991_tv_204');
ok('(1) A_cross_year_mark', S.mockCredits[0].redeemedBy === 'gig_1991_tv_204', 'GIGS 無 1991 年嗰陣，經 gigsByYear 照標');
ok('(1) A_cross_year_title', S.mockCredits[0].line.includes('通宵追捕'), '跨年 line 仍然搵到通告名，唔跌返 gig id');
GIGS = allGigs.map(g=>({ id: g.id, title: g.title, trigger: g.trigger }));
// film_109 雙 gig 清口：廖引薦債權經 film_109 兌現
S = { mockCredits: [{ id: 'credit_enc83_liu_patron', debtor: '廖炳星', title: 't', line: '原句。' }] };
genericCreditOnGigComplete283('gig_1991_film_109');
ok('(1) A_liu_dual_film109_marks', S.mockCredits[0].redeemedBy === 'gig_1991_film_109', '廖引薦雙 gig 缺口清零：film_109 殺青標到 credit_enc83_liu_patron');

// ---------- (2) H：逐卡「可以換」 ----------
const br89Expect = [
  ['credit_enc83_luk_patron', '江河歲月'],
  ['credit_enc84_pang_patron', '台慶大騷'],
  ['credit_enc84_ching_patron', '夜場匯演'],
  ['credit_enc79_liu_priority', '笑住過肥年'],
  ['credit_enc83_liu_patron', '吉星笑哈哈'],
  ['credit_enc83_mak_patron', '武館群英'],
  ['credit_enc83_yip_patron', '摩登一家人'],
  ['credit_enc83_gu_patron', '夜總會登台暖場'],
  ['credit_enc84_so_patron', '秀髮如瀑'],
  ['credit_enc84_chung_patron', '秋日絮語'],
  ['credit_enc83_lok_patron', '主打歌'],
  ['credit_enc83_ngai_patron', '鐵橋風雲'],
  ['credit_enc83_chai_patron', '油麻地夜班'],
  ['credit_wf3_comedy_crew', '笑到最後'],
];
br89Expect.forEach(([cid, titlePart])=>{
  const line = creditRedeemLine283({ id: cid });
  ok('(2) H_br89_' + cid, line.includes('可以換：') && line.includes(titlePart), cid + ' → 可以換：…' + titlePart + '…');
});
nine.forEach(([gid, cid, titlePart])=>{
  const line = creditRedeemLine283({ id: cid });
  ok('(2) H_generic_' + cid, line.includes('可以換：') && line.includes(titlePart), cid + ' → 可以換：…' + titlePart + '…');
});
ok('(2) H_liu_dual_both_titles', creditRedeemLine283({ id: 'credit_enc83_liu_patron' }).includes('吉星笑哈哈') && creditRedeemLine283({ id: 'credit_enc83_liu_patron' }).includes('笑聲震天響'), '廖引薦雙 gig 兩張名一併出');
ok('(2) H_v158_mak', creditRedeemLine283({ id: 'credit_enc79_mak_wuzhi' }).includes('可以換：武打通告免試鏡'), '武指照應 → 可以換：武打通告免試鏡');
ok('(2) H_v158_pang', creditRedeemLine283({ id: 'credit_enc84_pang_charity' }).includes('可以換：司儀通告免試鏡'), '慈善騷頂班 → 可以換：司儀通告免試鏡');
ok('(2) H_no_redeem_empty', creditRedeemLine283({ id: 'credit_no_such' }) === '', '無兌現通告嘅債權唔出「可以換」行');
ok('(2) H_cafe_empty', creditRedeemLine283({ id: 'credit_enc79_cafe_help_01' }) === '', '茶餐廳幫手債權唔出「可以換」行');
ok('(2) H_redeemed_empty', creditRedeemLine283({ id: 'credit_c7_rain', redeemedBy: 'gig_1991_tv_204' }) === '', '已兌現卡唔再出「可以換」行（c.line 已有已兌現句）');
ok('(2) H_null_empty', creditRedeemLine283(null) === '', 'null 債權返空字串，唔掟錯');
// 跨年：GIGS 只得 1992 年，1991 年債權卡照出名
GIGS = byYear[1992].map(g=>({ id: g.id, title: g.title, trigger: g.trigger }));
ok('(2) H_cross_year_title', creditRedeemLine283({ id: 'credit_c7_rain' }).includes('通宵追捕'), 'GIGS 無 1991 年嗰陣，經 gigsByYear 照出《通宵追捕》');
GIGS = allGigs.map(g=>({ id: g.id, title: g.title, trigger: g.trigger }));

console.log(fails.length === 0 ? 'ALL PASS' : 'FAILURES: ' + fails.join(', '));
process.exit(fails.length === 0 ? 0 : 1);
