# NOTES · Soft tip #110 — 地圖篩選 toast 跟一次切換之後嘅模式

> **狀態：** Soft≠PASS｜**唔 tip LIVE**｜SAVE `starVolunteer_map_v19w`｜產品 `?v=20a10` 唔抬  
> **softRev：** `s110`  
> **預覽：** `https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=20a10&softBehaviorGate=1&softRev=s110`  
> `<html data-soft-rev="s110">` 先算載到今次 index。89–92 HOLD。出圖 HOLD。  
> 基線：Soft tip #109 main `1920f714`／softRev=`s109`。toast-on-map 位置留低。

## 玩家面

- 地圖頂右掣「全部地點」⇄「只亮有事」。掣文案係**下一句指令**，可以同 toast 字面相反。
- 撳一次去**顯示全部**之後，toast「已顯示全部地點」。掣改為「只亮有事」。
- 撳一次去**只亮有事**之後，toast「只亮有事做嘅地點」。掣改返「全部地點」。
- Toast 仍然企喺地圖頂（s108 `.toast-on-map`）。

## 根因

s109 嘅三元運算同 `mapShowAllLocs` 極性本身係對嘅：翻旗之後 `true` 先 toast「已顯示全部地點」。`true` 會加 `.show-all-locs`（閒置針亮返）；`false` 先係只亮有事。掣喺 `true` 時寫「只亮有事」，係下一句指令。

自然 Soft QA 見到嘅係相反句，而且截圖入面掣文案**冇變**（撳之前係「只亮有事」，畫面仍然係「只亮有事」，toast 卻係「已顯示全部地點」）。呢個配對係**起點嗰個模式**，唔係單次翻旗之後。同一下手入面第二個 click（`detail > 1`，或者幾十毫秒內再入 handler）把旗翻返轉頭，toast 就講返玩家啱啱離開嗰句。好多存檔幾乎每個地點都算有事，地圖畫面唔會因為雙重翻旗而變，所以睇落就係 toast 講反。

## 本票做咗咩

- 500ms 內第二下，同 `detail > 1`，直接 return，唔再翻旗。
- 一句 `mapFilterToastText(showAllNow)` 只用翻旗**之後**嘅 flag。`true` →「已顯示全部地點」；`false` →「只亮有事做嘅地點」。
- `applyMapShowAllLocs` 喺 `drawMap()` 前後都寫低 class／掣文案。重繪中途拋錯都唔會留低舊掣、配上新句。
- softRev `s109` → `s110`。SAVE、產品 `?v=20a10`、toast-on-map 唔郁。

## 本票唔做

- 唔 tip LIVE；唔抬 SAVE；唔抬產品 `?v=`。
- 唔出圖；89–92 HOLD。
- 唔改掣文案、唔改針淡化規則。

## Console

- `__newspaper.check()`（框架同主線載入後）應 `{ ok:true, softRev:"s110", version:"v20a10", softStatus:"≠PASS" }`
- `runSoftP0Checks()` 應 `ok:true`（`data-soft-rev` 同 URL `softRev=s110`）

## QA

新分頁開上面條 URL。入地圖，撳一次「全部地點」：頂 toast「已顯示全部地點」，掣變「只亮有事」。再撳一次：頂 toast「只亮有事做嘅地點」，掣變返「全部地點」。連撳兩下只算一次。
