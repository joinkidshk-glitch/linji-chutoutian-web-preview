# V17Y_LOC_SHEET_BOTTOM

**SAVE：** `starVolunteer_map_v17y`  
**時間：** 2026-11-03 ~06:59（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；出圖暫緩

## 對標（tester：維港電影 sheet 浮屏幕中間）

| # | 項 | 修法 |
|---|---|---|
| 1 | `#loc-sheet` 唔貼底 | DOM：搬出 `.map-wrap`，做 `#v-map` 直屬 sibling |
| 2 | 定位 | `position:absolute; inset:auto 0 0 0; bottom:0; top:auto` 相對 `#v-map` |
| 3 | 開合 | `.on` → `translateY(0)`；max-height 72dvh；頂圓角保留 |
| 4 | v17x modal | 唔改 `#modal-inner` scroll／`#modal-btns` sticky |

## Tester 覆測（1 行）
港島 · 維港電影：sheet 貼 #app／地圖底；清 starVolunteer_map_* 開 ?v=17y。

## Ship
- commit：（push 後填）
- curl-verify：（push 後填）
- tar：`/workspace/star-volunteer-web-v17y.tar.gz`
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=17y
- Soft≠PASS；出圖暫緩
