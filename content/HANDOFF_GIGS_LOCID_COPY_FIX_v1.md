# HANDOFF：gigs synopsis 清 raw locId → 顯示名 v1

**日期：** 2026-11-03（Asia/Hong_Kong）  
**觸發：** tester v18q 抽樣 — 1989–91 通告文案露出 `film_harbour`  
**範圍：** gigs_1989–1992 synopsis（順手清齊所有 fill 模板 raw locId）  
**Soft≠PASS**／全量出圖 HOLD

## 顯示名（對齊 PLAN_STORY_UI_BEAT_SCHEMA_v1 HTML LOCS）

| locId | 顯示名 |
|---|---|
| film_harbour | 維港電影 |
| film_cotton | 紅棉影業 |
| film_lion | 獅子山製片 |
| tvb_longmen | 星河電視台 |
| tvb_kowloon | 九龍電視台 |
| tvb_harbour | 海港廣播 |
| rec_hk | 香江唱片 |
| rec_wanchai | 灣仔唱片 |
| rec_star | 天星音樂 |
| ad_central | 中環廣告 |
| ad_adm | 金鐘創意 |

`loc` 欄保持 machine id，只改玩家可見 `synopsis`。

## 版本／SHA16

| 年 | ver | SHA16 | n |
|---|---|---|---|
| 1989 | **1.1.1** | `6a2da912643f9af7` | 52 |
| 1990 | **1.1.1** | `0676d4a0658025ac` | 53 |
| 1991 | **1.1.1** | `89dd5602a72f9520` | 52 |
| 1992 | **1.1.1** | `3109a3e6f864ac2f` | 51 |

1988 **2.3.0**／`c58ccfa828e8ecf5` 無此問題、未改。

## 樣例

- `gig_1989_film_11`：`1989年電影組在維港電影拍春場次。…`
- `gig_1989_rec_09`：`香江唱片安排春錄音。…`（清 `rec_hk`）

## 備份／鏡像

- Backup：`gigs_{year}_pre_locid_copy_fix_backup.json`
- 已鏡：`sv-phone-preview/content/`＋store `store-cbdfa415-…`（sha sync OK）

## 請 tester

抽樣 1989–92 通告卡：synopsis **唔見** raw locId；維港相關應見「維港電影」。

## 請 iOS

本地核對 SHA 後問用戶推。Soft≠PASS。
