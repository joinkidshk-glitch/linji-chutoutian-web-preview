// v20a93 NAME93 名實對照・邏輯測試
// 合約（用戶 2026-11-11 12:59：臨記崗位唔准拎中高級價）：
//   A NAME93_FIX 對照表在位、43 個 id 全部喺全池存在
//   B 錨點：ad_08（用戶點名）片酬 4000→1500／快照壓返背景級；tv_08 主角約→
//     綜藝特輯 3 日 3600；rec_wanchai 改名專輯主唱＋synopsis 冇「主唱臨記」；
//     tv_kowloon_winter_high 改名男主角；gig_1991_film_04 14 日→2 日
//   C 名實守門（全池）：臨記類崗位（標題後綴／roleLabel 含臨記類字眼、非豁免）
//     日薪 ≤ 上限（廣告類 1600／其他 1700）、聲望中點 ≤17、人氣中點 ≤33、
//     日數 ≤8（長駐型白名單除外）；全池冇「臨記＋主角類」名銜自相矛盾
//   D 豁免完整：softBridge 保底機制冇俾人郁——1988 表 12 張片酬仍然 3700、
//     gig36 橋接家族 18 張仍然 softBridge 旗＋flat 年價（4700／5300）
//   E 冪等：NAME93 gig 兩次 normalize 結果一致（唔會俾 DUR90 二次校準覆寫）
//   F 改名冇撞名：改名 9 張新標題同全池其他 gig 唔重複
//   G 期限：43 張 deadline ≥ 拍完所需日曆日
// 反證：v92 index 冇 NAME93_FIX/name93ApplyGig → 抽取失敗 FAIL。
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
  const i = html.indexOf('const '+name+' =');
  if(i<0) return null;
  let depth=0, started=false;
  for(let k=i; k<html.length; k++){
    const ch = html[k];
    if(ch==='{'||ch==='['){ depth++; started = true; }
    else if(ch==='}'||ch===']'){ depth--; if(started && depth===0) return html.slice(i, k+1)+';'; }
    else if(ch===';' && !started) return html.slice(i, k+1);
  }
  return null;
}
let fails = 0;
function ok(name, cond, extra){
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : ''));
  if(!cond) fails++;
}
const tfA = html.indexOf('/* ==== v20a55 TEXTFIX');
const tfB = html.indexOf('async function refreshCopyPacksFromDisk(){');
if(tfA<0 || tfB<=tfA){ console.log('FAIL TEXTFIX55 block not found'); process.exit(1); }
const TF_SRC = html.slice(tfA, tfB);
const CONSTS = ['STAT_LABEL','LEADSTAR59','POSTER59_STAR_IDS','POSTER85_IDS','ENTRY_GIGS_1988',
  'GIG_REQ_KEYS88','WINTER_ENTRY_GIGS_88','GIG_SEASON_SPAN88','GIG_SEASON_LEAD88',
  'SHOOT_DAYS','ROLE_SCALE_BAND','MID_GIGS_1988_35','SOFT_BRIDGE_GIGS_1988','INTEL_HIDDEN_GIGS',
  'FAVOR_DUE_GIGS','RIVAL_FACEOFF_GIGS','EXODUS_GIGS','WF3_LIAO_GIG','WF3_LIAO_HARVEST_GIG','BR89_GIGS',
  'DUR90_OLD_BAND','DUR90_DAILY','NAT92_GIGS','NAME93_FIX'];
for(const m of html.matchAll(/const (GIGS36_[A-Z0-9_]+) =/g)){
  if(!CONSTS.includes(m[1]) && m[1] !== 'GIGS36_BY_YEAR' && m[1] !== 'GIGS36_ALL_IDS') CONSTS.push(m[1]);
}
CONSTS.push('GIGS36_BY_YEAR');
const FNS = ['years66ShiftYear','years66ShiftText','years66Walk','years66GigRemap','normalizeGigRecord',
  'bridge56NormalizeGig','leadStar59Apply','leadStar59Of','boardNotePlayerOk','looksLikeEraId','humanizeEraId',
  'clamp','resolveRoleScale','shootBandFor','effectiveShootDays','effectiveShootWeekdays',
  'effectiveShootDeadlineDays','gigPayExact','winterBridge88Gig','softBridgeGig','gig36','nat92Gig',
  'dur90RoundPay','dur90CalibrateGig','name93ApplyGig'];
const tryConst = c => { const s = extractConst(c); return s ? s.replace('const '+c, 'var '+c) : 'var '+c+' = undefined;'; };
const tryFn = f => extractFn(f) || '';
const WORLD_SRC = TF_SRC + '\n' + CONSTS.map(tryConst).join('\n') + '\n' + FNS.map(tryFn).join('\n')
  + '\n' + (extractConst('WINTER_BRIDGE_GIGS_88') || '').replace('const WINTER_BRIDGE_GIGS_88', 'var WINTER_BRIDGE_GIGS_88');
const STUBS_SRC = `
  var START = { y:1990, m:1, d:1 };
  var S = null;
  var GIGS = [];
  var COURSE_DEFS = {};
  var softPreviewOn = function(){ return false; };
`;
const W = new Function(STUBS_SRC + WORLD_SRC + `
; return { years66Walk, normalizeGigRecord, resolveRoleScale, effectiveShootDays,
  effectiveShootWeekdays, effectiveShootDeadlineDays, gigPayExact,
  NAME93_FIX: (typeof NAME93_FIX !== 'undefined') ? NAME93_FIX : null,
  name93ApplyGig: (typeof name93ApplyGig === 'function') ? name93ApplyGig : null,
  setS:(s)=>{S=s;},
  ENTRY_GIGS_1988, WINTER_ENTRY_GIGS_88, WINTER_BRIDGE_GIGS_88, MID_GIGS_1988_35,
  SOFT_BRIDGE_GIGS_1988, INTEL_HIDDEN_GIGS, FAVOR_DUE_GIGS, RIVAL_FACEOFF_GIGS, EXODUS_GIGS,
  WF3_LIAO_GIG, WF3_LIAO_HARVEST_GIG, BR89_GIGS, NAT92_GIGS, GIGS36_BY_YEAR };`)();
W.setS({ acting:99, stage:99, vocal:99, looks:99, charm:99, iq:99, stamina:99, fame:99, dayIndex:0, flags:{}, shoots:[], booked:[], enrolled:{} });
function deepClone(o){ return JSON.parse(JSON.stringify(o)); }

/* A 對照表在位 */
ok('A1 NAME93_FIX 在位', !!W.NAME93_FIX);
ok('A2 name93ApplyGig 在位', typeof W.name93ApplyGig === 'function');
const FIX = W.NAME93_FIX || {};
ok('A3 對照表 43 個 id', Object.keys(FIX).length === 43, 'n=' + Object.keys(FIX).length);

/* 全池（同 audit93 口徑） */
const pool = new Map();
function addPool(g, src){ if(g && g.id && !pool.has(g.id)) pool.set(g.id, g); }
for(const y of [1988, 1989, 1990, 1991, 1992]){
  const pack = deepClone(JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gigs_'+y+'.json'), 'utf8')));
  W.years66Walk(pack, null);
  for(const raw of (pack.gigs || [])) addPool(W.normalizeGigRecord(raw), 'pack');
}
const inj = [
  ...(W.ENTRY_GIGS_1988 || []), ...(W.WINTER_ENTRY_GIGS_88 || []), ...(W.WINTER_BRIDGE_GIGS_88 || []),
  ...(W.MID_GIGS_1988_35 || []), ...(W.SOFT_BRIDGE_GIGS_1988 || []), ...(W.INTEL_HIDDEN_GIGS || []),
  ...(W.FAVOR_DUE_GIGS || []), ...(W.RIVAL_FACEOFF_GIGS || []), ...(W.EXODUS_GIGS || []),
  W.WF3_LIAO_GIG, W.WF3_LIAO_HARVEST_GIG, ...(W.BR89_GIGS || []), ...(W.NAT92_GIGS || []),
];
for(const g of inj){ if(g && g.id) addPool(W.normalizeGigRecord(deepClone(g)), 'inj'); }
for(const y of Object.keys(W.GIGS36_BY_YEAR || {})){
  for(const g of (W.GIGS36_BY_YEAR[y] || [])){ if(g && g.id) addPool(W.normalizeGigRecord(deepClone(g)), 'gig36'); }
}
ok('A4 對照表 id 全部喺全池存在', Object.keys(FIX).every(id => pool.has(id)),
   Object.keys(FIX).filter(id => !pool.has(id)).join(','));
const G = id => pool.get(id);
const payOf = g => W.gigPayExact(g);
const daysOf = g => W.effectiveShootDays(g);
const dailyOf = g => { const p = payOf(g), d = daysOf(g); return (p != null && d) ? Math.round(p / d) : null; };

/* B 錨點 */
const ad08 = G('gig_1988_ad_08');
ok('B1 ad_08 片酬 1500', ad08 && payOf(ad08) === 1500, ad08 && String(payOf(ad08)));
ok('B2 ad_08 快照壓返背景級', ad08 && ad08.fame[1] <= 15 && ad08.popularity[1] <= 30,
   ad08 && (ad08.fame + '/' + ad08.popularity));
ok('B3 ad_08 違約金 830 < 片酬', ad08 && ad08.breachFee === 830 && ad08.breachFee < payOf(ad08));
const tv08 = G('gig_1988_tv_08');
ok('B4 tv_08 降格 variety_special／3 日／3600／tier 中',
   tv08 && W.resolveRoleScale(tv08) === 'variety_special' && daysOf(tv08) === 3 && payOf(tv08) === 3600 && tv08.tier === '中',
   tv08 && (W.resolveRoleScale(tv08) + '/' + daysOf(tv08) + '/' + payOf(tv08) + '/' + tv08.tier));
const recWH = G('gig_1988_rec_wanchai_winter_high');
ok('B5 主唱臨記改名專輯主唱', recWH && recWH.title === '《冬夜情歌通宵錄》專輯主唱' && !/臨記/.test(recWH.synopsis || ''),
   recWH && recWH.title);
ok('B6 主唱臨記片酬不變 24000（改名唔改價）', recWH && payOf(recWH) === 24000);
const tvKW = G('gig_1988_tv_kowloon_winter_high');
ok('B7 臨記男主改名男主角', tvKW && tvKW.title === '《九龍警網》男主角' && !/臨記男主/.test(tvKW.synopsis || ''),
   tvKW && tvKW.title);
ok('B9 gig_1991_film_04 14 日→2 日', daysOf(G('gig_1991_film_04')) === 2);
ok('B10 tv_06 替身雜務 30 日主角約→16 日 11000',
   daysOf(G('gig_1988_tv_06')) === 16 && payOf(G('gig_1988_tv_06')) === 11000);

/* C 名實守門（全池） */
const EXTRA_WORDS = ['臨記','群演','路人','背景','伴舞','企位','圍觀','充場','龍套','臨時演員','幫工','場務','群眾','替身','手替'];
const LEAD_WORDS = ['男主角','女主角','男主','女主','主唱','領銜','擔正','主角'];
const EXEMPT_IDS = new Set(['gig_exodus_tv_senior','gig_exodus_tv_kowloon','gig_exodus_film_hand']);
const LONGFORM_ALLOW = new Set(['gig_1988_tv_05','gig_1988_tv_06','gig_1988_tv_07',
  'gig_1988_film_harbour_winter_mid','gig_1988_film_harbour_winter_high','gig_1988_film_lion_autumn_high']);
function roleText(g){
  const suf = (g.title || '').split('》').pop() || '';
  return suf + '|' + (g.roleLabel || '');
}
let contra = [], overDaily = [], overSnap = [], overDays = [];
for(const g of pool.values()){
  const t = roleText(g);
  const hasExtra = EXTRA_WORDS.some(w => t.includes(w));
  const hasLead = LEAD_WORDS.some(w => t.includes(w));
  if(hasExtra && hasLead) contra.push(g.id);
  if(!hasExtra || g.softBridge || g.entryTier || EXEMPT_IDS.has(g.id)) continue;
  const isAd = g.type === '廣告' || ['ad_av','ad_print','photobook','ad_extra_day'].includes(W.resolveRoleScale(g));
  const cap = isAd ? 1600 : 1700;
  const d = dailyOf(g);
  if(d != null && d > cap) overDaily.push(g.id + ':' + d);
  const fm = Array.isArray(g.fame) ? (g.fame[0] + g.fame[1]) / 2 : 0;
  const pm = Array.isArray(g.popularity) ? (g.popularity[0] + g.popularity[1]) / 2 : 0;
  if(fm > 17 || pm > 33) overSnap.push(g.id + ':' + fm + '/' + pm);
  if(!LONGFORM_ALLOW.has(g.id) && daysOf(g) > 8) overDays.push(g.id + ':' + daysOf(g));
}
ok('C1 全池冇名銜自相矛盾（臨記＋主角類）', contra.length === 0, contra.join(','));
ok('C2 臨記類崗位日薪唔過上限', overDaily.length === 0, overDaily.join(','));
ok('C3 臨記類崗位快照唔過上限', overSnap.length === 0, overSnap.join(','));
ok('C4 臨記類崗位日數唔過 8（白名單除外）', overDays.length === 0, overDays.join(','));

/* D 豁免完整：softBridge 保底機制全家族冇俾人郁 */
const sb88 = [...pool.values()].filter(g => /^gig_1988_soft_bridge_/.test(g.id));
ok('D1 1988 softBridge 表 12 張在池', sb88.length === 12, 'n=' + sb88.length);
ok('D2 1988 softBridge 片酬全數 3700（保底機制冇郁）', sb88.every(g => payOf(g) === 3700),
   sb88.map(g => g.id + ':' + payOf(g)).join(','));
const brg36 = [...pool.values()].filter(g => /^g36_\d\d_brg_/.test(g.id));
ok('D3 gig36 橋接家族 18 張在池＋全數 softBridge 旗', brg36.length === 18 && brg36.every(g => g.softBridge),
   'n=' + brg36.length);
ok('D4 gig36 橋接 flat 年價冇郁（1991 批 4700／1992 批 5300）',
   brg36.every(g => payOf(g) === (g.id.startsWith('g36_89') ? 4700 : 5300)),
   brg36.map(g => g.id + ':' + payOf(g)).join(','));

/* E 冪等 */
let idemBad = [];
for(const id of Object.keys(FIX)){
  const g1 = G(id);
  const g2 = W.normalizeGigRecord(deepClone(g1));
  const fields = ['title','roleLabel','tier','roleScale','shootDaysHint','payExact','breachFee'];
  for(const f of fields){ if(JSON.stringify(g1[f]) !== JSON.stringify(g2[f])) idemBad.push(id + ':' + f); }
  if(JSON.stringify(g1.pay) !== JSON.stringify(g2.pay)) idemBad.push(id + ':pay');
  if(JSON.stringify(g1.fame) !== JSON.stringify(g2.fame)) idemBad.push(id + ':fame');
  if(JSON.stringify(g1.popularity) !== JSON.stringify(g2.popularity)) idemBad.push(id + ':popularity');
  if(JSON.stringify(g1.req) !== JSON.stringify(g2.req)) idemBad.push(id + ':req');
  if(payOf(g1) !== payOf(g2) || daysOf(g1) !== daysOf(g2)) idemBad.push(id + ':eff');
}
ok('E1 NAME93 冪等（二次 normalize 唔變、唔俾 DUR90 覆寫）', idemBad.length === 0, idemBad.join(','));

/* F 改名冇撞名 */
const titleCount = {};
for(const g of pool.values()) titleCount[g.title] = (titleCount[g.title] || 0) + 1;
const renamed = Object.keys(FIX).filter(id => FIX[id].title);
ok('F1 改名 9 張新標題全池冇重複', renamed.length === 9 && renamed.every(id => titleCount[G(id).title] === 1),
   renamed.map(id => G(id).title + '×' + titleCount[G(id).title]).join(' | '));

/* G 期限 */
let ddlBad = [];
for(const id of Object.keys(FIX)){
  const g = G(id), days = daysOf(g);
  const wds = W.effectiveShootWeekdays(g);
  const wdCount = Array.isArray(wds) ? new Set(wds.map(Number)).size : 5;
  const need = Math.ceil(days * 7 / Math.max(1, wdCount));
  const ddl = W.effectiveShootDeadlineDays(g, days);
  if(ddl < need) ddlBad.push(id + ':ddl' + ddl + '<need' + need);
}
ok('G1 43 張 deadline ≥ 拍完所需日曆日', ddlBad.length === 0, ddlBad.join(','));

console.log(fails ? ('FAILURES: ' + fails) : 'ALL PASS');
process.exit(fails ? 1 : 0);
