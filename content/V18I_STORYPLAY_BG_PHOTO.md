# V18I_STORYPLAY_BG_PHOTO

**SAVE：** `starVolunteer_map_v18i`  
**時間：** 2026-11-03（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；全量出圖未開

## 做咗咩

| # | 項 | 做法 |
|---|---|---|
| 1 | **P0 bg photo** | 定義 `window.__spApplyBgPhotos`：probe `data-sp-bg-fallbacks` → `style.backgroundImage` + class `has-photo`（v18h 只寫 fallback attr、未套圖） |
| 2 | Bust err | 定義 `window.__spBustErr` fallback chain |
| 3 | Candidate order | `spBgImageCandidates` prefer `assets/dialog/` → `assets/story/c1/` → `assets/bg/` |
| 4 | Render hook | `render` 後呼叫 `__spApplyBgPhotos(root)` |
| 5 | SAVE | `…_v18h` → `starVolunteer_map_v18i` |
| 6 | 未改 | Soft≠PASS；全量出圖 HOLD；art 沿用 v18h C1 pack |

## Tester 覆測（清 SAVE）

1. `?v=18i` 硬 refresh；SAVE=`starVolunteer_map_v18i`
2. C1：`.sp-bg-layer` 應有實圖（`has-photo`／background-image），唔止 gradient
3. beat0 `bg_loc_tvb_longmen`；beat1+ `bg_c1_tea_restaurant`
4. Soft≠PASS

## curl-verify（填 ship 後）

- SAVE=`starVolunteer_map_v18i`
- HTML：`__spApplyBgPhotos = function` · `function advance()` · `__spBustErr`
- Asset HTTP 200：`assets/dialog/bg_loc_tvb_longmen.jpg`

## Ship

- feature commit：`(pending)`
- tip／NOTES commit：`(pending)`
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18i
- Soft≠PASS · 全量出圖 HOLD
