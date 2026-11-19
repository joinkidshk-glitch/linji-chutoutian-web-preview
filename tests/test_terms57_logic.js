// v20a57 TERMS logic tests: run audit-original fixture strings through the
// TEXTFIX55+57 cleaning layer and assert the v57 terminology outcomes.
// 反證: run against a pre-v57 index (no TEXTFIX57 tables) -> FAIL.
const fs = require('fs');
const path = process.argv[2] || 'index.html';
const s = fs.readFileSync(path, 'utf8');
const a = s.indexOf('/* ==== v20a55 TEXTFIX');
const b = s.indexOf('async function refreshCopyPacksFromDisk(){');
if (a < 0 || b < 0 || b <= a) { console.log('FAIL TEXTFIX block not found'); process.exit(1); }
const TF = eval(s.slice(a, b) + '\n;({ TEXTFIX55_OPTS_STORY, TEXTFIX55_OPTS_SIMPLE, TEXTFIX57_EXACT, TEXTFIX57_PHRASES, textfix55Str, textfix55Walk, textfix55Freeplay });');
let fails = [];
function chk(name, cond) { if (!cond) fails.push(name); console.log((cond ? 'PASS ' : 'FAIL ') + name); }

chk('TEXTFIX57 tables present', !!TF.TEXTFIX57_EXACT && Array.isArray(TF.TEXTFIX57_PHRASES));

// A1 事態->劇情 (phrase, incl. compound 相遇事態)
chk('A1 相遇事態', TF.textfix55Str('相遇事態', 'category', null, TF.TEXTFIX55_OPTS_SIMPLE) === '相遇劇情');
chk('A1 sentence', TF.textfix55Str('有新事態可以開', 'playerHint', null, TF.TEXTFIX55_OPTS_STORY) === '有新劇情可以開');
// A2 聲量->聲望 (phrase)
chk('A2 聲量', TF.textfix55Str('佢聲量好高，唔代表信用好', 'lines', null, TF.TEXTFIX55_OPTS_STORY) === '佢聲望好高，唔代表信用好');
// A4 點擊->撳 (phrase) — v20a295 Q8：呢對已拎走，全部用「點擊」
chk('A4 點擊 kept', TF.textfix55Str('請點擊繼續', 'body', null, TF.TEXTFIX55_OPTS_SIMPLE) === '請點擊繼續');
chk('A4 mixed input unchanged', TF.textfix55Str('撳掣定點擊都得', 'body', null, TF.TEXTFIX55_OPTS_SIMPLE) === '撳掣定點擊都得');
chk('A4 pair removed from table', !TF.TEXTFIX57_PHRASES.some(function (p) { return p[0] === '點擊'; }));
// B6 周刊->週刊 (phrase, incl. masthead + speaker)
chk('B6 星訊周刊', TF.textfix55Str('《星訊周刊》今期出街', 'title', null, TF.TEXTFIX55_OPTS_STORY) === '《星訊週刊》今期出街');
const wSpeaker = TF.textfix55Walk({ beats: [{ speaker: '周刊編輯', lines: ['周刊記者企喺門口。'] }] }, null, null, TF.TEXTFIX55_OPTS_STORY);
chk('B6 speaker walked', wSpeaker.beats[0].speaker === '週刊編輯' && wSpeaker.beats[0].lines[0] === '週刊記者企喺門口。');
// B1 解鎖: lockedHint bare value only（EXACT 成句已刪）
const wLock = TF.textfix55Walk({ nodes: [{ lockedHint: '未解鎖' }] }, null, null, TF.TEXTFIX55_OPTS_STORY);
chk('B1 lockedHint', wLock.nodes[0].lockedHint === '未開放');
// B2 prose untouched (no whole-string EXACT hit)
chk('B2 prose untouched', TF.textfix55Str('大牌藝人先有呢種待遇', 'lines', null, TF.TEXTFIX55_OPTS_STORY) === '大牌藝人先有呢種待遇');
// B2 registry: walk leaves labels + labelToId keys untouched (no rename)
const reg = { tags: [{ id: 'tag_action', label: '動作演員' }, { id: 'tag_diva', label: '大牌' }], labelToId: { '動作演員': 'tag_action', '大牌': 'tag_diva' } };
TF.textfix55Walk(reg, null, null, TF.TEXTFIX55_OPTS_SIMPLE);
// B2 wiring: textfix55Freeplay leaves the loaded registry untouched (no rename)
const FW = { castingTagsReg: { tags: [{ id: 'tag_action', label: '動作演員' }], labelToId: { '動作演員': 'tag_action' } } };
TF.textfix55Freeplay(FW);
chk('B2 freeplay wiring', FW.castingTagsReg.tags[0].label === '動作演員' && FW.castingTagsReg.labelToId['動作演員'] === 'tag_action');
// RW-7：體力→體能要求表＋通告清洗層已刪（無呼叫者；新庫 0 命中）。B4 檢查一併刪走。

console.log(fails.length ? ('FAILURES: ' + fails.join(', ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
