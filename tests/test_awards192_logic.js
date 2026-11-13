// v20a192 修 v188 設計 review B1＋C1–C4・邏輯測試：
// B1：8 款贏獎報紙模板（AWARDS188_NP_WIN＋VENUE99_NP_DEK 生效後）零舊前提——
//     三句對白／茶餐廳食面／臨記生涯／不殺之恩／一句收工了／綠葉／和音／合唱單曲／
//     涼茶／跌低眼鏡／特別獎全部唔出；music_01 唔寫「新人」（會喺贏最佳男歌手嗰陣出）；
//     music_02 唯一乾淨款唔郁；nominee 模板唔郁。
// C1：cat_tv_lead_m loseLine「還有」→「仲有」，其餘 44 行唔含書面語「還有」。
// C2：awards62GateLineHtml 音樂閘句刪走——music gallery 唔再出「嗰年未唱過歌」，
//     跌返「坐觀禮席睇全場」；film／tv 版閘句逐字不變。
// C3：renderAwardResultHtml 第一行跟舞台 focus（awards63FocusCat）——雙格 pack
//     focus 格行先，其餘格維持 v184 id 序；同屆提名行仍然只出一次。
// C4：renderAwardInviteHtml gallery 請柬列全 slate（4 格＋觀禮標記）；nominee 請柬唔郁。
// 反證：對 pristine main b7ca827 index 行 → v192 文案／邏輯未入 → FAIL（唔 crash）。
// 用法：node tests/test_awards192_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
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
  let depth = 0, started = false;
  for(let k = i; k < html.length; k++){
    const ch = html[k];
    if(ch === '{' || ch === '['){ depth++; started = true; }
    else if(ch === '}' || ch === ']'){ depth--; if(started && depth === 0) return html.slice(i, k + 1) + ';'; }
    else if(ch === ';' && !started) return html.slice(i, k + 1);
  }
  throw new Error('const end not found: ' + name);
}

/* 反證守衛：v192 嘢唔存在嗰陣乾淨 FAIL（逐項列出），唔好等 extraction 喺頂層 throw 崩潰。 */
const NEED192 = ['阿偉憑實力跑出', '仲有下一場', '阿偉奪獎贏街坊票', '（觀禮）'];
let missing192 = NEED192.filter(s => html.indexOf(s) < 0);
if(missing192.length){
  missing192.forEach(m=>{ fails.push('反證：' + m + ' 唔存在'); console.log('FAIL 反證：' + m + ' 唔存在（pristine main 預期，v192 未入）'); });
  console.log('\nFAILED: ' + fails.length);
  process.exit(1);
}

var window = {};
var S = null;

/* ---- B1：生效後 8 款 win 模板 ---- */
eval(extractConst('AWARDS188_NP_WIN').replace('const AWARDS188_NP_WIN =', 'var AWARDS188_NP_WIN ='));
eval(extractFn('awards188ApplyNpOverlay'));
const NP_PACK_PATH = path.join(path.dirname(htmlPath), 'content', 'STUB_NEWSPAPER_MORNING_SOFT_v1.json');
const NP_PACK = JSON.parse(fs.readFileSync(NP_PACK_PATH, 'utf8'));
for(const c of ['VENUE99_INVITE_DEK','VENUE99_PRESS_DEK','VENUE99_NEWS_LINE','VENUE99_NP_DEK'])
  eval(extractConst(c).replace('const ' + c + ' =', 'var ' + c + ' ='));
eval(extractFn('venue99ApplyOverlay'));
const npCopy = JSON.parse(JSON.stringify(NP_PACK));
const FW192 = { awardsStub: {}, newspaperStub: npCopy };
venue99ApplyOverlay(FW192);
const npNomBefore = JSON.stringify((npCopy.templates && npCopy.templates.award_nominee) || []);
awards188ApplyNpOverlay(FW192);
const npWinAfter = (npCopy.templates && npCopy.templates.award_win) || [];
ok('B1：pack 有 8 款 award_win 模板', npWinAfter.length === 8);
const BANNED = ['三句對白', '茶餐廳食面', '臨記生涯', '不殺之恩', '一句收工了', '綠葉',
  '和音', '合唱單曲', '涼茶', '跌低眼鏡', '特別獎', '臨記組', '最受歡迎'];
let bannedHits = [];
npWinAfter.forEach(t => {
  ['headline', 'dek', 'clipLabel'].forEach(f => {
    const v = String((t && t[f]) || '');
    BANNED.forEach(b => { if(v.indexOf(b) >= 0) bannedHits.push(t.id + ':' + f + ':' + b); });
  });
});
ok('B1：8 款 win 模板 headline／dek／clipLabel 零舊前提', bannedHits.length === 0);
if(bannedHits.length) console.log('  dirty: ' + bannedHits.join(' | '));
const byId = {};
npWinAfter.forEach(t => { byId[t.id] = t; });
ok('B1：music_01 唔寫「新人」（贏最佳男歌手嗰陣唔可以係新人獎）',
  (byId.np_win_music_01.headline || '').indexOf('新人') < 0 && (byId.np_win_music_01.dek || '').indexOf('新人') < 0);
ok('B1：music_02 唯一乾淨款唔郁', byId.np_win_music_02.headline === '金碟夜 阿偉奪獎 樂壇多把靚聲');
ok('B1：film_01 dek 憑實力跑出（唔寫戲份）', (byId.np_win_film_01.dek || '').indexOf('憑實力跑出') >= 0);
ok('B1：film_02 headline 奪獎成焦點（唔寫茶餐廳／封王）', byId.np_win_film_02.headline === '影藝獎夜 阿偉奪獎成焦點');
ok('B1：tv_01 dek 多謝台前幕後（唔寫不殺之恩）', (byId.np_win_tv_01.dek || '').indexOf('多謝台前幕後') >= 0);
ok('B1：tv_02 headline／dek 通用（唔寫一句對白／綠葉）', byId.np_win_tv_02.headline === '台慶夜 阿偉奪獎贏街坊票');
ok('B1：ad_01 dek 憑廣告突圍（唔寫具體產品）', (byId.np_win_ad_01.dek || '').indexOf('憑廣告突圍') >= 0);
ok('B1：ad_02 headline 奪獎贏掌聲（唔寫跌低眼鏡）', byId.np_win_ad_02.headline === '街外一鏡 阿偉奪獎贏掌聲');
ok('B1：ad_02 dek 奪得廣告獎（VENUE99 嗰邊，唔寫特別獎／綠葉）', (byId.np_win_ad_02.dek || '').indexOf('奪得廣告獎') >= 0);
ok('B1：film_02 dek 奪得演員獎（VENUE99 嗰邊，唔寫臨記生涯）', (byId.np_win_film_02.dek || '').indexOf('奪得演員獎') >= 0);
ok('B1：4 款 nominee 模板唔郁（覆寫唔掂 nominee）',
  JSON.stringify((npCopy.templates && npCopy.templates.award_nominee) || []) === npNomBefore);
ok('B1：8 款 clipLabel 全部新名唔郁',
  npWinAfter.every(t => /・得獎$/.test(String(t.clipLabel || ''))));

/* ---- C1：電視男主角 loseLine ---- */
eval(extractConst('AWARDS188_CATEGORIES').replace('const AWARDS188_CATEGORIES =', 'var AWARDS188_CATEGORIES ='));
const tvLead = (AWARDS188_CATEGORIES.award_singho_tv || []).find(c => c && c.id === 'cat_tv_lead_m') || {};
ok('C1：cat_tv_lead_m loseLine「還有」→「仲有」',
  tvLead.loseLine === '名單滑過你個名——入圍咗，未抱盃。仲有下一場。');
let stillShu = [];
Object.keys(AWARDS188_CATEGORIES).forEach(k => {
  (AWARDS188_CATEGORIES[k] || []).forEach(c => {
    ['winLine', 'loseLine', 'galleryLine'].forEach(f => {
      if(String((c && c[f]) || '').indexOf('還有') >= 0) stillShu.push(c.id + ':' + f);
    });
  });
});
ok('C1：15 格 45 行文案再無書面語「還有」', stillShu.length === 0);
if(stillShu.length) console.log('  still: ' + stillShu.join(' | '));

/* ---- C2：閘句 ---- */
eval(extractConst('AWARDS62_MEDIUM_LABEL').replace('const AWARDS62_MEDIUM_LABEL =', 'var AWARDS62_MEDIUM_LABEL ='));
eval(extractFn('awards62GateLineHtml'));
function gatePack(medium){
  return { medium: medium, standing62: { tier: 'gallery', wraps: 2, wrapMin: 2, dualOk: true,
    gapWorks: 0, gapWin: 0, repTitle: '長篇劇' } };
}
const gateMusic = awards62GateLineHtml(gatePack('music'));
ok('C2：音樂 gallery 唔再出「嗰年未唱過歌」（死文案刪走）', gateMusic.indexOf('未唱過歌') < 0);
ok('C2：音樂 gallery 跌返「坐觀禮席睇全場」', gateMusic.indexOf('坐觀禮席睇全場') >= 0);
const gateFilm = awards62GateLineHtml(gatePack('film'));
ok('C2：電影版閘句逐字不變', gateFilm.indexOf('嗰年未做過主角／配角級作品，入圍唔到演員獎') >= 0);
const gateTv = awards62GateLineHtml(gatePack('tv'));
ok('C2：電視版閘句逐字不變', gateTv.indexOf('嗰年未做過主角／配角級作品，入圍唔到演員獎') >= 0);
const gateNom = awards62GateLineHtml({ medium: 'music',
  standing62: { tier: 'nominee', wraps: 2, wrapMin: 2, dualOk: true, gapWorks: 0, gapWin: 0, repTitle: '大碟' } });
ok('C2：nominee 分支唔受影響（音樂入圍門檻行照出）', /入圍門檻已達標/.test(gateNom) && /《大碟》/.test(gateNom));

/* ---- C3＋C4：結果卡／請柬呈現層 ---- */
eval(extractConst('EMOJI_ICON112').replace('const EMOJI_ICON112 =', 'var EMOJI_ICON112 ='));
eval(extractFn('iconHtml112'));
for(const f of ['awardsCatsSorted184', 'awards63FocusCat', 'awards63FellowsHtml', 'awardWinner149', 'awardWinLine149', 'renderAwardResultHtml', 'renderAwardInviteHtml'])
  eval(extractFn(f));
function count(hay, needle){ return hay.split(needle).length - 1; }
const FEL = [
  { starId: 'yip_manji', star: '葉敏芝', title: '渡輪燈火', gigId: 'gig_x1', poster: '', assigned: true },
  { starId: 'chung_choning', star: '鍾楚凝', title: '星光夜', gigId: 'gig_x2', poster: '', assigned: true }
];
const CAT_LEAD = { id: 'cat_film_lead_m', label: '最佳男主角', outcome: 'won',
  line: '影藝獎台上念到你個名。', repWorkTitle: '新春大吉', weakHint62: '', fellows63: FEL, winner63: null };
const CAT_SUP = { id: 'cat_film_support_m', label: '最佳男配角', outcome: 'won',
  line: '台上念到你個名。', repWorkTitle: '新春大吉', weakHint62: '', fellows63: FEL, winner63: null };
function resPack(cats, outcome){
  return { displayName: '維港影藝獎', tierLabel: '入圍／提名', year: 1990, venue99: '金禧大酒店',
    bestOutcome: outcome || 'won', categories: cats,
    press: { paperName: '娛樂快報', headline: '影藝獎揭曉', dek: '頒獎夜結束。' },
    news: { outlet: '晚間娛樂快訊', line: '影藝獎散場。' },
    metricEcho: '票房話題', metricEchoLabel: '票房話題', rewardsApplied: { stageVolume: 1, industryCredit: 2 } };
}
/* 雙贏 pack：pack 次序男配角先（review 實測次序）→ 舞台 focus 係男配角，結果卡第一行要係男配角 */
const dualWon = renderAwardResultHtml(resPack([CAT_SUP, CAT_LEAD], 'won'));
ok('C3：雙格 won——結果卡第一行＝舞台 focus（男配角先）',
  dualWon.indexOf('最佳男配角') < dualWon.indexOf('最佳男主角'));
ok('C3：雙格 won——兩張類別卡齊晒', count(dualWon, '最佳男主角') === 1 && count(dualWon, '最佳男配角') === 1);
ok('C3：雙格 won——同屆提名行仍然只出一次', count(dualWon, '同屆提名') === 1);
/* 反向 pack 次序：男主角先 → focus 係男主角，結果卡男主角行先（唔係死跟 id 序） */
const dualWonRev = renderAwardResultHtml(resPack([CAT_LEAD, CAT_SUP], 'won'));
ok('C3：pack 次序反轉——結果卡跟 focus 走（男主角行先）',
  dualWonRev.indexOf('最佳男主角') < dualWonRev.indexOf('最佳男配角'));
/* 單格唔變 */
const singleWon = renderAwardResultHtml(resPack([CAT_LEAD], 'won'));
ok('C3：單格結果卡不變（一張男主角卡）',
  count(singleWon, '最佳男主角') === 1 && count(singleWon, '最佳男配角') === 0);

/* ---- C4：請柬 ---- */
function invPack(cats, tier, ceremonyId){
  return { ceremonyId: ceremonyId || 'award_harbour_film', tier: tier, tierLabel: tier === 'gallery' ? '旁聽席' : '入圍／提名',
    displayName: '維港影藝獎', season: '秋', year: 1990, venue99: '金禧大酒店',
    inviteTitle: '維港影藝獎請柬', inviteDek: '你收到一封頒獎禮嘅請柬。', categories: cats, repWork62: '' };
}
const galFilm = renderAwardInviteHtml(invPack(
  [{ id: 'cat_film_support_m', label: '最佳男配角' }, { id: 'cat_film_lead_m', label: '最佳男主角' }], 'gallery'));
ok('C4：gallery 請柬列全 slate（電影 4 格男女獎齊）',
  /今晚獎項：最佳男主角、最佳女主角、最佳男配角、最佳女配角（觀禮）/.test(galFilm));
const galMusic = renderAwardInviteHtml(invPack(
  [{ id: 'cat_music_newcomer', label: '最佳新人獎' }, { id: 'cat_music_singer_m', label: '最佳男歌手' }], 'gallery', 'award_golddisc_music'));
ok('C4：gallery 請柬列全 slate（音樂 3 格男女獎＋新人獎齊）',
  /今晚獎項：最佳男歌手、最佳女歌手、最佳新人獎（觀禮）/.test(galMusic));
const galAd = renderAwardInviteHtml(invPack(
  [{ id: 'cat_ad_lead_m', label: '最佳廣告男主角' }], 'gallery', 'award_harbour_ad'));
ok('C4：gallery 請柬列全 slate（廣告 4 格男女獎齊）',
  /今晚獎項：最佳廣告男主角、最佳廣告女主角、最佳廣告男配角、最佳廣告女配角（觀禮）/.test(galAd));
const nomFilm = renderAwardInviteHtml(invPack(
  [{ id: 'cat_film_support_m', label: '最佳男配角' }, { id: 'cat_film_lead_m', label: '最佳男主角' }], 'nominee'));
ok('C4：nominee 請柬唔郁（淨列你爭嗰 2 格，唔加女獎／觀禮標記）',
  /今晚獎項：最佳男主角、最佳男配角<\/p>/.test(nomFilm) && nomFilm.indexOf('（觀禮）') < 0);
ok('C4：gallery 請柬女獎只係列名（唔寫阿偉會爭女獎）',
  galFilm.indexOf('女主角') >= 0 && galFilm.indexOf('你爭') < 0);

console.log(fails.length ? ('\nFAILED: ' + fails.length + ' -> ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
