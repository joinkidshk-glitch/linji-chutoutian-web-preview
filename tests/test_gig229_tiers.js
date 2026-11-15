// v20a229 B2 真五級引擎・邏輯測試
// 合約（AUDIT229 §3；SPEC §2.6 數值；DECISIONS.md D-1 引擎升級做真五級，唔用對應表）：
//   A fameFloor：臨記 0／初級 0／中級 16／高級 32／稀有 32；舊 初／中／高 照舊（0／16／32）
//   B chance 試鏡乘數：臨記 ×1.0／初級 ×1.0／中級 ×0.9／高級 ×0.82／稀有 ×0.82；
//     舊 初 ×1.0／中 ×0.9／高 ×0.82 照舊
//   C gigTierKey 五級各自一格（臨記 extra／初級 junior／中級 mid／高級 senior／稀有 rare），
//     臨記 ≠ 初級；舊 初→junior／中→mid／高→senior 照舊；gigTierCanon229 舊三級對位
//   D resolveRoleScale fallback 認齊五級；未認得嘅 tier 安全 fallback（唔 throw、唔靜默升格，跌返最低帶）
//   E gigBreachFee：高級／稀有行高分支（60%／下限 $1000）；臨記／初級／中級行一般分支（50%／下限 $500）
//   F gigDifficultyStars：高級／稀有 5 星、中級 4 星、臨記／初級按 hard 2／3 星
//   G aud91WaitDays：臨記／初級短工 1–2 日、高級／稀有 3–4 日、中級 2–3 日
//   H DUR90_DAILY 五級各一鍵（值按機械級對位），舊三級鍵留返
//   I 板面 tierOrder 五級：gigsForLocSeasonBoard 每級留一張＋按五級排序；舊三級按機械級對位照排
// 反證：v229 B1（舊三級）→ B1–B3／C1–C2／D／E／F／G／H／I 全部 FAIL（舊 code 唔識「中級」等新值，
//   臨記／初級撈埋 junior、板面 tierOrder 得三格）。
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
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
let fails = 0;
function ok(name, cond, extra){
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : ''));
  if(!cond) fails++;
}
function approx(a, b){ return Math.abs(a - b) < 1e-9; }

/* ---------- 靜態：五級表在位 ---------- */
ok('S0 GIG_TIER_ORDER229 五級次序 臨記／初級／中級／高級／稀有',
   html.includes('const GIG_TIER_ORDER229 = ["臨記","初級","中級","高級","稀有"]'));
ok('S1 板面 tierOrder 讀 GIG_TIER_ORDER229（唔係寫死三級）',
   (()=>{ const s = extractFn('gigsForLocSeasonBoard') || '';
     return s.includes('GIG_TIER_ORDER229') && s.includes('gigTierCanon229'); })());
ok('S2 DUR90_DAILY 五級鍵齊（臨記／初級／中級／高級／稀有）',
   ['"臨記"', '"初級"', '"中級"', '"高級"', '"稀有"'].every(k=>{
     const s = extractConst('DUR90_DAILY') || ''; return s.includes(k); }));
ok('S3 DUR90_DAILY 舊三級鍵留返（初／中／高）',
   (()=>{ const s = extractConst('DUR90_DAILY') || '';
     return s.includes('"初"') && s.includes('"中"') && s.includes('"高"'); })());

/* ---------- sandbox：核心五級函數 ---------- */
const STUBS_SRC = `
  var START = { y:1990, m:1, d:1 };
  var S = null;
  var GIGS = [];
`;
const CONSTS = ['ROLE_SCALE_BAND', 'DUR90_DAILY', 'GIG_TIER_ORDER229'];
const FNS = ['clamp', 'R', 'fameFloor', 'chance', 'gigTierCanon229', 'gigTierKey',
  'resolveRoleScale', 'shootBandFor', 'gigPayExact', 'gigBreachFee', 'gigDifficultyStars',
  'aud91WaitDays'];
const WORLD_SRC = CONSTS.map(c=>{
  const s = extractConst(c); return s ? s.replace('const '+c, 'var '+c) : 'var '+c+' = undefined;';
}).join('\n') + '\n' + FNS.map(f=>extractFn(f) || '').join('\n');
const W = new Function(STUBS_SRC + WORLD_SRC + `
; return { fameFloor, chance, gigTierCanon229, gigTierKey, resolveRoleScale, gigPayExact,
  gigBreachFee, gigDifficultyStars, aud91WaitDays, DUR90_DAILY,
  setS:(s)=>{S=s;}, getS:()=>S };`)();

/* ---------- A fameFloor ---------- */
const FAME_EXPECT = { '臨記':0, '初級':0, '中級':16, '高級':32, '稀有':32, '初':0, '中':16, '高':32 };
for(const [tier, want] of Object.entries(FAME_EXPECT)){
  ok('A fameFloor ' + tier + ' = ' + want, W.fameFloor({ tier }) === want,
     'got=' + W.fameFloor({ tier }));
}
ok('A9 fameFloor 缺 tier 預設 0', W.fameFloor({}) === 0);

/* ---------- B chance 乘數 ---------- */
const MAXED = { acting:999, stage:999, vocal:999, looks:999, charm:999, iq:999, stamina:100,
  fame:999, popularity:999, stress:0, money:999999, dayIndex:0, flags:{}, shoots:[], booked:[],
  enrolled:{}, board:{}, known:{}, npcs:{ director:0, agent:0, colleague:0 } };
function chanceOf(tier, req, sOverride){
  const s = JSON.parse(JSON.stringify(MAXED));
  Object.assign(s, sOverride || {});
  W.setS(s);
  return W.chance({ tier, req: req || {}, hard: 0.4 });
}
// req {}：p = 0.05 + 1×0.48 − 0.4×0.28 = 0.418（滿 ratio、無 keys、無 npc／體能／壓力加成）
const BASE_P = 0.418;
for(const [tier, mult] of [['臨記',1.0],['初級',1.0],['中級',0.9],['高級',0.82],['稀有',0.82],['初',1.0],['中',0.9],['高',0.82]]){
  ok('B chance ' + tier + ' ×' + mult, approx(chanceOf(tier), BASE_P * mult),
     'got=' + chanceOf(tier) + ' want=' + (BASE_P * mult));
}
// 有 req 嗰陣乘數一樣生效：req 全達標（演技 18＝要求 18，ratio 1）→ p = 0.418 + 0.10 = 0.518
ok('B9 chance 中級（有 req 全達標）= 0.518×0.9', approx(chanceOf('中級', { acting:18 }, { acting:18 }), 0.518 * 0.9),
   'got=' + chanceOf('中級', { acting:18 }, { acting:18 }));
ok('B10 chance 臨記（有 req 全達標）= 0.518×1.0', approx(chanceOf('臨記', { acting:18 }, { acting:18 }), 0.518),
   'got=' + chanceOf('臨記', { acting:18 }, { acting:18 }));

/* ---------- C gigTierKey／gigTierCanon229 ---------- */
const KEY_EXPECT = { '臨記':'extra', '初級':'junior', '中級':'mid', '高級':'senior', '稀有':'rare',
  '初':'junior', '中':'mid', '高':'senior' };
for(const [tier, want] of Object.entries(KEY_EXPECT)){
  ok('C gigTierKey ' + tier + ' = ' + want, W.gigTierKey({ tier }) === want,
     'got=' + W.gigTierKey({ tier }));
}
ok('C9 gigTierKey 臨記 ≠ 初級（五級可區分）',
   W.gigTierKey({ tier:'臨記' }) !== W.gigTierKey({ tier:'初級' }),
   W.gigTierKey({ tier:'臨記' }) + ' vs ' + W.gigTierKey({ tier:'初級' }));
ok('C10 gigTierKey 五級 key 全部唔同',
   new Set(['臨記','初級','中級','高級','稀有'].map(t=>W.gigTierKey({ tier:t }))).size === 5);
ok('C11 gigTierKey 缺 tier 預設 junior', W.gigTierKey({}) === 'junior');
const CANON_EXPECT = { '臨記':'臨記', '初級':'初級', '中級':'中級', '高級':'高級', '稀有':'稀有',
  '初':'初級', '中':'中級', '高':'高級' };
for(const [tier, want] of Object.entries(CANON_EXPECT)){
  ok('C12 gigTierCanon229 ' + tier + ' → ' + want, W.gigTierCanon229(tier) === want,
     'got=' + W.gigTierCanon229(tier));
}

/* ---------- D resolveRoleScale fallback ---------- */
const SCALE_CASES = [
  [{ type:'電影', tier:'高級' }, 'film_lead_big'],
  [{ type:'電影', tier:'稀有' }, 'film_lead_big'],
  [{ type:'電影', tier:'中級' }, 'film_support_main'],
  [{ type:'電影', tier:'臨記' }, 'film_support_small'],
  [{ type:'電影', tier:'初級' }, 'film_support_small'],
  [{ type:'電視劇', tier:'高級' }, 'tv_lead_long'],
  [{ type:'電視劇', tier:'稀有' }, 'tv_lead_long'],
  [{ type:'電視劇', tier:'中級' }, 'tv_support_main'],
  [{ type:'電視劇', tier:'臨記' }, 'tv_cameo_short'],
  [{ type:'綜藝', tier:'稀有' }, 'variety_special'],
  [{ type:'綜藝', tier:'高級' }, 'variety_special'],
  [{ type:'綜藝', tier:'中級' }, 'variety_ep'],
  [{ type:'綜藝', tier:'初級' }, 'variety_ep'],
  [{ type:'唱片通告', tier:'中級', title:'《歌》' }, 'rec_album'],
  // 舊三級照舊
  [{ type:'電影', tier:'高' }, 'film_lead_big'],
  [{ type:'電影', tier:'中' }, 'film_support_main'],
  [{ type:'電視劇', tier:'高' }, 'tv_lead_long'],
];
for(const [gig, want] of SCALE_CASES){
  ok('D resolveRoleScale ' + gig.type + '／' + gig.tier + ' → ' + want,
     W.resolveRoleScale(gig) === want, 'got=' + W.resolveRoleScale(gig));
}
// 安全 fallback：未認得嘅 tier 唔 throw、唔靜默升格，跌返最低帶
for(const gig of [{ type:'電影', tier:'唔知咩級' }, { type:'電視劇', tier:'' }, { type:'綜藝' }]){
  let got = null, threw = false;
  try{ got = W.resolveRoleScale(gig); }catch(_e){ threw = true; }
  const want = gig.type === '電影' ? 'film_support_small' : gig.type === '電視劇' ? 'tv_cameo_short' : 'variety_ep';
  ok('D9 安全 fallback ' + gig.type + '／' + JSON.stringify(gig.tier) + ' → ' + want + '（唔 throw）',
     !threw && got === want, 'got=' + got + ' threw=' + threw);
}
// 有 roleScale 嗰陣直接回傳，唔行 fallback
ok('D10 有 roleScale 直接回傳（唔受 tier 影響）',
   W.resolveRoleScale({ type:'電影', tier:'臨記', roleScale:'film_lead_big' }) === 'film_lead_big');

/* ---------- E gigBreachFee ---------- */
function breachOf(tier){
  return W.gigBreachFee({ tier, pay:[10000, 12000] }); // payExact 中位數 11000
}
for(const [tier, want] of [['臨記',5500],['初級',5500],['中級',5500],['高級',6600],['稀有',6600],['初',5500],['中',5500],['高',6600]]){
  ok('E gigBreachFee ' + tier + ' = $' + want, breachOf(tier) === want, 'got=' + breachOf(tier));
}
// 下限：總額 $1500 嗰陣 60%（$900）唔夠下限 → 高分支 $1000（min(fee,P) 唔會再壓低佢）；
// 總額 $800 嗰陣 50%（$400）唔夠下限 → 一般分支 $500。
ok('E9 gigBreachFee 高級細額下限 $1000', W.gigBreachFee({ tier:'高級', pay:[1400, 1600] }) === 1000,
   'got=' + W.gigBreachFee({ tier:'高級', pay:[1400, 1600] }));
ok('E10 gigBreachFee 臨記細額下限 $500', W.gigBreachFee({ tier:'臨記', pay:[700, 900] }) === 500,
   'got=' + W.gigBreachFee({ tier:'臨記', pay:[700, 900] }));

/* ---------- F gigDifficultyStars ---------- */
for(const [gig, want] of [
    [{ tier:'高級' }, 5], [{ tier:'稀有' }, 5], [{ tier:'中級' }, 4],
    [{ tier:'臨記', hard:0.3 }, 2], [{ tier:'臨記', hard:0.5 }, 3],
    [{ tier:'初級', hard:0.3 }, 2], [{ tier:'初級', hard:0.65 }, 3],
    [{ tier:'高' }, 5], [{ tier:'中' }, 4], [{ tier:'初', hard:0.3 }, 2]]){
  ok('F gigDifficultyStars ' + gig.tier + ' = ' + want + ' 星',
     W.gigDifficultyStars(gig).n === want, 'got=' + W.gigDifficultyStars(gig).n);
}

/* ---------- G aud91WaitDays ---------- */
function waitRange(tier, days){
  const seen = new Set();
  for(let i=0; i<40; i++) seen.add(W.aud91WaitDays({ tier }, days));
  return seen;
}
function rangeOk(seen, lo, hi){
  if(!seen.size) return false;
  for(const v of seen){ if(v < lo || v > hi) return false; }
  return true;
}
ok('G aud91WaitDays 臨記短工 1–2 日', rangeOk(waitRange('臨記', 1), 1, 2),
   [...waitRange('臨記', 1)].join(','));
ok('G2 aud91WaitDays 初級短工 1–2 日', rangeOk(waitRange('初級', 2), 1, 2));
ok('G3 aud91WaitDays 中級 2–3 日', rangeOk(waitRange('中級', 5), 2, 3));
ok('G4 aud91WaitDays 高級 3–4 日', rangeOk(waitRange('高級', 5), 3, 4));
ok('G5 aud91WaitDays 稀有 3–4 日', rangeOk(waitRange('稀有', 5), 3, 4));
ok('G6 aud91WaitDays 舊 高 3–4 日', rangeOk(waitRange('高', 5), 3, 4));
ok('G7 aud91WaitDays 舊 初短工 1–2 日', rangeOk(waitRange('初', 2), 1, 2));

/* ---------- H DUR90_DAILY 值 ---------- */
const D = W.DUR90_DAILY;
ok('H DUR90_DAILY 臨記／初級＝舊 初帶', JSON.stringify(D['臨記']) === JSON.stringify(D['初']) &&
   JSON.stringify(D['初級']) === JSON.stringify(D['初']));
ok('H2 DUR90_DAILY 中級＝舊 中帶', JSON.stringify(D['中級']) === JSON.stringify(D['中']));
ok('H3 DUR90_DAILY 高級／稀有＝舊 高帶', JSON.stringify(D['高級']) === JSON.stringify(D['高']) &&
   JSON.stringify(D['稀有']) === JSON.stringify(D['高']));

/* ---------- I 板面 tierOrder（live） ---------- */
const BOARD_FNS = ['clamp', 'seasonRank', 'calendarSeason', 'boardPriorityRank', 'boardSortCompare',
  'isGigWrapped', 'gigActiveShoot', 'isGigInProduction', 'isGigConsumed',
  'gigTierCanon229', 'gigsForLocSeasonBoard'];
const BOARD_SRC = CONSTS.filter(c=>c !== 'DUR90_DAILY').map(c=>{
  const s = extractConst(c); return s ? s.replace('const '+c, 'var '+c) : 'var '+c+' = undefined;';
}).join('\n') + '\n' + BOARD_FNS.map(f=>extractFn(f) || '').join('\n');
const WB = new Function(`
  var START = { y:1990, m:1, d:1 };
  var S = null;
  var GIGS = [];
` + BOARD_SRC + `
; return { board: gigsForLocSeasonBoard, season: calendarSeason,
  setS:(s)=>{S=s;}, setGIGS:(g)=>{GIGS=g;} };`)();
function mkGig(id, tier){
  return { id, tier, type:'電視劇', loc:'rec_hk', year:1990, season:'春',
    title:'《測》' + id, roleLabel:'配角', roleScale:'tv_cameo_short', req:{}, pay:[1000, 2000],
    boardPriority:'normal' };
}
const BASE_S = { dayIndex:60, fame:5, popularity:3, stress:12, money:12000,
  flags:{}, shoots:[], booked:[], pendingAud:[], enrolled:{}, board:{}, known:{} };
WB.setS(JSON.parse(JSON.stringify(BASE_S)));
ok('I0 板面沙盒季節係 春（dayIndex 60）', WB.season() === '春', 'got=' + WB.season());
WB.setGIGS(['臨記','初級','中級','高級','稀有'].map((t, i)=>mkGig('g229t_' + i, t)));
const shownNew = WB.board('rec_hk', '春').map(g=>g.tier);
ok('I1 板面五級齊晒＋按 臨記→初級→中級→高級→稀有 排序',
   JSON.stringify(shownNew) === JSON.stringify(['臨記','初級','中級','高級','稀有']),
   shownNew.join(','));
WB.setGIGS(['初','中','高'].map((t, i)=>mkGig('g229o_' + i, t)));
const shownOld = WB.board('rec_hk', '春').map(g=>g.tier);
ok('I2 板面舊三級按機械級對位照排（初→初級位／中→中級位／高→高級位）',
   JSON.stringify(shownOld) === JSON.stringify(['初','中','高']), shownOld.join(','));
// 臨記 vs 初級可區分：兩張同地同季，只係 tier 唔同，板面唔會撈埋同一格
WB.setGIGS([mkGig('g229l_1', '臨記'), mkGig('g229l_2', '初級')]);
const shownPair = WB.board('rec_hk', '春').map(g=>g.tier);
ok('I3 臨記 vs 初級同板出現、臨記行先', JSON.stringify(shownPair) === JSON.stringify(['臨記','初級']),
   shownPair.join(','));

console.log(fails ? ('FAILURES: ' + fails) : 'ALL PASS');
process.exit(fails ? 1 : 0);
