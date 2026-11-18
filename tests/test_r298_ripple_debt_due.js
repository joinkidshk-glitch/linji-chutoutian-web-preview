// v20a298 Q11（拒單債到期循環）測試：拒單債 debt_c4_ho_ripple 跟 F1 同一套——
//   到期 → 何生 Call 機叫數 → 事務所板出幫忙通告《午間劇場》臨時人手
//   （gig_favor_ho_ripple_errand）→ 4 日內做完清債＋何生 rel +2；
//   過期作廢唔計 settled、rel −3；到期前用現金／禮物還咗 → closed_other 兜底記帳。
// 反證：F1 教學債流程唔受影響（同一 sandbox 兩筆齊行，逐張獨立開關，
//   一張通告唔可以清兩筆債）。舊存檔（已有拒單債但無 dueDay）首次 tick 回填 dueDay。
// 用法：node tests/test_r298_ripple_debt_due.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond, extra){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name+(extra?' :: '+extra:'')); }
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) return null;
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){ if(html[j]==='{') depth++; else if(html[j]==='}'){ depth--; if(depth===0) break; } }
  return html.slice(i, j+1);
}
function extractConstVar(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) return null;
  let depth=0, started=false;
  for(let k=i; k<html.length; k++){
    const ch = html[k];
    if(ch==='{'||ch==='['){ depth++; started = true; }
    else if(ch==='}'||ch===']'){ depth--; if(started && depth===0) return html.slice(i, k+1).replace('const '+name, 'var '+name)+';'; }
    else if(ch===';' && !started) return html.slice(i, k+1).replace('const '+name, 'var '+name);
  }
  return null;
}

eval(extractConstVar('FAVOR_DUE_CFG'));
eval(extractConstVar('FAVOR_DUE_GIGS'));
eval(extractConstVar('RIPPLE_DUE_CFG'));
eval(extractConstVar('RIPPLE_DUE_GIGS'));
for(const f of ['favorDueDebt','ensureFavorDueSettled','ensureFavorDue','favorDueHintText','favorDueTick','mergeFavorGigs','rippleDueDebt','ensureRippleDue','rippleDueTick']){
  const src = extractFn(f);
  if(!src){ ok('抽取 function '+f, false); }
  else eval(src);
}
var S = null;
var GIGS = [];
var window = {};
var toasts = [];
var toast = function(m, opts){ toasts.push(String(m) + (opts && opts.sub ? ' | ' + String(opts.sub) : '')); };
var saveQ = function(){};
var syncNotebookMirror = function(){};
var ensureMockJournal = function(){};
var normalizeGigRecord = function(g){ return g; };
var settledCalls = [];
var favorLedgerNoteSettled = function(id, src){ settledCalls.push(id+':'+src); };
var bumpNpc = function(id, dv){ if(S && S.npcs) S.npcs[id] = (Number(S.npcs[id])||0) + dv; };
function freshS(day, debts){
  return { dayIndex: day||0, fame: 5, npcs:{ agent: 0 }, favorDueSettled:{}, favorDueArmed:false, rippleDueArmed:false,
    mockDebts: debts || [{ id:'debt_c4_ho_ripple', creditor:'何生', title:'拒單欠落・何生人情', status:'未到期' }],
    mockCredits:[], mockRumors:[], flags:{}, wrapHistory:[] };
}
const RIPPLE = 'debt_c4_ho_ripple';
const RGIG = 'gig_favor_ho_ripple_errand';
const TUT = 'debt_ho_tutorial';
const TGIG = 'gig_favor_ho_errand';

/* ---------- R1：接線形狀 ---------- */
ok('R1 RIPPLE_DUE_CFG 形狀（拒單債／獨立 gig／7 日／4 日窗）', RIPPLE_DUE_CFG.debtId===RIPPLE && RIPPLE_DUE_CFG.gigId===RGIG && RIPPLE_DUE_CFG.dueDays===7 && RIPPLE_DUE_CFG.windowDays===4);
ok('R1 RIPPLE_DUE_GIGS 得 1 張、id 啱、唔係 F1 嗰張', Array.isArray(RIPPLE_DUE_GIGS) && RIPPLE_DUE_GIGS.length===1 && RIPPLE_DUE_GIGS[0].id===RGIG && RGIG!==TGIG);
const g = RIPPLE_DUE_GIGS[0];
ok('R1 幫忙通告係臨記通告、事務所板、4 日窗、1 日工', g.loc==='agency_ho' && g.tier==='臨記' && g.category==='臨記通告' && g.applyDeadlineDays===4 && g.shootDaysHint===1);
ok('R1 標題無年份數字、有《午間劇場》', !/\d{4}/.test(g.title) && g.title.indexOf('午間劇場')>=0);
ok('R1 片酬 $40 定額、hi ≤ lo×1.25', g.payExact===40 && Array.isArray(g.pay) && g.pay[1] <= g.pay[0]*1.25, JSON.stringify(g.pay));
ok('R1 無 req、無死 data favorDelta', Object.keys(g.req||{}).length===0 && !('favorDelta' in g));
ok('R1 FAVOR_DUE_GIGS 仲係得 1 張（F1 D1 唔撞）', Array.isArray(FAVOR_DUE_GIGS) && FAVOR_DUE_GIGS.length===1 && FAVOR_DUE_GIGS[0].id===TGIG);

/* ---------- R2：到期 → 叫數 → 上板 ---------- */
S = freshS(150); GIGS = []; settledCalls = []; toasts = [];
rippleDueTick();
const d0 = S.mockDebts[0];
ok('R2 首見補 dueDay（當日 +7）＋ pending', d0 && d0.dueDay===157 && d0.favorState==='pending' && d0.kind==='help_gig');
ok('R2 提示文案出到期日數（favorDueHintText 通用）', favorDueHintText(d0).indexOf('7 日後到期')>=0, favorDueHintText(d0));
S.dayIndex = 156; rippleDueTick();
ok('R2 未到期唔叫數', d0.favorState==='pending');
mergeFavorGigs();
ok('R2 未叫數唔上板', !GIGS.some(x=>x.id===RGIG));
S.dayIndex = 157; rippleDueTick();
ok('R2 到期嗰日叫數（favorState called、favorGigDay 157）', d0.favorState==='called' && d0.favorGigDay===157);
ok('R2 叫數係何生拒單口吻', toasts.some(t=>t.indexOf('拒單')>=0 && t.indexOf('何生')>=0), toasts.join(' // '));
mergeFavorGigs();
ok('R2 叫數後事務所板有幫忙通告', GIGS.some(x=>x.id===RGIG));
ok('R2 叫數後 F1 嗰張唔上板', !GIGS.some(x=>x.id===TGIG));

/* ---------- R3：4 日內做完 → 清債＋rel +2 ---------- */
S.flags['done_'+RGIG] = 1;
S.dayIndex = 159; rippleDueTick();
ok('R3 做完清債（mockDebts 拎走）', !S.mockDebts.some(x=>x.id===RIPPLE));
ok('R3 結算記 repaid_help', S.favorDueSettled[RIPPLE] && S.favorDueSettled[RIPPLE].result==='repaid_help');
ok('R3 帳本計 settled（repaid_help）', settledCalls.indexOf(RIPPLE+':repaid_help')>=0);
ok('R3 何生 rel +2', S.npcs.agent===2, 'agent='+S.npcs.agent);
ok('R3 結清 toast 講一筆勾銷', toasts.some(t=>t.indexOf('一筆勾銷')>=0), toasts.join(' // '));
mergeFavorGigs();
ok('R3 結清後幫忙通告落板', !GIGS.some(x=>x.id===RGIG));

/* ---------- R4：過期作廢 → 唔計 settled、rel −3 ---------- */
S = freshS(150); GIGS = []; settledCalls = []; toasts = [];
rippleDueTick();
S.dayIndex = 157; rippleDueTick();
ok('R4 叫數後窗口內未做唔作廢（day 161）', (S.dayIndex = 161, rippleDueTick(), S.mockDebts.some(x=>x.id===RIPPLE)));
S.dayIndex = 162; rippleDueTick();
ok('R4 過期作廢（day 162 ＝ favorGigDay 157＋4 日後）', !S.mockDebts.some(x=>x.id===RIPPLE));
ok('R4 作廢記 void_expired', S.favorDueSettled[RIPPLE] && S.favorDueSettled[RIPPLE].result==='void_expired');
ok('R4 作廢唔計帳本 settled', !settledCalls.some(c=>c.indexOf(RIPPLE)===0));
ok('R4 何生 rel −3', S.npcs.agent===-3, 'agent='+S.npcs.agent);
ok('R4 作廢唔設「已逾期」status（免 soft 逾期鎖誤鎖）', !S.mockDebts.some(x=>x.id===RIPPLE));

/* ---------- R5：未叫數／已結算唔注入 ---------- */
S = freshS(150); GIGS = [{ id:RGIG }];
rippleDueTick(); /* pending，未叫數 */
mergeFavorGigs();
ok('R5 pending 嗰陣注入池清走殘留', !GIGS.some(x=>x.id===RGIG));

/* ---------- R6：到期前現金／禮物還咗 → closed_other 兜底 ---------- */
S = freshS(150); GIGS = []; settledCalls = []; toasts = [];
rippleDueTick(); /* armed、dueDay 157 */
S.mockDebts = []; /* 到期前用其他方法還清 */
rippleDueTick();
ok('R6 債唔見咗記 closed_other', S.favorDueSettled[RIPPLE] && S.favorDueSettled[RIPPLE].result==='closed_other');
ok('R6 closed_other 計帳本 settled', settledCalls.indexOf(RIPPLE+':closed_other')>=0);
rippleDueTick();
ok('R6 重行唔雙計', settledCalls.filter(c=>c===RIPPLE+':closed_other').length===1);

/* ---------- R7：舊存檔（已有拒單債但無 dueDay／kind）唔 crash、唔即到期 ---------- */
S = freshS(160, [{ id:RIPPLE, creditor:'何生', title:'拒單欠落・何生人情', status:'未到期' }]);
rippleDueTick();
const d7 = S.mockDebts[0];
ok('R7 舊檔首次 tick 回填 dueDay（當日 +7），唔即到期', d7 && d7.dueDay===167 && d7.favorState==='pending');
ok('R7 舊檔回填後提示文案啱', favorDueHintText(d7).indexOf('7 日後到期')>=0);

/* ---------- R8：F1 唔受影響（現實時序：教學債日 0–11 解決，拒單債日 150 先出世） ---------- */
S = freshS(0, [{ id:TUT, creditor:'何生', title:'教學債', status:'未到期' }]);
GIGS = []; settledCalls = []; toasts = [];
favorDueTick(); rippleDueTick();
ok('R8 教學債首見補 dueDay 7', S.mockDebts.find(x=>x.id===TUT).dueDay===7);
S.dayIndex = 7; favorDueTick(); rippleDueTick();
ok('R8 day 7 教學債叫數', S.mockDebts.find(x=>x.id===TUT).favorState==='called');
mergeFavorGigs();
ok('R8 day 7 板上淨係 F1 幫忙通告', GIGS.some(x=>x.id===TGIG) && !GIGS.some(x=>x.id===RGIG));
S.flags['done_'+TGIG] = 1;
S.dayIndex = 9; favorDueTick(); rippleDueTick();
ok('R8 做完 F1 通告清教學債、rel +2', !S.mockDebts.some(x=>x.id===TUT) && S.npcs.agent===2);
ok('R8 F1 清債記 repaid_help', S.favorDueSettled[TUT].result==='repaid_help');
mergeFavorGigs();
ok('R8 F1 結清後板上兩張都無', !GIGS.some(x=>x.id===TGIG) && !GIGS.some(x=>x.id===RGIG));
/* 日 150：N4 拒單，拒單債出世 */
S.dayIndex = 150;
S.mockDebts.push({ id:RIPPLE, creditor:'何生', title:'拒單欠落・何生人情', status:'未到期' });
favorDueTick(); rippleDueTick();
ok('R8 拒單債日 150 出世補 dueDay 157', S.mockDebts.find(x=>x.id===RIPPLE).dueDay===157);
ok('R8 教學債結算紀錄唔會俾拒單債郁到', S.favorDueSettled[TUT].result==='repaid_help' && !S.favorDueSettled[RIPPLE]);
S.dayIndex = 157; favorDueTick(); rippleDueTick();
ok('R8 day 157 拒單債叫數', S.mockDebts.find(x=>x.id===RIPPLE).favorState==='called');
mergeFavorGigs();
ok('R8 day 157 板上淨係拒單幫忙通告', GIGS.some(x=>x.id===RGIG) && !GIGS.some(x=>x.id===TGIG));

/* ---------- R9：兩筆同時叫數（人為），各清各 ---------- */
S = freshS(150, [
  { id:TUT, creditor:'何生', title:'教學債', status:'未到期' },
  { id:RIPPLE, creditor:'何生', title:'拒單欠落・何生人情', status:'未到期' }
]);
GIGS = []; settledCalls = []; toasts = [];
favorDueTick(); rippleDueTick();
S.dayIndex = 157; favorDueTick(); rippleDueTick();
mergeFavorGigs();
ok('R9 兩筆同時叫數，兩張通告齊上板', GIGS.some(x=>x.id===TGIG) && GIGS.some(x=>x.id===RGIG));
S.flags['done_'+RGIG] = 1;
S.dayIndex = 158; favorDueTick(); rippleDueTick();
ok('R9 做完拒單通告淨係清拒單債', !S.mockDebts.some(x=>x.id===RIPPLE) && S.mockDebts.some(x=>x.id===TUT));
ok('R9 拒單清債 rel +2、教學債未郁', S.npcs.agent===2 && !S.favorDueSettled[TUT]);

console.log(fails.length ? ('\nR298 RIPPLE DEBT DUE: '+fails.length+' FAIL') : '\nR298 RIPPLE DEBT DUE: ALL PASS');
process.exit(fails.length ? 1 : 0);
