# v20a16 — Weave Phase 2-1：情報旗正式化＋鏈 A 隱藏替工通告

Soft 預覽改動。唔改 SAVE key（`starVolunteer_map_v19w`）、唔改 softRev（s107）、唔改 `?v=`（v20a10）。

## 研究結論：通告上板管線

- 通告板名單由 `gigsForLocSeasonBoard(locId, curSeason)` 由全域 `GIGS` 過濾而成：地點相符、`seasonRank ≤ 0`、未被 `isGigConsumed`（已殺青／拍攝中）先上板；`doScout()` 用呢份名單渲染短卡。
- `boardHookMode` 只係 GIGS 數據欄位，全檔無任何邏輯引用，唔係過濾機制。
- 條件注入有現成先例：`mergeSoftBridgeGigs()` 喺 `gigsForLocSeasonBoard` 開頭呼叫，按條件將橋接通告注入／移出 `GIGS`。今次跟同一模式，改動面最細。

## 改動

1. **情報旗層**（近 Phase 1-3 情報區塊）：
   - `INTEL_FLAGS`：拼合 id → 旗名對照（`rumor_lu_baiyan_breakdown`→`intel_lu_burst`、`rumor_liao_bingxing_money`→`intel_liao_money`、`rumor_mai_zhendong_hide_injury`→`intel_mak_injury`）。
   - `S.intelFlags`：`fresh()` 新增預設 `{}`；旗值為 `{ day, backfilled? }`。
   - `ensureIntelFlags()`：舊存檔兼容——欄位缺失即補 `{}`，並按手帳已 `state:"merged"` 嘅行回填旗（標 `backfilled:true`）。
   - `setIntelFlag(mergedId)`／`hasIntelFlag(flagName)`。
   - `mergePickedRumors()` 拼合成功即 `setIntelFlag(pair.merged)`。
   - `hasMergedIntel()` 改為先查旗、再 fallback 掃 merged 行；Phase 1-3 使用點（通告卡情報行、遠觀對白）介面不變。
2. **鏈 A 隱藏通告**：
   - `INTEL_HIDDEN_GIGS`：一張新通告 `gig_intel_lu_standin`《星夜迷離》臨時替工（星河電視台 tvb_longmen、電視劇、季節不限、初階、1 日、平實命名，唔劇透拼合內容；`starHint` 陸柏言，卡面會照常顯示 Phase 1-3 情報行）。
   - `mergeIntelGigs()`：喺 `gigsForLocSeasonBoard` 開頭（緊貼 `mergeSoftBridgeGigs`）呼叫；持有 `intel_lu_burst` 先注入 `GIGS`，無旗即移除——無情報嘅玩家完全見唔到。
   - 通告接取／拍攝／殺青／薪酬／聲量全部行現有系統，無新寫結局事件。

## 未做（留待後續 Phase）

- 規劃鏈 A 第 2 拍嘅「7 日內」時效：今次旗為長期持有，未加保鮮期／到期（旗值已記 `day`，日後可加）。
- 鏈 A 第 4–6 拍（PA 人情、報紙跟進、NPC 專屬對白）未做，屬後續節拍。

## 測試

- 新增 `tests/test_weave2_logic.js` 26/26、`tests/test_weave2_static.py` 15/15。
- 回歸全過：P0 邏輯 17／靜態 27、P0-3 邏輯 7／靜態 12、Weave 1-1 邏輯 12／靜態 14、Weave 1-2 邏輯 16／靜態 7、Weave 1-3 邏輯 14／靜態 6。
- 全檔 script `node --check` 通過。
