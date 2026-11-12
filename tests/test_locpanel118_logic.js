// v20a118 LOCPANEL118 邏輯測試：地點面板（額度 pill＋負責人對照＋選項圖標）。
//   斷言：quota html 數字／點數／「已到埗」行只喺扣數嗰陣出；15 地點負責人對照——
//   11 間機構老闆圖源逐字等於 GIG_ISSUER_FIGURE_MAP30V2（證明唔係 hardcode）、何生經
//   S-30 fallback、霞姐／禮品檔名牌無圖、醫院 null、未知地點 null；選項圖標按掣類
//   揀 v112 手繪圖、揀唔到回空字串。
// 反證：pristine main（v117）跑呢檔要 throw（locpanel118 函數唔存在）；
//   對照表改指新檔（v116）嗰陣，ownerFor 要自動跟新 src（測試讀真 map，唔寫死路徑）。
// 用法：node tests/test_locpanel118_logic.js [path-to-index.html]
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
function extractConstObj(name){
  const i = html.indexOf('const ' + name);
  if(i < 0) throw new Error('const not found: ' + name);
  let depth = 0, j = html.indexOf('{', i);
  for(; j < html.length; j++){
    if(html[j] === '{') depth++;
    else if(html[j] === '}'){ depth--; if(depth === 0) break; }
  }
  return html.slice(i, j + 1);
}
function extractConstLine(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('const not found: ' + name);
  const j = html.indexOf('\n', i);
  return html.slice(i, j);
}
// 真 map＋真 cap＋真 icon map＋真函數，同一沙箱（唔寫死路徑／圖檔名）
const sandboxSrc =
  extractConstObj('GIG_ISSUER_FIGURE_MAP30V2') + ';\n' +
  extractConstLine('TRAVEL114_DAILY_CAP') + '\n' +
  extractConstObj('EMOJI_ICON112') + ';\n' +
  'const esc = (s)=>String(s==null?"":s);\n' +
  'var S = { dayIndex: 5 };\nvar locpanel118SpentVisit = null;\n' +
  ['gigIssuerFigure30v2', 'iconHtml112', 'locpanel118OwnerFor',
   'locpanel118QuotaHtml', 'locpanel118ActIcon', 'locpanel118ArrivedNow'].map(extractFn).join('\n') +
  '\nreturn { locpanel118OwnerFor, locpanel118QuotaHtml, locpanel118ActIcon, locpanel118ArrivedNow, GIG_ISSUER_FIGURE_MAP30V2,' +
  ' setVisit: (v)=>{ locpanel118SpentVisit = v; }, setDay: (d)=>{ S.dayIndex = d; } };';
const api = new Function(sandboxSrc)();
const MAP = api.GIG_ISSUER_FIGURE_MAP30V2;

/* ---- (1) 額度 pill ---- */
let h = api.locpanel118QuotaHtml(1, 1, true);
ok('pill 入場後：已用 1 / 2', h.indexOf('已用 1 / 2') >= 0);
ok('pill 入場後：仲可以去 1 個地方', h.indexOf('仲可以去 1 個地方') >= 0);
ok('pill 入場後：有「✓ 已到埗，扣咗 1 次出行額度」', h.indexOf('✓ 已到埗，扣咗 1 次出行額度') >= 0);
ok('pill 點數：2 粒點、1 粒已用', (h.match(/lp118-dot[ "]/g) || []).length === 2 && (h.match(/lp118-dot used/g) || []).length === 1);
h = api.locpanel118QuotaHtml(1, 1, false);
ok('pill 免費返嚟：數字照舊（已用 1 / 2），冇「已到埗」行', h.indexOf('已用 1 / 2') >= 0 && h.indexOf('已到埗') < 0);
h = api.locpanel118QuotaHtml(0, 2, true);
ok('pill 未入場：已用 0 / 2、仲可以去 2 個地方、0 粒已用',
   h.indexOf('已用 0 / 2') >= 0 && h.indexOf('仲可以去 2 個地方') >= 0 && (h.match(/lp118-dot used/g) || []).length === 0);
h = api.locpanel118QuotaHtml(2, 0, true);
ok('pill 用盡：已用 2 / 2、仲可以去 0 個地方、2 粒已用',
   h.indexOf('已用 2 / 2') >= 0 && h.indexOf('仲可以去 0 個地方') >= 0 && (h.match(/lp118-dot used/g) || []).length === 2);

/* ---- (1b) 已到埗行：探訪記憶（巧遇／WF4 攔截後免費返嚟、modal 免費重開都出） ---- */
const L_AG = { id: 'agency_ho' };
ok('arrived：今次扣數即出', api.locpanel118ArrivedNow(L_AG, true) === true);
ok('arrived：冇扣數、冇記憶唔出', api.locpanel118ArrivedNow(L_AG, false) === false);
api.setVisit({ loc: 'agency_ho', day: 5 });
ok('arrived：免費返嚟、同地點同日（探訪記憶）照出', api.locpanel118ArrivedNow(L_AG, false) === true);
ok('arrived：免費返嚟、唔同地點唔出', api.locpanel118ArrivedNow({ id: 'cafe_cha' }, false) === false);
api.setDay(6);
ok('arrived：免費返嚟、同地點但換日唔出', api.locpanel118ArrivedNow(L_AG, false) === false);
api.setDay(5); api.setVisit(null);
ok('arrived：記憶清走後唔出', api.locpanel118ArrivedNow(L_AG, false) === false);

/* ---- (2) 15 地點負責人對照 ---- */
const ORGS11 = ['film_lion', 'rec_hk', 'tvb_longmen', 'tvb_kowloon', 'tvb_harbour',
  'film_cotton', 'film_harbour', 'ad_central', 'ad_adm', 'rec_wanchai', 'rec_star'];
ORGS11.forEach((lid) => {
  const o = api.locpanel118OwnerFor(lid);
  ok('老闆 ' + lid + '：圖源逐字等於對照表（唔 hardcode）', !!o && o.src === MAP[lid].src);
  ok('老闆 ' + lid + '：名牌＝名 · 機構＋職位', !!o && o.name === MAP[lid].name && o.sub === MAP[lid].org + MAP[lid].role);
});
let o = api.locpanel118OwnerFor('agency_ho');
ok('何生：圖源＝S-30 fallback（ho_sang_base）', !!o && o.src.indexOf('ho_sang_base.webp') >= 0);
ok('何生：名牌「何生 · 事務所老闆」', !!o && o.name === '何生' && o.sub === '事務所老闆');
o = api.locpanel118OwnerFor('cafe_cha');
ok('霞姐：企立圖＋名牌（v20a131 B1）、「霞姐 · 金龍茶餐廳老闆娘」',
   !!o && !o.noFig && o.src.indexOf('xia_jie_base.webp') >= 0 && o.name === '霞姐' && o.sub === '金龍茶餐廳老闆娘');
o = api.locpanel118OwnerFor('gift_shop');
ok('禮品檔：企立圖＋名牌（v20a131 B1）、「老闆娘 · 廟街禮品檔」',
   !!o && !o.noFig && o.src.indexOf('gift_lady_base.webp') >= 0 && o.name === '老闆娘' && o.sub === '廟街禮品檔');
ok('醫院：null（唔出人、連名牌都唔出）', api.locpanel118OwnerFor('hospital') === null);
ok('未知地點：null（唔用何生頂替）', api.locpanel118OwnerFor('home') === null && api.locpanel118OwnerFor('nope') === null);

/* ---- (3) 選項圖標 ---- */
const ICON_CASES = [
  ['播劇情：《上岸路》', 'act-priority act-story', 'icon_mask.png'],
  ['劇情已完成：《上岸路》', 'act-story', 'icon_mask.png'],
  ['打聽電視城規矩', 'act-priority act-ask', 'icon_tv.png'],
  ['同何生傾談', 'act-priority', 'icon_people.png'],
  ['送禮：林曉晴', 'act-priority', 'icon_gift.png'],
  ['只查看通告欄', 'act-priority', 'icon_briefcase.png'],
  ['查看檔期：《夜班廠景》', '', 'icon_briefcase.png'],
  ['試鏡入口：《夜班廠景》', '', 'icon_clapper.png'],
  ['報名：旁聽對戲／綵排', 'act-priority', 'icon_fitness.png'],
  ['進行演技訓練', 'act-priority', 'icon_fitness.png'],
  ['休息室歇陣', 'act-priority', 'icon_sleep.png'],
  ['買禮物', 'act-priority', 'icon_gift.png'],
  ['身體檢查', '', 'icon_hospital.png'],
  ['醫院有咩用？', '', 'icon_book.png'],
  ['聽風聲', 'act-priority', 'icon_radio.png'],
  ['鄧麗萍約談排片', 'act-priority act-story', 'icon_phone.png'],
];
ICON_CASES.forEach(([title, cls, stem]) => {
  const out = api.locpanel118ActIcon(title, cls);
  ok('圖標「' + title + '」→ ' + stem, out.indexOf(stem) >= 0 && out.indexOf('act-ic118') >= 0);
});
ok('圖標：揀唔到合適圖標回空字串（唔用 emoji）', api.locpanel118ActIcon('隨便一個掣', '') === '');
ok('圖標：冇 emoji 殘留（輸出唔含 emoji 區段）',
   !/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/u.test(api.locpanel118ActIcon('播劇情：X', 'act-story')));

console.log('---');
console.log(fails.length ? 'FAIL: ' + fails.join('; ') : 'PASS');
process.exit(fails.length ? 1 : 0);
