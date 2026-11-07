# v19z8 — playtest UX rest（v19z7 deferred）

Branch `fix/playtest-ux-v19z7` (updates PR #58). Closes deferred items from NOTES_V19Z7 / UX report.

## Fixes

| # | Pri | Issue | Fix |
|---|-----|-------|-----|
| 1 | P1 | 通告詳情資訊過密 | `castingNoticeDetailHtml` 預設 **摘要**（片酬／日數／期間／差幾多）；「顯示詳細」展開條件表、違約、限制、導演、劇情。`wireGigCardSynToggles` 綁 `data-cn-toggle` |
| 2 | P1 | 一週連點「繼續」疲勞 | `resolveWeekRemaining`／`beginWeekAccel`／`countRemainingAutoDays`；日結／手帳結果加「加速本週剩餘」；合併休息／表演／訓練／中段拍攝；**停**喺殺青（wrap）、試鏡／job、週結；結束出摘要卡 |
| 3 | P1 | 桌面 900px+ 兩側留白 | `#desktop-rail` 操作提示；`@media (min-width:900px)` 放大 phone frame（≈468×960）；&lt;900／手機 390 不變 |
| 4 | P1 | 新遊戲原生 `confirm` | `startNew` → 應用內 modal：週數／存款／幕前聲量摘要＋「覆蓋開新局／取消」；本體入 `startNewFresh` |
| 5 | P2 | 人情債「去還」路徑長 | `renderDebtPane` 一鍵 `openHoRepaySheet`（唔再繞地圖） |
| 6 | P2 | 訓練報名後加練提示弱 | 第一堂 foot＋「入手帳排加練」extraBtn（開手帳訓練分類） |
| 7 | P3 | 遠觀 cost「無」含糊 | 改「僅遠望 · 無互動」 |

## Cache

`?v=19z7` → `?v=19z8`

## Soft≠PASS

- 唔改 `featureFlag_softBehaviorGatePreview`／`gatePath`
- 加速只合併非關鍵自動日；唔 tip LIVE week-gate

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z8&softBehaviorGate=1`

1. 通告詳情：先見摘要；撳「顯示詳細」先見條件表／劇情；再收起
2. 週中非關鍵日結：有「加速本週剩餘」→ 摘要合併；殺青日仍單獨停
3. 桌面 ≥900px：左／側欄有操作提示，手機框略大；手機闊度仍正常
4. 有存檔撳「新遊戲」→ 應用內 modal 顯示週／存款／聲量，無瀏覽器 confirm
5. 人情債「去還」→ 直接還款選項
6. 首次報名訓練 →「入手帳排加練」
7. 遠觀行動 cost＝「僅遠望 · 無互動」

## Leftovers（刻意未做）

- 多存檔槽、完整設定頁（音量／文字速度）
- 教學步數大幅刪減（已有跳過）
- 通告成功率浮動原因長文、人情倒數日 badge
