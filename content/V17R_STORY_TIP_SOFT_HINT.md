# V17R_STORY_TIP_SOFT_HINT

**SAVE：** `starVolunteer_map_v17r`  
**時間：** 2026-11-03 ~02:17（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`（lean Pages）  
**HOLD：** Soft≠PASS；唔 formal publish；出圖暫緩

## 對標（夜間自主｜劇情可發現性）

| # | 項 | 根因 | 修法 |
|---|---|---|---|
| 1 | 地圖事態 tip 金色描邊唔生效 | CSS 寫 `.pin.has-tip.story-tip`；JS 只加 `has-story-tip` | CSS 同時認 `.has-story-tip`；保留舊 `.story-tip` |
| 2 | soft C5 `nextHint` 露「這段」＋`P1.5` | `STORY_HINT_SOFT.C5` 未跟 JSON 1.2.1 | 改「呢段」＋「會嚟嘅新事態」（同 pack） |
| 3 | 事態 tip 同情報 tip 視覺撞 | `drawMap` 一律 `legend_intel`／💡 | story tip 改「劇」角標；aria「· 事態」 |

## 改動檔

- `/workspace/star-volunteer-web/index.html`（SAVE→v17r；CSS；soft hint；marks／aria）
- 本 NOTES

## 自檢

- [x] SAVE＝v17r
- [x] soft C5 無 P1.5／這段
- [x] `.has-story-tip .dot`／`.plab` 金色規則在碼
- [ ] Soft≠PASS；出圖未做
- [ ] 瀏覽器覆測：金 tip＋「劇」標；C1→結算→地圖

## Ship

- commit：`03e819f`（03e819fdc54261bd809e4bec919381748c668213）· 2026-11-03 02:17 HKT
- curl-verify：**PASS** — SAVE v17r + `has-story-tip .dot` + `mark-story` + soft C5「呢段」；LIVE HTML **1154424**
- tar：`/workspace/star-volunteer-web-v17r.tar.gz`
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=17r （清 `starVolunteer_map_*`）
