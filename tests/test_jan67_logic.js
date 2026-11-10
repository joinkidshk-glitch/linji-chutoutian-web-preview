// v20a67 JAN67 邏輯測試：1 月開局 epoch／評核新週位／softC10 年內週／開局文字對位／舊檔 +65 日遷移。
// 反證：喺 v20a66 index 上行會 FAIL（START 仍 3 月、冇 JAN67 block、邊界週仍 43/95）。
// 用法：node tests/test_jan67_logic.js [path-to-index.html]
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

/* ---- 世界 stub（跟 years66 測試同一套路） ---- */
var window = {};
var location = { search: '' };
var localStorage = { getItem: () => null, setItem: () => {}, removeItem: () => {} };
var S = null;
var refreshMoneyHud = function(){};
var softPreviewOn = function(){ return false; };
eval(extractConst('START').replace('const START =', 'var START ='));
eval(extractBlock('/* ===== v20a66 YEARS66', 'async function refreshCopyPacksFromDisk(){'));
eval(extractBlock('/* ===== v20a67 JAN67', 'async function refreshCopyPacksFromDisk(){'));
for(const c of ['STAT_LABEL','STAT_MAX','STRESS_MAX','LOCS','COURSE_DEFS']) eval(extractConst(c).replace('const ' + c + ' =', 'var ' + c + ' ='));
for(const c of ['CALIB60_FAME_BANDS','CALIB60_ATTR_BANDS','CALIB60_SCALED_KEYS','CALIB60_NODE_WINDOWS','CALIB60_NODE_TITLES','CONSEQ61_REVIEWS']) eval(extractConst(c).replace('const ' + c + ' =', 'var ' + c + ' ='));
const FNS = ['R','clamp','statHardMax','dualTrackNumbers','syncDualTracks','apply',
  'calib60BandScale','calib60ScaleFor','calib60BankedGain','calib60FameGain','calib60ScaleDelta','applyCalib60',
  'calib60YearOfWeek','weekNumNow','livingCostWeekNum','livingCostBand','livingCostRoll','livingCostEstimate','takeSoftBridgePay',
  'calib60SeasonIdx','calib60NowSeasonIdx','calib60NodeTitle','calib60MissedScan','normalizeSaveObj',
  'defaultWeekPlan','fameFloor','gigMissingReqGaps','courseForStatKey','preferredLocForTrainTarget','bestTrainJumpForGig',
  'tutorialFxFingerErr','dateObj','calendarSeason','looksLikeEraId','humanizeEraId','normalizeGigRecord',
  'shootRemain','conseq61State','conseq61DualOf','conseq61SettleEval','softC10WindowActive','fresh'];
for(const f of FNS) eval(extractFn(f));
Math.random = function(){ return 0; };
function ymd(d){ return d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate(); }
function dateAt(di){ const keep = S; S = { dayIndex: di }; const d = dateObj(); S = keep; return d; }
function oldEpochDate(dayIndex){ return new Date(1990, 2, 7 + dayIndex); } /* v66 epoch：1990-03-07 + dayIndex */

/* ================= (1) epoch：1990-01-01 星期一、足 3 年 ================= */
ok('START = 1990-01-01', START.y === 1990 && START.m === 1 && START.d === 1);
ok('dateObj(0) = 1990-01-01', ymd(dateAt(0)) === 19900101);
ok('1990-01-01 係星期一（週一起點夾返）', dateAt(0).getDay() === 1);
ok('dateObj(65) = 1990-03-07（舊 epoch 嘅 day 0）', ymd(dateAt(65)) === 19900307);
ok('足 3 年：dateObj(1095) = 1992-12-31、dateObj(1096) = 1993-01-01',
  ymd(dateAt(1095)) === 19921231 && ymd(dateAt(1096)) === 19930101);
S = { dayIndex: 0 };
ok('開局季節 = 冬', calendarSeason() === '冬');
S = { dayIndex: 45 };
ok('dayIndex 45（2 月中）仍係冬', calendarSeason() === '冬');

/* ================= (2) 評核新週位：52/104、wk43 唔觸、警告跟移 ================= */
ok('邊界週 52／104；地板／警告線不變',
  CONSEQ61_REVIEWS[1990].boundaryWeek === 52 && CONSEQ61_REVIEWS[1991].boundaryWeek === 104 &&
  CONSEQ61_REVIEWS[1990].floor === 45 && CONSEQ61_REVIEWS[1991].floor === 100 &&
  CONSEQ61_REVIEWS[1990].warnLine === 65 && CONSEQ61_REVIEWS[1991].warnLine === 130);
ok('守衛年份對位：yearOfWeek(52)=1990、yearOfWeek(104)=1991',
  calib60YearOfWeek(52) === 1990 && calib60YearOfWeek(104) === 1991);
function evalSave(){ return { fame: 0, popularity: 0, industryCreditDelta: 0, money: 99999, stress: 0, shoots: [], conseq61: { reviews: {}, grace: null } }; }
{
  const st = evalSave();
  const lines43 = conseq61SettleEval(st, 43);
  ok('wk43 週結：冇評核、冇警告、冇 pendingEnding（舊邊界週已廢）',
    !st.conseq61.reviews[1990] && !st.conseq61.pendingEnding && lines43.length === 0);
  const lines49 = conseq61SettleEval(st, 49);
  ok('wk49（距 3 週）：何生警告先行', lines49.some(t => t.includes('評核') && t.includes('何生')) && !st.conseq61.pendingEnding);
  conseq61SettleEval(st, 52);
  ok('wk52 週結：1990 評核先寫入＋判收場（dual 0 < 地板 45）',
    !!st.conseq61.reviews[1990] && st.conseq61.reviews[1990].passed === false &&
    !!st.conseq61.pendingEnding && st.conseq61.pendingEnding.year === 1990);
}

/* ================= (3) softC10 窗改年內週 ================= */
function c10AtWeek(w){ S = { dayIndex: (w - 1) * 7 }; return softC10WindowActive(); }
ok('softC10：第 41 週（年內 41）唔入窗（舊絕對週寫法會誤入）', c10AtWeek(41) === false);
ok('softC10：第 50 週（年內 50）入窗', c10AtWeek(50) === true);
ok('softC10：第二年第 50 週（絕對 102、年內 50）入窗', c10AtWeek(102) === true);
ok('softC10：第二年第 41 週（絕對 93、年內 41）唔入窗', c10AtWeek(93) === false);

/* ================= (4) 開局文字對位 ================= */
{
  /* 真形狀：beats 係 chapters[].open 字串陣列、tutorial 係 steps[].body 字串陣列
     （初版 walker 改唔到陣列字串元素，畀呢兩個 fixture 捉返） */
  const beats = { chapters: [ { id: 'Ch1', open: ['1990 年春，阿偉在黃大仙屋邨起步。', '手上有記數簿和名片冊，開始跑通告。'] } ] };
  jan67OpeningTextFix(beats);
  ok('開場白（open 陣列）：1990 年春 → 1990 年初', beats.chapters[0].open[0] === '1990 年初，阿偉在黃大仙屋邨起步。' && beats.chapters[0].open[1].indexOf('記數簿') >= 0);
  const tut = { steps: [ { id: 'TUT_WELCOME', body: ['1990 年春，你在黃大仙屋邨當臨記起步。', '這階段目標很簡單：先做到有穩定收入。'], bodyAlt: ['你從臨記做起。'] } ] };
  jan67OpeningTextFix(tut);
  ok('教學歡迎卡（body 陣列）：1990 年春 → 1990 年初', tut.steps[0].body[0] === '1990 年初，你在黃大仙屋邨當臨記起步。' && tut.steps[0].body[1].indexOf('穩定收入') >= 0);
  const story = { main: [ { id: 'C1', when: '1990春 / W1-4' }, { id: 'C2', when: '1990春' }, { id: 'C9', when: '1991冬' } ] };
  jan67OpeningTextFix(story);
  ok('C1 時期標籤：1990春 → 1990冬；其他節點唔郁',
    story.main[0].when === '1990冬 / W1-4' && story.main[1].when === '1990春' && story.main[2].when === '1991冬');
  const other = { chapters: [ { id: 'x', open: ['1990 年春，另一段唔關開局事嘅劇情。'] } ] };
  jan67OpeningTextFix(other);
  ok('非開局句子唔誤傷（全句定點對照）', other.chapters[0].open[0].indexOf('1990 年春') === 0);
}

/* ================= (5) 遷移 fixture A：評核前（3 月 epoch 檔） ================= */
function v66SaveBase(){
  return { dayIndex: 200, fame: 30, popularity: 10, acting: 40, stage: 30, vocal: 20, looks: 25, iq: 20, charm: 20,
    stress: 10, money: 8000, stamina: 80, industryCreditDelta: 3,
    flags: {}, npcs: {}, board: {}, booked: [], shoots: [ { id: 's1', gigId: 'g', deadlineDay: 210, hiredAtDay: 195, doneDays: 1, totalDays: 5 } ],
    trainCount: {}, enrolled: {}, years66Shifted: 1,
    story: { gigCount: 2, flags: {}, done: { C1: true }, lastMainDoneDay: 190 },
    mockDebts: [ { id: 'd1', dueDay: 230, dueDays: 30 } ],
    giftMeta: { lastGiveDay: { npc_a: 100 } },
    conseq61: { reviews: {}, grace: null, sick: null },
    awardsFlags: {}, wrapHistory: [], awardsLog: [] };
}
{
  const before = ymd(oldEpochDate(200));
  const mig = normalizeSaveObj(JSON.parse(JSON.stringify(v66SaveBase())));
  ok('A：dayIndex 200 → 265（+65）', mig.dayIndex === 265);
  S = mig;
  ok('A：曆法日期不變（遷移後 dateObj == 舊 epoch 同一日）', ymd(dateObj()) === before);
  ok('A：拍攝 deadlineDay／hiredAtDay 同步 +65', mig.shoots[0].deadlineDay === 275 && mig.shoots[0].hiredAtDay === 260);
  ok('A：doneDays／totalDays／dueDays 係日數唔移', mig.shoots[0].doneDays === 1 && mig.shoots[0].totalDays === 5 && mig.mockDebts[0].dueDays === 30);
  ok('A：債 dueDay +65、story.lastMainDoneDay +65、giftMeta map 值 +65',
    mig.mockDebts[0].dueDay === 295 && mig.story.lastMainDoneDay === 255 && mig.giftMeta.lastGiveDay.npc_a === 165);
  ok('A：打上 startEpoch67 戳、reviews 保持空（冇幻影評核）', mig.startEpoch67 === 1 && Object.keys(mig.conseq61.reviews).length === 0);
  const mig2 = normalizeSaveObj(JSON.parse(JSON.stringify(mig)));
  ok('A：冪等——再載入唔會二次偏移', mig2.dayIndex === 265 && mig2.shoots[0].deadlineDay === 275);
}

/* ================= (6) 遷移 fixture B：評核後（已過舊 wk43 評核） ================= */
{
  const b = v66SaveBase();
  b.dayIndex = 400; /* 3 月 epoch：1991-04-11，已過 1990 評核 */
  b.conseq61.reviews = { 1990: { passed: true, dual: 88 } };
  const before = ymd(oldEpochDate(400));
  const mig = normalizeSaveObj(JSON.parse(JSON.stringify(b)));
  ok('B：dayIndex 400 → 465（+65）', mig.dayIndex === 465);
  S = mig;
  ok('B：曆法日期不變（1991-04-11）', ymd(dateObj()) === before && before === 19910411);
  ok('B：reviews[1990] 原樣保留（passed／dual 唔郁）',
    mig.conseq61.reviews[1990] && mig.conseq61.reviews[1990].passed === true && mig.conseq61.reviews[1990].dual === 88);
  ok('B：冇新增 pendingEnding（唔補評、唔重收）', !mig.conseq61.pendingEnding);
  conseq61SettleEval(mig, 52);
  ok('B：遷移後就算行到 wk52 週結都唔重觸 1990 評核', !mig.conseq61.pendingEnding && mig.conseq61.reviews[1990].dual === 88);
}

/* ================= (7) 日戳 walker 邊界：哨兵／巢狀／map ================= */
{
  const o = { a: { deadlineDay: -1 }, giftMeta: { lastGiveDay: { npc_a: 100, npc_b: -1 } },
    nested: { list: [ { publishDay: 50 } ] }, plain: { dueDays: 14, deadlineDays: 7 }, conseq61: { cooldownUntil: 300, sick: { from: 280, to: 283 } } };
  jan67ShiftDayStamps(o);
  ok('walker：−1 哨兵不變、map 值 +65、巢狀陣列 +65',
    o.a.deadlineDay === -1 && o.giftMeta.lastGiveDay.npc_a === 165 && o.giftMeta.lastGiveDay.npc_b === -1 && o.nested.list[0].publishDay === 115);
  ok('walker：日數欄（dueDays／deadlineDays）唔移', o.plain.dueDays === 14 && o.plain.deadlineDays === 7);
  ok('walker：cooldownUntil +65；sick from/to 由 migrate 點名移（walker 本身唔認 from/to）',
    o.conseq61.cooldownUntil === 365 && o.conseq61.sick.from === 280);
  const b2 = v66SaveBase();
  b2.conseq61.sick = { from: 150, to: 153 };
  const migB2 = normalizeSaveObj(JSON.parse(JSON.stringify(b2)));
  ok('遷移：病倒窗 from/to 同步 +65', migB2.conseq61.sick.from === 215 && migB2.conseq61.sick.to === 218);
}

/* ================= (8) 新檔戳 ================= */
const JAN67_DAY_SHIFT = eval('(' + extractConst('JAN67_DAY_SHIFT').replace(/^const JAN67_DAY_SHIFT\s*=\s*/, '').replace(/;\s*$/, '') + ')');
{
  const f = fresh();
  ok('fresh()：startEpoch67=1（新檔唔會被遷移）＋ years66Shifted=1', f.startEpoch67 === 1 && f.years66Shifted === 1);
  ok('JAN67_DAY_SHIFT = 65', JAN67_DAY_SHIFT === 65);
}

console.log(fails.length ? ('\nFAILURES: ' + fails.length + ' -> ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
