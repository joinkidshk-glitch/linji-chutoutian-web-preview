// Weave Phase 3-1 邏輯測試：報紙連載口吻＋點名門檻
// 用法：node tests/test_weave31_logic.js [path-to-index.html]
const fs = require('fs');
const path = process.argv[2] || require('path').join(__dirname, '..', 'index.html');
const html = fs.readFileSync(path, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) throw new Error('fn not found: '+name);
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){
    if(html[j]==='{') depth++;
    else if(html[j]==='}'){ depth--; if(depth===0) break; }
  }
  return html.slice(i, j+1);
}
function extractConst(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) throw new Error('const not found: '+name);
  let depth=0, j=html.indexOf('[', i), started=false;
  for(; j<html.length; j++){
    if(html[j]==='['){ depth++; started=true; }
    else if(html[j]===']'){ depth--; if(started && depth===0) break; }
  }
  return html.slice(i, j+1)+';';
}
function extractConstLine(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) throw new Error('const not found: '+name);
  return html.slice(i, html.indexOf('\n', i))+';';
}

// stubs
var S = { fame: 5, dayIndex: 40, newspaperClippings: [] };
var displayDateObj = ()=> new Date(1988, 5, 15);
var fmtDateShort = ()=> '1988/6/15';
var ensureNewspaperClippings = ()=> S.newspaperClippings;
var FAKE_GIGS = {
  gig_lu: { starHint: { name: '陸柏言', adjacency: 'rumor' } },
  gig_mai: { starHint: { name: '麥震東', adjacency: 'rumor' } }
};
var newspaperLookupGig = (id)=> FAKE_GIGS[id] || null;

eval(extractConstLine('PAPER_NAME_TIER_NAMED').replace('const PAPER_NAME_TIER_NAMED', 'globalThis.PAPER_NAME_TIER_NAMED'));
eval(extractConstLine('PAPER_NAME_TIER_TITLED').replace('const PAPER_NAME_TIER_TITLED', 'globalThis.PAPER_NAME_TIER_TITLED'));
eval(extractFn('newspaperNameTier'));
eval(extractFn('newspaperPlayerRef'));
eval(extractFn('newspaperMediumFromGigType'));
eval(extractFn('newspaperWrapFaceLines'));
eval(extractConst('PAPER_TOPIC_STARS').replace('const PAPER_TOPIC_STARS', 'globalThis.PAPER_TOPIC_STARS'));
eval(extractFn('newspaperTopicKey'));
eval(extractFn('newspaperPrevTopicKey'));
eval(extractFn('newspaperSerialLine'));
eval(extractConst('PAPER_SIDE_ITEMS').replace('const PAPER_SIDE_ITEMS', 'globalThis.PAPER_SIDE_ITEMS'));
eval(extractFn('paperSideItemForDay'));
eval(extractFn('buildNewspaperEdition'));

// ---- 點名門檻分級 ----
ok('tier fame 0 -> anon', newspaperNameTier(0)==='anon');
ok('tier fame 14 -> anon', newspaperNameTier(14)==='anon');
ok('tier fame 15 -> named', newspaperNameTier(15)==='named');
ok('tier fame 39 -> named', newspaperNameTier(39)==='named');
ok('tier fame 40 -> titled', newspaperNameTier(40)==='titled');
ok('tier fame 80 -> titled', newspaperNameTier(80)==='titled');
ok('ref anon', newspaperPlayerRef('anon')==='一名臨記');
ok('ref named', newspaperPlayerRef('named')==='阿偉');
ok('ref titled', newspaperPlayerRef('titled')==='人氣新人阿偉');

// ---- FaceLines 稱呼層 ----
const subj = { gigId:'g1', work:'街景臨記', role:'路人', type:'電影' };
S.fame = 5;
const anon = newspaperWrapFaceLines(subj);
/* v20a37：頭條改行變體池（6 款，作品+角色 hash 定版）——斷言改守稱呼層不變量（邊個 tier 用邊個稱呼＋角色在場），唔再釘死單一句式 */
ok('anon headline uses 臨記 not name', anon.headline.includes('臨記') && anon.headline.includes('路人') && !anon.headline.includes('阿偉'));
ok('anon dek uses 一名臨記', anon.dek.includes('一名臨記') && !anon.dek.includes('阿偉'));
ok('anon rumor uses 有個臨記', anon.rumor.includes('有個臨記') && !anon.rumor.includes('阿偉'));
ok('anon tier field', anon.nameTier==='anon');
S.fame = 20;
const named = newspaperWrapFaceLines(subj);
ok('named headline names 阿偉', named.headline.includes('阿偉') && named.headline.includes('路人'));
ok('named dek names 阿偉', named.dek.includes('阿偉於'));
ok('named tier field', named.nameTier==='named');
S.fame = 45;
const titled = newspaperWrapFaceLines(subj);
ok('titled headline has title ref', titled.headline.includes('人氣新人阿偉') && titled.headline.includes('路人'));
ok('titled dek has title ref', titled.dek.includes('人氣新人阿偉於'));
// anon 電視無角色：唔寫「名字見諸內頁」
S.fame = 5;
const anonTv = newspaperWrapFaceLines({ gigId:'g2', work:'師奶劇場', role:'', type:'電視劇' });
ok('anon tv no-role dek has no 名字見諸內頁', !anonTv.dek.includes('名字見諸內頁') && anonTv.dek.includes('一名臨記'));
// 角度行為不變（跨 tier）
S.fame = 45;
const titledSpot = newspaperWrapFaceLines(subj, 'spotlight');
ok('titled spotlight dek keeps 搶眼', titledSpot.dek.includes('搶眼'));
S.fame = 5;
const anonSteady = newspaperWrapFaceLines(subj, 'steady');
ok('anon steady dek keeps 不搶戲', anonSteady.dek.includes('不搶戲'));

// ---- 關聯鍵 ----
ok('topic C3 -> rival:gao', newspaperTopicKey({ eventKey:'story:C3:hard' })==='rival:gao');
ok('topic wrap starHint via gigId', newspaperTopicKey({ eventKey:'wrap:gig_lu:12' })==='star:陸柏言');
ok('topic wrap starHint mai', newspaperTopicKey({ eventKey:'wrap:gig_mai:3', headline:'', dek:'', workTitle:'' })==='star:麥震東');
ok('topic text scan star', newspaperTopicKey({ headline:'麥震東新片開鏡', dek:'', workTitle:'' })==='star:麥震東');
ok('topic work fallback', newspaperTopicKey({ eventKey:'wrap:unknown:1', headline:'《試片》殺青', dek:'', workTitle:'試片' })==='work:試片');
ok('topic empty item', newspaperTopicKey({})==='');
ok('topic empty-ish item', newspaperTopicKey({ headline:'通告見報', dek:'一行' })==='');

// ---- 連載句 ----
ok('serial star line', newspaperSerialLine('star:陸柏言').includes('本報早前曾報道陸柏言'));
ok('serial rival line', newspaperSerialLine('rival:gao').includes('新人爭位'));
ok('serial work line', newspaperSerialLine('work:試片').includes('《試片》'));
ok('serial empty key', newspaperSerialLine('')==='');

// ---- 上一份話題鍵（新欄＋舊檔推斷） ----
S.newspaperClippings = [{ topicKey:'star:陸柏言' }];
ok('prev from stored topicKey', newspaperPrevTopicKey()==='star:陸柏言');
S.newspaperClippings = [{ headline:'陸柏言紅磡開唱', dek:'', eventKeys:['wrap:gig_lu:3'] }];
ok('prev legacy clipping via eventKeys', newspaperPrevTopicKey()==='star:陸柏言');
S.newspaperClippings = [{ headline:'某劇殺青', dek:'麥震東現身片場', eventKeys:[] }];
ok('prev legacy clipping via text scan', newspaperPrevTopicKey()==='star:麥震東');
S.newspaperClippings = [];
ok('prev none', newspaperPrevTopicKey()==='');

// ---- Edition 整合：同鍵先加跟進句 ----
const headItem = { eventKey:'wrap:gig_lu:40', source:'wrap', enqueuedDay:39, publishDay:40, fameDelta:2, paperName:'娛樂版', headline:'《星夜迷離》殺青', dek:'電視劇組殺青，一名臨記完成《星夜迷離》。', clipLabel:'', rumorEcho:'', workTitle:'星夜迷離' };
S.newspaperClippings = [{ topicKey:'star:陸柏言' }];
const edLink = buildNewspaperEdition([Object.assign({}, headItem)], 40);
ok('edition topicKey recorded', edLink.topicKey==='star:陸柏言');
ok('edition dek gains serial line on same topic', edLink.dek.includes('本報早前曾報道陸柏言'));
S.newspaperClippings = [{ topicKey:'work:另一套戲' }];
const edNoLink = buildNewspaperEdition([Object.assign({}, headItem)], 40);
ok('edition no serial when topic differs', !edNoLink.dek.includes('本報早前'));
S.newspaperClippings = [];
const edFirst = buildNewspaperEdition([Object.assign({}, headItem)], 40);
ok('edition no serial on first paper', !edFirst.dek.includes('本報早前') && edFirst.topicKey==='star:陸柏言');
// 已有跟進句唔好疊加
S.newspaperClippings = [{ topicKey:'star:陸柏言' }];
const dupItem = Object.assign({}, headItem, { dek:'電視劇組殺青。本報早前曾報道陸柏言的消息，今期再有跟進，讀者可對照前文。' });
const edDup = buildNewspaperEdition([dupItem], 40);
ok('edition serial not duplicated', (edDup.dek.match(/本報早前/g)||[]).length===1);

console.log(fails.length ? ('\nFAILED: '+fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length?1:0);
