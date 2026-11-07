# v19z2 — story location action label + repay align

Branch `fix/playtest-story-label-v19z2`. Official Pages smoke after v19z1 still showed `播事態：先學做動作戲／先賺／免費` on 金龍茶餐廳 after C1 was done (re-click → `這幕已完成`). Map tip prune was fine; **location action builder** was not.

## Fixes

| # | Bug | Fix |
|---|-----|-----|
| 1 | Completed incident still listed as `播事態…／免費` | Unified `locStoryIsDone` (`StoryOC.isDone` **and** `S.story.done`). Tip + `listOpen` paths never emit playable `播事態` when done. Done-at-loc → disabled gray **`事態已完成`** (cost `—`, not `免費`). Click-guard re-checks before `StoryPlay.start`. |
| 2 | `#modal-inner` leftover 劇情結算 + `story-play-on` | `closeModal` clears `#modal-inner` / `#modal-btns` HTML and removes `story-play-on`. |
| 3 | Journal shows 何生春季數 but 還人情 says 無欠 | `hoDebtsForRepay()` merges `mockDebts` + current-season `SEASON_COLLECT` 何生 cards (creditor **or** `creditorLabel`). Cleared season cards stored in `S.mockSeasonCleared` and hidden from journal. |

## Action builder contract (isDone)

For every location sheet:

1. If tip/`listOpen.open` node `locStoryIsDone(id)` → **do not** add `播事態：…`.
2. Optional: show disabled `事態已完成：{title}`.
3. Only undoned matching nodes get `播事態：…／免費`.
4. `refreshStoryMapTips` skips **all** done ids (not only C1).

## Cache

`?v=19z1` → `?v=19z2`.

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z2&softBehaviorGate=1`

1. Finish C1 at 金龍茶餐廳 → 回地圖 → reopen → **no** `播事態` actionable label (gray `事態已完成` OK).
2. 回地圖 after 劇情結算 → no leftover settlement HTML / stuck mask.
3. Journal 何生春季數 → 事務所「還人情」lists that debt (not `而家無欠何生人情`).
