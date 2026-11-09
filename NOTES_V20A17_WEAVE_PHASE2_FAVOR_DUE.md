# v20a17 — Weave Phase 2-2：人情到期觸發（幫忙通告型）

Soft 預覽改動。唔改 SAVE key（`starVolunteer_map_v19w`）、唔改 softRev（s107）、唔改 `?v=`（v20a10）。

## 研究結論：現有人情系統

- **來源**：①教學債 `debt_ho_tutorial`（債主何生，拼合教學完成 `markRumorTutorialDone` 時記入 `S.mockDebts`；手帳人情頁空嗰陣亦會補種）②`SEASON_COLLECT` 季節催收卡（靜態、按季喺人情頁顯示，唔入 mockDebts，另有 `S.mockSeasonCleared` 記錄已清）③FREEPLAY_FW favorDebt stub 按季種入 mockDebts ④GIGS 有 `favorDelta` 數據欄，但未見直接轉成 mockDebts 債嘅邏輯。
- **儲存**：`S.mockDebts` 陣列，欄位 `{id, creditor, title, weight, season（文案行）, status, amount?}`；`S.notebook.debts` 為鏡像（`syncNotebookMirror`）。
- **狀態**：只有三個靜態字串「未到期／就嚟到期／已逾期」，**無 dueDay／日期欄位、無隨日推進嘅轉換邏輯**；逾期唯一後果係 soft gate 開嗰陣 `softOverdueFavorDebtLock` 鎖接通告。
- **顯示／還款**：手帳人情頁 `renderDebtPane`（狀態徽章＋`DEBT_FUZZY` 模糊提示＋「去還」掣）；`openDebtRepaySheet` 行現金／禮物還款，`allDebtsForRepay` 列出全部未清債。
- **關係機制**：`S.npcs[id]`（0–100）＋`bumpNpc(id, delta)`；何生 npc id 為 `agent`，`bumpNpc("agent", d)` 會同步 `S.story.favor.agency_ho`。已有 `bumpNpc("agent", -1)` 扣減先例。

## 揀邊筆債同點解

揀 **教學債 `debt_ho_tutorial`（何生）**：現有數據最齊——債主明確而且有完整好感系統、係玩家第一筆債、有手帳顯示同現成還款路徑、記債時機明確（教學拼合完成）。其餘債源（季節卡係靜態展示、FW stub 文案未齊）都唔適合做第一款到期觸發。

## 實作（全部新欄位可選、舊存檔兼容）

1. **到期日**：`FAVOR_DUE_CFG = { debtId:"debt_ho_tutorial", gigId:"gig_favor_ho_errand", dueDays:7, windowDays:4 }`。`ensureFavorDue()` 畀呢筆債補 `kind:"help_gig"`、`favorState:"pending"`、`dueDay`（首次見到嗰日 +7；舊存檔回填同理，唔會一讀檔即到期）。手帳人情頁渲染時亦會補印，保證提示即時可見。
2. **玩家可見提示**：人情頁該債多一行到期提示（`favorDueHintText`）：未到期顯示「約 X 日後到期：到期何生會開張幫忙通告畀你，幫手做完即算還清，唔使另外畀錢。」；臨近到期（≤2 日）狀態自動轉「就嚟到期」。
3. **到期觸發**：`favorDueTick()` 掛喺 `advanceDay()` 尾。到期嗰日 `favorState→"called"`、記 `favorGigDay`，toast 何生 Call 機留言通知；`mergeFavorGigs()` 跟 Phase 2-1 同一條件注入模式（喺 `gigsForLocSeasonBoard` 開頭、緊貼 `mergeIntelGigs` 呼叫），將幫忙通告 `gig_favor_ho_errand`《晨光劇場》臨時人手（事務所板、$500 定額、1 日）注入 `GIGS`，窗口（4 日）外／未觸發／已結算即移除。
4. **結清**：tick 檢查 `S.wrapHistory`／`done_` 旗——幫忙通告殺青後翌日 tick 結清：債由 `mockDebts` 移除、`S.favorDueSettled[id]={result:"repaid_help"}`、`bumpNpc("agent", +2)`、toast 講明還清。
5. **作廢**：窗口過咗未殺青：債移除、`settled={result:"void_expired"}`、`bumpNpc("agent", -3)`、toast 講明「人情作廢、交情淡咗」。
6. **防重行／防誤傷**：到期前用現金／禮物還咗（債消失）→ tick 靜靜記 `closed_other`，唔觸發唔扣好感；結算後教學債被手帳補種返嚟都唔會重行到期流程（settled 守衛）。呢筆債**永不設「已逾期」狀態**，避免 soft 逾期鎖誤鎖幫忙通告本身。到期 tick 只行 `advanceDay`，即觸發／結清／作廢都喺過日嗰刻結算。

## 未做（留待後續）

- 其餘債款（還錢型／記仇型）同其他債主嘅到期行為未做，今次只一款幫忙通告型。
- 規劃 3.2「到期前一週債主喺日常地點出現多句對白」未做（今次用狀態轉「就嚟到期」＋手帳提示＋到期 toast 代替預告層）。

## 測試

- 新增 `tests/test_weave22_logic.js` 41/41、`tests/test_weave22_static.py` 18/18。
- 回歸全過：P0 邏輯 17／靜態 27、P0-3 邏輯 7／靜態 12、Weave 1-1 邏輯 12／靜態 14、Weave 1-2 邏輯 16／靜態 7、Weave 1-3 邏輯 14／靜態 6、Weave 2-1 邏輯 26／靜態 15。
- 全檔 script `node --check` 通過。
