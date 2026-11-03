# NOTES｜v19k gigs_1988 3.1.0 n=137

**日期：** 2026-11-03（Asia/Hong_Kong）  
**SAVE：** `starVolunteer_map_v19k`  
**預覽：** https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19k  
**Soft≠PASS · 唔 publish · 出圖 HOLD**

## 改動
1. `content/gigs_1988.json` 換成 canonical **3.1.0**，**n=137**（保留 3.0.0 全 72＋補槽 65）。整檔 byte-identical。  
   **SHA256：** `378fae3490f262e50f138b7946c17c0c06bab4dc24da0a1e1e818708f9ef12af`
2. SAVE `starVolunteer_map_v19j` → `starVolunteer_map_v19k`。`refreshCopyPacksFromDisk` 的 fetch `?v=` 跟住 bust。
3. 保留 v19j `applyDeadlineDays` Detail 接線（`gigApplyDeadlineDays`／`gigApplyDeadlineText`／`gigCastPeriodLine`）。硬鎖「條件未齊／暫未能報」未改。
4. 未改 `gigs_1989`–`gigs_1992`。未改顯示層。

## 載入
`refreshCopyPacksFromDisk` 先 `fetch(content/gigs_1988.json?v=SAVE)`。有 `gigs` 陣列就寫入 `STORY_WIRE.gigsByYear[1988]`，再 `syncGigsForCalendarYear` 用檔覆寫內嵌 `GIGS`，並把 `gigsVersion` 設成 `pack.version`。檔載入失敗先用內嵌 fallback。接線資料面板來源會顯示 `gigs_1988.json · v3.1.0`。

## Tester
Browser-sample loc×季×tier。Soft≠PASS。
