# v20a114 TRAVEL114 靜態守門：每日入地點出行額度（上限 2 次；重入同一地點都計）。
# 覆蓋：① 常量逐字 TRAVEL114_DAILY_CAP = 2 ② openLoc 閘口喺 enc79 攔截之前、
#       被擋 toast 文案逐字 ③ 地圖 #map-hint 剩餘次數行＋travel-locked 鎖定視覺
#       ④ 呼叫點分類覆蓋：全部 openLoc( 呼叫點逐個核對——唔係帶免費旗就係喺計清單
#       入面（兩份清單寫死做 allowlist，漏咗任何一個呼叫點都要 FAIL）⑤ 基線不變：
#       SAVE key／softRev／產品 ?v=
# 行號以合併後 main 版 index.html 為準（v117 刪詳細區淨 −93 行後再實量；分類內容不變，
# 逐行經 difflib 對位舊 main 行內容核實，唔係得個常數偏移）。
# v110 再實量：OVR110 喺行 32182 之後加 16 行（snippet 14 行＋函數內呼叫 2 行），
# 行號 ≥32183 者 +16；<32183 不變（最近釘行 30269／34824，中間冇釘行）。
# v122 再實量：AUD91FIX 淨 +5 行（H2 35396 +1、closeModal 38524 +2、H1 46912 +2）；
# 行號 ≥35396 者 +1、≥38524 者 +3、≥46912 者 +5。qa122/resync_travel114.py 核實：
# v120 再實量：LOCFULL120 淨 +127 行（CSS 全屏幕一節＋註解＋fix1 貼底／tuck 修正 +124 行喺 3530 附近、
# AnchorOwner 註解 +3 行喺 53300 附近）；行號 ≥3530 者 +124、≥53300 者再 +3。
# qa120/resync_travel114.py 核實：44 個 openLoc( 呼叫點序列逐字一致、內容逐行相同，
# 純漂移（COUNT 13／FREE 27 不變，DEF 52492→52616、WRAPPER 43344→43468）。
# 44 個 openLoc( 呼叫點序列逐字一致、內容逐行相同，純漂移（COUNT 13／FREE 27 不變）。
# v119 再實量：DLG119 剪影模組淨 +152 行（CSS 4877 起 +15、GAZE／DLG119 模組／
# LEGACY／REG／pair 去重／chars 25979–27386 起累積至 +152）；行號按 difflib 對位
# 逐行實量（qa119/resync_travel114.py 核實：44 個 openLoc( 呼叫點序列逐字一致、
# 內容逐行相同，純漂移；COUNT 13／FREE 27 不變）。
# 用法：python3 tests/test_travel114_static.py [path-to-index.html]
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "..", "index.html")
with open(IDX, encoding="utf-8") as f:
    src = f.read()
lines = src.split("\n")

fails = []
def ck(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond: fails.append(name)
def info(msg): print("INFO " + msg)

# ---------- 基線不變 ----------
ck("SAVE key 不變", "starVolunteer_map_v19w" in src)
ck("softRev 不變", "s107" in src)
ck("產品 ?v= 不變", "v20a10" in src)

# ---------- 常量＋helpers ----------
ck("常量逐字 const TRAVEL114_DAILY_CAP = 2;", "const TRAVEL114_DAILY_CAP = 2;" in src)
for fn in ("travel114State", "travel114Remain", "travel114IsFree", "travel114TrySpend"):
    ck("helper %s 已定義" % fn, ("function %s(" % fn) in src)
ck("travel114IsFree 認 travelFree／encDone／forceRestore／wf4Done 四旗",
   all(x in src for x in ("opts.travelFree", "opts.encDone", "opts.forceRestore", "opts.wf4Done")))
ck("travel114IsFree 有屋企守衛（id === \"home\" 唔計）", 'id==="home"' in src)
ck("travel114IsFree 唔用 atLoc 做判據",
   "atLoc" not in src[src.find("function travel114IsFree("):src.find("function travel114TrySpend(")])
ck("lazy rollover 只睇 S.dayIndex（換日歸零，同一日重載唔重置）",
   "Number(S.travel114.day)!==day" in src and "S.travel114 = { day: day, used: 0 }" in src)

# ---------- openLoc 閘口位置＋被擋文案 ----------
i = src.find("function openLoc(id, opts){")
assert i >= 0
depth, j = 0, src.find("{", i)
for k in range(j, len(src)):
    if src[k] == "{": depth += 1
    elif src[k] == "}":
        depth -= 1
        if depth == 0: j = k; break
openloc = src[i:j + 1]
ck("openLoc 入面有額度閘（travel114TrySpend）", "travel114TrySpend(opts, id)" in openloc)
ck("閘喺 enc79TryIntercept 之前（被擋嘅入場唔擲巧遇）",
   openloc.find("travel114TrySpend(opts, id)") < openloc.find("enc79TryIntercept"))
ck("閘喺 todayIsForcedDay return 之後（強制日唔計）",
   openloc.find("todayIsForcedDay()") < openloc.find("travel114TrySpend(opts, id)"))
ck("被擋 toast 文案逐字（玩家面用「出行」，唔出內部名）",
   'toast("今日出行額度用完——今日已經去咗 2 個地方，聽日再去。")' in openloc)
ck("計數入場即 saveQ（重新載入唔可以刷返額度）",
   'if(typeof travel114IsFree==="function" && !travel114IsFree(opts, id)){ try{ saveQ(); }catch(_e){} }' in openloc)
ck("閘口用 typeof 守衛（同 enc79／wf4 攔截慣例一致，抽真 openLoc 嘅舊測試唔會炸）",
   'if(typeof travel114TrySpend==="function" && !travel114TrySpend(opts, id)){' in openloc)

# ---------- 地圖顯示＋鎖定視覺 ----------
ck("#map-hint 有剩餘次數行（map-hint-travel）", "map-hint-travel" in src)
ck("剩餘次數文案「今日出行：仲可以去 N 個地方」",
   "今日出行：仲可以去 ${rem114} 個地方" in src)
ck("用盡文案「今日出行額度已用完，聽日再去」", "今日出行額度已用完，聽日再去" in src)
ck("剩餘次數行由 travel114Remain() 計（drawMap 每次渲染刷新）",
   "const rem114 = travel114Remain();" in src)
ck("鎖定視覺 CSS 齊全（.pin.travel-locked＋.map-area-list button.travel-locked）",
   ".pin.travel-locked" in src and ".map-area-list button.travel-locked" in src)
ck("地圖釘加 travel-locked class（額度用完）", '${travelLocked114?" travel-locked":""}' in src)
ck("drawMap 計 travelLocked114（travel114Remain() <= 0）",
   "const travelLocked114 = (typeof travel114Remain===\"function\") ? travel114Remain() <= 0 : false;" in src)

# ---------- 呼叫點分類覆蓋（allowlist，行號＝改後實量） ----------
# 計清單（玩家主動導航，預設計數，唔加旗）：13 處
COUNT_LINES = {
    31757,  # ux68GoLoc 手帳「前往」
    35208,  # 訓練建議「去報名」
    37331,  # 訓練報名導航
    38329,  # 進度頁「去現場播劇情」
    38685,
    38688,  # 地圖釘 goPin（最近針／後備 L.id）
    38719,  # 地圖底欄地點掣
    43217,  # 人情債「去事務所」
    56804,  # inv72GoShop 去禮品檔
    56971,  # people72GoLoc
    57114,  # jobs72GoBoard
    57135,  # jobs72GoLoc
    57585,  # 開局屋企 modal「去睇劇情」
}
# 免費清單（帶旗，唔計）：27 處
FREE_LINES = {
    24421,  # 劇情播完刷新（markDone fallback）
    27878,  # 劇情播完刷新（leaveStory）
    30478,
    30479,
    30491,
    30492,
    30503,
    30504,  # 病倒流程送去 hospital（體檢／買體檢／醫院說明 modal）
    30607,  # 故事 seed 就緒，系統傳送去劇情地點
    40176,  # wf4Fire 完（wf4Done，舊旗）
    42874,  # 人情債流程尾，返去而家身處地點
    42897,  # 人情債「取消」，返去而家身處地點（brief 未列，同一理據）
    51685,
    51773,  # 巧遇播完（encDone，舊旗）
    52664,  # 劇情播完刷新（refreshLocAfterStory）
    53049,
    53071,  # 「劇情已完成」toast 後重開而家身處地點
    53206,  # 聽完傳聞後 reopen 而家身處地點
    54838,  # forceRestore（舊旗）
    56248,  # 傾談結果 modal go（唔耗日嗰條路，返去而家身處地點）
    56581,  # promptAudition back（返去而家身處地點）
    56699,
    56700,
    56735,
    56736,  # 禮物店／送禮 modal 關閉／dismiss 後重開而家身處地點
    56755,  # doGiveGift 失敗後重開而家身處地點
    56770,  # 送禮結果 modal go（唔耗日嗰條路，返去而家身處地點）
}
FREE_FLAGS = ("travelFree:true", "encDone:true", "forceRestore:true", "wf4Done:true")
DEF_LINE = 52777       # function openLoc(id, opts){
WRAPPER_LINE = 43629   # window.__phase2.openLoc：轉發 opts
# 頁內測試區：runSoftP0Checks 函數範圍（brace-match 實量，唔靠死行號）
def fn_range(start_pat):
    s = src.find(start_pat)
    assert s >= 0, start_pat
    d, j = 0, src.find("{", s)
    for k in range(j, len(src)):
        if src[k] == "{": d += 1
        elif src[k] == "}":
            d -= 1
            if d == 0: j = k; break
    return (src[:s].count("\n") + 1, src[:j].count("\n") + 1)
TEST_START, TEST_END = fn_range("function runSoftP0Checks(){")

unaccounted = []
for ln, line in enumerate(lines, 1):
    if "openLoc(" not in line:
        continue
    if ln == DEF_LINE:
        ck("openLoc 定義行 %d 係函數定義，唔係呼叫點" % ln, "function openLoc(id, opts){" in line)
        continue
    if ln == WRAPPER_LINE:
        ck("__phase2 wrapper 轉發 opts（openLoc(id, opts)）",
           "openLoc: function(id, opts){ openLoc(id, opts); }" in line)
        continue
    if TEST_START <= ln <= TEST_END:
        continue  # 頁內測試 code（57830）＋字串檢查（57872），唔改
    if any(f in line for f in FREE_FLAGS):
        if ln not in FREE_LINES:
            unaccounted.append((ln, "帶免費旗但唔喺 FREE_LINES：" + line.strip()[:90]))
        continue
    if ln in COUNT_LINES:
        continue
    unaccounted.append((ln, line.strip()[:90]))
ck("全部 openLoc( 呼叫點都有分類（免費旗／計清單／定義／wrapper／測試區），零漏網",
   not unaccounted)
for ln, why in unaccounted:
    print("UNACCOUNTED line %d: %s" % (ln, why))
for ln in sorted(FREE_LINES):
    ck("免費清單行 %d 實際帶旗" % ln,
       any(f in lines[ln - 1] for f in FREE_FLAGS))
for ln in sorted(COUNT_LINES):
    ck("計清單行 %d 實際冇帶旗（預設計數）" % ln,
       not any(f in lines[ln - 1] for f in FREE_FLAGS))
info("呼叫點分類：免費 %d 處＋計數 %d 處＋定義／wrapper／測試區 4 處" %
     (len(FREE_LINES), len(COUNT_LINES)))
info("頁內測試區 runSoftP0Checks 行 %d–%d（內含測試呼叫＋字串檢查，唔改）" % (TEST_START, TEST_END))

print("RESULT " + ("FAIL (%d)" % len(fails) if fails else "PASS"))
sys.exit(1 if fails else 0)
