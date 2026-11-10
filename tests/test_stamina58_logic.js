// v20a58 擴展・邏輯測試：新增體能訓練課程「武師班」(train_stamina)＋收埋週結暗加。
// 鎖住：(1) 目標建議 stamina → train_stamina、指去電影地點、mode=train；
//       (2) 手帳排程堂（resolvePlannedDay）同即場堂（applyTrainLesson）結算真加 stamina；
//       (3) 正常報名路徑：電影地點 doEnrollRun 附帶報名 train_stamina＋手帳訓練清單見到「武師班」；
//       (4) 累計 3 堂自動開放（2 堂未開）；
//       (5) 週結 flavor 三分支 stamina 全部不變（低體能／週末／高壓），其他效果（fame/stress）保留。
// Math.random 釘死 0 → R() 取下限、pick 取首項、附帶報名擲骰必中，斷言可確定。
// 反證：對 rest-only 版（v58 未擴展）行 → 課程唔存在＋週結仍加 stamina → FAIL。
// 用法：node tests/test_stamina58_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) throw new Error('fn not found: '+name);
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){
    if(html[j]==='{') depth++;
    else if(html[j]==='}'){ depth--; if(depth===0) break; }
  }
  return html.slice(i, j+1);
}
function extractConst(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) throw new Error('const not found: '+name);
  let depth = 0, started = false;
  for(let k=i; k<html.length; k++){
    const ch = html[k];
    if(ch==='{'||ch==='['){ depth++; started = true; }
    else if(ch==='}'||ch===']'){ depth--; if(started && depth===0) return html.slice(i, k+1)+';'; }
    else if(ch===';' && !started) return html.slice(i, k+1);
  }
  throw new Error('const end not found: '+name);
}
/* 週結 flavor 區塊唔係獨立函數（喺 settleWeek 入面），抽原文區塊 eval 行真碼。
   唔用括號配對：區塊入面有 template literal，${} 會騙過 naive 掃描；
   改用下一個里程碑分支「if(S.fame>=50」做結束錨點。 */
function extractWeekFlavorBlock(){
  const marker = 'if(S.stamina<12){';
  const i = html.indexOf(marker);
  if(i<0) throw new Error('week flavor block not found');
  const end = html.indexOf('if(S.fame>=50', i);
  if(end<0) throw new Error('week flavor block end anchor not found');
  const block = html.slice(i, end).trimEnd();
  if(block.indexOf('stressAtEnd<75')<0 || block.indexOf('週末稍歇')<0) throw new Error('week flavor block incomplete');
  return block;
}

/* ---- 世界：stub 基礎設施（照 test_rest58 配方） ---- */
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

eval("var START = { y:1988, m:3, d:7 };");
const CONSTS = ['STAT_LABEL','STAT_MAX','STRESS_MAX','PLAN_ITEMS','LOCS','COURSE_DEFS','COURSE_ENROLL_EXTRA','TRAIN_BY_TYPE','EVENTS_ZH_HK','TRAIN75_SPEC','LEVELS75_NAMES','LEVELS75_STEP','LEVELS75_MAX'];
for(const c of CONSTS) eval(extractConst(c).replace('const '+c+' =', 'var '+c+' ='));
var EVENTS = EVENTS_ZH_HK;
const FNS = ['R','clamp','pick','statHardMax','apply','weekdayIdx','weekdayName','dateObj','fmtDate',
  'allPlanDefs','planMeta','formatResultNotes','isCriticalPlanDay','planDayWouldWrap','displayDateObj',
  'fillTpl','eventLine','enrollCourse','maybeUnlockMidCourses','applyTrainLesson','doEnrollRun','enrolledCourseCta',
  'enrolledTrainItems','gigMissingReqGaps','bestTrainJumpForGig','stressDeltaForAct',
  'courseForStatKey','preferredLocForTrainTarget','resolvePlannedDay',
  /* v20a75：兩條上堂路徑共用核心＋級別衍生，harness 要一併抽取先行得返 */
  'levels75Count','levels75Level','levels75Next','levels75GainRange','levels75GainRoll','train75ApplyLesson'];
for(const f of FNS) eval(extractFn(f));
const weekFlavorBlock = extractWeekFlavorBlock();

ok('harness: 課程/建議/週結函數載入', typeof applyTrainLesson==='function' && typeof doEnrollRun==='function'
  && typeof courseForStatKey==='function' && weekFlavorBlock.indexOf('WEEK_LOW_STA')>=0);
ok('COURSE_DEFS 有 train_stamina「武師班」', !!(COURSE_DEFS.train_stamina && COURSE_DEFS.train_stamina.name==='武師班'));

/* 釘死隨機：R 取下限、pick 取首項、附帶報名擲骰（<0.55）必中 */
Math.random = function(){ return 0; };

function baseSave(){
  return {
    dayIndex: 30, fame: 17, popularity: 10, acting: 50, stage: 30, vocal: 20, looks: 30, iq: 30, charm: 20,
    stress: 10, money: 5000, stamina: 50,
    flags: {}, npcs: { colleague: 8, director: 4, stylist: 5, rival: 6, reporter: 3, agent: 12 },
    board: {}, booked: [], shoots: [], weekPlan: ['rest','rest','rest','rest','rest','rest','rest'],
    weekGigsDone: 0, weekTrainDone: 0, trainCount: {}, mockRumors: [], enrolled: {},
    story: { gigCount: 0, flags: {}, done: {} },
  };
}

/* ---- 1) 目標建議映射 ---- */
ok('courseForStatKey(stamina) === train_stamina', courseForStatKey('stamina') === 'train_stamina');
ok('courseForStatKey(stress) 保留 rest', courseForStatKey('stress') === 'rest');
ok('courseForStatKey(acting) 冇變', courseForStatKey('acting') === 'train_acting');
const staT = preferredLocForTrainTarget('stamina', courseForStatKey('stamina'));
ok('stamina 建議 mode=train', staT.mode === 'train');
ok('stamina 建議 courseId=train_stamina', staT.courseId === 'train_stamina');
const staLoc = LOCS.find(l=>l.id===staT.locId);
ok('stamina 建議指去電影地點（實得 ' + staT.locId + '）', !!staLoc && staLoc.type === 'film');
S = baseSave();
const jump = bestTrainJumpForGig({ req:{ stamina:60 } });
ok('通告缺體能 10 → 建議跳去武師班', !!jump && jump.target.courseId === 'train_stamina' && jump.target.mode === 'train');
ok('壓力預覽 train_stamina = 10（同演技/台風/歌藝同級）', stressDeltaForAct('train_stamina') === 10);

/* ---- 2) 結算真加體能：手帳排程堂 ---- */
S = baseSave();
S.enrolled = { train_stamina:true };
resolvePlannedDay('train_stamina');
ok('排程堂：stamina 50→54（+4 下限）', S.stamina === 54);
ok('排程堂：stress 10→18（+8 下限）', S.stress === 18);
ok('排程堂：trainCount.train_stamina = 1', (S.trainCount||{}).train_stamina === 1);

/* ---- 3) 結算真加體能：即場堂 ---- */
S = baseSave();
const lessonNotes = [];
applyTrainLesson('train_stamina', lessonNotes);
ok('即場堂：stamina 50→54', S.stamina === 54);
ok('即場堂：trainCount.train_stamina = 1', (S.trainCount||{}).train_stamina === 1);
ok('即場堂：有 TRAIN_RESULT 句', lessonNotes.join(' ').indexOf('武師班') >= 0 || lessonNotes.length > 0);

/* ---- 4) 正常報名路徑：電影地點報名附帶開武師班 ---- */
S = baseSave();
ok('電影地點主課係演技（TRAIN_BY_TYPE.film）', TRAIN_BY_TYPE.film.courseId === 'train_acting');
doEnrollRun({ id:'film_lion', type:'film', name:'獅子山製片' }, TRAIN_BY_TYPE.film);
ok('報名後 train_acting 已報', !!(S.enrolled||{}).train_acting);
ok('報名後 train_stamina 經附帶路徑已報（COURSE_ENROLL_EXTRA.film）', !!(S.enrolled||{}).train_stamina);
const planItems = enrolledTrainItems();
ok('手帳訓練清單見到「武師班」', planItems.some(it=>it.id==='train_stamina' && it.name==='武師班'));

/* ---- 5) 累計堂數自動開放：2 堂未開、3 堂開 ---- */
S = baseSave();
S.trainCount = { train_acting:2 };
maybeUnlockMidCourses([]);
ok('累計 2 堂：武師班未開（魅力已開）', !S.enrolled.train_stamina && !!S.enrolled.train_charm);
S = baseSave();
S.trainCount = { train_acting:3 };
maybeUnlockMidCourses([]);
ok('累計 3 堂：武師班自動開放', !!S.enrolled.train_stamina);

/* ---- 6) 週結 flavor 三分支：stamina 全部不變，其他效果保留 ---- */
S = baseSave(); S.stamina = 10; S.stress = 60; stressAtEnd = 60; __flavor = [];
eval(weekFlavorBlock);
ok('週結低體能分支：stamina 不變（10）', S.stamina === 10);
ok('週結低體能分支：fame −2 保留（17→15）', S.fame === 15);
ok('週結低體能分支：stress +5 保留（60→65）', S.stress === 65);
S = baseSave(); S.stamina = 50; S.stress = 50; stressAtEnd = 50; __flavor = [];
eval(weekFlavorBlock);
ok('週結週末分支：stamina 不變（50）', S.stamina === 50);
ok('週結週末分支：stress −6 保留（50→44）', S.stress === 44);
S = baseSave(); S.stamina = 50; S.stress = 90; stressAtEnd = 90; __flavor = [];
eval(weekFlavorBlock);
ok('週結高壓分支：stamina 不變（50）', S.stamina === 50);
ok('週結高壓分支：stress 不變（90）', S.stress === 90);

console.log(fails.length ? ('\nFAILED: ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
