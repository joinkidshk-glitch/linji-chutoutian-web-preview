# v19z16 — B1 教學 CTA 文案／防漏 + B3 手帳「確定」永不靜默

Branch `fix/playtest-b1-b3-v19z16`. Follows merged B2 (`v19z15` `ensureWeekPlanCommittedForStory`).

## Fix

| # | Issue | Fix |
|---|-------|-----|
| 1 | B1 文案矛盾：教學「去金龍播事態」似會撞「先確定行程」 | B01 CTA 改「去金龍播事態（會用預設行程）」；金句列明雙 CTA：「去金龍…」vs「開始寫手帳」；toast「已用預設行程 · 到金龍…」 |
| 2 | B1 防漏：地點「播事態」未掛 silent commit | `openLoc` tip／listOpen「播事態」click 先 `ensureWeekPlanCommittedForStory()` 再 `StoryPlay.start` |
| 3 | B2 已掛：chip-story／home-story／menu story-play／B01 | **已確認仍在**；home-story toast 同步「已用預設行程」 |
| 4 | B3「確定」全日休息／低風險有時無畫面 | `confirmPlan` **一律**開壓力預覽（唔再低風險直出）；預覽加低風險提示；「確定出發」→ `commitPlanAndGo` |
| 5 | B3 靜默 no-op | `!homeEditable` 時 toast「行程已確定 · 本週無改動可改」；`ensureWeekPlanCommittedForStory` 後 `renderNotebook()` 收埋「確定」掣；confirm 掣 title／aria-label |
| 6 | Cache bust | `?v=19z15` → `?v=19z16` |

**保留**：`StoryPlay.start` 的 `homeEditable` 閘（唔用 `allowDuringPlanner`／唔拆閘）。唔改 soft BehaviorGate parsers／`featureFlag_softBehaviorGatePreview`／`gatePath`。唔 tip LIVE。

## Soft≠PASS

- 唔改 BehaviorGate 解析器或 soft flag 預設
- 唔移除 StoryPlay planner 閘
- Silent commit 仍**唔**呼叫 `runScheduleFromToday`（當日可自由去播事態）

## Wired paths（B1／B2）

| Path | ensureWeekPlanCommittedForStory |
|------|----------------------------------|
| B01「去金龍播事態（會用預設行程）」 | ✓ |
| `#home-story-open` | ✓ |
| `#chip-story` | ✓ |
| menu `story-play` | ✓ |
| loc「播事態」tip／listOpen | ✓ v19z16 |
| `autoPushC1IfNeeded({play:true})` | 故意拒播若 `homeEditable`（保留閘） |
| debug `force:true` | 繞過閘（debug only） |

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z16&softBehaviorGate=1`

1. **新局** → B01 見「去金龍播事態（會用預設行程）」與「開始寫手帳」；撳前者 → toast「已用預設行程…」→ 金龍可播 C1，**唔**再出「請先確定本週行程再播事態」
2. 新局 →「開始寫手帳」→ 填全日休息 → 撳「確定」→ **必出**壓力預覽（含低風險提示）→「確定出發」→「行程已定」並執行
3. 手帳編輯中若經 chip／事態導航 silent commit 後，「確定」應隱藏；若殘留再撳 → toast「行程已確定 · 本週無改動可改」（唔靜默）
4. grep：`會用預設行程`；`confirmPlan` 無 `isLowRiskWeek` early `go()`；`StoryPlay.start` 仍有 `請先確定本週行程再播事態`；helper 內無 `runScheduleFromToday`

## Residual risk

- Silent commit 仍用當前 `planDraft`／預設週程；想自訂應撳「開始寫手帳」。
- 壓力預覽多一步（低風險週以前可直出）；屬刻意統一 CTA。
