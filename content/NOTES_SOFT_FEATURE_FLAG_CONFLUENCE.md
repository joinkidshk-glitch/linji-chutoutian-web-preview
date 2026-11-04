> Soft≠PASS｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜SAVE `starVolunteer_map_v19w`｜`?v=19w` 唔抬

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
