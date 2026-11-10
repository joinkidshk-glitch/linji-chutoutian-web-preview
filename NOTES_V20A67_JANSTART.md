# NOTES V20A67 — 1 月開局＋足 3 年包（JAN67）

用戶 2026-11-10 10:21–10:23 拍板：改做 1990 年 1 月開局，遊戲時間足 3 年（1990 年 1 月 → 1992 年尾）；
年終評核跟住移去第 52／104 週（對返曆法年尾）。取代 v20a66 嘅 3 月開局（嗰個係令 wk43 評核落喺
年尾嘅取巧對位，1 月開局後唔再需要）。
基底＝v20a66（線上 4,844,087 bytes／tests 66/66）。唔郁：v65/v66 全部數值（壓力、經濟金額、
頒獎公式、E1 門檻）、相對節奏、內容包 JSON 本體。SAVE key／softRev／?v= 不變。

## 逐項改動

1. **START 改 1990-01-01**（原 1990-03-07）。1990-01-01 本身係星期一，同原設計週一起點夾。
   全程 day 0–1095 = 1990-01-01 至 1992-12-31，足 3 年；結局閘維持「1992 冬＋前置節點」事件閘
   唔改判定（冬 1992 ≈ 12 月自然落喺 day ~1060+）。HUD／報紙／手帳／週結全部由 dateObj() 衍生，
   逐個核實跟移；開局季節變**冬**。
2. **年終評核移位**：CONSEQ61_REVIEWS 邊界週 wk43 → **wk52**、wk95 → **wk104**；地板／警告線
   （45/65、100/130）不變；reviews 年份鍵維持 1990/1991。警告週位自動跟移：警告喺
   conseq61SettleEval 以 `dist = boundaryWeek − w`（1–4 週）衍生，即 wk48–51／wk100–103，
   唔使另改。評核守衛 `calib60YearOfWeek(boundaryWeek) === Y` 對新週位成立
   （wk52 首日 1990-12-24 → 1990；wk104 首日 1991-12-23 → 1991）。
3. **JAN67 block**（插喺 YEARS66 block 之後）：`JAN67_DAY_SHIFT=65`、日戳 allowlist
   `JAN67_DAY_KEYS`、`jan67ShiftDayStamps`（遞迴 walker）、`jan67MigrateSave`（epoch guard）、
   `JAN67_OPENING_TEXT_MAP`＋`jan67OpeningTextFix`（開局文字對位）。fresh() 出生打
   `startEpoch67:1` 戳。
4. **開局文字對位接線**：`refreshCopyPacksFromDisk` 三處——內嵌 BEATS／TUTORIAL（YEARS66 walk 後）、
   disk simple pack（c/d）、story pack main（C1 when 標籤）。全部行既有正規化基建，內容包本體唔郁。
5. **B01 開場 modal 日期改動態衍生**（dateObj() 格式化，fallback 字面「1990年1月1日」），
   唔再硬編碼「1990年3月7日」。
6. **開始畫面**：印章「一九八八」→「一九九零」（HTML div＋SVG 水印「香江 · 一九九零」＋CSS 註釋，
   全檔「一九八八」已清零——呢個係 v66 漏咗嘅中文數字版年份標記，本身同副題一對）；
   新遊戲按鈕注腳「1990 年春」→「1990 年冬」；副題「1990 · 片場星途」不變。
7. **softC10WindowActive 改年內週**：舊絕對週 40–43 係 3 月 epoch 嘅「年尾」近似；改用
   `((week−1)%52)+1` 第 49–52 週對位（每年 12 月），語義不變、跨年唔再錯位。
8. **人情債冬季開局卡來歷補完**（DEBT_ORIGIN_LINES34 加 card_biao_winter／card_may_winter）：
   1 月開局當季卡由春季對變冬季對，初版只有春季兩卡有「來歷」文案，冬季兩卡會缺——
   各補一句（阿標頂更人情、美兒精華液未交貨），語氣跟現有兩句；春季對保留春季照用。

## 週錨定盤點結論（逐個過，同新曆法對位）

- **CALIB60_NODE_WINDOWS／STORY_GATE_3Y pacing.weekMin**：相對節奏，**唔郁**。gate 全用
  yearMin/yearEq＋seasonIn 曆法閘做主導；新 epoch 下各 weekMin（C6=15…C13=144）全部早過或貼近
  其曆法閘開窗，節點開窗月份不變、尾段唔會壓縮（C13/C17 由 1992 冬曆法閘釘住 ≈ wk149+；
  總跨度 ~156 週＝足 3 年）。章節 chapterIdForWeek（Ch1 wk1–2 起）係相對節奏，唔郁。
- **生活費緩坡週段（wk1–4 $1100／5–12 $1300／13–26 $1500／27–43 $1700）**：**唔跟移**。
  緩坡用途係保開局現金流，唔係同評核對位；wk43→44 跳幅 $700 細過 v66 時代連年份加級嘅 $1000；
  新曆法首年總生活費約 $86,300 vs v66 約 $89,000，微降冇罅。已喺 livingCostBand 加註釋交代。
- **CALIB60 生活費年份加級（1991 +$300／1992 +$600）**：按 `calib60YearOfWeek` 真日曆年觸發，
  自動跟移——1 月 epoch 下 +$300 實際由 wk54 起（wk53 首日係 1990-12-31，仍屬 1990）。
- **頒獎**：awards62SeasonHints／awardsSeasonMatches／awardsCalendarYear 全曆法衍生，自動跟移；
  awardsWeekOk 只讀 schema 嘅 weekMinSoft 相對下限，唔破壞。抽驗：第一年典禮月份對位正常。
- **移民潮年份閘**：v66 已移（芬姐 1991 起、到期 1991 夏或 ≥1992），全曆法衍生，同新 epoch 冇打架
  （weave42 測試以新 epoch 重對位觸發日後 PASS）。
- **人情債季節卡（SEASON_COLLECT）**：四季齊全按當前季節出場，1 月開局自然出冬季卡，系統自洽；
  冬季卡來歷文案已補（見改動 8）。

## 開局文字審計清單（春 → 冬）

| 位置 | 處理 |
|---|---|
| 開始畫面印章／水印「一九八八」 | →「一九九零」（v66 漏網，今包清零） |
| 新遊戲按鈕「1990 年春 · 由零開始」 | →「1990 年冬 · 由零開始」 |
| B01 modal 硬編碼「1990年3月7日 · 阿偉的家」 | → 動態衍生（開局自然出 1990年1月1日） |
| Ch1 開場白「1990 年春，阿偉在黃大仙屋邨起步。」（beats pack＋內嵌 fallback） | jan67OpeningTextFix 全句定點對照 →「1990 年初，…」（唔綁季節講法；只對照呢句，唔誤傷其他春季劇情） |
| 教學 TUT_WELCOME「1990 年春，你在黃大仙屋邨當臨記起步。」 | 同上 →「1990 年初，…」 |
| C1 節點 when 標籤「1990春 / W1-4」（story picker 玩家可見） | 只限 C1：→「1990冬 / W1-4」 |
| Ch4「春夏小結」 | **保留**：新曆法 wk10 ＝ 3 月＝春，章節總結對得返 |
| 其餘春季意象（春季劇情／季節卡／春季通告） | 唔郁——春季係遊戲入面真實存在嘅季節，只係唔再係開局 |

## 舊存檔遷移（+65 日偏移）

- 方針：v66 或更早（3 月 epoch）存檔載入時，全部絕對日戳 **+65 日**（1990-01-01 → 03-07 相差 65 日），
  令玩家嘅曆法日期不變（玩到 1990 年 6 月，遷移後仍係 1990 年 6 月）。
- 機制：`normalizeSaveObj` 內接線次序＝ years66MigrateSave → **jan67MigrateSave** →
  calib60MissedScan → conseq61LegacyMark（後兩者用新 epoch 解讀 dayIndex，所以 jan67 必須喺佢哋之前）。
  guard＝冇 `startEpoch67` 戳先行；行完打戳，冪等（新檔出生已打戳、已遷移檔唔會二次偏移）。
- 日戳範圍（allowlist，遞迴全檔）：dayIndex、shoots deadlineDay/hiredAtDay、enqueuedDay、publishDay、
  wrappedDay、債項 dueDay、story.lastMainDoneDay、giftMeta.lastGiveDay（map 值逐個移）、
  conseq61.cooldownUntil、mapTips.untilDay、newspaperLastPresentedDay、familyHome seedDay/paidDay/
  seedFlavorDay/paidFlavorDay；病倒窗 conseq61.sick.from/to 點名移。**日數欄唔移**
  （deadlineDays/doneDays/dueDays 係時長唔係日戳）；week 計欄唔移（grace.startedWeek、shopWeek——
  只影響商店補貨提早觸發一次，無玩法後果）。
- 評核唔重觸：reviews 已記錄狀態原樣保留（遷移唔掂 reviews 內容）；遷移後就算行到 wk52 週結，
  評核邏輯見 reviews[1990] 已存在就跳過（單元測試 fixture B 證明）。
- **邊界行為（老實申報）**：舊檔若喺 3 月 epoch 玩到「新邊界啱啱過咗一兩日」嘅位置，遷移後
  conseq61LegacyMark 會按新 epoch 嘅 curYear 靜靜標記評核已過（legacy），唔補判、唔補收 E7——
  同 conseq61 一貫「永不追溯」哲學一致，屬預期行為，唔係 bug。

## 過程中捉到嘅兩個真 bug（已修，有測試釘住）

1. **jan67OpeningTextFix 初版改唔到陣列字串**：walker array 分支將字串元素傳入遞迴、畀
   `typeof !== "object"` 擋返——beats `open[]`／tutorial `body[]` 係字串陣列，永遠改唔到。
   單元測試初版 fixture 形狀錯（body 寫成字串）冇捉到，**真 UI 抽驗捉到**（教學卡實機出「1990 年春」）。
   已修：陣列字串元素就地行 jan67OpeningLineFix；測試 fixture 改返真形狀。
2. **JAN67_DAY_KEYS 漏 lastGiveDay**：map 形日戳（giftMeta.lastGiveDay）永遠唔移。
   遷移 fixture 斷言捉到，已補鍵。

## 驗證

- tests：**68/68 PASS**（66 基線＋新增 test_jan67_logic.js／test_jan67_static.py）；
  9 檔舊測試按新曆法更新預期（只改曆法/週位事實，金額/門檻斷言唔郁）；新測試對 v66 index 反證 FAIL。
  主 script `node --check` 過。
- 真 UI 抽驗（本地鏡像 serve67，index 與工作副本 sha256 一致；?softPreview=1、槽 3、零 pageerror）：
  新 game 開局 HUD 1990年1月1日／冬、副題＋印章＋注腳對位、教學卡「1990 年初」、B01 標題動態日期、
  DOM 禁詞（春季開局句／一九八八／1990年3月7日）清零；植 dayIndex 300 過 wk43 週結 → reviews
  保持空（舊邊界已廢）；植 363 過 wk52 週結 → reviews[1990] 喺 week 52 先寫入＋pendingEnding；
  遷移實載 A（評核前）200→265 日期 1990年9月23日不變、B（評核後）400→465 日期 1991年4月11日不變、
  reviews 原樣、冇補評。證據喺 linji-work67/verify67/（driver67.py＋driver67_log.txt＋截圖）。
  註：存檔處於行程執行中時，載入會 resume 行多一日（D 段觀察 266/466），係引擎既有行為，
  遷移不變量（+65＋日期對位）不受影響。
