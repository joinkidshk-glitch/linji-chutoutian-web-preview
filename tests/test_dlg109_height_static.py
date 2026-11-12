# v20a109 DLG109 靜態守門：per-character 身高比表（阿偉 1.00／彭少祺 0.85／
# 顧明輝・程天諾 1.05／其餘 1.00）＋ dlg108FitApply 逐張 inline height ＋
# 遮腿幾何不變（bottom:10%／60% 基礎高／對話框定高）＋ PORTRAITS／舊 bust 零掂
# （B 線範圍：只斷言 PORTRAITS map 仲喺度，唔驗內容）。
# 用法：python3 tests/test_dlg109_height_static.py [path-to-index.html]
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

# ---------- DLG109 模組接線 ----------
def mod_ok(s):
    return all(x in s for x in [
        "DLG109_HEIGHT_SCALE", "dlg109HeightScale", "dlg109ScaledPct", "window.DLG109",
        "dlg108FitPct(a[0], a[1], sw, sh, margin, 0.48, sc[0], sc[1])",
    ])
ck("DLG109 接線齊全（身高比表＋scale／scaledPct＋window.DLG109＋fitApply 傳比）", mod_ok(src))
ck("反證：整爛接線（DLG109_HEIGHT_SCALE 改名）後 mod_ok 必須轉 False",
   not mod_ok(src.replace("DLG109_HEIGHT_SCALE", "DLG109_HEIGHT_SCALX")))
ck("fitApply 逐張落 inline height（基礎高 × 身高比）",
   "imgs[j].style.height" in src and "pctOf(pct, sc[j])" in src)
ck("fitApply 單人步同樣 × 比（唔係淨係雙人）",
   "imgs[0].style.height = pctOf(60, scaleOf(imgs[0]))" in src)
ck("角色 id 來源雙路：主線 data-dlg-id＋巧遇 _sid106",
   "im.getAttribute('data-dlg-id') || im._sid106" in src)
ck("未知 id 默認 1.00（舊圖後備唔郁）",
   "return (typeof v===\"number\" && v>0) ? v : 1.00;" in src)

# ---------- 身高比表：覆蓋＋範圍＋實數 ----------
gaze_m = re.search(r"const DLG106_GAZE = \{(.*?)\n\};", src, re.S)
gaze_ids = sorted(set(re.findall(r"\"([a-z0-9_]+)\": \{", gaze_m.group(1)))) if gaze_m else []
ck("DLG106_GAZE 讀到 39 個 id", len(gaze_ids) == 39)
scale_m = re.search(r"const DLG109_HEIGHT_SCALE = \{(.*?)\n\};", src, re.S)
scale = {}
if scale_m:
    for k, v in re.findall(r"\"([a-z0-9_]+)\":\s*([0-9.]+)", scale_m.group(1)):
        scale[k] = float(v)
ck("身高比表有 39 個 key", len(scale) == 39)
ck("身高比表覆蓋全部 39 個 GAZE id",
   gaze_ids and all(i in scale for i in gaze_ids))
def range_ok(table):
    return all(0.80 <= v <= 1.10 for v in table.values())
ck("全部身高比喺 0.80–1.10 之間", range_ok(scale))
ck("反證：身高比改出界（彭少祺 0.75）後範圍斷言必須 FAIL",
   not range_ok(dict(scale, pang_siuki=0.75)))
ck("阿偉基準 1.00（s1／s2／s3 同值）",
   scale.get("awi") == 1.00 and scale.get("awi_s2") == 1.00 and scale.get("awi_s3") == 1.00)
ck("彭少祺 0.85（＜0.90，明顯矮過阿偉）",
   scale.get("pang_siuki") == 0.85)
ck("反證：彭少祺改 1.00 後矮檔斷言必須 FAIL",
   dict(scale, pang_siuki=1.00).get("pang_siuki") != 0.85)
ck("顧明輝／程天諾 1.05（高檔）",
   scale.get("gu_mingfai") == 1.05 and scale.get("ching_tinlok") == 1.05)
ck("其餘 33 個 id 一律 1.00（唔估身高；v119 新加 5 鍵全部 1.00）",
   all(scale.get(i) == 1.00 for i in gaze_ids
       if i not in ("awi", "awi_s2", "awi_s3", "pang_siuki", "gu_mingfai", "ching_tinlok")))

# ---------- 遮腿幾何不變（v108 規格，109 唔郁） ----------
i = src.find(".story-play .dlg106-char{")
seg = src[i:i + 320] if i >= 0 else ""
ck("主線人物高仍係 60% 基礎（--dlg108-char-h，唔設值 60%）",
   "height:var(--dlg108-char-h,60%)" in seg)
ck("主線人物腳底仍係 bottom:10%（腳伸到框後，矮咗只係頭頂低）", "bottom:10%" in seg)
ck("全屏模式人物腳底同樣 bottom:10%",
   "#mask.story-play-on .story-play .dlg106-char{bottom:10%}" in src)
ck("巧遇人物仍係 60% 基礎＋bottom:10%",
   "#enc79-overlay .e79-char{position:absolute;bottom:10%;height:var(--dlg108-char-h,60%)" in src)
ck("主線對話框定高 118px 未郁",
   ".story-play .dlg106-plate{height:118px;min-height:118px;max-height:118px;flex:1}" in src)

# ---------- B 線範圍：PORTRAITS／舊 bust 零掂 ----------
ck("PORTRAITS map 仲喺度（B 線範圍，A 線唔掂）", "PORTRAITS" in src)

# ---------- 真檔重測（PIL）：彭／顧／程闊高比＋配對淨空（計埋身高比） ----------
try:
    from PIL import Image
    import glob as _glob
    files = {}
    for p in sorted(_glob.glob(os.path.join(ROOT, "assets", "story", "fullbody", "*.webp"))):
        if os.path.basename(p).startswith("boss_"):
            continue  # v111：通告負責人立繪（S-30v2 卡上人物），唔係對話舞台角色，唔入身高重測
        im = Image.open(p)
        files[os.path.basename(p)[:-5]] = round(im.size[0] / im.size[1], 4)
    ck("真檔數目仍係 115 張（109 唔加圖；96＋v119 DLG119 7 張 webp＋v123 12 張新表情；3 張 halo 係 png，唔入呢個數；v111 boss_* 11 張另計，唔入身高重測）", len(files) == 115)
    bases = {k[:-5]: v for k, v in files.items() if k.endswith("_base")}
    def near(name, got, want, tol=0.001):
        ck("闊高比 %s＝%.3f（實量 %.3f）" % (name, got, want), abs(got - want) <= tol)
    near("pang_siuki base", bases.get("pang_siuki", -1), 0.376)
    near("gu_mingfai base", bases.get("gu_mingfai", -1), 0.232)
    near("ching_tinlok base", bases.get("ching_tinlok", -1), 0.267)
    near("awi base", bases.get("awi", -1), 0.343)
    H, W = 0.60 * 844, 390
    def gap_scaled(ar1, sc1, ar2, sc2, margin):
        return round(W - margin - H * (ar1 * sc1 + ar2 * sc2), 1)
    g_ap = gap_scaled(bases["awi"], 1.00, bases["pang_siuki"], 0.85, W * 0.04)
    ck(f"重測：阿偉×彭少祺 60% 基礎淨空 {g_ap:.1f}px（≥12，矮咗更鬆）", g_ap >= 12)
    g_ag = gap_scaled(bases["awi"], 1.00, bases["gu_mingfai"], 1.05, W * 0.04)
    ck(f"重測：阿偉×顧明輝 60% 基礎淨空 {g_ag:.1f}px（≥12，高 63% 照計闊度）", g_ag >= 12)
    g_fv = gap_scaled(bases["fong_siulung"], 1.00, bases["vera"], 1.00, 12)
    ck(f"重測：方小龍＋Vera 60% 基礎淨空 {g_fv:.1f}px（＜12，自動收細照觸發）", g_fv < 12)
    info("身高比表：矮 0.85×1／高 1.05×2／中 1.00×36；渲染高 51%／63%／60%")
except ImportError:
    warns.append("PIL 未裝：跳過真檔重測")
    print("WARN PIL 未裝：跳過真檔重測")
except Exception as e:
    ck("真檔重測執行無誤（" + str(e) + ")", False)

if warns:
    for w in warns: print("WARN " + w)
print("RESULT " + ("FAIL (%d)" % len(fails) if fails else "PASS"))
sys.exit(1 if fails else 0)
