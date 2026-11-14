// v20a214 NP214・殺青報紙＋WF3／story 報紙＋第二版厚度・邏輯測試（工人 3）
// 合約（用戶 2026-11-14 18:14／18:15 已拍板；樣本 v11 為設計權威）：
//   A base 閘：press94RoleClass == "base" 嘅殺青 → enqueueNewspaperFromWrap 回 null，
//     唔入隊、唔留去重 key、唔 claim 第一次點名；閘口係通告級別，唔係聲望。
//   B named 照舊：入隊＋排期（cardDay+1／publishDay+2）；fame<15 行 #104 淡紙
//     （「一名臨記」留返）；第一次真點名先加編輯按。
//   C 空隊列：淨係得 base 殺青到期嗰朝，pullDueNewspaperEdition 回 null，唔彈空報紙。
//   D 相片：named／anon 殺青報紙用通告作品海報（poster59Path：POSTER59 10 張＋
//     POSTER85 59 張，共 69 張有海報；其餘唔出相，唔亂配）；key 入 NEWS82_IMGS，
//     唔撞 WF3（E1–E6）／頒獎（np214_award_*）。
//   E WF3／story：同一隻 renderMorningPaperHtml——世界事件三段＋相、副題唔重複；
//     story 單段副題只出一次、冇相；buildNewspaperEdition 排序／摺疊唔郁。
//   F 第二版厚度：兩格真內容廣告（星光卡拉 OK／金龍茶餐廳，樣本 v11 原文），
//     渲染層出，唔入 shorts／傳聞／剪報。
//   G 邊欄：留返「影視娛樂」＋裝飾填充字，唔硬塞。
// 反證：pristine main（f58f19c）index 冇 np214*／press94 閘 → 抽取失敗 FAIL，唔 crash。
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
  if(cond){ console.log('PASS', name); }
  else { fails++; console.log('FAIL', name, extra||''); }
}
function countSub(s, sub){
  let n=0, i=0;
  while((i = s.indexOf(sub, i))>=0){ n++; i += sub.length; }
  return n;
}

const parts = [
  extractConst('PRESS94_STRONG_NAMED'), extractConst('PRESS94_BASE_LABEL'),
  extractConst('PRESS94_NAMED_LABEL'), extractConst('PRESS94_BASE_SCALES'),
  extractConst('PRESS94_NAMED_SCALES'), extractConst('POSTER85_IDS'),
  extractConst('NEWS82_EVENTS'), extractConst('PAPER_NAME_TIER_NAMED'),
  extractConst('PAPER_NAME_TIER_TITLED'),
  extractFn('press94ScaleOf'), extractFn('press94RoleClass'), extractFn('press94IsBaseRole'),
  extractFn('press94TierBadge'), extractFn('press94ClaimFirstNamed'),
  extractFn('newspaperMediumFromGigType'), extractFn('newspaperLookupGig'),
  extractFn('newspaperWrapSubject'), extractFn('newspaperWrapAngle'),
  extractFn('newspaperWrapFaceLines'), extractFn('newspaperWrapFadeLines'),
  extractFn('newspaperWrapFadeSubject'), extractFn('newspaperWrapLeadRelation'),
  extractFn('newspaperNameTier'), extractFn('newspaperPlayerRef'),
  extractFn('newspaperPickTemplate'), extractFn('newspaperCopyFromTemplate'),
  extractFn('newspaperFillPlayer'), extractFn('newspaperEventSeen'),
  extractFn('ensureNewspaperQueue'), extractFn('ensureNewspaperClippings'),
  extractFn('enqueueNewspaperItem'), extractFn('enqueueNewspaperFromWrap'),
  extractFn('newspaperDueItems'), extractFn('news82IsHead'), extractFn('news82EventById'),
  extractFn('buildNewspaperEdition'), extractFn('pullDueNewspaperEdition'),
  extractFn('newspaperEsc'), extractFn('renderMorningPaperHtml'),
  extractFn('poster85File'), extractFn('poster59Path'),
  extractFn('np214WrapPoster214'), extractFn('np214Page2Ads214')
];
ok('extract_all', parts.every(Boolean), parts.map((p,i)=>i+':'+!!p).join(','));
if(parts.every(Boolean)){
  const sandbox = `
var S = { dayIndex: 2, fame: 20, newspaperQueue: [], newspaperClippings: [], pendingMorningPaper: null, newspaperLastPresentedDay: null, press94FirstNamedDay: 0 };
var NEWS82_IMGS = { E1: 'data:image/webp;base64,FAKEE1', E2: 'data:image/webp;base64,FAKEE2', E3: 'data:image/webp;base64,FAKEE3', E4: 'data:image/webp;base64,FAKEE4', E5: 'data:image/webp;base64,FAKEE5', E6: 'data:image/webp;base64,FAKEE6' };
var POSTER59_IDS = { 'gig_1988_film_03': 1 };
var POSTER59_DATA = { 'gig_1988_film_03': 'data:image/webp;base64,FAKE59' };
var GIGS = [
  { id:'gig_1988_film_04', workTitle:'警網雄風', title:'警網雄風', roleLabel:'男主角', type:'電影', roleScale:'film_lead_big' },
  { id:'gig_1988_film_03', workTitle:'舊片', title:'舊片', roleLabel:'男主角', type:'電影', roleScale:'film_lead_big' },
  { id:'gig_1988_ad_01', workTitle:'離境大堂一封信', title:'離境大堂一封信', roleLabel:'機場臨記', type:'廣告', roleScale:'ad_av' },
  { id:'gig_1988_tv_99', workTitle:'處境劇', title:'處境劇', roleLabel:'男主角', type:'電視劇', roleScale:'tv_lead_long' },
  { id:'gig_1988_tv_cameo', workTitle:'某劇', title:'《某劇》', roleLabel:'', type:'電視劇', roleScale:'tv_cameo_short' },
  { id:'gig_1988_rec_99', workTitle:'新碟', title:'新碟', roleLabel:'專輯主唱', type:'唱片通告', roleScale:'rec_album' }
];
var FREEPLAY_FW = { newspaperStub: { templates: { wrap_success: [
  { id:'w_film', eventKey:'wrap_success.film', medium:'film', paperName:'娛樂版', headline:'', dek:'', clipLabel:'娛樂版・殺青', rumorEcho:'', fameDelta:2 },
  { id:'w_tv', eventKey:'wrap_success.tv', medium:'tv', paperName:'娛樂版', headline:'', dek:'', clipLabel:'娛樂版・殺青', rumorEcho:'', fameDelta:2 },
  { id:'w_ad', eventKey:'wrap_success.ad', medium:'ad', paperName:'廣告版', headline:'', dek:'', clipLabel:'廣告版・殺青', rumorEcho:'', fameDelta:2 },
  { id:'w_any', eventKey:'wrap_success.any', medium:'any', paperName:'娛樂版', headline:'', dek:'', clipLabel:'娛樂版・殺青', rumorEcho:'', fameDelta:1 }
]}}};
function postShootDisplayTitle(o){ o=o||{}; return o.workTitle || o.title || ''; }
function saveQ(){}
`;
  eval(sandbox + '\n' + parts.join('\n'));
  const resetQ = ()=>{ S.newspaperQueue=[]; S.newspaperClippings=[]; S.pendingMorningPaper=null; S.newspaperLastPresentedDay=null; };
  const wrapSh = (gigId, roleLabel, type, title)=>({ gigId: gigId, type: type, title: title||'', roleLabel: roleLabel });
  const wrapPack = (day, gigType)=>({ dayIndex: day, gigType: gigType });

  // ---- (a) base 閘 ----
  resetQ(); S.fame = 20; S.press94FirstNamedDay = 0;
  const b1 = enqueueNewspaperFromWrap(wrapSh('gig_1988_ad_01', '機場臨記', '廣告'), wrapPack(2, '廣告'), { persist:false });
  ok('A01_base_gig_role_null', b1===null, String(b1 && b1.headline));
  const b2 = enqueueNewspaperFromWrap(wrapSh('gig_unknown_x', '唱片幫工', '唱片通告'), wrapPack(2, '唱片通告'), { persist:false });
  ok('A02_base_label_hint_null', b2===null);
  ok('A03_base_no_queue', S.newspaperQueue.length===0, String(S.newspaperQueue.length));
  const b3 = enqueueNewspaperFromWrap(wrapSh('gig_unknown_x', '唱片幫工', '唱片通告'), wrapPack(2, '唱片通告'), { persist:false });
  ok('A04_base_retry_still_null', b3===null);
  const b4 = enqueueNewspaperFromWrap(wrapSh('gig_1988_tv_cameo', '', '電視劇', '《某劇》'), wrapPack(2, '電視劇'), { persist:false });
  ok('A05_base_scale_only_null', b4===null);
  const b5 = enqueueNewspaperFromWrap({ gigId:'gig_unknown_z', type:'電視劇', title:'《某劇》過海路人', roleLabel:'過海路人' }, wrapPack(2, '電視劇'), { persist:false });
  ok('A06_base_scale_label_null', b5===null);
  ok('A07_base_no_first_claim', (S.press94FirstNamedDay|0)===0, String(S.press94FirstNamedDay));
  ok('A08_base_fame20_still_null', b1===null && S.fame===20);

  // ---- (b) named 照舊＋淡紙「一名臨記」留返 ----
  resetQ(); S.fame = 20; S.press94FirstNamedDay = 0;
  const n1 = enqueueNewspaperFromWrap(wrapSh('gig_1988_film_04', '男主角', '電影'), wrapPack(2, '電影'), { persist:false });
  ok('B01_named_enqueued', !!n1 && n1.eventKey==='wrap:gig_1988_film_04:2' && n1.source==='wrap', n1 && n1.eventKey);
  ok('B02_named_schedule', !!n1 && (n1.enqueuedDay|0)===3 && (n1.publishDay|0)===4, n1 && (n1.enqueuedDay+'/'+n1.publishDay));
  ok('B03_named_fame', !!n1 && n1.fameDelta===2, n1 && String(n1.fameDelta));
  ok('B04_first_named_claim', !!n1 && n1.firstPress94===true && String(n1.dek||'').indexOf('編輯按')>=0 && (S.press94FirstNamedDay|0)===2);
  const n2 = enqueueNewspaperFromWrap(wrapSh('gig_1988_tv_99', '男主角', '電視劇'), wrapPack(3, '電視劇'), { persist:false });
  ok('B05_second_named_no_claim', !!n2 && n2.firstPress94!==true && String(n2.dek||'').indexOf('編輯按')<0);
  S.fame = 5;
  const n3 = enqueueNewspaperFromWrap(wrapSh('gig_1988_film_03', '男主角', '電影'), wrapPack(2, '電影'), { persist:false });
  ok('B06_anon_still_paper', !!n3 && n3.fameDelta===0, n3 && String(n3.fameDelta));
  ok('B07_anon_keeps_yiming', !!n3 && ((n3.headline||'')+(n3.dek||'')).indexOf('一名臨記')>=0, n3 && (n3.headline||''));
  ok('B08_anon_has_photo', !!n3 && n3.imgKey==='np214_poster_1988_film_03', n3 && n3.imgKey);
  resetQ(); S.fame = 20;
  const n4 = enqueueNewspaperFromWrap(wrapSh('gig_1988_rec_99', '專輯主唱', '唱片通告'), wrapPack(2, '唱片通告'), { persist:false });
  ok('B09_named_no_poster_no_img', !!n4 && n4.imgKey==='', n4 && JSON.stringify(n4.imgKey));
  ok('B10_named_with_poster_img', !!n1 && n1.imgKey==='np214_poster_1988_film_04', n1 && n1.imgKey);

  // ---- (c) 空隊列唔出晨報 ----
  resetQ(); S.fame = 20; S.dayIndex = 2;
  enqueueNewspaperFromWrap(wrapSh('gig_1988_ad_01', '機場臨記', '廣告'), wrapPack(2, '廣告'), { persist:false });
  S.dayIndex = 4;
  ok('C01_base_only_no_due', newspaperDueItems(4).length===0);
  ok('C02_base_only_no_edition', pullDueNewspaperEdition()===null);
  ok('C03_base_only_no_pending', !S.pendingMorningPaper);
  resetQ(); S.dayIndex = 6;
  const n5 = enqueueNewspaperFromWrap(wrapSh('gig_1988_tv_99', '男主角', '電視劇'), wrapPack(6, '電視劇'), { persist:false });
  S.dayIndex = 7;
  ok('C04_named_not_due_day7', pullDueNewspaperEdition()===null, 'publishDay='+(n5 && n5.publishDay));
  S.dayIndex = 8;
  const edC = pullDueNewspaperEdition();
  ok('C05_named_due_day8', !!edC && String(edC.headline||'').indexOf('處境劇')>=0, edC && edC.headline);

  // ---- (d) 海報 helper ----
  const p1 = np214WrapPoster214('gig_1988_film_04');
  ok('D01_poster85_file', !!p1 && p1.key==='np214_poster_1988_film_04' && p1.src==='assets/posters/poster-1988_film_04.webp', p1 && JSON.stringify(p1));
  ok('D02_poster_registered', NEWS82_IMGS['np214_poster_1988_film_04']==='assets/posters/poster-1988_film_04.webp');
  ok('D03_poster59_data', (np214WrapPoster214('gig_1988_film_03')||{}).src==='data:image/webp;base64,FAKE59');
  ok('D04_no_poster_null', np214WrapPoster214('gig_1988_ad_01')===null && np214WrapPoster214('gig_no_such')===null && np214WrapPoster214('')===null && np214WrapPoster214(null)===null);
  ok('D05_no_key_collision', (np214WrapPoster214('gig_1988_film_04')||{}).key!=='E1' && (np214WrapPoster214('gig_1988_film_04')||{}).key!=='np214_award_awi' && NEWS82_IMGS.E1==='data:image/webp;base64,FAKEE1');

  // ---- (e) WF3／story 渲染 ----
  const worldEd = { headline:'E1頭條', dek:'', paras:['世界第一段。','世界第二段。','世界第三段。'], imgKey:'E1', worldId:'E1', shorts:[], fameDelta:0, dateLabel:'1990年1月1日 星期一', paperName:'娛樂版' };
  const htmlW = renderMorningPaperHtml(worldEd);
  ok('E01_world_three_paras', countSub(htmlW, '世界第一段。')===1 && countSub(htmlW, '世界第二段。')===1 && countSub(htmlW, '世界第三段。')===1);
  ok('E02_world_photo', htmlW.indexOf('data:image/webp;base64,FAKEE1')>=0);
  ok('E03_world_no_dek_strip', htmlW.indexOf('np214-dek')<0);
  ok('E04_world_fame_flat', htmlW.indexOf('聲望未有變動')>=0);
  const worldShort = { eventKey:'world:E1', paperName:'娛樂版', headline:'E1頭條', dek:'世界第一段。世界第二段。世界第三段。', source:'world', imgKey:'E1' };
  const wrapHead = { headline:'警網雄風殺青', dek:'通告殺青。', shorts:[worldShort], fameDelta:2, dateLabel:'1990年1月1日 星期一', paperName:'娛樂版' };
  const htmlWS = renderMorningPaperHtml(wrapHead);
  ok('E05_world_short_once', countSub(htmlWS, 'E1頭條')===1 && htmlWS.indexOf('data:image/webp;base64,FAKEE1')>=0);
  const storyEd = { headline:'劇情見報頭條', dek:'劇情副題一行。', shorts:[], fameDelta:2, dateLabel:'1990年1月1日 星期一', paperName:'娛樂版' };
  const htmlS = renderMorningPaperHtml(storyEd);
  ok('E06_story_dek_once', countSub(htmlS, '劇情副題一行。')===1);
  ok('E07_story_no_photo', htmlS.indexOf('<img')<0);
  ok('E08_story_fame', htmlS.indexOf('聲望 +2')>=0);
  const storyShort = { eventKey:'story:C5:honest', paperName:'娛樂版', headline:'坦率見報', dek:'劇情副題一行。', source:'story' };
  const htmlSS = renderMorningPaperHtml({ headline:'頭條', dek:'主文。', shorts:[storyShort], fameDelta:0, dateLabel:'1990年1月1日 星期一', paperName:'娛樂版' });
  ok('E09_story_short_once', countSub(htmlSS, '坦率見報')===1 && countSub(htmlSS, '劇情副題一行。')===1);
  const edWorldFirst = buildNewspaperEdition([
    { eventKey:'wrap:x:1', source:'wrap', enqueuedDay:1, publishDay:2, fameDelta:2, paperName:'娛樂版', headline:' wrap頭條', dek:'wrap。', clipLabel:'', rumorEcho:'' },
    { eventKey:'world:E1', source:'world', enqueuedDay:1, publishDay:2, fameDelta:0, paperName:'娛樂版', headline:'E1頭條', dek:'', clipLabel:'', rumorEcho:'', paras:['一','二','三'], imgKey:'E1', worldId:'E1' }
  ], 2);
  ok('E10_world_first_kept', edWorldFirst.source==='world' && String(edWorldFirst.headline||'').indexOf('E1頭條')>=0 && (edWorldFirst.paras||[]).length===3 && edWorldFirst.imgKey==='E1');
  const many = [];
  for(let i=0;i<6;i++) many.push({ eventKey:'wrap:m'+i+':3', source:'wrap', enqueuedDay:3, publishDay:4, fameDelta:1, paperName:'娛樂版', headline:'則'+i, dek:'短', clipLabel:'', rumorEcho:'' });
  const edBig = buildNewspaperEdition(many, 4);
  ok('E11_overflow_fold_kept', (edBig.shorts||[]).length<=4 && (edBig.shorts||[]).some(s=>s && s.source==='summary' && String(s.headline||'').indexOf('同日還有 2 則')>=0), 'shorts='+(edBig.shorts||[]).length);

  // ---- (f) 第二版廣告 ----
  const ads = np214Page2Ads214();
  ok('F01_ads_content', ads.indexOf('星光卡拉 OK')>=0 && ads.indexOf('歡唱 $38／小時')>=0 && ads.indexOf('旺角彌敦道 123 號 3 樓')>=0 && ads.indexOf('電話 388 4567')>=0 && ads.indexOf('金龍茶餐廳')>=0 && ads.indexOf('菠蘿油')>=0 && ads.indexOf('絲襪奶茶')>=0 && ads.indexOf('通宵營業')>=0);
  ok('F02_ads_two_boxes', countSub(ads, 'np214-adbox')===2 && ads.indexOf('碟市')<0 && ads.indexOf('臨記席')<0);
  const htmlAds = renderMorningPaperHtml({ headline:'頭條', dek:'主文。', shorts:[{ eventKey:'wrap:s:1', paperName:'娛樂版', headline:'短訊頭條', dek:'短訊。', source:'wrap' }], fameDelta:1, dateLabel:'1990年1月1日 星期一', paperName:'娛樂版' });
  ok('F03_ads_on_page2', htmlAds.indexOf('data-np214-page="2"')>=0 && htmlAds.indexOf('星光卡拉 OK')>=0 && htmlAds.indexOf('金龍茶餐廳')>=0);
  const htmlNoShorts = renderMorningPaperHtml({ headline:'頭條', dek:'主文。', shorts:[], fameDelta:1, dateLabel:'1990年1月1日 星期一', paperName:'娛樂版' });
  ok('F04_no_page2_no_ads', htmlNoShorts.indexOf('data-np214-page="2"')<0 && htmlNoShorts.indexOf('星光卡拉 OK')<0);
  ok('F05_ads_not_in_edition_data', (edBig.shorts||[]).every(s=>s && String(s.headline||'').indexOf('卡拉 OK')<0 && String(s.headline||'').indexOf('金龍茶餐廳')<0));

  // ---- (g) 邊欄留返 ----
  ok('G01_sidebar_kept', htmlW.indexOf('影視娛樂')>=0 && htmlW.indexOf('np214-filler-v')>=0);
}
console.log(fails ? ('RESULT FAIL '+fails) : 'RESULT PASS');
process.exit(fails ? 1 : 0);
