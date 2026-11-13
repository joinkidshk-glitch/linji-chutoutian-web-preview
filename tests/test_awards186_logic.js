// v20a186 修 v184 設計 review 新 C1・邏輯測試：
// 兩類獎項嗰陣，結果卡「同屆提名」行只出一次（舊版逐類別卡各出一行，同一份名單重複兩次）。
// 修法：呈現層改動——同屆提名行由逐類別卡內移出，取排序後第一個有 fellows63 嘅類別，
// 喺卡列之後獨立一行；數據／判定／fellows 池／贏線／得主標記一字唔郁。
// 斷言：兩類＝1 行、單類＝1 行、冇 fellows＝0 行；名單逐字不變；kicker 次序（id 序）唔郁；
// 同屆提名行喺兩張類別卡之後（卡底獨立一行，唔係跟第一類卡）。
// 反證：對 pristine main b1b6092 index 行 → 兩類嗰陣出 2 行 → FAIL（唔 crash）。
// 用法：node tests/test_awards186_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }
function count(hay, needle){ return hay.split(needle).length - 1; }
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
  let depth = 0, started = false;
  for(let k = i; k < html.length; k++){
    const ch = html[k];
    if(ch === '{' || ch === '['){ depth++; started = true; }
    else if(ch === '}' || ch === ']'){ depth--; if(started && depth === 0) return html.slice(i, k + 1) + ';'; }
    else if(ch === ';' && !started) return html.slice(i, k + 1);
  }
  throw new Error('const end not found: ' + name);
}

let resultSrc;
try{
  eval(extractConst('EMOJI_ICON112').replace('const EMOJI_ICON112 =', 'var EMOJI_ICON112 ='));
  eval(extractFn('iconHtml112'));
  for(const f of ['awardsCatsSorted184', 'awards63FocusCat', 'awards63FellowsHtml', 'awardWinner149', 'awardWinLine149', 'renderAwardResultHtml'])
    eval(extractFn(f));
}catch(e){
  console.log('FAIL v186 結果卡函數抽唔到（' + e.message + '，pristine 預期）');
  console.log('\nFAILED: 1');
  process.exit(1);
}

/* review ko_932b 原場：葉敏芝《渡輪燈火》／鍾楚凝《星光夜》／高俊傑《潮汐家庭》，得主葉敏芝。 */
const FEL = [
  { starId: 'yip_manji', star: '葉敏芝', title: '渡輪燈火', gigId: 'gig_x1', poster: '', assigned: true },
  { starId: 'chung_choning', star: '鍾楚凝', title: '星光夜', gigId: 'gig_x2', poster: '', assigned: true },
  { starId: 'ko_chunkit', star: '高俊傑', title: '潮汐家庭', gigId: 'gig_1989_tv_05', poster: '', assigned: true }
];
const WIN = FEL[0];
const LIST_TXT = '葉敏芝《渡輪燈火》、鍾楚凝《星光夜》、高俊傑《潮汐家庭》';
const CAT_NEW = { id: 'cat_tv_lead_m', label: '最佳男主角', outcome: 'nominated',
  line: '名單滑過你個名——入圍咗，未抱盃。還有下一場。', repWorkTitle: '', weakHint62: '差啲咩：缺一部擔正嘅代表作。',
  fellows63: FEL, winner63: WIN };
const CAT_FACE = { id: 'cat_tv_support_m', label: '最佳男配角', outcome: 'nominated',
  line: '入圍名單有你，獎就落咗別人手上。', repWorkTitle: '', weakHint62: '差啲咩：缺一部擔正嘅代表作。',
  fellows63: FEL, winner63: WIN };
function basePack(cats){
  return { displayName: '星河台慶・年度頒獎夜', tierLabel: '入圍／提名', year: 1991, venue99: '星河電視台',
    bestOutcome: 'nominated', categories: cats,
    press: { paperName: '娛樂快報', headline: '台慶頒獎夜，版面多一行', dek: '星河台慶夜頒獎環節結束。' },
    news: { outlet: '晚間娛樂快訊', line: '台慶頒獎夜散場：臨記席都有鏡頭掃過。' },
    metricEcho: '收視餘溫', metricEchoLabel: '收視餘溫', rewardsApplied: { stageVolume: 1, industryCredit: 2 } };
}

/* ---- 兩類（raw 次序面孔先，id 序新人先，同 review ko_932b） ---- */
const dual = renderAwardResultHtml(basePack([CAT_FACE, CAT_NEW]));
ok('兩類：同屆提名行只出一次', count(dual, '同屆提名') === 1);
ok('兩類：psr-fellows63 節點只得一個', count(dual, 'psr-fellows63') === 1);
ok('兩類：名單逐字不變（葉敏芝《渡輪燈火》、鍾楚凝《星光夜》、高俊傑《潮汐家庭》只出一次）', count(dual, LIST_TXT) === 1);
ok('兩類：同屆提名行喺兩張類別卡之後（卡底獨立一行）',
  dual.indexOf('同屆提名') > dual.lastIndexOf('最佳男配角') && dual.indexOf('同屆提名') > dual.indexOf('最佳男主角'));
ok('兩類：kicker 次序唔郁（id 序：男主角先、男配角後）',
  dual.indexOf('最佳男主角') < dual.indexOf('最佳男配角'));
ok('兩類：兩張類別卡齊晒（label 各一；餘韻卡同用 psr-metrics class，唔計入）',
  count(dual, '最佳男主角') === 1 && count(dual, '最佳男配角') === 1);
ok('兩類：得主標記仲喺名單入面（🏆圖標＋為得主）', /同屆提名/.test(dual) && /為得主/.test(dual));
ok('兩類：請柬／結果卡以外內容唔郁（報紙卡＋餘韻卡＋雙軌行齊）',
  /娛樂快報/.test(dual) && /收視餘溫/.test(dual) && /幕前聲望 \+1 · 業內信用 \+2/.test(dual));

/* ---- 單類：維持原樣一行 ---- */
const single = renderAwardResultHtml(basePack([CAT_NEW]));
ok('單類：同屆提名行維持一行', count(single, '同屆提名') === 1);
ok('單類：名單逐字不變', count(single, LIST_TXT) === 1);
ok('單類：一張類別卡', count(single, '最佳男主角') === 1 && count(single, '最佳男配角') === 0);

/* ---- 冇 fellows：唔出空行 ---- */
const noFel = renderAwardResultHtml(basePack([
  { id: 'cat_tv_lead_m', label: '最佳男主角', outcome: 'won', line: '得獎。', repWorkTitle: '長篇劇', fellows63: [], winner63: null }
]));
ok('冇 fellows：同屆提名行 0 次（唔出空行）', count(noFel, '同屆提名') === 0);
ok('冇 fellows：結果卡其餘部分正常（得獎卡＋報紙卡齊）', /得獎 · 最佳男主角/.test(noFel) && /娛樂快報/.test(noFel));

/* ---- 第一類冇 fellows、第二類有：照出第二類嗰份（唔漏） ---- */
const mixed = renderAwardResultHtml(basePack([
  { id: 'cat_tv_lead_m', label: '最佳男主角', outcome: 'nominated', line: '入圍。', repWorkTitle: '', fellows63: [], winner63: null },
  CAT_FACE
]));
ok('首類無 fellows、次類有：同屆提名行照出一次', count(mixed, '同屆提名') === 1 && count(mixed, LIST_TXT) === 1);

console.log(fails.length ? ('\nFAILED: ' + fails.length + ' -> ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
