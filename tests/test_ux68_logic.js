// v20a68 UX68 邏輯測試：訓練指南衍生（增益解析／地點／開放狀態）＋地點選項分類＋要事訊號＋季尾日數。
// 反證：喺 v20a67 index 上行會 FAIL（冇 UX68 block、冇 guide 頁）。
// 用法：node tests/test_ux68_logic.js [path-to-index.html]
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
function extractBlock(marker, endMarker){
  const a = html.indexOf(marker);
  const b = html.indexOf(endMarker);
  if(a < 0 || b < 0 || b <= a) throw new Error('block not found: ' + marker);
  return html.slice(a, b);
}

/* ---- 世界 stub ---- */
var window = {};
var location = { search: '' };
var _ls = {};
var localStorage = { getItem: k => (k in _ls ? _ls[k] : null), setItem: (k,v)=>{ _ls[k]=String(v); }, removeItem: k=>{ delete _ls[k]; } };
var document = { getElementById: () => null, querySelectorAll: () => [], createElement: () => ({}) };
var S = null;
var softPreviewOn = function(){ return true; };
var START = null;
eval(extractConst('START').replace('const START =', 'var START =')); START = START || null;
/* START 係 const 物件：extractConst 回傳 const 宣告，改 var 後直接攞 */
try{ eval('START = (typeof START!=="undefined") ? START : null;'); }catch(_e){}
for(const c of ['STAT_LABEL','LOCS','COURSE_DEFS','TRAIN_BY_TYPE','COURSE_ENROLL_EXTRA','STORY_LOC_SOFT','CALIB60_NODE_WINDOWS','CALIB60_NODE_TITLES'])
  eval(extractConst(c).replace('const ' + c + ' =', 'var ' + c + ' ='));
for(const f of ['applyTrainLesson','calib60SeasonIdx','calib60NowSeasonIdx','calib60NodeTitle'])
  eval(extractFn(f));
/* prefs 真函數（指南／organizer 衍生要行真 loadPrefs/savePrefs/setPref） */
for(const c of ['PREFS_KEY']) eval(extractConst(c).replace('const ' + c + ' =', 'var ' + c + ' ='));
for(const f of ['defaultPrefs','loadPrefs','savePrefs','setPref']) eval(extractFn(f));
var applyPrefsChrome = function(){};
/* calendarSeason stub：跟遊戲月份分季 */
var calendarSeason = function(){
  const dt = new Date(START.y, START.m - 1, START.d + (Number(S && S.dayIndex) || 0));
  const m = dt.getMonth() + 1;
  return (m >= 3 && m <= 5) ? '春' : (m >= 6 && m <= 8) ? '夏' : (m >= 9 && m <= 11) ? '秋' : '冬';
};
var preferredLocForTrainTarget = function(stat, cid){
  if(stat === 'stress' || cid === 'rest') return { locId:'tvb_longmen', courseId:'rest', mode:'rest' };
  return { locId:'tvb_longmen', courseId: cid || 'train_acting', mode:'train' };
};
var _favorDebt = null;
var favorDueDebt = function(){ return _favorDebt; };
var GIGS = [];
eval(extractBlock('/* ===== v20a68 UX68', 'function looksLikeEraId(s){'));

/* ---------- (1) 增益表解析（由 applyTrainLesson 源碼衍生） ---------- */
const gains = ux68ParseGainTable();
/* v20a75 改版：增益改由 TRAIN75_SPEC 按現級衍生；演技一級附帶台風 +1 由一級起
   （跟用戶三級表「附帶跟級 +1/+2/+3」），期望值加 stage:[1,1]。 */
ok('增益解析：train_acting = 演技+4~6／附帶台風+1／壓力+8~12（v75 一級）',
  JSON.stringify(gains.train_acting) === JSON.stringify({ acting:[4,6], stage:[1,1], stress:[8,12] }));
ok('增益解析：train_iq 附帶演技+1', gains.train_iq && gains.train_iq.iq[0] === 3 && gains.train_iq.iq[1] === 5
  && gains.train_iq.acting[0] === 1 && gains.train_iq.acting[1] === 1 && gains.train_iq.stress[0] === 4);
/* v20a75 改版：進階演技已併入演技級別，唔再係獨立課——增益表冇 mid 鍵；
   改驗上滿 5 堂後 train_acting 增益轉二級數（同舊進階課數值一致）。 */
ok('v75：增益表冇進階課鍵（已併入級別）', !('train_acting_mid' in gains) && !('train_stage_mid' in gains));
S = { trainCount:{ train_acting:5 }, enrolled:{ train_acting:true }, dayIndex:0 };
const gains75Lv2 = ux68ParseGainTable();
ok('v75：演技 5 堂後增益轉二級 = 演技+6~8／台風+2／壓力+10~14',
  gains75Lv2.train_acting.acting[0] === 6 && gains75Lv2.train_acting.acting[1] === 8
  && gains75Lv2.train_acting.stage[0] === 2 && gains75Lv2.train_acting.stress[0] === 10 && gains75Lv2.train_acting.stress[1] === 14);
ok('增益解析：train_stage 有台風增益（解析層面）', gains.train_stage && gains.train_stage.stage[0] === 4);
ok('增益解析：train_looks = 外貌+3~5／魅力+1／學費 $800／壓力+6~9（同行串連分支）',
  !!gains.train_looks && gains.train_looks.looks[0] === 3 && gains.train_looks.looks[1] === 5
  && gains.train_looks.charm[0] === 1 && gains.train_looks.money[0] === -800
  && gains.train_looks.stress[0] === 6 && gains.train_looks.stress[1] === 9);

/* ---------- (2) 課程地點衍生 ---------- */
const vocalLocs = ux68CourseLocs('train_vocal');
ok('地點衍生：歌藝主課喺唱片地點（rec_hk）', vocalLocs.main.indexOf('rec_hk') >= 0 && vocalLocs.main.length === 3);
const actingLocs = ux68CourseLocs('train_acting');
ok('地點衍生：演技主課橫跨 tv＋film 地點', actingLocs.main.indexOf('tvb_longmen') >= 0 && actingLocs.main.indexOf('film_lion') >= 0);
const charmLocs = ux68CourseLocs('train_charm');
ok('地點衍生：魅力冇主課、附帶喺 tv/music/ad', charmLocs.main.length === 0 && charmLocs.extra.indexOf('tvb_longmen') >= 0);
const stamLocs = ux68CourseLocs('train_stamina');
ok('地點衍生：武師班附帶喺 film 地點', stamLocs.main.length === 0 && stamLocs.extra.indexOf('film_lion') >= 0);

/* ---------- (3) 開放狀態 ---------- */
S = { trainCount:{}, enrolled:{}, dayIndex:0 };
let st = ux68CourseStatus('train_vocal');
/* v20a70 BOOK70 改版：狀態改「短徽章＋一句進度」，地點唔再入狀態行（卡面瘦身——
   改由卡面「前往」掣交代）；「指去唱片地點」改驗前往衍生 ux68CourseGoLoc。
   喺 v69 index 上行會 FAIL（舊狀態冇 badge 欄，係反證）。 */
ok('狀態：未報名歌藝 → 徽章「未報名」＋無進度行＋前往衍生去唱片地點',
  !st.open && st.badge === '未報名' && st.detail === '' && ux68LocName(ux68CourseGoLoc('train_vocal', 'vocal')) === '香江唱片');
S.enrolled = { train_vocal:true };
st = ux68CourseStatus('train_vocal');
ok('狀態：已報名 → 已開放＋徽章「已開放」', st.open === true && st.badge === '已開放');
/* v20a75 改版：進階演技個案已廢（併入級別）；未開放狀態改用智商課驗證
   （開課門檻任何訓練累計 4 堂，v75 維持不變）。 */
S = { trainCount:{ train_acting:1 }, enrolled:{}, dayIndex:0 };
st = ux68CourseStatus('train_iq');
ok('狀態：智商未夠堂 → 徽章未開放＋條件＋進度 1／4＋差 3 堂（v75）', !st.open && st.badge === '未開放'
  && st.text.indexOf('任何訓練累計 4 堂') >= 0 && st.text.indexOf('1／4') >= 0 && st.detail.indexOf('差 3 堂') >= 0);
S = { trainCount:{ train_vocal:2 }, enrolled:{}, dayIndex:0 };
st = ux68CourseStatus('train_charm');
ok('狀態：魅力課——徽章未開放＋任何訓練 2 堂進度＋附帶途徑', !st.open && st.badge === '未開放' && st.text.indexOf('2／2') >= 0 && st.text.indexOf('附帶開放') >= 0);
st = ux68CourseStatus('train_stage');
/* v20a69 STAGE69 改版：台風訓練已補返接線（電視台附帶＋累計 2 堂自動開放）——
   本斷言由「老實標暫未有報名入口」改為新正確行為；喺 v68 index 上行會 FAIL（反證）。 */
/* v20a70 BOOK70 再改版：狀態行唔再列地點名（卡面瘦身），「星河電視台」改驗前往衍生；
   badge 斷言喺 v69 index 上行會 FAIL（反證）。 */
ok('狀態：台風訓練（v69 已接線）→ 徽章未開放＋條件進度＋附帶途徑，唔再標冇入口；前往衍生去星河電視台',
  !st.open && st.badge === '未開放' && st.text.indexOf('暫未有報名入口') < 0 && st.text.indexOf('任何訓練累計 2 堂') >= 0
  && st.text.indexOf('附帶開放') >= 0 && ux68CourseGoLoc('train_stage', 'stage') === 'tvb_longmen');

/* ---------- (4) v20a74：主攻目標（目標數值）成個移除（用戶 2026-11-10 16:06 拍板） ----------
   （v68–v73 舊斷言「目標數值 prefs 往返」隨功能移除改版；喺 v73 index 上行會 FAIL，係反證。） */
ok('v74：目標讀寫函數已不存在', typeof ux68TargetStat === 'undefined' && typeof ux68SetTargetStat === 'undefined');
ok('v74：目標標示函數已不存在', typeof ux68ApplyTargetBadges === 'undefined');

/* ---------- (5) 選項分類覆蓋 ---------- */
function fakeBtn(cls, n, c, disabled){
  /* 跟真 add() 模板：標題喺 .n、費用喺 .cost（唔係 .c——v68 實駕捉到嘅坑） */
  return { className: cls, disabled: !!disabled, textContent: n,
    querySelector: sel => sel === '.n' ? { textContent: n } : (sel === '.cost' ? { textContent: c } : null) };
}
ok('分類：報名掣 → 訓練', ux68ClassifyAct(fakeBtn('act act-priority', '報名：練歌／錄音室', '+1日')).group === 'train');
ok('分類：進行…訓練 → 訓練', ux68ClassifyAct(fakeBtn('act act-priority', '進行歌藝訓練', '+1日')).group === 'train');
ok('分類：播劇情 → 社交・劇情', ux68ClassifyAct(fakeBtn('act act-priority act-story', '播劇情：暴雨救場', '免費')).group === 'story');
ok('分類：打聽（act-ask） → 社交・劇情', ux68ClassifyAct(fakeBtn('act act-ask', '去茶水間打聽', '免費')).group === 'story');
ok('分類：傾談 → 社交・劇情', ux68ClassifyAct(fakeBtn('act act-priority', '同何生傾談', '免費')).group === 'story');
ok('分類：送禮未開放 → 社交・劇情＋locked', (()=>{ const r = ux68ClassifyAct(fakeBtn('act', '送禮：何生', '未開放')); return r.group === 'story' && r.locked; })());
ok('分類：只查看通告欄 → 接工', ux68ClassifyAct(fakeBtn('act act-priority', '只查看通告欄', '免費')).group === 'work');
ok('分類：試鏡入口 → 接工', ux68ClassifyAct(fakeBtn('act act-priority act-bridge', '試鏡入口：某片', '不耗日')).group === 'work');
ok('分類：接通告 → 接工', ux68ClassifyAct(fakeBtn('act', '接通告：某片', '+1日')).group === 'work');
ok('分類：查看檔期 → 接工', ux68ClassifyAct(fakeBtn('act', '查看檔期：某片', '—')).group === 'work');
ok('分類：暫未能報＋未開放 → 接工＋locked', (()=>{ const r = ux68ClassifyAct(fakeBtn('act', '暫未能報：某片', '未開放')); return r.group === 'work' && r.locked; })());
ok('分類：休息室 → 休息・雜項', ux68ClassifyAct(fakeBtn('act act-priority', '休息室歇陣', '+1日')).group === 'rest');
ok('分類：小賣 → 休息・雜項', ux68ClassifyAct(fakeBtn('act act-priority', '小賣／禮品', '免費')).group === 'rest');
ok('分類：已完成劇情（disabled） → locked', ux68ClassifyAct(fakeBtn('act act-story act-story-done', '劇情已完成', '', true)).locked === true);
ok('分類：未知掣 → 兜底休息・雜項（唔漏項）', ux68ClassifyAct(fakeBtn('act', '神秘選項', '免費')).group === 'rest');

/* ---------- (6) 季尾日數 ---------- */
S = { dayIndex: 144, trainCount:{}, enrolled:{} }; /* 1990-01-01 + 144 日 = 5 月 25 日（春） */
let se = ux68SeasonEndLeft();
ok('季尾：1990 春尾剩 6 日', se.season === '春' && se.left === 6);
S = { dayIndex: 30, trainCount:{}, enrolled:{} }; /* 1 月 31 日（冬） */
se = ux68SeasonEndLeft();
ok('季尾：1990 冬（1 月）剩 28 日', se.season === '冬' && se.left === 28);

/* ---------- (7) 要事訊號 ---------- */
S = { dayIndex: 100, trainCount:{}, enrolled:{}, favorDueSettled:{}, shoots:[], board:{}, story:{ done:{} }, calib60Missed:{} };
_favorDebt = { id:'debt_ho_tutorial', dueDay: 102, favorState:'pending' };
let urg = ux68LocUrgent(LOCS.find(l=>l.id === 'agency_ho'));
ok('要事：人情仲有 2 日到期 → repay matcher', urg.matchers.some(m=>m.key === 'repay' && m.reason.indexOf('2 日') >= 0));
urg = ux68LocUrgent(LOCS.find(l=>l.id === 'cafe_cha'));
ok('要事：人情訊號唔會喺第二度地點出', !urg.matchers.some(m=>m.key === 'repay'));
S.shoots = [{ locId:'film_lion', title:'測試片', deadlineDay: 101 }];
urg = ux68LocUrgent(LOCS.find(l=>l.id === 'film_lion'));
ok('要事：拍攝限期仲有 1 日 → shoot matcher', urg.matchers.some(m=>m.key === 'shoot:測試片' && m.reason.indexOf('1 日') >= 0));
ok('要事比對：shoot matcher 認得「查看檔期：」掣',
  ux68MatchBtn({ title:'查看檔期：測試片' }, 'shoot:測試片') === true);
ok('要事比對：gig matcher 認得「接通告：」掣',
  ux68MatchBtn({ title:'接通告：某通告' }, 'gig:某通告') === true);
/* 節點時窗尾：C7（1991 夏，loc film_harbour）喺 1991 夏任何一日 → nowIdx == endIdx */
S = { dayIndex: 365 + 181, trainCount:{}, enrolled:{}, favorDueSettled:{}, shoots:[], board:{}, story:{ done:{} }, calib60Missed:{} }; /* 1991-07-01 夏 */
_favorDebt = null;
urg = ux68LocUrgent(LOCS.find(l=>l.id === 'film_harbour'));
ok('要事：C7 時窗尾喺 film_harbour 出提示', urg.notes.some(n=>n.indexOf('時窗去到今季尾') >= 0));
urg = ux68LocUrgent(LOCS.find(l=>l.id === 'cafe_cha'));
ok('要事：C7 提示唔會喺 cafe_cha 出', !urg.notes.some(n=>n.indexOf('時窗') >= 0));

console.log(fails.length ? ('FAILURES: ' + fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
