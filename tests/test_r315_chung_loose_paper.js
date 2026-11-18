// v20a315 Q25 鍾楚凝 Beat 3「講出去」報紙花邊回音測試：
//   (A) 揀「講出去」（授 chung_loose_talk）→ 下一期晨報短訊列尾有花邊（細欄，唔係頭版），唔取代當日輪替花邊
//   (B) 文案：有「聽聞」／「女星」／「赴加」／「手續」；無「鍾楚凝」（DLG 明寫沒有點名）、無玩家名、無高調字眼
//   (C) 只出一次：commit 記 S.flags.chungLooseTalkPaper315，第二期唔再出
//   (D) 舊檔（已有 chung_loose_talk 旗，未出過）補出一次唔重複
//   (E) 泄漏花邊唔開風聲窗（enc79PaperWhisper 未知 id 係 no-op）；同 v302 告別花邊互不干擾
//   (F) 靜態：chung_f_clue 對白／授旗／fav／即派／heartCold／patron 兩閘唔郁；v302 花邊唔郁
// 用法：node tests/test_r315_chung_loose_paper.js [path-to-index.html]
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

eval(extractConstVar('PAPER_SIDE_ITEMS'));
eval(extractConstVar('PAPER_TOPIC_STARS'));
eval(extractConstVar('CHUNG_ADVICE_TEXT229'));
for(const f of ['paperSideItemForDay','newspaperTopicKey','newspaperPrevTopicKey','newspaperSerialLine','buildNewspaperEdition','commitMorningPaper','enc79PaperWhisper','chungAdviceCardHeld229']){
  const src = extractFn(f);
  if(!src){ ok('抽取 function '+f, false); }
  else eval(src);
}

/* ---------- stubs ---------- */
var S = null;
var clippings = [];
var whisperCalls = [];
function displayDateObj(){ return { getFullYear: function(){ return 1992; } }; }
function fmtNewspaperDate(day){ return '1992年秋'; }
function fmtDateShort(){ return '1992/9/1'; }
function newspaperLookupGig(gid){ return null; }
function ensureNewspaperClippings(){ return clippings; }
function news82IsHead(wid){ return false; }
function enc79GrantWhisper(sid, via){ whisperCalls.push(sid+'|'+via); }
function syncDualTracks(){}
function paintBar(){}
function readDualTracks(){ return { stageVolume: 0 }; }
function saveQ(){}
function familyPaperEchoTick(){}

function freshS(){
  return { dayIndex: 701, fame: 10, flags: {}, stars: {}, wrapHistory: [],
    newspaperQueue: [], newspaperClippings: [], pendingMorningPaper: null,
    newspaperLastPresentedDay: null };
}
function wrapBatch(n, day){
  const b = [];
  for(let i=0;i<n;i++) b.push({ eventKey:'wrap:g'+i+':0', source:'wrap', enqueuedDay:(day||701)-1, publishDay:(day||701), fameDelta:1, paperName:'娛樂版', headline:'殺青'+i, dek:'一行'+i });
  return b;
}
function looseShort(ed){
  return (ed && ed.shorts || []).filter(s=>s && s.sideId==='side_chung_loose315');
}
function farewellShort(ed){
  return (ed && ed.shorts || []).filter(s=>s && s.sideId==='side_chung_farewell302');
}
const BANNED = ['鍾楚凝','宣布','轟動','離開影壇','告別影壇','退出影壇','引退','移民','震撼','大鑼大鼓','阿偉','陳偉翔'];

/* ---------- A1：無旗 → 唔出 ---------- */
S = freshS();
let ed0 = buildNewspaperEdition(wrapBatch(1, 701), 701);
ok('A1 無 chung_loose_talk → 無泄漏花邊', looseShort(ed0).length===0);
ok('A1 無旗 → 當日輪替花邊照有', ed0 && ed0.shorts.some(s=>s && s.source==='side' && s.sideId!=='side_chung_loose315'));

/* ---------- A2：有旗 → 下一期有花邊 ---------- */
S = freshS();
S.flags.chung_loose_talk = 1;
clippings = [];
let ed1 = buildNewspaperEdition(wrapBatch(1, 701), 701);
const f1 = looseShort(ed1);
ok('A2 有旗 → 下一期有一則泄漏花邊', f1.length===1, 'shorts='+(ed1.shorts||[]).length);
ok('A2 泄漏花邊係短訊列尾（唔係頭條）', ed1.headline==='殺青0' && (ed1.shorts||[])[(ed1.shorts||[]).length-1].sideId==='side_chung_loose315');
ok('A2 泄漏花邊欄位（花邊短訊／side／fameDelta 0）',
  f1[0] && f1[0].paperName==='花邊短訊' && f1[0].source==='side' && f1[0].fameDelta===0);
ok('A2 泄漏花邊文案逐字（headline／dek）',
  f1[0] && f1[0].headline==='聽聞有女星赴加手續辦緊' &&
  f1[0].dek==='有行內人表示，有女星近日正辦赴加手續，詳情未明。');

/* ---------- A3：唔取代當日輪替花邊 ---------- */
const rot701 = paperSideItemForDay(701);
ok('A3 當日輪替花邊仍在（唔係被取代）', ed1.shorts.some(s=>s && s.headline===rot701.headline), 'rot='+rot701.headline);
ok('A3 注入點喺 build 尾段（sideItem 之後、v302 block 之後）',
  (extractFn('buildNewspaperEdition').indexOf('side_chung_loose315') > extractFn('buildNewspaperEdition').indexOf('side_chung_farewell302')));

/* ---------- B：文案斷言 ---------- */
const copy1 = (f1[0].headline||'') + (f1[0].dek||'');
ok('B 文案有聽聞／女星／赴加／手續',
  copy1.indexOf('聽聞')>=0 && copy1.indexOf('女星')>=0 && copy1.indexOf('赴加')>=0 && copy1.indexOf('手續')>=0);
const badHit = BANNED.filter(w=>copy1.indexOf(w)>=0);
ok('B 文案無鍾楚凝／無玩家名／無高調字眼（鍾楚凝／宣布／轟動／離開影壇／告別影壇／退出影壇／引退／移民／震撼／大鑼大鼓／阿偉／陳偉翔）',
  badHit.length===0, 'hit='+badHit.join(','));

/* ---------- C：只出一次 ---------- */
whisperCalls = [];
commitMorningPaper(ed1, { persist:false });
ok('C commit 記已出旗 chungLooseTalkPaper315', S.flags.chungLooseTalkPaper315===1);
ok('C 剪報入面泄漏花邊只得一次',
  clippings.length===1 && clippings[0].shorts.filter(s=>s && s.sideId==='side_chung_loose315').length===1);
let ed2 = buildNewspaperEdition(wrapBatch(1, 702), 702);
ok('C 第二期 build → 唔再出', looseShort(ed2).length===0);
commitMorningPaper(ed2, { persist:false });
ok('C 第二期 commit 後旗仍係 1（唔重複記）', S.flags.chungLooseTalkPaper315===1);
ok('C 兩期剪報加埋泄漏花邊仍只得一次',
  clippings.reduce((n,c)=>n+c.shorts.filter(s=>s && s.sideId==='side_chung_loose315').length, 0)===1);

/* ---------- D：舊檔補出 ---------- */
S = freshS(); S.flags.chung_loose_talk = 1; clippings = [];
let edOld = buildNewspaperEdition(wrapBatch(1, 701), 701);
ok('D1 舊檔（已有 chung_loose_talk、未出過）→ 補出一次', looseShort(edOld).length===1);
commitMorningPaper(edOld, { persist:false });
ok('D1 舊檔 commit 後記旗', S.flags.chungLooseTalkPaper315===1);
ok('D1 舊檔第二期唔再出', looseShort(buildNewspaperEdition(wrapBatch(1, 702), 702)).length===0);

/* ---------- E：唔開風聲窗；同 v302 互不干擾 ---------- */
whisperCalls = [];
enc79PaperWhisper('side_chung_loose315');
ok('E enc79PaperWhisper（未知 id）→ no-op，唔開風聲', whisperCalls.length===0);
S = freshS();
S.flags.chung_loose_talk = 1;
S.stars.chung_choning = { fav: 60, beatsDone: { chung_farewell: 690 } };
clippings = []; whisperCalls = [];
let edBoth = buildNewspaperEdition(wrapBatch(1, 701), 701);
ok('E 兩旗齊備 → 兩則先後出現（泄漏＋告別）', looseShort(edBoth).length===1 && farewellShort(edBoth).length===1);
ok('E 泄漏排告別之後（Beat 3 早、告別遲，列尾次序跟 build 次序）',
  edBoth.shorts.findIndex(s=>s && s.sideId==='side_chung_farewell302') < edBoth.shorts.findIndex(s=>s && s.sideId==='side_chung_loose315'));
commitMorningPaper(edBoth, { persist:false });
ok('E 兩則 commit 各記其旗', S.flags.chungLooseTalkPaper315===1 && S.flags.chungFarewellPaper302===1);
ok('E 含兩則嗰期 commit 只開 lu 風聲（side_lu_concert 係當日輪替外加項），兩則 chung 花邊唔開', whisperCalls.length===1 && whisperCalls[0]==='luk_baakyin|paper', JSON.stringify(whisperCalls));

/* ---------- S：靜態——唔郁清單 ---------- */
ok('S1 PAPER_SIDE_ITEMS 仍係 39 則', Array.isArray(PAPER_SIDE_ITEMS) && PAPER_SIDE_ITEMS.length===39, 'count='+(PAPER_SIDE_ITEMS && PAPER_SIDE_ITEMS.length));
ok('S1 chung_f_clue 對白唔郁（門半掩／加拿大手續／第二天整層樓）',
  html.indexOf('金鐘創意後台走廊，門半掩住')>=0 &&
  html.indexOf('第二天，整層樓都知道。《維港日報》花邊多了一句碎片，沒有點名')>=0);
ok('S1 授旗唔郁（chung_loose_talk／chung_kept_quiet）',
  html.indexOf('flags: ["chung_loose_talk"]')>=0 && html.indexOf('flags: ["chung_kept_quiet"]')>=0);
ok('S1 fav 判定唔郁（講兩句 −2／守口 ＋3）', html.indexOf('if(has("講兩句")) return { fav:-2 }')>=0);
ok('S1 即派唔郁（講兩句→gig_1990_tv_207）',
  html.indexOf('key:"講兩句", gigId:"gig_1990_tv_207"')>=0);
ok('S1 heartCold 分流唔郁', html.indexOf('(S.flags||{}).chung_loose_talk && D.heartCold')>=0);
ok('S1 patron 兩閘唔郁（冷版有 loose_talk／暖版排除）',
  html.indexOf('id:"chung_patron_cold"')>=0 && html.indexOf('id:"chung_patron"')>=0 &&
  html.indexOf('!(S.flags||{}).chung_loose_talk')>=0);
ok('S1 v302 告別花邊唔郁', html.indexOf('side_chung_farewell302')>=0 && html.indexOf('聽聞鍾楚凝赴加小住，權當一個長外景')>=0);
ok('S1 enc79PaperWhisper 查表唔郁（只得三項）',
  html.indexOf('side_lu_concert:"luk_baakyin"')>=0 && html.indexOf('side_chung_loose315')>=0 &&
  extractFn('enc79PaperWhisper').indexOf('side_chung_loose315')<0);
const gigsLib = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'content', 'gigs_new.json'), 'utf8')).gigs;
ok('S1 gigs_new.json 仍係 306 張', gigsLib.length===306, 'count='+gigsLib.length);

if(fails.length){ console.log('FAILURES: '+fails.join(', ')); process.exit(1); }
console.log('ALL PASS');
