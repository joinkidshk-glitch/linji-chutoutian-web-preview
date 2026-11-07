# Playtest polish notes (v19y → branch `fix/playtest-polish-v19y`)

承接 `NOTES_V19X_PLAYTEST_FIXES.md` Assumptions：入場通告未做強制補板；soft 閘傾談標籤已對齊但仍耗日。本輪補完。

## Fixed

| # | 項目 | 做法 |
|---|------|------|
| A | 強制入場通告補板 | `ensureEntryTierBoardFill()`：第 1–4 週或聲望 &lt;16 時，保證全域板面最少 **2** 張可報 `entryTier`；不足則由入場池 `unshift` 到對應 loc 板，並 `known`。掛勾：`doScout`／`openLoc`／`advanceDay`／`startNew`／`cont`。 |
| B | 內嵌 GIGS fallback 同步 | 新增 `ENTRY_GIGS_1988`（三張入場：街景群演／跟組雜務／廣告路人 B）；`mergeEntryGigsIntoPool()` 喺 boot、`syncGigsForCalendarYear(1988)` 補入／對齊 `entryTier`＋低門檻。disk `gigs_1988.json` 仍優先。 |
| C | 入場門檻開局可報 | 入場 req 對齊 `fresh()`：路人 B looks22／charm16；街景 acting15；跟組仍無 req → 開局即可報 ≥2。 |
| D | Soft 閘傾談不耗日 | `softTalkCostsDay()`：soft → 唔 `writeTodayPlan`、唔 `tickDay`；cost／hint／結算腳註改「不耗日」。訓練／試鏡／休息／送禮／茶錢路徑不變。 |
| E | 文案對齊 | 開場／地圖 hint／`paintBar` help／教學 TUT_NPC：soft 傾談免費；live 傾談 +1 日。 |
| F | Cache bust | 資產 `?v=19w` → `?v=19y`（seal／物理 UI／地圖底等）。 |

## Key files

- `index.html` — ENTRY 常數、補板、soft 傾談、文案、cache
- `content/gigs_1988.json`、`content/gigs_1988_3.2.10-soft.json` — 入場 req 微調
- `NOTES_V19Y_PLAYTEST_POLISH.md` — 本檔

## Assumptions / risks

- 正式站 Pages 跟 `main`；測 `?v=19y&softBehaviorGate=1` 並硬重整。
- 中後期（週&gt;4 且 fame≥16）唔再強制補入場，避免壓過中高階板。
- Soft 傾談免費只限 `doTalk`；`cafe_gig` 行程表演、送禮仍耗日。
- 若 `gigs_1988.json` fetch 失敗，內嵌 + `ENTRY_GIGS_1988` merge 仍可提供三張入場。
