// v20a84 ENC84 邏輯測試：紅星巧遇 Phase 3（彭少祺／蘇芷茵／鍾楚凝／程天諾）＋全系統回收——
//   (1) 註冊：四星入 ENC79_PILOT（12 星齊）／ENC79_DIALOG／ENC79_BEATS／STAGEUP／CAP／WRAP；主副場照設計表；
//   (2) 五層對白完整性＋句數（dlgCount 口徑同 enc79/83 測試）；
//   (3) 初遇／心聲／節拍抉擇 fx 接線（label 關鍵字對位）＋實效（慈善債權／收斂凍結旗／緋聞卡）；
//   (4) 節拍閘：彭 C10 閘＋N17 窗、蘇低級數閘＋合作閘、鍾 F 伏筆段閘＋告別窗、程 E4 報紙閘＋C16 雙旗回收；
//   (5) 彭少祺樞紐：T1 起每次巧遇恆常漏料生風聲；T0 唔漏；他星 T1 唔漏；漏料目標唔揀未解鎖星（程 1992 前）；
//   (6) 程天諾出沒：1992 前 P＝0（enc79PresenceP＋逐日種子盤）；1992 春基礎 50%、秋窗 75%；
//   (7) 鍾楚凝：1992 秋／冬 P 降 25%、1991 秋窗 75%、1992 春基礎 50%；
//   (8) 蘇芷茵收斂凍結：旗在期內主場在場都唔觸發；冇旗照常觸發；
//   (9) T4 回收：12 星 patron 節拍齊（排表尾、T4 先開、grants 入引薦債權）；
//   (10) 人脈頁回收：未遇 12 行剪影（？？？＋範疇）、已遇出行名／段名／主場；
//   (11) 舊檔兼容：冇 stars／whispers／news82 嘅狀態唔 crash。
// 反證：喺 v20a83 index 上行 → 冇 ENC84 對白／模組 → 抽取即 throw → FAIL。
// 用法：node tests/test_enc84_logic.js [path-to-index.html]
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
function extractDlg(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('missing ' + name);
  const j = html.indexOf('\nconst ', i + 10);
  return html.slice(i, j < 0 ? undefined : j);
}
/* ---- sandbox ---- */
let S;
let _merged = {};
let _week = 3;
let _ys = { year: 1990, season: '春' };
let _storyOpen = [];
let _doneNodes = new Set();
let _toasts = [];
const GIGS = [
  { id:'g_test_lead', roleScale:'film_lead_big', leadStarId:'luk_baakyin', genreLabel:'劇情片', type:'電影', title:'測試主角戲', workTitle:'測試主角戲' },
];
const LOCS = [ {id:'film_harbour', name:'維港電影'}, {id:'agency_ho', name:'何生事務所'}, {id:'tvb_harbour', name:'海港廣播'}, {id:'cafe_cha', name:'金龍茶餐廳'}, {id:'tvb_longmen', name:'星河電視台'}, {id:'rec_hk', name:'香江唱片'}, {id:'ad_central', name:'中環廣告'}, {id:'rec_wanchai', name:'灣仔唱片'}, {id:'rec_star', name:'天星音樂'}, {id:'ad_adm', name:'金鐘創意'}, {id:'film_lion', name:'獅子山製片'}, {id:'film_cotton', name:'紅棉影業'}, {id:'tvb_kowloon', name:'九龍電視台'} ];
const MERGE_FRAGS = [];
const MOCK_RUMOR_SEEDS = [];
function resetS(day){
  S = { dayIndex: day||0, fame: 0, money: 500, vocal: 0, flags: {}, npcs: { agent: 0 }, mockRumors: [], mockDebts: [], mockCredits: [], board: {}, shoots: [], mapTips: {}, news82: { pub:{}, arc:{}, echoDone:{} }, favorDueSettled: {} };
  _merged = {}; _doneNodes = new Set(); _toasts = []; _ledger = null;
}
function weekNumNow(){ return _week; }
function yearSeasonNow(){ return _ys; }
function hasMergedIntel(id){ return !!_merged[id]; }
function ensureMockJournal(){ if(!Array.isArray(S.mockRumors)) S.mockRumors=[]; if(!Array.isArray(S.mockDebts)) S.mockDebts=[]; }
function syncNotebookMirror(){}
function saveQ(){}
function refreshMoneyHud(){}
function noteWeekHighlight(){}
function toast(t){ _toasts.push(String(t)); }
function rumorStateLabel(state){ return ({ normal:'剛聽聞', fresh:'剛聽聞', teased:'已知', merged:'已拼合' })[String(state||'normal')] || '剛聽聞'; }
function R(a,b){ return a; }
function bumpNpc(id, d){ const b = S.npcs[id]||0; S.npcs[id] = Math.min(100, b+d); return S.npcs[id]-b; }
let _ledger = null;
function ensureFavorLedger(){ if(!_ledger) _ledger = { settled:0, credits:0, exodus:[], counted:{} }; return _ledger; }
function favorLedgerNoteCredit(id){ const L = ensureFavorLedger(); if(L.counted[id]) return false; L.counted[id]={kind:'credit'}; L.credits++; return true; }
function ensureFavorDueSettled(){ if(!S.favorDueSettled) S.favorDueSettled = {}; return S.favorDueSettled; }
function softSocialDailyCap(){ return { ok:true }; }
function softSocialDailyUse(){}
function softPreviewOn(){ return false; }
function ending78Gate(){ return false; }
function npcNextTierHint(){ return null; }
const BehaviorGate = { featureFlag_softBehaviorGatePreview: ()=>false };
const StoryOC = {
  isDone: (id)=>_doneNodes.has(id),
  listOpen: ()=>({ open: _storyOpen }),
  findNodeRaw: (id)=>({ id, __loc: (_storyOpen.find(r=>r.id===id)||{}).__loc }),
};
function storyNodeLocId(n){ return n && n.__loc; }
let _played = [];
function enc79PlayEncounter(sid, loc, wasMet){ _played.push([sid, loc, wasMet]); }

const names = ['ENC79_TIER_NAMES','ENC79_PLAYER_TIERS','ENC79_FAV_CAPS','ENC79_COOLDOWN','ENC79_DAILY_CAP','ENC79_WEEKLY_CAP','ENC79_WEEK_SOFT_CAP','ENC79_STARS','ENC79_PILOT','ENC79_DISTANCE_EXTRA','ENC79_STAGEUP','ENC79_CAP_LINES','ENC79_WRAP_ECHO','ENC79_TEA_POOL','ENC79_BEATS','ENC79_DIALOG'];
const asVar = (code, name)=> code.replace('const ' + name + ' =', 'var ' + name + ' =');
const P1 = ['luk_baakyin','liu_bingxing','mak_zhendong','yip_manji'];
const P2 = ['ngai_wingnaam','gu_mingfai','lok_gasing','chai_zanhoi'];
const P3 = ['pang_siuki','so_jiyan','chung_choning','ching_tinlok'];
const ALL = P1.concat(P2, P3);
const consts = names.map(n=> asVar(extractConst(n), n)).join('\n')
  + '\n' + P1.map(sid=>{ const cn = (sid==='yip_manji') ? 'yip_manzi' : sid; return asVar(extractDlg('ENC79_DLG_' + cn), 'ENC79_DLG_' + cn) + '\nENC79_DIALOG["' + sid + '"] = ENC79_DLG_' + cn + ';'; }).join('\n')
  + '\n' + P2.map(sid=> asVar(extractDlg('ENC83_DLG_' + sid), 'ENC83_DLG_' + sid) + '\n' + asVar(extractDlg('ENC83_FRAME_' + sid), 'ENC83_FRAME_' + sid)).join('\n')
  + '\n' + P3.map(sid=> asVar(extractDlg('ENC84_DLG_' + sid), 'ENC84_DLG_' + sid) + '\n' + asVar(extractDlg('ENC84_FRAME_' + sid), 'ENC84_FRAME_' + sid)).join('\n');
const fns = ['ensureFavorDueSettled','enc79StarDef','enc79LocName','enc79Hash','enc79Rand','enc79EnsureStars','enc79StarState','enc79TierOf','enc79PlayerTier','enc79FavCap','enc79AddFav','enc79InWindow','enc79WhisperActive','enc79PresenceP','enc79EnsureDay','enc79PresenceAt','enc79GrantWhisper','enc79GrantFrag','enc79GrantRumorCard','enc79GrantCredit','enc79HasMerged','enc79BoardHasStar','enc79BoardHasActionGig','enc79BeatOpen','enc79AnyBeatOpen','enc79PickBeat','enc79ChoiceFx','enc79RunChoiceFx','enc79NormSeg','enc79StoryPendingAt','enc79TryIntercept','enc79DistanceLook','enc79OnWrap','enc79PaperWhisper','enc79HoTrustLine','enc79HelpAvailable','enc79MockAskBranch','enc79PayTea','enc79TeaListen','enc79HelpClear','enc79AgencyWind','enc79BuildScript','enc79PeopleHtml','enc79StandCandidates','enc79SheetPresence'];
const iMod83 = html.indexOf('/* ===== v20a83 ENC83：紅星巧遇 Phase 2');
const iMod83End = html.indexOf('/* ===== ENC83 模組完 ===== */', iMod83);
if(iMod83 < 0 || iMod83End < 0) throw new Error('ENC83 module not found');
const mod83 = html.slice(iMod83, iMod83End);
const iMod84 = html.indexOf('/* ===== v20a84 ENC84：紅星巧遇 Phase 3');
const iMod84End = html.indexOf('/* ===== ENC84 模組完 ===== */', iMod84);
if(iMod84 < 0 || iMod84End < 0) throw new Error('ENC84 module not found');
const mod84 = html.slice(iMod84, iMod84End);
/* v20a112 ICONS112：enc79PeopleHtml 用 favDots112，沙盒要一併載入對照＋helper。 */
eval(extractConst('EMOJI_ICON112').replace('const EMOJI_ICON112 =', 'var EMOJI_ICON112 ='));
eval(extractFn('iconHtml112'));
eval(extractFn('favDots112'));
eval(consts + '\n' + fns.map(extractFn).join('\n') + '\n' + mod83 + '\n' + mod84);

const dlgCount = (o)=>{
  let n = 0;
  const walk = (x)=>{ if(Array.isArray(x)){ if(typeof x[0]==='string' && typeof x[1]==='string' && x.length===2){ n++; return; } x.forEach(walk); return; } if(x && typeof x==='object') Object.values(x).forEach(walk); };
  walk(o); return n;
};
function forcePresence(sid, loc){ S.starDay = { day: S.dayIndex, presence: { [loc]: [sid] }, triggered: 0, doneToday: {} }; }
function beatOf(sid, bid){ return (ENC79_BEATS[sid]||[]).find(b=>b.id===bid); }
function setFav(sid, fav){ enc79EnsureStars(); S.stars[sid].fav = fav; }

/* ---- (1) 註冊 ---- */
ok('名冊仍 12 星＋四星主副場照設計表', ENC79_STARS.length===12
  && enc79StarDef('pang_siuki').primary==='ad_central' && enc79StarDef('pang_siuki').secondary==='tvb_longmen'
  && enc79StarDef('so_jiyan').primary==='rec_wanchai' && enc79StarDef('so_jiyan').secondary==='ad_central'
  && enc79StarDef('chung_choning').primary==='rec_star' && enc79StarDef('chung_choning').secondary==='ad_adm'
  && enc79StarDef('ching_tinlok').primary==='rec_star' && enc79StarDef('ching_tinlok').secondary==='rec_hk'
  && enc79StarDef('ching_tinlok').unlockYear===1992);
ok('試點盤 12 星齊（PILOT 全開）', ALL.every(sid=>ENC79_PILOT[sid]===1) && Object.keys(ENC79_PILOT).length===12);
ok('四星對白／節拍表／框架句註冊齊', P3.every(sid=> !!ENC79_DIALOG[sid] && Array.isArray(ENC79_BEATS[sid]) && Array.isArray(ENC79_STAGEUP[sid]) && ENC79_STAGEUP[sid].length===3));
ok('CAP／WRAP 係扁平句對（唔嵌套）', P3.every(sid=> Array.isArray(ENC79_CAP_LINES[sid]) && typeof ENC79_CAP_LINES[sid][0]==='string' && typeof ENC79_CAP_LINES[sid][1]==='string' && Array.isArray(ENC79_WRAP_ECHO[sid]) && typeof ENC79_WRAP_ECHO[sid][0]==='string'));

/* ---- (2) 五層完整性＋句數 ---- */
const EXPECT_BEATS = {
  pang_siuki: ['pang_intel','pang_help','pang_n17','pang_patron'],
  so_jiyan: ['so_intel','so_risk','so_wrap','so_patron'],
  chung_choning: ['chung_review','chung_intel','chung_f_clue','chung_farewell','chung_patron'],
  ching_tinlok: ['ching_e4','ching_rival','ching_after_train','ching_after_polish','ching_patron'],
};
let total84 = 0;
for(const sid of P3){
  const D = ENC79_DIALOG[sid];
  const c = dlgCount(D); total84 += c;
  ok('五層完整：'+sid, !!D && D.first && D.first.lines.length>=5 && D.first.choices.length===3
    && ['T0','T1','T2','T3','T4'].every(t=> D.openers && D.openers[t] && D.openers[t].length>=2)
    && ['extra','support','lead','king'].every(k=> D.address && Array.isArray(D.address[k]))
    && D.heart && D.heart.lines.length>=5 && D.heart.choices.length===2
    && ['T1','T2','T3'].every(t=> D.pool && Array.isArray(D.pool[t]) && D.pool[t].length>=2));
  ok('節拍表順序＋對白節拍齊：'+sid, JSON.stringify((ENC79_BEATS[sid]||[]).map(b=>b.id))===JSON.stringify(EXPECT_BEATS[sid])
    && EXPECT_BEATS[sid].every(bid=> D.beats && D.beats[bid] && (D.beats[bid].lines||[]).length>=3));
  ok('句數 >= 115：'+sid+'（'+c+'）', c>=115);
}
console.log('Phase 3 四星對白句數（lines 元素計）：' + total84);
ok('四星總句數 >= 480', total84>=480);

/* ---- (3) 抉擇 fx 接線＋實效 ---- */
ok('初遇 fx：彭記性 +3／指教 +1／客套 -2', enc79ChoiceFx('first:pang_siuki','佩服佢記性：彭生，你記性真係冇得頂').fav===3 && enc79ChoiceFx('first:pang_siuki','客氣回應：係呀，我係阿偉，多多指教').fav===1 && enc79ChoiceFx('first:pang_siuki','覺得太假：唔使咁客套啦').fav===-2);
ok('初遇 fx：蘇護住 +3／讓開 +1／介紹 -2', enc79ChoiceFx('first:so_jiyan','護住佢入升降機，一句都唔多講').fav===3 && enc79ChoiceFx('first:so_jiyan','讓開企埋一邊，唔阻人做嘢').fav===1 && enc79ChoiceFx('first:so_jiyan','趁機介紹自己，想攞個機會').fav===-2);
ok('初遇 fx：鍾受教 +3／點頭 +1／頂返 -2', enc79ChoiceFx('first:chung_choning','企正啲，虛心受教：多謝鍾小姐指點').fav===3 && enc79ChoiceFx('first:chung_choning','點頭多謝，唔出聲').fav===1 && enc79ChoiceFx('first:chung_choning','唔忿氣，頂返佢一句').fav===-2);
ok('初遇 fx：程練到天光 +3／遞支水 +1／笑佢 -2', enc79ChoiceFx('first:ching_tinlok','講自己當年點捱：俾人笑嗰陣，我都係練到天光').fav===3 && enc79ChoiceFx('first:ching_tinlok','靜靜遞支水俾佢，唔出聲').fav===1 && enc79ChoiceFx('first:ching_tinlok','笑佢唱功：你唱嗰兩句真係唔掂').fav===-2);
ok('心聲 fx：四星最佳 +3／次選 +1', enc79ChoiceFx('heart:pang_siuki','靜靜聽佢講晒').fav===3 && enc79ChoiceFx('heart:pang_siuki','笑住話佢諗多咗').fav===1
  && enc79ChoiceFx('heart:so_jiyan','認真同佢講：你做得到').fav===3 && enc79ChoiceFx('heart:so_jiyan','笑住話佢諗太多').fav===1
  && enc79ChoiceFx('heart:chung_choning','靜靜聽，唔出聲').fav===3 && enc79ChoiceFx('heart:chung_choning','問佢會唔會返嚟').fav===1
  && enc79ChoiceFx('heart:ching_tinlok','企佢嗰邊：慢嗰條路先行得遠').fav===3 && enc79ChoiceFx('heart:ching_tinlok','叫佢唔好諗咁多，紅咗先算').fav===1);
ok('節拍 fx：彭幫手頂一晚 +5＋fx／嚟唔到 0', (()=>{ const a=enc79ChoiceFx('beat:pang_help','頂一晚：成晚跟到足，幫佢睇流程'); const b=enc79ChoiceFx('beat:pang_help','嗰晚有工開，嚟唔到'); return a.fav===5 && a.fx==='pang_helped' && b.fav===0; })());
ok('節拍 fx：蘇收斂 +1＋fx／唔理 -2＋fx', (()=>{ const a=enc79ChoiceFx('beat:so_risk','收斂：明白，以後保持距離，唔拖累佢'); const b=enc79ChoiceFx('beat:so_risk','唔理：行得正企得正，冇嘢好驚'); return a.fav===1 && a.fx==='so_cool' && b.fav===-2 && b.fx==='so_risk_news'; })());
resetS(300);
enc79RunChoiceFx('pang_helped');
ok('實效：慈善頂班入引薦債權＋帳本計數', S.mockCredits.some(c=>c.id==='credit_enc84_pang_charity') && ensureFavorLedger().credits>=1);
enc79RunChoiceFx('so_cool');
ok('實效：收斂 set 凍結旗（day+21）', (S.flags||{}).enc84_so_cool_until===321);
enc79RunChoiceFx('so_risk_news');
ok('實效：唔理出緋聞傳聞卡', S.mockRumors.some(r=>r.id==='rumor_so_gossip_risk'));

/* ---- (4) 節拍閘 ---- */
resetS(310); setFav('pang_siuki', 10);
ok('彭幫手閘：C10 未做唔開', enc79BeatOpen('pang_siuki', beatOf('pang_siuki','pang_help'))===false);
_doneNodes.add('C10');
ok('彭幫手閘：C10 做咗＋T1 開', enc79BeatOpen('pang_siuki', beatOf('pang_siuki','pang_help'))===true);
resetS(311); setFav('pang_siuki', 45); _ys = { year:1992, season:'秋' };
ok('彭 N17 閘：1992 秋唔開', enc79BeatOpen('pang_siuki', beatOf('pang_siuki','pang_n17'))===false);
_ys = { year:1992, season:'冬' };
ok('彭 N17 閘：1992 冬＋T3 開', enc79BeatOpen('pang_siuki', beatOf('pang_siuki','pang_n17'))===true);
resetS(312); setFav('so_jiyan', 25);
ok('蘇警告閘：T2＋阿偉臨記級開', enc79BeatOpen('so_jiyan', beatOf('so_jiyan','so_risk'))===true);
S.flags['done_g_test_lead'] = 1;
ok('蘇警告閘：阿偉升主角級後唔開（形象風險只對低級數）', enc79BeatOpen('so_jiyan', beatOf('so_jiyan','so_risk'))===false);
resetS(313); setFav('so_jiyan', 25);
ok('蘇回收閘：未合作唔開', enc79BeatOpen('so_jiyan', beatOf('so_jiyan','so_wrap'))===false);
S.stars.so_jiyan.workedWith = true;
ok('蘇回收閘：合作過＋T2 開', enc79BeatOpen('so_jiyan', beatOf('so_jiyan','so_wrap'))===true);
resetS(314); setFav('chung_choning', 45); _ys = { year:1990, season:'春' };
ok('鍾 F 伏筆閘：1990 唔開', enc79BeatOpen('chung_choning', beatOf('chung_choning','chung_f_clue'))===false);
_ys = { year:1991, season:'春' };
ok('鍾 F 伏筆閘：1991＋T3 開', enc79BeatOpen('chung_choning', beatOf('chung_choning','chung_f_clue'))===true);
setFav('chung_choning', 25); _ys = { year:1992, season:'春' };
ok('鍾告別閘：1992 春唔開', enc79BeatOpen('chung_choning', beatOf('chung_choning','chung_farewell'))===false);
_ys = { year:1992, season:'秋' };
ok('鍾告別閘：1992 秋＋T2 開', enc79BeatOpen('chung_choning', beatOf('chung_choning','chung_farewell'))===true);
resetS(315); setFav('ching_tinlok', 10); _ys = { year:1992, season:'秋' };
ok('程 E4 閘：報紙未出唔開', enc79BeatOpen('ching_tinlok', beatOf('ching_tinlok','ching_e4'))===false);
S.news82.pub.E4 = 1015;
ok('程 E4 閘：E4 刊出＋T1 開', enc79BeatOpen('ching_tinlok', beatOf('ching_tinlok','ching_e4'))===true);
ok('程競爭閘：C16 未做開', enc79BeatOpen('ching_tinlok', beatOf('ching_tinlok','ching_rival'))===true);
_doneNodes.add('C16');
ok('程競爭閘：C16 做咗唔開', enc79BeatOpen('ching_tinlok', beatOf('ching_tinlok','ching_rival'))===false);
S.flags.flag_vocal_train = 1;
ok('程回收（苦練）：服氣版開／修音版唔開', enc79BeatOpen('ching_tinlok', beatOf('ching_tinlok','ching_after_train'))===true && enc79BeatOpen('ching_tinlok', beatOf('ching_tinlok','ching_after_polish'))===false);
delete S.flags.flag_vocal_train; S.flags.flag_vocal_polish = 1;
ok('程回收（修音）：修音版開／服氣版唔開', enc79BeatOpen('ching_tinlok', beatOf('ching_tinlok','ching_after_polish'))===true && enc79BeatOpen('ching_tinlok', beatOf('ching_tinlok','ching_after_train'))===false);
resetS(316);
ok('節拍 grants：情報／伏筆／忠告／預知卡齊入傳聞池', (()=>{ 
  beatOf('pang_siuki','pang_intel').grants(); beatOf('so_jiyan','so_intel').grants();
  beatOf('chung_choning','chung_intel').grants(); beatOf('chung_choning','chung_f_clue').grants();
  beatOf('chung_choning','chung_farewell').grants(); beatOf('ching_tinlok','ching_rival').grants();
  const ids = S.mockRumors.map(r=>r.id);
  return ['rumor_pang_show_tip','rumor_so_ad_tip','rumor_chung_director_tip','rumor_chung_canada_heard','rumor_chung_advice','rumor_ching_rehearse'].every(id=>ids.indexOf(id)>=0);
})());

/* ---- (5) 彭少祺樞紐 ---- */
resetS(400); _ys = { year:1991, season:'春' };
enc79EnsureStars(); S.stars.pang_siuki.met = true; setFav('pang_siuki', 10);
{
  const built = enc79BuildScript('pang_siuki', false);
  const leak = built && built.steps.find(s=>s.seg==='leak:pang_siuki');
  ok('樞紐：彭 T1 巧遇恆常有漏料步', !!leak);
  if(leak && leak.segFx) leak.segFx();
  ok('樞紐：漏料真生風聲（whisper 窗＋風聲卡）', Object.keys(S.starWhispers||{}).length>=1 && S.mockRumors.some(r=>r.wind===true));
}
resetS(401); _ys = { year:1991, season:'春' };
enc79EnsureStars(); S.stars.pang_siuki.met = true; setFav('pang_siuki', 3);
ok('樞紐：彭 T0 唔漏', (()=>{ const b = enc79BuildScript('pang_siuki', false); return !!b && !b.steps.some(s=>s.seg==='leak:pang_siuki'); })());
resetS(402); _ys = { year:1991, season:'春' };
enc79EnsureStars(); S.stars.luk_baakyin.met = true; setFav('luk_baakyin', 10);
ok('樞紐對照：陸 T1 唔漏（恆常漏料係彭專屬）', (()=>{ const b = enc79BuildScript('luk_baakyin', false); return !!b && !b.steps.some(s=>String(s.seg||'').indexOf('leak:')===0); })());
resetS(403); _ys = { year:1991, season:'夏' };
enc79EnsureStars(); S.stars.pang_siuki.met = true; setFav('pang_siuki', 10);
for(const def of ENC79_STARS){ if(def.id!=='ching_tinlok' && def.id!=='pang_siuki') S.starWhispers[def.id] = { until: 405, src:'tea' }; }
ok('樞紐：1991 年漏料目標唔揀程天諾（未解鎖）', (()=>{ const b = enc79BuildScript('pang_siuki', false); return !!b && !b.steps.some(s=>s.seg==='leak:pang_siuki'); })());
_ys = { year:1992, season:'夏' };
{
  const built = enc79BuildScript('pang_siuki', false);
  const leak = built && built.steps.find(s=>s.seg==='leak:pang_siuki');
  ok('樞紐：1992 年漏料可指程天諾', !!leak);
  if(leak && leak.segFx) leak.segFx();
  ok('樞紐：1992 年風聲真開畀程天諾', !!enc79WhisperActive('ching_tinlok'));
}

/* ---- (6) 程天諾出沒（P＝0／種子盤） ---- */
resetS(0); _ys = { year:1991, season:'夏' };
ok('程出沒：1991 P＝0', enc79PresenceP(enc79StarDef('ching_tinlok'), 0).p===0);
_ys = { year:1992, season:'春' };
ok('程出沒：1992 春基礎 50%', enc79PresenceP(enc79StarDef('ching_tinlok'), 0).p===0.5);
_ys = { year:1992, season:'秋' };
ok('程出沒：1992 秋窗 75%', enc79PresenceP(enc79StarDef('ching_tinlok'), 0).p>=0.75);
{
  let cnt91 = 0, cnt92 = 0;
  _ys = { year:1991, season:'夏' };
  for(let d=0; d<200; d++){ S.dayIndex = d; delete S.starDay; const sd = enc79EnsureDay(); for(const loc in sd.presence) if(sd.presence[loc].indexOf('ching_tinlok')>=0) cnt91++; }
  _ys = { year:1992, season:'秋' };
  for(let d=730; d<930; d++){ S.dayIndex = d; delete S.starDay; const sd = enc79EnsureDay(); for(const loc in sd.presence) if(sd.presence[loc].indexOf('ching_tinlok')>=0) cnt92++; }
  ok('程種子盤：1991 全年 200 日零出沒', cnt91===0);
  ok('程種子盤：1992 秋 200 日有出沒（'+cnt92+' 日）', cnt92>30);
}

/* ---- (7) 鍾楚凝 P 降 ---- */
resetS(0); 
ok('鍾出沒：1991 秋窗 75%', (()=>{ _ys={year:1991,season:'秋'}; return enc79PresenceP(enc79StarDef('chung_choning'), 0).p>=0.75; })());
ok('鍾出沒：1992 春基礎 50%', (()=>{ _ys={year:1992,season:'春'}; return enc79PresenceP(enc79StarDef('chung_choning'), 0).p===0.5; })());
ok('鍾出沒：1992 秋降 25%', (()=>{ _ys={year:1992,season:'秋'}; return enc79PresenceP(enc79StarDef('chung_choning'), 0).p===0.25; })());
ok('鍾出沒：1992 冬降 25%', (()=>{ _ys={year:1992,season:'冬'}; return enc79PresenceP(enc79StarDef('chung_choning'), 0).p===0.25; })());

/* ---- (8) 蘇芷茵收斂凍結 ---- */
resetS(500); _ys = { year:1991, season:'春' }; _played = [];
enc79EnsureStars(); S.stars.so_jiyan.met = true;
forcePresence('so_jiyan','rec_wanchai');
ok('凍結：冇旗照常觸發', enc79TryIntercept('rec_wanchai')===true && _played.length===1 && _played[0][0]==='so_jiyan');
resetS(501); _ys = { year:1991, season:'春' }; _played = [];
enc79EnsureStars(); S.stars.so_jiyan.met = true;
S.flags.enc84_so_cool_until = 501 + 21;
forcePresence('so_jiyan','rec_wanchai');
ok('凍結：收斂期內在場都唔觸發', enc79TryIntercept('rec_wanchai')===false && _played.length===0);

/* ---- (9) T4 提攜 12 星回收 ---- */
const PATRON_BEAT = { luk_baakyin:'luk_patron', liu_bingxing:'liu_patron', mak_zhendong:'mak_patron', yip_manji:'yip_patron', ngai_wingnaam:'ngai_patron', gu_mingfai:'gu_patron', lok_gasing:'lok_patron', chai_zanhoi:'chai_patron', pang_siuki:'pang_patron', so_jiyan:'so_patron', chung_choning:'chung_patron', ching_tinlok:'ching_patron' };
const PATRON_CREDIT = { luk_baakyin:'credit_enc83_luk_patron', liu_bingxing:'credit_enc83_liu_patron', mak_zhendong:'credit_enc83_mak_patron', yip_manji:'credit_enc83_yip_patron', ngai_wingnaam:'credit_enc83_ngai_patron', gu_mingfai:'credit_enc83_gu_patron', lok_gasing:'credit_enc83_lok_patron', chai_zanhoi:'credit_enc83_chai_patron', pang_siuki:'credit_enc84_pang_patron', so_jiyan:'credit_enc84_so_patron', chung_choning:'credit_enc84_chung_patron', ching_tinlok:'credit_enc84_ching_patron' };
for(const sid of ALL){
  resetS(800); _ledger = null; setFav(sid, 45);
  ok('提攜 T3 未開：'+sid, enc79BeatOpen(sid, beatOf(sid, PATRON_BEAT[sid]))===false);
  setFav(sid, 70);
  const st = S.stars[sid];
  for(const b of (ENC79_BEATS[sid]||[])) if(!b.id.endsWith('_patron')) st.beatsDone[b.id] = 1;
  const picked = enc79PickBeat(sid);
  ok('提攜 T4 開＋排鏈節拍之後：'+sid, !!picked && picked.id===PATRON_BEAT[sid]);
  if(picked && picked.grants) picked.grants();
  ok('提攜入帳：引薦債權＋帳本計數：'+sid, S.mockCredits.some(c=>c.id===PATRON_CREDIT[sid]) && ensureFavorLedger().credits>=1);
  const D = ENC79_DIALOG[sid];
  ok('提攜對白在位：'+sid, !!D && !!D.beats && Object.keys(D.beats).some(k=>k.endsWith('_patron') && (D.beats[k].lines||[]).length>=5));
}

/* ---- (10) 人脈頁回收 ---- */
resetS(900); _ys = { year:1991, season:'春' };
{
  const h = enc79PeopleHtml();
  const silCount = (h.match(/？？？/g)||[]).length;
  ok('人脈頁：未遇 12 星全出剪影＋範疇', silCount===12 && h.indexOf('唱片公司嗰邊')>=0 && h.indexOf('廣告界嗰邊')>=0);
  enc79EnsureStars(); S.stars.pang_siuki.met = true; S.stars.pang_siuki.fav = 30;
  const h2 = enc79PeopleHtml();
  ok('人脈頁：已遇彭少祺出行名／段名／主場', h2.indexOf('彭少祺')>=0 && h2.indexOf('傾得埋')>=0 && h2.indexOf('中環廣告')>=0 && (h2.match(/？？？/g)||[]).length===11);
}

/* ---- (11) 舊檔兼容 ---- */
resetS(950); delete S.stars; delete S.starWhispers; delete S.news82;
ok('舊檔：冇 stars／news82 行節拍閘＋出沒盤＋初遇劇本唔 crash', (()=>{ try{
  enc79EnsureStars(); enc79EnsureDay();
  for(const sid of P3) enc79AnyBeatOpen(sid);
  const b = enc79BuildScript('ching_tinlok', true);
  return !!b && b.first===true;
} catch(e){ return false; } })());

console.log(fails.length ? ('\nFAILURES: ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
