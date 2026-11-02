# V17U_YEAR_HUD_PIN

**SAVE：**   
**時間：** 2026-11-03 ~05:59（Asia/Hong_Kong）  
**預覽：**   
**HOLD：** Soft≠PASS；出圖暫緩

## 對標（本輪 widget 批核）

| # | 項 | 修法 |
|---|---|---|
| 1 | 年切瀏覽器難驗 1989–1992 |  / (=syncGigsForCalendarYear) / ；選單「接線／年份」常開：packs 旗標 + →1988–1992 / force sync |
| 2 | 頂 HUD 擠（名貼邊） |  padding／ ellipsis／chips max-width |
| 3 | C3→C4 星河 stale story-pin | （rAF×2 + 140ms）於 markDone／showResult／回地圖 |

## 唔重做
v17r tip 金／v17s legend／v17t board-tut — 已 live。

## Tester：年切（1–2 行）
選單 → **接線／年份** → 睇 packs／按 →1989…；或 Console：、、。清舊  後開 。

## Ship
- commit：（）· 2026-11-03 ~05:59 HKT
- curl-verify：**PASS** — SAVE v17u + window.S / syncGigsForDay / gigsByYear + 接線／年份 + HUD pad + scheduleStoryMapRedraw；LIVE HTML **1161987**
- tar：
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=17u （清 ）
- Soft≠PASS；出圖暫緩；瀏覽器覆測交 tester（靜態／curl 已過）
