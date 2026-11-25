# v404 意圖更新：presentStartScheduleConfirm45 刪除，scene 家族計數 11→10。
# v398：第六輪 UI 檢視頭五項必修 — 靜態測試（釘字串／接線／禁區守門）。
# 用法：python3 tests/test_v398_static.py [repo-root]
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


# ---- (1) TUT_MAP 聚光燈＋教學卡遮 pin＋重複句 ----
ok("v398 教學聚光獨立金圈在位（唔靠 pin class）",
   "function refreshTutSpotlight398(){" in src
   and "function ensureTutSpotlightRing398(){" in src
   and "tut-spotlight-ring398" in src
   and "#tut-spotlight-ring" in src)
ok("v398 金圈由 drawMap 尾段＋教學 rAF＋showTutMainStep 補位",
   "refreshTutSpotlight398()" in src
   and seg("function drawMap(){", "function mapWrapEl()").count("refreshTutSpotlight398()") >= 1
   and "refreshTutSpotlight398();" in seg("function showTutMainStep(", "function finishTutorial("))
ok("v398 金圈入場後延遲再對位（地圖 settle 約 200ms，即刻嗰次會攞舊 rect）",
   'setTimeout(()=>{ try{ if(typeof refreshTutSpotlight398==="function") refreshTutSpotlight398(); }catch(_e){} }, 400);' in seg("function showTutMainStep(", "function finishTutorial("))
ok("v398 金圈 resize／捲動重定位（監聽只掛一次）",
   "ensureTutSpotlightRing398._wired" in src
   and 'window.addEventListener("resize"' in src
   and '.map-wrap' in src)
ok("v398 TUT_MAP 教學卡貼底（唔蓋聚光 pin）",
   "#mask.tut-on.tut-step-map{align-items:flex-end}" in src
   and 'mask.classList.toggle("tut-step-map", step.id==="TUT_MAP")' in src
   and 'mask.classList.remove("tut-step-map")' in src)
ok("v398 TUT_MAP 重複句只出一次（push 完即返，唔跌入 body／bodyAlt loop）",
   "st.body.push(LINE183); return;" in src)
ok("v398 WELCOME 聚光燈唔郁（照舊高亮 #btn-confirm-plan）",
   'if(stepId==="TUT_WELCOME" || stepId==="TUT_NOTEBOOK") sel="#btn-confirm-plan";' in src)

# ---- (2) 大地圖底邊截籤＋「今日」大卡 ----
ok("v398 夾實改用可見帶（polaroid 頂／日卡頂，唔係舞台底）",
   "function clampMapLabels397(){" in src
   and 'document.getElementById("map-polaroid")' in src
   and 'document.getElementById("map-hint")' in src)
ok("v398 夾實有頂邊夾（矮屏舞台頂伸出 polaroid 之外向下夾返）",
   "stageTop - rects[i].top" in src)
ok("v398 de-collide 之後再夾（settle 鏈重跑唔會漂移）",
   seg("function deCollideLabels363(){", "function stressScale363(").count("clampMapLabels397()") >= 1)
ok("v398 入地圖唔再彈「今日」大卡（日卡本身已經寫住同一句）",
   "toast(`今日：${meta.name}`" not in src
   and "toast(`今日行程：${meta.name}`" not in src
   and "今日：<b>${planName135}</b>" in src)
ok("v398 venue99 重疊修復唔郁（紅棉／金禧淨距）",
   "top:calc(24% + 30px)" in src)

# ---- (3) 35c 相片橫額＋P2 lead 淡出 ----
ok("v398 非金碟夜典禮裁橫額（cropBanner 旗＋渲染 class）",
   "cropBanner398" in src and "cropBanner: cropBanner398" in src
   and "np214-photo-cropbanner" in src
   and 'indexOf("金碟夜") < 0' in src)
ok("v398 裁橫額 CSS（鎖 520/550、貼底，燕尾服／獎座留低）",
   ".np214-photo.np214-photo-cropbanner{\n  aspect-ratio:520/550;" in src
   and "object-position:center bottom;" in src)
ok("v398 awi 相深裁（橫額文字底 ~150px，520/550 裁唔清，inline 520/500）",
   "p.key === 'np214_award_awi'" in src
   and 'style="aspect-ratio:520/500"' in src)
# v403 UI403-3（第十輪裁決改 fade）：26px mask 拆走，改紙邊「下接」提示；
# 驗證改為「唔洗字、唔露半截字」嘅結構條件（mask 不存在＋下接提示＋紙底留白保留）。
ok("v403 結果卡拆 26px mask（首屏唔洗字）",
   "calc(100% - 26px),transparent 100%)" not in src
   and "mask-image:linear-gradient(180deg,#000 calc(100% - 26px)" not in src)
ok("v403 結果卡紙邊下接提示＋紙底留白保留（捲到底完整）",
   "awd-next403" in src and "下接" in src
   and ".paper-sheet.awd-result396{ padding-bottom:32px; }" in src)
ok("v403 晨報不變（下接提示只限結果卡）",
   "awd403FoldAndHint" in src and '.awd-result396' in src)
ok("v398 金碟夜相本身唔郁（音樂典禮照用原相）",
   'np214_award_awi: "assets/story/newspaper/photo_awi_ceremony.webp"' in src)

# ---- (4) 通告欄頂部報表感＋底欄截印章＋86% 規則 ----
ok("v398 排序＋媒介合併做一粒「整理」掣（選項分兩組，功能唔減）",
   'data-board-menu397="organize"' in src and "整理 ▾" in src
   and "board-menu-group397" in src
   and 'data-board-menu397="sort"' not in src
   and 'data-board-menu397="filter"' not in src)
ok("v398 整理選單保留全部排序／篩選選項",
   'data-sort392="${k}"' in src and 'data-filter392="${m}"' in src
   and 'data-filter392="all"' in src
   and "board-sort392" in src and "board-filter392" in src)
ok("v398 總數行縮成紅印紙章（同一句，唔改數）",  # v399：改剪報標籤——虛線裁邊＋米紙底
   ".board-sum392{ display:inline-block;" in src
   and "border:1.5px dashed #9E2F2F;" in src)
ok("v398 板頭去報表工具列（透明貼紙底、冇框冇漸變，sticky 保留）",
   ".board-head392{ position:sticky; top:0;" in src
   and "background:var(--paper); border:0;" in src)  # --panel 係深啡 #3A3530，用佢會留返條深色報表帶；紙底先啱
ok("v398 列表成功率加「約」（詳情計法行註明用精確值）",
   "約 ${Math.round(chance(g)*100)}%" in src
   and "成功率用精確值" in src)
ok("v398 高版 modal 捲動區底 26px 淡出＋列表底墊",  # v399：底漸隱已刪（第 6 張 chips 行橫跨摺位，漸隱洗字）；底墊保留
   "#mask.board-tall392 #modal-inner{" not in src
   and ".gig-board-list{ padding-bottom:26px; }" in src)
ok("v398 計法本身唔郁（$378×86.3%÷4→$82）",
   "function boardExpCalc397(g){" in src and "四捨五入" in src)

# ---- (5) 日結卡場景唔一致＋黑 backdrop 家族 ----
ok("v398 modal() 掛 scene398（keepScene397 → 共享漸變 dim）",
   'maskEl.classList.toggle("scene398", !!(opts.keepScene397 || scene401));' in src  # v401 UI401-1：scenePaper401 同樣掛 scene398，keepScene397 觸發不變
   and 'classList.remove("scene398")' in src)
ok("v398 scene398 用 v396 日結漸變（頂 .10／底 .42）",
   "#mask.scene398{" in src
   and "rgba(0,0,0,.10) 0, rgba(0,0,0,.10) 48px, rgba(0,0,0,.42) 48px" in src)
ok("v398 日結家族 7 處 modal 用 scene 模式（27c×2／43／44×2／41／35_invite）",  # v399：試鏡等消息卡加入 scene 家族，10→11
   src.count("keepScene397:true") == 10)  # 7 新＋afterDayModal／presentRestSleepDayEnd 2 舊＋doAudition 1（v399）；presentStartScheduleConfirm45 已於 v404 隨確認閘刪除（11→10）
for _sig, _n, _label in [
        ("function confirmSpendDay(", 1, "43 確認卡"),
        ("function resolvePlannedDay(", 2, "27c 日結卡×2"),
        ("function rom159DateScene(", 2, "44 約會卡×2"),
        ("function openSettingsModal(", 1, "41 設定卡"),
        ("function presentAwardInvite(", 1, "35_invite 請柬")]:
    ok("v398 scene 模式：" + _label, fn_seg(_sig).count("keepScene397:true") == _n)
ok("v398 reconfirm helper 唔郁（確認框唔入 scene 家族）",
   "keepScene397" not in fn_seg("function confirmChoice236("))
ok("v398 休息卡 scene 模式唔郁（已有 keepScene397）",
   "keepScene397:true" in fn_seg("function presentRestSleepDayEnd("))

# ---- 唔郁嘅嘢：SAVE／softRev／?v= ----
ok("v398 SAVE key 不變 starVolunteer_map_v19w", "starVolunteer_map_v19w" in src)
ok("v398 softRev 不變 s107", 'SOFT_REV = "s107"' in src)
ok("v398 ?v= 不變 v=20a10", "v=20a10" in src)
ok("v398 靜態 <button 總數 111（v397：112，兩粒板掣合併做一粒）",
   src.count("<button") == 111)

print(f"\n{total[0] - len(fails)}/{total[0]} passed")
sys.exit(1 if fails else 0)
