// v20a99 VENUE99 邏輯測試：古典大樓場地化——金禧大酒店・大禮堂。
// (1) venue99ForCeremony：廣告／音樂／電影三大頒獎禮 → 金禧大酒店・大禮堂；
//     星河台慶頒獎夜 → 星河電視台（維持，同 C17 結局幕地點對齊）；未知 id → 空字串。
// (2) venue99ApplyOverlay 落喺真 content stub JSON 複本上：三大禮 inviteDek／press dek／
//     news line 改晒含場地；TV 嗰套逐字不變；朝早報紙每酒店媒介 win+nominee 各一款 dek
//     改（含場地），其餘模板（包括全部 TV）逐字不變；改動總數啱啱好（3+3+3+6）。
// (3) awards62CeremonyBeats 開場 beat：caption 帶場地行（pack 有 venue99 用 pack 值；
//     冇就按 ceremonyId 兜底）；gallery 短版 beats 結構不變。
// (4) 禁忌：所有 VENUE99 玩家面字串唔准含真酒店名／影射名。
// 反證：喺 v20a98 index 上行 → VENUE99 常量唔存在 → 抽取即 throw → FAIL。
// 用法：node tests/test_venue99_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const rootDir = path.dirname(htmlPath);
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
  let depth = 0, started = false;
  for(let k = i; k < html.length; k++){
    const ch = html[k];
    if(ch === '{' || ch === '['){ depth++; started = true; }
    else if(ch === '}' || ch === ']'){ depth--; if(started && depth === 0) return html.slice(i, k + 1) + ';'; }
    else if(ch === ';' && !started) return html.slice(i, k + 1);
  }
  throw new Error('const end not found: ' + name);
}

/* ---- 抽取 VENUE99 ---- */
for(const c of ['VENUE99_HOTEL', 'VENUE99_LINE', 'VENUE99_BY_CEREMONY', 'VENUE99_INVITE_DEK',
                'VENUE99_PRESS_DEK', 'VENUE99_NEWS_LINE', 'VENUE99_NP_DEK'])
  eval(extractConst(c).replace('const ' + c + ' =', 'var ' + c + ' ='));
eval(extractFn('venue99ForCeremony'));
eval(extractFn('venue99ApplyOverlay'));
eval(extractFn('awards62CeremonyBeats'));

/* ---- (1) 場地對照 ---- */
ok('酒店名＝金禧大酒店', VENUE99_HOTEL === '金禧大酒店');
ok('場地行＝金禧大酒店・大禮堂', VENUE99_LINE === '金禧大酒店・大禮堂');
ok('廣告賞 → 大禮堂', venue99ForCeremony('award_harbour_ad') === '金禧大酒店・大禮堂');
ok('金碟夜 → 大禮堂', venue99ForCeremony('award_golddisc_music') === '金禧大酒店・大禮堂');
ok('影藝獎 → 大禮堂', venue99ForCeremony('award_harbour_film') === '金禧大酒店・大禮堂');
ok('台慶頒獎夜 → 星河電視台（唔搬）', venue99ForCeremony('award_singho_tv') === '星河電視台');
ok('未知 id → 空字串', venue99ForCeremony('nope') === '' && venue99ForCeremony('') === '' && venue99ForCeremony(null) === '');

/* ---- (2) 覆寫落真 stub 複本 ---- */
const awardsStubRaw = JSON.parse(fs.readFileSync(path.join(rootDir, 'content', 'STUB_AWARDS_CEREMONY_v1.json'), 'utf8'));
const newsStubRaw = JSON.parse(fs.readFileSync(path.join(rootDir, 'content', 'STUB_NEWSPAPER_MORNING_SOFT_v1.json'), 'utf8'));
const FW = { awardsStub: JSON.parse(JSON.stringify(awardsStubRaw)), newspaperStub: JSON.parse(JSON.stringify(newsStubRaw)) };
venue99ApplyOverlay(FW);

const cer = id => FW.awardsStub.ceremonies.find(c => c.id === id);
const cer0 = id => awardsStubRaw.ceremonies.find(c => c.id === id);
['award_harbour_ad', 'award_golddisc_music', 'award_harbour_film'].forEach(id =>
  ok('inviteDek 含場地：' + id, cer(id).inviteDek.indexOf('金禧大酒店大禮堂舉行') >= 0));
ok('TV inviteDek 逐字不變', cer('award_singho_tv').inviteDek === cer0('award_singho_tv').inviteDek);
ok('TV inviteDek 冇酒店名', cer('award_singho_tv').inviteDek.indexOf('金禧') < 0);

const press = id => FW.awardsStub.pressTemplates.find(p => p.id === id);
const press0 = id => awardsStubRaw.pressTemplates.find(p => p.id === id);
['press_award_ad_01', 'press_award_music_01', 'press_award_film_01'].forEach(id =>
  ok('press dek 含場地：' + id, press(id).dek.indexOf('金禧大酒店') >= 0));
ok('TV press dek 逐字不變', press('press_award_tv_01').dek === press0('press_award_tv_01').dek);

const news = id => FW.awardsStub.newsTemplates.find(n => n.id === id);
const news0 = id => awardsStubRaw.newsTemplates.find(n => n.id === id);
['news_award_ad_01', 'news_award_music_01', 'news_award_film_01'].forEach(id =>
  ok('news line 含場地：' + id, news(id).line.indexOf('金禧大酒店') >= 0));
ok('TV news line 逐字不變', news('news_award_tv_01').line === news0('news_award_tv_01').line);

/* 朝早報紙模板：數改動總數（對原稿逐 id 比對） */
let npChanged = [];
['award_win', 'award_nominee'].forEach(b => {
  const before = {}; newsStubRaw.templates[b].forEach(t => before[t.id] = t.dek);
  FW.newspaperStub.templates[b].forEach(t => { if(t.dek !== before[t.id]) npChanged.push(t.id); });
});
ok('朝早報紙改動恰好 6 款', npChanged.length === 6);
ok('朝早報紙改動清單啱（film/music/ad 各 win+nominee 一款）',
   ['np_win_film_02', 'np_nom_film_01', 'np_win_music_02', 'np_nom_music_01', 'np_win_ad_02', 'np_nom_ad_01']
     .every(id => npChanged.indexOf(id) >= 0));
ok('朝早報紙改動款全含場地',
   npChanged.every(id => {
     const t = [...FW.newspaperStub.templates.award_win, ...FW.newspaperStub.templates.award_nominee].find(x => x.id === id);
     return t.dek.indexOf('金禧大酒店') >= 0;
   }));
ok('朝早報紙 TV 模板全不變', ['np_win_tv_01', 'np_win_tv_02', 'np_nom_tv_01'].every(id => {
  const a = [...FW.newspaperStub.templates.award_win, ...FW.newspaperStub.templates.award_nominee].find(x => x.id === id);
  const b = [...newsStubRaw.templates.award_win, ...newsStubRaw.templates.award_nominee].find(x => x.id === id);
  return a && b && a.dek === b.dek;
}));
/* stub 其餘欄位冇俾覆寫誤傷：displayName／分類文本原樣 */
ok('ceremony displayName 不變', FW.awardsStub.ceremonies.every(c => c.displayName === cer0(c.id).displayName));
ok('分類 winLine 不變', FW.awardsStub.categories.award_harbour_film[0].winLine === awardsStubRaw.categories.award_harbour_film[0].winLine);

/* ---- (3) 典禮 beats 開場 ---- */
const beatsFilm = awards62CeremonyBeats({ displayName: '維港影藝獎', bestOutcome: 'gallery', ceremonyId: 'award_harbour_film', venue99: '金禧大酒店・大禮堂', categories: [] });
ok('beats 開場含場地（pack 值）', beatsFilm[0].id === 'open' && beatsFilm[0].caption.indexOf('金禧大酒店・大禮堂') >= 0);
ok('beats 開場保留典禮名', beatsFilm[0].caption.indexOf('維港影藝獎') >= 0);
const beatsTv = awards62CeremonyBeats({ displayName: '星河台慶・年度頒獎夜', bestOutcome: 'gallery', ceremonyId: 'award_singho_tv', categories: [] });
ok('beats 開場 TV 按 ceremonyId 兜底＝星河電視台', beatsTv[0].caption.indexOf('星河電視台') >= 0 && beatsTv[0].caption.indexOf('金禧') < 0);
const beatsNone = awards62CeremonyBeats({ displayName: '頒獎夜', bestOutcome: 'gallery', ceremonyId: 'unknown_x', categories: [] });
ok('beats 開場未知典禮冇場地行', beatsNone[0].caption === '—— 頒獎夜 ——');
ok('gallery beats 新結構（v20a147：open/pan/names/suspense/reveal/out，約 9.6 秒）', beatsFilm.length === 6 && beatsFilm[1].id === 'pan' && beatsFilm[2].id === 'names' && beatsFilm[3].id === 'suspense' && beatsFilm[4].id === 'reveal' && beatsFilm[5].id === 'out');

/* ---- (4) 禁忌：真酒店名 ---- */
const FORBIDDEN = ['半島酒店', '文華東方', '文華酒店', '麗晶', '富麗華', '帝苑', '香格里拉', '凱悅', '喜來登',
                   '萬豪', '君悅', '港麗', '朗廷', '九龍酒店', '富豪酒店', '怡東酒店', '柏寧', '帝景酒店', '帝都酒店', '帝京酒店', '麗豪'];
const allVenueStrings = [VENUE99_HOTEL, VENUE99_LINE,
  ...Object.values(VENUE99_INVITE_DEK), ...Object.values(VENUE99_PRESS_DEK),
  ...Object.values(VENUE99_NEWS_LINE), ...Object.values(VENUE99_NP_DEK)].join('\n');
ok('VENUE99 玩家面字串零真酒店名', FORBIDDEN.every(n => allVenueStrings.indexOf(n) < 0));

console.log(fails.length ? ('FAILURES: ' + fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
