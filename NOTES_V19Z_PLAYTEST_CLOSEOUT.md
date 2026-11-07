# Playtest closeout notes (v19z → branch `fix/playtest-closeout-v19z`)

承接 `NOTES_V19Y_PLAYTEST_POLISH.md` 剩餘項：soft 社交耗日一致性、「差幾多達標」訓練捷徑、入場通告變奏、內嵌 fallback 完整性。本輪一次收完並上正式 Pages（`main`）。

## Closed

| # | 項目 | 做法 |
|---|------|------|
| 1 | Soft 閘社交耗日 | 新增 `softSocialCostsDay()`（`softTalkCostsDay` 仍係 alias）。**soft**：傾談＋romance **送禮** 不耗日（唔寫行程／唔 `tickDay`）；標籤／結算／教學／地圖 hint 對齊。**live**：傾談／送禮仍 +1 日。**兩邊都耗日**：訓練、休息、試鏡、拍攝、手帳「咖啡店駐場小表演」`cafe_gig`。茶餐廳 `$15` 等 **moneyCost 仍可扣費**（錢唔夠時 soft 預覽可免茶錢，沿用 v19w）。 |
| 2 | 「差幾多達標」→ 訓練 | 鎖定通告 Detail：顯示缺口摘要；主按鈕 `btn_train_jump` 跳去最佳訓練地（或已報名則入手帳訓練頁）。Mobile：按鈕 `width:100%`／`min-height:44px`。 |
| 3 | 入場通告變奏 | 新增 3 張 entry：`gig_1988_entry_ferry_crowd`（天星碼頭）、`gig_1988_entry_print_hand`（報紙夾頁手模）、`gig_1988_entry_rec_clap`（錄音室拍板）。同步 `ENTRY_GIGS_1988`、`content/gigs_1988.json`、`content/gigs_1988_3.2.10-soft.json`。入場池合共 **6** 張。 |
| 4 | 內嵌 GIGS fallback | `mergeEntryGigsIntoPool` 加強：`clampEntryReqToTemplate` 把 disk／內嵌已有入場 req **夾低至模板**；缺 id 則整張補入。`refreshCopyPacksFromDisk` 喺 `syncGigsForCalendarYear` 後再 merge 一次。disk 失敗時內嵌 + ENTRY 仍可提供入場板。 |
| 5 | Cache | 資產／UI `?v=19y` → `?v=19z`。 |

## Live vs soft（日耗）

| 行動 | live | soft（`?softBehaviorGate=1`） |
|------|------|-------------------------------|
| 通告欄／打聽／茶座 mock 打聽 | 不耗日 | 不耗日 |
| 傾談 | +1 日 | 不耗日 |
| 送禮（romance） | +1 日 | 不耗日 |
| 茶錢 `$15` 等 | 扣錢 | 錢夠扣；唔夠可免（預覽） |
| 訓練／休息／試鏡／拍攝 | +1 日 | +1 日 |
| 手帳街頭／Cafe 表演 | +1 日 | +1 日 |

## Intentional / out of scope

- 第 5 週起且 fame≥16：**唔再**強制補入場板（`needsEntryBoardFill` 維持）。
- 無 githack／非官方預覽依賴；只合正式 GitHub Pages（`main`）。

## Key files

- `index.html` — soft 社交、訓練捷徑、ENTRY×6、merge clamp、cache `?v=19z`
- `content/gigs_1988.json`、`content/gigs_1988_3.2.10-soft.json` — +3 entry
- `NOTES_V19Z_PLAYTEST_CLOSEOUT.md` — 本檔

## Verify

正式站：`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z&softBehaviorGate=1`（硬重整）。查：鎖定通告有「去練…」；soft 送禮結算寫「不耗日」；開局板面入場變奏多過三張。
