// v20a297：Vera／關海媚成個移除——靜態斷言＋舊存檔 smoke test。
// 靜態：NPCS／MAP_NPC_TO_KEY／rom176MeiUnlocked／gift_prefs／npc_lines_core／
//       gift_react_copy／kwan 圖檔／endingRomance410＋commit48 vera 行全部已刪。
// Smoke：舊 save（帶 rel_vera／S.npcs.stylist／flag_vera_*）行 endingRomanceScene410
//       唔 crash、唔再出 Vera 文案（跌返通用獨身收尾）。
// 用法：node tests/test_r297_remove_vera_mei.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond) { if (!cond) fails.push(name); console.log((cond ? 'PASS ' : 'FAIL ') + name); }
function extractFn(name) {
  const i = html.indexOf('function ' + name + '(');
  if (i < 0) throw new Error('fn not found: ' + name);
  let depth = 0, j = html.indexOf('{', i);
  for (; j < html.length; j++) { if (html[j] === '{') depth++; else if (html[j] === '}') { depth--; if (depth === 0) break; } }
  return html.slice(i, j + 1);
}

// ---- (1) NPCS ----
const npcsBlock = html.slice(html.indexOf('const NPCS = {'), html.indexOf('const NPCS = {') + 4000);
ok('NPCS 冇 stylist 條目', !/^\s*stylist:\{/m.test(npcsBlock));
ok('NPCS 冇 mei 條目', !/^\s*mei:\{/m.test(npcsBlock));
ok('NPCS 其餘 7 人在位', ['colleague', 'director', 'rival', 'reporter', 'lan', 'xu', 'agent'].every(k => new RegExp('^\\s*' + k + ':\\{', 'm').test(npcsBlock)));

// ---- (2) MAP／閘／旗 ----
ok('MAP_NPC_TO_KEY 冇 stylist', html.indexOf('stylist:"vera"') < 0);
ok('MAP_NPC_TO_KEY 新值在位', html.indexOf('const MAP_NPC_TO_KEY = { colleague:"hiu", reporter:"choi" };') >= 0);
ok('rom176MeiUnlocked 已刪', html.indexOf('rom176MeiUnlocked') < 0);
ok('全檔零關海媚（v151 歷史註解除外）', html.split('關海媚').length - 1 === 1 && html.indexOf('v151 退役：關海媚名禁令已撤') >= 0);
ok('全檔零 npc_vera', html.indexOf('npc_vera') < 0);
ok('全檔零 rel_vera／flag_vera／kwan_hoimei', html.indexOf('rel_vera') < 0 && html.indexOf('flag_vera') < 0 && html.indexOf('kwan_hoimei') < 0);
ok('全檔零 R_vera_（WF2 表頭註解除外）', (html.match(/R_vera_/g) || []).length === 1 && html.indexOf('R_vera_* 5 條已刪') >= 0);
ok('endingRomance410／commit48 vera 行已刪', html.indexOf('vera: line("R_vera_meet"') < 0);
ok('almost 揀序冇 vera', html.indexOf('"vera", "lan"') < 0 && html.indexOf('r.line==="vera"') < 0);
ok('E1／default 結局散文冇當紅花旦', html.indexOf('那位當紅花旦') < 0 && html.indexOf('當紅花旦唔入名冊') < 0);

// ---- (3) content packs ----
const prefs = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gift_prefs.json'), 'utf8'));
ok('gift_prefs 冇 vera', !('vera' in (prefs.npcs || {})));
const lines = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'npc_lines_core.json'), 'utf8'));
ok('npc_lines_core 冇 stylist', !('stylist' in lines));
const react = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gift_react_copy.json'), 'utf8'));
ok('gift_react entries 44 條零 vera', react.entries.length === 44 && !react.entries.some(e => e.npcKey === 'vera'));
ok('gift_react crisis 7 條零 vera', react.crisis.length === 7 && !react.crisis.some(e => e.npcKey === 'vera'));
ok('gift_react byKey 44 條零 vera', Object.keys(react.byKey).length === 44 && !Object.keys(react.byKey).some(k => k.indexOf('vera:') === 0));
const cast = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'cast_main.json'), 'utf8'));
ok('cast_main 冇 kwan_hoimei', !(cast.npcs || []).some(e => e.id === 'kwan_hoimei'));

// ---- (4) assets ----
ok('kwan_hoimei_base.webp 已刪', !fs.existsSync(path.join(ROOT, 'assets', 'story', 'fullbody', 'kwan_hoimei_base.webp')));
ok('kwan_hoimei_serious.webp 已刪', !fs.existsSync(path.join(ROOT, 'assets', 'story', 'fullbody', 'kwan_hoimei_serious.webp')));

// ---- (5) 舊存檔 smoke test：帶 vera 旗／好感行結局呈現唔 crash、唔出 Vera 文案 ----
try {
  // 手法同 test_br89_logic.js：extractFn 抽真身，new Function 傳 S 入去行。
  const src = extractFn('endingFlag410') + '\n' + extractFn('endingRomanceScene410');
  const mk = (S) => new Function('S', src + '\nreturn { endingRomanceScene410 };')(S);
  const oldSaveS = {
    dayIndex: 700, npcs: { colleague: 8, director: 4, stylist: 5, rival: 6, reporter: 3, agent: 12 },
    story: { rel: { rel_vera: 6, rel_hiu: 2 }, flags: { flag_vera_commit: 1, flag_vera_be: 1, flag_vera_he: 1 }, done: {} },
    flags: { flag_vera_t5: 1 },
  };
  const out = mk(oldSaveS).endingRomanceScene410({ career: 'E0', romance: { line: 'vera', kind: 'almost' } });
  ok('舊 save vera almost 唔 crash', typeof out === 'string' && out.length > 0);
  ok('舊 save vera almost 唔出 Vera 文案', out.indexOf('Vera') < 0 && out.indexOf('領口') < 0);
  ok('舊 save vera almost 跌返通用收尾', out.indexOf('那晚收工，你一個人走去搭車') >= 0);
} catch (e) {
  ok('舊 save smoke test (' + e.message + ')', false);
}

console.log(fails.length ? ('FAILURES: ' + fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
