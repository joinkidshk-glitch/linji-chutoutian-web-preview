// v20a112 ICONS112 圖標組・邏輯測試：中央對照 iconHtml112()＋S-46 favDots112() 真路徑。
//   段一：審計對照表 32 個欄位值逐個映射（31 個→正確圖檔，✅→CSS 勾）。
//   段二：欄位值以外嘅 emoji 原樣通過（🏆🔒💡🍍 等留低嗰批唔准誤換）。
//   段三：favDots112() 格數／鉗制／零 ♥/♡。
//   反證：對基線 546007d 跑，extractFn 搵唔到 iconHtml112 即 FAIL（見 NOTES §5）。
// 用法：node tests/test_icons112_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');

let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }

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
  code = extractConst('EMOJI_ICON112') + '\n' + extractFn('function iconHtml112(v)') + '\n' + extractFn('function favDots112(n)');
}catch(e){
  ok('helpers extractable from index.html (iconHtml112/favDots112 present)', false);
  console.log('');
  console.log('FAILED: ' + fails.join(' | ') + ' | extract error: ' + e.message);
  process.exit(1);
}
eval(code);

// ---- 段一：32 個欄位值逐個映射（審計 notes_icon_audit.md §2） ----
const EXPECT = {
  '🗺️':'map', '😴':'sleep', '🌙':'sleep', '🎤':'mic', '☕':'tea',
  '🎬':'clapper', '🎥':'clapper', '💪':'fitness', '🏠':'home', '📰':'news',
  '🎁':'gift', '🏥':'hospital', '🎵':'music', '💿':'music', '👥':'people',
  '📺':'tv', '📻':'radio', '📡':'radio', '🦁':'lion', '💼':'briefcase',
  '🏢':'building', '🎭':'mask', '📚':'book', '📖':'book', '🥋':'martial',
  '🧹':'broom', '🤒':'sick', '📞':'phone', '😊':'mood', '⭐':'star', '✨':'sparkle'
};
for(const [em, stem] of Object.entries(EXPECT)){
  const out = iconHtml112(em);
  ok('map ' + em + ' -> icon_' + stem + '.png',
    out === '<img class="ic112" src="assets/icons/icon_' + stem + '.png" alt="" aria-hidden="true"/>');
}
// ✅ 行 CSS，唔係 <img>
ok('map ✅ -> css check', iconHtml112('✅') === '<span class="ic-check112" aria-hidden="true">✓</span>');
ok('map ✅ has no img', !iconHtml112('✅').includes('<img'));
// 欄位值窮舉：index.html 入面所有 icon:/emoji: 值都對得上（除 ✅／·）
const fieldVals = new Set();
for(const m of html.matchAll(/(?:icon|emoji)\s*:\s*"([^"]*)"/g)) fieldVals.add(m[1]);
ok('field values enumerated (33 incl · = 32 emoji + placeholder)', fieldVals.size === 33);
for(const v of [...fieldVals].sort()){
  if(v === '✅' || v === '·') continue;
  ok('field value covered: ' + v, iconHtml112(v).includes('<img class="ic112"'));
}
// ---- 段二：留低嗰批原樣通過 ----
for(const em of ['🏆', '🔒', '💡', '📋', '👤', '🍍', '🧁', '🧴', '📎', '📝', '📼', '🍬', '🌸']){
  ok('passthrough ' + em, iconHtml112(em) === em);
}
ok('passthrough · placeholder', iconHtml112('·') === '·');
ok('empty -> empty', iconHtml112('') === '' && iconHtml112(null) === '' && iconHtml112(undefined) === '');
// ---- 段三：favDots112 ----
for(const [n, want] of [[0,0],[1,1],[2,2],[3,3],[4,4],[5,5],[8,5],[-2,0]]){
  const out = favDots112(n);
  const ons = (out.match(/<i class="on">/g) || []).length;
  const total = (out.match(/<i class=/g) || []).length;
  ok('dots n=' + n + ' -> ' + want + ' on / 5 total', ons === want && total === 5);
}
ok('dots has no hearts', !favDots112(3).includes('♥') && !favDots112(3).includes('♡'));
ok('dots wrapper class', favDots112(2).startsWith('<span class="fav-dots112"'));

console.log('');
if(fails.length){ console.log('FAILED: ' + fails.join(' | ')); process.exit(1); }
console.log('ALL PASS');
