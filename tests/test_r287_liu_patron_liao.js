// v20a287：Beat 5 冷版接 liaoChoice——廖炳星線 Beat 3 搶鏡抉擇之後，Beat 5 提攜要行冷版。
// 背景（v279 NOTES L65）：liu_patron／liu_patron_cold 閘門只讀 enc79_liu_declined／
// enc79_liu_clash_script，唔讀 liaoChoice——揀咗搶鏡（liaoChoice==="steal"）都行暖版。
// 修法（加法，唔改寫）：冷版閘加 (S.wf3 && S.wf3.liaoChoice)==="steal" 為開冷版條件；
// 暖版閘同步排除同一條件（跟 v269 排除式寫法）。讀旗路徑跟 liu_steal 閘本身
// （S.wf3 && S.wf3.liaoChoice，L39037），唔用 ensureWf3() 另起寫法。
// 斷言：A 組靜態——兩閘讀旗＋註冊次序＋結算唔郁；B 組邏輯——沙盒跑真 when()：
//   (a) steal → 冷開暖唔開（PickBeat 揀冷）；(b) steady → 暖開冷唔開；
//   (c) 無 liaoChoice＋無壞旗 → 暖開（v269 舊行為不變）。
// 用法：node tests/test_r287_liu_patron_liao.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
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
    else if(c === ';' && !started) { j++; break; }
  }
  return html.slice(i, j);
}
function extractDlg(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('missing ' + name);
  const j = html.indexOf('\nconst ', i + 10);
  return html.slice(i, j < 0 ? undefined : j);
}

/* ---- A 組：靜態——兩閘讀 liaoChoice，舊旗同次序唔變，結算唔郁 ---- */
const STEAL = '(S.wf3 && S.wf3.liaoChoice)==="steal"';
ok('A1 冷版閘讀 liaoChoice==="steal"（開冷版條件）',
  html.includes('{ id:"liu_patron_cold", when(st){ return enc79TierOf(st.fav)>=4 && ((S.flags||{}).enc79_liu_declined || (S.flags||{}).enc79_liu_clash_script || ' + STEAL + '); }'));
ok('A2 暖版閘排除 liaoChoice==="steal"（跟 v269 排除式寫法）',
  html.includes('{ id:"liu_patron", when(st){ return enc79TierOf(st.fav)>=4 && !((S.flags||{}).enc79_liu_declined || (S.flags||{}).enc79_liu_clash_script || ' + STEAL + '); }'));
ok('A3 冷版閘仲讀 v269 兩支舊旗（declined／clash_script）',
  html.includes('(S.flags||{}).enc79_liu_declined || (S.flags||{}).enc79_liu_clash_script || (S.wf3 && S.wf3.liaoChoice)==="steal")'));
ok('A4 暖版閘仲讀 v269 兩支舊旗',
  html.includes('!((S.flags||{}).enc79_liu_declined || (S.flags||{}).enc79_liu_clash_script || (S.wf3 && S.wf3.liaoChoice)==="steal")'));
ok('A5 讀旗路徑跟 liu_steal 閘一致（S.wf3.liaoChoice，唔係 ensureWf3 另起寫法）',
  html.includes('!(S.wf3 && S.wf3.liaoChoice) && enc83NodeDone("N9")'));
ok('A6 結算唔郁：wf3SettleTick 仲喺度，搶鏡結算照舊（+$800＋面子債 dueDay+14）',
  html.indexOf('function wf3SettleTick(') >= 0 &&
  html.includes('S.money = (Number(S.money)||0) + 800;') &&
  html.includes('id:"debt_wf3_liao_grudge"') &&
  html.includes('dueDay: day+14'));

/* ---- sandbox（ENC79，寫法跟 test_sideline269_logic.js） ---- */
let S;
let _ys = { year: 1990, season: '春' };
let _doneNodes = new Set();
let _storyFlags = {};
function resetS(day){
  S = { dayIndex: day||0, fame: 0, money: 2000, flags: {}, npcs: { agent: 0 }, mockRumors: [], mockDebts: [], mockCredits: [], board: {}, shoots: [], mapTips: {}, story: { flags: {} }, starWeek: {}, weekGigsDone: 0, starWhispers: {} };
  _doneNodes = new Set(); _storyFlags = {};
}
function setFav(sid, n){ enc79EnsureStars(); S.stars[sid].fav = n; }
function beatOf(sid, id){ return (ENC79_BEATS[sid] || []).find(b => b.id === id); }
function weekNumNow(){ return 3; }
function yearSeasonNow(){ return _ys; }
function enc87StoryFlag(f){ return !!_storyFlags[f]; }
function ensureMockJournal(){ if(!Array.isArray(S.mockRumors)) S.mockRumors=[]; if(!Array.isArray(S.mockDebts)) S.mockDebts=[]; }
function syncNotebookMirror(){}
function saveQ(){}
function refreshMoneyHud(){}
function noteWeekHighlight(){}
function rumorStateLabel(state){ return '剛聽聞'; }
function R(a,b){ return a; }
function bumpNpc(id, d){ const b = S.npcs[id]||0; S.npcs[id] = Math.min(100, b+d); return S.npcs[id]-b; }
function toast(){}
let _ledger = null;
function ensureFavorLedger(){ if(!_ledger) _ledger = { settled:0, credits:0, exodus:[], counted:{} }; return _ledger; }
function favorLedgerNoteCredit(id){ const L = ensureFavorLedger(); if(L.counted[id]) return false; L.counted[id]={kind:'credit'}; L.credits++; return true; }
function softSocialDailyCap(){ return { ok:true, used:0, max:99, left:99 }; }
function softSocialDailyUse(){}
function softPreviewOn(){ return false; }
function ending78Gate(){ return false; }
function npcNextTierHint(){ return null; }
const BehaviorGate = { featureFlag_softBehaviorGatePreview: ()=>false };
const StoryOC = {
  isDone: (id)=> _doneNodes.has(id),
  listOpen: ()=>({ open: [] }),
  findNodeRaw: (id)=>({ id }),
};
function storyNodeLocId(n){ return n && n.__loc; }
function enc79PlayEncounter(){}
function enc79LocName(id){ return id; }

const asVar = (code, name)=> code.replace('const ' + name + ' =', 'var ' + name + ' =');
const consts269 = ['ENC79_TIER_NAMES','ENC79_PLAYER_TIERS','ENC79_FAV_CAPS','ENC79_STARS','ENC79_PILOT','ENC79_STAGEUP','ENC79_CAP_LINES','ENC79_WRAP_ECHO','ENC79_BEATS','ENC79_DIALOG','ENC79_FIRST_ALT98'].map(n=> asVar(extractConst(n), n)).join('\n')
  + '\n' + ['ENC79_DLG_liu_bingxing','ENC79_DLG_mak_zhendong'].map(n=> asVar(extractDlg(n), n)).join('\n')
  + '\n' + asVar(extractDlg('ENC83_DLG_gu_mingfai'), 'ENC83_DLG_gu_mingfai')
  + '\nENC79_DIALOG["liu_bingxing"] = ENC79_DLG_liu_bingxing;\nENC79_DIALOG["mak_zhendong"] = ENC79_DLG_mak_zhendong;\nENC79_DIALOG["gu_mingfai"] = ENC83_DLG_gu_mingfai;';
const t4Start = html.indexOf('/* ---------- T4 提攜');
const t4End = html.indexOf('/* ===== v20a84 ENC84', t4Start);
if(t4Start < 0 || t4End < 0) throw new Error('T4 region not found');
const t4Region = html.slice(t4Start, t4End);
const fns269 = ['enc79StarDef','enc79Hash','enc79Rand','enc79EnsureStars','enc79StarState','enc79TierOf','enc79PlayerTier','enc79FavCap','enc79AddFav','enc79WhisperActive','enc79GrantWhisper','enc79GrantCredit','enc79BoardHasStar','enc79BoardHasActionGig','enc79BeatOpen','enc79AnyBeatOpen','enc79PickBeat','enc79ChoiceFx','enc79RunChoiceFx','enc79NormSeg','enc79BuildScript','enc83NodeDone','enc83Flag','contra98EncFirstLocSwap','ensureWf3'];
eval(consts269 + '\n' + t4Region + '\n' + fns269.map(extractFn).join('\n'));

function openBeat(sid, id){ return enc79BeatOpen(sid, beatOf(sid, id)); }
function beatIds(sid){ return (ENC79_BEATS[sid]||[]).map(b=>b.id); }
function liuSetup(day, fav, choice){
  resetS(day); _ys = { year: 1992, season: '秋' }; setFav('liu_bingxing', fav);
  if(choice) S.wf3 = { liaoChoice: choice };
}
function markOtherBeatsDone(){
  const st = S.stars.liu_bingxing;
  for(const b of (ENC79_BEATS.liu_bingxing||[]))
    if(!b.id.endsWith('_patron') && b.id!=='liu_patron_cold') st.beatsDone[b.id] = 1;
}
function markAllButWarmDone(){
  const st = S.stars.liu_bingxing;
  for(const b of (ENC79_BEATS.liu_bingxing||[]))
    if(!b.id.endsWith('_patron')) st.beatsDone[b.id] = 1;
}

/* ---- B 組：邏輯——真 when() 分流 ---- */
ok('B0 註冊次序：冷版排暖版之前（shadow 唔靠次序都識分流，但次序照舊）',
  beatIds('liu_bingxing').indexOf('liu_patron_cold') < beatIds('liu_bingxing').indexOf('liu_patron'));
liuSetup(300, 70, 'steal');
ok('B1 (a) steal → 冷版開、暖版唔開',
  openBeat('liu_bingxing','liu_patron_cold')===true && openBeat('liu_bingxing','liu_patron')===false);
ok('B2 (a) steal → PickBeat 揀冷版（其他 beat 已做晒）',
  (()=>{ markOtherBeatsDone(); const p = enc79PickBeat('liu_bingxing'); return !!p && p.id==='liu_patron_cold'; })());
liuSetup(301, 70, 'steady');
ok('B3 (b) steady → 暖版開、冷版唔開',
  openBeat('liu_bingxing','liu_patron')===true && openBeat('liu_bingxing','liu_patron_cold')===false);
ok('B4 (b) steady → PickBeat 揀暖版（其他 beat 已做晒）',
  (()=>{ markAllButWarmDone(); const p = enc79PickBeat('liu_bingxing'); return !!p && p.id==='liu_patron'; })());
liuSetup(302, 70, null);
ok('B5 (c) 無 liaoChoice＋無壞旗 → 暖版開、冷版唔開（v269 舊行為不變）',
  openBeat('liu_bingxing','liu_patron')===true && openBeat('liu_bingxing','liu_patron_cold')===false);
liuSetup(303, 30, 'steal');
ok('B6 steal 但 tier 未夠 4 → 冷暖都唔開（tier 門檻照舊）',
  openBeat('liu_bingxing','liu_patron')===false && openBeat('liu_bingxing','liu_patron_cold')===false);
ok('B7 端到端：enc79RunChoiceFx("liu_steal") 落旗 → 冷版開、暖版唔開',
  (()=>{ resetS(304); _ys = { year: 1992, season: '秋' }; setFav('liu_bingxing', 70);
    enc79RunChoiceFx('liu_steal');
    return S.wf3 && S.wf3.liaoChoice === 'steal' &&
      openBeat('liu_bingxing','liu_patron_cold')===true &&
      openBeat('liu_bingxing','liu_patron')===false; })());

console.log(fails.length ? ('\nFAILURES: ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
