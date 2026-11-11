// v20a58 休息加體能 bug 修復・邏輯測試
// 鎖住：四條休息系路徑（週計劃 rest 日／home_chore／地點 doRest／提早休息 endBrowseDayGoHome）
// 結算後 stamina 必須原封不動、stress 必須有減；目標建議 stamina 唔再指去 rest（stress 保留）。
// 行真路徑：真 apply、真 resolvePlannedDay、真 doRest、真 endBrowseDayGoHome、
// 真 courseForStatKey／preferredLocForTrainTarget（基礎設施照 test_verify37 段三配方 stub）。
// 反證：對 v20a56 index 行 → 四路徑都會加 stamina＋stamina 映射 rest → FAIL。
// 用法：node tests/test_rest58_logic.js [path-to-index.html]
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

/* ---- 世界：stub 基礎設施（照 verify37 段三） ---- */
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
var confirmSpendDay = function(label, cb){ if(typeof cb === 'function') cb(); }; /* 扮玩家確認咗 */
var writeTodayPlan = function(){};
var FREEPLAY_FW = { _pendingPostShootReward: null, postShootRewards: null };
var _weekAccel = false; var _weekAccelBuf = [];
var planSelDay = 0; var planCat = 'browse'; var planDraft = null; var planBackup = null;
var atLoc = null;
var GIGS = [];
var S = null;
var tickDay = function(){ S.dayIndex += 1; return { ended:false, summary:null }; };

eval("var START = { y:1988, m:3, d:7 };");
const CONSTS = ['STAT_LABEL','STAT_MAX','STRESS_MAX','PLAN_ITEMS','LOCS','COURSE_DEFS'];
for(const c of CONSTS) eval(extractConst(c).replace('const '+c+' =', 'var '+c+' ='));
/* v20a112 ICONS112：被抽函數調用 iconHtml112，沙盒要一併載入對照＋helper。 */
eval(extractConst('EMOJI_ICON112').replace('const EMOJI_ICON112 =', 'var EMOJI_ICON112 ='));
eval(extractFn('iconHtml112'));
eval(extractFn('favDots112'));
const FNS = ['R','clamp','pick','statHardMax','apply','weekdayIdx','weekdayName','dateObj','fmtDate',
  'allPlanDefs','planMeta','formatResultNotes','isCriticalPlanDay','planDayWouldWrap','displayDateObj',
  'courseForStatKey','preferredLocForTrainTarget','resolvePlannedDay','endBrowseDayGoHome','doRest'];
for(const f of FNS) eval(extractFn(f));

ok('harness: 四路徑函數載入', typeof resolvePlannedDay==='function' && typeof doRest==='function'
  && typeof endBrowseDayGoHome==='function' && typeof courseForStatKey==='function');

function baseSave(){
  return {
    dayIndex: 30, fame: 17, popularity: 10, acting: 50, stage: 30, vocal: 20, looks: 30, iq: 30, charm: 20,
    stress: 60, money: 5000, stamina: 50,
    flags: {}, npcs: { colleague: 8, director: 4, stylist: 5, rival: 6, reporter: 3, agent: 12 },
    board: {}, booked: [], shoots: [], weekPlan: ['rest','rest','rest','rest','rest','rest','rest'],
    weekGigsDone: 0, weekTrainDone: 0, trainCount: {}, mockRumors: [], enrolled: {},
    story: { gigCount: 0, flags: {}, done: {} },
  };
}

/* ---- 1) 週計劃 rest 日 ---- */
S = baseSave();
resolvePlannedDay('rest');
ok('rest 日：stamina 不變（50）', S.stamina === 50);
ok('rest 日：stress 清零（60→' + S.stress + '；v20a65 FIX65-1 用戶規則：全日休息＝清零，取代舊 −(18+R(0,8)) 斷言）', S.stress === 0);

/* ---- 2) 週計劃 home_chore 日 ---- */
S = baseSave();
resolvePlannedDay('home_chore');
ok('home_chore：stamina 不變（50）', S.stamina === 50);
ok('home_chore：stress 有減（60→' + S.stress + '）', S.stress < 60);

/* ---- 3) 地點 doRest（休息室歇陣） ---- */
S = baseSave();
doRest({ id:'tvb_longmen', type:'tv', name:'星河電視台' });
ok('doRest：stamina 不變（50）', S.stamina === 50);
ok('doRest：stress 清零（60→' + S.stress + '；v20a65 FIX65-1 用戶規則：全日休息＝清零，取代舊 −(14+R(0,8)) 斷言）', S.stress === 0);

/* ---- 4) 提早休息 endBrowseDayGoHome ---- */
S = baseSave();
endBrowseDayGoHome();
ok('提早休息：stamina 不變（50）', S.stamina === 50);
ok('提早休息：stress 有減（60→' + S.stress + '）', S.stress < 60);

/* ---- 5) 目標建議映射 ---- */
ok('courseForStatKey(stamina) 唔再係 rest', courseForStatKey('stamina') !== 'rest');
ok('courseForStatKey(stress) 保留 rest', courseForStatKey('stress') === 'rest');
const staTarget = preferredLocForTrainTarget('stamina', courseForStatKey('stamina'));
ok('stamina 建議 mode 唔係 rest（實得 ' + staTarget.mode + '）', staTarget.mode !== 'rest');
const strTarget = preferredLocForTrainTarget('stress', courseForStatKey('stress'));
ok('stress 建議 mode 保留 rest', strTarget.mode === 'rest');

/* ---- 6) 計劃選單 hint 文案（減壓向，唔再聲稱回復體能） ---- */
const restMeta = planMeta('rest'), choreMeta = planMeta('home_chore');
ok('休息睡覺 hint 冇「體能」字眼', String(restMeta.hint||'').indexOf('體能') < 0);
ok('休息睡覺 hint 有「減壓」', String(restMeta.hint||'').indexOf('減壓') >= 0);
ok('收拾房間 hint 冇「回復」字眼', String(choreMeta.hint||'').indexOf('回復') < 0);
ok('收拾房間 hint 有「減壓」', String(choreMeta.hint||'').indexOf('減壓') >= 0);

console.log(fails.length ? ('\nFAILED: ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
