// v20a271 支線實裝第二批邏輯測試：WORKORDER 1.10–1.17（廖／顧／麥即派分開＋交心新旗）＋陸柏言頂一晚重新設計——
//   (1) 靜態：即派對位（GRANT229 三表對 gigs_new.json 逐項核實存在＋媒介／級別／年份／角色）、
//       好感差異分支、交心旗欄位、陸 registry／DLG／tick／wrap hook／heart 閘、傳聞零殘留、舊釘位；
//   (2) 抉擇 fx：1.10／1.13／1.17 好感差異數字、陸 foreshadow 守口／講兩句、舊 fx 釘位保持；
//   (3) 節拍閘＋變體：陸冷暖 shadow＋PickBeat 排序、tease→GRANT229 派替工通告、thanks 開閘、
//       28 日唔做立 absent、heart 加閘、廖／顧 patron 變體正反兩面、陸 foreshadow 初遇變體、
//       pushSeg flags 傳遞（heart／foreshadow／first）。
// 反證：喺 pristine（v20a269）index 上行 → 靜態／fx／閘斷言乾淨 FAIL。
// 用法：node tests/test_sideline271_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const GIGS_NEW = require('../content/gigs_new.json');
const gigById = (id)=> (Array.isArray(GIGS_NEW) ? GIGS_NEW : (GIGS_NEW.gigs||[])).find(g=>g && g.id===id) || null;
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

/* ---- (1a) 靜態：即派對位（GRANT229 三表 × gigs_new.json） ---- */
const asVar = (code, name)=> code.replace('const ' + name + ' =', 'var ' + name + ' =');
eval(asVar(extractConst('GRANT229_ENC79'), 'GRANT229_ENC79') + '\n' + asVar(extractConst('GRANT229_CHOICE'), 'GRANT229_CHOICE') + '\n' + asVar(extractConst('GRANT229_DRAFT'), 'GRANT229_DRAFT'));
function enc79Rows(seg){ return GRANT229_ENC79.filter(r=>r && r.seg===seg); }
function enc79Gig(seg, keySub){
  const rows = enc79Rows(seg);
  for(const r of rows){ if(r.key && keySub && String(r.key).length && keySub.indexOf(r.key)>=0) return r.gigId; }
  const fb = rows[rows.length-1];
  return fb ? fb.gigId : null;
}
ok('對位 1.10：廖初遇三選三張唔同（tv_217／218／219）', enc79Gig('first:liu_bingxing','忍唔住笑出聲')==='gig_1990_tv_217' && enc79Gig('first:liu_bingxing','大膽講邊句橋好笑啲')==='gig_1990_tv_218' && enc79Gig('first:liu_bingxing','想攞簽名影相留念')==='gig_1990_tv_219');
ok('對位 1.10：三張皆電視劇喜劇替身雜務 1990', ['gig_1990_tv_217','gig_1990_tv_218','gig_1990_tv_219'].every(id=>{ const g=gigById(id); return g && g.type==='電視劇' && g.genre==='喜劇' && g.roleLabel==='喜劇替身雜務' && g.year===1990; }));
ok('對位 1.11：廖 Beat 2 兩邊唔同（W3_ho_liao_a tv_209／b tv_210）', GRANT229_CHOICE['W3_ho_liao:W3_ho_liao_a'] && GRANT229_CHOICE['W3_ho_liao:W3_ho_liao_b'] && GRANT229_CHOICE['W3_ho_liao:W3_ho_liao_a'].gigId==='gig_1990_tv_209' && GRANT229_CHOICE['W3_ho_liao:W3_ho_liao_b'].gigId==='gig_1990_tv_210');
ok('對位 1.11：兩張皆電視劇喜劇替身雜務 1990（廖炳星有份）', ['gig_1990_tv_209','gig_1990_tv_210'].every(id=>{ const g=gigById(id); return g && g.type==='電視劇' && g.genre==='喜劇' && g.roleLabel==='喜劇替身雜務' && g.year===1990 && JSON.stringify(g.cast||{}).indexOf('liu_bingxing')>=0; }));
ok('對位 1.13：顧初遇三選三張唔同（rec_209／201／210）', enc79Gig('first:gu_mingfai','靜靜站在那裡，聽他哼完那段舊歌')==='gig_1990_rec_209' && enc79Gig('first:gu_mingfai','點頭打個招呼，不打擾')==='gig_1990_rec_201' && enc79Gig('first:gu_mingfai','先走，不要讓人見到我和他站在一起')==='gig_1990_rec_210');
ok('對位 1.13：三張皆唱片通告初級和音歌手 1990', ['gig_1990_rec_209','gig_1990_rec_201','gig_1990_rec_210'].every(id=>{ const g=gigById(id); return g && g.type==='唱片通告' && g.tier==='初級' && g.roleLabel==='和音歌手' && g.year===1990; }));
ok('對位 1.14：顧 Beat 2 草稿兩邊唔同（rec_201／rec_207，1991 和音）', GRANT229_DRAFT.gu_promise_clean && GRANT229_DRAFT.gu_ask_back && GRANT229_DRAFT.gu_promise_clean.gigId==='gig_1991_rec_201' && GRANT229_DRAFT.gu_ask_back.gigId==='gig_1991_rec_207' && ['gig_1991_rec_201','gig_1991_rec_207'].every(id=>{ const g=gigById(id); return g && g.type==='唱片通告' && g.tier==='初級' && g.roleLabel==='和音歌手' && g.year===1991; }));
ok('對位 1.16：顧 n10after 兩邊唔同（rec_103／rec_104）', enc79Gig('beat:gu_n10after','恭喜他，終於上岸')==='gig_1992_rec_103' && enc79Gig('beat:gu_n10after','提醒他以後不要再碰賭')==='gig_1992_rec_104');
ok('對位 1.17：麥初遇三選三張唔同（film_211／213／214）', enc79Gig('first:mak_zhendong','放低支水喺佢身邊就走')==='gig_1990_film_211' && enc79Gig('first:mak_zhendong','堅持遞到佢手')==='gig_1990_film_213' && enc79Gig('first:mak_zhendong','開口問佢傷勢')==='gig_1990_film_214');
ok('對位 1.17：三張皆電影初級動作替身 1990', ['gig_1990_film_211','gig_1990_film_213','gig_1990_film_214'].every(id=>{ const g=gigById(id); return g && g.type==='電影' && g.tier==='初級' && g.roleLabel==='動作替身' && g.year===1990; }));
ok('對位 陸替工：gig_1991_tv_203 存在——電視劇初級 1991 冬替身，陸柏言男主角', (()=>{ const g=gigById('gig_1991_tv_203'); return !!g && g.type==='電視劇' && g.tier==='初級' && g.year===1991 && g.season==='冬' && g.roleLabel==='替身' && g.cast && g.cast.leadM==='luk_baakyin'; })());

/* ---- (1b) 靜態：好感分支／交心旗／陸機制在位 ---- */
ok('靜態：好感差異分支——廖 2／2／0、顧 2／1／0、麥 2／1', html.includes('if(has("好笑")) return { fav:2 }; if(has("笑出聲")) return { fav:2 }; return { fav:0 };') && html.includes('if(has("聽")) return { fav:2 }; if(has("招呼")) return { fav:1 }; return { fav:0 };') && html.includes('if(has("放低")) return { fav:2 }; /* 堅持遞到手／開口問傷勢皆 +1 */ return { fav:1 };'));
ok('靜態：交心旗欄位——廖 liu_heart_earnest／joke、顧 gu_heart_sit／quit', html.includes('flags: ["liu_heart_earnest"]') && html.includes('flags: ["liu_heart_joke"]') && html.includes('flags: ["gu_heart_sit"]') && html.includes('flags: ["gu_heart_quit"]'));
ok('靜態：陸初遇／交心旗欄位——first_quiet／pushy、confidant、kept／loose', html.includes('flags: ["luk_first_quiet"]') && html.includes('flags: ["luk_first_pushy"]') && html.includes('flags: ["luk_confidant"]') && html.includes('flags: ["luk_kept_secret"]') && html.includes('flags: ["luk_loose_talk"]'));
ok('靜態：陸 foreshadow 新抉擇 2 選項', html.includes('守口如瓶，乜都唔講') && html.includes('同人講兩句，話佢壓力大到掟嘢'));
ok('靜態：陸 registry——tease／thanks／finale_cold 在位', html.includes('{ id:"luk_tease"') && html.includes('{ id:"luk_thanks"') && html.includes('{ id:"luk_finale_cold"'));
ok('靜態：陸 tease 派 gig_1991_tv_203（GRANT229）', html.includes('grant229Record("gig_1991_tv_203", "陸柏言支線"'));
ok('靜態：陸冷版 DLG 在位（finale_cold 5 句／patron_cold 6 句）', html.includes('luk_finale_cold') && html.includes('luk_patron_cold'));
ok('靜態：陸暖版只加排除式條件（finale＋patron，無肯定式要求）', html.includes('!((S.flags||{}).luk_absent_night || (S.flags||{}).luk_loose_talk)'));
ok('靜態：陸 heart 加閘（T3＋luk_kept_secret）', html.includes('!(starId==="luk_baakyin" && !(S.flags||{}).luk_kept_secret)'));
ok('靜態：陸 absent tick 函數＋每日呼叫在位', html.includes('function enc271LukAbsentTick()') && html.includes('enc271LukAbsentTick();'));
ok('靜態：殺青 wrap 立 luk_cover_night（tv_203）', html.includes('if(sh.gigId==="gig_1991_tv_203"){ S.flags.luk_cover_night=1; delete S.flags.luk_absent_night; }'));
ok('靜態：BuildScript 變體在位——廖／顧 patron 認交心、陸 foreshadow 認初遇', html.includes('你嗰日認真回我嗰句，我收到') && html.includes('你嗰日用笑話接我嗰句') && html.includes('嗰晚你陪我坐到天光') && html.includes('把聲仲喺度，仲可以重新嚟過') && html.includes('遞返劇本嗰陣，陸柏言連望都冇望佢一眼'));
ok('靜態：傳聞引用零殘留（v267 已刪）', !html.includes('enc79GrantFrag') && !html.includes('enc79GrantRumorCard') && !html.includes('enc79HasMerged') && !html.includes('gig_intel_lu_standin'));
ok('靜態：B9 釘位——liu_repay／mak_respect beat 定義無 grants(', (()=>{ const a = html.indexOf('{ id:"liu_repay"'); const b = html.indexOf('{ id:"mak_respect"'); return a >= 0 && b >= 0 && !html.slice(a, a + 220).includes('grants(') && !html.slice(b, b + 220).includes('grants('); })());
ok('靜態：陸 intel 無傳聞閘（只讀 tier≥2）', (()=>{ const a = html.indexOf('{ id:"luk_intel"'); return a >= 0 && html.slice(a, a + 120).indexOf('enc79TierOf(st.fav)>=2') >= 0; })());

/* ---- sandbox（ENC79） ---- */
let S;
let _ys = { year: 1990, season: '春' };
let _doneNodes = new Set();
let _storyFlags = {};
function resetS(day){
  S = { dayIndex: day||0, fame: 0, money: 2000, flags: {}, npcs: { agent: 0 }, mockRumors: [], mockDebts: [], mockCredits: [], board: {}, shoots: [], mapTips: {}, story: { flags: {} }, starWeek: {}, weekGigsDone: 0, starWhispers: {}, grant229Queue: [] };
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
/* GRANT229 替工派發 stub（照 live grant229Record 語義：聽日到期、一生一次） */
function grant229Record(gigId, source, reason){
  try{
    if(!gigId || !S) return false;
    if(S.flags["grant229_recorded_"+gigId]) return false;
    S.flags["grant229_recorded_"+gigId] = 1;
    if(!Array.isArray(S.grant229Queue)) S.grant229Queue = [];
    S.grant229Queue.push({ gigId:String(gigId), source:String(source||""), reason:String(reason||""), dueDay:(S.dayIndex|0)+1, recordedDay:(S.dayIndex|0) });
    return true;
  }catch(_e){ return false; }
}

const consts271 = ['ENC79_TIER_NAMES','ENC79_PLAYER_TIERS','ENC79_FAV_CAPS','ENC79_STARS','ENC79_PILOT','ENC79_STAGEUP','ENC79_CAP_LINES','ENC79_WRAP_ECHO','ENC79_BEATS','ENC79_DIALOG','ENC79_FIRST_ALT98'].map(n=> asVar(extractConst(n), n)).join('\n')
  + '\n' + ['ENC79_DLG_luk_baakyin','ENC79_DLG_liu_bingxing','ENC79_DLG_mak_zhendong'].map(n=> asVar(extractDlg(n), n)).join('\n')
  + '\n' + asVar(extractDlg('ENC83_DLG_gu_mingfai'), 'ENC83_DLG_gu_mingfai')
  + '\nENC79_DIALOG["luk_baakyin"] = ENC79_DLG_luk_baakyin;\nENC79_DIALOG["liu_bingxing"] = ENC79_DLG_liu_bingxing;\nENC79_DIALOG["mak_zhendong"] = ENC79_DLG_mak_zhendong;\nENC79_DIALOG["gu_mingfai"] = ENC83_DLG_gu_mingfai;';
const t4Start = html.indexOf('/* ---------- T4 提攜');
const t4End = html.indexOf('/* ===== v20a84 ENC84', t4Start);
if(t4Start < 0 || t4End < 0) throw new Error('T4 region not found');
const t4Region = html.slice(t4Start, t4End);
const fns271 = ['enc79StarDef','enc79Hash','enc79Rand','enc79EnsureStars','enc79StarState','enc79TierOf','enc79PlayerTier','enc79FavCap','enc79AddFav','enc79WhisperActive','enc79GrantWhisper','enc79GrantCredit','enc79BoardHasStar','enc79BoardHasActionGig','enc79BeatOpen','enc79AnyBeatOpen','enc79PickBeat','enc79ChoiceFx','enc79RunChoiceFx','enc79NormSeg','enc79BuildScript','enc83NodeDone','enc83Flag','contra98EncFirstLocSwap','enc271LukAbsentTick'];
eval(consts271 + '\n' + t4Region + '\n' + fns271.map(extractFn).join('\n'));

/* ---- (2) 抉擇 fx ---- */
resetS(100);
ok('fx 1.10：廖初遇——笑出聲 +2／講邊句橋 +2／攞簽名影相 +0', enc79ChoiceFx('first:liu_bingxing','忍唔住笑出聲').fav===2 && enc79ChoiceFx('first:liu_bingxing','大膽講邊句橋好笑啲').fav===2 && enc79ChoiceFx('first:liu_bingxing','想攞簽名影相留念').fav===0);
ok('fx 1.13：顧初遇——聽哼舊歌 +2／點頭打招呼 +1／走先 +0', enc79ChoiceFx('first:gu_mingfai','靜靜站在那裡，聽他哼完那段舊歌').fav===2 && enc79ChoiceFx('first:gu_mingfai','點頭打個招呼，不打擾').fav===1 && enc79ChoiceFx('first:gu_mingfai','先走，不要讓人見到我和他站在一起').fav===0);
ok('fx 1.17：麥初遇——放低支水 +2／堅持遞到手 +1／開口問傷勢 +1', enc79ChoiceFx('first:mak_zhendong','放低支水喺佢身邊就走').fav===2 && enc79ChoiceFx('first:mak_zhendong','堅持遞到佢手').fav===1 && enc79ChoiceFx('first:mak_zhendong','開口問佢傷勢').fav===1);
ok('fx 陸 foreshadow：守口 +2／講兩句 -2', enc79ChoiceFx('beat:luk_foreshadow','守口如瓶，乜都唔講').fav===2 && enc79ChoiceFx('beat:luk_foreshadow','同人講兩句，話佢壓力大到掟嘢').fav===-2);
ok('fx 釘位：gu_loan 唔借 → 無 fx、fav -2', (()=>{ const c=enc79ChoiceFx('beat:gu_loan','不借，這筆錢我真的幫不了'); return !c.fx && c.fav===-2; })());
ok('fx 釘位：liu_repay／mak_respect fx＋fav 不變', (()=>{ const a=enc79ChoiceFx('beat:liu_repay','多謝受落'); const b=enc79ChoiceFx('beat:liu_repay','推辭講自己排緊期'); const c=enc79ChoiceFx('beat:mak_respect','應承隨時候命'); const d=enc79ChoiceFx('beat:mak_respect','老實講自己會驚'); return a.fx==='liu_accept' && a.fav===2 && b.fx==='liu_decline' && b.fav===1 && c.fx==='mak_accept' && c.fav===4 && d.fx==='mak_honest' && d.fav===2; })());
ok('fx 釘位：heart 廖／顧 fav 不變（笑話 1／認真 2；天亮 3／其他 1）', enc79ChoiceFx('heart:liu_bingxing','用笑話接住').fav===1 && enc79ChoiceFx('heart:liu_bingxing','認真回應').fav===2 && enc79ChoiceFx('heart:gu_mingfai','陪他坐到天亮，不出聲').fav===3);

/* ---- (3) 節拍閘 ---- */
function openBeat(sid, id){ return enc79BeatOpen(sid, beatOf(sid, id)); }
function beatIds(sid){ return (ENC79_BEATS[sid]||[]).map(b=>b.id); }
function metStar(sid){ enc79EnsureStars(); S.stars[sid].met = true; return S.stars[sid]; }
ok('註冊順序：陸冷版排暖版之前（finale＋patron）', beatIds('luk_baakyin').indexOf('luk_finale_cold') < beatIds('luk_baakyin').indexOf('luk_finale') && beatIds('luk_baakyin').indexOf('luk_patron_cold') < beatIds('luk_baakyin').indexOf('luk_patron'));
ok('註冊順序：陸 tease 在 intel 之後、thanks 之前', beatIds('luk_baakyin').indexOf('luk_intel') < beatIds('luk_baakyin').indexOf('luk_tease') && beatIds('luk_baakyin').indexOf('luk_tease') < beatIds('luk_baakyin').indexOf('luk_thanks'));
ok('冷版 DLG 句數：陸 finale_cold 5／patron_cold 6', ENC79_DIALOG.luk_baakyin.beats.luk_finale_cold.lines.length===5 && ENC79_DIALOG.luk_baakyin.beats.luk_patron_cold.lines.length===6);
resetS(300); _ys = { year:1991, season:'春' }; setFav('luk_baakyin', 30);
ok('閘：luk_tease 1991＋T2 開', openBeat('luk_baakyin','luk_tease')===true);
ok('閘：luk_tease 1990 唔開（夾替工通告 1991 冬）', (()=>{ _ys = { year:1990, season:'秋' }; return openBeat('luk_baakyin','luk_tease')===false; })());
ok('閘：luk_tease 頂過夜（cover）唔再開', (()=>{ _ys = { year:1991, season:'春' }; S.flags.luk_cover_night = 1; return openBeat('luk_baakyin','luk_tease')===false; })());
ok('閘：luk_tease 已經 absent 唔再開', (()=>{ resetS(301); _ys = { year:1991, season:'春' }; setFav('luk_baakyin', 30); S.flags.luk_absent_night = 1; return openBeat('luk_baakyin','luk_tease')===false; })());
ok('閘：luk_tease 播出即派替工通告（GRANT229，第二朝到期）', (()=>{ resetS(302); _ys = { year:1991, season:'夏' }; setFav('luk_baakyin', 30); const b = beatOf('luk_baakyin','luk_tease'); b.grants(); return S.grant229Queue.length===1 && S.grant229Queue[0].gigId==='gig_1991_tv_203' && S.grant229Queue[0].dueDay===303; })());
ok('閘：luk_tease 即派一生一次（重播唔重派）', (()=>{ const b = beatOf('luk_baakyin','luk_tease'); b.grants(); return S.grant229Queue.length===1; })());
resetS(310); _ys = { year:1991, season:'冬' }; setFav('luk_baakyin', 30);
ok('閘：luk_thanks 無 cover 唔開', openBeat('luk_baakyin','luk_thanks')===false);
S.flags.luk_cover_night = 1;
ok('閘：luk_thanks 有 cover 開', openBeat('luk_baakyin','luk_thanks')===true);
resetS(320); _ys = { year:1992, season:'冬' }; setFav('luk_baakyin', 70);
ok('閘：陸 finale 暖／冷分流（無旗行暖）', openBeat('luk_baakyin','luk_finale')===true && openBeat('luk_baakyin','luk_finale_cold')===false && openBeat('luk_baakyin','luk_patron')===true && openBeat('luk_baakyin','luk_patron_cold')===false);
ok('閘：陸 finale／patron 壞旗（absent）行冷', (()=>{ S.flags.luk_absent_night = 1; return openBeat('luk_baakyin','luk_finale')===false && openBeat('luk_baakyin','luk_finale_cold')===true && openBeat('luk_baakyin','luk_patron')===false && openBeat('luk_baakyin','luk_patron_cold')===true; })());
ok('閘：陸 finale／patron 壞旗（loose_talk）行冷', (()=>{ resetS(321); _ys = { year:1992, season:'冬' }; setFav('luk_baakyin', 70); S.flags.luk_loose_talk = 1; return openBeat('luk_baakyin','luk_finale')===false && openBeat('luk_baakyin','luk_finale_cold')===true && openBeat('luk_baakyin','luk_patron')===false && openBeat('luk_baakyin','luk_patron_cold')===true; })());
ok('閘：陸 finale 冷版排暖版之前（PickBeat 揀冷）', (()=>{ const st = S.stars.luk_baakyin; for(const b of (ENC79_BEATS.luk_baakyin||[])) if(b.id!=='luk_finale_cold' && b.id!=='luk_finale' && b.id!=='luk_patron_cold' && b.id!=='luk_patron') st.beatsDone[b.id] = 1; const p = enc79PickBeat('luk_baakyin'); return !!p && p.id==='luk_finale_cold'; })());
ok('閘：陸 finale 暖版 T4＋無旗 → PickBeat 揀暖 finale', (()=>{ resetS(322); _ys = { year:1992, season:'冬' }; setFav('luk_baakyin', 70); const st = S.stars.luk_baakyin; for(const b of (ENC79_BEATS.luk_baakyin||[])) if(b.id!=='luk_finale' && b.id!=='luk_patron') st.beatsDone[b.id] = 1; const p = enc79PickBeat('luk_baakyin'); return !!p && p.id==='luk_finale'; })());
ok('閘：陸 intel 無傳聞閘（T2 照開）', (()=>{ resetS(323); _ys = { year:1990, season:'秋' }; setFav('luk_baakyin', 30); return openBeat('luk_baakyin','luk_intel')===true; })());

/* ---- (4) 28 日 absent tick ---- */
ok('tick：tease 後 28 日唔做替工 → absent', (()=>{ resetS(400); setFav('luk_baakyin', 30); S.stars.luk_baakyin.beatsDone.luk_tease = 100; S.dayIndex = 128; enc271LukAbsentTick(); return S.flags.luk_absent_night===1; })());
ok('tick：tease 後 27 日未夠鐘 → 唔立 absent', (()=>{ resetS(401); setFav('luk_baakyin', 30); S.stars.luk_baakyin.beatsDone.luk_tease = 100; S.dayIndex = 127; enc271LukAbsentTick(); return !S.flags.luk_absent_night; })());
ok('tick：未播 tease → 唔立 absent', (()=>{ resetS(402); setFav('luk_baakyin', 30); S.dayIndex = 500; enc271LukAbsentTick(); return !S.flags.luk_absent_night; })());
ok('tick：替工已殺青（done_）→ 唔立 absent', (()=>{ resetS(403); setFav('luk_baakyin', 30); S.stars.luk_baakyin.beatsDone.luk_tease = 100; S.dayIndex = 200; S.flags['done_gig_1991_tv_203'] = 1; enc271LukAbsentTick(); return !S.flags.luk_absent_night; })());
ok('tick：替工排緊行程（shoots）→ 唔立 absent', (()=>{ resetS(404); setFav('luk_baakyin', 30); S.stars.luk_baakyin.beatsDone.luk_tease = 100; S.dayIndex = 200; S.shoots = [{ gigId:'gig_1991_tv_203' }]; enc271LukAbsentTick(); return !S.flags.luk_absent_night; })());
ok('tick：已經 cover → 唔立 absent', (()=>{ resetS(405); setFav('luk_baakyin', 30); S.stars.luk_baakyin.beatsDone.luk_tease = 100; S.dayIndex = 200; S.flags.luk_cover_night = 1; enc271LukAbsentTick(); return !S.flags.luk_absent_night; })());

/* ---- (5) 變體（BuildScript）＋pushSeg flags 傳遞 ---- */
ok('變體：liu_patron 認真回應（插句）', (()=>{ resetS(500); _ys = { year:1992, season:'秋' }; setFav('liu_bingxing', 70); metStar('liu_bingxing'); S.flags.liu_heart_earnest = 1; const st = S.stars.liu_bingxing; for(const b of (ENC79_BEATS.liu_bingxing||[])) if(b.id!=='liu_patron' && !b.id.endsWith('_patron')) st.beatsDone[b.id] = 1; const built = enc79BuildScript('liu_bingxing', false); return !!built && built.steps.some(s=>String(s.text||'').indexOf('你嗰日認真回我嗰句，我收到')>=0); })());
ok('變體：liu_patron 用笑話接住（插另一句）', (()=>{ resetS(501); _ys = { year:1992, season:'秋' }; setFav('liu_bingxing', 70); metStar('liu_bingxing'); S.flags.liu_heart_joke = 1; const st = S.stars.liu_bingxing; for(const b of (ENC79_BEATS.liu_bingxing||[])) if(b.id!=='liu_patron' && !b.id.endsWith('_patron')) st.beatsDone[b.id] = 1; const built = enc79BuildScript('liu_bingxing', false); return !!built && built.steps.some(s=>String(s.text||'').indexOf('你嗰日用笑話接我嗰句')>=0) && !built.steps.some(s=>String(s.text||'').indexOf('你嗰日認真回我嗰句')>=0); })());
ok('變體：liu_patron 無交心旗唔插句', (()=>{ resetS(502); _ys = { year:1992, season:'秋' }; setFav('liu_bingxing', 70); metStar('liu_bingxing'); const st = S.stars.liu_bingxing; for(const b of (ENC79_BEATS.liu_bingxing||[])) if(b.id!=='liu_patron' && !b.id.endsWith('_patron')) st.beatsDone[b.id] = 1; const built = enc79BuildScript('liu_bingxing', false); return !!built && !built.steps.some(s=>String(s.text||'').indexOf('你嗰日認真回我嗰句')>=0) && !built.steps.some(s=>String(s.text||'').indexOf('你嗰日用笑話接我嗰句')>=0); })());
ok('變體：gu_patron 陪到天光（插句）', (()=>{ resetS(503); _ys = { year:1992, season:'秋' }; setFav('gu_mingfai', 70); metStar('gu_mingfai'); S.flags.gu_heart_sit = 1; const st = S.stars.gu_mingfai; for(const b of (ENC79_BEATS.gu_mingfai||[])) if(b.id!=='gu_patron') st.beatsDone[b.id] = 1; const built = enc79BuildScript('gu_mingfai', false); return !!built && built.steps.some(s=>String(s.text||'').indexOf('嗰晚你陪我坐到天光')>=0); })());
ok('變體：gu_patron 勸戒賭（插另一句）', (()=>{ resetS(504); _ys = { year:1992, season:'秋' }; setFav('gu_mingfai', 70); metStar('gu_mingfai'); S.flags.gu_heart_quit = 1; const st = S.stars.gu_mingfai; for(const b of (ENC79_BEATS.gu_mingfai||[])) if(b.id!=='gu_patron') st.beatsDone[b.id] = 1; const built = enc79BuildScript('gu_mingfai', false); return !!built && built.steps.some(s=>String(s.text||'').indexOf('把聲仲喺度，仲可以重新嚟過')>=0) && !built.steps.some(s=>String(s.text||'').indexOf('嗰晚你陪我坐到天光')>=0); })());
ok('變體：gu_patron 無交心旗唔插句', (()=>{ resetS(505); _ys = { year:1992, season:'秋' }; setFav('gu_mingfai', 70); metStar('gu_mingfai'); const st = S.stars.gu_mingfai; for(const b of (ENC79_BEATS.gu_mingfai||[])) if(b.id!=='gu_patron') st.beatsDone[b.id] = 1; const built = enc79BuildScript('gu_mingfai', false); return !!built && !built.steps.some(s=>String(s.text||'').indexOf('嗰晚你陪我坐到天光')>=0) && !built.steps.some(s=>String(s.text||'').indexOf('把聲仲喺度，仲可以重新嚟過')>=0); })());
ok('變體：luk_foreshadow 認雙手遞劇本（插句）', (()=>{ resetS(506); _ys = { year:1990, season:'夏' }; setFav('luk_baakyin', 10); metStar('luk_baakyin'); S.flags.luk_first_quiet = 1; const built = enc79BuildScript('luk_baakyin', false); return !!built && built.steps.some(s=>String(s.text||'').indexOf('遞返劇本嗰陣，陸柏言連望都冇望佢一眼')>=0); })());
ok('變體：luk_foreshadow 認介紹自己（插另一句）', (()=>{ resetS(507); _ys = { year:1990, season:'夏' }; setFav('luk_baakyin', 10); metStar('luk_baakyin'); S.flags.luk_first_pushy = 1; const built = enc79BuildScript('luk_baakyin', false); return !!built && built.steps.some(s=>String(s.text||'').indexOf('佢話自己叫阿偉，陸柏言話臨記咁多個')>=0) && !built.steps.some(s=>String(s.text||'').indexOf('遞返劇本嗰陣，陸柏言連望都冇望佢一眼')>=0); })());
ok('變體：luk_foreshadow 無初遇旗唔插句', (()=>{ resetS(508); _ys = { year:1990, season:'夏' }; setFav('luk_baakyin', 10); metStar('luk_baakyin'); const built = enc79BuildScript('luk_baakyin', false); return !!built && !built.steps.some(s=>String(s.text||'').indexOf('遞返劇本嗰陣')>=0) && !built.steps.some(s=>String(s.text||'').indexOf('佢話自己叫阿偉')>=0); })());
ok('heart 閘：陸 T3 無守口旗 → heart 唔開', (()=>{ resetS(509); _ys = { year:1991, season:'夏' }; setFav('luk_baakyin', 45); metStar('luk_baakyin'); const st = S.stars.luk_baakyin; for(const b of (ENC79_BEATS.luk_baakyin||[])) st.beatsDone[b.id] = 1; const built = enc79BuildScript('luk_baakyin', false); return !!built && !built.steps.some(s=>s.seg==='heart:luk_baakyin'); })());
ok('heart 閘：陸 T3 有守口旗 → heart 開', (()=>{ resetS(510); _ys = { year:1991, season:'夏' }; setFav('luk_baakyin', 45); metStar('luk_baakyin'); S.flags.luk_kept_secret = 1; const st = S.stars.luk_baakyin; for(const b of (ENC79_BEATS.luk_baakyin||[])) st.beatsDone[b.id] = 1; const built = enc79BuildScript('luk_baakyin', false); return !!built && built.steps.some(s=>s.seg==='heart:luk_baakyin'); })());
ok('pushSeg：liu heart 抉擇 options 帶交心旗', (()=>{ resetS(511); _ys = { year:1991, season:'夏' }; setFav('liu_bingxing', 45); metStar('liu_bingxing'); const st = S.stars.liu_bingxing; for(const b of (ENC79_BEATS.liu_bingxing||[])) if(!b.id.endsWith('_patron')) st.beatsDone[b.id] = 1; const built = enc79BuildScript('liu_bingxing', false); const ch = (built.steps||[]).find(s=>s.choice && s.seg==='heart:liu_bingxing'); return !!ch && JSON.stringify(ch.options[0].flags)==='["liu_heart_earnest"]' && JSON.stringify(ch.options[1].flags)==='["liu_heart_joke"]'; })());
ok('pushSeg：gu heart 抉擇 options 帶交心旗', (()=>{ resetS(512); _ys = { year:1991, season:'夏' }; setFav('gu_mingfai', 45); metStar('gu_mingfai'); const st = S.stars.gu_mingfai; for(const b of (ENC79_BEATS.gu_mingfai||[])) if(!b.id.endsWith('_patron')) st.beatsDone[b.id] = 1; const built = enc79BuildScript('gu_mingfai', false); const ch = (built.steps||[]).find(s=>s.choice && s.seg==='heart:gu_mingfai'); return !!ch && JSON.stringify(ch.options[0].flags)==='["gu_heart_sit"]' && JSON.stringify(ch.options[1].flags)==='["gu_heart_quit"]'; })());
ok('pushSeg：luk foreshadow 抉擇 options 帶守口／講兩句旗', (()=>{ resetS(513); _ys = { year:1990, season:'夏' }; setFav('luk_baakyin', 10); metStar('luk_baakyin'); const built = enc79BuildScript('luk_baakyin', false); const ch = (built.steps||[]).find(s=>s.choice && s.seg==='beat:luk_foreshadow'); return !!ch && JSON.stringify(ch.options[0].flags)==='["luk_kept_secret"]' && JSON.stringify(ch.options[1].flags)==='["luk_loose_talk"]'; })());
ok('pushSeg：luk first 抉擇 options 帶初遇旗（第三選無旗）', (()=>{ resetS(514); _ys = { year:1990, season:'春' }; enc79EnsureStars(); const built = enc79BuildScript('luk_baakyin', true); const ch = (built.steps||[]).find(s=>s.choice && s.seg==='first:luk_baakyin'); return !!ch && JSON.stringify(ch.options[0].flags)==='["luk_first_quiet"]' && JSON.stringify(ch.options[1].flags)==='["luk_first_pushy"]' && (ch.options[2].flags===null || ch.options[2].flags===undefined); })());

console.log(fails.length ? ('\nFAILURES: ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
