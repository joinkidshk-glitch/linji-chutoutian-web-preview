# NOTES｜v19c 片酬 exact＋違約金＋synopsis clip（同一 tip）

**日期：** 2026-11-03（Asia/Hong_Kong）  
**SAVE：** `starVolunteer_map_v19c`  
**預覽：** https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19c  
**狀態：** Soft≠PASS · 出圖 HOLD · 唔 publish  

**對齊：**  
- `PLAN_GIG_PAY_EXACT_v1`  
- `PLAN_GIG_BREACH_FEE_v1`（用戶已刪簽約）  
- P0 synopsis clip（v19b CSS 保留於本 tip／本 SAVE）  
- 出圖 HOLD（無新 PNG）

---

## 本輪改動

### A. 劇情簡介 clip（P0；自 v19b 帶入）

- `.notice_sheet_frame`：`overflow:hidden`＋column flex  
- `.notice_synopsis_frame`：`max-height:min(28vh, 9.5rem)`；`overflow:hidden`  
- 內文 `p`：`overflow-y:auto`（框內滾）；外層 `#modal-inner` 仍滾整張 sheet  
- 唔蓋 sticky `#modal-btns`；保留 v18w pad／v19a `.cn-pay` nowrap

### B. 片酬 exact（`PLAN_GIG_PAY_EXACT_v1`）

- helper `gigPayExact(g)`：`payExact` → `payFixed` → `pay` number → `pay[]` 中位 `round((lo+hi)/2)` → null  
- 顯示 `$4,000`（千分位、`$` 後無空格）；Detail 包 `.cn-pay`  
- 短卡／teaser／舊 `gigCardHtml` meta：**刪**「約」／`$A–B`；改 `片酬 $N`／`酬勞 $N`  
- **顯示＝中位 stub**（無 `payExact` 時）；等劇本抬 `payExact`  
- 引擎獲聘仍可 `R(pay[0],pay[1])`（只改顯示層）

### C. 違約金（`PLAN_GIG_BREACH_FEE_v1`）

- Detail 右欄最終：片酬 → **違約金**（**無簽約**、**無特殊**）  
- `gigBreachFee(g)`：`breachFee` → else 由 P 派生（高 `0.6` min 1000；其他 `0.5` min 500；cap≤P）  
- `scheduleShoot` 寫入 `sh.breachFee`  
- `failShootOverdue`：掉單句 → 扣違約金（`apply` 錢 floor 0）→ fame／stress／pop（既有）＋書面句；錄音單用「未完成錄音」  
- HUD 可選加「逾期將扣除違約金 $X」

---

## 例

| 資料 | Detail |
|---|---|
| `pay:[3000,5000]` 初 | 片酬 `$4,000` · 違約金 `$2,000` |
| `payExact:8000` 高 | 片酬 `$8,000` · 違約金 `$4,800` |

---

## 鏡射／部署

`sv-phone-preview` → `/tmp/linji-chutoutian-web-preview` push `main`（no force）。  

Soft≠PASS · 出圖 HOLD
