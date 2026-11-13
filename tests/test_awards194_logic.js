// v20a194 頒獎禮拆 soft 閘・邏輯測試：
// 1. LIVE 模式（awardsSoftOn()==false）queueAwardsOnSeasonWindow() 照常排期——
//    春廣告賞／夏金碟夜／冬台慶各返 1（pristine main 返 []，因為閘喺第一行）。
// 2. awardsCheck() 加咗 live_queue 探針：ok:true、fails:[]、softStatus:"PASS"；
//    探針零副作用（flags／pending／queue／S.pendingAwardPack 前後一致），
//    已存在嘅 invited 旗標＋pending pack 照原樣還原。
// 3. awardsSoftOn() 保留、語義唔郁（無 BehaviorGate → false；回 true → true）。
// 4. 其餘排期邏輯唔郁：done 旗標唔重排、C10 讓路照樣延期台慶、debug force 路照 work。
// 反證：對 pristine main 2374637 index 行 → v194 標記未入 → FAIL（唔 crash）。
// 用法：node tests/test_awards194_logic.js [path-to-index.html]
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

/* 反證守衛：v194 嘢唔存在嗰陣乾淨 FAIL（逐項列出），唔好等 extraction 喺頂層 throw 崩潰。 */
const NEED194 = ['v20a194：頒獎禮拆 soft 閘', 'live_queue', 'softStatus:"PASS"', 'awards194ApplyMetaTip'];
let missing194 = NEED194.filter(s => html.indexOf(s) < 0);
if(missing194.length){
  missing194.forEach(m=>{ fails.push('反證：' + m + ' 唔存在'); console.log('FAIL 反證：' + m + ' 唔存在（pristine main 預期，v194 未入）'); });
  console.log('\nFAILED: ' + fails.length);
  process.exit(1);
}

/* ---- harness：真 pack JSON＋真排期函數；build／render 用 stub（只測閘＋排期＋自檢） ---- */
var window = {};
var SAVE = 'starVolunteer_map_v19w';
var START = { y: 1990, m: 1, d: 1 };
var S = { dayIndex: 60, fame: 26, industryCredit: 49, wrapHistory: [],
  awardsFlags: {}, awardsLog: [], pendingAwardPack: null };
var FREEPLAY_FW = {
  awardsSchema: JSON.parse(fs.readFileSync(path.join(path.dirname(htmlPath), 'content', 'SCHEMA_AWARDS_CEREMONY_v1.json'), 'utf8')),
  awardsStub: JSON.parse(fs.readFileSync(path.join(path.dirname(htmlPath), 'content', 'STUB_AWARDS_CEREMONY_v1.json'), 'utf8')),
  _pendingAward: null, _awardQueue: []
};
var __season = '春', __week = 9, __c10 = false;
function calendarSeason(){ return __season; }
function weekNumNow(){ return __week; }
function softC10WindowActive(){ return __c10; }
var METRIC = { award_harbour_ad: 'attention', award_golddisc_music: 'sales',
  award_harbour_film: 'boxOffice', award_singho_tv: 'ratings' };
function buildAwardResultPack(o){
  o = o || {};
  return { ceremonyId: o.ceremonyId, year: o.year, tier: o.forceTier || 'gallery',
    inviteTitle: 'x', metricEcho: METRIC[o.ceremonyId] || 'attention' };
}
function renderAwardInviteHtml(){ return ''; }
function renderAwardResultHtml(){ return ''; }
function presentPendingAward(){ return false; }
for(const f of ['awardsSoftOn', 'awardsCalendarYear', 'awardsEditionYear', 'awardsCeremonies',
  'awardsCeremonyById', 'awardsFlagKey', 'awardsGetFlag', 'awardsSetFlag',
  'ensureAwardsFlags', 'ensureAwardsLog', 'ensureAwardQueue', 'queueAwardInvite',
  'restorePendingAward136', 'awardsSeasonMatches', 'awardsWeekOk',
  'queueAwardsOnSeasonWindow', 'awardsCheck', 'awards194ApplyMetaTip'])
  eval(extractFn(f));
/* 模擬 loadFreeplayFramework 嘅覆寫步驟：pack 入 FW 之後先 tip meta。 */
awards194ApplyMetaTip(FREEPLAY_FW);
ok('0：覆寫後 schema meta.softStatus 係 PASS（runtime tip）',
  FREEPLAY_FW.awardsSchema.meta.softStatus === 'PASS');
ok('0：覆寫後 stub meta.softStatus 係 PASS（runtime tip）',
  FREEPLAY_FW.awardsStub.meta.softStatus === 'PASS');
ok('0：覆寫後 schema note 改做 tipped LIVE（唔再講 no tip LIVE）',
  FREEPLAY_FW.awardsSchema.meta.note.indexOf('no tip LIVE') < 0 &&
  FREEPLAY_FW.awardsSchema.meta.note.indexOf('v20a194: tipped LIVE') >= 0);
ok('0：覆寫後 stub note 改做 tipped LIVE（唔再講 Soft≠PASS）',
  FREEPLAY_FW.awardsStub.meta.note.indexOf('Soft≠PASS') < 0 &&
  FREEPLAY_FW.awardsStub.meta.note.indexOf('v20a194: tipped LIVE') >= 0);
ok('0：覆寫冪等（跑兩次唔會疊字／唔郁其他欄位）',
  (awards194ApplyMetaTip(FREEPLAY_FW),
   FREEPLAY_FW.awardsSchema.meta.softStatus === 'PASS' &&
   FREEPLAY_FW.awardsSchema.meta.version === 'v20a7' &&
   FREEPLAY_FW.awardsSchema.ceremonies.length === 4));
function reset(){
  S.awardsFlags = {}; S.awardsLog = []; S.pendingAwardPack = null;
  FREEPLAY_FW._pendingAward = null; FREEPLAY_FW._awardQueue = [];
}
function snap(){
  return JSON.stringify({ f: S.awardsFlags, p: FREEPLAY_FW._pendingAward,
    q: FREEPLAY_FW._awardQueue, sp: S.pendingAwardPack });
}

/* ---- 1. awardsSoftOn 保留、語義唔郁 ---- */
ok('1：無 BehaviorGate 嗰陣 awardsSoftOn()==false（live 預設）', awardsSoftOn() === false);
global.BehaviorGate = { featureFlag_softBehaviorGatePreview: function(){ return true; } };
ok('1：BehaviorGate 回 true 嗰陣 awardsSoftOn()==true（語義唔郁）', awardsSoftOn() === true);
delete global.BehaviorGate;
ok('1：BehaviorGate 拎走之後 awardsSoftOn() 返 false', awardsSoftOn() === false);

/* ---- 2. LIVE 模式排期：三窗各返 1（pristine 全部返 []） ---- */
reset(); S.dayIndex = 60; __season = '春'; __week = 9;
let q = queueAwardsOnSeasonWindow();
ok('2：LIVE 春窗 queue 返 1 張廣告賞（閘已拆）',
  Array.isArray(q) && q.length === 1 && q[0].ceremonyId === 'award_harbour_ad');
reset(); S.dayIndex = 160; __season = '夏'; __week = 23;
q = queueAwardsOnSeasonWindow();
ok('2：LIVE 夏窗 queue 返 1 張金碟夜',
  Array.isArray(q) && q.length === 1 && q[0].ceremonyId === 'award_golddisc_music');
reset(); S.dayIndex = 335; __season = '冬'; __week = 48;
q = queueAwardsOnSeasonWindow();
ok('2：LIVE 冬窗 queue 返 1 張台慶（C10 窗口之外）',
  Array.isArray(q) && q.length === 1 && q[0].ceremonyId === 'award_singho_tv');

/* ---- 3. 其餘排期邏輯唔郁 ---- */
reset(); S.dayIndex = 60; __season = '春'; __week = 9;
S.awardsFlags = { '1990/award_harbour_ad': 'done' };
q = queueAwardsOnSeasonWindow();
ok('3：done 旗標唔重排（春窗返 0）', Array.isArray(q) && q.length === 0);
reset(); S.dayIndex = 335; __season = '冬'; __week = 50; __c10 = true;
q = queueAwardsOnSeasonWindow();
ok('3：C10 窗口內台慶延期（冬窗返 0）', Array.isArray(q) && q.length === 0);
__c10 = false;
q = queueAwardsOnSeasonWindow();
ok('3：C10 窗口外／讓路完台慶照排（冬窗返 1）',
  Array.isArray(q) && q.length === 1 && q[0].ceremonyId === 'award_singho_tv');
reset(); S.dayIndex = 335; __season = '冬'; __week = 48;
q = queueAwardsOnSeasonWindow({ force: true, forceCeremonyId: 'award_harbour_ad',
  forceTier: 'gallery', ignoreC10: true });
ok('3：debug force 路照 work（冬窗 force 廣告賞返 1）',
  Array.isArray(q) && q.length === 1 && q[0].ceremonyId === 'award_harbour_ad');

/* ---- 4. awardsCheck：live_queue 探針＋softStatus PASS＋零副作用 ---- */
reset(); S.dayIndex = 60; __season = '春'; __week = 9;
let before = snap();
let chk = awardsCheck();
ok('4：awardsCheck ok:true、fails:[]', chk && chk.ok === true && Array.isArray(chk.fails) && chk.fails.length === 0);
if(chk && chk.fails && chk.fails.length) console.log('  fails: ' + chk.fails.join(','));
ok('4：awardsCheck softStatus 係 "PASS"（唔再係 ≠PASS）', chk && chk.softStatus === 'PASS');
ok('4：awardsCheck 零副作用（flags／pending／queue／存檔 pack 前後一致）', snap() === before);
reset(); S.dayIndex = 60; __season = '春'; __week = 9;
const sentinel = { ceremonyId: 'award_harbour_ad', year: 1990, tier: 'gallery' };
S.awardsFlags = { '1990/award_harbour_ad': 'invited' };
FREEPLAY_FW._pendingAward = sentinel; S.pendingAwardPack = sentinel;
chk = awardsCheck();
ok('4：awardsCheck 照過（已有 invited 旗標嗰陣都唔 fail）', chk && chk.ok === true);
ok('4：探針還原 invited 旗標（唔係食咗佢）', S.awardsFlags['1990/award_harbour_ad'] === 'invited');
ok('4：探針還原 _pendingAward（同一物件）', FREEPLAY_FW._pendingAward === sentinel);
ok('4：探針還原 S.pendingAwardPack（同一物件）', S.pendingAwardPack === sentinel);
ok('4：探針唔留低多餘 queue', FREEPLAY_FW._awardQueue.length === 0);
/* ---- 5. awardsCheck 同時驗 meta tip（未 tip 嗰陣要 fail） ---- */
reset(); S.dayIndex = 60; __season = '春'; __week = 9;
FREEPLAY_FW.awardsSchema.meta.softStatus = '≠PASS';
FREEPLAY_FW.awardsStub.meta.softStatus = '≠PASS';
chk = awardsCheck();
ok('5：meta 未 tip 嗰陣 awardsCheck fail（fails 有 meta_tip）',
  chk && chk.ok === false && (chk.fails || []).indexOf('meta_tip') >= 0);
ok('5：meta 未 tip 嗰陣 live_queue 探針本身照過（唔係佢 fail）',
  chk && (chk.fails || []).indexOf('live_queue') < 0);
awards194ApplyMetaTip(FREEPLAY_FW);
chk = awardsCheck();
ok('5：覆寫翻 tip 之後 awardsCheck 照過', chk && chk.ok === true);

console.log(fails.length ? ('\nFAILED: ' + fails.length + ' -> ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
