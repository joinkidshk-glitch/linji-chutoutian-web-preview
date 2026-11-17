// v20a276 ICONS276：地點面板標題＋地圖列掣圖示放大加亮。
//   背景：v275 瀏覽器實機（2026-11-17 21:02）——標題圖示 20px 深啡線（#3a2e22）
//   落場景相上面偏細偏暗；列掣圖示 13px 落深藍／深啡掣底幾乎隱形；山頂發射塔
//   喺細尺寸下睇唔到。
//   釘死：(1) #loc-title img.ic112 係 36px 米紙圓底 chip（畫芯 30px）；
//   (2) .map-area-list button img.ic112 係 22px 米紙圓底 chip（畫芯 18px）；
//   (3) iconHtml112() 輸出帶 per-asset cache-buster ?v=20a276；
//   (4) icon_peak.png 256×256 RGBA，發射塔區實色剪影（塔區深色像素 >1000，
//       v275 格仔塔 910）；其餘 3 隻圖 sha256 同 v275 一致，唔郁；
//   (5) 其餘 .ic112 用法原樣（base 1.15em；day-row／cat-tab／act-item 規則唔郁）。
// 用法：node tests/test_icons276_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const root = path.dirname(path.resolve(htmlPath));

let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS ' : 'FAIL ') + name); }

function cssRule(sel){
  // 搵 selector { ... } 第一個匹配，返內容（無註解干擾：規則本身無花括號）。
  const i = html.indexOf(sel + '{');
  if(i < 0) return null;
  const j = html.indexOf('}', i);
  return j < 0 ? null : html.slice(i + sel.length + 1, j);
}

// ---- (1) 標題圖示 36px 米紙圓底 chip ----
const titleRule = cssRule('#loc-title img.ic112');
ok('css #loc-title img.ic112 exists', titleRule !== null);
if(titleRule){
  ok('title icon 36px chip', /height:\s*36px/.test(titleRule) && /width:\s*36px/.test(titleRule));
  ok('title icon padding 3px (art 30px)', /padding:\s*3px/.test(titleRule));
  ok('title icon cream chip #f8f1de', /background:\s*#f8f1de/i.test(titleRule));
  ok('title icon round chip', /border-radius:\s*50%/.test(titleRule));
  ok('title icon box-sizing border-box', /box-sizing:\s*border-box/.test(titleRule));
}

// ---- (2) 地圖列掣圖示 22px 米紙圓底 chip ----
const btnRule = cssRule('.map-area-list button img.ic112');
ok('css .map-area-list button img.ic112 exists', btnRule !== null);
if(btnRule){
  ok('list button icon 22px chip', /height:\s*22px/.test(btnRule) && /width:\s*22px/.test(btnRule));
  ok('list button icon padding 2px (art 18px)', /padding:\s*2px/.test(btnRule));
  ok('list button icon cream chip #f8f1de', /background:\s*#f8f1de/i.test(btnRule));
  ok('list button icon round chip', /border-radius:\s*50%/.test(btnRule));
  ok('list button icon box-sizing border-box', /box-sizing:\s*border-box/.test(btnRule));
}

// ---- (3) iconHtml112() 輸出帶 ?v=20a276 ----
const m = html.match(/function iconHtml112\(v\)\{[\s\S]*?src="assets\/icons\/icon_'\+stem\+'\.png([^"]*)"/);
ok('iconHtml112 src has cache-buster ?v=20a276', !!m && m[1] === '?v=20a276');

// ---- (4) 山頂圖：256×256 RGBA＋實色塔；其餘 3 隻 sha256 唔郁 ----
function pngInfo(p){
  const b = fs.readFileSync(p);
  return { len: b.length, w: b.readUInt32BE(16), h: b.readUInt32BE(20), depth: b[24], type: b[25],
    sha: crypto.createHash('sha256').update(b).digest('hex') };
}
const peak = pngInfo(path.join(root, 'assets', 'icons', 'icon_peak.png'));
ok('peak 256x256 RGBA', peak.w === 256 && peak.h === 256 && peak.depth === 8 && peak.type === 6);
ok('peak sha is v276 solid version',
  peak.sha === 'd1a78c9418fe58263ac20d3bf2a1f12e32a8ffe2c97f81f5971a320b2dce9b4e');
// 塔區（x112–144，y48–142）深色像素：v275 格仔塔 910，v276 實色剪影 1138。
// 塔區（x112–144，y48–142）深色像素：v275 格仔塔 910，v276 實色剪影 1138。
// 純 Node 解 PNG（IHDR＋IDAT inflate＋逐行反濾鏡），唔靠 PIL／shell。
const zlib = require('zlib');
function pngPixels(p){
  const b = fs.readFileSync(p);
  if(b.readUInt32BE(0) !== 0x89504E47) throw new Error('not PNG: ' + p);
  let pos = 8, w = 0, h = 0, bitDepth = 0, colorType = 0;
  const idat = [];
  while(pos < b.length){
    const len = b.readUInt32BE(pos), type = b.toString('ascii', pos + 4, pos + 8);
    const data = b.slice(pos + 8, pos + 8 + len);
    if(type === 'IHDR'){ w = data.readUInt32BE(0); h = data.readUInt32BE(4); bitDepth = data[8]; colorType = data[9]; }
    else if(type === 'IDAT'){ idat.push(data); }
    else if(type === 'IEND'){ break; }
    pos += 12 + len;
  }
  if(bitDepth !== 8 || colorType !== 6) throw new Error('expect 8-bit RGBA: ' + p);
  const raw = zlib.inflateSync(Buffer.concat(idat));
  const stride = w * 4;
  const px = Buffer.alloc(w * h * 4);
  let prev = Buffer.alloc(stride);
  for(let y = 0; y < h; y++){
    const f = raw[y * (stride + 1)];
    const row = raw.slice(y * (stride + 1) + 1, (y + 1) * (stride + 1));
    const out = Buffer.alloc(stride);
    for(let x = 0; x < stride; x++){
      const a = x >= 4 ? out[x - 4] : 0, b2 = prev[x], c = x >= 4 ? prev[x - 4] : 0;
      let v = row[x];
      if(f === 1) v = (v + a) & 255;
      else if(f === 2) v = (v + b2) & 255;
      else if(f === 3) v = (v + ((a + b2) >> 1)) & 255;
      else if(f === 4){ const pa = Math.abs(b2 - c), pb = Math.abs(a - c), pc = Math.abs(a + b2 - 2 * c);
        v = (v + (pa <= pb && pa <= pc ? a : pb <= pc ? b2 : c)) & 255; }
      out[x] = v;
    }
    out.copy(px, y * stride);
    prev = out;
  }
  return { w, h, px };
}
const peakPx = pngPixels(path.join(root, 'assets', 'icons', 'icon_peak.png'));
let towerPx = 0;
for(let y = 48; y <= 142; y++)
  for(let x = 112; x <= 144; x++)
    if(peakPx.px[(y * 256 + x) * 4 + 3] > 10) towerPx++;
ok('peak tower zone solid (>1000 dark px, v275 lattice was 910)', towerPx > 1000);
const UNCHANGED = {
  wave: '7cb34640278f702f9a93eba0dd7a41dd9f9f1dff9fd621b258b5a4eeeb0f4952',
  beach: '9cd624d1e1508695dea3025340cf741afde53378b02ba6f810caac3bcf4bae41',
  plane: '7623408491e75b329f064adb01a50a42de60e7a2dd356a981c167da4e3697890',
};
for(const [stem, sha] of Object.entries(UNCHANGED)){
  const info = pngInfo(path.join(root, 'assets', 'icons', 'icon_' + stem + '.png'));
  ok('icon_' + stem + ' unchanged from v275 (sha256)', info.sha === sha);
}

// ---- (5) 其餘 .ic112 用法原樣 ----
ok('base .ic112 still 1.15em', /\.ic112\{\s*height:1\.15em;\s*width:1\.15em/.test(html));
ok('day-row icon rule untouched', /\.day-row \.ic img\.ic112\{\s*height:1\.2em;\s*width:1\.2em/.test(html));
ok('cat-tab icon rule untouched', /\.cat-tab \.ci img\.ic112\{\s*height:1\.4em;\s*width:1\.4em/.test(html));
ok('act-item icon rule untouched', /\.act-item \.ai img\.ic112\{\s*height:1\.25em;\s*width:1\.25em/.test(html));

console.log('');
if(fails.length){ console.log('FAILED: ' + fails.join(' | ')); process.exit(1); }
console.log('ALL PASS');
