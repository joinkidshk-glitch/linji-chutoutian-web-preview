// v20a176 ROM176 全面隨機巧遇・邏輯測試
// 合約（用戶 2026-11-13 拍板：全部人隨機撞到，連紅星都可以送禮；設計 DESIGN.md §2–§8）：
//   A 注入：12 星 prefs（最愛 2／喜歡 2／唔鍾意 1–2）＋海媚 prefs＋48 條星反應句
//     （最愛 24 item-specific＋喜歡／唔鍾意 24 tier-generic）＋藍／徐／海媚 NPC_LINES＋PORTRAITS；
//     注入冪等；唔郁 content pack JSON（靜態測試覆）。
//   B 女角出沒盤：P=0.50、主場 share 0.65、種子可重現；風聲窗 P≥0.80／share 0.85；
//     未完成故事節點 offer → P+0.10（上限 0.85）；海媚未解鎖（C9 未完成）P=0。
//   C caps＋保底：每日 1 次／每週 3 次／同一位冷卻 2 日／初遇保底 5 日；主線待播優先。
//   D 女角巧遇 modal：傾談恆出／送禮睇 canGive／約會入口 v159 未落地唔出／行開返 encDone。
//   E 星送禮：最愛 +4／喜歡 +2／普通 +1／唔鍾意 −2；重複第 2 次起正數減半；
//     每日每星 1 份；經 enc79AddFav "gift"——同對話共用每週軟頂 10（wrap 唔計）；
//     級數上限 30／55／80／100 照舊；未見過唔送得。
//   F 返程守衛：rom176BackOpts 旗在食咗佢返 {encDone:true}，唔在返 {travelFree:true}。
// 反證：pristine main (a618a5d) 冇 ROM176 函數 → 抽取即 throw → FAIL。
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
function extractFn(name){
  const i = html.indexOf('function ' + name + '(');
  if (i < 0) throw new Error('fn not found: ' + name);
  let depth = 0, j = html.indexOf('{', i);
  for (; j < html.length; j++){ if (html[j] === '{') depth++; else if (html[j] === '}'){ depth--; if (depth === 0) break; } }
  return html.slice(i, j + 1);
}
function extractConst(name){
  const i = html.indexOf('const ' + name + ' =');
  if (i < 0) throw new Error('const not found: ' + name);
  let depth = 0, started = false;
  for (let k = i; k < html.length; k++){
    const ch = html[k];
    if (ch === '{' || ch === '['){ depth++; started = true; }
    else if (ch === '}' || ch === ']'){ depth--; if (started && depth === 0) return html.slice(i, k + 1) + ';'; }
    else if (ch === ';' && !started) return html.slice(i, k + 1);
  }
  throw new Error('const end not found: ' + name);
}
let fails = 0;
function ok(name, cond, extra){
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : ''));
  if (!cond) fails++;
}

/* ---------- 沙盒 ---------- */
var window = {};
var location = { search: '' };
var localStorage = { getItem: ()=>null, setItem: ()=>{}, removeItem: ()=>{} };
function makeEl(){ return { innerHTML:'', textContent:'', style:{}, classList:{ add(){}, remove(){}, toggle(){} }, setAttribute(){}, appendChild(){}, querySelector(){ return makeEl(); }, querySelectorAll(){ return []; } }; }
var __els = {};
var document = {
  getElementById(id){ return __els[id] || (__els[id] = makeEl()); },
  querySelector(){ return makeEl(); }, querySelectorAll(){ return []; },
  createElement(){ return makeEl(); }, body: makeEl(), addEventListener(){},
};
var __modals = [], __toasts = [], __openLocCalls = [], __doTalkCalls = [], __giftPickCalls = [], __played = [];
var modal = function(body, btns, opts){ __modals.push({ body: String(body || ''), btns: btns || [], opts: opts || {} }); };
var toast = function(m){ __toasts.push(String(m || '')); };
var saveQ = function(){}; var paintBar = function(){}; var drawMap = function(){};
var openLoc = function(id, opts){ __openLocCalls.push({ id, opts: opts || {} }); };
var doTalk = function(npcId, L){ __doTalkCalls.push({ npcId, locId: L && L.id }); };
var openGiftPick = function(k, L){ __giftPickCalls.push({ key: k, locId: L && L.id }); };
var fmtDate = function(){ return '1990-01-01'; };
var __canGive = true;
var GIGS = [];
var S = null;
var GIFT_PREFS = { npcs:{}, placeholderLines:{ liked:'L', dislike:'D', neutral:'N' } };
var GIFT_REACT = { byKey:{}, entries:[] };
var NPC_LINES = {};
var PORTRAITS = {};
var NPCS = {
  colleague:{ face:'npc_cheung' }, reporter:{ face:'npc_chow' }, stylist:{ face:'npc_vera' },
  lan:{ face:'npc_lan' }, xu:{ face:'npc_xu' }, mei:{ face:'npc_mei' },
};
var LOCS = [
  { id:'tvb_longmen', name:'星河電視台' }, { id:'tvb_kowloon', name:'九龍電視城' },
  { id:'rec_star', name:'天星音樂' }, { id:'film_cotton', name:'棉花路片場' },
  { id:'ad_central', name:'中環廣告' }, { id:'ad_adm', name:'金鐘創意' }, { id:'rec_hk', name:'海港廣播' },
];
var GiftShop = {
  prefFor(k){ return (GIFT_PREFS.npcs && GIFT_PREFS.npcs[k]) || null; },
  itemById(id){ return { id, name:id }; },
  inventoryList(){ return Object.keys((S && S.inventory) || {}).filter(id=>Number(S.inventory[id])>0).map(id=>({ id })); },
  canGive(){ return { ok: __canGive, reason: __canGive ? '' : '未開放' }; },
  ensureSave(){},
};
var __storyNodes = {}, __storyDone = {};
var StoryOC = {
  ensure(){}, getFlag(k){ return !!(S && S.flags && S.flags[k]); },
  setFlag(k, v){ if (S){ S.flags = S.flags || {}; S.flags[k] = v; } },
  isDone(id){ return !!__storyDone[id] || !!(S && S.story && S.story.done && S.story.done[id]); },
  listOpen(){ return { open: [] }; },
  findNodeRaw(id){ return __storyNodes[id] || null; },
  evalNode(n){ return { ok: !!n }; },
};
var rom176InEncounter = null;
var rom176PlayEncounter = function(k, loc){ __played.push([k, loc]); };

let __extractFailed = null;
try {
for (const c of ['ENC79_STARS','ENC79_FAV_CAPS','ENC79_WEEK_SOFT_CAP'])
  eval(extractConst(c).replace('const ' + c + ' =', 'var ' + c + ' ='));
for (const c of ['ROM176_WOMEN','ROM176_MEET_NODES','ROM176_GREET','ROM176_TEA_LINES'])
  eval(extractConst(c).replace('const ' + c + ' =', 'var ' + c + ' ='));
eval(extractConst('ROM176_P').replace('const ROM176_P =', 'var ROM176_P ='));
for (const f of ['enc79Hash','enc79Rand','enc79StarDef','enc79EnsureStars','enc79StarState',
  'enc79PlayerTier','enc79FavCap','enc79AddFav','enc79StoryPendingAt','weekNumNow',
  'rom176SetEncounter','rom176BackOpts','rom176WomanDef','rom176WomanName','rom176IsWomanNpc',
  'rom176WomanMet','rom176MeiUnlocked','rom176WhisperActive','rom176BeatOpen','rom176PresenceP',
  'rom176EnsureDay','rom176PresenceAt','rom176GrantWhisper','rom176TeaTargets','rom176TryIntercept',
  'rom176StarPrefKind','rom176StarDelta','rom176CanGiveStarGift','rom176StarReactionLine',
  'rom176DoGiveStarGift','rom176ApplyGiftOverrides','rom183XuMetBefore183','rom183RelText183']) eval(extractFn(f));
} catch (e) { __extractFailed = e; }
if (__extractFailed){
  console.log('FAIL harness: 抽取 ROM176／enc79 函數失敗（pristine 預期反證） :: ' + __extractFailed.message);
  process.exit(1);
}
ok('harness: ROM176＋enc79 函數全載入',
  typeof rom176TryIntercept === 'function' && typeof rom176ApplyGiftOverrides === 'function' && typeof enc79AddFav === 'function');

function baseSave(over){
  return Object.assign({
    dayIndex: 0, fame: 5, flags: {}, story: { done: {}, rel: {} },
    inventory: {}, giftMeta: { lastGiveDay: {} }, stars: null,
    mockRumors: [], mapTips: {}, npcs: {},
  }, over || {});
}

/* ---------- A 注入 ---------- */
(function(){
  rom176ApplyGiftOverrides();
  const stars = ['luk_baakyin','liu_bingxing','ngai_wingnaam','yip_manji','mak_zhendong','lok_gasing',
    'pang_siuki','chung_choning','gu_mingfai','so_jiyan','chai_zanhoi','ching_tinlok'];
  const expect = {
    luk_baakyin:{ fav:['gift_coffee_beans','gift_memo_pad'], like:['gift_perfume_sample','gift_fashion_mag'], dis:['gift_pineapple_bun_set'] },
    liu_bingxing:{ fav:['gift_pineapple_bun_set','gift_egg_tart_box'], like:['gift_cassette_indie','gift_thermos'], dis:['gift_perfume_sample'] },
    ngai_wingnaam:{ fav:['gift_thermos','gift_pineapple_bun_set'], like:['gift_egg_tart_box','gift_cassette_indie'], dis:['gift_fashion_mag'] },
    yip_manji:{ fav:['gift_perfume_sample','gift_fashion_mag'], like:['gift_hair_clip_set','gift_thermos'], dis:['gift_pineapple_bun_set'] },
    mak_zhendong:{ fav:['gift_thermos','gift_egg_tart_box'], like:['gift_pineapple_bun_set','gift_cassette_indie'], dis:['gift_perfume_sample'] },
    lok_gasing:{ fav:['gift_cassette_indie','gift_coffee_beans'], like:['gift_memo_pad','gift_thermos'], dis:['gift_fashion_mag'] },
    pang_siuki:{ fav:['gift_coffee_beans','gift_memo_pad'], like:['gift_thermos','gift_egg_tart_box'], dis:['gift_perfume_sample'] },
    chung_choning:{ fav:['gift_memo_pad','gift_coffee_beans'], like:['gift_thermos','gift_cassette_indie'], dis:['gift_pineapple_bun_set'] },
    gu_mingfai:{ fav:['gift_pineapple_bun_set','gift_coffee_beans'], like:['gift_thermos','gift_egg_tart_box'], dis:['gift_perfume_sample','gift_fashion_mag'] },
    so_jiyan:{ fav:['gift_perfume_sample','gift_hair_clip_set'], like:['gift_fashion_mag','gift_handmade_sweet'], dis:['gift_pineapple_bun_set'] },
    chai_zanhoi:{ fav:['gift_coffee_beans','gift_memo_pad'], like:['gift_thermos','gift_cassette_indie'], dis:['gift_perfume_sample'] },
    ching_tinlok:{ fav:['gift_cassette_indie','gift_thermos'], like:['gift_coffee_beans','gift_egg_tart_box'], dis:['gift_fashion_mag','gift_perfume_sample'] },
  };
  let prefsOk = true;
  for (const id of stars){
    const p = GIFT_PREFS.npcs[id], e = expect[id];
    if (!p || p.relKey !== 'rel_' + id || JSON.stringify(p.favorites) !== JSON.stringify(e.fav)
      || JSON.stringify(p.likes) !== JSON.stringify(e.fav.concat(e.like))
      || JSON.stringify(p.dislikes) !== JSON.stringify(e.dis)
      || !Array.isArray(p.requireFlagsAny) || p.requireFlagsAny.length !== 0) prefsOk = false;
  }
  ok('A1 12 星 prefs 齊（最愛 2／喜歡 2／唔鍾意 1–2，relKey＋空閘）', prefsOk);
  const mei = GIFT_PREFS.npcs.mei;
  ok('A2 海媚 prefs（最愛保溫瓶＋拍紙簿）', !!mei && JSON.stringify(mei.favorites) === JSON.stringify(['gift_thermos','gift_memo_pad'])
    && JSON.stringify(mei.dislikes) === JSON.stringify(['gift_perfume_sample','gift_fashion_mag']));
  let favN = 0, likedN = 0, disN = 0, perStarOk = true;
  for (const id of stars){
    const f = Object.keys(GIFT_REACT.byKey).filter(k=>k.indexOf(id + ':') === 0 && k.endsWith(':favorite'));
    const l = GIFT_REACT.byKey[id + '::liked'], d = GIFT_REACT.byKey[id + '::dislike'];
    favN += f.length; if (l) likedN++; if (d) disN++;
    if (f.length !== 2 || !l || !d) perStarOk = false;
  }
  ok('A3 48 條星反應句（最愛 24＋喜歡 12＋唔鍾意 12，每星 2／1／1）',
    favN === 24 && likedN === 12 && disN === 12 && perStarOk && GIFT_REACT.entries.length === 48,
    'fav=' + favN + ' liked=' + likedN + ' dis=' + disN + ' entries=' + GIFT_REACT.entries.length);
  const before = GIFT_REACT.entries.length;
  rom176ApplyGiftOverrides();
  ok('A4 注入冪等（再跑一次唔會重複）', GIFT_REACT.entries.length === before && Object.keys(GIFT_REACT.byKey).length === 48);
  let nlOk = true;
  for (const k of ['lan','xu','mei']){
    const n = NPC_LINES[k];
    if (!n || !['greet','chat','advice','intel','pressure'].every(s=>Array.isArray(n[s]) && n[s].length === 2)) nlOk = false;
  }
  ok('A5 NPC_LINES 藍／徐／海媚（5 類 × 2 句）', nlOk);
  ok('A6 PORTRAITS 藍／徐／海媚 fullbody 圖', PORTRAITS.npc_lan === 'assets/story/fullbody/lan_ruoxi_base.webp?v=20a176'
    && PORTRAITS.npc_xu === 'assets/story/fullbody/tsui_poushan_base.webp?v=20a176'
    && PORTRAITS.npc_mei === 'assets/story/fullbody/kwan_hoimei_base.webp?v=20a176');
})();

/* ---------- B 女角出沒盤 ---------- */
function presenceOn(day, setup){
  S = baseSave({ dayIndex: day });
  if (setup) setup();
  const p = rom176EnsureDay().presence;
  return p;
}
(function(){
  const p1 = presenceOn(10), p2 = presenceOn(10);
  ok('B1 同一日種子可重現', JSON.stringify(p1) === JSON.stringify(p2));
  let daysWithHiu = 0, hiuPrimary = 0, hiuTotal = 0, seenDays = {};
  for (let d = 0; d < 365; d++){
    const p = presenceOn(d);
    const at = [].concat(p.tvb_longmen || [], p.tvb_kowloon || []);
    if (at.indexOf('hiu') >= 0){ daysWithHiu++; hiuTotal++; if ((p.tvb_longmen || []).indexOf('hiu') >= 0) hiuPrimary++; }
    seenDays[JSON.stringify(p)] = 1;
  }
  ok('B2 P(出)=0.50（365 日曉晴出沒率 0.35–0.65）', daysWithHiu >= 128 && daysWithHiu <= 237, '出沒 ' + daysWithHiu + '/365');
  ok('B3 主場 share 0.65（出沒日主場佔比 0.50–0.80）', hiuTotal > 0 && hiuPrimary / hiuTotal >= 0.50 && hiuPrimary / hiuTotal <= 0.80,
    '主場 ' + hiuPrimary + '/' + hiuTotal);
  ok('B4 唔係日日一樣（365 日 presence 有變化）', Object.keys(seenDays).length > 100, '相異 ' + Object.keys(seenDays).length);
  // 風聲：每日續窗，P≥0.80
  let wDays = 0, wPrimary = 0, wTotal = 0;
  for (let d = 0; d < 365; d++){
    S = baseSave({ dayIndex: d });
    S.romWhispers = { hiu: { until: d + 2, src: 'tea' } };
    const p = rom176EnsureDay().presence;
    if ((p.tvb_longmen || []).indexOf('hiu') >= 0 || (p.tvb_kowloon || []).indexOf('hiu') >= 0){ wDays++; wTotal++; if ((p.tvb_longmen || []).indexOf('hiu') >= 0) wPrimary++; }
  }
  ok('B5 風聲窗 P≥0.80（365 日出沒率 ≥0.75）', wDays >= 274, '出沒 ' + wDays + '/365');
  ok('B6 風聲窗 share 0.85（主場佔比 ≥0.70）', wTotal > 0 && wPrimary / wTotal >= 0.70, '主場 ' + wPrimary + '/' + wTotal);
  // 未完成節點 → P+0.10：對照同一批種子
  __storyNodes = { R_hiu_meet: { id: 'R_hiu_meet' } };
  let beatDays = 0;
  for (let d = 0; d < 365; d++){ const p = presenceOn(d); if ([].concat(p.tvb_longmen || [], p.tvb_kowloon || []).indexOf('hiu') >= 0) beatDays++; }
  __storyNodes = {};
  ok('B7 未完成節點 offer → 出沒率上升（P+0.10）', beatDays > daysWithHiu, '節點 ' + beatDays + ' vs 平時 ' + daysWithHiu);
  // 海媚閘
  S = baseSave({ dayIndex: 100 });
  ok('B8 海媚未解鎖（C9 未完成）P=0', rom176PresenceP('mei').p === 0);
  __storyDone = { C9: true };
  ok('B9 海媚解鎖（C9 完成）P=0.50', rom176PresenceP('mei').p === 0.50);
  __storyDone = {};
  const savedStoryOC = StoryOC;
  StoryOC = null;
  S = baseSave({ dayIndex: 100 }); delete S.story.done;
  ok('B10 海媚退路：done-state 讀唔到＋day<699 → 鎖住', rom176MeiUnlocked() === false);
  S = baseSave({ dayIndex: 699 }); delete S.story.done;
  ok('B11 海媚退路：done-state 讀唔到＋day≥699 → 解鎖', rom176MeiUnlocked() === true);
  S = baseSave({ dayIndex: 100, story: { done: { C9: true }, rel: {} } });
  ok('B12 海媚退路：S.story.done 有 C9 → 解鎖', rom176MeiUnlocked() === true);
  StoryOC = savedStoryOC;
  // 風聲 grant
  S = baseSave({ dayIndex: 10 });
  ok('B13 grantWhisper 寫入 3 日窗＋手帳', rom176GrantWhisper('hiu', 'tea') === true
    && S.romWhispers.hiu.until === 12 && S.mockRumors.length === 1 && S.mockRumors[0].id === 'romwind:hiu:10');
  ok('B14 風聲未過期 active／過期失效', rom176WhisperActive('hiu') === true
    && (function(){ S.dayIndex = 13; return rom176WhisperActive('hiu') === false; })());
  ok('B15 tea targets 唔包已有風聲／未解鎖海媚', (function(){
    S = baseSave({ dayIndex: 10 }); S.romWhispers = { hiu: { until: 12 } };
    const t = rom176TeaTargets();
    return t.indexOf('hiu') < 0 && t.indexOf('mei') < 0 && t.indexOf('lan') >= 0;
  })());
})();

/* ---------- C caps＋保底 ---------- */
function findDay(pred, max){
  for (let d = 0; d < (max || 120); d++){
    const p = presenceOn(d);
    if (pred(p, d)) return d;
  }
  return -1;
}
(function(){
  const dPresent = findDay(p=> (p.tvb_longmen || []).indexOf('hiu') >= 0);
  ok('C0 測試前提：搵到曉晴喺長門嘅日子', dPresent >= 0, 'day=' + dPresent);
  // C1 每日 1 次
  S = baseSave({ dayIndex: dPresent }); __played = [];
  ok('C1 每日第 1 次觸發', rom176TryIntercept('tvb_longmen') === true && __played.length === 1);
  ok('C1b 同日第 2 次唔觸發（每日 1 次）', rom176TryIntercept('tvb_longmen') === false && __played.length === 1);
  // C2 每週 3 次
  S = baseSave({ dayIndex: dPresent });
  S.romWeek = { week: weekNumNow(), count: 3 }; __played = [];
  ok('C2 每週 3 次已滿唔觸發', rom176TryIntercept('tvb_longmen') === false);
  S = baseSave({ dayIndex: dPresent });
  S.romWeek = { week: weekNumNow(), count: 2 }; __played = [];
  ok('C2b 每週 2 次仲觸發到', rom176TryIntercept('tvb_longmen') === true && S.romWeek.count === 3);
  // C3 冷卻 2 日：將在場者全部設為昨日見過
  S = baseSave({ dayIndex: dPresent });
  const here = rom176EnsureDay().presence.tvb_longmen || [];
  S.romLast = {}; here.forEach(k=>{ S.romLast[k] = dPresent - 1; }); __played = [];
  ok('C3 冷卻中（昨日見過）唔觸發', rom176TryIntercept('tvb_longmen') === false, '在場 ' + here.join(','));
  S = baseSave({ dayIndex: dPresent });
  const here2 = rom176EnsureDay().presence.tvb_longmen || [];
  S.romLast = {}; here2.forEach(k=>{ S.romLast[k] = dPresent - 3; }); __played = [];
  ok('C3b 冷卻過咗（3 日前）觸發返', rom176TryIntercept('tvb_longmen') === true);
  // C4 保底：搵長門冇人嘅日子，曉晴未見過、保底 5 日
  const dEmpty = findDay(p=> !(p.tvb_longmen && p.tvb_longmen.length));
  ok('C4 測試前提：搵到長門冇人嘅日子', dEmpty >= 0, 'day=' + dEmpty);
  S = baseSave({ dayIndex: dEmpty });
  S.romPity = { hiu: { days: 5, day: dEmpty - 1 } }; __played = [];
  ok('C4b 保底 5 日 → 下次入主場保證出沒', rom176TryIntercept('tvb_longmen') === true && __played[0][0] === 'hiu');
  ok('C4c 撞到後保底清零', S.romPity.hiu.days === 0);
  // C4d 保底未滿唔保證：今日已經計過（rec.day===當日），days 停喺 4 → 唔強制
  S = baseSave({ dayIndex: dEmpty });
  S.romPity = { hiu: { days: 4, day: dEmpty } }; __played = [];
  ok('C4d 保底 4 日（今日已計）唔保證', rom176TryIntercept('tvb_longmen') === false && __played.length === 0);
  // C5 主線待播優先
  S = baseSave({ dayIndex: dPresent });
  S.mapTips = { tvb_longmen: { kind: 'story', nodeId: 'C2' } }; __played = [];
  ok('C5 主線待播壓住女角巧遇', rom176TryIntercept('tvb_longmen') === false && __played.length === 0);
  // C6 觸發入帳：見過旗＋冷卻＋每週計數
  S = baseSave({ dayIndex: dPresent }); __played = [];
  rom176TryIntercept('tvb_longmen');
  ok('C6 觸發即計見過旗／冷卻／每週計數', S.flags.gift_met_hiu === true && S.romLast.hiu === dPresent && S.romWeek.count === 1);
  // C7 rom176WomanMet：旗／節點
  S = baseSave({}); ok('C7a 未見過 → false', rom176WomanMet('hiu') === false);
  S = baseSave({ flags: { gift_met_hiu: true } }); ok('C7b gift_met 旗 → true', rom176WomanMet('hiu') === true);
  S = baseSave({ story: { done: { R_hiu_meet: true }, rel: {} } }); ok('C7c R meet 完成 → true', rom176WomanMet('hiu') === true);
})();

/* ---------- D 女角巧遇 modal（真 rom176PlayEncounter） ---------- */
(function(){
  eval(extractFn('rom176PlayEncounter'));
  __modals = []; __doTalkCalls = []; __openLocCalls = []; __giftPickCalls = [];
  __canGive = false;
  S = baseSave({ dayIndex: 20 });
  rom176PlayEncounter('lan', 'tvb_longmen');
  let labels = __modals[0].btns.map(b=>b.label);
  ok('D1 唔可以送禮嗰陣只出傾談＋行開', JSON.stringify(labels) === JSON.stringify(['傾談','行開']), labels.join('/'));
  ok('D2 冇約會掣（v159 未落地，defensive）', labels.indexOf('約佢出街') < 0);
  ok('D3 greet 用注入 NPC_LINES（唔係 "……"）', __modals[0].body.indexOf('通告牌嗰邊啱啱先改完') >= 0);
  ok('D4 肖像係注入 fullbody 圖', __modals[0].body.indexOf('lan_ruoxi_base.webp') >= 0);
  __modals[0].btns[0].on();
  ok('D5 撳傾談 → doTalk（npcId lan）＋設返程旗', __doTalkCalls.length === 1 && __doTalkCalls[0].npcId === 'lan'
    && rom176BackOpts().encDone === true);
  __modals = []; __openLocCalls = [];
  __canGive = true;
  S = baseSave({ dayIndex: 20 });
  rom176PlayEncounter('xu', 'ad_central');
  labels = __modals[0].btns.map(b=>b.label);
  ok('D6 可以送禮嗰陣出送禮掣', JSON.stringify(labels) === JSON.stringify(['傾談','送禮','行開']), labels.join('/'));
  __modals[0].btns[1].on();
  ok('D7 撳送禮 → openGiftPick（key xu）＋設返程旗', __giftPickCalls.length === 1 && __giftPickCalls[0].key === 'xu'
    && rom176BackOpts().encDone === true);
  __modals = []; __openLocCalls = [];
  S = baseSave({ dayIndex: 20 });
  rom176PlayEncounter('mei', 'ad_adm');
  __modals[0].btns[__modals[0].btns.length - 1].on();
  ok('D8 撳行開 → openLoc encDone', __openLocCalls.length === 1 && __openLocCalls[0].opts.encDone === true);
})();

/* ---------- E 星送禮 ---------- */
(function(){
  S = baseSave({ dayIndex: 30, inventory: { gift_coffee_beans: 2, gift_perfume_sample: 1, gift_pineapple_bun_set: 1, gift_memo_pad: 1 } });
  enc79EnsureStars();
  S.stars.luk_baakyin.met = true;
  ok('E1a 最愛 +4', JSON.stringify(rom176StarDelta('luk_baakyin', 'gift_coffee_beans')) === JSON.stringify({ delta: 4, kind: 'favorite' }));
  ok('E1b 喜歡 +2', JSON.stringify(rom176StarDelta('luk_baakyin', 'gift_perfume_sample')) === JSON.stringify({ delta: 2, kind: 'liked' }));
  ok('E1c 唔鍾意 −2', JSON.stringify(rom176StarDelta('luk_baakyin', 'gift_pineapple_bun_set')) === JSON.stringify({ delta: -2, kind: 'dislike' }));
  ok('E1d 普通 +1', JSON.stringify(rom176StarDelta('luk_baakyin', 'gift_thermos')) === JSON.stringify({ delta: 1, kind: 'neutral' }));
  S.stars.luk_baakyin.giftHist = { gift_coffee_beans: 1, gift_perfume_sample: 1, gift_thermos: 1 };
  ok('E2a 重複最愛減半 +4→+2', rom176StarDelta('luk_baakyin', 'gift_coffee_beans').delta === 2);
  ok('E2b 重複喜歡減半 +2→+1', rom176StarDelta('luk_baakyin', 'gift_perfume_sample').delta === 1);
  ok('E2c 重複普通減半 +1→+0', rom176StarDelta('luk_baakyin', 'gift_thermos').delta === 0);
  ok('E2d 重複唔鍾意唔減半（−2 照舊）', rom176StarDelta('luk_baakyin', 'gift_pineapple_bun_set').delta === -2);
  S.stars.luk_baakyin.giftHist = {};
  ok('E3a 見過＋有庫存 → 送得', rom176CanGiveStarGift('luk_baakyin') === true);
  // E3b 實送一次
  __modals = [];
  rom176DoGiveStarGift('luk_baakyin', 'gift_coffee_beans', { id: 'tvb_longmen' });
  ok('E3b 送最愛：fav +4、扣庫存、記 giftHist、記 lastGiveDay', S.stars.luk_baakyin.fav === 4
    && S.inventory.gift_coffee_beans === 1 && S.stars.luk_baakyin.giftHist.gift_coffee_beans === 1
    && S.giftMeta.lastGiveDay.rel_luk_baakyin === 30);
  ok('E3c 結果 modal 講明「好感 +4」＋「送禮唔計日子」', __modals.length === 1
    && __modals[0].body.indexOf('好感 +4') >= 0 && __modals[0].body.indexOf('送禮唔計日子') >= 0);
  ok('E3d 同日再送唔得（每日每星 1 份）', rom176CanGiveStarGift('luk_baakyin') === false);
  ok('E3e 翌日送得返', (function(){ S.dayIndex = 31; return rom176CanGiveStarGift('luk_baakyin') === true; })());
  // E4 週軟頂共用（enc／beat／gift 同一池 10）
  S = baseSave({ dayIndex: 30 });
  enc79EnsureStars();
  S.starFavWeek = { week: weekNumNow(), gain: 8 };
  ok('E4a 送禮同對話共用軟頂（餘 2）', enc79AddFav('luk_baakyin', 4, 'gift') === 2 && S.starFavWeek.gain === 10);
  ok('E4b 軟頂滿咗再送＋0', enc79AddFav('luk_baakyin', 4, 'gift') === 0);
  ok('E4c wrap 唔計軟頂（照入）', enc79AddFav('luk_baakyin', 3, 'wrap') === 3);
  ok('E4d enc 同樣受軟頂（滿咗＋0）', enc79AddFav('luk_baakyin', 2, 'enc') === 0);
  // E5 級數上限
  S = baseSave({ dayIndex: 30 });
  enc79EnsureStars();
  S.stars.luk_baakyin.fav = 28; S.starFavWeek = { week: weekNumNow(), gain: 0 };
  ok('E5a 級數上限 30（tier 0）：28＋4 → 只入 2', enc79AddFav('luk_baakyin', 4, 'gift') === 2 && S.stars.luk_baakyin.fav === 30);
  ok('E5b 到頂再送＋0', enc79AddFav('luk_baakyin', 4, 'gift') === 0);
  // E6 未見過／冇庫存唔送得
  S = baseSave({ dayIndex: 30, inventory: { gift_coffee_beans: 1 } });
  enc79EnsureStars();
  ok('E6a 未見過唔送得', rom176CanGiveStarGift('luk_baakyin') === false);
  S.stars.luk_baakyin.met = true; S.inventory = {};
  ok('E6b 冇庫存唔送得', rom176CanGiveStarGift('luk_baakyin') === false);
  // E7 反應句
  ok('E7a 最愛反應句（item-specific）', rom176StarReactionLine('luk_baakyin', 'gift_coffee_beans', 'favorite').indexOf('呢隻豆沖出嚟夠濃') >= 0);
  ok('E7b 喜歡反應句（tier-generic）', rom176StarReactionLine('luk_baakyin', 'gift_thermos', 'liked').indexOf('陸柏言：「你送嚟嘅嘢，啱我用。唔該。」') >= 0);
  ok('E7c 唔鍾意反應句（tier-generic）', rom176StarReactionLine('luk_baakyin', 'gift_pineapple_bun_set', 'dislike').indexOf('唔使咁客氣') >= 0);
  ok('E7d 普通反應句（placeholder）', rom176StarReactionLine('luk_baakyin', 'gift_thermos', 'neutral') === 'N');
  // E8 唔會整出假 rel_<star>（唔行 bumpRel／giveGift）
  S = baseSave({ dayIndex: 30, inventory: { gift_coffee_beans: 1 } });
  enc79EnsureStars();
  S.stars.luk_baakyin.met = true;
  rom176DoGiveStarGift('luk_baakyin', 'gift_coffee_beans', { id: 'tvb_longmen' });
  ok('E8 星送禮唔寫 S.story.rel（冇假 rel_luk_baakyin）', !S.story.rel.rel_luk_baakyin);
})();

/* ---------- F 返程守衛 ---------- */
(function(){
  rom176SetEncounter(null);
  ok('F1 冇旗 → {travelFree:true}', JSON.stringify(rom176BackOpts()) === JSON.stringify({ travelFree: true }));
  rom176SetEncounter({ kind: 'woman', key: 'hiu', locId: 'tvb_longmen' });
  ok('F2 有旗 → {encDone:true}（食咗佢）', JSON.stringify(rom176BackOpts()) === JSON.stringify({ encDone: true }));
  ok('F3 旗只食一次', JSON.stringify(rom176BackOpts()) === JSON.stringify({ travelFree: true }));
  ok('F4 rom176IsWomanNpc（6 女角 npcId）', ['colleague','reporter','stylist','lan','xu','mei'].every(id=>rom176IsWomanNpc(id))
    && !rom176IsWomanNpc('director') && !rom176IsWomanNpc('agent'));
})();

console.log(fails === 0 ? 'ALL PASS' : fails + ' FAILURES');
process.exit(fails ? 1 : 0);
