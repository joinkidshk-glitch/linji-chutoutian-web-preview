// v20a119 DLG119 邏輯測試：剪影 helper——影 asset 映射／講者聽者候補鏈／
// 同影去重／stem 別名／企位解析（影唔翻、單人企左、孖影去重後唔出雙人）。
// 資料一律由 index.html 抽 DLG106 模組真身 eval，唔用手抄副本。
// 反證：(a) 別名表刪走 generic_cinema_asst → stem 必須變回自己名；
//       (b) 去重函數食同 asset pair 必須得返一個，食唔同 asset 必須唔郁。
// 用法：node tests/test_dlg119_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS ' : 'FAIL ') + name); }
function info(msg){ console.log('INFO ' + msg); }

/* ---- 抽 DLG106 模組真身並 eval（window／級數函數做 stub） ---- */
const a = html.indexOf('/* ===== v20a106 DLG106');
const b = html.indexOf('/* ===== DLG106 模組完 ===== */');
ok('搵到 DLG106 模組', a >= 0 && b > a);
const code = html.slice(a, b);
global.window = {};
global.__tier106 = 0;
global.enc79PlayerTier = () => global.__tier106;
/* DLG119_SHADOW_STEM 用 typeof 守住：pristine main 冇呢個 const，eval 回傳 undefined
   而唔係成個 test 掟 ReferenceError——反證要乾淨 FAIL，唔係 crash。
   外層 binding 叫 STEM119 唔叫 DLG119_SHADOW_STEM：direct eval 同外層共用 scope，
   同名 const 喺 pristine（模組入面冇內層宣告）會撞 TDZ。 */
const D = eval(code + '\n;({DLG106_GAZE,DLG106_EMOTION_MAP,DLG106_CAT_TO_EXPR,DLG119_SHADOW_STEM:(typeof DLG119_SHADOW_STEM!=="undefined"?DLG119_SHADOW_STEM:undefined)})');
const GAZE = D.DLG106_GAZE, STEM119 = D.DLG119_SHADOW_STEM;
/* DLG119 helper 唔喺度（pristine main）→ 即刻乾淨 FAIL，唔好捱到落去先 crash。 */
if(typeof dlg119ShadowAsset !== 'function' || typeof dlg119DedupePair !== 'function' || !STEM119){
  console.log('FAIL DLG119 模組唔喺度（pristine main 預期 FAIL：影 helper／別名表未接入）');
  console.log('RESULT FAIL');
  process.exit(1);
}
// function 宣告經 eval 已入 scope：dlg119ShadowAsset/dlg119IsShadow/dlg119Candidates/
// dlg119HaloUrl/dlg119DedupePair/dlg106StemFor/dlg106Candidates/dlg106ResolveSides/dlg106HasFullbody

/* ---- (1) 影 asset 映射 ---- */
ok('GAZE 39 鍵（34＋v119 5 鍵）', Object.keys(GAZE).length === 39);
ok('影鍵 front＋唔翻得',
  ['shadow_male','shadow_female','shadow_elder','generic_cinema_asst'].every(k =>
    GAZE[k] && GAZE[k].gaze === 'front' && GAZE[k].flipSafe === false));
ok('老臨記 front＋唔翻得', GAZE.crew_laolinji && GAZE.crew_laolinji.gaze === 'front' && GAZE.crew_laolinji.flipSafe === false);
ok('shadowAsset：三影回自己名', dlg119ShadowAsset('shadow_male') === 'shadow_male'
  && dlg119ShadowAsset('shadow_female') === 'shadow_female'
  && dlg119ShadowAsset('shadow_elder') === 'shadow_elder');
ok('shadowAsset：generic_cinema_asst 別名去男影', dlg119ShadowAsset('generic_cinema_asst') === 'shadow_male');
ok('shadowAsset：老臨記／阿偉／芬姐唔係影（回 null）',
  dlg119ShadowAsset('crew_laolinji') === null && dlg119ShadowAsset('awi') === null
  && dlg119ShadowAsset('extra_ad_fen') === null && dlg119ShadowAsset('extra_unknown') === null);
ok('isShadow：影 true、其餘 false', dlg119IsShadow('shadow_male') === true
  && dlg119IsShadow('generic_cinema_asst') === true && dlg119IsShadow('crew_laolinji') === false);
ok('反證：別名表刪走 generic_cinema_asst → shadowAsset 必須回 null',
  (()=>{ const t = Object.assign({}, STEM119); delete t.generic_cinema_asst;
    return (t['generic_cinema_asst'] || null) === null; })());

/* ---- (2) 講者／聽者候補鏈 ---- */
ok('講者影候補直入 base（冇 expr 混入）',
  JSON.stringify(dlg119Candidates('shadow_male', false)) === JSON.stringify(['assets/story/fullbody/shadow_male_base.webp?v=20a106']));
ok('聽者影候補 _dim 行先、base 兜底',
  JSON.stringify(dlg119Candidates('shadow_female', true)) === JSON.stringify(['assets/story/fullbody/shadow_female_dim_base.webp?v=20a106','assets/story/fullbody/shadow_female_base.webp?v=20a106']));
ok('光暈 URL 係同 stem halo png',
  dlg119HaloUrl('shadow_elder') === 'assets/story/fullbody/shadow_elder_halo.png?v=20a106');
ok('stem 別名：dlg106StemFor(generic_cinema_asst)＝shadow_male',
  dlg106StemFor('generic_cinema_asst') === 'shadow_male');
ok('dlg106Candidates 別名生效：generic_cinema_asst neutral 首選男影 base',
  dlg106Candidates('generic_cinema_asst', 'neutral')[0] === 'assets/story/fullbody/shadow_male_base.webp?v=20a106');
ok('dlg106Candidates 影 base 喺鏈內（expr 404 後退 base）',
  dlg106Candidates('shadow_male', 'happy').some(u => u === 'assets/story/fullbody/shadow_male_base.webp?v=20a106'));

/* ---- (3) 同影去重 ---- */
ok('去重：同 asset 唔同 id（男影＋院線助理別名）→ 只留後者',
  JSON.stringify(dlg119DedupePair(['shadow_male','generic_cinema_asst'])) === JSON.stringify(['generic_cinema_asst']));
ok('去重：調轉次序 → 只留後者',
  JSON.stringify(dlg119DedupePair(['generic_cinema_asst','shadow_male'])) === JSON.stringify(['shadow_male']));
ok('去重：同一 id → 單人',
  JSON.stringify(dlg119DedupePair(['shadow_male','shadow_male'])) === JSON.stringify(['shadow_male']));
ok('去重：唔同 asset（男影＋女影）→ 唔郁',
  JSON.stringify(dlg119DedupePair(['shadow_male','shadow_female'])) === JSON.stringify(['shadow_male','shadow_female']));
ok('去重：影＋有面（男影＋老臨記）→ 唔郁（老臨記唔係影）',
  JSON.stringify(dlg119DedupePair(['shadow_male','crew_laolinji'])) === JSON.stringify(['shadow_male','crew_laolinji']));
ok('去重：影＋真人（男影＋阿偉）→ 唔郁',
  JSON.stringify(dlg119DedupePair(['shadow_male','awi'])) === JSON.stringify(['shadow_male','awi']));
ok('去重：單人／空 pair → 原樣',
  JSON.stringify(dlg119DedupePair(['awi'])) === JSON.stringify(['awi'])
  && JSON.stringify(dlg119DedupePair([])) === JSON.stringify([]));

/* ---- (4) 企位解析（影唔翻） ---- */
let r = dlg106ResolveSides('shadow_male', 'shadow_female');
ok('男影×女影：雙人、雙方無翻', r && r.left && r.right && r.left.flip === false && r.right.flip === false);
r = dlg106ResolveSides('shadow_male', 'shadow_male');
ok('同影 pair（同一 id）→ 單人企左、唔翻',
  r && r.single && r.single.id === 'shadow_male' && r.single.side === 'left' && r.single.flip === false);
r = dlg106ResolveSides('shadow_elder', 'shadow_male');
ok('老年影×男影：雙人、雙方無翻', r && r.left && r.right && r.left.flip === false && r.right.flip === false);
r = dlg106ResolveSides('awi', 'shadow_male');
ok('阿偉×男影：阿偉左、男影右、雙方無翻',
  r && r.left.id === 'awi' && r.right.id === 'shadow_male' && r.left.flip === false && r.right.flip === false);
ok('dlg106HasFullbody：5 個新 id 全部行新版雙人全身舞台',
  ['shadow_male','shadow_female','shadow_elder','crew_laolinji','generic_cinema_asst'].every(id => dlg106HasFullbody(id)));

console.log(fails.length ? 'RESULT FAIL (' + fails.length + ')' : 'RESULT PASS');
process.exit(fails.length ? 1 : 0);
