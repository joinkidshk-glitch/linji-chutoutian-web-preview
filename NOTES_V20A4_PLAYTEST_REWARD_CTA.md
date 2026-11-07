# NOTES · Freeplay v20a4 PLAYTEST FIX — reward sheet + loc CTA

> **時間：** 2026-11-07（Asia/Hong_Kong）  
> **狀態：** Soft≠PASS；**唔 tip LIVE**；SAVE key 不變  
> **預覽：** `?v=20a4&softBehaviorGate=1`  
> **契約：** `docs/CONTENT_CONTRACT.md`

## 玩測 blocker（修）

1. **殺青後「傳媒・街外・成績」sheet 未出**
   - 根因：`dayEndContinueButtons` 嘅「返回地圖」直行 `goToMapForBrowse`，繞過 `goRunSchedule`／`afterDayRes` 獎勵鏈（依賴後加 wrap，易漏）。
   - 修：地圖／軟行程「返回地圖」改走 `goRunSchedule`；`goToMapForBrowse` 加 pending 安全網（仍有 `_pendingPostShootReward` 先出 sheet）。
   - `__reward.check()`／`__freeplay.rewardCheck()` 仍可用；cache bust → **v20a4**。

2. **地點 CTA 中途死掣**（只查看通告欄／接通告／傾談 → `#mask` 唔再開）
   - 根因：`doScout` 掛 `#loc-sheet.board-modal-open`（CSS `pointer-events:none` 喺 `#loc-acts`）；獲聘／關 modal／關 sheet 路徑未必清走 → 之後再開地點 CTA 全死。
   - 修：`closeSheet`／`closeModal`／`openLoc`／`ensureLocSheetInteractive`（無真實 mask／force）／通告 teaser→Detail 一律清 `board-modal-open`。

## Verify

```js
await __freeplay.load();
__freeplay.check();   // ok:true；version v20a4
__reward.check();     // ok:true
```

手測：
1. Soft 新局 → 接通告 → 殺青日結 → 收起後應出「傳媒・街外・成績」→ 收下 → 地圖。
2. 再開任意地點：通告欄／接通告／傾談應再出 `#mask.on`。

## HOLD

- 蘇芷茵 pin、記數 tab、C2 pacing、stub 內 `v20a1` 字串偏離（非本輪）
- tip LIVE／抬 SAVE
