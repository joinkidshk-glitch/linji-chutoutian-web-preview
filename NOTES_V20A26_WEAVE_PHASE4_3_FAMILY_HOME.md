# v20a26 — Weave Phase 4-3：鏈 G 阿偉屋企線第 1＋3 拍（屋企恆常債＋家人態度）

## 做咗乜

### 1. 屋企恆常債 `debt_family_home`（第 1 拍）
- 新常量 `FAMILY_HOME_CYCLES`（4 期輪替）＋ `ensureFamilyHomeDebt()`：
  - **播種**：經 `ensureMockJournal()`（新檔開局第一筆債就係屋企債；舊檔首次載入補種）＋ `advanceDay()` 雙入口，固定 id 冪等，只會有一筆。
  - **債主**：「屋企／阿媽」；status 恆「未到期」；無 dueDay（唔入 favorDue 到期流程）。
  - **金額輪替**（顯示額，沿用現行還款機制＝現金 $200／禮物，唔另開 UI）：
    1. 今個月家用 $600 → 2. 今期幫補交租 $800 → 3. 阿媽覆診藥費 $450 → 4. 屋企換雪櫃嗰份 $700 → 循環。
    量級對照：週生活費 $1,600–2,400，屋企嗰份係「幾百蚊級細額」，係恆常提醒唔係經濟壓力來源。
  - **補種節奏**：狀態存 `S.familyHome = { cycle, monthKey, seedDay, paidDay, … }`。月份以真日曆 `dateObj()` 計：
    有債在帳 → 唔補（跨幾多個月都係嗰一筆）；還清 → 當月唔補，下個月第一日（advanceDay 跨月嗰刻）自動補下一期。
    還清嗰陣 `applyMockAsk` 改行 `noteFamilyHomePaid()` 記低還清日＋當月份，唔經帳本（見下）。
- **永不懲罰（明確排除，唔靠 status 巧合，跟 4-2 絕響排除 pattern）**：
  - `favorPressure()`：filter 明文排除 `debt_family_home`；
  - `softOverdueFavorDebtLock()`：filter 明文排除（屋企唔會鎖你接通告）；
  - `S.favorLedger`：`applyMockAsk` 結清分支畀屋企債行專屬分支，**唔呼叫** `favorLedgerNoteSettled`（唔入 settled、唔入 counted）；
    `favorLedgerCounts().openDebts` 亦明文排除，免結局判定（E4／E5）計錯屋企嗰筆做圈內債。

### 2. 週結算屋企 flavor（節奏決定）
- `settleWeek()` 經 `familyHomeSettleLines()` 消費一次性標記後 `pushFlavor`：
  - **播種嗰週**：「屋企嗰邊：月頭到，阿媽冇打電話嚟催，只係將新一期嗰筆記入手帳——屋企人催數，從來唔出聲。」
  - **還清嗰週**：「屋企嗰邊：今個月嗰筆交咗。阿媽冇多講，只係嗰晚煲多咗個湯——屋企人嘅放心，從來唔係用口講嘅。」
  - 其他週唔出；每期／每次還清只出一次（seedFlavorDay／paidFlavorDay 消費標記）。
  - 窗口用 ≤7 日：settleWeek 喺星期一先行（dayIndex 已跳新週），事件日同結算日最多差 7 日。

### 3. 家人態度字條（第 3 拍）
- `familyAttitudeLine()` 借報紙點名三級 `newspaperNameTier()`（anon fame<15／named 15–39／titled ≥40），唔另計數；
  `renderDebtPane()` 喺屋企債卡內（`debt-note` 備註行之後、還款掣之前）加一行 `family-attitude`，唔另開頁面：
  - anon：「屋企字條：阿媽話——做臨記唔係辦法，隔離陳師奶個仔做文員，月月有糧出幾穩陣。你自己諗下啦，仲有，記得食飯。」
  - named：「屋企字條：阿媽話，聽講報紙有寫你個名？真定假㗎……唔好俾人呃先好，糧期到就追實啲，屋企等住你嗰份開飯。」
  - titled：「屋企字條：阿媽話，鄰居問起你做邊行，佢而家會答：「我個仔上報紙，做戲嗰個。」講嗰陣，腰骨都直啲。」

## 取捨／未做
- 還款金額沿用全域 mockDebts 機制（現金 $200／禮物一件），債卡「金額約 $X」係嗰期賬單面額——同季節卡等現有債一致，唔為屋企債另起按額收費，免改動還款核心。
- 鏈 G 第 2 拍（報紙首次點名觸發屋企事件：剪報／茶餐廳留言）同第 4 拍（1990 行留抉擇）唔喺今票，留返同結局系統一齊做。
- 茶餐廳唔係屋企駐場：字條只跟屋企債卡走，無新增地點／NPC。

## 測試
- 新增 `tests/test_weave43_logic.js`（40 項，全過）：真 ensureMockJournal 播種（新檔第一筆／舊檔補種／只一筆）、
  真 applyMockAsk 還款＋真 advanceDay 跨月補種（還清當月唔補、跨月輪替 $600→$800、未還唔補、冪等）、
  排除逐項斷言（favorPressure／逾期鎖連強制逾期狀態都排除、對照組照常計；帳本 settled 唔郁、openDebts 排除）、
  真 renderDebtPane × fame 5／20／50 三段字條（斷言喺屋企債卡內）、真 settleWeek flavor 節奏（播種週／還清週出、次週唔重複、靜週唔出）。
- 新增 `tests/test_weave43_static.py`（26 項，全過）：接線點、排除點、三段原文、慣例（SAVE key／softRev 不變）。
- 既有全套 30 個測試檔（連新檔共 32）全部通過；全檔 script `node --check` OK。

## 慣例
- soft 預覽 only；SAVE key（starVolunteer_map_v19w）、softRev（s107）、?v=（v20a10）不變。
