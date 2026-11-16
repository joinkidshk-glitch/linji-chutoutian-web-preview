// v20a229 B6 抉擇即派＋定期合約制測試（A8／A12；SPEC §3.7／附錄 A；AUDIT229 §8／§10；DECISIONS Q7／D-5）
//   T0 44 張即派 id 齊（主線 31＋支線 13）＋新庫 267 張（v251 補寫 16 張即派新通告；N9_a 重用現有 107）
//   T1 主線 32 映射：抉擇→記低指定 gig、dueDay＝聽日（N1_a／N1_b／N2_a／N2_b／N3_a／N3_b／N4_a／N4_b／N5_a／N5_b／N5_c／N6_a／N6F_a／N18_a／N18_b；N7_a／N7_b／N7_c／N8_a／N8_b／N8_c／N9_a／N9_b／N10_a／N10_b／N10_c／N11_a／N11_b／N12_a／N12_b／N19_a／N19_b；N6_b／N6F_b 唔派；v249 收窄 N4:*→N4:N4_b、N18:*→N18:N18_a；v250 拆 N5:* 做 N5_a／b／c；v251 加 N7–N12／N19 共 17 鍵）
//   T2 支線 11 live 映射：廖／顧／麥初遇各 3（關鍵字命中＋兜底）＋廖 Beat2（W3_ho_liao_a／b）；2 個 draft 存在但無 hook 觸發
//   T3 冪等：同一張記低兩次得一筆；派發一次後唔再派
//   T4 翌日先到期：今日 dueList 空、聽日有
//   T5 派發守衛：已殺青／拍攝中／等消息中／已預約 → 靜靜跳過（queue 清走、唔出電話）；gig 唔存在 → 跳過
//   T6 合約條款：N-3 2 週×$4,900＝$9,800；N-4 2 週×$4,200＝$8,400
//   T7 週結算：有拍攝進展先出糧（入 S.money＋S.weekEarn）、無進展唔出、shoot 消失閂合約、尾週找尾數唔超總額
//   T8 殺青尾糧：已付一半→尾數一半；付清→0；合約閂埋（status done）；payWrapNote／contract229CardLine 字句唔提簽約金餘額
//   T9 派發全程：何生電話 modal→直接獲聘入行程（shoot 入 S.shoots、signedPaid＝三成；合約 shoot.contract229 齊、signedPaid＝0）；獲聘後 isGigConsumed true（板面鎖死）
//   T10 派發唔經試鏡：grant 流程完全唔掂 pendingAud／booked（派完兩者都係空）
// 用法：node tests/test_gig229_grant.js [path-to-index.html]
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

/* ---------- stubs（跟 B5 harness 模式：S／GIGS／apply／scheduleShoot／confirmPlaceShoot／modal 等） ---------- */
var S = null;
var GIGS = gigs;
function freshS(day){
  S = { dayIndex:(day==null?10:day), flags:{}, grant229Queue:[], contracts229:[],
        shoots:[], pendingAud:[], booked:[], board:[], money:12000, weekEarn:0 };
  return S;
}
freshS();
var saveQ = function(){};
var apply = function(o){ if(o && typeof o.money==="number"){ S.money=(S.money||0)+o.money; if(o.money>0) S.weekEarn=(S.weekEarn||0)+o.money; } return []; };
var scheduleShoot = function(gig, pay, fame, pop, payBreak){
  const sh = { id:"sh_test_"+gig.id, gigId:gig.id, title:gig.title, type:gig.type,
    totalDays:(typeof gig.days==="number"?gig.days:0), daysLeft:(typeof gig.days==="number"?gig.days:0),
    doneDays:0, pay:pay, fame:fame, popularity:pop, locId:gig.locId||null, signedPaid:0 };
  S.shoots.push(sh);
  if(Array.isArray(S.board)) S.board = S.board.filter(b=>b!==gig.id);
  return sh;
};
var confirmPlaceShoot = function(shoot, weekday, thenFn){ if(typeof thenFn==="function") thenFn(); };
var lastModal = null, modalCalls = 0;
var modal = function(h, btns, opts){ lastModal = { html:h, btns:btns, opts:opts }; modalCalls++; if(btns && btns[0] && typeof btns[0].on==="function") btns[0].on(); };
var lastToast = null;
var toast = function(t){ lastToast = t; };
var paintBar = function(){};
var drawMap = function(){};
var fmtDate = function(){ return "1990-01-02"; };
var chk101Html = function(o){ return "<CHK101 amount="+o.amount+">"; };
var weekdayIdx = function(d){ return 0; };
var ending78Locked = function(){ return false; };
/* shootSpanFor stub：等同 B1 normalize 映射（days→shootDaysHint；effectiveShootDays 讀 hint）。
   N-3 14 日／N-4 12 日喺真路徑一樣得出 weeks＝2。 */
var shootSpanFor = function(g){ return (g && typeof g.days==="number") ? g.days : 0; };

/* ---------- 抽 B6 模組＋相依真函數（eval 必須喺頂層直接行，唔可以包喺回調入面，否則 var 會落錯 scope） ---------- */
eval(extractConstVar('GRANT229_CHOICE'));
eval(extractConstVar('GRANT229_ENC79'));
eval(extractConstVar('GRANT229_DRAFT'));
eval(extractConstVar('CONTRACT229_GIGS'));
eval(extractFn('grant229Ensure'));
eval(extractFn('grant229GigById'));
eval(extractFn('grant229Mid'));
eval(extractFn('grant229Record'));
eval(extractFn('grant229RecordFromChoice'));
eval(extractFn('grant229RecordFromEnc79'));
eval(extractFn('grant229RecordDraft'));
eval(extractFn('grant229DueList'));
eval(extractFn('grant229IsConsumed'));
eval(extractFn('grant229Drop'));
eval(extractFn('contract229Terms'));
eval(extractFn('grant229HireTerms'));
eval(extractFn('grant229DeliverOne'));
eval(extractFn('grant229PresentDue'));
eval(extractFn('contract229Start'));
eval(extractFn('contract229Find'));
eval(extractFn('contract229Close'));
eval(extractFn('contract229WeeklyTick'));
eval(extractFn('contract229WrapRemainder'));
eval(extractFn('contract229CardLine'));
eval(extractFn('gigPayExact'));
eval(extractFn('gigActiveShoot'));
eval(extractFn('isGigWrapped'));
eval(extractFn('isGigInProduction'));
eval(extractFn('isGigConsumed'));
eval(extractFn('payWrapNote'));

/* ---------- T0：44 張 id 齊＋新庫 267 張 ---------- */
const MAIN31 = ['gig_1990_tv_124','gig_1990_film_124','gig_1990_film_125','gig_1990_tv_125','gig_1990_tv_127','gig_1990_tv_128','gig_1990_ad_117','gig_1990_film_114','gig_1990_tv_130','gig_1990_tv_131','gig_1990_tv_105','gig_1990_film_110','gig_1990_tv_121','gig_1990_tv_129',
  'gig_1991_film_122','gig_1991_tv_123','gig_1991_tv_124','gig_1991_variety_109','gig_1991_rec_117','gig_1991_rec_118','gig_1991_film_107','gig_1991_film_123','gig_1991_film_124','gig_1991_film_125','gig_1991_tv_125','gig_1991_film_126','gig_1991_film_127','gig_1992_film_120','gig_1992_tv_120','gig_1991_tv_126','gig_1991_tv_127'];
const SIDE13 = ['gig_1990_tv_114','gig_1990_tv_115','gig_1990_tv_116','gig_1990_tv_117','gig_1990_tv_118',
  'gig_1990_rec_112','gig_1990_rec_111','gig_1990_rec_113','gig_1991_rec_111','gig_1991_rec_112',
  'gig_1990_film_116','gig_1990_film_117','gig_1990_film_115'];
ok('T0 新庫 267 張', gigs.length===267, 'n='+gigs.length);
ok('T0 主線 31 張 id 齊', MAIN31.every(id=>!!gigById(id)));
ok('T0 支線 13 張 id 齊', SIDE13.every(id=>!!gigById(id)));
ok('T0 《星夜迷離》新庫有且只有 1 張（v232 補寫）', gigs.filter(g=>(g.title||'').indexOf('星夜迷離')>=0).length===1 && gigById('gig_1991_tv_122'));
ok('T0 GRANT229_CHOICE 34 鍵', Object.keys(GRANT229_CHOICE).length===34, Object.keys(GRANT229_CHOICE).join(','));
ok('T0 GRANT229_ENC79 9 行', GRANT229_ENC79.length===9);
ok('T0 GRANT229_DRAFT 2 鍵', Object.keys(GRANT229_DRAFT).length===2);
ok('T0 CONTRACT229_GIGS 只得 N-3／N-4', Object.keys(CONTRACT229_GIGS).length===2 && CONTRACT229_GIGS.gig_1990_tv_105===1 && CONTRACT229_GIGS.gig_1990_film_110===1);

/* ---------- T1：主線 32 映射 ---------- */
function choiceMaps(nodeId, choiceId, wantGig){
  freshS(10);
  const r = grant229RecordFromChoice({id:nodeId}, {id:choiceId});
  const q = S.grant229Queue;
  return r && q.length===1 && q[0].gigId===wantGig && q[0].dueDay===11;
}
ok('T1 N1_a→tv_124', choiceMaps('N1','N1_a','gig_1990_tv_124'));
ok('T1 N1_b→film_124', choiceMaps('N1','N1_b','gig_1990_film_124'));
ok('T1 N2_a→film_125', choiceMaps('N2','N2_a','gig_1990_film_125'));
ok('T1 N2_b→tv_125', choiceMaps('N2','N2_b','gig_1990_tv_125'));
ok('T1 N3_a→tv_127', choiceMaps('N3','N3_a','gig_1990_tv_127'));
ok('T1 N3_b→tv_128', choiceMaps('N3','N3_b','gig_1990_tv_128'));
ok('T1 N4_a 拒絕→ad_117', choiceMaps('N4','N4_a','gig_1990_ad_117'));
ok('T1 N4_b 接下→film_114', choiceMaps('N4','N4_b','gig_1990_film_114'));
ok('T1 N5_a→tv_130', choiceMaps('N5','N5_a','gig_1990_tv_130'));
ok('T1 N5_b→tv_130（與 N5_a 共享）', choiceMaps('N5','N5_b','gig_1990_tv_130'));
ok('T1 N5_c→tv_131', choiceMaps('N5','N5_c','gig_1990_tv_131'));
ok('T1 N6_a→tv_105（合約）', choiceMaps('N6','N6_a','gig_1990_tv_105'));
ok('T1 N6F_a→film_110（合約）', choiceMaps('N6F','N6F_a','gig_1990_film_110'));
ok('T1 N18_a 學幕後→tv_121', choiceMaps('N18','N18_a','gig_1990_tv_121'));
ok('T1 N18_b 專心幕前→tv_129', choiceMaps('N18','N18_b','gig_1990_tv_129'));
ok('T1 N7_a 救場→film_122', choiceMaps('N7','N7_a','gig_1991_film_122'));
ok('T1 N7_b 保妝→tv_123', choiceMaps('N7','N7_b','gig_1991_tv_123'));
ok('T1 N7_c 兩頭→tv_124', choiceMaps('N7','N7_c','gig_1991_tv_124'));
ok('T1 N8_a 掩護→variety_109', choiceMaps('N8','N8_a','gig_1991_variety_109'));
ok('T1 N8_b 爆料→rec_117', choiceMaps('N8','N8_b','gig_1991_rec_117'));
ok('T1 N8_c 引開→rec_118', choiceMaps('N8','N8_c','gig_1991_rec_118'));
ok('T1 N9_a 認橋→film_107（重用廖炳星引薦 gig）', choiceMaps('N9','N9_a','gig_1991_film_107'));
ok('T1 N9_b 背景→film_123', choiceMaps('N9','N9_b','gig_1991_film_123'));
ok('T1 N10_a 追數→film_124', choiceMaps('N10','N10_a','gig_1991_film_124'));
ok('T1 N10_b 出頭→film_125', choiceMaps('N10','N10_b','gig_1991_film_125'));
ok('T1 N10_c 拖→tv_125', choiceMaps('N10','N10_c','gig_1991_tv_125'));
ok('T1 N11_a 黑幫→film_126', choiceMaps('N11','N11_a','gig_1991_film_126'));
ok('T1 N11_b 探長→film_127', choiceMaps('N11','N11_b','gig_1991_film_127'));
ok('T1 N12_a 跳→film_120', choiceMaps('N12','N12_a','gig_1992_film_120'));
ok('T1 N12_b 拒接→tv_120', choiceMaps('N12','N12_b','gig_1992_tv_120'));
ok('T1 N19_a 本份→tv_126', choiceMaps('N19','N19_a','gig_1991_tv_126'));
ok('T1 N19_b 偷師→tv_127', choiceMaps('N19','N19_b','gig_1991_tv_127'));
freshS(10);
ok('T1 N6_b 唔接→唔派', grant229RecordFromChoice({id:'N6'},{id:'N6_b'})===false && S.grant229Queue.length===0);
freshS(10);
ok('T1 N6F_b 唔接→唔派', grant229RecordFromChoice({id:'N6F'},{id:'N6F_b'})===false && S.grant229Queue.length===0);
freshS(10);
ok('T1 無關抉擇→唔派', grant229RecordFromChoice({id:'N13'},{id:'N13_a'})===false && S.grant229Queue.length===0);

/* ---------- T2：支線 11 live 映射＋2 draft dormant ---------- */
function enc79Maps(seg, label, wantGig){
  freshS(10);
  const r = grant229RecordFromEnc79(seg, label);
  const q = S.grant229Queue;
  return r && q.length===1 && q[0].gigId===wantGig && q[0].dueDay===11;
}
ok('T2 廖 笑出聲→tv_114', enc79Maps('first:liu_bingxing','忍唔住笑出聲','gig_1990_tv_114'));
ok('T2 廖 好笑→tv_115', enc79Maps('first:liu_bingxing','大膽講邊句橋好笑啲','gig_1990_tv_115'));
ok('T2 廖 簽名（兜底）→tv_116', enc79Maps('first:liu_bingxing','想攞簽名影相留念','gig_1990_tv_116'));
ok('T2 顧 聽舊歌→rec_112', enc79Maps('first:gu_mingfai','靜靜站在那裡，聽他哼完那段舊歌','gig_1990_rec_112'));
ok('T2 顧 打招呼→rec_111', enc79Maps('first:gu_mingfai','點頭打個招呼，不打擾','gig_1990_rec_111'));
ok('T2 顧 走先（兜底）→rec_113', enc79Maps('first:gu_mingfai','先走，不要讓人見到我和他站在一起','gig_1990_rec_113'));
ok('T2 麥 放低支水→film_116', enc79Maps('first:mak_zhendong','放低支水喺佢身邊就走','gig_1990_film_116'));
ok('T2 麥 堅持遞到手→film_117', enc79Maps('first:mak_zhendong','堅持遞到佢手','gig_1990_film_117'));
ok('T2 麥 問傷勢（兜底）→film_115', enc79Maps('first:mak_zhendong','開口問佢傷勢','gig_1990_film_115'));
freshS(10);
ok('T2 廖 Beat2 a→tv_117', grant229RecordFromChoice({id:'W3_ho_liao'},{id:'W3_ho_liao_a'}) && S.grant229Queue[0].gigId==='gig_1990_tv_117');
freshS(10);
ok('T2 廖 Beat2 b→tv_118', grant229RecordFromChoice({id:'W3_ho_liao'},{id:'W3_ho_liao_b'}) && S.grant229Queue[0].gigId==='gig_1990_tv_118');
ok('T2 draft 兩張 1991 和音喺 GRANT229_DRAFT', GRANT229_DRAFT.gu_promise_clean.gigId==='gig_1991_rec_111' && GRANT229_DRAFT.gu_ask_back.gigId==='gig_1991_rec_112');
freshS(10);
grant229RecordFromEnc79('first:gu_mingfai','靜靜站在那裡，聽他哼完那段舊歌');
ok('T2 draft 唔經初遇 hook 觸發（1991 id 唔會由 enc79 派）', S.grant229Queue.length===1 && S.grant229Queue[0].gigId==='gig_1990_rec_112');
ok('T2 html 入面 grant229RecordDraft 得定義＋註解，唔經任何 hook 呼叫', (html.split('grant229RecordDraft(').length-1)===2);
freshS(10);
ok('T2 draft 入口本身行得通（日後抉擇實裝即啟用）', grant229RecordDraft('gu_promise_clean') && S.grant229Queue[0].gigId==='gig_1991_rec_111');
ok('T2 draft 錯 key→false', grant229RecordDraft('gu_nope')===false);

/* ---------- T3：冪等 ---------- */
freshS(10);
grant229RecordFromChoice({id:'N4'},{id:'N4_b'});
ok('T3 同一張記低兩次得一筆', grant229RecordFromChoice({id:'N4'},{id:'N4_b'})===false && S.grant229Queue.length===1);
freshS(10);
grant229Record('gig_1990_film_114','N4','test');
S.dayIndex = 11;
let stepCalls = 0;
ok('T3 派發一次', grant229PresentDue(()=>{ stepCalls++; })===true && stepCalls===1 && S.grant229Queue.length===0);
ok('T3 派完唔再派（delivered 旗＋queue 空）', grant229PresentDue(()=>{ stepCalls++; })===false && stepCalls===1);

/* ---------- T4：翌日先到期 ---------- */
freshS(10);
grant229RecordFromChoice({id:'N4'},{id:'N4_b'});
ok('T4 今日 dueList 空', grant229DueList().length===0);
S.dayIndex = 11;
ok('T4 聽日 dueList 有', grant229DueList().length===1 && grant229DueList()[0].gigId==='gig_1990_film_114');

/* ---------- T5：派發守衛 ---------- */
function guardCase(setup){
  freshS(10);
  grant229Record('gig_1990_film_114','N4','test');
  S.dayIndex = 11;
  setup();
  modalCalls = 0; stepCalls = 0;
  const r = grant229PresentDue(()=>{ stepCalls++; });
  return { r:r, q:S.grant229Queue.length, modal:modalCalls, step:stepCalls, shoots:S.shoots.length };
}
let g = guardCase(()=>{ S.flags['done_gig_1990_film_114']=1; });
ok('T5 已殺青→跳過', g.r===false && g.q===0 && g.modal===0 && g.shoots===0);
g = guardCase(()=>{ S.shoots.push({id:'sh_x', gigId:'gig_1990_film_114'}); });
ok('T5 拍攝中→跳過', g.r===false && g.q===0 && g.modal===0 && g.shoots===1);
g = guardCase(()=>{ S.pendingAud.push({gigId:'gig_1990_film_114'}); });
ok('T5 等消息中→跳過', g.r===false && g.q===0 && g.modal===0);
g = guardCase(()=>{ S.booked.push({gigId:'gig_1990_film_114'}); });
ok('T5 已預約試鏡→跳過', g.r===false && g.q===0 && g.modal===0);
freshS(10);
grant229Record('gig_1990_film_114','N4','test');
S.dayIndex = 11;
S.grant229Queue[0].gigId = 'gig_no_such';
modalCalls = 0;
ok('T5 gig 唔存在→跳過', grant229PresentDue(()=>{})===false && S.grant229Queue.length===0 && modalCalls===0);

/* ---------- T5b：N9_a 防撞——107 同時係廖炳星引薦 gig（trigger credit_enc79_liu_priority）。
   已持有／已殺青嗰陣，第二朝即派靜默跳過，唔重派／唔出電話（見 V251_C_REPORT §2） ---------- */
freshS(10);
grant229RecordFromChoice({id:'N9'},{id:'N9_a'});
S.dayIndex = 11;
S.shoots.push({id:'sh_107', gigId:'gig_1991_film_107'});
modalCalls = 0; stepCalls = 0;
ok('T5b N9_a 107 已持有（引薦攞咗）→跳過', grant229PresentDue(()=>{ stepCalls++; })===false && S.grant229Queue.length===0 && modalCalls===0 && stepCalls===0);
freshS(10);
grant229RecordFromChoice({id:'N9'},{id:'N9_a'});
S.dayIndex = 11;
S.flags['done_gig_1991_film_107']=1;
modalCalls = 0; stepCalls = 0;
ok('T5b N9_a 107 已殺青→跳過', grant229PresentDue(()=>{ stepCalls++; })===false && S.grant229Queue.length===0 && modalCalls===0 && stepCalls===0);

/* ---------- T6：合約條款 ---------- */
let t6a = contract229Terms(gigById('gig_1990_tv_105'));
ok('T6 N-3 2 週×$4,900＝$9,800', t6a && t6a.weeks===2 && t6a.weeklyPay===4900 && t6a.totalPay===9800, JSON.stringify(t6a));
let t6b = contract229Terms(gigById('gig_1990_film_110'));
ok('T6 N-4 2 週×$4,200＝$8,400', t6b && t6b.weeks===2 && t6b.weeklyPay===4200 && t6b.totalPay===8400, JSON.stringify(t6b));
let t6c = grant229HireTerms(gigById('gig_1990_film_114'));
ok('T6 普通通告：簽約金三成、聲望中位數', t6c && t6c.contract===false && t6c.pay===600 && t6c.signPay===180 && t6c.fame===12, JSON.stringify(t6c));
let t6d = grant229HireTerms(gigById('gig_1990_tv_105'));
ok('T6 合約通告：無簽約金、帶週糧條款', t6d && t6d.contract===true && t6d.signPay===0 && t6d.weeks===2 && t6d.weeklyPay===4900 && t6d.totalPay===9800, JSON.stringify(t6d));

/* ---------- T7：週結算 ---------- */
function contractSetup(gigId){
  freshS(10);
  const gig = gigById(gigId);
  const terms = grant229HireTerms(gig);
  const sh = { id:'sh_c_'+gigId, gigId:gigId, title:gig.title, type:gig.type, totalDays:gig.days, daysLeft:gig.days, doneDays:0, pay:terms.pay, fame:terms.fame, popularity:terms.pop, signedPaid:0,
    contract229:{ gigId:gigId, weeks:terms.weeks, weeklyPay:terms.weeklyPay, totalPay:terms.totalPay, paidTotal:0, paidWeeks:0, tailPaid:0 } };
  S.shoots.push(sh);
  contract229Start(gig, sh, terms);
  return { gig:gig, sh:sh, c:S.contracts229[0] };
}
let s7 = contractSetup('gig_1990_tv_105');
ok('T7 合約紀錄開咗（active）', s7.c && s7.c.status==='active' && s7.c.weeks===2 && s7.c.weeklyPay===4900);
ok('T7 無拍攝進展→唔出糧', contract229WeeklyTick()===0 && S.money===12000 && s7.c.paidTotal===0);
s7.sh.doneDays = 5;
ok('T7 有進展→出第一週糧 $4,900（入錢＋入週收入）', contract229WeeklyTick()===1 && S.money===16900 && S.weekEarn===4900 && s7.c.paidTotal===4900 && s7.c.paidWeeks===1);
ok('T7 同一進展再 tick→唔重複出', contract229WeeklyTick()===0 && S.money===16900);
s7.sh.doneDays = 14;
ok('T7 第二週進展→出第二週糧，總額 $9,800 封頂', contract229WeeklyTick()===1 && S.money===21800 && s7.c.paidTotal===9800);
ok('T7 付清後再 tick→0（唔超總額）', contract229WeeklyTick()===0 && S.money===21800);
let s7b = contractSetup('gig_1990_film_110');
s7b.sh.doneDays = 6;
contract229WeeklyTick();
ok('T7 N-4 第一週 $4,200', S.money===16200 && s7b.c.paidTotal===4200);
S.shoots = [];
contract229WeeklyTick();
ok('T7 shoot 消失→合約閂埋（ended）', s7b.c.status==='ended');

/* ---------- T8：殺青尾糧 ---------- */
let s8 = contractSetup('gig_1990_tv_105');
s8.sh.doneDays = 7; contract229WeeklyTick(); /* 已付一半 $4,900 */
ok('T8 已付一半→殺青尾糧一半 $4,900', contract229WrapRemainder(s8.sh)===4900);
ok('T8 殺青後合約 done', s8.c.status==='done');
ok('T8 尾糧字句講尾糧唔講餘額', payWrapNote(s8.sh).indexOf('尾糧')>=0 && payWrapNote(s8.sh).indexOf('餘額')<0, payWrapNote(s8.sh));
ok('T8 拍攝卡字句講長期合約＋週糧', contract229CardLine(s8.sh).indexOf('長期合約')>=0 && contract229CardLine(s8.sh).indexOf('每週')>=0, contract229CardLine(s8.sh));
ok('T8 再計尾糧→0', contract229WrapRemainder(s8.sh)===0);
let s8b = contractSetup('gig_1990_film_110');
s8b.sh.doneDays = 6; contract229WeeklyTick(); /* 第一週 $4,200 */
s8b.sh.doneDays = 12; contract229WeeklyTick(); /* 第二週 $4,200，付清 */
ok('T8 付清→殺青尾糧 0', contract229WrapRemainder(s8b.sh)===0 && s8b.c.status==='done');
ok('T8 非合約 shoot→尾糧 0', contract229WrapRemainder({gigId:'gig_1990_film_114'})===0);

/* ---------- T9／T10：派發全程＋唔經試鏡 ---------- */
freshS(10);
grant229RecordFromChoice({id:'N4'},{id:'N4_b'});
S.dayIndex = 11; modalCalls = 0; stepCalls = 0; lastModal = null; lastToast = null;
ok('T9 普通通告：何生電話呈現', grant229PresentDue(()=>{ stepCalls++; })===true && modalCalls===1 && stepCalls===1);
ok('T9 modal 講何生來電＋簽約金', lastModal && lastModal.html.indexOf('何生來電')>=0 && lastModal.html.indexOf('簽約金')>=0);
ok('T9 簽約金 $180 已入帳', S.money===12180 && S.weekEarn===180);
ok('T9 shoot 入行程（signedPaid＝三成）', S.shoots.length===1 && S.shoots[0].gigId==='gig_1990_film_114' && S.shoots[0].signedPaid===180 && !S.shoots[0].contract229);
ok('T9 獲聘後 isGigConsumed true（板面鎖死）', isGigConsumed(gigById('gig_1990_film_114'))===true);
ok('T10 派發唔經試鏡（pendingAud／booked 皆空）', S.pendingAud.length===0 && S.booked.length===0);
ok('T10 toast 有通告名', lastToast && lastToast.indexOf('水塘夜戲')>=0, String(lastToast));

freshS(10);
grant229RecordFromChoice({id:'N6'},{id:'N6_a'});
S.dayIndex = 11; modalCalls = 0; stepCalls = 0; lastModal = null;
ok('T9 合約通告：何生電話呈現', grant229PresentDue(()=>{ stepCalls++; })===true && modalCalls===1 && stepCalls===1);
ok('T9 合約 modal 講長期合約＋每週出糧', lastModal && lastModal.html.indexOf('長期合約')>=0 && lastModal.html.indexOf('每週')>=0);
ok('T9 合約：無簽約金入帳', S.money===12000 && S.weekEarn===0);
ok('T9 合約 shoot 有 contract229（2 週×$4,900）', S.shoots.length===1 && S.shoots[0].contract229 && S.shoots[0].contract229.weeks===2 && S.shoots[0].contract229.weeklyPay===4900 && S.shoots[0].signedPaid===0);
ok('T9 合約紀錄 active', S.contracts229.length===1 && S.contracts229[0].status==='active' && S.contracts229[0].totalPay===9800);
ok('T9 合約獲聘後 isGigConsumed true', isGigConsumed(gigById('gig_1990_tv_105'))===true);
ok('T10 合約派發唔經試鏡', S.pendingAud.length===0 && S.booked.length===0);

/* ---------- 尾 ---------- */
console.log(fails.length ? ('\nFAILURES: '+fails.length+' :: '+fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
