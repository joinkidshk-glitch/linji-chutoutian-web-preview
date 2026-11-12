// v20a106 DLG106 邏輯測試：對話呈現層——視線表／企位解析／情緒解析（欄→map→分類器）／
// 表情映射／全身候補鏈／覆蓋率統計（同 handoff106/coverage_report.md 對數）。
// 資料一律由 index.html 抽真身（DLG106 模組整段 eval）＋ handoff106 真表對照，唔用手抄副本。
// 反證：(a) 視線表整爛（何生改可翻+望右）→ awi/ho 企位必須變，唔變即 FAIL；
//       (b) map 刪走芬姐旁白條目（clone）→ lookup 必須 miss，證明真係有查 map；
//       (c) 分類器／解析器食垃圾輸入唔准 crash、唔准出表外 category。
// 用法：node tests/test_dlg106_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const root = path.dirname(path.resolve(htmlPath));
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
const D = eval(code + '\n;({DLG106_GAZE,DLG106_EMOTION_MAP,DLG106_CAT_TO_EXPR})');
const GAZE = D.DLG106_GAZE, EMAP = D.DLG106_EMOTION_MAP;
// function 宣告經 eval 已入 scope：dlg106ResolveSides/dlg106ResolveCategory/dlg106Classify/
// dlg106Lookup/dlg106Hash/dlg106Normalize/dlg106Candidates/dlg106ExprFor/dlg106NormCategory/dlg106HasFullbody

/* ---- (1) 視線表：同 handoff106/gaze_table.json 全表一致 ---- */
let handoffGaze = null;
try{ handoffGaze = JSON.parse(fs.readFileSync(path.join(root, 'handoff106', 'gaze_table.json'), 'utf8')); }catch(_e){}
ok('視線表 39 條（31 角＋extra_ad_fen＋awi_s2/s3＋v20a119 DLG119 5 鍵）', Object.keys(GAZE).length === 39);
if(handoffGaze){
  ok('視線表同 handoff gaze_table.json 逐條一致', JSON.stringify(GAZE) === JSON.stringify(handoffGaze));
} else info('handoff106/gaze_table.json 唔喺度（可能已清走）——跳過逐條對照，淨驗分佈');
const dist = { front:0, left:0, right:0 };
let flipTrue = 0;
for(const k of Object.keys(GAZE)){ dist[GAZE[k].gaze]++; if(GAZE[k].flipSafe) flipTrue++; }
ok('視線分佈 front29／left6／right4（v119 加 5 個 front）', dist.front === 29 && dist.left === 6 && dist.right === 4);
ok('flipSafe=true 共 11 條', flipTrue === 11);
ok('何生 left＋唔翻得', GAZE.ho_sang.gaze === 'left' && GAZE.ho_sang.flipSafe === false);
ok('駱家聲 left＋唔翻得（C 實測，唔跟舊 bust 翻轉先例）', GAZE.lok_gasing.gaze === 'left' && GAZE.lok_gasing.flipSafe === false);
ok('阿偉 right＋翻得', GAZE.awi.gaze === 'right' && GAZE.awi.flipSafe === true);
ok('awi_s2 front＋唔翻得／awi_s3 front＋翻得', GAZE.awi_s2.gaze === 'front' && GAZE.awi_s2.flipSafe === false && GAZE.awi_s3.gaze === 'front' && GAZE.awi_s3.flipSafe === true);
ok('每條視線表都有 asym／note', Object.keys(GAZE).every(k => GAZE[k].asym && GAZE[k].note));

/* ---- (2) 企位解析 ---- */
const R = (x, y, t) => dlg106ResolveSides(x, y, t);
let r = R('awi', 'ho_sang');
ok('awi×何生：阿偉左（無翻）、何生右（無翻）', r.left.id === 'awi' && r.left.flip === false && r.right.id === 'ho_sang' && r.right.flip === false);
r = R('awi', 'lok_gasing');
ok('awi×駱家聲：阿偉左、駱右，雙方無翻', r.left.id === 'awi' && r.right.id === 'lok_gasing' && r.left.flip === false && r.right.flip === false);
r = R('awi', 'ko_chunkit');
ok('awi×高俊傑：唔翻得嘅高俊傑優先就左位（原生望右）、阿偉翻轉遷就企右',
   r.left.id === 'ko_chunkit' && r.left.flip === false && r.right.id === 'awi' && r.right.flip === true);
r = R('awi', 'cheung_hakfan');
ok('awi×張克凡：克凡唔翻得＋望左→企右；阿偉企左', r.right.id === 'cheung_hakfan' && r.right.flip === false && r.left.id === 'awi');
ok('雙表外 speaker → null（行舊呈現）', R('extra_unknown', 'generic_crew') === null);
r = R('extra_unknown', 'awi');
ok('一表外一表內 → 獨角（表內嗰個）', !!r.single && r.single.id === 'awi');
r = R('awi', 'awi');
ok('同角 → 獨角', !!r.single && r.single.id === 'awi');
/* 反證 (a)：整爛視線表，結果必須跟住變 */
const sabot = JSON.parse(JSON.stringify(GAZE));
sabot.ho_sang = { gaze:'right', flipSafe:true, asym:'x', note:'x' };
const rs = R('awi', 'ho_sang', sabot);
ok('反證：何生改望右+可翻後 awi/ho 企位／翻轉同真表唔同（解析器真係讀表）',
   JSON.stringify(rs) !== JSON.stringify(R('awi', 'ho_sang')));

/* ---- (3) emotion map：同 handoff 一致＋hash 查表真身驗證 ---- */
let handoffMap = null;
try{ handoffMap = JSON.parse(fs.readFileSync(path.join(root, 'handoff106', 'emotion_map_embed.json'), 'utf8')).map; }catch(_e){}
ok('emotion map 584 條', Object.keys(EMAP).length === 584);
if(handoffMap) ok('emotion map 同 handoff 逐條一致', JSON.stringify(EMAP) === JSON.stringify(handoffMap));
ok('map 值全部係合法代碼 H/S/A/D/U/Y/T', Object.values(EMAP).every(v => 'HSADUYT'.indexOf(v) >= 0));
const FEN = '星河電視台二號錄影廠外走廊，臨記排到成條龍咁長。阿偉攞住張紙本通告企喺隊中間，忽然有隻手伸過嚟，一把搶走咗。';
ok('C 對數向量：芬姐旁白句 lookup = sad（coverage_report 數據註）', dlg106Lookup(FEN, EMAP) === 'sad');
ok('hash 格式 8 位小寫 hex＋決定性', /^[0-9a-f]{8}$/.test(dlg106Hash(FEN)) && dlg106Hash(FEN) === dlg106Hash(FEN));
ok('正規化刪空白／標點＋細寫', dlg106Normalize(' Ab ，。C ') === 'abc');
/* 反證 (b)：clone map 刪條目 → lookup miss */
const cloneMap = Object.assign({}, EMAP);
delete cloneMap[dlg106Hash(FEN)];
ok('反證：刪走條目後 lookup miss（查表真係查嗰條）', dlg106Lookup(FEN, cloneMap) === null);

/* ---- (4) 解析次序：欄 → map → 分類器 → neutral ---- */
ok('beat emotion 欄行先（蓋過 map 命中句）', dlg106ResolveCategory({ emotion:'happy', text:FEN }) === 'happy');
ok('舊 emotion 詞彙正規化 worried→think', dlg106ResolveCategory({ emotion:'worried', text:'一句冇關鍵字嘅平靜說話' }) === 'think');
ok('舊 expression 詞彙正規化 frown→serious', dlg106ResolveCategory({ expression:'frown', text:'一句冇關鍵字嘅平靜說話' }) === 'serious');
ok('冇欄就查 map（芬姐句→sad）', dlg106ResolveCategory({ text:FEN }) === 'sad');
ok('map miss 就行分類器（嬲句→angry）', dlg106ResolveCategory({ text:'你再講！豈有此理，收聲！' }) === 'angry');
ok('全 miss＋冇關鍵字 → neutral', dlg106ResolveCategory({ text:'今日天氣幾好，我哋出發去片場。' }) === 'neutral');
/* 反證 (c)：垃圾輸入 */
ok('反證：垃圾 category 認唔到回空', dlg106NormCategory('bogus_cat') === '');
ok('反證：空輸入 resolveCategory 回 neutral 唔 crash', dlg106ResolveCategory({}) === 'neutral' && dlg106ResolveCategory({ text:'' }) === 'neutral');

/* ---- (5) category→expr 映射（規格逐字） ---- */
const EXP = { happy:'smile', neutral:'base', serious:'serious', sad:'sad', surprise:'surprise', shy:'shy', think:'think', angry:'angry' };
ok('category→expr 八項逐字啱', Object.keys(EXP).every(k => dlg106ExprFor(k) === EXP[k] && D.DLG106_CAT_TO_EXPR[k] === EXP[k]));

/* ---- (6) 全身候補鏈＋阿偉階段 ---- */
let c = dlg106Candidates('ho_sang', 'sad');
ok('候補：expr 先、base 後、?v=20a106', c[0] === 'assets/story/fullbody/ho_sang_sad.webp?v=20a106' && c.some(u => u === 'assets/story/fullbody/ho_sang_base.webp?v=20a106') && c.every(u => u.indexOf('?v=20a106') > 0));
ok('neutral 候補直入 base（冇 smile 混入）', dlg106Candidates('ho_sang', 'neutral')[0] === 'assets/story/fullbody/ho_sang_base.webp?v=20a106');
global.__tier106 = 2;
c = dlg106Candidates('awi', 'think');
ok('阿偉主角期（tier2）行 awi_s2 圖組＋退 awi base 兜底', c[0].indexOf('assets/story/fullbody/awi_s2_think') === 0 && c.some(u => u === 'assets/story/fullbody/awi_base.webp?v=20a106'));
global.__tier106 = 3;
ok('阿偉天王期（tier3）行 awi_s3 圖組', dlg106Candidates('awi', 'happy')[0].indexOf('assets/story/fullbody/awi_s3_smile') === 0);
global.__tier106 = 0;
ok('阿偉臨記期行 awi 圖組', dlg106Candidates('awi', 'happy')[0].indexOf('assets/story/fullbody/awi_smile') === 0);
ok('表外 speaker 冇候補（行舊呈現）', dlg106Candidates('extra_unknown', 'happy').length === 0 && dlg106HasFullbody('extra_unknown') === false);

/* ---- (7) 覆蓋率：跑晒遊戲內對白（ENC 逐星＋主線 beats），統計解析結果 ----
   口徑：解析到非 neutral category ＝嗰句會出非 base 表情（未計資產有冇嗰款）。
   C coverage_report 嘅 403/593＝68.0% 係「資產精確覆蓋」（類別有同名圖先計），
   要等 A 資產入庫先計得；兩者唔同口徑，呢度印埋 C 數字對數，唔冒充相等。 */
const NAME2ID = { '阿偉':'awi','何生':'ho_sang','Vera':'vera','林曉晴':'lin_hiu','張子駿':'cheung_tsijun','高俊傑':'ko_chunkit','周采兒':'chow_choiyi','高文瀚':'gao_wenhan','藍若曦':'lan_ruoxi','張克凡':'cheung_hakfan','雷勁':'lui_ging','鄭威廉':'cheng_william','唐素雲':'tong_souwan','方小龍':'fong_siulung','徐寶珊':'tsui_poushan','莫少輝':'mok_siufai','金九':'uncle_kim','鄧麗萍':'tang_laiping','陸柏言':'luk_baakyin','廖炳星':'liu_bingxing','魏詠男':'ngai_wingnaam','葉敏芝':'yip_manji','麥震東':'mak_zhendong','駱家聲':'lok_gasing','彭少祺':'pang_siuki','鍾楚凝':'chung_choning','顧明輝':'gu_mingfai','蘇芷茵':'so_jiyan','齊鎮海':'chai_zanhoi','程天諾':'ching_tinlok','副導演芬姐':'extra_ad_fen' };
const stats = {}; let totLines = 0, totNonNeutral = 0, totMapHit = 0;
function feed(sid, text, emotionField){
  if(!sid || !GAZE[sid] || typeof text !== 'string' || !text.trim()) return;
  const cat = dlg106ResolveCategory({ emotion:emotionField, text });
  const s = stats[sid] || (stats[sid] = { n:0, nn:0 });
  s.n++; totLines++;
  if(dlg106Lookup(text, EMAP)) totMapHit++;
  if(cat !== 'neutral'){ s.nn++; totNonNeutral++; }
}
/* ENC 對白塊（ENC79/83/84_DLG_<star>）：tuple ["S"|"A"|"N","..."] */
for(const m of html.matchAll(/const ENC(?:79|83|84)_DLG_(\w+) =/g)){
  const sid = m[1] === 'yip_manzi' ? 'yip_manji' : m[1];
  const seg = html.slice(m.index, m.index + 160000);
  const end = seg.search(/\nconst ENC|\n\/\* =====/);
  const body = end > 0 ? seg.slice(0, end) : seg;
  for(const t of body.matchAll(/\[\s*"(S|A|N)"\s*,\s*"((?:[^"\\]|\\.)*)"\s*\]/g)){
    if(t[1] === 'N') continue;
    feed(t[1] === 'A' ? 'awi' : sid, t[2].replace(/\\"/g, '"'));
  }
}
/* 主線 beats：lines:[...] 就近歸屬 speaker/speakerId */
for(const m of html.matchAll(/lines:\s*\[((?:"(?:[^"\\]|\\.)*"\s*,?\s*)+)\]/g)){
  const back = html.slice(Math.max(0, m.index - 420), m.index);
  const idAll = [...back.matchAll(/speakerId:\s*"([^"]+)"/g)];
  const spAll = [...back.matchAll(/speaker:\s*"([^"]+)"/g)];
  const idm = idAll.length ? idAll[idAll.length - 1] : null;
  const spm = spAll.length ? spAll[spAll.length - 1] : null;
  let sid = null;
  if(idm) sid = idm[1] === 'agent' ? 'ho_sang' : (idm[1] === 'player' ? 'awi' : idm[1]);
  else if(spm) sid = NAME2ID[spm[1]] || null;
  if(!sid) continue;
  const emoM = back.match(/emotion:\s*"([^"]+)"/);
  for(const t of m[1].matchAll(/"((?:[^"\\]|\\.)*)"/g)) feed(sid, t[1].replace(/\\"/g, '"'), emoM ? emoM[1] : undefined);
}
info('覆蓋語料：名冊對白 ' + totLines + ' 句；解析非 neutral ' + totNonNeutral + ' 句（' + (totLines ? (100 * totNonNeutral / totLines).toFixed(1) : '0') + '%）；map 直命中 ' + totMapHit + ' 句');
ok('語料夠大（>600 句，證明真係跑晒對白唔係抽樣）', totLines > 600);
ok('非 neutral 解析率 ≥15%（分類有實質作用）', totLines > 0 && totNonNeutral / totLines >= 0.15);
ok('map 命中 >80 句（584 表真係食到遊戲對白）', totMapHit > 80);
const zeroCov = Object.keys(stats).filter(k => stats[k].nn === 0).sort();
const noLines = Object.keys(GAZE).filter(k => k !== 'awi_s2' && k !== 'awi_s3' && !stats[k]).sort();
info('逐角覆蓋：' + Object.keys(stats).sort().map(k => k + ' ' + stats[k].nn + '/' + stats[k].n).join('；'));
info('零解析覆蓋（有對白但全 neutral）：' + (zeroCov.join(', ') || '（無）'));
info('語料未抽到對白嘅角：' + (noLines.join(', ') || '（無）') + '（可能只喺 content pack／結果 beats 入面，抽取口徑所限）');
info('C 對數參考：資產精確覆蓋 403/593=68.0%；零精確覆蓋 9 角＝cheung_tsijun, fong_siulung, gao_wenhan, tang_laiping, extra_ad_fen, uncle_kim, kwan_hoimei, cheng_william, mok_siufai（資產口徑，等 A 入庫後由 static 測試嘅資產掃描覆核）');
ok('阿偉非 neutral 解析 >50 句（主角表情有得換）', (stats.awi || { nn:0 }).nn > 50);

console.log(fails.length ? ('RESULT FAIL (' + fails.length + ')') : 'RESULT PASS');
process.exit(fails.length ? 1 : 0);
