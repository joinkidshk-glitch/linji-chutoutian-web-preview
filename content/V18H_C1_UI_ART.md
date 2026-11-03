# V18H_C1_UI_ART

**SAVE：** `starVolunteer_map_v18h`  
**時間：** 2026-11-03（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；全量出圖未開；**C1 UI test art only**（表情偏淡可後輪）

## 做咗咩

| # | 項 | 做法 |
|---|---|---|
| 1 | Art pack | Canonical `assets/story/c1/`＋MANIFEST；drop-in `assets/npc/`（bust）· `assets/bg/`（bg）· mirror `assets/dialog/`＋flat `assets/story/` |
| 2 | Resolver | bust／bg 搜尋加 `assets/story/c1/`、`assets/dialog/`；`bg_c1_tea_restaurant` CSS 佔位 |
| 3 | Emotion→expr | `spExprFromEmotion`（缺 expression 時）；worried→eyes_down(awi)／frown |
| 4 | C1 JSON | LIVE `story_detail` **1.2.8**：11 beats additive `kind`／`speakerId`／`emotion`／`expression`／`bg`（跟 ART_BRIEF §3） |
| 5 | SAVE | `…_v18g` → `starVolunteer_map_v18h` |
| 6 | **P0 boot fix** | 還原 StoryPlay `advance`／`skipToChoices`／`pickChoice`／`showResult`／`playerNotes`／`newlyOpenAfter`（v18g 誤刪 → `Uncaught ReferenceError: advance is not defined`） |
| 7 | 未改 | meet playerOffer；gift unlock；全量出圖；Soft≠PASS |

## Asset paths（公開預覽）

- `assets/story/c1/{bg_*,char_*_bust_*}`＋`MANIFEST.md`
- `assets/bg/bg_loc_tvb_longmen.jpg` · `assets/bg/bg_c1_tea_restaurant.jpg`
- `assets/npc/char_{hero,ho,cheung}_bust_*.png`

## Tester 覆測（清 SAVE）

1. `?v=18h` 硬 refresh；SAVE=`starVolunteer_map_v18h`
2. C1 beat0：系統置中＋`bg_loc_tvb_longmen` 實圖
3. beat1＋：茶餐廳底 `bg_c1_tea_restaurant`
4. 何生／阿偉／張：半身；beat4 阿偉 `eyes_down`；beat3 何生 `raise_brow`；beat10 阿偉 `raise_brow`
5. JSON version tip／curl 可見 1.2.8（若 UI 顯示）
6. Soft≠PASS；表情 Soft OK

## curl-verify（填 ship 後）

- SAVE=`starVolunteer_map_v18h`
- HTML markers：`function advance` `function showResult` `sp-stage` `char_hero_bust` `bg_c1_tea_restaurant` `assets/story/c1/` `spExprFromEmotion`
- 無殘缺 api：StoryPlay IIFE 含 advance／skipToChoices／pickChoice
- Asset HTTP 200：`assets/bg/bg_loc_tvb_longmen.jpg` · `assets/npc/char_ho_bust_default.png`

## Ship

- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18h
- feature commit： ()
- tip／NOTES commit：_pending_
- Soft≠PASS · 全量出圖 HOLD
