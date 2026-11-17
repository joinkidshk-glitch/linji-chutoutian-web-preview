// v20a67 JAN67 邏輯測試：1 月開局 epoch／評核新週位／softC10 年內週／開局文字對位（v228：舊檔遷移已刪）。
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
  'dateObj','calendarSeason','looksLikeEraId','humanizeEraId','normalizeGigRecord',
  'shootRemain','conseq61State','conseq61DualOf','conseq61SettleEval','softC10WindowActive','fresh'];
for(const f of FNS) eval(extractFn(f));
Math.random = function(){ return 0; };
function ymd(d){ return d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate(); }
function dateAt(di){ const keep = S; S = { dayIndex: di }; const d = dateObj(); S = keep; return d; }

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
  const story = { main: [ { id: 'N1', when: '1990春 / W1-4' }, { id: 'N2', when: '1990春' }, { id: 'N10', when: '1991冬' } ] };
  jan67OpeningTextFix(story);
  ok('N1 時期標籤：1990春 → 1990冬；其他節點唔郁',
    story.main[0].when === '1990冬 / W1-4' && story.main[1].when === '1990春' && story.main[2].when === '1991冬');
  const other = { chapters: [ { id: 'x', open: ['1990 年春，另一段唔關開局事嘅劇情。'] } ] };
  jan67OpeningTextFix(other);
  ok('非開局句子唔誤傷（全句定點對照）', other.chapters[0].open[0].indexOf('1990 年春') === 0);
}

/* ================= (8) 新檔戳 ================= */
{
  const f = fresh();
  ok('fresh()：startEpoch67=1＋years66Shifted=1（v228：遷移已刪，留印只為存檔格式相容）', f.startEpoch67 === 1 && f.years66Shifted === 1);
}

console.log(fails.length ? ('\nFAILURES: ' + fails.length + ' -> ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
