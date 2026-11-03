# NOTES｜v19j 報名截止 applyDeadlineDays

**日期：** 2026-11-03（Asia/Hong_Kong）  
**SAVE：** `starVolunteer_map_v19j`  
**預覽：** https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19j  
**Soft≠PASS · 唔 publish · 出圖 HOLD**

## 用戶閘
Detail 要分開顯示 **報名截止**（`applyDeadlineDays`，距招募完結的日數）同 **獲聘後 N 日內完成**（`shootDeadlineDays`）。兩欄同時存在就兩句都出。缺 `applyDeadlineDays` 就隱藏該行，唔可以崩。

## 改動
1. `gigApplyDeadlineDays`／`gigApplyDeadlineText`：只接受有限、非負數字；否則當缺欄。文案 `報名截止 N 日 · 招募完結`。
2. `gigCastPeriodLine`（通告期間條共用）：第一行維持季節檔＋`獲聘後 N 日內完成`＋工作天；有報名截止先另起一行。`castWindow` 早退路徑一併帶上。
3. 通告卡 meta（同一句式，若重用檔期／meta）：有欄先加報名截止，再保留獲聘後句。
4. SAVE `starVolunteer_map_v19i` → `starVolunteer_map_v19j`（fetch `?v=` 一併 bust）。
5. `content/gigs_1988.json` **3.0.0**，**n=72**（72 則都有 `applyDeadlineDays`）。整檔 byte-identical。  
   **SHA256：** `f04f0d469a0013b793e30735f68cda4835eafbd017434be6dc9eab57ee973305`

## 抽樣（跟檔內數字）
| id | apply | shoot 句 |
|---|---|---|
| `gig_1988_film_01` | 報名截止 9 日 · 招募完結 | 獲聘後 21 日內完成 |
| `gig_1988_tv_01` | 報名截止 9 日 · 招募完結 | 獲聘後 15 日內完成 |
| `gig_1988_ad_01` | 報名截止 5 日 · 招募完結 | 獲聘後 14 日內完成 |
| `gig_1988_ad_02` | 報名截止 5 日 · 招募完結 | 獲聘後 14 日內完成 |

片酬 `$N`、條件 `名：>N`、違約金、作品名／類型／角色職位／導演、sticky 只留即場／搏一搏＋離開：沿用 19i，本 tip 未改顯示層。

## 唔做
- Soft PASS／publish／切圖
- 改 1989–1992
- 把報名截止寫成獲聘後句
- 刪或改檔內任何一則（包括 `gig_1988_ad_02` 的 `applyDeadlineDays`）
