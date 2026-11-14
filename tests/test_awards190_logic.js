// v20a211 B1 resync：雙幾何（矮 480×432／高 480×540，HS211／HSC211＝×1.25）——短基準值不變，高 viewport 按比例換算；見 NOTES_V20A211。
// v20a190 修 v187 設計 review 新 C1・邏輯測試：
// 新 C1：v187 為咗避白牌將海報推到底，panel 上半留 46–48% 空暗底（932 空 273px／700 空 234px）。
// 修法（用戶 2026-11-13 19:40 拍板：海報置中返少少／panel 縮短）：panel 縮短貼底——
//   overlay align-items stretch→flex-end（panel 高改做內容高，唔再全高），海報＋cap 位置唔郁。
// 關鍵機制（探針證實，唔係估）：
//   (a) 淨係改 flex-end 唔得——img 嘅 max-height:40% 會對住而家內容高嘅 panel 解（不定→失效），
//       海報脹到 284.8 高（闊 273.1），頂會撞返白牌；
//   (b) 轉 40cqh 亦唔啱——會高 8px（228 vs 220），932 clearance 跌到 28px；
//   (c) 正確係 calc(40cqh - 8px)＋overlay container-type:size：40cqh＝舊 40%×overlay 高，
//       −8px＝扣返 panel 上下 padding 各 10px 嘅 40%（0.4×20；全域 border-box 下舊 cap＝
//       40%×(panel 高−20)），兩 viewport 逐 px 等價（932 cap 220／700 cap 193.6，探針核實）。
// 驗收（實駕量度）：panel 空佔比 47.9%→3.3%（932）／46.3%→3.6%（700）；海報盒唔郁
//   （932 img 396–616／700 img 390–583）；clearance 36／24 唔跌；底罅 77 唔郁；面完整。
// 唔郁守衛：B1 地板 y274–372／FLOOR 314（v20a207 B2）；C2 卡罅 24px／角標 10px；C3 out 留人；C4 walkup y＋6；
//   C5 glamour 下移 124px（trade-off，glamour-hide display:none）；C6 glyph −110（2.6 邏輯罅）。
// 唔郁：fellows 池／對手加權／贏線 0.875／報紙流程／6 beats 順序；唔直改 content pack JSON。
// 反證：對 pristine main dcf1b72 行 → 新 C1 斷言全部 FAIL（唔 crash）；守衛 pristine 應 PASS。
// 用法：node tests/test_awards190_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }
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
function cssRule(sel){
  const i = html.indexOf(sel + '{');
  if(i < 0) return '';
  const j = html.indexOf('}', i);
  return j >= 0 ? html.slice(i, j + 1) : '';
}

let baseSrc, beatsSrc, playSrc;
try{
  baseSrc = extractFn('awards181DrawBase');
  beatsSrc = extractFn('awards62CeremonyBeats');
  playSrc = extractFn('awards62PlayCeremony');
}catch(e){
  console.log('FAIL v190 舞台函數抽唔到（' + e.message + '，pristine 預期）');
  console.log('\nFAILED: 1');
  process.exit(1);
}
eval(baseSrc);
var iconHtml112 = function(s){ return s; };
var poster59Path = function(){ return 'poster.png'; };
eval(beatsSrc);

const glamCss = cssRule('.awd63-glamour');
const panelCss = cssRule('.awd63-glamour-panel');
const panelImgCss = cssRule('.awd63-glamour-panel>img');

/* ================= 新 C1：panel 縮短貼底（CSS 機制） ================= */
ok('C1 overlay 改 align-items:flex-end（panel 貼底，唔再 stretch 全高）',
  glamCss.includes('align-items:flex-end') && !glamCss.includes('align-items:stretch'));
ok('C1 overlay 有 container-type:size（cqh 以 overlay 高計，唔係 viewport）',
  glamCss.includes('container-type:size'));
ok('C1 海報 cap 轉 calc(40cqh - 8px)（舊 40% 唔再出現；裸 40cqh 亦唔准——會高 8px）',
  panelImgCss.includes('max-height:calc(40cqh - 8px)') && !panelImgCss.includes('max-height:40%') &&
  !panelImgCss.includes('max-height:40cqh'));
ok('C1 海報 max-width 88% 唔郁（闊 cap 仲在，防闊海報）',
  panelImgCss.includes('max-width:88%'));
ok('C1 海報金框＋光暈唔郁', panelImgCss.includes('border:4px solid #f2c14e') &&
  panelImgCss.includes('box-shadow:0 0 34px rgba(242,193,78,.45)'));
ok('C1 panel 闊 44%＋0.93 暗底＋column＋flex-end＋gap 8＋padding 10/12 唔郁',
  panelCss.includes('flex:0 0 44%') && panelCss.includes('rgba(10,6,18,.93)') &&
  panelCss.includes('flex-direction:column') && panelCss.includes('justify-content:flex-end') &&
  panelCss.includes('gap:8px') && panelCss.includes('padding:10px 12px'));
ok('C1 overlay 仲係 absolute top:0／left:0／width:100%＋aspect 480/432＋pointer-events:none（v20a207 B2）',
  glamCss.includes('position:absolute') && glamCss.includes('top:0') && glamCss.includes('left:0') &&
  glamCss.includes('width:100%') && glamCss.includes('aspect-ratio:480/432') &&
  glamCss.includes('pointer-events:none'));
ok('C1 cap 字體唔郁（19px／行高 1.55，兩行＝58.9px——計數用）',
  cssRule('.awd63-glamour .cap').includes('font-size:19px') &&
  cssRule('.awd63-glamour .cap').includes('line-height:1.55'));

/* ================= 新 C1：逐 px 計數（932／700，CSS px；v187 實測＋探針） ================= */
// panel 底＝frame 頂＋overlay 高（932：123＋570＝693；700：156＋504＝660）；牌底 360／366（v187 實測）。
// 內容高＝padding 上 10＋img cap＋gap 8＋cap 兩行 58.9＋padding 下 10；空＝padding 上 10px。
const CAP_H = 19 * 1.55 * 2; // 58.9
function geom(overlayH, panelBottom, boardBottom){
  const cap = 0.4 * overlayH - 8; // calc(40cqh - 8px) 嘅用值
  const contentH = 10 + cap + 8 + CAP_H + 10;
  const panelTop = panelBottom - contentH;
  const imgTop = Math.round(panelTop + 10);
  return { cap, contentH, panelTop, imgTop,
    clearance: imgTop - boardBottom, emptyRatio: 10 / contentH,
    bottomGap: Math.round(8 + CAP_H + 10) };
}
const g932 = geom(570, 693, 360), g700 = geom(504, 660, 366);
ok('C1 932 cap＝0.4×570−8＝220（同 v187 舊 cap 逐 px 等價）', g932.cap === 220);
ok('C1 700 cap＝0.4×504−8＝193.6（同 v187 舊 cap 逐 px 等價）', Math.abs(g700.cap - 193.6) < 0.01);
ok('C1 932 海報頂 396、離牌底 36px（v187 實測下限，唔准細過）',
  g932.imgTop === 396 && g932.clearance === 36);
ok('C1 700 海報頂 390、離牌底 24px（v187 實測下限，唔准細過）',
  g700.imgTop === 390 && g700.clearance === 24);
ok('C1 932 空佔比 10／306.9＝3.3% ≤25%（舊 47.9%）', g932.emptyRatio <= 0.25 && Math.abs(g932.emptyRatio - 0.033) < 0.002);
ok('C1 700 空佔比 10／280.5＝3.6% ≤25%（舊 46.3%）', g700.emptyRatio <= 0.25 && Math.abs(g700.emptyRatio - 0.036) < 0.002);
ok('C1 海報底到 panel 底 77px 唔郁（caption 嗰段保住，唔變新空位）',
  g932.bottomGap === 77 && g700.bottomGap === 77);
ok('C1 海報盒唔郁：932 img 396–616（220 高）、700 img 390–583（193.6 高）',
  g932.imgTop + 220 === 616 && g700.imgTop + 193.6 === 583.6);
ok('C1 panel 底唔郁（932：693；700：660——淨係頂收上嚟）',
  Math.round(g932.panelTop + g932.contentH) === 693 && Math.round(g700.panelTop + g700.contentH) === 660);
/* 高身海報 guard：0.5 比例海報喺新 cap 下闊＝(220−8)×0.5＝106，細過 max-width 88%（273），
   高 cap 照樣箍住，唔會脹到 392 撞牌（裸 40% 失效嗰陣就會）。 */
ok('C1 高身海報（0.5 比例）cap 下闊 106px＜max-width 273px（唔脹唔撞牌）',
  (220 - 8) * 0.5 === 106 && 106 < 0.88 * (334.4 - 24));

/* ================= 唔郁守衛：其餘六項 ================= */
ok('守衛 B1 地板 y274–372（#d9a75f，深 98px；v20a207 B2）', baseSrc.includes('228 / 360') && baseSrc.includes('310 / 360'));
ok('守衛 B1 觀眾席 y379–432（#120c20，高 53；v20a207 B2）', baseSrc.includes('316 / 360'));
ok('守衛 B1 FLOOR＝314（v20a207 B2）', playSrc.includes('const FLOOR = Math.round(314 * HSC211)'));
const cardsCss = cssRule('.awd63-cards');
const gapM = cardsCss.match(/gap:\s*(\d+)px/);
ok('守衛 C2 卡罅 gap 24px（角標 clearance 10px）', gapM && Number(gapM[1]) === 24);
const outIdx = playSrc.indexOf('if(id === "out"){');
const outBlock = outIdx >= 0 ? playSrc.slice(outIdx, playSrc.indexOf('};', outIdx)) : '';
ok('守衛 C3 out 分支照畫人物、alpha 1−step×0.25', outBlock.includes('drawFigure') && outBlock.includes('1 - step * 0.25'));
const walkIdx = playSrc.indexOf('if(id === "walkup"){');
const walkBlock = walkIdx >= 0 ? playSrc.slice(walkIdx, playSrc.indexOf('if(id === "out"){', walkIdx)) : '';
ok('守衛 C4 walkup 行緊 y＋6（只一處）', walkBlock.includes('y: 6') && (walkBlock.match(/y: 6/g) || []).length === 1);
ok('守衛 C5 glamour-hide 仲係 display:none（v174 trade-off：下移 124px 唔郁）',
  cssRule('.awd63-cards.glamour-hide').includes('display:none'));
ok('守衛 C6 燕尾服 glyph −129 兩處、舊 −112 唔見（v20a207 B2）', playSrc.includes('FLOOR + fp.y - Math.round(129 * HSC211)') && playSrc.includes('FLOOR - Math.round(129 * HSC211)') && !playSrc.includes('- 112'));
ok('守衛 C6 牌底 179.3 到 glyph 頂 185 留 5.7 邏輯罅（v20a207 B2）', Math.abs((314 - 129) - 179.3 - 5.7) < 0.01);

/* ================= 唔郁守衛：流程／版本 ================= */
const beatsWon = awards62CeremonyBeats({ displayName: '星河電視獎', bestOutcome: 'won', repWork62: '長篇劇',
  categories: [{ label: '最佳男主角', outcome: 'won', repWorkTitle: '長篇劇' }] });
ok('守衛 得獎 beats 全長 13350ms 唔郁', beatsWon.reduce((a, b) => a + b.ms, 0) === 13350);
ok('守衛 walkup 2200ms、glamour 1800ms、comfort 2600ms 唔郁',
  beatsWon.find(b => b.id === 'walkup').ms === 2200 && beatsWon.find(b => b.id === 'glamour').ms === 1800);
ok('守衛 6 beats 順序唔郁（reveal→walkup→glamour→out）',
  beatsSrc.indexOf('id: "reveal"') < beatsSrc.indexOf('id: "walkup"') &&
  beatsSrc.indexOf('id: "walkup"') < beatsSrc.indexOf('id: "glamour"'));
ok('守衛 fanfare＋掌聲仲在', playSrc.includes('awards160PlayWinAudio()'));
ok('守衛 SAVE key／softRev／?v= 唔郁', html.includes('starVolunteer_map_v19w') && html.includes('var SOFT_REV = "s107"') && html.includes('?v=20a10'));

console.log(fails.length ? ('\nFAILED: ' + fails.length) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
