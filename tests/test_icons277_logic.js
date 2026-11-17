// v20a277 ICONS277：山頂圖標重畫（支塔畫大）＋清走死 CSS。
//   背景：v276 標題圓片得咗，但山頂塔喺面板尺寸下依然讀做「座山多過發射塔」——
//   v276 填實做咗（塔區 1138），問題係成隻圖入面支塔太細（256px 圖入面塔闊得
//   32px，30px 畫芯下得 ~2px，睇落似天線）。v277 將支塔畫大做主體：橫臂
//   x40–216（177px，69% 畫面）、塔底闊 140（55%）、塔高 207（81%）。
//   同時清走 v276 留低嘅死 CSS：.map-area-list button img.ic112 22px chip
//   規則——嗰行掣自 v20a43 起 #app #map-area-list{ display:none !important; }
//   （用戶 2026-11-09 拍板刪走底部快捷列），規則永遠食唔到。
//   釘死：(1) 新塔幾何（塔闊 ≥128、塔高 ≥154、塔區深色像素 >12000）；
//   (2) 縮放可讀：box-downsample 到 30px／24px，橫臂帶最闊深色連續段同
//       塔底帶最闊深色連續段有足夠闊度（唔淨係釘檔案存在）；
//   (3) 死 CSS 已刪、#map-area-list display:none 留喺度；
//   (4) iconHtml112() 輸出帶 ?v=20a277；其餘 3 隻圖 sha256 唔郁。
// 用法：node tests/test_icons277_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const zlib = require('zlib');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const root = path.dirname(path.resolve(htmlPath));

let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS ' : 'FAIL ') + name); }

// ---- 純 Node 解 PNG（IHDR＋IDAT inflate＋逐行反濾鏡），唔靠 PIL／shell ----
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
function pngInfo(p){
  const b = fs.readFileSync(p);
  return { len: b.length, w: b.readUInt32BE(16), h: b.readUInt32BE(20), depth: b[24], type: b[25],
    sha: crypto.createHash('sha256').update(b).digest('hex') };
}
const alphaAt = (pp, x, y) => pp.px[(y * pp.w + x) * 4 + 3];

// ---- (1) 新塔幾何 ----
const peak = pngInfo(path.join(root, 'assets', 'icons', 'icon_peak.png'));
ok('peak 256x256 RGBA', peak.w === 256 && peak.h === 256 && peak.depth === 8 && peak.type === 6);
ok('peak sha is v277 redrawn version',
  peak.sha === '945fe0c929e35085b04feccef762d14ab45e5c5e93ddf21a8a9787b65813cc84');
const peakPx = pngPixels(path.join(root, 'assets', 'icons', 'icon_peak.png'));
// 塔區 x40–216、y16–222（橫臂＋天線＋主塔，不含月亮／星／山丘線）。
let towerPx = 0, minX = 999, maxX = -1, minY = 999, maxY = -1;
for(let y = 16; y <= 222; y++)
  for(let x = 40; x <= 216; x++)
    if(alphaAt(peakPx, x, y) > 10){
      towerPx++;
      if(x < minX) minX = x;
      if(x > maxX) maxX = x;
      if(y < minY) minY = y;
      if(y > maxY) maxY = y;
    }
ok('peak tower zone dark px >12000 (v276 was 1138 in old zone)', towerPx > 12000);
ok('peak tower width >=128 (half canvas, v276 was 32)', (maxX - minX + 1) >= 128);
ok('peak tower height >=154 (60% canvas, v276 was ~94)', (maxY - minY + 1) >= 154);

// ---- (2) 縮放可讀：box-downsample，覆蓋率 >0.25 計深色格 ----
// 模擬瀏覽器將 256px 圖縮到標題 chip 畫芯 30px／24px：橫臂帶（y 22–30%）
// 同塔底帶（y 80–88%）最闊深色連續段要夠闊，支塔先唔會縮成天線。
function downsample(pp, size){
  const cell = [];
  for(let oy = 0; oy < size; oy++){
    const row = [];
    for(let ox = 0; ox < size; ox++){
      const x0 = Math.floor(ox * 256 / size), x1 = Math.max(x0 + 1, Math.floor((ox + 1) * 256 / size));
      const y0 = Math.floor(oy * 256 / size), y1 = Math.max(y0 + 1, Math.floor((oy + 1) * 256 / size));
      let tot = 0, n = 0;
      for(let y = y0; y < y1; y++)
        for(let x = x0; x < x1; x++){ if(alphaAt(pp, x, y) > 10) tot++; n++; }
      row.push(tot / n);
    }
    cell.push(row);
  }
  return cell;
}
function widestRun(cell, y0f, y1f){
  let best = 0;
  for(let y = Math.floor(cell.length * y0f); y < Math.floor(cell.length * y1f); y++){
    let cur = 0;
    for(const c of cell[y]){ if(c > 0.25){ cur++; best = Math.max(best, cur); } else cur = 0; }
  }
  return best;
}
for(const size of [30, 24]){
  const d = downsample(peakPx, size);
  let dark = 0;
  for(const row of d) for(const c of row) if(c > 0.25) dark++;
  const arm = widestRun(d, 0.22, 0.30), base = widestRun(d, 0.80, 0.88);
  console.log(`  [${size}px] dark cells ${dark}/${size * size}, crossarm run ${arm}, base run ${base}`);
  ok(`${size}px dark cells enough (v277 measured ${dark})`, dark >= (size === 30 ? 200 : 140));
  ok(`${size}px crossarm band run >=${size === 30 ? 15 : 12} (measured ${arm})`, arm >= (size === 30 ? 15 : 12));
  ok(`${size}px base band run >=${size === 30 ? 12 : 10} (measured ${base})`, base >= (size === 30 ? 12 : 10));
}

// ---- (3) 死 CSS 已刪、#map-area-list display:none 留喺度 ----
ok('dead css .map-area-list button img.ic112 removed', html.indexOf('.map-area-list button img.ic112{') < 0);
ok('#map-area-list stays display:none (v20a43, do NOT revive)', /#app #map-area-list\{\s*display:none !important;/.test(html));

// ---- (4) cache-buster ?v=20a277；其餘 3 隻圖唔郁 ----
const m = html.match(/function iconHtml112\(v\)\{[\s\S]*?src="assets\/icons\/icon_'\+stem\+'\.png([^"]*)"/);
ok('iconHtml112 src has cache-buster ?v=20a277', !!m && m[1] === '?v=20a277');
const UNCHANGED = {
  wave: '7cb34640278f702f9a93eba0dd7a41dd9f9f1dff9fd621b258b5a4eeeb0f4952',
  beach: '9cd624d1e1508695dea3025340cf741afde53378b02ba6f810caac3bcf4bae41',
  plane: '7623408491e75b329f064adb01a50a42de60e7a2dd356a981c167da4e3697890',
};
for(const [stem, sha] of Object.entries(UNCHANGED)){
  const info = pngInfo(path.join(root, 'assets', 'icons', 'icon_' + stem + '.png'));
  ok('icon_' + stem + ' unchanged from v275 (sha256)', info.sha === sha);
}

console.log('');
if(fails.length){ console.log('FAILED: ' + fails.join(' | ')); process.exit(1); }
console.log('ALL PASS');
