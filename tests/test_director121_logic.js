// v20a121 DIRECTOR121 邏輯測試：導演欄職銜關鍵字規則（取代 v117 窮舉 Set）。
//   斷言：(1) live pool 16 個職銜 distinct 值（46 張）全部濾走；(2) 113 個真名
//   （137 張）逐個逐關鍵字零碰撞、全部原樣出；(3) fallback「組製未公開」＋空值
//   唔出；(4) 29 個假想將來新職銜值全部擋到；(5) 每個關鍵字都有用——或者命中
//   實池值，或者命中將來值，唔留死關鍵字。
// 反證：同一檔內嵌舊 v117 Set（9 個值），逐個將來值驗舊規則擋唔到——喺 pristine
//   main（v118，仲係舊 Set）跑呢檔，(4) 嘅新規則斷言要 FAIL（因為新函數唔存在，
//   抽取即 throw），(5) 同 (4) 嘅舊規則對照要成立。
// 數據來源：qa121/census_main.json（Playwright 實駕 dump，window.GIGS 183 張，
//   ?softPreview=1 新遊戲槽 3）。真名表內嵌喺呢檔，唔依賴 census 檔，獨立可跑。
// 用法：node tests/test_director121_logic.js [path-to-index.html]
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
function extractConstArray(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('const not found: ' + name);
  let depth = 0, j = html.indexOf('[', i);
  for(; j < html.length; j++){
    if(html[j] === '[') depth++;
    else if(html[j] === ']'){ depth--; if(depth === 0) break; }
  }
  return html.slice(i, j + 1);
}
// 真關鍵字表＋真函數，同一沙箱（唔寫死規則，讀 index.html 現行版本）
const sandboxSrc =
  extractConstArray('GIG_DIRECTOR_ROLE_KEYWORDS121') + ';\n' +
  extractFn('gigDirectorLabel') + '\n' +
  extractFn('gigDirectorIsRoleValue121') + '\n' +
  extractFn('gigDirectorRealName117') + '\n' +
  'return { GIG_DIRECTOR_ROLE_KEYWORDS121, gigDirectorIsRoleValue121, gigDirectorRealName117 };';
const api = new Function(sandboxSrc)();
const KW = api.GIG_DIRECTOR_ROLE_KEYWORDS121;
const realName = (d)=> api.gigDirectorRealName117({ director: d });

// ---- (0) 關鍵字表本身 ----
ok('關鍵字表係 25 個字、無重複', Array.isArray(KW) && KW.length === 25 && new Set(KW).size === 25);
ok('關鍵字全部係 2–3 字中文（唔留單字通配，防誤殺）', KW.every(k => typeof k === 'string' && [...k].length >= 2 && [...k].length <= 3));

// ---- (1) live pool 16 個職銜值（46 張）全部濾走 ----
//   計數：副導×19、監製×7、副導阿標×4、廣告助導×3、導演×2、其餘 11 個值各×1。
const GENERIC = [
  ['副導', 19], ['監製', 7], ['副導阿標', 4], ['廣告助導', 3], ['導演', 2],
  ['特輯副導', 1], ['場務阿強', 1], ['外景場記', 1], ['平面攝影師阿忠', 1],
  ['錄音室助導', 1], ['監製助理', 1], ['武指領班', 1], ['武術指導', 1],
  ['客戶代表', 1], ['副導阿成', 1], ['宣傳部阿玲', 1],
];
ok('職銜值 16 個 distinct、合共 46 張（同 census 一致）',
  GENERIC.length === 16 && GENERIC.reduce((a, x) => a + x[1], 0) === 46);
GENERIC.forEach(([v, n]) => ok('職銜值濾走：' + v + ' ×' + n, realName(v) === ''));

// ---- (2) 113 個真名（137 張）逐個零碰撞、原樣出 ----
const REAL_NAMES = ["何偉龍", "何家明", "何家輝", "何志光", "劉偉明", "劉偉華", "吳偉強", "吳啟泰", "吳天水", "吳家偉", "吳家輝", "吳志華", "周偉強", "周家明", "周文傑", "孫偉明", "孫國榮", "張伯良", "張偉強", "張偉明", "張堅偉", "張家偉", "張建華", "張德輝", "張志強", "張志輝", "徐天華", "徐建文", "徐志強", "方浩源", "曾偉明", "李伯良", "李啟泰", "李國強", "李國明", "李國輝", "李家輝", "李志強", "李志豪", "李志輝", "李志遠", "李慕華", "李柏龍", "李耀華", "杜偉輝", "杜家明", "杜明峰", "杜琪明", "林偉強", "林偉明", "林偉業", "林兆聲", "林家傑", "林柏堅", "林柏生", "林柏謙", "林耀宗", "梁家明", "梁志誠", "洪家輝", "王嘉明", "王國輝", "王天樂", "王家明", "王家輝", "王志輝", "王福良", "程小明", "程智東", "蘇偉文", "蘇建邦", "袁和明", "許安明", "許家強", "趙國華", "趙家明", "趙志成", "趙文傑", "趙文輝", "趙文龍", "鄭偉明", "鄭家明", "鄭志偉", "鄭漢雄", "陳啟文", "陳嘉明", "陳大文", "陳大龍", "陳子健", "陳子強", "陳子揚", "陳建國", "陳志輝", "陳志達", "陳耀明", "陳達志", "陳鏡鋒", "韋國強", "顧家明", "高志威", "高志強", "高志明", "麥家輝", "黃偉倫", "黃兆基", "黃家傑", "黃家明", "黃家輝", "黃建明", "黃志偉", "黃志豪", "黃志鳴", "黃肇文"]
;
ok('真名表 113 個名', REAL_NAMES.length === 113);
const missed = REAL_NAMES.filter(n => realName(n) !== n);
ok('113 個真名全部原樣出（零誤殺）', missed.length === 0);
if(missed.length) console.log('  誤殺：' + missed.join('、'));
// 逐關鍵字碰撞表：每個關鍵字對 113 真名嘅命中數必須係 0。
KW.forEach(k => {
  const hits = REAL_NAMES.filter(n => n.indexOf(k) >= 0);
  ok('關鍵字「' + k + '」對 113 真名零碰撞', hits.length === 0);
});

// ---- (3) fallback＋空值 ----
ok('fallback「組製未公開」唔出', realName('組製未公開') === '');
ok('缺 director（undefined）唔出', api.gigDirectorRealName117({}) === '');
ok('空字串 director 唔出', realName('') === '');
ok('只有空白 director 唔出', realName('   ') === '');
ok('null gig 唔出', api.gigDirectorRealName117(null) === '');

// ---- (4) 假想將來新職銜值：新規則全部擋到，舊窮舉全部擋唔到（反證） ----
const OLD_GENERIC117 = new Set(['副導', '特輯副導', '副導阿標', '廣告助導', '場務阿強', '外景場記', '平面攝影師阿忠', '錄音室助導', '組製未公開']);
const oldRealName = (d) => { const s = String(d || '').trim(); if(!s || OLD_GENERIC117.has(s)) return ''; return s; };
const FUTURE = ['執行導演', '副導阿強', '監製阿文', '外景副導', '攝影阿明', '導演助理',
  '武術指導阿強', '宣傳阿珍', '導演待定', '場務阿文', '廣告監製', '製片阿強',
  '燈光師阿輝', '收音阿明', '剪接阿文', '編劇阿文', '統籌阿強', '製作部阿文',
  '後期阿明', '幕後阿強', '美術指導', '服裝指導', '動作指導', '導演未公開',
  '監製待定', '場務組阿文', '副導阿成', '客戶經理', '宣傳部阿玲'];
ok('將來值 29 個（任務要求 ≥5）', FUTURE.length === 29);
FUTURE.forEach(v => ok('將來值新規則擋到：' + v, realName(v) === ''));
const oldBlocked = FUTURE.filter(v => oldRealName(v) === '');
ok('反證：舊 v117 窮舉 29 個將來值一個都擋唔到（' + oldBlocked.length + ' 個擋到即 FAIL）', oldBlocked.length === 0);
// 註：「副導阿成」「宣傳部阿玲」其實已經喺 live pool（各×1，見 (1)），舊規則連
// 現行值都漏——反證唔只係將來式。

// ---- (5) 每個關鍵字都有用：命中實池值或將來值，唔留死關鍵字 ----
KW.forEach(k => {
  const hitsLive = GENERIC.some(([v]) => v.indexOf(k) >= 0) || '組製未公開'.indexOf(k) >= 0;
  const hitsFuture = FUTURE.some(v => v.indexOf(k) >= 0);
  ok('關鍵字「' + k + '」有用（實池／將來至少命中一個）', hitsLive || hitsFuture);
});

console.log('---');
console.log(fails.length ? 'FAIL: ' + fails.join('; ') : 'PASS');
process.exit(fails.length ? 1 : 0);
