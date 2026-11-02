# V17W_MODAL_BTNS_STICKY

**SAVE：** `starVolunteer_map_v17w`  
**時間：** 2026-11-03 ~06:33（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；出圖暫緩

## 對標（tester 截圖：紅棉《霓虹夜冷風暴》無底鈕）

| # | 項 | 修法 |
|---|---|---|
| 1 | #modal-btns 跟內容滾走 | .modal flex column + overflow:hidden；#modal-btns flex:0 釘底 cream bar |
| 2 | 長卡只滾內容 | 只 #modal-inner overflow-y:auto |
| 3 | 鎖住試鏡首屏 | .gig-actions sticky bottom；卡 padding 略收；btn ≥44 |

## Tester 覆測（1 行）
只睇通告板 · 紅棉影業 · 《霓虹夜冷風暴》：首屏見鎖住試鏡；底欄常駐「返地點選單／關閉」唔使滾到底。清 starVolunteer_map_* 開 ?v=17w。

## Ship
- commit：`c76d015`（`c76d015e2e128248b2c171f29f4476a32b0febe1`）· 2026-11-03 ~06:33 HKT
- curl-verify：**PASS** — SAVE v17w + modal overflow hidden + #modal-inner scroll + #modal-btns flex:0 + gig-actions sticky；LIVE HTML **1166329**
- tar：`/workspace/star-volunteer-web-v17w.tar.gz`
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=17w （清 starVolunteer_map_*）
- Soft≠PASS；出圖暫緩；瀏覽器覆測交 tester（靜態／curl 已過）
