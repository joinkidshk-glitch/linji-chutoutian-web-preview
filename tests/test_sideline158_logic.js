// v20a158 人情免試鏡渠道＋支線抉擇即派測試（G-M1 武指照應／G-PANG-1 彭慈善／GRANT229_ENC79 加 8 行）
//   T1 兩條渠道 matcher：武打＝genre 動作／武俠＋category 作品（新庫 22 張；臨記散工唔入，
//       例 gig_1990_film_206 碼頭搬運）；司儀＝type 綜藝＋roleLabel 含「主持」（新庫 5 張）
//   T2 渠道供應條件：持有未兌現債權＋啱類別＋canAudition ok 先有（彭渠道 v20a300 起用減半台風計
//       canAudition，見 test_r300；呢度 stub canAudition，減半行為由新測試覆蓋）；冇債權／已兌現／絕響／
//       閘未過／錯類別 → 冇；金色提示行只喺有渠道嗰陣出
//   T3 兌現一次即清：用咗→ pending ok:true、revealDay 翌日（即日＋1）、via favor158；債權 redeemedBy＋
//       「已兌現」字句＋syncNotebookMirror；第二次唔再提供；通告落板
//   T4 彭渠道兌現（司儀通告，同一模式）
//   T5 守衛：已等緊消息同一張／等消息滿 3 張／閘未過 → 唔兌現，債權原封不動
//   T6 聽朝晨鏈呈現：revealDay 翌日（即日＋1）嘅 pending 翌日 aud91PresentDue 出何生電話，
//       簽約金＝片酬 30% 即付、shoot.signedPaid＝簽約金、modal 講明免試鏡直接獲聘
//   T7 GRANT229_ENC79 加 8 行：逐行 seg＋key（live 選項 label）→gig，8 張 id 喺新庫存在、
//       兩兩唔同、唔撞 CHOICE／BR89／DRAFT／原有 9 行；liu_repay 無匹配 label→唔派；
//       gu_loan 唔借→兜底 rec_106；全表 17 行
//   T8 BR89 13 對原封不動
//   T9 靜態：渠道函數／接線字句在位；aud91CreatePending 舊路徑（無 revealDay）照行 2–4 日等待
// 用法：node tests/test_sideline158_logic.js [path-to-index.html]
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

/* ---------- stubs ---------- */
var S = null;
var GIGS = gigs;
var canAuditionResult = { ok:true };
var canAudition = function(gig){ return canAuditionResult; };
var R = function(lo, hi){ return lo; }; /* 確定性：永遠取下限 */
var shootSpanFor = function(g){ return (g && typeof g.days==="number") ? g.days : 0; };
var rollAuditionPay = function(g){ const p = gigPayExact(g); return { pay:p, note:"", basePay:p, bonusPay:0, bonusLabel:"" }; };
var saveQ = function(){};
var syncMirrorCalls = 0;
var syncNotebookMirror = function(){ syncMirrorCalls++; };
var clearJobCalls = 0;
var clearJobFromPlans = function(id){ clearJobCalls++; };
var doScoutCalls = 0;
var doScout = function(L){ doScoutCalls++; };
var openDetailCalls = 0;
var openCastingNoticeDetail = function(g, L){ openDetailCalls++; };
var lastModal = null, modalCalls = 0;
var modal = function(h, btns, opts){ lastModal = { html:h, btns:btns||[], opts:opts }; modalCalls++; };
var lastToast = null;
var toast = function(t){ lastToast = t; };
var paintBar = function(){};
var drawMap = function(){};
var fmtDate = function(){ return "1990-01-02"; };
var chk101Html = function(o){ return "<CHK101 amount="+o.amount+">"; };
var weekdayIdx = function(d){ return 0; };
var ending78Locked = function(){ return false; };
var _aud91Presenting = false;
var apply = function(o){ if(o && typeof o.money==="number"){ S.money=(S.money||0)+o.money; if(o.money>0) S.weekEarn=(S.weekEarn||0)+o.money; } return []; };
var scheduleShoot = function(gig, pay, fame, pop, payBreak){
  const sh = { id:"sh_test_"+gig.id, gigId:gig.id, title:gig.title, type:gig.type,
    totalDays:(typeof gig.days==="number"?gig.days:0), daysLeft:(typeof gig.days==="number"?gig.days:0),
    doneDays:0, pay:pay, fame:fame, popularity:pop, locId:gig.locId||null, signedPaid:0 };
  S.shoots.push(sh);
  return sh;
};
var confirmPlaceShoot = function(shoot, weekday, thenFn){ if(typeof thenFn==="function") thenFn(); };
var eventLine = function(k, o){ return ""; };
var formatResultNotes = function(notes){ return (notes||[]).join(""); };
var phase3CastCopy = function(){ return { successToast:"獲聘", readyLabel:"接通告", lockedLabel:"未能報名", leaveLabel:"離開" }; };
var softPreviewOn = function(){ return false; };
var maybeShowTutToast = function(){ const a=[...arguments]; const cb=a[a.length-1]; if(typeof cb==="function") cb(); };

function freshS(day){
  S = { dayIndex:(day==null?10:day), flags:{}, grant229Queue:[], contracts229:[],
        shoots:[], pendingAud:[], booked:[], board:{}, money:12000, weekEarn:0,
        mockCredits:[], aud91Log:[], fame:5 };
  canAuditionResult = { ok:true };
  syncMirrorCalls = 0; clearJobCalls = 0; doScoutCalls = 0; openDetailCalls = 0;
  modalCalls = 0; lastModal = null; lastToast = null;
  return S;
}
function giveCredit(id, debtor){
  S.mockCredits.push({ id:id, debtor:debtor, title:"test", line:"test line", status:"未收" });
  return S.mockCredits[S.mockCredits.length-1];
}
freshS();

/* ---------- 抽 v20a158＋相依真函數 ---------- */
eval(extractConstVar('AUD91_CAP'));
eval(extractConstVar('GRANT229_CHOICE'));
eval(extractConstVar('GRANT229_ENC79'));
eval(extractConstVar('GRANT229_DRAFT'));
eval(extractConstVar('CONTRACT229_GIGS'));
eval(extractConstVar('BR89_PATRON_OF_GIG'));
eval(extractConstVar('FAVOR158_MAK_CREDIT_ID'));
eval(extractConstVar('FAVOR158_PANG_CREDIT_ID'));
eval(extractFn('grant229Ensure'));
eval(extractFn('grant229GigById'));
eval(extractFn('grant229Record'));
eval(extractFn('grant229RecordFromEnc79'));
eval(extractFn('grant229RecordDraft'));
eval(extractFn('grant229DueList'));
eval(extractFn('grant229IsConsumed'));
eval(extractFn('grant229Drop'));
eval(extractFn('gigPayExact'));
eval(extractFn('aud91Ensure'));
eval(extractFn('aud91PendingOf'));
eval(extractFn('aud91WaitDays'));
eval(extractFn('aud91CreatePending'));
eval(extractFn('aud91PendingHint'));
eval(extractFn('aud91LogPush'));
eval(extractFn('aud91DueList'));
eval(extractFn('aud91PresentDue'));
eval(extractFn('aud91PresentOne'));
eval(extractFn('favor158CreditHeld'));
eval(extractFn('isMakWuzhiGig158'));
eval(extractFn('isPangCharityGig158'));
eval(extractFn('favor158ChannelForGig'));
eval(extractFn('favor158ChannelHintHtml'));
/* v20a300 Q13：彭渠道台風減半——favor158ChannelForGig 依賴呢三個，唔抽會 ReferenceError。 */
eval(extractFn('pangHalvedStageReq158'));
eval(extractFn('pangEffectiveGig158'));
eval(extractFn('pangChannelReady158'));
eval(extractFn('favor158SpendCredit'));
eval(extractFn('favor158UseChannel'));
eval(extractFn('favor158RedeemChannel'));

/* ---------- T1：matcher ---------- */
const makMatches = gigs.filter(isMakWuzhiGig158);
ok('T1 武打 matcher：新庫 22 張（動作／武俠＋作品）', makMatches.length===22, makMatches.map(g=>g.id).join(','));
ok('T1 武打 matcher：gig_1990_film_206 碼頭搬運（臨記通告）唔入', !isMakWuzhiGig158(gigById('gig_1990_film_206')));
ok('T1 武打 matcher：臨記動作替身 film_211／213／214 唔入', ['gig_1990_film_211','gig_1990_film_213','gig_1990_film_214'].every(id=>!isMakWuzhiGig158(gigById(id))));
ok('T1 武打 matcher：電視動作 tv_102 入', isMakWuzhiGig158(gigById('gig_1990_tv_102')));
ok('T1 武打 matcher：喜劇／文藝唔入', !isMakWuzhiGig158(gigById('gig_1991_film_109')) && !isMakWuzhiGig158(gigById('gig_1991_film_103')));
const pangMatches = gigs.filter(isPangCharityGig158);
ok('T1 司儀 matcher：新庫 5 張', pangMatches.length===5, pangMatches.map(g=>g.id).join(','));
ok('T1 司儀 matcher：5 張正係 task 列嗰 5 張',
  ['gig_1990_variety_101','gig_1990_variety_105','gig_1991_variety_103','gig_1991_variety_104','gig_1992_variety_102']
    .every(id=>pangMatches.some(g=>g.id===id)));
ok('T1 司儀 matcher：嘉賓／參賽者／伴舞唔入',
  !isPangCharityGig158(gigById('gig_1990_variety_102')) && !isPangCharityGig158(gigById('gig_1991_variety_109')) &&
  !isPangCharityGig158(gigById('gig_1992_variety_103')) && !isPangCharityGig158(gigById('gig_1990_variety_201')));
ok('T1 司儀 matcher：電影／唱片唔入', !isPangCharityGig158(gigById('gig_1991_film_108')) && !isPangCharityGig158(gigById('gig_1991_rec_107')));

/* ---------- T2：渠道供應條件 ---------- */
const MAK_GIG = gigById('gig_1991_film_108'); /* 《月夜酒廊》男配角，動作＋作品 */
const PANG_GIG = gigById('gig_1991_variety_103'); /* 《樂善之夜》慈善晚會主持 */
freshS(10);
ok('T2 無債權→冇渠道', favor158ChannelForGig(MAK_GIG)===null && favor158ChannelForGig(PANG_GIG)===null);
ok('T2 無債權→提示行空', favor158ChannelHintHtml(MAK_GIG)==="" && favor158ChannelHintHtml(PANG_GIG)==="");
freshS(10);
giveCredit('credit_enc79_mak_wuzhi', '紅棉武指');
let ch = favor158ChannelForGig(MAK_GIG);
ok('T2 有武指債權＋武打通告→渠道（creditId／debtor 齊）',
  ch && ch.creditId==='credit_enc79_mak_wuzhi' && ch.debtor==='紅棉武指' && ch.shortLabel==='武指照應', JSON.stringify(ch));
ok('T2 武指渠道唔適用喺司儀通告', favor158ChannelForGig(PANG_GIG)===null);
ok('T2 武指渠道提示行係金色＋講明免試鏡',
  favor158ChannelHintHtml(MAK_GIG).indexOf('class="gold"')>=0 && favor158ChannelHintHtml(MAK_GIG).indexOf('無須試鏡')>=0);
freshS(10);
giveCredit('credit_enc84_pang_charity', '彭少祺');
ch = favor158ChannelForGig(PANG_GIG);
ok('T2 有彭債權＋司儀通告→渠道（creditId／debtor 齊）',
  ch && ch.creditId==='credit_enc84_pang_charity' && ch.debtor==='彭少祺' && ch.shortLabel==='慈善騷頂班', JSON.stringify(ch));
ok('T2 彭渠道唔適用喺武打通告', favor158ChannelForGig(MAK_GIG)===null);
ok('T2 彭渠道提示行係金色＋講明免試鏡',
  favor158ChannelHintHtml(PANG_GIG).indexOf('class="gold"')>=0 && favor158ChannelHintHtml(PANG_GIG).indexOf('無須試鏡')>=0);
freshS(10);
giveCredit('credit_enc79_mak_wuzhi', '紅棉武指');
S.mockCredits[0].redeemedBy = 'gig_1991_film_110';
ok('T2 已兌現債權→冇渠道', favor158ChannelForGig(MAK_GIG)===null);
freshS(10);
giveCredit('credit_enc79_mak_wuzhi', '紅棉武指');
S.mockCredits[0].status = '絕響';
ok('T2 絕響債權→冇渠道', favor158ChannelForGig(MAK_GIG)===null);
freshS(10);
giveCredit('credit_enc79_mak_wuzhi', '紅棉武指');
canAuditionResult = { ok:false, reason:"聲望未合" };
ok('T2 canAudition 未過→冇渠道（唔繞過硬閘）', favor158ChannelForGig(MAK_GIG)===null);
freshS(10);
giveCredit('credit_enc79_mak_wuzhi', '紅棉武指');
ok('T2 錯類別（喜劇作品）→冇渠道', favor158ChannelForGig(gigById('gig_1991_film_109'))===null);

/* ---------- T3：武指兌現一次即清 ---------- */
freshS(10);
const makCredit = giveCredit('credit_enc79_mak_wuzhi', '紅棉武指');
S.board = { film_harbour:[MAK_GIG.id, 'gig_1990_film_206'] };
ok('T3 兌現成功', favor158RedeemChannel(MAK_GIG, { id:'film_harbour' })===true);
const rec3 = S.pendingAud[0];
ok('T3 pending 一筆 ok:true、p=1（chancePct 100）', S.pendingAud.length===1 && rec3.ok===true && rec3.chancePct===100, JSON.stringify(rec3));
ok('T3 pending revealDay 翌日（＝用嗰日 dayIndex 10＋1）、wait 1', rec3.revealDay===11 && rec3.wait===1);
ok('T3 pending via favor158＋favorLabel 紅棉武指', rec3.via==='favor158' && rec3.favorLabel==='紅棉武指');
ok('T3 pending 片酬＝rollAuditionPay（中位數）', rec3.pay===gigPayExact(MAK_GIG) && rec3.pay>0, 'pay='+rec3.pay);
ok('T3 債權已兌現（redeemedBy＝gig id）', makCredit.redeemedBy===MAK_GIG.id);
ok('T3 債權 line 附加「已兌現」字句', makCredit.line.indexOf('已兌現')>=0 && makCredit.line.indexOf('月夜酒廊')>=0, makCredit.line);
ok('T3 兌現有 syncNotebookMirror', syncMirrorCalls>=1);
ok('T3 通告落板（board 剔走，隔籬嗰張留返）', S.board.film_harbour.length===1 && S.board.film_harbour[0]==='gig_1990_film_206');
ok('T3 兌現後唔再提供渠道', favor158ChannelForGig(MAK_GIG)===null && favor158ChannelHintHtml(MAK_GIG)==="");
ok('T3 第二次兌現→false，pending 唔會多一筆', favor158RedeemChannel(MAK_GIG, { id:'film_harbour' })===false && S.pendingAud.length===1);
ok('T3 兌現 modal 講明聽朝何生打嚟＋簽約金到時入帳',
  lastModal && lastModal.html.indexOf('聽朝何生會打嚟')>=0 && lastModal.html.indexOf('簽約金')>=0);
ok('T3 等消息提示行唔講「試鏡咗幾多日」', aud91PendingHint(rec3).indexOf('試鏡咗')<0 && aud91PendingHint(rec3).indexOf('免試鏡')>=0, aud91PendingHint(rec3));

/* ---------- T4：彭渠道兌現 ---------- */
freshS(10);
const pangCredit = giveCredit('credit_enc84_pang_charity', '彭少祺');
S.board = { tv_station:[PANG_GIG.id] };
ok('T4 彭兌現成功', favor158RedeemChannel(PANG_GIG, { id:'tv_station' })===true);
const rec4 = S.pendingAud[0];
ok('T4 彭 pending ok:true、revealDay 翌日、via favor158', rec4.ok===true && rec4.revealDay===11 && rec4.via==='favor158' && rec4.favorLabel==='彭少祺');
ok('T4 彭債權已兌現', pangCredit.redeemedBy===PANG_GIG.id && pangCredit.line.indexOf('已兌現')>=0);
ok('T4 彭兌現後唔再提供', favor158ChannelForGig(PANG_GIG)===null);

/* ---------- T5：守衛 ---------- */
freshS(10);
giveCredit('credit_enc79_mak_wuzhi', '紅棉武指');
S.pendingAud.push({ gigId:MAK_GIG.id, ok:false, revealDay:12 });
ok('T5 已等緊消息同一張→唔兌現，債權原封不動',
  favor158RedeemChannel(MAK_GIG, null)===false && S.pendingAud.length===1 && !S.mockCredits[0].redeemedBy);
freshS(10);
giveCredit('credit_enc79_mak_wuzhi', '紅棉武指');
S.pendingAud.push({ gigId:'gig_1990_film_201' }, { gigId:'gig_1990_film_202' }, { gigId:'gig_1990_tv_201' });
ok('T5 等消息滿 3 張→唔兌現，債權原封不動',
  favor158RedeemChannel(MAK_GIG, null)===false && S.pendingAud.length===3 && !S.mockCredits[0].redeemedBy);
freshS(10);
giveCredit('credit_enc79_mak_wuzhi', '紅棉武指');
canAuditionResult = { ok:false, reason:"聲望未合" };
ok('T5 閘未過→唔兌現，債權原封不動',
  favor158RedeemChannel(MAK_GIG, null)===false && S.pendingAud.length===0 && !S.mockCredits[0].redeemedBy);
freshS(10);
ok('T5 無債權→唔兌現', favor158RedeemChannel(MAK_GIG, null)===false && S.pendingAud.length===0);

/* ---------- T3b：確認 modal（用／取消） ---------- */
freshS(10);
giveCredit('credit_enc79_mak_wuzhi', '紅棉武指');
ok('T3b 用渠道先出確認 modal', favor158UseChannel(MAK_GIG, { id:'film_harbour' })===true && modalCalls===1 &&
  lastModal.html.indexOf('用人情免試鏡')>=0 && lastModal.html.indexOf('確認使用')<0);
ok('T3b 確認 modal 有確認／取消兩掣', lastModal.btns.length===2 && lastModal.btns[0].label==='確認使用' && lastModal.btns[1].label==='取消');
lastModal.btns[0].on(); /* 確認 */
ok('T3b 撳確認→兌現（pending 一筆＋債權已兌現）', S.pendingAud.length===1 && S.mockCredits[0].redeemedBy===MAK_GIG.id);
freshS(10);
giveCredit('credit_enc79_mak_wuzhi', '紅棉武指');
favor158UseChannel(MAK_GIG, { id:'film_harbour' });
lastModal.btns[1].on(); /* 取消 */
ok('T3b 撳取消→唔兌現（pending 空＋債權未動）＋返詳情頁', S.pendingAud.length===0 && !S.mockCredits[0].redeemedBy && openDetailCalls===1);
freshS(10);
ok('T3b 無渠道→用唔到（唔出確認 modal）', favor158UseChannel(MAK_GIG, null)===false && modalCalls===0);

/* ---------- T6：聽朝晨鏈呈現（直接獲聘＋簽約金） ---------- */
freshS(10);
giveCredit('credit_enc79_mak_wuzhi', '紅棉武指');
favor158RedeemChannel(MAK_GIG, null);
const pay6 = S.pendingAud[0].pay;
const sign6 = Math.round(pay6*0.3);
ok('T6 用嗰日 dueList 未有（revealDay 翌日，嚴格第二朝先出）', aud91DueList().length===0);
S.dayIndex = 11; /* 翌日 */
ok('T6 翌日 dueList 有', aud91DueList().length===1);
let step6 = 0;
modalCalls = 0; lastModal = null;
const presented6 = aud91PresentDue(()=>{ step6++; });
if(lastModal && lastModal.btns[0] && typeof lastModal.btns[0].on==="function") lastModal.btns[0].on(); /* 撳「好」續行晨鏈 */
ok('T6 翌日晨鏈呈現', presented6===true && step6===1);
ok('T6 呈現 modal 講明免試鏡直接獲聘（唔係「開完會」）',
  lastModal && lastModal.html.indexOf('免試鏡直接獲聘')>=0 && lastModal.html.indexOf('開完會')<0, lastModal && lastModal.html.slice(0, 200));
ok('T6 呈現 modal 何生嗰句講明紅棉武指應承咗',
  lastModal && lastModal.html.indexOf('紅棉武指嗰邊應承咗，直接用你，唔使試鏡')>=0);
ok('T6 簽約金三成已入帳', S.money===12000+sign6 && S.weekEarn===sign6, 'money='+S.money+' sign='+sign6);
ok('T6 shoot 入行程（signedPaid＝簽約金）', S.shoots.length===1 && S.shoots[0].gigId===MAK_GIG.id && S.shoots[0].signedPaid===sign6);
ok('T6 呈現後 pending 清走', S.pendingAud.length===0);

/* ---------- T7：GRANT229_ENC79 加 8 行 ---------- */
ok('T7 全表 74 行（原 17＋v20a278 六線 57）', GRANT229_ENC79.length===74, 'n='+GRANT229_ENC79.length);
const NEW8 = [
  ['beat:gu_n10after', '恭喜他，終於上岸', 'gig_1992_rec_103'],
  ['beat:gu_n10after', '提醒他以後不要再碰賭', 'gig_1992_rec_104'],
  ['beat:gu_loan', '借，一口應承', 'gig_1991_rec_107'],
  ['beat:gu_loan', '借一半，留一些給自己', 'gig_1991_rec_104'],
  ['beat:gu_loan', '不借，這筆錢我真的幫不了', 'gig_1991_rec_106'],
  ['beat:mak_respect', '應承隨時候命', 'gig_1991_film_108'],
  ['beat:mak_respect', '老實講自己會驚', 'gig_1992_film_107'],
  ['beat:liu_repay', '推辭講自己排緊期', 'gig_1991_film_109']
];
NEW8.forEach(c=>{
  freshS(10);
  const r = grant229RecordFromEnc79(c[0], c[1]);
  ok('T7 即派 ' + c[0] + '／' + c[1] + '→' + c[2],
    r===true && S.grant229Queue.length===1 && S.grant229Queue[0].gigId===c[2] && S.grant229Queue[0].dueDay===11,
    JSON.stringify(S.grant229Queue[0]));
});
ok('T7 8 張 id 全部喺新庫', NEW8.every(c=>!!gigById(c[2])));
ok('T7 8 張 id 兩兩唔同', new Set(NEW8.map(c=>c[2])).size===8);
ok('T7 8 張唔撞 GRANT229_CHOICE', NEW8.every(c=>!Object.values(GRANT229_CHOICE).some(v=>v.gigId===c[2])));
ok('T7 8 張唔撞 BR89 14 對', NEW8.every(c=>!Object.keys(BR89_PATRON_OF_GIG).some(id=>id===c[2])));
ok('T7 8 張唔撞 GRANT229_DRAFT', NEW8.every(c=>!Object.values(GRANT229_DRAFT).some(v=>v.gigId===c[2])));
ok('T7 8 張唔撞原有 ENC79 9 行',
  NEW8.every(c=>!GRANT229_ENC79.slice(0,9).some(r=>r.gigId===c[2])));
ok('T7 第 7 行係 1992《劍氣長虹》唔係 1991《沙田夜巡》（N11_b 目標）',
  gigById('gig_1992_film_107').title.indexOf('劍氣長虹')>=0 && gigById('gig_1991_film_107').title.indexOf('沙田夜巡')>=0);
ok('T7 第 6／8 行 gig 本身已有 trigger（即派唔理，唔郁）',
  gigById('gig_1991_film_108').trigger && gigById('gig_1991_film_108').trigger.creditId==='credit_c9_crew' &&
  gigById('gig_1991_film_109').trigger && gigById('gig_1991_film_109').trigger.creditId==='credit_enc83_liu_patron');
freshS(10);
ok('T7 liu_repay「多謝受落」→唔派（只此一行，唔設兜底）',
  grant229RecordFromEnc79('beat:liu_repay', '多謝受落')===false && S.grant229Queue.length===0);
freshS(10);
ok('T7 gu_n10after 兜底？無空 key 行→唔派',
  grant229RecordFromEnc79('beat:gu_n10after', '唔知講咩')===false && S.grant229Queue.length===0);
ok('T7 新 8 行 reason 全部有實際對位 gig 標題',
  GRANT229_ENC79.slice(9, 17).every(r=>{ const g=gigById(r.gigId); return g && r.reason.indexOf(g.title)>=0; }));
ok('T7 顧 Beat 2 DRAFT 兩行繼續 dormant（唔經初遇 hook 觸發）',
  Object.keys(GRANT229_DRAFT).length===2 && GRANT229_DRAFT.gu_promise_clean.gigId==='gig_1991_rec_201' &&
  GRANT229_DRAFT.gu_ask_back.gigId==='gig_1991_rec_207');

/* ---------- T8：BR89 13 對（v20a274 取代後） ---------- */
const BR89_EXPECTED = {
  gig_1991_film_101:"credit_enc83_luk_patron", gig_1991_variety_203:"credit_enc84_pang_patron",
  gig_1992_rec_106:"credit_enc84_ching_patron", gig_1991_film_103:"credit_enc79_liu_priority",
  gig_1992_film_103:"credit_enc83_liu_patron", gig_1991_film_211:"credit_enc83_mak_patron",
  gig_1992_tv_105:"credit_enc83_yip_patron", gig_1992_rec_205:"credit_enc83_gu_patron",
  gig_1991_ad_102:"credit_enc84_so_patron", gig_1991_film_213:"credit_enc84_chung_patron",
  gig_1992_rec_111:"credit_enc83_lok_patron", gig_1991_film_212:"credit_enc83_ngai_patron",
  gig_1992_film_206:"credit_enc83_chai_patron",
  gig_1992_film_202:"credit_wf3_comedy_crew",
  gig_1992_film_114:"credit_enc83_luk_patron"
};
ok('T8 BR89 15 對（v20a279 收割鏈＋v284 film_114）',
  Object.keys(BR89_PATRON_OF_GIG).length===15 &&
  Object.keys(BR89_EXPECTED).every(k=>BR89_PATRON_OF_GIG[k]===BR89_EXPECTED[k]));

/* ---------- T9：靜態＋舊路徑 ---------- */
ok('T9 html 有 v20a158 渠道 block', html.indexOf('v20a158')>=0 && html.indexOf('FAVOR158_MAK_CREDIT_ID')>=0);
ok('T9 詳情頁有「用人情免試鏡」掣', html.indexOf('用人情免試鏡')>=0);
ok('T9 通告卡有 favor158 提示接線', html.indexOf('favor158ChannelHintHtml')>=0 && html.indexOf('favor158Html')>=0);
ok('T9 aud91CreatePending 有 revealDay 覆寫', html.indexOf('pre.revealDay')>=0);
ok('T9 呈現 modal 有 favor158 分支（免試鏡字句＋favorLabel）',
  html.indexOf('免試鏡直接獲聘')>=0 && html.indexOf('rec.favorLabel')>=0);
freshS(10);
const normalGig = gigById('gig_1991_film_108');
const recN = aud91CreatePending(normalGig, null, { ok:true, p:0.5, days:3, payRoll:{ pay:100, basePay:100, bonusPay:0, bonusLabel:"", note:"" }, fame:5, pop:4, via:"board" });
ok('T9 舊路徑：無 revealDay 照行等待（revealDay＝聽日＋，wait≥1）',
  recN.revealDay>10 && recN.wait>=1 && recN.via==='board' && recN.favorLabel==='', 'revealDay='+recN.revealDay+' wait='+recN.wait);
ok('T9 舊路徑等消息提示行照舊講「試鏡咗」', aud91PendingHint(recN).indexOf('試鏡咗')>=0);

/* ---------- 尾 ---------- */
console.log(fails.length ? ('\nFAILURES: '+fails.length+' :: '+fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
