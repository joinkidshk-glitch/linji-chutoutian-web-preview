// S-30v2 更新版・邏輯測試（老闆對照表＋通告期間拆行）
// 跟 repo 測試慣例：由 patched index.html 抽函數＋const，Node 沙盒 eval。
// 覆蓋：期間行只留季節／檔期窗；期限獨立行；工作天刪走；castWindow／不限／全年邊界；
//      11 間對照表 key＝g.loc；未映射 loc → 何生後備。
// v20a111 S-30v2：老闆對照表＋通告期間拆行・守門測試
// 用法：node tests/test_s30v2upd_logic.js（讀 repo 內 index.html；亦接受 argv[1] 覆寫路徑）
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(process.argv[2] || path.join(__dirname, '..', 'index.html'), 'utf8');
function extractFn(name){
  const i = html.indexOf('function ' + name + '(');
  if (i < 0) throw new Error('fn not found: ' + name);
  let depth = 0, j = html.indexOf('{', i);
  for (; j < html.length; j++){ if (html[j] === '{') depth++; else if (html[j] === '}'){ depth--; if (depth === 0) break; } }
  return html.slice(i, j + 1);
}
function extractConst(name){
  const i = html.indexOf('const ' + name + ' =');
  if (i < 0) throw new Error('const not found: ' + name);
  let depth = 0, started = false;
  for (let k = i; k < html.length; k++){
    const ch = html[k];
    if (ch === '{' || ch === '['){ depth++; started = true; }
    else if (ch === '}' || ch === ']'){ depth--; if (started && depth === 0) return html.slice(i, k + 1) + ';'; }
    else if (ch === ';' && !started) return html.slice(i, k + 1);
  }
  throw new Error('const end not found: ' + name);
}
let fails = 0;
function ok(name, cond, extra){
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : ''));
  if (!cond) fails++;
}

/* ---------- 沙盒 stub（只補 period／deadline／resolver 依賴） ---------- */
function R(a){ return a; }
function clamp(v, lo, hi){ return Math.min(hi, Math.max(lo, v)); }
function calendarYear(){ return 1990; }
function gigApplyDeadlineDays(g){
  if(!g || typeof g.applyDeadlineDays !== 'number' || !Number.isFinite(g.applyDeadlineDays) || g.applyDeadlineDays < 0) return null;
  return Math.max(0, Math.round(g.applyDeadlineDays));
}
function gigApplyDeadlineText(g){
  const n = gigApplyDeadlineDays(g);
  if (n == null) return '';
  return '仲有 ' + n + ' 日截止';
}
for (const c of ['SHOOT_DAYS', 'ROLE_SCALE_BAND', 'GIG_ISSUER_FIGURE_MAP30V2'])
  eval(extractConst(c).replace('const ' + c + ' =', 'var ' + c + ' ='));
for (const f of ['resolveRoleScale', 'shootBandFor', 'effectiveShootDays',
                 'effectiveShootDeadlineDays', 'gigCastPeriodLine',
                 'gigCastDeadlineText30v2', 'gigIssuerFigure30v2'])
  eval(extractFn(f));

const winter = { year: 1990, season: '冬', shootDaysHint: 1, shootDeadlineDays: 10 };
ok('period: 冬季檔只留季節', gigCastPeriodLine(winter) === '1990年冬季檔',
   JSON.stringify(gigCastPeriodLine(winter)));
ok('period: 無獲聘後', !gigCastPeriodLine(winter).includes('獲聘後'));
ok('period: 無工作天', !gigCastPeriodLine(winter).includes('工作天'));
ok('deadline: 獲聘後 10 日內', gigCastDeadlineText30v2(winter) === '獲聘後 10 日內',
   JSON.stringify(gigCastDeadlineText30v2(winter)));
ok('period: castWindow 保留範圍寫法',
   gigCastPeriodLine({ castWindow: { startHint: '1月上旬', endHint: '2月下旬', weeks: 6 } })
     === '1月上旬 ～ 2月下旬，共 6 週');
ok('period: 季節不限 → 1990年通告檔',
   gigCastPeriodLine({ season: '不限', shootDaysHint: 2, shootDeadlineDays: 14 }) === '1990年通告檔');
ok('period: 季節全年 → 1990年通告檔',
   gigCastPeriodLine({ season: '全年', shootDaysHint: 2, shootDeadlineDays: 14 }) === '1990年通告檔');
ok('period: castWindow＋ddl 齊晒，期間唔黐期限',
   gigCastPeriodLine({ castWindow: { startHint: '1月上旬', endHint: '2月下旬' }, shootDeadlineDays: 10 })
     === '1月上旬 ～ 2月下旬'
   && gigCastDeadlineText30v2({ castWindow: { startHint: '1月上旬', endHint: '2月下旬' }, shootDeadlineDays: 10 })
     === '獲聘後 10 日內');
// 邊界實錄：effectiveShootDeadlineDays 有 fallback（max(14, d*3)），故空 gig 都有期限數；
// 「冇 ddl 隱藏行」係防禦分支（真實 149 張通告全部有 shootDeadlineDays）。
const emptyDdl = gigCastDeadlineText30v2({});
console.log('INFO deadline({}) =', JSON.stringify(emptyDdl), '（fallback 語義，見註）');
ok('deadline: 空 gig 不 throw', typeof emptyDdl === 'string');

for (const loc of ['tvb_longmen', 'film_lion', 'ad_adm', 'ad_central', 'rec_hk', 'tvb_kowloon',
               'film_cotton', 'rec_wanchai', 'tvb_harbour', 'film_harbour', 'rec_star']) {
  ok('asset: boss_' + loc + '_base.webp 已入庫',
     fs.existsSync(path.join(__dirname, '..', 'assets', 'story', 'fullbody', 'boss_' + loc + '_base.webp')));
}
ok('asset: ho_sang_base.webp（何生後備）存在',
   fs.existsSync(path.join(__dirname, '..', 'assets', 'story', 'fullbody', 'ho_sang_base.webp')));
const EXPECT = {
  tvb_longmen: ['沈卓衡', '星河電視台', '台長'],
  film_lion: ['羅勁威', '獅子山製片', '老闆'],
  ad_adm: ['方樂怡', '金鐘創意', '老闆'],
  ad_central: ['霍君豪', '中環廣告', '老闆'],
  rec_hk: ['伍兆昌', '香江唱片', '老闆'],
  tvb_kowloon: ['陶映紅', '九龍電視台', '台長'],
  film_cotton: ['鄭伯康', '紅棉影業', '老闆'],
  rec_wanchai: ['梁廣成', '灣仔唱片', '老闆'],
  tvb_harbour: ['顧學禮', '海港廣播', '台長'],
  film_harbour: ['夏文心', '維港電影', '老闆'],
  rec_star: ['溫子峰', '天星音樂', '老闆'],
};
ok('map: 11 間', Object.keys(GIG_ISSUER_FIGURE_MAP30V2).length === 11);
for (const [loc, [name, org, role]] of Object.entries(EXPECT)){
  const f = gigIssuerFigure30v2({ loc });
  ok('map: ' + loc + ' → ' + name,
     f && f.name === name && f.org === org && f.role === role
     && f.src === 'assets/story/fullbody/boss_' + loc + '_base.webp?v=20a106',
     JSON.stringify(f));
}
const ho = gigIssuerFigure30v2({ loc: 'cafe_cha' });
ok('fallback: 未映射 loc → 何生',
   ho && ho.name === '何生' && ho.org === '何生事務所' && ho.role === '你的經理人',
   JSON.stringify(ho));
ok('fallback: 無 loc → 何生', gigIssuerFigure30v2({}).name === '何生');
ok('fallback: null gig → 何生', gigIssuerFigure30v2(null).name === '何生');
console.log(fails === 0 ? 'ALL PASS' : fails + ' FAIL');
process.exit(fails ? 1 : 0);
