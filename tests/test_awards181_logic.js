// v20a181 頒獎禮橫向重建・邏輯測試：
// (1) awards181DrawBase 程式舞台幾何（mock ctx 錄 fillRect）：幕布／燈架／木地板／前緣／觀眾席
//     全部對位——地板 y200–334（深 134px＝37.2% 高，約四成）、前緣深木 y334–340、觀眾席 y340–360。
// (2) awards62FallbackStage 退化到同一個程式舞台（M1 底圖已撤，唔再分叉）。
// (3) pan 橫移：off 經 translate 傳入，±6。
// (4) beats 守衛（唔郁）：得獎全長約 11.5 秒、walkup 2200ms caption ""、旁聽約 9.6 秒、comfort 2600ms。
// 反證：對 pristine main 91f264a 行 → awards181DrawBase 唔存在 → FAIL（唔 crash）。
// 用法：node tests/test_awards181_logic.js [path-to-index.html]
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

let baseSrc, fbSrc, beatsSrc;
try{
  baseSrc = extractFn('awards181DrawBase');
  fbSrc = extractFn('awards62FallbackStage');
  beatsSrc = extractFn('awards62CeremonyBeats');
}catch(e){
  console.log('FAIL v181 舞台函數抽唔到（' + e.message + '，pristine 預期）');
  console.log('\nFAILED: 1');
  process.exit(1);
}
eval(baseSrc);
eval(fbSrc);
var iconHtml112 = function(s){ return s; };
var poster59Path = function(){ return 'poster.png'; }; /* glamour beat 要有海報先加（beats 內 typeof＋真值檢查） */
eval(beatsSrc);

/* ================= (1) 程式舞台幾何 ================= */
let m = mockCtx();
awards181DrawBase(m.ctx, 480, 360, 0);
const R = m.calls;
ok('幕布淺米底 y36–200（#f2e8d5）', rects(R, '#f2e8d5').some(r => r[1] === -8 && r[2] === 36 && r[3] === 496 && r[4] === 164));
ok('頂部深紅帶 y0–36（#6e1a20，橫額底）', rects(R, '#6e1a20').some(r => r[2] === 0 && r[4] === 36));
ok('側幕深紅兩邊（#7a1f24，x -8／450）', rects(R, '#7a1f24').some(r => r[1] === -8 && r[3] === 38) && rects(R, '#7a1f24').some(r => r[1] === 450 && r[3] === 38));
ok('燈架深色鐵杆左右（#23232c，x12／452，y40 高 160）', rects(R, '#23232c').some(r => r[1] === 12 && r[2] === 40 && r[4] === 160) && rects(R, '#23232c').some(r => r[1] === 452 && r[2] === 40 && r[4] === 160));
ok('木地板 y200–334（#d9a75f，深 134px＝37.2% 高）', rects(R, '#d9a75f').some(r => r[1] === -8 && r[2] === 200 && r[3] === 496 && r[4] === 134));
ok('地板佔畫面下半約四成（134/360＝37.2%，30–40% 帶內）', (134 / 360) >= 0.30 && (134 / 360) <= 0.42);
ok('地板前緣深木邊 y334–340（#5a3a1e，高 6）', rects(R, '#5a3a1e').some(r => r[2] === 334 && r[4] === 6));
ok('暗觀眾席 y340–360（#120c20，高 20，唔係圓台／講台）', rects(R, '#120c20').some(r => r[2] === 340 && r[4] === 20));
ok('觀眾席有光點（金色 3px 點 ≥4 粒）', rects(R, 'rgba(255,233,143,0.85)').filter(r => r[3] === 3 && r[4] === 3).length >= 4);
ok('冇圓台／講台形狀（唔畫橢圓台面，ellipse 只係剪影用，base 內 0 次）', R.filter(c => c[0] === 'ellipse').length === 0);

/* ================= (2) 後備舞台＝同一個程式舞台 ================= */
let m2 = mockCtx();
awards62FallbackStage(m2.ctx, 480, 360);
ok('fallback 畫出同一塊木地板（#d9a75f y200 高 134）', rects(m2.calls, '#d9a75f').some(r => r[2] === 200 && r[4] === 134));
ok('fallback 畫出同一條觀眾席（#120c20 y340）', rects(m2.calls, '#120c20').some(r => r[2] === 340 && r[4] === 20));
ok('fallback 唔再畫舊格仔舞台（rgba(255,255,255,0.03) 唔出現）', !m2.calls.some(c => c[0] === 'fillRect' && c[5] === 'rgba(255,255,255,0.03)'));

/* ================= (3) pan 橫移 ================= */
let m3 = mockCtx();
awards181DrawBase(m3.ctx, 480, 360, 6);
ok('pan off=6 經 translate(6,0) 傳入', m3.calls.some(c => c[0] === 'translate' && c[1] === 6 && c[2] === 0));
let m4 = mockCtx();
awards181DrawBase(m4.ctx, 480, 360, 0);
ok('off=0 唔橫移（translate(0,0)）', m4.calls.some(c => c[0] === 'translate' && c[1] === 0 && c[2] === 0));

/* ================= (4) beats 守衛（唔郁） ================= */
const beatsWon = awards62CeremonyBeats({ displayName: '星河電視獎', bestOutcome: 'won', repWork62: '長篇劇',
  categories: [{ label: '最佳男主角', outcome: 'won', repWorkTitle: '長篇劇' }] });
const totalWon = beatsWon.reduce((a, b) => a + b.ms, 0);
ok('得獎 beats 全長約 13.35 秒（有海報 glamour 1800ms：11550＋1800＝13350）', totalWon >= 13000 && totalWon <= 13700);
const walkupBeat = beatsWon.find(b => b.id === 'walkup');
ok('walkup beat 2200ms、caption 係空（文案改由 draw() setCaption）', !!walkupBeat && walkupBeat.ms === 2200 && walkupBeat.caption === '');
ok('贏分支順序 reveal→walkup→glamour→out', beatsWon.map(b => b.id).join(',').indexOf('reveal,walkup,glamour,out') >= 0);
const beatsGal = awards62CeremonyBeats({ displayName: '海港廣告獎', bestOutcome: 'gallery', categories: [] });
ok('旁聽 beats 約 9.6 秒', beatsGal.reduce((a, b) => a + b.ms, 0) >= 9000 && beatsGal.reduce((a, b) => a + b.ms, 0) <= 10000);
const beatsNom = awards62CeremonyBeats({ displayName: '星河電視獎', bestOutcome: 'nominated', repWork62: '長篇劇',
  categories: [{ label: '最佳男主角', outcome: 'nominated', repWorkTitle: '長篇劇' }] });
const comfortBeat = beatsNom.find(b => b.id === 'comfort');
ok('入圍 comfort beat 2600ms（何生安慰）', !!comfortBeat && comfortBeat.ms === 2600 && /何生/.test(comfortBeat.caption));

console.log(fails.length ? ('\nFAILED: ' + fails.length) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
