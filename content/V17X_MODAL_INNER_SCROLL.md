# V17X_MODAL_INNER_SCROLL

**SAVE：** `starVolunteer_map_v17x`  
**時間：** 2026-11-03 ~06:50（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；出圖暫緩

## 對標（v17w：底欄 OK 但「滾動不到」）

| # | 項 | 修法 |
|---|---|---|
| 1 | #modal-inner 無限高／滾唔到 | flex:1 1 0% + min-height:0 !important + overflow-y:auto |
| 2 | .gig-carousel touch-action:pan-x 食垂直 pan | 改 pan-x pan-y（全域＋modal 內） |
| 3 | sticky .gig-actions 攔截 | pointer-events:none on bar；buttons auto |
| 4 | #modal-btns | 保持 v17w 釘底 |

## Tester 覆測（1 行）
香江《夜班咪》／紅棉《霓虹夜冷風暴》：底欄常駐；展開／收起後可垂直滾睇 syn／meta／錯季。清 starVolunteer_map_* 開 ?v=17x。

## Ship
- commit：`8cac263`（`8cac263de0e72e41ceea13bb5bb574aeeabbde2f`）· 2026-11-03 ~06:50 HKT
- curl-verify：**PASS** — SAVE v17x + flex 1 1 0% + min-height:0 + overflow-y auto + pan-x pan-y + modal-btns flex:0；LIVE HTML **1167170**
- tar：`/workspace/star-volunteer-web-v17x.tar.gz`
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=17x （清 starVolunteer_map_*）
- Soft≠PASS；出圖暫緩；瀏覽器覆測交 tester（靜態／curl 已過）
