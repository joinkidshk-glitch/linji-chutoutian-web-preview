# v20a119 DLG119 靜態守門：無名角色剪影接入（男／女／老年影＋老臨記有面）。
# 覆蓋：① 38 個顯示名逐名解像（LEGACY→影 id／老臨記 id→GAZE 有鍵→磁碟檔存在）
#       ② 「週刊編輯」／「周刊編輯」兩寫法 ③ 院線助理顯式 speakerId 嗰句（PUSH 檔）
#       ④ 同影去重（spDlgPairIds 兩條 return 路都行 dlg119DedupePair）
#       ⑤ 聽者影用 _dim 版＋唔加 0.60 filter（source 斷言）⑥ 影圖缺失 fallback 黑卡
#       ⑦ 副導演芬姐唔受影響 ⑧ 何生／阿偉等 ①級不變 ⑨ generic_crew 其他用途不變
#       ⑩ SAVE key／softRev／產品 ?v= 不變 ⑪ fullbody 總數 128
# 反證：(a) 檔案集抽走一張 → checker 報缺；(b) 映射改錯／刪走 → checker 報錯；
#       (c) 成個測試對 pristine main index.html 跑必須 FAIL（見 handoff，唔喺呢檔入面跑）。
# 用法：python3 tests/test_dlg119_static.py [path-to-index.html]
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

# ---------- 抽表 ----------
def strip_js_comments(s):
    """刪走 JS 註解（/* */ 同 // 行尾），唔郁字串入面嘅內容。SP_SPEAKER_LEGACY
       內嵌咗 v20a119 段註解，唔剝就 json.loads 唔到。"""
    out, i, n = [], 0, len(s)
    in_str = False
    while i < n:
        ch = s[i]
        if in_str:
            out.append(ch)
            if ch == "\\" and i + 1 < n:
                out.append(s[i + 1]); i += 2; continue
            if ch == '"': in_str = False
            i += 1; continue
        if ch == '"':
            in_str = True; out.append(ch); i += 1; continue
        if ch == "/" and i + 1 < n and s[i + 1] == "*":
            j = s.find("*/", i + 2)
            i = n if j < 0 else j + 2; continue
        if ch == "/" and i + 1 < n and s[i + 1] == "/":
            j = s.find("\n", i + 2)
            i = n if j < 0 else j; continue
        out.append(ch); i += 1
    return "".join(out)

def extract_json_after(marker):
    k = src.find(marker)
    if k < 0: return None
    k = src.find("{", k)
    depth, in_str, esc, end = 0, False, False, None
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
    return json.loads(strip_js_comments(src[k:end]))

gaze = extract_json_after("const DLG106_GAZE =")
legacy = extract_json_after("const SP_SPEAKER_LEGACY =")
scale = extract_json_after("const DLG109_HEIGHT_SCALE =")
ck("搵到 DLG106_GAZE／SP_SPEAKER_LEGACY／DLG109_HEIGHT_SCALE",
   gaze is not None and legacy is not None and scale is not None)
ck("GAZE 39 鍵", gaze is not None and len(gaze) == 39)

# ---------- 38 名對照表（任務書逐名跟；昌叔預設影、場務預設男、約會對象預設女影） ----------
EXPECTED = {}
EXPECTED["crew_laolinji"] = ["老臨記"]
EXPECTED["shadow_elder"] = ["老武師"]
EXPECTED["shadow_female"] = ["助導阿玲", "場務姐姐", "服裝助手", "茶水阿姐", "飯堂阿姐",
                             "阿媽", "約會對象", "歌迷阿妹", "佳麗"]
EXPECTED["shadow_male"] = ["副導演", "副導", "處境劇副導", "電影組副導", "助導", "助導阿森",
                           "場務", "後台場務", "老場務", "場務大佬根叔", "導演", "選角導演",
                           "導演陸志明", "監製", "監製周世昌", "藍父", "院線助理", "唱片公司職員",
                           "武指", "周刊編輯", "週刊記者", "高仔", "老臨記昌叔",
                           "茶餐廳伙記", "酒廊伙記", "編劇阿昌", "保安"]
ALL38 = [d for v in EXPECTED.values() for d in v]
ck("對照表 38 名（27 男＋9 女＋1 老年＋1 老臨記）", len(ALL38) == 38
   and len(EXPECTED["shadow_male"]) == 27 and len(EXPECTED["shadow_female"]) == 9)

# ---------- ① 逐名解像 ----------
FB = os.path.join(ROOT, "assets", "story", "fullbody")
def check_mapping(leg, gz, fb_dir):
    """回傳問題清單（空＝全過）。供反證餵變異輸入。"""
    probs = []
    for sid, names in EXPECTED.items():
        for d in names:
            if leg.get(d) != sid:
                probs.append(f"LEGACY[{d}]={leg.get(d)}，預期 {sid}")
                continue
            if sid not in gz:
                probs.append(f"GAZE 缺 {sid}（{d}）")
                continue
            stem = "shadow_male" if sid == "generic_cinema_asst" else sid
            for fn in ([f"{stem}_base.webp"] if sid == "crew_laolinji" else
                       [f"{stem}_base.webp", f"{stem}_dim_base.webp", f"{stem}_halo.png"]):
                if not os.path.isfile(os.path.join(fb_dir, fn)):
                    probs.append(f"缺檔 {fn}（{d}）")
    if leg.get("週刊編輯") != "shadow_male":
        probs.append("別名「週刊編輯」唔係男影")
    return probs

probs = check_mapping(legacy or {}, gaze or {}, FB)
ck("38 名逐名解像全過（LEGACY→影 id／老臨記 id→GAZE 有鍵→磁碟檔存在）", not probs)
if probs: info("解像問題：" + "；".join(probs[:10]))

# 盤點 CSV 對照（如在場）：③級顯示名集必須同呢 38 名一致
AUDIT_CSV = os.path.abspath(os.path.join(ROOT, "..", "linji-noportrait-audit", "speakers_by_display.csv"))
if os.path.isfile(AUDIT_CSV):
    import csv as _csv
    with open(AUDIT_CSV, encoding="utf-8") as f:
        rows = list(_csv.DictReader(f))
    l3 = sorted(r["display"] for r in rows if r["level"] == "3")
    ck("盤點 CSV ③級 38 名同對照表一致", sorted(ALL38) == l3)
    if sorted(ALL38) != l3:
        info("CSV 有、對照表冇：" + str(sorted(set(l3) - set(ALL38))))
        info("對照表有、CSV 冇：" + str(sorted(set(ALL38) - set(l3))))
else:
    info("盤點 CSV 唔喺度——跳過 ③級對照")

# ---------- ② 兩寫法 ----------
ck("「周刊編輯」／「週刊編輯」兩寫法都解到男影",
   legacy.get("周刊編輯") == "shadow_male" and legacy.get("週刊編輯") == "shadow_male")

# ---------- ③ 院線助理顯式 speakerId ----------
ck("DLG119_SHADOW_STEM 有 generic_cinema_asst→shadow_male 別名",
   bool(re.search(r'"generic_cinema_asst":\s*"shadow_male"', src)))
ck("GAZE 有 generic_cinema_asst 鍵（顯式 id 行新版舞台）",
   gaze is not None and "generic_cinema_asst" in gaze)
ck("generic_cinema_asst GAZE front＋唔翻得",
   gaze is not None and gaze.get("generic_cinema_asst", {}).get("gaze") == "front"
   and gaze.get("generic_cinema_asst", {}).get("flipSafe") is False)
push = os.path.join(ROOT, "content", "MOCK_STORY_DENG_LINE_PUSH_SOFT_v1.json")
if os.path.isfile(push):
    with open(push, encoding="utf-8") as f:
        push_src = f.read()
    ck("PUSH 檔有 1 句顯式 speakerId generic_cinema_asst（LEGACY 改唔到嗰句）",
       push_src.count('"speakerId": "generic_cinema_asst"') == 1)
    ck("content 全庫顯式 generic_cinema_asst 只有呢 1 句（唔會漏網）",
       sum(open(os.path.join(ROOT, "content", fn), encoding="utf-8").read().count('"speakerId": "generic_cinema_asst"')
           for fn in os.listdir(os.path.join(ROOT, "content")) if fn.endswith(".json")) == 1)

# ---------- ④ 同影去重 ----------
ck("spDlgPairIds 旁白路行 dlg119DedupePair",
   "return dlg119DedupePair(order.slice(-2));" in src)
ck("spDlgPairIds 對白路行 dlg119DedupePair",
   "return dlg119DedupePair(pair);" in src)
ck("dlg119DedupePair 定義喺 DLG106 模組內（logic test 抽得到）",
   "function dlg119DedupePair(pair){" in src)

# ---------- ⑤ 聽者影 _dim＋唔加 0.60 ----------
ck("spDlgCharsHtml 影行 dlg119Candidates（講者 base／聽者 _dim）",
   "cands = dlg119Candidates(stem119, !isActive);" in src)
ck("影唔加 brightness filter（bright 一律 \"1\"）",
   'if(stem119) bright = "1";' in src)
ck("影貼光暈層（人物背後、底圖之上）",
   "dlg119HaloUrl(stem119)" in src and 'class="dlg119-halo ' in src)
ck("光暈 CSS 齊（同人物幾何、唔入 fit 計算）",
   ".dlg119-halo{" in src and "height:var(--dlg108-char-h,60%)" in src)
ck("影唔行 bust 後備鏈（唔接 spBustUrl／spBustCandidates）",
   "if(stem119){" in src and "cands = dlg119Candidates(stem119, !isActive);" in src)

# ---------- ⑥ 影圖缺失 fallback 黑卡 ----------
ck("__dlg106Err 有影→「影」黑卡分支",
   'img.getAttribute("data-dlg119-shadow")' in src and 'd.textContent = "影";' in src
   and "dlg119-sil" in src)
ck("「影」黑卡 CSS 齊（沿用 sp-bust-sil 配色、dlg106-char 幾何）",
   ".dlg106-char.dlg119-sil{" in src)
ck("spBustUrl 影回空（舊路 render 先出到「影」黑卡）",
   'if(typeof dlg119IsShadow==="function" && dlg119IsShadow(speakerId)) return "";' in src)
ck("影 img 有 data-dlg119-shadow 標記（fallback 先認到佢）",
   'data-dlg119-shadow=\\"1\\"' in src)

# ---------- ⑦ 芬姐唔受影響 ----------
ck("副導演芬姐 LEGACY／GAZE／REG 唔郁",
   legacy.get("副導演芬姐") == "extra_ad_fen"
   and gaze is not None and "extra_ad_fen" in gaze
   and 'extra_ad_fen: { artId:"generic_crew", portraitsKey:null, display:"副導演芬姐" }' in src)

# ---------- ⑧ ①級不變 ----------
ck("阿偉／何生 LEGACY 唔郁",
   legacy.get("阿偉") == "awi" and legacy.get("何生") == "ho_sang")
ck("阿偉／何生 GAZE 唔郁（awi right＋翻得／ho_sang left＋唔翻得）",
   gaze is not None
   and gaze.get("awi", {}).get("gaze") == "right" and gaze.get("awi", {}).get("flipSafe") is True
   and gaze.get("ho_sang", {}).get("gaze") == "left" and gaze.get("ho_sang", {}).get("flipSafe") is False)

# ---------- ⑨ generic_crew 其他用途不變 ----------
ck("LEGACY 再無值指向舊 9 個 id（generic_crew／generic_date／generic_cinema_asst／generic_mag_editor／extra_ad_ling／extra_ad_sam／extra_dir_luk／extra_prod_chow／extra_lan_father）",
   legacy is not None and not (set(legacy.values()) & {
       "generic_crew", "generic_date", "generic_cinema_asst", "generic_mag_editor",
       "extra_ad_ling", "extra_ad_sam", "extra_dir_luk", "extra_prod_chow", "extra_lan_father"}))
ck("舊 9 個 id 嘅 REG 條目全部保留（唔刪除）",
   all(re.search(re.escape(k) + r': \{ artId:"generic_crew"', src) for k in
       ["generic_crew", "generic_date", "generic_cinema_asst", "generic_mag_editor",
        "extra_lan_father", "extra_ad_ling", "extra_ad_sam", "extra_dir_luk", "extra_prod_chow"]))
ck("REG generic_crew display 仍係「臨記」",
   'generic_crew: { artId:"generic_crew", portraitsKey:null, display:"臨記" }' in src)
ck("spBustUrl generic_crew／extra_unknown 特判仲喺度",
   'speakerId==="generic_crew" || speakerId==="extra_unknown"' in src)
ck("新 REG 4 條（影×3＋老臨記，portraitsKey 全部 null）",
   all(f'{k}: {{ artId:"{k}", portraitsKey:null, ' in src
       for k in ("shadow_male", "shadow_female", "shadow_elder", "crew_laolinji")))

# ---------- ⑩ 基線不變 ----------
ck("SAVE key 不變", "starVolunteer_map_v19w" in src)
ck("softRev 不變", "s107" in src)
ck("產品 ?v= 不變", "v20a10" in src)

# ---------- ⑪ 資產總數 ----------
if os.path.isdir(FB):
    names = set(os.listdir(FB))
    ck("fullbody 總數 148（128＋v123 12 張新表情＋v126 6 張新表情＋v20a131 B1 2 張企立圖）",
       len([f for f in names if f.endswith((".webp", ".png"))]) == 148)
    ck("10 張新資產齊（6 張 base/dim＋3 張 halo＋老臨記 base）",
       all(fn in names for fn in (
           "shadow_male_base.webp", "shadow_male_dim_base.webp", "shadow_male_halo.png",
           "shadow_female_base.webp", "shadow_female_dim_base.webp", "shadow_female_halo.png",
           "shadow_elder_base.webp", "shadow_elder_dim_base.webp", "shadow_elder_halo.png",
           "crew_laolinji_base.webp")))

# ---------- 身高比 ----------
ck("DLG119 5 鍵身高比全部 1.00（老年影矮係圖內佔比，唔另外 ×0.84）",
   scale is not None and all(scale.get(k) == 1.00 for k in
       ("shadow_male", "shadow_female", "shadow_elder", "crew_laolinji", "generic_cinema_asst")))

# ---------- 反證（in-memory 變異） ----------
ck("反證：LEGACY 刪走「老臨記」→ checker 必須報錯",
   len(check_mapping({k: v for k, v in (legacy or {}).items() if k != "老臨記"}, gaze or {}, FB)) >= 1)
ck("反證：LEGACY「場務」指錯去女影 → checker 必須報錯",
   len(check_mapping(dict(legacy or {}, **{"場務": "shadow_female"}), gaze or {}, FB)) >= 1)
ck("反證：GAZE 刪走 shadow_male → checker 必須報錯",
   len(check_mapping(legacy or {}, {k: v for k, v in (gaze or {}).items() if k != "shadow_male"}, FB)) >= 1)
fake_fb = tempfile.mkdtemp(prefix="dlg119negfb_")
try:
    for fn in os.listdir(FB):
        os.symlink(os.path.join(FB, fn), os.path.join(fake_fb, fn))
    os.remove(os.path.join(fake_fb, "shadow_elder_halo.png")) if os.path.lexists(os.path.join(fake_fb, "shadow_elder_halo.png")) else None
    ck("反證（真磁碟）：抽走 shadow_elder_halo.png → checker 必須報缺",
       any("shadow_elder_halo.png" in p for p in check_mapping(legacy or {}, gaze or {}, fake_fb)))
finally:
    shutil.rmtree(fake_fb, ignore_errors=True)

print("WARNINGS " + (", ".join(warns) if warns else "none"))
print("RESULT " + ("FAIL (" + str(len(fails)) + ")" if fails else "PASS"))
sys.exit(1 if fails else 0)
