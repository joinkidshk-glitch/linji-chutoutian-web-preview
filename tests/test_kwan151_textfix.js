// RW-9 (C): TEXTFIX55_EXACT #9 逆向映射已刪——N16 synopsis 來源已重寫做書面語，
// walk 應原樣輸出（SRC === EXPECT）；關海媚真名留返，唔再洗返廣東話。
// Extraction mirrors tests/test_terms57_logic.js (TEXTFIX block eval).
// 反證: run against pristine main (e08a070) -> FAIL (N16 value + phrases).
const fs = require('fs');
const path = process.argv[2] || 'index.html';
const s = fs.readFileSync(path, 'utf8');
const a = s.indexOf('/* ==== v20a55 TEXTFIX');
const b = s.indexOf('async function refreshCopyPacksFromDisk(){');
if (a < 0 || b < 0 || b <= a) { console.log('FAIL TEXTFIX block not found'); process.exit(1); }
const TF = eval(s.slice(a, b) + '\n;({ TEXTFIX55_OPTS_STORY, TEXTFIX55_OPTS_SIMPLE, TEXTFIX55_EXACT, TEXTFIX55_PHRASES, TEXTFIX55_NOTE_EXACT, textfix55Str, textfix55Note });');
let fails = [];
function chk(name, cond) { if (!cond) fails.push(name); console.log((cond ? 'PASS ' : 'FAIL ') + name); }

const SRC = '1990年冬，娛樂週刊已經寫好緋聞草稿。周采兒要阿偉表態；關海媚提醒阿偉，頭條是一把雙刃劍。承認、否認，抑或含糊帶過，每條路都會改寫形象與關係。';
const EXPECT = '1990年冬，娛樂週刊已經寫好緋聞草稿。周采兒要阿偉表態；關海媚提醒阿偉，頭條是一把雙刃劍。承認、否認，抑或含糊帶過，每條路都會改寫形象與關係。';
const out = TF.textfix55Str(SRC, 'synopsis', null, TF.TEXTFIX55_OPTS_STORY);
chk('N16 synopsis exact value', out === EXPECT);
chk('N16 out has 關海媚', out.indexOf('關海媚') >= 0);
chk('N16 out has no 當紅花旦', out.indexOf('當紅花旦') < 0);
chk('N16 out keeps 1990年冬 fix', out.indexOf('1990年冬，娛樂週刊已經寫好緋聞草稿') === 0);

// PHRASES no longer rewrites her name anywhere
chk('PHRASES no 關海媚 pair', !TF.TEXTFIX55_PHRASES.some(p => p[0] === '關海媚'));
chk('bare name survives phrases', TF.textfix55Str('關海媚', 'lines', null, TF.TEXTFIX55_OPTS_STORY) === '關海媚');
// Other PHRASES pairs still live
chk('other phrase intact', TF.textfix55Str('星河電視城', 'lines', null, TF.TEXTFIX55_OPTS_STORY) === '星河電視台');

// relMap in textfix55Note now resolves rel_mei to her real name
const n1 = TF.textfix55Note('公開承認；fame 升，rel_choi／rel_mei 微升，公開戀愛壓力開始。');
chk('note 公開承認 has 關海媚', n1.indexOf('關海媚') >= 0);
chk('note 公開承認 no 當紅花旦', n1.indexOf('當紅花旦') < 0);
const n2 = TF.textfix55Note('對外否認；形象暫穩，但 rel_choi／rel_mei 下滑。');
chk('note 對外否認 has 關海媚', n2.indexOf('關海媚') >= 0);
chk('note 對外否認 no 當紅花旦', n2.indexOf('當紅花旦') < 0);

console.log(fails.length ? ('FAILURES: ' + fails.join(', ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
