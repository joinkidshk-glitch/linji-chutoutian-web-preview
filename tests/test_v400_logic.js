// v20a400 細改 1–3・邏輯測試：
// (1) 預設唔再自動揀課：第 2 週起訓練位預填自由日，第 1 週引導照舊；建議邏輯抽去
//     lowestStatTrain400，只限已報名課（唔再建議未報名課，v360 遺留問題隨之解決）。
// (2) 壓力唔靜靜換休息：高壓／重拍攝週預設照舊得一日休息；峰值計法保留喺
//     weekStressPeak400（現壓力 vs 預覽峰值取高，計埋已 lock 拍攝），改由建議列出掣。
// (3) 機會成本：日格 hint（訓練進度／外出剩餘）＋改格成本行文案＋建議列行為（fake DOM）。
// 用法：node tests/test_v400_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond, extra){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name+(extra?(' :: '+extra):'')); }
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

/* ---- 世界 stub ---- */
var window = {};
var location = { search: '' };
var localStorage = { getItem: ()=>null, setItem: ()=>{}, removeItem: ()=>{} };
var S = null;
var GIGS = [];
var planDraft = null;
var clamp = function(v,a,b){ return Math.max(a, Math.min(b, v)); };
var scrubStaleJobs = function(d){ return d; };
var shootRemain = function(sh){ return Math.max(0,(sh.totalDays||0)-(sh.doneDays||0)); };
var shootWeekdayOk = function(){ return true; };
var toast = function(){};
var renderNotebook = function(){};
function fakeEl(){ return { innerHTML:"", hidden:true, textContent:"", children:[], appendChild(c){ this.children.push(c); } }; }
var suggestBox = fakeEl(), costBox = fakeEl();
var document = {
  getElementById(id){ return id==="nb-suggest400" ? suggestBox : (id==="nb-cost400" ? costBox : null); },
  createElement(tag){ return { type:"button", className:"", textContent:"", onclick:null }; },
};
for(const c of ['STAT_LABEL','COURSE_DEFS','PLAN_ITEMS','TRAIN75_SPEC','LEVELS75_NAMES','LEVELS75_STEP','LEVELS75_MAX'])
  eval(extractConst(c).replace('const '+c+' =', 'var '+c+' ='));
for(const f of ['weekNumNow','weekdayName','levels75Count','levels75Level','levels75Next','planMeta','isMapDay',
  'dayPlanLocked','stressDeltaForAct','previewWeekStress','lockShootsIntoDraft','defaultWeekPlan',
  'lowestStatTrain400','weekStressPeak400','freeDays400','nbDayHint400','costLose400','costGain400',
  'costLine400','showCost400','renderSuggest400']) eval(extractFn(f));

function mkS(dayIndex, o){
  o = o || {};
  return { dayIndex, stress:(o.stress!=null?o.stress:10), money:5000,
    acting:(o.acting!=null?o.acting:18), stage:(o.stage!=null?o.stage:14),
    vocal:(o.vocal!=null?o.vocal:14), looks:(o.looks!=null?o.looks:22),
    iq:(o.iq!=null?o.iq:20), charm:(o.charm!=null?o.charm:16), stamina:75,
    fame:5, popularity:3, enrolled:o.enrolled||{}, trainCount:o.trainCount||{},
    mockDebts:o.mockDebts||[], shoots:o.shoots||[], flags:{}, npcs:{}, board:{},
    booked:[], story:{ gigCount:0, flags:{}, done:{} }, weekPlan:null,
    homeEditable:false, lastTrain400:o.lastTrain400 };
}

/* ================= (1) 預設計劃唔再自動揀課 ================= */
S = mkS(14, { enrolled:{ train_acting:true, train_vocal:true }, trainCount:{ train_acting:3, train_vocal:0 } });
let p1 = defaultWeekPlan();
ok('1A 第 2 週起訓練位係自由日', p1[1]==='scout_all', p1.join(','));
ok('1A 無債：週五咖啡／週六街演', p1[4]==='cafe_gig' && p1[5]==='street', p1.join(','));
ok('1A 週日休息保留', p1[6]==='rest', p1.join(','));
S = mkS(14, { mockDebts:[{id:'d1'}] });
let p1b = defaultWeekPlan();
ok('1B 有人情債留位：週五自由日＋週六咖啡', p1b[4]==='scout_all' && p1b[5]==='cafe_gig', p1b.join(','));
S = mkS(0, {});
ok('1C 第 1 週引導照舊（base 不變）',
  defaultWeekPlan().join(',')==='scout_all,rest,scout_all,scout_all,street,cafe_gig,rest',
  defaultWeekPlan().join(','));
/* 高壓：舊制會靜靜加休息到 3 日；v400 照舊得 plan[6] 一日 */
S = mkS(112, { stress:79 });
let p1d = defaultWeekPlan();
ok('1D 高壓預設唔靜靜加休息（得一日）', p1d.filter(x=>x==='rest').length===1 && p1d[1]==='scout_all', p1d.join(','));
/* 重拍攝週：舊制峰值跨 80 → 3 日休息；v400 照舊一日，daysLeft 唔郁 */
S = mkS(28, { stress:35, enrolled:{}, trainCount:{ train_acting:5 }, shoots:[{ id:'shB', totalDays:5, doneDays:0, daysLeft:99, deadlineDay:999 }] });
let p1e = defaultWeekPlan();
ok('1E 重拍攝週預設唔靜靜加休息（一日）', p1e.filter(x=>x==='rest').length===1, p1e.join(','));
ok('1E 預設唔留 daysLeft 副作用', S.shoots[0].daysLeft===99, 'daysLeft='+S.shoots[0].daysLeft);

/* ================= (2) 建議 helper：只限已報名課 ================= */
S = mkS(14, { enrolled:{ train_acting:true, train_vocal:true }, trainCount:{ train_acting:3, train_vocal:0 } });
ok('2A 已報歌藝 0 堂 → 補歌藝（屬性最低）', lowestStatTrain400()==='train_vocal', lowestStatTrain400());
S = mkS(14, { enrolled:{ train_acting:true }, trainCount:{ train_acting:1 } });
ok('2B 未報歌藝 → 唔建議歌藝，只建議已報名演技', lowestStatTrain400()==='train_acting', lowestStatTrain400());
S = mkS(14, { enrolled:{}, trainCount:{} });
ok('2C 未報任何課 → null（建議掣隱藏）', lowestStatTrain400()===null, String(lowestStatTrain400()));
S = mkS(14, { acting:30, vocal:30, enrolled:{ train_acting:true, train_vocal:true, train_looks:true }, trainCount:{ train_acting:3, train_vocal:2, train_looks:0 } });
ok('2D 三科已報：屬性最低係外貌 → 補外貌', lowestStatTrain400()==='train_looks', lowestStatTrain400());
S = mkS(14, { acting:20, vocal:20, enrolled:{ train_acting:true, train_vocal:true }, trainCount:{ train_acting:5, train_vocal:1 } });
ok('2E 同屬性：堂數少先（歌藝 1 堂）', lowestStatTrain400()==='train_vocal', lowestStatTrain400());

/* ================= (3) 壓力峰值計法保留 ================= */
S = mkS(112, { stress:79 });
planDraft = defaultWeekPlan();
ok('3A 峰值計法保留：79 入口＋兼職推峰 92', weekStressPeak400(planDraft)===92, 'peak='+weekStressPeak400(planDraft));
S = mkS(28, { stress:35, shoots:[{ id:'shB', totalDays:5, doneDays:0, daysLeft:99, deadlineDay:999 }] });
planDraft = defaultWeekPlan();
ok('3B 重拍攝週峰值計入已 lock 拍攝（≥80）', weekStressPeak400(planDraft)>=80, 'peak='+weekStressPeak400(planDraft));
ok('3B 峰值預覽唔留 daysLeft 副作用', S.shoots[0].daysLeft===99, 'daysLeft='+S.shoots[0].daysLeft);
S = mkS(14, { stress:10 });
planDraft = defaultWeekPlan();
ok('3C 低壓週峰值 23（咖啡＋6／街演＋7）', weekStressPeak400(planDraft)===23, 'peak='+weekStressPeak400(planDraft));

/* ================= (4) 自由日 ================= */
S = mkS(14, {});
planDraft = ["scout_all","train_acting","scout_all","rest","street","cafe_gig","rest"];
ok('4A 自由日只計未鎖定 scout_*（[0,2]）', freeDays400().join(',')==='0,2', freeDays400().join(','));

/* ================= (5) 日格 hint 機會成本 ================= */
S = mkS(14, { trainCount:{ train_vocal:3 } });
planDraft = ["scout_all","train_vocal","scout_all","scout_all","cafe_gig","street","rest"];
ok('5A 訓練格（可編輯）：再 2 堂升二級', nbDayHint400(1, planMeta("train_vocal"), true, false)==='再 2 堂升二級', nbDayHint400(1, planMeta("train_vocal"), true, false));
S = mkS(14, { trainCount:{ train_vocal:10 } });
ok('5B 訓練格到頂：已到三級', nbDayHint400(1, planMeta("train_vocal"), true, false)==='已到三級', nbDayHint400(1, planMeta("train_vocal"), true, false));
S = mkS(14, {});
planDraft = ["scout_all","train_vocal","scout_all","scout_all","cafe_gig","street","rest"];
ok('5C 外出日（可編輯）：本週外出機會剩 3 日', nbDayHint400(0, planMeta("scout_all"), true, false)==='本週外出機會剩 3 日', nbDayHint400(0, planMeta("scout_all"), true, false));
S = mkS(14, { trainCount:{ train_vocal:3 } });
ok('5D 訓練格（唯讀）：原 hint＋進度', nbDayHint400(1, planMeta("train_vocal"), false, false)==='發聲／跟唱 · 再 2 堂升二級', nbDayHint400(1, planMeta("train_vocal"), false, false));
ok('5E 鎖定格維持拍攝檔期已定', nbDayHint400(1, planMeta("train_vocal"), true, true)==='拍攝檔期已定 · 不可改');

/* ================= (6) 改格成本行文案 ================= */
S = mkS(14, { trainCount:{ train_vocal:3 } });
ok('6A 街演 → 休息：失去收入；得到壓力清零',
  costLine400("street","rest",1)==='週二：街頭表演 → 休息瞓覺：失去約 $35–60 收入；得到壓力清零', costLine400("street","rest",1));
ok('6B 咖啡 → 歌藝：失去收入；得到堂數＋學費＋壓力',
  costLine400("cafe_gig","train_vocal",1).indexOf('失去約 $45–75 收入')>=0
  && costLine400("cafe_gig","train_vocal",1).indexOf('得到歌藝 +1 堂（再 2 堂升二級）· 學費 $20 · 壓力 +10')>=0,
  costLine400("cafe_gig","train_vocal",1));
ok('6C 逛逛 → 街演：失去外出機會；得到收入＋壓力',
  costLine400("scout_all","street",0)==='週一：到處逛逛 → 街頭表演：失去一日外出機會；得到約 $35–60 收入 · 壓力 +7', costLine400("scout_all","street",0));
ok('6D 同一格唔變 → 空字串', costLine400("street","street",1)==='', JSON.stringify(costLine400("street","street",1)));
ok('6E 歌藝 → 休息：失去一堂（進度在內）',
  costLine400("train_vocal","rest",1).indexOf('失去一堂歌藝訓練（再 2 堂升二級）')>=0, costLine400("train_vocal","rest",1));

/* ================= (7) 建議列行為（fake DOM） ================= */
function resetBoxes(){ suggestBox = fakeEl(); costBox = fakeEl(); }
function btnLabels(){ return suggestBox.children.map(b=>b.textContent); }
S = mkS(14, { stress:10, enrolled:{ train_vocal:true }, trainCount:{ train_vocal:0 }, lastTrain400:'train_vocal' });
planDraft = defaultWeekPlan();
resetBoxes(); renderSuggest400(true);
ok('7A 第 2 週訓練位自由日：兩個訓練建議掣齊',
  btnLabels().join('|')==='沿用上次：歌藝訓練|補最低屬性：歌藝訓練' && suggestBox.hidden===false, btnLabels().join('|'));
suggestBox.children[1].onclick();
ok('7A 撳「補最低屬性」套用到訓練位＋記低上次', planDraft[1]==='train_vocal' && S.lastTrain400==='train_vocal', planDraft.join(','));
ok('7A 撳完成本行有訓練文案', costBox.textContent.indexOf('歌藝 +1 堂')>=0 && costBox.textContent.indexOf('學費 $20')>=0, costBox.textContent);
S = mkS(14, { stress:10, enrolled:{}, lastTrain400:undefined });
planDraft = defaultWeekPlan();
resetBoxes(); renderSuggest400(true);
ok('7B 舊檔（無 lastTrain、未報名）＋低壓 → 建議列隱藏', suggestBox.hidden===true && suggestBox.children.length===0, btnLabels().join('|'));
S = mkS(14, { stress:85, enrolled:{} });
planDraft = defaultWeekPlan();
resetBoxes(); renderSuggest400(true);
ok('7C 高壓 85：出換休息＋再加一日（標明星期幾）',
  btnLabels().join('|')==='建議：壓力偏高，用週一自由日換休息|再加一日休息：週二', btnLabels().join('|'));
suggestBox.children[0].onclick();
ok('7C 撳換休息：週一變休息，拍攝鎖位以外', planDraft[0]==='rest' && planDraft[6]==='rest', planDraft.join(','));
ok('7C 換休息成本行：失去外出機會；得到壓力清零',
  costBox.textContent.indexOf('失去一日外出機會')>=0 && costBox.textContent.indexOf('得到壓力清零')>=0, costBox.textContent);
S = mkS(14, { stress:10, enrolled:{ train_vocal:true }, lastTrain400:'train_vocal',
  shoots:[{ id:'sh', totalDays:2, doneDays:0 }] });
planDraft = ["scout_all","shoot:sh","scout_all","scout_all","cafe_gig","street","rest"];
resetBoxes(); renderSuggest400(true);
ok('7D 訓練位係拍攝鎖位 → 唔出訓練建議掣', btnLabels().indexOf('沿用上次：歌藝訓練')<0 && btnLabels().indexOf('補最低屬性：歌藝訓練')<0, btnLabels().join('|'));
S = mkS(14, { stress:85, enrolled:{ train_vocal:true }, lastTrain400:'train_vocal' });
planDraft = defaultWeekPlan();
resetBoxes(); renderSuggest400(false);
ok('7E 唯讀態 → 建議列隱藏', suggestBox.hidden===true && suggestBox.children.length===0);

/* ================= (8) 成本行留到下一次改格 ================= */
S = mkS(14, {});
resetBoxes();
showCost400("street","rest",1);
const firstCost = costBox.textContent;
showCost400("street","street",1);
ok('8A 同一格唔變 → 成本行保留上一次文案', costBox.textContent===firstCost && firstCost.indexOf('壓力清零')>=0, costBox.textContent);

console.log(fails.length ? ('TOTAL FAIL ' + fails.length) : 'TOTAL PASS');
process.exit(fails.length ? 1 : 0);
