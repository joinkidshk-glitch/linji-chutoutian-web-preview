// v20a320：彭少祺好收尾 finale 派 gig_1991_variety_203《台慶大騷》台上助理
//   pang_finale grants() 加 grant229Record（草稿 L1545；跟 luk_tease v271 前例）。
//   (1) 靜態：finale grants 派 variety_203、閘＋對白逐字唔郁、冷版唔派、n17 兩行唔郁、
//       variety_203 trigger／BR89 唔郁、計數 323／38／27／BR89 19、無 GRANT229 死 code 行；
//   (2) 行為：grants() 一次記低（聽日到期）、第二次唔重複、簽約金三成、
//       殺青標 redeemedBy＋variety_106 落板、已兌現唔重標、grant229IsConsumed 跳過、
//       n17 雲吞麵照派 ad_107 共存。
// 用法：node tests/test_r320_pang_finale_dispatch.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const GIGS_NEW = require('../content/gigs_new.json');
const GIGS = Array.isArray(GIGS_NEW) ? GIGS_NEW : (GIGS_NEW.gigs || []);
const gigById = (id) => GIGS.find(g => g && g.id === id) || null;
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }
function extractFn(name){
  const i = html.indexOf('function ' + name + '(');
  if(i < 0) throw new Error('fn not found: ' + name);
  let depth = 0, j = html.indexOf('{', i);
  for(; j < html.length; j++){
    if(html[j] === '{') depth++;
    else if(html[j] === '}'){ depth--; if(depth === 0) break; }
  }
  return html.slice(i, j + 1);
}
function extractConst(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('const not found: ' + name);
  let depth = 0, started = false, j = i;
  for(; j < html.length; j++){
    const c = html[j];
    if(c === '{' || c === '['){ depth++; started = true; }
    else if(c === '}' || c === ']'){ depth--; if(started && depth === 0){ j++; break; } }
    else if(c === ';' && !started) { j++; break; }
  }
  return html.slice(i, j);
}
function extractDlg(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('missing ' + name);
  const j = html.indexOf('\nconst ', i + 10);
  return html.slice(i, j < 0 ? undefined : j);
}

/* ---- (1) 靜態 ---- */
const FINALE_GATE = 'enc79TierOf(st.fav)>=3 && ys.year===1992 && ys.season==="冬" && (st.beatsDone||{}).pang_n17 && (S.flags||{}).pang_cover_night && (S.flags||{}).pang_listened && (S.flags||{}).pang_noodle_night';
ok('靜態：pang_finale grants() 派 variety_203（彭少祺支線）', html.includes('grant229Record("gig_1991_variety_203", "彭少祺支線"'));
ok('靜態：pang_finale 閘逐字唔郁', html.includes('{ id:"pang_finale", when(st){ const ys=yearSeasonNow(); return ' + FINALE_GATE + '; }'));
ok('靜態：pang_finale_cold 無 grant229Record（冷版唔派）', (() => {
  const i = html.indexOf('{ id:"pang_finale_cold"');
  const j = html.indexOf('{ id:"pang_finale"', i + 10);
  return i >= 0 && j > i && !html.slice(i, j).includes('grant229Record');
})());
ok('靜態：n17 GRANT229 兩行唔郁（雲吞麵→ad_107／返屋企瞓→tv_301）',
  html.includes('{ seg:"beat:pang_n17", key:"雲吞麵", gigId:"gig_1991_ad_107"') &&
  html.includes('{ seg:"beat:pang_n17", key:"返屋企瞓", gigId:"gig_1992_tv_301"'));
ok('靜態：無 GRANT229_ENC79 死 code 行（seg beat:pang_finale）', !html.includes('seg:"beat:pang_finale"'));
const v203 = gigById('gig_1991_variety_203');
ok('靜態：variety_203 trigger／storyKeys 唔郁', !!v203 && v203.trigger && v203.trigger.kind === 'credit' && v203.trigger.creditId === 'credit_enc84_pang_patron' && v203.trigger.creditOwner === '彭少祺' && Array.isArray(v203.storyKeys) && v203.storyKeys[0] === 'pang_siuki');
ok('靜態：BR89 第 18 對在位（variety_203＋variety_106 同一筆債權）',
  html.includes('gig_1991_variety_203:"credit_enc84_pang_patron"') &&
  html.includes('gig_1992_variety_106:"credit_enc84_pang_patron"'));
ok('靜態：庫 323 張／trigger 38／credit 27', GIGS.length === 323 &&
  GIGS.filter(g => g && g.trigger).length === 38 &&
  GIGS.filter(g => g && g.trigger && g.trigger.kind === 'credit').length === 27);

/* ---- (2) 行為：抽 live code＋stub ---- */
let S;
function resetS(day){
  S = { dayIndex: day || 0, fame: 0, money: 2000, flags: {}, npcs: { agent: 0 }, mockRumors: [], mockDebts: [], mockCredits: [], board: {}, shoots: [], pendingAud: [], booked: [], mapTips: {}, story: { flags: {} }, starWeek: {}, weekGigsDone: 0, starWhispers: {}, grant229Queue: [], contracts229: [] };
}
function syncNotebookMirror(){}
function saveQ(){}
/* GRANT229 派發 stub（照 live grant229Record 語義：聽日到期、一生一次） */
function grant229Record(gigId, source, reason){
  try{
    if(!gigId || !S) return false;
    if(S.flags["grant229_recorded_" + gigId]) return false;
    S.flags["grant229_recorded_" + gigId] = 1;
    if(!Array.isArray(S.grant229Queue)) S.grant229Queue = [];
    S.grant229Queue.push({ gigId: String(gigId), source: String(source || ""), reason: String(reason || ""), dueDay: (S.dayIndex | 0) + 1, recordedDay: (S.dayIndex | 0) });
    return true;
  }catch(_e){ return false; }
}
var BR89_GIGS = [];
function extractBeatsAssign(sid){
  const start = html.indexOf('ENC79_BEATS.' + sid + ' = [');
  if(start < 0) throw new Error('beats assign not found: ' + sid);
  const next = html.indexOf('ENC79_BEATS.', start + 20);
  return html.slice(start, next < 0 ? undefined : next);
}
const asVar = (code, name) => code.replace('const ' + name + ' =', 'var ' + name + ' =');
eval(asVar(extractConst('ENC79_BEATS'), 'ENC79_BEATS') + '\n' +
  asVar(extractConst('BR89_PATRON_OF_GIG'), 'BR89_PATRON_OF_GIG') + '\n' +
  asVar(extractConst('GRANT229_ENC79'), 'GRANT229_ENC79') + '\n' +
  asVar(extractDlg('ENC84_DLG_pang_siuki'), 'ENC84_DLG_pang_siuki'));
eval(extractBeatsAssign('pang_siuki'));
eval(['br89HasCredit', 'br89GigOn', 'triggerGigOn', 'br89OnGigComplete', 'grant229IsConsumed', 'grant229RecordFromEnc79', 'grant229HireTerms', 'gigPayExact', 'grant229Mid'].map(extractFn).join('\n'));
function beatOf(sid, id){ return (ENC79_BEATS[sid] || []).find(b => b.id === id); }
function holdPangPatron(redeemedBy){
  const c = { id: 'credit_enc84_pang_patron', debtor: '彭少祺', title: '司儀引薦', status: '未收' };
  if(redeemedBy) c.redeemedBy = redeemedBy;
  S.mockCredits = [c];
  return c;
}
const fin = beatOf('pang_siuki', 'pang_finale');
const finCold = beatOf('pang_siuki', 'pang_finale_cold');

ok('行為：finale DLG 7 句、第 6 句承諾逐字唔郁', (() => {
  const d = ENC84_DLG_pang_siuki.beats.pang_finale;
  return d && Array.isArray(d.lines) && d.lines.length === 7 &&
    d.lines[5][1] === '聽日，台慶大騷嗰邊爭個台上助理，我同監製講咗聲，你去試下。' &&
    !d.choices;
})());
ok('行為：冷版 finale 無 grants（乜都唔派）', !!finCold && typeof finCold.grants !== 'function');
ok('行為：finale grants() 行一次 → queue 有 variety_203、dueDay＝聽日', (() => {
  resetS(100);
  const r = fin.grants();
  const q = S.grant229Queue;
  return q.length === 1 && q[0].gigId === 'gig_1991_variety_203' && q[0].source === '彭少祺支線' &&
    q[0].dueDay === 101 && q[0].recordedDay === 100 && q[0].reason.indexOf('台慶大騷') >= 0;
})());
ok('行為：finale grants() 行第二次 → 唔重複記低（一生一次）', (() => {
  resetS(100);
  fin.grants(); fin.grants();
  return S.grant229Queue.length === 1 && S.grant229Queue[0].gigId === 'gig_1991_variety_203';
})());
ok('行為：派發條款——簽約金＝pay 中位數三成（220→66）', (() => {
  const t = grant229HireTerms(gigById('gig_1991_variety_203'));
  return !!t && t.pay === 220 && t.signPay === 66 && !t.contract;
})());
ok('行為：殺青 variety_203 → 債權標 redeemedBy、variety_106 落板', (() => {
  resetS(100);
  holdPangPatron(null);
  if(!triggerGigOn(gigById('gig_1992_variety_106'))) return false; // 兌現前上板
  if(!triggerGigOn(gigById('gig_1991_variety_203'))) return false;
  br89OnGigComplete('gig_1991_variety_203');
  const c = S.mockCredits[0];
  return c.redeemedBy === 'gig_1991_variety_203' &&
    !triggerGigOn(gigById('gig_1992_variety_106')) &&
    !triggerGigOn(gigById('gig_1991_variety_203'));
})());
ok('行為：殺青再標一次 → 唔重標（冪等）', (() => {
  resetS(100);
  holdPangPatron(null);
  br89OnGigComplete('gig_1991_variety_203');
  const line1 = S.mockCredits[0].line;
  br89OnGigComplete('gig_1991_variety_203');
  return S.mockCredits[0].redeemedBy === 'gig_1991_variety_203' && S.mockCredits[0].line === line1;
})());
ok('行為：債權已用 variety_106 兌現 → finale 照派 variety_203（新機會），殺青唔重標', (() => {
  resetS(100);
  holdPangPatron('gig_1992_variety_106');
  fin.grants();
  if(S.grant229Queue.length !== 1 || S.grant229Queue[0].gigId !== 'gig_1991_variety_203') return false;
  br89OnGigComplete('gig_1991_variety_203');
  return S.mockCredits[0].redeemedBy === 'gig_1992_variety_106';
})());
ok('行為：grant229IsConsumed——已做／已獲聘／等消息／已預約跳過，乾淨唔跳', (() => {
  resetS(100);
  if(grant229IsConsumed('gig_1991_variety_203')) return false;
  S.flags['done_gig_1991_variety_203'] = 1;
  if(!grant229IsConsumed('gig_1991_variety_203')) return false;
  delete S.flags['done_gig_1991_variety_203'];
  S.shoots = [{ gigId: 'gig_1991_variety_203' }];
  if(!grant229IsConsumed('gig_1991_variety_203')) return false;
  S.shoots = []; S.pendingAud = [{ gigId: 'gig_1991_variety_203' }];
  if(!grant229IsConsumed('gig_1991_variety_203')) return false;
  S.pendingAud = []; S.booked = [{ gigId: 'gig_1991_variety_203' }];
  if(!grant229IsConsumed('gig_1991_variety_203')) return false;
  return true;
})());
ok('行為：共存——n17 揀 A 照派 ad_107（另一條 queue、更早 dueDay）', (() => {
  resetS(100);
  const r1 = grant229RecordFromEnc79('beat:pang_n17', '雲吞麵');
  if(!r1) return false;
  if(S.grant229Queue.length !== 1 || S.grant229Queue[0].gigId !== 'gig_1991_ad_107' || S.grant229Queue[0].dueDay !== 101) return false;
  S.dayIndex = 101; // finale 播出嗰晚（n17 之後一日）
  fin.grants();
  return S.grant229Queue.length === 2 && S.grant229Queue[1].gigId === 'gig_1991_variety_203' && S.grant229Queue[1].dueDay === 102;
})());
ok('行為：共存——n17 揀 B 派 tv_301，冷版 finale 乜都唔派', (() => {
  resetS(100);
  const r1 = grant229RecordFromEnc79('beat:pang_n17', '返屋企瞓');
  return !!r1 && S.grant229Queue.length === 1 && S.grant229Queue[0].gigId === 'gig_1992_tv_301' &&
    typeof finCold.grants !== 'function';
})());
ok('行為：BR89 映射 19 對', Object.keys(BR89_PATRON_OF_GIG).length === 19);

console.log('\n' + (fails.length ? 'FAIL: ' + fails.join(' | ') : 'R320 PANG FINALE DISPATCH: ALL PASS'));
if(fails.length) process.exit(1);
