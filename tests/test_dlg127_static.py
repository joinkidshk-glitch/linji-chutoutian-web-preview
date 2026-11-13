# v20a195 resync：加 2 張 angry 表情（awi_s2／s3_angry），fullbody 總數 207→209、真檔 182→184。
# v20a127 DLG127 靜態守門：22 張新表情圖入庫＋檔名／映射／句數／焗邊。
# 覆蓋：① 22 張新資產本地存在＋檔名一字唔差＋WebP 檔頭＋fullbody 總數 170
#       ② 每張新圖有對應分類句數（句數來源：
#          linji-expression-inventory/work/lines_classified.json 2644 行，
#          同 qa127/coverage127.py 計法一致；此檔將期望值寫死做常數，
#          coverage 腳本重計對唔上會喺 qa127 先 FAIL）
#       ③ 反證：檢查函數食缺檔／改錯名嘅檔案集必須報缺；另做真實
#          臨時目錄負向測試（抽走一張 → checker 必須 FAIL）。
#       ④ 基線不變：SAVE key／softRev／產品 ?v=（v127 零 code 改動，
#          DLG106 接線原封不動；新檔名本身就係新 URL，用既有 ?v=20a106）。
#       ⑤ 焗邊驗證（qa127/bake_results127.json）：22 張全 PASS、
#          邊帶米白命中 ≥95%、內部大差異 <1%、單一邊帶。
#       ⑥ 標籤更正守門：chow_choiyi 係周采兒（唔係周刊編輯）、阿金叔 id 係
#          uncle_kim（唔係 kam_uncle）——新資產檔名用正確 id。
# 用法：python3 tests/test_dlg127_static.py [path-to-index.html]
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

# ---------- 基線不變（v127 零 code 改動） ----------
ck("SAVE key 不變", "starVolunteer_map_v19w" in src)
ck("softRev 不變", "s107" in src)
ck("產品 ?v= 不變", "v20a10" in src)
ck("DLG106 接線原封不動（無 v127 改動）",
   all(x in src for x in ["DLG106_GAZE", "dlg106Candidates", "dlg106AweiStem",
                          "dlg106ResolveCategory", "?v=20a106"]))

# ---------- 新資產表：檔名／講者／分類／對應句數 ----------
# 句數 = lines_classified.json 入面該講者該分類嘅行數（qa127/coverage127.py 重計核實）。
NEW = [
    # (檔名, 講者, 分類, 句數)
    ("gu_mingfai_shy.webp", "gu_mingfai", "shy", 3),
    ("gu_mingfai_angry.webp", "gu_mingfai", "angry", 1),
    ("gu_mingfai_think.webp", "gu_mingfai", "think", 1),
    ("pang_siuki_sad.webp", "pang_siuki", "sad", 3),
    ("chow_choiyi_sad.webp", "chow_choiyi", "sad", 3),
    ("chow_choiyi_angry.webp", "chow_choiyi", "angry", 2),
    ("yip_manji_surprise.webp", "yip_manji", "surprise", 2),
    ("yip_manji_angry.webp", "yip_manji", "angry", 2),
    ("yip_manji_shy.webp", "yip_manji", "shy", 1),
    ("ching_tinlok_shy.webp", "ching_tinlok", "shy", 1),
    ("ching_tinlok_surprise.webp", "ching_tinlok", "surprise", 1),
    ("ching_tinlok_think.webp", "ching_tinlok", "think", 1),
    ("lan_ruoxi_serious.webp", "lan_ruoxi", "serious", 1),
    ("lan_ruoxi_think.webp", "lan_ruoxi", "think", 1),
    ("fong_siulung_sad.webp", "fong_siulung", "sad", 2),
    ("fong_siulung_angry.webp", "fong_siulung", "angry", 1),
    ("cheng_william_serious.webp", "cheng_william", "serious", 1),
    ("cheng_william_shy.webp", "cheng_william", "shy", 1),
    ("kwan_hoimei_serious.webp", "kwan_hoimei", "serious", 1),
    ("mok_siufai_sad.webp", "mok_siufai", "sad", 1),
    ("uncle_kim_smile.webp", "uncle_kim", "happy", 1),
    ("uncle_kim_serious.webp", "uncle_kim", "serious", 1),
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

# ---------- 標籤更正守門 ----------
ck("chow_choiyi 註冊 display 係「周采兒」（唔係周刊編輯；周刊編輯行 shadow_male）",
   'chow_choiyi: { artId:"char_chow", portraitsKey:"npc_chow", display:"周采兒" }' in src
   and '"周刊編輯":"shadow_male"' in src)
ck("阿金叔 speaker id 係 uncle_kim（kam_uncle 唔存在）",
   "uncle_kim" in src and "kam_uncle" not in src)

FB = os.path.join(ROOT, "assets", "story", "fullbody")
def check_new_assets(names):
    """names：fullbody 目錄內檔名集。回傳缺失嘅新資產檔名清單。"""
    return [fn for fn, _sp, _c, _n in NEW if fn not in names]

if os.path.isdir(FB):
    names = set(os.listdir(FB))
    missing = check_new_assets(names)
    ck("22 張新資產全部喺 assets/story/fullbody/", not missing)
    if missing: info("缺新資產：" + ", ".join(missing))
    ck("fullbody 總數 148→170→207→209（v131 後 148 張＋v127 22 張新表情＋v138 37 張新表情＋v195 2 張 angry 表情）", len([f for f in names if f.endswith((".webp", ".png"))]) == 209)
    for fn, _sp, _cat, n in NEW:
        p = os.path.join(FB, fn)
        ok = os.path.isfile(p) and os.path.getsize(p) > 50000
        if ok:
            with open(p, "rb") as fh:
                head = fh.read(12)
            ok = head[:4] == b"RIFF" and head[8:12] == b"WEBP"
        ck(f"{fn} 存在＋WebP 檔頭＋>50KB", ok)
        ck(f"{fn} 有對應分類句數 {n} 句（唔係死圖）", n > 0)
    ck("新圖對應句數合計（全局升幅 32 句）",
       sum(n for _f, _sp, _c, n in NEW) == 32)
else:
    ck("assets/story/fullbody/ 目錄存在", False)

# ---------- 反證 ----------
ck("反證：檔案集抽走一張（in-memory）→ checker 必須報缺",
   check_new_assets(set(f for f, _, _, _ in NEW) - {"ching_tinlok_think.webp"}) == ["ching_tinlok_think.webp"])
ck("反證：檔案集改錯名（lan_ruoxi_think→lan_ruoxi_think2）→ checker 必須報缺",
   check_new_assets(set(f for f, _, _, _ in NEW) - {"lan_ruoxi_think.webp"} | {"lan_ruoxi_think2.webp"}) == ["lan_ruoxi_think.webp"])
ck("反證：空檔案集 → checker 報齊 22 張缺失",
   len(check_new_assets(set())) == 22)
# 真實臨時目錄負向測試：抄 21 張去 temp dir，checker 讀磁碟必須 FAIL 其中一張
# （對 pristine main 跑嗰陣新檔根本唔存在，跳過磁碟段——in-memory 反證已覆蓋，唔准 crash）
tmp = tempfile.mkdtemp(prefix="dlg127neg_")
try:
    if all(os.path.isfile(os.path.join(FB, fn)) for fn, _sp, _c, _n in NEW):
        for fn, _sp, _c, _n in NEW:
            if fn == "uncle_kim_serious.webp":
                continue
            shutil.copy(os.path.join(FB, fn), os.path.join(tmp, fn))
        disk_names = set(os.listdir(tmp))
        ck("反證（真磁碟）：temp 目錄得 21 張 → checker 報缺 uncle_kim_serious.webp",
           check_new_assets(disk_names) == ["uncle_kim_serious.webp"])
        shutil.copy(os.path.join(FB, "uncle_kim_serious.webp"), os.path.join(tmp, "uncle_kim_serious.webp"))
        ck("反證對照：temp 目錄補返第 22 張 → checker 報零缺失",
           check_new_assets(set(os.listdir(tmp))) == [])
    else:
        info("SKIP 磁碟反證：新資產唔齊（pristine 對照），in-memory 反證已覆蓋")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ---------- 焗邊驗證（qa127 如在場） ----------
BAKE = os.path.join(ROOT, "qa127", "bake_results127.json")
if os.path.isfile(BAKE):
    with open(BAKE, encoding="utf-8") as f:
        bake = json.load(f)
    ck("焗邊報告 22 張", len(bake) == 22)
    ck("焗邊 22 張全 PASS", all(b.get("pass") for b in bake))
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
    info("PENDING-BAKE-REPORT：qa127/bake_results127.json 唔喺度——跳過焗邊數值對照")

print("WARNINGS " + (", ".join(warns) if warns else "none"))
print("RESULT " + ("FAIL (" + str(len(fails)) + ")" if fails else "PASS"))
sys.exit(1 if fails else 0)
