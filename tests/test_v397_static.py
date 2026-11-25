# v406：選單刪「返回」列，靜態 <button 111→110（有意圖改動）。
# v404 意圖更新：確認閘刪除後 40 號掣層級斷言改做新掣名。
# v397：第五輪 UI 檢視頭五項必修 — 靜態測試（釘字串／接線／禁區守門）。
# 用法：python3 tests/test_v397_static.py [repo-root]
import os
import sys

root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..")
src = open(os.path.join(root, "index.html"), encoding="utf-8").read()
fails = []
total = [0]


def ok(msg, cond):
    total[0] += 1
    if cond:
        print("PASS " + msg)
    else:
        fails.append(msg)
        print("FAIL " + msg)


def seg(start, end):
    b = src.index(start)
    e = src.index(end, b)
    return src[b:e]


def fn_seg(sig):
    b = src.index(sig)
    e = src.index("\nfunction ", b + 1)
    return src[b:e]


# ---- (1) venue99 相疊＋地圖底邊截籤 ----
ok("v397 venue99 金禧錨點下移 30px（上下錯行）",
   "top:calc(24% + 30px)" in src)
ok("v397 碰撞夾實 helper 在位（8px 淨距）",
   "function clampMapLabels397(){" in src and "const GAP = 8" in src
   and ".md97-venue99" in src)
ok("v397 clamp 由 positionMapLabels137＋paintBar＋ResizeObserver 觸發",
   "clampMapLabels397()" in src and "__mapRO397" in src
   and src.count("clampMapLabels397()") >= 3)

# ---- (2) 35c 殘留 ----
ok("v397 35c 結果卡報頭收緊（只限結果卡，晨報唔郁）",
   ".paper-sheet.awd-result396 .np214-masthead .np214-name{ font-size:36px; }" in src
   and ".paper-sheet.awd-result396 .np214-photowrap{ float:none; width:min(240px,100%); margin:4px auto; }" in src)
ok("v397 35c 右欄模糊尾字換成非文字印記",
   ".np214-sb-mark397" in src and "np214-sb-mark397" in src)
render_award = fn_seg("function renderAwardResultHtml(")
render_morning = fn_seg("function renderMorningPaperHtml(")
ok("v397 35c 結果卡 sidebar 唔再有 filler-v（晨報保留）",
   '<p class="np214-filler-v"' not in render_award and '<p class="np214-filler-v"' in render_morning)
ok("v397 35c 第二版導語改散場鏡頭（唔再重複第一版入圍段）",
   "metricDek397" in src and "散場時分，掌聲未散" in src)
ok("v397 35c 第二版 lead 改散場報道（點明陳偉翔係觀察對象）",
   "metricLead397" in src and "散場報道的觀察對象" in src)
ok("v397 35c 第二版圖說用散場版（唔提典禮名，避橫額 mismatch）",
   "aftermath:true" in src and "散場時離開會場" in src)

# ---- (3) 通告欄峰值 ----
# v398：通告欄頭板改透明貼紙底（去報表工具列），sticky 保留；見 test_v398_static.py。
ok("v397 通告欄頂欄縮薄（sticky 保留）",
   ".board-head392{ position:sticky; top:0;" in src
   and "background:var(--paper); border:0;" in src  # v398 補：--panel 係深啡 #3A3530，用佢會留返條深色報表帶；紙底先啱
   and "padding:4px 2px 6px; margin:0 0 6px;" in src)
ok("v397 排序／篩選各收納成一粒下拉掣（顯示已套用條件）",  # v398：兩掣合併做一粒「整理」掣，選項分排序／媒介兩組
   'data-board-menu397="organize"' in src and "整理 ▾" in src and "board-ctl397" in src)
ok("v397 排序／篩選選項保留（功能唔減）",
   "board-sort392" in src and "board-filter392" in src
   and 'data-sort392' in src and 'data-filter392' in src)
ok("v397 詳情預期日薪計法 helper 在位",
   "function boardExpCalc397(g){" in src and "board-calc397" in src
   and "四捨五入" in src)
do_scout = seg("function doScout(L){", "function applyTrainLesson(")
ok("v397 鎖定摘要移去可接清單最尾（唔再插斷）",
   do_scout.index("readyList392.forEach") < do_scout.index("if(lockedF392.length) body+=lockedDetails392(lockedF392);"))

# ---- (4) 40／27／86 家族 ----
ok("v397 日結卡 scene 模式（場景留低、掣收起）",
   "keepScene397" in src and "dayres-scene397" in src
   and "setUnderlyingInert(true, !!(opts.keepScene397 || scene401))" in src  # v401 UI401-1：scenePaper401 同樣留場景，keepScene397 觸發不變
   and "#app.dayres-scene397 #map-pins," in src)
ok("v397 日結漸變放淺（.10／.42）",
   "linear-gradient(180deg, rgba(0,0,0,.10) 0, rgba(0,0,0,.10) 48px, rgba(0,0,0,.42) 48px) !important" in src)
ok("v397 40 號掣層級：確認閘已刪，執行掣名講明後果（v404）",
   'label:"返回休息卡"' not in src
   and 'label:"開始並結算當日"' not in src
   and '"休息並過日"' in src and '"執行今日行程"' in src
   and "dayEndContinueButtons(ended, go).forEach(b=>btns.push(b))" in src)
ok("v397 86c 週結提示改紅印章（正文唔再重複回家結算）",
   "dayres-stamp397" in src and "一週完結 → 回家結算" not in src
   and "一週完結" in src)
ok("v397 27c ledger helper 在位＋兩邊日結路徑都用",
   "function dayResLedger397(html){" in src
   and "dayResLedger397(resultHtml)" in src
   and "dayResLedger397(body)" in src)

# ---- (5) 掣量 ----
ok("v397 開局分步：教學期間收起手帳次要控制",
   'app.classList.toggle("tut-stage397", !!on)' in src
   and "#app.tut-stage397 #hgroup-career," in src
   and "#app.tut-stage397 #cat-tabs," in src
   and "#app.tut-stage397 #btn-intel381{" in src)
ok("v397 行程工具收成一粒下拉掣（id＋handler 保留）",
   'id="nb-q-tools397"' in src and 'id="nb-tools397-menu"' in src
   and 'id="nb-q-rest"' in src and 'id="nb-q-train"' in src
   and 'id="nb-q-clear"' in src and 'id="nb-q-copy"' in src
   and 'id="btn-reset-plan"' in src
   and 'document.getElementById("btn-reset-plan").onclick=resetPlanDraft' in src)
ok("v397 約會入口合併（一粒入內揀人）",
   "function rom159OpenDateWhoPicker(keys, L){" in src
   and 'add("約人出街"' in src
   and src.count("addRom159DateActs(add, L);") == 2
   and "約人出街" in src)
ok("v397 選單「過一日」已刪（地圖入口保留）",
   'data-m="rest-early"' not in src
   and 'm==="rest-early"' not in src
   and "confirmEarlyRestFromMenu" in src
   and ">過一日</button>" in src)
ok("v397 「未開放」改不可撳紙標",
   "sp-lock-tag" in src
   and '<button type="button" class="sp-play" disabled' not in src
   and "劇情未開放" in src)
ok("v397 33b 回顧唯讀收起編輯工具",
   'ct397.style.display = editable ? "" : "none"' in src
   and 'ib397.style.display = editable ? "" : "none"' in src
   and "ending78Locked" in src)

# ---- 靜態 <button 總數：v396 係 110；v397 係 112（＋2 板下拉掣＋1 工具掣＋1 約人 picker 模板
# －1 選單過一日－1 未開放掣；可見掣數每屏都跌，見實駕 counts397.json）；v398 係 111（兩粒板下拉掣合併做一粒「整理」） ----
ok("v397 靜態 <button 總數 110（v406：選單刪「返回」列 −1）（v396：110）",  # v398：111
   src.count("<button") == 110)

# ---- 唔郁嘅嘢：SAVE／softRev／?v= ----
ok("v397 SAVE key 不變 starVolunteer_map_v19w", "starVolunteer_map_v19w" in src)
ok("v397 softRev 不變 s107", 'SOFT_REV = "s107"' in src)
ok("v397 ?v= 不變 v20a10", "?v=20a10" in src)

print()
print("v397 static: %d passed, %d failed" % (total[0] - len(fails), len(fails)))
sys.exit(1 if fails else 0)
