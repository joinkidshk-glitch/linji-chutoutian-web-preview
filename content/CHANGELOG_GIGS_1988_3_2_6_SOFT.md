> Soft≠PASS｜Pack CD 寫庫｜1988 only｜version **3.2.6-soft**｜SHA `4a45521b`｜對照 pre `3.2.5-soft` backup `0390b091`｜qwen3.7-max＋deepseek-chat｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜0 新槽 n=137｜castWindow HOLD｜roles[] HOLD

# CHANGELOG_GIGS_1988_3_2_6_SOFT

## 摘要
按統籌 **Pack CD 拍板＝選項 1 · PLAN 原文**（`PLAN_GIG_1988_PACK_CD_BOARD_v1` SHA `4c31b967`）：**D1B＋D2A＋D3A＋D4A**。

| 項 | 前（3.2.5-soft） | 後（3.2.6-soft） |
|---|---|---|
| n | 137 | **137**（0 新槽） |
| softStatus | ≠PASS | **≠PASS** |
| 高階 limits | 43／46 | **46／46** |
| 高階 producer | 41／46 | **46／46** |
| 中階偏薄（綜藝+電視劇+廣告）limits | 12／21 | **21／21** |
| 中階偏薄 producer | 15／21 | **21／21** |
| 全中階 limits／producer | 20／27／45 | **29／33／45** |
| genreLabel OOV | 0 | **0** |
| castWindow／roles[] | HOLD | **HOLD** |

## 改動範圍
### D3A 高階 QA Soft patch（12 則）
- 補缺 limits×3：`tv_07`／`tv_08`／`film_07`
- 補缺 producer×5：`ad_adm_winter_high`／`film_harbour_high`／`rec_hk_winter_high`／`rec_wanchai_winter_high`／`tv_kowloon_winter_high`
- 修 mismatch×4：武俠／賀歲誤用「槍戰」notes×3；`tvb_kowloon_autumn_high` gender any→female（舉牌女郎）
- schema nit（缺 minAge/maxAge 鍵）×4 **唔改**（與庫內慣例一致）
- 報告：`QA_GIGS_1988_HIGH_LIMITS_PRODUCER_PACKCD_v1.md`

### D1B densify（0 新槽；中階 type∈綜藝／電視劇／廣告 · 21 則）
- 玩家面：`synopsis`／`blurb`／`boardNote`／`discoverNote` 經 **DeepSeek**（香港書面語）
- 方向矩陣經 **qwen3.7-max**
- limits：缺補／notes 潤（21）
- producer：缺補 6（虛構港式名；唔撞同則 director）
- **未改**：loc／season／tier／type／genreLabel／req／pay*／breachFee／favorDelta／rumorKeys／isKeyGig／storyKeys／tagOnComplete／boardHookMode／stars／roleScale／director／workTitle／roleLabel／id

## 明確未改
- 唔加新 gig；唔 mid+8；唔做 1989–1992；唔 tip LIVE；唔 publish；出圖 HOLD；唔抬 ?v=
- castWindow HOLD；roles[] HOLD
- 玩家面禁「Ho 哥」（掃描 0）；favor target 仍 `agency_ho`×19

## 產物路徑
| 檔 | 路徑 | SHA8 |
|---|---|---|
| Soft JSON | `/workspace/star-volunteer-web/content/gigs_1988.json` | `4a45521b` |
| store mirror | `/cursor/stores/store-cbdfa415-74f6-4e12-8fbd-513ef31077be/gigs_1988.json` | `4a45521b` |
| pre backup | `.../gigs_1988_v3.2.5_soft_pre_packcd_backup.json`（content＋store） | `0390b091` |
| patch | `/workspace/tmp/pack_cd_326/PATCH_GIGS_1988_3_2_6_SOFT.json` | `079f801e` |
| QA | `content/QA_GIGS_1988_HIGH_LIMITS_PRODUCER_PACKCD_v1.md` | （見下） |
| CHANGELOG | `content/CHANGELOG_GIGS_1988_3_2_6_SOFT.md` | （見下） |

## 時間
2026-11-05（Asia/Hong_Kong）

## Soft≠PASS
本檔同 JSON 均 **Soft≠PASS**；交統籌／tester 抽樣後先可談 tip。
