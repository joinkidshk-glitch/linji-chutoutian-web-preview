// v20a127 DLG127 邏輯測試：22 張新表情圖真係會被對話解析器揀中。
// 資料一律由 index.html 抽 DLG106 模組真身 eval（同 test_dlg123_logic.js 手法），
// tier 經 global.__tier106 stub（enc79PlayerTier 替身）控制。
// 覆蓋：(1) 每張新圖係對應（講者，分類）嘅候補鏈首選——即 runtime
//         唔會靜靜退 base；(2) 真實對白句經 dlg106ResolveCategory 判返對應分類
//         （每類新表情各一句；括號舞台指示句——ching_tinlok think／lan_ruoxi think——
//         係旁白動作句，唔入分類斷言，只驗首選）；(3) 反證：舊圖冇被搶（同角
//         其他分類首選不變）；未知講者回 []；垃圾輸入唔 crash、回 neutral；分類
//         真係影響揀圖；零覆蓋起家嘅四角（鄭威廉／關海媚／莫少輝／阿金叔）neutral 仍係 base。
// 注意：dlg106Candidates 只係排 URL 次序，唔查檔案存在——檔案存在由
// test_dlg127_static.py 守門；瀏覽器真載入由 qa127 實駕驗證。
// 用法：node tests/test_dlg127_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS ' : 'FAIL ') + name); }
function info(msg){ console.log('INFO ' + msg); }

const a = html.indexOf('/* ===== v20a106 DLG106');
const b = html.indexOf('/* ===== DLG106 模組完 ===== */');
ok('搵到 DLG106 模組', a >= 0 && b > a);
const code = html.slice(a, b);
global.window = {};
global.__tier106 = 0;
global.enc79PlayerTier = () => global.__tier106;
eval(code + '\n;({DLG106_GAZE,DLG106_EMOTION_MAP,DLG106_CAT_TO_EXPR})');
// function 宣告經 eval 已入 scope：dlg106Candidates/dlg106ResolveCategory/
// dlg106AweiStem/dlg106ExprFor/dlg106Classify/dlg106Lookup

const first = (sp, cat) => dlg106Candidates(sp, cat)[0];
const V = '?v=20a106';
const NEW = [
  // [speaker, category, 預期首選]
  ['gu_mingfai', 'shy', `assets/story/fullbody/gu_mingfai_shy.webp${V}`],
  ['gu_mingfai', 'angry', `assets/story/fullbody/gu_mingfai_angry.webp${V}`],
  ['gu_mingfai', 'think', `assets/story/fullbody/gu_mingfai_think.webp${V}`],
  ['pang_siuki', 'sad', `assets/story/fullbody/pang_siuki_sad.webp${V}`],
  ['chow_choiyi', 'sad', `assets/story/fullbody/chow_choiyi_sad.webp${V}`],
  ['chow_choiyi', 'angry', `assets/story/fullbody/chow_choiyi_angry.webp${V}`],
  ['yip_manji', 'surprise', `assets/story/fullbody/yip_manji_surprise.webp${V}`],
  ['yip_manji', 'angry', `assets/story/fullbody/yip_manji_angry.webp${V}`],
  ['yip_manji', 'shy', `assets/story/fullbody/yip_manji_shy.webp${V}`],
  ['ching_tinlok', 'shy', `assets/story/fullbody/ching_tinlok_shy.webp${V}`],
  ['ching_tinlok', 'surprise', `assets/story/fullbody/ching_tinlok_surprise.webp${V}`],
  ['ching_tinlok', 'think', `assets/story/fullbody/ching_tinlok_think.webp${V}`],
  ['lan_ruoxi', 'serious', `assets/story/fullbody/lan_ruoxi_serious.webp${V}`],
  ['lan_ruoxi', 'think', `assets/story/fullbody/lan_ruoxi_think.webp${V}`],
  ['fong_siulung', 'sad', `assets/story/fullbody/fong_siulung_sad.webp${V}`],
  ['fong_siulung', 'angry', `assets/story/fullbody/fong_siulung_angry.webp${V}`],
  ['cheng_william', 'serious', `assets/story/fullbody/cheng_william_serious.webp${V}`],
  ['cheng_william', 'shy', `assets/story/fullbody/cheng_william_shy.webp${V}`],
  ['kwan_hoimei', 'serious', `assets/story/fullbody/kwan_hoimei_serious.webp${V}`],
  ['mok_siufai', 'sad', `assets/story/fullbody/mok_siufai_sad.webp${V}`],
  ['uncle_kim', 'happy', `assets/story/fullbody/uncle_kim_smile.webp${V}`],
  ['uncle_kim', 'serious', `assets/story/fullbody/uncle_kim_serious.webp${V}`],
];
for (const [sp, cat, exp] of NEW) {
  global.__tier106 = 0;
  ok(`${sp} ${cat} 首選＝${exp.split('/').pop()}`, first(sp, cat) === exp);
}

/* ---- (2) 真實對白句分類（經 map lookup／分類器；句出自 lines_classified.json；
         開工前用 /tmp/probe127.js 逐句驗過，28/28 命中） ---- */
const LINES = [
  // [講者, 句, 預期分類]
  ['gu_mingfai', '哦，係你呀。唔好意思，我趕住入去錄節目，有咩下次先講。', 'shy'],
  ['gu_mingfai', '阿偉，唔好再行咁近住，我仲未企返到可以同你平排企嗰個位。', 'angry'],
  ['gu_mingfai', '你唔好問咁多，問咗，我都唔知點答你先唔失禮。我口頭應承你，一有，我就還返俾你。', 'think'],
  ['pang_siuki', '人哋叫我金牌司儀，咪就係邊度有窿就塞我去補，補到自己都冇咗聲。', 'sad'],
  ['chow_choiyi', '陸柏言嗰場戲，佢明明背熟晒對白，但一埋位就停咗兩停，導演冇鬧，仲叫大家抖下先，可能佢真係好攰。', 'sad'],
  ['chow_choiyi', '我前幾日喺清水灣嗰組做嘢，氣氛幾好，副導又唔會亂鬧人，新人去嗰邊撞下，學到嘢又唔使捱得咁辛苦。', 'angry'],
  ['yip_manji', '你……你點會知嗰單嘢係假㗎？我呢排俾人問到，我自己都唔知點答呀……', 'surprise'],
  ['yip_manji', '由細角做起……公司聽到實鬧我黐線。', 'angry'],
  ['yip_manji', '唔好意思，你擋住我條路喇。', 'shy'],
  ['ching_tinlok', '出面仲有人問，點解冇駱家聲份……我聽到都唔好意思，家聲哥唱功好過我咁多，點會輪到我先呀？', 'shy'],
  ['ching_tinlok', '咦，你而家有份量喇喎，唔再係企喺後面嗰啲喇，勁喎。', 'surprise'],
  ['lan_ruoxi', '但你要記住，無論選邊個，我們之後在片場見面，都不會再一樣。', 'serious'],
  ['fong_siulung', '我而家跟高師傅嗰班，做替身做到周身瘀傷——不過有飯食，就唔怕啦。', 'sad'],
  ['fong_siulung', '高師傅，你唔好嚇佢啦。我同佢自細打到大，佢食得苦㗎。', 'angry'],
  ['cheng_william', '唔好亂接平民貨，會拉低定位。', 'serious'],
  ['cheng_william', 'Darling！今日個 look 災難，但我鍾意你個眼神。', 'shy'],
  ['kwan_hoimei', '你要記住，公關可以幫你包裝，但包不住你真正的心意。', 'serious'],
  ['mok_siufai', '公司畀十萬要我捧別人，我偏偏想播你——唔好令我失望。', 'sad'],
  ['uncle_kim', '紅唔紅係命，開心先係本事。', 'happy'],
  ['uncle_kim', '傳承這種事，不是等你發了達才做，是你肯不肯記住自己是從哪裡來的。', 'serious'],
];
for (const [sp, text, cat] of LINES) {
  const got = dlg106ResolveCategory({ speakerId: sp, text });
  ok(`分類：${sp}「${text.slice(0, 12)}…」→ ${cat}`, got === cat);
  global.__tier106 = 0;
  const expr = dlg106ExprFor(got);
  ok(`分類 ${cat}→表情 ${expr}（候選首選唔係 base）`,
     dlg106Candidates(sp, cat)[0].indexOf(`_${expr}.webp`) >= 0);
}

/* ---- (3) 反證 ---- */
ok('反證：未知講者 → 空候補鏈（唔會亂指去現有圖）',
   dlg106Candidates('extra_unknown', 'happy').length === 0);
ok('反證：垃圾輸入唔 crash、回 neutral',
   dlg106ResolveCategory({ speakerId: 'fong_siulung', text: '＠＃＄％︿＆＊' }) === 'neutral');
ok('反證：fong_siulung happy 候補鏈 ≠ neutral 候補鏈（分類真係影響揀圖）',
   first('fong_siulung', 'happy') !== first('fong_siulung', 'neutral'));
ok('反證：gu_mingfai happy 首選仍係 v126 舊圖（新 shy/angry/think 圖冇搶走其他分類）',
   first('gu_mingfai', 'happy') === `assets/story/fullbody/gu_mingfai_smile.webp${V}`);
ok('反證：pang_siuki surprise 首選仍係 v123 舊圖（新 sad 圖冇搶走其他分類）',
   first('pang_siuki', 'surprise') === `assets/story/fullbody/pang_siuki_surprise.webp${V}`);
ok('反證：yip_manji smile 首選仍係舊圖 yip_manji_smile（新 surprise/angry/shy 圖冇搶走其他分類）',
   first('yip_manji', 'smile') === `assets/story/fullbody/yip_manji_smile.webp${V}`);
ok('反證：lan_ruoxi smile 首選仍係舊圖 lan_ruoxi_smile（新 serious/think 圖冇搶走其他分類）',
   first('lan_ruoxi', 'smile') === `assets/story/fullbody/lan_ruoxi_smile.webp${V}`);
ok('反證：ching_tinlok smile 首選仍係舊圖 ching_tinlok_smile（新 shy/surprise/think 圖冇搶走其他分類）',
   first('ching_tinlok', 'smile') === `assets/story/fullbody/ching_tinlok_smile.webp${V}`);
ok('反證：fong_siulung smile 首選仍係 v126 舊圖（新 sad/angry 圖冇搶走其他分類）',
   first('fong_siulung', 'smile') === `assets/story/fullbody/fong_siulung_smile.webp${V}`);
ok('反證：chow_choiyi smile 首選仍係舊圖（新 sad/angry 圖冇搶走其他分類）',
   first('chow_choiyi', 'smile') === `assets/story/fullbody/chow_choiyi_smile.webp${V}`);
ok('反證：cheng_william neutral 首選係 base（零覆蓋起家，neutral 不變）',
   first('cheng_william', 'neutral') === `assets/story/fullbody/cheng_william_base.webp${V}`);
ok('反證：kwan_hoimei neutral 首選係 base（零覆蓋起家，neutral 不變）',
   first('kwan_hoimei', 'neutral') === `assets/story/fullbody/kwan_hoimei_base.webp${V}`);
ok('反證：mok_siufai neutral 首選係 base（零覆蓋起家，neutral 不變）',
   first('mok_siufai', 'neutral') === `assets/story/fullbody/mok_siufai_base.webp${V}`);
ok('反證：uncle_kim neutral 首選係 base（零覆蓋起家，neutral 不變）',
   first('uncle_kim', 'neutral') === `assets/story/fullbody/uncle_kim_base.webp${V}`);
ok('反證：ching_tinlok think 候補鏈次選退 base（首選唔係硬編 base）',
   dlg106Candidates('ching_tinlok', 'think')[2].indexOf('ching_tinlok_base.webp') >= 0);

console.log(fails.length ? `RESULT FAIL (${fails.length})` : 'RESULT PASS');
process.exit(fails.length ? 1 : 0);
