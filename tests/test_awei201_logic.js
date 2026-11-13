// v20a201 s1 全身組重生邏輯測試：修 v199 review C1（s1 闊過 s2／s3 約 14–20%）。
// 抽 index.html 內 DLG108 模組切片 eval（同 test_awei199_logic.js 手法），
// fitApply 用手造 fake stage／img（唔使瀏覽器）。
// 覆蓋：(a) s1 8 張 AR 一律 ≈0.280（PIL 實量，見 static test），組內一致；
//       (b) painted 闊模型（box 高 × 真 AR，object-fit:contain）：932／700 兩個
//       viewport，逐個表情三 tier spread——base／sad／shy／surprise／think
//       ≤5px；serious／angry／smile 殘留 spread 係 s2／s3 本身 AR 分散造成
//       （s3 serious 0.3032、s2／s3 angry 0.3011、s3 smile 0.2907），
//       但修完 spread 不足修前一半（s1 唔再係離群值）；s1 vs s2 serious
//       闊度差由 35.5px 收窄到 0.3px（review  headline 數字）；
//       (c) 三 tier painted 高仍然 spread ≤1px（DLG199 唔郁，高度正規化無損）；
//       (d) 單人阿偉同高；非阿偉配對／身高比零影響；
//       (e) 反證：舊 s1 AR（0.335–0.345）嗰陣 serious／angry spread >14px，
//       證明呢個測試捉到 C1（唔係量度假象）。
// 數字來源：PIL 量度全庫 awi* AR（v201 後：s1 全部 0.2800–0.2801；
// s2／s3 見下面 AR 表）；box 高 932：635.4px、700：518.6px（v199 review 實駕）。
// 用法：node tests/test_awei201_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS ' : 'FAIL ') + name); }
function info(msg){ console.log('INFO ' + msg); }

// PIL 實量 AR（4 位小數）：s1 全部重生後 0.2800–0.2801；s2／s3 原封不動。
const ARS = {
  base:     { s1: 0.2800, s2: 0.2776, s3: 0.2779 },
  serious:  { s1: 0.2801, s2: 0.2797, s3: 0.3032 },
  angry:    { s1: 0.2801, s2: 0.3011, s3: 0.3011 },
  sad:      { s1: 0.2801, s2: 0.2839, s3: 0.2836 },
  shy:      { s1: 0.2801, s2: 0.2779, s3: 0.2764 },
  smile:    { s1: 0.2801, s2: 0.2864, s3: 0.2907 },
  surprise: { s1: 0.2801, s2: 0.2792, s3: 0.2767 },
  think:    { s1: 0.2801, s2: 0.2794, s3: 0.2773 },
};
// 舊 s1 AR（main 2c1a680 PIL 實量，反證用）
const OLD_S1 = { base: 0.3429, serious: 0.3356, angry: 0.3446, sad: 0.3351,
  shy: 0.3356, smile: 0.3354, surprise: 0.3360, think: 0.3355 };
const BOXH = { 932: 635.4, 700: 518.6 };
const widthAt = (boxH, ar)=> boxH * ar;
const spread = (xs)=> Math.max(...xs) - Math.min(...xs);

// ---- (a) s1 組內一致 ----
{
  const s1 = Object.values(ARS).map(r => r.s1);
  ok(`s1 8 張 AR 一律 ≈0.280（${Math.min(...s1).toFixed(4)}–${Math.max(...s1).toFixed(4)}）`,
     s1.every(a => Math.abs(a - 0.280) <= 0.004));
  ok(`s1 8 張 AR spread ≤0.001（組內一致）`, spread(s1) <= 0.001);
}

// ---- (b) 逐個表情三 tier painted 闊 ----
const PASS5 = ['base', 'sad', 'shy', 'surprise', 'think'];
const RESIDUAL = ['serious', 'angry', 'smile'];
for(const vp of [932, 700]){
  const boxH = BOXH[vp];
  for(const emo of Object.keys(ARS)){
    const ws = [ARS[emo].s1, ARS[emo].s2, ARS[emo].s3].map(a => widthAt(boxH, a));
    const sp = spread(ws);
    info(`  ${vp} ${emo}：闊 [${ws.map(w => w.toFixed(1)).join(', ')}] spread ${sp.toFixed(1)}px`);
    if(PASS5.includes(emo)){
      ok(`${vp} ${emo}：三 tier 同闊 spread ≤5px（實測 ${sp.toFixed(1)}px）`, sp <= 5.0);
    } else {
      // 殘留 spread 全部由 s2／s3 造成：修完 spread 不足修前一半
      const oldWs = [OLD_S1[emo], ARS[emo].s2, ARS[emo].s3].map(a => widthAt(boxH, a));
      const oldSp = spread(oldWs);
      ok(`${vp} ${emo}：殘留 spread ${sp.toFixed(1)}px 不足修前 ${oldSp.toFixed(1)}px 一半（s2／s3 AR 分散，唔係 s1）`,
         sp < oldSp * 0.5);
    }
  }
  // review headline：s1 vs s2 serious 由 35.5px → 0.3px
  const d = Math.abs(widthAt(boxH, ARS.serious.s1) - widthAt(boxH, ARS.serious.s2));
  ok(`${vp} serious：s1 vs s2 闊度差 ≤1px（實測 ${d.toFixed(1)}px，修前 35.5px）`, d <= 1.0);
  // s1 自身 8 個表情同一闊度（組內一致 → 唔會換表情嗰陣闊窄跳）
  const s1ws = Object.values(ARS).map(r => widthAt(boxH, r.s1));
  ok(`${vp} s1 8 個表情 painted 闊 spread ≤1px（${Math.min(...s1ws).toFixed(1)}–${Math.max(...s1ws).toFixed(1)}）`,
     spread(s1ws) <= 1.0);
}

// ---- (c)(d) DLG199 唔郁：高度正規化＋身高比＋單人（新 AR 表重跑 199 斷言） ----
const a = html.indexOf('/* ===== v20a108 DLG108');
const b = html.indexOf('/* ===== DLG108 模組完 ===== */');
ok('搵到 DLG108 模組', a >= 0 && b > a);
if (a < 0 || b <= a) { console.log('RESULT FAIL (no DLG108 module)'); process.exit(1); }
const code = html.slice(a, b);
global.window = {};
global.dlg109HeightScale = (id)=> id==='pang_siuki' ? 0.85 : (id==='gu_mingfai'||id==='ching_tinlok') ? 1.05 : 1.00;
let D = null, evalErr = null;
try {
  D = eval(code + '\n;({fitPct:dlg108FitPct, fitApply:dlg108FitApply, refAr:DLG199_AWEI_REF_AR, isAweiId:dlg199IsAweiId, fitAr:dlg199FitAr, pctCap:dlg199PctCap})');
} catch(e){ evalErr = e; }
ok('eval DLG108 模組切片（含 DLG199）', evalErr === null);
if (evalErr) { console.log('INFO eval 失敗：' + evalErr); console.log('RESULT FAIL (no DLG199)'); process.exit(1); }
ok('REF_AR 仍係 0.345（唔郁）', D.refAr === 0.345);
ok('fitAr：阿偉任何真 AR → 0.345', D.fitAr('awi', 0.28) === 0.345 && D.fitAr('awi_s2', 0.30) === 0.345);
ok('pctCap 468×1412 ≈ 46.1%', Math.abs(D.pctCap(468, 1412, 0.48) - 46.1) < 0.05);

function fakeImg(id, ar){
  const natH = 2000, natW = Math.round(ar * natH);
  return { naturalWidth: natW, naturalHeight: natH, _sid106: null,
    getAttribute: (k)=> k === 'data-dlg-id' ? id : null, style: {} };
}
function fakeStage(w, h, imgs, isEnc){
  return { clientWidth: w, clientHeight: h,
    classList: { contains: (c)=> !!isEnc && c === 'e79-stage' },
    style: { _props: {}, setProperty(k, v){ this._props[k] = v; } },
    querySelectorAll: ()=> imgs };
}
function painted(natW, natH, boxHpx, maxW){
  const ar = natW / natH;
  const ph = Math.min(boxHpx, maxW / ar);
  return { h: ph, w: ph * ar };
}
const SW = 468, SH = 1412, MAXW = 0.48 * SW;
const PARTNERS = { ho_sang: 0.3637, vera: 0.3821, fong_siulung: 0.4127,
  gu_mingfai: 0.2320, pang_siuki: 0.3760 };
function runPair(awiAr, partnerId, partnerAr){
  const imgs = [fakeImg('awi', awiAr), fakeImg(partnerId, partnerAr)];
  const st = fakeStage(SW, SH, imgs, false);
  if(!D.fitApply(st)) return null;
  const pct = parseFloat(st.style._props['--dlg108-char-h']);
  const boxH = pct / 100 * SH;
  return { pct, awi: painted(imgs[0].naturalWidth, imgs[0].naturalHeight, boxH, MAXW),
    partner: painted(imgs[1].naturalWidth, imgs[1].naturalHeight,
      pct / 100 * SH * global.dlg109HeightScale(partnerId), MAXW) };
}
// 24 個新 AR（8 表情 × 3 tier）全部同高
for(const [pid, par] of Object.entries(PARTNERS)){
  const hs = [];
  for(const emo of Object.keys(ARS))
    for(const t of ['s1', 's2', 's3'])
      hs.push(runPair(ARS[emo][t], pid, par).awi.h);
  ok(`配對 阿偉×${pid}：新 AR 表 24 格 painted 高 spread ≤1px（${Math.min(...hs).toFixed(1)}–${Math.max(...hs).toFixed(1)}）`,
     spread(hs) <= 1.0);
}
// 單人阿偉同高
{
  const hs = [];
  for(const emo of Object.keys(ARS))
    for(const t of ['s1', 's2', 's3']){
      const imgs = [fakeImg('awi', ARS[emo][t])];
      const st = fakeStage(SW, SH, imgs, false);
      D.fitApply(st);
      const pct = parseFloat(st.style._props['--dlg108-char-h']);
      hs.push(Math.min(pct / 100 * SH, MAXW / ARS[emo][t]));
    }
  ok(`單人阿偉：新 AR 表 24 格 painted 高 spread ≤1px（${Math.min(...hs).toFixed(1)}–${Math.max(...hs).toFixed(1)}）`,
     spread(hs) <= 1.0);
}
// 身高比零影響
{
  const r = runPair(ARS.base.s1, 'gu_mingfai', PARTNERS.gu_mingfai);
  ok(`顧明輝／阿偉 painted 比 ＝1.05（實測 ${(r.partner.h / r.awi.h).toFixed(3)}）`,
     Math.abs(r.partner.h / r.awi.h - 1.05) < 0.01);
  const r2 = runPair(ARS.base.s1, 'pang_siuki', PARTNERS.pang_siuki);
  ok(`彭少祺／阿偉 painted 比 ＝0.85（實測 ${(r2.partner.h / r2.awi.h).toFixed(3)}）`,
     Math.abs(r2.partner.h / r2.awi.h - 0.85) < 0.01);
}

// ---- (e) 反證：舊 s1 AR 嗰陣 spread 即刻超標 ----
{
  const boxH = BOXH[932];
  for(const emo of ['serious', 'angry']){
    const oldWs = [OLD_S1[emo], ARS[emo].s2, ARS[emo].s3].map(x => widthAt(boxH, x));
    ok(`反證：舊 s1 ${emo} spread ${spread(oldWs).toFixed(1)}px > 5px（C1 重現）`, spread(oldWs) > 5.0);
  }
}

console.log(fails.length ? 'RESULT FAIL (' + fails.length + ')' : 'RESULT PASS');
if(fails.length){ for(const f of fails) console.log(' - ' + f); process.exit(1); }
