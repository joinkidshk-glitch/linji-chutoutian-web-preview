// v416：未合要求改 span 整句不拆行，斷言跟新寫法。
// v416：店舖提示收去衣櫃頁首講一次，斷言跟新文案。
// v20a293 Q6：其餘 8 件衫入舖頭賣，達條件先買得——邏輯測試。
//   (1) 店列出 12 件（全數 shop:true；價錢總和 $6,270 不變，解鎖條件照表）；
//   (2) 鎖定條件逐個驗：開局（聲望 5／級數 0／歌藝 14／演技 18）c2 唔鎖，其餘 7 件各鎖
//       其門檻（fame／tier／vocal／acting），邊界值（差 1 鎖、啱數開）逐個核；
//   (3) 未達條件買唔到（ok:false＋「未合要求」＋錢／衣櫃唔郁）；達條件買到（扣錢＋入 owned）；
//   (4) 重複買唔到（「已經擁有」）、唔夠錢買唔到（錢唔郁）；
//   (5) 換衫加成只喺門檻嗰刻計：著衫後 S.* 七圍唔郁，costume265EffStat 先見到加成，
//       每圍上限 +4，除低即刻跌返；舊 4 件（c1／c4／c8／c10）行為不變。
// 衫圖：c2／c3／c5／c6／c7／c9／c11／c12 共 64 張未生成，呢票唔斷言檔案存在；
//   缺圖 fallback（dlg106Candidates 跌返 awi stem、enterHome #home-awi onerror 跌返
//   PORTRAITS.hero_awi）由 test_costume265_static.py §8 靜態覆蓋，見 NOTES_V20A293。
// 用法：node tests/test_r293_clothes_shop.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
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
    else if(c === ';' && !started){ j++; break; }
  }
  return html.slice(i, j);
}
const asVar = (code, name)=> code.replace('const ' + name + ' =', 'var ' + name + ' =');

/* ---- 沙盒：S＋級數 stub ---- */
var S;
var tierVar = 0;
function enc79PlayerTier(){ return tierVar; }
var STAT_LABEL = { acting:'演技', stage:'台風', vocal:'歌藝', looks:'外貌', charm:'魅力', stamina:'體能', iq:'智商' };
function freshS(o){
  S = Object.assign({ money: 1200, fame: 5, acting: 18, stage: 14, vocal: 14, looks: 22, charm: 16, stamina: 75, iq: 20, flags: { playerTierMax: 0 }, wardrobe: { owned: [], equipped: null } }, o || {});
  tierVar = (o && o._tier != null) ? o._tier : 0;
  return S;
}
eval(
  asVar(extractConst('COSTUME265'), 'COSTUME265') + '\n' +
  asVar(extractConst('COSTUME265_MAX_PER_STAT'), 'COSTUME265_MAX_PER_STAT') + '\n' +
  ['costume265ById','costume265EnsureWardrobe','costume265Tier','costume265UnlockReason',
   'costume265Unlocked','costume265EquippedDef','costume265BonusMap','costume265EffStat',
   'costume265BonusText','buyCostume265','costume265Equip'].map(extractFn).join('\n')
);
const shopRows = ()=> (COSTUME265 || []).filter(c=> c && c.shop);
const byId = id => costume265ById(id);

/* ---- (1) 店列出 12 件 ---- */
ok('店列出 12 件（全數 shop:true）', shopRows().length === 12
  && ['c1','c2','c3','c4','c5','c6','c7','c8','c9','c10','c11','c12'].every(id=> shopRows().some(c=> c.id === id)));
ok('12 件價錢總和 $6,270 不變', shopRows().reduce((a,c)=> a + (Number(c.price)||0), 0) === 6270);
ok('8 件新入店價錢／加成／解鎖照表（c2 $150／c3 $300／c5 $900／c6 $1500／c7 $250／c9 $800／c11 $400／c12 $600）',
  byId('c2').price === 150 && byId('c3').price === 300 && byId('c5').price === 900 && byId('c6').price === 1500
  && byId('c7').price === 250 && byId('c9').price === 800 && byId('c11').price === 400 && byId('c12').price === 600
  && JSON.stringify(byId('c6').unlock) === JSON.stringify({ tier: 2, fame: 40 })
  && JSON.stringify(byId('c11').unlock) === JSON.stringify({ acting: 35 }));

/* ---- (2) 鎖定條件：開局＋邊界 ---- */
freshS(); // 聲望 5／級數 0／歌藝 14／演技 18（開局七圍）
ok('開局：c2 無鎖（unlock null）', costume265UnlockReason(byId('c2')) === '');
ok('開局：c3 鎖聲望 ≥ 15', costume265UnlockReason(byId('c3')) === '聲望 ≥ 15');
ok('開局：c5 鎖級數 ≥ 配角（1 級）', costume265UnlockReason(byId('c5')) === '級數 ≥ 配角（1 級）');
ok('開局：c6 兩重鎖（聲望＋級數，fame 行先）', costume265UnlockReason(byId('c6')) === '聲望 ≥ 40＋級數 ≥ 主角（2 級）');
ok('開局：c7 鎖歌藝 ≥ 20', costume265UnlockReason(byId('c7')) === '歌藝 ≥ 20');
ok('開局：c9 鎖級數 ≥ 主角（2 級）', costume265UnlockReason(byId('c9')) === '級數 ≥ 主角（2 級）');
ok('開局：c11 鎖演技 ≥ 35', costume265UnlockReason(byId('c11')) === '演技 ≥ 35');
ok('開局：c12 鎖演技 ≥ 30', costume265UnlockReason(byId('c12')) === '演技 ≥ 30');
ok('邊界：c3 聲望 14 鎖、15 開', (()=>{ freshS({ fame: 14 }); const a = costume265UnlockReason(byId('c3')); freshS({ fame: 15 }); return a !== '' && costume265UnlockReason(byId('c3')) === ''; })());
ok('邊界：c7 歌藝 19 鎖、20 開', (()=>{ freshS({ vocal: 19 }); const a = costume265UnlockReason(byId('c7')); freshS({ vocal: 20 }); return a !== '' && costume265UnlockReason(byId('c7')) === ''; })());
ok('邊界：c12 演技 29 鎖、30 開；c11 演技 34 鎖、35 開', (()=>{ freshS({ acting: 29 }); const a = costume265UnlockReason(byId('c12')); freshS({ acting: 34 }); const b = costume265UnlockReason(byId('c11')); freshS({ acting: 35 }); return a !== '' && b !== '' && costume265UnlockReason(byId('c11')) === ''; })());
ok('邊界：c6 級數 2 但聲望 39 照鎖、40 開', (()=>{ freshS({ fame: 39, _tier: 2 }); const a = costume265UnlockReason(byId('c6')); freshS({ fame: 40, _tier: 2 }); return a !== '' && costume265UnlockReason(byId('c6')) === ''; })());
ok('級數用 max(即時, 最高紀錄)：即時 0 但 playerTierMax 2，c9 開', (()=>{ freshS({ flags: { playerTierMax: 2 } }); return costume265UnlockReason(byId('c9')) === ''; })());

/* ---- (3) 未達條件買唔到／達條件買到 ---- */
freshS();
let r = buyCostume265('c3');
ok('未達條件：c3 買唔到（ok:false＋「未合要求」）', r.ok === false && (r.reason || '').indexOf('未合要求') === 0);
ok('未達條件買唔到：錢／衣櫃唔郁', S.money === 1200 && S.wardrobe.owned.length === 0);
r = buyCostume265('c6');
ok('未達條件：c6（兩重鎖）買唔到', r.ok === false && (r.reason || '').indexOf('未合要求') === 0);
r = buyCostume265('c2');
ok('達條件：c2 買到（ok:true）', r.ok === true && r.name === '街坊波鞋套裝' && r.price === 150);
ok('達條件買到：扣錢 $1200→$1050＋入 owned', S.money === 1050 && S.wardrobe.owned.indexOf('c2') >= 0);

/* ---- (4) 重複買／唔夠錢 ---- */
r = buyCostume265('c2');
ok('重複買唔到（「已經擁有」＋錢唔郁）', r.ok === false && r.reason === '已經擁有' && S.money === 1050 && S.wardrobe.owned.length === 1);
freshS({ money: 100 });
r = buyCostume265('c2');
ok('唔夠錢買唔到（$100 買 $150，錢唔郁）', r.ok === false && S.money === 100 && S.wardrobe.owned.length === 0);

/* ---- (5) 逐件解鎖買到 ---- */
function buyUnlocked(id, setup, money){
  freshS(Object.assign({ money: money || 2000 }, setup || {}));
  const res = buyCostume265(id);
  return res.ok === true && S.wardrobe.owned.indexOf(id) >= 0 && S.money === (money || 2000) - byId(id).price;
}
ok('解鎖買到：c3（聲望 15）', buyUnlocked('c3', { fame: 15 }));
ok('解鎖買到：c5（級數 1）', buyUnlocked('c5', { _tier: 1 }));
ok('解鎖買到：c6（級數 2＋聲望 40）', buyUnlocked('c6', { _tier: 2, fame: 40 }));
ok('解鎖買到：c7（歌藝 20）', buyUnlocked('c7', { vocal: 20 }));
ok('解鎖買到：c9（級數 2）', buyUnlocked('c9', { _tier: 2 }));
ok('解鎖買到：c11（演技 35）', buyUnlocked('c11', { acting: 35 }));
ok('解鎖買到：c12（演技 30）', buyUnlocked('c12', { acting: 30 }));

/* ---- (6) 換衫加成只喺門檻嗰刻計 ---- */
freshS({ acting: 35, money: 2000 });
buyCostume265('c11');
ok('著衫前：S.acting 係底數 35，有效數值都係 35', S.acting === 35 && costume265EffStat('acting') === 35);
ok('著 c11：costume265Equip 成功', costume265Equip('c11') === true);
ok('著 c11：BonusMap acting+3／stage+1（單件 ≤ 上限 +4）', (()=>{ const b = costume265BonusMap(); return b.acting === 3 && b.stage === 1; })());
ok('著 c11：有效數值 acting 38／stage 15，但 S.acting／S.stage 唔郁', costume265EffStat('acting') === 38 && costume265EffStat('stage') === 15 && S.acting === 35 && S.stage === 14);
ok('著 c11：每圍有效加成 ≤ COSTUME265_MAX_PER_STAT（4）', Object.values(costume265BonusMap()).every(n=> n <= COSTUME265_MAX_PER_STAT));
ok('除低：BonusMap 清空，有效數值跌返底數', costume265Equip(null) === true && Object.keys(costume265BonusMap()).length === 0 && costume265EffStat('acting') === 35);
ok('未擁有著唔到', costume265Equip('c12') === false);
freshS({ money: 2000 });
ok('著 c6（looks+3／charm+3／stage+1）：有效數值各加，S.* 唔郁', (()=>{
  freshS({ money: 2000, _tier: 2, fame: 40 });
  buyCostume265('c6'); costume265Equip('c6');
  return costume265EffStat('looks') === 25 && costume265EffStat('charm') === 19 && costume265EffStat('stage') === 15
    && S.looks === 22 && S.charm === 16 && S.stage === 14;
})());

/* ---- (7) 舊 4 件行為不變 ---- */
freshS();
ok('舊 4 件仲有售（c1／c4／c8／c10 shop:true）', ['c1','c4','c8','c10'].every(id=> byId(id).shop === true));
ok('舊件鎖定照舊：開局 c4 鎖聲望 ≥ 25、c8 鎖歌藝 ≥ 25、c1／c10 唔鎖',
  costume265UnlockReason(byId('c4')) === '聲望 ≥ 25' && costume265UnlockReason(byId('c8')) === '歌藝 ≥ 25'
  && costume265UnlockReason(byId('c1')) === '' && costume265UnlockReason(byId('c10')) === '');
ok('舊件解鎖買到：c4（聲望 25）、c8（歌藝 25）', buyUnlocked('c4', { fame: 25 }) && buyUnlocked('c8', { vocal: 25 }));

/* ---- (8) 店面／衣櫃靜態接線 ---- */
const shopSrc = (()=>{
  const i = html.indexOf('function openClothingShop265(');
  let depth = 0, j = html.indexOf('{', i);
  for(; j < html.length; j++){ if(html[j] === '{') depth++; else if(html[j] === '}'){ depth--; if(depth === 0) break; } }
  return html.slice(i, j + 1);
})();
ok('店面：只列 shop:true（filter c.shop），12 件全出', shopSrc.indexOf('filter(c=>c && c.shop)') >= 0);
ok('店面：鎖住寫明要求＋顯示「鎖住」', shopSrc.indexOf('未合要求：') >= 0 && shopSrc.indexOf('"鎖住"') >= 0);
ok('店面：買前確認（confirmChoice236）＋行 buyCostume265', shopSrc.indexOf('confirmChoice236({') >= 0 && shopSrc.indexOf('buyCostume265(id)') >= 0);
ok('店面：已擁有顯示，唔可以重複買', shopSrc.indexOf('"已擁有"') >= 0);
ok('衣櫃：未擁有寫明去向（花園街成衣店有售）', html.indexOf('未購入嘅衫可以去花園街成衣店買') >= 0);

if(fails.length){ console.log('FAILURES: ' + fails.join(' | ')); process.exit(1); }
console.log('ALL PASS');
