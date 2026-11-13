// v20a183 ROM183 邏輯測試：修 v176 review B1–B4＋C1–C3／C9（B4／C5／C7 另見靜態測試＋實駕）。
// 反證：pristine main (6ed68f8) 冇 ROM183 函數 → 抽取即 throw → FAIL。
// 用法：node tests/test_rom183_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const IDX = process.argv[2] ? path.resolve(process.argv[2]) : path.join(__dirname, '..', 'index.html');
const ROOT = path.dirname(IDX);
const html = fs.readFileSync(IDX, 'utf8');
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
var __modals = [], __toasts = [], __openLocCalls = [], __doTalkCalls = [], __giftPickCalls = [];
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
var NPC_LINES_CORE = null;
var TUTORIAL = null, TUTORIAL_ZH_HK = null;
var PORTRAITS = {};
var NPCS = {
  colleague:{ name:'林曉晴', role:'同期演員', face:'npc_cheung' },
  reporter:{ name:'周采兒', role:'娛樂記者', face:'npc_chow' },
  stylist:{ name:'Vera', role:'造型師', face:'npc_vera' },
  lan:{ name:'藍若曦', role:'電視台場記', face:'npc_lan' },
  xu:{ name:'徐寶珊', role:'廣告客戶總監', face:'npc_xu' },
  mei:{ name:'關海媚', role:'台柱', face:'npc_mei' },
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
  getRel(k){ return (S && S.story && S.story.rel && Number(S.story.rel[k])) || 0; },
  bumpRel(k, d){ if (S){ S.story = S.story || {}; S.story.rel = S.story.rel || {}; S.story.rel[k] = (Number(S.story.rel[k])||0) + d; } },
};

let __extractFailed = null;
try {
for (const c of ['ROM176_WOMEN','ROM176_MEET_NODES','ROM176_GREET','ROM176_TEA_LINES','ROM183_GREET_MET','ROM183_PACK_GREET'])
  eval(extractConst(c).replace('const ' + c + ' =', 'var ' + c + ' ='));
eval(extractConst('ROM176_P').replace('const ROM176_P =', 'var ROM176_P ='));
eval(extractConst('TRAVEL114_DAILY_CAP').replace('const TRAVEL114_DAILY_CAP =', 'var TRAVEL114_DAILY_CAP ='));
for (const f of ['enc79Hash','enc79Rand','enc79LocName','enc79StoryPendingAt','weekNumNow',
  'rom176SetEncounter','rom176BackOpts','rom176WomanDef','rom176WomanName','rom176IsWomanNpc',
  'rom176WomanMet','rom176MeiUnlocked','rom176WhisperActive','rom176BeatOpen','rom176PresenceP',
  'rom176EnsureDay','rom176PresenceAt','rom176GrantWhisper','rom176TeaTargets','rom176TryIntercept',
  'rom176PlayEncounter',
  'rom183XuMetBefore183','rom183RelVal183','rom183RelText183','rom183RelLine183','rom183WhoLine183',
  'rom183ApplyLineOverrides','rom183ApplyGiftReactFix',
  'travel114State','travel114Remain','travel114IsFree','travel114TrySpend']) eval(extractFn(f));
} catch (e) { __extractFailed = e; }
if (__extractFailed){
  console.log('FAIL harness: 抽取 ROM183／ROM176／travel114 函數失敗（pristine 預期反證） :: ' + __extractFailed.message);
  process.exit(1);
}
ok('harness: ROM183＋ROM176＋travel114 函數全載入',
  typeof rom183ApplyLineOverrides === 'function' && typeof rom183ApplyGiftReactFix === 'function'
  && typeof rom176PlayEncounter === 'function' && typeof travel114TrySpend === 'function');

function baseSave(over){
  return Object.assign({
    dayIndex: 0, fame: 5, flags: {}, story: { done: {}, rel: {} },
    inventory: {}, giftMeta: { lastGiveDay: {}, weekGiftGain: {}, givenCount: {} }, stars: null,
    mockRumors: [], mapTips: {}, npcs: {},
  }, over || {});
}

/* ---------- B1：感情進度讀 S.story.rel ---------- */
(function(){
  S = baseSave({ story: { done: {}, rel: { rel_hiu: 2, rel_choi: 0, rel_mei: 5 } } });
  ok('B1 rel 值讀 S.story.rel（hiu 2／choi 0／mei 5）',
    rom183RelVal183('hiu') === 2 && rom183RelVal183('choi') === 0 && rom183RelVal183('mei') === 5);
  ok('B1 人脈行文案「感情：好感 2／5」',
    rom183RelLine183('hiu') === '<div class="people-next">感情：好感 2／5</div>');
  ok('B1 非女角／空 key 唔出感情行', rom183RelLine183('') === '' && rom183RelLine183(null) === '');
  ok('B1 modal 細字「而家好感 2／5。」', rom183RelText183('hiu') === '而家好感 2／5。');
})();

/* ---------- B2：GiftShop IIFE 最愛獨立（抽真 IIFE，唔係 stub） ---------- */
(function(){
  let gsSrc = null;
  try {
    const i = html.indexOf('const GiftShop = (function(){');
    if (i < 0) throw new Error('GiftShop IIFE not found');
    let depth = 0, j = html.indexOf('{', i);
    for (; j < html.length; j++){ if (html[j] === '{') depth++; else if (html[j] === '}'){ depth--; if (depth === 0) break; } }
    gsSrc = html.slice(i, j + 1);
    if (html.slice(j + 1, j + 5) !== ')();') throw new Error('GiftShop IIFE end not )();');
    gsSrc = gsSrc + ')();';
  } catch (e) { ok('B2 harness: 抽取 GiftShop IIFE', false, e.message); return; }
  var GIFT_ITEMS = { items: [
    { itemId:'gift_thermos', name:'保溫瓶', deltaRel:{ default:1, liked:2, disliked:-1 } },
    { itemId:'gift_memo_pad', name:'拍紙簿', deltaRel:{ default:1, liked:2, disliked:-1 } },
    { itemId:'gift_coffee_beans', name:'咖啡豆', deltaRel:{ default:1, liked:2, disliked:-1 } },
    { itemId:'gift_perfume_sample', name:'淡香水', deltaRel:{ default:1, liked:2, disliked:-1 } },
  ] };
  var GIFT_SHOPS = { shops: [] };
  GIFT_PREFS = { npcs: {
    mei: { relKey:'rel_mei', displayName:'關海媚', requireFlagsAny:[],
      favorites:['gift_thermos','gift_memo_pad'], likes:['gift_thermos','gift_memo_pad','gift_coffee_beans','gift_cassette_indie'], dislikes:['gift_perfume_sample'] },
    hiu: { relKey:'rel_hiu', displayName:'林曉晴', requireFlagsAny:[],
      likes:['gift_thermos'], dislikes:[] },
  }, placeholderLines:{ liked:'L', dislike:'D', neutral:'N' } };
  GIFT_REACT = { byKey: {
    'mei:gift_thermos:liked': { npcKey:'mei', itemId:'gift_thermos', pref:'liked', lines:['關海媚：「保溫瓶啱用。」'] },
    'hiu:gift_thermos:liked': { npcKey:'hiu', itemId:'gift_thermos', pref:'liked', lines:['林曉晴：「保溫瓶啱用。」'] },
  }, entries: [], system: {} };
  var weekNumNow = function(){ return Math.floor(((S && S.dayIndex)||0)/7)+1; };
  S = baseSave({ inventory: { gift_thermos: 2, gift_coffee_beans: 1 }, giftMeta: { lastGiveDay: {}, weekGiftGain: {}, givenCount: {} } });
  let GS = null;
  try { GS = eval(gsSrc.replace('const GiftShop =', 'var __GS183 =') + '; __GS183;'); }
  catch (e) { ok('B2 harness: GiftShop IIFE 執行', false, e.message); return; }
  ok('B2 harness: GiftShop IIFE 執行', !!GS && typeof GS.prefKind === 'function');
  if (!GS) return;
  ok('B2 prefKind 最愛回 favorite（唔再併入 liked）', GS.prefKind('mei','gift_thermos') === 'favorite');
  ok('B2 prefKind 喜歡照回 liked', GS.prefKind('mei','gift_coffee_beans') === 'liked' && GS.prefKind('hiu','gift_thermos') === 'liked');
  ok('B2 prefKind 唔鍾意／普通不變', GS.prefKind('mei','gift_perfume_sample') === 'dislike' && GS.prefKind('hiu','gift_coffee_beans') === 'neutral');
  ok('B2 calcDelta 最愛同喜歡同數 +2（唔跌返 +1）',
    GS.giveGift && (function(){ const r = GS.giveGift('mei','gift_thermos'); return r.ok && r.delta === 2; })());
  S = baseSave({ inventory: { gift_thermos: 2 }, giftMeta: { lastGiveDay: {}, weekGiftGain: {}, givenCount: {} }, story: { done: {}, rel: {} } });
  ok('B2 reactionEntry 最愛查到 :liked 句（唔係 neutral fallback）',
    (function(){ const e = GS.reactionEntry('mei','gift_thermos','favorite'); return !!e && e.lines[0].indexOf('保溫瓶啱用') >= 0; })());
  ok('B2 reactionLine 最愛行 liked fallback（唔出 neutral 謝謝）',
    GS.reactionLine('mei','gift_thermos','favorite', false).indexOf('保溫瓶啱用') >= 0);
})();

/* ---------- B3：地點板在場行跟返巧遇盤 ---------- */
(function(){
  S = baseSave({ dayIndex: 0 });
  S.romDay = { day: 0, presence: { tvb_longmen: ['hiu'] }, triggered: 0, doneToday: { hiu: 'tvb_longmen' } };
  ok('B3 今日喺呢度撞過曉晴 → 在場行寫曉晴＋「今日已經撞過佢，聽日再嚟」',
    rom183WhoLine183(LOCS[0], 'lan').indexOf('林曉晴') >= 0
    && rom183WhoLine183(LOCS[0], 'lan').indexOf('今日已經撞過佢，聽日再嚟') >= 0);
  S.romDay.doneToday = {};
  ok('B3 未撞過 → 跌返 locNpc 行（藍若曦）',
    rom183WhoLine183(LOCS[0], 'lan').indexOf('藍若曦') >= 0);
  S.romDay.doneToday = { hiu: 'ad_central' };
  ok('B3 撞過但唔係呢個地點 → 唔寫佢',
    rom183WhoLine183(LOCS[0], 'lan').indexOf('曉晴') < 0);
  /* 整合：TryIntercept 入帳記埋地點，唔係 1 */
  __modals = []; __storyDone = {};
  S = baseSave({ dayIndex: 0 });
  S.romDay = { day: 0, presence: { tvb_longmen: ['hiu'] }, triggered: 0, doneToday: {} };
  S.romWeek = { week: 1, count: 0 }; S.romPity = {}; S.romLast = {};
  NPC_LINES = { colleague: { greet: ['舊 greet'] } };
  const r = rom176TryIntercept('tvb_longmen');
  ok('B3 TryIntercept 觸發＋doneToday 記地點（唔係 1）',
    r === true && S.romDay.doneToday.hiu === 'tvb_longmen', 'doneToday=' + JSON.stringify(S.romDay.doneToday));
})();

/* ---------- C1：pack greet[0] 改粵語（runtime 覆寫）＋C6 教學 ---------- */
(function(){
  NPC_LINES = {
    colleague: { greet: ['阿偉，今天在星河電視台廠房碰到你，真巧', '第二句'] },
    stylist: { greet: ['阿偉，今天的髮型總算聽話', '第二句'] },
    reporter: { greet: ['阿偉，又見面了，今天有甚麼可以寫進版面的？', '第二句'] },
  };
  TUTORIAL = { steps: [
    { id: 'TUT_MAP', body: ['a', 'b'] },
    { id: 'TUT_NPC', body: ['打聽句', '而家同熟人傾談或者送禮都唔會計一日。'], bodyAlt: ['打聽句', '傾談同送禮都唔佔日子。'] },
  ] };
  TUTORIAL_ZH_HK = null;
  rom183ApplyLineOverrides();
  ok('C1 三人 greet[0] 變粵語（冇 今天／廠房／甚麼）',
    NPC_LINES.colleague.greet[0].indexOf('今天') < 0 && NPC_LINES.colleague.greet[0].indexOf('廠房') < 0
    && NPC_LINES.stylist.greet[0].indexOf('今天') < 0 && NPC_LINES.reporter.greet[0].indexOf('甚麼') < 0
    && NPC_LINES.colleague.greet[0].indexOf('咁啱') >= 0);
  ok('C1 greet[1] 之後唔郁', NPC_LINES.colleague.greet[1] === '第二句');
  ok('C6 教學 TUT_NPC body 加巧遇句',
    TUTORIAL.steps[1].body[1].indexOf('撞到先可以傾談／送禮') >= 0);
  ok('C6 修正：TUT_MAP body 加第三句巧遇句（live 只行四步）',
    TUTORIAL.steps[0].body.length === 3 && TUTORIAL.steps[0].body[2].indexOf('撞到先可以傾談／送禮') >= 0);
  rom183ApplyLineOverrides();
  ok('C1/C6 覆寫冪等（再跑一次唔重複加句）',
    (TUTORIAL.steps[1].body[1].split('撞到先可以傾談').length - 1) === 1
    && TUTORIAL.steps[0].body.length === 3);
})();

/* ---------- C2：徐寶珊開場白分見過／未見過 ---------- */
(function(){
  __modals = []; __storyDone = {};
  NPC_LINES = {};
  S = baseSave({ dayIndex: 6 });
  rom176PlayEncounter('xu', 'ad_central', false);
  ok('C2 未見過 → 初遇版，冇「上次春茗」',
    __modals.length === 1 && __modals[0].body.indexOf('上次春茗') < 0
    && __modals[0].body.indexOf('啱啱先撞到') >= 0);
  __modals = [];
  rom176PlayEncounter('xu', 'ad_central', true);
  ok('C2 見過 → 講「上次春茗」',
    __modals.length === 1 && __modals[0].body.indexOf('上次春茗') >= 0);
  __modals = []; __storyDone = { R_xu_meet: true };
  rom176PlayEncounter('xu', 'ad_central');
  ok('C2 唔傳 metBefore 嗰陣跟 R_xu_meet（已播 → 春茗版）',
    __modals.length === 1 && __modals[0].body.indexOf('上次春茗') >= 0);
  __modals = []; __storyDone = {};
  rom176PlayEncounter('mei', 'ad_adm', false);
  ok('C4 海媚開場白冇括號舞台指示',
    __modals.length === 1 && __modals[0].body.indexOf('（佢望咗你一眼') < 0
    && __modals[0].body.indexOf('咁啱，喺呢度撞到你') >= 0);
})();

/* ---------- C3：55 條女角反應句過粵語 filter ---------- */
(function(){
  const pack = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gift_react_copy.json'), 'utf8'));
  GIFT_REACT = JSON.parse(JSON.stringify(pack));
  const before = GIFT_REACT.entries.length;
  rom183ApplyGiftReactFix();
  let bad = [];
  GIFT_REACT.entries.forEach(e => (e.lines || []).forEach(ln => { if (ln.indexOf('是不是') >= 0 || ln.indexOf('什麼') >= 0) bad.push(ln); }));
  ok('C3 55 條反應句再無「是不是」／「什麼」', bad.length === 0, 'bad=' + bad.length);
  ok('C3 條數不變（55 條，唔加唔減）', GIFT_REACT.entries.length === 55 && before === 55);
  const hiuThermos = GIFT_REACT.byKey['hiu:gift_thermos:liked'];
  ok('C3 曉晴保溫瓶句變粵語（係咪見到／唔該你）',
    !!hiuThermos && hiuThermos.lines[0].indexOf('係咪見到') >= 0);
  const starEnt = { npcKey: 'liu_bingxing', itemId: 'gift_pineapple_bun_set', pref: 'favorite', lines: ['廖炳星：「菠蘿油加奶茶券！」'] };
  GIFT_REACT.entries.push(starEnt);
  const hiuThermosN = GIFT_REACT.entries.filter(e => e.npcKey === 'hiu' && e.itemId === 'gift_thermos').length;
  rom183ApplyGiftReactFix();
  ok('C3 星反應句唔受影響＋覆寫冪等', starEnt.lines[0] === '廖炳星：「菠蘿油加奶茶券！」'
    && (GIFT_REACT.entries.filter(e => e.npcKey === 'hiu' && e.itemId === 'gift_thermos').length) === hiuThermosN);
})();

/* ---------- C9：travel114 免費旗唔扣額度 ---------- */
(function(){
  S = baseSave({ dayIndex: 0 });
  S.travel114 = { day: 0, used: 0 };
  ok('C9 免費入場（travelFree）唔扣額度',
    travel114TrySpend({ travelFree: true }, 'agency_ho') === true && S.travel114.used === 0);
  ok('C9 計數入場扣 1', travel114TrySpend({}, 'tvb_longmen') === true && S.travel114.used === 1);
  ok('C9 計數入場扣到上限 2 後擋住',
    travel114TrySpend({}, 'rec_star') === true && travel114TrySpend({}, 'film_cotton') === false && S.travel114.used === 2);
  S.travel114 = { day: 0, used: 2 };
  ok('C9 額度用完，免費返程照入得（encDone）',
    travel114TrySpend({ encDone: true }, 'tvb_longmen') === true && S.travel114.used === 2);
})();

console.log(fails ? ('FAILURES: ' + fails) : 'ALL PASS');
process.exit(fails ? 1 : 0);
