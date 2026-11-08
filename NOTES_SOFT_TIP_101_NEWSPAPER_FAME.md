# NOTES · Soft tip #101 — 報紙＋「聲量」正名「聲望」

> **狀態：** Soft≠PASS｜**唔 tip LIVE**｜SAVE `starVolunteer_map_v19w`｜產品 `?v=20a10` 唔抬  
> **softRev：** `s101`  
> **預覽：** `https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=20a10&softBehaviorGate=1&softRev=s101`  
> `<html data-soft-rev="s101">` 先算載到今次 index。89–92 HOLD。出圖 HOLD。

## 玩家面正名
- HUD、手帳、存檔槽、通告條件、殺青短卡、頒獎結果、記數簿：`聲量`／`幕前聲量` → `聲望`／`幕前聲望`。
- 內部 key 唔改：`fame`、`stageVolume`、`#c-stage-volume`。`writeDualTrack` 仍接受舊標「幕前聲量」做別名。
- 業內信用唔改名。

## 報紙
- 觸發日寫入 `S.newspaperQueue`（同一單 `eventKey` 去重），**唔即彈整張報**。
- 文案種子：`content/STUB_NEWSPAPER_MORNING_SOFT_v1.json`（原 sha8 `51e207bf`；press nit 後 sha8 `d8efaca1`）。`wrap_success` 15、`award_win` 8、`award_nominee` 4。按桶＋`medium` 抽。schema sha8 `1343f543`。
- `publishDay = 觸發日 + 1`。進地圖，或下一日行程會耗日之前，先彈「今日報紙」。
- 同日多則合併一版：頭條 1＋短訊最多 3；再多就收成一句「同日還有 N 則」。
- 撳「收下這份剪報」（或點外面關閉）先加模板 `fameDelta`（玩家面「聲望」）、寫入 `S.newspaperClippings`。
- 模板有 `rumorEcho` 就寫一則來源「報紙」、狀態「已知」的耳語，唔入拼合。傳聞仍係圈內耳語。
- 殺青成功：`wrap_success` × 電影／電視／唱片／廣告／其他。種子未載到先用殺青 press 短句，聲望 +1。場內短卡照舊。
- 頒獎：得獎 `award_win`、入圍 `award_nominee`。觀禮同推辭唔入報。
- press nit：`np_wrap_film_03`、`np_win_tv_02`、`np_win_ad_02`、`np_nom_music_01`、`np_nom_ad_01` 的 headline／dek／clipLabel 改書面語。`rumorEcho` 口語保留。「聲量」只留喺種子 meta 禁詞說明。

## Console
- `__newspaper.check()`
- `__freeplay.check()` 會帶 `paper:` 失敗項

## QA
1. 新分頁開上面條 URL。頂欄同手帳見「聲望」，唔見「聲量」。
2. 殺青一單：當日只見「傳媒・街外・成績」短卡。過日、返地圖（或下一日耗日之前）先見整張報紙。收下後聲望增加，手帳「剪報」有頭條。
3. 頒獎出席後，次日先見該晚報紙。
4. `softBehaviorGate=1`。無 softSeed 要求。唔好用舊分頁重整。
