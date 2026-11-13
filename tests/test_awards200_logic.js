// v20a200 修 v194 設計 review C1＋C2・邏輯測試：
// C1：gap 句加「今年」——邀請函閘句（awards62GateLineHtml）＋季前提示（awards62SeasonHints）
//     兩邊一齊加，講法一致；計數規則本身唔郁（按屆計，跨年作品唔計；gapWorks＝wrapMin－wraps）。
// C2：旁聽請柬 rep 行改寫法——gallery 嗰陣「你今年憑《X》入場觀禮。」（唔再話爭獎），
//     海報＋同屆提名照留；nominee／won 照舊「爭獎」；fallback 行同樣分流，唔會兜返舊寫法。
// v192 殘留（對過）：nominee 請柬「今晚獎項」行淨列你爭嗰 1–2 格——改標籤唔改 slate，
//     變「你爭嘅獎項：…」；gallery 嗰邊 v192 C4 全 slate＋（觀禮）唔郁。
// 反證：對 pristine main a1a6681 index 行 → v200 文案未入 → FAIL（唔 crash）。
// 用法：node tests/test_awards200_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
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
  let depth = 0, started = false;
  for(let k = i; k < html.length; k++){
    const ch = html[k];
    if(ch === '{' || ch === '['){ depth++; started = true; }
    else if(ch === '}' || ch === ']'){ depth--; if(started && depth === 0) return html.slice(i, k + 1) + ';'; }
    else if(ch === ';' && !started) return html.slice(i, k + 1);
  }
  throw new Error('const end not found: ' + name);
}

/* 反證守衛：v200 嘢唔存在嗰陣乾淨 FAIL（逐項列出），唔好等 extraction 喺頂層 throw 崩潰。 */
const NEED200 = ['今年仲差 ', '入場觀禮', '你爭嘅獎項'];
let missing200 = NEED200.filter(s => html.indexOf(s) < 0);
if(missing200.length){
  missing200.forEach(m=>{ fails.push('反證：' + m + ' 唔存在'); console.log('FAIL 反證：' + m + ' 唔存在（pristine main 預期，v200 未入）'); });
  console.log('\nFAILED: ' + fails.length);
  process.exit(1);
}

eval(extractConst('AWARDS62_MEDIUM_LABEL').replace('const AWARDS62_MEDIUM_LABEL =', 'var AWARDS62_MEDIUM_LABEL ='));
eval(extractFn('awards62GateLineHtml'));
function count(hay, needle){ return hay.split(needle).length - 1; }

/* ---- C1：邀請函閘句 ---- */
function gapPack(medium, wraps, wrapMin, dualOk){
  return { medium: medium, standing62: { tier: 'gallery', wraps: wraps, wrapMin: wrapMin,
    dualOk: dualOk, gapWorks: Math.max(0, wrapMin - wraps), gapWin: 0, repTitle: '' } };
}
/* v194 C1 原案：上一年做過 2 部廣告、呢屆 0 部 → 邀請函話 0/1 */
const gapAd = awards62GateLineHtml(gapPack('ad', 0, 1, true));
ok('C1：邀請函 gap 句有「今年」（廣告 0/1 原案逐字）',
  gapAd.indexOf('今晚席位：觀禮。今年仲差 1 部廣告作品先夠入圍（而家 0/1）。') >= 0);
ok('C1：邀請函 gap 句唔再係無年份嘅舊寫法',
  gapAd.indexOf('觀禮。仲差 1 部') < 0);
const gapFilm = awards62GateLineHtml(gapPack('film', 1, 2, true));
ok('C1：電影版 gap 句同樣有「今年」（1/2）',
  gapFilm.indexOf('今年仲差 1 部電影作品先夠入圍（而家 1/2）') >= 0);
/* 計數口徑唔郁：同年夠數嗰陣唔出 gap 句，跌返角色閘句 */
const noGap = awards62GateLineHtml(gapPack('film', 2, 2, true));
ok('C1：夠數嗰陣唔出 gap 句（角色閘句照出，計數唔郁）',
  noGap.indexOf('仲差') < 0 && noGap.indexOf('嗰年未做過主角／配角級作品，入圍唔到演員獎') >= 0);
/* nominee 分支唔郁 */
const gateNom = awards62GateLineHtml({ medium: 'film',
  standing62: { tier: 'nominee', wraps: 3, wrapMin: 2, dualOk: true, gapWorks: 0, gapWin: 0, repTitle: '新春大吉' } });
ok('C1：nominee 分支唔郁（嗰年 3 部＋憑《新春大吉》爭獎）',
  gateNom.indexOf('入圍門檻已達標：嗰年 3 部電影作品，憑《新春大吉》爭獎。') >= 0);

/* ---- C1：季前提示（真執行 awards62SeasonHints，stub 季度／旗標／standing） ---- */
var START = { y: 1991 };
var calendarSeason = function(){ return '春'; };
var awardsCalendarYear = function(){ return 1991; };
var awardsEditionYear = function(cer){ return 1991; };
var awardsGetFlag = function(){ return ''; };
var awardsCopyLine = function(s, fb){ return s || fb || ''; };
var awardsStubCeremony = function(){ return null; };
var awardsCeremonies = function(){
  return [{ id: 'award_harbour_ad', season: '春', medium: 'ad', displayName: '維港街招・年度廣告賞' }];
};
var awards62Standing = function(cer, y){
  return { tier: 'gallery', wraps: 0, wrapMin: 1, dualOk: true, gapWorks: 1, gapWin: 0, repTitle: '' };
};
eval(extractFn('awards62SeasonHints'));
const hintAd = awards62SeasonHints({}, 0) || '';
ok('C1：季前提示 gap 句有「今年」，同邀請函講法一致',
  hintAd.indexOf('今季就係「維港街招・年度廣告賞」：今年仲差 1 部廣告作品先夠入圍——呢排接廣告通告要留神。') >= 0);

/* ---- C2：rep 行分流 ---- */
var poster59Path = function(){ return ''; };
var awards63FocusFellows = function(){ return []; };
eval(extractFn('awards63InviteBitHtml'));
const repGal = awards63InviteBitHtml({ tier: 'gallery', repWork62: '過江龍', repGigId63: '' });
ok('C2：gallery rep 行改「入場觀禮」，唔再話爭獎',
  repGal.indexOf('你今年憑《過江龍》入場觀禮。') >= 0 && repGal.indexOf('爭獎') < 0);
const repNom = awards63InviteBitHtml({ tier: 'nominee', repWork62: '新春大吉', repGigId63: '' });
ok('C2：nominee rep 行照舊「爭獎」',
  repNom.indexOf('你今年憑《新春大吉》爭獎。') >= 0);
ok('C2：冇代表作嗰陣唔出 rep 行',
  awards63InviteBitHtml({ tier: 'gallery', repWork62: '' }) === '');

/* ---- C2＋殘留：成張請柬 ---- */
eval(extractConst('AWARDS188_CATEGORIES').replace('const AWARDS188_CATEGORIES =', 'var AWARDS188_CATEGORIES ='));
eval(extractFn('awardsCatsSorted184'));
eval(extractFn('renderAwardInviteHtml'));
function invPack(cats, tier, ceremonyId, repWork){
  return { ceremonyId: ceremonyId || 'award_harbour_film', tier: tier, medium: 'film',
    tierLabel: tier === 'gallery' ? '旁聽席' : '入圍／提名',
    displayName: '維港影藝獎', season: '秋', year: 1990, venue99: '金禧大酒店',
    inviteTitle: '維港影藝獎請柬', inviteDek: '你收到一封頒獎禮嘅請柬。', categories: cats,
    repWork62: repWork || '', repGigId63: '',
    standing62: { tier: tier, wraps: 0, wrapMin: 1, dualOk: true, gapWorks: 1, gapWin: 0, repTitle: '' } };
}
const galInvite = renderAwardInviteHtml(invPack(
  [{ id: 'cat_film_support_m', label: '最佳男配角' }, { id: 'cat_film_lead_m', label: '最佳男主角' }],
  'gallery', 'award_harbour_film', '過江龍'));
ok('C2：成張 gallery 請柬零「爭獎」（rep 行＋閘句＋其他行都唔講爭獎）',
  galInvite.indexOf('爭獎') < 0);
ok('C2：成張 gallery 請柬有「入場觀禮」',
  galInvite.indexOf('你今年憑《過江龍》入場觀禮。') >= 0);
ok('C2：gallery 請柬 gap 句有「今年」',
  galInvite.indexOf('今年仲差 1 部電影作品先夠入圍（而家 0/1）') >= 0);
ok('C2：gallery 請柬席位＋全 slate＋（觀禮）唔郁',
  galInvite.indexOf('席位：旁聽席') >= 0 &&
  galInvite.indexOf('今晚獎項：最佳男主角、最佳女主角、最佳男配角、最佳女配角（觀禮）') >= 0);
const nomInvite = renderAwardInviteHtml(invPack(
  [{ id: 'cat_film_support_m', label: '最佳男配角' }, { id: 'cat_film_lead_m', label: '最佳男主角' }],
  'nominee', 'award_harbour_film', '新春大吉'));
ok('C2：nominee 請柬 rep 行照舊「爭獎」',
  nomInvite.indexOf('你今年憑《新春大吉》爭獎。') >= 0);
/* v192 殘留：nominee 行改標籤唔改 slate */
ok('殘留：nominee 請柬「今晚獎項」改做「你爭嘅獎項」，slate 照列你爭嗰 2 格',
  nomInvite.indexOf('你爭嘅獎項：最佳男主角、最佳男配角</p>') >= 0 &&
  nomInvite.indexOf('今晚獎項') < 0 && nomInvite.indexOf('（觀禮）') < 0);
ok('殘留：gallery 請柬仲係「今晚獎項」＋（觀禮）（v192 C4 唔郁）',
  galInvite.indexOf('今晚獎項：最佳男主角、最佳女主角、最佳男配角、最佳女配角（觀禮）') >= 0);

console.log(fails.length ? ('\nFAILED: ' + fails.length + ' -> ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
