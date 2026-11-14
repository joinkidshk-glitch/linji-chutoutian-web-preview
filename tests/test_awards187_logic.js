// v20a187 修 v181 設計 review B1＋C1–C6・邏輯測試：
// B1：地板收窄 y228–310（深 82px＝22.8% 高；v20a207 B2 resync：地板 y274–372，深 98px＝22.7% 高；
//     地板深／人物高 98/108≈0.91、腳底以下空地板 58px＝0.54 倍，
//     貼近參考圖 0.64／0.43 方向；舊 y200–334／134px 係工人 NOTES 讀錯參考圖，見 review §4 B1）。
//     幕布拉長到 y274、燈架跟到 y274、觀眾席 y379–432（前緣 372–379 之下，深 53px，光點照舊）。
// C1：glamour 海報改做下半置中（panel justify-content:flex-end＋img max-height 60%→40%），海報頂唔再壓白牌。
// v20a190 新 C1：panel 縮短貼底（overlay align-items flex-end＋container-type:size），img cap 轉等價
//   calc(40cqh - 8px)——舊 40% 會對住內容高嘅 panel 失效；以下 C1 斷言跟住更新，結論（海報頂唔壓牌）不變。
// C2：卡罅 8→24px，「你」徽（右出 7px）同隔籬卡 🏆 徽（左出 7px）中間留 10px。
// C3：out beat 照畫人物、跟 overlay 一齊暗落（alpha＝1−step×0.25；won 只留燕尾服阿偉，其餘跟 comfort 暗度）。
// C4：walkup 行緊嗰陣 y＋6（行前一格，掠過左邊提名人有前後層次），行完換燕尾服 y 歸 0。
// C5：glamour frame 下移 124px 係 v174 已接受 trade-off（卡列 display:none 殺死位）——B1 唔郁 frame 高，
//     評估後 keep：本檔只釘死 trade-off 仲在（glamour-hide display:none），唔當未修。
// C6：獎盃 glyph −112→−110（牌底 149.4 到 glyph 頂 152，留 2.6 邏輯罅；glyph 底 170 離頭頂 173 仲有 3px）。
// 唔郁守衛：FLOOR 314（v20a207 B2）／企位／beats 全長／fanfare／彩紙／SAVE key／softRev／?v=。
// 反證：對 pristine main b1b6092 行 → B1／C1／C2／C3／C4／C6 新斷言全部 FAIL（唔 crash）；守衛 pristine 應 PASS。
// 用法：node tests/test_awards187_logic.js [path-to-index.html]
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

function mockCtx(){
  const calls = [];
  const ctx = {
    fillStyle: '', strokeStyle: '', lineWidth: 1, _tx: 0,
    save(){ calls.push(['save']); },
    restore(){ calls.push(['restore']); },
    translate(x, y){ this._tx = x; calls.push(['translate', x, y]); },
    fillRect(x, y, w, h){ calls.push(['fillRect', x, y, w, h, this.fillStyle]); },
    beginPath(){ calls.push(['beginPath']); },
    moveTo(x, y){ calls.push(['moveTo', x, y]); },
    lineTo(x, y){ calls.push(['lineTo', x, y]); },
    stroke(){ calls.push(['stroke']); },
    fill(){ calls.push(['fill']); },
    ellipse(){ calls.push(['ellipse']); }
  };
  return { ctx, calls };
}
function rects(calls, style){
  return calls.filter(c => c[0] === 'fillRect' && c[5] === style);
}

let baseSrc, beatsSrc, playSrc;
try{
  baseSrc = extractFn('awards181DrawBase');
  beatsSrc = extractFn('awards62CeremonyBeats');
  playSrc = extractFn('awards62PlayCeremony');
}catch(e){
  console.log('FAIL v187 舞台函數抽唔到（' + e.message + '，pristine 預期）');
  console.log('\nFAILED: 1');
  process.exit(1);
}
eval(baseSrc);
var iconHtml112 = function(s){ return s; };
var poster59Path = function(){ return 'poster.png'; };
eval(beatsSrc);

/* ================= B1：程式舞台幾何（mock ctx） ================= */
let m = mockCtx();
awards181DrawBase(m.ctx, 480, 432, 0); /* v20a207 B2：用實況 H=432 驗新幾何（舊 360） */
const R = m.calls;
const floorRect = rects(R, '#d9a75f').find(r => r[3] === 496);
const FLOOR_TOP = floorRect ? floorRect[2] : -1, FLOOR_H = floorRect ? floorRect[4] : -1;
const FLOOR_BOT = FLOOR_TOP + FLOOR_H, FEET = 314, PERSON_H = 108; /* 人物高約 108px（dispH 136×102/128，v20a207 B2 實測） */
ok('B1 地板 y274–372（#d9a75f，深 98px；v20a207 B2）', FLOOR_TOP === 274 && FLOOR_H === 98);
ok('B1 地板深 98px＝22.7% 高（20–26% 帶，貼近參考圖 ~15% 方向；舊 134px／37.2% 唔再出現）',
  Math.abs(FLOOR_H / 432 - 0.227) < 0.005 && !rects(R, '#d9a75f').some(r => r[4] === 134));
ok('B1 地板深／人物高 98/108≈0.91（0.85–1.00；舊 1.51）', FLOOR_H / PERSON_H >= 0.85 && FLOOR_H / PERSON_H <= 1.00);
ok('B1 腳底以下空地板 372−314＝58px＝0.54 倍人物高（0.48–0.60；舊 72px／0.81）',
  (FLOOR_BOT - FEET) === 58 && (FLOOR_BOT - FEET) / PERSON_H >= 0.48 && (FLOOR_BOT - FEET) / PERSON_H <= 0.60);
ok('B1 幕布淺米底 y43–274（#f2e8d5，高 231，地板頂唔留生口；v20a207 B2）',
  rects(R, '#f2e8d5').some(r => r[1] === -8 && r[2] === 43 && r[3] === 496 && r[4] === 231));
ok('B1 側幕深紅落到 y274（#7a1f24，高 274；v20a207 B2）', rects(R, '#7a1f24').every(r => r[4] === 274));
ok('B1 燈架鐵杆落到 y274（#23232c，y48 高 226；v20a207 B2）',
  rects(R, '#23232c').some(r => r[1] === 12 && r[2] === 48 && r[4] === 226) &&
  rects(R, '#23232c').some(r => r[1] === 452 && r[2] === 48 && r[4] === 226));
ok('B1 地板前緣深木邊 y372–379（#5a3a1e，高 7；v20a207 B2）', rects(R, '#5a3a1e').some(r => r[2] === 372 && r[4] === 7));
ok('B1 暗觀眾席 y379–432（#120c20，高 53，前緣之下；舊 y340／高 20 唔再出現）',
  rects(R, '#120c20').some(r => r[2] === 379 && r[4] === 53) && !rects(R, '#120c20').some(r => r[2] === 340));
ok('B1 觀眾席光點散開成帶（金色 3px ≥4 粒，全部 y 379–432；v20a207 B2）',
  rects(R, 'rgba(255,233,143,0.85)').filter(r => r[3] === 3 && r[4] === 3 && r[2] >= 379 && r[2] <= 432).length >= 4);
ok('B1 冇圓台／講台（base 內 ellipse 0 次）', R.filter(c => c[0] === 'ellipse').length === 0);

/* ================= C1：glamour 海報下半置中（CSS） ================= */
function cssRule(sel){
  const i = html.indexOf(sel + '{');
  if(i < 0) return '';
  const j = html.indexOf('}', i);
  return j >= 0 ? html.slice(i, j + 1) : '';
}
const panelCss = cssRule('.awd63-glamour-panel');
const panelImgCss = cssRule('.awd63-glamour-panel>img');
ok('C1 glamour panel 改 flex-end（海報＋cap 沉底，唔再垂直置中頂住牌）', panelCss.includes('justify-content:flex-end'));
ok('C1 海報 max-height 40%→calc(40cqh - 8px)（v20a190 等價轉換；max-width 88% 唔郁）',
  panelImgCss.includes('max-height:calc(40cqh - 8px)') && panelImgCss.includes('max-width:88%') && !panelImgCss.includes('max-height:40%') && !panelImgCss.includes('max-height:60%'));
/* 最差情況計數（邏輯單位）：panel 高 432；img ≤172.8；cap 兩行＋padding＋gap 預 45 → 海報頂 ≥214 ＞ 牌底 179.3（v20a207 B2） */
ok('C1 海報頂計數 ≥214 邏輯＞牌底 179.3（432−172.8−45）', (432 - 0.40 * 432 - 45) > 179.3);
ok('C1 panel 闊 44%＋0.93 暗底唔郁（v20a190：全高改做貼底縮短，見 test_awards190；牌 z-index 3 照喺上面）',
  panelCss.includes('flex:0 0 44%') && panelCss.includes('rgba(10,6,18,.93)'));

/* ================= C2：卡罅 8→24px（CSS＋角標計數） ================= */
const cardsCss = cssRule('.awd63-cards');
const gapM = cardsCss.match(/gap:\s*(\d+)px/);
const gap = gapM ? Number(gapM[1]) : -1;
ok('C2 卡罅 gap 24px（舊 8px 唔再出現）', gap === 24);
ok('C2 角標唔撞：gap 24 − 你徽右出 7 − 🏆 左出 7 ＝ 10px 罅', gap - 7 - 7 === 10);
ok('C2 卡列總闊 4×88＋3×24＝424px ≤ 760 框', 4 * 88 + 3 * gap <= 760);
ok('C2 🏆 仲喺左上角（left:-7，唔搬去右上角——免得同「你」徽爭同一個 ::after／同邊）',
  cssRule('.awd63-card.win::after').includes('left:-7px'));
ok('C2 「你」徽仲喺右上角（right:-7 唔郁）', cssRule('.awd63-card.me::after').includes('right:-7px'));

/* ================= C3：out beat 照畫人物（play 原文） ================= */
const outIdx = playSrc.indexOf('if(id === "out"){');
const outBlock = outIdx >= 0 ? playSrc.slice(outIdx, playSrc.indexOf('};', outIdx)) : '';
ok('C3 out 分支畫人物（唔再淨係畫 overlay）', outBlock.includes('drawFigure'));
ok('C3 人物 alpha 跟 step 遞減（1−step×0.25，overlay 步進 0.25 唔郁）',
  outBlock.includes('1 - step * 0.25') && outBlock.includes('step * 0.25'));
ok('C3 won 只留燕尾服阿偉（跟 glamour 一致，tuxedo）', outBlock.includes('tuxedo: true') && outBlock.includes('best === "won"'));
ok('C3 其餘跟 comfort 暗度（player 1／得主 0.85／其他 0.7 再 ×fa）',
  outBlock.includes('winnerSlot ? 0.85 : 0.7'));
ok('C3 out 仲係 500ms（唔加 beat）', beatsSrc.includes('id: "out", ms: 500'));

/* ================= C4：walkup y＋6（play 原文） ================= */
const walkIdx = playSrc.indexOf('if(id === "walkup"){');
const walkBlock = walkIdx >= 0 ? playSrc.slice(walkIdx, playSrc.indexOf('if(id === "out"){', walkIdx)) : '';
ok('C4 walkup 行緊 y＋6（行前一格）', walkBlock.includes('y: 6'));
ok('C4 行完換燕尾服 y 歸 0（企定嗰句 x: targetX，冇 y）',
  walkBlock.includes('x: targetX, hold: true') && (walkBlock.match(/y: 6/g) || []).length === 1);
ok('C4 walkup 仲係由台左 −40 行 1400ms（路徑唔郁，只加 y）',
  walkBlock.includes('-40 + (targetX + 40) * wp') && walkBlock.includes('beatElapsed / 1400'));

/* ================= C5：glamour 下移 trade-off 保留（評估結論） ================= */
ok('C5 glamour-hide 仲係 display:none（v174 trade-off 保留：B1 唔郁 frame 高，死位唔返嚟）',
  cssRule('.awd63-cards.glamour-hide').includes('display:none'));
ok('C5 syncGlamour 仲係同一個 choke point toggle glamour-hide',
  playSrc.includes("cardsEl.classList.toggle(\"glamour-hide\""));

/* ================= C6：glyph −110（play 原文＋計數） ================= */
ok('C6 燕尾服 glyph −129 兩處（reveal 行前＋walkup 捧杯；v20a207 B2）',
  playSrc.includes('FLOOR + fp.y - 129') && playSrc.includes('FLOOR - 129'));
ok('C6 舊 −112 唔再出現（頒獎禮範圍）', !playSrc.includes('- 112'));
ok('C6 牌底 179.3 到 glyph 頂 185 留 5.7 邏輯罅（v20a207 B2）', Math.abs((314 - 129) - 179.3 - 5.7) < 0.01);
ok('C6 glyph 底 203 離頭頂 206 仲有 3px（唔掂頭；v20a207 B2）', (314 - 129 + 18) === 203 && 206 - 203 === 3);
ok('C6 對手胸前 glyph −61（v20a207 B2）', playSrc.includes('FLOOR + fp.y - 61'));

/* ================= 唔郁守衛 ================= */
ok('守衛 FLOOR＝314（v20a207 B2）', playSrc.includes('const FLOOR = 314'));
ok('守衛 4 slots 60／180／300／420、gallery 75／240／405 唔郁',
  playSrc.includes('240 + (i - (slots.length - 1) / 2) * 120') && playSrc.includes('[75, 240, 405]'));
const beatsWon = awards62CeremonyBeats({ displayName: '星河電視獎', bestOutcome: 'won', repWork62: '長篇劇',
  categories: [{ label: '最佳男主角', outcome: 'won', repWorkTitle: '長篇劇' }] });
ok('守衛 得獎 beats 全長 13350ms 唔郁', beatsWon.reduce((a, b) => a + b.ms, 0) === 13350);
ok('守衛 walkup 2200ms、glamour 1800ms、comfort 2600ms 唔郁',
  beatsWon.find(b => b.id === 'walkup').ms === 2200 && beatsWon.find(b => b.id === 'glamour').ms === 1800);
const beatsNom = awards62CeremonyBeats({ displayName: '星河電視獎', bestOutcome: 'nominated', repWork62: '長篇劇',
  categories: [{ label: '最佳男主角', outcome: 'nominated', repWorkTitle: '長篇劇' }] });
ok('守衛 入圍 comfort 2600ms 唔郁', beatsNom.find(b => b.id === 'comfort').ms === 2600);
ok('守衛 fanfare＋掌聲仲在（揭曉觸發）', playSrc.includes('awards160PlayWinAudio()'));
ok('守衛 彩紙 M5 仲在', playSrc.includes('syncConfetti149'));
ok('守衛 SAVE key／softRev／?v= 唔郁', html.includes('starVolunteer_map_v19w') && html.includes('var SOFT_REV = "s107"') && html.includes('?v=20a10'));

console.log(fails.length ? ('\nFAILED: ' + fails.length) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
