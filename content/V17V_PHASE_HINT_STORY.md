# V17V_PHASE_HINT_STORY

**SAVE：** `starVolunteer_map_v17v`  
**時間：** 2026-11-03 ~06:24（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；出圖暫緩

## 對標（v17u PASS soft nits）

| # | 項 | 修法 |
|---|---|---|
| 1 | 年跳 1992→1988 phase 卡 P5 | `recomputePhaseFromProgress`：由 done＋日曆年從頭計並 setPhase（可回落）；`previewJumpCalendarYear`／接線按鈕改叫它 |
| 2 | C3→C4 `.map-hint-story` 仍 C3「對對手硬／忍」 | `storyMapHintHtml` 用 playerHint（同 tip）；`scheduleStoryMapRedraw` 內 `refreshMapHintStory` |

## Tester 覆測（1 行）
接線／年份：1988→1992→1988 睇 phase／可出數回落；播完 C3 後地圖 `.map-hint-story` 應變 C4 hint（何生檯面…），針去中環廣告。清 `starVolunteer_map_*` 開 `?v=17v`。

## Ship
- commit：（push 後填）
- curl-verify：（push 後填）
- tar：`/workspace/star-volunteer-web-v17v.tar.gz`
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=17v
- Soft≠PASS；出圖暫緩
