# v20a123 DLG123 靜態守門：12 張新表情圖入庫＋檔名／映射／句數／焗邊。
# 覆蓋：① 12 張新資產本地存在＋檔名一字唔差＋WebP 檔頭＋fullbody 總數 130
#       ② 每張新圖有對應分類句數（句數來源：
#          linji-expression-inventory/work/lines_classified.json 2644 行，
#          同 qa123/coverage123.py 計法一致；此檔將期望值寫死做常數，
#          coverage 腳本重計對唔上會喺 qa123 先 FAIL）
#       ③ 反證：檢查函數食缺檔／改錯名嘅檔案集必須報缺；另做真實
#          臨時目錄負向測試（抽走一張 → checker 必須 FAIL）。
#       ④ 基線不變：SAVE key／softRev／產品 ?v=（v123 零 code 改動，
#          DLG106 接線原封不動；新檔名本身就係新 URL，用既有 ?v=20a106）。
#       ⑤ 焗邊驗證（qa123/bake_results123.json）：12 張全 PASS、
#          邊帶米白命中 ≥95%、內部大差異 <1%、單一邊帶。
# 用法：python3 tests/test_dlg123_static.py [path-to-index.html]
import json, os, re, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "..", "index.html")
ROOT = os.path.dirname(IDX)
with open(IDX, encoding="utf-8") as f:
    src = f.read()

fails, warns = [], []
def ck(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond: fails.append(name)
def info(msg): print("INFO " + msg)

# ---------- 基線不變（v123 零 code 改動） ----------
ck("SAVE key 不變", "starVolunteer_map_v19w" in src)
ck("softRev 不變", "s107" in src)
ck("產品 ?v= 不變", "v20a10" in src)
ck("DLG106 接線原封不動（無 v123 改動）",
   all(x in src for x in ["DLG106_GAZE", "dlg106Candidates", "dlg106AweiStem",
                          "dlg106ResolveCategory", "?v=20a106"]))

# ---------- 新資產表：檔名／講者／分類／對應句數 ----------
# 句數 = lines_classified.json 入面該講者該分類嘅行數（qa123/coverage123.py 重計核實）。
NEW = [
    # (檔名, 講者, 分類, 句數)
    ("awi_s2_surprise.webp", "awi_s2", "surprise", 27),
    ("awi_s2_sad.webp", "awi_s2", "sad", 20),
    ("awi_s2_shy.webp", "awi_s2", "shy", 14),
    ("awi_s3_surprise.webp", "awi_s3", "surprise", 27),
    ("awi_s3_sad.webp", "awi_s3", "sad", 20),
    ("awi_s3_shy.webp", "awi_s3", "shy", 14),
    ("awi_angry.webp", "awi", "angry", 4),
    ("chung_choning_think.webp", "chung_choning", "think", 4),
    ("chung_choning_smile.webp", "chung_choning", "happy", 3),
    ("ho_sang_angry.webp", "ho_sang", "angry", 4),
    ("liu_bingxing_shy.webp", "liu_bingxing", "shy", 2),
    ("pang_siuki_surprise.webp", "pang_siuki", "surprise", 2),
]
CAT2EXPR = {"happy": "smile", "neutral": "base", "serious": "serious",
            "sad": "sad", "surprise": "surprise", "shy": "shy",
            "think": "think", "angry": "angry"}

# 檔名必須跟「講者_表情」規則：分類→表情映射要同 index.html 內 DLG106_CAT_TO_EXPR 一致
m = re.search(r"const DLG106_CAT_TO_EXPR = \{([^}]*)\}", src)
ck("搵到 DLG106_CAT_TO_EXPR", bool(m))
if m:
    live_map = dict(re.findall(r"(\w+):\"(\w+)\"", m.group(1)))
    for fn, sp, cat, _n in NEW:
        ck(f"映射 {cat}→{CAT2EXPR[cat]} 同內嵌表一致",
           live_map.get(cat) == CAT2EXPR[cat])
        ck(f"檔名 {fn}＝講者_{CAT2EXPR[cat]}",
           fn == f"{sp}_{CAT2EXPR[cat]}.webp")

FB = os.path.join(ROOT, "assets", "story", "fullbody")
def check_new_assets(names):
    """names：fullbody 目錄內檔名集。回傳缺失嘅新資產檔名清單。"""
    return [fn for fn, _sp, _c, _n in NEW if fn not in names]

if os.path.isdir(FB):
    names = set(os.listdir(FB))
    missing = check_new_assets(names)
    ck("12 張新資產全部喺 assets/story/fullbody/", not missing)
    if missing: info("缺新資產：" + ", ".join(missing))
    ck("fullbody 總數 128→140→146（v119 後 128 張＋v123 12 張新表情＋v126 6 張新表情）", len([f for f in names if f.endswith((".webp", ".png"))]) == 146)
    for fn, _sp, _cat, n in NEW:
        p = os.path.join(FB, fn)
        ok = os.path.isfile(p) and os.path.getsize(p) > 50000
        if ok:
            with open(p, "rb") as fh:
                head = fh.read(12)
            ok = head[:4] == b"RIFF" and head[8:12] == b"WEBP"
        ck(f"{fn} 存在＋WebP 檔頭＋>50KB", ok)
        ck(f"{fn} 有對應分類句數 {n} 句（唔係死圖）", n > 0)
    ck("新圖對應句數合計（全局升幅 19 句：4+4+3+4+2+2；awi s2/s3 各 61 句計階段，唔計入全局）",
       sum(n for _f, sp, _c, n in NEW if not sp.startswith("awi_")) == 19)
else:
    ck("assets/story/fullbody/ 目錄存在", False)

# ---------- 反證 ----------
ck("反證：檔案集抽走一張（in-memory）→ checker 必須報缺",
   check_new_assets(set(f for f, _, _, _ in NEW) - {"ho_sang_angry.webp"}) == ["ho_sang_angry.webp"])
ck("反證：檔案集改錯名（pang_siuki_surprise→pang_siuki_surprise2）→ checker 必須報缺",
   check_new_assets(set(f for f, _, _, _ in NEW) - {"pang_siuki_surprise.webp"} | {"pang_siuki_surprise2.webp"}) == ["pang_siuki_surprise.webp"])
ck("反證：空檔案集 → checker 報齊 12 張缺失",
   len(check_new_assets(set())) == 12)
# 真實臨時目錄負向測試：抄 11 張去 temp dir，checker 讀磁碟必須 FAIL 其中一張
tmp = tempfile.mkdtemp(prefix="dlg123neg_")
try:
    for fn, _sp, _c, _n in NEW:
        if fn == "liu_bingxing_shy.webp":
            continue
        shutil.copy(os.path.join(FB, fn), os.path.join(tmp, fn))
    disk_names = set(os.listdir(tmp))
    ck("反證（真磁碟）：temp 目錄得 11 張 → checker 報缺 liu_bingxing_shy.webp",
       check_new_assets(disk_names) == ["liu_bingxing_shy.webp"])
    shutil.copy(os.path.join(FB, "liu_bingxing_shy.webp"), os.path.join(tmp, "liu_bingxing_shy.webp"))
    ck("反證對照：temp 目錄補返第 12 張 → checker 報零缺失",
       check_new_assets(set(os.listdir(tmp))) == [])
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ---------- 焗邊驗證（qa123 如在場） ----------
BAKE = os.path.join(ROOT, "qa123", "bake_results123.json")
if os.path.isfile(BAKE):
    with open(BAKE, encoding="utf-8") as f:
        bake = json.load(f)
    ck("焗邊報告 12 張", len(bake) == 12)
    ck("焗邊 12 張全 PASS", all(b.get("pass") for b in bake))
    ck("焗邊：邊帶米白命中全部 ≥95%",
       all(b.get("edge_color_frac", 0) >= 0.95 for b in bake))
    ck("焗邊：內部大差異全部 <1%",
       all(b.get("interior_bigdiff_frac", 1) < 0.01 for b in bake))
    ck("焗邊：單一邊帶（far_cream_px 全部 0，唔准兩重邊）",
       all(b.get("far_cream_px", -1) == 0 for b in bake))
    ck("焗邊：尺寸全部＝原圖+2r",
       all(b.get("size_ok") for b in bake))
else:
    warns.append("BAKE_REPORT_MISSING")
    info("PENDING-BAKE-REPORT：qa123/bake_results123.json 唔喺度——跳過焗邊數值對照")

print("WARNINGS " + (", ".join(warns) if warns else "none"))
print("RESULT " + ("FAIL (" + str(len(fails)) + ")" if fails else "PASS"))
sys.exit(1 if fails else 0)
