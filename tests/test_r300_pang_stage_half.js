// v20a300 Q13：彭少祺人情渠道司儀通告台風要求減半（ceil）
//   減半表：15→8、25→13、30→15、45→23、80→40；只適用於經彭渠道入場嗰陣，
//   庫 req／charm／聲望 floor／其他硬閘唔郁；武指渠道唔郁。
//   用真 canAudition（非 stub）驗資格，mock S 直接設數值。
// 用法：node tests/test_r300_pang_stage_half.js [path-to-index.html]
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

/* ---------- stubs：soft 閘一律放行，lifecycle 一律未開始 ---------- */
var S = null;
var GIGS = gigs;
var COURSE_DEFS = {};
var isGigInProduction = function(){ return false; };
var softCastingTagGate = function(){ return null; };
var softIndustryCreditGate = function(){ return null; };
var softOverdueFavorDebtLock = function(){ return null; };
var costume265EffStat = function(k){ return (S && S[k]) || 0; };

/* ---------- 抽真函數 ---------- */
eval(extractConstVar('GIG_REQ_KEYS88'));
eval(extractConstVar('FAVOR158_MAK_CREDIT_ID'));
eval(extractConstVar('FAVOR158_PANG_CREDIT_ID'));
eval(extractFn('isGigWrapped'));
eval(extractFn('fameFloor'));
eval(extractFn('reqGap'));
eval(extractFn('gateTrainHint'));
eval(extractFn('canAudition'));
eval(extractFn('favor158CreditHeld'));
eval(extractFn('isMakWuzhiGig158'));
eval(extractFn('isPangCharityGig158'));
eval(extractFn('pangHalvedStageReq158'));
eval(extractFn('pangEffectiveGig158'));
eval(extractFn('pangChannelReady158'));
eval(extractFn('favor158ChannelForGig'));
eval(extractFn('favor158ChannelHintHtml'));

const PANG_IDS = ['gig_1990_variety_101','gig_1990_variety_105','gig_1991_variety_104','gig_1991_variety_103','gig_1992_variety_102'];
const HALVED = { 'gig_1990_variety_101':8, 'gig_1990_variety_105':13, 'gig_1991_variety_104':15, 'gig_1991_variety_103':23, 'gig_1992_variety_102':40 };

function freshS(stats){
  S = { dayIndex:10, flags:{}, enrolled:{}, mockCredits:[], shoots:[], pendingAud:[], booked:[], board:{},
        fame:5, acting:18, stage:14, vocal:14, looks:22, charm:16, iq:20, stamina:75 };
  if(stats) Object.assign(S, stats);
  return S;
}
function givePangCredit(){
  S.mockCredits.push({ id:'credit_enc84_pang_charity', debtor:'彭少祺', title:'test', line:'test line', status:'未收' });
}
function giveMakCredit(){
  S.mockCredits.push({ id:'credit_enc79_mak_wuzhi', debtor:'紅棉武指', title:'test', line:'test line', status:'未收' });
}

/* ---------- A：減半表（ceil） ---------- */
PANG_IDS.forEach(id=>{
  const g = gigById(id);
  ok('A 減半表 ' + id + ' stage ' + g.req.stage + '→' + HALVED[id], pangHalvedStageReq158(g)===HALVED[id]);
});
ok('A 冇 stage req → 0', pangHalvedStageReq158({ req:{} })===0 && pangHalvedStageReq158(null)===0);

/* ---------- B：effective gig 只改 stage，唔郁原 gig ---------- */
(function(){
  const g = gigById('gig_1990_variety_101');
  const eff = pangEffectiveGig158(g);
  ok('B effective gig stage 減半', eff.req.stage===8);
  ok('B effective gig charm／tier／id 照舊', eff.req.charm===12 && eff.tier===g.tier && eff.id===g.id);
  ok('B 原 gig 唔郁', g.req.stage===15);
})();

/* ---------- C：開局邊界——台風 14 過到最低嗰張 ---------- */
freshS({ stage:14, charm:16, fame:5 }); givePangCredit();
(function(){
  const g = gigById('gig_1990_variety_101');
  ok('C 開局 canAudition 全數唔過（stage 14 < 15）', canAudition(g).ok===false);
  const ch = favor158ChannelForGig(g);
  ok('C 開局有彭債權→渠道開到', !!ch && ch.creditId==='credit_enc84_pang_charity' && ch.shortLabel==='慈善騷頂班', JSON.stringify(ch));
  ok('C 提示寫明台風要求 15→8', !!ch && ch.hint.indexOf('台風要求 15→8')>=0, ch && ch.hint);
  ok('C 提示行金色＋講明免試鏡', favor158ChannelHintHtml(g).indexOf('class="gold"')>=0 && favor158ChannelHintHtml(g).indexOf('無須試鏡')>=0);
})();

/* ---------- D：冇債權→冇渠道 ---------- */
freshS({ stage:14, charm:16, fame:5 });
ok('D 冇債權→冇渠道', favor158ChannelForGig(gigById('gig_1990_variety_101'))===null);
ok('D 冇債權→提示行空', favor158ChannelHintHtml(gigById('gig_1990_variety_101'))==="");

/* ---------- E：減半邊界——7 唔過、8 過 ---------- */
freshS({ stage:7, charm:16, fame:5 }); givePangCredit();
ok('E 台風 7（減半要 8）→冇渠道', favor158ChannelForGig(gigById('gig_1990_variety_101'))===null);
freshS({ stage:8, charm:16, fame:5 }); givePangCredit();
ok('E 台風 8（剛好減半數）→有渠道', !!favor158ChannelForGig(gigById('gig_1990_variety_101')));

/* ---------- F：charm 閘唔郁 ---------- */
freshS({ stage:14, charm:11, fame:5 }); givePangCredit();
ok('F charm 11（要 12）→冇渠道', favor158ChannelForGig(gigById('gig_1990_variety_101'))===null);

/* ---------- G：聲望 floor 唔郁 ---------- */
freshS({ stage:30, charm:30, fame:5 }); givePangCredit();
ok('G 中級 floor 16、聲望 5 →冇渠道', favor158ChannelForGig(gigById('gig_1991_variety_103'))===null);
freshS({ stage:30, charm:30, fame:16 }); givePangCredit();
ok('G 聲望 16 過 floor、台風 30 過減半 23 →有渠道', !!favor158ChannelForGig(gigById('gig_1991_variety_103')));

/* ---------- H：五張掃描 ---------- */
freshS({ stage:40, charm:55, fame:32 }); givePangCredit();
ok('H 台風 40／charm 55／聲望 32 → 5 張全開', PANG_IDS.every(id=>!!favor158ChannelForGig(gigById(id))), PANG_IDS.map(id=>id+':'+!!favor158ChannelForGig(gigById(id))).join(','));
freshS({ stage:14, charm:16, fame:5 }); givePangCredit();
ok('H 開局 → 淨係最低嗰張開到', PANG_IDS.filter(id=>!!favor158ChannelForGig(gigById(id))).join(',')==='gig_1990_variety_101');
freshS({ stage:39, charm:55, fame:32 }); givePangCredit();
ok('H 台風 39（減半要 40）→最高嗰張唔開', favor158ChannelForGig(gigById('gig_1992_variety_102'))===null);
freshS({ stage:40, charm:55, fame:32 }); givePangCredit();
ok('H 台風 40（剛好減半數）→最高嗰張開到，提示 80→40', (function(){ const ch=favor158ChannelForGig(gigById('gig_1992_variety_102')); return !!ch && ch.hint.indexOf('台風要求 80→40')>=0; })());

/* ---------- I：武指渠道唔郁（全數過關先提供） ---------- */
(function(){
  const MAK_GIG = gigById('gig_1991_film_108');
  freshS({ stage:0, charm:0, fame:0 }); giveMakCredit();
  ok('I 武指：全數唔過→冇渠道', favor158ChannelForGig(MAK_GIG)===null);
  freshS({ stage:99, charm:99, fame:99, acting:99, vocal:99, looks:99, iq:99, stamina:99 }); giveMakCredit();
  const ch = favor158ChannelForGig(MAK_GIG);
  ok('I 武指：全數過→有渠道', !!ch && ch.shortLabel==='武指照應');
  ok('I 武指提示唔講台風減半', !!ch && ch.hint.indexOf('台風要求')<0);
})();

/* ---------- J：唔係主持→唔入彭渠道 ---------- */
freshS({ stage:99, charm:99, fame:99, acting:99, vocal:99, looks:99, iq:99, stamina:99 }); givePangCredit();
ok('J 歌唱比賽參賽者（綜藝但唔係主持）→冇彭渠道', favor158ChannelForGig(gigById('gig_1990_variety_102'))===null);
ok('J 電影／唱片→冇彭渠道', favor158ChannelForGig(gigById('gig_1991_film_108'))===null && favor158ChannelForGig(gigById('gig_1991_rec_107'))===null);

/* ---------- K：pangChannelReady158 直接斷言 ---------- */
freshS({ stage:14, charm:16, fame:5 }); givePangCredit();
ok('K ready：開局＋債權→101 ready', pangChannelReady158(gigById('gig_1990_variety_101'))===true);
ok('K ready：開局＋債權→105 唔 ready（要 13）', pangChannelReady158(gigById('gig_1990_variety_105'))===false);
freshS({ stage:14, charm:16, fame:5 });
ok('K ready：冇債權→唔 ready', pangChannelReady158(gigById('gig_1990_variety_101'))===false);

/* ---------- L：詳情頁鎖定分支＋註解（靜態） ---------- */
(function(){
  const detailSrc = extractFn('openCastingNoticeDetail');
  ok('L 詳情頁函數在位', !!detailSrc);
  ok('L 鎖定分支有彭渠道掣（ch158Locked）', !!detailSrc && detailSrc.indexOf('ch158Locked')>=0);
  ok('L 鎖定分支有「用人情免試鏡」掣', !!detailSrc && detailSrc.indexOf('用人情免試鏡')>=0);
  ok('L v20a158 頭註解已改「台風放寬」已定', html.indexOf('「台風放寬」已定')>=0 && html.indexOf('「台風放寬」未定')<0);
  ok('L 庫 req 唔郁：5 張原 stage 要求不變', PANG_IDS.every(id=>{ const g=gigById(id); return g.req.stage===({ 'gig_1990_variety_101':15, 'gig_1990_variety_105':25, 'gig_1991_variety_104':30, 'gig_1991_variety_103':45, 'gig_1992_variety_102':80 })[id]; }));
})();

console.log(fails.length ? ('FAILURES: '+fails.length+' :: '+fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
