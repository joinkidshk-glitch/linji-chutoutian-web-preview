# V17T_BOARD_TUT_RETURN

**SAVE：** `starVolunteer_map_v17t`  
**時間：** 2026-11-03 ~04:35（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；出圖暫緩

## 對標（QA_V17S_BROWSER_v1 nits）

| # | 項 | 修法 |
|---|---|---|
| 1 | 首次鎖板 tut dismiss 返地圖 | `maybeShowTutToast(..., ()=>doScout(L))`（原 `()=>{}`） |
| 2 | C1 後 B01 仍推「先練／先賺」 | `showB01HomeModal`：C1 done → 改下一宗事態／已播完文案 |

## Ship

- commit：`db2b2fa`（`db2b2fa134d24930ae48faf5d815527bcbe2f18d`）· 2026-11-03 ~04:35 HKT
- curl-verify：**PASS** — SAVE v17t + `doScout(L)` after TUT_AUD_LOCK + B01 post-C1 copy；LIVE HTML **1157020**
- tar：`/workspace/star-volunteer-web-v17t.tar.gz`
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=17t （清 `starVolunteer_map_*`）
- Soft≠PASS；出圖暫緩；瀏覽器全量覆測交下輪（靜態／curl 已過；對標 QA_V17S P1）
