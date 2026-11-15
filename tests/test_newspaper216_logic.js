// v20a216 報紙修復・邏輯／真路徑測試
//   R0 殘留填位項成類過濾（queue 遷移／入隊閘／合版濾／pullDue 回 null）
//   R1 頭條按字數降級（≤10 字 37px／11–16 字 30px／>16 字 26px）＋書名號唔斷開＋套紅
//   R2 第二版真標題（第一則短訊標題；得摺行用頭版標題＋「（續）」）
//   R3 短正文填版（資料格真數據／第一版填充字／邊欄預告／第二版填充字三行）
//   R5 晨報短訊書面語（花邊池 39 則＋world 短訊段＋推出短訊輸出）
//   R4 靜態部分（掣位 CSS）見 test_newspaper216_static.py；DOM 量度見 newspaperCheck＋實駕。
// 用法：node tests/test_newspaper216_logic.js [path-to-index.html]
// 反證：對 pristine main（v215，/tmp/pristine216_index.html）乾淨 FAIL——
//   舊 code 無 fill 過濾、無降級、第二版硬寫「同版短訊」、晨報唔出資料格、花邊全口語。
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');

let fails = [];
function ok(name, cond, extra){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name + (extra && !cond ? ' :: ' + extra : '')); }

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

const NEED = ['fmtNewspaperDate', 'newspaperEsc', 'newspaperFullName214', 'np214DateLabel',
  'renderMorningPaperHtml', 'buildNewspaperEdition', 'pullDueNewspaperEdition',
  'newspaperDueItems', 'ensureNewspaperQueue', 'ensureNewspaperClippings',
  'enqueueNewspaperItem', 'newspaperEventSeen', 'release215CopyFor',
  'dateObj', 'displayDateObj', 'fmtDateShort'];
const missing = [];
const srcs = {};
NEED.forEach(n => {
  const s = extractFn('function ' + n + '(');
  if(!s) missing.push(n); else srcs[n] = s;
});
['START', 'PAPER_SIDE_ITEMS', 'NEWS82_EVENTS', 'RELEASE215_SEASON_WORD'].forEach(n => {
  const s = extractConst(n);
  if(!s) missing.push(n); else srcs[n] = s;
});
ok('setup: v216 真函數／常數全部抽得到', missing.length === 0, missing.join(' | '));
if(missing.length){ console.log('MISSING: ' + missing.join(' | ')); console.log('FAILED: ' + fails.join(' | ')); process.exit(1); }

var S = { dayIndex: 40, fame: 10, wrapHistory: [{ gigId: 'g1', roleLabel: '男主角' }] };
var NEWS82_IMGS = { img_test: 'assets/test.png' };
var news82IsHead = function(){ return false; };
var paperSideItemForDay = function(){ return null; };
var newspaperTopicKey = function(){ return ''; };
var newspaperPrevTopicKey = function(){ return ''; };
global.document = { getElementById: function(){ return { scrollTop: 0 }; } };

eval(srcs['START'].replace('const START', 'var START'));
eval(srcs['PAPER_SIDE_ITEMS'].replace('const PAPER_SIDE_ITEMS', 'var PAPER_SIDE_ITEMS'));
eval(srcs['NEWS82_EVENTS'].replace('const NEWS82_EVENTS', 'var NEWS82_EVENTS'));
eval(srcs['RELEASE215_SEASON_WORD'].replace('const RELEASE215_SEASON_WORD', 'var RELEASE215_SEASON_WORD'));
for(let i = 0; i < NEED.length; i++){ eval(srcs[NEED[i]]); }

/* R0：殘留填位項 */
function fillItem(){
  return { eventKey: 'wrap:gig_1990_test_403:38', source: 'wrap', enqueuedDay: 39,
    publishDay: 40, fameDelta: 0, paperName: '樂壇速遞',
    headline: '《錄音室拍板》錄音完成 準備派台',
    dek: '唱片《錄音室拍板》錄製完成，唱片公司趕工出貨，趕及檔期推出。',
    clipLabel: '樂壇速遞・MV直擊', rumorEcho: '', templateEventKey: 'wrap_success.music',
    medium: 'music', workTitle: '錄音室拍板', press94: 'fill' };
}
S.newspaperQueue = [fillItem()];
S.pendingMorningPaper = null;
S.newspaperLastPresentedDay = null;
ok('R0a queue purge on read', ensureNewspaperQueue().length === 0);
ok('R0a due empty after purge', newspaperDueItems(40).length === 0);
ok('R0a pullDue null (no empty paper)', pullDueNewspaperEdition() === null);
const fillRaw = { eventKey: 'wrap:fill216:39', source: 'wrap', enqueuedDay: 39,
  publishDay: 40, fameDelta: 0, paperName: '樂壇速遞', headline: '填位', dek: '填位內文', press94: 'fill' };
ok('R0b enqueue gate refuses fill', enqueueNewspaperItem(fillRaw, { persist: false }) === null);
ok('R0b gate leaves no queue item', !ensureNewspaperQueue().some(it => it && it.eventKey === 'wrap:fill216:39'));
ok('R0c build all-fill returns null', buildNewspaperEdition([fillItem()], 40) === null);
const edMixed = buildNewspaperEdition([fillItem(), { eventKey: 'wrap:ok216:39', source: 'wrap',
  enqueuedDay: 39, publishDay: 40, fameDelta: 1, paperName: '娛樂版', headline: '正紙', dek: '正紙內文' }], 40);
ok('R0c build mixed keeps real paper', !!edMixed && edMixed.headline === '正紙');
S.newspaperQueue = [fillItem()];
S.pendingMorningPaper = null;
ok('R0d pullDue with only fill queued returns null', pullDueNewspaperEdition() === null);
ok('R0d queue drained (no leftover)', ensureNewspaperQueue().length === 0);

/* R1：頭條降級＋書名唔斷開＋套紅 */
function ed216(extra){ return Object.assign({ paperName: '娛樂版', dateLabel: '1990年2月10日 星期六',
  dayIndex: 40, headline: '頭條', dek: '主文一句。', fameDelta: 0, shorts: [] }, extra || {}); }
let out = renderMorningPaperHtml(ed216({ headline: '駱家聲奪新人獎', dek: '金碟夜新人輩出。', fameDelta: 1 }));
ok('R1a short headline stays 37px', out.indexOf('class="np214-headline"') >= 0);
ok('R1a award verb red (sample v11)', out.indexOf('<span class="red">奪新人獎</span>') >= 0);
out = renderMorningPaperHtml(ed216({ headline: '駱家聲《熱浪之夏》奪獎', dek: '典禮後仍有人提起。', fameDelta: 1 }));
ok('R1b 11-char headline drops to 30px', out.indexOf('class="np214-headline2"') >= 0);
ok('R1b book title red + nobreak', out.indexOf('<span class="np214-nobreak red">《熱浪之夏》</span>') >= 0);
out = renderMorningPaperHtml(ed216({ headline: '《錄音室拍板》錄音完成 準備派台',
  dek: '唱片《錄音室拍板》錄製完成，唱片公司趕工出貨，趕及檔期推出。',
  clipLabel: '樂壇速遞・MV直擊', workTitle: '錄音室拍板', medium: 'music',
  shorts: [{ paperName: '花邊短訊', headline: '陸柏言紅磡開唱', dek: '歌迷排隊。', source: 'side' }] }));
ok('R1c 15-char repro headline at 30px', out.slice(0, out.indexOf('data-np214-page="2"')).indexOf('class="np214-headline2"') >= 0);
ok('R1c repro book title nobreak+red', out.indexOf('<span class="np214-nobreak red">《錄音室拍板》</span>') >= 0);
out = renderMorningPaperHtml(ed216({ headline: '陸柏言紅磡開唱未公佈，黃牛票價高企', dek: '唱片趕工出貨。' }));
ok('R1d 17-char headline drops to 26px', out.indexOf('class="np214-headline3"') >= 0);
out = renderMorningPaperHtml(ed216({ headline: '陸柏言紅磡開唱未公佈，黃牛票價已經高企', dek: '唱片趕工出貨。' }));
ok('R1d >18-char headline drops to 22px', out.indexOf('class="np214-headline4"') >= 0);

/* R2：第二版真標題 */
const htmlLong = renderMorningPaperHtml(ed216({ headline: '《錄音室拍板》錄音完成 準備派台',
  dek: '唱片《錄音室拍板》錄製完成，唱片公司趕工出貨，趕及檔期推出。',
  workTitle: '錄音室拍板', medium: 'music',
  shorts: [{ paperName: '花邊短訊', headline: '陸柏言紅磡開唱', dek: '歌迷排隊。', source: 'side' }] }));
ok('R2a hardcoded section-name headline gone', htmlLong.indexOf('<h3 class="np214-headline2">同版短訊</h3>') < 0);
const p2slice = htmlLong.slice(htmlLong.indexOf('data-np214-page="2"'));
ok('R2a p2 headline is first short (star red)', p2slice.indexOf('<span class="red">陸柏言</span>') >= 0
  && p2slice.indexOf('紅磡開唱') >= 0);
ok('R2a p2 dek line from first short', htmlLong.indexOf('歌迷排隊') >= 0);
ok('R2a column name kept in kicker + pagefoot only',
  (htmlLong.match(/同版短訊/g) || []).length === 2
  && htmlLong.indexOf('<p class="np214-kicker">同版短訊</p>') >= 0); /* kicker + pagefoot（邊欄預告標籤已改「同版：」；pristine 得 2 但無 kicker，照樣 FAIL） */
const htmlSum = renderMorningPaperHtml(ed216({ headline: '頭條', dek: '主文。',
  shorts: [{ source: 'summary', headline: '同日還有 2 則', dek: '版面有限，其餘從略。' }] }));
ok('R2b summary-only falls back to head headline + （續）', htmlSum.indexOf('頭條（續）') >= 0);

/* R3：短正文填版 */
ok('R3a factbox emitted with real data', htmlLong.indexOf('np214-factbox') >= 0
  && htmlLong.indexOf('錄音室拍板》小檔案') >= 0);
ok('R3a factbox rows are real (works + medium)', htmlLong.indexOf('<b>作品</b>') >= 0 && htmlLong.indexOf('<b>媒介</b>') >= 0);
/* 實駕修正：無相嗰陣 p1 填充字唔浮動（全闊放正文＋資料格下面），p2 填充字跟短訊數縮（1 則 1 段、2 則 2 段、3 則以上 0 段；v20a218 C-C1b）；邊欄預告改「同版：」＋截 6 字。 */
const p1slice216 = htmlLong.slice(0, htmlLong.indexOf('data-np214-page="2"'));
ok('R3b p1 filler for short dek + no photo, not floated', p1slice216.indexOf('<p class="np214-filler"') >= 0
  && p1slice216.indexOf('np214-filler-left') < 0);
ok('R3c sidebar carries real preview', htmlLong.indexOf('<span class="np214-sb-tag">同版：</span>陸柏言紅磡開……') >= 0);
ok('R3d p2 filler scales with shorts: 1 short → 1 paragraph (v20a218 C-C1b)', (p2slice.match(/<p class="np214-filler"/g) || []).length === 1);
const html2short = renderMorningPaperHtml(ed216({ headline: '頭條', dek: '主文一句。',
  shorts: [{ paperName: '花邊短訊', headline: '短訊一', dek: '內文一。', source: 'side' },
           { paperName: '花邊短訊', headline: '短訊二', dek: '內文二。', source: 'side' }] }));
const p2b = html2short.slice(html2short.indexOf('data-np214-page="2"'));
ok('R3d p2 filler: 2 shorts → 2 paragraphs', (p2b.match(/<p class="np214-filler"/g) || []).length === 2);
const html3short = renderMorningPaperHtml(ed216({ headline: '頭條', dek: '主文一句。',
  shorts: [{ paperName: '花邊短訊', headline: '短訊一', dek: '內文一。', source: 'side' },
           { paperName: '花邊短訊', headline: '短訊二', dek: '內文二。', source: 'side' },
           { paperName: '花邊短訊', headline: '短訊三', dek: '內文三。', source: 'side' }] }));
const p2c = html3short.slice(html3short.indexOf('data-np214-page="2"'));
ok('R3d p2 filler: 3 shorts → 0 paragraphs', (p2c.match(/<p class="np214-filler"/g) || []).length === 0);
const edRole = buildNewspaperEdition([{ eventKey: 'wrap:g1:39', source: 'wrap', enqueuedDay: 39,
  publishDay: 40, fameDelta: 1, paperName: '娛樂版', headline: '正紙', dek: '正紙內文',
  workTitle: '試片', medium: 'film' }], 40);
ok('R3e edition passes work/medium/role', !!edRole && edRole.workTitle === '試片'
  && edRole.medium === 'film' && edRole.roleLabel === '男主角');
const htmlPhoto = renderMorningPaperHtml(ed216({ headline: '頭條', dek: '主文一句。', imgKey: 'img_test' }));
ok('R3f photo present skips p1 filler', htmlPhoto.indexOf('np214-photo') >= 0
  && htmlPhoto.indexOf('<p class="np214-filler"') < 0); /* 邊欄裝飾 filler-v 唔計（佢係 -v，唔係填充段） */

/* R5：書面語（同 newspaperCheck 口徑） */
function banned216(txt){
  const noq = String(txt || '').replace(/「[^」]*」/g, '');
  if(/[喺嘅咗唔]/.test(noq)) return true;
  if(/嗰/.test(noq)) return true;
  if(/係[^。]{0,12}定/.test(noq)) return true; /* 「係…定…」口語選擇句（E5 原文） */
  if(/估緊/.test(noq)) return true;
  const t2 = String(txt || '').replace(/電話|說話|話題|通話|熱話|一句話/g, '');
  if(/話/.test(t2)) return true;
  if(/cut|mark/i.test(String(txt || ''))) return true;
  return false;
}
ok('R5a side pool is 39 items', PAPER_SIDE_ITEMS.length === 39, 'n=' + PAPER_SIDE_ITEMS.length);
const badSide = PAPER_SIDE_ITEMS.filter(it => it && banned216((it.h || '') + (it.d || '')));
ok('R5a all 39 side items clean', badSide.length === 0, JSON.stringify(badSide.slice(0, 2)));
const badWorld = [];
NEWS82_EVENTS.forEach(ev => {
  if(ev && ev.level === 'side' && Array.isArray(ev.paras)){
    ev.paras.forEach(p => { if(banned216(p)) badWorld.push(ev.id); });
  }
});
ok('R5b world side paras clean', badWorld.length === 0, badWorld.join(','));
let relBad = false;
try{
  [['春', '電影'], ['夏', '電視劇'], ['秋', '唱片'], ['冬', '廣告']].forEach(([season, type]) => {
    const r = release215CopyFor({ workTitle: '試片' }, { season: season, type: type });
    if(!r || banned216(r.headline + r.dek)) relBad = true;
  });
}catch(_e){ relBad = true; }
ok('R5c release copy clean', !relBad);

/* R4：靜態 CSS（DOM 量度見 newspaperCheck＋實駕） */
ok('R4a no negative btn margin anywhere', html.indexOf('margin-top:-7px') < 0);
ok('R4b 76px short-screen padding comes after 34px (later wins)',
  html.indexOf('padding-bottom:76px') > html.indexOf('padding-bottom:34px'));
ok('R4c paper-on modal widened to 88dvh',
  /#mask\.paper-on:not\(\.tut-on\) \.modal\{\n  max-height:min\(88dvh,88svh,760px\)/.test(html));
ok('R4d switch row sticky at visible bottom', html.indexOf('.paper-sheet .np214-switchrow{ position:sticky; bottom:0;') >= 0);

console.log('');
if(fails.length){ console.log('FAILED: ' + fails.join(' | ')); process.exit(1); }
console.log('ALL PASS');
