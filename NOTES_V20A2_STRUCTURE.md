# NOTES · Freeplay v20a2 STRUCTURE

> **時間：** 2026-11-07（Asia/Hong_Kong）  
> **狀態：** Soft≠PASS；結構／功能殼；**唔 tip LIVE**；**唔發明長對白**  
> **預覽：** `?v=20a2&softBehaviorGate=1`  
> **契約：** `docs/CONTENT_CONTRACT.md`

## 本輪加咗咩

1. **C6–C17 Freeplay slots**
   - `content/STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json` 擴到 C1–C17（對白仍係「待補」）。
   - Soft：`BehaviorGate.applyFreeplaySlots` 會 **create** 缺席嘅 C6–C17 stub node（sandbox 仍只載 C1–C5）。
   - `coversNode` 擴到 `C1–C17`。
   - Trigger 生態殼：weekMin／loc／needDone／rumor／favor／season／gigCount／relAny／tag（框架擁有；內容 bot 預設唔改）。

2. **名冊遠觀殼（無長互動）**
   - MVP4 之外：`mak_zhendong`／`lok_gasing`／`pang_siuki`／`chung_choning`／`gu_mingfai`／**`so_jiyan`** 入 `STAR_SIGHTINGS`＋stub。
   - 各地點釘在既有 hub（唔開新地圖）：`film_cotton`／`tvb_longmen`／`ad_central`／`rec_star`／`tvb_harbour`／**`rec_wanchai`（蘇芷茵）**。
   - `chai_zanhoi`／`placeholder_era_08` **HOLD 唔上地圖**。
   - Soft `phase3Stars()` = MVP4 mock overlay **＋** 其餘 STAR_SIGHTINGS。

3. **業內信用 Soft 試鏡因子**
   - `softIndustryCreditGate(gig)`：通告有 `industryCreditMin` 先閘；缺欄＝no-op。
   - 接 `canAudition`／`gateShortReason`／`reqHtml`（Soft path）。

4. **催收罰鎖**
   - `softOverdueFavorDebtLock()`：只鎖 **`已逾期`**；教學債 `未到期` 唔鎖。
   - 清數後狀態非逾期 → 自動放行。

5. **era bust preferFile**
   - StoryPlay `SP_ERA_STEM`：`luk_baakyin`／`liu_bingxing`／`ngai_wingnaam`／`yip_manji`／`so_jiyan` 優先 `assets/story/era_stars/{id}_bust_*.png`。
   - 遠觀剪影仍用 `eraSilhouetteFarSrc`（含 so_jiyan）。

## Verify

```js
await __freeplay.load();
__freeplay.check(); // ok:true, infra:"v20a2", slotsCount:17, soJiyan:true
__freeplay.softIndustryCreditGate({ industryCreditMin: 99 });
__freeplay.softOverdueFavorDebtLock({});
```

## HOLD（刻意）

- LIVE tip／抬 SAVE／89–92  
- 31 人 LOOKS 出圖；紅星長互動／romance 樹  
- 齊鎮海上地圖；填晒 C1–C17 粵語長對白（交內容 bot）
