# NOTES · Soft tip #106 — 合版短訊亦入手帳傳聞

> **狀態：** Soft≠PASS｜**唔 tip LIVE**｜SAVE `starVolunteer_map_v19w`｜產品 `?v=20a10` 唔抬  
> **softRev：** `s106`  
> **預覽：** `https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=20a10&softBehaviorGate=1&softRev=s106`  
> `<html data-soft-rev="s106">` 先算載到今次 index。89–92 HOLD。出圖 HOLD。  
> 基線：Soft tip #105 main `b8a2cbcd`／softRev=`s105`。

## 玩家面

- 合版朝早報（常見：劇情＋殺青／頒獎／周刊）收下之後，手帳「傳聞」見到頭條同每一則短訊，來源都係「報紙」、狀態「已知」。
- 文案用該則已有 `rumorEcho`。空則仍然係「街外報紙寫道：「{headline}」。茶餐廳有人照著念。這是公開版面，不是圈內耳語。」
- 「同日還有 N 則」嗰行版面摘要唔入傳聞。
- 紙面、聲望加總、合版邊則做頭條、次日先出，都唔改。報紙唔加人情／好感。

## 根因

- #102 已把頭條 `rumorEcho` 經 `pushNewspaperRumor` 寫入 `mockRumors`（`source:"報紙"`、`state:"teased"`）。
- `buildNewspaperEdition` 只抄頭條 `rumorEcho`。短訊物件冇呢個欄。
- `pushNewspaperRumor` 只 push 一則，id 係 `paper_${edition.id}`。
- 合版按 `|fameDelta|` 排頭條，劇情稿多數變短訊，所以爭執／廠景交換／拒單嘅圈內耳語唔入手帳。種子 14 則本來就有 `rumorEcho`。

## 本票做咗咩

- 短訊補 `rumorEcho`（summary 行唔加）。
- `pushNewspaperRumor`：頭條 id 仍係 `paper_${edition.id}`。其餘非 summary 短訊另 push，id 係 `paper_${edition.id}_${eventKey}`，冇 eventKey 就用 `s` 加該則序號。同一 id 重入唔再加。
- `__newspaper.check()` 加合版單元：年賞頭條＋`story:C3:hard`＋`story:R_hiu_meet:exchange`。一次 `commitMorningPaper` 得三則 `source:"報紙"`／`state:"teased"`，文案對得上各則 `rumorEcho`（C3「嗌交」、廠景「休息角」）。再 commit 或再 push 唔加。空 echo 後備句同 summary 跳過另有斷言。C5 `story_rumor`、迴避淡紙、殺青淡紙回歸仍在。

## 本票唔做

- 唔 tip LIVE；唔抬 SAVE；唔抬產品 `?v=20a10`。
- 唔出圖；89–92 HOLD。
- 唔改種子文案；唔發明新標題／對白。
- 唔改合版排序、聲望加總、呈現時機。
- 唔因報紙加 favor／rel。唔做通告板氣味演算法。

## Console

- `__newspaper.check()`（框架同主線載入後）應 `{ ok:true, softRev:"s106", version:"v20a10", softStatus:"≠PASS" }`

## QA

新分頁開上面條 URL。同日見報一則高聲望頭條（頒獎或殺青）加兩則劇情短訊（例如廠景爭執同休息角交流）。下一朝收下報紙，打開手帳「傳聞」：除咗頭條，短訊對應嘅圈內耳語都在，來源「報紙」、狀態「已知」。再收同一份唔會多一則。
