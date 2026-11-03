# NOTES｜v19a 通告 Detail 片酬 nowrap＋右欄收緊

**日期：** 2026-11-03（Asia/Hong_Kong）  
**SAVE：** `starVolunteer_map_v19a`  
**預覽：** https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19a  
**狀態：** Soft≠PASS · 出圖 HOLD · 唔 publish  

**對齊：**  
- 用戶 via tester：片酬中間斷字（`$ 2,000 — 4, / 000`）；右欄 label／值間距過闊  
- 條件 `名：>N` 維持 v18z，本輪唔改  
- 出圖 HOLD（無新 PNG）

---

## 本輪改動

1. **片酬字串**（`castingNoticeDetailHtml` `payStr`）  
   - 改 compact：`$2,000–4,000`（`$` 後無空格；en-dash；唔用 spaced em-dash）  
   - 包 `<span class="cn-pay">…</span>`：`white-space:nowrap`＋`word-break:keep-all`＋`overflow-wrap:normal`＋輕微 letter-spacing／字級，避免逗號後斷行  

2. **右欄 `.cn-kv` 收緊**  
   - `justify-content:flex-start`；`gap:4px`（原 8px）  
   - `.k` 固定約 `2.2em`；`.v` `margin-left:auto`（唔再靠巨大 space-between 中空）  
   - `.cn-kv .v`：`overflow-wrap:anywhere` → `normal`（保留 keep-all）  
   - 每週頂行 `.cn-kv-top` 同步 gap／k 寬  

3. **簽約／特殊（FYI stub）**  
   - UI 仍顯示 `—`  
   - 語意＝**長約／特殊條款** stub；劇本填入前維持空白 dash  
   - 本輪唔加 title／tooltip（可之後補）

---

## 例（玩家面）

- 片酬：`$2,000–4,000`（單行、唔斷）  
- 簽約：`—`（長約 stub）  
- 特殊：`—`（特殊條款 stub）  
- 條件：仍 `演技：>60`（綠／紅）

短卡／teaser 本輪未改數字格式。

---

## 鏡射／部署

`sv-phone-preview` → `/tmp/linji-chutoutian-web-preview` push `main`（no force）。  

Soft≠PASS · 出圖 HOLD
