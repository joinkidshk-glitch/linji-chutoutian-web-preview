// Weave Phase 3-2 邏輯測試：報紙花邊入傳聞池（鏈 D 跨系統拼合）
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
var renderRumorPane = ()=>{};
var playTutorialPhase2MergeFx = ()=>{};
var phase2Steps56Line = (s,k,fb)=>fb;
var phase2Steps56Copy = ()=>false;
var contentFilterOn = ()=>true;
var mockMergePick = [];
var S = { dayIndex: 0, fame: 0, mockRumors: [] };

eval(extractConst('PAPER_SIDE_ITEMS').replace('const PAPER_SIDE_ITEMS', 'globalThis.PAPER_SIDE_ITEMS'));
eval(extractConst('SIDE_PAPER_FRAGS').replace('const SIDE_PAPER_FRAGS', 'globalThis.SIDE_PAPER_FRAGS'));
eval(extractConst('MERGE_PAIRS').replace('const MERGE_PAIRS', 'globalThis.MERGE_PAIRS'));
eval(extractConst('MERGE_FLOW').replace('const MERGE_FLOW', 'globalThis.MERGE_FLOW'));
eval(extractConst('RUMOR_STATE_ZH').replace('const RUMOR_STATE_ZH', 'globalThis.RUMOR_STATE_ZH'));
eval(extractConst('INTEL_FLAGS').replace('const INTEL_FLAGS', 'globalThis.INTEL_FLAGS'));
eval(extractFn('paperSideItemForDay'));
eval(extractFn('paperSideFragmentFor'));
eval(extractFn('buildNewspaperEdition'));
eval(extractFn('pushNewspaperRumor'));
eval(extractFn('rumorStateLabel'));
eval(extractFn('findMergePair'));
eval(extractFn('heardPickIds'));
eval(extractFn('ensureIntelFlags'));
eval(extractFn('setIntelFlag'));
eval(extractFn('hasIntelFlag'));
eval(extractFn('mergePickedRumors'));
eval(extractFn('familySafeRumorText'));
eval(extractFn('displayRumor'));

const SIDE = globalThis.PAPER_SIDE_ITEMS;
const FRAGS = globalThis.SIDE_PAPER_FRAGS;

// 1. 登記表：三條情報線各一塊報紙碎片，其餘花邊唔登記
// v20a82 WF3 有意變更：鏈 D 擴充——登記表 3→12 條（加葉敏芝／顧明輝新情報線＋7 條時代花邊碎片），原位改版
ok('frag map has exactly 12 entries (v82 WF3 鏈 D 擴充)', Object.keys(FRAGS).length===12);
ok('frag map yip (v82)', FRAGS['side_yip_swimsuit']==='paperfrag_yip_swimsuit');
ok('frag map ku (v82)', FRAGS['side_ku_wrap']==='paperfrag_ku_wrap');
ok('frag map lu', FRAGS['side_lu_concert']==='paperfrag_lu_concert');
ok('frag map liao', FRAGS['side_liao_newfilm']==='paperfrag_liao_newfilm');
ok('frag map mak', FRAGS['side_mak_wrap']==='paperfrag_mak_wrap');
ok('every mapped sideId exists in pool', Object.keys(FRAGS).every(id=>SIDE.some(it=>it.id===id)));
ok('pool grew to 39 (v86 WF4 花邊補完 +10；v82 WF3 鏈 D 擴充時為 29)', SIDE.length===39);
ok('mak side item mentions 麥震東 without banned words', (()=>{ const m = SIDE.find(it=>it.id==='side_mak_wrap'); return !!m && m.h.indexOf('麥震東')>=0 && !/買醉|爛醉|食煙|抽煙/.test(m.h+m.d); })());

// 2. paperSideItemForDay 帶 sideId（1988 池 12 則：day0=陸、day1=廖、day11=麥、day2=魏無關聯）
ok('day0 side is lu concert with sideId', (()=>{ const s = paperSideItemForDay(0); return s && s.sideId==='side_lu_concert'; })());
ok('day1 side is liao with sideId', (()=>{ const s = paperSideItemForDay(1); return s && s.sideId==='side_liao_newfilm'; })());
ok('day11 side is mak wrap with sideId', (()=>{ const s = paperSideItemForDay(11); return s && s.sideId==='side_mak_wrap'; })());
ok('day2 side unlinked (empty sideId)', (()=>{ const s = paperSideItemForDay(2); return s && s.sideId===''; })());
ok('side item still fameDelta 0', paperSideItemForDay(0).fameDelta===0);

// 3. paperSideFragmentFor：有關聯先生成，無關聯／非 side 一律 null
ok('frag descriptor for lu', (()=>{ const f = paperSideFragmentFor(paperSideItemForDay(0)); return f && f.id==='paperfrag_lu_concert' && f.paperFrag===true && f.headline.indexOf('陸柏言')>=0; })());
ok('frag null for unlinked side', paperSideFragmentFor(paperSideItemForDay(2))===null);
ok('frag null for non-side', paperSideFragmentFor({ source:'wrap', sideId:'side_lu_concert', headline:'x' })===null);
ok('frag null for missing sideId', paperSideFragmentFor({ source:'side', headline:'x', dek:'y' })===null);

// 4. 見報入池：edition(day0) → pushNewspaperRumor → 碎片入 mockRumors
function classicFrags(){
  return [
    { id:'rumor_lu_baiyan_angry', source:'場務八卦', title:'陸柏言片場發脾氣', text:'陸柏言喺片場無端端發火，鬧到成個場靜晒。', state:'normal', season:'' },
    { id:'rumor_lu_baiyan_drunk', source:'酒保閒聊', title:'陸柏言深夜買醉', text:'有人見到陸柏言半夜喺蘭桂坊飲到爛醉。', state:'normal', season:'' },
    { id:'rumor_mai_zhendong_hurt', source:'武師目擊', title:'麥震東片場整親', text:'麥震東拍動作戲跌親，行路一拐一拐。', state:'normal', season:'' },
  ];
}
const batch = [{ eventKey:'wrap:g1:0', source:'wrap', enqueuedDay:0, publishDay:0, fameDelta:2, paperName:'娛樂版', headline:'阿偉新片殺青', dek:'', clipLabel:'', rumorEcho:'' }];
S = { dayIndex: 0, fame: 0, mockRumors: classicFrags() };
const ed0 = buildNewspaperEdition(batch, 0);
pushNewspaperRumor(ed0);
const fragRow = S.mockRumors.find(r=>r.id==='paperfrag_lu_concert');
ok('paper fragment entered pool', !!fragRow);
ok('fragment source marks newspaper', !!fragRow && fragRow.source==='報紙花邊' && fragRow.fromPaper===true && fragRow.paperFrag===true);
ok('fragment state is heard (pickable)', !!fragRow && rumorStateLabel(fragRow.state)==='剛聽聞');
ok('fragment title is paper headline verbatim', !!fragRow && fragRow.title===paperSideItemForDay(0).headline);
ok('fragment text is paper dek verbatim', !!fragRow && fragRow.text===paperSideItemForDay(0).dek);

// 5. 去重：同一 edition 重推、另一日同一花邊再見報，都唔重複入池
pushNewspaperRumor(ed0);
const ed12 = buildNewspaperEdition(batch, 12);
pushNewspaperRumor(ed12);
ok('fragment not duplicated across editions', S.mockRumors.filter(r=>r.id==='paperfrag_lu_concert').length===1);

// 6. 無關聯花邊唔入池
S = { dayIndex: 2, fame: 0, mockRumors: classicFrags() };
pushNewspaperRumor(buildNewspaperEdition(batch, 2));
ok('unlinked side stays out of pool', !S.mockRumors.some(r=>r.paperFrag));

// 7. 跨系統拼合：報紙碎片 × 聽聞碎片 → 同一 merged 情報＋置旗（陸柏言線）
S = { dayIndex: 3, fame: 0, mockRumors: classicFrags() };
pushNewspaperRumor(buildNewspaperEdition(batch, 0));
mockMergePick = ['paperfrag_lu_concert', 'rumor_lu_baiyan_angry'];
const m1 = mergePickedRumors();
ok('cross merge ok', m1 && m1.ok===true && m1.merged==='rumor_lu_baiyan_breakdown');
ok('merged row created', S.mockRumors.some(r=>r.id==='rumor_lu_baiyan_breakdown' && r.state==='merged'));
ok('both ingredients consumed', ['paperfrag_lu_concert','rumor_lu_baiyan_angry'].every(id=>{ const r = S.mockRumors.find(x=>x.id===id); return r && r.state==='merged'; }));
ok('intel flag set by cross merge', hasIntelFlag('intel_lu_burst')===true);

// 8. 配對鍵：findMergePair 雙向搵到三條跨系統對；經典對不變
ok('pair mak cross (swapped order)', (()=>{ const p = findMergePair('rumor_mai_zhendong_hurt', 'paperfrag_mak_wrap'); return !!p && p.merged==='rumor_mai_zhendong_hide_injury'; })());
ok('pair liao cross', (()=>{ const p = findMergePair('paperfrag_liao_newfilm', 'rumor_liao_bingxing_talk'); return !!p && p.merged==='rumor_liao_bingxing_money'; })());
ok('pair classic lu intact', (()=>{ const p = findMergePair('rumor_lu_baiyan_angry', 'rumor_lu_baiyan_drunk'); return !!p && p.merged==='rumor_lu_baiyan_breakdown'; })());
ok('no bogus cross pair', findMergePair('paperfrag_lu_concert', 'rumor_mai_zhendong_hurt')===null);

// 9. 麥震東線端到端：報紙碎片＋整親碎片 → 隱瞞傷情報旗
S = { dayIndex: 20, fame: 0, mockRumors: classicFrags() };
pushNewspaperRumor(buildNewspaperEdition(batch, 11));
ok('mak fragment entered pool', S.mockRumors.some(r=>r.id==='paperfrag_mak_wrap' && r.state==='normal'));
mockMergePick = ['rumor_mai_zhendong_hurt', 'paperfrag_mak_wrap'];
const m2 = mergePickedRumors();
ok('mak cross merge ok + flag', m2 && m2.ok===true && hasIntelFlag('intel_mak_injury')===true);

// 10. P0-3 守衛：碎片顯示行 displayRumor 唔爆、原文同顯示一致（連結花邊無禁用詞）
ok('linked side items carry no filter-sensitive words', SIDE.filter(it=>FRAGS[it.id]).every(it=>!/買醉|爛醉|食煙|抽煙/.test(it.h+it.d)));
ok('displayRumor passes fragment through', (()=>{ const d = displayRumor({ title:fragRow.title, text:fragRow.text }); return d && d.title===fragRow.title && d.text===fragRow.text; })());

console.log(fails.length ? ('\nFAILED: '+fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length?1:0);
