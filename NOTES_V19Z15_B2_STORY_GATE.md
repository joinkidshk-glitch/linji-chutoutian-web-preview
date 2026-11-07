# v19z15 — B2 開局事態卡死（homeEditable × 去金龍）

Branch `fix/playtest-b2-story-gate-v19z15`. Playtest High bug：教學／B01 CTA「去金龍播事態」開地圖＋`openLoc("cafe_cha")` 時，`S.homeEditable` 仍為 true（新局 `enterHome(null, true)`）。之後喺金龍開 C1 會撞 `StoryPlay.start` 閘：

```
if(S.homeEditable && !opts.allowDuringPlanner && !opts.force){
  toast("請先確定本週行程再播事態");
  return false;
}
```

玩家若先入「到處逛逛」日，手帳變唯讀，更難回頭確定 → 事態 badge 可卡到第 8 週。

## Fix

| # | Issue | Fix |
|---|-------|-----|
| 1 | B2 CTA 未提交行程就去金龍 | 新增 `ensureWeekPlanCommittedForStory()`：有 `planDraft`／`defaultWeekPlan` → scrub／lock shoots → `S.weekPlan` → `homeEditable=false` → `paintBar`／`saveQ`；**唔**呼叫 `runScheduleFromToday()`（當日仍可自由去金龍播 C1） |
| 2 | B01「去金龍播事態」 | CTA 先 silent commit，再 `show(v-map)`／`openLoc("cafe_cha")`；toast「行程已定 · 到金龍可播開局事態」（已確定則沿用舊 toast） |
| 3 | 同牆：`home-story-open`／chip-story／menu `story-play` | 開導航或 `playOpenPicker` 前同樣 call helper |
| 4 | Cache bust | `?v=19z14` → `?v=19z15` |

**保留**：`StoryPlay.start` 的 `homeEditable` 閘（v19z12 防手帳期間誤播／自動播）。唔改 soft BehaviorGate parsers。

C1 已完成時 B01 本來就不顯示「去金龍播事態」（`StoryOC.isDone("C1")`）。

## Soft≠PASS

- 唔改 `featureFlag_softBehaviorGatePreview`／`gatePath`
- 唔 tip LIVE
- 唔移除 StoryPlay planner 閘

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z15&softBehaviorGate=1`

本地／Pages：

1. **新局** → 教學完 → B01「去金龍播事態」→ toast「行程已定 · 到金龍…」；頂欄事態／金龍可播 C1；**唔**應再出「請先確定本週行程再播事態」
2. 播完 C1 後事態 badge 應降（唔再永久 =1）
3. 手帳已確定後再撳「去金龍」→ 只導航，唔重複燒週程（helper no-op）
4. 未撳 CTA、仍喺手帳編輯 → 其他自動播路徑仍被 StoryPlay 閘擋住
5. grep：`ensureWeekPlanCommittedForStory` 存在；helper 內無 `runScheduleFromToday`；`StoryPlay.start` 仍有 `請先確定本週行程再播事態`

## Residual risk

- Silent commit 用當前 `planDraft`／預設週程；玩家若想先改手帳再去金龍，應撳「開始寫手帳」而非「去金龍」。
- 其他未掛 helper 的直接 `StoryPlay.start`／`openLoc` 路徑若在 `homeEditable` 下仍可能撞閘（預期：保留閘）。
