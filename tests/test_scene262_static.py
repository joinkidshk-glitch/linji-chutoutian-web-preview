# v20a262 靜態守門：6 張約會場景圖重做平滑版（像素版作廢）。
# v159 像素版 6 張（assets/story/locs/bg_159_*.jpg，720×1280）改做平滑二次元動畫風，
# 風格錨 style-anchor-awei-anime.jpg；每張先搵真實香港相片做參照（見
# ~/workspace/linji-work-news-refs/SOURCES262.md），目視逐張核實合格先入庫。
# §1：6 張圖存在、JPEG、720×1280。
# §2：sha256 唔等於 v159 像素版舊 sha（防回潮／誤還原），舊 sha 見下表。
# §3：不變量——換圖唔郁 code：6 個 date_* LOC_SHEET_BG 條目維持原路徑唔加 ?v= 參數；
#     SAVE key／softRev／產品 ?v= 不變。
# 反證：對 pristine main（9b1e6f0）跑，§2 6 項必須乾淨 FAIL（仲係像素版舊 sha），唔 crash。
# 用法：python3 tests/test_scene262_static.py [path-to-index.html]
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "..", "index.html")
ROOT = os.path.dirname(IDX)
with open(IDX, encoding="utf-8") as f:
    src = f.read()

fails = []


def ck(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)


def info(msg):
    print("INFO " + msg)


# v159 像素版舊 sha256（完整值；由 linji-repo 實量，見 NOTES_V20A262.md）
OLD_SHA = {
    "airport": "a899e3f60fec12bde299d4711917df5efa981b2b68e016d33ebaf36092594abc",
    "beach": "9b8e3a9874f6295b194791f01e9d78879c5d3bfbeaa3d2f61cb14c7db4104f8e",
    "cinema": "5f60242539b05a287390da4b0bf1dc45456129e55ac54b9cc7e5c6ce08e59cb4",
    "harbour": "5d5cdc5339f7cf05eca710a75a2edc574aebb40df939dcc5d9f9ef708048b3d4",
    "lounge": "572b19fb9c8dcc6d127c87821b3caa2bee501cd591566ead2b0568cb901c9862",
    "peak": "421a643e0a71edddd7438eca53b547be67012950454ac899ee8f0e4fc6d9d15d",
}

try:
    from PIL import Image
    have_pil = True
except ImportError:
    have_pil = False
    info("PIL 缺失：跳過尺寸斷言（只驗存在＋sha）")

# ---------- §1＋§2：6 張圖 ----------
for stem, old_sha in OLD_SHA.items():
    p = os.path.join(ROOT, "assets", "story", "locs", "bg_159_%s.jpg" % stem)
    ck("§1 bg_159_%s 存在" % stem, os.path.isfile(p))
    if not os.path.isfile(p):
        continue
    with open(p, "rb") as f:
        data = f.read()
    ck("§1 bg_159_%s 係 JPEG" % stem, data[:2] == b"\xff\xd8")
    sha = hashlib.sha256(data).hexdigest()
    info("bg_159_%s sha %s" % (stem, sha[:12]))
    ck("§2 bg_159_%s 唔係 v159 像素版舊檔" % stem, sha != old_sha)
    if have_pil:
        im = Image.open(p)
        ck("§1 bg_159_%s 720x1280（實量 %s）" % (stem, im.size), im.size == (720, 1280))

# ---------- §3：不變量 ----------
for stem in OLD_SHA:
    key = "date_%s" % stem
    want = '%s:"assets/story/locs/bg_159_%s.jpg"' % (key, stem)
    ck("§3 LOC_SHEET_BG[%s] 維持原路徑唔加 ?v=" % key, want in src)
ck("§3 SAVE key 不變", "starVolunteer_map_v19w" in src)
ck("§3 softRev 不變", "s107" in src)
ck("§3 產品 ?v= 不變", "v20a10" in src)

print("TOTAL %s" % ("PASS" if not fails else "FAIL %d: %s" % (len(fails), fails)))
sys.exit(0 if not fails else 1)
