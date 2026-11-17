# NOTES_V20A272 — 手帳 tab 死掣修復

## 問題（瀏覽器實機捉到，2026-11-17 19:36，main e742377 v270）

live 遊戲「阿偉的家 · 行程手帳」面板：行程 tab 正常顯示（本週行程空白＋
提示＋「本週行程已確定（唯讀）」印章），返回地圖正常；但事業／近況／消息／
人情四個 tab＋衣櫃＋瞓覺撳落去全部毫無反應，冇切換、冇畫面變化、冇錯誤
訊息。瀏覽器試過多種方法（按鈕參照點、畫面描述定位、聚焦後按 Enter、
方向鍵、準確座標連續約 60 次點擊）全部無效。結束時日期同存款不變。

## 定性：唔關存檔事，新舊存檔一樣死

瀏覽器當時用嘅係舊存檔（第 1 週、荷包 $12,000＝v261 經濟 ÷10 之前嘅舊
scale、行程已鎖定）。但呢個唔係原因——根源係程式碼層面嘅未定義函數呼叫，
任何存檔狀態行到同一行都會掟錯。證據（唔使靠瀏覽器分新舊）：

- `grep` 全檔：`applyPhase2Steps56TabLabel` 零定義（得返一行殘留呼叫＋
  一行 v267 註解提及另一個函數名）。
- node 直接執行由 live 抽出嚟嘅 `setHomeTab` 原文：`works`／`ledger`／
  `plan` 三個 tab 全部掟 `ReferenceError: applyPhase2Steps56TabLabel
  is not defined`。
- 呼叫點喺 `setHomeTab` 第三行，行到嗰度之前完全唔讀存檔數據。
- **用戶 2026-11-17 19:49 親自確認：自己手機新存檔（開局 $1,200，
  第 1 日）撳「事業」tab 一樣轉唔到頁**——新存檔一樣失靈，唔係舊存檔
  相容問題，係 live UI bug（parent 轉告）。

## 根源：v267 刪傳聞系統嗰陣漏咗一行

- v266（9bb08fc）L12695 有定義：
  `applyPhase2Steps56TabLabel()`——純傳聞教學 label 邏輯，幫已刪嘅
  `#htab-rumor`／`#rumor-list` 設 label，依賴同樣已刪嘅
  `phase2Steps56Line`。
- v267（491958a）刪傳聞系統嗰陣正確刪走咗個定義＋guarded 呼叫＋另一行
  裸呼叫（diff 顯示三處 `-`），但漏咗 `setHomeTab` 入面嗰行裸呼叫
  （diff 入面嗰行只係 context，冇刪到）。
- 之後每次 `setHomeTab()` 都喺第三行掟錯，之後嘅 `book70SyncTabGroups`、
  pane 切換、pane 渲染全部唔行——tab 撳落去靜默無反應（event handler
  入面嘅 exception 只入 console，玩家面睇唔到）。
- 連帶傷害：`enterHome` 喺 `setHomeTab(_homeTab)` 之後先呼叫
  `renderNotebook()`，而且嗰個呼叫無 try/catch，入屋流程喺嗰度斷埋——
  `#nb-days` 空白（瀏覽器報告話「本週行程空白」）、`wireHome265()` 無
  行（瞓覺／衣櫃掣無接線）、`saveQ()` 無行。`#home-stats` 喺
  `setHomeTab` 之前已經填好，所以銀包／聲望／信用照常顯示；`show("v-home")`
  亦喺之前，所以面板照樣出現；「行程已定」印章經另一條路
  （`syncConfirmPlanStamp197` 其他呼叫點）出，唔受影響。
- 返回地圖獨善其身：`#home-back-map-tabs` 嘅 handler 直行
  `book70ExitHome`，唔經 `setHomeTab`。
- 點解而家先捉到：v267 落地之後瀏覽器死咗兩日（11-15 至 11-17 19:31），
  19:36 嗰次係首次開手帳面板實檢。

## 修復（index.html 淨 +3 行）

1. `setHomeTab`：刪走殘留裸呼叫 `applyPhase2Steps56TabLabel();`（附註解
   說明來龍去脈）。唔恢復個函數——佢係傳聞教學專用，恢復等於復活已刪
   嘅教學邏輯。
2. `enterHome`：`setHomeTab(_homeTab)` 加 `try{...}catch(_e){}` 防禦——
   tab 切換失敗唔可以再拖死成個入屋流程（renderNotebook／wireHome265／
   saveQ）。其他 `setHomeTab` 呼叫點經核實全部已有 try/catch。

## 驗證

- node 抽修復後嘅 `setHomeTab`＋DOM stub：`works`／`ledger`／
  `clippings`／`debt`／`plan` 五個 tab 全部 OK，每個恰好一個 pane 變 `on`。
- 新測試 `tests/test_home272_static.py` **24 項 ALL PASS**：殘留呼叫零、
  setHomeTab 本體完整、setHomeTab 呼叫嘅每個頂層函數都有定義（呢個就係
  v272 失敗類別嘅回歸檢查）、enterHome 有防禦、瞓覺／衣櫃接線路徑在位、
  node --check、紅線（SAVE key／softRev／?v=）不變。
- 全檔其他傳聞教學呼叫名全部零殘留：`renderRumorPane`／
  `phase2Steps56Line`／`rumorTutorialDone`／`markRumorTutorialDone`／
  `skipRumorTutorial`／`phase2Steps56CoachHtml`／
  `loadTutorialPhase2Steps56Overlay`／`TUTORIAL_PHASE2_STEPS56` 全部 0；
  `tutorialPhase2FxOn`／`tutorialPhase2Steps56SelfCheck` 各 1 次，全部只係
  註解（前者 v267 NOTES 已記錄）。
- `node --check` 主 script 通過。
- 全套 suite：見下面。

## Suite

- 第一輪（v270 base）：**330／15**——對基線 335／9 多咗 6 項 FAIL，
  全部係修復淨 +3 行造成嘅純行數漂移（gift185／rom159／rom176／
  tang171／tang173／travel114），difflib 對位核實 62 個錨點內容逐字相同。
- resync 後第二輪：**336／9**——335 基線＋新檔 test_home272_static.py；
  FAIL 名單同基線逐項一致（flash51／slot50／soft_tip_111_restore／
  start53／weave43_static／weave44_static／weave49_static／wf5_87／
  wrap38），零回歸。
- **rebase 上 v271**：v271（支線補完第二批）喺 v272 suite 第二輪期間
  落地，main 變咗 f25df08（suite 336／9 新基線）。v272 commit rebase
  上新 main：index.html 兩處改動乾淨套用（無衝突），6 檔測試 resync
  有衝突——原因係 v271 亦 resync 過同一批釘行。解法：取 v271 版測試檔
  做底，對照 v271 index.html → 工作副本 index.html（45463→45466，
  淨 +3）重新 difflib 映射（COUNT 20991→20994 等 10 處＋3、FREE
  38877→38880 等 30 處＋3、DEF 40713→40716、rom159 25198→25201 等、
  rom176 39079→39082 等；≤插入點錨點＋0），逐檔單次掃描 dict 查表
  重寫；6 檔逐個重跑全部 PASS。rebase 完成後全套重跑：**337／9**
  （336 v271 基線＋新檔 1 項，FAIL 名單同基線逐項一致），零回歸。

## 留低

- 瀏覽器重驗（新存檔開局 $1,200，撳四個 tab＋衣櫃＋瞓覺）要 parent
  安排——subagent 無瀏覽器操作權限。修復本身已經由 node 功能驗證＋
  靜態測試釘死，瀏覽器重驗係確認畫面層。
- v273 跟進（唔入 v272）：顧明輝 heart fx 關鍵字對唔上 live label
  （「天光」vs「陪他坐到天亮，不出聲」，+1 唔係 +3）＋陸 heart
  foreshadow 錯過放寬（用戶 19:52 已拍板）——parent 獨立核實，留
  v273 修。
