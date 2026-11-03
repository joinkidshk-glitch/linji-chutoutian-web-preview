# HANDOFF｜gigs_1989–1992 拍攝生涯 A→B v1

> 2026-11-03（Asia/Hong_Kong）｜對齊 `PLAN_SHOOT_CAREER_SCHEDULE_v2`
> **用戶拍板**（經 tester）：A 抬全則欄 → B 每年約 4–6 則補缺邊；另 **t327u** 硬要求：季節 hard-hide 後 11 loc×春夏秋冬 每格 ≥1，否則空板 FAIL。
> **1988 未改**（本輪不動；庫內現況另見他手 v2.3.0 loc 填縫）。
> **Soft≠PASS**；全量出圖 HOLD。唔當 Soft PASS。

## 總表

| 年 | version | SHA256₁₆ | n | career 新則 | loc 填縫 | 缺邊 photobook/mtv/film_lead/tv_lead | 空板 |
|---|---|---|---|---|---|---|---|
| 1989 | **1.1.0** | `11c983094fdd1f40` | **37 → 52** | 5 | 10 | 0 | ✅ 0 |
| 1990 | **1.1.0** | `fa1ac9aa1b24da2b` | **37 → 53** | 5 | 11 | 0 | ✅ 0 |
| 1991 | **1.1.0** | `63a1ad8cfa62b35d` | **37 → 52** | 5 | 10 | 0 | ✅ 0 |
| 1992 | **1.1.0** | `8965d60dd2ef06dd` | **30 → 51** | 4 | 17 | 0 | ✅ 0 |

## 檔案／鏡像

| 項 | 路徑 |
|---|---|
| LIVE | `/workspace/star-volunteer-web/content/gigs_{1989..1992}.json` |
| mirror preview | `/workspace/sv-phone-preview/content/gigs_{1989..1992}.json` |
| mirror store | `/cursor/stores/store-cbdfa415-74f6-4e12-8fbd-513ef31077be/gigs_{1989..1992}.json` |
| backup | `gigs_{year}_pre_shoot_career_ab_backup.json`（同 LIVE 目錄） |

---

## 1989

| 項 | 值 |
|---|---|
| version | **1.1.0**（前：1.0） |
| SHA256₁₆ | `11c983094fdd1f40` |
| n gigs | **37 → 52**（+15） |
| weekday-only `[1..5]` | **24** ≥8 ✅ |
| weekend-only `[6,7]` | **5** ≥5 ✅ |

### A｜抬欄

每則補／對齊：`roleScale`／`shootBand`／抬 `shootDaysHint` 入帶／`shootWeekdays`／`shootDeadlineDays=max(ceil(days×7/|wd|)+2, days+3)`。

抽樣（既有則 before→after）：

| id | type/tier | roleScale | band | days | weekdays | deadline | title |
|---|---|---|---|---|---|---|---|
| `gig_1989_ad_01` | 廣告/初 | `ad_av` | [3, 4] | 2→**3** | `[6, 7]` | **13** | 「暖巢」慈善機構形象短片 |
| `gig_1989_film_01` | 電影/初 | `film_support_small` | [12, 15] | 2→**13** | `[1, 2, 3, 4, 5, 6]` | **18** | 《靜巷》文藝短場：送傘的路人 |
| `gig_1989_tv_01` | 電視劇/初 | `tv_cameo_short` | [8, 10] | 3→**9** | `[1, 2, 3, 4, 5, 6]` | **13** | 《街燈下》公益單元：夜班清潔工阿強 |

### B｜career 新則（5）

| id | type | tier | roleScale | loc | season | days | weekdays | deadline | title |
|---|---|---|---|---|---|---|---|---|---|
| `gig_1989_photo_01` | 廣告 | 初 | `photobook` | `ad_adm` | 夏 | 6 | `[5, 6, 7]` | 16 | 「燈下映像」初夏寫真集《雨遮與街燈》 |
| `gig_1989_photo_02` | 廣告 | 中 | `photobook` | `ad_central` | 冬 | 6 | `[1, 2, 3, 4, 5]` | 11 | 「香江鏡框」冬日寫真集《大衣與碼頭》 |
| `gig_1989_mtv_01` | 唱片通告 | 初 | `mtv` | `rec_star` | 春 | 3 | `[6, 7]` | 13 | 樂隊「夜渡」快歌 MTV 男主角 |
| `gig_1989_film_09` | 電影 | 高 | `film_lead_big` | `film_lion` | 秋 | 29 | `[1, 2, 3, 4, 5, 6]` | 36 | 《離岸的信》歸僑青年阿信 |
| `gig_1989_tv_10` | 電視劇 | 高 | `tv_lead_long` | `tvb_harbour` | 秋 | 22 | `[1, 2, 3, 4, 5, 6]` | 28 | 《渡輪燈火》渡輪水手阿海 |

### loc×季節 空板（抬欄後／填縫前）→ 填縫（10）

初始缺口 **15**：`tvb_harbour/秋`, `film_lion/秋`, `film_cotton/秋`, `film_harbour/春`, `film_harbour/秋`, `rec_hk/春`, `rec_hk/夏`, `rec_hk/冬`, `rec_wanchai/春`, `rec_wanchai/冬`, `rec_star/春`, `rec_star/冬`, `ad_central/冬`, `ad_adm/夏`, `ad_adm/冬`

career 優先佔位（含 tvb_harbour 秋／春）：其餘每缺口一則填縫。

| id | loc | season | type | roleScale | days | title |
|---|---|---|---|---|---|---|
| `gig_1989_film_10` | `film_cotton` | 秋 | 電影 | `film_support_small` | 13 | 《棉廠秋單》過場：送布疋青年 |
| `gig_1989_film_11` | `film_harbour` | 春 | 電影 | `film_support_small` | 13 | 《海港春潮》過場：碼頭腳夫 |
| `gig_1989_film_12` | `film_harbour` | 秋 | 電影 | `film_support_small` | 13 | 《海港秋航》過場：送船親友 |
| `gig_1989_rec_09` | `rec_hk` | 春 | 唱片通告 | `rec_album` | 12 | 春日合唱單曲《開閘》和音 |
| `gig_1989_rec_10` | `rec_hk` | 夏 | 唱片通告 | `rec_album` | 12 | 夏日專輯《熱浪》和音錄音 |
| `gig_1989_rec_11` | `rec_hk` | 冬 | 唱片通告 | `rec_album` | 12 | 冬日賀歲歌《開年》合唱 |
| `gig_1989_rec_12` | `rec_wanchai` | 春 | 唱片通告 | `rec_album` | 12 | 灣仔室：春日口白試音 |
| `gig_1989_rec_13` | `rec_wanchai` | 冬 | 唱片通告 | `rec_album` | 12 | 灣仔室：歲晚合唱收聲 |
| `gig_1989_rec_14` | `rec_star` | 冬 | 唱片通告 | `rec_album` | 12 | 星廠冬：賀歲歌收束合唱 |
| `gig_1989_ad_06` | `ad_adm` | 冬 | 廣告 | `ad_print` | 3 | 「金鐘冬封」賀歲平面 |

最終空板：**0 ✅**

### roleScale 直方圖

| roleScale | n |
|---|---|
| `ad_av` | 4 |
| `ad_print` | 2 |
| `film_lead_big` | 1 |
| `film_support_main` | 4 |
| `film_support_small` | 7 |
| `mtv` | 1 |
| `photobook` | 2 |
| `rec_album` | 14 |
| `tv_cameo_short` | 7 |
| `tv_lead_long` | 1 |
| `tv_support_main` | 2 |
| `variety_ep` | 7 |

### type counts

| type | n |
|---|---|
| 電視劇 | 10 |
| 廣告 | 8 |
| 電影 | 12 |
| 綜藝 | 7 |
| 唱片通告 | 15 |
| **total** | **52** |

### 星期多樣性 ids

- weekday-only：`['gig_1989_rec_02', 'gig_1989_ad_03', 'gig_1989_rec_03', 'gig_1989_rec_04', 'gig_1989_rec_05', 'gig_1989_rec_06', 'gig_1989_rec_07', 'gig_1989_var_02', 'gig_1989_var_03', 'gig_1989_ad_04', 'gig_1989_ad_05', 'gig_1989_var_04', 'gig_1989_var_05', 'gig_1989_var_06', 'gig_1989_var_07', 'gig_1989_rec_08', 'gig_1989_photo_02', 'gig_1989_rec_09', 'gig_1989_rec_10', 'gig_1989_rec_11', 'gig_1989_rec_12', 'gig_1989_rec_13', 'gig_1989_rec_14', 'gig_1989_ad_06']`
- weekend-only：`['gig_1989_ad_01', 'gig_1989_ad_02', 'gig_1989_var_01', 'gig_1989_rec_01', 'gig_1989_mtv_01']`

---

## 1990

| 項 | 值 |
|---|---|
| version | **1.1.0**（前：1.0） |
| SHA256₁₆ | `fa1ac9aa1b24da2b` |
| n gigs | **37 → 53**（+16） |
| weekday-only `[1..5]` | **23** ≥8 ✅ |
| weekend-only `[6,7]` | **5** ≥5 ✅ |

### A｜抬欄

每則補／對齊：`roleScale`／`shootBand`／抬 `shootDaysHint` 入帶／`shootWeekdays`／`shootDeadlineDays=max(ceil(days×7/|wd|)+2, days+3)`。

抽樣（既有則 before→after）：

| id | type/tier | roleScale | band | days | weekdays | deadline | title |
|---|---|---|---|---|---|---|---|
| `gig_1990_ad_01` | 廣告/中 | `ad_av` | [3, 4] | 1→**3** | `[6, 7]` | **13** | 「金時鐘」手錶商場快閃廣告 |
| `gig_1990_film_01` | 電影/初 | `film_support_small` | [12, 15] | 2→**13** | `[1, 2, 3, 4, 5, 6]` | **18** | 《櫥窗》過場：櫥窗換裝模特 |
| `gig_1990_tv_01` | 電視劇/中 | `tv_support_main` | [14, 16] | 3→**15** | `[1, 2, 3, 4, 5, 6]` | **20** | 《商場風雲》單元：假日促銷店員 |

### B｜career 新則（5）

| id | type | tier | roleScale | loc | season | days | weekdays | deadline | title |
|---|---|---|---|---|---|---|---|---|---|
| `gig_1990_photo_01` | 廣告 | 初 | `photobook` | `ad_adm` | 夏 | 6 | `[5, 6, 7]` | 16 | 「鏡海」夏日寫真集《商場中庭的風》 |
| `gig_1990_photo_02` | 廣告 | 中 | `photobook` | `ad_adm` | 秋 | 6 | `[1, 2, 3, 4, 5]` | 11 | 「金廊映像」秋日寫真集《櫥窗少年》 |
| `gig_1990_mtv_01` | 唱片通告 | 初 | `mtv` | `rec_star` | 春 | 3 | `[6, 7]` | 13 | 新晉歌手「南風」主打 MTV 男主角 |
| `gig_1990_film_10` | 電影 | 高 | `film_lead_big` | `film_harbour` | 秋 | 29 | `[1, 2, 3, 4, 5, 6]` | 36 | 《鐵橋風雲》熱血拳手阿龍 |
| `gig_1990_tv_09` | 電視劇 | 高 | `tv_lead_long` | `tvb_harbour` | 秋 | 22 | `[1, 2, 3, 4, 5, 6]` | 28 | 《商場歲月》百貨少掌櫃阿邦 |

### loc×季節 空板（抬欄後／填縫前）→ 填縫（11）

初始缺口 **14**：`tvb_kowloon/秋`, `film_lion/冬`, `film_cotton/春`, `film_harbour/春`, `film_harbour/秋`, `film_harbour/冬`, `rec_hk/春`, `rec_hk/夏`, `rec_wanchai/春`, `rec_wanchai/夏`, `rec_wanchai/冬`, `rec_star/春`, `rec_star/冬`, `ad_adm/秋`

career 優先佔位（含 tvb_harbour 秋／春）：其餘每缺口一則填縫。

| id | loc | season | type | roleScale | days | title |
|---|---|---|---|---|---|---|
| `gig_1990_tv_10` | `tvb_kowloon` | 秋 | 電視劇 | `tv_cameo_short` | 9 | 《九龍秋雨》單元：撐傘路人 |
| `gig_1990_film_11` | `film_lion` | 冬 | 電影 | `film_support_small` | 13 | 《獅山歲晚》群戲：殺青宴後排 |
| `gig_1990_film_12` | `film_cotton` | 春 | 電影 | `film_support_small` | 13 | 《棉廠春班》群戲：車間學徒 |
| `gig_1990_film_13` | `film_harbour` | 春 | 電影 | `film_support_small` | 13 | 《海港春潮》過場：碼頭腳夫 |
| `gig_1990_film_14` | `film_harbour` | 冬 | 電影 | `film_support_small` | 13 | 《海港冬霧》群戲：落雪（人造）街景 |
| `gig_1990_rec_06` | `rec_hk` | 春 | 唱片通告 | `rec_album` | 12 | 春日合唱單曲《開閘》和音 |
| `gig_1990_rec_07` | `rec_hk` | 夏 | 唱片通告 | `rec_album` | 12 | 夏日專輯《熱浪》和音錄音 |
| `gig_1990_rec_08` | `rec_wanchai` | 春 | 唱片通告 | `rec_album` | 12 | 灣仔室：春日口白試音 |
| `gig_1990_rec_09` | `rec_wanchai` | 夏 | 唱片通告 | `rec_album` | 12 | 灣仔室：夏日快歌和音 |
| `gig_1990_rec_10` | `rec_wanchai` | 冬 | 唱片通告 | `rec_album` | 12 | 灣仔室：歲晚合唱收聲 |
| `gig_1990_rec_11` | `rec_star` | 冬 | 唱片通告 | `rec_album` | 12 | 星廠冬：賀歲歌收束合唱 |

最終空板：**0 ✅**

### roleScale 直方圖

| roleScale | n |
|---|---|
| `ad_av` | 6 |
| `ad_print` | 3 |
| `film_lead_big` | 1 |
| `film_support_main` | 6 |
| `film_support_small` | 7 |
| `mtv` | 1 |
| `photobook` | 2 |
| `rec_album` | 11 |
| `tv_cameo_short` | 6 |
| `tv_lead_long` | 1 |
| `tv_support_main` | 3 |
| `variety_ep` | 6 |

### type counts

| type | n |
|---|---|
| 廣告 | 11 |
| 綜藝 | 6 |
| 電視劇 | 10 |
| 電影 | 14 |
| 唱片通告 | 12 |
| **total** | **53** |

### 星期多樣性 ids

- weekday-only：`['gig_1990_var_01', 'gig_1990_var_02', 'gig_1990_ad_05', 'gig_1990_ad_06', 'gig_1990_rec_01', 'gig_1990_rec_02', 'gig_1990_rec_03', 'gig_1990_rec_04', 'gig_1990_ad_07', 'gig_1990_var_03', 'gig_1990_var_04', 'gig_1990_var_05', 'gig_1990_var_06', 'gig_1990_ad_08', 'gig_1990_ad_09', 'gig_1990_rec_05', 'gig_1990_photo_02', 'gig_1990_rec_06', 'gig_1990_rec_07', 'gig_1990_rec_08', 'gig_1990_rec_09', 'gig_1990_rec_10', 'gig_1990_rec_11']`
- weekend-only：`['gig_1990_ad_01', 'gig_1990_ad_02', 'gig_1990_ad_03', 'gig_1990_ad_04', 'gig_1990_mtv_01']`

---

## 1991

| 項 | 值 |
|---|---|
| version | **1.1.0**（前：1.0） |
| SHA256₁₆ | `63a1ad8cfa62b35d` |
| n gigs | **37 → 52**（+15） |
| weekday-only `[1..5]` | **24** ≥8 ✅ |
| weekend-only `[6,7]` | **5** ≥5 ✅ |

### A｜抬欄

每則補／對齊：`roleScale`／`shootBand`／抬 `shootDaysHint` 入帶／`shootWeekdays`／`shootDeadlineDays=max(ceil(days×7/|wd|)+2, days+3)`。

抽樣（既有則 before→after）：

| id | type/tier | roleScale | band | days | weekdays | deadline | title |
|---|---|---|---|---|---|---|---|
| `gig_1991_ad_01` | 廣告/中 | `ad_av` | [3, 4] | 1→**3** | `[6, 7]` | **13** | 「歸心電話」長途電話卡溫情廣告 |
| `gig_1991_film_01` | 電影/中 | `film_support_main` | [20, 24] | 3→**22** | `[1, 2, 3, 4, 5, 6]` | **28** | 《宴會廳》豪門聯姻：遠房表弟跑龍套 |
| `gig_1991_tv_01` | 電視劇/中 | `tv_support_main` | [14, 16] | 3→**15** | `[1, 2, 3, 4, 5, 6]` | **20** | 《家事簿》單元：拒聯姻的表態練習 |

### B｜career 新則（5）

| id | type | tier | roleScale | loc | season | days | weekdays | deadline | title |
|---|---|---|---|---|---|---|---|---|---|
| `gig_1991_photo_01` | 廣告 | 初 | `photobook` | `ad_adm` | 夏 | 6 | `[5, 6, 7]` | 16 | 「家書影室」寫真集《門閘內外》 |
| `gig_1991_photo_02` | 廣告 | 中 | `photobook` | `ad_central` | 冬 | 6 | `[1, 2, 3, 4, 5]` | 11 | 「渡海影集」寫真集《兩岸同款外套》 |
| `gig_1991_mtv_01` | 唱片通告 | 初 | `mtv` | `rec_wanchai` | 春 | 3 | `[6, 7]` | 13 | 打歌快歌《門閘外》MTV 男主角 |
| `gig_1991_film_10` | 電影 | 高 | `film_lead_big` | `film_lion` | 秋 | 29 | `[1, 2, 3, 4, 5, 6]` | 36 | 《門閘之內》拒聯姻的長子阿傑 |
| `gig_1991_tv_07` | 電視劇 | 高 | `tv_lead_long` | `tvb_harbour` | 秋 | 22 | `[1, 2, 3, 4, 5, 6]` | 28 | 《家事簿》拒聯姻長子阿傑 |

### loc×季節 空板（抬欄後／填縫前）→ 填縫（10）

初始缺口 **15**：`tvb_harbour/秋`, `film_lion/秋`, `film_cotton/秋`, `film_harbour/春`, `film_harbour/夏`, `film_harbour/秋`, `rec_hk/春`, `rec_hk/夏`, `rec_hk/冬`, `rec_wanchai/春`, `rec_wanchai/夏`, `rec_star/夏`, `ad_central/冬`, `ad_adm/夏`, `ad_adm/冬`

career 優先佔位（含 tvb_harbour 秋／春）：其餘每缺口一則填縫。

| id | loc | season | type | roleScale | days | title |
|---|---|---|---|---|---|---|
| `gig_1991_film_11` | `film_cotton` | 秋 | 電影 | `film_support_small` | 13 | 《棉廠秋單》過場：送布疋青年 |
| `gig_1991_film_12` | `film_harbour` | 春 | 電影 | `film_support_small` | 13 | 《海港春潮》過場：碼頭腳夫 |
| `gig_1991_film_13` | `film_harbour` | 夏 | 電影 | `film_support_small` | 13 | 《海港夏雷》群戲：避雨路人 |
| `gig_1991_film_14` | `film_harbour` | 秋 | 電影 | `film_support_small` | 13 | 《海港秋航》過場：送船親友 |
| `gig_1991_rec_09` | `rec_hk` | 春 | 唱片通告 | `rec_album` | 12 | 春日合唱單曲《開閘》和音 |
| `gig_1991_rec_10` | `rec_hk` | 夏 | 唱片通告 | `rec_album` | 12 | 夏日專輯《熱浪》和音錄音 |
| `gig_1991_rec_11` | `rec_hk` | 冬 | 唱片通告 | `rec_album` | 12 | 冬日賀歲歌《開年》合唱 |
| `gig_1991_rec_12` | `rec_wanchai` | 夏 | 唱片通告 | `rec_album` | 12 | 灣仔室：夏日快歌和音 |
| `gig_1991_rec_13` | `rec_star` | 夏 | 唱片通告 | `rec_album` | 12 | 星廠夏：卡帶內頁棚拍 |
| `gig_1991_ad_06` | `ad_adm` | 冬 | 廣告 | `ad_print` | 3 | 「金鐘冬封」賀歲平面 |

最終空板：**0 ✅**

### roleScale 直方圖

| roleScale | n |
|---|---|
| `ad_av` | 3 |
| `ad_print` | 3 |
| `film_lead_big` | 1 |
| `film_support_main` | 8 |
| `film_support_small` | 5 |
| `mtv` | 1 |
| `photobook` | 2 |
| `rec_album` | 13 |
| `tv_cameo_short` | 5 |
| `tv_lead_long` | 1 |
| `tv_support_main` | 1 |
| `variety_ep` | 8 |
| `variety_special` | 1 |

### type counts

| type | n |
|---|---|
| 電影 | 14 |
| 電視劇 | 7 |
| 廣告 | 8 |
| 唱片通告 | 14 |
| 綜藝 | 9 |
| **total** | **52** |

### 星期多樣性 ids

- weekday-only：`['gig_1991_var_03', 'gig_1991_var_04', 'gig_1991_var_05', 'gig_1991_ad_03', 'gig_1991_rec_02', 'gig_1991_rec_03', 'gig_1991_rec_04', 'gig_1991_rec_05', 'gig_1991_rec_06', 'gig_1991_var_06', 'gig_1991_var_07', 'gig_1991_ad_04', 'gig_1991_ad_05', 'gig_1991_var_08', 'gig_1991_var_09', 'gig_1991_rec_07', 'gig_1991_rec_08', 'gig_1991_photo_02', 'gig_1991_rec_09', 'gig_1991_rec_10', 'gig_1991_rec_11', 'gig_1991_rec_12', 'gig_1991_rec_13', 'gig_1991_ad_06']`
- weekend-only：`['gig_1991_ad_01', 'gig_1991_ad_02', 'gig_1991_rec_01', 'gig_1991_var_02', 'gig_1991_mtv_01']`

---

## 1992

| 項 | 值 |
|---|---|
| version | **1.1.0**（前：1.0） |
| SHA256₁₆ | `8965d60dd2ef06dd` |
| n gigs | **30 → 51**（+21） |
| weekday-only `[1..5]` | **22** ≥8 ✅ |
| weekend-only `[6,7]` | **5** ≥5 ✅ |

### A｜抬欄

每則補／對齊：`roleScale`／`shootBand`／抬 `shootDaysHint` 入帶／`shootWeekdays`／`shootDeadlineDays=max(ceil(days×7/|wd|)+2, days+3)`。

抽樣（既有則 before→after）：

| id | type/tier | roleScale | band | days | weekdays | deadline | title |
|---|---|---|---|---|---|---|---|
| `gig_1992_ad_01` | 廣告/中 | `ad_av` | [3, 4] | 1→**3** | `[1, 2, 3, 4, 5]` | **7** | 「晨光菲林」回望式廣告：沖曬店一場 |
| `gig_1992_film_01` | 電影/高 | `film_lead_big` | [28, 30] | 2→**29** | `[1, 2, 3, 4, 5, 6]` | **36** | 《劇本堆》晨光選角：三個角色試一段 |
| `gig_1992_tv_01` | 電視劇/中 | `tv_support_main` | [14, 16] | 3→**15** | `[1, 2, 3, 4, 5, 6]` | **20** | 《選擇題》單元：拒與接的兩場戲 |

### B｜career 新則（4）

| id | type | tier | roleScale | loc | season | days | weekdays | deadline | title |
|---|---|---|---|---|---|---|---|---|---|
| `gig_1992_photo_01` | 廣告 | 初 | `photobook` | `ad_central` | 冬 | 6 | `[5, 6, 7]` | 16 | 「晨光冊頁」寫真集《舊底片上的臉》 |
| `gig_1992_photo_02` | 廣告 | 中 | `photobook` | `ad_central` | 春 | 6 | `[1, 2, 3, 4, 5]` | 11 | 「收束冊」寫真集《燈滅前一頁》 |
| `gig_1992_mtv_01` | 唱片通告 | 初 | `mtv` | `rec_hk` | 夏 | 3 | `[6, 7]` | 13 | 回望輯快歌《舊路燈》MTV 男主角 |
| `gig_1992_tv_06` | 電視劇 | 高 | `tv_lead_long` | `tvb_harbour` | 秋 | 22 | `[1, 2, 3, 4, 5, 6]` | 28 | 《選擇題》青年演員阿偉自傳式長線 |

### loc×季節 空板（抬欄後／填縫前）→ 填縫（17）

初始缺口 **21**：`tvb_longmen/秋`, `tvb_longmen/冬`, `tvb_kowloon/冬`, `tvb_harbour/秋`, `film_lion/冬`, `film_cotton/秋`, `film_harbour/秋`, `film_harbour/冬`, `rec_hk/夏`, `rec_hk/秋`, `rec_hk/冬`, `rec_wanchai/夏`, `rec_wanchai/冬`, `rec_star/夏`, `rec_star/秋`, `rec_star/冬`, `ad_central/春`, `ad_central/秋`, `ad_central/冬`, `ad_adm/春`, `ad_adm/秋`

career 優先佔位（含 tvb_harbour 秋／春）：其餘每缺口一則填縫。

| id | loc | season | type | roleScale | days | title |
|---|---|---|---|---|---|---|
| `gig_1992_var_06` | `tvb_longmen` | 秋 | 綜藝 | `variety_ep` | 3 | 《龍門秋訊》廠內短訪 |
| `gig_1992_tv_07` | `tvb_longmen` | 冬 | 電視劇 | `tv_cameo_short` | 9 | 《龍門歲晚》單元：搶通告臨記 |
| `gig_1992_var_07` | `tvb_kowloon` | 冬 | 綜藝 | `variety_ep` | 3 | 《九龍倒數》前哨對手 |
| `gig_1992_film_13` | `film_lion` | 冬 | 電影 | `film_support_small` | 13 | 《獅山歲晚》群戲：殺青宴後排 |
| `gig_1992_film_14` | `film_cotton` | 秋 | 電影 | `film_support_small` | 13 | 《棉廠秋單》過場：送布疋青年 |
| `gig_1992_film_15` | `film_harbour` | 秋 | 電影 | `film_support_small` | 13 | 《海港秋航》過場：送船親友 |
| `gig_1992_film_16` | `film_harbour` | 冬 | 電影 | `film_support_small` | 13 | 《海港冬霧》群戲：落雪（人造）街景 |
| `gig_1992_rec_05` | `rec_hk` | 秋 | 唱片通告 | `rec_album` | 12 | 秋日單曲《落葉郵筒》和音 |
| `gig_1992_rec_06` | `rec_hk` | 冬 | 唱片通告 | `rec_album` | 12 | 冬日賀歲歌《開年》合唱 |
| `gig_1992_rec_07` | `rec_wanchai` | 夏 | 唱片通告 | `rec_album` | 12 | 灣仔室：夏日快歌和音 |
| `gig_1992_rec_08` | `rec_wanchai` | 冬 | 唱片通告 | `rec_album` | 12 | 灣仔室：歲晚合唱收聲 |
| `gig_1992_rec_09` | `rec_star` | 夏 | 唱片通告 | `rec_album` | 12 | 星廠夏：卡帶內頁棚拍 |
| `gig_1992_rec_10` | `rec_star` | 秋 | 唱片通告 | `rec_album` | 12 | 星廠秋：打歌期和音加錄 |
| `gig_1992_rec_11` | `rec_star` | 冬 | 唱片通告 | `rec_album` | 12 | 星廠冬：賀歲歌收束合唱 |
| `gig_1992_ad_05` | `ad_central` | 秋 | 廣告 | `ad_av` | 3 | 「中環秋裝」服裝十五秒 |
| `gig_1992_ad_06` | `ad_adm` | 春 | 廣告 | `ad_print` | 3 | 「金鐘春訊」機構形象平面 |
| `gig_1992_ad_07` | `ad_adm` | 秋 | 廣告 | `ad_av` | 3 | 「金鐘秋訊」服務短片 |

最終空板：**0 ✅**

### roleScale 直方圖

| roleScale | n |
|---|---|
| `ad_av` | 4 |
| `ad_print` | 3 |
| `film_lead_big` | 2 |
| `film_support_main` | 4 |
| `film_support_small` | 10 |
| `mtv` | 1 |
| `photobook` | 2 |
| `rec_album` | 11 |
| `tv_cameo_short` | 4 |
| `tv_lead_long` | 1 |
| `tv_support_main` | 2 |
| `variety_ep` | 7 |

### type counts

| type | n |
|---|---|
| 電影 | 16 |
| 電視劇 | 7 |
| 唱片通告 | 12 |
| 綜藝 | 7 |
| 廣告 | 9 |
| **total** | **51** |

### 星期多樣性 ids

- weekday-only：`['gig_1992_rec_03', 'gig_1992_var_01', 'gig_1992_var_02', 'gig_1992_var_03', 'gig_1992_var_04', 'gig_1992_ad_01', 'gig_1992_ad_02', 'gig_1992_ad_03', 'gig_1992_var_05', 'gig_1992_rec_04', 'gig_1992_ad_04', 'gig_1992_photo_02', 'gig_1992_var_07', 'gig_1992_rec_05', 'gig_1992_rec_06', 'gig_1992_rec_07', 'gig_1992_rec_08', 'gig_1992_rec_09', 'gig_1992_rec_10', 'gig_1992_rec_11', 'gig_1992_ad_05', 'gig_1992_ad_06']`
- weekend-only：`['gig_1992_rec_01', 'gig_1992_rec_02', 'gig_1992_mtv_01', 'gig_1992_var_06', 'gig_1992_ad_07']`

---

## 引擎／iOS 注意

1. 跟 `roleScale`／`shootBand`，**唔再**跟 tier 日數下限（v1 廢止）。
2. 手帳：只許 `shootWeekdays`；排滿 `shootDaysHint`；逾 `shootDeadlineDays` → PLAN §3 罰則一次。
3. 缺欄 fallback 仍：平日 + `max(14,days×3)`（本四檔已無缺欄）。
4. **季節 hard-hide 後**：11 loc × 4 季每格 ≥1（本四檔已填滿）；空板＝FAIL。
5. Soft≠PASS；全量出圖 HOLD。
6. 1988 本輪**未改**。

## 下一步（tester）

1. 覆測：短廣告／寫真／MTV 週末／長電影男主／長劇男主／逾期一次。
2. 覆測：每季 hard-hide 後 11 loc 通告板非空（尤 tvb_harbour 春／秋）。
3. ping eng／iOS：89–92 schema 已 LIVE。

*完 — HANDOFF_GIGS_1989_1992_SHOOT_CAREER_AB_v1*
