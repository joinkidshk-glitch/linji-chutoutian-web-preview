// v20a66 YEARS66 年份推移邏輯測試：epoch／評核鍵／生活費年份閘／gig 正規化 remap／存檔遷移。
// 反證：喺 v20a65 index 上行會 FAIL（START 仍 1988、冇 YEARS66 block、冇遷移）。
// 用法：node tests/test_years66_logic.js [path-to-index.html]
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
/* YEARS66 block 全段抽出（marker → refreshCopyPacksFromDisk 之前） */
function extractYears66Block(){
  const a = html.indexOf('/* ===== v20a66 YEARS66');
  const b = html.indexOf('async function refreshCopyPacksFromDisk(){');
  if(a < 0 || b < 0 || b <= a) throw new Error('YEARS66 block not found');
  return html.slice(a, b);
}

/* ---- 世界 stub（跟 calib60/giglib36 測試同一套路） ---- */
var window = {};
var location = { search: '' };
var localStorage = { getItem: () => null, setItem: () => {}, removeItem: () => {} };
var S = null;
var refreshMoneyHud = function(){};
var softPreviewOn = function(){ return false; };
eval(extractConst('START').replace('const START =', 'var START ='));
eval(extractYears66Block());
for(const c of ['STAT_LABEL','STAT_MAX','STRESS_MAX','LOCS','COURSE_DEFS']) eval(extractConst(c).replace('const ' + c + ' =', 'var ' + c + ' ='));
for(const c of ['CALIB60_FAME_BANDS','CALIB60_ATTR_BANDS','CALIB60_SCALED_KEYS','CALIB60_NODE_WINDOWS','CALIB60_NODE_TITLES','CONSEQ61_REVIEWS']) eval(extractConst(c).replace('const ' + c + ' =', 'var ' + c + ' ='));
const FNS = ['R','clamp','statHardMax','dualTrackNumbers','syncDualTracks','apply',
  'calib60BandScale','calib60ScaleFor','calib60BankedGain','calib60FameGain','calib60ScaleDelta','applyCalib60',
  'calib60YearOfWeek','weekNumNow','livingCostWeekNum','livingCostBand','livingCostRoll','livingCostEstimate','takeSoftBridgePay',
  'calib60SeasonIdx','calib60NowSeasonIdx','calib60NodeTitle','calib60MissedScan','normalizeSaveObj',
  'defaultWeekPlan','fameFloor','gigMissingReqGaps','courseForStatKey','preferredLocForTrainTarget','bestTrainJumpForGig',
  'tutorialFxFingerErr','dateObj','looksLikeEraId','humanizeEraId','normalizeGigRecord'];
for(const f of FNS) eval(extractFn(f));
Math.random = function(){ return 0; };

/* ================= (1) epoch ================= */
ok('START = 1990-01-01（v20a67 JAN67）', START.y === 1990 && START.m === 1 && START.d === 1);
const d0 = dateObj(0);
ok('dateObj(0) = 1990年1月1日', d0.getFullYear() === 1990 && d0.getMonth() === 0 && d0.getDate() === 1);
ok('calib60YearOfWeek：wk1=1990、wk52=1990、wk54=1991、wk104=1991、wk106=1992（v20a67）',
  calib60YearOfWeek(1) === 1990 && calib60YearOfWeek(52) === 1990 && calib60YearOfWeek(54) === 1991 &&
  calib60YearOfWeek(104) === 1991 && calib60YearOfWeek(106) === 1992);

/* ================= (2) 評核鍵＋生活費年份閘 ================= */
ok('CONSEQ61_REVIEWS 鍵 = 1990/1991、地板 45/100 不變',
  CONSEQ61_REVIEWS[1990] && CONSEQ61_REVIEWS[1990].floor === 45 && CONSEQ61_REVIEWS[1990].boundaryWeek === 52 &&
  CONSEQ61_REVIEWS[1991] && CONSEQ61_REVIEWS[1991].floor === 100 && CONSEQ61_REVIEWS[1991].boundaryWeek === 104 &&
  !CONSEQ61_REVIEWS[1988] && !CONSEQ61_REVIEWS[1989]);
S = { fame: 0, popularity: 0, industryCreditDelta: 0 };
ok('生活費：wk50 仍係曆法 1990 → 未加級 2400（v20a67：加級跟真日曆年）', livingCostBand(50).mid === 2400);
ok('生活費：1991 年 wk56 = 2400+300（年份加幅跟移）', livingCostBand(56).mid === 2700);
ok('生活費：1992 年 wk110 = 2400+600', livingCostBand(110).mid === 3000);
S = null;

/* ================= (3) gig 正規化 remap ================= */
const gIn = { id: 'gig_1988_film_test', type: '電影', year: 1988, season: '春', loc: 'film_lion',
  title: '1988年《試驗》', workTitle: '《試驗》', synopsis: '1989 年上映的電影', req: { acting: 10 }, pay: [100, 200] };
const g1 = normalizeGigRecord(JSON.parse(JSON.stringify(gIn)));
ok('gig remap：year 1988 → 1990', g1.year === 1990);
ok('gig remap：title 年份字眼 +2', g1.title.indexOf('1990年') >= 0 && g1.title.indexOf('1988') < 0);
ok('gig remap：synopsis 年份字眼 +2', g1.synopsis.indexOf('1991 年') >= 0 && g1.synopsis.indexOf('1989') < 0);
ok('gig remap：id 不變（存檔鍵）', g1.id === 'gig_1988_film_test');
const g2 = normalizeGigRecord(g1);
ok('gig remap 冪等：再 normalize 唔會變 1992', g2.year === 1990 && g2.title.indexOf('1990年') >= 0);

/* ================= (4) years66Walk 單位行為 ================= */
const wIn = { id: 'gig_1988_x', eraTag: 'era_1988_spring', year: 1989, title: '1989年夏', nested: { when: '1990冬', pay: 1990 } };
years66Walk(wIn, null);
ok('walk：id／eraTag 跳過不變', wIn.id === 'gig_1988_x' && wIn.eraTag === 'era_1988_spring');
ok('walk：year 鍵 +2、文字 +2', wIn.year === 1991 && wIn.title === '1991年夏' && wIn.nested.when === '1992冬');
ok('walk：非年份數字不變（pay 1990）', wIn.nested.pay === 1990);
years66Walk(wIn, null);
ok('walk 冪等：二次行唔再移', wIn.year === 1991 && wIn.title === '1991年夏');

/* ================= (5) 存檔遷移（v65 形狀 fixture） ================= */
function v65Save(){
  return { dayIndex: 500, fame: 40, popularity: 10, acting: 50, stage: 40, vocal: 30, looks: 30, iq: 25, charm: 25,
    stress: 20, money: 9000, stamina: 80, industryCreditDelta: 5,
    flags: {}, npcs: {}, board: {}, booked: [], shoots: [], trainCount: {}, enrolled: {},
    story: { gigCount: 3, flags: {}, done: { C1: true } },
    conseq61: { reviews: { 1988: { passed: true, dual: 70 }, 1989: { passed: false, dual: 40 } },
      pendingEnding: { kind: 'review', year: 1988, atDay: 300 } },
    ending410: { career: 'E7', careerVariant: 'review1989', earlyEnd: { kind: 'review', year: 1989, floor: 100 } },
    awardsFlags: { '1988/award_harbour_film': { attended: true } },
    wrapHistory: [ { gigId: 'gig_1988_film_01', year: 1988, title: '舊作' } ],
    awardsLog: [ { year: 1989, ceremonyId: 'award_singho_tv' } ] };
}
const mig = normalizeSaveObj(JSON.parse(JSON.stringify(v65Save())));
ok('遷移：v66 年份 remap 之後 v67 日數 +65（組裝行為；500 → 565）', mig.dayIndex === 565);
ok('遷移：打上 years66Shifted 戳', mig.years66Shifted === 1);
ok('遷移：reviews 鍵 1988/1989 → 1990/1991（內容保留）',
  !mig.conseq61.reviews[1988] && !mig.conseq61.reviews[1989] &&
  mig.conseq61.reviews[1990] && mig.conseq61.reviews[1990].dual === 70 &&
  mig.conseq61.reviews[1991] && mig.conseq61.reviews[1991].dual === 40);
ok('遷移：pendingEnding.year → 1990', mig.conseq61.pendingEnding.year === 1990);
ok('遷移：careerVariant review1989 → review1991', mig.ending410.careerVariant === 'review1991');
ok('遷移：earlyEnd.year → 1991', mig.ending410.earlyEnd.year === 1991);
ok('遷移：awardsFlags 鍵年份 → 1990/', !!mig.awardsFlags['1990/award_harbour_film'] && !mig.awardsFlags['1988/award_harbour_film']);
ok('遷移：wrapHistory year → 1990、gigId 不變', mig.wrapHistory[0].year === 1990 && mig.wrapHistory[0].gigId === 'gig_1988_film_01');
ok('遷移：awardsLog year → 1991', mig.awardsLog[0].year === 1991);
const mig2 = normalizeSaveObj(JSON.parse(JSON.stringify(mig)));
ok('遷移冪等：再載入唔會二次 +2',
  mig2.conseq61.reviews[1990] && mig2.conseq61.reviews[1990].dual === 70 && !mig2.conseq61.reviews[1992] &&
  mig2.wrapHistory[0].year === 1990 && mig2.ending410.careerVariant === 'review1991');

/* ================= (6) 新檔唔受遷移影響 ================= */
const freshLike = v65Save();
freshLike.years66Shifted = 1;
freshLike.conseq61.reviews = { 1990: { passed: true, dual: 88 } };
freshLike.conseq61.pendingEnding = null;
freshLike.ending410 = null;
freshLike.wrapHistory = [ { gigId: 'gig_1988_film_01', year: 1990, title: '新作' } ];
const keep = normalizeSaveObj(JSON.parse(JSON.stringify(freshLike)));
ok('新檔（已打戳）：reviews／wrapHistory 原封不動',
  keep.conseq61.reviews[1990] && keep.conseq61.reviews[1990].dual === 88 && keep.wrapHistory[0].year === 1990);

/* ================= (7) spPlayerMeta eraTag 顯示唔漏舊年份 ================= */
var BehaviorGate = { featureFlag_softBehaviorGatePreview: function(){ return false; } };
var spIsForcedStory = function(){ return false; };
eval(extractFn('spSoftLane'));
eval(extractFn('spPlayerMeta'));
ok('spPlayerMeta：eraTag 舊曆編碼顯示 +2（era_1988 → 主線 · 1990）',
  spPlayerMeta({ id: 'R_TEST', eraTag: 'era_1988_spring', title: '' }, null, '') === '主線 · 1990');
ok('spPlayerMeta：when 已 walk 時唔雙重移（1991夏 → 主線 · 1991）',
  spPlayerMeta({ id: 'R_TEST2', when: '1991夏', title: '' }, null, '') === '主線 · 1991');

console.log(fails.length ? ('\nFAILURES: ' + fails.length + ' -> ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
