# QA｜WIRING_OC_ENGINE_v1 靜態對表覆測（STATIC｜browser 待併）

> **範圍：** `content/WIRING_OC_ENGINE_v1.md`＋`index.html` vs `index.html.bak-before-oc-engine`。  
> **對照：** `WIRING_JSON_CONDITIONS_v1`、`WIRING_INDEX_HOOK_v1`、`story_detail_romance_tang.json` v1.2、`story_detail_c1_to_c17.json` v1.1。  
> **方法：** grep／Read／diff／JSON 抽樣；**NOT browser**（HTTP／Console／UI 點擊另輪併）。  
> **規則：** Soft≠PASS・唔 publish；本輪 QA **未改** content／index。  
> **時間：** 2026-11-02 23:55（Asia/Hong_Kong）

---

## Overall：**PASS with nits**（STATIC）

| 層 | 結果 |
|---|---|
| `window.StoryOC` API（文檔 §4 ↔ 碼） | **PASS** |
| Tang：meet=`[]`／push1+ 雙閘／threshold=2／`tangFileThreshold`／`debugUnlockTangPush` | **PASS**（碼＋JSON 同向） |
| null threshold → `THRESHOLD_NULL_POLICY="skip"` | **PASS**（在碼內） |
| `showWireDebug` 標 **OC_ENGINE_v1**／可出清單／Playtest 鈕 | **PASS**（靜態） |
| 未接對白播放／`flags_written` 自動 | **PASS** |
| Soft HOLD；出圖／1989 未做 | **PASS** |
| 與 CONDITIONS／JSON id 同向 | **PASS** |
| Browser 驗收步驟（文檔 §8 HTTP／Console） | **PENDING**（本輪不做） |
| Soft remaining／文件 nits | **NIT**（不升 FAIL） |

**出圖仍暫緩。** Soft leftover **仍 HOLD**。本輪 **唔 publish**。Browser 待併。

---

## 1. Diff 範圍（bak → index）

| 項 | 結果 |
|---|---|
| `index.html.bak-before-oc-engine` | 存在；**無** `StoryOC`／`OC_ENGINE` |
| `index.html` | 新增 `StoryOC` IIFE（約 L3134–3451）；擴充 `showWireDebug`；`fresh().story`；load `ensure` |
| 出圖／1989／art pipeline | diff **無**相關改動 |
| 教學／`story_beats`／通告主路徑 | 未見改寫（OC 層分離） |

---

## 2. `window.StoryOC` API

文檔 §4 所列方法均在碼內匯出並掛 `window.StoryOC`：

| 方法／常數 | 在碼 |
|---|---|
| `ensure`／`evalToken`／`evalNode`／`listOpen`／`iterNodes` | ✓ |
| `markDone`／`setFlag`／`bumpRel`／`setPhase`／`setRoute` | ✓ |
| `resolveThreshold`／`tangFileThreshold`／`debugUnlockTangPush` | ✓ |
| `PHASE_ORDER`／`THRESHOLD_NULL_POLICY` | ✓ |
| 輔助：`phaseRank`／`currentPhase`／`isDone`／`getFlag`／`getRel` | ✓（一併匯出） |

狀態形狀：`S.story = { done, flags, rel, routes, phase }`；與教學 `S.flags` 分離；`getFlag` 相容讀 `S.flags`。`fresh()` 已帶 `story` 預設；load 路徑呼叫 `StoryOC.ensure()`。

---

## 3. Tang 雙閘（碼 ↔ JSON）

| 節點／機制 | JSON（tang v1.2） | StoryOC 行為 |
|---|---|---|
| `R_tang_meet` | `openConditions=[]` | `[]`＝AND 全過（無旗閘） |
| `R_tang_push1+`（push1／2／crisis／ending） | AND=`[flag_tang_open, rel_tang_threshold]`；**無** `openConditionsAny`；`thresholds.rel_tang_threshold=2` | `rel_tang_threshold` **不 skip**；讀 node.thresholds → 否則 `tangFileThreshold()`（檔級／qa／預設 **2**） |
| `debugUnlockTangPush` | — | `flag_tang_open=true` + `rel_tang ≥ need` |
| 檔級 | `meet=[]`；`pushAndAfter=[flag_tang_open, rel_tang_threshold]`；`rel_tang_threshold=2` | 與 CONDITIONS／Soft FIX 同向 |

---

## 4. null threshold → skip

| 證據 | 結果 |
|---|---|
| `const THRESHOLD_NULL_POLICY = "skip"` | ✓ |
| `fame_threshold`／其他 `rel_*_threshold` 為 null／缺省 → `skipped:true`，`evalToken` 回 `{ok:true, skipped:true, reason:"*_null_skip"}` | ✓ |
| `rel_tang_threshold` **例外執行**（不用 skip） | ✓ |
| 面板 `∅th` 標 `skippedThresholds` | ✓（`showWireDebug`） |
| JSON 有 null 門檻可餵引擎（例 C5／C6／C13／C15） | ✓（與 CONDITIONS 同向） |

---

## 5. `showWireDebug`（靜態）

| 項 | 結果 |
|---|---|
| 文案含 **OC_ENGINE_v1** | ✓ |
| 呼叫 `StoryOC.listOpen`；列可出／未開／done；`rel_tang`／`flag_tang_open` | ✓ |
| Playtest：標記 C1、phase→P2、Tang 雙閘、重新評估 | ✓ |
| 選單「接線資料」`data-m="wire"` | ✓（INDEX_HOOK 既有） |

**Browser 實際開局可見 C1／R_tang_meet、mark C1→C2、雙閘→push1：本輪未跑 → PENDING。**

---

## 6. 未接範圍（屬實）

| 項 | 證據 |
|---|---|
| 無對白／抉擇播放器 | `markDone` 只寫 `done[id]`；無 beats／choices runner |
| `flags_written` 不自動套用 | `index.html` **零** `flags_written` 引用；僅存於 JSON |
| 排他 commit／HE·BE | 未見 |
| 出圖／1989 | 文檔聲明＋diff 無；**暫緩** |

---

## 7. Soft HOLD（同向，未誤清）

| leftover（前輪） | 現況 |
|---|---|
| `R_tang_meet_stub` 仍列；`flags_written` 仍含 `flag_tang_open`（與 choice 不一致） | **仍在** lan_xu；`openConditionsNote` 自標 Soft HOLD |
| Pack3 ending `parallelOk: true` | **仍在**（抽樣 8 ending） |
| 徐 cast `tier=阻力` | **仍在** `cast_main.json`（`tsui_poushan`） |
| Vera「裸旗」 | OC token 已為 `hiu_`／`choi_`／`flag_vera_*` 等（前輪 nit 語意若指 speaker／文案則另；本輪引擎未改 JSON） |

文檔 §9 Soft HOLD 聲明與碼／JSON **同向**。

---

## 8. 與 CONDITIONS／INDEX_HOOK／JSON id 同向

| 項 | 結果 |
|---|---|
| `iterNodes` 掃 main＋veraHiuChoi＋lanXu＋tang＋rival | 與 INDEX_HOOK fetch 五包一致 |
| C1=`[]`→C2=`[C1]` 鏈 | 與 c1_to_c17／CONDITIONS 一致 |
| Tang 雙閘 id／flag／threshold=2 | 與 CONDITIONS §Tang／JSON v1.2 一致 |
| Token 語義（done／flag_*／route_*／phase／rel_*_threshold／fame／season soft） | 與文檔 §5 對得上（靜態） |

---

## 9. Nits（不升 FAIL）

1. **Browser PENDING**：文檔 §8 六步（HTTP、`[WIRING]`、開局可出、mark C1、Tang 雙閘 Console）未在本輪執行；Verdict 僅 STATIC。  
2. Soft leftover **仍 HOLD**（stub `flags_written`、Pack3 `parallelOk`、徐 `tier=阻力`）— 預期。  
3. `season_*`／`era_*` 軟閘失敗會鎖 AND／ANY（文檔已標風險）；靜態無法證季節日曆互動。  
4. 自測「node harness」聲稱通過 — 本輪未重跑 harness；以碼／JSON 對表為準。

---

## 10. 結論

**STATIC PASS with nits。** `StoryOC`／Tang 雙閘／null-skip **均在碼內**且與 CONDITIONS／tang・c1 JSON 同向；未接對白／`flags_written` 自動屬實；Soft HOLD；**出圖仍暫緩**。併 browser 後可升完整 Verdict。

*完 — QA_WIRING_OC_ENGINE_v1（STATIC）*
