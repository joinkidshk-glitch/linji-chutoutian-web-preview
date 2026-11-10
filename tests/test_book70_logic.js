// v20a70 BOOK70 邏輯測試：主次分家衍生（ux68CoursePrimaryStat／book70SplitForStat）＋
// 狀態新契約（短徽章 badge／一句進度 detail／狀態行唔含地點名）。
// 反證：喺 v20a69 index 上行會 FAIL（冇 book70SplitForStat、狀態冇 badge 欄）。
// 用法：node tests/test_book70_logic.js [path-to-index.html]
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

/* ---- 世界 stub（同 test_ux68_logic 同一套） ---- */
var window = {};
var location = { search: '' };
var _ls = {};
var localStorage = { getItem: k => (k in _ls ? _ls[k] : null), setItem: (k,v)=>{ _ls[k]=String(v); }, removeItem: k=>{ delete _ls[k]; } };
var document = { getElementById: () => null, querySelectorAll: () => [], createElement: () => ({}) };
var S = null;
var softPreviewOn = function(){ return true; };
eval(extractConst('START').replace('const START =', 'var START ='));
for(const c of ['STAT_LABEL','LOCS','COURSE_DEFS','TRAIN_BY_TYPE','COURSE_ENROLL_EXTRA'])
  eval(extractConst(c).replace('const ' + c + ' =', 'var ' + c + ' ='));
eval(extractFn('applyTrainLesson'));
for(const c of ['PREFS_KEY']) eval(extractConst(c).replace('const ' + c + ' =', 'var ' + c + ' ='));
for(const f of ['defaultPrefs','loadPrefs','savePrefs','setPref']) eval(extractFn(f));
var applyPrefsChrome = function(){};
var preferredLocForTrainTarget = function(stat, cid){
  if(stat === 'stress' || cid === 'rest') return { locId:'tvb_longmen', courseId:'rest', mode:'rest' };
  return { locId:'tvb_longmen', courseId: cid || 'train_acting', mode:'train' };
};
var favorDueDebt = function(){ return null; };
var GIGS = [];
eval(extractBlock('/* ===== v20a68 UX68', 'function looksLikeEraId(s){'));

/* ---------- (1) 主修判定（增益表 argmax 衍生，撇除壓力／學費） ---------- */
/* v20a75 改版：進階課併入母課級別，主修判定只剩 7 基礎課。 */
ok('主修判定：演技＝train_acting（v75 進階已併入級別）', ux68CoursePrimaryStat('train_acting') === 'acting');
ok('主修判定：台風＝train_stage（唔畀附帶魅力搶主修）',
  ux68CoursePrimaryStat('train_stage') === 'stage');
ok('主修判定：歌藝／外貌／魅力／智商／體能',
  ux68CoursePrimaryStat('train_vocal') === 'vocal' && ux68CoursePrimaryStat('train_looks') === 'looks'
  && ux68CoursePrimaryStat('train_charm') === 'charm' && ux68CoursePrimaryStat('train_iq') === 'iq'
  && ux68CoursePrimaryStat('train_stamina') === 'stamina');
ok('主修判定：7 課全部有主修數值（v75）', Object.keys(COURSE_DEFS).length === 7 && Object.keys(COURSE_DEFS).every(cid => !!ux68CoursePrimaryStat(cid)));

/* ---------- (2) 主次分家（每頁主修大卡／附帶細行） ---------- */
let sp = book70SplitForStat('acting');
ok('分家：演技頁主修＝[演技訓練]、附帶＝[智商・修養]（v75 一級現況）',
  JSON.stringify(sp.prim) === JSON.stringify(['train_acting']) && JSON.stringify(sp.sec) === JSON.stringify(['train_iq']));
sp = book70SplitForStat('stage');
ok('分家：台風頁主修＝[台風訓練]、附帶＝[演技訓練]（台風 +1 細行，v75）',
  JSON.stringify(sp.prim) === JSON.stringify(['train_stage']) && JSON.stringify(sp.sec) === JSON.stringify(['train_acting']));
sp = book70SplitForStat('charm');
ok('分家：魅力頁主修＝[魅力訓練]、附帶＝[外貌・形象（+1)， 台風訓練（+1)]（v75 一級同值按課 id 序）',
  JSON.stringify(sp.prim) === JSON.stringify(['train_charm']) && JSON.stringify(sp.sec) === JSON.stringify(['train_looks','train_stage']));
sp = book70SplitForStat('iq');
ok('分家：智商頁主修＝[智商・修養]、冇附帶', JSON.stringify(sp.prim) === JSON.stringify(['train_iq']) && sp.sec.length === 0);
sp = book70SplitForStat('vocal');
ok('分家：歌藝頁主修＝[歌藝訓練]、冇附帶', JSON.stringify(sp.prim) === JSON.stringify(['train_vocal']) && sp.sec.length === 0);
sp = book70SplitForStat('stamina');
ok('分家：體能頁主修＝[武師班]、冇附帶', JSON.stringify(sp.prim) === JSON.stringify(['train_stamina']) && sp.sec.length === 0);
sp = book70SplitForStat('looks');
ok('分家：外貌頁主修＝[外貌・形象]、冇附帶', JSON.stringify(sp.prim) === JSON.stringify(['train_looks']) && sp.sec.length === 0);
ok('分家：主修同附帶唔重疊、合併＝全部有呢個數值增益嘅課',
  ['acting','stage','vocal','looks','charm','iq','stamina'].every(k=>{
    const s = book70SplitForStat(k);
    return s.prim.every(c => s.sec.indexOf(c) < 0);
  }));

/* ---------- (3) 狀態新契約：短徽章＋一句進度、狀態行零地點名 ---------- */
S = { trainCount:{}, enrolled:{}, dayIndex:0 };
let st = ux68CourseStatus('train_acting');
ok('狀態契約：主課未報名 → badge=未報名、detail 空、text 就係徽章', st.badge === '未報名' && st.detail === '' && st.text === '未報名' && !st.open);
/* v20a75 改版：進階演技個案已廢；未開放一句 detail 改用智商課（門檻 4 堂）。 */
st = ux68CourseStatus('train_iq');
ok('狀態契約：智商 → badge=未開放、detail 一句（條件＋進度＋差 4 堂）（v75）',
  st.badge === '未開放' && st.detail.indexOf('任何訓練累計 4 堂（0／4）') >= 0 && st.detail.indexOf('差 4 堂') >= 0);
st = ux68CourseStatus('train_stage');
ok('狀態契約：台風（v69 接線）→ badge=未開放、detail 含累計 2 堂＋差 2 堂＋附帶途徑',
  st.badge === '未開放' && st.detail.indexOf('任何訓練累計 2 堂（0／2）') >= 0 && st.detail.indexOf('差 2 堂') >= 0 && st.detail.indexOf('附帶開放') >= 0);
S = { trainCount:{}, enrolled:{ train_stage:true }, dayIndex:0 };
st = ux68CourseStatus('train_stage');
ok('狀態契約：已報名 → open＋badge=已開放', st.open === true && st.badge === '已開放');
/* v20a75 改版：已達標個案改用魅力課（任何訓練 2 堂達標、未報名）。 */
S = { trainCount:{ train_vocal:2 }, enrolled:{}, dayIndex:0 };
st = ux68CourseStatus('train_charm');
ok('狀態契約：已達標未報名 → detail 標「已達標」唔再寫差堂數（v75 魅力個案）',
  st.badge === '未開放' && st.detail.indexOf('已達標') >= 0 && st.detail.indexOf('差') < 0);
/* 用戶診斷核心：地點名唔准喺狀態行出現（舊版「未報名——去 A／B／C…」就係咁嚟） */
S = { trainCount:{}, enrolled:{}, dayIndex:0 };
const locNames = LOCS.map(l => l.name);
const dirty = Object.keys(COURSE_DEFS).filter(cid => locNames.some(n => ux68CourseStatus(cid).text.indexOf(n) >= 0));
ok('狀態契約：全部 7 課狀態文字零地點名（v75；地點改由前往掣交代）', dirty.length === 0);

console.log(fails.length ? ('FAILURES: ' + fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
