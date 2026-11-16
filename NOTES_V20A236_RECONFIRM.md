# NOTES_V20A236_RECONFIRM — 抉擇再確認（v236）

## 做咗咩

全 repo 原本 0 個 reconfirm，10 個即刻落決定的面一次過加確認：

- **共用機制**：`confirmChoice236(opts)`（L20725，`confirmSpendDay` 之後）——確認框顯示選項原文＋後果提示，書面語；「返去揀過」行先、「確定」行後；只有「確定」先落決定，「返去」／撳遮罩返去選項列零副作用。
- **故事側**：`pickChoice`（L12156）確認插喺 `applyChoice` 之前——覆蓋主線 N1–N19、支線、感情線、commit、F4、G4、WF3 N8_d、contra98；N17 前夕（留低／收山／走）同一條路，加「去留決定一旦落定，不可更改。」；WF4 `decide()`（後果＝fx 數值譯書面語，`wf4FxLine236` L24861）；ENC79 巧遇 overlay 行內確認（唔經 `modal()`，避免俾 mask 蓋住），後果預覽行 `enc79ChoiceFx`。
- **系統側**：買禮物（`openGiftShop`）、打聽（地點板掣）、傾談（地點掣＋女角 modal 兩處）、還債（`openDebtRepaySheet` 禮物／現金）、頒獎請柬（出席／推辭，遮罩＝推辭唔郁）、醫院治療（`hosp96TreatGate`）。全部只包確認一步，執行函數本體（`buyItem`／`applyMockAsk`／`doTalk`／`applyChoice`／`resolveEnding410`）一行冇郁。
- **唔加**：已有確認的面、無選項「完成這一節」掣（得一個出口、無實質抉擇）。

## 測試

- 改 17 檔測試做兩步流程新期望；新增 `tests/test_reconfirm236_logic.js`＋`tests/test_reconfirm236_static.py`。
- 行數釘 resync 見 `qa236/resync236.py`（difflib 映射、內容逐字核實純漂移；`index.html` 淨 +146 行，45327→45473；travel114 另加 2 處新 `openLoc(` 免費點入 FREE_LINES，呼叫點總數 51→53）。
- Suite：基線 312／10 → 完成 **314／10**（FAIL 集合同基線一致，10 項皆 pre-existing 靜態）；`node --check` 通過。
- 詳見 `~/workspace/linji-v236/WORKLOG.md`。

## 未落地

工作副本 `~/workspace/linji-work236`，未 merge、未 push，等統籌核實。
