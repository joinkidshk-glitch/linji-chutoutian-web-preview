// v20a338 wf3SettleTick 信用 delta 修復測試：steady 結算 +2／收割過期 −2 之前直接寫
//   S.industryCredit 鏡像欄，緊接 syncDualTracks 將鏡像覆寫做派生值（baseCredit+delta），
//   兩筆數永遠落唔到袋（v287 實駕 steady 48→48）。今版改寫 industryCreditDelta。
// 本測試用「真」dualTrackNumbers/readDualTracks/syncDualTracks（唔 stub），證明數真係落袋。
// 用法：node tests/test_r338_wf3_credit_delta.js [path-to-index.html]
// 反證：喺 v337 index 上行 → A1／B1 乾淨 FAIL（delta 唔郁、鏡像唔郁）。
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond, extra){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name + (extra ? ' :: ' + extra : '')); }
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

/* ---------- stubs ---------- */
let S = null;
let _toasts = [], _enqueued = [], _settled = [];
let _storyFlags = {}, _doneNodes = new Set();
function resetS(day){
  /* fame 20 → baseCredit = round(20*0.5) = 10；鏡像起始 10、delta 0，兩者一致。 */
  S = { dayIndex: day || 0, fame: 20, stage: 0, acting: 0, stress: 0, money: 2000,
    industryCredit: 10, industryCreditDelta: 0, stageVolume: 20,
    mockRumors: [], mockCredits: [], mockDebts: [], wrapHistory: [], flags: {},
    stars: {}, story: { done: {}, flags: {} }, news82: { pub: {}, arc: {} } };
  _toasts = []; _enqueued = []; _settled = []; _storyFlags = {}; _doneNodes = new Set();
}
function saveQ(){}
function syncNotebookMirror(){}
function toast(m, o){ _toasts.push(String(m || '') + ' ' + String((o && o.sub) || '')); }
function enqueueNewspaperItem(item){ _enqueued.push(item); return item; }
function ensureFavorLedger(){ return { settled: 0, credits: 0, exodus: [], counted: {} }; }
function favorLedgerNoteCredit(){}
function favorLedgerNoteSettled(id, source){ _settled.push(id + '|' + source); return source !== 'wf3_harvest_expired'; }
function calendarSeason(){ return '秋'; }
const StoryOC = {
  ensure(){},
  isDone(id){ return _doneNodes.has(id); },
  getFlag(f){ return !!_storyFlags[f]; },
  setFlag(f, v){ _storyFlags[f] = v; }
};

eval(['dualTrackNumbers', 'readDualTracks', 'syncDualTracks',
  'ensureWf3', 'wf3GrantCredit', 'wf3SettleTick'].map(extractFn).join('\n'));

/* ---------- A. steady 結算 +2 真落袋 ---------- */
resetS(600);
S.wf3 = { liaoChoice: 'steady' };
wf3SettleTick();
ok('A1 steady：industryCreditDelta +2', Number(S.industryCreditDelta) === 2, 'delta=' + S.industryCreditDelta);
ok('A1 steady：sync 後鏡像 industryCredit 真係 10→12', S.industryCredit === 12, 'mirror=' + S.industryCredit);
ok('A1 steady：liaoSettled 落記＋報紙好評入隊', S.wf3.liaoSettled === 1 && _enqueued.some(e => e.eventKey === 'wf3:liao_steady' && e.publishDay === 601));
ok('A1 steady：toast 講行內信用 +2（文案不變）', _toasts.join(' ').indexOf('行內信用 +2') >= 0);
ok('A2 steady 冪等：重複 tick delta／鏡像唔重複派', (()=>{ wf3SettleTick(); return Number(S.industryCreditDelta) === 2 && S.industryCredit === 12; })());

/* ---------- B. 收割過期 −2 真落袋 ---------- */
resetS(600);
S.wf3 = { liaoChoice: 'steal', liaoSettled: 1, grudgeDue: 614, liaoHarvest: { gigDay: 614, window: 7 } };
S.mockDebts = [{ id: 'debt_wf3_liao_grudge' }];
S.dayIndex = 622; wf3SettleTick();
ok('B1 過期：industryCreditDelta −2', Number(S.industryCreditDelta) === -2, 'delta=' + S.industryCreditDelta);
ok('B1 過期：sync 後鏡像 industryCredit 真係 10→8', S.industryCredit === 8, 'mirror=' + S.industryCredit);
ok('B1 過期：債銷＋標 expired＋唔計 settled＋唔授債權',
  !S.mockDebts.some(d => d.id === 'debt_wf3_liao_grudge') && S.wf3.liaoHarvestExpired === 1
  && _settled.length === 0 && !S.mockCredits.some(c => c.id === 'credit_wf3_comedy_crew'));
ok('B1 過期：toast 講行內信用 −2（文案不變）', _toasts.join(' ').indexOf('行內信用 −2') >= 0);
ok('B2 過期冪等：重複 tick delta 唔重複扣', (()=>{ wf3SettleTick(); return Number(S.industryCreditDelta) === -2 && S.industryCredit === 8; })());

/* ---------- C. steal 分支不變（+$800，信用唔郁） ---------- */
resetS(600);
S.wf3 = { liaoChoice: 'steal' };
wf3SettleTick();
ok('C1 steal：片酬 +$800 照舊', S.money === 2800);
ok('C1 steal：delta／鏡像唔郁（信用唔關事）', Number(S.industryCreditDelta) === 0 && S.industryCredit === 10);
ok('C1 steal：記面子債 dueDay+14 照舊', S.mockDebts.some(d => d.id === 'debt_wf3_liao_grudge' && d.dueDay === 614));

/* ---------- D. 靜態：舊直寫鏡像字串清零、新 delta 寫法在位、全檔掃描 ---------- */
const tick = extractFn('wf3SettleTick');
ok('D1 舊直寫 +2 字串已刪', !html.includes('S.industryCredit = Math.max(0, (Number(S.industryCredit)||0) + 2);'));
ok('D2 舊直寫 −2 字串已刪', !html.includes('S.industryCredit = Math.max(0, (Number(S.industryCredit)||0) - 2);'));
ok('D3 steady 分支改寫 delta +2', tick.includes('S.industryCreditDelta = (Number(S.industryCreditDelta)||0) + 2;'));
ok('D4 過期分支改寫 delta −2', tick.includes('S.industryCreditDelta = (Number(S.industryCreditDelta)||0) - 2;'));
ok('D5 全檔無 S.industryCredit 直寫（=／+=／−=，syncDualTracks 用 s. 參數唔計）',
  !/S\.industryCredit\s*=(?!=)/.test(html) && !/S\.industryCredit\s*\+=/.test(html) && !/S\.industryCredit\s*-=/.test(html));
ok('D6 statsApplied 路徑照舊寫 delta（L8427 冇郁）',
  html.includes('S.industryCreditDelta = (Number(S.industryCreditDelta)||0) + Number(statsApplied.industryCredit);'));

if(fails.length){ console.log('FAILURES: ' + fails.length); process.exit(1); }
console.log('ALL PASS');
