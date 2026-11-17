# NOTES_V20A281 — 收尾獎勵信用收窄（v280 跟進）

- 版本：v281。Base：main `37c1a28`（v280，suite 345／9）。
- 拍板：用戶 2026-11-18 05:45 揀收窄（delta ＋2→＋1，令每線信用淨 ＋2）。

## 改動（index.html，行數淨 ±0）

1. `sideline280GrantCompletion`（L38882 helper）：信用 delta `+ 2` → `+ 1`（L38902）。聲望 ＋2 唔郁。冪等旗 `S.flags.sideline280_<line>` 唔郁。
2. Helper 頭註解兩行同步：
   - 「數字用建議值原樣（＋2／＋2…）」→「數字：聲望 ＋2／信用淨 ＋2（v20a281 收窄：delta ＋1＋派生 ＋1；九線全暖 ＋18／＋18）」。
   - 「派生值註：…連 ＋2 delta…實際 ＋3」→「連 ＋1 delta…實際 ＋2（v20a281 收窄：delta ＋2→＋1；舊版每線實際 ＋3，九線 ＋27）」。
   - 「暖版完成＝…聲望 ＋2／信用 ＋2…」嗰句唔使改——淨信用本來就係 ＋2。

## 機制（已核實，L16777）

`baseCredit = Math.round(fame×0.5 + stage×0.3 + acting×0.2 − …)`。＋2 聲望令 baseCredit ＋1，連 ＋1 delta，`readDualTracks` 嘅 industryCredit 實際 ＋2。九線全暖：聲望 ＋18／信用 ＋18（E1 雙軌 ＋36），唔係 v280 嘅 ＋18／＋27（雙軌 ＋45）。

## 舊存檔

唔追溯。已派過獎勵嘅舊存檔，冪等旗 `sideline280_<line>` 已落，唔會重派；已經入帳嘅 ＋2 delta 唔會扣返。只影響未派獎勵嘅存檔／新遊戲。

## 測試

- `tests/test_sideline280_logic.js`：41 項（原 40＋新 1），ALL PASS。
  - 13 處 `S.industryCreditDelta===2` 斷言 → `===1`（(1) helper 單元／(1) 冪等／(1) 派生值／(2) patron 整合／(3) 補派點各處）。
  - (1) 派生值斷言：`after===3` → `after===2`，標題改做「＋2 聲望＋＋1 delta → 信用 ＋2」。
  - (6) 九線全暖：`delta===18 && derived===27` → `delta===9 && derived===18`。
  - 新加 (6b)：每線信用淨 ＋2 機制斷言（＋2 聲望派生 ＋1 ＋ delta ＋1 ＝ ＋2，`after-before===2`）。
- 全套 suite：見下（基線 345／9；9 項 pre-existing FAIL 名單：flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）。

## Suite

- 全套 suite：**TOTAL PASS 345 FAIL 9**（`bash qa131/run_suite.sh`，工作副本）。9 項 FAIL 全部係已知 pre-existing（flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38），同 345／9 基線對照**零回歸**。`tests/test_sideline280_logic.js` PASS。
