# v19z11 — smoke-test fix（v19z10 驗收失敗項）

Branch `fix/playtest-smoke-fix-v19z11`. Hardens four smoke failures from official `?v=19z10`.

## Root causes & fixes

| # | Smoke FAIL | Root cause | Fix |
|---|------------|------------|-----|
| 1 | 老張「去還」toast「而家無欠何生」 | 舊路徑／漏綁會落到 `openHoRepaySheet`→`canRepayHoDebt`；按鈕 onclick 重渲易丟 | `#debt-list` **事件委派**；debtId 由該卡 `data-repay-id`／`data-debt-id`／`data-collect-id` 讀取；**永唔**走 `openHoRepaySheet`；空 id 明示「搵唔到呢筆」 |
| 2 | `.home-money`／地圖 HUD 滯後 | `refreshMoneyHud` 只刷單一節點；地圖存款易被 dual-hud 擠走 | 刷 **全部** `.home-money`＋`#c-money`；`#c-money-wrap` 強制可見；CSS `flex:0 0 auto`；`apply`／小賣／茶／還債後照刷 |
| 3 | 選單「返屋企」一撳即過日 | 單一 `data-m=home` 語意混「返手帳／休息」；條件分叉易睇成偷耗日 | 選單拆 **「返手帳」**（不耗日）＋ **「提早休息／+1日」**（二次確認）；舊 `goHomeFromMenu` 改只返手帳 |
| 4 | 通告欄「關閉」掏空地點 | `modal()`→`closeSheet()` 清 HTML；`openLoc` 遇強制日會拒還原 | `keepSheetContent` 只收起唔掏空；關閉／返地點選單／dismiss 一律 `openLoc(..., {forceRestore:true})` |

何生現金還債原子扣款（v19z10）保留；還債後 HUD 一定 refresh。

## Cache

`?v=19z10` → `?v=19z11`

Prefs key 仍 `starVolunteer_prefs_v19z9`（相容舊設定）。

## Soft≠PASS

- 唔改 `featureFlag_softBehaviorGatePreview`／gatePath
- soft 預覽空手還仍只展示、唔清債

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z11&softBehaviorGate=1`

1. 人情債「道具組老張」→「去還」開「還人情 · 道具組老張」，**唔**出「無欠何生」；何生卡同樣獨立可開
2. 現金還債／小賣後：地圖頂「存款」＋手帳 `.home-money` 即時同步
3. 選單見「返手帳」同「提早休息／+1日」；前者唔過日，後者要確認先 +1日
4. 通告欄撳「關閉」同「返地點選單」都還原地點行動列（唔留「點地圖針」占位）

Auth: t24u
