# NOTES · Freeplay v20a9 — 休息睡覺 8-bit FX

> **時間：** 2026-11-07（Asia/Hong_Kong）  
> **狀態：** Soft≠PASS；**唔 tip LIVE**；SAVE `starVolunteer_map_v19w`（唔抬 key）  
> **預覽：** `?v=20a9&softBehaviorGate=1`  
> **來源：** 用戶選定 ultra-chunky 8-bit 睡覺短片（~3s）

## 本輪做咗咩
- 資產：`assets/fx/awei-rest-sleep.mp4`（約 3s retro pixel／8-bit）
- Overlay `#rest-sleep-fx`（z-index 800，高過 `#mask`）— 完片／撳略過／撳畫面即關
- 觸發（播一次再出日結；唔改數值）：
  1. 手帳行程 **「休息睡覺」**（`resolvePlannedDay` · `id==="rest"`）
  2. 地點 **休息室歇陣**（`doRest`）
  3. 選單 **提早休息／+1日**（`endBrowseDayGoHome`）
- **週加速靜默合併**休息日唔播（避免打斷加速）
- Console：`__restFx.check()`／`__restFx.play(fn)`；`__freeplay.check()` 含 `restSleepFx`

## Soft≠PASS
- 純視覺 FX；唔改 BehaviorGate／生活費／通告閘
- 唔 tip LIVE；SAVE 不變

## Retest
1. Soft 新局 → 開手帳排一日「休息睡覺」→ 確定出發 → 應先見 8-bit 睡覺片 → 完／略過後出日結 → 返地圖 CTA 正常
2. 去電視台「休息室」→ 確認耗日 → 同樣先播片再日結
3. 選單「提早休息／+1日」→ 確認 → 先播片
4. `?v=20a9&softBehaviorGate=1` 硬重整；`__restFx.check()` → `ok:true`；`__freeplay.check()` 唔 fail `restFx:*`／`ver`
