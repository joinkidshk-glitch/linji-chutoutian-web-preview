// v422 情報站／試鏡帶判定層：三種七圍狀態下，派出的通告必須可試鏡；無可試鏡者回 null（不收費路徑）。
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
let pass = 0, fail = 0;
function ok(name, cond){ if(cond){ pass++; console.log('  ok - ' + name); } else { fail++; console.log('  FAIL - ' + name); } }
function extractFn(decl){
  const i = html.indexOf(decl); if(i < 0) throw new Error('fn not found: ' + decl);
  let j = html.indexOf('{', i), depth = 0, k = j;
  for(; k < html.length; k++){ if(html[k] === '{') depth++; else if(html[k] === '}'){ depth--; if(depth === 0){ k++; break; } } }
  return html.slice(i, k);
}
var S = null;
var GIG_TIER_ORDER229 = ["臨記","初級","中級","高級","稀有"];
var GIG_REQ_KEYS88 = { acting:1, stage:1, vocal:1, looks:1, charm:1, iq:1, stamina:1, fame:1 };
var COURSE_DEFS = { train_acting:{} };
function gigTierCanon229(t){ return t || "初級"; }
function enc79PlayerTier(){ return 1; }
function isGigConsumed(){ return false; }
function isGigWrapped(){ return false; }
function isGigInProduction(){ return false; }
function gigLifecycleStatus(){ return { key:'open' }; }
function costume265EffStat(k){ return Number(S[k]) || 0; }
function softCastingTagGate(){ return { ok:true }; }
function softIndustryCreditGate(){ return { ok:true }; }
function costume382Gate(){ return { ok:true }; }
function dateObj(){ return new Date(1991, 5, 15); }
var GIGS = [
  { id:'g_low_ok', tier:'初級', type:'電影', req:{ acting:20 }, loc:'film_lion', title:'低門檻電影' },
  { id:'g_mid_ok', tier:'中級', type:'電影', req:{ acting:40, stage:30 }, loc:'film_lion', title:'中門檻電影' },
  { id:'g_mid_hard', tier:'中級', type:'電影', req:{ acting:90 }, loc:'film_lion', title:'高門檻電影' },
  { id:'g_var_ok', tier:'初級', type:'綜藝', req:{ stage:20, charm:15 }, loc:'tvb_longmen', title:'綜藝通告' },
  { id:'g_var_hard', tier:'中級', type:'綜藝', req:{ stage:80 }, loc:'tvb_longmen', title:'高台風綜藝' },
  { id:'g_fame_hard', tier:'高級', type:'電影', req:{ acting:10 }, loc:'film_lion', title:'高聲望電影' },
];
const FNS = ['function reqGap','function fameFloor','function gateTrainHint','function canAudition',
  'function intel381MonthKey','function intel381PickGig','function tape383QuarterKey','function tape383PickGig','function v422Auditionable'];
eval(FNS.map(f => extractFn(f)).join('\n'));
function setStats(o){ S = Object.assign({ flags:{}, booked:[], enrolled:{}, fame:0, acting:0, stage:0, vocal:0, looks:0, charm:0, iq:0, stamina:0 }, o); }
/* 未達標：只有低門檻可試鏡（acting 25 過 g_low_ok，聲望 0 擋高級） */
setStats({ acting:25, stage:10, charm:10, fame:0 });
{
  const g = intel381PickGig();
  ok('未達標態：情報派可試鏡通告', !!g && canAudition(g).ok && g.id === 'g_low_ok');
  const t = tape383PickGig('綜藝');
  ok('未達標態：綜藝無可試鏡者回 null（不收費）', t === null);
}
/* 部分達標：中門檻可試鏡，高門檻不可被派中 */
setStats({ acting:45, stage:35, charm:20, fame:20 });
{
  const g = intel381PickGig();
  ok('部分達標態：情報派可試鏡通告', !!g && canAudition(g).ok && reqGap(g).missing === 0);
  const t = tape383PickGig('電影');
  ok('部分達標態：試鏡帶派可試鏡電影', !!t && canAudition(t).ok && t.id !== 'g_mid_hard');
  const tv = tape383PickGig('綜藝');
  ok('部分達標態：試鏡帶派可試鏡綜藝', !!tv && canAudition(tv).ok && tv.id === 'g_var_ok');
}
/* 全未達標（連低門檻都過不了）：回 null */
setStats({ acting:5, stage:5, charm:5, fame:0 });
{
  ok('全未達標態：情報回 null', intel381PickGig() === null);
  ok('全未達標態：試鏡帶回 null', tape383PickGig('電影') === null);
}
/* 已達標：高門檻亦可被派中且可試鏡 */
setStats({ acting:120, stage:100, charm:80, fame:60 });
{
  const g = intel381PickGig();
  ok('已達標態：情報派可試鏡通告', !!g && canAudition(g).ok);
}
console.log(fail === 0 ? 'ALL PASS (' + pass + ')' : 'FAILURES ' + fail + '/' + (pass + fail));
process.exit(fail === 0 ? 0 : 1);
