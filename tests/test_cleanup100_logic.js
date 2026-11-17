// v20a100 CLEAN100 邏輯測試：矛盾審計清理包——
//   (1) A-04：CLEAN100_WHEN_FIX 經 contra98FixNodeWhen＋真 years66Walk 後，
//       N2／N3 頁首（真 spPlayerMeta）＝「主線 · 1990冬」；N1 不受影響；
//   (2) A-05/A-06：spPlayerMeta 對 N5／A-06 五節點用當下曆法（day 0→1990冬、day 75→1990春、
//       R_xu_meet day 800→1992春）；一般節點唔受影響（用返 eraTag 路徑）；
//   (3) A-12：JSON pack 嘅 N18/N19 pacing.weekMin＝48／61，經 walk＋
//       storyWeekStamp 出「第 48 週／第 61 週」；其他 WF1 節點 weekMin 原封；
//   (4) B-03：content/story_detail_romance_lan_xu.json R_lan_push1 冇 stats.music、主抉擇 stage:1；
//       flag_family_marriage 兩抉擇保留（唔拆旗決定）＋flags_written 不變；
//       （v20a242：ROMANCE_LAN_PA_OVERRIDES 已刪，JSON 唯一來源；stage 修正已入 JSON）
//   (5) A-08：真 news82Tick——day 1015 未做 N15 → E4 唔刊；做完 N15 → 照刊；
//       舊檔 ensureNews82 唔好搶先歸檔 E4；其他事件（E5 day 532）照常；
//   (6) B-05：真 enc79PresenceP——鍾楚凝 farewell 未播 1992秋 p=0.25、播完 p=0；
//       其他星唔受影響；
//   (7) A-07：真 gigReleaseLine88——有 releaseLabel 用 label（新年特輯）；
//       真・春季通告冇 label 照衍生「春季」。
// v20a229 B3：CLEAN100_GIG_RELEASE 表已刪（舊表），normalize 唔再幫通告加 releaseLabel；
//       gigReleaseLine88 本身留返（label 直通＋季節衍生）。
// 反證：喺 v20a99 index 上行 → 冇 CLEAN100_* → 抽取即 throw → FAIL。
// 用法：node tests/test_cleanup100_logic.js [path-to-index.html]
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
/* ---- sandbox stubs ---- */
const START = { y: 1990, m: 1, d: 1 };
let S = { dayIndex: 0, stars: {}, news82: null, mockRumors: [] };
let __c16done = false;
function enc83NodeDone(id){ return id === 'N15' ? __c16done : false; }
let __enqueued = [];
function enqueueNewspaperItem(item){ __enqueued.push(item); return item; }
function ensureNewspaperClippings(){ return []; }
function news82DateLabel(){ return ''; }
function syncNotebookMirror(){}
function ensureMockJournal(){}
function saveQ(){}
let __ys = { year: 1992, season: '秋' };
function yearSeasonNow(){ return __ys; }
function enc79AnyBeatOpen(){ return false; }
function enc79WhisperActive(){ return false; }
/* ---- eval real code ---- */
eval([
  extractConst('YEARS66_SHIFT'), extractConst('YEARS66_OLD_MIN'), extractConst('YEARS66_TOKEN_RE'),
  extractConst('YEARS66_SKIP_KEYS'), extractConst('YEARS66_YEAR_KEYS'),
  extractFn('years66ShiftYear'), extractFn('years66ShiftText'), extractFn('years66Walk'),
  extractConst('CONTRA98_WHEN_FIX'), extractConst('CLEAN100_WHEN_FIX'), extractFn('contra98FixNodeWhen'),
  extractConst('GIG_SEASON_SPAN88'),
  extractFn('calendarSeason'),
  extractFn('spSoftSeasonChar'), extractFn('spPlayerMeta'),
  extractFn('storyWeekStamp'),
  extractConst('NEWS82_EVENTS'), extractFn('ensureNews82'), extractFn('news82Tick'),
  extractFn('enc79PresenceP'),
  extractFn('gigReleaseLine88'),
  'globalThis.__C100 = { CLEAN100_WHEN_FIX, contra98FixNodeWhen, years66Walk, spPlayerMeta, storyWeekStamp, NEWS82_EVENTS, ensureNews82, news82Tick, enc79PresenceP, gigReleaseLine88 };',
].join('\n'));
const C = globalThis.__C100;

/* (1) A-04 */
const mainPack = JSON.parse(fs.readFileSync(path.join(rootDir, 'content', 'story_detail_n1_to_n17.json'), 'utf8'));
C.contra98FixNodeWhen([mainPack]);
const nC2 = mainPack.nodes.find(n => n.id === 'N2'), nC3 = mainPack.nodes.find(n => n.id === 'N3');
ok('A04 N2 when 已改冬', nC2.when.indexOf('冬') >= 0 && nC2.eraTag.indexOf('winter') >= 0);
ok('A04 N3 when 已改冬', nC3.when.indexOf('冬') >= 0 && nC3.eraTag.indexOf('winter') >= 0);
C.years66Walk(mainPack, null);
ok('A04 N2 頁首 1990冬', C.spPlayerMeta(nC2) === '主線 · 1990冬');
ok('A04 N3 頁首 1990冬', C.spPlayerMeta(nC3) === '主線 · 1990冬');
const nC1 = mainPack.nodes.find(n => n.id === 'N1');
ok('A04 N1 頁首不受影響', C.spPlayerMeta(nC1) === '主線 · 1990冬');

/* (2) A-05/A-06 */
S.dayIndex = 0;
ok('A05 N5 day0 頁首 1990冬', C.spPlayerMeta({ id: 'N5', when: '1988秋 / W9-10', eraTag: 'era_1988_autumn_unitdrama' }) === '主線 · 1990冬');
S.dayIndex = 75; /* 1990-03-17 春 */
ok('A05 N5 春日頁首 1990春', C.spPlayerMeta({ id: 'N5', when: '1988秋 / W9-10', eraTag: 'era_1988_autumn_unitdrama' }) === '主線 · 1990春');
S.dayIndex = 800; /* 1992-03-11 春 */
ok('A06 R_xu_meet 頁首 1992春', C.spPlayerMeta({ id: 'R_xu_meet', when: '1992春', eraTag: 'era_1992_spring' }) === '主線 · 1992春');
ok('A06 A_fong_crisis 頁首跟曆法', C.spPlayerMeta({ id: 'A_fong_crisis', when: '1992夏', eraTag: 'era_1992_summer' }) === '主線 · 1992春');
S.dayIndex = 75; /* 春：一般節點唔應該跟曆法轉季 */
const other = C.spPlayerMeta({ id: 'N10', when: '1988冬 / W40', eraTag: 'era_1988_winter_unitdrama' });
ok('A06 一般節點行返舊路徑', other === '主線 · 1990冬');
S.dayIndex = 0;

/* (3) A-12（v20a234：WF1 內嵌表已刪，N18/N19 由 JSON pack 直出） */
const n18 = mainPack.nodes.find(n => n.id === 'N18'), n19 = mainPack.nodes.find(n => n.id === 'N19');
ok('A12 N18 weekMin=48', n18 && n18.pacing.weekMin === 48);
ok('A12 N19 weekMin=61', n19 && n19.pacing.weekMin === 61);
const wf1copy = JSON.parse(JSON.stringify({ N18: n18, N19: n19 }));
C.years66Walk(wf1copy, null);
ok('A12 N18 章戳第48週', C.storyWeekStamp(wf1copy.N18).indexOf('約第48週') >= 0);
ok('A12 N19 章戳第61週', C.storyWeekStamp(wf1copy.N19).indexOf('約第61週') >= 0);
ok('A12 pack N18/N19 各一（冇重複注入）',
   mainPack.nodes.filter(n => n.id === 'N18').length === 1 && mainPack.nodes.filter(n => n.id === 'N19').length === 1);

/* (4) B-03（v20a242：覆寫表已刪，讀 content JSON 直出） */
const lanPack = JSON.parse(fs.readFileSync(path.join(rootDir, 'content', 'story_detail_romance_lan_xu.json'), 'utf8'));
const lanById = {};
lanPack.nodes.forEach(n => { if(n.id.startsWith('R_lan_')) lanById[n.id] = n; });
const push1 = lanById.R_lan_push1;
const allStats = [];
(function collect(o){ if(!o || typeof o !== 'object') return; if(o.stats) allStats.push(o.stats); Object.keys(o).forEach(k => collect(o[k])); })(lanById);
ok('B03 全藍線冇 stats.music', allStats.every(s => !('music' in s)));
const sang = (push1.choices || []).find(c => (c.effects && c.effects.flags || []).indexOf('flag_lan_sang_together') >= 0);
ok('B03 一齊捱過抉擇 stage:1', !!(sang && sang.effects.stats.stage === 1 && sang.effects.stats.rel_lan === 2));
const crisis = lanById.R_lan_crisis;
/* v20a159 ROM159：crisis 由豪門／聯姻改做屋企／阿爸壓力，flag_family_marriage 兩抉擇都刪；help 寫 flag_family_help＋flag_lan_help，stepback 寫 flag_lan_stepback。 */
const famFlags = (crisis.choices || []).map(c => (c.effects && c.effects.flags) || []).filter(f => f.indexOf('flag_family_help') >= 0);
ok('B03 屋企壓力：help 寫 flag_family_help（唔再係豪門聯姻旗）', famFlags.length === 1);
ok('B03 crisis flags_written 不變（新版）', JSON.stringify(crisis.flags_written) === JSON.stringify(['flag_family_help', 'flag_lan_help', 'flag_lan_stepback']));

/* (5) A-08 */
function freshNews(day){ S = { dayIndex: day, stars: {}, news82: null, mockRumors: [] }; __enqueued = []; }
freshNews(532); __c16done = false;
C.news82Tick();
ok('A08 E5 day532 照刊', !!S.news82.pub.E5);
freshNews(1015); __c16done = false;
C.news82Tick();
ok('A08 E4 未做N15唔刊', !S.news82.pub.E4 && !__enqueued.some(e => e.worldId === 'E4'));
__c16done = true;
C.news82Tick();
ok('A08 E4 做完N15照刊', !!S.news82.pub.E4 && __enqueued.some(e => e.worldId === 'E4'));
freshNews(1030); __c16done = false;
const stArc = C.ensureNews82();
ok('A08 舊檔歸檔唔食E4', !stArc.arc.E4);
__c16done = true;
C.news82Tick();
ok('A08 舊檔N15後E4補刊', !!S.news82.pub.E4);

/* (6) B-05 presence */
__ys = { year: 1992, season: '秋' };
S = { dayIndex: 1000, stars: { chung_choning: { fav: 50, beatsDone: {} } }, starWhispers: {} };
const chungDef = { id: 'chung_choning', win: [[1991, '秋']] };
ok('B05 farewell未播 1992秋 p=0.25', C.enc79PresenceP(chungDef, 1000).p === 0.25);
S.stars.chung_choning.beatsDone.chung_farewell = 1000;
ok('B05 farewell播完 p=0', C.enc79PresenceP(chungDef, 1000).p === 0);
ok('B05 其他星不受影響', C.enc79PresenceP({ id: 'luk_baakyin', win: [] }, 1000).p === 0.5);

/* (7) A-07 */
ok('A07 B3：CLEAN100_GIG_RELEASE 表已刪（index.html 無此常量）', html.indexOf('const CLEAN100_GIG_RELEASE') < 0);
ok('A07 有label用label', C.gigReleaseLine88({ releaseLabel: '預計播出：1990 年農曆新年特輯', season: '春', year: 1988, type: '綜藝' }) === '預計播出：1990 年農曆新年特輯');
ok('A07 真春通告照衍生春季（綜藝 1990 春）', C.gigReleaseLine88({ season: '春', year: 1990, type: '綜藝' }) === '預計播出：1990 年春季');
ok('A07 真春電影衍生春季上映線', C.gigReleaseLine88({ season: '春', year: 1990, type: '電影' }) === '預計上映：1990 年春季');

console.log(fails.length ? ('FAILURES: ' + fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
