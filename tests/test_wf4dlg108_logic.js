// v20a108 D-8（二期）邏輯測試：WF4 隨機事件具名講者企立
// 用法：node tests/test_wf4dlg108_logic.js [path-to-index.html] [path-to-baseline-index.html]
// 反證：(a) 斷資產路徑——dlg106Candidates 換成淨返一條爛路徑，chars html 嘅
//       後備鏈仍須含 bust／剪影／SVG 兜底（證明後備行到，唔會停喺斷鏈）；
//       (b) 資產表閘——dlg106HasFullbody 恒 false 時 onTable 必須歸零、
//       beat 改行舊呈現（證明路由真係睇資產表，唔係硬編）；
//       (c) 傳入舊版 index（argv[3]）時 wf4SpeakerId108 必須唔存在。
// 資料一律由 index.html 抽真身（DLG106 模組＋WF4 函數＋DAILY_EVENTS_WF4），唔用手抄副本。
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const root = path.dirname(path.resolve(htmlPath));
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS ' : 'FAIL ') + name); }
function info(msg){ console.log('INFO ' + msg); }
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

/* ---- sandbox stubs（modal 捕獲式，唔自動撳掣，逐步驗呈現） ---- */
let S;
function freshS(){ return { dayIndex:0, money:1000, stress:30, stamina:60, fame:10, popularity:10, acting:10, charm:10, stage:10, looks:10, iq:10 }; }
let atLoc = 'cafe_cha';
const LOC_SHEET_BG = { cafe_cha:'assets/story/locs/cafe_cha.png?v=20a105', film_lion:'assets/story/locs/film_lion.png?v=20a105' };
let modalCalls = [];
function modal(html, buttons, opts){ modalCalls.push({ html, buttons: buttons||[], labels:(buttons||[]).map(b=>b.label) }); }
function clickBtn(idx){ const c = modalCalls[modalCalls.length-1]; const b = c.buttons[idx||0]; if(b && b.on) b.on(); }
function apply(fx){ const notes=[]; for(const k of Object.keys(fx||{})){ const v=fx[k]; if(typeof v!=='number'||!v) continue; if(k==='money') S.money=Math.max(0,(S.money||0)+v); else S[k]=Math.max(0,(S[k]||0)+v); notes.push(k+v); } return notes; }
function saveQ(){}

/* ---- DLG106 模組真身（window／級數 stub；tier 0＝阿偉 s1） ---- */
global.window = {};
global.__tier108 = 0;
global.enc79PlayerTier = () => global.__tier108;
const a106 = html.indexOf('/* ===== v20a106 DLG106');
const b106 = html.indexOf('/* ===== DLG106 模組完 ===== */');
ok('搵到 DLG106 模組', a106 >= 0 && b106 > a106);
eval(html.slice(a106, b106) + '\n;({DLG106_GAZE})');
// function 宣告經 eval 已入 scope：dlg106ResolveSides/dlg106ResolveCategory/
// dlg106Candidates/dlg106HasFullbody/dlg106AweiStem/dlg106ExprFor
/* 候補鏈尾段：SVG／剪影抽真身（extractConst 會喺字串內 ; 截斷，改用引號感知 regex）；
   UI40_STAND（433KB base64）用標記 stub 代替本體 */
function extractQuotedConst(name){
  const m = html.match(new RegExp('const ' + name + ' = "((?:[^"\\\\]|\\\\.)*)"'));
  if(!m) throw new Error('const not found: ' + name);
  return eval('"' + m[1] + '"'); /* 字串本體原樣求值（內無雙引號，已核對） */
}
global.ENC105_STAND_FALLBACK = extractQuotedConst('ENC105_STAND_FALLBACK');
global.ENC105_STAND_SILHOUETTE = extractQuotedConst('ENC105_STAND_SILHOUETTE');
const UI40_STAND = { awi: 'data:image/png;base64,STUB108AWI' };

/* ---- WF4 真身 ---- */
const evs = eval(extractConst('DAILY_EVENTS_WF4').replace('const DAILY_EVENTS_WF4', 'let __evs108') + '\n;__evs108');
const __wf4code108 = ['wf4Scene105','wf4PlayEvent','wf4ApplyFx','wf4Esc',
 'wf4SpeakerId108','wf4OnTableIds108','wf4DlgExtraCands108','wf4DlgCharsHtml108','wf4BeatStageHtml108'
].map(n => extractFn(n)).join('\n');
eval(__wf4code108); /* 頂層直接 eval：function 宣告入模組作用域（forEach 回呼內 eval 唔會漏出） */

const NEW108 = ['wf4_ev_cha02','wf4_ev_home01','wf4_ev_st01','wf4_ev_st03','wf4_ev_boss01','wf4_ev_boss02','wf4_ev_boss03','wf4_ev_day02'];
const byId = id => evs.find(e => e.id === id);
function imgOf(stageHtml){
  const m = stageHtml.match(/<img class="dlg106-char([^"]*)" src="([^"]*)"[^>]*data-dlg-fallbacks="([^"]*)"[^>]*style="([^"]*)"/);
  if(!m) return null;
  return { cls:m[1], src:m[2], fallbacks:m[3], style:m[4] };
}

/* ---- (1) 盤點：72 事件，8 單新路徑（只得阿偉），64 單舊路徑（v20a193 新事件唔用阿偉做講者） ---- */
{
  ok('WF4 事件總數 72（v20a193）', evs.length === 72);
  const routed = evs.map(e => ({ id:e.id, on:wf4OnTableIds108(e) }));
  const newIds = routed.filter(r => r.on.length).map(r => r.id).sort();
  ok('新路徑 8 單＝cha02/home01/st01/st03/boss01/boss02/boss03/day02',
    JSON.stringify(newIds) === JSON.stringify(NEW108.slice().sort()));
  ok('舊路徑 64 單（v20a193：28 舊＋36 新，全部冇阿偉講者）', routed.filter(r => !r.on.length).length === 64);
  ok('新路徑 onTable 全部只含 awi（冇第二個全身講者）',
    routed.every(r => r.on.every(id => id === 'awi')));
  ok('三人事件（boss01-03）同樣只出阿偉獨角（唔會多角輪換出假人）',
    ['wf4_ev_boss01','wf4_ev_boss02','wf4_ev_boss03'].every(id => JSON.stringify(wf4OnTableIds108(byId(id))) === '["awi"]'));
  info('具名但冇資產（行舊路徑）：阿媽／霞姐／阿成／昌叔／表姨媽＋全部功能 NPC');
}

/* ---- (2) 講者映射 ---- */
{
  ok('阿偉→awi', wf4SpeakerId108('阿偉') === 'awi');
  const off = ['阿媽','霞姐','阿成','昌叔','表姨媽','老闆娘','場務','副導演','武指','收音師','臨記頭','甘草老戲骨','茶客阿叔','茶客後生仔','鄰枱茶客','鄰居嬸嬸','前面阿姐','冰室伙記','臨記朋友','魚檔阿姐','影碟舖老闆','的士司機','老燈光師','涼茶阿婆','茶水阿姐','旁白','',null,undefined];
  ok('具名家人／熟人／功能 NPC／旁白全部→null（表外）', off.every(s => wf4SpeakerId108(s) === null));
}

/* ---- (3) 阿偉表情分類（真函數：map→分類器） ---- */
{
  const expect = { wf4_ev_cha02:'neutral', wf4_ev_home01:'neutral', wf4_ev_st01:'neutral',
    wf4_ev_st03:'think', wf4_ev_boss01:'neutral', wf4_ev_boss02:'neutral',
    wf4_ev_boss03:'happy', wf4_ev_day02:'sad' };
  let bad = [];
  for(const id of NEW108){
    const ev = byId(id);
    const line = ev.beats.find(b => b.sp === '阿偉');
    const cat = dlg106ResolveCategory({ text:line.tx, speakerId:'awi' });
    if(cat !== expect[id]) bad.push(id + ':' + cat);
  }
  ok('8 單阿偉句分類＝neutral×5／think／happy／sad（st03 think、boss03 happy、day02 sad）', bad.length === 0);
  if(bad.length) info('分類不符：' + bad.join('；'));
}

/* ---- (4) 獨角企位：視線表左位唔翻 ---- */
{
  const sides = dlg106ResolveSides('awi', 'awi');
  ok('awi 獨角＝single 左位 flip false', !!sides && !!sides.single && sides.single.id === 'awi' && sides.single.side === 'left' && sides.single.flip === false);
  const ch = wf4DlgCharsHtml108(byId('wf4_ev_st03'), byId('wf4_ev_st03').beats[1]);
  ok('chars html 係 dlg106-left、冇 dlg106-right、冇 dlg106-flip',
    ch.includes('dlg106-left') && !ch.includes('dlg106-right') && !ch.includes('dlg106-flip'));
}

/* ---- (5) st03 逐句：旁白齊暗冇名牌 → 阿偉 think 全光 ---- */
{
  const ev = byId('wf4_ev_st03');
  const s0 = wf4BeatStageHtml108(ev, ev.beats[0], 'assets/story/locs/cafe_cha.png');
  ok('st03 beat0（旁白）行 narration 舞台＋narration 板', s0.includes('sp-mode-narration') && s0.includes('sp-plate-narration105'));
  ok('st03 beat0 冇名牌（sp-speaker 唔出現）', !s0.includes('sp-speaker'));
  const im0 = imgOf(s0);
  ok('st03 beat0 阿偉 base＋0.6（聽者／旁白態）', !!im0 && im0.src.includes('awi_base.webp') && im0.style.includes('brightness(0.6)'));
  const s1 = wf4BeatStageHtml108(ev, ev.beats[1], 'assets/story/locs/cafe_cha.png');
  ok('st03 beat1（阿偉）行 dialogue 舞台＋名牌「阿偉」', s1.includes('sp-mode-dialogue') && s1.includes('<div class="sp-speaker">阿偉</div>'));
  const im1 = imgOf(s1);
  ok('st03 beat1 阿偉 think 圖＋brightness(1)＋z-index 4（表情切換睇得出）',
    !!im1 && im1.src.includes('awi_think.webp') && im1.style.includes('brightness(1)') && im1.style.includes('z-index:4'));
  ok('st03 兩句同一人但圖／明暗唔同（base 0.6 → think 1.0）',
    !!im0 && !!im1 && im0.src !== im1.src && im0.style !== im1.style);
}

/* ---- (6) cha02：阿成講嘢嗰句阿偉留台做聽者；day02／boss03 表情 ---- */
{
  const ev = byId('wf4_ev_cha02');
  const s0 = wf4BeatStageHtml108(ev, ev.beats[0], 'assets/story/locs/cafe_cha.png');
  ok('cha02 beat0（阿成）名牌「阿成」、阿偉 base 0.6 在場',
    s0.includes('<div class="sp-speaker">阿成</div>') && (imgOf(s0) || {}).style.includes('brightness(0.6)'));
  const s1 = wf4BeatStageHtml108(ev, ev.beats[1], 'assets/story/locs/cafe_cha.png');
  const im1 = imgOf(s1);
  ok('cha02 beat1（阿偉）base 全光', !!im1 && im1.src.includes('awi_base.webp') && im1.style.includes('brightness(1)'));
  const d2 = byId('wf4_ev_day02');
  const imD = imgOf(wf4BeatStageHtml108(d2, d2.beats[1], ''));
  ok('day02 阿偉句出 sad 圖＋全光', !!imD && imD.src.includes('awi_sad.webp') && imD.style.includes('brightness(1)'));
  const b3 = byId('wf4_ev_boss03');
  const imB = imgOf(wf4BeatStageHtml108(b3, b3.beats[2], ''));
  ok('boss03 阿偉句出 smile 圖＋全光', !!imB && imB.src.includes('awi_smile.webp') && imB.style.includes('brightness(1)'));
  ok('冇場景圖（scene105 空字串）照出舞台（漸變底兜底）', wf4BeatStageHtml108(d2, d2.beats[1], '').includes('sp-bg-layer'));
}

/* ---- (7) 候補鏈：全身圖→企立／bust→剪影→SVG 兜底＋__dlg106Err ---- */
{
  const ev = byId('wf4_ev_st03');
  const im = imgOf(wf4BeatStageHtml108(ev, ev.beats[1], ''));
  ok('候補鏈含 bust（char_hero_bust_default）', !!im && im.fallbacks.includes('char_hero_bust_default.png'));
  ok('候補鏈含 ENC105 剪影', !!im && im.fallbacks.includes('enc105_stand_silhouette.png'));
  ok('候補鏈以 SVG data URI 收尾（必載入到）', !!im && im.fallbacks.split('|').pop().startsWith('data:image/svg+xml'));
  ok('候補鏈首選係全身 think webp', !!im && im.src.includes('awi_think.webp?v=20a106'));
  ok('img 掛 onerror＝__dlg106Err', wf4BeatStageHtml108(ev, ev.beats[1], '').includes('window.__dlg106Err'));
  /* __dlg106Err 真身：mock img 逐級退圖，耗盡隱藏唔出破圖 */
  const errFn = global.window.__dlg106Err;
  ok('__dlg106Err 已載入', typeof errFn === 'function');
  if(typeof errFn === 'function'){
    const mk = fb => ({ src:'BROKEN', style:{}, _fb:fb,
      getAttribute(k){ return k === 'data-dlg-fallbacks' ? this._fb : null; },
      setAttribute(k, v){ if(k === 'data-dlg-fallbacks') this._fb = v; } });
    const img = mk('NEXT1|NEXT2');
    errFn(img); ok('err 第 1 級→NEXT1', img.src === 'NEXT1' && img._fb === 'NEXT2');
    errFn(img); ok('err 第 2 級→NEXT2', img.src === 'NEXT2' && img._fb === '');
    errFn(img); ok('err 耗盡→隱藏（visibility hidden，唔出破圖）', img.style.visibility === 'hidden');
  }
}

/* ---- (8) 反證 A：斷資產路徑，後備鏈仍行到 ---- */
{
  const realCands = dlg106Candidates;
  dlg106Candidates = () => ['assets/story/fullbody/NOPE_broken.webp?v=20a106'];
  const ev = byId('wf4_ev_st03');
  const im = imgOf(wf4DlgCharsHtml108(ev, ev.beats[1]));
  ok('反證A：首選爛路徑時 fallbacks 仍有 bust／剪影／SVG（唔會停喺斷鏈）',
    !!im && im.src.includes('NOPE_broken.webp') && im.fallbacks.includes('char_hero_bust_default.png')
    && im.fallbacks.includes('enc105_stand_silhouette.png') && im.fallbacks.includes('data:image/svg+xml'));
  dlg106Candidates = realCands;
  const im2 = imgOf(wf4DlgCharsHtml108(ev, ev.beats[1]));
  ok('反證A 還原後首選返 think 圖', !!im2 && im2.src.includes('awi_think.webp'));
}

/* ---- (9) 反證 B：資產表閘——冇全身資產就歸零行舊路徑 ---- */
{
  const realHas = dlg106HasFullbody;
  dlg106HasFullbody = () => false;
  ok('反證B：hasFullbody 恒 false → onTable 歸零', wf4OnTableIds108(byId('wf4_ev_st03')).length === 0);
  ok('反證B：onTable 歸零 → stage html 係空字串', wf4BeatStageHtml108(byId('wf4_ev_st03'), byId('wf4_ev_st03').beats[1], '') === '');
  dlg106HasFullbody = realHas;
  ok('反證B 還原後 onTable 返 ["awi"]', JSON.stringify(wf4OnTableIds108(byId('wf4_ev_st03'))) === '["awi"]');
}

/* ---- (10) 舊路徑全程：set01（場務／旁白）維持 v105 舊呈現＋數值入帳 ---- */
{
  S = freshS(); modalCalls = [];
  let done = false;
  wf4PlayEvent(byId('wf4_ev_set01'), () => { done = true; });
  ok('set01 beat0 有 v105 場景帶、冇 dlg106-char', modalCalls.length === 1
    && modalCalls[0].html.includes('wf4-scene105') && !modalCalls[0].html.includes('dlg106-char')
    && !modalCalls[0].html.includes('fullbody'));
  clickBtn(0);
  ok('set01 beat1 同樣舊呈現', modalCalls.length === 2 && !modalCalls[1].html.includes('dlg106-char'));
  clickBtn(0);
  ok('set01 到抉擇（2 個選擇）', modalCalls.length === 3 && modalCalls[2].labels.length === 2);
  clickBtn(0);
  ok('set01 結算有 out 文案', modalCalls.length === 4 && modalCalls[3].html.includes('好意頭'));
  clickBtn(0);
  ok('set01 播完 doneCb 有叫', done === true);
  ok('set01 揀項 fx 入帳（stress 30→28、fame 10→11）', S.stress === 28 && S.fame === 11);
}

/* ---- (11) 新路徑全程：st03（tail）＋boss03（choices）---- */
{
  S = freshS(); modalCalls = [];
  let done = false;
  wf4PlayEvent(byId('wf4_ev_st03'), () => { done = true; });
  ok('st03 beat0 舞台＋場景底（cafe_cha）', modalCalls.length === 1
    && modalCalls[0].html.includes('dlg106-on') && modalCalls[0].html.includes('cafe_cha.png'));
  clickBtn(0);
  ok('st03 beat1 舞台（think 全光）', modalCalls.length === 2 && modalCalls[1].html.includes('awi_think.webp'));
  clickBtn(0);
  ok('st03 結算係 tail 舊文字、唔含 dlg106-char', modalCalls.length === 3
    && modalCalls[2].html.includes('買咗支汽水') && !modalCalls[2].html.includes('dlg106-char'));
  clickBtn(0);
  ok('st03 播完 doneCb 有叫＋tail fx 入帳（stress 30→32）', done === true && S.stress === 32);

  S = freshS(); modalCalls = [];
  let done3 = false;
  wf4PlayEvent(byId('wf4_ev_boss03'), () => { done3 = true; });
  ok('boss03 三句全部舞台', modalCalls.length === 1 && modalCalls[0].html.includes('dlg106-on'));
  clickBtn(0); clickBtn(0);
  ok('boss03 beat2（阿偉）smile 全光', modalCalls[2].html.includes('awi_smile.webp'));
  clickBtn(0);
  ok('boss03 到抉擇（2 個選擇）', modalCalls.length === 4 && modalCalls[3].labels.length === 2);
  clickBtn(0);
  ok('boss03 結算舊文字', modalCalls.length === 5 && modalCalls[4].html.includes('常餐走蔥'));
  clickBtn(0);
  ok('boss03 播完 doneCb 有叫', done3 === true);
}

/* ---- (12) 分工護欄：WF4 只出組件原有 class，唔加幾何／CSS ---- */
{
  const ev = byId('wf4_ev_st03');
  const s1 = wf4BeatStageHtml108(ev, ev.beats[1], 'assets/story/locs/cafe_cha.png');
  ok('分工：舞台 markup 冇 wf4 專屬 class（唔掂組件幾何）', !s1.includes('wf4-play') && !s1.includes('wf4_play'));
  ok('分工：舞台只用 v106 原有 class（sp-stage／dlg106-on／dlg106-plate）',
    s1.includes('class="sp-stage sp-mode-dialogue dlg106-on"') && s1.includes('dlg106-plate'));
  ok('分工：舞台 div 冇 inline 高／闊（幾何留返 v108-dlg）', !/sp-stage[^>]*style="[^"]*(height|width)/.test(s1));
}

/* ---- (13) 舊版反證（有傳 baseline 路徑先驗） ---- */
{
  if(process.argv[3]){
    const oldSrc = fs.readFileSync(path.resolve(process.argv[3]), 'utf8');
    ok('反證C：舊版 index 冇 wf4SpeakerId108（測試識分新舊）', !oldSrc.includes('function wf4SpeakerId108('));
    ok('反證C：舊版 index 冇 wf4BeatStageHtml108', !oldSrc.includes('function wf4BeatStageHtml108('));
  } else {
    info('反證C 跳過（未傳 baseline 路徑；跑全套 A/B 時對照 suite_baseline.txt）');
  }
}

console.log(fails.length ? ('FAILURES: ' + fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
