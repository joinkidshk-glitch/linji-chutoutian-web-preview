# NOTES_V20A330_E2_CENSUS_TIER_NAMES.md

## 一、改動（測試檔 only，唔郁 live code）

- `tests/test_nat92_logic.js` L250–252：普查函數 `censusYear()` 嘅 tier key 由舊三級名改做 live 五級名——`'中'`→`'中級'`、`'高'`→`'高級'`（兩處：`tiers` 物件＋`for(const t of [...])`）。
- 原因（v324 NOTES §3(a) 已指出，pre-existing）：live tier 係「中級」／「高級」，舊 key 永遠 `undefined`，`ex2` 恒 0，E1／E3 pct 恒 0.0%，守衛形同虛設。
- `index.html`／`content/gigs_new.json` 零改動；通告庫維持 322 張。

## 二、測試（measure-first 真實數字）

- `node tests/test_nat92_logic.js`：**ALL PASS**。
  - E1 1990「恰好 2」占比：**1.6%**（<40% PASS）。
  - E3 1991／1992「恰好 2」占比：**12.2%／9.6%**（<40% PASS）。
  - E2 三年全板 0 地點-週＝0（1990:0／1991:0／1992:0）。
  - 其餘全部 PASS（F1／F1b／F2 錯峰合資格 310 張／F2b／F3／F3b／A1／A2／B1／B2／N1／D1 day-0 全板可接 45／D2／D3／D4／E0 MAXED 開齊 37 張 trigger）。
- v324 時代舊分析話真實 1990 pct 曾經 44.8%（index.html 註解附近）——今次實測 1.6%，唔再成立，原因係 v324 補咗 15 張分布缺口通告＋庫由 307→322，分布已變；§3 停手條件**未觸發**，唔使 B4 設計決定。
- 全套 suite：見 §五（已 commit 樹跑，TOTAL PASS 386 FAIL 9＝v328 基線，9 項 FAIL 同基線逐項一致，零回歸）。

## 三、驗收

- key 已改（`grep -n "中級" tests/test_nat92_logic.js` 見新 key；舊 `'中':0`／`'高':0` 字面 0 命中）。
- 真實 pct 已寫入本 NOTES §二；E1／E3 守衛全部 PASS。
- `index.html` 行數不變（47,249）；SAVE key／softRev／`?v=` 原封不動。

## 四、備註

- 本票只係修復普查函數嘅量度，唔係改分布——E1／E3 守衛而家先至量度到真實分布，之前 0.0% 係假數。
- B4（E2 守衛門檻 vs 分布）唔使開：三個 pct 全部遠低於 40%，守衛有足夠 headroom。

## 五、合併＋部署（待填）
