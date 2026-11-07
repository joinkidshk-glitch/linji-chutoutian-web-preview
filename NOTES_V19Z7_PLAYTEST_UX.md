# v19z7 — playtest UX（v19z6 試玩改善）

Branch `fix/playtest-ux-v19z7`. Implements P0 + key P1 from 《臨記出頭天-UX改善報告-v19z6試玩》.

## Fixes

| # | Pri | Issue | Fix |
|---|-----|-------|-----|
| 1 | P0 | Modal／mask 叠層時背後仍可點（日結 HUD、地圖、手帳） | `setUnderlyingInert`：`#v-map`／`#v-home`／`#v-start`／`#loc-sheet` 加 `inert`；CSS `#app.mask-up … { pointer-events:none }`；`body.day-res-open` 禁 bar／手帳按鈕；`modal`／`closeModal`／`setTutMask`／`setStoryPlayLock` 同步；開 modal 聚焦第一掣 |
| 2 | P0 | 「返地圖／回地圖」用語分裂 | 關 overlay →「關閉／知道了」；關地點 sheet →「返回地圖」；週末／週結掣 →「回家結算」；自由日回家門 →「返回地圖」（強制日仍「繼續行程」） |
| 3 | P0 | 日結後日期／今日計劃／手帳頂欄不同步 | `syncDateChrome`：`paintBar`＋`#home-date`＋notebook `is-today`／非編輯時 `.on`；`tickDay`／`afterDayModal` 即時呼叫 |
| 4 | P0 | 地圖耗日行動無預告 | `confirmSpendDay`：訓練（`doEnroll`）／休息（`doRest`）／接通告（`openCastingNoticeDetail`／`promptAudition`）前確認「用掉今天」＋下一日手帳預覽；傾談／送禮／打聽仍跟 soft 閘免費 |
| 5 | P1 | 打聽成功只有 toast | `applyMockAsk` 成功後短卡：傳聞標題＋摘要＋「已記入傳聞」＋「去傳聞拼合」／「知道了」；已聽過鎖不變 |
| 6 | P1 | 拼合失敗反饋弱 | `mergePickedRumors` 無 pair → 強制 modal「拼合未成」＋「呢兩單未見關聯…」 |
| 7 | P1 | 標題頁規則過密 | 標題只留一句賣點；試玩規則收成 `#start-soft-tip`（`paintBar` 跟 softPreview 顯示／隱藏）；地圖黃字 banner 保留 |
| 8 | P1 | 教學可跳過 | 維持既有「跳過教學」；未刪 soft 規則 |

## Cache

`?v=19z6` → `?v=19z7`

## Soft≠PASS

- 唔改 `featureFlag_softBehaviorGatePreview`／`gatePath` 語意
- 唔 tip LIVE week-gate
- Soft 免費社交路徑唔強制耗日確認

## Deferred

- 手帳自動行程（`cafe_gig`／街頭／拍攝日）唔逐日再彈耗日確認（避免連點疲勞）；只擋地圖主動 +1 日
- 通告詳情摘要／詳細兩段、週日結加速、桌面雙欄、新遊戲原生 confirm 改 modal：未做
- 教學步數未大幅刪減（只靠既有跳過）

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z7&softBehaviorGate=1`

1. 日結／事態／教學 modal 開住 → 點唔到背後「繼續行程」／地點／分頁
2. 地點 sheet 掣＝「返回地圖」；事態結算＝「關閉」；週結掣＝「回家結算」
3. 報名訓練／休息後，結果卡「而家」日期＝頂欄／`#home-date`／今日計劃
4. 地圖訓練／休息／接通告先出「確認耗日」；打聽／傾談／送禮（soft）唔出
5. 金龍打聽成功 → 結果卡＋可去傳聞；錯拼合 →「拼合未成」modal
6. 標題短賣點＋試玩規則 tip；選單仍可「跳過教學」
