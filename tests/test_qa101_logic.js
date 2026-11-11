// QA101 邏輯測試（v20a101 第 0 部分）：GH 金牌司儀入格——彭少祺好感 key 修復守門。
// 背景：end95PangProgress 舊版讀 s.stars.pang_siu_kei，但巧遇系統星 id 係 pang_siuki
//   （ENC79_STARS 定義、S.stars 實際寫入 key、v100 GH 回望 pf100 讀法都係 pang_siuki），
//   好感路（fav ≥45）喺真存檔永遠讀唔到值。本版修返讀 pang_siuki。
// 驗證：(1) 好感路：真 id fav 45 → true、fav 44 → false；
//       (2) 債權路（credit_enc84_pang_patron）同 C10 路不受影響、各自成立；
//       (3) 全判定：綜藝專長弧＋真 id 好感 50 → resolveEnding410 出 GH；
//           好感得 44 又冇其他兩路 → 唔入 GH（落下一格）。
// 反證：喺 v20a100 index 上行 → 好感路斷言 FAIL（舊 code 讀錯 key）。
// 用法：node tests/test_qa101_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');

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
var GIGS = [];

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

ok('harness: 函數載入', typeof end95PangProgress === 'function' && typeof resolveEnding410 === 'function');

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
function arc(fame, credit, over){
  const delta = credit - Math.round(fame * 0.5);
  return baseSave(Object.assign({ fame: fame, industryCreditDelta: delta }, over || {}));
}
function R(save){ S = save; return resolveEnding410(S); }

/* (1) 好感路：真星 id pang_siuki */
ok('好感路：pang_siuki fav 45 → end95PangProgress true',
  end95PangProgress(baseSave({ stars: { pang_siuki: { fav: 45 } } })) === true);
ok('好感路：pang_siuki fav 44 → false（門檻冇郁）',
  end95PangProgress(baseSave({ stars: { pang_siuki: { fav: 44 } } })) === false);
ok('好感路：冇 stars → false 唔 crash',
  end95PangProgress(baseSave({ stars: {} })) === false && end95PangProgress({}) === false);

/* (2) 債權路／C10 路各自成立（不受 key 修復影響） */
ok('債權路：持有 credit_enc84_pang_patron → true（冇好感都得）',
  end95PangProgress(baseSave({ mockCredits: [{ id: 'credit_enc84_pang_patron', amount: 1 }] })) === true);
ok('C10 路：主線 C10 done → true（冇好感冇債權都得）',
  end95PangProgress(baseSave({ story: { flags: {}, rel: {}, done: { C10: true }, choices: {} } })) === true);
ok('三路皆冇 → false',
  end95PangProgress(baseSave({})) === false);

/* (3) 全判定：綜藝專長弧行 GH（好感路） */
const ghStats = () => stats95({ total: 55,
  byMedium: { film: 8, tv: 10, music: 4, variety: 30, ad: 3 },
  leadByMedium: { variety: 1 }, genreIdentified: 20, genreComedy: 5, genreAction: 4 });
{
  const r = R(arc(100, 90, { careerStats95: ghStats(), stars: { pang_siuki: { fav: 50, tier: 3, metN: 9, lastMet: 500 } } }));
  ok('全判定：綜藝 55%＋pang_siuki 好感 50 → GH 金牌司儀', r.career === 'GH');
}
{
  const r = R(arc(100, 90, { careerStats95: ghStats(), stars: { pang_siuki: { fav: 44 } } }));
  ok('全判定：好感 44 又冇債權/C10 → 唔入 GH', r.career !== 'GH');
}
{
  const r = R(arc(100, 90, { careerStats95: ghStats(), mockCredits: [{ id: 'credit_enc84_pang_patron', amount: 1 }] }));
  ok('全判定：債權路單獨 → GH', r.career === 'GH');
}
{
  const r = R(arc(100, 90, { careerStats95: ghStats(), story: { flags: {}, rel: {}, done: { C10: true }, choices: {} } }));
  ok('全判定：C10 路單獨 → GH', r.career === 'GH');
}

/* ---------- CHK101 支票：大寫金額轉換＋金額保真 ---------- */
{
  let _chkOk = true;
  try{ eval(extractFn('function chk101AmountWords(')); }catch(e){ _chkOk = false; }
  ok('CHK101 函數在位', _chkOk);
  if(_chkOk){
    const T = (n, want) => ok('CHK101 大寫 ' + n + ' → ' + want, chk101AmountWords(n) === want);
    T(400, '肆佰元正'); T(1500, '壹仟伍佰元正'); T(10500, '壹萬零伍佰元正');
    T(10010, '壹萬零壹拾元正'); T(123456, '壹拾貳萬參仟肆佰伍拾陸元正'); T(100001, '壹拾萬零壹元正');
    T(350238, '參拾伍萬零貳佰參拾捌元正'); T(1000000, '壹佰萬元正');
    ok('CHK101 builder 帶金額屬性', /data-chk101/.test(extractFn('function chk101Html(')));
    ok('CHK101 底圖路徑存在於 builder', html.includes('assets/cheque101_base.jpg'));
    ok('CHK101 簽約金接入用 signPay 原數', html.includes('chk101Html({amount: signPay, memo: "簽約金"})'));
    ok('CHK101 殺青接入用 wrapPay91 原數', html.includes('chk101Html({ amount: wrapPay91,'));
  }
}

console.log('\nqa101 logic: ' + pass + ' pass / ' + fail + ' fail');
process.exit(fail ? 1 : 0);
