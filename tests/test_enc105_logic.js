// v20a105 ENC105 邏輯測試：巧遇資產組 D-2／D-3——
//   (1) 12 星逐個：enc79StandCandidates 第一候補＝企立檔（路徑逐字對版）＋實檔存在；
//       bust 做後備；候補尾＝入庫剪影檔＋內嵌 SVG 兜底（全失敗都唔會冇人）。
//   (2) enc79SceneSrc：每個巧遇可達地點（12 星 primary＋secondary 併集）回傳
//       LOC_SHEET_BG 逐地點新場景（逐字對版＋實檔存在），唔係 UI40 類別圖；
//       未有逐地點檔嘅地點先退 UI40 兜底。
// 反證：路徑逐字比對——改爛任何一個 stand／scene 路徑字串，呢度即 FAIL；
//       喺 v20a104 index 上行（冇 stand 候補、場景冇 LOC 來源）亦會 FAIL。
// 用法：node tests/test_enc105_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const root = path.dirname(path.resolve(htmlPath));
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS ' : 'FAIL ') + name); }
function extractFn(name){
  const i = html.indexOf('function ' + name + '(');
  if(i < 0) throw new Error('fn not found: ' + name);
  let depth = 0, j = html.indexOf('{', i);
  for(; j < html.length; j++){
    if(html[j] === '{') depth++;
    else if(html[j] === '}'){ depth--; if(depth === 0) break; }
  }
  return html.slice(i, j + 1);
}
function extractConstLine(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('const not found: ' + name);
  const j = html.indexOf('\n', i);
  return html.slice(i, j).replace(/;$/, '');
}
/* ---- 真資料：ENC79_STARS 名冊＋LOC_SHEET_BG（由 index 抽真身，唔用手抄表） ---- */
const starsBlock = html.slice(html.indexOf('const ENC79_STARS = ['), html.indexOf('];', html.indexOf('const ENC79_STARS = [')));
const STARS = [];
for(const mm of starsBlock.matchAll(/\{ id:"([^"]+)",\s*name:"([^"]+)",\s*primary:"([^"]+)",\s*secondary:"([^"]+)"/g)){
  STARS.push({ id: mm[1], name: mm[2], primary: mm[3], secondary: mm[4] });
}
ok('名冊抽到 12 星', STARS.length === 12);
const locBlock = html.slice(html.indexOf('const LOC_SHEET_BG = {'), html.indexOf('};', html.indexOf('const LOC_SHEET_BG = {')));
const LOC_SHEET_BG = {};
for(const mm of locBlock.matchAll(/(\w+):"([^"]+)"/g)) LOC_SHEET_BG[mm[1]] = mm[2];
ok('LOC_SHEET_BG 抽到 15 地點', Object.keys(LOC_SHEET_BG).length === 15);
/* ---- sandbox stubs（UI40 用哨兵值，方便分辨場景來源；silhouette 跟真函數 5 星範圍） ---- */
const UI40_SCENE = { cafe: 'UI40::cafe', agency: 'UI40::agency', studio: 'UI40::studio', startv: 'UI40::startv', recording: 'UI40::recording' };
const UI40_BG_BY_KEY = { bg_loc_cafe_cha: 'cafe', bg_loc_agency_ho: 'agency', bg_loc_film_lion: 'studio', bg_loc_film_cotton: 'studio', bg_loc_film_harbour: 'studio', bg_loc_tvb_longmen: 'startv', bg_loc_rec_hk: 'recording', bg_loc_rec_wanchai: 'recording', bg_loc_rec_star: 'recording' };
const UI40_STAND = { luk_baakyin: 'UI40::stand_luk_baakyin' };
const ERA_SIL5 = ['luk_baakyin', 'liu_bingxing', 'ngai_wingnaam', 'yip_manji', 'so_jiyan'];
function eraSilhouetteFarSrc(id){ return ERA_SIL5.indexOf(id) >= 0 ? 'assets/story/era_stars/' + id + '_silhouette_far.png?v=20a8' : ''; }
const api = new Function('UI40_SCENE', 'UI40_BG_BY_KEY', 'UI40_STAND', 'LOC_SHEET_BG', 'eraSilhouetteFarSrc',
  extractConstLine('ENC105_STAND_FALLBACK') + '\n' +
  extractConstLine('ENC105_STAND_SILHOUETTE') + '\n' +
  extractFn('enc79SceneSrc') + '\n' + extractFn('enc79StandCandidates') +
  '\nreturn { enc79SceneSrc, enc79StandCandidates, ENC105_STAND_FALLBACK, ENC105_STAND_SILHOUETTE };'
)(UI40_SCENE, UI40_BG_BY_KEY, UI40_STAND, LOC_SHEET_BG, eraSilhouetteFarSrc);
const fileOf = (url)=> path.join(root, String(url).split('?')[0]);
/* ---- (1) D-2：12 星候補 ---- */
for(const s of STARS){
  const cands = api.enc79StandCandidates(s.id);
  const expectStand = 'assets/story/era_stars/' + s.id + '_stand_default.png?v=20a105';
  ok(s.id + '（' + s.name + '）第一候補＝企立檔（逐字）', cands[0] === expectStand);
  ok(s.id + ' 企立實檔存在', fs.existsSync(fileOf(cands[0])));
  ok(s.id + ' bust 做後備（候補第 2 位起含 bust_default）', cands.slice(1).some(c => c.indexOf('_bust_default.png') >= 0));
  ok(s.id + ' 候補尾二＝入庫剪影檔＋實檔存在', cands[cands.length - 2] === api.ENC105_STAND_SILHOUETTE && fs.existsSync(fileOf(cands[cands.length - 2])));
  ok(s.id + ' 候補最尾＝內嵌 SVG 兜底（唔經網絡）', cands[cands.length - 1] === api.ENC105_STAND_FALLBACK && cands[cands.length - 1].indexOf('data:image/svg+xml') === 0);
  ok(s.id + ' 候補冇重複', new Set(cands).size === cands.length);
}
/* ---- (2) D-3：巧遇可達地點場景 ---- */
const reachLocs = [...new Set(STARS.flatMap(s => [s.primary, s.secondary]))];
ok('巧遇可達地點共 13 個', reachLocs.length === 13);
for(const loc of reachLocs){
  const got = api.enc79SceneSrc(loc);
  ok(loc + ' 場景＝LOC_SHEET_BG 逐地點檔（逐字）', got === LOC_SHEET_BG[loc]);
  ok(loc + ' 場景係逐地點新圖路徑（非 UI40 類別圖）', got.indexOf('assets/story/locs/bg_loc_' + loc + '.jpg') === 0 && got.indexOf('UI40::') !== 0);
  ok(loc + ' 場景實檔存在', fs.existsSync(fileOf(got)));
}
/* v20a118 LOCPANEL118：15 地點場景圖齊晒——醫院已有逐地點檔，唔再退 UI40 兜底
   （UI40 兜底分支留喺程式入面，畀將來冇圖嘅地點用；呢度改斷言跟新事實）。 */
ok('hospital 已有逐地點檔（＝LOC_SHEET_BG，不退 UI40）', api.enc79SceneSrc('hospital') === LOC_SHEET_BG['hospital']);
ok('hospital 場景實檔存在', fs.existsSync(fileOf(api.enc79SceneSrc('hospital'))));
console.log('---');
console.log('ENC105 LOGIC: ' + (fails.length ? fails.length + ' FAIL' : 'ALL PASS'));
process.exit(fails.length ? 1 : 0);
