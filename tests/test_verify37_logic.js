// v20a37 驗證修復包・邏輯／真路徑測試
// 宗旨（吸取 v20a34/35 教訓）：唔齋 call 被修函數餵假數據——每段都行玩家真路徑：
//   段一：真 StoryOC.listOpen offer → 真 StoryPlay.start/skipToChoices/pickChoice → 真 showResult 畫面（捕捉 modal body）
//   段二：真 buildPostShootRewardPack 組裝 ×30＋真 newspaperWrapFaceLines
//   段三：真 doAudition 獲聘 → 真 scheduleShoot → 真 resolvePlannedDay 逐日行到殺青（item 3/5/6b）＋真訓練日 ×20（item 6a）
//   段四：真 renderNotebook（DOM stub 捕捉標頭）
//   段五：真 gigGap* 顯示路徑（item 8）
//   段六：真 applyMockAsk 打聽路徑（item 9）
// 用法：node tests/test_verify37_logic.js
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const storyPack = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'story_detail_c1_to_c17.json'), 'utf8'));
const gateStubPack = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'behavior_gate_c1_c5.json'), 'utf8'));

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
function extractConstLine(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('const line not found: ' + name);
  return html.slice(i, html.indexOf('\n', i)) + ';';
}
function extractIIFE(decl){
  const i = html.indexOf(decl);
  if(i < 0) throw new Error('iife not found: ' + decl);
  const end = html.indexOf('\n})();', i);
  if(end < 0) throw new Error('iife end not found: ' + decl);
  return html.slice(i, end) + '\n})();';
}
function makeEl(){
  const el = {
    children: [], style: {}, dataset: {}, hidden: false, disabled: false,
    textContent: '', innerHTML: '', value: '', title: '', className: '',
    classList: { add(){}, remove(){}, toggle(){}, contains(){ return false; } },
    setAttribute(){}, getAttribute(){ return null; }, removeAttribute(){},
    appendChild(c){ el.children.push(c); return c; },
    addEventListener(){}, removeEventListener(){},
    querySelector(){ return makeEl(); }, querySelectorAll(){ return []; },
    closest(){ return null; }, focus(){}, click(){}, remove(){},
  };
  return el;
}

/* ================================================================
   段一：item 1（雙軌解釋真路徑）＋ item 7（事態預告）
   真 StoryOC＋真 BehaviorGate＋真 StoryPlay；modal 捕捉真渲染輸出。
   ================================================================ */
(function(){
  var window = {};
  var location = { search: '?softBehaviorGate=1' };
  var localStorage = { getItem: ()=>null, setItem: ()=>{}, removeItem: ()=>{} };
  var __els = {};
  var document = {
    getElementById(id){ return __els[id] || (__els[id] = makeEl()); },
    querySelector(){ return makeEl(); }, querySelectorAll(){ return []; },
    createElement(){ return makeEl(); }, body: makeEl(), addEventListener(){},
  };
  var __modals = [];
  var modal = function(body, btns, opts){ __modals.push({ body: String(body || ''), btns: btns || [], opts: opts || {} }); };
  var toast = function(){};
  var saveQ = function(){};
  var paintBar = function(){}; var drawMap = function(){};
  var syncNotebookMirror = function(){};
  var STORY_WIRE = { main: null };
  var atLoc = 'agency_ho';
  var S = null;
  var apply = function(delta){ Object.keys(delta || {}).forEach(k => { S[k] = (Number(S[k]) || 0) + delta[k]; }); return []; };
  var applyCastingTags = function(labels){
    if(!Array.isArray(S.castingTags)) S.castingTags = [];
    (labels || []).forEach(lb => { const s = String(lb || ''); if(s && !S.castingTags.some(t => t && t.id === s)) S.castingTags.push({ id: s, label: s }); });
    return [];
  };

  const SRC = [
    "var START = { y:1988, m:3, d:7 };",
    extractFn('function dateObj'),
    extractFn('function calendarSeason'),
    extractFn('function weekNumNow'),
    extractFn('function dualTrackNumbers'),
    extractFn('function readDualTracks'),
    extractFn('function syncDualTracks'),
    extractFn('function yearSeasonNow'),
    extractFn('function storyHintPack'),
    extractFn('function storyNodeLocId'),
    extractFn('function storyWeekStamp'),
    extractFn('function storyLockMeta'),
    extractFn('function storyFaceLine'),
    extractFn('function dualResultHtml'),
    extractFn('function dualDeltaBit'),
    extractFn('function dualTrackExplainHtml34'),
    extractFn('function storyMainProgressLine'),
    extractConst('STORY_GATE_3Y'),
    extractConst('STORY_LOC_SOFT'),
    extractConst('STORY_HINT_SOFT'),
    extractConst('STORY_TITLE_SOFT'),
    extractConst('LOCS'),
    extractIIFE('const BehaviorGate = (function(){'),
    extractIIFE('const StoryOC = (()=>{'),
    extractIIFE('const StoryPlay = (()=>{'),
  ].join('\n')
   .replace('const STORY_GATE_3Y =', 'var STORY_GATE_3Y =')
   .replace('const STORY_LOC_SOFT =', 'var STORY_LOC_SOFT =')
   .replace('const STORY_HINT_SOFT =', 'var STORY_HINT_SOFT =')
   .replace('const STORY_TITLE_SOFT =', 'var STORY_TITLE_SOFT =')
   .replace('const LOCS =', 'var LOCS =')
   .replace('const BehaviorGate =', 'var BehaviorGate =')
   .replace('const StoryOC =', 'var StoryOC =')
   .replace('const StoryPlay =', 'var StoryPlay =');
  eval(SRC);

  ok('seg1 harness: StoryPlay/StoryOC 載入', typeof StoryPlay === 'object' && typeof StoryPlay.start === 'function' && typeof StoryOC.listOpen === 'function');

  function freshSave(over){
    return Object.assign({
      dayIndex: 0, fame: 5, popularity: 3, acting: 18, stage: 14, vocal: 14, looks: 22, iq: 20, charm: 16,
      stress: 12, money: 12000, stamina: 75, industryCreditDelta: 0,
      flags: {}, npcs: { colleague: 8, director: 4, stylist: 5, rival: 6, reporter: 3, agent: 12 },
      mockRumors: [], mockDebts: [], castingTags: [], inventory: {},
      story: { done: {}, flags: {}, rel: {}, routes: {}, phase: 'P1', gigCount: 0 },
    }, over || {});
  }
  function loadGame(save){
    S = save; window.S = S;
    STORY_WIRE.main = JSON.parse(JSON.stringify(storyPack));
    /* 照真 boot 路徑載入軟閘 stub（repo loader 喺 refreshCopyPacksFromDisk 做呢步） */
    BehaviorGate.loadStub_nodes_trigger(JSON.parse(JSON.stringify(gateStubPack)));
    StoryOC.ensure();
    return S;
  }
  function lastResultBody(){
    for(let i = __modals.length - 1; i >= 0; i--){
      if(__modals[i].body.indexOf('sp-result') >= 0) return __modals[i].body;
    }
    return '';
  }

  /* ---- item 1：C1 真播到結算，解釋要出現；C2 結算唔再出 ---- */
  loadGame(freshSave());
  const open0 = StoryOC.listOpen({ player: true }).open.map(r => r.id);
  ok('seg1 C1 喺真 offer 列表', open0.includes('C1'));
  __modals = [];
  const started = StoryPlay.start('C1');
  ok('seg1 StoryPlay.start(C1) 成功', started === true);
  StoryPlay.skipToChoices();
  StoryPlay.pickChoice('C1_a');
  const body1 = lastResultBody();
  ok('seg1 C1 結算畫面（真 showResult）有雙軌白話解釋', body1.indexOf('何生提你') >= 0 && body1.indexOf('聲望＝觀眾識唔識你') >= 0);
  ok('seg1 解釋旗已燒（只出一次）', S.flags.guidanceDualExplained34 === true);
  ok('seg1 C1 已完成', StoryOC.isDone('C1') === true);

  /* C2：去到第 4 週＋隔日＋聽過守則傳聞＋通告數（行軟閘真 trigger） */
  S.dayIndex = 24; /* 第 4 週 */
  S.flags.tvb_rules_gossip = true;
  S.mockRumors.push({ id: 'tvb_rules_gossip', source: '何生事務所', title: '電視城廠景生存守則', text: 'x', state: 'normal' });
  S.story.gigCount = 5;
  atLoc = 'tvb_longmen';
  __modals = [];
  const started2 = StoryPlay.start('C2');
  ok('seg1 StoryPlay.start(C2) 成功（第 4 週＋傳聞＋隔日）', started2 === true);
  if(started2){
    StoryPlay.skipToChoices();
    StoryPlay.pickChoice('C2_a');
    const body2 = lastResultBody();
    ok('seg1 C2 結算畫面唔再重出解釋（只出一次）', body2.indexOf('sp-result') >= 0 && body2.indexOf('何生提你') < 0);
  }

  /* ---- item 7(a)：C2 未解鎖嗰陣，picker「即將可出」行要寫明條件＋地點 ---- */
  loadGame(freshSave({ dayIndex: 8, story: { done: { C1: true }, flags: {}, rel: {}, routes: {}, phase: 'P1', gigCount: 1 } }));
  S.flags = { rumorTutorialDone: true };
  __modals = [];
  StoryPlay.playOpenPicker();
  const pickerHtml = __modals.map(m => m.body).join('\n');
  ok('seg7 picker 有即將可出區', pickerHtml.indexOf('即將可出') >= 0);
  const c2RowAt = pickerHtml.indexOf('留人脈／趕通告');
  ok('seg7 picker 列出 C2', c2RowAt >= 0);
  const c2Row = c2RowAt >= 0 ? pickerHtml.slice(c2RowAt, c2RowAt + 700) : '';
  ok('seg7 C2 行寫明第 4 週條件（軟閘真文案／週次戳）', c2Row.indexOf('未到第 4 週') >= 0 || /約第4/.test(c2Row));
  /* v20a71 PROGRESS71 改版：舊斷言驗「開咗去星河電視台播」拼裝碎片——用戶評文法怪，
     v71 改完整子句「（開咗之後，去X就會觸發）」，斷言跟新正確行為改。 */
  ok('seg7 C2 行寫明去星河電視台觸發（v71 完整子句）', c2Row.indexOf('星河電視台') >= 0 && c2Row.indexOf('開咗之後') >= 0 && c2Row.indexOf('開咗去') < 0);

  /* ---- item 7(c)：主線進度行——C6（三年版閘、非軟閘覆蓋）補地點 ---- */
  loadGame(freshSave({
    dayIndex: 66,
    /* v20a87 WF5 修正：routes 真 key 係 route_tv（routeHeld 以全名查 st.routes）。
       舊 fixture 寫 { tv: true } 等於冇持有路線——本場景 dayIndex 66（第 10 週）本身未到
       weekMin 15，route 有冇都出同一句「未開」，所以寫錯 key 一直冇被發現（測試盲點）。
       C6 閘嘅正反驗證改由 test_wf5_87_logic.js 補齊（route＋週數齊備先開、欠 route 唔開）。 */
    story: { done: { C1: true, C2: true, C3: true, C4: true, C5: true }, flags: {}, rel: {}, routes: { route_tv: true }, phase: 'P2', gigCount: 9 },
  }));
  S.flags = {};
  const prog = storyMainProgressLine();
  /* v20a71 PROGRESS71 改版：舊斷言驗「第N幕即將」碎片頭＋「開咗去…播」拼裝尾——
     用戶評文法怪，v71 全面改完整句子，斷言跟新正確行為改（句子內容由 v71 專測覆蓋）。 */
  ok('seg7 主線進度行指向下一幕（v71 完整句）', prog.indexOf('第 6 幕〈飯堂閒角〉') >= 0 && prog.indexOf('未開') >= 0 && prog.indexOf('即將') < 0);
  ok('seg7 主線進度行講明去星河電視台觸發（v71）', prog.indexOf('星河電視台') >= 0 && prog.indexOf('就會觸發。') >= 0 && prog.indexOf('開咗去') < 0);
})();

/* ================================================================
   段二：item 2——真 buildPostShootRewardPack 組裝＋真 newspaperWrapFaceLines
   (a) 頭條變體池 (b) metrics 單抽唔再鎖死 (c) 反響唔寫錯劇名
   ================================================================ */
(function(){
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
  const FNS = ['psrPickNoRepeat35','augmentPostShootRewards35','postShootPickTemplate',
    'postShootCopyLine','postShootDisplayTitle','postShootMetricKindForType','buildPostShootRewardPack',
    /* v20a38：跨次記憶＋場景適配新函數，一併抽真 */
    'psrRecent38','psrSceneForShoot38','psrSceneFilter38'];
  for(let i = 0; i < FNS.length; i++) eval(extractFn('function ' + FNS[i]));
  eval(extractConst('PSR_SCENE_TAGS38').replace('const PSR_SCENE_TAGS38', 'var PSR_SCENE_TAGS38'));
  eval(extractConst('PAPER_NAME_TIER_NAMED').replace('const PAPER_NAME_TIER_NAMED', 'var PAPER_NAME_TIER_NAMED'));
  eval(extractConst('PAPER_NAME_TIER_TITLED').replace('const PAPER_NAME_TIER_TITLED', 'var PAPER_NAME_TIER_TITLED'));
  const NFNS = ['newspaperNameTier','newspaperPlayerRef','newspaperMediumFromGigType','newspaperWrapFaceLines'];
  for(let i = 0; i < NFNS.length; i++) eval(extractFn('function ' + NFNS[i]));

  augmentPostShootRewards35();

  /* (b) 連組 30 份電視劇殺青：metrics（收視關注）欄唔准鎖死同一張 */
  const metricIds = [], metricTitles = [];
  for(let i = 0; i < 30; i++){
    const pack = buildPostShootRewardPack({ gigId: 'v37_' + i, type: '電視劇', workTitle: '試作劇' + i, title: '《試作劇' + i + '》街坊' });
    const mc = (pack.cards || []).find(c => c.channel === 'metrics');
    metricIds.push(mc && mc.meta && mc.meta.templateId);
    metricTitles.push(mc && mc.title);
  }
  ok('seg2 metrics 卡齊備', metricIds.every(x => !!x));
  ok('seg2 收視關注唔再鎖死同一張（≥2 款輪替）', new Set(metricIds).size >= 2);
  let consecSame = false;
  for(let i = 1; i < metricIds.length; i++) if(metricIds[i] === metricIds[i - 1]) consecSame = true;
  ok('seg2 收視關注冇連續兩份相同', !consecSame);
  ok('seg2 收視關注標題有變化', new Set(metricTitles).size >= 2);

  /* (c) 《天星碼頭》殺青反響唔准寫錯第二套劇名。
     v20a38 更新：改好嗰張「深宵廠景煞科」加咗場景標籤（night+studio）——
     《天星碼頭》係碼頭日間外景，呢張由「要入輪替」改為「永不出現先啱」；
     張卡本身唔係封殺：夜晚廠景工仍然要抽得中（細節驗證喺 test_wrap38）。 */
  let sawSceneCard = false, sawWrongWork = false;
  for(let i = 0; i < 60; i++){
    const pack = buildPostShootRewardPack({ gigId: 'ferry_' + i, type: '電視劇', workTitle: '天星碼頭', title: '《天星碼頭》水手' });
    (pack.cards || []).forEach(c => {
      const blob = String(c.title || '') + ' ' + String(c.body || '');
      if(blob.indexOf('夜班廠景') >= 0) sawWrongWork = true;
      if(blob.indexOf('深宵廠景煞科') >= 0) sawSceneCard = true;
    });
  }
  ok('seg2 《天星碼頭》反響冇寫錯劇名（冇「夜班廠景」）', !sawWrongWork);
  ok('seg2 v20a38：碼頭外景唔再抽中「深宵廠景煞科」（場景適配）', !sawSceneCard);
  let sawNightStudio = false;
  for(let i = 0; i < 60 && !sawNightStudio; i++){
    const pack = buildPostShootRewardPack({ gigId: 'ns_' + i, type: '電視劇', workTitle: '深宵疑雲', title: '《深宵疑雲》廠景群演' });
    (pack.cards || []).forEach(c => {
      if((String(c.title || '') + ' ' + String(c.body || '')).indexOf('深宵廠景煞科') >= 0) sawNightStudio = true;
    });
  }
  ok('seg2 v20a38：夜晚廠景工仍然抽得中「深宵廠景煞科」（唔係一刀切封殺）', sawNightStudio);

  /* (a) 報紙頭條：同作品定版、跨作品有變化、每款都帶作品＋角色 */
  const works = [
    { work: '天星碼頭', role: '水手' }, { work: '霓虹夜影', role: '舞女' }, { work: '大廈保安', role: '看更' },
    { work: '茶餐廳風雲', role: '伙記' }, { work: '武館春秋', role: '弟子' }, { work: '碼頭歲月', role: '苦力' },
    { work: '夜校疑雲', role: '校工' }, { work: '摩登保鑣', role: '司機' }, { work: '巴士奇緣', role: '乘客' },
    { work: '海角情緣', role: '漁民' }, { work: '戲班春秋', role: '小生' }, { work: '靈異屋邨夜話', role: '鄰居' },
  ];
  const heads = works.map(w => newspaperWrapFaceLines({ gigId: 'h', work: w.work, role: w.role, type: '電視劇' }, 'steady').headline);
  ok('seg2 頭條跨作品有變化（≥3 款句式）', new Set(heads).size >= 3);
  /* 句式骨架：抽走作品／角色／稱呼之後剩低嘅句式——舊碼單一句式嗰陣全部一樣 */
  const skeletons = works.map((w, i) => heads[i].split(w.work).join('').split(w.role).join('').split('阿偉').join('').split('臨記').join(''));
  ok('seg2 頭條句式骨架 ≥3 款（唔係靠作品名扮變化）', new Set(skeletons).size >= 3);
  ok('seg2 每條頭條都帶返自己作品＋角色', works.every((w, i) => heads[i].indexOf('《' + w.work + '》') >= 0 && heads[i].indexOf(w.role) >= 0));
  const again = newspaperWrapFaceLines({ gigId: 'h', work: '天星碼頭', role: '水手', type: '電視劇' }, 'steady').headline;
  ok('seg2 同一作品頭條定版（重組結果相同）', again === heads[0]);
  const noRole = newspaperWrapFaceLines({ gigId: 'h', work: '天星碼頭', role: '', type: '電視劇' }, 'steady').headline;
  ok('seg2 無角色頭條都成立', noRole.indexOf('《天星碼頭》') >= 0 && noRole.length > 6);
})();

/* ================================================================
   段三：真 doAudition → 真 scheduleShoot → 真 resolvePlannedDay 逐日
   item 3（聲望兌現時機）／item 5（場數文案）／item 6（訓練＋長工抉擇節奏）
   ================================================================ */
(function(){
  var window = {};
  var location = { search: '' };
  var localStorage = { getItem: ()=>null, setItem: ()=>{}, removeItem: ()=>{} };
  var __els = {};
  var document = {
    getElementById(id){ return __els[id] || (__els[id] = makeEl()); },
    querySelector(){ return makeEl(); }, querySelectorAll(){ return []; },
    createElement(){ return makeEl(); }, body: makeEl(), addEventListener(){},
  };
  var __modals = [];
  /* modal stub 扮玩家：記錄畫面後撳主掣（role 'p'）——confirmPlaceShoot 嗰種確認框
     唔撳就唔會行到 finishHire，同真玩家流程一致 */
  var modal = function(body, btns, opts){
    __modals.push({ body: String(body || ''), btns: btns || [], opts: opts || {} });
    const p = (btns || []).find(b => b && b.role === 'p' && typeof b.on === 'function');
    if(p){ try{ p.on(); }catch(_e){} }
  };
  var toast = function(){}; var saveQ = function(){};
  var paintBar = function(){}; var drawMap = function(){}; var closeSheet = function(){};
  var enterHome = function(){}; var runScheduleFromToday = function(){}; var goToMapForBrowse = function(){};
  var maybeShowTutToast = function(k, t, cb){ if(typeof cb === 'function') cb(); };
  var softPreviewOn = function(){ return false; };
  var phase3CastCopy = function(){ return { successToast: '', failToast: '', lockedTag: '', readyTag: '' }; };
  var dayEndContinueButtons = function(){ return [{ label: '返回地圖', role: 'g', on: function(){} }]; };
  var livingCostDayEndHint = function(){ return ''; };
  var presentAudFailSettlement = function(){ return false; };
  var presentRestSleepDayEnd = function(){};
  var flushWeekAccelSummary = function(){};
  var FREEPLAY_FW = { _pendingPostShootReward: null, postShootRewards: null };
  var _weekAccel = false;
  var planSelDay = 0; var planCat = 'browse'; var planDraft = null; var planBackup = null;
  var EVENTS = null;
  var GIGS = [];
  var S = null;
  var tickDay = function(){ S.dayIndex += 1; return { ended: false, summary: null }; };

  eval("var START = { y:1988, m:3, d:7 };");
  const CONSTS = ['STAT_LABEL','STAT_MAX','STRESS_MAX','EVENTS_ZH_HK','SHOOT_DAY_BY_TYPE','TRAIN_EVENTS_35','SET_CHOICES_35','MOCK_RUMOR_SEEDS','COURSE_DEFS','PLAN_ITEMS'];
  for(const c of CONSTS) eval(extractConst(c).replace('const ' + c + ' =', 'var ' + c + ' ='));
  const FNS = ['R','clamp','statHardMax','apply','bumpNpc','planMeta','isGigWrapped','isGigInProduction','planCatForId','shootDeadlineHud','shootRemain','reqGap','gigActiveShoot','weekdayIdx','weekdayName','dateObj','fmtDate',
    'fillTpl','pick','eventLine','shootDayLine','formatResultNotes','shootDailyDelta','maybeUnlockMidCourses',
    'maybeTrainEvent35','setChoiceOffer35','applySetChoice35','resolvePlannedDay',
    'shootSpanFor','effectiveShootDays','effectiveShootWeekdays','effectiveShootDeadlineDays','newShootId','scheduleShoot',
    'defaultWeekPlan','lockShootsIntoDraft','placeShootOnPlan','previewShootPlacement','confirmPlaceShoot',
    'weekNumNow','stampWeekPlan37','writeTodayPlan','clearJobFromPlans',
    'shootBandFor','resolveRoleScale','shootWeekdayOk','shootWeekdaySet0','isFreePlanSlot','isMapDay','isRecordGig','shootWeekdayLabel','gigScheduleVerb','displayDateObj','isCriticalPlanDay','planDayWouldWrap','enrollCourse','fameFloor','canAudition','chance','rollAuditionPay','chanceVarianceNote','payContractNote','doAudition'];
  for(const f of FNS) eval(extractFn('function ' + f + '('));

  ok('seg3 harness: resolvePlannedDay/doAudition 載入', typeof resolvePlannedDay === 'function' && typeof doAudition === 'function');

  function baseSave(over){
    return Object.assign({
      dayIndex: 30, fame: 17, popularity: 10, acting: 50, stage: 30, vocal: 20, looks: 30, iq: 30, charm: 20,
      stress: 12, money: 5000, stamina: 80, industryCreditDelta: 0,
      flags: {}, npcs: { colleague: 8, director: 4, stylist: 5, rival: 6, reporter: 3, agent: 12 },
      board: {}, booked: [], shoots: [], weekPlan: ['rest','rest','rest','rest','rest','rest','rest'],
      weekGigsDone: 0, weekTrainDone: 0, trainCount: {}, mockRumors: [], story: { gigCount: 0, flags: {}, done: {} },
    }, over || {});
  }
  const gigTv3 = {
    id: 'v37_gig_tv3', title: '《試作劇》鄰居', workTitle: '試作劇', roleLabel: '鄰居', type: '電視劇', loc: 'tvb_longmen',
    req: {}, pay: [900, 900], payExact: 900, fame: [5, 5], popularity: [17, 17], hard: 0.1, tier: '初',
    shootDaysHint: 3, shootBand: [3, 3], shootWeekdays: [1, 2, 3, 4, 5, 6], shootDeadlineDays: 12,
    limits: { gender: 'any', licenses: [], groupOnly: false, notes: [] },
  };

  /* ---- item 3：獲聘對話數字 vs 頂欄實際入帳 ---- */
  S = baseSave(); GIGS = [gigTv3]; S.board = { tvb_longmen: [gigTv3.id] };
  const realRandom = Math.random;
  Math.random = () => 0.05; /* 釘死試鏡 roll（必獲聘）；fame/pop 區間係單值，唔受影響 */
  __modals = [];
  doAudition(gigTv3, { id: 'tvb_longmen', name: '星河電視台' });
  Math.random = realRandom;
  const hireBody = __modals.map(m => m.body).join('\n');
  ok('seg3 獲聘對話有講明「殺青後入帳」', hireBody.indexOf('殺青後入帳') >= 0);
  ok('seg3 獲聘對話聲望 +5／人氣 +17（同 shoot record 同源）', hireBody.indexOf('聲望 +5') >= 0 && hireBody.indexOf('人氣 +17') >= 0);
  ok('seg3 獲聘嗰刻聲望未入帳（S.fame 仍 17）', S.fame === 17 && S.popularity === 10);
  const shoot = (S.shoots || [])[0];
  ok('seg3 shoot record 存住 fame 5／pop 17 待殺青', !!shoot && shoot.fame === 5 && shoot.popularity === 17);
  if(shoot){
    S.weekPlan = ['shoot:' + shoot.id, 'shoot:' + shoot.id, 'shoot:' + shoot.id, 'rest', 'rest', 'rest', 'rest'];
    resolvePlannedDay('shoot:' + shoot.id);
    ok('seg3 拍攝第 1 日後聲望仍 17', S.fame === 17);
    resolvePlannedDay('shoot:' + shoot.id);
    ok('seg3 拍攝第 2 日後聲望仍 17', S.fame === 17);
    resolvePlannedDay('shoot:' + shoot.id);
    ok('seg3 殺青日聲望入帳 17→22（＝對話 +5）', S.fame === 22);
    ok('seg3 殺青日人氣入帳 10→27（＝對話 +17）', S.popularity === 27);
    ok('seg3 殺青後 shoot 已清', (S.shoots || []).length === 0);
  }

  /* ---- item 5：場數文案——真拍攝日路徑，餘數＝total−done ---- */
  function shootDayBodies(type, totalDays, trials){
    const bodies = [];
    for(let t = 0; t < trials; t++){
      S = baseSave();
      const sh = { id: 'sh5_' + t, gigId: 'g5', title: '《場數劇》', workTitle: '場數劇', type: type, totalDays: totalDays, doneDays: 0, daysLeft: totalDays, pay: 500, fame: 2, popularity: 3, locId: 'tvb_longmen' };
      S.shoots = [sh];
      S.weekPlan = ['shoot:' + sh.id, 'rest', 'rest', 'rest', 'rest', 'rest', 'rest'];
      __modals = [];
      resolvePlannedDay('shoot:' + sh.id);
      bodies.push(__modals.map(m => m.body).join('\n'));
    }
    return bodies;
  }
  const tvBodies = shootDayBodies('電視劇', 3, 40);
  ok('seg5 電視劇第 1 日（1/3）冇「餘3場」', !tvBodies.some(b => b.indexOf('餘3場') >= 0));
  ok('seg5 電視劇第 1 日有出「餘2場」（抽中嗰款模板）', tvBodies.some(b => b.indexOf('餘2場') >= 0));
  const oneBodies = shootDayBodies('電視劇', 1, 40);
  ok('seg5 單日劇（1/1）冇「餘1場」', !oneBodies.some(b => b.indexOf('餘1場') >= 0));
  ok('seg5 單日劇有出「餘0場」', oneBodies.some(b => b.indexOf('餘0場') >= 0));
  /* pack 蓋過內嵌池嗰種情況：pack 模板仲係舊「餘{total}」寫法，填充層要正規化 */
  EVENTS = { SHOOT_DAY: ['劇集外景：{title}第{done}場過關，餘{total}場。'] };
  const packBodies = shootDayBodies('紀錄片', 3, 3);
  ok('seg5 pack 舊模板經正規化出「餘2場」', packBodies.every(b => b.indexOf('餘2場') >= 0) && !packBodies.some(b => b.indexOf('餘3場') >= 0));
  EVENTS = null;

  /* ---- item 6a：訓練微事件——真 resolvePlannedDay 訓練日 ×20、多輪統計 ---- */
  let totalEv = 0, totalDays = 0, anyConsec = false;
  for(let run = 0; run < 10; run++){
    S = baseSave({ dayIndex: 100 + run * 40, flags: {} });
    let prevHit = false;
    for(let d = 0; d < 20; d++){
      __modals = [];
      resolvePlannedDay('train_acting');
      const hit = __modals.some(m => m.body.indexOf('課堂小插曲') >= 0);
      if(hit && prevHit) anyConsec = true;
      prevHit = hit;
      if(hit) totalEv++;
      totalDays++;
    }
  }
  const freq = totalEv / totalDays;
  ok('seg6a 訓練微事件長期頻率 25–55%（實測 ' + Math.round(freq * 100) + '%）', freq >= 0.25 && freq <= 0.55);
  ok('seg6a 冇任何連續兩堂都出（冷卻生效）', !anyConsec);

  /* ---- item 6b：長工抉擇——真 9 日拍攝路徑統計 ---- */
  let offerCounts = [];
  for(let run = 0; run < 8; run++){
    S = baseSave({ dayIndex: 200 + run * 30, flags: {} });
    const sh = { id: 'sh9_' + run, gigId: 'g9', title: '《長工劇》', workTitle: '長工劇', type: '電影', totalDays: 9, doneDays: 0, daysLeft: 9, pay: 3000, fame: 6, popularity: 8, locId: 'film_lion' };
    S.shoots = [sh];
    S.weekPlan = Array(7).fill('shoot:' + sh.id);
    let offers = 0;
    for(let d = 0; d < 8; d++){ /* 第 9 日係殺青日，唔出抉擇 */
      __modals = [];
      resolvePlannedDay('shoot:' + sh.id);
      if(__modals.some(m => m.body.indexOf('片場小事') >= 0)) offers++;
    }
    offerCounts.push(offers);
  }
  const avgOffers = offerCounts.reduce((a, b) => a + b, 0) / offerCounts.length;
  ok('seg6b 9 日工抉擇平均 2.5–5 次（實測 ' + avgOffers.toFixed(1) + '）', avgOffers >= 2.5 && avgOffers <= 5);
  ok('seg6b 每輪至少 2 次', offerCounts.every(n => n >= 2));
})();

/* ================================================================
   段四：item 4——真 renderNotebook 標頭跟 plan 週次
   ================================================================ */
(function(){
  var __els = {};
  var document = {
    getElementById(id){ return __els[id] || (__els[id] = makeEl()); },
    querySelector(){ return makeEl(); }, querySelectorAll(){ return []; },
    createElement(){ return makeEl(); }, body: makeEl(), addEventListener(){},
  };
  var toast = function(){}; var saveQ = function(){};
  var goEnrollableCompany = function(){}; var openCopyFromDay = function(){}; var toggleCopyPanel = function(){};
  var renderCopyChips = function(){}; var syncHomeTabExit = function(){}; var updateLiveStressStrip = function(){};
  var todayHasSoftSchedule = function(){ return false; }; var todayIsForcedDay = function(){ return false; };
  var enrolledTrainItems = function(){ return []; }; var workItems = function(){ return []; };
  var planSelDay = 0; var planCat = 'browse'; var planDraft = null; var planBackup = null;
  var S = null;
  eval("var START = { y:1988, m:3, d:7 };");
  eval(extractConst('COURSE_DEFS').replace('const COURSE_DEFS =', 'var COURSE_DEFS ='));
  eval(extractConst('PLAN_ITEMS').replace('const PLAN_ITEMS =', 'var PLAN_ITEMS ='));
  eval(extractConst('PLAN_CATS').replace('const PLAN_CATS =', 'var PLAN_CATS ='));
  const FNS = ['weekdayIdx','weekdayName','weekNumNow','weekRangeLabelFor','weekRangeLabel','stampWeekPlan37','nbShowingPrevWeek37','nbRangeLabel37',
    'planCatForId','planMeta','isGigWrapped','isGigInProduction','gigActiveShoot','shootDeadlineHud','shootRemain','reqGap','dayPlanLocked','defaultWeekPlan','renderNotebook'];
  for(const f of FNS) eval(extractFn('function ' + f + '('));

  function nbSave(stamp){
    planDraft = null;
    return {
      dayIndex: 14, /* 第 3 週一 */ fame: 5, stress: 10, money: 1000,
      flags: {}, npcs: {}, story: { gigCount: 0 }, shoots: [], booked: [],
      weekPlan: ['train_acting','train_acting','train_acting','train_acting','train_acting','train_acting','rest'],
      weekPlanWeek37: stamp, homeEditable: false,
    };
  }
  S = nbSave(2);
  renderNotebook();
  ok('seg4 上週 plan（戳=2）標頭顯示上週範圍', __els['nb-range'].textContent === weekRangeLabelFor(7));
  ok('seg4 上週 plan 標題講明「上週行程（唯讀）」', __els['nb-plan-title'].textContent.indexOf('上週行程') >= 0);
  S = nbSave(3);
  renderNotebook();
  ok('seg4 本週 plan（戳=3）標頭顯示本週範圍', __els['nb-range'].textContent === weekRangeLabelFor(14));
  ok('seg4 本週 plan 標題係「本週行程（唯讀）」', __els['nb-plan-title'].textContent.indexOf('本週行程') >= 0);
  const legacy = nbSave(undefined); delete legacy.weekPlanWeek37;
  S = legacy;
  renderNotebook();
  ok('seg4 舊檔冇戳：當本週（零回歸）', __els['nb-range'].textContent === weekRangeLabelFor(14));
  S = nbSave(2); stampWeekPlan37();
  ok('seg4 stampWeekPlan37 寫入當前週數', S.weekPlanWeek37 === 3);
})();

/* ================================================================
   段五：item 8——差額顯示界限（板面 vs 詳情）
   ================================================================ */
(function(){
  var S = { fame: 5, acting: 18, stage: 14, vocal: 14, looks: 22, iq: 20, charm: 16, stamina: 75 };
  eval(extractConst('STAT_LABEL').replace('const STAT_LABEL', 'var STAT_LABEL'));
  eval(extractConst('GIG_GAP_FAR37').replace('const GIG_GAP_FAR37', 'var GIG_GAP_FAR37'));
  const FNS = ['fameFloor','gigGapBits34','gigGapTotal34','gigGapLine34','gigGapFar37','gigGapBoardLine37'];
  for(const f of FNS) eval(extractFn('function ' + f + '('));

  const farGig = { id: 'far1', req: { vocal: 650 } };        /* 開局歌藝 14 → 欠 636（試玩實見數字） */
  const nearGig = { id: 'near1', req: { acting: 45 } };      /* 演技 18 → 欠 27（《靈異》級數） */
  const edgeGig = { id: 'edge1', req: { acting: 98 } };      /* 總差額剛好 80 → 照出真數 */
  const overGig = { id: 'over1', req: { acting: 99 } };      /* 總差額 81 → 長遠目標 */
  ok('seg8 遠卡板面行係「長遠目標・暫未及」唔出數字', gigGapBoardLine37(farGig).indexOf('長遠目標') >= 0 && !/\d/.test(gigGapBoardLine37(farGig)));
  ok('seg8 詳情計法保留真數（欠：歌藝 636）', gigGapLine34(farGig).indexOf('636') >= 0);
  ok('seg8 近卡板面照出真差額（欠：演技 27）', gigGapBoardLine37(nearGig).indexOf('演技 27') >= 0);
  ok('seg8 界限=80 照出真數／81 轉長遠目標', gigGapBoardLine37(edgeGig).indexOf('演技 80') >= 0 && gigGapBoardLine37(overGig).indexOf('長遠目標') >= 0);
  ok('seg8 gigGapFar37 判定一致', gigGapFar37(farGig) === true && gigGapFar37(nearGig) === false);
})();

/* ================================================================
   段六：item 9——真 applyMockAsk：傳聞來源跟實際聽到嘅地點
   ================================================================ */
(function(){
  var window = {};
  var location = { search: '' };
  var localStorage = { getItem: ()=>null, setItem: ()=>{}, removeItem: ()=>{} };
  var toast = function(){}; var saveQ = function(){}; var syncNotebookMirror = function(){};
  var refreshMoneyHud = function(){}; var noteFamilyHomePaid = function(){};
  var softPreviewOn = function(){ return true; };
  var softSocialDailyUse = function(){}; var softSocialDailyCap = function(){ return { ok: true }; };
  var canRepayDebtById = function(){ return false; }; var ensureFavorDueSettled = function(){};
  var _storyPlayLocked = false;
  var S = null;
  eval("var START = { y:1988, m:3, d:7 };");
  const CONSTS = ['MOCK_ASK','MOCK_RUMOR_SEEDS','MERGE_FRAGS','MOCK_TOAST','SEASON_COLLECT','FAVOR_DUE_CFG'];
  for(const c of CONSTS) eval(extractConst(c).replace('const ' + c + ' =', 'var ' + c + ' ='));
  const FNS = ['R','clamp','statHardMax','apply','bumpNpc','weekNumNow','dateObj','calendarSeason','yearSeasonNow',
    'healMayDebtCopy','ensureMockJournal','rumorStateLabel','familySafeRumorText','displayRumor',
    'debtCreditorName','ensureSeasonDebtClearedBag','favorLedgerNoteSettled','ensureFavorLedger',
    'mockAskDefs','mockIntelHits','mockAskAlreadyHeard','applyMockAsk'];
  for(const f of FNS) eval(extractFn('function ' + f + '('));

  function askSave(){
    return {
      dayIndex: 2, fame: 5, popularity: 3, acting: 18, stress: 12, money: 5000, stamina: 80,
      flags: {}, npcs: { agent: 12, colleague: 8 }, mockRumors: [], mockDebts: [], mockCredits: [],
      favorLedger: null, mockAskNonce: 1, story: { gigCount: 0, flags: {}, done: {} },
    };
  }
  /* 喺何生事務所請教何生 → 來源要係何生事務所，唔係種子寫死嘅金龍茶餐廳 */
  S = askSave();
  applyMockAsk('agency_ho', 'act_ho_tvb_rules');
  const fromAgency = (S.mockRumors || []).find(r => r && r.id === 'tvb_rules_gossip');
  ok('seg9 事務所聽返嚟嘅傳聞有入帳', !!fromAgency);
  ok('seg9 來源跟實際地點（何生事務所）', !!fromAgency && fromAgency.source === '何生事務所');
  /* 喺金龍茶餐廳打聽 → 來源係金龍茶餐廳 */
  S = askSave();
  applyMockAsk('cafe_cha', 'act_cha_tvb_rules');
  const fromCafe = (S.mockRumors || []).find(r => r && r.id === 'tvb_rules_gossip');
  ok('seg9 茶餐廳聽返嚟來源係金龍茶餐廳', !!fromCafe && fromCafe.source === '金龍茶餐廳');
})();

console.log(fails.length ? ('\nVERIFY37 LOGIC: ' + fails.length + ' FAIL -> ' + fails.join(' | ')) : '\nVERIFY37 LOGIC: ALL PASS');
process.exit(fails.length ? 1 : 0);
