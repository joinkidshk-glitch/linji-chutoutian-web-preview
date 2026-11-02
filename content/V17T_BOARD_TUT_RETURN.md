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

- （push 後填）
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=17t
