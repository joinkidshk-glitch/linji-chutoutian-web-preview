// v20a229 B3 換庫：單一來源＋年份唔郁・邏輯測試（B1 地基嘅 B3 版）
// 合約（AUDIT229 §2／§13／附錄 B；SPEC §2.2.2 year 欄位）：
//   A 載入接線：gigs_new.json 有 fetch、唔行 years66Walk、分三年入 gigsByYear（單一來源，
//     唔再經 gigsByYearNew）、syncGigsForCalendarYear 只讀 gigsByYear
//   B 舊 pack 已刪：content/gigs_1988–1992.json 唔存在；loader 唔再 fetch 舊 pack；
//     index.html 入面冇舊 pack 檔名字面
//   C 新 pack 年份唔郁：載入層打旗＋normalize 守衛兩道防線，1990／1991／1992 各有數；
//     兩次 normalize 冪等；玩家面文字欄年份 token 唔變
//   D days→shootDaysHint 映射：抽 20 張跨 roleScale＋全數 282 張，
//     effectiveShootDays 全部等於 days；新 gig 全部有 days
//   E 舊表已刪：TIER110／REQ110／NAME93／LEADSTAR59／CLEAN100 全部唔喺 index.html，
//     normalize 入面亦無佢哋嘅呼叫
// 反證：對 B2 index 行 → A3／A4 雙來源 FAIL、B 舊 pack 在位 FAIL、E 舊表在位 FAIL。
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
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
let fails = 0;
function ok(name, cond, extra){
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : ''));
  if(!cond) fails++;
}
function deepClone(o){ return JSON.parse(JSON.stringify(o)); }

/* ---------- A 載入接線（靜態） ---------- */
ok('A1 loader fetch gigs_new.json', html.includes('get("gigs_new.json")'));
ok('A2 新 pack 唔行 years66Walk', !html.includes('years66Walk(gigsNew'));
ok('A3 新 pack 分三年入 gigsByYear（單一來源，唔經 gigsByYearNew）',
   !html.includes('STORY_WIRE.gigsByYearNew') &&
   html.includes('STORY_WIRE.gigsByYear[yy] = { version: gigsNew.version'));
ok('A4 syncGigsForCalendarYear 單一來源（pick(y) || pick(y-1) || pick(1990)，無 pickNew）',
   (()=>{ const s = extractFn('syncGigsForCalendarYear') || '';
     return s.includes('pick(y) || pick(y-1) || pick(1990)') && !s.includes('pickNew'); })());
ok('A5 新 pack 載入打 __y66w 旗（唔係 JSON 欄位）',
   html.includes('g.__y66w = 1') && !fs.readFileSync(path.join(ROOT, 'content', 'gigs_new.json'), 'utf8').includes('__y66w'));

/* ---------- sandbox：normalize＋effectiveShootDays ---------- */
const tfA = html.indexOf('/* ==== v20a55 TEXTFIX');
const tfB = html.indexOf('async function refreshCopyPacksFromDisk(){');
if(tfA<0 || tfB<=tfA){ console.log('FAIL TEXTFIX55 block not found'); process.exit(1); }
const TF_SRC = html.slice(tfA, tfB);
const CONSTS = ['STAT_LABEL','POSTER59_STAR_IDS','GIG_REQ_KEYS88','SHOOT_DAYS',
  'ROLE_SCALE_BAND','DUR90_OLD_BAND','DUR90_DAILY'];
const FNS = ['years66ShiftYear','years66ShiftText','years66Walk','years66GigRemap','normalizeGigRecord',
  'bridge56NormalizeGig','boardNotePlayerOk','looksLikeEraId','humanizeEraId',
  'clamp','resolveRoleScale','shootBandFor','effectiveShootDays','effectiveShootWeekdays',
  'effectiveShootDeadlineDays','gigPayExact','dur90RoundPay','dur90CalibrateGig'];
const STUBS_SRC = `
  var START = { y:1990, m:1, d:1 };
  var S = null;
  var GIGS = [];
`;
const WORLD_SRC = TF_SRC + '\n' + CONSTS.map(c=>{
  const s = extractConst(c); return s ? s.replace('const '+c, 'var '+c).replace('var '+c, 'var '+c) : 'var '+c+' = undefined;';
}).join('\n') + '\n' + FNS.map(f=>extractFn(f) || '').join('\n');
const W = new Function(STUBS_SRC + WORLD_SRC + `
; return { years66Walk, normalizeGigRecord, effectiveShootDays };`)();

/* ---------- A6 sync 行為：三個年份真係揀新庫，缺席跌返舊庫 ---------- */
function makeSyncSandbox(year){
  const stubs = `
  var START = { y:1990, m:1, d:1 };
  var S = { dayIndex: 0 };
  var GIGS = [];
  var STORY_WIRE = { gigsByYear: {}, gigsYearActive: null, gigsVersion: null, errors: [] };
  var window = {};
  function dateObj(){ return new Date(${year}, 0, 1); }
  function mergeEntryGigsIntoPool(){}
  function mergeWinterBridge88(){}
`;
  const worldSync = TF_SRC + '\n' + CONSTS.map(c=>{
    const s = extractConst(c); return s ? s.replace('const '+c, 'var '+c).replace('var '+c, 'var '+c) : 'var '+c+' = undefined;';
  }).join('\n') + '\n' + FNS.concat(['syncGigsForCalendarYear','calendarSeason']).map(f=>extractFn(f) || '').join('\n');
  return new Function(stubs + worldSync + `
; return { sync: syncGigsForCalendarYear, norm: normalizeGigRecord, walk: years66Walk,
  getGIGS: function(){ return GIGS; }, getVer: function(){ return STORY_WIRE.gigsVersion; },
  setBy: function(by){ STORY_WIRE.gigsByYear = by; STORY_WIRE.gigsYearActive = null; } };`)();
}
const _newPackA6 = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gigs_new.json'), 'utf8'));
for(const y of [1990, 1991, 1992]){
  const W2 = makeSyncSandbox(y);
  const by = {};
  for(const yy of [1990, 1991, 1992]){
    const gs = _newPackA6.gigs.filter(g=>g.year === yy).map(g=>{ const c = deepClone(g); c.__y66w = 1; return c; });
    by[yy] = { version: 'gigs_new v2', year: yy, gigs: gs };
  }
  W2.setBy(by);
  W2.sync(true);
  const gigs = W2.getGIGS();
  const want = { 1990: 111, 1991: 95, 1992: 76 }[y];
  ok('A6 sync ' + y + ' 年揀新庫（' + want + ' 張、年份全部 ' + y + '、版本 gigs_new v2）',
     gigs.length === want && gigs.every(g=>g.year === y) && W2.getVer() === 'gigs_new v2',
     'n=' + gigs.length + ' ver=' + W2.getVer());
}
{
  /* 新庫缺席（by 空）→ 唔再有舊庫／內嵌 fallback，GIGS 留空 */
  const W2 = makeSyncSandbox(1990);
  W2.setBy({});
  W2.sync(true);
  const gigs = W2.getGIGS();
  ok('A6 新庫缺席（by 空）→ GIGS 留空，唔跌返舊庫', gigs.length === 0, 'n=' + gigs.length);
}
{
  /* 缺年跌返較早一年：1991 缺庫 → 用 1990（111 張、年份 1990） */
  const W2 = makeSyncSandbox(1991);
  const by = { 1990: { version: 'gigs_new v2', year: 1990, gigs: _newPackA6.gigs.filter(g=>g.year === 1990).map(g=>{ const c = deepClone(g); c.__y66w = 1; return c; }) } };
  W2.setBy(by);
  W2.sync(true);
  const gigs = W2.getGIGS();
  ok('A6 1991 缺庫跌返 1990（111 張、年份 1990）',
     gigs.length === 111 && gigs.every(g=>g.year === 1990), 'n=' + gigs.length);
}

/* ---------- B 舊 pack 已刪 ---------- */
for(const f of ['gigs_1988.json', 'gigs_1989.json', 'gigs_1990.json', 'gigs_1991.json', 'gigs_1992.json']){
  ok('B1 content/' + f + ' 已刪', !fs.existsSync(path.join(ROOT, 'content', f)));
  ok('B2 loader 唔再 fetch ' + f, !html.includes('get("' + f + '")'));
  ok('B3 index.html 無 ' + f + ' 字面', !html.includes(f));
}

/* ---------- C 新 pack 年份唔郁 ---------- */
const newPack = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gigs_new.json'), 'utf8'));
const newGigs = newPack.gigs || [];
ok('C0 gigs_new.json 282 張、版本 gigs_new v2、id 唯一', newGigs.length === 282 &&
   newPack.version === 'gigs_new v2' &&
   new Set(newGigs.map(g=>g.id)).size === 282, 'n=' + newGigs.length + ' ver=' + newPack.version);
/* C1：模擬 loader——打旗＋按年分組，再 normalize */
const stamped = deepClone(newGigs);
const byYear = { 1990: [], 1991: [], 1992: [] };
stamped.forEach(g=>{ g.__y66w = 1; if(byYear[g.year]) byYear[g.year].push(g); });
ok('C1 loader 分組 1990／1991／1992 = 111／95／76',
   byYear[1990].length === 111 && byYear[1991].length === 95 && byYear[1992].length === 76,
   [1990, 1991, 1992].map(y=>y + ':' + byYear[y].length).join(' '));
const normedStamped = stamped.map(g=>W.normalizeGigRecord(g));
const yearBad = normedStamped.filter((g, i)=>g.year !== newGigs[i].year);
ok('C2 打旗後 normalize：282 張年份全部唔郁', yearBad.length === 0,
   yearBad.slice(0, 3).map(g=>g.id + ':' + g.year).join(','));
/* C3：唔打旗、直接 normalize——normalize 層守衛都要擋住 */
const normedRaw = deepClone(newGigs).map(g=>W.normalizeGigRecord(g));
const rawBad = normedRaw.filter((g, i)=>g.year !== newGigs[i].year);
ok('C3 無旗直接 normalize：282 張年份全部唔郁（守衛）', rawBad.length === 0,
   rawBad.slice(0, 3).map(g=>g.id + ':' + g.year).join(','));
/* C4：冪等——兩次 normalize 年份唔變 */
const normedTwice = normedStamped.map(g=>W.normalizeGigRecord(deepClone(g)));
const twiceBad = normedTwice.filter((g, i)=>g.year !== newGigs[i].year);
ok('C4 兩次 normalize：282 張年份全部唔郁', twiceBad.length === 0,
   twiceBad.slice(0, 3).map(g=>g.id + ':' + g.year).join(','));
/* C5：玩家面文字欄年份 token 唔變（唔可以由 walker／remap 偷偷 +2） */
const TEXT_FIELDS = ['title','workTitle','roleLabel','roleHint','blurb','synopsis','boardNote','shootHint','discoverNote'];
const YEAR_TOKEN_RE = /1988|1989|1990|1991|1992|1993|1994/g;
function yearTokens(s){ return (String(s || '').match(YEAR_TOKEN_RE) || []).join(','); }
const textBad = [];
normedStamped.forEach((g, i)=>{
  for(const f of TEXT_FIELDS){
    if(yearTokens(g[f]) !== yearTokens(newGigs[i][f])) textBad.push(g.id + ':' + f);
  }
});
ok('C5 玩家面文字欄年份 token 全部唔變', textBad.length === 0, textBad.slice(0, 5).join(','));
/* C6：每一年各抽三張核對 */
for(const y of [1990, 1991, 1992]){
  const sample = normedStamped.filter(g=>g.year === y).slice(0, 3);
  ok('C6 ' + y + ' 年抽樣 3 張年份正確', sample.length === 3 && sample.every(g=>g.year === y),
     sample.map(g=>g.id).join(','));
}

/* ---------- D days→shootDaysHint 映射 ---------- */
const SCALES = ['film_lead_big','film_support_main','film_support_small','tv_lead_long','tv_support_main',
  'tv_cameo_short','rec_album','mtv','ad_av','ad_print','photobook','variety_ep','variety_special'];
const sample20 = [];
for(const sc of SCALES){
  const ofScale = normedStamped.filter(g=>g.roleScale === sc);
  if(ofScale[0] && sample20.length < 20) sample20.push(ofScale[0]);
}
for(const sc of SCALES){
  const ofScale = normedStamped.filter(g=>g.roleScale === sc);
  if(ofScale[1] && sample20.length < 20) sample20.push(ofScale[1]);
}
while(sample20.length < 20){
  const extra = normedStamped.find(g=>!sample20.includes(g));
  if(!extra) break;
  sample20.push(extra);
}
const sampleBad = sample20.filter(g=>g.shootDaysHint !== g.days || W.effectiveShootDays(g) !== g.days);
ok('D1 抽 20 張跨 roleScale：shootDaysHint＝days＝effectiveShootDays',
   sample20.length === 20 && sampleBad.length === 0,
   'n=' + sample20.length + ' scales=' + new Set(sample20.map(g=>g.roleScale)).size +
   ' bad=' + sampleBad.slice(0, 3).map(g=>g.id + ':' + g.days + '/' + g.shootDaysHint + '/' + W.effectiveShootDays(g)).join(','));
const allHintBad = normedStamped.filter(g=>g.shootDaysHint !== g.days);
ok('D2 全數 282 張 shootDaysHint＝days', allHintBad.length === 0,
   allHintBad.slice(0, 3).map(g=>g.id + ':' + g.days + '/' + g.shootDaysHint).join(','));
const allEffBad = normedStamped.filter(g=>W.effectiveShootDays(g) !== g.days);
ok('D3 全數 282 張 effectiveShootDays＝days', allEffBad.length === 0,
   allEffBad.slice(0, 3).map(g=>g.id + ':' + g.days + '/' + W.effectiveShootDays(g)).join(','));
const twiceHintBad = normedTwice.filter(g=>g.shootDaysHint !== g.days);
ok('D4 兩次 normalize：hint 仍然＝days', twiceHintBad.length === 0,
   twiceHintBad.slice(0, 3).map(g=>g.id).join(','));
/* D5：新 gig 全部有 days（映射有料，唔係空轉） */
ok('D5 新 gig 全部有 days 欄位',
   normedStamped.every(g=>typeof g.days === 'number'), 'n=' + normedStamped.length);

/* ---------- E 舊表已刪 ---------- */
for(const name of ['const LEADSTAR59', 'var TIER110', 'var REQ110', 'const NAME93_FIX',
    'const CLEAN100_GIG_RELEASE', 'const POSTER59_DATA', 'const POSTER85_IDS']){
  ok('E1 index.html 無 ' + name, !html.includes(name));
}
const normSrc = extractFn('normalizeGigRecord') || '';
for(const token of ['LEADSTAR59', 'name93ApplyGig', 'ovr110Apply', 'CLEAN100']){
  ok('E2 normalizeGigRecord 入面無 ' + token, !normSrc.includes(token));
}

console.log(fails ? ('FAILURES: ' + fails) : 'ALL PASS');
process.exit(fails ? 1 : 0);
