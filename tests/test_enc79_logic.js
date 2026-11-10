// v20a79 ENC79 邏輯測試：紅星巧遇 Phase 1——
//   (1) 出沒盤：種子確定性（同日重算不變）／程天諾 1992 前 P=0／風聲窗 P 升 80%；
//   (2) 觸發閘：冷卻 3 日壓制／每日上限 2／主線待播壓制（出沒保留、doneToday 唔入帳）；
//   (3) 好感：五段邊界／級數上限（臨記 30）／每週軟頂 +10（巧遇來源）／殺青來源唔計軟頂／跌幅直扣；
//   (4) 舊檔兼容：冇 S.stars 嘅舊檔 lazy-init 唔 crash、冪等；
//   (5) 風聲：入傳聞頁「風聲」類、同星同時最多 1 條、過期轉舊聞；
//   (6) 處置表：茶餐廳飲茶未持有保底（已持有唔收錢唔出卡）／執漏真債權／事務所聽風聲每日真資訊＋人情可重複累積；
//   (7) 閘匙保留：茶餐廳三粒＋事務所兩粒打聽 defs 仍在；後巷食煙／打招呼已刪；
//   (8) 節拍：陸伏筆 1990 T0 開、陸情報要拼合情報先開；殺青 +3 入帳＋workedWith。
// 反證：喺 v20a78 index 上行 → 冇 ENC79_* 函數 → 抽取即 throw → FAIL。
// 用法：node tests/test_enc79_logic.js [path-to-index.html]
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

const names = ['ENC79_TIER_NAMES','ENC79_PLAYER_TIERS','ENC79_FAV_CAPS','ENC79_COOLDOWN','ENC79_DAILY_CAP','ENC79_WEEK_SOFT_CAP','ENC79_STARS','ENC79_PILOT','ENC79_DISTANCE_EXTRA','ENC79_STAGEUP','ENC79_CAP_LINES','ENC79_WRAP_ECHO','ENC79_TEA_POOL','ENC79_BEATS','ENC79_DIALOG'];
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

/* ---- (4) 舊檔兼容 lazy-init ---- */
resetS(0);
ok('舊檔（冇 stars 欄）lazy-init 唔 crash', (()=>{ try{ const m = enc79EnsureStars(); return m && m.luk_baakyin && m.luk_baakyin.fav===0 && m.luk_baakyin.lastDay===-999; }catch(e){ return false; } })());
ok('lazy-init 冪等（fav 唔會被重置）', (()=>{ S.stars.luk_baakyin.fav = 33; enc79EnsureStars(); return S.stars.luk_baakyin.fav===33; })());
ok('名冊 12 星齊＋當紅花旦唔入名冊', ENC79_STARS.length===12 && !ENC79_STARS.some(s=>s.name.indexOf('海媚')>=0));

/* ---- (3) 好感 ---- */
ok('五段邊界', enc79TierOf(0)===0 && enc79TierOf(9)===0 && enc79TierOf(10)===1 && enc79TierOf(24)===1 && enc79TierOf(25)===2 && enc79TierOf(44)===2 && enc79TierOf(45)===3 && enc79TierOf(69)===3 && enc79TierOf(70)===4 && enc79TierOf(100)===4);
resetS(10); _week = 3;
ok('級數：冇作品冇聲望＝臨記、上限 30', enc79PlayerTier()===0 && enc79FavCap()===30);
ok('每週軟頂：巧遇來源 +7 再 +7 只入 3', (()=>{ const a = enc79AddFav('luk_baakyin', 7, 'enc'); const b = enc79AddFav('luk_baakyin', 7, 'enc'); return a===7 && b===3 && S.stars.luk_baakyin.fav===10; })());
ok('殺青來源唔計軟頂、但受級數上限 30', (()=>{ const a = enc79AddFav('luk_baakyin', 50, 'wrap'); return a===20 && S.stars.luk_baakyin.fav===30; })());
ok('跌幅直扣（放料 -8）', (()=>{ const a = enc79AddFav('luk_baakyin', -8, 'enc'); return a===-8 && S.stars.luk_baakyin.fav===22; })());
ok('級數：做過主角級通告＝主角、上限 80', (()=>{ S.flags['done_g_test_lead']=1; return enc79PlayerTier()===2 && enc79FavCap()===80; })());

/* ---- (1) 出沒盤 ---- */
resetS(100); _ys = { year:1990, season:'春' };
const sd1 = enc79EnsureDay();
const snap1 = JSON.stringify(sd1.presence);
S.starDay = null;
const sd2 = enc79EnsureDay();
ok('出沒盤種子確定性（同日重算結果不變）', JSON.stringify(sd2.presence)===snap1);
ok('程天諾 1992 前 P=0', enc79PresenceP(enc79StarDef('ching_tinlok'), 100).p===0);
_ys = { year:1992, season:'秋' };
ok('程天諾 1992 秋窗 P=75%', enc79PresenceP(enc79StarDef('ching_tinlok'), 800).p>=0.75);
_ys = { year:1990, season:'春' };

/* ---- (5) 風聲 ---- */
resetS(50);
ok('風聲：入帳＋傳聞卡來源「風聲」', (()=>{ enc79GrantWhisper('luk_baakyin','tea'); const r = S.mockRumors.find(r=>r.wind); return enc79WhisperActive('luk_baakyin') && r && r.source==='風聲' && r.windUntil===52; })());
ok('風聲窗：P 升到 80%', enc79PresenceP(enc79StarDef('luk_baakyin'), 50).p>=0.8);
ok('同星同時最多 1 條風聲（再 grant 唔出新卡）', (()=>{ const n0 = S.mockRumors.filter(r=>r.wind).length; enc79GrantWhisper('luk_baakyin','paper'); return S.mockRumors.filter(r=>r.wind).length===n0; })());
ok('風聲過期：轉舊聞＋窗口清除', (()=>{ S.dayIndex = 60; S.starDay = null; enc79EnsureDay(); const r = S.mockRumors.find(r=>r.wind); return !enc79WhisperActive('luk_baakyin') && r && r.windOld===true; })());

/* ---- (2) 觸發閘 ---- */
function forcePresence(sid, loc){
  S.starDay = { day: S.dayIndex, presence: { [loc]: [sid] }, triggered: 0, doneToday: {} };
}
resetS(200); _ys = { year:1990, season:'春' }; _played = [];
forcePresence('luk_baakyin','film_lion');
ok('正常觸發：播巧遇＋入帳（seen/lastDay/doneToday）', (()=>{ const r = enc79TryIntercept('film_lion'); return r===true && _played.length===1 && S.stars.luk_baakyin.seen===1 && S.stars.luk_baakyin.lastDay===200; })());
resetS(201); _played = [];
S.stars = undefined; enc79EnsureStars(); S.stars.luk_baakyin.lastDay = 199; /* 冷卻中（差 2 日） */
forcePresence('luk_baakyin','film_lion');
ok('冷卻 3 日內壓制', enc79TryIntercept('film_lion')===false && _played.length===0);
resetS(210); _played = [];
forcePresence('luk_baakyin','film_lion'); S.starDay.triggered = 2;
ok('每日上限 2 壓制', enc79TryIntercept('film_lion')===false && _played.length===0);
resetS(220); _played = [];
forcePresence('luk_baakyin','film_lion');
_storyOpen = [{ id:'C1', __loc:'film_lion' }];
ok('主線待播壓制：唔播＋出沒保留（doneToday 冇入帳）', (()=>{ const r = enc79TryIntercept('film_lion'); return r===false && _played.length===0 && !S.starDay.doneToday.luk_baakyin && S.stars.luk_baakyin.seen===0; })());
_storyOpen = [];
ok('主線播完後同日再入場：出沒仲喺度、可觸發', (()=>{ const r = enc79TryIntercept('film_lion'); return r===true && _played.length===1; })());

/* ---- (8) 節拍＋殺青 ---- */
resetS(30); _ys = { year:1990, season:'夏' };
ok('陸伏筆：1990 T0 開', enc79AnyBeatOpen('luk_baakyin') && enc79PickBeat('luk_baakyin').id==='luk_foreshadow');
ok('陸情報：未拼合唔開', !enc79BeatOpen('luk_baakyin', ENC79_BEATS.luk_baakyin[1]));
_merged['rumor_lu_baiyan_breakdown'] = 1;
S.stars.luk_baakyin.fav = 30;
ok('陸情報：T2＋拼合後開', enc79BeatOpen('luk_baakyin', ENC79_BEATS.luk_baakyin[1]));
resetS(40);
enc79OnWrap({ gigId:'g_test_lead', fame: 5 });
ok('殺青：同星主演 +3＋workedWith＋回望標記', S.stars.luk_baakyin.fav===3 && S.stars.luk_baakyin.workedWith===true && S.stars.luk_baakyin.wrapEcho===true);
resetS(41);
enc79OnWrap({ gigId:'g_test_lead', fame: 0 });
ok('殺青劣評減半 +1', S.stars.luk_baakyin.fav===1);

/* ---- (6) 處置表分支 ---- */
resetS(60); _ledger = null;
const _mr = Math.random;
Math.random = ()=>0.10; /* 茶：風聲路徑 */
const tea1 = enc79TeaListen({ id:'act_cha_hall_tea', moneyCost:15, source:'金龍茶餐廳' });
ok('飲茶：扣 $15＋出風聲', tea1 && tea1.ok && S.money===485 && Object.keys(S.starWhispers).length===1);
Math.random = ()=>0.90; /* 茶：碎片路徑 */
const tea2 = enc79TeaListen({ id:'act_cha_hall_tea', moneyCost:15, source:'金龍茶餐廳' });
ok('飲茶：碎片入帳（未持有）', tea2 && tea2.ok && S.mockRumors.some(r=>r.heardByAsk));
Math.random = _mr;
/* 已持有保底：將成個池標晒已聽過，兼所有星風聲開晒 → 應該冇收穫、唔收錢 */
resetS(61);
for(const f of MERGE_FRAGS) S.mockRumors.push({ id:f.id, state:'normal', heardByAsk:true });
for(const f of MOCK_RUMOR_SEEDS) S.mockRumors.push({ id:f.id, state:'normal', heardByAsk:true });
for(const c of ENC79_TEA_POOL) S.mockRumors.push({ id:c.id, state:'normal', heardByAsk:true });
S.starWhispers = {};
for(const s of ENC79_STARS) S.starWhispers[s.id] = { until: 9999, src:'tea' };
const tea3 = enc79TeaListen({ id:'act_cha_hall_tea', moneyCost:15, source:'金龍茶餐廳' });
ok('飲茶保底：全部已持有 → 唔收錢、唔出卡', tea3 && tea3.ok===false && S.money===500);
resetS(62); _ledger = null;
S.flags.enc79HelpDay = -1;
const help1 = enc79HelpClear({ id:'act_cha_help_clear' });
ok('執漏：登記老闆娘債權＋帳本計數', (()=>{ const c = S.mockCredits.find(c=>c.id.indexOf('credit_enc79_cafe_help_')===0); return help1 && help1.ok && !!c && ensureFavorLedger().credits>=1; })());
const help2 = enc79HelpClear({ id:'act_cha_help_clear' });
ok('執漏：一日一次', help2 && help2.ok===false);
resetS(63);
S.npcs.agent = 0;
const wind1 = enc79AgencyWind({ id:'act_ho_rumor' });
ok('事務所聽風聲：出真風聲＋何生人情入帳', wind1 && wind1.ok && S.npcs.agent>0 && Object.keys(S.starWhispers).length>=1);
const relAfter1 = S.npcs.agent;
const wind2 = enc79AgencyWind({ id:'act_ho_rumor' });
ok('事務所聽風聲：同日再聽只講「講完喇」但人情照加（E5 命脈）', wind2 && wind2.ok && /講完喇/.test(wind2.toast) && S.npcs.agent>relAfter1);
S.dayIndex = 64;
const wind3 = enc79AgencyWind({ id:'act_ho_rumor' });
ok('事務所聽風聲：第二日再有新風聲', wind3 && wind3.ok && !/講完喇/.test(wind3.toast));

/* ---- (7) 閘匙 defs（直接查 index 原文 MOCK_ASK 段） ---- */
const iAsk = html.indexOf('const MOCK_ASK =');
const iAskEnd = html.indexOf('let mockMergePick', iAsk);
const askSeg = html.slice(iAsk, iAskEnd);
ok('閘匙：茶餐廳三粒保留（tvb_rules／gao／曉晴）', askSeg.includes('grantsRumorId:"tvb_rules_gossip"') && askSeg.includes('grantsRumorId:"gao_steal_spotlight"') && askSeg.includes('grantsRumorId:"hau_ching_recent_news"'));
ok('閘匙：事務所采兒＋入廠守則＋還人情保留', askSeg.includes('grantsRumorId:"choi_recent_news"') && askSeg.split('grantsRumorId:"tvb_rules_gossip"').length>=3 && askSeg.includes('act_ho_repay'));
ok('處置：後巷食煙＋打招呼已刪', !askSeg.includes('act_cha_alley_smoke') && !askSeg.includes('act_ho_greet'));
ok('處置：執漏假「壓力上升」已除＋聽風聲改名', !askSeg.includes('壓力上升') && askSeg.includes('title:"聽風聲"'));

/* ---- buildScript：初遇只播定場戲（forceFirst 穿透；v79 實駕 bug 迴歸） ---- */
resetS(300);
{
  const built = enc79BuildScript('luk_baakyin', true);
  ok('初遇劇本：first 標記＋含抉擇步', !!built && built.first===true && built.steps.some(s=>s.choice && s.seg==='first:luk_baakyin'));
  ok('初遇劇本：唔混入恆常段', !!built && !built.steps.some(s=>String(s.seg||'').indexOf('opener:')===0));
  S.stars.luk_baakyin.met = true;
  const built2 = enc79BuildScript('luk_baakyin', false);
  ok('恆常劇本：opener＋節拍/日常段在位', !!built2 && built2.first===false && built2.steps.some(s=>s.seg==='opener:luk_baakyin') && built2.steps.length > 3);
  const fx = enc79ChoiceFx('first:luk_baakyin', '雙手遞返，唔多口');
  ok('初遇抉擇效果：雙手遞返 +3', !!fx && fx.fav===3);
}

/* ---- 對白數據 ---- */
const dlgCount = (o)=>{
  let n = 0;
  const walk = (x)=>{ if(Array.isArray(x)){ if(typeof x[0]==='string' && typeof x[1]==='string' && x.length===2){ n++; return; } x.forEach(walk); return; } if(x && typeof x==='object') Object.values(x).forEach(walk); };
  walk(o); return n;
};
let totalDlg = 0;
for(const sid of ['luk_baakyin','liu_bingxing','mak_zhendong','yip_manji']){
  const d = ENC79_DIALOG[sid];
  ok('對白在位：'+sid, !!d);
  if(d) totalDlg += dlgCount(d);
}
console.log('四星對白句數（lines 元素計）：' + totalDlg);
ok('四星對白總句數 >= 430', totalDlg >= 430);

console.log(fails.length ? ('\nFAILURES: ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
