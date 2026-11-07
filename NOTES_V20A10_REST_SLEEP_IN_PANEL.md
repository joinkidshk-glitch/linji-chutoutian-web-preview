# NOTES · Freeplay v20a10 — 休息睡覺片嵌日結板

> **時間：** 2026-11-07（Asia/Hong_Kong）  
> **狀態：** Soft≠PASS；**唔 tip LIVE**；SAVE `starVolunteer_map_v19w`（唔抬 key）  
> **預覽：** `?v=20a10&softBehaviorGate=1`  
> **來源：** 用戶回饋 v20a9 全螢幕 overlay 唔啱；期望喺「休息（週x）」米色日結板內播，文案只顯示數值變化

## 本輪做咗咩
- **唔再**用全螢幕 `#rest-sleep-fx` overlay（已移除）
- 休息日結板（`presentRestSleepDayEnd`）內嵌 `assets/fx/awei-rest-sleep.mp4`
- 文案精簡：標題 `休息（週x）` + 數值（例如 `體能 +23`／`壓力 -18`）+ CTA；唔再出「大回復體能·減壓」／長說明／完成日行
- 觸發不變：手帳「休息睡覺」、地點休息室、選單提早休息；週加速靜默合併仍唔播
- Console：`__restFx.check()`／`present`／`arm`；`__freeplay.check()` → `infra:v20a10`

## Soft≠PASS
- 純 UX／FX 呈現；唔改 BehaviorGate／生活費／通告閘
- 唔 tip LIVE；SAVE 不變

## Retest
1. Soft 新局 → 手帳排「休息睡覺」→ 確定出發 → **直接**出米色「休息（週x）」板，板內播 8-bit 片＋數值 → 返回地圖
2. 確認**冇**先出全黑全螢幕片再出日結
3. 電視台休息室／提早休息：同樣嵌板播片
4. `?v=20a10&softBehaviorGate=1`；`__restFx.check()` → `ok:true` mode:`in-panel`
