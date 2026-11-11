// v20a100 CLEAN100 邏輯測試（二）：巧遇／結局／醫院／通告——抽真函數行真場景：
//   (1) B-04：真 enc79BuildScript——鍾楚凝 1990 年（day 100）fav 50：heart 唔播、
//       opener 封頂 T2；1991 年（day 400）：heart 照播；
//   (2) B-06：真 enc79BuildScript——顧明輝 gu_n10after 開場按 C9 三路旗分版
//       （standup／mediate／chase 原句／無旗中性）；
//   (3) B-05/B-07/B-08/B-09：真結局呈現函數——去留段鍾楚凝回收（要有 farewell 旗）、
//       GH 三路歸因、E5 新句、曉晴 commit 按 awardsLog 分版；
//   (4) B-10：真 hosp96VisitNote——冇熟人時出珍姐糖水句、冇芬姐字眼；
//   (5) A-07：真 normalizeGigRecord＋gigReleaseLine88——迎春夜入 label、
//       真・春季通告冇 label 照衍生「春季」、迎春夜冇 label 時（對照）先係春季。
// 反證：喺 v20a99 index 上行 → 多項 FAIL（chungPre91／beatSeg100／ghOrigin100 等不存在）。
// 用法：node tests/test_cleanup100_enc.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const rootDir = path.dirname(htmlPath);
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
    else if(c === ';' && !started){ j++; break; }
  }
  return html.slice(i, j);
}
/* ---- sandbox ---- */
const START = { y: 1990, m: 1, d: 1 };
let S = null;
let GIGS = [];
function freshS(day){ return { dayIndex: day, flags: {}, story: { flags: {}, done: {}, rel: {} }, stars: {}, npcs: {}, awardsLog: [], mockRumors: [], mockCredits: [], starWhispers: {} }; }
function br89HoldsCard(){ return false; }
function boardNotePlayerOk(){ return true; }
function extractAssign(lhs){
  const i = html.indexOf(lhs + ' =');
  if(i < 0) throw new Error('assign not found: ' + lhs);
  let depth = 0, started = false, j = i;
  for(; j < html.length; j++){
    const c = html[j];
    if(c === '{' || c === '['){ depth++; started = true; }
    else if(c === '}' || c === ']'){ depth--; if(started && depth === 0){ j++; break; } }
  }
  return html.slice(i, j) + ';';
}
function enc79GrantWhisper(){}
function enc79GrantRumorCard(){}
function enc79GrantCredit(){}
function bumpNpc(){}
function conseq61State(){ return { sick: {} }; }
function looksLikeEraId(){ return false; }
function humanizeEraId(x){ return x; }
eval([
  extractFn('dateObj'), extractFn('calendarSeason'), extractFn('yearSeasonNow'),
  extractFn('enc83Flag'), extractFn('enc83NodeDone'), extractFn('enc87StoryFlag'),
  extractConst('ENC79_PLAYER_TIERS'), extractConst('ENC79_STARS'), extractConst('ENC79_BEATS'),
  extractAssign('ENC79_BEATS.gu_mingfai'), extractAssign('ENC79_BEATS.chung_choning'),
  extractConst('ENC84_DLG_chung_choning'), extractConst('ENC83_DLG_gu_mingfai'),
  extractFn('enc79EnsureStars'), extractFn('enc79StarState'), extractFn('enc79TierOf'),
  extractFn('enc79PlayerTier'), extractFn('enc79StarDef'), extractFn('enc79BeatOpen'),
  extractFn('enc79PickBeat'), extractFn('enc79NormSeg'), extractFn('enc79Rand'), extractFn('enc79Hash'),
  extractFn('enc79LocName'), extractFn('enc79AddFav'),
  extractConst('ENC79_FIRST_ALT98'), extractFn('contra98EncFirstLocSwap'),
  extractFn('enc79BuildScript'),
  extractFn('endingFlag410'), extractFn('end95StoryDone'), extractFn('end95Awards'),
  extractFn('endingCareerScene410'), extractFn('endingRomanceScene410'), extractFn('endingExodusScene410'),
  extractFn('hosp96VisitNote'),
  extractConst('GIG_SEASON_SPAN88'), extractConst('CLEAN100_GIG_RELEASE'),
  extractFn('gigReleaseLine88'), extractFn('normalizeGigRecord'),
  'globalThis.__E = { enc79BuildScript, endingCareerScene410, endingRomanceScene410, endingExodusScene410, hosp96VisitNote, gigReleaseLine88, normalizeGigRecord, ENC79_DIALOG: { chung_choning: ENC84_DLG_chung_choning, gu_mingfai: ENC83_DLG_gu_mingfai }, ENC79_STAGEUP: {}, ENC79_CAP_LINES: {}, ENC79_WRAP_ECHO: {} };',
].join('\n'));
const E = globalThis.__E;
/* buildScript 參照嘅全域（eval 作用域內補齊） */
eval('var ENC79_DIALOG = globalThis.__E.ENC79_DIALOG, ENC79_STAGEUP = {}, ENC79_CAP_LINES = {}, ENC79_WRAP_ECHO = {};');
function stepsText(sc){ return (sc && sc.steps || []).map(s => s.text).join('\n'); }

/* (1) B-04 */
const CHUNG_DONE = { chung_review: 1, chung_intel: 1, chung_f_clue: 1, chung_patron: 1 };
S = freshS(100);
S.stars.chung_choning = { fav: 50, met: true, stage: 99, heartDone: false, beatsDone: Object.assign({}, CHUNG_DONE), poolSeen: {} };
let t = stepsText(E.enc79BuildScript('chung_choning'));
ok('B04 1990 heart 唔播', t.indexOf('去加拿大嗰邊住一排') < 0);
ok('B04 1990 opener T2', t.indexOf('邊套戲先算真演技') >= 0);
S = freshS(400);
S.stars.chung_choning = { fav: 50, met: true, stage: 99, heartDone: false, beatsDone: Object.assign({}, CHUNG_DONE), poolSeen: {} };
t = stepsText(E.enc79BuildScript('chung_choning'));
ok('B04 1991 heart 照播', t.indexOf('去加拿大嗰邊住一排') >= 0);

/* (2) B-06 */
function guRun(){
  S.stars.gu_mingfai = { fav: 30, met: true, stage: 99, heartDone: true, beatsDone: {}, poolSeen: {} };
  return stepsText(E.enc79BuildScript('gu_mingfai'));
}
S = freshS(100); S.flags.done_C9 = 1;
S.flags.flag_standup_crew = 1;
ok('B06 standup 版開場', guRun().indexOf('你企出嚟幫成組人出聲之後') >= 0);
S = freshS(100); S.flags.done_C9 = 1; S.flags.flag_mediate_gu_debt = 1;
ok('B06 mediate 版開場', guRun().indexOf('幫顧明輝同何生爭取到分期之後') >= 0);
S = freshS(100); S.flags.done_C9 = 1; S.flags.flag_chase_for_ho = 1;
ok('B06 chase 版原句', guRun().indexOf('追數嗰場風波過咗之後') >= 0);
S = freshS(100); S.flags.done_C9 = 1;
ok('B06 無旗中性版', guRun().indexOf('嗰排台慶前後嘅事過咗之後') >= 0);

/* (3) 結局呈現 */
S = freshS(1090);
S.stars.chung_choning = { beatsDone: { chung_farewell: 1000 } };
ok('B05 去留回收鍾楚凝', E.endingExodusScene410({ exodus: 'stay' }, { exodusNames: [] }).indexOf('鍾楚凝嗰班機') >= 0);
S.stars.chung_choning = { beatsDone: {} };
ok('B05 冇farewell冇回收', E.endingExodusScene410({ exodus: 'stay' }, { exodusNames: [] }).indexOf('鍾楚凝嗰班機') < 0);
S = freshS(1090);
S.stars.pang_siuki = { fav: 60 };
let gh = E.endingCareerScene410({ career: 'GH' });
ok('B07 GH 好感路點醒版', gh.indexOf('點醒你') >= 0 && gh.indexOf('慈善騷') < 0);
S.flags.done_C10 = 1;
gh = E.endingCareerScene410({ career: 'GH' });
ok('B07 GH C10路慈善騷版', gh.indexOf('慈善騷嗰晚開始') >= 0);
S = freshS(1090); S.stars.pang_siuki = { fav: 10 };
gh = E.endingCareerScene410({ career: 'GH' });
ok('B07 GH 提攜路版', gh.indexOf('彭少祺留低嗰份提攜') >= 0);
const e5 = E.endingCareerScene410({ career: 'E5' });
ok('B09 E5 新句冇虛構', e5.indexOf('嗰種光，你認得') >= 0 && e5.indexOf('攞咗新人獎') < 0);
S = freshS(1090); S.awardsLog = [];
let hiu = E.endingRomanceScene410({ career: 'E2', romance: { line: 'hiu', kind: 'commit' } });
ok('B08 曉晴冇win冇獎座', hiu.indexOf('獎座') < 0 && hiu.indexOf('一個攞獎') < 0);
S.awardsLog = [{ categories: [{ outcome: 'won' }] }];
hiu = E.endingRomanceScene410({ career: 'E1', romance: { line: 'hiu', kind: 'commit' } });
ok('B08 曉晴有win獎座版', hiu.indexOf('獎座') >= 0);

/* (4) B-10 醫院 */
S = freshS(50); S.npcs = {};
const note = E.hosp96VisitNote(1);
ok('B10 探病珍姐句', !!note && note.indexOf('茶水檔珍姐') >= 0 && note.indexOf('芬姐') < 0);

/* (5) A-07 */
const gigsPack = JSON.parse(fs.readFileSync(path.join(rootDir, 'content', 'gigs_1988.json'), 'utf8'));
const gigArr = Array.isArray(gigsPack) ? gigsPack : gigsPack.gigs;
const springGigRaw = JSON.parse(JSON.stringify(gigArr.find(g => g.id === 'gig_1988_tvb_longmen_spring_high')));
const springGig = E.normalizeGigRecord(springGigRaw);
ok('A07 迎春夜 normalize 後有 label', springGig.releaseLabel === '預計播出：1990 年農曆新年特輯');
ok('A07 迎春夜播出線係新年特輯', E.gigReleaseLine88(springGig) === '預計播出：1990 年農曆新年特輯');
ok('A07 對照：冇label時衍生春季（證明label先係修復）', E.gigReleaseLine88(springGigRaw) === '預計播出：1988 年春季');
const otherSpring = gigArr.find(g => g.id !== 'gig_1988_tvb_longmen_spring_high' && g.season === '春');
if(otherSpring){
  const oc = E.normalizeGigRecord(JSON.parse(JSON.stringify(otherSpring)));
  ok('A07 其他春季通告冇label冇誤傷', !oc.releaseLabel && E.gigReleaseLine88(oc).indexOf('春季') >= 0);
} else {
  ok('A07 其他春季通告冇label冇誤傷', false);
}

console.log(fails.length ? ('FAILURES: ' + fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
