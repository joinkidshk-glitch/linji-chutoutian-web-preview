// v20a290 Q2 五位名冊外女星入紅星系統：邏輯測試——
//   (1) 名冊 12→17：def 齊、主副場係有效 LOCS id、win 格式啱、PILOT 齊；
//   (2) lazy-init：五位有 enc79 狀態位（fav 0）；
//   (3) 殺青四角分格對五位生效（好評主角 +3／配角 +1、劣評主角 +1／配角 0；null 格／重複格／名冊外跳過），
//       證明 grant() 讀 enc79StarDef 自動生效，唔使另開特例；
//   (4) 送禮喜好：星層 prefs 讀到（最愛 2／喜歡 2／唔鍾意 1–2），delta +4／+2／−2，
//       反應句齊，GIFT_REACT 48→68；藍星層最愛同感情層最愛零重疊（分流靠入口）；
//   (5) stageup 3 句／cap 1 句／wrap 1 句齊，升段句唔含感情線承諾句；
//   (6) 初遇劇本：BuildScript 初遇＋重遇 opener 非空，冇 DIALOG 嗰陣返 null（對照）；
//   (7) 出沒盤：五位 P＞0，win 窗內 P 升到 0.75；遠觀描寫有句。
// 用法：node tests/test_r290_five_stars.js [path-to-index.html]
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
/* ---- sandbox ---- */
let S;
let _week = 3;
let _ys = { year: 1990, season: '春' };
let _rVal = 100; /* 可控擲骰：1＝最差運，100＝最好運 */
let GIFT_PREFS = { npcs:{}, placeholderLines:{ liked:'L', dislike:'D', neutral:'N' } };
let GIFT_REACT = { byKey:{}, entries:[] };
const GiftShop = {
  prefFor: (k)=> (GIFT_PREFS.npcs || {})[k] || null,
  inventoryList: ()=> Object.keys(S.inventory || {}).filter(id=> (Number(S.inventory[id])||0) > 0),
  itemById: (id)=> ({ itemId:id }),
};
const GIGS = [
  { id:'g290_cast5', type:'電影', title:'測試五星四角戲', workTitle:'測試五星四角戲', req:{ acting:18 },
    cast:{ leadM:null, leadF:'kong_siying', supportM:'hon_sauting', supportF:'shum_yingsuet' } },
  { id:'g290_cast_lan', type:'電影', title:'測試藍配角戲', workTitle:'測試藍配角戲', req:{ acting:18 },
    cast:{ leadM:null, leadF:'wu_meilam', supportM:null, supportF:'lan_ruoxi' } },
  { id:'g290_cast_dup', type:'電影', title:'測試重複格戲', workTitle:'測試重複格戲', req:{ acting:18 },
    cast:{ leadM:'kong_siying', leadF:'kong_siying', supportM:null, supportF:null } },
  { id:'g290_cast_out', type:'電影', title:'測試名冊外戲', workTitle:'測試名冊外戲', req:{ acting:18 },
    cast:{ leadM:'someone_else', leadF:null, supportM:null, supportF:null } },
  { id:'g_test_lead', roleScale:'film_lead_big', leadStarId:'luk_baakyin', genreLabel:'劇情片', type:'電影', title:'測試主角戲', workTitle:'測試主角戲' },
];
function resetS(day){
  S = { dayIndex: day||0, fame: 0, money: 500, flags: {}, npcs: { agent: 0 }, mockRumors: [], mockDebts: [], mockCredits: [], board: {}, shoots: [], mapTips: {},
    acting: 18, stage: 14, vocal: 14, looks: 22, stamina: 75, iq: 20, charm: 16, stress: 12,
    inventory: { gift_coffee_beans: 1, gift_memo_pad: 1 }, giftMeta: { lastGiveDay: {} }, stars: null };
  GIFT_PREFS = { npcs:{}, placeholderLines:{ liked:'L', dislike:'D', neutral:'N' } };
  GIFT_REACT = { byKey:{}, entries:[] };
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
const StoryOC = { isDone: ()=>false, listOpen: ()=>({ open: [] }), findNodeRaw: (id)=>({ id }) };
function storyNodeLocId(n){ return n && n.__loc; }
function toast(){}
function modal(){}
function openLoc(){}
function paintBar(){}
function drawMap(){}

const names = ['ENC79_TIER_NAMES','ENC79_PLAYER_TIERS','ENC79_FAV_CAPS','ENC79_COOLDOWN','ENC79_DAILY_CAP','ENC79_WEEKLY_CAP','ENC79_WEEK_SOFT_CAP','ENC79_STARS','ENC79_PILOT','ENC79_DISTANCE_EXTRA','ENC79_STAGEUP','ENC79_CAP_LINES','ENC79_WRAP_ECHO','ENC79_DIALOG','ENC79_BEATS','ENC79_FIRST_ALT98','STAR_SIGHTINGS','LOCS'];
const asVar = (code, name)=> code.replace('const ' + name + ' =', 'var ' + name + ' =');
function extractDlg(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i<0) throw new Error('missing ' + name);
  const j = html.indexOf('\nconst ', i + 10);
  return html.slice(i, j<0 ? undefined : j);
}
const NEW5 = ['lan_ruoxi','kong_siying','shum_yingsuet','wu_meilam','hon_sauting'];
const consts = names.map(n=> asVar(extractConst(n), n)).join('\n')
  + '\n' + ['luk_baakyin','liu_bingxing','mak_zhendong','yip_manzi'].concat(NEW5).map(sid=>{
      try{ return asVar(extractDlg('ENC79_DLG_' + sid), 'ENC79_DLG_' + sid) + '\nENC79_DIALOG["' + (sid==='yip_manzi' ? 'yip_manji' : sid) + '"] = ENC79_DLG_' + sid + ';'; }
      catch(e){ return ''; }
    }).join('\n');
const fns = ['enc79StarDef','enc79LocName','enc79Hash','enc79Rand','enc79EnsureStars','enc79StarState','enc79TierOf','enc79PlayerTier','enc79FavCap','enc79AddFav','enc79InWindow','enc79WhisperActive','enc79PresenceP','enc79EnsureDay','enc79PresenceAt','enc79GrantWhisper','enc79GrantCredit','enc79BeatOpen','enc79AnyBeatOpen','enc79PickBeat','enc79ChoiceFx','enc79RunChoiceFx','enc79NormSeg','enc79StoryPendingAt','enc79DistanceLook','enc79OnWrap','enc79WrapPerf','enc79BuildScript','contra98EncFirstLocSwap','rom176StarPrefKind','rom176StarDelta','rom176CanGiveStarGift','rom176StarReactionLine','rom176ApplyGiftOverrides'];
eval(consts + '\n' + fns.map(extractFn).join('\n'));

const LOC_IDS = new Set(LOCS.map(l=> l.id));
const SEASONS = ['春','夏','秋','冬'];

/* ---- (1) 名冊 ---- */
ok('名冊 17 星（12＋5）', ENC79_STARS.length===17);
ok('五位 def 齊（id／name）', NEW5.every(id=>{ const d = enc79StarDef(id); return d && d.name; }));
ok('五位主場／副場係有效 LOCS id', NEW5.every(id=>{ const d = enc79StarDef(id); return LOC_IDS.has(d.primary) && LOC_IDS.has(d.secondary) && d.primary!==d.secondary; }));
ok('五位 win 格式啱（[[年,"季"],...]，季節合法）', NEW5.every(id=>{ const w = enc79StarDef(id).win; return Array.isArray(w) && w.length>=1 && w.every(x=> Array.isArray(x) && typeof x[0]==='number' && SEASONS.indexOf(x[1])>=0); }));
ok('五位 win 按巔峰年份：胡 1990／韓 1991／藍 1990–91', enc79StarDef('wu_meilam').win.every(w=> w[0]===1990) && enc79StarDef('hon_sauting').win.every(w=> w[0]===1991) && enc79StarDef('lan_ruoxi').win.some(w=> w[0]===1990) && enc79StarDef('lan_ruoxi').win.some(w=> w[0]===1991));
ok('PILOT 齊五位（巧遇揀星必要，否則永遠唔觸發）', NEW5.every(id=> ENC79_PILOT[id]===1));
ok('藍主場／副場避開感情線地點（rec_hk／tvb_longmen／tvb_kowloon／cafe_cha／date_lounge）', (()=>{ const d = enc79StarDef('lan_ruoxi'); return ['rec_hk','tvb_longmen','tvb_kowloon','cafe_cha','date_lounge'].indexOf(d.primary)<0 && ['rec_hk','tvb_longmen','tvb_kowloon','cafe_cha','date_lounge'].indexOf(d.secondary)<0; })());
ok('五位主副場全部喺舊 13 個可達地點併集入面（reachLocs 維持 13）', (()=>{ const old = ['film_lion','rec_star','cafe_cha','film_cotton','film_harbour','agency_ho','rec_hk','tvb_kowloon','tvb_longmen','ad_central','rec_wanchai','ad_adm','tvb_harbour']; return NEW5.every(id=>{ const d = enc79StarDef(id); return old.indexOf(d.primary)>=0 && old.indexOf(d.secondary)>=0; }); })());

/* ---- (2) lazy-init ---- */
resetS(0);
ok('lazy-init：五位有狀態位（fav 0／lastDay −999）', (()=>{ enc79EnsureStars(); return NEW5.every(id=> S.stars[id] && S.stars[id].fav===0 && S.stars[id].lastDay===-999 && S.stars[id].met===false); })());
ok('lazy-init 冪等（fav 唔會被重置）', (()=>{ S.stars.kong_siying.fav = 33; enc79EnsureStars(); return S.stars.kong_siying.fav===33; })());

/* ---- (3) 殺青四角分格 ---- */
resetS(40); _rVal = 100;
enc79OnWrap({ gigId:'g290_cast5', fame: 5 });
ok('殺青好評：五位主角格 +3／配角格 +1（江主角／韓配角／沈配角）', S.stars.kong_siying.fav===3 && S.stars.hon_sauting.fav===1 && S.stars.shum_yingsuet.fav===1 && S.stars.kong_siying.workedWith===true && S.stars.kong_siying.wrapEcho===true);
resetS(41); _rVal = 100;
enc79OnWrap({ gigId:'g290_cast_lan', fame: 5 });
ok('殺青好評：胡主角 +3／藍配角 +1', S.stars.wu_meilam.fav===3 && S.stars.lan_ruoxi.fav===1);
resetS(42); S.stress = 90; _rVal = 1;
enc79OnWrap({ gigId:'g290_cast5', fame: 5 });
ok('殺青劣評：主角 +1／配角 0（江 +1／韓 0／沈 0）', S.stars.kong_siying.fav===1 && S.stars.hon_sauting.fav===0 && S.stars.shum_yingsuet.fav===0);
resetS(43); _rVal = 100;
enc79OnWrap({ gigId:'g290_cast_dup', fame: 5 });
ok('重複格只計主角格一次（江佔 leadM＋leadF 只 +3）', S.stars.kong_siying.fav===3);
resetS(44); _rVal = 100;
enc79OnWrap({ gigId:'g290_cast_out', fame: 5 });
ok('名冊外星跳過唔 crash（someone_else 冇狀態位）', (()=>{ enc79EnsureStars(); return !S.stars.someone_else && S.stars.kong_siying.fav===0; })());

/* ---- (4) 送禮喜好 ---- */
resetS(0);
rom176ApplyGiftOverrides();
const EXPECT_PREFS = {
  lan_ruoxi:{ fav:['gift_coffee_beans','gift_memo_pad'], like:['gift_thermos','gift_egg_tart_box'], dis:['gift_fashion_mag'] },
  kong_siying:{ fav:['gift_memo_pad','gift_cassette_indie'], like:['gift_coffee_beans','gift_handmade_sweet'], dis:['gift_fashion_mag'] },
  shum_yingsuet:{ fav:['gift_cassette_indie','gift_thermos'], like:['gift_coffee_beans','gift_handmade_sweet'], dis:['gift_pineapple_bun_set'] },
  wu_meilam:{ fav:['gift_perfume_sample','gift_hair_clip_set'], like:['gift_fashion_mag','gift_handmade_sweet'], dis:['gift_thermos'] },
  hon_sauting:{ fav:['gift_cassette_indie','gift_coffee_beans'], like:['gift_thermos','gift_memo_pad'], dis:['gift_perfume_sample','gift_fashion_mag'] },
};
ok('五位星層 prefs 齊（最愛 2／喜歡 2／唔鍾意 1–2，relKey＋空閘）', NEW5.every(id=>{ const p = GIFT_PREFS.npcs[id], e = EXPECT_PREFS[id]; return p && p.relKey==='rel_'+id && JSON.stringify(p.favorites)===JSON.stringify(e.fav) && JSON.stringify(p.likes)===JSON.stringify(e.fav.concat(e.like)) && JSON.stringify(p.dislikes)===JSON.stringify(e.dis) && Array.isArray(p.requireFlagsAny) && p.requireFlagsAny.length===0; }));
ok('藍星層最愛同感情層最愛零重疊（分流靠入口：星層鍵 lan_ruoxi vs 感情層鍵 lan）', (()=>{ const fav = GIFT_PREFS.npcs.lan_ruoxi.favorites; return fav.indexOf('gift_handmade_sweet')<0 && fav.indexOf('gift_cassette_indie')<0 && !GIFT_PREFS.npcs.lan; })());
ok('送禮 delta 分層：最愛 +4／喜歡 +2／唔鍾意 −2／普通 +1', rom176StarDelta('lan_ruoxi','gift_coffee_beans').delta===4 && rom176StarDelta('lan_ruoxi','gift_thermos').delta===2 && rom176StarDelta('lan_ruoxi','gift_fashion_mag').delta===-2 && rom176StarDelta('lan_ruoxi','gift_hair_clip_set').delta===1);
ok('送禮反應句齊：每星最愛 2 條＋喜歡 1 條＋唔鍾意 1 條，GIFT_REACT 48→68', (()=>{ let favN=0, likedN=0, disN=0, perOk=true; for(const id of NEW5){ const f = Object.keys(GIFT_REACT.byKey).filter(k=> k.indexOf(id+':')===0 && k.endsWith(':favorite')); const l = GIFT_REACT.byKey[id+'::liked'], d = GIFT_REACT.byKey[id+'::dislike']; favN+=f.length; if(l) likedN++; if(d) disN++; if(f.length!==2 || !l || !d) perOk=false; } return favN===10 && likedN===5 && disN===5 && perOk && GIFT_REACT.entries.length===68; })());
ok('最愛反應句講得出名（藍咖啡豆句）', rom176StarReactionLine('lan_ruoxi','gift_coffee_beans','favorite').indexOf('藍若曦')>=0 && rom176StarReactionLine('lan_ruoxi','gift_coffee_beans','favorite').indexOf('咖啡豆')>=0);
ok('送禮閘：未見過唔送得，見過先送得', (()=>{ resetS(0); rom176ApplyGiftOverrides(); const before = rom176CanGiveStarGift('lan_ruoxi'); enc79EnsureStars(); S.stars.lan_ruoxi.met = true; return before===false && rom176CanGiveStarGift('lan_ruoxi')===true; })());

/* ---- (5) stageup／cap／wrap ---- */
ok('升段句齊：每星 3 句', NEW5.every(id=> Array.isArray(ENC79_STAGEUP[id]) && ENC79_STAGEUP[id].length===3 && ENC79_STAGEUP[id].every(l=> Array.isArray(l) && l.length===2 && l[1])));
ok('上限句齊：每星 1 句（單句 ["S", text] 格式）', NEW5.every(id=> Array.isArray(ENC79_CAP_LINES[id]) && ENC79_CAP_LINES[id].length===2 && ENC79_CAP_LINES[id][0]==='S' && ENC79_CAP_LINES[id][1]));
ok('回望句齊：每星 1 句（單句 ["S", text] 格式）', NEW5.every(id=> Array.isArray(ENC79_WRAP_ECHO[id]) && ENC79_WRAP_ECHO[id].length===2 && ENC79_WRAP_ECHO[id][0]==='S' && ENC79_WRAP_ECHO[id][1]));
ok('升段句唔含感情線承諾句（唔寫拍拖／等收工／企隔籬）', NEW5.every(id=> ENC79_STAGEUP[id].every(l=> l[1].indexOf('拍拖')<0 && l[1].indexOf('等埋我收工')<0 && l[1].indexOf('企喺我隔籬')<0)));

/* ---- (6) 初遇劇本 ---- */
resetS(0);
ok('初遇劇本：五位 first 非空＋有抉擇', NEW5.every(id=>{ const b = enc79BuildScript(id, true, enc79StarDef(id).primary); return b && b.first===true && b.steps.length>5 && b.steps.some(s=> s.choice===true); }));
ok('重遇劇本：opener 非空（T1 段）', NEW5.every(id=>{ enc79EnsureStars(); S.stars[id].met = true; S.stars[id].fav = 15; const b = enc79BuildScript(id, false, enc79StarDef(id).primary); return b && b.steps.length>0 && b.steps.some(s=> typeof s.text==='string' && s.text.length>0); }));
ok('升段＋回望接入劇本（fav 升段＋wrapEcho 有句）', (()=>{ resetS(0); enc79EnsureStars(); S.stars.lan_ruoxi.met = true; S.stars.lan_ruoxi.fav = 15; S.stars.lan_ruoxi.stage = 0; S.stars.lan_ruoxi.wrapEcho = true; const b = enc79BuildScript('lan_ruoxi', false, 'film_cotton'); const txt = b.steps.map(s=> s.text||'').join('|'); return txt.indexOf('通告牌我派完喇')>=0 && txt.indexOf('執通告牌嗰手快過我哋成班人')>=0; })());
ok('對照：冇 DIALOG 嘅星返 null（mei）', enc79BuildScript('mei', true, 'cafe_cha')===null);

/* ---- (7) 出沒盤＋遠觀 ---- */
resetS(100); _ys = { year:1990, season:'春' };
ok('出沒盤：五位 P＞0（1990 春）', NEW5.every(id=> enc79PresenceP(enc79StarDef(id), 100).p>0));
ok('win 窗內 P 升到 0.75（胡 1990 夏／韓 1991 夏）', (()=>{ _ys = { year:1990, season:'夏' }; const wu = enc79PresenceP(enc79StarDef('wu_meilam'), 100).p; _ys = { year:1991, season:'夏' }; const hon = enc79PresenceP(enc79StarDef('hon_sauting'), 100).p; _ys = { year:1990, season:'春' }; return wu===0.75 && hon===0.75; })());
ok('遠觀描寫：五位 SIGHTINGS 行齊（distanceLook＋locs＝主場）', NEW5.every(id=>{ const r = STAR_SIGHTINGS.find(s=> s.starId===id); return r && r.distanceLook && r.locs && r.locs[0]===enc79StarDef(id).primary && r.resultToast; }));
ok('遠觀描寫讀得到（藍）', enc79DistanceLook('lan_ruoxi').indexOf('藍若曦')>=0);

if(fails.length){ console.log('FAILURES: ' + fails.join(' | ')); process.exit(1); }
console.log('ALL PASS');
