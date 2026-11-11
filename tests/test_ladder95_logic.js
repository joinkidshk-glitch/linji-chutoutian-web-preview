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
  'function endingFlag410','function endingDual410','function endingNegTagCount410','function endingBackstageTagCount410','function endingFavor410',
  'function endingRomance410','function endingE2Eligible410','function endingE3Eligible410','function endingBackstageClose410',
  'function end95GenreOf','function end95IsLead','function end95ClassifyWrap','function end95EmptyStats','function end95StatsAddOne',
  'function end95DeriveStats','function careerStats95Of','function end95AddWrap','function end95Awards','function end95EverHeldCredit',
  'function end95StoryDone','function end95ChainsDone','function end95PangProgress','function end95E3Variant','function end95BuildGaps',
  'function resolveEnding410','function endingEveOptions410','function endingEsc410','function endingCareerScene410','function endingSummaryHtml410'];
const CONST_LIST = ['ENDING410_CAREER_NAMES','ENDING410_T','ENDING_NEG_TAGS410','ENDING410_BACKSTAGE_KEYS','ENDING410_EXODUS_NAME_FALLBACK',
  'ENDING410_NPC_NAMES','ENDING95_T','END95_TYPE_MEDIUM','END95_LEAD_SCALES','END95_STRONG_LEAD','END95_GENRE_TYPE_NAMES',
  'END95_COMEDY_G','END95_ACTION_G','END95_COMEDY_KW','END95_ACTION_KW','ENDING410_ADJ_RUMOR'];
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
  return baseSave(Object.assign({ fame: fame, industryCreditDelta: delta }, over || {}));
}
function R(save){ S = save; return resolveEnding410(S); }
function canon(o){
  if(Array.isArray(o)) return '[' + o.map(canon).join(',') + ']';
  if(o && typeof o === 'object') return '{' + Object.keys(o).sort().map(k => JSON.stringify(k) + ':' + canon(o[k])).join(',') + '}';
  return JSON.stringify(o);
}

/* ============ 校準弧 1：正常強弧（fullarc3 正常弧實測錨）→ SS 一線巨星 ============ */
{
  const st = arc(181, 210, {
    careerStats95: stats95({ total: 95,
      byMedium: { film: 30, tv: 28, music: 20, variety: 10, ad: 7 },
      leadByMedium: { film: 2, tv: 2, music: 1 },
      tvLongLeads: 1, genreIdentified: 34, genreComedy: 10, genreAction: 8 }),
    awardsLog: [
      { medium: 'film', categories: [{ id: 'n', outcome: 'nominated', repTitle: '甲片' }] },
      { medium: 'tv', categories: [{ id: 'n', outcome: 'nominated', repTitle: '乙劇' }] },
    ],
  });
  const r = R(st);
  ok('弧1 正常強弧：雙軌 391（fame 181／credit 210）', r.snapshot.dual === 391 && r.snapshot.fame === 181 && r.snapshot.credit === 210);
  ok('弧1：冇獎＋冇鏈 → 落 SS 一線巨星（唔自然上 E1）', r.career === 'SS' && r.ladder95.hasWin === false && r.ladder95.chains.length === 0);
  ok('弧1：差邊瓣第一句講差個獎', /獎/.test(r.gaps95[0] || ''));
}

/* ============ 校準弧 2：近乎完美弧 → E1 天王接班 ============ */
{
  const st = arc(190, 215, {
    careerStats95: stats95({ total: 100,
      byMedium: { film: 34, tv: 26, music: 22, variety: 10, ad: 8 },
      leadByMedium: { film: 3, tv: 2, music: 1 },
      tvLongLeads: 2, genreIdentified: 36, genreComedy: 9, genreAction: 9 }),
    awardsLog: [{ medium: 'film', categories: [{ id: 'w', outcome: 'won', repTitle: '丙片' }] }],
    wf3: { liaoHarvestDone: 1 },
  });
  const r = R(st);
  ok('弧2 近乎完美弧：雙軌 405 → E1 天王接班', r.career === 'E1' && r.snapshot.dual === 405);
  ok('弧2：質性閘三件齊（獎／兩媒介擔正／鏈 B）', r.ladder95.hasWin === true && r.ladder95.leadMedia.length === 3 && r.ladder95.chains.join() === 'B');
  ok('弧2：E1 差邊瓣＝冇差嗰句', r.gaps95.length === 1 && /冇差/.test(r.gaps95[0]));
}

/* E1 邊界：雙軌 350＋全閘 → E1；349＋全閘 → SS＋差距句 */
{
  const mk = (credit) => arc(170, credit, {
    careerStats95: stats95({ total: 90,
      byMedium: { film: 30, tv: 26, music: 20, variety: 8, ad: 6 },
      leadByMedium: { film: 3, tv: 2 },
      tvLongLeads: 2, genreIdentified: 30, genreComedy: 8, genreAction: 8 }),
    awardsLog: [{ medium: 'film', categories: [{ id: 'w', outcome: 'won', repTitle: '丙片' }] }],
    wf3: { liaoHarvestDone: 1 },
  });
  const r350 = R(mk(180));
  ok('E1 邊界：雙軌 350＋全閘 → E1', r350.career === 'E1' && r350.snapshot.dual === 350);
  const r349 = R(mk(179));
  ok('E1 邊界：雙軌 349＋全閘 → SS，差邊瓣寫差 1', r349.career === 'SS' && r349.gaps95.some(g => /差 1 /.test(g)));
  const rNoChain = R(arc(190, 215, {
    careerStats95: stats95({ total: 100,
      byMedium: { film: 34, tv: 26, music: 22, variety: 10, ad: 8 },
      leadByMedium: { film: 3, tv: 2, music: 1 },
      tvLongLeads: 2, genreIdentified: 36, genreComedy: 9, genreAction: 9 }),
    awardsLog: [{ medium: 'film', categories: [{ id: 'w', outcome: 'won', repTitle: '丙片' }] }],
  }));
  ok('E1 閘拆解：雙軌 405＋獎＋擔正、鏈 0 → SS，差邊瓣講主線未行到尾', rNoChain.career === 'SS' && rNoChain.gaps95.some(g => /主線/.test(g)));
  const rOneLead = R(arc(190, 215, {
    careerStats95: stats95({ total: 100,
      byMedium: { film: 60, tv: 15, music: 12, variety: 7, ad: 6 },
      leadByMedium: { film: 4 },
      tvLongLeads: 0, genreIdentified: 36, genreComedy: 9, genreAction: 9 }),
    awardsLog: [{ medium: 'film', categories: [{ id: 'w', outcome: 'won', repTitle: '丙片' }] }],
    wf3: { liaoHarvestDone: 1 },
  }));
  /* 雙軌 405 本身已過 SS 線（SS 排喺專長格之前，係「未齊 E1 質性閘」嘅頂格）→ 落 SS 而唔係 FK；
     差邊瓣要講明差擔正媒介嗰瓣。 */
  ok('E1 閘拆解：只得一種媒介擔正 → 唔上 E1（落 SS），差邊瓣講擔正', rOneLead.career === 'SS' && rOneLead.gaps95.some(g => /擔正/.test(g)));
}

/* ============ 校準弧 3：電影專長弧 → FK 影壇天王 ============ */
{
  const r = R(arc(120, 115, {
    careerStats95: stats95({ total: 70,
      byMedium: { film: 42, tv: 10, music: 8, variety: 5, ad: 5 },
      leadByMedium: { film: 3 },
      genreIdentified: 26, genreComedy: 6, genreAction: 7 }),
  }));
  ok('弧3 電影專長：雙軌 235、電影佔比 60%、擔正 3 → FK', r.career === 'FK' && r.snapshot.dual === 235);
}
{
  const r = R(arc(110, 120, {
    careerStats95: stats95({ total: 72,
      byMedium: { film: 12, tv: 40, music: 10, variety: 6, ad: 4 },
      leadByMedium: { tv: 2 }, tvLongLeads: 2, genreIdentified: 30, genreComedy: 8, genreAction: 5 }),
  }));
  ok('分科：電視專長（佔比 55%＋長劇擔正 2）→ TK 電視天王', r.career === 'TK');
}
{
  const r = R(arc(130, 100, {
    careerStats95: stats95({ total: 65,
      byMedium: { film: 10, tv: 9, music: 36, variety: 6, ad: 4 },
      leadByMedium: { music: 2 }, genreIdentified: 28, genreComedy: 6, genreAction: 4 }),
    awardsLog: [{ medium: 'music', categories: [{ id: 'n', outcome: 'nominated', repTitle: '某碟' }] }],
  }));
  ok('分科：唱片專長（佔比 55%＋音樂提名）→ SK 歌王', r.career === 'SK' && r.ladder95.musicHonor === true);
}
{
  const r = R(arc(100, 90, {
    careerStats95: stats95({ total: 55,
      byMedium: { film: 8, tv: 10, music: 4, variety: 30, ad: 3 },
      leadByMedium: { variety: 1 }, genreIdentified: 20, genreComedy: 5, genreAction: 3 }),
    stars: { pang_siuki: { fav: 50, tier: 2, metN: 9, lastMet: 500 } },
  }));
  ok('分科：綜藝專長（佔比 55%＋彭少祺好感 50）→ GH 金牌司儀', r.career === 'GH');
}
{
  const r = R(arc(105, 95, {
    careerStats95: stats95({ total: 50,
      byMedium: { film: 15, tv: 12, music: 10, variety: 8, ad: 5 },
      leadByMedium: { film: 1 }, genreIdentified: 30, genreComedy: 17, genreAction: 4 }),
  }));
  ok('分科：喜劇佔比 57%（可辨識 30）＋信用 95 → CK 喜劇泰斗', r.career === 'CK');
}
{
  const r = R(arc(108, 92, {
    careerStats95: stats95({ total: 60,
      byMedium: { film: 20, tv: 15, music: 10, variety: 6, ad: 9 },
      leadByMedium: { film: 1 }, genreIdentified: 28, genreComedy: 3, genreAction: 15 }),
    trainCount: { train_stamina: 10 },
  }));
  ok('分科：動作佔比 54%（可辨識 28）＋武師班 10 堂 → AK 動作巨星', r.career === 'AK');
}
{
  const r = R(arc(105, 95, {
    careerStats95: stats95({ total: 50,
      byMedium: { film: 15, tv: 12, music: 10, variety: 8, ad: 5 },
      leadByMedium: { film: 1 }, genreIdentified: 3, genreComedy: 3, genreAction: 0 }),
  }));
  ok('片種樣本守門：可辨識得 3（喜劇 3/3）唔入 CK → 落 E2', r.career === 'E2');
}

/* ============ ID／CR 帶位弧 ============ */
{
  const r = R(arc(75, 45, {
    careerStats95: stats95({ total: 30,
      byMedium: { film: 8, tv: 7, music: 8, variety: 4, ad: 3 },
      leadByMedium: { film: 1 }, genreIdentified: 10, genreComedy: 3, genreAction: 2 }),
  }));
  ok('帶位：聲望 75／信用 45（30–54 帶）→ ID 人氣偶像', r.career === 'ID');
}
{
  const r = R(arc(45, 70, {
    careerStats95: stats95({ total: 25,
      byMedium: { film: 8, tv: 8, music: 4, variety: 3, ad: 2 },
      leadByMedium: { tv: 1 }, genreIdentified: 9, genreComedy: 2, genreAction: 2 }),
  }));
  ok('帶位：信用 70／聲望 45（35–59 帶）→ CR 實力派演員', r.career === 'CR');
}

/* ============ E3 三變體（只分呈現） ============ */
{
  const base = { npcs: { agent: 0, director: 65, colleague: 0, reporter: 0, stylist: 0, rival: 0 } };
  const rDir = R(arc(30, 50, Object.assign({}, base, {
    careerStats95: stats95({ total: 30, byMedium: { film: 20, tv: 5, music: 2, variety: 2, ad: 1 }, backstageWorks: 4 }) })));
  ok('E3 變體：電影幕後多 → 大導演', rDir.career === 'E3' && rDir.careerVariant === '大導演' && rDir.title.indexOf('大導演') === 0);
  const rProd = R(arc(30, 50, Object.assign({}, base, {
    careerStats95: stats95({ total: 30, byMedium: { film: 3, tv: 20, music: 2, variety: 3, ad: 2 }, backstageWorks: 4 }) })));
  ok('E3 變體：電視幕後多 → 金牌監製', rProd.career === 'E3' && rProd.careerVariant === '金牌監製');
  const rBoss = R(arc(30, 50, Object.assign({}, base, {
    careerStats95: stats95({ total: 30, byMedium: { film: 20, tv: 5, music: 2, variety: 2, ad: 1 }, backstageWorks: 4 }),
    /* 人情總量口徑＝endingFavor410 total：settled 4＋未用 favor/debt 債權 2（mockCredits）＝6 */
    favorLedger: { settled: 4, credits: 0, exodus: [], counted: {} },
    mockCredits: [{ id: 'favor_x1', amount: 1 }, { id: 'debt_y1', amount: 1 }] })));
  ok('E3 變體：人情總量 6（≥5）→ 製片老闆（壓過媒介構成）', rBoss.career === 'E3' && rBoss.careerVariant === '製片老闆');
  S = arc(30, 50, Object.assign({}, base, {
    careerStats95: stats95({ total: 30, byMedium: { film: 20, tv: 5, music: 2, variety: 2, ad: 1 }, backstageWorks: 4 }) }));
  const scene = endingCareerScene410({ career: 'E3', careerVariant: '大導演', adjPicked: {} });
  ok('E3 變體呈現：大導演場景有「偉導」字眼', scene.includes('偉導'));
}

/* ============ 計數器：衍生／種子／累加 ============ */
{
  const hist = [
    { gigId: 'g_film_lead', totalDays: 25 }, { gigId: 'g_film_com', totalDays: 5 },
    { gigId: 'g_tv_long', totalDays: 30 }, { gigId: 'g_rec_helper', totalDays: 3 },
    { gigId: 'g_ad_extra', totalDays: 1 }, { gigId: 'g_stunt', totalDays: 2 },
    { gigId: 'g_tv_crew', totalDays: 4 },
  ];
  const st = baseSave({ wrapHistory: hist.slice() });
  const cs = careerStats95Of(st);
  ok('衍生：總數 7、媒介 film 3／tv 2／music 1／ad 1', cs.total === 7 && cs.byMedium.film === 3 && cs.byMedium.tv === 2 && cs.byMedium.music === 1 && cs.byMedium.ad === 1);
  ok('衍生：擔正 film 1／tv 1（替身唔計、場記唔計）＋長劇擔正 1', cs.leadByMedium.film === 1 && cs.leadByMedium.tv === 1 && cs.tvLongLeads === 1);
  ok('衍生：片種可辨識 6（喜劇 1／動作 2／其餘 other）', cs.genreIdentified === 6 && cs.genreComedy === 1 && cs.genreAction === 2);
  ok('衍生：幕後作品 1（場記）', cs.backstageWorks === 1);
  end95AddWrap(st, GIGS[1], { totalDays: 5 });
  ok('addWrap：首次以衍生做種子再加一單，唔雙計（total 8、喜劇 2）', st.careerStats95.total === 8 && st.careerStats95.genreComedy === 2);
  end95AddWrap(st, GIGS[2], { totalDays: 30 });
  ok('addWrap：再加長劇（total 9、tv 擔正 2、長劇 2）', st.careerStats95.total === 9 && st.careerStats95.leadByMedium.tv === 2 && st.careerStats95.tvLongLeads === 2);
  const noHist = baseSave({});
  let threw95 = false;
  try { end95AddWrap(noHist, null, null); } catch (e) { threw95 = true; }
  ok('addWrap：空 gig 唔 throw；唯讀衍生照出零計數', !threw95 && careerStats95Of(noHist).total === 0);
}
{
  const st = arc(120, 115, { wrapHistory: [
    { gigId: 'g_film_lead', totalDays: 25 }, { gigId: 'g_film_com', totalDays: 5 },
    { gigId: 'g_tv_long', totalDays: 30 }, { gigId: 'g_rec_helper', totalDays: 3 },
    { gigId: 'g_ad_extra', totalDays: 1 }, { gigId: 'g_stunt', totalDays: 2 },
    { gigId: 'g_tv_crew', totalDays: 4 }] });
  let r = null, threw = false;
  try { r = R(st); } catch (e) { threw = true; }
  ok('舊檔（冇 careerStats95、得履歷 7 條）resolve 唔 crash 且用衍生數', !threw && r && r.ladder95.total === 7 && r.ladder95.leadMedia.length === 2);
}

/* ============ 質性件單元 ============ */
{
  const nom = baseSave({ awardsLog: [{ medium: 'music', categories: [{ outcome: 'nominated' }] }] });
  ok('end95Awards：提名唔係 win；音樂提名＝musicHonor', end95Awards(nom).hasWin === false && end95Awards(nom).musicHonor === true);
  const winTv = baseSave({ awardsLog: [{ medium: 'tv', categories: [{ outcome: 'won' }] }] });
  ok('end95Awards：電視 win＝hasWin、唔係 musicHonor', end95Awards(winTv).hasWin === true && end95Awards(winTv).musicHonor === false);
  ok('end95ChainsDone：六鏈標記逐一認到',
    end95ChainsDone(baseSave({ wf3: { luSettled: 1 } })).includes('A') &&
    end95ChainsDone(baseSave({ wf3: { liaoHarvestDone: 1 } })).includes('B') &&
    end95ChainsDone(baseSave({ story: { flags: {}, rel: {}, done: { C15: true }, choices: {} }, intelFlags: { intel_mak_injury: true } })).includes('C') &&
    end95ChainsDone(baseSave({ wf3: { yipCreditDone: 1 } })).includes('D') &&
    end95ChainsDone(baseSave({ story: { flags: { flag_gao_ending_stay: true }, rel: {}, done: {}, choices: {} } })).includes('E') &&
    end95ChainsDone(baseSave({ story: { flags: { flag_stay_mind: true }, rel: {}, done: {}, choices: {} } })).includes('F') &&
    end95ChainsDone(baseSave({})).length === 0);
  ok('end95PangProgress：好感路／債權路／C10 路任一通',
    end95PangProgress(baseSave({ stars: { pang_siuki: { fav: 45 } } })) === true &&
    end95PangProgress(baseSave({ mockCredits: [{ id: 'credit_enc84_pang_patron', amount: 1 }] })) === true &&
    end95PangProgress(baseSave({ story: { flags: {}, rel: {}, done: { C10: true }, choices: {} } })) === true &&
    end95PangProgress(baseSave({ stars: { pang_siuki: { fav: 44 } } })) === false);
}

/* ============ 純函數不變性＋總結頁呈現 ============ */
{
  const st = arc(181, 210, {
    careerStats95: stats95({ total: 95,
      byMedium: { film: 30, tv: 28, music: 20, variety: 10, ad: 7 },
      leadByMedium: { film: 2, tv: 2, music: 1 },
      tvLongLeads: 1, genreIdentified: 34, genreComedy: 10, genreAction: 8 }),
  });
  const before = canon(st);
  const r = R(st);
  ok('resolve 純函數：狀態逐字不變（計數器唔俾 resolve 寫）', canon(st) === before);
  S = st;
  S.ending410 = { career: 'SS', title: r.title, romanceAxis: 'none', exodusAxis: 'stay',
    snapshot: r.snapshot, gaps95: r.gaps95, careerVariant: null };
  const sum = endingSummaryHtml410(S);
  ok('總結頁：SS 稱號卡＋差邊瓣句在場', sum.includes('一線巨星') && sum.includes('回望嗰一格'));
  const keys = endingEveOptions410(S, resolveEnding410(S)).map(c => c.key);
  ok('前夕：SS 冇相鄰分流選項（只有 natural／quit／leave 系）', !keys.includes('to_backstage') && !keys.includes('to_support') && keys.includes('natural'));
}

console.log('\nladder95 logic: ' + pass + ' passed, ' + fail + ' failed');
if(fail) process.exit(1);
