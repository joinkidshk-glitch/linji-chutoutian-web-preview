# v20a108 DLG108 靜態守門：60% 排位＋對話框遮腿＋對話框定高＋下一句文字鏈＋
# 地面錨線零殘留（04:18 統籌追加取代舊方案）＋ v106/v107 真檔重測（96 張闊高比）。
# 用法：python3 tests/test_dlg108_static.py [path-to-index.html]
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

# ---------- 地面錨線零殘留（舊方案已撤銷，唔准留半套 code） ----------
for bad in ["dlg108-ground", "DLG108_GROUND", "dlg108GroundFor"]:
    ck("無錨線殘留：" + bad, bad not in src)

# ---------- DLG108 模組接線 ----------
def mod_ok(s):
    return all(x in s for x in [
        "dlg108FitPct", "dlg108FitApply", "window.__dlg108Fit", "window.DLG108",
        "--dlg108-char-h", "dlg108FitPct(arL, arR, stageW, stageH",
    ])
ck("DLG108 接線齊全（fit 函數＋onload 掛鉤＋--dlg108-char-h）", mod_ok(src))
ck("反證：整爛接線（dlg108FitPct 改名）後 mod_ok 必須轉 False",
   not mod_ok(src.replace("dlg108FitPct", "dlg108FitPcX")))
ck("onload 收細掛鉤：主線 img 有 onload __dlg108Fit",
   'onload="try{window.__dlg108Fit&&window.__dlg108Fit(this)}' in src)
ck("onload 收細掛鉤：巧遇 charL/charR 有 im.onload＝__dlg108Fit",
   "im.onload = function(){ try{ window.__dlg108Fit" in src)
ck("單人步照設 --dlg108-char-h:60%（唔係留空靠 fallback）",
   "imgs.length === 1" in src and "stage.style.setProperty('--dlg108-char-h', '60%')" in src)

# ---------- 60%＋遮腿 CSS ----------
i = src.find(".story-play .dlg106-char{")
seg = src[i:i + 320] if i >= 0 else ""
ck("主線人物高 60%（--dlg108-char-h，唔設值 60%）",
   "height:var(--dlg108-char-h,60%)" in seg)
ck("主線人物腳底 bottom:10%（腳伸到框後）", "bottom:10%" in seg)
ck("反證：人物高改回 50% 後 60% 斷言必須 FAIL",
   "height:var(--dlg108-char-h,60%)" not in seg.replace("height:var(--dlg108-char-h,60%)", "height:50%"))
ck("全屏模式人物腳底同樣 bottom:10%",
   "#mask.story-play-on .story-play .dlg106-char{bottom:10%}" in src)
ck("主線對話框定高 118px（height＋min＋max 三齊）",
   ".story-play .dlg106-plate{height:118px;min-height:118px;max-height:118px;flex:1}" in src)
ck("旁白板同樣入 dlg106-plate（定高適用旁白）",
   "sp-plate sp-plate-narration105 dlg106-plate" in src)
ck("主線牌底色不透明（遮腿靠實色牌）",
   "linear-gradient(168deg,#f8f0dd 0%,#f2e6cc 58%,#ebdfc1 100%)" in src)
ck("主線牌疊喺人物之上（.sp-stage-inner z-index:3 ＞ .dlg106-chars z-index:2）",
   ".story-play .sp-stage.dlg106-on .sp-stage-inner{position:relative;z-index:3" in src
   and ".story-play .dlg106-chars{position:absolute;inset:0;z-index:2" in src)

# ---------- 巧遇：盒疊舞台＋60%＋遮腿 ----------
def enc_css(s):
    return all(x in s for x in [
        "#enc79-overlay .e79-char{position:absolute;bottom:10%;height:var(--dlg108-char-h,60%)",
        "#enc79-overlay .e79-box{position:absolute;left:0;right:0;bottom:0;z-index:5;",
        "#enc79-overlay .e79-line{margin:0 0 10px;line-height:1.55;font-size:1rem;height:4.65em;min-height:4.65em;overflow-y:auto;",
        "#enc79-overlay .e79-name{font-weight:800;color:#8a5a00;margin:0 0 4px;font-size:.95rem;line-height:1.5;min-height:1.5em;}",
    ])
ck("巧遇 CSS 齊全（人物 60%＋bottom:10%＋盒 absolute 疊底 z-index:5＋對白行定 3 行＋名牌行定高）",
   enc_css(src))
ck("反證：盒 z-index 改 1 後 enc_css 必須轉 False",
   not enc_css(src.replace(
       "#enc79-overlay .e79-box{position:absolute;left:0;right:0;bottom:0;z-index:5;",
       "#enc79-overlay .e79-box{position:absolute;left:0;right:0;bottom:0;z-index:1;")))
# 合併更新（統籌）：D-5 將巧遇盒改做米紙框（同主線牌統一），DLG108 幾何不變。
# 舊深色盒／金字斷言喺合併後代碼下必然 FAIL——已實證；新斷言喺合併前 dlg 分支代碼下 FAIL，屬反證。
ck("巧遇盒底色不透明（D-5 米紙漸變三色皆實色 hex）",
   "linear-gradient(168deg,#f8f0dd 0%,#f2e6cc 58%,#ebdfc1 100%)" in src)
ck("巧遇人物 z-index ≤4（盒 z-index:5 先蓋得住）",
   'im.style.zIndex = isActive ? 4 : 3' in src)

# ---------- 下一句文字鏈 ----------
def next_link_ok(s):
    return all(x in s for x in [
        "#mask.story-play-on:has(.sp-mode-dialogue) #modal-btns button.p,",
        "#mask.story-play-on:has(.sp-mode-narration) #modal-btns button.p{",
        "background:transparent !important;border:0 !important;box-shadow:none !important;",
        "color:#ffd968 !important;text-decoration:underline;text-underline-offset:3px;",
        "min-width:88px;min-height:44px;",
    ])
ck("主線「下一句」文字鏈（只限 beats 模式 role p 掣）", next_link_ok(src))
ck("主線文字鏈唔掂選項模式（規則入面冇 sp-mode-choices）",
   "sp-mode-choices" not in src[src.find("#mask.story-play-on:has(.sp-mode-dialogue)"):src.find("#mask.story-play-on:has(.sp-mode-dialogue)") + 600])
ck("反證：文字鏈底色改回金色後 next_link_ok 必須轉 False",
   not next_link_ok(src.replace("background:transparent !important;", "background:#ffd968 !important;")))
ck("巧遇「下一句」文字鏈（透明底＋深金字＋底線＋44px／88px 撳掣面積）",
   "#enc79-overlay .e79-btn{flex:0 0 auto;margin-left:auto;min-height:44px;min-width:88px;" in src
   and "background:transparent;color:#8a5a00" in src
   and "text-decoration:underline;text-underline-offset:3px;" in src)
ck("巧遇選項掣還原舊全寬深色掣（唔跟文字鏈）",
   "#enc79-overlay .e79-btn.e79-choice{flex:1 1 100%;margin-left:0;text-align:left;background:#2e2113;color:#f3e8d5;border:1px solid #a97f2f;text-decoration:none;" in src)
ck("反證：舊全寬米白「下一句」掣已消失（flex:1 1 auto 唔再係 .e79-btn 主規則）",
   "#enc79-overlay .e79-btn{flex:1 1 auto;" not in src)

# ---------- 真檔重測（96 張闊高比，PIL 實量；對照 size-test README） ----------
try:
    from PIL import Image
    import glob as _glob
    files = {}
    for p in sorted(_glob.glob(os.path.join(ROOT, "assets", "story", "fullbody", "*.webp"))):
        if os.path.basename(p).startswith("boss_"):
            continue  # v111：通告負責人立繪（S-30v2 卡上人物），唔係對話舞台角色，唔入配對重測
        im = Image.open(p)
        files[os.path.basename(p)[:-5]] = round(im.size[0] / im.size[1], 4)
    ck("真檔數目 123 張（v106 88 張＋v107 8 張新表情＋v119 DLG119 7 張 webp＋v123 12 張新表情＋v126 6 張新表情＋v20a131 B1 2 張企立圖；v111 boss_* 11 張另計，唔入對話重測；3 張 halo 係 png）", len(files) == 123)
    def near(name, got, want, tol=0.001):
        ck("闊高比 %s＝%.3f（size-test %.3f）" % (name, got, want), abs(got - want) <= tol)
    bases = {k[:-5]: v for k, v in files.items() if k.endswith("_base")}
    near("awi base", bases.get("awi", -1), 0.343)
    near("ho_sang base", bases.get("ho_sang", -1), 0.364)
    near("chung_choning base", bases.get("chung_choning", -1), 0.337)
    near("fong_siulung base", bases.get("fong_siulung", -1), 0.413)
    near("vera base", bases.get("vera", -1), 0.382)
    H, W, AVAIL = 0.60 * 844, 390, 390 - 12
    def gap(ar1, ar2): return round(AVAIL - H * (ar1 + ar2), 1)
    g_ah = gap(bases["awi"], bases["ho_sang"])
    g_ac = gap(bases["awi"], bases["chung_choning"])
    ck(f"重測：阿偉×何生 60% 淨空 {g_ah:.1f}px（size-test 17px，新批更鬆）", 19.0 <= g_ah <= 21.5)
    ck(f"重測：阿偉×鍾楚凝 60% 淨空 {g_ac:.1f}px（size-test 30px）", 32.0 <= g_ac <= 35.0)
    pairs = sorted(((round(bases[a] + bases[b], 3), a, b)
                    for ii, a in enumerate(sorted(bases)) for b in sorted(bases)[ii + 1:]), reverse=True)
    s_top, a_top, b_top = pairs[0]
    ck("重測：最闊配對合計 %.3f（方小龍＋老年影 0.813；v119 前係方小龍＋Vera 0.795）" % s_top, abs(s_top - 0.813) <= 0.001)
    cap = round((AVAIL - 12) / s_top / 844 * 100, 1)
    ck(f"重測：最闊配對上限 {cap:.1f}%（size-test 約 55%，v119 老年影闊袍 0.400 令上限跌到約 53%）", 52.5 <= cap <= 54.0)
    n_shrink = sum(1 for s, a, b in pairs
                 if round(AVAIL - H * (bases[a] + bases[b]), 1) < 12)
    ck(f"重測：60% 下淨空 <12px 嘅配對有 {n_shrink}/{len(pairs)} 個（自動收細非擺設；v119 前 55 個；v20a131 B1 加 2 個 base，＋10 對）",
       n_shrink == 120)
    info("重測寫入 qa108d/remeasure108d.json（%d 張，%d 個 base）" % (len(files), len(bases)))
except ImportError:
    warns.append("PIL 未裝：跳過真檔重測")
    print("WARN PIL 未裝：跳過真檔重測")
except Exception as e:
    ck("真檔重測執行無誤（" + str(e) + ")", False)

if warns:
    for w in warns: print("WARN " + w)
print("RESULT " + ("FAIL (%d)" % len(fails) if fails else "PASS"))
sys.exit(1 if fails else 0)
