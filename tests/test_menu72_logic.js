// v20a72 MENU72 邏輯測試：分組映射新子頁（people→人情組／inv→近況組）＋
// 三個歸位內容產生器（jobs72SectionHtml 拍攝簿三態／people72Html 人脈列／
// inv72Html 庫存兩態）用真函數＋stub 世界行，內容同舊 modal 一致。
// 反證：喺 v20a71 index 上行會 FAIL（冇 jobs72／people72／inv72 函數、
// BOOK70_TAB_GROUP 冇 people／inv）。
// 用法：node tests/test_menu72_logic.js [path-to-index.html]
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
  let depth = 0, started = false;
  for(let k = i; k < html.length; k++){
    const ch = html[k];
    if(ch === '{' || ch === '['){ depth++; started = true; }
    else if(ch === '}' || ch === ']'){ depth--; if(started && depth === 0) return html.slice(i, k + 1) + ';'; }
    else if(ch === ';' && !started) return html.slice(i, k + 1);
  }
  throw new Error('const end not found: ' + name);
}

/* ---- 世界 stub ---- */
var S = null;
var GIGS = [];
eval(extractConst('LOCS').replace('const LOCS =', 'var LOCS ='));
eval(extractConst('NPCS').replace('const NPCS =', 'var NPCS ='));
eval(extractConst('BOOK70_TAB_GROUP').replace('const BOOK70_TAB_GROUP =', 'var BOOK70_TAB_GROUP ='));
eval(extractConst('BOOK70_GROUP_FIRST').replace('const BOOK70_GROUP_FIRST =', 'var BOOK70_GROUP_FIRST ='));
eval(extractConst('book70GroupSub').replace('const book70GroupSub =', 'var book70GroupSub ='));
var PORTRAITS = new Proxy({}, { get: () => 'face.png' });
var affNextUnlock = function(v){ return v < 100 ? { need: 10, label: '閒談', at: 10 } : null; };
var shootSpanFor = function(){ return 3; };
var isRecordGig = function(){ return false; };
var gigCardHtml = function(){ return '<div class="gig-stub"></div>'; };
var rarityLabelZh = function(){ return '稀有'; };
var softSocialCostsDay = function(){ return false; };
var GiftShop = { ensureSave: function(){}, inventoryList: function(){ return []; } };
eval(extractFn('shootRemain'));
eval(extractFn('ensureWrapHistoryFromFlags'));
eval(extractFn('jobs72SectionHtml'));
eval(extractFn('people72Html'));
eval(extractFn('inv72Html'));

/* ---------- (1) 分組映射 ---------- */
ok('映射：people→人情組、inv→近況組', BOOK70_TAB_GROUP.people === 'favor' && BOOK70_TAB_GROUP.inv === 'status');
ok('映射：舊子頁冇走樣（debt→favor、ledger→status、works→career、progress→plan）',
  BOOK70_TAB_GROUP.debt === 'favor' && BOOK70_TAB_GROUP.ledger === 'status'
  && BOOK70_TAB_GROUP.works === 'career' && BOOK70_TAB_GROUP.progress === 'plan');
ok('人情組預設子頁＝人情債（GROUP_FIRST＋groupSub）',
  BOOK70_GROUP_FIRST.favor === 'debt' && book70GroupSub.favor === 'debt');
ok('映射：全部子頁都落入五大類之一',
  Object.values(BOOK70_TAB_GROUP).every(g => ['plan', 'career', 'status', 'news', 'favor'].indexOf(g) >= 0));

/* ---------- (2) 拍攝簿三態 ---------- */
S = { booked: [], shoots: [], wrapHistory: [], flags: {}, weekPlan: [], dayIndex: 0 };
let h = jobs72SectionHtml();
ok('拍攝簿空態：標題＋未有紀錄＋去通告欄掣', h.indexOf('拍攝簿') >= 0 && h.indexOf('未有拍攝中') >= 0
  && h.indexOf('jobs72-goboard') >= 0 && h.indexOf('去通告欄') >= 0);
S = { booked: [], shoots: [{ id: 'sh1', gigId: 'g1', title: '測試戲', type: '電影', locId: LOCS[0].id, doneDays: 1, totalDays: 3, pay: 5000, fame: 10, popularity: 5 }], wrapHistory: [], flags: {}, weekPlan: [], dayIndex: 0 };
h = jobs72SectionHtml();
ok('拍攝簿拍攝中：段名＋戲名＋進度＋剩餘 2 日＋去相關地點掣', h.indexOf('拍攝中／已獲聘') >= 0 && h.indexOf('測試戲') >= 0
  && h.indexOf('進度 1/3') >= 0 && h.indexOf('剩餘 2 日') >= 0 && h.indexOf('jobs72-goloc') >= 0 && h.indexOf('去相關地點') >= 0);
S = { booked: [], shoots: [], wrapHistory: [{ gigId: 'g9', title: '舊戲', type: '電視', totalDays: 2, pay: 3000, fame: 5, rating: '好評如潮' }], flags: {}, weekPlan: [], dayIndex: 0 };
h = jobs72SectionHtml();
ok('拍攝簿履歷：已殺青履歷＋戲名＋評價保留', h.indexOf('已殺青履歷') >= 0 && h.indexOf('舊戲') >= 0 && h.indexOf('好評如潮') >= 0);
GIGS = [{ id: 'gb1', loc: LOCS[0].id, title: '待試鏡戲' }];
S = { booked: [{ gigId: 'gb1', title: '待試鏡戲' }], shoots: [], wrapHistory: [], flags: {}, weekPlan: [], dayIndex: 0 };
h = jobs72SectionHtml();
ok('拍攝簿待試鏡段（gigCardHtml 渲染）', h.indexOf('待試鏡（未獲聘）') >= 0 && h.indexOf('gig-stub') >= 0);
GIGS = [];

/* ---------- (3) 人脈列 ---------- */
S = { npcs: { agent: 40 } };
h = people72Html();
ok('人脈：標題＋門檻說明在位', h.indexOf('人脈') >= 0 && h.indexOf('好感門檻：寒暄0') >= 0);
ok('人脈：何生列（名＋經理人＋好感 40＋去找何生事務所）', h.indexOf('何生') >= 0 && h.indexOf('經理人') >= 0
  && h.indexOf('40／100') >= 0 && h.indexOf('data-loc="agency_ho"') >= 0 && h.indexOf('people-go') >= 0);
ok('人脈：其他 NPC 列齊（林曉晴在列）', h.indexOf('林曉晴') >= 0 && h.indexOf('同期演員') >= 0);
ok('人脈：解鎖提示行保留', h.indexOf('人情：再加 10') >= 0);

/* ---------- (4) 庫存兩態 ---------- */
S = { money: 500 };
GiftShop.inventoryList = function(){ return []; };
h = inv72Html();
ok('庫存空態：存款＋空空文案＋去小賣掣', h.indexOf('庫存') >= 0 && h.indexOf('$500') >= 0
  && h.indexOf('庫存空空') >= 0 && h.indexOf('inv72-goshop') >= 0 && h.indexOf('去香江唱片小賣') >= 0);
S = { money: 1234 };
GiftShop.inventoryList = function(){ return [{ itemId: 'a', count: 2, item: { name: '朱古力', rarity: 'rare', price: 80, emoji: '🍫' } }]; };
h = inv72Html();
ok('庫存有貨：品名＋數量＋稀有度＋價錢＋送禮提示', h.indexOf('朱古力') >= 0 && h.indexOf('×2') >= 0
  && h.indexOf('稀有') >= 0 && h.indexOf('$80') >= 0 && h.indexOf('送禮') >= 0 && h.indexOf('$1,234') >= 0);

console.log(fails.length ? ('FAILURES: ' + fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
