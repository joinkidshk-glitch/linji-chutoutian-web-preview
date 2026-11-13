// v20a185 GIFT185 邏輯測試：抽 openGiftPick 嘅真 row 模板 literal，用 stub 評值，
// 驗渲染出嚟嘅卡片 HTML 結構——卡名入 .gift-pick-name span、數量入 .gift-pick-count span，
// 名＋×N 同行唔斷行（C1），而唔係舊版裸 `${item.name} ×${count}`（會換行跌孤兒 ×N）。
// 另驗 v185 CSS 規則在位（ellipsis＋nowrap＋grid 軌 min-width:0，B1 路線 a）。
// 反證：pristine main (01ddcaa) row 模板冇 spans、冇 v185 規則 → 多項 FAIL（唔 crash）。
// 用法：node tests/test_gift185_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const IDX = process.argv[2] ? path.resolve(process.argv[2]) : path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(IDX, 'utf8');
let fails = 0;
function ok(name, cond, extra){
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : ''));
  if (!cond) fails++;
}

// ---- 抽真模板：openGiftPick 內 `return `<button class="act act-priority" ...` ----
const fnStart = html.indexOf('function openGiftPick(npcKey, L){');
ok('openGiftPick 在位', fnStart >= 0);
const tplStart = html.indexOf('return `<button type="button" class="act act-priority"', fnStart);
ok('row 模板 literal 在位', tplStart >= 0);
let rendered = '';
if (tplStart >= 0){
  const bt = html.indexOf('`', tplStart); // 模板開 backtick
  const et = html.indexOf('`;', bt + 1);  // 模板閂 backtick
  ok('row 模板有開閂 backtick', bt >= 0 && et > bt);
  if (bt >= 0 && et > bt){
    const tpl = html.slice(bt, et + 1);
    const stubIcon = () => '<img class="ic112" src="assets/icons/icon_gift.png" alt=""/>';
    const stubCost = () => '不耗日 · 只用今日送禮次數';
    // 最長名＋最短名兩個實例，驗結構唔依賴名長度
    for (const [itemId, count, item] of [
      ['gift_cassette_indie', 3, { emoji: '🎁', name: '原創卡帶（獨立樂隊）' }],
      ['gift_thermos', 3, { emoji: '🎁', name: '實用不銹鋼保溫瓶' }],
    ]){
      const tag = '喜';
      const fn = new Function('itemId', 'count', 'item', 'tag', 'iconHtml112', 'giftConfirmCostLine',
        'return ' + tpl + ';');
      const out = fn(itemId, count, item, tag, stubIcon, stubCost);
      if (itemId === 'gift_cassette_indie') rendered = out;
      ok('渲染 [' + item.name + '] 有 .gift-pick-name span 包住全名',
        out.includes('<span class="gift-pick-name">' + item.name + '</span>'));
      ok('渲染 [' + item.name + '] 有 .gift-pick-count span 包住 ×' + count,
        out.includes('<span class="gift-pick-count">×' + count + '</span>'));
      ok('渲染 [' + item.name + '] 名 span 在數量 span 之前（名＋×N 同行次序）',
        out.indexOf('gift-pick-name') < out.indexOf('gift-pick-count'));
      ok('渲染 [' + item.name + '] 冇裸「名 ×N」文字（唔會換行跌孤兒）',
        !out.includes(item.name + ' ×' + count));
      ok('渲染 [' + item.name + '] 仍有「選」掣', out.includes('<div class="cost">選</div>'));
    }
  }
}

// ---- v185 CSS 規則（B1 路線 a：卡片矮返＋唔撐闊 grid 軌；C1：名 ellipsis＋數量 nowrap） ----
ok('v185 標記在位', html.includes('v20a185 B1+C1'));
const nameRule = html.includes('#gift-pick-list .n .gift-pick-name{ flex:1 1 auto !important; min-width:0 !important; overflow:hidden !important; text-overflow:ellipsis !important; white-space:nowrap !important; }');
ok('C1 名 span：flex:1＋min-width:0＋ellipsis＋nowrap', nameRule);
ok('C1 數量 span：flex:0 0 auto＋nowrap',
  html.includes('#gift-pick-list .n .gift-pick-count{ flex:0 0 auto !important; white-space:nowrap !important; }'));
ok('C1 .n 行 flex 排（icon＋名＋數量一行）',
  html.includes('#gift-pick-list .n{ display:flex !important; align-items:baseline !important; gap:4px !important; }'));
ok('C1 icon 唔縮（.ic112 flex:0 0 auto）',
  html.includes('#gift-pick-list .n .ic112{ flex:0 0 auto !important; }'));
ok('B1 grid 軌唔被 nowrap 名撐闊（.act min-width:0）',
  html.includes('#gift-pick-list .act{ min-width:0 !important; }'));
// v183 C7 兩欄設計原封不動（淨係修遮擋，唔推翻）
ok('C7 700 media query 兩欄原封不動',
  html.includes('@media (max-height:720px){ #gift-pick-list{ display:grid; grid-template-columns:1fr 1fr;'));

console.log(fails ? 'FAILURES: ' + fails : 'ALL PASS');
process.exit(fails ? 1 : 0);
