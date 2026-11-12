// v20a144 ENC144 邏輯測試：紅星巧遇頻率收緊（用戶 2026-11-12 拍板：每日上限 2→1＋新增每週硬上限 2）——
//   (1) 常數：DAILY_CAP=1、WEEKLY_CAP=2；
//   (2) 同日第二次觸發被擋（每日 1 次）；
//   (3) 同一週第三次被擋（每週 2 次）；
//   (4) 跳過照計：入帳喺播出之前（enc79PlayEncounter 只係 stub、未完成對話，計數已入帳）；
//   (5) 跨週重置（weekNumNow 週界＝星期一）；
//   (6) 不變項：同星冷卻 3 日、每週好感軟頂 +10、級數上限 [30,55,80,100]、出沒率 base 0.5；
//   (7) 舊檔兼容：冇 S.starWeek 嘅舊檔 lazy-init 唔 crash、冪等。
// 反證：喺 pristine main（v20a141）index 上行 → 冇 ENC79_WEEKLY_CAP → 抽取即 throw → FAIL。
// 用法：node tests/test_enc144_logic.js [path-to-index.html]
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
let _merged = {};
let _week = 3;
let _ys = { year: 1990, season: '春' };
let _storyOpen = [];
const GIGS = [
  { id:'g_test_lead', roleScale:'film_lead_big', leadStarId:'luk_baakyin', genreLabel:'劇情片', type:'電影', title:'測試主角戲', workTitle:'測試主角戲' },
  { id:'g_test_sup', roleScale:'film_support_main', genreLabel:'動作片', type:'電影', title:'測試配角戲', workTitle:'測試配角戲' },
];
const LOCS = [ {id:'film_lion', name:'獅子山製片'}, {id:'cafe_cha', name:'金龍茶餐廳'}, {id:'rec_star', name:'天星音樂'}, {id:'film_cotton', name:'紅棉影業'}, {id:'rec_hk', name:'香江唱片'}, {id:'tvb_kowloon', name:'九龍電視台'} ];
const MERGE_FRAGS = [
  { id:'rumor_lu_baiyan_angry', source:'場務八卦', title:'陸柏言片場發脾氣', text:'…' },
  { id:'rumor_liao_bingxing_talk', source:'茶水姐傳聞', title:'廖炳星同導演密談', text:'…' },
  { id:'rumor_mai_zhendong_hurt', source:'武師目擊', title:'麥震東片場整親', text:'…' },
];
const MOCK_RUMOR_SEEDS = [
  { id:'tvb_rules_gossip', source:'金龍茶餐廳', title:'電視城廠景生存守則', text:'…', season:'' },
  { id:'gao_steal_spotlight', source:'片場休息區', title:'高仔片場搶鏡', text:'…', season:'' },
];
function resetS(day){
  S = { dayIndex: day||0, fame: 0, money: 500, flags: {}, npcs: { agent: 0 }, mockRumors: [], mockDebts: [], mockCredits: [], board: {}, shoots: [], mapTips: {} };
  _merged = {};
}
function weekNumNow(){ return _week; }
function yearSeasonNow(){ return _ys; }
function hasMergedIntel(id){ return !!_merged[id]; }
function ensureMockJournal(){ if(!Array.isArray(S.mockRumors)) S.mockRumors=[]; if(!Array.isArray(S.mockDebts)) S.mockDebts=[]; }
function syncNotebookMirror(){}
function saveQ(){}
function refreshMoneyHud(){}
function noteWeekHighlight(){}
function rumorStateLabel(state){ return ({ normal:'剛聽聞', fresh:'剛聽聞', teased:'已知', merged:'已拼合' })[String(state||'normal')] || '剛聽聞'; }
function R(a,b){ return a; }
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
/* DLG 對白內文含括號字元，brace-count 抽取會截斷——改用行首錨點切片 */
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
const fns = ['enc79StarDef','enc79LocName','enc79Hash','enc79Rand','enc79EnsureStars','enc79StarState','enc79TierOf','enc79PlayerTier','enc79FavCap','enc79AddFav','enc79InWindow','enc79WhisperActive','enc79PresenceP','enc79EnsureDay','enc79PresenceAt','enc79GrantWhisper','enc79GrantFrag','enc79GrantRumorCard','enc79GrantCredit','enc79HasMerged','enc79BoardHasStar','enc79BoardHasActionGig','enc79BeatOpen','enc79AnyBeatOpen','enc79PickBeat','enc79ChoiceFx','enc79RunChoiceFx','enc79NormSeg','enc79StoryPendingAt','enc79TryIntercept','enc79DistanceLook','enc79OnWrap','enc79PaperWhisper','enc79HoTrustLine','enc79HelpAvailable','enc79MockAskBranch','enc79PayTea','enc79TeaListen','enc79HelpClear','enc79AgencyWind','enc79BuildScript'];
eval(consts + '\n' + fns.map(extractFn).join('\n'));


/* ---- (1) 常數 ---- */
ok('常數：DAILY_CAP=1、WEEKLY_CAP=2', ENC79_DAILY_CAP===1 && ENC79_WEEKLY_CAP===2);
ok('不變：冷卻 3 日／軟頂 10／級數上限 [30,55,80,100]', ENC79_COOLDOWN===3 && ENC79_WEEK_SOFT_CAP===10 && JSON.stringify(ENC79_FAV_CAPS)==='[30,55,80,100]');

/* ---- (7) 舊檔兼容：S.starWeek lazy-init ---- */
resetS(200); _week = 29;
ok('舊檔（冇 starWeek 欄）lazy-init 唔 crash', (()=>{ try{ enc79EnsureStars(); return S.starWeek && S.starWeek.week===-1 && S.starWeek.triggered===0; }catch(e){ return false; } })());
ok('lazy-init 冪等（計數唔會被重置）', (()=>{ S.starWeek.week = 29; S.starWeek.triggered = 2; enc79EnsureStars(); return S.starWeek.week===29 && S.starWeek.triggered===2; })());

/* ---- (2)(3)(4)(5) 觸發閘：同一 resetS 會話內連續四日（唔 reset，週計數要跨日保留） ---- */
/* forcePresence：模擬真實 enc79EnsureDay——同日 starDay 沿用（triggered／doneToday 保留），跨日先重開 */
function forcePresence(sid, loc){
  const keep = (S.starDay && S.starDay.day===S.dayIndex) ? S.starDay : null;
  S.starDay = { day: S.dayIndex, presence: { [loc]: [sid] }, triggered: keep ? (keep.triggered||0) : 0, doneToday: keep ? Object.assign({}, keep.doneToday) : {} };
}
resetS(200); _week = 29; _played = []; _storyOpen = [];
forcePresence('luk_baakyin','film_lion');
ok('第 1 次（週 29 日 200）：正常觸發＋日／週計數同步入帳', (()=>{ const r = enc79TryIntercept('film_lion'); return r===true && _played.length===1 && S.starDay.triggered===1 && S.starWeek.week===29 && S.starWeek.triggered===1; })());
ok('跳過照計：入帳喺播出之前（stub play 未完成對話，計數已係 1）', S.starDay.triggered===1 && S.starWeek.triggered===1);
forcePresence('liu_bingxing','cafe_cha'); /* 同日第二個有星地點 */
ok('同日第二次被擋（每日 1 次）：唔播＋週計數唔變', (()=>{ const r = enc79TryIntercept('cafe_cha'); return r===false && _played.length===1 && S.starWeek.triggered===1; })());
S.dayIndex = 201; /* 同週下一日 */
forcePresence('mak_zhendong','film_cotton');
ok('第 2 次（週 29 日 201）：跨日但同週，照觸發＋週計數到 2', (()=>{ const r = enc79TryIntercept('film_cotton'); return r===true && _played.length===2 && S.starWeek.week===29 && S.starWeek.triggered===2; })());
S.dayIndex = 202;
forcePresence('yip_manji','rec_hk');
ok('同一週第三次被擋（每週 2 次）：唔播＋日計數冇入帳', (()=>{ const r = enc79TryIntercept('rec_hk'); return r===false && _played.length===2 && S.starWeek.triggered===2 && S.starDay.triggered===0; })());
S.dayIndex = 207; _week = 30; /* 下一週星期一 */
forcePresence('luk_baakyin','film_lion'); /* 陸上次 200 日，207-200=7>3 冷卻已過 */
ok('跨週重置（週 30）：又觸發到＋週計數由 0 起計', (()=>{ const r = enc79TryIntercept('film_lion'); return r===true && _played.length===3 && S.starWeek.week===30 && S.starWeek.triggered===1; })());

/* ---- (6) 不變：冷卻 3 日 ---- */
resetS(201); _week = 29; _played = [];
S.stars = undefined; enc79EnsureStars(); S.stars.luk_baakyin.lastDay = 199;
forcePresence('luk_baakyin','film_lion');
ok('冷卻 3 日內壓制（不變）', enc79TryIntercept('film_lion')===false && _played.length===0);

/* ---- (6) 不變：每週好感軟頂 10 ---- */
resetS(10); _week = 3;
ok('每週好感軟頂不變：巧遇來源 +7 再 +7 只入 3', (()=>{ const a = enc79AddFav('luk_baakyin', 7, 'enc'); const b = enc79AddFav('luk_baakyin', 7, 'enc'); return a===7 && b===3 && S.stars.luk_baakyin.fav===10; })());

/* ---- (6) 不變：出沒率 base 0.5（葉敏芝 1990 春：冇節拍開住、唔喺季節窗、冇風聲） ---- */
resetS(100); _ys = { year:1990, season:'春' };
ok('出沒率 base 不變：葉敏芝 1990 春 P=0.5', enc79PresenceP(enc79StarDef('yip_manji'), 100).p===0.5);

console.log(fails.length ? ('\nFAILURES: ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
