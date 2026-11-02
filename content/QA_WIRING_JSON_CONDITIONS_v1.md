# QA｜WIRING_JSON_CONDITIONS_v1 對表覆測（文件｜非 browser）

> **範圍：** `content/WIRING_JSON_CONDITIONS_v1.md`＋五份 story detail JSON（版本以 CONDITIONS 為準）。  
> **對照：** `WIRING_DRAFT_v1.md`、`QA_WIRING_DRAFT_v1.md`、`QA_SOFT_NITS_FIX_v1.md` leftover（**HOLD**）。  
> **Canon：** `PLOT_MASTER_PLAN_v1.4-DS.md`、`PLOT_DETAIL_UNLOCK_v1.md`。  
> **規則：** Soft≠PASS・唔 publish；核對**實際 JSON 欄位**；不出圖／不 browser；本輪 QA **未改** content。  
> **時間：** 2026-11-02 23:50（Asia/Hong_Kong）

---

## Overall：**PASS with nits**

| 層 | 結果 |
|---|---|
| 88 節 `openConditions`（文檔清單 ↔ JSON） | **PASS**（17+15+11+5+40＝**88**；缺 OC＝0） |
| Tang：meet=`[]`／push1+ 雙閘／`rel_tang_threshold=2` | **PASS**（檔級＋節點＋`thresholds` 一致） |
| 與 WIRING_DRAFT 同向（flag／id 寫入 JSON） | **PASS**（draft 所列 MISSING OC 已填；抽樣＋主線／romance／Tang／Pack3 AND 全檢 0 mismatch） |
| 回歸（版本／E01–E10／C14=T6／保護意圖／分冊未同步／本輪未改 index） | **PASS**（見 §4；對白「一字不差」依 edits 聲稱＋結構抽樣，無預 CONDITIONS 快照可逐字 diff） |
| Soft HOLD 同向（未誤稱已清） | **PASS** |
| Soft remaining / 文件 nits | **NIT**（不升 FAIL） |
| 出圖 | **暫緩** |

**出圖仍暫緩。** Soft leftover **仍 HOLD**。本輪 **唔 publish**。

---

## 1. 版本／節點數

| 檔案 | 聲稱 | JSON `version` | nodes | 有 `openConditions` |
|---|---|---|---|---|
| `story_detail_c1_to_c17.json` | 1.1 | **1.1** | 17 | **17** |
| `story_detail_romance_vera_hiu_choi.json` | 1.2 | **1.2** | 15 | **15** |
| `story_detail_romance_lan_xu.json` | 2.2 | **2.2** | 11 | **11** |
| `story_detail_romance_tang.json` | 1.2 | **1.2** | 5 | **5** |
| `story_detail_rival_mentor.json` | 2.2 | **2.2** | 40 | **40** |
| **合計** | 83 寫入／對齊＋Tang 5 確認 | — | **88** | **88** |

CONDITIONS §9「83＋Tang 5」與實際 **88 節皆有 OC** 對齊。五檔皆有 `conditionSchema`。

---

## 2. 88 節 openConditions（清單 ↔ JSON）

### 2.1 主線 C1–C17（全檢）

CONDITIONS §3 表之 AND／ANY／thresholds 有無與 JSON **0 mismatch**。

| 抽樣／關鍵 | JSON 實際 | 結果 |
|---|---|---|
| C1 AND=`[]` | `[]` | PASS |
| C2–C4／C7–C8／C10／C12／C17 鏈 | 與表一致（C12–C15 共同前置 C11） | PASS |
| C5 AND=`[C4]` ANY＝rel_choi∥season…；thresholds null | 一致 | PASS |
| C6 ANY＝三 rel_*；thresholds null | 一致 | PASS |
| C9 ANY＝lan meet 雙旗 | 一致 | PASS |
| C11 ANY＝route_indie∥tsijun 旗 | 一致 | PASS |
| C13 ANY＝choi／mei／fame／`R_choi_crisis` | 一致 | PASS |
| C14 ANY＝xu 旗／`R_xu_crisis`；**conflict=T6** | 一致 | PASS |
| C15 ANY＝lan／`R_lan_crisis`；when 可早於 C12（Note） | 一致 | PASS |
| C16 AND=`[phase_P5]` | 一致 | PASS |

### 2.2 Pack1／Pack2／Tang／Pack3

| 包 | 檢法 | 結果 |
|---|---|---|
| Pack1 15 | CONDITIONS §4 AND／ANY **全檢** | **0 mismatch** |
| Pack2 11（含 stub） | §4 AND／ANY **全檢**；stub OC=`[]` | **0 mismatch** |
| Tang 5 | meet=`[]`；push1+＝`[flag_tang_open, rel_tang_threshold]`；**無** `openConditionsAny`；push+ `thresholds.rel_tang_threshold=2` | **PASS** |
| Pack3 40 | AND **全檢 0 mismatch**；ANY 與表（含截斷列之完整 JSON 值）對得上 | **PASS**（見 nits：meet 表寫 `[]` vs 鍵缺省） |

Tang **檔級**：`meet=[]`；`pushAndAfter=[flag_tang_open, rel_tang_threshold]`；`rel_tang_threshold=2` — 與 Soft FIX／CONDITIONS §4 同向。

---

## 3. 與 WIRING_DRAFT 同向

| 項 | 結果 |
|---|---|
| Draft 標 `<MISSING>`／硬接線債之節點級 OC | 本輪 JSON **已寫入**（主線／romance／rival） |
| Draft 旗／id（如 C9 lan、C11 route_indie、C13 `R_choi_crisis`、C14 `R_xu_crisis`、Tang 雙閘） | **已入** `openConditions`／`Any` |
| Pack3 `linksMain` 既有保留 | 抽樣 `A_ko_meet→[C3]`、`R_xu_crisis→[C14]`＋conflict T6 | PASS |
| 誤收緊？ | 未見把 Soft HOLD 收成必清；Tang meet 仍空閘 | PASS |
| 漏接？ | 權威 merge＝`c1_to_c17`；**phase 分冊 OC=0**（CONDITIONS §6 已標未同步）—預期 | PASS／INFO |

---

## 4. 回歸

| 項 | 核對 | 結果 |
|---|---|---|
| E01–E10 | `C17.endings_catalog` 名稱：穩陣男演員…未出頭（10／10） | **PASS** |
| C14↔T6 | `C14.conflict="T6"` | **PASS** |
| 顯示名無線／TVB（主線 body） | 抽樣無「無線」；無誤插 TVB 顯示 | **PASS／抽樣** |
| phase 分冊 | `story_detail_phase*.json` **withOC=0**（聲稱未同步） | **PASS** |
| index 本輪未改 | index mtime **23:28**；JSON／CONDITIONS md **23:47–23:48** | **PASS**（mtime） |
| index 已 fetch 五 JSON？ | 是（`STORY_WIRE`＋OC 抽樣 UI）；**早於**本輪 JSON 寫入 | **FYI**（見 nits §6） |
| 對白／synopsis | 五檔 `edits` 皆稱「對白未改」；beats／choices 結構齊（C 120 beats／50 choices 等）；無預 CONDITIONS 位元組快照可證「一字不差」 | **PASS（聲稱＋結構）** |
| cast／gigs | 本輪 CONDITIONS **未**改（mtime 23:32＜JSON 23:47） | **PASS** |

---

## 5. Soft HOLD（同向・唔當 FAIL）

| Soft leftover（`QA_SOFT_NITS_FIX_v1`） | JSON 現況 | CONDITIONS |
|---|---|---|
| stub `flags_written` 仍 `flag_tang_open` | **仍是** `["flag_tang_open"]`；choice 仍寫 met | §6 HOLD |
| Vera 裸旗＋`qa.flagAlias` | 裸 `hiu_*`／`choi_*` **15**；alias **15** 鍵 | §6 HOLD |
| Vera speaker「阿偉」 | beats speaker 阿偉 **11** | qa.softHold 標明 |
| Pack3 ending `parallelOk=true` | 8 ending **全 true** | §6 HOLD |
| 徐 cast `tier=阻力` | `tsui_poushan.tier=阻力` | §6 HOLD；`R_xu_meet` 僅 `phase_P3` |

**無**誤修成「已清」。

---

## 6. Nits（不升 FAIL）

1. **表 vs JSON：`openConditionsAny: []`：** CONDITIONS Pack3（及 Pack1）meet 列寫 ANY=`[]`，實際 **省略鍵**（schema：可選）。語意＝無 OR 閘，**功能 OK**；文件表宜改「—／omit」。  
2. **`A_fong_ending.openConditionsAny`：** `flag_fong_saved_once` **重複兩次** — JSON 小 nit，建議去重。  
3. **Store sync 聲稱：** CONDITIONS §8／§9 寫「已 sync store」；store 現僅見既有 `QA_WIRING_DRAFT_v1.md`，**未見**本批 CONDITIONS md／五 JSON 複本 — **聲稱過滿**（content／為準）。  
4. **§7.1「原型尚未 fetch」偏舊：** index **已** `get()` 五 story_detail 入 `STORY_WIRE` 並有 OC 抽樣顯示（mtime 早於本輪欄位寫入）。「本輪未改 index」仍成立；硬玩法閘是否吃齊 OC 另屬引擎債。  
5. Soft leftover 四／五項 **仍 HOLD**（正確不本輪清）。

---

## 7. 建議下一步

1. Soft 續 HOLD；另票再清 stub `flags_written`／裸旗 rename／parallelOk／徐 tier。  
2. 可選小修：`A_fong_ending` ANY 去重；CONDITIONS 表 ANY=`[]`→omit；§7.1 改寫為「已 fetch／閘邏輯待吃齊」；補 store 複本或刪 sync 勾。  
3. phase 分冊 OC 同步另任務（權威＝ merge）。  
4. **出圖仍暫緩**；唔 publish（Soft≠PASS）。

---

## 8. 一句給用戶／劇本 manager

**WIRING_JSON_CONDITIONS_v1：PASS with nits**（`QA_WIRING_JSON_CONDITIONS_v1.md`）。**88 節 OC 達標**；**Tang meet=[]／push 雙閘／threshold=2 達標**；與 DRAFT 同向；Soft HOLD 未誤清；本輪 index 未改（mtime）；出圖仍暫緩。Nits：ANY=`[]` 表 vs omit、`A_fong_ending` 重複旗、store sync 聲稱、§7.1 fetch 表述偏舊。
