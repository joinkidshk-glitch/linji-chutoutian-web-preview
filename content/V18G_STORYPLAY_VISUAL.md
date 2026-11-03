# V18G_STORYPLAY_VISUAL

**SAVE：** `starVolunteer_map_v18g`  
**時間：** 2026-11-03 12:41 HKT（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；全量出圖未開；**C1 UI test art gate** 已開（GD 產 bust／`bg_loc_tvb_longmen`；未到檔＝佔位＋路徑已留）  
**契約：** 用戶拍板劇情界面；schema 跟 `PLAN_STORY_UI_BEAT_SCHEMA_v1.md`；LIVE JSON **唔改**；meet／送禮 unlock **未改**

## Schema 鎖定

權威：`PLAN_STORY_UI_BEAT_SCHEMA_v1.md` · 引擎摘要：`SCHEMA_STORYPLAY_VISUAL_v1.md` · C1 測閘：`ART_BRIEF_C1_UI_TEST_v1.md`

- Beat：`kind` `speakerId` `speaker` `emotion` `expression` `lines` `locId` `bg`
- **無** `portrait`；bust＝speakerId→artId→`{artId}_bust_{expression}`
- emotion／expression 枚舉＝PLAN A.4（expression：`default|smile|frown|raise_brow|eyes_down|look_aside`）
- BG：beat.bg → beat.locId → node.locId → `bg_loc_*` → `bg_generic_interior`
- awi artId＝`char_hero`

## 做咗咩

| # | 項 | 做法 |
|---|---|---|
| 1 | StoryPlay CSS | `sp-stage` `sp-bust` `sp-plate` `sp-narration` `bg_loc_*`／`bg_generic_interior` |
| 2 | Render | dialogue bust＋plate；system 置中；emotion CSS tint；bg／bust drop-in＋onerror 鏈 |
| 3 | Registry | PLAN §B 主表＋legacy 名；artId 含 cast／extra |
| 4 | Asset slots | `assets/npc/` `assets/bg/` `assets/story/` README；等 GD drop-in |
| 5 | SAVE | `…_v18f` → `starVolunteer_map_v18g` |
| 6 | 未改 | LIVE beats 字段；meet playerOffer；gift unlock；Soft≠PASS；全量出圖 |

## Tester 覆測（清 SAVE）

1. `?v=18g` 硬 refresh；SAVE=`starVolunteer_map_v18g`
2. C1 系統拍：置中無 bust；底 `bg_loc_tvb_longmen`（有檔用圖，無檔用漸層）
3. 何生／阿偉／張：半身（現網 PORTRAITS 或 GD `char_*_bust_*`）
4. HTML 含 `sp-stage` `sp-bust` `sp-narration`
5. Soft≠PASS；全量出圖 HOLD

## curl-verify（公開 Pages）

- SAVE=`starVolunteer_map_v18g`
- HTML markers：`sp-stage` `sp-bust` `sp-narration` `char_hero` `bg_generic_interior` `raise_brow`
- curl confirmed 2026-11-03 12:41 HKT（Asia/Hong_Kong）
- raw + Pages both serve v18g SAVE

## Ship

- feature commit：`99f0b93fc5a5` (`99f0b93fc5a5a216c3aa572873d65ad860cfb7f5`)
- NOTES commit：`a7a372430f3d` (`a7a372430f3d` pending fill after this fix)
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18g
- tar：`/workspace/star-volunteer-web-v18g.tar.gz`
- Soft≠PASS · 出圖 HOLD（C1 UI test gate only）
