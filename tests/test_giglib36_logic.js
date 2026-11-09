// 通告庫修補包（v20a36）邏輯／路徑測試：F1 死卡正規化／F2–F7 補庫注入／
// 逐季活工數／階梯段／信用・標籤閘／跨年唔洩漏。
// 行真路徑：真 normalizeGigRecord（年包 fixture 逐張行）、真 gigsForLocSeasonBoard、
// 真 mergeYearGigs36／mergeExodusGigs／mergeSoftBridgeGigs、真 canAudition＋真閘函數。
// 年包 fixture＝repo content/gigs_1989|1990|1991.json 嘅原檔副本（tests/fixtures/）。
// 用法：node tests/test_giglib36_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
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
function dayIndexOf(y, m, d){ return Math.round((Date.UTC(y, m-1, d) - Date.UTC(1988, 2, 7)) / 86400000); }
function loadPack(y){
  return JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'gigs_'+y+'.json'), 'utf8'));
}
const LOCS11 = ["tvb_longmen","tvb_kowloon","tvb_harbour","film_lion","film_cotton","film_harbour","ad_central","ad_adm","rec_hk","rec_wanchai","rec_star"];

/* 真碼片段：每個 section 自己 eval 入作用域（跟節奏包測試同一套路） */
const WORLD_CONSTS = ['STAT_LABEL','COURSE_DEFS','CHOICE47_SEASON_IDX','MID_GIGS_1988_35','SOFT_BRIDGE_GIGS_1988','EXODUS_GIGS',
  'GIGS36_1989_SPRING_F5','GIGS36_1989_BRIDGE','GIGS36_1989_HIGH_F2','GIGS36_1989_MID_F3',
  'GIGS36_1990_HIGH_F2','GIGS36_1990_MID_F3','GIGS36_1990_BRIDGE','GIGS36_1990_AUTUMN_F6','GIGS36_1990_FINALE_F7',
  'GIGS36_BY_YEAR'];
const WORLD_FNS = ['clamp','fameFloor','reqGap','isGigWrapped','gigActiveShoot','isGigInProduction','isGigConsumed',
  'gateTrainHint','canAudition','boardNotePlayerOk','looksLikeEraId','humanizeEraId','normalizeGigRecord',
  'seasonRank','boardPriorityRank','boardSortCompare','calendarSeason','dateObj','yearSeasonNow','choice47SeasonReached',
  'gigGapBits34','gigGapTotal34','mergeMidGigs35','softBridgeGig','mergeSoftBridgeGigs','mergeExodusGigs',
  'dualTrackNumbers','readDualTracks','ensureCastingTagsState','castingTagRegistry','castingTagLabelToId','castingTagMeta',
  'softCastingTagGate','softIndustryCreditGate','softOverdueFavorDebtLock','gateShortReason','reqHtml',
  'gig36','mergeYearGigs36','gigsForLocSeasonBoard'];
const WORLD_SRC = WORLD_CONSTS.map(c=>extractConst(c).replace('const '+c, 'var '+c)).join('\n')
  + '\n' + WORLD_FNS.map(f=>extractFn(f)).join('\n')
  + '\nvar GIGS36_ALL_IDS = {}; Object.keys(GIGS36_BY_YEAR).forEach(function(y){ (GIGS36_BY_YEAR[y]||[]).forEach(function(g){ if(g && g.id) GIGS36_ALL_IDS[g.id]=Number(y); }); });';
const STUBS_SRC = `
  var BehaviorGate = { featureFlag_softBehaviorGatePreview: function(){ return true; } };
  var softPreviewOn = function(){ return true; };
  var FREEPLAY_FW = { castingTagsReg: {
    tags: [ {id:"tag_comedy", label:"喜劇細胞"}, {id:"tag_action", label:"動作演員"} ],
    labelToId: { "喜劇細胞":"tag_comedy", "動作演員":"tag_action" } } };
`;
function baseState(dayIndex, stats){
  return Object.assign({ dayIndex: dayIndex, acting:30, iq:20, stamina:120, looks:26, charm:22,
    stage:25, vocal:20, fame:10, popularity:5, stress:0, money:20000, industryCreditDelta:0,
    flags:{}, shoots:[], booked:[], board:{}, known:{}, npcs:{director:0,agent:0,colleague:0},
    enrolled:{}, mockDebts:[], mockRumors:[], castingTags:[] }, stats||{});
}

/* ================================================================
   段一 (a)：F1——年包逐張行真 normalize，死卡回血＋可達性
   ================================================================ */
(function(){
  eval(WORLD_SRC); eval(STUBS_SRC);
  var START = { y:1988, m:3, d:7 };
  var S = baseState(dayIndexOf(1989,4,15), {});
  var GIGS = [];
  const DEAD = {
    1989: ["gig_1989_mtv_01","gig_1989_rec_09","gig_1989_rec_10","gig_1989_rec_11","gig_1989_rec_12","gig_1989_rec_13","gig_1989_rec_14"],
    1990: ["gig_1990_mtv_01","gig_1990_rec_06","gig_1990_rec_07","gig_1990_rec_08","gig_1990_rec_09","gig_1990_rec_10","gig_1990_rec_11"],
    1991: ["gig_1991_mtv_01","gig_1991_rec_09","gig_1991_rec_10","gig_1991_rec_11","gig_1991_rec_12","gig_1991_rec_13"]
  };
  for(const y of [1989, 1990, 1991]){
    const pack = loadPack(y);
    const gigs = pack.gigs.map(normalizeGigRecord);
    ok('a-'+y+' no req keeps sing/dance after normalize',
      gigs.every(g=>!g.req || (g.req.sing==null && g.req.dance==null)));
    for(const id of DEAD[y]){
      const g = gigs.find(x=>x.id===id);
      ok('a-'+y+' dead card '+id+' remapped (value kept)', !!g && (g.req.vocal===18 || g.req.stage===16));
    }
    const rawSing = pack.gigs.find(g=>g.req && g.req.sing!=null);
    ok('a-'+y+' threshold value unchanged (sing->vocal)', !!rawSing && normalizeGigRecord(rawSing).req.vocal===rawSing.req.sing);
    const once = normalizeGigRecord(rawSing), twice = normalizeGigRecord(once);
    ok('a-'+y+' normalize idempotent', JSON.stringify(once.req)===JSON.stringify(twice.req));
  }
  /* 可達性：真 board＋真 canAudition */
  GIGS = loadPack(1989).gigs.map(normalizeGigRecord);
  S.vocal = 25; S.stage = 25; S.looks = 30; S.charm = 25; S.stamina = 80;
  const boardRecHk = gigsForLocSeasonBoard('rec_hk', '春');
  const rec09 = boardRecHk.find(g=>g.id==='gig_1989_rec_09');
  ok('a-rec09 on board + auditionable at vocal25', !!rec09 && canAudition(rec09).ok===true);
  S.vocal = 0;
  ok('a-rec09 still locked at vocal0 (real threshold)', !!rec09 && canAudition(rec09).ok===false);
  S.vocal = 25; S.stage = 0;
  const boardRecStar = gigsForLocSeasonBoard('rec_star', '春');
  const mtv = boardRecStar.find(g=>g.id==='gig_1989_mtv_01');
  ok('a-mtv01 locked at stage0', !!mtv && canAudition(mtv).ok===false);
  S.stage = 25;
  ok('a-mtv01 auditionable at stage25', !!mtv && canAudition(mtv).ok===true);
})();

/* ================================================================
   段二 (b)：逐季活工數（真 board 全地點聯集）＋(f) 跨年唔洩漏
   ================================================================ */
function seasonBoardCount(year, season, month, stats){
  eval(WORLD_SRC); eval(STUBS_SRC);
  var START = { y:1988, m:3, d:7 };
  var S = baseState(dayIndexOf(year, month, 15), stats);
  var GIGS = loadPack(year).gigs.map(normalizeGigRecord);
  const seen = {};
  LOCS11.forEach(loc=>{ gigsForLocSeasonBoard(loc, season).forEach(g=>{ seen[g.id]=g; }); });
  return { count: Object.keys(seen).length, gigs: seen, pool: GIGS };
}
(function(){
  const STATS = {
    1989: { acting:50, iq:28, looks:28, charm:26, stage:30, vocal:22, fame:25 },
    1990: { acting:80, iq:32, looks:32, charm:32, stage:45, vocal:30, fame:50 }
  };
  const SEASONS = [ ['春',4], ['夏',7], ['秋',10], ['冬',12] ];
  for(const year of [1989, 1990]){
    for(const [season, month] of SEASONS){
      const r = seasonBoardCount(year, season, month, STATS[year]);
      console.log('  [count] '+year+' '+season+' live board gigs = '+r.count);
      ok('b-'+year+season+' live gigs >= 20 (was 10-14)', r.count>=20);
      ok('b-'+year+season+' live gigs <= 32 (density sane)', r.count<=32);
      const other = (year===1989) ? 'g36_90_' : 'g36_89_';
      ok('f-'+year+season+' no cross-year gig36 leak', !Object.keys(r.gigs).some(id=>id.indexOf(other)===0));
      ok('f-'+year+season+' pool has no cross-year gig36', !r.pool.some(g=>g.id && g.id.indexOf(other)===0));
    }
  }
  const spr89 = seasonBoardCount(1989, '春', 4, STATS[1989]);
  ok('b-1989春 no longer 10 live (F5承接)', spr89.count>=20);
  const f5 = Object.keys(spr89.gigs).filter(id=>id.indexOf('g36_89_spr_')===0 || id.indexOf('g36_89_brg_spr_')===0);
  ok('b-1989春 F5+bridge spring gigs on board (>=10)', f5.length>=10);
})();

/* ================================================================
   段三 (c)：階梯段＋(d) 信用／標籤閘＋(e) 1990 冬壓軸／exodus
   ================================================================ */
(function(){
  eval(WORLD_SRC); eval(STUBS_SRC);
  var START = { y:1988, m:3, d:7 };
  var S = baseState(dayIndexOf(1989,7,15), {});
  var GIGS = [];
  const pool89 = GIGS36_BY_YEAR[1989], pool90 = GIGS36_BY_YEAR[1990];
  ok('c-1989 additions = 31', pool89.length===31);
  ok('c-1990 additions = 28 (+3 exodus = 31)', pool90.length===28);
  const band = (pool, lo, hi)=> pool.some(g=>g.req && g.req.acting>=lo && g.req.acting<=hi);
  ok('c-1989 has acting 45-55 band', band(pool89, 45, 55));
  ok('c-1989 has acting 60-75 band', band(pool89, 60, 75));
  ok('c-1990 has acting 60-75 band', band(pool90, 60, 75));
  ok('c-1990 has acting 80-95 band', band(pool90, 80, 95));
  ok('c-1990 has acting 100+ band', pool90.some(g=>g.req && g.req.acting>=100));
  const REALKEYS = { acting:1, stage:1, vocal:1, looks:1, stamina:1, iq:1, charm:1 };
  ok('c-all new gigs use real req keys only',
    pool89.concat(pool90).every(g=>Object.keys(g.req||{}).every(k=>REALKEYS[k])));
  const gated89 = pool89.filter(g=>(g.industryCreditMin>0) || (Array.isArray(g.requiresCastingTagAny) && g.requiresCastingTagAny.length));
  const gated90 = pool90.filter(g=>(g.industryCreditMin>0) || (Array.isArray(g.requiresCastingTagAny) && g.requiresCastingTagAny.length));
  ok('c-1989 gated gigs (credit/tag) = 3', gated89.length===3);
  ok('c-1990 gated gigs incl F7 = 3', gated90.length===3);

  /* (d) 信用閘：未達鎖＋鎖因顯示；達閘開 */
  const creditGig = pool89.find(g=>g.id==='g36_89_sum_longmen_credit');
  S = baseState(dayIndexOf(1989,7,15), { acting:50, stage:20, fame:20 }); /* credit = 10+6+10 = 26 < 30 */
  ok('d-credit gate locks below min', canAudition(creditGig).ok===false);
  ok('d-credit lock reason shown', gateShortReason(creditGig).indexOf('業內信用')>=0);
  ok('d-credit req line shown', reqHtml(creditGig).indexOf('業內信用：需要 30')>=0);
  S = baseState(dayIndexOf(1989,7,15), { acting:55, stage:30, fame:30 }); /* credit = 15+9+11 = 35 >= 30 */
  ok('d-credit gate opens at min', canAudition(creditGig).ok===true);

  /* (d) 標籤閘：冇標籤鎖＋鎖因；有標籤開 */
  const tagGig = pool89.find(g=>g.id==='g36_89_aut_cotton_comedy');
  S = baseState(dayIndexOf(1989,10,15), { acting:60, stage:35, fame:20 });
  ok('d-tag gate locks without tag', canAudition(tagGig).ok===false);
  ok('d-tag lock reason shown', gateShortReason(tagGig).indexOf('口碑')>=0);
  S.castingTags = [ { id:'tag_comedy', label:'喜劇細胞' } ];
  ok('d-tag gate opens with tag', canAudition(tagGig).ok===true);

  /* (e) exodus 5 張真注入 + 1990 冬壓軸上板 */
  ok('e-EXODUS_GIGS total = 5', EXODUS_GIGS.length===5);
  S = baseState(dayIndexOf(1990,10,15), { acting:80, fame:50 });
  GIGS = loadPack(1990).gigs.map(normalizeGigRecord);
  gigsForLocSeasonBoard('rec_hk', '秋');
  const exoIds = ['gig_exodus_tv_senior','gig_exodus_film_hand','gig_exodus_rec_producer','gig_exodus_tv_kowloon','gig_exodus_ad_manager'];
  ok('e-all 5 exodus gigs injected in 1990 autumn', exoIds.every(id=>GIGS.some(g=>g.id===id)));
  S = baseState(dayIndexOf(1989,10,15), { acting:50, fame:25 });
  GIGS = loadPack(1989).gigs.map(normalizeGigRecord);
  gigsForLocSeasonBoard('rec_hk', '秋');
  ok('e-no exodus gigs in 1989', !exoIds.some(id=>GIGS.some(g=>g.id===id)));
  S = baseState(dayIndexOf(1990,12,15), { acting:90, stage:40, fame:55, iq:32 });
  GIGS = loadPack(1990).gigs.map(normalizeGigRecord);
  const lionWinter = gigsForLocSeasonBoard('film_lion', '冬');
  ok('e-1990冬 film_lion has newyear finale gig', lionWinter.some(g=>g.id==='g36_90_win_lion_newyear'));
  const fin = lionWinter.find(g=>g.id==='g36_90_win_lion_newyear');
  ok('e-finale is high tier, 12 days', !!fin && fin.tier==='高' && fin.shootBand[0]===12);
})();

/* ================================================================
   段四 (g)：內容標準——香港味／主幹呼應／冇通用工名
   ================================================================ */
(function(){
  eval(WORLD_SRC); eval(STUBS_SRC);
  const HK_KEYS = ['清水灣','廟街','啟德','重慶大廈','沙田','城門河','旺角','灣仔','銅鑼灣','尖沙咀','中環','金鐘','紅磡','西環','渡輪','卡拉OK','賀歲','選美','台慶','武打','江湖','梟雄','酒廊','冰室','大排檔','錄音室','頒獎禮','收視','樂壇','星河','九龍','廠景','百貨','的士','麻將','戲院','商場','碼頭','天橋','武館','追數','清貨','拜年','金飾','汽水','手錶','霓虹'];
  const BANNED = ['電影配角','電視配角','廣告拍攝','電影拍攝','配角招募','演員招募','臨時演員招募','群眾演員'];
  const all = GIGS36_BY_YEAR[1989].concat(GIGS36_BY_YEAR[1990]);
  ok('g-every new gig title carries a work title 《》or「」',
    all.every(g=>/《|「/.test(g.title)));
  ok('g-no banned generic titles', all.every(g=>!BANNED.some(b=>g.title.indexOf(b)>=0)));
  const noFlavor = all.filter(g=>{
    const text = (g.title||'')+(g.blurb||'')+(g.synopsis||'');
    return !HK_KEYS.some(k=>text.indexOf(k)>=0);
  });
  if(noFlavor.length) console.log('  [flavor-miss]', noFlavor.map(g=>g.id).join(', '));
  ok('g-every new gig has HK flavor keyword', noFlavor.length===0);
  /* 主幹呼應抽查：1989 夏有暴雨/救場語境、秋有選美/笑匠、冬有酒廊/追數；1990 春有武打/替身、夏有收視/挖角、秋有樂壇、冬有賀歲 */
  const txt = (pool, season)=> pool.filter(g=>g.season===season).map(g=>(g.title||'')+(g.synopsis||'')).join('');
  ok('g-1989夏 echoes N7 rain/rescue troupe', /暴雨|救場|班底/.test(txt(GIGS36_BY_YEAR[1989],'夏')));
  ok('g-1989秋 echoes N8/N9 pageant+comedy', /選美/.test(txt(GIGS36_BY_YEAR[1989],'秋')) && /笑匠|喜劇/.test(txt(GIGS36_BY_YEAR[1989],'秋')));
  ok('g-1989冬 echoes N10/N11 lounge+debt', /酒廊/.test(txt(GIGS36_BY_YEAR[1989],'冬')) && /追數|清貨|梟雄/.test(txt(GIGS36_BY_YEAR[1989],'冬')));
  ok('g-1990春 echoes N12 martial/stunt', /武打|替身/.test(txt(GIGS36_BY_YEAR[1990],'春')));
  ok('g-1990夏 echoes N13 ratings/poach', /收視/.test(txt(GIGS36_BY_YEAR[1990],'夏')) && /挖角|陣營/.test(txt(GIGS36_BY_YEAR[1990],'夏')));
  ok('g-1990秋 echoes N14 music scene', /樂壇|一哥|唱片/.test(txt(GIGS36_BY_YEAR[1990],'秋')));
  ok('g-1990冬 echoes N16 newyear film', /賀歲/.test(txt(GIGS36_BY_YEAR[1990],'冬')));
})();

console.log(fails.length ? ('\nFAILURES: '+fails.length+' -> '+fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
