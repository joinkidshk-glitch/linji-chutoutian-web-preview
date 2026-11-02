# WIRING_STORY_PLAY_v1

> **時間：** 2026-11-02（Asia/Hong_Kong）  
> **依據：** `WIRING_OC_ENGINE_v1.md`、`WIRING_INDEX_HOOK_v1.md`  
> **範圍：** 本地原型最小對白／choices 播放＋`flags_written`／effects 寫入；**不出圖**、**不開 1989**、Soft **HOLD**。  
> **Soft≠PASS：** 非正式上線。

---

## 1. 目的

從 `StoryOC.listOpen()` 的可出節點進入播放：逐步顯示 `beats` 對白 → 揀 `choices` → 套用 `effects.flags`／`effects.stats`（含 `rel_*`）→ `markDone`。  
`flags_written` 僅作**候選目錄**；實際只寫所選 choice 的 flags。

---

## 2. 改動檔

| 路徑 | 說明 |
|---|---|
| `index.html` | `StoryOC.applyChoice`／`findNode`；新增 `StoryPlay`；接線面板「播放」；選單「可出劇情」 |
| `index.html.bak-before-story-play` | 套用前備份 |
| `content/WIRING_STORY_PLAY_v1.md` | 本說明 |

---

## 3. API

### `StoryOC` 新增

| 方法 | 作用 |
|---|---|
| `findNode(id)` | → `{pack,label,node}` |
| `findNodeRaw(id)` | → node |
| `applyChoice(node, choice)` | 寫 flags／route／rel／stats 映射、記錄 `S.story.choices`、`markDone` |

### `window.StoryPlay`

| 方法 | 作用 |
|---|---|
| `start(id\|node, {force?})` | 檢查 openable（除非 force）後開播放 modal |
| `advance()`／`skipToChoices()` | 下一句／跳至選項 |
| `pickChoice(choiceId)` | 套用並結算 |
| `playOpenPicker()` | 可出列表 modal |
| `abort()` | 中止（不寫進度） |

---

## 4. effects 映射（最小）

| effects 鍵 | 寫入 |
|---|---|
| `flags[]` `flag_*`／裸前綴 | `StoryOC.setFlag` |
| `flags[]` `route_*` | `StoryOC.setRoute` |
| `stats.rel_*` | `StoryOC.bumpRel` |
| `stats.fame` | `S.fame`（經 `apply`） |
| `stats.craft` | `S.acting` |
| `stats.wealth` | `S.money` += 值×500 |
| `stats.standing` | `S.popularity` |
| 其他 | `S.story.soft[k]` |

`endingId`（若有）→ `S.story.endings`。

**Tang：** meet 選「數據」→ `flag_tang_open`＋`rel_tang+1`；push+ 仍須 `flag_tang_open` ∧ `rel_tang≥2`（引擎不變）。

---

## 5. UI 入口

1. 選單 **接線資料** → 可出列「播放」  
2. 選單 **可出劇情** → picker  
3. Console：`StoryPlay.start('C1')`

播放：modal 內「下一句」／「跳至選項」→ choice 按鈕 → 結算卡。頁尾「中止」不寫入。

---

## 6. 驗收

1. HTTP 開頁，等 wiring fetch。  
2. 接線資料 → 對 **C1** 按播放 → 讀完／跳至選項 → 選「先練班底」→ 結算見 `route_tv`；done 含 C1；可出出現 C2。  
3. 播 **R_tang_meet**（必要時 phase／force playtest）→ 選數據開閘 → `flag_tang_open`、`rel_tang≥1`；再 `bumpRel` 至 2 或再互動 → **R_tang_push1** 可出。  
4. 教學／通告／存檔仍可用；舊檔 `ensure` 補 `choices`／`choiceLog`／`soft`。  

自測（node）：C1 apply、Tang meet→push 雙閘、A_ko_meet flag、StoryPlay advance／skip／pick ✓。

---

## 7. 未做／風險

| 項 | 說明 |
|---|---|
| 立繪／出圖 | 不做；純文字 modal |
| 1989+ 年庫 | 不做 |
| Soft HOLD | stub／Vera 裸旗 rename／parallelOk／徐 tier |
| beats↔章節 UI | 未與 `story_beats` 自動同步 |
| wealth×500 | 粗糙映射，playtest 可調 |
| 多結局／commit 排他 | 只記 `endingId`；不執行平行線降溫 |
| 無 choices 節點 | 稀有；提供「完成節點」後備 |
| `pcSilent` | 不隱藏既有 beats（資料已多半無 PC 對白） |

---

---

## 2026-11-03 補丁（tester｜事態／一屏）

- 玩家入口改稱「**事態**」；接線／Playtest 收 debug。  
- StoryPlay：**一屏無滾**零容忍（翻頁；禁內層 `overflow:auto`）。  
- 結算加玩家 `lockedHint`／下一幕句（PLAN_MAP §4）；禁工程結算詞。  
- Soft → `SOFT_NITS_FIX_v2.md`；地圖 P0 → `PLAN_MAP_STORY_PROGRESS_v1.md`；gap → `QA_PLAN_GAP_vs_PLAYER_V17N_v1.md`。  
- 本檔「Soft HOLD｜stub／Vera…」段：**過時**（v2 已清五項）。


*完 — WIRING_STORY_PLAY_v1*
