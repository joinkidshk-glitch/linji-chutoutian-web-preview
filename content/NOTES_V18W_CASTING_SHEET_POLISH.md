# NOTES｜v18w 通告 Casting Sheet polish（跟 v18v feedback）

**日期：** 2026-11-03（Asia/Hong_Kong）  
**SAVE：** `starVolunteer_map_v18w`  
**預覽：** https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18w  
**狀態：** Soft≠PASS · 出圖 HOLD · 唔 publish  

**對齊：**  
- tester／用戶 v18v feedback（每週斷字、兩欄頂、導演 chip、簡介被底欄吃、三掣擠）  
- `ART_BRIEF_CASTING_NOTICE_DETAIL_v1.md`＋`CASTING_DETAIL_WIRE.md`＋PLAN §4  
- 出圖 HOLD（無新 PNG）

---

## 本輪改動

1. **每週行**  
   - 右欄拆兩行：`每週 N 天`＋副行 `逢週一至六`（`gigCastingWeekdayHint`；連續日用「至」、唔塞錄音／拍攝動詞）。  
   - `.cn-kv .v`／`.cn-wd-sub`：`word-break:keep-all`＋`line-break:strict`，避免「週 二」中間斷字。

2. **左右兩欄頂對齊**  
   - 右欄 `.cn-lab` 改「難易度 ★★★★☆」（同左「條件」同一行高）。  
   - `.notice_table_cell` flex column、同 padding；grid `align-items:stretch`。

3. **導演**  
   - 移出橙頭 chip；橙頭只留作品名。  
   - 橙頭下普通副行 `.cn-director-line`：`導演：組製未公開`。

4. **劇情簡介可滾盡**  
   - `#mask.casting-sheet-on #modal-inner` 加 `padding-bottom`／`scroll-padding-bottom`（含 safe-area）。  
   - `.notice_sheet_frame` 底 padding 加大；CTA 仍係 `#modal-btns` 外層 pin，唔蓋內容。

5. **底三掣**  
   - `#mask.casting-sheet-on #modal-btns`：`flex-wrap`、gap 8、min-height 44。  
   - 掣 `flex:1 1 calc(50% - 8px)`（2＋1 wrap）；`≤360px` 直向 100% 寬。  
   - `modal({ castingSheet:true })` → mask class；`closeModal` 清 class。

---

## 鏡射／部署

`sv-phone-preview` → `star-volunteer-web` → `/tmp/linji-chutoutian-web-preview` push `main`（no force）。  

Soft≠PASS · 出圖 HOLD
