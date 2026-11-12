// v20a138 DLG138 邏輯測試：37 張新表情圖真係會被對話解析器揀中。
// 資料一律由 index.html 抽 DLG106 模組真身 eval（同 test_dlg127_logic.js 手法），
// tier 經 global.__tier106 stub（enc79PlayerTier 替身）控制。
// 覆蓋：(1) 每張新圖係對應（講者，分類）嘅候補鏈首選——即 runtime
//         唔會靜靜退 base；(2) 真實對白句經 dlg106ResolveCategory 判返對應分類
//         （每類新表情各一句，全部係 verdict138.json 嘅 live evidence 句；
//         luk_baakyin sad 嗰句 beat emotion 欄係 tired，要跟 runtime 主路徑
//         一樣傳 emotion 先判到 sad）；(3) 反證：舊圖冇被搶（同角
//         其他分類首選不變）；未知講者回 []；垃圾輸入唔 crash、回 neutral；分類
//         真係影響揀圖；得 base 嘅兩角（老臨記／芬姐）neutral 仍係 base。
// 注意：dlg106Candidates 只係排 URL 次序，唔查檔案存在——檔案存在由
// test_dlg138_static.py 守門；瀏覽器真載入由 qa138 實駕驗證。
// 用法：node tests/test_dlg138_logic.js [path-to-index.html]
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
  ['chai_zanhoi', 'angry', `assets/story/fullbody/chai_zanhoi_angry.webp${V}`],
  ['chai_zanhoi', 'shy', `assets/story/fullbody/chai_zanhoi_shy.webp${V}`],
  ['chai_zanhoi', 'happy', `assets/story/fullbody/chai_zanhoi_smile.webp${V}`],
  ['chai_zanhoi', 'think', `assets/story/fullbody/chai_zanhoi_think.webp${V}`],
  ['cheung_hakfan', 'serious', `assets/story/fullbody/cheung_hakfan_serious.webp${V}`],
  ['cheung_tsijun', 'sad', `assets/story/fullbody/cheung_tsijun_sad.webp${V}`],
  ['cheung_tsijun', 'think', `assets/story/fullbody/cheung_tsijun_think.webp${V}`],
  ['chung_choning', 'angry', `assets/story/fullbody/chung_choning_angry.webp${V}`],
  ['crew_laolinji', 'serious', `assets/story/fullbody/crew_laolinji_serious.webp${V}`],
  ['extra_ad_fen', 'sad', `assets/story/fullbody/extra_ad_fen_sad.webp${V}`],
  ['extra_ad_fen', 'serious', `assets/story/fullbody/extra_ad_fen_serious.webp${V}`],
  ['ho_sang', 'surprise', `assets/story/fullbody/ho_sang_surprise.webp${V}`],
  ['ko_chunkit', 'shy', `assets/story/fullbody/ko_chunkit_shy.webp${V}`],
  ['ko_chunkit', 'think', `assets/story/fullbody/ko_chunkit_think.webp${V}`],
  ['lin_hiu', 'serious', `assets/story/fullbody/lin_hiu_serious.webp${V}`],
  ['lin_hiu', 'happy', `assets/story/fullbody/lin_hiu_smile.webp${V}`],
  ['liu_bingxing', 'sad', `assets/story/fullbody/liu_bingxing_sad.webp${V}`],
  ['liu_bingxing', 'surprise', `assets/story/fullbody/liu_bingxing_surprise.webp${V}`],
  ['liu_bingxing', 'think', `assets/story/fullbody/liu_bingxing_think.webp${V}`],
  ['lok_gasing', 'angry', `assets/story/fullbody/lok_gasing_angry.webp${V}`],
  ['lok_gasing', 'shy', `assets/story/fullbody/lok_gasing_shy.webp${V}`],
  ['lok_gasing', 'happy', `assets/story/fullbody/lok_gasing_smile.webp${V}`],
  ['lok_gasing', 'surprise', `assets/story/fullbody/lok_gasing_surprise.webp${V}`],
  ['lui_ging', 'serious', `assets/story/fullbody/lui_ging_serious.webp${V}`],
  ['luk_baakyin', 'angry', `assets/story/fullbody/luk_baakyin_angry.webp${V}`],
  ['luk_baakyin', 'sad', `assets/story/fullbody/luk_baakyin_sad.webp${V}`],
  ['luk_baakyin', 'happy', `assets/story/fullbody/luk_baakyin_smile.webp${V}`],
  ['mak_zhendong', 'angry', `assets/story/fullbody/mak_zhendong_angry.webp${V}`],
  ['mak_zhendong', 'happy', `assets/story/fullbody/mak_zhendong_smile.webp${V}`],
  ['ngai_wingnaam', 'angry', `assets/story/fullbody/ngai_wingnaam_angry.webp${V}`],
  ['ngai_wingnaam', 'serious', `assets/story/fullbody/ngai_wingnaam_serious.webp${V}`],
  ['ngai_wingnaam', 'happy', `assets/story/fullbody/ngai_wingnaam_smile.webp${V}`],
  ['ngai_wingnaam', 'surprise', `assets/story/fullbody/ngai_wingnaam_surprise.webp${V}`],
  ['ngai_wingnaam', 'think', `assets/story/fullbody/ngai_wingnaam_think.webp${V}`],
  ['so_jiyan', 'surprise', `assets/story/fullbody/so_jiyan_surprise.webp${V}`],
  ['tsui_poushan', 'serious', `assets/story/fullbody/tsui_poushan_serious.webp${V}`],
  ['vera', 'serious', `assets/story/fullbody/vera_serious.webp${V}`],
];
for (const [sp, cat, exp] of NEW) {
  global.__tier106 = 0;
  ok(`${sp} ${cat} 首選＝${exp.split('/').pop()}`, first(sp, cat) === exp);
}

/* ---- (2) 真實對白句分類（經 map lookup／分類器；句出自 verdict138.json live evidence） ---- */
const LINES = [
  // [講者, 句, 預期分類, beat emotion 欄（有先傳，無傳 null）]
  ['chai_zanhoi', "又係你？企遠少少，唔好阻住我默書。", 'angry', null],
  ['chai_zanhoi', "阿偉，嚟得啱喇，陪我行去化妝間，邊行邊講。", 'shy', null],
  ['chai_zanhoi', "台慶爭位，年年都爭，今年特別勁，邊個企前排、邊個壓軸出場，監製開咗幾次會都未定到。", 'happy', null],
  ['chai_zanhoi', "留低嘅亦唔一定係忠心，可能係驚去到新台冇位企。邊個會走邊個會留，要睇佢最近接咩戲，唔好睇佢把口。", 'think', null],
  ['cheung_hakfan', "我從小到大都是人家讓我先，你沒有讓過，所以我記住你。", 'serious', null],
  ['cheung_tsijun', "嗰個長鏡頭係成套戲個心嚟㗎，剪走咗，佢演嘅嘢就變咗佈景喇。", 'sad', null],
  ['cheung_tsijun', "有戲拍，同拍到戲，係兩回事嚟㗎。企多陣，諗下先答我。", 'think', null],
  ['chung_choning', "有天份冇用功，一樣企唔穩。演技係磨出嚟㗎，唔係跌落嚟㗎。", 'angry', null],
  ['crew_laolinji', "後生仔，星河電視台啲規矩，書本邊會寫㗎。", 'serious', null],
  ['extra_ad_fen', "驕傲少少唔怕，最怕你哋呢班後生，走嘅走、散嘅散。唉，而家成日聽到邊個又話走……唔講喇，飲茶。", 'sad', null],
  ['extra_ad_fen', "你唔同，你肯做啲冇人想做嘅嘢，又唔多聲氣。呢種人，個廠先會記住。", 'serious', null],
  ['ho_sang', "呢排成日有人嚟問我攞主意：走，定唔走。我做呢行廿幾年，清水灣未起電視城嗰陣，我已經喺度。你呢——你有冇諗過走？", 'surprise', null],
  ['ko_chunkit', "何生帶人呀？你就聽話啲啦，佢唔鍾意人臨場至問東問西㗎。", 'shy', null],
  ['ko_chunkit', "邊個負責條安全帶㗎？點解會鬆成咁？快啲搵人上去呀！", 'think', null],
  ['lin_hiu', "不過你要記住，有些助導比較挑剔，你要先打聽清楚他們的喜好，免得白走一趟。", 'serious', null],
  ['lin_hiu', "聽到你這樣說，我很開心。其實我也一直很在意你，只是不敢開口。", 'happy', null],
  ['liu_bingxing', "我阿媽成日話，食呢行飯，最緊要對得住一齊開工嗰班人。之不過一班人入面，有人有屋企要養，有人就嚟移民，你點叫人哋同你一齊搏呀？", 'sad', null],
  ['liu_bingxing', "咦，隔籬枱嗰個後生仔，又係你呀？", 'surprise', null],
  ['liu_bingxing', "呢度啲奶茶，飲咗咁多年都係呢隻味，唔知係茶好，定係我念舊。", 'think', null],
  ['lok_gasing', "冇運行？你都識講。行開啦後生仔，唔好阻住條走廊。", 'angry', null],
  ['lok_gasing', "鍾意還鍾意，但電視台直情唔畀原創上大騷，話怕觀眾唔識欣賞。咁寫歌嗰啲人，係咪要餓死呀？", 'shy', null],
  ['lok_gasing', "唔使你唱到幾勁，嗰段得幾句，你把聲夠實淨就得，我聽過你喺片場哼歌㗎。", 'happy', null],
  ['lok_gasing', "咦，你又嚟呀？坐低啦，唔使企到咁拘謹。", 'surprise', null],
  ['lui_ging', "不過你要記住，我這個人，不會忘記誰在我低谷時走了。", 'serious', null],
  ['luk_baakyin', "臨記咁多個，我記唔晒。唔好阻住走廊。", 'angry', null],
  ['luk_baakyin', "唔好意思，連累你哋。做呢行，俾人愛同俾人鬧，有時係同一班人。", 'sad', "tired"],
  ['luk_baakyin', "……多謝。肯靜靜聽我講晒嘅人，真係冇幾個。", 'happy', null],
  ['mak_zhendong', "收聲。", 'angry', null],
  ['mak_zhendong', "捱到今日，唔係我叻，係我唔敢停。", 'happy', null],
  ['ngai_wingnaam', "走啦。唔好學人哋咁八卦，武行嘅嘢，睇多都冇用。", 'angry', null],
  ['ngai_wingnaam', "後生仔，你嗰場企穩啲，鏡頭掃過嚟嗰陣唔好亂郁。", 'serious', null],
  ['ngai_wingnaam', "你企喺度做咩啫？等我請你飲呀？我而家請唔起喇。", 'happy', null],
  ['ngai_wingnaam', "咦，阿偉嚟咗呀？坐低先啦，唔使企到咁生外。", 'surprise', null],
  ['ngai_wingnaam', "而家人哋一聽我個名，就話諗下先，諗下先即係冇下文㗎喇。", 'think', null],
  ['so_jiyan', "咦，你咪嗰日喺大堂幫我擋鏡頭嗰個？", 'surprise', null],
  ['tsui_poushan', "挺機靈。做臨時演員也要有記性，記住誰是客人、誰是老闆，你才有機會站前一點。", 'serious', null],
  ['vera', "規矩就是：你站在鏡頭前，觀眾第一眼看到的是整體感覺，不是你的演技。", 'serious', null],
];
for (const [sp, text, cat, emo] of LINES) {
  const got = dlg106ResolveCategory({ speakerId: sp, emotion: emo, text });
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
   dlg106ResolveCategory({ speakerId: 'ngai_wingnaam', text: '＠＃＄％︿＆＊' }) === 'neutral');
ok('反證：chai_zanhoi happy 候補鏈 ≠ neutral 候補鏈（分類真係影響揀圖）',
   first('chai_zanhoi', 'happy') !== first('chai_zanhoi', 'neutral'));
// 舊圖唔被搶：同角其他分類首選維持舊檔
ok('反證：chai_zanhoi serious 首選仍係舊圖（新 angry/shy/smile/think 圖冇搶走）',
   first('chai_zanhoi', 'serious') === `assets/story/fullbody/chai_zanhoi_serious.webp${V}`);
ok('反證：cheung_hakfan angry 首選仍係舊圖（新 serious 圖冇搶走）',
   first('cheung_hakfan', 'angry') === `assets/story/fullbody/cheung_hakfan_angry.webp${V}`);
ok('反證：cheung_tsijun smile 首選仍係舊圖（新 sad/think 圖冇搶走）',
   first('cheung_tsijun', 'happy') === `assets/story/fullbody/cheung_tsijun_smile.webp${V}`);
ok('反證：chung_choning smile 首選仍係舊圖（新 angry 圖冇搶走）',
   first('chung_choning', 'happy') === `assets/story/fullbody/chung_choning_smile.webp${V}`);
ok('反證：ho_sang smile 首選仍係舊圖（新 surprise 圖冇搶走）',
   first('ho_sang', 'happy') === `assets/story/fullbody/ho_sang_smile.webp${V}`);
ok('反證：ko_chunkit smile 首選仍係舊圖（新 shy/think 圖冇搶走）',
   first('ko_chunkit', 'happy') === `assets/story/fullbody/ko_chunkit_smile.webp${V}`);
ok('反證：lin_hiu sad 首選仍係舊圖（新 serious/smile 圖冇搶走）',
   first('lin_hiu', 'sad') === `assets/story/fullbody/lin_hiu_sad.webp${V}`);
ok('反證：liu_bingxing smile 首選仍係舊圖（新 sad/surprise/think 圖冇搶走）',
   first('liu_bingxing', 'happy') === `assets/story/fullbody/liu_bingxing_smile.webp${V}`);
ok('反證：lok_gasing serious 首選仍係舊圖（新 angry/shy/smile/surprise 圖冇搶走）',
   first('lok_gasing', 'serious') === `assets/story/fullbody/lok_gasing_serious.webp${V}`);
ok('反證：lui_ging smile 首選仍係舊圖（新 serious 圖冇搶走）',
   first('lui_ging', 'happy') === `assets/story/fullbody/lui_ging_smile.webp${V}`);
ok('反證：luk_baakyin serious 首選仍係舊圖（新 angry/sad/smile 圖冇搶走）',
   first('luk_baakyin', 'serious') === `assets/story/fullbody/luk_baakyin_serious.webp${V}`);
ok('反證：mak_zhendong serious 首選仍係舊圖（新 angry/smile 圖冇搶走）',
   first('mak_zhendong', 'serious') === `assets/story/fullbody/mak_zhendong_serious.webp${V}`);
ok('反證：ngai_wingnaam sad 首選仍係舊圖（新 angry/serious/smile/surprise/think 圖冇搶走）',
   first('ngai_wingnaam', 'sad') === `assets/story/fullbody/ngai_wingnaam_sad.webp${V}`);
ok('反證：so_jiyan smile 首選仍係舊圖（新 surprise 圖冇搶走）',
   first('so_jiyan', 'happy') === `assets/story/fullbody/so_jiyan_smile.webp${V}`);
ok('反證：tsui_poushan shy 首選仍係舊圖（新 serious 圖冇搶走）',
   first('tsui_poushan', 'shy') === `assets/story/fullbody/tsui_poushan_shy.webp${V}`);
ok('反證：vera smile 首選仍係舊圖（新 serious 圖冇搶走）',
   first('vera', 'happy') === `assets/story/fullbody/vera_smile.webp${V}`);
ok('反證：crew_laolinji neutral 首選係 base（得 base 起家，neutral 不變）',
   first('crew_laolinji', 'neutral') === `assets/story/fullbody/crew_laolinji_base.webp${V}`);
ok('反證：extra_ad_fen neutral 首選係 base（得 base 起家，neutral 不變）',
   first('extra_ad_fen', 'neutral') === `assets/story/fullbody/extra_ad_fen_base.webp${V}`);
ok('反證：ngai_wingnaam think 候補鏈次選退 base（首選唔係硬編 base）',
   dlg106Candidates('ngai_wingnaam', 'think')[2].indexOf('ngai_wingnaam_base.webp') >= 0);

console.log(fails.length ? `RESULT FAIL (${fails.length})` : 'RESULT PASS');
process.exit(fails.length ? 1 : 0);
