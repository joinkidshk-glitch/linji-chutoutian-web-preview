# V17U_YEAR_HUD_PIN

**SAVE：** `starVolunteer_map_v17u`  
**時間：** 2026-11-03 ~05:58（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；出圖暫緩

## 對標（本輪 widget 批核）

| # | 項 | 修法 |
|---|---|---|
| 1 | 年切瀏覽器難驗 1989–1992 | `window.S` / `syncGigsForDay`(=syncGigsForCalendarYear) / `gigsByYear`；選單「接線／年份」常開：packs 旗標 + →1988–1992 / force sync |
| 2 | 頂 HUD 擠（名貼邊） | `.bar` padding／`.who` ellipsis／chips max-width |
| 3 | C3→C4 星河 stale story-pin | `scheduleStoryMapRedraw`（rAF×2 + 140ms）於 markDone／showResult／回地圖 |

## 唔重做
v17r tip 金／v17s legend／v17t board-tut — 已 live。

## Tester：年切（1–2 行）
選單 → **接線／年份** → 睇 packs／按 →1989…；或 Console：`previewJumpCalendarYear(1989)`、`syncGigsForDay(true)`、`gigsByYear`。清舊 `starVolunteer_map_*` 後開 `?v=17u`。

## Ship
- commit：（push 後填）
- curl-verify：（push 後填）
- tar：`/workspace/star-volunteer-web-v17u.tar.gz`
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=17u
- Soft≠PASS；出圖暫緩
