# QA_GIGS_1991_v1

> 《臨記出頭天》`gigs_1991` **v1.0** 年庫｜文件／靜態碼 QA（**不改正文**；**NOT browser**）
>
> 對照：`content/gigs_1991.json`、`content/GIGS_1991_v1.md`、`gigs_1988`／`1989`／`1990` schema、`QA_GIGS_1989_v1`／`QA_GIGS_1990_v1`、`PLOT_MASTER_PLAN_v1.4-DS` §2A.2／§2A.6、`index.html`（fetch 1991／`gigsByYear[1991]`／`syncGigsForCalendarYear`）
>
> QA 時間：2026-11-03（Asia/Hong_Kong）

## Overall

**PASS with nits**

- Canonical **`content/gigs_1991.json` v1.0**：**37** 則 parse OK；類型／四季配比＝`GIGS_1991_v1` 表；**每季 high＝4** 且 high.eraTag ∈ §2A.6 當季主詞。
- eraTag **12** 覆蓋表＝實際＝MASTER §2A.6 1991 詞表；`seasonWeight` 主 1.0／次 0.6 全對（31×1.0／6×0.6；無誤標 0.3）。
- 紅線：無政治口號／抗爭／六四／九七政治表態／真人藝名／真實報刊電台；顯示無無線／TVB／龍門（用**星河**）；`loc` id 可留 `tvb_*`。
- Per-gig schema 與 1988／1989／1990 **欄位集合對齊**；id 全 `gig_1991_*`。
- index 靜態：fetch `gigs_1991.json`→`gigsByYear[1991]`；`syncGigsForCalendarYear` 含 1991（`pick(y)||pick(y-1)||pick(1989)||pick(1988)`）；`advanceDay` 呼叫；接線面板年庫；`index.html.bak-before-gigs-1991` 存在。
- Soft leftover **未誤清**（HOLD）；**未出圖**；**1992 未做**。

---

## 1. Hard — 數量／類型／季配比

| 檢查 | 結果 |
|---|---|
| JSON parse（top：`version/year/gigs[]`） | **PASS**（v1.0／1991） |
| 則數 | **37／37** |
| 類型 | 綜藝 9／電影 9／唱片通告 8／電視劇 6／廣告 5＝文檔表 |
| 季則數 | 春 9／夏 10／秋 9／冬 9 |
| 季×類型 | 春 電影3+TV3+廣告2+唱片1；夏 綜藝5+電影2+TV2+廣告1；秋 唱片5+綜藝2+廣告2；冬 電影4+綜藝2+唱片2+TV1 — **全對文檔** |
| `boardPriority` | high 16／normal 12／low 9 |

§2A.2 1991 方向（綜高／影高／唱高／劇中／廣中）：配比合理，不擋 PASS。

---

## 2. Hard — 每季 high×4 ＋ 主詞

| 季 | high | 目標 | high.eraTag ∈ 主集合（§2A.6） |
|---|---|---|---|
| 春 | 4 | 4 | PASS（family／departure；`film_01`–`03`、`tv_01`） |
| 夏 | 4 | 4 | PASS（anniversary／power；`var_01`–`03`、`film_04`） |
| 秋 | 4 | 4 | PASS（music／radio；`rec_02`–`05`） |
| 冬 | 4 | 4 | PASS（festive／press；`film_06`–`09`） |

---

## 3. Hard — eraTag 覆蓋 ＋ seasonWeight

| eraTag | 文檔 | 實際 | §2A.6 | 角色 | sw |
|---|---|---|---|---|---|
| `era_1991_spring_family` | 5 | 5 | 主 | 主 | 1.0 |
| `era_1991_spring_departure` | 3 | 3 | 主 | 主 | 1.0 |
| `era_1991_spring_literary` | 1 | 1 | 次 | 次 | 0.6 |
| `era_1991_summer_anniversary` | 4 | 4 | 主 | 主 | 1.0 |
| `era_1991_summer_power` | 4 | 4 | 主 | 主 | 1.0 |
| `era_1991_summer_festive` | 2 | 2 | 次 | 次 | 0.6 |
| `era_1991_autumn_music` | 4 | 4 | 主 | 主 | 1.0 |
| `era_1991_autumn_radio` | 3 | 3 | 主 | 主 | 1.0 |
| `era_1991_autumn_variety` | 2 | 2 | 次 | 次 | 0.6 |
| `era_1991_winter_festive` | 5 | 5 | 主 | 主 | 1.0 |
| `era_1991_winter_press` | 3 | 3 | 主 | 主 | 1.0 |
| `era_1991_winter_scandal` | 1 | 1 | 次 | 次 | 0.6 |

**eraTag 12／12** 覆蓋；`season`（春夏秋冬）與 eraTag 季段 **0 mismatch**；元數據 `seasonWeightRule` 與實值一致。

---

## 4. Hard — 紅線／專名／id

| 檢查 | 結果 |
|---|---|
| 政治口號／抗爭／六四／天安門／九七政治表態 | **PASS**（顯示僅見否定句「不談政治／不寫政治口號／不做政治隱喻」等） |
| 真人藝名（抽核 80s–90s 常見名） | **PASS**（0） |
| 真實報刊／電台名 | **PASS**（0） |
| 顯示字串無線／TVB／龍門（除 `loc` id） | **PASS**（0）；星河提及 19 處 |
| `displayRules.tvStationName=星河電視台`；`locIdRetained` 含 `tvb_*` | **PASS**（與 1988–1990 慣例一致） |
| id 前綴 `gig_1991_`；唯一 37 | **PASS** |
| `year` 欄全 1991 | **PASS** |

---

## 5. Hard — schema vs `gigs_1988`／`1989`／`1990`

| 檢查 | 結果 |
|---|---|
| per-gig 鍵集合 | **相等**（25 鍵；與 1988／1989／1990 一致） |
| 全則欄位齊 | **37／37** 無缺欄 |
| `eraTag` 型別 | str |
| `discoverNote`≤30／`boardNote`≤20 | **PASS**（max 10／9） |
| top-level | 與 1989／1990 同型超集（`locale`／`displayRules`／`eraTagPrimary|Secondary`／`highBySeason` 等）；gig 層對齊即可 |
| workspace ≡ manager store 檔 | **PASS**（byte-identical） |

---

## 6. Hard — index 掛載（靜態 grep）

| 檢查 | 結果 |
|---|---|
| `refreshCopyPacksFromDisk` fetch `gigs_1991.json` | **PASS** |
| `STORY_WIRE.gigsByYear` 含 **1991** 寫入 | **PASS** |
| `syncGigsForCalendarYear`：`pick(y)\|\|pick(y-1)\|\|pick(1989)\|\|pick(1988)` | **PASS**（含 1991） |
| `advanceDay` 呼叫 sync | **PASS** |
| 接線面板「年庫：`gigsYearActive`／來源 gigs_YEAR.json」 | **PASS** |
| `index.html.bak-before-gigs-1991` 存在 | **PASS** |
| 本輪瀏覽器推 `dayIndex`→1991 前綴 | **未驗**（brief＝NOT browser；靜態掛載 OK） |

---

## 7. Soft / nits（不擋年庫收口）

1. **`syncGigsForCalendarYear` 註解**仍寫「1988／1989」；實作已含 1990／1991（`pick(y)`／`pick(y-1)`）— 建議改註解對齊（承接 `QA_GIGS_1990` nit）。
2. **瀏覽器跨年**（`S.dayIndex`→1991、`GIGS` id 前綴、`boardSortCompare`）本 QA **未跑 HTTP**；靜態掛載已過。
3. Soft leftover／出圖／1992：**仍 HOLD／暫緩／未做**（與 brief 一致，非回歸）。

---

## 8. 出圖／範圍

| 項 | 判定 |
|---|---|
| 出圖 | **仍暫緩**（無 1991 art asset） |
| 1992 年庫 | **未做**（無 `gigs_1992`） |
| Soft≠PASS；Soft HOLD | **遵守** |

---

## 9. 對 Manager 一句

`gigs_1991` v1：**PASS with nits**（`QA_GIGS_1991_v1.md`）。37 則；季 high×4＋主詞；era12／sw／星河／schema／index 靜態掛載 OK；nit：sync 註解仍寫 88／89；瀏覽器跨年另驗；出圖仍暫緩。

---

*完 — QA_GIGS_1991_v1*
