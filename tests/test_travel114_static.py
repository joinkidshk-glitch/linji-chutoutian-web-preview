# v20a195 resync：index.html 淨 +87 行（見 qa195/resync195.py difflib 對位核實純漂移），COUNT／FREE／DEF／WRAPPER 按段重算，總數不變。
# v20a114 TRAVEL114 靜態守門：每日入地點出行額度（上限 2 次；重入同一地點都計）。
# v20a191 resync：index.html 淨 +47 行（CSS +2／StoryPlay head +7／storyMainProgressLine +2／prog71 +36）；COUNT／FREE／DEF／WRAPPER 按段 +2／+9／+11／+47 重算，內容逐字核實純漂移，呼叫點總數不變。
# v20a191 rebase 上 main b3db32f resync：見 COUNT_LINES 區註解。
# 覆蓋：① 常量逐字 TRAVEL114_DAILY_CAP = 2 ② openLoc 閘口喺 enc79 攔截之前、
#       被擋 toast 文案逐字 ③ 地圖 #map-hint 剩餘次數行＋travel-locked 鎖定視覺
#       ④ 呼叫點分類覆蓋：全部 openLoc( 呼叫點逐個核對——唔係帶免費旗就係喺計清單
#       入面（兩份清單寫死做 allowlist，漏咗任何一個呼叫點都要 FAIL）⑤ 基線不變：
#       SAVE key／softRev／產品 ?v=
# 行號以合併後 main 版 index.html 為準（v117 刪詳細區淨 −93 行後再實量；分類內容不變，
# 逐行經 difflib 對位舊 main 行內容核實，唔係得個常數偏移）。
# v110 再實量：OVR110 喺行 32182 之後加 16 行（snippet 14 行＋函數內呼叫 2 行），
# 行號 ≥32197 者 +16；<32197 不變（最近釘行 30269／34824，中間冇釘行）。
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
# v20a156 EMPTY156 resync：CSS ＋15／PICKER156 ＋19／獎項空狀態 ＋2／剪報 ＋3／庫存 ＋2；qa156/resync156.py 核實：46 個錨點內容逐行相同，純漂移；COUNT 13／FREE 27 不變，DEF 53562→53601、WRAPPER 44171→44205。
  # v20a161 rebase 上 bf612bc（v155 先落地）resync：START161 淨 +14 行（插入段新行 4793-4806），
# 行號 ≥4793 者 +14；本檔釘行全部喺插入點之後，一律 +14（difflib 對位＋逐行錨點核實，見 qa161/resolve_rebase161_v155.py）。
# v20a155 rebase 上 main 9346a8e（v151＋v156）resync：v155 淨 ＋17（B1 註解 ＋6／B2 註解 ＋7／B3 ＋4），全部錨點再 ＋17；COUNT 13／FREE 27 不變，DEF 53601→53618、WRAPPER 44205→44222。
# v20a157 resync：splice 8 份 fragment（C6/C6F/1989/1990/C17/F4/G4/WF1）＋C17 synopsis 第2段改寫，行號純漂移；/tmp/resync114.py difflib 對位核實：44 個 openLoc( 呼叫點序列逐字一致、內容逐行相同；COUNT 13／FREE 27 不變，DEF 53562→53632、WRAPPER 44171→44241。
# v20a157 rebase 上 main 60b0a8f resync：main v152–v166 淨刪行＋splice 漂移（早段 −191／−185／−184、中段 −137、尾段 −22／−6／−4；qa131/resync_rebase157.py difflib 對位核實：42 個錨點內容逐行相同，純漂移；COUNT 13／FREE 27 不變，DEF 53632→53610、WRAPPER 44241→44104）。
# v20a146 rebase B1 步 resync：覆寫表加 st05／st08 兩行（其後錨點 ＋2）；qa146/resync_travel114_147.py HEAD 核實：44 個 openLoc( 呼叫點序列逐字一致、內容逐行相同，純漂移；COUNT 13／FREE 27 不變，DEF 53560→53562、WRAPPER 44169→44171。
# v20a160 rebase 上 main 222a984（v152）M1 步：淨 ＋7 行（M1 底圖常數段）；difflib 核實純漂移（3 replace 段、44 個 openLoc 呼叫點逐字一致、41 個釘行內容逐行相同）；COUNT 13／FREE 27 不變，DEF 53425→53432、WRAPPER 44029 不變。
# v20a160 rebase 上 main 222a984（v152）M4 步：淨 ＋37 行（walkup CSS ＋5／beats walkup ＋8／beat caption ＋2／PlayCeremony 其餘 ＋22；difflib 核實純漂移，44 個 openLoc 呼叫點逐字一致；COUNT 13／FREE 27 不變，DEF 53432→53469、WRAPPER 44029→44034；行號 ＜46131 者 ＋5，其後者 ＋37）。
# v20a160 rebase 上 main 222a984（v152）M6 步：淨 ＋30 行（tuxRec 預載 ＋8／drawTuxedo＋drawFigure 分流 ＋10／reveal won 燕尾服＋獎盃 glyph ＋5／glamour ＋1／常量 ＋7，減 4 行舊；difflib 核實純漂移，44 個 openLoc 呼叫點逐字一致；COUNT 13／FREE 27 不變，DEF 53469→53499、WRAPPER 44034 不變；行號 ≥46232 者 ＋30）。
# v20a160 rebase 上 main 222a984（v152）M9 步：淨 ＋41 行（fanfare 常數＋預載＋揭曉觸發）；difflib 核實純漂移，44 個 openLoc 呼叫點逐字一致；COUNT 13／FREE 27 不變，DEF 53499→53540、WRAPPER 44034 不變；行號 ≥46301 者 ＋41。
# v20a164 rebase 上 main 276ffa1（v160）resync：TANG164 事務所送禮掣 ＋16 行
# （base 53764–53779，v160 漂移 ＋115 → rebased 插入點 53879）；行號 ＞53879 者 ＋16；
# DEF 53540／WRAPPER 44034 喺插入點之前唔郁；COUNT 13／FREE 27 不變。
# v20a165 rebase 上 main 807440f（v157）resync：STORY165 淨 ＋42 行（goToMap 掛點 ＋8／新函數 ＋49／進度頁 −11／skip ＋9／beats ＋3／委派 −16）；qa165/resync_travel114_157.py 核實：difflib 只得 6 個 hunks，其餘純漂移；COUNT 13／FREE 27 不變，openLoc( 呼叫點總數 44 不變，DEF 53610→53668、WRAPPER 44104→44150。
# v20a165 (c) resync：(c) 3 hunks 淨 ＋31 行（story165ModalOpen helper ＋15／book70ExitHome 掛點 ＋7／#loc-close 包裝 −1＋10；modal 閘由 CanPlay 移出，見 NOTES §9）；qa165/resync_travel114_165c.py 核實：difflib 對 HEAD 只得 3 個 hunks，其餘純漂移；COUNT 13／FREE 27 不變，openLoc( 呼叫點總數 44 不變，DEF 53668→53690、WRAPPER 44150→44172。
# v20a170 rebase 上 main 56141a3 resync：淨 +2 行（FallbackStage 註解 2 行，插入點 L46098；FLOOR 原地改）；
# 行號 >=46098 者 +2，DEF 53690→53692、WRAPPER 44172 唔郁；COUNT 13／FREE 27 不變。
# v20a149 rebase 上 main e8c3a73（v170）resync：淨 ＋98 行（CSS ＋13／JS ＋85；v170 fallback +2 之上；difflib 核實 40 個釘行內容逐行相同，純漂移；reveal 行拆兩行原文令 ＋97→＋98）；COUNT 13／FREE 27 不變，DEF 53692→53790、WRAPPER 44172→44185。
# v20a149 fixup3（rebase 上 e8c3a73）：reveal 行融返一行（−1，插入點 L46602），淨 ＋98→＋97；COUNT 13／FREE 27 不變，DEF 53790→53789、WRAPPER 44185 唔郁。
# 計清單（玩家主動導航，預設計數，唔加旗）：12 處（v183 C9：開局 intro 改行免費，59358→FREE）
# v20a181 第二次 rebase 上 main 77603b3（v184）resync：v184 淨 ＋16（全部喺 45748–46484 之間）；COUNT 58691→58707、58869→58885、59012→59028、59033→59049，FREE 52884 之後 22 處各 ＋16，其餘唔郁；DEF 54631→54647、WRAPPER 44353 唔郁；COUNT 12／FREE 34 不變（difflib 雙基底對位核實純漂移，見 qa181/resync181_rebase2.py）。
# v20a186 resync：v186 淨 ＋4 行（結果卡同屆提名行移出逐類別卡，插入點 L45783–45826）；其後錨點各 ＋4（COUNT 58707→58711、58885→58889、59028→59032、59049→59053；FREE 52900 之後 22 處各 ＋4；DEF 54647→54651、WRAPPER 44353 唔郁）；COUNT 12／FREE 34 不變。
# v20a189 resync：index.html 淨 ＋34 行（accel-link CSS ＋15 @~1831／day-res 92dvh media ＋10 @~3235／hint 刪除 −10 @37990／soft map 掣 ＋3／accel link push ＋12／day-res class ＋4；difflib 對位核實純漂移，見 qa189/resync189.py）。
# v20a199 resync：index.html 淨 +44 行（DLG199 ＋30／fitApply ＋13／WF4 onload ＋1）；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重算，內容逐字核實純漂移。
# v20a200 rebase resync：index.html 淨 ＋12 行（C1 註解＋2／提示註解＋1／C2 註解＋分流＋6／nominee 標籤註解＋3；插入點 main L46187／46680／46767／47609；COUNT 12／FREE 34 不變，DEF 55204→55216、WRAPPER 44480 唔郁；qa200/resync200_rebase.py difflib 對位核實純漂移）。
# v20a189 rebase 上 main 0c29f03（v188）resync：淨 +254（v188；v190 淨 0）；COUNT／FREE／DEF 按段 +0／+254 映射（COUNT 12／FREE 34 不變，DEF 54685→54939、WRAPPER 44387 唔郁；difflib 對位核實純漂移，見 qa189/resync189_rebase.py）。
COUNT_LINES = {
    32230,  # ux68GoLoc 手帳「前往」
    35729,  # 訓練建議「去報名」
    37856,  # 訓練報名導航
    38898,  # 進度頁「去現場播劇情」
    39330,
    39333,  # 地圖釘 goPin（最近針／後備 L.id）
    39364,  # 地圖底欄地點掣
    43932,  # 人情債「去事務所」
    59276,  # inv72GoShop 去禮品檔
    59454,  # people72GoLoc
    59600,  # jobs72GoBoard
    59621,  # jobs72GoLoc
}
# 免費清單（帶旗，唔計）：34 處（舊 27 減 2 條改行 back176 守衛，加 ROM176 新 8 處＋v183 C9 intro 1 處）
FREE_LINES = {
    24686,  # 劇情播完刷新（markDone fallback）
    28275,  # 劇情播完刷新（leaveStory）
    30897,
    30898,
    30910,
    30911,
    30922,
    30923,  # 病倒流程送去 hospital（體檢／買體檢／醫院說明 modal）
    31026,  # 故事 seed 就緒，系統傳送去劇情地點
    40887,  # wf4Fire 完（wf4Done，舊旗）
    43589,  # 人情債流程尾，返去而家身處地點
    43612,  # 人情債「取消」，返去而家身處地點（brief 未列，同一理據）
    53469,
    53588,  # 巧遇播完（encDone，舊旗）
    53638,  # v176 星巧遇送禮掣 fallback（encDone）
    53861,  # v176 女角巧遇 def-missing（encDone）
    53900,  # v176 女角巧遇「行開」（encDone）
    53906,  # v176 女角巧遇 onDismiss（encDone）
    53973,  # v176 星送禮 canGive-fail（encDone）
    53975,  # v176 星送禮冇 item（encDone）
    53978,  # v176 星送禮冇庫存（encDone）
    54005,  # v176 星送禮結果 modal go（encDone）
    55116,  # 劇情播完刷新（refreshLocAfterStory）
    55490,
    55512,  # 「劇情已完成」toast 後重開而家身處地點
    55663,  # 聽完傳聞後 reopen 而家身處地點
    57300,  # forceRestore（舊旗）
    59044,  # promptAudition back（返去而家身處地點）
    59162,
    59163,
    59198,
    59199,  # 禮物店／送禮 modal 關閉／dismiss 後重開而家身處地點
    59224,  # doGiveGift 失敗後重開而家身處地點
    60071,  # v183 C9 開局 intro「去睇劇情」掣（travelFree，唔計額度）
}
FREE_FLAGS = ("travelFree:true", "encDone:true", "forceRestore:true", "wf4Done:true")
DEF_LINE = 55216      # function openLoc(id, opts){  # v20a200 rebase：＋12
WRAPPER_LINE = 44480  # window.__phase2.openLoc：轉發 opts
# v20a198 resync：index.html 淨 −7 行（C1 死 code 刪 −43／B1 守衛 ＋12／C2＋C3 ＋24）；/tmp/resync198.py difflib 對位核實 73 個錨點內容逐行相同，純漂移；COUNT 12／FREE 34 不變。
# v20a191 rebase 上 main b3db32f resync：v189 淨 +34 行＋v191 淨 +47 行；COUNT／FREE／DEF／WRAPPER 按兩段 shift 重算，difflib 對位核實純漂移。
# v20a176 resync：NPCS ＋7／星收尾掣 ＋12／ROM176 block ＋501／茶聽 ＋12／addLoc −13／openLoc 掛點 ＋5／
# doGiveGift ＋4／人脈頁 ＋10，淨 ＋538 行；qa176/resync176.py 逐行核實全部釘行內容逐字相同（純漂移），
# 新 8 處 encDone 係 ROM176 返程（星送禮 fallback 1＋女角巧遇 3＋星送禮 4）；doTalk／doGiveGift 兩條 go
# 改行 rom176BackOpts()（結構上只返 {encDone:true} 或 {travelFree:true}），由 back176 規則認，唔入 FREE_LINES。
# 呼叫點總數 44→52（免費 33＋計數 13＋定義／wrapper／測試區 4＋back176 2）。# v20a176 rebase 上 main a41b789（v179）resync：main 淨 ＋15（27110／38436／44078 各 ＋5），
# COUNT／FREE／DEF／WRAPPER 按段 ＋0／＋5／＋10／＋15（grep openLoc( 逐行核對），總數 52 不變。
# v20a176 rebase 上 main 91f264a（v175）resync：v175 淨 ＋78，COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫（qa176/resync176_rebase.py），總數 52 不變。
# v20a153 第三輪 rebase 上 main a500536（v149）resync：difflib 對位核實純漂移，COUNT/FREE/DEF/WRAPPER 行號按映射重寫（見 qa153/resync_rebase153c.py）。
# v20a182 resync：v182 淨 ＋17 行（CSS＋2／請柬＋4／presentAwardInvite＋6／C1 JS＋5）；＜45746 者 ＋2、其後者 ＋17，COUNT 13／FREE 33 不變，DEF 54493→54510、WRAPPER 44335→44337（qa182/resync182.py difflib 對位核實純漂移）。
# v20a172 rebase 上 main a500536（v149）resync：v149 淨 ＋97；＜45594 者 ＋13、典禮區後者 ＋97，DEF 53707→53804、WRAPPER 44187→44200；COUNT 13／FREE 27 不變（qa172/resync172b.py difflib 對位核實）。
# v20a172 rebase 上 main e2add29（v174）resync：COUNT／FREE 按段 ＋0／＋5／＋10／＋15，DEF 53860→53875、WRAPPER 44235→44250（qa172/resync172c.py difflib 對位核實純漂移）。
# v20a175 rebase 上 main f09fa1b（v177）resync：index.html 淨 ＋78（CSS ＋10／toast() ＋15／helpers ＋51／adopt ＋2）；錨點逐行核實內容逐字相同，純漂移（＜33710 者 ＋10、33711–44131 者 ＋25、≥44223 者 ＋78；COUNT 13／FREE 27 不變，DEF 53875→53953、WRAPPER 44250→44328）。
# v20a178 第二次 rebase 上 main 91f264a（v175）resync：v178 ＋25 行（註解＋1／sprite＋3／fellows＋21，插入點新行號 46815／46850／46993；其後者 ＋25、之前者唔郁）；COUNT 13／FREE 27 不變，DEF 53953→53978、WRAPPER 44328 唔郁（qa178/resync178b.py difflib 對位核實純漂移；三檔 rebase 衝突後以 v175 版為底重算）。
# v20a178 strip 上 91f264a resync：strip 淨 −4 行（註解＋1／sprite＋3，刪除點舊行號 46815／46852–46854；其後者 −4、之前者唔郁）；COUNT 13／FREE 27 不變，DEF 53978→53974、WRAPPER 44328 唔郁（qa178/resync178c.py difflib 對位核實純漂移）。
# v20a183 resync：v183 淨 ＋117 行（C7 CSS ＋2／prefKind ＋1／TryIntercept ＋1／PlayEncounter ＋2／ROM183 block ＋107／確認 modal ＋3／goBit ＋1；difflib 對位核實純漂移，見 qa183/resync183.py）。
# v20a184 rebase 上 main 0f90dc7（v183）resync：v184 淨 ＋16 行（C2 helper＋9／請柬＋1／結果卡＋1／C1 DEEPS＋4／漸變＋1 淨）；＜45748 者唔郁、其後者 ＋16（difflib 對位核實純漂移，見 qa184/resync184_rebase.py）。
# v20a184 resync（travel114）：COUNT 12／FREE 34 不變，DEF 54623→54639、WRAPPER 44340 唔郁。
# v20a176 第三輪 rebase 上 main c682cc2（v178）resync：v178 淨 ＋21（fellows 特別名額＋21，插入點 46993 之後者 ＋21）；COUNT 13／FREE 33 不變，DEF 54472→54493、WRAPPER 44335 唔郁（qa176/resync176_rebase3.py difflib 對位核實純漂移；三檔 rebase 衝突後取 v176 嗰邊，v178 註解行補返）。
# v20a181 resync：index.html 淨 ＋8（awards CSS ＋13／頒獎禮區淨 −26／尾段 ＋8）；difflib 對位核實 44 個 openLoc( 呼叫點內容逐行相同，純漂移（＜45175 者 ＋13、≥52828 者 ＋8；COUNT 13／FREE 27 不變，DEF 53953→53961、WRAPPER 44328→44341）。
# v20a188 resync：index.html 淨 +225 行（AWARDS188 覆寫表＋角色閘，插入點 L45380–46310）；其後釘行各 +225，之前唔郁；總行數 60155→60380。
# v20a188 resync 補 +29：上一手 +225 計少咗其後再加嘅 NP_WIN 覆寫＋load 呼叫＋gate 行＋debug 入口（淨 +29）；總淨變 +254，總行數 60409；difflib 對位核實全部錨點純漂移，見 qa188/resync188_verify.py。
# v20a181 rebase 上 main 9640c6f（v183）resync：v181 淨 ＋8 疊喺 main 之上，總行數 60127→60135；掃描全部 52 個 openLoc( 呼叫點逐行核對，COUNT 12／FREE 34 不變（v176 8 處 encDone＋v183 C9 intro 免費照舊），DEF 54623→54631、WRAPPER 44340→44353。
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
    if "back176" in line:
        # v176：rom176BackOpts() 返程守衛——只返 {encDone:true} 或 {travelFree:true}，結構上免費。
        # doTalk／doGiveGift 兩條 go 行呢個（舊 FREE 57350／57872 嗰兩行）；openGiftPick 取消／dismiss
        # 兩行同時帶 back176＋travelFree:true 字面，留喺 FREE_LINES，逐行旗檢查照過。
        continue
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
info("呼叫點分類：免費 %d 處＋計數 %d 處＋back176 守衛 2 處＋定義／wrapper／測試區 4 處" %
     (len(FREE_LINES), len(COUNT_LINES)))
info("頁內測試區 runSoftP0Checks 行 %d–%d（內含測試呼叫＋字串檢查，唔改）" % (TEST_START, TEST_END))

print("RESULT " + ("FAIL (%d)" % len(fails) if fails else "PASS"))
sys.exit(1 if fails else 0)
