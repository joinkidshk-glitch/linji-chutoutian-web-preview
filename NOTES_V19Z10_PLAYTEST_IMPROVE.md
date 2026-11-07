# v19z10 — playtest improve（v19z9 再試玩清單）

Branch `fix/playtest-improve-v19z10`. Implements P0–P2 from《臨記出頭天-v19z9-再試玩改善方向》.

## Fixes

| # | Pri | Issue | Fix |
|---|-----|-------|-----|
| 1 | P0 | 地圖／外層 HUD 存款不同步 | 地圖 dual-hud 加 `#c-money`；`refreshMoneyHud()` 統一地圖頂＋手帳頂；`apply()`／小賣／茶錢／還債後強制 refresh |
| 2 | P0 | 現金還何生清債不扣款 | 還款原子：先 `apply({money:-200})`＋HUD，成功先 clear；失敗明示「債項未清」 |
| 3 | P0 | 老張「去還」錯綁何生 | `openDebtRepaySheet(debtId)`；`allDebtsForRepay`；唔 fallback 已清何生 |
| 4 | P1 | 開局「先看事態」誤導 | CTA「去金龍播事態」／「去現場播事態」導航至地點；标明到現場先可播 |
| 5 | P1 | 選單「返屋企」偷耗日 | 拆「返手帳（不耗日）」／「今日提早休息（+1日）」＋二次確認 |
| 6 | P1 | 關通告欄掏空地點面板 | `doScout` `onDismiss`／關閉 → `openLoc` 恢復 |
| 7 | P2 | 新槽大量「已聽過」 | 新檔只播 MERGE 教學碎片＋「教學預置」；`mockAskAlreadyHeard` 只認 `fromAsk`／已拼合 |
| 8 | P2 | 手帳殘留／深水埗 | 頂欄改黃大仙；結算文案跟當週；過兩週藏舊結算卡 |
| 9 | P2 | 針「N 則」與欄不一致 | 針則數用 `gigsForLocSeasonBoard`；aria「可接 N／共 M」 |
| 10 | P2 | 拍攝標籤／加速掠過 | `拍攝日：`；所有 `shoot:` 當 critical；1 日通告標「拍攝日→殺青」 |
| 11 | P2 | 還債後錯落何生所 | 手帳「去還」`fromJournal` 唔 `openLoc(agency_ho)`；返地圖清 `atLoc` |
| 12 | P2 | 茶餐廳 dismiss 掉面板 | toast 路徑 `setTimeout(reopen)`；同 #6 關閉回調 |

## Cache

`?v=19z9` → `?v=19z10`

Prefs key 仍 `starVolunteer_prefs_v19z9`（相容舊設定）。

## Soft≠PASS

- 唔改 `featureFlag_softBehaviorGatePreview`／gatePath
- soft 預覽空手還仍只展示、唔清債

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z10&softBehaviorGate=1`

1. 殺青／買禮後地圖頂「存款」即時跟狀態一致
2. 現金 $200 還何生：扣款＋清債＋toast 結餘
3. 老張「去還」開老張還款，唔出「無欠何生」
4. 開局「去金龍播事態」→ 地圖金龍
5. 選單返屋企 → 揀返手帳（唔過日）／提早休息（確認後 +1日）
6. 通告欄關閉後仍留地點選單
7. 新槽打聽唔預鎖「已聽過」；傳聞牆教學碎片標「教學預置」

## Deferred

- 無
