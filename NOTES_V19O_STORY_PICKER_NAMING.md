# v19o Soft≠PASS · 出圖 HOLD · 唔 publish

Night QA chrome only (`index.html`). Soft story JSON dialogue beats unchanged. Gigs packs untouched. Soft≠PASS stays. 出圖 HOLD. 唔 publish.

1. SAVE `starVolunteer_map_v19n` → `starVolunteer_map_v19o`.
2. StoryPlay settlement secondary buttons: `劇情列表` → `事態列表` (both `btns.push` after pickChoice settlement).
3. StoryOC missing toast: `劇情尚未載入` → `事態尚未載入`.
4. `storyWeekStamp`: `W4` → `約第4週`, `W4-5` → `約第4–5週`. `pacing.weekMin` / `week_min:` still `約第N週`. Lock meta no longer shows raw `W4-5`.
5. `playOpenPicker` openRows / doneRows: no raw `P1` / `P2`. Open uses `spPlayerMeta` (C1 → `主線 · 1988春`) plus human week stamp. Done prefers `主線 · 1988春 · 已完成`, else `已完成`.
6. `paintStoryEntryHints` calls `scheduleStoryMapRedraw("paintStoryEntryHints")` after chip/badge (fallback `refreshStoryMapTips` + `drawMap`) so 星河「劇」pin `.marks` redraw with the chip. Re-entry guard avoids a redraw loop.
7. Map board mark: `alt="板"` → `alt="通告"`.
