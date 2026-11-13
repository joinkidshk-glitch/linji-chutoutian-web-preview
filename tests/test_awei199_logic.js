// v20a199 DLG199 邏輯測試：阿偉三 tier 高度正規化（修 v195 review B1）。
// 抽 index.html 內 DLG108 模組切片 eval（同 test_dlg108_logic.js 手法），
// fitApply 用手造 fake stage／img（唔使瀏覽器）。
// 覆蓋：(a) 同一配對同一舞台，三 tier＋各表情 painted 高全部相等（誤差 ≤1px）；
//       (b) fit 落點（--dlg108-char-h）同 tier 無關；(c) 單人阿偉同樣受天花板；
//       (d) 非阿偉配對／單人零影響（fitPct 純函數輸出同舊錨點一致）；
//       (e) 顧明輝／阿偉 painted 比回復 v109 嘅 1.05（舊失真 1.108）；
//       (f) 配對總闊 ≤ stageW-margin-12（中間淨空 ≥12px，無重疊、無溢出）；
//       (g) 天花板／參考 AR 輔助函數本身；(h) 反證：REF 唔啱（用真 AR 計）嗰陣
//       三 tier painted 高即刻散開（證明正規化係修復本身，唔係量度假象）；
//       (i) 巧遇 e79 分支（isEnc：margin sw*0.04＋.e79-char 選擇器）：同一配對三 tier 同高。
// 數字來源：probe199（實駕量度，932 viewport、舞台 468×1412／1464）＋ PIL
// 量度全庫 awi* AR（見 test_awei199_static.py，REF 0.345 ＝ s1 angry 0.3446 封頂）。
// 用法：node tests/test_awei199_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS ' : 'FAIL ') + name); }
function info(msg){ console.log('INFO ' + msg); }

const a = html.indexOf('/* ===== v20a108 DLG108');
const b = html.indexOf('/* ===== DLG108 模組完 ===== */');
ok('搵到 DLG108 模組', a >= 0 && b > a);
if (a < 0 || b <= a) { console.log('RESULT FAIL (no DLG108 module)'); process.exit(1); }
const code = html.slice(a, b);
global.window = {};
// DLG109 身高比替身（模組切片外）：阿偉 1.00／彭少祺 0.85／顧明輝・程天諾 1.05，其餘 1.00。
global.dlg109HeightScale = (id)=> id==='pang_siuki' ? 0.85 : (id==='gu_mingfai'||id==='ching_tinlok') ? 1.05 : 1.00;
let D = null, evalErr = null;
try {
  D = eval(code + '\n;({fitPct:dlg108FitPct, fitApply:dlg108FitApply, refAr:DLG199_AWEI_REF_AR, isAweiId:dlg199IsAweiId, fitAr:dlg199FitAr, pctCap:dlg199PctCap})');
} catch(e){ evalErr = e; }
// pristine main 無 DLG199：eval 會 ReferenceError——要乾淨 FAIL，唔准 crash。
ok('eval DLG108 模組切片（含 DLG199）', evalErr === null);
if (evalErr) {
  console.log('INFO eval 失敗：' + evalErr);
  console.log('RESULT FAIL (no DLG199)');
  process.exit(1);
}
ok('搵到 dlg108FitPct／dlg108FitApply', typeof D.fitPct === 'function' && typeof D.fitApply === 'function');
ok('搵到 DLG199 輔助函數', typeof D.fitAr === 'function' && typeof D.pctCap === 'function' && typeof D.refAr === 'number');

// ---------- fake DOM ----------
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
// 瀏覽器 painted 高模型（object-fit:contain，bottom 對齊）：
// painted 高 = min(box 高, maxW/AR)；painted 闊 = painted 高 × AR。
function painted(natW, natH, boxHpx, maxW){
  const ar = natW / natH;
  const ph = Math.min(boxHpx, maxW / ar);
  return { h: ph, w: ph * ar };
}

// 實測 AR（PIL 量度，見 static test）：s1 base 0.3429／angry 0.3446／serious 0.3356；
// s2 base 0.2776／angry 0.288／serious 0.2797；s3 base 0.2779／angry 0.288／serious 0.3032。
const AWI_ARS = { s1_base: 0.3429, s1_angry: 0.3446, s1_serious: 0.3356,
  s2_base: 0.2776, s2_angry: 0.2880, s2_serious: 0.2797,
  s3_base: 0.2779, s3_angry: 0.2880, s3_serious: 0.3032 };
const PARTNERS = { ho_sang: 0.3637, vera: 0.3821, fong_siulung: 0.4127,
  chung_choning: 0.3370, lin_hiu: 0.3220, gu_mingfai: 0.2320, pang_siuki: 0.3760 };
const SW = 468, SH = 1412, MAXW = 0.48 * SW, MARGIN = 12;

function runPair(awiAr, partnerId, partnerAr, stageH){
  const sh = stageH || SH;
  const imgs = [fakeImg('awi', awiAr), fakeImg(partnerId, partnerAr)];
  const st = fakeStage(SW, sh, imgs, false);
  const r = D.fitApply(st);
  if(!r) return null;
  const pct = parseFloat(st.style._props['--dlg108-char-h']);
  const boxH = pct / 100 * sh;
  const boxHp = pct / 100 * sh * global.dlg109HeightScale(partnerId);
  return { pct, awi: painted(imgs[0].naturalWidth, imgs[0].naturalHeight, boxH, MAXW),
    partner: painted(imgs[1].naturalWidth, imgs[1].naturalHeight, boxHp, MAXW),
    inlineH: [imgs[0].style.height, imgs[1].style.height] };
}

// ---- (g) 輔助函數 ----
ok('REF_AR ＝ 0.345', D.refAr === 0.345);
ok('fitAr：阿偉任何真 AR → 0.345', D.fitAr('awi', 0.28) === 0.345 && D.fitAr('awi_s2', 0.30) === 0.345);
ok('fitAr：非阿偉原值奉還', D.fitAr('ho_sang', 0.3637) === 0.3637 && D.fitAr('vera', 0.3821) === 0.3821);
ok('isAweiId：awi／awi_s2／awi_s3 真，其餘假', D.isAweiId('awi') && D.isAweiId('awi_s2') && D.isAweiId('awi_s3') && !D.isAweiId('ho_sang') && !D.isAweiId(''));
ok('pctCap 468×1412 ≈ 46.1%', Math.abs(D.pctCap(SW, SH, 0.48) - 46.1) < 0.05);
ok('pctCap 468×1464 ≈ 44.5%（舞台高啲，天花板 % 低啲，boxH 像素不變）', Math.abs(D.pctCap(SW, 1464, 0.48) - 44.5) < 0.05);
ok('pctCap 無效尺寸回 60', D.pctCap(0, SH, 0.48) === 60 && D.pctCap(SW, 0, 0.48) === 60);

// ---- (a)(b)(f) 逐個搭檔：九個阿偉 AR 全部同高、同一 pct、淨空 ≥12 ----
for(const [pid, par] of Object.entries(PARTNERS)){
  const runs = {};
  for(const [k, ar] of Object.entries(AWI_ARS)) runs[k] = runPair(ar, pid, par);
  const hs = Object.values(runs).map(r => r.awi.h);
  const spread = Math.max(...hs) - Math.min(...hs);
  const pcts = [...new Set(Object.values(runs).map(r => r.pct))];
  ok(`配對 阿偉×${pid}：三 tier 九表情 painted 高 spread ≤1px（${Math.min(...hs).toFixed(1)}–${Math.max(...hs).toFixed(1)}）`, spread <= 1.0);
  ok(`配對 阿偉×${pid}：fit 落點同 tier 無關（pct 唯一：${pcts.join(',')}）`, pcts.length === 1);
  const gaps = Object.values(runs).map(r => SW - MARGIN - (r.awi.w + r.partner.w));
  ok(`配對 阿偉×${pid}：中間淨空 ≥12px（最細 ${Math.min(...gaps).toFixed(1)}px）`, Math.min(...gaps) >= 12 - 0.01);
  info(`  ${pid}: pct=${pcts[0]}% boxH=${(pcts[0]/100*SH).toFixed(1)}px painted=${hs[0].toFixed(1)}px 搭檔 painted=${Object.values(runs)[0].partner.h.toFixed(1)}px`);
}

// ---- (a) 1400 級舞台高（s1 實駕嗰陣 1464）同樣成立 ----
{
  const runs = {};
  for(const [k, ar] of Object.entries(AWI_ARS)) runs[k] = runPair(ar, 'ho_sang', PARTNERS.ho_sang, 1464);
  const hs = Object.values(runs).map(r => r.awi.h);
  ok(`舞台 468×1464 阿偉×何生：三 tier painted 高 spread ≤1px（${Math.min(...hs).toFixed(1)}–${Math.max(...hs).toFixed(1)}）`, Math.max(...hs) - Math.min(...hs) <= 1.0);
}

// ---- (i) 巧遇 e79 分支（isEnc：margin sw*0.04，.e79-char 選擇器） ----
{
  const ENC_MARGIN = SW * 0.04;
  const runPairEnc = (awiAr, partnerId, partnerAr)=>{
    const imgs = [fakeImg('awi', awiAr), fakeImg(partnerId, partnerAr)];
    const st = fakeStage(SW, SH, imgs, true);
    if(!D.fitApply(st)) return null;
    const pct = parseFloat(st.style._props['--dlg108-char-h']);
    const boxH = pct / 100 * SH;
    const boxHp = pct / 100 * SH * global.dlg109HeightScale(partnerId);
    return { pct, awi: painted(imgs[0].naturalWidth, imgs[0].naturalHeight, boxH, MAXW),
      partner: painted(imgs[1].naturalWidth, imgs[1].naturalHeight, boxHp, MAXW) };
  };
  const runs = {};
  for(const [k, ar] of Object.entries(AWI_ARS)) runs[k] = runPairEnc(ar, 'vera', PARTNERS.vera);
  const hs = Object.values(runs).map(r => r.awi.h);
  const pcts = [...new Set(Object.values(runs).map(r => r.pct))];
  ok(`巧遇 e79 阿偉×Vera：三 tier 九表情 painted 高 spread ≤1px（${Math.min(...hs).toFixed(1)}–${Math.max(...hs).toFixed(1)}）`, Math.max(...hs) - Math.min(...hs) <= 1.0);
  ok(`巧遇 e79 阿偉×Vera：fit 落點同 tier 無關（pct 唯一：${pcts.join(',')}）`, pcts.length === 1);
  const gaps = Object.values(runs).map(r => SW - ENC_MARGIN - (r.awi.w + r.partner.w));
  ok(`巧遇 e79 阿偉×Vera：無重疊、無溢出（margin 後淨空最細 ${Math.min(...gaps).toFixed(1)}px，margin 用 sw*0.04）`, Math.min(...gaps) >= 0);
  info(`  e79: pct=${pcts[0]}% painted=${hs[0].toFixed(1)}px 搭檔 painted=${Object.values(runs)[0].partner.h.toFixed(1)}px`);
}

// ---- (c) 單人阿偉 ----
{
  const hs = {};
  for(const [k, ar] of Object.entries(AWI_ARS)){
    const imgs = [fakeImg('awi', ar)];
    const st = fakeStage(SW, SH, imgs, false);
    ok('單人 fitApply 成功 ' + k, D.fitApply(st) === true);
    const pct = parseFloat(st.style._props['--dlg108-char-h']);
    hs[k] = Math.min(pct / 100 * SH, MAXW / ar);
    if(k === 's1_base') ok('單人阿偉 pct ＝天花板 46.1%（唔係 60%）', Math.abs(pct - 46.1) < 0.05);
  }
  const vals = Object.values(hs);
  ok(`單人阿偉：三 tier painted 高 spread ≤1px（${Math.min(...vals).toFixed(1)}–${Math.max(...vals).toFixed(1)}）`, Math.max(...vals) - Math.min(...vals) <= 1.0);
  // 非阿偉單人維持 60%
  const imgs = [fakeImg('ho_sang', PARTNERS.ho_sang)];
  const st = fakeStage(SW, SH, imgs, false);
  D.fitApply(st);
  ok('單人何生維持 60%', st.style._props['--dlg108-char-h'] === '60%');
}

// ---- (d) 非阿偉配對零影響 ----
{
  const pOld = D.fitPct(PARTNERS.fong_siulung, PARTNERS.vera, SW, SH, MARGIN, 0.48);
  const imgs = [fakeImg('fong_siulung', PARTNERS.fong_siulung), fakeImg('vera', PARTNERS.vera)];
  const st = fakeStage(SW, SH, imgs, false);
  D.fitApply(st);
  ok('非阿偉配對：fitApply pct ＝舊 fitPct（無正規化干預）', parseFloat(st.style._props['--dlg108-char-h']) === pOld);
  ok('fitPct 純函數錨點：方小龍＋Vera 54–56%（舊 test 相同，390×844 舞台）', D.fitPct(PARTNERS.fong_siulung, PARTNERS.vera, 390, 844, 12, 0.48) >= 54 && D.fitPct(PARTNERS.fong_siulung, PARTNERS.vera, 390, 844, 12, 0.48) <= 56);
  ok('fitPct 純函數錨點：典型配對 60%', D.fitPct(0.325, 0.325, 390, 844, 12, 0.48) === 60);
  ok('fitPct 純函數錨點：阿偉×何生舊數 60%（390×844 舞台，舊 test 相同）', D.fitPct(0.3429, 0.3637, 390, 844, 12, 0.48) === 60);
}

// ---- (e) 顧明輝／阿偉 painted 比回復 1.05 ----
{
  const r = runPair(AWI_ARS.s2_base, 'gu_mingfai', PARTNERS.gu_mingfai);
  const ratio = r.partner.h / r.awi.h;
  ok(`顧明輝／阿偉 painted 比 ＝1.05（實測 ${ratio.toFixed(3)}，舊失真 1.108）`, Math.abs(ratio - 1.05) < 0.01);
  // 彭少祺 0.85 同理
  const r2 = runPair(AWI_ARS.s2_base, 'pang_siuki', PARTNERS.pang_siuki);
  ok(`彭少祺／阿偉 painted 比 ＝0.85（實測 ${(r2.partner.h / r2.awi.h).toFixed(3)}）`, Math.abs(r2.partner.h / r2.awi.h - 0.85) < 0.01);
}

// ---- (h) 反證：唔用 REF（齋 fitPct＋真 AR）三 tier 即刻散開 ----
{
  // 模擬舊行為：pct＝fitPct(真 AR)，painted＝min(boxH, maxW/AR)
  const oldPainted = (ar, pid, par)=>{
    const pct = D.fitPct(ar, par, SW, SH, MARGIN, 0.48, 1, global.dlg109HeightScale(pid));
    return Math.min(pct / 100 * SH, MAXW / ar);
  };
  const h1 = oldPainted(AWI_ARS.s1_base, 'ho_sang', PARTNERS.ho_sang);
  const h2 = oldPainted(AWI_ARS.s2_base, 'ho_sang', PARTNERS.ho_sang);
  const h3 = oldPainted(AWI_ARS.s3_base, 'ho_sang', PARTNERS.ho_sang);
  info(`  反證舊行為：s1 ${h1.toFixed(1)}px vs s2 ${h2.toFixed(1)}px vs s3 ${h3.toFixed(1)}px`);
  ok('反證：舊行為 s1 比 s2 矮 ≥100px（B1 重現，唔係量度假象）', h2 - h1 >= 100);
}

console.log(fails.length ? 'RESULT FAIL (' + fails.length + ')' : 'RESULT PASS');
if(fails.length){ for(const f of fails) console.log(' - ' + f); process.exit(1); }
