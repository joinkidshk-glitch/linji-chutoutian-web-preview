// Weave Phase 3-2 邏輯測試（v20a267 重寫）：報紙花邊唔再入傳聞池——
//   傳聞拼合系統已刪（SIDE_PAPER_FRAGS／pushNewspaperRumor／MERGE_PAIRS／
//   findMergePair／mergePickedRumors／hasIntelFlag／displayRumor 全部消失）。
//   保留：PAPER_SIDE_ITEMS 花邊池（39 則）＋paperSideItemForDay＋buildNewspaperEdition；
//   新歸宿：有風聲映射嗰 3 張花邊（side_lu_concert／side_liao_newfilm／side_mak_wrap）
//   經 commitMorningPaper → enc79PaperWhisper 直接開風聲窗，唔寫卡。
// 用法：node tests/test_weave32_logic.js [path-to-index.html]
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
  let j = i;
  while(j<html.length && html[j]!=='{' && html[j]!=='[') j++;
  const openCh = html[j], closeCh = openCh==='{' ? '}' : ']';
  let depth=0, started=false;
  for(; j<html.length; j++){
    if(html[j]===openCh){ depth++; started=true; }
    else if(html[j]===closeCh){ depth--; if(started && depth===0) break; }
  }
  return html.slice(i, j+1)+';';
}

// stubs
var _year = 1988;
var displayDateObj = ()=> new Date(_year, 0, 15);
var fmtDateShort = ()=> '1988/1/15';
var ensureMockJournal = ()=>{};
var syncNotebookMirror = ()=>{};
var saveQ = ()=>{};
var toast = ()=>{};
var modal = ()=>{};
var contentFilterOn = ()=>true;
var S = { dayIndex: 0, fame: 0, mockRumors: [] };

eval(extractConst('PAPER_SIDE_ITEMS').replace('const PAPER_SIDE_ITEMS', 'globalThis.PAPER_SIDE_ITEMS'));
eval(extractFn('paperSideItemForDay'));
eval(extractFn('buildNewspaperEdition'));

const SIDE = globalThis.PAPER_SIDE_ITEMS;

// 1. 傳聞系統已刪：全部識別碼零殘留
ok('deleted: SIDE_PAPER_FRAGS／pushNewspaperRumor／paperSideFragmentFor 消失',
  ['SIDE_PAPER_FRAGS','pushNewspaperRumor','paperSideFragmentFor'].every(n=>html.indexOf(n)<0));
ok('deleted: MERGE_PAIRS／MERGE_FLOW／MERGE_FRAGS／INTEL_FLAGS 消失',
  ['MERGE_PAIRS','MERGE_FLOW','MERGE_FRAGS','INTEL_FLAGS'].every(n=>html.indexOf(n)<0));
ok('deleted: findMergePair／mergePickedRumors／heardPickIds／mockMergePick 消失',
  ['findMergePair','mergePickedRumors','heardPickIds','mockMergePick'].every(n=>html.indexOf(n)<0));
ok('deleted: ensureIntelFlags／setIntelFlag／hasIntelFlag／hasMergedIntel 消失',
  ['ensureIntelFlags','setIntelFlag','hasIntelFlag','hasMergedIntel'].every(n=>html.indexOf(n)<0));
ok('deleted: rumorStateLabel／RUMOR_STATE_ZH／displayRumor／familySafeRumorText 消失',
  ['rumorStateLabel','RUMOR_STATE_ZH','displayRumor','familySafeRumorText'].every(n=>html.indexOf(n)<0));
ok('deleted: mockRumors 零殘留', html.indexOf('mockRumors')<0);

// 2. 花邊池保留：39 則；三條風聲映射 sideId 仍在池
ok('pool still 39', SIDE.length===39);
ok('whisper-mapped sides still in pool', ['side_lu_concert','side_liao_newfilm','side_mak_wrap'].every(id=>SIDE.some(it=>it.id===id)));
ok('mak side item mentions 麥震東 without banned words', (()=>{ const m = SIDE.find(it=>it.id==='side_mak_wrap'); return !!m && m.h.indexOf('麥震東')>=0 && !/買醉|爛醉|食煙|抽煙/.test(m.h+m.d); })());
ok('linked side items carry no filter-sensitive words', SIDE.filter(it=>it.id).every(it=>!/買醉|爛醉|食煙|抽煙/.test(it.h+it.d)));

// 3. paperSideItemForDay 帶 sideId（1988 池：day0=陸、day1=廖、day11=麥、day2=魏無關聯）
ok('day0 side is lu concert with sideId', (()=>{ const s = paperSideItemForDay(0); return s && s.sideId==='side_lu_concert'; })());
ok('day1 side is liao with sideId', (()=>{ const s = paperSideItemForDay(1); return s && s.sideId==='side_liao_newfilm'; })());
ok('day11 side is mak wrap with sideId', (()=>{ const s = paperSideItemForDay(11); return s && s.sideId==='side_mak_wrap'; })());
ok('day2 side unlinked (empty sideId)', (()=>{ const s = paperSideItemForDay(2); return s && s.sideId===''; })());
ok('side item still fameDelta 0', paperSideItemForDay(0).fameDelta===0);

// 4. 新歸宿：edition 帶 side 短訊（source "side"），commitMorningPaper 經 enc79PaperWhisper 開風聲
const batch = [{ eventKey:'wrap:g1:0', source:'wrap', enqueuedDay:0, publishDay:0, fameDelta:2, paperName:'娛樂版', headline:'阿偉新片殺青', dek:'', clipLabel:'', rumorEcho:'' }];
const ed0 = buildNewspaperEdition(batch, 0);
ok('edition carries side short with sideId', Array.isArray(ed0.shorts) && ed0.shorts.some(s=>s.source==='side' && s.sideId==='side_lu_concert'));
{
  const iC = html.indexOf('function commitMorningPaper(');
  const segC = html.slice(iC, iC + 4000);
  ok('commitMorningPaper routes side shorts to enc79PaperWhisper', segC.indexOf('enc79PaperWhisper(sh.sideId)')>=0);
  ok('enc79PaperWhisper maps 3 sides to stars', html.indexOf('side_lu_concert')>=0 && html.indexOf('side_liao_newfilm')>=0 && html.indexOf('side_mak_wrap')>=0 && html.indexOf('enc79PaperWhisper')>=0);
}

console.log(fails.length ? ('\nFAILED: '+fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length?1:0);
