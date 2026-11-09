// v20a48 打磨邏輯測試：第 3 項眉題去重（renderMorningPaperHtml 純呈現層）。
// 抽真 renderMorningPaperHtml＋真 newspaperEsc 行真路徑：
// 前綴重複（原句／全同／去空白後前綴）要 suppress；唔係前綴要保留（反例）；
// 冇 clipLabel 行為不變；標題／dek／聲望行結構唔受影響。
// 用法：node tests/test_polish48_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) throw new Error('fn not found: '+name);
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){
    if(html[j]==='{') depth++;
    else if(html[j]==='}'){ depth--; if(depth===0) break; }
  }
  return html.slice(i, j+1);
}
/* journalText 唔存在嗰陣 newspaperEsc 行自己嘅 escape 分支，毋須 stub。
   renderMorningPaperHtml 只依賴 newspaperEsc；兩者都係真碼。 */
eval(extractFn('newspaperEsc'));
eval(extractFn('renderMorningPaperHtml'));

function clipCount(out){ return (out.match(/paper-kicker/g)||[]).length; }
function baseEd(extra){
  return Object.assign({
    paperName:'電視週刊', dateLabel:'1988年3月8日（二）',
    headline:'電視城臨記班底添新血 阿偉獲青睞',
    dek:'何生事務所新簽臨記阿偉，首日開工即獲導演點名。',
    fameDelta:1, shorts:[]
  }, extra||{});
}

/* 1. 任務原例：kicker 係 headline 開頭（後接空格續句）→ suppress */
let out = renderMorningPaperHtml(baseEd({ clipLabel:'電視城臨記班底添新血' }));
ok('dup prefix kicker suppressed', clipCount(out)===0);
ok('headline still rendered', out.includes('電視城臨記班底添新血 阿偉獲青睞'));
ok('dek still rendered', out.includes('何生事務所新簽臨記阿偉'));
ok('fame line still rendered', out.includes('聲望 +1'));

/* 2. kicker 同 headline 全同 → suppress */
out = renderMorningPaperHtml(baseEd({ clipLabel:'電視城臨記班底添新血 阿偉獲青睞' }));
ok('identical kicker suppressed', clipCount(out)===0);

/* 3. kicker 內部有空格、去空白後係 headline 前綴 → suppress */
out = renderMorningPaperHtml(baseEd({ clipLabel:'電視城 臨記班底' }));
ok('whitespace-normalised prefix suppressed', clipCount(out)===0);

/* 4. 反例：kicker 唔係前綴（獨立眉題）→ 保留原封 */
out = renderMorningPaperHtml(baseEd({ clipLabel:'獨家直擊' }));
ok('non-prefix kicker kept', clipCount(out)===1 && out.includes('獨家直擊'));

/* 5. 反例：kicker 只同 headline 共用個別字、唔成前綴 → 保留 */
out = renderMorningPaperHtml(baseEd({ clipLabel:'阿偉獲青睞' }));
ok('suffix-only kicker kept', clipCount(out)===1 && out.includes('阿偉獲青睞'));

/* 6. 反例：kicker 長過 headline 且唔係 headline 前綴關係 → 保留 */
out = renderMorningPaperHtml(baseEd({ clipLabel:'電視城臨記班底添新血 阿偉獲青睞 震驚全城' }));
ok('overlong kicker kept', clipCount(out)===1);

/* 7. 冇 clipLabel → 冇眉題行（舊行為） */
out = renderMorningPaperHtml(baseEd({}));
ok('no clipLabel no kicker', clipCount(out)===0);

/* 8. headline 缺失＋有 kicker → kicker 保留（冇嘢可比，唔好誤殺） */
out = renderMorningPaperHtml({ paperName:'電視週刊', dateLabel:'今早', headline:'', clipLabel:'獨家', fameDelta:0, shorts:[] });
ok('empty headline keeps kicker', clipCount(out)===1);

console.log(fails.length ? ('FAILURES: '+fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
