// v20a89 BR89 邏輯測試：分支補完 S+M
//  (A) ripple 消費者：N1–N5 文案承諾嘅 ripple 四欄（stress/health/credit/debt）＋tag 真入帳；
//      逐條對返 pack 文案數值，唔多唔少。
//  (B) 巧遇 grants 條件派發：liu_repay 推辭唔攞債權（改攞風聲卡）、mak_respect 講會驚唔攞人情；
//      應承先攞返原本嗰筆（id／debtor 逐字同 v88 定版）。
//  (C) N6F 電影線對稱幕：節點＋閘＋注入器齊；同 N6 等量級（W15、wealth 對稱）。
//  (D) 結局呈現回收：八線 ending 旗 → endingInserts410 出返該線句子；提攜債已兌現 → 點名句；
//      半線 he/be → endingRomanceScene410 分版。
//  (E) BR89 條件通告：B5——BR89_GIGS 注入池已清空，mergeBr89Gigs 本身唔再注入舊通告；
//      新庫 13 張引薦通告經通用 trigger 系統（triggerGigOn＋板面過濾）上板，
//      見 tests/test_gig229_trigger.js；br89OnGigComplete 標記兌現但 status 唔郁（結局人情計數口徑不變）。
// (F) v20a267：情報拼合／單卡使用點已刪（MERGE_PAIRS／INTEL_FLAGS／INTEL_USE_POINTS／
//      br89HoldsCard／br89CardUsePointForGig／br89CardUsePointForStar 全部刪除）。
// 反證：對 v88 index 行 → BR89 符號不存在，抽取即 FAIL。
// 用法：node tests/test_br89_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) throw new Error('fn not found: '+name);
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){ if(html[j]==='{') depth++; else if(html[j]==='}'){ depth--; if(depth===0) break; } }
  return html.slice(i, j+1);
}
function extractConst(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) throw new Error('const not found: '+name);
  let depth=0, started=false;
  for(let k=i; k<html.length; k++){
    const ch = html[k];
    if(ch==='{'||ch==='['){ depth++; started = true; }
    else if(ch==='}'||ch===']'){ depth--; if(started && depth===0) return html.slice(i, k+1)+';'; }
    else if(ch===';' && !started) return html.slice(i, k+1);
  }
  throw new Error('const end not found: '+name);
}
function extractBetween(a, b){
  const i = html.indexOf(a), j = html.indexOf(b, i);
  if(i<0 || j<0) throw new Error('segment not found: '+a);
  return html.slice(i, j);
}

/* ================= (A) ripple 消費者 ================= */
try{
  const seg = extractBetween('const rp89 =', 'if(typeof apply==="function" && Object.keys(gameDelta).length){');
  const pack = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'story_detail_n1_to_n17.json'), 'utf8'));
  const nodeOf = id => (pack.nodes||[]).find(n=>n.id===id);
  function runRipple(nodeId, choiceId){
    const node = nodeOf(nodeId);
    const choice = (node.choices||[]).find(c=>c.id===choiceId);
    const env = {
      eff: choice.effects || {}, node,
      gameDelta: {}, statsApplied: {}, notes: [],
      S: { mockDebts: [] },
      applyCastingTags: (tags)=> tags.map(t=>({ id:'tag:'+t, label:t })),
    };
    const fn = new Function('eff','node','gameDelta','statsApplied','notes','S','applyCastingTags',
      seg + '\nreturn { gameDelta, statsApplied, notes, S };');
    return fn(env.eff, env.node, env.gameDelta, env.statsApplied, env.notes, env.S, env.applyCastingTags);
  }
  // N2_a: stressDelta +1；N2_b: −1（pack 文案數值）
  let r = runRipple('N2','N2_a'); ok('A1 N2_a ripple stress +1', r.gameDelta.stress===1);
  r = runRipple('N2','N2_b'); ok('A2 N2_b ripple stress −1', r.gameDelta.stress===-1);
  // N3_a: credit −1＋stress +2；N3_b: credit +1＋stress +3
  r = runRipple('N3','N3_a'); ok('A3 N3_a credit −1／stress +2', r.statsApplied.industryCredit===-1 && r.gameDelta.stress===2);
  r = runRipple('N3','N3_b'); ok('A4 N3_b credit +1／stress +3', r.statsApplied.industryCredit===1 && r.gameDelta.stress===3);
  // N4_a: debtDelta +1 → 真債一筆（何生）；重行唔好重複入帳
  r = runRipple('N4','N4_a'); ok('A5 N4_a 入何生人情債', r.S.mockDebts.length===1 && r.S.mockDebts[0].id==='debt_c4_ho_ripple' && r.S.mockDebts[0].creditor==='何生' && r.statsApplied.industryCredit===-1);
  // N4_b: stress +8＋health −5（→體能）
  r = runRipple('N4','N4_b'); ok('A6 N4_b stress +8／體能 −5', r.gameDelta.stress===8 && r.gameDelta.stamina===-5);
  // N1_a/b: 只有 tag／描述欄 → 入沉澱標籤，唔入任何數值（唔加文案冇講嘅懲罰）
  r = runRipple('N1','N1_a'); ok('A7 N1_a 只入標籤零數值', Object.keys(r.gameDelta).length===0 && !r.statsApplied.industryCredit && r.notes.some(x=>x.indexOf('沉澱標籤')>=0));
  r = runRipple('N1','N1_b'); ok('A8 N1_b 只入標籤零數值', Object.keys(r.gameDelta).length===0 && r.notes.some(x=>x.indexOf('沉澱標籤')>=0));
  // N5_c: stressDelta −1
  r = runRipple('N5','N5_c'); ok('A9 N5_c stress −1', r.gameDelta.stress===-1);
}catch(e){ ok('A ripple 抽取/執行 ('+e.message+')', false); }

/* ================= (B) grants 條件派發 ================= */
try{
  const grants = [], cards = [];
  const sandbox = {
    S: { flags:{}, dayIndex: 100, mockRumors: [], mockCredits: [] },
    enc79GrantCredit: (c)=>{ grants.push(c); return true; },
  };
  const src = extractFn('enc79ChoiceFx') + '\n' + extractFn('enc79RunChoiceFx');
  const api = new Function('S','enc79GrantCredit',
    src + '\nreturn { enc79ChoiceFx, enc79RunChoiceFx };')(sandbox.S, sandbox.enc79GrantCredit);
  // 路由：標籤 → fx
  ok('B1 liu 應承 → liu_accept', api.enc79ChoiceFx('beat:liu_repay', '多謝受落').fx==='liu_accept');
  ok('B2 liu 推辭 → liu_decline', api.enc79ChoiceFx('beat:liu_repay', '推辭講自己排緊期').fx==='liu_decline');
  ok('B3 mak 應承 → mak_accept＋fav 4', (()=>{ const v=api.enc79ChoiceFx('beat:mak_respect','應承隨時候命'); return v.fx==='mak_accept' && v.fav===4; })());
  ok('B4 mak 講會驚 → mak_honest＋fav 2', (()=>{ const v=api.enc79ChoiceFx('beat:mak_respect','老實講自己會驚'); return v.fx==='mak_honest' && v.fav===2; })());
  // 派發結果
  api.enc79RunChoiceFx('liu_accept');
  ok('B5 liu_accept 派返原債權', grants.length===1 && grants[0].id==='credit_enc79_liu_priority' && grants[0].debtor==='廖炳星');
  grants.length = 0; cards.length = 0;
  api.enc79RunChoiceFx('liu_decline');
  ok('B6 liu_decline 乜都唔派（v267：風聲卡已刪，推辭唔再有卡）', grants.length===0 && cards.length===0);
  grants.length = 0; cards.length = 0;
  api.enc79RunChoiceFx('mak_accept');
  ok('B7 mak_accept 派返原債權', grants.length===1 && grants[0].id==='credit_enc79_mak_wuzhi');
  grants.length = 0;
  api.enc79RunChoiceFx('mak_honest');
  ok('B8 mak_honest 乜都唔派', grants.length===0 && cards.length===0);
  // beat 定義已冇無條件 grants
  ok('B9 beat 定義冇 grants 殘留', !/id:"liu_repay"[^}]*grants\(/.test(html) && !/id:"mak_respect"[^}]*grants\(/.test(html));
}catch(e){ ok('B grants 抽取/執行 ('+e.message+')', false); }

/* ================= (C) N6F 對稱幕（v20a250：內嵌表已刪，JSON 做唯一來源） ================= */
try{
  const gate = extractConst('STORY_GATE_3Y');
  const pack = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'story_detail_n1_to_n17.json'), 'utf8'));
  const env = new Function(gate + '\nreturn { STORY_GATE_3Y };')();
  ok('N1 閘 N6F＝route_film＋W15＋needDone N5（同 N6 對稱）', env.STORY_GATE_3Y.N6F && env.STORY_GATE_3Y.N6F.route==='route_film' && env.STORY_GATE_3Y.N6F.weekMin===env.STORY_GATE_3Y.N6.weekMin && JSON.stringify(env.STORY_GATE_3Y.N6F.needDone)==='["N5"]');
  const n = (pack.nodes||[]).find(x=>x.id==='N6F');
  ok('N2 節點由 JSON 出：locId film_lion＋openConditions 對位', !!n && n.locId==='film_lion' && n.openConditions.includes('route_film') && n.openConditions.includes('week_min:15'));
  const ca = n.choices.find(c=>c.id==='N6F_a'), cb = n.choices.find(c=>c.id==='N6F_b');
  ok('N3 抉擇對稱 N6（接＝wealth 1／唔接＝零）', ca.effects.stats.wealth===1 && Object.keys(cb.effects.stats).length===0 && ca.effects.flags[0]==='flag_studio_follow' && cb.effects.flags[0]==='flag_studio_roam');
  ok('N4 內嵌表＋注入器已刪（v20a250）', html.indexOf('const STORY_SPINE_NODES_BR89')<0 && html.indexOf('function applyStoryBr89Nodes89(')<0 && html.indexOf('applyStoryBr89Nodes89()')<0);
  ok('N5 進度頁有 N6F＋JSON 節點有 playerHint（soft 表 N6F 條目已刪）', html.indexOf('["N6F",20]')>=0 && !!n.playerHint && html.indexOf('N6F: { playerHint:')<0);
  ok('N6 N5 nextHint 已改兩線並陳', html.indexOf('走電影線有「片場跟班」')>=0 && html.indexOf('行電視線先有；係處境劇班底')<0);
}catch(e){ ok('C N6F 抽取/執行 ('+e.message+')', false); }

/* ================= (D) 結局呈現回收 ================= */
try{
  const src = extractConst('ENDING410_NPC_NAMES') + '\n' + extractFn('endingFlag410') + '\n' + extractFn('endingInserts410') + '\n' + extractFn('endingRomanceScene410');
  const mk = (S)=> new Function('S', src + '\nreturn { endingInserts410, endingRomanceScene410 };')(S);
  const baseS = ()=>({ npcs:{}, fame:10, story:{ flags:{}, done:{} }, flags:{}, mockCredits:[], mockDebts:[] });
  const favor = { openDebts:[], heldList:[], exodusNames:[], settled:0, creditsHeld:0 };
  let S = baseS(); S.story.flags['flag_ko_rival_respect'] = 1;
  let ins = mk(S).endingInserts410({}, favor);
  ok('D1 高俊傑 respect 旗 → 結局有佢句', ins.some(t=>t.indexOf('高俊傑')>=0 && t.indexOf('惺惺相惜')>=0));
  S = baseS(); S.flags['flag_fong_ending_save'] = 1;
  ins = mk(S).endingInserts410({}, favor);
  ok('D2 方小龍 save 旗（S.flags 庫）→ 結局有佢句', ins.some(t=>t.indexOf('方小龍')>=0 && t.indexOf('兄弟情')>=0));
  S = baseS(); S.mockCredits.push({ id:'credit_enc83_luk_patron', debtor:'陸柏言', title:'天王引薦', line:'x', status:'未收', redeemedBy:'patron-gig-redeemed' });
  ins = mk(S).endingInserts410({}, favor);
  ok('D3 提攜債已兌現 → 點名句', ins.some(t=>t.indexOf('陸柏言')>=0 && t.indexOf('兌現')>=0));
  S = baseS();
  ins = mk(S).endingInserts410({}, favor);
  ok('D4 冇旗 → 冇八線句（唔好亂出）', !ins.some(t=>t.indexOf('高俊傑與你鬥足')>=0 || t.indexOf('方小龍那次意外')>=0));
  // 半線 he/be 分版
  const rec = { career:'E0', romance:{ line:'vera', kind:'almost' } };
  S = baseS(); S.story.flags['flag_vera_be'] = 1;
  const beTxt = mk(S).endingRomanceScene410(rec);
  S = baseS();
  const deTxt = mk(S).endingRomanceScene410(rec);
  S = baseS(); S.story.flags['flag_vera_he'] = 1;
  const heTxt = mk(S).endingRomanceScene410(rec);
  ok('D5 Vera be 版 ≠ 預設版', beTxt !== deTxt && beTxt.indexOf('不再是你')>=0);
  ok('D6 Vera he 版有留白句 ≠ 預設版', heTxt !== deTxt && heTxt.indexOf('留到不必再怕')>=0);
  S = baseS(); S.flags['flag_xu_be'] = 1;
  const xuBe = mk(S).endingRomanceScene410({ career:'E0', romance:{ line:'xu', kind:'almost' } });
  ok('D7 徐寶珊 be 版（退禮物）', xuBe.indexOf('原封退回')>=0);
}catch(e){ ok('D 結局呈現抽取/執行 ('+e.message+')', false); }

/* ================= (E)+(F) BR89 模組（通告／拼合／卡使用點） ================= */
try{
  const modSrc = extractBetween('/* =====================================================================\n   v20a89 BR89：分支補完', '/* ---------- WF3-3 地點一次性對白');
  const env = {
    S: { flags:{}, mockRumors:[], mockCredits:[], dayIndex: 10 },
    GIGS: [], window: {},
    normalizeGigRecord: (g)=> g,
    MERGE_PAIRS: [], INTEL_FLAGS: {}, INTEL_USE_POINTS: {},
    syncNotebookMirror: ()=>{},
  };
  const api = new Function('S','GIGS','window','normalizeGigRecord','syncNotebookMirror',
    modSrc + '\nreturn { BR89_GIGS, mergeBr89Gigs, br89GigOn, br89OnGigComplete, BR89_PATRON_OF_GIG };'
  )(env.S, env.GIGS, env.window, env.normalizeGigRecord, env.syncNotebookMirror);
  // (F) v267：拼合系統／單卡使用點已刪
  ok('F1 MERGE_PAIRS 已刪', html.indexOf('MERGE_PAIRS')<0);
  ok('F2 INTEL_FLAGS 已刪', html.indexOf('INTEL_FLAGS')<0);
  ok('F3 INTEL_USE_POINTS 已刪', html.indexOf('INTEL_USE_POINTS')<0);
  ok('F4 br89HoldsCard 已刪', html.indexOf('br89HoldsCard')<0);
  ok('F5 br89CardUsePointForGig 已刪', html.indexOf('br89CardUsePointForGig')<0);
  ok('F6 br89CardUsePointForStar 已刪', html.indexOf('br89CardUsePointForStar')<0);
  ok('F7 intelLineForGig／intelSightLineFor 已刪', html.indexOf('intelLineForGig')<0 && html.indexOf('intelSightLineFor')<0);
  // (E) 通告注入：冇債權冇卡 → 空板
  env.GIGS.length = 0; api.mergeBr89Gigs();
  ok('E1 冇持有 → BR89 通告唔上板', env.GIGS.length===0);
  env.S.mockCredits.push({ id:'credit_enc83_luk_patron', debtor:'陸柏言', title:'天王引薦', line:'陸柏言講過會引薦你。', status:'未收' });
  api.mergeBr89Gigs();
  ok('E2 B5：mergeBr89Gigs 本身唔再注入（新庫引薦通告經 trigger 系統上板，見 test_gig229_trigger.js）', env.GIGS.length===0 && !env.GIGS.some(g=>/^gig_br89_/.test(g.id)));
  // 情報卡 → 替身通告
  env.S.mockRumors.push({ id:'rumor_ngai_stunt_tip', state:'normal' });
  api.mergeBr89Gigs();
  ok('E3 B5：mergeBr89Gigs 唔出舊情報通告（舊情報通告已刪，新庫對應見 test_gig229_trigger.js）', env.GIGS.length===0 && !env.GIGS.some(g=>/^gig_br89_/.test(g.id)));
  // 殺青標記兌現：line 追加、status 不變、再 merge 唔再出（通告 id 由留返嘅映射表反查，唔寫死舊 id 字面）
  const patId = Object.keys(api.BR89_PATRON_OF_GIG).find(k=>api.BR89_PATRON_OF_GIG[k]==='credit_enc83_luk_patron');
  api.br89OnGigComplete(patId);
  const c = env.S.mockCredits.find(x=>x.id==='credit_enc83_luk_patron');
  ok('E4 兌現標記＋line 交代＋status 唔郁', c.redeemedBy===patId && c.line.indexOf('已兌現')>=0 && c.status==='未收');
  api.mergeBr89Gigs();
  ok('E5 兌現後引薦通告落板', !env.GIGS.some(g=>g.id===patId));
  // 完成旗 → 情報通告唔再出（池已空：任何完成旗都唔會令舊通告返嚟）
  env.S.flags['done_gig_1990_film_101'] = 1;
  api.mergeBr89Gigs();
  ok('E6 完成後情報通告落板', !env.GIGS.some(g=>/^gig_br89_/.test(g.id)));
}catch(e){ ok('E/F BR89 模組抽取/執行 ('+e.message+')', false); }

/* ================= (H) B5：BR89 映射 13 張＋R-4 雙觸發 ================= */
try{
  const modSrc = extractBetween('/* =====================================================================\n   v20a89 BR89：分支補完', '/* ---------- WF3-3 地點一次性對白');
  const env = {
    S: { flags:{}, mockRumors:[], mockCredits:[], dayIndex: 10 },
    GIGS: [], window: {},
    normalizeGigRecord: (g)=> g,
    MERGE_PAIRS: [], INTEL_FLAGS: {}, INTEL_USE_POINTS: {},
    syncNotebookMirror: ()=>{},
  };
  const api = new Function('S','GIGS','window','normalizeGigRecord','syncNotebookMirror',
    modSrc + '\nreturn { BR89_GIGS, mergeBr89Gigs, br89GigOn, br89OnGigComplete, BR89_PATRON_OF_GIG };'
  )(env.S, env.GIGS, env.window, env.normalizeGigRecord, env.syncNotebookMirror);
  const EXPECT13 = {
    gig_1991_film_101:'credit_enc83_luk_patron', gig_1991_variety_203:'credit_enc84_pang_patron',
    gig_1992_rec_106:'credit_enc84_ching_patron', gig_1991_film_103:'credit_enc79_liu_priority',
    gig_1992_film_103:'credit_enc83_liu_patron', gig_1991_film_211:'credit_enc83_mak_patron',
    gig_1992_tv_105:'credit_enc83_yip_patron', gig_1992_rec_205:'credit_enc83_gu_patron',
    gig_1991_ad_102:'credit_enc84_so_patron', gig_1991_film_213:'credit_enc84_chung_patron',
    gig_1992_rec_111:'credit_enc83_lok_patron', gig_1991_film_212:'credit_enc83_ngai_patron',
    gig_1992_film_206:'credit_enc83_chai_patron'
  };
  ok('H1 BR89 映射 13 張逐對啱（SPEC §3.5A）',
    Object.keys(api.BR89_PATRON_OF_GIG).length===13 &&
    Object.keys(EXPECT13).every(k=>api.BR89_PATRON_OF_GIG[k]===EXPECT13[k]));
  ok('H2 舊 gig_br89_* 已清', !Object.keys(api.BR89_PATRON_OF_GIG).some(k=>/^gig_br89_/.test(k)));
  // R-4 雙觸發 OR（兩條路獨立驗；v20a274：顧引薦 gig 由 gig_1992_rec_105《當年情懷》搬去新 gig_1992_rec_205《夜總會登台暖場》）
  const r4 = { id:'gig_1992_rec_205' };
  env.S.mockCredits.length = 0; env.S.flags = {};
  ok('H3 R-4 兩條路都冇 → 唔開', api.br89GigOn(r4)===false);
  env.S.flags.enc83_gu_loan_result = 1;
  ok('H4 R-4 還錢結算完成（result＝1）→ 開（唔使持債）', api.br89GigOn(r4)===true);
  env.S.flags.enc83_gu_loan_result = 2;
  ok('H5 R-4 還錢失敗（result＝2）→ 唔開', api.br89GigOn(r4)===false);
  env.S.flags = {};
  env.S.mockCredits.push({ id:'credit_enc83_gu_patron', debtor:'顧明輝', title:'登台引薦', line:'x', status:'未收' });
  ok('H6 R-4 持債權 → 開', api.br89GigOn(r4)===true);
  // 兌現標記：標題由新庫 GIGS 反查
  env.S.mockCredits.length = 0;
  env.S.mockCredits.push({ id:'credit_enc83_luk_patron', debtor:'陸柏言', title:'天王引薦', line:'x', status:'未收' });
  env.GIGS.length = 0;
  env.GIGS.push({ id:'gig_1991_film_101', title:'《江河歲月》男配角' });
  const patId = Object.keys(api.BR89_PATRON_OF_GIG).find(k=>api.BR89_PATRON_OF_GIG[k]==='credit_enc83_luk_patron');
  api.br89OnGigComplete(patId);
  const c = env.S.mockCredits.find(x=>x.id==='credit_enc83_luk_patron');
  ok('H7 兌現標記標題用新庫名（唔係「引薦通告」）', c.redeemedBy===patId && c.line.indexOf('《江河歲月》')>=0 && c.status==='未收');
}catch(e){ ok('H BR89 13 張／R-4 抽取/執行 ('+e.message+')', false); }

/* ================= (G) A_ho 寫返 npcs.agent（源碼級） ================= */
try{
  ok('G1 HO89 表齊（meet/push/crisis/ending）', html.indexOf('A_ho_ending:{ flag_ho_mentor_complete:6')>=0 && html.indexOf('flag_ho_big_bet:3')>=0 && html.indexOf('bumpNpc("agent", dv)')>=0);
  ok('G2 gu_loan 讀 mediate 旗＋顧明輝 tier ≥1（v267：情報卡閘改 tier 閘）', html.indexOf('enc87StoryFlag("flag_mediate_gu_debt")')>=0 && html.indexOf('if(beat.id==="gu_loan" && tier>=1)')>=0 && html.indexOf('br89HoldsCard("rumor_gu_money_heard")')<0);
  ok('G3 魏詠男讀 rain_split 旗', html.indexOf('flag:"flag_rain_split"')>=0);
  ok('G4 芬姐送別讀相識旗', html.indexOf('fenFlag("flag_wf4_fen_tea")')>=0 && html.indexOf('fenFlag("flag_wf4_fen_help")')>=0);
}catch(e){ ok('G 源碼檢查 ('+e.message+')', false); }

console.log(fails.length ? ('\nBR89 LOGIC: '+fails.length+' FAIL') : '\nBR89 LOGIC: ALL PASS');
process.exit(fails.length ? 1 : 0);
