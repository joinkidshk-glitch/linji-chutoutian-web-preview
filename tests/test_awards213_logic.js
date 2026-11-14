// v20a213 請柬提前 3 日＋典禮改晚上播・邏輯測試（用戶 2026-11-14 18:07 拍板）：
// 1. 典禮日＝季節首日（春 3/1・夏 6/1・秋 9/1・冬 12/1），請柬窗口＝[典禮日−3, 典禮日]。
// 2. 請柬決定＝預約（S.awardBooked213），唔即播；典禮日未完唔播，翌日晨鏈／日結續鏈先播。
// 3. 晚間播：出席＝現場版＋結果卡；推辭＝電視直播版＋log skipped＋翌日報紙 declined 版。
// 4. 報紙 publishDay＝典禮日＋1（唔係播嗰陣 dayIndex＋1）。
// 5. 舊存檔 pending 請柬遷移：還原後照彈，決定嗰陣典禮日取屆別季節首日（過期當今晚）；
//    決定咗就唔會由旗標重建返請柬。未知 ceremonyId 嘅合成 pack 保留舊即播行為。
// 6. 請柬文案：有 stamp 寫實日期（6月1日獎項／席位＋典禮夜行），冇 stamp 跌返「今晚」。
// 7. 典禮日係關鍵日（唔可以靜默加速掠過）。
// 反證：對 pristine main f58f19c index 行 → v213 標記未入 → FAIL（唔 crash）。
// 用法：node tests/test_awards213_logic.js [path-to-index.html]
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

/* 反證守衛：v213 嘢唔存在嗰陣乾淨 FAIL（逐項列出），唔好等 extraction 喺頂層 throw 崩潰。 */
const NEED213 = ['AWARDS213_LEAD_DAYS', 'awardBooked213', 'awards213PlayBookedEvening', '典禮夜：'];
let missing213 = NEED213.filter(s => html.indexOf(s) < 0);
if(missing213.length){
  missing213.forEach(m=>{ fails.push('反證：' + m + ' 唔存在'); console.log('FAIL 反證：' + m + ' 唔存在（pristine main 預期，v213 未入）'); });
  console.log('\nFAILED: ' + fails.length);
  process.exit(1);
}

/* ---- harness ---- */
var START = { y: 1990, m: 1, d: 1 };
var S = { dayIndex: 148, fame: 26, industryCredit: 49, wrapHistory: [],
  awardsFlags: {}, awardsLog: [], pendingAwardPack: null, awardBooked213: null,
  newspaperQueue: [], newspaperClippings: [], pendingMorningPaper: null };
var FREEPLAY_FW = {
  awardsSchema: JSON.parse(fs.readFileSync(path.join(path.dirname(htmlPath), 'content', 'SCHEMA_AWARDS_CEREMONY_v1.json'), 'utf8')),
  awardsStub: JSON.parse(fs.readFileSync(path.join(path.dirname(htmlPath), 'content', 'STUB_AWARDS_CEREMONY_v1.json'), 'utf8')),
  _pendingAward: null, _awardQueue: [], _awardBooked213: null, _awardCeremonyDay213: null
};
var __c10 = false;
function softC10WindowActive(){ return __c10; }
function weekNumNow(){ return Math.floor(((S && S.dayIndex) || 0) / 7) + 1; }
function buildAwardResultPack(o){
  o = o || {};
  return { ceremonyId: o.ceremonyId, year: o.year, tier: o.forceTier || 'gallery',
    dayIndex: (S && (S.dayIndex | 0)) || 0, inviteTitle: 'x', categories: [] };
}
var play62Calls = [];
function awards62PlayCeremony(pack, done){ play62Calls.push(pack); if(typeof done === 'function') done(); }
function awards62CeremonyActive(){ return __ceremonyActive; }
var __ceremonyActive = false;
var resultCalls = [];
function presentAwardResult(pack, cont){ resultCalls.push({ pack: pack, override: FREEPLAY_FW._awardCeremonyDay213 }); if(typeof cont === 'function') cont(); }
var logCalls = [];
function commitAwardToLog(pack){ logCalls.push(pack); }
var toastCalls = [];
function toast(msg, opts){ toastCalls.push(msg); }
function setStoryPlayLock(){}
var modalCaptured = null;
function modal(htmlText, btns, opts){ modalCaptured = { html: htmlText, btns: btns, opts: opts || {} }; return true; }
global.document = { getElementById: function(){ return { classList: { remove: function(){} } }; } };
function planDayWouldWrap(){ return false; }
function poster59Path(){ return ''; }
function awards63FocusFellows(){ return []; }
function newspaperMediumFromAward(pack){ return (pack && pack.medium) || ''; }
function newspaperCopyFromTemplate(tmpl, fb){
  return { paperName: fb.paperName, headline: fb.headline, dek: fb.dek, fameDelta: fb.fameDelta,
    clipLabel: '', rumorEcho: '', templateId: '', templateEventKey: '', medium: fb.medium };
}
function newspaperPickTemplate(){ return null; }
function awardWinner149(){ return null; }
function awardGalleryCopy149(){ return { headline: 'x', dek: 'y' }; }
var NEWSPAPER_AWARD_GALLERY_TEMPLATES_136 = [{ medium: 'music', id: 'g1' }];
function saveQ(){}

for(const f of ['awardsCalendarYear', 'awardsEditionYear', 'awardsCeremonies',
  'awardsCeremonyById', 'awardsFlagKey', 'awardsGetFlag', 'awardsSetFlag',
  'ensureAwardsFlags', 'ensureAwardQueue', 'queueAwardInvite',
  'restorePendingAward136', 'awardsSeasonMatches', 'awardsWeekOk',
  'awards213DateObj', 'awards213DateLabel', 'awards213DateLabelShort',
  'awards213CeremonyDay', 'awards213NightLabel', 'awards213CeremonyDayForPack',
  'awards213Booked', 'awards213HasBooked', 'awards213Book', 'awards213ClearBooked',
  'awards213BookedForDay', 'awards213DueBooked', 'awards213PlayDecision',
  'awards213PlayBookedEvening', 'awards213EveningThen',
  'queueAwardsOnSeasonWindow', 'awardsCatsSorted184', 'renderAwardInviteHtml',
  'awards62GateLineHtml', 'awards63InviteBitHtml', 'presentAwardInvite',
  'ensureNewspaperQueue', 'ensureNewspaperClippings', 'newspaperEventSeen',
  'enqueueNewspaperItem', 'enqueueNewspaperFromAward', 'isCriticalPlanDay'])
  eval(extractFn(f));
eval(extractConst('AWARDS213_LEAD_DAYS').replace('const AWARDS213_LEAD_DAYS =', 'var AWARDS213_LEAD_DAYS ='));
eval(extractConst('AWARDS213_SEASON_MONTH').replace('const AWARDS213_SEASON_MONTH =', 'var AWARDS213_SEASON_MONTH ='));
eval(extractConst('AWARDS62_MEDIUM_LABEL').replace('const AWARDS62_MEDIUM_LABEL =', 'var AWARDS62_MEDIUM_LABEL ='));
eval(extractConst('AWARDS188_CATEGORIES').replace('const AWARDS188_CATEGORIES =', 'var AWARDS188_CATEGORIES ='));

function reset(){
  S.dayIndex = 148; S.awardsFlags = {}; S.awardsLog = []; S.pendingAwardPack = null;
  S.awardBooked213 = null; S.newspaperQueue = []; S.newspaperClippings = [];
  FREEPLAY_FW._pendingAward = null; FREEPLAY_FW._awardQueue = [];
  FREEPLAY_FW._awardBooked213 = null; FREEPLAY_FW._awardCeremonyDay213 = null;
  play62Calls = []; resultCalls = []; logCalls = []; toastCalls = [];
  modalCaptured = null; __c10 = false; __ceremonyActive = false;
}

/* ---- 1. 典禮日＝季節首日（1990–1992） ---- */
ok('1：春 1990 典禮日 3/1＝day 59', awards213CeremonyDay({ season: '春' }, 1990) === 59);
ok('1：夏 1990 典禮日 6/1＝day 151', awards213CeremonyDay({ season: '夏' }, 1990) === 151);
ok('1：秋 1990 典禮日 9/1＝day 243', awards213CeremonyDay({ season: '秋' }, 1990) === 243);
ok('1：冬 1990 典禮日 12/1＝day 334', awards213CeremonyDay({ season: '冬' }, 1990) === 334);
ok('1：夏 1991 典禮日 6/1＝day 516', awards213CeremonyDay({ season: '夏' }, 1991) === 516);
ok('1：冬 1991 典禮日 12/1＝day 699', awards213CeremonyDay({ season: '冬' }, 1991) === 699);
ok('1：春 1992 典禮日 3/1＝day 790（閏年）', awards213CeremonyDay({ season: '春' }, 1992) === 790);
ok('1：冬 1992 典禮日 12/1＝day 1065', awards213CeremonyDay({ season: '冬' }, 1992) === 1065);
ok('1：LEAD_DAYS＝3', AWARDS213_LEAD_DAYS === 3);
ok('1：日期標籤 6/1＝「6月1日（星期五）」', awards213DateLabel(151) === '6月1日（星期五）');
ok('1：日期標籤 3/1＝「3月1日（星期四）」', awards213DateLabel(59) === '3月1日（星期四）');
ok('1：日期標籤 12/1＝「12月1日（星期六）」', awards213DateLabel(334) === '12月1日（星期六）');
ok('1：短標籤 6/1＝「6月1日」', awards213DateLabelShort(151) === '6月1日');

/* ---- 2. 請柬決定＝預約，唔即播 ---- */
function musicPack(stamp){
  const p = { ceremonyId: 'award_golddisc_music', year: 1990, tier: 'gallery', medium: 'music',
    tierLabel: '旁聽席', displayName: '星河金碟夜', season: '夏', venue99: '金禧大酒店',
    inviteTitle: '金碟夜請柬', inviteDek: '你收到一張席位信。',
    categories: [{ id: 'cat_music_male', label: '最佳男歌手' }],
    repWork62: '', repGigId63: '',
    standing62: { tier: 'gallery', wraps: 0, wrapMin: 1, dualOk: true, gapWorks: 1, gapWin: 0, repTitle: '' } };
  if(stamp) p.ceremonyDay213 = 151;
  return p;
}
reset(); S.dayIndex = 148;
let pack = musicPack(true);
let contN = 0;
ok('2：請柬 modal 彈出（出席／推辭掣齊）',
  presentAwardInvite(pack, function(){ contN++; }) === true &&
  modalCaptured && modalCaptured.btns.map(b => b.label).join('/') === '出席/推辭');
modalCaptured.btns[0].on(); /* 出席 */
ok('2：出席＝預約（S.awardBooked213：attend＋典禮日 151），唔即播典禮',
  S.awardBooked213 && S.awardBooked213.decision === 'attend' &&
  S.awardBooked213.ceremonyDay === 151 && play62Calls.length === 0);
ok('2：出席預約後續鏈行咗（cont 叫咗一次）', contN === 1);
ok('2：預約後 pending 清走（_pendingAward＋S.pendingAwardPack）',
  FREEPLAY_FW._pendingAward === null && S.pendingAwardPack === null);
ok('2：典禮日未完唔播（day 151 返 false，booking 留返）',
  (S.dayIndex = 151, awards213PlayBookedEvening(function(){}) === false) &&
  S.awardBooked213 !== null);
ok('2：翌日播（day 152 返 true，播完 booking 清走）',
  (S.dayIndex = 152, awards213PlayBookedEvening(function(){ contN++; }) === true) &&
  S.awardBooked213 === null && FREEPLAY_FW._awardBooked213 === null);
ok('2：晚間播用現場版（presentAwardResult 叫咗，pack.dayIndex＝典禮日 151）',
  resultCalls.length === 1 && resultCalls[0].pack.dayIndex === 151);
ok('2：播嗰陣報紙 override＝典禮日（151），播完清返 null',
  resultCalls[0].override === 151 && FREEPLAY_FW._awardCeremonyDay213 === null);
ok('2：播完續鏈行咗（cont 叫多一次）', contN === 2);
ok('2：播完唔重播（第二次返 false）', awards213PlayBookedEvening(function(){}) === false);

/* 推辭＝預約 decline，晚間播電視直播版 */
reset(); S.dayIndex = 148;
pack = musicPack(true);
contN = 0;
presentAwardInvite(pack, function(){ contN++; });
modalCaptured.btns[1].on(); /* 推辭 */
ok('2：推辭＝預約 decline（典禮日 151），唔即播',
  S.awardBooked213 && S.awardBooked213.decision === 'decline' && play62Calls.length === 0 && contN === 1);
S.dayIndex = 152;
ok('2：推辭晚間播電視直播版（bestOutcome gallery＋declined165）',
  awards213PlayBookedEvening(function(){ contN++; }) === true &&
  play62Calls.length === 1 && play62Calls[0].bestOutcome === 'gallery' && play62Calls[0].declined165 === true);
ok('2：推辭播完入 log（skipped＋獎勵歸零）＋報紙 declined 版（publishDay＝典禮日＋1＝152）＋toast，唔出結果卡',
  logCalls.length === 1 && logCalls[0].skipped === true &&
  logCalls[0].rewardsApplied.stageVolume === 0 &&
  S.newspaperQueue.length === 1 && S.newspaperQueue[0].publishDay === 152 &&
  S.newspaperQueue[0].enqueuedDay === 151 &&
  S.newspaperQueue[0].templateEventKey === 'award_declined.music' &&
  toastCalls.indexOf('已推辭席位') >= 0 && resultCalls.length === 0 && contN === 2);

/* onDismiss＝推辭 */
reset(); S.dayIndex = 148;
pack = musicPack(true);
contN = 0;
presentAwardInvite(pack, function(){ contN++; });
modalCaptured.opts.onDismiss();
ok('2：dismiss＝推辭預約（唔係即播）', S.awardBooked213 && S.awardBooked213.decision === 'decline' && play62Calls.length === 0);

/* 未知 ceremonyId 嘅合成 pack 保留舊即播行為（in-page 自檢假請柬） */
reset(); S.dayIndex = 148;
const fakePack = { ceremonyId: 'award_test_invite', year: 1988, displayName: '測試請柬' };
contN = 0;
presentAwardInvite(fakePack, function(){ contN++; });
modalCaptured.btns[0].on();
ok('2：合成 pack 出席照舊即播（唔入 booking）',
  play62Calls.length === 1 && S.awardBooked213 === null && contN === 1);
reset();
presentAwardInvite(fakePack, function(){ contN++; });
modalCaptured.btns[1].on();
ok('2：合成 pack 推辭照舊即播電視版（log＋declined 報紙）',
  play62Calls.length === 1 && logCalls.length === 1 && S.newspaperQueue.length === 1 && S.awardBooked213 === null);

/* ---- 3. 預約咗就唔重排／唔重建 ---- */
reset(); S.dayIndex = 148;
pack = musicPack(true);
awards213Book(pack, 'attend');
ok('3：預約咗 queueAwardInvite 唔再排入 pending', (queueAwardInvite(musicPack(true)), FREEPLAY_FW._pendingAward === null));
S.awardsFlags = { '1990/award_golddisc_music': 'invited' };
S.pendingAwardPack = null;
restorePendingAward136();
ok('3：預約咗 restore 唔會由旗標重建返請柬', FREEPLAY_FW._pendingAward === null);
ok('3：典禮日係關鍵日（isCriticalPlanDay 返 true，唔靜默加速）',
  (S.dayIndex = 151, isCriticalPlanDay('rest', false) === true));
ok('3：冇預約嗰日唔係關鍵日', (awards213ClearBooked(), isCriticalPlanDay('rest', false) === false));
ok('3：典禮進行中唔重入（guard 返 false，booking 留返）',
  (awards213Book(musicPack(true), 'attend'), S.dayIndex = 152, __ceremonyActive = true,
   awards213PlayBookedEvening(function(){}) === false && S.awardBooked213 !== null));
ok('3：已入 log（done 旗標）唔重播',
  (__ceremonyActive = false, awardsSetFlag(1990, 'award_golddisc_music', 'done'),
   awards213PlayBookedEvening(function(){}) === false));

/* ---- 4. 舊存檔 pending 請柬遷移 ---- */
reset(); S.dayIndex = 151;
const oldPack = { ceremonyId: 'award_golddisc_music', year: 1990, tier: 'gallery',
  dayIndex: 151, displayName: '星河金碟夜', season: '夏', venue99: '金禧大酒店',
  inviteTitle: '金碟夜請柬', inviteDek: '你收到一張席位信。', categories: [],
  repWork62: '', repGigId63: '',
  standing62: { tier: 'gallery', wraps: 0, wrapMin: 1, dualOk: true, gapWorks: 1, gapWin: 0, repTitle: '' } };
S.awardsFlags = { '1990/award_golddisc_music': 'invited' };
S.pendingAwardPack = oldPack;
restorePendingAward136();
ok('4：舊存檔 pending 請柬還原返（唔會唔見）',
  FREEPLAY_FW._pendingAward === oldPack);
contN = 0;
presentAwardInvite(oldPack, function(){ contN++; });
modalCaptured.btns[0].on();
ok('4：舊請柬決定嗰陣典禮日＝屆別季節首日（151，唔係 build 日亂估）',
  S.awardBooked213 && S.awardBooked213.ceremonyDay === 151 && contN === 1);
S.dayIndex = 152;
ok('4：舊請柬預約咗嗰晚照播', awards213PlayBookedEvening(function(){}) === true);
/* 過期舊 pack（載入嗰陣已經過咗典禮日）→ 當今晚 */
reset(); S.dayIndex = 153;
const stalePack = musicPack(false);
stalePack.dayIndex = 151;
awards213Book(stalePack, 'attend');
ok('4：過期 pack 預約典禮日＝今日（153，當今晚，唔會開唔到）',
  S.awardBooked213.ceremonyDay === 153);

/* ---- 5. 報紙 publishDay＝典禮日＋1（真 enqueueNewspaperFromAward） ---- */
reset();
const paperPack = { ceremonyId: 'award_golddisc_music', year: 1990, medium: 'music',
  displayName: '星河金碟夜', bestOutcome: 'gallery', skipped: false,
  press: { paperName: '娛樂快報', headline: '金碟夜見報', dek: '側記。' },
  news: {}, categories: [], rewardsApplied: {} };
S.dayIndex = 152;
FREEPLAY_FW._awardCeremonyDay213 = 151;
let item = enqueueNewspaperFromAward(paperPack);
ok('5：晚間播報紙 enqueuedDay＝典禮日 151、publishDay＝152（唔係 153）',
  item && item.enqueuedDay === 151 && item.publishDay === 152);
FREEPLAY_FW._awardCeremonyDay213 = null;
const paperPack2 = { ceremonyId: 'award_harbour_film', year: 1991, medium: 'film',
  displayName: '維港影藝獎', bestOutcome: 'gallery', skipped: false,
  press: { paperName: '娛樂快報', headline: '影藝獎見報', dek: '側記。' },
  news: {}, categories: [], rewardsApplied: {} };
item = enqueueNewspaperFromAward(paperPack2);
ok('5：冇 override 嗰陣照舊（enqueuedDay＝今日 152、publishDay＝153）',
  item && item.enqueuedDay === 152 && item.publishDay === 153);

/* ---- 6. 請柬文案：有 stamp 寫實日期，冇 stamp 跌返「今晚」 ---- */
reset();
const galInvite = renderAwardInviteHtml(musicPack(true));
ok('6：有 stamp 請柬有「典禮夜：6月1日（星期五）」行',
  galInvite.indexOf('典禮夜：6月1日（星期五）') >= 0);
ok('6：有 stamp gallery 獎項行寫實日期（6月1日獎項），唔再寫「今晚獎項」',
  galInvite.indexOf('6月1日獎項：最佳男歌手、最佳女歌手、最佳新人獎（觀禮）') >= 0 &&
  galInvite.indexOf('今晚獎項') < 0);
const galInviteOld = renderAwardInviteHtml(musicPack(false));
ok('6：冇 stamp 請柬跌返「今晚獎項」（舊測試逐字期望唔郁）',
  galInviteOld.indexOf('今晚獎項：最佳男歌手、最佳女歌手、最佳新人獎（觀禮）') >= 0);
const gateStamped = awards62GateLineHtml(musicPack(true));
ok('6：有 stamp 閘句寫實日期（6月1日席位）',
  gateStamped.indexOf('6月1日席位：觀禮。今年仲差 1 部唱片作品先夠入圍（而家 0/1）。') >= 0);
const gateOld = awards62GateLineHtml(musicPack(false));
ok('6：冇 stamp 閘句跌返「今晚席位」',
  gateOld.indexOf('今晚席位：觀禮。今年仲差 1 部唱片作品先夠入圍（而家 0/1）。') >= 0);

console.log(fails.length ? ('\nFAILED: ' + fails.length) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
