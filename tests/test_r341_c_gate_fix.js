// v20a341 C-id 閘門修復邏輯測試：四個 ENC79 beat 閘由舊 C id 改讀 N id
//   (1) 靜態：liu_foreshadow／liu_steal 讀 N9、liu_clash 讀 N16、mak_intel 讀 N12；
//       enc83NodeDone("C…") 全檔零殘留；註解唔再寫 C8＝N9 等舊對照。
//   (2) 真跑：抽真 enc83NodeDone＋enc83Flag＋enc79TierOf＋ENC79_BEATS，
//       StoryOC.isDone 以 _doneNodes 模擬真實存檔 story.done（只寫 N id）：
//       播種 N9 → foreshadow／steal 閘開；無 N9 → 唔開；淨播種 C8 → 唔開（舊死閘行為已除）。
//       N16／N12 同理。
// 反證：喺 v340 index 上行 → 靜態＋真跑 N 播種斷言乾淨 FAIL。
// 用法：node tests/test_r341_c_gate_fix.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
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

/* ---- (1) 靜態：四閘讀 N id、C 閘零殘留 ---- */
ok('靜態 A1：liu_foreshadow 閘讀 N9', html.includes('{ id:"liu_foreshadow", when(st){ const ys=yearSeasonNow(); return ys.year<=1991 && enc79TierOf(st.fav)<=1 && enc83NodeDone("N9"); }'));
ok('靜態 A2：liu_steal 閘讀 N9', html.includes('!(S.wf3 && S.wf3.liaoChoice) && enc83NodeDone("N9")'));
ok('靜態 A3：liu_clash 閘讀 N16', html.includes('{ id:"liu_clash", when(st){ const ys=yearSeasonNow(); return ys.year===1992 && ys.season==="冬" && enc83NodeDone("N16"); }'));
ok('靜態 A4：mak_intel 閘讀 N12', html.includes('{ id:"mak_intel", when(st){ return enc79TierOf(st.fav)>=2 && enc83NodeDone("N12"); }'));
ok('靜態 A5：enc83NodeDone("C…") 全檔零殘留', !/enc83NodeDone\("C\d+"\)/.test(html));
ok('靜態 A6：註解唔再寫 C＝N 對照', !html.includes('C8＝N9') && !html.includes('C13＝N16') && !html.includes('C15＝N12') && !html.includes('N9 已完成（C8）'));
ok('靜態 A7：enc83NodeDone 本身無 C→N 翻譯層（直查 isDone／done_ 旗）', (()=>{ const src = extractFn('enc83NodeDone'); return src.includes('StoryOC.isDone(id)') && src.includes('"done_"+id') && !/C8|C13|C15|C2N/.test(src); })());

/* ---- sandbox：真 enc83NodeDone＋真 beat when ---- */
let S;
let _ys = { year: 1991, season: '秋' };
let _doneNodes = new Set();
function yearSeasonNow(){ return _ys; }
const StoryOC = { isDone: (id)=> _doneNodes.has(id) };
const asVar = (code, name)=> code.replace('const ' + name + ' =', 'var ' + name + ' =');
eval(asVar(extractConst('ENC79_BEATS'), 'ENC79_BEATS')
  + '\n' + extractFn('enc79TierOf')
  + '\n' + extractFn('enc83Flag')
  + '\n' + extractFn('enc83NodeDone'));
function beatOf(sid, id){ return (ENC79_BEATS[sid] || []).find(b => b.id === id); }
function gate(sid, id, fav){ return beatOf(sid, id).when({ fav: fav||0 }); }
function resetGates(year, season){ S = { flags: {}, wf3: {} }; _ys = { year, season }; _doneNodes = new Set(); }

/* ---- (2) 真跑：N 播種開閘、C 播種唔開 ---- */
resetGates(1991, '秋');
ok('真跑 B1：enc83NodeDone 無播種 → false', enc83NodeDone('N9') === false);
_doneNodes.add('N9');
ok('真跑 B2：enc83NodeDone 播種 N9 → true', enc83NodeDone('N9') === true);
ok('真跑 B3：liu_foreshadow N9 完開（1991 T1）', gate('liu_bingxing', 'liu_foreshadow', 10) === true);
ok('真跑 B4：liu_steal N9 完開（1991 秋 T2）', gate('liu_bingxing', 'liu_steal', 30) === true);
resetGates(1991, '秋'); _doneNodes.add('C8');
ok('真跑 B5：liu_foreshadow 淨 C8 唔開（舊死閘已除）', gate('liu_bingxing', 'liu_foreshadow', 10) === false);
ok('真跑 B6：liu_steal 淨 C8 唔開（收割鏈入口跟真實存檔）', gate('liu_bingxing', 'liu_steal', 30) === false);
resetGates(1992, '冬');
ok('真跑 B7：liu_clash 無 N16 唔開', gate('liu_bingxing', 'liu_clash', 30) === false);
_doneNodes.add('N16');
ok('真跑 B8：liu_clash N16 完開（1992 冬）', gate('liu_bingxing', 'liu_clash', 30) === true);
resetGates(1992, '冬'); _doneNodes.add('C13');
ok('真跑 B9：liu_clash 淨 C13 唔開', gate('liu_bingxing', 'liu_clash', 30) === false);
resetGates(1991, '夏');
ok('真跑 B10：mak_intel 無 N12 唔開', gate('mak_zhendong', 'mak_intel', 30) === false);
_doneNodes.add('N12');
ok('真跑 B11：mak_intel N12 完開', gate('mak_zhendong', 'mak_intel', 30) === true);
resetGates(1991, '夏'); _doneNodes.add('C15');
ok('真跑 B12：mak_intel 淨 C15 唔開', gate('mak_zhendong', 'mak_intel', 30) === false);

console.log(fails.length ? ('FAILURES: ' + fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
