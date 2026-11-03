# HANDOFF｜gigs_1988 拍攝生涯 A→B v1

> 2026-11-03（Asia/Hong_Kong）｜對齊 `PLAN_SHOOT_CAREER_SCHEDULE_v2`  
> **用戶拍板**（經 tester）：A 抬全則欄 → B 每年約 4–6 則補缺邊。本輪只做 **1988**。  
> **Soft≠PASS**；全量出圖 HOLD。唔當 Soft PASS。

## 檔案

| 項 | 值 |
|---|---|
| LIVE | `/workspace/star-volunteer-web/content/gigs_1988.json` |
| mirror preview | `/workspace/sv-phone-preview/content/gigs_1988.json` |
| mirror store | `/cursor/stores/store-cbdfa415-74f6-4e12-8fbd-513ef31077be/gigs_1988.json` |
| backup | `gigs_1988_pre_shoot_career_ab_backup.json`（同目錄） |
| version | **2.2.0**（前：2.1.1） |
| SHA256₁₆ | `20a8b9740e802176` |
| n gigs | **30 → 35**（+5） |

## A｜抬欄（30／30）

每則補／對齊：

- `roleScale`（按 type×tier／標題關鍵字；見 PLAN §5）
- `shootBand` `[min,max]`
- `shootDaysHint`：已在 band 則保留；否則改 band 中位（或 low+1）；演唱會嘉賓 `rec_04` 手設 mid **12**
- `shootWeekdays`（1=一…7=日）
- `shootDeadlineDays` = `max(ceil(days×7/|wd|)+2, days+3)`

### 抽樣 3 則（before → after）

**Before**

| id | type/tier | roleScale | shootBand | days | weekdays | deadline | title |
|---|---|---|---|---|---|---|---|
| `gig_1988_ad_01` | 廣告/初 | — | — | 2 | — | — | 「星聲」隨身聽潮流街舞宣傳片 |
| `gig_1988_film_01` | 電影/初 | — | — | 2 | — | — | 《鐵血英雄傳》火海槍手替身 |
| `gig_1988_tv_06` | 電視劇/高 | — | — | 8 | — | — | 《城寨暗夜1988》臥底警察阿鋒 |

**After**

| id | — | roleScale | shootBand | days | weekdays | deadline | title |
|---|---|---|---|---|---|---|---|
| `gig_1988_ad_01` | — | `ad_av` | [3, 4] | **3** | `[1, 2, 3, 4, 5]` | **7** | 「星聲」隨身聽潮流街舞宣傳片 |
| `gig_1988_film_01` | — | `film_support_small` | [12, 15] | **13** | `[1, 2, 3, 4, 5, 6]` | **18** | 《鐵血英雄傳》火海槍手替身 |
| `gig_1988_tv_06` | — | `tv_lead_long` | [20, 24] | **22** | `[1, 2, 3, 4, 5, 6]` | **28** | 《城寨暗夜1988》臥底警察阿鋒 |

> 對 PLAN v2 §4：ad_01 days 2→3／film_01 2→13／tv_06 8→22；deadline 跟公式（tv_06=28，非舊建議 35）。

## B｜新則 +5

- `gig_1988_photo_01`
- `gig_1988_mtv_02`
- `gig_1988_film_07`
- `gig_1988_tv_08`
- `gig_1988_photo_02`

| id | type | tier | roleScale | days | weekdays | deadline | title |
|---|---|---|---|---|---|---|---|
| `gig_1988_photo_01` | 廣告 | 初 | `photobook` | 6 | `[5, 6, 7]` | 16 | 「星河映像」初夏寫真集《巷口少年》 |
| `gig_1988_mtv_02` | 唱片通告 | 初 | `mtv` | 3 | `[6, 7]` | 13 | 樂隊「夜航燈」主打快歌 MTV 男主角 |
| `gig_1988_film_07` | 電影 | 高 | `film_lead_big` | 29 | `[1, 2, 3, 4, 5, 6]` | 36 | 《獅子山下的信》歸僑少年阿信 |
| `gig_1988_tv_08` | 電視劇 | 高 | `tv_lead_long` | 22 | `[1, 2, 3, 4, 5, 6]` | 28 | 《渡輪彼岸》渡輪水手阿海 |
| `gig_1988_photo_02` | 廣告 | 中 | `photobook` | 6 | `[1, 2, 3, 4, 5]` | 11 | 「香江鏡框」冬日寫真集《大衣與街燈》 |

覆蓋補齊：`photobook`×2、`mtv`×2（原 1＋新 1）、`film_lead_big`×3（原抬 2＋新 1）、`tv_lead_long`×3（原抬 2＋新 1）。

## roleScale 直方圖（35）

| roleScale | n |
|---|---|
| `ad_av` | 6 |
| `ad_print` | 2 |
| `film_lead_big` | 3 |
| `film_support_main` | 2 |
| `film_support_small` | 2 |
| `mtv` | 2 |
| `photobook` | 2 |
| `rec_album` | 3 |
| `tv_cameo_short` | 2 |
| `tv_lead_long` | 3 |
| `tv_support_main` | 3 |
| `variety_ep` | 4 |
| `variety_special` | 1 |

## type counts

| type | n |
|---|---|
| 廣告 | 10 |
| 綜藝 | 5 |
| 電視劇 | 8 |
| 電影 | 7 |
| 唱片通告 | 5 |
| **total** | **35** |

## 星期多樣性（QA）

- weekday-only `[1,2,3,4,5]`：**11** ≥8 ✅  
  `['gig_1988_ad_01', 'gig_1988_ad_02', 'gig_1988_ad_05', 'gig_1988_ad_06', 'gig_1988_ad_07', 'gig_1988_ad_08', 'gig_1988_var_04', 'gig_1988_rec_01', 'gig_1988_rec_03', 'gig_1988_rec_04', 'gig_1988_photo_02']`
- weekend-only `[6,7]`：**6** ≥5 ✅  
  `['gig_1988_ad_03', 'gig_1988_ad_04', 'gig_1988_var_01', 'gig_1988_var_03', 'gig_1988_rec_02', 'gig_1988_mtv_02']`
- 其餘多為廠／實景 `[1,2,3,4,5,6]`；寫真 `photo_01`＝`[5,6,7]`

## 引擎／iOS 注意

1. 跟 `roleScale`／`shootBand`，**唔再**跟 tier 日數下限（v1 廢止）。  
2. 手帳：只許 `shootWeekdays`；排滿 `shootDaysHint`；逾 `shootDeadlineDays` → PLAN §3 罰則一次。  
3. 缺欄 fallback 仍：平日 + `max(14,days×3)`（本檔已無缺欄）。  
4. **未改** story_detail／index；89–92 **未滾**。  
5. Soft≠PASS；全量出圖 HOLD。

## 下一步（tester）

1. 覆測短廣告／長電影主角／長劇男主／週末 MTV／寫真／逾期一次。  
2. 用戶 OK 後再滾 1989–92 A→B。  
3. ping eng／iOS：schema 已 LIVE 於 1988。

*完 — HANDOFF_GIGS_1988_SHOOT_CAREER_AB_v1*
