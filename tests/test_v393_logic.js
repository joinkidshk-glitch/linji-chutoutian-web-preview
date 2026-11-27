// v20a393 十項修復票 — 邏輯測試（抽 index.html 真函數喺沙盒行）。
// 守門：SS 截格新梯（六專長排 SS 之前）／GH 自選佔比＋8 宗下限／CR 窗 35–110／
//   E4 扣除 fame 後信用 <45＋曝光／E0 低名望＋低投入／E3 職務入口／ID 對照信用／
//   E2 文案按 awardsLog 憑據／自選履歷＋曝光＋活動量＋職務＋對照信用單元。
// 用法：node tests/test_v393_logic.js
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
var GIGS = [
  { id:'g_film_lead', type:'電影', title:'《龍虎風雲》男主角', workTitle:'龍虎風雲', roleLabel:'男主角', roleScale:'film_lead_big', genreLabel:'警匪片' },
  { id:'g_film_com', type:'電影', title:'《笑匠當家》諧星', workTitle:'笑匠當家', roleLabel:'諧星', roleScale:'film_support_main', genreLabel:'喜劇片' },
  { id:'g_tv_long', type:'電視劇', title:'《大時代》男主角', workTitle:'大時代', roleLabel:'男主角', roleScale:'tv_lead_long', genreLabel:'時裝劇' },
  { id:'g_var', type:'綜藝', title:'《歡樂今宵》主持', workTitle:'歡樂今宵', roleLabel:'主持', roleScale:'variety_host_lead', genreLabel:'綜藝' },
  { id:'g_ad', type:'廣告', title:'《汽水》代言', workTitle:'汽水', roleLabel:'代言人', roleScale:'ad_lead', genreLabel:'' },
  { id:'g_rec', type:'唱片通告', title:'《新碟》主唱', workTitle:'新碟', roleLabel:'主唱', roleScale:'rec_album', genreLabel:'粵語流行' },
];

const FN_LIST = ['function dateObj','function calendarSeason','function dualTrackNumbers','function readDualTracks','function syncDualTracks',
  'function endingFlag410','function endingDual410','function endingNegTagCount410','function endingBackstageTagCount410','function favorCreditCountsAsHeld','function endingFavor410',
  'function endingRomance410','function endingE2Eligible410','function endingE3Eligible410','function endingBackstageClose410',
  'function end95GenreOf','function end95IsLead','function end95ClassifyWrap','function end95EmptyStats','function end95StatsAddOne',
  'function end95DeriveStats','function careerStats95Of','function end95AddWrap','function end95Awards','function end95EverHeldCredit',
  'function end95StoryDone','function end95ChainsDone','function end95SpineDone','function end95PangProgress','function end95E3Variant','function end95BuildGaps',
  'function end229IsLead','function end229ClassifyLead','function end229EmptyLeadStats',
  'function end229DeriveLeadStats','function leadStats229Of','function end229AddWrap',
  'function isForcedGig392','function day392YearMonth','function end392SelDeriveStats','function careerStats392SelOf',
  'function exposure392Of','function activity392Of','function isLowActivity392',
  'function duty392GigById','function backstageDuties392Of',
  'function forcedCredit392ReplayWraps','function forcedCredit392Of','function forcedCredit392CounterCredit',
  'function endingAward392TvSupport','function endingAward392WonLabel',
  'function resolveEnding410','function endingEveOptions410','function endingEsc410','function endingCareerScene410','function endingSummaryHtml410'];
const CONST_LIST = ['ENDING410_CAREER_NAMES','ENDING410_T','ENDING_NEG_TAGS410','ENDING410_BACKSTAGE_KEYS','ENDING410_EXODUS_NAME_FALLBACK',
  'ENDING410_NPC_NAMES','ENDING95_T','END95_TYPE_MEDIUM','END95_LEAD_SCALES','END95_STRONG_LEAD','END95_GENRE_TYPE_NAMES',
  'END95_COMEDY_G','END95_ACTION_G','END95_COMEDY_KW','END95_ACTION_KW','ENDING410_ADJ_RUMOR','END229_LEAD_MEDIUM','SPINE95_REQUIRED',
  'DUTY392_KIND_BY_ID','DUTY392_GIGS'];
let SRC = "var START = { y:1990, m:1, d:1 };\n" + FN_LIST.map(extractFn).join('\n') + '\n' + CONST_LIST.map(extractConst).join('\n');
CONST_LIST.forEach(n => { SRC = SRC.split('const '+n+' =').join('var '+n+' ='); });
eval(SRC);

ok('harness: v393 函數載入', typeof resolveEnding410 === 'function' && typeof careerStats392SelOf === 'function' && typeof backstageDuties392Of === 'function' && typeof forcedCredit392CounterCredit === 'function');

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
  if(o.careerStats95 && o.careerStats95.leadByMedium && !o.leadStats229){
    o.leadStats229 = { byMedium: Object.assign({ film: 0, tv: 0, music: 0, variety: 0, ad: 0 }, o.careerStats95.leadByMedium) };
  }
  return baseSave(o);
}
function R(save){ S = save; return resolveEnding410(S); }

/* ============ (1) SS 截格——六專長排 SS 之前 ============ */
{
  /* 原被截 FK 存檔：dual 320、電影佔比 60%、電影擔正 2、負標籤 0 */
  const r = R(arc(170, 150, {
    careerStats95: stats95({ total: 80, byMedium: { film: 48, tv: 12, music: 10, variety: 5, ad: 5 },
      leadByMedium: { film: 2 }, genreIdentified: 30, genreComedy: 5, genreAction: 5 }),
  }));
  ok('SS 截格：原被截 FK（dual 320／電影 60%／擔正 2）→ FK，唔係 SS', r.career === 'FK');
}
{
  /* 原被截 CK 存檔：dual 310、喜劇佔比 57%、信用 95 */
  const r = R(arc(160, 150, {
    careerStats95: stats95({ total: 70, byMedium: { film: 20, tv: 15, music: 12, variety: 8, ad: 15 },
      leadByMedium: { film: 1 }, genreIdentified: 30, genreComedy: 17, genreAction: 4 }),
  }));
  ok('SS 截格：原被截 CK（dual 310／喜劇 57%／信用 95）→ CK，唔係 SS', r.career === 'CK');
}
{
  /* 原被截 GH 存檔：dual 300、自選綜藝 10／自選共 18（56%）、彭線 N11 done */
  const r = R(arc(160, 140, {
    careerStats95: stats95({ total: 60, byMedium: { film: 10, tv: 12, music: 8, variety: 20, ad: 10 } }),
    careerStats392Sel: stats95({ total: 18, byMedium: { film: 2, tv: 2, music: 1, variety: 10, ad: 3 } }),
    story: { flags: {}, rel: {}, done: { N11: true }, choices: {} },
  }));
  ok('SS 截格：原被截 GH（dual 300／自選綜藝 10/18／彭線）→ GH，唔係 SS', r.career === 'GH');
}
{
  /* 無專長一般路線：dual 320、媒介平均 → 仍落 SS */
  const r = R(arc(170, 150, {
    careerStats95: stats95({ total: 90, byMedium: { film: 25, tv: 25, music: 20, variety: 10, ad: 10 },
      leadByMedium: { film: 1, tv: 1 }, genreIdentified: 30, genreComedy: 8, genreAction: 8 }),
  }));
  /* v421：ID（聲望主導帶）排 SS 前——fame 170／credit 150 對照信用 150 ≤ max(60,153)，
     呢個聲望行先嘅 profile 派 ID；SS 留畀信用企得穩嘅高雙軌態。 */
  ok('SS 截格：無專長一般路線（dual 320／聲望主導）→ ID（v421 ID 先過 SS）', r.career === 'ID');
}
{
  /* 雙專長重疊：電影＋電視都達標 → FK 排先（FK→TK 次序決勝） */
  const r = R(arc(170, 150, {
    careerStats95: stats95({ total: 80, byMedium: { film: 40, tv: 40, music: 0, variety: 0, ad: 0 },
      leadByMedium: { film: 2, tv: 2 }, tvLongLeads: 1, genreIdentified: 20, genreComedy: 2, genreAction: 2 }),
  }));
  ok('SS 截格：雙專長重疊（電影＋電視）→ FK 排先', r.career === 'FK');
}

/* ============ (2) GH——自選佔比＋8 宗下限 ============ */
{
  const mkSel = (variety, total) => R(arc(160, 140, {
    careerStats95: stats95({ total: 60, byMedium: { film: 10, tv: 12, music: 8, variety: 20, ad: 10 } }),
    careerStats392Sel: stats95({ total: total, byMedium: { film: 0, tv: 0, music: 0, variety: variety, ad: total - variety } }),
    story: { flags: {}, rel: {}, done: { N11: true }, choices: {} },
  }));
  ok('GH：自選綜藝 8/16（50%）→ GH', mkSel(8, 16).career === 'GH');
  /* v421：唔入 GH 之後唔再落 SS——fame 160／credit 140 喺 ID 聲望主導帶（140 ≤ 144），派 ID。 */
  ok('GH：自選綜藝 8/17（47%）→ 唔入 GH（落 ID）', mkSel(8, 17).career === 'ID');
  ok('GH：自選綜藝 7/7（100% 但得 7 宗）→ 唔入 GH（落 ID）', mkSel(7, 7).career === 'ID');
}

/* ============ (3) CR——fame 窗 35–110 ============ */
{
  const mk = (fame, credit) => R(arc(fame, credit, {
    careerStats95: stats95({ total: 30, byMedium: { film: 8, tv: 8, music: 6, variety: 4, ad: 4 }, genreIdentified: 10, genreComedy: 2, genreAction: 2 }),
  }));
  /* 注意：ID 排喺 CR 之前，窗係 credit ≤ max(60, fame×0.9)——CR 邊界 fixture 要用高過 ID 窗嘅信用先至測到 CR 本身 */
  ok('CR：fame 59／credit 70 → CR', mk(59, 70).career === 'CR');
  ok('CR：fame 60／credit 70 → CR（70 > max(60,54)，唔入 ID）', mk(60, 70).career === 'CR');
  ok('CR：原 CR 路線 fame 95／credit 95 → CR（95 > 85.5，唔入 ID）', mk(95, 95).career === 'CR');
  ok('CR：fame 110／credit 105 → CR（105 > 99，唔入 ID）', mk(110, 105).career === 'CR');
  ok('CR：fame 111／credit 105 → 唔入 CR（落 E2）', mk(111, 105).career === 'E2');
}

/* ============ (4) E4——v421 曝光型（fame≥50＋曝光≥6 宗橫跨≥3 月＋影視擔正皆 0；net 已刪） ============ */
{
  const expo6 = [
    { gigId: 'e1', type: '廣告', wrappedDay: 10 }, { gigId: 'e2', type: '廣告', wrappedDay: 15 },
    { gigId: 'e3', type: '綜藝', wrappedDay: 40 }, { gigId: 'e4', type: '綜藝', wrappedDay: 45 },
    { gigId: 'e5', type: '廣告', wrappedDay: 70 }, { gigId: 'e6', type: '廣告', wrappedDay: 75 },
  ];
  const mk = (fame, credit, wh) => R(arc(fame, credit, { wrapHistory: wh || expo6.slice() }));
  /* v421：net 已刪——信用幾高都唔再擋 E4，曝光＋冇影視擔正就係泡沫偶像身份證據 */
  ok('E4：fame 100／credit 94＋曝光 6 宗 → E4', mk(100, 94).career === 'E4');
  ok('E4 邊界：fame 100／credit 95＋曝光 6 宗 → E4（舊 net 邊界已刪）', mk(100, 95).career === 'E4');
  ok('E4 守門：曝光得 5 宗 → 唔入 E4（落 CR）', mk(100, 94, expo6.slice(0, 5)).career === 'CR');
  /* 高信用偶像對照：fame 100／credit 120＋曝光 6 宗＋冇擔正 → E4（ID 窗 120 > max(60,90) 唔入 ID） */
  ok('E4 對照：高信用偶像（fame 100／credit 120）＋曝光 → E4', mk(100, 120).career === 'E4');
  /* v421：曝光態同時合 ID 聲望帶（fame 200／credit 150，對照信用 150 ≤ 180）→ 派 E4 唔派 ID
     （真玩驗證：fame 293／曝光 27 宗／擔正 0 曾被 ID 截走） */
  ok('E4 先過 ID：曝光達標＋冇擔正＋聲望主導 → E4', mk(200, 150).career === 'E4');
  /* v421 守門：有電影擔正 → 唔入 E4（曝光型身份唔成立） */
  const rLead = R(arc(100, 120, { wrapHistory: expo6.slice(),
    careerStats95: stats95({ total: 20, byMedium: { film: 6, tv: 4, music: 2, variety: 4, ad: 4 }, leadByMedium: { film: 1 } }) }));
  ok('E4 守門：有電影擔正＋曝光 → 唔入 E4（落 CR）', rLead.career === 'CR');
}

/* ============ (4b) v421 SS 兜底——具體身份先判、唔使負標籤 ============ */
{
  /* E3 態同時合 SS（dual 310／負標籤 0）→ 派 E3，唔使攞負標籤擋 SS */
  const d2 = [{ kind: '場記', production: '甲組', gigId: 'duty392_clapper_a', day: 100 }, { kind: '剪接助理', production: '乙組', gigId: 'duty392_editor_a', day: 200 }];
  const rE3 = R(arc(150, 160, { backstageDuties392: d2,
    careerStats95: stats95({ total: 40, byMedium: { film: 15, tv: 10, music: 5, variety: 5, ad: 5 }, leadByMedium: { film: 1, tv: 1 } }) }));
  ok('v421：E3 態合 SS 門檻＋負標籤 0 → E3（唔使負標籤避格）', rE3.career === 'E3' && rE3.snapshot.negTags === 0);
  /* SS 仍可達：信用主導高雙軌、冇具體身份證據 → SS */
  const rSS = R(arc(150, 220, {
    careerStats95: stats95({ total: 60, byMedium: { film: 20, tv: 18, music: 10, variety: 6, ad: 6 }, leadByMedium: { film: 1, tv: 1 }, genreIdentified: 20, genreComedy: 4, genreAction: 4 }) }));
  ok('v421：信用主導 dual 370 冇身份證據 → SS 兜底', rSS.career === 'SS');
}

/* ============ (4c) v421 E0 浮沉收尾——安全線標記免被 ID／CR／E2 截走 ============ */
{
  const drift = { conseq61: { reviews: { 1991: { dual: 78, floor: 100, passed: true, week: 104, drift421: true } } } };
  /* 對照：冇標記 fame 68／credit 61（sum 129）→ ID（聲望帶成立） */
  ok('E0 對照：冇浮沉標記 fame 68／credit 61 → ID', R(arc(68, 61)).career === 'ID');
  /* 有標記＋sum<140 → E0（主線強制 fame 推入 ID 窗都唔截走真浮沉） */
  ok('v421：浮沉標記＋sum 129 → E0（免 ID／CR／E2 截走）', R(arc(68, 61, drift)).career === 'E0');
  /* 有標記但 sum≥140 → 唔再係浮沉，照正常判定 */
  ok('v421：浮沉標記＋sum 150 → ID（雙軌回升照派更好格）', R(arc(80, 70, drift)).career === 'ID');
}

/* ============ (5) E3／E5 職務入口（單元） ============ */
{
  const d2 = [{ kind: '場記', production: '甲組', gigId: 'duty392_clapper_a', day: 100 }, { kind: '剪接助理', production: '乙組', gigId: 'duty392_editor_a', day: 200 }];
  const s = baseSave({ backstageDuties392: d2 });
  const out = backstageDuties392Of(s);
  ok('職務單元：2 種／2 製作 → tagEntrance 開、relEntrance 唔開', out.tagEntrance === true && out.relEntrance === false && out.total === 2 && out.kinds.length === 2);
  const s3 = baseSave({ backstageDuties392: d2.concat([{ kind: '副導演助理', production: '丙組', gigId: 'duty392_ad_a', day: 300 }]) });
  const out3 = backstageDuties392Of(s3);
  ok('職務單元：3 宗／3 製作 → relEntrance 開', out3.relEntrance === true && out3.total === 3);
  const sSame = baseSave({ backstageDuties392: [{ kind: '場記', production: '甲組', gigId: 'duty392_clapper_a', day: 100 }, { kind: '剪接助理', production: '甲組', gigId: 'duty392_editor_a', day: 200 }] });
  const outSame = backstageDuties392Of(sSame);
  ok('職務單元：兩種職務同一製作 → 兩個入口都唔開（製作得 1 個）', outSame.tagEntrance === false && outSame.relEntrance === false && outSame.total === 2 && outSame.productions.length === 1);
  const sDup = baseSave({ backstageDuties392: [{ kind: '場記', production: '甲組', gigId: 'duty392_clapper_a', day: 100 }, { kind: '場記', production: '乙組', gigId: 'duty392_clapper_b', day: 200 }] });
  const outDup = backstageDuties392Of(sDup);
  ok('職務單元：兩次同類職務（唔同製作）→ kinds 得 1，標籤入口唔開', outDup.kinds.length === 1 && outDup.tagEntrance === false);
  const sWrap = baseSave({ wrapHistory: [{ gigId: 'duty392_clapper_a', type: '電影', wrappedDay: 50 }, { gigId: 'duty392_editor_a', type: '電視劇', wrappedDay: 60 }] });
  const outWrap = backstageDuties392Of(sWrap);
  ok('職務單元：無 log 嗰陣由 wrapHistory＋職務表衍生', outWrap.tagEntrance === true && outWrap.total === 2);
}

/* ============ (6) ID——對照信用 ============ */
{
  /* fame 100／credit 100：實信用 100 > max(60,90)＝90 → 唔入 ID（落 CR） */
  const rNo = R(arc(100, 100, {
    careerStats95: stats95({ total: 30, byMedium: { film: 8, tv: 8, music: 6, variety: 4, ad: 4 }, genreIdentified: 10, genreComedy: 2, genreAction: 2 }),
  }));
  ok('ID：fame 100／credit 100、無強制增量 → 唔入 ID（落 CR）', rNo.career === 'CR');
  /* 同數值＋強制帳 {direct:15, fame:5}：對照信用＝round(95×0.5)=48＋(50−15)=83 ≤90 → ID */
  const rYes = R(arc(100, 100, {
    forcedCredit392: { direct: 15, fame: 5, wraps: 5, choices: 3, backfilled: false },
    careerStats95: stats95({ total: 30, byMedium: { film: 8, tv: 8, music: 6, variety: 4, ad: 4 }, genreIdentified: 10, genreComedy: 2, genreAction: 2 }),
  }));
  ok('ID：同數值＋強制增量 15／強制 fame 5 → 對照信用 83 → ID', rYes.career === 'ID' && rYes.snapshot.forcedCredit392.counterCredit === 83);
  /* 對照組：同終局 fame、靠自選推高信用（無強制帳）→ 唔入 ID */
  const rSelf = R(arc(100, 100, {
    careerStats95: stats95({ total: 30, byMedium: { film: 8, tv: 8, music: 6, variety: 4, ad: 4 }, genreIdentified: 10, genreComedy: 2, genreAction: 2 }),
  }));
  ok('ID 對照組：自選推高信用、無強制增量 → 唔入 ID', rSelf.career === 'CR');
}

/* ============ (7) E0——低名望＋低投入 ============ */
{
  const mk = (fame, credit, over) => R(arc(fame, credit, over || {}));
  ok('E0：fame 36、零投入 → E0', mk(36, 36).career === 'E0');
  ok('E0：fame 40、投入 2 宗 → E0', mk(40, 42, { trainCount: { train_acting: 2 } }).career === 'E0');
  ok('E0 邊界：fame 41、零投入 → 唔係低名望（落 E2：信用 42）', mk(41, 42).career === 'E2');
  ok('E0 邊界：fame 40、投入 3 宗 → 唔係低投入（落 E2：信用 42）', mk(40, 42, { trainCount: { train_acting: 3 } }).career === 'E2');
  ok('E0：只做糊口兼職（零通告／零試鏡／零訓練）→ E0', mk(36, 36).career === 'E0');
}

/* ============ 單元：自選履歷／曝光／活動量／對照重播 ============ */
{
  const hist = [
    { gigId: 'g_film_lead', type: '電影', wrappedDay: 10, totalDays: 25 },
    { gigId: 'g_var', type: '綜藝', wrappedDay: 20, totalDays: 3 },
    { gigId: 'g_film_com', type: '電影', wrappedDay: 30, totalDays: 5 },
  ];
  const st = baseSave({ wrapHistory: hist.slice() });
  const sel = careerStats392SelOf(st);
  ok('自選履歷：由 wrapHistory 衍生（total 3、film 2、variety 1）', sel.total === 3 && sel.byMedium.film === 2 && sel.byMedium.variety === 1);
  const stF = baseSave({ wrapHistory: hist.slice(), flags: { 'grant229_delivered_g_var': 1 } });
  const selF = careerStats392SelOf(stF);
  ok('自選履歷：強制即派剔出（total 2、variety 0）', selF.total === 2 && selF.byMedium.variety === 0);
  const stDuty = baseSave({ wrapHistory: [{ gigId: 'duty392_clapper_a', type: '電影', wrappedDay: 10, totalDays: 2 }, { gigId: 'g_film_lead', type: '電影', wrappedDay: 20, totalDays: 25 }] });
  const selD = careerStats392SelOf(stDuty);
  ok('自選履歷：幕後職務唔入演藝通告計數（total 1）', selD.total === 1 && selD.byMedium.film === 1);
  const stCnt = baseSave({ careerStats392Sel: stats95({ total: 5, byMedium: { film: 3, variety: 2 } }), wrapHistory: hist.slice() });
  ok('自選履歷：有計數器就讀計數器（total 5）', careerStats392SelOf(stCnt).total === 5);
  const stOld = baseSave({ careerStats95: stats95({ total: 4, byMedium: { film: 2, variety: 2 } }) });
  ok('自選履歷：無履歷嗰陣跌返 careerStats95 副本', careerStats392SelOf(stOld).total === 4);
}
{
  const st = baseSave({ wrapHistory: [
    { gigId: 'a1', type: '廣告', wrappedDay: 10 }, { gigId: 'a2', type: '廣告', wrappedDay: 40 },
    { gigId: 'v1', type: '綜藝', wrappedDay: 70 }, { gigId: 'v2', type: '綜藝', wrappedDay: 75 },
    { gigId: 'f1', type: '電影', wrappedDay: 80 },
  ] });
  const ex = exposure392Of(st);
  ok('曝光：廣告／綜藝 4 宗、橫跨 3 個月', ex.count === 4 && ex.months === 3);
  const stF = baseSave({ wrapHistory: [
    { gigId: 'a1', type: '廣告', wrappedDay: 10 }, { gigId: 'a2', type: '廣告', wrappedDay: 40 },
    { gigId: 'v1', type: '綜藝', wrappedDay: 70 },
  ], flags: { 'grant229_recorded_v1': 1 } });
  const exF = exposure392Of(stF);
  ok('曝光：強制即派剔出（2 宗／2 個月）', exF.count === 2 && exF.months === 2);
}
{
  const st = baseSave({
    wrapHistory: [{ gigId: 'g_film_lead', type: '電影', wrappedDay: 10, totalDays: 25 }],
    aud91Log: [{ gigId: 'g_x' }, { gigId: 'g_y' }],
    trainCount: { train_acting: 2, train_stage: 1 },
  });
  const a = activity392Of(st);
  ok('活動量：通告 1＋試鏡 2＋訓練 3 ＝ 6', a.wraps === 1 && a.auditions === 2 && a.training === 3 && a.total === 6);
  ok('低投入：fame 40＋活動 6 → 唔係低投入', isLowActivity392(arc(40, 42, { wrapHistory: [{ gigId: 'g_film_lead', type: '電影', wrappedDay: 10, totalDays: 25 }], aud91Log: [{ gigId: 'g_x' }, { gigId: 'g_y' }], trainCount: { train_acting: 2, train_stage: 1 } })) === false);
  ok('低投入：fame 40＋活動 0 → 係低投入', isLowActivity392(arc(40, 42)) === true);
}
{
  /* 對照重播：同一季 5 宗強制殺青 → 季上限 4；另加 1 宗自選唔計 */
  const st = baseSave({
    wrapHistory: [
      { gigId: 'f1', type: '電影', wrappedDay: 10, fame: 5 },
      { gigId: 'f2', type: '電影', wrappedDay: 20, fame: 5 },
      { gigId: 'f3', type: '電影', wrappedDay: 30, fame: 5 },
      { gigId: 'f4', type: '電影', wrappedDay: 40, fame: 5 },
      { gigId: 'f5', type: '電影', wrappedDay: 50, fame: 5 },
      { gigId: 's1', type: '電影', wrappedDay: 60, fame: 5 },
    ],
    flags: { 'grant229_delivered_f1': 1, 'grant229_delivered_f2': 1, 'grant229_delivered_f3': 1, 'grant229_delivered_f4': 1, 'grant229_delivered_f5': 1 },
  });
  const fc = forcedCredit392Of(st);
  ok('對照重播：5 宗強制殺青同一季 → direct 封頂 4、fame 25', fc.direct === 4 && fc.fame === 25);
  const stLed = baseSave({ forcedCredit392: { direct: 7, fame: 12, wraps: 4, choices: 2, backfilled: true } });
  const fcLed = forcedCredit392Of(stLed);
  ok('對照帳：有帳就讀帳（direct 7／fame 12）', fcLed.direct === 7 && fcLed.fame === 12);
  ok('對照信用：無強制增量 → 回 null', forcedCredit392CounterCredit(baseSave({})) === null);
}

/* ============ (9) E2 文案——按 awardsLog 憑據 ============ */
{
  const scene = (awardsLog) => { S = baseSave({ awardsLog: awardsLog || [] }); return endingCareerScene410({ career: 'E2', adjPicked: {} }); };
  ok('E2 文案：0 勝／0 提名 → 只出主文，唔提最佳男配角', !scene([]).includes('最佳男配角'));
  ok('E2 文案：舊檔欠紀錄（awardsLog 缺失）→ 只出主文', (()=>{ S = baseSave({}); delete S.awardsLog; return !endingCareerScene410({ career: 'E2', adjPicked: {} }).includes('最佳男配角'); })());
  ok('E2 文案：只有該獎提名 → 出提名句', scene([{ medium: 'tv', categories: [{ id: 'cat_tv_support_m', outcome: 'nominated', repTitle: '某劇' }] }]).includes('入圍了電視台最佳男配角'));
  ok('E2 文案：贏得該獎 → 出得獎句', scene([{ medium: 'tv', categories: [{ id: 'cat_tv_support_m', outcome: 'won', repTitle: '某劇' }] }]).includes('拿下了電視台最佳男配角'));
  ok('E2 文案：只贏其他獎 → 唔出電視台最佳男配角句', !scene([{ medium: 'film', categories: [{ id: 'cat_film_support_m', outcome: 'won', repTitle: '某片' }] }]).includes('電視台最佳男配角'));
  ok('E2 文案：同一獎既有提名又有勝出 → 只顯示勝出句', (()=>{ const s = scene([{ medium: 'tv', categories: [{ id: 'cat_tv_support_m', outcome: 'nominated', repTitle: '某劇' }] }, { medium: 'tv', categories: [{ id: 'cat_tv_support_m', outcome: 'won', repTitle: '某劇' }] }]); return s.includes('拿下了電視台最佳男配角') && !s.includes('入圍了電視台最佳男配角'); })());
  ok('E2 文案：主文係甘草敘事（有「金牌甘草」／穩字）', scene([]).includes('甘草'));
  /* E1 同樣寫死獎名已修：贏電視台最佳男配角以外嘅獎 → E1 場景唔寫最佳男配角 */
  S = baseSave({ awardsLog: [{ medium: 'film', categories: [{ id: 'cat_film_lead_m', outcome: 'won', repTitle: '某片' }] }] });
  const e1scene = endingCareerScene410({ career: 'E1', adjPicked: {} });
  ok('E1 文案：贏其他獎 → 唔寫死最佳男配角', !e1scene.includes('最佳男配角'));
}

console.log('\nv393 logic: ' + pass + ' passed, ' + fail + ' failed');
if(fail) process.exit(1);
