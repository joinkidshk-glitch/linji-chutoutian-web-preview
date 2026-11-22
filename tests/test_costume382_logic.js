// v20a382 COSTUME382 自備戲服通告・邏輯測試
// 合約（用戶 2026-11-22 拍板次序②；方案 GPT-6.2-sol）：
//   A 選取：只中級／高級／稀有（舊 中／高）＋ id 雜湊 %10==3，佔比少；
//     臨記／初級永遠唔標（保開局可接數）；entryTier／softBridge／引薦觸發／
//     人情渠道（武指／彭）／補位通告一律排除。
//   B 類別：按 genre／type 對應 12 件衫四類（日常／正式／舞台／戲行）。
//   C 門檻：未持有對應類別 → gate 拒絕＋書面語理由（指去花園街成衣店）；
//     持有 → 放行。唔改試鏡成功率公式（chance 唔喺本測試範圍，靜態釘另驗）。
//   D 呈現：短卡標籤「自備戲服 · 類別（未持有）」；詳情行持有／未持有兩態＋首次提示一次。
// 反證：v381 index 冇 costume382 函數 → 抽取即 throw → FAIL。
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
function extractConst(name){
  const i = html.indexOf('const ' + name + ' =');
  if (i < 0) throw new Error('const not found: ' + name);
  let depth = 0, started = false;
  for (let k = i; k < html.length; k++){
    const ch = html[k];
    if (ch === '{' || ch === '['){ depth++; started = true; }
    else if (ch === '}' || ch === ']'){ depth--; if (started && depth === 0) return html.slice(i, k + 1) + ';'; }
    else if (ch === ';' && !started) return html.slice(i, k + 1);
  }
  throw new Error('const end not found: ' + name);
}
let fails = 0;
function ok(name, cond, extra){
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : ''));
  if (!cond) fails++;
}

/* ---------- 沙盒 ---------- */
var S = { wardrobe: { owned: [], equipped: null }, flags: {} };
var isMakWuzhiGig158 = function(){ return false; };
var isPangCharityGig158 = function(){ return false; };
var triggerGigLabel229 = function(){ return ""; };
var intel381Label = function(){ return ""; };
eval([
  extractConst('COSTUME265'),
  extractFn('costume265ById'),
  extractFn('costume265EnsureWardrobe'),
  extractFn('costume382Hash'),
  extractFn('costume382GigReq'),
  extractFn('costume382OwnedCat'),
  extractFn('costume382Gate'),
  extractFn('costume382PillHtml'),
  extractFn('costume382DetailRowHtml'),
].join('\n'));

const gigs = JSON.parse(fs.readFileSync(path.join(ROOT, 'content/gigs_new.json'), 'utf8')).gigs;
ok('gig pool 330', gigs.length === 330, 'n=' + gigs.length);

const tagged = gigs.filter(g => costume382GigReq(g));
ok('tagged share small (5..40)', tagged.length >= 5 && tagged.length <= 40, 'n=' + tagged.length);
ok('no 臨記/初級 tagged', tagged.every(g => ['中級','高級','稀有','中','高'].includes(g.tier)));
ok('no entry/bridge tagged', tagged.every(g => !g.entryTier && !g.softBridge));
const cats = {};
for (const g of tagged) cats[costume382GigReq(g)] = (cats[costume382GigReq(g)] || 0) + 1;
ok('all cats valid', Object.keys(cats).every(c => ['日常','正式','舞台','戲行'].includes(c)), JSON.stringify(cats));

/* 類別映射抽樣：用合成 gig 逐 genre 驗（雜湊要命中 %10==3，先搵 id） */
function findId(){
  for (let i = 0; i < 10000; i++){ const id = 'test382_' + i; if (costume382Hash(id) % 10 === 3) return id; }
  return null;
}
const tid = findId();
ok('hash id found', !!tid, tid);
const mk = (genre, type) => ({ id: tid, tier: '中級', genre, type });
ok('武俠→戲行', costume382GigReq(mk('武俠','電影')) === '戲行');
ok('動作→戲行', costume382GigReq(mk('動作','電影')) === '戲行');
ok('情歌→舞台', costume382GigReq(mk('情歌','唱片通告')) === '舞台');
ok('晚會→舞台', costume382GigReq(mk('晚會','綜藝')) === '舞台');
ok('平面廣告→正式', costume382GigReq(mk('平面廣告','廣告')) === '正式');
ok('時裝處境→日常', costume382GigReq(mk('時裝處境','電視劇')) === '日常');
ok('初級唔標', costume382GigReq({ id: tid, tier: '初級', genre: '武俠', type: '電影' }) === null);
ok('臨記唔標', costume382GigReq({ id: tid, tier: '臨記', genre: '武俠', type: '電影' }) === null);

/* 門檻 */
const g0 = mk('武俠', '電影');
S.wardrobe.owned = [];
const gate1 = costume382Gate(g0);
ok('未持有被擋', !!gate1 && gate1.ok === false);
ok('理由書面語指去成衣店', !!gate1 && gate1.reason.includes('自備戲服') && gate1.reason.includes('花園街成衣店'), gate1 && gate1.reason);
S.wardrobe.owned = ['c10']; /* 武師練功服＝戲行 */
ok('持有戲行放行', costume382Gate(g0) === null);
S.wardrobe.owned = ['c1']; /* 日常，唔啱類 */
ok('持有錯類照擋', !!costume382Gate(g0));
S.wardrobe.owned = [];

/* 呈現 */
const pill = costume382PillHtml(g0);
ok('短卡標籤未持有', pill.includes('自備戲服 · 戲行（未持有）'), pill);
S.wardrobe.owned = ['c10'];
ok('短卡標籤已持有無尾', costume382PillHtml(g0).includes('自備戲服 · 戲行') && !costume382PillHtml(g0).includes('未持有'));
S.wardrobe.owned = [];
delete S.flags.costume382Seen;
const row1 = costume382DetailRowHtml(g0);
ok('詳情未持有行＋引導＋首次提示', row1.includes('戲行類服裝（未持有）') && row1.includes('花園街成衣店') && row1.includes('部分通告需要自備戲服'), row1.slice(0, 120));
const row2 = costume382DetailRowHtml(g0);
ok('首次提示只出一次', !row2.includes('部分通告需要自備戲服'));
S.wardrobe.owned = ['c11']; /* 民初長衫＝戲行 */
ok('詳情已持有行', costume382DetailRowHtml(g0).includes('戲行類服裝（已持有）'));

console.log(fails ? ('TOTAL FAIL ' + fails) : 'TOTAL PASS');
process.exit(fails ? 1 : 0);
