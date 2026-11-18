# NOTES_V20A287 — Beat 5 冷版接 liaoChoice（廖炳星線）

## 背景
- v279 NOTES（NOTES_V20A279_G-L2.md L65）留跟進：「Beat 5 冷版未接：WORKORDER 1.1 話搶鏡嗰邊『冷版開』，但 `liu_patron`／`liu_patron_cold` 閘門現時只讀 `enc79_liu_declined`／`enc79_liu_clash_script`，唔讀 `liaoChoice`。本票唔郁 patron 閘（v269 已測行為，唔想順手改）；留跟進票：搶鏡後 Beat 5 行冷版要讀 `liaoChoice==="steal"`。」
- 本票就係嗰張跟進票。基線：main e4b2e08（v286 已落地），suite 基線 350／9。

## 前提核實（parent 親查 live main，2026-11-18；工作副本再核實）
- `liu_steal` beat：index.html L39037——1991 秋＋tier ≥2＋C8 已完成先開；抉擇落旗 L39164：`st.liaoChoice = (fx==="liu_steal") ? "steal" : "steady"`（`st = ensureWf3()`）。
- `ensureWf3()`（L27489）回傳 `S.wf3`（冇就起一個空 object）。所以正宗讀旗路徑係 `S.wf3.liaoChoice`——`liu_steal` 閘本身就係咁讀（`!(S.wf3 && S.wf3.liaoChoice)`），兩閘跟同一寫法，唔另起 `ensureWf3()`。
- 冷版閘 `liu_patron_cold`：L39040——`enc79TierOf(st.fav)>=4 && ((S.flags||{}).enc79_liu_declined || (S.flags||{}).enc79_liu_clash_script)`。
- 暖版閘 `liu_patron`：L40876——`enc79TierOf(st.fav)>=4 && !((S.flags||{}).enc79_liu_declined || (S.flags||{}).enc79_liu_clash_script)`，grants 授 `credit_enc83_liu_patron`＋`sideline280GrantCompletion("liu")`。
- `wf3SettleTick`（L27514–27545）：抉擇翌日結算一次（steady → 信用 +2＋報紙好評；steal → +$800＋面子債 `debt_wf3_liao_grudge` dueDay+14＋報紙內訌）。本票唔郁。

## 修法（最小改動，加法唔改寫；同行改動，行數不變，零釘行漂移）
1. 冷版閘（L39040）加開冷版條件：`|| (S.wf3 && S.wf3.liaoChoice)==="steal"`。
2. 暖版閘（L40876）同步排除同一條件：`!((S.flags||{}).enc79_liu_declined || (S.flags||{}).enc79_liu_clash_script || (S.wf3 && S.wf3.liaoChoice)==="steal")`——跟 v269 排除式寫法，搶鏡者唔可以同時合暖版資格，唔靠註冊次序兜底（冷版本身已排暖版之前 shadow）。
3. 唔改對白、唔改結算、唔改 tier 門檻、唔改 credit 授出邏輯、唔改 SAVE key／softRev／`?v=`。

## 附帶：v269 測試靜態斷言同步（唔係回歸）
- `tests/test_sideline269_logic.js` L53「靜態：暖版只加排除式條件」釘死舊暖版閘字串（`...enc79_liu_clash_script)` 收括號）。今版有意擴充排除表，舊字串唔再存在——斷言字串同步更新為新排除表，意圖不變（暖版純排除式、無肯定式要求）。其餘 v269 斷言全部照舊。

## 測試
- 新 `tests/test_r287_liu_patron_liao.js`，13 項全過（A 組靜態 6 項＋B 組邏輯 7 項）：
  - (a) `liaoChoice==="steal"`（tier ≥4）→ 冷版開、暖版唔開；PickBeat 揀冷版。
  - (b) `liaoChoice==="steady"` → 暖版開、冷版唔開；PickBeat 揀暖版。
  - (c) 無 liaoChoice＋無壞旗 → 暖版開、冷版唔開（v269 舊行為不變）。
  - steal 但 tier 未夠 4 → 冷暖都唔開（tier 門檻照舊）。
  - 端到端：`enc79RunChoiceFx("liu_steal")` 落旗 → 冷版開、暖版唔開。
- 反證：新測試喺 pristine main（e4b2e08）跑，7 項乾淨 FAIL（A1／A2／A3／A4／B1／B2／B7），其餘 6 項行為保留斷言照過——證明測試真係驗到今版改動。
- v269 相關舊測試逐個直接跑：`test_sideline269_logic.js` ALL PASS、`test_wf3_279_logic.js` ALL PASS。
- 全套 suite：TOTAL PASS 351 FAIL 9——FAIL 清單同基線完全一致（flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38），零新 FAIL；PASS 351＝基線 350＋新測試檔 1 項。

## 落地
- main commit：7d900ac（e4b2e08 → 7d900ac，已 push，ls-remote 核實一致）；NOTES landing record 補 commit（見下）。
- Pages 核實：HTTP 200，4,688,798 bytes，sha256 `edf7263e18d2cdbf0da71ec13d12d069783baa31e451de70c65a6f5f5942c4f1`，同本地 byte-identical；`liaoChoice)==="steal"` 線上命中 2 處（兩閘）。
- 工作副本 linji-work287 已刪；下一版號：v288（用前再核實）。
