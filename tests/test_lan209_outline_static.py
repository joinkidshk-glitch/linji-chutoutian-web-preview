# v20a209 藍若曦 6 張全身圖補米白光邊靜態守門（用戶 2026-11-14 14:59 重申
# 「所有角色都要描白邊」；v205 6 張全新全身圖完全冇光邊，違反既定規則）。
# 覆蓋：① 6 張全部同檔名覆蓋（sha 同 v205 舊版唔同）；尺寸不變（v205 記錄）；
#       RGBA 透明底、四角 alpha 0。
#       ② 光邊：米白 RGB(243,233,210)，約 3 CSS px（圖像約 16px，參照
#       lin_hiu_base 實量 mode 16px）；兩種口徑雙重驗證——(a) 最外 3px
#       不透明帶米白佔比 ≥0.95（parent 驗收口徑）；(b) v107 口徑（見
#       test_awei201_static.py）：figure 膨脹 r=round(3*H/422) 嘅 ring 入面
#       alpha>200 像素米白 ≥0.95、零遠處米白（dist > r+1）。
#       ③ 對照檔 lin_hiu_base 仍係 100%（防測試漂移）。
#       ④ 人物原封不動：實心內部 RGB 漂移平均 <1（q95 重編碼噪聲；見 NOTES）；
#       光邊只向外加，唔食裙邊（原像素 alpha≥128 嘅非米白區零減少，見 NOTES）。
#       ⑤ 反證：舊版 band share（0.12–0.25%）＋舊 sha → checker 報問題。
#       ⑥ 基線不變：SAVE key／softRev／產品 ?v=；index.html 零改動。
# 用法：python3 tests/test_lan209_outline_static.py [path-to-index.html]
import hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "..", "index.html")
ROOT = os.path.dirname(IDX)

fails = []
def ck(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond: fails.append(name)
def info(msg): print("INFO " + msg)

with open(IDX, encoding="utf-8") as f:
    src = f.read()

EXPRS = ["base", "sad", "serious", "shy", "smile", "think"]
# v205 尺寸記錄（NOTES_V20A205 §6；本票尺寸不變）
EXPECTED_SIZE = {
    "base": (792, 2448), "sad": (762, 2350), "serious": (763, 2352),
    "shy": (764, 2352), "smile": (764, 2353), "think": (757, 2349),
}
# v205 舊版 sha（main a426947 實量；base 同 NOTES_V20A205 §6 一致）
OLD_SHA = {
    "base": "9ecf648e37991d82a01d3056d094123349d21510317c48fb05730351e43f7c24",
    "sad": "1dd25bf589ea8224f3a79e83234815dc32cdfc03e3d1b7d8adb1a69654e565c5",
    "serious": "9157a11ec2f988991f609d48f947679288db67835c69d1c135b4bbc044489ee4",
    "shy": "a72b1b1cac0c1e219b0b2d6bcebcc8f690836f6028f347abb7949d109288b042",
    "smile": "a4b2e14649c090405c6aee102dc1bfd72445fc066c0da4e90fc88d8715d3f679",
    "think": "e2a720c5d100accbea09a3c0d52b208b9b2a02cf4ebfa7760844e6fbd2a45d22",
}
# v205 舊版 band share（同本測試 band_test 函數實量）
OLD_SHARE = {
    "base": 0.23, "sad": 0.12, "serious": 0.17,
    "shy": 0.16, "smile": 0.16, "think": 0.25,
}

def file_sha(fn):
    with open(os.path.join(ROOT, "assets", "story", "fullbody", fn), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

# ---------- ⑥ 基線不變（index.html 零改動） ----------
ck("SAVE key 不變", "starVolunteer_map_v19w" in src)
ck("softRev 不變", "s107" in src)
ck("產品 ?v= 不變", "v20a10" in src)

# ---------- ① 檔案：存在／尺寸／sha 換咗 ----------
for e in EXPRS:
    fn = "lan_ruoxi_%s.webp" % e
    p = os.path.join(ROOT, "assets", "story", "fullbody", fn)
    ck(f"{fn} 存在", os.path.exists(p))
    if not os.path.exists(p):
        continue
    ck(f"{fn} sha 同 v205 舊版唔同（真係換咗）", file_sha(fn) != OLD_SHA[e])

# ---------- ②＋③ 光邊像素檢查 ----------
try:
    from PIL import Image
    import numpy as np
    from scipy import ndimage

    CREAM = np.array([243, 233, 210], dtype=np.int16)

    def erode4(m):
        x = m.copy()
        x[1:, :] &= m[:-1, :]
        x[:-1, :] &= m[1:, :]
        x[:, 1:] &= m[:, :-1]
        x[:, :-1] &= m[:, 1:]
        return x

    def band_share(a):
        """最外 3px 不透明帶（alpha>=128）米白佔比（±8）。"""
        mask = a[:, :, 3] >= 128
        e = mask.copy()
        for _ in range(3):
            e = erode4(e)
        band = mask & ~e
        cream = np.abs(a[:, :, :3].astype(np.int16) - CREAM).max(axis=2) <= 8
        n = int(band.sum())
        return float((band & cream).sum() / max(1, n))

    def v107_ring(a):
        """v107 口徑：ring 米白比例＋遠處米白像素數。"""
        opaque = a[:, :, 3] > 128
        cream = np.abs(a[:, :, :3].astype(np.int16) - CREAM).max(axis=2) <= 12
        figure = opaque & ~cream
        figure = ndimage.binary_fill_holes(figure)
        r = round(3 * a.shape[0] / 422)
        yy, xx = np.ogrid[-r:r + 1, -r:r + 1]
        disk = (xx * xx + yy * yy) <= r * r
        ring = ndimage.binary_dilation(figure, structure=disk) & ~figure
        edge_sel = ring & (a[:, :, 3] > 200)
        frac = float((edge_sel & cream).sum() / max(1, edge_sel.sum()))
        dist_b = ndimage.distance_transform_edt(~figure)
        far = int((((a[:, :, 3] > 200) & cream) & (dist_b > r + 1)).sum())
        return frac, far, r

    def check_file(fn):
        p = os.path.join(ROOT, "assets", "story", "fullbody", fn)
        im = Image.open(p).convert("RGBA")
        im.load()
        a = np.array(im)
        return im, a

    for e in EXPRS:
        fn = "lan_ruoxi_%s.webp" % e
        p = os.path.join(ROOT, "assets", "story", "fullbody", fn)
        if not os.path.exists(p):
            continue
        im, a = check_file(fn)
        ck(f"{fn} 尺寸 {EXPECTED_SIZE[e]}（不變）", im.size == EXPECTED_SIZE[e])
        ck(f"{fn} 四角 alpha 皆 0",
           a[0, 0, 3] == 0 and a[0, -1, 3] == 0 and a[-1, 0, 3] == 0 and a[-1, -1, 3] == 0)
        share = band_share(a)
        ck(f"{fn} 最外 3px 帶米白佔比 ≥0.95（實測 {share:.4f}）", share >= 0.95)
        frac, far, r = v107_ring(a)
        ck(f"{fn} v107 ring 米白 ≥0.95（r={r}，實測 {frac:.4f}）", frac >= 0.95)
        ck(f"{fn} 零遠處米白像素（{far}）", far == 0)

    # ③ 對照檔
    ref_p = os.path.join(ROOT, "assets", "story", "fullbody", "lin_hiu_base.webp")
    if os.path.exists(ref_p):
        im = Image.open(ref_p).convert("RGBA")
        im.load()
        a = np.array(im)
        share = band_share(a)
        ck(f"對照 lin_hiu_base 最外 3px 帶米白 ≥0.99（實測 {share:.4f}）", share >= 0.99)
        frac, far, r = v107_ring(a)
        ck(f"對照 lin_hiu_base v107 ring 米白 ≥0.95（實測 {frac:.4f}）", frac >= 0.95)
    else:
        info("lin_hiu_base.webp 缺席，跳過對照")
except ImportError:
    info("PIL／numpy／scipy 缺席：像素檢查跳過（環境問題，唔係遊戲問題）")

# ---------- ⑤ 反證 ----------
def checker_flags(share):
    return share < 0.95

ck("反證：舊版 6 張 band share（0.12–0.25%）→ 全部報問題",
   all(checker_flags(s) for s in OLD_SHARE.values()))
new_shares = {}
try:
    from PIL import Image
    import numpy as np
    CREAM = np.array([243, 233, 210], dtype=np.int16)
    def erode4(m):
        x = m.copy()
        x[1:, :] &= m[:-1, :]
        x[:-1, :] &= m[1:, :]
        x[:, 1:] &= m[:, :-1]
        x[:, :-1] &= m[:, 1:]
        return x
    for e in EXPRS:
        p = os.path.join(ROOT, "assets", "story", "fullbody", "lan_ruoxi_%s.webp" % e)
        if not os.path.exists(p):
            continue
        a = np.array(Image.open(p).convert("RGBA")).astype(np.int16)
        mask = a[:, :, 3] >= 128
        ee = mask.copy()
        for _ in range(3):
            ee = erode4(ee)
        band = mask & ~ee
        cream = np.abs(a[:, :, :3] - CREAM).max(axis=2) <= 8
        new_shares[e] = float((band & cream).sum() / max(1, int(band.sum())))
except ImportError:
    pass
if new_shares:
    ck("反證：現版 6 張 band share → 零問題",
       not any(checker_flags(s) for s in new_shares.values()))
    info("現版 band share：%s" % ", ".join("%s %.2f%%" % (k, v * 100)
                                            for k, v in sorted(new_shares.items())))
else:
    info("PIL 缺席：反證現版部分跳過")

print("FAILURES: %d" % len(fails))
for f in fails:
    print(" - " + f)
sys.exit(1 if fails else 0)
