# NOTES_V20A122 — AUD91 試鏡結果公佈修復（H1 晨報旗卡死＋H2 排程 modal 遮罩點走）

- 分支：`v122-aud91-fix`（基底 main `f7fb273`＝v121；合併嗰陣 main 未郁，無 rebase）。
- 性質：純防守性修復，兩處 in-memory 旗卡死。唔改 content pack JSON；唔郁 SAVE key／softRev／產品 `?v=`；R2（modal 取代覆寫 `_modalDismiss`）唔做，另開一票。
- 來源：調查報告 `~/workspace/linji-aud91-invest/NOTES_AUD91_INVEST.md`（基準舊 main `215b97e`；行號已喺新 main `f7fb273` 重新對過——H1／H2／closeModal 行號同舊基準一致，零漂移）。
- 用戶症狀：經日結板返地圖等 4 日都唔公佈試鏡結果；經手帳事業頁返地圖即刻彈。調查結論：99% 係 H1。

## 改咗咩

### index.html（＋7／−2 行，淨 +5 行，對 main `f7fb273`）

**H1 — `presentDueMorningPaper()`（46904 行起），晨報 `_paperShowing` 旗卡死（主因）**
- 舊 46909 行：`if(FREEPLAY_FW && FREEPLAY_FW._paperShowing) return true;` —— 旗 true 就靜默 return true，乜都唔做、唔叫 `cont`；`goToMapForBrowse` 當佢「已處理」直接 return，aud91 連檢查都未到。
- 新 46909–46913 行（標記 `v20a122 AUD91FIX H1`）：旗 true 嗰陣清返 `_paperShowing = false`，然後跌落去正常流程——再檢查 `newspaperHoldForToday()`／`pullDueNewspaperEdition()`，冇到期就 return false，條鏈繼續行 aud91；有到期就照常出晨報 modal。
- 保底：`closeModal()`（38522 行起）頂部加統一清旗（標記 `v20a122 AUD91FIX H1`，約 2 行）：`try{ if(FREEPLAY_FW) FREEPLAY_FW._paperShowing = false; }catch(_p122){}`。任何關 modal 嘅路都唔會漏清。遊戲自檢 `newspaperCheck` #105（約 47349 行起）本身用人手 reset 做同樣嘅事，嗰三處 reset 原封不動，冇整爛。

**H2 — `confirmPlaceShoot()`（35381 行起），獲聘「拍攝排程」modal 冇 `onDismiss`（已確認真 bug）**
- 舊 35389–35400 行：要佔用日子嗰陣彈三掣 modal（確定佔用／只排空日／取消），冇傳第三個參數——遮罩點走會關 modal，但 `go()`／`thenFn`（即 `finishReveal`）唔會行，`_aud91Presenting` 永久 true；嗰單 pending 已經喺 `aud91PresentOne`（56201 行）先剔除，公佈永久遺失。
- 新 35396–35397 行（標記 `v20a122 AUD91FIX H2`）：加 `{ onDismiss: ()=>go(false) }`，等同撳「取消」：只排空日，其餘留待下週。`go()` 定義不變（`placeShootOnPlan(shoot, fromWeekday, !!overwrite)`＋`thenFn()`）；按掣路徑先 null 掉 `_modalDismiss`，所以 `onDismiss` 只會喺遮罩點走嗰陣行，唔會同掣重複行。遮罩 handler（57591 行起）先 `closeModal()` 再行 `fn()`，`finishReveal` 照行、「獲聘」modal 照出、`_aud91Presenting` 清旗。

**R2 唔做**：`modal()` 取代舊 modal 之前行舊 `_modalDismiss` 嘅防守性改動另開一票，呢包冇郁 `modal()`。

## 測試

- 新守門（全部 PASS；pristine main 跑新測試 FAIL，反證成立）：
  - `tests/test_aud91fix122_logic.js`（node 沙箱，抽真函數）：20 斷言——H1a 旗卡死＋冇報紙（return false＋清旗＋冇 modal）、H1a2 旗卡死＋hold、H1b 旗卡死＋有報紙（照出 modal，dismiss 後清旗＋cont＋commit）、H1c 正常路徑不變（有報紙／冇報紙）、H1d `closeModal()` 保底清旗、H2a 排程 modal 帶 onDismiss、H2b 遮罩點走等同取消（go(false)＋thenFn）、H2b 對照（取消掣／確定佔用掣語義不變）、H2c 唔使佔用即刻 go(false)唔彈 modal。喺 pristine main 跑 **9 FAIL**。
  - `tests/test_aud91fix122_static.py`：26 斷言——舊靜默 early-return 已刪、新清旗行＋流程順序（清旗→hold→到期）、晨報 done() 清旗不變、#105 reset 不變、closeModal 保底行在、H2 onDismiss＝go(false)＋三掣不變＋go() 定義不變、R2 冇郁 `modal()`、紅線（SAVE／softRev／?v=／content pack JSON）不變、NOTES 在位。喺 pristine main 跑 **10 FAIL**。
- 全套回歸：pristine main 基線 **161 PASS／14 FAIL**（14＝12 個已知環境性 static FAIL＋2 檔新守門喺 pristine 上 FAIL）；工作版 **163 PASS／12 FAIL**（＋2 新守門檔），FAIL 清單逐字一致（flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38）。零回歸。行號漂移一處：`test_travel114_static.py` 因本包淨 +5 行要 resync（`qa122/resync_travel114.py` 核實 44 個 `openLoc(` 呼叫點序列逐字一致、內容逐行相同，純漂移；COUNT 13／FREE 27 不變，DEF 52487→52492、WRAPPER 43341→43344），resync 後再 PASS。

## 實駕（Playwright 真 UI 路徑，390×844，`?softPreview=1`，本地鏡像＋http.server；驗證劇本改調查嘅 driver 嚟用）

- 環境：Playwright venv `/home/hatch/pwenv49/bin/python`，headless shell；`python3 -m http.server 8972` 服工作版；curl 核實 served bytes＝本地 index.html（5,139,966 bytes，sha256 `97dd13db…`）。Driver `qa122/drive_verify122.py`，log `qa122/logs/verify122.log`，截圖 `qa122/shots/`（20 張）。
- U6（H1 主因）：設 `_paperShowing=true` 後連續 4 日路徑 A，**4/4 即刻公佈、0 靜默**（舊版調查：4/4 靜默）。probe：`present()=false`＋無 modal（舊版 `true`＋無 modal，靜默吞鏈）。第 3 循環撞正週界板（得「回家結算」）→ 撳佢 aud91 跟住出，屬設計流程。
- R1（H2）：ok:true、全週 street、入屋出「拍攝排程」modal、遮罩點走 → **即刻出「獲聘！」modal**（舊版：乜都冇；簽約金 $900 已入帳，shoot 已排）；之後再播種一單，入屋**即刻呈現**（舊版：due=1 但零呈現，旗卡死）。
- 對照 T1（乾淨路徑 A，fail）：即刻出「系統／本次未獲聘」，PASS。T2（晨報到期＋路徑 A）：晨報 modal 先出 → 「收下這份剪報」掣 dismiss → aud91「系統／本次未獲聘」跟住出，PASS——H1 正常流程唔爛。
- 全部劇本 **0 pageerror**。Driver 教訓（寫埋入 driver 註解）：唔好用手帳來回重畫 CTA——入屋會經路徑 B 即刻呈現 pending，modal 未閂就程式化撳開始掣會繞過 inert、stranded `_aud91Presenting`（R2 機制），會令成個 U6 變 0/4 假 FAIL；第 2 週 plan 清空嗰陣先設 plan 再返地圖（forced day 自動行一日，係設計流程）。

## 合併

- 待填：squash commit、線上 index byte／sha 核實。

## 回滾

- `git revert <squash commit>`（成包只係 index.html 3 處＋2 檔新測試＋本 NOTES；revert 即回復 v121 行為——H1 靜默吞鏈＋H2 遮罩卡死會返嚟）。

## 殘留

- **H1 自然觸發點仍然未搵到**：掣 dismiss 同遮罩 dismiss 兩條合法路徑都已驗證會清旗，正常遊玩入面搵唔到邊個位會漏清。呢包修復係防守性清旗——無論觸發點係咩，旗卡死都唔會再吞鏈；觸發點本身唔影響修復有效性。要查觸發點需要用戶嗰邊嘅資料（調查報告 §8 五條問題）。
- R2 另開一票。
- 廖炳星欠 `shy` 表情圖（舊問題，兩次實駕 console 404，fallback 正常行）——唔係呢包範圍。
