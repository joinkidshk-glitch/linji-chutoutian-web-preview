// v20a85 POSTER85 邏輯測試：A 級 59 張作品圖檔案參照接入。
// - POSTER85_IDS 恰好 59 個、全部係選角表 A 級（本檔內嵌權威清單）、全部真喺 1988 包、
//   同試點 POSTER59_IDS 零重疊；
// - poster59Path 對 A59 回 assets/posters/poster-<id 去 gig_>.webp（poster85File 衍生一致）；
// - 試點 10 張仍回 data URI（優先序冇回歸）；B 級／散工／入門／亂 id 回空（降級路徑）；
// - 圖檔真存在喺 index 同級 assets/posters/，且係 WebP RIFF、體積合理。
// 反證：對 v20a84 index 行 → POSTER85_IDS 抽取唔到即 FAIL。
// 用法：node tests/test_poster85_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const rootDir = path.dirname(htmlPath);
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) throw new Error('fn not found: '+name);
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){
    if(html[j]==='{') depth++;
    else if(html[j]==='}'){ depth--; if(depth===0) break; }
  }
  return html.slice(i, j+1);
}
function extractConst(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) throw new Error('const not found: '+name);
  let depth = 0, started = false;
  for(let k=i; k<html.length; k++){
    const ch = html[k];
    if(ch==='{'||ch==='['){ depth++; started = true; }
    else if(ch==='}'||ch===']'){ depth--; if(started && depth===0) return html.slice(i, k+1)+';'; }
    else if(ch===';' && !started) return html.slice(i, k+1);
  }
  throw new Error('const end not found: '+name);
}
let WORLD;
try{
  WORLD = ['POSTER59_IDS','POSTER85_IDS'].map(c=>extractConst(c).replace('const '+c,'var '+c)).join('\n')
    + '\nvar POSTER59_DATA = {"gig_1988_tv_06":"data:image/webp;base64,STUB"};\n'
    + ['poster85File','poster59Path'].map(f=>extractFn(f)).join('\n');
}catch(e){ console.log('FAIL extraction: '+e.message); process.exit(1); }
eval(WORLD);

/* 選角表 A 級權威清單（linji-poster-casting-1990.md，59 部） */
const A59 = ['gig_1988_ad_03','gig_1988_ad_05','gig_1988_ad_06','gig_1988_ad_07','gig_1988_ad_08',
'gig_1988_ad_adm_autumn_high','gig_1988_ad_adm_spring_high','gig_1988_ad_adm_spring_mid','gig_1988_ad_adm_summer_high','gig_1988_ad_adm_winter_high',
'gig_1988_ad_central_autumn_high','gig_1988_ad_central_spring_mid','gig_1988_ad_central_summer_high',
'gig_1988_film_04','gig_1988_film_05','gig_1988_film_06','gig_1988_film_07',
'gig_1988_film_cotton_autumn_high','gig_1988_film_cotton_spring_mid','gig_1988_film_cotton_summer_high',
'gig_1988_film_harbour_spring_high','gig_1988_film_harbour_spring_mid','gig_1988_film_harbour_summer_high','gig_1988_film_harbour_winter_high',
'gig_1988_film_lion_autumn_high','gig_1988_film_lion_spring_high','gig_1988_film_lion_spring_mid','gig_1988_film_lion_winter_mid',
'gig_1988_mtv_wanchai_autumn_mid','gig_1988_mtv_wanchai_summer_mid',
'gig_1988_photo_02','gig_1988_rec_04',
'gig_1988_rec_hk_autumn_high','gig_1988_rec_hk_spring_high','gig_1988_rec_hk_spring_mid','gig_1988_rec_hk_summer_high','gig_1988_rec_hk_winter_high','gig_1988_rec_hk_winter_mid',
'gig_1988_rec_star_autumn_high','gig_1988_rec_star_spring_high','gig_1988_rec_star_summer_high','gig_1988_rec_star_summer_mid',
'gig_1988_rec_wanchai_autumn_high','gig_1988_rec_wanchai_spring_high','gig_1988_rec_wanchai_summer_high','gig_1988_rec_wanchai_winter_high',
'gig_1988_tv_07','gig_1988_tv_08','gig_1988_tv_kowloon_winter_high','gig_1988_tv_longmen_spring_mid',
'gig_1988_tvb_harbour_autumn_high','gig_1988_tvb_harbour_spring_high','gig_1988_tvb_harbour_summer_high','gig_1988_tvb_kowloon_autumn_high',
'gig_1988_tvb_kowloon_summer_high','gig_1988_tvb_kowloon_spring_high',
'gig_1988_tvb_longmen_spring_high','gig_1988_tvb_longmen_summer_high',
'gig_1988_var_05'];

const keys = Object.keys(POSTER85_IDS);
ok('ids: POSTER85_IDS 恰好 59', keys.length===59);
ok('ids: 同選角表 A 級清單完全一致（冇漏冇多）',
  A59.every(id=>POSTER85_IDS[id]===1) && keys.every(k=>A59.indexOf(k)>=0));
const PACK88 = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'gigs_1988.json'), 'utf8'));
const packIds = new Set(PACK88.gigs.map(g=>g.id));
ok('ids: 59 個全部真喺 1988 包', A59.every(id=>packIds.has(id)));
ok('ids: 同試點 POSTER59_IDS 零重疊', keys.every(k=>!POSTER59_IDS[k]));

ok('path: A59 全部回檔案參照', A59.every(id=>poster59Path(id)==='assets/posters/poster-'+id.replace(/^gig_/,'')+'.webp'));
ok('path: poster85File 衍生同查表一致', A59.every(id=>poster85File(id)==='poster-'+id.replace(/^gig_/,'')+'.webp'));
ok('path: 試點仍優先回 data URI（冇回歸）', poster59Path('gig_1988_tv_06').indexOf('data:image/webp;base64,')===0);
ok('path: B 級／未出圖回空', poster59Path('gig_1988_film_02')==='' && poster59Path('gig_1988_film_01')==='');
ok('path: 散工／入門／亂 id／空值回空（降級）',
  poster59Path('gig_1988_soft_bridge_summer_ad')==='' && poster59Path('gig_1988_entry_ad_passerby')==='' &&
  poster59Path('nope')==='' && poster59Path('')==='' && poster59Path(null)==='' && poster59Path(undefined)==='');

/* 圖檔存在性＋格式（index 同級 assets/posters/） */
let missing = [], badfmt = [];
A59.forEach(id=>{
  const f = path.join(rootDir, 'assets', 'posters', poster85File(id));
  if(!fs.existsSync(f)){ missing.push(id); return; }
  const buf = fs.readFileSync(f);
  if(!(buf.length>15000 && buf.slice(0,4).toString('ascii')==='RIFF' && buf.slice(8,12).toString('ascii')==='WEBP')) badfmt.push(id+':'+buf.length);
});
ok('files: 59 張圖檔齊喺 assets/posters/', missing.length===0);
if(missing.length) console.log('  missing:', missing.join(', '));
ok('files: 全部係 WebP RIFF 且 >15KB', badfmt.length===0);
if(badfmt.length) console.log('  badfmt:', badfmt.join(', '));

if(fails.length){ console.log('FAILURES:', fails.join(' | ')); process.exit(1); }
console.log('ALL PASS');
