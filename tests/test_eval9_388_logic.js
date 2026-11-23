// v20a388 第九輪補跑 P2 收尾・邏輯測試
// 合約：
//   A 腳燈圖層（W1 P2）：.awd62-stage 第二規則腳燈漸層列喺聚光燈之前（CSS 先列層畫上面，
//     腳燈唔再被不透明聚光燈遮蔽）；.16 透明度不變。
//   B 摺疊掣觸控（W2 P2）：.ux68-locked-toggle 有 min-height:44px。
//   C 預設填位唔跨限期（W3 P2）：lockShootsIntoDraft 只填限期內嘅格；限期喺本週內而
//     限期前非休息格唔夠，先覆寫限期前休息格（救援）；限期喺下週唔覆寫休息。
//   D 跨年殺青查全庫（W4 P2）：殺青結算四處查 gig 改用 grant229GigById（先當年後三年全庫）；
//     grant229GigById 喺當年庫搵唔到嗰陣查到跨年庫記錄。
// 反證：v387 index 腳燈列第二、locked-toggle 無 min-height、填位跨限期、結算淨查 GIGS → FAIL。
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
function extractFn(name){
  const i = html.indexOf('function ' + name + '(');
  if (i < 0) throw new Error('fn not found: ' + name);
  let depth = 0, j = html.indexOf('{', i);
  for (; j < html.length; j++){ if (html[j] === '{') depth++; else if (html[j] === '}'){ depth--; if (depth === 0) break; } }
  return html.slice(i, j + 1);
}
let fails = 0;
function ok(name, cond, extra){
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : ''));
  if (!cond) fails++;
}

/* ---------- A 腳燈圖層次序 ---------- */
const stageRule = html.slice(html.indexOf('.awd62-stage{overflow-x:hidden;'));
const footIdx = stageRule.indexOf('rgba(180,150,82,.16)');
const spotIdx = stageRule.indexOf('#2c2148');
ok('A 腳燈列喺聚光燈之前', footIdx >= 0 && spotIdx >= 0 && footIdx < spotIdx, 'foot=' + footIdx + ' spot=' + spotIdx);

/* ---------- B 摺疊掣 44px ---------- */
const togRule = html.slice(html.indexOf('.ux68-locked-toggle{'), html.indexOf('.ux68-locked-toggle{') + 400);
ok('B locked-toggle min-height 44px', /min-height:\s*44px/.test(togRule), togRule.slice(0, 120));

/* ---------- 沙盒（C/D） ---------- */
var S = { dayIndex: 100, shoots: [], flags: {} };
var shootRemain = (sh) => Math.max(0, (sh.totalDays || 0) - (sh.doneDays || 0));
var shootWeekdayOk = () => true;
var scrubStaleJobs = (d) => d;
var normalizeGigRecord = (g) => g;
var GIGS = [{ id: 'gig_1991_tv_001', title: '當年劇', type: '電視劇' }];
var STORY_WIRE = { gigsByYear: {
  1990: { gigs: [{ id: 'gig_1990_tv_113', title: '劍嘯山河', type: '電視劇', tier: '中級', roleScale: 'tv_lead', roleLabel: '男主角', category: '電視劇', workTitle: '劍嘯山河', year: 1990 }] },
  1991: { gigs: GIGS },
  1992: { gigs: [] },
} };
eval([
  extractFn('lockShootsIntoDraft'),
  extractFn('grant229GigById'),
].join('\n'));

/* ---------- C 填位唔跨限期 ---------- */
// dayIndex=100 → 本週週一曆日 98，格 0..6 ＝ 曆日 98..104
// C1：剩 2 日、限期曆日 100（週三）→ 只填格 0/1，格 3 之後唔填
S.shoots = [{ id: 'c1', totalDays: 2, doneDays: 0, deadlineDay: 100 }];
const dC1 = lockShootsIntoDraft(['scout_all','scout_all','scout_all','scout_all','scout_all','scout_all','scout_all']);
ok('C1 限期後格唔填', dC1.filter(x => x === 'shoot:c1').length === 2 && dC1[3] === 'scout_all' && dC1[6] === 'scout_all', dC1.join(','));
// C2：剩 3 日、限期 100、限期前得一格非休息 → 救援覆寫限期前休息格
S.shoots = [{ id: 'c2', totalDays: 3, doneDays: 0, deadlineDay: 100 }];
const dC2 = lockShootsIntoDraft(['rest','rest','scout_all','scout_all','scout_all','scout_all','scout_all']);
ok('C2 救援覆寫限期前休息', dC2.filter(x => x === 'shoot:c2').length === 3 && dC2[3] === 'scout_all', dC2.join(','));
// C3：限期喺下週（110）→ 唔覆寫休息，留待下週
S.shoots = [{ id: 'c3', totalDays: 3, doneDays: 0, deadlineDay: 110, daysLeft: 0 }];
const dC3 = lockShootsIntoDraft(['rest','rest','rest','rest','rest','rest','rest']);
ok('C3 下週限期唔覆寫休息', dC3.filter(x => x === 'shoot:c3').length === 0 && S.shoots[0].daysLeft === 3, dC3.join(','));
// C4：回歸——第六輪 C 場景（近限期先得位）
S.shoots = [
  { id: 'long', totalDays: 6, doneDays: 0, deadlineDay: 130 },
  { id: 'tail', totalDays: 1, doneDays: 0, deadlineDay: 102 },
];
const dC4 = lockShootsIntoDraft(['scout_all','scout_all','scout_all','scout_all','scout_all','scout_all','scout_all']);
ok('C4 尾日拍攝有位', dC4.includes('shoot:tail'), dC4.join(','));
ok('C4 長拍攝填其餘', dC4.filter(x => x === 'shoot:long').length === 6, dC4.join(','));
// C5：無 deadlineDay（舊檔）→ 行為不變
S.shoots = [{ id: 'c5', totalDays: 2, doneDays: 0 }];
const dC5 = lockShootsIntoDraft(['scout_all','scout_all','scout_all','scout_all','scout_all','scout_all','scout_all']);
ok('C5 無限期照舊填位', dC5.filter(x => x === 'shoot:c5').length === 2, dC5.join(','));

/* ---------- D 跨年查全庫 ---------- */
const gCross = grant229GigById('gig_1990_tv_113');
ok('D 跨年庫查到 1990 通告', !!gCross && gCross.id === 'gig_1990_tv_113' && gCross.roleScale === 'tv_lead', JSON.stringify(gCross));
const gCur = grant229GigById('gig_1991_tv_001');
ok('D 當年庫照查', !!gCur && gCur.id === 'gig_1991_tv_001');
ok('D 殺青結算四處改用全庫查', (html.match(/grant229GigById\(sh\.gigId\)/g) || []).length >= 4,
   'count=' + ((html.match(/grant229GigById\(sh\.gigId\)/g) || []).length));

console.log(fails ? ('TOTAL FAIL ' + fails) : 'TOTAL PASS');
process.exit(fails ? 1 : 0);
