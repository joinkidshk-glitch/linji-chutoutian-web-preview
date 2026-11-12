// v20a143 BOOK143 邏輯測試：B1 全部編輯掣接線唔郁（只換呈現，功能照舊）＋
// B2 subtab 切換 handler 係共用 setHomeTab（四組同 plan 組同一條路）。
// 做法：原始碼層面核對 onclick 綁定／生成邏輯。反證：喺 pristine main 上行，
// B1/B2 相關斷言會 FAIL（冇 BOOK143 段／冇 :not(plan) 擴展）。
// 用法：node tests/test_book143_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }

// --- 門：BOOK143 呈現規則本身要喺度（否則下面接線斷言喺 pristine 都 PASS，唔成反證） ---
ok('BOOK143 段在場（B1/B2/B3 呈現規則已入 index.html）',
  html.includes('v20a143 BOOK143') && html.includes('BOOK143 完'));

// --- B1：快捷四掣＋複製＋還原＋確定，接線全部仲喺度 ---
ok('快捷四掣 onclick 綁定齊（rest／train／clear／copy）',
  html.includes('rest.onclick=()=>quickFillRest()')
  && html.includes('train.onclick=()=>quickFillTrain()')
  && html.includes('clear.onclick=()=>quickClearWeek()')
  && html.includes('copy.onclick=()=>toggleCopyPanel()'));
ok('套用複製＋預設三掣綁定齊',
  html.includes('apply.onclick=()=>applyCopyToTargets()')
  && html.includes('selectCopyPreset(b.getAttribute("data-copy"))'));
ok('每行「複製」生成邏輯仲喺度（cp.onclick → openCopyFromDay，鍵盤 Enter／Space 一樣）',
  html.includes('cp.textContent="⧉ 複製"')
  && html.includes('cp.onclick=(e)=>{ e.stopPropagation(); openCopyFromDay(i); }')
  && html.includes('if(e.key==="Enter"||e.key===" "){ e.preventDefault(); e.stopPropagation(); openCopyFromDay(i); }'));
ok('還原＋確定綁定齊（resetPlanDraft／confirmPlan）',
  html.includes('document.getElementById("btn-reset-plan").onclick=resetPlanDraft')
  && html.includes('document.getElementById("btn-confirm-plan").onclick=confirmPlan'));
ok('鎖定態邏輯仲喺度（唔 editable → disabled＋is-locked＋「行程已定」；editable →「確定本週行程」）',
  html.includes('confBtn.classList.add("is-locked")')
  && html.includes('confBtn.textContent = "行程已定"')
  && html.includes('confBtn.textContent = "確定本週行程"'));

// --- B2：subtab 切換係共用 handler，四組同 plan 組同一條路 ---
ok('subtab 切換共用 setHomeTab（delegate 到 button[data-htab]，唔分組）',
  html.includes('_homeSubtabsEl.onclick=e=>{')
  && html.includes('const btn=e.target.closest("button[data-htab]"); if(!btn) return;')
  && html.includes('setHomeTab(btn.getAttribute("data-htab"))'));
ok('四組 subtab 掣 data-htab 齊（works／awards／memory／ledger／tags／inv／rumor／clippings／debt／people）',
  ['data-htab="works"', 'data-htab="awards"', 'data-htab="memory"', 'data-htab="ledger"',
   'data-htab="tags"', 'data-htab="inv"', 'data-htab="rumor"', 'data-htab="clippings"',
   'data-htab="debt"', 'data-htab="people"'].every(s => html.includes(s)));

console.log(fails.length ? ('FAILURES: ' + fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
