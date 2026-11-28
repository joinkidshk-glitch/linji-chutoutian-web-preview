// LADDER95 邏輯測試（v20a95）：結局梯擴充。
// - 三條校準弧（正常強弧→SS、近乎完美弧→E1、電影專長弧→FK）＋專長分科弧（TK/SK/GH/CK/AK）
//   ＋ID/CR 帶位弧＋E3 三變體＋E1 邊界（349/350）與質性閘逐項拆解；
// - 累計計數器：careerStats95Of 存檔路徑／wrapHistory 衍生路徑／end95AddWrap 種子唔雙計；
// - 質性件單元：end95Awards（win vs 提名）、end95ChainsDone 六鏈標記、end95PangProgress 三路；
// v20a101 QA101 改版註記：彭少祺星 id 正名——巧遇系統真 id 係 pang_siuki，本檔舊 fixture
//   誤用 pang_siu_kei（同 end95PangProgress 舊 bug 同源、互相掩護）；本版 fixture 改用真 id，
//   end95PangProgress 亦已修返讀 pang_siuki。專門守門見 tests/test_qa101_logic.js。
// - 差邊瓣：end95BuildGaps 經 resolve 輸出（獎／擔正／鏈／雙軌差額）；純函數不變性；舊檔唔 crash。
// 用法：node tests/test_ladder95_logic.js
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');

let pass = 0, fail = 0;
function ok(name, cond){
  if(cond){ pass++; console.log('  ok - ' + name); }
  else { fail++; console.log('  FAIL - ' + name); }
}
function extractFn(decl){
  const i = html.indexOf(decl);
  if(i<0) throw new Error('fn not found: '+decl);
  let j = html.indexOf('{', i), depth = 0, k = j;
  for(; k<html.length; k++){
    if(html[k]==='{') depth++;
    else if(html[k]==='}'){ depth--; if(depth===0){ k++; break; } }
  }
  return html.slice(i, k);
}
function extractConst(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) throw new Error('const not found: '+name);
  let depth = 0, started = false;
  for(let k=i; k<html.length; k++){
    const ch = html[k];
    if(ch==='{'||ch==='['){ depth++; started = true; }
    else if(ch==='}'||ch===']'){ depth--; if(started && depth===0) return html.slice(i, k+1)+';'; }
    else if(ch===';' && !started) return html.slice(i, k+1);
  }
  throw new Error('const end not found: '+name);
}

var window = {};
var location = { search: "" };
var localStorage = { getItem: ()=>null, setItem: ()=>{}, removeItem: ()=>{} };
var S = null;
var saveQ = function(){};
var toast = function(){};
var modal = function(){};
/* 衍生路徑用嘅假通告庫（分類器只需要 type/title/roleLabel/roleScale/genreLabel） */
var GIGS = [
  { id:'g_film_lead', type:'電影', title:'《龍虎風雲》男主角', workTitle:'龍虎風雲', roleLabel:'男主角', roleScale:'film_lead_big', genreLabel:'警匪片' },
  { id:'g_film_com', type:'電影', title:'《笑匠當家》諧星', workTitle:'笑匠當家', roleLabel:'諧星', roleScale:'film_support_main', genreLabel:'喜劇片' },
  { id:'g_tv_long', type:'電視劇', title:'《大時代》男主角', workTitle:'大時代', roleLabel:'男主角', roleScale:'tv_lead_long', genreLabel:'時裝劇' },
  { id:'g_rec_helper', type:'唱片通告', title:'《和音》唱片幫工', workTitle:'和音', roleLabel:'唱片幫工', roleScale:'rec_album', genreLabel:'粵語流行' },
  { id:'g_ad_extra', type:'廣告', title:'《汽水》路人', workTitle:'汽水', roleLabel:'路人', roleScale:'ad_extra_day', genreLabel:'' },
  { id:'g_stunt', type:'電影', title:'《武打戲》替身', workTitle:'武打戲', roleLabel:'男主角替身', roleScale:'film_stunt', genreLabel:'江湖動作片' },
  { id:'g_tv_crew', type:'電視劇', title:'《廠景日常》場記', workTitle:'廠景日常', roleLabel:'場記', roleScale:'tv_cameo_short', genreLabel:'幕後' },
];

const FN_LIST = ['function dateObj','function calendarSeason','function dualTrackNumbers','function readDualTracks','function syncDualTracks',
  'function endingFlag410','function endingDual410','function endingNegTagCount410','function endingBackstageTagCount410','function favorCreditCountsAsHeld','function endingFavor410', // v259 R1＋R2
  'function endingRomance410','function endingE2Eligible410','function endingE3Eligible410','function endingBackstageClose410',
  'function end95GenreOf','function end95IsLead','function end95ClassifyWrap','function end95EmptyStats','function end95StatsAddOne',
  'function end95DeriveStats','function careerStats95Of','function end95AddWrap','function end95Awards','function end95EverHeldCredit',
  'function end95StoryDone','function end95ChainsDone','function end95SpineDone','function end95PangProgress','function end95E3Variant','function end95BuildGaps',
  'function end229IsLead','function end229ClassifyLead','function end229EmptyLeadStats',
  'function end229DeriveLeadStats','function leadStats229Of','function end229AddWrap',
  'function isForcedGig392','function day392YearMonth','function end392SelDeriveStats','function careerStats392SelOf', // v20a393 自選履歷
  'function exposure392Of','function activity392Of','function isLowActivity392', // v20a393 曝光／活動量
  'function duty392GigById','function backstageDuties392Of', // v20a393 幕後職務
  'function forcedCredit392ReplayWraps','function forcedCredit392Of','function forcedCredit392CounterCredit', // v20a393 對照信用
  'function endingAward392TvSupport','function endingAward392WonLabel', // v20a393 獎項句憑據
  'function resolveEnding410','function endingEveOptions410','function endingEsc410','function endingCareerScene410','function endingSummaryHtml410'];
const CONST_LIST = ['ENDING410_CAREER_NAMES','ENDING410_T','ENDING_NEG_TAGS410','ENDING410_BACKSTAGE_KEYS','ENDING410_EXODUS_NAME_FALLBACK',
  'ENDING410_NPC_NAMES','ENDING95_T','END95_TYPE_MEDIUM','END95_LEAD_SCALES','END95_STRONG_LEAD','END95_GENRE_TYPE_NAMES',
  'END95_COMEDY_G','END95_ACTION_G','END95_COMEDY_KW','END95_ACTION_KW','ENDING410_ADJ_RUMOR','END229_LEAD_MEDIUM','SPINE95_REQUIRED',
  'DUTY392_KIND_BY_ID','DUTY392_GIGS']; // v20a393 職務表
let SRC = "var START = { y:1990, m:1, d:1 };\n" + FN_LIST.map(extractFn).join('\n') + '\n' + CONST_LIST.map(extractConst).join('\n');
CONST_LIST.forEach(n => { SRC = SRC.split('const '+n+' =').join('var '+n+' ='); });
eval(SRC);

ok('harness: LADDER95 函數載入', typeof resolveEnding410 === 'function' && typeof careerStats95Of === 'function' && typeof end95AddWrap === 'function');

/* 狀態工廠：credit = round(fame*0.5) + delta（stage/acting/stress 全 0） */
function baseSave(over){
  return Object.assign({
    dayIndex: 1060, money: 9000, fame: 20, stage: 0, acting: 0, popularity: 30, stress: 0,
    industryCredit: 0, industryCreditDelta: 0,
    flags: {}, routes: {}, mockCredits: [], mockDebts: [], mockRumors: [], inventory: {},
    castingTags: [], npcs: { agent: 0, director: 0, colleague: 0, reporter: 0, stylist: 0, rival: 0 },
    favorLedger: { settled: 0, credits: 0, exodus: [], counted: {} },
    story: { flags: {}, rel: {}, done: {}, choices: {} },
    awardsLog: [], wrapHistory: [], trainCount: {}, stars: {}, intelFlags: {}, wf3: {},
  }, over || {});
}
function stats95(o){
  const base = { total: 0, byMedium: { film:0, tv:0, music:0, variety:0, ad:0 },
    leadByMedium: { film:0, tv:0, music:0, variety:0, ad:0 },
    tvLongLeads: 0, genreIdentified: 0, genreComedy: 0, genreAction: 0, backstageWorks: 0 };
  if(o){
    Object.keys(o).forEach(k => {
      if(k === 'byMedium' || k === 'leadByMedium') Object.assign(base[k], o[k]);
      else base[k] = o[k];
    });
  }
  return base;
}
/* fame/credit 精確構造：delta = credit - round(fame/2) */
function arc(fame, credit, over){
  const delta = credit - Math.round(fame * 0.5);
  const o = Object.assign({ fame: fame, industryCreditDelta: delta }, over || {});
  /* v20a229 B4：合成存檔只帶舊計數器 careerStats95——新計數器 leadStats229
     由佢嘅 leadByMedium 鏡像補齊（等同舊檔回填；新計數器本身嘅寫入／衍生路徑
     由 test_gig229_counts.js 另行驗，呢度唔靠舊計數器做判定）。 */
  if(o.careerStats95 && o.careerStats95.leadByMedium && !o.leadStats229){
    o.leadStats229 = { byMedium: Object.assign({ film: 0, tv: 0, music: 0, variety: 0, ad: 0 }, o.careerStats95.leadByMedium) };
  }
  return baseSave(o);
}
function R(save){ S = save; return resolveEnding410(S); }
function canon(o){
  if(Array.isArray(o)) return '[' + o.map(canon).join(',') + ']';
  if(o && typeof o === 'object') return '{' + Object.keys(o).sort().map(k => JSON.stringify(k) + ':' + canon(o[k])).join(',') + '}';
  return JSON.stringify(o);
}


/* v422 負標籤邊界：自然 profile、負標籤 0，E3/E5/ID/CR/E2 不被 SS 截走 */
function neg0(r){ return r.snapshot.negTags===0; }
/* E3：信用主導＋幕後職務 2 種 2 製作，雙軌高到本可入 SS 帶 */
{
  const st=arc(160,170,{ careerStats95: stats95({total:40, byMedium:{film:20,tv:20}}),
    backstageDuties392:[{kind:"場記",production:"甲",gigId:"duty392_clapper_a",day:1},{kind:"剪接助理",production:"乙",gigId:"duty392_editor_a",day:2}] });
  const r=R(st);
  ok('v422 E3 零負標籤命中（不被 SS 截走）', r.career==='E3' && neg0(r));
}
/* E5：信用主導＋人情總量>=6＋何生 rel>=60 */
{
  const credits=[1,2,3,4,5,6].map(i=>({id:"credit_x"+i, debtor:"某人", status:"未收"}));
  const st=arc(160,170,{ careerStats95: stats95({total:40, byMedium:{film:20,tv:20}}),
    mockCredits:credits, npcs:{agent:80,director:0,colleague:0,reporter:0,stylist:0,rival:0} });
  const r=R(st);
  ok('v422 E5 零負標籤命中（不被 SS 截走）', r.career==='E5' && neg0(r));
}
/* ID：聲望主導帶（fame>=60、對照信用在窗內），雙軌未到 SS */
{
  const st=arc(100,80,{ careerStats95: stats95({total:30, byMedium:{ad:20,variety:10}}) });
  const r=R(st);
  ok('v422 ID 零負標籤命中', r.career==='ID' && neg0(r));
}
/* CR：信用>=55、聲望 35-110、非低活動，雙軌未到 SS */
{
  const st=arc(50,80,{ careerStats95: stats95({total:30, byMedium:{film:15,tv:15}}),
    wrapHistory:[{gigId:"g_film_com", wrappedDay:100},{gigId:"g_tv_long", wrappedDay:200},{gigId:"g_film_lead", wrappedDay:300}] });
  const r=R(st);
  ok('v422 CR 零負標籤命中', r.career==='CR' && neg0(r));
}
/* E2：信用>=42、聲望>=35、未入 CR 窗（聲望>110 且信用<聲望-10 避開 E3/E5 帶、雙軌<300 避 SS） */
{
  const st=arc(130,125,{ careerStats95: stats95({total:30, byMedium:{film:15,tv:15}}),
    wrapHistory:[{gigId:"g_film_com", wrappedDay:100},{gigId:"g_tv_long", wrappedDay:200},{gigId:"g_film_lead", wrappedDay:300}] });
  const r=R(st);
  ok('v422 E2 零負標籤命中', r.career==='E2' && neg0(r));
}
/* 對照：加兩個負標籤只關 E1/SS，不改變上述具體格（E3 照中） */
{
  const st=arc(160,170,{ careerStats95: stats95({total:40, byMedium:{film:20,tv:20}}),
    castingTags:[{id:"tag_x",label:"八卦"},{id:"tag_y",label:"高冷"}],
    backstageDuties392:[{kind:"場記",production:"甲",gigId:"duty392_clapper_a",day:1},{kind:"剪接助理",production:"乙",gigId:"duty392_editor_a",day:2}] });
  const r=R(st);
  ok('v422 負標籤 2 個不令 E3 需要靠它避格（照中 E3）', r.career==='E3' && r.snapshot.negTags===2);
}
console.log(fail===0 ? 'ALL PASS ('+pass+')' : 'FAILURES '+fail+'/'+(pass+fail));
process.exit(fail===0?0:1);
