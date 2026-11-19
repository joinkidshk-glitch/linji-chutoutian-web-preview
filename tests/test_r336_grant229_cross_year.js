// v20a336 跨年即派修復測試（G-NGAI-3 實駕 BUG-1）
//   機制：runtime GIGS 按日曆年載入（syncGigsForCalendarYear），grant229GigById 舊版淨查當年
//   GIGS；即派表多處跨年配對（1990 gig 喺 1991 播、1992 gig 喺 1991 播、1991 gig 喺 1992 播）
//   靜默 return false，beats 一次性＝永久冇咗，玩家面零提示。
//   修復：grant229GigById 查唔到當年就查 STORY_WIRE.gigsByYear 三年全庫（同 gigRecordById283
//   同一查法，normalize 後返）；grant229DeliverOne 派發成功後將跨年 gig 補入 runtime GIGS
//   （拍攝／殺青路徑 GIGS 反查照常 resolve；補入嗰刻 shoot 已建立，isGigConsumed 擋板面 pool）。
//   沙盒同 test_gig229_grant.js 同模式，但 GIGS 改做「當年年庫」（normalize 後），
//   STORY_WIRE.gigsByYear 係三年 raw 全庫——同 runtime 一致，舊 test 用全庫做 GIGS 遮住咗呢個 bug。
//   A 三個實駕實例：film_210（1990）喺 1991 GIGS、film_108（1992）喺 1991 GIGS、
//     film_114（1991）喺 1992 GIGS，record 成功入 queue
//   B 全表掃描：GRANT229_ENC79 74 行＋GRANT229_CHOICE 44 行＋GRANT229_DRAFT 2 行＋直接呼叫
//     2 張（luk_tease tv_203／pang_finale variety_203），逐行喺「最唔利年份」GIGS 下 record 成功
//   C 派發全程跨年：翌朝 dispatch → shoot 建立＋簽約金三成入帳＋gig 補入 GIGS（shootDaysHint
//     齊＝normalized）＋isGigConsumed true（板面 pool 唔貼）；同年派發唔重複補入
//   D 守衛不變：全庫冇嘅 id 仍然 return false（唔派空頭支票）；一生一次 flag；
//     record 唔補入 GIGS（未派發前板面無污染）
// 用法：node tests/test_r336_grant229_cross_year.js [path-to-index.html]
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
/* runtime 結構（index.html L14809）：gigsByYear[yy] = { version, year, gigs: raw[] } */
const gigsByYear = { 1990:null, 1991:null, 1992:null };
[1990,1991,1992].forEach(yy=>{
  const arr = gigs.filter(g=>g.year===yy);
  if(arr.length) gigsByYear[yy] = { version: pack.version || "gigs_new v1", year: yy, gigs: arr };
});
var STORY_WIRE = { gigsByYear: gigsByYear };

/* ---------- stubs（跟 test_gig229_grant.js B5 harness 模式） ---------- */
var S = null;
var GIGS = [];
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
var fmtDate = function(){ return "1991-01-02"; };
var chk101Html = function(o){ return "<CHK101 amount="+o.amount+">"; };
var shootSpanFor = function(g){ return (g && typeof g.days==="number") ? g.days : 0; };
/* normalizeGigRecord 嘅 era 標籤 helper（真 script 有定義；沙盒 stub，唔影響 shootDaysHint／req 清洗） */
var boardNotePlayerOk = function(){ return false; };
var looksLikeEraId = function(){ return false; };
var humanizeEraId = function(s){ return String(s||""); };

eval(extractConstVar('GRANT229_CHOICE'));
eval(extractConstVar('GRANT229_ENC79'));
eval(extractConstVar('GRANT229_DRAFT'));
eval(extractConstVar('CONTRACT229_GIGS'));
eval(extractFn('bridge56NormalizeGig'));
eval(extractFn('normalizeGigRecord'));
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
eval(extractFn('gigPayExact'));
eval(extractFn('gigActiveShoot'));
eval(extractFn('isGigWrapped'));
eval(extractFn('isGigInProduction'));
eval(extractFn('isGigConsumed'));

/* 模擬 syncGigsForCalendarYear：GIGS＝當年年庫 normalize 後 */
function setYearGigs(y){ GIGS = gigsByYear[y].gigs.map(normalizeGigRecord); }
function inGigs(id){ return (GIGS||[]).some(g=>g && g.id===id); }
function wrongYearFor(gigId){
  const g = gigById(gigId);
  if(!g) return null;
  return g.year===1990 ? 1992 : 1990; /* 1990 gig 用 1992 庫；1991／1992 gig 用 1990 庫——一律跨年 */
}

/* ---------- A：三個實駕實例 ---------- */
(function(){
  freshS(521); setYearGigs(1991);
  ok('A0 前提：film_210 唔喺 1991 GIGS', !inGigs('gig_1990_film_210'));
  const r = grant229Record('gig_1990_film_210', '魏詠男支線', '下次先');
  ok('A1 film_210（1990）喺 1991 record 成功', r===true && S.grant229Queue.length===1 && S.grant229Queue[0].gigId==='gig_1990_film_210', 'queue='+JSON.stringify(S.grant229Queue.map(q=>q.gigId)));
  ok('A1b dueDay＝聽日', S.grant229Queue[0] && S.grant229Queue[0].dueDay===522, 'dueDay='+(S.grant229Queue[0]&&S.grant229Queue[0].dueDay));
})();
(function(){
  freshS(521); setYearGigs(1991);
  ok('A0b 前提：film_108 唔喺 1991 GIGS', !inGigs('gig_1992_film_108'));
  const r = grant229Record('gig_1992_film_108', '魏詠男支線', '認真記低');
  ok('A2 film_108（1992）喺 1991 record 成功', r===true && S.grant229Queue.length===1 && S.grant229Queue[0].gigId==='gig_1992_film_108');
})();
(function(){
  freshS(730); setYearGigs(1992);
  ok('A0c 前提：film_114 唔喺 1992 GIGS', !inGigs('gig_1991_film_114'));
  const r = grant229Record('gig_1991_film_114', '魏詠男支線', '講大話');
  ok('A3 film_114（1991）喺 1992 record 成功', r===true && S.grant229Queue.length===1 && S.grant229Queue[0].gigId==='gig_1991_film_114');
})();

/* ---------- B：全表掃描（逐行最唔利年份） ---------- */
(function(){
  let n=0, bad=[];
  GRANT229_ENC79.forEach(function(row){
    freshS(400);
    const wy = wrongYearFor(row.gigId);
    if(wy==null){ bad.push(row.gigId+'(庫無此 id)'); return; }
    setYearGigs(wy);
    if(inGigs(row.gigId)){ bad.push(row.gigId+'(前提錯：喺錯年庫入面)'); return; }
    const r = grant229Record(row.gigId, row.source, row.reason);
    if(r===true && S.grant229Queue.length===1 && S.grant229Queue[0].gigId===row.gigId) n++;
    else bad.push(row.gigId+'@GIGS'+wy);
  });
  ok('B1 GRANT229_ENC79 全表 '+GRANT229_ENC79.length+' 行跨年 record 全部成功', bad.length===0 && n===GRANT229_ENC79.length, 'pass='+n+' bad='+bad.slice(0,6).join(','));
})();
(function(){
  const ids = Object.keys(GRANT229_CHOICE).map(k=>GRANT229_CHOICE[k].gigId);
  let n=0, bad=[];
  ids.forEach(function(gigId){
    freshS(400);
    const wy = wrongYearFor(gigId);
    if(wy==null){ bad.push(gigId+'(庫無此 id)'); return; }
    setYearGigs(wy);
    const r = grant229Record(gigId, '主線', '');
    if(r===true && S.grant229Queue.length===1) n++; else bad.push(gigId+'@GIGS'+wy);
  });
  ok('B2 GRANT229_CHOICE 全表 '+ids.length+' 行跨年 record 全部成功', bad.length===0 && n===ids.length, 'pass='+n+' bad='+bad.slice(0,6).join(','));
})();
(function(){
  const ids = Object.keys(GRANT229_DRAFT).map(k=>GRANT229_DRAFT[k].gigId).concat(['gig_1991_tv_203','gig_1991_variety_203']);
  let n=0, bad=[];
  ids.forEach(function(gigId){
    freshS(400);
    const wy = wrongYearFor(gigId);
    if(wy==null){ bad.push(gigId+'(庫無此 id)'); return; }
    setYearGigs(wy);
    const r = grant229Record(gigId, '支線', '');
    if(r===true && S.grant229Queue.length===1) n++; else bad.push(gigId+'@GIGS'+wy);
  });
  ok('B3 DRAFT 2 行＋直接呼叫 2 張跨年 record 全部成功', bad.length===0 && n===ids.length, 'pass='+n+' bad='+bad.slice(0,6).join(','));
})();

/* ---------- C：派發全程 ---------- */
(function(){
  freshS(521); setYearGigs(1991);
  const len0 = GIGS.length;
  const r = grant229Record('gig_1990_film_210', '魏詠男支線', '下次先');
  ok('C0 record 後 GIGS 無補入（未派發前板面無污染）', r===true && GIGS.length===len0 && !inGigs('gig_1990_film_210'));
  S.dayIndex = 522; /* 翌朝 */
  const mc0 = modalCalls;
  const presented = grant229PresentDue(function(){});
  const sh = (S.shoots||[]).find(x=>x && x.gigId==='gig_1990_film_210');
  const raw = gigById('gig_1990_film_210');
  const pay = gigPayExact(raw);
  const expectSign = Math.round(pay*0.3);
  ok('C1 跨年 dispatch 呈現（何生來電 modal）', presented===true && modalCalls>mc0, 'modalCalls='+modalCalls);
  ok('C2 shoot 建立＋簽約金三成', !!sh && sh.signedPaid===expectSign, 'pay='+pay+' sign='+(sh&&sh.signedPaid)+' expect='+expectSign);
  ok('C3 簽約金入帳', S.money===12000+expectSign, 'money='+S.money);
  ok('C4 queue 清走＋delivered flag', S.grant229Queue.length===0 && S.flags['grant229_delivered_gig_1990_film_210']===1);
  const inG = (GIGS||[]).filter(g=>g && g.id==='gig_1990_film_210');
  ok('C5 gig 補入 GIGS 一次＋normalized（shootDaysHint＝days）', inG.length===1 && inG[0].shootDaysHint===raw.days, 'count='+inG.length+' hint='+(inG[0]&&inG[0].shootDaysHint)+' days='+raw.days);
  ok('C6 補入後 isGigConsumed＝true（板面 pool 唔貼）', inG.length===1 && isGigConsumed(inG[0])===true);
})();
(function(){
  freshS(521); setYearGigs(1991);
  const len0 = GIGS.length;
  const r = grant229Record('gig_1991_film_205', '魏詠男支線', '認真學');
  S.dayIndex = 522;
  const presented = grant229PresentDue(function(){});
  const sh = (S.shoots||[]).find(x=>x && x.gigId==='gig_1991_film_205');
  const count = (GIGS||[]).filter(g=>g && g.id==='gig_1991_film_205').length;
  ok('C7 同年 dispatch 照常＋唔重複補入', r===true && presented===true && !!sh && GIGS.length===len0 && count===1, 'len='+GIGS.length+'/'+len0+' count='+count);
})();

/* ---------- D：守衛不變 ---------- */
(function(){
  freshS(521); setYearGigs(1991);
  const r = grant229Record('gig_1990_film_999', '測試', '');
  ok('D1 全庫冇嘅 id 仍然 return false＋唔入 queue＋唔設 flag', r===false && S.grant229Queue.length===0 && !S.flags['grant229_recorded_gig_1990_film_999']);
  ok('D1b grant229GigById(冇嘅 id)＝null', grant229GigById('gig_1990_film_999')===null);
})();
(function(){
  freshS(521); setYearGigs(1991);
  const r1 = grant229Record('gig_1990_film_210', '魏詠男支線', '下次先');
  const r2 = grant229Record('gig_1990_film_210', '魏詠男支線', '下次先');
  ok('D2 一生一次：第二次 record false＋queue 得一筆', r1===true && r2===false && S.grant229Queue.length===1);
})();

if(fails.length){ console.log('FAILURES: '+fails.length+' :: '+fails.join(' | ')); process.exit(1); }
console.log('ALL PASS');
