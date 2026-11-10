// v20a75 LEVELS75 邏輯測試：訓練課程三級制——
//   (1) 級別衍生（累計堂數 → 一/二/三級、升下一級進度）；
//   (2) 逐課逐級增益表：地點即時堂（applyTrainLesson）實擲下限/上限 == 用戶拍板表；
//   (3) 排程堂（resolvePlannedDay）同核心同表（train_acting 二級抽驗）；
//   (4) 升級流程：上滿 5 堂出「升到二級」提示、再 5 堂「升到三級」、到頂冇再升；
//   (5) 存檔遷移 fixture (a)-(d)＋冪等；
//   (6) picker：全未開放組（智商組）出通用一句；已報名卡有級別名＋進度行。
// Math.random 釘死：0 = 擲下限、0.999999 = 擲上限。
// 反證：喺 v74 index 上行 → 冇 TRAIN75_SPEC／levels75* → 抽取即 throw → FAIL。
// 用法：node tests/test_levels75_logic.js [path-to-index.html]
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
function extractBlock(marker, endMarker){
  const a = html.indexOf(marker), b = html.indexOf(endMarker);
  if(a < 0 || b < 0 || b <= a) throw new Error('block not found: ' + marker);
  return html.slice(a, b);
}

/* ---- 世界 stub（照 test_stamina58 配方） ---- */
function makeEl(){
  return { classList:{ add(){}, remove(){}, toggle(){}, contains(){ return false; } },
    style:{}, dataset:{}, children:[], textContent:'', innerHTML:'',
    appendChild(){}, remove(){}, addEventListener(){}, querySelector(){ return makeEl(); }, querySelectorAll(){ return []; } };
}
var window = {};
var location = { search: '' };
var localStorage = { getItem: ()=>null, setItem: ()=>{}, removeItem: ()=>{} };
var __els = {};
var document = {
  getElementById(id){ return __els[id] || (__els[id] = makeEl()); },
  querySelector(){ return makeEl(); }, querySelectorAll(){ return []; },
  createElement(){ return makeEl(); }, body: makeEl(), addEventListener(){},
};
var modal = function(){}; var toast = function(){}; var saveQ = function(){};
var paintBar = function(){}; var drawMap = function(){}; var closeSheet = function(){}; var closeModal = function(){};
var enterHome = function(){}; var runScheduleFromToday = function(){}; var goToMapForBrowse = function(){};
var presentAudFailSettlement = function(){ return false; };
var presentRestSleepDayEnd = function(){};
var presentDueMorningPaper = function(){ return false; };
var afterDayModal = function(){}; var formatRestSleepDeltas = function(){ return ''; };
var flushWeekAccelSummary = function(){};
var dayEndContinueButtons = function(){ return [{ label:'返回地圖', role:'g', on:function(){} }]; };
var livingCostDayEndHint = function(){ return ''; };
var confirmSpendDay = function(label, cb){ if(typeof cb === 'function') cb(); };
var writeTodayPlan = function(){};
var FREEPLAY_FW = { _pendingPostShootReward: null, postShootRewards: null };
var _weekAccel = false; var _weekAccelBuf = [];
var planSelDay = 0; var planCat = 'browse'; var planDraft = null; var planBackup = null;
var atLoc = null;
var GIGS = [];
var S = null;
var tickDay = function(){ S.dayIndex += 1; return { ended:false, summary:null }; };
var __flavor = [];
var pushFlavor = function(x){ __flavor.push(x); };
var stressAtEnd = 0;
var softPreviewOn = function(){ return true; };
var _favorDebt = null;
var favorDueDebt = function(){ return _favorDebt; };

eval("var START = { y:1990, m:1, d:1 };");
const CONSTS = ['STAT_LABEL','STAT_MAX','STRESS_MAX','PLAN_ITEMS','LOCS','COURSE_DEFS','COURSE_ENROLL_EXTRA',
  'TRAIN_BY_TYPE','EVENTS_ZH_HK','TRAIN75_SPEC','LEVELS75_NAMES','LEVELS75_STEP','LEVELS75_MAX','LEVELS75_MID_OF','PREFS_KEY'];
for(const c of CONSTS) eval(extractConst(c).replace('const ' + c + ' =', 'var ' + c + ' ='));
var EVENTS = EVENTS_ZH_HK;
const FNS = ['R','clamp','pick','statHardMax','apply','weekdayIdx','weekdayName','dateObj','fmtDate',
  'allPlanDefs','planMeta','formatResultNotes','isCriticalPlanDay','planDayWouldWrap','displayDateObj',
  'fillTpl','eventLine','enrollCourse','maybeUnlockMidCourses','applyTrainLesson','resolvePlannedDay',
  'defaultPrefs','loadPrefs','savePrefs','setPref','progressToward',
  'levels75Count','levels75Level','levels75Next','levels75GainRange','levels75GainRoll','train75ApplyLesson','levels75MigrateSave'];
for(const f of FNS) eval(extractFn(f));
var applyPrefsChrome = function(){};
var calendarSeason = function(){ return '冬'; };

function baseSave(){
  return {
    dayIndex: 30, fame: 17, popularity: 10, acting: 10, stage: 10, vocal: 10, looks: 10, iq: 10, charm: 10,
    stress: 10, money: 5000, stamina: 10,
    flags: {}, npcs: { colleague: 8, director: 4, stylist: 5, rival: 6, reporter: 3, agent: 12 },
    board: {}, booked: [], shoots: [], weekPlan: ['rest','rest','rest','rest','rest','rest','rest'],
    weekGigsDone: 0, weekTrainDone: 0, trainCount: {}, mockRumors: [], enrolled: {},
    story: { gigCount: 0, flags: {}, done: {} },
  };
}

/* ---------- (1) 級別衍生 ---------- */
ok('級別衍生：0-4 堂一級／5-9 堂二級／10+ 堂三級',
  levels75Level({ trainCount:{} }, 'train_acting') === 1
  && levels75Level({ trainCount:{ train_acting:4 } }, 'train_acting') === 1
  && levels75Level({ trainCount:{ train_acting:5 } }, 'train_acting') === 2
  && levels75Level({ trainCount:{ train_acting:9 } }, 'train_acting') === 2
  && levels75Level({ trainCount:{ train_acting:10 } }, 'train_acting') === 3
  && levels75Level({ trainCount:{ train_acting:99 } }, 'train_acting') === 3);
ok('升級進度：7 堂 → 二級、級內 2 堂、再 3 堂升三級',
  (()=>{ const n = levels75Next({ trainCount:{ train_acting:7 } }, 'train_acting');
    return n.lv === 2 && n.inLv === 2 && n.left === 3 && !n.top; })());
ok('升級進度：10 堂 → 已到三級（top）',
  (()=>{ const n = levels75Next({ trainCount:{ train_acting:10 } }, 'train_acting');
    return n.lv === 3 && n.top === true; })());

/* ---------- (2) 逐課逐級增益表（即時堂實擲） ---------- */
/* 期望表（用戶 2026-11-10 拍板＋各課現行一級原值）：
   [mainLo, mainHi, subStat, subVal, stressLo, stressHi, fee] × 三級 */
const EXPECT = {
  train_acting:  { stat:'acting',  sub:'stage', base:[4,6], sBase:[8,12] },
  train_stage:   { stat:'stage',   sub:'charm', base:[4,6], sBase:[8,12] },
  train_vocal:   { stat:'vocal',   sub:null,    base:[4,6], sBase:[8,12] },
  train_looks:   { stat:'looks',   sub:'charm', base:[3,5], sBase:[6,9], fee:800 },
  train_charm:   { stat:'charm',   sub:null,    base:[3,5], sBase:[5,8] },
  train_iq:      { stat:'iq',      sub:'acting', base:[3,5], sBase:[4,6] },
  train_stamina: { stat:'stamina', sub:null,    base:[4,6], sBase:[8,12] },
};
function expAt(e, lv){ /* lv: 1..3 → 主 [lo,hi]、附帶值、壓力 [lo,hi] */
  const lo = e.base[0] + (lv - 1) * 2, hi = e.base[1] + (lv - 1) * 2 + (lv === 3 ? 1 : 0);
  const sLo = e.sBase[0] + (lv - 1) * 2, sHi = e.sBase[1] + (lv - 1) * 2;
  return { lo, hi, sub: e.sub ? lv : 0, sLo, sHi };
}
for(const cid of Object.keys(EXPECT)){
  const e = EXPECT[cid];
  for(let lv = 1; lv <= 3; lv++){
    const x = expAt(e, lv);
    /* 下限擲 */
    Math.random = function(){ return 0; };
    S = baseSave(); S.enrolled = { [cid]: true }; S.trainCount = { [cid]: (lv - 1) * 5 };
    const before = { m: S[e.stat], s: e.sub ? S[e.sub] : null, st: S.stress, money: S.money };
    applyTrainLesson(cid, []);
    ok(`增益表 ${cid} ${lv}級下限：主+${x.lo}／附帶+${x.sub}／壓力+${x.sLo}`,
      S[e.stat] - before.m === x.lo && S.stress - before.st === x.sLo
      && (!e.sub || S[e.sub] - before.s === x.sub)
      && (!e.fee || before.money - S.money === e.fee));
    /* 上限擲 */
    Math.random = function(){ return 0.999999; };
    S = baseSave(); S.enrolled = { [cid]: true }; S.trainCount = { [cid]: (lv - 1) * 5 };
    const b2 = { m: S[e.stat], s: e.sub ? S[e.sub] : null, st: S.stress };
    applyTrainLesson(cid, []);
    ok(`增益表 ${cid} ${lv}級上限：主+${x.hi}／壓力+${x.sHi}`,
      S[e.stat] - b2.m === x.hi && S.stress - b2.st === x.sHi && (!e.sub || S[e.sub] - b2.s === x.sub));
  }
}
ok('冇附帶嘅課（三級都冇）：歌藝／魅力／武師班',
  TRAIN75_SPEC.train_vocal.sub === null && TRAIN75_SPEC.train_charm.sub === null && TRAIN75_SPEC.train_stamina.sub === null);
ok('顯示衍生同實擲同表：ux68 增益表行 TRAIN75_SPEC（train_acting 二級）',
  (()=>{ const r = levels75GainRange('train_acting', 2);
    return r.acting[0] === 6 && r.acting[1] === 8 && r.stage[0] === 2 && r.stage[1] === 2 && r.stress[0] === 10 && r.stress[1] === 14; })());

/* ---------- (3) 排程堂同表（演技二級抽驗） ---------- */
Math.random = function(){ return 0; };
S = baseSave(); S.enrolled = { train_acting: true }; S.trainCount = { train_acting: 5 };
const pa = { a: S.acting, s: S.stage, st: S.stress };
resolvePlannedDay('train_acting');
ok('排程堂（演技二級）同表：演技+6／台風+2／壓力+10＋計堂 6',
  S.acting - pa.a === 6 && S.stage - pa.s === 2 && S.stress - pa.st === 10 && S.trainCount.train_acting === 6);

/* ---------- (4) 升級流程 ---------- */
Math.random = function(){ return 0; };
S = baseSave(); S.enrolled = { train_acting: true }; S.trainCount = { train_acting: 4 };
let notes = applyTrainLesson('train_acting', []);
ok('升級：第 5 堂出「升到二級」提示＋堂數 5＋級別二級',
  S.trainCount.train_acting === 5 && levels75Level(S, 'train_acting') === 2
  && notes.join('').indexOf('升到二級') >= 0);
S.trainCount.train_acting = 9;
notes = applyTrainLesson('train_acting', []);
ok('升級：第 10 堂出「升到三級」提示＋級別三級',
  S.trainCount.train_acting === 10 && levels75Level(S, 'train_acting') === 3
  && notes.join('').indexOf('升到三級') >= 0);
notes = applyTrainLesson('train_acting', []);
ok('升級：到頂後再上堂冇升級提示、級別維持三級',
  S.trainCount.train_acting === 11 && levels75Level(S, 'train_acting') === 3
  && notes.join('').indexOf('升到') < 0);

/* ---------- (5) 存檔遷移 ---------- */
function mig(o){ return levels75MigrateSave(JSON.parse(JSON.stringify(o))); }
let m = mig({ trainCount:{ train_acting:3, train_acting_mid:2 }, enrolled:{ train_acting:true, train_acting_mid:true },
  weekPlan:['train_acting_mid','rest','rest','rest','rest','rest','rest'] });
ok('遷移 (a)：已報進階＋中課 2 堂 → 演技堂數 7（二級、升三級進度 2/5）＋mid 鍵清＋排程改母課',
  m.trainCount.train_acting === 7 && !('train_acting_mid' in m.trainCount) && !('train_acting_mid' in m.enrolled)
  && m.enrolled.train_acting === true && m.weekPlan[0] === 'train_acting'
  && levels75Next(m, 'train_acting').inLv === 2 && levels75Next(m, 'train_acting').left === 3);
m = mig({ trainCount:{ train_acting:7 }, enrolled:{ train_acting:true }, weekPlan:['rest'] });
ok('遷移 (b)：基礎 7 堂冇進階 → 原封 7 堂（二級＋進度 2/5）',
  m.trainCount.train_acting === 7 && levels75Level(m, 'train_acting') === 2 && levels75Next(m, 'train_acting').inLv === 2);
m = mig({ trainCount:{ train_acting:3 }, enrolled:{ train_acting:true, train_acting_mid:true }, weekPlan:['rest'] });
ok('遷移 (c)：基礎 3 堂＋已報進階未上過 → 補到 5 堂＝二級進度 0（唔跌返一級）',
  m.trainCount.train_acting === 5 && levels75Level(m, 'train_acting') === 2 && levels75Next(m, 'train_acting').inLv === 0);
const clean = { trainCount:{ train_vocal:2 }, enrolled:{ train_vocal:true }, weekPlan:['rest','train_vocal'] };
ok('遷移 (d)：v74 乾淨檔原封不動', JSON.stringify(mig(clean)) === JSON.stringify(clean));
const fa = { trainCount:{ train_acting:3, train_acting_mid:2, train_stage:1, train_stage_mid:4 },
  enrolled:{ train_acting:true, train_acting_mid:true, train_stage:true, train_stage_mid:true },
  weekPlan:['train_stage_mid','train_acting_mid'] };
ok('遷移冪等：行兩次結果一樣（演技 7／台風 max(1,5)+4=9）',
  JSON.stringify(mig(mig(fa))) === JSON.stringify(mig(fa))
  && mig(fa).trainCount.train_acting === 7 && mig(fa).trainCount.train_stage === 9
  && mig(fa).weekPlan[0] === 'train_stage' && mig(fa).weekPlan[1] === 'train_acting');

/* ---------- (6) picker：通用一句＋卡面級別/進度 ---------- */
/* ux68GuideStat 係 UX68 block 內 let——要同 block 放埋同一個 eval 先共享
   （照 test_progress71 嘅 SRC 做法）。 */
const pickerSrc = extractBlock('/* ===== v20a68 UX68', 'function looksLikeEraId(s){') + `
  ;(function(){
    S = baseSave();
    ux68GuideStat = 'iq';
    const pIq = train71PickerHtml('day');
    ok('picker：智商組全未開放（冇附帶課）→ 出通用一句、課名隱藏',
      pIq.indexOf('暫時未開放報名') >= 0 && pIq.indexOf('智商・修養') < 0);
    S = baseSave(); S.enrolled = { train_acting: true }; S.trainCount = { train_acting: 4 };
    ux68GuideStat = 'acting';
    const pAct = train71PickerHtml('day');
    ok('picker：演技卡名「演技訓練・一級」＋進度「再 1 堂升二級」',
      pAct.indexOf('演技訓練・一級') >= 0 && pAct.indexOf('再 1 堂升二級') >= 0);
    S.trainCount.train_acting = 5;
    const pAct2 = train71PickerHtml('day');
    ok('picker：5 堂後卡變「演技訓練・二級」＋「再 5 堂升三級」',
      pAct2.indexOf('演技訓練・二級') >= 0 && pAct2.indexOf('再 5 堂升三級') >= 0);
    S.trainCount.train_acting = 10;
    const pAct3 = train71PickerHtml('day');
    ok('picker：10 堂卡「演技訓練・三級」＋「已到三級」',
      pAct3.indexOf('演技訓練・三級') >= 0 && pAct3.indexOf('已到三級') >= 0);
    ux68GuideStat = '';
  })();
`;
eval(pickerSrc);

console.log(fails.length ? ('FAILURES: ' + fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
