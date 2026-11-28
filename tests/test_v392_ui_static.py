# v416：頒獎快進提示改揭曉下一張，斷言跟新文案。
# v404 意圖更新：確認閘成個刪走（用戶拍板），v392 掣名斷言改做「已刪」。
#!/usr/bin/env python3
# v392 UI 檢視修正（第三輪頭五項）靜態守門：五項呈現層修法嘅關鍵標記在位＋對比度守門。
# 只驗靜態標記（實駕量度見 ~/workspace/linji-drive392/verify/measurements.json）；
# 數值／邏輯／文案零改動由其他測試守。
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "..", "index.html")
with open(IDX, encoding="utf-8") as f:
    src = f.read()

fails = []


def ok(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)


def lum(hexcol):
    h = hexcol.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def f(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = f(r), f(g), f(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg, bg):
    l1, l2 = sorted((lum(fg), lum(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


# --- v392 CSS 區塊在位 ---
m = re.search(r"/\* ===== v392 UI392：.*?/\* ===== v392 UI392 完 ===== \*/", src, re.S)
ok("v392 CSS 區塊在位", bool(m))

# --- (1) 日結／休息卡家族：dismiss 唔再推進日期 ---
ok("1 afterDayModal dismiss 非週結＝null", "const dismissFn = ended ? go : null;" in src)
ok("1 日結 modal dismiss 非週結＝null", "const dismissNb = ended ? nextNbReward : null;" in src)
ok("1 休息卡 dismiss 非週結＝null", "const dismissFn = ended ? goSchedule : null;" in src)
ok("1 dayEndDismissNote202 已刪", "function dayEndDismissNote202(" not in src)
ok("1 「點擊外面＝」細字已清（玩家面）",
    "點擊外面＝繼續跑明日行程" not in src and "點擊外面＝返回地圖" not in src
    and "點擊外面＝回家結算" not in src and "點擊外面＝開始今日行程" not in src)
ok("1 確認金掣已隨確認閘刪除（v404）", "開始並結算當日" not in src)
ok("1 取消掣已隨確認閘刪除（v404）", "返回休息卡" not in src)

# --- (2) 39 拍攝排程：刪「取消」、金色畀安全選項 ---
ok("2 confirmPlaceShoot 無獨立「取消」掣（去重後兩個出口＋安全主掣）",
    "go(false, true)" in src and "留待下週" in src and "取消原安排並拍攝" in src)
ok("2 警告講明損失（會取消＋改為拍攝）", "會取消" in src and "改為拍攝" in src)
ok("2 警告深紅 .shoot-warn392", ".shoot-warn392{ color:#9c2418" in src)
ok("2 警告深紅贏到 modal p !important（#mask:not(.tut-on) .modal p.shoot-warn392）",
    "#mask:not(.tut-on) .modal p.shoot-warn392{ color:#9c2418 !important; }" in src)
c = contrast("#9c2418", "#fbf2da")
ok("2 警告深紅對紙底 ≥4.5:1（實算 %.2f:1）" % c, c >= 4.5)
c2 = contrast("#9c2418", "#f3e5c3")
ok("2 警告深紅對紙底變體 ≥4.5:1（實算 %.2f:1）" % c2, c2 >= 4.5)
ok("2 confirmPlaceShoot 無 onDismiss（撳遮罩只收起）",
    "confirmPlaceShoot" in src and "onDismiss: undefined" not in src)

# --- (3) 通告欄峰值分層 ---
ok("3 board392ExpDaily 在位（預期日薪＝成功率×片酬÷日數）", "function board392ExpDaily(g)" in src)
ok("3 board392Compare 在位", "function board392Compare(a, b, key)" in src)
ok("3 板頂總數行 board-sum392", "board-sum392" in src and "共 " in src and "可報名 " in src)
ok("3 排序掣 data-sort392（預期日薪／總片酬／成功率）",
    "data-sort392" in src and '["exp","pay","chance"]' in src
    and "預期日薪" in src and "總片酬" in src and "成功率" in src)
ok("3 媒介篩選掣 data-filter392", "data-filter392" in src)
ok("3 板頭 sticky 釘住", ".board-head392{ position:sticky; top:0;" in src)
ok("3 推介卡 gt-featured＋推介標籤", "gt-featured" in src and "推介" in src)
ok("3 未達標組有「最接近」預覽行", "board-closest392" in src and "最接近：" in src)
ok("3 短卡 meta 併一行（$｜日｜%）", "metaLine392" in src)
ok("3 0 張可報名直寫「今日沒有可報名試鏡的通告」", "今日沒有可報名試鏡的通告" in src)
ok("3 細板（≤3 張）唔加分層（layered392 門檻）", "layered392 = shown.length > 3" in src)
ok("3 gt-meta／gt-meta-line class 保留（s30 測試釘住）",
    ".gt-meta" in src and ".gt-meta-line" in src)

# --- (4) 18 拍攝簿截字 ---
ok("4 作品頁整頁捲動（#home-pane-works overflow-y:auto）",
    "#app #home-pane-works{ overflow-y:auto;" in src)
ok("4 works-list 唔再被 flex 夾扁（flex:0 0 auto；overflow:visible）",
    "#app #home-pane-works #works-list{ flex:0 0 auto; overflow:visible; }" in src)
ok("4 稱號段本身無郁（tags389-fold 規則原位）", ".tags389-fold{ margin-top:10px; }" in src)

# --- (5) 35 頒獎系列 ---
# tap div 喺 skip 掣之前（唔係之後）：buttons197／awards166 釘死咗
# 'skip</button>' + '</div>' + glamHtml 相鄰，tap 插喺中間會斷咗條釘；tap 係
# absolute 左下角，DOM 前後唔影響視覺位置，依然同跳過掣同一列。
ok("5 快進提示搬入 canvaswrap（同跳過掣同一列，喺跳過掣之前）",
    '<div class="awd62-tap">點擊畫面揭曉下一張</div><button type="button" class="awd62-skip">' in src)
c3 = contrast("#d6cdf0", "#14101f")
ok("5 快進提示 #d6cdf0 對舞台暗底 ≥4.5:1（實算 %.2f:1）" % c3, c3 >= 4.5)
c4 = contrast("#d6cdf0", "#2c2148")
ok("5 快進提示對 #2c2148 ≥4.5:1（實算 %.2f:1）" % c4, c4 >= 4.5)
ok("5 吊牌先後 syncBoardSub392 在位", "function" in src and "syncBoardSub392" in src)
ok("5 逐位宣佈字幕唔再重複名＋作品（只留進度）",
    "syncBoardSub392 500ms 後先揭" in src)
ok("5 未揭曉卡實色卡背（.awd63-card:not(.show)::before）",
    ".awd63-card:not(.show)::before" in src)
ok("5 未揭曉卡隱藏卡面（img／csscard／名／作品 visibility:hidden）",
    ".awd63-card:not(.show) img" in src and ".awd63-card:not(.show) .t" in src)
ok("5 得主角標未揭嗰陣隱藏（唔洩露）", ".awd63-card:not(.show).win::after{ display:none; }" in src)
ok("5 頒獎結果卡 .awd-sheet 未郁（今輪未驗證）", ".awd-sheet" in src)

# 3 TDZ 回歸（2026-11-24 實駕捉到）：gigBoardTeaserHtml 嘅 meta-line 區塊讀 boardState，
# boardState 嘅 const 聲明必須喺嗰行之前，否則一撳通告欄即 ReferenceError、板面唔開。
_fn_start = src.index("function gigBoardTeaserHtml")
_fn_end = src.index("\nfunction ", _fn_start + 10)
_fn = src[_fn_start:_fn_end]
_decl = _fn.index("const boardState =")
_read = _fn.index('if(boardState==="ready")')
ok("3 boardState 聲明喺 meta-line 讀取之前（唔撞 TDZ）", _decl < _read)
ok("3 gigBoardTeaserHtml 內 boardState 只聲明一次", _fn.count("const boardState =") == 1)
ok("3 通告欄高版 modal（boardTall opt → 92dvh）",
    "boardTall" in src and "#mask.board-tall392 .modal{ max-height:min(92dvh,92svh,780px) !important; }" in src)
ok("3 高版 modal 喺 closeModal 清除（唔漏去下一張 modal）",
    'classList.remove("board-tall392")' in src)
ok("3 doScout 傳 boardTall:true", "boardTall: true" in src)

print()
if fails:
    print("FAILURES: %d -> %s" % (len(fails), " | ".join(fails)))
    sys.exit(1)
print("ALL PASS")
