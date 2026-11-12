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
# v20a130 resync：actFx102Html 喺行 55209 加 1 行（shoot 專屬 ?v=20a130 early
# return），行號 ≥55209 者 +1；<55209 不變。qa130/resync_travel114.py 核實：
# 44 個 openLoc( 呼叫點序列逐字一致、內容逐行相同，純漂移（COUNT 13／FREE 27 不變）。
# v20a125 resync：TEXT125 淨 +12 行（currentLine +4／advance +1／familySafe +7），行號跟 qa125/resync_travel114.py 重算。
# v20a131 resync：UI131 B2/B4 淨 +41 行（v131 CSS 段喺 </style> 前加 41 行；B3 原地改行數不變），
# 行號 ≥5236 者 +41；<5236 不變。qa131/resync_travel114.py 核實：44 個 openLoc( 呼叫點序列逐字一致、
# 內容逐行相同，純漂移（COUNT 13／FREE 27 不變）。
# v20a135 resync：MAP135 淨 −14 行（CSS 死規則清理淨 +1 行喺 5162 附近、paintBar 模板合併淨 −15 行喺 38396–38612；
# 行號 ≥5162 者 +1、≥38396 者再 −15，逐行內容經 difflib 對位核實純漂移）。qa135/resync_travel114.py 核實：
# v20a136 resync：ENDGATE136 淨行數見 qa136/resync_travel114.py 輸出（閘＋評估器＋評核＋文案）；
# v20a142 resync：A1 modal 歸零 ＋7 行＋focus setTimeout ＋1 行；A2a 進度頁「星途寄語」CSS ＋6 行＋HTML ＋9 行；A2b 作品牆空畫框 CSS ＋4 行＋HTML ＋2 行；B1 標籤錨微調原地改行數不變（另 ＋4 行註解）。
# 行號按 difflib 對位逐行實量（COUNT 13／FREE 27 不變，DEF 53369→53402、WRAPPER 44054→44087）。
# 44 個 openLoc( 呼叫點序列逐字一致、內容逐行相同，純漂移（COUNT 13／FREE 27 不變）。
# 44 個 openLoc( 呼叫點序列逐字一致、內容逐行相同，純漂移（COUNT 13／FREE 27 不變）。
# v20a135 文案 resync：地圖卡計劃＋出行合併做一行（用戶拍板），舊分行文案「今日出行：…」改合併行文案。
# v20a144 resync：ENC144 淨 +8 行（DAILY_CAP 改值原地／WEEKLY_CAP 新常數 +1 行喺 51232 後、
# starWeek lazy-init +1 行喺 51327 後、TryIntercept 週重置 +4 行喺 51853 後、每週檢查 +1 行喺 51871 後、
# 每週遞增 +1 行喺 51891 後）；行號 ≥51892 者 +8、其餘按逐行對位（qa144/resync_travel114.py 核實：
# 44 個 openLoc( 呼叫點序列逐字一致、內容逐行相同，純漂移；COUNT 13／FREE 27 不變，DEF 53143→53151）。
# v20a134 resync：WF4 覆寫表喺約行 40362 插入 28 行；行號 ＞40362 者 ＋28（已逐行實量核對：
# FREE 18 處＋COUNT 6 處＋DEF→53222＋WRAPPER→44009；v143 版行號已含佢嗰 +43）。
# v20a141 resync：BOOK141 淨 +62 行（CSS 段 ＋42／SVG defs ＋13／手帳 HTML 淨 ＋5／enterHome 註解 ＋2）；
# 行號 ≥5308 者 +60、≥37218 者再 +2（共 +62），逐行內容經對位核實純漂移。
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
# v20a135 MAP135：計劃＋出行合併做一行——「今日：〈計劃〉 · 仲可以去 N 個地方」；
# 額度用完變體同樣併入（「出行額度已用完，聽日再去」）。舊分行文案已刪。
ck("剩餘次數文案「仲可以去 N 個地方」（v135 合併行）",
   "仲可以去 ${rem135} 個地方" in src)
ck("用盡文案「出行額度已用完，聽日再去」（v135 合併行）", "出行額度已用完，聽日再去" in src)
ck("剩餘次數行由 travel114Remain() 計（paintBar 每次渲染刷新）",
   "const rem135 = travel114Remain();" in src)
ck("鎖定視覺 CSS 齊全（.pin.travel-locked＋.map-area-list button.travel-locked）",
   ".pin.travel-locked" in src and ".map-area-list button.travel-locked" in src)
ck("地圖釘加 travel-locked class（額度用完）", '${travelLocked114?" travel-locked":""}' in src)
ck("drawMap 計 travelLocked114（travel114Remain() <= 0）",
   "const travelLocked114 = (typeof travel114Remain===\"function\") ? travel114Remain() <= 0 : false;" in src)

# ---------- 呼叫點分類覆蓋（allowlist，行號＝改後實量；v20a137 MAP137 令行號移位：CSS ＋23／地區名 HTML －10／JS ＋73＋6＋2／resize ＋9，見 NOTES_V20A137_MAP.md；v20a144 ENC144 ＋8 行（WEEKLY_CAP／starWeek／每週重置）；v20a143 BOOK143 ＋43 行（CSS 段，全部錨點再 ＋43）；v20a147 AWARDS147 ＋67 行（贏線註解＋3／gallery 宣佈弧＋14／comfort beat＋6／comfort draw＋10／結果卡安慰行＋2／對手加權＋32，全部錨點再 ＋67） ----------
# v20a147 rebase 上 main 57d4081（v145）resync：v145 ＋67 行（CSS 段）全部錨點再 ＋67；difflib 對位核實——新舊 index.html 只差 1 行→68 行一個 replace 段，42 個釘行內容逐行相同，純漂移；COUNT 13／FREE 27 不變，DEF 53478→53545、WRAPPER 44087→44154（同 v145 版 44154 一致）。
# v20a147 D4 重做校準 resync：淨 ＋9 行（贏線註解 ＋2／YearOf 註解＋函數 ＋7；cap／scoreCategory 註解原地改行數不變）；行號 ≥45711 者 ＋9（qa147/resync_travel114.py 核實：44 個 openLoc( 呼叫點序列逐字一致、內容逐行相同，純漂移；COUNT 13／FREE 27 不變，DEF 53469→53478、WRAPPER 44087 不變）。
# v20a146 rebase 上 main 687a3a1（v147）resync：MASK146 CSS ＋8／modal 高帽 ＋2（其前錨點 ＋10）／B2 ＋5（其後錨點再 ＋5，合共 ＋15）；qa146/resync_travel114_147.py 核實：44 個 openLoc( 呼叫點序列逐字一致、內容逐行相同，純漂移；COUNT 13／FREE 27 不變，DEF 53545→53560、WRAPPER 44154→44169。
# v20a146 rebase B1 步 resync：覆寫表加 st05／st08 兩行（其後錨點 ＋2）；qa146/resync_travel114_147.py HEAD 核實：44 個 openLoc( 呼叫點序列逐字一致、內容逐行相同，純漂移；COUNT 13／FREE 27 不變，DEF 53560→53562、WRAPPER 44169→44171。
# 計清單（玩家主動導航，預設計數，唔加旗）：13 處
COUNT_LINES = {
    32132,  # ux68GoLoc 手帳「前往」
    35613,  # 訓練建議「去報名」
    37740,  # 訓練報名導航
    38734,  # 進度頁「去現場播劇情」
    39168,
    39171,  # 地圖釘 goPin（最近針／後備 L.id）
    39202,  # 地圖底欄地點掣
    43748,  # 人情債「去事務所」
    57592,  # inv72GoShop 去禮品檔
    57759,  # people72GoLoc
    57902,  # jobs72GoBoard
    57923,  # jobs72GoLoc
    58373,  # 開局屋企 modal「去睇劇情」
}
# 免費清單（帶旗，唔計）：27 處
FREE_LINES = {
    24772,  # 劇情播完刷新（markDone fallback）
    28267,  # 劇情播完刷新（leaveStory）
    30853,
    30854,
    30866,
    30867,
    30878,
    30879,  # 病倒流程送去 hospital（體檢／買體檢／醫院說明 modal）
    30982,  # 故事 seed 就緒，系統傳送去劇情地點
    40707,  # wf4Fire 完（wf4Done，舊旗）
    43405,  # 人情債流程尾，返去而家身處地點
    43428,  # 人情債「取消」，返去而家身處地點（brief 未列，同一理據）
    52437,
    52556,  # 巧遇播完（encDone，舊旗）
    53449,  # 劇情播完刷新（refreshLocAfterStory）
    53831,
    53853,  # 「劇情已完成」toast 後重開而家身處地點
    53988,  # 聽完傳聞後 reopen 而家身處地點
    55625,  # forceRestore（舊旗）
    57036,  # 傾談結果 modal go（唔耗日嗰條路，返去而家身處地點）
    57369,  # promptAudition back（返去而家身處地點）
    57487,
    57488,
    57523,
    57524,  # 禮物店／送禮 modal 關閉／dismiss 後重開而家身處地點
    57543,  # doGiveGift 失敗後重開而家身處地點
    57558,  # 送禮結果 modal go（唔耗日嗰條路，返去而家身處地點）
}
FREE_FLAGS = ("travelFree:true", "encDone:true", "forceRestore:true", "wf4Done:true")
DEF_LINE = 53562      # function openLoc(id, opts){
WRAPPER_LINE = 44171  # window.__phase2.openLoc：轉發 opts
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
        continue  # 頁內測試 code（57835）＋字串檢查（57877），唔改
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
