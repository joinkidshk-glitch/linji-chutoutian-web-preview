// v343 crisis 頁首年份測試：CONTRA98_WHEN_FIX 表值 1989→1990，頁首顯示 1992。
// 背景：drive-342 實駕發現 R_choi_crisis 頁首「主線 · 1991冬」、R_hiu_crisis 1991秋
//（期望 1992）。根因：CONTRA98_WHEN_FIX（載入時 contra98FixNodeWhen，行喺 years66Walk
// 之前）覆寫節點 when/eraTag 做 1989 舊曆值 → walk／顯示 +2 → 1991；v342 改嘅 JSON
// when（1990）俾表冚住完全無效。v342 沙盒用 soft 路徑（spPlayerMeta_softSeasonFrom，
// 讀 when）推算出 1992，同 live 路徑（spPlayerMeta 讀 eraTag 優先）唔同——今次抽
// live 真函數 spPlayerMeta 行完整載入路徑，唔齋推算。
// 用法：node tests/test_r343_crisis_year_fix.js
const fs = require('fs');
const path = require('path');
const rootDir = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(rootDir, 'index.html'), 'utf8');
const packVH = JSON.parse(fs.readFileSync(path.join(rootDir, 'content', 'story_detail_romance_vera_hiu_choi.json'), 'utf8'));
const packLX = JSON.parse(fs.readFileSync(path.join(rootDir, 'content', 'story_detail_romance_lan_xu.json'), 'utf8'));

let pass = 0, fail = 0;
function ok(name, cond){
  if(cond){ pass++; console.log('  ok - ' + name); }
  else { fail++; console.log('  FAIL - ' + name); }
}

function extractFn(decl){
  const i = html.indexOf(decl);
  if(i<0) throw new Error('fn not found: '+decl);
  let j = html.indexOf('{', i), depth = 0, k = j;
  for(; k<html.length; k++){
    if(html[k]==='{') depth++;
    else if(html[k]==='}'){ depth--; if(depth===0){ k++; break; } }
  }
  return html.slice(i, k);
}
function extractConst(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) throw new Error('const not found: '+name);
  let depth = 0, started = false;
  for(let k=i; k<html.length; k++){
    const ch = html[k];
    if(ch==='{'||ch==='['){ depth++; started = true; }
    else if(ch==='}'||ch===']'){ depth--; if(started && depth===0) return html.slice(i, k+1)+';'; }
    else if(ch===';' && !started) return html.slice(i, k+1);
  }
  throw new Error('const end not found: '+name);
}

/* ---- 環境 stub（spPlayerMeta live 路徑依賴）---- */
var START = { y:1990, m:3, d:7 };
var S = { dayIndex: 1000 };
var calendarSeason = function(){ return "冬"; };

const SRC = [
  // YEARS66 walk
  extractConst('YEARS66_SHIFT'),
  extractConst('YEARS66_OLD_MIN'),
  extractConst('YEARS66_TOKEN_RE'),
  extractFn('function years66ShiftYear'),
  extractFn('function years66ShiftText'),
  extractConst('YEARS66_SKIP_KEYS'),
  extractConst('YEARS66_YEAR_KEYS'),
  extractFn('function years66Walk'),
  // CONTRA98 載入覆寫（行喺 walk 之前）
  extractConst('CONTRA98_WHEN_FIX'),
  extractConst('CLEAN100_WHEN_FIX'),
  extractFn('function contra98FixNodeWhen'),
  // 頁首 live 路徑（spPlayerMeta）＋ soft 路徑（對照）
  extractFn('function spSoftSeasonChar'),
  extractFn('function spSoftLane'),
  extractFn('function spSoftSeasonLine'),
  extractFn('function spPlayerMeta_softSeasonFrom'),
  extractFn('function spPlayerMeta(node, pack, label)'),
].join('\n')
 .replace('const YEARS66_SHIFT =', 'var YEARS66_SHIFT =')
 .replace('const YEARS66_OLD_MIN =', 'var YEARS66_OLD_MIN =')
 .replace('const YEARS66_TOKEN_RE =', 'var YEARS66_TOKEN_RE =')
 .replace('const YEARS66_SKIP_KEYS =', 'var YEARS66_SKIP_KEYS =')
 .replace('const YEARS66_YEAR_KEYS =', 'var YEARS66_YEAR_KEYS =')
 .replace('const CONTRA98_WHEN_FIX =', 'var CONTRA98_WHEN_FIX =')
 .replace('const CLEAN100_WHEN_FIX =', 'var CLEAN100_WHEN_FIX =');
eval(SRC);

ok('harness: contra98FixNodeWhen／years66Walk／spPlayerMeta 載入',
  typeof contra98FixNodeWhen === 'function' && typeof years66Walk === 'function' && typeof spPlayerMeta === 'function');

/* ---- 靜態：表值已改 1990、舊 1989 值清零 ---- */
ok('表值 R_choi_crisis＝1990冬／era_1990_winter_gossip',
  CONTRA98_WHEN_FIX.R_choi_crisis && CONTRA98_WHEN_FIX.R_choi_crisis[0] === '1990冬' && CONTRA98_WHEN_FIX.R_choi_crisis[1] === 'era_1990_winter_gossip');
ok('表值 R_hiu_crisis＝1990秋／era_1990_autumn_anni',
  CONTRA98_WHEN_FIX.R_hiu_crisis && CONTRA98_WHEN_FIX.R_hiu_crisis[0] === '1990秋' && CONTRA98_WHEN_FIX.R_hiu_crisis[1] === 'era_1990_autumn_anni');
ok('index.html 無殘留 1989 crisis 表值',
  html.indexOf('R_choi_crisis:["1989冬"') < 0 && html.indexOf('R_hiu_crisis:["1989秋"') < 0);

/* ---- 完整載入路徑：contra98FixNodeWhen → years66Walk → spPlayerMeta ---- */
function loadPacks(){
  const vh = JSON.parse(JSON.stringify(packVH));
  const lx = JSON.parse(JSON.stringify(packLX));
  contra98FixNodeWhen([vh, lx]);
  [vh, lx].forEach(p => years66Walk(p, null));
  const byId = {};
  [vh, lx].forEach(p => (p.nodes||[]).forEach(n => { if(n && n.id) byId[n.id] = n; }));
  return byId;
}

const nodes = loadPacks();
const EXPECT = {
  R_choi_crisis: '主線 · 1992冬',
  R_hiu_crisis:  '主線 · 1992秋',
  R_lan_crisis:  '主線 · 1992秋',
  R_xu_push2:    '主線 · 1992秋',
  R_xu_crisis:   '主線 · 1992秋',
};
Object.keys(EXPECT).forEach(id => {
  const n = nodes[id];
  ok(id + ' 節點在位', !!n);
  if(!n) return;
  ok(id + ' 頁首（live spPlayerMeta）＝' + EXPECT[id], spPlayerMeta(n) === EXPECT[id]);
  ok(id + ' 頁首（soft 路徑）＝' + EXPECT[id], spPlayerMeta_softSeasonFrom(n, {}) === EXPECT[id]);
});
ok('R_choi_crisis runtime when＝1992冬（walk 後）', nodes.R_choi_crisis && nodes.R_choi_crisis.when === '1992冬');
ok('R_hiu_crisis runtime when＝1992秋（walk 後）', nodes.R_hiu_crisis && nodes.R_hiu_crisis.when === '1992秋');
ok('R_choi_crisis runtime eraTag＝era_1990_winter_gossip（walk 唔掂）', nodes.R_choi_crisis && nodes.R_choi_crisis.eraTag === 'era_1990_winter_gossip');
ok('R_hiu_crisis runtime eraTag＝era_1990_autumn_anni（walk 唔掂）', nodes.R_hiu_crisis && nodes.R_hiu_crisis.eraTag === 'era_1990_autumn_anni');

/* ---- 反證：表值還原 1989 → 頁首跌返 1991（證明測試捉到原 bug）---- */
const savedChoi = CONTRA98_WHEN_FIX.R_choi_crisis;
const savedHiu = CONTRA98_WHEN_FIX.R_hiu_crisis;
CONTRA98_WHEN_FIX.R_choi_crisis = ['1989冬', 'era_1989_winter_gossip'];
CONTRA98_WHEN_FIX.R_hiu_crisis = ['1989秋', 'era_1989_autumn_anni'];
const oldNodes = loadPacks();
ok('反證：舊表值 R_choi_crisis 頁首＝1991冬（原 bug 重現）', spPlayerMeta(oldNodes.R_choi_crisis) === '主線 · 1991冬');
ok('反證：舊表值 R_hiu_crisis 頁首＝1991秋（原 bug 重現）', spPlayerMeta(oldNodes.R_hiu_crisis) === '主線 · 1991秋');
CONTRA98_WHEN_FIX.R_choi_crisis = savedChoi;
CONTRA98_WHEN_FIX.R_hiu_crisis = savedHiu;

/* ---- JSON when 雙保險未郁（v342 已改 1990，今票唔掂）---- */
function jsonNode(pack, id){ return (pack.nodes||[]).find(n => n && n.id === id); }
ok('JSON R_choi_crisis when 仍＝1990冬', jsonNode(packVH, 'R_choi_crisis').when === '1990冬');
ok('JSON R_hiu_crisis when 仍＝1990', jsonNode(packVH, 'R_hiu_crisis').when === '1990');

console.log('');
console.log('TOTAL ' + pass + ' PASS / ' + fail + ' FAIL');
process.exit(fail ? 1 : 0);
