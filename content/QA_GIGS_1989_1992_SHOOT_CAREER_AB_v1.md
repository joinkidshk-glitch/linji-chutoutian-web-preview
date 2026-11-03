# QA｜HANDOFF_GIGS_1989_1992_SHOOT_CAREER_AB_v1

> 2026-11-03（Asia/Hong_Kong）｜靜態抽樣審計  
> 路徑：`/workspace/sv-phone-preview/content/`（mirror preview）  
> 對照 store：`/cursor/stores/store-cbdfa415-74f6-4e12-8fbd-513ef31077be/`  
> LIVE：`/workspace/star-volunteer-web/content/`（只讀比對，**未推／未發佈**）  
> **Soft≠PASS**；全量出圖 HOLD。唔當 Soft PASS。

## Verdict

**PASS**（靜態抽樣；無 FAIL blocker；無 nits）  
**Soft≠PASS**

未做 runtime／手帳／hard-hide 板面實機；未推版。

---

## 總表

| 年 | ver | SHA16（preview） | store=preview | LIVE=preview | n | empty loc×季 | film_harbour 春/秋 | tvb_harbour 春/秋 |
|---|---|---|---|---|---|---|---|---|
| 1989 | 1.1.0 | `11c983094fdd1f40` | ✅ | ✅ | 52 | **0** | 1 / 1 | 1 / 1 |
| 1990 | 1.1.0 | `fa1ac9aa1b24da2b` | ✅ | ✅ | 53 | **0** | 1 / 1 | 1 / 2 |
| 1991 | 1.1.0 | `63a1ad8cfa62b35d` | ✅ | ✅ | 52 | **0** | 1 / 1 | 1 / 1 |
| 1992 | 1.1.0 | `8965d60dd2ef06dd` | ✅ | ✅ | 51 | **0** | 1 / 1 | 1 / 1 |

Claimed SHA／n／ver 全部對上；preview ≡ store ≡ LIVE（本輪檔案已一致，但仍 **Soft≠PASS**，唔等於可當產品 PASS）。

### 1988 spot-check（本輪不動）

| 源 | ver | SHA16 | n |
|---|---|---|---|
| preview | **2.3.0** | `c58ccfa828e8ecf5` | 52 |
| store | **2.3.0** | `c58ccfa828e8ecf5` | 52 |

與 handoff「1988 未改」一致。未修改任何 1988 檔。

---

## Checks

### 1. version + count

| 年 | claimed | observed | OK |
|---|---|---|---|
| 1989 | 1.1.0 / 52 | 1.1.0 / 52 | ✅ |
| 1990 | 1.1.0 / 53 | 1.1.0 / 53 | ✅ |
| 1991 | 1.1.0 / 52 | 1.1.0 / 52 | ✅ |
| 1992 | 1.1.0 / 51 | 1.1.0 / 51 | ✅ |

### 2. SHA16（sha256 首 16 hex）

四檔 preview／store／LIVE 均＝handoff claimed。✅

### 3. Raised career fields（對齊 1988 2.3.0 schema）

每則皆有：`roleScale`／`shootBand`／`shootDaysHint`／`shootWeekdays`／`shootDeadlineDays`。

- days ∈ shootBand：**0** 違規  
- `shootDeadlineDays = max(ceil(days×7/|wd|)+2, days+3)`：**0** 違規  
- weekday-only `[1..5]`／weekend-only `[6,7]` 數量與 handoff 一致（89:24/5，90:23/5，91:24/5，92:22/5）

#### type×roleScale 日帶抽樣（每年度）

| 年 | id | type | roleScale | days | band | wd | deadline | 合理？ |
|---|---|---|---|---|---|---|---|---|
| 1989 | `gig_1989_ad_01` | 廣告 | `ad_av` | 3 | [3,4] | [6,7] | 13 | ✅ 短廣告週末 |
| 1989 | `gig_1989_photo_01` | 廣告 | `photobook` | 6 | [5,7] | [5,6,7] | 16 | ✅ 寫真 |
| 1989 | `gig_1989_mtv_01` | 唱片通告 | `mtv` | 3 | [2,3] | [6,7] | 13 | ✅ MTV 週末 |
| 1989 | `gig_1989_film_09` | 電影 | `film_lead_big` | 29 | [28,30] | [1–6] | 36 | ✅ 長電影男主 |
| 1989 | `gig_1989_tv_10` | 電視劇 | `tv_lead_long` | 22 | [20,24] | [1–6] | 28 | ✅ 長劇男主 |
| 1990 | `gig_1990_mtv_01` | 唱片通告 | `mtv` | 3 | [2,3] | [6,7] | 13 | ✅ |
| 1990 | `gig_1990_film_10` | 電影 | `film_lead_big` | 29 | [28,30] | [1–6] | 36 | ✅ |
| 1990 | `gig_1990_tv_09` | 電視劇 | `tv_lead_long` | 22 | [20,24] | [1–6] | 28 | ✅ |
| 1990 | `gig_1990_photo_01` | 廣告 | `photobook` | 6 | [5,7] | [5,6,7] | 16 | ✅ |
| 1991 | `gig_1991_mtv_01` | 唱片通告 | `mtv` | 3 | [2,3] | [6,7] | 13 | ✅ |
| 1991 | `gig_1991_film_10` | 電影 | `film_lead_big` | 29 | [28,30] | [1–6] | 36 | ✅ |
| 1991 | `gig_1991_tv_07` | 電視劇 | `tv_lead_long` | 22 | [20,24] | [1–6] | 28 | ✅ |
| 1992 | `gig_1992_film_01` | 電影 | `film_lead_big` | 29 | [28,30] | [1–6] | 36 | ✅ |
| 1992 | `gig_1992_mtv_01` | 唱片通告 | `mtv` | 3 | [2,3] | [6,7] | 13 | ✅ |
| 1992 | `gig_1992_tv_06` | 電視劇 | `tv_lead_long` | 22 | [20,24] | [1–6] | 28 | ✅ |
| 1992 | `gig_1992_photo_01` | 廣告 | `photobook` | 6 | [5,7] | [5,6,7] | 16 | ✅ |

Handoff A／B 抽樣列（含 before→after days）字段值全部核對通過。

### 4. loc × season（11 loc × 春夏秋冬）

每年度 loc 池相同 11 個：  
`ad_adm`, `ad_central`, `film_cotton`, `film_harbour`, `film_lion`, `rec_hk`, `rec_star`, `rec_wanchai`, `tvb_harbour`, `tvb_kowloon`, `tvb_longmen`。

| 年 | empty cells | film_harbour 春 | film_harbour 秋 | tvb_harbour 春 | tvb_harbour 秋 |
|---|---|---|---|---|---|
| 1989 | **0** | 1 | 1 | 1 | 1 |
| 1990 | **0** | 1 | 1 | 1 | 2 |
| 1991 | **0** | 1 | 1 | 1 | 1 |
| 1992 | **0** | 1 | 1 | 1 | 1 |

海港春／秋均 ≥1。✅（靜態矩陣；runtime hard-hide 板面未測）

### 5. Career supplements（寫真／MTV／長電影／長電視）

| 年 | photobook | mtv | film_lead_big | tv_lead_long |
|---|---|---|---|---|
| 1989 | 2 | 1 | 1 | 1 |
| 1990 | 2 | 1 | 1 | 1 |
| 1991 | 2 | 1 | 1 | 1 |
| 1992 | 2 | 1 | 2 | 1 |

每年四類皆 ≥1。✅  
（1992 career B 新則無另加 `film_lead_big`，但既有抬欄已有 `gig_1992_film_01` 等，直方圖＝2，符合「庫內有長電影男主」。）

### 6. Handoff fill／career ids 存在

| 年 | claimed new／fill ids | missing |
|---|---|---|
| 1989 | 5 career + 10 fill | **0** |
| 1990 | 5 career + 11 fill | **0** |
| 1991 | 5 career + 10 fill | **0** |
| 1992 | 4 career + 17 fill | **0** |

含 `gig_*_film_*` 海港春／秋填縫 id（如 `gig_1989_film_11`／`_12`、`gig_1990_film_13`、`gig_1991_film_12`／`_14`、`gig_1992_film_15`）皆在庫。✅

---

## FAIL blockers

**無。**

## Nits

**無**（靜態範圍內）。

## Soft≠PASS

- Soft ≠ PASS（硬規則；本報告唔當 Soft PASS）。  
- 未做：每季 hard-hide 後通告板實機、手帳排期／逾期罰則、全量出圖。  
- 未推／未發佈任何東西。  
- 下一步仍歸 tester／用戶拍板（handoff §下一步）。

---

*完 — QA_GIGS_1989_1992_SHOOT_CAREER_AB_v1*
