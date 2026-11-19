// v20a302 Q15 鍾楚凝告別補報紙花邊測試：
//   (A) 告別完成 → 下一期晨報短訊列尾有花邊（細欄，唔係頭版），唔取代當日輪替花邊
//   (B) 文案：有「鍾楚凝」／「聽聞」／「小住」／「外景」；無玩家名、無高調字眼
//   (C) 只出一次：commit 記 S.flags.chungFarewellPaper302，第二期唔再出
//   (D) 舊檔（已有 chungAdviceHeld229／beatsDone.chung_farewell，未出過）補出一次唔重複
//   (E) 告別未做唔出；告別花邊唔開風聲窗（enc79PaperWhisper 未知 id 係 no-op）
//   (F) 忠告試鏡提示機制照舊（chungAdviceCardHeld229）；靜態：輪替池 39 則、告別對白、結局回望唔郁
// 用法：node tests/test_r302_chung_farewell_paper.js [path-to-index.html]
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
function farewellShort(ed){
  return (ed && ed.shorts || []).filter(s=>s && s.sideId==='side_chung_farewell302');
}
const BANNED = ['宣布','轟動','離開影壇','告別影壇','退出影壇','引退','移民','震撼','大鑼大鼓','阿偉','陳偉翔'];

/* ---------- A1：告別未做 → 唔出 ---------- */
S = freshS();
let ed0 = buildNewspaperEdition(wrapBatch(1, 701), 701);
ok('A1 告別未做 → 無告別花邊', farewellShort(ed0).length===0);
ok('A1 告別未做 → 當日輪替花邊照有', ed0 && ed0.shorts.some(s=>s && s.source==='side' && s.sideId!=='side_chung_farewell302'));

/* ---------- A2：告別完成（beatsDone）→ 下一期有花邊 ---------- */
S = freshS();
S.stars.chung_choning = { fav: 60, beatsDone: { chung_farewell: 690 } };
clippings = [];
let ed1 = buildNewspaperEdition(wrapBatch(1, 701), 701);
const f1 = farewellShort(ed1);
ok('A2 beatsDone → 下一期有一則告別花邊', f1.length===1, 'shorts='+(ed1.shorts||[]).length);
ok('A2 告別花邊係短訊列尾（唔係頭條）', ed1.headline==='殺青0' && (ed1.shorts||[])[(ed1.shorts||[]).length-1].sideId==='side_chung_farewell302');
ok('A2 告別花邊欄位（花邊短訊／side／fameDelta 0）',
  f1[0] && f1[0].paperName==='花邊短訊' && f1[0].source==='side' && f1[0].fameDelta===0);
ok('A2 告別花邊文案逐字（headline／dek）',
  f1[0] && f1[0].headline==='聽聞鍾楚凝赴加小住，權當一個長外景' &&
  f1[0].dek==='有行內人表示，鍾楚凝近日將赴加拿大，小住一段日子，權當一個長一點的外景，歸期未定。');

/* ---------- A3：唔取代當日輪替花邊 ---------- */
const rot701 = paperSideItemForDay(701);
ok('A3 當日輪替花邊仍在（唔係被取代）', ed1.shorts.some(s=>s && s.headline===rot701.headline), 'rot='+rot701.headline);
ok('A3 注入點喺 build 尾段（sideItem 之後）',
  (extractFn('buildNewspaperEdition').indexOf('side_chung_farewell302') > extractFn('buildNewspaperEdition').indexOf('paperSideItemForDay(day)')));

/* ---------- B：文案斷言 ---------- */
const copy1 = (f1[0].headline||'') + (f1[0].dek||'');
ok('B 文案有鍾楚凝／聽聞／小住／外景',
  copy1.indexOf('鍾楚凝')>=0 && copy1.indexOf('聽聞')>=0 && copy1.indexOf('小住')>=0 && copy1.indexOf('外景')>=0);
const badHit = BANNED.filter(w=>copy1.indexOf(w)>=0);
ok('B 文案無高調字眼／無玩家名（宣布／轟動／離開影壇／告別影壇／退出影壇／引退／移民／震撼／大鑼大鼓／阿偉／陳偉翔）',
  badHit.length===0, 'hit='+badHit.join(','));

/* ---------- C：只出一次 ---------- */
whisperCalls = [];
commitMorningPaper(ed1, { persist:false });
ok('C commit 記已出旗 chungFarewellPaper302', S.flags.chungFarewellPaper302===1);
ok('C 剪報入面告別花邊只得一次',
  clippings.length===1 && clippings[0].shorts.filter(s=>s && s.sideId==='side_chung_farewell302').length===1);
let ed2 = buildNewspaperEdition(wrapBatch(1, 702), 702);
ok('C 第二期 build → 唔再出', farewellShort(ed2).length===0);
commitMorningPaper(ed2, { persist:false });
ok('C 第二期 commit 後旗仍係 1（唔重複記）', S.flags.chungFarewellPaper302===1);
ok('C 兩期剪報加埋告別花邊仍只得一次',
  clippings.reduce((n,c)=>n+c.shorts.filter(s=>s && s.sideId==='side_chung_farewell302').length, 0)===1);

/* ---------- D：舊檔補出 ---------- */
S = freshS(); S.flags.chungAdviceHeld229 = 1; clippings = [];
let edOld = buildNewspaperEdition(wrapBatch(1, 701), 701);
ok('D1 舊檔（得 chungAdviceHeld229）→ 補出一次', farewellShort(edOld).length===1);
commitMorningPaper(edOld, { persist:false });
ok('D1 舊檔 commit 後記旗', S.flags.chungFarewellPaper302===1);
ok('D1 舊檔第二期唔再出', farewellShort(buildNewspaperEdition(wrapBatch(1, 702), 702)).length===0);
S = freshS(); S.stars.chung_choning = { fav: 60, beatsDone: { chung_farewell: 650 } }; clippings = [];
let edOld2 = buildNewspaperEdition(wrapBatch(1, 701), 701);
ok('D2 舊檔（得 beatsDone、無 advice 旗）→ 補出一次', farewellShort(edOld2).length===1);

/* ---------- E：唔開風聲窗 ---------- */
whisperCalls = [];
enc79PaperWhisper('side_chung_farewell302');
ok('E enc79PaperWhisper（未知 id）→ no-op，唔開風聲', whisperCalls.length===0);
enc79PaperWhisper('side_lu_concert');
enc79PaperWhisper('side_liao_newfilm');
enc79PaperWhisper('side_mak_wrap');
ok('E 對照組三個已知 id 照開風聲', whisperCalls.length===3 &&
  whisperCalls.indexOf('luk_baakyin|paper')>=0 && whisperCalls.indexOf('liu_bingxing|paper')>=0 && whisperCalls.indexOf('mak_zhendong|paper')>=0);
S = freshS(); S.stars.chung_choning = { fav: 60, beatsDone: { chung_farewell: 690 } }; clippings = []; whisperCalls = [];
let edW = buildNewspaperEdition(wrapBatch(1, 39), 39);
ok('E 含 lu＋liao＋farewell 嗰期有三則 side 短訊', edW.shorts.filter(s=>s && s.source==='side').length===3);
commitMorningPaper(edW, { persist:false });
ok('E commit 嗰期只開兩個風聲（lu／liao），告別花邊唔開', whisperCalls.length===2, JSON.stringify(whisperCalls));

/* ---------- F：忠告機制照舊 ---------- */
S = freshS(); S.flags.chungAdviceHeld229 = 1;
ok('F 忠告持有 → chungAdviceCardHeld229 true', chungAdviceCardHeld229()===true);
S.flags.chungAdviceSpent229 = 1;
ok('F 忠告用過 → chungAdviceCardHeld229 false', chungAdviceCardHeld229()===false);
S = freshS();
ok('F 無忠告旗 → chungAdviceCardHeld229 false', chungAdviceCardHeld229()===false);
ok('F 忠告原文在位', typeof CHUNG_ADVICE_TEXT229==='string' && CHUNG_ADVICE_TEXT229.indexOf('唔好學人哋點演')===0);
ok('F 忠告用一次即清邏輯在位', html.indexOf('S.flags.chungAdviceSpent229 = 1')>=0);

/* ---------- S：靜態——唔郁清單 ---------- */
ok('S1 PAPER_SIDE_ITEMS 仍係 39 則', Array.isArray(PAPER_SIDE_ITEMS) && PAPER_SIDE_ITEMS.length===39, 'count='+(PAPER_SIDE_ITEMS && PAPER_SIDE_ITEMS.length));
ok('S1 輪替池照輪（day 0 vs day 1 標題唔同）', paperSideItemForDay(0).headline!==paperSideItemForDay(1).headline);
ok('S1 告別 beat 對白唔郁', html.indexOf('我走，唔想大鑼大鼓。你都唔好同人講，當我去咗一個長啲嘅外景就得喇。')>=0);
ok('S1 結局回望讀 beatsDone 唔郁', html.indexOf('bdC100.chung_farewell')>=0 && html.indexOf('鍾楚凝那班機')>=0);
ok('S1 出沒盤停出讀 beatsDone 唔郁', html.indexOf('cs100.beatsDone.chung_farewell')>=0);
ok('S1 grants() 授 advice 旗唔郁', html.indexOf('S.flags.chungAdviceHeld229 = 1')>=0);
const gigsLib = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'content', 'gigs_new.json'), 'utf8')).gigs;
ok('S1 gigs_new.json 仍係 322 張', gigsLib.length===322, 'count='+gigsLib.length);

if(fails.length){ console.log('FAILURES: '+fails.join(', ')); process.exit(1); }
console.log('ALL PASS');
