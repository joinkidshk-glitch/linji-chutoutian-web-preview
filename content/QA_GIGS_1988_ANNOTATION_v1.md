# QA_GIGS_1988_ANNOTATION_v1

> 《臨記出頭天》§2A 1988 通告標註文件 QA｜對照 `gigs_1988.json` v2、`gigs_1988_pre_annotation_backup.json`、`GIGS_1988_ANNOTATION_v1.md`、`PLOT_MASTER_PLAN_v1.4-DS.md` §2A.0／§2A.1／§2A.6、`PLOT_DETAIL_UNLOCK_v1.md`（1988 只加標註）
>
> QA 時間：2026-11-02（Asia/Hong_Kong）｜**不改正文**

## Overall

**PASS with nits**

- 標註可作 Phase1 wiring 草案（`boardPriority`／`eraTag`／`seasonWeight`／`boardNote`／`discoverNote` 齊）。
- **出圖仍暫緩**（本包無 art 交付；與既有暫緩一致）。
- 鐵律（synopsis／title／blurb／pay／fame／req 對 backup 深比）**30/30 不變 → PASS**。

---

## 1. 鐵律（HARD）

| 檢查 | 結果 |
|---|---|
| id 集合與 backup 一致（30） | PASS |
| `synopsis` 深比（含 SHA 抽樣） | PASS 30/30 |
| `title`／`blurb`／`pay`／`fame`／`req` 深比 | PASS 30/30 |
| 其他結算／結構正文（`loc`／`hard`／`popularity`／`tier`／`type`／`year`／`season`／shoot*／`roleHint`／`stressDeltaHint`／`heroAngle`／`diasporaHook`） | PASS（對 backup 無改） |

註：annotated 相對 backup **只新增**每則 `boardPriority`／`boardNote`／`seasonWeight`；`eraTag`／`discoverNote` 在 backup 已存在，本版改為 §2A.6 詞表單字串＋≤30 字氛圍句（屬標註合規化，**不屬**鐵律保護欄）。

Top-level：`version` 1→2；`edits` 追加 §2A 標註一行；`year`／`source`／`counts` 不變。

---

## 2. 必填標註欄

| 欄位 | 30/30 有值 | 備註 |
|---|---|---|
| `boardPriority` | PASS | 分布 high 14／normal 11／low 5 |
| `boardNote` | PASS | 見字數 |
| `eraTag` | PASS | 單一 `string`（非 array） |
| `discoverNote` | PASS | 見字數 |
| `seasonWeight` | PASS | 見推導對齊 |

---

## 3. eraTag ∈ §2A.6（1988）

詞表（主／次）：

| 季 | 主（high 須落此） | 次 |
|---|---|---|
| 春 | `era_1988_spring_grassroot`、`era_1988_spring_factory` | `era_1988_spring_alley` |
| 夏 | `era_1988_summer_variety`、`era_1988_summer_karaoke` | `era_1988_summer_mall` |
| 秋 | `era_1988_autumn_unitdrama`、`era_1988_autumn_readthrough` | `era_1988_autumn_studio` |
| 冬 | `era_1988_winter_festive`、`era_1988_winter_recruit` | `era_1988_winter_record` |

| 檢查 | 結果 |
|---|---|
| 每則 eraTag 為單一 string | PASS |
| 皆 ∈ 1988 該季主∪次詞表 | PASS（0 越界／0 跨季錯掛） |
| 與交付表 `GIGS_1988_ANNOTATION_v1.md` 分布一致 | PASS |

主／次計數（全庫）：春 主4／次3；夏 主4／次5；秋 主2／次4；冬 主5／次3。

---

## 4. high 計數與主詞對齊

| 季 | high 數 | 目標（交付／本 QA） | high 之 eraTag ∈ 當季**主**集合 |
|---|---|---|---|
| 春 | 4 | ≥4（交付 4） | PASS |
| 夏 | 4 | ≥4（交付 4） | PASS |
| 秋 | 2 | ≥2（交付 2） | PASS |
| 冬 | 4 | ≥3（交付 4） | PASS |

high 清單（抽核）：

- 春：`tv_01` grassroot、`tv_02` factory、`film_01` factory、`var_01` grassroot
- 夏：`var_02`／`var_03`／`ad_04` variety、`rec_02` karaoke
- 秋：`tv_05` unitdrama、`film_04` readthrough
- 冬：`var_05`／`tv_07`／`film_06` festive、`tv_06` recruit

**0 則 high 落在次詞。**

---

## 5. seasonWeight 與 eraTag

MASTER：當季主=1.0、次=0.6、非當季=0.3（可由 eraTag 推導）。

| 檢查 | 結果 |
|---|---|
| 30/30 與「該則 season＋eraTag」推導值一致 | PASS |
| 無手填偏離（無 ±0.1 微調殘留） | PASS |

例：`film_05`＝`era_1988_winter_recruit`（主）＋`boardPriority=normal`＋`seasonWeight=1.0` → 權重對、優先級可低於 high（合規）。

---

## 6. 字數（MASTER）

| 欄位 | 上限 | 最長實測 | 結果 |
|---|---|---|---|
| `boardNote` | ≤20 字 | 9 | PASS |
| `discoverNote` | ≤30 字 | 13 | PASS |

（按 Unicode codepoint＝中文「字」計。）

---

## 7. Soft／nits（不擋 PASS）

1. **週覆蓋未驗：** MASTER／§2A.1「首 12 週每週 ≥2 則 high」屬 playtest／上板模擬層；本交付只宣稱季合計 high，**本 QA 未跑週曆模擬**——標為 soft defer，wiring 後 playtest 再驗。
2. **`var_01` boardNote 季節口吻：** 春檔 high，note「賀歲直播緊急招募」——eraTag=`spring_grassroot` 合主詞，但「賀歲」語感偏冬；建議 detail 微調用字（例如「開年／直播緊急招募」），**非硬傷**。
3. **eraTag／discoverNote 相對 backup 全面置換：** backup 為自由 tag **array**＋較長 discoverNote；v2 改詞表 id＋縮句。符合 §2A「詞表化＋discoverNote 氛圍短句」；UNLOCK「只加 eraTag／boardPriority／seasonWeight」與 MASTER 亦要求 `boardNote`／`discoverNote`——本包以 MASTER 為準加齊，**可接受**。
4. **heroAngle／diasporaHook：** 30/30 有值且對 backup 不變；選填內部向，未寫入 synopsis。
5. **越界抽嗅（標註欄）：** 未見政治口號／真實抗爭再現；真人藝名／真實台名未在 boardNote／discoverNote 硬撞（舊 heroAngle 若含角色名屬既有欄，本次未改）。

---

## 8. 與交付自檢對照

| 交付自檢項 | 獨立覆核 |
|---|---|
| synopsis SHA 30/30 | PASS |
| 保護欄不變 | PASS（鐵律六欄） |
| eraTag 詞表＋單 string | PASS |
| 五標註欄齊 | PASS |
| high 春4夏4秋2冬4 且 ∈主詞 | PASS |

---

## 9. Wiring／出圖

| 項 | 結論 |
|---|---|
| 可作 §2A Phase1 通告板／discover wiring 草案？ | **可以**（優先級＋詞表＋權重齊） |
| 出圖 | **仍暫緩** |
| 需回修正文？ | **否**（鐵律無破） |
| 建議回修（optional nit） | 僅 `var_01` boardNote 賀歲用字；週≥2 high 留 playtest |

## Verdict

**PASS with nits** — `gigs_1988.json` v2 標註可進 wiring；出圖仍暫緩。
