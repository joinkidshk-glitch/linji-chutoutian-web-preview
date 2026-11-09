# NOTES V20A45 — 「開始今日行程」確認閘（用戶拍板 A 方案）

性質：soft 預覽流程修訂。唔改 SAVE key（starVolunteer_map_v19w）、softRev（s107）、產品 ?v=（v20a10）；唔改 content pack；唔改任何日結算數值公式（提早休息 6+R(0,4)、計劃休息 20+R(0,8) 原封不動）。根因見 `linji-double-day-diagnosis.md`：唔係 bug，係日結休息卡「開始今日行程」同翌日自動行程之間零停頓，玩家觀感似「撳一次瞓咗兩日」；A 方案＝喺嗰個入口加確認。

## 入口區分方法（今次嘅關鍵決定）

兩條路徑最終都去 `runScheduleFromToday`，分別唔喺被呼叫函數，而喺**呼叫者身份**：

- **要加確認（結算卡延續）**：日結休息卡 `presentRestSleepDayEnd` 上嘅「開始今日行程」掣。呢張卡有三個真日結呼叫者，全部傳新旗標 `confirmStartSchedule: true`：
  1. `endBrowseDayGoHome`（提早休息卡——即診斷個案嗰張）
  2. `resolvePlannedDay` 休息分支（計劃休息卡，onSchedule＝nextNbReward 延續鏈，一樣會即時結算自動日）
  3. `doRest`（地點休息卡，同卡同預設路徑）
- **唔加確認（主動開始）**：地圖／選單／朝早主動撳嘅開始行程路徑——`startTodayScheduleFromMap`、頂欄／手帳 CTA、各 `runScheduleFromToday` 直接呼叫者，全部冇經 `presentRestSleepDayEnd`，一行冇改。
- **同卡內唔落閘嘅掣**：「返回地圖」（本來就安全）、「回家結算」（ended 週結，掣本身就係結算動作）、「加速本週剩餘」（已有自己嘅 `confirmWeekAccel` 二次確認，唔疊多層）。
- **排除在外（已申報）**：`playRestSleepFx`（legacy／console 開卡路徑，傳自訂 cont）冇傳旗標，行為不變；通用日結卡 `afterDayModal` 係另一個 presenter（工作日結算用），不在今次範圍，日後要統一可另開一票。

實作手法：**加旗標參數＋卡內包一層**（冇改 `runScheduleFromToday` 本體、冇喺佢入面加全域閘——嗰度分唔到呼叫者，一定誤傷主動路徑）。

## 改動清單（vs v20a44，逐行 diff 只有以下，60 行）

1. **新函數 `presentStartScheduleConfirm45(onStart, onMap)`**（置於 `presentRestSleepDayEnd` 之前）：用返現有 `modal()` 模式（同 `confirmEarlyRestFromMenu` 一套）。文案按今日計劃動態生成：
   - 標題「開始今日行程？」＋「將會開始 {fmtDate()} 嘅行程。」
   - 休息：「今日排咗「休息」，一開始就會即時結算埋今日（即係連續過日）。」
   - 自動行程（soft 非地圖日）：「今日排咗「{planLabel}」（自動行程），會即時結算埋今日（即係連續過日）。」
   - 已排定（shoot:/job:）：「今日有已排定嘅行程，開始後會直接進行。」（唔講即時結算，因為嗰類日係去進行拍攝，唔係自動結算）
   - 掣：「開始今日行程」（p）／「返回地圖」（g）；modal 背景關閉（onDismiss）＝返回地圖，同卡本身 dismiss 語義一致。
   - 本函數只出 modal 同轉交回呼，**唔掂 dayIndex／存檔狀態**（static 測試有斷言函數體內冇 dayIndex）。
2. **`presentRestSleepDayEnd` 內部重構（行為等價）＋加閘**：原 `goSchedule`／`goMap` 嘅 finish 回呼拆出 `proceedSchedule`／`proceedMap`；新增 `goScheduleAsk`——冇旗標就直行 `goSchedule`（舊行為）；有旗標就先行 `finish()` 做既定清理（停睡覺 FX、除 day-res class），再開確認 modal，確認嘅兩個去向直接行 `proceedSchedule`／`proceedMap`（唔再經 finish 守衛，唔會被 advanced 旗擋住）。確認 modal 開唔到（例外）會 fallback 去 `proceedMap`——停喺結算後地圖狀態，永遠唔會卡死或者誤推日。
3. **掣面改綁**：卡內 label 改綁一段拆開——「回家結算」→ `goSchedule`（不變）、「開始今日」→ `goScheduleAsk`（新）、「返回地圖」→ `goMap`（不變）、「加速」→ 原有包裝（不變）。
4. **三個呼叫點各加一行旗標**：`endBrowseDayGoHome`、`resolvePlannedDay` 休息分支、`doRest` 嘅 `presentRestSleepDayEnd({...})` 各加 `confirmStartSchedule: true`。

確認之後嘅原本流程（`presentDueMorningPaper` 派朝早報紙 → `resolvePlannedDay` 結算）原封不動；取消（返回地圖／關閉）只行 `proceedMap`，係結算卡本來就有嘅安全去向，零副作用。

## 驗證結果（工作副本 ~/workspace/linji-work45）

- `node --check`：全檔 2 段 script 全部 OK。
- **新增測試（跟 v20a37 反證慣例，兩套行落 v20a44 舊檔都 exit 1 FAIL）**：
  - `tests/test_flow45_logic.js`（17 斷言）：抽真 `presentRestSleepDayEnd`＋真 `dayEndContinueButtons`＋真 `presentStartScheduleConfirm45` 行真路徑——A 旗標開＋休息日：撳開始先出確認、行程未行、dayIndex 冇郁、文案有日期＋即時結算警告、確認開始後行程只行一次；B／B2 返回地圖／關閉：只去地圖、行程零執行、冇推日；C 冇旗標：即刻行程、冇確認（legacy 行為不變）；D 計劃休息卡（onSchedule 延續）：確認後行 onSchedule；E ended＋旗標：「回家結算」直行、冇確認；F／G 文案：自動行程講明計劃名＋即時結算、已排定行程講「直接進行」而冇即時結算警告。**17/17 PASS**。
  - `tests/test_flow45_static.py`（24 斷言）：確認函數接線、閘只綁「開始今日」掣、「回家結算」冇閘、旗標呼叫點恰好 3 處且逐一對位三個函數、legacy／afterDayModal／地圖主動路徑冇旗標、紅線、兩條結算公式同 `S.dayIndex += 1` 原樣。**24/24 PASS**。
- repo 測試全套：**32/32 檔案 PASS**（原 30 ＋ 新 2；16+2 node 邏輯、14+1 python 靜態…實數：node 17 檔＋python 15 檔）。
- 紅線 grep：`starVolunteer_map_v19w` 10 處、`softRev=s107` 在位、`"v20a10"` 7 處，同 v20a44 一致。
- 逐行 diff（vs v20a44）：只有上述 4 組改動，共 60 行 diff，冇計劃外改動。
- 檔大小：4,196,333 → **4,199,207 bytes**（+2,874；推送通道上限實測介乎 4.20MB（過）同 5.23MB（413）之間，今次 4.199MB 同 v20a44 同級、屬已驗證可推範圍；下一票若要加素材要先留意體積）。

留待主代理：推分支＋PR＋部署核實＋實機驗（重點：新檔第一週撳「逛完・過一日」→休息卡撳「開始今日行程」→應先出確認、文案講明 3/8 休息會即時結算；撳返回地圖應停喺 3/8 地圖冇推日；再喺地圖主動開始行程應冇確認直接行）。
