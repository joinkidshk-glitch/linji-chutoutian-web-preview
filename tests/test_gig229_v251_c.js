/* v20a251 工人 C 載入模擬：GRANT229 34 鍵＋N9_a 防撞＋三筆債權 trigger＋淡香水結算＋GATE 對照。
   抽 index.html 內函數／常數入 VM 跑真 code（唔係靜態 grep）；story JSON 唔係本票範圍，
   但 settle tick 讀嘅三支旗（flag_rain_rescue／flag_standup_crew／flag_stunt_double）
   已由工人 A 寫入 JSON effects（見報告 §3）。 */
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
const pack = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'gigs_new.json'), 'utf8'));
const gigs = pack.gigs || [];
const gigById = id => gigs.find(g => g.id === id);
let fails = [];
function ok(name, cond, extra) { console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : '')); if (!cond) fails.push(name); }
function extractFn(name) {
  const i = html.indexOf('function ' + name + '(');
  if (i < 0) return null;
  let depth = 0, j = html.indexOf('{', i);
  for (; j < html.length; j++) { if (html[j] === '{') depth++; else if (html[j] === '}') { depth--; if (depth === 0) break; } }
  return html.slice(i, j + 1);
}
function extractConstVar(name) {
  const i = html.indexOf('const ' + name + ' =');
  if (i < 0) return null;
  let depth = 0, started = false;
  for (let k = i; k < html.length; k++) {
    const ch = html[k];
    if (ch === '{' || ch === '[') { depth++; started = true; }
    else if (ch === '}' || ch === ']') { depth--; if (started && depth === 0) return html.slice(i, k + 1).replace('const ' + name, 'var ' + name) + ';'; }
    else if (ch === ';' && !started) return html.slice(i, k + 1).replace('const ' + name, 'var ' + name);
  }
  return null;
}

/* ---------- 1. GRANT229 全表 ---------- */
eval(extractConstVar('GRANT229_CHOICE'));
const keys = Object.keys(GRANT229_CHOICE);
/* v20a253 統籌：GRANT229 34→44 鍵（C 組 10 鍵；N13_c 不派）。 */
ok('GRANT229 44 鍵', keys.length === 44, keys.length);
ok('GRANT229 無 wildcard', !keys.some(k => k.endsWith(':*')));
ok('GRANT229 全部 gigId 喺 287 張庫入面', keys.every(k => !!gigById(GRANT229_CHOICE[k].gigId)), keys.filter(k => !gigById(GRANT229_CHOICE[k].gigId)).join(','));
ok('GRANT229 N9_a 重用 103（廖炳星引薦 gig，舊 107）', GRANT229_CHOICE['N9:N9_a'].gigId === 'gig_1991_film_103');
ok('GRANT229 N5_a／N5_b 共享 tv_205', GRANT229_CHOICE['N5:N5_a'].gigId === 'gig_1990_tv_205' && GRANT229_CHOICE['N5:N5_b'].gigId === 'gig_1990_tv_205');
ok('GRANT229 17 個新 reason 全部非空（何生傳呼口吻）', ['N7:N7_a','N7:N7_b','N7:N7_c','N8:N8_a','N8:N8_b','N8:N8_c','N9:N9_a','N9:N9_b','N10:N10_a','N10:N10_b','N10:N10_c','N11:N11_a','N11:N11_b','N12:N12_a','N12:N12_b','N19:N19_a','N19:N19_b'].every(k => (GRANT229_CHOICE[k].reason || '').length > 10));
/* v20a253 C 組 10 鍵：N13_a tv_114／N13_b film_102／N14_a rec_111／N14_b rec_201／N14_c ad_109／N15_a ad_110／N15_b rec_202／N16_a film_113／N16_b film_104／N16_c ad_111；N13_c 不派。 */
ok('GRANT229 C 組 10 鍵對照', GRANT229_CHOICE['N13:N13_a'].gigId==='gig_1992_tv_114' && GRANT229_CHOICE['N13:N13_b'].gigId==='gig_1992_film_102' && GRANT229_CHOICE['N14:N14_a'].gigId==='gig_1992_rec_111' && GRANT229_CHOICE['N14:N14_b'].gigId==='gig_1992_rec_201' && GRANT229_CHOICE['N14:N14_c'].gigId==='gig_1992_ad_109' && GRANT229_CHOICE['N15:N15_a'].gigId==='gig_1992_ad_110' && GRANT229_CHOICE['N15:N15_b'].gigId==='gig_1992_rec_202' && GRANT229_CHOICE['N16:N16_a'].gigId==='gig_1992_film_113' && GRANT229_CHOICE['N16:N16_b'].gigId==='gig_1992_film_104' && GRANT229_CHOICE['N16:N16_c'].gigId==='gig_1992_ad_111');
ok('GRANT229 C 組 10 個 reason 全部非空', ['N13:N13_a','N13:N13_b','N14:N14_a','N14:N14_b','N14:N14_c','N15:N15_a','N15:N15_b','N16:N16_a','N16:N16_b','N16:N16_c'].every(k => (GRANT229_CHOICE[k].reason || '').length > 10));
ok('GRANT229 N13_c 不派', !('N13:N13_c' in GRANT229_CHOICE));

/* ---------- 2. 三筆債權 trigger gig 板面開關 ---------- */
var S = null;
var GIGS = gigs;
eval(extractConstVar('BR89_PATRON_OF_GIG'));
eval(extractFn('br89HasCredit'));
eval(extractFn('br89GigOn'));
eval(extractFn('triggerGigOn'));
function freshSCredits(ids) {
  S = { dayIndex: 500, flags: {}, mockCredits: ids.map(id => ({ id, debtor: 'x', title: 'x', line: 'x', status: '未收' })) };
}
const CRED_GIGS = { credit_c7_rain: 'gig_1991_tv_204', credit_c9_crew: 'gig_1991_film_108', credit_c15_stunt: 'gig_1992_film_203' };
for (const [cid, gid] of Object.entries(CRED_GIGS)) {
  freshSCredits([cid]);
  ok(`trigger ${gid} 持 ${cid} → 上板`, triggerGigOn(gigById(gid)) === true);
  freshSCredits([]);
  ok(`trigger ${gid} 無債權 → 唔上板`, triggerGigOn(gigById(gid)) === false);
  freshSCredits([cid]);
  S.mockCredits[0].redeemedBy = gid;
  ok(`trigger ${gid} 已兌現標記 → 落板`, triggerGigOn(gigById(gid)) === false);
}
ok('三筆債權 gig 全部唔喺 BR89_PATRON_OF_GIG（行通用 credit 規則）',
  Object.values(CRED_GIGS).every(gid => !(gid in BR89_PATRON_OF_GIG)));

/* ---------- 3. 授出端：settle tick 授債權＋淡香水結算 ---------- */
var StoryOC = {
  ensure() { if (!S.story) S.story = { flags: {} }; if (!S.story.flags) S.story.flags = {}; },
  getFlag(f) { return !!((S.story && S.story.flags) || {})[f]; },
  setFlag(f, v) { this.ensure(); S.story.flags[f] = !!v; }
};
var saveQ = function () {};
var toastCalls = [];
var toast = function (t, o) { toastCalls.push(t); };
var ensureFavorLedger = function () { return { counted: {} }; };
var favorLedgerNoteCredit = function () {};
var syncNotebookMirror = function () {};
eval(extractConstVar('STORY46_CREDIT_N7'));
eval(extractConstVar('STORY46_CREDIT_N10'));
eval(extractConstVar('STORY46_GIFT_ID'));
eval(extractFn('story46SettleTick'));
eval(extractConstVar('STORY48_CREDIT_N12'));
eval(extractConstVar('STORY48_CREDIT_N16'));
eval(extractFn('story48SettleTick'));
function freshS46(flags, inv) {
  S = { dayIndex: 500, flags: {}, mockCredits: [], inventory: inv || {}, story: { flags: flags || {} } };
}
freshS46({ flag_rain_rescue: true });
story46SettleTick();
ok('settle：flag_rain_rescue → credit_c7_rain 入帳', S.mockCredits.some(c => c.id === 'credit_c7_rain'));
freshS46({ flag_standup_crew: true });
story46SettleTick();
ok('settle：flag_standup_crew → credit_c9_crew 入帳', S.mockCredits.some(c => c.id === 'credit_c9_crew'));
freshS46({ flag_rain_rescue: true });
story46SettleTick(); story46SettleTick();
ok('settle：重複 tick 唔雙計債權', S.mockCredits.filter(c => c.id === 'credit_c7_rain').length === 1);
freshS46({ flag_miss_cover: true }, { gift_perfume_sample: 1 });
toastCalls = [];
story46SettleTick();
ok('淡香水：有試用裝 → 扣 1＋flag_miss_gift_prepared', (S.inventory.gift_perfume_sample || 0) === 0 && S.story.flags.flag_miss_gift_prepared === true, JSON.stringify(S.inventory));
ok('淡香水：有試用裝 → toast 送禮', toastCalls.some(t => t.indexOf('淡香水試用裝送咗畀葉敏芝') >= 0));
freshS46({ flag_miss_cover: true }, {});
story46SettleTick();
ok('淡香水：無試用裝 → flag_miss_gift_missed', S.story.flags.flag_miss_gift_missed === true && !S.story.flags.flag_miss_gift_prepared);
freshS46({ flag_miss_cover: true }, { gift_perfume_sample: 2 });
story46SettleTick(); story46SettleTick();
ok('淡香水：結算冪等（第二 tick 唔再扣）', S.inventory.gift_perfume_sample === 1);
S = { dayIndex: 500, flags: {}, mockCredits: [], story: { flags: { flag_stunt_double: true } } };
story48SettleTick();
ok('settle：flag_stunt_double → credit_c15_stunt 入帳', S.mockCredits.some(c => c.id === 'credit_c15_stunt'));

/* ---------- 4. 殺青鉤：br89OnGigComplete 只標 BR89 13 張 ---------- */
var BR89_GIGS = [];
eval(extractFn('br89OnGigComplete'));
S = { flags: {}, mockCredits: [{ id: 'credit_c7_rain', debtor: 'x', title: 'x', line: 'x', status: '未收' }] };
br89OnGigComplete('gig_1991_tv_204');
ok('殺青鉤：通用 credit gig 唔設 redeemedBy（現況缺口，見報告 §3）', !S.mockCredits[0].redeemedBy);
S.mockCredits = [{ id: 'credit_enc83_liu_patron', debtor: 'x', title: 'x', line: 'x', status: '未收' }];
br89OnGigComplete('gig_1992_film_103');
ok('殺青鉤：BR89 映射內 gig（film_103／1992）殺青 → redeemedBy 有標記', S.mockCredits[0].redeemedBy === 'gig_1992_film_103');
/* v20a254 修復：新庫廖優先 gig（film_103／1991《笑住過肥年・外傳》）已入 BR89 映射，
   殺青鉤會標記 credit_enc79_liu_priority 做已兌現——v252 缺口已補，唔再係缺口。 */
S.mockCredits = [{ id: 'credit_enc79_liu_priority', debtor: 'x', title: 'x', line: 'x', status: '未收' }];
br89OnGigComplete('gig_1991_film_103');
ok('殺青鉤：新庫廖優先 gig（film_103／1991）喺映射 → 有標記（v252 缺口已修）', S.mockCredits[0].redeemedBy === 'gig_1991_film_103');

/* ---------- 5. GATE 表靜態對照（D8 附錄 K4） ---------- */
eval(extractConstVar('STORY_GATE_3Y'));
const GATE_WANT = {
  N7: { needDone: ['N5'], creditGt: 20, yearMin: 1991, seasonIn: ['夏'] },
  N8: { needDone: ['N7'], yearMin: 1991, seasonIn: ['夏', '秋'] },
  N9: { needDone: ['N7'], fameGt: 28, tagAny: ['喜劇', 'comedy', '動作', 'action', 'tag_comedy', '喜劇細胞', 'tag_action', '身手好'], yearMin: 1991, seasonIn: ['秋'] },
  N10: { weekMin: 100, yearMin: 1991, seasonIn: ['冬'] }, // v372：加 weekMin 100 防年頭冬尾搶閘
  N11: { needDone: ['N10'], dualGt: 70, weekMin: 100, yearMin: 1991, seasonIn: ['冬'] }, // v372：同上
  N12: { needDone: ['N11'], yearMin: 1992, seasonIn: ['春', '夏'] }, // v20a393：刪動作標籤前置、窗口擴至春／夏
  N19: { needDone: ['N18'], weekMin: 61, yearMin: 1991, seasonIn: ['春'] },
};
for (const [id, want] of Object.entries(GATE_WANT)) {
  ok('GATE ' + id + ' 同 D8 附錄一致', JSON.stringify(STORY_GATE_3Y[id]) === JSON.stringify(want), JSON.stringify(STORY_GATE_3Y[id]));
}

console.log(fails.length ? ('\nFAILURES: ' + fails.length + ' :: ' + fails.join(' | ')) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
