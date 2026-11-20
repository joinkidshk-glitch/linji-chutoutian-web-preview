// v20a266 林曉晴《留低》覆寫層移植測試（ROMANCE_V158_OVERRIDES，v158 WIP 移植）。
// 只測曉晴層：apply 命中 5 節點、鏈重排（choices／flags／phase／openConditions C→N）、
// 語體（beats 廣東話／synopsis 書面語）、冪等、commit 層唔郁；
// prepare-hook：crisis 開場三版、ending 事業收尾＋承諾收口、走收尾成組換、choices 唔郁；
// 載入鏈：V158 → contra98 → years66Walk 之後，crisis 1991秋／push2 1991冬／ending 1992秋。
// 移植適配（相對舊 WIP）：(1) openConditions C→N（C4→N4、C8→N9、C9→N10、C12→N14）；
// (2) 5 段 synopsis 改寫做香港式書面語；(3) packs 刪 rom.tang；
// (4) CONTRA98_WHEN_FIX 兩項已由 v223 落地，呢度唔郁，只斷言在位。
// 用法：node tests/test_hiu266_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const rootDir = path.dirname(htmlPath);
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }
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
function extractConst(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('const not found: ' + name);
  let depth = 0, started = false, j = i;
  for(; j < html.length; j++){
    const c = html[j];
    if(c === '{' || c === '['){ depth++; started = true; }
    else if(c === '}' || c === ']'){ depth--; if(started && depth === 0){ j++; break; } }
    else if(c === ';' && !started) { j++; break; }
  }
  return html.slice(i, j);
}

/* ---- (1) 靜態 ---- */
ok('靜態：V158 表 5 節點＋apply＋載入鏈呼叫', html.includes('const ROMANCE_V158_OVERRIDES') && html.includes('function applyRomanceV158Overrides158') && html.includes('applyRomanceV158Overrides158();'));
ok('靜態：V158 表有兩封信三揀一＋新旗', html.includes('hiu_deal_refused') && html.includes('hiu_deal_signed') && html.includes('hiu_family_go') && html.includes('C_hiu_push1_c'));
ok('靜態：C→N——舊 C 閘全無，新 N 閘在位', !html.includes('"openConditions": ["C4"]') && !html.includes('"openConditions": ["C8"]') && !html.includes('"openConditions": ["C9"]') && !html.includes('"phase_P4", "C12"') && html.includes('"openConditions": ["N4"]') && html.includes('"openConditions": ["N9"]') && html.includes('"openConditions": ["N10"]') && html.includes('"phase_P4", "N14"'));
ok('靜態：CONTRA98 時期已在位（crisis 1990秋／ending 1990秋，v223＋v343）', html.includes('R_hiu_crisis:["1990秋"') && html.includes('R_hiu_ending:["1990秋"'));
ok('靜態：apply fn packs 無 rom.tang（v152 已刪）', (()=>{ const fn = extractFn('applyRomanceV158Overrides158'); return fn.includes('rom.veraHiuChoi') && fn.includes('rom.lanXu') && !fn.includes('rom.tang'); })());
ok('靜態：prepare-hook 在位＋StoryPlay 掛鈎', html.includes('function enc158PrepareNode') && html.includes('enc158PrepareNode(node)'));

/* ---- sandbox（V158 層） ---- */
const packHiu = JSON.parse(fs.readFileSync(path.join(rootDir, 'content', 'story_detail_romance_vera_hiu_choi.json'), 'utf8'));
function clone(o){ return JSON.parse(JSON.stringify(o)); }
const CANT = ['嘅','咗','喇','呀','啦','㗎','呢','嗰','邊','咁','仲','都','先','唔','冇','係','你','我','佢','哋','啲','返','埋','搵','講','睇','食','瞓','企','行','入','出','去','嚟','到','過','開','收','攞','畀','幫','等','知','明','想','要','會','可','得','好','真','大','細','新','舊','夜','朝','晏','廠','戲','歌','人','心','錢'];
const WRITTEN = ['的','了','沒有','什麼','為什麼','他們','我們','不是','著'];
const SYN_CANT = ['喺','咗','佢','搵','嘢','嗰','呢','啦','喇','㗎','唔','冇','哋','啲','瞓','嘅','咁','一齊','同埋','走埋','叫咗','係咪','係咁','返嚟','返工','返去','傾下','識咗'];
const REAL_NAMES = ['周潤發','劉德華','張國榮','梅艷芳','陳百強','鄧麗君','成龍','周星馳','梁朝偉','張曼玉','王祖賢','林青霞','鍾楚紅','李連杰','洪金寶'];
function beatsText(node){ return (node.beats||[]).map(b=>(b.lines||[]).join('')).join(''); }
function countMarkers(txt, list){ let n = 0; for(const m of list){ let i = 0; while((i = txt.indexOf(m, i)) >= 0){ n++; i += m.length; } } return n; }
let _storyFlags = {};
function enc87StoryFlag(f){ return !!_storyFlags[f]; }

/* ---- (2) V158 層 apply ---- */
const T158 = eval(extractConst('ROMANCE_V158_OVERRIDES') + '\nROMANCE_V158_OVERRIDES;');
ok('V158：覆寫表 5 節點齊', Object.keys(T158).length === 5 && ['R_hiu_meet','R_hiu_push1','R_hiu_push2','R_hiu_crisis','R_hiu_ending'].every(id=>!!T158[id]));
const wire158 = { romance: { veraHiuChoi: clone(packHiu), lanXu: { nodes: [] } } };
const run158 = new Function('ROMANCE_V158_OVERRIDES', 'STORY_WIRE', 'V158_APPLIED158',
  'const V158A = V158_APPLIED158;\n' + extractFn('applyRomanceV158Overrides158').replace('V158_APPLIED158', 'V158A') + '\nreturn applyRomanceV158Overrides158();');
const appliedSet = new WeakSet();
const applied158 = run158(T158, wire158, appliedSet);
ok('V158：apply 命中 5 節點', applied158 === 5);
const byId158 = {};
wire158.romance.veraHiuChoi.nodes.forEach(n => { byId158[n.id] = n; });
const meet158 = byId158.R_hiu_meet, push1 = byId158.R_hiu_push1, push2 = byId158.R_hiu_push2, crisis = byId158.R_hiu_crisis, ending = byId158.R_hiu_ending;
ok('V158：meet 加靚女句、choices 唔郁', beatsText(meet158).indexOf('靚女') >= 0 && meet158.choices.length === 2 && meet158.choices[0].effects.flags[0] === 'flag_hiu_meet_exchange');
ok('V158：push1 兩封信三揀一＋新旗＋P1＋N4 閘', push1.beats.length === 7 && push1.choices.length === 3 && push1.choices.some(c=>c.id==='C_hiu_push1_c' && c.effects.flags[0]==='hiu_family_go') && push1.choices.some(c=>c.effects.flags[0]==='hiu_deal_refused' && c.effects.stats.rel_hiu===2) && push1.phase === 'P1' && JSON.stringify(push1.openConditions) === '["N4"]' && JSON.stringify(push1.flags_written) === '["hiu_deal_refused","hiu_deal_signed","hiu_family_go"]');
ok('V158：push2 承諾兩旗＋N10 閘＋when 1989冬', push2.choices.length === 2 && push2.choices[0].label === '我哋一齊捱' && push2.choices[0].effects.flags[0] === 'hiu_promise_together' && push2.choices[0].effects.stats.rel_hiu === 2 && push2.choices[1].effects.flags[0] === 'hiu_promise_support' && push2.choices[1].effects.stats.rel_hiu === 0 && JSON.stringify(push2.openConditions) === '["N10"]' && push2.when === '1989冬');
ok('V158：crisis 加新旗（舊旗保留）＋P2＋N9 閘＋鏈重排', crisis.choices[0].effects.flags.includes('hiu_given_role') && crisis.choices[0].effects.flags.includes('flag_hiu_crisis_yield') && crisis.choices[1].effects.flags.includes('hiu_lost_role') && crisis.phase === 'P2' && JSON.stringify(crisis.openConditions) === '["N9"]' && crisis.openConditionsAny.includes('hiu_deal_refused') && crisis.openConditionsAny.includes('flag_hiu_push2_date'));
ok('V158：ending P4＋N14 閘＋promise 旗＋commit 層唔郁', ending.phase === 'P4' && JSON.stringify(ending.openConditions) === '["phase_P4","N14"]' && ending.openConditionsAny.includes('hiu_promise_together') && ending.choices.length === 2 && ending.choices[0].id === 'C_hiu_ending_he' && ending.choices[0].effects.flags.includes('flag_hiu_commit') && ending.choices[1].id === 'C_hiu_ending_be');
ok('V158：冪等（第二次 applied = 0）', run158(T158, wire158, appliedSet) === 0);
for(const id of ['R_hiu_meet','R_hiu_push1','R_hiu_push2','R_hiu_crisis','R_hiu_ending']){
  const node = byId158[id], bt = beatsText(node);
  ok('V158 語體 beats：' + id + ' 廣東話 ≥25／書面語 0／冇年份／冇真人名／beats ≥300 字', countMarkers(bt, CANT) >= 25 && countMarkers(bt, WRITTEN) === 0 && !/199\d|198\d/.test(bt) && REAL_NAMES.every(x=>!bt.includes(x)) && bt.length >= 300);
  ok('V158 語體 synopsis：' + id + ' 書面語（廣東話標記 0／冇年份）', countMarkers(node.synopsis || '', SYN_CANT) === 0 && !/199\d|198\d/.test(node.synopsis || ''));
}
globalThis.__byId158 = byId158;

/* ---- (3) prepare-hook ---- */
eval(extractFn('enc158PrepareNode'));
{
  const byId158 = globalThis.__byId158;
  const mkNode = (id)=> clone(byId158[id]);
  _storyFlags = { hiu_deal_refused: 1 };
  ok('hook：crisis refused 開場換版', (()=>{ const src = mkNode('R_hiu_crisis'); const out = enc158PrepareNode(src); return !!out && out.beats[0].lines[0].indexOf('叫我留低') >= 0 && out.choices === src.choices; })());
  _storyFlags = { hiu_deal_signed: 1 };
  ok('hook：crisis signed 開場換版', (()=>{ const out = enc158PrepareNode(mkNode('R_hiu_crisis')); return !!out && out.beats[0].lines[0].indexOf('叫我簽') >= 0; })());
  _storyFlags = { hiu_family_go: 1 };
  ok('hook：crisis family_go 開場換版', (()=>{ const out = enc158PrepareNode(mkNode('R_hiu_crisis')); return !!out && out.beats[0].lines[0].indexOf('買咗機票') >= 0; })());
  _storyFlags = {};
  ok('hook：crisis 無旗 → null（原版照行）', enc158PrepareNode(mkNode('R_hiu_crisis')) === null);
  ok('hook：非目標節點 → null', enc158PrepareNode({ id:'R_hiu_meet', beats: clone(byId158.R_hiu_meet.beats) }) === null);
  _storyFlags = { hiu_deal_signed: 1, hiu_promise_support: 1 };
  ok('hook：ending signed 玉女收尾＋support 收口', (()=>{ const out = enc158PrepareNode(mkNode('R_hiu_ending')); return !!out && out.beats[0].lines[0].indexOf('叫我簽') >= 0 && out.beats[2].lines[1].indexOf('淨係林曉晴') >= 0 && out.beats[3].lines[0].indexOf('你撐我') >= 0 && out.beats[4].lines[0].indexOf('等佢開口') >= 0; })());
  _storyFlags = { hiu_family_go: 1 };
  ok('hook：ending 走收尾成組換（啟德機場送機）', (()=>{ const out = enc158PrepareNode(mkNode('R_hiu_ending')); return !!out && out.beats[0].lines[0].indexOf('啟德機場') >= 0 && out.beats[4].lines[0].indexOf('留低嗰張相') >= 0; })());
  _storyFlags = { hiu_deal_refused: 1, hiu_promise_together: 1 };
  ok('hook：ending refused＋together → null（表預設就係好收尾）', enc158PrepareNode(mkNode('R_hiu_ending')) === null);
  _storyFlags = { hiu_family_go: 1 };
  ok('hook：ending 走收尾 choices 唔郁（commit 層一字唔郁）', (()=>{ const src = mkNode('R_hiu_ending'); const out = enc158PrepareNode(src); return !!out && out.choices === src.choices && out.choices[0].id === 'C_hiu_ending_he'; })());
}

/* ---- (4) 載入鏈：V158 → contra98 → years66Walk ---- */
{
  eval([
    extractConst('YEARS66_SHIFT'), extractConst('YEARS66_OLD_MIN'), extractConst('YEARS66_TOKEN_RE'),
    extractConst('YEARS66_SKIP_KEYS'), extractConst('YEARS66_YEAR_KEYS'),
    extractFn('years66ShiftYear'), extractFn('years66ShiftText'), extractFn('years66Walk'),
    extractConst('CONTRA98_WHEN_FIX'), extractConst('CLEAN100_WHEN_FIX'), extractFn('contra98FixNodeWhen'),
    'globalThis.__CH158 = { CONTRA98_WHEN_FIX, contra98FixNodeWhen, years66Walk };',
  ].join('\n'));
  const T158b = eval(extractConst('ROMANCE_V158_OVERRIDES') + '\nROMANCE_V158_OVERRIDES;');
  const wireChain = { romance: { veraHiuChoi: clone(packHiu), lanXu: { nodes: [] } } };
  const run158b = new Function('ROMANCE_V158_OVERRIDES', 'STORY_WIRE', 'V158_APPLIED158',
    'const V158A = V158_APPLIED158;\n' + extractFn('applyRomanceV158Overrides158').replace('V158_APPLIED158', 'V158A') + '\nreturn applyRomanceV158Overrides158();');
  run158b(T158b, wireChain, new WeakSet());
  globalThis.__CH158.contra98FixNodeWhen([wireChain.romance.veraHiuChoi]);
  globalThis.__CH158.years66Walk(wireChain.romance.veraHiuChoi, null);
  const chainById = {};
  wireChain.romance.veraHiuChoi.nodes.forEach(n => { chainById[n.id] = n; });
  ok('載入鏈：crisis 頁首 1992秋（v343 表值 1990）', chainById.R_hiu_crisis.when === '1992秋');
  ok('載入鏈：push2 頁首 1991冬', chainById.R_hiu_push2.when === '1991冬');
  ok('載入鏈：ending 頁首 1992秋', chainById.R_hiu_ending.when === '1992秋');
  ok('載入鏈：meet 頁首 1990春不變', chainById.R_hiu_meet.when === '1990春');
}

console.log(fails.length ? ('\nFAILURES: ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
