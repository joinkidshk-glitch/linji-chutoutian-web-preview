// Weave Phase 4-5（v20a28）邏輯測試：主幹基建——三年版 phase／閘重映射＋openGate ctx 擴充
// 跟 v20a22 教訓：閘評估行真 StoryOC.evalNode＋真 BehaviorGate.evalGate3Y／readCtx，
// 狀態一律用真欄位砌（dayIndex 行真 dateObj 日曆、credit 行真 readDualTracks 派生、
// castingTags 用真 {id,label} 形狀）；唔 mock openGate／evalNode 本身。
// 覆寫節點嘅測試 node 故意帶五年版 pack 欄位（phase:"P5"＋week_min:100），證明覆寫真係取代咗 pack 閘。
// 用法：node tests/test_weave45_logic.js [path-to-index.html]
const fs = require('fs');
const path = process.argv[2] || require('path').join(__dirname, '..', 'index.html');
const html = fs.readFileSync(path, 'utf8');
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
  const i = html.indexOf('const '+name+' =') >= 0 ? html.indexOf('const '+name+' =') : html.indexOf('const '+name+'=');
  if(i<0) throw new Error('const not found: '+name);
  let depth=0, j=i;
  while(j<html.length && html[j]!=='{' && html[j]!=='[' && html[j]!==';') j++;
  if(html[j]===';') return html.slice(i, j+1);
  const openCh = html[j], closeCh = openCh==='{' ? '}' : ']';
  let started=false;
  for(; j<html.length; j++){
    if(html[j]===openCh){ depth++; started=true; }
    else if(html[j]===closeCh){ depth--; if(started && depth===0) break; }
  }
  return html.slice(i, j+1)+';';
}
function extractIIFE(decl){
  const i = html.indexOf(decl);
  if(i<0) throw new Error('iife not found: '+decl);
  const end = html.indexOf('\n})();', i);
  if(end<0) throw new Error('iife end not found: '+decl);
  return html.slice(i, end) + '\n})();';
}

/* ---- 環境 stub（module scope；eval 喺同一 scope 行，函數宣告會漏出嚟） ---- */
var window = {};
var location = { search: "" };
var localStorage = { getItem: ()=>null, setItem: ()=>{}, removeItem: ()=>{} };
var S = null;
var atLoc = null;
var saveQ = function(){};
var STORY_WIRE = { main:{ nodes: [] }, romance:{ veraHiuChoi:{ nodes: [] }, lanXu:{ nodes: [] }, tang:{ nodes: [] } }, rival:{ nodes: [] } };

const SRC = [
  extractConst('START'),
  extractFn('dateObj'),
  extractFn('calendarSeason'),
  extractFn('weekNumNow'),
  extractFn('dualTrackNumbers'),
  extractFn('readDualTracks'),
  extractFn('syncDualTracks'),
  extractFn('yearSeasonNow'),
  extractConst('STORY_GATE_3Y'),
  extractIIFE('const BehaviorGate = (function(){'),
  extractIIFE('const StoryOC = (()=>{'),
].join('\n')
 .replace('const START =', 'var START =')
 .replace('const STORY_GATE_3Y =', 'var STORY_GATE_3Y =')
 .replace('const BehaviorGate =', 'var BehaviorGate =')
 .replace('const StoryOC =', 'var StoryOC =');
eval(SRC);

ok('harness: BehaviorGate.evalGate3Y 載入', typeof BehaviorGate === 'object' && typeof BehaviorGate.evalGate3Y === 'function');
ok('harness: StoryOC.evalNode 載入', typeof StoryOC === 'object' && typeof StoryOC.evalNode === 'function');

/* ---- 狀態工具：全部行真欄位 ---- */
function dayIndexFor(y, m, d){
  const probe = { dayIndex: 0 };
  for(let i=0;i<2200;i++){
    probe.dayIndex = i;
    const keep = S; S = probe;
    const dt = dateObj();
    S = keep;
    if(dt.getFullYear()===y && dt.getMonth()+1===m && dt.getDate()===d) return i;
  }
  throw new Error('date not found: '+y+'-'+m+'-'+d);
}
function baseSave(){
  return {
    dayIndex: 0, fame: 0, stage: 0, acting: 0, stress: 0,
    industryCreditDelta: 0, industryCredit: 10,
    castingTags: [], mockDebts: [], mockRumors: [], flags: {}, npcs: {},
    story: { done:{}, flags:{}, rel:{}, routes:{}, phase:"P1" },
  };
}
function setSave(mut){ S = baseSave(); if(mut) mut(S); return S; }
function at(y, m, d){ const di = dayIndexFor(y, m, d); return (sv)=>{ sv.dayIndex = di; }; }
function withDone(){ const ids = Array.prototype.slice.call(arguments); return (sv)=>{ ids.forEach(id=>{ sv.story.done[id] = true; }); }; }
function compose(){ const fns = Array.prototype.slice.call(arguments); return (sv)=>{ fns.forEach(f=>f(sv)); }; }
/* 用真派生公式調 credit：credit = round(fame*0.5 + stage*0.3 + acting*0.2 - stress懲罰) + delta */
function setCredit(sv, want){
  sv.stage = 0; sv.acting = 0; sv.stress = 0;
  sv.industryCreditDelta = want - Math.round((Number(sv.fame)||0) * 0.5);
}
function setDual(sv, fame, wantDual){
  sv.fame = fame;
  setCredit(sv, wantDual - fame);
}
/* 覆寫節點：一律帶五年版 pack 欄位，證明覆寫取代 pack 閘 */
function gateOf(id, opts){
  return StoryOC.evalNode({ id: id, phase: "P5", openConditions: ["week_min:100", "phase_P5"] }, opts || {});
}
function expectGate(id, label, mut, want){
  setSave(mut);
  const r = gateOf(id);
  ok('gate '+id+' '+label+' → '+(want?'開':'唔開'), r.gate3Y === true && r.ok === want);
}

/* ================= (c) ctx 擴充 ================= */
(function(){
  setSave(compose(
    at(1991, 7, 10),
    (sv)=>{ sv.fame = 30; sv.stage = 10; sv.acting = 10; sv.stress = 0; sv.industryCreditDelta = 5;
            sv.castingTags = [{ id:"action", label:"動作" }]; }
  ));
  const ctx = BehaviorGate.readCtx({});
  ok('ctx: fame 行真 S.fame', ctx.fame === 30);
  ok('ctx: credit 行真派生（30*.5+10*.3+10*.2=20，+delta 5 → 25）', ctx.credit === 25);
  ok('ctx: dual = fame + credit', ctx.dual === 55);
  ok('ctx: year 行真日曆（1991）', ctx.year === 1991);
  ok('ctx: season 行真日曆（7 月→夏）', ctx.season === "夏");
  ok('ctx: tags 正規化含 id＋label', ctx.tags.indexOf("action")>=0 && ctx.tags.indexOf("動作")>=0);
  ok('ctx: week 行真 weekNumNow', ctx.week === Math.floor(S.dayIndex/7)+1);

  const over = BehaviorGate.readCtx({ ctx: { fame: 3, credit: 4, year: 1992, season: "冬", tags: ["喜劇"] } });
  ok('ctx: 明確傳入優先＋dual 自動計', over.fame === 3 && over.credit === 4 && over.dual === 7 && over.year === 1992 && over.season === "冬" && over.tags.join() === "喜劇");
  const blank = BehaviorGate.readCtx({ ctx: {} });
  ok('ctx: 空 ctx 預設（fame/credit/dual 0、year 1990、tags 空）', blank.fame === 0 && blank.credit === 0 && blank.dual === 0 && blank.year === 1990 && blank.tags.length === 0);
})();

/* ================= (a)+(e) 閘矩陣：齊條件→開；逐個抽走關鍵條件→唔開 ================= */
/* N6＝C6：route_tv＋W15+ */
expectGate('C6', 'route_tv＋W16', compose(at(1990,4,19), (sv)=>{ sv.story.routes.route_tv = true; }), true);
expectGate('C6', '缺 route', at(1990,6,20), false);
expectGate('C6', '得 route 但 W14', compose(at(1990,4,5), (sv)=>{ sv.story.routes.route_tv = true; }), false);
/* N7＝C7：C5 done＋信用>20＋1991 夏 */
expectGate('C7', '齊條件', compose(at(1991,7,10), withDone('C5'), (sv)=>setCredit(sv,21)), true);
expectGate('C7', '缺 C5', compose(at(1991,7,10), (sv)=>setCredit(sv,21)), false);
expectGate('C7', '信用得 20（唔過 >20）', compose(at(1991,7,10), withDone('C5'), (sv)=>setCredit(sv,20)), false);
expectGate('C7', '1991 春（季節唔啱）', compose(at(1991,4,10), withDone('C5'), (sv)=>setCredit(sv,21)), false);
expectGate('C7', '1990 夏（年份唔啱）', compose(at(1990,7,10), withDone('C5'), (sv)=>setCredit(sv,21)), false);
/* N8＝C11：1991 夏／秋 */
expectGate('C11', '1991 夏', at(1991,7,10), true);
expectGate('C11', '1991 秋', at(1991,10,10), true);
expectGate('C11', '1991 春', at(1991,4,10), false);
expectGate('C11', '1990 夏', at(1990,7,10), false);
/* N9＝C8：C7 done＋聲量>28＋喜劇/動作標籤＋1991 秋 */
expectGate('C8', '齊條件（標籤 id 命中）', compose(at(1991,10,10), withDone('C7'), (sv)=>{ sv.fame = 29; sv.castingTags = [{ id:"comedy", label:"喜劇" }]; }), true);
expectGate('C8', '標籤 label 命中（動作）', compose(at(1991,10,10), withDone('C7'), (sv)=>{ sv.fame = 29; sv.castingTags = [{ label:"動作" }]; }), true);
expectGate('C8', '標籤字串形（action）', compose(at(1991,10,10), withDone('C7'), (sv)=>{ sv.fame = 29; sv.castingTags = ["action"]; }), true);
expectGate('C8', '聲量得 28（唔過 >28）', compose(at(1991,10,10), withDone('C7'), (sv)=>{ sv.fame = 28; sv.castingTags = [{ id:"comedy", label:"喜劇" }]; }), false);
expectGate('C8', '無標籤', compose(at(1991,10,10), withDone('C7'), (sv)=>{ sv.fame = 29; }), false);
expectGate('C8', '缺 C7', compose(at(1991,10,10), (sv)=>{ sv.fame = 29; sv.castingTags = [{ id:"comedy", label:"喜劇" }]; }), false);
expectGate('C8', '1991 夏（季節唔啱）', compose(at(1991,7,10), withDone('C7'), (sv)=>{ sv.fame = 29; sv.castingTags = [{ id:"comedy", label:"喜劇" }]; }), false);
/* N10＝C9：1991 冬 */
expectGate('C9', '1991 冬', at(1991,12,10), true);
expectGate('C9', '1991 秋', at(1991,10,10), false);
expectGate('C9', '1990 冬', at(1990,12,10), false);
/* N11＝C10：C9 done＋雙軌>70＋1991 冬 */
expectGate('C10', '齊條件（雙軌 71）', compose(at(1991,12,10), withDone('C9'), (sv)=>setDual(sv,40,71)), true);
expectGate('C10', '雙軌得 70（唔過 >70）', compose(at(1991,12,10), withDone('C9'), (sv)=>setDual(sv,40,70)), false);
expectGate('C10', '缺 C9', compose(at(1991,12,10), (sv)=>setDual(sv,40,71)), false);
/* N12＝C15：動作標籤＋1992 春 */
expectGate('C15', '齊條件', compose(at(1992,4,10), (sv)=>{ sv.castingTags = [{ id:"action", label:"動作" }]; }), true);
expectGate('C15', '無動作標籤', at(1992,4,10), false);
expectGate('C15', '1991 春（年份唔啱）', compose(at(1991,4,10), (sv)=>{ sv.castingTags = [{ id:"action", label:"動作" }]; }), false);
/* N13＝C14：C10 done＋信用>42＋1992 夏 */
expectGate('C14', '齊條件（信用 43）', compose(at(1992,7,10), withDone('C10'), (sv)=>setCredit(sv,43)), true);
expectGate('C14', '信用得 42（唔過 >42）', compose(at(1992,7,10), withDone('C10'), (sv)=>setCredit(sv,42)), false);
expectGate('C14', '缺 C10', compose(at(1992,7,10), (sv)=>setCredit(sv,43)), false);
/* N14＝C12：C14 done＋聲量>50＋1992 秋 */
expectGate('C12', '齊條件（聲量 51）', compose(at(1992,10,10), withDone('C14'), (sv)=>{ sv.fame = 51; }), true);
expectGate('C12', '聲量得 50（唔過 >50）', compose(at(1992,10,10), withDone('C14'), (sv)=>{ sv.fame = 50; }), false);
expectGate('C12', '缺 C14', compose(at(1992,10,10), (sv)=>{ sv.fame = 51; }), false);
/* N15＝C16：C12 done＋雙軌>125＋1992 秋 */
expectGate('C16', '齊條件（雙軌 126）', compose(at(1992,10,10), withDone('C12'), (sv)=>setDual(sv,60,126)), true);
expectGate('C16', '雙軌得 125（唔過 >125）', compose(at(1992,10,10), withDone('C12'), (sv)=>setDual(sv,60,125)), false);
expectGate('C16', '缺 C12', compose(at(1992,10,10), (sv)=>setDual(sv,60,126)), false);
/* N16＝C13：1992 冬 */
expectGate('C13', '1992 冬', at(1992,12,10), true);
expectGate('C13', '1992 秋', at(1992,10,10), false);
expectGate('C13', '1991 冬', at(1991,12,10), false);
/* N17＝C17：C13 done＋1992 冬（事件閘） */
expectGate('C17', '齊條件', compose(at(1992,12,10), withDone('C13')), true);
expectGate('C17', '缺 C13', at(1992,12,10), false);
expectGate('C17', '1993 冬（yearEq 1992 唔啱）', compose(at(1993,12,10), withDone('C13')), false);

/* 同日禁：同 v17z 口徑，當日播完任一 C* → 覆寫節點都唔入可播；ignorePacing 可豁免 */
(function(){
  setSave(compose(at(1990,6,20), (sv)=>{ sv.story.routes.route_tv = true; sv.story.lastMainDoneDay = sv.dayIndex; }));
  const blocked = gateOf('C6');
  ok('same-day: 當日已播 C* → C6 唔開', blocked.ok === false && blocked.reasons.indexOf('days_after_prev:same_day')>=0);
  const waived = gateOf('C6', { ignorePacing: true });
  ok('same-day: ignorePacing 豁免 → 開', waived.ok === true);
})();

/* ================= (b) phase 三年版邊界 ================= */
function phaseAt(mut){ setSave(mut); return StoryOC.recomputePhaseFromProgress(); }
ok('phase: 1990 年中・無 done → P1', phaseAt(at(1990,6,1)) === 'P1');
ok('phase: C5 done → P1.5', phaseAt(compose(at(1990,6,1), withDone('C5'))) === 'P1.5');
ok('phase: 1991 年到 → P2', phaseAt(at(1991,1,15)) === 'P2');
ok('phase: 1992 年頭（1 月，冬尾唔跳級）→ P3', phaseAt(at(1992,1,15)) === 'P3');
ok('phase: 1992 春 → P3', phaseAt(at(1992,4,15)) === 'P3');
ok('phase: 1992 秋 → P4', phaseAt(at(1992,10,15)) === 'P4');
ok('phase: 1992 冬（12 月）→ P5', phaseAt(at(1992,12,15)) === 'P5');
ok('phase: 1992 春＋C14 done → P4', phaseAt(compose(at(1992,4,15), withDone('C14'))) === 'P4');
ok('phase: 1992 春＋C13 done → P5', phaseAt(compose(at(1992,4,15), withDone('C13'))) === 'P5');
(function(){
  setSave(compose(at(1990,6,1), (sv)=>{ sv.story.phase = 'P3'; }));
  ok('phase: 舊檔 P3 載入後 sync 唔拉低', StoryOC.syncPhaseFromProgress() === 'P3');
  setSave(compose(at(1990,7,10), withDone('C5'), (sv)=>{ setCredit(sv,21); sv.story.phase = 'P3'; }));
  const r = gateOf('C7');
  ok('phase: 舊檔 phase 高都唔會誤開 C7（閘行年份唔行 phase）', r.ok === false);
})();

/* ================= (d) C1–C5 零變化 ================= */
['C1','C2','C3','C4','C5'].forEach(id=>{
  ok('legacy: '+id+' 無 3Y 覆寫', BehaviorGate.gate3YEntry(id) === null && BehaviorGate.evalGate3Y({ id: id }) === null);
});
(function(){
  setSave(at(1990,4,1));
  const locked = StoryOC.evalNode({ id: 'C5', openConditions: ['C4'] }, {});
  ok('legacy: C5 行舊 token 閘（缺 C4 唔開）', locked.ok === false && locked.gate3Y === undefined);
  setSave(compose(at(1990,4,1), withDone('C4')));
  const open = StoryOC.evalNode({ id: 'C5', openConditions: ['C4'] }, {});
  ok('legacy: C5 行舊 token 閘（C4 done 開）', open.ok === true && open.gate3Y === undefined);
  setSave(compose(at(1990,4,10), withDone('C1')));
  const c2 = StoryOC.evalNode({ id: 'C2', openConditions: ['C1', 'week_min:4'] }, {});
  ok('legacy: C2 舊 week_min token 閘仍運作', c2.ok === true);
})();

console.log(fails.length ? ('FAILURES: '+fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
