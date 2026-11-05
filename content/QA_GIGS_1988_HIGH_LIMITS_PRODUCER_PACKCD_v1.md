> Soft≠PASS｜Pack CD D3A｜高階 limits／producer 抽樣 QA｜基準 Soft 3.2.5→寫庫 3.2.6｜經 qwen3.7-max｜唔 tip LIVE｜89–92 HOLD｜castWindow HOLD｜roles[] HOLD

# QA_GIGS_1988_HIGH_LIMITS_PRODUCER_PACKCD_v1

## 範圍
- 高階 n=46；審查 limits（原 43/46）與 producer（原 41/46）
- 模型：`qwen3.7-max` @ token-plan.ap-southeast-1（compatible-mode chat/completions）
- 拍板：D3A（抽樣 QA＋有問題 Soft patch）

## 摘要
| 項 | 數 |
|---|---|
| 審查 | 46 |
| qwen 標 issues | 16 |
| 實修 Soft patch | 12 |
| 跳過（純 minAge/maxAge schema nit） | 4 |
| 修後高階 limits | **46/46** |
| 修後高階 producer | **46/46** |

## 問題表
| id | field | severity | detail | Soft 處理 |
|---|---|---|---|---|
| `gig_1988_tv_07` | limits | missing | limits 欄位為 null，缺失所有限制條件 | 已 Soft patch |
| `gig_1988_tv_08` | limits | missing | limits 欄位為 null，缺失所有限制條件 | 已 Soft patch |
| `gig_1988_film_07` | limits | missing | limits 欄位為 null，缺失所有限制條件 | 已 Soft patch |
| `gig_1988_ad_adm_winter_high` | producer | missing | producer 欄位為 null，缺失製作人資訊 | 已 Soft patch |
| `gig_1988_film_harbour_high` | producer | missing | producer 欄位為 null，缺失製作人資訊 | 已 Soft patch |
| `gig_1988_rec_hk_winter_high` | producer | missing | producer 欄位為 null，缺失製作人資訊 | 已 Soft patch |
| `gig_1988_rec_wanchai_winter_high` | producer | missing | producer 欄位為 null，缺失製作人資訊 | 已 Soft patch |
| `gig_1988_tv_kowloon_winter_high` | producer | missing | producer 欄位為 null，缺失製作人資訊 | 已 Soft patch |
| `gig_1988_ad_07` | limits | other | limits 物件缺少 minAge 及 maxAge 欄位，不符合 schema 規範 | 跳過（schema nit：缺 minAge/maxAge 鍵；庫內多數省略，唔強制） |
| `gig_1988_film_05` | limits | other | limits 物件缺少 minAge 及 maxAge 欄位，不符合 schema 規範 | 跳過（schema nit：缺 minAge/maxAge 鍵；庫內多數省略，唔強制） |
| `gig_1988_film_harbour_summer_high` | limits | mismatch | notes 提及『須接受槍戰場面』，但 synopsis 為古裝武俠劇，時代背景矛盾。 | 已 Soft patch |
| `gig_1988_film_lion_summer_high` | limits | mismatch | notes 提及『須接受槍戰場面』，但 synopsis 為古裝武俠劇，時代背景矛盾。 | 已 Soft patch |
| `gig_1988_film_harbour_winter_high` | limits | mismatch | notes 提及『須接受槍戰場面』，但 synopsis 為賀歲喜劇，內容不符，疑為複製貼上錯誤。 | 已 Soft patch |
| `gig_1988_tvb_kowloon_autumn_high` | limits | mismatch | gender 設為 any，但 synopsis 明確要求飾演『舉牌女郎』，應限為 female。 | 已 Soft patch |
| `gig_1988_film_harbour_spring_high` | limits | other | limits 物件缺少 minAge 及 maxAge 欄位，未完全符合 schema 規範，建議補上 null。 | 跳過（schema nit：缺 minAge/maxAge 鍵；庫內多數省略，唔強制） |
| `gig_1988_rec_hk_spring_high` | limits | other | limits 物件缺少 minAge 及 maxAge 欄位，未完全符合 schema 規範，建議補上 null。 | 跳過（schema nit：缺 minAge/maxAge 鍵；庫內多數省略，唔強制） |

## 已修明細（12）
- `gig_1988_tv_07`（missing）：limits←{"gender": "male", "licenses": [], "groupOnly": false, "minAge": null, "maxAge": null, "notes": ["須接受高危拍攝場面及熬夜趕通告"]}
- `gig_1988_tv_08`（missing）：limits←{"gender": "any", "licenses": [], "groupOnly": false, "minAge": null, "maxAge": null, "notes": ["須接受高強度舞蹈排練及熬夜"]}
- `gig_1988_film_07`（missing）：limits←{"gender": "male", "licenses": [], "groupOnly": false, "minAge": null, "maxAge": null, "notes": ["須接受夜戲拍攝及情緒演繹"]}
- `gig_1988_ad_adm_winter_high`（missing）：producer←陳志強
- `gig_1988_film_harbour_high`（missing）：producer←黃國輝
- `gig_1988_rec_hk_winter_high`（missing）：producer←李淑儀
- `gig_1988_rec_wanchai_winter_high`（missing）：producer←張志偉
- `gig_1988_tv_kowloon_winter_high`（missing）：producer←劉志華
- `gig_1988_film_harbour_summer_high`（mismatch）：limits←{"gender": "male", "licenses": [], "groupOnly": false, "minAge": null, "maxAge": null, "notes": ["須接受高難度武打及吊威也場面"]}
- `gig_1988_film_lion_summer_high`（mismatch）：limits←{"gender": "male", "licenses": [], "groupOnly": false, "minAge": null, "maxAge": null, "notes": ["須接受高難度武打及吊威也場面"]}
- `gig_1988_film_harbour_winter_high`（mismatch）：limits←{"gender": "male", "licenses": [], "groupOnly": false, "minAge": null, "maxAge": null, "notes": ["須接受高難度動作排練", "須接受通宵綵排"]}
- `gig_1988_tvb_kowloon_autumn_high`（mismatch）：limits←{"gender": "female", "licenses": [], "groupOnly": false, "minAge": null, "maxAge": null, "notes": ["須接受高壓檔期安排"]}

## ok_ids（qwen 無問題）
`gig_1988_ad_adm_autumn_high`, `gig_1988_ad_adm_spring_high`, `gig_1988_ad_adm_summer_high`, `gig_1988_ad_central_autumn_high`, `gig_1988_ad_central_spring_high`, `gig_1988_ad_central_summer_high`, `gig_1988_film_06`, `gig_1988_film_cotton_autumn_high`, `gig_1988_film_cotton_spring_high`, `gig_1988_film_cotton_summer_high`, `gig_1988_film_lion_autumn_high`, `gig_1988_film_lion_spring_high`, `gig_1988_rec_04`, `gig_1988_rec_hk_autumn_high`, `gig_1988_rec_hk_summer_high`, `gig_1988_rec_star_autumn_high`, `gig_1988_rec_star_spring_high`, `gig_1988_rec_star_summer_high`, `gig_1988_rec_wanchai_autumn_high`, `gig_1988_rec_wanchai_spring_high`, `gig_1988_rec_wanchai_summer_high`, `gig_1988_tv_06`, `gig_1988_tvb_harbour_autumn_high`, `gig_1988_tvb_harbour_spring_high`, `gig_1988_tvb_harbour_summer_high`, `gig_1988_tvb_kowloon_spring_high`, `gig_1988_tvb_kowloon_summer_high`, `gig_1988_tvb_longmen_spring_high`, `gig_1988_tvb_longmen_summer_high`, `gig_1988_var_05`

## 硬閘
- Soft≠PASS｜唔 tip LIVE｜唔抬 ?v=｜出圖 HOLD｜89–92 HOLD
- 禁「Ho 哥」／真藝名；favor 仍 `agency_ho`

## 時間
2026-11-05（Asia/Hong_Kong）
