// v405 P1-2: stress suggestion appears even with zero free days (training day swap).
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) throw new Error('fn not found: '+name);
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){ if(html[j]==='{') depth++; else if(html[j]==='}'){ depth--; if(depth===0) break; } }
  return html.slice(i, j+1);
}
function extractConst(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) throw new Error('const not found: '+name);
  let depth=0, started=false;
  for(let k=i;k<html.length;k++){ const ch=html[k];
    if(ch==='{'||ch==='['){ depth++; started=true; }
    else if(ch==='}'||ch===']'){ depth--; if(started&&depth===0) return html.slice(i,k+1)+';'; }
    else if(ch===';'&&!started) return html.slice(i,k+1); }
  throw new Error('const end: '+name);
}
var window = {}; var location = { search:'' };
var localStorage = { getItem:()=>null, setItem:()=>{}, removeItem:()=>{} };
var S = null; var GIGS = []; var planDraft = null;
var clamp = function(v,a,b){ return Math.max(a, Math.min(b, v)); };
var scrubStaleJobs = function(d){ return d; };
var shootRemain = function(sh){ return Math.max(0,(sh.totalDays||0)-(sh.doneDays||0)); };
var shootWeekdayOk = function(){ return true; };
var toast = function(){}; var renderNotebook = function(){};
function fakeEl(){ return { innerHTML:"", hidden:true, textContent:"", children:[], appendChild(c){ this.children.push(c); } }; }
var suggestBox = fakeEl(), costBox = fakeEl();
var document = {
  getElementById(id){ return id==="nb-suggest400" ? suggestBox : (id==="nb-cost400" ? costBox : null); },
  createElement(tag){ return { type:"button", className:"", textContent:"", onclick:null }; },
};
for(const c of ['STAT_LABEL','COURSE_DEFS','PLAN_ITEMS','TRAIN75_SPEC','LEVELS75_NAMES','LEVELS75_STEP','LEVELS75_MAX'])
  eval(extractConst(c).replace('const '+c+' =','var '+c+' ='));
for(const f of ['weekNumNow','weekdayName','levels75Count','levels75Level','levels75Next','planMeta','isMapDay',
  'dayPlanLocked','stressDeltaForAct','previewWeekStress','lockShootsIntoDraft','defaultWeekPlan',
  'lowestStatTrain400','weekStressPeak400','freeDays400','nbDayHint400','costLose400','costGain400',
  'costLine400','showCost400','renderSuggest400']) eval(extractFn(f));
S = { dayIndex:14, stress:85, money:5000, acting:18, stage:14, vocal:14, looks:22, iq:20, charm:16, stamina:75,
  fame:5, popularity:3, enrolled:{ train_acting:true }, trainCount:{}, mockDebts:[], shoots:[], flags:{}, npcs:{},
  board:{}, booked:[], story:{ gigCount:0, flags:{}, done:{} }, weekPlan:null, homeEditable:false, lastTrain400:undefined };
planDraft = ["train_acting","train_acting","train_acting","train_acting","train_acting","train_acting","rest"];
renderSuggest400(true);
const labels = suggestBox.children.map(b=>b.textContent);
const stressBtn = suggestBox.children.find(b=>b.textContent.indexOf('壓力偏高')>=0);
let after = null;
if(stressBtn){ stressBtn.onclick(); after = planDraft.slice(); }
console.log(JSON.stringify({ labels, after }));
const pass = !!stressBtn && stressBtn.textContent.indexOf('訓練日')>=0 && after && after[0]==='rest' && after[6]==='rest';
console.log(pass ? 'P12 PASS' : 'P12 FAIL');
process.exit(pass?0:1);
