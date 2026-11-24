# NOTES_V20A394 — E0 加入 1992 floor 豁免

- 拍板：用戶 2026-11-24 20:17「E0 加入 floor 豁免」。
- 背景：v393 之後 E0 條件係 fame≤40 且活動 ≤2 宗（`lowAct392`）；呢類玩家 dual 上限約 124，
  結構上到唔到 1992 floor 140。v393 實證：閒置路線 fame 36／credit 40／dual 76 行到 N17，
  `resolveEnding410` 本身判 E0，但 `ending410ResolvePresent410` 嗰刻 dual 76＜140、E0 唔喺
  `ending361FloorExempt` 之列，改判 E7 `review1992`。E0 同 floor 互斥，19 格得 18 格可達。

## 改動（只做呢一項）

- `index.html` `ending361FloorExempt`（L14901）：加 `|| career==="E0"`。
  豁免名單而家係 E6／E4／E3／E5／E0。註解補 v20a394 交代；`CONSEQ61_REVIEWS[1992]`
  註解同 `ending410ResolvePresent410` 內 F2 註解同步提及 E0。
- 唔郁：1992 floor 140／warnLine 180、`resolveEnding410` 各格門檻、`lowAct392` 定義、
  中途破產／年尾評核唔合格嘅提早收場路徑、其他結局條件、頒獎贏線 0.875、SAVE key、
  softRev、產品 `?v=`、source 年份。

## 測試

- 新增 `tests/test_v394_logic.js`（24 項）：豁免名單（E0 入、E2／E1／SS／FK 唔入）、
  E0 dual 76（v393 閒置個案）留 E0 唔寫 earlyEnd、E0 dual 139／140 留 E0、
  E2 dual 100 照舊改判 E7 review1992（earlyEnd floor 140）、E2 dual 200 照舊、E4 dual 83 豁免回歸。
  結果：24 passed／0 failed。
- 新增 `tests/test_v394_static.py`（10 項）：豁免名單、floor 數字不變、F2 覆寫接線、
  E0 預設 fallback＋`lowAct392` 不變、註解。結果：ALL PASS。
- 舊測試更新：`tests/test_r345_fullarc_fix.js`「E0 dual 139 改判 E7」改為「E0 dual 139 豁免留 E0」
  （舊行為已廢），加「唔寫 earlyEnd」斷言。結果：TOTAL PASS 42 FAIL 0。
- `tests/test_p361_static.py` B3 檢查只驗舊成員存在，唔使改。

## 實駕（工人回報，`~/workspace/linji-drive394/REPORT.md`）

四局 Playwright 全部 PASS（工作副本 serve 9462，對照 main 171f9c3 喺 9461）：
- **E0（v394）**：E0「浮沉未定・留下來的人」，day 1066，fame 38／credit 41／dual 79（＜floor 140），
  無 `earlyEnd`，gaps95 保留。文案：「三年，你沒有沉下去，也未浮到水面上。」
- **E0 對照（v393 main）**：同一種子、同一路徑、同一終局數字，E7 review1992，
  `earlyEnd {review, 1992, dual 79, floor 140}`——A/B 證明改動正正係令同一局由 E7 變返 E0。
- **E2 兜底（v394）**：E7 review1992，dual 103——豁免只限 E0，非豁免格照舊。
- **1991 評核（v394）**：E7 review1991，day 728，dual 76＜100，提早收場路徑未郁。
  1990 路徑以邏輯＋測試引用（diff 零改動，`test_conseq61_logic.js` 82／0 重跑通過）。
- **Brief 前提更正**：brief 話 `E0b_ls_checkpoint_d1050.json` 係「v393 閒置局 fame 36／credit 40／dual 76」——
  實測該檔係 fame 147／credit 266／dual 413、活動 17 宗（Strategy S 訓練局，終局 SS）。工人冇直接用佢，
  而係以該檔嘅真實故事進度骨架（day 1050、N1–N15 已做、1990／1991 評核已過）改寫成 v393 閒置個案
  （fame 36／credit 40／dual 76、活動 0 宗），入 game 後 probe 核實 live 數字零漂移。
  方法同理據見 `~/workspace/linji-drive394/REPORT.md` 同 `make_seeds.py`。
- 細發現：Resume 入 game 後 `S.weekPlan` 會畀 preset 覆寫（driver 每次 planner 改寫返，數字零漂移）；
  N16 揀「臨場爆肚」（電影 gig，N17 前殺唔到青）避開「兩個版本」（廣告 gig 2 日，萬一 N17 延遲會殺青推高數值入 E2 區）；
  R91 局中途病倒一次，送醫院處理，壓力機制如常；E0 終局 creditsHeld 3 vs 途中 held 2 係 N16 人情結算嗰刻計入，純顯示差異。

## Resync（v394 註解令 index.html 淨 +5 行）

- 第一輪 suite 405／17：8 項額外 FAIL 全部係行號釘漂移（gift185／rom159／rom176／tang152／
  tang171／tang173／text125／travel114），唔係邏輯回歸。插入點：豁免函數前註解 +4 行＠舊 L14897、
  CONSEQ61_REVIEWS 1992 註解 +1 行＠舊 L18516。
- `qa394/resync394.py`：difflib 映射＋內容逐行核實純漂移，釘值由現行檔動態抽出（base 171f9c3）。
  travel114 DEF 45484→45489、WRAPPER 31674→31679（COUNT／FREE 零移除）；
  rom159 16097→16101、27802→27807、28565→28570、28710→28715、全佳 27830→27835（9289／11469 唔郁）；
  rom176 16095→16099、43479→43484、43838→43843、45404→45409、45525→45530（7428 唔郁）；
  tang152 [16024]→[16028]、[16149]→[16153]；text125 17762→17766（12049／12191 唔郁）；
  gift185／tang171／tang173 總行數 50506→50511、openLoc DEF 45484→45489。
- 逐檔重跑 8 檔全部 PASS。resync 腳本本身有兩個過程事故已修：(1) 全佳行括號數字本身就係 1-indexed，
  初版多加咗 1 令 assert 炒車（已修，travel114 已寫入嗰次靠 `git checkout` 還原重做）；(2) DEF 檢查行
  係 ok() 嘅下一行 continuation，初版 loop 漏咗（已修）。

## Suite

- 基線 411 PASS／9 FAIL（九項已知 pre-existing）。第一輪 405／17（8 項行號釘漂移，見上）。
  Resync 後第二輪待跑。
