// v20a269 支線實裝第一批邏輯測試：廖炳星／顧明輝／麥震東——
//   (1) 靜態：flags 欄位、冷版 beats、registry 閘（C8／C13／C15）、暖版排除式條件、
//       傳聞引用零殘留、liu_repay／mak_respect beat 定義無 grants（test_br89 B9 釘位）；
//   (2) 抉擇 fx：clash 企邊邊；舊 fx 釘位（liu_repay／mak_respect／gu_loan 唔借無 fx）保持；
//   (3) 節拍閘：patron 冷暖 shadow＋PickBeat 排序、暖版無旗照開（提攜測試態）、
//       BuildScript 兩變體（gu_n10after 認拒借／mak_patron 認守秘密）、
//       pushSeg flags 傳遞、冷版 DLG 句數。
// 反證：喺 pristine（v20a268）index 上行 → 靜態斷言乾淨 FAIL。
// 用法：node tests/test_sideline269_logic.js [path-to-index.html]
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
  let depth = 0, started = false, j = i;
  for(; j < html.length; j++){
    const c = html[j];
    if(c === '{' || c === '['){ depth++; started = true; }
    else if(c === '}' || c === ']'){ depth--; if(started && depth === 0){ j++; break; } }
    else if(c === ';' && !started) { j++; break; }
  }
  return html.slice(i, j);
}
function extractDlg(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('missing ' + name);
  const j = html.indexOf('\nconst ', i + 10);
  return html.slice(i, j < 0 ? undefined : j);
}

/* ---- (1) 靜態：新 beats／旗／閘在位 ---- */
ok('靜態：flags 欄位——廖 repay／clash', html.includes('flags: ["enc79_liu_accepted"]') && html.includes('flags: ["enc79_liu_declined"]') && html.includes('flags: ["enc79_liu_clash_stand"]') && html.includes('flags: ["enc79_liu_clash_script"]'));
ok('靜態：flags 欄位——顧 loan／n10after', html.includes('flags: ["enc83_gu_loan_refused"]') && html.includes('flags: ["gu_n10_celebrate"]') && html.includes('flags: ["gu_n10_warned"]'));
ok('靜態：flags 欄位——麥 respect／heart', html.includes('flags: ["enc79_mak_accepted"]') && html.includes('flags: ["enc79_mak_honest"]') && html.includes('flags: ["mak_kept_secret"]') && html.includes('flags: ["mak_told_doctor"]'));
ok('靜態：flags 欄位消費點——pushSeg 傳遞＋揀嗰陣寫入', html.includes('flags:c.flags||null') && html.includes('if(opt.flags) (opt.flags||[]).forEach'));
ok('靜態：冷版 beats 在位', html.includes('liu_patron_cold') && html.includes('gu_patron_cold') && html.includes('mak_patron_cold'));
ok('靜態：廖 clash 新抉擇 2 選項', html.includes('企廖炳星嗰邊，話飛紙仔改得啱') && html.includes('企導演嗰邊，話照劇本拍先啱'));
ok('靜態：registry 閘——廖 C8／C13、麥 C15', html.includes('enc83NodeDone("C8")') && html.includes('enc83NodeDone("C13")') && html.includes('enc83NodeDone("C15")'));
ok('靜態：暖版只加排除式條件（無肯定式要求）', html.includes('!((S.flags||{}).enc79_liu_declined || (S.flags||{}).enc79_liu_clash_script)') && html.includes('!(S.flags||{}).enc83_gu_loan_refused && !(S.flags||{}).gu_n10_warned') && html.includes('!(S.flags||{}).enc79_mak_honest'));
ok('靜態：傳聞引用零殘留（v267 已刪）', !html.includes('enc79GrantFrag') && !html.includes('enc79GrantRumorCard') && !html.includes('enc79HasMerged'));
ok('靜態：B9 釘位——liu_repay／mak_respect beat 定義無 grants(', (()=>{ const a = html.indexOf('{ id:"liu_repay"'); const b = html.indexOf('{ id:"mak_respect"'); return a >= 0 && b >= 0 && !html.slice(a, a + 220).includes('grants(') && !html.slice(b, b + 220).includes('grants('); })());
ok('靜態：BuildScript 變體在位——gu 認拒借／mak 認守秘密', html.includes('嗰陣你話幫唔到') && html.includes('嗰陣你應承幫我守秘密'));

/* ---- sandbox（ENC79） ---- */
let S;
let _ys = { year: 1990, season: '春' };
let _doneNodes = new Set();
let _storyFlags = {};
function resetS(day){
  S = { dayIndex: day||0, fame: 0, money: 2000, flags: {}, npcs: { agent: 0 }, mockRumors: [], mockDebts: [], mockCredits: [], board: {}, shoots: [], mapTips: {}, story: { flags: {} }, starWeek: {}, weekGigsDone: 0, starWhispers: {} };
  _doneNodes = new Set(); _storyFlags = {};
}
function setFav(sid, n){ enc79EnsureStars(); S.stars[sid].fav = n; }
function beatOf(sid, id){ return (ENC79_BEATS[sid] || []).find(b => b.id === id); }
function weekNumNow(){ return 3; }
function yearSeasonNow(){ return _ys; }
function enc87StoryFlag(f){ return !!_storyFlags[f]; }
function ensureMockJournal(){ if(!Array.isArray(S.mockRumors)) S.mockRumors=[]; if(!Array.isArray(S.mockDebts)) S.mockDebts=[]; }
function syncNotebookMirror(){}
function saveQ(){}
function refreshMoneyHud(){}
function noteWeekHighlight(){}
function rumorStateLabel(state){ return '剛聽聞'; }
function R(a,b){ return a; }
function bumpNpc(id, d){ const b = S.npcs[id]||0; S.npcs[id] = Math.min(100, b+d); return S.npcs[id]-b; }
function toast(){}
let _ledger = null;
function ensureFavorLedger(){ if(!_ledger) _ledger = { settled:0, credits:0, exodus:[], counted:{} }; return _ledger; }
function favorLedgerNoteCredit(id){ const L = ensureFavorLedger(); if(L.counted[id]) return false; L.counted[id]={kind:'credit'}; L.credits++; return true; }
function softSocialDailyCap(){ return { ok:true, used:0, max:99, left:99 }; }
function softSocialDailyUse(){}
function softPreviewOn(){ return false; }
function ending78Gate(){ return false; }
function npcNextTierHint(){ return null; }
const BehaviorGate = { featureFlag_softBehaviorGatePreview: ()=>false };
const StoryOC = {
  isDone: (id)=> _doneNodes.has(id),
  listOpen: ()=>({ open: [] }),
  findNodeRaw: (id)=>({ id }),
};
function storyNodeLocId(n){ return n && n.__loc; }
function enc79PlayEncounter(){}
function enc79LocName(id){ return id; }

const asVar = (code, name)=> code.replace('const ' + name + ' =', 'var ' + name + ' =');
const consts269 = ['ENC79_TIER_NAMES','ENC79_PLAYER_TIERS','ENC79_FAV_CAPS','ENC79_STARS','ENC79_PILOT','ENC79_STAGEUP','ENC79_CAP_LINES','ENC79_WRAP_ECHO','ENC79_BEATS','ENC79_DIALOG','ENC79_FIRST_ALT98'].map(n=> asVar(extractConst(n), n)).join('\n')
  + '\n' + ['ENC79_DLG_liu_bingxing','ENC79_DLG_mak_zhendong'].map(n=> asVar(extractDlg(n), n)).join('\n')
  + '\n' + asVar(extractDlg('ENC83_DLG_gu_mingfai'), 'ENC83_DLG_gu_mingfai')
  + '\nENC79_DIALOG["liu_bingxing"] = ENC79_DLG_liu_bingxing;\nENC79_DIALOG["mak_zhendong"] = ENC79_DLG_mak_zhendong;\nENC79_DIALOG["gu_mingfai"] = ENC83_DLG_gu_mingfai;';
const t4Start = html.indexOf('/* ---------- T4 提攜');
const t4End = html.indexOf('/* ===== v20a84 ENC84', t4Start);
if(t4Start < 0 || t4End < 0) throw new Error('T4 region not found');
const t4Region = html.slice(t4Start, t4End);
const fns269 = ['enc79StarDef','enc79Hash','enc79Rand','enc79EnsureStars','enc79StarState','enc79TierOf','enc79PlayerTier','enc79FavCap','enc79AddFav','enc79WhisperActive','enc79GrantWhisper','enc79GrantCredit','enc79BoardHasStar','enc79BoardHasActionGig','enc79BeatOpen','enc79AnyBeatOpen','enc79PickBeat','enc79ChoiceFx','enc79RunChoiceFx','enc79NormSeg','enc79BuildScript','enc83NodeDone','enc83Flag','contra98EncFirstLocSwap'];
eval(consts269 + '\n' + t4Region + '\n' + fns269.map(extractFn).join('\n'));

/* ---- (2) 抉擇 fx ---- */
resetS(100);
ok('fx：clash 企廖炳星 → +2／企導演 → -1', enc79ChoiceFx('beat:liu_clash','企廖炳星嗰邊，話飛紙仔改得啱').fav===2 && enc79ChoiceFx('beat:liu_clash','企導演嗰邊，話照劇本拍先啱').fav===-1);
ok('fx 釘位：liu_repay 應承／推辭 fx 不變', enc79ChoiceFx('beat:liu_repay','多謝受落').fx==='liu_accept' && enc79ChoiceFx('beat:liu_repay','推辭講自己排緊期').fx==='liu_decline');
ok('fx 釘位：mak_respect 應承／講驚 fx＋fav 不變', (()=>{ const a=enc79ChoiceFx('beat:mak_respect','應承隨時候命'); const b=enc79ChoiceFx('beat:mak_respect','老實講自己會驚'); return a.fx==='mak_accept' && a.fav===4 && b.fx==='mak_honest' && b.fav===2; })());
ok('fx 釘位：gu_loan 唔借 → 無 fx、fav -2（旗行 DLG 欄位）', (()=>{ const c=enc79ChoiceFx('beat:gu_loan','不借，這筆錢我真的幫不了'); return !c.fx && c.fav===-2; })());
ok('fx 釘位：liu_repay 債權經 fx 派（accept 入帳）', (()=>{ resetS(101); _ledger = null; enc79RunChoiceFx('liu_accept'); return S.mockCredits.some(c=>c.id==='credit_enc79_liu_priority'); })());
ok('fx 釘位：mak_respect 債權經 fx 派（accept 入帳）', (()=>{ resetS(102); _ledger = null; enc79RunChoiceFx('mak_accept'); return S.mockCredits.some(c=>c.id==='credit_enc79_mak_wuzhi'); })());

/* ---- (3) 節拍閘 ---- */
function openBeat(sid, id){ return enc79BeatOpen(sid, beatOf(sid, id)); }
function beatIds(sid){ return (ENC79_BEATS[sid]||[]).map(b=>b.id); }
ok('註冊順序：冷版排暖版之前（三線）', beatIds('liu_bingxing').indexOf('liu_patron_cold') < beatIds('liu_bingxing').indexOf('liu_patron') && beatIds('mak_zhendong').indexOf('mak_patron_cold') < beatIds('mak_zhendong').indexOf('mak_patron') && beatIds('gu_mingfai').indexOf('gu_patron_cold') < beatIds('gu_mingfai').indexOf('gu_patron'));
ok('冷版 DLG 句數 ≥3（三線）', ENC79_DIALOG.liu_bingxing.beats.liu_patron_cold.lines.length>=3 && ENC79_DIALOG.mak_zhendong.beats.mak_patron_cold.lines.length>=3 && ENC79_DIALOG.gu_mingfai.beats.gu_patron_cold.lines.length>=3);
ok('冷版 DLG 句數：廖 6／麥 6／顧 7', ENC79_DIALOG.liu_bingxing.beats.liu_patron_cold.lines.length===6 && ENC79_DIALOG.mak_zhendong.beats.mak_patron_cold.lines.length===6 && ENC79_DIALOG.gu_mingfai.beats.gu_patron_cold.lines.length===7);
resetS(210); _ys = { year:1990, season:'夏' }; setFav('liu_bingxing', 10);
ok('閘：liu_foreshadow C8 未完唔開（N9 開口）', openBeat('liu_bingxing','liu_foreshadow')===false);
_doneNodes.add('C8');
ok('閘：liu_foreshadow C8 完開', openBeat('liu_bingxing','liu_foreshadow')===true);
resetS(211); _ys = { year:1992, season:'冬' }; setFav('liu_bingxing', 30);
ok('閘：liu_clash C13 未完唔開（N16 再開口）', openBeat('liu_bingxing','liu_clash')===false);
_doneNodes.add('C13');
ok('閘：liu_clash C13 完開', openBeat('liu_bingxing','liu_clash')===true);
resetS(212); _ys = { year:1992, season:'秋' }; setFav('liu_bingxing', 70);
ok('閘：liu_patron 暖／冷分流（declined 行冷）', openBeat('liu_bingxing','liu_patron')===true && openBeat('liu_bingxing','liu_patron_cold')===false && (S.flags.enc79_liu_declined=1, openBeat('liu_bingxing','liu_patron')===false && openBeat('liu_bingxing','liu_patron_cold')===true));
ok('閘：liu_patron 壞旗（clash_script）行冷', (()=>{ resetS(2121); _ys = { year:1992, season:'秋' }; setFav('liu_bingxing', 70); S.flags.enc79_liu_clash_script = 1; return openBeat('liu_bingxing','liu_patron')===false && openBeat('liu_bingxing','liu_patron_cold')===true; })());
ok('閘：liu_patron 冷版排暖版之前（PickBeat 揀冷）', (()=>{ resetS(213); _ys = { year:1992, season:'秋' }; setFav('liu_bingxing', 70); S.flags.enc79_liu_declined = 1; const st = S.stars.liu_bingxing; for(const b of (ENC79_BEATS.liu_bingxing||[])) if(!b.id.endsWith('_patron') && b.id!=='liu_patron_cold') st.beatsDone[b.id] = 1; const p = enc79PickBeat('liu_bingxing'); return !!p && p.id==='liu_patron_cold'; })());
ok('閘：liu_patron 暖版 T4＋無旗 → PickBeat 揀暖（提攜測試態）', (()=>{ resetS(214); _ys = { year:1992, season:'秋' }; setFav('liu_bingxing', 70); const st = S.stars.liu_bingxing; for(const b of (ENC79_BEATS.liu_bingxing||[])) if(!b.id.endsWith('_patron')) st.beatsDone[b.id] = 1; const p = enc79PickBeat('liu_bingxing'); return !!p && p.id==='liu_patron'; })());
resetS(215); _ys = { year:1991, season:'夏' }; setFav('mak_zhendong', 30);
ok('閘：mak_intel C15 未完唔開（N12 開口）', openBeat('mak_zhendong','mak_intel')===false);
_doneNodes.add('C15');
ok('閘：mak_intel C15 完開', openBeat('mak_zhendong','mak_intel')===true);
resetS(216); _ys = { year:1992, season:'秋' }; setFav('mak_zhendong', 70);
ok('閘：mak_patron 暖／冷分流（honest 行冷）', openBeat('mak_zhendong','mak_patron')===true && openBeat('mak_zhendong','mak_patron_cold')===false && (S.flags.enc79_mak_honest=1, openBeat('mak_zhendong','mak_patron')===false && openBeat('mak_zhendong','mak_patron_cold')===true));
ok('閘：mak_patron 冷版排暖版之前（PickBeat 揀冷）', (()=>{ const st = S.stars.mak_zhendong; for(const b of (ENC79_BEATS.mak_zhendong||[])) if(!b.id.endsWith('_patron') && b.id!=='mak_patron_cold') st.beatsDone[b.id] = 1; const p = enc79PickBeat('mak_zhendong'); return !!p && p.id==='mak_patron_cold'; })());
ok('閘：mak_patron 暖版 T4＋無旗 → PickBeat 揀暖（提攜測試態）', (()=>{ resetS(217); _ys = { year:1992, season:'秋' }; setFav('mak_zhendong', 70); const st = S.stars.mak_zhendong; for(const b of (ENC79_BEATS.mak_zhendong||[])) if(!b.id.endsWith('_patron')) st.beatsDone[b.id] = 1; const p = enc79PickBeat('mak_zhendong'); return !!p && p.id==='mak_patron'; })());
ok('閘：mak_patron kept_secret 唔做閘（暖版照開）', (()=>{ resetS(218); _ys = { year:1992, season:'秋' }; setFav('mak_zhendong', 70); S.flags.mak_kept_secret = 1; return openBeat('mak_zhendong','mak_patron')===true && openBeat('mak_zhendong','mak_patron_cold')===false; })());
ok('閘：mak_patron told_doctor 唔係冷路（暖版照開）', (()=>{ resetS(219); _ys = { year:1992, season:'秋' }; setFav('mak_zhendong', 70); S.flags.mak_told_doctor = 1; return openBeat('mak_zhendong','mak_patron')===true && openBeat('mak_zhendong','mak_patron_cold')===false; })());
resetS(220); _ys = { year:1992, season:'秋' }; setFav('gu_mingfai', 70);
ok('閘：gu_patron 暖／冷分流（refused 行冷）', openBeat('gu_mingfai','gu_patron')===true && openBeat('gu_mingfai','gu_patron_cold')===false && (S.flags.enc83_gu_loan_refused=1, openBeat('gu_mingfai','gu_patron')===false && openBeat('gu_mingfai','gu_patron_cold')===true));
ok('閘：gu_patron 冷版排暖版之前（PickBeat 揀冷）', (()=>{ const st = S.stars.gu_mingfai; for(const b of (ENC79_BEATS.gu_mingfai||[])) if(!b.id.endsWith('_patron') && b.id!=='gu_patron_cold') st.beatsDone[b.id] = 1; const p = enc79PickBeat('gu_mingfai'); return !!p && p.id==='gu_patron_cold'; })());
ok('閘：gu_patron 暖版 T4＋無旗 → PickBeat 揀暖（提攜測試態）', (()=>{ resetS(221); _ys = { year:1992, season:'秋' }; setFav('gu_mingfai', 70); const st = S.stars.gu_mingfai; for(const b of (ENC79_BEATS.gu_mingfai||[])) if(!b.id.endsWith('_patron')) st.beatsDone[b.id] = 1; const p = enc79PickBeat('gu_mingfai'); return !!p && p.id==='gu_patron'; })());
ok('閘：gu_patron warned 行冷', (()=>{ resetS(222); _ys = { year:1992, season:'秋' }; setFav('gu_mingfai', 70); S.flags.gu_n10_warned = 1; return openBeat('gu_mingfai','gu_patron')===false && openBeat('gu_mingfai','gu_patron_cold')===true; })());
ok('閘：gu_patron celebrate 唔係冷路（暖版照開）', (()=>{ resetS(223); _ys = { year:1992, season:'秋' }; setFav('gu_mingfai', 70); S.flags.gu_n10_celebrate = 1; return openBeat('gu_mingfai','gu_patron')===true && openBeat('gu_mingfai','gu_patron_cold')===false; })());

/* ---- 變體（BuildScript）＋pushSeg flags 傳遞 ---- */
function metStar(sid){ enc79EnsureStars(); S.stars[sid].met = true; return S.stars[sid]; }
ok('變體：gu_n10after 認拒借（插句）', (()=>{ resetS(230); _ys = { year:1991, season:'秋' }; setFav('gu_mingfai', 30); metStar('gu_mingfai'); _doneNodes.add('N10'); S.flags.enc83_gu_loan_refused = 1; const st = S.stars.gu_mingfai; for(const b of (ENC79_BEATS.gu_mingfai||[])) if(b.id!=='gu_n10after' && !b.id.endsWith('_patron')) st.beatsDone[b.id] = 1; const built = enc79BuildScript('gu_mingfai', false); return !!built && built.steps.some(s=>String(s.text||'').indexOf('嗰陣你話幫唔到')>=0); })());
ok('變體：gu_n10after 無拒借旗唔插句', (()=>{ resetS(231); _ys = { year:1991, season:'秋' }; setFav('gu_mingfai', 30); metStar('gu_mingfai'); _doneNodes.add('N10'); const st = S.stars.gu_mingfai; for(const b of (ENC79_BEATS.gu_mingfai||[])) if(b.id!=='gu_n10after' && !b.id.endsWith('_patron')) st.beatsDone[b.id] = 1; const built = enc79BuildScript('gu_mingfai', false); return !!built && !built.steps.some(s=>String(s.text||'').indexOf('嗰陣你話幫唔到')>=0); })());
ok('變體：mak_patron 認守秘密（插句）', (()=>{ resetS(232); _ys = { year:1992, season:'秋' }; setFav('mak_zhendong', 70); metStar('mak_zhendong'); S.flags.mak_kept_secret = 1; const st = S.stars.mak_zhendong; for(const b of (ENC79_BEATS.mak_zhendong||[])) if(b.id!=='mak_patron' && !b.id.endsWith('_patron')) st.beatsDone[b.id] = 1; st.beatsDone.mak_patron_cold = 1; const built = enc79BuildScript('mak_zhendong', false); return !!built && built.steps.some(s=>String(s.text||'').indexOf('應承幫我守秘密')>=0); })());
ok('變體：mak_patron 無守秘密旗唔插句', (()=>{ resetS(233); _ys = { year:1992, season:'秋' }; setFav('mak_zhendong', 70); metStar('mak_zhendong'); const st = S.stars.mak_zhendong; for(const b of (ENC79_BEATS.mak_zhendong||[])) if(b.id!=='mak_patron' && !b.id.endsWith('_patron')) st.beatsDone[b.id] = 1; st.beatsDone.mak_patron_cold = 1; const built = enc79BuildScript('mak_zhendong', false); return !!built && !built.steps.some(s=>String(s.text||'').indexOf('應承幫我守秘密')>=0); })());
ok('pushSeg：liu_repay 抉擇 options 帶 flags', (()=>{ resetS(234); _ys = { year:1991, season:'夏' }; setFav('liu_bingxing', 30); metStar('liu_bingxing'); const st = S.stars.liu_bingxing; for(const b of (ENC79_BEATS.liu_bingxing||[])) if(b.id!=='liu_repay' && !b.id.endsWith('_patron')) st.beatsDone[b.id] = 1; const built = enc79BuildScript('liu_bingxing', false); const ch = (built.steps||[]).find(s=>s.choice && s.seg==='beat:liu_repay'); return !!ch && JSON.stringify(ch.options[0].flags)==='["enc79_liu_accepted"]' && JSON.stringify(ch.options[1].flags)==='["enc79_liu_declined"]'; })());
ok('pushSeg：liu_clash 抉擇 options 帶 flags', (()=>{ resetS(235); _ys = { year:1992, season:'冬' }; setFav('liu_bingxing', 30); metStar('liu_bingxing'); _doneNodes.add('C13'); const st = S.stars.liu_bingxing; for(const b of (ENC79_BEATS.liu_bingxing||[])) if(b.id!=='liu_clash' && !b.id.endsWith('_patron')) st.beatsDone[b.id] = 1; const built = enc79BuildScript('liu_bingxing', false); const ch = (built.steps||[]).find(s=>s.choice && s.seg==='beat:liu_clash'); return !!ch && JSON.stringify(ch.options[0].flags)==='["enc79_liu_clash_stand"]' && JSON.stringify(ch.options[1].flags)==='["enc79_liu_clash_script"]'; })());
ok('pushSeg：gu_loan 抉擇 options 帶 flags（唔借）', (()=>{ resetS(236); _ys = { year:1991, season:'夏' }; setFav('gu_mingfai', 30); metStar('gu_mingfai'); const st = S.stars.gu_mingfai; for(const b of (ENC79_BEATS.gu_mingfai||[])) if(b.id!=='gu_loan' && !b.id.endsWith('_patron')) st.beatsDone[b.id] = 1; const built = enc79BuildScript('gu_mingfai', false); const ch = (built.steps||[]).find(s=>s.choice && s.seg==='beat:gu_loan'); return !!ch && JSON.stringify(ch.options[2].flags)==='["enc83_gu_loan_refused"]'; })());
ok('pushSeg：mak_respect 抉擇 options 帶 flags', (()=>{ resetS(237); _ys = { year:1992, season:'春' }; setFav('mak_zhendong', 30); metStar('mak_zhendong'); S.stars.mak_zhendong.workedWith = true; const st = S.stars.mak_zhendong; for(const b of (ENC79_BEATS.mak_zhendong||[])) if(b.id!=='mak_respect' && !b.id.endsWith('_patron')) st.beatsDone[b.id] = 1; const built = enc79BuildScript('mak_zhendong', false); const ch = (built.steps||[]).find(s=>s.choice && s.seg==='beat:mak_respect'); return !!ch && JSON.stringify(ch.options[0].flags)==='["enc79_mak_accepted"]' && JSON.stringify(ch.options[1].flags)==='["enc79_mak_honest"]'; })());

console.log(fails.length ? ('\nFAILURES: ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
