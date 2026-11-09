// 節奏包（v20a35）邏輯／路徑測試：P0-2(c) 中階通告／P0-2(b) 訓練微事件／
// P1-6 長工輕量抉擇／P0-6 文案池（PSR 增補＋防重複＋報紙 dek 變體）。
// 行真路徑：真 gigsForLocSeasonBoard＋真 mergeMidGigs35＋真 canAudition（內嵌 GIGS 全池）、
// 真 maybeTrainEvent35＋真 apply、真 setChoiceOffer35／applySetChoice35、
// 真 augmentPostShootRewards35／postShootPickTemplate／buildPostShootRewardPack、
// 真 newspaperWrapFaceLines。
// 用法：node tests/test_pacing35_logic.js [path-to-index.html]
const fs = require('fs');
const path = process.argv[2] || require('path').join(__dirname, '..', 'index.html');
const html = fs.readFileSync(path, 'utf8');
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
function extractArrDecl(decl){
  const i = html.indexOf(decl);
  if(i<0) throw new Error('decl not found: '+decl);
  let depth=0, j=html.indexOf('[', i);
  for(; j<html.length; j++){
    if(html[j]==='[') depth++;
    else if(html[j]===']'){ depth--; if(depth===0) return html.slice(i, j+1)+';'; }
  }
  throw new Error('arr end not found: '+decl);
}
function dayIndexOf(y, m, d){ return Math.round((Date.UTC(y, m-1, d) - Date.UTC(1988, 2, 7)) / 86400000); }

/* ================================================================
   段一 (a)：P0-2(c)——第 3 週、演技 ~35 嘅真狀態行真通告板
   中階工可報名（星河）／只差少少（獅子山）；《靈異》仍然係未達目標。
   ================================================================ */
(function(){
  var S = { dayIndex: dayIndexOf(1988,3,21), acting:35, iq:22, stamina:120, looks:22, charm:16,
    stage:14, vocal:14, fame:8, popularity:5, stress:10, money:9000,
    flags:{}, shoots:[], booked:[], board:{}, known:{}, npcs:{ director:4, agent:12, colleague:8 },
    enrolled:{}, mockDebts:[], mockRumors:[] };
  var START = { y:1988, m:3, d:7 };
  var GIGS;
  eval(extractArrDecl('let GIGS = [').replace('let GIGS', 'GIGS'));
  eval(extractConst('STAT_LABEL').replace('const STAT_LABEL', 'var STAT_LABEL'));
  eval(extractConst('COURSE_DEFS').replace('const COURSE_DEFS', 'var COURSE_DEFS'));
  const FNS = ['clamp','fameFloor','reqGap','isGigWrapped','gigActiveShoot','isGigInProduction',
    'isGigConsumed','gateTrainHint','canAudition','boardNotePlayerOk','looksLikeEraId',
    'humanizeEraId','normalizeGigRecord','seasonRank','boardPriorityRank','boardSortCompare',
    'calendarSeason','dateObj','gigGapBits34','gigGapTotal34','mergeMidGigs35','gigsForLocSeasonBoard'];
  for(let i=0;i<FNS.length;i++) eval(extractFn(FNS[i]));
  eval(extractConst('MID_GIGS_1988_35').replace('const MID_GIGS_1988_35', 'var MID_GIGS_1988_35'));

  ok('a0 audit baseline: embedded pool has NO spring gig with acting req 19-44 except tv_01(45)',
    GIGS.filter(g=>g.season==='春' && g.req && g.req.acting>18 && g.req.acting<45).length===0);

  const boardLongmen = gigsForLocSeasonBoard('tvb_longmen', '春');
  const midA = boardLongmen.find(g=>g.id==='gig_1988_mid35_longmen_night');
  ok('a1 mid gig A on longmen spring board', !!midA);
  ok('a2 mid gig A auditionable at acting35/iq22/stamina120', !!midA && canAudition(midA).ok===true);
  ok('a3 mid gig A shoot days = 3', !!midA && (function(){ const b=midA.shootBand; return midA.shootDaysHint===3 && b[0]===3 && b[1]===3; })());
  const tv01 = boardLongmen.find(g=>g.id==='gig_1988_tv_01');
  ok('a4 lingyi still locked at acting35 (goal preserved, no threshold cut)', !!tv01 && canAudition(tv01).ok===false);

  const boardLion = gigsForLocSeasonBoard('film_lion', '春');
  const midB = boardLion.find(g=>g.id==='gig_1988_mid35_lion_chase');
  ok('a5 mid gig B on lion spring board', !!midB);
  ok('a6 mid gig B near-miss: gap total = 3 (acting 35 -> 38)', !!midB && gigGapTotal34(midB)===3);

  S.dayIndex = dayIndexOf(1989,3,21);
  mergeMidGigs35();
  ok('a7 mid gigs removed after calendar year 1989', !GIGS.some(g=>g.id==='gig_1988_mid35_longmen_night') && !GIGS.some(g=>g.id==='gig_1988_mid35_lion_chase'));
  S.dayIndex = dayIndexOf(1988,3,21);
  mergeMidGigs35();
  ok('a8 mid gigs restored back in 1988 (idempotent merge)', GIGS.filter(g=>g.id==='gig_1988_mid35_longmen_night').length===1);
})();

/* ================================================================
   段二 (b)：P0-2(b)——訓練微事件：真 maybeTrainEvent35＋真 apply
   ================================================================ */
(function(){
  var S = { dayIndex: 20, acting:30, iq:20, stage:14, stamina:90, stress:10, popularity:3, fame:5,
    money:5000, flags:{}, npcs:{ colleague:8, director:4 }, mockRumors:[], story:{} };
  var saveQ = ()=>{};
  var paintBar = ()=>{};
  eval(extractConst('STAT_LABEL').replace('const STAT_LABEL', 'var STAT_LABEL'));
  eval(extractConst('STAT_MAX').replace('const STAT_MAX', 'var STAT_MAX'));
  eval(extractConst('STRESS_MAX').replace('const STRESS_MAX', 'var STRESS_MAX'));
  const FNS = ['clamp','statHardMax','apply','bumpNpc','maybeTrainEvent35'];
  for(let i=0;i<FNS.length;i++) eval(extractFn(FNS[i]));
  eval(extractConst('TRAIN_EVENTS_35').replace('const TRAIN_EVENTS_35', 'var TRAIN_EVENTS_35'));
  eval(extractConst('MOCK_RUMOR_SEEDS').replace('const MOCK_RUMOR_SEEDS', 'var MOCK_RUMOR_SEEDS'));

  ok('b0 event pool size = 8', TRAIN_EVENTS_35.length===8);

  // 保底觸發（since>=3）＋同日唔出兩次
  S.flags.trainEvSince35 = 3;
  const notes1 = [];
  const hit1 = maybeTrainEvent35(notes1, 'train_acting');
  ok('b1 forced trigger fires', hit1===true && notes1.length>0);
  ok('b2 same-day second call blocked', maybeTrainEvent35([], 'train_acting')===false);

  // 效果正確：導師示範（index 1）→ acting +1（gate 以 since 保底繞過擲骰；揀事件擲骰釘死）
  S.dayIndex = 21; S.flags.trainEvSince35 = 3; S.flags.trainEvLastId35 = 'train35_demo_x';
  const realRandom = Math.random;
  Math.random = ()=> 0.13; // floor(0.13*8)=1 -> train35_demo
  const beforeActing = S.acting;
  const notes2 = [];
  const hit2 = maybeTrainEvent35(notes2, 'train_acting');
  Math.random = realRandom;
  ok('b3 demo event applies acting +1', hit2===true && S.acting===beforeActing+1);

  // 情報碎片：訓練八卦（index 0）→ 攞到真 catalog 碎片；再觸發同則 → 行 fallback 人氣 +1
  S.dayIndex = 22; S.flags.trainEvSince35 = 3; S.flags.trainEvLastId35 = 'zzz';
  Math.random = ()=> 0.0;
  const hit3 = maybeTrainEvent35([], 'train_iq');
  ok('b4 gossip event grants catalog frag', hit3===true && S.mockRumors.some(r=>r.id==='gao_steal_spotlight'));
  S.dayIndex = 23; S.flags.trainEvSince35 = 3; S.flags.trainEvLastId35 = 'zzz';
  const beforePop = S.popularity;
  const hit4 = maybeTrainEvent35([], 'train_iq');
  Math.random = realRandom;
  ok('b5 gossip repeat -> fallback popularity +1, no duplicate frag',
    hit4===true && S.popularity===beforePop+1 && S.mockRumors.filter(r=>r.id==='gao_steal_spotlight').length===1);

  // 節奏：12 個訓練日（逐日推 dayIndex），事件數介乎保底與每日上限之間
  let evCount = 0;
  for(let d=0; d<12; d++){
    S.dayIndex = 30 + d;
    if(maybeTrainEvent35([], 'train_acting')) evCount++;
  }
  ok('b6 cadence: 12 train days -> 3..12 events (force floor at since>=3)', evCount>=3 && evCount<=12);
})();

/* ================================================================
   段三 (c)：P1-6——長工輕量抉擇：真 setChoiceOffer35／applySetChoice35
   ================================================================ */
(function(){
  var S = { dayIndex: 40, money:1000, stress:20, stamina:80, popularity:3, acting:30, iq:20,
    flags:{}, npcs:{ colleague:10, director:5 }, story:{} };
  var _weekAccel = false;
  var saveQ = ()=>{};
  var paintBar = ()=>{};
  eval(extractConst('STAT_LABEL').replace('const STAT_LABEL', 'var STAT_LABEL'));
  eval(extractConst('STAT_MAX').replace('const STAT_MAX', 'var STAT_MAX'));
  eval(extractConst('STRESS_MAX').replace('const STRESS_MAX', 'var STRESS_MAX'));
  const FNS = ['clamp','statHardMax','apply','bumpNpc','setChoiceOffer35','applySetChoice35'];
  for(let i=0;i<FNS.length;i++) eval(extractFn(FNS[i]));
  eval(extractConst('SET_CHOICES_35').replace('const SET_CHOICES_35', 'var SET_CHOICES_35'));

  ok('c0 choice pool size = 6', SET_CHOICES_35.length===6);
  const realRandom = Math.random;
  Math.random = ()=> 0.5; // 0.5 < 0.6 -> 出抉擇

  const shLong = { id:'sh_t1', gigId:'gig_x', totalDays:9, doneDays:1, title:'《長工》' };
  const htmlOffer = setChoiceOffer35(shLong);
  ok('c1 long shoot (>=4d) offers choice', typeof htmlOffer==='string' && htmlOffer.indexOf('片場小事')>=0 && htmlOffer.indexOf('data-sckey="sh_t1_1"')>=0);
  ok('c2 offer alone changes nothing (safe default)', S.money===1000 && S.stress===20 && S.npcs.colleague===10);
  ok('c3 same shoot-day re-offer blocked', setChoiceOffer35(shLong)==='');

  // 輪轉第一則 = set35_supper，選項 0：money -60／stress -6／colleague +2
  const r = applySetChoice35('sh_t1_1', 0);
  ok('c4 apply choice returns result', !!r && r.eventId==='set35_supper' && r.result.length>0);
  ok('c5 deltas applied exactly', S.money===940 && S.stress===14 && S.npcs.colleague===12);
  ok('c6 double apply blocked (no double settle)', applySetChoice35('sh_t1_1', 0)===null && S.money===940);

  // 間距：翌日（差 1 日）唔出；隔日（差 2 日）出
  S.dayIndex = 41;
  const shNext = { id:'sh_t1', gigId:'gig_x', totalDays:9, doneDays:2, title:'《長工》' };
  ok('c7 next-day spacing blocks offer', setChoiceOffer35(shNext)==='');
  S.dayIndex = 42;
  ok('c8 day-after-next offers again', setChoiceOffer35(shNext).indexOf('片場小事')>=0);

  // 短工唔出
  S.dayIndex = 50; S.flags.setEvLastDay35 = 0;
  const shShort = { id:'sh_t2', gigId:'gig_y', totalDays:3, doneDays:1, title:'《短工》' };
  ok('c9 short shoot (<4d) never offers', setChoiceOffer35(shShort)==='');
  Math.random = realRandom;
})();

/* ================================================================
   段四 (d)：P0-6——PSR 文案池增補＋防重複＋真 buildPostShootRewardPack
   pack 模擬線上 STUB_POST_SHOOT_REWARDS_v1.json 嘅真實形狀（press 5／news 4／fans 3／metrics 5）
   ================================================================ */
(function(){
  var S = { dayIndex: 30, fame: 10, postShootRewards: [] };
  var FREEPLAY_FW = { postShootSchema: null, postShootRewards: {
    templates: {
      press: [
        { id:'press_film_01', matchTypes:['電影'], paperName:'娛樂版', headline:'新人臨記殺青，版面留低一格', dek:'x' },
        { id:'press_tv_01', matchTypes:['電視劇','綜藝'], paperName:'娛樂版', headline:'廠景殺青，娛樂版順手記一筆', dek:'x' },
        { id:'press_rec_01', matchTypes:['唱片通告'], paperName:'樂版', headline:'錄音室散場，樂版一句帶過', dek:'x' },
        { id:'press_ad_01', matchTypes:['廣告'], paperName:'廣告版', headline:'廣告殺青，報紙夾頁有你一眼', dek:'x' },
        { id:'press_any_01', matchTypes:[], paperName:'娛樂版', headline:'通告殺青，娛樂版留低一行', dek:'x' }
      ],
      news: [
        { id:'news_film_01', matchTypes:['電影'], outlet:'娛樂快訊', line:'電影組殺青消息：有新人臨記入鏡完成。' },
        { id:'news_tv_01', matchTypes:['電視劇','綜藝'], outlet:'娛樂快訊', line:'電視台組製收工，臨記檔期順利殺青。' },
        { id:'news_rec_01', matchTypes:['唱片通告'], outlet:'娛樂快訊', line:'錄音室散場，唱片通告順利完成。' },
        { id:'news_any_01', matchTypes:[], outlet:'娛樂快訊', line:'通告殺青：新人又過一關。' }
      ],
      streetFans: [
        { id:'fans_01', matchTypes:[], place:'街上', line:'轉角突然幾個人圍住問。', stageVolumeDelta:0 },
        { id:'fans_02', matchTypes:['電影','電視劇'], place:'街上', line:'有人遞紙筆過嚟。', stageVolumeDelta:0 },
        { id:'fans_03', matchTypes:['唱片通告','廣告'], place:'街口', line:'等燈時有人拍你膊頭。', stageVolumeDelta:0 }
      ],
      metrics: [
        { id:'metric_box_01', matchTypes:['電影'], metricKind:'boxOffice', valueLine:'首輪口碑：街坊開始問檔期', blurb:'x' },
        { id:'metric_rate_01', matchTypes:['電視劇','綜藝'], metricKind:'ratings', valueLine:'同檔時段：有觀眾問邊個臨記', blurb:'x' },
        { id:'metric_sales_01', matchTypes:['唱片通告'], metricKind:'sales', valueLine:'舖頭返貨：有人問封面邊個', blurb:'x' },
        { id:'metric_att_01', matchTypes:['廣告'], metricKind:'attention', valueLine:'品牌回訪：造型照有人截圖', blurb:'x' },
        { id:'metric_any_01', matchTypes:[], metricKind:'attention', valueLine:'本單完成後關注度微升', blurb:'x' }
      ]
    },
    fallbacks: { press:{ paperName:'娛樂版', headline:'通告殺青', dek:'又完成一單拍攝。' },
      news:{ outlet:'娛樂快訊', line:'殺青完成。' },
      streetFans:{ place:'街上', line:'有人多望你兩眼。', stageVolumeDelta:0 },
      metrics:{ label:'關注度', valueLine:'關注度＋', blurb:'履歷又多一筆。' } },
    metricKindLabels: { boxOffice:'票房關注', ratings:'收視關注', sales:'銷量關注', attention:'關注度' }
  } };
  eval(extractConst('PSR_EXTRA_TEMPLATES_35').replace('const PSR_EXTRA_TEMPLATES_35', 'var PSR_EXTRA_TEMPLATES_35'));
  eval(extractConst('_psrLastPick35').replace('const _psrLastPick35', 'var _psrLastPick35'));
  const FNS = ['psrPickNoRepeat35','augmentPostShootRewards35','postShootPickTemplate',
    'postShootCopyLine','postShootDisplayTitle','postShootMetricKindForType','buildPostShootRewardPack'];
  for(let i=0;i<FNS.length;i++) eval(extractFn(FNS[i]));

  const added = augmentPostShootRewards35();
  const T = FREEPLAY_FW.postShootRewards.templates;
  ok('d1 augment adds 23 templates', added===23);
  ok('d2 pool sizes: press 5->12 / news 4->11 / fans 3->8 / metrics 5->9',
    T.press.length===12 && T.news.length===11 && T.streetFans.length===8 && T.metrics.length===9);
  ok('d3 augment idempotent', augmentPostShootRewards35()===0 && T.press.length===12);

  // 防重複：連抽 20 次 press（電視劇），唔會連續兩次同 id，而且唔止一款
  let prev = '', distinct = new Set(), noRepeat = true;
  for(let i=0;i<20;i++){
    const t = postShootPickTemplate('press', '電視劇');
    if(t.id===prev) noRepeat = false;
    prev = t.id; distinct.add(t.id);
  }
  ok('d4 press picks never repeat consecutively + vary', noRepeat && distinct.size>=3);

  // 真組裝：多次殺青反響，press 標題同 fans 標題都要有變化
  const pressHeads = new Set(), fansTitles = new Set();
  for(let i=0;i<40;i++){
    const pack = buildPostShootRewardPack({ gigId:'g35_'+i, type:'電視劇', workTitle:'試作劇', title:'《試作劇》街坊' });
    (pack.cards||[]).forEach(c=>{
      if(c.channel==='press') pressHeads.add(c.title);
      if(c.channel==='streetFans') fansTitles.add(c.title);
    });
  }
  ok('d5 wrap packs vary press headlines', pressHeads.size>=3);
  ok('d6 fans card titles vary (not always 被 fans 包圍)', fansTitles.size>=2);
})();

/* ================================================================
   段五 (e)：P0-6——報紙 dek 變體：真 newspaperWrapFaceLines
   定版（同作品同講法）＋跨作品有變化＋關鍵字不變量保留
   ================================================================ */
(function(){
  var S = { fame: 20 };
  eval(extractConst('PAPER_NAME_TIER_NAMED').replace('const PAPER_NAME_TIER_NAMED', 'var PAPER_NAME_TIER_NAMED'));
  eval(extractConst('PAPER_NAME_TIER_TITLED').replace('const PAPER_NAME_TIER_TITLED', 'var PAPER_NAME_TIER_TITLED'));
  const FNS = ['newspaperNameTier','newspaperPlayerRef','newspaperMediumFromGigType','newspaperWrapFaceLines'];
  for(let i=0;i<FNS.length;i++) eval(extractFn(FNS[i]));

  const tvRole = { gigId:'e1', work:'師奶劇場', role:'鄰居', type:'電視劇' };
  const d1 = newspaperWrapFaceLines(tvRole, 'steady');
  const d2 = newspaperWrapFaceLines(tvRole, 'steady');
  ok('e1 same work+role -> deterministic dek', d1.dek===d2.dek);
  ok('e2 tv steady role keeps 走位穩妥 (師奶劇場 seed)', d1.dek.indexOf('走位穩妥')>=0);
  ok('e3 tv spotlight role keeps 俾人記住', newspaperWrapFaceLines(tvRole, 'spotlight').dek.indexOf('俾人記住')>=0);

  const filmRole = { gigId:'e2', work:'街景臨記', role:'路人', type:'電影' };
  ok('e4 film steady role keeps 不搶戲', newspaperWrapFaceLines(filmRole, 'steady').dek.indexOf('不搶戲')>=0);
  ok('e5 film spotlight role keeps 搶眼', newspaperWrapFaceLines(filmRole, 'spotlight').dek.indexOf('搶眼')>=0);
  const musicSpot = { gigId:'e3', work:'金曲夜', role:'和音', type:'唱片通告' };
  ok('e6 music spotlight keeps 點名', newspaperWrapFaceLines(musicSpot, 'spotlight').dek.indexOf('點名')>=0);

  S.fame = 5;
  const anonTv = newspaperWrapFaceLines({ gigId:'e4', work:'師奶劇場', role:'', type:'電視劇' }, 'steady');
  ok('e7 anon tv no-role: no 名字見諸內頁, has 一名臨記', anonTv.dek.indexOf('名字見諸內頁')<0 && anonTv.dek.indexOf('一名臨記')>=0);
  S.fame = 20;

  // 跨作品變化：10 個唔同作品（電視劇・有角色・穩陣）→ 至少 2 種尾句
  const tails = new Set();
  ['海角情緣','霓虹夜話','大廈保安','茶餐廳風雲','巴士奇緣','武館春秋','夜校疑雲','碼頭歲月','戲班春秋','摩登保鑣']
    .forEach(w=>{ tails.add(newspaperWrapFaceLines({ gigId:'ex', work:w, role:'鄰居', type:'電視劇' }, 'steady').dek); });
  ok('e8 dek varies across works (>=2 distinct)', tails.size>=2);
})();

console.log(fails.length ? ('\nFAILED: '+fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length?1:0);
