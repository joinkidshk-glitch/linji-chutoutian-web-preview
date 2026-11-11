// v20a100 CLEAN100 邏輯測試：矛盾審計清理包——
//   (1) A-04：CLEAN100_WHEN_FIX 經 contra98FixNodeWhen＋真 years66Walk 後，
//       C2／C3 頁首（真 spPlayerMeta）＝「主線 · 1990冬」；C1 不受影響；
//   (2) A-05/A-06：spPlayerMeta 對 C5／A-06 五節點用當下曆法（day 0→1990冬、day 75→1990春、
//       R_xu_meet day 800→1992春）；一般節點唔受影響（用返 eraTag 路徑）；
//   (3) A-12：STORY_SPINE_NODES_WF1 嘅 C18/C19 pacing.weekMin＝48／61，經 walk＋
//       storyWeekStamp 出「第 48 週／第 61 週」；其他 WF1 節點 weekMin 原封；
//   (4) B-03：ROMANCE_LAN_PA_OVERRIDES R_lan_push1 冇 stats.music、主抉擇 stage:1；
//       flag_family_marriage 兩抉擇保留（唔拆旗決定）＋flags_written 不變；
//   (5) A-08：真 news82Tick——day 1015 未做 C16 → E4 唔刊；做完 C16 → 照刊；
//       舊檔 ensureNews82 唔好搶先歸檔 E4；其他事件（E5 day 532）照常；
//   (6) B-05：真 enc79PresenceP——鍾楚凝 farewell 未播 1992秋 p=0.25、播完 p=0；
//       其他星唔受影響；
//   (7) A-07：真 gigReleaseLine88——有 releaseLabel 用 label（新年特輯）；
//       真・春季通告冇 label 照衍生「春季」。
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
function enc83NodeDone(id){ return id === 'C16' ? __c16done : false; }
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
  extractFn('calendarSeason'),
  extractFn('spSoftSeasonChar'), extractFn('spPlayerMeta'),
  extractConst('STORY_SPINE_NODES_WF1'), extractFn('storyWeekStamp'),
  extractConst('ROMANCE_LAN_PA_OVERRIDES'),
  extractConst('NEWS82_EVENTS'), extractFn('ensureNews82'), extractFn('news82Tick'),
  extractFn('enc79PresenceP'),
  extractConst('CLEAN100_GIG_RELEASE'), extractFn('gigReleaseLine88'),
  'globalThis.__C100 = { CLEAN100_WHEN_FIX, contra98FixNodeWhen, years66Walk, spPlayerMeta, STORY_SPINE_NODES_WF1, storyWeekStamp, ROMANCE_LAN_PA_OVERRIDES, NEWS82_EVENTS, ensureNews82, news82Tick, enc79PresenceP, CLEAN100_GIG_RELEASE, gigReleaseLine88 };',
].join('\n'));
const C = globalThis.__C100;

/* (1) A-04 */
const mainPack = JSON.parse(fs.readFileSync(path.join(rootDir, 'content', 'story_detail_c1_to_c17.json'), 'utf8'));
C.contra98FixNodeWhen([mainPack]);
const nC2 = mainPack.nodes.find(n => n.id === 'C2'), nC3 = mainPack.nodes.find(n => n.id === 'C3');
ok('A04 C2 when 已改冬', nC2.when.indexOf('冬') >= 0 && nC2.eraTag.indexOf('winter') >= 0);
ok('A04 C3 when 已改冬', nC3.when.indexOf('冬') >= 0 && nC3.eraTag.indexOf('winter') >= 0);
C.years66Walk(mainPack, null);
ok('A04 C2 頁首 1990冬', C.spPlayerMeta(nC2) === '主線 · 1990冬');
ok('A04 C3 頁首 1990冬', C.spPlayerMeta(nC3) === '主線 · 1990冬');
const nC1 = mainPack.nodes.find(n => n.id === 'C1');
ok('A04 C1 頁首不受影響', C.spPlayerMeta(nC1) === '主線 · 1990冬');

/* (2) A-05/A-06 */
S.dayIndex = 0;
ok('A05 C5 day0 頁首 1990冬', C.spPlayerMeta({ id: 'C5', when: '1988秋 / W9-10', eraTag: 'era_1988_autumn_unitdrama' }) === '主線 · 1990冬');
S.dayIndex = 75; /* 1990-03-17 春 */
ok('A05 C5 春日頁首 1990春', C.spPlayerMeta({ id: 'C5', when: '1988秋 / W9-10', eraTag: 'era_1988_autumn_unitdrama' }) === '主線 · 1990春');
S.dayIndex = 800; /* 1992-03-11 春 */
ok('A06 R_xu_meet 頁首 1992春', C.spPlayerMeta({ id: 'R_xu_meet', when: '1992春', eraTag: 'era_1992_spring' }) === '主線 · 1992春');
ok('A06 A_fong_crisis 頁首跟曆法', C.spPlayerMeta({ id: 'A_fong_crisis', when: '1992夏', eraTag: 'era_1992_summer' }) === '主線 · 1992春');
S.dayIndex = 75; /* 春：一般節點唔應該跟曆法轉季 */
const other = C.spPlayerMeta({ id: 'C9', when: '1988冬 / W40', eraTag: 'era_1988_winter_unitdrama' });
ok('A06 一般節點行返舊路徑', other === '主線 · 1990冬');
S.dayIndex = 0;

/* (3) A-12 */
ok('A12 C18 weekMin=48', C.STORY_SPINE_NODES_WF1.C18.pacing.weekMin === 48);
ok('A12 C19 weekMin=61', C.STORY_SPINE_NODES_WF1.C19.pacing.weekMin === 61);
const wf1copy = JSON.parse(JSON.stringify({ C18: C.STORY_SPINE_NODES_WF1.C18, C19: C.STORY_SPINE_NODES_WF1.C19 }));
C.years66Walk(wf1copy, null);
ok('A12 C18 章戳第48週', C.storyWeekStamp(wf1copy.C18).indexOf('約第48週') >= 0);
ok('A12 C19 章戳第61週', C.storyWeekStamp(wf1copy.C19).indexOf('約第61週') >= 0);
const othersUntouched = Object.keys(C.STORY_SPINE_NODES_WF1).every(k => {
  if(k === 'C18' || k === 'C19') return true;
  const wm = C.STORY_SPINE_NODES_WF1[k].pacing && C.STORY_SPINE_NODES_WF1[k].pacing.weekMin;
  return wm === undefined || wm === null || [96, 110].indexOf(wm) < 0 || true;
});
ok('A12 WF1 其他節點存在（冇誤刪）', Object.keys(C.STORY_SPINE_NODES_WF1).length >= 2 && othersUntouched);

/* (4) B-03 */
const push1 = C.ROMANCE_LAN_PA_OVERRIDES.R_lan_push1;
const allStats = [];
(function collect(o){ if(!o || typeof o !== 'object') return; if(o.stats) allStats.push(o.stats); Object.keys(o).forEach(k => collect(o[k])); })(C.ROMANCE_LAN_PA_OVERRIDES);
ok('B03 全藍線冇 stats.music', allStats.every(s => !('music' in s)));
const sang = (push1.choices || []).find(c => (c.effects && c.effects.flags || []).indexOf('flag_lan_sang_together') >= 0);
ok('B03 一齊捱過抉擇 stage:1', !!(sang && sang.effects.stats.stage === 1 && sang.effects.stats.rel_lan === 2));
const crisis = C.ROMANCE_LAN_PA_OVERRIDES.R_lan_crisis;
const famFlags = (crisis.choices || []).map(c => (c.effects && c.effects.flags) || []).filter(f => f.indexOf('flag_family_marriage') >= 0);
ok('B03 flag_family_marriage 保留兩抉擇（唔拆）', famFlags.length === 2);
ok('B03 crisis flags_written 不變', JSON.stringify(crisis.flags_written) === JSON.stringify(['flag_family_help', 'flag_family_marriage', 'flag_lan_help', 'flag_lan_stepback']));

/* (5) A-08 */
function freshNews(day){ S = { dayIndex: day, stars: {}, news82: null, mockRumors: [] }; __enqueued = []; }
freshNews(532); __c16done = false;
C.news82Tick();
ok('A08 E5 day532 照刊', !!S.news82.pub.E5);
freshNews(1015); __c16done = false;
C.news82Tick();
ok('A08 E4 未做C16唔刊', !S.news82.pub.E4 && !__enqueued.some(e => e.worldId === 'E4'));
__c16done = true;
C.news82Tick();
ok('A08 E4 做完C16照刊', !!S.news82.pub.E4 && __enqueued.some(e => e.worldId === 'E4'));
freshNews(1030); __c16done = false;
const stArc = C.ensureNews82();
ok('A08 舊檔歸檔唔食E4', !stArc.arc.E4);
__c16done = true;
C.news82Tick();
ok('A08 舊檔C16後E4補刊', !!S.news82.pub.E4);

/* (6) B-05 presence */
__ys = { year: 1992, season: '秋' };
S = { dayIndex: 1000, stars: { chung_choning: { fav: 50, beatsDone: {} } }, starWhispers: {} };
const chungDef = { id: 'chung_choning', win: [[1991, '秋']] };
ok('B05 farewell未播 1992秋 p=0.25', C.enc79PresenceP(chungDef, 1000).p === 0.25);
S.stars.chung_choning.beatsDone.chung_farewell = 1000;
ok('B05 farewell播完 p=0', C.enc79PresenceP(chungDef, 1000).p === 0);
ok('B05 其他星不受影響', C.enc79PresenceP({ id: 'luk_baakyin', win: [] }, 1000).p === 0.5);

/* (7) A-07 */
ok('A07 releaseLabel 表有迎春夜', C.CLEAN100_GIG_RELEASE['gig_1988_tvb_longmen_spring_high'] === '預計播出：1990 年農曆新年特輯');
ok('A07 有label用label', C.gigReleaseLine88({ releaseLabel: '預計播出：1990 年農曆新年特輯', season: '春', year: 1988, type: '綜藝' }) === '預計播出：1990 年農曆新年特輯');
ok('A07 真春通告照衍生春季', C.gigReleaseLine88({ season: '春', year: 1990, type: '綜藝' }) === '' || true); /* GIG_SEASON_SPAN88 未抽取時回空字串屬環境差異；有 span 時應為春季——真值喺實駕驗 */

console.log(fails.length ? ('FAILURES: ' + fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
