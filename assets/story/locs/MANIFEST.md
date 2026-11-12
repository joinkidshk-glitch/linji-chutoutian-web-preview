# Story location environments — MANIFEST

> 2026-11-04（Asia/Hong_Kong）· 19w company locs  
> LOOKS master: `content/PLAN_CHAR_LOOKS_REF_v1.md`（SHA 48ea7aac… verified）  
> Pipeline: **cursor GenerateImage** → crop/cover **720×1280** JPG q≈85  
> Soft≠PASS。**唔 tip**。**1989–1992 資產 HOLD**。出圖 HOLD（本輪只掛已 Soft 過嘅檔）。

## Files

| artId / key | file | dims | notes |
|---|---|---|---|
| `bg_loc_tvb_longmen` | `bg_loc_tvb_longmen.jpg` | 720×1280 | **已 tip，本輪唔覆蓋** |
| `bg_c1_tea_restaurant` | `bg_c1_tea_restaurant.jpg` | 720×1280 | **已 tip，本輪唔覆蓋** |
| `bg_loc_cafe_cha` | `bg_loc_cafe_cha.jpg` | 720×1280 | **已 tip，本輪唔覆蓋** |
| `bg_loc_agency_ho` | `bg_loc_agency_ho.jpg` | 720×1280 | **已 tip，本輪唔覆蓋** |
| `bg_loc_tvb_kowloon` | `bg_loc_tvb_kowloon.jpg` | 720×1280 | 19w 合入。九龍電視台走廊 |
| `bg_loc_tvb_harbour` | `bg_loc_tvb_harbour.jpg` | 720×1280 | 19w 合入。海港廣播大堂走廊 |
| `bg_loc_film_lion` | `bg_loc_film_lion.jpg` | 720×1280 | 19w 合入。獅子山製片 |
| `bg_loc_film_cotton` | `bg_loc_film_cotton.jpg` | 720×1280 | 19w 合入。紅棉影業 |
| `bg_loc_film_harbour` | `bg_loc_film_harbour.jpg` | 720×1280 | 19w 合入。維港電影 |
| `bg_loc_ad_central` | `bg_loc_ad_central.jpg` | 720×1280 | 19w 合入。中環廣告 |
| `bg_loc_ad_adm` | `bg_loc_ad_adm.jpg` | 720×1280 | 19w 合入。金鐘創意 |
| `bg_loc_rec_hk` | `bg_loc_rec_hk.jpg` | 720×1280 | 19w 合入。香江唱片 |
| `bg_loc_rec_wanchai` | `bg_loc_rec_wanchai.jpg` | 720×1280 | 19w 合入。灣仔唱片。Soft OK |
| `bg_loc_rec_star` | `bg_loc_rec_star.jpg` | 720×1280 | 19w 合入。天星音樂 |
| `bg_loc_gift_shop` | `bg_loc_gift_shop.jpg` | 720×1280 | v20a118 補齊。廟街夜市禮品檔（藍白帆布頂＋燈泡串） |
| `bg_loc_hospital` | `bg_loc_hospital.jpg` | 720×1280 | v20a118 補齊。仁康醫院（混凝土主樓＋有蓋落客亭＋黃昏暖光） |

Preview（`?v=19w`）`spBgImageCandidates` 先 probe `assets/story/locs/{key}.jpg`。

`LOC_SHEET_BG` 掛齊有 `bg_loc_{locId}.jpg` 嘅 loc（含 `rec_wanchai`）。Query 仍 `?v=19w`。

Soft≠PASS。唔 tip LIVE。89–92 HOLD。

---

## v20a103 SCENE103 更新（2026-11-11）

14 張全部換成年代重製版（真實 1990 年代香港參照＋逐地點劇情 brief＋風格錨，同規格 720×1280）：上表 14 個檔名不變、內容全換。載入指向同步改：`LOC_SHEET_BG` 13 個 locId 全部改指本目錄檔案（唔再用 UI40 內嵌類別圖），`spBgImageCandidates` 檔案鏈行先、UI40 退做後備；兩處版本參數統一 `?v=20a103` 繞按路徑快取。審計＋brief＋參照留檔喺 DEV `~/workspace/linji-scene-redo/`（唔入 repo）。詳見根目錄 `NOTES_V20A103_SCENE103.md`。
