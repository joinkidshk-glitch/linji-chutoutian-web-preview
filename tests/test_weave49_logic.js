// Weave Phase 4-9 邏輯測試（v20a32）：預兆系統——軌跡分類＋報紙稱呼／何生介紹語／殺青評語三渠道
// 行真路徑：真 dualTrackNumbers/readDualTracks 計信用、真 trajectoryOf49 分類、
// 真 newspaperWrapFaceLines 出標題／dek／rumor、真 enqueueNewspaperFromWrap 入佇列、
// 真 npcTierPool/pickNpcLine 傾談池。預兆只改用字：數值／fameDelta／狀態零變化一併驗。
// 用法：node tests/test_weave49_logic.js
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');

let pass = 0, fail = 0;
function ok(name, cond){
  if(cond){ pass++; console.log('  ok - ' + name); }
  else { fail++; console.log('  FAIL - ' + name); }
}
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) throw new Error('fn not found: '+name);
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){
    if(html[j]==='{') depth++;
    else if(html[j]==='}'){ depth--; if(depth===0) break; }
  }
  return html.slice(i, j+1);
}
function extractConst(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) throw new Error('const not found: '+name);
  let depth = 0, started = false;
  for(let k=i; k<html.length; k++){
    const ch = html[k];
    if(ch==='{'||ch==='['){ depth++; started = true; }
    else if(ch==='}'||ch===']'){ depth--; if(started && depth===0) return html.slice(i, k+1)+';'; }
    else if(ch===';' && !started) return html.slice(i, k+1);
  }
  throw new Error('const end not found: '+name);
}
function evalConst(name){
  eval(extractConst(name).replace('const '+name, 'globalThis.'+name));
  return globalThis[name];
}

/* ---- 共用：真雙軌＋真軌跡分類 ---- */
eval(extractFn('dualTrackNumbers'));
eval(extractFn('readDualTracks'));
['TRAJ49_IDOL_GAP','TRAJ49_IDOL_FAME','TRAJ49_CREDIT_GAP','TRAJ49_TAG_LEAD','TRAJ49_SUPER_FAME',
 'TRAJ49_SUPER_CREDIT','TRAJ49_CRAFT_FAME','TRAJ49_CRAFT_CREDIT','TRAJ49_CRAFT_GAP','TRAJ49_DIRECTOR_REL'
].forEach(n=> evalConst(n));
evalConst('TRAJ49_TAG_SETS');
eval(extractFn('trajTagCounts49'));
eval(extractFn('trajectoryOf49'));
evalConst('TRAJ_PAPER_REF49');
eval(extractFn('newspaperTrajRef49'));
evalConst('HO_INTRO_LINES49');
eval(extractFn('hoIntroLine49'));
evalConst('TRAJ_WRAP_NOTES49');
eval(extractFn('wrapTrajNotePool49'));

var S = null;
function st(o){ return Object.assign({ fame:0, stage:0, acting:0, stress:0, industryCreditDelta:0, castingTags:[], npcs:{} }, o||{}); }
const TAG = {
  reliable: { id:'tag_reliable', label:'穩重' },
  endure:   { id:'tag_endure', label:'捱得' },
  street:   { id:'tag_street', label:'爛仔' }
};

/* ================================================================
   段一：軌跡分類矩陣＋純函數（唔改狀態）
   信用公式（真 dualTrackNumbers）：round(0.5×聲量＋0.3×台風＋0.2×演技)＋delta
   ================================================================ */
console.log('段一：分類矩陣');
ok('idol: fame50/stage10/acting10 (credit30, gap20)', trajectoryOf49(st({ fame:50, stage:10, acting:10 }))==='idol');
ok('craft-super beats jianghu tags: fame60 dual60 + 爛仔/識做',
  trajectoryOf49(st({ fame:60, stage:60, acting:60, castingTags:[TAG.street, { label:'識做' }] }))==='craft');
ok('craft-mid: fame45/stage50/acting50 (credit48, gap3)',
  trajectoryOf49(st({ fame:45, stage:50, acting:50 }))==='craft');
ok('support-numeric: credit45 gap15 + 穩重x1',
  trajectoryOf49(st({ fame:30, stage:60, acting:60, castingTags:[TAG.reliable] }))==='support');
ok('support-tags: 穩重+捱得 (lead2) at low numbers',
  trajectoryOf49(st({ fame:20, stage:20, acting:20, castingTags:[TAG.reliable, TAG.endure] }))==='support');
ok('backstage-tags: 幕後統籌+編劇',
  trajectoryOf49(st({ fame:20, stage:20, acting:20, castingTags:[{ label:'幕後統籌' }, { label:'編劇' }] }))==='backstage');
ok('backstage-director: director rel65, no tags',
  trajectoryOf49(st({ fame:20, stage:20, acting:20, npcs:{ director:65 } }))==='backstage');
ok('jianghu: 爛仔+識做',
  trajectoryOf49(st({ fame:20, stage:20, acting:20, castingTags:[TAG.street, { label:'識做' }] }))==='jianghu');
ok('early average -> null', trajectoryOf49(st({ fame:8, stage:8, acting:8 }))===null);
ok('balanced-but-below-craft -> null (fame45 credit33 gap12)',
  trajectoryOf49(st({ fame:45, stage:30, acting:30, industryCreditDelta:-5 }))===null);
ok('credit-high without support tag -> null (甘草要標籤)',
  trajectoryOf49(st({ fame:30, stage:60, acting:60 }))===null);
ok('single jianghu tag -> null (lead needs 2)',
  trajectoryOf49(st({ fame:20, stage:20, acting:20, castingTags:[{ label:'識做' }] }))===null);
ok('tie jianghu2 vs support2 -> jianghu (固定 tie-break)',
  trajectoryOf49(st({ fame:20, stage:20, acting:20, castingTags:[TAG.street, { label:'識做' }, TAG.reliable, TAG.endure] }))==='jianghu');

/* 標籤計數：{id,label} 物件逐標籤計一次，唔會 id+label 雙計 */
{
  const c1 = trajTagCounts49(st({ castingTags:[TAG.street] }));
  ok('one registry tag object counts once (jianghu=1)', c1.jianghu===1 && c1.support===0 && c1.backstage===0);
  const c2 = trajTagCounts49(st({ castingTags:[TAG.reliable] }));
  ok('one registry tag object counts once (support=1)', c2.support===1);
  const c3 = trajTagCounts49(st({ castingTags:['識做'] }));
  ok('bare string tag counts once (jianghu=1)', c3.jianghu===1);
}

/* 純函數：分類前後狀態逐字不變 */
{
  const probe = st({ fame:45, stage:50, acting:50, castingTags:[TAG.reliable, { label:'幕後統籌' }], npcs:{ director:70, agent:30 } });
  const before = JSON.stringify(probe);
  trajectoryOf49(probe); trajTagCounts49(probe); wrapTrajNotePool49.call(null);
  S = probe; trajectoryOf49(); hoIntroLine49();
  ok('purity: state deep-equal after classify calls', JSON.stringify(probe)===before);
  S = null;
}

/* ================================================================
   段二：報紙稱呼——真 newspaperWrapFaceLines（＋真 enqueueNewspaperFromWrap 整合）
   ================================================================ */
console.log('段二：報紙稱呼軌跡風味');
evalConst('PAPER_NAME_TIER_NAMED'); evalConst('PAPER_NAME_TIER_TITLED');
eval(extractFn('newspaperNameTier'));
eval(extractFn('newspaperPlayerRef'));
eval(extractFn('newspaperMediumFromGigType'));
eval(extractFn('newspaperWrapFaceLines'));

const SUBJ = { gigId:'g49', work:'街景臨記', role:'路人', type:'電影' };
function faceWith(state){ S = state; return newspaperWrapFaceLines(SUBJ, 'steady'); }

ok('titled idol -> 人氣偶像阿偉', faceWith(st({ fame:45, stage:10, acting:10 })).dek.includes('人氣偶像阿偉'));
ok('titled craft -> 當紅小生阿偉', faceWith(st({ fame:45, stage:50, acting:50 })).dek.includes('當紅小生阿偉'));
ok('titled support(tags) -> 金牌甘草阿偉',
  faceWith(st({ fame:45, stage:20, acting:20, castingTags:[TAG.reliable, TAG.endure] })).dek.includes('金牌甘草阿偉'));
ok('titled backstage -> 幕後能手阿偉',
  faceWith(st({ fame:45, stage:20, acting:20, castingTags:[{ label:'幕後' }, { label:'編劇' }] })).dek.includes('幕後能手阿偉'));
ok('titled jianghu -> 江湖味阿偉 (headline too)',
  faceWith(st({ fame:45, stage:20, acting:20, castingTags:[TAG.street, { label:'識做' }] })).headline.includes('江湖味阿偉'));
{
  const f = faceWith(st({ fame:45, stage:30, acting:30, industryCreditDelta:-5 }));
  ok('titled unformed -> 舊稱呼 人氣新人阿偉 (zero regression)',
    f.dek.includes('人氣新人阿偉') && f.headline.includes('人氣新人阿偉') &&
    !f.dek.includes('偶像阿偉') && !f.dek.includes('甘草') && !f.dek.includes('江湖味'));
}
ok('named support(tags) -> 穩陣綠葉阿偉',
  faceWith(st({ fame:20, stage:20, acting:20, castingTags:[TAG.reliable, TAG.endure] })).dek.includes('穩陣綠葉阿偉'));
{
  const f = faceWith(st({ fame:5, castingTags:[TAG.street, { label:'識做' }] }));
  ok('anon + jianghu tags -> still 一名臨記/有個臨記, no flavor',
    f.dek.includes('一名臨記') && f.rumor.includes('有個臨記') && !f.dek.includes('江湖') && !f.headline.includes('阿偉'));
}
/* FaceLines 唔郁狀態 */
{
  const probe = st({ fame:45, stage:10, acting:10 });
  const before = JSON.stringify(probe);
  S = probe; for(let i=0;i<10;i++) newspaperWrapFaceLines(SUBJ, 'steady');
  ok('FaceLines leaves state untouched', JSON.stringify(probe)===before);
}

/* 整合：真 enqueueNewspaperFromWrap——稱呼入到佇列 item；fameDelta／tone 同無軌跡一致 */
(function(){
  var saveQ = ()=>{};
  var FREEPLAY_FW = { newspaperStub: null };
  var GIGS = [];
  var postShootDisplayTitle = (o)=> (o && (o.workTitle || o.title)) || '';
  eval(extractFn('ensureNewspaperQueue'));
  eval(extractFn('ensureNewspaperClippings'));
  eval(extractFn('newspaperEventSeen'));
  eval(extractFn('enqueueNewspaperItem'));
  eval(extractFn('newspaperFillPlayer'));
  eval(extractFn('newspaperPickTemplate'));
  eval(extractFn('newspaperCopyFromTemplate'));
  eval(extractFn('newspaperLookupGig'));
  eval(extractFn('newspaperWrapSubject'));
  eval(extractFn('newspaperWrapAngle'));
  eval(extractFn('newspaperWrapLeadRelation'));
  eval(extractFn('newspaperWrapFadeSubject'));
  eval(extractFn('newspaperWrapFadeLines'));
  eval(extractFn('enqueueNewspaperFromWrap'));

  const sh = { gigId:'gig_49a', type:'電影', workTitle:'江邊小鎮', roleLabel:'武師', title:'《江邊小鎮》武師', fame:0 };
  S = Object.assign(st({ fame:45, stage:10, acting:10 }), { dayIndex:10, newspaperQueue:[], newspaperClippings:[], pendingMorningPaper:null });
  const idolItem = enqueueNewspaperFromWrap(sh, { dayIndex:10, cards:[] }, { persist:false });
  ok('wrap integration: idol item enqueued with 人氣偶像阿偉',
    !!idolItem && idolItem.dek.includes('人氣偶像阿偉'));
  ok('wrap integration: rumorEcho carries an idol note',
    !!idolItem && TRAJ_WRAP_NOTES49.idol.some(n=> idolItem.rumorEcho.includes(n)));

  const sh2 = { gigId:'gig_49b', type:'電影', workTitle:'江邊小鎮', roleLabel:'武師', title:'《江邊小鎮》武師', fame:0 };
  S = Object.assign(st({ fame:45, stage:30, acting:30, industryCreditDelta:-5 }), { dayIndex:10, newspaperQueue:[], newspaperClippings:[], pendingMorningPaper:null });
  const plainItem = enqueueNewspaperFromWrap(sh2, { dayIndex:10, cards:[] }, { persist:false });
  ok('wrap integration: unformed item keeps 人氣新人阿偉',
    !!plainItem && plainItem.dek.includes('人氣新人阿偉'));
  ok('wrap integration: fameDelta identical (presentation only)',
    !!idolItem && !!plainItem && idolItem.fameDelta===plainItem.fameDelta && idolItem.tone===plainItem.tone);
})();

/* ================================================================
   段三：何生介紹語——真 npcTierPool 組成＋真 pickNpcLine 抽樣
   ================================================================ */
console.log('段三：何生介紹語');
evalConst('AFF_DIALOGUE_GATES');
eval(extractFn('affUnlockedKeys'));
evalConst('NPC_AFF_TIERS');
evalConst('NPC_TIER_LINES');
eval(extractFn('npcTierPool'));
eval(extractFn('npcIntelPool'));
var NPC_LINES = null;
var NPC_LINES_CORE = { agent: { greet:['[greet]'], chat:['[chat]'], advice:['[advice]'], intel:['[intel-core]'], pressure:['[pressure]'] } };
eval(extractFn('pickNpcLine'));

const IDOL_S = st({ fame:50, stage:10, acting:10, npcs:{ agent:30 } });
const NULL_S = st({ fame:45, stage:30, acting:30, industryCreditDelta:-5, npcs:{ agent:30 } });

S = IDOL_S;
ok('tierPool agent aff30 + idol -> traj = idol intro',
  JSON.stringify(npcTierPool('agent', 30).traj)===JSON.stringify([HO_INTRO_LINES49.idol]));
ok('tierPool agent aff30 + idol -> daily still 4 lines', npcTierPool('agent', 30).daily.length===4);
S = NULL_S;
ok('tierPool agent aff30 + unformed -> traj empty', npcTierPool('agent', 30).traj.length===0);
S = IDOL_S;
ok('tierPool agent aff10 + idol -> traj empty (aff gate)', npcTierPool('agent', 10).traj.length===0);
ok('tierPool reporter aff80 + idol -> traj empty (agent only)', npcTierPool('reporter', 80).traj.length===0);
{
  S = Object.assign({}, IDOL_S, { npcs:{ agent:60 } });
  const pool = npcIntelPool('agent');
  ok('npcIntelPool excludes intro line (not intel)', !pool.includes(HO_INTRO_LINES49.idol) && pool.length>4);
}
{
  S = IDOL_S;
  const seen = new Set();
  for(let i=0;i<400;i++) seen.add(pickNpcLine('agent', {}));
  ok('pickNpcLine samples idol intro when formed', seen.has(HO_INTRO_LINES49.idol));
  S = NULL_S;
  const seen2 = new Set();
  const allIntro = Object.values(HO_INTRO_LINES49);
  for(let i=0;i<400;i++) seen2.add(pickNpcLine('agent', {}));
  ok('pickNpcLine never samples any intro when unformed', ![...seen2].some(l=> allIntro.includes(l)));
}

/* ================================================================
   段四：殺青評語——池組成＋rumor 附加＋未定型逐字一致
   ================================================================ */
console.log('段四：殺青評語軌跡詞');
const BASE_RUMOR = '聽講《街景臨記》殺青，阿偉做路人，場記話佢跟得齊。';
const BASE_RUMOR_ANON = '聽講《街景臨記》殺青，有個臨記做路人，場記話佢跟得齊。';
{
  const cases = {
    idol: st({ fame:50, stage:10, acting:10 }),
    craft: st({ fame:45, stage:50, acting:50 }),
    support: st({ fame:20, stage:20, acting:20, castingTags:[TAG.reliable, TAG.endure] }),
    backstage: st({ fame:20, stage:20, acting:20, castingTags:[{ label:'幕後' }, { label:'編劇' }] }),
    jianghu: st({ fame:20, stage:20, acting:20, castingTags:[TAG.street, { label:'識做' }] })
  };
  Object.keys(cases).forEach(k=>{
    S = cases[k];
    ok('note pool for '+k+' = its 2 lines', JSON.stringify(wrapTrajNotePool49())===JSON.stringify(TRAJ_WRAP_NOTES49[k]));
  });
  S = NULL_S;
  ok('note pool unformed = []', wrapTrajNotePool49().length===0);
}
{
  S = st({ fame:45, stage:20, acting:20, castingTags:[TAG.reliable, TAG.endure] });
  const tails = new Set();
  let allPrefixed = true, allInPool = true;
  for(let i=0;i<80;i++){
    const r = newspaperWrapFaceLines(SUBJ, 'steady').rumor;
    if(!r.startsWith(BASE_RUMOR)) allPrefixed = false;
    const tail = r.slice(BASE_RUMOR.length);
    if(!TRAJ_WRAP_NOTES49.support.includes(tail)) allInPool = false;
    tails.add(tail);
  }
  ok('support wrap: rumor = baseline + support note (always appended)', allPrefixed && allInPool);
  ok('support wrap: both notes appear over samples', tails.size===2);
}
{
  S = NULL_S;
  ok('unformed wrap: rumor byte-identical to baseline', newspaperWrapFaceLines(SUBJ, 'steady').rumor===BASE_RUMOR);
  S = st({ fame:5, castingTags:[TAG.street, { label:'識做' }] });
  ok('anon wrap: rumor byte-identical to anon baseline (no note)',
    newspaperWrapFaceLines(SUBJ, 'steady').rumor===BASE_RUMOR_ANON);
}

console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
