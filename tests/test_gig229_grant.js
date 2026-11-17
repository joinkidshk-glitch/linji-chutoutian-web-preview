// v20a229 B6 抉擇即派＋定期合約制測試（A8／A12；SPEC §3.7／附錄 A；AUDIT229 §8／§10；DECISIONS Q7／D-5）
//   T0 44 張即派 id 齊（主線 31＋支線 13）＋新庫 289 張（v255：ENC79 9 張＋DRAFT 2 張重對完成——
//       REUSE 4 張（rec_209／rec_201／film_211／1991_rec_201）＋NEW 7 張（tv_217／218／219、rec_210、
//       film_213／214、1991_rec_207）；11 張舊 id 已唔喺新庫，映射已改指新 id，實機初遇／draft 即派 live；
//       v253 C 組再加 6 張新 gig，庫 276→282；v20a274 再加 5 張引薦 gig，庫 282→287；v20a279 再加 1 張收割 gig，庫 287→288；v20a284 再加 1 張陸引薦 gig，庫 288→289；v20a158 再加 8 行支線抉擇即派（顧／麥／廖，ENC79 9→17））
//   T1 主線 42 映射：抉擇→記低指定 gig、dueDay＝聽日（同上；v252 新 id：N1 tv_201／film_201、N2 film_202／tv_202、
//       N3 tv_203／tv_204、N4 ad_206／film_203、N5 tv_205／tv_205／tv_206、N6 tv_107 合約、N6F film_113 合約、
//       N18 tv_208／tv_110、N7 film_104／tv_107／tv_201、N8 variety_109／rec_205／rec_206、N9 film_103／film_201、
//       N10 film_105／film_202／tv_202、N11 film_106／film_107、N12 film_201／tv_103、N19 tv_104／tv_105；
//       v253 C 組 10：N13 tv_114／film_102、N14 rec_111／rec_201／ad_109、N15 ad_110／rec_202、N16 film_113／film_104／ad_111；N13_c 不派）
//   T2 支線：ENC79 廖／顧／麥初遇各 3（關鍵字命中＋兜底，映射表揀啱新 id，實機 record 派得出——v255 live）
//       ＋廖 Beat2（W3_ho_liao_a／b → tv_209／tv_210，live）＋2 個 draft 目標 live（入口派得出，仍無呼叫點）
//   T3 冪等：同一張記低兩次得一筆；派發一次後唔再派
//   T4 翌日先到期：今日 dueList 空、聽日有
//   T5 派發守衛：已殺青／拍攝中／等消息中／已預約 → 靜靜跳過（queue 清走、唔出電話）；gig 唔存在 → 跳過
//   T6 合約條款：N-3 2 週×$490＝$980；N-4 2 週×$390＝$780（v261 ÷10）
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
/* ---------- T11 D7 抽取：殺青計數＋作品牆＋提名計數（真函數，v253 工人 C） ---------- */
eval(extractConstVar('START'));
eval(extractConstVar('END95_TYPE_MEDIUM'));
eval(extractConstVar('END95_LEAD_SCALES'));
eval(extractConstVar('END95_STRONG_LEAD'));
eval(extractConstVar('END95_GENRE_TYPE_NAMES'));
eval(extractConstVar('END95_COMEDY_G'));
eval(extractConstVar('END95_ACTION_G'));
eval(extractConstVar('END95_COMEDY_KW'));
eval(extractConstVar('END95_ACTION_KW'));
eval(extractConstVar('ENDING410_BACKSTAGE_KEYS'));
eval(extractConstVar('END229_LEAD_MEDIUM'));
eval(extractConstVar('POSTER59_STAR_IDS'));
eval(extractFn('awardsCalendarYear'));
eval(extractFn('awardsYearFromDay'));
eval(extractFn('gig229CategoryOf'));
eval(extractFn('countYearMediumWraps'));
eval(extractFn('end95GenreOf'));
eval(extractFn('end95IsLead'));
eval(extractFn('end95ClassifyWrap'));
eval(extractFn('end95EmptyStats'));
eval(extractFn('end95StatsAddOne'));
eval(extractFn('end95DeriveStats'));
eval(extractFn('careerStats95Of'));
eval(extractFn('end95AddWrap'));
eval(extractFn('end229IsLead'));
eval(extractFn('end229ClassifyLead'));
eval(extractFn('end229EmptyLeadStats'));
eval(extractFn('end229DeriveLeadStats'));
eval(extractFn('leadStats229Of'));
eval(extractFn('end229AddWrap'));
eval(extractFn('work59GigLookup'));
eval(extractFn('work59IsNamed'));
eval(extractFn('work59WorkOf'));
eval(extractFn('work59RoleOf'));
eval(extractFn('work59YearOf'));
eval(extractFn('poster59Path'));
eval(extractFn('leadStar59Of'));
eval(extractFn('worksWallEntries59'));

/* ---------- T0：44 張 id 齊＋新庫 288 張 ---------- */
const MAIN31 = ['gig_1990_tv_201','gig_1990_film_201','gig_1990_film_202','gig_1990_tv_202','gig_1990_tv_203','gig_1990_tv_204','gig_1990_ad_206','gig_1990_film_203','gig_1990_tv_205','gig_1990_tv_206','gig_1990_tv_107','gig_1990_film_113','gig_1990_tv_208','gig_1990_tv_110',
  'gig_1991_film_104','gig_1991_tv_107','gig_1991_tv_201','gig_1991_variety_109','gig_1991_rec_205','gig_1991_rec_206','gig_1991_film_103','gig_1991_film_201','gig_1991_film_105','gig_1991_film_202','gig_1991_tv_202','gig_1991_film_106','gig_1991_film_107','gig_1992_film_201','gig_1992_tv_103','gig_1991_tv_104','gig_1991_tv_105'];
/* v255：11 張舊 id 仲係唔喺新庫（已刪）；映射已改指新 id（REUSE 4＋NEW 7），舊 id 只留喺呢度做反證。 */
const SIDE_LIVE11 = ['gig_1990_tv_217','gig_1990_tv_218','gig_1990_tv_219',
  'gig_1990_rec_209','gig_1990_rec_201','gig_1990_rec_210',
  'gig_1990_film_211','gig_1990_film_213','gig_1990_film_214',
  'gig_1991_rec_201','gig_1991_rec_207'];
const SIDE_DEAD11 = ['gig_1990_tv_114','gig_1990_tv_115','gig_1990_tv_116',
  'gig_1990_rec_112','gig_1990_rec_111','gig_1990_rec_113',
  'gig_1990_film_116','gig_1990_film_117','gig_1990_film_115',
  'gig_1991_rec_111','gig_1991_rec_112'];
const SIDE_W3_2 = ['gig_1990_tv_209','gig_1990_tv_210'];
ok('T0 新庫 289 張', gigs.length===289, 'n='+gigs.length);
ok('T0 主線 31 張 id 齊', MAIN31.every(id=>!!gigById(id)));
ok('T0 支線 W3 2 張 id 齊', SIDE_W3_2.every(id=>!!gigById(id)));
ok('T0 ENC79／DRAFT 11 張舊 id 已唔喺新庫（v255：已刪，映射改指新 id）', SIDE_DEAD11.every(id=>!gigById(id)),
   'dead=' + SIDE_DEAD11.filter(id=>!gigById(id)).length + '/11');
ok('T0 ENC79 原 9 行指住 live 新 id（REUSE 4＋NEW 7；v20a158 新 8 行另見 test_sideline158_logic.js T7）', GRANT229_ENC79.slice(0,9).every(r=>SIDE_LIVE11.indexOf(r.gigId)>=0));
ok('T0 DRAFT 2 鍵指住 live 新 id', Object.values(GRANT229_DRAFT).every(v=>SIDE_LIVE11.indexOf(v.gigId)>=0));
ok('T0 11 張新 id 全部喺庫', SIDE_LIVE11.every(id=>!!gigById(id)));
ok('T0 《星夜迷離》新庫有且只有 1 張（v232 補寫，v252 重編號 tv_122→tv_203）', gigs.filter(g=>(g.title||'').indexOf('星夜迷離')>=0).length===1 && gigById('gig_1991_tv_203'));
ok('T0 GRANT229_CHOICE 44 鍵', Object.keys(GRANT229_CHOICE).length===44, Object.keys(GRANT229_CHOICE).join(','));
ok('T0 GRANT229_ENC79 74 行（原 17＋v20a278 六線 57 行）', GRANT229_ENC79.length===74);
ok('T0 GRANT229_DRAFT 2 鍵', Object.keys(GRANT229_DRAFT).length===2);
ok('T0 CONTRACT229_GIGS 只得 N-3／N-4', Object.keys(CONTRACT229_GIGS).length===2 && CONTRACT229_GIGS.gig_1990_tv_107===1 && CONTRACT229_GIGS.gig_1990_film_113===1);

/* ---------- T1：主線 32 映射 ---------- */
function choiceMaps(nodeId, choiceId, wantGig){
  freshS(10);
  const r = grant229RecordFromChoice({id:nodeId}, {id:choiceId});
  const q = S.grant229Queue;
  return r && q.length===1 && q[0].gigId===wantGig && q[0].dueDay===11;
}
ok('T1 N1_a→tv_201', choiceMaps('N1','N1_a','gig_1990_tv_201'));
ok('T1 N1_b→film_201', choiceMaps('N1','N1_b','gig_1990_film_201'));
ok('T1 N2_a→film_202', choiceMaps('N2','N2_a','gig_1990_film_202'));
ok('T1 N2_b→tv_202', choiceMaps('N2','N2_b','gig_1990_tv_202'));
ok('T1 N3_a→tv_203', choiceMaps('N3','N3_a','gig_1990_tv_203'));
ok('T1 N3_b→tv_204', choiceMaps('N3','N3_b','gig_1990_tv_204'));
ok('T1 N4_a 拒絕→ad_206', choiceMaps('N4','N4_a','gig_1990_ad_206'));
ok('T1 N4_b 接下→film_203', choiceMaps('N4','N4_b','gig_1990_film_203'));
ok('T1 N5_a→tv_205', choiceMaps('N5','N5_a','gig_1990_tv_205'));
ok('T1 N5_b→tv_205（與 N5_a 共享）', choiceMaps('N5','N5_b','gig_1990_tv_205'));
ok('T1 N5_c→tv_206', choiceMaps('N5','N5_c','gig_1990_tv_206'));
ok('T1 N6_a→tv_107（合約）', choiceMaps('N6','N6_a','gig_1990_tv_107'));
ok('T1 N6F_a→film_113（合約）', choiceMaps('N6F','N6F_a','gig_1990_film_113'));
ok('T1 N18_a 學幕後→tv_208', choiceMaps('N18','N18_a','gig_1990_tv_208'));
ok('T1 N18_b 專心幕前→tv_110', choiceMaps('N18','N18_b','gig_1990_tv_110'));
ok('T1 N7_a 救場→film_104', choiceMaps('N7','N7_a','gig_1991_film_104'));
ok('T1 N7_b 保妝→tv_107', choiceMaps('N7','N7_b','gig_1991_tv_107'));
ok('T1 N7_c 兩頭→tv_201', choiceMaps('N7','N7_c','gig_1991_tv_201'));
ok('T1 N8_a 掩護→variety_109', choiceMaps('N8','N8_a','gig_1991_variety_109'));
ok('T1 N8_b 爆料→rec_205', choiceMaps('N8','N8_b','gig_1991_rec_205'));
ok('T1 N8_c 引開→rec_206', choiceMaps('N8','N8_c','gig_1991_rec_206'));
ok('T1 N9_a 認橋→film_103（重用廖炳星引薦 gig）', choiceMaps('N9','N9_a','gig_1991_film_103'));
ok('T1 N9_b 背景→film_201', choiceMaps('N9','N9_b','gig_1991_film_201'));
ok('T1 N10_a 追數→film_105', choiceMaps('N10','N10_a','gig_1991_film_105'));
ok('T1 N10_b 出頭→film_202', choiceMaps('N10','N10_b','gig_1991_film_202'));
ok('T1 N10_c 拖→tv_202', choiceMaps('N10','N10_c','gig_1991_tv_202'));
ok('T1 N11_a 黑幫→film_106', choiceMaps('N11','N11_a','gig_1991_film_106'));
ok('T1 N11_b 探長→film_107', choiceMaps('N11','N11_b','gig_1991_film_107'));
ok('T1 N12_a 跳→film_201', choiceMaps('N12','N12_a','gig_1992_film_201'));
ok('T1 N12_b 拒接→tv_103', choiceMaps('N12','N12_b','gig_1992_tv_103'));
ok('T1 N13_a 企邊電視台→tv_114', choiceMaps('N13','N13_a','gig_1992_tv_114'));
ok('T1 N13_b 企邊電影公司→film_102', choiceMaps('N13','N13_b','gig_1992_film_102'));
ok('T1 N14_a 主打歌MV→rec_111', choiceMaps('N14','N14_a','gig_1992_rec_111'));
ok('T1 N14_b 樂壇洗牌→rec_201', choiceMaps('N14','N14_b','gig_1992_rec_201'));
ok('T1 N14_c 頒獎禮前哨→ad_109', choiceMaps('N14','N14_c','gig_1992_ad_109'));
ok('T1 N15_a 櫥窗少年→ad_110', choiceMaps('N15','N15_a','gig_1992_ad_110'));
ok('T1 N15_b 影展主題歌→rec_202', choiceMaps('N15','N15_b','gig_1992_rec_202'));
ok('T1 N16_a 賀歲大鑊→film_113', choiceMaps('N16','N16_a','gig_1992_film_113'));
ok('T1 N16_b 笑爆賀歲→film_104', choiceMaps('N16','N16_b','gig_1992_film_104'));
ok('T1 N16_c 聖誕中環→ad_111', choiceMaps('N16','N16_c','gig_1992_ad_111'));
ok('T1 N19_a 本份→tv_104', choiceMaps('N19','N19_a','gig_1991_tv_104'));
ok('T1 N19_b 偷師→tv_105', choiceMaps('N19','N19_b','gig_1991_tv_105'));
freshS(10);
ok('T1 N6_b 唔接→唔派', grant229RecordFromChoice({id:'N6'},{id:'N6_b'})===false && S.grant229Queue.length===0);
freshS(10);
ok('T1 N6F_b 唔接→唔派', grant229RecordFromChoice({id:'N6F'},{id:'N6F_b'})===false && S.grant229Queue.length===0);
freshS(10);
ok('T1 無關抉擇→唔派', grant229RecordFromChoice({id:'N13'},{id:'N13_c'})===false && S.grant229Queue.length===0);

/* ---------- T2：支線 11 live 映射＋2 draft dormant ---------- */
/* v255：ENC79 9 行＋DRAFT 2 鍵已重對新庫（REUSE 4＋NEW 7）。呢度分兩層驗：
   (a) 映射表揀啱邊張（跟 grant229RecordFromEnc79 同一規則：關鍵字命中，否則兜底最後一行空 key）；
   (b) 實機 record 派得出（queue 有一筆、dueDay＝聽日、目標喺庫）。 */
function enc79Pick(seg, label){
  const rows = GRANT229_ENC79.filter(r=>r && r.seg===seg);
  for(let i=0;i<rows.length;i++){ const k = String(rows[i].key||''); if(k && label.indexOf(k)>=0) return rows[i].gigId; }
  const fb = rows[rows.length-1];
  return (fb && !String(fb.key||'')) ? fb.gigId : null;
}
function enc79Live(seg, label, wantGig){
  freshS(10);
  const r = grant229RecordFromEnc79(seg, label);
  return r===true && S.grant229Queue.length===1 && S.grant229Queue[0].gigId===wantGig && S.grant229Queue[0].dueDay===11;
}
const ENC79_CASES = [
  ['first:liu_bingxing','忍唔住笑出聲','gig_1990_tv_217'],
  ['first:liu_bingxing','大膽講邊句橋好笑啲','gig_1990_tv_218'],
  ['first:liu_bingxing','想攞簽名影相留念','gig_1990_tv_219'],
  ['first:gu_mingfai','靜靜站在那裡，聽他哼完那段舊歌','gig_1990_rec_209'],
  ['first:gu_mingfai','點頭打個招呼，不打擾','gig_1990_rec_201'],
  ['first:gu_mingfai','先走，不要讓人見到我和他站在一起','gig_1990_rec_210'],
  ['first:mak_zhendong','放低支水喺佢身邊就走','gig_1990_film_211'],
  ['first:mak_zhendong','堅持遞到佢手','gig_1990_film_213'],
  ['first:mak_zhendong','開口問佢傷勢','gig_1990_film_214']
];
ENC79_CASES.forEach(c=>{
  ok('T2 初遇映射揀啱 ' + c[2] + '（' + c[0] + '）', enc79Pick(c[0], c[1])===c[2]);
  ok('T2 初遇實機派得出（記低＋聽日到期）' + c[2], enc79Live(c[0], c[1], c[2]));
});
freshS(10);
ok('T2 廖 Beat2 a→tv_209', grant229RecordFromChoice({id:'W3_ho_liao'},{id:'W3_ho_liao_a'}) && S.grant229Queue[0].gigId==='gig_1990_tv_209');
freshS(10);
ok('T2 廖 Beat2 b→tv_210', grant229RecordFromChoice({id:'W3_ho_liao'},{id:'W3_ho_liao_b'}) && S.grant229Queue[0].gigId==='gig_1990_tv_210');
ok('T2 draft 兩張 1991 和音喺 GRANT229_DRAFT', GRANT229_DRAFT.gu_promise_clean.gigId==='gig_1991_rec_201' && GRANT229_DRAFT.gu_ask_back.gigId==='gig_1991_rec_207');
freshS(10);
grant229RecordFromEnc79('first:gu_mingfai','靜靜站在那裡，聽他哼完那段舊歌');
ok('T2 draft 唔經初遇 hook 觸發（初遇只派 rec_209，1991 draft id 唔會出現）', S.grant229Queue.length===1 && S.grant229Queue[0].gigId==='gig_1990_rec_209' && !S.grant229Queue.some(q=>q.gigId==='gig_1991_rec_201' || q.gigId==='gig_1991_rec_207'));
ok('T2 v273：grant229RecordDraft 得定義＋註解＋enc79RunChoiceFx 呼叫點（顧 Beat 2 即派，gu_promise_clean／gu_ask_back）', (html.split('grant229RecordDraft(').length-1)===3 && html.includes('grant229RecordDraft(fx)'));
freshS(10);
ok('T2 draft gu_promise_clean 入口派得出（→1991_rec_201）', grant229RecordDraft('gu_promise_clean')===true && S.grant229Queue.length===1 && S.grant229Queue[0].gigId==='gig_1991_rec_201');
freshS(10);
ok('T2 draft gu_ask_back 入口派得出（→1991_rec_207）', grant229RecordDraft('gu_ask_back')===true && S.grant229Queue.length===1 && S.grant229Queue[0].gigId==='gig_1991_rec_207');
ok('T2 draft 錯 key→false', grant229RecordDraft('gu_nope')===false);

/* ---------- T3：冪等 ---------- */
freshS(10);
grant229RecordFromChoice({id:'N4'},{id:'N4_b'});
ok('T3 同一張記低兩次得一筆', grant229RecordFromChoice({id:'N4'},{id:'N4_b'})===false && S.grant229Queue.length===1);
freshS(10);
grant229Record('gig_1990_film_203','N4','test');
S.dayIndex = 11;
let stepCalls = 0;
ok('T3 派發一次', grant229PresentDue(()=>{ stepCalls++; })===true && stepCalls===1 && S.grant229Queue.length===0);
ok('T3 派完唔再派（delivered 旗＋queue 空）', grant229PresentDue(()=>{ stepCalls++; })===false && stepCalls===1);

/* ---------- T4：翌日先到期 ---------- */
freshS(10);
grant229RecordFromChoice({id:'N4'},{id:'N4_b'});
ok('T4 今日 dueList 空', grant229DueList().length===0);
S.dayIndex = 11;
ok('T4 聽日 dueList 有', grant229DueList().length===1 && grant229DueList()[0].gigId==='gig_1990_film_203');

/* ---------- T5：派發守衛 ---------- */
function guardCase(setup){
  freshS(10);
  grant229Record('gig_1990_film_203','N4','test');
  S.dayIndex = 11;
  setup();
  modalCalls = 0; stepCalls = 0;
  const r = grant229PresentDue(()=>{ stepCalls++; });
  return { r:r, q:S.grant229Queue.length, modal:modalCalls, step:stepCalls, shoots:S.shoots.length };
}
let g = guardCase(()=>{ S.flags['done_gig_1990_film_203']=1; });
ok('T5 已殺青→跳過', g.r===false && g.q===0 && g.modal===0 && g.shoots===0);
g = guardCase(()=>{ S.shoots.push({id:'sh_x', gigId:'gig_1990_film_203'}); });
ok('T5 拍攝中→跳過', g.r===false && g.q===0 && g.modal===0 && g.shoots===1);
g = guardCase(()=>{ S.pendingAud.push({gigId:'gig_1990_film_203'}); });
ok('T5 等消息中→跳過', g.r===false && g.q===0 && g.modal===0);
g = guardCase(()=>{ S.booked.push({gigId:'gig_1990_film_203'}); });
ok('T5 已預約試鏡→跳過', g.r===false && g.q===0 && g.modal===0);
freshS(10);
grant229Record('gig_1990_film_203','N4','test');
S.dayIndex = 11;
S.grant229Queue[0].gigId = 'gig_no_such';
modalCalls = 0;
ok('T5 gig 唔存在→跳過', grant229PresentDue(()=>{})===false && S.grant229Queue.length===0 && modalCalls===0);

/* ---------- T5b：N9_a 防撞——film_103 同時係廖炳星引薦 gig（trigger credit_enc79_liu_priority）。
   已持有／已殺青嗰陣，第二朝即派靜默跳過，唔重派／唔出電話（見 V251_C_REPORT §2；v252 重編號 107→103） ---------- */
freshS(10);
grant229RecordFromChoice({id:'N9'},{id:'N9_a'});
S.dayIndex = 11;
S.shoots.push({id:'sh_103', gigId:'gig_1991_film_103'});
modalCalls = 0; stepCalls = 0;
ok('T5b N9_a 103 已持有（引薦攞咗）→跳過', grant229PresentDue(()=>{ stepCalls++; })===false && S.grant229Queue.length===0 && modalCalls===0 && stepCalls===0);
freshS(10);
grant229RecordFromChoice({id:'N9'},{id:'N9_a'});
S.dayIndex = 11;
S.flags['done_gig_1991_film_103']=1;
modalCalls = 0; stepCalls = 0;
ok('T5b N9_a 103 已殺青→跳過', grant229PresentDue(()=>{ stepCalls++; })===false && S.grant229Queue.length===0 && modalCalls===0 && stepCalls===0);

/* ---------- T6：合約條款 ---------- */
let t6a = contract229Terms(gigById('gig_1990_tv_107'));
ok('T6 N-3 2 週×$490＝$980', t6a && t6a.weeks===2 && t6a.weeklyPay===490 && t6a.totalPay===980, JSON.stringify(t6a));
let t6b = contract229Terms(gigById('gig_1990_film_113'));
ok('T6 N-4 2 週×$390＝$780（pay [720,840] 中位 780／12 日 2 週）', t6b && t6b.weeks===2 && t6b.weeklyPay===390 && t6b.totalPay===780, JSON.stringify(t6b));
let t6c = grant229HireTerms(gigById('gig_1990_film_203'));
ok('T6 普通通告：簽約金三成、聲望中位數（pay [55,65] 中位 60／fame [5,10] 中位 8）', t6c && t6c.contract===false && t6c.pay===60 && t6c.signPay===18 && t6c.fame===8, JSON.stringify(t6c));
let t6d = grant229HireTerms(gigById('gig_1990_tv_107'));
ok('T6 合約通告：無簽約金、帶週糧條款', t6d && t6d.contract===true && t6d.signPay===0 && t6d.weeks===2 && t6d.weeklyPay===490 && t6d.totalPay===980, JSON.stringify(t6d));

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
let s7 = contractSetup('gig_1990_tv_107');
ok('T7 合約紀錄開咗（active）', s7.c && s7.c.status==='active' && s7.c.weeks===2 && s7.c.weeklyPay===490);
ok('T7 無拍攝進展→唔出糧', contract229WeeklyTick()===0 && S.money===12000 && s7.c.paidTotal===0);
s7.sh.doneDays = 5;
ok('T7 有進展→出第一週糧 $490（入錢＋入週收入）', contract229WeeklyTick()===1 && S.money===12490 && S.weekEarn===490 && s7.c.paidTotal===490 && s7.c.paidWeeks===1);
ok('T7 同一進展再 tick→唔重複出', contract229WeeklyTick()===0 && S.money===12490);
s7.sh.doneDays = 14;
ok('T7 第二週進展→出第二週糧，總額 $980 封頂', contract229WeeklyTick()===1 && S.money===12980 && s7.c.paidTotal===980);
ok('T7 付清後再 tick→0（唔超總額）', contract229WeeklyTick()===0 && S.money===12980);
let s7b = contractSetup('gig_1990_film_113');
s7b.sh.doneDays = 6;
contract229WeeklyTick();
ok('T7 N-4 第一週 $390', S.money===12390 && s7b.c.paidTotal===390);
S.shoots = [];
contract229WeeklyTick();
ok('T7 shoot 消失→合約閂埋（ended）', s7b.c.status==='ended');

/* ---------- T8：殺青尾糧 ---------- */
let s8 = contractSetup('gig_1990_tv_107');
s8.sh.doneDays = 7; contract229WeeklyTick(); /* 已付一半 $490 */
ok('T8 已付一半→殺青尾糧一半 $490', contract229WrapRemainder(s8.sh)===490);
ok('T8 殺青後合約 done', s8.c.status==='done');
ok('T8 尾糧字句講尾糧唔講餘額', payWrapNote(s8.sh).indexOf('尾糧')>=0 && payWrapNote(s8.sh).indexOf('餘額')<0, payWrapNote(s8.sh));
ok('T8 拍攝卡字句講長期合約＋週糧', contract229CardLine(s8.sh).indexOf('長期合約')>=0 && contract229CardLine(s8.sh).indexOf('每週')>=0, contract229CardLine(s8.sh));
ok('T8 再計尾糧→0', contract229WrapRemainder(s8.sh)===0);
let s8b = contractSetup('gig_1990_film_113');
s8b.sh.doneDays = 6; contract229WeeklyTick(); /* 第一週 $390 */
s8b.sh.doneDays = 12; contract229WeeklyTick(); /* 第二週 $390，付清 */
ok('T8 付清→殺青尾糧 0', contract229WrapRemainder(s8b.sh)===0 && s8b.c.status==='done');
ok('T8 非合約 shoot→尾糧 0', contract229WrapRemainder({gigId:'gig_1990_film_203'})===0);

/* ---------- T9／T10：派發全程＋唔經試鏡 ---------- */
freshS(10);
grant229RecordFromChoice({id:'N4'},{id:'N4_b'});
S.dayIndex = 11; modalCalls = 0; stepCalls = 0; lastModal = null; lastToast = null;
ok('T9 普通通告：何生電話呈現', grant229PresentDue(()=>{ stepCalls++; })===true && modalCalls===1 && stepCalls===1);
ok('T9 modal 講何生來電＋簽約金', lastModal && lastModal.html.indexOf('何生來電')>=0 && lastModal.html.indexOf('簽約金')>=0);
ok('T9 簽約金 $18 已入帳', S.money===12018 && S.weekEarn===18);
ok('T9 shoot 入行程（signedPaid＝三成）', S.shoots.length===1 && S.shoots[0].gigId==='gig_1990_film_203' && S.shoots[0].signedPaid===18 && !S.shoots[0].contract229);
ok('T9 獲聘後 isGigConsumed true（板面鎖死）', isGigConsumed(gigById('gig_1990_film_203'))===true);
ok('T10 派發唔經試鏡（pendingAud／booked 皆空）', S.pendingAud.length===0 && S.booked.length===0);
ok('T10 toast 有通告名', lastToast && lastToast.indexOf('水塘夜戲')>=0, String(lastToast));

freshS(10);
grant229RecordFromChoice({id:'N6'},{id:'N6_a'});
S.dayIndex = 11; modalCalls = 0; stepCalls = 0; lastModal = null;
ok('T9 合約通告：何生電話呈現', grant229PresentDue(()=>{ stepCalls++; })===true && modalCalls===1 && stepCalls===1);
ok('T9 合約 modal 講長期合約＋每週出糧', lastModal && lastModal.html.indexOf('長期合約')>=0 && lastModal.html.indexOf('每週')>=0);
ok('T9 合約：無簽約金入帳', S.money===12000 && S.weekEarn===0);
ok('T9 合約 shoot 有 contract229（2 週×$490）', S.shoots.length===1 && S.shoots[0].contract229 && S.shoots[0].contract229.weeks===2 && S.shoots[0].contract229.weeklyPay===490 && S.shoots[0].signedPaid===0);
ok('T9 合約紀錄 active', S.contracts229.length===1 && S.contracts229[0].status==='active' && S.contracts229[0].totalPay===980);
ok('T9 合約獲聘後 isGigConsumed true', isGigConsumed(gigById('gig_1990_tv_107'))===true);
ok('T10 合約派發唔經試鏡', S.pendingAud.length===0 && S.booked.length===0);

/* ---------- T11 D7：作品類即派 gig 殺青計一個作品（v253 工人 C） ----------
   作品類：gig_1991_film_104《半張船票》男配角（N7_a 即派，category 作品，tier 中級）。
   全鏈：grant229RecordFromChoice(N7,N7_a) → 翌日 grant229PresentDue 派發 → shoot 入行程 →
   殺青結算（生產同一時機：end95AddWrap＋end229AddWrap → wrapHistory.unshift）→
   careerStats95.total＋1、作品牆有佢、countYearMediumWraps(['電影'],1991) 計 1。
   對照：臨記通告類同樣流程 → total 照＋1，但作品牆／提名計數唔計（category 分流）。 */
function wrapSettleD7(sh){
  const g = gigById(sh.gigId);
  end95AddWrap(S, g, sh);
  end229AddWrap(S, g);
  S.wrapHistory = S.wrapHistory || [];
  S.wrapHistory.unshift({
    gigId: sh.gigId, title: sh.title, type: sh.type || "",
    workTitle: g ? (g.workTitle || "") : "", roleLabel: g ? (g.roleLabel || "") : "", year: g ? (g.year || 0) : 0,
    category: g ? (g.category || "") : "", roleScale: g ? (g.roleScale || "") : "",
    totalDays: sh.totalDays || 0, pay: sh.pay || 0, fame: sh.fame || 0,
    popularity: sh.popularity != null ? sh.popularity : 0,
    wrappedDay: S.dayIndex | 0, rating: "順利殺青"
  });
}
const gig104 = gigById('gig_1991_film_104');
ok('T11 film_104 係作品類男配角（N7_a 即派目標）', !!gig104 && gig104.category === '作品' && gig104.type === '電影' && gig104.roleScale === 'film_support_main', gig104 && (gig104.category + '/' + gig104.type + '/' + gig104.roleScale));
freshS(10);
ok('T11 grant：N7_a 記低 film_104（dueDay＝聽日）', grant229RecordFromChoice({ id: 'N7' }, { id: 'N7_a' }) === true && S.grant229Queue.length === 1 && S.grant229Queue[0].gigId === 'gig_1991_film_104' && S.grant229Queue[0].dueDay === 11);
S.dayIndex = 11; modalCalls = 0;
ok('T11 派發：翌日何生電話派 film_104', grant229PresentDue(() => {}) === true && S.shoots.length === 1 && S.shoots[0].gigId === 'gig_1991_film_104');
S.dayIndex = 400; /* 1991-02-04：殺青年份入 1991 提名池 */
wrapSettleD7(S.shoots[0]);
ok('T11 殺青：careerStats95.total＋1（byMedium.film＋1）', careerStats95Of(S).total === 1 && careerStats95Of(S).byMedium.film === 1);
ok('T11 殺青：作品牆有《半張船票》（男配角）', worksWallEntries59().some(e => e.gigId === 'gig_1991_film_104' && e.work === '半張船票' && e.role === '男配角'));
ok('T11 殺青：1991 年電影提名計數＋1', countYearMediumWraps(['電影'], 1991) === 1);
const extraGig = gigs.find(g => g.category === '臨記通告' && g.type === '電影');
ok('T11 對照：庫入面有臨記通告類電影 gig', !!extraGig, extraGig && extraGig.id);
const shExtra = { id: 'sh_test_' + extraGig.id, gigId: extraGig.id, title: extraGig.title, type: extraGig.type, totalDays: extraGig.days || 0, pay: 0, fame: 0, popularity: 0 };
wrapSettleD7(shExtra);
ok('T11 對照：臨記通告殺青 total 照＋1（total＝2）', careerStats95Of(S).total === 2);
ok('T11 對照：臨記通告唔入作品牆', !worksWallEntries59().some(e => e.gigId === extraGig.id) && worksWallEntries59().length === 1);
ok('T11 對照：臨記通告唔計提名數（1991 電影仍係 1）', countYearMediumWraps(['電影'], 1991) === 1);

/* ---------- 尾 ---------- */
console.log(fails.length ? ('\nFAILURES: '+fails.length+' :: '+fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
