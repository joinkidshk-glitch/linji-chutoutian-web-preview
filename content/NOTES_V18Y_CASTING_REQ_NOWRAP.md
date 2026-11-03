# NOTES｜v18y 通告 Detail 條件列 nowrap（斷行 nit）

**日期：** 2026-11-03（Asia/Hong_Kong）  
**SAVE：** `starVolunteer_map_v18y`  
**預覽：** https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18y  
**狀態：** Soft≠PASS · 出圖 HOLD · 唔 publish  

**對齊：**  
- tester `?v=18x` 斷行 nit（`· 合|未合` 孤兒換行）  
- `PLAN_GIG_CASTING_REQ_NUM_COPY_v1` 句式一字勿改骨架  
- 出圖 HOLD（無新 PNG）

---

## 本輪改動

1. **CSS `.cn-cond-row`**  
   - `font-size:.78rem; letter-spacing:-.02em; line-height:1.3`  
   - 維持 `word-break:keep-all; line-break:strict`  
   - `.ok`／`.no`：`white-space:nowrap; display:inline-block; max-width:100%`  
   - 長聲望列：`font-size:clamp(.68rem, 3.1vw, .8rem)` 優先於允許 `·合` 斷行  

2. **字串膠尾（Detail + `reqHtml`）**  
   - ` · ${mark}` → NBSP·NBSP（`\u00a0·\u00a0${mark}`）  
   - 可見句式仍：`名：現 cur／要求 need · 合|未合`；聲望 `這檔要求`  

3. **SAVE**  
   - `starVolunteer_map_v18x` → `starVolunteer_map_v18y`

---

## 鏡射／部署

`sv-phone-preview` → `star-volunteer-web` → `/tmp/linji-chutoutian-web-preview` push `main`（no force）。  

Soft≠PASS · 出圖 HOLD
