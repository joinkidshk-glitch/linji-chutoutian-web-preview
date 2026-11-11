// v20a107 DLG107 邏輯測試：8 張 fix2 新表情圖真係會被對話解析器揀中。
// 資料一律由 index.html 抽 DLG106 模組真身 eval（同 test_dlg106_logic.js 手法），
// tier 經 global.__tier106 stub（enc79PlayerTier 替身）控制。
// 覆蓋：(1) 每張新圖係對應（講者，分類，階段）嘅候補鏈首選——即 runtime
//         唔會靜靜退 base；(2) 阿偉 s2/s3 階段判定：tier 2→awi_s2、tier 3→awi_s3、
//         tier 0→awi（s1 回歸）；(3) 真實對白句經 dlg106ResolveCategory
//         判返對應分類（C1 阿偉 think 句＋每類新表情各一句）；
//         (4) 反證：tier 2↔3 切換時首選必須跟住變；未知講者回 []；
//         垃圾輸入唔 crash、回 neutral。
// 注意：dlg106Candidates 只係排 URL 次序，唔查檔案存在——檔案存在由
// test_dlg107_static.py 守門；瀏覽器真載入由 qa107 實駕驗證。
// 用法：node tests/test_dlg107_logic.js [path-to-index.html]
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
  // [speaker, category, tier, 預期首選]
  ['awi', 'think', 2, `assets/story/fullbody/awi_s2_think.webp${V}`],
  ['awi', 'think', 3, `assets/story/fullbody/awi_s3_think.webp${V}`],
  ['so_jiyan', 'happy', 0, `assets/story/fullbody/so_jiyan_smile.webp${V}`],
  ['cheung_tsijun', 'serious', 0, `assets/story/fullbody/cheung_tsijun_serious.webp${V}`],
  ['ho_sang', 'sad', 0, `assets/story/fullbody/ho_sang_sad.webp${V}`],
  ['gao_wenhan', 'serious', 0, `assets/story/fullbody/gao_wenhan_serious.webp${V}`],
  ['tang_laiping', 'serious', 0, `assets/story/fullbody/tang_laiping_serious.webp${V}`],
  ['chow_choiyi', 'think', 0, `assets/story/fullbody/chow_choiyi_think.webp${V}`],
];
for (const [sp, cat, tier, exp] of NEW) {
  global.__tier106 = tier;
  ok(`${sp} ${cat} (tier ${tier}) 首選＝${exp.split('/').pop()}`, first(sp, cat) === exp);
}

/* ---- (2) 阿偉階段判定＋回歸 ---- */
global.__tier106 = 2;
ok('tier 2 → awi_s2 stem', dlg106AweiStem() === 'awi_s2');
global.__tier106 = 3;
ok('tier 3 → awi_s3 stem', dlg106AweiStem() === 'awi_s3');
global.__tier106 = 0;
ok('tier 0 → awi stem（s1 回歸）', dlg106AweiStem() === 'awi');
ok('tier 0 awi think 首選仍係 s1 awi_think（舊圖冇被搶）',
   first('awi', 'think') === `assets/story/fullbody/awi_think.webp${V}`);
global.__tier106 = 2;
ok('tier 2 awi happy 首選 awi_s2_smile（舊 s2 圖冇被搶）',
   first('awi', 'happy') === `assets/story/fullbody/awi_s2_smile.webp${V}`);
global.__tier106 = 3;
ok('tier 3 awi serious 首選 awi_s3_serious（舊 s3 圖冇被搶）',
   first('awi', 'serious') === `assets/story/fullbody/awi_s3_serious.webp${V}`);

/* ---- (3) 真實對白句分類（經 map lookup；句出自 lines_classified.json） ---- */
const LINES = [
  // [講者, 句, 預期分類] —— C1 阿偉 think 句＋每類新表情各一句
  ['awi', '呢兩條路真係各有千秋，要諗清楚先好決定。', 'think'],
  ['so_jiyan', '阿偉，我接到一套新戲，個角色終於唔使我齋笑，我好緊張又好開心。', 'happy'],
  ['cheung_tsijun', '我睇住你由企唔穩做到企得穩。記住，邊個位都好——唔好丟咗當初捱通宵嗰份心。', 'serious'],
  ['ho_sang', '後生仔心頭高，唔怪你。出面風大雨大——唔好後悔就得。', 'sad'],
  ['gao_wenhan', '呢個圈子最唔缺勤力嘅人，我要睇到你嘅天賦。', 'serious'],
  ['tang_laiping', '感情唔值錢，數字先係標準。', 'serious'],
  ['chow_choiyi', '我上次同陸柏言同場，見佢休息嗰陣一個人坐埋邊，劇本都冇揭開，唔知係攰定有心事，我都唔敢行埋去。', 'think'],
];
for (const [sp, text, cat] of LINES) {
  const got = dlg106ResolveCategory({ speakerId: sp, text });
  ok(`分類：${sp}「${text.slice(0, 12)}…」→ ${cat}`, got === cat);
  global.__tier106 = 0;
  const expr = dlg106ExprFor(got);
  ok(`分類 ${cat}→表情 ${expr}（候選首選唔係 base）`,
     dlg106Candidates(sp, cat)[0].indexOf(`_${expr}.webp`) >= 0);
}

/* ---- (4) 反證 ---- */
global.__tier106 = 2;
const s2 = first('awi', 'think');
global.__tier106 = 3;
const s3 = first('awi', 'think');
ok('反證：tier 2↔3 切換，awi think 首選必須跟住變（s2≠s3）', s2 !== s3);
ok('反證：未知講者 → 空候補鏈（唔會亂指去現有圖）',
   dlg106Candidates('extra_unknown', 'think').length === 0);
ok('反證：so_jiyan happy 候補鏈 ≠ neutral 候補鏈（分類真係影響揀圖）',
   first('so_jiyan', 'happy') !== first('so_jiyan', 'neutral'));
ok('反證：垃圾輸入唔 crash、回 neutral',
   dlg106ResolveCategory({ speakerId: 'awi', text: '＠＃＄％︿＆＊' }) === 'neutral');
ok('反證：cheung_tsijun think（冇 think 圖）首選係 think URL、次選退 base——'
   + '證明首選唔係硬編 base',
   dlg106Candidates('cheung_tsijun', 'think')[0].indexOf('cheung_tsijun_think.webp') >= 0
   && dlg106Candidates('cheung_tsijun', 'think')[2].indexOf('cheung_tsijun_base.webp') >= 0);

console.log(fails.length ? `RESULT FAIL (${fails.length})` : 'RESULT PASS');
process.exit(fails.length ? 1 : 0);
