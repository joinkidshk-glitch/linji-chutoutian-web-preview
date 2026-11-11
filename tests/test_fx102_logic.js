// FX102 邏輯測試（v20a102）：行程動畫映射守門。
// 驗證：(1) 拍攝日映射——唱片類→record、外景關鍵字→shootExt、
//   「清水灣片場」唔誤判外景（室內廠景）→shoot、rec_ 地點→record；
//   (2) 訓練映射——歌藝/外貌→trainB、武師班→trainC、其餘四課→trainA、
//   未知課程→null；(3) 映射表 8 條齊＋路徑格式；(4) actFx102Html
//   有 kind 先出片、冇 kind 回空字串；(5) 頁內自檢 actFx102Check 全綠。
// 反證：喺 v20a101 index 上行 → 函數唔存在，extractFn 拋錯 FAIL。
// 用法：node tests/test_fx102_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');

let pass = 0, fail = 0;
function ok(name, cond){
  if(cond){ pass++; console.log('  ok - ' + name); }
  else { fail++; console.log('  FAIL - ' + name); }
}
function extractFn(decl){
  const i = html.indexOf(decl);
  if(i<0) throw new Error('fn not found: '+decl);
  let j = html.indexOf('{', i), depth = 0, k = j;
  for(; k<html.length; k++){
    if(html[k]==='{') depth++;
    else if(html[k]==='}'){ depth--; if(depth===0){ k++; break; } }
  }
  return html.slice(i, k);
}
function extractConst(decl){
  const i = html.indexOf(decl);
  if(i<0) throw new Error('const not found: '+decl);
  const j = html.indexOf(';', i);
  return html.slice(i, j+1);
}

let ACT_FX102, actFx102KindForShoot, actFx102KindForTrain, actFx102Html, actFx102Check;
try{
  const src = [
    extractConst('const ACT_FX102 ='),
    extractConst('const ACT_FX102_EXT_KW ='),
    extractFn('function actFx102KindForShoot'),
    extractFn('function actFx102KindForTrain'),
    extractFn('function actFx102Html'),
    extractFn('function actFx102Check'),
    'return { ACT_FX102, actFx102KindForShoot, actFx102KindForTrain, actFx102Html, actFx102Check };'
  ].join('\n');
  const out = new Function('SAVE', src)('starVolunteer_map_v19w');
  ACT_FX102 = out.ACT_FX102;
  actFx102KindForShoot = out.actFx102KindForShoot;
  actFx102KindForTrain = out.actFx102KindForTrain;
  actFx102Html = out.actFx102Html;
  actFx102Check = out.actFx102Check;
} catch(e){
  console.log('  FAIL - extract: ' + e.message);
  process.exit(1);
}

// (3) 映射表
ok('映射表 8 條', Object.keys(ACT_FX102).length === 8);
ok('映射表路徑全 assets/fx/fx_*.mp4',
   Object.values(ACT_FX102).every(v => /^assets\/fx\/fx_[a-z_]+\.mp4$/.test(v)));

// (1) 拍攝日映射
ok('唱片通告→record', actFx102KindForShoot({type:'唱片通告', title:'錄音日'}) === 'record');
ok('type=music→record', actFx102KindForShoot({type:'music', title:'單曲'}) === 'record');
ok('電影外景標題→shootExt', actFx102KindForShoot({type:'電影', title:'廟街外景夜戲'}) === 'shootExt');
ok('電視劇街頭→shootExt', actFx102KindForShoot({type:'電視劇', title:'街頭追逐'}) === 'shootExt');
ok('清水灣片場唔誤判（室內）→shoot', actFx102KindForShoot({type:'電影', title:'清水灣片場拍攝'}) === 'shoot');
ok('一般電視劇→shoot', actFx102KindForShoot({type:'電視劇', title:'師奶劇場'}) === 'shoot');
ok('rec_ 地點→record', actFx102KindForShoot({type:'綜藝', title:'錄音節目', locId:'rec_star'}) === 'record');
ok('null→null', actFx102KindForShoot(null) === null);

// (2) 訓練映射
ok('演技→trainA', actFx102KindForTrain('train_acting') === 'trainA');
ok('台風→trainA', actFx102KindForTrain('train_stage') === 'trainA');
ok('魅力→trainA', actFx102KindForTrain('train_charm') === 'trainA');
ok('智商→trainA', actFx102KindForTrain('train_iq') === 'trainA');
ok('歌藝→trainB', actFx102KindForTrain('train_vocal') === 'trainB');
ok('外貌→trainB', actFx102KindForTrain('train_looks') === 'trainB');
ok('武師班→trainC', actFx102KindForTrain('train_stamina') === 'trainC');
ok('未知課程→null', actFx102KindForTrain('train_nope') === null);

// (4) html 生成
ok('有 kind 出 video', actFx102Html('shoot').indexOf('fx_shoot.mp4') >= 0
   && actFx102Html('shoot').indexOf('act-fx102-video') >= 0);
ok('null kind 回空', actFx102Html(null) === '');
ok('未知 kind 回空', actFx102Html('bogus') === '');

// (5) 頁內自檢
const chk = actFx102Check();
ok('actFx102Check 全綠', chk.ok === true && chk.fails.length === 0);

console.log(`FX102 logic: ${pass} pass / ${fail} fail`);
process.exit(fail ? 1 : 0);
