// v20a91 AUD91 試鏡流程改版・邏輯測試
// 合約（用戶 2026-11-11 拍板，照明星志願嗰套）：
//   A 等待帶：入門/臨記 1–2 日、一般 2–3 日、高級/大製作 3–4 日（試鏡刻定死）
//   B 狀態機：doAudition 只入 pending（結果＋片酬＋效果預roll 定死），試鏡當日
//     唔揭曉、唔入任何成敗效果、唔開 shoot；存檔 JSON 來回後成單不變（防刷骰）
//   C 公佈時機：revealDay 之前 PresentDue 唔出；到期先公佈（continuation 有行）
//   D 簽約金對數：公佈入 round(pay×0.3)，殺青入餘額，兩筆加埋＝合約總額分毫不差
//     （多個金額抽樣＋一單真駕駛全程）
//   E 落選路徑：公佈嗰刻先入預roll 落選效果（fame），冇 shoot、冇錢入帳
//   F 上限：等消息滿 3 張，第 4 張 doAudition 被擋（toast 講明原因、冇入 pending）
//   G 舊檔相容：冇 pendingAud 欄位載入安全；v90 舊制 shoot（冇 signedPaid）殺青全數入帳
// 反證：v90 index 冇 AUD91 函數 → 抽取即 throw → FAIL。
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
function extractFn(name){
  const i = html.indexOf('function ' + name + '(');
  if (i < 0) throw new Error('fn not found: ' + name);
  let depth = 0, j = html.indexOf('{', i);
  for (; j < html.length; j++){ if (html[j] === '{') depth++; else if (html[j] === '}'){ depth--; if (depth === 0) break; } }
  return html.slice(i, j + 1);
}
function extractConst(name){
  const i = html.indexOf('const ' + name + ' =');
  if (i < 0) throw new Error('const not found: ' + name);
  let depth = 0, started = false;
  for (let k = i; k < html.length; k++){
    const ch = html[k];
    if (ch === '{' || ch === '['){ depth++; started = true; }
    else if (ch === '}' || ch === ']'){ depth--; if (started && depth === 0) return html.slice(i, k + 1) + ';'; }
    else if (ch === ';' && !started) return html.slice(i, k + 1);
  }
  throw new Error('const end not found: ' + name);
}
let fails = 0;
function ok(name, cond, extra){
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : ''));
  if (!cond) fails++;
}

/* ---------- 沙盒（跟 verify37 段三同一套 stub 慣例） ---------- */
var window = {};
var location = { search: '' };
var localStorage = { getItem: ()=>null, setItem: ()=>{}, removeItem: ()=>{} };
function makeEl(){ return { innerHTML:'', textContent:'', style:{}, classList:{ add(){}, remove(){}, toggle(){} }, setAttribute(){}, appendChild(){}, querySelector(){ return makeEl(); }, querySelectorAll(){ return []; } }; }
var __els = {};
var document = {
  getElementById(id){ return __els[id] || (__els[id] = makeEl()); },
  querySelector(){ return makeEl(); }, querySelectorAll(){ return []; },
  createElement(){ return makeEl(); }, body: makeEl(), addEventListener(){},
};
var __modals = [], __toasts = [];
var modal = function(body, btns, opts){
  __modals.push({ body: String(body || ''), btns: btns || [], opts: opts || {} });
  const p = (btns || []).find(b => b && b.role === 'p' && typeof b.on === 'function');
  if (p){ try{ p.on(); }catch(_e){} }
};
var toast = function(m){ __toasts.push(String(m || '')); };
var saveQ = function(){}; var paintBar = function(){}; var drawMap = function(){}; var closeSheet = function(){};
var enterHome = function(){}; var runScheduleFromToday = function(){}; var goToMapForBrowse = function(){};
var openCastingNoticeDetail = function(){}; var openLoc = function(){};
var maybeShowTutToast = function(k, t, cb){ if (typeof cb === 'function') cb(); };
var softPreviewOn = function(){ return false; };
var phase3CastCopy = function(){ return { successToast: '', failToast: '', lockedTag: '', readyTag: '' }; };
var dayEndContinueButtons = function(){ return [{ label: '返回地圖', role: 'g', on: function(){} }]; };
var livingCostDayEndHint = function(){ return ''; };
var presentAudFailSettlement = function(){ return false; };
var presentRestSleepDayEnd = function(){};
var flushWeekAccelSummary = function(){};
var FREEPLAY_FW = { _pendingPostShootReward: null, postShootRewards: null };
var _weekAccel = false;
var planSelDay = 0; var planCat = 'browse'; var planDraft = null; var planBackup = null;
var EVENTS = null;
var GIGS = [];
var S = null;
var tickDay = function(){ S.dayIndex += 1; return { ended: false, summary: null }; };

eval("var START = { y:1990, m:1, d:1 };");
for (const c of ['STAT_LABEL','STAT_MAX','STRESS_MAX','EVENTS_ZH_HK','SHOOT_DAY_BY_TYPE','TRAIN_EVENTS_35','SET_CHOICES_35','MOCK_RUMOR_SEEDS','COURSE_DEFS','PLAN_ITEMS'])
  eval(extractConst(c).replace('const ' + c + ' =', 'var ' + c + ' ='));
eval(extractConst('AUD91_CAP').replace('const AUD91_CAP =', 'var AUD91_CAP ='));
eval("var _aud91Presenting = false;");
const FNS = ['R','clamp','statHardMax','apply','bumpNpc','planMeta','isGigWrapped','isGigInProduction','planCatForId','shootDeadlineHud','shootRemain','reqGap','gigActiveShoot','weekdayIdx','weekdayName','dateObj','fmtDate',
  'fillTpl','pick','eventLine','shootDayLine','formatResultNotes','shootDailyDelta','maybeUnlockMidCourses',
  'maybeTrainEvent35','setChoiceOffer35','applySetChoice35','resolvePlannedDay',
  'shootSpanFor','effectiveShootDays','effectiveShootWeekdays','effectiveShootDeadlineDays','newShootId','scheduleShoot',
  'defaultWeekPlan','lockShootsIntoDraft','placeShootOnPlan','previewShootPlacement','confirmPlaceShoot',
  'weekNumNow','stampWeekPlan37','writeTodayPlan','clearJobFromPlans',
  'shootBandFor','resolveRoleScale','shootWeekdayOk','shootWeekdaySet0','isFreePlanSlot','isMapDay','isRecordGig','shootWeekdayLabel','gigScheduleVerb','displayDateObj','isCriticalPlanDay','planDayWouldWrap','enrollCourse','fameFloor','canAudition','chance','rollAuditionPay','chanceVarianceNote','payContractNote','doAudition',
  'aud91Ensure','aud91PendingOf','aud91WaitDays','aud91WaitPhrase','aud91CreatePending','aud91LogPush','aud91DueList','aud91PendingHint','aud91PresentDue','aud91PresentOne','payWrapNote','shootPendingLine38',
  /* v20a202：resolvePlannedDay 而家靠呢啲 helper 出去向行＋dismiss 提示 */
  'esc202','nextDayLabel202','dayEndNextLine202','dayEndDismissNote202','storyResultDestLine202'];
/* v20a112 ICONS112：被抽函數調用 iconHtml112，沙盒要一併載入對照＋helper。 */
eval(extractConst('EMOJI_ICON112').replace('const EMOJI_ICON112 =', 'var EMOJI_ICON112 ='));
eval(extractFn('iconHtml112'));
eval(extractFn('favDots112'));
for (const f of FNS) eval(extractFn(f));
ok('harness: AUD91 函數全載入', typeof aud91CreatePending === 'function' && typeof aud91PresentDue === 'function' && typeof doAudition === 'function');

function baseSave(over){
  return Object.assign({
    dayIndex: 30, fame: 17, popularity: 10, acting: 50, stage: 30, vocal: 20, looks: 30, iq: 30, charm: 20,
    stress: 12, money: 5000, stamina: 80, industryCreditDelta: 0,
    flags: {}, npcs: { colleague: 8, director: 4, stylist: 5, rival: 6, reporter: 3, agent: 12 },
    board: {}, booked: [], shoots: [], pendingAud: [], aud91Log: [],
    weekPlan: ['rest','rest','rest','rest','rest','rest','rest'],
    weekGigsDone: 0, weekTrainDone: 0, trainCount: {}, mockRumors: [], story: { gigCount: 0, flags: {}, done: {} },
  }, over || {});
}
function mkGig(over){
  return Object.assign({
    id: 'a91_gig', title: '《測試片》配角', workTitle: '測試片', roleLabel: '配角', type: '電視劇', loc: 'tvb_longmen',
    req: {}, pay: [900, 900], payExact: 900, fame: [5, 5], popularity: [17, 17], hard: 0.1, tier: '初',
    shootDaysHint: 3, shootBand: [3, 3], shootWeekdays: [1, 2, 3, 4, 5, 6], shootDeadlineDays: 12,
    limits: { gender: 'any', licenses: [], groupOnly: false, notes: [] },
  }, over || {});
}
const L91 = { id: 'tvb_longmen', name: '星河電視台' };

/* ---------- A 等待帶 ---------- */
(function(){
  S = baseSave();
  const band = (gig, days) => { const s = new Set(); for (let i = 0; i < 300; i++) s.add(aud91WaitDays(gig, days)); return [...s].sort(); };
  ok('A 入門（entryTier）帶 1–2 日', JSON.stringify(band(mkGig({ entryTier: true }), 1)) === '[1,2]');
  ok('A 初級短工（tier 初・1 日）帶 1–2 日', JSON.stringify(band(mkGig({}), 1)) === '[1,2]');
  ok('A 一般製作（tier 中・5 日）帶 2–3 日', JSON.stringify(band(mkGig({ tier: '中' }), 5)) === '[2,3]');
  ok('A 初級長工（tier 初・6 日）帶 2–3 日', JSON.stringify(band(mkGig({}), 6)) === '[2,3]');
  ok('A 高級（tier 高）帶 3–4 日', JSON.stringify(band(mkGig({ tier: '高' }), 5)) === '[3,4]');
  ok('A 大製作（tier 中・12 日）帶 3–4 日', JSON.stringify(band(mkGig({ tier: '中' }), 12)) === '[3,4]');
  ok('A 上限係 3 張', AUD91_CAP === 3);
})();

/* ---------- B 狀態機＋重載不變 ---------- */
(function(){
  S = baseSave(); const gig = mkGig({}); GIGS = [gig]; S.board = { tvb_longmen: [gig.id] };
  const realRandom = Math.random;
  Math.random = () => 0.05; /* 必獲聘 */
  __modals = [];
  doAudition(gig, L91);
  Math.random = realRandom;
  const body = __modals.map(m => m.body).join('\n');
  ok('B 試鏡當日只講等消息（冇揭曉）', body.indexOf('等消息') >= 0 && body.indexOf('獲聘！') < 0 && body.indexOf('未獲錄用') < 0);
  ok('B pending 已寫入（ok 定死・片酬定死・公佈日＝試鏡日＋等待）',
    (S.pendingAud || []).length === 1 && S.pendingAud[0].ok === true && S.pendingAud[0].pay === 900 &&
    S.pendingAud[0].revealDay === S.pendingAud[0].audDay + S.pendingAud[0].wait);
  ok('B 試鏡當日冇 shoot／冇入錢／聲望冇郁', (S.shoots || []).length === 0 && S.money === 5000 && S.fame === 17);
  ok('B 板面已剔除嗰張', (S.board.tvb_longmen || []).indexOf(gig.id) < 0);
  const snap = JSON.stringify(S.pendingAud[0]);
  const reloaded = JSON.parse(JSON.stringify(S));
  ok('B 存檔 JSON 來回後成單不變（結果／片酬／公佈日）', JSON.stringify(reloaded.pendingAud[0]) === snap);
  S = reloaded; GIGS = [gig];
  ok('B 重載後 PresentDue 未到期唔出', aud91DueList().length === 0 && aud91PresentDue(() => {}) === false);
})();

/* ---------- C＋D 公佈＋簽約金全程 ---------- */
(function(){
  S = baseSave(); const gig = mkGig({}); GIGS = [gig]; S.board = { tvb_longmen: [gig.id] };
  const realRandom = Math.random;
  Math.random = () => 0.05;
  doAudition(gig, L91);
  const rec = S.pendingAud[0];
  S.dayIndex = rec.revealDay - 1;
  ok('C 公佈日前一日 PresentDue 唔出', aud91PresentDue(() => {}) === false && (S.pendingAud || []).length === 1);
  S.dayIndex = rec.revealDay;
  __modals = [];
  let cont = false;
  const presented = aud91PresentDue(() => { cont = true; });
  Math.random = realRandom;
  const body = __modals.map(m => m.body).join('\n');
  ok('C 到期公佈（呈現有行・continuation 有行・pending 清空）', presented === true && cont === true && (S.pendingAud || []).length === 0);
  ok('D 公佈對話講明簽約金＋餘額', body.indexOf('簽約金') >= 0 && body.indexOf('餘額') >= 0);
  ok('D 簽約金 270 已入帳', S.money === 5270);
  const shoot = (S.shoots || [])[0];
  ok('D shoot 已排（signedPaid=270・hiredAtDay=公佈日）', !!shoot && shoot.signedPaid === 270 && shoot.hiredAtDay === rec.revealDay);
  if (shoot){
    S.weekPlan = ['shoot:' + shoot.id, 'shoot:' + shoot.id, 'shoot:' + shoot.id, 'rest', 'rest', 'rest', 'rest'];
    resolvePlannedDay('shoot:' + shoot.id);
    resolvePlannedDay('shoot:' + shoot.id);
    ok('D 拍攝中段未入餘額', S.money === 5270);
    resolvePlannedDay('shoot:' + shoot.id);
    ok('D 殺青入餘額 630（270＋630＝900 分毫不差）', S.money === 5900 && (S.shoots || []).length === 0);
  }
  /* 金額抽樣：簽約金＋餘額＝總額（純算式多點抽樣） */
  let sumOk = true;
  for (const pay of [100, 450, 900, 1234, 333, 10000, 7, 99999]){
    const sign = Math.round(pay * 0.3);
    if (sign + Math.max(0, pay - sign) !== pay) sumOk = false;
  }
  ok('D 多金額抽樣：簽約金＋餘額＝總額', sumOk);
  /* payWrapNote／shootPendingLine38 對新舊制嘅講法 */
  ok('D 殺青附註（新制）講明餘額＋總額', payWrapNote({ pay: 900, signedPaid: 270 }).indexOf('餘額 $630') >= 0 && payWrapNote({ pay: 900, signedPaid: 270 }).indexOf('合約總額 $900') >= 0);
  ok('D 手帳拍攝中行（新制）分開簽約金／餘額', shootPendingLine38({ pay: 900, signedPaid: 270, fame: 5, popularity: 17 }).indexOf('餘額 $630') >= 0);
})();

/* ---------- E 落選路徑 ---------- */
(function(){
  S = baseSave(); const gig = mkGig({ id: 'a91_fail' }); GIGS = [gig]; S.board = { tvb_longmen: [gig.id] };
  const realRandom = Math.random;
  Math.random = () => 0.99; /* 必落選 */
  doAudition(gig, L91);
  Math.random = realRandom;
  const rec = (S.pendingAud || [])[0];
  ok('E 落選都係試鏡刻定死（ok=false・落選效果已預roll）', !!rec && rec.ok === false && rec.fxFame < 0);
  ok('E 試鏡當日落選效果未入帳（fame 仍 17）', S.fame === 17);
  S.dayIndex = rec.revealDay;
  __modals = [];
  aud91PresentDue(() => {});
  const body = __modals.map(m => m.body).join('\n');
  ok('E 公佈先揭曉落選（何生來電）', body.indexOf('何生來電') >= 0 || body.indexOf('未獲錄用') >= 0);
  ok('E 落選效果公佈嗰刻入帳（fame 17→' + (17 + rec.fxFame) + '）', S.fame === 17 + rec.fxFame);
  ok('E 落選冇 shoot／冇錢入帳', (S.shoots || []).length === 0 && S.money === 5000);
})();

/* ---------- F 上限 ---------- */
(function(){
  S = baseSave(); GIGS = [mkGig({})];
  for (let i = 0; i < 3; i++)
    aud91CreatePending(mkGig({ id: 'a91_cap_' + i }), L91, { ok: true, p: 0.5, days: 3, payRoll: { pay: 500, basePay: 500, bonusPay: 0, bonusLabel: '', note: '' }, fame: 3, pop: 4, via: 'board' });
  ok('F 已有 3 張等消息', (S.pendingAud || []).length === 3);
  const gig4 = mkGig({ id: 'a91_cap_4' }); GIGS = [gig4]; S.board = { tvb_longmen: [gig4.id] };
  __toasts = []; __modals = [];
  doAudition(gig4, L91);
  ok('F 第 4 張被擋（冇入 pending）', (S.pendingAud || []).length === 3 && !aud91PendingOf('a91_cap_4'));
  ok('F 擋嗰陣有講明原因（等消息已滿 3 張）', __toasts.join(' ').indexOf('3 張通告等緊消息') >= 0);
  ok('F 被擋唔耗日（dayIndex 冇郁）', S.dayIndex === 30);
})();

/* ---------- G 舊檔相容 ---------- */
(function(){
  S = baseSave(); delete S.pendingAud; delete S.aud91Log; /* 扮 v90 舊檔：冇呢兩欄 */
  let threw = false, len = -1;
  try{ len = aud91Ensure().length; }catch(_e){ threw = true; }
  ok('G 舊檔冇 pendingAud 欄位 → 安全預設空陣列', !threw && len === 0 && Array.isArray(S.pendingAud) && Array.isArray(S.aud91Log));
  /* v90 舊制 shoot：scheduleShoot 直開（冇 signedPaid）→ 殺青全數入帳 */
  S = baseSave(); const gig = mkGig({ id: 'a91_old' }); GIGS = [gig];
  const shoot = scheduleShoot(gig, 900, 5, 17, { basePay: 900, bonusPay: 0, bonusLabel: '' });
  ok('G 舊制 shoot 冇 signedPaid 欄位', shoot.signedPaid == null);
  S.weekPlan = ['shoot:' + shoot.id, 'shoot:' + shoot.id, 'shoot:' + shoot.id, 'rest', 'rest', 'rest', 'rest'];
  resolvePlannedDay('shoot:' + shoot.id);
  resolvePlannedDay('shoot:' + shoot.id);
  resolvePlannedDay('shoot:' + shoot.id);
  ok('G 舊制殺青全數 900 入帳（冇簽約金補發／冇扣減）', S.money === 5900);
  ok('G 殺青附註（舊制）維持原句', payWrapNote({ pay: 900 }).indexOf('獲聘時合約鎖定額') >= 0);
})();

console.log('\nAUD91 LOGIC: ' + (fails ? fails + ' FAIL' : 'ALL PASS'));
process.exit(fails ? 1 : 0);
