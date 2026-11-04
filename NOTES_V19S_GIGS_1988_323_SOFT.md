# NOTES｜v19s gigs_1988 3.2.3-soft n=137

**日期：** 2026-11-04（Asia/Hong_Kong）  
**SAVE：** `starVolunteer_map_v19s`  
**預覽：** https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19s  
**Soft≠PASS · 唔 publish · 出圖 HOLD**

## 改動
1. `content/gigs_1988.json` 換成 canonical **3.2.3-soft**，**n=137**。整檔 byte-identical。  
   **SHA256：** `cfc72fe8b6fa4797d333a4347800f395764c0d059989c609c5b5a12765b31c18`  
   `isKeyGig` true＝**66**（3.2.2 為 76；10 則初階 favor max=1 由 true 改 false）。檔內 `counts.keyGigs` 仍寫 76，以布林計數為準。
2. SAVE `starVolunteer_map_v19r` → `starVolunteer_map_v19s`。`refreshCopyPacksFromDisk` 的 fetch `?v=` 跟住 bust。
3. 未改行為閘、硬鎖、通告板 tier、教學 UX。未改 `gigs_1989`–`gigs_1992`。

## 初階 isKeyGig true→false
`gig_1988_ad_01`、`gig_1988_tv_01`、`gig_1988_rec_02`、`gig_1988_film_lion_autumn`、`gig_1988_rec_hk_winter`、`gig_1988_ad_adm_autumn_low`、`gig_1988_film_cotton_winter_low`、`gig_1988_rec_hk_autumn_low`、`gig_1988_tvb_harbour_autumn_low`、`gig_1988_tvb_longmen_winter_low`。  
favorDelta／rumorKeys／boardHookMode／pay／req／loc／season／tier／storyKeys／玩家面文案未因本步再改。玩家面經理人仍「何生」；favor target 仍 `agency_ho`。

## 載入
`refreshCopyPacksFromDisk` 先 `fetch(content/gigs_1988.json?v=SAVE)`。有 `gigs` 陣列就寫入 `STORY_WIRE.gigsByYear[1988]`，再 `syncGigsForCalendarYear` 用檔覆寫內嵌 `GIGS`，並把 `gigsVersion` 設成 `pack.version`。檔載入失敗先用內嵌 fallback（仍係舊 30 則，唔係 3.1.0）。接線資料面板來源會顯示 `gigs_1988.json · v3.2.3-soft`。

## Tester
硬 refresh `?v=19s`。Console `[WIRING] gigs 137`，來源檔 version **3.2.3-soft**。Soft≠PASS。
