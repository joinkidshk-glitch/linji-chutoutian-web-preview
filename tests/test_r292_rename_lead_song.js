// v20a292 Q4 兩張《主打歌》唱片通告改名：邏輯測試——
//   (1) rec_108 →《只差一步》MV 男主角（1992 秋）、rec_111 →《銅鑼灣》MV 男主角（1992 春）；
//   (2) 兩張新名唔同、workTitle 唔再係「主打歌」，全庫再無 workTitle 係「主打歌」嘅 gig；
//   (3) 其餘欄位不變：singer／pay／tier／season／year／req／genre／format／days／fame／type／loc／
//       storyKeys／trigger（rec_111 駱家聲人情）全部照舊；
//   (4) 新 workTitle 各自喺全庫只出現一次；blurb／synopsis 提新歌名、唔再提《主打歌》；
//   (5) index.html 接駁位跟埋新名：N14_a 即派 reason＋BR89 註解。
// 新名依據（見 NOTES_V20A292_RENAME_LEAD_SONG.md）：跟 TITLE_AUDIT §4 唱片規律＋R1–R8；
//   《只差一步》四字短句（封王前夕「只差一步」＋情歌「差一步講出口」）；《銅鑼灣》地名做歌名
//   （對照〈皇后大道東〉，AUDIT §6 樣本 11 曾提議；MV 本身就係銅鑼灣街頭雨夜追電車）。
//   兩個名都做過網上撞名抽查：無香港歌曲叫《只差一步》／《銅鑼灣》；
//   《一步之遙》撞任然同名歌、《並肩行》撞庫內《並肩前行》，兩個都棄用。
// 用法：node tests/test_r292_rename_lead_song.js [path-to-repo-root]
const fs = require('fs');
const path = require('path');
const ROOT = process.argv[2] || path.join(__dirname, '..');
const gigs = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gigs_new.json'), 'utf8')).gigs;
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
const byId = id => gigs.find(g => g.id === id);
const g108 = byId('gig_1992_rec_108');
const g111 = byId('gig_1992_rec_111');

/* ---- (1) 新名 ---- */
ok('rec_108 title 係《只差一步》MV 男主角', g108 && g108.title === '《只差一步》MV 男主角');
ok('rec_108 workTitle 係只差一步', g108 && g108.workTitle === '只差一步');
ok('rec_111 title 係《銅鑼灣》MV 男主角', g111 && g111.title === '《銅鑼灣》MV 男主角');
ok('rec_111 workTitle 係銅鑼灣', g111 && g111.workTitle === '銅鑼灣');

/* ---- (2) 兩張唔同、舊名清零 ---- */
ok('兩張 title 唔同', g108 && g111 && g108.title !== g111.title);
ok('兩張 workTitle 唔同', g108 && g111 && g108.workTitle !== g111.workTitle);
ok('全庫再無 workTitle 係「主打歌」', gigs.every(g => g.workTitle !== '主打歌'));
ok('兩張 title 唔再含《主打歌》', g108 && g111 && g108.title.indexOf('主打歌') < 0 && g111.title.indexOf('主打歌') < 0);

/* ---- (3) 其餘欄位不變 ---- */
function sameFields(g, season){
  return g && g.singer === 'luk_baakyin' && g.singerGender === 'M'
    && JSON.stringify(g.pay) === '[600,720]' && g.tier === '高級'
    && g.year === 1992 && g.season === season
    && g.req && g.req.acting === 85 && g.req.stage === 65 && g.req.vocal === 55
    && g.genre === '情歌' && g.format === 'MTV' && g.days === 3
    && JSON.stringify(g.fame) === '[42,60]' && g.type === '唱片通告'
    && g.category === '作品' && g.loc === 'rec_star'
    && JSON.stringify(g.storyKeys) === '["N14"]';
}
ok('rec_108 其餘欄位不變（singer／pay／tier／秋／req／情歌／MTV）', sameFields(g108, '秋'));
ok('rec_111 其餘欄位不變（singer／pay／tier／春／req／情歌／MTV）', sameFields(g111, '春'));
ok('rec_111 trigger 照舊（駱家聲人情）', g111 && g111.trigger && g111.trigger.kind === 'credit'
  && g111.trigger.creditId === 'credit_enc83_lok_patron' && g111.trigger.creditOwner === '駱家聲');
ok('rec_108／rec_111 roleLabel 照舊 MV 男主角', g108 && g111 && g108.roleLabel === 'MV 男主角' && g111.roleLabel === 'MV 男主角');

/* ---- (4) 新名唯一＋文案跟名 ---- */
ok('只差一步喺全庫只出現一次', gigs.filter(g => g.workTitle === '只差一步').length === 1);
ok('銅鑼灣喺全庫只出現一次', gigs.filter(g => g.workTitle === '銅鑼灣').length === 1);
ok('rec_108 blurb／synopsis 提《只差一步》、唔提《主打歌》',
  g108 && g108.blurb.indexOf('《只差一步》') >= 0 && g108.synopsis.indexOf('《只差一步》') >= 0
  && g108.blurb.indexOf('主打歌') < 0 && g108.synopsis.indexOf('主打歌') < 0);
ok('rec_111 blurb 提《銅鑼灣》、唔提《主打歌》',
  g111 && g111.blurb.indexOf('《銅鑼灣》') >= 0 && g111.blurb.indexOf('主打歌') < 0);
ok('rec_111 synopsis 唔提《主打歌》（本身無舊名，照舊）', g111 && g111.synopsis.indexOf('主打歌') < 0);

/* ---- (5) index.html 接駁位 ---- */
ok('N14_a 即派 reason 用《銅鑼灣》、唔用《主打歌》',
  html.indexOf('陸柏言新碟《銅鑼灣》MV要個街頭男主角') >= 0
  && html.indexOf('陸柏言新碟《主打歌》MV') < 0);
ok('BR89 註解用《銅鑼灣》MV（駱）→rec_111',
  html.indexOf('《銅鑼灣》MV（駱）→gig_1992_rec_111《銅鑼灣》MV') >= 0);
ok('index.html 再無《主打歌》MV 標題引用（N8 通用「主打歌星」除外）',
  (html.match(/《主打歌》/g) || []).length === 0);

if(fails.length){ console.log('FAILURES: ' + fails.join(' | ')); process.exit(1); }
console.log('ALL PASS');
