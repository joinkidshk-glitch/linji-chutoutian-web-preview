# QA_GIGS_1992_v1

> 《臨記出頭天》`gigs_1992` **v1.0** 年庫｜文件／靜態碼 QA（**不改正文**；**NOT browser**）
>
> 對照：`content/gigs_1992.json`、`content/GIGS_1992_v1.md`、`gigs_1988`–`1991` schema、`QA_GIGS_1989`–`1991_v1`、`PLOT_MASTER_PLAN_v1.4-DS` §2A.2⑥／§2A.6、`index.html`（fetch 1992／`gigsByYear[1992]`／`syncGigsForCalendarYear`）
>
> QA 時間：2026-11-03（Asia/Hong_Kong）

## Overall

**PASS with nits**

- Canonical **`content/gigs_1992.json` v1.0**：**30** 則 parse OK（非 37；落在 25–35）。
- **§2A.2⑥ 收束年**：春 12＋夏 12 為主；秋 3＋冬 3 收束（非完整季庫）；秋冬 **high＝0**；掛 `era_1992_summer_lookback`／`legacy`，`seasonWeight=0.3`。
- **high 春／夏各 4**（合計 high 8）；high.eraTag ∈ §2A.6 當季主詞。
- eraTag **6** 覆蓋＝文檔＝MASTER §2A.6 1992 詞表（秋冬無獨立條，掛夏主詞）；`seasonWeight` 主 1.0／次 0.6／掛鉤 0.3 全對。
- 紅線：無政治口號／抗爭／六四／九七政治表態／真人藝名／真實報刊電台獎項；顯示無無線／TVB／龍門（用**星河**）；`loc` id 可留 `tvb_*`。
- Per-gig schema 與 1988–1991 **欄位集合對齊**；id 全 `gig_1992_*`。
- index 靜態：fetch `gigs_1992.json`→`gigsByYear[1992]`；`syncGigsForCalendarYear`：`pick(y)||pick(y-1)||pick(1989)||pick(1988)`（含 1992）；`advanceDay` 呼叫；接線面板年庫；`index.html.bak-before-gigs-1992` 存在。
- Soft leftover **未誤清**（HOLD）；**未出圖**。

---

## 1. Hard — 數量／類型／季配比（收束年）

| 檢查 | 結果 |
|---|---|
| JSON parse（top：`version/year/gigs[]`） | **PASS**（v1.0／1992） |
| 則數 | **30／30**（≠前幾年 37；符合 §2A.2⑥／文檔 25–35） |
| 類型 | 電影 12／綜藝 5／電視劇 5／廣告 4／唱片通告 4＝文檔表 |
| 季則數 | 春 12／夏 12／秋 3／冬 3 |
| 季×類型 | 春 電影5+TV4+唱片3；夏 電影5+綜藝4+廣告3；秋 電影1+綜藝1+唱片1；冬 電影1+廣告1+TV1 — **全對文檔** |
| `boardPriority` | high 8／normal 12／low 10 |

§2A.2 1992 方向（影高／綜中高／劇中／廣中／唱中；春揀劇本→夏收束回望）：配比合理，不擋 PASS。

---

## 2. Hard — high 春夏各 4；秋冬 0

| 季 | high | 目標 | high.eraTag ∈ 主集合（§2A.6） |
|---|---|---|---|
| 春 | 4 | 4 | PASS（choice／script；`film_01`／`02`／`04`、`tv_01`） |
| 夏 | 4 | 4 | PASS（legacy／lookback；`film_06`–`08`、`var_01`） |
| 秋 | 0 | 0 | PASS（收束；無 high） |
| 冬 | 0 | 0 | PASS（收束；無 high） |

---

## 3. Hard — eraTag 覆蓋 ＋ seasonWeight

| eraTag | 文檔 | 實際 | §2A.6 | 角色 | sw（春夏）／掛鉤 |
|---|---|---|---|---|---|
| `era_1992_spring_choice` | 4 | 4 | 主 | 主 | 1.0 |
| `era_1992_spring_script` | 5 | 5 | 主 | 主 | 1.0 |
| `era_1992_spring_literary` | 3 | 3 | 次 | 次 | 0.6 |
| `era_1992_summer_legacy` | 7 | 7 | 主 | 主＋秋冬掛 | 1.0／0.3 |
| `era_1992_summer_lookback` | 8 | 8 | 主 | 主＋秋冬掛 | 1.0／0.3 |
| `era_1992_summer_festive` | 3 | 3 | 次 | 次 | 0.6 |

**eraTag 6／6** 覆蓋（1992 詞表無秋／冬獨立條）；春夏 `season`↔eraTag 季段 **0 mismatch**；秋冬 6 則全掛 summer lookback／legacy 且 **sw=0.3**；元數據 `seasonWeightRule`／`eraTagWrapNote` 與實值一致。

---

## 4. Hard — 紅線／專名／id

| 檢查 | 結果 |
|---|---|
| 政治口號／抗爭／六四／天安門／九七政治表態 | **PASS**（0） |
| 真人藝名（抽核 80s–90s 常見名） | **PASS**（0） |
| 真實報刊／電台／獎項名 | **PASS**（0） |
| 顯示字串無線／TVB／龍門（除 `loc` id） | **PASS**（0）；星河提及 9 處 |
| `displayRules.tvStationName=星河電視台`；`locIdRetained` 含 `tvb_*` | **PASS** |
| id 前綴 `gig_1992_`；唯一 30 | **PASS** |
| `year` 欄全 1992 | **PASS** |
| `discoverNote`≤30／`boardNote`≤20 | **PASS**（max 9／8） |

---

## 5. Hard — schema vs `gigs_1988`–`1991`

| 檢查 | 結果 |
|---|---|
| per-gig 鍵集合 | **相等**（25 鍵；與 1988–1991 一致） |
| 全則欄位齊 | **30／30** 無缺欄 |
| `eraTag` 型別 | str |
| top-level | 含 `scopeNote`／`eraTagWrapNote`／`highBySeason`（春夏 only）等收束年註記；gig 層對齊即可 |
| workspace ≡ manager store 檔 | **PASS**（byte-identical） |

---

## 6. Hard — index 掛載（靜態 grep）

| 檢查 | 結果 |
|---|---|
| `refreshCopyPacksFromDisk` fetch `gigs_1992.json` | **PASS** |
| `STORY_WIRE.gigsByYear` 含 **1992** 寫入 | **PASS** |
| `syncGigsForCalendarYear`：`pick(y)\|\|pick(y-1)\|\|pick(1989)\|\|pick(1988)` | **PASS**（含 1992） |
| `advanceDay` 呼叫 sync | **PASS** |
| 接線面板「年庫：`gigsYearActive`／來源 gigs_YEAR.json」 | **PASS** |
| `index.html.bak-before-gigs-1992` 存在 | **PASS** |
| 本輪瀏覽器推 `dayIndex`→1992 前綴 | **未驗**（brief＝NOT browser；靜態掛載 OK） |

---

## 7. Soft / nits（不擋年庫收口）

1. **`syncGigsForCalendarYear` 註解**仍寫「1988／1989」；實作已含 1990–1992（`pick(y)`／`pick(y-1)`）— 建議改註解對齊（承接 `QA_GIGS_1990`／`1991` nit）。
2. **瀏覽器跨年**（`S.dayIndex`→1992、`GIGS` id 前綴 `gig_1992_`、`boardSortCompare`）本 QA **未跑 HTTP**；靜態掛載已過。
3. Soft leftover／出圖：**仍 HOLD／暫緩**（與 brief 一致，非回歸）。完整 1992 秋／冬季庫：文檔明示未做（§2A.2⑥ 暫定不產）— 非缺陷。

---

## 8. 出圖／範圍

| 項 | 判定 |
|---|---|
| 出圖 | **仍暫緩**（無 1992 art asset） |
| Soft≠PASS；Soft HOLD | **遵守** |
| 完整秋／冬庫 | **未做**（收束 3＋3 符合 §2A.2⑥） |

---

## 9. 對 Manager 一句

`gigs_1992` v1：**PASS with nits**（`QA_GIGS_1992_v1.md`）。30 則；春夏主＋秋冬各 3 收束；high 春夏各 4／秋冬 0；era6／sw／星河／schema／index 靜態掛載 OK；nit：sync 註解仍寫 88／89；瀏覽器跨年另驗；出圖仍暫緩。

---

*完 — QA_GIGS_1992_v1*
