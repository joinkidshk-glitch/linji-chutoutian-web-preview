# NOTES — v20a12 P0-3 傳聞過濾一致性修復（soft）

日期：2026-11-09
Branch：`fix/p03-rumor-filter-consistency`（base：main 21eeee8）
範圍：只改 `index.html` 三處顯示路徑；唔改 SAVE key、唔改 softRev、唔改 ?v=。

## 覆檢發現（2026-11-09 線上新版實測）

P0 五項覆檢：P0-1／P0-2／P0-5 PASS、P0-4 部分通過、P0-3 FAIL。
P0-3 排版已修好，但文字出現不一致：

- 碎片卡面標題：「陸柏言深夜夜歸散心」；拼合確認彈窗標題：「陸柏言深夜買醉」
- 碎片／拼合文字：卡面「…半夜喺蘭桂坊坐到好夜…」，但有路徑顯示原文「飲到爛醉」

## 根因

遊戲本身有一層刻意設計嘅「家庭友善」顯示過濾 `familySafeRumorText()`
（v19z12 B2；soft 預覽經 softBehaviorGate 預設開，玩家可喺設定關閉）：
顯示時將「買醉→夜歸散心」「飲到爛醉→坐到好夜」「抽煙／食煙→歇息」。
`renderRumorPane()` 有行 `displayRumor()` 所以卡面一致；但以下三條顯示路徑
繞過咗過濾，直接用原文，同卡面打架：

1. `requestMergeConfirm()` 拼合確認彈窗：直接用 `rows[i].title` 原文。
2. 聽到傳聞 toast（v19z3 短標題）：直接用 `rumorTitle` 原文。
3. `noteWeekHighlight()`：原文標題存入週回顧，再喺 `weekBestReplayLine()` 原文顯示。

拼合結果文字本身（`MERGE_PAIRS`）自 v20a11 起已改用碎片原句
（「半夜又喺蘭桂坊飲到爛醉」）；過濾開時，碎片同拼合卡會一齊顯示軟化版
（「…坐到好夜…」），過濾關時兩邊都顯示原句 — 修完上述三處後全程一致。

## 修法（只改 index.html）

1. `requestMergeConfirm()`：新增 `dRows`（逐行行 `displayRumor()`），彈窗改用 `dRows[i].title`。
2. 聽聞 toast：新增 `safeRumorTitle`（`displayRumor({title})` 結果），toast 改用佢。
3. `noteWeekHighlight()`：`kind==="rumor"` 時存入前先行 `displayRumor({title})` 過濾。

過濾函數本身、過濾詞表、開關邏輯全部無改；過濾關閉時行為同以前原文顯示完全一樣。

## 驗證

- 內嵌 scripts `node --check` 通過。
- `tests/test_p03_filter.js`：抽出真實 `familySafeRumorText`／`displayRumor` 行為驗證 —
  過濾開：碎片標題／內文同拼合文案軟化後一致（同句「…坐到好夜…」）；
  過濾關：拼合文案逐字包含碎片原句「半夜又喺蘭桂坊飲到爛醉」。
- `tests/test_p03_static.py`：三處修法字串在位、過濾函數原文不變、版本字串次數與修前一致。

## 未處理

- 覆檢提到拼合文案「爆煲／爆鑊」兩寫：全 repo 搜尋只有 `MERGE_PAIRS` 用「爆鑊」，
  「爆煲」只出現喺另外兩條無關傳聞標題，未能重現，暫列觀察，今次無改。
- P0-4 提示 1.8 秒計時未能喺瀏覽器精確量度（行為與預期一致），維持觀察。
