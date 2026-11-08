# NOTES · Soft tip #107 — 傳聞高亮框貼卡

> **狀態：** Soft≠PASS｜**唔 tip LIVE**｜SAVE `starVolunteer_map_v19w`｜產品 `?v=20a10` 唔抬  
> **softRev：** `s107`  
> **預覽：** `https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=20a10&softBehaviorGate=1&softRev=s107`  
> `<html data-soft-rev="s107">` 先算載到今次 index。89–92 HOLD。出圖 HOLD。  
> 基線：Soft tip #106 main `5b56aa93`／softRev=`s106`。

## 玩家面

- 行程手帳 →「傳聞」。金色虛線高亮框包住**一張**「剛聽聞」，上下相鄰卡唔再被框切住。
- 揀兩張做拼合時，每張卡嘅邊緣金光同樣貼住自己張卡。
- 傳聞教學未完（未跳過、未成功拼合）先見目標槽。跳過或拼合成功之後，目標槽同拖曳指引一齊收。
- 冇新圖。卡面排版唔改。

## 根因

- Soft Phase2 喺第一張未揀嘅「剛聽聞」掛 `fx_slot_highlight.png`（360×200）。`.tut-fx-edge` 係 `fx_merge_edge_glow.png`（420×280）。
- `<img>` 係 replaced element。`width`／`height` 都係 `auto` 時跟 PNG 固有尺寸，`inset` 嘅底邊被 over-constrained 規則甩掉。框高約 200px，短過張卡就向下溢出（卡本身無 `overflow:hidden`），視覺上跨兩張卡。

## 本票做咗咩

- `.tut-fx-slot`／`.tut-fx-edge` 用 `left/right/top/bottom: -6px` 加 `width/height: calc(100% + 12px)`，逼 layout 盒貼卡 ±6px。`max-width/max-height: none`。同一張 PNG，`object-fit:fill`。
- 目標槽跟拖曳指引：`!rumorTutorialDone()` 先掛。教學進行中仍然有槽；完成或跳過先收。拼合邊緣光唔跟呢個閘。

## 本票唔做

- 唔 tip LIVE；唔抬 SAVE；唔抬產品 `?v=20a10`。
- 唔出圖；89–92 HOLD。
- 唔改 merge 邏輯、傳聞文案、PNG。

## Console

- `__newspaper.check()`（框架同主線載入後）應 `{ ok:true, softRev:"s107", version:"v20a10", softStatus:"≠PASS" }`
- `runSoftP0Checks()` 應 `ok:true`（`data-soft-rev` 同 URL `softRev=s107`）

## QA

新分頁開上面條 URL。新遊戲，跳過開局教學，手帳「傳聞」：第一張「剛聽聞」嘅虛線框完全包住嗰張卡，唔切到下一張。點兩張「剛聽聞」，每張邊緣金光貼自己張卡。跳過傳聞教學或拼合成功後，目標槽收起；再揀兩張時邊緣金光仍貼卡。
