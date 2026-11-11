// v20a90 DUR90 工期/片酬校準・邏輯測試
// 合約（用戶 2026-11-11 08:30：正常製作拍攝/錄製日數要對得返現實）：
//   A 校準帶常量同 spec 一致（ROLE_SCALE_BAND 已更新、DUR90 舊帶指紋/日薪帶在位）
//   B 全池普查（五包庫存＋全部注入）：模板帶校準級 gig 工期必喺校準帶內、日薪必喺
//     位階日薪帶內（容許四捨五入誤差）；人手 pin 帶 gig 工期 ≤3 日（兩張人手大碟例外）
//   C 期限：全部 gig 嘅 deadline ≥ 拍完所需日曆日（唔會接咗拍唔完）
//   D 提早窗夾位：全部 gig 所需日曆日 ≤ 提早窗＋成季（60＋92＝152，接到趕得上檔期）
//   E 冪等：校準後再 normalize，工期/片酬/deadline 唔再變
//   F 錨點：film_01 總額保住 3500、日薪 269→入帶；頂級廣告日薪 ≤8000
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
const SPEC_DAILY = {
  '初': [[300,1200],[300,2000]],
  '中': [[600,2500],[600,4000]],
  '高': [[1000,3000],[1500,8000]],
};
const HAND_ALLOW_DAYS = { gig_1988_rec_hk_autumn:13, gig_1988_rec_star_spring:13 };
let fails = 0;
function ok(name, cond, extra){
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : ''));
  if(!cond) fails++;
}
const tfA = html.indexOf('/* ==== v20a55 TEXTFIX');
const tfB = html.indexOf('async function refreshCopyPacksFromDisk(){');
const TF_SRC = html.slice(tfA, tfB);
const CONSTS = ['STAT_LABEL','LEADSTAR59','POSTER59_STAR_IDS','POSTER85_IDS','ENTRY_GIGS_1988',
  'GIG_REQ_KEYS88','WINTER_ENTRY_GIGS_88','GIG_SEASON_SPAN88','GIG_SEASON_LEAD88',
  'SHOOT_DAYS','ROLE_SCALE_BAND','MID_GIGS_1988_35','SOFT_BRIDGE_GIGS_1988','INTEL_HIDDEN_GIGS',
  'FAVOR_DUE_GIGS','RIVAL_FACEOFF_GIGS','EXODUS_GIGS','WF3_LIAO_GIG','WF3_LIAO_HARVEST_GIG','BR89_GIGS',
  'DUR90_OLD_BAND','DUR90_DAILY'];
const FNS = ['years66ShiftYear','years66ShiftText','years66Walk','years66GigRemap','normalizeGigRecord',
  'bridge56NormalizeGig','leadStar59Apply','leadStar59Of','boardNotePlayerOk','looksLikeEraId','humanizeEraId',
  'clamp','resolveRoleScale','shootBandFor','effectiveShootDays','effectiveShootWeekdays',
  'effectiveShootDeadlineDays','gigPayExact','winterBridge88Gig','softBridgeGig',
  'dur90RoundPay','dur90CalibrateGig'];
let W = null, extractErr = '';
try{
  const WORLD_SRC = TF_SRC + '\n' + CONSTS.map(c=>extractConst(c).replace('const '+c, 'var '+c)).join('\n')
    + '\n' + FNS.map(f=>extractFn(f)).join('\n')
    + '\n' + extractConst('WINTER_BRIDGE_GIGS_88').replace('const WINTER_BRIDGE_GIGS_88', 'var WINTER_BRIDGE_GIGS_88');
  const STUBS_SRC = `
    var START = { y:1990, m:1, d:1 };
    var S = null;
    var GIGS = [];
    var COURSE_DEFS = {};
    var softPreviewOn = function(){ return false; };
  `;
  W = new Function(STUBS_SRC + WORLD_SRC + `
; return { years66Walk, normalizeGigRecord, resolveRoleScale, shootBandFor, effectiveShootDays,
  effectiveShootWeekdays, effectiveShootDeadlineDays, gigPayExact,
  ENTRY_GIGS_1988, WINTER_ENTRY_GIGS_88, WINTER_BRIDGE_GIGS_88, MID_GIGS_1988_35,
  SOFT_BRIDGE_GIGS_1988, INTEL_HIDDEN_GIGS, FAVOR_DUE_GIGS, RIVAL_FACEOFF_GIGS, EXODUS_GIGS,
  WF3_LIAO_GIG, WF3_LIAO_HARVEST_GIG, BR89_GIGS, ROLE_SCALE_BAND, SHOOT_DAYS, DUR90_OLD_BAND, DUR90_DAILY };`)();
}catch(e){ extractErr = e.message; }
ok('A0 DUR90 符號抽取成功（v89 冇呢啲常量 → 抽唔到）', !!W, extractErr);
if(W){
  // STUBS 內 S=null：normalize 各層對 S 嘅讀取都有 try/catch 或空值防御（同 audit90 harness 一致）
  function deepClone(o){ return JSON.parse(JSON.stringify(o)); }
  function loadPackPipeline(y){
    const pack = deepClone(JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gigs_'+y+'.json'), 'utf8')));
    W.years66Walk(pack, null);
    return (pack.gigs || []).map(g => W.normalizeGigRecord(g));
  }
  const pool = [];
  for(const y of [1988, 1989, 1990, 1991, 1992]) for(const g of loadPackPipeline(y)) pool.push(g);
  const inj = [
    ...(W.ENTRY_GIGS_1988 || []), ...(W.WINTER_ENTRY_GIGS_88 || []), ...(W.WINTER_BRIDGE_GIGS_88 || []),
    ...(W.MID_GIGS_1988_35 || []), ...(W.SOFT_BRIDGE_GIGS_1988 || []), ...(W.INTEL_HIDDEN_GIGS || []),
    ...(W.FAVOR_DUE_GIGS || []), ...(W.RIVAL_FACEOFF_GIGS || []), ...(W.EXODUS_GIGS || []),
    W.WF3_LIAO_GIG, W.WF3_LIAO_HARVEST_GIG, ...(W.BR89_GIGS || []),
  ];
  for(const g of inj){ if(g && g.id) pool.push(W.normalizeGigRecord(deepClone(g))); }

  // A 校準帶常量
  ok('A1 ROLE_SCALE_BAND ＝ 校準 spec', JSON.stringify(W.ROLE_SCALE_BAND) === JSON.stringify(SPEC_BAND), JSON.stringify(W.ROLE_SCALE_BAND));
  ok('A2 DUR90_DAILY ＝ spec 日薪帶', JSON.stringify(W.DUR90_DAILY) === JSON.stringify(SPEC_DAILY));
  ok('A3 SHOOT_DAYS fallback 跟新帶', W.SHOOT_DAYS['廣告'][1] === 2 && W.SHOOT_DAYS['唱片通告'][0] === 6 && W.SHOOT_DAYS['綜藝'][1] === 2);

  // B 全池普查
  const isAdScale = s => (s === 'ad_av' || s === 'ad_print' || s === 'photobook');
  let calN = 0, handN = 0, bandBad = [], dailyBad = [], handBad = [];
  for(const g of pool){
    const rs = W.resolveRoleScale(g);
    const days = W.effectiveShootDays(g);
    if(g.entryTier || g.softBridge){ if(!(days >= 1 && days <= 2)) handBad.push(g.id + ':entry/bridge days=' + days); continue; }
    if(!rs || !SPEC_BAND[rs]){ if(days > 5) handBad.push(g.id + ':noscale days=' + days); continue; }
    const calibrated = Array.isArray(g.shootBand) && g.shootBand[0] === SPEC_BAND[rs][0] && g.shootBand[1] === SPEC_BAND[rs][1];
    if(calibrated){
      calN++;
      const band = SPEC_BAND[rs];
      if(!(days >= band[0] && days <= band[1])) bandBad.push(g.id + ':' + rs + ' days=' + days);
      const pay = W.gigPayExact(g);
      if(pay != null && pay > 0){
        const db = (SPEC_DAILY[g.tier || '初'] || SPEC_DAILY['初'])[isAdScale(rs) ? 1 : 0];
        const daily = pay / days;
        const slack = 55 / days + daily * 0.02;
        if(daily < db[0] - slack || daily > db[1] + slack) dailyBad.push(g.id + ':' + rs + '/' + (g.tier || '初') + ' daily=' + Math.round(daily) + ' band=' + db.join('-'));
      }
    } else {
      handN++;
      if(!(days <= 3 || HAND_ALLOW_DAYS[g.id] === days)) handBad.push(g.id + ':hand days=' + days);
    }
  }
  ok('B1 校準級工期全喺帶內（' + calN + ' 張）', bandBad.length === 0, bandBad.slice(0, 5).join(' ; '));
  ok('B2 校準級日薪全喺位階帶內', dailyBad.length === 0, dailyBad.slice(0, 5).join(' ; '));
  ok('B3 人手級工期 ≤3 日或表列例外（' + handN + ' 張）', handBad.length === 0, handBad.slice(0, 5).join(' ; '));
  ok('B4 校準級覆蓋庫存主體（≥330）', calN >= 330, 'calN=' + calN);

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
  const film01 = pool.find(g => g.id === 'gig_1988_film_01');
  ok('F1 film_01 工期 13→5、總額保住 3500', !!film01 && W.effectiveShootDays(film01) === 5 && W.gigPayExact(film01) === 3500,
     film01 ? ('days=' + W.effectiveShootDays(film01) + ' pay=' + W.gigPayExact(film01)) : 'missing');
  const ad07 = pool.find(g => g.id === 'gig_1988_ad_07');
  ok('F2 ad_07 日薪由 9167 夾到 ≤8000', !!ad07 && (W.gigPayExact(ad07) / W.effectiveShootDays(ad07)) <= 8000 + 30,
     ad07 ? ('daily=' + Math.round(W.gigPayExact(ad07) / W.effectiveShootDays(ad07))) : 'missing');
}
console.log(fails === 0 ? 'ALL PASS' : ('FAILURES: ' + fails));
process.exit(fails === 0 ? 0 : 1);
