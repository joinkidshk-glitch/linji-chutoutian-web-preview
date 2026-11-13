# v20a201 s1 全身組重生靜態守門（修 v199 review C1：s1 闊過 s2／s3 約 14–20%）。
# 覆蓋：① s1 8 張全部重生（media pipeline，風格錨＋舊圖做底）——檔案 AR 一律
#       ≈0.280（±0.004），尺寸 base 784×2800、其餘 7 張 865×3088，RGBA 透明底、
#       四角 alpha 0、米白光邊（v107 口徑，ring 米白 ≥0.95、零遠處米白、畫框全透明）；
#       sha 同 v199 舊版全部唔同（證明真係換晒 8 張，唔係淨換 review 量過嗰兩張）。
#       ② bake201_results.json 交叉比對（8 張全部 ok、AR 0.28、光邊完整）。
#       ③ s2／s3 16 張原封不動（sha 同 main 2c1a680 實量一致）——今票唔郁佢哋；
#       殘留闊度差（serious／angry／smile 三 tier spread >5px）係 s2／s3 本身 AR
#       分散（s3 serious 0.3032、s2／s3 angry 0.3011）造成，見 logic test，
#       唔係 s1 未修好。
#       ④ DLG199 唔郁：REF 仍係 0.345，且 ≥ 全庫最大 AR（而家係 s3 serious 0.3032，
#       唔再係 s1 angry 0.3446）；DLG199 註解話「最大 AR 0.345」已成歷史陳述，
#       code 本身唔郁（見 NOTES）。
#       ⑤ hero_awi bust 由新 base 重裁：sha 同 qa201/crop201.json 一致，唔等於
#       crop199 舊值；awi_s3 bust 唔郁。
#       ⑥ 反證：checker 食舊 s1 sha／舊 AR 必須報問題。
#       ⑦ 基線不變：SAVE key／softRev／產品 ?v=；同路徑覆蓋、loader 零改動
#       （?v=20a106 不變，見 NOTES 快取一節：GitHub Pages max-age=600）。
# 用法：python3 tests/test_awei201_static.py [path-to-index.html]
import base64, glob, hashlib, json, os, re, sys

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

EXPRS = ["base", "serious", "angry", "sad", "shy", "smile", "surprise", "think"]
# s1 舊版 sha（main 2c1a680 實量，bake201_results.json 亦有記錄）
OLD_S1 = {
  "awi_angry.webp": "8508c88d22f532c83e849ad10f0815558a6d83450775a13735755d8b57596dbe",
  "awi_base.webp": "33138b6679ce5f9ce15db32c90a4f6e50a6952cbed6a2d213bc31bfed48b454c",
  "awi_sad.webp": "edb5c850751cdca19a98625f83d02dbb289010e156978c13de5761e4a8075938",
  "awi_serious.webp": "54d1d2f81cd0ec9d35769e5a5f7fd941659c4214baffeb62a610ffc9bc7cf896",
  "awi_shy.webp": "5c3f09a1b9c8c54e9b08e6476509fd8dffef57dc601a7742e857e97ff7c16156",
  "awi_smile.webp": "51c51a33e7eeed68b76b0494827499a25b73066e68344db98a5d396189e72f27",
  "awi_surprise.webp": "51c75ab012334ecc8c83c11c1d192aa1a79bc9142d37c994d928849aacbc5441",
  "awi_think.webp": "3e2650f9a3533225d10e7c9fe9754177820f2ad2032b08ce9f0d5e80468d0f9e",
}
# s1 新版 sha（bake201 後實量）
NEW_S1 = {
  "awi_angry.webp": "d9fd6ea920e8b430b69f496c2d6ba59f357d9e2a0103a14473f04066e5b090b3",
  "awi_base.webp": "3472eb79e0ef3f14bca0aec468b75b39475656d928a0d11cf40cbea591ff2b12",
  "awi_sad.webp": "b3955b771909b835827ddfe14542da35c23444ca44e539f0bd0aa2c87199a17e",
  "awi_serious.webp": "feafa77b60ba5ef180b07d8c181b7f45fddd40ac557ca78f1d50e844b4970a60",
  "awi_shy.webp": "5c0022a27f5de03498a7a3bc9dd60dcf0fc5ffe145442e7f37a56aad406b445d",
  "awi_smile.webp": "eb9e8c14b5ce5fe3a93ff49725427224428f8c4a962a6d82ab19dcce84335fd4",
  "awi_surprise.webp": "13cee91ce5fba1d5378b7fc8514e93bd79479315375a5110efd81153fcbdc8e2",
  "awi_think.webp": "2d4ef8776e4d8759deb1f5ded0296d5eb126b6fe78f8c3d978a920918e84c033",
}
EXPECTED_SIZE = {"awi_base.webp": (784, 2800)}
for e in EXPRS:
    if e != "base":
        EXPECTED_SIZE["awi_%s.webp" % e] = (865, 3088)
# s2／s3 原封不動（main 2c1a680 實量）
UNTOUCHED_S23 = {
  "awi_s2_angry.webp": "ba23f9ae3f9a72a86464d0effcd8916b4fe3623b46eaff3c1bd0c74c6d622705",
  "awi_s2_base.webp": "205f73928308304ab477f8c20d4b9be4925af56cab760e9c915d573b1388f349",
  "awi_s2_sad.webp": "3fc90191570ec07ac1e2f2858b23dcc05464a1fb87886d32752584d504b91315",
  "awi_s2_serious.webp": "0a8b8e825a8b8b51a6354c94d2fa7f702473eb24c5066a2653ce1bf64acd47ae",
  "awi_s2_shy.webp": "93a5be0eb4200999ba368f336e51c9dbd59ce2f061f6207a8a81e642207cea10",
  "awi_s2_smile.webp": "63b434d2586b35c481eddfe13a654dfe7037f920428ab2bc157a2493d19268eb",
  "awi_s2_surprise.webp": "1441a2a388e89d77d93421c6154dc58a2bd0be5ffa9d0e2276e7ec5f7b3c1232",
  "awi_s2_think.webp": "fd9e4b214ac6d60ce9b5b2d13a8d51a3bb7cc84135a5fdff871694779419cad3",
  "awi_s3_angry.webp": "a37d1e34c8fe885268acc436c05c3f96b6e3f99422b7e90b653cc3051edff7e4",
  "awi_s3_base.webp": "89541cffbbf0a87d9a4ceaeb1bf3145472e0eaf8094fb513ba54b1e3d8e9527b",
  "awi_s3_sad.webp": "9c8721107940a3377d65dcc229e914c88e4187171c6b66da0ac45ffcda66b8e2",
  "awi_s3_serious.webp": "e05c2fe8928d714838119e39d6fbc4ae96175dc584f1d86b0f78cc8d1f165f97",
  "awi_s3_shy.webp": "6d9d7a1b3af2c8acac6ea3072354d2704edb34d83db8e4e620a9c6c760887638",
  "awi_s3_smile.webp": "775305cb62014cf8fb4338344e8b94356f62929daa7c46300fa4e373d41e2d69",
  "awi_s3_surprise.webp": "3753137ba83c4529cbe1e274162f9c0ab04d810a07d340d510bf1ac6abba9bbb",
  "awi_s3_think.webp": "9ee8d9a73a3e34dfede96df67fded119218e66312af337ab53f60968d7ef8a41",
}

def file_sha(fn):
    with open(os.path.join(ROOT, "assets", "story", "fullbody", fn), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

# ---------- ⑦ 基線不變 ----------
ck("SAVE key 不變", "starVolunteer_map_v19w" in src)
ck("softRev 不變", "s107" in src)
ck("產品 ?v= 不變", "v20a10" in src)
ck("loader 零改動：fullbody ?v= 仍係 20a106（同路徑覆蓋，唔使新檔名）",
   "assets/story/fullbody/\"+st+\"_\"+ex+\".webp?v=20a106" in src)

# ---------- ① s1 8 張重生：AR／尺寸／sha／透明底／光邊 ----------
try:
    from PIL import Image
    import numpy as np
    from scipy import ndimage
    ars = {}
    for e in EXPRS:
        fn = "awi_%s.webp" % e
        p = os.path.join(ROOT, "assets", "story", "fullbody", fn)
        ck(f"{fn} 存在", os.path.exists(p))
        if not os.path.exists(p):
            continue
        ck(f"{fn} sha 同舊版唔同（真係換咗）", file_sha(fn) != OLD_S1[fn])
        ck(f"{fn} sha 同新版記錄一致", file_sha(fn) == NEW_S1[fn])
        im = Image.open(p).convert("RGBA"); im.load()
        a = np.array(im)
        ars[fn] = im.size[0] / im.size[1]
        ck(f"{fn} 尺寸 {EXPECTED_SIZE[fn]}", im.size == EXPECTED_SIZE[fn])
        ck(f"{fn} AR ≈ 0.280（實測 {ars[fn]:.4f}）", abs(ars[fn] - 0.280) <= 0.004)
        ck(f"{fn} 四角 alpha 皆 0",
           a[0, 0, 3] == 0 and a[0, -1, 3] == 0 and a[-1, 0, 3] == 0 and a[-1, -1, 3] == 0)
        transp = float((a[:, :, 3] == 0).mean())
        ck(f"{fn} 透明底佔比 0.30–0.45（實測 {transp:.3f}）", 0.30 <= transp <= 0.45)
        # 米白光邊（v107 口徑）：figure＝不透明且唔係米白；ring＝figure 膨脹 r 減 figure；
        # ring 入面 alpha>200 嗰啲像素 ≥95% 係米白 ±12；米白像素唔可以離 figure >r+1。
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
        ck(f"{fn} 光邊帶米白比例 ≥0.95（實測 {frac:.3f}）", frac >= 0.95)
        dist_b = ndimage.distance_transform_edt(~figure)
        far = int((((a[:, :, 3] > 200) & cream) & (dist_b > r + 1)).sum())
        ck(f"{fn} 零遠處米白像素（{far}）", far == 0)
        # 人物完整：alpha bbox 唔掂畫框（光邊離框 ≥1px 透明邊，唔係裁甩邊）
        ys, xs = np.where(opaque)
        ck(f"{fn} 人物唔掂畫框（邊距 L{xs.min()} R{a.shape[1]-1-xs.max()} T{ys.min()} B{a.shape[0]-1-ys.max()}）",
           xs.min() >= 1 and ys.min() >= 1
           and (a.shape[1] - 1 - xs.max()) >= 1 and (a.shape[0] - 1 - ys.max()) >= 1)
    if ars:
        info("s1 AR：%s（spread %.4f）" % (
            ", ".join("%s %.4f" % (k, v) for k, v in sorted(ars.items())),
            max(ars.values()) - min(ars.values())))
        ck("s1 8 張 AR spread ≤0.001（組內一致）", max(ars.values()) - min(ars.values()) <= 0.001)
except ImportError:
    info("PIL／scipy 缺席：像素檢查跳過（環境問題，唔係遊戲問題）")

# ---------- ② bake201 交叉比對 ----------
bake_path = os.path.join(ROOT, "qa201", "samples201", "bake201_results.json")
if os.path.exists(bake_path):
    with open(bake_path, encoding="utf-8") as f: bake = json.load(f)
    ck("bake201_results.json 有 8 項", len(bake) == 8)
    for r in bake:
        ck(f"bake201 {r['file']}：ok、AR 0.28、邊帶米白 ≥0.95、零遠處米白、畫框全透明",
           r["ok"] and abs(r["ar"] - 0.28) <= 0.004 and r["edge_color_frac"] >= 0.95
           and r["far_cream_px"] == 0 and r["frame_transparent_frac"] >= 0.99)
else:
    info("bake201_results.json 缺席，跳過 bake 交叉比對")

# ---------- ③ s2／s3 原封不動 ----------
for fn, sha in UNTOUCHED_S23.items():
    ck(f"{fn} 原封不動（今票唔郁）", file_sha(fn) == sha)

# ---------- ④ DLG199 唔郁 ----------
m = re.search(r"const DLG199_AWEI_REF_AR = ([0-9.]+);", src)
ck("搵到 DLG199_AWEI_REF_AR", bool(m))
REF = float(m.group(1)) if m else 0
ck("REF_AR 仍係 0.345（唔郁）", REF == 0.345)
try:
    from PIL import Image
    ars_all = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "assets", "story", "fullbody", "awi*.webp"))):
        im = Image.open(p); im.load()
        ars_all[os.path.basename(p)] = im.size[0] / im.size[1]
    mx = max(ars_all.values())
    info("全庫 awi* %d 張，最大 AR %.4f（%s）" % (len(ars_all), mx, max(ars_all, key=ars_all.get)))
    ck("REF ≥ 全庫最大 AR", REF >= mx)
    ck("全庫最大 AR 而家係 s3 serious 0.3032（唔再係 s1 angry）",
       max(ars_all, key=ars_all.get) == "awi_s3_serious.webp"
       and abs(mx - 0.3032) < 0.001)
except ImportError:
    info("PIL 缺席：AR 量度跳過")

# ---------- ⑤ hero_awi bust 由新 base 重裁 ----------
def extract_map(name):
    a = src.index("const %s = {" % name)
    b = src.index("};", a) + 2
    return dict(re.findall(r'"([^"]+)":\s*"([^"]+)"', src[a:b]))
crop201_path = os.path.join(ROOT, "qa201", "crop201.json")
if os.path.exists(crop201_path):
    with open(crop201_path, encoding="utf-8") as f: crop201 = json.load(f)
    ck("crop201.json 有 1 項（hero_awi）", set(crop201) == {"hero_awi"})
    P = extract_map("PORTRAITS")
    raw = base64.b64decode(P.get("hero_awi", "").split(",", 1)[1])
    ck("hero_awi bust sha 同 crop201.json 一致",
       hashlib.sha256(raw).hexdigest() == crop201["hero_awi"]["webp_sha256"])
    ck("hero_awi bust 唔等於 crop199 舊值（base 換咗，bust 跟住換）",
       hashlib.sha256(raw).hexdigest() != crop201["hero_awi"]["old_webp_sha256"])
else:
    info("qa201/crop201.json 缺席，跳過 bust 交叉比對")

# ---------- ⑥ 反證 ----------
def check_s1(ars_dict, shas):
    problems = []
    for fn, ar in ars_dict.items():
        if abs(ar - 0.280) > 0.004:
            problems.append(fn + " AR 唔係 0.28")
    for fn, old in OLD_S1.items():
        if shas.get(fn) == old:
            problems.append(fn + " 未換")
    return problems
cur_ars = {}
try:
    from PIL import Image
    for e in EXPRS:
        im = Image.open(os.path.join(ROOT, "assets", "story", "fullbody", "awi_%s.webp" % e))
        cur_ars["awi_%s.webp" % e] = im.size[0] / im.size[1]
except ImportError:
    pass
cur_shas = {fn: file_sha(fn) for fn in OLD_S1}
old_ars = {"awi_%s.webp" % e: v for e, v in
           zip(EXPRS, [0.3429, 0.3356, 0.3446, 0.3351, 0.3356, 0.3354, 0.3360, 0.3355])}
ck("反證：舊 s1 AR（0.335–0.345）＋舊 sha → 報問題",
   len(check_s1(old_ars, OLD_S1)) >= 8)
ck("反證：現值（AR 0.28＋新 sha）→ 零問題", check_s1(cur_ars, cur_shas) == [])

print("FAILURES: %d" % len(fails))
for f in fails: print(" - " + f)
sys.exit(1 if fails else 0)
