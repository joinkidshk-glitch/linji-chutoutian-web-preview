// v20a120 LOCFULL120 邏輯測試：地點面板改全屏幕——負責人錨定幾何（AnchorOwner）。
//   斷言：全屏幕之後 sheet 高變咗（~844px），人物高度上限 230→400（貼近 Phase 1 樣本
//   400px）、下限 120 不變；腳部收 120px 入選項卡後面（遮腿，跟樣本腳入卡 120px 做法，
//   個人可以放大、淨係頭＋身喺卡上面見到）；上限由 actsTop（選項卡頂）本身限住，
//   唔頂穿 sheet 頂（未封頂嗰陣頂緣啱啱 y=8）；短屏（700px）同樣公式；owner hidden
//   嗰陣早退，唔郁 style。
// 反證：pristine main（v118 版）跑呢檔要 FAIL（上限仲係 230、腳收 8px）。
// 用法：node tests/test_locfull120_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS ' : 'FAIL ') + name); }
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
// 假 DOM：只夠 AnchorOwner 用（getElementById＋style＋offset／client 讀數）
function fakeDoc(sheetH, actsTop, tagH, ownerHidden){
  const els = {
    'loc-sheet': { clientHeight: sheetH, style: {} },
    'loc-owner118': { hidden: !!ownerHidden, style: {} },
    'loc-acts': { offsetTop: actsTop, style: {} },
    'loc-owner-tag118': { offsetHeight: tagH, style: {} },
    'loc-owner-img118': { style: {} },
  };
  return { getElementById: (id)=>els[id] || null, _els: els };
}
const anchorSrc = extractFn('locpanel118AnchorOwner') + '\nreturn locpanel118AnchorOwner;';
const anchor = new Function('document', anchorSrc);

function run(sheetH, actsTop, tagH, ownerHidden){
  const doc = fakeDoc(sheetH, actsTop, tagH, ownerHidden);
  const fn = anchor(doc); // new Function 體回傳 inner fn；inner fn 閉包食外層 document 參數
  fn();
  return doc._els;
}

// ---- (1) 上限 400：actsTop 夠高嗰陣唔再限 230 ----
let els = run(844, 600, 28, false);
ok('上限 400：actsTop 600、tagH 28 → img 高 400px（唔係舊 230）',
   els['loc-owner-img118'].style.height === '400px');
ok('上限 400：owner 高＝img＋tag＋4',
   els['loc-owner118'].style.height === (400 + 28 + 4) + 'px');
// ---- (2) 中間值：actsTop＋tuck 限住（唔頂穿 sheet 頂） ----
els = run(844, 200, 28, false);
ok('中間值：actsTop 200、tagH 28 → img 高 280px（actsTop-tagH-12+120）',
   els['loc-owner-img118'].style.height === '280px');
// ---- (3) 下限 120 不變 ----
els = run(844, 30, 28, false);
ok('下限 120：actsTop 30 → img 高 120px（唔穿底）',
   els['loc-owner-img118'].style.height === '120px');
// ---- (4) 腳部收 120px 入選項卡（遮腿，跟樣本）：bottom＝sheet 高－actsTop－120 ----
els = run(844, 400, 28, false);
ok('遮腿：844 屏、actsTop 400 → owner bottom 324px',
   els['loc-owner118'].style.bottom === '324px');
ok('遮腿：封頂嗰陣 owner 頂 ≥ 0（actsTop 400、img 400 → 頂 y=88）',
   (844 - 324 - (400 + 28 + 4)) >= 0);
els = run(844, 200, 28, false);
ok('遮腿：未封頂嗰陣 owner 頂啱啱 y=8（唔頂穿 sheet 頂）',
   (844 - parseInt(els['loc-owner118'].style.bottom, 10)
    - parseInt(els['loc-owner118'].style.height, 10)) === 8);
// ---- (5) 短屏同一公式 ----
els = run(700, 300, 28, false);
ok('短屏 700px：actsTop 300 → img 高 380px、bottom 280px',
   els['loc-owner-img118'].style.height === '380px' &&
   els['loc-owner118'].style.bottom === '280px');
// ---- (6) owner hidden 早退，唔郁 style ----
els = run(844, 400, 28, true);
ok('owner hidden 嗰陣早退（img／owner 無 style 寫入）',
   els['loc-owner-img118'].style.height === undefined &&
   els['loc-owner118'].style.bottom === undefined);

console.log(fails.length ? 'RESULT FAIL (' + fails.length + ')' : 'RESULT PASS');
process.exit(fails.length ? 1 : 0);
