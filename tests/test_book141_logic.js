// v20a141 BOOK141 邏輯測試：備忘紙渲染用 live state（唔係寫死樣本數字）。
// 做法：抽 enterHome 入面 #home-stats 嘅 innerHTML 模板字串，用兩組唔同 S／dual 值
// eval，驗輸出跟住數字郁。反證：喺 pristine main 上行會 FAIL（舊模板係三粒 pill
// span，無 memo141／無「銀包」字樣）。
// 用法：node tests/test_book141_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }

const marker = 'hs.innerHTML = `';
// enterHome 嗰個係檔內唯一一個 hs.innerHTML 賦值
const i = html.indexOf(marker);
ok('enterHome 有 #home-stats innerHTML 模板', i >= 0);
let tpl = null;
if(i >= 0){
  const j = html.indexOf('`;', i);
  ok('模板字串完整閉合', j > i);
  if(j > i) tpl = html.slice(i + marker.length, j);
}
function render(S, dual){
  // 模板用 ${...}，直接 eval 成 template literal
  return eval('`' + tpl.replace(/`/g, '\\`') + '`');
}
if(tpl){
  ok('模板係備忘紙（有 memo141／銀包／偉字印）',
    tpl.indexOf('memo141') >= 0 && tpl.indexOf('銀包') >= 0 && tpl.indexOf('偉') >= 0);
  const S = { money: 12927 };
  const dual = { stageVolume: 5, industryCredit: 11 };
  const out1 = render(S, dual);
  ok('樣本數字 12,927／5／11 係 live 值而唔係寫死（第一組照出）',
    out1.indexOf('$ 12,927') >= 0 && out1.indexOf('>5<') >= 0 && out1.indexOf('>11<') >= 0);
  const S2 = { money: 5000 };
  const dual2 = { stageVolume: 9, industryCredit: 3 };
  const out2 = render(S2, dual2);
  ok('換數字就跟住郁（$ 5,000／9／3），證明唔係寫死',
    out2.indexOf('$ 5,000') >= 0 && out2.indexOf('>9<') >= 0 && out2.indexOf('>3<') >= 0
    && out2.indexOf('12,927') < 0);
  ok('錢數 span 保留 .home-money（refreshMoneyHud 刷得到）',
    out1.indexOf('home-money') >= 0);
  ok('聲望／信用 id 保留（h-stage-volume／h-industry-credit）',
    out1.indexOf('h-stage-volume') >= 0 && out1.indexOf('h-industry-credit') >= 0);
}

console.log(fails.length ? ('FAILURES: ' + fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
