// v20a301 Q14-B：只對調 1.11 A／B（廖 Beat 2 獎懲倒轉修正）
//   舊：A（應承懂做人，表現好）→ tv_209《大排檔鬥氣》秋／$55–65／2 日；
//       B（追問金主，表現差）→ tv_210《街市喜宴》冬／$80–100／3 日。
//   新：A → tv_210（冬檔高薪），B → tv_209（秋檔低薪）。只改 GRANT229_CHOICE 兩行 gigId，
//       reason 文字、其餘 7 格、A 位、通告庫全部唔郁。
// 用法：node tests/test_r301_swap_111.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const GIGS_NEW = require('../content/gigs_new.json');
const gigById = (id)=> (Array.isArray(GIGS_NEW) ? GIGS_NEW : (GIGS_NEW.gigs||[])).find(g=>g && g.id===id) || null;
let fails = [];
let total = 0;
function ok(name, cond){ total++; if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }
function extractConst(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('const not found: ' + name);
  let depth = 0, started = false, j = i;
  for(; j < html.length; j++){
    const c = html[j];
    if(c === '{' || c === '['){ depth++; started = true; }
    else if(c === '}' || c === ']'){ depth--; if(started && depth === 0){ j++; break; } }
    else if(c === ';' && !started) { j++; break; }
  }
  return html.slice(i, j);
}
const asVar = (code, name)=> code.replace('const ' + name + ' =', 'var ' + name + ' =');
eval(asVar(extractConst('GRANT229_CHOICE'), 'GRANT229_CHOICE') + '\n' +
     asVar(extractConst('GRANT229_ENC79'), 'GRANT229_ENC79') + '\n' +
     asVar(extractConst('GRANT229_DRAFT'), 'GRANT229_DRAFT'));

const A = GRANT229_CHOICE['W3_ho_liao:W3_ho_liao_a'];
const B = GRANT229_CHOICE['W3_ho_liao:W3_ho_liao_b'];
ok('1.11 A→tv_210（表現好攞冬檔高薪）', A && A.gigId === 'gig_1990_tv_210');
ok('1.11 B→tv_209（追問金主攞秋檔低薪）', B && B.gigId === 'gig_1990_tv_209');
ok('1.11 A／B 兩張唔同', A && B && A.gigId !== B.gigId);
ok('1.11 reason 文字唔郁（兩行一樣）', A && B && A.reason === B.reason && A.reason === '何生今朝話，喜劇組嗰邊有個替身雜務位留咗畀你，聽朝去報到。');
ok('1.11 source 唔郁', A && B && A.source === '廖炳星支線' && B.source === '廖炳星支線');

const g210 = gigById('gig_1990_tv_210');
const g209 = gigById('gig_1990_tv_209');
ok('tv_210 係冬／臨記／pay [112,140]／3 日（v390 ×1.4）', g210 && g210.season === '冬' && g210.tier === '臨記' && JSON.stringify(g210.pay) === '[112,140]' && g210.days === 3);
ok('tv_209 係秋／臨記／pay [77,91]／2 日（v390 ×1.4）', g209 && g209.season === '秋' && g209.tier === '臨記' && JSON.stringify(g209.pay) === '[77,91]' && g209.days === 2);
ok('獎懲啱返：A 嗰張 pay／days 高過 B 嗰張', g210 && g209 && g210.pay[0] > g209.pay[0] && g210.days > g209.days);
ok('兩張皆電視劇喜劇替身雜務 1990（廖炳星有份）', [g210, g209].every(g=> g && g.type === '電視劇' && g.genre === '喜劇' && g.roleLabel === '喜劇替身雜務' && g.year === 1990 && JSON.stringify(g.cast || {}).indexOf('liu_bingxing') >= 0));

/* 其餘 7 格唔郁：ENC79 初遇池 9 行＋1.14 draft */
function enc79GigIds(seg){
  return GRANT229_ENC79.filter(r=>r && r.seg === seg).map(r=>r.gigId).sort();
}
ok('1.10 廖初遇三張唔郁（tv_217／218／219）', JSON.stringify(enc79GigIds('first:liu_bingxing')) === JSON.stringify(['gig_1990_tv_217','gig_1990_tv_218','gig_1990_tv_219']));
ok('1.13 顧初遇三張唔郁（rec_209／201／210）', JSON.stringify(enc79GigIds('first:gu_mingfai')) === JSON.stringify(['gig_1990_rec_201','gig_1990_rec_209','gig_1990_rec_210']));
ok('1.17 麥初遇三張唔郁（film_211／213／214）', JSON.stringify(enc79GigIds('first:mak_zhendong')) === JSON.stringify(['gig_1990_film_211','gig_1990_film_213','gig_1990_film_214']));
ok('1.14 顧 Beat 2 唔郁（gu_ask_back→rec_207）', GRANT229_DRAFT && GRANT229_DRAFT.gu_ask_back && GRANT229_DRAFT.gu_ask_back.gigId === 'gig_1991_rec_207');

/* 無重用衝突：全 CHOICE 表入面 tv_209／tv_210 各得一格 */
const choiceIds = Object.values(GRANT229_CHOICE).map(r=>r && r.gigId);
ok('tv_209 喺 CHOICE 表得一格', choiceIds.filter(id=>id === 'gig_1990_tv_209').length === 1);
ok('tv_210 喺 CHOICE 表得一格', choiceIds.filter(id=>id === 'gig_1990_tv_210').length === 1);
ok('1.11 兩格喺庫入面（唔係死 id）', !!g210 && !!g209);

if(fails.length){ console.log('FAILURES: ' + fails.length); process.exit(1); }
console.log('ALL PASS (' + total + ' checks)');
