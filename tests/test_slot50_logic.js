// v20a50 存檔槽顯示診斷守護測試：首次載入槽位顯示不一致——查證後根因假設唔成立，
// 本測試鎖死三項已驗證事實，防日後改版真係引入「渲染／遷移時序」問題：
//   (1) 槽位摘要（週／存款／聲望）對 normalizeSaveObj 遷移係不變量；
//   (2) loadFromSlot 只喺記憶體遷移，唔寫回 localStorage；
//   (3) loadPrefs 一次性遷移（familySafeContent false→null）只寫 prefs 一次、唔掂存檔 key、唔改 activeSlot。
// 用法：node tests/test_slot50_logic.js [path-to-index.html]
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
function extractConst(name){
  const m = html.match(new RegExp('const '+name+'\\s*=\\s*[^;]+;'));
  if(!m) throw new Error('const not found: '+name);
  return m[0].replace(/^const\s+/, 'globalThis.');
}

/* ---- localStorage stub（記錄所有寫入） ---- */
let store = {};
let writeLog = [];
const localStorage = {
  getItem(k){ return Object.prototype.hasOwnProperty.call(store, k) ? store[k] : null; },
  setItem(k, v){ writeLog.push(String(k)); store[String(k)] = String(v); },
  removeItem(k){ delete store[k]; },
};

/* ---- 真碼入作用域 ---- */
eval(extractConst('SAVE'));
eval(extractConst('SAVE_SLOT_COUNT'));
eval(extractConst('PREFS_KEY'));
eval(extractConst('STRESS_MAX'));
eval(extractFn('saveKeyForSlot'));
eval(extractFn('defaultPrefs'));
eval(extractFn('loadPrefs'));
eval(extractFn('dualTrackNumbers'));
eval(extractFn('readDualTracks'));
eval(extractFn('syncDualTracks'));
eval(extractFn('normalizeSaveObj'));
eval(extractFn('saveSummaryFrom'));
eval(extractFn('readSlotRaw'));
eval(extractFn('listSaveSlots'));
eval(extractFn('slotLabel'));
eval(extractFn('hasSave'));
eval(extractFn('loadFromSlot'));

/* ---- 舊格式 fixture（v19z9 多槽／normalize 之前嘅形狀） ---- */
const OLD_SAVE_1 = {
  dayIndex: 30, money: 23456, fame: 42, stage: 10, acting: 20,
  stress: 130, popularity: 7, flags: { tutorialDone: true },
  story: { done: { C1: true }, rel: {}, favor: {} },
  weekPlan: ['rest','rest','rest','rest','rest','rest','rest'],
};
const OLD_SAVE_3 = {
  dayIndex: 3, money: 11500, fame: 5, stage: 2, acting: 8,
  stress: 20, flags: { tutorialDone: true },
};
const OLD_PREFS = {
  bgmMuted: false, sfxMuted: false, volume: 70, textSpeed: 'fast',
  reduceMotion: false, familySafeContent: false, activeSlot: 1, lastSlot: 1,
};
function seed(){
  store = {};
  store[SAVE] = JSON.stringify(OLD_SAVE_1);
  store[SAVE + '_slot3'] = JSON.stringify(OLD_SAVE_3);
  store[PREFS_KEY] = JSON.stringify(OLD_PREFS);
  writeLog = [];
}
const clone = o => JSON.parse(JSON.stringify(o));

/* ---- A：舊檔槽位摘要係預期值 ---- */
seed();
const slotsA = listSaveSlots();
ok('A slot1 summary from old save', !!slotsA[0].summary && slotsA[0].summary.week===5 && slotsA[0].summary.money===23456 && slotsA[0].summary.stage===42);
ok('A slot2 empty', slotsA[1].empty===true && slotsA[1].summary===null);
ok('A slot3 summary from old save', !!slotsA[2].summary && slotsA[2].summary.week===1 && slotsA[2].summary.money===11500 && slotsA[2].summary.stage===5);
ok('A slotLabel format', slotLabel(1, slotsA[0].summary, false)==='槽 1 · 第 5 週 · $23,456 · 聲望 42');
ok('A hasSave true', hasSave()===true);

/* ---- B：遷移不變量＋loadFromSlot 唔寫回 ---- */
seed();
const before = clone(listSaveSlots());
writeLog = [];
const loaded1 = loadFromSlot(1);
const loaded3 = loadFromSlot(3);
ok('B loadFromSlot returns normalized objects', !!loaded1 && !!loaded3);
ok('B loadFromSlot writes nothing back', writeLog.length===0);
ok('B stored bytes untouched by load', store[SAVE]===JSON.stringify(OLD_SAVE_1) && store[SAVE+'_slot3']===JSON.stringify(OLD_SAVE_3));
const after = listSaveSlots();
ok('B slot summaries invariant under migration', JSON.stringify(before)===JSON.stringify(after));

/* ---- C：normalizeSaveObj 遷移結果本身（同現行規則一致） ---- */
const norm = normalizeSaveObj(clone(OLD_SAVE_1));
ok('C fills inventory', !!norm.inventory && typeof norm.inventory==='object');
ok('C fills giftMeta shape', !!norm.giftMeta && Array.isArray(norm.giftMeta.lastGiveDay)===false && typeof norm.giftMeta.lastGiveDay==='object' && typeof norm.giftMeta.shopWeek==='number');
ok('C fills wrapHistory/castingTags/postShootRewards arrays', Array.isArray(norm.wrapHistory) && Array.isArray(norm.castingTags) && Array.isArray(norm.postShootRewards));
ok('C fills awardsLog/awardsFlags', Array.isArray(norm.awardsLog) && !!norm.awardsFlags && typeof norm.awardsFlags==='object');
ok('C fills newspaper arrays', Array.isArray(norm.newspaperQueue) && Array.isArray(norm.newspaperClippings));
ok('C vocal defaults to 14', norm.vocal===14);
ok('C stress clamped to STRESS_MAX', norm.stress===STRESS_MAX);
ok('C core fields untouched', norm.dayIndex===30 && norm.money===23456 && norm.fame===42 && norm.stage===10 && norm.acting===20);
ok('C normalize(null) is null', normalizeSaveObj(null)===null);

/* ---- D：loadPrefs 一次性遷移只寫 prefs 一次、唔掂存檔／activeSlot ---- */
seed();
writeLog = [];
const p1 = loadPrefs();
ok('D legacy familySafeContent upgraded to null', p1.familySafeContent===null);
ok('D prefs migration writes prefs exactly once', writeLog.length===1 && writeLog[0]===PREFS_KEY);
ok('D activeSlot preserved', p1.activeSlot===1 && p1.lastSlot===1);
writeLog = [];
const p2 = loadPrefs();
ok('D second loadPrefs performs no migration write', writeLog.length===0 && p2.familySafeContent===null);
ok('D slot summaries unaffected by prefs migration', JSON.stringify(listSaveSlots())===JSON.stringify(before));

/* ---- E：壞檔／非物件檔唔爆、顯示空白 ---- */
seed();
store[SAVE + '_slot2'] = '{not json';
store[SAVE + '_slot3'] = '42';
let threw = false, slotsE = null;
try{ slotsE = listSaveSlots(); }catch(_e){ threw = true; }
ok('E corrupt slot does not throw', !threw && !!slotsE);
ok('E corrupt/non-object slots read as empty', !!slotsE && slotsE[1].empty===true && slotsE[2].empty===true);
ok('E slot1 still read fine', !!slotsE && slotsE[0].empty===false);
store = {}; writeLog = [];
ok('E no saves at all -> hasSave false', hasSave()===false);

console.log(fails.length ? ('FAILURES: ' + fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
