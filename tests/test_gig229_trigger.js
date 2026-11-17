// v20a229 B5 觸發系統＋BR89 擴充測試（A6／A7；SPEC §2.4／§3.5；AUDIT229 §5／§7／§8；DECISIONS D-4／D-7／D-11／D-14）
//   T0 新庫 33 張 trigger 形狀逐種齊（kind 必填欄齊全；credit 23／fame 5／rel 3／rival 1／story 1，award 0——
//       v252 新庫已無 award kind；award 機制見 T1／T3 合成樣本。稀有級 21 張，當中 6 張有 trigger）
//   T1 六種 kind 各一例：credit／award／fame／story／rel／rival（觸發前 false、觸發後 true；
//       award 嗰例用合成樣本——攞舊庫 gig_1991_film_111 原 trigger，一字唔改，因為新庫 0 張 award 樣本）
//   T2 R-4 雙觸發 OR：持債權／還錢結算（enc83_gu_loan_result＝1）兩條路各驗一次（真 gig
//       gig_1992_rec_205；v20a274 接線由 rec_105 搬去新顧引薦 gig rec_205）
//   T3 獎項級紀錄 S.awardsResults：recordAwardResult 寫入＋獎項級／典禮級觸發判定（合成樣本——舊庫 6 張 award gig 原 trigger）
//   T4 板面：觸發前無、觸發後有；已觸發唔受 gigBoardPosted92 再擋（stagger stub 返 false 照上板）；標「引薦／邀約」
//   T5 D-11 通知：首次上板先 toast 一次（引薦＝何生轉告、其餘＝情報站）；未入季節窗／未觸發唔通知
//   T6 G-L2／G-NGAI-3 經新 trigger 系統開到
//   T7 D-14：mergeIntelGigs 改源 T2（唔再讀 intel_lu_burst）；v232 新庫補寫《星夜迷離》做第 241 張（rel luk_baakyin ≥25），INTEL_HIDDEN_GIGS 池留空，唔留雙重閘（v252 重編號 tv_122→tv_203）
//   T8 BR89 映射 13 張逐對錨點＋獎項對照表 15 個 id 齊
//   T9 G-9：1992 年金碟夜喺遊戲期內（夏），1992 年唱片 award 觸發開得到（合成樣本，見 T3）
//   T10 trigger 過 normalizeGigRecord 唔跌（年份＋trigger 齊全）
//   T11 真季節窗：1991 秋觸發通告喺 1991-09-01 入窗、1991-01-01 未入窗
// 反證：對 B4 index 行 → T1／T4／T5 抽唔到 triggerGigOn 即 FAIL。
// 用法：node tests/test_gig229_trigger.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond, extra){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name+(extra?' :: '+extra:'')); }
function deepClone(o){ return JSON.parse(JSON.stringify(o)); }
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) return null;
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){ if(html[j]==='{') depth++; else if(html[j]==='}'){ depth--; if(depth===0) break; } }
  return html.slice(i, j+1);
}
function extractConstVar(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) return null;
  let depth=0, started=false;
  for(let k=i; k<html.length; k++){
    const ch = html[k];
    if(ch==='{'||ch==='['){ depth++; started = true; }
    else if(ch==='}'||ch===']'){ depth--; if(started && depth===0) return html.slice(i, k+1).replace('const '+name, 'var '+name)+';'; }
    else if(ch===';' && !started) return html.slice(i, k+1).replace('const '+name, 'var '+name);
  }
  return null;
}

const pack = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gigs_new.json'), 'utf8'));
const gigs = pack.gigs || [];
const gigById = id => gigs.find(g=>g.id===id);

/* ---------- T0：trigger 形狀 ---------- */
const trig = gigs.filter(g=>g.trigger && g.trigger.kind);
ok('T0 觸發通告 33 張', trig.length===33, 'n='+trig.length);
const shapeBad = trig.filter(g=>{
  const t = g.trigger;
  if(t.kind==='credit') return !(typeof t.creditId==='string' && t.creditId && typeof t.creditOwner==='string');
  if(t.kind==='award') return !(typeof t.awardId==='string' && t.awardId && (t.result==='提名' || t.result==='得獎'));
  if(t.kind==='fame') return !(typeof t.fameMin==='number');
  if(t.kind==='story') return !(typeof t.nodeId==='string' && /^N\d+$/.test(t.nodeId));
  if(t.kind==='rel') return !(typeof t.npcId==='string' && typeof t.relMin==='number');
  if(t.kind==='rival') return !(typeof t.rivalScoreMin==='number');
  return true;
});
ok('T0 六種 kind 形狀齊（必填欄全部有）', shapeBad.length===0, shapeBad.slice(0,3).map(g=>g.id).join(','));
const rareGigs = gigs.filter(g=>g.tier==='稀有');
ok('T0 稀有級 21 張、其中 6 張有 trigger（稀有≠觸發閘，新庫真相）',
  rareGigs.length===21 && rareGigs.filter(g=>g.trigger && g.trigger.kind).length===6,
  'rare=' + rareGigs.length + ' withTrig=' + rareGigs.filter(g=>g.trigger && g.trigger.kind).length);

/* ---------- eval 沙盒：trigger 模組 ---------- */
eval(extractConstVar('BR89_PATRON_OF_GIG'));
eval(extractConstVar('GIG_TRIGGER_AWARD_MAP229'));
eval(extractConstVar('RIVAL_CFG'));
eval(extractConstVar('RIVAL_FACEOFF_GIGS'));
for(const f of ['br89HasCredit','br89GigOn','awardTriggerOn229','rivalTriggerOpenable229',
  'triggerGigOn','triggerGigLabel229','triggerGigLocName229','mergeTriggerGigs',
  'ensureAwardsResults','recordAwardResult','rivalryScore','ensureRivalry',
  'rivalryGigForRound','enc79TierOf','gigsForLocSeasonBoard']){
  const src = extractFn(f);
  if(!src){ ok('抽取 function '+f, false); }
  else eval(src);
}
var S = null;
var GIGS = [];
var window = {};
var LOCS = [
  { id:'film_lion', name:'獅子山製片' }, { id:'film_cotton', name:'紅棉影業' },
  { id:'film_harbour', name:'維港電影' }, { id:'tvb_longmen', name:'星河電視台' },
  { id:'tvb_kowloon', name:'九龍電視台' }, { id:'tvb_harbour', name:'海港廣播' },
  { id:'rec_star', name:'天星音樂' }, { id:'rec_hk', name:'香江唱片' },
  { id:'rec_wanchai', name:'灣仔唱片' }, { id:'ad_central', name:'中環廣告' },
  { id:'ad_adm', name:'金鐘創意' }
];
var toasts = [];
var toast = function(m){ toasts.push(String(m)); };
var calendarSeason = function(){ return '秋'; };
var gigSeasonHidden88 = function(){ return false; };
var gigBoardPosted92 = function(){ return false; };
var isGigConsumed = function(){ return false; };
var boardSortCompare = function(){ return 0; };
var normalizeGigRecord = function(g){ return g; };
var mergeSoftBridgeGigs = function(){};
var mergeFavorGigs = function(){};
var mergeWf3Gigs = function(){};
var mergeBr89Gigs = function(){};
var mergeRivalGigs = function(){};
var mergeExodusGigs = function(){};
var mergeMidGigs35 = function(){};
var mergeWinterBridge88 = function(){};
var mergeYearGigs36 = function(){};
var mergeNat92Gigs = function(){};
function freshS(){
  return {
    dayIndex: 600, fame: 0, popularity: 0, industryCredit: 0, money: 12000, stress: 0,
    story: { done: {}, flags: {}, rel: {} },
    flags: {}, npcs: {}, stars: {}, mockCredits: [], mockDebts: [], mockRumors: [],
    newspaperClippings: [], wrapHistory: [], pendingAud: [],
    awardsLog: [], awardsFlags: {}, awardsResults: {},
    rivalry: { score: 0, faceoffState: 'none', openedDay: null, settledDay: null, stance: '',
      round: 1, gigId: null, nextOpenDay: null, lastResult: '', wins: 0, newsIdx: 0, workTitle: '' }
  };
}

/* ---------- T1：六種 kind 各一例 ---------- */
S = freshS();
const gCredit = gigById('gig_1991_film_101'); /* 陸引薦 credit_enc83_luk_patron（《江河歲月》，舊 film_106 同名同 trigger 搬咗過嚟） */
ok('T1 credit 未持債 → 唔開', triggerGigOn(gCredit)===false);
S.mockCredits.push({ id:'credit_enc83_luk_patron', debtor:'陸柏言', title:'天王引薦', line:'x', status:'未收' });
ok('T1 credit 持債 → 開', triggerGigOn(gCredit)===true);
S.mockCredits[0].redeemedBy = 'gig_1991_film_101';
ok('T1 credit 已兌現 → 唔再開', triggerGigOn(gCredit)===false);
S.mockCredits[0].redeemedBy = undefined;
ok('T1 credit 標籤＝引薦', triggerGigLabel229(gCredit)==='引薦');

S = freshS();
/* v252 新庫 0 張 award kind：用合成樣本，trigger 同舊庫 gig_1991_film_111 一字一樣（award_film_best_actor 得獎），驗 index.html awardTriggerOn229 機制本身。 */
const gAward = { id:'gig_1991_film_111', trigger:{ kind:'award', awardId:'award_film_best_actor', result:'得獎' } };
ok('T1 award 未得獎 → 唔開', triggerGigOn(gAward)===false);
S.awardsResults['1991/award_harbour_film'] = { year:1991, won:false, nominated:true, cats:{ cat_film_lead_m:'nominated' } };
ok('T1 award 只提名 → 得獎觸發唔開', triggerGigOn(gAward)===false);
S.awardsResults['1991/award_harbour_film'] = { year:1991, won:true, nominated:true, cats:{ cat_film_lead_m:'won' } };
ok('T1 award 得獎 → 開', triggerGigOn(gAward)===true);
ok('T1 award 標籤＝邀約', triggerGigLabel229(gAward)==='邀約');

S = freshS();
const gFame = gigById('gig_1991_film_209'); /* fame ≥40（大製作武打替身；舊 ad_108 已改做高級、無 trigger） */
S.fame = 39;
ok('T1 fame 39 → 唔開', triggerGigOn(gFame)===false);
S.fame = 40;
ok('T1 fame 40 → 開', triggerGigOn(gFame)===true);

S = freshS();
const gStory = gigById('gig_1992_film_205'); /* story N13（古裝武俠頂位替身；舊 tv_117 已唔喺庫） */
ok('T1 story N13 未完成 → 唔開', triggerGigOn(gStory)===false);
S.story.done.N13 = true;
ok('T1 story N13 完成 → 開', triggerGigOn(gStory)===true);

S = freshS();
const gRel = gigById('gig_1992_tv_203'); /* rel luk_baakyin ≥60（台慶晚會頂位群演；舊 tv_118 已唔喺庫） */
S.npcs.luk_baakyin = 59;
ok('T1 rel 59 → 唔開', triggerGigOn(gRel)===false);
S.npcs.luk_baakyin = 60;
ok('T1 rel 60 → 開', triggerGigOn(gRel)===true);

S = freshS();
const gRel25 = gigById('gig_1991_tv_203'); /* v232《星夜迷離》rel luk_baakyin ≥25（T2；v252 重編號 tv_122→tv_203） */
S.npcs.luk_baakyin = 24;
ok('T1 rel 24 →《星夜迷離》唔開（舊 npcs 兜底）', triggerGigOn(gRel25)===false);
S.npcs.luk_baakyin = 25;
ok('T1 rel 25 →《星夜迷離》開（T2，舊 npcs 兜底）', triggerGigOn(gRel25)===true);
S = freshS();
S.stars.luk_baakyin = { fav: 24 };
ok('T1 rel 星好感 24 →《星夜迷離》唔開（S.stars 主路徑）', triggerGigOn(gRel25)===false);
S.stars.luk_baakyin = { fav: 25 };
ok('T1 rel 星好感 25 →《星夜迷離》開（S.stars 主路徑，唔靠 S.npcs）', triggerGigOn(gRel25)===true);
ok('T1《星夜迷離》標籤＝邀約', triggerGigLabel229(gRel25)==='邀約');

S = freshS();
const gRival = gigById('gig_1991_film_102'); /* rival ≥3（《霓虹夜影》男主角，爭位格；舊 film_109 已改做 credit） */
ok('T1 rival 0 分 → 唔開', triggerGigOn(gRival)===false);
S.story.done.N3 = true;
S.newspaperClippings.push({ topicKey:'rival:gao', eventKey:'story:N3' });
ok('T1 rival 3 分（N3＋報紙；傳聞分已刪）→ 開', triggerGigOn(gRival)===true && rivalryScore()===3);
S.rivalry.nextOpenDay = 9999;
ok('T1 rival 冷卻期內 → 唔開', triggerGigOn(gRival)===false);
S.rivalry.nextOpenDay = null;
S.rivalry.faceoffState = 'won';
S.rivalry.round = 3; /* 真終態：第 3 輪先至 won／lost 落幕（round<3 嘅 won／lost 會由 ensureRivalry 轉返下一輪循環，唔係終態） */
ok('T1 rival 終態 won → 唔開', triggerGigOn(gRival)===false);
ok('T1 無 trigger 通告照常開（普通板上）', triggerGigOn({ id:'gig_1990_film_101' })===true);
ok('T1 未識 kind 唔開（fail closed）', triggerGigOn({ id:'x', trigger:{ kind:'bogus' } })===false);

/* ---------- T2：R-4 雙觸發 OR ---------- */
S = freshS();
/* v20a274：R-4 接線已由 gig_1992_rec_105《當年情懷》（trigger 已拆，變普通板通告）搬去
   新顧引薦 gig gig_1992_rec_205《夜總會登台暖場》；用真 gig 驗機制，唔再用合成樣本。 */
const gR4 = gigById('gig_1992_rec_205'); /* 顧明輝引薦夜總會登台暖場，credit_enc83_gu_patron */
ok('T2 R-4 兩條路都冇 → 唔開', triggerGigOn(gR4)===false && br89GigOn(gR4)===false);
S.mockCredits.push({ id:'credit_enc83_gu_patron', debtor:'顧明輝', title:'登台引薦', line:'x', status:'未收' });
ok('T2 R-4 路一：持債權 → 開', triggerGigOn(gR4)===true && br89GigOn(gR4)===true);
S.mockCredits.length = 0;
ok('T2 R-4 債權拎走 → 唔開', triggerGigOn(gR4)===false);
S.flags.enc83_gu_loan_result = 1;
ok('T2 R-4 路二：還錢結算完成（result＝1）→ 開', triggerGigOn(gR4)===true && br89GigOn(gR4)===true);
S.flags.enc83_gu_loan_result = 2;
ok('T2 R-4 還錢失敗（result＝2）→ 唔開', triggerGigOn(gR4)===false);
S.flags.enc83_gu_loan_result = 1;
S.flags['done_gig_1992_rec_205'] = 1;
ok('T2 R-4 完成後唔再開（done_ 旗）', triggerGigOn(gR4)===false);

/* ---------- T2b：新庫顧引薦 gig（gig_1992_rec_205，通用 credit 規則） ---------- */
S = freshS();
const gR4b = gigById('gig_1992_rec_205'); /* 顧明輝引薦夜總會登台暖場，credit_enc83_gu_patron */
ok('T2b 新庫顧 gig 喺庫入面、係 credit_enc83_gu_patron', !!gR4b && gR4b.trigger && gR4b.trigger.kind==='credit' && gR4b.trigger.creditId==='credit_enc83_gu_patron');
ok('T2b 新庫顧 gig 未持債 → 唔開', triggerGigOn(gR4b)===false);
S.mockCredits.push({ id:'credit_enc83_gu_patron', debtor:'顧明輝', title:'登台引薦', line:'x', status:'未收' });
ok('T2b 新庫顧 gig 持債 → 開（通用規則）', triggerGigOn(gR4b)===true);
S.mockCredits.length = 0;
ok('T2b 新庫顧 gig 債權拎走 → 唔開', triggerGigOn(gR4b)===false);
/* v20a274：還錢結算路已接線去新顧引薦 gig rec_205（br89GigOn R-4 硬編碼跟住搬），
   唔再係接線缺口——見 T2 路二。 */
S.flags.enc83_gu_loan_result = 1;
ok('T2b 新庫顧 gig 還錢結算旗 → 開（R-4 第二條路）', triggerGigOn(gR4b)===true);

/* ---------- T3：獎項級紀錄＋典禮級觸發 ---------- */
S = freshS();
const recPack = { year:1991, ceremonyId:'award_harbour_film', skipped:false,
  categories:[ { id:'cat_film_lead_m', outcome:'won' }, { id:'cat_film_lead_f', outcome:'nominated' }, { id:'cat_film_support_m', outcome:'gallery' } ] };
const rec = recordAwardResult(recPack);
ok('T3 recordAwardResult 寫入年／典禮 key', !!rec && !!S.awardsResults['1991/award_harbour_film'], JSON.stringify(S.awardsResults));
ok('T3 won／nominated 旗＋cats 齊', rec.won===true && rec.nominated===true && rec.cats.cat_film_lead_m==='won' && rec.cats.cat_film_lead_f==='nominated' && !rec.cats.cat_film_support_m);
ok('T3 commitAwardToLog 調用 recordAwardResult（唯一結算點）', (extractFn('commitAwardToLog')||'').indexOf('recordAwardResult(pack)')>=0);
/* v252 新庫 0 張 award kind：以下 6 個樣本全部合成，trigger 同舊庫原 gig 一字一樣，驗 awardTriggerOn229 機制本身。 */
const SYN_AWARD = {
  filmNewcomer91:{ id:'gig_1991_film_112', trigger:{ kind:'award', awardId:'award_film_best_newcomer', result:'提名' } },
  musicAlbum92:{ id:'gig_1992_rec_107', trigger:{ kind:'award', awardId:'award_music_best_album', result:'得獎' } },
  musicSong92:{ id:'gig_1992_rec_108', trigger:{ kind:'award', awardId:'award_music_best_song', result:'得獎' } },
  musicNewcomer92:{ id:'gig_1992_rec_109', trigger:{ kind:'award', awardId:'award_music_best_newcomer', result:'提名' } },
  adNewcomer92:{ id:'gig_1992_ad_107', trigger:{ kind:'award', awardId:'award_ad_best_newcomer', result:'提名' } },
  filmActor92:{ id:'gig_1992_film_110', trigger:{ kind:'award', awardId:'award_film_best_actor', result:'得獎' } }
};
S = freshS();
S.awardsResults['1991/award_harbour_film'] = { year:1991, won:false, nominated:true, cats:{ cat_film_lead_f:'nominated' } };
ok('T3 典禮級：電影新人獎提名（合成 gig_1991_film_112）→ 影藝獎嗰屆有提名就開', triggerGigOn(SYN_AWARD.filmNewcomer91)===true);
S = freshS();
S.awardsResults['1992/award_golddisc_music'] = { year:1992, won:true, nominated:true, cats:{ cat_music_singer_m:'won' } };
ok('T3 典禮級：音樂大碟得獎（合成 gig_1992_rec_107）→ 金碟夜嗰屆有得獎就開', triggerGigOn(SYN_AWARD.musicAlbum92)===true);
ok('T3 典禮級：音樂歌曲得獎（合成 gig_1992_rec_108）→ 同屆得獎就開', triggerGigOn(SYN_AWARD.musicSong92)===true);
S = freshS();
S.awardsResults['1992/award_golddisc_music'] = { year:1992, won:false, nominated:true, cats:{ cat_music_newcomer:'nominated' } };
ok('T3 典禮級得獎唔可以靠提名開（只提名 → 大碟得獎唔開）', triggerGigOn(SYN_AWARD.musicAlbum92)===false);
ok('T3 獎項級：音樂新人獎提名（合成 gig_1992_rec_109）→ cat_music_newcomer 提名就開', triggerGigOn(SYN_AWARD.musicNewcomer92)===true);
S = freshS();
S.awardsResults['1992/award_harbour_ad'] = { year:1992, won:false, nominated:true, cats:{ cat_ad_support_m:'nominated' } };
ok('T3 典禮級：廣告新人獎提名（合成 gig_1992_ad_107）→ 廣告賞嗰屆有提名就開', triggerGigOn(SYN_AWARD.adNewcomer92)===true);
S = freshS();
S.awardsResults['1991/award_harbour_film'] = { year:1991, won:true, nominated:true, cats:{ cat_film_lead_m:'won' } };
S.awardsResults['1992/award_harbour_film'] = { year:1992, won:false, nominated:false, cats:{} };
ok('T3 舊屆紀錄唔俾新屆覆寫（1991 贏咗，1992 gallery 照開 1992 秋通告，合成 gig_1992_film_110）', triggerGigOn(SYN_AWARD.filmActor92)===true);

/* ---------- T4：板面（過濾＋錯峰豁免＋標籤） ---------- */
S = freshS();
const boardGigs = [
  deepClone(gigById('gig_1991_film_101')), /* credit，未觸發（《江河歲月》，film_harbour） */
  deepClone(gigs.find(g=>g.loc==='film_harbour' && !g.trigger)), /* 普通板上 */
];
GIGS = boardGigs;
gigBoardPosted92 = function(){ return true; }; /* 先放行錯峰，淨驗觸發過濾 */
let board = gigsForLocSeasonBoard('film_harbour', '秋').map(g=>g.id);
ok('T4 觸發前板面無引薦通告（普通通告照有）', board.indexOf('gig_1991_film_101')<0 && board.length===1, JSON.stringify(board));
S.mockCredits.push({ id:'credit_enc83_luk_patron', debtor:'陸柏言', title:'天王引薦', line:'x', status:'未收' });
gigBoardPosted92 = function(){ return false; }; /* 再閘死錯峰，驗已觸發豁免 */
board = gigsForLocSeasonBoard('film_harbour', '秋').map(g=>g.id);
ok('T4 觸發後上板（gigBoardPosted92 stub 返 false 照上——錯峰豁免）', board.indexOf('gig_1991_film_101')>=0, JSON.stringify(board));
ok('T4 普通通告唔享豁免（stagger 返 false → 照擋）', (function(){
  S = freshS(); GIGS = [deepClone(gigs.find(g=>g.loc==='film_harbour' && !g.trigger))];
  return gigsForLocSeasonBoard('film_harbour', '秋').length===0;
})());
S = freshS();
S.mockCredits.push({ id:'credit_enc83_luk_patron', debtor:'陸柏言', title:'天王引薦', line:'x', status:'未收' });
GIGS = [deepClone(gigById('gig_1991_film_101'))];
board = gigsForLocSeasonBoard('film_harbour', '秋');
ok('T4 短卡／詳情卡有引薦標籤位（gt-trigger／bp-tag trig）', html.indexOf('gt-trigger')>=0 && html.indexOf('bp-tag trig')>=0 && board.length===1 && triggerGigLabel229(board[0])==='引薦');
ok('T4 mergeTriggerGigs 掛入 gigsForLocSeasonBoard 開頭', (extractFn('gigsForLocSeasonBoard')||'').indexOf('mergeTriggerGigs(locId)')>=0);

/* ---------- T5：D-11 通知 ---------- */
S = freshS();
toasts.length = 0;
GIGS = [deepClone(gigById('gig_1991_film_101'))];
ok('T5 未觸發 → 唔通知', mergeTriggerGigs('film_harbour')===0 && toasts.length===0);
S.mockCredits.push({ id:'credit_enc83_luk_patron', debtor:'陸柏言', title:'天王引薦', line:'x', status:'未收' });
ok('T5 引薦類首次上板 → 何生轉告一次', mergeTriggerGigs('film_harbour')===1 && toasts.length===1 && toasts[0].indexOf('何生轉告')===0 && toasts[0].indexOf('陸柏言')>=0 && toasts[0].indexOf('維港電影')>=0, toasts[0]||'');
ok('T5 第二次開板唔再通知（冪等）', mergeTriggerGigs('film_harbour')===0 && toasts.length===1);
S = freshS();
toasts.length = 0;
S.fame = 60;
GIGS = [deepClone(gigById('gig_1991_film_210'))]; /* fame ≥40，film_lion（暑期大製作頂位） */
ok('T5 非引薦類 → 情報站口徑', mergeTriggerGigs('film_lion')===1 && toasts.length===1 && toasts[0].indexOf('情報站')===0 && toasts[0].indexOf('邀約通告')>=0, toasts[0]||'');
S = freshS();
toasts.length = 0;
S.mockCredits.push({ id:'credit_enc83_luk_patron', debtor:'陸柏言', title:'天王引薦', line:'x', status:'未收' });
GIGS = [deepClone(gigById('gig_1991_film_101'))];
gigSeasonHidden88 = function(){ return true; }; /* 未入季節窗 */
ok('T5 未入季節窗 → 唔通知住（等入窗先講）', mergeTriggerGigs('film_harbour')===0 && toasts.length===0 && !S.flags['triggerNotified_gig_1991_film_101']);
gigSeasonHidden88 = function(){ return false; };
ok('T5 入窗之後先通知', mergeTriggerGigs('film_harbour')===1 && toasts.length===1);
S = freshS();
toasts.length = 0;
S.mockCredits.push({ id:'credit_enc83_luk_patron', debtor:'陸柏言', title:'天王引薦', line:'x', status:'未收' });
GIGS = [deepClone(gigById('gig_1991_film_101'))];
ok('T5 唔同地點開板唔通知（loc 對唔上）', mergeTriggerGigs('film_lion')===0 && toasts.length===0);

/* ---------- T6：G-L2／G-NGAI-3 ---------- */
S = freshS();
ok('T6 G-L2 未持債 → 唔開', triggerGigOn(gigById('gig_1992_film_202'))===false);
S.mockCredits.push({ id:'credit_wf3_comedy_crew', debtor:'廖炳星', title:'喜劇組熟人', line:'x', status:'未收' });
ok('T6 G-L2 持 credit_wf3_comedy_crew → 開（唔經舊 WF3 池）', triggerGigOn(gigById('gig_1992_film_202'))===true);
S = freshS();
ok('T6 G-NGAI-3 未持債 → 唔開', triggerGigOn(gigById('gig_1992_film_101'))===false);
S.mockCredits.push({ id:'credit_enc83_ngai_meal', debtor:'魏詠男', title:'一餐飯', line:'x', status:'未收' });
ok('T6 G-NGAI-3 持 credit_enc83_ngai_meal → 開（唔經舊 FAVOR_DUE 池）', triggerGigOn(gigById('gig_1992_film_101'))===true);
S = freshS();
S.mockCredits.push({ id:'credit_wf3_comedy_crew', debtor:'廖炳星', title:'喜劇組熟人', line:'x', status:'未收' });
GIGS = [deepClone(gigById('gig_1992_film_202'))];
ok('T6 G-L2 上板（film_lion，1992 夏）', gigsForLocSeasonBoard('film_lion', '夏').some(g=>g.id==='gig_1992_film_202'));

/* ---------- T7：D-14——v20a267：mergeIntelGigs／INTEL_HIDDEN_GIGS 已刪；
   《星夜迷離》只行通用 rel trigger（星好感 S.stars），唔留雙重閘 ---------- */
const gXingye = gigs.filter(g=>(g.title||'').indexOf('星夜迷離')>=0);
ok('T7 v232 新庫有《星夜迷離》通告（第 241 張，經通用 trigger 系統；v252 重編號 tv_122→tv_203）', gXingye.length===1 && gXingye[0].id==='gig_1991_tv_203');
ok('T7《星夜迷離》觸發＝陸好感 ≥25（T2）', gXingye.length===1 && gXingye[0].trigger && gXingye[0].trigger.kind==='rel' && gXingye[0].trigger.npcId==='luk_baakyin' && gXingye[0].trigger.relMin===25);
ok('T7 唔留雙重閘：mergeIntelGigs 已刪', html.indexOf('mergeIntelGigs')<0);
ok('T7 唔留雙重閘：INTEL_HIDDEN_GIGS 已刪', html.indexOf('INTEL_HIDDEN_GIGS')<0);
ok('T7 唔留雙重閘：gig_intel_lu_standin 已清', html.indexOf('gig_intel_lu_standin')<0);
S = freshS();
GIGS = [];
S.stars.luk_baakyin = { fav: 10 };
ok('T7 星好感 10（T1）→《星夜迷離》唔開', triggerGigOn(gigById('gig_1991_tv_203'))===false);
S.stars.luk_baakyin = { fav: 25 };
ok('T7 星好感 25（T2）→《星夜迷離》開（triggerGigOn 主路徑）', triggerGigOn(gigById('gig_1991_tv_203'))===true);
S.stars.luk_baakyin = { fav: 0 };
ok('T7 星好感跌返 0 →《星夜迷離》唔開', triggerGigOn(gigById('gig_1991_tv_203'))===false);

/* ---------- T8：BR89 13 張＋獎項對照表 ---------- */
const BR89_EXPECT = {
  gig_1991_film_101:'credit_enc83_luk_patron', gig_1991_variety_203:'credit_enc84_pang_patron',
  gig_1992_rec_106:'credit_enc84_ching_patron', gig_1991_film_103:'credit_enc79_liu_priority',
  gig_1992_film_103:'credit_enc83_liu_patron', gig_1991_film_211:'credit_enc83_mak_patron',
  gig_1992_tv_105:'credit_enc83_yip_patron', gig_1992_rec_205:'credit_enc83_gu_patron',
  gig_1991_ad_102:'credit_enc84_so_patron', gig_1991_film_213:'credit_enc84_chung_patron',
  gig_1992_rec_111:'credit_enc83_lok_patron', gig_1991_film_212:'credit_enc83_ngai_patron',
  gig_1992_film_206:'credit_enc83_chai_patron'
};
const br89Keys = Object.keys(BR89_PATRON_OF_GIG);
ok('T8 BR89 映射 13 張', br89Keys.length===13, 'n='+br89Keys.length);
ok('T8 BR89 13 對逐對啱（SPEC §3.5A）', br89Keys.every(k=>BR89_PATRON_OF_GIG[k]===BR89_EXPECT[k]) && Object.keys(BR89_EXPECT).every(k=>BR89_PATRON_OF_GIG[k]===BR89_EXPECT[k]));
ok('T8 舊 gig_br89_* id 已清', !br89Keys.some(k=>/^gig_br89_/.test(k)) && html.indexOf('gig_br89_patron_luk')<0);
ok('T8 BR89 13 張全部喺新庫（v20a254 重對後，舊消失 id gig_1991_variety_108 已換 gig_1991_variety_203）', br89Keys.filter(k=>!!gigById(k)).length===13 && !gigById('gig_1991_variety_108'),
  'missing=gig_1991_variety_108');
/* v20a254 修復：BR89 映射由舊庫 13 對重對做新庫 13 對（全部 REUSE 新庫已有 credit-trigger
   gig，0 張新開；舊《江河歲月》等 4 張同名直對，其餘 9 張按舊 title＋全文＋trigger 逐對
   還原——詳見 index.html BR89 註解）。廖炳星引薦有兩張新庫 gig（film_109／1991＋
   film_103／1992），BR89 表只取 film_103（1992 電影，同舊年＋媒介）做 canonical，
   film_109 行通用 credit 規則照開。
   v20a274：上面 13 對之中 6 對由新開 5 張＋rec_111 接駁取代（舊 6 張 trigger 已拆），總數維持 13 對。 */
const br89Match = br89Keys.filter(k=>{ const g = gigById(k); return g && g.trigger && g.trigger.kind==='credit' && g.trigger.creditId===BR89_PATRON_OF_GIG[k]; });
const br89Mismatch = br89Keys.filter(k=>{ const g = gigById(k); return g && g.trigger && g.trigger.kind==='credit' && g.trigger.creditId!==BR89_PATRON_OF_GIG[k]; });
const br89NoTrig = br89Keys.filter(k=>{ const g = gigById(k); return g && !(g.trigger && g.trigger.kind==='credit'); });
ok('T8 BR89 映射同新庫 credit trigger 13 張全部對得上（v20a274 取代）',
  br89Match.length===13 && br89Mismatch.length===0 && br89NoTrig.length===0,
  'match=' + br89Match.length + ' mismatch=' + br89Mismatch.join(',') + ' noTrig=' + br89NoTrig.length);
ok('T8 G-G2「觸發通告變 26 張」唔喺 code／註解入面', html.indexOf('變 26 張')<0);
const awardMap = GIG_TRIGGER_AWARD_MAP229;
ok('T8 獎項對照表 15 個新庫 id 齊', Object.keys(awardMap).length===15);
ok('T8 直接對應 8 個（film／tv 男主＋男配、音樂新人、廣告男主＋男配）',
  awardMap.award_film_best_actor.catId==='cat_film_lead_m' && awardMap.award_film_best_supporting.catId==='cat_film_support_m' &&
  awardMap.award_tv_best_actor.catId==='cat_tv_lead_m' && awardMap.award_tv_best_supporting.catId==='cat_tv_support_m' &&
  awardMap.award_music_best_newcomer.catId==='cat_music_newcomer' && awardMap.award_ad_best_actor.catId==='cat_ad_lead_m' &&
  awardMap.award_ad_best_supporting.catId==='cat_ad_support_m' && awardMap.award_film_best_actress.catId==='cat_film_lead_f');
ok('T8 典禮級 5 個（電影／電視／廣告新人＋音樂大碟／歌曲，catId null）',
  awardMap.award_film_best_newcomer.catId===null && awardMap.award_tv_best_newcomer.catId===null &&
  awardMap.award_ad_best_newcomer.catId===null && awardMap.award_music_best_album.catId===null &&
  awardMap.award_music_best_song.catId===null);
ok('T8 4 張典禮級觸發通告對返啱典禮',
  awardMap.award_film_best_newcomer.ceremonyId==='award_harbour_film' &&
  awardMap.award_music_best_album.ceremonyId==='award_golddisc_music' &&
  awardMap.award_music_best_song.ceremonyId==='award_golddisc_music' &&
  awardMap.award_ad_best_newcomer.ceremonyId==='award_harbour_ad');

/* ---------- T9：G-9（1992 金碟夜喺遊戲期內） ---------- */
const schema = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'SCHEMA_AWARDS_CEREMONY_v1.json'), 'utf8'));
const gold = (schema.ceremonies||[]).find(c=>c.id==='award_golddisc_music');
ok('T9 1992 金碟夜係夏季典禮（weekMinSoft 16，約 1992 年 6 月，遊戲結束之前）',
  !!gold && gold.season==='夏' && Number(gold.weekMinSoft)===16);
S = freshS();
S.awardsResults['1992/award_golddisc_music'] = { year:1992, won:true, nominated:true, cats:{ cat_music_singer_m:'won' } };
ok('T9 1992 金碟夜得獎 → 1992 秋／冬唱片觸發通告開得到（合成樣本，見 T3）',
  triggerGigOn(SYN_AWARD.musicAlbum92)===true && triggerGigOn(SYN_AWARD.musicSong92)===true);

/* ---------- T10：trigger 過 normalize 唔跌 ---------- */
try{
  const tfA = html.indexOf('/* ==== v20a55 TEXTFIX');
  const tfB = html.indexOf('async function refreshCopyPacksFromDisk(){');
  const TF_SRC = html.slice(tfA, tfB);
  const CONSTS = ['STAT_LABEL', 'POSTER59_STAR_IDS', 'GIG_REQ_KEYS88', 'SHOOT_DAYS',
    'ROLE_SCALE_BAND', 'DUR90_OLD_BAND', 'DUR90_DAILY'];
  const FNS = ['years66ShiftYear', 'years66ShiftText', 'years66Walk', 'years66GigRemap', 'normalizeGigRecord',
    'bridge56NormalizeGig', 'boardNotePlayerOk', 'looksLikeEraId', 'humanizeEraId',
    'clamp', 'resolveRoleScale', 'shootBandFor', 'effectiveShootDays', 'effectiveShootWeekdays',
    'effectiveShootDeadlineDays', 'gigPayExact', 'dur90RoundPay', 'dur90CalibrateGig',
    'clampEntryReqToTemplate', 'entryGigPool229', 'mergeEntryGigsIntoPool', 'mergeSoftBridgeGigs'];
  const WORLD_SRC = TF_SRC + '\n' + CONSTS.map(c=>{
    const s = extractConstVar(c); return s ? s : 'var '+c+' = undefined;';
  }).join('\n') + '\n' + FNS.map(f=>extractFn(f) || '').join('\n');
  const W = new Function('var START = { y:1990, m:1, d:1 }; var S = null; var GIGS = [];\n' + WORLD_SRC + '\n; return { normalizeGigRecord };')();
  const normedTrig = deepClone(trig).map(g=>{ g.__y66w = 1; return W.normalizeGigRecord(g); });
  ok('T10 normalize 後 33 張 trigger 全部留返', normedTrig.every(g=>g.trigger && g.trigger.kind));
  ok('T10 normalize 後 trigger 內容一字唔郁', normedTrig.every((g,i)=>JSON.stringify(g.trigger)===JSON.stringify(trig[i].trigger)));
  ok('T10 normalize 後年份唔郁', normedTrig.every((g,i)=>g.year===trig[i].year));
}catch(e){ ok('T10 normalize 沙盒 ('+e.message+')', false); }

/* ---------- T11：真季節窗 ---------- */
try{
  eval(extractConstVar('GIG_SEASON_SPAN88'));
  eval(extractConstVar('GIG_SEASON_LEAD88'));
  eval(extractFn('seasonRank'));
  eval(extractFn('gigSeasonEarlyVisible88'));
  eval(extractFn('gigSeasonHidden88'));
  var dateObj = function(){ return new Date(1991, 8, 1); }; /* 1991-09-01 */
  const gAutumn = gigById('gig_1991_film_101'); /* 1991 秋《江河歲月》（舊 film_109 已改做 credit 春） */
  ok('T11 1991 秋觸發通告喺 1991-09-01 入季節窗', gigSeasonHidden88(gAutumn, '秋')===false);
  dateObj = function(){ return new Date(1991, 0, 1); }; /* 1991-01-01 */
  ok('T11 1991 秋觸發通告喺 1991-01-01 未入季節窗', gigSeasonHidden88(gAutumn, '冬')===true);
}catch(e){ ok('T11 真季節窗沙盒 ('+e.message+')', false); }

console.log(fails.length ? ('\nGIG229 TRIGGER: '+fails.length+' FAIL') : '\nGIG229 TRIGGER: ALL PASS');
process.exit(fails.length ? 1 : 0);
