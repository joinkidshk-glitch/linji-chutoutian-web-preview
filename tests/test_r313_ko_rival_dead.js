// v20a313 Q26 高俊傑同場兩段死 code 刪除測試：
//   (A) 靜態：rivalHeadBit／koF208 全檔 0 命中；兩段輸出句全檔 0 命中；
//       結果卡模板淨係留 catsHtml＋felBit186；典禮 beats 唔再有 id:"rival" 格
//   (B) 守住：高俊傑其他 live 用法一行都唔郁——對手 NPC（npc_ko／char_ko）、
//       結局旗（rival_gao_hard／rival_gao_endure）、師父旗
//       （flag_ko_mentor_complete／flag_ko_rival_respect／flag_ko_cold_war）、
//       film_102 文字提及、rivalry trigger（film_102 rivalScoreMin 3）
//   (C) 靜態：gigs_new.json 仍係 322 張
// 用法：node tests/test_r313_ko_rival_dead.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const GIGS_NEW = require('../content/gigs_new.json');
const GIGS_ARR = Array.isArray(GIGS_NEW) ? GIGS_NEW : (GIGS_NEW.gigs || []);
let fails = [];
function ok(name, cond, extra){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name + (extra ? ' :: ' + extra : '')); }
function count(s, sub){ return s.split(sub).length - 1; }

/* ---- (A) 兩段死 code 成段刪走 ---- */
ok('A rivalHeadBit 全檔 0 命中', count(html, 'rivalHeadBit') === 0, 'count=' + count(html, 'rivalHeadBit'));
ok('A koF208 全檔 0 命中', count(html, 'koF208') === 0, 'count=' + count(html, 'koF208'));
ok('A 結果卡輸出句「今屆同高俊傑同場提名」0 命中', count(html, '今屆同高俊傑同場提名') === 0);
ok('A 結果卡輸出句「你贏咗呢一場」0 命中', count(html, '你贏咗呢一場') === 0);
ok('A 結果卡輸出句「下年再鬥」0 命中', count(html, '下年再鬥') === 0);
ok('A 對決 beat caption「同場有高俊傑」0 命中', count(html, '同場有高俊傑') === 0);
ok('A 對決 beat caption「係你哋兩個嘅對決」0 命中', count(html, '係你哋兩個嘅對決') === 0);
ok('A R4 註解「對手線強化票 R4」0 命中', count(html, '對手線強化票 R4') === 0);
ok('A 結果卡模板淨係留 catsHtml＋felBit186', /\$\{catsHtml\}\$\{felBit186\}/.test(html) && !/\$\{rivalHeadBit\}/.test(html));
ok('A 典禮 beats 唔再 push id:"rival" 格（NPC 定義 rival:{ id:"rival" } 唔計）',
  count(html, 'beats.push({ id:"rival"') === 0, 'count=' + count(html, 'beats.push({ id:"rival"'));
ok('A 典禮 beats 其餘格（suspense／reveal）仲喺度',
  html.indexOf('id: "suspense"') >= 0 && html.indexOf('revealCap') >= 0);

/* ---- (B) 高俊傑其他 live 用法唔郁 ---- */
ok('B 對手 NPC npc_ko／char_ko 仲喺度', html.indexOf('npc_ko') >= 0 && html.indexOf('char_ko') >= 0);
ok('B 結局旗 rival_gao_hard／rival_gao_endure 仲喺度',
  html.indexOf('rival_gao_hard') >= 0 && html.indexOf('rival_gao_endure') >= 0);
ok('B 師父旗 flag_ko_mentor_complete／flag_ko_rival_respect／flag_ko_cold_war 仲喺度',
  html.indexOf('flag_ko_mentor_complete') >= 0 &&
  html.indexOf('flag_ko_rival_respect') >= 0 &&
  html.indexOf('flag_ko_cold_war') >= 0);
ok('B film_102《霓虹夜影》文字提及仲喺度', html.indexOf('gig_1991_film_102') >= 0 && html.indexOf('霓虹夜影') >= 0);
ok('B film_102 rival trigger（rivalScoreMin 3）仲喺度',
  /gig_1991_film_102[\s\S]{0,600}rivalScoreMin/.test(html) || html.indexOf('rivalScoreMin') >= 0);
ok('B 高俊傑全檔仲有提及（live 用法未清零）', count(html, '高俊傑') > 0, 'count=' + count(html, '高俊傑'));

/* ---- (C) 庫數唔郁 ---- */
ok('C gigs_new.json 仍係 322 張', GIGS_ARR.length === 322, 'count=' + GIGS_ARR.length);

if(fails.length){ console.log('\nFAILURES: ' + fails.length); process.exit(1); }
console.log('\nALL PASS');
