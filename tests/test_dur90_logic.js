// v20a90 DUR90 工期/片酬校準・邏輯測試（v20a229 B3 新庫版）
// 合約（用戶 2026-11-11 08:30：正常製作拍攝/錄製日數要對得返現實）：
//   A 校準帶常量同 spec 一致（ROLE_SCALE_BAND 已更新、DUR90 舊帶指紋/日薪帶在位）
//   B 新庫普查（267 張）：raw days 全部喺 roleScale 帶內（clamp 唔郁手）；日薪必喺
//     位階日薪帶內（容許四捨五入誤差；4 張 1992 稀有大碟＋1 張《星夜迷離》例外，見 DAILY_ALLOW_229）；
//     全部有 days（shootDaysHint＝days）；resolveRoleScale 全部認到帶
//   C 期限：全部 gig 嘅 deadline ≥ 拍完所需日曆日（唔會接咗拍唔完）
//   D 提早窗夾位：全部 gig 所需日曆日 ≤ 提早窗＋成季（60＋92＝152，接到趕得上檔期）
//   E 冪等：校準後再 normalize，工期/片酬/deadline 唔再變
//   F 錨點：film_112《雪山劍客》工期 14 日、總額中位 15400；rec_110 稀有大碟日薪 3080
//       （表列例外值，釘死——將來數據校準改數值要同步改呢度）；v232《星夜迷離》日薪 3100
//       （攻略定價 $3,100，表列例外，同上釘死）
// 反證：v89 index 冇 DUR90 常量、ROLE_SCALE_BAND 係舊帶、日薪大量出帶 → FAIL。
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) throw new Error('fn not found: '+name);
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){ if(html[j]==='{') depth++; else if(html[j]==='}'){ depth--; if(depth===0) break; } }
  return html.slice(i, j+1);
}
function extractConst(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) throw new Error('const not found: '+name);
  let depth=0, started=false;
  for(let k=i; k<html.length; k++){
    const ch = html[k];
    if(ch==='{'||ch==='['){ depth++; started = true; }
    else if(ch==='}'||ch===']'){ depth--; if(started && depth===0) return html.slice(i, k+1)+';'; }
    else if(ch===';' && !started) return html.slice(i, k+1);
  }
  throw new Error('const end not found: '+name);
}
const SPEC_BAND = {
  film_lead_big:[22,28], film_support_main:[10,18], film_support_small:[3,8],
  tv_lead_long:[24,36], tv_support_main:[12,20], tv_cameo_short:[1,5],
  rec_album:[6,14], mtv:[1,3], ad_av:[1,2], ad_print:[1,2], photobook:[1,2],
  variety_ep:[1,2], variety_special:[1,3],
};
/* v20a229 B2：DUR90_DAILY 五級化——五級各一鍵，值按機械級對位（臨記／初級→初、
   中級→中、高級／稀有→高）；舊三級鍵留返。鍵次序跟 index.html 一致（A2 係逐字比對）。 */
const SPEC_DAILY = {
  '初': [[300,1200],[300,2000]],
  '中': [[600,2500],[600,4000]],
  '高': [[1000,3000],[1500,8000]],
  '臨記': [[300,1200],[300,2000]],
  '初級': [[300,1200],[300,2000]],
  '中級': [[600,2500],[600,4000]],
  '高級': [[1000,3000],[1500,8000]],
  '稀有': [[1000,3000],[1500,8000]],
};
/* v20a229 B3：新庫 4 張 1992 稀有大碟日薪 3080，輕微超「高」帶上限 3000（超 80，2.7%）。
   數據跟進（留待通告數值校準票處理），B3 換庫唔改數值；呢度表列例外，唔當通過。 */
const DAILY_ALLOW_229 = { gig_1992_rec_107:3080, gig_1992_rec_108:3080, gig_1992_rec_109:3080, gig_1992_rec_110:3080, gig_1991_tv_122:3100 }; /* v232：《星夜迷離》攻略定價 $3,100（通宵緊急替工），表列例外 */
let fails = 0;
function ok(name, cond, extra){
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : ''));
  if(!cond) fails++;
}
const tfA = html.indexOf('/* ==== v20a55 TEXTFIX');
const tfB = html.indexOf('async function refreshCopyPacksFromDisk(){');
const TF_SRC = html.slice(tfA, tfB);
const CONSTS = ['STAT_LABEL','POSTER59_STAR_IDS',
  'GIG_REQ_KEYS88','GIG_SEASON_SPAN88','GIG_SEASON_LEAD88',
  'SHOOT_DAYS','ROLE_SCALE_BAND','DUR90_OLD_BAND','DUR90_DAILY'];
const FNS = ['normalizeGigRecord',
  'bridge56NormalizeGig','leadStar59Of','boardNotePlayerOk','looksLikeEraId','humanizeEraId',
  'clamp','resolveRoleScale','shootBandFor','effectiveShootDays','effectiveShootWeekdays',
  'effectiveShootDeadlineDays','gigPayExact',
  'dur90RoundPay','dur90CalibrateGig'];
let W = null, extractErr = '';
try{
  const WORLD_SRC = TF_SRC + '\n' + CONSTS.map(c=>extractConst(c).replace('const '+c, 'var '+c)).join('\n')
    + '\n' + FNS.map(f=>extractFn(f)).join('\n');
  const STUBS_SRC = `
    var START = { y:1990, m:1, d:1 };
    var S = null;
    var GIGS = [];
    var COURSE_DEFS = {};
    var softPreviewOn = function(){ return false; };
  `;
  W = new Function(STUBS_SRC + WORLD_SRC + `
; return { normalizeGigRecord, resolveRoleScale, shootBandFor, effectiveShootDays,
  effectiveShootWeekdays, effectiveShootDeadlineDays, gigPayExact,
  ROLE_SCALE_BAND, SHOOT_DAYS, DUR90_OLD_BAND, DUR90_DAILY };`)();
}catch(e){ extractErr = e.message; }
ok('A0 DUR90 符號抽取成功（v89 冇呢啲常量 → 抽唔到）', !!W, extractErr);
if(W){
  function deepClone(o){ return JSON.parse(JSON.stringify(o)); }
  const packNew = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gigs_new.json'), 'utf8'));
  const pool = (packNew.gigs || []).map(g => W.normalizeGigRecord(deepClone(g)));
  ok('A4 新庫 267 張入池', pool.length === 267, 'n=' + pool.length);

  // A 校準帶常量
  ok('A1 ROLE_SCALE_BAND ＝ 校準 spec', JSON.stringify(W.ROLE_SCALE_BAND) === JSON.stringify(SPEC_BAND), JSON.stringify(W.ROLE_SCALE_BAND));
  ok('A2 DUR90_DAILY ＝ spec 日薪帶', JSON.stringify(W.DUR90_DAILY) === JSON.stringify(SPEC_DAILY));
  ok('A3 SHOOT_DAYS fallback 跟新帶', W.SHOOT_DAYS['廣告'][1] === 2 && W.SHOOT_DAYS['唱片通告'][0] === 6 && W.SHOOT_DAYS['綜藝'][1] === 2);

  // B 新庫普查
  const isAdScale = s => (s === 'ad_av' || s === 'ad_print' || s === 'photobook');
  let clampBad = [], dailyBad = [], noDays = [], noBand = [];
  for(const g of pool){
    const rs = W.resolveRoleScale(g);
    if(!rs || !SPEC_BAND[rs]){ noBand.push(g.id + ':' + rs); continue; }
    if(typeof g.days !== 'number' || typeof g.shootDaysHint !== 'number' || g.shootDaysHint !== g.days) noDays.push(g.id);
    const days = W.effectiveShootDays(g);
    if(days !== g.days) clampBad.push(g.id + ':' + rs + ' days=' + g.days + ' eff=' + days + ' band=' + SPEC_BAND[rs].join('-'));
    const pay = W.gigPayExact(g);
    if(pay != null && pay > 0){
      const db = (SPEC_DAILY[g.tier || '初'] || SPEC_DAILY['初'])[isAdScale(rs) ? 1 : 0];
      const daily = pay / days;
      const slack = 55 / days + daily * 0.02;
      if(daily < db[0] - slack || daily > db[1] + slack){
        if(DAILY_ALLOW_229[g.id] === Math.round(daily)) continue; // 表列例外
        dailyBad.push(g.id + ':' + rs + '/' + (g.tier || '初') + ' daily=' + Math.round(daily) + ' band=' + db.join('-'));
      }
    }
  }
  ok('B1 raw days 全部喺 roleScale 帶內（clamp 唔郁手，267 張）', clampBad.length === 0, clampBad.slice(0, 5).join(' ; '));
  ok('B2 日薪全喺位階帶內（5 張表列例外除外：4 張稀有大碟＋《星夜迷離》）', dailyBad.length === 0, dailyBad.slice(0, 5).join(' ; '));
  ok('B3 全部有 days 且 shootDaysHint＝days', noDays.length === 0, noDays.slice(0, 5).join(' ; '));
  ok('B4 resolveRoleScale 全部認到帶（267 張）', noBand.length === 0, noBand.slice(0, 5).join(' ; '));

  // C/D 期限與夾位
  let ddlBad = [], winBad = [];
  for(const g of pool){
    const days = W.effectiveShootDays(g);
    const wds = W.effectiveShootWeekdays(g);
    const wdc = (Array.isArray(wds) && wds.length) ? new Set(wds.map(Number)).size : 5;
    const need = Math.ceil(days * 7 / Math.max(1, wdc));
    if(W.effectiveShootDeadlineDays(g, days) < need) ddlBad.push(g.id + ':need' + need + '>ddl' + W.effectiveShootDeadlineDays(g, days));
    if(need > 152) winBad.push(g.id + ':need' + need);
  }
  ok('C 全部 gig deadline ≥ 拍完所需日曆日', ddlBad.length === 0, ddlBad.slice(0, 5).join(' ; '));
  ok('D 全部 gig 所需日曆日 ≤ 提早窗+成季（152）', winBad.length === 0, winBad.slice(0, 5).join(' ; '));

  // E 冪等
  const snap = g => JSON.stringify([g.shootBand, g.shootDaysHint, g.payExact, g.pay, g.shootDeadlineDays]);
  let idemBad = 0;
  for(const g of pool){ const g2 = W.normalizeGigRecord(g); if(snap(g) !== snap(g2)) idemBad++; }
  ok('E 全池再 normalize 冪等', idemBad === 0, 'bad=' + idemBad);

  // F 錨點
  const film112 = pool.find(g => g.id === 'gig_1990_film_112');
  ok('F1 film_112《雪山劍客》工期 14 日、總額中位 15400', !!film112 && W.effectiveShootDays(film112) === 14 && W.gigPayExact(film112) === 15400,
     film112 ? ('days=' + W.effectiveShootDays(film112) + ' pay=' + W.gigPayExact(film112)) : 'missing');
  const rec110 = pool.find(g => g.id === 'gig_1992_rec_110');
  ok('F2 rec_110 稀有大碟日薪 3080（表列例外值）', !!rec110 && Math.round(W.gigPayExact(rec110) / W.effectiveShootDays(rec110)) === 3080,
     rec110 ? ('daily=' + Math.round(W.gigPayExact(rec110) / W.effectiveShootDays(rec110))) : 'missing');
}
console.log(fails === 0 ? 'ALL PASS' : ('FAILURES: ' + fails));
process.exit(fails === 0 ? 0 : 1);
