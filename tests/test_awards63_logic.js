// v20a63 頒獎禮群星版・邏輯測試（v20a229 B3 新庫版；v20a252 D-v2-2／D-v2-3 cast 模型重寫）：
// (1) fellows 衍生：只讀嗰年嗰格新庫通告嘅真陣容——電影／電視／廣告讀 cast 四角、
//     唱片讀 singer、新人獎讀 singer（混合）、最佳司儀讀 host；按片酬序、每星一部、
//     唔用冇 sprite 嘅主演（程天諾唔入 POSTER59_STAR_IDS）；彭少祺 sprite 已接線，
//     唔再排除。D-12 之前 poster59Path 一律回空，fellows 全部 poster:''。
// (2) 玩家自己殺青過嘅作品唔會變對手；年份係顯示年，唔再 +2。
// (3) 唔夠 3 個唔兜底（D-v2-2）：池抽（AWARDS63_POOL＋AWARDS63_TIER_WEIGHT＋
//     awards63WeightedPick）同高俊傑特別名額（v20a178）一併刪除，唔留 dormant——
//     候選唔夠 3 個就回少過 3 個，assigned 永遠 false；格分流由 catId 經
//     awards63CatSlot 決定（leadM／leadF／supportM／supportF／singer／newcomer／host）。
// (4) beats：入圍揭曉唱出得主星名＋作品；得獎＋有海報先有 glamour beat——D-12 之前冇海報，
//     得獎一律冇 glamour、全長約 11.5 秒（v20a160-m4：加 walkup 2200ms）；入圍落選有
//     comfort 安慰 beat（v20a147，reveal 之後、out 之前）；旁聽行埋宣佈弧約 9.6 秒，
//     唱名／揭曉唔寫阿偉（v20a147）。
// (5) focus cat 揀啱（won 優先 won cat、nominated 揀 nominated cat）。
// (6) 確定性：同一輸入兩次呼叫結果一致；舊 signature（唔傳 gender／catId）＝傳 ""；
//     每星只取一部（片酬最高嗰部）。
// 反證：對 v20a62 index 行 → AWARDS63 函數唔存在 → FAIL。
// 用法：node tests/test_awards63_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
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

/* ---- 世界：新庫 276 張經真 normalize；真 leadStar59Of／poster59Path／work59WorkOf ---- */
const tfA = html.indexOf('/* ==== v20a55 TEXTFIX');
const tfB = html.indexOf('async function refreshCopyPacksFromDisk(){');
if(tfA < 0 || tfB <= tfA){ console.log('FAIL TEXTFIX55 block not found'); process.exit(1); }
const TF_SRC = html.slice(tfA, tfB);
for(const c of ['POSTER59_STAR_IDS','AWARDS188_CATEGORIES','AWARDS204_FEMALE_STARS','EMOJI_ICON112'])
  eval(extractConst(c).replace('const '+c+' =', 'var '+c+' ='));
eval(extractConst('GIG_REQ_KEYS88').replace('const GIG_REQ_KEYS88 =', 'var GIG_REQ_KEYS88 ='));
for(const f of ['normalizeGigRecord','bridge56NormalizeGig','boardNotePlayerOk','looksLikeEraId','humanizeEraId','dur90CalibrateGig',
  'leadStar59Of','poster59Path','work59WorkOf','awards63StarName','awards63AllGigs','awards63GigYear','awards63GigPay',
  'awards63CatSlot','awards63HasSprite','awards63Fellows','awards63FocusCat','awards62CeremonyBeats',
  'awards204StarGender','iconHtml112'])
  eval(TF_SRC + '\n' + extractFn(f));

const packNew = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'content', 'gigs_new.json'), 'utf8'));
var GIGS = packNew.gigs.map(g => normalizeGigRecord(JSON.parse(JSON.stringify(g))));
var S = { wrapHistory: [] };
var STORY_WIRE = { gigsByYear: { 1990: null, 1991: null, 1992: null } };

const CER_FILM = { id:'award_harbour_film', medium:'film', matchTypes:['電影'] };
const CER_TV   = { id:'award_singho_tv',    medium:'tv',   matchTypes:['電視劇','綜藝'] };
const CER_AD   = { id:'award_harbour_ad',   medium:'ad',   matchTypes:['廣告'] };
const CER_MUS  = { id:'award_golddisc_music', medium:'music', matchTypes:['唱片通告'] };

/* ---- (1) 真陣容衍生（新庫實數，cast／singer／host） ---- */
S.wrapHistory = [];
let fl = awards63Fellows(CER_FILM, 1990);
ok('1990 電影 fellows 有 3 位', fl.length === 3);
ok('按片酬序：廖炳星《笑匠出山》居首', fl[0] && fl[0].star === '廖炳星' && fl[0].title === '笑匠出山' && fl[0].starId === 'liu_bingxing' && fl[0].gigId === 'gig_1990_film_109');
ok('廖炳星只出現一次（每星一部，取最高 pay 嗰部）', fl.filter(f=>f.star==='廖炳星').length === 1);
ok('第三位係麥震東《鐵血拳手》', fl[2] && fl[2].star === '麥震東' && fl[2].title === '鐵血拳手' && fl[2].gigId === 'gig_1990_film_103');
ok('fellows assigned 一律 false（冇第二輪，唔再有 assigned=true）', fl.every(f=>f.assigned === false));
ok('D-12 之前 fellows 全部冇海報（poster59Path 回空）', fl.every(f=>f.poster === ''));

let flAd = awards63Fellows(CER_AD, 1990);
ok('廣告 fellows：彭少祺 sprite 已接線，唔再排除（《守望相助》居首）',
  flAd.length === 3 && flAd[0].star === '彭少祺' && flAd[0].title === '守望相助' && flAd[0].gigId === 'gig_1990_ad_108' && flAd.every(f=>f.starId));

let flTv = awards63Fellows(CER_TV, 1990);
ok('電視 fellows：陸柏言＋麥震東＋齊鎮海', flTv.length === 3 && flTv[0].star === '陸柏言' && flTv[0].title === '兄弟有義氣' && flTv[1].star === '麥震東' && flTv[1].title === '雷霆幹探' && flTv[2].star === '齊鎮海' && flTv[2].title === '劍嘯山河');

/* ---- (2) 自己作品唔做對手＋年份隔離 ---- */
S.wrapHistory = [{ gigId:'gig_1990_film_109' }];
fl = awards63Fellows(CER_FILM, 1990);
ok('玩家殺青過嘅《笑匠出山》唔做對手', !fl.some(f=>f.title==='笑匠出山') && fl[0] && fl[0].star === '陸柏言');
S.wrapHistory = [];
const fl91 = awards63Fellows(CER_FILM, 1991);
ok('1991 fellows 只用 1991 作品（id 內嵌年份已係顯示年，唔再 +2）',
  fl91.length === 3 && fl91.every(f=>/^gig_1991_/.test(f.gigId)) &&
  fl91[0].star === '魏詠男' && fl91[0].title === '劍嘯長空' &&
  fl91[1].star === '陸柏言' && fl91[1].title === '江河歲月' &&
  fl91[2].star === '廖炳星' && fl91[2].title === '笑住過肥年・外傳');
ok('任何 fellows 都唔會係程天諾（唔入 POSTER59_STAR_IDS，冇 sprite）',
  fl.concat(fl91, flTv, flAd).every(f=>f.star !== '程天諾' && f.starId !== 'ching_tinlok'));

/* ---- (3) 格分流由 catId 決定＋唔夠 3 個唔兜底 ---- */
const flLeadF = awards63Fellows(CER_FILM, 1990, 'f', 'cat_film_lead_f');
ok('女主角格：只出女星（鍾楚凝＋胡美琳＋魏詠男）', flLeadF.length === 3 &&
  flLeadF[0].star === '鍾楚凝' && flLeadF[1].star === '胡美琳' && flLeadF[2].star === '魏詠男' &&
  flLeadF.every(f=>awards204StarGender(f.starId) === 'f'));
const flLeadM = awards63Fellows(CER_FILM, 1990, 'm', 'cat_film_lead_m');
ok('男主角格：只出男星（廖炳星＋陸柏言＋麥震東）', flLeadM.length === 3 &&
  flLeadM[0].star === '廖炳星' && flLeadM[1].star === '陸柏言' && flLeadM[2].star === '麥震東');
const flSupM = awards63Fellows(CER_FILM, 1990, 'm', 'cat_film_support_m');
const flSupF = awards63Fellows(CER_FILM, 1990, 'f', 'cat_film_support_f');
ok('配角格讀 support 角（男：陸柏言＋麥震東＋齊鎮海；女：韓秀婷＋魏詠男＋鍾楚凝）',
  flSupM.length === 3 && flSupM[0].star === '陸柏言' && flSupM[1].star === '麥震東' && flSupM[2].star === '齊鎮海' &&
  flSupF.length === 3 && flSupF[0].star === '韓秀婷' && flSupF[1].star === '魏詠男' && flSupF[2].star === '鍾楚凝');
ok('主角格同配角格唔同人（格分流，唔係同一份名單）',
  JSON.stringify(flLeadM.map(f=>f.starId)) !== JSON.stringify(flSupM.map(f=>f.starId)));
const flHost = awards63Fellows(CER_TV, 1990, '', 'cat_tv_host');
ok('最佳司儀格讀 host（陸柏言＋彭少祺＋顧明輝，中性唔分性別）', flHost.length === 3 &&
  flHost[0].star === '陸柏言' && flHost[0].title === '台慶大匯演' &&
  flHost[1].star === '彭少祺' && flHost[2].star === '顧明輝');
const flSingF = awards63Fellows(CER_MUS, 1990, 'f', 'cat_music_singer_f');
ok('女歌手格讀 singer＋singerGender（沈映雪＋韓秀婷＋藍若曦）', flSingF.length === 3 &&
  flSingF[0].star === '沈映雪' && flSingF[1].star === '韓秀婷' && flSingF[2].star === '藍若曦' &&
  flSingF.every(f=>awards204StarGender(f.starId) === 'f'));
const flSingM = awards63Fellows(CER_MUS, 1990, 'm', 'cat_music_singer_m');
ok('男歌手格讀 singer（顧明輝＋駱家聲＋陸柏言）', flSingM.length === 3 &&
  flSingM[0].star === '顧明輝' && flSingM[1].star === '駱家聲' && flSingM[2].star === '陸柏言');
const flNew = awards63Fellows(CER_MUS, 1990, '', 'cat_music_newcomer');
ok('新人獎讀 singer 混合（男女齊）', flNew.length === 3 &&
  flNew.some(f=>awards204StarGender(f.starId) === 'f') && flNew.some(f=>awards204StarGender(f.starId) === 'm'));
/* 唔夠 3 個唔兜底：受限世界得 2 張候選作品 → 回 2 個，唔填數 */
const savedGigs = GIGS;
GIGS = packNew.gigs.filter(g=>g.id === 'gig_1990_film_109' || g.id === 'gig_1990_film_110')
  .map(g=>normalizeGigRecord(JSON.parse(JSON.stringify(g))));
const flShort = awards63Fellows(CER_FILM, 1990, 'm', 'cat_film_lead_m');
ok('唔夠 3 個唔兜底（得 2 張候選 → 回 2 個，唔填池星）', flShort.length === 2 &&
  flShort[0].star === '廖炳星' && flShort[1].star === '陸柏言' && flShort.every(f=>f.assigned === false));
GIGS = [];
ok('零候選 → fellows=[]，唔 crash', Array.isArray(awards63Fellows(CER_FILM, 1990)) && awards63Fellows(CER_FILM, 1990).length === 0);
GIGS = savedGigs;
const fellowsSrc = extractFn('awards63Fellows');
ok('fellows 唔用池抽／權重／seeded draw／高俊傑名額（D-v2-2，唔留 dormant）',
  fellowsSrc.indexOf('AWARDS63_POOL') < 0 && fellowsSrc.indexOf('AWARDS63_TIER_WEIGHT') < 0 &&
  fellowsSrc.indexOf('awards63WeightedPick') < 0 && fellowsSrc.indexOf('awards63SeededRng') < 0 &&
  fellowsSrc.indexOf('Math.random') < 0 && fellowsSrc.indexOf('ko_chunkit') < 0);
ok('AWARDS63_POOL／AWARDS63_TIER_WEIGHT／awards63WeightedPick 已刪（全檔零殘留）',
  html.indexOf('const AWARDS63_POOL') < 0 && html.indexOf('const AWARDS63_TIER_WEIGHT') < 0 &&
  html.indexOf('function awards63WeightedPick(') < 0);

/* ---- (5) focus cat ---- */
const packMix = { bestOutcome:'nominated', categories:[
  { id:'a', outcome:'gallery' }, { id:'b', outcome:'nominated' }, { id:'c', outcome:'nominated' } ] };
ok('focus：nominated 揀第一個 nominated cat', awards63FocusCat(packMix).id === 'b');
const packWon = { bestOutcome:'won', categories:[ { id:'a', outcome:'nominated' }, { id:'b', outcome:'won' } ] };
ok('focus：won 揀 won cat', awards63FocusCat(packWon).id === 'b');

/* ---- (4) beats ---- */
const felLuk = { starId:'luk_baakyin', star:'陸柏言', title:'賀歲喜劇笑滿堂', gigId:'gig_1990_tv_101', poster:'', assigned:false };
const packNom = { displayName:'星河電視獎', bestOutcome:'nominated', repWork62:'飛天劍影決雌雄', repGigId63:'gig_1990_tv_101',
  categories:[{ label:'最佳男主角', outcome:'nominated', repWorkTitle:'飛天劍影決雌雄', fellows63:[felLuk], winner63:felLuk }] };
const beatsNom = awards62CeremonyBeats(packNom);
const revealNom = beatsNom.find(b=>b.id==='reveal');
ok('入圍揭曉 caption 唱出得主星名＋作品', !!revealNom && /陸柏言/.test(revealNom.caption) && /《賀歲喜劇笑滿堂》/.test(revealNom.caption));
ok('入圍揭曉 caption 提玩家代表作', !!revealNom && /《飛天劍影決雌雄》/.test(revealNom.caption));
const namesNom = beatsNom.find(b=>b.id==='names');
ok('唱名 lines 有齊玩家＋對手', !!namesNom && namesNom.lines.some(l=>/阿偉/.test(l)) && namesNom.lines.some(l=>/陸柏言/.test(l)));
ok('入圍冇 glamour beat（得獎先有）', !beatsNom.some(b=>b.id==='glamour'));

const packWonTop = { displayName:'維港影藝獎', bestOutcome:'won', repWork62:'雪山劍客', repGigId63:'gig_1990_film_112',
  categories:[{ label:'最佳電影', outcome:'won', repWorkTitle:'雪山劍客', fellows63:[], winner63:null }] };
const beatsWT = awards62CeremonyBeats(packWonTop);
const totalWT = beatsWT.reduce((a,b)=>a+b.ms,0);
ok('得獎＋D-12 之前冇海報 → 冇 glamour、全長約 11.5 秒（walkup 2200ms，9350＋2200＝11550）', !beatsWT.some(b=>b.id==='glamour') && totalWT >= 11000 && totalWT <= 12000);
ok('得獎＋冇海報都有 walkup beat（reveal 之後）', !!beatsWT.find(b=>b.id==='walkup') && beatsWT.find(b=>b.id==='walkup').ms === 2200);

const packWonNoPoster = { displayName:'維港影藝獎', bestOutcome:'won', repWork62:'大排檔笑話', repGigId63:'gig_1990_film_101',
  categories:[{ label:'最佳電影', outcome:'won', repWorkTitle:'大排檔笑話', fellows63:[], winner63:null }] };
const beatsWN = awards62CeremonyBeats(packWonNoPoster);
const totalWN = beatsWN.reduce((a,b)=>a+b.ms,0);
ok('得獎＋另一部作品都係冇 glamour、全長約 11.5 秒', !beatsWN.some(b=>b.id==='glamour') && totalWN >= 11000 && totalWN <= 12000);

const beatsGal = awards62CeremonyBeats({ displayName:'海港廣告獎', bestOutcome:'gallery', categories:[] });
const totalGal = beatsGal.reduce((a,b)=>a+b.ms,0);
ok('旁聽：行埋宣佈弧（有 names/suspense/reveal），約 9.6 秒', totalGal >= 9000 && totalGal <= 10000 && ['open','pan','names','suspense','reveal','out'].every(id=>beatsGal.some(b=>b.id===id)));
ok('旁聽唱名唔列阿偉（冇 fellows 嗰陣用通用行）', !!(beatsGal.find(b=>b.id==='names')) && !beatsGal.find(b=>b.id==='names').lines.some(l=>/阿偉/.test(l)));
ok('旁聽揭曉唔寫阿偉入圍／得獎', !!(beatsGal.find(b=>b.id==='reveal')) && !/阿偉/.test(beatsGal.find(b=>b.id==='reveal').caption));
ok('旁聽冇 comfort beat（只限入圍落選）', !beatsGal.some(b=>b.id==='comfort'));
const packGalF = { displayName:'海港廣告獎', bestOutcome:'gallery', repWork62:'', categories:[{ label:'最佳廣告', outcome:'gallery', repWorkTitle:'', fellows63:[felLuk], winner63:null }] };
const beatsGalF = awards62CeremonyBeats(packGalF);
ok('旁聽唱名只列對手（有 fellows 嗰陣）', !!(beatsGalF.find(b=>b.id==='names')) && beatsGalF.find(b=>b.id==='names').lines.some(l=>/陸柏言/.test(l)) && !beatsGalF.find(b=>b.id==='names').lines.some(l=>/阿偉/.test(l)));
ok('旁聽揭曉唱出得主（fellows[0]）', !!(beatsGalF.find(b=>b.id==='reveal')) && /陸柏言/.test(beatsGalF.find(b=>b.id==='reveal').caption) && /《賀歲喜劇笑滿堂》/.test(beatsGalF.find(b=>b.id==='reveal').caption));

/* ---- (6) 確定性（冇 seeded draw，同一輸入同一結果） ---- */
const oldFilm = awards63Fellows(CER_FILM, 1990);
const oldFilmEmpty = awards63Fellows(CER_FILM, 1990, '');
ok('舊 signature（唔傳 gender）＝傳 ""（同一結果）', JSON.stringify(oldFilm) === JSON.stringify(oldFilmEmpty));
ok('舊 signature 兩次呼叫一致（確定性，唔靠 seed）', JSON.stringify(awards63Fellows(CER_FILM, 1991)) === JSON.stringify(awards63Fellows(CER_FILM, 1991)));
ok('同類別兩次呼叫一致（(gender, catId) 可重現）',
  JSON.stringify(awards63Fellows(CER_FILM, 1991, 'm', 'cat_film_lead_m')) === JSON.stringify(awards63Fellows(CER_FILM, 1991, 'm', 'cat_film_lead_m')));

console.log('');
console.log(fails.length ? ('FAILED: '+fails.length+' -> '+fails.join(' | ')) : 'ALL PASS');
process.exit(fails.length ? 1 : 0);
