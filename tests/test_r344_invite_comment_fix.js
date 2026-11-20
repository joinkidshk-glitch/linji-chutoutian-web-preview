// v344 請柬註解漏出＋晨鏈繞鏈硬化測試。
// Bug 1：renderAwardInviteHtml 嘅 template literal 入面寫咗一行 JS 註解
// （/* v20a218 C-B1... */），照字面渲染出請柬 modal（drive-192 實駕截圖實證）。
// 修法：註解移出 template literal，改做 JS 註解放喺 return 後、反引號前（同一行，
// 零行號漂移），內容原樣保留。
// Bug 2：startTodayScheduleFromMap／kickScheduleIfNeeded 直接 resolvePlannedDay，
// 繞過 morningChain196——一旦觸發，昨晚典禮＋晨報靜默遲一日（drive-192 harness
// 首跑實測）。修法：跟 runScheduleFromToday 同一寫法，
// morningChain196(()=>resolvePlannedDay(id), {mapMode:false}) 先行全晨鏈。
// 安全依據：mapMode:false 令鏈尾唔再 kick 自己（無遞迴）；各 presenter 冇 pending
// 就回 false（典禮 one-shot 清旗、報紙 pull 嗰刻出隊），重入無害。
// 用法：node tests/test_r344_invite_comment_fix.js
const fs = require('fs');
const path = require('path');
const rootDir = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(rootDir, 'index.html'), 'utf8');

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

/* ---- Bug 1：抽 live 真函數渲染請柬 ---- */
var awards213DateLabel = function(d){ return '9月1日（星期日）'; };
var awards213DateLabelShort = function(d){ return '9月1日'; };
var awardsCeremonyById = function(id){ return id ? { id:id } : null; };
var awards63InviteBitHtml = function(pack){ return ''; };
var awards62GateLineHtml = function(pack){ return ''; };
// AWARDS188_CATEGORIES 唔定義：gallery 分支 typeof 守衛跌返原寫法（同舊測試環境一致）

eval([
  extractFn('function awardsCatsSorted184(pack)'),
  extractFn('function renderAwardInviteHtml(pack)'),
].join('\n'));

ok('harness: renderAwardInviteHtml 載入', typeof renderAwardInviteHtml === 'function');

const nominee = {
  inviteTitle: '維港影藝獎請柬', displayName: '維港影藝獎', season: '秋', year: 1991,
  venue99: '香港文化中心', ceremonyDay213: 608, ceremonyId: 'film_autumn',
  inviteDek: '誠邀出席。', tier: 'nominee', tierLabel: '入圍／提名',
  categories: [{ id:'actor', label:'最佳男主角' }],
};
const outNominee = renderAwardInviteHtml(nominee);
ok('Bug1: nominee 請柬唔含 /* 註解字面', !outNominee.includes('/*'));
ok('Bug1: nominee 請柬唔含 v20a218 註解文字', !outNominee.includes('v20a218'));
ok('Bug1: 「出席即預約」行照常出（k213 分支唔受影響）', outNominee.includes('出席即預約：典禮夜收工之後先播出。'));
ok('Bug1: 典禮夜行照常出', outNominee.includes('典禮夜：9月1日（星期日）'));

const gallery = Object.assign({}, nominee, { tier:'gallery', tierLabel:'旁聽席' });
const outGallery = renderAwardInviteHtml(gallery);
ok('Bug1: gallery 請柬唔含 /* 註解字面', !outGallery.includes('/*'));

const outEmpty = renderAwardInviteHtml({});
ok('Bug1: 空 pack 請柬唔含 /* 註解字面', !outEmpty.includes('/*'));
ok('Bug1: 空 pack 標題跌返預設', outEmpty.includes('頒獎夜請柬'));

const synth = Object.assign({}, nominee, { ceremonyId: null });
const outSynth = renderAwardInviteHtml(synth);
ok('Bug1: 合成 pack（冇 ceremonyId）唔出預約行', !outSynth.includes('出席即預約'));
ok('Bug1: 合成 pack 唔含 /* 註解字面', !outSynth.includes('/*'));

// 註解內容保留（移出做 JS 註解，唔係刪走）
ok('Bug1: v20a218 C-B1 註解文字仲喺 index.html（JS 註解）',
   html.includes('/* v20a218 C-B1：請柬要講明「預約」'));
// 註解唔再喺 template literal 入面：renderAwardInviteHtml 函數體入面，return 之後嘅
// template 區（第一個反引號之後）唔應該有 /* 字面
(function(){
  const src = extractFn('function renderAwardInviteHtml(pack)');
  const retIdx = src.indexOf('return');
  const tickIdx = src.indexOf('`', retIdx);
  const tpl = src.slice(tickIdx);
  ok('Bug1: template literal 區內無 /* 字面', !tpl.includes('/*'));
})();

/* ---- Bug 2：抽兩函數真跑，證先行晨鏈、唔直接 resolve ---- */
var _planId = 'shoot:abc';
var _isMap = false;
var _forced = true;
var calls = { chain: [], resolve: [], map: 0, toast: [] };
var todayPlanId = function(){ return _planId; };
var isMapDay = function(id){ return _isMap; };
var goToMapForBrowse = function(){ calls.map++; };
var todayIsForcedDay = function(){ return _forced; };
var toast = function(m){ calls.toast.push(m); };
var morningChain196 = function(finalFn, opts){ calls.chain.push({ finalFn: finalFn, opts: opts }); };
var resolvePlannedDay = function(id){ calls.resolve.push(id); };

eval([
  extractFn('function startTodayScheduleFromMap()'),
  extractFn('function kickScheduleIfNeeded()'),
].join('\n'));

function resetCalls(){ calls = { chain: [], resolve: [], map: 0, toast: [] }; }

// startTodayScheduleFromMap：排程日 → 先晨鏈，resolve 要等 finalFn
resetCalls(); _planId = 'shoot:abc'; _isMap = false;
startTodayScheduleFromMap();
ok('Bug2: startTodayScheduleFromMap 行 morningChain196 一次', calls.chain.length === 1);
ok('Bug2: startTodayScheduleFromMap 唔直接 resolvePlannedDay（等鏈尾）', calls.resolve.length === 0);
ok('Bug2: startTodayScheduleFromMap 用 mapMode:false（鏈尾唔再 kick）',
   calls.chain.length === 1 && calls.chain[0].opts && calls.chain[0].opts.mapMode === false);
if(calls.chain.length === 1) calls.chain[0].finalFn();
ok('Bug2: 鏈尾 finalFn 先 resolvePlannedDay(當日 id)',
   calls.resolve.length === 1 && calls.resolve[0] === 'shoot:abc');

// startTodayScheduleFromMap：地圖日 → 照舊返地圖，唔行鏈
resetCalls(); _isMap = true;
startTodayScheduleFromMap();
ok('Bug2: 地圖日照舊 goToMapForBrowse、唔行鏈', calls.map === 1 && calls.chain.length === 0 && calls.resolve.length === 0);
_isMap = false;

// startTodayScheduleFromMap：wrap 日 → 照舊返地圖
resetCalls(); _planId = 'wrap:xyz';
startTodayScheduleFromMap();
ok('Bug2: wrap 日照舊 goToMapForBrowse、唔行鏈', calls.map === 1 && calls.chain.length === 0);
_planId = 'shoot:abc';

// kickScheduleIfNeeded：強制日 → 先晨鏈、回 true、resolve 等鏈尾
resetCalls(); _forced = true;
const kicked = kickScheduleIfNeeded();
ok('Bug2: kickScheduleIfNeeded 強制日回 true（接管流程）', kicked === true);
ok('Bug2: kickScheduleIfNeeded 行 morningChain196 一次', calls.chain.length === 1);
ok('Bug2: kickScheduleIfNeeded 唔直接 resolvePlannedDay（等鏈尾）', calls.resolve.length === 0);
ok('Bug2: kickScheduleIfNeeded 用 mapMode:false（無遞迴）',
   calls.chain.length === 1 && calls.chain[0].opts && calls.chain[0].opts.mapMode === false);
ok('Bug2: kickScheduleIfNeeded toast 照出', calls.toast.length === 1);
if(calls.chain.length === 1) calls.chain[0].finalFn();
ok('Bug2: kick 鏈尾 finalFn 先 resolvePlannedDay(當日 id)',
   calls.resolve.length === 1 && calls.resolve[0] === 'shoot:abc');

// kickScheduleIfNeeded：非強制日 → 回 false，乜都唔行
resetCalls(); _forced = false;
const notKicked = kickScheduleIfNeeded();
ok('Bug2: kickScheduleIfNeeded 非強制日回 false、唔行鏈唔 resolve',
   notKicked === false && calls.chain.length === 0 && calls.resolve.length === 0);

// 靜態兜底：兩函數體入面唔再有裸 resolvePlannedDay(id); 直呼（只准喺 finalFn 入面）
(function(){
  const s1 = extractFn('function startTodayScheduleFromMap()');
  const s2 = extractFn('function kickScheduleIfNeeded()');
  const bare = /(^|\n)\s*resolvePlannedDay\(id\);/;
  ok('Bug2: startTodayScheduleFromMap 無裸 resolvePlannedDay 直呼', !bare.test(s1));
  ok('Bug2: kickScheduleIfNeeded 無裸 resolvePlannedDay 直呼', !bare.test(s2));
  ok('Bug2: 兩函數都包 morningChain196', s1.includes('morningChain196(') && s2.includes('morningChain196('));
})();

console.log(`\nTOTAL: ${pass} PASS / ${fail} FAIL`);
if(fail > 0){ console.log('R344 FAIL'); process.exit(1); }
console.log('R344 ALL PASS');
