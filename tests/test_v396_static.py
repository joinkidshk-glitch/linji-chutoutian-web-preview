# v396：第四輪 UI 檢視頭五項必修 — 靜態測試（釘字串／接線／禁區守門）。
# 用法：python3 tests/test_v396_static.py [repo-root]
import os
import re
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


# 禮品店／買衫店區塊（gift185／reconfirm236 同款切法）
seg_gift = seg('function openGiftShop(shopId, L){', 'function openGiftPick(')
seg_ward = seg('function openClothingShop265(L){', 'function renderWardrobe265(){')


# ---- (1) 35c 頒獎結果卡：390px 下正文改單欄（只限結果卡，晨報唔郁） ----
ok("v396 35c 結果卡有 awd-result396 專屬 class",
   'paper-sheet awd-result396' in src)
ok("v396 35c 專屬 CSS：body2 單欄",
   ".paper-sheet.awd-result396 .np214-body2{ column-count:1; column-rule:none; }" in src)
ok("v396 35c 專屬 CSS：相片＋圖說成組、取消繞排",
   ".paper-sheet.awd-result396 .np214-photowrap{ float:none; width:min(240px,100%); margin:8px auto; }" in src)
ok("v396 35c 專屬 CSS：第二版掣改 static（隨正文捲動，唔再遮正文）",
   ".paper-sheet.awd-result396 .np214-switchrow{ position:static; background:transparent; }" in src)
ok("v396 35c 小檔案抽成共用 factboxHtml214",
   "factboxHtml214" in src)
ok("v396 35c 小檔案喺第二版用全闊格",
   "np214-factbox np214-factbox-wide" in src)
# 測試約束不變：報紙 214／頒獎 186／192 釘嘅標記全部保留
for mark in ["np214-body2", "np214-sidebar", "np214AwardPhoto214", "np214-photowrap",
             'data-np214-page="1"', 'data-np214-page="2"', "np214-factbox"]:
    ok("v396 35c 保留舊標記 " + mark, mark in src)

# ---- (2) 通告欄峰值：預期日薪透明化＋類別統一＋篩選計數 ----
ok("v396 board392ExpDaily 存在：預期日薪＝片酬×成功率÷日數",
   "function board392ExpDaily(g){" in src
   and "(Number(p)||0) * pay / Math.max(1, Number(d)||1)" in src)
ok("v396 通告欄 lead 出計法（一行）",
   "預期日薪＝片酬×成功率÷日數" in src)
ok("v396 通告欄篩選總數行出「顯示 X／總數」",
   "顯示 ${readyF392.length+lockedF392.length}／${shown.length} 張" in src)
ok("v396 通告欄類別 pill 先出媒介（coarse396）再出 genre",
   "const coarse396 = gigTypeCoarse(g);" in src
   and "const genrePills396" in src)
ok("v396 通告欄可接卡出「預期 $X／日」",
   "預期 $" in src and "／日" in src)
ok("v396 通告欄 exp 計算有 typeof 守門（test sandbox 無 board392ExpDaily／_boardSort392 都唔爆）",
   'typeof board392ExpDaily==="function"' in src
   and 'typeof _boardSort392!=="undefined"' in src)
ok("v396 通告欄 6 粒排序／篩選掣保留（唔減功能）",
   "board-sort392" in src and "board-filter392" in src)

# ---- (3) 40／27／86 家族：日結卡日期標示＋淺遮罩真生效 ----
ok("v396 日結日期 helper 存在：settledDateObj396／fmtShortDate396／dayResDateLine396",
   "function settledDateObj396(){" in src
   and "function fmtShortDate396(d){" in src
   and "function dayResDateLine396(firstLabel, doneFull){" in src)
ok("v396 日結日期標示：結算日同下一日分開標",
   "結算：" in src and "下一日：" in src and "行程" in src)
ok("v396 日結日期標示：完成日標籤",
   "完成日" in src)
ok("v396 40 號確認卡用 day-res 底部＋淺遮罩",
   "day-res-open" in src and "day-res" in src)
ok("v396 日結漸變補返 !important（#mask.on 嘅 .72 !important 一直蓋住佢）",
   "linear-gradient(180deg, rgba(0,0,0,.18) 0, rgba(0,0,0,.18) 48px, rgba(0,0,0,.58) 48px) !important" in src)
ok("v396 40 號卡日期用 dayResDateLine396（結算）",
   'dayResDateLine396("結算")' in src)
ok("v396 afterDayModal／afterDayRes 日期用 dayResDateLine396（完成日）",
   'dayResDateLine396("完成日", opts.dayDone)' in src
   and 'dayResDateLine396("完成日", dayDone)' in src)

# ---- (5) Modal 開住時卸載背景地圖互動層 ----
ok("v396 背景卸載用 display:none（visibility:hidden 唔減 COUNT_JS）",
   "#app.ui-hide-under396 #v-map," in src
   and "display: none !important;" in src)
ok("v396 背景卸載覆蓋 v-map／v-home／v-start／loc-sheet／menubar／.menu／btn-confirm-plan",
   "#app.ui-hide-under396 #v-home," in src
   and "#app.ui-hide-under396 #loc-sheet," in src
   and "#app.ui-hide-under396 #btn-confirm-plan{" in src)
ok("v396 setUnderlyingInert 同步開關 ui-hide-under396",
   'app.classList.toggle("ui-hide-under396", !!(on && !tut))' in src)
ok("v396 教學聚光燈（mask.tut-on）豁免卸載",
   'mask.classList.contains("tut-on")' in src)
ok("v396 禮品／買衫行改做 div（唔係掣，唔計入掣數）",
   '<div class="act' in seg_gift and '<button type="button" class="act' not in seg_gift
   and '<div class="act' in seg_ward and '<button type="button" class="act' not in seg_ward)
ok("v396 商店行唔再有 <button ... data-buy／data-buy265",
   '<button type="button" class="act' not in seg_gift
   and '<button type="button" class="act' not in seg_ward)
ok("v396 商店揀中行用 act-sel396 金框",
   "act-sel396" in src)
ok("v396 商店單一購買掣 shop-buy396＋stay:true（唔關窗）",
   'cls:"shop-buy396", stay:true' in src)
ok("v396 未揀就撳購買出 toast、唔關窗",
   'toast("請先揀一件禮物")' in src and 'toast("請先揀一件衫")' in src)
ok("v396 買衫流程不變：confirmChoice236＋buyCostume265(id)",
   'confirmChoice236({' in seg_ward and 'buyCostume265(id)' in seg_ward)
ok("v396 禮品流程不變：confirmChoice236＋GiftShop.buyItem(shopId, id)",
   'confirmChoice236({' in seg_gift and 'GiftShop.buyItem(shopId, id)' in seg_gift)
ok("v396 禮品店唔用 gift-pick-name（gift185 禁區）",
   '<span class="gift-pick-name">' not in seg_gift
   and src.count('gift-pick-name') == 2)  # 只剩 CSS＋openGiftPick 各一處

# ---- 靜態 <button 總數：v392 係 112，v396 係 110（兩間商店嘅行模板由 button 轉 div；
# 每間得一個模板字串，所以靜態只減 2；實駕掣數禮品 37→2、買衫 33→2） ----
ok("v396 靜態 <button 總數 110（v392：112）",
   src.count("<button") == 110)

# ---- 唔郁嘅嘢：SAVE／softRev／?v= ----
ok("v396 SAVE key 不變 starVolunteer_map_v19w", "starVolunteer_map_v19w" in src)
ok("v396 softRev 不變 s107", 'SOFT_REV = "s107"' in src)
ok("v396 產品 ?v= 不變 20a10", '"20a10"' in src)

print()
if fails:
    print("FAILURES: %d" % len(fails))
    for f in fails:
        print(" - " + f)
    sys.exit(1)
print("ALL PASS (%d checks)" % total[0])
