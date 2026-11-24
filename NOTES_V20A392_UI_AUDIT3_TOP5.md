# NOTES_V20A392_UI_AUDIT3_TOP5.md

v392：第三輪全畫面 UI 再檢視（2026-11-24，`~/workspace/linji-ui-audit-2026-11-24b/REPORT.md`，GPT A 0／B 5／C 76、Gemini A 0／B 71／C 10）頭五項必修實裝。用戶 2026-11-24 16:01 下令「直到 GPT 覺得全部畫面 A 級先停下來畀我睇」——檢視→修正→再檢視循環自動接續。

⚠️ **尺度警告**：今輪 GPT 把尺收緊咗（「有一項硬傷即 C」、「似網頁報表」列為硬傷），62 屏 B→C 係尺度效應，**唔係 v391 退步**。

## 1. 40／27／86 家族：撳外面／撳卡外唔准推進日期
- 修法：`afterDayModal` dismiss 改 `ended? go: null`（週結照去屋企結算，嗰步唔推進日期；非週結只收起卡）；日結 modal（`dismissNb`）同樣 `ended? nextNbReward: null`；`presentRestSleepDayEnd`（86 家族）dismiss 改 `ended? goSchedule: null`；`presentStartScheduleConfirm45`（40）重寫——金掣「開始今日行程」→「開始並結算當日」，取消掣→「返回休息卡」，後果寫入正文，onDismiss＝有 onCancel 就行取消（返休息卡），冇就 null（永不開始／返地圖）；刪走 `dayEndDismissNote202` 函數＋兩屏底部「點擊外面＝⋯」細字。一次過套用到成個日結／休息卡家族。
- 刻意無郁：`flushWeekAccelSummary` 嘅 onDismiss（週加速自動繼續係重點，範圍外）；`rom159DateScene` 約會結果卡（範圍外）。
- 實測（Playwright，`~/workspace/linji-drive392-ui/`，2＋1 輪）：1a 日結 modal 撳外面 day 2→2、weekPlan 無變；1b 休息卡撳外面 day 3→3；1c 確認 40 撳外面返返休息卡 day 4→4；1d afterDayModal 撳外面 day 5→5。全部通過。

## 2. 39 拍攝排程：刪「取消」、金色畀安全選項
- 修法：`confirmPlaceShoot` 重寫——`go(overwrite, defer)`；defer 記 `shoot._v392defer=true`，跳過 `placeShootOnPlan`（唔郁 weekPlan／daysLeft），照行 thenFn；安全掣金色（有空日「只排空日」；冇空日「留待下週」）；覆寫用次級掣「取消原安排並拍攝」；「取消」掣已刪；無 onDismiss（撳遮罩只收起 modal）；警告直接講損失＋`.shoot-warn392`（#9c2418、800 字重、「會取消」900）。
- ⚠️ 實駕教訓：`.shoot-warn392` 實算色起初係 #3a2e22 而唔係 #9c2418——`#mask:not(.tut-on).modal p{color:#3a2e22!important}`（v391 規則）壓住普通 class；要補高權重覆寫 `#mask:not(.tut-on).modal p.shoot-warn392{ color:#9c2418!important;}` 先贏到。靜態測試已釘住呢條覆寫。
- 實測（真試鏡路徑，2＋1 輪）：A 2 空日→「只排空日」只排入空日（daysLeft 剩 1）；B 0 空日→「留待下週」weekPlan 無變、shoot 記 defer 旗、finishReveal 講「拍攝日留待下週再排。」；C 撳外面 mask 關、weekPlan／shoots 無變、無 finishReveal；D「取消原安排並拍攝」覆寫＋finishReveal。警告色實測 rgb(156,36,24)＝#9c2418，對實測紙底 6.59:1。
- 取捨（記低）：39 modal 撳外面唔出獲聘通知，shoot 由下週編排 `lockShootsIntoDraft` 兜底排入；`aud91PresentOne` 呈現前已將 record 剔出 `pendingAud`，`grant229Drop(rec)` 亦喺 `confirmPlaceShoot` 之前，所以唔會重播／重複獲聘。

## 3. 通告欄峰值分層
- 修法：預設按預期日薪（`chance × 片酬 ÷ 拍攝日數`）排序，標明「按預期日薪」，可切換總片酬／成功率；板頂固定總數行；短卡改可掃讀紙條（`$378｜3 日｜86%` 同一行，卡高 141→**92.3px**）；媒介吊牌篩選（全部／電視劇／綜藝），唔做預設摺疊；推介大卡（可接之中片酬最高者，鎖定卡唔入推介）；未達標組標題上移並附「最接近」預覽行；細板直出（≤3 張唔加分層；0 張可接直寫「今日冇可接通告」）。
- ⚠️ **TDZ 回歸（實駕捉到，v392 引入）**：我寫嘅 meta-line 區塊插喺 `const boardState` 聲明之前，但入面讀 `boardState`，撞 temporal dead zone——`gigBoardTeaserHtml` 一叫即 `ReferenceError: Cannot access 'boardState' before initialization`，`doScout` 掟 exception、板面撳極都唔開（只彈「行動未能完成」toast）。修法：將 `lifeKey`／`boardState` 兩行搬去 meta-line 區塊之前，刪走後面重複聲明；靜態測試加釘（聲明行必須喺讀取行之前＋全函數只聲明一次）。
- ⚠️ **高版 modal 初版唔生效**：`#mask.board-tall392 .modal{ max-height:min(92dvh,780px); }` 輸畀 `#mask:not(.tut-on) .modal` 嗰條 78dvh `!important`（同權重、冇 `!important` 贏唔到）。跟 day-res 前例加 `!important`（我條寫喺後面，同權重後者贏）＋補 `92svh` 後備帽，先至生效。
- 實測（峰值：星河電視台 day 7，16 張）：第一眼完整 **5 張**（修前 3 張；目標 5–6，取下限；第 6 張探頭）；卡高 92.3px；總數行「共 16 張 · 可接 16 張 · 未達標 0 張」；推介＝冬日鄰里情（$378 最高）；總片酬排序頭三 $378＞$284＝$284；電視劇篩選剩 10 張；板頂 sticky、scroller 673px（修前 555px）。頭行 head 收身 110→96px。

## 4. 18 稱號段同一屏「拍攝簿」截字
- 成因：`#home-pane-works` 係 `display:flex; overflow:hidden`，`#works-list`（flex:1）被稱號摺疊內容壓到約 25px，夾住身為其第一個子元素嘅 `<h3 class="jobs72-h">拍攝簿</h3>` 下半。
- 修法：CSS `#app #home-pane-works{ overflow-y:auto; background:#f3e6c8;}`、`#app #home-pane-works #works-list{ flex:0 0 auto; overflow:visible;}`，等成頁一齊捲。稱號段本身唔郁（內文 11.48:1、印章 6.31:1）；「去獎項頁睇入圍同得獎紀錄」掣唔刪（GPT 建議第 ④ 項超出範圍）。
- 實測：`.jobs72-h` rect h23（完整行高），`hFullyInsidePane: true`，`#works-list` h621（修前約 25px），pane scrollHeight 1252＞clientHeight 528。

## 5. 35 頒獎系列：快進提示 3.89:1 → ≥4.5:1＋雙焦
- 修法：`.awd62-tap` 搬入 `.awd62-canvaswrap`（跳過掣隔籬），色改 #d6cdf0、700 字重、文字陰影；nominee beat 字幕只留進度（「入圍名單 n/N · 獎項名」），名＋作品集中去舞台吊牌（`syncBoardSub392`：頭 500ms 隱藏、之後先揭名）；未揭曉卡實色卡背（`::before`「？」漸變 #3a2a4a→#241736、金字 #f2c14e；img／名／作品 `visibility:hidden`；得主角標未揭嗰陣隱藏）。
- 實測：tap 實算色 #d6cdf0，對實測底 rgb(67,59,45)＝**7.28:1**（像素採樣 13.04:1），同跳過掣同一行；12 個 nominee beat 全部字幕零漏名（`caption_name_leak: []`），吊牌隱藏 0.43–0.47s、0.53–0.59s 後揭名（500ms 設計）；未揭曉卡樣本 45–46 個，`::before` content「？」＋漸變底。頒獎結果卡（`.awd-sheet`）今輪未驗證、無郁，列入下一輪補截。
- tap div 搬去 skip 掣之前後重跑 3＋5 輪（2026-11-24）量度不變（rect x9.5 y334.4、對比 7.28、採樣 13.04、sameRow；板面第一眼完整 5 張、卡高 92.3px；nominee beat 12 個、字幕零漏名、未揭曉卡樣本 45 個）。
- 註：nominee 截圖條件（nominee cap＋nShown==0）一次都冇命中——nominee beat 開始嗰陣卡已有揭開狀態，係 driver 條件寫窄咗，唔係產品問題；舞台截圖 `35b_awards_1.png`（吊牌只寫類別＋「入圍名單逐一揭曉」）＋輪詢數字已足夠證實雙焦。

## 測試
- 新增 `tests/test_v392_ui_static.py`（釘 v392 CSS 區塊、五項標記、對比度實算、TDZ 次序、高版 modal）＋`tests/test_v392_ui_logic.js`（`board392Compare` 排序、`confirmPlaceShoot` 四態）——ALL PASS。
- 更新 `tests/test_dayend202_logic.js`（dismiss 斷言＋標籤）＋`tests/test_terms57_static.py` A4——ALL PASS。
- 更新其餘受 brief 改動影響嘅測試——全部 ALL PASS：`test_dayend202_static.py`（8 項）、`test_dayflow196_static.py`（4 項）、`test_flow45_static.py`（2 項）、`test_aud91fix122_static.py`＋`test_aud91fix122_logic.js`（H2 重寫）、`test_r295_click_not_gam.js`（dismiss notes x4 改斷言）、`test_s30dedup117_static.py` D3、`test_ui108_static.py` S-29、`test_guidance34_static.py`、`test_r335_board_favor158_hint.js`、`test_awards166_static.py`、`test_buttons197_static.py`。
- **resync**（`qa392/resync392.py`，difflib 對位，舊基底 main HEAD 967e2d8）：index.html 淨 **+146 行**（49753→49899）；travel114（COUNT／FREE 零移除、DEF 44847→44938、WRAPPER 31067→31128）、rom159（6 釘＋全佳 27225→27284）、rom176（6 釘）、tang152（2 釘）、text125（3 錨點）、gift185／tang171／tang173（總行數＋openLoc DEF）——逐行核實內容相同，純漂移。
- ⚠️ **「7 項 flake」係誤判**：首輪 suite 後 7 項 .js 邏輯測試被當成 flake（話直接跑 PASS），實情係佢哋抽已刪嘅 `dayEndDismissNote202`——直接跑係真 FAIL（`fn not found: dayEndDismissNote202`）。其中 dayflow196／flow45 仲有舊 dismiss 行為斷言（dismiss 行程／返地圖），已按 v392 契約重寫（非週結 dismiss＝null 乜都唔做；確認 dismiss＝返休息卡；確認金掣「開始並結算當日」）；其餘 5 檔（aud91／levels75／rest58／stamina58／verify37）只刪載入。改完 7 檔逐個跑 ALL PASS。
- 實駕：`~/workspace/linji-drive392-ui/drive392ui.py`（項目 1／2／4 喺 2＋1 輪驗過，項目 3／5 喺 3＋5 輪驗過；截圖＋measurements.json 喺 verify/）。⚠️ 2＋1 輪嘅 measurements.json 其後被 3＋5 輪覆寫，第 2 項 D case 詳情以本 NOTES 記錄為準；第 1／2／4 項 code 路徑自驗證後未再郁過。
- Suite：`bash qa131/run_suite.sh ~/workspace/linji-work392-ui ~/workspace/suite392_out3.txt` → **TOTAL PASS 409 FAIL 9**（基線 407＋2 新測試檔；9 項全部係已知 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38）。首輪 382／36 係因為 12 項 brief 改動測試未更新＋7 項行號釘未 resync＋7 項邏輯測試未跟進 dayEndDismissNote202 刪除——全部已修，見上。
- 跑完 suite 已還原 `qa296/derive296.json`（`git checkout -- qa296/derive296.json`；suite 再生 +513/−268 行，唔入版）。

## 出貨
- SAVE key／softRev／產品 `?v=` 不變。
- index.html 淨改動：+252／−106 行（總行數 49753→49899，淨 +146）。全版共 26 個已追蹤檔改動＋4 個新檔（NOTES、qa392/resync392.py、tests/test_v392_ui_static.py、tests/test_v392_ui_logic.js）。
