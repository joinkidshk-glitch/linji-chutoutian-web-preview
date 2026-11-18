// v20a297 重寫：Vera／關海媚成個移除——
//   (1) 舊 N16 synopsis 硬編 SRC（1990年冬緋聞草稿＋關海媚）係 RW-9 之前嘅凍結文案，
//       live N16（飛紙仔）早已重寫，唔再提佢；改為讀 live pack N16 synopsis 驗原樣輸出＋零關海媚。
//   (2) TEXTFIX55_NOTE_EXACT 兩句 rel_mei outcome note 已刪；textfix55Note 泛用路徑應將
//       rel_mei 當殘留 token 清走，唔再解做關海媚。
//   (3) TEXTFIX55_NOTE_EXACT 唔可以再有 vera／mei 鍵。
// Extraction mirrors tests/test_terms57_logic.js (TEXTFIX block eval).
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || 'index.html';
const s = fs.readFileSync(htmlPath, 'utf8');
const ROOT = path.dirname(path.resolve(htmlPath));
const a = s.indexOf('/* ==== v20a55 TEXTFIX');
const b = s.indexOf('async function refreshCopyPacksFromDisk(){');
if (a < 0 || b < 0 || b <= a) { console.log('FAIL TEXTFIX block not found'); process.exit(1); }
const TF = eval(s.slice(a, b) + '\n;({ TEXTFIX55_OPTS_STORY, TEXTFIX55_OPTS_SIMPLE, TEXTFIX55_EXACT, TEXTFIX55_PHRASES, TEXTFIX55_NOTE_EXACT, textfix55Str, textfix55Note });');
let fails = [];
function chk(name, cond) { if (!cond) fails.push(name); console.log((cond ? 'PASS ' : 'FAIL ') + name); }

// (1) live N16 synopsis 原樣輸出＋零關海媚
const pack = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'story_detail_n1_to_n17.json'), 'utf8'));
const n16 = (pack.nodes || []).find(n => n.id === 'N16');
chk('live N16 在位', !!n16 && typeof n16.synopsis === 'string' && n16.synopsis.length > 0);
chk('live N16 synopsis 零關海媚', n16.synopsis.indexOf('關海媚') < 0);
const out = TF.textfix55Str(n16.synopsis, 'synopsis', null, TF.TEXTFIX55_OPTS_STORY);
chk('N16 synopsis 原樣輸出', out === n16.synopsis);
chk('N16 out 零關海媚', out.indexOf('關海媚') < 0);
chk('N16 out 零當紅花旦', out.indexOf('當紅花旦') < 0);

// PHRASES no longer rewrites her name anywhere
chk('PHRASES no 關海媚 pair', !TF.TEXTFIX55_PHRASES.some(p => p[0] === '關海媚'));
chk('bare name survives phrases', TF.textfix55Str('關海媚', 'lines', null, TF.TEXTFIX55_OPTS_STORY) === '關海媚');
// Other PHRASES pairs still live
chk('other phrase intact', TF.textfix55Str('星河電視城', 'lines', null, TF.TEXTFIX55_OPTS_STORY) === '星河電視台');

// (2) 兩句舊 note：exact 條目已刪，泛用路徑清走 rel_mei，唔再解做關海媚
const n1 = TF.textfix55Note('公開承認；fame 升，rel_choi／rel_mei 微升，公開戀愛壓力開始。');
chk('note 公開承認零關海媚', n1.indexOf('關海媚') < 0);
chk('note 公開承認零 rel_mei', n1.indexOf('rel_mei') < 0);
chk('note 公開承認零當紅花旦', n1.indexOf('當紅花旦') < 0);
const n2 = TF.textfix55Note('對外否認；形象暫穩，但 rel_choi／rel_mei 下滑。');
chk('note 對外否認零關海媚', n2.indexOf('關海媚') < 0);
chk('note 對外否認零 rel_mei', n2.indexOf('rel_mei') < 0);
chk('note 對外否認零當紅花旦', n2.indexOf('當紅花旦') < 0);

// (3) NOTE_EXACT 零 vera／mei 鍵
chk('NOTE_EXACT 零 rel_vera 鍵', !Object.keys(TF.TEXTFIX55_NOTE_EXACT).some(k => k.indexOf('rel_vera') >= 0));
chk('NOTE_EXACT 零 rel_mei 鍵', !Object.keys(TF.TEXTFIX55_NOTE_EXACT).some(k => k.indexOf('rel_mei') >= 0));
chk('NOTE_EXACT 零 Vera／關海媚', JSON.stringify(TF.TEXTFIX55_NOTE_EXACT).indexOf('Vera') < 0 && JSON.stringify(TF.TEXTFIX55_NOTE_EXACT).indexOf('關海媚') < 0);

console.log(fails.length ? ('FAILURES: ' + fails.join(', ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
