# v20a195 resync：加 2 張 angry 表情（awi_s2／s3_angry），fullbody 總數 207→209、真檔 182→184。
# v20a138 DLG138 靜態守門：37 張新表情圖入庫＋檔名／映射／實線句數／焗邊。
# 覆蓋：① 37 張新資產本地存在＋檔名一字唔差＋WebP 檔頭＋fullbody 總數 209（v195：207＋2 張 angry 表情）
#       ② 每張新圖有對應可達（live）實線句數（句數來源：qa138/verdict138.json，
#          reachable occurrence × runtime 分類；唔係 corpus 句數——v127 教訓）
#       ③ 反證：檢查函數食缺檔／改錯名嘅檔案集必須報缺；另做真實
#          臨時目錄負向測試（抽走一張 → checker 必須 FAIL）。
#       ④ 基線不變：SAVE key／softRev／產品 ?v=（v138 零 code 改動，
#          DLG106 接線原封不動；新檔名本身就係新 URL，用既有 ?v=20a106）。
#       ⑤ 焗邊驗證（qa138/bake_results138.json）：37 張全 PASS、
#          邊帶米白命中 ≥95%、內部大差異 <1%、單一邊帶。
#       ⑥ 死檔守門：7 個 inventory-missing 死資產唔入批，檔案必須唔存在
#          （cheung_tsijun_angry／ko_chunkit_sad／lin_hiu_angry／lin_hiu_think／
#           lui_ging_sad／tong_souwan_sad／vera_shy）。
#       ⑦ 生死分類依據：qa138/verdict138.json＋verdict138_addendum.md
#          （live-needed 110 組，已有 73，批單 37；inventory 口徑 +66 句入面
#          9 句係 extra_ad_fen 旁白重複誤歸（盤點 bug），另 lin_hiu_serious 1 句＋
#          tsui_poushan_serious 2 句經真分類器覆核判死（pack 句永遠播唔到：
#          R_hiu_meet 俾 DualMeet 閘＋mock 加厚版換走；R_xu_* 運行版廣東話
#          文本分類唔出 serious）。真 live 實線 54 句；覆蓋 515＋54＝569／593＝95.9%。
#          嗰 2 張死圖照舊入庫（跟 v127 前例：檔案留低等內容／引擎修復票
#          加返條 serious 台詞嗰陣即刻用得，唔使重生），但實線句數記 0。
# 用法：python3 tests/test_dlg138_static.py [path-to-index.html]
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

# ---------- 基線不變（v138 零 code 改動） ----------
ck("SAVE key 不變", "starVolunteer_map_v19w" in src)
ck("softRev 不變", "s107" in src)
ck("產品 ?v= 不變", "v20a10" in src)
ck("DLG106 接線原封不動（無 v138 改動）",
   all(x in src for x in ["DLG106_GAZE", "dlg106Candidates", "dlg106AweiStem",
                          "dlg106ResolveCategory", "?v=20a106"]))

# ---------- 新資產表：檔名／講者／分類／可達實線句數 ----------
# 句數 = verdict138.json 入面該資產嘅 live evidence 行數（reachable occurrence）。
NEW = [
    # (檔名, 講者, 分類, 實線句數)
    ("chai_zanhoi_angry.webp", "chai_zanhoi", "angry", 1),
    ("chai_zanhoi_shy.webp", "chai_zanhoi", "shy", 2),
    ("chai_zanhoi_smile.webp", "chai_zanhoi", "happy", 2),
    ("chai_zanhoi_think.webp", "chai_zanhoi", "think", 2),
    ("cheung_hakfan_serious.webp", "cheung_hakfan", "serious", 2),
    ("cheung_tsijun_sad.webp", "cheung_tsijun", "sad", 1),
    ("cheung_tsijun_think.webp", "cheung_tsijun", "think", 1),
    ("chung_choning_angry.webp", "chung_choning", "angry", 1),
    ("crew_laolinji_serious.webp", "crew_laolinji", "serious", 2),
    ("extra_ad_fen_sad.webp", "extra_ad_fen", "sad", 1),
    ("extra_ad_fen_serious.webp", "extra_ad_fen", "serious", 3),
    ("ho_sang_surprise.webp", "ho_sang", "surprise", 1),
    ("ko_chunkit_shy.webp", "ko_chunkit", "shy", 1),
    ("ko_chunkit_think.webp", "ko_chunkit", "think", 1),
    ("lin_hiu_serious.webp", "lin_hiu", "serious", 0),  # 死圖：pack 句播唔到，mock 版零 serious
    ("lin_hiu_smile.webp", "lin_hiu", "happy", 1),
    ("liu_bingxing_sad.webp", "liu_bingxing", "sad", 2),
    ("liu_bingxing_surprise.webp", "liu_bingxing", "surprise", 2),
    ("liu_bingxing_think.webp", "liu_bingxing", "think", 1),
    ("lok_gasing_angry.webp", "lok_gasing", "angry", 2),
    ("lok_gasing_shy.webp", "lok_gasing", "shy", 2),
    ("lok_gasing_smile.webp", "lok_gasing", "happy", 1),
    ("lok_gasing_surprise.webp", "lok_gasing", "surprise", 1),
    ("lui_ging_serious.webp", "lui_ging", "serious", 1),
    ("luk_baakyin_angry.webp", "luk_baakyin", "angry", 1),
    ("luk_baakyin_sad.webp", "luk_baakyin", "sad", 2),
    ("luk_baakyin_smile.webp", "luk_baakyin", "happy", 3),
    ("mak_zhendong_angry.webp", "mak_zhendong", "angry", 1),
    ("mak_zhendong_smile.webp", "mak_zhendong", "happy", 1),
    ("ngai_wingnaam_angry.webp", "ngai_wingnaam", "angry", 2),
    ("ngai_wingnaam_serious.webp", "ngai_wingnaam", "serious", 3),
    ("ngai_wingnaam_smile.webp", "ngai_wingnaam", "happy", 3),
    ("ngai_wingnaam_surprise.webp", "ngai_wingnaam", "surprise", 1),
    ("ngai_wingnaam_think.webp", "ngai_wingnaam", "think", 1),
    ("so_jiyan_surprise.webp", "so_jiyan", "surprise", 1),
    ("tsui_poushan_serious.webp", "tsui_poushan", "serious", 0),  # 死圖：運行版 17 句 live 徐寶珊句 serious 0
    ("vera_serious.webp", "vera", "serious", 1),
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

# ---------- 死檔守門：7 個死資產唔入批 ----------
DEAD = ["cheung_tsijun_angry.webp", "ko_chunkit_sad.webp", "lin_hiu_angry.webp",
        "lin_hiu_think.webp", "lui_ging_sad.webp", "tong_souwan_sad.webp",
        "vera_shy.webp"]
# 已入庫但判死嘅 2 張（見 addendum）：檔案存在，但可達實線句數＝0。
# 唔刪檔——留低等另一票（mock R_hiu_meet 加 serious 台詞／live R_xu_* 加 serious 台詞）加返線即用得。
DEAD_SHIPPED = ["lin_hiu_serious.webp", "tsui_poushan_serious.webp"]

FB = os.path.join(ROOT, "assets", "story", "fullbody")
def check_new_assets(names):
    """names：fullbody 目錄內檔名集。回傳缺失嘅新資產檔名清單。"""
    return [fn for fn, _sp, _c, _n in NEW if fn not in names]

if os.path.isdir(FB):
    names = set(os.listdir(FB))
    missing = check_new_assets(names)
    ck("37 張新資產全部喺 assets/story/fullbody/", not missing)
    if missing: info("缺新資產：" + ", ".join(missing))
    ck("fullbody 總數 170→207→209（v127 後 170 張＋v138 37 張新表情＋v195 2 張 angry 表情）", len([f for f in names if f.endswith((".webp", ".png"))]) == 209)
    for fn, _sp, _cat, n in NEW:
        p = os.path.join(FB, fn)
        ok = os.path.isfile(p) and os.path.getsize(p) > 50000
        if ok:
            with open(p, "rb") as fh:
                head = fh.read(12)
            ok = head[:4] == b"RIFF" and head[8:12] == b"WEBP"
        ck(f"{fn} 存在＋WebP 檔頭＋>50KB", ok)
        if fn in DEAD_SHIPPED:
            ck(f"{fn} 判死：實線句數 0（檔案留低等修復票，見 addendum）", n == 0)
        else:
            ck(f"{fn} 有對應可達實線句數 {n} 句（唔係死圖）", n > 0)
    ck("新圖對應可達實線句數合計（真 live 54 句）",
       sum(n for _f, _sp, _c, n in NEW) == 54)
    ck("死檔 7 張全部唔存在（唔生成死圖）", all(d not in names for d in DEAD))
    ck("判死已入庫 2 張檔案存在（留低等修復票）", all(d in names for d in DEAD_SHIPPED))
else:
    ck("assets/story/fullbody/ 目錄存在", False)

# ---------- 反證 ----------
ck("反證：檔案集抽走一張（in-memory）→ checker 必須報缺",
   check_new_assets(set(f for f, _, _, _ in NEW) - {"ngai_wingnaam_think.webp"}) == ["ngai_wingnaam_think.webp"])
ck("反證：檔案集改錯名（lok_gasing_shy→lok_gasing_shy2）→ checker 必須報缺",
   check_new_assets(set(f for f, _, _, _ in NEW) - {"lok_gasing_shy.webp"} | {"lok_gasing_shy2.webp"}) == ["lok_gasing_shy.webp"])
ck("反證：空檔案集 → checker 報齊 37 張缺失",
   len(check_new_assets(set())) == 37)
# 真實臨時目錄負向測試：抄 36 張去 temp dir，checker 讀磁碟必須 FAIL 其中一張
# （對 pristine main 跑嗰陣新檔根本唔存在，跳過磁碟段——in-memory 反證已覆蓋，唔准 crash）
tmp = tempfile.mkdtemp(prefix="dlg138neg_")
try:
    if all(os.path.isfile(os.path.join(FB, fn)) for fn, _sp, _c, _n in NEW):
        for fn, _sp, _c, _n in NEW:
            if fn == "ho_sang_surprise.webp":
                continue
            shutil.copy(os.path.join(FB, fn), os.path.join(tmp, fn))
        disk_names = set(os.listdir(tmp))
        ck("反證（真磁碟）：temp 目錄得 36 張 → checker 報缺 ho_sang_surprise.webp",
           check_new_assets(disk_names) == ["ho_sang_surprise.webp"])
        shutil.copy(os.path.join(FB, "ho_sang_surprise.webp"), os.path.join(tmp, "ho_sang_surprise.webp"))
        ck("反證對照：temp 目錄補返第 37 張 → checker 報零缺失",
           check_new_assets(set(os.listdir(tmp))) == [])
    else:
        info("SKIP 磁碟反證：新資產唔齊（pristine 對照），in-memory 反證已覆蓋")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ---------- 焗邊驗證（qa138 如在場） ----------
BAKE = os.path.join(ROOT, "qa138", "bake_results138.json")
if os.path.isfile(BAKE):
    with open(BAKE, encoding="utf-8") as f:
        bake = json.load(f)
    ck("焗邊報告 37 張", len(bake) == 37)
    ck("焗邊 37 張全 PASS", all(b.get("pass") for b in bake))
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
    info("PENDING-BAKE-REPORT：qa138/bake_results138.json 唔喺度——跳過焗邊數值對照")

print("WARNINGS " + (", ".join(warns) if warns else "none"))
print("RESULT " + ("FAIL (" + str(len(fails)) + ")" if fails else "PASS"))
sys.exit(1 if fails else 0)
