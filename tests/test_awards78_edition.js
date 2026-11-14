// v20a78 AWARDS78 邏輯測試：台慶頒獎年界雙觸發去重。
// 背景（全弧驗證第三輪實證）：day 364（1990-12-31・冬1990・入圍）同 day 365
// （1991-01-01・冬1991・旁聽）連續兩日舉行兩屆台慶。根因：queueAwardsOnSeasonWindow
// 用「今日曆法年」做 S.awardsFlags 去重鍵＋pack 年份；冬季（12–2 月）橫跨公曆年界，
// 同一季冬喺 12 月尾同 1 月頭各開一屆，兼食埋下一年 12 月嗰屆嘅旗標（典禮漂移去 1 月）。
// 修法：awardsEditionYear——冬季屆別歸「開季嗰年」（12 月＝當年、1–2 月＝上一年）；
// 春／夏／秋唔跨年界，屆別年＝曆法年（行為不變）。
// v20a213（用戶 2026-11-14 18:07 拍板）：排期窗口改做 [典禮日−3, 典禮日]（典禮日＝季節首日），
// 端到端日子改用窗口內日子（冬 1990 屆 day 334、冬 1991 屆 day 699、春 1991 屆 day 424）；
// 延期情境改寫：窗口內 C10 讓路完照排同一屆，窗口過咗（day 365）唔再補開。
// (1) awardsEditionYear 單元：冬 12 月→當年、冬 1/2 月→上一年；其餘季節→曆法年。
// (2) 端到端 queue：day 334 開 1990 屆（pack.year=1990、旗標 invited）；
//     標 done 後 day 365、day 400（1991-02-04）唔再開新屆（舊版會開 1991 屆）；
//     day 699（1991-12-01）開 1991 屆；標 done 後 day 730（1992-01-01）唔重開。
// (3) C10 延期唔誤殺：窗口內讓路完照排同一屆（屆別年不變）；窗口過咗唔補開。
// (4) 非冬季對照：春廣告獎 1991 年 3 月開屆年份＝1991（曆法年，冇被提早／推遲）。
// 反證：對 v20a77 index 行 → awardsEditionYear 唔存在 → FAIL。
// 用法：node tests/test_awards78_edition.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) throw new Error('fn not found: '+name);
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){
    if(html[j]==='{') depth++;
    else if(html[j]==='}'){ depth--; if(depth===0) break; }
  }
  return html.slice(i, j+1);
}

/* ---- 世界 stub（season／weekMinSoft 跟線上 SCHEMA_AWARDS_CEREMONY_v1.json 真值） ---- */
var window = {};
var START = { y:1990, m:1, d:1 };
var S = null;
var FREEPLAY_FW = {
  awardsSchema: { ceremonies: [
    { id:'award_harbour_ad',    season:'春', weekMinSoft:6,  medium:'ad' },
    { id:'award_golddisc_music',season:'夏', weekMinSoft:16, medium:'music' },
    { id:'award_harbour_film',  season:'秋', weekMinSoft:28, medium:'film' },
    { id:'award_singho_tv',     season:'冬', weekMinSoft:40, medium:'tv' }
  ]},
  awardsStub: null,
  _awardQueue: [], _pendingAward: null
};
function awardsSoftOn(){ return true; }
function softC10WindowActive(){ return false; }
var builtPacks = [];
function buildAwardResultPack(o){
  builtPacks.push({ ceremonyId:o.ceremonyId, year:o.year });
  return { ceremonyId:o.ceremonyId, year:o.year, tier:'audience', ceremonyName:'X', workCount:0 };
}

let booted = true;
try{
  eval(extractFn('weekNumNow'));
  eval(extractFn('awardsCalendarYear'));
  eval(extractFn('awardsEditionYear'));
  eval(extractFn('calendarSeason'));
  eval(extractFn('awardsCeremonies'));
  eval(extractFn('awardsCeremonyById'));
  eval(extractFn('awardsSeasonMatches'));
  eval(extractFn('awardsWeekOk'));
  eval(extractFn('ensureAwardsFlags'));
  eval(extractFn('awardsFlagKey'));
  eval(extractFn('awardsGetFlag'));
  eval(extractFn('awardsSetFlag'));
  eval(extractFn('ensureAwardQueue'));
  eval(extractFn('queueAwardInvite'));
  eval(extractFn('awards213CeremonyDay'));
  eval(extractFn('awards213HasBooked'));
  eval(extractFn('awards213Booked'));
  eval(extractFn('queueAwardsOnSeasonWindow'));
  /* v20a213：queue 用 AWARDS213_LEAD_DAYS／AWARDS213_SEASON_MONTH（const，要抽出嚟先用到；
     頂層直接 eval——包入 IIFE 嘅 var 出唔返嚟，queue 會拎唔到。） */
  eval(html.slice(html.indexOf('const AWARDS213_LEAD_DAYS ='), html.indexOf(';', html.indexOf('const AWARDS213_LEAD_DAYS =')) + 1).replace('const AWARDS213_LEAD_DAYS =', 'var AWARDS213_LEAD_DAYS ='));
  eval((function(){
    const i2 = html.indexOf('const AWARDS213_SEASON_MONTH =');
    let depth = 0, k = html.indexOf('{', i2);
    for(; k < html.length; k++){
      if(html[k] === '{') depth++;
      else if(html[k] === '}'){ depth--; if(depth === 0) break; }
    }
    return html.slice(i2, k + 1).replace('const AWARDS213_SEASON_MONTH =', 'var AWARDS213_SEASON_MONTH =') + ';';
  })());
}catch(e){
  booted = false;
  ok('AWARDS78 函數存在（awardsEditionYear 可抽出）', false);
  console.log('  extract error: '+e.message);
}

const TV = { id:'award_singho_tv', season:'冬', weekMinSoft:40, medium:'tv' };
const AD = { id:'award_harbour_ad', season:'春', weekMinSoft:6, medium:'ad' };
const FILM = { id:'award_harbour_film', season:'秋', weekMinSoft:28, medium:'film' };
function freshSave(day){
  FREEPLAY_FW._awardQueue = []; FREEPLAY_FW._pendingAward = null; builtPacks = [];
  return { dayIndex:day, awardsFlags:{}, flags:{}, fame:0, npcs:{}, story:{} };
}
function tvPacks(){ return builtPacks.filter(p=>p.ceremonyId==='award_singho_tv'); }

if(booted){
  /* (1) awardsEditionYear 單元（dayIndex 以 1990-01-01 為 day 0） */
  ok('冬・1990-12-31（day 364）→ 1990', awardsEditionYear(TV, 364) === 1990);
  ok('冬・1991-01-01（day 365）→ 1990（歸開季嗰年）', awardsEditionYear(TV, 365) === 1990);
  ok('冬・1991-02-04（day 399）→ 1990', awardsEditionYear(TV, 399) === 1990);
  ok('冬・1991-12-31（day 729）→ 1991', awardsEditionYear(TV, 729) === 1991);
  ok('冬・1992-01-01（day 730）→ 1991', awardsEditionYear(TV, 730) === 1991);
  ok('春・1991-01-01（day 365）→ 1991（非冬季唔調整）', awardsEditionYear(AD, 365) === 1991);
  ok('秋・1991-01-01（day 365）→ 1991（非冬季唔調整）', awardsEditionYear(FILM, 365) === 1991);
  ok('春・1991-03-01（day 424）→ 1991', awardsEditionYear(AD, 424) === 1991);

  /* (2) 端到端：跨年界只開一屆（v20a213：日子改用窗口內——冬屆典禮日 12/1） */
  S = freshSave(334); /* 1990-12-01・冬屆典禮日 */
  queueAwardsOnSeasonWindow();
  ok('day 334：台慶開屆 pack.year=1990', tvPacks().length === 1 && tvPacks()[0].year === 1990);
  ok('day 334：旗標 1990/award_singho_tv=invited', awardsGetFlag(1990, 'award_singho_tv') === 'invited');
  awardsSetFlag(1990, 'award_singho_tv', 'done'); FREEPLAY_FW._pendingAward = null;
  S.dayIndex = 365; builtPacks = [];
  queueAwardsOnSeasonWindow();
  ok('day 365（1991-01-01）：唔再開第二屆（舊版會開 1991 屆）', tvPacks().length === 0);
  S.dayIndex = 399; builtPacks = [];
  queueAwardsOnSeasonWindow();
  ok('day 399（1991-02-04・同季冬）：仍然唔重開', tvPacks().length === 0);
  S.dayIndex = 699; builtPacks = []; /* 1991-12-01・下一屆典禮日 */
  queueAwardsOnSeasonWindow();
  ok('day 699（1991-12-01）：開下一屆 pack.year=1991', tvPacks().length === 1 && tvPacks()[0].year === 1991);
  awardsSetFlag(1991, 'award_singho_tv', 'done'); FREEPLAY_FW._pendingAward = null;
  S.dayIndex = 730; builtPacks = [];
  queueAwardsOnSeasonWindow();
  ok('day 730（1992-01-01）：1991 屆唔重開', tvPacks().length === 0);

  /* (3) C10 延期情境（v20a213 改寫）：窗口內讓路完照排同一屆；窗口過咗唔補開。
     註：真實曆法下 C10 窗口（每年第 49–52 週）掂唔到請柬窗口（11/28–12/1 係第 48 週），
     呢度用 stub 扮 C10 喺窗口內 active，驗延期本身唔改屆別年。 */
  S = freshSave(334);
  softC10WindowActive = function(){ return true; };
  queueAwardsOnSeasonWindow();
  ok('延期情境：day 334 C10 讓路嗰陣唔排（返 0）', tvPacks().length === 0);
  softC10WindowActive = function(){ return false; };
  queueAwardsOnSeasonWindow();
  ok('延期情境：C10 讓路完 day 334 照排，仍然係 1990 屆（冇變第二屆）',
    tvPacks().length === 1 && tvPacks()[0].year === 1990);
  S = freshSave(365);
  queueAwardsOnSeasonWindow();
  ok('延期情境：窗口過咗（day 365）唔再補開', tvPacks().length === 0);

  /* (4) 非冬季對照：春廣告獎 */
  S = freshSave(424); /* 1991-03-01・春 */
  queueAwardsOnSeasonWindow();
  const adPacks = builtPacks.filter(p=>p.ceremonyId==='award_harbour_ad');
  ok('春・day 424：廣告獎開屆 pack.year=1991（曆法年不變）', adPacks.length === 1 && adPacks[0].year === 1991);
}

console.log(fails.length ? ('\nFAILED: '+fails.length) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
