# v20a106 DLG106 靜態守門：基線字串不變 / DLG106 接線齊全 / 視線表×資產名冊一致 /
# 資產檔案存在（工人 A 未交付時出 PENDING，唔冒充 PASS；入庫後缺檔即 FAIL）/
# C 交付物（gaze 表＋emotion map）同 index.html 內嵌版逐條一致 / 反證自檢。
# 用法：python3 tests/test_dlg106_static.py [path-to-index.html]
import json, os, re, sys

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

# ---------- 基線不變 ----------
ck("SAVE key 不變", "starVolunteer_map_v19w" in src)
ck("softRev 不變", "s107" in src)
ck("產品 ?v= 不變", "v20a10" in src)

# ---------- DLG106 接線 ----------
def wiring_ok(s):
    return all(x in s for x in [
        "DLG106_GAZE", "DLG106_EMOTION_MAP", "dlg106ResolveSides", "dlg106ResolveCategory",
        "dlg106Candidates", "dlg106Classify", "dlg106Lookup", "spDlgCharsHtml", "dlg106-on",
        "dlg106-plate", "paintDlg106", "e79-char-l", "?v=20a106",
    ])
ck("DLG106 接線齊全（模組＋主線分支＋巧遇分支＋新資產版本）", wiring_ok(src))
ck("反證：整爛接線（DLG106_GAZE 改名）後 wiring_ok 必須轉 False（predicate 係 live）",
   not wiring_ok(src.replace("DLG106_GAZE", "DLG106_G0NE")))
i = src.find(".dlg106-char{")
seg = src[i:i + 420] if i >= 0 else ""
ck("舞台人物高 60%（v20a108 取代 50%：--dlg108-char-h，自動收細）＋filter 過渡 250ms", "height:var(--dlg108-char-h,60%)" in seg and "250ms" in seg)
ck("聽者 0.6／電話 0.8 規格喺呈現碼入面", "0.6" in src and "0.8" in src and "dlg106-phone" in src)
ck("圖載入失敗後備鏈（__dlg106Err＋data-dlg-fallbacks）", "__dlg106Err" in src and "data-dlg-fallbacks" in src)

# 解析次序：emotion 欄 → map lookup → classifier
r0 = src.find("function dlg106ResolveCategory")
body = src[r0:r0 + 1200] if r0 >= 0 else ""
p_field = body.find("src.emotion")
p_map = body.find("dlg106Lookup")
p_cls = body.find("dlg106Classify(src.text")
ck("情緒解析次序 欄→map→分類器", 0 <= p_field < p_map < p_cls)

# ---------- 內嵌表抽取（同 C 交付逐條對照） ----------
def extract_json_after(marker):
    j = src.index(marker)
    k = src.index("{", j)
    depth, end = 0, k
    in_str = False
    esc = False
    for n in range(k, len(src)):
        ch = src[n]
        if in_str:
            if esc: esc = False
            elif ch == "\\": esc = True
            elif ch == '"': in_str = False
        else:
            if ch == '"': in_str = True
            elif ch == "{": depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0: end = n + 1; break
    return json.loads(src[k:end])

gaze = extract_json_after("const DLG106_GAZE =")
emap = extract_json_after("const DLG106_EMOTION_MAP =")
ck("視線表 39 條（34＋v20a119 DLG119 5 鍵：shadow_male／shadow_female／shadow_elder／crew_laolinji／generic_cinema_asst）", len(gaze) == 39)
ck("emotion map 584 條", len(emap) == 584)

HAND = os.path.join(ROOT, "handoff106")
if os.path.isdir(HAND):
    with open(os.path.join(HAND, "gaze_table.json"), encoding="utf-8") as f:
        ck("視線表同 handoff gaze_table.json 逐條一致", gaze == json.load(f))
    with open(os.path.join(HAND, "emotion_map_embed.json"), encoding="utf-8") as f:
        ck("emotion map 同 handoff 逐條一致", emap == json.load(f)["map"])
else:
    info("handoff106/ 唔喺 work copy（可能已清理）——跳過逐條對照，淨驗內嵌表規模")

ROSTER = [k for k in gaze if k not in ("awi_s2", "awi_s3")]
ck("名冊 37 角（39 減 awi 兩階段）", len(ROSTER) == 37)
ck("extra_ad_fen 喺名冊入面", "extra_ad_fen" in ROSTER)
ck("DLG119 5 鍵喺名冊入面",
   all(k in ROSTER for k in ("shadow_male", "shadow_female", "shadow_elder", "crew_laolinji", "generic_cinema_asst")))
ck("DLG119 影鍵全部 front＋唔翻得（邊光永遠右側）",
   all(gaze[k]["gaze"] == "front" and gaze[k]["flipSafe"] is False
       for k in ("shadow_male", "shadow_female", "shadow_elder", "generic_cinema_asst")))
ck("老臨記 front＋唔翻得（右手持杯＋左胸袋，實圖量度）",
   gaze["crew_laolinji"]["gaze"] == "front" and gaze["crew_laolinji"]["flipSafe"] is False)
ck("視線表每角都有合法 gaze 同 flipSafe bool",
   all(v.get("gaze") in ("left", "right", "front") and isinstance(v.get("flipSafe"), bool) for v in gaze.values()))

# ---------- 資產存在（A 交付狀態感知） ----------
FB = os.path.join(ROOT, "assets", "story", "fullbody")
STEMS = ROSTER + ["awi_s2", "awi_s3"]  # ROSTER 已含 awi（s1）
if not os.path.isdir(FB):
    warns.append("ASSETS_PENDING")
    info("PENDING-ASSETS：assets/story/fullbody/ 未存在——資產工人 A 未交付，"
         "88 張焗邊圖未入庫；本節只申報唔 FAIL。入庫後重跑本測試，缺檔即 FAIL。")
else:
    # v20a119 DLG119：generic_cinema_asst 係別名鍵，圖走 shadow_male（唔係自己 stem 嘅 base 檔）。
    STEM_ALIAS = {"generic_cinema_asst": "shadow_male"}
    missing = []
    for stem in STEMS:
        disk = STEM_ALIAS.get(stem, stem)
        if not (os.path.isfile(os.path.join(FB, disk + "_base.webp")) or os.path.isfile(os.path.join(FB, disk + "_base.png"))):
            missing.append(stem + "_base")
    ck("名冊 37 角＋阿偉 s2/s3 全部有 fullbody base 資產（generic_cinema_asst 計 shadow_male 別名）", not missing)
    if missing: info("缺 base 資產：" + ", ".join(missing))
    nfiles = len([f for f in os.listdir(FB) if f.endswith((".webp", ".png"))])
    info("fullbody 資產檔數：" + str(nfiles))

# 名冊外豁免（功能 NPC：行舊呈現 bust/剪影/無圖，按規格喺交代列明）
# v20a119 DLG119：generic_cinema_asst 已入名冊（別名鍵），唔再豁免；其餘 9 個舊 id
# 只留 REG 條目做後備（LEGACY 已經唔再指去佢哋），名冊外豁免維持。
EXEMPT = ["generic_crew", "generic_date", "generic_mag_editor",
          "extra_lan_father", "extra_ad_ling", "extra_ad_sam", "extra_dir_luk",
          "extra_prod_chow", "extra_unknown"]
info("名冊外豁免 speaker（無全身資產、行舊呈現）：" + ", ".join(EXEMPT))
ck("豁免名單同名冊冇交集（唔會誤豁免有名冊嘅角）", not (set(EXEMPT) & set(ROSTER)))

print("WARNINGS " + (", ".join(warns) if warns else "none"))
print("RESULT " + ("FAIL (" + str(len(fails)) + ")" if fails else "PASS"))
sys.exit(1 if fails else 0)
