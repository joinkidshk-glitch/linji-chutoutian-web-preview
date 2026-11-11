// v20a114 TRAVEL114 邏輯測試：每日入地點出行額度（上限 2 次）。
//   斷言：第一次入場計 1、第二個唔同地點計 2、第三次被擋；重入同一地點都計；
//   travelFree／encDone／forceRestore／wf4Done／屋企（id "home"）唔計；
//   換日 rollover 歸零；舊檔（冇 S.travel114）初值滿額；save／load round-trip 後 used 一致。
// 反證：cap 改做 99 → 第三次入場要放行（測試即 FAIL 唔到）；計數行刪走 → used 永遠 0。
// 用法：node tests/test_travel114_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS ' : 'FAIL ') + name); }
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
function extractConstLine(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('const not found: ' + name);
  const j = html.indexOf('\n', i);
  return html.slice(i, j).replace(/;$/, '');
}
const CAP_SRC = extractConstLine('TRAVEL114_DAILY_CAP');
const FNS_SRC = ['travel114State', 'travel114Remain', 'travel114IsFree', 'travel114TrySpend']
  .map(extractFn).join('\n');
function makeSandbox(S, capSrc, fnsSrc){
  return new Function('S', (capSrc || CAP_SRC) + '\n' + (fnsSrc || FNS_SRC) +
    '\nreturn { travel114State, travel114Remain, travel114IsFree, travel114TrySpend, TRAVEL114_DAILY_CAP };')(S);
}

/* ---- (1) 基本計數：兩次放行，第三次擋 ---- */
let S = { dayIndex: 5 };
let api = makeSandbox(S);
ok('常量 TRAVEL114_DAILY_CAP = 2', api.TRAVEL114_DAILY_CAP === 2);
ok('舊檔（冇 S.travel114）初值滿額（remain 2）', api.travel114Remain() === 2);
ok('第一次入場（cafe_cha）放行', api.travel114TrySpend({}, 'cafe_cha') === true);
ok('第一次入場計 1（used 1／remain 1）', S.travel114.used === 1 && api.travel114Remain() === 1);
ok('第二個唔同地點（agency_ho）放行', api.travel114TrySpend({}, 'agency_ho') === true);
ok('第二次入場計 2（used 2／remain 0）', S.travel114.used === 2 && api.travel114Remain() === 0);
ok('第三次入場被擋', api.travel114TrySpend({}, 'tvb_longmen') === false);
ok('被擋唔扣數（used 仍然 2）', S.travel114.used === 2);

/* ---- (2) 重入同一地點都計（07:11 更正後規則，重點） ---- */
S = { dayIndex: 5 };
api = makeSandbox(S);
ok('重入：第一次入 cafe_cha 放行', api.travel114TrySpend({}, 'cafe_cha') === true);
ok('重入：第二次入返同一地點都計（放行，used 2）',
  api.travel114TrySpend({}, 'cafe_cha') === true && S.travel114.used === 2);
ok('重入：第三次入返同一地點被擋', api.travel114TrySpend({}, 'cafe_cha') === false);

/* ---- (3) 免費路徑唔計 ---- */
S = { dayIndex: 5 };
api = makeSandbox(S);
for(const [label, opts, id] of [
  ['travelFree', {travelFree:true}, 'cafe_cha'],
  ['encDone', {encDone:true}, 'cafe_cha'],
  ['forceRestore', {forceRestore:true}, 'cafe_cha'],
  ['wf4Done', {wf4Done:true}, 'cafe_cha'],
  ['屋企 id "home"', {}, 'home'],
]){
  ok(label + ' 放行', api.travel114TrySpend(opts, id) === true);
  ok(label + ' 唔計（remain 仍然 2）', api.travel114Remain() === 2);
}
ok('免費路徑之後，正常入場照計（used 1）',
  api.travel114TrySpend({}, 'cafe_cha') === true && S.travel114.used === 1);
ok('travel114IsFree 唔用 atLoc 做判據（唔可以靠佢分返轉頭定再入場）',
  extractFn('travel114IsFree').indexOf('atLoc') < 0);

/* ---- (4) 換日 rollover 歸零 ---- */
S = { dayIndex: 5, travel114: { day: 5, used: 2 } };
api = makeSandbox(S);
ok('同一日 remain 0（用晒）', api.travel114Remain() === 0);
S.dayIndex = 6;
ok('換日 rollover：used 歸零、remain 返 2', api.travel114Remain() === 2 && S.travel114.used === 0 && S.travel114.day === 6);
ok('換日之後入場照計', api.travel114TrySpend({}, 'cafe_cha') === true && S.travel114.used === 1);

/* ---- (5) save／load round-trip 後 used 一致 ---- */
S = { dayIndex: 5 };
api = makeSandbox(S);
api.travel114TrySpend({}, 'cafe_cha');
api.travel114TrySpend({}, 'agency_ho');
const loaded = JSON.parse(JSON.stringify(S));
const api2 = makeSandbox(loaded);
ok('round-trip 後 used 仍然 2（唔會重新載入刷返額度）',
  loaded.travel114.used === 2 && api2.travel114Remain() === 0);
ok('round-trip 後第三次入場仍然被擋', api2.travel114TrySpend({}, 'tvb_longmen') === false);

/* ---- (6) 反證 ---- */
S = { dayIndex: 5 };
const apiCap99 = makeSandbox(S, CAP_SRC.replace('= 2', '= 99'), FNS_SRC);
apiCap99.travel114TrySpend({}, 'cafe_cha');
apiCap99.travel114TrySpend({}, 'agency_ho');
ok('反證：cap 改做 99 → 第三次入場要放行（否則測試唔識捉 cap 改錯）',
  apiCap99.travel114TrySpend({}, 'tvb_longmen') === true);
S = { dayIndex: 5 };
const apiNoCount = makeSandbox(S, CAP_SRC, FNS_SRC.replace('st.used = (Number(st.used)||0) + 1;', '/* count removed */'));
apiNoCount.travel114TrySpend({}, 'cafe_cha');
apiNoCount.travel114TrySpend({}, 'agency_ho');
ok('反證：計數行刪走 → used 永遠 0、第三次唔會被擋（測試識捉計數失效）',
  S.travel114.used === 0 && apiNoCount.travel114TrySpend({}, 'tvb_longmen') === true);

console.log('---');
console.log('TRAVEL114 LOGIC: ' + (fails.length ? fails.length + ' FAIL' : 'ALL PASS'));
process.exit(fails.length ? 1 : 0);
