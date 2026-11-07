# v20a1 — Freeplay PROGRAM INFRASTRUCTURE

Branch `feat/freeplay-infra-v20a1`. Follows merged v20a0 (`2613f19` / #82).

對齊 `PLAN_vs_v20a0_GAP.md` D 建序：C1–C5 權威、人情債單源、標籤 UX、噂 merge 對表、Soft casting tag 閘、`rosterPlanned`。

Soft≠PASS；唔 tip LIVE；唔發明長對白弧；玩家面禁真藝名。

## What shipped

1. **C1–C5 slots ↔ Soft gate**
   - `STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json` triggers synced to sandbox ecology (C3 rumor+fame, C4 favorMin, C5 rumor+season…).
   - `applyFreeplaySlotsToSoftGate()` overlays slots triggers onto BehaviorGate after stub load; filled `playerFaceLine` / non-placeholder `beats` / choice labels overlay story play.
   - Placeholder「待補」→ keep Soft stub / `story_detail` dialogue.
   - Sandbox file remains DEV mirror / fallback loader.

2. **Favor-debt single source**
   - `seedFreeplayFavorDebt()` merges stub `debts[]`/`hooks[]` into `S.mockDebts` for matching `calendarSeason()`.
   - Empty line → shell placeholder; SEASON_COLLECT stays playable.
   - Tutorial debt behavior unchanged.

3. **Tags UX = Phase2 weak-display**
   - `ensureWeakSeals()` driven by earned `S.castingTags` (registry labels; ~8% opacity).
   - 手帳「標籤」tab hidden unless `?devTags=1` / `localStorage.starVolunteer_devTags=1`.
   - `__freeplay.tags()` kept for DEV.

4. **Soft `canAudition` casting gates**
   - `softCastingTagGate(gig)` reads gig `requiresCastingTagAny` / `blocksCastingTagAny` vs `S.castingTags`.
   - LIVE path unchanged when Soft flag off; missing fields = no-op.

5. **Rumor stub ↔ Phase2 MERGE_PAIRS**
   - Stub fragments include Phase2 pair ids; `mergeGroup`/`phase2PairId` documented.
   - Seed only when `text` non-empty AND season allows.

6. **Schema `rosterPlanned`**
   - 8 planned ids beyond MVP4 (incl. `so_jiyan` art-without-pin HOLD).
   - No new map pins.

## Verify

```js
await __freeplay.load();
__freeplay.check(); // expect ok:true, infra:"v20a1"
```

Checks: slots_wire / favorDebt_seed / weak_seals_tags / soft_tag_gate / rosterPlanned≥8 / total≥12 / nextHint hidden.

## Preview

`?v=20a1&softBehaviorGate=1`

## Content bot edit now

- `content/STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json` → playerFaceLine / beats.lines / choices.label  
- `content/STUB_RUMOR_FRAGMENTS_v1.json` → text  
- `content/STUB_FAVOR_DEBT_SEASON_v1.json` → line / title  
- optional: `STUB_ERA_STARS_MVP_v1.json` short lines; gig JSON Soft tag gates  

See `docs/CONTENT_CONTRACT.md`.

## HOLD left

出圖／長互動／C6–C17／89–92／LIVE tip／齊鎮海上地圖／`so_jiyan` map pin／催收罰鎖。

## Pointer

`NOTES_V20A_FRAMEWORK.md` = v20a0 shell notes；**以本檔 v20a1 為準**。
