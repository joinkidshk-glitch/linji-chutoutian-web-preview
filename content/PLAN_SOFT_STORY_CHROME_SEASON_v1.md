# PLAN_SOFT_STORY_CHROME_SEASON_v1.md

**Soft≠PASS｜唔 tip LIVE｜89–92 HOLD｜出圖 HOLD｜經 qwen3.7-max**

## 問題說明
目前鄧麗萍 meet 及任何 Soft 覆蓋季節嘅節拍，於 chrome 顯示時均硬碼為「主線 · 1988春」。
根因在於 `index.html` 中 `spPlayerMeta` 邏輯強制讀取開局預設，未有讀取 Soft season 或 `beat.when` 之季節資訊，導致 Mock 設定之「初秋午後」無法正確反映於玩家介面。

## Soft 規則建議
為確保 iOS Soft 與 web Soft 顯示一致，且唔改 LIVE 預設直至 tip，建議 `playerMeta` 優先序如下：
1. `node.playerMeta`（節點明確指定）
2. Soft season 派生（autumn→「主線 · 1988秋」／winter→「主線 · 1988冬」／spring→春／summer→夏）
3. `when`／`eraTag` 解析
4. 最後 fallback「主線 · 1988春」（僅限 C1 開局或無季節資訊時）

**鄧麗萍 R_tang_meet 適用：**
Mock／seed 季節設定為 autumn，chrome 應顯示「主線 · 1988秋」（或「支線 · 1988秋」，詳見 Soft A/B）。

## Soft A/B 選項（交統籌拍板）
- **A1 chrome 線別標籤**
  - 選項 A：鄧麗萍 meet 使用「主線 · 1988{季}」
  - 選項 B：使用「支線 · 1988{季}」（可選線視覺）
  - *建議：先寫「建議 A」，並註明等拍板。*
- **A2 Soft 季節來源**
  - 選項 A：`seed.season`／`softSeasonOverride` 優先
  - 選項 B：只跟 `dayIndex` `calendarSeason`（seed 必須揀秋冬 dayIndex）
  - *建議：選項 A。*

## 可直接 Soft 修 vs 等拍板
- **可直接 Soft 修**：於 Mock 及 seed 加設 `chromeSeason`／`playerMetaProposed` 欄位，並實作上述優先序邏輯。
- **等拍板**：A1（主線 vs 支線標籤）、A2（季節來源優先序）。

## iOS Soft hooks
- 新增 `spPlayerMeta_softSeason`。
- 讀取 Mock `playerMeta`／`chromeSeason` 以覆蓋預設。

## Acceptance 檢查表
1. chrome 季節顯示正確（autumn 對應 1988秋）。
2. 線別標籤 A1 拍板後正確套用。
3. 季節來源 A2 優先序邏輯無誤。
4. Mock 1.1 載入無報錯。
5. 玩家面無洩漏工程詞／Ho 哥／真藝名。
6. 89–92 HOLD 狀態維持。
7. 確認唔 tip LIVE。

## Acceptance／Out of scope
- 唔改 LIVE week-gate 預設。
- 唔 tip LIVE。
- 89–92 HOLD。
- 唔改對白及 choices。

---
*本檔 body SHA8 `d24caf74`｜經 qwen3.7-max｜Soft≠PASS｜唔 tip LIVE。*

---

## Soft A/B 拍板（2026-11-04 · 統籌）

- **A1＝A**：chrome 線別用「主線 · 1988{季}」（唔用支線）
- **A2＝A**：季節來源 `seed.season`／`softSeasonOverride`（softCalendarSeason）優先，其後 when／eraTag，最後 fallback「主線 · 1988春」
- Mock 1.1：`playerMetaProposed` 已升格 **`playerMeta=主線 · 1988秋`**（JSON SHA8 見交收）
- iOS Soft：`spPlayerMeta_softSeason` 由統籌交修；**唔 tip LIVE**
- Soft≠PASS｜89–92 HOLD｜鄧 push+ HOLD｜出圖 HOLD

