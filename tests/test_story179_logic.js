// v20a179 STORY179・邏輯測試：v172 review 唯一新項 C1（用戶已拍板修）
//   進度頁鎖行嘅「（場景：X）」係一句無動詞嘅孤兒括號，隔籬四項全部係條件句，
//   初睇要諗一諗佢即係咩。修法（用戶拍板）：拎走括號，改做標籤式「場景：X」。
//   三種鎖行都要改齊：
//     C3 單地點鎖行：「到星河電視台播」→「場景：星河電視台」
//     C4 OR 行：「…或到何生事務所」→「…或場景：何生事務所」
//     C5 多地點鎖行：「到金龍茶餐廳或星河電視台播」→「場景：金龍茶餐廳或星河電視台」
//   已開放行完整句式「已經開放——返地圖嗰陣就會播出。（場景：X）」唔郁（靜態測試覆蓋）。
//   其餘條件句（前置／週數／通告／聲望／傳聞）唔變。
// 反證：喺 pristine main（v172，7801a72）上行會 FAIL（鎖行仲係括號寫法），唔會 crash。
// 用法：node tests/test_story179_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }
function extractFn(decl){
  const i = html.indexOf(decl);
  if(i < 0) throw new Error('fn not found: ' + decl);
  let j = html.indexOf('{', i), depth = 0, k = j;
  for(; k < html.length; k++){
    if(html[k] === '{') depth++;
    else if(html[k] === '}'){ depth--; if(depth === 0){ k++; break; } }
  }
  return html.slice(i, k);
}

var STORY_TITLE_SOFT = {};
var CASES = {};
var BehaviorGate = { progressToward: function(arg){ return CASES[arg.id] || null; } };
var StoryOC = { isDone: function(){ return false; } };
eval(extractFn('function prog71Title') + '\n' + extractFn('function prog71StubItems'));
function texts(id){ return (prog71StubItems(id) || []).map(function(it){ return it.text; }); }

/* C3：單地點鎖行 */
CASES.C3 = { done:false, needDone:['C2'], weekMin:6, week:4, gigNeed:0, gigHave:0,
  remain:['到星河電視台播', '聲望需多於 15（現 5）'] };
const c3 = texts('C3');
ok('C3 鎖行：單地點改做標籤式「場景：星河電視台」', c3.indexOf('場景：星河電視台') >= 0);
ok('C3 鎖行：成列冇「（場景：」括號寫法', c3.every(function(t){ return t.indexOf('（場景：') < 0; }));
ok('C3 鎖行：其餘條件句唔變（前置／週數／聲望）',
  c3.indexOf('先完成第 2 幕〈C2〉') >= 0
  && c3.indexOf('到第 6 週（而家第 4 週）') >= 0
  && c3.indexOf('聲望要多於 15（而家 5）') >= 0);

/* C4：OR 行 */
CASES.C4 = { done:false, needDone:['C3'], weekMin:8, week:4, gigNeed:0, gigHave:0,
  remain:['人情債 0／1／何生人情 0／1／或到何生事務所'] };
const c4 = texts('C4');
ok('C4 OR 行：改做標籤式「或場景：何生事務所」',
  c4.indexOf('以下任一達標：人情債 0／1／何生人情 0／1／或場景：何生事務所') >= 0);
ok('C4 OR 行：成列冇「（場景：」括號寫法', c4.every(function(t){ return t.indexOf('（場景：') < 0; }));
ok('C4 OR 行：冇留「或到」觸發寫法', c4.every(function(t){ return t.indexOf('或到') < 0; }));

/* C5：多地點鎖行（同 C3 同一 lm 分支，raw 係「到 A 或 B 播」） */
CASES.C5 = { done:false, needDone:['C4'], weekMin:0, week:0, gigNeed:0, gigHave:0,
  remain:['到金龍茶餐廳或星河電視台播'] };
const c5 = texts('C5');
ok('C5 多地點鎖行：改做標籤式「場景：金龍茶餐廳或星河電視台」',
  c5.indexOf('場景：金龍茶餐廳或星河電視台') >= 0);
ok('C5 多地點鎖行：成列冇「（場景：」括號寫法', c5.every(function(t){ return t.indexOf('（場景：') < 0; }));

/* 守衛：傳聞提示等其餘 remain 項唔變 */
CASES.C3b = { done:false, needDone:[], weekMin:0, week:0, gigNeed:0, gigHave:0,
  remain:['未聽聞「高仔片場搶鏡」（去金龍茶餐廳打聽）'] };
const c3b = texts('C3b');
ok('守衛：傳聞提示「聽到傳聞」唔變（條件提示，唔係觸發句）',
  c3b.indexOf('聽到傳聞：「高仔片場搶鏡」（去金龍茶餐廳打聽）') >= 0);

console.log(fails.length ? ('STORY179 LOGIC: ' + fails.length + ' FAIL -> ' + fails.join(' | ')) : 'STORY179 LOGIC: ALL PASS');
process.exit(fails.length ? 1 : 0);
