# v20a120 LOCFULL120 靜態守門：地點面板改全屏幕（純呈現層）。
# 覆蓋：① sheet 全屏幕（inset 0＋height 100%＋max-height none，壓得過 v17y／toast-up
#       keep-sheet 嗰兩條 max-height 規則）② 場景圖全幅底（absolute inset 0，唔再係
#       210px banner；短屏媒體查詢唔再設 150／120px banner 高）③ 頂欄淺米字＋頂部暗角
#       ④ 額度 pill 改行 in-flow（地名下面，flex order 4）⑤ 選項區內滾、掣列貼住卡底
#       ⑥ 負責人闊 150px、標題收窄 164px、錨定上限 400／下限 120／腳收 120px
#       ⑦ 冇圖素底態全屏幕有實底 ⑧ v118 [hidden] 覆寫保留 ⑨ 紀律：SAVE key／softRev／
#       產品 ?v= 不變；openLoc／travel114 計數邏輯零改動
# 反證：pristine main（v118 版）跑呢檔要 FAIL（LOCFULL120 一節／400 上限全部唔存在）。
# 用法：python3 tests/test_locfull120_static.py [path-to-index.html]
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "..", "index.html")
ROOT = os.path.dirname(IDX)
with open(IDX, encoding="utf-8") as f:
    src = f.read()

fails = []
def ck(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond: fails.append(name)

def extract_fn(name):
    i = src.find("function %s(" % name)
    assert i >= 0, "fn not found: " + name
    depth, j = 0, src.find("{", i)
    for k in range(j, len(src)):
        if src[k] == "{": depth += 1
        elif src[k] == "}":
            depth -= 1
            if depth == 0: j = k; break
    return src[i:j + 1]

def block_of(marker, length=9000):
    i = src.find(marker)
    assert i >= 0, "marker not found: " + marker
    return src[i:i + length]

# ---------- 0. 紀律 ----------
ck("SAVE key 不變", "starVolunteer_map_v19w" in src)
ck("softRev 不變", "s107" in src)
ck("產品 ?v= 不變", "v20a10" in src)

css120 = block_of("v20a120 LOCFULL120")

# ---------- 1. sheet 全屏幕 ----------
ck("LOCFULL120 一節存在", "v20a120 LOCFULL120" in src)
ck("sheet 全屏幕：#app 選擇器 inset 0（壓得過 v17y）",
   "#app #loc-sheet.sheet.locpanel118" in css120 and "inset:0 !important" in css120)
ck("sheet 全屏幕：height 100%",
   "height:100% !important" in css120)
ck("sheet 全屏幕：max-height none（壓得過 72dvh／560px）",
   "max-height:none !important" in css120)
ck("sheet 全屏幕：border-radius 0（唔再係 bottom sheet 圓角）",
   "border-radius:0 !important" in css120)
ck("sheet 全屏幕：透明底（場景圖做底）",
   "background:transparent !important" in css120)
ck("sheet 全屏幕：overflow hidden（負責人／暗角唔會碌出）",
   "overflow:hidden !important" in css120)
ck("sheet 全屏幕：safe-area 底 inset 保留",
   "env(safe-area-inset-bottom" in css120)
ck("toast-up keep-sheet 嗰條 max-height 另有專條覆寫（唔會限返 100dvh-176px）",
   "#app.toast-up.keep-sheet #loc-sheet.sheet.locpanel118" in css120)

# ---------- 2. 場景圖全幅底，唔再係 banner ----------
ck("場景圖全幅底：.loc-bg absolute inset 0",
   ".locpanel118 .loc-bg" in css120 and "position:absolute !important" in css120
   and "inset:0 !important" in css120)
ck("場景圖全幅底：background-position center 30%（跟樣本）",
   "background-position:center 30% !important" in css120)
ck("210px banner 已刪（全檔唔再有 locpanel118 210px 規則）",
   "#loc-sheet.locpanel118 .loc-bg{ height:210px; }" not in src)
ck("短屏唔再設 150／120px banner 高",
   "#loc-sheet.locpanel118 .loc-bg{ height:150px; }" not in src
   and "#loc-sheet.locpanel118 .loc-bg{ height:120px; }" not in src)

# ---------- 3. 頂欄可讀：淺米字＋頂部暗角 ----------
ck("頂部暗角 ::before（跟樣本 .scrim-top）",
   "#app #loc-sheet.sheet.locpanel118::before" in css120
   and "linear-gradient(rgba(20,14,8,.72)" in css120)
ck("標題／描述／#loc-who 淺米字＋陰影",
   "color:#f8f1de !important" in css120 and "text-shadow:0 1px 6px rgba(0,0,0,.6)" in css120)
ck("拖手 .grab 全屏幕隱藏", ".locpanel118 .grab{ display:none !important; }" in css120)

# ---------- 4. 額度 pill 改行 in-flow（地名下面） ----------
ck("pill in-flow：position static（唔再 absolute 疊 banner）",
   ".locpanel118-quota" in css120 and "position:static !important" in css120)
ck("pill flex order 4（標題 1／描述 2／#loc-who 3 之後）",
   "#loc-title{ order:1;" in css120 and "#loc-desc{ order:2;" in css120
   and "#loc-who{ order:3;" in css120 and "order:4" in css120)
ck("名牌列 order 5", ".locpanel118-tagrow" in css120 and "order:5" in css120)

# ---------- 5. 選項區內滾、掣列貼住卡底 ----------
ck("選項卡 order 6", "#loc-acts" in css120 and "order:6" in css120)
ck("選項區內滾（.acts flex:1＋overflow auto 規則仲喺度）",
   "#loc-sheet.sheet .acts" in src and "overflow-y: auto !important" in src)
ck("選項區唔撐滿成版（fix1：flex:0 1 auto＋margin-top:auto 貼底，grid 唔拉長啲掣）",
   "flex:0 1 auto !important" in css120 and "margin-top:auto !important" in css120
   and "align-content:start" in css120)
ck("掣列 order 7、貼住卡底（負 margin 食 gap、去頂框、底圓角）",
   ".btnrow" in css120 and "order:7" in css120
   and "margin:-6px 0 0 !important" in css120 and "border-top:none" in css120
   and "border-radius:0 0 12px 12px" in css120)
ck("掣列米紙底（同選項卡同一塊）", "background:#f8f1de" in css120)

# ---------- 6. 負責人幾何 ----------
ck("負責人闊 150px（貼近樣本）", ".locpanel118-owner{ width:150px; }" in css120)
ck("負責人圖 max-width 150px", "max-width:150px" in css120)
ck("有負責人嗰陣標題／描述收窄 164px",
   "calc(100% - 164px)" in css120)
ck("標題 1.15rem（11 字地名＋164px 收窄都唔換行）",
   "font-size:1.15rem" in css120)
anchor_src = extract_fn("locpanel118AnchorOwner")
ck("錨定：人物高度上限 400（v118 嘅 230 已升；貼近樣本 400px）",
   "Math.min(400" in anchor_src)
ck("錨定：人物高度下限 120 不變", "Math.max(120" in anchor_src)
ck("錨定：腳部收 120px 入選項卡（遮腿，跟樣本；v118 嘅 8px 已改）", "- 120" in anchor_src)

# ---------- 7. 冇圖素底態全屏幕有實底 ----------
ck("素底態：全屏幕還原米紙底（唔可以透明見到地圖）",
   ".locpanel118.locpanel118-nobg" in css120
   and "background:#F2EBD8 !important" in css120)
ck("素底態：深色字＋冇暗角",
   ".locpanel118-nobg #loc-title" in css120 and "text-shadow:none" in css120)

# ---------- 8. v118 [hidden] 覆寫保留 ----------
ck("[hidden] 覆寫仲喺度（三元素 hidden 嗰陣 display:none）",
   ".locpanel118-quota[hidden]" in src and ".locpanel118-owner[hidden]" in src
   and ".locpanel118-tagrow[hidden]" in src and "display:none !important" in src)

# ---------- 9. 計數／行為零改動 ----------
for fn in ("travel114State", "travel114Remain", "travel114IsFree", "travel114TrySpend"):
    ck("v114 %s 源碼唔含 locpanel118／locfull120（計數零改動）" % fn,
       "locpanel118" not in extract_fn(fn) and "locfull120" not in extract_fn(fn))
ck("openLoc 額度閘原文不變",
   "travel114TrySpend(opts, id)" in src)
ck("content pack JSON 唔喺呢包改動範圍（index.html 內無新增 content 引用）",
   "content/" not in css120)

print("RESULT " + ("FAIL (%d)" % len(fails) if fails else "PASS"))
sys.exit(1 if fails else 0)
