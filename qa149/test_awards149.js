// qa149/test_awards149.js — v20a149 B1–B4 測試（Node，抽 index.html 真函數 eval＋靜態檢查）
// 用法：node qa149/test_awards149.js [index.html路徑]   （預設 index.html，在工作副本根目錄執行）
// 反證：對 pristine main（da90957，qa149/pristine_index.html）跑，149 新檢查要乾淨 FAIL，唔 crash。
// v20a174 rebase 上 main a500536 resync：backing 636×360→636×540、邏輯 424×240→424×360
// （v174 B1 舞台垂直拉伸；setTransform 1.5 均勻不變）。其餘斷言（B2／B3／B4／彩紙／跳過掣）逐項對位過，唔郁。
const fs = require('fs');
const vm = require('vm');

const IDX = process.argv[2] || 'index.html';
const SRC = fs.readFileSync(IDX, 'utf8');
const fails = [];
let nPass = 0, nFail = 0;
function chk(name, cond) {
  if (cond) { nPass++; console.log('PASS ' + name); }
  else { nFail++; fails.push(name); console.log('FAIL ' + name); }
}

// ---------- 抽 source 段（brace matching，字串感知） ----------
function extractFn(name) {
  const re = new RegExp('function ' + name + '\\s*\\(');
  const m = SRC.match(re);
  if (!m) return null;
  let i = SRC.indexOf('{', m.index);
  let d = 0, j = i;
  for (; j < SRC.length; j++) { if (SRC[j] === '{') d++; else if (SRC[j] === '}') { d--; if (!d) break; } }
  return SRC.slice(m.index, j + 1);
}
function extractConst(name) {
  const re = new RegExp('(?:const|let|var)\\s+' + name + '\\s*=');
  const m = SRC.match(re);
  if (!m) return null;
  let i = SRC.indexOf('=', m.index) + 1;
  while (SRC[i] === ' ' || SRC[i] === '\n') i++;
  const open = SRC[i];
  if (open !== '{' && open !== '[') { const j = SRC.indexOf(';', i); return SRC.slice(m.index, j + 1); }
  const close = open === '{' ? '}' : ']';
  let d = 0, j = i, inS = null, esc = false;
  for (; j < SRC.length; j++) {
    const c = SRC[j];
    if (inS) { if (esc) esc = false; else if (c === '\\') esc = true; else if (c === inS) inS = null; continue; }
    if (c === '"' || c === "'" || c === '`') { inS = c; continue; }
    if (c === open) d++; else if (c === close) { d--; if (!d) break; }
  }
  return SRC.slice(m.index, j + 1);
}

// ---------- vm 上下文（stub 最小依賴） ----------
const captured = [];
const ctx = vm.createContext({
  console,
  S: { dayIndex: 100, newspaperQueue: [], newspaperClippings: [] },
  FREEPLAY_FW: { newspaperStub: { templates: {} } },
  esc: (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch])),
  enqueueNewspaperItem: (raw, opts) => { captured.push(raw); return raw; },
});
function tryEval(code, label) {
  if (!code) { console.log('MISS ' + label); return false; }
  try { vm.runInContext(code, ctx); return true; }
  catch (e) { console.log('EVAL-ERR ' + label + ': ' + e.message); return false; }
}
const got = {};
['EMOJI_ICON112', 'NEWSPAPER_AWARD_GALLERY_TEMPLATES_136'].forEach((c) => { got[c] = tryEval(extractConst(c), c); });
['iconHtml112', 'newspaperFillPlayer', 'newspaperMediumFromAward', 'newspaperCopyFromTemplate',
 'awards63FocusCat', 'awardWinner149', 'awardWinLine149', 'awardGalleryCopy149',
 'awards63FellowsHtml', 'renderAwardResultHtml', 'enqueueNewspaperFromAward'
].forEach((f) => { got[f] = tryEval(extractFn(f), f); });
const live = got.awardWinner149 && got.awards63FellowsHtml && got.renderAwardResultHtml && got.enqueueNewspaperFromAward;
chk('149 helper 函數齊（awardWinner149／awardWinLine149／awardGalleryCopy149）',
  got.awardWinner149 && got.awardWinLine149 && got.awardGalleryCopy149);

// ---------- mock packs ----------
const FELLOWS = [
  { star: '廖炳星', title: '離岸的信', starId: 'liu_bingxing', gigId: 'g1', poster: '' },
  { star: '陸柏言', title: '半張船票', starId: 'luk_baakyin', gigId: 'g2', poster: '' },
  { star: '魏詠男', title: '離岸燈', starId: 'ngai_wingnaam', gigId: 'g3', poster: '' },
];
const FELLOWS_TV = [
  { star: '陸柏言', title: '半張船票', starId: 'luk_baakyin', gigId: 'g2', poster: '' },
  { star: '廖炳星', title: '離岸的信', starId: 'liu_bingxing', gigId: 'g1', poster: '' },
];
function pack149(o) {
  return Object.assign({
    bestOutcome: 'gallery', year: 1991, ceremonyId: 'award_harbour_film', medium: 'film',
    displayName: '維港影藝獎', metricEcho: 'boxOffice', metricEchoLabel: '票房話題',
    press: { paperName: '娛樂快報', headline: '影藝獎夜，銀幕外多一行', dek: '維港影藝獎散場。金禧大酒店門外，票房話題以外，亦有新人入圍消息。' },
    categories: [{ id: 'c1', outcome: 'gallery', label: '最佳電影', fellows63: FELLOWS, winner63: null }],
  }, o || {});
}
function runInCtx(code) { return vm.runInContext(code, ctx); }

// ---------- (1) awardWinner149 ----------
if (live) {
  const wGal = runInCtx(`awardWinner149(${JSON.stringify(pack149())})`);
  chk('B2 helper：gallery 回 fellows[0]（廖炳星《離岸的信》）', wGal && wGal.star === '廖炳星' && wGal.title === '離岸的信');
  const wNom = runInCtx(`awardWinner149(${JSON.stringify(pack149({ bestOutcome: 'nominated', categories: [{ id: 'c1', outcome: 'nominated', label: '最佳電影', fellows63: FELLOWS, winner63: FELLOWS[0] }] }))})`);
  chk('B2 helper：nominated 回 winner63', wNom && wNom.star === '廖炳星' && wNom.title === '離岸的信');
  const wWon = runInCtx(`awardWinner149(${JSON.stringify(pack149({ bestOutcome: 'won', categories: [{ id: 'c1', outcome: 'won', label: '最佳電影', fellows63: FELLOWS, winner63: null }] }))})`);
  chk('B2 helper：won 回 null（得主係阿偉，唔標對手）', wWon === null);
  let nullOk = true, nullOut = 'x';
  try { nullOut = runInCtx('awardWinner149(null)'); nullOk = (nullOut === null); } catch (e) { nullOk = false; }
  chk('B2 helper：null／空 pack 回 null 唔 crash', nullOk && nullOut === null);
  const wEmpty = runInCtx(`awardWinner149(${JSON.stringify({ bestOutcome: 'gallery', categories: [] })})`);
  chk('B2 helper：冇 focus 回 null', wEmpty === null);
} else {
  ['B2 helper：gallery 回 fellows[0]（廖炳星《離岸的信》）', 'B2 helper：nominated 回 winner63',
   'B2 helper：won 回 null（得主係阿偉，唔標對手）', 'B2 helper：null／空 pack 回 null 唔 crash',
   'B2 helper：冇 focus 回 null'].forEach((n) => chk(n, false));
}

// ---------- (2) 報紙：gallery／declined ----------
if (live) {
  captured.length = 0;
  runInCtx(`enqueueNewspaperFromAward(${JSON.stringify(pack149())}, { persist: false })`);
  const gal = captured[0] || {};
  chk('B2 gallery 報紙：headline 含動態得主＋作品', (gal.headline || '').includes('廖炳星') && (gal.headline || '').includes('離岸的信') && (gal.headline || '').includes('奪獎'));
  chk('B2 gallery 報紙：dek 含得主＋阿偉台下見證', (gal.dek || '').includes('廖炳星') && (gal.dek || '').includes('阿偉'));
  chk('B2 gallery 報紙：fameDelta 1＋templateEventKey award_gallery.film',
    gal.fameDelta === 1 && gal.templateEventKey === 'award_gallery.film');
  // 換 seed／換 ceremony：得主唔同，頭版跟住變（唔係寫死廖炳星）
  captured.length = 0;
  const tvPack = pack149({ ceremonyId: 'award_singho_tv', medium: 'tv', displayName: '星河台慶', bestOutcome: 'gallery',
    categories: [{ id: 'c1', outcome: 'gallery', label: '最佳劇集', fellows63: FELLOWS_TV, winner63: null }] });
  runInCtx(`enqueueNewspaperFromAward(${JSON.stringify(tvPack)}, { persist: false })`);
  const galTv = captured[0] || {};
  chk('B2 gallery 報紙（換 ceremony／得主）：頭版跟實際得主（陸柏言＋星河台慶夜）',
    (galTv.headline || '').includes('陸柏言') && (galTv.headline || '').includes('星河台慶夜') && !(galTv.headline || '').includes('廖炳星'));
  // declined
  captured.length = 0;
  runInCtx(`enqueueNewspaperFromAward(${JSON.stringify(pack149())}, { persist: false, declined: true })`);
  const dec = captured[0] || {};
  chk('B2 declined 報紙：headline／dek 含動態得主＋作品', (dec.headline || '').includes('廖炳星') && (dec.headline || '').includes('離岸的信') && (dec.dek || '').includes('照常舉行'));
  chk('B2 declined 報紙：fameDelta 0＋templateEventKey award_declined.film',
    dec.fameDelta === 0 && dec.templateEventKey === 'award_declined.film');
  // winner null → 跌返舊文案
  captured.length = 0;
  const noWin = pack149({ categories: [{ id: 'c1', outcome: 'gallery', label: '最佳電影', fellows63: [], winner63: null }] });
  runInCtx(`enqueueNewspaperFromAward(${JSON.stringify(noWin)}, { persist: false })`);
  const galOld = captured[0] || {};
  chk('B2 gallery winner null：跌返舊靜態模板，唔 crash',
    (galOld.headline || '') === '維港影藝獎之夜 阿偉台下見證新面孔誕生');
  captured.length = 0;
  runInCtx(`enqueueNewspaperFromAward(${JSON.stringify(noWin)}, { persist: false, declined: true })`);
  const decOld = captured[0] || {};
  chk('B2 declined winner null：跌返 press 舊文案，唔 crash',
    (decOld.headline || '') === '影藝獎夜，銀幕外多一行');
} else {
  ['B2 gallery 報紙：headline 含動態得主＋作品', 'B2 gallery 報紙：dek 含得主＋阿偉台下見證',
   'B2 gallery 報紙：fameDelta 1＋templateEventKey award_gallery.film',
   'B2 gallery 報紙（換 ceremony／得主）：頭版跟實際得主（陸柏言＋星河台慶夜）',
   'B2 declined 報紙：headline／dek 含動態得主＋作品', 'B2 declined 報紙：fameDelta 0＋templateEventKey award_declined.film',
   'B2 gallery winner null：跌返舊靜態模板，唔 crash', 'B2 declined winner null：跌返 press 舊文案，唔 crash'
  ].forEach((n) => chk(n, false));
}

// ---------- (3) 結果卡：fellows 🏆＋metricLine ----------
if (live) {
  const fhGal = runInCtx(`awards63FellowsHtml(${JSON.stringify({ outcome: 'gallery', fellows63: FELLOWS, winner63: null })})`);
  chk('B2 結果卡：gallery 有 🏆 標記＋「為得主」', fhGal.includes('trophy') && fhGal.includes('為得主') && fhGal.includes('廖炳星'));
  const fhNom = runInCtx(`awards63FellowsHtml(${JSON.stringify({ outcome: 'nominated', fellows63: FELLOWS, winner63: FELLOWS[0] })})`);
  chk('B2 結果卡：nominated 照舊有 🏆 標記', fhNom.includes('trophy') && fhNom.includes('為得主'));
  const fhWon = runInCtx(`awards63FellowsHtml(${JSON.stringify({ outcome: 'won', fellows63: FELLOWS, winner63: null })})`);
  chk('B2 結果卡：won 唔標對手做得主', !fhWon.includes('trophy') && !fhWon.includes('為得主'));
  const resGal = runInCtx(`renderAwardResultHtml(${JSON.stringify(pack149())})`);
  chk('B2 結果卡 metricLine：gallery 寫實內容（含得主＋奪獎）',
    resGal.includes('廖炳星') && resGal.includes('離岸的信') && resGal.includes('奪獎') && !resGal.includes('票房話題——典禮後仍有人提起。'));
  const resWon = runInCtx(`renderAwardResultHtml(${JSON.stringify(pack149({ bestOutcome: 'won', categories: [{ id: 'c1', outcome: 'won', label: '最佳電影', fellows63: FELLOWS, winner63: null }] }))})`);
  chk('B2 結果卡 metricLine：won 唔寫對手做得主（跌返舊句）',
    resWon.includes('票房話題——典禮後仍有人提起。') && !resWon.includes('廖炳星憑'));
} else {
  ['B2 結果卡：gallery 有 🏆 標記＋「為得主」', 'B2 結果卡：nominated 照舊有 🏆 標記',
   'B2 結果卡：won 唔標對手做得主', 'B2 結果卡 metricLine：gallery 寫實內容（含得主＋奪獎）',
   'B2 結果卡 metricLine：won 唔寫對手做得主（跌返舊句）'].forEach((n) => chk(n, false));
}

// ---------- (4) B3：卡片 csscard／win class（靜態，抽 playCeremony 段） ----------
const playSrc = extractFn('awards62PlayCeremony') || '';
chk('B3 卡片：cardsData 有 win 旗（me 逢 won／fellow 對照 winFellow）',
  playSrc.includes('win: best === "won"') && playSrc.includes('win: !!(winFellow'));
chk('B3 卡片：win 卡加 win class', playSrc.includes('(c.win ? " win" : "")'));
chk('B3 卡片：冇 poster 嗰陣 csscard 係媒介圖標＋典禮名，唔印片名',
  playSrc.includes('awd63-cssicon') && playSrc.includes('awd63-cssname') && !playSrc.includes('<div class="awd63-csscard">《\' + c.title + \'》</div>'));
chk('B3 卡面：win 角標 CSS 在位（.awd63-card.win::after 🏆）',
  SRC.includes('.awd63-card.win::after') && SRC.includes('content:"🏆"'));

// ---------- (5) B1：舞台／canvas／彩紙（靜態） ----------
// 反向斷言：觀眾帶已剔走（字串拆開寫，唔好令本檔出現該 class 名全寫，否則 grep 零命中驗收會誤報）
chk('B1 舞台：觀眾帶已剔走——.awd62-stage 還原橫向置中 flex，檔內零觀眾帶',
  SRC.includes('.awd62-stage{position:fixed;inset:0;z-index:9990;background:#14101f;display:flex;align-items:center;justify-content:center;padding:12px}')
  && !SRC.includes('.awd62-frame{position:relative;width:min(96vw,760px);flex:none}')
  && !SRC.includes('awd62-' + 'aud') && !SRC.includes('aud' + '149'));
chk('B1 舞台：canvas backing 636×540（v149×v174 合併：邏輯 424×360 ×1.5）', SRC.includes('width="636" height="540"'));
chk('B1 舞台：draw() 入口 setTransform 1.5（邏輯座標 424×360，v174 B1）',
  SRC.includes('ctx.setTransform(1.5, 0, 0, 1.5, 0, 0);') && playSrc.includes('const W = 424, H = 360'));
chk('B1 彩紙：M5 GIF 資產入 repo＋code 用 ?v=20a149 引用',
  fs.existsSync('assets/fx/awd_confetti_m5.gif') && fs.statSync('assets/fx/awd_confetti_m5.gif').size > 10000
  && SRC.includes('assets/fx/awd_confetti_m5.gif?v=20a149'));
chk('B1 彩紙：spawnConfetti 90 粒', playSrc.includes('for(let i = 0; i < 90; i++)'));
chk('B1 彩紙：reveal 唔限 won 先 spawn（gallery／nominated 都有）',
  playSrc.includes('if(beats[beatIdx].id === "reveal") spawnConfetti();'));
chk('B1 彩紙：comfort 期間彩紙繼續落＋畫', playSrc.includes('b.id === "reveal" || b.id === "comfort"') && playSrc.includes('comfort 期間彩紙維持飄落'));
chk('B1 彩紙：M5 overlay 有開關（syncConfetti149＋reveal／comfort／out 顯示）',
  playSrc.includes('syncConfetti149') && playSrc.includes('b.id === "reveal" || b.id === "comfort" || b.id === "out"'));
chk('B1 跳過掣：框內對齊 top:8px;right:8px', SRC.includes('.awd62-skip{position:absolute;top:8px;right:8px;'));

// ---------- (6) B4＋log pane（靜態） ----------
chk('B4 報紙：短屏 media query 加 padding-bottom 76px（932 唔郁）',
  SRC.includes('@media (max-height:800px)') && SRC.includes('#mask.paper-on .paper-sheet{ padding-bottom:76px; }'));
chk('B2 log 列表：gallery 嗰行同樣用 fellows[0] 標得主',
  SRC.includes('c.outcome === "gallery"') && extractFn('renderAwardsPane62').includes('fellows63[0]'));

// ---------- 紀律 ----------
chk('紀律：SAVE key 未郁；產品 ?v=v20a10 未郁；新資產 ?v=20a149 只用喺 M5 兩張 img',
  SRC.includes('starVolunteer_map_v19w') && SRC.includes('v20a10') && (SRC.split('?v=20a149').length - 1) === 2);
chk('紀律：贏線 0.875／D4 數字未郁', SRC.includes('0.875'));

console.log(`\nTOTAL PASS ${nPass} FAIL ${nFail}`);
if (fails.length) console.log('FAILS: ' + fails.join(' | '));
process.exit(nFail ? 1 : 0);
