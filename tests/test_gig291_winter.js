// v20a291 Q3：補 1990 冬開局通告・新通告測試
//   W0 13 張新通告在位、id 唯一、新格式、年份／季節／tier 正確
//   W1 必填欄齊（按類型：作品有 posterBrief；影視廣告有 cast 四格；唱片有 singer；綜藝有 host）
//   W2 1990 冬 40 張、開局可接 18 張（req ≤ 開局數值）
//   W3 獎項提名人收集零變動：1990 年各格頭三名同舊庫一致（按 awards63Fellows 口徑重計）
//   W4 魏詠男唔入任何唱片格；新通告無 trigger；新名唔含年份數字
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

const NEW_IDS = [
  'gig_1990_film_302', 'gig_1990_film_303', 'gig_1990_film_304', 'gig_1990_film_305',
  'gig_1990_tv_302', 'gig_1990_tv_303', 'gig_1990_tv_304',
  'gig_1990_ad_302', 'gig_1990_ad_303',
  'gig_1990_rec_302', 'gig_1990_rec_303',
  'gig_1990_variety_302', 'gig_1990_variety_303'
];
const WANT = {
  'gig_1990_film_302': ['初級', '作品'], 'gig_1990_film_303': ['中級', '作品'],
  'gig_1990_film_304': ['高級', '臨記通告'], 'gig_1990_film_305': ['臨記', '臨記通告'],
  'gig_1990_tv_302': ['初級', '作品'], 'gig_1990_tv_303': ['初級', '作品'],
  'gig_1990_tv_304': ['中級', '作品'],
  'gig_1990_ad_302': ['初級', '作品'], 'gig_1990_ad_303': ['初級', '臨記通告'],
  'gig_1990_rec_302': ['初級', '作品'], 'gig_1990_rec_303': ['中級', '作品'],
  'gig_1990_variety_302': ['初級', '作品'], 'gig_1990_variety_303': ['初級', '作品']
};

/* ---------- W0：在位＋唯一＋格式＋年份／季節／tier ---------- */
ok('W0 13 張新通告全部在位', NEW_IDS.every(id=>!!byId[id]),
   NEW_IDS.filter(id=>!byId[id]).join(','));
ok('W0 全庫 id 唯一（306 張）', gigs.length === 306 && new Set(gigs.map(g=>g.id)).size === 306,
   'n=' + gigs.length);
const badId = NEW_IDS.filter(id=>!/^gig_(1990|1991|1992)_[a-z]+_\d{3}$/.test(id));
ok('W0 新 id 全部新格式', badId.length === 0, badId.join(','));
const badYS = NEW_IDS.filter(id=>{ const g = byId[id]; return !g || g.year !== 1990 || g.season !== '冬'; });
ok('W0 新通告全部 year 1990、season 冬', badYS.length === 0, badYS.join(','));
const badTier = NEW_IDS.filter(id=>{ const g = byId[id]; return !g || g.tier !== WANT[id][0] || g.category !== WANT[id][1]; });
ok('W0 新通告 tier／category 同設計表一致', badTier.length === 0, badTier.join(','));

/* ---------- W1：必填欄 ---------- */
const BASE = ['title', 'type', 'tier', 'category', 'loc', 'year', 'season', 'days', 'pay', 'req', 'fame', 'blurb', 'synopsis', 'roleHint'];
const missingBase = [];
NEW_IDS.forEach(id=>{
  const g = byId[id];
  BASE.forEach(k=>{ if(g[k] === undefined || g[k] === null || g[k] === '') missingBase.push(id + ':' + k); });
});
ok('W1 新通告基本欄齊', missingBase.length === 0, missingBase.slice(0, 5).join(','));
const noBrief = NEW_IDS.filter(id=>byId[id].category === '作品' && !byId[id].posterBrief);
ok('W1 新作品全部有 posterBrief', noBrief.length === 0, noBrief.join(','));
const noCast = NEW_IDS.filter(id=>['電影', '電視劇', '廣告'].indexOf(byId[id].type) >= 0 &&
  !(byId[id].cast && ['leadM', 'leadF', 'supportM', 'supportF'].every(k=>k in byId[id].cast)));
ok('W1 新影視廣告全部有 cast 四格', noCast.length === 0, noCast.join(','));
const noSinger = NEW_IDS.filter(id=>byId[id].type === '唱片通告' && (!byId[id].singer || !byId[id].singerGender));
ok('W1 新唱片全部有 singer／singerGender', noSinger.length === 0, noSinger.join(','));
const noHost = NEW_IDS.filter(id=>byId[id].type === '綜藝' && !byId[id].host);
ok('W1 新綜藝全部有 host', noHost.length === 0, noHost.join(','));
const noProduct = NEW_IDS.filter(id=>byId[id].type === '廣告' && (!byId[id].product || !byId[id].productKind || !byId[id].productGender || !byId[id].brand));
ok('W1 新廣告全部寫明產品／類別／性別／品牌', noProduct.length === 0, noProduct.join(','));
const badLoc = NEW_IDS.filter(id=>['ad_adm', 'ad_central', 'film_cotton', 'film_harbour', 'film_lion', 'rec_hk', 'rec_star', 'rec_wanchai', 'tvb_harbour', 'tvb_kowloon', 'tvb_longmen'].indexOf(byId[id].loc) < 0);
ok('W1 新通告 loc 全部喺 11 個板面地點入面', badLoc.length === 0, badLoc.join(','));

/* ---------- W2：冬季總數＋開局可接 ---------- */
const w90 = gigs.filter(g=>g.year === 1990 && g.season === '冬');
ok('W2 1990 冬 40 張', w90.length === 40, 'n=' + w90.length);
const openStats = { acting: 18, stage: 14, vocal: 14, looks: 22, charm: 16, iq: 20, stamina: 75 };
const reqMet = g=>{
  const req = g.req || {};
  return Object.keys(req).every(k=>(Number(req[k]) || 0) <= (openStats[k] != null ? openStats[k] : 0));
};
const openWinter = w90.filter(reqMet);
ok('W2 冬季開局可接 18 張', openWinter.length === 18, 'n=' + openWinter.length + ' ' + openWinter.map(g=>g.id).join(','));
const newOpen = NEW_IDS.filter(id=>reqMet(byId[id]));
ok('W2 新通告 9 張開局可接', newOpen.length === 9, 'n=' + newOpen.length + ' ' + newOpen.join(','));
const high1990 = gigs.filter(g=>g.year === 1990 && (g.tier === '高級' || g.tier === '稀有'));
ok('W2 1990 年高級 1 張（film_304）', high1990.length === 1 && high1990[0].id === 'gig_1990_film_304',
   high1990.map(g=>g.id).join(','));

/* ---------- W3：獎項提名人收集零變動（awards63Fellows 口徑） ---------- */
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
function payOf(g){ return Array.isArray(g.pay) ? (Number(g.pay[1] != null ? g.pay[1] : g.pay[0]) || 0) : (Number(g.pay) || 0); }
function top3(slotKind, slotKey, typeList, gender){
  const cands = [];
  gigs.forEach(g=>{
    if(g.year !== 1990 || (g.category && g.category !== '作品')) return;
    if(typeList.indexOf(g.type) < 0) return;
    let starId = '';
    if(slotKind === 'singer'){ starId = String(g.singer || ''); if(!starId) return; if(gender && String(g.singerGender || '').toLowerCase() !== gender) return; }
    else if(slotKind === 'host'){ starId = String(g.host || ''); if(!starId) return; }
    else if(slotKind === 'newcomer'){ starId = String(g.singer || ''); if(!starId) return; }
    else { const c = g.cast || {}; starId = String(c[slotKey] || ''); if(!starId) return; }
    if(!sprite.has(starId)) return;
    cands.push({ pay: payOf(g), id: g.id, starId });
  });
  cands.sort((a, b)=>(b.pay - a.pay) || (a.id < b.id ? -1 : (a.id > b.id ? 1 : 0)));
  const used = {}, out = [];
  cands.forEach(c=>{ if(out.length >= 3 || used[c.starId]) return; used[c.starId] = true; out.push(c.starId); });
  return out;
}
function eqArr(a, b){ return a.length === b.length && a.every((v, i)=>v === b[i]); }
ok('W3 電影男主角格不變（廖炳星＋陸柏言＋麥震東）',
   eqArr(top3('cast', 'leadM', ['電影']), ['liu_bingxing', 'luk_baakyin', 'mak_zhendong']),
   top3('cast', 'leadM', ['電影']).join(','));
ok('W3 電影女主角格不變（鍾楚凝＋胡美琳＋魏詠男）',
   eqArr(top3('cast', 'leadF', ['電影']), ['chung_choning', 'wu_meilam', 'ngai_wingnaam']),
   top3('cast', 'leadF', ['電影']).join(','));
ok('W3 電影男配角格不變（陸柏言＋麥震東＋齊鎮海）',
   eqArr(top3('cast', 'supportM', ['電影']), ['luk_baakyin', 'mak_zhendong', 'chai_zanhoi']),
   top3('cast', 'supportM', ['電影']).join(','));
ok('W3 電影女配角格不變（韓秀婷＋魏詠男＋鍾楚凝）',
   eqArr(top3('cast', 'supportF', ['電影']), ['hon_sauting', 'ngai_wingnaam', 'chung_choning']),
   top3('cast', 'supportF', ['電影']).join(','));
ok('W3 電視男主角格不變（陸柏言＋麥震東＋齊鎮海）',
   eqArr(top3('cast', 'leadM', ['電視劇']), ['luk_baakyin', 'mak_zhendong', 'chai_zanhoi']),
   top3('cast', 'leadM', ['電視劇']).join(','));
ok('W3 電視女主角格不變（胡美琳＋鍾楚凝＋魏詠男）',
   eqArr(top3('cast', 'leadF', ['電視劇']), ['wu_meilam', 'chung_choning', 'ngai_wingnaam']),
   top3('cast', 'leadF', ['電視劇']).join(','));
ok('W3 電視男配角格不變（陸柏言＋麥震東＋齊鎮海）',
   eqArr(top3('cast', 'supportM', ['電視劇']), ['luk_baakyin', 'mak_zhendong', 'chai_zanhoi']),
   top3('cast', 'supportM', ['電視劇']).join(','));
ok('W3 電視女配角格不變（魏詠男＋江詩盈＋蘇芷茵）',
   eqArr(top3('cast', 'supportF', ['電視劇']), ['ngai_wingnaam', 'kong_siying', 'so_jiyan']),
   top3('cast', 'supportF', ['電視劇']).join(','));
ok('W3 司儀格不變（陸柏言＋彭少祺＋顧明輝）',
   eqArr(top3('host', null, ['綜藝']), ['luk_baakyin', 'pang_siuki', 'gu_mingfai']),
   top3('host', null, ['綜藝']).join(','));
ok('W3 男歌手格不變（顧明輝＋駱家聲＋陸柏言）',
   eqArr(top3('singer', null, ['唱片通告'], 'm'), ['gu_mingfai', 'lok_gasing', 'luk_baakyin']),
   top3('singer', null, ['唱片通告'], 'm').join(','));
ok('W3 女歌手格不變（沈映雪＋韓秀婷＋藍若曦）',
   eqArr(top3('singer', null, ['唱片通告'], 'f'), ['shum_yingsuet', 'hon_sauting', 'lan_ruoxi']),
   top3('singer', null, ['唱片通告'], 'f').join(','));
const newcomer = top3('newcomer', null, ['唱片通告']);
ok('W3 新人獎 3 個、男女齊', newcomer.length === 3 &&
   newcomer.some(id=>['gu_mingfai', 'lok_gasing', 'luk_baakyin'].indexOf(id) >= 0) &&
   newcomer.some(id=>['shum_yingsuet', 'hon_sauting', 'lan_ruoxi', 'so_jiyan'].indexOf(id) >= 0),
   newcomer.join(','));

/* ---------- W4：硬規則 ---------- */
const ngaiRec = gigs.filter(g=>g.type === '唱片通告' && g.singer === 'ngai_wingnaam');
ok('W4 魏詠男唔入任何唱片格', ngaiRec.length === 0, ngaiRec.map(g=>g.id).join(','));
const trigNew = NEW_IDS.filter(id=>byId[id].trigger);
ok('W4 新通告無 trigger（P7 維持 34 張）', trigNew.length === 0, trigNew.join(','));
const yearInName = NEW_IDS.filter(id=>/\d/.test(byId[id].workTitle || '') || /\d/.test(byId[id].title || ''));
ok('W4 新名唔含年份數字', yearInName.length === 0, yearInName.join(','));
const dupTitle = NEW_IDS.filter(id=>{
  const g = byId[id];
  if(!g.workTitle) return false;
  return gigs.some(o=>o.id !== id && o.workTitle === g.workTitle);
});
ok('W4 新作品名唔撞現庫', dupTitle.length === 0, dupTitle.join(','));

console.log(fails === 0 ? 'ALL PASS' : fails + ' FAIL');
process.exit(fails === 0 ? 0 : 1);
