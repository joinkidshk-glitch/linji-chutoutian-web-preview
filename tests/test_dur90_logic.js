// v20a90 DUR90 工期/片酬校準・邏輯測試（v20a229 B3 新庫版）
// 合約（用戶 2026-11-11 08:30：正常製作拍攝/錄製日數要對得返現實）：
//   A 校準帶常量同 spec 一致（ROLE_SCALE_BAND 已更新、DUR90 舊帶指紋/日薪帶在位）
//   B 新庫普查（276 張）：raw days 全部喺 roleScale 帶內（clamp 唔郁手）；日薪必喺
//     位階日薪帶內（容許四捨五入誤差；表列例外已清零，見 DAILY_ALLOW_229——舊 5 個例外值
//     全部同現數據唔符，已退役，唔再豁免任何一張）；
//     全部有 days（shootDaysHint＝days）；resolveRoleScale 全部認到帶
//   C 期限：全部 gig 嘅 deadline ≥ 拍完所需日曆日（唔會接咗拍唔完）
//   D 提早窗夾位：全部 gig 所需日曆日 ≤ 提早窗＋成季（60＋92＝152，接到趕得上檔期）
//   E 冪等：校準後再 normalize，工期/片酬/deadline 唔再變
//   F 錨點（v252 重寫，舊庫錨點全數作廢；v261 ÷10）：film_112 係《西環月色》愛情青春男配角，工期 4 日、
//       總額中位 260；《雪山劍客》呢個名新庫根本唔存在，最接近係《雪山雙劍傳》（film_111／1991，
//       6 日／390）；rec_110 係稀有 MTV《黃昏之約》男主角，日薪 275（入帶，唔再係例外）；
//       《星夜迷離》而家係 tv_203，日薪 68（入帶）。將來數據校準改數值要同步改呢度。
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
/* v20a261：B2 普查改用 SPEC §7.1 新日薪帶（臨記 25–40／初級 50–90／中級 90–160／
   高級 160–300／稀有 200–400；庫內實測 287 張全部落帶，見 §6.2 驗證）。
   SPEC_DAILY 保持原值——佢係 A2 逐字比對 live DUR90_DAILY 嘅舊帶；live DUR90_DAILY
   本身係舊庫校準兜底（註解明言「新庫唔行 DUR90 指紋校準，呢度係兜底，唔係新庫片酬來源」），
   v261 冇郁佢，呢度亦唔郁。捨入寬容同步 ÷10（55→5.5；新庫 pay 捨入到 $1）。 */
const SPEC_TIER_DAILY = {
  '臨記': [25, 40],
  '初級': [50, 90],
  '中級': [90, 160],
  '高級': [160, 300],
  '稀有': [200, 400],
};
/* v252 重推導：舊表列例外 5 個值全部同現數據唔符，已退役——
   rec_107／1992 實際日薪 121（中級 MTV，新帶 [90,160]，入帶）、rec_108／1992 實際 220
   （高級 MTV，新帶 [160,300]，入帶）、rec_109／1992 實際 220（高級大碟，新帶 [160,300]，入帶）、
   rec_110／1992 實際 275（稀有 MTV，新帶 [200,400] 入帶；舊 2750 對應舊稀有帶 [2000,4000]，
   3080 係更舊庫遺留值）、《星夜迷離》舊 tv_122 已唔存在，
   而家 tv_203 日薪 68（初級 tv_cameo_short，新帶 [50,90]，入帶）。現庫 0 張出帶，例外表清零；
   機制留返（將來真有出帶先再填表，唔可以靜默豁免）。 */
const DAILY_ALLOW_229 = {};
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
  ok('A4 新庫 287 張入池', pool.length === 287, 'n=' + pool.length);

  // A 校準帶常量
  ok('A1 ROLE_SCALE_BAND ＝ 校準 spec', JSON.stringify(W.ROLE_SCALE_BAND) === JSON.stringify(SPEC_BAND), JSON.stringify(W.ROLE_SCALE_BAND));
  ok('A2 DUR90_DAILY ＝ spec 日薪帶', JSON.stringify(W.DUR90_DAILY) === JSON.stringify(SPEC_DAILY));
  ok('A3 SHOOT_DAYS fallback 跟新帶', W.SHOOT_DAYS['廣告'][1] === 2 && W.SHOOT_DAYS['唱片通告'][0] === 6 && W.SHOOT_DAYS['綜藝'][1] === 2);

  // B 新庫普查
  let clampBad = [], dailyBad = [], noDays = [], noBand = [];
  for(const g of pool){
    const rs = W.resolveRoleScale(g);
    if(!rs || !SPEC_BAND[rs]){ noBand.push(g.id + ':' + rs); continue; }
    if(typeof g.days !== 'number' || typeof g.shootDaysHint !== 'number' || g.shootDaysHint !== g.days) noDays.push(g.id);
    const days = W.effectiveShootDays(g);
    if(days !== g.days) clampBad.push(g.id + ':' + rs + ' days=' + g.days + ' eff=' + days + ' band=' + SPEC_BAND[rs].join('-'));
    const pay = W.gigPayExact(g);
    if(pay != null && pay > 0){
      const db = SPEC_TIER_DAILY[g.tier || '初級'] || SPEC_TIER_DAILY['初級'];
      const daily = pay / days;
      const slack = 5.5 / days + daily * 0.02;
      if(daily < db[0] - slack || daily > db[1] + slack){
        if(DAILY_ALLOW_229[g.id] === Math.round(daily)) continue; // 表列例外
        dailyBad.push(g.id + ':' + rs + '/' + (g.tier || '初') + ' daily=' + Math.round(daily) + ' band=' + db.join('-'));
      }
    }
  }
  ok('B1 raw days 全部喺 roleScale 帶內（clamp 唔郁手，287 張）', clampBad.length === 0, clampBad.slice(0, 5).join(' ; '));
  ok('B2 日薪全喺位階帶內（表列例外 0 張）', dailyBad.length === 0, dailyBad.slice(0, 5).join(' ; '));
  ok('B3 全部有 days 且 shootDaysHint＝days', noDays.length === 0, noDays.slice(0, 5).join(' ; '));
  ok('B4 resolveRoleScale 全部認到帶（287 張）', noBand.length === 0, noBand.slice(0, 5).join(' ; '));

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

  // F 錨點（v252 重寫）
  const film112 = pool.find(g => g.id === 'gig_1990_film_112');
  ok('F1 film_112《西環月色》男配角工期 4 日、總額中位 260', !!film112 && W.effectiveShootDays(film112) === 4 && W.gigPayExact(film112) === 260,
     film112 ? ('days=' + W.effectiveShootDays(film112) + ' pay=' + W.gigPayExact(film112)) : 'missing');
  const noSnowSword = pool.filter(g => (g.title || '').indexOf('雪山劍客') >= 0);
  const snowTwin = pool.find(g => g.id === 'gig_1991_film_111');
  ok('F1b《雪山劍客》已唔喺新庫；最接近《雪山雙劍傳》（film_111／1991）6 日／390',
     noSnowSword.length === 0 && !!snowTwin && W.effectiveShootDays(snowTwin) === 6 && W.gigPayExact(snowTwin) === 390,
     snowTwin ? ('days=' + W.effectiveShootDays(snowTwin) + ' pay=' + W.gigPayExact(snowTwin)) : 'missing');
  const rec110 = pool.find(g => g.id === 'gig_1992_rec_110');
  ok('F2 rec_110《黃昏之約》MV 男主角日薪 275（稀有 MTV，入帶，唔再係表列例外）',
     !!rec110 && Math.round(W.gigPayExact(rec110) / W.effectiveShootDays(rec110)) === 275 && !(rec110.id in DAILY_ALLOW_229),
     rec110 ? ('daily=' + Math.round(W.gigPayExact(rec110) / W.effectiveShootDays(rec110))) : 'missing');
  const xingye = pool.find(g => g.id === 'gig_1991_tv_203');
  ok('F2b《星夜迷離》（tv_203）日薪 68（入帶，唔再係表列例外；舊 tv_122 已唔存在）',
     !!xingye && Math.round(W.gigPayExact(xingye) / W.effectiveShootDays(xingye)) === 68 && !pool.find(g => g.id === 'gig_1991_tv_122'),
     xingye ? ('daily=' + Math.round(W.gigPayExact(xingye) / W.effectiveShootDays(xingye))) : 'missing');
  const oldAllow = [['gig_1992_rec_107', 121], ['gig_1992_rec_108', 220], ['gig_1992_rec_109', 220]];
  ok('F2c 舊 3080 例外值已退役（rec_107 121／rec_108 220／rec_109 220，全部入帶）',
     oldAllow.every(([id, daily]) => { const g = pool.find(x => x.id === id); return g && Math.round(W.gigPayExact(g) / W.effectiveShootDays(g)) === daily; }) &&
     Object.keys(DAILY_ALLOW_229).length === 0,
     oldAllow.map(([id]) => { const g = pool.find(x => x.id === id); return id + '=' + (g ? Math.round(W.gigPayExact(g) / W.effectiveShootDays(g)) : 'missing'); }).join(', '));
}
console.log(fails === 0 ? 'ALL PASS' : ('FAILURES: ' + fails));
process.exit(fails === 0 ? 0 : 1);
