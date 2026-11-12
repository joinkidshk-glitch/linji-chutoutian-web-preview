// v20a123 DLG123 邏輯測試：12 張新表情圖真係會被對話解析器揀中。
// 資料一律由 index.html 抽 DLG106 模組真身 eval（同 test_dlg107_logic.js 手法），
// tier 經 global.__tier106 stub（enc79PlayerTier 替身）控制。
// 覆蓋：(1) 每張新圖係對應（講者，分類，階段）嘅候補鏈首選——即 runtime
//         唔會靜靜退 base；(2) 阿偉 s2/s3 階段判定＋跨階段 angry 後備：
//         s2/s3 冇自己嘅 angry 圖，候補鏈必須經 awi_angry（新圖）先至退 base；
//         (3) 真實對白句經 dlg106ResolveCategory 判返對應分類（每類新表情各一句）；
//         (4) 反證：tier 2↔3 切換時首選必須跟住變；未知講者回 []；
//         垃圾輸入唔 crash、回 neutral。
// 注意：dlg106Candidates 只係排 URL 次序，唔查檔案存在——檔案存在由
// test_dlg123_static.py 守門；瀏覽器真載入由 qa123 實駕驗證。
// 用法：node tests/test_dlg123_logic.js [path-to-index.html]
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
  ['awi', 'surprise', 2, `assets/story/fullbody/awi_s2_surprise.webp${V}`],
  ['awi', 'sad', 2, `assets/story/fullbody/awi_s2_sad.webp${V}`],
  ['awi', 'shy', 2, `assets/story/fullbody/awi_s2_shy.webp${V}`],
  ['awi', 'surprise', 3, `assets/story/fullbody/awi_s3_surprise.webp${V}`],
  ['awi', 'sad', 3, `assets/story/fullbody/awi_s3_sad.webp${V}`],
  ['awi', 'shy', 3, `assets/story/fullbody/awi_s3_shy.webp${V}`],
  ['awi', 'angry', 0, `assets/story/fullbody/awi_angry.webp${V}`],
  ['chung_choning', 'think', 0, `assets/story/fullbody/chung_choning_think.webp${V}`],
  ['chung_choning', 'happy', 0, `assets/story/fullbody/chung_choning_smile.webp${V}`],
  ['ho_sang', 'angry', 0, `assets/story/fullbody/ho_sang_angry.webp${V}`],
  ['liu_bingxing', 'shy', 0, `assets/story/fullbody/liu_bingxing_shy.webp${V}`],
  ['pang_siuki', 'surprise', 0, `assets/story/fullbody/pang_siuki_surprise.webp${V}`],
];
for (const [sp, cat, tier, exp] of NEW) {
  global.__tier106 = tier;
  ok(`${sp} ${cat} (tier ${tier}) 首選＝${exp.split('/').pop()}`, first(sp, cat) === exp);
}

/* ---- (2) 阿偉階段判定＋回歸＋跨階段 angry 後備 ---- */
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
// s2/s3 冇自己嘅 angry 圖：候補鏈 [sX_angry, sX_base, awi_angry, awi_base]
// （webp/png 各一，awi_angry.webp 排第 5 位 index 4），唔會靜靜退 sX_base。
for (const tier of [2, 3]) {
  global.__tier106 = tier;
  const chain = dlg106Candidates('awi', 'angry');
  ok(`tier ${tier} awi angry 候補鏈第 5 位＝awi_angry.webp（跨階段後備，唔退 base）`,
     chain[4] === `assets/story/fullbody/awi_angry.webp${V}`);
  ok(`tier ${tier} awi angry 候補鏈第 3 位係 s${tier}_base（先退本階段 base 再跨階段）`,
     chain[2] === `assets/story/fullbody/awi_s${tier}_base.webp${V}`);
}

/* ---- (3) 真實對白句分類（經 map lookup／分類器；句出自 lines_classified.json） ---- */
const LINES = [
  // [講者, 句, 預期分類]
  ['awi', '張導，我……我其實冇諗過咁深，我淨係想有戲拍。', 'surprise'],
  ['awi', '（佢講到「睇我跌」嗰陣，隻手不自覺摸咗摸條腰——嗰啲傷，隔咗咁多年，一落雨，會唔會仲痛？）', 'sad'],
  ['awi', '哦……唔好意思，我而家行開。', 'shy'],
  ['awi', '齊生？我……我冇阻住你呀，我企邊邊咋。', 'angry'],
  ['chung_choning', '諗清楚你係邊個先企。心入面冇嗰個人，你企成點都係你自己喺度罰企。', 'think'],
  ['chung_choning', '嗰個，阿偉，你嗰場望住人走嗰下，眼神有半秒係真嘅，半秒啫，唔好咁快開心。', 'happy'],
  ['ho_sang', '顧明輝，駐唱嗰個。佢唔係衰人，係真係冇。', 'angry'],
  ['liu_bingxing', '唔得唔得，呢句一出，觀眾未笑，我自己先尷尬……', 'shy'],
  ['pang_siuki', '咦，阿偉！係咪先？我冇記錯人呀？', 'surprise'],
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
const s2 = first('awi', 'surprise');
global.__tier106 = 3;
const s3 = first('awi', 'surprise');
ok('反證：tier 2↔3 切換，awi surprise 首選必須跟住變（s2≠s3）', s2 !== s3);
ok('反證：未知講者 → 空候補鏈（唔會亂指去現有圖）',
   dlg106Candidates('extra_unknown', 'surprise').length === 0);
ok('反證：pang_siuki surprise 候補鏈 ≠ neutral 候補鏈（分類真係影響揀圖）',
   first('pang_siuki', 'surprise') !== first('pang_siuki', 'neutral'));
ok('反證：垃圾輸入唔 crash、回 neutral',
   dlg106ResolveCategory({ speakerId: 'awi', text: '＠＃＄％︿＆＊' }) === 'neutral');
ok('反證：pang_siuki serious（冇 serious 圖）首選係 serious URL、次選退 base——'
   + '證明首選唔係硬編 base',
   dlg106Candidates('pang_siuki', 'serious')[0].indexOf('pang_siuki_serious.webp') >= 0
   && dlg106Candidates('pang_siuki', 'serious')[2].indexOf('pang_siuki_base.webp') >= 0);
ok('反證：chung_choning angry（冇 angry 圖）首選係 angry URL、唔係偷換做 think／smile',
   dlg106Candidates('chung_choning', 'angry')[0].indexOf('chung_choning_angry.webp') >= 0);

console.log(fails.length ? `RESULT FAIL (${fails.length})` : 'RESULT PASS');
process.exit(fails.length ? 1 : 0);
