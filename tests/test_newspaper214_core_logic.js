// v20a214 NP214 晨報核心渲染器・邏輯／真路徑測試
//   段一 (a)：遊戲日期——fmtNewspaperDate 由 START＋dayIndex 計出中文連星期
//             （dayIndex 152＝1990年6月2日 星期六，樣本日期；dayIndex 4＝1990年1月5日 星期五）
//   段二 (b)：寫全名——渲染時 阿偉→陳偉翔、何生→經理人何生；一名臨記／何生事務所唔郁
//   段三 (c)：v11 版式——報頭 A、兩欄、相片黑白半調、第一版／第二版分版＋切換、聲望行
//   段四 (d)：＞3 則摺疊仲喺度（buildNewspaperEdition：3 則＋「同日還有 N 則」）
//   段五 (e)：版內切換 np214ShowPage（fake DOM）＋冇天氣格、冇「今早」
// 用法：node tests/test_newspaper214_core_logic.js [path-to-index.html]
// 反證：對 pristine main f58f19c 乾淨 FAIL（抽唔到新函數），唔 crash。
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');

let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }

function extractFn(decl){
  const i = html.indexOf(decl);
  if(i < 0) return null;
  let j = html.indexOf('{', i), depth = 0, k = j;
  for(; k < html.length; k++){
    if(html[k] === '{') depth++;
    else if(html[k] === '}'){ depth--; if(depth === 0){ k++; break; } }
  }
  return html.slice(i, k);
}
function extractConst(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) return null;
  let depth = 0, started = false;
  for(let k = i; k < html.length; k++){
    const ch = html[k];
    if(ch === '{' || ch === '['){ depth++; started = true; }
    else if(ch === '}' || ch === ']'){ depth--; if(started && depth === 0) return html.slice(i, k + 1) + ';'; }
    else if(ch === ';' && !started) return html.slice(i, k + 1);
  }
  return null;
}

/* 抽真函數；抽唔到就記低、成段 skip，最後乾淨 FAIL（反證用）。 */
const NEED = ['fmtNewspaperDate', 'newspaperEsc', 'newspaperFullName214', 'np214DateLabel',
  'np214ShowPage', 'renderMorningPaperHtml', 'buildNewspaperEdition', 'newspaperSerialLine',
  'dateObj', 'displayDateObj', 'fmtDateShort'];
const missing = [];
const srcs = {};
NEED.forEach(n => {
  const s = extractFn('function ' + n + '(');
  if(!s) missing.push(n); else srcs[n] = s;
});
const startSrc = extractConst('START');
if(!startSrc) missing.push('START');
ok('setup: NP214 真函數全部抽得到', missing.length === 0);
if(missing.length){
  console.log('MISSING: ' + missing.join(' | '));
  console.log('FAILED: ' + fails.join(' | '));
  process.exit(1);
}

var S = { dayIndex: 152, fame: 20 };
var NEWS82_IMGS = { img_test: 'assets/test.png' };
var news82IsHead = function(){ return false; };
var paperSideItemForDay = function(){ return null; };
var newspaperTopicKey = function(){ return ''; };
var newspaperPrevTopicKey = function(){ return ''; };
global.document = { getElementById: function(){ return { scrollTop: 0 }; } };

eval(startSrc.replace('const START', 'var START'));
/* 唔可以用 forEach 回調入面 eval——function 宣告會困喺回調 scope，唔升返 module scope。 */
for(let i = 0; i < NEED.length; i++){ eval(srcs[NEED[i]]); }

/* ================================================================
   段一 (a)：遊戲日期
   ================================================================ */
ok('a1 fmtNewspaperDate(152)＝1990年6月2日 星期六', fmtNewspaperDate(152) === '1990年6月2日 星期六');
ok('a2 fmtNewspaperDate(4)＝1990年1月5日 星期五', fmtNewspaperDate(4) === '1990年1月5日 星期五');
ok('a3 fmtNewspaperDate(0)＝1990年1月1日 星期一', fmtNewspaperDate(0) === '1990年1月1日 星期一');
S.dayIndex = 152;
ok('a4 fmtNewspaperDate() 跟 S.dayIndex', fmtNewspaperDate() === '1990年6月2日 星期六');
ok('a5 np214DateLabel 照用中文標籤', np214DateLabel({ dateLabel: '1990年6月2日 星期六' }) === '1990年6月2日 星期六');
ok('a6 np214DateLabel 舊數字標籤轉中文', np214DateLabel({ dateLabel: '1990/1/5' }) === '1990年1月5日 星期五');
ok('a7 np214DateLabel「今早」唔留、用遊戲日期計返', np214DateLabel({ dateLabel: '今早', dayIndex: 152 }) === '1990年6月2日 星期六');
ok('a8 np214DateLabel 缺標籤都計得出', np214DateLabel({ dayIndex: 4 }) === '1990年1月5日 星期五');

/* ================================================================
   段二 (b)：寫全名
   ================================================================ */
ok('b1 阿偉→陳偉翔', newspaperFullName214('阿偉獲青睞') === '陳偉翔獲青睞');
ok('b2 人氣新人阿偉→人氣新人陳偉翔', newspaperFullName214('人氣新人阿偉') === '人氣新人陳偉翔');
ok('b3 何生→經理人何生', newspaperFullName214('何生話：') === '經理人何生話：');
ok('b4 經理人何生唔重複加', newspaperFullName214('經理人何生話：') === '經理人何生話：');
ok('b5 何生事務所（機構名）唔改', newspaperFullName214('何生事務所新簽臨記') === '何生事務所新簽臨記');
ok('b6 一名臨記留返', newspaperFullName214('一名臨記') === '一名臨記');
ok('b7 陳偉翔本身唔郁', newspaperFullName214('陳偉翔的名字') === '陳偉翔的名字');

/* ================================================================
   段三 (c)：v11 版式渲染
   ================================================================ */
function baseEd(extra){
  return Object.assign({
    paperName: '娛樂版', dateLabel: '1990年6月2日 星期六', dayIndex: 152,
    headline: '《天星碼頭》煞科 阿偉武師配角一角企到尾',
    dek: '通告殺青，阿偉於《天星碼頭》飾演武師配角，順利收工。何生在場見證。',
    clipLabel: '獨家', fameDelta: 2,
    shorts: [
      { paperName: '娛樂快報', headline: '短訊一', dek: '短訊內文一', fameDelta: 0, source: 'wrap' },
      { paperName: '電視週刊', headline: '短訊二', dek: '短訊內文二', fameDelta: 0, source: 'wrap' }
    ]
  }, extra || {});
}
let out = renderMorningPaperHtml(baseEd());
ok('c1 報頭 A：維港日報＋英文', out.indexOf('維港日報') >= 0 && out.indexOf('VICTORIA HARBOUR DAILY') >= 0);
ok('c2 日期行係遊戲日期', out.indexOf('1990年6月2日 星期六') >= 0);
ok('c3 冇「今早」fallback', out.indexOf('今早') < 0);
ok('c4 兩欄內文 np214-body2', out.indexOf('np214-body2') >= 0);
ok('c5 右直欄影視娛樂', out.indexOf('影視娛樂') >= 0);
ok('c6 冇聲量、有聲望＋2', out.indexOf('聲量') < 0 && out.indexOf('聲望 +2') >= 0);
ok('c7 報紙面全名：陳偉翔＋經理人何生、冇阿偉／裸何生',
  out.indexOf('陳偉翔') >= 0 && out.indexOf('經理人何生') >= 0
  && out.indexOf('阿偉') < 0 && !/何生(?!事務所)/.test(out.replace(/經理人何生/g, '')));
ok('c8 舊 masthead／date class 已唔用', out.indexOf('paper-mast') < 0 && out.indexOf('paper-date') < 0);
ok('c9 冇天氣格', out.indexOf('天氣') < 0 && out.indexOf('明日天氣') < 0);
ok('c10 冇「收下這份剪報」字樣（切換唔係 commit 掣）', out.indexOf('收下這份剪報') < 0);

out = renderMorningPaperHtml(baseEd({ fameDelta: 0 }));
ok('c11 fame 0 出聲望未有變動', out.indexOf('聲望未有變動') >= 0 && out.indexOf('聲望 +') < 0);

out = renderMorningPaperHtml(baseEd({ imgKey: 'img_test' }));
ok('c12 有 imgKey 出黑白半調相', out.indexOf('np214-photo') >= 0 && out.indexOf('assets/test.png') >= 0);
out = renderMorningPaperHtml(baseEd({ imgKey: '' }));
ok('c13 冇 imgKey 唔出相', out.indexOf('<img') < 0);

out = renderMorningPaperHtml(baseEd({ shorts: [] }));
ok('c14 冇短訊就單版、冇切換掣', out.indexOf('np214-page') >= 0 && out.indexOf('第二版') < 0 && out.indexOf('np214ShowPage') < 0);

out = renderMorningPaperHtml(baseEd());
ok('c15 短訊喺第二版、頭條喺第一版',
  out.indexOf('data-np214-page="1"') >= 0 && out.indexOf('data-np214-page="2"') >= 0
  && out.indexOf('短訊一') > out.indexOf('data-np214-page="2"')
  && out.indexOf('《天星碼頭》') < out.indexOf('data-np214-page="2"'));
ok('c16 切換掣行 np214ShowPage、唔經 modal 掣列',
  out.indexOf('onclick="np214ShowPage(this,2)"') >= 0 && out.indexOf('onclick="np214ShowPage(this,1)"') >= 0);

/* 世界事件：副題＋三段正文分開出 */
out = renderMorningPaperHtml(baseEd({
  worldId: 'w1', imgKey: 'img_test', dek: '世界事件副題。',
  paras: ['第一段正文。', '第二段正文。', '第三段正文。']
}));
ok('c17 世界事件：副題＋三段正文＋相',
  out.indexOf('np214-dek') >= 0 && out.indexOf('世界事件副題') >= 0
  && out.indexOf('第一段正文') >= 0 && out.indexOf('第三段正文') >= 0
  && out.indexOf('np214-photo') >= 0);
/* 眉題去重（v20a48 行為不變） */
out = renderMorningPaperHtml(baseEd({ clipLabel: '《天星碼頭》煞科', headline: '《天星碼頭》煞科 阿偉武師配角一角企到尾' }));
ok('c18 眉題係標題前綴照 suppress', (out.match(/paper-kicker/g) || []).length === 0);
out = renderMorningPaperHtml(baseEd({ clipLabel: '獨家直擊' }));
ok('c19 眉題唔係前綴照保留', (out.match(/paper-kicker/g) || []).length === 1 && out.indexOf('獨家直擊') >= 0);

/* ================================================================
   段四 (d)：＞3 則摺疊仲喺度（真 buildNewspaperEdition）
   ================================================================ */
(function(){
  const batch = [];
  for(let i = 0; i < 6; i++){
    batch.push({ eventKey: 'wrap:m' + i + ':3', source: 'wrap', enqueuedDay: 3, publishDay: 4,
      fameDelta: 1, paperName: '娛樂版', headline: '則' + i, dek: '短' + i });
  }
  const ed = buildNewspaperEdition(batch, 152);
  ok('d1 edition 日期係中文遊戲日期', ed.dateLabel === '1990年6月2日 星期六');
  ok('d2 ＞3 則摺疊：shorts 係 3＋summary＝4', ed.shorts.length === 4
    && ed.shorts.some(s => s.source === 'summary' && s.headline === '同日還有 2 則'));
  const html2 = renderMorningPaperHtml(ed);
  ok('d3 摺疊行渲染喺第二版', html2.indexOf('同日還有 2 則') >= 0
    && html2.indexOf('同日還有 2 則') > html2.indexOf('data-np214-page="2"'));
  ok('d4 全路徑渲染有聲望、冇聲量', html2.indexOf('聲望') >= 0 && html2.indexOf('聲量') < 0);
})();

/* ================================================================
   段五 (e)：版內切換（fake DOM）
   ================================================================ */
(function(){
  function fakePage(on){
    const cls = new Set(on ? ['np214-page', 'on'] : ['np214-page']);
    return { classList: {
      toggle: function(c, force){ if(force) cls.add(c); else cls.delete(c); },
      contains: function(c){ return cls.has(c); }
    }};
  }
  const p1 = fakePage(true), p2 = fakePage(false);
  const sheet = { querySelectorAll: function(){ return [p1, p2]; } };
  const btn = { closest: function(){ return sheet; } };
  np214ShowPage(btn, 2);
  ok('e1 切去第二版', !p1.classList.contains('on') && p2.classList.contains('on'));
  np214ShowPage(btn, 1);
  ok('e2 切返第一版', p1.classList.contains('on') && !p2.classList.contains('on'));
  let threw = false;
  try{ np214ShowPage(null, 2); np214ShowPage({}, 2); }catch(_e){ threw = true; }
  ok('e3 壞輸入唔爆', !threw);
})();

console.log('');
if(fails.length){ console.log('FAILED: ' + fails.join(' | ')); process.exit(1); }
console.log('ALL PASS');
