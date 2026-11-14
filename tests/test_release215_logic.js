// v20a215 推出日提及・邏輯測試：
// (a) 臨記級通告喺推出季首日前已殺青 → 推出日朝早晨報有呢則短訊（作品名＋播出資訊、冇玩家名、fameDelta 0）
// (b) 配角級以上通告唔出呢則
// (c) 推出日當日／之後先殺青唔出（唔補出）；未到推出日唔出
// (d) 同一張通告唔重複出（去重 key release:<gigId>）
// (e) 撞獎項報同一朝（同 enqueuedDay）→ 併一份報，獎項做頭條、推出做短訊，聲望只計獎項嗰份
// (f) source "release" 正規化保留＋排序永遠排最後（唔搶頭條）；淨係得佢嗰陣先做頭版
// (g) 文案用季節寫法，唔讀 releaseLabel（賀歲檔 label 同季首日對撞）；書面語、唔點名玩家
// (h) 跨年查 gig（GIGS 換池後經 STORY_WIRE.gigsByYear 搵返）＋逾期載入照出＋tick／懶掃兩條路等價
// 反證：對 pristine main 行 → release215* 唔存在 → 乾淨 FAIL（exit 1，唔 crash）。
// 用法：node tests/test_release215_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
const ASSERT_NAMES = [
  '觸發日換算：1990 春 59／夏 151／秋 243／冬 334',
  '觸發日換算：1991 春 424／1992 春 790（閏年）',
  '舊曆年：1988 秋→243、1989 夏→516',
  '無效季節／年份 → null',
  '文案：廣告《便利店短片》春季推出＋廣告時段',
  '文案：電影《烈日碼頭》夏季上映＋院線排片',
  '文案：電視劇《屋簷下》冬季播出＋黃金時段',
  '文案唔讀 releaseLabel：有賀歲檔 label 都唔出賀歲／農曆／新年',
  '文案唔點名玩家：headline／dek 冇阿偉／陳偉翔',
  '(a) 春季臨記：推出日朝早晨報有呢則，頭版係佢、source release、fameDelta 0',
  '(a)  commit 後聲望唔郁、剪報留底',
  '(d) 去重：再掃再拉都唔出第二則',
  '(b) 配角級唔出呢則',
  '(c) 推出日當日先殺青唔出',
  '(c) 推出日之後先殺青唔出',
  '(c) 未到推出日唔出',
  '(e) 撞獎項報同一朝：併一份報，獎項做頭條、推出做短訊、聲望只計獎項',
  '(f) 排序：release 唔搶 wrap 頭條',
  '(f) 排序：淨係得 release 嗰陣先做頭版',
  '(f) source 正規化：release 保留、未知 source 跌返 wrap',
  '(h) 跨年查 gig：只在 gigsByYear 嘅通告都搵到、照出',
  '(h) 逾期載入：推出日過咗、殺青早過推出日，照出（publishDay＝推出日）',
  '(h) tick 路徑：直接掃描入隊，enqueuedDay＝尋日、publishDay＝推出日'
];
function cleanFailMissing(what){
  console.log('抽唔到 ' + what + '（呢個版本冇 v20a215）：以下斷言全部 FAIL');
  ASSERT_NAMES.forEach(n=>{ console.log('FAIL ' + n); fails.push(n); });
  console.log('\nFAILED: ' + fails.length);
  process.exit(1);
}
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) cleanFailMissing('function ' + name);
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){
    if(html[j]==='{') depth++;
    else if(html[j]==='}'){ depth--; if(depth===0) break; }
  }
  return html.slice(i, j+1);
}
function extractConst(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i<0) cleanFailMissing('const ' + name);
  let depth=0, started=false;
  for(let k=i;k<html.length;k++){
    const ch=html[k];
    if(ch==='{'||ch==='['){ depth++; started=true; }
    else if(ch==='}'||ch===']'){ depth--; if(started&&depth===0) return html.slice(i,k+1)+';'; }
    else if(ch===';'&&!started) return html.slice(i,k+1);
  }
  cleanFailMissing('const ' + name + ' 結尾');
}

/* ---------- 沙盒 ---------- */
var document = {
  getElementById(){ return { classList:{ contains(){ return false; } } }; },
  querySelector(){ return null; }, querySelectorAll(){ return []; },
  createElement(){ return {}; }, body: {}
};
var saveQ = function(){};
var news82IsHead = function(){ return false; };
let S = null;
let GIGS = [];
let STORY_WIRE = { gigsByYear: {} };

for(const c of ['RELEASE215_SEASON_MONTH','RELEASE215_SEASON_WORD',
  'PRESS94_STRONG_NAMED','PRESS94_BASE_LABEL','PRESS94_NAMED_LABEL',
  'PRESS94_BASE_SCALES','PRESS94_NAMED_SCALES','PAPER_TOPIC_STARS'])
  eval(extractConst(c).replace('const ' + c + ' =', 'var ' + c + ' ='));
for(const f of ['release215GameYear','release215ReleaseDay','release215LookupGig',
  'release215CopyFor','release215EnqueueDue',
  'press94ScaleOf','press94RoleClass','press94IsBaseRole','postShootDisplayTitle',
  'newspaperLookupGig','ensureNewspaperQueue','ensureNewspaperClippings',
  'newspaperEventSeen','enqueueNewspaperItem','newspaperDueItems',
  'newspaperTopicKey','buildNewspaperEdition','pullDueNewspaperEdition',
  'commitMorningPaper']) eval(extractFn(f));

/* ---------- 世界 ---------- */
const G_BASE_AD = { id:"g_base_ad", year:1990, season:"春", type:"廣告",
  title:"《便利店短片》廣告路人 B", workTitle:"便利店短片", roleLabel:"廣告路人 B", roleScale:"ad_extra_day" };
const G_BASE_FILM = { id:"g_base_film", year:1990, season:"夏", type:"電影",
  title:"《烈日碼頭》臨記", workTitle:"烈日碼頭", roleLabel:"臨記", roleScale:"film_extra_day" };
const G_NAMED = { id:"g_named", year:1990, season:"夏", type:"電影",
  title:"《夜半靈異》男配角", workTitle:"夜半靈異", roleLabel:"男配角", roleScale:"film_support" };
const G_BASE_TV = { id:"g_base_tv", year:1990, season:"冬", type:"電視劇",
  title:"《屋簷下》臨時演員", workTitle:"屋簷下", roleLabel:"臨時演員", roleScale:"tv_extra_day" };
const G_PACK = { id:"g_pack", year:1991, season:"春", type:"電影",
  title:"《山海》臨記", workTitle:"山海", roleLabel:"臨記", roleScale:"film_extra_day" };
GIGS = [G_BASE_AD, G_BASE_FILM, G_NAMED, G_BASE_TV];
STORY_WIRE = { gigsByYear: { 1991: { year:1991, gigs:[G_PACK] } } };

function freshS(day, wraps){
  S = { dayIndex: day, fame: 5, popularity: 3, stress: 0, money: 12000,
    wrapHistory: wraps || [], newspaperQueue: [], newspaperClippings: [],
    pendingMorningPaper: null, newspaperLastPresentedDay: null, mockRumors: [], flags: {} };
  return S;
}
function wrapEntry(gig, wrappedDay){
  return { gigId: gig.id, title: gig.title, type: gig.type, workTitle: gig.workTitle,
    roleLabel: gig.roleLabel, year: gig.year, totalDays: 2, pay: 950, fame: 1,
    popularity: 0, wrappedDay: wrappedDay, rating: "順利殺青" };
}
function dayIdx(y, m, d){ return Math.round((Date.UTC(y, m-1, d) - Date.UTC(1990, 0, 1)) / 86400000); }

/* ---------- 觸發日換算 ---------- */
ok('觸發日換算：1990 春 59／夏 151／秋 243／冬 334',
  release215ReleaseDay(1990,"春")===dayIdx(1990,3,1) && release215ReleaseDay(1990,"春")===59 &&
  release215ReleaseDay(1990,"夏")===dayIdx(1990,6,1) && release215ReleaseDay(1990,"夏")===151 &&
  release215ReleaseDay(1990,"秋")===dayIdx(1990,9,1) && release215ReleaseDay(1990,"秋")===243 &&
  release215ReleaseDay(1990,"冬")===dayIdx(1990,12,1) && release215ReleaseDay(1990,"冬")===334);
ok('觸發日換算：1991 春 424／1992 春 790（閏年）',
  release215ReleaseDay(1991,"春")===dayIdx(1991,3,1) && release215ReleaseDay(1991,"春")===424 &&
  release215ReleaseDay(1992,"春")===dayIdx(1992,3,1) && release215ReleaseDay(1992,"春")===790);
ok('舊曆年：1988 秋→243、1989 夏→516',
  release215ReleaseDay(1988,"秋")===243 && release215ReleaseDay(1989,"夏")===516);
ok('無效季節／年份 → null',
  release215ReleaseDay(1990,"不限")===null && release215ReleaseDay(1990,"")===null &&
  release215ReleaseDay(0,"春")===null && release215ReleaseDay(2000,"春")===null);

/* ---------- 文案 ---------- */
const copyAd = release215CopyFor(wrapEntry(G_BASE_AD, 30), G_BASE_AD);
ok('文案：廣告《便利店短片》春季推出＋廣告時段',
  copyAd && copyAd.headline==="《便利店短片》春季推出" && copyAd.dek.indexOf("春季推出")>=0 && copyAd.dek.indexOf("廣告時段")>=0);
const copyFilm = release215CopyFor(wrapEntry(G_BASE_FILM, 100), G_BASE_FILM);
ok('文案：電影《烈日碼頭》夏季上映＋院線排片',
  copyFilm && copyFilm.headline==="《烈日碼頭》夏季上映" && copyFilm.dek.indexOf("院線排片")>=0);
const copyTv = release215CopyFor(wrapEntry(G_BASE_TV, 300), G_BASE_TV);
ok('文案：電視劇《屋簷下》冬季播出＋黃金時段',
  copyTv && copyTv.headline==="《屋簷下》冬季播出" && copyTv.dek.indexOf("黃金時段")>=0);
const copyLabel = release215CopyFor(wrapEntry(G_BASE_FILM, 100),
  Object.assign({}, G_BASE_FILM, { releaseLabel:"賀歲檔農曆新年上映" }));
ok('文案唔讀 releaseLabel：有賀歲檔 label 都唔出賀歲／農曆／新年',
  copyLabel && copyLabel.headline.indexOf("賀歲")<0 && copyLabel.headline.indexOf("農曆")<0 &&
  copyLabel.dek.indexOf("賀歲")<0 && copyLabel.dek.indexOf("農曆")<0 && copyLabel.dek.indexOf("新年")<0);
ok('文案唔點名玩家：headline／dek 冇阿偉／陳偉翔',
  [copyAd, copyFilm, copyTv].every(c=> c && c.headline.indexOf("阿偉")<0 && c.headline.indexOf("陳偉翔")<0 &&
    c.dek.indexOf("阿偉")<0 && c.dek.indexOf("陳偉翔")<0));

/* ---------- (a) 推出日朝早有呢則 ---------- */
freshS(59, [wrapEntry(G_BASE_AD, 30)]);
const edA = pullDueNewspaperEdition();
ok('(a) 春季臨記：推出日朝早晨報有呢則，頭版係佢、source release、fameDelta 0',
  !!edA && edA.headline==="《便利店短片》春季推出" && edA.source==="release" &&
  (Number(edA.fameDelta)||0)===0 && (edA.eventKeys||[]).indexOf("release:g_base_ad")>=0);
const fameA = Number(S.fame)||0;
if(edA) commitMorningPaper(edA, { persist:false });
ok('(a)  commit 後聲望唔郁、剪報留底',
  (Number(S.fame)||0)===fameA && (S.newspaperClippings||[]).length===1 &&
  ((S.newspaperClippings[0].eventKeys||[]).indexOf("release:g_base_ad")>=0));

/* ---------- (d) 去重 ---------- */
release215EnqueueDue();
const edD = pullDueNewspaperEdition();
ok('(d) 去重：再掃再拉都唔出第二則',
  (S.newspaperQueue||[]).length===0 && !edD && (S.newspaperClippings||[]).length===1);

/* ---------- (b) 配角級唔出 ---------- */
freshS(151, [wrapEntry(G_NAMED, 100)]);
ok('(b) 配角級唔出呢則', pullDueNewspaperEdition()===null && (S.newspaperQueue||[]).length===0);

/* ---------- (c) 殺青時機 ---------- */
freshS(151, [wrapEntry(G_BASE_FILM, 151)]);
ok('(c) 推出日當日先殺青唔出', pullDueNewspaperEdition()===null && (S.newspaperQueue||[]).length===0);
freshS(151, [wrapEntry(G_BASE_FILM, 152)]);
ok('(c) 推出日之後先殺青唔出', pullDueNewspaperEdition()===null && (S.newspaperQueue||[]).length===0);
freshS(58, [wrapEntry(G_BASE_AD, 30)]);
ok('(c) 未到推出日唔出', pullDueNewspaperEdition()===null && (S.newspaperQueue||[]).length===0);

/* ---------- (e) 撞獎項報同一朝 ---------- */
freshS(151, [wrapEntry(G_BASE_FILM, 100)]);
enqueueNewspaperItem({ eventKey:"award:1990:award_harbour_film", source:"award",
  enqueuedDay:150, publishDay:151, fameDelta:2, paperName:"娛樂快報",
  headline:"頒獎見報", dek:"三" }, { persist:false });
const edE = pullDueNewspaperEdition();
const shortsE = (edE && edE.shorts) || [];
ok('(e) 撞獎項報同一朝：併一份報，獎項做頭條、推出做短訊、聲望只計獎項',
  !!edE && edE.headline==="頒獎見報" && (Number(edE.fameDelta)||0)===2 &&
  (edE.eventKeys||[]).length===2 && (edE.eventKeys||[]).indexOf("release:g_base_film")>=0 &&
  (edE.eventKeys||[]).indexOf("award:1990:award_harbour_film")>=0 &&
  shortsE.some(s=> s && s.headline==="《烈日碼頭》夏季上映" && s.source==="release") &&
  (S.newspaperQueue||[]).length===0);
if(edE) commitMorningPaper(edE, { persist:false });
ok('(e) 撞獎項報同一朝：commit 後聲望只加獎項嗰 2 分', (Number(S.fame)||0)===7);

/* ---------- (f) 排序＋source ---------- */
const relItem = { eventKey:"release:g_base_film", source:"release", enqueuedDay:150, publishDay:151,
  fameDelta:0, paperName:"娛樂版", headline:"《烈日碼頭》夏季上映", dek:"夏" };
const wrapItem = { eventKey:"wrap:g9:100", source:"wrap", enqueuedDay:150, publishDay:151,
  fameDelta:1, paperName:"娛樂版", headline:"甲殺青", dek:"一行" };
ok('(f) 排序：release 唔搶 wrap 頭條',
  buildNewspaperEdition([relItem, wrapItem], 151).headline==="甲殺青" &&
  buildNewspaperEdition([wrapItem, relItem], 151).headline==="甲殺青");
ok('(f) 排序：淨係得 release 嗰陣先做頭版',
  buildNewspaperEdition([relItem], 151).headline==="《烈日碼頭》夏季上映");
freshS(0, []);
const relEnq = enqueueNewspaperItem({ eventKey:"release:g_base_ad", source:"release",
  enqueuedDay:0, publishDay:1, fameDelta:0, paperName:"娛樂版", headline:"測", dek:"" }, { persist:false });
const bogEnq = enqueueNewspaperItem({ eventKey:"wrap:gx:0", source:"bogus",
  enqueuedDay:0, publishDay:1, fameDelta:1, paperName:"娛樂版", headline:"測二", dek:"" }, { persist:false });
ok('(f) source 正規化：release 保留、未知 source 跌返 wrap',
  !!relEnq && relEnq.source==="release" && !!bogEnq && bogEnq.source==="wrap");

/* ---------- (h) 跨年查 gig／逾期／tick ---------- */
freshS(424, [wrapEntry(G_PACK, 400)]);
const edH = pullDueNewspaperEdition();
ok('(h) 跨年查 gig：只在 gigsByYear 嘅通告都搵到、照出',
  !!edH && edH.headline==="《山海》春季上映" && (edH.eventKeys||[]).indexOf("release:g_pack")>=0);
freshS(200, [wrapEntry(G_BASE_FILM, 100)]);
const nOver = release215EnqueueDue();
const qOver = (S.newspaperQueue||[])[0];
ok('(h) 逾期載入：推出日過咗、殺青早過推出日，照出（publishDay＝推出日）',
  nOver===1 && !!qOver && (qOver.publishDay|0)===151 && (qOver.enqueuedDay|0)===199);
ok('(h) 逾期載入：pullDue 照拉到呢份逾期報', !!pullDueNewspaperEdition());
freshS(151, [wrapEntry(G_BASE_FILM, 100)]);
const nTick = release215EnqueueDue();
const qTick = (S.newspaperQueue||[])[0];
ok('(h) tick 路徑：直接掃描入隊，enqueuedDay＝尋日、publishDay＝推出日',
  nTick===1 && !!qTick && (qTick.enqueuedDay|0)===150 && (qTick.publishDay|0)===151 &&
  qTick.eventKey==="release:g_base_film" && (Number(qTick.fameDelta)||0)===0);

console.log(fails.length ? ('\nFAILED: ' + fails.length) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
