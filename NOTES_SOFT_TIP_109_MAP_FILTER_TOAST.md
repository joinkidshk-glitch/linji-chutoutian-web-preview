# NOTES · Soft tip #109 — 地圖篩選 toast 跟切換後嘅模式

> **狀態：** Soft≠PASS｜**唔 tip LIVE**｜SAVE `starVolunteer_map_v19w`｜產品 `?v=20a10` 唔抬  
> **softRev：** `s109`  
> **預覽：** `https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=20a10&softBehaviorGate=1&softRev=s109`  
> `<html data-soft-rev="s109">` 先算載到今次 index。89–92 HOLD。出圖 HOLD。  
> 基線：Soft tip #108 main `62e08955`／softRev=`s108`。toast-on-map 位置留低。

## 玩家面

- 地圖頂右掣「全部地點」⇄「只亮有事」。
- 撳去**顯示全部**之後，toast「已顯示全部地點」。掣改為「只亮有事」（下一句指令，唔係而家模式）。
- 撳去**只亮有事**之後，toast「只亮有事做嘅地點」。掣改返「全部地點」。
- Toast 仍然企喺地圖頂（s108 `.toast-on-map`）。

## 根因

- `wireMapShowAllLocs` 本來係先 `mapShowAllLocs = !mapShowAllLocs`，再 `drawMap()`，再按個 flag toast。極性同「切換之後」一致：true →「已顯示全部地點」。
- 掣文案係**下一句指令**（開晒全部之後寫「只亮有事」），所以同 toast 字面相反，唔係模式講反。
- 如果 `drawMap()` 喺更新掣之後拋錯，舊寫法唔會再 toast，上一句會留喺畫面，睇落就係講緊相反模式。

## 本票做咗咩

- 翻旗之後先 snapshot `showAllNow`，再畫地圖。Toast 用 snapshot，唔再用可能被重繪改過嘅 flag。
- `drawMap()` 包喺 try 入面。重繪失敗都 toast 切換之後嗰句。
- softRev `s108` → `s109`。SAVE、產品 `?v=20a10`、toast-on-map 唔郁。

## 本票唔做

- 唔 tip LIVE；唔抬 SAVE；唔抬產品 `?v=`。
- 唔出圖；89–92 HOLD。
- 唔改掣文案、唔改針淡化規則。

## Console

- `__newspaper.check()`（框架同主線載入後）應 `{ ok:true, softRev:"s109", version:"v20a10", softStatus:"≠PASS" }`
- `runSoftP0Checks()` 應 `ok:true`（`data-soft-rev` 同 URL `softRev=s109`）

## QA

新分頁開上面條 URL。入地圖，撳「全部地點」：頂 toast「已顯示全部地點」，掣變「只亮有事」。再撳：頂 toast「只亮有事做嘅地點」，掣變返「全部地點」。
