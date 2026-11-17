// v20a275 ICONS275：約會新點 4 隻手繪圖標接入測試。
//   釘死：(1) LOCS 4 個約會地點定義在位，emoji 欄位值保留原值（v112 慣例：存檔／舊測試唔郁）；
//   (2) iconHtml112() 將 4 個值轉做對應手繪圖 <img>，輸出入面無 emoji 原樣殘留；
//   (3) 4 隻圖檔齊、256×256 RGBA 透明底；
//   (4) 全檔 4 個 emoji 各只出現 2 次（LOCS 定義＋EMOJI_ICON112 鍵），其餘渲染位無硬編碼 emoji。
// 用法：node tests/test_icons275_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const root = path.dirname(path.resolve(htmlPath));

let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS ' : 'FAIL ') + name); }

function extractFn(decl){
  const i = html.indexOf(decl);
  if(i < 0) throw new Error('fn not found: ' + decl);
  let j = html.indexOf('{', i), depth = 0, k = j;
  for(; k < html.length; k++){
    if(html[k] === '{') depth++;
    else if(html[k] === '}'){ depth--; if(depth === 0){ k++; break; } }
  }
  return html.slice(i, k);
}
function extractConst(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('const not found: ' + name);
  let depth = 0, started = false;
  for(let k = i; k < html.length; k++){
    const ch = html[k];
    if(ch === '{' || ch === '['){ depth++; started = true; }
    else if(ch === '}' || ch === ']'){ depth--; if(started && depth === 0) return html.slice(i, k + 1) + ';'; }
    else if(ch === ';' && !started) return html.slice(i, k + 1);
  }
  throw new Error('const end not found: ' + name);
}

let code;
try{
  code = extractConst('EMOJI_ICON112') + '\n' + extractFn('function iconHtml112(v)');
}catch(e){
  ok('helpers extractable from index.html (EMOJI_ICON112/iconHtml112 present)', false);
  console.log('');
  console.log('FAILED: ' + fails.join(' | ') + ' | extract error: ' + e.message);
  process.exit(1);
}
eval(code);

// ---- (1) LOCS 4 個約會地點在位，emoji 欄位值保留原值 ----
const LOCS275 = [
  ['date_harbour', '🌊', 'wave'],
  ['date_peak', '🌃', 'peak'],
  ['date_beach', '🏖️', 'beach'],
  ['date_airport', '✈️', 'plane'],
];
for(const [id, em] of LOCS275){
  ok('loc ' + id + ' defined with emoji ' + em,
    html.includes('id:"' + id + '"') && html.includes('emoji:"' + em + '"'));
}

// ---- (2) 渲染轉手繪圖，輸出無 emoji 殘留 ----
for(const [, em, stem] of LOCS275){
  const out = iconHtml112(em);
  ok('render ' + em + ' -> icon_' + stem + '.png',
    out === '<img class="ic112" src="assets/icons/icon_' + stem + '.png?v=20a276" alt="" aria-hidden="true"/>');
  ok('render ' + em + ' output has no raw emoji', !out.includes(em));
}

// ---- (3) 4 隻圖檔齊、256×256 RGBA ----
// PNG 頭：寬高喺 bytes 16–24（IHDR），bit depth 8／color type 6＝RGBA。
for(const [, , stem] of LOCS275){
  const p = path.join(root, 'assets', 'icons', 'icon_' + stem + '.png');
  let good = false;
  try{
    const b = fs.readFileSync(p);
    good = b.length > 1000 && b.readUInt32BE(16) === 256 && b.readUInt32BE(20) === 256
      && b[24] === 8 && b[25] === 6;
  }catch(e){ good = false; }
  ok('file assets/icons/icon_' + stem + '.png 256x256 RGBA', good);
}

// ---- (4) 全檔 4 個 emoji 各只出現 2 次（LOCS 定義＋對照鍵），無其他硬編碼殘留 ----
for(const [, em] of LOCS275){
  const n = html.split(em).length - 1;
  ok('emoji ' + em + ' occurs exactly twice in index.html (loc def + map key)', n === 2);
}

console.log('');
if(fails.length){ console.log('FAILED: ' + fails.join(' | ')); process.exit(1); }
console.log('ALL PASS');
