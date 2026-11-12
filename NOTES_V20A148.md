# NOTES_V20A148 — v146 設計 review B1 修復：st08 的士 banner 裁切位改 20%

- 版本：v20a148（分支 `v20a148`，由 main `da90957` 開；工作副本 `~/workspace/linji-work148/`）
- 日期：2026-11-13
- 範圍：**只修 B1 一項**（v146 review 唯一 B 級）。C1（K房電視空白）係 C 級，留返原生版，今次唔郁。
- 用戶拍板：2026-11-13 03:22「好，修 B1」

## 問題

v146 review B1：st08「的士佬送機有感」卡片 banner 中央裁切（50%），747＋啟德跑道完全出框——
banner 只見深色頭枕＋軚盤＋咪錶，頂部得一條跑道燈帶。原圖最有價值嘅迎面降落 747＋啟德跑道燈，
喺遊戲入面一次都見唔到；st08 係移民潮暗線最實一單（的士佬講尋晚車一家人去啟德）。
成因：banner 342×150，cover 縮放後原圖可見帶係中央 y 482–798（50%）；747 喺 y ~200–280，
跑道燈主體喺 y ~450–650——成個上半截裁走晒。唔係圖嘅問題，係裁切位問題
（同 v134 街市 banner 50% 裁到招牌帶同一類問題，嗰次用 75% 修好）。

## 修法（一行 CSS，唔使重生圖）

`index.html` `wf4PlayEvent` 內 `scenePos146` 分流（L40625–40629）：
跟 v146 B2 街市 75% 同一個 per-image override 機制，加埋的士圖：

```js
const scenePos146 = scene105 && scene105.indexOf("bg_wf4_market.jpg")>=0 ? ";background-position:center 75%" : scene105 && scene105.indexOf("bg_wf4_taxi.jpg")>=0 ? ";background-position:center 20%" : "";
```

- 20% 係 review 已模擬驗證嘅甜點（`sim_taxi_20.png`：成架 747 入晒鏡＋跑道燈齊；25% 機頂微裁、30% 已出框）。
- 只限 `bg_wf4_taxi.jpg` 一張圖；街市 75% 不變；set08／st04／st05 共用 `.wf4-scene105`
  嘅 `background-position:center` 不變；舞台版 `sp-bg-layer` 唔郁。
- 註解同步改寫（同樣 4 行，行數零漂移——`test_travel114_static.py` 硬計嘅 DEF 53562／WRAPPER 44171
  行號唔使 resync；`git diff` 淨 5 行改 5 行）。
- 覆寫表唔郁（st08 仲係 `bg_wf4_taxi.jpg?v=20a146`）；唔改 SAVE key／softRev／產品 `?v=`；唔改 content pack JSON。

## 測試

- 新測試 `tests/test_taxi148_static.py`：12 項斷言（B1 分流＋20% 只出現一次＋註解在場＋同一條 ternary 同時認
  market 75% 同 taxi 20%；B2 回歸守衛：75% 仲喺度且只出現一次、v20a146 B2 註解、共用規則同 sp-bg-layer 不變；
  基線：SAVE key／softRev／?v=、覆寫表 st08／st05／st06／set08／st04）。
  - 工作版：**12/12 PASS**；pristine main（`da90957`）：4 項 B1 斷言乾淨 FAIL（反證成立，唔係 crash）。
- 全套 `qa131/run_suite.sh`：
  - pristine baseline（`da90957`）：**210 PASS／12 FAIL**
  - 工作版：**211 PASS／12 FAIL**（多咗嘅 1 個 PASS 就係新測試；FAIL 清單逐行一致＝零回歸）
  - FAIL 12 項全部 pre-existing（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111／start53／weave43／44／49／wrap38），同 v146 baseline 相同。

## 實駕（`qa148/drive148.py`，本地鏡像 port 8918，Playwright）

7/7 PASS，0 pageerror：
- **st08 @700＋@932**（播種 dayIndex=365＝1991-01-01，cond yearMin:1991；過一日後 day 366）：
  banner `bg_wf4_taxi.jpg?v=20a146`、`background-position: 50% 20%`、`background-size: cover`、342×150。
  目視確認（`qa148/shots148/card_st08_700.png`／`card_st08_932.png`）：**成架 747 迎面降落入晒鏡
  （機身＋翼＋落機燈完整）＋啟德跑道燈＋海港＋吊牌齊晒**，同 review 模擬 `sim_taxi_20.png` 一致。
- **st06 @700＋@932**：`bg_wf4_market.jpg?v=20a134`、`50% 75%`——檔口帶（魚檔＋菜檔＋簷篷）不變。
- **st05／set08／st04 @700**：全部 `50% 50%`——共用規則唔受影響。
- 證據：`qa148/drive148.json`＋`qa148/shots148/` 7 張截圖＋`qa148/suite_baseline148.txt`／`suite_work148.txt`。

## 落地

- main commit `e323db1`（squash merge，分支 `v20a148`，base `da90957`；v149 未落地，唔使 rebase）。
- index.html staged diff 同分支原 diff 逐字相同（blob `98615c6..4f5a4ae`，5＋／5－）；`git fsck --strict` 乾淨。
- 已推上 GitHub（`da90957..e323db1 main -> main`，origin/main 已確認 `e323db1`）。
- 線上核實：（待填：curl bytes／sha）
