# v399：第七輪 UI 檢視頭五項必修 — 靜態測試（釘字串／接線／對比度實算）。
# 用法：python3 tests/test_v399_static.py [repo-root]
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


def _lum(hexs):
    h = hexs.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(fg, bg):
    l1, l2 = _lum(fg), _lum(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


# ---- (1) 設定深啡條對比度 9 項 fail ----
ok("v399 設定行改淺紙底配深墨字（唔再深啡 #4a433c 配近黑字）",
   ".settings-row{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:8px 10px;background:#fbf4dd;border:1px solid #a98d4f;border-radius:10px;color:#1a1410}" in src
   and ".settings-row .hint{font-size:.68rem;color:#5c4a1f;margin-top:2px}" in src)
ok("v399 設定行唔再用深啡 panel2 底",
   "background:var(--panel2)" not in seg(".settings-row{display:flex", ".settings-row select"))
ok("v399 設定 lab／hint／速度掣對比度實算全部 ≥4.5:1",
   ratio("#1a1410", "#fbf4dd") >= 4.5
   and ratio("#5c4a1f", "#fbf4dd") >= 4.5
   and ratio("#fff8e8", "#5c4a1f") >= 4.5)
ok("v399 已選速度 pill 改深底白字（唔再 cream on gold 3.03）",
   ".set-speed128 .set-speed-btn.on{ background:#5c4a1f; border-color:#3a2f14; color:#fff8e8; }" in src
   and "background:#c97f1f; border-color:#8a5a12; color:#fff8e8;" not in src)

# ---- (2) 43b／43c 黑背底 bottom-sheet ----
_aud = fn_seg("function doAudition(")
ok("v399 試鏡等消息卡用 scene 模式（同休息／訓練／病倒卡同一套）",
   "keepScene397:true" in _aud)
ok("v399 試鏡卡標題加「・等消息」，唔再令人誤解為已出結果",
   "<h3>試鏡完畢・等消息 ${gig.title}</h3>" in src
   and "<h3>試鏡完畢 ${gig.title}</h3>" not in src)
ok("v399 試鏡卡仍係同一隻掣＋同一條 cont 路（唔改流程）",
   '{label: ended?"回家結算":"繼續", role:"p", on:cont}' in _aud
   and "{onDismiss: cont, keepScene397:true}" in _aud)

# ---- (3) 教學聚光燈圈埋鄰居 ----
ok("v399 撞圈標籤暫隱＋目標標籤浮貼 helper 在位",
   "function ensureTutTargetLabel399(){" in src
   and "function restoreTutLabels399(){" in src
   and "function updateTutLabels399(ringRect, appRect){" in src
   and '#tut-target-label399{' in src
   and ".tut-label-hide399{ visibility:hidden; }" in src)
ok("v399 金圈定位後即避圈（refresh 內調 update，離開 step 1 即還原）",
   "updateTutLabels399({left: pr.left - pad" in src
   and 'if(!on){ ring.style.display = "none"; try{ restoreTutLabels399(); }catch(_e){} return; }' in src
   and "restoreTutLabels399();" in seg("function clearTutSpotlight(){", "function applyTutSpotlight("))
ok("v399 浮貼目標標籤上移 12px＋z 521 蓋過遮罩（原標籤同時隱藏）",
   'clone.style.top = (tr.top - appRect.top - 12) + "px";' in src
   and "z-index:521" in src
   and 'clone.textContent = "星河電視台";' in src)
ok("v399 金圈繼續跟 pin 中心（唔靠移偏避字）",
   "ring.style.left = (pr.left - ar.left - pad)" in src
   and "ring.style.top = (pr.top - ar.top - pad)" in src)

# ---- (4) 35c 右欄直排淡出截半行 ----
_awd = fn_seg("function renderAwardResultHtml(")
ok("v399 35c 右欄只留 outlet＋行首 6 字（fade 區前收尾）",
   'const sbLine399 = String(news.line || "").slice(0, 6);' in _awd
   and "${esc214(sbLine399)}</p>" in _awd)
ok("v399 35c 右欄唔再全文直排（舊寫法已換走）",
   '：</span>${esc214(news.line)}</p>' not in _awd)
ok("v399 35c 全文仍喺第二版主欄（唔失內容）",
   "<p>${esc214(news.line)}</p>" in _awd)
ok("v399 晨報渲染器唔郁（右欄模糊 filler 保留）",
   "np214-filler-v" in src)

# ---- (5) 通告欄底部漸隱洗字＋頂部報表感 ----
ok("v399 通告欄底漸隱已刪（摺位乾切，底墊保留）",
   "#mask.board-tall392 #modal-inner{" not in src
   and ".gig-board-list{ padding-bottom:26px; }" in src)
ok("v399 統計列改剪報標籤（虛線裁邊＋米紙底＋微斜）",
   "border:1.5px dashed #9E2F2F;" in src
   and "background:linear-gradient(100deg,#fff6dc,#f9edca 75%,#ead8ad);" in src)
ok("v399 「整理」縮成側邊紙籤（靠右自動闊，選單 200px 靠右掛籤下）",
   ".board-ctl397{ display:flex; justify-content:flex-end; margin-top:4px; }" in src
   and ".board-ctl397-btn{ width:auto; text-align:left; }" in src
   and ".board-menu397{ display:flex; flex-direction:column; gap:4px; margin-top:4px; width:200px; align-self:flex-end; }" in src)
ok("v399 整理選單選項唔減（排序 3＋媒介全部）",
   'data-board-menu397="organize"' in src and "整理 ▾" in src
   and 'data-sort392="${k}"' in src and 'data-filter392="${m}"' in src)
ok("v399 卡頂圖釘護欄（圖釘上移半出卡頂，標題唔郁）",
   '#app .gig-teaser::before{\n  content:""; position:absolute; top:-4px; left:50%;' in src
   and "#app .gig-teaser .gt-title{ margin:0 0 4px; }" in src)

print("TOTAL %d FAIL %d" % (total[0], len(fails)))
if fails:
    print("FAILURES:")
    for f in fails:
        print(" - " + f)
    sys.exit(1)
