// v20a294 Q7 曉晴 HE 鎖死測試：
// (1) 危機 family_go 開場改寫——買咗機票、走之前試埋呢個角色（最後一個機會），唔再講「返轉頭」，
//     之後試鏡競爭嗰幾段照接；同結局啟德送機一致（危機話要走，結局話行入閘口走咗，唔矛盾）。
// (2) HE 鎖死兩條路：CMT offer（commit48Available）有 hiu_family_go 就唔開；pack ending HE 選擇
//     經 rom159PrepareNode 換成「差一步」變體，只寫 flag_hiu_be（唔寫 flag_hiu_he／flag_hiu_commit）。
// (3) 無旗嗰陣行為唔變：crisis 無旗 → null；ending 無旗唔鎖 → null；CMT 無旗照開。
// 用法：node tests/test_r294_hiu_he_lock.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const rootDir = path.dirname(htmlPath);
let fails = [];
function ok(name, cond) { if (!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }
function extractFn(sig) {
  const s = html.indexOf(sig);
  if (s < 0) return null;
  let i = html.indexOf('{', s), d = 0, inS = null, esc = false, k;
  for (k = i; k < html.length; k++) {
    const c = html[k];
    if (inS) { if (esc) esc = false; else if (c === '\\') esc = true; else if (c === inS) inS = null; continue; }
    if (c === '"' || c === "'" || c === '`') { inS = c; continue; }
    if (c === '{') d++; else if (c === '}') { d--; if (!d) break; }
  }
  return html.slice(s, k + 1);
}
function extractConst(name) {
  const s = html.indexOf('const ' + name);
  if (s < 0) return null;
  const eq = html.indexOf('=', s);
  const semi = html.indexOf(';', eq);
  let i = html.indexOf('{', eq), j = html.indexOf('[', eq);
  if ((i < 0 || i > semi) && (j < 0 || j > semi)) {
    // 純量：const NAME = <value>;
    return 'const ' + name + ' = ' + html.slice(eq + 1, semi + 1);
  }
  if (j >= 0 && (i < 0 || j < i)) i = j;
  const open = html[i], close = open === '{' ? '}' : ']';
  let d = 0, inS = null, esc = false, k;
  for (k = i; k < html.length; k++) {
    const c = html[k];
    if (inS) { if (esc) esc = false; else if (c === '\\') esc = true; else if (c === inS) inS = null; continue; }
    if (c === '"' || c === "'" || c === '`') { inS = c; continue; }
    if (c === open) d++; else if (c === close) { d--; if (!d) break; }
  }
  return 'const ' + name + ' = ' + html.slice(i, k + 1) + ';';
}
function clone(o) { return JSON.parse(JSON.stringify(o)); }

/* ---- (1) 靜態 ---- */
ok('靜態：三處 v294 標記在位（危機／CMT／rom159）', html.includes('v20a294 Q7') && html.includes('CMT_hiu_commit" && choice47StoryFlag("hiu_family_go")') && html.includes('enc87StoryFlag("hiu_family_go")'));
ok('靜態：舊危機對白「返轉頭喇」已無（全文）', !html.includes('返轉頭喇'));
ok('靜態：危機新版「買咗機票喇」＋「最後一個機會」在位', html.includes('買咗機票喇') && html.includes('最後一個機會'));
ok('靜態：HE 變體 label＋BE 旗在位', html.includes('坦白心意：佢已經跟屋企走咗') && html.includes('呢一步就係嗰句話嘅代價'));

/* ---- sandbox：真 pack＋V158 層（跟 test_hiu266_logic.js 做法） ---- */
const packHiu = JSON.parse(fs.readFileSync(path.join(rootDir, 'content', 'story_detail_romance_vera_hiu_choi.json'), 'utf8'));
const T158 = eval(extractConst('ROMANCE_V158_OVERRIDES') + '\nROMANCE_V158_OVERRIDES;');
const wire158 = { romance: { veraHiuChoi: clone(packHiu), lanXu: { nodes: [] } } };
const run158 = new Function('ROMANCE_V158_OVERRIDES', 'STORY_WIRE', 'V158_APPLIED158',
  'const V158A = V158_APPLIED158;\n' + extractFn('function applyRomanceV158Overrides158(').replace('V158_APPLIED158', 'V158A') + '\nreturn applyRomanceV158Overrides158();');
run158(T158, wire158, new WeakSet());
const byId158 = {};
wire158.romance.veraHiuChoi.nodes.forEach(n => { byId158[n.id] = n; });

var S = { dayIndex: 10, money: 10000, flags: {}, story: { rel: {}, flags: {}, done: {} } };
eval(extractFn('function enc87StoryFlag('));
eval(extractFn('function enc158PrepareNode('));
function beatsText(node) { return (node.beats || []).map(b => (b.lines || []).join('')).join(''); }

/* ---- (2) 危機改寫 ---- */
{
  S.story.flags = { hiu_family_go: 1 };
  const src = clone(byId158.R_hiu_crisis);
  const out = enc158PrepareNode(src);
  ok('危機 family_go：開場含「買咗機票」', !!out && out.beats[0].lines[0].indexOf('買咗機票') >= 0);
  ok('危機 family_go：開場唔講「返轉頭」', !!out && out.beats[0].lines.join('').indexOf('返轉頭') < 0);
  ok('危機 family_go：開場唔講「留低嘅理由」', !!out && out.beats[0].lines.join('').indexOf('留低嘅理由') < 0);
  ok('危機 family_go：開場講明係最後一個機會', !!out && out.beats[0].lines.join('').indexOf('最後一個機會') >= 0);
  ok('危機 family_go：之後試鏡競爭嗰幾段照接（公平競爭＋助導叫入去）', !!out && out.beats[1].lines.join('').indexOf('公平競爭') >= 0 && out.beats[4].lines.join('').indexOf('準備入嚟') >= 0);
  ok('危機 family_go：choices 唔郁（同一引用，成全／硬搶照舊）', !!out && out.choices === src.choices && out.choices[0].id === 'C_hiu_crisis_a' && out.choices[1].id === 'C_hiu_crisis_b');
  S.story.flags = {};
  ok('危機無旗 → null（原版照行）', enc158PrepareNode(clone(byId158.R_hiu_crisis)) === null);
}

/* ---- (3) 危機 vs 結局一致（兩段唔可以同時話留低又話走咗） ---- */
{
  S.story.flags = { hiu_family_go: 1 };
  const crisisOut = enc158PrepareNode(clone(byId158.R_hiu_crisis));
  const endingOut = enc158PrepareNode(clone(byId158.R_hiu_ending));
  const crisisTxt = beatsText(crisisOut), endingTxt = beatsText(endingOut);
  ok('一致：危機唔話留低（無「返轉頭」／「留低」）', !/返轉頭|留低/.test(crisisTxt));
  ok('一致：結局話走咗（啟德機場＋行入閘口＋冇再回頭）', endingTxt.indexOf('啟德機場') >= 0 && endingTxt.indexOf('行入閘口') >= 0 && endingTxt.indexOf('冇再回頭') >= 0);
  ok('一致：危機話買咗機票要走，結局話上機前返嚟見一面先走（同一條路）', crisisTxt.indexOf('買咗機票') >= 0 && endingTxt.indexOf('上機之前') >= 0);
  S.story.flags = {};
}

/* ---- (4) pack ending HE 換選擇（rom159PrepareNode） ---- */
const ROM159_WOMEN = { hiu: { name: '林曉晴' }, choi: { name: '周采兒' }, lan: { name: '藍若曦' }, xu: { name: '徐寶珊' }, yip: { name: '葉敏芝' }, so: { name: '蘇芷茵' } };
let lockedWho = null;
function rom159LockedWho() { return lockedWho; }
eval(extractFn('function rom159PrepareNode('));
function mkEndingNode() {
  return {
    id: 'R_hiu_ending',
    beats: clone(byId158.R_hiu_ending.beats),
    choices: [
      { id: 'C_hiu_ending_he', label: '確定關係：同行情侶', effects: { flags: ['flag_hiu_he', 'flag_hiu_commit'], stats: { rel_hiu: 3 }, notes: '兩個人互相成就，事業與感情可以並行。' } },
      { id: 'C_hiu_ending_be', label: '保持距離：漸行漸遠', effects: { flags: ['flag_hiu_be'], stats: { rel_hiu: -2 }, notes: '兩個人漸行漸遠，競爭撕破了關係，只剩下淡淡的交情。' } }
    ]
  };
}
{
  S.story.flags = { hiu_family_go: 1 };
  lockedWho = null;
  const src = mkEndingNode();
  const out = rom159PrepareNode(src);
  ok('ending family_go：HE 選擇換成「差一步」變體（有 copy 返）', !!out && out !== src);
  const he = out && out.choices.find(c => c.id === 'C_hiu_ending_he');
  ok('ending family_go：變體只寫 flag_hiu_be（唔寫 HE／commit）', !!he && JSON.stringify(he.effects.flags) === '["flag_hiu_be"]' && JSON.stringify(he.effects.stats) === '{}');
  ok('ending family_go：變體 label 講明佢跟屋企走咗', !!he && he.label.indexOf('跟屋企走咗') >= 0);
  ok('ending family_go：BE 選擇原封不動', !!out && out.choices.find(c => c.id === 'C_hiu_ending_be').effects.flags[0] === 'flag_hiu_be');
  ok('ending family_go：beats 唔郁（同一引用，啟德送機照播）', !!out && out.beats === src.beats);
  S.story.flags = {};
  lockedWho = null;
  ok('ending 無旗唔鎖 → null（HE 照舊，唔換）', rom159PrepareNode(mkEndingNode()) === null);
  S.story.flags = { hiu_family_go: 1 };
  lockedWho = 'choi';
  const out2 = rom159PrepareNode(mkEndingNode());
  ok('ending family_go＋鎖采兒：family_go 變體行先（唔係鎖另一位嗰句）', !!out2 && out2.choices.find(c => c.id === 'C_hiu_ending_he').label.indexOf('跟屋企走咗') >= 0);
  S.story.flags = {};
  lockedWho = null;
}

/* ---- (5) CMT offer 閘（commit48Available） ---- */
/* const 經 eval 唔漏出 module scope，要用返回值接住（function 宣告先會漏出）。 */
const COMMIT48_REL_MIN = eval(extractConst('COMMIT48_REL_MIN') + '\nCOMMIT48_REL_MIN;');
const COMMIT48_DEFS = eval(extractConst('COMMIT48_DEFS') + '\nCOMMIT48_DEFS;');
const COMMIT48_NODES = eval(extractConst('COMMIT48_NODES') + '\nCOMMIT48_NODES;');
eval(extractFn('function choice47StoryFlag('));
eval(extractFn('function choice47StoryDone('));
eval(extractFn('function commit48Rel('));
function rom159RelKeyWho(relKey) { return ({ rel_hiu: 'hiu', rel_choi: 'choi', rel_lan: 'lan', rel_xu: 'xu', rel_yip: 'yip', rel_so: 'so' })[relKey] || null; }
function choice47SeasonReached() { return true; }
eval(extractFn('function commit48Available('));
{
  // 基準：rel 6、crisis done、1992 秋（stub true）、鎖 hiu——無旗嗰陣 offer 照開
  S.story.flags = {};
  S.story.done = { R_hiu_crisis: 1 };
  S.story.rel = { rel_hiu: 6 };
  lockedWho = 'hiu';
  ok('CMT 無旗：hiu offer 照開（rel 6＋crisis done＋鎖 hiu）', commit48Available('CMT_hiu_commit') === true);
  S.story.flags = { hiu_family_go: 1 };
  ok('CMT family_go：hiu offer 唔開（條件齊晒都鎖死）', commit48Available('CMT_hiu_commit') === false);
  // family_go 只限 hiu：choi offer 唔受影響
  S.story.done = { R_choi_crisis: 1 };
  S.story.rel = { rel_choi: 6 };
  lockedWho = 'choi';
  ok('CMT family_go：choi offer 照開（閘只限曉晴）', commit48Available('CMT_choi_commit') === true);
  S.story.flags = {};
  S.story.done = {};
  S.story.rel = {};
  lockedWho = null;
}

console.log(fails.length ? ('\nFAILURES: ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
