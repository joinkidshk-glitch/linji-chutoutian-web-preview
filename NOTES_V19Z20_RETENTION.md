# v19z20 — 留存／沉浸式 P1（早期經濟 · 事態進度 · 加速返看）

Branch `fix/playtest-retention-v19z20`. Follows merged `v19z19` (`4d3ca75`).

目標：明星育成留存——減早期生存焦慮、常駐下一幕 cliffhanger、加速後唔斷離。

## Changes

| # | Item | What |
|---|------|------|
| 1 | 早期生活費（W1–4） | `livingCostRoll`：頭 4 週 **$1,400–1,800**（中位預估 $1,600）；第 5 週起維持 **$2,000–2,800**。壓力預覽／週五六日結提示跟 `livingCostEstimate`／`livingCostRangeLabel`。 |
| 2 | 事態進度常駐 | 地圖底 `#map-hint`：`storyMainProgressLine` 顯示例如「通告 1／3 · 第2幕即將 · 留人脈／趕通告」；有開放事態時併入「有事態 · …」。Soft stub 經 `BehaviorGate.progressToward` 讀 `gigCountMin`／`weekMin`（唔洩漏 pacing `nextHint` 長文）。 |
| 3 | 加速本週返看 | `weekBestReplayLine`：加速摘要／加速完成卡加一句「本週最值得返看：…」（事態／通告／傳聞／傾談／訓練優先）。`noteWeekHighlight` 掛 `doTalk`／殺青／`markDone`／打聽。週結後重置。 |
| 4 | 地點 sheet 死鍵加固（顺手） | 玩測回報「香江唱片」全 sheet 唔可點——同 v19z19 `mask-up`／`inert` 類。加 `#loc-sheet.sheet-live`：JS 開 sheet／關 modal 時掛／清；CSS **唔靠 `:has(#mask.on)`** 強制 `pointer-events:auto`。`closeModal` 後再跑 `ensureLocSheetInteractive`。若仍死鍵，先硬重整 `?v=19z19`／`?v=19z20` 排除舊 cache。 |

**經濟數字（NOTES）**

| 週 | 生活費實際 | 預估中位 | 對照入門臨記 |
|----|------------|----------|--------------|
| 1–4 | $1,400–1,800 | $1,600 | 入門 `payExact` 約 $800–1,100／日；每週 2 張 entry 板面保底仍由 `ensureEntryTierBoardFill`（不變） |
| 5+ | $2,000–2,800 | $2,400 | 同舊 |

開局存款仍 $12,000。

## Out of scope（本 PR 唔做）

- P2：非主線針再淡、雙「下一句」、手帳標籤同步、頂欄角色名 truncation
- 唔改 soft BehaviorGate 預設／`gatePath`／stub 觸發條件；唔 tip LIVE

## Soft≠PASS

- `progressToward` 只讀 stub trigger 畀 UI；唔改 `evalTrigger`／week-gate
- 生活費／加速文案唔開第二個 soft flag

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z20&softBehaviorGate=1`（硬重整）

1. 新局 W1–4：週末結算生活費落在 $1,400–1,800；壓力預覽寫「頭4週優惠」
2. 地圖底欄：C1 後未達 C2 時見「通告 x／3 · 第2幕即將…」（即使無金框開放事態）
3. 加速本週剩餘 → 摘要卡有「本週最值得返看：…」
4. 開香江唱片等地點 sheet：通告／休息室／返回可點；若仍死 → 先確認 URL 已係 `v=19z20`（或至少 `v=19z19`）並硬重整

若用戶仍見全 sheet 死鍵而 URL 仍係舊 `v`：提醒先驗 **`?v=19z19&softBehaviorGate=1`**（v19z19 已合埋）再升 `v=19z20`。
