// v20a229 B8 錯峰／提早窗補充測試（AUDIT229 §6；SPEC §2.2.2／§3.3；DECISIONS D-4）
//   補 B1–B7 gig229 套未覆蓋嘅一環：季節排期提早窗＋NAT92 錯峰真函數（唔係 stub）。
//   之前覆蓋：trigger.js T11 只驗 gigSeasonHidden88 兩個點（1991-09-01 入窗／1991-01-01 未入窗），
//   T4 嘅 gigBoardPosted92 係 stub（錯峰豁免用假函數證）。以下全部用真函數＋真新庫數據：
//   S0 常量：提早窗 GIG_SEASON_LEAD88＝60 日；NAT92_SPREAD＝40、PULL_MAX＝24、PULL_OPEN_MAX＝30
//   S1 提早窗邊界（gigSeasonEarlyVisible88）：1990 秋 gig_1990_film_106，季首 1990-09-01，
//       窗首＝季首−60 日＝1990-07-03（含）可見、1990-07-02 隱；季尾 1990-11-30 可見、1990-12-01 隱
//   S2 gigSeasonHidden88：當季唔藏；錯季未入窗藏；錯季入提早窗唔藏
//   S3 nat92PostIntervals 錨定顯示年：1990 春 gig_1990_film_102 開局已上板（off＝0、post＝0）；
//       1990 冬 gig_1990_film_101 有兩個 interval；1991 秋 gig_1991_film_104 interval 落喺 1991 年
//       dayIndex 365–729，唔係 YEARS66＋2 移後兩年
//   S4 gigBoardPosted92 真函數（S.dayIndex）：秋 gig post 前一日 false、post 當日 true、last 之後 false；
//       冬 gig 兩窗之間（day 300）false、第二窗 post 當日 true
//   S5 全庫掃描 241 張：全部 nat92StaggerEligible；每張喺自己年份內至少有一日上板（唔會永久隱藏）；
//       全部 interval 唔出 [年首−60 日, 年尾]（無＋2 漏移）；off ∈ [0,39]、pull ∈ [0,30]
//   S6 gigReleaseLine88：1990 秋 gig 顯示「1990 年秋季」，唔係 1992 年
// 反證：對 B1 前（舊曆＋walker＋2）index 行 → S3／S5 interval 全部移後兩年 FAIL；
//   對 NAT92_SPREAD 改大／LEAD88 改 30 嘅 index 行 → S0／S1 邊界 FAIL。
// 用法：node tests/test_gig229_stagger.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const ROOT = path.join(__dirname, '..');
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

const pack = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gigs_new.json'), 'utf8'));
const gigs = pack.gigs || [];
const gigById = id => gigs.find(g=>g.id===id);

/* ---------- S0：常量 ---------- */
ok('S0 GIG_SEASON_LEAD88＝60', html.indexOf('const GIG_SEASON_LEAD88 = 60;')>=0);
ok('S0 NAT92_SPREAD＝40／PULL_MAX＝24／PULL_OPEN_MAX＝30',
  html.indexOf('const NAT92_SPREAD = 40;')>=0 && html.indexOf('const NAT92_PULL_MAX = 24;')>=0 &&
  html.indexOf('const NAT92_PULL_OPEN_MAX = 30;')>=0);

/* ---------- eval 沙盒：排期真函數 ---------- */
var S = { dayIndex: 0 };
var dateObj = function(){ return new Date(1990, 0, 1); };
try{
  for(const c of ['START','GIG_SEASON_SPAN88','GIG_SEASON_LEAD88','NAT92_SPREAD','NAT92_PULL_MAX',
    'NAT92_PULL_OPEN_MAX','ROLE_SCALE_BAND','SHOOT_DAYS','DUR90_DAILY','DUR90_OLD_BAND']){
    const src = extractConstVar(c);
    if(!src) ok('抽取 const '+c, false); else eval(src);
  }
  for(const f of ['seasonRank','gigSeasonEarlyVisible88','gigSeasonHidden88','gigReleaseLine88',
    'nat92Hash','nat92DayIdxOf','nat92StaggerEligible','nat92CalNeedDays','nat92PostIntervals',
    'gigBoardPosted92','resolveRoleScale','shootBandFor','effectiveShootDays','effectiveShootWeekdays',
    'effectiveShootDeadlineDays','clamp']){
    const src = extractFn(f);
    if(!src) ok('抽取 function '+f, false); else eval(src);
  }
}catch(e){ ok('S 沙盒抽取 ('+e.message+')', false); }

const autumn90 = gigById('gig_1990_film_106'); /* 1990 秋 */
const winter90 = gigById('gig_1990_film_101'); /* 1990 冬 */
const spring90 = gigById('gig_1990_film_102'); /* 1990 春 */
const autumn91 = gigById('gig_1991_film_104'); /* 1991 秋 */
ok('S 樣本 gig 齊（秋90／冬90／春90／秋91）', !!(autumn90 && winter90 && spring90 && autumn91));

/* ---------- S1：提早窗邊界（秋 1990：季首 1990-09-01，窗首＝季首−60 日＝1990-07-03） ---------- */
try{
  dateObj = function(){ return new Date(1990, 6, 3); }; /* 1990-07-03 窗首當日 */
  ok('S1 窗首當日 1990-07-03 可見', gigSeasonEarlyVisible88(autumn90)===true);
  dateObj = function(){ return new Date(1990, 6, 2); }; /* 1990-07-02 窗首前一日 */
  ok('S1 窗首前一日 1990-07-02 唔可見', gigSeasonEarlyVisible88(autumn90)===false);
  dateObj = function(){ return new Date(1990, 10, 30); }; /* 1990-11-30 季尾當日 */
  ok('S1 季尾當日 1990-11-30 可見', gigSeasonEarlyVisible88(autumn90)===true);
  dateObj = function(){ return new Date(1990, 11, 1); }; /* 1990-12-01 季尾之後 */
  ok('S1 季尾之後 1990-12-01 唔可見', gigSeasonEarlyVisible88(autumn90)===false);
  dateObj = function(){ return new Date(1990, 8, 15); }; /* 1990-09-15 當季 */
  ok('S1 當季 1990-09-15 可見', gigSeasonEarlyVisible88(autumn90)===true);
}catch(e){ ok('S1 提早窗邊界沙盒 ('+e.message+')', false); }

/* ---------- S2：gigSeasonHidden88 ---------- */
try{
  dateObj = function(){ return new Date(1990, 8, 15); };
  ok('S2 當季唔藏', gigSeasonHidden88(autumn90, '秋')===false);
  dateObj = function(){ return new Date(1990, 6, 3); };
  ok('S2 錯季但入提早窗唔藏', gigSeasonHidden88(autumn90, '夏')===false);
  dateObj = function(){ return new Date(1990, 0, 1); };
  ok('S2 錯季未入窗藏', gigSeasonHidden88(autumn90, '冬')===true);
}catch(e){ ok('S2 隱藏判準沙盒 ('+e.message+')', false); }

/* ---------- S3：nat92PostIntervals 錨定顯示年 ---------- */
let ivSpring90, ivWinter90, ivAutumn90, ivAutumn91;
try{
  ivSpring90 = nat92PostIntervals(spring90);
  ivWinter90 = nat92PostIntervals(winter90);
  ivAutumn90 = nat92PostIntervals(autumn90);
  ivAutumn91 = nat92PostIntervals(autumn91);
  ok('S3 1990 春單 interval、開局已上板（off＝0、post＝0）',
    ivSpring90.length===1 && ivSpring90[0].off===0 && ivSpring90[0].post===0,
    JSON.stringify(ivSpring90));
  ok('S3 1990 春 interval 落喺 1990 年內（from 0、to ≤364）',
    ivSpring90[0].from===0 && ivSpring90[0].to<=364);
  ok('S3 1990 冬有兩個 interval（年初窗＋錨定提早窗）', ivWinter90.length===2, JSON.stringify(ivWinter90));
  ok('S3 1990 冬第二窗 post＝309（1990-11-06 前後，唔係移後兩年）',
    ivWinter90[1].post===309 && ivWinter90[1].to===364, JSON.stringify(ivWinter90[1]));
  ok('S3 1991 秋 interval 落喺 1991 年 dayIndex 365–729',
    ivAutumn91[0].from>=365 && ivAutumn91[0].to<=729, JSON.stringify(ivAutumn91));
  ok('S3 1990 秋 interval 落喺 1990 年（from 183＝1990-07-03、to 333＝1990-11-30）',
    ivAutumn90[0].from===183 && ivAutumn90[0].to===333, JSON.stringify(ivAutumn90));
}catch(e){ ok('S3 錯峰 interval 沙盒 ('+e.message+')', false); }

/* ---------- S4：gigBoardPosted92 真函數 ---------- */
try{
  S.dayIndex = 198; /* 秋90 post（199）前一日 */
  ok('S4 秋 gig post 前一日唔上板', gigBoardPosted92(autumn90)===false);
  S.dayIndex = 199; /* post 當日 */
  ok('S4 秋 gig post 當日上板', gigBoardPosted92(autumn90)===true);
  S.dayIndex = 313; /* last（312）之後 */
  ok('S4 秋 gig last 之後落板', gigBoardPosted92(autumn90)===false);
  S.dayIndex = 0; /* 春90 開局 */
  ok('S4 春 gig 開局 day 0 已上板', gigBoardPosted92(spring90)===true);
  S.dayIndex = 300; /* 冬90 兩窗之間 */
  ok('S4 冬 gig 兩窗之間唔上板', gigBoardPosted92(winter90)===false);
  S.dayIndex = 309; /* 冬90 第二窗 post 當日 */
  ok('S4 冬 gig 第二窗 post 當日上板', gigBoardPosted92(winter90)===true);
  S.dayIndex = 352; /* 冬90 第二窗 last（351）之後 */
  ok('S4 冬 gig 第二窗 last 之後落板', gigBoardPosted92(winter90)===false);
}catch(e){ ok('S4 上板判準沙盒 ('+e.message+')', false); }

/* ---------- S5：全庫掃描 ---------- */
try{
  const inelig = gigs.filter(g=>!nat92StaggerEligible(g));
  ok('S5 241 張全部 nat92StaggerEligible', inelig.length===0, inelig.slice(0,3).map(g=>g.id).join(','));
  let noPostDay = [], outOfYear = [], offBad = [], pullBad = [];
  for(const g of gigs){
    const ivs = nat92PostIntervals(g);
    if(!ivs || !ivs.length){ noPostDay.push(g.id); continue; }
    const yStart = nat92DayIdxOf(g.year, 1, 1), yEnd = nat92DayIdxOf(g.year, 12, 31);
    let hasDay = false;
    for(const iv of ivs){
      if(iv.post<=yEnd && iv.last>=yStart) hasDay = true;
      if(iv.from < yStart-60 || iv.to > yEnd) outOfYear.push(g.id);
      if(!(iv.off>=0 && iv.off<=39)) offBad.push(g.id+':off='+iv.off);
      if(!(iv.pull>=0 && iv.pull<=30)) pullBad.push(g.id+':pull='+iv.pull);
    }
    if(!hasDay) noPostDay.push(g.id);
  }
  ok('S5 每張喺自己年份內至少有一日上板（唔會永久隱藏）', noPostDay.length===0, noPostDay.slice(0,5).join(','));
  ok('S5 全部 interval 唔出 [年首−60 日, 年尾]（無＋2 漏移）', outOfYear.length===0, outOfYear.slice(0,5).join(','));
  ok('S5 off 全部 ∈ [0,39]', offBad.length===0, offBad.slice(0,3).join(','));
  ok('S5 pull 全部 ∈ [0,30]', pullBad.length===0, pullBad.slice(0,3).join(','));
}catch(e){ ok('S5 全庫掃描沙盒 ('+e.message+')', false); }

/* ---------- S6：上映行顯示年 ---------- */
try{
  ok('S6 gigReleaseLine88 顯示 1990 年秋季（唔係 1992 年）',
    gigReleaseLine88(autumn90)==='預計上映：1990 年秋季', gigReleaseLine88(autumn90));
  ok('S6 gigReleaseLine88 1991 秋顯示 1991 年秋季',
    gigReleaseLine88(autumn91)==='預計上映：1991 年秋季', gigReleaseLine88(autumn91));
}catch(e){ ok('S6 上映行沙盒 ('+e.message+')', false); }

console.log(fails.length ? ('\nGIG229 STAGGER: '+fails.length+' FAIL') : '\nGIG229 STAGGER: ALL PASS');
process.exit(fails.length ? 1 : 0);
