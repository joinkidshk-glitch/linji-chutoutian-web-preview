// v20a145 BOOK145 邏輯測試：B1/B2/B3 全部只換呈現，接線唔郁。
// 做法：原始碼層面核對 onclick 綁定／生成邏輯／鎖定邏輯。反證：喺 pristine main 上行，
// BOOK145 相關斷言會 FAIL（冇 BOOK145 段）。
// 用法：node tests/test_book145_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }

// --- 門：BOOK145 呈現規則本身要喺度（否則下面接線斷言喺 pristine 都 PASS，唔成反證） ---
ok('BOOK145 段在場（B1/B2/B3 呈現規則已入 index.html）',
  html.includes('v20a145 BOOK145') && html.includes('BOOK145 完'));

// --- B3：chips／排入掣接線唔郁（只換 CSS，唔郁 JS） ---
ok('B3：屬性 chip 委派接線仲喺度（closest [data-gstat] → ux68GuideStat）',
  html.includes('t.closest("[data-gstat]")')
  && html.includes('ux68GuideStat = chip.getAttribute("data-gstat")'));
ok('B3：排入掣委派接線仲喺度（closest [data-t71pick] → getAttribute）',
  html.includes('t.closest("[data-t71pick]")')
  && html.includes('pick.getAttribute("data-t71pick")'));
ok('B3：picker 兩個 host 仲喺度（全日填滿 #train71-picker＋逐日 .train71-host）',
  html.includes('id="train71-picker"') && html.includes('train71PickerHtml("fill")')
  && html.includes('train71PickerHtml("day")'));
ok('B3：未報名提示邏輯仲喺度（train73-note／train73-zero 純文字句）',
  html.includes('train73-note train73-zero') && html.includes('你仲未報名任何課程'));

// --- B2：pane 切換 handler 共用 setHomeTab（八組同事業組同一條路） ---
ok('B2：八組 pane 嘅 HTML id 全部仲喺度（ledger／inv／rumor／clippings／debt／people／tags／progress）',
  ['home-pane-ledger', 'home-pane-inv', 'home-pane-rumor', 'home-pane-clippings',
   'home-pane-debt', 'home-pane-people', 'home-pane-tags', 'home-pane-progress']
    .every(id => html.includes('id="' + id + '"')));
ok('B2：subtab 切換 handler 仲喺度（setHomeTab／htab id 齊）',
  html.includes('setHomeTab') && html.includes('id="htab-ledger"')
  && html.includes('id="htab-clippings"') && html.includes('id="htab-people"')
  && html.includes('id="htab-progress"'));
ok('B2：各 pane 渲染函數仲喺度（renderClippingsPane／renderInvPane／renderRumorPane 唔郁）',
  html.includes('function renderClippingsPane()') && html.includes('function renderInvPane()'));

// --- B1：鎖定邏輯唔郁（淨係 CSS 收起兩行，DOM／文字／is-locked 照舊；v20a197 B2＋D1：經 helper 互換 button／span） ---
ok('B1：鎖定態邏輯仲喺度（syncConfirmPlanStamp197 切鎖定印章＋「行程已定」）',
  html.includes('syncConfirmPlanStamp197(true)')
  && html.includes('el.textContent = "行程已定"'));
ok('B1：提示列文字仲喺度（「行程已定，下週一回家結算後再排。」——短屏淨係 CSS 隱藏）',
  html.includes('行程已定，下週一回家結算後再排。'));
ok('B1：標題行／range 行 HTML 唔郁',
  html.includes('id="nb-plan-title">本週行程</p>') && html.includes('id="nb-range"'));

console.log('RESULT ' + (fails.length ? 'FAIL (' + fails.length + ')' : 'PASS'));
process.exit(fails.length ? 1 : 0);
