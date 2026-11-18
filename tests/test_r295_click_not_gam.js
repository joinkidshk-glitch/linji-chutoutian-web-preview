// v20a295 Q8: ["點擊","撳"] pair removed from TEXTFIX57_PHRASES — all player
// text uses 「點擊」; dialogue 「撳」 (Cantonese, e.g. 藍若曦's 撳通告牌) stays.
// Also covers the 13 hardcoded non-dialogue UI strings that said 撳 in source
// (the pair alone never produced them) and the TEXTFIX57_EXACT tutorial value.
const fs = require('fs');
const path = process.argv[2] || 'index.html';
const s = fs.readFileSync(path, 'utf8');
const a = s.indexOf('/* ==== v20a55 TEXTFIX');
const b = s.indexOf('async function refreshCopyPacksFromDisk(){');
if (a < 0 || b < 0 || b <= a) { console.log('FAIL TEXTFIX block not found'); process.exit(1); }
const TF = eval(s.slice(a, b) + '\n;({ TEXTFIX55_OPTS_STORY, TEXTFIX55_OPTS_SIMPLE, TEXTFIX57_EXACT, TEXTFIX57_PHRASES, textfix55Str });');
let fails = [];
function chk(name, cond) { if (!cond) fails.push(name); console.log((cond ? 'PASS ' : 'FAIL ') + name); }

// 1. table: exactly the three remaining pairs, no 點擊 pair
chk('table has 3 pairs', TF.TEXTFIX57_PHRASES.length === 3);
chk('table has no 點擊 pair', !TF.TEXTFIX57_PHRASES.some(function (p) { return p[0] === '點擊' || p[1] === '撳'; }));
chk('table keeps 事態->劇情', TF.TEXTFIX57_PHRASES.some(function (p) { return p[0] === '事態' && p[1] === '劇情'; }));
chk('table keeps 聲量->聲望', TF.TEXTFIX57_PHRASES.some(function (p) { return p[0] === '聲量' && p[1] === '聲望'; }));
chk('table keeps 周刊->週刊', TF.TEXTFIX57_PHRASES.some(function (p) { return p[0] === '周刊' && p[1] === '週刊'; }));

// 2. runtime: 點擊 survives textfix55Str in every key family; other pairs still fire
chk('點擊 kept in body', TF.textfix55Str('請點擊繼續', 'body', null, TF.TEXTFIX55_OPTS_SIMPLE) === '請點擊繼續');
chk('點擊 kept in lines', TF.textfix55Str('點擊呢個掣', 'lines', null, TF.TEXTFIX55_OPTS_STORY) === '點擊呢個掣');
chk('點擊 kept in title', TF.textfix55Str('點擊開始', 'title', null, TF.TEXTFIX55_OPTS_SIMPLE) === '點擊開始');
chk('事態 still -> 劇情', TF.textfix55Str('相遇事態', 'category', null, TF.TEXTFIX55_OPTS_SIMPLE) === '相遇劇情');
chk('聲量 still -> 聲望', TF.textfix55Str('佢聲量好高', 'lines', null, TF.TEXTFIX55_OPTS_STORY) === '佢聲望好高');
chk('周刊 still -> 週刊', TF.textfix55Str('《星訊周刊》今期出街', 'title', null, TF.TEXTFIX55_OPTS_STORY) === '《星訊週刊》今期出街');

// 3. source: the 13 hardcoded UI strings now say 點擊
chk('hospital FAQ', s.indexOf('撳入嚟睇') < 0 && s.indexOf('治療／探病／體檢——邊樣幾時先有，點擊入嚟睇') >= 0);
chk('planner confirm', s.indexOf('改完要點擊確定才生效') >= 0);
chk('planner readonly', s.indexOf('可點擊「壓力估」看已定行程') >= 0);
chk('day toast', s.indexOf('要過日請點擊「開始今日行程」') >= 0);
chk('dismiss notes x4', s.indexOf('點擊外面＝回家結算') >= 0 && s.indexOf('點擊外面＝返回地圖') >= 0 && s.indexOf('點擊外面＝繼續跑明日行程') >= 0 && s.indexOf('點擊外面＝開始今日行程') >= 0);
chk('free-day titles', (s.match(/逛完點擊這個掣返回屋企睡覺，過到下一日/g) || []).length === 2);
chk('awards tap hint', s.indexOf('點擊畫面可以快進') >= 0);
chk('gig board toast', s.indexOf('請在地圖點擊有通告的地點') >= 0);
chk('no 撳外面 left', s.indexOf('撳外面') < 0);

// 3b. source: 6 more UI strings that hid in template literals (found via the
// static test's tokenizer, not a plain quote scan)
chk('hospital checkup hint', s.indexOf('點擊「身體檢查」嗰陣會先確認') >= 0);
chk('train jump hint', s.indexOf('點擊下面「去訓練／手帳」') >= 0);
chk('planner confirm hint', s.indexOf('點擊「確定出發」就會落實行程') >= 0);
chk('dialogue lock hint', s.indexOf('點擊「完成對白」才可以繼續') >= 0);
chk('gift shop hint', s.indexOf('地點選單點擊「買禮物」買入') >= 0);
chk('jobs book hint', s.indexOf('點擊下面可直達') >= 0);

// 4. dialogue 撳 untouched (Cantonese dialogue is legitimate)
chk('dialogue 撳通告牌 kept', s.indexOf('專幫人撳通告牌') >= 0);
chk('dialogue 撳牌 kept', s.indexOf('第日你唔使人撳牌嗰陣') >= 0);

// 5. TEXTFIX57_EXACT tutorial value aligned (dead entry: key lives only in a mock)
chk('EXACT tutorial value uses 點擊', s.indexOf('再點擊「確認拼合」。唔識拖都得，點擊嚟揀都得。') >= 0);

console.log(fails.length ? ('FAILURES: ' + fails.join(', ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
