# QA｜WIRING_STORY_PLAY_v1 靜態碼覆測（STATIC｜browser 待併）

> **範圍：** `content/WIRING_STORY_PLAY_v1.md`＋`index.html` vs `index.html.bak-before-story-play`。  
> **對照：** `WIRING_OC_ENGINE_v1.md`、`QA_WIRING_OC_ENGINE_v1.md`、`story_detail_romance_tang.json` v1.2、`story_detail_c1_to_c17.json` v1.1。  
> **方法：** grep／Read／diff／JSON 抽樣；**NOT browser**（HTTP／Console／modal 點擊另輪併）。  
> **規則：** Soft≠PASS・唔 publish；本輪 QA **未改** content／index。  
> **時間：** 2026-11-02 23:57（Asia/Hong_Kong）

---

## Overall：**PASS with nits**（STATIC）

| 層 | 結果 |
|---|---|
| `window.StoryPlay` API（start／advance／skipToChoices／pickChoice／playOpenPicker／abort） | **PASS**（均在碼內並掛窗） |
| `StoryOC.applyChoice`／`findNode`／`findNodeRaw` | **PASS** |
| 選單「可出劇情」＋接線面板「播放」 | **PASS**（靜態入口在碼） |
| effects 映射（flags／route／rel／stats→fame・acting・money×500・popularity／soft） | **PASS**（碼內） |
| Tang meet 數據→`flag_tang_open`＋`rel_tang+1`；push 雙閘仍靠 OC | **PASS**（JSON＋碼同向） |
| `flags_written` 僅候選目錄（不自動套用） | **PASS** |
| Soft HOLD；出圖／1989 未做 | **PASS** |
| Browser 驗收（文檔 §6 HTTP／C1／Tang 路徑） | **PENDING**（本輪不做） |
| Soft remaining／文件 nits | **NIT**（不升 FAIL） |

**出圖仍暫緩。** Soft leftover **仍 HOLD**。本輪 **唔 publish**。Browser 待併。

---

## 1. Diff 範圍（bak → index）

| 項 | 結果 |
|---|---|
| `index.html.bak-before-story-play` | 存在；**無** `StoryPlay`／`applyChoice`／`wire-play`／選單 `story-play` |
| `index.html` | +~339／−~11 行量級；新增 CSS `.story-play`；`StoryOC` 擴充 `findNode`／`findNodeRaw`／`applyChoice`；`ensure` 補 `choices`／`choiceLog`／`soft`；新增 `StoryPlay` IIFE；接線面板「播放」＋選單「可出劇情」 |
| 出圖／1989／art pipeline | diff **無**相關改動（`1989`／`GenerateImage`／出圖關鍵字 +0） |
| Soft leftover JSON | **未改**（mtime／內容仍見 stub／Pack3 `parallelOk`／徐 `tier=阻力`） |

---

## 2. `window.StoryPlay` API

文檔 §3 所列方法均在碼內匯出並掛 `window.StoryPlay`：

| 方法 | 在碼 | 行為摘要（靜態） |
|---|---|---|
| `start(id\|node, {force?})` | ✓ | `findNode`；非 force 時 `isDone`／`evalNode.openable` 閘；開 modal |
| `advance()` | ✓ | beats 內下一句／下一 beat；完則 `mode=choices` |
| `skipToChoices()` | ✓ | 直接 `mode=choices` |
| `pickChoice(choiceId)` | ✓ | 找 choice → `StoryOC.applyChoice` → 結算卡；清 `_sess` |
| `playOpenPicker()` | ✓ | `listOpen` → modal 列「播放」 |
| `abort()` | ✓ | `_sess=null`（中止鈕／dismiss；**不**寫進度） |
| `session` getter | ✓（額外） | 除錯用 |

無 choices 時後備「完成節點」→ fake choice + `applyChoice`（文檔 §7 風險項屬實）。

---

## 3. `StoryOC` 新增

| 方法 | 在碼 |
|---|---|
| `findNode(id)` → `{pack,label,node}` | ✓ |
| `findNodeRaw(id)` → node | ✓ |
| `applyChoice(node, choice)` | ✓：flags／`route_*`／`rel_*`／stats 映射／`choices`＋`choiceLog`／`endingId`／`markDone`／`saveQ` |

`ensure()` 相對 bak **新增**補齊：`st.choices`／`st.choiceLog`／`st.soft`（對齊文檔「舊檔 ensure 補」）。`endings` 僅在有 `endingId` 時 lazy 建立。

---

## 4. effects 映射（碼 ↔ 文檔 §4）

| effects 鍵 | 碼路徑 | 結果 |
|---|---|---|
| `flags[]` `flag_*`／裸前綴 | `setFlag` | ✓ |
| `flags[]` `route_*` | `setRoute` | ✓ |
| `stats.rel_*` | `bumpRel` | ✓ |
| `stats.fame` | `apply`→`S.fame` | ✓ |
| `stats.craft` | →`acting` | ✓ |
| `stats.wealth` | →`money` += 值×500 | ✓（粗糙；文檔已標） |
| `stats.standing` | →`popularity` | ✓ |
| 其他 | `S.story.soft[k]` | ✓ |
| `endingId` | `S.story.endings` | ✓ |

**`flags_written`：** `index.html` 僅 2 處字串（`applyChoice` 註解＋結算卡說明）；**零**讀 JSON `flags_written` 自動寫入。實際只寫 `choice.effects.flags`。✓

---

## 5. Tang／C1 數據同向（靜態）

| 路徑 | JSON | 播放／引擎 |
|---|---|---|
| `R_tang_meet` 選「數據」`C_tang_meet_data` | `effects.flags=['flag_tang_open']`，`stats.rel_tang=1` | `applyChoice` 會寫開閘＋rel；與文檔 §4 Tang 一致 |
| `R_tang_meet` `openConditions=[]` | ✓ | 開局可出仍靠 OC；播放器不另開閘 |
| `R_tang_push1` | AND=`[flag_tang_open, rel_tang_threshold]`；`thresholds.rel_tang_threshold=2` | **雙閘仍由 `StoryOC.evalNode`**；播放器不繞過 |
| C1 選「先練班底」 | `route_tv`＋`craft:1` | 結算應見 route／craft→acting（browser 待證） |
| C2 | `openConditions=['C1']` | markDone(C1) 後 listOpen 可出（browser 待證） |

---

## 6. UI 入口（靜態）

| 入口 | 證據 |
|---|---|
| 選單 **可出劇情** | `data-m="story-play"` → `StoryPlay.playOpenPicker()` |
| 接線資料可出列 **播放** | `showWireDebug` `lisOpen`＋`data-play` → `StoryPlay.start`；標 **STORY_PLAY_v1** |
| Playtest「可出列表」 | `data-wire="picker"` → `playOpenPicker` |
| Console | 面板文案提示 `StoryPlay.start('C1')` |

**Browser 實際播 C1／Tang 路徑：本輪未跑 → PENDING。**

---

## 7. Soft HOLD／未做（同向）

| 項 | 現況 |
|---|---|
| Soft HOLD（stub `flags_written` 仍含 `flag_tang_open`；Pack3 ending／多節 `parallelOk:true`；徐 cast `tier=阻力`） | **仍在**；本 patch **未清** |
| 立繪／出圖 | 不做；純文字 modal；**暫緩** |
| 1989+ | 不做 |
| 對白↔`story_beats` 自動同步／多結局排他 | 未做（文檔 §7） |

---

## 8. Nits（不升 FAIL）

1. **Browser PENDING**：文檔 §6（HTTP、C1→route_tv→C2、Tang meet→push1）未在本輪執行；Verdict 僅 STATIC。  
2. Soft leftover **仍 HOLD** — 預期。  
3. `fresh().story` 形狀仍為 `{done,flags,rel,routes,phase}`；`choices`／`choiceLog`／`soft` 靠 `ensure` 補（功能 OK；形狀微不一致）。`endings` 未在 ensure 預建。  
4. 自測 harness「C1 apply、Tang 雙閘」文檔聲稱 ✓ — 本輪未重跑 harness；以碼／JSON 對表為準。  
5. `wealth×500` 粗糙映射 — 文檔已標風險。

---

## 9. 結論

**STATIC PASS with nits。** `StoryPlay` 六法＋`applyChoice`／`findNode(Raw)`／雙入口 **均在碼內**；effects 映射與 Tang meet 數據／OC 雙閘同向；`flags_written` 僅候選；Soft HOLD；**出圖仍暫緩**。併 browser 後可升完整 Verdict。

*完 — QA_WIRING_STORY_PLAY_v1（STATIC）*
