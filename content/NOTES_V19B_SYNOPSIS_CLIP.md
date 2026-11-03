# NOTES｜v19b 通告 Detail 劇情簡介 clip＋框內滾

**日期：** 2026-11-03（Asia/Hong_Kong）  
**SAVE：** `starVolunteer_map_v19b`  
**預覽：** https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19b  
**狀態：** Soft≠PASS · 出圖 HOLD · 唔 publish  

**對齊：**  
- 用戶 via tester P0：Detail「劇情簡介」內容溢出／走出框、可蓋 sticky 底掣  
- 保留 v19a 片酬 nowrap（`.cn-pay`）＋右欄 `.cn-kv` 收緊  
- 保留 v18w `#modal-inner` pad／`#modal-btns` wrap  
- 出圖 HOLD（無新 PNG）

---

## 本輪改動（CSS only）

1. **`.notice_sheet_frame`**  
   - `overflow:hidden`；`min-height:0`；`display:flex; flex-direction:column`  
   - 子層唔畫出 sheet 紙框

2. **`.notice_synopsis_frame`**  
   - `overflow:hidden`；`min-height:0`；`max-height:min(28vh, 9.5rem)`  
   - flex column；`flex:0 1 auto`；`box-sizing:border-box`  
   - 長文唔再撐破簡介框

3. **`.notice_synopsis_frame p`**  
   - 移除 `max-height:none`  
   - `flex:1 1 auto; min-height:0`  
   - `overflow-y:auto`＋`-webkit-overflow-scrolling:touch`＋`overscroll-behavior:contain`  
   - 長劇情**框內滾**；外層 `#modal-inner` 仍可滾整張 sheet  
   - 唔蓋 `#modal-btns`（仍係 modal flex sibling pin）

4. **`.notice_synopsis_frame .cn-lab`／`.cn-role-note`**  
   - `flex:0 0 auto`（標籤／角色 note 唔被 p 擠走；p 縮高內滾）

---

## 刻意唔改

- 片酬 compact `$2,000–4,000`／`.cn-pay` nowrap  
- 條件 `名：>N`（v18z）  
- 簽約／特殊 stub `—`  
- `#mask.casting-sheet-on #modal-inner` padding-bottom／scroll-padding-bottom（v18w）

---

## 鏡射／部署

`sv-phone-preview` → `/tmp/linji-chutoutian-web-preview` push `main`（no force）。  

Soft≠PASS · 出圖 HOLD
