// v20a289 Q1 劣評分支：殺青表現判定 enc79WrapPerf 邏輯測試——
//   (1) 公式：欠數（底圍 vs req）每點 +3%（上限 30%）＋壓力 60–84 加 8%／≥85 加 20%，合計上限 50% ；
//   (2) 表現合格（欠數 0＋壓力 <60）→ pBad 0，絕唔出劣評（好評係常態）；
//   (3) 擲骰邊界：R(1,100) <= pBad*100 先算劣評，兩邊都測得到；
//   (4) onWrap 整合：好評主角 +3／配角 +1，劣評主角 +1／配角 0；fame 唔再決定好劣。
// 用法：node tests/test_r289_wrap_perf_logic.js [path-to-index.html]
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
  let depth = 0, started = false, j = i;
  for(; j < html.length; j++){
    const c = html[j];
    if(c === '{' || c === '['){ depth++; started = true; }
    else if(c === '}' || c === ']'){ depth--; if(started && depth === 0){ j++; break; } }
    else if(c === ';' && !started) { j++; break; }
  }
  return html.slice(i, j);
}
/* ---- sandbox ---- */
let S;
let _week = 3;
let _ys = { year: 1990, season: '春' };
let _storyOpen = [];
let _rVal = 1; /* 可控擲骰：1＝最差運，100＝最好運 */
const GIGS = [
  { id:'g_test_lead', roleScale:'film_lead_big', leadStarId:'luk_baakyin', genreLabel:'劇情片', type:'電影', title:'測試主角戲', workTitle:'測試主角戲' },
  { id:'g289_req', type:'電影', title:'測試欠數戲', workTitle:'測試欠數戲', req:{ acting:60, stamina:40 } },
  { id:'g289_cast', type:'電影', title:'測試四角戲', workTitle:'測試四角戲', req:{ acting:18 }, cast:{ leadM:'luk_baakyin', leadF:null, supportM:'liu_bingxing', supportF:null } },
  { id:'g289_noreq', type:'電影', title:'測試無門檻戲', workTitle:'測試無門檻戲' },
];
const LOCS = [ {id:'film_lion', name:'獅子山製片'} ];
function resetS(day){
  /* 開局七圍＋壓力 12（live 開局值），各 case 再改 */
  S = { dayIndex: day||0, fame: 0, money: 500, flags: {}, npcs: { agent: 0 }, mockRumors: [], mockDebts: [], mockCredits: [], board: {}, shoots: [], mapTips: {},
    acting: 18, stage: 14, vocal: 14, looks: 22, stamina: 75, iq: 20, charm: 16, stress: 12 };
}
function weekNumNow(){ return _week; }
function yearSeasonNow(){ return _ys; }
function ensureMockJournal(){ if(!Array.isArray(S.mockRumors)) S.mockRumors=[]; if(!Array.isArray(S.mockDebts)) S.mockDebts=[]; }
function syncNotebookMirror(){}
function saveQ(){}
function refreshMoneyHud(){}
function noteWeekHighlight(){}
function R(a,b){ return _rVal; }
function bumpNpc(id, d){ const b = S.npcs[id]||0; S.npcs[id] = Math.min(100, b+d); return S.npcs[id]-b; }
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
  isDone: ()=>false,
  listOpen: ()=>({ open: _storyOpen }),
  findNodeRaw: (id)=>({ id, __loc: (_storyOpen.find(r=>r.id===id)||{}).__loc }),
};
function storyNodeLocId(n){ return n && n.__loc; }
let _played = [];
function enc79PlayEncounter(sid, loc, wasMet){ _played.push([sid, loc, wasMet]); }

const names = ['ENC79_TIER_NAMES','ENC79_PLAYER_TIERS','ENC79_FAV_CAPS','ENC79_COOLDOWN','ENC79_DAILY_CAP','ENC79_WEEKLY_CAP','ENC79_WEEK_SOFT_CAP','ENC79_STARS','ENC79_PILOT','ENC79_DISTANCE_EXTRA','ENC79_STAGEUP','ENC79_CAP_LINES','ENC79_WRAP_ECHO','ENC79_TEA_POOL','ENC79_BEATS','ENC79_DIALOG'];
const asVar = (code, name)=> code.replace('const ' + name + ' =', 'var ' + name + ' =');
function extractDlg(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i<0) throw new Error('missing ' + name);
  const j = html.indexOf('\nconst ', i + 10);
  return html.slice(i, j<0 ? undefined : j);
}
const consts = names.map(n=> asVar(extractConst(n), n)).join('\n')
  + '\n' + ['luk_baakyin','liu_bingxing','mak_zhendong','yip_manzi'].map(sid=>{
      try{ return asVar(extractDlg('ENC79_DLG_' + sid), 'ENC79_DLG_' + sid) + '\nENC79_DIALOG["' + (sid==='yip_manzi' ? 'yip_manji' : sid) + '"] = ENC79_DLG_' + sid + ';'; }
      catch(e){ return ''; }
    }).join('\n');
const fns = ['enc79StarDef','enc79LocName','enc79Hash','enc79Rand','enc79EnsureStars','enc79StarState','enc79TierOf','enc79PlayerTier','enc79FavCap','enc79AddFav','enc79InWindow','enc79WhisperActive','enc79PresenceP','enc79EnsureDay','enc79PresenceAt','enc79GrantWhisper','enc79GrantCredit','enc79BoardHasStar','enc79BoardHasActionGig','enc79BeatOpen','enc79AnyBeatOpen','enc79PickBeat','enc79ChoiceFx','enc79RunChoiceFx','enc79NormSeg','enc79StoryPendingAt','enc79TryIntercept','enc79DistanceLook','enc79OnWrap','enc79WrapPerf','enc79PaperWhisper','enc79HoTrustLine','enc79HelpAvailable','enc79MockAskBranch','enc79PayTea','enc79TeaListen','enc79HelpClear','enc79AgencyWind','enc79BuildScript'];
eval(consts + '\n' + fns.map(extractFn).join('\n'));

const G_REQ = GIGS.find(g=>g.id==='g289_req');
const G_CAST = GIGS.find(g=>g.id==='g289_cast');
const G_NOREQ = GIGS.find(g=>g.id==='g289_noreq');

/* ---- (1) 公式：欠數 ---- */
resetS(10); S.acting = 60; S.stamina = 40; S.stress = 12; _rVal = 1;
ok('表現合格：欠數 0＋壓力 12 → pBad 0，擲骰點差都唔劣評', (()=>{ const p = enc79WrapPerf({}, G_REQ); return p.pBad===0 && p.bad===false && p.short===0; })());
resetS(11); S.acting = 60; S.stamina = 40; S.stress = 12; _rVal = 100;
ok('表現合格：最好運都係好評（pBad 0 唔睇骰）', enc79WrapPerf({}, G_REQ).bad===false);
resetS(12); S.acting = 56; S.stamina = 40; S.stress = 12;
ok('欠數 4（衫頂住嘅規模）：pBad 12%', enc79WrapPerf({}, G_REQ).pBad===0.12);
resetS(13); S.acting = 59; S.stamina = 40; S.stress = 12;
ok('欠數 1：pBad 3%', enc79WrapPerf({}, G_REQ).pBad===0.03);
resetS(14); S.acting = 50; S.stamina = 40; S.stress = 12;
ok('欠數 10：pBad 30%（欠數項上限）', enc79WrapPerf({}, G_REQ).pBad===0.30);
resetS(15); S.acting = 30; S.stamina = 40; S.stress = 12;
ok('欠數 30：pBad 仍然 30%（欠數項封頂）', enc79WrapPerf({}, G_REQ).pBad===0.30);
resetS(16); S.acting = 60; S.stamina = 40; S.stress = 12;
ok('無 req 通告：底圍 0 都唔計欠數', enc79WrapPerf({}, G_NOREQ).pBad===0);
resetS(17); S.acting = 60; S.stamina = 40; S.stress = 12;
ok('非屬性 req 鍵唔計欠數（__y66w 防禦）', enc79WrapPerf({}, { req:{ acting:60, stamina:40, __y66w:99 } }).short===0);
resetS(18); S.acting = undefined; S.stamina = undefined; S.stress = 12;
ok('底圍缺值當 0：欠數計足 100', enc79WrapPerf({}, G_REQ).short===100);

/* ---- (2) 公式：壓力 ---- */
resetS(20); S.acting = 60; S.stamina = 40; S.stress = 59;
ok('壓力 59：pBad 0（未入加壓區）', enc79WrapPerf({}, G_REQ).pBad===0);
resetS(21); S.acting = 60; S.stamina = 40; S.stress = 60;
ok('壓力 60：pBad 8%', enc79WrapPerf({}, G_REQ).pBad===0.08);
resetS(22); S.acting = 60; S.stamina = 40; S.stress = 84;
ok('壓力 84：pBad 仍然 8%', enc79WrapPerf({}, G_REQ).pBad===0.08);
resetS(23); S.acting = 60; S.stamina = 40; S.stress = 85;
ok('壓力 85（危險線）：pBad 20%', enc79WrapPerf({}, G_REQ).pBad===0.20);
resetS(24); S.acting = 50; S.stamina = 40; S.stress = 90;
ok('欠數 10＋壓力 90：pBad 50%（合計上限）', enc79WrapPerf({}, G_REQ).pBad===0.50);
resetS(25); S.acting = 60; S.stamina = 40; S.stress = 90;
ok('無欠數但壓力爆煲：pBad 20%，劣評出得到', enc79WrapPerf({}, G_REQ).pBad===0.20);

/* ---- (3) 擲骰邊界 ---- */
resetS(30); S.acting = 56; S.stamina = 40; S.stress = 12; _rVal = 12;
ok('擲骰邊界：pBad 12%，擲 12 → 劣評', enc79WrapPerf({}, G_REQ).bad===true);
_rVal = 13;
ok('擲骰邊界：pBad 12%，擲 13 → 好評', enc79WrapPerf({}, G_REQ).bad===false);
resetS(31); S.acting = 60; S.stamina = 40; S.stress = 12; _rVal = 1;
ok('缺 gig：當表現合格，唔劣評', enc79WrapPerf({}, null).bad===false && enc79WrapPerf({}, undefined).pBad===0);

/* ---- (4) onWrap 整合：四角分格＋舊制退役 ---- */
resetS(40); _rVal = 1;
enc79OnWrap({ gigId:'g289_cast', fame: 5 });
ok('殺青好評：主角 +3／配角 +1', S.stars.luk_baakyin.fav===3 && S.stars.liu_bingxing.fav===1);
resetS(41); S.stress = 90; _rVal = 1;
enc79OnWrap({ gigId:'g289_cast', fame: 5 });
ok('殺青劣評：主角 +1／配角 0，合作標記照設', S.stars.luk_baakyin.fav===1 && S.stars.liu_bingxing.fav===0 && S.stars.luk_baakyin.workedWith===true && S.stars.liu_bingxing.wrapEcho===true);
resetS(42); S.stress = 90; _rVal = 100;
enc79OnWrap({ gigId:'g289_cast', fame: 5 });
ok('壓力爆煲但擲骰好：照樣好評 +3／+1（好評仍係常態）', S.stars.luk_baakyin.fav===3 && S.stars.liu_bingxing.fav===1);
resetS(43);
enc79OnWrap({ gigId:'g289_cast', fame: 0 });
ok('舊制退役：fame 0 但表現合格 → 好評 +3（唔再睇 fame）', S.stars.luk_baakyin.fav===3);

if(fails.length){ console.log('FAILURES: ' + fails.join(' | ')); process.exit(1); }
console.log('ALL PASS');
