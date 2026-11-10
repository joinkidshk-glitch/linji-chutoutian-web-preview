// v20a83 ENC83 邏輯測試：紅星巧遇 Phase 2（魏詠男／顧明輝／駱家聲／齊鎮海）＋ T4 提攜通用機制——
//   (1) 註冊：四星入 ENC79_PILOT／ENC79_DIALOG／ENC79_BEATS／STAGEUP／CAP／WRAP；主副場照設計表；
//   (2) 五層對白完整性＋句數（dlgCount 口徑同 enc79 測試）；
//   (3) 初遇／心聲／節拍抉擇 fx 接線（label 關鍵字對位）；
//   (4) 節拍閘：駱 E4 報紙閘、駱和音歌藝 35 閘、顧 C9 前後閘、齊站隊旗閘、魏還人情債權閘；
//   (5) 顧明輝借錢全週期：入 S.mockCredits＋favorLedger 計數＋扣錢＋due 旗 → enc83GuLoanTick 到期結算
//       （還款／壞帳兩路同種子一致、記入 S.favorDueSettled、債權移出清單、冪等）；身家太淺唔成債；
//   (6) 魏詠男大排檔 fx：扣 $150＋開債權；錢唔夠唔扣唔開；
//   (7) 齊鎮海 fx：勸停出避禍傳聞卡／沉默出撻朵傳聞卡；
//   (8) T4 提攜：八星齊（Phase 1 四星補入）——T4 先開、節拍完成 grants 入引薦債權＋帳本計數；
//   (9) 攔截：Phase 2 星喺主場真觸發；初遇劇本只播定場戲；
//   (10) 舊檔兼容：冇 news82／冇 loan 旗嘅狀態行 tick／newsOut 唔 crash。
// 反證：喺 v20a82 index 上行 → 冇 ENC83 對白／模組 → 抽取即 throw → FAIL。
// 用法：node tests/test_enc83_logic.js [path-to-index.html]
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
const LOCS = [ {id:'film_harbour', name:'海港製片廠'}, {id:'agency_ho', name:'何生事務所'}, {id:'tvb_harbour', name:'海港電視台'}, {id:'cafe_cha', name:'金龍茶餐廳'}, {id:'tvb_longmen', name:'龍門電視台'}, {id:'rec_hk', name:'香江唱片'} ];
const MERGE_FRAGS = [];
const MOCK_RUMOR_SEEDS = [];
function resetS(day){
  S = { dayIndex: day||0, fame: 0, money: 500, vocal: 0, flags: {}, npcs: { agent: 0 }, mockRumors: [], mockDebts: [], mockCredits: [], board: {}, shoots: [], mapTips: {}, news82: { pub:{}, arc:{}, echoDone:{} }, favorDueSettled: {} };
  _merged = {}; _doneNodes = new Set(); _toasts = [];
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
function softSocialDailyCap(){ return { ok:true, used:0, max:99, left:99 }; }
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

const names = ['ENC79_TIER_NAMES','ENC79_PLAYER_TIERS','ENC79_FAV_CAPS','ENC79_COOLDOWN','ENC79_DAILY_CAP','ENC79_WEEK_SOFT_CAP','ENC79_STARS','ENC79_PILOT','ENC79_DISTANCE_EXTRA','ENC79_STAGEUP','ENC79_CAP_LINES','ENC79_WRAP_ECHO','ENC79_TEA_POOL','ENC79_BEATS','ENC79_DIALOG'];
const asVar = (code, name)=> code.replace('const ' + name + ' =', 'var ' + name + ' =');
const P1 = ['luk_baakyin','liu_bingxing','mak_zhendong','yip_manji'];
const P2 = ['ngai_wingnaam','gu_mingfai','lok_gasing','chai_zanhoi'];
const consts = names.map(n=> asVar(extractConst(n), n)).join('\n')
  + '\n' + P1.map(sid=>{ const cn = (sid==='yip_manji') ? 'yip_manzi' : sid; return asVar(extractDlg('ENC79_DLG_' + cn), 'ENC79_DLG_' + cn) + '\nENC79_DIALOG["' + sid + '"] = ENC79_DLG_' + cn + ';'; }).join('\n')
  + '\n' + P2.map(sid=> asVar(extractDlg('ENC83_DLG_' + sid), 'ENC83_DLG_' + sid) + '\n' + asVar(extractDlg('ENC83_FRAME_' + sid), 'ENC83_FRAME_' + sid)).join('\n');
const fns = ['ensureFavorDueSettled','enc79StarDef','enc79LocName','enc79Hash','enc79Rand','enc79EnsureStars','enc79StarState','enc79TierOf','enc79PlayerTier','enc79FavCap','enc79AddFav','enc79InWindow','enc79WhisperActive','enc79PresenceP','enc79EnsureDay','enc79PresenceAt','enc79GrantWhisper','enc79GrantFrag','enc79GrantRumorCard','enc79GrantCredit','enc79HasMerged','enc79BoardHasStar','enc79BoardHasActionGig','enc79BeatOpen','enc79AnyBeatOpen','enc79PickBeat','enc79ChoiceFx','enc79RunChoiceFx','enc79NormSeg','enc79StoryPendingAt','enc79TryIntercept','enc79DistanceLook','enc79OnWrap','enc79PaperWhisper','enc79HoTrustLine','enc79HelpAvailable','enc79MockAskBranch','enc79PayTea','enc79TeaListen','enc79HelpClear','enc79AgencyWind','enc79BuildScript'];
const iMod = html.indexOf('/* ===== v20a83 ENC83：紅星巧遇 Phase 2');
const iModEnd = html.indexOf('/* ===== ENC83 模組完 ===== */', iMod);
if(iMod < 0 || iModEnd < 0) throw new Error('ENC83 module not found');
const mod83 = html.slice(iMod, iModEnd);
eval(consts + '\n' + fns.map(extractFn).join('\n') + '\n' + mod83);

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
  && enc79StarDef('ngai_wingnaam').primary==='film_harbour' && enc79StarDef('ngai_wingnaam').secondary==='agency_ho'
  && enc79StarDef('gu_mingfai').primary==='tvb_harbour' && enc79StarDef('gu_mingfai').secondary==='cafe_cha'
  && enc79StarDef('lok_gasing').primary==='tvb_longmen' && enc79StarDef('lok_gasing').secondary==='rec_hk'
  && enc79StarDef('chai_zanhoi').primary==='tvb_longmen' && enc79StarDef('chai_zanhoi').secondary==='tvb_harbour');
ok('四星入試點盤（PILOT 八星齊）', P2.every(sid=>ENC79_PILOT[sid]===1) && P1.every(sid=>ENC79_PILOT[sid]===1));
ok('四星對白／節拍表／框架句註冊齊', P2.every(sid=> !!ENC79_DIALOG[sid] && Array.isArray(ENC79_BEATS[sid]) && Array.isArray(ENC79_STAGEUP[sid]) && ENC79_STAGEUP[sid].length===3));
ok('CAP／WRAP 係扁平句對（唔嵌套）', P2.every(sid=> Array.isArray(ENC79_CAP_LINES[sid]) && typeof ENC79_CAP_LINES[sid][0]==='string' && typeof ENC79_CAP_LINES[sid][1]==='string' && Array.isArray(ENC79_WRAP_ECHO[sid]) && typeof ENC79_WRAP_ECHO[sid][0]==='string'));
ok('出沒窗：魏 1991 春 P 升 75%', (()=>{ _ys={year:1991,season:'春'}; resetS(0); return enc79PresenceP(enc79StarDef('ngai_wingnaam'), 0).p>=0.75; })());
ok('出沒窗外：齊 1991 春得基礎 50%', (()=>{ _ys={year:1991,season:'春'}; resetS(0); return enc79PresenceP(enc79StarDef('chai_zanhoi'), 0).p===0.5; })());

/* ---- (2) 五層完整性＋句數 ---- */
const EXPECT_BEATS = {
  ngai_wingnaam: ['ngai_intel','ngai_help','ngai_repay','ngai_patron'],
  gu_mingfai: ['gu_foreshadow','gu_tease','gu_loan','gu_after_repay','gu_after_default','gu_n10after','gu_patron'],
  lok_gasing: ['lok_foreshadow','lok_intel','lok_help','lok_recover','lok_e4grudge','lok_patron'],
  chai_zanhoi: ['chai_intel','chai_choice','chai_repay','chai_patron'],
};
let total83 = 0;
for(const sid of P2){
  const D = ENC79_DIALOG[sid];
  const c = dlgCount(D); total83 += c;
  ok('五層完整：'+sid, !!D && D.first && D.first.lines.length>=5 && D.first.choices.length===3
    && ['T0','T1','T2','T3','T4'].every(t=> D.openers && D.openers[t] && D.openers[t].length>=2)
    && ['extra','support','lead','king'].every(k=> D.address && Array.isArray(D.address[k]))
    && D.heart && D.heart.lines.length>=5 && D.heart.choices.length===2
    && ['T1','T2','T3'].every(t=> D.pool && Array.isArray(D.pool[t]) && D.pool[t].length>=2));
  ok('節拍表順序＋對白節拍齊：'+sid, JSON.stringify((ENC79_BEATS[sid]||[]).map(b=>b.id))===JSON.stringify(EXPECT_BEATS[sid])
    && EXPECT_BEATS[sid].every(bid=> D.beats && D.beats[bid] && (D.beats[bid].lines||[]).length>=3));
  ok('句數 >= 115：'+sid+'（'+c+'）', c>=115);
}
console.log('Phase 2 四星對白句數（lines 元素計）：' + total83);
ok('四星總句數 >= 480', total83>=480);

/* ---- (3) 抉擇 fx 接線 ---- */
ok('初遇 fx：魏汽水 +5／紙巾 +1／行開 -2', enc79ChoiceFx('first:ngai_wingnaam','拎支汽水俾佢，陪佢坐一陣').fav===5 && enc79ChoiceFx('first:ngai_wingnaam','放低包紙巾就走，唔打擾').fav===1 && enc79ChoiceFx('first:ngai_wingnaam','當冇睇到，行開算').fav===-2);
ok('初遇 fx：顧聽歌 +3／齊答得出 +3／駱撐 +3', enc79ChoiceFx('first:gu_mingfai','靜靜企喺度，聽佢哼埋嗰段舊歌').fav===3 && enc79ChoiceFx('first:chai_zanhoi','一口答得出：左三步，望返城門').fav===3 && enc79ChoiceFx('first:lok_gasing','出聲撐佢一句：啲歌係好聽嘅').fav===3);
ok('心聲 fx：顧陪到天光 +3', enc79ChoiceFx('heart:gu_mingfai','陪佢坐到天光，唔出聲').fav===3);
ok('借錢 fx：一口應承 → gu_loan_full／借一半 → gu_loan_half', (()=>{ const a=enc79ChoiceFx('beat:gu_loan','借，一口應承'); const b=enc79ChoiceFx('beat:gu_loan','借一半，留返啲畀自己'); const c=enc79ChoiceFx('beat:gu_loan','唔借，呢筆錢我真係幫唔到'); return a.fx==='gu_loan_full' && a.fav===4 && b.fx==='gu_loan_half' && b.fav===2 && !c.fx && c.fav===-2; })());

/* ---- (4) 節拍閘 ---- */
resetS(100); _ys = { year:1992, season:'秋' }; setFav('lok_gasing', 10);
ok('駱 E4 閘：報紙未出 → 唔忿拍唔開', enc79BeatOpen('lok_gasing', beatOf('lok_gasing','lok_e4grudge'))===false);
S.news82.pub.E4 = 1015;
ok('駱 E4 閘：E4 刊出後 → 開', enc79BeatOpen('lok_gasing', beatOf('lok_gasing','lok_e4grudge'))===true);
resetS(101); setFav('lok_gasing', 45); S.vocal = 34;
ok('駱和音閘：歌藝 34 唔開', enc79BeatOpen('lok_gasing', beatOf('lok_gasing','lok_help'))===false);
S.vocal = 35;
ok('駱和音閘：歌藝 35 開', enc79BeatOpen('lok_gasing', beatOf('lok_gasing','lok_help'))===true);
resetS(102); _ys = { year:1991, season:'秋' }; setFav('gu_mingfai', 25);
ok('顧 C9 閘：C9 未完 → 預告拍開、N10 後續拍唔開', enc79BeatOpen('gu_mingfai', beatOf('gu_mingfai','gu_tease'))===true && enc79BeatOpen('gu_mingfai', beatOf('gu_mingfai','gu_n10after'))===false);
_doneNodes.add('C9');
ok('顧 C9 閘：C9 完成 → 預告拍收、後續拍開', enc79BeatOpen('gu_mingfai', beatOf('gu_mingfai','gu_tease'))===false && enc79BeatOpen('gu_mingfai', beatOf('gu_mingfai','gu_n10after'))===true);
resetS(103); setFav('chai_zanhoi', 25);
ok('齊回收閘：未站隊唔開', enc79BeatOpen('chai_zanhoi', beatOf('chai_zanhoi','chai_repay'))===false);
S.flags.flag_side_tv = 1;
ok('齊回收閘：站隊旗（flag_side_tv）開', enc79BeatOpen('chai_zanhoi', beatOf('chai_zanhoi','chai_repay'))===true);
resetS(104); setFav('ngai_wingnaam', 25);
ok('魏還人情閘：冇大排檔債權唔開', enc79BeatOpen('ngai_wingnaam', beatOf('ngai_wingnaam','ngai_repay'))===false);
S.mockCredits.push({ id:'credit_enc83_ngai_meal', debtor:'魏詠男' });
ok('魏還人情閘：有債權開', enc79BeatOpen('ngai_wingnaam', beatOf('ngai_wingnaam','ngai_repay'))===true);

/* ---- (5) 顧明輝借錢全週期 ---- */
resetS(400); _ys = { year:1991, season:'秋' }; _ledger = null; S.money = 2000;
enc79RunChoiceFx(enc79ChoiceFx('beat:gu_loan','借，一口應承').fx);
ok('借錢：扣身家 20%（$400）＋債權入 mockCredits＋帳本計數＋due 旗', S.money===1600
  && S.mockCredits.some(c=>c.id==='credit_enc83_gu_loan')
  && ensureFavorLedger().credits>=1
  && S.flags.enc83_gu_loan_amt===400 && S.flags.enc83_gu_loan_due===428);
S.dayIndex = 410; enc83GuLoanTick();
ok('借錢：未到期唔結算', !S.flags.enc83_gu_loan_result && S.mockCredits.some(c=>c.id==='credit_enc83_gu_loan'));
S.dayIndex = 428; enc83GuLoanTick();
const expectRepay = enc79Rand('gu83loan:400') < 0.3;
ok('借錢到期：結算記入 favorDueSettled＋債權移出清單', !!S.favorDueSettled['credit_enc83_gu_loan'] && !S.mockCredits.some(c=>c.id==='credit_enc83_gu_loan'));
ok('借錢到期：結果同種子一致（'+(expectRepay?'還款':'壞帳')+'路）', expectRepay
  ? (S.flags.enc83_gu_loan_result===1 && S.favorDueSettled['credit_enc83_gu_loan'].result==='repaid_loan' && S.money===2000 && S.mockRumors.some(r=>r.id==='rumor_gu_loan_repaid'))
  : (S.flags.enc83_gu_loan_result===2 && S.favorDueSettled['credit_enc83_gu_loan'].result==='void_loan' && S.money===1600 && S.mockRumors.some(r=>r.id==='rumor_gu_loan_gone')));
const moneyAfterSettle = S.money; enc83GuLoanTick();
ok('借錢：重複 tick 冪等（唔重複結算）', S.money===moneyAfterSettle);
resetS(500); S.money = 2000;
enc79RunChoiceFx(enc79ChoiceFx('beat:gu_loan','借一半，留返啲畀自己').fx);
ok('借一半：金額減半 $200＋lvl 旗', S.money===1800 && S.flags.enc83_gu_loan_amt===200 && S.flags.enc83_gu_loan_lvl===2);
resetS(600); S.money = 100;
enc79RunChoiceFx(enc79ChoiceFx('beat:gu_loan','借，一口應承').fx);
ok('身家太淺（$100→借出 $20 < $50）：唔成債、唔扣錢', S.money===100 && !S.mockCredits.some(c=>c.id==='credit_enc83_gu_loan') && !S.flags.enc83_gu_loan_due);

/* ---- (6) 魏大排檔 fx ---- */
resetS(700); S.money = 500;
enc79RunChoiceFx('ngai_meal');
ok('大排檔：扣 $150＋開債權 credit_enc83_ngai_meal', S.money===350 && S.mockCredits.some(c=>c.id==='credit_enc83_ngai_meal'));
resetS(701); S.money = 100;
enc79RunChoiceFx('ngai_meal');
ok('大排檔：錢唔夠 $150 → 唔扣唔開債權', S.money===100 && !S.mockCredits.some(c=>c.id==='credit_enc83_ngai_meal'));

/* ---- (7) 齊 fx 傳聞卡 ---- */
resetS(710);
enc79RunChoiceFx('chai_advise');
ok('齊勸停：出避禍傳聞卡', S.mockRumors.some(r=>r.id==='rumor_chai_drama_dodged'));
resetS(711);
enc79RunChoiceFx('chai_silent');
ok('齊沉默：出撻朵傳聞卡', S.mockRumors.some(r=>r.id==='rumor_chai_drama_flop'));

/* ---- (8) T4 提攜（八星） ---- */
const PATRON_BEAT = { luk_baakyin:'luk_patron', liu_bingxing:'liu_patron', mak_zhendong:'mak_patron', yip_manji:'yip_patron', ngai_wingnaam:'ngai_patron', gu_mingfai:'gu_patron', lok_gasing:'lok_patron', chai_zanhoi:'chai_patron' };
const PATRON_CREDIT = { luk_baakyin:'credit_enc83_luk_patron', liu_bingxing:'credit_enc83_liu_patron', mak_zhendong:'credit_enc83_mak_patron', yip_manji:'credit_enc83_yip_patron', ngai_wingnaam:'credit_enc83_ngai_patron', gu_mingfai:'credit_enc83_gu_patron', lok_gasing:'credit_enc83_lok_patron', chai_zanhoi:'credit_enc83_chai_patron' };
for(const sid of P1.concat(P2)){
  resetS(800); _ledger = null; setFav(sid, 45);
  ok('提攜 T3 未開：'+sid, enc79BeatOpen(sid, beatOf(sid, PATRON_BEAT[sid]))===false);
  setFav(sid, 70);
  const st = S.stars[sid];
  for(const b of (ENC79_BEATS[sid]||[])) if(!b.id.endsWith('_patron')) st.beatsDone[b.id] = true;
  const picked = enc79PickBeat(sid);
  ok('提攜 T4 開＋排鏈節拍之後：'+sid, !!picked && picked.id===PATRON_BEAT[sid]);
  if(picked && picked.grants) picked.grants();
  ok('提攜入帳：引薦債權＋帳本計數：'+sid, S.mockCredits.some(c=>c.id===PATRON_CREDIT[sid]) && ensureFavorLedger().credits>=1);
  const D = ENC79_DIALOG[sid];
  ok('提攜對白在位：'+sid, !!D && !!D.beats && Object.keys(D.beats).some(k=>k.endsWith('_patron') && (D.beats[k].lines||[]).length>=5));
}

/* ---- (9) 攔截＋初遇劇本 ---- */
resetS(900); _ys = { year:1991, season:'春' }; _played = [];
forcePresence('ngai_wingnaam','film_harbour');
ok('攔截：魏詠男主場真觸發', enc79TryIntercept('film_harbour')===true && _played.length===1 && _played[0][0]==='ngai_wingnaam' && S.stars.ngai_wingnaam.seen===1);
resetS(901);
{
  const built = enc79BuildScript('gu_mingfai', true);
  ok('初遇劇本：顧明輝 first 標記＋抉擇步＋唔混恆常段', !!built && built.first===true && built.steps.some(s=>s.choice && s.seg==='first:gu_mingfai') && !built.steps.some(s=>String(s.seg||'').indexOf('opener:')===0));
}

/* ---- (10) 舊檔兼容 ---- */
resetS(950); delete S.news82; delete S.favorDueSettled;
ok('舊檔：冇 news82 行 enc83NewsOut 唔 crash 回 false', (()=>{ try{ return enc83NewsOut('E4')===false; }catch(e){ return false; } })());
ok('舊檔：冇 loan 旗行 enc83GuLoanTick 唔 crash', (()=>{ try{ enc83GuLoanTick(); return true; }catch(e){ return false; } })());

console.log(fails.length ? ('\nFAILURES: ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
