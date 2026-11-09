// v20a38 收尾修復包・邏輯／真路徑測試
//   段一 (a)：跨次記憶——真 buildPostShootRewardPack 連組多份，同一 channel 唔准喺
//             最近 3 次內重複（池夠大嗰啲 channel）；舊存檔（冇欄／爛欄）組裝唔爆。
//   段二 (b)：場景適配——真組裝：碼頭外景永不抽夜晚廠景卡；夜晚廠景工抽得返；
//             夜晚外景唔抽「曬足成日」卡；推唔出場景嗰陣唔過濾。
//   段三 (c)：手帳拍攝中卡——真 workItems 渲染：新 record 出齊數額、
//             舊 record（冇待入帳數）出定性版、唔出 NaN。
// 用法：node tests/test_wrap38_logic.js
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');

let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }

function extractFn(decl){
  const i = html.indexOf(decl);
  if(i < 0) throw new Error('fn not found: ' + decl);
  let j = html.indexOf('{', i), depth = 0, k = j;
  for(; k < html.length; k++){
    if(html[k] === '{') depth++;
    else if(html[k] === '}'){ depth--; if(depth === 0){ k++; break; } }
  }
  return html.slice(i, k);
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

/* 共用 sandbox：模擬線上 STUB_POST_SHOOT_REWARDS_v1.json 真實形狀（同 verify37 段二） */
function psrSandbox(){
  var S = { dayIndex: 30, fame: 20, postShootRewards: [] };
  var FREEPLAY_FW = { postShootSchema: null, postShootRewards: {
    templates: {
      press: [
        { id:'press_film_01', matchTypes:['電影'], paperName:'娛樂版', headline:'新人臨記殺青，版面留低一格', dek:'x' },
        { id:'press_tv_01', matchTypes:['電視劇','綜藝'], paperName:'娛樂版', headline:'廠景殺青，娛樂版順手記一筆', dek:'x' },
        { id:'press_rec_01', matchTypes:['唱片通告'], paperName:'樂版', headline:'錄音室散場，樂版一句帶過', dek:'x' },
        { id:'press_ad_01', matchTypes:['廣告'], paperName:'廣告版', headline:'廣告殺青，報紙夾頁有你一眼', dek:'x' },
        { id:'press_any_01', matchTypes:[], paperName:'娛樂版', headline:'通告殺青，娛樂版留低一行', dek:'x' }
      ],
      news: [
        { id:'news_film_01', matchTypes:['電影'], outlet:'娛樂快訊', line:'電影組殺青消息：有新人臨記入鏡完成。' },
        { id:'news_tv_01', matchTypes:['電視劇','綜藝'], outlet:'娛樂快訊', line:'電視台組製收工，臨記檔期順利殺青。' },
        { id:'news_rec_01', matchTypes:['唱片通告'], outlet:'娛樂快訊', line:'錄音室散場，唱片通告順利完成。' },
        { id:'news_any_01', matchTypes:[], outlet:'娛樂快訊', line:'通告殺青：新人又過一關。' }
      ],
      streetFans: [
        { id:'fans_01', matchTypes:[], place:'街上', line:'轉角突然幾個人圍住問。', stageVolumeDelta:0 },
        { id:'fans_02', matchTypes:['電影','電視劇'], place:'街上', line:'有人遞紙筆過嚟。', stageVolumeDelta:0 },
        { id:'fans_03', matchTypes:['唱片通告','廣告'], place:'街口', line:'等燈時有人拍你膊頭。', stageVolumeDelta:0 }
      ],
      metrics: [
        { id:'metric_box_01', matchTypes:['電影'], metricKind:'boxOffice', valueLine:'首輪口碑：街坊開始問檔期', blurb:'x' },
        { id:'metric_rate_01', matchTypes:['電視劇','綜藝'], metricKind:'ratings', valueLine:'同檔時段：有觀眾問邊個臨記', blurb:'收視唔係你一個人，但入鏡位開始有人留意。' },
        { id:'metric_sales_01', matchTypes:['唱片通告'], metricKind:'sales', valueLine:'舖頭返貨：有人問封面邊個', blurb:'x' },
        { id:'metric_att_01', matchTypes:['廣告'], metricKind:'attention', valueLine:'品牌回訪：造型照有人截圖', blurb:'x' },
        { id:'metric_any_01', matchTypes:[], metricKind:'attention', valueLine:'本單完成後關注度微升', blurb:'x' }
      ]
    },
    fallbacks: { press:{ paperName:'娛樂版', headline:'通告殺青', dek:'又完成一單拍攝。' },
      news:{ outlet:'娛樂快訊', line:'殺青完成。' },
      streetFans:{ place:'街上', line:'有人多望你兩眼。', stageVolumeDelta:0 },
      metrics:{ label:'關注度', valueLine:'關注度＋', blurb:'履歷又多一筆。' } },
    metricKindLabels: { boxOffice:'票房關注', ratings:'收視關注', sales:'銷量關注', attention:'關注度' }
  } };
  eval(extractConst('PSR_EXTRA_TEMPLATES_35').replace('const PSR_EXTRA_TEMPLATES_35', 'var PSR_EXTRA_TEMPLATES_35'));
  eval(extractConst('_psrLastPick35').replace('const _psrLastPick35', 'var _psrLastPick35'));
  eval(extractConst('PSR_SCENE_TAGS38').replace('const PSR_SCENE_TAGS38', 'var PSR_SCENE_TAGS38'));
  const FNS = ['psrRecent38','psrPickNoRepeat35','augmentPostShootRewards35','postShootPickTemplate',
    'postShootCopyLine','postShootDisplayTitle','postShootMetricKindForType','buildPostShootRewardPack',
    'psrSceneForShoot38','psrSceneFilter38'];
  const api = {};
  for(let i = 0; i < FNS.length; i++){ eval(extractFn('function ' + FNS[i])); api[FNS[i]] = eval(FNS[i]); }
  return { S, FREEPLAY_FW, api };
}
function noRepeatWithin(seq, w){
  for(let i = 0; i < seq.length; i++){
    for(let j = Math.max(0, i - w); j < i; j++) if(seq[j] === seq[i]) return false;
  }
  return true;
}

/* ================================================================
   段一 (a)：跨次記憶（S.psrRecent38）
   ================================================================ */
(function(){
  const sb = psrSandbox();
  const build = sb.api.buildPostShootRewardPack;
  sb.api.augmentPostShootRewards35();
  const S = sb.S;
  /* pressSeed 冇 templateId → 用 headline 反查（press 池 headline 互不相同） */
  const headToId = {};
  sb.FREEPLAY_FW.postShootRewards.templates.press.forEach(t => { headToId[t.headline] = t.id; });

  const fansSeq = [], pressSeq = [], metricSeq = [];
  for(let i = 0; i < 24; i++){
    const pack = build({ gigId: 'w38a_' + i, type: '綜藝', workTitle: '試作騷' + i, title: '《試作騷' + i + '》群演' });
    (pack.cards || []).forEach(c => {
      if(c.channel === 'streetFans') fansSeq.push(c.meta.templateId);
      if(c.channel === 'metrics') metricSeq.push(c.meta.templateId);
    });
    pressSeq.push(headToId[pack.pressSeed.headline]);
  }
  ok('a1 fans 抽樣足夠（≥6 次）', fansSeq.length >= 6);
  ok('a2 fans（池 5 張）最近 3 次內唔重複', noRepeatWithin(fansSeq, 3));
  ok('a3 press（池 3 張）最近 2 次內唔重複', noRepeatWithin(pressSeq, 2));
  ok('a4 metrics（池 2 張）唔連續重複', noRepeatWithin(metricSeq, 1));
  ok('a5 記憶入咗存檔欄 S.psrRecent38（每 channel ≤3）',
    !!S.psrRecent38 && Array.isArray(S.psrRecent38.press) && S.psrRecent38.press.length >= 1 && S.psrRecent38.press.length <= 3
    && Array.isArray(S.psrRecent38.streetFans));
  ok('a6 記憶最新一張＝最後抽中嗰張', S.psrRecent38.press[0] === pressSeq[pressSeq.length - 1]);

  /* 舊存檔：完全冇 psrRecent38 欄（新 S 物件）→ 組裝唔爆、照出卡 */
  const sb2 = psrSandbox();
  sb2.api.augmentPostShootRewards35();
  delete sb2.S.psrRecent38;
  let threw = false, pack2 = null;
  try{ pack2 = sb2.api.buildPostShootRewardPack({ gigId: 'old1', type: '電影', workTitle: '舊戲', title: '《舊戲》路人' }); }catch(_e){ threw = true; }
  ok('a7 舊存檔（冇記憶欄）組裝唔爆＋有卡', !threw && !!pack2 && pack2.cards.length >= 1);

  /* 爛欄：psrRecent38 俾舊版／手誤寫到唔係陣列 → 唔爆 */
  const sb3 = psrSandbox();
  sb3.api.augmentPostShootRewards35();
  sb3.S.psrRecent38 = { press: 'garbage', metrics: 42 };
  threw = false; let pack3 = null;
  try{ pack3 = sb3.api.buildPostShootRewardPack({ gigId: 'old2', type: '電視劇', workTitle: '舊劇', title: '《舊劇》街坊' }); }catch(_e){ threw = true; }
  ok('a8 記憶欄爛值唔爆＋有卡', !threw && !!pack3 && pack3.cards.length >= 1);
})();

/* ================================================================
   段二 (b)：場景適配
   ================================================================ */
(function(){
  const sb = psrSandbox();
  const build = sb.api.buildPostShootRewardPack;
  sb.api.augmentPostShootRewards35();
  const NIGHT_STUDIO_HEAD = '深宵廠景煞科，新面孔企到尾';
  const OUTDOOR_DAY_HEAD = '外景煞科，新人臨記跟足全程';

  /* 碼頭日間外景（電視劇）：夜晚廠景卡永不出現 */
  let ferryBad = 0;
  for(let i = 0; i < 60; i++){
    const pack = build({ gigId: 'ferry38_' + i, type: '電視劇', workTitle: '天星碼頭', title: '《天星碼頭》過海路人' });
    if(pack.pressSeed.headline === NIGHT_STUDIO_HEAD) ferryBad++;
    (pack.cards || []).forEach(c => { if(c.meta && c.meta.templateId === 'psr35_press_tv_02') ferryBad++; });
  }
  ok('b1 《天星碼頭》60 份反響永不抽中夜晚廠景卡', ferryBad === 0);

  /* 夜晚廠景（電視劇）：嗰張卡入得返池 */
  let nightHits = 0;
  for(let i = 0; i < 60; i++){
    const pack = build({ gigId: 'ns38_' + i, type: '電視劇', workTitle: '深宵疑雲', title: '《深宵疑雲》廠景群演' });
    if(pack.pressSeed.headline === NIGHT_STUDIO_HEAD) nightHits++;
  }
  ok('b2 夜晚廠景工抽得返夜晚廠景卡（≥3 次／60）', nightHits >= 3);

  /* 日間外景（電影）：外景卡入池（press＋news 各驗） */
  let pressOut = 0, newsOut = 0;
  for(let i = 0; i < 60; i++){
    const pack = build({ gigId: 'od38_' + i, type: '電影', workTitle: '碼頭歲月', title: '《碼頭歲月》外景群戲' });
    if(pack.pressSeed.headline === OUTDOOR_DAY_HEAD) pressOut++;
    (pack.cards || []).forEach(c => { if(c.meta && c.meta.templateId === 'psr35_news_film_02') newsOut++; });
  }
  ok('b3 日間外景工抽得返 press 外景卡', pressOut >= 3);
  ok('b4 日間外景工抽得返 news 外景卡', newsOut >= 2);

  /* 夜晚外景（電影）：「曬足成日」卡永不出現，但純外景 news 卡唔受影響（唔喺度斷言次數，只驗唔死鎖） */
  let nightOutBad = 0, nightPacks = 0;
  for(let i = 0; i < 60; i++){
    const pack = build({ gigId: 'no38_' + i, type: '電影', workTitle: '猛鬼碼頭夜話', title: '《猛鬼碼頭夜話》夜半搬運工' });
    nightPacks++;
    if(pack.pressSeed.headline === OUTDOOR_DAY_HEAD) nightOutBad++;
    (pack.cards || []).forEach(c => { if(c.meta && c.meta.templateId === 'psr35_press_film_02') nightOutBad++; });
  }
  ok('b5 夜晚外景永不抽中「曬足成日」卡', nightOutBad === 0 && nightPacks === 60);

  /* 推唔出場景（冇關鍵字）：唔過濾——夜晚廠景卡仍然入到池 */
  let genericHits = 0;
  for(let i = 0; i < 60; i++){
    const pack = build({ gigId: 'gn38_' + i, type: '電視劇', workTitle: '試作劇', title: '《試作劇》街坊' });
    if(pack.pressSeed.headline === NIGHT_STUDIO_HEAD) genericHits++;
  }
  ok('b6 推唔出場景嗰陣唔過濾（夜晚廠景卡仍入池）', genericHits >= 3);
})();

/* ================================================================
   段三 (c)：手帳拍攝中卡（真 workItems）
   ================================================================ */
(function(){
  var S = { booked: [], shoots: [], dayIndex: 40 };
  eval(extractFn('function shootRemain'));
  eval(extractFn('function shootPendingLine38'));
  eval(extractFn('function workItems'));

  S.shoots = [{ id: 'sh_t1', gigId: 'g1', title: '《試作劇》街坊', totalDays: 3, doneDays: 1, pay: 1164, fame: 5, popularity: 17, locId: 'tvb_longmen' }];
  const items = workItems();
  const row = items.find(x => x.id === 'shoot:sh_t1');
  ok('c1 拍攝中卡有待入帳標示連正確數額', !!row && row.hint.indexOf('殺青後入帳：約酬 $1,164 · 聲望 +5 · 人氣 +17') >= 0);
  ok('c2 拍攝中卡保留原有檔期／進度字樣', !!row && row.hint.indexOf('檔期已定') >= 0 && row.hint.indexOf('進度 1/3') >= 0);

  /* 舊 record：冇 pay/fame/popularity → 定性版、冇 NaN、唔爆 */
  S.shoots = [{ id: 'sh_old', gigId: 'g2', title: '《舊劇》路人', totalDays: 2, doneDays: 0, locId: 'tvb_kowloon' }];
  let threw = false, row2 = null;
  try{ row2 = workItems().find(x => x.id === 'shoot:sh_old'); }catch(_e){ threw = true; }
  ok('c3 舊 record 渲染唔爆', !threw && !!row2);
  ok('c4 舊 record 出定性版「殺青後入帳」', !!row2 && row2.hint.indexOf('殺青後入帳') >= 0);
  ok('c5 舊 record 冇 NaN／冇約酬數字', !!row2 && row2.hint.indexOf('NaN') < 0 && row2.hint.indexOf('約酬') < 0);

  /* 半舊 record：得 pay → 出約酬、唔出 NaN */
  S.shoots = [{ id: 'sh_p', gigId: 'g3', title: '《半舊》路人', totalDays: 2, doneDays: 0, pay: 500, locId: 'x' }];
  const row3 = workItems().find(x => x.id === 'shoot:sh_p');
  ok('c6 半舊 record 出約酬＋冇 NaN', !!row3 && row3.hint.indexOf('約酬 $500') >= 0 && row3.hint.indexOf('NaN') < 0);
})();

console.log('');
if(fails.length){ console.log('FAILED: ' + fails.join(' | ')); process.exit(1); }
console.log('ALL PASS');
