> Soft≠PASS｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜SAVE `starVolunteer_map_v19w`｜`?v=` 唔抬（而家產品版仍 `20a10`）

## Soft QA 必用網址（index 快取）

GitHub Pages 對 HTML 送 `Cache-Control: max-age=600`。試玩箱瀏覽器又會按**完整 URL**持久快取文件。只開 `?v=20a10&softBehaviorGate=1` 會繼續執行 tip 之前嘅 `index.html`（教學去金龍、chrome 標主線），即使 origin sha 已係新檔。

**每次 Soft tip 改完 index，Soft 抽樣必須用下面這條（`softRev` 跟 head 腳本 `SOFT_REV`，而家 `s107`）：**

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=20a10&softBehaviorGate=1&softRev=s107`

唔好改 SAVE `starVolunteer_map_v19w`。唔好把 `?v=20a10` 抬去 `20a11`。新局請開新分頁打呢條，唔好按舊分頁重新整理。`<html data-soft-rev="s107">` 先算載到今次 index。

# Soft feature-flag 合流

Soft 同未來 LIVE tip 共用**一套開關**。本包只對齊模型同薄接線。唔退休 LIVE 週數閘。

## 兩個名字，一個決策點

| 名字 | 角色 | 而家 |
|---|---|---|
| `BehaviorGate.featureFlag_softBehaviorGatePreview()` | Soft 行為閘路徑（opt-in）。**唯一**解析 `?softBehaviorGate=1`／`?softPreview=1`／`localStorage starVolunteer_softBehaviorGatePreview=1` | 預設 `false` |
| `BehaviorGate.gatePath()` | 共用路徑名。只呼叫上面個旗：`"soft"` 或 `"live"`。唔再讀 URL／localStorage | 跟旗 |
| `BehaviorGate.liveWeekGateStillActive()` | LIVE 週數閘哨兵。預設權威，直至**明示 tip LIVE** | runtime **永遠 `true`** |

`StoryOC.evalNode` 用 `gatePath()==="soft"` 先入 stub。否則 fall through 到 `openConditions`／`pacing.weekMin`。

## 路徑

- **Soft on**（`?v=19w&softBehaviorGate=1`，可加 `softSeed`）：C1–C5，加上已掛嘅 Deng／雙女／seed／chrome 守衛，只認 stub `nodes[].trigger` 同 `engineSlice.evalOrder`。決策點仍然係 `featureFlag_softBehaviorGatePreview`（`gatePath` 只係轉呼叫）。
- **Soft off／非 Soft**：只認 week-gate。`softSeed` 唔注入（`softSeedRecord` 見 `gatePath()!=="soft"` 即返回 null）。
- **tip 前**：stub／slice `liveWeekGateStillActive:true`、`tipForbidden:true`。`selfCheck` 仍要求 `liveWeekGateStillActive()===true`（`live_fn`）。Soft 路徑開住都唔可以令哨兵變 false。

ENGINE_SLICE §6「tip 前唔合流」仍然成立：指**唔退休** LIVE week-gate、唔 tip LIVE。本包合流嘅係開關模型，唔係把 LIVE 哨兵關掉。

## 硬禁

- 唔好把 `liveWeekGateStillActive()` 改成 `return false`，亦唔好刪 LIVE week-gate 碼。
- 唔好把 stub／slice `liveWeekGateStillActive` 或 `tipForbidden` 改 false。
- 唔好喺 `featureFlag_softBehaviorGatePreview` 之外再解析同一組 query／localStorage。
- 唔好抬 `?v=`／SAVE、唔好 tip LIVE、唔好改 89–92、唔好出圖、唔好改已鎖 trigger 數值／choice／flags id。

## 抽樣

`?v=19w&softBehaviorGate=1`（可加 `&softSeed=seed_hiu_meet_ready`）。無關旗：`?v=19w` 仍行 week-gate。主控台 `__behaviorGate.selfCheck()` 應 OK，而且 `liveWeekGateStillActive()` 仍 true。

對照：`PLAN_OUTSTANDING_SOFT_NEXT_v2.md` #8、`PLAN_STORY_BEHAVIOR_GATE_FULL_ALIGN_SOFT_v1.md` §3。

## 教學 Phase2 `behaviorGate` 標記（唔係合流缺口）

`TUTORIAL_PHASE2_SOFT_NITS.behaviorGate`＝`"not_bound"`：教學 Phase2 Soft 唔強制綁 BehaviorGate C stubs，亦唔把教學步接到 C 閘。呢個字串唔係 feature-flag 合流未做（合流已 Done Soft，#17 `5ebf08c4`；`gatePath()` 仍單開關）。教學步 5–6 已 Done Soft：copy #23 `8a63e477`、FX #24 `ff1d5eed`（`artHold:false`）。Soft≠PASS｜唔 tip LIVE。
