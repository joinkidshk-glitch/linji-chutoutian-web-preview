// v20a176 模擬校準（DESIGN §11.3）：專注追一位女角（林曉晴），每週去主場 3 日（Mon／Wed／Fri），
// 每次撞到送一份喜歡禮物（+2，女角每週軟頂 +2／週 → 每週最多 +2 rel），中位數幾多週到 rel 5。
// 超過 10 週就將 P(出) 0.50 調上 0.60，唔郁 caps。種子用真 rom176EnsureDay／rom176TryIntercept。
// 用法：node qa176/sim176.js
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
var window = {};
var localStorage = { getItem: ()=>null, setItem: ()=>{}, removeItem: ()=>{} };
var saveQ = function(){};
var toast = function(){};
var modal = function(){};
var S = null;
var GIGS = [];
var StoryOC = {
  ensure(){}, getFlag(){ return false; }, setFlag(){},
  isDone(){ return false; }, listOpen(){ return { open: [] }; },
  findNodeRaw(){ return null; }, evalNode(){ return { ok: false }; },
};
var rom176InEncounter = null;
var __played = [];
var rom176PlayEncounter = function(k, loc){ __played.push([k, loc]); };
eval(extractConst('ROM176_WOMEN').replace('const ROM176_WOMEN =', 'var ROM176_WOMEN ='));
eval(extractConst('ROM176_MEET_NODES').replace('const ROM176_MEET_NODES =', 'var ROM176_MEET_NODES ='));
eval(extractConst('ROM176_P').replace('const ROM176_P =', 'var ROM176_P ='));
for (const f of ['enc79Hash','enc79Rand','weekNumNow','enc79StoryPendingAt',
  'rom176SetEncounter','rom176BackOpts','rom176WomanDef','rom176WomanName','rom176IsWomanNpc',
  'rom176WomanMet','rom176MeiUnlocked','rom176WhisperActive','rom176BeatOpen','rom176PresenceP',
  'rom176EnsureDay','rom176PresenceAt','rom176GrantWhisper','rom176TeaTargets','rom176TryIntercept'])
  eval(extractFn(f));

function baseSave(){
  return { dayIndex: 0, fame: 5, flags: {}, story: { done: {}, rel: {} },
    inventory: {}, giftMeta: { lastGiveDay: {} }, stars: null, mockRumors: [], mapTips: {}, npcs: {} };
}

// 一次模擬：由 startDay 起，每週去主場 3 日（相對 Mon／Wed／Fri：start+0／2／4、+7／9／11…），追曉晴。
// 撞到曉晴 → 送喜歡禮物 +2（同週已 +2 就 +0）；撞到其他人唔加 rel。回傳到 rel 5 嘅週數（由 1 起計）。
// 注意：種子按 dayIndex 定死，唔同 run 一定要用唔同起步日，否則 100 次係同一條序列。
function oneRun(startDay){
  S = baseSave();
  let rel = 0, weekGift = 0, curWeek = -1;
  for (let w = 0; w < 52; w++){
    for (const off of [0, 2, 4]){
      const day = startDay + w * 7 + off;
      S.dayIndex = day;
      const wk = weekNumNow();
      if (wk !== curWeek){ curWeek = wk; weekGift = 0; }
      __played = [];
      if (rom176TryIntercept('tvb_longmen') && __played.length && __played[0][0] === 'hiu'){
        const gain = Math.min(2, 2 - weekGift); // 喜歡 +2，受每週 +2 軟頂
        rel += gain; weekGift += gain;
        if (rel >= 5) return w + 1;
      }
    }
  }
  return null; // 52 週都未到
}

const N = 100, out = [];
for (let i = 0; i < N; i++) out.push(oneRun((i * 37) % 365));
const done = out.filter(x=>x !== null).sort((a, b)=>a - b);
const median = done[Math.floor(done.length / 2)];
const p90 = done[Math.floor(done.length * 0.9)];
const dist = {};
done.forEach(x=>{ dist[x] = (dist[x] || 0) + 1; });
console.log('runs:', N, 'reached rel 5 within 52w:', done.length);
console.log('median weeks to rel 5:', median);
console.log('p90 weeks:', p90, 'max:', done[done.length - 1]);
console.log('distribution (weeks: count):', JSON.stringify(dist));
console.log('over 10 weeks:', done.filter(x=>x > 10).length, '/', done.length);
console.log('verdict:', median > 10 ? 'MEDIAN > 10w -> RAISE P 0.50 -> 0.60' : 'MEDIAN <= 10w -> KEEP P 0.50');
