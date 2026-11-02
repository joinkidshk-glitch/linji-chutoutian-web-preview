# QA_GIGS_1989_v1

> 《臨記出頭天》`gigs_1989` **v1.0** 年庫｜文件／靜態碼 QA（**不改正文**；瀏覽器跨年切換另驗）
>
> 對照：`content/gigs_1989.json`、`content/GIGS_1989_v1.md`、`content/gigs_1988.json` schema、`PLOT_MASTER_PLAN_v1.4-DS` §2A.2／§2A.6、`QA_GIGS_1988_*`、`index.html`（`syncGigsForCalendarYear`／fetch 1989／接線年庫）
>
> QA 時間：2026-11-03（Asia/Hong_Kong）

## Overall

**PASS with nits**

- Canonical **`content/gigs_1989.json` v1.0**：**37** 則 parse OK；類型／四季配比＝`GIGS_1989_v1` 表；**每季 high＝4** 且 high.eraTag ∈ §2A.6 當季主詞。
- eraTag 覆蓋表＝實際；`seasonWeight` 主 1.0／次 0.6 自動規則全對；未用 `era_1989_summer_action`（刻意）。
- 紅線：無政治／六四／真人藝名；顯示無無線／TVB／龍門（用**星河**）；`loc` id 可留 `tvb_*`。
- Per-gig schema 與 1988 **欄位集合對齊**；id 全 `gig_1989_*`。
- index 靜態：fetch `gigs_1989.json`→`gigsByYear[1989]`；`syncGigsForCalendarYear`；`advanceDay` 呼叫；接線面板顯示年庫。
- Soft leftover **未誤清**（HOLD）；**未出圖**；**未做 1990+**。

---

## 1. Hard — 數量／類型／季配比

| 檢查 | 結果 |
|---|---|
| JSON parse（top：`version/year/gigs[]`） | **PASS** |
| 則數 | **37／37** |
| 類型 | 電視劇 9／唱片通告 8／電影 8／綜藝 7／廣告 5＝文檔表 |
| 季則數 | 春 9／夏 9／秋 10／冬 9 |
| 季×類型 | 春 TV4+廣告2+電影2+綜藝1；夏 電影3+TV3+唱片2+廣告1；秋 唱片6+綜藝2+廣告2；冬 綜藝4+電影3+TV2 — **全對文檔** |
| `boardPriority` | high 16／normal 13／low 8 |

§2A.2 1989 方向（廣中／綜中高／劇高／影中高／唱高）：配比合理，不擋 PASS。

---

## 2. Hard — 每季 high×4 ＋ 主詞

| 季 | high | 目標 | high.eraTag ∈ 主集合（§2A.6） |
|---|---|---|---|
| 春 | 4 | 4 | PASS（charity／quiet；`tv_01`–`tv_04`） |
| 夏 | 4 | 4 | PASS（departure／literary；`film_03`–`05`、`tv_05`） |
| 秋 | 4 | 4 | PASS（music／karaoke；`rec_03`–`06`） |
| 冬 | 4 | 4 | PASS（anniversary／festive；`var_04`／`05`／`07`、`film_06`） |

---

## 3. Hard — eraTag 覆蓋 ＋ seasonWeight

| eraTag | 文檔 | 實際 | 角色 | sw |
|---|---|---|---|---|
| `era_1989_spring_charity` | 4 | 4 | 主 | 1.0 |
| `era_1989_spring_quiet` | 4 | 4 | 主 | 1.0 |
| `era_1989_spring_studio` | 1 | 1 | 次 | 0.6 |
| `era_1989_summer_departure` | 5 | 5 | 主 | 1.0 |
| `era_1989_summer_literary` | 4 | 4 | 主 | 1.0 |
| `era_1989_summer_action` | 0（未用） | 0 | 次（詞表有） | — |
| `era_1989_autumn_music` | 5 | 5 | 主 | 1.0 |
| `era_1989_autumn_karaoke` | 3 | 3 | 主 | 1.0 |
| `era_1989_autumn_variety` | 2 | 2 | 次 | 0.6 |
| `era_1989_winter_anniversary` | 4 | 4 | 主 | 1.0 |
| `era_1989_winter_festive` | 3 | 3 | 主 | 1.0 |
| `era_1989_winter_press` | 2 | 2 | 次 | 0.6 |

`season`（春夏秋冬）與 eraTag 季段 **0 mismatch**；元數據 `seasonWeightRule` 與實值一致（主 32×1.0／次 5×0.6；無誤標 0.3）。

---

## 4. Hard — 紅線／專名／id

| 檢查 | 結果 |
|---|---|
| 政治口號／抗爭／六四／天安門等 | **PASS**（0） |
| 真人藝名（抽核 80s 常見名） | **PASS**（0） |
| 顯示字串無線／TVB／龍門（除 `loc` id） | **PASS**（0）；星河提及 28 處 |
| `displayRules.tvStationName=星河電視台`；`locIdRetained` 含 `tvb_*` | **PASS**（與 1988 慣例一致） |
| id 前綴 `gig_1989_`；唯一 37 | **PASS** |
| `year` 欄全 1989 | **PASS** |

---

## 5. Hard — schema vs `gigs_1988.json`

| 檢查 | 結果 |
|---|---|
| per-gig 鍵集合 | **相等**（25 鍵：含 `boardPriority`／`seasonWeight`／`eraTag`／`discoverNote`／`boardNote`／`heroAngle` 等） |
| 全則欄位齊 | **37／37** 無缺欄 |
| `eraTag` 型別 | str（與 1988 現行一致） |
| `discoverNote`≤30／`boardNote`≤20 | **PASS**（max 14／10） |
| top-level | 1989 多 `locale`／`displayRules`／`eraTagPrimary|Secondary`／`highBySeason` 等元數據（**超集**）；gig 層對齊即可 |

---

## 6. Hard — index 掛載（靜態 grep）

| 檢查 | 結果 |
|---|---|
| `refreshCopyPacksFromDisk` fetch `gigs_1989.json` | **PASS** |
| `STORY_WIRE.gigsByYear = {1988,1989}` 寫入 | **PASS** |
| `syncGigsForCalendarYear`（缺年→1988 fallback） | **PASS** |
| `advanceDay` 呼叫 sync | **PASS** |
| 接線面板「年庫：`gigsYearActive`／來源 gigs_YEAR.json」 | **PASS** |
| `index.html.bak-before-gigs-1989` 存在 | **PASS** |
| 本輪瀏覽器推 `dayIndex`→1989 前綴 | **未驗**（交瀏覽器；靜態掛載 OK） |

---

## 7. Soft / nits（不擋年庫收口）

1. **`gig_1989_tv_08` title**《台慶劇《星河風雲》》侍衛替補 — 書名號嵌套彆扭；建議改如「台慶劇《星河風雲》侍衛替補」或「《星河風雲》（台慶劇）侍衛替補」。
2. **瀏覽器跨年**（`S.dayIndex`→1989、`GIGS` id 前綴、`boardSortCompare`）本 QA **未跑 HTTP**；靜態掛載已過。
3. Soft leftover／出圖／1990+：**仍 HOLD／暫緩／未做**（與 brief 一致，非回歸）。

---

## 8. 出圖／範圍

| 項 | 判定 |
|---|---|
| 出圖 | **仍暫緩**（workspace 無 1989 art asset） |
| 1990–1992 年庫 | **未做**（無 `gigs_199*`） |
| Soft≠PASS；Soft HOLD | **遵守** |

---

## 9. 對 Manager 一句

`gigs_1989` v1：**PASS with nits**（`QA_GIGS_1989_v1.md`）。37 則；季 high×4＋主詞；era／sw／星河／schema／index 靜態掛載 OK；nit：`tv_08` 書名號嵌套；瀏覽器跨年另驗；出圖仍暫緩。

---

*完 — QA_GIGS_1989_v1*
