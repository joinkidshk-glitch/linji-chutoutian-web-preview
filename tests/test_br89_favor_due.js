// v20a254 D3（F1 幫忙通告恢復）測試：教學債到期循環——到期 → 事務所板出幫忙通告
//   《晨光劇場》臨時人手（gig_favor_ho_errand）→ 4 日內做完清債＋何生 rel +2；
//   過期作廢唔計 settled、rel −3；到期前用現金／禮物還咗 → closed_other 兜底記帳。
// 反證：對 v229–v253 index 行（FAVOR_DUE_CFG gigId null、FAVOR_DUE_GIGS []）→ D1 即 FAIL。
// 用法：node tests/test_br89_favor_due.js [path-to-index.html]
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
for(const f of ['favorDueDebt','ensureFavorDueSettled','ensureFavorDue','favorDueHintText','favorDueTick','mergeFavorGigs']){
  const src = extractFn(f);
  if(!src){ ok('抽取 function '+f, false); }
  else eval(src);
}
var S = null;
var GIGS = [];
var window = {};
var toasts = [];
var toast = function(m){ toasts.push(String(m)); };
var saveQ = function(){};
var syncNotebookMirror = function(){};
var ensureMockJournal = function(){};
var normalizeGigRecord = function(g){ return g; };
var settledCalls = [];
var favorLedgerNoteSettled = function(id, src){ settledCalls.push(id+':'+src); };
var bumpNpc = function(id, dv){ if(S && S.npcs) S.npcs[id] = (Number(S.npcs[id])||0) + dv; };
function freshS(day){
  return { dayIndex: day||0, fame: 5, npcs:{ agent: 0 }, favorDueSettled:{}, favorDueArmed:false,
    mockDebts:[{ id:'debt_ho_tutorial', creditor:'何生', title:'教學債', status:'未到期' }],
    mockCredits:[], mockRumors:[], flags:{}, wrapHistory:[] };
}

/* ---------- D1：接線形狀 ---------- */
ok('D1 FAVOR_DUE_CFG gigId 係 gig_favor_ho_errand（唔係 null）', FAVOR_DUE_CFG.gigId==='gig_favor_ho_errand' && FAVOR_DUE_CFG.debtId==='debt_ho_tutorial' && FAVOR_DUE_CFG.dueDays===7 && FAVOR_DUE_CFG.windowDays===4);
ok('D1 FAVOR_DUE_GIGS 得 1 張、id 啱', Array.isArray(FAVOR_DUE_GIGS) && FAVOR_DUE_GIGS.length===1 && FAVOR_DUE_GIGS[0].id==='gig_favor_ho_errand');
const g = FAVOR_DUE_GIGS[0];
ok('D1 幫忙通告係臨記通告、事務所板、4 日窗、1 日工', g.loc==='agency_ho' && g.tier==='臨記' && g.category==='臨記通告' && g.applyDeadlineDays===4 && g.shootDaysHint===1);
ok('D1 標題無年份數字', !/\d{4}/.test(g.title) && g.title.indexOf('晨光劇場')>=0);
ok('D1 片酬 $400 定額、hi ≤ lo×1.25', g.payExact===400 && Array.isArray(g.pay) && g.pay[1] <= g.pay[0]*1.25, JSON.stringify(g.pay));
ok('D1 無 req、無死 data favorDelta', Object.keys(g.req||{}).length===0 && !('favorDelta' in g));

/* ---------- D2：到期 → 叫數 → 上板 ---------- */
S = freshS(0); GIGS = []; settledCalls = [];
favorDueTick();
const d0 = S.mockDebts[0];
ok('D2 首見補 dueDay（當日 +7）＋ pending', d0 && d0.dueDay===7 && d0.favorState==='pending');
S.dayIndex = 6; favorDueTick();
ok('D2 未到期唔叫數', d0.favorState==='pending');
mergeFavorGigs();
ok('D2 未叫數唔上板', !GIGS.some(x=>x.id==='gig_favor_ho_errand'));
S.dayIndex = 7; favorDueTick();
ok('D2 到期嗰日叫數（favorState called、favorGigDay 7）', d0.favorState==='called' && d0.favorGigDay===7);
mergeFavorGigs();
ok('D2 叫數後事務所板有幫忙通告', GIGS.some(x=>x.id==='gig_favor_ho_errand'));

/* ---------- D3：4 日內做完 → 清債＋rel +2 ---------- */
S.flags['done_gig_favor_ho_errand'] = 1;
S.dayIndex = 9; favorDueTick();
ok('D3 做完清債（mockDebts 拎走）', !S.mockDebts.some(x=>x.id==='debt_ho_tutorial'));
ok('D3 結算記 repaid_help', S.favorDueSettled['debt_ho_tutorial'] && S.favorDueSettled['debt_ho_tutorial'].result==='repaid_help');
ok('D3 帳本計 settled（repaid_help）', settledCalls.indexOf('debt_ho_tutorial:repaid_help')>=0);
ok('D3 何生 rel +2', S.npcs.agent===2, 'agent='+S.npcs.agent);
mergeFavorGigs();
ok('D3 結清後幫忙通告落板', !GIGS.some(x=>x.id==='gig_favor_ho_errand'));

/* ---------- D4：過期作廢 → 唔計 settled、rel −3 ---------- */
S = freshS(0); GIGS = []; settledCalls = [];
favorDueTick();
S.dayIndex = 7; favorDueTick();
ok('D4 叫數後窗口內未做唔作廢（day 11）', (S.dayIndex = 11, favorDueTick(), S.mockDebts.some(x=>x.id==='debt_ho_tutorial')));
S.dayIndex = 12; favorDueTick();
ok('D4 過期作廢（day 12 ＝ favorGigDay 7＋4 日後）', !S.mockDebts.some(x=>x.id==='debt_ho_tutorial'));
ok('D4 作廢記 void_expired', S.favorDueSettled['debt_ho_tutorial'] && S.favorDueSettled['debt_ho_tutorial'].result==='void_expired');
ok('D4 作廢唔計帳本 settled', !settledCalls.some(c=>c.indexOf('debt_ho_tutorial')===0));
ok('D4 何生 rel −3', S.npcs.agent===-3, 'agent='+S.npcs.agent);

/* ---------- D5：未叫數／已結算唔注入 ---------- */
S = freshS(0); GIGS = [{ id:'gig_favor_ho_errand' }];
favorDueTick(); /* pending，未叫數 */
mergeFavorGigs();
ok('D5 pending 嗰陣注入池清走殘留', !GIGS.some(x=>x.id==='gig_favor_ho_errand'));

/* ---------- D6：到期前現金／禮物還咗 → closed_other 兜底 ---------- */
S = freshS(0); GIGS = []; settledCalls = [];
favorDueTick(); /* armed、dueDay 7 */
S.mockDebts = []; /* 到期前用其他方法還清 */
favorDueTick();
ok('D6 債唔見咗記 closed_other', S.favorDueSettled['debt_ho_tutorial'] && S.favorDueSettled['debt_ho_tutorial'].result==='closed_other');
ok('D6 closed_other 計帳本 settled', settledCalls.indexOf('debt_ho_tutorial:closed_other')>=0);
favorDueTick();
ok('D6 重行唔雙計', settledCalls.filter(c=>c==='debt_ho_tutorial:closed_other').length===1);

console.log(fails.length ? ('\nBR89 FAVOR DUE: '+fails.length+' FAIL') : '\nBR89 FAVOR DUE: ALL PASS');
process.exit(fails.length ? 1 : 0);
