/* v20a159 ROM159 Phase 1＋v159 感情線重排邏輯測試：抽 ROM159 純函數＋stub 跑行為。
   反證行法：ROM159_INDEX=~/workspace/linji-repo/index.html node tests/test_rom159_logic.js
   → 應該 FAIL（pristine 抽唔到 ROM159 函數）；預設行 work159 index 應該全 PASS。 */
'use strict';
const fs = require('fs');
const path = require('path');
const INDEX = process.env.ROM159_INDEX || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(INDEX, 'utf8');
let pass = 0, fail = 0;
function ok(name, cond) { if (cond) { pass++; } else { fail++; console.log('FAIL: ' + name); } }

function extractFn(sig) {
  const s = html.indexOf(sig);
  if (s < 0) return null;
  let i = html.indexOf('{', s), d = 0, inS = null, esc = false, k;
  for (k = i; k < html.length; k++) {
    const c = html[k];
    if (inS) { if (esc) esc = false; else if (c === '\\') esc = true; else if (c === inS) inS = null; continue; }
    if (c === '"' || c === "'" || c === '`') { inS = c; continue; }
    if (c === '{') d++; else if (c === '}') { d--; if (!d) break; }
  }
  return html.slice(s, k + 1);
}
function extractConst(name) {
  const s = html.indexOf('const ' + name);
  if (s < 0) return null;
  const eq = html.indexOf('=', s);
  let i = html.indexOf('{', eq), j = html.indexOf('[', eq);
  if (j >= 0 && (i < 0 || j < i)) i = j;
  const open = html[i], close = open === '{' ? '}' : ']';
  let d = 0, inS = null, esc = false, k;
  for (k = i; k < html.length; k++) {
    const c = html[k];
    if (inS) { if (esc) esc = false; else if (c === '\\') esc = true; else if (c === inS) inS = null; continue; }
    if (c === '"' || c === "'" || c === '`') { inS = c; continue; }
    if (c === open) d++; else if (c === close) { d--; if (!d) break; }
  }
  return 'const ' + name + ' = ' + html.slice(i, k + 1) + ';';
}

/* ---- stub 環境（注意：S 係同一個物件原地重置，唔可以換新物件——env 捉住佢） ---- */
const S = {
  dayIndex: 10, money: 10000, flags: {},
  story: { rel: {}, flags: {}, done: {} },
  weekPlan: ['scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'],
  shoots: [], booked: [],
  romance159: { week: 1, enc: {}, dates: {}, dateWeekWho: null, phone: {}, softWarn: {} },
};
let talkMet = true;
let playerTier = 0; /* v159：enc79PlayerTier stub，阿偉級數（0 臨記／1 配角） */
const toasts = [];
const GIFT_PREFS = { npcs: {
  hiu: { likes: ['gift_pineapple_bun_set', 'gift_egg_tart_box'], dislikes: [] },
  choi: { likes: ['gift_coffee_beans', 'gift_memo_pad'], dislikes: [] },
  lan: { likes: ['gift_handmade_sweet', 'gift_cassette_indie'], dislikes: ['gift_perfume_sample'] },
  xu: { likes: [], dislikes: ['gift_pineapple_bun_set', 'gift_handmade_sweet', 'gift_egg_tart_box'] },
  /* yip／so 故意唔放：rom159ApplyGiftOverrides 要自己建立條目（pack 無佢哋） */
} };
const GIFT_REACT = { byKey: {}, entries: [] };
function resetS() {
  S.dayIndex = 10; S.money = 10000; S.flags = {};
  S.story = { rel: {}, flags: {}, done: {} };
  S.weekPlan = ['scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all', 'scout_all'];
  S.shoots = []; S.booked = [];
  S.romance159 = { week: 1, enc: {}, dates: {}, dateWeekWho: null, phone: {}, softWarn: {} };
  talkMet = true;
  toasts.length = 0;
}
resetS();
const StoryOC = {
  getRel: (k) => Number((S.story.rel || {})[k]) || 0,
  getFlag: (k) => !!((S.story.flags || {})[k]),
  isDone: (id) => !!(S.story.done || {})[id],
  ensure: () => {},
  iterNodes: () => [],
  hasPlayerOffer: () => false,
  findNodeRaw: (id) => {
    const known = {
      R_yip_meet: { id: 'R_yip_meet', phase: 'P2', openConditions: ['phase_P2'] },
      R_so_meet: { id: 'R_so_meet', phase: 'P3', openConditions: ['phase_P3'] },
      R_yip_push1: { id: 'R_yip_push1', phase: 'P2', openConditions: [] },
      R_so_push1: { id: 'R_so_push1', phase: 'P3', openConditions: [] },
      R_yip_push2: { id: 'R_yip_push2', phase: 'P3', openConditions: [] },
      R_so_push2: { id: 'R_so_push2', phase: 'P4', openConditions: [] },
      R_yip_crisis: { id: 'R_yip_crisis', phase: 'P4', openConditions: [] },
      R_so_crisis: { id: 'R_so_crisis', phase: 'P4', openConditions: [] },
      R_yip_ending: { id: 'R_yip_ending', phase: 'P5', openConditions: ['phase_P5'] },
      R_so_ending: { id: 'R_so_ending', phase: 'P5', openConditions: ['phase_P5'] },
    };
    return known[id] || null;
  },
  evalNode: () => ({ ok: true }),
};
const GiftShop = {
  weekNow: () => 1,
  talkMetOk: () => talkMet,
  romanceKeyFromMapNpc: (id) => ({ colleague: 'hiu', reporter: 'choi' }[id] || null),
};
const toast = (m) => { toasts.push(String(m)); };
const saveQ = () => {};
const enc87StoryFlag = (f) => !!((S.story.flags || {})[f]);
const weekdayIdx = (d) => ((d % 7) + 7) % 7;
const enc79PlayerTier = () => playerTier;

/* COMMIT48_DEFS／NODES 嘅新條目係後面賦值加（COMMIT48_DEFS.CMT_x = {...};），
   唔喺 const 字面量入面——要連賦值句一齊抽，否則 env 只得 hiu／choi。 */
function extractAssigns(prefix) {
  const out = [];
  let from = 0;
  for (;;) {
    const s = html.indexOf(prefix, from);
    if (s < 0) break;
    const eq = html.indexOf('=', s);
    const i = html.indexOf('{', eq);
    let d = 0, inS = null, esc = false, k;
    for (k = i; k < html.length; k++) {
      const c = html[k];
      if (inS) { if (esc) esc = false; else if (c === '\\') esc = true; else if (c === inS) inS = null; continue; }
      if (c === '"' || c === "'" || c === '`') { inS = c; continue; }
      if (c === '{') d++; else if (c === '}') { d--; if (!d) break; }
    }
    const semi = html.indexOf(';', k);
    out.push(html.slice(s, semi + 1));
    from = semi + 1;
  }
  return out.join('\n');
}
const DEFS_ASSIGN = extractAssigns('COMMIT48_DEFS.CMT_');
ok('抽到 CMT DEFS 賦值句', DEFS_ASSIGN.indexOf('CMT_lan_commit') >= 0 && DEFS_ASSIGN.indexOf('CMT_so_commit') >= 0 && DEFS_ASSIGN.indexOf('CMT_vera_commit') < 0);
function extractScalar(name) {
  const s = html.indexOf('const ' + name);
  if (s < 0) return null;
  const e = html.indexOf(';', s);
  if (e < 0) return null;
  return html.slice(s, e + 1);
}
const CONSTS = ['ROM159_LOCK_REL', 'ROM159_ENC_CAP', 'ROM159_DATE_PER_WEEK']
  .map(extractScalar)
  .concat(['ROM159_WOMEN', 'ROM159_DATES', 'ROM159_XU_PRICES', 'ROM159_GIFT_OVERRIDES',
    'ROM176_MEET_NODES', 'COMMIT48_DEFS']
  .map(extractConst));
const FNS = ['rom159Week', 'rom159State', 'rom159RelKeyWho', 'rom159RelOf',
  'rom159EnsureLock', 'rom159LockedWho', 'rom159SetLock', 'rom159GainAllowed',
  'rom159CheckLock', 'rom159GiftBlocked', 'rom159TalkCapped', 'rom159RecordTalk',
  'rom159HasPhone', 'rom159PhoneExchange', 'rom159DateGate', 'rom159TodayConflict',
  'rom159PrepareNode', 'rom159ApplyGiftOverrides', 'rom159SoMeetGate',
  'rom176BeatOpen', 'choice47StoryFlag'].map(n => extractFn('function ' + n + '('));
ok('抽到全部 const', CONSTS.every(Boolean));
ok('抽到全部函數', FNS.every(Boolean));
if (!CONSTS.every(Boolean) || !FNS.every(Boolean)) {
  console.log('TOTAL PASS ' + pass + ' FAIL ' + fail);
  process.exit(1);
}
const env = new Function('S', 'StoryOC', 'GiftShop', 'toast', 'saveQ', 'enc87StoryFlag',
  'weekdayIdx', 'GIFT_PREFS', 'GIFT_REACT', 'enc79PlayerTier',
  CONSTS.join('\n') + '\n' + DEFS_ASSIGN + '\n' + FNS.join('\n') +
  '\nreturn { ROM159_WOMEN, ROM159_DATES, ROM159_XU_PRICES, ROM159_GIFT_OVERRIDES,' +
  ' ROM176_MEET_NODES, COMMIT48_DEFS,' +
  ' rom159RelKeyWho, rom159RelOf, rom159EnsureLock, rom159LockedWho, rom159SetLock,' +
  ' rom159GainAllowed, rom159CheckLock, rom159GiftBlocked, rom159TalkCapped,' +
  ' rom159RecordTalk, rom159HasPhone, rom159PhoneExchange, rom159DateGate,' +
  ' rom159TodayConflict, rom159PrepareNode, rom159ApplyGiftOverrides,' +
  ' rom159SoMeetGate, rom176BeatOpen, choice47StoryFlag };')
  (S, StoryOC, GiftShop, toast, saveQ, enc87StoryFlag, weekdayIdx, GIFT_PREFS, GIFT_REACT, enc79PlayerTier);

/* ---- A. relKey ↔ 人對照 ---- */
ok('A rel_hiu→hiu', env.rom159RelKeyWho('rel_hiu') === 'hiu');
ok('A rel_yip→yip', env.rom159RelKeyWho('rel_yip') === 'yip');
ok('A rel_so→so', env.rom159RelKeyWho('rel_so') === 'so');
ok('A rel_vera→null（Vera 出局）', env.rom159RelKeyWho('rel_vera') === null);
ok('A rel_mei→null（海媚出局）', env.rom159RelKeyWho('rel_mei') === null);
ok('A rel_tang→null（鄧唔入線）', env.rom159RelKeyWho('rel_tang') === null);
ok('A rel_ho→null（非感情）', env.rom159RelKeyWho('rel_ho') === null);
ok('A 裸名 hiu→hiu', env.rom159RelKeyWho('hiu') === 'hiu');

/* ---- B. 排他鎖凍結 ---- */
resetS();
ok('B 未鎖：全部放行', env.rom159GainAllowed('rel_choi') === true);
S.flags = { flag_romance_locked: true, romance_locked_who: 'hiu' };
S.story.rel = { rel_hiu: 5, rel_choi: 2 };
ok('B 鎖曉晴：采兒凍結', env.rom159GainAllowed('rel_choi') === false);
ok('B 鎖曉晴：曉晴照加', env.rom159GainAllowed('rel_hiu') === true);
ok('B 鎖曉晴：非感情 rel_ho 照加', env.rom159GainAllowed('rel_ho') === true);
ok('B 鎖曉晴：葉敏芝凍結', env.rom159GainAllowed('rel_yip') === false);
ok('B 鎖曉晴：蘇芷茵凍結', env.rom159GainAllowed('rel_so') === false);
ok('B 鎖曉晴：Vera 唔受鎖影響（已出局，pack NPC 送禮殘留——見報告）', env.rom159GainAllowed('rel_vera') === true);

/* ---- C. rel 4 軟提示 → rel 5 鎖定（注意：bumpRel 係先加數、再 CheckLock，
       所以呼叫 CheckLock 之前 S.story.rel 已經係加完嗰個數——要照呢個次序模擬） ---- */
resetS();
S.story.rel = { rel_hiu: 4 };
env.rom159CheckLock('rel_hiu', 4);
ok('C rel 4：軟提示旗落咗', S.romance159.softWarn.hiu === 1);
ok('C rel 4：待發通知係 soft', S.romance159.pendingNotice && S.romance159.pendingNotice.type === 'soft');
ok('C rel 4：未鎖', env.rom159LockedWho() === null);
ok('C rel 4：toast 有軟提示', toasts.some(t => t.indexOf('越嚟越近') >= 0));
S.story.rel = { rel_hiu: 5 };
env.rom159CheckLock('rel_hiu', 5);
ok('C rel 5：鎖定曉晴', env.rom159LockedWho() === 'hiu');
ok('C rel 5：待發通知係 lock', S.romance159.pendingNotice && S.romance159.pendingNotice.type === 'lock');
ok('C rel 5：toast 有鎖定句', toasts.some(t => t.indexOf('心入面已經有人') >= 0));
env.rom159CheckLock('rel_hiu', 4);
ok('C 軟提示只發一次', toasts.filter(t => t.indexOf('越嚟越近') >= 0).length === 1);

/* ---- C2. 實駕 T2 回歸：送最愛禮 rel 4→6（bumpRel 先加到 6 再 CheckLock）——
       舊寫法 CheckLock 入面先行 EnsureLock 遷移，見到 6 分靜默鎖咗，食咗 lock 通知＋toast；
       修正後必須照出 lock 通知＋toast。 ---- */
resetS();
S.story.rel = { rel_hiu: 6 };
env.rom159CheckLock('rel_hiu', 6);
ok('C2 rel 6：鎖定曉晴', env.rom159LockedWho() === 'hiu');
ok('C2 rel 6：待發通知係 lock（唔係俾遷移食咗）', S.romance159.pendingNotice && S.romance159.pendingNotice.type === 'lock');
ok('C2 rel 6：toast 有鎖定句', toasts.some(t => t.indexOf('心入面已經有人') >= 0));

/* ---- D. 舊檔遷移：未鎖但有人已 ≥5 → 鎖最高嗰位 ---- */
resetS();
S.story.rel = { rel_choi: 5, rel_hiu: 3 };
ok('D 遷移：鎖采兒（5 分最高）', env.rom159EnsureLock() === 'choi');
resetS();
S.story.rel = { rel_hiu: 5, rel_choi: 5 };
ok('D 遷移：同分鎖曉晴（次序優先）', env.rom159EnsureLock() === 'hiu');
resetS();
S.story.rel = { rel_hiu: 4, rel_choi: 4 };
ok('D 遷移：全部未到 5 唔鎖', env.rom159EnsureLock() === null);
resetS();
S.story.rel = { rel_yip: 5, rel_hiu: 3 };
ok('D 遷移：鎖葉敏芝（5 分最高）', env.rom159EnsureLock() === 'yip');
resetS();
S.story.rel = { rel_so: 6, rel_yip: 5 };
ok('D 遷移：鎖蘇芷茵（6 分最高）', env.rom159EnsureLock() === 'so');

/* ---- D2. 舊檔遷移照舊靜默：直接 EnsureLock 鎖人，唔出通知／toast（鎖定時刻已過）。 ---- */
resetS();
S.story.rel = { rel_choi: 5, rel_hiu: 3 };
ok('D2 遷移鎖采兒', env.rom159EnsureLock() === 'choi');
ok('D2 遷移唔出通知', !S.romance159.pendingNotice);
ok('D2 遷移唔出 toast', toasts.length === 0);

/* ---- E. 送禮拒收 ---- */
resetS();
S.flags = { flag_romance_locked: true, romance_locked_who: 'hiu' };
ok('E 鎖曉晴：送采兒被拒', typeof env.rom159GiftBlocked('choi') === 'string' && env.rom159GiftBlocked('choi').indexOf('心領') === 0);
ok('E 鎖曉晴：送曉晴照收', env.rom159GiftBlocked('hiu') === null);
ok('E 鎖曉晴：送葉敏芝被拒', typeof env.rom159GiftBlocked('yip') === 'string');
ok('E 鎖曉晴：送蘇芷茵被拒', typeof env.rom159GiftBlocked('so') === 'string');
ok('E 鎖曉晴：鄧唔受鎖影響', env.rom159GiftBlocked('tang') === null);
resetS();
ok('E 未鎖：送禮唔擋', env.rom159GiftBlocked('choi') === null);

/* ---- F. 約會閘 ---- */
resetS();
/* v20a378（U10）：約會要先行完故事初遇節點——測試預設六線 meet 已做，「未見面」個案清走曉晴 meet。 */
S.story.done = { R_hiu_meet:true, R_choi_meet:true, R_lan_meet:true, R_xu_meet:true, R_yip_meet:true, R_so_meet:true };
ok('F 未見面約唔到', (() => { delete S.story.done.R_hiu_meet; const g = env.rom159DateGate('hiu', null); return !g.ok && g.reason.indexOf('見過面') >= 0; })());
resetS();
S.story.done = { R_hiu_meet:true, R_choi_meet:true, R_lan_meet:true, R_xu_meet:true, R_yip_meet:true, R_so_meet:true };
ok('F 見過面＋有錢：開', env.rom159DateGate('hiu', null).ok === true);
ok('F 銀包唔夠：擋', env.rom159DateGate('hiu', { cost: 60 }).ok === false || (() => { S.money = 10; return env.rom159DateGate('hiu', { cost: 60 }).ok === false; })());
resetS();
S.story.done = { R_hiu_meet:true, R_choi_meet:true, R_lan_meet:true, R_xu_meet:true, R_yip_meet:true, R_so_meet:true };
S.romance159.dates = { hiu: 1 };
ok('F 今週已約過佢：擋', env.rom159DateGate('hiu', null).ok === false);
resetS();
S.story.done = { R_hiu_meet:true, R_choi_meet:true, R_lan_meet:true, R_xu_meet:true, R_yip_meet:true, R_so_meet:true };
S.romance159.dateWeekWho = 'choi';
ok('F 今週已約第二個人：擋', env.rom159DateGate('hiu', null).ok === false);
resetS();
S.story.done = { R_hiu_meet:true, R_choi_meet:true, R_lan_meet:true, R_xu_meet:true, R_yip_meet:true, R_so_meet:true };
S.flags = { flag_romance_locked: true, romance_locked_who: 'choi' };
ok('F 鎖咗采兒：約曉晴擋', env.rom159DateGate('hiu', null).ok === false);
ok('F 鎖咗采兒：約采兒開', env.rom159DateGate('choi', null).ok === true);
resetS();
S.story.done = { R_hiu_meet:true, R_choi_meet:true, R_lan_meet:true, R_xu_meet:true, R_yip_meet:true, R_so_meet:true };
ok('F 藍有 spots：見過面就約到', env.rom159DateGate('lan', null).ok === true);
resetS();
S.story.done = { R_hiu_meet:true, R_choi_meet:true, R_lan_meet:true, R_xu_meet:true, R_yip_meet:true, R_so_meet:true };
ok('F 葉有 spots：見過面就約到', env.rom159DateGate('yip', null).ok === true);
resetS();
S.story.done = { R_hiu_meet:true, R_choi_meet:true, R_lan_meet:true, R_xu_meet:true, R_yip_meet:true, R_so_meet:true };
ok('F 蘇有 spots：見過面就約到', env.rom159DateGate('so', null).ok === true);

/* ---- G. 撞期偵測 ---- */
resetS();
S.weekPlan[3] = 'shoot:x1';
S.shoots = [{ id: 'x1', title: '《戲名》' }];
ok('G 拍攝日撞期', (() => { const c = env.rom159TodayConflict(); return c && c.kind === 'shoot' && c.title === '《戲名》'; })());
resetS();
S.weekPlan[3] = 'job:g1';
S.booked = [{ gigId: 'g1', title: '試鏡戲' }];
ok('G 試鏡日撞期', (() => { const c = env.rom159TodayConflict(); return c && c.kind === 'audition' && c.title === '試鏡戲'; })());
resetS();
ok('G 自由日唔撞期', env.rom159TodayConflict() === null);

/* ---- H. 結局節點預備鉤 ---- */
function endingNode(id, heId) {
  return { id, choices: [
    { id: heId, label: '確定關係', effects: { flags: ['flag_x_he', 'flag_x_commit'], stats: {}, notes: 'HE' } },
    { id: heId.replace('_he', '_be'), label: '保持距離', effects: { flags: ['flag_x_be'], stats: {}, notes: 'BE' } },
  ] };
}
resetS();
S.flags = { flag_romance_locked: true, romance_locked_who: 'choi' };
const origHiu = endingNode('R_hiu_ending', 'C_hiu_ending_he');
let out = env.rom159PrepareNode(origHiu);
ok('H 鎖采兒：曉晴 ending HE 換坦白', out && out.choices[0].label.indexOf('坦白心意') === 0);
ok('H 坦白只寫 BE 旗', out && out.choices[0].effects.flags.length === 1 && out.choices[0].effects.flags[0] === 'flag_hiu_be');
ok('H 原節點唔郁', origHiu.choices[0].id === 'C_hiu_ending_he');
resetS();
S.flags = { flag_romance_locked: true, romance_locked_who: 'hiu' };
out = env.rom159PrepareNode(endingNode('R_choi_ending', 'C_choi_ending_he'));
ok('H 鎖曉晴：采兒 ending HE 同樣換坦白', out && out.choices.length === 2 && out.choices[0].label.indexOf('坦白心意') === 0);
resetS();
S.flags = { flag_romance_locked: true, romance_locked_who: 'choi' };
out = env.rom159PrepareNode(endingNode('R_choi_ending', 'C_choi_ending_he'));
ok('H 鎖采兒：采兒 HE 拆兩揀', out && out.choices.length === 3);
ok('H 公開寫 flag_choi_public＋fame', out && out.choices.some(c => c.id === 'C_choi_ending_he_public' && c.effects.flags.indexOf('flag_choi_public') >= 0 && c.effects.stats.fame === 1));
ok('H 低調唔寫 public', out && out.choices.some(c => c.id === 'C_choi_ending_he_quiet' && c.effects.flags.indexOf('flag_choi_public') < 0 && c.effects.flags.indexOf('flag_choi_commit') >= 0));
resetS();
S.flags = { flag_romance_locked: true, romance_locked_who: 'choi' };
out = env.rom159PrepareNode(endingNode('R_yip_ending', 'C_yip_ending_he'));
ok('H 鎖采兒：葉 ending HE 同樣換坦白', out && out.choices[0].label.indexOf('坦白心意') === 0 && out.choices[0].effects.flags[0] === 'flag_yip_be');
resetS();
S.flags = { flag_romance_locked: true, romance_locked_who: 'so' };
out = env.rom159PrepareNode(endingNode('R_so_ending', 'C_so_ending_he'));
ok('H 鎖蘇：蘇 ending 唔換（自己線）', out === null);
resetS();
ok('H 未鎖：葉 ending 唔郁', env.rom159PrepareNode(endingNode('R_yip_ending', 'C_yip_ending_he')) === null);
resetS();
S.flags = { flag_romance_locked: true, romance_locked_who: 'hiu' };
S.story.flags = { flag_hiu_commit: true };
ok('H 已 commit：唔再換', env.rom159PrepareNode(endingNode('R_hiu_ending', 'C_hiu_ending_he')) === null);

/* ---- I. 送禮覆寫數據＋徐寶珊價錢表＋撞到計數 ---- */
ok('I 曉晴最愛 2 樣', env.ROM159_GIFT_OVERRIDES.favorites.hiu.length === 2);
ok('I 曉晴最愛係菠蘿油＋蛋撻', env.ROM159_GIFT_OVERRIDES.favorites.hiu.indexOf('gift_pineapple_bun_set') >= 0 && env.ROM159_GIFT_OVERRIDES.favorites.hiu.indexOf('gift_egg_tart_box') >= 0);
ok('I 采兒 dislike 加香水＋雜誌', env.ROM159_GIFT_OVERRIDES.dislikesAdd.choi.indexOf('gift_perfume_sample') >= 0 && env.ROM159_GIFT_OVERRIDES.dislikesAdd.choi.indexOf('gift_fashion_mag') >= 0);
ok('I 藍最愛係甜品盒＋卡帶', env.ROM159_GIFT_OVERRIDES.favorites.lan.indexOf('gift_handmade_sweet') >= 0 && env.ROM159_GIFT_OVERRIDES.favorites.lan.indexOf('gift_cassette_indie') >= 0);
ok('I 藍喜歡係菠蘿油／蛋撻／保溫瓶', JSON.stringify(env.ROM159_GIFT_OVERRIDES.likes.lan) === JSON.stringify(['gift_pineapple_bun_set', 'gift_egg_tart_box', 'gift_thermos']));
ok('I 藍 dislike 加香水', env.ROM159_GIFT_OVERRIDES.dislikesAdd.lan.indexOf('gift_perfume_sample') >= 0);
ok('I 徐最愛係保溫瓶＋卡帶', env.ROM159_GIFT_OVERRIDES.favorites.xu.indexOf('gift_thermos') >= 0 && env.ROM159_GIFT_OVERRIDES.favorites.xu.indexOf('gift_cassette_indie') >= 0);
ok('I 徐喜歡係咖啡豆／拍紙簿', JSON.stringify(env.ROM159_GIFT_OVERRIDES.likes.xu) === JSON.stringify(['gift_coffee_beans', 'gift_memo_pad']));
ok('I 葉最愛係卡帶＋咖啡豆', env.ROM159_GIFT_OVERRIDES.favorites.yip.indexOf('gift_cassette_indie') >= 0 && env.ROM159_GIFT_OVERRIDES.favorites.yip.indexOf('gift_coffee_beans') >= 0);
ok('I 葉 dislike 香水＋雜誌', env.ROM159_GIFT_OVERRIDES.dislikesAdd.yip.indexOf('gift_perfume_sample') >= 0 && env.ROM159_GIFT_OVERRIDES.dislikesAdd.yip.indexOf('gift_fashion_mag') >= 0);
ok('I 蘇最愛係卡帶＋拍紙簿', env.ROM159_GIFT_OVERRIDES.favorites.so.indexOf('gift_cassette_indie') >= 0 && env.ROM159_GIFT_OVERRIDES.favorites.so.indexOf('gift_memo_pad') >= 0);
ok('I 蘇 dislike 香水＋雜誌', env.ROM159_GIFT_OVERRIDES.dislikesAdd.so.indexOf('gift_perfume_sample') >= 0 && env.ROM159_GIFT_OVERRIDES.dislikesAdd.so.indexOf('gift_fashion_mag') >= 0);
ok('I 覆寫無 vera', !env.ROM159_GIFT_OVERRIDES.favorites.vera && !(env.ROM159_GIFT_OVERRIDES.dislikesAdd || {}).vera);
ok('I 反應句 22 條', env.ROM159_GIFT_OVERRIDES.react.length === 22);
ok('I 徐寶珊價錢：中環貴過茶餐廳', env.ROM159_XU_PRICES.ad_central === 150 && env.ROM159_XU_PRICES.cafe_cha === 35);
ok('I 約會地點：曉晴 7 個（含茶餐廳）', env.ROM159_WOMEN.hiu.spots.length === 7);
ok('I 約會地點：采兒 5 個', env.ROM159_WOMEN.choi.spots.length === 5);
ok('I 約會地點：藍 6 個', env.ROM159_WOMEN.lan.spots.length === 6);
ok('I 約會地點：徐 7 個', env.ROM159_WOMEN.xu.spots.length === 7);
ok('I 約會地點：葉 6 個', env.ROM159_WOMEN.yip.spots.length === 6);
ok('I 約會地點：蘇 6 個', env.ROM159_WOMEN.so.spots.length === 6);
ok('I 約會地點：六人共 37 場', Object.values(env.ROM159_WOMEN).reduce((n, w) => n + w.spots.length, 0) === 37);
ok('I 約會地點：全部係現有 21 地點（15 舊＋6 約會新點）', (() => {
  const locs = ['film_lion', 'rec_hk', 'tvb_longmen', 'tvb_kowloon', 'tvb_harbour', 'film_cotton', 'film_harbour', 'ad_central', 'ad_adm', 'rec_wanchai', 'rec_star', 'cafe_cha', 'agency_ho', 'gift_shop', 'hospital', 'date_harbour', 'date_peak', 'date_lounge', 'date_cinema', 'date_beach', 'date_airport'];
  return Object.values(env.ROM159_DATES).every(d => locs.indexOf(d.locId) >= 0);
})());
ok('I 約會地點：事務所／醫院唔做約會地點', (() => {
  return Object.values(env.ROM159_DATES).every(d => d.locId !== 'agency_ho' && d.locId !== 'hospital');
})());
resetS();
ok('I 覆寫第一次行到', env.rom159ApplyGiftOverrides() === true);
ok('I 覆寫後曉晴 favorites 落袋', GIFT_PREFS.npcs.hiu.favorites.length === 2);
ok('I 覆寫後采兒 dislikes 有香水', GIFT_PREFS.npcs.choi.dislikes.indexOf('gift_perfume_sample') >= 0);
ok('I 覆寫後藍 likes 係菠蘿油／蛋撻／保溫瓶', JSON.stringify(GIFT_PREFS.npcs.lan.likes) === JSON.stringify(['gift_pineapple_bun_set', 'gift_egg_tart_box', 'gift_thermos']));
ok('I 覆寫後藍 dislikes 有香水', GIFT_PREFS.npcs.lan.dislikes.indexOf('gift_perfume_sample') >= 0);
ok('I 覆寫後徐 favorites 係保溫瓶＋卡帶', GIFT_PREFS.npcs.xu.favorites.indexOf('gift_thermos') >= 0 && GIFT_PREFS.npcs.xu.favorites.indexOf('gift_cassette_indie') >= 0);
ok('I 覆寫後徐 dislikes 照舊有菠蘿油', GIFT_PREFS.npcs.xu.dislikes.indexOf('gift_pineapple_bun_set') >= 0);
ok('I 覆寫後葉條目建立', !!GIFT_PREFS.npcs.yip && GIFT_PREFS.npcs.yip.relKey === 'rel_yip' && GIFT_PREFS.npcs.yip.displayName === '葉敏芝');
ok('I 覆寫後葉最愛卡帶＋咖啡豆', GIFT_PREFS.npcs.yip.favorites.indexOf('gift_cassette_indie') >= 0 && GIFT_PREFS.npcs.yip.favorites.indexOf('gift_coffee_beans') >= 0);
ok('I 覆寫後葉 requireFlagsAny 係 meet 旗', JSON.stringify(GIFT_PREFS.npcs.yip.requireFlagsAny) === JSON.stringify(['flag_yip_met_warm', 'flag_yip_met_cool']));
ok('I 覆寫後蘇條目建立', !!GIFT_PREFS.npcs.so && GIFT_PREFS.npcs.so.relKey === 'rel_so' && GIFT_PREFS.npcs.so.displayName === '蘇芷茵');
ok('I 覆寫後蘇最愛卡帶＋拍紙簿', GIFT_PREFS.npcs.so.favorites.indexOf('gift_cassette_indie') >= 0 && GIFT_PREFS.npcs.so.favorites.indexOf('gift_memo_pad') >= 0);
ok('I 覆寫後蘇 dislike 香水＋雜誌', GIFT_PREFS.npcs.so.dislikes.indexOf('gift_perfume_sample') >= 0 && GIFT_PREFS.npcs.so.dislikes.indexOf('gift_fashion_mag') >= 0);
ok('I 覆寫後 byKey 最愛句行 :liked（唔係死 :favorite）', !!GIFT_REACT.byKey['hiu:gift_pineapple_bun_set:liked'] && !GIFT_REACT.byKey['hiu:gift_pineapple_bun_set:favorite']);
ok('I 覆寫後 byKey 有葉香水 dislike 句（花瓶）', (GIFT_REACT.byKey['yip:gift_perfume_sample:dislike'] || { lines: [] }).lines.join('').indexOf('花瓶') >= 0);
ok('I 覆寫後 byKey 有蘇香水 dislike 句（玉女海報）', (GIFT_REACT.byKey['so:gift_perfume_sample:dislike'] || { lines: [] }).lines.join('').indexOf('玉女海報') >= 0);
ok('I 覆寫第二次冪等（唔重複）', env.rom159ApplyGiftOverrides() === false && GIFT_REACT.entries.length === 22);
resetS();
ok('I 撞到計數＋3 次封頂', (() => {
  env.rom159RecordTalk('colleague'); env.rom159RecordTalk('colleague');
  if (env.rom159TalkCapped('colleague', null)) return false;
  env.rom159RecordTalk('colleague');
  return env.rom159TalkCapped('colleague', null) === true;
})());
ok('I 交換電話一次有效', (() => {
  if (!env.rom159PhoneExchange('hiu')) return false;
  if (!env.rom159HasPhone('hiu')) return false;
  return env.rom159PhoneExchange('hiu') === false;
})());

/* ---- J. 蘇層級閘 ---- */
resetS();
playerTier = 0;
ok('J tier 0：閘閂', env.rom159SoMeetGate() === false);
playerTier = 1;
ok('J tier 1：閘開', env.rom159SoMeetGate() === true);
playerTier = 2;
ok('J tier 2：閘開', env.rom159SoMeetGate() === true);
resetS();
playerTier = 0;
ok('J tier 0：rom176BeatOpen(so) 唔當有開 beat', env.rom176BeatOpen('so') === false);
playerTier = 1;
ok('J tier 1：rom176BeatOpen(so) 有開 beat', env.rom176BeatOpen('so') === true);
resetS();
playerTier = 0;
ok('J tier 0：rom176BeatOpen(yip) 唔使閘', env.rom176BeatOpen('yip') === true);
resetS();
playerTier = 0;
const soMeet = { id: 'R_so_meet', when: '1989春', phase: 'P3',
  beats: [{ speaker: '旁白', lines: ['灣仔唱片大堂。'] }],
  choices: [
    { id: 'C_so_meet_warm', label: '擋住鏡頭', effects: { flags: ['flag_so_met_warm'], stats: { rel_so: 1 }, notes: '' } },
    { id: 'C_so_meet_cool', label: '行開', effects: { flags: ['flag_so_met_cool'], stats: { rel_so: 0 }, notes: '' } },
  ] };
const gateOut = env.rom159PrepareNode(soMeet);
ok('J tier 0：R_so_meet 換 gate 變體', gateOut && gateOut.id === 'R_so_meet_gate');
ok('J gate 變體有暗示句', gateOut && gateOut.beats.some(b => (b.lines || []).join('').indexOf('你而家仲係臨記') >= 0));
ok('J gate 變體單一抉擇', gateOut && gateOut.choices.length === 1 && gateOut.choices[0].id === 'C_so_gate_ok');
ok('J gate 抉擇寫 flag_so_gate_seen、rel 0', gateOut && gateOut.choices[0].effects.flags.indexOf('flag_so_gate_seen') >= 0 && gateOut.choices[0].effects.stats.rel_so === 0);
ok('J gate 變體唔係真 meet id', gateOut && gateOut.id !== 'R_so_meet');
ok('J gate 原節點唔郁', soMeet.choices.length === 2 && soMeet.id === 'R_so_meet');
resetS();
playerTier = 1;
ok('J tier 1：R_so_meet 照原文播（唔換）', env.rom159PrepareNode(soMeet) === null);

/* ---- K. Commit defs＋otherFlag null 安全 ---- */
ok('K CMT 有 lan／xu／yip／so，冇 vera', env.COMMIT48_DEFS.CMT_lan_commit && env.COMMIT48_DEFS.CMT_xu_commit && env.COMMIT48_DEFS.CMT_yip_commit && env.COMMIT48_DEFS.CMT_so_commit && !env.COMMIT48_DEFS.CMT_vera_commit);
ok('K CMT_lan 地點係錄音室', env.COMMIT48_DEFS.CMT_lan_commit.loc === 'rec_hk' && env.COMMIT48_DEFS.CMT_lan_commit.crisis === 'R_lan_crisis' && env.COMMIT48_DEFS.CMT_lan_commit.relKey === 'rel_lan');
ok('K CMT_xu 地點係中環', env.COMMIT48_DEFS.CMT_xu_commit.loc === 'ad_central' && env.COMMIT48_DEFS.CMT_xu_commit.crisis === 'R_xu_crisis');
ok('K CMT_yip 地點係選美後台', env.COMMIT48_DEFS.CMT_yip_commit.loc === 'tvb_kowloon' && env.COMMIT48_DEFS.CMT_yip_commit.crisis === 'R_yip_crisis');
ok('K CMT_so 地點係灣仔唱片', env.COMMIT48_DEFS.CMT_so_commit.loc === 'rec_wanchai' && env.COMMIT48_DEFS.CMT_so_commit.crisis === 'R_so_crisis');
ok('K 新 def otherFlag 係 null（排他鎖先係把關）', env.COMMIT48_DEFS.CMT_lan_commit.otherFlag === null && env.COMMIT48_DEFS.CMT_yip_commit.otherFlag === null && env.COMMIT48_DEFS.CMT_so_commit.otherFlag === null);
ok('K 新 def flag 係 commit 旗', env.COMMIT48_DEFS.CMT_lan_commit.flag === 'flag_lan_commit' && env.COMMIT48_DEFS.CMT_yip_commit.flag === 'flag_yip_commit' && env.COMMIT48_DEFS.CMT_so_commit.flag === 'flag_so_commit');
resetS();
ok('K choice47StoryFlag(null) 安全回 false', env.choice47StoryFlag(null) === false);
ok('K choice47StoryFlag(undefined) 安全回 false', env.choice47StoryFlag(undefined) === false);
S.story.flags = { flag_hiu_commit: true };
ok('K choice47StoryFlag 有旗回 true', env.choice47StoryFlag('flag_hiu_commit') === true);
ok('K choice47StoryFlag 無旗回 false', env.choice47StoryFlag('flag_so_commit') === false);

/* ---- L. ROM176 meet 節點表 ---- */
ok('L MEET_NODES 有 yip／so，冇 vera', JSON.stringify(env.ROM176_MEET_NODES.yip) === JSON.stringify(['R_yip_meet']) && JSON.stringify(env.ROM176_MEET_NODES.so) === JSON.stringify(['R_so_meet']) && !env.ROM176_MEET_NODES.vera);
ok('L MEET_NODES hiu／choi／lan／xu 不變', JSON.stringify(env.ROM176_MEET_NODES.hiu) === JSON.stringify(['R_hiu_meet']) && JSON.stringify(env.ROM176_MEET_NODES.lan) === JSON.stringify(['R_lan_meet']) && JSON.stringify(env.ROM176_MEET_NODES.xu) === JSON.stringify(['R_xu_meet']));

console.log('TOTAL PASS ' + pass + ' FAIL ' + fail);
if (fail) process.exit(1);
