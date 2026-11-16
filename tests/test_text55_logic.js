// v20a55 TEXTFIX logic tests: extract the TEXTFIX55 block from index.html and
// run audit-original fixture strings through the cleaners.
// 反證: run against a pre-v55 index (no TEXTFIX55 block) -> extraction fails.
const fs = require('fs');
const path = process.argv[2] || 'index.html';
const s = fs.readFileSync(path, 'utf8');
const a = s.indexOf('/* ==== v20a55 TEXTFIX');
const b = s.indexOf('async function refreshCopyPacksFromDisk(){');
if (a < 0 || b < 0 || b <= a) { console.log('FAIL TEXTFIX55 block not found'); process.exit(1); }
const TF = eval(s.slice(a, b) + '\n;({ TEXTFIX55_OPTS_STORY, TEXTFIX55_OPTS_SIMPLE, textfix55Str, textfix55Walk, textfix55Note, textfix55Label });');
let fails = [];
function chk(name, cond) { if (!cond) fails.push(name); }

// A10: rumor id leak line -> natural line
chk('A10 rumor line', TF.textfix55Str('你啱啱聽完關於星河電視台嘅傳聞 tvb_rules_gossip，心入面有好多問號。', 'lines', null, TF.TEXTFIX55_OPTS_STORY) === '你啱啱聽完星河電視台嗰啲規矩傳聞，心入面有好多問號。');
// A6: tutorial softBehaviorGate body -> natural wording
// v20a108 TEXT108 S-42：A6 期望值跟新潤飾句（舊值係 v55 橋接句，意思不變；反證：舊值喺新表下已唔再係輸出）
chk('A6 tutorial body', TF.textfix55Str('正式版同熟人「傾談／送禮」耗一日；試玩閘（softBehaviorGate）下傾談／送禮不耗日（茶錢仍可能扣費；訓練／試鏡／休息／行程表演仍耗日）。', 'body', null, TF.TEXTFIX55_OPTS_SIMPLE) === '現在和熟人傾談或者送禮都不會算一日（茶錢照扣）；只有訓練、試鏡、休息和跟行程開工才會算日。');
// C11: sent-death-question phrase swap
chk('C11 phrase', TF.textfix55Str('接送命題嗰陣', 'lines', null, TF.TEXTFIX55_OPTS_STORY) === '接辣手問題嗰陣');
// KHM (v151)：名禁令退役——display 欄位而家直出真名，唔再洗做稱號
const w1 = TF.textfix55Walk({ beats: [{ speaker: '關海媚', lines: ['關海媚企喺窗邊。'] }] }, null, null, TF.TEXTFIX55_OPTS_STORY);
chk('KHM speaker+lines', w1.beats[0].speaker === '關海媚' && w1.beats[0].lines[0] === '關海媚企喺窗邊。');
// A16/A17: effects.notes engine shorthand -> human text
chk('note ending-parallel strip', TF.textfix55Note('張子駿／文藝線；craft 高。愛情結局另表並存。') === '跟張子駿行文藝線，手藝夠硬。');
chk('note flag write', TF.textfix55Note('你拒絕咗，信用加一，寫入 flag_ho_trust') === '你拒絕咗，信用加一。');
chk('note prefix strip', TF.textfix55Note('連 N10；你企出嚟撐佢，信用升。') === '你企出嚟撐佢，信用升。');
chk('note rel map', TF.textfix55Note('你幫佢頂住；rel_hiu 大升。') === '你幫佢頂住；曉晴大升。');
chk('note label strip', TF.textfix55Label('HE：天王接班（連 T6）') === '天王接班');
// RW-7：通告清洗層已刪（新庫 241 張 0 命中）。C20／softBridge／shootHint／B63／B58 檢查一併刪走。

if (fails.length) { console.log('FAILURES:', fails.join(' | ')); process.exit(1); }
console.log('ALL PASS');
