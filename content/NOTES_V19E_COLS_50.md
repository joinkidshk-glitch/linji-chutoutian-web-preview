# NOTES｜v19e notice_table_frame 兩欄 50/50

**日期：** 2026-11-03（Asia/Hong_Kong）  
**SAVE：** `starVolunteer_map_v19e`  
**預覽：** https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19e  
**狀態：** Soft≠PASS · 出圖 HOLD · 唔 publish  
**授權：** t230u（用戶：兩個格子唔係平均分配）

---

## 改咗乜

Casting Detail 中間表 `.notice_table_frame` 垂直分隔線偏左（左欄較闊）。

| | before | after |
|---|---|---|
| CSS | `grid-template-columns:1.15fr .95fr;` | `grid-template-columns:1fr 1fr;` |

`@media (max-width:360px)` 仍 `grid-template-columns:1fr`（窄屏疊欄）——唔改。

唔改類型／角色 label nits；唔 publish；唔出圖。

## 鏡射／部署

`sv-phone-preview` → `/tmp/linji-chutoutian-web-preview` push `main`（no force）。

Soft≠PASS · 出圖 HOLD
