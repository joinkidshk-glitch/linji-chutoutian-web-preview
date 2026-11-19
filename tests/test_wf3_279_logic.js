// v20a279 G-L2 還原收割鏈邏輯測試：ENC79 Beat 3 搶鏡抉擇 → 記仇債 → 14 日後開收割窗 →
//   收割通告殺青清債＋計 settled＋授喜劇組債權 → film_202 兌現＋redeemedBy；過期壞帳照 Q13。
// 用法：node tests/test_wf3_279_logic.js [path-to-index.html]
// 反證：喺 v20a278 index 上行 → Beat 3／收割窗／授債權斷言乾淨 FAIL（liaoChoice 0 命中、grudgeDue 永遠無人設）。
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const GIGS_NEW = require('../content/gigs_new.json');
const GIGS_ARR = Array.isArray(GIGS_NEW) ? GIGS_NEW : (GIGS_NEW.gigs || []);
const gigById = (id)=> GIGS_ARR.find(g=>g && g.id===id) || null;
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
function extractConst(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('const not found: ' + name);
  let depth = 0, started = false, j = i;
  for(; j < html.length; j++){
    const c = html[j];
    if(c === '{' || c === '['){ depth++; started = true; }
    else if(c === '}' || c === ']'){ depth--; if(started && depth === 0){ j++; break; } }
    else if(c === ';' && !started){ j++; break; }
  }
  return html.slice(i, j);
}
function extractDlg(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('missing ' + name);
  const j = html.indexOf('\nconst ', i + 10);
  return html.slice(i, j < 0 ? undefined : j);
}

/* ---------- stubs ---------- */
let S = null;
let _ys = { year: 1991, season: '秋' };
let _season = '秋';
let _doneNodes = new Set();
let _storyFlags = {};
let _toasts = [];
let _enqueued = [];
let _settled = [];
let _granted79 = [];
function resetS(day){
  S = { dayIndex: day || 0, fame: 0, money: 2000, industryCredit: 10,
    mockRumors: [], mockCredits: [], mockDebts: [], wrapHistory: [], flags: {},
    stars: {}, story: { done: {}, flags: {} }, news82: { pub: {}, arc: {} } };
  _doneNodes = new Set(); _storyFlags = {};
  _toasts = []; _enqueued = []; _settled = []; _granted79 = [];
}
function saveQ(){}
function syncNotebookMirror(){}
function syncDualTracks(){}
function toast(m, o){ _toasts.push(String(m || '') + ' ' + String((o && o.sub) || '')); }
function enqueueNewspaperItem(item){ _enqueued.push(item); return item; }
function ensureFavorLedger(){ return { settled: 0, credits: 0, exodus: [], counted: {} }; }
function favorLedgerNoteCredit(){}
function favorLedgerNoteSettled(id, source){ _settled.push(id + '|' + source); return source !== 'wf3_harvest_expired'; }
function calendarSeason(){ return _season; }
function yearSeasonNow(){ return _ys; }
function enc79BoardHasStar(){ return true; }
function enc79TierOf(fav){ return fav >= 70 ? 4 : fav >= 45 ? 3 : fav >= 25 ? 2 : fav >= 10 ? 1 : 0; }
function enc79StarState(id){ if(!S.stars[id]) S.stars[id] = { fav: 0, beatsDone: {}, met: false }; return S.stars[id]; }
function enc79GrantCredit(c){ _granted79.push(c.id); S.mockCredits.push(Object.assign({}, c)); }
function boardSortCompare(){ return 0; } /* 板面排序沙盒樁（本測試只驗收割通告在唔在板） */
function isGigConsumed(){ return false; } /* 板面沙盒樁 */
const StoryOC = {
  ensure(){},
  isDone(id){ return _doneNodes.has(id); },
  getFlag(f){ return !!_storyFlags[f]; },
  setFlag(f, v){ _storyFlags[f] = v; }
};
function setFav(sid, n){ const st = enc79StarState(sid); st.fav = n; st.met = true; return st; }
function beatOf(sid, id){ return (ENC79_BEATS[sid] || []).find(b => b.id === id); }
var GIGS = GIGS_ARR;
var BR89_GIGS = []; /* br89OnGigComplete 讀 BR89_GIGS 反查標題（已清空，實測只係 fallback 到 GIGS） */

const asVar = (code, name)=> code.replace('const ' + name + ' =', 'var ' + name + ' =');
eval(asVar(extractConst('ENC79_BEATS'), 'ENC79_BEATS') + '\n'
  + asVar(extractDlg('ENC79_DLG_liu_bingxing'), 'ENC79_DLG_liu_bingxing') + '\n'
  + asVar(extractConst('BR89_PATRON_OF_GIG'), 'BR89_PATRON_OF_GIG') + '\n'
  + asVar(extractConst('GIG_SEASON_SPAN88'), 'GIG_SEASON_SPAN88') + '\n'
  + ['enc79BeatOpen', 'enc79PickBeat', 'enc79ChoiceFx', 'enc79RunChoiceFx', 'enc83NodeDone',
     'ensureWf3', 'wf3GrantCredit', 'wf3SettleTick',
     'triggerGigOn', 'br89HasCredit', 'br89GigOn', 'br89OnGigComplete', 'gigsForLocSeasonBoard',
     'seasonRank', 'gigSeasonEarlyVisible88', 'gigSeasonHidden88'].map(extractFn).join('\n'));

const HARVEST_ID = 'gig_1991_film_214';
const harvestGig = gigById(HARVEST_ID);
const film202 = gigById('gig_1992_film_202');

/* ---------- 1. 收割通告靜態 ---------- */
ok('收割通告在庫：gig_1991_film_214《笑住過肥年》夜景補拍', !!harvestGig && harvestGig.title === '《笑住過肥年》夜景補拍');
ok('收割通告：1991 秋／臨記／補拍通告／1 日／紅棉影業', !!harvestGig && harvestGig.year === 1991 && harvestGig.season === '秋'
  && harvestGig.tier === '臨記' && harvestGig.category === '補拍通告' && harvestGig.days === 1 && harvestGig.loc === 'film_cotton');
ok('收割通告 trigger kind wf3harvest（唔係舊 gig_wf3_ id）', !!harvestGig && harvestGig.trigger && harvestGig.trigger.kind === 'wf3harvest');
ok('收割通告 cast 係《笑住過肥年》班底（廖主演）', !!harvestGig && harvestGig.cast && harvestGig.cast.leadM === 'liu_bingxing' && harvestGig.cast.leadF === 'wu_meilam');

/* ---------- 2. Beat 3 對白＋註冊表 ---------- */
const stealBeat = ENC79_DLG_liu_bingxing.beats.liu_steal;
ok('DLG liu_steal 在位：兩選項（照劇本演／搏一搏搶鏡）', !!stealBeat && (stealBeat.choices || []).length === 2
  && stealBeat.choices[0].label === '照劇本演，企返自己個位' && stealBeat.choices[1].label === '搏一搏，自己加戲搶鏡');
ok('DLG liu_steal 選項帶旗 enc79_liu_steady／enc79_liu_steal', !!stealBeat
  && JSON.stringify(stealBeat.choices[0].flags) === '["enc79_liu_steady"]'
  && JSON.stringify(stealBeat.choices[1].flags) === '["enc79_liu_steal"]');
ok('DLG 次序：liu_steal 喺 liu_tease 之後、liu_repay 之前', (()=>{ const ks = Object.keys(ENC79_DLG_liu_bingxing.beats); return ks.indexOf('liu_steal') === ks.indexOf('liu_tease') + 1 && ks.indexOf('liu_steal') === ks.indexOf('liu_repay') - 1; })());
ok('註冊表次序：liu_steal 喺 liu_tease 之後、liu_repay 之前', (()=>{ const ids = (ENC79_BEATS.liu_bingxing || []).map(b => b.id); return ids.indexOf('liu_steal') === ids.indexOf('liu_tease') + 1 && ids.indexOf('liu_steal') === ids.indexOf('liu_repay') - 1; })());
ok('對白無黑名單詞（站隊／排工／派工／忠誠帳／人情帳／識分寸／收科／係帳）', (()=>{ const txt = JSON.stringify(stealBeat); return !['站隊', '排工', '派工', '忠誠帳', '人情帳', '識分寸', '收科', '係帳', '認橋'].some(w => txt.indexOf(w) >= 0); })());

/* ---------- 3. ChoiceFx＋RunChoiceFx ---------- */
ok('fx 搶鏡：fav 1／fx liu_steal', (()=>{ const r = enc79ChoiceFx('beat:liu_steal', '搏一搏，自己加戲搶鏡'); return r.fav === 1 && r.fx === 'liu_steal'; })());
ok('fx 照劇本演：fav 2／fx liu_steady', (()=>{ const r = enc79ChoiceFx('beat:liu_steal', '照劇本演，企返自己個位'); return r.fav === 2 && r.fx === 'liu_steady'; })());
ok('fx 落旗：liu_steal → liaoChoice=steal', (()=>{ resetS(600); enc79RunChoiceFx('liu_steal'); return S.wf3 && S.wf3.liaoChoice === 'steal'; })());
ok('fx 落旗：liu_steady → liaoChoice=steady', (()=>{ resetS(600); enc79RunChoiceFx('liu_steady'); return S.wf3 && S.wf3.liaoChoice === 'steady'; })());

/* ---------- 4. Beat 閘門 ---------- */
function liuSetup(year, season, fav, doneBeats){
  resetS(600); _ys = { year, season }; _doneNodes = new Set(['N9']);
  const st = setFav('liu_bingxing', fav);
  (doneBeats || []).forEach(id => { st.beatsDone[id] = 1; });
  return st;
}
ok('閘：1991 秋 T2＋N9＋前三 beat 已播 → PickBeat 係 liu_steal', (()=>{ liuSetup(1991, '秋', 30, ['liu_foreshadow', 'liu_intel', 'liu_tease']); return enc79PickBeat('liu_bingxing') && enc79PickBeat('liu_bingxing').id === 'liu_steal'; })());
ok('閘：問過一次（liaoChoice）→ 唔再開，行 liu_repay', (()=>{ liuSetup(1991, '秋', 30, ['liu_foreshadow', 'liu_intel', 'liu_tease']); enc79RunChoiceFx('liu_steal'); return enc79PickBeat('liu_bingxing') && enc79PickBeat('liu_bingxing').id === 'liu_repay'; })());
ok('閘：1991 冬（未問過）→ 搶鏡閘口已關，行 liu_repay', (()=>{ liuSetup(1991, '冬', 30, ['liu_foreshadow', 'liu_intel', 'liu_tease']); return enc79PickBeat('liu_bingxing') && enc79PickBeat('liu_bingxing').id === 'liu_repay'; })());
ok('閘：1990 → 唔開搶鏡', (()=>{ liuSetup(1990, '秋', 30, ['liu_foreshadow', 'liu_intel', 'liu_tease']); return enc79BeatOpen('liu_bingxing', beatOf('liu_bingxing', 'liu_steal')) === false; })());
ok('閘：T1（fav 20）→ 唔開搶鏡', (()=>{ liuSetup(1991, '秋', 20, ['liu_foreshadow', 'liu_intel', 'liu_tease']); return enc79BeatOpen('liu_bingxing', beatOf('liu_bingxing', 'liu_steal')) === false; })());

/* ---------- 5. 搶鏡全鏈：抉擇 → 記債 → 到期 → 收割窗開 → 殺青授債權 → film_202 兌現 ---------- */
resetS(600); _ys = { year: 1991, season: '秋' }; _season = '秋';
enc79RunChoiceFx('liu_steal');
ok('鏈：揀搶鏡 → liaoChoice=steal', S.wf3 && S.wf3.liaoChoice === 'steal');
wf3SettleTick();
ok('鏈：翌日 tick 結算 → 片酬 +$800', S.money === 2800);
ok('鏈：翌日 tick 結算 → 記面子債＋dueDay+14', S.mockDebts.some(d => d.id === 'debt_wf3_liao_grudge' && d.creditor === '廖炳星一方' && d.status === '未到期' && d.dueDay === 614) && S.wf3.grudgeDue === 614);
ok('鏈：翌日 tick 結算 → 報紙內訌角度入隊（聽朝刊）', _enqueued.some(e => e.eventKey === 'wf3:liao_steal' && e.publishDay === 601));
ok('鏈：結算冪等（重複 tick 唔重記債／唔重加錢）', (()=>{ wf3SettleTick(); return S.money === 2800 && S.mockDebts.filter(d => d.id === 'debt_wf3_liao_grudge').length === 1; })());
S.dayIndex = 613; wf3SettleTick();
ok('鏈：到期前一日（613）收割窗唔開', !S.wf3.liaoHarvest);
ok('鏈：到期前收割通告唔開（trigger 唔成立）', triggerGigOn(harvestGig) === false);
S.dayIndex = 614; wf3SettleTick();
ok('鏈：到期日（614）收割窗開（gigDay 614／window 7）', S.wf3.liaoHarvest && S.wf3.liaoHarvest.gigDay === 614 && S.wf3.liaoHarvest.window === 7);
ok('鏈：開窗 toast 講明夜景補拍＋7 日', _toasts.join(' ').indexOf('夜景補拍') >= 0 && _toasts.join(' ').indexOf('7 日') >= 0);
ok('鏈：窗內收割通告開（trigger 成立）', triggerGigOn(harvestGig) === true);
S.dayIndex = 621;
ok('鏈：窗尾日（gigDay+7）收割通告照開', triggerGigOn(harvestGig) === true);
S.dayIndex = 622;
ok('鏈：窗外（gigDay+8）收割通告唔開', triggerGigOn(harvestGig) === false);
S.dayIndex = 617;
S.wrapHistory.push({ gigId: HARVEST_ID, wrappedDay: 616 });
wf3SettleTick();
ok('鏈：收割殺青 → 債清咗', !S.mockDebts.some(d => d.id === 'debt_wf3_liao_grudge'));
ok('鏈：收割殺青 → 計 settled（wf3_harvest 真還清）', _settled.indexOf('debt_wf3_liao_grudge|wf3_harvest') >= 0);
ok('鏈：收割殺青 → 授喜劇組債權 credit_wf3_comedy_crew', S.mockCredits.some(c => c.id === 'credit_wf3_comedy_crew' && c.debtor === '喜劇組場務'));
ok('鏈：收割殺青 → liaoHarvestDone＝1', S.wf3.liaoHarvestDone === 1);
ok('鏈：授債權冪等（重複 tick 唔重授）', (()=>{ wf3SettleTick(); return S.mockCredits.filter(c => c.id === 'credit_wf3_comedy_crew').length === 1; })());
ok('鏈：收割完成唔標 redeemedBy（兌現留返 film_202）', !S.mockCredits.some(c => c.id === 'credit_wf3_comedy_crew' && c.redeemedBy));
ok('鏈：持新債權 → film_202《笑到最後》開（兌現通告）', triggerGigOn(film202) === true);
ok('鏈：film_202 經 BR89 map（第 14 對）', BR89_PATRON_OF_GIG['gig_1992_film_202'] === 'credit_wf3_comedy_crew');
br89OnGigComplete('gig_1992_film_202');
ok('鏈：film_202 殺青 → 債權標 redeemedBy', S.mockCredits.some(c => c.id === 'credit_wf3_comedy_crew' && c.redeemedBy === 'gig_1992_film_202'));
ok('鏈：兌現後 film_202 落板（唔重開）', triggerGigOn(film202) === false);

/* ---------- 5b. 板面：收割窗通告豁免季節閘（窗開喺冬都照上板） ---------- */
ok('板：收割通告季節係秋（stagger 有實季）', harvestGig.season === '秋');
ok('板：秋通告喺冬原本俾季節閘藏起', gigSeasonHidden88(harvestGig, '冬') === true);
ok('板：窗開喺冬（day 699）→ 紅棉板照見收割通告', (()=>{ resetS(699); _season = '冬'; S.wf3 = { liaoHarvest: { gigDay: 699, window: 7 } }; const pool = gigsForLocSeasonBoard('film_cotton', '冬'); return pool.some(g => g.id === HARVEST_ID); })());
ok('板：窗未開（無 liaoHarvest）→ 紅棉板唔見收割通告', (()=>{ resetS(699); _season = '冬'; const pool = gigsForLocSeasonBoard('film_cotton', '冬'); return !pool.some(g => g.id === HARVEST_ID); })());
ok('板：窗外（day 710）→ 紅棉板唔見收割通告', (()=>{ resetS(710); _season = '冬'; S.wf3 = { liaoHarvest: { gigDay: 699, window: 7 } }; const pool = gigsForLocSeasonBoard('film_cotton', '冬'); return !pool.some(g => g.id === HARVEST_ID); })());

/* ---------- 6. 照劇本演：報紙好評、冇債 ---------- */
resetS(600); _ys = { year: 1991, season: '秋' }; _season = '秋';
enc79RunChoiceFx('liu_steady');
wf3SettleTick();
ok('穩陣：信用 +2（delta，v20a338；真 sync 落袋由 test_r338 驗）', Number(S.industryCreditDelta) === 2);
ok('穩陣：報紙好評角度入隊（聽朝刊）', _enqueued.some(e => e.eventKey === 'wf3:liao_steady' && e.publishDay === 601));
ok('穩陣：冇債、冇 grudgeDue、唔開收割窗', S.mockDebts.length === 0 && !S.wf3.grudgeDue && !S.wf3.liaoHarvest);
ok('穩陣：收割通告唔開', triggerGigOn(harvestGig) === false);

/* ---------- 7. 過期壞帳（Q13／R3：唔計 settled，信用 −2） ---------- */
resetS(600); _ys = { year: 1991, season: '秋' }; _season = '秋';
S.wf3 = { liaoChoice: 'steal', liaoSettled: 1, grudgeDue: 614, liaoHarvest: { gigDay: 614, window: 7 } };
S.mockDebts = [{ id: 'debt_wf3_liao_grudge' }];
const deltaBefore = Number(S.industryCreditDelta)||0;
S.dayIndex = 622; wf3SettleTick();
ok('過期：債銷＋信用 −2（delta，v20a338）＋標 expired', !S.mockDebts.some(d => d.id === 'debt_wf3_liao_grudge') && Number(S.industryCreditDelta) === deltaBefore - 2 && S.wf3.liaoHarvestExpired === 1);
ok('過期：唔授喜劇組債權', !S.mockCredits.some(c => c.id === 'credit_wf3_comedy_crew'));
ok('過期：唔計 settled（壞帳，唔入帳本）', _settled.length === 0);
ok('過期：遲做收割通告都唔開（窗已關）', triggerGigOn(harvestGig) === false);

if(fails.length){ console.log('FAILURES: ' + fails.length); process.exit(1); }
console.log('ALL PASS');
