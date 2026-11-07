# Playtest remediation notes (v19w → branch `fix/playtest-remediation-v19w`)

依據試玩報告 `docs/FIXES_FROM_PLAYTEST_v1.md`／`臨記出頭天-問題改善具體改法.md` 落實。

## Fixed in this PR

| # | 項目 | 做法摘要 |
|---|------|----------|
| 1 | 入門通告門檻 | `gigs_1988.json` + `gigs_1988_3.2.10-soft.json`：春「初」門檻下調；新增 3 張 `entryTier` 臨記（街景群演／跟組雜務／廣告路人 B）。內嵌 fallback 同步調低《靈異屋邨夜話》《街頭路人》。 |
| 2 | 傳聞拼卡教學卡住 | Soft coach 唔再永久顯示「呢個位仲未啱」；改 click 教學文案；加「跳過教學」；`flags.rumorTutorialDone`；`?skipTutorials=1`。 |
| 3 | 事態可重播 | 地點「播事態」先查 `StoryOC.isDone`；已完成改「事態已完成」；`pruneMapTips` 清已完成 tip。 |
| 4 | 還人情空手還清 | `canRepayHoDebt` + `openHoRepaySheet`：揀債→禮物／現金 $200；禁空手；結果文案放 settle。 |
| 5 | 茶錢 $15 | `moneyCost:15` 實扣；不足拒做；soft 閘錢不夠時標「本次免費」；toast 顯示八卦＋結餘。 |
| 6 | 按鈕劇透 | `choiceHint` vs `resultHint`；按鈕只顯示 choice。 |
| 7 | 熟人文案 | 有事態／情報時唔硬寫「暫時未見熟人」。 |
| 8 | 星河地名 | `tvb_longmen` desc：將軍澳→九龍塘廠房。 |
| 10 | 週結算文案 | `weekGigsDone`／`weekTrainDone`；0 通告用 `WEEK_IDLE`／`WEEK_TRAIN_HEAVY`。 |
| 11 | 通告天數 | 「每週」→「可開工／每週最多」；總天→「通告日數」；total\<weekly 加說明。 |
| 12 | Seal 圖 | `?v=19w` + `onerror` 隱藏。 |
| 13 | rarity 中英 | `rarityLabelZh`：普通／少見／稀有／名貴。 |
| 14 | 空「叮」toast | `toast` 拒空白／純「叮」。 |
| 15 | Day1 人情債 | 開局 `mockDebts=[]`；教學完成後可記 `MOCK_DEBT_TUTORIAL`。 |

## Deferred / partial → 本輪補完

| # | 狀態 |
|---|------|
| 9 訓練結算換行 | **Fixed**：`formatResultNotes()` 每條屬性／壓力／金錢獨立一行。 |
| 16 鎖定事態「播放」 | **Fixed**：未解鎖改灰鈕「事態未解鎖」＋🔒；leave modal 唔再用通告「暫未能報」。 |
| 17 行程日格黏連 | **Fixed**：主行動／hint 分行（`.plan-main`／`.plan-hint`）。 |
| 18 自動推進吞結算 | **Fixed**：`afterDayModal`／`resolvePlannedDay` 一次推進閘，撳「繼續」先跑下一日。 |
| 19 「已練 N 次」 | **Fixed**：地點鈕／結算／手帳報名後即時更新次數。 |
| 20 空白地點側欄 | **Fixed**：`loc-hydrating` skeleton，acts 填完先揭。 |
| 21 Day1 廠景收工對白 | **Fixed**：C1 synopsis／開場線改「才剛起步／剛入行未幾」。 |
| 22 soft 閘 vs 傾談耗日 | **Fixed**：教學／地圖 hint／傾談＋打聽 cost 標籤對齊；打聽標不耗日。 |
| 壓力提示 | **Fixed**：≥60 地圖 tip；≥70 全日訓練確認。 |

## Key files

- `index.html` — 行為／UI
- `content/gigs_1988.json`、`content/gigs_1988_3.2.10-soft.json` — 通告門檻＋入門池
- `content/events_zh_HK.json` — `WEEK_IDLE`／`WEEK_TRAIN_HEAVY`
- `content/MOCK_TUTORIAL_PHASE2_STEPS_5_6_COPY_SOFT_v1.json` — 傳聞教學文案

## Assumptions

- 運行時優先載入 `content/gigs_1988.json`（`refreshCopyPacksFromDisk`）。
- Soft preview `?softBehaviorGate=1` 下，茶錢不足可免扣；還人情無資源時可「預覽記還」。
- 入門通告 `entryTier` 未另做「強制每週補板」邏輯；靠低門檻＋ high boardPriority 自然上板。若 QA 發現仍不足，下一 sprint 再加 refresh 補池。
