# v19z6 — playtest improve（v19z5 再試玩清單）

Branch `fix/playtest-improve-v19z6`. Implements P0–P2 from 《臨記出頭天-v19z5-再試玩改善方向》.

## Fixes

| # | Pri | Issue | Fix |
|---|-----|-------|-----|
| 1 | P0 | 送禮結果洩漏 `rel_hiu` | `doGiveGift` 結果只顯示「好感 ±N」，唔再 append `relKey` |
| 2 | P1 | softGate 送禮確認寫「會用去 1 日」 | `giftConfirmCostLine`／`giftHintLabel`：閘開 →「不耗日 · 只用今日送禮次數」；list／確認 modal 共用 |
| 3 | P1 | reward／條件字串黐埋 | gap spans `display:block`；`lab 差 N` 加空格；獲聘 notes 改 `formatResultNotes` |
| 4 | P1 | 手帳「返地圖」實際過日 | 強制行程日標籤改「繼續行程」；自由日「返大地圖」 |
| 5 | P2 | 地點 sheet 擋選單 | `.menu` z-index 25→45；開 ☰ 時 `closeSheet()` |
| 6 | P2 | 庫存空夾英文 | 「地點選單」「熟人／可培養對象」 |
| 7 | P2 | 金龍打聽／飲茶可連刷 | `mockAskAlreadyHeard` 鎖已聽；飲茶每日上限 2（`softTeaUsed`）；UI 標「已聽過／今日已滿」 |
| 8 | P2 | 林曉晴首次傾談過短 | `hiu_talk_first_done`：寒暄 → 2 選 → 再入情報結果（其後傾談維持短版） |
| 9 | P2 | 幕前聲量 vs 聲望 | `STAT_LABEL.fame`→「幕前聲量」；差幾多／門檻／jump 文案跟標籤 |
| 10 | P2 | 拼合後人情債 toast 易誤解 | JSON `favorDebtSettleLine` 標明教學債＋「唔係拼合生出嚟」；modal 加副句 |

## Cache

`?v=19z5` → `?v=19z6`

## Deferred

- EVENTS_ZH_HK／殺青旁白仍有「聲望／人氣」flavor（非頂欄／狀態主標）；未全面改寫劇情字串
- 林曉晴首次傾談加長只做 map `doTalk` 路徑；正式 Romance meet（`R_hiu_meet`）內容未動

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z6&softBehaviorGate=1`

1. 傾談林曉晴 → 送禮 → 結果無 `rel_*`
2. softGate 確認送禮文案＝不耗日／今日次數
3. 鎖通告「差幾多」各條件分行；獲聘數值唔黐埋
4. 手帳有強制行程時掣＝「繼續行程」；自由日＝「返大地圖」
5. 開住地點 sheet 撳 ☰ → sheet 收起，選單可撳
6. 庫存空文案無 `sheet`／`romance`
7. 金龍同一打聽第二次＝已聽過；飲茶每日最多 2
8. 林曉晴首次傾談有選擇枝
9. 頂欄／狀態／差幾多統一「幕前聲量」
10. 拼合成功人情債提示標明教學來源
