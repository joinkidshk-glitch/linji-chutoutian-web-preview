# WIRING_OC_ENGINE_v1

> **時間：** 2026-11-02（Asia/Hong_Kong）  
> **依據：** `WIRING_INDEX_HOOK_v1.md`、`WIRING_JSON_CONDITIONS_v1.md`  
> **範圍：** 本地原型最小 `openConditions` 執行引擎；**不出圖**、**不開 1989**、Soft leftover **HOLD**。  
> **Soft≠PASS：** 可改本地原型，非正式上線。

---

## 1. 目的

在已掛載的 `STORY_WIRE` 上，判斷 C／R／A 節點**此刻可否觸發**（AND ∩ OR＋thresholds），並在「接線資料」面板列出可出／未開清單。  
**不做**完整對白／抉擇播放器；**不**改寫教學／`story_beats`／通告主路徑。

---

## 2. 改動檔

| 路徑 | 說明 |
|---|---|
| `index.html` | 新增 `StoryOC`；`fresh().story`；load `ensure`；擴充 `showWireDebug` |
| `index.html.bak-before-oc-engine` | 套用前備份（含 INDEX_HOOK） |
| `content/WIRING_OC_ENGINE_v1.md` | 本說明 |

---

## 3. 狀態形狀（存檔相容）

```js
S.story = {
  done: {},    // 節點 id → true（已完成）
  flags: {},   // flag_*／裸前綴／等
  rel: {},     // rel_tang／rel_vera／… 數值
  routes: {},  // route_indie／…
  phase: "P1"  // P1 | P1_5 | P2 | P3 | P4 | P5
}
```

- 與 `S.flags`（教學／通告 milestone）**分離**；`getFlag` 會**順帶**讀 `S.flags` 作相容。  
- 舊存檔無 `story` → `StoryOC.ensure()` 補齊；不破壞既有欄位。

---

## 4. API（`window.StoryOC`）

| 方法 | 作用 |
|---|---|
| `ensure()` | 保證 `S.story` 齊備 |
| `evalToken(token, node)` | 單 token → `{ok, reason, soft?, skipped?}` |
| `evalNode(node, opts?)` | AND+ANY（＋可選 node.phase soft）→ `{ok, openable, and, any, reasons, skippedThresholds}` |
| `listOpen(opts?)` | 掃 `STORY_WIRE` 全包 → `{open, locked, done, phase}` |
| `iterNodes()` | `{pack,label,node}[]` |
| `markDone(id)` / `setFlag(k,v)` / `bumpRel(k,δ)` / `setPhase(p)` / `setRoute(k,v)` | 寫進度並 `saveQ` |
| `resolveThreshold(token, node)` | 解析門檻來源 |
| `debugUnlockTangPush()` | playtest：`flag_tang_open` + `rel_tang ≥ 2` |
| `tangFileThreshold()` | 讀 Tang 檔級值（預設 **2**） |

`evalNode`：`openable`＝僅 AND+ANY；`ok`＝再計 node.phase soft（可用 `ignorePhaseSoft`）。

---

## 5. Token 語義

| Token | 判定 |
|---|---|
| `C*`／`R_*`／`A_*` | `S.story.done[id]` |
| `flag_*`／`hiu_*`／`choi_*`／`vera_*` | `S.story.flags`（＋`S.flags` 相容） |
| `route_*` | `S.story.routes` 或同名 flag |
| `phase_P*` | 當前 `S.story.phase` 等級 ≥ 需求 |
| `rel_*_threshold` | `getRel` ≥ 門檻（見 §6） |
| `fame_threshold` | `S.fame` ≥ 門檻；null → skip |
| `season_*`／`era_*` | 年／季**軟**匹配（失敗則該 token 不成立） |

**AND：** `openConditions` 全過（`[]`＝無旗閘）。  
**OR：** 若有 `openConditionsAny`，至少一項；與 AND 同時成立。  
Tang：**不用** `openConditionsAny`。

### Tang 雙閘

| 節點 | openConditions |
|---|---|
| `R_tang_meet` | `[]`（可寫 `flag_tang_open`） |
| `R_tang_push1+` | `flag_tang_open` **AND** `rel_tang_threshold`（**=2**） |

---

## 6. thresholds 政策（playtest）

| 情況 | 行為 |
|---|---|
| `thresholds.rel_tang_threshold = 2`（Tang push+） | **執行** |
| 檔級 Tang `openConditions.rel_tang_threshold` | 節點缺省時回退；再缺省 → **2** |
| 其他 `rel_*_threshold`／`fame_threshold` 為 **null** | **`THRESHOLD_NULL_POLICY = "skip"`**：該 token 視為通過並標 `skipped`（面板 `∅th`） |
| 未寫 `thresholds` | 同 null → skip |

**不**發明 UNLOCK 未給的精確數值；skip 僅供本地原型可列可出，正式數值另輪 playtest 填入。

---

## 7. UI

選單 **「接線資料」** → `showWireDebug()`：

- 載入狀態、通告 high、loc 星河  
- **可出 C／R／A**／未開抽樣／done 數、`rel_tang`、`flag_tang_open`  
- Playtest 鈕：標記 C1、phase→P2、Tang 雙閘、重新評估  

Console：`StoryOC.listOpen()`、`StoryOC.evalNode(node)`。

---

## 8. 驗收步驟

1. HTTP 開本地原型，等 `[WIRING] … ok`。  
2. 選單 → 接線資料：應見「OC_ENGINE_v1」；開局可出含 **C1**、**R_tang_meet**（及若干 meet／`[]` 節）。  
3. 「標記 C1 完成」→ 可出出現 **C2**；C1 進 done。  
4. 「Tang 雙閘」→ `flag_tang_open` + `rel_tang≥2` → **R_tang_push1** 可出。  
5. Console：`StoryOC.evalNode(STORY_WIRE.romance.tang.nodes[1])` 在雙閘前後對比。  
6. 教學／存檔／通告板／beats 路徑仍可用；舊檔繼續遊戲會 `ensure()` 補 `story`。  

自測（2026-11-02 node harness）：C1→C2、Tang meet／push 雙閘、null threshold skip、`listOpen` 通過。

---

## 9. 未做／風險

| 項 | 說明 |
|---|---|
| 劇情播放 UI | 無對白／choices 執行；`flags_written` 不自動套用（選擇支相關） |
| 與 beats 同步 | `B01`… 與 C 節仍雙軌；未把 beat 完成映射為 C done |
| Soft HOLD | stub／Vera 裸旗／Pack3 parallelOk／徐 tier 不修 |
| season 軟閘 | 僅影響含該 token 的 ANY／AND；可能令部份節「季節不對」鎖住 |
| `R_tang_meet_stub` | 仍在 lan_xu 包列出（HOLD） |
| 出圖／1989／publish | 不做 |
| 排他 commit／HE·BE 規則 | 未執行 |

---

---

## 2026-11-03 補丁（tester｜玩家閘）

| 項 | 規格 |
|---|---|
| 玩家 `listOpen`／`StoryPlay.start` | 必須 **`ev.ok`**（含 phase soft）；`openable`  alone 唔夠 |
| stub | 唔入玩家 open（見 PLAN_MAP §9.3） |
| `setPhase` | 跟 **`PHASE_AUTO_TABLE_v1.md`**；唔靠 Playtest |
| Soft | **`SOFT_NITS_FIX_v2.md`** 為準（本檔 §9 Soft HOLD 段過時） |
| 地圖／事態 | `PLAN_MAP_STORY_PROGRESS_v1.md`；gap：`QA_PLAN_GAP_vs_PLAYER_V17N_v1.md` |


*完 — WIRING_OC_ENGINE_v1*
