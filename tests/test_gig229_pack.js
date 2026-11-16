// v20a229 B3 換庫：新庫做唯一來源・pack 測試
// 合約（AUDIT229 §1／§2／§8；SPEC §2／§3；DECISIONS D-1～D-15）：
//   P0 新庫 251 張、id 唯一、全部新格式 gig_1990|1991|1992_<媒介>_<三位數字>、年份只係 1990–1992
//   P1 五級分布 臨記 76／初級 73／中級 51／高級 17／稀有 23
//   P2 category 作品 142／臨記通告 103／補拍通告 6
//   P3 1990 年高級（高級／稀有）0 張
//   P4 年份唔 double-shift：normalize 前後＋兩次 normalize，年份全部唔郁（真 normalizeGigRecord）
//   P5 開局 1990 板面有臨記／初級通告：entryGigPool229 返 12 張臨記、全部合開局數值、冬季有貨
//   P6 每地點有通告：11 個板面地點全部有 gig；每張 gig 嘅 loc 全部喺呢 11 個入面
//   P7 觸發通告 47 張（credit 22／award 9／fame 8／story 4／rel 3／rival 1）
//   P8 主演：152 張有 leadStarId（全部係已知星 id）、142 張作品全部有 posterBrief（129 係唯一例外：leadStarId 未定，見 V250_B_REPORT §5.1）
//   P9 舊表已刪：LEADSTAR59／TIER110／REQ110／NAME93_FIX／CLEAN100_GIG_RELEASE／
//       POSTER59_DATA／POSTER85_IDS／ENTRY_GIGS_1988／gigsByYearNew 全部唔喺 index.html
//       （BR89_PATRON_OF_GIG 映射表本身留返，B5 先擴充——呢度唔斷言佢）
//   P10 舊 pack 已刪：content/gigs_1988–1992.json 唔存在；loader 唔再 fetch 舊 pack
//   P11 單一來源：syncGigsForCalendarYear 只讀 gigsByYear（pick(y) || pick(y-1) || pick(1990)）
//   P12 F1 死卡正規化留返：normalize 將 req sing→vocal、dance→stage（giglib36 退役後嘅覆蓋）
// 反證：對 B2 index 行 → P9 舊表在位 FAIL、P10 舊 pack 在位 FAIL、P11 雙來源 FAIL。
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
let fails = 0;
function ok(name, cond, extra){
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : ''));
  if(!cond) fails++;
}
function deepClone(o){ return JSON.parse(JSON.stringify(o)); }
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) return null;
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){ if(html[j]==='{') depth++; else if(html[j]==='}'){ depth--; if(depth===0) break; } }
  return html.slice(i, j+1);
}
function extractConst(name){
  for(const kw of ['const ', 'var ']){
    const i = html.indexOf(kw+name+' =');
    if(i<0) continue;
    let depth=0, started=false;
    for(let k=i; k<html.length; k++){
      const ch = html[k];
      if(ch==='{'||ch==='['){ depth++; started = true; }
      else if(ch==='}'||ch===']'){ depth--; if(started && depth===0) return html.slice(i, k+1)+';'; }
      else if(ch===';' && !started) return html.slice(i, k+1);
    }
  }
  return null;
}

/* ---------- P0–P3／P6–P8：pack 靜態 ---------- */
const pack = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gigs_new.json'), 'utf8'));
const gigs = pack.gigs || [];
ok('P0 251 張、id 唯一', gigs.length === 251 && new Set(gigs.map(g=>g.id)).size === 251, 'n=' + gigs.length);
const ID_RE = /^gig_(1990|1991|1992)_[a-z]+_\d{3}$/;
const badId = gigs.filter(g=>!ID_RE.test(g.id || ''));
ok('P0 全部 id 係新格式', badId.length === 0, badId.slice(0, 3).map(g=>g.id).join(','));
const badYear = gigs.filter(g=>[1990, 1991, 1992].indexOf(g.year) < 0);
ok('P0 年份只係 1990–1992', badYear.length === 0, badYear.slice(0, 3).map(g=>g.id + ':' + g.year).join(','));
const tierCount = {};
gigs.forEach(g=>{ tierCount[g.tier] = (tierCount[g.tier] || 0) + 1; });
ok('P1 五級分布 76／84／51／17／23',
   tierCount['臨記'] === 76 && tierCount['初級'] === 84 && tierCount['中級'] === 51 &&
   tierCount['高級'] === 17 && tierCount['稀有'] === 23,
   JSON.stringify(tierCount));
const catCount = {};
gigs.forEach(g=>{ catCount[g.category] = (catCount[g.category] || 0) + 1; });
ok('P2 category 作品 142／臨記通告 103／補拍通告 6',
   catCount['作品'] === 142 && catCount['臨記通告'] === 103 && catCount['補拍通告'] === 6,
   JSON.stringify(catCount));
const high1990 = gigs.filter(g=>g.year === 1990 && (g.tier === '高級' || g.tier === '稀有'));
ok('P3 1990 年高級 0 張', high1990.length === 0, high1990.slice(0, 3).map(g=>g.id).join(','));
const yearCount = {};
gigs.forEach(g=>{ yearCount[g.year] = (yearCount[g.year] || 0) + 1; });
ok('P0 每年張數 1990／1991／1992 = 104／80／67',
   yearCount[1990] === 104 && yearCount[1991] === 80 && yearCount[1992] === 67,
   JSON.stringify(yearCount));
const LOCS_11 = ['ad_adm', 'ad_central', 'film_cotton', 'film_harbour', 'film_lion',
  'rec_hk', 'rec_star', 'rec_wanchai', 'tvb_harbour', 'tvb_kowloon', 'tvb_longmen'];
const locCount = {};
gigs.forEach(g=>{ locCount[g.loc] = (locCount[g.loc] || 0) + 1; });
ok('P6 11 個板面地點全部有通告', LOCS_11.every(l=>(locCount[l] || 0) > 0),
   LOCS_11.map(l=>l + ':' + (locCount[l] || 0)).join(' '));
const badLoc = gigs.filter(g=>LOCS_11.indexOf(g.loc) < 0);
ok('P6 每張 gig 嘅 loc 全部喺 11 個板面地點入面', badLoc.length === 0,
   badLoc.slice(0, 3).map(g=>g.id + ':' + g.loc).join(','));
const trig = gigs.filter(g=>g.trigger && g.trigger.kind);
const trigKind = {};
trig.forEach(g=>{ trigKind[g.trigger.kind] = (trigKind[g.trigger.kind] || 0) + 1; });
ok('P7 觸發通告 47 張（credit 22／award 9／fame 8／story 4／rel 3／rival 1）',
   trig.length === 47 && trigKind.credit === 22 && trigKind.award === 9 && trigKind.fame === 8 &&
   trigKind.story === 4 && trigKind.rel === 3 && trigKind.rival === 1,
   'n=' + trig.length + ' ' + JSON.stringify(trigKind));
const withStar = gigs.filter(g=>g.leadStarId);
ok('P8 153 張有 leadStarId', withStar.length === 153, 'n=' + withStar.length);
const POSTER59_STAR_IDS = (()=>{ const s = extractConst('POSTER59_STAR_IDS') || ''; const o = {}; const m = s.match(/"([^"]+)":\s*"([^"]+)"/g) || []; m.forEach(kv=>{ const mm = kv.match(/"([^"]+)":\s*"([^"]+)"/); if(mm) o[mm[1]] = mm[2]; }); return o; })();
const knownStars = new Set(Object.values(POSTER59_STAR_IDS).filter(Boolean).concat(['ching_tinlok', 'pang_siuki']));
const badStar = withStar.filter(g=>!knownStars.has(g.leadStarId));
ok('P8 全部 leadStarId 係已知星 id', badStar.length === 0,
   badStar.slice(0, 3).map(g=>g.id + ':' + g.leadStarId).join(','));
const works = gigs.filter(g=>g.category === '作品');
const noBrief = works.filter(g=>!g.posterBrief);
ok('P8 142 張作品全部有 posterBrief', noBrief.length === 0,
   noBrief.slice(0, 3).map(g=>g.id).join(','));

/* ---------- sandbox：真 normalizeGigRecord＋entryGigPool229 ---------- */
const tfA = html.indexOf('/* ==== v20a55 TEXTFIX');
const tfB = html.indexOf('async function refreshCopyPacksFromDisk(){');
if(tfA<0 || tfB<=tfA){ console.log('FAIL TEXTFIX55 block not found'); process.exit(1); }
const TF_SRC = html.slice(tfA, tfB);
const CONSTS = ['STAT_LABEL', 'POSTER59_STAR_IDS', 'GIG_REQ_KEYS88', 'SHOOT_DAYS',
  'ROLE_SCALE_BAND', 'DUR90_OLD_BAND', 'DUR90_DAILY'];
const FNS = ['years66ShiftYear', 'years66ShiftText', 'years66Walk', 'years66GigRemap', 'normalizeGigRecord',
  'bridge56NormalizeGig', 'boardNotePlayerOk', 'looksLikeEraId', 'humanizeEraId',
  'clamp', 'resolveRoleScale', 'shootBandFor', 'effectiveShootDays', 'effectiveShootWeekdays',
  'effectiveShootDeadlineDays', 'gigPayExact', 'dur90RoundPay', 'dur90CalibrateGig',
  'clampEntryReqToTemplate', 'entryGigPool229', 'mergeEntryGigsIntoPool', 'mergeSoftBridgeGigs'];
const STUBS_SRC = `
  var START = { y:1990, m:1, d:1 };
  var S = null;
  var GIGS = [];
`;
const WORLD_SRC = TF_SRC + '\n' + CONSTS.map(c=>{
  const s = extractConst(c); return s ? s.replace('const '+c, 'var '+c).replace('var '+c, 'var '+c) : 'var '+c+' = undefined;';
}).join('\n') + '\n' + FNS.map(f=>extractFn(f) || '').join('\n');
const W = new Function(STUBS_SRC + WORLD_SRC + `
; return { normalizeGigRecord, entryGigPool229, mergeEntryGigsIntoPool,
  setGIGS:(gs)=>{ GIGS = gs; }, getGIGS:()=>GIGS };`)();

/* ---------- P4：年份唔 double-shift ---------- */
const stamped = deepClone(gigs);
stamped.forEach(g=>{ g.__y66w = 1; });
const normed = stamped.map(g=>W.normalizeGigRecord(g));
const yearBad = normed.filter((g, i)=>g.year !== gigs[i].year);
ok('P4 打旗後 normalize：251 張年份全部唔郁', yearBad.length === 0,
   yearBad.slice(0, 3).map(g=>g.id + ':' + g.year).join(','));
const normedRaw = deepClone(gigs).map(g=>W.normalizeGigRecord(g));
const rawBad = normedRaw.filter((g, i)=>g.year !== gigs[i].year);
ok('P4 無旗直接 normalize：251 張年份全部唔郁（守衛）', rawBad.length === 0,
   rawBad.slice(0, 3).map(g=>g.id + ':' + g.year).join(','));
const normedTwice = normed.map(g=>W.normalizeGigRecord(deepClone(g)));
const twiceBad = normedTwice.filter((g, i)=>g.year !== gigs[i].year);
ok('P4 兩次 normalize：251 張年份全部唔郁', twiceBad.length === 0,
   twiceBad.slice(0, 3).map(g=>g.id + ':' + g.year).join(','));
const daysBad = normed.filter(g=>g.shootDaysHint !== g.days);
ok('P4 全數 251 張 shootDaysHint＝days', daysBad.length === 0,
   daysBad.slice(0, 3).map(g=>g.id).join(','));

/* ---------- P5：開局 1990 板面 ---------- */
const g1990 = deepClone(gigs.filter(g=>g.year === 1990)).map(g=>W.normalizeGigRecord(g));
const openStats = { acting:18, stage:14, vocal:14, looks:22, charm:16, iq:20, stamina:75 };
const entry1990 = g1990.filter(g=>g.tier === '臨記');
const entryOk = entry1990.filter(g=>{
  const req = g.req || {};
  return Object.keys(req).every(k=>(Number(req[k]) || 0) <= (openStats[k] != null ? openStats[k] : 0));
});
ok('P5 1990 年臨記 52 張全部合開局數值', entry1990.length === 52 && entryOk.length === 52,
   'entry=' + entry1990.length + ' ok=' + entryOk.length);
W.setGIGS(g1990);
const pool = W.entryGigPool229();
ok('P5 entryGigPool229 返 12 張臨記', pool.length === 12 && pool.every(g=>g.tier === '臨記'),
   'n=' + pool.length + ' tiers=' + [...new Set(pool.map(g=>g.tier))].join(','));
const poolOk = pool.every(g=>{
  const req = g.req || {};
  return Object.keys(req).every(k=>(Number(req[k]) || 0) <= (openStats[k] != null ? openStats[k] : 0));
});
ok('P5 入口池 12 張全部合開局數值', poolOk);
const poolSeasons = new Set(pool.map(g=>g.season));
ok('P5 入口池有冬季通告（開局 1 月）', poolSeasons.has('冬'), [...poolSeasons].join(','));
const junior1990 = g1990.filter(g=>g.tier === '初級');
ok('P5 1990 年有初級通告', junior1990.length > 0, 'n=' + junior1990.length);

/* ---------- P9–P11：舊嘢已刪、單一來源 ---------- */
for(const name of ['const LEADSTAR59', 'var TIER110', 'var REQ110', 'const NAME93_FIX',
    'const CLEAN100_GIG_RELEASE', 'const POSTER59_DATA', 'const POSTER85_IDS',
    'const ENTRY_GIGS_1988', 'STORY_WIRE.gigsByYearNew', 'function leadStar59Apply',
    'function name93ApplyGig', 'function ovr110Apply', 'function gig36(spec)',
    'function softBridgeGig(', 'function winterBridge88Gig(']){
  ok('P9 index.html 無 ' + name, !html.includes(name));
}
for(const f of ['gigs_1988.json', 'gigs_1989.json', 'gigs_1990.json', 'gigs_1991.json', 'gigs_1992.json']){
  ok('P10 content/' + f + ' 已刪', !fs.existsSync(path.join(ROOT, 'content', f)));
  ok('P10 loader 唔再 fetch ' + f, !html.includes('get("' + f + '")'));
}
ok('P11 sync 只讀 gigsByYear（pick(y) || pick(y-1) || pick(1990)）',
   (extractFn('syncGigsForCalendarYear') || '').includes('pick(y) || pick(y-1) || pick(1990)') &&
   !(extractFn('syncGigsForCalendarYear') || '').includes('pickNew'));
ok('P11 loader 將新庫寫入 gigsByYear（唔經 gigsByYearNew）',
   html.includes('STORY_WIRE.gigsByYear[yy] = { version: gigsNew.version') &&
   !html.includes('STORY_WIRE.gigsByYearNew'));

/* ---------- P12：F1 死卡正規化留返 ---------- */
const dead = W.normalizeGigRecord({ id:'gig_1990_test_201', year:1990, req:{ sing:50, dance:40, acting:10 } });
ok('P12 normalize sing→vocal、dance→stage',
   dead.req.vocal === 50 && dead.req.stage === 40 && dead.req.sing == null && dead.req.dance == null,
   JSON.stringify(dead.req));

console.log(fails ? ('FAILURES: ' + fails) : 'ALL PASS');
process.exit(fails ? 1 : 0);
