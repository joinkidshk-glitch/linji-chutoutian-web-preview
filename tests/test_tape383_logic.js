// v422B resync：index.html 淨 +179 行（53212→53391）；釘行按 difflib 映射重寫，內容逐字核實純漂移；見 qa422/resync422b.py。
// v20a383 TAPE383 自費試鏡帶・邏輯測試
// 合約（用戶 2026-11-22 拍板次序③；方案 GPT-6.2-sol「自費試鏡帶」）：
//   A 開閘：1991 年起（第二、三年）；每季一次（季鍵 year*4+季）；1990 年停用、本季已用停用。
//   B 定價：按季種子 $1,200–1,800（$100 步，flat scale 唔跟通脹），同季同價、讀檔唔重擲。
//   C 選通告：自選媒介類別（五類），由嗰類揀一張未消費、無 trigger、tier 窗 [pt,pt+1] 嘅真通告；
//     同季同類種子定死同一張；唔加新通告（庫 330 不變）。
//   D 保留／到期：買後 state=kept、標籤「自費試鏡」＋截止日；7 日未試鏡→expired；已試鏡→used。
//   E 唔買分：本模組唔改試鏡成功率／判定（chance 唔喺本測試範圍，靜態釘另驗）。
// 反證：v382 index 冇 tape383 函數 → 抽取即 throw → FAIL。
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
function extractFn(name){
  const i = html.indexOf('function ' + name + '(');
  if (i < 0) throw new Error('fn not found: ' + name);
  let depth = 0, j = html.indexOf('{', i);
  for (; j < html.length; j++){ if (html[j] === '{') depth++; else if (html[j] === '}'){ depth--; if (depth === 0) break; } }
  return html.slice(i, j + 1);
}
let fails = 0;
function ok(name, cond, extra){
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : ''));
  if (!cond) fails++;
}

/* ---------- 沙盒 ---------- */
const START = { y: 1990, m: 1, d: 1 };
var S = { dayIndex: 0, money: 10000, flags: {}, booked: [], pendingAud: [], shoots: [], tape383: null, fame: 99, acting: 99, stage: 99, vocal: 99, looks: 99, charm: 99, iq: 99, stamina: 99, wardrobeOwned: [] }; /* v422B：試鏡帶揀通告改查 req，沙盒玩家設為全達標 */
var dateObj = function(){ return new Date(START.y, START.m - 1, START.d + (S.dayIndex | 0)); };
var enc79PlayerTier = function(){ return 1; }; /* 配角 */
var GIG_TIER_ORDER229 = ["臨記","初級","中級","高級","稀有"];
var gigTierCanon229 = function(t){ return t || "初級"; };
var isGigConsumed = function(){ return false; };
var saveQ = function(){};
var isGigWrapped = function(){ return false; };
var isGigInProduction = function(){ return false; };
var gigLifecycleStatus = function(){ return 'open'; };
var STAT_KEYS = ['acting','stage','vocal','looks','charm','iq','stamina'];
var toast = function(){};
var triggerGigLocName229 = function(id){ return String(id || ""); };
const allGigs = JSON.parse(fs.readFileSync(path.join(ROOT, 'content/gigs_new.json'), 'utf8')).gigs;
ok('gig pool 330', allGigs.length === 330, 'n=' + allGigs.length);
var GIGS = allGigs.filter(g => g.year === 1991);
S.wardrobeOwned = Array.from(new Set(allGigs.flatMap(g => (g.wardrobe && g.wardrobe.need) || [])));
eval([
  extractFn('tape383QuarterKey'),
  extractFn('tape383Price'),
  extractFn('tape383Slot'),
  extractFn('tape383State'),
  extractFn('fameFloor'), extractFn('gateTrainHint'), extractFn('costume382Gate'), extractFn('reqGap'), extractFn('canAudition'), extractFn('v422Auditionable'), extractFn('v422PickAuditionable'),
  extractFn('tape383PickGig'),
  extractFn('tape383FmtDay'),
  extractFn('tape383LocName'),
  extractFn('tape383Tick'),
  extractFn('tape383KeptGig'),
  extractFn('tape383Label'),
  extractFn('tape383DeadlineText'),
].join('\n'));

/* A 開閘 */
S.dayIndex = 0; /* 1990-01-01 */
ok('1990 early', tape383State() === 'early', tape383State());
S.dayIndex = 365; /* 1991-01-01 */
ok('1991 ok', tape383State() === 'ok', tape383State());
S.tape383 = { qk: tape383QuarterKey(), gigId: 'x', state: 'kept', keptDay: 365 };
ok('本季已用 used', tape383State() === 'used', tape383State());
S.tape383 = { qk: tape383QuarterKey() - 1, gigId: 'x', state: 'used', keptDay: 300 };
ok('上季用過今季 ok', tape383State() === 'ok', tape383State());
S.tape383 = null;

/* B 定價 */
const prices = new Set();
for (let d = 365; d < 365 + 731; d += 30){ S.dayIndex = d; prices.add(tape383Price()); }
const parr = [...prices].sort((a, b) => a - b);
ok('定價帶 1200–1800', parr.every(p => p >= 1200 && p <= 1800 && p % 100 === 0), JSON.stringify(parr));
S.dayIndex = 365;
ok('同季同價', tape383Price() === tape383Price());
ok('1991Q1 價', tape383Price() === 1500, 'price=' + tape383Price());

/* C 選通告 */
S.dayIndex = 365;
const cats = ["電影","電視劇","唱片通告","廣告","綜藝"];
for (const c of cats){
  const g = tape383PickGig(c);
  ok('揀到 ' + c, !!g && g.type === c && !g.trigger, g ? g.id : 'null');
  if (g){
    const ti = GIG_TIER_ORDER229.indexOf(gigTierCanon229(g.tier));
    ok(c + ' tier 窗 [1,2]', ti >= 1 && ti <= 2, 'tier=' + g.tier);
    ok(c + ' 種子定死', tape383PickGig(c).id === g.id);
  }
}
ok('唔存在類別揀唔到', tape383PickGig('不存在') === null);
S.flags['done_' + tape383PickGig('電影').id] = true;
const gAfter = tape383PickGig('電影');
ok('已完成通告唔再揀', !!gAfter && !S.flags['done_' + gAfter.id], gAfter ? gAfter.id : 'null');
S.flags = {};

/* D 保留／到期 */
const g1 = tape383PickGig('電視劇');
S.tape383 = { qk: tape383QuarterKey(), gigId: g1.id, locId: g1.loc, title: g1.title, type: '電視劇', state: 'kept', keptDay: 365, price: 1500 };
ok('kept 標籤', tape383Label(g1) === '自費試鏡' && tape383KeptGig(g1) === true);
ok('非目標通告無標籤', tape383Label({ id: 'other' }) === '');
ok('截止日文字', tape383DeadlineText(g1) === '1991年1月8日', tape383DeadlineText(g1));
S.dayIndex = 372; /* keptDay+7，未過 */
tape383Tick();
ok('第 7 日未過期', S.tape383.state === 'kept', S.tape383.state);
S.dayIndex = 373; /* keptDay+8 */
tape383Tick();
ok('第 8 日過期', S.tape383.state === 'expired', S.tape383.state);
ok('過期後無標籤', tape383Label(g1) === '');
S.tape383 = { qk: tape383QuarterKey(), gigId: g1.id, state: 'kept', keptDay: 365 };
S.pendingAud = [{ gigId: g1.id }];
S.dayIndex = 380;
tape383Tick();
ok('已試鏡轉 used', S.tape383.state === 'used', S.tape383.state);

/* E 靜態釘：模組唔碰試鏡判定核心字串 */
ok('模組冇改 chance', !/function tape383[\s\S]{0,4000}chance/.test(html.slice(html.indexOf('function tape383QuarterKey'), html.indexOf('function tape383DeadlineText') + 500)));

console.log(fails ? ('TOTAL FAIL ' + fails) : 'TOTAL PASS');
process.exit(fails ? 1 : 0);
