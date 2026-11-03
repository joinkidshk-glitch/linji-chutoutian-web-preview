# V18C_PIN_BADGE_ANCHOR

**SAVE：** `starVolunteer_map_v18c`  
**時間：** 2026-11-03（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；唔 publish；出圖暫緩  
**契約：** 用戶 widget t276s1197「批準改地圖角標貼紅針再推 ?v=」；唔回歸 v18a／v18b 故事／JSON

## Bug

電話預覽地圖上「情報」／「有板」（及「劇」）角標錨喺成個 `.pin`（含闊 `.plab`），`top/right` 用 button 右上角 → 離紅針太遠；九龍電視台／星河電視台尤甚。

## Fix

| # | 項 | 做法 |
|---|---|---|
| 1 | DOM | `drawMap`：`<span class="pin-head">` 包住 `.marks` + `.pin-img`；`.plab` 仍喺 head 外 |
| 2 | CSS | `.marks` 改錨 `pin-head`；`top:4px; right:6px`（針圖 hit pad 10px 內 inset，貼視覺針頭） |
| 3 | Hit | `.pin-img` ≥44 pad 唔改；`.marks` `pointer-events:none` |
| 4 | Marker | pin class `v18c-pin-marks-hug`（curl-verify） |
| 5 | Story | JSON 1.2.5／v18a UX 唔動 |

## Tester 覆測（清 SAVE）

1. 清 `localStorage` `starVolunteer_map_*` 後開 `?v=18c`
2. 地圖睇九龍電視台／星河電視台：有板或情報時角標貼紅針頭右上，唔再飄去 label 右外
3. 點針仍準（≥44）；label 仍可點
4. 靜態：SAVE v18c；`v18c-pin-marks-hug`／`pin-head` 存在；JSON 仍 1.2.5

## Ship

- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18c
- tar：`/workspace/star-volunteer-web-v18c.tar.gz`
- Soft≠PASS · 出圖 HOLD
