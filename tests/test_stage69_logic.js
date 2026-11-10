// v20a69 STAGE69 邏輯測試：台風訓練（train_stage）報名入口接線——
// 電視台附帶開放（COURSE_ENROLL_EXTRA）／自動開放規則（maybeUnlockMidCourses）／
// 指南鏡像（ux68UnlockRule、ux68CourseLocs、ux68CourseStatus、ux68CourseGoLoc）／
// 通告捷徑唔再借演技課代行（preferredLocForTrainTarget）／全課程可達性掃描。
// 反證：喺 v20a68 index 上行會 FAIL（train_stage 邊度都冇接線、冇 stage 解鎖規則、捷徑別名去 train_acting）。
// 用法：node tests/test_stage69_logic.js [path-to-index.html]
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
var eventLine = function(){ return ''; };
for(const c of ['LOCS','COURSE_DEFS','TRAIN_BY_TYPE','COURSE_ENROLL_EXTRA'])
  eval(extractConst(c).replace('const ' + c + ' =', 'var ' + c + ' ='));
for(const f of ['enrollCourse','maybeUnlockMidCourses','courseForStatKey','preferredLocForTrainTarget'])
  eval(extractFn(f));
eval(extractBlock('/* ===== v20a68 UX68', 'function looksLikeEraId(s){'));

/* ---------- (1) 接線：駐點 ---------- */
ok('接線：COURSE_ENROLL_EXTRA.tv 含 train_stage（電視台附帶開放）',
  (COURSE_ENROLL_EXTRA.tv || []).indexOf('train_stage') >= 0);
const stageTypes = Object.keys(COURSE_ENROLL_EXTRA).filter(t => (COURSE_ENROLL_EXTRA[t] || []).indexOf('train_stage') >= 0);
ok('接線：train_stage 附帶駐點唯一（只 tv，唔遍地開）', stageTypes.length === 1 && stageTypes[0] === 'tv');
const stageMain = Object.keys(TRAIN_BY_TYPE).filter(t => TRAIN_BY_TYPE[t].courseId === 'train_stage');
ok('接線：train_stage 唔係任何主課（主課位冇被搶／冇改既有主課）', stageMain.length === 0);
ok('接線：既有附帶冇被郁（film 仍係 iq＋stamina、tv 仍含 charm）',
  JSON.stringify(COURSE_ENROLL_EXTRA.film) === JSON.stringify(['train_iq','train_stamina'])
  && (COURSE_ENROLL_EXTRA.tv || []).indexOf('train_charm') >= 0);

/* ---------- (2) 指南衍生：地點／狀態／前往 ---------- */
const sl = ux68CourseLocs('train_stage');
ok('指南衍生：台風冇主課地點、附帶＝三間電視台',
  sl.main.length === 0 && sl.extra.length === 3
  && sl.extra.indexOf('tvb_longmen') >= 0 && sl.extra.indexOf('tvb_kowloon') >= 0 && sl.extra.indexOf('tvb_harbour') >= 0);
S = { trainCount:{}, enrolled:{}, dayIndex:0 };
let st = ux68CourseStatus('train_stage');
/* v20a70 BOOK70 改版：狀態改「短徽章＋一句進度」，地點唔再入狀態行（卡面瘦身）——
   「星河電視台」由緊接嘅前往衍生斷言覆蓋；badge／差堂數斷言喺 v69 index 上行會 FAIL（反證）。 */
ok('指南狀態：未開放徽章＋條件＋進度 0／2＋差 2 堂＋附帶途徑（唔再係「暫未有報名入口」）',
  !st.open && st.badge === '未開放' && st.text.indexOf('暫未有報名入口') < 0
  && st.text.indexOf('任何訓練累計 2 堂') >= 0 && st.text.indexOf('0／2') >= 0
  && st.text.indexOf('差 2 堂') >= 0 && st.text.indexOf('附帶開放') >= 0);
ok('指南前往：台風 → 星河電視台（tv 首站）', ux68CourseGoLoc('train_stage', 'stage') === 'tvb_longmen');
S = { trainCount:{}, enrolled:{ train_stage:true }, dayIndex:0 };
st = ux68CourseStatus('train_stage');
ok('指南狀態：已報名 → 已開放＋徽章「已開放」', st.open === true && st.badge === '已開放');

/* ---------- (3) 解鎖規則：真規則同指南鏡像同步 ---------- */
S = { trainCount:{ train_acting:1 }, enrolled:{}, dayIndex:0 };
maybeUnlockMidCourses([]);
ok('解鎖：累計 1 堂未夠 → 台風未開放', !S.enrolled.train_stage);
S = { trainCount:{ train_acting:1, train_vocal:1 }, enrolled:{}, dayIndex:0 };
maybeUnlockMidCourses([]);
ok('解鎖：任何訓練累計 2 堂 → 台風自動開放（同魅力同級）', !!S.enrolled.train_stage && !!S.enrolled.train_charm);
const rule = ux68UnlockRule('train_stage');
ok('鏡像同步：ux68UnlockRule(train_stage)＝任何訓練累計 2 堂、進度即時計',
  !!rule && rule.goal === 2 && rule.have === 2 && rule.need.indexOf('任何訓練累計 2 堂') >= 0);
/* v20a75 改版：進階台風併入台風級別——3 堂唔再開獨立課，級別仍一級；
   上滿 5 堂升二級；顯示鏡像 ux68UnlockRule 刪 mid 個案（回 null）。 */
S = { trainCount:{ train_stage:3 }, enrolled:{ train_stage:true }, dayIndex:0 };
maybeUnlockMidCourses([]);
ok('v75：台風 3 堂唔再開獨立進階課＋級別仍一級', !S.enrolled.train_stage_mid && levels75Level(S, 'train_stage') === 1);
S.trainCount.train_stage = 5;
ok('v75：台風 5 堂 → 升二級（levels75Level 衍生）', levels75Level(S, 'train_stage') === 2);
ok('v75 鏡像同步：ux68UnlockRule(train_stage_mid) 已刪（回 null）', ux68UnlockRule('train_stage_mid') === null);

/* ---------- (4) 通告捷徑：唔再借演技課代行 ---------- */
ok('courseForStatKey：stage → train_stage（不變）', courseForStatKey('stage') === 'train_stage');
const pref = preferredLocForTrainTarget('stage', 'train_stage');
ok('捷徑：台風目標回 train_stage 本人（唔再別名去 train_acting）＋指去電視台',
  pref.courseId === 'train_stage' && pref.locId === 'tvb_longmen' && pref.mode === 'train');
const prefAct = preferredLocForTrainTarget('acting', 'train_acting');
ok('捷徑：演技目標不受影響（仍係 train_acting）', prefAct.courseId === 'train_acting' && prefAct.mode === 'train');

/* ---------- (5) 全課程可達性掃描（防同類缺口再生） ---------- */
S = { trainCount:{}, enrolled:{}, dayIndex:0 };
const unreachable = Object.keys(COURSE_DEFS).filter(cid => {
  const locs = ux68CourseLocs(cid);
  return locs.main.length === 0 && locs.extra.length === 0 && !ux68UnlockRule(cid);
});
ok('全課程可達：9 課全部有路徑（主課／附帶／解鎖規則至少其一）', unreachable.length === 0);

console.log(fails.length ? ('\nFAILURES: ' + fails.length) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
