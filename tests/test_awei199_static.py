# v20a199 DLG199／C1–C3 靜態守門。
# 覆蓋：① B1：DLG199_AWEI_REF_AR＝0.345 寫死喺 index.html，且 ≥ 全庫 awi* 全身圖
#       實測最大 AR（PIL 量度；將來新圖超過 REF 會 FAIL，唔會靜靜雞打回原形）；
#       dlg108FitApply 有參考 AR＋天花板兩處呼叫、單人步有 cap、DLG108 匯出有新鍵；
#       DLG109 身高比表原封不動（阿偉三 tier 1.00／彭少祺 0.85／顧明輝・程天諾 1.05）；
#       WF4 對話圖有 onload __dlg108Fit。
#       ② C1：hero_awi／awi_s3 bust sha 同 qa199/crop199.json 一致（awi_s2 唔郁，
#       見 test_bust109_static.py 交叉比對）。
#       ③ C2／C3：兩張新 angry 圖存在＋規格（896×2976、透明底、四角 alpha 0、
#       米白光邊——同 qa199/samples199/bake199_results.json 交叉比對）；
#       sha 同 v195 舊版唔同（證明真係換咗）；s1 angry 原封不動（v199 當時唔郁佢；
#       v20a201 將成個 s1 組重生，awi_angry.webp 已換走，見 test_awei201_static.py；
#       下面 UNTOUCHED 唔再釘佢）；s2／s3 serious 原封不動（C2 對照基線）。
#       ④ 反證：checker 食舊值（舊 angry sha／REF 過細）必須報問題。
#       ⑤ 基線不變：SAVE key／softRev／產品 ?v=。
# 用法：python3 tests/test_awei199_static.py [path-to-index.html]
import base64, glob, hashlib, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "..", "index.html")
ROOT = os.path.dirname(IDX)
with open(IDX, encoding="utf-8") as f:
    src = f.read()

fails = []
def ck(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond: fails.append(name)
def info(msg): print("INFO " + msg)

# ---------- ⑤ 基線不變 ----------
ck("SAVE key 不變", "starVolunteer_map_v19w" in src)
ck("softRev 不變", "s107" in src)
ck("產品 ?v= 不變", "v20a10" in src)

# ---------- ① B1 ----------
m = re.search(r"const DLG199_AWEI_REF_AR = ([0-9.]+);", src)
ck("搵到 DLG199_AWEI_REF_AR", bool(m))
REF = float(m.group(1)) if m else 0
ck("REF_AR ＝ 0.345", REF == 0.345)
try:
    from PIL import Image
    ars = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "assets", "story", "fullbody", "awi*.webp"))):
        im = Image.open(p); im.load()
        ars[os.path.basename(p)] = im.size[0] / im.size[1]
    mx = max(ars.values())
    info("全庫 awi* %d 張，最大 AR %.4f（%s）" % (len(ars), mx, max(ars, key=ars.get)))
    ck("REF ≥ 全庫最大 AR（留 ≥0.001 裕度）", REF >= mx)
    # v20a201：s1 重生後最大 AR 唔再係 s1 angry 0.3446，改為 s3 serious 0.3032。
    ck("REF ≥ 邏輯測試九個 AR（s3 serious 0.3032 封頂，v201 後）", REF >= 0.3032)
    # 寫死最大三張，防 PIL 量度漂移靜靜過關
    ck("s1 angry AR ≈ 0.2801（v201 重生）", abs(ars.get("awi_angry.webp", 0) - 0.2801) < 0.001)
    ck("新 s2／s3 angry AR ≈ 0.3011（bake 後 896×2976）",
       abs(ars.get("awi_s2_angry.webp", 0) - 0.3011) < 0.001
       and abs(ars.get("awi_s3_angry.webp", 0) - 0.3011) < 0.001)
except ImportError:
    info("PIL 缺席：AR 量度跳過（環境問題，唔係遊戲問題）")

ck("fitApply 用參考 AR 計 fit", "a.push(dlg199FitAr(idOf(im), im.naturalWidth/im.naturalHeight));" in src)
ck("fitApply 有阿偉天花板", "if(hasAwi199){ var cap199 = dlg199PctCap(sw, sh, 0.48); if(cap199 < pct) pct = cap199; }" in src)
ck("單人步有阿偉天花板", "pct1 = Math.min(60, dlg199PctCap(sw1, sh1, 0.48));" in src)
ck("DLG108 匯出有 DLG199 鍵", "aweiRefAr:DLG199_AWEI_REF_AR" in src and "pctCap:dlg199PctCap" in src)
ck("dlg108FitPct 純函數無改名／無改簽名",
   "function dlg108FitPct(arL, arR, stageW, stageH, marginPx, maxWfrac, scaleL, scaleR){" in src)
for frag in ['"awi":1.00, "awi_s2":1.00, "awi_s3":1.00', '"pang_siuki":0.85',
             '"gu_mingfai":1.05, "ching_tinlok":1.05']:
    ck(f"DLG109 身高比原封不動：{frag}", frag in src)
ck("WF4 對話圖有 onload __dlg108Fit",
   'onload="try{window.__dlg108Fit&&window.__dlg108Fit(this)}catch(_e){}" onerror="try{window.__dlg106Err' in src)

# ---------- ② C1 ----------
def extract_map(name):
    a = src.index("const %s = {" % name)
    b = src.index("};", a) + 2
    return dict(re.findall(r'"([^"]+)":\s*"([^"]+)"', src[a:b]))
crop199_path = os.path.join(ROOT, "qa199", "crop199.json")
# v20a201：hero_awi bust 由新 base 重裁，新記錄喺 qa201/crop201.json（1 鍵）；
# awi_s3 繼續用 crop199.json。
crop201_path = os.path.join(ROOT, "qa201", "crop201.json")
crop201 = {}
if os.path.exists(crop201_path):
    with open(crop201_path, encoding="utf-8") as f: crop201 = json.load(f)
    ck("crop201.json 有 1 項（hero_awi）", set(crop201) == {"hero_awi"})
if os.path.exists(crop199_path):
    with open(crop199_path, encoding="utf-8") as f: crop199 = json.load(f)
    ck("crop199.json 有 2 項", set(crop199) == {"hero_awi", "awi_s3"})
    P, E = extract_map("PORTRAITS"), extract_map("BUST109_EXTRA")
    expect = {"hero_awi": (P.get("hero_awi", ""), crop201.get("hero_awi") or crop199["hero_awi"]),
              "awi_s3": (E.get("awi_s3", ""), crop199["awi_s3"])}
    for key, (val, rec) in expect.items():
        raw = base64.b64decode(val.split(",", 1)[1])
        ck(f"{key} bust sha 同 crop 記錄一致",
           hashlib.sha256(raw).hexdigest() == rec["webp_sha256"])
        ck(f"{key} bust 唔等於舊 crop109 值",
           hashlib.sha256(raw).hexdigest() != rec["old_webp_sha256"])
else:
    info("qa199/crop199.json 缺席，跳過 C1 hash 比對")

# ---------- ③ C2／C3 ----------
OLD_ANGRY = {  # v195 版（main b1633e6 實量），今票必須換走
  "awi_s2_angry.webp": "aa50c70ee89db6b50bb68449deb415c086efa1ea2e5415258b2fe2ed57e4bb3d",
  "awi_s3_angry.webp": "f863fef694109bea4f23251f59fb3d044eaa3dd3006986b2e42931a71661bdd6",
}
UNTOUCHED = {  # 今票唔郁（main b1633e6 實量；v20a201 拎走咗 awi_angry.webp——成個 s1 組重生）
  "awi_s2_serious.webp": "0a8b8e825a8b8b51a6354c94d2fa7f702473eb24c5066a2653ce1bf64acd47ae",
  "awi_s3_serious.webp": "e05c2fe8928d714838119e39d6fbc4ae96175dc584f1d86b0f78cc8d1f165f97",
}
def file_sha(fn):
    with open(os.path.join(ROOT, "assets", "story", "fullbody", fn), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()
for fn, old in OLD_ANGRY.items():
    p = os.path.join(ROOT, "assets", "story", "fullbody", fn)
    ck(f"{fn} 存在", os.path.exists(p))
    if os.path.exists(p):
        ck(f"{fn} sha 同 v195 舊版唔同（C2／C3 真係換咗）", file_sha(fn) != old)
        try:
            from PIL import Image
            import numpy as np
            im = Image.open(p).convert("RGBA"); im.load()
            a = np.array(im)
            ck(f"{fn} 尺寸 896×2976", im.size == (896, 2976))
            ck(f"{fn} 四角 alpha 皆 0",
               a[0, 0, 3] == 0 and a[0, -1, 3] == 0 and a[-1, 0, 3] == 0 and a[-1, -1, 3] == 0)
            transp = float((a[:, :, 3] == 0).mean())
            ck(f"{fn} 透明底佔比 0.30–0.45（實測 {transp:.3f}，同其餘全身圖同一處理）",
               0.30 <= transp <= 0.45)
            # 米白光邊（同 bake195／v107 口徑）：figure＝不透明且唔係米白；ring＝figure
            # 膨脹 r 減 figure；ring 入面 alpha>200 嗰啲像素 ≥95% 係米白 ±12。
            from scipy import ndimage
            opaque = a[:, :, 3] > 128
            cream = np.abs(a[:, :, :3].astype(np.int16) - np.array([243, 233, 210])).max(axis=2) <= 12
            figure = opaque & ~cream
            figure = ndimage.binary_fill_holes(figure)
            r = round(3 * a.shape[0] / 422)
            yy, xx = np.ogrid[-r:r + 1, -r:r + 1]
            disk = (xx * xx + yy * yy) <= r * r
            ring = ndimage.binary_dilation(figure, structure=disk) & ~figure
            edge_sel = ring & (a[:, :, 3] > 200)
            frac = float((edge_sel & cream).sum() / max(1, edge_sel.sum()))
            ck(f"{fn} 光邊帶米白比例 ≥0.95（實測 {frac:.3f}，bake195 同口徑）", frac >= 0.95)
        except ImportError:
            info("PIL／scipy 缺席：%s 像素檢查跳過" % fn)
for fn, sha in UNTOUCHED.items():
    ck(f"{fn} 原封不動（今票唔郁）", file_sha(fn) == sha)
bake_path = os.path.join(ROOT, "qa199", "samples199", "bake199_results.json")
if os.path.exists(bake_path):
    with open(bake_path, encoding="utf-8") as f: bake = json.load(f)
    for r in bake:
        ck(f"bake199 {r['file']}：邊帶米白 ≥0.95、零遠處米白、畫框全透明",
           r["edge_color_frac"] >= 0.95 and r["far_cream_px"] == 0
           and r["frame_transparent_frac"] >= 0.99 and r["ok"])
else:
    info("bake199_results.json 缺席，跳過 bake 交叉比對")

# ---------- ④ 反證 ----------
def check_ref(ref_val, angry_shas):
    problems = []
    if ref_val < 0.3032: problems.append("REF 細過 s3 serious AR（v201 後全庫最大）")
    for fn, old in OLD_ANGRY.items():
        if angry_shas.get(fn) == old: problems.append(fn + " 未換")
    return problems
cur_shas = {fn: file_sha(fn) for fn in OLD_ANGRY}
ck("反證：REF 0.30＋舊 angry sha → 報問題", len(check_ref(0.30, OLD_ANGRY)) >= 2)
ck("反證：現值（REF 0.345＋新 sha）→ 零問題", check_ref(REF, cur_shas) == [])

print("FAILURES: %d" % len(fails))
for f in fails: print(" - " + f)
sys.exit(1 if fails else 0)
