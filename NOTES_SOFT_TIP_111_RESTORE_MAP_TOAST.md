# NOTES · Soft tip #111 — 還原地圖 toast 同遠觀 placeholder（LIVE 覆蓋之後）

> **狀態：** Soft≠PASS｜**唔 tip LIVE**｜SAVE `starVolunteer_map_v19w`｜產品 `?v=20a10` 唔抬  
> **softRev：** `s111`  
> **預覽：** `https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=20a10&softBehaviorGate=1&softRev=s111`  
> `<html data-soft-rev="s111">` 先算載到今次 index。89–92 HOLD。出圖 HOLD。  
> 基線：main `007dc9b`（v20a64 Q 版群星，含 v20a59–v20a63）。Soft tip s110 `61d8aaf7` 之後，LIVE tip 把 Soft tip 層蓋返 `s107`。本票只移植 s108–s110 塊，唔整檔覆蓋 index，Q 版群星留低。

## 玩家面

- 地圖頂右掣「全部地點」⇄「只亮有事」。掣文案係**下一句指令**。
- 撳一次去**顯示全部**之後，toast「已顯示全部地點」，掣變「只亮有事」。
- 隔至少 500ms 再撳，toast「只亮有事做嘅地點」，掣變返「全部地點」。連撳只算一次。
- 地圖 filter toast 企喺地圖上方（`.toast-on-map`），唔壓底部快捷列。
- 遠觀 Phase3 紅星玩家面無「文案待補／選項待補」。同句 flavor 唔再重複一段。

## 本票做咗咩

- `SOFT_REV` `s107` → `s111`。SAVE、產品 `?v=20a10` 唔郁。
- 還原 `mapFilterToastText`、`applyMapShowAllLocs`、`wireMapShowAllLocs`（`detail > 1` 或 500ms echo 忽略）。
- 還原 `.toast-on-map` CSS，同 `toast()` 喺 `#v-map.on` 且無 sheet 時加／清 class。舊 `:has` 留作雙保險。
- 還原 `eraSightIsPlaceholder`（行現成 `freeplayIsPlaceholderLine`）同 `eraSightParagraphs` 過濾。`phase3Stars` 合併 `silhouetteDesc` 時唔寫入待補字串。
- 頒獎群星、Q 版人仔、作品圖、後果包留低。

## 本票唔做

- 唔 tip LIVE；唔抬 SAVE；唔抬產品 `?v=`。
- 唔出圖；89–92 HOLD。
- 唔回滾 v20a59–v20a64。

## Console

- `__newspaper.check()`（框架同主線載入後）應 `{ ok:true, softRev:"s111", version:"v20a10", softStatus:"≠PASS" }`
- `runSoftP0Checks()` 應 `ok:true`（`data-soft-rev` 同 URL `softRev=s111`）

## QA

新分頁開上面條 URL。入地圖，撳一次「全部地點」：頂 toast「已顯示全部地點」，掣變「只亮有事」。隔至少半秒再撳：頂 toast「只亮有事做嘅地點」，掣變返「全部地點」。遠觀紅星唔見「文案待補」。
