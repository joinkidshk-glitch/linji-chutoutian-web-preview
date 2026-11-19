// v20a339 剪報文案死引用清理測試：傳聞系統已於 v20a267 成個刪走，剪報空狀態卡
//   仲寫住「傳聞仍是圈內耳語，跟這疊公開剪報分開。」——死引用。今版刪走嗰句，
//   順手清埋全檔 grep「傳聞」掃描搵到嘅另外兩處玩家面死引用：
//   L9693 R_choi_meet hint（傳聞閘已刪，鎖文案得返「要到秋或冬」）、
//   NPC_TIER_LINES 兩句貼士（手帳拼合機制已刪，改指打聽／風聲）。
// 用法：node tests/test_r339_clipping_copy.js [path-to-index.html]
// 反證：喺 v338 index 上行 → A1／A2／A3／A4／B2 乾淨 FAIL（舊文案在位）。
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond, extra){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name + (extra ? ' :: ' + extra : '')); }
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

/* ---------- A 組：靜態——死引用字串已清、新文案在位 ---------- */
ok('A1 剪報空狀態舊句「傳聞仍是圈內耳語」已刪', html.indexOf('傳聞仍是圈內耳語') < 0);
ok('A2 R_choi_meet hint 舊句「聽過采兒或曉晴傳聞」已刪', html.indexOf('聽過采兒或曉晴傳聞') < 0);
ok('A3 何生貼士舊句「返去手帳拼下先」已刪', html.indexOf('返去手帳拼下先') < 0);
ok('A4 采兒貼士舊句「拼返去傳聞度」已刪', html.indexOf('拼返去傳聞度') < 0);
ok('A5 剪報空狀態新文案在位（第一句完整）',
  html.indexOf('<h4>未有剪報</h4><p>殺青、頒獎或劇情見報之後，下一朝的報紙會留在這裡。</p>') >= 0);
ok('A6 R_choi_meet hint 新文案在位',
  html.indexOf('hint = "支線《週刊小訪》。不等於主線《采兒小訪題》。主線要到秋或冬。";') >= 0);
ok('A7 何生貼士新文案在位（改指打聽）',
  html.indexOf('聽到啲傳聞唔好齋聽，去打聽下查實先。查得實嘅情報，先至值錢。') >= 0);
ok('A8 采兒貼士新文案在位（改指風聲）',
  html.indexOf('同圈內風聲對下，先知邊單先係真。') >= 0);

/* ---------- B 組：真跑 renderClippingsPane 空狀態 ---------- */
let _box = { innerHTML: '' };
let document = { getElementById: (id)=> id === 'clippings-list' ? _box : null };
let S = {}; /* 無 ending410 → 結局卡分支跳過 */
function ensureNewspaperClippings(){ return []; }
/* ensureNews82 唔定義：函數入面 typeof 守衛，照行 */
eval(extractFn('renderClippingsPane'));
try{ renderClippingsPane(); }catch(_e){}
ok('B1 空狀態照常渲染（未有剪報卡＋等第一張剪報裝飾）',
  _box.innerHTML.indexOf('<h4>未有剪報</h4>') >= 0 && _box.innerHTML.indexOf('等第一張剪報') >= 0,
  _box.innerHTML.slice(0, 80));
ok('B2 空狀態渲染輸出無「傳聞」死引用', _box.innerHTML.indexOf('傳聞') < 0);
ok('B3 空狀態第一句完整在位',
  _box.innerHTML.indexOf('殺青、頒獎或劇情見報之後，下一朝的報紙會留在這裡。') >= 0);

/* ---------- C 組：非空狀態唔受影響（有剪報照常出卡） ---------- */
function newspaperEsc(s){ return String(s == null ? '' : s); }
let NEWS82_IMGS = {};
ensureNewspaperClippings = function(){ return [{ dateLabel:'1990 年春', paperName:'維港日報', headline:'新人殺青', dek:'正文', fameDelta: 2, shorts: [], clipLabel: '' }]; };
_box = { innerHTML: '' };
try{ renderClippingsPane(); }catch(_e){}
ok('C1 非空狀態照常渲染剪報卡', _box.innerHTML.indexOf('新人殺青') >= 0 && _box.innerHTML.indexOf('未有剪報') < 0);

console.log(fails.length ? ('FAILURES: ' + fails.join(', ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
