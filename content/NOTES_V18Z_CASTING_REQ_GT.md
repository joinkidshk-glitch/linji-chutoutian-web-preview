# NOTES｜v18z 通告 Detail 條件 `名：>N`（用戶改口）

**日期：** 2026-11-03（Asia/Hong_Kong）  
**SAVE：** `starVolunteer_map_v18z`  
**預覽：** https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18z  
**狀態：** Soft≠PASS · 出圖 HOLD · 唔 publish  

**對齊：**  
- 用戶改口 via tester（覆蓋 PLAN v1.0「現／要求 · 合」＋先前禁 `>`）  
- `PLAN_GIG_CASTING_REQ_NUM_COPY_v1` **v1.1**：`{名}：>{need}`／`聲望：>{need}`；色標達／未達；唔寫合未合／現值  
- 仍禁：差N／你X／≥  
- 出圖 HOLD（無新 PNG）

---

## 本輪改動

1. **`castingNoticeDetailHtml` condParts**  
   - 聲望：`<span class="ok|no">聲望：>{v}</span>`  
   - 能力：`<span class="ok|no">{lab}：>{v}</span>`  
   - 刪：`現 cur／要求`、`這檔要求`、`· 合|未合`、NBSP 膠尾  

2. **`reqHtml`**（其餘 gigCard 路徑）同上 `名：>{v}`／`聲望：>{floor}`  

3. **SAVE**  
   - `starVolunteer_map_v18y` → `starVolunteer_map_v18z`  
   - v18y nowrap 對長句已 **obsolete**（短句本身唔易 wrap；CSS nowrap 可留）

---

## 例（玩家面）

- `演技：>60`（綠＝達／紅＝未達）  
- `體力：>35`  
- `聲望：>20`  

短卡／teaser 仍可無數字。

---

## 鏡射／部署

`sv-phone-preview` → `star-volunteer-web` → `/tmp/linji-chutoutian-web-preview` push `main`（no force）。  

Soft≠PASS · 出圖 HOLD
