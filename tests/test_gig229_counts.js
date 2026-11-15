// v20a229 B4 提名＋擔正計數・邏輯測試
// 合約（AUDIT229 §4；SPEC §2.9 擔正定義；DECISIONS D-3／D-9）：
//   A4 countYearMediumWraps 只計 category＝作品嘅殺青（臨記通告／補拍通告唔計提名池）；
//      寫入點（wrapHistory unshift／PSR pack）要寫埋 category；無 category 嘅舊檔／fixture
//      當作品計（舊口徑），唔跌舊數；提名門檻數字本身唔變。
//   A5 擔正累計式計數器 S.leadStats229（SPEC §2.9 五組 roleScale＋roleLabel；替身唔計）：
//      殺青嗰刻寫入（end229AddWrap，wrapHistory unshift 之前）；跨年累加，唔受 wrapHistory
//      90 條窗口影響；按媒介分開計；舊檔由 wrapHistory 衍生種子（normalizeSaveObj 回填）。
//   A6 結局梯（E1／FK／TK）讀新計數器——舊計數器 leadByMedium 寫乜都唔影響判定（單一來源）。
// 反證：B4 之前嘅 code → A4 臨記計入 FAIL、A5 二番／tv_lead／mtv 當擔正 FAIL、
//   A6 舊計數器零擔正但新計數器有擔正嗰陣 E1 落 SS FAIL。
// 用法：node tests/test_gig229_counts.js
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
let fails = 0;
function ok(name, cond, extra){
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : ''));
  if(!cond) fails++;
}
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) return null;
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){ if(html[j]==='{') depth++; else if(html[j]==='}'){ depth--; if(depth===0) break; } }
  return html.slice(i, j+1);
}
function extractConst(name){
  for(const kw of ['const ', 'var ']){
    const i = html.indexOf(kw+name+' =');
    if(i<0) continue;
    let depth=0, started=false;
    for(let k=i; k<html.length; k++){
      const ch = html[k];
      if(ch==='{'||ch==='['){ depth++; started = true; }
      else if(ch==='}'||ch===']'){ depth--; if(started && depth===0) return html.slice(i, k+1)+';'; }
      else if(ch===';' && !started) return html.slice(i, k+1);
    }
  }
  return null;
}

var START = { y:1990, m:1, d:1 };
var S = null;
/* 假通告庫（分類器／衍生／計數共用；roleScale＋roleLabel＋category 齊） */
var GIGS = [
  { id:'g_film_lead', type:'電影', title:'《大製作》男主角', roleLabel:'男主角', roleScale:'film_lead_big', category:'作品' },
  { id:'g_film_second', type:'電影', title:'《二番戲》第二男主角', roleLabel:'第二男主角', roleScale:'film_second_lead', category:'作品' },
  { id:'g_tv_lead', type:'電視劇', title:'《長篇劇》男主角', roleLabel:'男主角', roleScale:'tv_lead_long', category:'作品' },
  { id:'g_tv_lead_short', type:'電視劇', title:'《短劇》男主角', roleLabel:'男主角', roleScale:'tv_lead', category:'作品' },
  { id:'g_rec_lead', type:'唱片通告', title:'《大碟》主唱', roleLabel:'大碟主唱', roleScale:'rec_album', category:'作品' },
  { id:'g_rec_chorus', type:'唱片通告', title:'《和音碟》', roleLabel:'和音歌手', roleScale:'rec_album', category:'作品' },
  { id:'g_mtv_lead', type:'唱片通告', title:'《冠軍歌MV》男主角', roleLabel:'男主角', roleScale:'mtv', category:'作品' },
  { id:'g_ad_lead', type:'廣告', title:'《品牌片》代言', roleLabel:'形象廣告代言', roleScale:'ad_av', category:'作品' },
  { id:'g_ad_star', type:'廣告', title:'《品牌片》主角', roleLabel:'廣告主角', roleScale:'ad_av', category:'作品' },
  { id:'g_ad_extra', type:'廣告', title:'《街招》路人', roleLabel:'廣告路人', roleScale:'ad_av', category:'作品' },
  { id:'g_var_lead', type:'綜藝', title:'《台慶晚會》主持', roleLabel:'台慶晚會主持', roleScale:'variety_special', category:'作品' },
  { id:'g_var_ep', type:'綜藝', title:'《遊戲夜》主持', roleLabel:'遊戲環節主持', roleScale:'variety_ep', category:'作品' },
  { id:'g_stunt', type:'電影', title:'《武打戲》替身', roleLabel:'男主角替身', roleScale:'film_lead_big', category:'臨記通告' },
  { id:'g_extra', type:'電影', title:'《臨記工》', roleLabel:'臨記', roleScale:'film_support_small', category:'臨記通告' },
  { id:'g_repair', type:'電影', title:'《補拍》', roleLabel:'補拍臨記', roleScale:'film_support_small', category:'補拍通告' }
];
function gig(id){ return GIGS.find(g=>g.id===id) || null; }

eval(extractConst('END229_LEAD_MEDIUM').replace('const END229_LEAD_MEDIUM =', 'var END229_LEAD_MEDIUM ='));
eval(['end229IsLead','end229ClassifyLead','end229EmptyLeadStats','end229DeriveLeadStats','leadStats229Of','end229AddWrap',
 'gig229CategoryOf','countYearMediumWraps','awardsYearFromDay','awardsCalendarYear'].map(extractFn).join('\n'));
var ensurePostShootRewardLog = function(){ return (S && S.postShootRewards) || []; };

/* ================= A SPEC §2.9 擔正分類器 ================= */
ok('A1 電影大製作男主角 → film', end229ClassifyLead(gig('g_film_lead')) === 'film');
ok('A2 電視長劇男主角 → tv', end229ClassifyLead(gig('g_tv_lead')) === 'tv');
ok('A3 大碟主唱 → music', end229ClassifyLead(gig('g_rec_lead')) === 'music');
ok('A4 廣告代言 → ad', end229ClassifyLead(gig('g_ad_lead')) === 'ad');
ok('A5 廣告主角（含主角）→ ad', end229ClassifyLead(gig('g_ad_star')) === 'ad');
ok('A6 綜藝特輯主持 → variety', end229ClassifyLead(gig('g_var_lead')) === 'variety');
ok('A7 二番男主角唔係擔正（舊闊定義會計，SPEC 唔計）', end229ClassifyLead(gig('g_film_second')) === '');
ok('A8 tv_lead（唔係長劇）男主角唔係擔正', end229ClassifyLead(gig('g_tv_lead_short')) === '');
ok('A9 大碟和音唔係擔正', end229ClassifyLead(gig('g_rec_chorus')) === '');
ok('A10 MTV 男主角唔係擔正', end229ClassifyLead(gig('g_mtv_lead')) === '');
ok('A11 廣告路人唔係擔正', end229ClassifyLead(gig('g_ad_extra')) === '');
ok('A12 單集綜藝主持唔係擔正', end229ClassifyLead(gig('g_var_ep')) === '');
ok('A13 替身唔係擔正（roleScale 話大製作都唔計）', end229ClassifyLead(gig('g_stunt')) === '');
ok('A14 臨記唔係擔正', end229ClassifyLead(gig('g_extra')) === '');

/* ================= B A4 提名計數讀 category ================= */
function wrap(gigId, type, category, wrappedDay){
  const w = { gigId: gigId, type: type, wrappedDay: wrappedDay };
  if(category !== undefined) w.category = category;
  return w;
}
S = { dayIndex: 500, wrapHistory: [], postShootRewards: [] };
S.wrapHistory = [wrap('w1', '電影', '作品', 120), wrap('w2', '電影', '作品', 130)];
ok('B1 兩張作品 → 計 2', countYearMediumWraps(['電影'], 1990) === 2);
S.wrapHistory = [wrap('w1', '電影', '臨記通告', 120), wrap('w2', '電影', '臨記通告', 130)];
ok('B2 兩張臨記通告 → 計 0', countYearMediumWraps(['電影'], 1990) === 0);
S.wrapHistory = [wrap('w1', '電影', '作品', 120), wrap('w2', '電影', '臨記通告', 130)];
ok('B3 一作品一臨記 → 計 1', countYearMediumWraps(['電影'], 1990) === 1);
S.wrapHistory = [wrap('w1', '電影', '補拍通告', 120), wrap('w2', '電影', '補拍通告', 130)];
ok('B4 補拍通告 → 計 0', countYearMediumWraps(['電影'], 1990) === 0);
S.wrapHistory = [wrap('w1', '電影', undefined, 120), wrap('w2', '電影', undefined, 130)];
ok('B5 無 category 舊檔 → 當作品計 2（唔跌舊數）', countYearMediumWraps(['電影'], 1990) === 2);
S.wrapHistory = [wrap('g_extra', '電影', undefined, 120), wrap('g_extra', '電影', undefined, 130)];
ok('B6 無 category 但 gigId 查到臨記通告 → 計 0', countYearMediumWraps(['電影'], 1990) === 0);
S.wrapHistory = [wrap('w1', '電影', '作品', 485)];
ok('B7 1991 年作品唔計入 1990（計入 1991 係 1）',
  countYearMediumWraps(['電影'], 1990) === 0 && countYearMediumWraps(['電影'], 1991) === 1);
S.wrapHistory = [wrap('w1', '電影', '作品', 120)];
ok('B8 媒介唔啱唔計（電視劇桶唔計電影作品）', countYearMediumWraps(['電視劇'], 1990) === 0);
S.wrapHistory = [];
S.postShootRewards = [
  { gigId: 'p1', gigType: '電影', category: '作品', dayIndex: 120 },
  { gigId: 'p2', gigType: '電影', category: '作品', dayIndex: 130 }
];
ok('B9 PSR 兩張作品 → 計 2', countYearMediumWraps(['電影'], 1990) === 2);
S.postShootRewards = [
  { gigId: 'p1', gigType: '電影', category: '臨記通告', dayIndex: 120 },
  { gigId: 'p2', gigType: '電影', category: '臨記通告', dayIndex: 130 }
];
ok('B10 PSR 兩張臨記通告 → 計 0', countYearMediumWraps(['電影'], 1990) === 0);
S.wrapHistory = [wrap('w1', '電影', '作品', 120)];
S.postShootRewards = [{ gigId: 'w1', gigType: '電影', category: '作品', dayIndex: 120 }];
ok('B11 wrap＋PSR 鏡像同一殺青 → 取 max 係 1，唔係 2', countYearMediumWraps(['電影'], 1990) === 1);

/* ================= C PSR pack 寫 category ================= */
(function(){
  var S2 = { dayIndex: 30, fame: 10, postShootRewards: [] };
  var FREEPLAY_FW = { postShootRewards: { templates: { press: [], news: [], streetFans: [], metrics: [] }, metricKindLabels: {} } };
  var postShootCopyLine = function(v, fb){ return (v==null || v==='') ? fb : v; };
  var postShootDisplayTitle = function(sh){ return (sh && (sh.title || sh.workTitle)) || ''; };
  var postShootMetricKindForType = function(t){ return t==='電影' ? 'boxOffice' : 'attention'; };
  var postShootPickTemplate = function(){
    return { id:'t1', paperName:'娛樂版', headline:'h', dek:'d', outlet:'o', line:'l',
      place:'街上', title:'t', valueLine:'v', blurb:'b', label:'關注度', metricKind:'attention' };
  };
  var _S = S; S = S2;
  var _G = GIGS;
  eval(extractFn('buildPostShootRewardPack'));
  var p1 = buildPostShootRewardPack({ gigId:'g_film_lead', type:'電影', title:'《大製作》男主角' });
  var p2 = buildPostShootRewardPack({ gigId:'g_extra', type:'電影', title:'《臨記工》' });
  var p3 = buildPostShootRewardPack({ gigId:'g_unknown', type:'電影', title:'《唔知》' });
  ok('C1 PSR pack：作品 gig 寫 category＝作品', p1.category === '作品');
  ok('C2 PSR pack：臨記 gig 寫 category＝臨記通告', p2.category === '臨記通告');
  ok('C3 PSR pack：查唔到 gig 寫空字串（唔扮作品）', p3.category === '');
  S = _S; GIGS = _G;
})();

/* ================= D A5 擔正計數器：寫入／衍生／窗口 ================= */
{
  const st = { wrapHistory: [], leadStats229: null };
  end229AddWrap(st, gig('g_film_lead'));
  ok('D1 殺青電影擔正 → film 1', st.leadStats229 && st.leadStats229.byMedium.film === 1);
  end229AddWrap(st, gig('g_tv_lead'));
  end229AddWrap(st, gig('g_rec_lead'));
  end229AddWrap(st, gig('g_ad_lead'));
  end229AddWrap(st, gig('g_var_lead'));
  ok('D2 五媒介擔正各計各（film／tv／music／ad／variety 各 1）',
    st.leadStats229.byMedium.film === 1 && st.leadStats229.byMedium.tv === 1
    && st.leadStats229.byMedium.music === 1 && st.leadStats229.byMedium.ad === 1
    && st.leadStats229.byMedium.variety === 1);
  end229AddWrap(st, gig('g_film_second'));
  end229AddWrap(st, gig('g_stunt'));
  end229AddWrap(st, gig('g_extra'));
  ok('D3 二番／替身／臨記殺青唔加擔正數', st.leadStats229.byMedium.film === 1 && st.leadStats229.byMedium.tv === 1);
  let threw = false;
  try{ end229AddWrap(st, null); }catch(e){ threw = true; }
  ok('D4 空 gig 唔 throw、計數唔郁', !threw && st.leadStats229.byMedium.film === 1);
}
{
  const st = { wrapHistory: [{ gigId:'g_film_lead' }, { gigId:'g_tv_lead' }], leadStats229: null };
  end229AddWrap(st, gig('g_ad_lead'));
  ok('D5 首次寫入以當刻 wrapHistory 做種子再加本單（film 1／tv 1／ad 1，唔雙計）',
    st.leadStats229.byMedium.film === 1 && st.leadStats229.byMedium.tv === 1 && st.leadStats229.byMedium.ad === 1);
}
{
  const st = { wrapHistory: [], leadStats229: { byMedium: { film: 3, tv: 0, music: 0, variety: 0, ad: 0 } } };
  ok('D6 計數器唔受 wrapHistory 窗口影響：履歷清空，film 照係 3', leadStats229Of(st).byMedium.film === 3);
  end229AddWrap(st, gig('g_film_lead'));
  ok('D7 有計數器嗰陣寫入直接累加（3→4），唔會由履歷重衍生', st.leadStats229.byMedium.film === 4);
}
{
  const hist = [];
  for(let i=0;i<95;i++) hist.push({ gigId:'g_extra' });
  hist.push({ gigId:'g_film_lead' }, { gigId:'g_film_lead' }, { gigId:'g_tv_lead' },
    { gigId:'g_rec_lead' }, { gigId:'g_ad_lead' });
  const d = end229DeriveLeadStats({ wrapHistory: hist });
  ok('D8 衍生掃晒全履歷（100 條入面 5 個擔正照計，唔受 90 條窗口截）',
    d.byMedium.film === 2 && d.byMedium.tv === 1 && d.byMedium.music === 1 && d.byMedium.ad === 1);
  const st2 = { wrapHistory: [{ gigId:'g_film_lead' }] };
  const got = leadStats229Of(st2);
  ok('D9 唯讀衍生唔寫入存檔（st2.leadStats229 照舊 undefined）',
    got.byMedium.film === 1 && st2.leadStats229 === undefined);
  const d2 = end229DeriveLeadStats({ wrapHistory: [
    { type:'電影', roleLabel:'男主角', roleScale:'film_lead_big', title:'《舊作》男主角' } ] });
  ok('D10 搵唔到 gig 嗰陣用條目本身 roleScale／roleLabel 兜底', d2.byMedium.film === 1);
}
{
  var STRESS_MAX = 100, STAT_MAX = {};
  eval(extractFn('normalizeSaveObj'));
  const o = { wrapHistory: [{ gigId:'g_film_lead' }, { gigId:'g_tv_lead' }] };
  normalizeSaveObj(o);
  ok('E0 normalizeSaveObj 回填擔正種子（film 1／tv 1）',
    o.leadStats229 && o.leadStats229.byMedium.film === 1 && o.leadStats229.byMedium.tv === 1);
  normalizeSaveObj(o);
  ok('E0b 回填冪等（再行一次唔雙計）', o.leadStats229.byMedium.film === 1);
  const o2 = { wrapHistory: [{ gigId:'g_film_lead' }], leadStats229: { byMedium: { film: 2, tv: 1, music: 0, variety: 0, ad: 0 } } };
  normalizeSaveObj(o2);
  ok('E0c 已有計數器唔郁（film 照係 2）', o2.leadStats229.byMedium.film === 2);
}

/* ================= F 結局梯讀新計數器（單一來源） ================= */
(function(){
  const FN_LIST = ['function dateObj','function calendarSeason','function dualTrackNumbers','function readDualTracks','function syncDualTracks',
    'function endingFlag410','function endingDual410','function endingNegTagCount410','function endingBackstageTagCount410','function endingFavor410',
    'function endingRomance410','function endingE2Eligible410','function endingE3Eligible410','function endingBackstageClose410',
    'function end95GenreOf','function end95IsLead','function end95ClassifyWrap','function end95EmptyStats','function end95StatsAddOne',
    'function end95DeriveStats','function careerStats95Of','function end95AddWrap','function end95Awards','function end95EverHeldCredit',
    'function end95StoryDone','function end95ChainsDone','function end95PangProgress','function end95E3Variant','function end95BuildGaps',
    'function end229IsLead','function end229ClassifyLead','function end229EmptyLeadStats',
    'function end229DeriveLeadStats','function leadStats229Of','function end229AddWrap',
    'function resolveEnding410','function endingEveOptions410','function endingEsc410','function endingCareerScene410','function endingSummaryHtml410'];
  const CONST_LIST = ['ENDING410_CAREER_NAMES','ENDING410_T','ENDING_NEG_TAGS410','ENDING410_BACKSTAGE_KEYS','ENDING410_EXODUS_NAME_FALLBACK',
    'ENDING410_NPC_NAMES','ENDING95_T','END95_TYPE_MEDIUM','END95_LEAD_SCALES','END95_STRONG_LEAD','END95_GENRE_TYPE_NAMES',
    'END95_COMEDY_G','END95_ACTION_G','END95_COMEDY_KW','END95_ACTION_KW','ENDING410_ADJ_RUMOR','END229_LEAD_MEDIUM'];
  let SRC = 'var START = { y:1990, m:1, d:1 };\n' + FN_LIST.map(n => extractFn(n.replace(/^function /, ''))).join('\n') + '\n' + CONST_LIST.map(extractConst).join('\n');
  CONST_LIST.forEach(n => { SRC = SRC.split('const '+n+' =').join('var '+n+' ='); });
  eval(SRC);
  function baseSave(over){
    return Object.assign({
      dayIndex: 1060, money: 9000, fame: 20, stage: 0, acting: 0, popularity: 30, stress: 0,
      industryCredit: 0, industryCreditDelta: 0,
      flags: {}, routes: {}, mockCredits: [], mockDebts: [], mockRumors: [], inventory: {},
      castingTags: [], npcs: { agent: 0, director: 0, colleague: 0, reporter: 0, stylist: 0, rival: 0 },
      favorLedger: { settled: 0, credits: 0, exodus: [], counted: {} },
      story: { flags: {}, rel: {}, done: {}, choices: {} },
      awardsLog: [], wrapHistory: [], trainCount: {}, stars: {}, intelFlags: {}, wf3: {}
    }, over || {});
  }
  function stats95(o){
    const base = { total: 0, byMedium: { film:0, tv:0, music:0, variety:0, ad:0 },
      leadByMedium: { film:0, tv:0, music:0, variety:0, ad:0 },
      tvLongLeads: 0, genreIdentified: 0, genreComedy: 0, genreAction: 0, backstageWorks: 0 };
    if(o) Object.keys(o).forEach(k => {
      if(k === 'byMedium' || k === 'leadByMedium') Object.assign(base[k], o[k]);
      else base[k] = o[k];
    });
    return base;
  }
  function arc(fame, credit, over){
    const delta = credit - Math.round(fame * 0.5);
    return baseSave(Object.assign({ fame: fame, industryCreditDelta: delta }, over || {}));
  }
  function R(save){ S = save; return resolveEnding410(S); }
  const win = [{ medium: 'film', categories: [{ id: 'w', outcome: 'won', repTitle: '丙片' }] }];
  {
    const st = arc(190, 215, {
      careerStats95: stats95({ total: 100,
        byMedium: { film: 34, tv: 26, music: 22, variety: 10, ad: 8 },
        leadByMedium: { film: 0, tv: 0, music: 0, variety: 0, ad: 0 },
        tvLongLeads: 0, genreIdentified: 36, genreComedy: 9, genreAction: 9 }),
      leadStats229: { byMedium: { film: 1, tv: 1, music: 0, variety: 0, ad: 0 } },
      awardsLog: win, wf3: { liaoHarvestDone: 1 }
    });
    const r = R(st);
    ok('F1 E1：舊計數器零擔正、新計數器兩媒介擔正 → 照上 E1（讀新唔讀舊）',
      r.career === 'E1' && r.ladder95.leadMedia.length === 2);
  }
  {
    const st = arc(190, 215, {
      careerStats95: stats95({ total: 100,
        byMedium: { film: 34, tv: 26, music: 22, variety: 10, ad: 8 },
        leadByMedium: { film: 3, tv: 2, music: 1 },
        tvLongLeads: 2, genreIdentified: 36, genreComedy: 9, genreAction: 9 }),
      leadStats229: { byMedium: { film: 0, tv: 0, music: 0, variety: 0, ad: 0 } },
      awardsLog: win, wf3: { liaoHarvestDone: 1 }
    });
    const r = R(st);
    ok('F2 E1：舊計數器話有擔正、新計數器零擔正 → 唔上 E1（落 SS，差邊瓣講擔正）',
      r.career === 'SS' && r.ladder95.leadMedia.length === 0 && r.gaps95.some(g => /擔正/.test(g)));
  }
  {
    const st = arc(120, 115, {
      careerStats95: stats95({ total: 70,
        byMedium: { film: 42, tv: 10, music: 8, variety: 5, ad: 5 },
        leadByMedium: { film: 0 }, tvLongLeads: 0, genreIdentified: 26, genreComedy: 6, genreAction: 7 }),
      leadStats229: { byMedium: { film: 2, tv: 0, music: 0, variety: 0, ad: 0 } }
    });
    ok('F3 FK：電影擔正讀新計數器（舊計數器 0 都照上 FK）', R(st).career === 'FK');
  }
  {
    const st = arc(110, 120, {
      careerStats95: stats95({ total: 72,
        byMedium: { film: 12, tv: 40, music: 10, variety: 6, ad: 4 },
        leadByMedium: { tv: 0 }, tvLongLeads: 0, genreIdentified: 30, genreComedy: 8, genreAction: 5 }),
      leadStats229: { byMedium: { film: 0, tv: 1, music: 0, variety: 0, ad: 0 } }
    });
    ok('F4 TK：電視長劇擔正讀新計數器（舊 tvLongLeads 0 都照上 TK）', R(st).career === 'TK');
  }
})();

/* ================= G 靜態接線 ================= */
ok('G1 殺青結算呼叫 end229AddWrap（同 end95AddWrap 同一位置、wrapHistory 之前）',
  html.includes('if(_g95 && typeof end229AddWrap==="function") end229AddWrap(S, _g95);'));
ok('G2 存檔預設有 leadStats229: null（唔改 SAVE key／softRev）',
  html.includes('leadStats229: null,'));
ok('G3 normalizeSaveObj 回填 leadStats229',
  html.includes('o.leadStats229 = end229DeriveLeadStats(o);'));
ok('G4 wrapHistory 寫入帶 category',
  html.includes('category: _wg59w ? (_wg59w.category||"") : ""'));
ok('G5 結局判定唔再用 wrapHistory 計擔正（resolveEnding410 段內零 wrapHistory）',
  (()=>{ const a = html.indexOf('function resolveEnding410(');
    const b = html.indexOf('/* 前夕抉擇選項生成', a);
    return a >= 0 && b > a && html.slice(a, b).indexOf('wrapHistory') < 0; })());
ok('G6 結局判定唔再讀舊計數器擔正欄（resolveEnding410 段內零 stats95.leadByMedium／stats95.tvLongLeads）',
  (()=>{ const a = html.indexOf('function resolveEnding410(');
    const b = html.indexOf('/* 前夕抉擇選項生成', a);
    const seg = html.slice(a, b);
    return seg.indexOf('stats95.leadByMedium') < 0 && seg.indexOf('stats95.tvLongLeads') < 0; })());

console.log('\ngig229 counts: ' + (fails === 0 ? 'ALL PASS' : fails + ' FAILED'));
if(fails) process.exit(1);
