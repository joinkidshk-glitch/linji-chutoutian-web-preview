# V18M_CHOICES_FIT

**SAVE：** `starVolunteer_map_v18m`  
**時間：** 2026-11-03（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；全量出圖未開；唔 publish

## 做咗咩

| # | 項 | 做法 |
|---|---|---|
| 1 | **P0 C1 choices 裁掣** | 真機 Safari：茶餐廳 stage 過高 → 第二選項「先賺錢、趕通告…」出屏；一屏無滾 |
| 2 | **縮 stage** | `.sp-mode-choices`：`min-height:96`／`max-height:min(24dvh,150px)`／`height:auto`／`flex:1 1 auto`（取代 v18j 180／200／36dvh） |
| 3 | **掣置底** | 根加 `sp-choices-layout`；`.sp-choices` `flex:0 0 auto`＋`margin-top:auto`；兩掣必須可視區完整 |
| 4 | **收 head** | choices 模式 meta／h3／synopsis padding＋字細；synopsis max-height 裁 |
| 5 | SAVE | `…_v18l` → `starVolunteer_map_v18m` |
| 6 | 未改 | Soft≠PASS；出圖 HOLD；gigs JSON／shoot-schedule 無動 |

## Tester 覆測（清 SAVE）

1. `?v=18m` 硬 refresh；SAVE=`starVolunteer_map_v18m`
2. C1 選項頁：兩掣（含「先賺錢、趕通告…」）一屏內完整可見；唔使整頁豎滾
3. 茶餐廳底圖仍見（較矮 crop／cover OK）；唔回歸短灰條
4. Soft≠PASS

## curl-verify（填 ship 後）

- SAVE=`starVolunteer_map_v18m`
- HTML：`sp-choices-layout` · `max-height:min(24dvh,150px)` · `v18m: choices-mode`

## Ship

- feature commit：`cf6dff29fa7d` (`cf6dff29fa7d8b0a1c6bdc97cd5ac9356c34b1ee`)
- tip／NOTES：`6a278ee8ebef` (`6a278ee8ebef739d7be0eff4a27e8c83b909be5a`)
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18m
- Soft≠PASS · 全量出圖 HOLD
