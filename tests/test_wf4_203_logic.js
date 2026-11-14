// v20a203 WF4 迎新期＋Phase 2 擴池＋B3／C1 文案＋C2 場景圖＋C3 典禮撞強制播邏輯測試。
// 用法：node tests/test_wf4_203_logic.js [path-to-index.html]
// 反證：喺 pristine main（6e45cdb＝v193 落地）上行 → 冇 pDayWelcome／wf4EffPDay、
//   池得 72 單、set17／st17 舊文案、day15 moneyMax 1000、story165CanPlay 冇典禮閘 → 多項乾淨 FAIL（唔 crash）。
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
    else if(c === ';' && !started){ j++; break; }
  }
  return html.slice(i, j);
}
/* ---- sandbox（同 test_wf4_193_logic.js 形狀，加 C2／C3 stub） ---- */
let S;
let _ys = { year: 1990, season: '春' };
let _tier = 0;
let atLoc = null;
let _storyPlayLocked = false;
let _ceremonyOn = false;
const LOC_SHEET_BG = { cafe_cha: 'assets/story/locs/bg_loc_cafe_cha.jpg?v=20a104' };
function yearSeasonNow(){ return _ys; }
function enc79PlayerTier(){ return _tier; }
function ending78Locked(){ return false; }
function ending78Gate(){ return false; }
function todayIsForcedDay(){ return false; }
function conseq61IsSickToday(){ return false; }
function saveQ(){}
function apply(fx){ const n=[]; for(const k of Object.keys(fx||{})){ const v=fx[k]; if(typeof v!=='number'||!v) continue; n.push(k+v); } return n; } // v20a203：唔寫 S（跟 sim_wf4.js 嘅 apply-undefined 行為一致，sim 數字先對得上）
function modal(h, buttons, opts){ if(buttons && buttons[0] && buttons[0].on) buttons[0].on(); }
function openLoc(id, opts){}
function goToMapForBrowse(){}
function enc79StoryPendingAt(){ return false; }
function wf4PresentFenFarewell(){ return false; }
function isStoryPlayActive(){ return false; }
let _storyOpen = []; // 預設冇主線待播（sim 嗰陣 wf4TryLocEvent 唔 defer）；C3 嗰節先設做 [{id:'C6F'}]
const StoryOC = { ensure(){}, listOpen(){ return { open: _storyOpen }; } };
global.document = { querySelector: (sel) => (sel === '.awd62-stage' && _ceremonyOn) ? { node: 1 } : null };
const NEWS82_SRC = extractConst('NEWS82_EVENTS');
eval(NEWS82_SRC.replace('const NEWS82_EVENTS', 'global.NEWS82_EVENTS'));
const NEWS82_EVENTS = global.NEWS82_EVENTS;
const parts = [];
['DAILY_EVENTS_WF4','WF4_CFG','WF4_SCENE_OVERRIDE134'].forEach(n => parts.push(extractConst(n)));
['wf4Ensure','wf4Hash','wf4Rand','wf4NewsDay','wf4YearSeason','wf4Tier','wf4BaseOk','wf4CondOk','wf4PickEvent',
 'wf4ApplyFx','wf4Esc','wf4Scene105','wf4PlayEvent','wf4Fire','wf4DailyTick','wf4TryLocEvent','wf4PresentPending',
 'story165NextOpen','story165CanPlay'].forEach(n => parts.push(extractFn(n)));
/* v203 新增函數（pristine 冇）：抽唔到就用 stub 頂住，等斷言乾淨 FAIL，唔好成個測試 crash */
['wf4EffPDay','wf4EffPLoc','awards62CeremonyActive'].forEach(n => {
  try { parts.push(extractFn(n)); }
  catch(e) { parts.push('function ' + n + '(){ return NaN; }'); }
});
eval(parts.join('\n') + '; global.__W = { DAILY_EVENTS_WF4, WF4_CFG, WF4_SCENE_OVERRIDE134, wf4Ensure, wf4BaseOk, wf4CondOk, wf4PickEvent, wf4Fire, wf4DailyTick, wf4TryLocEvent, wf4PresentPending, wf4EffPDay, wf4EffPLoc, wf4Scene105, awards62CeremonyActive, story165CanPlay };');
const W = global.__W;
function freshS(day){
  return { dayIndex: day||0, money: 12000, stress: 50, stamina: 60, fame: 10, popularity: 10, acting: 10, charm: 10, stage: 10,
    mockRumors: [], mockDebts: [], mockCredits: [], story: { done:{}, flags:{} } };
}
function approx(a, b){ return Math.abs(a - b) < 1e-3; } // 曲線值 0.033／0.032 係四捨五入寫法，容差 1e-3

/* (1) 迎新期曲線：CFG 值＋漸降數值（day 0／15／29／30） */
{
  ok('WF4_CFG pDayWelcome 0.12', W.WF4_CFG.pDayWelcome === 0.12);
  ok('WF4_CFG pLocWelcome 0.08', W.WF4_CFG.pLocWelcome === 0.08);
  ok('WF4_CFG welcomeDays 30', W.WF4_CFG.welcomeDays === 30);
  ok('WF4_CFG 基線 pDay／pLoc 仲係 0.03', W.WF4_CFG.pDay === 0.03 && W.WF4_CFG.pLoc === 0.03);
  ok('wf4EffPDay(0)=0.12／(15)=0.075／(29)=0.033／(30)=0.03',
    approx(W.wf4EffPDay(0), 0.12) && approx(W.wf4EffPDay(15), 0.075) && approx(W.wf4EffPDay(29), 0.033) && approx(W.wf4EffPDay(30), 0.03));
  ok('wf4EffPLoc(0)=0.08／(15)=0.055／(29)=0.032／(30)=0.03',
    approx(W.wf4EffPLoc(0), 0.08) && approx(W.wf4EffPLoc(15), 0.055) && approx(W.wf4EffPLoc(29), 0.032) && approx(W.wf4EffPLoc(30), 0.03));
  ok('迎新期之後全程基線（day 100／500／1000 都係 0.03）',
    W.wf4EffPDay(100) === 0.03 && W.wf4EffPDay(1000) === 0.03 && W.wf4EffPLoc(100) === 0.03 && W.wf4EffPLoc(1000) === 0.03);
}

/* (2) 迎新期頭 30 日密度（inline sim，seeded 確定性數字；對照 qa203/sim_output.txt） */
{
  function runRoute(days, routeFn){
    S = freshS(0); _ys = { year: 1990, season: '春' }; _tier = 0;
    W.wf4Ensure();
    const fired = [];
    for(let d = 0; d < days; d++){
      S.dayIndex = d;
      const dt = new Date(1990, 0, 1 + d);
      _ys = { year: dt.getFullYear(), season: (dt.getMonth()+1>=3&&dt.getMonth()+1<=5)?'春':(dt.getMonth()+1>=6&&dt.getMonth()+1<=8)?'夏':(dt.getMonth()+1>=9&&dt.getMonth()+1<=11)?'秋':'冬' };
      _tier = d < 100 ? 0 : d < 400 ? 1 : 2;
      const snap = Object.assign({}, S.wf4.seen);
      W.wf4DailyTick();
      for(const loc of routeFn(d)){ W.wf4TryLocEvent(loc); }
      W.wf4PresentPending();
      for(const id of Object.keys(S.wf4.seen)){
        if(id === '__n') continue;
        if((S.wf4.seen[id]||0) > (snap[id]||0)) fired.push({ day: d, id });
      }
    }
    return fired;
  }
  const routes = {
    A: d => [['film_lion','tvb_longmen','cafe_cha','film_cotton','film_harbour','tvb_harbour','tvb_kowloon'][d%7],
             ['film_lion','tvb_longmen','cafe_cha','film_cotton','film_harbour','tvb_harbour','tvb_kowloon'][(d+3)%7]],
    B: () => ['tvb_longmen','cafe_cha'],
    C: () => ['film_lion','film_cotton'],
    D: () => ['cafe_cha','cafe_cha'],
  };
  const expect30 = { A: 4, B: 5, C: 2, D: 4 }; // sim 實測；pristine v193 係 A2／B3／C1／D1
  for(const [label, fn] of Object.entries(routes)){
    const fired = runRoute(30, fn);
    ok(`迎新期頭 30 日 ${label} 路線 ${expect30[label]} 單（sim 實測，唔係感覺）`, fired.length === expect30[label]);
  }
  // 三年四路線重複率 0%（硬指標，池 113 下重驗）
  for(const [label, fn] of Object.entries(routes)){
    const fired = runRoute(1095, fn);
    const ids = fired.map(f=>f.id);
    ok(`三年模擬 ${label} 路線重複率 0%（${fired.length} 單，${new Set(ids).size} 唔同）`,
      fired.length === new Set(ids).size && fired.length > 0);
  }
}

/* (3) B3：set17 嗰句改寫＋st17 換晒場景／人物／慰勞方式（day12／day04 保留做對照） */
{
  const evs = W.DAILY_EVENTS_WF4;
  const byId = id => evs.find(e=>e.id===id);
  const txt17 = JSON.stringify(byId('wf4_ev_set17'));
  ok('B3 set17 唔再有「我喊埋一份」', !txt17.includes('我喊埋一份'));
  ok('B3 set17 唔再有「喊戲」', !txt17.includes('喊戲'));
  ok('B3 set17 仲係錄影廠門口粉絲認人（標題／地點唔變）',
    byId('wf4_ev_set17').title === '錄影廠門口嗰班粉絲' && byId('wf4_ev_set17').loc === 'tvb_longmen');
  const st17 = byId('wf4_ev_st17');
  const txtSt17 = JSON.stringify(st17);
  ok('B3 st17 改做樓下士多豆漿（標題／場景換晒）',
    st17.title === '樓下士多嗰支豆漿' && st17.setting.includes('士多'));
  ok('B3 st17 唔再有涼茶舖／阿婆／廿四味',
    !txtSt17.includes('涼茶') && !txtSt17.includes('廿四味') && !txtSt17.includes('阿婆'));
  ok('B3 st17 講者係士多阿叔（唔係涼茶阿婆）',
    st17.beats.some(b=>b.sp==='士多阿叔'));
  ok('B3 對照：day12「我喊埋一份」保留（全池得呢一處）',
    JSON.stringify(byId('wf4_ev_day12')).includes('我喊埋一份'));
  ok('B3 對照：day04 涼茶阿婆廿四味保留（全池得呢一處）',
    JSON.stringify(byId('wf4_ev_day04')).includes('廿四味') && JSON.stringify(byId('wf4_ev_day04')).includes('涼茶阿婆'));
}

/* (4) C1：點歌只留一單＋銀包分層閘 */
{
  const evs = W.DAILY_EVENTS_WF4;
  const byId = id => evs.find(e=>e.id===id);
  const sing = evs.filter(e=>JSON.stringify(e).includes('點歌')).map(e=>e.id);
  ok('C1「點歌」全池只留 set21 一單（st15 已改做司機追星往事）',
    JSON.stringify(sing) === JSON.stringify(['wf4_ev_set21']));
  ok('C1 st15 改做司機追星往事（標題／講者／beat 換晒，唔再係點歌）',
    byId('wf4_ev_st15').title === '的士司機嗰段追星往事'
    && byId('wf4_ev_st15').beats.some(b=>b.sp==='的士司機')
    && JSON.stringify(byId('wf4_ev_st15')).includes('追星')); // 「追星」喺旁白句（司機講起追星往事）＋司機句講追夢
  ok('C1 day15 閘改做 moneyMax 200（同 day03 ≤$1000 分層）',
    byId('wf4_ev_day15').cond.moneyMax === 200 && byId('wf4_ev_day03').cond.moneyMax === 1000);
  // 分層實證：錢 $500 → day03 出、day15 唔出；錢 $150 → 兩單都出
  S = freshS(100); _ys = { year: 1990, season: '春' }; _tier = 0; S.money = 500;
  ok('C1 分層：銀包 $500，day03 合資格、day15 唔合資格',
    W.wf4CondOk(byId('wf4_ev_day03')) === true && W.wf4CondOk(byId('wf4_ev_day15')) === false);
  S.money = 150;
  ok('C1 分層：銀包 $150，兩單都合資格（唔係封死咗 day15）',
    W.wf4CondOk(byId('wf4_ev_day03')) === true && W.wf4CondOk(byId('wf4_ev_day15')) === true);
}

/* (5) C2：場景圖重映射（wf4Scene105 實讀覆寫表） */
{
  const scene = id => W.wf4Scene105(W.DAILY_EVENTS_WF4.find(e=>e.id===id));
  ok('C2 day05 冰室→茶餐廳圖（唔再係街市）', scene('wf4_ev_day05').includes('bg_loc_cafe_cha.jpg'));
  ok('C2 day07 電車→的士車廂圖（唔再係電話亭）', scene('wf4_ev_day07').includes('bg_wf4_taxi.jpg'));
  ok('C2 day09 唱片舖→店舖圖（唔再係街市）', scene('wf4_ev_day09').includes('bg_loc_gift_shop.jpg'));
  ok('C2 day11 茶樓→茶餐廳圖（唔再係街市）', scene('wf4_ev_day11').includes('bg_loc_cafe_cha.jpg'));
  ok('C2 day14 片場休息區→獅子山廠圖（唔再係電話亭）', scene('wf4_ev_day14').includes('bg_loc_film_lion.jpg'));
  ok('C2 day15 茶餐廳門口→茶餐廳圖本身（唔再係街市）', scene('wf4_ev_day15').includes('bg_loc_cafe_cha.jpg'));
  ok('C2 st17 士多→店舖圖（唔再係街市）', scene('wf4_ev_st17').includes('bg_loc_gift_shop.jpg'));
  const expectNew = {
    wf4_ev_day17: 'bg_wf4_home.jpg', wf4_ev_day18: 'bg_wf4_market.jpg', wf4_ev_day19: 'bg_wf4_home.jpg',
    wf4_ev_day20: 'bg_loc_gift_shop.jpg', wf4_ev_day21: 'bg_loc_gift_shop.jpg', wf4_ev_day22: 'bg_wf4_taxi.jpg',
    wf4_ev_day23: 'bg_wf4_market.jpg', wf4_ev_day24: 'bg_wf4_home.jpg', wf4_ev_day25: 'bg_wf4_market.jpg',
    wf4_ev_day26: 'bg_wf4_taxi.jpg', wf4_ev_day27: 'bg_wf4_taxi.jpg', wf4_ev_day28: 'bg_wf4_home.jpg',
  };
  ok('C2 12 單新 day 事件全部有場景圖（唔留灰）',
    Object.entries(expectNew).every(([id, f])=>scene(id).includes(f)));
  ok('C2 對照：st05 卡拉OK／st08 的士圖唔郁', scene('wf4_ev_st05').includes('bg_wf4_karaoke.jpg') && scene('wf4_ev_st08').includes('bg_wf4_taxi.jpg'));
}

/* (6) C3：典禮進行中唔開強制播（防兩層疊埋）；典禮完咗故事照開，唔會唔見 */
{
  S = freshS(98); _ys = { year: 1990, season: '春' }; _tier = 1;
  _storyOpen = [{ id: 'C6F' }]; // C6F 待播（v198 defer 嗰套唔影響呢節：CanPlay 只驗典禮閘）
  _ceremonyOn = false;
  ok('C3 冇典禮嗰陣 CanPlay 照返 C6F', W.story165CanPlay() && W.story165CanPlay().id === 'C6F');
  ok('C3 awards62CeremonyActive 冇 stage 返 false', W.awards62CeremonyActive() === false);
  _ceremonyOn = true; // .awd62-stage 喺 DOM（典禮進行中）
  ok('C3 awards62CeremonyActive 有 stage 返 true', W.awards62CeremonyActive() === true);
  ok('C3 典禮進行中 CanPlay 返 null（唔開強制播，唔疊層）', W.story165CanPlay() === null);
  _ceremonyOn = false; // 典禮播完，stage 拆走
  ok('C3 典禮完咗 CanPlay 即刻返 C6F（故事唔會唔見，唔使等下一日）',
    W.story165CanPlay() && W.story165CanPlay().id === 'C6F');
}

console.log(fails.length ? ('FAILURES: ' + fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
