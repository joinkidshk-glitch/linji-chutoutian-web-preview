// v20a299 Q12 三旗遊戲中跟進測試：
//   (C) choi_spin／choi_dodge → R_choi_push1 變體（choi299PrepareNode）
//   (G) N6／N6F 四旗 → code-side 跟進通告（Q12_FOLLOW_GIGS＋mergeQ12Gigs）
//   (S) 靜態：ECHO89 結局回望唔郁、N5／N6／N6F 抉擇唔郁、gigs_new.json 仍係 322 張
// 用法：node tests/test_r299_three_flags.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond, extra){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name+(extra?' :: '+extra:'')); }
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) return null;
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){ if(html[j]==='{') depth++; else if(html[j]==='}'){ depth--; if(depth===0) break; } }
  return html.slice(i, j+1);
}
function extractConstVar(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) return null;
  let depth=0, started=false;
  for(let k=i; k<html.length; k++){
    const ch = html[k];
    if(ch==='{'||ch==='['){ depth++; started = true; }
    else if(ch==='}'||ch===']'){ depth--; if(started && depth===0) return html.slice(i, k+1).replace('const '+name, 'var '+name)+';'; }
    else if(ch===';' && !started) return html.slice(i, k+1).replace('const '+name, 'var '+name);
  }
  return null;
}

eval(extractConstVar('Q12_FOLLOW_GIGS'));
for(const f of ['enc87StoryFlag','choice47StoryFlag','q12FlagOn','q12GigDone','mergeQ12Gigs','choi299PrepareNode']){
  const src = extractFn(f);
  if(!src){ ok('抽取 function '+f, false); }
  else eval(src);
}
var S = null;
var GIGS = [];
var window = {};
var toasts = [];
var toast = function(m, opts){ toasts.push(String(m)+' | '+((opts&&opts.sub)||'')); };
var normalizeGigRecord = function(g){ return g; };
const romance = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'content', 'story_detail_romance_vera_hiu_choi.json'), 'utf8'));
const push1 = romance.nodes.find(n=>n.id==='R_choi_push1');
const meet = romance.nodes.find(n=>n.id==='R_choi_meet');
const push2 = romance.nodes.find(n=>n.id==='R_choi_push2');
const crisis = romance.nodes.find(n=>n.id==='R_choi_crisis');
const gigsLib = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'content', 'gigs_new.json'), 'utf8')).gigs;
const libTitles = new Set(gigsLib.map(g=>g.workTitle).concat(gigsLib.map(g=>g.title)));
const libLocs = new Set(gigsLib.map(g=>g.loc));

/* ---------- C1：hook 接線 ---------- */
ok('C1 choi299PrepareNode 存在', typeof choi299PrepareNode==='function');
ok('C1 StoryPlay.start 喺 rom159 之後 call choi299PrepareNode',
  html.indexOf('rom159PrepareNode(node)')>=0 && html.indexOf('choi299PrepareNode(node)')>html.indexOf('rom159PrepareNode(node)'));
ok('C1 gigsForLocSeasonBoard 喺 mergeFavorGigs 之後 call mergeQ12Gigs',
  html.indexOf('mergeFavorGigs()')>=0 && html.indexOf('mergeQ12Gigs()')>html.indexOf('mergeFavorGigs()'));

/* ---------- C2：無旗／honest／其他節點 → null ---------- */
function freshS(){ return { dayIndex:100, flags:{}, story:{ flags:{} }, wrapHistory:[] }; }
S = freshS();
ok('C2 無旗 → null', choi299PrepareNode(push1)===null);
S.flags.choi_honest = 1;
ok('C2 honest 旗 → null（行原版）', choi299PrepareNode(push1)===null);
S = freshS(); S.flags.choi_spin = 1;
ok('C2 spin 旗但唔係 push1 → null', choi299PrepareNode({ id:'R_choi_push2', beats:push1.beats, choices:push1.choices })===null);

/* ---------- C3：spin 版 ---------- */
S = freshS(); S.flags.choi_spin = 1;
const before0 = JSON.stringify(push1.beats[0]);
const beforeA = JSON.stringify(push1.choices[0].effects.stats);
const vSpin = choi299PrepareNode(push1);
ok('C3 spin → 回 copy', !!vSpin && vSpin!==push1);
ok('C3 spin beats[0] 回指休息角嗰次（人影晃過／包裝版）',
  vSpin && vSpin.beats[0].lines.join('').indexOf('人影晃過')>=0 && vSpin.beats[0].lines.join('').indexOf('包裝版')>=0);
ok('C3 spin beats[3] 情報互惠變查證後先兌現',
  vSpin && vSpin.beats[3].lines.join('').indexOf('查證')>=0);
const spinA = vSpin.choices.find(c=>c.id==='C_choi_push1_a');
const spinB = vSpin.choices.find(c=>c.id==='C_choi_push1_b');
ok('C3 spin-a rel＋1／fame＋0／落 flag_choi_spin_repaid',
  spinA.effects.stats.rel_choi===1 && spinA.effects.stats.fame===0 && spinA.effects.flags.indexOf('flag_choi_spin_repaid')>=0);
ok('C3 spin-b rel−1／standing＋1 照舊',
  spinB.effects.stats.rel_choi===-1 && spinB.effects.stats.standing===1);
ok('C3 原節點唔郁', JSON.stringify(push1.beats[0])===before0 && JSON.stringify(push1.choices[0].effects.stats)===beforeA);

/* ---------- C4：flag_ 前綴寫法（S.story.flags）都認 ---------- */
S = freshS(); S.story.flags.flag_choi_spin = 1;
const vSpin2 = choi299PrepareNode(push1);
ok('C4 S.story.flags flag_choi_spin → 同 spin 版', !!vSpin2 && vSpin2.beats[0].lines.join('').indexOf('包裝版')>=0);

/* ---------- C5：dodge 版對稱 ---------- */
S = freshS(); S.flags.choi_dodge = 1;
const vDodge = choi299PrepareNode(push1);
const dodgeA = vDodge && vDodge.choices.find(c=>c.id==='C_choi_push1_a');
const dodgeB = vDodge && vDodge.choices.find(c=>c.id==='C_choi_push1_b');
ok('C5 dodge → 回 copy，開場冷淡一句（副導叫你）',
  !!vDodge && vDodge.beats[0].lines.join('').indexOf('副導叫你')>=0);
ok('C5 dodge-a 照舊 rel＋2／fame＋1', dodgeA.effects.stats.rel_choi===2 && dodgeA.effects.stats.fame===1);
ok('C5 dodge-b rel−1（同 spin 一致）', dodgeB.effects.stats.rel_choi===-1);

/* ---------- C6：spin 全佳路線 rel 剛好夠 commit 門檻 ---------- */
const relMin = Number((html.match(/COMMIT48_REL_MIN\s*=\s*(\d+)/)||[])[1]);
const meetA = meet.choices.find(c=>c.id==='C_choi_meet_a').effects.stats.rel_choi;
const push2A = push2.choices.find(c=>c.id==='C_choi_push2_a').effects.stats.rel_choi;
const crisisA = crisis.choices.find(c=>c.id==='C_choi_crisis_a').effects.stats.rel_choi;
const spinTotal = meetA + spinA.effects.stats.rel_choi + push2A + crisisA;
ok('C6 COMMIT48_REL_MIN 係 6', relMin===6, 'relMin='+relMin);
ok('C6 spin 全佳 rel＝1＋1＋2＋2＝6，剛好夠門檻', spinTotal===6 && spinTotal>=relMin, 'total='+spinTotal);

/* ---------- G1：池形狀 ---------- */
ok('G1 池得 4 張', Array.isArray(Q12_FOLLOW_GIGS) && Q12_FOLLOW_GIGS.length===4);
const qids = Q12_FOLLOW_GIGS.map(g=>g.id);
ok('G1 四張 id 啱', ['gig_q12_canteen_grind','gig_q12_canteen_quit','gig_q12_studio_follow','gig_q12_studio_roam'].every(id=>qids.indexOf(id)>=0));
let shapeOk = true, shapeWhy = '';
Q12_FOLLOW_GIGS.forEach(g=>{
  if(g.year!==1988) { shapeOk=false; shapeWhy+=g.id+':year '; }
  if(g.season!=='不限') { shapeOk=false; shapeWhy+=g.id+':season '; }
  if(g.tier!=='臨記' || g.category!=='臨記通告') { shapeOk=false; shapeWhy+=g.id+':tier/cat '; }
  if(!(Array.isArray(g.pay) && g.pay[1]<=g.pay[0]*1.25) || g.payExact!==60) { shapeOk=false; shapeWhy+=g.id+':pay '; }
  if(JSON.stringify(g.req)!==JSON.stringify({acting:24})) { shapeOk=false; shapeWhy+=g.id+':req '; }
  if(g.shootDaysHint!==2 || JSON.stringify(g.shootBand)!==JSON.stringify([2,2])) { shapeOk=false; shapeWhy+=g.id+':days '; }
  if(/\d{4}/.test(g.title+g.workTitle+g.blurb+g.synopsis+g.roleHint+g.discoverNote)) { shapeOk=false; shapeWhy+=g.id+':年份數字 '; }
  if('trigger' in g || 'cast' in g || 'favorDelta' in g || 'applyDeadlineDays' in g) { shapeOk=false; shapeWhy+=g.id+':禁欄 '; }
  if(!libLocs.has(g.loc)) { shapeOk=false; shapeWhy+=g.id+':loc '; }
  if(libTitles.has(g.workTitle)) { shapeOk=false; shapeWhy+=g.id+':撞名 '; }
});
ok('G1 四張共通欄位（year 1988／不限季／臨記／pay 55-65 定額 60／req acting 24／2 日／零年份數字／無 trigger-cast-favorDelta-applyDeadlineDays／loc 存在／戲名零撞）', shapeOk, shapeWhy);
ok('G1 兩邊 roleScale 分流（電視 tv_cameo_short／電影 film_support_small）',
  Q12_FOLLOW_GIGS.find(g=>g.id==='gig_q12_canteen_grind').roleScale==='tv_cameo_short' &&
  Q12_FOLLOW_GIGS.find(g=>g.id==='gig_q12_canteen_quit').roleScale==='tv_cameo_short' &&
  Q12_FOLLOW_GIGS.find(g=>g.id==='gig_q12_studio_follow').roleScale==='film_support_small' &&
  Q12_FOLLOW_GIGS.find(g=>g.id==='gig_q12_studio_roam').roleScale==='film_support_small');
ok('G1 grind／follow 係班底、quit／roam 係街外（boardNote＋loc 分流）',
  Q12_FOLLOW_GIGS.find(g=>g.id==='gig_q12_canteen_grind').loc==='tvb_longmen' &&
  Q12_FOLLOW_GIGS.find(g=>g.id==='gig_q12_canteen_quit').loc==='tvb_kowloon' &&
  Q12_FOLLOW_GIGS.find(g=>g.id==='gig_q12_studio_follow').loc==='film_lion' &&
  Q12_FOLLOW_GIGS.find(g=>g.id==='gig_q12_studio_roam').loc==='film_harbour');

/* ---------- G2：旗未落 → 唔注入＋清殘留 ---------- */
S = freshS(); GIGS = []; toasts = [];
ok('G2 旗未落 merge 回 0', mergeQ12Gigs()===0 && GIGS.length===0);
GIGS = [{ id:'gig_q12_canteen_grind' }];
ok('G2 旗未落清走殘留', mergeQ12Gigs()===0 && !GIGS.some(x=>x.id==='gig_q12_canteen_grind'));

/* ---------- G3：逐支旗只開自己嗰張＋通知一次 ---------- */
const cases = [
  ['flag_canteen_grind', 'gig_q12_canteen_grind', '何生轉告'],
  ['flag_canteen_quit', 'gig_q12_canteen_quit', '情報站'],
  ['flag_studio_follow', 'gig_q12_studio_follow', '何生轉告'],
  ['flag_studio_roam', 'gig_q12_studio_roam', '情報站'],
];
cases.forEach(([flag, gid, mouth])=>{
  S = freshS(); S.flags[flag] = 1; GIGS = []; toasts = [];
  const n1 = mergeQ12Gigs();
  const got = GIGS.filter(x=>x && x.id===gid).length;
  const others = GIGS.filter(x=>x && x.id && x.id.indexOf('gig_q12_')===0 && x.id!==gid).length;
  ok('G3 '+flag+' → 只開 '+gid+'（1 張、無其他、q12FollowGig 標記）',
    n1===1 && got===1 && others===0 && GIGS.find(x=>x.id===gid).q12FollowGig===true);
  ok('G3 '+flag+' 通知一次（'+mouth+'口徑）',
    toasts.length===1 && toasts[0].indexOf(mouth)>=0, JSON.stringify(toasts));
  const n2 = mergeQ12Gigs();
  ok('G3 '+flag+' 第二次 merge 唔重推、唔再通知',
    n2===0 && GIGS.filter(x=>x.id===gid).length===1 && toasts.length===1);
});

/* ---------- G4：做完 → 落板 ---------- */
S = freshS(); S.flags.flag_canteen_grind = 1; GIGS = []; toasts = [];
mergeQ12Gigs();
S.flags['done_gig_q12_canteen_grind'] = 1;
ok('G4 done_ 旗 → 落板', mergeQ12Gigs()===0 && !GIGS.some(x=>x.id==='gig_q12_canteen_grind'));
S = freshS(); S.flags.flag_studio_follow = 1; S.wrapHistory = [{ gigId:'gig_q12_studio_follow' }]; GIGS = []; toasts = [];
ok('G4 wrapHistory 有該 gig → 唔注入', mergeQ12Gigs()===0 && !GIGS.some(x=>x.id==='gig_q12_studio_follow'));

/* ---------- G5：舊檔（旗只在 S.flags）即見 ---------- */
S = freshS(); S.flags.flag_studio_roam = 1; GIGS = []; toasts = [];
ok('G5 舊檔 S.flags 有旗 → 注入', mergeQ12Gigs()===1 && GIGS.some(x=>x.id==='gig_q12_studio_roam'));

/* ---------- S1：靜態——唔郁清單 ---------- */
ok('S1 ECHO89 四句回望文案在位',
  html.indexOf('電視台飯堂那排閒角，你熬得安安穩穩——這樣熬過來，就是你的底子。')>=0 &&
  html.indexOf('電視台飯堂那份閒角，你選擇不接，繼續跑通告搏機會——那種不安分，推著你走到這裡。')>=0 &&
  html.indexOf('大製作那期跟班，你由開鏡跟到殺青——整個廠怎樣運作，你那期學完了。')>=0 &&
  html.indexOf('大製作那個跟班位，你選擇不接，繼續跑通告搏機會——那種不安分，推著你走到這裡。')>=0);
const main = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'content', 'story_detail_n1_to_n17.json'), 'utf8'));
const n5 = main.nodes.find(n=>n.id==='N5');
const n6 = main.nodes.find(n=>n.id==='N6');
const n6f = main.nodes.find(n=>n.id==='N6F');
ok('S1 N5_b 仍落 choi_spin', JSON.stringify(n5.choices.find(c=>c.id==='N5_b').effects.flags)==='["choi_spin"]');
ok('S1 N6_a 仍落 flag_canteen_grind', JSON.stringify(n6.choices.find(c=>c.id==='N6_a').effects.flags)==='["flag_canteen_grind"]');
ok('S1 N6F_a 仍落 flag_studio_follow', JSON.stringify(n6f.choices.find(c=>c.id==='N6F_a').effects.flags)==='["flag_studio_follow"]');
ok('S1 gigs_new.json 仍係 322 張', gigsLib.length===322, 'count='+gigsLib.length);

if(fails.length){ console.log('FAILURES: '+fails.join(', ')); process.exit(1); }
console.log('ALL PASS');
