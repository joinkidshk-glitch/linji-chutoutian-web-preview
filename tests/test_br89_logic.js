// v20a89 BR89 邏輯測試：分支補完 S+M
//  (A) ripple 消費者：C1–C5 文案承諾嘅 ripple 四欄（stress/health/credit/debt）＋tag 真入帳；
//      逐條對返 pack 文案數值，唔多唔少。
//  (B) 巧遇 grants 條件派發：liu_repay 推辭唔攞債權（改攞風聲卡）、mak_respect 講會驚唔攞人情；
//      應承先攞返原本嗰筆（id／debtor 逐字同 v88 定版）。
//  (C) C6F 電影線對稱幕：節點＋閘＋注入器齊；同 C6 等量級（W15、wealth 對稱）。
//  (D) 結局呈現回收：八線 ending 旗 → endingInserts410 出返該線句子；提攜債已兌現 → 點名句；
//      半線 he/be → endingRomanceScene410 分版。
//  (E) BR89 條件通告：提攜債／情報卡持有先注入，兌現／完成後唔再出；br89OnGigComplete
//      標記兌現但 status 唔郁（結局人情計數口徑不變）。
//  (F) 情報拼合新 pair＋單卡使用點：MERGE_PAIRS／INTEL_FLAGS／INTEL_USE_POINTS 真註冊；
//      持卡先有 gigLine／sightLine。
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
  const pack = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'story_detail_c1_to_c17.json'), 'utf8'));
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
  // C2_a: stressDelta +1；C2_b: −1（pack 文案數值）
  let r = runRipple('C2','C2_a'); ok('A1 C2_a ripple stress +1', r.gameDelta.stress===1);
  r = runRipple('C2','C2_b'); ok('A2 C2_b ripple stress −1', r.gameDelta.stress===-1);
  // C3_a: credit −1＋stress +2；C3_b: credit +1＋stress +3
  r = runRipple('C3','C3_a'); ok('A3 C3_a credit −1／stress +2', r.statsApplied.industryCredit===-1 && r.gameDelta.stress===2);
  r = runRipple('C3','C3_b'); ok('A4 C3_b credit +1／stress +3', r.statsApplied.industryCredit===1 && r.gameDelta.stress===3);
  // C4_a: debtDelta +1 → 真債一筆（何生）；重行唔好重複入帳
  r = runRipple('C4','C4_a'); ok('A5 C4_a 入何生人情債', r.S.mockDebts.length===1 && r.S.mockDebts[0].id==='debt_c4_ho_ripple' && r.S.mockDebts[0].creditor==='何生' && r.statsApplied.industryCredit===-1);
  // C4_b: stress +8＋health −5（→體能）
  r = runRipple('C4','C4_b'); ok('A6 C4_b stress +8／體能 −5', r.gameDelta.stress===8 && r.gameDelta.stamina===-5);
  // C1_a/b: 只有 tag／描述欄 → 入沉澱標籤，唔入任何數值（唔加文案冇講嘅懲罰）
  r = runRipple('C1','C1_a'); ok('A7 C1_a 只入標籤零數值', Object.keys(r.gameDelta).length===0 && !r.statsApplied.industryCredit && r.notes.some(x=>x.indexOf('沉澱標籤')>=0));
  r = runRipple('C1','C1_b'); ok('A8 C1_b 只入標籤零數值', Object.keys(r.gameDelta).length===0 && r.notes.some(x=>x.indexOf('沉澱標籤')>=0));
  // C5_c: stressDelta −1
  r = runRipple('C5','C5_c'); ok('A9 C5_c stress −1', r.gameDelta.stress===-1);
}catch(e){ ok('A ripple 抽取/執行 ('+e.message+')', false); }

/* ================= (B) grants 條件派發 ================= */
try{
  const grants = [], cards = [];
  const sandbox = {
    S: { flags:{}, dayIndex: 100, mockRumors: [], mockCredits: [] },
    enc79GrantCredit: (c)=>{ grants.push(c); return true; },
    enc79GrantRumorCard: (c)=>{ cards.push(c); return true; },
  };
  const src = extractFn('enc79ChoiceFx') + '\n' + extractFn('enc79RunChoiceFx');
  const api = new Function('S','enc79GrantCredit','enc79GrantRumorCard',
    src + '\nreturn { enc79ChoiceFx, enc79RunChoiceFx };')(sandbox.S, sandbox.enc79GrantCredit, sandbox.enc79GrantRumorCard);
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
  ok('B6 liu_decline 唔派債權、改派風聲卡', grants.length===0 && cards.length===1 && cards[0].id==='rumor_liu_priority_passed');
  grants.length = 0; cards.length = 0;
  api.enc79RunChoiceFx('mak_accept');
  ok('B7 mak_accept 派返原債權', grants.length===1 && grants[0].id==='credit_enc79_mak_wuzhi');
  grants.length = 0;
  api.enc79RunChoiceFx('mak_honest');
  ok('B8 mak_honest 乜都唔派', grants.length===0 && cards.length===0);
  // beat 定義已冇無條件 grants
  ok('B9 beat 定義冇 grants 殘留', !/id:"liu_repay"[^}]*grants\(/.test(html) && !/id:"mak_respect"[^}]*grants\(/.test(html));
}catch(e){ ok('B grants 抽取/執行 ('+e.message+')', false); }

/* ================= (C) C6F 對稱幕 ================= */
try{
  const gate = extractConst('STORY_GATE_3Y');
  const nodes = extractConst('STORY_SPINE_NODES_BR89');
  const env = new Function(gate + '\n' + nodes + '\nreturn { STORY_GATE_3Y, STORY_SPINE_NODES_BR89 };')();
  ok('C1 閘 C6F＝route_film＋W15（同 C6 對稱）', env.STORY_GATE_3Y.C6F && env.STORY_GATE_3Y.C6F.route==='route_film' && env.STORY_GATE_3Y.C6F.weekMin===env.STORY_GATE_3Y.C6.weekMin);
  const n = env.STORY_SPINE_NODES_BR89.C6F;
  ok('C2 節點 locId film_lion＋openConditions 對位', n.locId==='film_lion' && n.openConditions.includes('route_film') && n.openConditions.includes('week_min:15'));
  const ca = n.choices.find(c=>c.id==='C6F_a'), cb = n.choices.find(c=>c.id==='C6F_b');
  ok('C3 抉擇對稱 C6（接＝wealth 1／唔接＝零）', ca.effects.stats.wealth===1 && Object.keys(cb.effects.stats).length===0 && ca.effects.flags[0]==='flag_studio_follow' && cb.effects.flags[0]==='flag_studio_roam');
  ok('C4 注入器存在', html.indexOf('function applyStoryBr89Nodes89(')>=0 && html.indexOf('applyStoryBr89Nodes89()')>=0);
  ok('C5 進度頁有 C6F＋提示表有 C6F', html.indexOf('["C6F",20]')>=0 && html.indexOf('C6F: { playerHint:')>=0);
  ok('C6 C5 nextHint 已改兩線並陳', html.indexOf('行電影線有「片場跟班」')>=0 && html.indexOf('行電視線先有；係處境劇班底')<0);
}catch(e){ ok('C C6F 抽取/執行 ('+e.message+')', false); }

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
  S = baseS(); S.mockCredits.push({ id:'credit_enc83_luk_patron', debtor:'陸柏言', title:'天王引薦', line:'x', status:'未收', redeemedBy:'gig_br89_patron_luk' });
  ins = mk(S).endingInserts410({}, favor);
  ok('D3 提攜債已兌現 → 點名句', ins.some(t=>t.indexOf('陸柏言')>=0 && t.indexOf('兌現')>=0));
  S = baseS();
  ins = mk(S).endingInserts410({}, favor);
  ok('D4 冇旗 → 冇八線句（唔好亂出）', !ins.some(t=>t.indexOf('高俊傑同你鬥足')>=0 || t.indexOf('方小龍嗰次意外')>=0));
  // 半線 he/be 分版
  const rec = { career:'E0', romance:{ line:'vera', kind:'almost' } };
  S = baseS(); S.story.flags['flag_vera_be'] = 1;
  const beTxt = mk(S).endingRomanceScene410(rec);
  S = baseS();
  const deTxt = mk(S).endingRomanceScene410(rec);
  S = baseS(); S.story.flags['flag_vera_he'] = 1;
  const heTxt = mk(S).endingRomanceScene410(rec);
  ok('D5 Vera be 版 ≠ 預設版', beTxt !== deTxt && beTxt.indexOf('唔再係你')>=0);
  ok('D6 Vera he 版有留白句 ≠ 預設版', heTxt !== deTxt && heTxt.indexOf('留返')>=0);
  S = baseS(); S.flags['flag_xu_be'] = 1;
  const xuBe = mk(S).endingRomanceScene410({ career:'E0', romance:{ line:'xu', kind:'almost' } });
  ok('D7 徐寶珊 be 版（退禮物）', xuBe.indexOf('原封退返')>=0);
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
  const api = new Function('S','GIGS','window','normalizeGigRecord','MERGE_PAIRS','INTEL_FLAGS','INTEL_USE_POINTS','syncNotebookMirror',
    modSrc + '\nreturn { BR89_GIGS, mergeBr89Gigs, br89GigOn, br89OnGigComplete, br89HoldsCard, br89CardUsePointForGig, br89CardUsePointForStar, MERGE_PAIRS, INTEL_FLAGS, INTEL_USE_POINTS };'
  )(env.S, env.GIGS, env.window, env.normalizeGigRecord, env.MERGE_PAIRS, env.INTEL_FLAGS, env.INTEL_USE_POINTS, env.syncNotebookMirror);
  // (F) 拼合註冊
  ok('F1 新 pair ×2 已註冊', api.MERGE_PAIRS.some(p=>p.merged==='rumor_lok_highlevel_truth') && api.MERGE_PAIRS.some(p=>p.merged==='rumor_chung_farewell_truth'));
  ok('F2 情報旗映射齊', api.INTEL_FLAGS['rumor_lok_highlevel_truth']==='intel_lok_truth' && api.INTEL_FLAGS['rumor_chung_farewell_truth']==='intel_chung_leave');
  ok('F3 使用點齊', !!(api.INTEL_USE_POINTS['rumor_lok_highlevel_truth'] && api.INTEL_USE_POINTS['rumor_chung_farewell_truth']));
  // (F) 單卡使用點：冇卡 → null；有卡 → 出行
  ok('F4 冇卡冇使用點', api.br89CardUsePointForGig({ title:'彭少祺台慶騷', workTitle:'台慶大騷' })===null);
  env.S.mockRumors.push({ id:'rumor_pang_show_tip', state:'normal' });
  const cp = api.br89CardUsePointForGig({ title:'彭少祺台慶騷', workTitle:'台慶大騷' });
  ok('F5 持卡 → 通告情報行', !!cp && cp.line.indexOf('台慶大騷缺個台上助理')>=0);
  ok('F6 持卡 → 巧遇提示行', !!api.br89CardUsePointForStar('pang_siuki'));
  ok('F7 唔關事嘅星冇提示行', api.br89CardUsePointForStar('luk_baakyin')===null);
  // (E) 通告注入：冇債權冇卡 → 空板
  env.GIGS.length = 0; api.mergeBr89Gigs();
  ok('E1 冇持有 → BR89 通告唔上板', env.GIGS.length===0);
  env.S.mockCredits.push({ id:'credit_enc83_luk_patron', debtor:'陸柏言', title:'天王引薦', line:'陸柏言講過會引薦你。', status:'未收' });
  api.mergeBr89Gigs();
  ok('E2 持提攜債 → 引薦通告上板', env.GIGS.some(g=>g.id==='gig_br89_patron_luk'));
  // 情報卡 → 替身通告
  env.S.mockRumors.push({ id:'rumor_ngai_stunt_tip', state:'normal' });
  api.mergeBr89Gigs();
  ok('E3 持替身情報卡 → 情報通告上板', env.GIGS.some(g=>g.id==='gig_br89_stunt_ngai'));
  // 殺青標記兌現：line 追加、status 不變、再 merge 唔再出
  api.br89OnGigComplete('gig_br89_patron_luk');
  const c = env.S.mockCredits.find(x=>x.id==='credit_enc83_luk_patron');
  ok('E4 兌現標記＋line 交代＋status 唔郁', c.redeemedBy==='gig_br89_patron_luk' && c.line.indexOf('已兌現')>=0 && c.status==='未收');
  api.mergeBr89Gigs();
  ok('E5 兌現後引薦通告落板', !env.GIGS.some(g=>g.id==='gig_br89_patron_luk'));
  // 完成旗 → 替身通告唔再出
  env.S.flags['done_gig_br89_stunt_ngai'] = 1;
  api.mergeBr89Gigs();
  ok('E6 完成後情報通告落板', !env.GIGS.some(g=>g.id==='gig_br89_stunt_ngai'));
}catch(e){ ok('E/F BR89 模組抽取/執行 ('+e.message+')', false); }

/* ================= (G) A_ho 寫返 npcs.agent（源碼級） ================= */
try{
  ok('G1 HO89 表齊（meet/push/crisis/ending）', html.indexOf('A_ho_ending:{ flag_ho_mentor_complete:6')>=0 && html.indexOf('flag_ho_big_bet:3')>=0 && html.indexOf('bumpNpc("agent", dv)')>=0);
  ok('G2 gu_loan 讀 mediate 旗＋情報卡', html.indexOf('enc87StoryFlag("flag_mediate_gu_debt")')>=0 && html.indexOf('br89HoldsCard("rumor_gu_money_heard")')>=0);
  ok('G3 魏詠男讀 rain_split 旗', html.indexOf('flag:"flag_rain_split"')>=0);
  ok('G4 芬姐送別讀相識旗', html.indexOf('fenFlag("flag_wf4_fen_tea")')>=0 && html.indexOf('fenFlag("flag_wf4_fen_help")')>=0);
}catch(e){ ok('G 源碼檢查 ('+e.message+')', false); }

console.log(fails.length ? ('\nBR89 LOGIC: '+fails.length+' FAIL') : '\nBR89 LOGIC: ALL PASS');
process.exit(fails.length ? 1 : 0);
