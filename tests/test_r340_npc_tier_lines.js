// v20a340 NPC_TIER_LINES insider 貼士死引用重寫測試：v20a267 刪走傳聞拼合＋
//   通告卡情報行機制，但 NPC insider 貼士仲有四句指去佢哋（何生 insider 兩句
//   「拼到相關情報」「通告卡嘅情報行」、采兒 insider 兩句「相關碎片，試下拼埋」
//   「通告卡有情報行會提你」）——玩家面會見到一個唔存在嘅系統。今版四句改指
//   現行系統（好感 trigger／打聽／風聲），保留原意同廣東話口吻。
// 用法：node tests/test_r340_npc_tier_lines.js [path-to-index.html]
// 反證：喺 v339 index 上行 → A1–A9＋C4 乾淨 FAIL（舊文案在位），B／C1–C3 照過。
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond, extra){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name + (extra ? ' :: ' + extra : '')); }

/* ---------- 抽出 NPC_TIER_LINES 物件（eval 取值，註解唔入值） ---------- */
const start = html.indexOf('const NPC_TIER_LINES');
const end = html.indexOf('function npcTierPool');
if(start < 0 || end < 0) throw new Error('NPC_TIER_LINES block not found');
const block = html.slice(start, end);
const NPC_TIER_LINES = eval('(' + block.replace('const NPC_TIER_LINES =', '').trim().replace(/;$/, '') + ')');
const allLines = [];
Object.keys(NPC_TIER_LINES).forEach(function(npc){
  ['daily','insider'].forEach(function(tier){
    (NPC_TIER_LINES[npc][tier] || []).forEach(function(l){ allLines.push({ npc: npc, tier: tier, text: l }); });
  });
});
const poolText = allLines.map(function(x){ return x.text; }).join('\n');

/* ---------- A 組：靜態——死引用字串已清、新文案在位 ---------- */
ok('A1 何生 insider 舊句「拼到相關情報」已刪（池內）', poolText.indexOf('拼到相關情報') < 0);
ok('A2 何生 insider 舊句「通告卡嘅情報行」已刪（池內）', poolText.indexOf('通告卡嘅情報行') < 0);
ok('A3 采兒 insider 舊句「相關碎片，試下拼埋」已刪（池內）', poolText.indexOf('相關碎片，試下拼埋') < 0);
ok('A4 采兒 insider 舊句「通告卡有情報行會提你」已刪（池內）', poolText.indexOf('通告卡有情報行會提你') < 0);
ok('A5 何生 insider 新文案在位（陸替工改指好感 trigger）',
  poolText.indexOf('你同佢熟啲、好感夠，通告欄有機會多一張替工通告') >= 0);
ok('A6 何生 insider 新文案在位（麥瞞傷改指打聽）',
  poolText.indexOf('記得去打聽下佢組嘅情況先') >= 0);
ok('A7 采兒 insider 新文案在位（陸夜歸改指打聽／風聲）',
  poolText.indexOf('你去打聽下佢近排嘅風聲') >= 0);
ok('A8 采兒 insider 新文案在位（麥瞞傷改指打聽）',
  poolText.indexOf('接之前記得去打聽下，唔好冇打聽就接') >= 0);
ok('A9 全池死引用字眼掃描（碎片／拼埋／拼到／情報行／情報卡／拼合）零命中',
  ['碎片','拼埋','拼到','情報行','情報卡','拼合'].every(function(w){ return poolText.indexOf(w) < 0; }));

/* ---------- B 組：貼士池結構不變（5 NPC × daily 4 ＋ insider 4 ＝ 40 句） ---------- */
const npcs = Object.keys(NPC_TIER_LINES);
ok('B1 NPC 數目不變（agent／reporter／colleague／rival／director）',
  npcs.length === 5 && ['agent','reporter','colleague','rival','director'].every(function(n){ return npcs.indexOf(n) >= 0; }),
  npcs.join(','));
ok('B2 每 NPC daily 4 句＋insider 4 句，總數 40',
  allLines.length === 40 && npcs.every(function(n){
    return (NPC_TIER_LINES[n].daily || []).length === 4 && (NPC_TIER_LINES[n].insider || []).length === 4;
  }), 'total=' + allLines.length);
ok('B3 每句都係非空字串',
  allLines.every(function(x){ return typeof x.text === 'string' && x.text.length > 0; }));

/* ---------- C 組：npcTierPool 真跑（aff 分層照舊） ---------- */
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
const tiersStart = html.indexOf('const NPC_AFF_TIERS');
var NPC_AFF_TIERS = eval('(' + html.slice(tiersStart, html.indexOf(';', tiersStart)).replace('const NPC_AFF_TIERS =', '') + ')');
eval(extractFn('npcTierPool'));
const none = npcTierPool('agent', 0);
const mid = npcTierPool('agent', 30);
const high = npcTierPool('agent', 100);
ok('C1 npcTierPool 好感 0 兩層都唔出（dailyAt 25／insiderAt 60）', none.daily.length === 0 && none.insider.length === 0,
  'daily=' + none.daily.length + ' insider=' + none.insider.length);
ok('C2 npcTierPool 中好感只出 daily', mid.daily.length === 4 && mid.insider.length === 0,
  'daily=' + mid.daily.length + ' insider=' + mid.insider.length);
ok('C3 npcTierPool 高好感 daily＋insider 齊出', high.daily.length === 4 && high.insider.length === 4,
  'daily=' + high.daily.length + ' insider=' + high.insider.length);
ok('C4 新文案經 npcTierPool 出到（陸替工新句喺 insider 池）',
  high.insider.join('\n').indexOf('你同佢熟啲、好感夠') >= 0);

console.log(fails.length ? ('FAILURES: ' + fails.join(', ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
