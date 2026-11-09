// v20a57 TERMS logic tests: run audit-original fixture strings through the
// TEXTFIX55+57 cleaning layer and assert the v57 terminology outcomes.
// 反證: run against a pre-v57 index (no TEXTFIX57 tables) -> FAIL.
const fs = require('fs');
const path = process.argv[2] || 'index.html';
const s = fs.readFileSync(path, 'utf8');
const a = s.indexOf('/* ==== v20a55 TEXTFIX');
const b = s.indexOf('async function refreshCopyPacksFromDisk(){');
if (a < 0 || b < 0 || b <= a) { console.log('FAIL TEXTFIX block not found'); process.exit(1); }
const TF = eval(s.slice(a, b) + '\n;({ TEXTFIX55_OPTS_STORY, TEXTFIX55_OPTS_SIMPLE, TEXTFIX57_EXACT, TEXTFIX57_PHRASES, TEXTFIX57_GIG_REQ, textfix55Str, textfix55Walk, textfix55GigRecord, textfix55Freeplay });');
let fails = [];
function chk(name, cond) { if (!cond) fails.push(name); console.log((cond ? 'PASS ' : 'FAIL ') + name); }

chk('TEXTFIX57 tables present', !!TF.TEXTFIX57_EXACT && Array.isArray(TF.TEXTFIX57_PHRASES) && Array.isArray(TF.TEXTFIX57_GIG_REQ));

// A1 事態->劇情 (phrase, incl. compound 相遇事態)
chk('A1 相遇事態', TF.textfix55Str('相遇事態', 'category', null, TF.TEXTFIX55_OPTS_SIMPLE) === '相遇劇情');
chk('A1 sentence', TF.textfix55Str('有新事態可以開', 'playerHint', null, TF.TEXTFIX55_OPTS_STORY) === '有新劇情可以開');
// A2 聲量->聲望 (phrase)
chk('A2 聲量', TF.textfix55Str('佢聲量好高，唔代表信用好', 'lines', null, TF.TEXTFIX55_OPTS_STORY) === '佢聲望好高，唔代表信用好');
// A4 點擊->撳 (phrase)
chk('A4 點擊', TF.textfix55Str('撳掣定點擊都得', 'body', null, TF.TEXTFIX55_OPTS_SIMPLE) === '撳掣定撳都得');
// B6 周刊->週刊 (phrase, incl. masthead + speaker)
chk('B6 星訊周刊', TF.textfix55Str('《星訊周刊》今期出街', 'title', null, TF.TEXTFIX55_OPTS_STORY) === '《星訊週刊》今期出街');
const wSpeaker = TF.textfix55Walk({ beats: [{ speaker: '周刊編輯', lines: ['周刊記者企喺門口。'] }] }, null, null, TF.TEXTFIX55_OPTS_STORY);
chk('B6 speaker walked', wSpeaker.beats[0].speaker === '週刊編輯' && wSpeaker.beats[0].lines[0] === '週刊記者企喺門口。');
// B1 解鎖: EXACT sentences + lockedHint bare value
chk('B1 unlock event', TF.textfix55Str('新課程解鎖：魅力課可以報名。', 'lines', null, TF.TEXTFIX55_OPTS_SIMPLE) === '新課程開咗：魅力課可以報名。');
chk('B1 tutorial title', TF.textfix55Str('訓練解鎖試鏡', 'title', null, TF.TEXTFIX55_OPTS_SIMPLE) === '訓練夠先報得試鏡');
const wLock = TF.textfix55Walk({ nodes: [{ lockedHint: '未解鎖' }] }, null, null, TF.TEXTFIX55_OPTS_STORY);
chk('B1 lockedHint', wLock.nodes[0].lockedHint === '未開放');
// A3 刷新: refresh hint sentence via EXACT
chk('A3 情報刷新', TF.textfix55Str('情報刷新，去金龍茶餐廳聽下新風聲。', 'randomRefreshHint', null, TF.TEXTFIX55_OPTS_SIMPLE) === '有新情報，去金龍茶餐廳聽下新風聲。');
// B2 tag values via EXACT (whole-string only)
chk('B2 動作演員 tag', TF.textfix55Str('動作演員', 'tags', null, TF.TEXTFIX55_OPTS_SIMPLE) === '身手好');
chk('B2 大牌 tag', TF.textfix55Str('大牌', 'tags', null, TF.TEXTFIX55_OPTS_SIMPLE) === '耍大牌');
chk('B2 prose untouched', TF.textfix55Str('大牌藝人先有呢種待遇', 'lines', null, TF.TEXTFIX55_OPTS_STORY) === '大牌藝人先有呢種待遇');
// B2 registry: labels renamed + labelToId KEYS renamed, ids intact (via walk)
const reg = { tags: [{ id: 'tag_action', label: '動作演員' }, { id: 'tag_diva', label: '大牌' }], labelToId: { '動作演員': 'tag_action', '大牌': 'tag_diva' } };
TF.textfix55Walk(reg, null, null, TF.TEXTFIX55_OPTS_SIMPLE);
chk('B2 registry labels', reg.tags[0].label === '身手好' && reg.tags[1].label === '耍大牌');
chk('B2 registry labelToId keys', reg.labelToId['身手好'] === 'tag_action' && reg.labelToId['耍大牌'] === 'tag_diva' && !('動作演員' in reg.labelToId) && !('大牌' in reg.labelToId));
// B2 wiring: textfix55Freeplay cleans the loaded registry
const FW = { castingTagsReg: { tags: [{ id: 'tag_action', label: '動作演員' }], labelToId: { '動作演員': 'tag_action' } } };
TF.textfix55Freeplay(FW);
chk('B2 freeplay wiring', FW.castingTagsReg.tags[0].label === '身手好' && FW.castingTagsReg.labelToId['身手好'] === 'tag_action');
// B4 體力->體能: gig requirement fragments only; prose kept
const gig = TF.textfix55GigRecord({ id: 'gx', shootHint: '極考體力與走位，需高度專注。', synopsis: '外景日曬體力消耗大，記得補水；呢張要體力與耐性。', blurb: '屬高強度體力活，量力而為。', limits: { notes: '高強度體力要求' } });
chk('B4 req pair in hint', gig.shootHint.indexOf('體能與走位') >= 0);
chk('B4 req pair in synopsis', gig.synopsis.indexOf('體能與耐性') >= 0);
chk('B4 prose 體力消耗 kept', gig.synopsis.indexOf('體力消耗大') >= 0);
chk('B4 prose 體力活 kept', gig.blurb.indexOf('體力活') >= 0);
chk('B4 體力要求 in notes', gig.limits.notes.indexOf('體能要求') >= 0);

console.log(fails.length ? ('FAILURES: ' + fails.join(', ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
