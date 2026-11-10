# NOTES V20A66 — 年份推移包（1990–1992）

用戶 2026-11-10 06:20 拍板：成個遊戲改為 1990 年開始、三年 1990–1992，避開 1989 年 6 月 4 日嗰個時間點。
基底＝v20a65（線上 4,835,003 bytes／tests 64/64）。本包只郁年份鍵同年份文字，唔郁相對週數結構、
v65 四項修復邏輯、E1 門檻、頒獎贏線、内容包 JSON 本體。SAVE key／softRev／?v= 不變。

## 做法總覽（三層，全部行既有正規化／覆寫基建）

1. **曆法主樞紐**：`START.y 1988 → 1990`（保持 3 月 7 日開局、dayIndex 相對結構不變）。
   HUD 日期、報紙日期、手帳、週結、calib60YearOfWeek、awardsCalendarYear、yearSeasonNow 等
   全部由 dateObj()/START 衍生，自動跟移，逐個核實過。
2. **載入正規化層 remap（YEARS66）**：新增自含 block（`years66ShiftYear`／`years66ShiftText`／
   `years66Walk`／`years66GigRemap`／`years66MigrateSave`，`YEARS66_SHIFT=2`）。
   - gig：`normalizeGigRecord` 尾加 `years66GigRemap`——gig.year 欄＋文字欄（title/workTitle/
     roleLabel/blurb/synopsis 等）+2；`__y66w` 旗冪等；**gig id 不變**（存檔鍵／LEADSTAR59／
     POSTER59 以 id 為鍵，零改動自動跟移；程天諾「首年零出場」紅線係結構性，自動變 1990）。
   - 內容包：`refreshCopyPacksFromDisk` 內三段 walk（函數頂靜態覆寫表＋內嵌池；simple pack；
     story pack 喺主幹覆寫＋TEXTFIX 之後）；gigsByYear 賦值改鍵——檔案 gigs_1988.json → 鍵 **1990**、
     1989 → **1991**、1990 → **1992**、1991 → **1993**、1992 → **1994**（檔案名不變；包物件補
     `pack.year`；1993/1994 包＝原五年計劃年 4/5，推移後做完結後 freeplay 安全網，語義對稱）。
   - walker 跳過鍵：id、eraTag、gigId、loc、season、ceremonyId 等機器鍵不變；數字只移
     year/minYear/yearMin/yearEq/fromYear 等年份鍵。
3. **硬編碼邏輯位逐個 +2**：STORY_GATE_3Y（yearMin/yearEq）、CALIB60_NODE_WINDOWS、
   CONSEQ61_REVIEWS 鍵（地板 45/100、邊界週 43/95 不變）、生活費年份加級（1991 +$300／1992 +$600，
   金額同 fame 加級不變）、報紙 phase bump 年閘、PAPER_SIDE_ITEMS fromYear（程天諾預熱 → 1992）、
   移民潮鏈 F 閘（芬姐 1991 起、到期式 1991 夏或 ≥1992）、choice47 窗口（1992 秋；CHOICE47_DEFS
   year 字面改 1992）、GIGS36_BY_YEAR 鍵（1991/1992；入面 GIGS36_1989_* 變數名不變）、MID gigs
   注入年閘（1990)、syncGigsForCalendarYear 回退鏈、spPlayerMeta eraTag 顯示分支（eraTag 係舊曆
   編碼，顯示前 +2；when 已 walk 唔雙重移）。
   玩家面字面：副題「1990 · 片場星途」、新遊戲注腳、開場 modal「1990年3月7日」、結局／剪報
   年份文字（1992 年冬收科、E4/E7/去留文字 +2)、dualMeet fallback playerMeta。
   id 內嵌年份解析（awards62YearOf／work59YearOf／awards63GigYear fallback）加守衛 +2
   （1988–1992 → +2，其餘原樣），令舊編碼 id 派生嘅年份同新曆一致。

## 舊存檔遷移（epoch guard）

- `normalizeSaveObj` 開頭行 `years66MigrateSave(o)`（喺 calib60 補登同 conseq61 legacy 標記之前）：
  dayIndex 不變；conseq61.reviews 鍵、pendingEnding.year、ending410.careerVariant
  （review1988/1989 → review1990/1991)、earlyEnd.year、awardsFlags「YYYY/...」鍵、
  wrapHistory[].year、awardsLog 条目、報紙剪報／佇列年份字眼 remap；完成打 `years66Shifted=1` 戳。
- 新檔 `fresh()` 出生即打戳，遷移唔掂。遷移冪等（再載入唔會二次 +2）。

## 玩家面文字審計結果

- 敏感參照掃描：index.html ＋全部玩家內容包對 北京／天安門／六月／學運／坦克／戒嚴／鎮壓／民運／八九
  **零命中**（推移前已零命中；「風波」係粉絲／唱片公司語境、「廣場」係置地／太古廣場地名、
  「初夏」係 C5 台慶籌備嘅季節詞，均與事件無關，保留）。移民潮文字本身冇點名事件，
  靠年份閘遲移完成語境轉移（1990–94 移民高峰、1997 倒數焦慮）。
- 運行時審計（用 index 真函數行正規化後掃描，跳過機器鍵）：五個 gig 包、九個 story/detail 包、
  index 覆寫表（STORY_SPINE／HINT／CHOICE47／COMMIT48／FREEPLAY）、15 個衍生 gig 池——
  玩家可見字串入面 **「1988」「1989」出現次數 = 0**。
- index 源碼字面殘留（非玩家可見，分開交代）：gig/star id 鍵（~345 行）、eraTag 值（~201 行，
  機器鍵，顯示路徑已 shift-aware）、歷史 dev 註釋、dev 自測代碼、walk 表格嘅源頭字面
  （運行時由 YEARS66 walk 移走，harness 已證）。
- 既有內容債（推移前已存在、本包不改寫）：story 包部分 late 節點 `when`/synopsis 沿用五年版
  年份標籤（原 1991/1992），+2 後變 1993/1994——相對偏移同推移前一致；eraTag 衍生顯示
  （era_1992_finale 等）推移後反而同新曆對齊。原生移植回寫 pack 時一併清理（見回寫清單）。

## 測試

- 基線 64/64 守住；新增 test_years66_logic.js＋test_years66_static.py → **66/66**。
  新測試反證：喺 v65 index 上行 exit 1（YEARS66 block 不存在／21 項 static FAIL）。
- 既有測試更新（只改 sandbox 曆法同年份預期，金額／門檻／週數斷言不變）：
  test_calib60_logic（stub START 1990、DAY 基點、評核窗標籤）、test_conseq61_logic（年份鍵 +2)、
  test_fix65_logic（stub START；金額 2700/3000 不變）、test_giglib36_logic（sandbox +2、
  loadPack 用 gameYear−2 對返 fixture 檔名）、test_awards63_logic（fellows 查詢年 1990/1991)、
  test_pacing35／weave43／45／46／47／48／410 logic（sandbox 曆法 +2；const 名還原）、
  test_calib60／conseq61／fix65／weave42／45／47／48／410 static（年份閘字串 +2)。
- 真 UI 抽驗（gate-on、槽 3、本地鏡像 serve66）：新 game 副題 1990＋HUD「1990春」；
  真日流程過 wk43 週結 → reviews 鍵 **1990**（floor 45)、pendingEnding.year 1990；
  手帳獎項頁顯示「1990年6月15日」＋「海港電影獎入圍」、全頁冇 1988/1989；
  v65 形狀存檔實載 → dayIndex 不變、reviews [1990, 1991]、variant review1991、HUD「1991夏」。
  全程零 pageerror。證據喺 linji-work66/verify66/。

## 過程捉到嘅兩個真 bug（已修＋有測試守）

1. GIGS36_BY_YEAR 表格推移時誤改埋入面嘅變數名（GIGS36_1991_* vs 定義 GIGS36_1989_*）→
   已還原變數名、只改鍵。
2. awardsLog 遷移 explicit set 同 walk 雙重 +2（變 +4）→ 改為只行 walk；遷移測試覆蓋。

## 回寫清單（原生移植／內容包整理時處理）

- content pack JSON 本體仍載舊年份（gigs_1988–1992.json 檔名同內容、story 包年份標籤），
  靠 YEARS66 正規化層 remap；原生移植時要回寫 pack 本體或成層搬移 remap 邏輯。
- story 包 late 節點五年版年份標籤（見審計節）回寫時清理。
- dev 自測代碼（index 內 bad() 診斷）嘅 1988 基線期望未逐個更新——屬 dev 診斷、唔影響玩家面；
  原生移植唔使搬。
- LEADSTAR59 目前只回填首年（1990)137 部；1991/1992 選角表（linji-poster-casting-1990.md
  只含首年）同回填係後續批次，機制已預留。
