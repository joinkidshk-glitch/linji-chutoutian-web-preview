// v20a307 B1：10 張玩家主唱唱片 gig singer／singerGender 改 null＋補 4 張真唱片通告
//   (A) 10 張 singer／singerGender 係 null，其他欄（title／pay／tier／season／year／category）唔郁
//   (B) 4 張新 gig 在位、必填欄齊、category 作品、歌手正確、玩家唔係主唱（配唱／MV 男主角）
//   (C) awards63Fellows 口徑：1990／1991／1992 男歌手格各返 3 個；女歌手格唔郁；新人獎各 3 個男女齊
//   (D) 庫總數 330 張、id 唯一、按年 130／105／87；1990 冬 41 張（v324＋A）；1990 高級仍 1 張 film_304
//   (E) 魏詠男唔入任何唱片格；新名唔含年份數字；新作品名唔撞現庫
//   註：brief 原擬補 3 張（1990×2＋1991×1），live 覆核發現 1992 男歌手格實際係 3→2——
//   程天諾（ching_tinlok）唔入 POSTER59_STAR_IDS，awards63HasSprite 濾走佢，唔計數；
//   所以 1992 要多補 1 張（lok_gasing），共 4 張，庫 302→306。
// 用法：node tests/test_r307_record_singer_null.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
let fails = 0;
function ok(name, cond, extra){
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : ''));
  if(!cond) fails++;
}
const pack = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gigs_new.json'), 'utf8'));
const gigs = pack.gigs || [];
const byId = {};
gigs.forEach(g=>{ byId[g.id] = g; });

/* ---------- A：10 張改 null＋其他欄唔郁 ---------- */
const NULL10 = { /* v390：pay ×1.4 */
  'gig_1990_rec_106': ['《節拍飛揚》快歌男主唱', '初級', '夏', [168, 202]],
  'gig_1990_rec_107': ['《燃燒青春》大碟主唱', '初級', '秋', [756, 945]],
  'gig_1990_rec_109': ['《不羈少年》新人單曲主唱', '初級', '春', [252, 302]],
  'gig_1990_rec_110': ['《白頭相守》大碟主唱', '中級', '冬', [1386, 1663]],
  'gig_1991_rec_105': ['《風雨搖滾路》搖滾主唱', '初級', '春', [756, 945]],
  'gig_1991_rec_107': ['《情濃款款》大碟主唱', '中級', '秋', [1386, 1663]],
  'gig_1991_rec_108': ['《全城狂歡夜》大碟主唱', '中級', '冬', [1386, 1663]],
  'gig_1992_rec_102': ['《硬漢柔情》新人搖滾主唱', '初級', '夏', [252, 302]],
  'gig_1992_rec_105': ['《當年情懷》大碟主唱', '中級', '春', [1386, 1663]],
  'gig_1992_rec_109': ['《熱血狂奔》大碟主唱', '高級', '冬', [2800, 3360]],
};
const nullBad = Object.keys(NULL10).filter(id=>{
  const g = byId[id];
  if(!g) return true;
  const w = NULL10[id];
  return g.singer !== null || g.singerGender !== null ||
    g.title !== w[0] || g.tier !== w[1] || g.season !== w[2] ||
    JSON.stringify(g.pay) !== JSON.stringify(w[3]) ||
    g.category !== '作品' || g.type !== '唱片通告';
});
ok('A 10 張 singer／singerGender 係 null、其餘欄唔郁', nullBad.length === 0, nullBad.join(','));

/* ---------- B：4 張新 gig ---------- */
const NEW_IDS = ['gig_1990_rec_114', 'gig_1990_rec_115', 'gig_1991_rec_113', 'gig_1992_rec_112'];
const WANT_NEW = {
  'gig_1990_rec_114': ['luk_baakyin', 'M', '《星光閃耀》MV 男主角', '中級', '秋'],
  'gig_1990_rec_115': ['lok_gasing', 'M', '《風中勁草》配唱歌手', '初級', '夏'],
  'gig_1991_rec_113': ['lok_gasing', 'M', '《午夜快車》配唱歌手', '初級', '冬'],
  'gig_1992_rec_112': ['lok_gasing', 'M', '《追風少年》MV 男主角', '中級', '春'],
};
ok('B 4 張新 gig 全部在位', NEW_IDS.every(id=>!!byId[id]),
   NEW_IDS.filter(id=>!byId[id]).join(','));
const newBad = NEW_IDS.filter(id=>{
  const g = byId[id];
  if(!g) return true;
  const w = WANT_NEW[id];
  return g.singer !== w[0] || g.singerGender !== w[1] || g.title !== w[2] ||
    g.tier !== w[3] || g.season !== w[4] || g.category !== '作品' || g.type !== '唱片通告';
});
ok('B 新 gig 歌手／title／tier／season 同設計表一致', newBad.length === 0, newBad.join(','));
const BASE = ['title', 'type', 'tier', 'category', 'loc', 'year', 'season', 'days', 'pay', 'req', 'fame', 'blurb', 'synopsis', 'roleHint'];
const missingBase = [];
NEW_IDS.forEach(id=>{
  const g = byId[id];
  if(!g) return;
  BASE.forEach(k=>{ if(g[k] === undefined || g[k] === null || g[k] === '') missingBase.push(id + ':' + k); });
  if(!g.posterBrief) missingBase.push(id + ':posterBrief');
  if(!g.workTitle || !g.roleLabel) missingBase.push(id + ':workTitle/roleLabel');
});
ok('B 新 gig 必填欄齊（連 posterBrief）', missingBase.length === 0, missingBase.slice(0, 5).join(','));
const playerLead = NEW_IDS.filter(id=>{
  const g = byId[id];
  return g && /主唱/.test(g.roleLabel || '');
});
ok('B 新 gig 玩家唔係主唱（配唱／MV 男主角）', playerLead.length === 0, playerLead.join(','));

/* ---------- C：awards63Fellows 口徑重計（同 test_gig291 W3 做法） ---------- */
function extractConst(name){
  for(const kw of ['const ', 'var ']){
    const i = html.indexOf(kw + name + ' =');
    if(i < 0) continue;
    let depth = 0, started = false;
    for(let k = i; k < html.length; k++){
      const ch = html[k];
      if(ch === '{' || ch === '['){ depth++; started = true; }
      else if(ch === '}' || ch === ']'){ depth--; if(started && depth === 0) return html.slice(i, k + 1) + ';'; }
      else if(ch === ';' && !started) return html.slice(i, k + 1);
    }
  }
  return null;
}
const POSTER59_STAR_IDS = (()=>{
  const s = extractConst('POSTER59_STAR_IDS') || '';
  const o = {};
  const m = s.match(/"([^"]+)":\s*("[^"]*"|null)/g) || [];
  m.forEach(kv=>{
    const mm = kv.match(/"([^"]+)":\s*("[^"]*"|null)/);
    if(mm) o[mm[1]] = mm[2] === 'null' ? null : mm[2].replace(/"/g, '');
  });
  return o;
})();
const sprite = new Set(Object.values(POSTER59_STAR_IDS).filter(Boolean));
ok('C 程天諾無 sprite（1992 要補第 4 張嘅原因）', !sprite.has('ching_tinlok'));
function payOf(g){ return Array.isArray(g.pay) ? (Number(g.pay[1] != null ? g.pay[1] : g.pay[0]) || 0) : (Number(g.pay) || 0); }
function top3(year, gender){
  const cands = [];
  gigs.forEach(g=>{
    if(g.year !== year || (g.category && g.category !== '作品')) return;
    if(g.type !== '唱片通告') return;
    const starId = String(g.singer || '');
    if(!starId) return;
    if(gender && String(g.singerGender || '').toLowerCase() !== gender) return;
    if(!sprite.has(starId)) return;
    cands.push({ pay: payOf(g), id: g.id, starId });
  });
  cands.sort((a, b)=>(b.pay - a.pay) || (a.id < b.id ? -1 : (a.id > b.id ? 1 : 0)));
  const used = {}, out = [];
  cands.forEach(c=>{ if(out.length >= 3 || used[c.starId]) return; used[c.starId] = true; out.push(c.starId); });
  return out;
}
function eqSet(a, b){ return a.length === b.length && a.slice().sort().join(',') === b.slice().sort().join(','); }
ok('C 1990 男歌手格返 3 個（顧明輝＋駱家聲＋陸柏言）',
   eqSet(top3(1990, 'm'), ['gu_mingfai', 'lok_gasing', 'luk_baakyin']), top3(1990, 'm').join(','));
ok('C 1991 男歌手格返 3 個（駱家聲＋陸柏言＋廖炳星）',
   eqSet(top3(1991, 'm'), ['lok_gasing', 'luk_baakyin', 'liu_bingxing']), top3(1991, 'm').join(','));
ok('C 1992 男歌手格返 3 個（陸柏言＋駱家聲＋顧明輝）',
   eqSet(top3(1992, 'm'), ['luk_baakyin', 'lok_gasing', 'gu_mingfai']), top3(1992, 'm').join(','));
ok('C 1990 女歌手格唔郁（沈映雪＋韓秀婷＋藍若曦）',
   eqSet(top3(1990, 'f'), ['shum_yingsuet', 'hon_sauting', 'lan_ruoxi']), top3(1990, 'f').join(','));
ok('C 1991 女歌手格唔郁（沈映雪＋藍若曦＋蘇芷茵）',
   eqSet(top3(1991, 'f'), ['shum_yingsuet', 'lan_ruoxi', 'so_jiyan']), top3(1991, 'f').join(','));
ok('C 1992 女歌手格唔郁（藍若曦＋蘇芷茵＋韓秀婷）',
   eqSet(top3(1992, 'f'), ['lan_ruoxi', 'so_jiyan', 'hon_sauting']), top3(1992, 'f').join(','));
[1990, 1991, 1992].forEach(y=>{
  const nc = top3(y, '');
  ok('C ' + y + ' 新人獎 3 個、男女齊', nc.length === 3 &&
     nc.some(id=>['gu_mingfai', 'lok_gasing', 'luk_baakyin', 'liu_bingxing'].indexOf(id) >= 0) &&
     nc.some(id=>['shum_yingsuet', 'hon_sauting', 'lan_ruoxi', 'so_jiyan'].indexOf(id) >= 0),
     nc.join(','));
});

/* ---------- D：總數／按年／冬季／高級 ---------- */
ok('D 庫總數 330 張、id 唯一', gigs.length === 330 && new Set(gigs.map(g=>g.id)).size === 330,
   'n=' + gigs.length);
ok('D 按年 1990:130／1991:110／1992:90',
   gigs.filter(g=>g.year === 1990).length === 130 &&
   gigs.filter(g=>g.year === 1991).length === 110 &&
   gigs.filter(g=>g.year === 1992).length === 90,
   [1990, 1991, 1992].map(y=>gigs.filter(g=>g.year === y).length).join('/'));
const w90 = gigs.filter(g=>g.year === 1990 && g.season === '冬');
ok('D 1990 冬 41 張', w90.length === 41, 'n=' + w90.length);
const high1990 = gigs.filter(g=>g.year === 1990 && (g.tier === '高級' || g.tier === '稀有'));
ok('D 1990 年高級仍 1 張（film_304）', high1990.length === 1 && high1990[0].id === 'gig_1990_film_304',
   high1990.map(g=>g.id).join(','));

/* ---------- E：硬規則 ---------- */
const ngaiRec = gigs.filter(g=>g.type === '唱片通告' && g.singer === 'ngai_wingnaam');
ok('E 魏詠男唔入任何唱片格', ngaiRec.length === 0, ngaiRec.map(g=>g.id).join(','));
const yearInName = NEW_IDS.filter(id=>/\d/.test(byId[id].workTitle || '') || /\d/.test(byId[id].title || ''));
ok('E 新名唔含年份數字', yearInName.length === 0, yearInName.join(','));
const dupTitle = NEW_IDS.filter(id=>{
  const g = byId[id];
  if(!g.workTitle) return false;
  return gigs.some(o=>o.id !== id && o.workTitle === g.workTitle);
});
ok('E 新作品名唔撞現庫', dupTitle.length === 0, dupTitle.join(','));

console.log(fails === 0 ? 'ALL PASS' : fails + ' FAIL');
process.exit(fails === 0 ? 0 : 1);
