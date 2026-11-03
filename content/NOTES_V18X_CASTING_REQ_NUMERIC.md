# NOTES｜v18x 通告 Detail 條件現值／門檻（PLAN_GIG_CASTING_REQ_NUM_COPY_v1）

**日期：** 2026-11-03（Asia/Hong_Kong）  
**SAVE：** `starVolunteer_map_v18x`  
**預覽：** https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18x  
**狀態：** Soft≠PASS · 出圖 HOLD · 唔 publish  

**對齊：**  
- 用戶拍板＋`PLAN_GIG_CASTING_REQ_NUM_COPY_v1.md`  
- `PLAN_GIG_CASTING_NOTICE_DETAIL_v1` §3.7 覆寫  
- 出圖 HOLD（無新 PNG）

---

## 本輪改動

1. **Detail `castingNoticeDetailHtml` 條件列**  
   - 能力：`{名}：現 {cur}／要求 {need} · 合|未合`（綠 `ok`／紅 `no`）  
   - 聲望：`聲望：現 {cur}／這檔要求 {need} · 合|未合`  
   - 空：`組製暫無額外能力條件`  
   - **禁**差N／你X／≥／裸 `>`

2. **`reqHtml`（試鏡 modal／殘 gigCardHtml）**  
   - 同句式，保持一致。

3. **`SHOW_REQ_THRESHOLD`**  
   - 刪 flag；永遠數字句（唔走舊合／未合-only／唔走舊 `> N`）。

4. **列表短卡 `gig-teaser`**  
   - 維持無數字（唔顯示條件列）。

---

## 鏡射／部署

`sv-phone-preview` → `star-volunteer-web` → `/tmp/linji-chutoutian-web-preview` push `main`（no force）。  

Soft≠PASS · 出圖 HOLD
