// v20a126 DLG126 邏輯測試：6 張新表情圖真係會被對話解析器揀中。
// 資料一律由 index.html 抽 DLG106 模組真身 eval（同 test_dlg123_logic.js 手法），
// tier 經 global.__tier106 stub（enc79PlayerTier 替身）控制。
// 覆蓋：(1) 每張新圖係對應（講者，分類）嘅候補鏈首選——即 runtime
//         唔會靜靜退 base；(2) 真實對白句經 dlg106ResolveCategory 判返對應分類
//         （每類新表情各一句）；(3) 反證：舊圖冇被搶（同角其他分類首選不變）；
//         未知講者回 []；垃圾輸入唔 crash、回 neutral；分類真係影響揀圖。
// 注意：dlg106Candidates 只係排 URL 次序，唔查檔案存在——檔案存在由
// test_dlg126_static.py 守門；瀏覽器真載入由 qa126 實駕驗證。
// 用法：node tests/test_dlg126_logic.js [path-to-index.html]
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
  ['fong_siulung', 'happy', `assets/story/fullbody/fong_siulung_smile.webp${V}`],
  ['pang_siuki', 'serious', `assets/story/fullbody/pang_siuki_serious.webp${V}`],
  ['gu_mingfai', 'happy', `assets/story/fullbody/gu_mingfai_smile.webp${V}`],
  ['yip_manji', 'serious', `assets/story/fullbody/yip_manji_serious.webp${V}`],
  ['lan_ruoxi', 'shy', `assets/story/fullbody/lan_ruoxi_shy.webp${V}`],
  ['ching_tinlok', 'sad', `assets/story/fullbody/ching_tinlok_sad.webp${V}`],
];
for (const [sp, cat, exp] of NEW) {
  global.__tier106 = 0;
  ok(`${sp} ${cat} 首選＝${exp.split('/').pop()}`, first(sp, cat) === exp);
}

/* ---- (2) 真實對白句分類（經 map lookup／分類器；句出自 lines_classified.json） ---- */
const LINES = [
  // [講者, 句, 預期分類]
  ['fong_siulung', '跳完呢場，我請你食宵夜，哈哈！', 'happy'],
  ['pang_siuki', '後台有啲規矩冇寫出嚟㗎，大佬嗰張梳化唔好亂坐，人哋嗰支咪唔好亂掂。', 'serious'],
  ['gu_mingfai', '一半都好，一半已經幫我頂住最急嗰關。多謝你，你冇當我係外人。', 'happy'],
  ['yip_manji', '記住，你講過嘅每一句，佢哋都可以剪到變第二個意思。', 'serious'],
  ['lan_ruoxi', '哎呀——唔好意思，唔好意思，借過！（成疊通告牌同流程表，俾人一撞，散晒一地）', 'shy'],
  ['ching_tinlok', '你係少數見過我喊、又冇走開嘅人。呢行，肯企埋同一邊嘅人，冇幾個咋。', 'sad'],
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
ok('反證：pang_siuki surprise 候補鏈首選仍係 v123 舊圖（新 serious 圖冇搶走其他分類）',
   first('pang_siuki', 'surprise') === `assets/story/fullbody/pang_siuki_surprise.webp${V}`);
ok('反證：gu_mingfai sad 首選仍係舊圖 gu_mingfai_sad（新 smile 圖冇搶走其他分類）',
   first('gu_mingfai', 'sad') === `assets/story/fullbody/gu_mingfai_sad.webp${V}`);
ok('反證：yip_manji smile 首選仍係舊圖 yip_manji_smile（新 serious 圖冇搶走其他分類）',
   first('yip_manji', 'smile') === `assets/story/fullbody/yip_manji_smile.webp${V}`);
ok('反證：lan_ruoxi smile 首選仍係舊圖 lan_ruoxi_smile（新 shy 圖冇搶走其他分類）',
   first('lan_ruoxi', 'smile') === `assets/story/fullbody/lan_ruoxi_smile.webp${V}`);
ok('反證：ching_tinlok smile 首選仍係舊圖 ching_tinlok_smile（新 sad 圖冇搶走其他分類）',
   first('ching_tinlok', 'smile') === `assets/story/fullbody/ching_tinlok_smile.webp${V}`);
ok('反證：fong_siulung serious 首選仍係舊圖 fong_siulung_serious（新 smile 圖冇搶走其他分類）',
   first('fong_siulung', 'serious') === `assets/story/fullbody/fong_siulung_serious.webp${V}`);
ok('反證：ching_tinlok sad 候補鏈次選退 base（首選唔係硬編 base）',
   dlg106Candidates('ching_tinlok', 'sad')[2].indexOf('ching_tinlok_base.webp') >= 0);

console.log(fails.length ? `RESULT FAIL (${fails.length})` : 'RESULT PASS');
process.exit(fails.length ? 1 : 0);
