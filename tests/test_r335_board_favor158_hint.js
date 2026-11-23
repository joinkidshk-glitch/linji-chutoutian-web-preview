// v20a335 板短卡補返人情免試鏡金色提示（gigBoardTeaserHtml＋addLocGigActs）
//   背景：v158 實駕抽檢（77 PASS／2 FAIL）搵到——金提示 favor158Html 只寫喺 gigCardHtml，
//   live 唯一 call 位係手帳待試鏡列表（L46187）；板短卡由 gigBoardTeaserHtml 另行渲染，
//   零 favor158 引用，板上睇唔到邊張可以用人情免試鏡。詳情頁提示＋掣本身正常。
//   修法：gigBoardTeaserHtml 入面加返 favor158ChannelHintHtml(g) 同一行（同 gigCardHtml
//   同一寫法＋typeof 守衛），CSS 加 .gig-teaser .gold 收細做短卡尺寸。
//   覆蓋：兩渠道 ready 卡有提示／無債權／閘未過／唔啱類別／已兌現 → 無提示；
//   彭渠道鎖定卡（全數台風唔夠、減半過到）都有提示（同詳情頁鎖定分支一致，v20a300）；
//   提示字串同詳情頁逐字相同、只出一次。
//   v20a335b 補充：實駕覆驗發現 A1 檢查嗰層係地點面板 #loc-acts 嘅 button.act 短卡，
//   由 addLocGigActs 另行渲染，唔經 gigBoardTeaserHtml——所以同一行金提示要喺嗰度再補一次：
//   add() 加選填第 6 參數 extraHtml（掣內描述行之後嘅附加 HTML；.h 單行截短，放唔入去），
//   addLocGigActs 用 favor158ChannelForGig(g).hint 包做 <div class="gold"> 傳入；
//   CSS 加 #loc-sheet.sheet .act .gold（深金，掣內描述尺寸）。
// 用法：node tests/test_r335_board_favor158_hint.js [path-to-index.html]
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
/* canAudition：按 req 逐項對 S 數值（stage／acting／stamina／charm），其餘要求當過關；
   彭渠道減半邏輯靠真 pangEffectiveGig158 改 req.stage 後再行呢個 stub。 */
var canAudition = function(g){
  const r = (g && g.req) || {};
  const need = [['stage','stage'],['acting','acting'],['stamina','stamina'],['charm','charm']];
  for(const [rk, sk] of need){
    if(Number(r[rk]||0) > Number(S[sk]||0)) return { ok:false, reason:rk+'未合' };
  }
  return { ok:true };
};
var gigWorkTitle = function(g){ return (g && g.title) || ''; };
var gigTypeCoarse = function(g){ return (g && g.type) || '通告'; };
var gigRecruitStatus = function(g){ return { key:'', label:'招募中' }; };
var gigTierKey = function(g){ return 'mid'; };
var gigPayExactText = function(g){ return '$100'; };
var gigScheduleVerb = function(g){ return '拍攝'; };
var effectiveShootDays = function(g){ return (g && typeof g.days==='number') ? g.days : 1; };
var phase3CastCopy = function(){ return { lockedTag:'暫未能報', readyTag:'可接通告', readyLabel:'接通告', lockedLabel:'暫未能報' }; };
var gigGapBoardLine37 = function(g){ return ''; };
var triggerGigLabel229 = function(g){ return ''; };
var chance = function(g){ return 0.64; };
var gigGenreLabel = function(g){ return (g && g.type) || '通告'; };
var softPreviewOn = function(){ return false; };
var lifecycleOverride = null;
var gigLifecycleStatus = function(g){ return lifecycleOverride; };
var shootRemain = function(sh){ return 1; };

function freshS(o){
  o = o || {};
  S = { dayIndex:10, flags:{}, mockCredits:[], money:12000, fame:5, shoots:[],
        stage:(o.stage==null?50:o.stage), acting:(o.acting==null?80:o.acting),
        stamina:(o.stamina==null?80:o.stamina), charm:(o.charm==null?30:o.charm) };
  return S;
}
function giveCredit(id, debtor){
  S.mockCredits.push({ id:id, debtor:debtor, title:'test', line:'test line', status:'未收' });
  return S.mockCredits[S.mockCredits.length-1];
}
freshS();

/* ---------- 抽真函數 ---------- */
eval(extractConstVar('FAVOR158_MAK_CREDIT_ID'));
eval(extractConstVar('FAVOR158_PANG_CREDIT_ID'));
eval(extractFn('gigBoardCardState'));
eval(extractFn('favor158CreditHeld'));
eval(extractFn('isMakWuzhiGig158'));
eval(extractFn('isPangCharityGig158'));
eval(extractFn('pangHalvedStageReq158'));
eval(extractFn('pangEffectiveGig158'));
eval(extractFn('pangChannelReady158'));
eval(extractFn('favor158ChannelForGig'));
eval(extractFn('favor158ChannelHintHtml'));
eval(extractFn('gigBoardTeaserHtml'));
/* v389：addLocGigActs 已刪（逐張通告掣收埋入通告欄），金提示只剩通告欄短卡一層。 */

const MAK_GIG = gigById('gig_1991_film_108');      /* 《月夜酒廊》男配角，動作＋作品，演技 78／體能 70 */
const MAK_WRONG = gigById('gig_1990_film_206');    /* 碼頭搬運，臨記通告，唔入武指渠道 */
const MAK_NONACTION = gigById('gig_1991_film_109');/* 《笑聲震天響》，喜劇，唔入武指渠道 */
const PANG_GIG = gigById('gig_1991_variety_103');  /* 《樂善之夜》慈善晚會主持，台風 45／魅力 30 */
const PANG_LOW = gigById('gig_1990_variety_101');  /* 《今夜歡笑》，台風 15／魅力 12 */
function countGold(s){ return (s.match(/class="gold"/g)||[]).length; }

/* ---------- A. 武指渠道（ready 卡） ---------- */
freshS({ stage:50, acting:80, stamina:80, charm:30 });
giveCredit('credit_enc79_mak_wuzhi', '紅棉武指');
let hint = favor158ChannelHintHtml(MAK_GIG);
let card = gigBoardTeaserHtml(MAK_GIG, {});
ok('A1 武指 ready 卡：短卡有金提示行', card.indexOf('class="gold"')>=0 && card.indexOf('武指照應')>=0);
ok('A2 武指 ready 卡：提示字串同詳情頁逐字相同', hint !== '' && card.indexOf(hint)>=0, hint);
ok('A3 武指 ready 卡：金提示只出一次', countGold(card)===1, 'count='+countGold(card));
ok('A4 武指 ready 卡：標題＋meta 照常渲染', card.indexOf('月夜酒廊')>=0 && card.indexOf('片酬')>=0);

freshS({ stage:50, acting:80, stamina:80, charm:30 });
card = gigBoardTeaserHtml(MAK_GIG, {});
ok('A5 無債權 → 短卡無金提示', countGold(card)===0 && favor158ChannelHintHtml(MAK_GIG)==='');

freshS({ stage:50, acting:10, stamina:80, charm:30 });
giveCredit('credit_enc79_mak_wuzhi', '紅棉武指');
card = gigBoardTeaserHtml(MAK_GIG, {});
ok('A6 閘未過（演技唔夠）→ 短卡無金提示', countGold(card)===0);

freshS({ stage:50, acting:80, stamina:80, charm:30 });
giveCredit('credit_enc79_mak_wuzhi', '紅棉武指');
card = gigBoardTeaserHtml(MAK_WRONG, {});
ok('A7 唔啱類別（臨記搬運）→ 短卡無金提示', countGold(card)===0);
card = gigBoardTeaserHtml(MAK_NONACTION, {});
ok('A8 唔啱類別（喜劇）→ 短卡無金提示', countGold(card)===0);

freshS({ stage:50, acting:80, stamina:80, charm:30 });
const c = giveCredit('credit_enc79_mak_wuzhi', '紅棉武指');
c.redeemedBy = 'gig_1991_film_110';
card = gigBoardTeaserHtml(MAK_GIG, {});
ok('A9 已兌現債權 → 短卡無金提示', countGold(card)===0);

/* ---------- B. 彭渠道（ready 卡＋鎖定卡） ---------- */
freshS({ stage:50, acting:80, stamina:80, charm:30 });
giveCredit('credit_enc84_pang_charity', '彭少祺');
hint = favor158ChannelHintHtml(PANG_GIG);
card = gigBoardTeaserHtml(PANG_GIG, {});
ok('B1 彭 ready 卡：短卡有金提示行', card.indexOf('class="gold"')>=0 && card.indexOf('慈善騷頂班')>=0);
ok('B2 彭 ready 卡：提示字串同詳情頁逐字相同', hint !== '' && card.indexOf(hint)>=0, hint);
ok('B3 彭 ready 卡：金提示只出一次', countGold(card)===1, 'count='+countGold(card));

freshS({ stage:25, acting:80, stamina:80, charm:30 });
giveCredit('credit_enc84_pang_charity', '彭少祺');
hint = favor158ChannelHintHtml(PANG_GIG);
card = gigBoardTeaserHtml(PANG_GIG, {});
ok('B4 彭鎖定卡（全數台風 45 唔夠、減半 23 過到）：短卡有金提示', card.indexOf('class="gold"')>=0, hint);
ok('B5 彭鎖定卡：提示寫明台風減半數字', card.indexOf('台風要求 45→23')>=0);
ok('B6 彭鎖定卡：卡態係 locked（正常試鏡路線照鎖）', card.indexOf('data-board-state="locked"')>=0);

freshS({ stage:14, acting:80, stamina:80, charm:12 });
giveCredit('credit_enc84_pang_charity', '彭少祺');
hint = favor158ChannelHintHtml(PANG_LOW);
card = gigBoardTeaserHtml(PANG_LOW, {});
ok('B7 開局台風 14：《今夜歡笑》全數 15 唔夠、減半 8 過到 → 有金提示', card.indexOf('class="gold"')>=0, hint);

freshS({ stage:10, acting:80, stamina:80, charm:30 });
giveCredit('credit_enc84_pang_charity', '彭少祺');
card = gigBoardTeaserHtml(PANG_GIG, {});
ok('B8 減半都唔夠（台風 10＜23）→ 短卡無金提示', countGold(card)===0);

freshS({ stage:50, acting:80, stamina:80, charm:30 });
card = gigBoardTeaserHtml(PANG_GIG, {});
ok('B9 無債權 → 短卡無金提示', countGold(card)===0);
card = gigBoardTeaserHtml(MAK_GIG, {});
ok('B10 彭債權唔適用喺武打通告', countGold(card)===0);

/* ---------- C. 靜態 ---------- */
ok('C1 gigBoardTeaserHtml 內有 favor158ChannelHintHtml 呼叫', html.indexOf('favor158ChannelHintHtml(g)')>=0);
ok('C2 CSS 有 .gig-teaser .gold 短卡尺寸規則', html.indexOf('.gig-teaser .gold')>=0);
ok('C3 gigCardHtml 提示寫法原封不動', html.indexOf('let favor158Html = "";')>=0);
ok('C4 add() 有 extraHtml 第 6 參數（地點掣金提示行）', html.indexOf('const add=(title,hint,cost,fn,cls,extraHtml)=>{')>=0);
ok('C5 addLocGigActs 已刪（v389 逐張掣收埋入通告欄）', html.indexOf('function addLocGigActs')<0);
ok('C6 CSS 有 #loc-sheet.sheet .act .gold 掣內金行規則', html.indexOf('#loc-sheet.sheet .act .gold')>=0);

/* ---------- D. （v389 已刪：地點面板逐張接通告掣收埋入通告欄，金提示由 A／B 段短卡覆蓋） ---------- */

console.log(fails.length ? ('FAILURES: '+fails.length+' :: '+fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
