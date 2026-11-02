# QA｜WIRING_INDEX_HOOK_v1 靜態對表（文件／碼｜非 browser）

> **範圍：** `content/WIRING_INDEX_HOOK_v1.md`＋`index.html`（對照 `index.html.bak-before-wiring-hook`）。  
> **對照：** `gigs_1988.json` v2.1.1、`WIRING_DRAFT_v1.md`、`WIRING_JSON_CONDITIONS_v1.md`、`QA_WIRING_DRAFT_v1.md`、`QA_WIRING_JSON_CONDITIONS_v1.md`。  
> **方法：** 檔案 grep／diff／Read；**NOT browser**（並行有人做瀏覽器驗；本檔標 **STATIC**）。  
> **規則：** Soft≠PASS・唔 publish；缺關鍵 hook → FAIL；其餘 nits 不升 FAIL。  
> **時間：** 2026-11-02 23:51（Asia/Hong_Kong）

---

## Overall：**PASS with nits**（**STATIC**）

| 層 | 結果 |
|---|---|
| fetch 清單 → `STORY_WIRE`／覆寫 `GIGS` | **PASS** |
| `boardSortCompare` 次序 | **PASS** |
| 選單「接線資料」→ `showWireDebug` | **PASS** |
| Console `[WIRING]` 字串在碼內 | **PASS**（runtime 待 browser 併） |
| `tvb_longmen` id 保留／顯示名星河 | **PASS** |
| 未接 openConditions 執行引擎／完整劇情 UI | **PASS**（聲稱屬實） |
| Soft HOLD；出圖／1989 未做 | **PASS** |
| 與 CONDITIONS／JSON 路徑檔名一致 | **PASS** |
| Soft／文件 nits | **NIT**（不升 FAIL） |
| 出圖 | **暫緩** |

**Verdict 以靜態為準。** Browser Console／通告板實跑結果 **待併**（本 QA 未開 browser）。  
**出圖仍暫緩。** Soft leftover **仍 HOLD**。本輪 **唔 publish**。本 QA **未改** index／story JSON。

---

## 1. fetch → STORY_WIRE／GIGS

`refreshCopyPacksFromDisk()`（約 L3277–3331）`Promise.all` 含：

| 資源 | 路徑字串 | 寫入 |
|---|---|---|
| 通告 | `content/gigs_1988.json` | 成功則 `GIGS = gigsPack.gigs.map(normalizeGigRecord)`；`STORY_WIRE.gigsFromFile=true` |
| 主線 | `story_detail_c1_to_c17.json` | `STORY_WIRE.main` |
| romance×3 | `…_vera_hiu_choi`／`…_lan_xu`／`…_tang` | `STORY_WIRE.romance.{veraHiuChoi,lanXu,tang}` |
| 對手 | `story_detail_rival_mentor.json` | `STORY_WIRE.rival` |

另保留既有 npc／events／beats／tutorial fetch。`let GIGS`（非 const）；頁尾 `GIGS = GIGS.map(normalizeGigRecord)` 後呼叫 `refreshCopyPacksFromDisk()`。`window.STORY_WIRE`／`window.GIGS` 掛載存在。

**五路徑檔案皆存在於 `content/`**（與 CONDITIONS §改動檔一致）。

---

## 2. `boardSortCompare`

L3353–3362：

1. `seasonRank(a,cur) - seasonRank(b,cur)`（當季優先）  
2. `boardPriorityRank`：high(0) → normal(1) → low(2)  
3. `seasonWeight` 高者先（`wb - wa`）  
4. `id` `localeCompare`

`doScout` 用 `byBoard=(a,b)=> boardSortCompare(a,b,curSeason)` 排序 eligible／locked／fallback。  
`gigCardHtml`：`bp-tag` 優先／一般／次要＋`discoverNote`＋`eraTag`。  
`tipGig`：high +8／low −4／`seasonWeight*6`（與 HOOK §3 一致）。

---

## 3. 選單「接線資料」

- HTML：`<button … data-m="wire">接線資料</button>`（約 L1640）  
- Handler：`if(m==="wire")showWireDebug();`（約 L5690）  
- `showWireDebug`：載入狀態、來源標籤、high 列表、`openConditions` **抽樣顯示**、`tvb_longmen` 顯示名；明示「完整劇情 UI 未實作」

---

## 4. Console `[WIRING]`

碼內存在：

```text
console.info("[WIRING]", "gigs", …, "fromFile", …, "high", …, "C", …, "R", …, "A", …, errors|"ok")
```

與 HOOK §5 預期字串形狀一致。**實際 HTTP 下是否印出** → 待 browser QA 併入。

---

## 5. `tvb_longmen`／星河

- `LOCS`：`id:"tvb_longmen"`, `name:"星河電視台"`（約 L1801）  
- Debug 面板標「id 保留」  
- 內嵌／JSON gigs 仍用 loc id `tvb_longmen`（未改 id）

---

## 6. 未接引擎／劇情 UI（範圍「未做」屬實）

| 聲稱 | 靜態核對 |
|---|---|
| 完整劇情 UI 未做 | **無** C／R／A 抉擇播放器；`STORY_WIRE` 僅資料層＋debug |
| `openConditions` 未接狀態機 | 全檔 `openConditions` **僅**出現於 `showWireDebug` 抽樣 JSON.stringify；**無** evaluate／gate／flag 消費邏輯 |
| 不出圖／不開 1989 | index／HOOK 無 `gigs_1989`／出圖流程；HOOK §6 明示 |
| Soft HOLD | index **無** 改 stub `flag_tang_open`／`parallelOk`／徐 tier；與 CONDITIONS leftover 同向 |

---

## 7. 與 CONDITIONS／DRAFT 路徑一致

fetch 檔名＝CONDITIONS §改動檔／DRAFT 消費路徑：

- `gigs_1988.json`  
- `story_detail_c1_to_c17.json`  
- `story_detail_romance_vera_hiu_choi.json`  
- `story_detail_romance_lan_xu.json`  
- `story_detail_romance_tang.json`  
- `story_detail_rival_mentor.json`  

**進度說明（非 FAIL）：** DRAFT／CONDITIONS 曾寫「index 未改／下一輪」——本 HOOK **即該下一輪**；靜態上已落地，與前兩份 QA「未掛 index」時間點不衝突。

backup：`index.html.bak-before-wiring-hook` 存在；diff 主要新增 STORY_WIRE／fetch／sort／選單／卡片標籤／`[WIRING]` log。

---

## 8. Soft leftover（HOLD｜同向）

對照 `QA_SOFT_NITS_FIX_v1`／CONDITIONS leftover：本輪 **未**清 stub `flag_tang_open` 節點陣列、Vera 裸旗 rename、Pack3 ending `parallelOk`、徐 cast `tier=阻力`。HOOK §5.6／§6 明示不檢查 → **同向 HOLD**。

---

## 9. Nits（不升 FAIL）

1. **Browser 未驗**：fetch 成功／`[WIRING] … ok`／春 high 前列排序 runtime → 待併。  
2. DRAFT／CONDITIONS 正文仍留「index 未掛」舊句（歷史正確；可下輪文件補一句「已由 INDEX_HOOK_v1 接」）。  
3. 內嵌 fallback GIGS 仍無完整標註欄（HOOK 已知風險；`normalizeGigRecord` 填 normal／0.6）——`file://` 預期。  
4. Soft 徐 `tier=阻力` 仍未入 DRAFT §8（舊 nit；本輪 index 亦不涉及 cast）。

---

## 10. 本輪觸碰

| 檔 | 本 QA |
|---|---|
| `content/QA_WIRING_INDEX_HOOK_v1.md` | **新建** |
| `index.html`／story JSON／gigs | **未改** |

*完 — QA_WIRING_INDEX_HOOK_v1（STATIC）*
