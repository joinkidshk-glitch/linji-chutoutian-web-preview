# WIRING_INDEX_HOOK_v1

> **時間：** 2026-11-02（Asia/Hong_Kong）  
> **依據：** `WIRING_DRAFT_v1.md`、`WIRING_JSON_CONDITIONS_v1.md`  
> **範圍：** 本地原型 `index.html` 掛載 story detail／gigs 標註；**不出圖**、**不開 1989**、Soft leftover **HOLD**。

---

## 1. 策略

| 項 | 做法 |
|---|---|
| 通告 | **fetch 優先** `content/gigs_1988.json`；失敗則保留**內嵌** `GIGS` fallback（`const`→`let`） |
| 劇情 detail | fetch merge／romance／rival JSON → 存入全域 `STORY_WIRE`（資料層） |
| 教學／beats | 既有 `story_beats_phase1`／tutorial／events／npc **路徑不變** |
| 劇情 UI | **未**做完整抉擇播放器；選單「接線資料」＝除錯面板 |
| loc | id `tvb_longmen` 保留；`LOCS.name`＝星河電視台 |

---

## 2. 掛載清單

| 資源 | 路徑 | 消費方式 |
|---|---|---|
| 通告＋標註 | `content/gigs_1988.json` | 覆寫 `GIGS`；用 `boardPriority`／`seasonWeight`／`eraTag`／`discoverNote` |
| 主線 | `content/story_detail_c1_to_c17.json` | `STORY_WIRE.main`（權威 merge；不分冊） |
| 感情 Pack1 | `…_romance_vera_hiu_choi.json` | `STORY_WIRE.romance.veraHiuChoi` |
| 感情 Pack2 | `…_romance_lan_xu.json` | `STORY_WIRE.romance.lanXu` |
| 鄧麗萍 | `…_romance_tang.json` | `STORY_WIRE.romance.tang` |
| 對手／導師 | `…_rival_mentor.json` | `STORY_WIRE.rival` |
| 既有 | npc／events／beats／tutorial | `refreshCopyPacksFromDisk` 原邏輯 |

啟動：`refreshCopyPacksFromDisk()`（頁尾）；先 `GIGS.map(normalizeGigRecord)` 再 fetch。

---

## 3. 通告板排序／卡片

`doScout` 排序改為 `boardSortCompare`：

1. `seasonRank`（當季優先，與舊行為一致）  
2. `boardPriority`：high → normal → low  
3. `seasonWeight` 高者先  
4. `id` 穩定次序  

`tipGig` 對 high／`seasonWeight` 略加分。

`gigCardHtml` 顯示：優先／一般／次要標籤、`discoverNote`、`eraTag`（字串或舊陣列）。

---

## 4. 除錯入口

- 選單 **「接線資料」** → `showWireDebug()`：載入狀態、high 列表、C 節 `openConditions` 抽樣、`tvb_longmen` 顯示名  
- Console：`STORY_WIRE`、`GIGS`（fetch 成功後掛到 `window`）

---

## 5. 如何驗收

1. 以 **http(s)** 開本地原型（勿純 `file://` 若要測 fetch；`file://` 會走內嵌 fallback）。  
2. 開 DevTools Console，應見 `[WIRING] gigs 30 fromFile true high 14 … ok`。  
3. 選單 → 接線資料：通告來源＝`gigs_1988.json`；春 high 應為 4 則且排在當季前列。  
4. 地圖開星河電視台（`tvb_longmen`）→ 只睇通告板：卡片有「優先」標籤與「發現：…」。  
5. 教學／存檔／story_beats 週章節仍可用。  
6. Soft HOLD：不檢查 stub `flag_tang_open` 節點陣列、裸旗 rename、Pack3 `parallelOk`、徐 tier。

自測紀錄（2026-11-02）：JSON parse OK；春排序 high→normal→low 通過；HTTP 提供 content 包 OK。

---

## 6. 風險／未做

| 項 | 說明 |
|---|---|
| 完整劇情 UI | 未播 C／R／A 對白與 choices；僅資料層 |
| `openConditions` 執行 | 未接遊戲旗標狀態機 |
| phase 分冊 | 不讀；只讀 `c1_to_c17` |
| 內嵌 GIGS 過時 | fallback 無 `boardPriority`／`seasonWeight`（正規化會填預設 normal／0.6） |
| `file://` | fetch 失敗屬預期；不阻擋可玩 |
| 出圖／1989／publish | 未做 |
| Soft leftovers | HOLD |
| index 其他未提交改動 | 工作樹可能另有 v17 教學等既有 diff；本輪只加 wiring hook |

---

## 7. 改動檔

- `index.html`（backup：`index.html.bak-before-wiring-hook`）  
- `content/WIRING_INDEX_HOOK_v1.md`（本檔）  
- store 同步：本 md（index 體積大，store 慣例以 content 文檔為主；若需亦可存註記）

*完 — WIRING_INDEX_HOOK_v1*
